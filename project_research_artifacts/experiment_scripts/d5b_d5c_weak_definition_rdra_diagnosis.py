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
from scipy.io import loadmat

import d4_gao77_strong_baseline_sanity as d4
import d5_diagnosis_weak_weighting_failure as d5diag
import d5_gao77_weak_target_weighted_sanity as d5
from d1a_gao77_clean_fixed_pfa_sanity import (
    EXPECTED_ADC_SHAPE,
    RADAR_DIR,
    ROOT,
    VALID_RANGE_MAX_BIN,
    VALID_RANGE_MIN_BIN,
    ca_cfar_score_1d_np,
    radar_maps,
    write_csv,
    write_json,
)
from d1a_plus_mask_stress_test import target_hit
from d1b_gao77_synthetic_interference_sanity import EPS
from d2a_gao77_small_model_sanity import evaluate_cases


RESULT_DIR = ROOT / "results" / "d5b_d5c_weak_definition_rdra_diagnosis"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5b_d5c_figures"
SUMMARY_PATH = RESULT_DIR / "d5b_d5c_summary.md"
GO_NOGO_PATH = RESULT_DIR / "d5b_d5c_go_nogo_decision.md"
RANDOM_SEED = 20260627
PRIMARY_PFA = 1e-2
SECONDARY_PFA = 1e-3
WEAK_WEIGHT = 2.0
TRAIN_SAMPLE_COUNT = 600


