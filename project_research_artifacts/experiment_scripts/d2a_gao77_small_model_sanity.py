from __future__ import annotations

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
from scipy.io import loadmat

from d1a_gao77_clean_fixed_pfa_sanity import (
    EXPECTED_ADC_SHAPE,
    GAO77_CLASS_GROUP,
    LABEL_DIR,
    MANIFEST_PATH,
    OBJECTNESS_CLASSES,
    RADAR_DIR,
    RANGE_RESOLUTION_M,
    ROOT,
    VALID_RANGE_MAX_BIN,
    VALID_RANGE_MIN_BIN,
    ca_cfar_score_1d_np,
    parse_label_file,
    radar_maps,
    read_csv_dicts,
    write_csv,
    write_json,
)
from d1a_plus_mask_stress_test import Target, load_split, target_hit
from d1b_gao77_synthetic_interference_sanity import (
    EPS,
    SIR_CONFIGS as D1B_SIR_CONFIGS,
    build_mask_context,
    evaluate_by_class_group,
    evaluate_by_sequence,
    evaluate_scores,
    make_interference,
    range_noise_and_target_bias,
)


RESULT_DIR = ROOT / "results" / "d2a_gao77_small_model_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d2a_figures"
REPORT_PATH = ROOT / "refine-logs" / "D2A_GAO77_SMALL_MODEL_SANITY_REPORT.md"

RANDOM_SEED = 20260626
VALID_PFA_TARGETS = [1e-2, 1e-3]
ACTIVE_MASK_NAMES = {"narrow", "default"}
TRAIN_SIR_NAMES = ["light", "medium"]
VAL_SIR_NAMES = ["light", "medium"]
TEST_SIR_NAMES = ["light", "medium", "severe"]
EVAL_SIR_NAMES = ["light", "medium", "severe"]

N_TRAIN_FRAMES = 128
N_VAL_FRAMES = 64
N_TEST_FRAMES = 64
BATCH_SIZE = 4
TINY_BATCH_SIZE = 4
TINY_SAMPLE_COUNT = 16
TINY_STEPS = 300
SMALL_EPOCHS = 25
LEARNING_RATE = 2e-3
IDENTITY_LOSS_WEIGHT = 0.05


def db(x: float) -> float:
    return 10.0 * math.log10(max(float(x), EPS))


class SimpleRangeFCN(nn.Module):
    def __init__(self, n_bins: int, hidden: int = 128) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_bins, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, n_bins),
        )
        nn.init.zeros_(self.net[-1].weight)
        nn.init.zeros_(self.net[-1].bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: batch x 1 x range_bins. Residual form starts as identity.
        flat = x[:, 0, :]
        out = flat + self.net(flat)
        return out[:, None, :]


def load_clean_data() -> tuple[list[dict[str, str]], list[Target], np.ndarray, np.ndarray, dict[int, np.ndarray]]:
    manifest = read_csv_dicts(MANIFEST_PATH)
    n_frames = len(manifest)
    n_bins = EXPECTED_ADC_SHAPE[0]
    clean_power = np.zeros((n_frames, n_bins), dtype=np.float64)
    clean_db = np.zeros((n_frames, n_bins), dtype=np.float64)
    rd_for_fig: dict[int, np.ndarray] = {}
    sample_indices = set(np.linspace(0, n_frames - 1, 6, dtype=int).tolist())
    targets: list[Target] = []
    target_id = 0
    for frame_idx, row in enumerate(manifest):
        adc = loadmat(RADAR_DIR / row["new_radar_file"])["adcData"]
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"unexpected adcData shape {adc.shape} in {row['new_radar_file']}")
        rp, rd_map, _ = radar_maps(adc)
        clean_power[frame_idx] = rp
        clean_db[frame_idx] = 10.0 * np.log10(rp + EPS)
        if frame_idx in sample_indices:
            rd_for_fig[frame_idx] = rd_map
        for uid, cls, px, py, wid, length in parse_label_file(LABEL_DIR / row["new_label_file"]):
            if cls not in OBJECTNESS_CLASSES:
                continue
            target_id += 1
            range_m = math.sqrt(px * px + py * py)
            azimuth_deg = math.degrees(math.atan2(px, py))
            range_bin = int(round(range_m / RANGE_RESOLUTION_M))
            valid = VALID_RANGE_MIN_BIN <= range_bin <= VALID_RANGE_MAX_BIN
            targets.append(
                Target(
                    target_id=target_id,
                    frame_idx=frame_idx,
                    frame_id=row["new_frame_id"],
                    source_sequence=row["source_sequence"],
                    uid=uid,
                    cls=cls,
                    group=GAO77_CLASS_GROUP[cls],
                    px=px,
                    py=py,
                    wid=wid,
                    length=length,
                    range_m=range_m,
                    azimuth_deg=azimuth_deg,
                    range_bin=range_bin,
                    valid_projection=valid,
                )
            )
    return manifest, targets, clean_power, clean_db, rd_for_fig


def sir_cfg(sir_name: str) -> dict[str, Any]:
    for cfg in D1B_SIR_CONFIGS:
        if str(cfg["sir_name"]) == sir_name:
            return cfg
    raise KeyError(sir_name)


def load_adc(frame_idx: int, manifest: list[dict[str, str]]) -> np.ndarray:
    return loadmat(RADAR_DIR / manifest[frame_idx]["new_radar_file"])["adcData"]


