from __future__ import annotations

import csv
import json
import math
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

import d4_gao77_strong_baseline_sanity as d4
import d5b_d5c_weak_definition_rdra_diagnosis as d5c
from d1a_gao77_clean_fixed_pfa_sanity import (
    EXPECTED_ADC_SHAPE,
    MANIFEST_PATH,
    RADAR_DIR,
    RANGE_RESOLUTION_M,
    ROOT,
    VALID_RANGE_MAX_BIN,
    VALID_RANGE_MIN_BIN,
    ca_cfar_score_1d_np,
    radar_maps,
    read_csv_dicts,
    write_csv,
    write_json,
)
from d1a_plus_mask_stress_test import MASK_CONFIGS, assign_splits, build_masks, interval, target_peak_and_projection
from d1b_gao77_synthetic_interference_sanity import EPS, non_overlap_ids
from d2a_gao77_small_model_sanity import load_clean_data, load_split


RESULT_DIR = ROOT / "results" / "d5c_ra_rca_self_check"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5c_ra_rca_figures"
PRIOR_D5C_DIR = ROOT / "results" / "d5b_d5c_weak_definition_rdra_diagnosis"
PRIOR_D1A_PLUS_DIR = ROOT / "results" / "d1a_plus_mask_stress_test"

PRIMARY_PFA = 1e-2
SECONDARY_PFA = 1e-3
SPLIT_KEY = "clean_peak_percentile"
ANGLE_TOTAL_WIDTHS = [1, 2, 3, 5, 7, 10]
RANGE_MASK_NAMES = ["narrow", "default", "wide"]


ANGLE_CANDIDATES: list[dict[str, str]] = [
    {
        "candidate": "atan2_px_py_current",
        "formula": "atan2(px, py)",
        "unit_mode": "degrees_correct",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "normal",
    },
    {
        "candidate": "atan2_py_px_current",
        "formula": "atan2(py, px)",
        "unit_mode": "degrees_correct",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "normal",
    },
    {
        "candidate": "atan2_neg_px_py_current",
        "formula": "atan2(-px, py)",
        "unit_mode": "degrees_correct",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "normal",
    },
    {
        "candidate": "atan2_px_neg_py_current",
        "formula": "atan2(px, -py)",
        "unit_mode": "degrees_correct",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "normal",
    },
    {
        "candidate": "atan2_px_py_degrees_treated_as_radians",
        "formula": "atan2(px, py)",
        "unit_mode": "degrees_treated_as_radians",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "normal",
    },
    {
        "candidate": "atan2_px_py_radians_treated_as_degrees",
        "formula": "atan2(px, py)",
        "unit_mode": "radians_treated_as_degrees",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "normal",
    },
    {
        "candidate": "atan2_px_py_axis_reversed",
        "formula": "atan2(px, py)",
        "unit_mode": "degrees_correct",
        "bin_mode": "fftshift_linear_sin",
        "axis_sign": "reversed",
    },
    {
        "candidate": "atan2_px_py_unshifted_bins_on_shifted_map",
        "formula": "atan2(px, py)",
        "unit_mode": "degrees_correct",
        "bin_mode": "unshifted_bins_on_shifted_map",
        "axis_sign": "normal",
    },
]


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def to_float(value: Any, default: float = 0.0) -> float:
    if value in ("", None):
        return default
    return float(value)


def finite_mean(values: list[float]) -> float | str:
    vals = [float(v) for v in values if np.isfinite(float(v))]
    return float(np.mean(vals)) if vals else ""


def finite_median(values: list[float]) -> float | str:
    vals = [float(v) for v in values if np.isfinite(float(v))]
    return float(np.median(vals)) if vals else ""


def finite_p90(values: list[float]) -> float | str:
    vals = [float(v) for v in values if np.isfinite(float(v))]
    return float(np.quantile(vals, 0.9)) if vals else ""


def centered_bounds(center: int, total_width: int, n_bins: int) -> tuple[int, int]:
    total = max(1, int(total_width))
    left = total // 2
    right = total - left
    return max(0, center - left), min(n_bins, center + right)


def valid_range_mask(n_bins: int) -> np.ndarray:
    mask = np.zeros(n_bins, dtype=bool)
    mask[VALID_RANGE_MIN_BIN : min(VALID_RANGE_MAX_BIN + 1, n_bins)] = True
    return mask


def write_csv_versioned(path: Path, rows: list[dict[str, Any]], outputs: list[tuple[Path, str]], desc: str) -> None:
    write_csv(path, rows)
    outputs.append((path, desc))
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    write_csv(ts_path, rows)
    outputs.append((ts_path, f"{desc} timestamped copy"))


def write_json_versioned(path: Path, data: Any, outputs: list[tuple[Path, str]], desc: str) -> None:
    write_json(path, data)
    outputs.append((path, desc))
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    write_json(ts_path, data)
    outputs.append((ts_path, f"{desc} timestamped copy"))


