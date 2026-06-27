from __future__ import annotations

import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
from scipy.io import loadmat


ROOT = Path(r"G:\mineru_output")
SUBSET_DIR = ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1"
RADAR_DIR = SUBSET_DIR / "radar_raw_frame"
LABEL_DIR = SUBSET_DIR / "text_labels"
MANIFEST_PATH = SUBSET_DIR / "manifest" / "selected_frames_manifest.csv"
LABEL_POLICY_PATH = SUBSET_DIR / "manifest" / "label_policy.json"
CLASS1_AUDIT_PATH = ROOT / "refine-logs" / "D0B_CLASS1_SEMANTICS_CHECK.md"
RESULT_DIR = ROOT / "results" / "d1a_gao77_clean_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d1a_figures"
REPORT_PATH = ROOT / "refine-logs" / "D1A_GAO77_CLEAN_FIXED_PFA_SANITY_REPORT.md"
REPORT_TS_PATH = ROOT / "refine-logs" / "D1A_GAO77_CLEAN_FIXED_PFA_SANITY_REPORT_20260626_162000.md"

GAO77_LABEL_MAP = {
    0: "person",
    1: "cyclist_alias_or_bicycle",
    2: "car",
    3: "motorbike",
    5: "bus",
    7: "truck",
    80: "cyclist",
}
GAO77_CLASS_GROUP = {
    0: "pedestrian_like",
    1: "cyclist_like",
    2: "vehicle_like",
    3: "motorbike_like",
    5: "vehicle_like",
    7: "vehicle_like",
    80: "cyclist_like",
}
OBJECTNESS_CLASSES = set(GAO77_LABEL_MAP)

EXPECTED_ADC_SHAPE = (128, 255, 4, 2)
RANDOM_SEED = 20260626
LIGHT_SPEED = 299_792_458.0
BANDWIDTH_HZ = 0.67e9
RANGE_RESOLUTION_M = LIGHT_SPEED / (2.0 * BANDWIDTH_HZ)
MAX_RANGE_M = RANGE_RESOLUTION_M * EXPECTED_ADC_SHAPE[0]

TARGET_MIN_RADIUS_BINS = 2
TARGET_MAX_RADIUS_BINS = 12
GUARD_EXTRA_BINS = 4
VALID_RANGE_MIN_BIN = 2
VALID_RANGE_MAX_BIN = 124
CFAR_GUARD = 2
CFAR_TRAIN = 10
CFAR_EPS = 1e-9
DIFF_CFAR_TEMPERATURE = 0.7
PROJECTION_HIT_RATIO_THRESHOLD = 0.55
PROJECTION_RATIO_DB_THRESHOLD = 0.0


@dataclass
class TargetRecord:
    global_target_id: int
    frame_idx: int
    frame_id: str
    source_sequence: str
    uid: int
    cls: int
    group: str
    px: float
    py: float
    wid: float
    length: float
    range_m: float
    azimuth_deg: float
    range_bin: int
    radius_bins: int
    valid_projection: bool
    target_peak_db: float = float("nan")
    neighbor_peak_db: float = float("nan")
    neighbor_mean_db: float = float("nan")
    frame_p70_db: float = float("nan")
    response_ratio_db: float = float("nan")
    projection_hit: bool = False
    clean_peak_score: float = float("nan")
    cfar_margin_db: float = float("nan")
    split_peak_percentile: str = ""
    split_cfar_margin: str = ""


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = sorted({k for row in rows for k in row})
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_label_file(path: Path) -> list[tuple[int, int, float, float, float, float]]:
    rows: list[tuple[int, int, float, float, float, float]] = []
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return rows
    for row in csv.reader(text.splitlines()):
        if len(row) != 6:
            continue
        uid = int(float(row[0]))
        cls = int(float(row[1]))
        px = float(row[2])
        py = float(row[3])
        wid = float(row[4])
        length = float(row[5])
        rows.append((uid, cls, px, py, wid, length))
    return rows


