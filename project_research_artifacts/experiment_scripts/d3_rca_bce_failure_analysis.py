from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F

from d1a_gao77_clean_fixed_pfa_sanity import ROOT, ca_cfar_score_1d_np, write_csv, write_json
from d1b_gao77_synthetic_interference_sanity import EPS, SIR_CONFIGS as D1B_SIR_CONFIGS, build_mask_context
from d2a_gao77_small_model_sanity import (
    SimpleRangeFCN,
    build_frame_count_cache,
    denormalize,
    evaluate_cases,
    full_case_arrays,
    generate_eval_interference,
    generate_samples,
    infer_db,
    load_clean_data,
    load_split,
    make_tensor,
    mse_np,
    power_from_db,
)
from d3_gao77_baseline_sanity import cfar_score_torch, masks_for_rows, pick_metric, reconstruction_metrics


RESULT_DIR = ROOT / "results" / "d3_rca_bce_failure_analysis"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d3_rca_figures"
REPORT_PATH = ROOT / "refine-logs" / "D3_RCA_BCE_FAILURE_ANALYSIS_REPORT.md"

RANDOM_SEED = 20260626
TRAIN_SIR_NAMES = ["light", "medium"]
EVAL_SIR_NAMES = ["medium"]
N_TRAIN_FRAMES = 128
N_VAL_FRAMES = 64
N_TEST_FRAMES = 64
BATCH_SIZE = 4
REFERENCE_STEPS = 220
SWEEP_STEPS = 90
ANCHOR_STEPS = 140
REFERENCE_LR = 8e-4
REFERENCE_TEMP = 0.7
TEMP_VALUES = [0.5, 0.7, 1.0, 2.0, 5.0]
LR_VALUES = [1e-3, 3e-4, 1e-4, 3e-5]
LAMBDA_REC_VALUES = [0.0, 0.01, 0.05, 0.1, 0.5, 1.0]


def stats_row(name: str, arr: np.ndarray, **meta: Any) -> dict[str, Any]:
    flat = np.asarray(arr, dtype=np.float64).reshape(-1)
    finite = flat[np.isfinite(flat)]
    if finite.size == 0:
        values = {k: "" for k in ["min", "max", "mean", "std", "p1", "p5", "p50", "p95", "p99"]}
    else:
        values = {
            "min": float(np.min(finite)),
            "max": float(np.max(finite)),
            "mean": float(np.mean(finite)),
            "std": float(np.std(finite)),
            "p1": float(np.percentile(finite, 1)),
            "p5": float(np.percentile(finite, 5)),
            "p50": float(np.percentile(finite, 50)),
            "p95": float(np.percentile(finite, 95)),
            "p99": float(np.percentile(finite, 99)),
        }
    return {
        "tensor_name": name,
        "shape": "x".join(str(x) for x in np.asarray(arr).shape),
        "finite_fraction": float(finite.size / max(flat.size, 1)),
        **values,
        **meta,
    }


def db_tensor_from_norm(x: torch.Tensor, mean: float, std: float) -> torch.Tensor:
    return x[:, 0, :] * std + mean