DEFINITIONS: list[dict[str, str]] = [
    {
        "key": "clean_peak_percentile",
        "short": "orig_peak",
        "display": "clean_peak_percentile original",
    },
    {
        "key": "clean_peak_non_overlap",
        "short": "peak_non_overlap",
        "display": "clean_peak_percentile + non-overlap-only",
    },
    {
        "key": "clean_peak_overlap_aware",
        "short": "peak_overlap_aware",
        "display": "clean_peak_percentile + overlap-aware filtering",
    },
    {
        "key": "isolated_target_only",
        "short": "isolated_only",
        "display": "isolated-target-only weak definition",
    },
    {
        "key": "peak_to_local_background_ratio",
        "short": "local_ratio",
        "display": "peak-to-local-background ratio",
    },
    {
        "key": "range_bin_unique_distance",
        "short": "range_unique",
        "display": "range-bin uniqueness / nearest-target-distance filtering",
    },
]


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def f(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value == "" or value is None:
        return default
    return float(value)


def i(row: dict[str, Any], key: str, default: int = 0) -> int:
    value = row.get(key, default)
    if value == "" or value is None:
        return default
    return int(float(value))


def direction_consistent(a: float, b: float) -> bool:
    return (a == 0.0 and b == 0.0) or (a * b >= 0.0)


def finite_mean(values: list[float]) -> float | str:
    vals = [float(v) for v in values if v is not None and np.isfinite(float(v))]
    return float(np.mean(vals)) if vals else ""


def valid_range_mask(n_bins: int) -> np.ndarray:
    mask = np.zeros(n_bins, dtype=bool)
    mask[VALID_RANGE_MIN_BIN : min(VALID_RANGE_MAX_BIN + 1, n_bins)] = True
    return mask


def add_output_version(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8-sig")
    path.write_text(text, encoding="utf-8-sig")
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
    rows = []
    for path, desc in outputs:
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        rows.append(f"| {stamp} | /experiment-bridge | {rel} | implementation | {desc} |")
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")


def relation_stats_for_context(ctx: dict[str, Any], targets: list[Any]) -> dict[int, dict[str, Any]]:
    intervals = ctx["intervals"]
    by_frame: dict[int, list[Any]] = defaultdict(list)
    for target in targets:
        if target.target_id in intervals:
            by_frame[int(target.frame_idx)].append(target)
    stats: dict[int, dict[str, Any]] = {}
    for frame_targets in by_frame.values():
        for target in frame_targets:
            tid = int(target.target_id)
            lo, hi, radius = intervals[tid]
            nearest = math.inf
            exact_bin_conflict = False
            interval_overlap = False
            stronger_overlap = False
            overlap_count = 0
            target_peak = float(ctx["target_values"].get(tid, {}).get("target_peak_db", float("nan")))
            for other in frame_targets:
                oid = int(other.target_id)
                if oid == tid or oid not in intervals:
                    continue
                olo, ohi, _ = intervals[oid]
                dist = abs(int(target.range_bin) - int(other.range_bin))
                nearest = min(nearest, float(dist))
                if dist == 0:
                    exact_bin_conflict = True
                if max(lo, olo) < min(hi, ohi):
                    interval_overlap = True
                    overlap_count += 1
                    other_peak = float(ctx["target_values"].get(oid, {}).get("target_peak_db", float("nan")))
                    if np.isfinite(other_peak) and np.isfinite(target_peak) and other_peak > target_peak + 1.0:
                        stronger_overlap = True
            stats[tid] = {
                "nearest_target_distance_bins": "" if math.isinf(nearest) else nearest,
                "range_bin_conflict": exact_bin_conflict,
                "interval_overlap": interval_overlap,
                "stronger_overlap": stronger_overlap,
                "overlap_partner_count": overlap_count,
                "radius_bins": radius,
            }
    return stats


def assign_split_by_quantiles(values: dict[int, float]) -> dict[int, str]:
    vals = [float(v) for v in values.values() if np.isfinite(float(v))]
    if not vals:
        return {}
    q30, q70 = np.quantile(vals, [0.3, 0.7])
    out: dict[int, str] = {}
    for tid, value in values.items():
        v = float(value)
        if v <= q30:
            out[tid] = "weak"
        elif v <= q70:
            out[tid] = "mid"
        else:
            out[tid] = "strong"
    return out


def remap_removed_weak_to_mid(original: dict[int, str], weak_ids: set[int]) -> dict[int, str]:
    out: dict[int, str] = {}
    for tid, split in original.items():
        if tid in weak_ids:
            out[tid] = "weak"
        elif split == "weak":
            out[tid] = "mid"
        else:
            out[tid] = split
    return out


def extend_context_splits(contexts: dict[str, dict[str, Any]], targets: list[Any]) -> dict[str, dict[int, dict[str, Any]]]:
    all_relation_stats: dict[str, dict[int, dict[str, Any]]] = {}
    for mask_name, ctx in contexts.items():
        relation = relation_stats_for_context(ctx, targets)
        all_relation_stats[mask_name] = relation
        original = dict(ctx["splits"]["clean_peak_percentile"])
        original_weak = {tid for tid, split in original.items() if split == "weak"}
        non_overlap = set(ctx["non_overlap_ids"])

        non_overlap_weak = original_weak & non_overlap
        ctx["splits"]["clean_peak_non_overlap"] = remap_removed_weak_to_mid(original, non_overlap_weak)

        overlap_aware_weak = {
            tid
            for tid in original_weak
            if not relation.get(tid, {}).get("stronger_overlap", False)
            and not relation.get(tid, {}).get("range_bin_conflict", False)
            and float(relation.get(tid, {}).get("nearest_target_distance_bins", 99.0) or 99.0) >= 2.0
        }
        ctx["splits"]["clean_peak_overlap_aware"] = remap_removed_weak_to_mid(original, overlap_aware_weak)

        isolated_weak = {
            tid
            for tid in original_weak
            if tid in non_overlap
            and not relation.get(tid, {}).get("interval_overlap", False)
            and float(relation.get(tid, {}).get("nearest_target_distance_bins", 99.0) or 99.0) >= 6.0
        }
        ctx["splits"]["isolated_target_only"] = remap_removed_weak_to_mid(original, isolated_weak)

        ratio_values = {
            int(tid): float(values["target_background_ratio_db"])
            for tid, values in ctx["target_values"].items()
            if values.get("valid_projection") and values.get("target_background_ratio_db") != ""
        }
        ctx["splits"]["peak_to_local_background_ratio"] = assign_split_by_quantiles(ratio_values)

        unique_distance_weak = {
            tid
            for tid in original_weak
            if not relation.get(tid, {}).get("range_bin_conflict", False)
            and float(relation.get(tid, {}).get("nearest_target_distance_bins", 99.0) or 99.0) >= 4.0
        }
        ctx["splits"]["range_bin_unique_distance"] = remap_removed_weak_to_mid(original, unique_distance_weak)
    return all_relation_stats


def weak_definition_audit_rows(
    ctx: dict[str, Any], relation: dict[int, dict[str, Any]]
) -> list[dict[str, Any]]:
    original = ctx["splits"]["clean_peak_percentile"]
    original_weak = {tid for tid, split in original.items() if split == "weak"}
    non_overlap = set(ctx["non_overlap_ids"])
    rows = []
    for spec in DEFINITIONS:
        key = spec["key"]
        splits = ctx["splits"][key]
        weak_ids = {tid for tid, split in splits.items() if split == "weak"}
        mid_ids = {tid for tid, split in splits.items() if split == "mid"}
        strong_ids = {tid for tid, split in splits.items() if split == "strong"}
        union = weak_ids | original_weak
        values = ctx["target_values"]
        weak_values = [values[tid] for tid in weak_ids if tid in values]
        nearest = [
            float(relation[tid]["nearest_target_distance_bins"])
            for tid in weak_ids
            if tid in relation and relation[tid]["nearest_target_distance_bins"] != ""
        ]
        conflict_n = sum(1 for tid in weak_ids if relation.get(tid, {}).get("range_bin_conflict", False))
        interval_overlap_n = sum(1 for tid in weak_ids if relation.get(tid, {}).get("interval_overlap", False))
        rows.append(
            {
                "definition": key,
                "definition_display": spec["display"],
                "weak_n": len(weak_ids),
                "mid_n": len(mid_ids),
                "strong_n": len(strong_ids),
                "weak_overlap_mask_ratio": (sum(1 for tid in weak_ids if tid not in non_overlap) / max(len(weak_ids), 1)),
                "weak_non_overlap_count": sum(1 for tid in weak_ids if tid in non_overlap),
                "jaccard_with_clean_peak_percentile": len(weak_ids & original_weak) / max(len(union), 1),
                "mean_clean_peak_db": finite_mean([float(v["target_peak_db"]) for v in weak_values]),
                "mean_cfar_margin_db": finite_mean([float(v["cfar_margin_db"]) for v in weak_values]),
                "mean_peak_to_local_background_ratio_db": finite_mean(
                    [float(v["target_background_ratio_db"]) for v in weak_values]
                ),
                "range_bin_conflict_ratio": conflict_n / max(len(weak_ids), 1),
                "interval_overlap_ratio": interval_overlap_n / max(len(weak_ids), 1),
                "average_nearest_target_distance_bins": finite_mean(nearest),
                "weak_ids_preview": ";".join(str(x) for x in sorted(weak_ids)[:20]),
            }
        )
    return rows


def pick_metric(
    rows: list[dict[str, Any]],
    input_type: str,
    sir_name: str = "",
    mask_name: str = "default",
    split_definition: str = "clean_peak_percentile",
    pfa: float = PRIMARY_PFA,
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


def rename_training_rows(rows: list[dict[str, Any]], label: str, definition: str) -> list[dict[str, Any]]:
    renamed = []
    for row in rows:
        new_row = dict(row)
        new_row["baseline"] = label
        new_row["definition"] = definition
        renamed.append(new_row)
    return renamed


def rename_training_metrics(metrics: dict[str, Any], label: str, definition: str) -> dict[str, Any]:
    out = dict(metrics)
    out["baseline"] = label
    out["definition"] = definition
    return out


def build_repaired_result_rows(
    audit_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    label_by_definition: dict[str, str],
) -> list[dict[str, Any]]:
    audit_lookup = {r["definition"]: r for r in audit_rows}
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    rows = []
    for spec in DEFINITIONS:
        definition = spec["key"]
        label = label_by_definition[definition]
        weak_input = f"{label}_output"
        weak_clean = f"{label}_model_clean"
        try:
            balanced = pick_metric(fixed_rows, "balanced_mild_output", "medium", split_definition=definition)
            weak = pick_metric(fixed_rows, weak_input, "medium", split_definition=definition)
            balanced_narrow = pick_metric(
                fixed_rows, "balanced_mild_output", "medium", mask_name="narrow", split_definition=definition
            )
            weak_narrow = pick_metric(fixed_rows, weak_input, "medium", mask_name="narrow", split_definition=definition)
            balanced_non = pick_metric(
                fixed_rows,
                "balanced_mild_output",
                "medium",
                split_definition=definition,
                scope="non_overlap_only",
            )
            weak_non = pick_metric(fixed_rows, weak_input, "medium", split_definition=definition, scope="non_overlap_only")
            weak_clean_metric = pick_metric(fixed_rows, weak_clean, split_definition=definition)
        except KeyError as exc:
            rows.append(
                {
                    **audit_lookup[definition],
                    "train_label": label,
                    "status": f"missing_metric: {exc}",
                }
            )
            continue
        default_delta = f(weak, "weak_pd") - f(balanced, "weak_pd")
        narrow_delta = f(weak_narrow, "weak_pd") - f(balanced_narrow, "weak_pd")
        non_delta = f(weak_non, "weak_pd") - f(balanced_non, "weak_pd")
        clean_rec = recon_lookup.get((weak_clean, ""), {})
        clean_no_harm = (
            f(clean_rec, "mse_db_to_clean", 999.0) < 3.0
            and f(weak_clean_metric, "measured_pfa", 999.0) < 0.08
            and f(weak_clean_metric, "target_peak_abs_bias_db_mean", 999.0) < 2.0
        )
        rows.append(
            {
                **audit_lookup[definition],
                "train_label": label,
                "status": "DONE",
                "baseline": "balanced_mild",
                "weak_weighting": "weak_peak_w2p0",
                "target_pfa": PRIMARY_PFA,
                "sir_name": "medium",
                "mask_name": "default",
                "target_scope": "all",
                "balanced_mild_weak_n": balanced["weak_n"],
                "weak_weighting_weak_n": weak["weak_n"],
                "balanced_mild_weak_hits": balanced["weak_hits"],
                "weak_weighting_weak_hits": weak["weak_hits"],
                "balanced_mild_weak_pd": balanced["weak_pd"],
                "weak_weighting_weak_pd": weak["weak_pd"],
                "weak_pd_delta": default_delta,
                "weak_hit_delta": i(weak, "weak_hits") - i(balanced, "weak_hits"),
                "balanced_mild_mid_pd": balanced["mid_pd"],
                "weak_weighting_mid_pd": weak["mid_pd"],
                "mid_pd_delta": f(weak, "mid_pd") - f(balanced, "mid_pd"),
                "balanced_mild_strong_pd": balanced["strong_pd"],
                "weak_weighting_strong_pd": weak["strong_pd"],
                "strong_pd_delta": f(weak, "strong_pd") - f(balanced, "strong_pd"),
                "balanced_mild_overall_pd": balanced["overall_pd"],
                "weak_weighting_overall_pd": weak["overall_pd"],
                "measured_pfa": weak["measured_pfa"],
                "balanced_mild_measured_pfa": balanced["measured_pfa"],
                "measured_pfa_delta": f(weak, "measured_pfa") - f(balanced, "measured_pfa"),
                "false_alarm_count_delta": i(weak, "false_alarm_count") - i(balanced, "false_alarm_count"),
                "weak_weighting_false_alarm_count": weak["false_alarm_count"],
                "balanced_mild_false_alarm_count": balanced["false_alarm_count"],
                "clean_input_no_harm": clean_no_harm,
                "model_clean_mse_db_to_clean": clean_rec.get("mse_db_to_clean", ""),
                "model_clean_measured_pfa": weak_clean_metric.get("measured_pfa", ""),
                "default_mask_weak_pd_delta": default_delta,
                "narrow_mask_weak_pd_delta": narrow_delta,
                "default_vs_narrow_mask_consistency": direction_consistent(default_delta, narrow_delta),
                "all_targets_weak_pd_delta": default_delta,
                "non_overlap_only_weak_pd_delta": non_delta,
                "all_vs_non_overlap_consistency": direction_consistent(default_delta, non_delta),
                "non_overlap_weak_hit_delta": i(weak_non, "weak_hits") - i(balanced_non, "weak_hits"),
                "meets_min_weak_pd_gain_bar": default_delta >= 0.02,
                "meets_min_hit_delta_bar": (i(weak, "weak_hits") - i(balanced, "weak_hits")) >= 5,
                "pfa_not_increased": f(weak, "measured_pfa") <= f(balanced, "measured_pfa") + 1e-12,
                "false_alarm_not_increased": i(weak, "false_alarm_count") <= i(balanced, "false_alarm_count"),
            }
        )
    return rows


def angle_bin_from_target(target: Any, n_angle: int) -> int:
    sin_theta = math.sin(math.radians(float(target.azimuth_deg)))
    return int(round((sin_theta + 1.0) * 0.5 * (n_angle - 1)))


def rects_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    ar0, ar1, ac0, ac1 = a
    br0, br1, bc0, bc1 = b
    return max(ar0, br0) < min(ar1, br1) and max(ac0, bc0) < min(ac1, bc1)


def range_representation_rows(
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    ctx: dict[str, Any],
    targets: list[Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    split_key: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    scores = ca_cfar_score_1d_np(clean_power)
    background_mask = ctx["background_mask"]
    intervals = ctx["intervals"]
    splits = ctx["splits"][split_key]
    test_set = set(int(x) for x in test_frames.tolist())
    thresholds = {
        pfa: float(np.quantile(scores[val_frames][background_mask[val_frames]], 1.0 - pfa))
        for pfa in [PRIMARY_PFA, SECONDARY_PFA]
    }
    pfa_rows = {}
    for pfa, threshold in thresholds.items():
        detections = scores >= threshold
        bg_test = background_mask[test_frames]
        pfa_rows[pfa] = {
            "threshold": threshold,
            "measured_pfa": float(np.logical_and(detections[test_frames], bg_test).sum() / max(int(bg_test.sum()), 1)),
        }

    per_target = []
    rect_by_target: dict[int, tuple[int, int, int, int]] = {}
    detections_primary = scores >= thresholds[PRIMARY_PFA]
    for target in targets:
        tid = int(target.target_id)
        if int(target.frame_idx) not in test_set or tid not in intervals or tid not in splits:
            continue
        lo, hi, _ = intervals[tid]
        frame_db = clean_db[int(target.frame_idx)]
        peak = float(np.max(frame_db[lo:hi]))
        values = ctx["target_values"].get(tid, {})
        contrast = float(values.get("target_background_ratio_db", 0.0))
        hit = target_hit(detections_primary, target, intervals)
        rect_by_target[tid] = (lo, hi, 0, 1)
        per_target.append(
            {
                "target_id": tid,
                "frame_idx": int(target.frame_idx),
                "split": splits[tid],
                "peak_score": peak,
                "local_background": float(values.get("neighbor_mean_db", 0.0)),
                "contrast_db": contrast,
                "fixed_pfa_hit": hit,
            }
        )
    row = summarize_representation("range_only", per_target, rect_by_target, pfa_rows, targets)
    return row, per_target


def compute_2d_representation(
    representation: str,
    manifest: list[dict[str, str]],
    targets: list[Any],
    ctx: dict[str, Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    split_key: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[int, np.ndarray]]:
    frame_indices = np.asarray(sorted(set(val_frames.tolist()) | set(test_frames.tolist())), dtype=int)
    frame_to_pos = {int(frame): pos for pos, frame in enumerate(frame_indices.tolist())}
    test_frame_set = set(int(x) for x in test_frames.tolist())
    maps: list[np.ndarray] = []
    sample_maps: dict[int, np.ndarray] = {}
    for frame_idx in frame_indices.tolist():
        adc = loadmat(RADAR_DIR / manifest[int(frame_idx)]["new_radar_file"])["adcData"]
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"unexpected adcData shape {adc.shape}")
        _rp, rd_map, ra_map = radar_maps(adc)
        rep_map = rd_map if representation == "rd" else ra_map
        maps.append(rep_map.astype(np.float32))
        if int(frame_idx) in set(test_frames[:8].tolist()):
            sample_maps[int(frame_idx)] = rep_map.astype(np.float32)
    score = np.stack(maps, axis=0)
    n_frames, n_range, n_other = score.shape
    target_mask = np.zeros((n_frames, n_range, n_other), dtype=bool)
    guard_mask = np.zeros((n_frames, n_range, n_other), dtype=bool)
    intervals = ctx["intervals"]
    splits = ctx["splits"][split_key]
    per_target: list[dict[str, Any]] = []
    rect_by_target: dict[int, tuple[int, int, int, int]] = {}
    valid_range = valid_range_mask(n_range)[:, None]
    frame_set = set(int(x) for x in frame_indices.tolist())

    for target in targets:
        tid = int(target.target_id)
        frame_idx = int(target.frame_idx)
        if frame_idx not in frame_set or tid not in intervals or tid not in splits:
            continue
        pos = frame_to_pos[frame_idx]
        lo, hi, _radius = intervals[tid]
        if representation == "rd":
            sub = score[pos, lo:hi, :]
            if sub.size == 0:
                continue
            peak_flat = int(np.argmax(sub))
            _peak_r, peak_c = np.unravel_index(peak_flat, sub.shape)
            clo, chi = max(0, peak_c - 2), min(n_other, peak_c + 3)
            gclo, gchi = max(0, peak_c - 5), min(n_other, peak_c + 6)
        else:
            center = angle_bin_from_target(target, n_other)
            clo, chi = max(0, center - 3), min(n_other, center + 4)
            gclo, gchi = max(0, center - 6), min(n_other, center + 7)
        rlo, rhi = lo, hi
        grlo, grhi = max(0, lo - 4), min(n_range, hi + 4)
        target_mask[pos, rlo:rhi, clo:chi] = True
        guard_mask[pos, grlo:grhi, gclo:gchi] = True
        rect = (rlo, rhi, clo, chi)
        target_values = score[pos, rlo:rhi, clo:chi]
        local_guard = np.zeros((n_range, n_other), dtype=bool)
        local_guard[grlo:grhi, gclo:gchi] = True
        local_target = np.zeros((n_range, n_other), dtype=bool)
        local_target[rlo:rhi, clo:chi] = True
        local_bg = np.logical_and(local_guard, ~local_target)
        local_bg = np.logical_and(local_bg, valid_range)
        bg_values = score[pos][local_bg]
        peak = float(np.max(target_values)) if target_values.size else float("nan")
        bg_med = float(np.median(bg_values)) if bg_values.size else float(np.median(score[pos][valid_range[:, 0]]))
        if frame_idx in test_frame_set:
            rect_by_target[tid] = rect
            per_target.append(
                {
                    "target_id": tid,
                    "frame_idx": frame_idx,
                    "split": splits[tid],
                    "peak_score": peak,
                    "local_background": bg_med,
                    "contrast_db": peak - bg_med,
                    "fixed_pfa_hit": False,
                }
            )

    guard_ring = np.logical_and(guard_mask, ~target_mask)
    valid = np.broadcast_to(valid_range, target_mask.shape).copy()
    background_mask = np.logical_and(valid, ~np.logical_or(target_mask, guard_ring))
    pfa_rows = {}
    val_pos = np.asarray([frame_to_pos[int(x)] for x in val_frames.tolist() if int(x) in frame_to_pos], dtype=int)
    test_pos = np.asarray([frame_to_pos[int(x)] for x in test_frames.tolist() if int(x) in frame_to_pos], dtype=int)
    val_bg = score[val_pos][background_mask[val_pos]]
    for pfa in [PRIMARY_PFA, SECONDARY_PFA]:
        threshold = float(np.quantile(val_bg, 1.0 - pfa))
        det = score >= threshold
        test_bg = background_mask[test_pos]
        measured = float(np.logical_and(det[test_pos], test_bg).sum() / max(int(test_bg.sum()), 1))
        pfa_rows[pfa] = {"threshold": threshold, "measured_pfa": measured}
        if pfa == PRIMARY_PFA:
            hit_by_tid = {}
            for tid, rect in rect_by_target.items():
                target = next(t for t in targets if int(t.target_id) == tid)
                if int(target.frame_idx) not in frame_to_pos:
                    continue
                pos = frame_to_pos[int(target.frame_idx)]
                rlo, rhi, clo, chi = rect
                hit_by_tid[tid] = bool(det[pos, rlo:rhi, clo:chi].any())
            for item in per_target:
                item["fixed_pfa_hit"] = hit_by_tid.get(int(item["target_id"]), False)

    row = summarize_representation(representation.upper(), per_target, rect_by_target, pfa_rows, targets)
    return row, per_target, sample_maps


def summarize_representation(
    name: str,
    per_target: list[dict[str, Any]],
    rect_by_target: dict[int, tuple[int, int, int, int]],
    pfa_rows: dict[float, dict[str, float]],
    targets: list[Any],
) -> dict[str, Any]:
    target_by_id = {int(t.target_id): t for t in targets}
    test_ids = [int(r["target_id"]) for r in per_target]
    weak_ids = [int(r["target_id"]) for r in per_target if r["split"] == "weak"]
    overlapped_targets: set[int] = set()
    by_frame: dict[int, list[int]] = defaultdict(list)
    for tid in test_ids:
        by_frame[int(target_by_id[tid].frame_idx)].append(tid)
    for tids in by_frame.values():
        for ix, tid in enumerate(tids):
            for oid in tids[ix + 1 :]:
                if rects_overlap(rect_by_target[tid], rect_by_target[oid]):
                    overlapped_targets.add(tid)
                    overlapped_targets.add(oid)
    weak_overlap = [tid for tid in weak_ids if tid in overlapped_targets]
    hits = sum(1 for r in per_target if r["fixed_pfa_hit"])
    weak_hits = sum(1 for r in per_target if r["split"] == "weak" and r["fixed_pfa_hit"])
    contrasts = [float(r["contrast_db"]) for r in per_target if np.isfinite(float(r["contrast_db"]))]
    weak_contrasts = [
        float(r["contrast_db"]) for r in per_target if r["split"] == "weak" and np.isfinite(float(r["contrast_db"]))
    ]
    pfa_1 = pfa_rows[PRIMARY_PFA]["measured_pfa"]
    pfa_3 = pfa_rows[SECONDARY_PFA]["measured_pfa"]
    sanity = pfa_1 <= PRIMARY_PFA * 2.0 + 0.002 and pfa_3 <= SECONDARY_PFA * 3.0 + 0.001
    return {
        "representation": name,
        "score_type": "CA-CFAR ratio" if name == "range_only" else "2D map dB threshold smoke",
        "target_projection_hit_rate": hits / max(len(per_target), 1),
        "weak_target_projection_hit_rate": weak_hits / max(len(weak_ids), 1),
        "target_overlap_ratio": len(overlapped_targets) / max(len(test_ids), 1),
        "weak_target_overlap_ratio": len(weak_overlap) / max(len(weak_ids), 1),
        "target_count": len(test_ids),
        "weak_target_count": len(weak_ids),
        "separability_proxy_db": float(np.mean(contrasts)) if contrasts else "",
        "weak_separability_proxy_db": float(np.mean(weak_contrasts)) if weak_contrasts else "",
        "background_target_contrast_db": float(np.median(contrasts)) if contrasts else "",
        "fixed_pfa_calibration_sanity": "pass" if sanity else "warn",
        "threshold_at_pfa_1e_2": pfa_rows[PRIMARY_PFA]["threshold"],
        "measured_pfa_at_target_pfa_1e_2": pfa_1,
        "threshold_at_pfa_1e_3": pfa_rows[SECONDARY_PFA]["threshold"],
        "measured_pfa_at_target_pfa_1e_3": pfa_3,
        "supports_followup_rdra_training": "smoke_only_no" if name == "range_only" else "",
        "scope_note": "clean-map projection smoke; RD has no Doppler labels; RA uses label azimuth projection",
    }


def update_rdra_support_flags(rows: list[dict[str, Any]]) -> None:
    range_row = next(r for r in rows if r["representation"] == "range_only")
    range_sep = f(range_row, "weak_separability_proxy_db")
    range_overlap = f(range_row, "weak_target_overlap_ratio")
    range_weak_hit = f(range_row, "weak_target_projection_hit_rate")
    for row in rows:
        if row["representation"] == "range_only":
            continue
        sep_gain = f(row, "weak_separability_proxy_db") - range_sep
        overlap_drop = range_overlap - f(row, "weak_target_overlap_ratio")
        weak_hit_delta = f(row, "weak_target_projection_hit_rate") - range_weak_hit
        sane = row["fixed_pfa_calibration_sanity"] == "pass"
        support = bool(sane and sep_gain >= 1.0 and overlap_drop >= 0.05 and weak_hit_delta >= -0.05)
        row["weak_separability_gain_vs_range_db"] = sep_gain
        row["weak_overlap_drop_vs_range"] = overlap_drop
        row["weak_projection_hit_delta_vs_range"] = weak_hit_delta
        row["supports_followup_rdra_training"] = "feasibility_smoke_yes" if support else "feasibility_smoke_inconclusive"


def plot_d5b_figures(
    audit_rows: list[dict[str, Any]],
    result_rows: list[dict[str, Any]],
    clean_db: np.ndarray,
    targets: list[Any],
    ctx: dict[str, Any],
    test_frames: np.ndarray,
) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    labels = [r["definition_display"].replace("clean_peak_percentile + ", "+\n") for r in audit_rows]
    x = np.arange(len(audit_rows))
    plt.figure(figsize=(11, 5), dpi=150)
    plt.bar(x - 0.2, [float(r["weak_n"]) for r in audit_rows], 0.4, label="weak_n")
    plt.bar(x + 0.2, [float(r["weak_non_overlap_count"]) for r in audit_rows], 0.4, label="weak non-overlap")
    plt.xticks(x, labels, rotation=20, ha="right")
    plt.ylabel("Target count")
    plt.title("Weak definition overlap comparison")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "weak_definition_overlap_comparison.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    plt.figure(figsize=(11, 5), dpi=150)
    plt.plot(labels, [float(r["weak_overlap_mask_ratio"]) for r in audit_rows], marker="o", label="overlap-mask ratio")
    plt.plot(labels, [float(r["jaccard_with_clean_peak_percentile"]) for r in audit_rows], marker="o", label="Jaccard vs original")
    plt.ylim(-0.02, 1.02)
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Ratio")
    plt.title("Weak definition stability ratios")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "weak_definition_stability_ratios.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    good_rows = [r for r in result_rows if r.get("status") == "DONE"]
    labels2 = [r["definition_display"].replace("clean_peak_percentile + ", "+\n") for r in good_rows]
    plt.figure(figsize=(11, 5), dpi=150)
    xs = np.arange(len(good_rows))
    plt.bar(xs, [float(r["weak_pd_delta"]) for r in good_rows], color="#2563eb")
    plt.axhline(0.02, color="red", linestyle="--", linewidth=1, label="GO weak Pd delta bar")
    plt.xticks(xs, labels2, rotation=20, ha="right")
    plt.ylabel("Weak Pd delta vs balanced_mild")
    plt.title("Fixed-PFA weak Pd sanity")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "fixed_pfa_pd_sanity.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    plt.figure(figsize=(11, 5), dpi=150)
    plt.bar(xs - 0.2, [float(r["measured_pfa"]) for r in good_rows], 0.4, label="weak weighting PFA")
    plt.bar(xs + 0.2, [float(r["balanced_mild_measured_pfa"]) for r in good_rows], 0.4, label="balanced_mild PFA")
    plt.axhline(PRIMARY_PFA, color="black", linestyle="--", linewidth=1)
    plt.xticks(xs, labels2, rotation=20, ha="right")
    plt.ylabel("Measured PFA")
    plt.title("Fixed-PFA threshold sanity")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "fixed_pfa_threshold_pfa_sanity.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    intervals = ctx["intervals"]
    test_set = set(int(x) for x in test_frames.tolist())
    candidate_frames = []
    for frame_idx in test_set:
        tids = [int(t.target_id) for t in targets if int(t.frame_idx) == frame_idx and int(t.target_id) in intervals]
        overlap_count = 0
        for a_ix, tid in enumerate(tids):
            for oid in tids[a_ix + 1 :]:
                lo, hi, _ = intervals[tid]
                olo, ohi, _ = intervals[oid]
                if max(lo, olo) < min(hi, ohi):
                    overlap_count += 1
        if overlap_count:
            candidate_frames.append((overlap_count, frame_idx, tids))
    if candidate_frames:
        _count, frame_idx, tids = sorted(candidate_frames, reverse=True)[0]
        plt.figure(figsize=(10, 4), dpi=150)
        xbins = np.arange(clean_db.shape[1])
        plt.plot(xbins, clean_db[frame_idx], linewidth=1.2)
        for tid in tids[:12]:
            target = next(t for t in targets if int(t.target_id) == tid)
            lo, hi, _ = intervals[tid]
            plt.axvspan(lo, hi, alpha=0.2)
            plt.text((lo + hi) / 2, np.max(clean_db[frame_idx]) - 3, str(tid), fontsize=7, ha="center")
            plt.axvline(int(target.range_bin), color="red", linewidth=0.5)
        plt.xlabel("Range bin")
        plt.ylabel("Power (dB)")
        plt.title(f"Range-only overlap example: frame {frame_idx}")
        plt.tight_layout()
        out = FIG_DIR / "range_only_overlap_examples.png"
        plt.savefig(out)
        plt.close()
        outputs.append(out)
    return outputs


def plot_d5c_figures(
    d5c_rows: list[dict[str, Any]],
    sample_rd: dict[int, np.ndarray],
    sample_ra: dict[int, np.ndarray],
    targets: list[Any],
    ctx: dict[str, Any],
    test_frames: np.ndarray,
) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    labels = [r["representation"] for r in d5c_rows]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(r["weak_target_overlap_ratio"]) for r in d5c_rows], label="weak overlap")
    plt.plot(labels, [float(r["weak_separability_proxy_db"]) for r in d5c_rows], marker="o", color="black", label="weak sep proxy dB")
    plt.ylabel("Ratio / dB")
    plt.title("RD/RA separability smoke")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "rd_ra_separability_smoke_summary.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot(labels, [float(r["measured_pfa_at_target_pfa_1e_2"]) for r in d5c_rows], marker="o", label="target 1e-2")
    plt.plot(labels, [float(r["measured_pfa_at_target_pfa_1e_3"]) for r in d5c_rows], marker="o", label="target 1e-3")
    plt.axhline(PRIMARY_PFA, color="#777", linestyle="--", linewidth=0.8)
    plt.axhline(SECONDARY_PFA, color="#aaa", linestyle=":", linewidth=0.8)
    plt.ylabel("Measured PFA")
    plt.title("RD/RA fixed-PFA calibration smoke")
    plt.legend()
    plt.tight_layout()
    out = FIG_DIR / "rd_ra_fixed_pfa_smoke.png"
    plt.savefig(out)
    plt.close()
    outputs.append(out)

    shared = [idx for idx in test_frames.tolist() if int(idx) in sample_rd and int(idx) in sample_ra]
    if shared:
        frame_idx = int(shared[0])
        fig, axes = plt.subplots(1, 2, figsize=(11, 4), dpi=150)
        axes[0].imshow(sample_rd[frame_idx].T, aspect="auto", origin="lower", cmap="magma")
        axes[0].set_title(f"RD smoke frame {frame_idx}")
        axes[0].set_xlabel("Range bin")
        axes[0].set_ylabel("Doppler bin")
        axes[1].imshow(sample_ra[frame_idx].T, aspect="auto", origin="lower", cmap="magma")
        axes[1].set_title(f"RA smoke frame {frame_idx}")
        axes[1].set_xlabel("Range bin")
        axes[1].set_ylabel("Angle bin")
        intervals = ctx["intervals"]
        for target in targets:
            if int(target.frame_idx) != frame_idx or int(target.target_id) not in intervals:
                continue
            lo, hi, _ = intervals[int(target.target_id)]
            axes[0].axvline(int(target.range_bin), color="cyan", linewidth=0.6)
            angle_bin = angle_bin_from_target(target, sample_ra[frame_idx].shape[1])
            axes[1].scatter([int(target.range_bin)], [angle_bin], s=16, c="cyan", marker="x")
            axes[1].axvspan(lo, hi, color="cyan", alpha=0.08)
        plt.tight_layout()
        out = FIG_DIR / "rd_ra_separability_smoke_examples.png"
        plt.savefig(out)
        plt.close(fig)
        outputs.append(out)
    return outputs


def markdown_table(rows: list[dict[str, Any]], cols: list[str], max_rows: int | None = None) -> str:
    use_rows = rows[:max_rows] if max_rows else rows
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in use_rows:
        vals = []
        for col in cols:
            val = row.get(col, "")
            if isinstance(val, float):
                vals.append(f"{val:.4f}")
            else:
                vals.append(str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def make_decision_rows(d5b_rows: list[dict[str, Any]], d5c_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    done = [r for r in d5b_rows if r.get("status") == "DONE"]
    weak_go = [
        r
        for r in done
        if r["definition"] != "clean_peak_percentile"
        and r["meets_min_weak_pd_gain_bar"]
        and r["meets_min_hit_delta_bar"]
        and r["pfa_not_increased"]
        and r["false_alarm_not_increased"]
        and r["clean_input_no_harm"]
        and r["default_vs_narrow_mask_consistency"]
        and r["all_vs_non_overlap_consistency"]
    ]
    range_row = next(r for r in d5c_rows if r["representation"] == "range_only")
    rdra_yes = [r for r in d5c_rows if r.get("supports_followup_rdra_training") == "feasibility_smoke_yes"]
    best = max(done, key=lambda r: (float(r["weak_pd_delta"]), int(r["weak_hit_delta"]))) if done else {}
    final_route = "record_range_only_negative_result"
    if weak_go:
        final_route = "continue_repaired_weak_weighting_with_confirmation_needed"
    elif rdra_yes and float(range_row["weak_target_overlap_ratio"]) > 0.25:
        final_route = "conditional_switch_to_rdra_smoke_followup"
    rows = [
        {
            "decision_item": "continue_weak_weighting",
            "verdict": "NO-GO" if not weak_go else "CONDITIONAL-GO",
            "evidence": (
                f"best_definition={best.get('definition', 'NA')}, "
                f"weak_pd_delta={float(best.get('weak_pd_delta', 0.0)):.4f}, "
                f"weak_hit_delta={best.get('weak_hit_delta', 'NA')}"
            ),
            "route": final_route,
        },
        {
            "decision_item": "switch_to_rdra",
            "verdict": "CONDITIONAL-SMOKE" if rdra_yes else "NO-GO/INCONCLUSIVE",
            "evidence": "; ".join(
                f"{r['representation']}: sep_gain={float(r.get('weak_separability_gain_vs_range_db', 0.0)):.2f}, "
                f"overlap_drop={float(r.get('weak_overlap_drop_vs_range', 0.0)):.3f}"
                for r in d5c_rows
                if r["representation"] != "range_only"
            ),
            "route": final_route,
        },
        {
            "decision_item": "enter_D6",
            "verdict": "NO-GO",
            "evidence": "D5B-D5C is restricted to definition repair and RD/RA feasibility; no false alarm penalty tested.",
            "route": final_route,
        },
    ]
    return rows


def write_reports(
    audit_rows: list[dict[str, Any]],
    d5b_rows: list[dict[str, Any]],
    d5c_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    outputs: list[tuple[Path, str]],
) -> tuple[Path, Path]:
    best = max(
        [r for r in d5b_rows if r.get("status") == "DONE"],
        key=lambda r: (float(r["weak_pd_delta"]), int(r["weak_hit_delta"])),
    )
    rdra_rows = [r for r in d5c_rows if r["representation"] != "range_only"]
    summary = f"""# D5B-D5C weak definition / RD-RA diagnosis

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

阶段：D5B-D5C。没有进入 D6，没有加入 false alarm penalty，没有修改 detector 或 CFAR 主评价协议，没有引入新大模型或 3 seeds 正式实验。

## 1. 执行边界

- 主 baseline：`balanced_mild`。
- weak weighting：仅最小 sanity，沿用 `weak_peak_w2p0`。
- 数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`。
- 训练样本：{TRAIN_SAMPLE_COUNT} synthetic-interference samples；非正式 3-seed 实验。
- D5C：只做 clean-map RD/RA projection smoke，不声称 RD/RA target mask 是精确真值。

## 2. D5B weak definition audit

{markdown_table(audit_rows, ['definition', 'weak_n', 'weak_overlap_mask_ratio', 'weak_non_overlap_count', 'jaccard_with_clean_peak_percentile', 'range_bin_conflict_ratio', 'interval_overlap_ratio', 'average_nearest_target_distance_bins'])}

## 3. D5B repaired definition results

{markdown_table(d5b_rows, ['definition', 'weak_n', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa', 'false_alarm_count_delta', 'clean_input_no_harm', 'default_vs_narrow_mask_consistency', 'all_vs_non_overlap_consistency'])}

Best weak-Pd delta row: `{best['definition']}` with weak Pd delta = {float(best['weak_pd_delta']):.4f}, hit delta = {best['weak_hit_delta']}. This remains a small-sample sanity result, not a confirmed improvement.

## 4. D5C RD/RA feasibility smoke

{markdown_table(d5c_rows, ['representation', 'target_projection_hit_rate', 'weak_target_projection_hit_rate', 'target_overlap_ratio', 'weak_target_overlap_ratio', 'weak_separability_proxy_db', 'fixed_pfa_calibration_sanity', 'measured_pfa_at_target_pfa_1e_2', 'measured_pfa_at_target_pfa_1e_3', 'supports_followup_rdra_training'])}

RD/RA interpretation is limited to feasibility evidence. RD has no Doppler ground-truth label in this subset; RA uses rough label azimuth projection.

## 5. Decision summary

{markdown_table(decision_rows, ['decision_item', 'verdict', 'evidence', 'route'])}

## 6. Output paths

- Result dir: `{RESULT_DIR}`
- Figure dir: `{FIG_DIR}`
- Key CSV:
  - `d5b_weak_definition_audit.csv`
  - `d5b_repaired_definition_results.csv`
  - `d5c_range_rd_ra_separability.csv`
"""
    go = f"""# D5B-D5C GO / NO-GO decision

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Verdict

{markdown_table(decision_rows, ['decision_item', 'verdict', 'route'])}

## Conservative conclusion

- Repaired weak definitions must meet all weak-weighting bars before continuing: weak Pd gain >= 0.02, weak hit delta >= +5, no PFA/false alarm increase, clean no-harm, default/narrow consistency, and all/non-overlap consistency.
- Current D5B decision is based on the generated CSV, not a best-case single number.
- RD/RA evidence is smoke-only feasibility evidence; it cannot be written as confirmed RD/RA improvement.
- D6 remains forbidden in this run.

## Next minimal prompt

`/result-to-claim "D5B-D5C audited results: decide whether to record range-only weak weighting as a negative result, or run one narrow RD/RA feasibility confirmation without entering D6" -- reviewer: codex, assurance: conference-ready`
"""
    summary_ts = add_output_version(SUMMARY_PATH, summary)
    go_ts = add_output_version(GO_NOGO_PATH, go)
    outputs.extend(
        [
            (SUMMARY_PATH, "D5B-D5C latest summary"),
            (summary_ts, "D5B-D5C timestamped summary"),
            (GO_NOGO_PATH, "D5B-D5C latest GO/NO-GO decision"),
            (go_ts, "D5B-D5C timestamped GO/NO-GO decision"),
        ]
    )
    return summary_ts, go_ts


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    outputs: list[tuple[Path, str]] = []

    base = d5diag.prepare_base()
    relation_by_mask = extend_context_splits(base["contexts"], base["targets"])
    data = d5diag.make_train_data(base, TRAIN_SAMPLE_COUNT)
    default_ctx = data["contexts"]["default"]
    audit_rows = weak_definition_audit_rows(default_ctx, relation_by_mask["default"])

    training_rows: list[dict[str, Any]] = []
    training_metrics: list[dict[str, Any]] = []
    models: dict[str, Any] = {}
    label_by_definition: dict[str, str] = {}

    balanced_cfg = {"label": "balanced_mild", "family": "balanced", "balance": "mild"}
    balanced_model, balanced_rows, balanced_metrics = d4.train_strong_baseline(
        balanced_cfg,
        data["train_x"],
        data["train_y"],
        data["train_rows"],
        data["val_x"],
        data["val_y"],
        data["val_rows"],
        data["contexts"],
        data["clean_power"],
        data["val_frames"],
        data["norm_mean"],
        data["norm_std"],
        device,
        seed_offset=5100,
    )
    if balanced_model is None:
        raise RuntimeError("balanced_mild training failed; cannot run D5B comparisons")
    models["balanced_mild"] = balanced_model
    training_rows.extend(rename_training_rows(balanced_rows, "balanced_mild", "baseline"))
    training_metrics.append(rename_training_metrics(balanced_metrics, "balanced_mild", "baseline"))

    for idx, spec in enumerate(DEFINITIONS):
        definition = spec["key"]
        label = f"d5b_{spec['short']}_w2p0"
        label_by_definition[definition] = label
        model, rows, metrics = d5.train_weak_baseline(
            definition,
            WEAK_WEIGHT,
            data["train_x"],
            data["train_y"],
            data["train_rows"],
            data["val_x"],
            data["val_y"],
            data["val_rows"],
            data["contexts"],
            data["targets"],
            data["clean_power"],
            data["val_frames"],
            data["norm_mean"],
            data["norm_std"],
            device,
            seed_offset=5200 + idx,
        )
        training_rows.extend(rename_training_rows(rows, label, definition))
        training_metrics.append(rename_training_metrics(metrics, label, definition))
        if model is not None:
            models[label] = model

    case_arrays = d5.build_case_arrays(
        data["clean_power"],
        data["clean_db"],
        data["val_frames"],
        data["test_frames"],
        data["eval_val_inter_db"],
        data["eval_test_inter_db"],
        models,
        data["norm_mean"],
        data["norm_std"],
        device,
    )
    metrics = evaluate_cases(
        data["manifest"],
        data["targets"],
        data["contexts"],
        data["clean_power"],
        data["clean_db"],
        data["val_frames"],
        data["test_frames"],
        case_arrays,
    )
    recon_rows = d5.reconstruction_metrics(case_arrays, data["clean_db"], data["clean_power"], data["test_frames"])
    d5b_rows = build_repaired_result_rows(
        audit_rows, metrics["fixed"], recon_rows, label_by_definition
    )

    range_row, _range_targets = range_representation_rows(
        data["clean_power"],
        data["clean_db"],
        default_ctx,
        data["targets"],
        data["val_frames"],
        data["test_frames"],
        "clean_peak_percentile",
    )
    rd_row, _rd_targets, rd_samples = compute_2d_representation(
        "rd",
        data["manifest"],
        data["targets"],
        default_ctx,
        data["val_frames"],
        data["test_frames"],
        "clean_peak_percentile",
    )
    ra_row, _ra_targets, ra_samples = compute_2d_representation(
        "ra",
        data["manifest"],
        data["targets"],
        default_ctx,
        data["val_frames"],
        data["test_frames"],
        "clean_peak_percentile",
    )
    d5c_rows = [range_row, rd_row, ra_row]
    update_rdra_support_flags(d5c_rows)
    decision_rows = make_decision_rows(d5b_rows, d5c_rows)

    csv_outputs = [
        (RESULT_DIR / "d5b_weak_definition_audit.csv", audit_rows, "D5B weak definition audit"),
        (RESULT_DIR / "d5b_repaired_definition_results.csv", d5b_rows, "D5B repaired definition fixed-PFA results"),
        (RESULT_DIR / "d5c_range_rd_ra_separability.csv", d5c_rows, "D5C range/RD/RA separability smoke"),
        (RESULT_DIR / "d5b_training_summary.csv", training_metrics, "D5B training summary"),
        (RESULT_DIR / "d5b_training_loss.csv", training_rows, "D5B training loss"),
        (RESULT_DIR / "d5b_fixed_pfa_metrics.csv", metrics["fixed"], "D5B all fixed-PFA metrics"),
        (RESULT_DIR / "d5b_metrics_by_mask.csv", metrics["by_mask"], "D5B metrics by mask"),
        (RESULT_DIR / "d5b_metrics_non_overlap_only.csv", metrics["non_overlap"], "D5B non-overlap metrics"),
        (RESULT_DIR / "d5b_reconstruction_metrics.csv", recon_rows, "D5B reconstruction/no-harm metrics"),
        (RESULT_DIR / "d5b_d5c_decision_rows.csv", decision_rows, "D5B-D5C mechanical decision rows"),
    ]
    for path, rows, desc in csv_outputs:
        write_csv(path, rows)
        outputs.append((path, desc))

    config = {
        "stage": "D5B-D5C",
        "date": datetime.now().isoformat(),
        "python_device": str(device),
        "train_sample_count": TRAIN_SAMPLE_COUNT,
        "weak_weight": WEAK_WEIGHT,
        "primary_pfa": PRIMARY_PFA,
        "secondary_pfa": SECONDARY_PFA,
        "definitions": DEFINITIONS,
        "constraints": {
            "entered_d6": False,
            "false_alarm_penalty": False,
            "detector_modified": False,
            "cfar_protocol_modified": False,
            "three_seed_formal_experiment": False,
            "large_model": False,
        },
        "input_paths": {
            "dataset": str(ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1"),
            "d5_diagnosis": str(ROOT / "results" / "d5_diagnosis_weak_weighting_failure"),
            "d5_check": str(ROOT / "results" / "d5_check_improvement_significance"),
        },
        "output_paths": {"result_dir": str(RESULT_DIR), "figure_dir": str(FIG_DIR)},
    }
    config_path = RESULT_DIR / "d5b_d5c_config.json"
    write_json(config_path, config)
    outputs.append((config_path, "D5B-D5C config"))

    figure_paths = []
    figure_paths.extend(
        plot_d5b_figures(audit_rows, d5b_rows, data["clean_db"], data["targets"], default_ctx, data["test_frames"])
    )
    figure_paths.extend(plot_d5c_figures(d5c_rows, rd_samples, ra_samples, data["targets"], default_ctx, data["test_frames"]))
    for fig in figure_paths:
        outputs.append((fig, "D5B-D5C diagnostic figure"))

    summary_ts, go_ts = write_reports(audit_rows, d5b_rows, d5c_rows, decision_rows, outputs)
    append_manifest(outputs)

    print(
        json.dumps(
            {
                "stage": "D5B-D5C",
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "summary": str(SUMMARY_PATH),
                "timestamped_summary": str(summary_ts),
                "go_nogo": str(GO_NOGO_PATH),
                "timestamped_go_nogo": str(go_ts),
                "decision_rows": decision_rows,
                "artifact_count": len(outputs),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
