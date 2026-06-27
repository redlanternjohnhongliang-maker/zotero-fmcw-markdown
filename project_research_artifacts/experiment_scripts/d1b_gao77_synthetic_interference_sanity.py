from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
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
from d1a_plus_mask_stress_test import (
    CFAR_GUARD,
    CFAR_TRAIN,
    MASK_CONFIGS,
    Target,
    assign_splits,
    build_masks,
    load_split,
    target_hit,
    target_peak_and_projection,
)


RESULT_DIR = ROOT / "results" / "d1b_gao77_synthetic_interference_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d1b_figures"
REPORT_PATH = ROOT / "refine-logs" / "D1B_GAO77_SYNTHETIC_INTERFERENCE_SANITY_REPORT.md"
RANDOM_SEED = 20260626
VALID_PFA_TARGETS = [1e-2, 1e-3]
SIR_CONFIGS = [
    {"sir_name": "light", "sir_db": 10.0, "num_interferers": 1},
    {"sir_name": "medium", "sir_db": 0.0, "num_interferers": 2},
    {"sir_name": "severe", "sir_db": -10.0, "num_interferers": 3},
]
ACTIVE_MASK_NAMES = {"narrow", "default"}
EPS = 1e-12


def db(x: float) -> float:
    return 10.0 * math.log10(max(float(x), EPS))


def valid_mask_1d(n_bins: int) -> np.ndarray:
    mask = np.zeros(n_bins, dtype=bool)
    mask[VALID_RANGE_MIN_BIN : min(VALID_RANGE_MAX_BIN + 1, n_bins)] = True
    return mask


def load_clean_data() -> tuple[list[dict[str, str]], list[Target], np.ndarray, np.ndarray, dict[int, np.ndarray], np.ndarray]:
    manifest = read_csv_dicts(MANIFEST_PATH)
    n_frames = len(manifest)
    n_bins = EXPECTED_ADC_SHAPE[0]
    range_power = np.zeros((n_frames, n_bins), dtype=np.float64)
    range_db = np.zeros((n_frames, n_bins), dtype=np.float64)
    clean_adc_power = np.zeros(n_frames, dtype=np.float64)
    sample_indices = set(np.linspace(0, n_frames - 1, 6, dtype=int).tolist())
    rd_for_fig: dict[int, np.ndarray] = {}
    targets: list[Target] = []
    target_id = 0

    for frame_idx, row in enumerate(manifest):
        mat = loadmat(RADAR_DIR / row["new_radar_file"])
        if "adcData" not in mat:
            raise RuntimeError(f"adcData missing in {row['new_radar_file']}")
        adc = mat["adcData"]
        if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
            raise RuntimeError(f"unexpected adcData shape {adc.shape} in {row['new_radar_file']}")
        clean_adc_power[frame_idx] = float(np.mean(np.abs(adc) ** 2))
        rp, rd_map, _ = radar_maps(adc)
        range_power[frame_idx] = rp
        range_db[frame_idx] = 10.0 * np.log10(rp + EPS)
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
    return manifest, targets, range_power, range_db, rd_for_fig, clean_adc_power


def make_interference(
    adc: np.ndarray,
    sir_db: float,
    num_interferers: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[dict[str, Any]], dict[str, float]]:
    samples, chirps, rx, tx = adc.shape
    n = (np.arange(samples, dtype=np.float64) - 0.5 * samples) / samples
    m = np.arange(chirps, dtype=np.float64)
    base = np.zeros(adc.shape, dtype=np.complex128)
    param_rows: list[dict[str, Any]] = []

    for interferer_id in range(num_interferers):
        phase0 = float(rng.uniform(0.0, 2.0 * np.pi))
        fast_freq = float(rng.uniform(-0.42, 0.42))
        slope_mismatch = float(rng.uniform(-7.5, 7.5))
        time_offset = float(rng.uniform(-0.35, 0.35))
        slow_freq = float(rng.uniform(-0.075, 0.075))
        amp_jitter = float(rng.uniform(0.75, 1.25))
        shifted = n - time_offset
        fast_phase = 2.0 * np.pi * (fast_freq * shifted + 0.5 * slope_mismatch * shifted * shifted)
        slow_phase = 2.0 * np.pi * slow_freq * m
        chirp_like = np.exp(1j * (phase0 + fast_phase[:, None] + slow_phase[None, :]))
        channel_phase = np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, size=(rx, tx)))
        base += amp_jitter * chirp_like[:, :, None, None] * channel_phase[None, None, :, :]
        param_rows.append(
            {
                "interferer_id": interferer_id,
                "phase0_rad": phase0,
                "fast_freq_norm": fast_freq,
                "slope_mismatch_norm": slope_mismatch,
                "time_offset_norm": time_offset,
                "slow_time_freq_cycles_per_chirp": slow_freq,
                "amp_jitter": amp_jitter,
            }
        )

    signal_power = float(np.mean(np.abs(adc) ** 2))
    base_power = float(np.mean(np.abs(base) ** 2))
    desired_interference_power = signal_power / (10.0 ** (sir_db / 10.0))
    scale = math.sqrt(desired_interference_power / max(base_power, EPS))
    interference = scale * base
    interference_power = float(np.mean(np.abs(interference) ** 2))
    achieved_sir_db = db(signal_power / max(interference_power, EPS))
    interfered = adc.astype(np.complex128, copy=True) + interference
    summary = {
        "clean_signal_power": signal_power,
        "interference_power": interference_power,
        "base_interference_power": base_power,
        "desired_interference_power": desired_interference_power,
        "scale": scale,
        "achieved_sir_db": achieved_sir_db,
    }
    return interfered, param_rows, summary


