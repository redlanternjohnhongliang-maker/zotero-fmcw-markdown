from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.io import loadmat

from d1a_gao77_clean_fixed_pfa_sanity import (
    EXPECTED_ADC_SHAPE,
    RADAR_DIR,
    ROOT,
    VALID_RANGE_MAX_BIN,
    VALID_RANGE_MIN_BIN,
    radar_maps,
    write_csv,
    write_json,
)
from d1b_gao77_synthetic_interference_sanity import EPS, SIR_CONFIGS as D1B_SIR_CONFIGS, build_mask_context, make_interference
from d2a_gao77_small_model_sanity import load_clean_data, load_split, mse_np, power_from_db
from d5b_d5c_weak_definition_rdra_diagnosis import relation_stats_for_context


RESULT_DIR = ROOT / "results" / "d5d_rd_only_supplementary"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5d_rd_only_figures"
SUMMARY_PATH = RESULT_DIR / "d5d_rd_summary.md"
GO_NOGO_PATH = RESULT_DIR / "d5d_rd_go_nogo_decision.md"

RANDOM_SEED = 20260627
TRAIN_SIR_NAMES = ["light", "medium"]
EVAL_SIR_NAME = "medium"
N_TRAIN_FRAMES = 96
N_VAL_FRAMES = 96
N_TEST_FRAMES = 96
SEEDS = [42, 200]

PRIMARY_PFA = 1e-2
SECONDARY_PFA = 1e-3
TARGET_PFAS = [PRIMARY_PFA, SECONDARY_PFA]
SPLIT_DEFINITION = "frozen_clean_peak_overlap_aware"
WEAK_WEIGHT = 2.0
LAMBDA_REC = 0.5

BATCH_SIZE = 2
TINY_SAMPLE_COUNT = 12
TINY_STEPS = 35
SMALL_EPOCHS = 5
LR = 3e-4
RD_TEMPERATURE_DB = 2.0


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def f(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value in ("", None):
        return default
    return float(value)


def i(row: dict[str, Any], key: str, default: int = 0) -> int:
    value = row.get(key, default)
    if value in ("", None):
        return default
    return int(float(value))


def md_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in rows:
        vals = []
        for col in cols:
            val = row.get(col, "")
            if isinstance(val, bool):
                vals.append("True" if val else "False")
                continue
            if isinstance(val, float):
                vals.append(f"{val:.4f}")
            else:
                try:
                    vals.append(f"{float(val):.4f}" if val not in ("", None) else "")
                except Exception:
                    vals.append(str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def direction_consistent(a: float, b: float) -> bool:
    return (abs(a) < 1e-12 and abs(b) < 1e-12) or (a * b >= 0.0)


def write_versioned_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8-sig")
    path.write_text(text, encoding="utf-8-sig")
    return ts_path


def write_versioned_json(path: Path, obj: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    return ts_path


def append_manifest(outputs: list[tuple[Path, str]]) -> None:
    if len(outputs) <= 15:
        return
    manifest = ROOT / "MANIFEST.md"
    if not manifest.exists():
        manifest.write_text(
            "# Research Output Manifest\n\n"
            "> Auto-maintained by ARIS skills. Tracks all generated artifacts across the research lifecycle.\n\n"
            "| Timestamp | Skill | File | Stage | Description |\n"
            "|-----------|-------|------|-------|-------------|\n",
            encoding="utf-8",
        )
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    for path, desc in outputs:
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        lines.append(f"| {stamp} | /experiment-bridge | {rel} | implementation | {desc} |")
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def sir_cfg(name: str) -> dict[str, Any]:
    for cfg in D1B_SIR_CONFIGS:
        if str(cfg["sir_name"]) == name:
            return cfg
    raise KeyError(name)


def valid_range_mask_2d(shape: tuple[int, int]) -> np.ndarray:
    mask = np.zeros(shape, dtype=bool)
    mask[VALID_RANGE_MIN_BIN : min(VALID_RANGE_MAX_BIN + 1, shape[0]), :] = True
    return mask


def rects_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    return max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3])


def clean_peak_frozen_splits(
    ctx: dict[str, Any],
    targets: list[Any],
    train_frames: np.ndarray,
) -> tuple[dict[int, str], dict[str, Any]]:
    train_set = {int(x) for x in train_frames.tolist()}
    values = ctx["target_values"]
    train_values = {
        int(t.target_id): float(values[int(t.target_id)]["target_peak_db"])
        for t in targets
        if int(t.frame_idx) in train_set
        and int(t.target_id) in values
        and values[int(t.target_id)].get("valid_projection")
    }
    vals = np.asarray(list(train_values.values()), dtype=np.float64)
    if vals.size == 0:
        raise RuntimeError("no train targets available for frozen weak threshold")
    q30, q70 = np.quantile(vals, [0.3, 0.7])
    relation = relation_stats_for_context(ctx, targets)
    splits: dict[int, str] = {}
    weak_candidate_ids: set[int] = set()
    filtered_ids: set[int] = set()
    for tid_raw, item in values.items():
        tid = int(tid_raw)
        if not item.get("valid_projection"):
            continue
        peak = float(item["target_peak_db"])
        if peak <= q30:
            weak_candidate_ids.add(tid)
            nearest_raw = relation.get(tid, {}).get("nearest_target_distance_bins", 99.0)
            nearest = 99.0 if nearest_raw == "" else float(nearest_raw)
            keep_weak = (
                not relation.get(tid, {}).get("stronger_overlap", False)
                and not relation.get(tid, {}).get("range_bin_conflict", False)
                and nearest >= 2.0
            )
            if keep_weak:
                splits[tid] = "weak"
            else:
                splits[tid] = "mid"
                filtered_ids.add(tid)
        elif peak <= q70:
            splits[tid] = "mid"
        else:
            splits[tid] = "strong"

    by_frame = {int(t.target_id): int(t.frame_idx) for t in targets}
    counts: dict[str, dict[str, int]] = {}
    for name, frame_ids in {
        "train": set(int(x) for x in train_frames.tolist()),
    }.items():
        ids = [tid for tid in splits if by_frame.get(tid) in frame_ids]
        c = Counter(splits[tid] for tid in ids)
        counts[name] = {"weak_n": c["weak"], "mid_n": c["mid"], "strong_n": c["strong"]}

    meta = {
        "split_definition": SPLIT_DEFINITION,
        "threshold_source": "train split only",
        "train_target_peak_db_q30_weak_threshold": float(q30),
        "train_target_peak_db_q70_strong_threshold": float(q70),
        "train_target_count_for_threshold": int(vals.size),
        "weak_candidate_count_all_frames": len(weak_candidate_ids),
        "overlap_filtered_weak_candidate_count_all_frames": len(filtered_ids),
        "threshold_leakage": False,
        "used_test_clean_map_property_for_threshold": False,
        "repair_rule": "clean_peak <= train q30, then remove stronger-overlap/range-bin-conflict/nearest<2-bin weak candidates to mid",
        "counts": counts,
    }
    return splits, meta


def split_counts_for_frames(splits: dict[int, str], targets: list[Any], frames: np.ndarray) -> dict[str, int]:
    frame_set = {int(x) for x in frames.tolist()}
    ids = [int(t.target_id) for t in targets if int(t.frame_idx) in frame_set and int(t.target_id) in splits]
    c = Counter(splits[tid] for tid in ids)
    return {"weak_n": c["weak"], "mid_n": c["mid"], "strong_n": c["strong"], "target_n": len(ids)}


def compute_rd_maps(
    manifest: list[dict[str, str]],
    frame_indices: np.ndarray,
    sir_names: list[str],
    rng: np.random.Generator,
) -> tuple[dict[int, np.ndarray], dict[str, dict[int, np.ndarray]], list[dict[str, Any]]]:
    clean_rd: dict[int, np.ndarray] = {}
    inter_rd: dict[str, dict[int, np.ndarray]] = {name: {} for name in sir_names}
    rows: list[dict[str, Any]] = []
    for frame_idx_raw in frame_indices.tolist():
        frame_idx = int(frame_idx_raw)
        adc = loadmat(RADAR_DIR / manifest[frame_idx]["new_radar_file"])["adcData"]
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"unexpected adcData shape {adc.shape}")
        _rp, rd_map, _ra = radar_maps(adc)
        clean_rd[frame_idx] = rd_map.astype(np.float32)
        for name in sir_names:
            cfg = sir_cfg(name)
            interfered_adc, params, summary = make_interference(adc, float(cfg["sir_db"]), int(cfg["num_interferers"]), rng)
            _irp, ird_map, _ira = radar_maps(interfered_adc)
            inter_rd[name][frame_idx] = ird_map.astype(np.float32)
            rows.append(
                {
                    "frame_idx": frame_idx,
                    "frame_id": manifest[frame_idx]["new_frame_id"],
                    "source_sequence": manifest[frame_idx]["source_sequence"],
                    "sir_name": name,
                    "target_sir_db": float(cfg["sir_db"]),
                    "num_interferers": int(cfg["num_interferers"]),
                    "achieved_sir_db": summary["achieved_sir_db"],
                    "interference_params_json": json.dumps(params, ensure_ascii=False),
                }
            )
    return clean_rd, inter_rd, rows


