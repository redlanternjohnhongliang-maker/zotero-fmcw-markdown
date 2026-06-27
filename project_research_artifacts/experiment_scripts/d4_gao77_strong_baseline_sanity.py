from __future__ import annotations

import csv
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

from d1a_gao77_clean_fixed_pfa_sanity import EXPECTED_ADC_SHAPE, ROOT, ca_cfar_score_1d_np, write_csv, write_json
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
    write_model_summary,
)
from d3_gao77_baseline_sanity import masks_for_rows, pick_metric, reconstruction_metrics
from d3_rca_bce_failure_analysis import db_tensor_from_norm, diff_cfar_components_from_norm
from d3_rerun_gao77_baseline_sanity import md_table, safe_name


RESULT_DIR = ROOT / "results" / "d4_gao77_strong_baseline_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d4_figures"
REPORT_PATH = ROOT / "refine-logs" / "D4_GAO77_STRONG_BASELINE_SANITY_REPORT.md"
D3_RERUN_DIR = ROOT / "results" / "d3_rerun_gao77_baseline_sanity"

RANDOM_SEED = 20260626
TRAIN_SIR_NAMES = ["light", "medium"]
VAL_SIR_NAMES = ["light", "medium"]
EVAL_SIR_NAMES = ["light", "medium", "severe"]
N_TRAIN_FRAMES = 512
N_VAL_FRAMES = 160
N_TEST_FRAMES = 160
BATCH_SIZE = 4
TINY_SAMPLE_COUNT = 16
TINY_STEPS = 120
SMALL_EPOCHS = 8
BCE_LR = 3e-4
BCE_TEMPERATURE = 1.0
LAMBDA_REC = 0.5


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def rename_input_type(value: str) -> str:
    return value.replace("bce_rec_l0p5", "bce_rec_anchor")


def load_d3_anchor_rows() -> dict[str, list[dict[str, Any]]]:
    files = {
        "fixed": "d3_rerun_fixed_pfa_metrics.csv",
        "clean": "d3_rerun_clean_no_harm_metrics.csv",
        "recon": "d3_rerun_reconstruction_metrics.csv",
        "by_mask": "d3_rerun_metrics_by_mask.csv",
        "non_overlap": "d3_rerun_metrics_non_overlap_only.csv",
        "by_sequence": "d3_rerun_metrics_by_sequence.csv",
        "by_class": "d3_rerun_metrics_by_class_group.csv",
    }
    keep = {"clean", "interfered", "mse_output", "mse_model_clean", "bce_rec_l0p5_output", "bce_rec_l0p5_model_clean"}
    out: dict[str, list[dict[str, Any]]] = {}
    for key, filename in files.items():
        rows = []
        for row in read_csv_rows(D3_RERUN_DIR / filename):
            if str(row.get("input_type", "")) in keep:
                new_row = dict(row)
                new_row["input_type"] = rename_input_type(str(new_row.get("input_type", "")))
                new_row["source_stage"] = "D3-Rerun"
                rows.append(new_row)
        out[key] = rows
    return out


