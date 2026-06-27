from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

import d1a_gao77_clean_fixed_pfa_sanity as d1a
from d1a_gao77_clean_fixed_pfa_sanity import ROOT, write_csv, write_json
from d1a_plus_mask_stress_test import MASK_CONFIGS, build_masks, target_peak_and_projection
from d1b_gao77_synthetic_interference_sanity import build_mask_context
from d2a_gao77_small_model_sanity import load_clean_data, load_split
from d5b_d5c_weak_definition_rdra_diagnosis import relation_stats_for_context
from d5d_rd_only_supplementary import (
    EVAL_SIR_NAME,
    LAMBDA_REC,
    N_TEST_FRAMES,
    N_TRAIN_FRAMES,
    N_VAL_FRAMES,
    RANDOM_SEED,
    SEEDS,
    SPLIT_DEFINITION,
    TRAIN_SIR_NAMES,
    WEAK_WEIGHT,
    build_sample_arrays,
    case_from_by_frame,
    clean_peak_frozen_splits,
    compute_rd_maps,
    infer_rd,
    md_table,
    reconstruction_rows,
    split_counts_for_frames,
    train_model,
    valid_range_mask_2d,
)


RESULT_DIR = ROOT / "results" / "d5e_rd_proxy_ceiling_diagnosis"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5e_rd_proxy_ceiling_figures"
SUMMARY_PATH = RESULT_DIR / "d5e_rd_proxy_ceiling_summary.md"
DECISION_PATH = RESULT_DIR / "d5e_rd_proxy_ceiling_decision.md"
CONFIG_PATH = RESULT_DIR / "d5e_config.json"
GPT_HANDOFF_PATH = RESULT_DIR / "GPT_HANDOFF_D5E.md"

PFA_LEVELS = [1e-2, 5e-3, 1e-3, 5e-4, 1e-4]
MASK_RANGE_NAMES = ["narrow", "default", "wide"]
DOPPLER_RADII = [1, 2, 3, 5]
WEAK_Q_LEVELS = [0.10, 0.20, 0.30, 0.40]
BOOTSTRAP_N = 2000


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