def build_sample_arrays(
    frames: np.ndarray,
    sir_names: list[str],
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    split_name: str,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]]]:
    xs: list[np.ndarray] = []
    ys: list[np.ndarray] = []
    rows: list[dict[str, Any]] = []
    sample_id = 0
    for frame_idx_raw in frames.tolist():
        frame_idx = int(frame_idx_raw)
        for name in sir_names:
            sample_id += 1
            xs.append(inter_rd[name][frame_idx])
            ys.append(clean_rd[frame_idx])
            rows.append({"sample_id": f"{split_name}_{sample_id:05d}", "split": split_name, "frame_idx": frame_idx, "sir_name": name})
    return np.stack(xs).astype(np.float32), np.stack(ys).astype(np.float32), rows


def build_rd_context(
    clean_rd: dict[int, np.ndarray],
    targets: list[Any],
    range_ctx: dict[str, Any],
    splits: dict[int, str],
    frame_indices: np.ndarray,
    mask_name: str,
) -> dict[str, Any]:
    frame_set = {int(x) for x in frame_indices.tolist()}
    shape = next(iter(clean_rd.values())).shape
    target_mask_by_frame = {idx: np.zeros(shape, dtype=bool) for idx in frame_set}
    guard_mask_by_frame = {idx: np.zeros(shape, dtype=bool) for idx in frame_set}
    rect_by_target: dict[int, tuple[int, int, int, int]] = {}
    intervals = range_ctx["intervals"]
    doppler_radius = 1 if mask_name == "narrow" else 2
    doppler_guard = 3 if mask_name == "narrow" else 5
    range_guard = 3 if mask_name == "narrow" else 4
    for target in targets:
        tid = int(target.target_id)
        frame_idx = int(target.frame_idx)
        if frame_idx not in frame_set or tid not in intervals or tid not in splits:
            continue
        rd = clean_rd[frame_idx]
        lo, hi, _radius = intervals[tid]
        sub = rd[lo:hi, :]
        if sub.size == 0:
            continue
        _r, doppler_center = np.unravel_index(int(np.argmax(sub)), sub.shape)
        dlo = max(0, int(doppler_center) - doppler_radius)
        dhi = min(shape[1], int(doppler_center) + doppler_radius + 1)
        gdlo = max(0, int(doppler_center) - doppler_guard)
        gdhi = min(shape[1], int(doppler_center) + doppler_guard + 1)
        grlo = max(0, lo - range_guard)
        grhi = min(shape[0], hi + range_guard)
        target_mask_by_frame[frame_idx][lo:hi, dlo:dhi] = True
        guard_mask_by_frame[frame_idx][grlo:grhi, gdlo:gdhi] = True
        rect_by_target[tid] = (lo, hi, dlo, dhi)

    background_mask_by_frame: dict[int, np.ndarray] = {}
    valid = valid_range_mask_2d(shape)
    for frame_idx in frame_set:
        guard_ring = np.logical_and(guard_mask_by_frame[frame_idx], ~target_mask_by_frame[frame_idx])
        background_mask_by_frame[frame_idx] = np.logical_and(valid, ~np.logical_or(target_mask_by_frame[frame_idx], guard_ring))

    by_frame: dict[int, list[int]] = defaultdict(list)
    for target in targets:
        tid = int(target.target_id)
        if tid in rect_by_target:
            by_frame[int(target.frame_idx)].append(tid)
    overlapped: set[int] = set()
    for tids in by_frame.values():
        for ix, tid in enumerate(tids):
            for oid in tids[ix + 1 :]:
                if rects_overlap(rect_by_target[tid], rect_by_target[oid]):
                    overlapped.add(tid)
                    overlapped.add(oid)
    non_overlap_ids = {tid for tid in rect_by_target if tid not in overlapped}
    return {
        "mask_name": mask_name,
        "shape": shape,
        "target_mask_by_frame": target_mask_by_frame,
        "background_mask_by_frame": background_mask_by_frame,
        "guard_mask_by_frame": guard_mask_by_frame,
        "rect_by_target": rect_by_target,
        "splits": {SPLIT_DEFINITION: splits},
        "non_overlap_ids": non_overlap_ids,
        "doppler_radius": doppler_radius,
        "doppler_guard": doppler_guard,
        "range_guard": range_guard,
        "projection_note": "Doppler center is projected from the clean RD peak inside the range-label interval; no Doppler GT is available.",
    }


def stack_masks(rows: list[dict[str, Any]], rd_ctx: dict[str, Any], key: str, device: torch.device) -> torch.Tensor:
    arr = np.stack([rd_ctx[key][int(row["frame_idx"])] for row in rows]).astype(bool)
    return torch.from_numpy(arr).to(device)


def stack_weights(rows: list[dict[str, Any]], weight_by_frame: dict[int, np.ndarray], device: torch.device) -> torch.Tensor:
    arr = np.stack([weight_by_frame[int(row["frame_idx"])] for row in rows]).astype(np.float32)
    return torch.from_numpy(arr).to(device)


def make_weight_by_frame(rd_ctx: dict[str, Any], targets: list[Any], frame_indices: np.ndarray, weak_weight: float) -> dict[int, np.ndarray]:
    frame_set = {int(x) for x in frame_indices.tolist()}
    shape = rd_ctx["shape"]
    splits = rd_ctx["splits"][SPLIT_DEFINITION]
    rects = rd_ctx["rect_by_target"]
    out = {idx: np.zeros(shape, dtype=np.float32) for idx in frame_set}
    for target in targets:
        tid = int(target.target_id)
        frame_idx = int(target.frame_idx)
        if frame_idx not in frame_set or tid not in rects:
            continue
        rlo, rhi, dlo, dhi = rects[tid]
        weight = float(weak_weight) if splits.get(tid) == "weak" else 1.0
        out[frame_idx][rlo:rhi, dlo:dhi] = np.maximum(out[frame_idx][rlo:rhi, dlo:dhi], weight)
    return out


def normalize(arr: np.ndarray, mean: float, std: float) -> np.ndarray:
    return ((arr - mean) / max(std, EPS)).astype(np.float32)


def denormalize(arr: np.ndarray, mean: float, std: float) -> np.ndarray:
    return arr.astype(np.float64) * max(std, EPS) + mean


def make_tensor(arr: np.ndarray, mean: float, std: float, device: torch.device) -> torch.Tensor:
    return torch.from_numpy(normalize(arr, mean, std)[:, None, :, :]).to(device)


def db_tensor_from_norm(x: torch.Tensor, mean: float, std: float) -> torch.Tensor:
    return x[:, 0, :, :] * max(std, EPS) + mean


class TinyRDResidualCNN(nn.Module):
    def __init__(self, channels: int = 8) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(channels, channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(channels, 1, kernel_size=3, padding=1),
        )
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.net(x)


def soft_rd_detection(out_norm: torch.Tensor, mean: float, std: float, threshold: float) -> torch.Tensor:
    out_db = db_tensor_from_norm(out_norm, mean, std)
    return torch.sigmoid((out_db - threshold) / RD_TEMPERATURE_DB)