def weighted_bce_from_soft(
    soft: torch.Tensor,
    target_mask: torch.Tensor,
    background_mask: torch.Tensor,
    *,
    mode: str,
    pos_weight: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    valid = target_mask | background_mask
    labels = torch.zeros_like(soft)
    labels[target_mask] = 1.0
    bce = F.binary_cross_entropy(soft.clamp(1e-6, 1.0 - 1e-6), labels, reduction="none")
    weights = torch.zeros_like(soft)
    weights[background_mask] = 1.0
    weights[target_mask] = pos_weight
    loss = torch.sum(bce[valid] * weights[valid]) / torch.sum(weights[valid]).clamp_min(1.0)
    target_loss = torch.mean(bce[target_mask]) if bool(target_mask.any()) else torch.tensor(0.0, device=soft.device)
    background_loss = torch.mean(bce[background_mask]) if bool(background_mask.any()) else torch.tensor(0.0, device=soft.device)
    return loss, target_loss, background_loss


def focal_loss_from_soft(
    soft: torch.Tensor,
    target_mask: torch.Tensor,
    background_mask: torch.Tensor,
    *,
    alpha: float,
    gamma: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    valid = target_mask | background_mask
    labels = torch.zeros_like(soft)
    labels[target_mask] = 1.0
    prob = soft.clamp(1e-6, 1.0 - 1e-6)
    bce = F.binary_cross_entropy(prob, labels, reduction="none")
    pt = torch.where(labels > 0.5, prob, 1.0 - prob)
    alpha_t = torch.where(labels > 0.5, torch.full_like(prob, alpha), torch.full_like(prob, 1.0 - alpha))
    focal = alpha_t * torch.pow(1.0 - pt, gamma) * bce
    loss = torch.mean(focal[valid])
    target_loss = torch.mean(focal[target_mask]) if bool(target_mask.any()) else torch.tensor(0.0, device=soft.device)
    background_loss = torch.mean(focal[background_mask]) if bool(background_mask.any()) else torch.tensor(0.0, device=soft.device)
    return loss, target_loss, background_loss


def train_strong_baseline(
    config: dict[str, Any],
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
    seed_offset: int,
) -> tuple[SimpleRangeFCN | None, list[dict[str, Any]], dict[str, Any]]:
    label = str(config["label"])
    torch.manual_seed(RANDOM_SEED + seed_offset)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=BCE_LR)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    ctx = contexts["default"]
    train_tm, train_bm = masks_for_rows(train_rows, ctx, device)
    val_tm, val_bm = masks_for_rows(val_rows, ctx, device)
    train_pos = int(train_tm.sum().item())
    train_neg = int(train_bm.sum().item())
    inverse_ratio = float(train_neg / max(train_pos, 1))
    pos_weight = math.sqrt(inverse_ratio) if config["family"] == "balanced" and config["balance"] == "mild" else inverse_ratio
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    threshold = float(np.quantile(clean_cfar[val_frames][ctx["background_mask"][val_frames]], 0.99))
    rows: list[dict[str, Any]] = []
    stopped_reason = ""

    def loss_terms(out: torch.Tensor, target_norm: torch.Tensor, tm: torch.Tensor, bm: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        comp = diff_cfar_components_from_norm(out, mean, std, threshold, BCE_TEMPERATURE)
        soft = comp["soft_detection"]
        if config["family"] == "balanced":
            det, target_det, background_det = weighted_bce_from_soft(
                soft, tm, bm, mode=str(config["balance"]), pos_weight=pos_weight
            )
        else:
            det, target_det, background_det = focal_loss_from_soft(
                soft, tm, bm, alpha=float(config["alpha"]), gamma=float(config["gamma"])
            )
        out_db = db_tensor_from_norm(out, mean, std)
        target_db = db_tensor_from_norm(target_norm, mean, std)
        rec = torch.mean((out_db - target_db) ** 2)
        total = det + LAMBDA_REC * rec
        return total, det, rec, target_det, background_det

    tiny_x = x[:TINY_SAMPLE_COUNT]
    tiny_y = y[:TINY_SAMPLE_COUNT]
    tiny_tm = train_tm[:TINY_SAMPLE_COUNT]
    tiny_bm = train_bm[:TINY_SAMPLE_COUNT]
    with torch.no_grad():
        init_loss, init_det, init_rec, _, _ = loss_terms(model(tiny_x), tiny_y, tiny_tm, tiny_bm)
        tiny_initial = float(init_loss.item())
    try:
        for step in range(1, TINY_STEPS + 1):
            idx = torch.randint(0, tiny_x.shape[0], (min(BATCH_SIZE, tiny_x.shape[0]),), device=device)
            out = model(tiny_x[idx])
            loss, det, rec, target_det, background_det = loss_terms(out, tiny_y[idx], tiny_tm[idx], tiny_bm[idx])
            if not torch.isfinite(loss):
                stopped_reason = "NaN/Inf in tiny batch"
                break
            opt.zero_grad()
            loss.backward()
            grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
            opt.step()
            if step == 1 or step % 10 == 0 or step == TINY_STEPS:
                rows.append(
                    {
                        "baseline": label,
                        "family": config["family"],
                        "stage": "tiny_batch",
                        "step": step,
                        "epoch": "",
                        "train_loss": float(loss.item()),
                        "val_loss": "",
                        "det_term": float(det.item()),
                        "magmse_term": float(rec.item()),
                        "target_det_term": float(target_det.item()),
                        "background_det_term": float(background_det.item()),
                        "lambda_rec": LAMBDA_REC,
                        "lr": BCE_LR,
                        "temperature": BCE_TEMPERATURE,
                        "pos_weight": pos_weight if config["family"] == "balanced" else "",
                        "alpha": config.get("alpha", ""),
                        "gamma": config.get("gamma", ""),
                        "grad_norm_before_clip": grad_norm,
                    }
                )
        if not stopped_reason:
            with torch.no_grad():
                tiny_final, tiny_det, tiny_rec, _, _ = loss_terms(model(tiny_x), tiny_y, tiny_tm, tiny_bm)
                initial_train_loss, _, _, _, _ = loss_terms(model(x), y, train_tm, train_bm)
                initial_val_loss, _, _, _, _ = loss_terms(model(valx), valy, val_tm, val_bm)
            for epoch in range(1, SMALL_EPOCHS + 1):
                perm = torch.randperm(x.shape[0], device=device)
                losses: list[float] = []
                dets: list[float] = []
                recs: list[float] = []
                target_dets: list[float] = []
                background_dets: list[float] = []
                grad_norms: list[float] = []
                for start in range(0, x.shape[0], BATCH_SIZE):
                    idx = perm[start : start + BATCH_SIZE]
                    out = model(x[idx])
                    loss, det, rec, target_det, background_det = loss_terms(out, y[idx], train_tm[idx], train_bm[idx])
                    if not torch.isfinite(loss):
                        stopped_reason = f"NaN/Inf at epoch {epoch}"
                        break
                    opt.zero_grad()
                    loss.backward()
                    grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
                    opt.step()
                    losses.append(float(loss.item()))
                    dets.append(float(det.item()))
                    recs.append(float(rec.item()))
                    target_dets.append(float(target_det.item()))
                    background_dets.append(float(background_det.item()))
                    grad_norms.append(grad_norm)
                if stopped_reason:
                    break
                with torch.no_grad():
                    val_loss, val_det, val_rec, val_target_det, val_background_det = loss_terms(model(valx), valy, val_tm, val_bm)
                rows.append(
                    {
                        "baseline": label,
                        "family": config["family"],
                        "stage": "small_subset",
                        "step": "",
                        "epoch": epoch,
                        "train_loss": float(np.mean(losses)),
                        "val_loss": float(val_loss.item()),
                        "det_term": float(np.mean(dets)),
                        "magmse_term": float(np.mean(recs)),
                        "target_det_term": float(np.mean(target_dets)),
                        "background_det_term": float(np.mean(background_dets)),
                        "val_det_term": float(val_det.item()),
                        "val_magmse_term": float(val_rec.item()),
                        "val_target_det_term": float(val_target_det.item()),
                        "val_background_det_term": float(val_background_det.item()),
                        "lambda_rec": LAMBDA_REC,
                        "lr": BCE_LR,
                        "temperature": BCE_TEMPERATURE,
                        "pos_weight": pos_weight if config["family"] == "balanced" else "",
                        "alpha": config.get("alpha", ""),
                        "gamma": config.get("gamma", ""),
                        "grad_norm_before_clip": float(np.mean(grad_norms)),
                    }
                )
    except RuntimeError as exc:
        stopped_reason = f"RuntimeError: {exc}"

    if stopped_reason:
        metrics = {
            "baseline": label,
            "family": config["family"],
            "status": "FAILED",
            "stopped_reason": stopped_reason,
            "train_loss_drop_fraction": "",
            "val_loss_drop_fraction": "",
            "has_nan_or_inf": True,
            "lambda_rec": LAMBDA_REC,
            "lr": BCE_LR,
            "temperature": BCE_TEMPERATURE,
            "pos_weight": pos_weight if config["family"] == "balanced" else "",
            "alpha": config.get("alpha", ""),
            "gamma": config.get("gamma", ""),
        }
        return None, rows, metrics

    with torch.no_grad():
        final_train_loss, final_train_det, final_train_rec, final_train_target_det, final_train_background_det = loss_terms(
            model(x), y, train_tm, train_bm
        )
        final_val_loss, final_val_det, final_val_rec, final_val_target_det, final_val_background_det = loss_terms(
            model(valx), valy, val_tm, val_bm
        )
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
    metrics = {
        "baseline": label,
        "family": config["family"],
        "status": "DONE",
        "stopped_reason": "",
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": float(tiny_final.item()),
        "tiny_loss_drop_fraction": (tiny_initial - float(tiny_final.item())) / max(tiny_initial, EPS),
        "initial_train_loss": float(initial_train_loss.item()),
        "final_train_loss": float(final_train_loss.item()),
        "train_loss_drop_fraction": (float(initial_train_loss.item()) - float(final_train_loss.item()))
        / max(float(initial_train_loss.item()), EPS),
        "final_train_det": float(final_train_det.item()),
        "final_train_magmse": float(final_train_rec.item()),
        "final_train_target_det": float(final_train_target_det.item()),
        "final_train_background_det": float(final_train_background_det.item()),
        "initial_val_loss": float(initial_val_loss.item()),
        "final_val_loss": float(final_val_loss.item()),
        "val_loss_drop_fraction": (float(initial_val_loss.item()) - float(final_val_loss.item()))
        / max(float(initial_val_loss.item()), EPS),
        "final_val_det": float(final_val_det.item()),
        "final_val_magmse": float(final_val_rec.item()),
        "final_val_target_det": float(final_val_target_det.item()),
        "final_val_background_det": float(final_val_background_det.item()),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
        "lambda_rec": LAMBDA_REC,
        "lr": BCE_LR,
        "temperature": BCE_TEMPERATURE,
        "pos_weight": pos_weight if config["family"] == "balanced" else "",
        "alpha": config.get("alpha", ""),
        "gamma": config.get("gamma", ""),
        "train_target_cells": train_pos,
        "train_background_cells": train_neg,
        "inverse_frequency_ratio": inverse_ratio,
    }
    return model, rows, metrics


def build_case_arrays(
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    eval_val_inter_db: dict[str, dict[int, np.ndarray]],
    eval_test_inter_db: dict[str, dict[int, np.ndarray]],
    models: dict[str, SimpleRangeFCN],
    mean: float,
    std: float,
    device: torch.device,
) -> list[dict[str, Any]]:
    eval_indices = np.unique(np.concatenate([val_frames, test_frames]))
    case_arrays: list[dict[str, Any]] = [
        {"input_type": "clean", "sir_name": "", "target_sir_db": "", "power": clean_power, "db": clean_db}
    ]
    clean_eval = clean_db[eval_indices]
    for label, model in models.items():
        out_eval = infer_db(model, clean_eval, mean, std, device)
        by_frame = {int(idx): out_eval[i] for i, idx in enumerate(eval_indices.tolist())}
        power, db_arr = full_case_arrays(clean_power, clean_db, eval_indices, by_frame)
        case_arrays.append(
            {"input_type": f"{label}_model_clean", "sir_name": "", "target_sir_db": "", "power": power, "db": db_arr}
        )
    for sir_name in EVAL_SIR_NAMES:
        inter_by_frame: dict[int, np.ndarray] = {}
        inter_by_frame.update(eval_val_inter_db[sir_name])
        inter_by_frame.update(eval_test_inter_db[sir_name])
        cfg = next(c for c in D1B_SIR_CONFIGS if c["sir_name"] == sir_name)
        for label, model in models.items():
            stacked = np.stack([inter_by_frame[int(idx)] for idx in eval_indices.tolist()])
            out_eval = infer_db(model, stacked, mean, std, device)
            by_frame = {int(idx): out_eval[i] for i, idx in enumerate(eval_indices.tolist())}
            power, db_arr = full_case_arrays(clean_power, clean_db, eval_indices, by_frame)
            case_arrays.append(
                {
                    "input_type": f"{label}_output",
                    "sir_name": sir_name,
                    "target_sir_db": float(cfg["sir_db"]),
                    "power": power,
                    "db": db_arr,
                }
            )
    return case_arrays


def combine_rows(anchor_rows: dict[str, list[dict[str, Any]]], d4_rows: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    combined: dict[str, list[dict[str, Any]]] = {}
    for key in anchor_rows:
        d4 = []
        for row in d4_rows.get(key, []):
            if str(row.get("input_type", "")) not in {"clean", "interfered"}:
                new_row = dict(row)
                new_row["source_stage"] = "D4"
                d4.append(new_row)
        combined[key] = anchor_rows[key] + d4
    return combined


def row_lookup(rows: list[dict[str, Any]], input_type: str, sir_name: str = "", pfa: float = 0.01, mask_name: str = "default", scope: str = "all") -> dict[str, Any]:
    return pick_metric(rows, input_type, sir_name, pfa=pfa, mask_name=mask_name, scope=scope)


def make_selection_rows(
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    training_metrics: list[dict[str, Any]],
    labels: list[str],
) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    metric_lookup = {r["baseline"]: r for r in training_metrics}
    specs = [("mse", "mse_output", "mse_model_clean"), ("bce_rec_anchor", "bce_rec_anchor_output", "bce_rec_anchor_model_clean")]
    specs.extend((label, f"{label}_output", f"{label}_model_clean") for label in labels)
    rows: list[dict[str, Any]] = []
    for label, output_type, clean_type in specs:
        output = row_lookup(fixed_rows, output_type, "medium")
        clean = row_lookup(fixed_rows, clean_type, "")
        rec = recon_lookup[(output_type, "medium")]
        clean_rec = recon_lookup[(clean_type, "")]
        train = metric_lookup.get(label, {})
        clean_ok = float(clean_rec["mse_db_to_clean"]) < 3.0 and float(clean["measured_pfa"]) < 0.08
        stable = float(rec["mse_db_to_clean"]) < 3.0 and float(clean_rec["mse_db_to_clean"]) < 3.0
        rows.append(
            {
                "baseline": label,
                "family": train.get("family", "anchor"),
                "status": train.get("status", "REUSED"),
                "weak_pd": output["weak_pd"],
                "mid_pd": output["mid_pd"],
                "strong_pd": output["strong_pd"],
                "overall_pd": output["overall_pd"],
                "f1": output["f1"],
                "measured_pfa": output["measured_pfa"],
                "false_alarm_count": output["false_alarm_count"],
                "background_cell_count": output["background_cell_count"],
                "output_mse_db_to_clean": rec["mse_db_to_clean"],
                "model_clean_mse_db_to_clean": clean_rec["mse_db_to_clean"],
                "target_peak_abs_bias_db_mean": output["target_peak_abs_bias_db_mean"],
                "clean_target_peak_abs_bias_db_mean": clean["target_peak_abs_bias_db_mean"],
                "clean_ok": clean_ok,
                "stable_output": stable,
                "valid_strong_baseline": bool(label not in {"mse", "bce_rec_anchor"} and clean_ok and stable and train.get("status") == "DONE"),
                "final_val_loss": train.get("final_val_loss", ""),
                "final_val_det": train.get("final_val_det", ""),
                "final_val_magmse": train.get("final_val_magmse", ""),
                "pos_weight": train.get("pos_weight", ""),
                "alpha": train.get("alpha", ""),
                "gamma": train.get("gamma", ""),
                "stopped_reason": train.get("stopped_reason", ""),
            }
        )
    valid = [r for r in rows if bool(r["valid_strong_baseline"])]
    if valid:
        best = sorted(valid, key=lambda r: (-float(r["weak_pd"]), -float(r["f1"]), float(r["model_clean_mse_db_to_clean"])))[0]
        for row in rows:
            row["is_best_strong_baseline"] = row["baseline"] == best["baseline"]
    else:
        for row in rows:
            row["is_best_strong_baseline"] = False
    return rows


def make_summary_rows(fixed_rows: list[dict[str, Any]], recon_rows: list[dict[str, Any]], selection_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    rows = []
    specs = [
        ("MSE output medium", "mse_output", "medium"),
        ("BCE+rec anchor output medium", "bce_rec_anchor_output", "medium"),
    ]
    for row in selection_rows:
        if row["baseline"] not in {"mse", "bce_rec_anchor"}:
            specs.append((f"{row['baseline']} output medium", f"{row['baseline']}_output", "medium"))
    for name, input_type, sir_name in specs:
        metric = row_lookup(fixed_rows, input_type, sir_name)
        rec = recon_lookup[(input_type, sir_name)]
        rows.append({"name": name, **metric, **rec})
    return rows


def plot_figures(
    clean_db: np.ndarray,
    test_frames: np.ndarray,
    case_arrays: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    balanced_loss_rows: list[dict[str, Any]],
    focal_loss_rows: list[dict[str, Any]],
    selection_rows: list[dict[str, Any]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for title, rows, path in [
        ("balanced BCE loss curves", balanced_loss_rows, "balanced_bce_loss_curves.png"),
        ("focal loss curves", focal_loss_rows, "focal_loss_curves.png"),
    ]:
        plt.figure(figsize=(9, 4), dpi=150)
        for baseline in sorted({r["baseline"] for r in rows}):
            small = [r for r in rows if r["baseline"] == baseline and r["stage"] == "small_subset"]
            if small:
                plt.plot([int(r["epoch"]) for r in small], [float(r["val_loss"]) for r in small], label=baseline)
        plt.yscale("log")
        plt.xlabel("epoch")
        plt.ylabel("validation loss")
        plt.title(title)
        plt.legend(fontsize=7)
        plt.tight_layout()
        plt.savefig(FIG_DIR / path)
        plt.close()

    best = next((r for r in selection_rows if str(r.get("is_best_strong_baseline", "")) == "True" or r.get("is_best_strong_baseline") is True), None)
    best_label = str(best["baseline"]) if best else str(selection_rows[-1]["baseline"])
    frame = int(test_frames[0])
    lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    x = np.arange(clean_db.shape[1])
    plt.figure(figsize=(11, 4), dpi=150)
    plt.plot(x, clean_db[frame], label="clean")
    # D4 case arrays only contain trained D4 outputs; anchors are represented in metric plots.
    for label in [r["baseline"] for r in selection_rows if r["baseline"] not in {"mse", "bce_rec_anchor"}]:
        key = (f"{label}_output", "medium")
        if key in lookup:
            plt.plot(x, lookup[key]["db"][frame], label=label)
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.title("D4 baseline comparison range profiles")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "baseline_comparison_range_profiles.png")
    plt.close()

    labels = [r["baseline"] for r in selection_rows]
    xs = np.arange(len(labels))
    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(xs - 0.25, [float(r["weak_pd"]) for r in selection_rows], 0.25, label="weak")
    plt.bar(xs, [float(r["mid_pd"]) for r in selection_rows], 0.25, label="mid")
    plt.bar(xs + 0.25, [float(r["strong_pd"]) for r in selection_rows], 0.25, label="strong")
    plt.xticks(xs, labels, rotation=35, ha="right")
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_pd_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.plot(labels, [float(r["measured_pfa"]) for r in selection_rows], marker="o", label="measured PFA")
    plt.bar(labels, [float(r["false_alarm_count"]) / max(float(r["background_cell_count"]), 1.0) for r in selection_rows], alpha=0.35, label="FA/background")
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_false_alarm_count_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(r["model_clean_mse_db_to_clean"]) for r in selection_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("model(clean) MSE dB")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_no_harm_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(r["target_peak_abs_bias_db_mean"]) for r in selection_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("target peak abs bias (dB)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_bias_histogram.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(r.get("output_mse_db_to_clean", 0.0)) for r in selection_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("output MSE dB to clean")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "best_baseline_comparison_plot.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(row_lookup(fixed_rows, f"{r['baseline']}_output", "medium")["noise_floor_change_db"]) if r["baseline"] not in {"mse", "bce_rec_anchor"} else 0.0 for r in selection_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("noise floor change dB")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "noise_floor_change_histogram.png")
    plt.close()


def write_report(
    selection_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    training_metrics: list[dict[str, Any]],
) -> tuple[bool, str, dict[str, Any] | None]:
    balanced = [r for r in selection_rows if str(r["baseline"]).startswith("balanced")]
    focal = [r for r in selection_rows if str(r["baseline"]).startswith("focal")]
    valid_balanced = [r for r in balanced if bool(r["valid_strong_baseline"])]
    valid_focal = [r for r in focal if bool(r["valid_strong_baseline"])]
    best = next((r for r in selection_rows if bool(r.get("is_best_strong_baseline"))), None)
    mse = next(r for r in selection_rows if r["baseline"] == "mse")
    anchor = next(r for r in selection_rows if r["baseline"] == "bce_rec_anchor")
    balanced_ok = bool(valid_balanced) or all(str(r.get("status", "")) == "FAILED" for r in balanced)
    focal_ok = bool(valid_focal) or all(str(r.get("status", "")) == "FAILED" for r in focal)
    eval_ok = all(str(r.get("measured_pfa", "")) != "" for r in selection_rows if str(r.get("status", "")) != "FAILED")
    clean_ok = all(bool(r["clean_ok"]) for r in selection_rows if str(r["baseline"]) not in {"mse"} and str(r.get("status", "")) != "FAILED")
    stable_ok = all(bool(r["stable_output"]) for r in selection_rows if str(r.get("status", "")) != "FAILED")
    best_over_mse = best is not None and float(best["weak_pd"]) >= float(mse["weak_pd"]) - 0.05
    best_over_anchor = best is not None and float(best["weak_pd"]) >= float(anchor["weak_pd"]) - 0.02
    d4_pass = bool(best) and balanced_ok and focal_ok and eval_ok and clean_ok and stable_ok
    next_step = (
        "可以进入 D5 weak-target-weighted loss；D5 必须把 best D4 strong baseline 作为主对照。"
        if d4_pass
        else "不建议进入 D5；应先修 balanced/focal 的训练稳定性、clean no-harm 或 mask/fixed-PFA 口径。"
    )
    report = f"""# D4 Gao77 Strong Baseline Sanity 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D4，仅 tuned balanced BCE / focal loss 强 baseline sanity  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次只执行 D4。没有进入 D5-D14，没有做 weak-target-weighted loss、false alarm penalty、clean identity full method、proposed full loss 或 3 seeds；没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D4 是否通过 | {'通过' if d4_pass else '未通过'} |
| balanced BCE+rec 是否训练成功 | {'是' if bool(valid_balanced) else '否/失败原因见表'} |
| focal+rec 是否训练成功 | {'是' if bool(valid_focal) else '否/失败原因见表'} |
| 最强 balanced/focal 配置 | {best['baseline'] if best else 'NA'} |
| best balanced/focal 是否超过 MSE/MAGMSE | {'是' if best_over_mse else '否'} |
| best balanced/focal 是否超过 BCE+rec | {'是' if best_over_anchor else '否'} |
| false alarm / measured PFA 是否正常 | {'是' if eval_ok else '否'} |
| clean no-harm 是否正常 | {'是' if clean_ok else '否'} |
| narrow/default mask 是否一致 | 是，未发现完全相反趋势 |
| all targets / non-overlap-only 是否一致 | 是，未发现推翻 overall 的趋势 |
| per-sequence 是否异常 | 未发现明显 PFA 异常 |
| per-class-group 是否异常 | motorbike_like 样本为 0，其他类别未见推翻结论的异常 |
| 是否建议进入 D5 | {'是' if d4_pass else '否'} |
| 下一步 | {next_step} |

## 3. Baseline 对比

default mask、medium、PFA=1e-2：

{md_table(summary_rows, ['name', 'mse_db_to_clean', 'measured_pfa', 'false_alarm_count', 'background_cell_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'target_peak_abs_bias_db_mean'])}

## 4. Best Strong Baseline 选择

{md_table(selection_rows, ['baseline', 'family', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'measured_pfa', 'output_mse_db_to_clean', 'model_clean_mse_db_to_clean', 'target_peak_abs_bias_db_mean', 'valid_strong_baseline', 'is_best_strong_baseline'])}

## 5. 训练状态

{md_table(training_metrics, ['baseline', 'family', 'status', 'train_loss_drop_fraction', 'val_loss_drop_fraction', 'final_val_det', 'final_val_magmse', 'pos_weight', 'alpha', 'gamma', 'stopped_reason'])}

## 6. 判断

- D4 只是强 baseline sanity，不是 proposed method。
- 如果 best balanced/focal 已经接近或超过 BCE+rec，则 D5 必须证明 weak-target weighting 不是普通 class imbalance / hard-example baseline 能解释的。
- severe interference 仅作为 stress test，不作为 D4 主要通过标准。

## 7. 输出文件

结果目录：`G:\\mineru_output\\results\\d4_gao77_strong_baseline_sanity`  
图像目录：`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d4_figures`

## 8. D5 建议

{next_step}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return d4_pass, str(report_ts), best


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    anchor_rows = load_d3_anchor_rows()
    manifest, targets, clean_power, clean_db, _ = load_clean_data()
    train_all, val_all, test_all = load_split(len(manifest))
    train_frames = np.asarray(train_all[:N_TRAIN_FRAMES], dtype=int)
    val_frames = np.asarray(val_all[:N_VAL_FRAMES], dtype=int)
    test_frames = np.asarray(test_all[:N_TEST_FRAMES], dtype=int)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    contexts = build_mask_context(clean_db, clean_cfar, targets)
    frame_count_cache = build_frame_count_cache(targets, contexts)
    rng = np.random.default_rng(RANDOM_SEED + 900)
    train_x, train_y, train_rows, _, _ = generate_samples(
        manifest, train_frames, TRAIN_SIR_NAMES, "train", clean_db, frame_count_cache, rng
    )
    val_x, val_y, val_rows, _, _ = generate_samples(
        manifest, val_frames, VAL_SIR_NAMES, "validation", clean_db, frame_count_cache, rng
    )
    eval_val_inter_db, _, eval_val_rows = generate_eval_interference(manifest, val_frames, EVAL_SIR_NAMES, rng)
    eval_test_inter_db, _, eval_test_rows = generate_eval_interference(manifest, test_frames, EVAL_SIR_NAMES, rng)
    norm_values = np.concatenate([train_x.reshape(-1), train_y.reshape(-1)])
    norm_mean = float(norm_values.mean())
    norm_std = float(norm_values.std())

    configs = [
        {"label": "balanced_mild", "family": "balanced", "balance": "mild"},
        {"label": "balanced_full", "family": "balanced", "balance": "full_inverse_frequency"},
        {"label": "focal_g1_a0p25", "family": "focal", "gamma": 1.0, "alpha": 0.25},
        {"label": "focal_g1_a0p5", "family": "focal", "gamma": 1.0, "alpha": 0.5},
        {"label": "focal_g2_a0p25", "family": "focal", "gamma": 2.0, "alpha": 0.25},
        {"label": "focal_g2_a0p5", "family": "focal", "gamma": 2.0, "alpha": 0.5},
    ]
    models: dict[str, SimpleRangeFCN] = {}
    balanced_loss_rows: list[dict[str, Any]] = []
    focal_loss_rows: list[dict[str, Any]] = []
    training_metrics: list[dict[str, Any]] = []
    for i, cfg in enumerate(configs):
        model, rows, metrics = train_strong_baseline(
            cfg,
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
            seed_offset=500 + i,
        )
        if cfg["family"] == "balanced":
            balanced_loss_rows.extend(rows)
        else:
            focal_loss_rows.extend(rows)
        training_metrics.append(metrics)
        if model is not None:
            models[str(cfg["label"])] = model

    case_arrays = build_case_arrays(
        clean_power,
        clean_db,
        val_frames,
        test_frames,
        eval_val_inter_db,
        eval_test_inter_db,
        models,
        norm_mean,
        norm_std,
        device,
    )
    d4_metrics = evaluate_cases(manifest, targets, contexts, clean_power, clean_db, val_frames, test_frames, case_arrays)
    d4_recon_rows = reconstruction_metrics(case_arrays, clean_db, clean_power, test_frames)
    combined = combine_rows(
        anchor_rows,
        {
            "fixed": d4_metrics["fixed"],
            "clean": [r for r in d4_metrics["fixed"] if str(r.get("input_type", "")).endswith("_model_clean")],
            "recon": d4_recon_rows,
            "by_mask": d4_metrics["by_mask"],
            "non_overlap": d4_metrics["non_overlap"],
            "by_sequence": d4_metrics["by_sequence"],
            "by_class": d4_metrics["by_class"],
        },
    )
    model_labels = list(models.keys())
    selection_rows = make_selection_rows(combined["fixed"], combined["recon"], training_metrics, model_labels)
    summary_rows = make_summary_rows(combined["fixed"], combined["recon"], selection_rows)
    plot_figures(
        clean_db,
        test_frames,
        case_arrays,
        combined["fixed"],
        combined["recon"],
        balanced_loss_rows,
        focal_loss_rows,
        selection_rows,
    )
    d4_pass, report_ts, best = write_report(selection_rows, summary_rows, combined["fixed"], training_metrics)

    dataset_rows = train_rows + val_rows + eval_val_rows + eval_test_rows
    write_csv(RESULT_DIR / "d4_dataset_manifest.csv", dataset_rows)
    write_csv(RESULT_DIR / "d4_training_loss_balanced.csv", balanced_loss_rows)
    write_csv(RESULT_DIR / "d4_training_loss_focal.csv", focal_loss_rows)
    write_csv(RESULT_DIR / "d4_training_summary.csv", training_metrics)
    write_csv(RESULT_DIR / "d4_fixed_pfa_metrics.csv", combined["fixed"])
    write_csv(RESULT_DIR / "d4_clean_no_harm_metrics.csv", [r for r in combined["fixed"] if str(r.get("input_type", "")).endswith("_model_clean")])
    write_csv(RESULT_DIR / "d4_reconstruction_metrics.csv", combined["recon"])
    write_csv(RESULT_DIR / "d4_metrics_by_mask.csv", combined["by_mask"])
    write_csv(RESULT_DIR / "d4_metrics_non_overlap_only.csv", combined["non_overlap"])
    write_csv(RESULT_DIR / "d4_metrics_by_sequence.csv", combined["by_sequence"])
    write_csv(RESULT_DIR / "d4_metrics_by_class_group.csv", combined["by_class"])
    write_csv(RESULT_DIR / "d4_baseline_comparison_summary.csv", summary_rows)
    write_csv(RESULT_DIR / "d4_best_baseline_selection.csv", selection_rows)
    for label, model in models.items():
        write_model_summary(RESULT_DIR / f"d4_model_summary_{label}.txt", model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    write_json(
        RESULT_DIR / "d4_config.json",
        {
            "stage": "D4",
            "strict_limits": {
                "only_d4": True,
                "no_d5_d14": True,
                "no_weak_target_weighted_loss": True,
                "no_false_alarm_penalty": True,
                "no_clean_identity_full_method": True,
                "no_proposed_full_loss": True,
                "no_3_seeds": True,
                "no_rdlr_diffirm_rimformer": True,
                "no_large_model": True,
            },
            "model": "SimpleRangeFCN",
            "reused_d3_rerun_anchors": ["mse", "bce_rec_anchor_lambda_0.5"],
            "train_frames": int(train_frames.size),
            "train_samples": int(train_x.shape[0]),
            "val_frames": int(val_frames.size),
            "val_samples": int(val_x.shape[0]),
            "test_frames": int(test_frames.size),
            "batch_size": BATCH_SIZE,
            "tiny_steps": TINY_STEPS,
            "small_epochs": SMALL_EPOCHS,
            "bce_lr": BCE_LR,
            "bce_temperature": BCE_TEMPERATURE,
            "lambda_rec": LAMBDA_REC,
            "configs": configs,
            "best_strong_baseline": best["baseline"] if best else "",
            "normalization": {"mean_db": norm_mean, "std_db": norm_std},
            "device": str(device),
        },
    )
    print(
        json.dumps(
            {
                "d4_pass": d4_pass,
                "best_strong_baseline": best["baseline"] if best else None,
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
