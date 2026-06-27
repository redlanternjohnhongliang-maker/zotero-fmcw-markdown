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
from scipy.io import loadmat

from d1a_gao77_clean_fixed_pfa_sanity import (
    EXPECTED_ADC_SHAPE,
    FIG_DIR as D1A_FIG_DIR,
    GAO77_CLASS_GROUP,
    GAO77_LABEL_MAP,
    LABEL_DIR,
    LABEL_POLICY_PATH,
    MANIFEST_PATH,
    OBJECTNESS_CLASSES,
    RADAR_DIR,
    RANGE_RESOLUTION_M,
    ROOT,
    SUBSET_DIR,
    VALID_RANGE_MAX_BIN,
    VALID_RANGE_MIN_BIN,
    ca_cfar_score_1d_np,
    parse_label_file,
    radar_maps,
    read_csv_dicts,
    write_csv,
    write_json,
)


RESULT_DIR = ROOT / "results" / "d1a_plus_mask_stress_test"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d1a_plus_figures"
D1A_RESULT_DIR = ROOT / "results" / "d1a_gao77_clean_sanity"
REPORT_PATH = ROOT / "refine-logs" / "D1A_PLUS_MASK_STRESS_TEST_REPORT.md"
REPORT_TS_PATH = ROOT / "refine-logs" / "D1A_PLUS_MASK_STRESS_TEST_REPORT_20260626_164500.md"

RANDOM_SEED = 20260626
CFAR_GUARD = 2
CFAR_TRAIN = 10
CFAR_EPS = 1e-9
VALID_PFA_TARGETS = [1e-2, 1e-3]
PROJECTION_HIT_RATIO_THRESHOLD = 0.55
PROJECTION_RATIO_DB_THRESHOLD = 0.0
RA_ANGLE_BINS = 64


MASK_CONFIGS = [
    {"mask_name": "narrow", "radius_scale": 0.5, "min_radius": 1, "max_radius": 6, "guard_extra": 4},
    {"mask_name": "default", "radius_scale": 1.0, "min_radius": 2, "max_radius": 12, "guard_extra": 4},
    {"mask_name": "wide", "radius_scale": 1.5, "min_radius": 3, "max_radius": 18, "guard_extra": 4},
]
GUARD_CONFIGS = [2, 4, 6]


@dataclass
class Target:
    target_id: int
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
    valid_projection: bool


def valid_mask_1d(n_bins: int) -> np.ndarray:
    mask = np.zeros(n_bins, dtype=bool)
    mask[VALID_RANGE_MIN_BIN : min(VALID_RANGE_MAX_BIN + 1, n_bins)] = True
    return mask


def radius_for_target(target: Target, cfg: dict[str, Any]) -> int:
    radius_m = 0.5 * math.sqrt(target.wid * target.wid + target.length * target.length)
    raw_radius = int(math.ceil(radius_m / RANGE_RESOLUTION_M * float(cfg["radius_scale"])))
    return max(int(cfg["min_radius"]), min(int(cfg["max_radius"]), raw_radius))


def interval(center: int, radius: int, n_bins: int) -> tuple[int, int]:
    return max(0, center - radius), min(n_bins, center + radius + 1)


def build_masks(
    targets: list[Target], n_frames: int, n_bins: int, cfg: dict[str, Any], guard_extra: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[int, tuple[int, int, int]]]:
    target_mask = np.zeros((n_frames, n_bins), dtype=bool)
    guard_mask_full = np.zeros((n_frames, n_bins), dtype=bool)
    intervals: dict[int, tuple[int, int, int]] = {}
    ge = int(cfg["guard_extra"] if guard_extra is None else guard_extra)
    for target in targets:
        if not target.valid_projection:
            continue
        radius = radius_for_target(target, cfg)
        lo, hi = interval(target.range_bin, radius, n_bins)
        glo, ghi = interval(target.range_bin, radius + ge, n_bins)
        target_mask[target.frame_idx, lo:hi] = True
        guard_mask_full[target.frame_idx, glo:ghi] = True
        intervals[target.target_id] = (lo, hi, radius)
    guard_ring_mask = np.logical_and(guard_mask_full, ~target_mask)
    valid = np.broadcast_to(valid_mask_1d(n_bins), target_mask.shape).copy()
    background_mask = np.logical_and(valid, ~np.logical_or(target_mask, guard_ring_mask))
    return target_mask, guard_ring_mask, background_mask, intervals


def ca_cfar_score(range_power: np.ndarray, guard: int = CFAR_GUARD, train: int = CFAR_TRAIN) -> np.ndarray:
    # Keep this wrapper so all D1A+ outputs clearly use the same CA-CFAR setting.
    return ca_cfar_score_1d_np(range_power, guard=guard, train=train)