def context_frame_counts(contexts: dict[str, dict[str, Any]], frame_idx: int) -> dict[str, Any]:
    out: dict[str, Any] = {"mask_types": ";".join(sorted(contexts))}
    for mask_name, ctx in contexts.items():
        intervals = ctx["intervals"]
        splits = ctx["splits"]["clean_peak_percentile"]
        non_overlap = ctx["non_overlap_ids"]
        frame_tids = [tid for tid, (lo, hi, radius) in intervals.items() if False]
        # Build from targets is cheaper outside, but this fallback keeps row construction simple.
        out[f"{mask_name}_weak_count"] = 0
        out[f"{mask_name}_mid_count"] = 0
        out[f"{mask_name}_strong_count"] = 0
        out[f"{mask_name}_non_overlap_count"] = 0
        out[f"{mask_name}_has_overlap"] = False
    return out


def build_frame_count_cache(targets: list[Target], contexts: dict[str, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    cache: dict[int, dict[str, Any]] = defaultdict(dict)
    for mask_name, ctx in contexts.items():
        intervals = ctx["intervals"]
        splits = ctx["splits"]["clean_peak_percentile"]
        non_overlap = ctx["non_overlap_ids"]
        by_frame: dict[int, list[int]] = defaultdict(list)
        for target in targets:
            if target.target_id in intervals:
                by_frame[target.frame_idx].append(target.target_id)
        for frame_idx, tids in by_frame.items():
            split_counts = Counter(splits.get(tid, "") for tid in tids)
            non_count = sum(1 for tid in tids if tid in non_overlap)
            cache[frame_idx][f"{mask_name}_weak_count"] = split_counts["weak"]
            cache[frame_idx][f"{mask_name}_mid_count"] = split_counts["mid"]
            cache[frame_idx][f"{mask_name}_strong_count"] = split_counts["strong"]
            cache[frame_idx][f"{mask_name}_target_count"] = len(tids)
            cache[frame_idx][f"{mask_name}_non_overlap_count"] = non_count
            cache[frame_idx][f"{mask_name}_has_overlap"] = non_count < len(tids)
    for frame_idx in cache:
        cache[frame_idx]["mask_types"] = ";".join(sorted(contexts))
    return cache


def generate_samples(
    manifest: list[dict[str, str]],
    frame_indices: np.ndarray,
    sir_names: list[str],
    split_name: str,
    clean_db: np.ndarray,
    frame_count_cache: dict[int, dict[str, Any]],
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, Any]], dict[str, dict[int, np.ndarray]], dict[str, dict[int, np.ndarray]]]:
    inputs: list[np.ndarray] = []
    targets: list[np.ndarray] = []
    rows: list[dict[str, Any]] = []
    inter_db_by_sir: dict[str, dict[int, np.ndarray]] = defaultdict(dict)
    inter_power_by_sir: dict[str, dict[int, np.ndarray]] = defaultdict(dict)
    sample_id = 0
    for frame_idx_raw in frame_indices.tolist():
        frame_idx = int(frame_idx_raw)
        adc = load_adc(frame_idx, manifest)
        for name in sir_names:
            cfg = sir_cfg(name)
            interfered_adc, params, summary = make_interference(
                adc, float(cfg["sir_db"]), int(cfg["num_interferers"]), rng
            )
            rp, _, _ = radar_maps(interfered_adc)
            inter_db = 10.0 * np.log10(rp + EPS)
            inputs.append(inter_db.astype(np.float32))
            targets.append(clean_db[frame_idx].astype(np.float32))
            inter_db_by_sir[name][frame_idx] = inter_db.astype(np.float64)
            inter_power_by_sir[name][frame_idx] = rp.astype(np.float64)
            sample_id += 1
            rows.append(
                {
                    "sample_id": f"{split_name}_{sample_id:05d}",
                    "split": split_name,
                    "frame_idx": frame_idx,
                    "frame_id": manifest[frame_idx]["new_frame_id"],
                    "source_sequence": manifest[frame_idx]["source_sequence"],
                    "sir_name": name,
                    "target_sir_db": float(cfg["sir_db"]),
                    "num_interferers": int(cfg["num_interferers"]),
                    "achieved_sir_db": summary["achieved_sir_db"],
                    "interference_params_json": json.dumps(params, ensure_ascii=False),
                    **frame_count_cache.get(frame_idx, {}),
                }
            )
    return np.stack(inputs), np.stack(targets), rows, inter_db_by_sir, inter_power_by_sir


def normalize(arr: np.ndarray, mean: float, std: float) -> np.ndarray:
    return ((arr - mean) / max(std, EPS)).astype(np.float32)


def denormalize(arr: np.ndarray, mean: float, std: float) -> np.ndarray:
    return arr.astype(np.float64) * max(std, EPS) + mean


def make_tensor(arr: np.ndarray, mean: float, std: float, device: torch.device) -> torch.Tensor:
    return torch.from_numpy(normalize(arr, mean, std)[:, None, :]).to(device)


def mse_np(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2))


