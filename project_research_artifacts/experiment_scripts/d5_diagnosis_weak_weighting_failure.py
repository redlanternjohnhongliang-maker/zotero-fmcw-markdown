from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn

import d4_gao77_strong_baseline_sanity as d4
import d5_gao77_weak_target_weighted_sanity as d5
from d1a_gao77_clean_fixed_pfa_sanity import EXPECTED_ADC_SHAPE, ROOT, ca_cfar_score_1d_np, write_csv, write_json
from d1b_gao77_synthetic_interference_sanity import build_mask_context
from d1a_plus_mask_stress_test import target_hit
from d2a_gao77_small_model_sanity import (
    SimpleRangeFCN,
    build_frame_count_cache,
    evaluate_cases,
    generate_eval_interference,
    generate_samples,
    load_clean_data,
    load_split,
    write_model_summary,
)
from d3_gao77_baseline_sanity import pick_metric, reconstruction_metrics
from d3_rerun_gao77_baseline_sanity import md_table


RESULT_DIR = ROOT / "results" / "d5_diagnosis_weak_weighting_failure"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5_diagnosis_figures"
REPORT_PATH = ROOT / "refine-logs" / "D5_DIAGNOSIS_WEAK_WEIGHTING_FAILURE_REPORT.md"
D5_CHECK_DIR = ROOT / "results" / "d5_check_improvement_significance"

RANDOM_SEED = 20260626
PRIMARY_SIR = "medium"
PRIMARY_MASK = "default"
PRIMARY_SCOPE = "all"
PRIMARY_PFA = 1e-2
PRIMARY_SPLIT_DEFINITION = "clean_peak_percentile"