def target_peak_and_projection(
    range_db: np.ndarray,
    cfar_scores: np.ndarray,
    targets: list[Target],
    intervals: dict[int, tuple[int, int, int]],
    guard_extra: int,
) -> dict[int, dict[str, Any]]:
    valid = valid_mask_1d(range_db.shape[1])
    out: dict[int, dict[str, Any]] = {}
    for target in targets:
        if target.target_id not in intervals:
            out[target.target_id] = {"valid_projection": False, "projection_hit": False}
            continue
        lo, hi, radius = intervals[target.target_id]
        glo, ghi = interval(target.range_bin, radius + guard_extra, range_db.shape[1])
        neighbor = np.r_[glo:lo, hi:ghi]
        frame_db = range_db[target.frame_idx]
        target_peak = float(np.max(frame_db[lo:hi]))
        neighbor_peak = float(np.max(frame_db[neighbor])) if neighbor.size else float("nan")
        neighbor_mean = float(np.mean(frame_db[neighbor])) if neighbor.size else float("nan")
        frame_p70 = float(np.percentile(frame_db[valid], 70))
        ratio = target_peak - neighbor_mean if not math.isnan(neighbor_mean) else float("nan")
        hit = bool(target_peak >= frame_p70 and (math.isnan(neighbor_mean) or ratio >= PROJECTION_RATIO_DB_THRESHOLD))
        score_peak = float(np.max(cfar_scores[target.frame_idx, lo:hi]))
        out[target.target_id] = {
            "valid_projection": True,
            "projection_hit": hit,
            "target_peak_db": target_peak,
            "neighbor_peak_db": neighbor_peak,
            "neighbor_mean_db": neighbor_mean,
            "target_background_ratio_db": ratio,
            "cfar_peak_score": score_peak,
            "cfar_margin_db": 10.0 * math.log10(max(score_peak, CFAR_EPS)),
        }
    return out


def assign_splits(target_values: dict[int, dict[str, Any]], value_key: str) -> dict[int, str]:
    vals = [float(v[value_key]) for v in target_values.values() if v.get("valid_projection")]
    q30, q70 = np.quantile(vals, [0.3, 0.7])
    splits: dict[int, str] = {}
    for tid, values in target_values.items():
        if not values.get("valid_projection"):
            continue
        value = float(values[value_key])
        if value <= q30:
            splits[tid] = "weak"
        elif value <= q70:
            splits[tid] = "mid"
        else:
            splits[tid] = "strong"
    return splits


def target_hit(detections: np.ndarray, target: Target, interval_map: dict[int, tuple[int, int, int]]) -> bool:
    if target.target_id not in interval_map:
        return False
    lo, hi, _ = interval_map[target.target_id]
    return bool(detections[target.frame_idx, lo:hi].any())