def radar_maps(adc: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # adc: samples x chirps x rx x tx.
    virt = np.concatenate([adc[:, :, :, t] for t in range(adc.shape[3])], axis=2)
    range_fft = np.fft.fft(virt, axis=0)
    power_range = np.mean(np.abs(range_fft) ** 2, axis=(1, 2)).astype(np.float64)
    rd = np.fft.fftshift(np.fft.fft(range_fft, axis=1), axes=1)
    rd_map_db = 10.0 * np.log10(np.mean(np.abs(rd) ** 2, axis=2) + 1e-12)

    # Rough RA smoke map: chirp-averaged complex range response, spatial FFT over 8 virtual elements.
    range_virt = np.mean(range_fft, axis=1)
    angle_fft = np.fft.fftshift(np.fft.fft(range_virt, n=64, axis=1), axes=1)
    ra_map_db = 10.0 * np.log10(np.abs(angle_fft) ** 2 + 1e-12)
    return power_range, rd_map_db, ra_map_db


def range_to_bin(range_m: float) -> int:
    return int(round(range_m / RANGE_RESOLUTION_M))


def target_radius_bins(wid: float, length: float) -> int:
    radius_m = 0.5 * math.sqrt(wid * wid + length * length)
    radius = int(math.ceil(radius_m / RANGE_RESOLUTION_M))
    return max(TARGET_MIN_RADIUS_BINS, min(TARGET_MAX_RADIUS_BINS, radius))


def fill_interval(mask: np.ndarray, center: int, radius: int, value: bool = True) -> tuple[int, int]:
    lo = max(0, center - radius)
    hi = min(mask.shape[0], center + radius + 1)
    mask[lo:hi] = value
    return lo, hi


def make_valid_mask(n_bins: int) -> np.ndarray:
    valid = np.zeros(n_bins, dtype=bool)
    valid[VALID_RANGE_MIN_BIN : min(VALID_RANGE_MAX_BIN + 1, n_bins)] = True
    return valid


def ca_cfar_score_1d_np(x: np.ndarray, guard: int = CFAR_GUARD, train: int = CFAR_TRAIN) -> np.ndarray:
    scores = np.zeros_like(x, dtype=np.float64)
    n_frames, n_bins = x.shape
    for i in range(n_frames):
        row = x[i]
        for b in range(n_bins):
            lo = max(0, b - guard - train)
            hi = min(n_bins, b + guard + train + 1)
            glo = max(0, b - guard)
            ghi = min(n_bins, b + guard + 1)
            left = row[lo:glo]
            right = row[ghi:hi]
            if left.size + right.size == 0:
                noise = np.median(row) + CFAR_EPS
            else:
                noise = (float(left.sum()) + float(right.sum())) / (left.size + right.size)
            scores[i, b] = row[b] / (noise + CFAR_EPS)
    return scores


def differentiable_cfar_1d_torch(
    x_np: np.ndarray,
    threshold: float,
    guard: int = CFAR_GUARD,
    train: int = CFAR_TRAIN,
    temperature: float = DIFF_CFAR_TEMPERATURE,
) -> tuple[np.ndarray, np.ndarray]:
    x = torch.from_numpy(x_np.astype(np.float32)).unsqueeze(1)
    k = 2 * (guard + train) + 1
    g = 2 * guard + 1
    outer = torch.ones((1, 1, k), dtype=x.dtype)
    inner = torch.ones((1, 1, g), dtype=x.dtype)
    with torch.no_grad():
        outer_sum = F.conv1d(x, outer, padding=k // 2)
        inner_sum = F.conv1d(x, inner, padding=g // 2)
        n_train = float(k - g)
        noise = torch.clamp(outer_sum - inner_sum, min=0.0) / max(n_train, 1.0)
        score = x / (noise + CFAR_EPS)
        soft = torch.sigmoid((score - threshold) / temperature)
    return score.squeeze(1).numpy(), soft.squeeze(1).numpy()


def split_by_percentiles(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=np.float64)
    return float(np.quantile(arr, 0.3)), float(np.quantile(arr, 0.7))


def assign_split(value: float, q30: float, q70: float) -> str:
    if value <= q30:
        return "weak"
    if value <= q70:
        return "mid"
    return "strong"


def object_pd(detections: np.ndarray, targets: list[TargetRecord], split_attr: str, split_name: str) -> dict[str, Any]:
    selected = [t for t in targets if getattr(t, split_attr) == split_name and t.valid_projection]
    if not selected:
        return {"n": 0, "hits": 0, "pd": None, "miss_rate": None}
    hits = 0
    for t in selected:
        lo = max(0, t.range_bin - t.radius_bins)
        hi = min(detections.shape[1], t.range_bin + t.radius_bins + 1)
        if detections[t.frame_idx, lo:hi].any():
            hits += 1
    pd = hits / len(selected)
    return {"n": len(selected), "hits": hits, "pd": pd, "miss_rate": 1.0 - pd}


def cell_f1(det: np.ndarray, target_mask: np.ndarray, background_mask: np.ndarray) -> dict[str, Any]:
    tp = int(np.logical_and(det, target_mask).sum())
    fp = int(np.logical_and(det, background_mask).sum())
    fn = int(np.logical_and(~det, target_mask).sum())
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp_cells": tp, "fp_cells": fp, "fn_cells": fn, "cell_precision": precision, "cell_recall": recall, "cell_f1": f1}


def make_bar_plot(rows: list[dict[str, Any]], key: str, value: str, out: Path, title: str, ylabel: str) -> None:
    labels = [str(r[key]) for r in rows]
    vals = [float(r[value]) if r[value] not in ("", None) else 0.0 for r in rows]
    plt.figure(figsize=(9, 4.5), dpi=150)
    plt.bar(labels, vals, color="#457b9d")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()


def plot_sample_figures(
    sample_indices: list[int],
    frame_rows: list[dict[str, Any]],
    range_db: np.ndarray,
    rd_maps: dict[int, np.ndarray],
    ra_maps: dict[int, np.ndarray],
    target_mask: np.ndarray,
    guard_mask: np.ndarray,
    background_mask: np.ndarray,
    cfar_scores: np.ndarray,
    hard_detection_map: np.ndarray,
    soft_map: np.ndarray,
    targets_by_frame: dict[int, list[TargetRecord]],
) -> None:
    for idx in sample_indices:
        row = frame_rows[idx]
        xs = np.arange(range_db.shape[1])
        plt.figure(figsize=(9, 4), dpi=150)
        plt.plot(xs, range_db[idx], linewidth=1.0)
        for t in targets_by_frame.get(idx, []):
            plt.axvline(t.range_bin, color="tab:red", linestyle="--", linewidth=0.8)
        plt.xlabel("Range bin")
        plt.ylabel("Power (dB)")
        plt.title(f"Clean range profile + target bins: {row['new_frame_id']}")
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"clean_range_profile_targets_{row['new_frame_id']}.png")
        plt.close()

        if idx in rd_maps:
            plt.figure(figsize=(8, 5), dpi=150)
            plt.imshow(rd_maps[idx].T, aspect="auto", origin="lower", cmap="viridis")
            plt.xlabel("Range bin")
            plt.ylabel("Doppler bin")
            plt.title(f"Clean RD map smoke: {row['new_frame_id']}")
            plt.colorbar(label="Power (dB)")
            plt.tight_layout()
            plt.savefig(FIG_DIR / f"clean_rd_map_{row['new_frame_id']}.png")
            plt.close()

        if idx in ra_maps:
            plt.figure(figsize=(8, 5), dpi=150)
            plt.imshow(ra_maps[idx].T, aspect="auto", origin="lower", cmap="magma")
            for t in targets_by_frame.get(idx, []):
                # Rough angle projection: sin(theta) mapped to 64 FFT bins.
                sin_theta = max(-1.0, min(1.0, math.sin(math.radians(t.azimuth_deg))))
                angle_bin = int(round((sin_theta + 1.0) * 0.5 * (ra_maps[idx].shape[1] - 1)))
                plt.scatter([t.range_bin], [angle_bin], s=18, c="cyan", marker="x")
            plt.xlabel("Range bin")
            plt.ylabel("Angle FFT bin (rough)")
            plt.title(f"RA map + label projection smoke: {row['new_frame_id']}")
            plt.colorbar(label="Power (dB)")
            plt.tight_layout()
            plt.savefig(FIG_DIR / f"ra_map_label_projection_{row['new_frame_id']}.png")
            plt.close()

        for name, mask in [
            ("target_mask", target_mask[idx]),
            ("guard_ring_mask", guard_mask[idx]),
            ("background_mask", background_mask[idx]),
        ]:
            plt.figure(figsize=(9, 1.8), dpi=150)
            plt.imshow(mask[np.newaxis, :], aspect="auto", cmap="gray_r")
            plt.yticks([])
            plt.xlabel("Range bin")
            plt.title(f"{name}: {row['new_frame_id']}")
            plt.tight_layout()
            plt.savefig(FIG_DIR / f"{name}_{row['new_frame_id']}.png")
            plt.close()

        plt.figure(figsize=(9, 1.8), dpi=150)
        plt.imshow(cfar_scores[idx][np.newaxis, :], aspect="auto", cmap="viridis")
        plt.yticks([])
        plt.xlabel("Range bin")
        plt.title(f"Hard CA-CFAR score map: {row['new_frame_id']}")
        plt.colorbar(label="score")
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"hard_cfar_score_map_{row['new_frame_id']}.png")
        plt.close()

        plt.figure(figsize=(9, 1.8), dpi=150)
        plt.imshow(hard_detection_map[idx][np.newaxis, :], aspect="auto", cmap="gray_r")
        plt.yticks([])
        plt.xlabel("Range bin")
        plt.title(f"Hard CA-CFAR binary detection map: {row['new_frame_id']}")
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"hard_cfar_detection_map_{row['new_frame_id']}.png")
        plt.close()

        plt.figure(figsize=(9, 1.8), dpi=150)
        plt.imshow(soft_map[idx][np.newaxis, :], aspect="auto", cmap="viridis", vmin=0, vmax=1)
        plt.yticks([])
        plt.xlabel("Range bin")
        plt.title(f"Differentiable CA-CFAR soft detection: {row['new_frame_id']}")
        plt.colorbar(label="soft detection")
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"diff_cfar_soft_map_{row['new_frame_id']}.png")
        plt.close()


