from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from d1a_gao77_clean_fixed_pfa_sanity import EXPECTED_ADC_SHAPE, ROOT, ca_cfar_score_1d_np, write_csv, write_json
from d1b_gao77_synthetic_interference_sanity import build_mask_context
from d2a_gao77_small_model_sanity import (
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
from d4_gao77_strong_baseline_sanity import (
    BCE_LR,
    BCE_TEMPERATURE,
    BATCH_SIZE,
    EVAL_SIR_NAMES,
    LAMBDA_REC,
    N_TEST_FRAMES,
    N_TRAIN_FRAMES,
    N_VAL_FRAMES,
    RANDOM_SEED,
    SMALL_EPOCHS,
    TINY_STEPS,
    TRAIN_SIR_NAMES,
    VAL_SIR_NAMES,
    train_strong_baseline,
)
from d5_gao77_weak_target_weighted_sanity import build_case_arrays, train_weak_baseline


RESULT_DIR = ROOT / "results" / "d5_check_improvement_significance"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5_check_figures"
REPORT_PATH = ROOT / "refine-logs" / "D5_CHECK_IMPROVEMENT_SIGNIFICANCE_REPORT.md"
D4_DIR = ROOT / "results" / "d4_gao77_strong_baseline_sanity"
D5_DIR = ROOT / "results" / "d5_gao77_weak_target_weighted_sanity"

PRIMARY_SIR = "medium"
PRIMARY_MASK = "default"
PRIMARY_SCOPE = "all"
PRIMARY_PFA = 1e-2
PRIMARY_SPLIT_DEFINITION = "clean_peak_percentile"
SEEDS = [0, 1, 2]


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


def safe_float(value: Any, default: float = 0.0) -> float:
    if value in ("", None):
        return default
    return float(value)


def make_alt_split(n_frames: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(RANDOM_SEED + 555)
    indices = np.arange(n_frames)
    rng.shuffle(indices)
    train_frames = np.sort(indices[:N_TRAIN_FRAMES])
    val_frames = np.sort(indices[N_TRAIN_FRAMES : N_TRAIN_FRAMES + N_VAL_FRAMES])
    test_frames = np.sort(indices[N_TRAIN_FRAMES + N_VAL_FRAMES : N_TRAIN_FRAMES + N_VAL_FRAMES + N_TEST_FRAMES])
    return train_frames, val_frames, test_frames


def pair_metric(
    rows: list[dict[str, Any]],
    input_type: str,
    *,
    sir_name: str = PRIMARY_SIR,
    mask_name: str = PRIMARY_MASK,
    scope: str = PRIMARY_SCOPE,
    pfa: float = PRIMARY_PFA,
    split_definition: str = PRIMARY_SPLIT_DEFINITION,
) -> dict[str, Any]:
    return pick_metric(
        rows,
        input_type,
        sir_name,
        mask_name=mask_name,
        split_definition=split_definition,
        pfa=pfa,
        scope=scope,
    )


def make_hit_count_comparison(fixed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for mask_name in ["narrow", "default"]:
        for scope in ["all", "non_overlap_only"]:
            for pfa_value in [1e-2, 1e-3]:
                balanced = pair_metric(
                    fixed_rows,
                    "balanced_mild_output",
                    mask_name=mask_name,
                    scope=scope,
                    pfa=pfa_value,
                )
                weak = pair_metric(
                    fixed_rows,
                    "weak_peak_w2p0_output",
                    mask_name=mask_name,
                    scope=scope,
                    pfa=pfa_value,
                )
                weak_delta = i(weak, "weak_hits") - i(balanced, "weak_hits")
                out.append(
                    {
                        "mask_name": mask_name,
                        "target_scope": scope,
                        "target_pfa": pfa_value,
                        "weak_n": balanced["weak_n"],
                        "balanced_weak_hits": balanced["weak_hits"],
                        "d5_weak_hits": weak["weak_hits"],
                        "weak_hit_delta": weak_delta,
                        "balanced_weak_miss": i(balanced, "weak_n") - i(balanced, "weak_hits"),
                        "d5_weak_miss": i(weak, "weak_n") - i(weak, "weak_hits"),
                        "balanced_weak_pd": balanced["weak_pd"],
                        "d5_weak_pd": weak["weak_pd"],
                        "weak_pd_delta": f(weak, "weak_pd") - f(balanced, "weak_pd"),
                        "mid_n": balanced["mid_n"],
                        "balanced_mid_hits": balanced["mid_hits"],
                        "d5_mid_hits": weak["mid_hits"],
                        "mid_hit_delta": i(weak, "mid_hits") - i(balanced, "mid_hits"),
                        "balanced_mid_pd": balanced["mid_pd"],
                        "d5_mid_pd": weak["mid_pd"],
                        "strong_n": balanced["strong_n"],
                        "balanced_strong_hits": balanced["strong_hits"],
                        "d5_strong_hits": weak["strong_hits"],
                        "strong_hit_delta": i(weak, "strong_hits") - i(balanced, "strong_hits"),
                        "balanced_strong_pd": balanced["strong_pd"],
                        "d5_strong_pd": weak["strong_pd"],
                        "overall_n": balanced["overall_n"],
                        "balanced_overall_hits": balanced["overall_hits"],
                        "d5_overall_hits": weak["overall_hits"],
                        "overall_hit_delta": i(weak, "overall_hits") - i(balanced, "overall_hits"),
                        "balanced_measured_pfa": balanced["measured_pfa"],
                        "d5_measured_pfa": weak["measured_pfa"],
                        "balanced_false_alarm_count": balanced["false_alarm_count"],
                        "d5_false_alarm_count": weak["false_alarm_count"],
                        "background_cell_count": balanced["background_cell_count"],
                        "statistically_weak_signal": abs(weak_delta) <= 2,
                    }
                )
    return out


def make_mask_robustness(hit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in hit_rows:
        out.append(
            {
                "mask_name": row["mask_name"],
                "target_scope": row["target_scope"],
                "target_pfa": row["target_pfa"],
                "balanced_weak_pd": row["balanced_weak_pd"],
                "d5_weak_pd": row["d5_weak_pd"],
                "weak_pd_delta": row["weak_pd_delta"],
                "weak_hit_delta": row["weak_hit_delta"],
                "d5_beats_balanced": float(row["weak_pd_delta"]) > 0,
                "evidence_level": "weak" if abs(int(row["weak_hit_delta"])) <= 2 else "moderate",
            }
        )
    return out


def prepare_data(split_mode: str) -> dict[str, Any]:
    manifest, targets, clean_power, clean_db, _ = load_clean_data()
    if split_mode == "original":
        train_all, val_all, test_all = load_split(len(manifest))
        train_frames = np.asarray(train_all[:N_TRAIN_FRAMES], dtype=int)
        val_frames = np.asarray(val_all[:N_VAL_FRAMES], dtype=int)
        test_frames = np.asarray(test_all[:N_TEST_FRAMES], dtype=int)
    elif split_mode == "alternate":
        train_frames, val_frames, test_frames = make_alt_split(len(manifest))
    else:
        raise ValueError(split_mode)

    clean_cfar = ca_cfar_score_1d_np(clean_power)
    contexts = build_mask_context(clean_db, clean_cfar, targets)
    frame_count_cache = build_frame_count_cache(targets, contexts)
    rng = np.random.default_rng(RANDOM_SEED + (900 if split_mode == "original" else 1900))
    train_x, train_y, train_rows, _, _ = generate_samples(
        manifest, train_frames, TRAIN_SIR_NAMES, "train", clean_db, frame_count_cache, rng
    )
    val_x, val_y, val_rows, _, _ = generate_samples(
        manifest, val_frames, VAL_SIR_NAMES, "validation", clean_db, frame_count_cache, rng
    )
    eval_val_inter_db, _, eval_val_rows = generate_eval_interference(manifest, val_frames, EVAL_SIR_NAMES, rng)
    eval_test_inter_db, _, eval_test_rows = generate_eval_interference(manifest, test_frames, EVAL_SIR_NAMES, rng)
    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    return {
        "manifest": manifest,
        "targets": targets,
        "clean_power": clean_power,
        "clean_db": clean_db,
        "contexts": contexts,
        "train_frames": train_frames,
        "val_frames": val_frames,
        "test_frames": test_frames,
        "train_x": train_x,
        "train_y": train_y,
        "train_rows": train_rows,
        "val_x": val_x,
        "val_y": val_y,
        "val_rows": val_rows,
        "eval_val_inter_db": eval_val_inter_db,
        "eval_test_inter_db": eval_test_inter_db,
        "eval_val_rows": eval_val_rows,
        "eval_test_rows": eval_test_rows,
        "norm_mean": float(norm_values.mean()),
        "norm_std": float(norm_values.std()),
    }


def rename_rows(rows: list[dict[str, Any]], label: str) -> list[dict[str, Any]]:
    renamed: list[dict[str, Any]] = []
    for row in rows:
        new_row = dict(row)
        new_row["baseline"] = label
        renamed.append(new_row)
    return renamed


def rename_metrics(metrics: dict[str, Any], label: str, method: str, seed: int | str, split_mode: str) -> dict[str, Any]:
    out = dict(metrics)
    out["baseline"] = label
    out["method"] = method
    out["seed"] = seed
    out["split_mode"] = split_mode
    return out


def train_pair_for_seed(data: dict[str, Any], seed: int, split_mode: str, device: torch.device) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    balanced_label = f"balanced_mild_seed{seed}" if split_mode == "original" else "balanced_mild_alt_split"
    weak_label = f"weak_peak_w2p0_seed{seed}" if split_mode == "original" else "weak_peak_w2p0_alt_split"
    models: dict[str, Any] = {}
    training_rows: list[dict[str, Any]] = []
    training_metrics: list[dict[str, Any]] = []

    torch.manual_seed(RANDOM_SEED + 3000 + int(seed if isinstance(seed, int) else 0))
    balanced_model, balanced_rows, balanced_metrics = train_strong_baseline(
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
        seed_offset=3000 + int(seed if isinstance(seed, int) else 0),
    )
    training_rows.extend(rename_rows(balanced_rows, balanced_label))
    training_metrics.append(rename_metrics(balanced_metrics, balanced_label, "balanced_mild", seed, split_mode))
    if balanced_model is not None:
        models[balanced_label] = balanced_model

    torch.manual_seed(RANDOM_SEED + 4000 + int(seed if isinstance(seed, int) else 0))
    weak_model, weak_rows, weak_metrics = train_weak_baseline(
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
        seed_offset=4000 + int(seed if isinstance(seed, int) else 0),
    )
    training_rows.extend(rename_rows(weak_rows, weak_label))
    training_metrics.append(rename_metrics(weak_metrics, weak_label, "weak_peak_w2p0", seed, split_mode))
    if weak_model is not None:
        models[weak_label] = weak_model

    return models, training_rows, training_metrics


def evaluate_models(data: dict[str, Any], models: dict[str, Any], device: torch.device) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    case_arrays = build_case_arrays(
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
    recon_rows = reconstruction_metrics(case_arrays, data["clean_db"], data["clean_power"], data["test_frames"])
    metrics["recon"] = recon_rows
    return metrics, case_arrays


def extract_seed_rows(
    fixed_rows: list[dict[str, Any]], recon_rows: list[dict[str, Any]], model_labels: list[str], split_mode: str
) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    rows: list[dict[str, Any]] = []
    for label in model_labels:
        method = "weak_peak_w2p0" if label.startswith("weak_peak") else "balanced_mild"
        seed = label.rsplit("seed", 1)[-1] if "seed" in label else "alt"
        for mask_name in ["narrow", "default"]:
            for scope in ["all", "non_overlap_only"]:
                for pfa_value in [1e-2, 1e-3]:
                    metric = pair_metric(
                        fixed_rows,
                        f"{label}_output",
                        mask_name=mask_name,
                        scope=scope,
                        pfa=pfa_value,
                    )
                    clean_metric = pair_metric(
                        fixed_rows,
                        f"{label}_model_clean",
                        sir_name="",
                        mask_name=mask_name,
                        scope=scope,
                        pfa=pfa_value,
                    )
                    output_rec = recon_lookup[(f"{label}_output", PRIMARY_SIR)]
                    clean_rec = recon_lookup[(f"{label}_model_clean", "")]
                    rows.append(
                        {
                            "row_kind": "seed",
                            "split_mode": split_mode,
                            "method": method,
                            "model_label": label,
                            "seed": seed,
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


def aggregate_seed_rows(seed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_keys = [
        "weak_pd",
        "mid_pd",
        "strong_pd",
        "overall_pd",
        "measured_pfa",
        "false_alarm_count",
        "mse_db_to_clean",
        "magmse_db_to_clean",
        "model_clean_mse_db_to_clean",
        "target_peak_abs_bias_db_mean",
    ]
    out: list[dict[str, Any]] = []
    groups: dict[tuple[str, str, str, float], list[dict[str, Any]]] = {}
    for row in seed_rows:
        if row["split_mode"] != "original":
            continue
        key = (str(row["method"]), str(row["mask_name"]), str(row["target_scope"]), float(row["target_pfa"]))
        groups.setdefault(key, []).append(row)
    for (method, mask_name, scope, pfa_value), rows in sorted(groups.items()):
        agg: dict[str, Any] = {
            "row_kind": "aggregate",
            "split_mode": "original",
            "method": method,
            "seed": "mean_std",
            "mask_name": mask_name,
            "target_scope": scope,
            "target_pfa": pfa_value,
            "n_seeds": len(rows),
        }
        for key in numeric_keys:
            values = np.asarray([safe_float(r.get(key), np.nan) for r in rows], dtype=np.float64)
            values = values[np.isfinite(values)]
            if values.size:
                agg[f"{key}_mean"] = float(values.mean())
                agg[f"{key}_std"] = float(values.std(ddof=1)) if values.size > 1 else 0.0
        out.append(agg)
    return out


def compare_seed_aggregates(seed_summary_rows: list[dict[str, Any]]) -> dict[str, Any]:
    aggs = [r for r in seed_summary_rows if r.get("row_kind") == "aggregate"]

    def find(method: str, mask: str = PRIMARY_MASK, scope: str = PRIMARY_SCOPE, pfa_value: float = PRIMARY_PFA) -> dict[str, Any]:
        for row in aggs:
            if (
                row["method"] == method
                and row["mask_name"] == mask
                and row["target_scope"] == scope
                and abs(float(row["target_pfa"]) - pfa_value) < 1e-12
            ):
                return row
        raise KeyError((method, mask, scope, pfa_value))

    balanced = find("balanced_mild")
    weak = find("weak_peak_w2p0")
    gain = f(weak, "weak_pd_mean") - f(balanced, "weak_pd_mean")
    balanced_std = f(balanced, "weak_pd_std")
    weak_std = f(weak, "weak_pd_std")
    return {
        "balanced_mean_weak_pd": balanced["weak_pd_mean"],
        "balanced_std_weak_pd": balanced["weak_pd_std"],
        "d5_mean_weak_pd": weak["weak_pd_mean"],
        "d5_std_weak_pd": weak["weak_pd_std"],
        "seed_mean_weak_pd_gain": gain,
        "gain_greater_than_both_std": gain > max(balanced_std, weak_std),
        "gain_greater_than_pooled_std": gain > float(np.sqrt(balanced_std**2 + weak_std**2)),
    }


def make_split_robustness_rows(split_seed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mask_name in ["narrow", "default"]:
        for scope in ["all", "non_overlap_only"]:
            for pfa_value in [1e-2, 1e-3]:
                subset = [
                    r
                    for r in split_seed_rows
                    if r["split_mode"] == "alternate"
                    and r["mask_name"] == mask_name
                    and r["target_scope"] == scope
                    and abs(float(r["target_pfa"]) - pfa_value) < 1e-12
                ]
                balanced = next(r for r in subset if r["method"] == "balanced_mild")
                weak = next(r for r in subset if r["method"] == "weak_peak_w2p0")
                rows.append(
                    {
                        "mask_name": mask_name,
                        "target_scope": scope,
                        "target_pfa": pfa_value,
                        "balanced_weak_pd": balanced["weak_pd"],
                        "d5_weak_pd": weak["weak_pd"],
                        "weak_pd_delta": f(weak, "weak_pd") - f(balanced, "weak_pd"),
                        "balanced_weak_hits": balanced["weak_hits"],
                        "d5_weak_hits": weak["weak_hits"],
                        "weak_hit_delta": i(weak, "weak_hits") - i(balanced, "weak_hits"),
                        "d5_beats_balanced": f(weak, "weak_pd") > f(balanced, "weak_pd"),
                    }
                )
    return rows


def plot_outputs(
    hit_rows: list[dict[str, Any]],
    seed_rows: list[dict[str, Any]],
    seed_agg_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    primary_aggs = [
        r
        for r in seed_agg_rows
        if r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    ]
    labels = [r["method"] for r in primary_aggs]
    means = [f(r, "weak_pd_mean") for r in primary_aggs]
    stds = [f(r, "weak_pd_std") for r in primary_aggs]
    plt.figure(figsize=(6.5, 4), dpi=150)
    plt.bar(labels, means, yerr=stds, capsize=5, color=["#6b7280", "#2563eb"])
    plt.ylabel("weak Pd mean +/- std")
    plt.title("D5-check: weak Pd over 3 seeds")
    plt.ylim(0, max(means + stds + [0.05]) * 1.2)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_pd_mean_std.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    xs = np.arange(len(hit_rows))
    labels = [f"{r['mask_name']}\n{r['target_scope']}\nPFA={r['target_pfa']}" for r in hit_rows]
    plt.bar(xs, [int(r["weak_hit_delta"]) for r in hit_rows], color="#0891b2")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(xs, labels, rotation=35, ha="right", fontsize=7)
    plt.ylabel("D5 - balanced weak hit count")
    plt.title("Hit count difference")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "hit_count_difference.png")
    plt.close()

    primary_seed = [
        r
        for r in seed_rows
        if r["split_mode"] == "original"
        and r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    ]
    plt.figure(figsize=(7, 4), dpi=150)
    for method in ["balanced_mild", "weak_peak_w2p0"]:
        ys = [f(r, "weak_pd") for r in primary_seed if r["method"] == method]
        plt.plot(SEEDS, ys, marker="o", label=method)
    plt.xlabel("seed")
    plt.ylabel("weak Pd")
    plt.title("balanced_mild vs weak_peak_w2p0")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "balanced_vs_weak_peak_w2p0_comparison.png")
    plt.close()

    plt.figure(figsize=(9, 4), dpi=150)
    labels = [f"{r['mask_name']}\n{r['target_scope']}\nPFA={r['target_pfa']}" for r in mask_rows]
    xs = np.arange(len(labels))
    plt.bar(xs, [float(r["weak_pd_delta"]) for r in mask_rows], color="#4f46e5")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(xs, labels, rotation=35, ha="right", fontsize=7)
    plt.ylabel("weak Pd delta")
    plt.title("Mask/PFA robustness delta")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "mask_robustness_comparison.png")
    plt.close()

    non_overlap = [r for r in mask_rows if r["target_scope"] == "non_overlap_only"]
    plt.figure(figsize=(7, 4), dpi=150)
    labels = [f"{r['mask_name']}\nPFA={r['target_pfa']}" for r in non_overlap]
    xs = np.arange(len(labels))
    plt.bar(xs, [float(r["weak_pd_delta"]) for r in non_overlap], color="#059669")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(xs, labels, rotation=25, ha="right")
    plt.ylabel("weak Pd delta")
    plt.title("Non-overlap-only comparison")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "non_overlap_only_comparison.png")
    plt.close()


def make_decision(
    hit_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    seed_decision: dict[str, Any],
    seed_summary_rows: list[dict[str, Any]],
    split_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    primary_hit = next(
        r
        for r in hit_rows
        if r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    )
    narrow_support = all(
        float(r["weak_pd_delta"]) > 0
        for r in mask_rows
        if r["mask_name"] == "narrow" and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    )
    default_support = all(
        float(r["weak_pd_delta"]) > 0
        for r in mask_rows
        if r["mask_name"] == "default" and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    )
    non_overlap_support = all(
        float(r["weak_pd_delta"]) > 0
        for r in mask_rows
        if r["target_scope"] == "non_overlap_only" and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    )
    pfa_1e3_support = all(float(r["weak_pd_delta"]) > 0 for r in mask_rows if abs(float(r["target_pfa"]) - 1e-3) < 1e-12)
    clean_rows = [
        r
        for r in seed_summary_rows
        if r.get("row_kind") == "aggregate"
        and r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    ]
    weak_clean = next(r for r in clean_rows if r["method"] == "weak_peak_w2p0")
    clean_no_harm_ok = f(weak_clean, "model_clean_mse_db_to_clean_mean") < 0.1
    split_primary = next(
        r
        for r in split_rows
        if r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    )
    recommend_d6 = bool(
        seed_decision["seed_mean_weak_pd_gain"] > 0
        and seed_decision["gain_greater_than_both_std"]
        and int(primary_hit["weak_hit_delta"]) > 1
        and narrow_support
        and default_support
        and non_overlap_support
        and pfa_1e3_support
        and clean_no_harm_ok
    )
    if recommend_d6:
        repair = "可进入 D6，但仍需把 false alarm / peak inflation 作为主检查"
    else:
        repair = "暂不建议进入 D6；优先修 weak target 定义，并检查模型容量或升级 RD/RA 表示，当前 weak weighting 更接近弱证据/负结果"
    return {
        "primary_weak_n": primary_hit["weak_n"],
        "primary_balanced_weak_hits": primary_hit["balanced_weak_hits"],
        "primary_d5_weak_hits": primary_hit["d5_weak_hits"],
        "primary_weak_hit_delta": primary_hit["weak_hit_delta"],
        "primary_weak_pd_delta": primary_hit["weak_pd_delta"],
        "statistically_weak_signal": bool(primary_hit["statistically_weak_signal"]),
        **seed_decision,
        "narrow_support": narrow_support,
        "default_support": default_support,
        "non_overlap_support": non_overlap_support,
        "pfa_1e3_support": pfa_1e3_support,
        "clean_no_harm_ok": clean_no_harm_ok,
        "alternate_split_primary_gain": split_primary["weak_pd_delta"],
        "alternate_split_support": bool(split_primary["d5_beats_balanced"]),
        "recommend_d6": recommend_d6,
        "next_action": repair,
    }


def write_report(
    hit_rows: list[dict[str, Any]],
    mask_rows: list[dict[str, Any]],
    seed_summary_rows: list[dict[str, Any]],
    split_rows: list[dict[str, Any]],
    decision: dict[str, Any],
) -> str:
    primary_hit = next(
        r
        for r in hit_rows
        if r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    )
    primary_seed_rows = [
        r
        for r in seed_summary_rows
        if r.get("row_kind") == "aggregate"
        and r["mask_name"] == PRIMARY_MASK
        and r["target_scope"] == PRIMARY_SCOPE
        and abs(float(r["target_pfa"]) - PRIMARY_PFA) < 1e-12
    ]
    key_mask_rows = [
        r
        for r in mask_rows
        if (r["mask_name"], r["target_scope"], float(r["target_pfa"]))
        in {
            ("default", "all", 1e-2),
            ("narrow", "all", 1e-2),
            ("default", "non_overlap_only", 1e-2),
            ("default", "all", 1e-3),
        }
    ]
    report = f"""# D5-check Improvement Significance 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D5-check，仅检查 D5 weak-target-weighted improvement significance  
边界：没有进入 D6，没有加入 false alarm penalty、clean identity full method 或 proposed full loss。

## 1. 总体结论

| 问题 | 结论 |
|---|---|
| D5 的 weak Pd 提升对应多检测了几个 weak target | {primary_hit['weak_hit_delta']} 个 |
| 是否可能只是 1 个或少数目标造成 | {'是' if decision['statistically_weak_signal'] else '否'} |
| 是否标记为 statistically weak signal | {'是' if decision['statistically_weak_signal'] else '否'} |
| 3 seeds 下 D5 平均是否超过 balanced_mild | {'是' if float(decision['seed_mean_weak_pd_gain']) > 0 else '否'} |
| 提升是否大于随机 seed std | {'是' if decision['gain_greater_than_both_std'] else '否'} |
| narrow/default mask 是否一致 | {'是' if decision['narrow_support'] and decision['default_support'] else '否'} |
| all/non-overlap-only 是否一致 | {'是' if decision['non_overlap_support'] else '否'} |
| PFA=1e-3 下是否仍有提升 | {'是' if decision['pfa_1e3_support'] else '否'} |
| clean no-harm 是否正常 | {'是' if decision['clean_no_harm_ok'] else '否'} |
| 是否建议继续 D6 | {'是' if decision['recommend_d6'] else '否'} |
| 下一步 | {decision['next_action']} |

## 2. Hit-count 差异

主口径：medium / default mask / all targets / PFA=1e-2。

| 指标 | balanced_mild | weak_peak_w2p0 | 差异 |
|---|---:|---:|---:|
| weak target 总数 | {primary_hit['weak_n']} | {primary_hit['weak_n']} | 0 |
| weak target hit count | {primary_hit['balanced_weak_hits']} | {primary_hit['d5_weak_hits']} | {primary_hit['weak_hit_delta']} |
| weak target miss count | {primary_hit['balanced_weak_miss']} | {primary_hit['d5_weak_miss']} | {int(primary_hit['d5_weak_miss']) - int(primary_hit['balanced_weak_miss'])} |
| weak Pd | {float(primary_hit['balanced_weak_pd']):.4f} | {float(primary_hit['d5_weak_pd']):.4f} | {float(primary_hit['weak_pd_delta']):.4f} |
| mid hit count | {primary_hit['balanced_mid_hits']} | {primary_hit['d5_mid_hits']} | {primary_hit['mid_hit_delta']} |
| strong hit count | {primary_hit['balanced_strong_hits']} | {primary_hit['d5_strong_hits']} | {primary_hit['strong_hit_delta']} |

结论：这个 D5 原始提升只多 hit `{primary_hit['weak_hit_delta']}` 个 weak target，应视为统计上很弱的信号。

## 3. Mask / Scope / PFA Robustness

{md_table(key_mask_rows, ['mask_name', 'target_scope', 'target_pfa', 'balanced_weak_pd', 'd5_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'd5_beats_balanced', 'evidence_level'])}

## 4. 3 Seeds Mini-check

主口径 3 seeds 聚合：

{md_table(primary_seed_rows, ['method', 'n_seeds', 'weak_pd_mean', 'weak_pd_std', 'mid_pd_mean', 'mid_pd_std', 'strong_pd_mean', 'strong_pd_std', 'measured_pfa_mean', 'false_alarm_count_mean', 'model_clean_mse_db_to_clean_mean', 'target_peak_abs_bias_db_mean_mean'])}

3 seeds 平均 weak Pd gain = `{float(decision['seed_mean_weak_pd_gain']):.6f}`。  
balanced std = `{float(decision['balanced_std_weak_pd']):.6f}`，D5 std = `{float(decision['d5_std_weak_pd']):.6f}`。  
是否大于两者 std：`{decision['gain_greater_than_both_std']}`。

## 5. Split Robustness Mini-check

{md_table(split_rows, ['mask_name', 'target_scope', 'target_pfa', 'balanced_weak_pd', 'd5_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'd5_beats_balanced'])}

## 6. 决策

按照你给的进入 D6 条件，当前 **{'建议进入 D6' if decision['recommend_d6'] else '不建议进入 D6'}**。

核心原因：

- 原始 D5 主口径只多 hit `{primary_hit['weak_hit_delta']}` 个 weak target；
- 这是 statistically weak signal；
- mask / non-overlap / PFA=1e-3 只要有一个口径不支持，就不能把 D5 当成稳定有效信号；
- 下一步更应该先修 weak target 定义，或检查模型容量 / 升级 RD/RA 表示；也可以把当前 range-only weak weighting 记录为负结果。

## 7. 输出文件

结果目录：`G:\\mineru_output\\results\\d5_check_improvement_significance`  
图像目录：`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d5_check_figures`
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

    d5_fixed_rows = read_csv_rows(D5_DIR / "d5_fixed_pfa_metrics.csv")
    hit_rows = make_hit_count_comparison(d5_fixed_rows)
    mask_rows = make_mask_robustness(hit_rows)

    data = prepare_data("original")
    all_models: dict[str, Any] = {}
    all_training_rows: list[dict[str, Any]] = []
    all_training_metrics: list[dict[str, Any]] = []
    for seed in SEEDS:
        models, training_rows, training_metrics = train_pair_for_seed(data, seed, "original", device)
        all_models.update(models)
        all_training_rows.extend(training_rows)
        all_training_metrics.extend(training_metrics)
    metrics, _case_arrays = evaluate_models(data, all_models, device)
    seed_rows = extract_seed_rows(metrics["fixed"], metrics["recon"], list(all_models.keys()), "original")
    seed_agg_rows = aggregate_seed_rows(seed_rows)

    split_data = prepare_data("alternate")
    split_models, split_training_rows, split_training_metrics = train_pair_for_seed(split_data, 0, "alternate", device)
    split_metrics, _split_case_arrays = evaluate_models(split_data, split_models, device)
    split_seed_rows = extract_seed_rows(split_metrics["fixed"], split_metrics["recon"], list(split_models.keys()), "alternate")
    split_rows = make_split_robustness_rows(split_seed_rows)
    all_training_rows.extend(split_training_rows)
    all_training_metrics.extend(split_training_metrics)

    seed_summary_rows = seed_rows + seed_agg_rows
    seed_decision = compare_seed_aggregates(seed_summary_rows)
    decision = make_decision(hit_rows, mask_rows, seed_decision, seed_summary_rows, split_rows)

    plot_outputs(hit_rows, seed_rows, seed_agg_rows, mask_rows)

    write_csv(RESULT_DIR / "d5_check_hit_count_comparison.csv", hit_rows)
    write_csv(RESULT_DIR / "d5_check_seed_summary.csv", seed_summary_rows)
    write_csv(RESULT_DIR / "d5_check_split_robustness.csv", split_rows)
    write_csv(RESULT_DIR / "d5_check_mask_robustness.csv", mask_rows)
    write_csv(RESULT_DIR / "d5_check_decision_summary.csv", [decision])
    write_csv(RESULT_DIR / "d5_check_training_loss.csv", all_training_rows)
    write_csv(RESULT_DIR / "d5_check_training_summary.csv", all_training_metrics)
    write_json(
        RESULT_DIR / "d5_check_config.json",
        {
            "stage": "D5-check",
            "strict_limits": {
                "no_d6": True,
                "no_false_alarm_penalty": True,
                "no_clean_identity_full_method": True,
                "no_proposed_full_loss": True,
                "only_balanced_mild_and_weak_peak_w2p0": True,
                "no_large_model": True,
                "no_rdlr_diffirm_rimformer": True,
            },
            "model": "SimpleRangeFCN",
            "seeds": SEEDS,
            "primary_protocol": {
                "sir": PRIMARY_SIR,
                "mask": PRIMARY_MASK,
                "scope": PRIMARY_SCOPE,
                "pfa": PRIMARY_PFA,
                "split_definition": PRIMARY_SPLIT_DEFINITION,
            },
            "train_frames": int(data["train_frames"].size),
            "val_frames": int(data["val_frames"].size),
            "test_frames": int(data["test_frames"].size),
            "batch_size": BATCH_SIZE,
            "tiny_steps": TINY_STEPS,
            "small_epochs": SMALL_EPOCHS,
            "bce_lr": BCE_LR,
            "bce_temperature": BCE_TEMPERATURE,
            "lambda_rec": LAMBDA_REC,
            "device": str(device),
        },
    )
    for label, model in {**all_models, **split_models}.items():
        write_model_summary(RESULT_DIR / f"d5_check_model_summary_{label}.txt", model, EXPECTED_ADC_SHAPE[0], device, data["norm_mean"], data["norm_std"])

    report_ts = write_report(hit_rows, mask_rows, seed_summary_rows, split_rows, decision)
    print(
        json.dumps(
            {
                "recommend_d6": decision["recommend_d6"],
                "primary_weak_hit_delta": decision["primary_weak_hit_delta"],
                "seed_mean_weak_pd_gain": decision["seed_mean_weak_pd_gain"],
                "gain_greater_than_both_std": decision["gain_greater_than_both_std"],
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