def train_tiny(
    train_x: np.ndarray,
    train_y: np.ndarray,
    clean_y: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    torch.manual_seed(RANDOM_SEED)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    x = make_tensor(train_x[:TINY_SAMPLE_COUNT], mean, std, device)
    y = make_tensor(train_y[:TINY_SAMPLE_COUNT], mean, std, device)
    clean = make_tensor(clean_y[:TINY_SAMPLE_COUNT], mean, std, device)
    rows: list[dict[str, Any]] = []
    with torch.no_grad():
        initial_loss = float(torch.mean((model(x) - y) ** 2).item())
    for step in range(1, TINY_STEPS + 1):
        idx = torch.randint(0, x.shape[0], (min(TINY_BATCH_SIZE, x.shape[0]),), device=device)
        pred = model(x[idx])
        loss_main = torch.mean((pred - y[idx]) ** 2)
        pred_clean = model(clean[idx])
        loss_identity = torch.mean((pred_clean - clean[idx]) ** 2)
        loss = loss_main + IDENTITY_LOSS_WEIGHT * loss_identity
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step == 1 or step % 5 == 0 or step == TINY_STEPS:
            rows.append(
                {
                    "stage": "tiny_batch",
                    "step": step,
                    "epoch": "",
                    "train_loss": float(loss_main.item()),
                    "identity_loss": float(loss_identity.item()),
                    "total_loss": float(loss.item()),
                    "val_loss": "",
                }
            )
    with torch.no_grad():
        final_pred = model(x)
        final_loss = float(torch.mean((final_pred - y) ** 2).item())
        out_db = denormalize(final_pred.detach().cpu().numpy()[:, 0, :], mean, std)
    metrics = {
        "stage": "tiny_batch",
        "sample_count": int(x.shape[0]),
        "steps": TINY_STEPS,
        "initial_loss": initial_loss,
        "final_loss": final_loss,
        "loss_drop_fraction": (initial_loss - final_loss) / max(initial_loss, EPS),
        "input_mse_db": mse_np(train_x[:TINY_SAMPLE_COUNT], train_y[:TINY_SAMPLE_COUNT]),
        "output_mse_db": mse_np(out_db, train_y[:TINY_SAMPLE_COUNT]),
        "output_min_db": float(np.min(out_db)),
        "output_max_db": float(np.max(out_db)),
        "output_std_db": float(np.std(out_db)),
        "has_nan_or_inf": bool(not np.isfinite(out_db).all()),
    }
    return rows, metrics


def train_small(
    train_x: np.ndarray,
    train_y: np.ndarray,
    val_x: np.ndarray,
    val_y: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
) -> tuple[SimpleRangeFCN, list[dict[str, Any]], dict[str, Any]]:
    torch.manual_seed(RANDOM_SEED + 1)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    clean_train = make_tensor(train_y, mean, std, device)
    rows: list[dict[str, Any]] = []
    batch_size = min(BATCH_SIZE, x.shape[0])
    with torch.no_grad():
        initial_train_loss = float(torch.mean((model(x) - y) ** 2).item())
        initial_val_loss = float(torch.mean((model(valx) - valy) ** 2).item())
    for epoch in range(1, SMALL_EPOCHS + 1):
        perm = torch.randperm(x.shape[0], device=device)
        batch_losses: list[float] = []
        ident_losses: list[float] = []
        for start in range(0, x.shape[0], batch_size):
            idx = perm[start : start + batch_size]
            pred = model(x[idx])
            loss_main = torch.mean((pred - y[idx]) ** 2)
            pred_clean = model(clean_train[idx])
            loss_identity = torch.mean((pred_clean - clean_train[idx]) ** 2)
            loss = loss_main + IDENTITY_LOSS_WEIGHT * loss_identity
            opt.zero_grad()
            loss.backward()
            opt.step()
            batch_losses.append(float(loss_main.item()))
            ident_losses.append(float(loss_identity.item()))
        with torch.no_grad():
            val_loss = float(torch.mean((model(valx) - valy) ** 2).item())
        rows.append(
            {
                "stage": "small_subset",
                "step": "",
                "epoch": epoch,
                "train_loss": float(np.mean(batch_losses)),
                "identity_loss": float(np.mean(ident_losses)),
                "total_loss": float(np.mean(batch_losses) + IDENTITY_LOSS_WEIGHT * np.mean(ident_losses)),
                "val_loss": val_loss,
            }
        )
    with torch.no_grad():
        train_out = denormalize(model(x).detach().cpu().numpy()[:, 0, :], mean, std)
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
        final_train_loss = float(torch.mean((model(x) - y) ** 2).item())
        final_val_loss = float(torch.mean((model(valx) - valy) ** 2).item())
    metrics = {
        "stage": "small_subset",
        "train_sample_count": int(train_x.shape[0]),
        "val_sample_count": int(val_x.shape[0]),
        "epochs": SMALL_EPOCHS,
        "batch_size": batch_size,
        "initial_train_loss": initial_train_loss,
        "final_train_loss": final_train_loss,
        "train_loss_drop_fraction": (initial_train_loss - final_train_loss) / max(initial_train_loss, EPS),
        "initial_val_loss": initial_val_loss,
        "final_val_loss": final_val_loss,
        "val_loss_drop_fraction": (initial_val_loss - final_val_loss) / max(initial_val_loss, EPS),
        "train_input_mse_db": mse_np(train_x, train_y),
        "train_output_mse_db": mse_np(train_out, train_y),
        "val_input_mse_db": mse_np(val_x, val_y),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
    }
    return model, rows, metrics


def infer_db(model: nn.Module, arr_db: np.ndarray, mean: float, std: float, device: torch.device) -> np.ndarray:
    model.eval()
    outs: list[np.ndarray] = []
    with torch.no_grad():
        for start in range(0, arr_db.shape[0], 64):
            batch = make_tensor(arr_db[start : start + 64], mean, std, device)
            out = model(batch).detach().cpu().numpy()[:, 0, :]
            outs.append(denormalize(out, mean, std))
    return np.concatenate(outs, axis=0)


def power_from_db(arr_db: np.ndarray) -> np.ndarray:
    clipped = np.clip(arr_db, -120.0, 120.0)
    return np.power(10.0, clipped / 10.0).astype(np.float64)


def full_case_arrays(
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    frame_indices: np.ndarray,
    case_db_by_frame: dict[int, np.ndarray],
) -> tuple[np.ndarray, np.ndarray]:
    power = clean_power.copy()
    db_arr = clean_db.copy()
    for idx in frame_indices.tolist():
        if int(idx) in case_db_by_frame:
            db_arr[int(idx)] = case_db_by_frame[int(idx)]
            power[int(idx)] = power_from_db(case_db_by_frame[int(idx)][None, :])[0]
    return power, db_arr


def generate_eval_interference(
    manifest: list[dict[str, str]],
    frame_indices: np.ndarray,
    sir_names: list[str],
    rng: np.random.Generator,
) -> tuple[dict[str, dict[int, np.ndarray]], dict[str, dict[int, np.ndarray]], list[dict[str, Any]]]:
    inter_db: dict[str, dict[int, np.ndarray]] = defaultdict(dict)
    inter_power: dict[str, dict[int, np.ndarray]] = defaultdict(dict)
    rows: list[dict[str, Any]] = []
    for frame_idx_raw in frame_indices.tolist():
        frame_idx = int(frame_idx_raw)
        adc = load_adc(frame_idx, manifest)
        for name in sir_names:
            cfg = sir_cfg(name)
            interfered_adc, params, summary = make_interference(
                adc, float(cfg["sir_db"]), int(cfg["num_interferers"]), rng
            )
            rp, _, _ = radar_maps(interfered_adc)
            inter_power[name][frame_idx] = rp.astype(np.float64)
            inter_db[name][frame_idx] = 10.0 * np.log10(rp + EPS)
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
                    "split": "fixed_pfa_eval",
                }
            )
    return inter_db, inter_power, rows