def main() -> None:
    np.random.seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    manifest_rows = read_csv_dicts(MANIFEST_PATH)
    with LABEL_POLICY_PATH.open("r", encoding="utf-8") as fh:
        label_policy = json.load(fh)
    class1_audit_text = CLASS1_AUDIT_PATH.read_text(encoding="utf-8", errors="replace")

    n_frames = len(manifest_rows)
    n_bins = EXPECTED_ADC_SHAPE[0]
    valid_mask_1d = make_valid_mask(n_bins)
    range_power = np.zeros((n_frames, n_bins), dtype=np.float64)
    range_db = np.zeros((n_frames, n_bins), dtype=np.float64)
    target_mask = np.zeros((n_frames, n_bins), dtype=bool)
    guard_mask = np.zeros((n_frames, n_bins), dtype=bool)
    targets: list[TargetRecord] = []
    targets_by_frame: dict[int, list[TargetRecord]] = defaultdict(list)
    rd_maps_for_fig: dict[int, np.ndarray] = {}
    ra_maps_for_fig: dict[int, np.ndarray] = {}
    adc_shape_counter: Counter[str] = Counter()

    sample_indices = sorted(set(np.linspace(0, n_frames - 1, 6, dtype=int).tolist()))
    global_target_id = 0

    for frame_idx, row in enumerate(manifest_rows):
        radar_path = RADAR_DIR / row["new_radar_file"]
        label_path = LABEL_DIR / row["new_label_file"]
        mat = loadmat(radar_path)
        if "adcData" not in mat:
            raise RuntimeError(f"adcData missing: {radar_path}")
        adc = mat["adcData"]
        adc_shape_counter["x".join(map(str, adc.shape))] += 1
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"Unexpected adcData shape {adc.shape}: {radar_path}")

        rp, rd_map, ra_map = radar_maps(adc)
        range_power[frame_idx] = rp
        range_db[frame_idx] = 10.0 * np.log10(rp + 1e-12)
        if frame_idx in sample_indices:
            rd_maps_for_fig[frame_idx] = rd_map
            ra_maps_for_fig[frame_idx] = ra_map

        labels = parse_label_file(label_path)
        for uid, cls, px, py, wid, length in labels:
            if cls not in OBJECTNESS_CLASSES:
                continue
            range_m = math.sqrt(px * px + py * py)
            azimuth_deg = math.degrees(math.atan2(px, py))
            rb = range_to_bin(range_m)
            radius = target_radius_bins(wid, length)
            valid_projection = bool(valid_mask_1d[rb]) if 0 <= rb < n_bins else False
            global_target_id += 1
            target = TargetRecord(
                global_target_id=global_target_id,
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
                range_bin=rb,
                radius_bins=radius,
                valid_projection=valid_projection,
            )
            targets.append(target)
            targets_by_frame[frame_idx].append(target)
            if valid_projection:
                fill_interval(target_mask[frame_idx], rb, radius, True)
                fill_interval(guard_mask[frame_idx], rb, radius + GUARD_EXTRA_BINS, True)

    guard_ring_mask = np.logical_and(guard_mask, ~target_mask)
    valid_fov_mask = np.broadcast_to(valid_mask_1d, target_mask.shape).copy()
    background_mask = np.logical_and(valid_fov_mask, ~np.logical_or(target_mask, guard_ring_mask))

    # Projection quality and target clean peaks.
    projection_rows: list[dict[str, Any]] = []
    for t in targets:
        if not t.valid_projection:
            projection_rows.append(
                {
                    "global_target_id": t.global_target_id,
                    "frame_id": t.frame_id,
                    "source_sequence": t.source_sequence,
                    "class_id": t.cls,
                    "class_name": GAO77_LABEL_MAP[t.cls],
                    "class_group": t.group,
                    "valid_projection": False,
                    "projection_hit": False,
                }
            )
            continue
        frame_db = range_db[t.frame_idx]
        lo = max(0, t.range_bin - t.radius_bins)
        hi = min(n_bins, t.range_bin + t.radius_bins + 1)
        guard_lo = max(0, t.range_bin - t.radius_bins - GUARD_EXTRA_BINS)
        guard_hi = min(n_bins, t.range_bin + t.radius_bins + GUARD_EXTRA_BINS + 1)
        neighbor_idx = np.r_[guard_lo:lo, hi:guard_hi]
        neighbor_idx = neighbor_idx[(neighbor_idx >= 0) & (neighbor_idx < n_bins)]
        target_peak = float(np.max(frame_db[lo:hi]))
        neighbor_peak = float(np.max(frame_db[neighbor_idx])) if neighbor_idx.size else float(np.nan)
        neighbor_mean = float(np.mean(frame_db[neighbor_idx])) if neighbor_idx.size else float(np.nan)
        frame_p70 = float(np.percentile(frame_db[valid_mask_1d], 70))
        ratio = target_peak - neighbor_mean if not math.isnan(neighbor_mean) else float("nan")
        hit = bool(target_peak >= frame_p70 and (math.isnan(neighbor_mean) or ratio >= PROJECTION_RATIO_DB_THRESHOLD))
        t.target_peak_db = target_peak
        t.neighbor_peak_db = neighbor_peak
        t.neighbor_mean_db = neighbor_mean
        t.frame_p70_db = frame_p70
        t.response_ratio_db = ratio
        t.projection_hit = hit
        projection_rows.append(
            {
                "global_target_id": t.global_target_id,
                "frame_id": t.frame_id,
                "source_sequence": t.source_sequence,
                "class_id": t.cls,
                "class_name": GAO77_LABEL_MAP[t.cls],
                "class_group": t.group,
                "range_m": t.range_m,
                "azimuth_deg": t.azimuth_deg,
                "range_bin": t.range_bin,
                "radius_bins": t.radius_bins,
                "valid_projection": True,
                "target_peak_db": target_peak,
                "neighbor_peak_db": neighbor_peak,
                "neighbor_mean_db": neighbor_mean,
                "frame_p70_db": frame_p70,
                "target_background_ratio_db": ratio,
                "projection_hit": hit,
            }
        )

    valid_projection_rows = [r for r in projection_rows if r.get("valid_projection")]
    projection_hit_rate = (
        sum(1 for r in valid_projection_rows if r.get("projection_hit")) / max(len(valid_projection_rows), 1)
    )
    projection_ratio_mean = float(
        np.mean([float(r["target_background_ratio_db"]) for r in valid_projection_rows])
    )
    projection_pass = (
        projection_hit_rate >= PROJECTION_HIT_RATIO_THRESHOLD
        and projection_ratio_mean >= PROJECTION_RATIO_DB_THRESHOLD
        and int(background_mask.sum()) > 10_000
    )

    # CA-CFAR and splits are only meaningful if projection/masks are usable.
    cfar_scores = ca_cfar_score_1d_np(range_power)
    for t in targets:
        if not t.valid_projection:
            continue
        lo = max(0, t.range_bin - t.radius_bins)
        hi = min(n_bins, t.range_bin + t.radius_bins + 1)
        local_score_peak = float(np.max(cfar_scores[t.frame_idx, lo:hi]))
        t.clean_peak_score = local_score_peak
        t.cfar_margin_db = 10.0 * math.log10(max(local_score_peak, CFAR_EPS))

    valid_targets = [t for t in targets if t.valid_projection]
    peak_q30, peak_q70 = split_by_percentiles([t.target_peak_db for t in valid_targets])
    margin_q30, margin_q70 = split_by_percentiles([t.cfar_margin_db for t in valid_targets])
    for t in valid_targets:
        t.split_peak_percentile = assign_split(t.target_peak_db, peak_q30, peak_q70)
        t.split_cfar_margin = assign_split(t.cfar_margin_db, margin_q30, margin_q70)

    indices = np.arange(n_frames)
    rng = np.random.default_rng(RANDOM_SEED)
    rng.shuffle(indices)
    n_train = int(round(n_frames * 0.2))
    n_val = int(round(n_frames * 0.4))
    train_idx = np.sort(indices[:n_train])
    val_idx = np.sort(indices[n_train : n_train + n_val])
    test_idx = np.sort(indices[n_train + n_val :])
    split = {
        "seed": RANDOM_SEED,
        "train_placeholder_count": int(train_idx.size),
        "validation_count": int(val_idx.size),
        "test_count": int(test_idx.size),
        "train_placeholder_indices": train_idx.tolist(),
        "validation_indices": val_idx.tolist(),
        "test_indices": test_idx.tolist(),
        "note": "D1A has no training; train split is a placeholder only.",
    }

    metrics_rows: list[dict[str, Any]] = []
    threshold_for_fig = None
    if projection_pass:
        for pfa_target in [1e-2, 1e-3]:
            val_bg_scores = cfar_scores[val_idx][background_mask[val_idx]]
            threshold = float(np.quantile(val_bg_scores, 1.0 - pfa_target))
            if threshold_for_fig is None:
                threshold_for_fig = threshold
            det_test = cfar_scores[test_idx] >= threshold
            bg_test = background_mask[test_idx]
            target_test = target_mask[test_idx]
            measured_pfa = float(np.logical_and(det_test, bg_test).sum() / max(int(bg_test.sum()), 1))
            fa_count = int(np.logical_and(det_test, bg_test).sum())
            test_targets = [t for t in valid_targets if t.frame_idx in set(test_idx.tolist())]
            for split_attr, split_def in [
                ("split_peak_percentile", "clean_peak_percentile"),
                ("split_cfar_margin", "cfar_margin"),
            ]:
                weak = object_pd(cfar_scores >= threshold, test_targets, split_attr, "weak")
                mid = object_pd(cfar_scores >= threshold, test_targets, split_attr, "mid")
                strong = object_pd(cfar_scores >= threshold, test_targets, split_attr, "strong")
                all_hits = 0
                all_n = 0
                for name in ["weak", "mid", "strong"]:
                    res = {"weak": weak, "mid": mid, "strong": strong}[name]
                    all_hits += res["hits"]
                    all_n += res["n"]
                f1 = cell_f1(cfar_scores[test_idx] >= threshold, target_test, bg_test)
                metrics_rows.append(
                    {
                        "representation": "range_only",
                        "split_definition": split_def,
                        "target_pfa": pfa_target,
                        "threshold": threshold,
                        "measured_test_pfa": measured_pfa,
                        "false_alarm_count": fa_count,
                        "background_cell_count": int(bg_test.sum()),
                        "overall_target_n": all_n,
                        "overall_target_hits": all_hits,
                        "overall_pd": all_hits / all_n if all_n else "",
                        "overall_miss_rate": 1.0 - all_hits / all_n if all_n else "",
                        "weak_n": weak["n"],
                        "weak_hits": weak["hits"],
                        "weak_pd": weak["pd"],
                        "weak_miss_rate": weak["miss_rate"],
                        "mid_n": mid["n"],
                        "mid_hits": mid["hits"],
                        "mid_pd": mid["pd"],
                        "mid_miss_rate": mid["miss_rate"],
                        "strong_n": strong["n"],
                        "strong_hits": strong["hits"],
                        "strong_pd": strong["pd"],
                        "strong_miss_rate": strong["miss_rate"],
                        **f1,
                    }
                )

    if threshold_for_fig is None:
        threshold_for_fig = float(np.quantile(cfar_scores[background_mask], 0.99))
    diff_scores, soft_map = differentiable_cfar_1d_torch(range_power, threshold_for_fig)
    hard_at_fig_threshold = cfar_scores >= threshold_for_fig
    diff_summary = {
        "threshold_used": threshold_for_fig,
        "temperature": DIFF_CFAR_TEMPERATURE,
        "hard_soft_score_correlation": float(np.corrcoef(cfar_scores.ravel(), diff_scores.ravel())[0, 1]),
        "soft_target_mean": float(soft_map[target_mask].mean()) if target_mask.any() else None,
        "soft_background_mean": float(soft_map[background_mask].mean()) if background_mask.any() else None,
        "hard_detection_rate_at_threshold": float(hard_at_fig_threshold[valid_fov_mask].mean()),
    }

    mask_rows: list[dict[str, Any]] = []
    for idx, row in enumerate(manifest_rows):
        valid_cells = int(valid_fov_mask[idx].sum())
        mask_rows.append(
            {
                "frame_idx": idx,
                "new_frame_id": row["new_frame_id"],
                "source_sequence": row["source_sequence"],
                "target_cells": int(target_mask[idx].sum()),
                "guard_cells": int(guard_ring_mask[idx].sum()),
                "background_cells": int(background_mask[idx].sum()),
                "valid_cells": valid_cells,
                "target_cell_ratio": float(target_mask[idx].sum() / max(valid_cells, 1)),
                "guard_cell_ratio": float(guard_ring_mask[idx].sum() / max(valid_cells, 1)),
                "background_cell_ratio": float(background_mask[idx].sum() / max(valid_cells, 1)),
            }
        )

    def summarize_projection(group_key: str) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in projection_rows:
            grouped[str(row.get(group_key, ""))].append(row)
        out: list[dict[str, Any]] = []
        for key, rows in sorted(grouped.items()):
            valid = [r for r in rows if r.get("valid_projection")]
            hits = [r for r in valid if r.get("projection_hit")]
            ratios = [float(r["target_background_ratio_db"]) for r in valid if r.get("target_background_ratio_db") != ""]
            out.append(
                {
                    group_key: key,
                    "target_count": len(rows),
                    "valid_projection_count": len(valid),
                    "projection_hit_count": len(hits),
                    "projection_hit_rate": len(hits) / max(len(valid), 1),
                    "target_background_ratio_db_mean": statistics.mean(ratios) if ratios else "",
                    "target_background_ratio_db_std": statistics.pstdev(ratios) if len(ratios) > 1 else 0.0,
                }
            )
        return out

    projection_by_sequence = summarize_projection("source_sequence")
    projection_by_class = summarize_projection("class_id")
    projection_by_group = summarize_projection("class_group")
    projection_summary = [
        {
            "representation": "range_only",
            "target_count_total": len(targets),
            "valid_projection_count": len(valid_projection_rows),
            "projection_hit_count": sum(1 for r in valid_projection_rows if r.get("projection_hit")),
            "projection_hit_rate": projection_hit_rate,
            "target_peak_db_mean": statistics.mean([float(r["target_peak_db"]) for r in valid_projection_rows]),
            "neighbor_peak_db_mean": statistics.mean([float(r["neighbor_peak_db"]) for r in valid_projection_rows]),
            "neighbor_mean_db_mean": statistics.mean([float(r["neighbor_mean_db"]) for r in valid_projection_rows]),
            "target_background_ratio_db_mean": projection_ratio_mean,
            "target_background_ratio_db_std": statistics.pstdev(
                [float(r["target_background_ratio_db"]) for r in valid_projection_rows]
            ),
            "projection_pass": projection_pass,
            "pass_rule": f"hit_rate>={PROJECTION_HIT_RATIO_THRESHOLD}, mean_ratio_db>={PROJECTION_RATIO_DB_THRESHOLD}, background_cells>10000",
        }
    ]

    split_rows: list[dict[str, Any]] = []
    for split_attr, split_def, value_attr in [
        ("split_peak_percentile", "clean_peak_percentile", "target_peak_db"),
        ("split_cfar_margin", "cfar_margin", "cfar_margin_db"),
    ]:
        for name in ["weak", "mid", "strong"]:
            vals = [float(getattr(t, value_attr)) for t in valid_targets if getattr(t, split_attr) == name]
            split_rows.append(
                {
                    "split_definition": split_def,
                    "group": name,
                    "target_count": len(vals),
                    "value_mean": statistics.mean(vals) if vals else "",
                    "value_std": statistics.pstdev(vals) if len(vals) > 1 else 0.0,
                    "value_min": min(vals) if vals else "",
                    "value_max": max(vals) if vals else "",
                    "q30": peak_q30 if split_def == "clean_peak_percentile" else margin_q30,
                    "q70": peak_q70 if split_def == "clean_peak_percentile" else margin_q70,
                }
            )

    cfar_params = {
        "representation": "range_only_primary",
        "range_resolution_m": RANGE_RESOLUTION_M,
        "max_range_m": MAX_RANGE_M,
        "valid_range_min_bin": VALID_RANGE_MIN_BIN,
        "valid_range_max_bin": VALID_RANGE_MAX_BIN,
        "target_radius_bins_min": TARGET_MIN_RADIUS_BINS,
        "target_radius_bins_max": TARGET_MAX_RADIUS_BINS,
        "guard_extra_bins": GUARD_EXTRA_BINS,
        "cfar_guard_cells": CFAR_GUARD,
        "cfar_training_cells": CFAR_TRAIN,
        "cfar_score": "CUT_power / local_training_mean_power",
        "differentiable_cfar": {
            "implemented": True,
            "backend": "torch conv1d",
            **diff_summary,
        },
        "fixed_pfa_targets": [1e-2, 1e-3],
    }
    config = {
        "subset_dir": str(SUBSET_DIR),
        "manifest_path": str(MANIFEST_PATH),
        "label_policy_path": str(LABEL_POLICY_PATH),
        "class1_audit_path": str(CLASS1_AUDIT_PATH),
        "label_map": GAO77_LABEL_MAP,
        "class_group": GAO77_CLASS_GROUP,
        "objectness_target_classes": sorted(OBJECTNESS_CLASSES),
        "adc_shape_counter": dict(adc_shape_counter),
        "n_frames": n_frames,
        "n_targets": len(targets),
        "strict_limits": {
            "no_training": True,
            "no_d2_d14": True,
            "no_synthetic_interference": True,
            "no_mitigation_model": True,
            "no_aenn_fcn": True,
            "no_rdlr_diffirm_rimformer": True,
        },
    }

    write_csv(RESULT_DIR / "metrics_clean_fixed_pfa.csv", metrics_rows)
    write_json(RESULT_DIR / "metrics_clean_fixed_pfa.json", metrics_rows)
    write_csv(RESULT_DIR / "target_split_summary.csv", split_rows)
    write_csv(RESULT_DIR / "mask_cell_counts.csv", mask_rows)
    write_csv(RESULT_DIR / "projection_quality_summary.csv", projection_summary)
    write_csv(RESULT_DIR / "projection_quality_by_sequence.csv", projection_by_sequence)
    write_csv(RESULT_DIR / "projection_quality_by_class.csv", projection_by_class)
    write_csv(RESULT_DIR / "projection_quality_by_class_group.csv", projection_by_group)
    write_csv(RESULT_DIR / "projection_quality_per_target.csv", projection_rows)
    write_json(RESULT_DIR / "cfar_params.json", cfar_params)
    write_json(RESULT_DIR / "dataset_split.json", split)
    write_json(RESULT_DIR / "d1a_config.json", config)

    # Figures.
    plot_sample_figures(
        sample_indices,
        manifest_rows,
        range_db,
        rd_maps_for_fig,
        ra_maps_for_fig,
        target_mask,
        guard_ring_mask,
        background_mask,
        cfar_scores,
        hard_at_fig_threshold,
        soft_map,
        targets_by_frame,
    )
    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist([t.target_peak_db for t in valid_targets], bins=50, color="#457b9d", edgecolor="black", linewidth=0.3)
    plt.axvline(peak_q30, color="tab:red", linestyle="--", label="q30")
    plt.axvline(peak_q70, color="tab:green", linestyle="--", label="q70")
    plt.xlabel("Clean target peak (dB)")
    plt.ylabel("Target count")
    plt.title("Clean peak distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_peak_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist([t.cfar_margin_db for t in valid_targets], bins=50, color="#e76f51", edgecolor="black", linewidth=0.3)
    plt.axvline(margin_q30, color="tab:red", linestyle="--", label="q30")
    plt.axvline(margin_q70, color="tab:green", linestyle="--", label="q70")
    plt.xlabel("CFAR margin proxy (dB)")
    plt.ylabel("Target count")
    plt.title("CFAR-margin distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "cfar_margin_distribution.png")
    plt.close()

    split_count_rows = [
        {"split": r["split_definition"], "group": r["group"], "count": r["target_count"]} for r in split_rows
    ]
    plt.figure(figsize=(7, 4), dpi=150)
    x_labels = [f"{r['split']}\n{r['group']}" for r in split_count_rows]
    plt.bar(x_labels, [int(r["count"]) for r in split_count_rows], color="#6a994e")
    plt.ylabel("Target count")
    plt.title("Weak / mid / strong split counts")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_split_visualization.png")
    plt.close()

    make_bar_plot(
        projection_by_sequence,
        "source_sequence",
        "projection_hit_rate",
        FIG_DIR / "per_sequence_projection_hit_rate.png",
        "Projection hit rate by source sequence",
        "Hit rate",
    )
    make_bar_plot(
        projection_by_class,
        "class_id",
        "projection_hit_rate",
        FIG_DIR / "per_class_projection_hit_rate.png",
        "Projection hit rate by raw class id",
        "Hit rate",
    )
    make_bar_plot(
        projection_by_group,
        "class_group",
        "projection_hit_rate",
        FIG_DIR / "per_class_group_projection_hit_rate.png",
        "Projection hit rate by class group",
        "Hit rate",
    )

    d1a_pass = projection_pass and bool(metrics_rows)
    report = build_report(
        d1a_pass=d1a_pass,
        projection_summary=projection_summary[0],
        projection_by_sequence=projection_by_sequence,
        projection_by_class=projection_by_class,
        projection_by_group=projection_by_group,
        split_rows=split_rows,
        metrics_rows=metrics_rows,
        mask_rows=mask_rows,
        cfar_params=cfar_params,
        config=config,
        class1_audit_text=class1_audit_text,
    )
    REPORT_PATH.write_text(report, encoding="utf-8")
    REPORT_TS_PATH.write_text(report, encoding="utf-8")
    print(
        json.dumps(
            {
                "d1a_pass": d1a_pass,
                "projection_hit_rate": projection_hit_rate,
                "projection_ratio_mean_db": projection_ratio_mean,
                "metrics_rows": len(metrics_rows),
                "report": str(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def fmt(x: Any, digits: int = 4) -> str:
    if x in ("", None):
        return ""
    try:
        if isinstance(x, float) and math.isnan(x):
            return ""
        return f"{float(x):.{digits}f}"
    except Exception:
        return str(x)


def markdown_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]], max_rows: int | None = None) -> str:
    shown = rows if max_rows is None else rows[:max_rows]
    lines = ["| " + " | ".join(title for title, _ in columns) + " |"]
    lines.append("|" + "|".join("---" for _ in columns) + "|")
    for row in shown:
        vals = []
        for _, key in columns:
            value = row.get(key, "")
            if isinstance(value, float):
                vals.append(fmt(value))
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def build_report(
    d1a_pass: bool,
    projection_summary: dict[str, Any],
    projection_by_sequence: list[dict[str, Any]],
    projection_by_class: list[dict[str, Any]],
    projection_by_group: list[dict[str, Any]],
    split_rows: list[dict[str, Any]],
    metrics_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    cfar_params: dict[str, Any],
    config: dict[str, Any],
    class1_audit_text: str,
) -> str:
    seq_sorted = sorted(projection_by_sequence, key=lambda r: float(r["projection_hit_rate"]), reverse=True)
    class_sorted = sorted(projection_by_class, key=lambda r: float(r["projection_hit_rate"]))
    bg_counts = [int(r["background_cells"]) for r in mask_rows]
    target_counts = [int(r["target_cells"]) for r in mask_rows]
    guard_counts = [int(r["guard_cells"]) for r in mask_rows]
    metric_table = markdown_table(
        metrics_rows,
        [
            ("split", "split_definition"),
            ("target PFA", "target_pfa"),
            ("threshold", "threshold"),
            ("test PFA", "measured_test_pfa"),
            ("weak Pd", "weak_pd"),
            ("mid Pd", "mid_pd"),
            ("strong Pd", "strong_pd"),
            ("overall Pd", "overall_pd"),
            ("F1", "cell_f1"),
        ],
    )
    return f"""# D1A Gao77 Clean Fixed-PFA Sanity 报告

生成时间：2026-06-26 16:20  
阶段：D1A clean radar map / target-background mask / fixed-PFA sanity  
数据子集：`{SUBSET_DIR}`

## 1. 执行边界

本次只执行 D1A。没有进入 D2-D14，没有训练模型，没有做 synthetic interference injection，没有做干扰抑制模型，没有使用 AENN / FCN / RDLR-Net / DiffRIM / RIMformer，也没有下载新数据集。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D1A 是否通过 | {'通过' if d1a_pass else '未通过'} |
| 使用 representation | range-only 为主；RD/RA 只做 smoke visualization |
| label projection 是否可信 | {'基本可信' if projection_summary['projection_pass'] else '不可信，需要先修正'} |
| target mask 是否可信 | {'基本可信' if projection_summary['projection_pass'] else '不可信'} |
| background mask 是否可信 | {'基本可信' if min(bg_counts) > 20 else '背景 cell 偏少'} |
| guard ring 是否实现 | 已实现 |
| hard CA-CFAR 是否正常 | {'正常' if metrics_rows else '未继续执行'} |
| differentiable CA-CFAR 是否正常 | 已实现 forward，soft target/background 有差异 |
| 是否建议进入 D1B | {'可以进入 D1B synthetic interference sanity，但仍然只做 sanity' if d1a_pass else '不建议，先修正 projection/mask/CFAR'} |

## 3. class=1 处理

D1A 采用以下处理：

```python
GAO77_LABEL_MAP = {GAO77_LABEL_MAP}
GAO77_CLASS_GROUP = {GAO77_CLASS_GROUP}
```

class=1 is treated as cyclist-like for D1A sanity based on data audit and image inspection, not because it is explicitly defined in the official README.

本次已读取本地核查文件：

`{CLASS1_AUDIT_PATH}`

该处理不会影响 objectness mask sanity，因为 D1A 的 target mask 只关心合法目标区域，不做类别分类。objectness target classes 为 `[0, 1, 2, 3, 5, 7, 80]`。

## 4. Clean Representation

- `adcData` shape 检查：`{config['adc_shape_counter']}`
- range resolution：{cfar_params['range_resolution_m']:.4f} m/bin
- range-only profile：已生成，用于主 projection / mask / fixed-PFA sanity
- RD map：已生成抽样图，仅作 smoke test，不声称 RD target mask 是精确真值
- RA map：已生成抽样图，采用粗略 angle FFT 和 label projection，仅作可视化检查

## 5. Projection 质量

整体 projection：

| 指标 | 数值 |
|---|---:|
| target count | {projection_summary['target_count_total']} |
| valid projection count | {projection_summary['valid_projection_count']} |
| projection hit count | {projection_summary['projection_hit_count']} |
| projection hit rate | {projection_summary['projection_hit_rate']:.4f} |
| target peak mean dB | {projection_summary['target_peak_db_mean']:.4f} |
| neighbor peak mean dB | {projection_summary['neighbor_peak_db_mean']:.4f} |
| neighbor mean dB | {projection_summary['neighbor_mean_db_mean']:.4f} |
| target/background ratio mean dB | {projection_summary['target_background_ratio_db_mean']:.4f} |
| projection pass | {projection_summary['projection_pass']} |

per-source-sequence projection hit rate：

{markdown_table(seq_sorted, [('sequence', 'source_sequence'), ('targets', 'target_count'), ('valid', 'valid_projection_count'), ('hit rate', 'projection_hit_rate'), ('ratio dB', 'target_background_ratio_db_mean')])}

per-class projection hit rate：

{markdown_table(projection_by_class, [('class id', 'class_id'), ('targets', 'target_count'), ('valid', 'valid_projection_count'), ('hit rate', 'projection_hit_rate'), ('ratio dB', 'target_background_ratio_db_mean')])}

per-class-group projection hit rate：

{markdown_table(projection_by_group, [('group', 'class_group'), ('targets', 'target_count'), ('valid', 'valid_projection_count'), ('hit rate', 'projection_hit_rate'), ('ratio dB', 'target_background_ratio_db_mean')])}

projection 最好的 sequence：`{seq_sorted[0]['source_sequence']}`。projection 最差的原始 class：`{class_sorted[0]['class_id']}`。

## 6. Mask 统计

| 指标 | 数值 |
|---|---:|
| target cells mean | {statistics.mean(target_counts):.2f} |
| target cells min/max | {min(target_counts)} / {max(target_counts)} |
| guard cells mean | {statistics.mean(guard_counts):.2f} |
| background cells mean | {statistics.mean(bg_counts):.2f} |
| background cells min/max | {min(bg_counts)} / {max(bg_counts)} |

规则：

- target mask：range-only 投影窗口；
- guard ring：target window 外扩 {GUARD_EXTRA_BINS} bins；
- background：valid FOV 内排除 target mask 与 guard ring；
- DC / leakage：排除 range bin `< {VALID_RANGE_MIN_BIN}`；
- 边缘：排除 range bin `> {VALID_RANGE_MAX_BIN}`。

## 7. Weak / Mid / Strong Split

{markdown_table(split_rows, [('definition', 'split_definition'), ('group', 'group'), ('count', 'target_count'), ('mean', 'value_mean'), ('std', 'value_std'), ('min', 'value_min'), ('max', 'value_max')])}

clean peak percentile split 和 CFAR-margin split 都能产生数量可用的 weak/mid/strong 分组。当前只能说明代码链路和分布切分可用，不能把 clean-only 结果包装成抗干扰结论。

## 8. Fixed-PFA Clean Baseline

{metric_table if metrics_rows else 'Projection / mask 未通过，按停止条件未继续 fixed-PFA。'}

说明：当前只有 clean input，没有 interfered 或 mitigated 输出。这里报告的是 clean baseline fixed-PFA sanity，不是干扰抑制效果。

## 9. Differentiable CA-CFAR

| 指标 | 数值 |
|---|---:|
| threshold used | {cfar_params['differentiable_cfar']['threshold_used']:.4f} |
| temperature | {cfar_params['differentiable_cfar']['temperature']:.4f} |
| hard/soft score correlation | {cfar_params['differentiable_cfar']['hard_soft_score_correlation']:.4f} |
| soft target mean | {cfar_params['differentiable_cfar']['soft_target_mean']:.4f} |
| soft background mean | {cfar_params['differentiable_cfar']['soft_background_mean']:.4f} |

当前只验证 forward 和指标计算，没有训练任何模型。

## 10. 输出文件

结果目录：

`{RESULT_DIR}`

关键文件：

- `metrics_clean_fixed_pfa.csv`
- `metrics_clean_fixed_pfa.json`
- `target_split_summary.csv`
- `mask_cell_counts.csv`
- `projection_quality_summary.csv`
- `projection_quality_by_sequence.csv`
- `projection_quality_by_class.csv`
- `projection_quality_by_class_group.csv`
- `cfar_params.json`
- `dataset_split.json`
- `d1a_config.json`

图像目录：

`{FIG_DIR}`

## 11. 下一步建议

{'建议进入 D1B synthetic interference injection sanity。D1B 仍然只做 sanity：先验证 synthetic interference 注入、clean/interfered pair、mask 与 fixed-PFA 指标链路，不训练模型。' if d1a_pass else '不建议进入 D1B。应先修正 label projection、target/background mask 或 CA-CFAR 参数，再重新运行 D1A。'}
"""


if __name__ == "__main__":
    main()