TRAIN_SAMPLE_SIZES = [600, 1000, 1500]
CAPACITY_TRAIN_SAMPLES = 600
CAPACITY_SPECS = [
    {"capacity": "current_simple_fcn_h128", "kind": "fcn", "hidden": 128},
    {"capacity": "wider_fcn_h256", "kind": "fcn", "hidden": 256},
    {"capacity": "shallow_unet1d_c16", "kind": "unet", "base": 16},
]


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def f(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return default
    return float(value)


def i(row: dict[str, Any], key: str, default: int = 0) -> int:
    value = row.get(key, "")
    if value in ("", None):
        return default
    return int(float(value))


class ShallowRangeUNet1D(nn.Module):
    def __init__(self, n_bins: int, base: int = 16) -> None:
        super().__init__()
        self.enc1 = nn.Sequential(
            nn.Conv1d(1, base, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(base, base, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        self.down = nn.AvgPool1d(kernel_size=2)
        self.enc2 = nn.Sequential(
            nn.Conv1d(base, base * 2, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(base * 2, base * 2, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        self.dec = nn.Sequential(
            nn.Conv1d(base * 3, base, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(base, 1, kernel_size=3, padding=1),
        )
        nn.init.zeros_(self.dec[-1].weight)
        nn.init.zeros_(self.dec[-1].bias)
        self.n_bins = n_bins

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        e1 = self.enc1(x)
        e2 = self.enc2(self.down(e1))
        up = torch.nn.functional.interpolate(e2, size=self.n_bins, mode="linear", align_corners=False)
        delta = self.dec(torch.cat([e1, up], dim=1))
        return x + delta


def make_model_factory(spec: dict[str, Any]) -> Callable[[int], nn.Module]:
    if spec["kind"] == "fcn":
        hidden = int(spec["hidden"])
        return lambda n_bins: SimpleRangeFCN(n_bins, hidden=hidden)
    if spec["kind"] == "unet":
        base = int(spec["base"])
        return lambda n_bins: ShallowRangeUNet1D(n_bins, base=base)
    raise ValueError(f"unknown capacity spec: {spec}")


def make_training_frame_sequence(
    train_pool: np.ndarray,
    requested_samples: int,
    sir_count: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, int, bool]:
    frames_needed = int(math.ceil(requested_samples / max(sir_count, 1)))
    pool = np.asarray(train_pool, dtype=int)
    if frames_needed <= pool.size:
        return np.sort(pool[:frames_needed]), frames_needed, False
    frames: list[int] = []
    while len(frames) < frames_needed:
        shuffled = rng.permutation(pool).astype(int).tolist()
        frames.extend(shuffled[: frames_needed - len(frames)])
    return np.asarray(frames, dtype=int), len(set(frames)), True


def prepare_base() -> dict[str, Any]:
    manifest, targets, clean_power, clean_db, _ = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    val_frames = np.asarray(val_all[: d4.N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[: d4.N_TEST_FRAMES], dtype=int)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    contexts = build_mask_context(clean_db, clean_cfar, targets)
    frame_count_cache = build_frame_count_cache(targets, contexts)
    rng_eval = np.random.default_rng(RANDOM_SEED + 9100)
    val_x, val_y, val_rows, _, _ = generate_samples(
        manifest, val_frames, d4.VAL_SIR_NAMES, "validation", clean_db, frame_count_cache, rng_eval
    )
    eval_val_inter_db, _, eval_val_rows = generate_eval_interference(
        manifest, val_frames, d4.EVAL_SIR_NAMES, rng_eval
    )
    eval_test_inter_db, _, eval_test_rows = generate_eval_interference(
        manifest, test_frames, d4.EVAL_SIR_NAMES, rng_eval
    )
    return {
        "manifest": manifest,
        "targets": targets,
        "clean_power": clean_power,
        "clean_db": clean_db,
        "contexts": contexts,
        "frame_count_cache": frame_count_cache,
        "train_pool": np.asarray(train_all, dtype=int),
        "val_frames": val_frames,
        "test_frames": test_frames,
        "val_x": val_x,
        "val_y": val_y,
        "val_rows": val_rows,
        "eval_val_inter_db": eval_val_inter_db,
        "eval_test_inter_db": eval_test_inter_db,
        "eval_val_rows": eval_val_rows,
        "eval_test_rows": eval_test_rows,
    }


def make_train_data(base: dict[str, Any], requested_samples: int) -> dict[str, Any]:
    rng_frames = np.random.default_rng(RANDOM_SEED + 12000)
    max_frames, unique_count, uses_repeats = make_training_frame_sequence(
        base["train_pool"], max(TRAIN_SAMPLE_SIZES), len(d4.TRAIN_SIR_NAMES), rng_frames
    )
    frames_needed = int(math.ceil(requested_samples / len(d4.TRAIN_SIR_NAMES)))
    train_frames = np.asarray(max_frames[:frames_needed], dtype=int)
    rng_train = np.random.default_rng(RANDOM_SEED + 13000)
    train_x, train_y, train_rows, _, _ = generate_samples(
        base["manifest"],
        train_frames,
        d4.TRAIN_SIR_NAMES,
        f"train_{requested_samples}",
        base["clean_db"],
        base["frame_count_cache"],
        rng_train,
    )
    if train_x.shape[0] > requested_samples:
        train_x = train_x[:requested_samples]
        train_y = train_y[:requested_samples]
        train_rows = train_rows[:requested_samples]
    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    return {
        **base,
        "train_frames": train_frames,
        "train_unique_frames": len(set(int(x) for x in train_frames.tolist())),
        "train_uses_repeated_frames": bool(uses_repeats or len(set(train_frames.tolist())) < len(train_frames)),
        "requested_train_samples": requested_samples,
        "actual_train_samples": int(train_x.shape[0]),
        "train_x": train_x,
        "train_y": train_y,
        "train_rows": train_rows,
        "norm_mean": float(norm_values.mean()),
        "norm_std": float(norm_values.std()),
    }


def with_model_factory(factory: Callable[[int], nn.Module]) -> None:
    d4.SimpleRangeFCN = factory
    d5.SimpleRangeFCN = factory


def restore_model_factory() -> None:
    d4.SimpleRangeFCN = SimpleRangeFCN
    d5.SimpleRangeFCN = SimpleRangeFCN


def rename_training_rows(rows: list[dict[str, Any]], label: str, extra: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        new_row = dict(row)
        new_row["baseline"] = label
        new_row.update(extra)
        out.append(new_row)
    return out


def rename_training_metrics(metrics: dict[str, Any], label: str, method: str, extra: dict[str, Any]) -> dict[str, Any]:
    out = dict(metrics)
    out["baseline"] = label
    out["method"] = method
    out.update(extra)
    return out


def train_pair(
    data: dict[str, Any],
    capacity_spec: dict[str, Any],
    label_prefix: str,
    device: torch.device,
    seed_offset_base: int,
) -> tuple[dict[str, nn.Module], list[dict[str, Any]], list[dict[str, Any]]]:
    factory = make_model_factory(capacity_spec)
    with_model_factory(factory)
    models: dict[str, nn.Module] = {}
    training_rows: list[dict[str, Any]] = []
    training_metrics: list[dict[str, Any]] = []
    extra = {
        "capacity": capacity_spec["capacity"],
        "requested_train_samples": data["requested_train_samples"],
        "actual_train_samples": data["actual_train_samples"],
        "train_unique_frames": data["train_unique_frames"],
        "train_uses_repeated_frames": data["train_uses_repeated_frames"],
    }
    try:
        balanced_label = f"{label_prefix}_balanced_mild"
        torch.manual_seed(RANDOM_SEED + seed_offset_base)
        balanced_model, balanced_rows, balanced_metrics = d4.train_strong_baseline(
            {"label": balanced_label, "family": "balanced", "balance": "mild"},
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
            seed_offset=seed_offset_base,
        )
        training_rows.extend(rename_training_rows(balanced_rows, balanced_label, extra))
        training_metrics.append(rename_training_metrics(balanced_metrics, balanced_label, "balanced_mild", extra))
        if balanced_model is not None:
            models[balanced_label] = balanced_model

        weak_label = f"{label_prefix}_weak_peak_w2p0"
        torch.manual_seed(RANDOM_SEED + seed_offset_base + 100)
        weak_model, weak_rows, weak_metrics = d5.train_weak_baseline(
            "clean_peak_percentile",
            2.0,
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
            seed_offset=seed_offset_base + 100,
        )
        training_rows.extend(rename_training_rows(weak_rows, weak_label, extra))
        training_metrics.append(rename_training_metrics(weak_metrics, weak_label, "weak_peak_w2p0", extra))
        if weak_model is not None:
            models[weak_label] = weak_model
    finally:
        restore_model_factory()
    return models, training_rows, training_metrics


def evaluate_model_group(data: dict[str, Any], models: dict[str, nn.Module], device: torch.device) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
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
    metrics["recon"] = reconstruction_metrics(case_arrays, data["clean_db"], data["clean_power"], data["test_frames"])
    return metrics, case_arrays


def extract_eval_rows(
    metrics: dict[str, list[dict[str, Any]]],
    model_meta: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in metrics["recon"]}
    rows: list[dict[str, Any]] = []
    for label, meta in model_meta.items():
        method = "weak_peak_w2p0" if label.endswith("weak_peak_w2p0") else "balanced_mild"
        for mask_name in ["narrow", "default"]:
            for scope in ["all", "non_overlap_only"]:
                for pfa_value in [1e-2, 1e-3]:
                    metric = pick_metric(
                        metrics["fixed"],
                        f"{label}_output",
                        PRIMARY_SIR,
                        mask_name=mask_name,
                        split_definition=PRIMARY_SPLIT_DEFINITION,
                        pfa=pfa_value,
                        scope=scope,
                    )
                    clean_metric = pick_metric(
                        metrics["fixed"],
                        f"{label}_model_clean",
                        "",
                        mask_name=mask_name,
                        split_definition=PRIMARY_SPLIT_DEFINITION,
                        pfa=pfa_value,
                        scope=scope,
                    )
                    output_rec = recon_lookup[(f"{label}_output", PRIMARY_SIR)]
                    clean_rec = recon_lookup[(f"{label}_model_clean", "")]
                    rows.append(
                        {
                            **meta,
                            "method": method,
                            "model_label": label,
                            "mask_name": mask_name,
                            "target_scope": scope,
                            "target_pfa": pfa_value,
                            "weak_n": metric["weak_n"],
                            "weak_hits": metric["weak_hits"],
                            "weak_miss": i(metric, "weak_n") - i(metric, "weak_hits"),
                            "weak_pd": metric["weak_pd"],
                            "mid_n": metric["mid_n"],
                            "mid_hits": metric["mid_hits"],
                            "mid_pd": metric["mid_pd"],
                            "strong_n": metric["strong_n"],
                            "strong_hits": metric["strong_hits"],
                            "strong_pd": metric["strong_pd"],
                            "overall_n": metric["overall_n"],
                            "overall_hits": metric["overall_hits"],
                            "overall_pd": metric["overall_pd"],
                            "f1": metric["f1"],
                            "measured_pfa": metric["measured_pfa"],
                            "false_alarm_count": metric["false_alarm_count"],
                            "background_cell_count": metric["background_cell_count"],
                            "mse_db_to_clean": output_rec["mse_db_to_clean"],
                            "magmse_db_to_clean": output_rec["magmse_db_to_clean"],
                            "model_clean_mse_db_to_clean": clean_rec["mse_db_to_clean"],
                            "model_clean_magmse_db_to_clean": clean_rec["magmse_db_to_clean"],
                            "target_peak_abs_bias_db_mean": metric["target_peak_abs_bias_db_mean"],
                            "clean_measured_pfa": clean_metric["measured_pfa"],
                            "clean_false_alarm_count": clean_metric["false_alarm_count"],
                        }
                    )
    return rows


def pair_rows(eval_rows: list[dict[str, Any]], group_keys: list[str]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in eval_rows:
        key = tuple(row[k] for k in group_keys + ["mask_name", "target_scope", "target_pfa"])
        groups[key].append(row)
    out: list[dict[str, Any]] = []
    for key, rows in sorted(groups.items()):
        balanced = next((r for r in rows if r["method"] == "balanced_mild"), None)
        weak = next((r for r in rows if r["method"] == "weak_peak_w2p0"), None)
        if balanced is None or weak is None:
            continue
        base = {k: balanced[k] for k in group_keys + ["mask_name", "target_scope", "target_pfa"]}
        out.append(
            {
                **base,
                "balanced_weak_n": balanced["weak_n"],
                "weak_weak_n": weak["weak_n"],
                "balanced_weak_hits": balanced["weak_hits"],
                "weak_weak_hits": weak["weak_hits"],
                "weak_hit_delta": i(weak, "weak_hits") - i(balanced, "weak_hits"),
                "balanced_weak_pd": balanced["weak_pd"],
                "weak_weighted_weak_pd": weak["weak_pd"],
                "weak_pd_delta": f(weak, "weak_pd") - f(balanced, "weak_pd"),
                "balanced_mid_pd": balanced["mid_pd"],
                "weak_weighted_mid_pd": weak["mid_pd"],
                "mid_pd_delta": f(weak, "mid_pd") - f(balanced, "mid_pd"),
                "balanced_strong_pd": balanced["strong_pd"],
                "weak_weighted_strong_pd": weak["strong_pd"],
                "strong_pd_delta": f(weak, "strong_pd") - f(balanced, "strong_pd"),
                "balanced_overall_pd": balanced["overall_pd"],
                "weak_weighted_overall_pd": weak["overall_pd"],
                "overall_pd_delta": f(weak, "overall_pd") - f(balanced, "overall_pd"),
                "balanced_measured_pfa": balanced["measured_pfa"],
                "weak_weighted_measured_pfa": weak["measured_pfa"],
                "measured_pfa_delta": f(weak, "measured_pfa") - f(balanced, "measured_pfa"),
                "balanced_false_alarm_count": balanced["false_alarm_count"],
                "weak_weighted_false_alarm_count": weak["false_alarm_count"],
                "false_alarm_count_delta": i(weak, "false_alarm_count") - i(balanced, "false_alarm_count"),
                "background_cell_count": balanced["background_cell_count"],
                "balanced_f1": balanced["f1"],
                "weak_weighted_f1": weak["f1"],
                "f1_delta": f(weak, "f1") - f(balanced, "f1"),
                "balanced_mse_db_to_clean": balanced["mse_db_to_clean"],
                "weak_weighted_mse_db_to_clean": weak["mse_db_to_clean"],
                "balanced_magmse_db_to_clean": balanced["magmse_db_to_clean"],
                "weak_weighted_magmse_db_to_clean": weak["magmse_db_to_clean"],
                "balanced_model_clean_mse_db_to_clean": balanced["model_clean_mse_db_to_clean"],
                "weak_weighted_model_clean_mse_db_to_clean": weak["model_clean_mse_db_to_clean"],
                "balanced_target_peak_abs_bias_db_mean": balanced["target_peak_abs_bias_db_mean"],
                "weak_weighted_target_peak_abs_bias_db_mean": weak["target_peak_abs_bias_db_mean"],
            }
        )
    return out


def primary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        r
        for r in rows
        if r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    ]


def target_level_hits(
    data: dict[str, Any],
    case_arrays: list[dict[str, Any]],
    balanced_label: str,
    weak_label: str,
) -> list[dict[str, Any]]:
    ctx = data["contexts"][PRIMARY_MASK]
    splits = ctx["splits"][PRIMARY_SPLIT_DEFINITION]
    intervals = ctx["intervals"]
    non_overlap = ctx["non_overlap_ids"]
    background_mask = ctx["background_mask"]
    lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    test_set = set(int(x) for x in data["test_frames"].tolist())
    out: list[dict[str, Any]] = []
    detections_by_label: dict[str, np.ndarray] = {}
    threshold_by_label: dict[str, float] = {}
    for label in [balanced_label, weak_label]:
        case = lookup[(f"{label}_output", PRIMARY_SIR)]
        scores = ca_cfar_score_1d_np(case["power"])
        threshold = float(np.quantile(scores[data["val_frames"]][background_mask[data["val_frames"]]], 1.0 - PRIMARY_PFA))
        detections_by_label[label] = scores >= threshold
        threshold_by_label[label] = threshold
    values = ctx["target_values"]
    for target in data["targets"]:
        tid = int(target.target_id)
        if target.frame_idx not in test_set or tid not in splits:
            continue
        if splits[tid] != "weak":
            continue
        balanced_hit = target_hit(detections_by_label[balanced_label], target, intervals)
        weak_hit = target_hit(detections_by_label[weak_label], target, intervals)
        if balanced_hit and weak_hit:
            status = "both_hit"
        elif (not balanced_hit) and weak_hit:
            status = "weak_only_gain"
        elif balanced_hit and (not weak_hit):
            status = "balanced_only_loss"
        else:
            status = "both_miss"
        tv = values.get(tid, {})
        out.append(
            {
                "row_type": "weak_target_hit_status",
                "target_id": tid,
                "frame_idx": target.frame_idx,
                "frame_id": target.frame_id,
                "source_sequence": target.source_sequence,
                "class_id": target.cls,
                "class_group": target.group,
                "range_bin": target.range_bin,
                "range_m": target.range_m,
                "azimuth_deg": target.azimuth_deg,
                "split_peak": splits[tid],
                "split_cfar_margin": ctx["splits"]["cfar_margin"].get(tid, ""),
                "in_non_overlap": tid in non_overlap,
                "target_peak_db": tv.get("target_peak_db", ""),
                "cfar_margin_db": tv.get("cfar_margin_db", ""),
                "balanced_hit": balanced_hit,
                "weak_weighted_hit": weak_hit,
                "hit_status": status,
                "balanced_threshold": threshold_by_label[balanced_label],
                "weak_weighted_threshold": threshold_by_label[weak_label],
            }
        )
    return out


def weak_definition_diagnostics(data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ctx = data["contexts"][PRIMARY_MASK]
    splits = ctx["splits"]
    values = ctx["target_values"]
    non_overlap = ctx["non_overlap_ids"]
    valid_tids = sorted(tid for tid, v in values.items() if v.get("valid_projection"))
    peak_weak = {tid for tid in valid_tids if splits["clean_peak_percentile"].get(tid) == "weak"}
    cfar_weak = {tid for tid in valid_tids if splits["cfar_margin"].get(tid) == "weak"}
    overlap = peak_weak & cfar_weak
    union = peak_weak | cfar_weak
    target_lookup = {int(t.target_id): t for t in data["targets"]}
    rows: list[dict[str, Any]] = []
    for name, weak_ids in [("clean_peak_percentile", peak_weak), ("cfar_margin", cfar_weak)]:
        split_counts = Counter(splits[name].get(tid, "") for tid in valid_tids)
        peaks = [float(values[tid]["target_peak_db"]) for tid in weak_ids]
        margins = [float(values[tid]["cfar_margin_db"]) for tid in weak_ids]
        rows.append(
            {
                "row_type": "definition_summary",
                "definition": name,
                "weak_n": len(weak_ids),
                "mid_n": split_counts["mid"],
                "strong_n": split_counts["strong"],
                "weak_overlap_with_other_definition_n": len(overlap),
                "weak_overlap_jaccard": len(overlap) / max(len(union), 1),
                "weak_non_overlap_n": sum(1 for tid in weak_ids if tid in non_overlap),
                "weak_overlap_mask_n": sum(1 for tid in weak_ids if tid not in non_overlap),
                "weak_overlap_mask_ratio": sum(1 for tid in weak_ids if tid not in non_overlap) / max(len(weak_ids), 1),
                "weak_target_peak_db_mean": float(np.mean(peaks)) if peaks else "",
                "weak_target_peak_db_std": float(np.std(peaks)) if peaks else "",
                "weak_cfar_margin_db_mean": float(np.mean(margins)) if margins else "",
                "weak_cfar_margin_db_std": float(np.std(margins)) if margins else "",
            }
        )
        seq_counts = Counter(target_lookup[tid].source_sequence for tid in weak_ids if tid in target_lookup)
        for seq, count in sorted(seq_counts.items()):
            rows.append({"row_type": "weak_count_by_sequence", "definition": name, "source_sequence": seq, "weak_n": count})
        group_counts = Counter(target_lookup[tid].group for tid in weak_ids if tid in target_lookup)
        for group, count in sorted(group_counts.items()):
            rows.append({"row_type": "weak_count_by_class_group", "definition": name, "class_group": group, "weak_n": count})
    overlap_rows: list[dict[str, Any]] = [
        {
            "row_type": "definition_overlap_summary",
            "clean_peak_weak_n": len(peak_weak),
            "cfar_margin_weak_n": len(cfar_weak),
            "both_weak_n": len(overlap),
            "clean_peak_only_n": len(peak_weak - cfar_weak),
            "cfar_margin_only_n": len(cfar_weak - peak_weak),
            "weak_definition_jaccard": len(overlap) / max(len(union), 1),
        }
    ]
    for tid in sorted(union):
        t = target_lookup.get(tid)
        tv = values[tid]
        overlap_rows.append(
            {
                "row_type": "weak_target_definition_membership",
                "target_id": tid,
                "frame_idx": t.frame_idx if t else "",
                "source_sequence": t.source_sequence if t else "",
                "class_group": t.group if t else "",
                "range_bin": t.range_bin if t else "",
                "clean_peak_weak": tid in peak_weak,
                "cfar_margin_weak": tid in cfar_weak,
                "in_non_overlap": tid in non_overlap,
                "target_peak_db": tv.get("target_peak_db", ""),
                "cfar_margin_db": tv.get("cfar_margin_db", ""),
            }
        )
    return rows, overlap_rows


def make_plots(
    scale_rows: list[dict[str, Any]],
    capacity_rows: list[dict[str, Any]],
    definition_rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, Any]],
    target_hit_rows: list[dict[str, Any]],
    case_arrays: list[dict[str, Any]],
    data: dict[str, Any],
    balanced_label: str,
    weak_label: str,
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    scale_primary = primary_rows(scale_rows)
    plt.figure(figsize=(7, 4), dpi=150)
    plt.plot(
        [int(r["actual_train_samples"]) for r in scale_primary],
        [float(r["weak_pd_delta"]) for r in scale_primary],
        marker="o",
        color="#2563eb",
    )
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("effective train samples")
    plt.ylabel("weak Pd gain over balanced_mild")
    plt.title("Weak Pd gain vs train size")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_pd_gain_vs_train_size.png")
    plt.close()

    cap_primary = primary_rows(capacity_rows)
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar([r["capacity"] for r in cap_primary], [float(r["weak_pd_delta"]) for r in cap_primary], color="#7c3aed")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("weak Pd gain over balanced_mild")
    plt.title("Weak Pd gain vs model capacity")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_pd_gain_vs_model_capacity.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar([str(r["actual_train_samples"]) for r in scale_primary], [int(r["weak_hit_delta"]) for r in scale_primary], color="#0891b2")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("effective train samples")
    plt.ylabel("weak hit count delta")
    plt.title("Hit count difference")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "hit_count_difference_plot.png")
    plt.close()

    summary = next(r for r in overlap_rows if r["row_type"] == "definition_overlap_summary")
    plt.figure(figsize=(6, 4), dpi=150)
    plt.bar(
        ["peak only", "both", "cfar-margin only"],
        [int(summary["clean_peak_only_n"]), int(summary["both_weak_n"]), int(summary["cfar_margin_only_n"])],
        color=["#16a34a", "#f59e0b", "#dc2626"],
    )
    plt.ylabel("target count")
    plt.title("Weak target definition overlap")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_target_definition_overlap_plot.png")
    plt.close()

    memberships = [r for r in overlap_rows if r.get("row_type") == "weak_target_definition_membership"]
    peak_vals = [float(r["target_peak_db"]) for r in memberships if r.get("clean_peak_weak") in (True, "True")]
    cfar_vals = [float(r["cfar_margin_db"]) for r in memberships if r.get("cfar_margin_weak") in (True, "True")]
    plt.figure(figsize=(9, 4), dpi=150)
    plt.subplot(1, 2, 1)
    plt.hist(peak_vals, bins=24, color="#16a34a", alpha=0.8)
    plt.xlabel("target peak dB")
    plt.ylabel("count")
    plt.title("clean-peak weak")
    plt.subplot(1, 2, 2)
    plt.hist(cfar_vals, bins=24, color="#dc2626", alpha=0.8)
    plt.xlabel("CFAR margin dB")
    plt.title("CFAR-margin weak")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_target_peak_margin_distribution.png")
    plt.close()

    non_overlap_rows = [
        r
        for r in scale_rows
        if r["target_scope"] == "non_overlap_only"
        and r["mask_name"] == PRIMARY_MASK
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    ]
    plt.figure(figsize=(7, 4), dpi=150)
    plt.bar(
        [str(r["actual_train_samples"]) for r in non_overlap_rows],
        [float(r["weak_pd_delta"]) for r in non_overlap_rows],
        color="#059669",
    )
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("effective train samples")
    plt.ylabel("non-overlap-only weak Pd gain")
    plt.title("Non-overlap-only gain comparison")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "non_overlap_only_gain_comparison.png")
    plt.close()

    examples = [r for r in target_hit_rows if r["hit_status"] in {"both_miss", "balanced_only_loss"}][:6]
    lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    clean_db = data["clean_db"]
    balanced_db = lookup[(f"{balanced_label}_output", PRIMARY_SIR)]["db"]
    weak_db = lookup[(f"{weak_label}_output", PRIMARY_SIR)]["db"]
    if examples:
        n = len(examples)
        plt.figure(figsize=(10, 2.4 * n), dpi=150)
        x = np.arange(clean_db.shape[1])
        for idx, row in enumerate(examples, 1):
            frame = int(row["frame_idx"])
            center = int(row["range_bin"])
            plt.subplot(n, 1, idx)
            plt.plot(x, clean_db[frame], label="clean", linewidth=1)
            plt.plot(x, balanced_db[frame], label="balanced", linewidth=1)
            plt.plot(x, weak_db[frame], label="weak_weighted", linewidth=1)
            plt.axvline(center, color="black", linestyle="--", linewidth=0.8)
            plt.xlim(max(0, center - 20), min(clean_db.shape[1] - 1, center + 20))
            plt.title(f"target {row['target_id']} {row['hit_status']}")
            if idx == 1:
                plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(FIG_DIR / "weak_target_miss_examples.png")
        plt.close()


def make_decision_summary(
    scale_rows: list[dict[str, Any]],
    capacity_rows: list[dict[str, Any]],
    definition_rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    scale_primary = primary_rows(scale_rows)
    capacity_primary = primary_rows(capacity_rows)
    best_scale = max(scale_primary, key=lambda r: float(r["weak_pd_delta"]))
    best_capacity = max(capacity_primary, key=lambda r: float(r["weak_pd_delta"]))
    definition_summary = [r for r in definition_rows if r["row_type"] == "definition_summary"]
    peak_summary = next(r for r in definition_summary if r["definition"] == "clean_peak_percentile")
    overlap_summary = next(r for r in overlap_rows if r["row_type"] == "definition_overlap_summary")
    scale_gain_reaches_bar = float(best_scale["weak_pd_delta"]) >= 0.02
    capacity_gain_reaches_bar = float(best_capacity["weak_pd_delta"]) >= 0.02
    non_overlap_support = any(
        r["target_scope"] == "non_overlap_only"
        and r["mask_name"] == PRIMARY_MASK
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
        and float(r["weak_pd_delta"]) > 0.0
        for r in scale_rows
    )
    pfa_1e3_support = any(
        r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - 1e-3) < 1e-12
        and float(r["weak_pd_delta"]) > 0.0
        for r in scale_rows
    )
    recommend_d6 = bool(
        (scale_gain_reaches_bar or capacity_gain_reaches_bar)
        and non_overlap_support
        and pfa_1e3_support
        and float(best_scale["weak_weighted_model_clean_mse_db_to_clean"]) < 0.1
    )
    if scale_gain_reaches_bar:
        main_diagnosis = "训练样本量可能是瓶颈之一，但仍需确认 non-overlap、narrow 与 PFA=1e-3 是否同步支持。"
    elif capacity_gain_reaches_bar:
        main_diagnosis = "simple FCN 容量可能限制了 weak weighting，需要先用轻量容量升级复核。"
    elif float(peak_summary["weak_overlap_mask_ratio"]) > 0.25:
        main_diagnosis = "weak target 定义明显受 range-only mask overlap 污染，优先修 weak 定义或升级 RD/RA 表示。"
    else:
        main_diagnosis = "当前设置下 weak weighting 没有显示稳定有效贡献，更接近负结果。"
    return [
        {
            "best_train_size_samples": best_scale["actual_train_samples"],
            "best_train_size_weak_pd_delta": best_scale["weak_pd_delta"],
            "best_train_size_weak_hit_delta": best_scale["weak_hit_delta"],
            "best_capacity": best_capacity["capacity"],
            "best_capacity_weak_pd_delta": best_capacity["weak_pd_delta"],
            "best_capacity_weak_hit_delta": best_capacity["weak_hit_delta"],
            "clean_peak_weak_overlap_mask_ratio": peak_summary["weak_overlap_mask_ratio"],
            "weak_definition_jaccard": overlap_summary["weak_definition_jaccard"],
            "scale_gain_reaches_0p02": scale_gain_reaches_bar,
            "capacity_gain_reaches_0p02": capacity_gain_reaches_bar,
            "non_overlap_support": non_overlap_support,
            "pfa_1e3_support": pfa_1e3_support,
            "recommend_d6": recommend_d6,
            "main_diagnosis": main_diagnosis,
            "next_action": (
                "可以谨慎重新考虑 D6，但只限于通过相同 robust 口径的配置。"
                if recommend_d6
                else "不进入 D6；优先修 weak target 定义、升级 RD/RA 表示，或把当前 range-only weak weighting 记录为负结果。"
            ),
        }
    ]


def write_report(
    scale_rows: list[dict[str, Any]],
    capacity_rows: list[dict[str, Any]],
    definition_rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
) -> str:
    decision = decision_rows[0]
    scale_primary = primary_rows(scale_rows)
    capacity_primary = primary_rows(capacity_rows)
    definition_summary = [r for r in definition_rows if r["row_type"] == "definition_summary"]
    report = f"""# D5-diagnosis：weak-target weighting 不稳定原因诊断

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D5-diagnosis。没有进入 D6，没有加入 false alarm penalty、clean identity full method 或 proposed full loss，没有引入 RDLR-Net / DiffRIM / RIMformer。

## 1. 总体结论

| 问题 | 结论 |
|---|---|
| 是否主要因为训练数据量不足 | {'有一定迹象' if decision['scale_gain_reaches_0p02'] else '当前未支持'} |
| 增大 train size 后 gain 是否扩大 | best gain = {float(decision['best_train_size_weak_pd_delta']):.4f}，best hit delta = {decision['best_train_size_weak_hit_delta']} |
| 模型容量增大后 gain 是否扩大 | best capacity = {decision['best_capacity']}，gain = {float(decision['best_capacity_weak_pd_delta']):.4f} |
| clean_peak_percentile weak target 定义是否可靠 | overlap-mask ratio = {float(decision['clean_peak_weak_overlap_mask_ratio']):.3f}；需谨慎 |
| CFAR-margin 是否仍不适合作为主定义 | 是；它与 clean_peak weak set 的 Jaccard = {float(decision['weak_definition_jaccard']):.3f}，且 D5 已显示 CFAR-margin 口径弱 Pd 很低 |
| weak targets 是否被 range-only overlap 污染 | {'是，污染偏明显' if float(decision['clean_peak_weak_overlap_mask_ratio']) > 0.25 else '存在但不是唯一解释'} |
| weak weighting 当前是否应视为负结果 | {'否，仍可谨慎复核' if bool(decision['recommend_d6']) else '是，当前 range-only 设置下更接近负结果'} |
| 是否还建议进入 D6 | {'是' if bool(decision['recommend_d6']) else '否'} |
| 下一步 | {decision['next_action']} |

## 2. Train Size 检查（主口径）

主口径：medium / default mask / all targets / PFA=1e-2。注意：D1A split 中非泄漏训练独立帧只有 300 帧；1000/1500 effective samples 使用重复训练帧生成新的 synthetic interference，因此检查的是训练样本/合成干扰样本量，不是新增真实 clean frame 多样性。

{md_table(scale_primary, ['actual_train_samples', 'train_unique_frames', 'train_uses_repeated_frames', 'balanced_weak_pd', 'weak_weighted_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'balanced_mid_pd', 'weak_weighted_mid_pd', 'balanced_strong_pd', 'weak_weighted_strong_pd', 'weak_weighted_measured_pfa', 'false_alarm_count_delta', 'weak_weighted_model_clean_mse_db_to_clean'])}

## 3. 容量检查（主口径）

{md_table(capacity_primary, ['capacity', 'actual_train_samples', 'balanced_weak_pd', 'weak_weighted_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'balanced_mid_pd', 'weak_weighted_mid_pd', 'balanced_strong_pd', 'weak_weighted_strong_pd', 'weak_weighted_measured_pfa', 'false_alarm_count_delta', 'weak_weighted_model_clean_mse_db_to_clean'])}

## 4. Weak Target 定义诊断

{md_table(definition_summary, ['definition', 'weak_n', 'mid_n', 'strong_n', 'weak_overlap_with_other_definition_n', 'weak_overlap_jaccard', 'weak_non_overlap_n', 'weak_overlap_mask_n', 'weak_overlap_mask_ratio', 'weak_target_peak_db_mean', 'weak_cfar_margin_db_mean'])}

## 5. 判断

- 如果 train size 或容量增加后 gain 没有达到 0.02-0.03，不能说 weak weighting 有稳定贡献。
- 如果 non-overlap-only 或 PFA=1e-3 不同步支持，不能进入 D6。
- 当前更合理的方向是先修 weak target 定义，或者升级到 RD/RA 表示来减少 range-only overlap 污染。
- 如果后续仍要推进，D6 必须建立在通过 robust 口径的配置上，而不是沿用 D5 原始的 1 个 target 差异。

## 6. 输出文件

结果目录：`G:\\mineru_output\\results\\d5_diagnosis_weak_weighting_failure`  
图像目录：`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d5_diagnosis_figures`
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return str(report_ts)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base = prepare_base()

    all_training_rows: list[dict[str, Any]] = []
    all_training_metrics: list[dict[str, Any]] = []
    scale_eval_rows: list[dict[str, Any]] = []
    scale_case_arrays_for_examples: list[dict[str, Any]] = []
    scale_data_for_examples: dict[str, Any] | None = None
    example_balanced_label = ""
    example_weak_label = ""

    current_spec = CAPACITY_SPECS[0]
    for idx, sample_count in enumerate(TRAIN_SAMPLE_SIZES):
        data = make_train_data(base, sample_count)
        prefix = f"scale_s{data['actual_train_samples']}_{current_spec['capacity']}"
        models, training_rows, training_metrics = train_pair(
            data,
            current_spec,
            prefix,
            device,
            seed_offset_base=5000 + idx * 200,
        )
        all_training_rows.extend(training_rows)
        all_training_metrics.extend(training_metrics)
        meta = {
            label: {
                "experiment_type": "train_size",
                "capacity": current_spec["capacity"],
                "requested_train_samples": data["requested_train_samples"],
                "actual_train_samples": data["actual_train_samples"],
                "train_unique_frames": data["train_unique_frames"],
                "train_uses_repeated_frames": data["train_uses_repeated_frames"],
            }
            for label in models
        }
        metrics, case_arrays = evaluate_model_group(data, models, device)
        scale_eval_rows.extend(extract_eval_rows(metrics, meta))
        if sample_count == TRAIN_SAMPLE_SIZES[-1]:
            scale_case_arrays_for_examples = case_arrays
            scale_data_for_examples = data
            example_balanced_label = f"{prefix}_balanced_mild"
            example_weak_label = f"{prefix}_weak_peak_w2p0"
        for label, model in models.items():
            write_model_summary(
                RESULT_DIR / f"d5_diagnosis_model_summary_{label}.txt",
                model,
                EXPECTED_ADC_SHAPE[0],
                device,
                data["norm_mean"],
                data["norm_std"],
            )

    capacity_eval_rows: list[dict[str, Any]] = []
    cap_data = make_train_data(base, CAPACITY_TRAIN_SAMPLES)
    for idx, spec in enumerate(CAPACITY_SPECS):
        prefix = f"capacity_{spec['capacity']}_s{cap_data['actual_train_samples']}"
        models, training_rows, training_metrics = train_pair(
            cap_data,
            spec,
            prefix,
            device,
            seed_offset_base=7000 + idx * 200,
        )
        all_training_rows.extend(training_rows)
        all_training_metrics.extend(training_metrics)
        meta = {
            label: {
                "experiment_type": "capacity",
                "capacity": spec["capacity"],
                "requested_train_samples": cap_data["requested_train_samples"],
                "actual_train_samples": cap_data["actual_train_samples"],
                "train_unique_frames": cap_data["train_unique_frames"],
                "train_uses_repeated_frames": cap_data["train_uses_repeated_frames"],
            }
            for label in models
        }
        metrics, _case_arrays = evaluate_model_group(cap_data, models, device)
        capacity_eval_rows.extend(extract_eval_rows(metrics, meta))
        for label, model in models.items():
            write_model_summary(
                RESULT_DIR / f"d5_diagnosis_model_summary_{label}.txt",
                model,
                EXPECTED_ADC_SHAPE[0],
                device,
                cap_data["norm_mean"],
                cap_data["norm_std"],
            )

    scale_rows = pair_rows(scale_eval_rows, ["experiment_type", "capacity", "requested_train_samples", "actual_train_samples", "train_unique_frames", "train_uses_repeated_frames"])
    capacity_rows = pair_rows(capacity_eval_rows, ["experiment_type", "capacity", "requested_train_samples", "actual_train_samples", "train_unique_frames", "train_uses_repeated_frames"])
    definition_rows, overlap_rows = weak_definition_diagnostics(base)
    if scale_data_for_examples is None:
        raise RuntimeError("missing example data")
    target_hit_rows = target_level_hits(
        scale_data_for_examples,
        scale_case_arrays_for_examples,
        example_balanced_label,
        example_weak_label,
    )
    overlap_rows.extend(target_hit_rows)
    decision_rows = make_decision_summary(scale_rows, capacity_rows, definition_rows, overlap_rows)

    make_plots(
        scale_rows,
        capacity_rows,
        definition_rows,
        overlap_rows,
        target_hit_rows,
        scale_case_arrays_for_examples,
        scale_data_for_examples,
        example_balanced_label,
        example_weak_label,
    )

    write_csv(RESULT_DIR / "d5_scale_gain_by_train_size.csv", scale_rows)
    write_csv(RESULT_DIR / "d5_capacity_check_summary.csv", capacity_rows)
    write_csv(RESULT_DIR / "d5_weak_definition_diagnostics.csv", definition_rows)
    write_csv(RESULT_DIR / "d5_weak_target_overlap_analysis.csv", overlap_rows)
    write_csv(RESULT_DIR / "d5_weak_target_hit_miss_examples.csv", target_hit_rows)
    write_csv(RESULT_DIR / "d5_diagnosis_training_loss.csv", all_training_rows)
    write_csv(RESULT_DIR / "d5_diagnosis_training_summary.csv", all_training_metrics)
    write_csv(RESULT_DIR / "d5_diagnosis_decision_summary.csv", decision_rows)
    write_json(
        RESULT_DIR / "d5_diagnosis_config.json",
        {
            "stage": "D5-diagnosis",
            "strict_limits": {
                "no_d6": True,
                "no_false_alarm_penalty": True,
                "no_clean_identity_full_method": True,
                "no_proposed_full_loss": True,
                "only_balanced_mild_and_weak_peak_w2p0": True,
                "no_large_model": True,
                "no_rdlr_diffirm_rimformer": True,
            },
            "primary_protocol": {
                "sir": PRIMARY_SIR,
                "mask": PRIMARY_MASK,
                "scope": PRIMARY_SCOPE,
                "pfa": PRIMARY_PFA,
                "split_definition": PRIMARY_SPLIT_DEFINITION,
            },
            "train_sample_sizes": TRAIN_SAMPLE_SIZES,
            "capacity_train_samples": CAPACITY_TRAIN_SAMPLES,
            "capacity_specs": CAPACITY_SPECS,
            "train_pool_unique_frames": int(base["train_pool"].size),
            "val_frames": int(base["val_frames"].size),
            "test_frames": int(base["test_frames"].size),
            "batch_size": d4.BATCH_SIZE,
            "tiny_steps": d4.TINY_STEPS,
            "small_epochs": d4.SMALL_EPOCHS,
            "bce_lr": d4.BCE_LR,
            "bce_temperature": d4.BCE_TEMPERATURE,
            "lambda_rec": d4.LAMBDA_REC,
            "device": str(device),
        },
    )
    report_ts = write_report(scale_rows, capacity_rows, definition_rows, overlap_rows, decision_rows)
    print(
        json.dumps(
            {
                "recommend_d6": decision_rows[0]["recommend_d6"],
                "main_diagnosis": decision_rows[0]["main_diagnosis"],
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "report": str(REPORT_PATH),
                "timestamped_report": report_ts,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