def evaluate_cases(
    manifest: list[dict[str, str]],
    targets: list[Target],
    contexts: dict[str, dict[str, Any]],
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    val_idx: np.ndarray,
    test_idx: np.ndarray,
    case_arrays: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    fixed_rows: list[dict[str, Any]] = []
    by_mask_rows: list[dict[str, Any]] = []
    non_overlap_rows: list[dict[str, Any]] = []
    by_sequence_rows: list[dict[str, Any]] = []
    by_class_rows: list[dict[str, Any]] = []
    clean_no_harm_rows: list[dict[str, Any]] = []
    for case in case_arrays:
        scores = ca_cfar_score_1d_np(case["power"])
        for mask_name, ctx in contexts.items():
            target_mask = ctx["target_mask"]
            background_mask = ctx["background_mask"]
            intervals = ctx["intervals"]
            for split_definition, splits in ctx["splits"].items():
                noise_row, bias_row = range_noise_and_target_bias(
                    clean_power,
                    case["power"],
                    clean_db,
                    case["db"],
                    background_mask,
                    targets,
                    intervals,
                    test_idx,
                    mask_name,
                    str(case.get("sir_name", "")),
                    case.get("target_sir_db", ""),
                )
                for pfa in VALID_PFA_TARGETS:
                    threshold = float(np.quantile(scores[val_idx][background_mask[val_idx]], 1.0 - pfa))
                    for scope, allowed in [("all", None), ("non_overlap_only", ctx["non_overlap_ids"])]:
                        base = {
                            "mask_name": mask_name,
                            "split_definition": split_definition,
                            "target_pfa": pfa,
                            "input_type": case["input_type"],
                            "sir_name": case.get("sir_name", ""),
                            "target_sir_db": case.get("target_sir_db", ""),
                            "threshold_source": "input_specific_validation_background",
                            "mse_db_to_clean": mse_np(case["db"][test_idx], clean_db[test_idx]),
                            "mse_power_to_clean": mse_np(case["power"][test_idx], clean_power[test_idx]),
                            "noise_floor_change_db": noise_row["noise_floor_change_db"],
                            "background_energy_increase_db": noise_row["background_energy_increase_db"],
                            "target_peak_bias_db_mean": bias_row["target_peak_bias_db_mean"],
                            "target_peak_abs_bias_db_mean": bias_row["target_peak_abs_bias_db_mean"],
                        }
                        metrics = evaluate_scores(
                            scores,
                            threshold,
                            target_mask,
                            background_mask,
                            targets,
                            intervals,
                            splits,
                            test_idx,
                            scope,
                            allowed,
                        )
                        row = {**base, **metrics}
                        fixed_rows.append(row)
                        if scope == "all":
                            by_mask_rows.append(row)
                            by_sequence_rows.extend(
                                evaluate_by_sequence(
                                    "D2A_fixed_pfa",
                                    scores,
                                    threshold,
                                    background_mask,
                                    targets,
                                    intervals,
                                    manifest,
                                    test_idx,
                                    base,
                                )
                            )
                        else:
                            non_overlap_rows.append(row)
                        by_class_rows.extend(
                            evaluate_by_class_group(
                                "D2A_fixed_pfa",
                                scores,
                                threshold,
                                targets,
                                intervals,
                                splits,
                                test_idx,
                                base,
                                scope,
                                allowed,
                            )
                        )
                        if case["input_type"] == "model_clean":
                            clean_no_harm_rows.append(row)
    return {
        "fixed": fixed_rows,
        "by_mask": by_mask_rows,
        "non_overlap": non_overlap_rows,
        "by_sequence": by_sequence_rows,
        "by_class": by_class_rows,
        "clean_no_harm": clean_no_harm_rows,
    }


def pick_metric(
    rows: list[dict[str, Any]],
    input_type: str,
    sir_name: str = "",
    mask_name: str = "default",
    split_definition: str = "clean_peak_percentile",
    pfa: float = 0.01,
    scope: str = "all",
) -> dict[str, Any]:
    for row in rows:
        if (
            row["input_type"] == input_type
            and str(row.get("sir_name", "")) == sir_name
            and row["mask_name"] == mask_name
            and row["split_definition"] == split_definition
            and abs(float(row["target_pfa"]) - pfa) < 1e-12
            and row["target_scope"] == scope
        ):
            return row
    raise KeyError((input_type, sir_name, mask_name, split_definition, pfa, scope))


def plot_outputs(
    training_rows: list[dict[str, Any]],
    clean_db: np.ndarray,
    test_idx: np.ndarray,
    case_arrays: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    small_rows = [r for r in training_rows if r["stage"] == "small_subset"]
    tiny_rows = [r for r in training_rows if r["stage"] == "tiny_batch"]
    plt.figure(figsize=(8, 4), dpi=150)
    if tiny_rows:
        plt.plot([int(r["step"]) for r in tiny_rows], [float(r["train_loss"]) for r in tiny_rows], label="tiny train")
    if small_rows:
        plt.plot([int(r["epoch"]) for r in small_rows], [float(r["train_loss"]) for r in small_rows], label="small train")
        plt.plot([int(r["epoch"]) for r in small_rows], [float(r["val_loss"]) for r in small_rows], label="small val")
    plt.yscale("log")
    plt.xlabel("Step / epoch")
    plt.ylabel("MSE loss")
    plt.title("D2A training loss curve")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "training_loss_curve.png")
    plt.close()

    sample_frame = int(test_idx[0])
    case_lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    plt.figure(figsize=(9, 4), dpi=150)
    x = np.arange(clean_db.shape[1])
    plt.plot(x, clean_db[sample_frame], label="clean")
    if ("interfered", "medium") in case_lookup:
        plt.plot(x, case_lookup[("interfered", "medium")]["db"][sample_frame], label="interfered medium")
    if ("model_output", "medium") in case_lookup:
        plt.plot(x, case_lookup[("model_output", "medium")]["db"][sample_frame], label="model output medium")
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.title("Clean vs interfered vs model output range profile")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_vs_interfered_vs_model_output_range_profile.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    plt.plot(x, clean_db[sample_frame], label="clean")
    if ("model_clean", "") in case_lookup:
        plt.plot(x, case_lookup[("model_clean", "")]["db"][sample_frame], label="model(clean)")
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.title("Model clean-input output")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "model_clean_input_output.png")
    plt.close()

    rows = [
        r
        for r in fixed_rows
        if r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and r["target_scope"] == "all"
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
        and (r["input_type"], str(r.get("sir_name", ""))) in {("clean", ""), ("interfered", "medium"), ("model_output", "medium"), ("model_clean", "")}
    ]
    labels = [f"{r['input_type']} {r.get('sir_name','')}".strip() for r in rows]
    plt.figure(figsize=(9, 4), dpi=150)
    width = 0.25
    xs = np.arange(len(rows))
    plt.bar(xs - width, [float(r["weak_pd"]) for r in rows], width, label="weak")
    plt.bar(xs, [float(r["mid_pd"]) for r in rows], width, label="mid")
    plt.bar(xs + width, [float(r["strong_pd"]) for r in rows], width, label="strong")
    plt.xticks(xs, labels, rotation=20, ha="right")
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.title("Weak/mid/strong Pd bar plot")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_pd_bar_plot.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    plt.plot(labels, [float(r["measured_pfa"]) for r in rows], marker="o", label="PFA")
    plt.ylabel("Measured PFA")
    plt.xticks(rotation=20, ha="right")
    plt.title("PFA plot")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_plot.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    plt.bar(labels, [float(r["false_alarm_count"]) for r in rows])
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("False alarm count")
    plt.title("False alarm count plot")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "false_alarm_count_plot.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    plt.bar(labels, [float(r["target_peak_abs_bias_db_mean"]) for r in rows])
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Mean abs target peak bias (dB)")
    plt.title("Target peak bias histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_bias_histogram.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    plt.bar(labels, [float(r["noise_floor_change_db"]) for r in rows])
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Noise floor change (dB)")
    plt.title("Noise floor change histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "noise_floor_change_histogram.png")
    plt.close()


def write_model_summary(path: Path, model: nn.Module, n_bins: int, device: torch.device, mean: float, std: float) -> None:
    param_count = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    text = f"""D2A model summary

Model: SimpleRangeFCN
Input shape: batch x 1 x {n_bins}
Output shape: batch x 1 x {n_bins}
Parameter count: {param_count}
Trainable parameters: {trainable}
Device: {device}
Normalization mean dB: {mean:.6f}
Normalization std dB: {std:.6f}
Architecture:
{model}
"""
    path.write_text(text, encoding="utf-8")


def write_report(
    tiny_metrics: dict[str, Any],
    small_metrics: dict[str, Any],
    fixed_rows: list[dict[str, Any]],
    clean_no_harm_rows: list[dict[str, Any]],
    model_summary: dict[str, Any],
) -> tuple[bool, str]:
    clean = pick_metric(fixed_rows, "clean")
    inter_medium = pick_metric(fixed_rows, "interfered", "medium")
    model_medium = pick_metric(fixed_rows, "model_output", "medium")
    model_clean = pick_metric(fixed_rows, "model_clean")
    narrow_clean = pick_metric(fixed_rows, "clean", mask_name="narrow")
    narrow_model = pick_metric(fixed_rows, "model_output", "medium", mask_name="narrow")
    non_clean = pick_metric(fixed_rows, "clean", scope="non_overlap_only")
    non_model = pick_metric(fixed_rows, "model_output", "medium", scope="non_overlap_only")

    dataloader_ok = model_summary["train_sample_count"] > 0 and model_summary["val_sample_count"] > 0
    shape_ok = model_summary["input_shape"] == model_summary["output_shape"]
    tiny_ok = float(tiny_metrics["loss_drop_fraction"]) > 0.5
    small_ok = float(small_metrics["train_loss_drop_fraction"]) > 0.2 and float(small_metrics["val_loss_drop_fraction"]) > 0.0
    nan_ok = not bool(tiny_metrics["has_nan_or_inf"]) and not bool(small_metrics["has_nan_or_inf"])
    output_ok = float(small_metrics["output_std_db"]) > 1e-4
    mse_ok = float(small_metrics["val_output_mse_db"]) <= float(small_metrics["val_input_mse_db"]) * 1.05
    fixed_ok = len(fixed_rows) > 0 and all(str(r.get("measured_pfa", "")) != "" for r in fixed_rows)
    clean_no_harm_ok = (
        float(model_clean["mse_db_to_clean"]) < 1.0
        and abs(float(model_clean["target_peak_bias_db_mean"])) < 0.5
        and float(model_clean["measured_pfa"]) < 0.05
    )
    mask_consistent = (float(model_medium["weak_pd"]) - float(inter_medium["weak_pd"])) * (
        float(narrow_model["weak_pd"]) - float(narrow_clean["weak_pd"])
    ) >= 0
    non_overlap_consistent = (float(model_medium["weak_pd"]) - float(inter_medium["weak_pd"])) * (
        float(non_model["weak_pd"]) - float(non_clean["weak_pd"])
    ) >= 0
    d2a_pass = all(
        [
            dataloader_ok,
            shape_ok,
            tiny_ok,
            small_ok,
            nan_ok,
            output_ok,
            mse_ok,
            fixed_ok,
            clean_no_harm_ok,
            mask_consistent,
            non_overlap_consistent,
        ]
    )
    next_step = (
        "可以进入 D3，但 D3 仍应先从 MSE/MAGMSE baseline 和 ordinary differentiable CA-CFAR BCE 开始，不要直接上 weak-target full loss。"
        if d2a_pass
        else "不建议进入 D3；应先修 dataloader/model/loss 中未通过的环节。"
    )

    key_rows = [clean, inter_medium, model_medium, model_clean]
    def md_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
        lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
        for row in rows:
            vals: list[str] = []
            for col in cols:
                val = row.get(col, "")
                try:
                    vals.append(f"{float(val):.4f}" if val != "" else "")
                except Exception:
                    vals.append(str(val))
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    report = f"""# D2A Gao77 Small Model Sanity 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D2A，仅 range-only simple FCN / 小 batch overfit sanity  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次只执行 D2A。没有进入 D3-D14，没有跑正式 baseline，没有做 MSE vs BCE vs focal 对比，没有实现 weak-target full loss，没有做 3 seeds，没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D2A 是否通过 | {'通过' if d2a_pass else '未通过'} |
| 使用模型 | simple FCN |
| 输入输出 shape 是否正确 | {'是' if shape_ok else '否'} |
| tiny batch 是否能 overfit | {'是' if tiny_ok else '否'} |
| small subset loss 是否下降 | {'是' if small_ok else '否'} |
| 输出是否有 NaN/Inf | {'否' if nan_ok else '是'} |
| model output 是否比 interfered 更接近 clean | {'是' if mse_ok else '否'} |
| fixed-PFA 是否能评估 model output | {'是' if fixed_ok else '否'} |
| clean-input no-harm 是否明显失败 | {'否' if clean_no_harm_ok else '是'} |
| narrow/default mask 趋势是否一致 | {'是' if mask_consistent else '否'} |
| all targets 与 non-overlap-only 是否一致 | {'是' if non_overlap_consistent else '否'} |
| 当前是否建议进入 D3 | {'是' if d2a_pass else '否'} |
| 下一步 | {next_step} |

## 3. 训练 Sanity

| stage | initial_loss | final_loss | loss_drop_fraction | input_mse_db | output_mse_db |
|---|---:|---:|---:|---:|---:|
| tiny_batch | {tiny_metrics['initial_loss']:.6f} | {tiny_metrics['final_loss']:.6f} | {tiny_metrics['loss_drop_fraction']:.4f} | {tiny_metrics['input_mse_db']:.6f} | {tiny_metrics['output_mse_db']:.6f} |
| small_subset_train | {small_metrics['initial_train_loss']:.6f} | {small_metrics['final_train_loss']:.6f} | {small_metrics['train_loss_drop_fraction']:.4f} | {small_metrics['train_input_mse_db']:.6f} | {small_metrics['train_output_mse_db']:.6f} |
| small_subset_val | {small_metrics['initial_val_loss']:.6f} | {small_metrics['final_val_loss']:.6f} | {small_metrics['val_loss_drop_fraction']:.4f} | {small_metrics['val_input_mse_db']:.6f} | {small_metrics['val_output_mse_db']:.6f} |

## 4. Fixed-PFA Sanity

默认 mask、clean_peak_percentile、PFA=1e-2：

{md_table(key_rows, ['input_type', 'sir_name', 'mse_db_to_clean', 'measured_pfa', 'false_alarm_count', 'background_cell_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'noise_floor_change_db', 'target_peak_abs_bias_db_mean'])}

## 5. Clean-Input No-Harm

model(clean) 默认 mask、PFA=1e-2：

{md_table([model_clean], ['mse_db_to_clean', 'measured_pfa', 'false_alarm_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'noise_floor_change_db', 'target_peak_bias_db_mean', 'target_peak_abs_bias_db_mean'])}

## 6. 注意事项

- D2A 只说明训练链路、shape、loss 和 fixed-PFA evaluation 能跑通，不说明方法优于 baseline。
- severe interference 只作为 stress test，不作为 D2A 主要训练 sanity 判断。
- 后续 D3 必须单独跑 MSE/MAGMSE baseline 和 ordinary differentiable CA-CFAR BCE，不能把 D2A 的 simple FCN 结果当正式 baseline。

## 7. 输出文件

结果目录：

`G:\\mineru_output\\results\\d2a_gao77_small_model_sanity`

图像目录：

`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d2a_figures`

关键文件：

- `d2a_config.json`
- `d2a_dataset_manifest.csv`
- `d2a_model_summary.txt`
- `d2a_training_loss.csv`
- `d2a_tiny_batch_overfit_metrics.csv`
- `d2a_small_subset_metrics.csv`
- `d2a_fixed_pfa_metrics.csv`
- `d2a_clean_no_harm_metrics.csv`
- `d2a_metrics_by_mask.csv`
- `d2a_metrics_non_overlap_only.csv`
- `d2a_metrics_by_sequence.csv`
- `d2a_metrics_by_class_group.csv`

## 8. D3 建议

{next_step}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return d2a_pass, str(report_ts)


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    manifest, targets, clean_power, clean_db, clean_rd = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    train_frames = np.asarray(train_all[:N_TRAIN_FRAMES], dtype=int)
    val_frames = np.asarray(val_all[:N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[:N_TEST_FRAMES], dtype=int)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    contexts = build_mask_context(clean_db, clean_cfar, targets)
    frame_count_cache = build_frame_count_cache(targets, contexts)

    rng = np.random.default_rng(RANDOM_SEED + 200)
    train_x, train_y, train_rows, _, _ = generate_samples(
        manifest, train_frames, TRAIN_SIR_NAMES, "train", clean_db, frame_count_cache, rng
    )
    val_x, val_y, val_rows, val_inter_db_train, val_inter_power_train = generate_samples(
        manifest, val_frames, VAL_SIR_NAMES, "validation", clean_db, frame_count_cache, rng
    )
    # Severe validation is generated only for fixed-PFA calibration, not for training sanity loss.
    eval_val_inter_db, eval_val_inter_power, eval_val_rows = generate_eval_interference(
        manifest, val_frames, EVAL_SIR_NAMES, rng
    )
    eval_test_inter_db, eval_test_inter_power, eval_test_rows = generate_eval_interference(
        manifest, test_frames, EVAL_SIR_NAMES, rng
    )

    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    norm_mean = float(norm_values.mean())
    norm_std = float(norm_values.std())

    tiny_loss_rows, tiny_metrics = train_tiny(train_x, train_y, train_y, norm_mean, norm_std, device)
    model, small_loss_rows, small_metrics = train_small(train_x, train_y, val_x, val_y, norm_mean, norm_std, device)
    training_rows = tiny_loss_rows + small_loss_rows

    eval_indices = np.unique(np.concatenate([val_frames, test_frames]))
    clean_eval_db = clean_db[eval_indices]
    model_clean_eval_db = infer_db(model, clean_eval_db, norm_mean, norm_std, device)
    model_clean_by_frame = {int(idx): model_clean_eval_db[i] for i, idx in enumerate(eval_indices.tolist())}
    case_arrays: list[dict[str, Any]] = [
        {"input_type": "clean", "sir_name": "", "target_sir_db": "", "power": clean_power, "db": clean_db}
    ]
    model_clean_power, model_clean_db = full_case_arrays(clean_power, clean_db, eval_indices, model_clean_by_frame)
    case_arrays.append(
        {"input_type": "model_clean", "sir_name": "", "target_sir_db": "", "power": model_clean_power, "db": model_clean_db}
    )

    for name in EVAL_SIR_NAMES:
        inter_db_by_frame: dict[int, np.ndarray] = {}
        inter_db_by_frame.update(eval_val_inter_db[name])
        inter_db_by_frame.update(eval_test_inter_db[name])
        inter_power, inter_db_full = full_case_arrays(clean_power, clean_db, eval_indices, inter_db_by_frame)
        cfg = sir_cfg(name)
        case_arrays.append(
            {
                "input_type": "interfered",
                "sir_name": name,
                "target_sir_db": float(cfg["sir_db"]),
                "power": inter_power,
                "db": inter_db_full,
            }
        )
        model_out_eval_db = infer_db(
            model,
            np.stack([inter_db_by_frame[int(idx)] for idx in eval_indices.tolist()]),
            norm_mean,
            norm_std,
            device,
        )
        model_out_by_frame = {int(idx): model_out_eval_db[i] for i, idx in enumerate(eval_indices.tolist())}
        model_power, model_db = full_case_arrays(clean_power, clean_db, eval_indices, model_out_by_frame)
        case_arrays.append(
            {
                "input_type": "model_output",
                "sir_name": name,
                "target_sir_db": float(cfg["sir_db"]),
                "power": model_power,
                "db": model_db,
            }
        )

    metrics = evaluate_cases(manifest, targets, contexts, clean_power, clean_db, val_frames, test_frames, case_arrays)
    plot_outputs(training_rows, clean_db, test_frames, case_arrays, metrics["fixed"])

    dataset_rows = train_rows + val_rows + eval_val_rows + eval_test_rows
    write_csv(RESULT_DIR / "d2a_dataset_manifest.csv", dataset_rows)
    write_model_summary(RESULT_DIR / "d2a_model_summary.txt", model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    write_csv(RESULT_DIR / "d2a_training_loss.csv", training_rows)
    write_csv(RESULT_DIR / "d2a_tiny_batch_overfit_metrics.csv", [tiny_metrics])
    write_csv(RESULT_DIR / "d2a_small_subset_metrics.csv", [small_metrics])
    write_csv(RESULT_DIR / "d2a_fixed_pfa_metrics.csv", metrics["fixed"])
    write_csv(RESULT_DIR / "d2a_clean_no_harm_metrics.csv", metrics["clean_no_harm"])
    write_csv(RESULT_DIR / "d2a_metrics_by_mask.csv", metrics["by_mask"])
    write_csv(RESULT_DIR / "d2a_metrics_non_overlap_only.csv", metrics["non_overlap"])
    write_csv(RESULT_DIR / "d2a_metrics_by_sequence.csv", metrics["by_sequence"])
    write_csv(RESULT_DIR / "d2a_metrics_by_class_group.csv", metrics["by_class"])

    model_summary = {
        "model": "SimpleRangeFCN",
        "device": str(device),
        "input_shape": [1, 1, EXPECTED_ADC_SHAPE[0]],
        "output_shape": [1, 1, EXPECTED_ADC_SHAPE[0]],
        "parameter_count": sum(p.numel() for p in model.parameters()),
        "train_sample_count": int(train_x.shape[0]),
        "val_sample_count": int(val_x.shape[0]),
        "test_frame_count": int(test_frames.size),
    }
    config = {
        "stage": "D2A",
        "strict_limits": {
            "only_d2a": True,
            "no_d3_d14": True,
            "no_formal_baseline": True,
            "no_mse_bce_focal_comparison": True,
            "no_weak_target_full_loss": True,
            "no_3_seeds": True,
            "no_rdlr_diffirm_rimformer": True,
            "no_large_model": True,
        },
        "model": model_summary,
        "simple_fcn": {
            "hidden": 128,
            "residual_identity_init": True,
            "learning_rate": LEARNING_RATE,
            "batch_size": BATCH_SIZE,
            "tiny_steps": TINY_STEPS,
            "small_epochs": SMALL_EPOCHS,
            "identity_loss_weight": IDENTITY_LOSS_WEIGHT,
        },
        "data": {
            "train_frames": int(train_frames.size),
            "train_samples": int(train_x.shape[0]),
            "val_frames": int(val_frames.size),
            "val_samples_for_loss": int(val_x.shape[0]),
            "test_frames": int(test_frames.size),
            "train_sir_names": TRAIN_SIR_NAMES,
            "val_sir_names": VAL_SIR_NAMES,
            "test_sir_names": TEST_SIR_NAMES,
            "severe_validation_generated_for_fixed_pfa_calibration_only": True,
        },
        "normalization": {"mean_db": norm_mean, "std_db": norm_std},
        "valid_pfa_targets": VALID_PFA_TARGETS,
        "mask_names": sorted(ACTIVE_MASK_NAMES),
    }
    write_json(RESULT_DIR / "d2a_config.json", config)
    d2a_pass, report_ts = write_report(tiny_metrics, small_metrics, metrics["fixed"], metrics["clean_no_harm"], model_summary)
    print(
        json.dumps(
            {
                "d2a_pass": d2a_pass,
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "report": str(REPORT_PATH),
                "timestamped_report": report_ts,
                "device": str(device),
                "train_samples": int(train_x.shape[0]),
                "val_samples": int(val_x.shape[0]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