def generate_interfered_range_maps(
    manifest: list[dict[str, str]],
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[int, np.ndarray]]]:
    n_frames = len(manifest)
    n_bins = EXPECTED_ADC_SHAPE[0]
    rng = np.random.default_rng(RANDOM_SEED + 17)
    range_power_by_sir = {cfg["sir_name"]: np.zeros((n_frames, n_bins), dtype=np.float64) for cfg in SIR_CONFIGS}
    range_db_by_sir = {cfg["sir_name"]: np.zeros((n_frames, n_bins), dtype=np.float64) for cfg in SIR_CONFIGS}
    params_rows: list[dict[str, Any]] = []
    sir_frame_rows: list[dict[str, Any]] = []
    rd_samples: dict[str, dict[int, np.ndarray]] = {cfg["sir_name"]: {} for cfg in SIR_CONFIGS}
    sample_indices = set(np.linspace(0, n_frames - 1, 6, dtype=int).tolist())

    for frame_idx, row in enumerate(manifest):
        adc = loadmat(RADAR_DIR / row["new_radar_file"])["adcData"]
        for cfg in SIR_CONFIGS:
            sir_name = str(cfg["sir_name"])
            sir_db = float(cfg["sir_db"])
            num_interferers = int(cfg["num_interferers"])
            interfered_adc, param_rows, summary = make_interference(adc, sir_db, num_interferers, rng)
            rp, rd_map, _ = radar_maps(interfered_adc)
            range_power_by_sir[sir_name][frame_idx] = rp
            range_db_by_sir[sir_name][frame_idx] = 10.0 * np.log10(rp + EPS)
            if frame_idx in sample_indices:
                rd_samples[sir_name][frame_idx] = rd_map
            frame_summary = {
                "frame_idx": frame_idx,
                "frame_id": row["new_frame_id"],
                "source_sequence": row["source_sequence"],
                "sir_name": sir_name,
                "target_sir_db": sir_db,
                "num_interferers": num_interferers,
                **summary,
            }
            sir_frame_rows.append(frame_summary)
            for p in param_rows:
                params_rows.append({**frame_summary, **p})
    return range_power_by_sir, range_db_by_sir, params_rows, sir_frame_rows, rd_samples


def non_overlap_ids(intervals: dict[int, tuple[int, int, int]], targets: list[Target]) -> set[int]:
    by_frame: dict[int, list[Target]] = defaultdict(list)
    for t in targets:
        if t.target_id in intervals:
            by_frame[t.frame_idx].append(t)
    overlapped: set[int] = set()
    for frame_targets in by_frame.values():
        for i in range(len(frame_targets)):
            t1 = frame_targets[i]
            lo1, hi1, _ = intervals[t1.target_id]
            for j in range(i + 1, len(frame_targets)):
                t2 = frame_targets[j]
                lo2, hi2, _ = intervals[t2.target_id]
                if max(lo1, lo2) < min(hi1, hi2):
                    overlapped.add(t1.target_id)
                    overlapped.add(t2.target_id)
    return {tid for tid in intervals if tid not in overlapped}


def pfa_stats(detections: np.ndarray, background_mask: np.ndarray, test_idx: np.ndarray, n_boot: int = 300) -> dict[str, Any]:
    rng = np.random.default_rng(RANDOM_SEED + 31)
    frame_fa: list[int] = []
    frame_bg: list[int] = []
    frame_pfa: list[float] = []
    for idx in test_idx:
        bg = background_mask[idx]
        bg_count = int(bg.sum())
        fa = int(np.logical_and(detections[idx], bg).sum())
        if bg_count:
            frame_fa.append(fa)
            frame_bg.append(bg_count)
            frame_pfa.append(fa / bg_count)
    fa_arr = np.asarray(frame_fa, dtype=np.float64)
    bg_arr = np.asarray(frame_bg, dtype=np.float64)
    boot_values: list[float] = []
    if len(fa_arr):
        for _ in range(n_boot):
            choices = rng.integers(0, len(fa_arr), size=len(fa_arr))
            boot_values.append(float(fa_arr[choices].sum() / max(bg_arr[choices].sum(), 1.0)))
    return {
        "frame_level_pfa_mean": float(np.mean(frame_pfa)) if frame_pfa else "",
        "frame_level_pfa_std": float(np.std(frame_pfa)) if frame_pfa else "",
        "bootstrap_pfa_std": float(np.std(boot_values)) if boot_values else "",
        "bootstrap_pfa_ci_low": float(np.quantile(boot_values, 0.025)) if boot_values else "",
        "bootstrap_pfa_ci_high": float(np.quantile(boot_values, 0.975)) if boot_values else "",
    }