def balanced_detection_loss(
    out: torch.Tensor,
    tm: torch.Tensor,
    bm: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
    pos_weight: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    soft = soft_rd_detection(out, mean, std, threshold).clamp(1e-6, 1.0 - 1e-6)
    labels = torch.zeros_like(soft)
    labels[tm] = 1.0
    valid = tm | bm
    bce = F.binary_cross_entropy(soft, labels, reduction="none")
    weights = torch.zeros_like(soft)
    weights[bm] = 1.0
    weights[tm] = float(pos_weight)
    det = torch.sum(bce[valid] * weights[valid]) / torch.sum(weights[valid]).clamp_min(1.0)
    target_det = torch.mean(bce[tm]) if bool(tm.any()) else torch.tensor(0.0, device=out.device)
    background_det = torch.mean(bce[bm]) if bool(bm.any()) else torch.tensor(0.0, device=out.device)
    return det, target_det, background_det


def weak_detection_loss(
    out: torch.Tensor,
    tm: torch.Tensor,
    bm: torch.Tensor,
    tw: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    soft = soft_rd_detection(out, mean, std, threshold).clamp(1e-6, 1.0 - 1e-6)
    labels = torch.zeros_like(soft)
    labels[tm] = 1.0
    valid = tm | bm
    bce = F.binary_cross_entropy(soft, labels, reduction="none")
    weights = torch.zeros_like(soft)
    weights[bm] = 1.0
    weights[tm] = tw[tm].clamp_min(1.0)
    det = torch.sum(bce[valid] * weights[valid]) / torch.sum(weights[valid]).clamp_min(1.0)
    target_det = torch.mean(bce[tm]) if bool(tm.any()) else torch.tensor(0.0, device=out.device)
    background_det = torch.mean(bce[bm]) if bool(bm.any()) else torch.tensor(0.0, device=out.device)
    return det, target_det, background_det


def infer_rd(model: nn.Module, arr_db: np.ndarray, mean: float, std: float, device: torch.device) -> np.ndarray:
    model.eval()
    outs: list[np.ndarray] = []
    with torch.no_grad():
        for start in range(0, arr_db.shape[0], 12):
            batch = make_tensor(arr_db[start : start + 12], mean, std, device)
            pred = model(batch).detach().cpu().numpy()[:, 0, :, :]
            outs.append(denormalize(pred, mean, std))
    return np.concatenate(outs, axis=0).astype(np.float32)


def train_model(
    method: str,
    seed: int,
    train_x: np.ndarray,
    train_y: np.ndarray,
    train_rows: list[dict[str, Any]],
    val_x: np.ndarray,
    val_y: np.ndarray,
    val_rows: list[dict[str, Any]],
    rd_ctx: dict[str, Any],
    targets: list[Any],
    val_frames: np.ndarray,
    clean_rd: dict[int, np.ndarray],
    mean: float,
    std: float,
    device: torch.device,
) -> tuple[nn.Module | None, list[dict[str, Any]], dict[str, Any]]:
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = TinyRDResidualCNN().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    train_tm = stack_masks(train_rows, rd_ctx, "target_mask_by_frame", device)
    train_bm = stack_masks(train_rows, rd_ctx, "background_mask_by_frame", device)
    val_tm = stack_masks(val_rows, rd_ctx, "target_mask_by_frame", device)
    val_bm = stack_masks(val_rows, rd_ctx, "background_mask_by_frame", device)
    train_pos = int(train_tm.sum().item())
    train_neg = int(train_bm.sum().item())
    pos_weight = math.sqrt(float(train_neg / max(train_pos, 1)))
    threshold_values = []
    for frame_idx in val_frames.tolist():
        frame = int(frame_idx)
        threshold_values.append(clean_rd[frame][rd_ctx["background_mask_by_frame"][frame]])
    detection_threshold = float(np.quantile(np.concatenate(threshold_values), 1.0 - PRIMARY_PFA))
    weight_by_frame = make_weight_by_frame(rd_ctx, targets, np.asarray([int(r["frame_idx"]) for r in train_rows]), WEAK_WEIGHT)
    val_weight_by_frame = make_weight_by_frame(rd_ctx, targets, np.asarray([int(r["frame_idx"]) for r in val_rows]), WEAK_WEIGHT)
    train_tw = stack_weights(train_rows, weight_by_frame, device)
    val_tw = stack_weights(val_rows, val_weight_by_frame, device)
    rows: list[dict[str, Any]] = []
    stopped_reason = ""

    def loss_terms(
        out: torch.Tensor,
        target_norm: torch.Tensor,
        tm: torch.Tensor,
        bm: torch.Tensor,
        tw: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        if method == "balanced_mild":
            det, target_det, background_det = balanced_detection_loss(out, tm, bm, mean, std, detection_threshold, pos_weight)
        else:
            det, target_det, background_det = weak_detection_loss(out, tm, bm, tw, mean, std, detection_threshold)
        rec = torch.mean((db_tensor_from_norm(out, mean, std) - db_tensor_from_norm(target_norm, mean, std)) ** 2)
        return det + LAMBDA_REC * rec, det, rec, target_det, background_det

    tiny_n = min(TINY_SAMPLE_COUNT, x.shape[0])
    tiny_x = x[:tiny_n]
    tiny_y = y[:tiny_n]
    tiny_tm = train_tm[:tiny_n]
    tiny_bm = train_bm[:tiny_n]
    tiny_tw = train_tw[:tiny_n]
    with torch.no_grad():
        init_loss, _init_det, _init_rec, _it, _ib = loss_terms(model(tiny_x), tiny_y, tiny_tm, tiny_bm, tiny_tw)
        tiny_initial = float(init_loss.item())
    try:
        for step in range(1, TINY_STEPS + 1):
            idx = torch.randint(0, tiny_n, (min(BATCH_SIZE, tiny_n),), device=device)
            out = model(tiny_x[idx])
            loss, det, rec, target_det, background_det = loss_terms(out, tiny_y[idx], tiny_tm[idx], tiny_bm[idx], tiny_tw[idx])
            if not torch.isfinite(loss):
                stopped_reason = "NaN/Inf in tiny batch"
                break
            opt.zero_grad()
            loss.backward()
            grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
            opt.step()
            if step == 1 or step % 5 == 0 or step == TINY_STEPS:
                rows.append(
                    {
                        "seed": seed,
                        "method": method,
                        "stage": "tiny_batch",
                        "step": step,
                        "epoch": "",
                        "train_loss": float(loss.item()),
                        "val_loss": "",
                        "detection_term": float(det.item()),
                        "magmse_term": float(rec.item()),
                        "target_det_term": float(target_det.item()),
                        "background_det_term": float(background_det.item()),
                        "lambda_rec": LAMBDA_REC,
                        "weak_weight": WEAK_WEIGHT if method == "weak_weighting" else "",
                        "pos_weight": pos_weight if method == "balanced_mild" else "",
                        "lr": LR,
                        "grad_norm_before_clip": grad_norm,
                    }
                )
        if not stopped_reason:
            with torch.no_grad():
                tiny_final, _td, _tr, _tt, _tb = loss_terms(model(tiny_x), tiny_y, tiny_tm, tiny_bm, tiny_tw)
                initial_train_loss, _d, _r, _t, _b = loss_terms(model(x), y, train_tm, train_bm, train_tw)
                initial_val_loss, _vd, _vr, _vt, _vb = loss_terms(model(valx), valy, val_tm, val_bm, val_tw)
            for epoch in range(1, SMALL_EPOCHS + 1):
                perm = torch.randperm(x.shape[0], device=device)
                losses: list[float] = []
                dets: list[float] = []
                recs: list[float] = []
                target_dets: list[float] = []
                background_dets: list[float] = []
                grad_norms: list[float] = []
                for start in range(0, x.shape[0], BATCH_SIZE):
                    idx = perm[start : start + BATCH_SIZE]
                    out = model(x[idx])
                    loss, det, rec, target_det, background_det = loss_terms(out, y[idx], train_tm[idx], train_bm[idx], train_tw[idx])
                    if not torch.isfinite(loss):
                        stopped_reason = f"NaN/Inf at epoch {epoch}"
                        break
                    opt.zero_grad()
                    loss.backward()
                    grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
                    opt.step()
                    losses.append(float(loss.item()))
                    dets.append(float(det.item()))
                    recs.append(float(rec.item()))
                    target_dets.append(float(target_det.item()))
                    background_dets.append(float(background_det.item()))
                    grad_norms.append(grad_norm)
                if stopped_reason:
                    break
                with torch.no_grad():
                    val_loss, val_det, val_rec, val_target_det, val_background_det = loss_terms(
                        model(valx), valy, val_tm, val_bm, val_tw
                    )
                rows.append(
                    {
                        "seed": seed,
                        "method": method,
                        "stage": "small_subset",
                        "step": "",
                        "epoch": epoch,
                        "train_loss": float(np.mean(losses)),
                        "val_loss": float(val_loss.item()),
                        "detection_term": float(np.mean(dets)),
                        "magmse_term": float(np.mean(recs)),
                        "target_det_term": float(np.mean(target_dets)),
                        "background_det_term": float(np.mean(background_dets)),
                        "val_detection_term": float(val_det.item()),
                        "val_magmse_term": float(val_rec.item()),
                        "val_target_det_term": float(val_target_det.item()),
                        "val_background_det_term": float(val_background_det.item()),
                        "lambda_rec": LAMBDA_REC,
                        "weak_weight": WEAK_WEIGHT if method == "weak_weighting" else "",
                        "pos_weight": pos_weight if method == "balanced_mild" else "",
                        "lr": LR,
                        "grad_norm_before_clip": float(np.mean(grad_norms)),
                    }
                )
    except RuntimeError as exc:
        stopped_reason = f"RuntimeError: {exc}"

    if stopped_reason:
        metrics = {
            "seed": seed,
            "method": method,
            "status": "FAILED",
            "stopped_reason": stopped_reason,
            "has_nan_or_inf": True,
            "train_target_cells": train_pos,
            "train_background_cells": train_neg,
            "pos_weight": pos_weight if method == "balanced_mild" else "",
            "weak_weight": WEAK_WEIGHT if method == "weak_weighting" else "",
            "lambda_rec": LAMBDA_REC,
            "lr": LR,
        }
        return None, rows, metrics

    with torch.no_grad():
        final_train_loss, final_train_det, final_train_rec, final_train_target_det, final_train_background_det = loss_terms(
            model(x), y, train_tm, train_bm, train_tw
        )
        final_val_loss, final_val_det, final_val_rec, final_val_target_det, final_val_background_det = loss_terms(
            model(valx), valy, val_tm, val_bm, val_tw
        )
        val_out = infer_rd(model, val_x, mean, std, device)
    metrics = {
        "seed": seed,
        "method": method,
        "status": "DONE",
        "stopped_reason": "",
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": float(tiny_final.item()),
        "tiny_loss_drop_fraction": (tiny_initial - float(tiny_final.item())) / max(tiny_initial, EPS),
        "initial_train_loss": float(initial_train_loss.item()),
        "final_train_loss": float(final_train_loss.item()),
        "train_loss_drop_fraction": (float(initial_train_loss.item()) - float(final_train_loss.item()))
        / max(float(initial_train_loss.item()), EPS),
        "initial_val_loss": float(initial_val_loss.item()),
        "final_val_loss": float(final_val_loss.item()),
        "val_loss_drop_fraction": (float(initial_val_loss.item()) - float(final_val_loss.item()))
        / max(float(initial_val_loss.item()), EPS),
        "final_train_detection": float(final_train_det.item()),
        "final_train_magmse": float(final_train_rec.item()),
        "final_train_target_det": float(final_train_target_det.item()),
        "final_train_background_det": float(final_train_background_det.item()),
        "final_val_detection": float(final_val_det.item()),
        "final_val_magmse": float(final_val_rec.item()),
        "final_val_target_det": float(final_val_target_det.item()),
        "final_val_background_det": float(final_val_background_det.item()),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
        "train_target_cells": train_pos,
        "train_background_cells": train_neg,
        "inverse_frequency_ratio": float(train_neg / max(train_pos, 1)),
        "pos_weight": pos_weight if method == "balanced_mild" else "",
        "weak_weight": WEAK_WEIGHT if method == "weak_weighting" else "",
        "lambda_rec": LAMBDA_REC,
        "lr": LR,
        "rd_detection_threshold_from_clean_val_background": detection_threshold,
    }
    return model, rows, metrics


def case_from_by_frame(
    input_type: str,
    frames: np.ndarray,
    db_by_frame: dict[int, np.ndarray],
    *,
    method: str = "",
    seed: int | str = "",
    sir_name: str = "",
) -> dict[str, Any]:
    return {
        "input_type": input_type,
        "method": method,
        "seed": seed,
        "sir_name": sir_name,
        "frames": np.asarray(frames, dtype=int),
        "db_by_frame": {int(idx): db_by_frame[int(idx)] for idx in frames.tolist()},
    }


def pfa_stats_by_frame(detections: dict[int, np.ndarray], bg_by_frame: dict[int, np.ndarray], test_frames: np.ndarray) -> dict[str, Any]:
    rng = np.random.default_rng(RANDOM_SEED + 404)
    frame_fa: list[int] = []
    frame_bg: list[int] = []
    frame_pfa: list[float] = []
    for frame_idx_raw in test_frames.tolist():
        frame_idx = int(frame_idx_raw)
        bg = bg_by_frame[frame_idx]
        bg_count = int(bg.sum())
        fa = int(np.logical_and(detections[frame_idx], bg).sum())
        if bg_count:
            frame_fa.append(fa)
            frame_bg.append(bg_count)
            frame_pfa.append(fa / bg_count)
    boot = []
    if frame_fa:
        fa_arr = np.asarray(frame_fa, dtype=np.float64)
        bg_arr = np.asarray(frame_bg, dtype=np.float64)
        for _ in range(200):
            choices = rng.integers(0, len(fa_arr), size=len(fa_arr))
            boot.append(float(fa_arr[choices].sum() / max(bg_arr[choices].sum(), 1.0)))
    return {
        "frame_level_pfa_mean": float(np.mean(frame_pfa)) if frame_pfa else "",
        "frame_level_pfa_std": float(np.std(frame_pfa)) if frame_pfa else "",
        "bootstrap_pfa_std": float(np.std(boot)) if boot else "",
        "bootstrap_pfa_ci_low": float(np.quantile(boot, 0.025)) if boot else "",
        "bootstrap_pfa_ci_high": float(np.quantile(boot, 0.975)) if boot else "",
    }


def evaluate_case(
    case: dict[str, Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    rd_ctx: dict[str, Any],
    targets: list[Any],
    mask_name: str,
    target_scope: str,
    pfa: float,
) -> dict[str, Any]:
    bg_by_frame = rd_ctx["background_mask_by_frame"]
    tm_by_frame = rd_ctx["target_mask_by_frame"]
    rects = rd_ctx["rect_by_target"]
    splits = rd_ctx["splits"][SPLIT_DEFINITION]
    allowed = None if target_scope == "all" else rd_ctx["non_overlap_ids"]
    val_scores = np.concatenate([case["db_by_frame"][int(idx)][bg_by_frame[int(idx)]] for idx in val_frames.tolist()])
    threshold = float(np.quantile(val_scores, 1.0 - pfa))
    detections = {int(idx): case["db_by_frame"][int(idx)] >= threshold for idx in case["frames"].tolist()}
    bg_count = 0
    fa = 0
    tp_cells = 0
    fn_cells = 0
    for idx_raw in test_frames.tolist():
        idx = int(idx_raw)
        bg = bg_by_frame[idx]
        tm = tm_by_frame[idx]
        det = detections[idx]
        bg_count += int(bg.sum())
        fa += int(np.logical_and(det, bg).sum())
        tp_cells += int(np.logical_and(det, tm).sum())
        fn_cells += int(np.logical_and(~det, tm).sum())
    precision = tp_cells / (tp_cells + fa) if tp_cells + fa else 0.0
    recall = tp_cells / (tp_cells + fn_cells) if tp_cells + fn_cells else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    test_set = {int(x) for x in test_frames.tolist()}
    selected_targets = [
        t
        for t in targets
        if int(t.frame_idx) in test_set
        and int(t.target_id) in rects
        and int(t.target_id) in splits
        and (allowed is None or int(t.target_id) in allowed)
    ]
    out: dict[str, Any] = {
        "input_type": case["input_type"],
        "method": case.get("method", ""),
        "seed": case.get("seed", ""),
        "sir_name": case.get("sir_name", ""),
        "representation": "RD",
        "mask_name": mask_name,
        "split_definition": SPLIT_DEFINITION,
        "target_scope": target_scope,
        "target_pfa": pfa,
        "threshold_source": "input_specific_validation_background",
        "threshold": threshold,
        "measured_pfa": fa / max(bg_count, 1),
        "false_alarm_count": fa,
        "background_cell_count": bg_count,
        "validation_background_cell_count": int(sum(bg_by_frame[int(idx)].sum() for idx in val_frames.tolist())),
        "tp_cells": tp_cells,
        "fp_cells": fa,
        "fn_cells": fn_cells,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        **pfa_stats_by_frame(detections, bg_by_frame, test_frames),
    }
    for split_name in ["weak", "mid", "strong"]:
        subset = [t for t in selected_targets if splits[int(t.target_id)] == split_name]
        hits = 0
        for target in subset:
            tid = int(target.target_id)
            rlo, rhi, dlo, dhi = rects[tid]
            hits += int(bool(detections[int(target.frame_idx)][rlo:rhi, dlo:dhi].any()))
        out[f"{split_name}_n"] = len(subset)
        out[f"{split_name}_hits"] = hits
        out[f"{split_name}_pd"] = hits / len(subset) if subset else ""
        out[f"{split_name}_miss_rate"] = 1.0 - hits / len(subset) if subset else ""
    all_hits = 0
    for target in selected_targets:
        tid = int(target.target_id)
        rlo, rhi, dlo, dhi = rects[tid]
        all_hits += int(bool(detections[int(target.frame_idx)][rlo:rhi, dlo:dhi].any()))
    out["overall_n"] = len(selected_targets)
    out["overall_hits"] = all_hits
    out["overall_pd"] = all_hits / len(selected_targets) if selected_targets else ""
    out["overall_miss_rate"] = 1.0 - all_hits / len(selected_targets) if selected_targets else ""
    return out


def evaluate_cases(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    rd_contexts: dict[str, dict[str, Any]],
    targets: list[Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        for mask_name, ctx in rd_contexts.items():
            for scope in ["all", "non_overlap_only"]:
                for pfa in TARGET_PFAS:
                    rows.append(evaluate_case(case, val_frames, test_frames, ctx, targets, mask_name, scope, pfa))
    return rows


def reconstruction_rows(cases: list[dict[str, Any]], clean_rd: dict[int, np.ndarray], test_frames: np.ndarray) -> list[dict[str, Any]]:
    clean_stack = np.stack([clean_rd[int(idx)] for idx in test_frames.tolist()])
    clean_power = power_from_db(clean_stack)
    rows = []
    for case in cases:
        db_stack = np.stack([case["db_by_frame"][int(idx)] for idx in test_frames.tolist()])
        power_stack = power_from_db(db_stack)
        rows.append(
            {
                "input_type": case["input_type"],
                "method": case.get("method", ""),
                "seed": case.get("seed", ""),
                "sir_name": case.get("sir_name", ""),
                "mse_db_to_clean": mse_np(db_stack, clean_stack),
                "magmse_db_to_clean": float(np.mean(np.abs(db_stack - clean_stack) ** 2)),
                "mse_power_to_clean": mse_np(power_stack, clean_power),
            }
        )
    return rows


def finite_mean(values: list[float]) -> float | str:
    vals = [float(v) for v in values if np.isfinite(float(v))]
    return float(np.mean(vals)) if vals else ""


def smoke_rows(eval_rows: list[dict[str, Any]], rd_ctx: dict[str, Any], targets: list[Any], clean_rd: dict[int, np.ndarray], test_frames: np.ndarray) -> list[dict[str, Any]]:
    rows = []
    test_set = {int(x) for x in test_frames.tolist()}
    splits = rd_ctx["splits"][SPLIT_DEFINITION]
    rects = rd_ctx["rect_by_target"]
    contrasts = []
    weak_contrasts = []
    for target in targets:
        tid = int(target.target_id)
        if int(target.frame_idx) not in test_set or tid not in rects:
            continue
        rlo, rhi, dlo, dhi = rects[tid]
        bg = rd_ctx["background_mask_by_frame"][int(target.frame_idx)]
        local = clean_rd[int(target.frame_idx)]
        peak = float(np.max(local[rlo:rhi, dlo:dhi]))
        bg_med = float(np.median(local[bg]))
        contrast = peak - bg_med
        contrasts.append(contrast)
        if splits.get(tid) == "weak":
            weak_contrasts.append(contrast)
    for row in eval_rows:
        if (
            row["mask_name"] == "default"
            and row["target_scope"] == "all"
            and row["input_type"] in {"clean", f"interfered_{EVAL_SIR_NAME}"}
        ):
            rows.append(
                {
                    "input_type": row["input_type"],
                    "sir_name": row.get("sir_name", ""),
                    "target_pfa": row["target_pfa"],
                    "calibration_threshold": row["threshold"],
                    "measured_pfa": row["measured_pfa"],
                    "weak_pd": row["weak_pd"],
                    "overall_pd": row["overall_pd"],
                    "false_alarm_count": row["false_alarm_count"],
                    "validation_background_cell_count": row["validation_background_cell_count"],
                    "test_background_cell_count": row["background_cell_count"],
                    "target_background_contrast_db": finite_mean(contrasts),
                    "weak_separability_proxy_db": finite_mean(weak_contrasts),
                    "scope_note": "RD fixed-PFA smoke with range labels and clean-RD Doppler peak projection.",
                }
            )
    return rows


def lookup_metric(
    rows: list[dict[str, Any]],
    input_type: str,
    *,
    seed: int,
    mask_name: str = "default",
    scope: str = "all",
    pfa: float = PRIMARY_PFA,
) -> dict[str, Any]:
    for row in rows:
        if (
            row["input_type"] == input_type
            and str(row.get("seed", "")) == str(seed)
            and row["mask_name"] == mask_name
            and row["target_scope"] == scope
            and abs(float(row["target_pfa"]) - pfa) < 1e-12
        ):
            return row
    raise KeyError((input_type, seed, mask_name, scope, pfa))


def lookup_recon(rows: list[dict[str, Any]], input_type: str, seed: int, sir_name: str = "") -> dict[str, Any]:
    for row in rows:
        if row["input_type"] == input_type and str(row.get("seed", "")) == str(seed) and str(row.get("sir_name", "")) == sir_name:
            return row
    raise KeyError((input_type, seed, sir_name))


def seed_summary_rows(eval_rows: list[dict[str, Any]], recon: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for seed in SEEDS:
        b_out = f"rd_balanced_mild_seed{seed}_output"
        w_out = f"rd_weak_w2p0_seed{seed}_output"
        b_clean = f"rd_balanced_mild_seed{seed}_model_clean"
        w_clean = f"rd_weak_w2p0_seed{seed}_model_clean"
        balanced = lookup_metric(eval_rows, b_out, seed=seed)
        weak = lookup_metric(eval_rows, w_out, seed=seed)
        balanced_narrow = lookup_metric(eval_rows, b_out, seed=seed, mask_name="narrow")
        weak_narrow = lookup_metric(eval_rows, w_out, seed=seed, mask_name="narrow")
        balanced_non = lookup_metric(eval_rows, b_out, seed=seed, scope="non_overlap_only")
        weak_non = lookup_metric(eval_rows, w_out, seed=seed, scope="non_overlap_only")
        balanced_1e3 = lookup_metric(eval_rows, b_out, seed=seed, pfa=SECONDARY_PFA)
        weak_1e3 = lookup_metric(eval_rows, w_out, seed=seed, pfa=SECONDARY_PFA)
        weak_clean = lookup_metric(eval_rows, w_clean, seed=seed, pfa=PRIMARY_PFA)
        balanced_clean = lookup_metric(eval_rows, b_clean, seed=seed, pfa=PRIMARY_PFA)
        weak_clean_recon = lookup_recon(recon, w_clean, seed)
        balanced_clean_recon = lookup_recon(recon, b_clean, seed)
        default_delta = f(weak, "weak_pd") - f(balanced, "weak_pd")
        narrow_delta = f(weak_narrow, "weak_pd") - f(balanced_narrow, "weak_pd")
        non_delta = f(weak_non, "weak_pd") - f(balanced_non, "weak_pd")
        pfa_1e3_delta = f(weak_1e3, "weak_pd") - f(balanced_1e3, "weak_pd")
        clean_no_harm = (
            f(weak_clean_recon, "mse_db_to_clean") <= 3.0
            and f(weak_clean_recon, "mse_db_to_clean") <= f(balanced_clean_recon, "mse_db_to_clean") + 0.5
            and f(weak_clean, "measured_pfa") <= 0.08
        )
        rows.append(
            {
                "seed": seed,
                "baseline": "balanced_mild",
                "weak_weighting": "weak_weighting_w2p0",
                "split_definition": SPLIT_DEFINITION,
                "target_pfa": PRIMARY_PFA,
                "mask_name": "default",
                "target_scope": "all",
                "weak_n": weak["weak_n"],
                "mid_n": weak["mid_n"],
                "strong_n": weak["strong_n"],
                "balanced_mild_weak_hits": balanced["weak_hits"],
                "weak_weighting_weak_hits": weak["weak_hits"],
                "balanced_mild_weak_pd": balanced["weak_pd"],
                "weak_weighting_weak_pd": weak["weak_pd"],
                "weak_pd_delta": default_delta,
                "weak_hit_delta": i(weak, "weak_hits") - i(balanced, "weak_hits"),
                "balanced_mild_overall_pd": balanced["overall_pd"],
                "weak_weighting_overall_pd": weak["overall_pd"],
                "overall_pd_delta": f(weak, "overall_pd") - f(balanced, "overall_pd"),
                "balanced_mild_measured_pfa": balanced["measured_pfa"],
                "weak_weighting_measured_pfa": weak["measured_pfa"],
                "measured_pfa_delta": f(weak, "measured_pfa") - f(balanced, "measured_pfa"),
                "balanced_mild_false_alarm_count": balanced["false_alarm_count"],
                "weak_weighting_false_alarm_count": weak["false_alarm_count"],
                "false_alarm_count_delta": i(weak, "false_alarm_count") - i(balanced, "false_alarm_count"),
                "balanced_mild_clean_mse_db_to_clean": balanced_clean_recon["mse_db_to_clean"],
                "weak_weighting_clean_mse_db_to_clean": weak_clean_recon["mse_db_to_clean"],
                "weak_weighting_clean_measured_pfa": weak_clean["measured_pfa"],
                "clean_no_harm_pass": clean_no_harm,
                "default_mask_weak_pd_delta": default_delta,
                "narrow_mask_weak_pd_delta": narrow_delta,
                "default_vs_narrow_mask_consistency": direction_consistent(default_delta, narrow_delta),
                "all_targets_weak_pd_delta": default_delta,
                "non_overlap_only_weak_pd_delta": non_delta,
                "non_overlap_weak_hit_delta": i(weak_non, "weak_hits") - i(balanced_non, "weak_hits"),
                "all_vs_non_overlap_consistency": direction_consistent(default_delta, non_delta),
                "pfa_1e3_balanced_weak_pd": balanced_1e3["weak_pd"],
                "pfa_1e3_weak_weighting_weak_pd": weak_1e3["weak_pd"],
                "pfa_1e3_weak_pd_delta": pfa_1e3_delta,
                "pfa_1e3_weak_hit_delta": i(weak_1e3, "weak_hits") - i(balanced_1e3, "weak_hits"),
                "pfa_1e3_not_reversed": pfa_1e3_delta >= -0.005,
                "meets_min_weak_pd_gain_bar": default_delta >= 0.02,
                "meets_min_hit_delta_bar": (i(weak, "weak_hits") - i(balanced, "weak_hits")) >= 5,
                "pfa_not_increased": f(weak, "measured_pfa") <= f(balanced, "measured_pfa") + 1e-12,
                "false_alarm_not_increased": i(weak, "false_alarm_count") <= i(balanced, "false_alarm_count"),
            }
        )
    return rows


def mean_std_rows(seed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = [
        "balanced_mild_weak_pd",
        "weak_weighting_weak_pd",
        "weak_pd_delta",
        "weak_hit_delta",
        "measured_pfa_delta",
        "false_alarm_count_delta",
        "pfa_1e3_weak_pd_delta",
        "non_overlap_only_weak_pd_delta",
    ]
    rows = []
    for metric in metrics:
        values = np.asarray([f(r, metric) for r in seed_rows], dtype=np.float64)
        rows.append(
            {
                "metric": metric,
                "n_seeds": len(seed_rows),
                "mean": float(np.mean(values)),
                "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
                "min": float(np.min(values)),
                "max": float(np.max(values)),
            }
        )
    return rows


def make_decision(seed_rows: list[dict[str, Any]], mean_rows: list[dict[str, Any]]) -> dict[str, Any]:
    mean_lookup = {r["metric"]: r for r in mean_rows}
    mean_gain = f(mean_lookup["weak_pd_delta"], "mean")
    mean_hit_delta = f(mean_lookup["weak_hit_delta"], "mean")
    mean_pfa_delta = f(mean_lookup["measured_pfa_delta"], "mean")
    mean_fa_delta = f(mean_lookup["false_alarm_count_delta"], "mean")
    criteria = {
        "mean_weak_pd_delta_ge_0p02": mean_gain >= 0.02,
        "mean_weak_hit_delta_ge_5": mean_hit_delta >= 5.0,
        "measured_pfa_not_up_all_seeds": all(str(r["pfa_not_increased"]) == "True" or r["pfa_not_increased"] is True for r in seed_rows),
        "false_alarm_not_up_all_seeds": all(str(r["false_alarm_not_increased"]) == "True" or r["false_alarm_not_increased"] is True for r in seed_rows),
        "clean_no_harm_all_seeds": all(str(r["clean_no_harm_pass"]) == "True" or r["clean_no_harm_pass"] is True for r in seed_rows),
        "default_narrow_consistent_all_seeds": all(
            str(r["default_vs_narrow_mask_consistency"]) == "True" or r["default_vs_narrow_mask_consistency"] is True
            for r in seed_rows
        ),
        "all_non_overlap_consistent_all_seeds": all(
            str(r["all_vs_non_overlap_consistency"]) == "True" or r["all_vs_non_overlap_consistency"] is True for r in seed_rows
        ),
        "pfa_1e3_not_reversed_all_seeds": all(str(r["pfa_1e3_not_reversed"]) == "True" or r["pfa_1e3_not_reversed"] is True for r in seed_rows),
        "mean_gain_not_below_balanced": mean_gain >= 0.0,
        "weak_threshold_leakage": False,
    }
    go = (
        criteria["mean_weak_pd_delta_ge_0p02"]
        and criteria["mean_weak_hit_delta_ge_5"]
        and criteria["measured_pfa_not_up_all_seeds"]
        and criteria["false_alarm_not_up_all_seeds"]
        and criteria["clean_no_harm_all_seeds"]
        and criteria["default_narrow_consistent_all_seeds"]
        and criteria["all_non_overlap_consistent_all_seeds"]
        and criteria["pfa_1e3_not_reversed_all_seeds"]
        and criteria["mean_gain_not_below_balanced"]
        and not criteria["weak_threshold_leakage"]
    )
    failed = [name for name, ok in criteria.items() if (name != "weak_threshold_leakage" and not ok) or (name == "weak_threshold_leakage" and ok)]
    return {
        "verdict": "GO" if go else "NO-GO",
        "final_route": "continue RD weak weighting" if go else "NO-GO: do not enter D6; record RD-only result as limited/negative or weak evidence",
        "criteria": criteria,
        "failed_criteria": failed,
        "mean_weak_pd_delta": mean_gain,
        "mean_weak_hit_delta": mean_hit_delta,
        "mean_measured_pfa_delta": mean_pfa_delta,
        "mean_false_alarm_count_delta": mean_fa_delta,
        "scope_note": "2-seed limited RD-only supplementary sanity; RD Doppler boxes are clean-peak projections, not Doppler ground truth.",
    }


def plot_figures(
    eval_rows: list[dict[str, Any]],
    seed_rows: list[dict[str, Any]],
    training_rows: list[dict[str, Any]],
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    cases: list[dict[str, Any]],
    rd_ctx: dict[str, Any],
    targets: list[Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    test_set = {int(x) for x in test_frames.tolist()}
    weak_targets = [
        t
        for t in targets
        if int(t.frame_idx) in test_set
        and int(t.target_id) in rd_ctx["rect_by_target"]
        and rd_ctx["splits"][SPLIT_DEFINITION].get(int(t.target_id)) == "weak"
    ]
    if weak_targets:
        target = weak_targets[0]
        frame = int(target.frame_idx)
        rlo, rhi, dlo, dhi = rd_ctx["rect_by_target"][int(target.target_id)]
        plt.figure(figsize=(10, 4), dpi=150)
        plt.subplot(1, 2, 1)
        plt.imshow(clean_rd[frame].T, aspect="auto", origin="lower", cmap="magma")
        plt.axvline(target.range_bin, color="cyan", linewidth=0.8)
        plt.gca().add_patch(plt.Rectangle((rlo, dlo), rhi - rlo, dhi - dlo, fill=False, edgecolor="cyan", linewidth=1.0))
        plt.title(f"Clean RD weak target frame {frame}")
        plt.xlabel("Range bin")
        plt.ylabel("Doppler bin")
        plt.subplot(1, 2, 2)
        plt.imshow(inter_rd[EVAL_SIR_NAME][frame].T, aspect="auto", origin="lower", cmap="magma")
        plt.axvline(target.range_bin, color="cyan", linewidth=0.8)
        plt.gca().add_patch(plt.Rectangle((rlo, dlo), rhi - rlo, dhi - dlo, fill=False, edgecolor="cyan", linewidth=1.0))
        plt.title(f"Interfered RD ({EVAL_SIR_NAME})")
        plt.xlabel("Range bin")
        plt.tight_layout()
        out = FIG_DIR / "rd_weak_target_examples.png"
        plt.savefig(out)
        plt.close()
        outputs.append(out)

    val_bg = np.concatenate([clean_rd[int(idx)][rd_ctx["background_mask_by_frame"][int(idx)]] for idx in val_frames.tolist()])
    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(val_bg, bins=80, alpha=0.8)
    for pfa in TARGET_PFAS:
        thr = float(np.quantile(val_bg, 1.0 - pfa))
        plt.axvline(thr, linestyle="--", linewidth=1.2, label=f"PFA {pfa:g}: {thr:.2f} dB")
    plt.xlabel("RD background score (dB)")
    plt.ylabel("Count")
    plt.title("RD fixed-PFA validation threshold sanity")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "rd_fixed_pfa_threshold_sanity.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    labels = [str(r["seed"]) for r in seed_rows]
    x = np.arange(len(seed_rows))
    width = 0.35
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(x - width / 2, [f(r, "balanced_mild_weak_pd") for r in seed_rows], width, label="balanced_mild")
    plt.bar(x + width / 2, [f(r, "weak_weighting_weak_pd") for r in seed_rows], width, label="weak_weighting")
    plt.axhline(0.0, color="black", linewidth=0.5)
    plt.xticks(x, labels)
    plt.ylim(0, 1.05)
    plt.ylabel("Weak Pd")
    plt.xlabel("Seed")
    plt.title("RD weak Pd: balanced_mild vs weak_weighting")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "rd_balanced_vs_weak_weighting_weak_pd.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    plt.figure(figsize=(9, 4), dpi=150)
    plt.subplot(1, 2, 1)
    plt.bar(x - width / 2, [f(r, "balanced_mild_measured_pfa") for r in seed_rows], width, label="balanced")
    plt.bar(x + width / 2, [f(r, "weak_weighting_measured_pfa") for r in seed_rows], width, label="weak")
    plt.xticks(x, labels)
    plt.ylabel("Measured PFA")
    plt.title("PFA")
    plt.subplot(1, 2, 2)
    plt.bar(x - width / 2, [f(r, "balanced_mild_false_alarm_count") for r in seed_rows], width, label="balanced")
    plt.bar(x + width / 2, [f(r, "weak_weighting_false_alarm_count") for r in seed_rows], width, label="weak")
    plt.xticks(x, labels)
    plt.ylabel("False alarm count")
    plt.title("False alarms")
    plt.tight_layout()
    out = FIG_DIR / "rd_pfa_false_alarm_comparison.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    plt.figure(figsize=(8, 4), dpi=150)
    small = [r for r in training_rows if r["stage"] == "small_subset"]
    for method in ["balanced_mild", "weak_weighting"]:
        for seed in SEEDS:
            subset = [r for r in small if r["method"] == method and int(r["seed"]) == seed]
            if subset:
                plt.plot([int(r["epoch"]) for r in subset], [float(r["val_loss"]) for r in subset], marker="o", label=f"{method} s{seed}")
    plt.yscale("log")
    plt.xlabel("Epoch")
    plt.ylabel("Validation loss")
    plt.title("RD training loss curve")
    plt.legend(fontsize=7)
    plt.tight_layout()
    out = FIG_DIR / "rd_training_loss_curve.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    frame = int(test_frames[0])
    case_lookup = {(case["input_type"], str(case.get("seed", ""))): case for case in cases}
    seed = SEEDS[0]
    b_key = (f"rd_balanced_mild_seed{seed}_model_clean", str(seed))
    w_key = (f"rd_weak_w2p0_seed{seed}_model_clean", str(seed))
    plt.figure(figsize=(10, 6), dpi=150)
    images = [
        ("clean", clean_rd[frame]),
        ("balanced model(clean)", case_lookup[b_key]["db_by_frame"][frame] if b_key in case_lookup else clean_rd[frame]),
        ("weak model(clean)", case_lookup[w_key]["db_by_frame"][frame] if w_key in case_lookup else clean_rd[frame]),
    ]
    vmin = np.percentile(clean_rd[frame], 2)
    vmax = np.percentile(clean_rd[frame], 99)
    for idx, (title, image) in enumerate(images, start=1):
        plt.subplot(1, 3, idx)
        plt.imshow(image.T, aspect="auto", origin="lower", cmap="magma", vmin=vmin, vmax=vmax)
        plt.title(title)
        plt.xlabel("Range")
        if idx == 1:
            plt.ylabel("Doppler")
    plt.tight_layout()
    out = FIG_DIR / "rd_clean_no_harm_reconstruction_comparison.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)
    return outputs


def write_reports(
    weak_meta: dict[str, Any],
    smoke: list[dict[str, Any]],
    seed_rows: list[dict[str, Any]],
    mean_rows: list[dict[str, Any]],
    decision: dict[str, Any],
    outputs: list[tuple[Path, str]],
) -> tuple[Path, Path]:
    summary = f"""# D5D RD-only supplementary experiment

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. Scope

This is D5D only: RD representation, fixed-PFA calibration, train-only frozen weak definition, `balanced_mild` vs `weak_weighting_w2p0`.

Hard boundaries: no D6, no false alarm penalty, no clean identity full method, no proposed full loss, no detector modification, no large model, no RA mainline.

RD target boxes use dataset range labels plus a clean-RD peak Doppler projection. This is a constrained supplementary sanity result, not confirmed RD performance.

## 2. Frozen Weak Definition

| field | value |
|---|---:|
| train weak threshold q30 dB | {weak_meta['train_target_peak_db_q30_weak_threshold']:.4f} |
| train q70 dB | {weak_meta['train_target_peak_db_q70_strong_threshold']:.4f} |
| threshold target count | {weak_meta['train_target_count_for_threshold']} |
| threshold leakage | {weak_meta['threshold_leakage']} |
| used test clean-map property for threshold | {weak_meta['used_test_clean_map_property_for_threshold']} |

## 3. RD Fixed-PFA Smoke

{md_table(smoke, ['input_type', 'target_pfa', 'calibration_threshold', 'measured_pfa', 'weak_pd', 'overall_pd', 'false_alarm_count', 'validation_background_cell_count', 'test_background_cell_count', 'weak_separability_proxy_db'])}

## 4. Seed Summary

{md_table(seed_rows, ['seed', 'weak_n', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta', 'clean_no_harm_pass', 'default_vs_narrow_mask_consistency', 'all_vs_non_overlap_consistency', 'pfa_1e3_weak_pd_delta'])}

## 5. Mean / Std

{md_table(mean_rows, ['metric', 'n_seeds', 'mean', 'std', 'min', 'max'])}

## 6. Interpretation

Verdict: **{decision['verdict']}**.

Final route: {decision['final_route']}.

Mean weak Pd delta = {decision['mean_weak_pd_delta']:.4f}; mean weak hit delta = {decision['mean_weak_hit_delta']:.2f}; mean PFA delta = {decision['mean_measured_pfa_delta']:.6f}; mean false alarm delta = {decision['mean_false_alarm_count_delta']:.2f}.

Failed criteria: {', '.join(decision['failed_criteria']) if decision['failed_criteria'] else 'none'}.

## 7. Output Files

{md_table([{'file': str(path), 'description': desc} for path, desc in outputs], ['file', 'description'])}
"""
    go = f"""# D5D RD-only GO / NO-GO decision

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Verdict

**{decision['verdict']}**

Route: {decision['final_route']}

## Mechanical Criteria

{md_table([{'criterion': k, 'pass': v} for k, v in decision['criteria'].items()], ['criterion', 'pass'])}

## Evidence

{md_table(seed_rows, ['seed', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta', 'clean_no_harm_pass', 'default_vs_narrow_mask_consistency', 'all_vs_non_overlap_consistency', 'pfa_1e3_not_reversed'])}

## Conservative Note

D5D remains a limited RD-only supplementary sanity experiment. It does not authorize D6 unless all bars pass. Because RD boxes use clean-RD Doppler peak projection rather than Doppler ground truth, any positive result must still be written as preliminary.
"""
    summary_ts = write_versioned_text(SUMMARY_PATH, summary)
    go_ts = write_versioned_text(GO_NOGO_PATH, go)
    return summary_ts, go_ts


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    outputs: list[tuple[Path, str]] = []

    manifest, targets, clean_power, clean_range_db, _rd_for_fig = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    train_frames = np.asarray(train_all[:N_TRAIN_FRAMES], dtype=int)
    val_frames = np.asarray(val_all[:N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[:N_TEST_FRAMES], dtype=int)
    all_frames = np.asarray(sorted(set(train_frames.tolist()) | set(val_frames.tolist()) | set(test_frames.tolist())), dtype=int)

    clean_cfar_range = __import__("d1a_gao77_clean_fixed_pfa_sanity").ca_cfar_score_1d_np(clean_power)
    contexts_1d = build_mask_context(clean_range_db, clean_cfar_range, targets)
    default_range_ctx = contexts_1d["default"]
    frozen_splits, weak_meta = clean_peak_frozen_splits(default_range_ctx, targets, train_frames)
    weak_meta["counts"]["val"] = split_counts_for_frames(frozen_splits, targets, val_frames)
    weak_meta["counts"]["test"] = split_counts_for_frames(frozen_splits, targets, test_frames)
    weak_meta["dataset"] = str(ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1")
    weak_meta["train_frames"] = [int(x) for x in train_frames.tolist()]
    weak_meta["val_frames"] = [int(x) for x in val_frames.tolist()]
    weak_meta["test_frames"] = [int(x) for x in test_frames.tolist()]

    rng = np.random.default_rng(RANDOM_SEED + 1700)
    clean_rd, inter_rd, inter_rows = compute_rd_maps(manifest, all_frames, TRAIN_SIR_NAMES, rng)
    train_x, train_y, train_rows = build_sample_arrays(train_frames, TRAIN_SIR_NAMES, clean_rd, inter_rd, "train")
    val_x, val_y, val_rows = build_sample_arrays(val_frames, TRAIN_SIR_NAMES, clean_rd, inter_rd, "val")
    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    norm_mean = float(norm_values.mean())
    norm_std = float(norm_values.std())

    rd_contexts = {
        mask_name: build_rd_context(clean_rd, targets, contexts_1d[mask_name], frozen_splits, all_frames, mask_name)
        for mask_name in ["default", "narrow"]
    }
    default_rd_ctx = rd_contexts["default"]

    training_rows: list[dict[str, Any]] = []
    training_summary: list[dict[str, Any]] = []
    models: dict[tuple[int, str], nn.Module] = {}
    for seed in SEEDS:
        for method in ["balanced_mild", "weak_weighting"]:
            model, rows, metrics = train_model(
                method,
                seed,
                train_x,
                train_y,
                train_rows,
                val_x,
                val_y,
                val_rows,
                default_rd_ctx,
                targets,
                val_frames,
                clean_rd,
                norm_mean,
                norm_std,
                device,
            )
            training_rows.extend(rows)
            training_summary.append(metrics)
            if model is not None:
                models[(seed, method)] = model

    eval_frames = np.asarray(sorted(set(val_frames.tolist()) | set(test_frames.tolist())), dtype=int)
    cases: list[dict[str, Any]] = [
        case_from_by_frame("clean", eval_frames, clean_rd),
        case_from_by_frame(f"interfered_{EVAL_SIR_NAME}", eval_frames, inter_rd[EVAL_SIR_NAME], sir_name=EVAL_SIR_NAME),
    ]
    eval_clean_stack = np.stack([clean_rd[int(idx)] for idx in eval_frames.tolist()])
    eval_inter_stack = np.stack([inter_rd[EVAL_SIR_NAME][int(idx)] for idx in eval_frames.tolist()])
    for (seed, method), model in models.items():
        label = f"rd_{method}_seed{seed}" if method == "balanced_mild" else f"rd_weak_w2p0_seed{seed}"
        clean_out = infer_rd(model, eval_clean_stack, norm_mean, norm_std, device)
        inter_out = infer_rd(model, eval_inter_stack, norm_mean, norm_std, device)
        clean_by_frame = {int(idx): clean_out[pos] for pos, idx in enumerate(eval_frames.tolist())}
        inter_by_frame = {int(idx): inter_out[pos] for pos, idx in enumerate(eval_frames.tolist())}
        cases.append(case_from_by_frame(f"{label}_model_clean", eval_frames, clean_by_frame, method=method, seed=seed))
        cases.append(
            case_from_by_frame(f"{label}_output", eval_frames, inter_by_frame, method=method, seed=seed, sir_name=EVAL_SIR_NAME)
        )

    eval_rows = evaluate_cases(cases, val_frames, test_frames, rd_contexts, targets)
    recon_rows = reconstruction_rows(cases, clean_rd, test_frames)
    seed_rows = seed_summary_rows(eval_rows, recon_rows)
    mean_rows = mean_std_rows(seed_rows)
    decision = make_decision(seed_rows, mean_rows)
    smoke = smoke_rows(eval_rows, default_rd_ctx, targets, clean_rd, test_frames)

    csv_outputs = [
        (RESULT_DIR / "d5d_rd_fixed_pfa_smoke.csv", smoke, "D5D RD fixed-PFA smoke"),
        (RESULT_DIR / "d5d_rd_training_summary.csv", training_summary, "D5D RD training summary"),
        (RESULT_DIR / "d5d_rd_training_loss.csv", training_rows, "D5D RD training loss"),
        (RESULT_DIR / "d5d_rd_eval_metrics.csv", eval_rows, "D5D RD fixed-PFA eval metrics"),
        (RESULT_DIR / "d5d_rd_reconstruction_metrics.csv", recon_rows, "D5D RD reconstruction metrics"),
        (RESULT_DIR / "d5d_rd_seed_summary.csv", seed_rows, "D5D RD seed summary"),
        (RESULT_DIR / "d5d_rd_seed_mean_std.csv", mean_rows, "D5D RD seed mean/std"),
        (RESULT_DIR / "d5d_rd_interference_manifest.csv", inter_rows, "D5D generated synthetic FMCW-like interference manifest"),
    ]
    for path, rows, desc in csv_outputs:
        write_csv(path, rows)
        outputs.append((path, desc))

    thresholds_path = RESULT_DIR / "d5d_rd_weak_thresholds.json"
    write_json(thresholds_path, weak_meta)
    outputs.append((thresholds_path, "D5D train-only frozen weak thresholds"))

    config = {
        "stage": "D5D",
        "date": datetime.now().isoformat(),
        "device": str(device),
        "representation": "RD-only",
        "seeds": SEEDS,
        "train_sir_names": TRAIN_SIR_NAMES,
        "eval_sir_name": EVAL_SIR_NAME,
        "n_train_frames": N_TRAIN_FRAMES,
        "n_val_frames": N_VAL_FRAMES,
        "n_test_frames": N_TEST_FRAMES,
        "batch_size": BATCH_SIZE,
        "tiny_steps": TINY_STEPS,
        "small_epochs": SMALL_EPOCHS,
        "lr": LR,
        "lambda_rec": LAMBDA_REC,
        "weak_weight": WEAK_WEIGHT,
        "split_definition": SPLIT_DEFINITION,
        "target_pfas": TARGET_PFAS,
        "constraints": {
            "entered_d6": False,
            "false_alarm_penalty": False,
            "clean_identity_full_method": False,
            "proposed_full_loss": False,
            "detector_modified": False,
            "fixed_pfa_protocol_modified": False,
            "large_model": False,
            "ra_mainline": False,
            "threshold_leakage": False,
        },
        "projection_caveat": default_rd_ctx["projection_note"],
        "result_dir": str(RESULT_DIR),
        "figure_dir": str(FIG_DIR),
    }
    config_path = RESULT_DIR / "d5d_rd_config.json"
    write_json(config_path, config)
    outputs.append((config_path, "D5D RD config"))

    figure_paths = plot_figures(eval_rows, seed_rows, training_rows, clean_rd, inter_rd, cases, default_rd_ctx, targets, val_frames, test_frames)
    for fig in figure_paths:
        outputs.append((fig, "D5D RD figure"))

    summary_ts, go_ts = write_reports(weak_meta, smoke, seed_rows, mean_rows, decision, outputs)
    outputs.extend(
        [
            (SUMMARY_PATH, "D5D RD summary latest"),
            (summary_ts, "D5D RD summary timestamped"),
            (GO_NOGO_PATH, "D5D RD go/no-go latest"),
            (go_ts, "D5D RD go/no-go timestamped"),
        ]
    )
    append_manifest(outputs)

    print(
        json.dumps(
            {
                "stage": "D5D",
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "summary": str(SUMMARY_PATH),
                "go_nogo": str(GO_NOGO_PATH),
                "verdict": decision["verdict"],
                "final_route": decision["final_route"],
                "seed_rows": seed_rows,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