def write_csv_versioned(path: Path, rows: list[dict[str, Any]], desc: str, outputs: list[tuple[Path, str]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    write_csv(ts_path, rows)
    write_csv(path, rows)
    outputs.append((path, desc))
    outputs.append((ts_path, f"{desc} timestamped copy"))
    return ts_path


def write_text_versioned(path: Path, text: str, desc: str, outputs: list[tuple[Path, str]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8-sig")
    path.write_text(text, encoding="utf-8-sig")
    outputs.append((path, desc))
    outputs.append((ts_path, f"{desc} timestamped copy"))
    return ts_path


def write_json_versioned(path: Path, obj: Any, desc: str, outputs: list[tuple[Path, str]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    ts_path = path.with_name(f"{path.stem}_{now_stamp()}{path.suffix}")
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    ts_path.write_text(text, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    outputs.append((path, desc))
    outputs.append((ts_path, f"{desc} timestamped copy"))
    return ts_path


def append_manifest(outputs: list[tuple[Path, str]], skill: str = "/experiment-bridge") -> None:
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
        lines.append(f"| {stamp} | {skill} | {rel} | implementation | {desc} |")
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def one_d_contexts_all(clean_range_db: np.ndarray, clean_cfar: np.ndarray, targets: list[Any]) -> dict[str, dict[str, Any]]:
    n_frames, n_bins = clean_range_db.shape
    out: dict[str, dict[str, Any]] = {}
    for cfg in MASK_CONFIGS:
        tm, gm, bm, intervals = build_masks(targets, n_frames, n_bins, cfg)
        target_values = target_peak_and_projection(clean_range_db, clean_cfar, targets, intervals, int(cfg["guard_extra"]))
        out[str(cfg["mask_name"])] = {
            "cfg": cfg,
            "target_mask": tm,
            "guard_mask": gm,
            "background_mask": bm,
            "intervals": intervals,
            "target_values": target_values,
        }
    return out


def split_by_train_quantile(
    ctx: dict[str, Any],
    targets: list[Any],
    train_frames: np.ndarray,
    q_weak: float,
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
        raise RuntimeError("no train targets available for quantile split")
    qv = float(np.quantile(vals, q_weak))
    q70 = float(np.quantile(vals, 0.70))
    relation = relation_stats_for_context(ctx, targets)
    splits: dict[int, str] = {}
    weak_candidate_ids: set[int] = set()
    filtered_ids: set[int] = set()
    for tid_raw, item in values.items():
        tid = int(tid_raw)
        if not item.get("valid_projection"):
            continue
        peak = float(item["target_peak_db"])
        if peak <= qv:
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
    return splits, {
        "q_weak": q_weak,
        "train_target_peak_db_q_threshold": qv,
        "train_target_peak_db_q70_strong_threshold": q70,
        "train_target_count_for_threshold": int(vals.size),
        "weak_candidate_count_all_frames": len(weak_candidate_ids),
        "overlap_filtered_weak_candidate_count_all_frames": len(filtered_ids),
        "threshold_source": "train split only",
        "threshold_leakage": False,
        "used_test_clean_map_property_for_threshold": False,
    }


def doppler_center(
    mode: str,
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    frame_idx: int,
    lo: int,
    hi: int,
) -> int:
    rd = clean_rd[frame_idx]
    n_doppler = rd.shape[1]
    zero = n_doppler // 2
    if mode == "clean_peak":
        sub = clean_rd[frame_idx][lo:hi, :]
        _r, d = np.unravel_index(int(np.argmax(sub)), sub.shape)
        return int(d)
    if mode == "interfered_peak":
        sub = inter_rd[EVAL_SIR_NAME][frame_idx][lo:hi, :]
        _r, d = np.unravel_index(int(np.argmax(sub)), sub.shape)
        return int(d)
    if mode == "local_window_peak":
        half = min(8, zero)
        dlo = max(0, zero - half)
        dhi = min(n_doppler, zero + half + 1)
        sub = clean_rd[frame_idx][lo:hi, dlo:dhi]
        _r, d = np.unravel_index(int(np.argmax(sub)), sub.shape)
        return int(dlo + d)
    if mode == "nearest_high_energy":
        profile = np.max(clean_rd[frame_idx][lo:hi, :], axis=0)
        cutoff = max(float(np.max(profile) - 3.0), float(np.quantile(profile, 0.90)))
        candidates = np.where(profile >= cutoff)[0]
        if candidates.size == 0:
            return int(np.argmax(profile))
        return int(candidates[np.argmin(np.abs(candidates - zero))])
    raise KeyError(mode)


def build_rd_context_variant(
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    targets: list[Any],
    range_ctx: dict[str, Any],
    splits: dict[int, str],
    frame_indices: np.ndarray,
    *,
    range_mask_name: str,
    doppler_mode: str = "clean_peak",
    doppler_radius: int = 2,
) -> dict[str, Any]:
    frame_set = {int(x) for x in frame_indices.tolist()}
    shape = next(iter(clean_rd.values())).shape
    n_doppler = shape[1]
    target_mask_by_frame = {idx: np.zeros(shape, dtype=bool) for idx in frame_set}
    guard_mask_by_frame = {idx: np.zeros(shape, dtype=bool) for idx in frame_set}
    rect_by_target: dict[int, tuple[int, int, int, int]] = {}
    clean_peak_cell_by_target: dict[int, tuple[int, int]] = {}
    intervals = range_ctx["intervals"]
    range_guard = 3 if range_mask_name == "narrow" else 6 if range_mask_name == "wide" else 4
    doppler_guard = max(int(doppler_radius) + 3, 3)
    for target in targets:
        tid = int(target.target_id)
        frame_idx = int(target.frame_idx)
        if frame_idx not in frame_set or tid not in intervals or tid not in splits:
            continue
        lo, hi, _radius = intervals[tid]
        clean_sub = clean_rd[frame_idx][lo:hi, :]
        if clean_sub.size == 0:
            continue
        cr, cd = np.unravel_index(int(np.argmax(clean_sub)), clean_sub.shape)
        clean_peak_cell_by_target[tid] = (lo + int(cr), int(cd))
        if doppler_mode == "vertical_stripe":
            dlo, dhi = 0, n_doppler
            gdlo, gdhi = 0, n_doppler
        elif doppler_mode == "multi_bin_uncertainty":
            center = doppler_center("clean_peak", clean_rd, inter_rd, frame_idx, lo, hi)
            radius = max(int(doppler_radius), 5)
            dlo = max(0, center - radius)
            dhi = min(n_doppler, center + radius + 1)
            gdlo = max(0, center - radius - 3)
            gdhi = min(n_doppler, center + radius + 4)
        else:
            center = doppler_center(doppler_mode, clean_rd, inter_rd, frame_idx, lo, hi)
            dlo = max(0, center - int(doppler_radius))
            dhi = min(n_doppler, center + int(doppler_radius) + 1)
            gdlo = max(0, center - doppler_guard)
            gdhi = min(n_doppler, center + doppler_guard + 1)
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
            a = rect_by_target[tid]
            for oid in tids[ix + 1 :]:
                b = rect_by_target[oid]
                if max(a[0], b[0]) < min(a[1], b[1]) and max(a[2], b[2]) < min(a[3], b[3]):
                    overlapped.add(tid)
                    overlapped.add(oid)

    return {
        "mask_name": f"{range_mask_name}_doppler_r{doppler_radius}_{doppler_mode}",
        "range_mask_name": range_mask_name,
        "doppler_mode": doppler_mode,
        "doppler_radius": int(doppler_radius),
        "shape": shape,
        "target_mask_by_frame": target_mask_by_frame,
        "background_mask_by_frame": background_mask_by_frame,
        "guard_mask_by_frame": guard_mask_by_frame,
        "rect_by_target": rect_by_target,
        "clean_peak_cell_by_target": clean_peak_cell_by_target,
        "splits": {SPLIT_DEFINITION: splits},
        "non_overlap_ids": {tid for tid in rect_by_target if tid not in overlapped},
        "range_guard": range_guard,
        "doppler_guard": doppler_guard,
        "projection_note": "RD Doppler boxes are diagnostic proxies derived from range labels; no Doppler GT is available.",
    }


def evaluate_case_variant(
    case: dict[str, Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    rd_ctx: dict[str, Any],
    targets: list[Any],
    pfa: float,
    target_scope: str = "all",
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
        "mask_name": rd_ctx["mask_name"],
        "range_mask_name": rd_ctx.get("range_mask_name", ""),
        "doppler_mode": rd_ctx.get("doppler_mode", ""),
        "doppler_radius": rd_ctx.get("doppler_radius", ""),
        "split_definition": SPLIT_DEFINITION,
        "target_scope": target_scope,
        "target_pfa": pfa,
        "threshold_source": "input_specific_validation_background",
        "threshold": threshold,
        "measured_pfa": fa / max(bg_count, 1),
        "false_alarm_count": fa,
        "background_cell_count": bg_count,
        "validation_background_cell_count": int(sum(bg_by_frame[int(idx)].sum() for idx in val_frames.tolist())),
        "target_mask_cell_count_test": int(sum(tm_by_frame[int(idx)].sum() for idx in test_frames.tolist())),
        "tp_cells": tp_cells,
        "fp_cells": fa,
        "fn_cells": fn_cells,
        "precision": precision,
        "recall": recall,
        "f1": f1,
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
        out[f"{split_name}_miss_count"] = len(subset) - hits
    all_hits = 0
    for target in selected_targets:
        tid = int(target.target_id)
        rlo, rhi, dlo, dhi = rects[tid]
        all_hits += int(bool(detections[int(target.frame_idx)][rlo:rhi, dlo:dhi].any()))
    out["overall_n"] = len(selected_targets)
    out["overall_hits"] = all_hits
    out["overall_pd"] = all_hits / len(selected_targets) if selected_targets else ""
    out["overall_miss_count"] = len(selected_targets) - all_hits
    return out


def lookup_case(cases: list[dict[str, Any]], input_type: str, seed: int | str = "") -> dict[str, Any]:
    for case in cases:
        if case["input_type"] == input_type and str(case.get("seed", "")) == str(seed):
            return case
    raise KeyError((input_type, seed))


def target_hit_array(
    case: dict[str, Any],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    rd_ctx: dict[str, Any],
    targets: list[Any],
    pfa: float,
    split_name: str = "weak",
) -> tuple[list[int], np.ndarray]:
    bg_by_frame = rd_ctx["background_mask_by_frame"]
    rects = rd_ctx["rect_by_target"]
    splits = rd_ctx["splits"][SPLIT_DEFINITION]
    val_scores = np.concatenate([case["db_by_frame"][int(idx)][bg_by_frame[int(idx)]] for idx in val_frames.tolist()])
    threshold = float(np.quantile(val_scores, 1.0 - pfa))
    detections = {int(idx): case["db_by_frame"][int(idx)] >= threshold for idx in case["frames"].tolist()}
    test_set = {int(x) for x in test_frames.tolist()}
    ids: list[int] = []
    hits: list[int] = []
    for target in targets:
        tid = int(target.target_id)
        if int(target.frame_idx) not in test_set or tid not in rects or splits.get(tid) != split_name:
            continue
        rlo, rhi, dlo, dhi = rects[tid]
        ids.append(tid)
        hits.append(int(bool(detections[int(target.frame_idx)][rlo:rhi, dlo:dhi].any())))
    return ids, np.asarray(hits, dtype=np.int32)


def pair_metrics(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    ctx: dict[str, Any],
    targets: list[Any],
    seed: int,
    pfa: float,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    b_case = lookup_case(cases, f"rd_balanced_mild_seed{seed}_output", seed)
    w_case = lookup_case(cases, f"rd_weak_w2p0_seed{seed}_output", seed)
    b = evaluate_case_variant(b_case, val_frames, test_frames, ctx, targets, pfa)
    w = evaluate_case_variant(w_case, val_frames, test_frames, ctx, targets, pfa)
    delta = {
        "seed": seed,
        "target_pfa": pfa,
        "weak_n": b["weak_n"],
        "balanced_mild_weak_hits": b["weak_hits"],
        "weak_weighting_weak_hits": w["weak_hits"],
        "balanced_mild_weak_pd": b["weak_pd"],
        "weak_weighting_weak_pd": w["weak_pd"],
        "weak_pd_delta": f(w, "weak_pd") - f(b, "weak_pd"),
        "weak_hit_delta": i(w, "weak_hits") - i(b, "weak_hits"),
        "balanced_mild_overall_pd": b["overall_pd"],
        "weak_weighting_overall_pd": w["overall_pd"],
        "overall_pd_delta": f(w, "overall_pd") - f(b, "overall_pd"),
        "balanced_mild_mid_pd": b["mid_pd"],
        "weak_weighting_mid_pd": w["mid_pd"],
        "balanced_mild_strong_pd": b["strong_pd"],
        "weak_weighting_strong_pd": w["strong_pd"],
        "balanced_mild_measured_pfa": b["measured_pfa"],
        "weak_weighting_measured_pfa": w["measured_pfa"],
        "measured_pfa_delta": f(w, "measured_pfa") - f(b, "measured_pfa"),
        "balanced_mild_false_alarm_count": b["false_alarm_count"],
        "weak_weighting_false_alarm_count": w["false_alarm_count"],
        "false_alarm_count_delta": i(w, "false_alarm_count") - i(b, "false_alarm_count"),
    }
    return b, w, delta


def add_mean_rows(rows: list[dict[str, Any]], group_keys: list[str], numeric_keys: list[str]) -> list[dict[str, Any]]:
    out = list(rows)
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if str(row.get("seed", "")) == "mean":
            continue
        groups[tuple(row.get(k, "") for k in group_keys)].append(row)
    for key, group in groups.items():
        mean_row = {k: v for k, v in zip(group_keys, key)}
        mean_row["seed"] = "mean"
        mean_row["n_seeds"] = len(group)
        for nk in numeric_keys:
            vals = [f(r, nk, float("nan")) for r in group if r.get(nk, "") not in ("", None)]
            vals = [v for v in vals if np.isfinite(v)]
            mean_row[nk] = float(np.mean(vals)) if vals else ""
        out.append(mean_row)
    return out


def ceiling_effect_audit(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    ctx: dict[str, Any],
    targets: list[Any],
) -> list[dict[str, Any]]:
    rows = []
    for seed in SEEDS:
        b, w, delta = pair_metrics(cases, val_frames, test_frames, ctx, targets, seed, 1e-2)
        improvement_room = i(b, "weak_n") - i(b, "weak_hits")
        rows.append(
            {
                **delta,
                "target_pfa": 1e-2,
                "balanced_mild_weak_miss_count": improvement_room,
                "weak_weighting_weak_miss_count": i(w, "weak_miss_count"),
                "balanced_mild_overall_miss_count": i(b, "overall_miss_count"),
                "balanced_mild_mid_miss_count": i(b, "mid_miss_count"),
                "balanced_mild_strong_miss_count": i(b, "strong_miss_count"),
                "weak_pd_saturated": f(b, "weak_pd") >= 0.999,
                "overall_pd_saturated": f(b, "overall_pd") >= 0.999,
                "mid_pd_saturated": f(b, "mid_pd") >= 0.999,
                "strong_pd_saturated": f(b, "strong_pd") >= 0.999,
                "improvement_room_weak_hits": improvement_room,
                "ceiling_effect_present": improvement_room == 0 and f(b, "weak_pd") >= 0.999,
                "no_gain_from_weak_weighting": i(w, "weak_hits") <= i(b, "weak_hits"),
            }
        )
    return add_mean_rows(
        rows,
        ["target_pfa"],
        [
            "weak_n",
            "balanced_mild_weak_hits",
            "weak_weighting_weak_hits",
            "balanced_mild_weak_pd",
            "weak_weighting_weak_pd",
            "weak_pd_delta",
            "weak_hit_delta",
            "balanced_mild_overall_pd",
            "weak_weighting_overall_pd",
            "overall_pd_delta",
            "balanced_mild_measured_pfa",
            "weak_weighting_measured_pfa",
            "measured_pfa_delta",
            "balanced_mild_false_alarm_count",
            "weak_weighting_false_alarm_count",
            "false_alarm_count_delta",
            "balanced_mild_weak_miss_count",
            "weak_weighting_weak_miss_count",
            "improvement_room_weak_hits",
        ],
    )


def pfa_sensitivity(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    ctx: dict[str, Any],
    targets: list[Any],
) -> list[dict[str, Any]]:
    rows = []
    for pfa in PFA_LEVELS:
        for seed in SEEDS:
            _b, _w, delta = pair_metrics(cases, val_frames, test_frames, ctx, targets, seed, pfa)
            rows.append(
                {
                    **delta,
                    "weak_weighting_improves_weak_pd": delta["weak_pd_delta"] > 0,
                    "weak_weighting_hit_gain_positive": delta["weak_hit_delta"] > 0,
                    "weak_weighting_pfa_not_higher": delta["measured_pfa_delta"] <= 0,
                }
            )
    return add_mean_rows(
        rows,
        ["target_pfa"],
        [
            "weak_n",
            "balanced_mild_weak_hits",
            "weak_weighting_weak_hits",
            "balanced_mild_weak_pd",
            "weak_weighting_weak_pd",
            "weak_pd_delta",
            "weak_hit_delta",
            "balanced_mild_overall_pd",
            "weak_weighting_overall_pd",
            "overall_pd_delta",
            "balanced_mild_measured_pfa",
            "weak_weighting_measured_pfa",
            "measured_pfa_delta",
            "balanced_mild_false_alarm_count",
            "weak_weighting_false_alarm_count",
            "false_alarm_count_delta",
        ],
    )


def mask_width_sensitivity(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    targets: list[Any],
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    range_contexts: dict[str, dict[str, Any]],
    splits: dict[int, str],
    all_frames: np.ndarray,
) -> list[dict[str, Any]]:
    rows = []
    for range_name in MASK_RANGE_NAMES:
        for radius in DOPPLER_RADII:
            ctx = build_rd_context_variant(
                clean_rd,
                inter_rd,
                targets,
                range_contexts[range_name],
                splits,
                all_frames,
                range_mask_name=range_name,
                doppler_mode="clean_peak",
                doppler_radius=radius,
            )
            target_cells = int(sum(ctx["target_mask_by_frame"][int(idx)].sum() for idx in test_frames.tolist()))
            bg_cells = int(sum(ctx["background_mask_by_frame"][int(idx)].sum() for idx in test_frames.tolist()))
            for seed in SEEDS:
                _b, _w, delta = pair_metrics(cases, val_frames, test_frames, ctx, targets, seed, 1e-2)
                rows.append(
                    {
                        "range_mask_name": range_name,
                        "doppler_radius_bins": radius,
                        "mask_name": ctx["mask_name"],
                        "target_mask_cell_count_test": target_cells,
                        "target_mask_area_per_frame_mean": target_cells / len(test_frames),
                        "background_cell_count": bg_cells,
                        **delta,
                        "balanced_mild_saturated": f(delta, "balanced_mild_weak_pd") >= 0.999,
                        "weak_weighting_improves": f(delta, "weak_pd_delta") > 0,
                    }
                )
    return add_mean_rows(
        rows,
        ["range_mask_name", "doppler_radius_bins", "mask_name"],
        [
            "target_mask_cell_count_test",
            "target_mask_area_per_frame_mean",
            "background_cell_count",
            "weak_n",
            "balanced_mild_weak_pd",
            "weak_weighting_weak_pd",
            "weak_pd_delta",
            "weak_hit_delta",
            "balanced_mild_measured_pfa",
            "weak_weighting_measured_pfa",
            "measured_pfa_delta",
            "balanced_mild_false_alarm_count",
            "weak_weighting_false_alarm_count",
            "false_alarm_count_delta",
        ],
    )


def difficulty_stats(
    ctx: dict[str, Any],
    range_ctx: dict[str, Any],
    clean_rd: dict[int, np.ndarray],
    targets: list[Any],
    frames: np.ndarray,
    splits: dict[int, str],
) -> dict[str, Any]:
    frame_set = {int(x) for x in frames.tolist()}
    rects = ctx["rect_by_target"]
    clean_peaks = []
    range_peaks = []
    contrasts = []
    target_values = range_ctx["target_values"]
    for target in targets:
        tid = int(target.target_id)
        frame_idx = int(target.frame_idx)
        if frame_idx not in frame_set or splits.get(tid) != "weak" or tid not in rects:
            continue
        rlo, rhi, dlo, dhi = rects[tid]
        clean_peak = float(np.max(clean_rd[frame_idx][rlo:rhi, dlo:dhi]))
        bg_median = float(np.median(clean_rd[frame_idx][ctx["background_mask_by_frame"][frame_idx]]))
        clean_peaks.append(clean_peak)
        contrasts.append(clean_peak - bg_median)
        if tid in target_values and target_values[tid].get("valid_projection"):
            range_peaks.append(float(target_values[tid]["target_peak_db"]))
    return {
        "mean_clean_rd_peak_db": float(np.mean(clean_peaks)) if clean_peaks else "",
        "mean_range_only_peak_db": float(np.mean(range_peaks)) if range_peaks else "",
        "mean_target_background_contrast_db": float(np.mean(contrasts)) if contrasts else "",
    }


def weak_threshold_difficulty(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    train_frames: np.ndarray,
    targets: list[Any],
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    default_range_ctx: dict[str, Any],
    all_frames: np.ndarray,
) -> list[dict[str, Any]]:
    rows = []
    for q in WEAK_Q_LEVELS:
        splits, meta = split_by_train_quantile(default_range_ctx, targets, train_frames, q)
        ctx = build_rd_context_variant(
            clean_rd,
            inter_rd,
            targets,
            default_range_ctx,
            splits,
            all_frames,
            range_mask_name="default",
            doppler_mode="clean_peak",
            doppler_radius=2,
        )
        counts_train = split_counts_for_frames(splits, targets, train_frames)
        counts_val = split_counts_for_frames(splits, targets, val_frames)
        counts_test = split_counts_for_frames(splits, targets, test_frames)
        diff = difficulty_stats(ctx, default_range_ctx, clean_rd, targets, test_frames, splits)
        for seed in SEEDS:
            _b, _w, delta = pair_metrics(cases, val_frames, test_frames, ctx, targets, seed, 1e-2)
            rows.append(
                {
                    "q_weak": q,
                    "train_weak_threshold_db": meta["train_target_peak_db_q_threshold"],
                    "train_weak_n": counts_train["weak_n"],
                    "val_weak_n": counts_val["weak_n"],
                    "test_weak_n": counts_test["weak_n"],
                    **diff,
                    **delta,
                    "scope_note": "Same D5D q30-trained model outputs; this row re-bins evaluation targets by train-only q threshold for difficulty diagnosis.",
                }
            )
    return add_mean_rows(
        rows,
        ["q_weak", "train_weak_threshold_db", "train_weak_n", "val_weak_n", "test_weak_n"],
        [
            "mean_clean_rd_peak_db",
            "mean_range_only_peak_db",
            "mean_target_background_contrast_db",
            "balanced_mild_weak_pd",
            "weak_weighting_weak_pd",
            "weak_pd_delta",
            "weak_hit_delta",
            "balanced_mild_measured_pfa",
            "weak_weighting_measured_pfa",
            "measured_pfa_delta",
        ],
    )


def rect_iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    inter = max(0, min(a[1], b[1]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[2], b[2]))
    area_a = max(0, a[1] - a[0]) * max(0, a[3] - a[2])
    area_b = max(0, b[1] - b[0]) * max(0, b[3] - b[2])
    union = area_a + area_b - inter
    return inter / union if union else 0.0


def proxy_label_dependence(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    targets: list[Any],
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    default_range_ctx: dict[str, Any],
    splits: dict[int, str],
    all_frames: np.ndarray,
) -> list[dict[str, Any]]:
    modes = [
        ("clean_peak", 2, "D5D default: range label plus clean-RD Doppler peak projection."),
        ("interfered_peak", 2, "Doppler center from interfered RD peak; diagnostic proxy, not GT."),
        ("local_window_peak", 2, "Clean RD peak restricted to central local Doppler window."),
        ("nearest_high_energy", 2, "Nearest high-energy Doppler bin to zero-Doppler among clean RD candidates."),
        ("vertical_stripe", 0, "Doppler-agnostic vertical stripe over the full Doppler axis."),
        ("multi_bin_uncertainty", 5, "Clean-peak-centered multi-bin uncertainty box."),
    ]
    clean_ctx = build_rd_context_variant(
        clean_rd,
        inter_rd,
        targets,
        default_range_ctx,
        splits,
        all_frames,
        range_mask_name="default",
        doppler_mode="clean_peak",
        doppler_radius=2,
    )
    test_set = {int(x) for x in test_frames.tolist()}
    rows = []
    for mode, radius, note in modes:
        ctx = build_rd_context_variant(
            clean_rd,
            inter_rd,
            targets,
            default_range_ctx,
            splits,
            all_frames,
            range_mask_name="default",
            doppler_mode=mode,
            doppler_radius=max(radius, 1),
        )
        weak_ids = [
            int(t.target_id)
            for t in targets
            if int(t.frame_idx) in test_set and splits.get(int(t.target_id)) == "weak" and int(t.target_id) in ctx["rect_by_target"]
        ]
        hit_clean_peak = 0
        overlaps = []
        areas = []
        for tid in weak_ids:
            rlo, rhi, dlo, dhi = ctx["rect_by_target"][tid]
            cr, cd = clean_ctx["clean_peak_cell_by_target"].get(tid, (-1, -1))
            hit_clean_peak += int(rlo <= cr < rhi and dlo <= cd < dhi)
            if tid in clean_ctx["rect_by_target"]:
                overlaps.append(rect_iou(ctx["rect_by_target"][tid], clean_ctx["rect_by_target"][tid]))
            areas.append((rhi - rlo) * (dhi - dlo))
        weak_projection_hit_rate = hit_clean_peak / len(weak_ids) if weak_ids else ""
        mean_overlap = float(np.mean(overlaps)) if overlaps else ""
        mean_area = float(np.mean(areas)) if areas else ""
        for seed in SEEDS:
            _b, _w, delta = pair_metrics(cases, val_frames, test_frames, ctx, targets, seed, 1e-2)
            rows.append(
                {
                    "doppler_box_mode": mode,
                    "doppler_radius_bins": radius,
                    "weak_projection_hit_rate_against_clean_peak": weak_projection_hit_rate,
                    "target_box_area_mean_weak": mean_area,
                    "overlap_ratio_vs_clean_peak_box": mean_overlap,
                    **delta,
                    "scope_note": note,
                }
            )
    return add_mean_rows(
        rows,
        ["doppler_box_mode", "doppler_radius_bins"],
        [
            "weak_projection_hit_rate_against_clean_peak",
            "target_box_area_mean_weak",
            "overlap_ratio_vs_clean_peak_box",
            "balanced_mild_weak_pd",
            "weak_weighting_weak_pd",
            "weak_pd_delta",
            "weak_hit_delta",
            "balanced_mild_measured_pfa",
            "weak_weighting_measured_pfa",
            "measured_pfa_delta",
            "balanced_mild_false_alarm_count",
            "weak_weighting_false_alarm_count",
            "false_alarm_count_delta",
        ],
    )


def bootstrap_ci(vals: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    if vals.size == 0:
        return float("nan"), float("nan"), float("nan")
    boot = []
    for _ in range(BOOTSTRAP_N):
        choices = rng.integers(0, vals.size, size=vals.size)
        boot.append(float(np.mean(vals[choices])))
    return float(np.mean(vals)), float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))


def sample_size_stability(
    cases: list[dict[str, Any]],
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    ctx: dict[str, Any],
    targets: list[Any],
) -> list[dict[str, Any]]:
    rows = []
    for pfa in [1e-2, 1e-3]:
        deltas_for_seed = []
        for seed in SEEDS:
            b_case = lookup_case(cases, f"rd_balanced_mild_seed{seed}_output", seed)
            w_case = lookup_case(cases, f"rd_weak_w2p0_seed{seed}_output", seed)
            b_ids, b_hits = target_hit_array(b_case, val_frames, test_frames, ctx, targets, pfa)
            w_ids, w_hits = target_hit_array(w_case, val_frames, test_frames, ctx, targets, pfa)
            if b_ids != w_ids:
                raise RuntimeError("target ordering mismatch for bootstrap")
            weak_n = len(b_ids)
            rng = np.random.default_rng(RANDOM_SEED + int(seed) + int(pfa * 1e6))
            b_mean, b_lo, b_hi = bootstrap_ci(b_hits.astype(np.float64), rng)
            w_mean, w_lo, w_hi = bootstrap_ci(w_hits.astype(np.float64), rng)
            diff = w_hits.astype(np.float64) - b_hits.astype(np.float64)
            d_mean, d_lo, d_hi = bootstrap_ci(diff, rng)
            hit_delta = int(w_hits.sum() - b_hits.sum())
            deltas_for_seed.append(d_mean)
            rows.append(
                {
                    "seed": seed,
                    "target_pfa": pfa,
                    "weak_n": weak_n,
                    "balanced_mild_weak_pd": b_mean,
                    "balanced_mild_weak_pd_ci_low": b_lo,
                    "balanced_mild_weak_pd_ci_high": b_hi,
                    "weak_weighting_weak_pd": w_mean,
                    "weak_weighting_weak_pd_ci_low": w_lo,
                    "weak_weighting_weak_pd_ci_high": w_hi,
                    "weak_pd_delta": d_mean,
                    "weak_pd_delta_ci_low": d_lo,
                    "weak_pd_delta_ci_high": d_hi,
                    "weak_hit_delta": hit_delta,
                    "one_hit_pd_delta": 1.0 / max(weak_n, 1),
                    "two_hit_pd_delta": 2.0 / max(weak_n, 1),
                    "five_hit_pd_delta": 5.0 / max(weak_n, 1),
                    "plus_0_hits_meaningful": False,
                    "plus_1_hit_meets_pd_bar_0p02": (1.0 / max(weak_n, 1)) >= 0.02,
                    "plus_2_hits_meets_hit_bar_5": 2 >= 5,
                    "plus_5_hits_required_for_d5d_bar": True,
                    "weak_n_small_for_claim": weak_n < 100,
                    "hit_delta_confidence": "no_positive_gain" if hit_delta <= 0 else "low_with_n62",
                }
            )
        rows.append(
            {
                "seed": "seed_sensitivity",
                "target_pfa": pfa,
                "weak_n": "",
                "weak_pd_delta": float(np.mean(deltas_for_seed)) if deltas_for_seed else "",
                "weak_pd_delta_seed_std": float(np.std(deltas_for_seed, ddof=1)) if len(deltas_for_seed) > 1 else 0.0,
                "hit_delta_confidence": "two_seed_only",
            }
        )
    return rows


def plot_outputs(
    pfa_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    q_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    sample_rows: list[dict[str, Any]],
    ceiling_rows: list[dict[str, Any]],
    clean_rd: dict[int, np.ndarray],
    inter_rd: dict[str, dict[int, np.ndarray]],
    targets: list[Any],
    default_ctx: dict[str, Any],
    test_frames: np.ndarray,
) -> list[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    figs: list[Path] = []
    mean_pfa = [r for r in pfa_rows if str(r.get("seed")) == "mean"]
    mean_pfa = sorted(mean_pfa, key=lambda r: f(r, "target_pfa"), reverse=True)
    x = [f(r, "target_pfa") for r in mean_pfa]
    plt.figure(figsize=(7, 4))
    plt.semilogx(x, [f(r, "balanced_mild_weak_pd") for r in mean_pfa], marker="o", label="balanced_mild")
    plt.semilogx(x, [f(r, "weak_weighting_weak_pd") for r in mean_pfa], marker="o", label="weak_weighting")
    plt.gca().invert_xaxis()
    plt.xlabel("Target PFA")
    plt.ylabel("Weak Pd")
    plt.title("D5E weak Pd vs fixed-PFA threshold")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = FIG_DIR / "weak_pd_vs_pfa_threshold.png"
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    figs.append(out)

    plt.figure(figsize=(7, 4))
    plt.semilogx(x, [f(r, "weak_hit_delta") for r in mean_pfa], marker="o")
    plt.axhline(0, color="black", linewidth=1)
    plt.gca().invert_xaxis()
    plt.xlabel("Target PFA")
    plt.ylabel("Weak hit delta")
    plt.title("D5E weak hit delta vs fixed-PFA threshold")
    plt.grid(True, alpha=0.3)
    out = FIG_DIR / "weak_hit_delta_vs_pfa_threshold.png"
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    figs.append(out)

    mean_mask = [r for r in mask_rows if str(r.get("seed")) == "mean"]
    labels = [f"{r['range_mask_name']}/r{int(float(r['doppler_radius_bins']))}" for r in mean_mask]
    plt.figure(figsize=(11, 4))
    xpos = np.arange(len(labels))
    plt.plot(xpos, [f(r, "balanced_mild_weak_pd") for r in mean_mask], marker="o", label="balanced_mild")
    plt.plot(xpos, [f(r, "weak_weighting_weak_pd") for r in mean_mask], marker="o", label="weak_weighting")
    plt.xticks(xpos, labels, rotation=45, ha="right")
    plt.ylabel("Weak Pd")
    plt.title("D5E mask width vs weak Pd")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = FIG_DIR / "mask_width_vs_weak_pd.png"
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    figs.append(out)

    mean_q = [r for r in q_rows if str(r.get("seed")) == "mean"]
    plt.figure(figsize=(7, 4))
    plt.plot([f(r, "q_weak") for r in mean_q], [f(r, "balanced_mild_weak_pd") for r in mean_q], marker="o", label="balanced_mild")
    plt.plot([f(r, "q_weak") for r in mean_q], [f(r, "weak_weighting_weak_pd") for r in mean_q], marker="o", label="weak_weighting")
    plt.xlabel("Train-only weak quantile")
    plt.ylabel("Weak Pd")
    plt.title("D5E q-threshold vs weak Pd")
    plt.grid(True, alpha=0.3)
    plt.legend()
    out = FIG_DIR / "q_threshold_vs_weak_pd.png"
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    figs.append(out)

    test_set = {int(x) for x in test_frames.tolist()}
    weak_targets = [
        t
        for t in targets
        if int(t.frame_idx) in test_set
        and default_ctx["splits"][SPLIT_DEFINITION].get(int(t.target_id)) == "weak"
        and int(t.target_id) in default_ctx["rect_by_target"]
    ]
    if weak_targets:
        target = weak_targets[0]
        frame = int(target.frame_idx)
        rect = default_ctx["rect_by_target"][int(target.target_id)]
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for ax, data, title in [
            (axes[0], clean_rd[frame], "Clean RD proxy label"),
            (axes[1], inter_rd[EVAL_SIR_NAME][frame], "Interfered RD diagnostic view"),
        ]:
            im = ax.imshow(data.T, aspect="auto", origin="lower", cmap="viridis")
            rlo, rhi, dlo, dhi = rect
            ax.add_patch(plt.Rectangle((rlo, dlo), rhi - rlo, dhi - dlo, fill=False, edgecolor="red", linewidth=1.5))
            ax.set_title(title)
            ax.set_xlabel("Range bin")
            ax.set_ylabel("Doppler bin")
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        out = FIG_DIR / "rd_proxy_label_examples.png"
        plt.tight_layout()
        plt.savefig(out, dpi=180)
        plt.close()
        figs.append(out)

    sample_default = [r for r in sample_rows if str(r.get("seed")) not in {"seed_sensitivity", ""} and abs(f(r, "target_pfa") - 1e-2) < 1e-12]
    plt.figure(figsize=(7, 4))
    xpos = np.arange(len(sample_default))
    means = [f(r, "weak_pd_delta") for r in sample_default]
    lows = [f(r, "weak_pd_delta") - f(r, "weak_pd_delta_ci_low") for r in sample_default]
    highs = [f(r, "weak_pd_delta_ci_high") - f(r, "weak_pd_delta") for r in sample_default]
    plt.errorbar(xpos, means, yerr=[lows, highs], fmt="o", capsize=4)
    plt.axhline(0, color="black", linewidth=1)
    plt.xticks(xpos, [f"seed {r['seed']}" for r in sample_default])
    plt.ylabel("Bootstrap weak Pd delta")
    plt.title("D5E bootstrap CI for weak Pd delta")
    plt.grid(True, alpha=0.3)
    out = FIG_DIR / "bootstrap_ci_plot.png"
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    figs.append(out)

    seed_ceiling = [r for r in ceiling_rows if str(r.get("seed")) != "mean"]
    plt.figure(figsize=(7, 4))
    xpos = np.arange(len(seed_ceiling))
    plt.bar(xpos - 0.2, [f(r, "balanced_mild_weak_hits") for r in seed_ceiling], width=0.4, label="balanced hits")
    plt.bar(xpos + 0.2, [f(r, "weak_weighting_weak_hits") for r in seed_ceiling], width=0.4, label="weak-weighting hits")
    for pos, row in enumerate(seed_ceiling):
        plt.axhline(f(row, "weak_n"), color="gray", linestyle="--", linewidth=0.8)
    plt.xticks(xpos, [f"seed {r['seed']}" for r in seed_ceiling])
    plt.ylabel("Weak target hits / weak_n")
    plt.title("D5E ceiling effect: weak hits already saturated")
    plt.legend()
    out = FIG_DIR / "ceiling_effect_visualization.png"
    plt.tight_layout()
    plt.savefig(out, dpi=180)
    plt.close()
    figs.append(out)

    return figs


def summarize_decision(
    ceiling_rows: list[dict[str, Any]],
    pfa_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    q_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    sample_rows: list[dict[str, Any]],
    weak_meta: dict[str, Any],
    outputs: list[tuple[Path, str]],
) -> tuple[dict[str, Any], str, str, str]:
    c_mean = next(r for r in ceiling_rows if str(r.get("seed")) == "mean")
    pfa_mean_rows = [r for r in pfa_rows if str(r.get("seed")) == "mean"]
    mask_mean_rows = [r for r in mask_rows if str(r.get("seed")) == "mean"]
    q_mean_rows = [r for r in q_rows if str(r.get("seed")) == "mean"]
    proxy_mean_rows = [r for r in proxy_rows if str(r.get("seed")) == "mean"]
    strict_rows = [r for r in pfa_mean_rows if f(r, "target_pfa") <= 1e-3]
    any_strict_advantage = any(f(r, "weak_pd_delta") > 0 and f(r, "weak_hit_delta") > 0 for r in strict_rows)
    any_mask_advantage = any(f(r, "weak_pd_delta") > 0 and f(r, "weak_hit_delta") > 0 for r in mask_mean_rows)
    q30 = min(q_mean_rows, key=lambda r: abs(f(r, "q_weak") - 0.30))
    hard_q = [r for r in q_mean_rows if f(r, "q_weak") <= 0.20]
    hard_q_advantage = any(f(r, "weak_pd_delta") > 0 and f(r, "weak_hit_delta") > 0 for r in hard_q)
    clean_proxy = next(r for r in proxy_mean_rows if r["doppler_box_mode"] == "clean_peak")
    non_clean_modes = [r for r in proxy_mean_rows if r["doppler_box_mode"] != "clean_peak"]
    proxy_optimistic = f(clean_proxy, "balanced_mild_weak_pd") >= 0.999 and any(
        f(r, "balanced_mild_weak_pd") < 0.999 or f(r, "overlap_ratio_vs_clean_peak_box") < 0.80 for r in non_clean_modes
    )
    sample_default = [r for r in sample_rows if abs(f(r, "target_pfa") - 1e-2) < 1e-12 and str(r.get("seed")) not in {"seed_sensitivity"}]
    weak_n_small = any(str(r.get("weak_n", "")) not in {"", "mean"} and i(r, "weak_n") < 100 for r in sample_default)
    decision = {
        "date": datetime.now().isoformat(),
        "stage": "D5E",
        "verdict": "NO-GO",
        "claim_supported": "no",
        "integrity_status": "pending_audit",
        "confidence": "medium",
        "ceiling_effect_present": bool(f(c_mean, "balanced_mild_weak_pd") >= 0.999 and f(c_mean, "balanced_mild_weak_miss_count") == 0),
        "q30_too_easy": bool(f(q30, "balanced_mild_weak_pd") >= 0.999),
        "strict_pfa_supports_weak_weighting": bool(any_strict_advantage),
        "mask_deformation_supports_weak_weighting": bool(any_mask_advantage),
        "harder_q_supports_weak_weighting": bool(hard_q_advantage),
        "rd_proxy_label_overly_optimistic": bool(proxy_optimistic),
        "weak_n_too_small_for_strong_claim": bool(weak_n_small),
        "d6_allowed": False,
        "continue_weak_weighting": False,
        "recommended_next": "Do not enter D6. Record D5D/D5E as limited negative RD-proxy evidence; only continue after fixing RD proxy/task difficulty.",
    }
    summary = f"""# D5E RD proxy and ceiling-effect diagnosis

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Input basis: D5D RD-only supplementary setup, re-run as a diagnostic only. This is not D6, not a new large model, and not a confirmed RD-performance evaluation.

## 1. Purpose

D5E diagnoses why D5D reported `balanced_mild weak Pd = 1.0` at the main PFA, leaving no room for weak weighting to show improvement.

## 2. Key Diagnostic Tables

### Ceiling Effect

{md_table(ceiling_rows, ['seed', 'weak_n', 'balanced_mild_weak_hits', 'weak_weighting_weak_hits', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'balanced_mild_weak_miss_count', 'ceiling_effect_present'])}

### PFA Sensitivity

{md_table(pfa_mean_rows, ['target_pfa', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta'])}

### Mask Width Sensitivity

{md_table(mask_mean_rows, ['range_mask_name', 'doppler_radius_bins', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'background_cell_count'])}

### Weak Threshold Difficulty

{md_table(q_mean_rows, ['q_weak', 'train_weak_threshold_db', 'train_weak_n', 'test_weak_n', 'mean_clean_rd_peak_db', 'mean_range_only_peak_db', 'mean_target_background_contrast_db', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

### RD Proxy Label Dependence

{md_table(proxy_mean_rows, ['doppler_box_mode', 'weak_projection_hit_rate_against_clean_peak', 'target_box_area_mean_weak', 'overlap_ratio_vs_clean_peak_box', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

## 3. Decision Summary

- Ceiling effect present: `{decision['ceiling_effect_present']}`
- q30 too easy under the current RD proxy: `{decision['q30_too_easy']}`
- Stricter PFA supports weak weighting: `{decision['strict_pfa_supports_weak_weighting']}`
- Mask deformation supports weak weighting: `{decision['mask_deformation_supports_weak_weighting']}`
- Harder q10/q20 subsets support weak weighting: `{decision['harder_q_supports_weak_weighting']}`
- RD proxy label overly optimistic: `{decision['rd_proxy_label_overly_optimistic']}`
- weak_n too small for strong claims: `{decision['weak_n_too_small_for_strong_claim']}`

## 4. Conservative Interpretation

The D5D NO-GO is strongly affected by a ceiling effect in the current RD proxy task: the `balanced_mild` model already hits all weak targets at PFA=1e-2. D5E does not find a robust weak-weighting advantage under stricter PFA thresholds, narrower/wider masks, or harder train-only weak-threshold subsets. RD target boxes remain proxy labels derived from range labels and Doppler projections rather than true Doppler/velocity ground truth. Therefore D5E reinforces a conservative NO-GO: do not enter D6, do not claim confirmed RD performance, and treat weak weighting as unsupported until the RD proxy/task difficulty is repaired.
"""
    decision_md = f"""# D5E RD proxy and ceiling-effect decision

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Verdict: **NO-GO**

Final route: **Do not enter D6. Do not continue weak weighting from the current evidence.**

## Decision Checks

| check | result |
|---|---:|
| ceiling effect present | {decision['ceiling_effect_present']} |
| q30 weak threshold too easy | {decision['q30_too_easy']} |
| stricter PFA supports weak weighting | {decision['strict_pfa_supports_weak_weighting']} |
| mask deformation supports weak weighting | {decision['mask_deformation_supports_weak_weighting']} |
| harder q thresholds support weak weighting | {decision['harder_q_supports_weak_weighting']} |
| RD proxy label overly optimistic | {decision['rd_proxy_label_overly_optimistic']} |
| weak_n too small for strong claim | {decision['weak_n_too_small_for_strong_claim']} |
| D6 allowed | {decision['d6_allowed']} |

## Rationale

At PFA=1e-2, `balanced_mild` has no missed weak targets in the current RD proxy task, so D5D cannot demonstrate an incremental weak-weighting gain. The stricter and alternative diagnostics do not produce a robust positive weak-hit delta for weak weighting. Because RD Doppler boxes are still proxy-derived and not true Doppler ground truth, the evidence ceiling is a limited RD-proxy sanity conclusion only.
"""
    handoff = f"""# 给 GPT 的单文件交接稿：D5E RD proxy and ceiling-effect diagnosis

你只需要把这个文件发给 GPT。它包含本轮 D5E 诊断的目标、约束、关键数据、文件路径和保守结论。

## 1. 本轮任务

D5E 用来解释 D5D 为什么出现 `balanced_mild weak Pd = 1.0`，导致 weak weighting 没有提升空间。D5E 是诊断，不是正式方法；不能进入 D6，不能加入 false alarm penalty，不能把 RD proxy 写成 confirmed RD performance。

## 2. 关键路径

- D5E 脚本：`{ROOT / 'experiments' / 'd5e_rd_proxy_ceiling_diagnosis.py'}`
- D5E 结果目录：`{RESULT_DIR}`
- D5E 图像目录：`{FIG_DIR}`
- 总结：`{SUMMARY_PATH}`
- 决策：`{DECISION_PATH}`
- 配置：`{CONFIG_PATH}`
- analyze-results：`{RESULT_DIR / 'D5E_ANALYZE_RESULTS.md'}`
- experiment-audit：`{RESULT_DIR / 'EXPERIMENT_AUDIT.md'}`
- result-to-claim：`{RESULT_DIR / 'RESULT_TO_CLAIM.md'}`

## 3. 核心结果

- ceiling effect 是否成立：`{decision['ceiling_effect_present']}`
- q30 weak threshold 是否太容易：`{decision['q30_too_easy']}`
- stricter PFA 是否给 weak weighting 优势：`{decision['strict_pfa_supports_weak_weighting']}`
- mask 变形是否给 weak weighting 优势：`{decision['mask_deformation_supports_weak_weighting']}`
- RD proxy label 是否过度乐观：`{decision['rd_proxy_label_overly_optimistic']}`
- weak_n 是否太小不适合强 claim：`{decision['weak_n_too_small_for_strong_claim']}`
- 是否允许 D6：`{decision['d6_allowed']}`
- 是否继续 weak weighting：`{decision['continue_weak_weighting']}`

## 4. 关键表格摘要

### Ceiling effect

{md_table(ceiling_rows, ['seed', 'weak_n', 'balanced_mild_weak_hits', 'weak_weighting_weak_hits', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'balanced_mild_weak_miss_count', 'ceiling_effect_present'])}

### PFA sensitivity mean rows

{md_table(pfa_mean_rows, ['target_pfa', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta'])}

### Mask sensitivity mean rows

{md_table(mask_mean_rows, ['range_mask_name', 'doppler_radius_bins', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

### Weak threshold difficulty mean rows

{md_table(q_mean_rows, ['q_weak', 'train_weak_threshold_db', 'train_weak_n', 'test_weak_n', 'mean_target_background_contrast_db', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

### RD proxy label dependence mean rows

{md_table(proxy_mean_rows, ['doppler_box_mode', 'weak_projection_hit_rate_against_clean_peak', 'overlap_ratio_vs_clean_peak_box', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

## 5. 保守结论，可写进项目报告

In the D5E diagnostic, the current RD-only proxy task shows a clear ceiling effect: under the D5D default clean-RD Doppler-peak projection and PFA=1e-2, `balanced_mild` already detects all weak targets, leaving no measurable room for weak weighting. Stricter PFA thresholds, mask-width perturbations, and harder train-only weak-target quantiles do not reveal a robust weak-weighting advantage. Because RD boxes are still proxy-derived from range labels and Doppler projections rather than true Doppler/velocity ground truth, D5E should be reported only as a limited RD-proxy diagnosis. The correct route remains NO-GO: do not enter D6 and do not claim confirmed RD performance.
"""
    return decision, summary, decision_md, handoff


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[tuple[Path, str]] = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    manifest, targets, clean_power, clean_range_db, _rd_for_fig = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    train_frames = np.asarray(train_all[:N_TRAIN_FRAMES], dtype=int)
    val_frames = np.asarray(val_all[:N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[:N_TEST_FRAMES], dtype=int)
    all_frames = np.asarray(sorted(set(train_frames.tolist()) | set(val_frames.tolist()) | set(test_frames.tolist())), dtype=int)

    clean_cfar_range = d1a.ca_cfar_score_1d_np(clean_power)
    contexts_1d_d5d = build_mask_context(clean_range_db, clean_cfar_range, targets)
    range_contexts = one_d_contexts_all(clean_range_db, clean_cfar_range, targets)
    default_range_ctx = contexts_1d_d5d["default"]
    frozen_splits, weak_meta = clean_peak_frozen_splits(default_range_ctx, targets, train_frames)
    weak_meta["counts"]["val"] = split_counts_for_frames(frozen_splits, targets, val_frames)
    weak_meta["counts"]["test"] = split_counts_for_frames(frozen_splits, targets, test_frames)
    weak_meta["dataset"] = str(ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1")
    weak_meta["diagnostic_stage"] = "D5E"

    rng = np.random.default_rng(RANDOM_SEED + 1700)
    clean_rd, inter_rd, inter_rows = compute_rd_maps(manifest, all_frames, TRAIN_SIR_NAMES, rng)
    train_x, train_y, train_rows = build_sample_arrays(train_frames, TRAIN_SIR_NAMES, clean_rd, inter_rd, "train")
    val_x, val_y, val_rows = build_sample_arrays(val_frames, TRAIN_SIR_NAMES, clean_rd, inter_rd, "val")
    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    norm_mean = float(norm_values.mean())
    norm_std = float(norm_values.std())

    default_rd_ctx = build_rd_context_variant(
        clean_rd,
        inter_rd,
        targets,
        default_range_ctx,
        frozen_splits,
        all_frames,
        range_mask_name="default",
        doppler_mode="clean_peak",
        doppler_radius=2,
    )

    training_rows: list[dict[str, Any]] = []
    training_summary: list[dict[str, Any]] = []
    models: dict[tuple[int, str], torch.nn.Module] = {}
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
        cases.append(case_from_by_frame(f"{label}_output", eval_frames, inter_by_frame, method=method, seed=seed, sir_name=EVAL_SIR_NAME))

    ceiling_rows = ceiling_effect_audit(cases, val_frames, test_frames, default_rd_ctx, targets)
    pfa_rows = pfa_sensitivity(cases, val_frames, test_frames, default_rd_ctx, targets)
    mask_rows = mask_width_sensitivity(cases, val_frames, test_frames, targets, clean_rd, inter_rd, range_contexts, frozen_splits, all_frames)
    q_rows = weak_threshold_difficulty(cases, val_frames, test_frames, train_frames, targets, clean_rd, inter_rd, default_range_ctx, all_frames)
    proxy_rows = proxy_label_dependence(cases, val_frames, test_frames, targets, clean_rd, inter_rd, default_range_ctx, frozen_splits, all_frames)
    sample_rows = sample_size_stability(cases, val_frames, test_frames, default_rd_ctx, targets)
    recon_rows = reconstruction_rows(cases, clean_rd, test_frames)
    figures = plot_outputs(
        pfa_rows,
        mask_rows,
        q_rows,
        proxy_rows,
        sample_rows,
        ceiling_rows,
        clean_rd,
        inter_rd,
        targets,
        default_rd_ctx,
        test_frames,
    )

    write_csv_versioned(RESULT_DIR / "d5e_ceiling_effect_audit.csv", ceiling_rows, "D5E ceiling effect audit", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_pfa_sensitivity.csv", pfa_rows, "D5E PFA sensitivity", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_rd_mask_width_sensitivity.csv", mask_rows, "D5E RD mask width sensitivity", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_weak_threshold_difficulty.csv", q_rows, "D5E weak threshold difficulty", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_rd_proxy_label_dependence.csv", proxy_rows, "D5E RD proxy label dependence", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_sample_size_stability.csv", sample_rows, "D5E sample size stability", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_training_summary.csv", training_summary, "D5E training summary", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_training_loss.csv", training_rows, "D5E training loss", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_reconstruction_metrics.csv", recon_rows, "D5E reconstruction metrics", outputs)
    write_csv_versioned(RESULT_DIR / "d5e_interference_manifest.csv", inter_rows, "D5E synthetic FMCW-like interference manifest", outputs)
    write_json_versioned(RESULT_DIR / "d5e_weak_thresholds.json", weak_meta, "D5E D5D-compatible train-only weak thresholds", outputs)

    decision, summary, decision_md, handoff = summarize_decision(
        ceiling_rows,
        pfa_rows,
        mask_rows,
        q_rows,
        proxy_rows,
        sample_rows,
        weak_meta,
        outputs,
    )

    config = {
        "stage": "D5E",
        "date": datetime.now().isoformat(),
        "device": str(device),
        "representation": "RD-only proxy diagnosis",
        "seeds": SEEDS,
        "train_sir_names": TRAIN_SIR_NAMES,
        "eval_sir_name": EVAL_SIR_NAME,
        "n_train_frames": N_TRAIN_FRAMES,
        "n_val_frames": N_VAL_FRAMES,
        "n_test_frames": N_TEST_FRAMES,
        "pfa_levels": PFA_LEVELS,
        "mask_range_names": MASK_RANGE_NAMES,
        "doppler_radii": DOPPLER_RADII,
        "weak_q_levels": WEAK_Q_LEVELS,
        "weak_weight": WEAK_WEIGHT,
        "lambda_rec": LAMBDA_REC,
        "split_definition": SPLIT_DEFINITION,
        "constraints": {
            "entered_d6": False,
            "false_alarm_penalty": False,
            "clean_identity_full_method": False,
            "proposed_full_loss": False,
            "detector_modified": False,
            "fixed_pfa_protocol_modified": False,
            "large_model": False,
            "rd_proxy_written_as_confirmed_performance": False,
        },
        "evaluation_type": "mixed_proxy",
        "projection_caveat": default_rd_ctx["projection_note"],
        "decision": decision,
        "result_dir": str(RESULT_DIR),
        "figure_dir": str(FIG_DIR),
    }
    write_json_versioned(CONFIG_PATH, config, "D5E config", outputs)
    write_text_versioned(SUMMARY_PATH, summary, "D5E RD proxy ceiling summary", outputs)
    write_text_versioned(DECISION_PATH, decision_md, "D5E RD proxy ceiling decision", outputs)
    write_text_versioned(GPT_HANDOFF_PATH, handoff, "D5E GPT handoff single-file report", outputs)
    for fig in figures:
        outputs.append((fig, "D5E diagnostic figure"))

    append_manifest(outputs, "/experiment-bridge")

    print(
        json.dumps(
            {
                "stage": "D5E",
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "summary": str(SUMMARY_PATH),
                "decision": str(DECISION_PATH),
                "gpt_handoff": str(GPT_HANDOFF_PATH),
                "verdict": decision["verdict"],
                "d6_allowed": decision["d6_allowed"],
                "outputs": len(outputs),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"D5E failed: {exc}", file=sys.stderr)
        raise