def evaluate_scores(
    scores: np.ndarray,
    threshold: float,
    target_mask: np.ndarray,
    background_mask: np.ndarray,
    targets: list[Target],
    intervals: dict[int, tuple[int, int, int]],
    splits: dict[int, str],
    test_idx: np.ndarray,
    target_scope: str,
    allowed_target_ids: set[int] | None,
) -> dict[str, Any]:
    detections = scores >= threshold
    bg_test = background_mask[test_idx]
    target_test = target_mask[test_idx]
    fa = int(np.logical_and(detections[test_idx], bg_test).sum())
    bg_count = int(bg_test.sum())
    tp = int(np.logical_and(detections[test_idx], target_test).sum())
    fp = fa
    fn = int(np.logical_and(~detections[test_idx], target_test).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    test_set = set(int(i) for i in test_idx.tolist())
    selected_targets = [
        t
        for t in targets
        if t.frame_idx in test_set
        and t.target_id in splits
        and t.target_id in intervals
        and (allowed_target_ids is None or t.target_id in allowed_target_ids)
    ]
    out: dict[str, Any] = {
        "target_scope": target_scope,
        "threshold": threshold,
        "measured_pfa": fa / max(bg_count, 1),
        "false_alarm_count": fa,
        "background_cell_count": bg_count,
        "tp_cells": tp,
        "fp_cells": fp,
        "fn_cells": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        **pfa_stats(detections, background_mask, test_idx),
    }
    for split_name in ["weak", "mid", "strong"]:
        split_targets = [t for t in selected_targets if splits[t.target_id] == split_name]
        hits = sum(1 for t in split_targets if target_hit(detections, t, intervals))
        out[f"{split_name}_n"] = len(split_targets)
        out[f"{split_name}_hits"] = hits
        out[f"{split_name}_pd"] = hits / len(split_targets) if split_targets else ""
        out[f"{split_name}_miss_rate"] = 1.0 - hits / len(split_targets) if split_targets else ""
    all_hits = sum(1 for t in selected_targets if target_hit(detections, t, intervals))
    out["overall_n"] = len(selected_targets)
    out["overall_hits"] = all_hits
    out["overall_pd"] = all_hits / len(selected_targets) if selected_targets else ""
    out["overall_miss_rate"] = 1.0 - all_hits / len(selected_targets) if selected_targets else ""
    return out


def evaluate_by_sequence(
    protocol: str,
    scores: np.ndarray,
    threshold: float,
    background_mask: np.ndarray,
    targets: list[Target],
    intervals: dict[int, tuple[int, int, int]],
    manifest: list[dict[str, str]],
    test_idx: np.ndarray,
    row_base: dict[str, Any],
) -> list[dict[str, Any]]:
    detections = scores >= threshold
    rows: list[dict[str, Any]] = []
    seq_by_idx = {i: row["source_sequence"] for i, row in enumerate(manifest)}
    test_set = set(int(i) for i in test_idx.tolist())
    for seq in sorted({row["source_sequence"] for row in manifest}):
        idxs = np.asarray([i for i in test_idx.tolist() if seq_by_idx[i] == seq], dtype=int)
        if idxs.size == 0:
            continue
        bg = background_mask[idxs]
        fa = int(np.logical_and(detections[idxs], bg).sum())
        bg_count = int(bg.sum())
        seq_targets = [t for t in targets if t.frame_idx in test_set and t.source_sequence == seq and t.target_id in intervals]
        hits = sum(1 for t in seq_targets if target_hit(detections, t, intervals))
        rows.append(
            {
                **row_base,
                "protocol": protocol,
                "source_sequence": seq,
                "test_frame_count": int(idxs.size),
                "background_cell_count": bg_count,
                "false_alarm_count": fa,
                "measured_pfa": fa / max(bg_count, 1),
                "target_count": len(seq_targets),
                "hit_count": hits,
                "pd": hits / len(seq_targets) if seq_targets else "",
            }
        )
    return rows


def evaluate_by_class_group(
    protocol: str,
    scores: np.ndarray,
    threshold: float,
    targets: list[Target],
    intervals: dict[int, tuple[int, int, int]],
    splits: dict[int, str],
    test_idx: np.ndarray,
    row_base: dict[str, Any],
    target_scope: str,
    allowed_target_ids: set[int] | None,
) -> list[dict[str, Any]]:
    detections = scores >= threshold
    test_set = set(int(i) for i in test_idx.tolist())
    rows: list[dict[str, Any]] = []
    for group in sorted(set(GAO77_CLASS_GROUP.values())):
        selected = [
            t
            for t in targets
            if t.frame_idx in test_set
            and t.group == group
            and t.target_id in intervals
            and t.target_id in splits
            and (allowed_target_ids is None or t.target_id in allowed_target_ids)
        ]
        hits = sum(1 for t in selected if target_hit(detections, t, intervals))
        rows.append(
            {
                **row_base,
                "protocol": protocol,
                "target_scope": target_scope,
                "class_group": group,
                "target_count": len(selected),
                "hit_count": hits,
                "pd": hits / len(selected) if selected else "",
            }
        )
    return rows


def range_noise_and_target_bias(
    clean_power: np.ndarray,
    inter_power: np.ndarray,
    clean_db: np.ndarray,
    inter_db: np.ndarray,
    background_mask: np.ndarray,
    targets: list[Target],
    intervals: dict[int, tuple[int, int, int]],
    eval_idx: np.ndarray,
    mask_name: str,
    sir_name: str,
    sir_db: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    idx = np.asarray(eval_idx, dtype=int)
    bg = background_mask[idx]
    clean_bg_power = float(np.mean(clean_power[idx][bg]))
    inter_bg_power = float(np.mean(inter_power[idx][bg]))
    clean_bg_db_values = clean_db[idx][bg]
    inter_bg_db_values = inter_db[idx][bg]
    noise_row = {
        "mask_name": mask_name,
        "sir_name": sir_name,
        "target_sir_db": sir_db,
        "clean_background_power_mean": clean_bg_power,
        "interfered_background_power_mean": inter_bg_power,
        "background_energy_increase_db": db(inter_bg_power / max(clean_bg_power, EPS)),
        "clean_noise_floor_db_median": float(np.median(clean_bg_db_values)),
        "interfered_noise_floor_db_median": float(np.median(inter_bg_db_values)),
        "noise_floor_change_db": float(np.median(inter_bg_db_values) - np.median(clean_bg_db_values)),
    }
    eval_set = set(int(i) for i in idx.tolist())
    deltas: list[float] = []
    for t in targets:
        if t.frame_idx not in eval_set or t.target_id not in intervals:
            continue
        lo, hi, _ = intervals[t.target_id]
        clean_peak = float(np.max(clean_db[t.frame_idx, lo:hi]))
        inter_peak = float(np.max(inter_db[t.frame_idx, lo:hi]))
        deltas.append(inter_peak - clean_peak)
    bias_row = {
        "mask_name": mask_name,
        "sir_name": sir_name,
        "target_sir_db": sir_db,
        "target_count": len(deltas),
        "target_peak_bias_db_mean": float(np.mean(deltas)) if deltas else "",
        "target_peak_bias_db_std": float(np.std(deltas)) if deltas else "",
        "target_peak_bias_db_median": float(np.median(deltas)) if deltas else "",
        "target_peak_abs_bias_db_mean": float(np.mean(np.abs(deltas))) if deltas else "",
    }
    return noise_row, bias_row


def summarize_sir(frame_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cfg in SIR_CONFIGS:
        sir_name = str(cfg["sir_name"])
        selected = [r for r in frame_rows if r["sir_name"] == sir_name]
        rows.append(
            {
                "sir_name": sir_name,
                "target_sir_db": float(cfg["sir_db"]),
                "num_interferers": int(cfg["num_interferers"]),
                "frame_count": len(selected),
                "clean_signal_power_mean": float(np.mean([r["clean_signal_power"] for r in selected])),
                "interference_power_mean": float(np.mean([r["interference_power"] for r in selected])),
                "achieved_sir_db_mean": float(np.mean([r["achieved_sir_db"] for r in selected])),
                "achieved_sir_db_std": float(np.std([r["achieved_sir_db"] for r in selected])),
                "achieved_sir_abs_error_db_mean": float(
                    np.mean([abs(float(r["achieved_sir_db"]) - float(cfg["sir_db"])) for r in selected])
                ),
            }
        )
    return rows


def build_mask_context(
    clean_range_db: np.ndarray,
    clean_cfar: np.ndarray,
    targets: list[Target],
) -> dict[str, dict[str, Any]]:
    n_frames, n_bins = clean_range_db.shape
    contexts: dict[str, dict[str, Any]] = {}
    for cfg in [c for c in MASK_CONFIGS if c["mask_name"] in ACTIVE_MASK_NAMES]:
        target_mask, guard_mask, background_mask, intervals = build_masks(targets, n_frames, n_bins, cfg)
        target_values = target_peak_and_projection(clean_range_db, clean_cfar, targets, intervals, int(cfg["guard_extra"]))
        peak_splits = assign_splits(target_values, "target_peak_db")
        margin_splits = assign_splits(target_values, "cfar_margin_db")
        contexts[str(cfg["mask_name"])] = {
            "cfg": cfg,
            "target_mask": target_mask,
            "guard_mask": guard_mask,
            "background_mask": background_mask,
            "intervals": intervals,
            "splits": {
                "clean_peak_percentile": peak_splits,
                "cfar_margin": margin_splits,
            },
            "non_overlap_ids": non_overlap_ids(intervals, targets),
            "target_values": target_values,
        }
    return contexts


def run_protocols(
    manifest: list[dict[str, str]],
    targets: list[Target],
    clean_range_power: np.ndarray,
    clean_range_db: np.ndarray,
    range_power_by_sir: dict[str, np.ndarray],
    range_db_by_sir: dict[str, np.ndarray],
    contexts: dict[str, dict[str, Any]],
    val_idx: np.ndarray,
    test_idx: np.ndarray,
) -> dict[str, list[dict[str, Any]]]:
    clean_cfar = ca_cfar_score_1d_np(clean_range_power, guard=CFAR_GUARD, train=CFAR_TRAIN)
    cfar_by_input: dict[str, np.ndarray] = {"clean": clean_cfar}
    for sir_name, power in range_power_by_sir.items():
        cfar_by_input[sir_name] = ca_cfar_score_1d_np(power, guard=CFAR_GUARD, train=CFAR_TRAIN)

    protocol_a_rows: list[dict[str, Any]] = []
    protocol_b_rows: list[dict[str, Any]] = []
    metrics_by_mask_rows: list[dict[str, Any]] = []
    non_overlap_rows: list[dict[str, Any]] = []
    by_sequence_rows: list[dict[str, Any]] = []
    by_class_rows: list[dict[str, Any]] = []
    noise_rows: list[dict[str, Any]] = []
    peak_bias_rows: list[dict[str, Any]] = []

    for mask_name, ctx in contexts.items():
        target_mask = ctx["target_mask"]
        background_mask = ctx["background_mask"]
        intervals = ctx["intervals"]
        for sir_cfg in SIR_CONFIGS:
            sir_name = str(sir_cfg["sir_name"])
            noise_row, bias_row = range_noise_and_target_bias(
                clean_range_power,
                range_power_by_sir[sir_name],
                clean_range_db,
                range_db_by_sir[sir_name],
                background_mask,
                targets,
                intervals,
                test_idx,
                mask_name,
                sir_name,
                float(sir_cfg["sir_db"]),
            )
            noise_rows.append(noise_row)
            peak_bias_rows.append(bias_row)

        for split_definition, splits in ctx["splits"].items():
            for pfa in VALID_PFA_TARGETS:
                clean_threshold = float(np.quantile(clean_cfar[val_idx][background_mask[val_idx]], 1.0 - pfa))
                protocol_a_inputs = [("clean", "clean", "", "")]
                protocol_a_inputs.extend(
                    [
                        (str(cfg["sir_name"]), "interfered", str(cfg["sir_name"]), float(cfg["sir_db"]))
                        for cfg in SIR_CONFIGS
                    ]
                )
                for input_key, input_type, sir_name, sir_db in protocol_a_inputs:
                    scores = cfar_by_input[input_key]
                    for target_scope, allowed_ids in [
                        ("all", None),
                        ("non_overlap_only", ctx["non_overlap_ids"]),
                    ]:
                        row_base = {
                            "protocol": "A_clean_threshold",
                            "mask_name": mask_name,
                            "split_definition": split_definition,
                            "target_pfa": pfa,
                            "threshold_source": "clean_validation_background",
                            "input_type": input_type,
                            "sir_name": sir_name,
                            "target_sir_db": sir_db,
                        }
                        metrics = evaluate_scores(
                            scores,
                            clean_threshold,
                            target_mask,
                            background_mask,
                            targets,
                            intervals,
                            splits,
                            test_idx,
                            target_scope,
                            allowed_ids,
                        )
                        row = {**row_base, **metrics}
                        protocol_a_rows.append(row)
                        if target_scope == "all":
                            metrics_by_mask_rows.append(row)
                            by_sequence_rows.extend(
                                evaluate_by_sequence(
                                    "A_clean_threshold",
                                    scores,
                                    clean_threshold,
                                    background_mask,
                                    targets,
                                    intervals,
                                    manifest,
                                    test_idx,
                                    row_base,
                                )
                            )
                        else:
                            non_overlap_rows.append(row)
                        by_class_rows.extend(
                            evaluate_by_class_group(
                                "A_clean_threshold",
                                scores,
                                clean_threshold,
                                targets,
                                intervals,
                                splits,
                                test_idx,
                                row_base,
                                target_scope,
                                allowed_ids,
                            )
                        )

                protocol_b_inputs = [("clean", "clean", "", "")]
                protocol_b_inputs.extend(
                    [
                        (str(cfg["sir_name"]), "interfered", str(cfg["sir_name"]), float(cfg["sir_db"]))
                        for cfg in SIR_CONFIGS
                    ]
                )
                for input_key, input_type, sir_name, sir_db in protocol_b_inputs:
                    scores = cfar_by_input[input_key]
                    recal_threshold = float(np.quantile(scores[val_idx][background_mask[val_idx]], 1.0 - pfa))
                    for target_scope, allowed_ids in [
                        ("all", None),
                        ("non_overlap_only", ctx["non_overlap_ids"]),
                    ]:
                        row_base = {
                            "protocol": "B_fixed_pfa_recalibrated",
                            "mask_name": mask_name,
                            "split_definition": split_definition,
                            "target_pfa": pfa,
                            "threshold_source": "input_specific_validation_background",
                            "input_type": input_type,
                            "sir_name": sir_name,
                            "target_sir_db": sir_db,
                        }
                        metrics = evaluate_scores(
                            scores,
                            recal_threshold,
                            target_mask,
                            background_mask,
                            targets,
                            intervals,
                            splits,
                            test_idx,
                            target_scope,
                            allowed_ids,
                        )
                        row = {**row_base, **metrics}
                        protocol_b_rows.append(row)
                        if target_scope == "all":
                            metrics_by_mask_rows.append(row)
                            by_sequence_rows.extend(
                                evaluate_by_sequence(
                                    "B_fixed_pfa_recalibrated",
                                    scores,
                                    recal_threshold,
                                    background_mask,
                                    targets,
                                    intervals,
                                    manifest,
                                    test_idx,
                                    row_base,
                                )
                            )
                        else:
                            non_overlap_rows.append(row)
                        by_class_rows.extend(
                            evaluate_by_class_group(
                                "B_fixed_pfa_recalibrated",
                                scores,
                                recal_threshold,
                                targets,
                                intervals,
                                splits,
                                test_idx,
                                row_base,
                                target_scope,
                                allowed_ids,
                            )
                        )

    return {
        "protocol_a": protocol_a_rows,
        "protocol_b": protocol_b_rows,
        "metrics_by_mask": metrics_by_mask_rows,
        "non_overlap": non_overlap_rows,
        "by_sequence": by_sequence_rows,
        "by_class": by_class_rows,
        "noise": noise_rows,
        "peak_bias": peak_bias_rows,
    }


def plot_outputs(
    clean_range_power: np.ndarray,
    range_power_by_sir: dict[str, np.ndarray],
    clean_rd_samples: dict[int, np.ndarray],
    rd_samples_by_sir: dict[str, dict[int, np.ndarray]],
    metrics: dict[str, list[dict[str, Any]]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    sample_idx = sorted(clean_rd_samples)[0]
    x = np.arange(clean_range_power.shape[1])
    plt.figure(figsize=(9, 4), dpi=150)
    plt.plot(x, 10.0 * np.log10(clean_range_power[sample_idx] + EPS), label="clean", linewidth=1.5)
    for cfg in SIR_CONFIGS:
        sir_name = str(cfg["sir_name"])
        plt.plot(x, 10.0 * np.log10(range_power_by_sir[sir_name][sample_idx] + EPS), label=f"{sir_name} ({cfg['sir_db']} dB)", alpha=0.85)
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.title("Clean vs interfered range profile")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_vs_interfered_range_profile.png")
    plt.close()

    for cfg in SIR_CONFIGS:
        sir_name = str(cfg["sir_name"])
        plt.figure(figsize=(10, 4), dpi=150)
        plt.subplot(1, 2, 1)
        plt.imshow(clean_rd_samples[sample_idx].T, aspect="auto", origin="lower", cmap="magma")
        plt.title("clean RD smoke")
        plt.xlabel("Range bin")
        plt.ylabel("Doppler bin")
        plt.subplot(1, 2, 2)
        plt.imshow(rd_samples_by_sir[sir_name][sample_idx].T, aspect="auto", origin="lower", cmap="magma")
        plt.title(f"{sir_name} interfered RD smoke")
        plt.xlabel("Range bin")
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"clean_vs_{sir_name}_rd_smoke.png")
        plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    noise_rows = [r for r in metrics["noise"] if r["mask_name"] == "default"]
    for r in noise_rows:
        plt.bar(r["sir_name"], float(r["noise_floor_change_db"]))
    plt.ylabel("Median noise floor change (dB)")
    plt.title("Background noise floor change vs SIR")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "background_noise_floor_histogram.png")
    plt.close()

    bias_rows = [r for r in metrics["peak_bias"] if r["mask_name"] == "default"]
    plt.figure(figsize=(9, 4), dpi=150)
    plt.bar([r["sir_name"] for r in bias_rows], [float(r["target_peak_bias_db_mean"]) for r in bias_rows])
    plt.ylabel("Mean target peak change (dB)")
    plt.title("Target peak change vs SIR")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_change_histogram.png")
    plt.close()

    pfa_rows = [
        r
        for r in metrics["protocol_b"]
        if r["target_scope"] == "all"
        and r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
        and r["input_type"] == "interfered"
    ]
    order = {str(cfg["sir_name"]): i for i, cfg in enumerate(SIR_CONFIGS)}
    pfa_rows = sorted(pfa_rows, key=lambda r: order[str(r["sir_name"])])
    plt.figure(figsize=(9, 4), dpi=150)
    plt.plot([r["sir_name"] for r in pfa_rows], [float(r["weak_pd"]) for r in pfa_rows], marker="o", label="weak")
    plt.plot([r["sir_name"] for r in pfa_rows], [float(r["mid_pd"]) for r in pfa_rows], marker="o", label="mid")
    plt.plot([r["sir_name"] for r in pfa_rows], [float(r["strong_pd"]) for r in pfa_rows], marker="o", label="strong")
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.title("Weak/mid/strong Pd vs SIR (Protocol B, default mask, PFA=1e-2)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_pd_vs_sir.png")
    plt.close()

    protocol_a_rows = [
        r
        for r in metrics["protocol_a"]
        if r["target_scope"] == "all"
        and r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
    ]
    labels = ["clean"] + [str(cfg["sir_name"]) for cfg in SIR_CONFIGS]
    pfa_by_label = {("clean" if r["input_type"] == "clean" else r["sir_name"]): float(r["measured_pfa"]) for r in protocol_a_rows}
    fa_by_label = {("clean" if r["input_type"] == "clean" else r["sir_name"]): float(r["false_alarm_count"]) for r in protocol_a_rows}
    plt.figure(figsize=(9, 4), dpi=150)
    plt.plot(labels, [pfa_by_label.get(label, np.nan) for label in labels], marker="o")
    plt.ylabel("Measured PFA")
    plt.title("Protocol A PFA vs SIR")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_vs_sir.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    plt.bar(labels, [fa_by_label.get(label, np.nan) for label in labels])
    plt.ylabel("False alarm count")
    plt.title("Protocol A false alarm count vs SIR")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "false_alarm_count_vs_sir.png")
    plt.close()

    compare_rows = [
        r
        for r in metrics["protocol_b"]
        if r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
        and (r["input_type"] == "clean" or r["sir_name"] == "severe")
    ]
    plt.figure(figsize=(8, 4), dpi=150)
    keys = []
    values = []
    for r in compare_rows:
        label = ("clean" if r["input_type"] == "clean" else "severe") + "/" + r["target_scope"]
        keys.append(label)
        values.append(float(r["weak_pd"]) if r["weak_pd"] != "" else np.nan)
    plt.bar(keys, values)
    plt.xticks(rotation=20, ha="right")
    plt.ylim(0, 1.05)
    plt.ylabel("Weak Pd")
    plt.title("All targets vs non-overlap-only")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "all_targets_vs_non_overlap_only.png")
    plt.close()

    for cfg in SIR_CONFIGS:
        sir_name = str(cfg["sir_name"])
        plt.figure(figsize=(8, 4), dpi=150)
        plt.plot(x, 10.0 * np.log10(clean_range_power[sample_idx] + EPS), label="clean")
        plt.plot(x, 10.0 * np.log10(range_power_by_sir[sir_name][sample_idx] + EPS), label=f"{sir_name} interfered")
        plt.title(f"{sir_name} interference visualization")
        plt.xlabel("Range bin")
        plt.ylabel("Power (dB)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(FIG_DIR / f"{sir_name}_interference_visualization.png")
        plt.close()


def pick_row(
    rows: list[dict[str, Any]],
    protocol: str,
    mask_name: str = "default",
    split_definition: str = "clean_peak_percentile",
    pfa: float = 0.01,
    input_type: str = "clean",
    sir_name: str = "",
    target_scope: str = "all",
) -> dict[str, Any]:
    for row in rows:
        if (
            row["protocol"] == protocol
            and row["mask_name"] == mask_name
            and row["split_definition"] == split_definition
            and abs(float(row["target_pfa"]) - pfa) < 1e-12
            and row["input_type"] == input_type
            and str(row["sir_name"]) == str(sir_name)
            and row["target_scope"] == target_scope
        ):
            return row
    raise KeyError((protocol, mask_name, split_definition, pfa, input_type, sir_name, target_scope))


def trend(values: list[float]) -> bool:
    return all(values[i] >= values[i + 1] - 1e-9 for i in range(len(values) - 1))


def write_report(
    sir_summary: list[dict[str, Any]],
    metrics: dict[str, list[dict[str, Any]]],
    contexts: dict[str, dict[str, Any]],
) -> tuple[bool, str]:
    rows_a = metrics["protocol_a"]
    rows_b = metrics["protocol_b"]
    clean_a = pick_row(rows_a, "A_clean_threshold")
    severe_a = pick_row(rows_a, "A_clean_threshold", input_type="interfered", sir_name="severe")
    clean_b = pick_row(rows_b, "B_fixed_pfa_recalibrated")
    severe_b = pick_row(rows_b, "B_fixed_pfa_recalibrated", input_type="interfered", sir_name="severe")
    light_b = pick_row(rows_b, "B_fixed_pfa_recalibrated", input_type="interfered", sir_name="light")
    medium_b = pick_row(rows_b, "B_fixed_pfa_recalibrated", input_type="interfered", sir_name="medium")
    narrow_clean_b = pick_row(rows_b, "B_fixed_pfa_recalibrated", mask_name="narrow")
    narrow_severe_b = pick_row(rows_b, "B_fixed_pfa_recalibrated", mask_name="narrow", input_type="interfered", sir_name="severe")
    non_clean_b = pick_row(rows_b, "B_fixed_pfa_recalibrated", target_scope="non_overlap_only")
    non_severe_b = pick_row(
        rows_b,
        "B_fixed_pfa_recalibrated",
        input_type="interfered",
        sir_name="severe",
        target_scope="non_overlap_only",
    )

    achieved_ok = all(float(r["achieved_sir_abs_error_db_mean"]) < 0.05 for r in sir_summary)
    sir_gradient_ok = trend([float(r["achieved_sir_db_mean"]) for r in sir_summary])
    noise_default = [r for r in metrics["noise"] if r["mask_name"] == "default"]
    noise_by_name = {r["sir_name"]: float(r["noise_floor_change_db"]) for r in noise_default}
    energy_by_name = {
        r["sir_name"]: float(r["background_energy_increase_db"])
        for r in noise_default
    }
    noise_up = all(noise_by_name[name] > 0.0 for name in ["light", "medium", "severe"]) and all(
        energy_by_name[name] > 0.0 for name in ["light", "medium", "severe"]
    )
    noise_gradient_ok = noise_by_name["light"] <= noise_by_name["medium"] <= noise_by_name["severe"]
    light_noise_mild = noise_by_name["light"] < 0.1
    weak_b_values = [
        float(clean_b["weak_pd"]),
        float(light_b["weak_pd"]),
        float(medium_b["weak_pd"]),
        float(severe_b["weak_pd"]),
    ]
    fixed_pfa_weak_down = weak_b_values[-1] < weak_b_values[0]
    protocol_a_false_alarm_up = float(severe_a["false_alarm_count"]) > float(clean_a["false_alarm_count"])
    protocol_a_weak_down = float(severe_a["weak_pd"]) < float(clean_a["weak_pd"])
    mask_consistent = (float(severe_b["weak_pd"]) - float(clean_b["weak_pd"])) * (
        float(narrow_severe_b["weak_pd"]) - float(narrow_clean_b["weak_pd"])
    ) >= 0
    non_overlap_consistent = (float(severe_b["weak_pd"]) - float(clean_b["weak_pd"])) * (
        float(non_severe_b["weak_pd"]) - float(non_clean_b["weak_pd"])
    ) >= 0
    pfa_chain_ok = all(
        0 <= float(row["measured_pfa"]) <= 1
        for row in rows_b
        if row["target_scope"] == "all" and str(row.get("measured_pfa", "")) != ""
    )
    all_zero_or_one = any(
        float(row["overall_pd"]) in (0.0, 1.0) and float(row["f1"]) in (0.0, 1.0)
        for row in rows_b
        if row["target_scope"] == "all" and row["input_type"] == "interfered"
    )
    d1b_pass = (
        achieved_ok
        and sir_gradient_ok
        and noise_up
        and noise_gradient_ok
        and fixed_pfa_weak_down
        and pfa_chain_ok
        and mask_consistent
        and non_overlap_consistent
        and not all_zero_or_one
    )
    next_recommendation = (
        "可以进入 D2 simple FCN / AENN 小 batch overfit，但 D2 必须继续保留 narrow/default 与 non-overlap-only 辅助统计。"
        if d1b_pass
        else "不建议进入 D2；应先修 synthetic interference model 或 fixed-PFA evaluation，使 fixed-PFA weak Pd 退化趋势更稳定。"
    )

    def md_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
        lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
        for row in rows:
            vals = []
            for col in cols:
                value = row.get(col, "")
                if isinstance(value, float):
                    vals.append(f"{value:.4f}")
                else:
                    try:
                        vals.append(f"{float(value):.4f}" if value != "" else "")
                    except Exception:
                        vals.append(str(value))
            lines.append("| " + " | ".join(vals) + " |")
        return "\n".join(lines)

    protocol_a_key = [
        r
        for r in rows_a
        if r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and r["target_scope"] == "all"
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
    ]
    protocol_b_key = [
        r
        for r in rows_b
        if r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and r["target_scope"] == "all"
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
    ]
    non_overlap_key = [
        r
        for r in rows_b
        if r["mask_name"] == "default"
        and r["split_definition"] == "clean_peak_percentile"
        and r["target_scope"] in {"all", "non_overlap_only"}
        and (r["input_type"] == "clean" or r["sir_name"] == "severe")
        and abs(float(r["target_pfa"]) - 0.01) < 1e-12
    ]
    context_rows = []
    for mask_name, ctx in contexts.items():
        context_rows.append(
            {
                "mask_name": mask_name,
                "target_cells_mean": float(ctx["target_mask"].sum(axis=1).mean()),
                "background_cells_mean": float(ctx["background_mask"].sum(axis=1).mean()),
                "target_count": len(ctx["intervals"]),
                "non_overlap_target_count": len(ctx["non_overlap_ids"]),
            }
        )

    report = f"""# D1B Gao77 Synthetic Interference Sanity 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D1B，仅 synthetic FMCW-like interference injection sanity + fixed-PFA evaluation  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次只执行 D1B。没有训练模型，没有进入 D2-D14，没有做干扰抑制模型，没有引入 AENN / FCN / RDLR-Net / DiffRIM / RIMformer，也没有下载新数据集。

D1B uses a simplified synthetic FMCW-like mutual interference model for sanity only. 本报告不把 D1B 结果包装成方法效果，只判断 ADC 层 synthetic interference 注入和 fixed-PFA 指标链路是否可用。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D1B 是否通过 | {'通过' if d1b_pass else '未通过'} |
| synthetic interference 是否成功注入 | {'是' if achieved_ok and noise_up else '不充分'} |
| achieved SIR 是否接近设定 | {'是' if achieved_ok else '否'} |
| range profile 是否出现可见干扰 | 是，图像已保存 |
| background noise floor 是否合理上升 | {'是（light 档 median 上升较轻微）' if noise_up and noise_gradient_ok and light_noise_mild else ('是' if noise_up and noise_gradient_ok else '不稳定')} |
| target peak 是否被明显污染 | 是，target peak bias 已统计 |
| Protocol A false alarm 是否增加 | {'是' if protocol_a_false_alarm_up else '否'} |
| Protocol A weak Pd 是否下降 | {'是' if protocol_a_weak_down else '否'} |
| Protocol B fixed-PFA weak Pd 是否下降 | {'是' if fixed_pfa_weak_down else '否'} |
| light / medium / severe 是否形成合理梯度 | {'是' if sir_gradient_ok and noise_gradient_ok else '否'} |
| narrow/default mask 趋势是否一致 | {'是' if mask_consistent else '否'} |
| all targets 与 non-overlap-only 是否一致 | {'是' if non_overlap_consistent else '否'} |
| 当前是否建议进入 D2 | {'是' if d1b_pass else '否'} |
| 下一步 | {next_recommendation} |

## 3. Achieved SIR

{md_table(sir_summary, ['sir_name', 'target_sir_db', 'num_interferers', 'clean_signal_power_mean', 'interference_power_mean', 'achieved_sir_db_mean', 'achieved_sir_db_std', 'achieved_sir_abs_error_db_mean'])}

## 4. Mask 口径

{md_table(context_rows, ['mask_name', 'target_cells_mean', 'background_cells_mean', 'target_count', 'non_overlap_target_count'])}

## 5. Protocol A：clean-threshold degradation test

默认 mask、clean_peak_percentile、PFA=1e-2：

{md_table(protocol_a_key, ['input_type', 'sir_name', 'measured_pfa', 'false_alarm_count', 'background_cell_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1'])}

Protocol A 的目的不是公平 fixed-PFA 比较，而是观察 clean threshold 固定后干扰是否造成虚警上升和检测退化。

## 6. Protocol B：fixed-PFA recalibrated test

默认 mask、clean_peak_percentile、PFA=1e-2：

{md_table(protocol_b_key, ['input_type', 'sir_name', 'threshold', 'measured_pfa', 'false_alarm_count', 'background_cell_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'bootstrap_pfa_std'])}

## 7. Noise Floor 与 Target Peak 污染

{md_table(noise_default, ['mask_name', 'sir_name', 'noise_floor_change_db', 'background_energy_increase_db', 'clean_noise_floor_db_median', 'interfered_noise_floor_db_median'])}

{md_table([r for r in metrics['peak_bias'] if r['mask_name'] == 'default'], ['mask_name', 'sir_name', 'target_count', 'target_peak_bias_db_mean', 'target_peak_bias_db_std', 'target_peak_abs_bias_db_mean'])}

## 8. All Targets vs Non-Overlap-Only

默认 mask、clean_peak_percentile、PFA=1e-2：

{md_table(non_overlap_key, ['input_type', 'sir_name', 'target_scope', 'weak_n', 'weak_pd', 'mid_n', 'mid_pd', 'strong_n', 'strong_pd', 'overall_n', 'overall_pd'])}

## 9. 异常检查

- per-sequence 指标已保存到 `d1b_metrics_by_sequence.csv`。D1A+ 已提示 per-sequence PFA 可能分化，因此 D2 前仍需持续观察。
- per-class-group 指标已保存到 `d1b_metrics_by_class_group.csv`。如果某类为空或目标数很少，不能单独解读成类别结论。
- narrow/default mask 均已输出；如果后续 D2 中二者趋势相反，应先回到 mask 设计，而不是训练模型。

## 10. 输出文件

结果目录：

`G:\\mineru_output\\results\\d1b_gao77_synthetic_interference_sanity`

图像目录：

`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d1b_figures`

关键文件：

- `d1b_interference_config.json`
- `d1b_interference_params_per_frame.csv`
- `d1b_achieved_sir_summary.csv`
- `d1b_protocol_a_clean_threshold_metrics.csv`
- `d1b_protocol_b_fixed_pfa_recalibrated_metrics.csv`
- `d1b_metrics_by_mask.csv`
- `d1b_metrics_non_overlap_only.csv`
- `d1b_noise_floor_summary.csv`
- `d1b_target_peak_bias_summary.csv`
- `d1b_metrics_by_sequence.csv`
- `d1b_metrics_by_class_group.csv`

## 11. D2 建议

{next_recommendation}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return d1b_pass, str(report_ts)


def main() -> None:
    np.random.seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    manifest, targets, clean_range_power, clean_range_db, clean_rd_samples, clean_adc_power = load_clean_data()
    _, val_idx, test_idx = load_split(len(manifest))
    clean_cfar = ca_cfar_score_1d_np(clean_range_power, guard=CFAR_GUARD, train=CFAR_TRAIN)
    contexts = build_mask_context(clean_range_db, clean_cfar, targets)
    range_power_by_sir, range_db_by_sir, params_rows, sir_frame_rows, rd_samples = generate_interfered_range_maps(manifest)
    sir_summary = summarize_sir(sir_frame_rows)
    metrics = run_protocols(
        manifest,
        targets,
        clean_range_power,
        clean_range_db,
        range_power_by_sir,
        range_db_by_sir,
        contexts,
        val_idx,
        test_idx,
    )
    plot_outputs(clean_range_power, range_power_by_sir, clean_rd_samples, rd_samples, metrics)

    config = {
        "stage": "D1B",
        "strict_limits": {
            "no_training": True,
            "no_d2_d14": True,
            "no_mitigation_model": True,
            "no_aenn_fcn_rdlr_diffirm_rimformer": True,
            "no_new_dataset": True,
            "range_only_primary": True,
            "ra_auxiliary_only": True,
        },
        "interference_model": "simplified synthetic FMCW-like mutual interference model for sanity only",
        "sir_configs": SIR_CONFIGS,
        "mask_names": sorted(ACTIVE_MASK_NAMES),
        "valid_pfa_targets": VALID_PFA_TARGETS,
        "cfar_guard": CFAR_GUARD,
        "cfar_train": CFAR_TRAIN,
        "subset_dir": str(ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1"),
        "clean_adc_power_mean": float(np.mean(clean_adc_power)),
        "n_frames": len(manifest),
        "n_targets": len(targets),
    }
    write_json(RESULT_DIR / "d1b_interference_config.json", config)
    write_csv(RESULT_DIR / "d1b_interference_params_per_frame.csv", params_rows)
    write_csv(RESULT_DIR / "d1b_achieved_sir_summary.csv", sir_summary)
    write_csv(RESULT_DIR / "d1b_protocol_a_clean_threshold_metrics.csv", metrics["protocol_a"])
    write_csv(RESULT_DIR / "d1b_protocol_b_fixed_pfa_recalibrated_metrics.csv", metrics["protocol_b"])
    write_csv(RESULT_DIR / "d1b_metrics_by_mask.csv", metrics["metrics_by_mask"])
    write_csv(RESULT_DIR / "d1b_metrics_non_overlap_only.csv", metrics["non_overlap"])
    write_csv(RESULT_DIR / "d1b_noise_floor_summary.csv", metrics["noise"])
    write_csv(RESULT_DIR / "d1b_target_peak_bias_summary.csv", metrics["peak_bias"])
    write_csv(RESULT_DIR / "d1b_metrics_by_sequence.csv", metrics["by_sequence"])
    write_csv(RESULT_DIR / "d1b_metrics_by_class_group.csv", metrics["by_class"])
    d1b_pass, report_ts = write_report(sir_summary, metrics, contexts)
    print(
        json.dumps(
            {
                "d1b_pass": d1b_pass,
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "report": str(REPORT_PATH),
                "timestamped_report": report_ts,
                "rows_protocol_a": len(metrics["protocol_a"]),
                "rows_protocol_b": len(metrics["protocol_b"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