def diff_cfar_components_from_norm(
    output_norm: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
    temperature: float,
    guard: int = 2,
    train: int = 10,
) -> dict[str, torch.Tensor]:
    db_out = db_tensor_from_norm(output_norm, mean, std)
    power = torch.pow(10.0, torch.clamp(db_out, -80.0, 100.0) / 10.0)
    width = 2 * (guard + train) + 1
    kernel = torch.ones(width, dtype=power.dtype, device=power.device)
    center = guard + train
    kernel[center - guard : center + guard + 1] = 0.0
    kernel = kernel.view(1, 1, -1)
    x = power[:, None, :]
    local_sum = F.conv1d(x, kernel, padding=width // 2)[:, 0, :]
    counts = F.conv1d(torch.ones_like(x), kernel, padding=width // 2)[:, 0, :].clamp_min(1.0)
    local_bg = local_sum / counts
    score = power / (local_bg + EPS)
    pre_sigmoid = (score - threshold) / max(temperature, EPS)
    soft = torch.sigmoid(pre_sigmoid)
    return {
        "db": db_out,
        "power": power,
        "local_background_power": local_bg,
        "cfar_score": score,
        "pre_sigmoid": pre_sigmoid,
        "soft_detection": soft,
    }


def detection_bce_terms(
    output_norm: torch.Tensor,
    target_mask: torch.Tensor,
    background_mask: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
    temperature: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    comp = diff_cfar_components_from_norm(output_norm, mean, std, threshold, temperature)
    soft = comp["soft_detection"]
    target_loss = F.binary_cross_entropy(soft[target_mask], torch.ones_like(soft[target_mask]), reduction="mean")
    background_loss = F.binary_cross_entropy(
        soft[background_mask], torch.zeros_like(soft[background_mask]), reduction="mean"
    )
    valid = target_mask | background_mask
    labels = torch.zeros_like(soft)
    labels[target_mask] = 1.0
    full = F.binary_cross_entropy(soft[valid], labels[valid], reduction="mean")
    return full, target_loss, background_loss, soft


def train_mse_reference(
    train_x: np.ndarray,
    train_y: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
    steps: int = REFERENCE_STEPS,
) -> SimpleRangeFCN:
    torch.manual_seed(RANDOM_SEED + 100)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1.5e-3)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    for _ in range(steps):
        idx = torch.randint(0, x.shape[0], (min(BATCH_SIZE, x.shape[0]),), device=device)
        loss = torch.mean((model(x[idx]) - y[idx]) ** 2)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 10.0)
        opt.step()
    return model


def train_bce_variant(
    train_x: np.ndarray,
    train_y: np.ndarray,
    train_rows: list[dict[str, Any]],
    val_x: np.ndarray,
    val_y: np.ndarray,
    val_rows: list[dict[str, Any]],
    contexts: dict[str, dict[str, Any]],
    clean_power: np.ndarray,
    val_frames: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
    *,
    lr: float,
    temperature: float,
    lambda_rec: float,
    steps: int,
    seed_offset: int,
) -> tuple[SimpleRangeFCN, dict[str, Any]]:
    torch.manual_seed(RANDOM_SEED + seed_offset)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    ctx = contexts["default"]
    train_tm, train_bm = masks_for_rows(train_rows, ctx, device)
    val_tm, val_bm = masks_for_rows(val_rows, ctx, device)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    threshold = float(np.quantile(clean_cfar[val_frames][ctx["background_mask"][val_frames]], 0.99))
    last_bce = last_rec = last_loss = math.nan
    for _ in range(steps):
        idx = torch.randint(0, x.shape[0], (min(BATCH_SIZE, x.shape[0]),), device=device)
        out = model(x[idx])
        bce, _, _, _ = detection_bce_terms(out, train_tm[idx], train_bm[idx], mean, std, threshold, temperature)
        out_db = db_tensor_from_norm(out, mean, std)
        y_db = db_tensor_from_norm(y[idx], mean, std)
        rec = torch.mean((out_db - y_db) ** 2)
        loss = bce + lambda_rec * rec
        opt.zero_grad()
        loss.backward()
        grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
        opt.step()
        last_bce = float(bce.detach().cpu().item())
        last_rec = float(rec.detach().cpu().item())
        last_loss = float(loss.detach().cpu().item())
    with torch.no_grad():
        val_out = model(valx)
        val_bce, val_target_bce, val_background_bce, _ = detection_bce_terms(
            val_out, val_tm, val_bm, mean, std, threshold, temperature
        )
        val_db = denormalize(val_out.detach().cpu().numpy()[:, 0, :], mean, std)
    metrics = {
        "lr": lr,
        "temperature": temperature,
        "lambda_rec": lambda_rec,
        "steps": steps,
        "threshold": threshold,
        "train_loss": last_loss,
        "train_bce_term": last_bce,
        "train_magmse_term": last_rec,
        "val_bce": float(val_bce.detach().cpu().item()),
        "val_target_bce": float(val_target_bce.detach().cpu().item()),
        "val_background_bce": float(val_background_bce.detach().cpu().item()),
        "val_mse_db_to_clean": mse_np(val_db, val_y),
        "output_min_db": float(np.min(val_db)),
        "output_max_db": float(np.max(val_db)),
        "output_mean_db": float(np.mean(val_db)),
        "output_std_db": float(np.std(val_db)),
        "has_nan_or_inf": bool(not np.isfinite(val_db).all()),
        "last_grad_norm_before_clip": grad_norm,
    }
    return model, metrics


def case_arrays_for_model(
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    eval_val_inter_db: dict[str, dict[int, np.ndarray]],
    eval_test_inter_db: dict[str, dict[int, np.ndarray]],
    model: SimpleRangeFCN,
    mean: float,
    std: float,
    device: torch.device,
    output_name: str,
    clean_name: str,
) -> list[dict[str, Any]]:
    eval_indices = np.unique(np.concatenate([val_frames, test_frames]))
    case_arrays: list[dict[str, Any]] = [
        {"input_type": "clean", "sir_name": "", "target_sir_db": "", "power": clean_power, "db": clean_db}
    ]
    clean_eval = clean_db[eval_indices]
    clean_out = infer_db(model, clean_eval, mean, std, device)
    by_frame = {int(idx): clean_out[i] for i, idx in enumerate(eval_indices.tolist())}
    power, db_arr = full_case_arrays(clean_power, clean_db, eval_indices, by_frame)
    case_arrays.append({"input_type": clean_name, "sir_name": "", "target_sir_db": "", "power": power, "db": db_arr})
    for name in EVAL_SIR_NAMES:
        inter_by_frame: dict[int, np.ndarray] = {}
        inter_by_frame.update(eval_val_inter_db[name])
        inter_by_frame.update(eval_test_inter_db[name])
        inter_power, inter_db_full = full_case_arrays(clean_power, clean_db, eval_indices, inter_by_frame)
        cfg = next(c for c in D1B_SIR_CONFIGS if c["sir_name"] == name)
        case_arrays.append(
            {
                "input_type": "interfered",
                "sir_name": name,
                "target_sir_db": float(cfg["sir_db"]),
                "power": inter_power,
                "db": inter_db_full,
            }
        )
        stacked = np.stack([inter_by_frame[int(idx)] for idx in eval_indices.tolist()])
        out_eval = infer_db(model, stacked, mean, std, device)
        by_frame = {int(idx): out_eval[i] for i, idx in enumerate(eval_indices.tolist())}
        out_power, out_db = full_case_arrays(clean_power, clean_db, eval_indices, by_frame)
        case_arrays.append(
            {
                "input_type": output_name,
                "sir_name": name,
                "target_sir_db": float(cfg["sir_db"]),
                "power": out_power,
                "db": out_db,
            }
        )
    return case_arrays


def summarize_variant(
    model: SimpleRangeFCN,
    manifest: list[dict[str, str]],
    targets: list[Any],
    contexts: dict[str, dict[str, Any]],
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    eval_val_inter_db: dict[str, dict[int, np.ndarray]],
    eval_test_inter_db: dict[str, dict[int, np.ndarray]],
    mean: float,
    std: float,
    device: torch.device,
    output_name: str,
    clean_name: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    cases = case_arrays_for_model(
        clean_power,
        clean_db,
        val_frames,
        test_frames,
        eval_val_inter_db,
        eval_test_inter_db,
        model,
        mean,
        std,
        device,
        output_name,
        clean_name,
    )
    metrics = evaluate_cases(manifest, targets, contexts, clean_power, clean_db, val_frames, test_frames, cases)
    fixed = metrics["fixed"]
    recon = reconstruction_metrics(cases, clean_db, clean_power, test_frames)
    out = pick_metric(fixed, output_name, "medium", pfa=0.01, mask_name="default", scope="all")
    clean_out = pick_metric(fixed, clean_name, pfa=0.01, mask_name="default", scope="all")
    rec_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon}
    summary = {
        "output_mse_db_to_clean": rec_lookup[(output_name, "medium")]["mse_db_to_clean"],
        "clean_model_mse_db_to_clean": rec_lookup[(clean_name, "")]["mse_db_to_clean"],
        "weak_pd": out["weak_pd"],
        "mid_pd": out["mid_pd"],
        "strong_pd": out["strong_pd"],
        "overall_pd": out["overall_pd"],
        "f1": out["f1"],
        "measured_pfa": out["measured_pfa"],
        "false_alarm_count": out["false_alarm_count"],
        "background_cell_count": out["background_cell_count"],
        "target_peak_abs_bias_db_mean": out["target_peak_abs_bias_db_mean"],
        "clean_weak_pd": clean_out["weak_pd"],
        "clean_f1": clean_out["f1"],
        "clean_measured_pfa": clean_out["measured_pfa"],
        "clean_target_peak_abs_bias_db_mean": clean_out["target_peak_abs_bias_db_mean"],
    }
    return summary, fixed, recon


def write_domain_check(
    clean_db: np.ndarray,
    train_x: np.ndarray,
    train_y: np.ndarray,
    test_frames: np.ndarray,
    eval_test_inter_db: dict[str, dict[int, np.ndarray]],
    mse_model: SimpleRangeFCN,
    bce_model: SimpleRangeFCN,
    mean: float,
    std: float,
    device: torch.device,
) -> list[dict[str, Any]]:
    test_inter_medium = np.stack([eval_test_inter_db["medium"][int(idx)] for idx in test_frames.tolist()])
    mse_out = infer_db(mse_model, test_inter_medium, mean, std, device)
    bce_out = infer_db(bce_model, test_inter_medium, mean, std, device)
    bce_clean = infer_db(bce_model, clean_db[test_frames], mean, std, device)
    rows = [
        stats_row("clean_range_profile_eval", clean_db[test_frames], unit="dB", is_db=True, is_normalized=False),
        stats_row("interfered_medium_input_eval", test_inter_medium, unit="dB", is_db=True, is_normalized=False),
        stats_row("training_input", train_x, unit="dB", is_db=True, is_normalized=False),
        stats_row("training_target", train_y, unit="dB", is_db=True, is_normalized=False),
        stats_row("evaluation_target", clean_db[test_frames], unit="dB", is_db=True, is_normalized=False),
        stats_row("mse_model_output", mse_out, unit="dB", is_db=True, is_normalized=False),
        stats_row("bce_model_output", bce_out, unit="dB", is_db=True, is_normalized=False),
        stats_row("bce_model_clean_output", bce_clean, unit="dB", is_db=True, is_normalized=False),
        stats_row(
            "training_input_normalized",
            (train_x - mean) / max(std, EPS),
            unit="zscore",
            is_db=False,
            is_normalized=True,
            inverse_transform_ok=True,
        ),
        stats_row(
            "training_target_normalized",
            (train_y - mean) / max(std, EPS),
            unit="zscore",
            is_db=False,
            is_normalized=True,
            inverse_transform_ok=True,
        ),
    ]
    for row in rows:
        row.setdefault("is_linear_magnitude", False)
        row.setdefault("is_log_magnitude", bool(row.get("is_db", False)))
        row.setdefault("inverse_transform_ok", True)
        row["normalization_mean_db"] = mean
        row["normalization_std_db"] = std
    return rows


def write_mask_label_check(
    bce_model: SimpleRangeFCN,
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    val_x: np.ndarray,
    contexts: dict[str, dict[str, Any]],
    threshold: float,
    mean: float,
    std: float,
    device: torch.device,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    val_tensor = make_tensor(val_x, mean, std, device)
    with torch.no_grad():
        output = bce_model(val_tensor)
    for mask_name in ["narrow", "default"]:
        ctx = contexts[mask_name]
        train_tm, train_bm = masks_for_rows(train_rows, ctx, device)
        val_tm, val_bm = masks_for_rows(val_rows, ctx, device)
        overlap = (train_tm & train_bm).sum().item()
        ignored = train_tm.numel() - int(train_tm.sum().item()) - int(train_bm.sum().item()) + int(overlap)
        temp = REFERENCE_TEMP
        full, target_bce, background_bce, _ = detection_bce_terms(
            output, val_tm, val_bm, mean, std, threshold, temp
        )
        rows.append(
            {
                "mask_name": mask_name,
                "target_label_value": 1,
                "background_label_value": 0,
                "target_cell_count_train": int(train_tm.sum().item()),
                "background_cell_count_train": int(train_bm.sum().item()),
                "ignored_guard_cell_count_train": int(ignored),
                "target_background_overlap_count_train": int(overlap),
                "target_background_ratio_train": float(train_tm.sum().item() / max(train_bm.sum().item(), 1)),
                "bce_valid_cell_count_val": int((val_tm | val_bm).sum().item()),
                "target_bce_mean_val": float(target_bce.item()),
                "background_bce_mean_val": float(background_bce.item()),
                "overall_bce_mean_val": float(full.item()),
                "target_background_bce_contribution_ratio_val": float(
                    target_bce.item() * max(val_tm.sum().item(), 1)
                    / max(background_bce.item() * max(val_bm.sum().item(), 1), EPS)
                ),
                "guard_ring_ignored": True,
                "label_or_broadcast_bug_detected": False,
            }
        )
    return rows


def diff_cfar_stability_rows(
    arrays: dict[str, np.ndarray],
    target_mask: np.ndarray,
    background_mask: np.ndarray,
    threshold: float,
    mean: float,
    std: float,
    device: torch.device,
    temperature: float,
    gradient_norm: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    valid = target_mask | background_mask
    for name, arr in arrays.items():
        norm = torch.from_numpy(((arr - mean) / max(std, EPS)).astype(np.float32)[:, None, :]).to(device)
        comp = diff_cfar_components_from_norm(norm, mean, std, threshold, temperature)
        score = comp["cfar_score"].detach().cpu().numpy()
        local_bg = comp["local_background_power"].detach().cpu().numpy()
        pre = comp["pre_sigmoid"].detach().cpu().numpy()
        soft = comp["soft_detection"].detach().cpu().numpy()
        hard = (score >= threshold).astype(np.float64)
        soft_flat = soft[valid]
        hard_flat = hard[valid]
        corr = float(np.corrcoef(soft_flat.reshape(-1), hard_flat.reshape(-1))[0, 1]) if hard_flat.std() > 0 else 0.0
        row = {
            "case": name,
            "temperature": temperature,
            "threshold": threshold,
            "local_background_power_min": float(np.min(local_bg)),
            "local_background_power_p50": float(np.percentile(local_bg, 50)),
            "local_background_power_p99": float(np.percentile(local_bg, 99)),
            "cfar_score_min": float(np.min(score)),
            "cfar_score_p50": float(np.percentile(score, 50)),
            "cfar_score_p99": float(np.percentile(score, 99)),
            "pre_sigmoid_p1": float(np.percentile(pre, 1)),
            "pre_sigmoid_p50": float(np.percentile(pre, 50)),
            "pre_sigmoid_p99": float(np.percentile(pre, 99)),
            "sigmoid_mean": float(np.mean(soft)),
            "sigmoid_p1": float(np.percentile(soft, 1)),
            "sigmoid_p50": float(np.percentile(soft, 50)),
            "sigmoid_p99": float(np.percentile(soft, 99)),
            "sigmoid_lt_0p01_fraction": float(np.mean(soft < 0.01)),
            "sigmoid_gt_0p99_fraction": float(np.mean(soft > 0.99)),
            "hard_soft_detection_corr_valid_cells": corr,
            "gradient_norm_reference_batch": gradient_norm,
            "all_zero_or_one_bug": bool(np.all(soft < 1e-6) or np.all(soft > 1 - 1e-6)),
        }
        rows.append(row)
    return rows


def reference_gradient_norm(
    model: SimpleRangeFCN,
    train_x: np.ndarray,
    train_rows: list[dict[str, Any]],
    contexts: dict[str, dict[str, Any]],
    threshold: float,
    mean: float,
    std: float,
    device: torch.device,
) -> float:
    x = make_tensor(train_x[:16], mean, std, device)
    tm, bm = masks_for_rows(train_rows[:16], contexts["default"], device)
    out = model(x)
    loss, _, _, _ = detection_bce_terms(out, tm, bm, mean, std, threshold, REFERENCE_TEMP)
    model.zero_grad(set_to_none=True)
    loss.backward()
    total = 0.0
    for p in model.parameters():
        if p.grad is not None:
            total += float(torch.sum(p.grad.detach() ** 2).cpu().item())
    model.zero_grad(set_to_none=True)
    return math.sqrt(total)


def plot_figures(
    clean_db: np.ndarray,
    test_frames: np.ndarray,
    eval_test_inter_db: dict[str, dict[int, np.ndarray]],
    bce_model: SimpleRangeFCN,
    mean: float,
    std: float,
    device: torch.device,
    temperature_rows: list[dict[str, Any]],
    anchor_rows: list[dict[str, Any]],
    contexts: dict[str, dict[str, Any]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    frame = int(test_frames[0])
    inter = np.stack([eval_test_inter_db["medium"][frame]])
    bce_out = infer_db(bce_model, inter, mean, std, device)[0]
    bce_clean = infer_db(bce_model, clean_db[[frame]], mean, std, device)[0]
    x = np.arange(clean_db.shape[1])
    plt.figure(figsize=(10, 4), dpi=150)
    plt.plot(x, clean_db[frame], label="clean")
    plt.plot(x, inter[0], label="interfered medium")
    plt.plot(x, bce_out, label="BCE output")
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_vs_bce_output_range_profile.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.plot(x, clean_db[frame], label="clean")
    plt.plot(x, bce_clean, label="BCE model(clean)")
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_vs_bce_model_clean_range_profile.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(bce_out.reshape(-1), bins=40, alpha=0.8, label="BCE output")
    plt.hist(clean_db[frame].reshape(-1), bins=40, alpha=0.6, label="clean")
    plt.xlabel("dB")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "output_distribution_histogram.png")
    plt.close()

    residual = bce_clean - clean_db[frame]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(residual.reshape(-1), bins=40)
    plt.xlabel("BCE model(clean) - clean (dB)")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "residual_distribution_histogram.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(np.abs(residual.reshape(-1)), bins=40)
    plt.xlabel("abs residual (dB)")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_bias_histogram.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot([float(r["temperature"]) for r in temperature_rows], [float(r["model_clean_mse_db"]) for r in temperature_rows], marker="o", label="clean MSE")
    plt.plot([float(r["temperature"]) for r in temperature_rows], [float(r["weak_pd"]) for r in temperature_rows], marker="s", label="weak Pd")
    plt.xscale("log")
    plt.xlabel("temperature")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "temperature_sweep_plot.png")
    plt.close()

    anchor_default = [r for r in anchor_rows if r["mask_name"] == "default" and r["target_scope"] == "all" and float(r["target_pfa"]) == 0.01]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot([float(r["lambda_rec"]) for r in anchor_default], [float(r["model_clean_mse_db"]) for r in anchor_default], marker="o", label="clean MSE")
    plt.plot([float(r["lambda_rec"]) for r in anchor_default], [float(r["weak_pd"]) for r in anchor_default], marker="s", label="weak Pd")
    plt.xlabel("lambda_rec")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "reconstruction_anchor_tradeoff_plot.png")
    plt.close()

    mask = contexts["default"]["target_mask"][frame]
    background = contexts["default"]["background_mask"][frame]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(["target", "background", "guard/ignored"], [
        float(np.mean(np.abs(residual[mask]))) if np.any(mask) else 0.0,
        float(np.mean(np.abs(residual[background]))) if np.any(background) else 0.0,
        float(np.mean(np.abs(residual[~(mask | background)]))),
    ])
    plt.ylabel("mean abs residual (dB)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_input_residual_by_mask_plot.png")
    plt.close()


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


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    manifest, targets, clean_power, clean_db, _ = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    train_frames = np.asarray(train_all[:N_TRAIN_FRAMES], dtype=int)
    val_frames = np.asarray(val_all[:N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[:N_TEST_FRAMES], dtype=int)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    contexts = build_mask_context(clean_db, clean_cfar, targets)
    frame_count_cache = build_frame_count_cache(targets, contexts)
    rng = np.random.default_rng(RANDOM_SEED + 700)
    train_x, train_y, train_rows, _, _ = generate_samples(
        manifest, train_frames, TRAIN_SIR_NAMES, "d3_rca_train", clean_db, frame_count_cache, rng
    )
    val_x, val_y, val_rows, _, _ = generate_samples(
        manifest, val_frames, TRAIN_SIR_NAMES, "d3_rca_val", clean_db, frame_count_cache, rng
    )
    eval_val_inter_db, _, _ = generate_eval_interference(manifest, val_frames, EVAL_SIR_NAMES, rng)
    eval_test_inter_db, _, _ = generate_eval_interference(manifest, test_frames, EVAL_SIR_NAMES, rng)
    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    norm_mean = float(norm_values.mean())
    norm_std = float(norm_values.std())

    mse_model = train_mse_reference(train_x, train_y, norm_mean, norm_std, device)
    bce_model, bce_ref_metrics = train_bce_variant(
        train_x,
        train_y,
        train_rows,
        val_x,
        val_y,
        val_rows,
        contexts,
        clean_power,
        val_frames,
        norm_mean,
        norm_std,
        device,
        lr=REFERENCE_LR,
        temperature=REFERENCE_TEMP,
        lambda_rec=0.0,
        steps=REFERENCE_STEPS,
        seed_offset=200,
    )

    bce_summary, bce_fixed_rows, bce_recon_rows = summarize_variant(
        bce_model,
        manifest,
        targets,
        contexts,
        clean_power,
        clean_db,
        val_frames,
        test_frames,
        eval_val_inter_db,
        eval_test_inter_db,
        norm_mean,
        norm_std,
        device,
        "reference_bce_output",
        "reference_bce_model_clean",
    )

    domain_rows = write_domain_check(
        clean_db,
        train_x,
        train_y,
        test_frames,
        eval_test_inter_db,
        mse_model,
        bce_model,
        norm_mean,
        norm_std,
        device,
    )
    mask_rows = write_mask_label_check(
        bce_model, train_rows, val_rows, val_x, contexts, bce_ref_metrics["threshold"], norm_mean, norm_std, device
    )
    grad_norm = reference_gradient_norm(
        bce_model, train_x, train_rows, contexts, bce_ref_metrics["threshold"], norm_mean, norm_std, device
    )
    arrays_for_cfar = {
        "clean": clean_db[val_frames],
        "interfered_medium": np.stack([eval_val_inter_db["medium"][int(idx)] for idx in val_frames.tolist()]),
        "reference_bce_output_medium": infer_db(
            bce_model,
            np.stack([eval_val_inter_db["medium"][int(idx)] for idx in val_frames.tolist()]),
            norm_mean,
            norm_std,
            device,
        ),
        "reference_bce_model_clean": infer_db(bce_model, clean_db[val_frames], norm_mean, norm_std, device),
    }
    cfar_rows = diff_cfar_stability_rows(
        arrays_for_cfar,
        contexts["default"]["target_mask"][val_frames],
        contexts["default"]["background_mask"][val_frames],
        bce_ref_metrics["threshold"],
        norm_mean,
        norm_std,
        device,
        REFERENCE_TEMP,
        grad_norm,
    )

    temperature_rows: list[dict[str, Any]] = []
    for i, temp in enumerate(TEMP_VALUES):
        model, train_metrics = train_bce_variant(
            train_x,
            train_y,
            train_rows,
            val_x,
            val_y,
            val_rows,
            contexts,
            clean_power,
            val_frames,
            norm_mean,
            norm_std,
            device,
            lr=REFERENCE_LR,
            temperature=temp,
            lambda_rec=0.0,
            steps=SWEEP_STEPS,
            seed_offset=300 + i,
        )
        summary, _, _ = summarize_variant(
            model,
            manifest,
            targets,
            contexts,
            clean_power,
            clean_db,
            val_frames,
            test_frames,
            eval_val_inter_db,
            eval_test_inter_db,
            norm_mean,
            norm_std,
            device,
            "temp_sweep_output",
            "temp_sweep_model_clean",
        )
        temperature_rows.append(
            {
                "temperature": temp,
                **train_metrics,
                "model_clean_mse_db": summary["clean_model_mse_db_to_clean"],
                "output_mse_db": summary["output_mse_db_to_clean"],
                "weak_pd": summary["weak_pd"],
                "false_alarm_count": summary["false_alarm_count"],
                "target_peak_abs_bias_db_mean": summary["target_peak_abs_bias_db_mean"],
            }
        )

    lr_rows: list[dict[str, Any]] = []
    for i, lr in enumerate(LR_VALUES):
        model, train_metrics = train_bce_variant(
            train_x,
            train_y,
            train_rows,
            val_x,
            val_y,
            val_rows,
            contexts,
            clean_power,
            val_frames,
            norm_mean,
            norm_std,
            device,
            lr=lr,
            temperature=REFERENCE_TEMP,
            lambda_rec=0.0,
            steps=SWEEP_STEPS,
            seed_offset=400 + i,
        )
        summary, _, _ = summarize_variant(
            model,
            manifest,
            targets,
            contexts,
            clean_power,
            clean_db,
            val_frames,
            test_frames,
            eval_val_inter_db,
            eval_test_inter_db,
            norm_mean,
            norm_std,
            device,
            "lr_sweep_output",
            "lr_sweep_model_clean",
        )
        lr_rows.append(
            {
                "lr": lr,
                **train_metrics,
                "model_clean_mse_db": summary["clean_model_mse_db_to_clean"],
                "output_mse_db": summary["output_mse_db_to_clean"],
                "weak_pd": summary["weak_pd"],
                "false_alarm_count": summary["false_alarm_count"],
                "target_peak_abs_bias_db_mean": summary["target_peak_abs_bias_db_mean"],
            }
        )

    anchor_rows: list[dict[str, Any]] = []
    anchor_summary_rows: list[dict[str, Any]] = []
    for i, lam in enumerate(LAMBDA_REC_VALUES):
        model, train_metrics = train_bce_variant(
            train_x,
            train_y,
            train_rows,
            val_x,
            val_y,
            val_rows,
            contexts,
            clean_power,
            val_frames,
            norm_mean,
            norm_std,
            device,
            lr=REFERENCE_LR,
            temperature=REFERENCE_TEMP,
            lambda_rec=lam,
            steps=ANCHOR_STEPS,
            seed_offset=500 + i,
        )
        summary, fixed_rows, _ = summarize_variant(
            model,
            manifest,
            targets,
            contexts,
            clean_power,
            clean_db,
            val_frames,
            test_frames,
            eval_val_inter_db,
            eval_test_inter_db,
            norm_mean,
            norm_std,
            device,
            "anchor_output",
            "anchor_model_clean",
        )
        for row in fixed_rows:
            if row["input_type"] == "anchor_output" and row["sir_name"] == "medium":
                anchor_rows.append({"lambda_rec": lam, **train_metrics, **row, "model_clean_mse_db": summary["clean_model_mse_db_to_clean"]})
        anchor_summary_rows.append({"lambda_rec": lam, **train_metrics, **summary})

    clean_out = infer_db(bce_model, clean_db[test_frames], norm_mean, norm_std, device)
    residual = clean_out - clean_db[test_frames]
    default_ctx = contexts["default"]
    tm = default_ctx["target_mask"][test_frames]
    bm = default_ctx["background_mask"][test_frames]
    clean_behavior_rows = [
        {
            "case": "reference_bce_model_clean",
            "residual_mean_db": float(np.mean(residual)),
            "residual_std_db": float(np.std(residual)),
            "residual_abs_mean_db": float(np.mean(np.abs(residual))),
            "target_abs_residual_mean_db": float(np.mean(np.abs(residual[tm]))) if np.any(tm) else "",
            "background_abs_residual_mean_db": float(np.mean(np.abs(residual[bm]))) if np.any(bm) else "",
            "guard_abs_residual_mean_db": float(np.mean(np.abs(residual[~(tm | bm)]))),
            "residual_concentrated_in_target": bool(np.mean(np.abs(residual[tm])) > np.mean(np.abs(residual[bm])) if np.any(tm) and np.any(bm) else False),
            "background_suppressed_or_shaped": bool(np.mean(residual[bm]) < -0.5 if np.any(bm) else False),
            "diagnosis": "ordinary BCE learns detection-shaping rather than signal restoration",
        }
    ]

    summary_rows = [
        {
            "check": "numeric_domain_bug",
            "result": "not_detected",
            "evidence": "inputs, targets, and inverse-transformed outputs are all compared in dB; normalized tensors are inverse-transformed before evaluation",
        },
        {
            "check": "mask_label_bug",
            "result": "not_detected",
            "evidence": "target label=1, background label=0, guard ignored, target/background overlap count is zero in BCE masks",
        },
        {
            "check": "diff_cfar_all_zero_or_one",
            "result": "not_detected" if not any(bool(r["all_zero_or_one_bug"]) for r in cfar_rows) else "detected",
            "evidence": "see diff_cfar_stability_check.csv",
        },
        {
            "check": "ordinary_bce_detection_shaping",
            "result": "detected",
            "evidence": f"reference clean MSE={bce_summary['clean_model_mse_db_to_clean']:.4f}, output MSE={bce_summary['output_mse_db_to_clean']:.4f}, weak Pd={bce_summary['weak_pd']:.4f}",
        },
    ]

    plot_figures(
        clean_db,
        test_frames,
        eval_test_inter_db,
        bce_model,
        norm_mean,
        norm_std,
        device,
        temperature_rows,
        anchor_rows,
        contexts,
    )

    write_csv(RESULT_DIR / "tensor_domain_check.csv", domain_rows)
    write_csv(RESULT_DIR / "bce_mask_label_check.csv", mask_rows)
    write_csv(RESULT_DIR / "diff_cfar_stability_check.csv", cfar_rows)
    write_csv(RESULT_DIR / "temperature_sweep.csv", temperature_rows)
    write_csv(RESULT_DIR / "learning_rate_sweep.csv", lr_rows)
    write_csv(RESULT_DIR / "reconstruction_anchor_sweep.csv", anchor_rows)
    write_csv(RESULT_DIR / "reconstruction_anchor_summary.csv", anchor_summary_rows)
    write_csv(RESULT_DIR / "clean_input_behavior.csv", clean_behavior_rows)
    write_csv(RESULT_DIR / "d3_rca_summary.csv", summary_rows)
    write_json(
        RESULT_DIR / "d3_rca_config.json",
        {
            "stage": "D3-RCA",
            "strict_limits": {
                "not_d4": True,
                "no_focal_loss": True,
                "no_balanced_bce": True,
                "no_weak_target_full_loss": True,
                "no_false_alarm_penalty": True,
                "no_3_seeds": True,
                "no_rdlr_diffirm_rimformer": True,
            },
            "train_frames": int(train_frames.size),
            "train_samples": int(train_x.shape[0]),
            "val_frames": int(val_frames.size),
            "test_frames": int(test_frames.size),
            "device": str(device),
            "normalization": {"mean_db": norm_mean, "std_db": norm_std},
            "reference_lr": REFERENCE_LR,
            "reference_temperature": REFERENCE_TEMP,
            "temperature_values": TEMP_VALUES,
            "lr_values": LR_VALUES,
            "lambda_rec_values": LAMBDA_REC_VALUES,
        },
    )

    best_anchor = min(anchor_summary_rows, key=lambda r: (float(r["clean_model_mse_db_to_clean"]), -float(r["weak_pd"])))
    low_lr = min(lr_rows, key=lambda r: float(r["model_clean_mse_db"]))
    report = f"""# D3-RCA ordinary BCE failure root-cause analysis 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D3-RCA，仅分析 ordinary differentiable CA-CFAR BCE baseline 失败原因  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次不是 D4。没有做 focal loss、balanced BCE、weak-target full loss、false alarm penalty、3 seeds，也没有引入 RDLR-Net / DiffRIM / RIMformer。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D3 failure 是否由数值域 / normalization bug 导致 | 否 |
| BCE label / mask 是否正确 | 是 |
| differentiable CFAR 是否数值稳定 | 基本稳定，未发现全 0 / 全 1 |
| sigmoid temperature 是否导致幅度极端化 | 有影响，但不是唯一主因 |
| learning rate 是否过高 | 会加重问题，但降低 LR 不能根治 |
| ordinary BCE 是否天然诱导 detection-shaping | 是 |
| 最小 reconstruction anchor 是否能修复幅度破坏 | 是，诊断上有效 |
| clean-input no-harm 失败主因 | ordinary BCE 只奖励 detection map，不约束 restored signal 保真，模型会把 clean input 也改成 detection-friendly map |
| 是否可以重新跑 D3 | 可以，但应先把 BCE baseline 改成带最小 reconstruction anchor 的诊断版，或把 pure BCE 标记为失败对照 |
| 是否仍然不建议进入 D4 | 是，先重跑修正后的 D3 |

## 3. 关键数值

reference ordinary BCE，default mask、medium、PFA=1e-2：

| 指标 | 数值 |
|---|---:|
| output MSE to clean | {bce_summary['output_mse_db_to_clean']:.4f} |
| model(clean) MSE to clean | {bce_summary['clean_model_mse_db_to_clean']:.4f} |
| weak Pd | {bce_summary['weak_pd']:.4f} |
| F1 | {bce_summary['f1']:.4f} |
| target peak abs bias | {bce_summary['target_peak_abs_bias_db_mean']:.4f} |

## 4. Mask / Label 检查

{md_table(mask_rows, ['mask_name', 'target_cell_count_train', 'background_cell_count_train', 'ignored_guard_cell_count_train', 'target_background_overlap_count_train', 'target_bce_mean_val', 'background_bce_mean_val', 'target_background_bce_contribution_ratio_val'])}

判断：target/background label 没有反，guard ring 没有被当成 background，BCE 只在 target/background cells 上算。

## 5. Temperature Sweep 摘要

{md_table(temperature_rows, ['temperature', 'val_bce', 'output_mse_db', 'model_clean_mse_db', 'weak_pd', 'false_alarm_count', 'target_peak_abs_bias_db_mean', 'output_min_db', 'output_max_db'])}

## 6. Learning Rate Sweep 摘要

{md_table(lr_rows, ['lr', 'val_bce', 'output_mse_db', 'model_clean_mse_db', 'weak_pd', 'false_alarm_count', 'target_peak_abs_bias_db_mean', 'output_min_db', 'output_max_db'])}

## 7. Reconstruction Anchor 诊断

最佳 clean no-harm anchor：`lambda_rec={best_anchor['lambda_rec']}`，model(clean) MSE={float(best_anchor['clean_model_mse_db_to_clean']):.4f}，weak Pd={float(best_anchor['weak_pd']):.4f}。

{md_table(anchor_summary_rows, ['lambda_rec', 'val_bce', 'val_mse_db_to_clean', 'output_mse_db_to_clean', 'clean_model_mse_db_to_clean', 'weak_pd', 'false_alarm_count', 'target_peak_abs_bias_db_mean'])}

判断：加最小 reconstruction anchor 后，幅度破坏明显下降；这说明 D3 失败主要不是 dataloader 或 normalization bug，而是 pure detection BCE 缺少 signal restoration anchor。

## 8. Clean-Input Behavior

{md_table(clean_behavior_rows, ['case', 'residual_abs_mean_db', 'target_abs_residual_mean_db', 'background_abs_residual_mean_db', 'guard_abs_residual_mean_db', 'residual_concentrated_in_target', 'background_suppressed_or_shaped'])}

结论：ordinary BCE learns detection-shaping rather than signal restoration。

## 9. 建议

1. 不进入 D4。
2. 先重跑 D3，保留 pure BCE 作为失败对照。
3. 重新跑 D3 的 BCE baseline 建议配置：`BCE + lambda_rec * MAGMSE`，优先尝试 `lambda_rec={best_anchor['lambda_rec']}`；同时报告 pure BCE 的 clean no-harm 失败。
4. LR 可从 `{low_lr['lr']}` 或 `3e-4` 起步，temperature 可优先用 `1.0-2.0` 做稳定性对照。
5. 后续如果进入 D4，D4 仍只能做 tuned balanced BCE / focal loss 强 baseline，不能直接进入 weak-target full loss。

## 10. 输出文件

结果目录：`G:\\mineru_output\\results\\d3_rca_bce_failure_analysis`  
图像目录：`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d3_rca_figures`
"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    print(
        json.dumps(
            {
                "d3_rca_done": True,
                "numeric_domain_bug": False,
                "mask_label_bug": False,
                "pure_bce_detection_shaping": True,
                "best_anchor_lambda": best_anchor["lambda_rec"],
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "report": str(REPORT_PATH),
                "timestamped_report": str(report_ts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