def write_text_versioned(path: Path, text: str, outputs: list[tuple[Path, str]], desc: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig")
    outputs.append((path, desc))
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8-sig")
    outputs.append((ts_path, f"{desc} timestamped copy"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def target_angle_rad(target: Any, formula: str) -> float:
    px = float(target.px)
    py = float(target.py)
    if formula == "atan2(px, py)":
        return math.atan2(px, py)
    if formula == "atan2(py, px)":
        return math.atan2(py, px)
    if formula == "atan2(-px, py)":
        return math.atan2(-px, py)
    if formula == "atan2(px, -py)":
        return math.atan2(px, -py)
    raise KeyError(formula)


def candidate_sin_theta(target: Any, candidate: dict[str, str]) -> tuple[float, float]:
    rad = target_angle_rad(target, candidate["formula"])
    deg = math.degrees(rad)
    unit_mode = candidate["unit_mode"]
    if unit_mode == "degrees_correct":
        sin_theta = math.sin(math.radians(deg))
    elif unit_mode == "degrees_treated_as_radians":
        sin_theta = math.sin(deg)
    elif unit_mode == "radians_treated_as_degrees":
        sin_theta = math.sin(math.radians(rad))
    else:
        raise KeyError(unit_mode)
    if candidate["axis_sign"] == "reversed":
        sin_theta = -sin_theta
    return deg, max(-1.0, min(1.0, sin_theta))


def angle_bin_for_candidate(target: Any, n_angle: int, candidate: dict[str, str]) -> int:
    _deg, sin_theta = candidate_sin_theta(target, candidate)
    if candidate["bin_mode"] == "fftshift_linear_sin":
        return int(round((sin_theta + 1.0) * 0.5 * (n_angle - 1)))
    if candidate["bin_mode"] == "unshifted_bins_on_shifted_map":
        return int(round((0.5 * sin_theta * n_angle))) % n_angle
    raise KeyError(candidate["bin_mode"])


def current_linear_angle_axis_deg(n_angle: int) -> np.ndarray:
    sin_axis = np.linspace(-1.0, 1.0, n_angle)
    return np.degrees(np.arcsin(np.clip(sin_axis, -1.0, 1.0)))


def exact_fftshift_angle_axis_deg(n_angle: int) -> np.ndarray:
    freq = np.fft.fftshift(np.fft.fftfreq(n_angle, d=1.0))
    sin_axis = np.clip(2.0 * freq, -1.0, 1.0)
    return np.degrees(np.arcsin(sin_axis))


def unshifted_angle_axis_deg(n_angle: int) -> np.ndarray:
    freq = np.fft.fftfreq(n_angle, d=1.0)
    sin_axis = np.clip(2.0 * freq, -1.0, 1.0)
    return np.degrees(np.arcsin(sin_axis))


def build_all_range_contexts(clean_db: np.ndarray, clean_cfar: np.ndarray, targets: list[Any]) -> dict[str, dict[str, Any]]:
    contexts: dict[str, dict[str, Any]] = {}
    n_frames, n_bins = clean_db.shape
    for cfg in MASK_CONFIGS:
        tm, gm, bm, intervals = build_masks(targets, n_frames, n_bins, cfg)
        target_values = target_peak_and_projection(clean_db, clean_cfar, targets, intervals, int(cfg["guard_extra"]))
        contexts[str(cfg["mask_name"])] = {
            "cfg": cfg,
            "target_mask": tm,
            "guard_mask": gm,
            "background_mask": bm,
            "intervals": intervals,
            "splits": {
                "clean_peak_percentile": assign_splits(target_values, "target_peak_db"),
                "cfar_margin": assign_splits(target_values, "cfar_margin_db"),
            },
            "non_overlap_ids": non_overlap_ids(intervals, targets),
            "target_values": target_values,
        }
    d5c.extend_context_splits(contexts, targets)
    return contexts


def load_all_ra_maps(manifest: list[dict[str, str]]) -> tuple[np.ndarray, list[dict[str, Any]]]:
    n_frames = len(manifest)
    n_range = EXPECTED_ADC_SHAPE[0]
    n_angle = 64
    ra_maps = np.zeros((n_frames, n_range, n_angle), dtype=np.float32)
    audit_rows: list[dict[str, Any]] = []
    first_shapes: dict[str, Any] = {}
    for frame_idx, row in enumerate(manifest):
        adc = loadmat(RADAR_DIR / row["new_radar_file"])["adcData"]
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"unexpected adcData shape {adc.shape} in {row['new_radar_file']}")
        if frame_idx == 0:
            virt = np.concatenate([adc[:, :, :, t] for t in range(adc.shape[3])], axis=2)
            range_fft = np.fft.fft(virt, axis=0)
            range_virt = np.mean(range_fft, axis=1)
            angle_fft = np.fft.fftshift(np.fft.fft(range_virt, n=n_angle, axis=1), axes=1)
            first_shapes = {
                "raw_adc_shape": "x".join(str(x) for x in adc.shape),
                "sample_axis": 0,
                "chirp_axis": 1,
                "rx_axis": 2,
                "tx_axis": 3,
                "virtual_array_shape_after_tx_concat": "x".join(str(x) for x in virt.shape),
                "range_fft_axis": 0,
                "range_fft_shape": "x".join(str(x) for x in range_fft.shape),
                "range_virt_shape_after_chirp_mean": "x".join(str(x) for x in range_virt.shape),
                "angle_fft_axis_in_range_virt": 1,
                "angle_fft_shape": "x".join(str(x) for x in angle_fft.shape),
                "uses_rx_or_virtual_antenna_axis": True,
                "uses_chirp_axis_for_angle_fft": False,
                "uses_sample_axis_for_angle_fft": False,
                "uses_fftshift": True,
                "virtual_array_note": "8 elements from 4 RX x 2 TX concatenation; no TDM-MIMO phase compensation in this smoke map",
            }
        _rp, _rd, ra_map = radar_maps(adc)
        ra_maps[frame_idx] = ra_map.astype(np.float32)
        if frame_idx % 250 == 0:
            print(json.dumps({"event": "loaded_ra_frame", "frame_idx": frame_idx, "frame_count": n_frames}))

    audit_rows.append(
        {
            "check": "adc_dimension_interpretation",
            **first_shapes,
            "axis_bug_found": False,
            "reliability_note": "RA is a smoke representation, not a calibrated production RA pipeline",
        }
    )
    return ra_maps, audit_rows


def d1a_style_projection_rows(
    ra_maps: np.ndarray,
    targets: list[Any],
    candidate: dict[str, str],
    frame_filter: set[int] | None = None,
    split_map: dict[int, str] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    n_range = ra_maps.shape[1]
    n_angle = ra_maps.shape[2]
    for target in targets:
        frame_idx = int(target.frame_idx)
        if frame_filter is not None and frame_idx not in frame_filter:
            continue
        if not bool(target.valid_projection):
            continue
        angle_bin = angle_bin_for_candidate(target, n_angle, candidate)
        r0, r1 = interval(int(target.range_bin), 2, n_range)
        a0, a1 = interval(angle_bin, 2, n_angle)
        gr0, gr1 = interval(int(target.range_bin), 6, n_range)
        ga0, ga1 = interval(angle_bin, 6, n_angle)
        frame = ra_maps[frame_idx]
        target_patch = frame[r0:r1, a0:a1]
        guard_patch = frame[gr0:gr1, ga0:ga1].copy()
        local_mask = np.ones_like(guard_patch, dtype=bool)
        local_mask[(r0 - gr0) : (r1 - gr0), (a0 - ga0) : (a1 - ga0)] = False
        bg_vals = guard_patch[local_mask]
        target_peak = float(np.max(target_patch)) if target_patch.size else float("nan")
        bg_mean = float(np.mean(bg_vals)) if bg_vals.size else float("nan")
        ratio = target_peak - bg_mean if not math.isnan(bg_mean) else float("nan")
        frame_p70 = float(np.percentile(frame, 70))
        hit = bool(target_peak >= frame_p70 and (math.isnan(bg_mean) or ratio >= 0.0))
        rows.append(
            {
                "target_id": int(target.target_id),
                "frame_idx": frame_idx,
                "source_sequence": str(target.source_sequence),
                "class_group": str(target.group),
                "split": split_map.get(int(target.target_id), "") if split_map is not None else "",
                "range_bin": int(target.range_bin),
                "angle_bin": angle_bin,
                "ra_target_peak_db": target_peak,
                "ra_background_mean_db": bg_mean,
                "ra_target_background_ratio_db": ratio,
                "ra_projection_hit": hit,
            }
        )
    return rows


def aggregate_local_projection(rows: list[dict[str, Any]], split_name: str | None = None) -> dict[str, Any]:
    selected = rows if split_name is None else [r for r in rows if r.get("split") == split_name]
    hits = sum(1 for r in selected if bool(r["ra_projection_hit"]))
    ratios = [float(r["ra_target_background_ratio_db"]) for r in selected if np.isfinite(float(r["ra_target_background_ratio_db"]))]
    return {
        "target_count": len(selected),
        "hit_count": hits,
        "hit_rate": hits / max(len(selected), 1),
        "target_background_ratio_db_mean": float(np.mean(ratios)) if ratios else "",
    }


def compute_overlap_flags(rect_by_target: dict[int, tuple[int, int, int, int]], target_by_id: dict[int, Any]) -> set[int]:
    by_frame: dict[int, list[int]] = defaultdict(list)
    for tid in rect_by_target:
        by_frame[int(target_by_id[tid].frame_idx)].append(tid)
    overlapped: set[int] = set()
    for tids in by_frame.values():
        for i, tid in enumerate(tids):
            for oid in tids[i + 1 :]:
                if d5c.rects_overlap(rect_by_target[tid], rect_by_target[oid]):
                    overlapped.add(tid)
                    overlapped.add(oid)
    return overlapped


def evaluate_ra_fixed_pfa(
    ra_maps: np.ndarray,
    targets: list[Any],
    ctx: dict[str, Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    candidate: dict[str, str],
    angle_total_width: int,
    range_mask_name: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    eval_frames = np.asarray(sorted(set(val_frames.tolist()) | set(test_frames.tolist())), dtype=int)
    frame_to_pos = {int(frame): pos for pos, frame in enumerate(eval_frames.tolist())}
    score = ra_maps[eval_frames]
    n_eval, n_range, n_angle = score.shape
    target_mask = np.zeros((n_eval, n_range, n_angle), dtype=bool)
    guard_mask = np.zeros((n_eval, n_range, n_angle), dtype=bool)
    intervals = ctx["intervals"]
    splits = ctx["splits"][SPLIT_KEY]
    valid_range = valid_range_mask(n_range)[:, None]
    test_set = set(int(x) for x in test_frames.tolist())
    val_pos = np.asarray([frame_to_pos[int(x)] for x in val_frames.tolist() if int(x) in frame_to_pos], dtype=int)
    test_pos = np.asarray([frame_to_pos[int(x)] for x in test_frames.tolist() if int(x) in frame_to_pos], dtype=int)
    angle_axis = current_linear_angle_axis_deg(n_angle)

    per_target: list[dict[str, Any]] = []
    rect_by_target: dict[int, tuple[int, int, int, int]] = {}
    target_by_id = {int(t.target_id): t for t in targets}
    for target in targets:
        tid = int(target.target_id)
        frame_idx = int(target.frame_idx)
        if frame_idx not in frame_to_pos or tid not in intervals or tid not in splits:
            continue
        pos = frame_to_pos[frame_idx]
        lo, hi, _radius = intervals[tid]
        angle_bin = angle_bin_for_candidate(target, n_angle, candidate)
        clo, chi = centered_bounds(angle_bin, angle_total_width, n_angle)
        gclo, gchi = centered_bounds(angle_bin, angle_total_width + 6, n_angle)
        grlo, grhi = max(0, lo - 4), min(n_range, hi + 4)
        target_mask[pos, lo:hi, clo:chi] = True
        guard_mask[pos, grlo:grhi, gclo:gchi] = True
        if frame_idx not in test_set:
            continue

        target_values = score[pos, lo:hi, clo:chi]
        local_guard = np.zeros((n_range, n_angle), dtype=bool)
        local_target = np.zeros((n_range, n_angle), dtype=bool)
        local_guard[grlo:grhi, gclo:gchi] = True
        local_target[lo:hi, clo:chi] = True
        local_bg = np.logical_and(local_guard, ~local_target)
        local_bg = np.logical_and(local_bg, valid_range)
        bg_values = score[pos][local_bg]
        peak = float(np.max(target_values)) if target_values.size else float("nan")
        bg_med = float(np.median(bg_values)) if bg_values.size else float("nan")
        range_sub = score[pos, lo:hi, :]
        if range_sub.size:
            peak_flat = int(np.argmax(range_sub))
            _peak_r, peak_angle_bin = np.unravel_index(peak_flat, range_sub.shape)
            peak_angle_bin = int(peak_angle_bin)
        else:
            peak_angle_bin = -1
        if peak_angle_bin >= 0:
            signed_err_bins = peak_angle_bin - angle_bin
            signed_err_deg = float(angle_axis[peak_angle_bin] - angle_axis[angle_bin])
            abs_err_deg = abs(signed_err_deg)
        else:
            signed_err_bins = ""
            signed_err_deg = ""
            abs_err_deg = ""
        rect_by_target[tid] = (lo, hi, clo, chi)
        per_target.append(
            {
                "target_id": tid,
                "frame_idx": frame_idx,
                "source_sequence": str(target.source_sequence),
                "class_group": str(target.group),
                "split": splits[tid],
                "range_bin": int(target.range_bin),
                "angle_bin": angle_bin,
                "angle_total_width_bins": int(angle_total_width),
                "range_mask_name": range_mask_name,
                "peak_angle_bin": peak_angle_bin,
                "signed_peak_angle_error_bins": signed_err_bins,
                "signed_peak_angle_error_deg": signed_err_deg,
                "abs_peak_angle_error_deg": abs_err_deg,
                "peak_score_db": peak,
                "local_background_db": bg_med,
                "contrast_db": peak - bg_med if np.isfinite(peak) and np.isfinite(bg_med) else "",
                "fixed_pfa_hit": False,
                "ra_rect_overlap": False,
            }
        )

    guard_ring = np.logical_and(guard_mask, ~target_mask)
    valid = np.broadcast_to(valid_range, target_mask.shape).copy()
    background_mask = np.logical_and(valid, ~np.logical_or(target_mask, guard_ring))
    val_bg = score[val_pos][background_mask[val_pos]]
    thresholds = {
        PRIMARY_PFA: float(np.quantile(val_bg, 1.0 - PRIMARY_PFA)),
        SECONDARY_PFA: float(np.quantile(val_bg, 1.0 - SECONDARY_PFA)),
    }
    detections = score >= thresholds[PRIMARY_PFA]
    test_bg = background_mask[test_pos]
    false_alarm_count = int(np.logical_and(detections[test_pos], test_bg).sum())
    background_cell_count = int(test_bg.sum())
    measured_pfa = false_alarm_count / max(background_cell_count, 1)
    hit_by_tid = {}
    for tid, rect in rect_by_target.items():
        target = target_by_id[tid]
        pos = frame_to_pos[int(target.frame_idx)]
        rlo, rhi, clo, chi = rect
        hit_by_tid[tid] = bool(detections[pos, rlo:rhi, clo:chi].any())
    overlapped = compute_overlap_flags(rect_by_target, target_by_id)
    for row in per_target:
        tid = int(row["target_id"])
        row["fixed_pfa_hit"] = hit_by_tid.get(tid, False)
        row["ra_rect_overlap"] = tid in overlapped

    subset_rows = aggregate_fixed_pfa_subsets(per_target, candidate, range_mask_name, angle_total_width)
    hits = sum(1 for r in per_target if r["fixed_pfa_hit"])
    weak_rows = [r for r in per_target if r["split"] == "weak"]
    weak_hits = sum(1 for r in weak_rows if r["fixed_pfa_hit"])
    valid_cells = int(valid[test_pos].sum())
    summary = {
        "candidate": candidate["candidate"],
        "formula": candidate["formula"],
        "unit_mode": candidate["unit_mode"],
        "bin_mode": candidate["bin_mode"],
        "axis_sign": candidate["axis_sign"],
        "range_mask_name": range_mask_name,
        "angle_total_width_bins": int(angle_total_width),
        "angle_guard_total_width_bins": int(angle_total_width + 6),
        "target_count": len(per_target),
        "target_hit_count": hits,
        "target_projection_hit_rate": hits / max(len(per_target), 1),
        "weak_target_count": len(weak_rows),
        "weak_target_hit_count": weak_hits,
        "weak_target_projection_hit_rate": weak_hits / max(len(weak_rows), 1),
        "target_overlap_ratio": sum(1 for r in per_target if r["ra_rect_overlap"]) / max(len(per_target), 1),
        "weak_target_overlap_ratio": sum(1 for r in weak_rows if r["ra_rect_overlap"]) / max(len(weak_rows), 1),
        "threshold_at_pfa_1e_2": thresholds[PRIMARY_PFA],
        "threshold_at_pfa_1e_3": thresholds[SECONDARY_PFA],
        "measured_pfa_at_target_pfa_1e_2": measured_pfa,
        "false_alarm_count": false_alarm_count,
        "background_cell_count": background_cell_count,
        "target_mask_cell_count": int(target_mask[test_pos].sum()),
        "guard_ring_cell_count": int(guard_ring[test_pos].sum()),
        "valid_cell_count": valid_cells,
        "target_mask_area_ratio": int(target_mask[test_pos].sum()) / max(valid_cells, 1),
        "excluded_area_ratio": (int(target_mask[test_pos].sum()) + int(guard_ring[test_pos].sum())) / max(valid_cells, 1),
        "mean_abs_peak_angle_error_deg": finite_mean(
            [float(r["abs_peak_angle_error_deg"]) for r in per_target if r["abs_peak_angle_error_deg"] != ""]
        ),
        "median_abs_peak_angle_error_deg": finite_median(
            [float(r["abs_peak_angle_error_deg"]) for r in per_target if r["abs_peak_angle_error_deg"] != ""]
        ),
        "p90_abs_peak_angle_error_deg": finite_p90(
            [float(r["abs_peak_angle_error_deg"]) for r in per_target if r["abs_peak_angle_error_deg"] != ""]
        ),
        "mean_contrast_db": finite_mean([float(r["contrast_db"]) for r in per_target if r["contrast_db"] != ""]),
        "weak_mean_contrast_db": finite_mean([float(r["contrast_db"]) for r in weak_rows if r["contrast_db"] != ""]),
        "scope_note": "D5C fixed-PFA RA smoke on validation/test split; no model training",
    }
    return summary, per_target, subset_rows


def aggregate_fixed_pfa_subsets(
    per_target: list[dict[str, Any]],
    candidate: dict[str, str],
    range_mask_name: str,
    angle_total_width: int,
) -> list[dict[str, Any]]:
    subset_defs = {
        "all": lambda r: True,
        "weak": lambda r: r["split"] == "weak",
        "mid": lambda r: r["split"] == "mid",
        "strong": lambda r: r["split"] == "strong",
        "non_overlap_only_weak": lambda r: r["split"] == "weak" and not bool(r["ra_rect_overlap"]),
        "overlap_only_weak": lambda r: r["split"] == "weak" and bool(r["ra_rect_overlap"]),
    }
    rows: list[dict[str, Any]] = []
    for subset, pred in subset_defs.items():
        selected = [r for r in per_target if pred(r)]
        hits = sum(1 for r in selected if bool(r["fixed_pfa_hit"]))
        rows.append(
            {
                "candidate": candidate["candidate"],
                "formula": candidate["formula"],
                "unit_mode": candidate["unit_mode"],
                "bin_mode": candidate["bin_mode"],
                "axis_sign": candidate["axis_sign"],
                "range_mask_name": range_mask_name,
                "angle_total_width_bins": int(angle_total_width),
                "subset": subset,
                "target_count": len(selected),
                "hit_count": hits,
                "projection_hit_rate": hits / max(len(selected), 1),
                "overlap_ratio": sum(1 for r in selected if bool(r["ra_rect_overlap"])) / max(len(selected), 1),
                "mean_contrast_db": finite_mean([float(r["contrast_db"]) for r in selected if r["contrast_db"] != ""]),
                "mean_abs_peak_angle_error_deg": finite_mean(
                    [float(r["abs_peak_angle_error_deg"]) for r in selected if r["abs_peak_angle_error_deg"] != ""]
                ),
            }
        )
    return rows


def axis_audit_rows(n_angle: int) -> list[dict[str, Any]]:
    current = current_linear_angle_axis_deg(n_angle)
    exact_shift = exact_fftshift_angle_axis_deg(n_angle)
    unshifted = unshifted_angle_axis_deg(n_angle)
    axes = [
        ("d5c_current_linear_shifted_sin_axis", current, True, True),
        ("exact_fftshift_fftfreq_half_lambda_axis", exact_shift, True, True),
        ("unshifted_fftfreq_half_lambda_axis", unshifted, False, False),
        ("reversed_d5c_current_linear_shifted_sin_axis", current[::-1], True, False),
    ]
    rows = []
    for name, axis, fftshift, monotonic_expected in axes:
        diffs = np.diff(axis)
        rows.append(
            {
                "axis_name": name,
                "angle_axis_min_deg": float(np.min(axis)),
                "angle_axis_max_deg": float(np.max(axis)),
                "angle_bin_count": int(n_angle),
                "unit": "degree",
                "uses_fftshift": fftshift,
                "is_monotonic_increasing": bool(np.all(diffs >= -1e-9)),
                "expected_monotonic_for_shifted_plot": monotonic_expected,
                "bin0_angle_deg": float(axis[0]),
                "center_bin": int(n_angle // 2),
                "center_angle_deg": float(axis[n_angle // 2]),
                "last_bin_angle_deg": float(axis[-1]),
                "mean_bin_step_deg": float(np.mean(np.abs(diffs))) if diffs.size else "",
                "max_abs_step_deg": float(np.max(np.abs(diffs))) if diffs.size else "",
            }
        )
    return rows


def formula_distribution_rows(
    targets: list[Any],
    candidates: list[dict[str, str]],
    local_rows_by_candidate: dict[str, list[dict[str, Any]]],
    fixed_rows_by_candidate: dict[str, dict[str, Any]],
    manifest_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    manifest_az_min = min(float(r["azimuth_min"]) for r in manifest_rows if r.get("azimuth_min") not in ("", None))
    manifest_az_max = max(float(r["azimuth_max"]) for r in manifest_rows if r.get("azimuth_max") not in ("", None))
    rows: list[dict[str, Any]] = []
    valid_targets = [t for t in targets if bool(t.valid_projection)]
    for candidate in candidates:
        az = [math.degrees(target_angle_rad(t, candidate["formula"])) for t in valid_targets]
        local_all = aggregate_local_projection(local_rows_by_candidate[candidate["candidate"]], None)
        local_weak = aggregate_local_projection(local_rows_by_candidate[candidate["candidate"]], "weak")
        fixed = fixed_rows_by_candidate[candidate["candidate"]]
        rows.append(
            {
                "candidate": candidate["candidate"],
                "formula": candidate["formula"],
                "unit_mode": candidate["unit_mode"],
                "bin_mode": candidate["bin_mode"],
                "axis_sign": candidate["axis_sign"],
                "azimuth_deg_min": float(np.min(az)),
                "azimuth_deg_max": float(np.max(az)),
                "azimuth_deg_mean": float(np.mean(az)),
                "azimuth_deg_std": float(np.std(az)),
                "within_minus90_to_90_ratio": sum(-90.0 <= x <= 90.0 for x in az) / max(len(az), 1),
                "d1a_manifest_azimuth_min_deg": manifest_az_min,
                "d1a_manifest_azimuth_max_deg": manifest_az_max,
                "consistent_with_manifest_range": bool(
                    abs(float(np.min(az)) - manifest_az_min) < 1.0 and abs(float(np.max(az)) - manifest_az_max) < 1.0
                ),
                "d1a_style_projection_hit_rate_all_frames": local_all["hit_rate"],
                "d1a_style_projection_hit_rate_d5c_test_weak": local_weak["hit_rate"],
                "d5c_fixed_pfa_target_projection_hit_rate": fixed["target_projection_hit_rate"],
                "d5c_fixed_pfa_weak_projection_hit_rate": fixed["weak_target_projection_hit_rate"],
                "mean_abs_peak_angle_error_deg": fixed["mean_abs_peak_angle_error_deg"],
                "median_abs_peak_angle_error_deg": fixed["median_abs_peak_angle_error_deg"],
                "p90_abs_peak_angle_error_deg": fixed["p90_abs_peak_angle_error_deg"],
                "formula_rank_key_weak_hit": fixed["weak_target_projection_hit_rate"],
            }
        )
    return rows


def plot_outputs(
    targets: list[Any],
    candidates: list[dict[str, str]],
    fixed_rows: list[dict[str, Any]],
    per_target_by_key: dict[tuple[str, str, int], list[dict[str, Any]]],
    ra_maps: np.ndarray,
    test_frames: np.ndarray,
    ctx: dict[str, Any],
    best_candidate: str,
    outputs: list[tuple[Path, str]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    main_formula_names = [
        "atan2_px_py_current",
        "atan2_py_px_current",
        "atan2_neg_px_py_current",
        "atan2_px_neg_py_current",
    ]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for candidate in candidates:
        if candidate["candidate"] not in main_formula_names:
            continue
        vals = [math.degrees(target_angle_rad(t, candidate["formula"])) for t in targets if bool(t.valid_projection)]
        ax.hist(vals, bins=50, alpha=0.38, label=candidate["candidate"])
    ax.set_xlabel("Azimuth (deg)")
    ax.set_ylabel("Target count")
    ax.set_title("Label azimuth formula distribution")
    ax.legend(fontsize=7)
    path = FIG_DIR / "azimuth_distribution_comparison.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs.append((path, "azimuth distribution comparison"))

    n_angle = ra_maps.shape[2]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(np.arange(n_angle), current_linear_angle_axis_deg(n_angle), label="D5C current linear shifted sin axis")
    ax.plot(np.arange(n_angle), exact_fftshift_angle_axis_deg(n_angle), label="exact fftshift(fftfreq) half-lambda axis")
    ax.set_xlabel("Angle bin")
    ax.set_ylabel("Angle (deg)")
    ax.set_title("RA angle axis definitions")
    ax.legend(fontsize=8)
    path = FIG_DIR / "angle_axis_visualization.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs.append((path, "angle axis visualization"))

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for candidate_name in ["atan2_px_py_current", best_candidate]:
        key = (candidate_name, "default", 7)
        if key not in per_target_by_key:
            continue
        vals = [
            float(r["abs_peak_angle_error_deg"])
            for r in per_target_by_key[key]
            if r["abs_peak_angle_error_deg"] != ""
        ]
        ax.hist(vals, bins=40, alpha=0.45, label=candidate_name)
    ax.set_xlabel("Abs. angle error to range-local RA peak (deg)")
    ax.set_ylabel("Target count")
    ax.set_title("Angle error histogram")
    ax.legend(fontsize=8)
    path = FIG_DIR / "angle_error_histogram.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs.append((path, "angle error histogram"))

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    for candidate_name in sorted({"atan2_px_py_current", best_candidate}):
        rows = [
            r
            for r in fixed_rows
            if r["candidate"] == candidate_name and r["range_mask_name"] == "default"
        ]
        rows = sorted(rows, key=lambda r: int(r["angle_total_width_bins"]))
        ax.plot(
            [int(r["angle_total_width_bins"]) for r in rows],
            [float(r["weak_target_projection_hit_rate"]) for r in rows],
            marker="o",
            label=f"{candidate_name} weak",
        )
        ax.plot(
            [int(r["angle_total_width_bins"]) for r in rows],
            [float(r["target_projection_hit_rate"]) for r in rows],
            marker="x",
            linestyle="--",
            label=f"{candidate_name} all",
        )
    ax.set_xlabel("Angle target mask total width (bins)")
    ax.set_ylabel("Fixed-PFA hit rate")
    ax.set_title("Mask width vs RA hit rate")
    ax.legend(fontsize=7)
    path = FIG_DIR / "mask_width_vs_hit_rate_curve.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs.append((path, "mask width vs hit rate curve"))

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    intervals = ctx["intervals"]
    splits = ctx["splits"][SPLIT_KEY]
    shown = 0
    current_candidate = next(c for c in candidates if c["candidate"] == "atan2_px_py_current")
    for frame_idx in test_frames.tolist():
        frame_targets = [
            t
            for t in targets
            if int(t.frame_idx) == int(frame_idx) and int(t.target_id) in intervals and int(t.target_id) in splits
        ]
        if not frame_targets:
            continue
        ax = axes[shown]
        frame = ra_maps[int(frame_idx)]
        ax.imshow(frame.T, aspect="auto", origin="lower", cmap="magma")
        for target in frame_targets:
            tid = int(target.target_id)
            lo, hi, _ = intervals[tid]
            center = angle_bin_for_candidate(target, frame.shape[1], current_candidate)
            color = "cyan" if splits[tid] == "weak" else "white"
            ax.scatter([int(target.range_bin)], [center], s=18, c=color, marker="x")
            clo, chi = centered_bounds(center, 7, frame.shape[1])
            ax.plot([lo, hi, hi, lo, lo], [clo, clo, chi, chi, clo], color=color, linewidth=0.6)
        ax.set_title(f"RA frame {int(frame_idx)}")
        ax.set_xlabel("range bin")
        if shown == 0:
            ax.set_ylabel("angle bin")
        shown += 1
        if shown >= 3:
            break
    path = FIG_DIR / "ra_target_overlay_examples.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs.append((path, "RA target overlay examples"))

    original = next(
        r
        for r in fixed_rows
        if r["candidate"] == "atan2_px_py_current"
        and r["range_mask_name"] == "default"
        and int(r["angle_total_width_bins"]) == 7
    )
    best = max(
        fixed_rows,
        key=lambda r: (
            float(r["weak_target_projection_hit_rate"]),
            float(r["target_projection_hit_rate"]),
            -float(r["excluded_area_ratio"]),
        ),
    )
    labels = ["D5C original weak", "best fixed-PFA weak", "D5C original all", "best fixed-PFA all"]
    vals = [
        float(original["weak_target_projection_hit_rate"]),
        float(best["weak_target_projection_hit_rate"]),
        float(original["target_projection_hit_rate"]),
        float(best["target_projection_hit_rate"]),
    ]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(labels, vals, color=["#b91c1c", "#2563eb", "#ef4444", "#60a5fa"])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Hit rate")
    ax.set_title("D1A+ vs D5C criterion comparison anchor")
    ax.tick_params(axis="x", rotation=20)
    path = FIG_DIR / "d1a_vs_d5c_hit_criterion_comparison.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    outputs.append((path, "D1A+ vs D5C hit criterion comparison"))


def old_summary_rows() -> tuple[dict[str, str], dict[str, str]]:
    d1a_summary = next(r for r in read_csv_rows(PRIOR_D1A_PLUS_DIR / "ra_projection_sanity.csv") if r["row_type"] == "summary")
    d5c_ra = next(r for r in read_csv_rows(PRIOR_D5C_DIR / "d5c_range_rd_ra_separability.csv") if r["representation"] == "RA")
    return d1a_summary, d5c_ra


def make_consistency_rows(
    old_d1a: dict[str, str],
    old_d5c_ra: dict[str, str],
    local_all: dict[str, Any],
    local_test_weak: dict[str, Any],
    original_fixed: dict[str, Any],
    best_fixed: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "source": "D1A+ prior ra_projection_sanity.csv",
            "target_scope": "all valid targets / all frames",
            "hit_criterion": "local RA target patch >= frame p70 and target-background ratio >= 0",
            "candidate": "atan2_px_py_current",
            "formula": "atan2(px, py)",
            "bin_mode": "fftshift_linear_sin",
            "range_mask": "fixed radius 2 bins",
            "angle_mask_total_width_bins": 5,
            "target_count": old_d1a["target_count"],
            "hit_count": old_d1a["ra_projection_hit_count"],
            "hit_rate": old_d1a["ra_projection_hit_rate"],
            "notes": "not fixed-PFA; not weak-only",
        },
        {
            "source": "D5C prior d5c_range_rd_ra_separability.csv",
            "target_scope": "test split / weak targets",
            "hit_criterion": "fixed-PFA 2D RA threshold at target PFA 1e-2",
            "candidate": "atan2_px_py_current",
            "formula": "atan2(px, py)",
            "bin_mode": "fftshift_linear_sin",
            "range_mask": "default object-size range interval",
            "angle_mask_total_width_bins": 7,
            "target_count": old_d5c_ra["weak_target_count"],
            "hit_count": "",
            "hit_rate": old_d5c_ra["weak_target_projection_hit_rate"],
            "notes": "weak-only D5C fixed-PFA smoke",
        },
        {
            "source": "D5C-RCA recomputed D1A-style",
            "target_scope": "all valid targets / all frames",
            "hit_criterion": "local RA target patch >= frame p70 and target-background ratio >= 0",
            "candidate": "atan2_px_py_current",
            "formula": "atan2(px, py)",
            "bin_mode": "fftshift_linear_sin",
            "range_mask": "fixed radius 2 bins",
            "angle_mask_total_width_bins": 5,
            "target_count": local_all["target_count"],
            "hit_count": local_all["hit_count"],
            "hit_rate": local_all["hit_rate"],
            "notes": "recomputed in this script as D1A+ path check",
        },
        {
            "source": "D5C-RCA recomputed D1A-style",
            "target_scope": "D5C test split / weak targets",
            "hit_criterion": "local RA target patch >= frame p70 and target-background ratio >= 0",
            "candidate": "atan2_px_py_current",
            "formula": "atan2(px, py)",
            "bin_mode": "fftshift_linear_sin",
            "range_mask": "fixed radius 2 bins",
            "angle_mask_total_width_bins": 5,
            "target_count": local_test_weak["target_count"],
            "hit_count": local_test_weak["hit_count"],
            "hit_rate": local_test_weak["hit_rate"],
            "notes": "same weak subset but D1A-style criterion",
        },
        {
            "source": "D5C-RCA recomputed original fixed-PFA",
            "target_scope": "D5C test split / weak targets",
            "hit_criterion": "fixed-PFA 2D RA threshold at target PFA 1e-2",
            "candidate": original_fixed["candidate"],
            "formula": original_fixed["formula"],
            "bin_mode": original_fixed["bin_mode"],
            "range_mask": original_fixed["range_mask_name"],
            "angle_mask_total_width_bins": original_fixed["angle_total_width_bins"],
            "target_count": original_fixed["weak_target_count"],
            "hit_count": original_fixed["weak_target_hit_count"],
            "hit_rate": original_fixed["weak_target_projection_hit_rate"],
            "notes": "should match D5C prior 0.0305 if metric path is aligned",
        },
        {
            "source": "D5C-RCA best fixed-PFA candidate",
            "target_scope": "D5C test split / weak targets",
            "hit_criterion": "fixed-PFA 2D RA threshold at target PFA 1e-2",
            "candidate": best_fixed["candidate"],
            "formula": best_fixed["formula"],
            "bin_mode": best_fixed["bin_mode"],
            "range_mask": best_fixed["range_mask_name"],
            "angle_mask_total_width_bins": best_fixed["angle_total_width_bins"],
            "target_count": best_fixed["weak_target_count"],
            "hit_count": best_fixed["weak_target_hit_count"],
            "hit_rate": best_fixed["weak_target_projection_hit_rate"],
            "notes": "best RCA sweep row; smoke-only, not confirmed RA method performance",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str], max_rows: int | None = None) -> str:
    shown = rows[:max_rows] if max_rows is not None else rows
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in shown:
        vals = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                vals.append(f"{value:.4f}")
            else:
                vals.append(str(value))
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep] + body)


def write_reports(
    formula_rows: list[dict[str, Any]],
    axis_rows: list[dict[str, Any]],
    fft_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    breakdown_rows: list[dict[str, Any]],
    consistency_rows: list[dict[str, Any]],
    outputs: list[tuple[Path, str]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    original = next(
        r
        for r in mask_rows
        if r["candidate"] == "atan2_px_py_current"
        and r["range_mask_name"] == "default"
        and int(r["angle_total_width_bins"]) == 7
    )
    best_empirical = max(
        mask_rows,
        key=lambda r: (
            float(r["weak_target_projection_hit_rate"]),
            float(r["target_projection_hit_rate"]),
            -float(r["excluded_area_ratio"]),
        ),
    )
    physical_rows = [r for r in mask_rows if r["candidate"] == "atan2_px_py_current"]
    best_physical = max(
        physical_rows,
        key=lambda r: (
            float(r["weak_target_projection_hit_rate"]),
            float(r["target_projection_hit_rate"]),
            -float(r["excluded_area_ratio"]),
        ),
    )
    best_default = max(
        [r for r in mask_rows if r["range_mask_name"] == "default"],
        key=lambda r: (
            float(r["weak_target_projection_hit_rate"]),
            float(r["target_projection_hit_rate"]),
            -float(r["excluded_area_ratio"]),
        ),
    )
    d1a_recomputed = next(r for r in consistency_rows if r["source"] == "D5C-RCA recomputed D1A-style" and r["target_scope"] == "all valid targets / all frames")
    d1a_prior = next(r for r in consistency_rows if r["source"] == "D1A+ prior ra_projection_sanity.csv")

    weak_gain_physical = float(best_physical["weak_target_projection_hit_rate"]) - float(
        original["weak_target_projection_hit_rate"]
    )
    weak_gain_empirical = float(best_empirical["weak_target_projection_hit_rate"]) - float(
        original["weak_target_projection_hit_rate"]
    )
    best_physical_is_mask_change = (
        best_physical["range_mask_name"] != "default" or int(best_physical["angle_total_width_bins"]) != 7
    )
    original_matches_prior = abs(
        float(original["weak_target_projection_hit_rate"]) - 0.030534351145038167
    ) < 1e-9
    original_angle_error = float(original["mean_abs_peak_angle_error_deg"])
    empirical_angle_error = float(best_empirical["mean_abs_peak_angle_error_deg"])
    empirical_physically_suspicious = (
        best_empirical["candidate"] != "atan2_px_py_current"
        and empirical_angle_error > original_angle_error + 10.0
    )
    if best_physical_is_mask_change and weak_gain_physical >= 0.1:
        verdict = "RA prior failure likely includes mask-width sensitivity under the physically consistent angle formula"
        next_step = "Rerun D5C RA smoke with justified mask after RCA; keep RD as primary until rerun."
        bug_found = True
    elif weak_gain_physical >= 0.05 or weak_gain_empirical >= 0.1:
        verdict = "RA prior result is sensitive but not physically restored"
        next_step = "Keep RA inconclusive; optional RCA follow-up should justify angle-axis physics before any RA rerun."
        bug_found = False
    else:
        verdict = "No clear RA projection bug found; D5C RA remains fixed-PFA-inconclusive"
        next_step = "Continue RD-only supplementary path; keep RA as smoke-only note."
        bug_found = False

    summary = f"""# D5C-RA-RCA self-check summary

阶段：D5C-RA-RCA，仅 RA projection / angle mapping / mask / metric 自检。未训练模型，未进入 D6，未修改 detector 或 fixed-PFA 协议。

Evaluation type: `diagnostic_proxy`。

## 1. 关键结论

- Recomputed original D5C RA weak fixed-PFA hit rate: `{float(original['weak_target_projection_hit_rate']):.6f}`；prior D5C 为 `0.030534`。metric path match: `{original_matches_prior}`。
- Prior D1A+ RA hit rate: `{float(d1a_prior['hit_rate']):.6f}`；本脚本 D1A-style 复算: `{float(d1a_recomputed['hit_rate']):.6f}`。
- Best empirical fixed-PFA RCA row: `{best_empirical['candidate']}`, range mask `{best_empirical['range_mask_name']}`, angle total width `{best_empirical['angle_total_width_bins']}` bins, weak hit rate `{float(best_empirical['weak_target_projection_hit_rate']):.6f}`。
- Best physically plausible row (`atan2(px, py)`, shifted RA map): range mask `{best_physical['range_mask_name']}`, angle total width `{best_physical['angle_total_width_bins']}` bins, weak hit rate `{float(best_physical['weak_target_projection_hit_rate']):.6f}`。
- Empirical best mapping suspicious by angle error: `{empirical_physically_suspicious}`。
- Conservative verdict: **{verdict}**

## 2. Label azimuth formula audit

{markdown_table(sorted(formula_rows, key=lambda r: float(r['d5c_fixed_pfa_weak_projection_hit_rate']), reverse=True), ['candidate', 'formula', 'unit_mode', 'bin_mode', 'axis_sign', 'azimuth_deg_min', 'azimuth_deg_max', 'within_minus90_to_90_ratio', 'd1a_style_projection_hit_rate_all_frames', 'd5c_fixed_pfa_weak_projection_hit_rate', 'mean_abs_peak_angle_error_deg'], max_rows=8)}

## 3. Angle axis / FFT axis audit

{markdown_table(axis_rows, ['axis_name', 'angle_axis_min_deg', 'angle_axis_max_deg', 'angle_bin_count', 'uses_fftshift', 'is_monotonic_increasing', 'center_bin', 'center_angle_deg'])}

{markdown_table(fft_rows, ['check', 'raw_adc_shape', 'sample_axis', 'chirp_axis', 'rx_axis', 'tx_axis', 'virtual_array_shape_after_tx_concat', 'angle_fft_axis_in_range_virt', 'uses_rx_or_virtual_antenna_axis', 'axis_bug_found'])}

## 4. Mask width sensitivity

Original row:

{markdown_table([original], ['candidate', 'range_mask_name', 'angle_total_width_bins', 'target_projection_hit_rate', 'weak_target_projection_hit_rate', 'target_overlap_ratio', 'weak_target_overlap_ratio', 'excluded_area_ratio', 'measured_pfa_at_target_pfa_1e_2'])}

Best empirical row:

{markdown_table([best_empirical], ['candidate', 'range_mask_name', 'angle_total_width_bins', 'target_projection_hit_rate', 'weak_target_projection_hit_rate', 'target_overlap_ratio', 'weak_target_overlap_ratio', 'excluded_area_ratio', 'mean_abs_peak_angle_error_deg', 'measured_pfa_at_target_pfa_1e_2'])}

Best physically plausible row:

{markdown_table([best_physical], ['candidate', 'range_mask_name', 'angle_total_width_bins', 'target_projection_hit_rate', 'weak_target_projection_hit_rate', 'target_overlap_ratio', 'weak_target_overlap_ratio', 'excluded_area_ratio', 'mean_abs_peak_angle_error_deg', 'measured_pfa_at_target_pfa_1e_2'])}

Best default-range row:

{markdown_table([best_default], ['candidate', 'range_mask_name', 'angle_total_width_bins', 'target_projection_hit_rate', 'weak_target_projection_hit_rate', 'target_overlap_ratio', 'weak_target_overlap_ratio', 'excluded_area_ratio', 'measured_pfa_at_target_pfa_1e_2'])}

## 5. D1A+ vs D5C consistency

{markdown_table(consistency_rows, ['source', 'target_scope', 'hit_criterion', 'candidate', 'formula', 'bin_mode', 'range_mask', 'angle_mask_total_width_bins', 'target_count', 'hit_rate', 'notes'])}

## 6. Files

- `ra_label_azimuth_formula_audit.csv`
- `ra_angle_axis_audit.csv`
- `ra_fft_axis_audit.csv`
- `ra_mask_width_sensitivity.csv`
- `ra_projection_hit_breakdown.csv`
- `ra_d1a_vs_d5c_consistency.csv`
- `ra_rca_config.json`

结论限制：这是 projection/mapping/mask RCA，不是 RA method performance，也不是 weak-target weighting 成功证据。
"""

    decision = f"""# D5C-RA-RCA decision

## Verdict

{verdict}

Evaluation type: `diagnostic_proxy`。

## Conservative GO / NO-GO

| Item | Decision |
|---|---|
| RA bug found | {bug_found} |
| Evaluation type | diagnostic_proxy |
| D1A+ vs D5C gap explained | Mostly criterion/scope gap: D1A+ is all-target local contrast sanity; D5C is weak-only fixed-PFA RA threshold smoke. |
| Most reasonable physical formula | `atan2(px, py)` remains the dataset-consistent formula unless a follow-up calibration justifies sign/axis reversal. |
| Best empirical formula in this sweep | `{best_empirical['candidate']}` |
| Best physically plausible row | `{best_physical['candidate']}` / `{best_physical['range_mask_name']}` / `{best_physical['angle_total_width_bins']}` total angle bins |
| Most reasonable angle mask width | Original D5C uses 7 total bins. The physically consistent sweep improves only to `{best_physical['angle_total_width_bins']}` total bins and remains low, so it is sensitivity evidence, not a confirmed fix. |
| Best physically plausible RA projection hit rate | {float(best_physical['target_projection_hit_rate']):.6f} |
| Best physically plausible weak projection hit rate | {float(best_physical['weak_target_projection_hit_rate']):.6f} |
| Best empirical weak projection hit rate | {float(best_empirical['weak_target_projection_hit_rate']):.6f} |
| Prioritize RD? | {'yes' if not bug_found else 'yes, until RA rerun confirms the fix'} |
| Need rerun D5C? | {'yes, RA smoke only, before any RA claim' if bug_found else 'not required for RD-only path; optional only if angle-axis physics is first justified'} |
| D6 allowed? | no |

## Rationale

- The old D1A+ `0.8763` number and D5C `0.0305` number are not the same metric.
- The D5C original RA fixed-PFA path was reproduced in this RCA, so the prior low value is not a dead-code artifact.
- The highest empirical row uses an unshifted-bin hypothesis with much larger angle error; it is a diagnostic warning, not a physically justified fix.
- A higher RCA sweep row is only a candidate projection/mask setting. It does not establish weak-target-preserving training performance.

## Next minimal prompt

```text
/experiment-bridge "D5C-Rerun RA/RD side-by-side smoke only if D5C-RA-RCA selected a physically justified RA projection or mask fix; otherwise continue RD-only supplementary analysis. Keep D6 forbidden, no training beyond smoke, no detector or fixed-PFA protocol changes." -- effort: balanced, assurance: conference-ready, gpu: local, AUTO_PROCEED: true, human checkpoint: false
```
"""

    write_text_versioned(RESULT_DIR / "ra_rca_summary.md", summary, outputs, "D5C RA RCA summary")
    write_text_versioned(RESULT_DIR / "ra_rca_decision.md", decision, outputs, "D5C RA RCA decision")

    decision_data = {
        "verdict": verdict,
        "bug_found": bug_found,
        "original_matches_prior": original_matches_prior,
        "original_weak_hit_rate": float(original["weak_target_projection_hit_rate"]),
        "best_empirical_candidate": best_empirical["candidate"],
        "best_empirical_range_mask_name": best_empirical["range_mask_name"],
        "best_empirical_angle_total_width_bins": int(best_empirical["angle_total_width_bins"]),
        "best_empirical_target_hit_rate": float(best_empirical["target_projection_hit_rate"]),
        "best_empirical_weak_hit_rate": float(best_empirical["weak_target_projection_hit_rate"]),
        "best_physical_candidate": best_physical["candidate"],
        "best_physical_range_mask_name": best_physical["range_mask_name"],
        "best_physical_angle_total_width_bins": int(best_physical["angle_total_width_bins"]),
        "best_physical_target_hit_rate": float(best_physical["target_projection_hit_rate"]),
        "best_physical_weak_hit_rate": float(best_physical["weak_target_projection_hit_rate"]),
        "weak_hit_gain_vs_original_physical": weak_gain_physical,
        "weak_hit_gain_vs_original_empirical": weak_gain_empirical,
        "empirical_physically_suspicious": empirical_physically_suspicious,
        "next_step": next_step,
        "d6_allowed": False,
    }
    return decision_data, best_physical


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[tuple[Path, str]] = []
    np.random.seed(20260627)

    manifest, targets, clean_power, clean_db, _rd = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    val_frames = np.asarray(val_all[: d4.N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[: d4.N_TEST_FRAMES], dtype=int)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    contexts = build_all_range_contexts(clean_db, clean_cfar, targets)
    default_ctx = contexts["default"]
    manifest_rows = read_csv_dicts(MANIFEST_PATH)

    ra_maps, fft_rows = load_all_ra_maps(manifest)
    n_angle = int(ra_maps.shape[2])
    axis_rows = axis_audit_rows(n_angle)

    local_rows_by_candidate: dict[str, list[dict[str, Any]]] = {}
    local_test_rows_by_candidate: dict[str, list[dict[str, Any]]] = {}
    fixed_original_by_candidate: dict[str, dict[str, Any]] = {}
    per_target_by_key: dict[tuple[str, str, int], list[dict[str, Any]]] = {}

    test_set = set(int(x) for x in test_frames.tolist())
    split_map = default_ctx["splits"][SPLIT_KEY]
    for candidate in ANGLE_CANDIDATES:
        local_rows_by_candidate[candidate["candidate"]] = d1a_style_projection_rows(
            ra_maps, targets, candidate, frame_filter=None, split_map=split_map
        )
        local_test_rows_by_candidate[candidate["candidate"]] = d1a_style_projection_rows(
            ra_maps, targets, candidate, frame_filter=test_set, split_map=split_map
        )
        fixed, per_target, _subset_rows = evaluate_ra_fixed_pfa(
            ra_maps,
            targets,
            default_ctx,
            val_frames,
            test_frames,
            candidate,
            angle_total_width=7,
            range_mask_name="default",
        )
        fixed_original_by_candidate[candidate["candidate"]] = fixed
        per_target_by_key[(candidate["candidate"], "default", 7)] = per_target

    formula_rows = formula_distribution_rows(
        targets,
        ANGLE_CANDIDATES,
        local_rows_by_candidate,
        fixed_original_by_candidate,
        manifest_rows,
    )

    mask_rows: list[dict[str, Any]] = []
    breakdown_rows: list[dict[str, Any]] = []
    for candidate in ANGLE_CANDIDATES:
        for range_mask_name in RANGE_MASK_NAMES:
            ctx = contexts[range_mask_name]
            for angle_total in ANGLE_TOTAL_WIDTHS:
                fixed, per_target, subset_rows = evaluate_ra_fixed_pfa(
                    ra_maps,
                    targets,
                    ctx,
                    val_frames,
                    test_frames,
                    candidate,
                    angle_total_width=angle_total,
                    range_mask_name=range_mask_name,
                )
                mask_rows.append(fixed)
                breakdown_rows.extend(subset_rows)
                per_target_by_key[(candidate["candidate"], range_mask_name, int(angle_total))] = per_target

    old_d1a, old_d5c_ra = old_summary_rows()
    current_local_all = aggregate_local_projection(local_rows_by_candidate["atan2_px_py_current"], None)
    current_local_test_weak = aggregate_local_projection(local_test_rows_by_candidate["atan2_px_py_current"], "weak")
    original_fixed = next(
        r
        for r in mask_rows
        if r["candidate"] == "atan2_px_py_current"
        and r["range_mask_name"] == "default"
        and int(r["angle_total_width_bins"]) == 7
    )
    best_fixed = max(
        mask_rows,
        key=lambda r: (
            float(r["weak_target_projection_hit_rate"]),
            float(r["target_projection_hit_rate"]),
            -float(r["excluded_area_ratio"]),
        ),
    )
    consistency_rows = make_consistency_rows(
        old_d1a,
        old_d5c_ra,
        current_local_all,
        current_local_test_weak,
        original_fixed,
        best_fixed,
    )

    write_csv_versioned(RESULT_DIR / "ra_label_azimuth_formula_audit.csv", formula_rows, outputs, "RA label azimuth formula audit")
    write_csv_versioned(RESULT_DIR / "ra_angle_axis_audit.csv", axis_rows, outputs, "RA angle axis audit")
    write_csv_versioned(RESULT_DIR / "ra_fft_axis_audit.csv", fft_rows, outputs, "RA FFT axis audit")
    write_csv_versioned(RESULT_DIR / "ra_mask_width_sensitivity.csv", mask_rows, outputs, "RA mask width sensitivity")
    write_csv_versioned(RESULT_DIR / "ra_projection_hit_breakdown.csv", breakdown_rows, outputs, "RA projection hit breakdown")
    write_csv_versioned(RESULT_DIR / "ra_d1a_vs_d5c_consistency.csv", consistency_rows, outputs, "D1A+ vs D5C consistency")

    plot_outputs(
        targets,
        ANGLE_CANDIDATES,
        mask_rows,
        per_target_by_key,
        ra_maps,
        test_frames,
        default_ctx,
        best_fixed["candidate"],
        outputs,
    )

    decision_data, best = write_reports(
        formula_rows,
        axis_rows,
        fft_rows,
        mask_rows,
        breakdown_rows,
        consistency_rows,
        outputs,
    )

    config = {
        "stage": "D5C-RA-RCA",
        "date": datetime.now().isoformat(),
        "eval_type": "diagnostic_proxy",
        "dataset": str(ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1"),
        "result_dir": str(RESULT_DIR),
        "figure_dir": str(FIG_DIR),
        "python": "G:\\Anaconda\\envs\\cnn_learn\\python.exe",
        "constraints": {
            "entered_d6": False,
            "false_alarm_penalty": False,
            "clean_identity_full_method": False,
            "proposed_full_loss": False,
            "large_model_training": False,
            "detector_modified": False,
            "fixed_pfa_protocol_modified": False,
            "ra_smoke_written_as_confirmed_performance": False,
        },
        "split": {
            "val_frame_count": int(len(val_frames)),
            "test_frame_count": int(len(test_frames)),
            "d5c_split_key": SPLIT_KEY,
        },
        "angle_candidates": ANGLE_CANDIDATES,
        "angle_total_widths": ANGLE_TOTAL_WIDTHS,
        "range_mask_names": RANGE_MASK_NAMES,
        "primary_pfa": PRIMARY_PFA,
        "secondary_pfa": SECONDARY_PFA,
        "decision": decision_data,
        "output_files": [str(path) for path, _desc in outputs],
    }
    write_json_versioned(RESULT_DIR / "ra_rca_config.json", config, outputs, "D5C RA RCA config")
    d5c.append_manifest(outputs)

    print(
        json.dumps(
            {
                "stage": "D5C-RA-RCA",
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "bug_found": decision_data["bug_found"],
                "verdict": decision_data["verdict"],
                "original_weak_hit_rate": decision_data["original_weak_hit_rate"],
                "best_physical_candidate": decision_data["best_physical_candidate"],
                "best_physical_weak_hit_rate": decision_data["best_physical_weak_hit_rate"],
                "best_empirical_candidate": decision_data["best_empirical_candidate"],
                "best_empirical_weak_hit_rate": decision_data["best_empirical_weak_hit_rate"],
                "summary": str(RESULT_DIR / "ra_rca_summary.md"),
                "decision": str(RESULT_DIR / "ra_rca_decision.md"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