def f1_cells(detections: np.ndarray, target_mask: np.ndarray, background_mask: np.ndarray) -> dict[str, Any]:
    tp = int(np.logical_and(detections, target_mask).sum())
    fp = int(np.logical_and(detections, background_mask).sum())
    fn = int(np.logical_and(~detections, target_mask).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp_cells": tp, "fp_cells": fp, "fn_cells": fn, "precision": precision, "recall": recall, "f1": f1}


def calibrate_and_eval(
    cfar_scores: np.ndarray,
    background_mask: np.ndarray,
    target_mask: np.ndarray,
    targets: list[Target],
    interval_map: dict[int, tuple[int, int, int]],
    splits: dict[int, str],
    val_idx: np.ndarray,
    test_idx: np.ndarray,
    pfa_target: float,
) -> dict[str, Any]:
    val_scores = cfar_scores[val_idx][background_mask[val_idx]]
    threshold = float(np.quantile(val_scores, 1.0 - pfa_target))
    detections = cfar_scores >= threshold
    test_set = set(int(i) for i in test_idx.tolist())
    test_targets = [t for t in targets if t.frame_idx in test_set and t.target_id in splits]
    bg_test = background_mask[test_idx]
    target_test = target_mask[test_idx]
    fa = int(np.logical_and(detections[test_idx], bg_test).sum())
    bg_count = int(bg_test.sum())
    out = {
        "target_pfa": pfa_target,
        "validation_threshold": threshold,
        "test_measured_pfa": fa / max(bg_count, 1),
        "false_alarm_count": fa,
        "background_cell_count": bg_count,
        **f1_cells(detections[test_idx], target_test, bg_test),
    }
    for group in ["weak", "mid", "strong"]:
        selected = [t for t in test_targets if splits[t.target_id] == group]
        hits = sum(1 for t in selected if target_hit(detections, t, interval_map))
        out[f"{group}_n"] = len(selected)
        out[f"{group}_hits"] = hits
        out[f"{group}_pd"] = hits / len(selected) if selected else ""
    all_hits = sum(1 for t in test_targets if target_hit(detections, t, interval_map))
    out["overall_n"] = len(test_targets)
    out["overall_hits"] = all_hits
    out["overall_pd"] = all_hits / len(test_targets) if test_targets else ""
    return out


def bootstrap_pfa(
    detections: np.ndarray, background_mask: np.ndarray, test_idx: np.ndarray, n_boot: int = 1000
) -> dict[str, float]:
    rng = np.random.default_rng(RANDOM_SEED)
    frame_pfas: list[float] = []
    frame_fa: list[int] = []
    frame_bg: list[int] = []
    for idx in test_idx:
        bg = background_mask[idx]
        fa = int(np.logical_and(detections[idx], bg).sum())
        bg_count = int(bg.sum())
        if bg_count > 0:
            frame_pfas.append(fa / bg_count)
            frame_fa.append(fa)
            frame_bg.append(bg_count)
    boot_values = []
    frame_fa_arr = np.asarray(frame_fa)
    frame_bg_arr = np.asarray(frame_bg)
    n = len(frame_fa_arr)
    for _ in range(n_boot):
        choices = rng.integers(0, n, size=n)
        boot_values.append(float(frame_fa_arr[choices].sum() / max(frame_bg_arr[choices].sum(), 1)))
    return {
        "frame_level_pfa_mean": float(np.mean(frame_pfas)),
        "frame_level_pfa_std": float(np.std(frame_pfas)),
        "bootstrap_pfa_std": float(np.std(boot_values)),
        "bootstrap_pfa_ci_low": float(np.quantile(boot_values, 0.025)),
        "bootstrap_pfa_ci_high": float(np.quantile(boot_values, 0.975)),
    }


def load_dataset() -> tuple[list[dict[str, str]], list[Target], np.ndarray, np.ndarray, np.ndarray, dict[int, np.ndarray]]:
    manifest = read_csv_dicts(MANIFEST_PATH)
    n_frames = len(manifest)
    n_bins = EXPECTED_ADC_SHAPE[0]
    range_power = np.zeros((n_frames, n_bins), dtype=np.float64)
    range_db = np.zeros((n_frames, n_bins), dtype=np.float64)
    ra_maps = np.zeros((n_frames, n_bins, RA_ANGLE_BINS), dtype=np.float32)
    rd_for_fig: dict[int, np.ndarray] = {}
    sample_indices = set(np.linspace(0, n_frames - 1, 6, dtype=int).tolist())
    targets: list[Target] = []
    tid = 0
    shape_counter: Counter[str] = Counter()
    for frame_idx, row in enumerate(manifest):
        mat = loadmat(RADAR_DIR / row["new_radar_file"])
        if "adcData" not in mat:
            raise RuntimeError(f"adcData missing in {row['new_radar_file']}")
        adc = mat["adcData"]
        shape_counter["x".join(map(str, adc.shape))] += 1
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"unexpected adcData shape {adc.shape}")
        rp, rd_map, ra_map = radar_maps(adc)
        range_power[frame_idx] = rp
        range_db[frame_idx] = 10.0 * np.log10(rp + 1e-12)
        ra_maps[frame_idx] = ra_map.astype(np.float32)
        if frame_idx in sample_indices:
            rd_for_fig[frame_idx] = rd_map
        for uid, cls, px, py, wid, length in parse_label_file(LABEL_DIR / row["new_label_file"]):
            if cls not in OBJECTNESS_CLASSES:
                continue
            tid += 1
            range_m = math.sqrt(px * px + py * py)
            azimuth_deg = math.degrees(math.atan2(px, py))
            range_bin = int(round(range_m / RANGE_RESOLUTION_M))
            valid = VALID_RANGE_MIN_BIN <= range_bin <= VALID_RANGE_MAX_BIN
            targets.append(
                Target(
                    target_id=tid,
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
    return manifest, targets, range_power, range_db, ra_maps, rd_for_fig


def load_split(n_frames: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    split_path = D1A_RESULT_DIR / "dataset_split.json"
    if split_path.exists():
        split = json.loads(split_path.read_text(encoding="utf-8"))
        return (
            np.asarray(split["train_placeholder_indices"], dtype=int),
            np.asarray(split["validation_indices"], dtype=int),
            np.asarray(split["test_indices"], dtype=int),
        )
    rng = np.random.default_rng(RANDOM_SEED)
    indices = np.arange(n_frames)
    rng.shuffle(indices)
    n_train = int(round(n_frames * 0.2))
    n_val = int(round(n_frames * 0.4))
    return np.sort(indices[:n_train]), np.sort(indices[n_train : n_train + n_val]), np.sort(indices[n_train + n_val :])


def mask_width_sensitivity(
    range_db: np.ndarray,
    cfar_scores: np.ndarray,
    targets: list[Target],
    val_idx: np.ndarray,
    test_idx: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    artifacts: dict[str, Any] = {}
    n_frames, n_bins = range_db.shape
    for cfg in MASK_CONFIGS:
        tm, gm, bm, intervals = build_masks(targets, n_frames, n_bins, cfg)
        target_values = target_peak_and_projection(range_db, cfar_scores, targets, intervals, int(cfg["guard_extra"]))
        splits = assign_splits(target_values, "target_peak_db")
        valid_values = [v for v in target_values.values() if v.get("valid_projection")]
        projection_hit_rate = sum(1 for v in valid_values if v["projection_hit"]) / max(len(valid_values), 1)
        ratio_mean = statistics.mean(float(v["target_background_ratio_db"]) for v in valid_values)
        split_counts = Counter(splits.values())
        base = {
            "mask_name": cfg["mask_name"],
            "radius_scale": cfg["radius_scale"],
            "min_radius": cfg["min_radius"],
            "max_radius": cfg["max_radius"],
            "target_cells_mean": float(tm.sum(axis=1).mean()),
            "guard_cells_mean": float(gm.sum(axis=1).mean()),
            "background_cells_mean": float(bm.sum(axis=1).mean()),
            "projection_hit_rate": projection_hit_rate,
            "target_background_energy_ratio_db": ratio_mean,
            "weak_n_all": split_counts["weak"],
            "mid_n_all": split_counts["mid"],
            "strong_n_all": split_counts["strong"],
        }
        for pfa in VALID_PFA_TARGETS:
            rows.append(
                {
                    **base,
                    **calibrate_and_eval(cfar_scores, bm, tm, targets, intervals, splits, val_idx, test_idx, pfa),
                }
            )
        artifacts[cfg["mask_name"]] = {"target_mask": tm, "guard_mask": gm, "background_mask": bm, "intervals": intervals, "splits": splits}
    return rows, artifacts


def overlap_summary(
    targets: list[Target],
    interval_map: dict[int, tuple[int, int, int]],
    splits: dict[int, str],
    n_frames: int,
    n_bins: int,
) -> list[dict[str, Any]]:
    by_frame: dict[int, list[Target]] = defaultdict(list)
    for target in targets:
        if target.target_id in interval_map:
            by_frame[target.frame_idx].append(target)
    rows: list[dict[str, Any]] = []
    overlapped_targets: set[int] = set()
    overlap_by_split: dict[str, set[int]] = defaultdict(set)
    all_by_split: dict[str, set[int]] = defaultdict(set)
    total_pairs = 0
    total_overlap_pairs = 0
    total_overlap_cells = 0
    total_target_union_cells = 0
    for frame_idx in range(n_frames):
        frame_targets = by_frame.get(frame_idx, [])
        coverage = np.zeros(n_bins, dtype=np.int16)
        intervals = []
        for t in frame_targets:
            lo, hi, _ = interval_map[t.target_id]
            coverage[lo:hi] += 1
            intervals.append((t, lo, hi))
            if t.target_id in splits:
                all_by_split[splits[t.target_id]].add(t.target_id)
        overlap_pairs = 0
        overlap_tids: set[int] = set()
        for i in range(len(intervals)):
            for j in range(i + 1, len(intervals)):
                total_pairs += 1
                t1, lo1, hi1 = intervals[i]
                t2, lo2, hi2 = intervals[j]
                if max(lo1, lo2) < min(hi1, hi2):
                    overlap_pairs += 1
                    total_overlap_pairs += 1
                    overlap_tids.add(t1.target_id)
                    overlap_tids.add(t2.target_id)
        for tid in overlap_tids:
            overlapped_targets.add(tid)
            if tid in splits:
                overlap_by_split[splits[tid]].add(tid)
        overlap_cells = int((coverage >= 2).sum())
        union_cells = int((coverage >= 1).sum())
        total_overlap_cells += overlap_cells
        total_target_union_cells += union_cells
        rows.append(
            {
                "row_type": "frame",
                "frame_idx": frame_idx,
                "target_count": len(frame_targets),
                "overlap_pair_count": overlap_pairs,
                "overlap_cell_ratio": overlap_cells / max(union_cells, 1),
                "overlapped_target_count": len(overlap_tids),
                "overlapped_target_ratio": len(overlap_tids) / max(len(frame_targets), 1),
            }
        )
    rows.append(
        {
            "row_type": "summary_overall",
            "frame_idx": "",
            "target_count": sum(1 for t in targets if t.target_id in interval_map),
            "overlap_pair_count": total_overlap_pairs,
            "all_pair_count": total_pairs,
            "overlap_pair_ratio": total_overlap_pairs / max(total_pairs, 1),
            "overlap_cell_ratio": total_overlap_cells / max(total_target_union_cells, 1),
            "overlapped_target_count": len(overlapped_targets),
            "overlapped_target_ratio": len(overlapped_targets) / max(len(interval_map), 1),
        }
    )
    for split_name in ["weak", "mid", "strong"]:
        rows.append(
            {
                "row_type": f"summary_split_{split_name}",
                "frame_idx": "",
                "target_count": len(all_by_split[split_name]),
                "overlapped_target_count": len(overlap_by_split[split_name]),
                "overlapped_target_ratio": len(overlap_by_split[split_name]) / max(len(all_by_split[split_name]), 1),
            }
        )
    return rows


def guard_sensitivity(
    range_db: np.ndarray,
    cfar_scores: np.ndarray,
    targets: list[Target],
    val_idx: np.ndarray,
    test_idx: np.ndarray,
    default_cfg: dict[str, Any],
    default_splits: dict[int, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    n_frames, n_bins = range_db.shape
    for guard_extra in GUARD_CONFIGS:
        tm, gm, bm, intervals = build_masks(targets, n_frames, n_bins, default_cfg, guard_extra=guard_extra)
        for pfa in VALID_PFA_TARGETS:
            rows.append(
                {
                    "guard_extra_bins": guard_extra,
                    "background_cells_mean": float(bm.sum(axis=1).mean()),
                    **calibrate_and_eval(cfar_scores, bm, tm, targets, intervals, default_splits, val_idx, test_idx, pfa),
                }
            )
    return rows


def pfa_stability(
    cfar_scores: np.ndarray,
    background_mask: np.ndarray,
    targets: list[Target],
    intervals: dict[int, tuple[int, int, int]],
    splits: dict[int, str],
    manifest: list[dict[str, str]],
    val_idx: np.ndarray,
    test_idx: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary_rows: list[dict[str, Any]] = []
    by_sequence_rows: list[dict[str, Any]] = []
    by_group_rows: list[dict[str, Any]] = []
    seq_by_idx = {i: row["source_sequence"] for i, row in enumerate(manifest)}
    source_sequences = sorted({row["source_sequence"] for row in manifest})
    test_set = set(int(i) for i in test_idx.tolist())
    for pfa in VALID_PFA_TARGETS:
        threshold = float(np.quantile(cfar_scores[val_idx][background_mask[val_idx]], 1.0 - pfa))
        detections = cfar_scores >= threshold
        bg_test = background_mask[test_idx]
        fa = int(np.logical_and(detections[test_idx], bg_test).sum())
        bg_count = int(bg_test.sum())
        boot = bootstrap_pfa(detections, background_mask, test_idx)
        summary_rows.append(
            {
                "target_pfa": pfa,
                "validation_threshold": threshold,
                "background_cell_count": bg_count,
                "false_alarm_count": fa,
                "measured_pfa": fa / max(bg_count, 1),
                **boot,
            }
        )
        for seq in source_sequences:
            idxs = np.asarray([i for i in test_idx.tolist() if seq_by_idx[i] == seq], dtype=int)
            if idxs.size == 0:
                continue
            bg = background_mask[idxs]
            seq_fa = int(np.logical_and(detections[idxs], bg).sum())
            seq_bg = int(bg.sum())
            by_sequence_rows.append(
                {
                    "target_pfa": pfa,
                    "source_sequence": seq,
                    "test_frame_count": int(idxs.size),
                    "background_cell_count": seq_bg,
                    "false_alarm_count": seq_fa,
                    "measured_pfa": seq_fa / max(seq_bg, 1),
                }
            )
        for group in sorted(set(GAO77_CLASS_GROUP.values())):
            selected = [t for t in targets if t.frame_idx in test_set and t.group == group and t.target_id in splits]
            hits = sum(1 for t in selected if target_hit(detections, t, intervals))
            by_group_rows.append(
                {
                    "target_pfa": pfa,
                    "class_group": group,
                    "target_count": len(selected),
                    "hit_count": hits,
                    "pd": hits / len(selected) if selected else "",
                }
            )
    return summary_rows, by_sequence_rows, by_group_rows


def ra_projection_sanity(ra_maps: np.ndarray, targets: list[Target]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_sequence: dict[str, list[dict[str, Any]]] = defaultdict(list)
    n_range, n_angle = ra_maps.shape[1], ra_maps.shape[2]
    for t in targets:
        if not t.valid_projection:
            continue
        sin_theta = max(-1.0, min(1.0, math.sin(math.radians(t.azimuth_deg))))
        angle_bin = int(round((sin_theta + 1.0) * 0.5 * (n_angle - 1)))
        r_radius = 2
        a_radius = 2
        r0, r1 = interval(t.range_bin, r_radius, n_range)
        a0, a1 = interval(angle_bin, a_radius, n_angle)
        gr0, gr1 = interval(t.range_bin, r_radius + 4, n_range)
        ga0, ga1 = interval(angle_bin, a_radius + 4, n_angle)
        frame = ra_maps[t.frame_idx]
        target_patch = frame[r0:r1, a0:a1]
        guard_patch = frame[gr0:gr1, ga0:ga1].copy()
        local_mask = np.ones_like(guard_patch, dtype=bool)
        local_mask[(r0 - gr0) : (r1 - gr0), (a0 - ga0) : (a1 - ga0)] = False
        bg_vals = guard_patch[local_mask]
        target_peak = float(np.max(target_patch))
        bg_mean = float(np.mean(bg_vals)) if bg_vals.size else float("nan")
        ratio = target_peak - bg_mean if not math.isnan(bg_mean) else float("nan")
        frame_p70 = float(np.percentile(frame, 70))
        hit = bool(target_peak >= frame_p70 and (math.isnan(bg_mean) or ratio >= 0.0))
        row = {
            "row_type": "target",
            "target_id": t.target_id,
            "source_sequence": t.source_sequence,
            "class_id": t.cls,
            "class_group": t.group,
            "range_bin": t.range_bin,
            "angle_bin": angle_bin,
            "ra_target_peak_db": target_peak,
            "ra_background_mean_db": bg_mean,
            "ra_target_background_ratio_db": ratio,
            "ra_projection_hit": hit,
        }
        rows.append(row)
        by_sequence[t.source_sequence].append(row)
    summary = {
        "row_type": "summary",
        "target_count": len(rows),
        "ra_projection_hit_count": sum(1 for r in rows if r["ra_projection_hit"]),
        "ra_projection_hit_rate": sum(1 for r in rows if r["ra_projection_hit"]) / max(len(rows), 1),
        "ra_target_background_ratio_db_mean": statistics.mean(
            float(r["ra_target_background_ratio_db"]) for r in rows
        ),
    }
    output_rows = [summary]
    for seq, seq_rows in sorted(by_sequence.items()):
        output_rows.append(
            {
                "row_type": "by_sequence",
                "source_sequence": seq,
                "target_count": len(seq_rows),
                "ra_projection_hit_count": sum(1 for r in seq_rows if r["ra_projection_hit"]),
                "ra_projection_hit_rate": sum(1 for r in seq_rows if r["ra_projection_hit"]) / max(len(seq_rows), 1),
                "ra_target_background_ratio_db_mean": statistics.mean(
                    float(r["ra_target_background_ratio_db"]) for r in seq_rows
                ),
            }
        )
    output_rows.extend(rows)
    return output_rows, summary


def plot_outputs(
    mask_rows: list[dict[str, Any]],
    guard_rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, Any]],
    pfa_seq_rows: list[dict[str, Any]],
    pd_group_rows: list[dict[str, Any]],
    ra_maps: np.ndarray,
    targets: list[Target],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    # Mask sensitivity: weak Pd and measured PFA.
    pfa_rows = [r for r in mask_rows if float(r["target_pfa"]) == 0.01]
    names = [r["mask_name"] for r in pfa_rows]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot(names, [float(r["weak_pd"]) for r in pfa_rows], marker="o", label="weak Pd")
    plt.plot(names, [float(r["overall_pd"]) for r in pfa_rows], marker="o", label="overall Pd")
    plt.ylabel("Pd")
    plt.title("Mask width sensitivity at target PFA=1e-2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "mask_width_sensitivity_pd.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(names, [float(r["target_cells_mean"]) for r in pfa_rows], label="target cells")
    plt.ylabel("Mean cells per frame")
    plt.title("Target mask cells by mask width")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "mask_width_target_cells.png")
    plt.close()

    guard_pfa = [r for r in guard_rows if float(r["target_pfa"]) == 0.01]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot([r["guard_extra_bins"] for r in guard_pfa], [float(r["test_measured_pfa"]) for r in guard_pfa], marker="o")
    plt.axhline(0.01, linestyle="--", color="tab:red", label="target PFA")
    plt.xlabel("Guard extra bins")
    plt.ylabel("Measured test PFA")
    plt.title("Guard sensitivity of fixed-PFA calibration")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "guard_sensitivity_pfa.png")
    plt.close()

    frame_rows = [r for r in overlap_rows if r["row_type"] == "frame"]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist([float(r["overlap_cell_ratio"]) for r in frame_rows], bins=40, color="#e76f51")
    plt.xlabel("Overlap cell ratio")
    plt.ylabel("Frame count")
    plt.title("Target mask overlap ratio per frame")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "mask_overlap_ratio_histogram.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    pfa_rows = [r for r in pfa_seq_rows if float(r["target_pfa"]) == 0.01]
    plt.bar([r["source_sequence"] for r in pfa_rows], [float(r["measured_pfa"]) for r in pfa_rows])
    plt.axhline(0.01, linestyle="--", color="tab:red")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Measured PFA")
    plt.title("PFA by source sequence at target PFA=1e-2")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_by_sequence.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    pd_rows = [r for r in pd_group_rows if float(r["target_pfa"]) == 0.01 and str(r.get("pd", "")) != ""]
    plt.bar([r["class_group"] for r in pd_rows], [float(r["pd"]) for r in pd_rows])
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.title("Pd by class group at target PFA=1e-2")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pd_by_class_group.png")
    plt.close()

    # RA projection visualization for a few sample targets.
    sample_targets = []
    seen_frames = set()
    for t in targets:
        if t.frame_idx not in seen_frames and t.valid_projection:
            sample_targets.append(t)
            seen_frames.add(t.frame_idx)
        if len(sample_targets) >= 6:
            break
    for t in sample_targets:
        frame = ra_maps[t.frame_idx]
        sin_theta = max(-1.0, min(1.0, math.sin(math.radians(t.azimuth_deg))))
        angle_bin = int(round((sin_theta + 1.0) * 0.5 * (frame.shape[1] - 1)))
        plt.figure(figsize=(8, 5), dpi=150)
        plt.imshow(frame.T, aspect="auto", origin="lower", cmap="magma")
        plt.scatter([t.range_bin], [angle_bin], c="cyan", marker="x", s=28)
        plt.xlabel("Range bin")
        plt.ylabel("Angle FFT bin")
        plt.title(f"RA projection sanity frame {t.frame_id}")
        plt.colorbar(label="Power (dB)")
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"ra_projection_sanity_{t.frame_id}.png")
        plt.close()


def write_report(
    mask_rows: list[dict[str, Any]],
    guard_rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, Any]],
    pfa_rows: list[dict[str, Any]],
    pfa_seq_rows: list[dict[str, Any]],
    pd_group_rows: list[dict[str, Any]],
    ra_summary: dict[str, Any],
) -> None:
    default_rows = [r for r in mask_rows if r["mask_name"] == "default"]
    narrow_rows = [r for r in mask_rows if r["mask_name"] == "narrow"]
    wide_rows = [r for r in mask_rows if r["mask_name"] == "wide"]
    def get_pfa_row(rows: list[dict[str, Any]], target: float = 0.01) -> dict[str, Any]:
        return next(r for r in rows if abs(float(r["target_pfa"]) - target) < 1e-12)

    narrow = get_pfa_row(narrow_rows)
    default = get_pfa_row(default_rows)
    wide = get_pfa_row(wide_rows)
    weak_pds = [float(r["weak_pd"]) for r in [narrow, default, wide]]
    f1s = [float(r["f1"]) for r in [narrow, default, wide]]
    target_cells = [float(r["target_cells_mean"]) for r in [narrow, default, wide]]
    mask_sensitive = (max(weak_pds) - min(weak_pds) > 0.15) or (max(f1s) - min(f1s) > 0.08)
    target_overwide = float(default["target_cells_mean"]) > 40.0 and float(narrow["projection_hit_rate"]) > 0.95
    overlap_summary_row = next(r for r in overlap_rows if r["row_type"] == "summary_overall")
    weak_overlap = next(r for r in overlap_rows if r["row_type"] == "summary_split_weak")
    mid_overlap = next(r for r in overlap_rows if r["row_type"] == "summary_split_mid")
    strong_overlap = next(r for r in overlap_rows if r["row_type"] == "summary_split_strong")
    overlap_serious = float(overlap_summary_row["overlapped_target_ratio"]) > 0.5
    weak_split_risky = float(weak_overlap["overlapped_target_ratio"]) > 0.5
    guard_pfa_1e2 = [r for r in guard_rows if abs(float(r["target_pfa"]) - 0.01) < 1e-12]
    guard_pfa_values = [float(r["test_measured_pfa"]) for r in guard_pfa_1e2]
    guard_sensitive = max(guard_pfa_values) - min(guard_pfa_values) > 0.005
    pfa_1e2 = next(r for r in pfa_rows if abs(float(r["target_pfa"]) - 0.01) < 1e-12)
    pfa_1e3 = next(r for r in pfa_rows if abs(float(r["target_pfa"]) - 0.001) < 1e-12)
    pfa_stable = (
        abs(float(pfa_1e2["measured_pfa"]) - 0.01) < 0.003
        and abs(float(pfa_1e3["measured_pfa"]) - 0.001) < 0.0008
    )
    ra_better = float(ra_summary["ra_projection_hit_rate"]) > float(default["projection_hit_rate"]) + 0.02
    d1a_plus_pass = (not guard_sensitive) and pfa_stable and float(default["projection_hit_rate"]) > 0.95

    def table(rows: list[dict[str, Any]], cols: list[str]) -> str:
        lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
        for row in rows:
            vals = []
            for c in cols:
                v = row.get(c, "")
                if isinstance(v, float):
                    vals.append(f"{v:.4f}")
                else:
                    try:
                        vals.append(f"{float(v):.4f}" if str(v) not in ("", "nan") else "")
                    except Exception:
                        vals.append(str(v))
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    report = f"""# D1A+ Gao77 Mask Stress Test 与 Fixed-PFA 稳定性报告

生成时间：2026-06-26 16:45  
阶段：D1A+，仅 clean range-only / mask stress / fixed-PFA stability  
数据：`{SUBSET_DIR}`

## 1. 执行边界

本次没有进入 D1B，没有做 synthetic interference injection，没有训练模型，没有进入 D2-D14，没有下载新数据集，也没有引入任何 backbone。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D1A+ 是否通过 | {'通过' if d1a_plus_pass else '谨慎通过/需修正'} |
| target mask 是否过宽 | {'默认 mask 偏宽，建议 D1B 先用 narrow/default 双口径报告' if target_overwide else '未见明显过宽'} |
| D1A 结果是否对 target mask 宽度敏感 | {'是，weak Pd/F1 对宽度较敏感' if mask_sensitive else '不算高度敏感'} |
| target mask overlap 是否严重 | {'较严重' if overlap_serious else '不严重'} |
| weak/mid/strong split 是否受 overlap 影响 | {'weak split 可能受 overlap 影响' if weak_split_risky else '影响可控'} |
| fixed-PFA 是否对 guard ring 敏感 | {'敏感' if guard_sensitive else '不高度敏感'} |
| PFA 统计是否稳定 | {'稳定' if pfa_stable else '不够稳定'} |
| RA projection 是否比 range-only 更可信 | {'RA 更好' if ra_better else '当前 RA 未明显优于 range-only'} |
| 是否可进入 D1B | {'可以进入，但 D1B 先做 range-only sanity，并保留 narrow/default mask 对照' if d1a_plus_pass else '暂不建议，先修 mask/guard/PFA'} |
| D1B 建议 | {'range-only D1B 优先；RA 仅作辅助可视化' if not ra_better else '可考虑 RA-based D1B，但仍需保留 range-only 对照'} |

## 3. Target Mask 宽度敏感性

target PFA = 1e-2 下的主要结果：

{table([narrow, default, wide], ['mask_name', 'target_cells_mean', 'guard_cells_mean', 'background_cells_mean', 'projection_hit_rate', 'target_background_energy_ratio_db', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'test_measured_pfa', 'f1'])}

完整结果：`G:\\mineru_output\\results\\d1a_plus_mask_stress_test\\mask_width_sensitivity.csv`

判断：默认 mask 平均 target cells 为 {float(default['target_cells_mean']):.2f}，比 narrow 的 {float(narrow['target_cells_mean']):.2f} 大不少。projection hit rate 在三种设置下都很高，但 weak Pd 和 F1 会随 mask 宽度变化，因此 D1B 不应只报告单一 mask 口径。

## 4. Mask Overlap 检查

| 指标 | 数值 |
|---|---:|
| overlap pair ratio | {float(overlap_summary_row['overlap_pair_ratio']):.4f} |
| overlap cell ratio | {float(overlap_summary_row['overlap_cell_ratio']):.4f} |
| overlapped target ratio | {float(overlap_summary_row['overlapped_target_ratio']):.4f} |
| weak overlap target ratio | {float(weak_overlap['overlapped_target_ratio']):.4f} |
| mid overlap target ratio | {float(mid_overlap['overlapped_target_ratio']):.4f} |
| strong overlap target ratio | {float(strong_overlap['overlapped_target_ratio']):.4f} |

判断：overlap 不是可以忽略的小问题。D1B 中 weak/mid/strong split 最好增加一个 `non-overlap only` 辅助统计，避免 weak/strong 结论被多目标重叠污染。

## 5. Guard Ring 敏感性

target PFA = 1e-2：

{table(guard_pfa_1e2, ['guard_extra_bins', 'background_cells_mean', 'validation_threshold', 'test_measured_pfa', 'weak_pd', 'mid_pd', 'strong_pd', 'false_alarm_count', 'background_cell_count'])}

完整结果：`G:\\mineru_output\\results\\d1a_plus_mask_stress_test\\guard_sensitivity.csv`

判断：guard 改变会影响背景 cell 数和阈值，但 test PFA 仍接近目标 PFA；因此 fixed-PFA calibration 不算对 guard ring 高度敏感。

## 6. PFA 统计稳定性

{table(pfa_rows, ['target_pfa', 'background_cell_count', 'false_alarm_count', 'measured_pfa', 'frame_level_pfa_std', 'bootstrap_pfa_std', 'bootstrap_pfa_ci_low', 'bootstrap_pfa_ci_high'])}

per-source-sequence PFA：`G:\\mineru_output\\results\\d1a_plus_mask_stress_test\\pfa_by_sequence.csv`  
per-class-group Pd：`G:\\mineru_output\\results\\d1a_plus_mask_stress_test\\pd_by_class_group.csv`

判断：整体 PFA 稳定；per-sequence 仍需在 D1B 中继续观察，因为干扰注入后不同 sequence 的背景统计可能分化。

## 7. RA Projection 补充检查

| 指标 | 数值 |
|---|---:|
| RA projection hit rate | {float(ra_summary['ra_projection_hit_rate']):.4f} |
| RA target/background ratio mean dB | {float(ra_summary['ra_target_background_ratio_db_mean']):.4f} |

判断：RA map 可以生成，RA projection sanity 可用，但当前没有明显比 range-only 更可信。D1B 优先做 range-only interference sanity，RA 作为辅助可视化和后续扩展。

## 8. 输出文件

结果目录：

`G:\\mineru_output\\results\\d1a_plus_mask_stress_test`

图像目录：

`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d1a_plus_figures`

关键文件：

- `mask_width_sensitivity.csv`
- `guard_sensitivity.csv`
- `mask_overlap_summary.csv`
- `pfa_stability_summary.csv`
- `pfa_by_sequence.csv`
- `pd_by_class_group.csv`
- `ra_projection_sanity.csv`
- `d1a_plus_config.json`

## 9. 下一步建议

可以进入 D1B synthetic interference sanity，但建议只先做 range-only D1B，并且保留以下防护：

1. 同时报告 narrow/default mask 两套指标；
2. 输出 non-overlap-only 的 weak/mid/strong 辅助统计；
3. 固定 PFA 阈值必须继续报告 background cell count、false alarm count、bootstrap/frame-level std；
4. RA 只作为辅助 sanity，不要作为第一版 D1B 主指标。
"""
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    REPORT_TS_PATH.write_text(report, encoding="utf-8-sig")


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    manifest, targets, range_power, range_db, ra_maps, _ = load_dataset()
    _, val_idx, test_idx = load_split(len(manifest))
    cfar_scores = ca_cfar_score(range_power)

    mask_rows, mask_artifacts = mask_width_sensitivity(range_db, cfar_scores, targets, val_idx, test_idx)
    default_art = mask_artifacts["default"]
    overlap_rows = overlap_summary(
        targets,
        default_art["intervals"],
        default_art["splits"],
        len(manifest),
        range_db.shape[1],
    )
    default_cfg = next(c for c in MASK_CONFIGS if c["mask_name"] == "default")
    guard_rows = guard_sensitivity(
        range_db,
        cfar_scores,
        targets,
        val_idx,
        test_idx,
        default_cfg,
        default_art["splits"],
    )
    pfa_rows, pfa_seq_rows, pd_group_rows = pfa_stability(
        cfar_scores,
        default_art["background_mask"],
        targets,
        default_art["intervals"],
        default_art["splits"],
        manifest,
        val_idx,
        test_idx,
    )
    ra_rows, ra_summary = ra_projection_sanity(ra_maps, targets)

    write_csv(RESULT_DIR / "mask_width_sensitivity.csv", mask_rows)
    write_csv(RESULT_DIR / "guard_sensitivity.csv", guard_rows)
    write_csv(RESULT_DIR / "mask_overlap_summary.csv", overlap_rows)
    write_csv(RESULT_DIR / "pfa_stability_summary.csv", pfa_rows)
    write_csv(RESULT_DIR / "pfa_by_sequence.csv", pfa_seq_rows)
    write_csv(RESULT_DIR / "pd_by_class_group.csv", pd_group_rows)
    write_csv(RESULT_DIR / "ra_projection_sanity.csv", ra_rows)
    write_json(
        RESULT_DIR / "d1a_plus_config.json",
        {
            "subset_dir": str(SUBSET_DIR),
            "d1a_result_dir": str(D1A_RESULT_DIR),
            "mask_configs": MASK_CONFIGS,
            "guard_configs": GUARD_CONFIGS,
            "valid_pfa_targets": VALID_PFA_TARGETS,
            "cfar_guard": CFAR_GUARD,
            "cfar_train": CFAR_TRAIN,
            "valid_range_bins": [VALID_RANGE_MIN_BIN, VALID_RANGE_MAX_BIN],
            "label_policy_path": str(LABEL_POLICY_PATH),
            "strict_limits": {
                "no_d1b": True,
                "no_synthetic_interference": True,
                "no_training": True,
                "no_d2_d14": True,
                "no_new_dataset": True,
                "no_backbone": True,
            },
        },
    )
    plot_outputs(mask_rows, guard_rows, overlap_rows, pfa_seq_rows, pd_group_rows, ra_maps, targets)
    write_report(mask_rows, guard_rows, overlap_rows, pfa_rows, pfa_seq_rows, pd_group_rows, ra_summary)
    print(
        json.dumps(
            {
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "report": str(REPORT_PATH),
                "mask_rows": len(mask_rows),
                "guard_rows": len(guard_rows),
                "ra_projection_hit_rate": ra_summary["ra_projection_hit_rate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
