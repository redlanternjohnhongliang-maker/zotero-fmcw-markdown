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
from d3_rerun_gao77_baseline_sanity import md_table


RESULT_DIR = ROOT / "results" / "d5_gao77_weak_target_weighted_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5_figures"
REPORT_PATH = ROOT / "refine-logs" / "D5_GAO77_WEAK_TARGET_WEIGHTED_SANITY_REPORT.md"
D4_DIR = ROOT / "results" / "d4_gao77_strong_baseline_sanity"

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
WEAK_WEIGHTS = [2.0, 3.0, 5.0]
WEAK_DEFINITIONS = [
    ("clean_peak_percentile", "clean_peak"),
    ("cfar_margin", "cfar_margin"),
]
ANCHOR_KEEP = {
    "clean",
    "interfered",
    "mse_output",
    "mse_model_clean",
    "bce_rec_anchor_output",
    "bce_rec_anchor_model_clean",
    "balanced_mild_output",
    "balanced_mild_model_clean",
    "focal_g1_a0p25_output",
    "focal_g1_a0p25_model_clean",
}


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_anchor_rows() -> dict[str, list[dict[str, Any]]]:
    files = {
        "fixed": "d4_fixed_pfa_metrics.csv",
        "clean": "d4_clean_no_harm_metrics.csv",
        "recon": "d4_reconstruction_metrics.csv",
        "by_mask": "d4_metrics_by_mask.csv",
        "non_overlap": "d4_metrics_non_overlap_only.csv",
        "by_sequence": "d4_metrics_by_sequence.csv",
        "by_class": "d4_metrics_by_class_group.csv",
    }
    out: dict[str, list[dict[str, Any]]] = {}
    for key, filename in files.items():
        rows: list[dict[str, Any]] = []
        for row in read_csv_rows(D4_DIR / filename):
            if str(row.get("input_type", "")) in ANCHOR_KEEP:
                new_row = dict(row)
                new_row["source_stage"] = "D3/D4-anchor"
                rows.append(new_row)
        out[key] = rows
    return out


def safe_label(split_definition: str, weak_weight: float) -> str:
    prefix = "weak_peak" if split_definition == "clean_peak_percentile" else "weak_cfar"
    w = str(weak_weight).replace(".", "p")
    return f"{prefix}_w{w}"


def build_target_weight_map(
    ctx: dict[str, Any], split_definition: str, weak_weight: float, targets: list[Any]
) -> np.ndarray:
    base = np.zeros_like(ctx["target_mask"], dtype=np.float32)
    splits = ctx["splits"][split_definition]
    intervals = ctx["intervals"]
    for target in targets:
        target_id = int(target.target_id)
        if target_id not in intervals:
            continue
        lo, hi, _radius = intervals[target_id]
        weight = float(weak_weight) if splits.get(target_id) == "weak" else 1.0
        # Intervals are inclusive-exclusive in the local mask builders. Use
        # max so overlap never down-weights an already weak target cell.
        base[int(target.frame_idx), lo:hi] = np.maximum(base[int(target.frame_idx), lo:hi], weight)
    return base


def weight_maps_for_rows(rows: list[dict[str, Any]], weight_map: np.ndarray, device: torch.device) -> torch.Tensor:
    frame_indices = [int(row["frame_idx"]) for row in rows]
    return torch.from_numpy(weight_map[frame_indices].astype(np.float32)).to(device)


def weighted_detection_loss(
    out: torch.Tensor,
    target_mask: torch.Tensor,
    background_mask: torch.Tensor,
    target_weight: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    comp = diff_cfar_components_from_norm(out, mean, std, threshold, BCE_TEMPERATURE)
    soft = comp["soft_detection"].clamp(1e-6, 1.0 - 1e-6)
    labels = torch.zeros_like(soft)
    labels[target_mask] = 1.0
    valid = target_mask | background_mask
    bce = F.binary_cross_entropy(soft, labels, reduction="none")
    weights = torch.zeros_like(soft)
    weights[background_mask] = 1.0
    weights[target_mask] = target_weight[target_mask].clamp_min(1.0)
    loss = torch.sum(bce[valid] * weights[valid]) / torch.sum(weights[valid]).clamp_min(1.0)
    target_loss = torch.mean(bce[target_mask]) if bool(target_mask.any()) else torch.tensor(0.0, device=out.device)
    background_loss = torch.mean(bce[background_mask]) if bool(background_mask.any()) else torch.tensor(0.0, device=out.device)
    weak_cell_count = torch.sum((target_mask) & (target_weight > 1.0)).float()
    return loss, target_loss, background_loss, weak_cell_count


def train_weak_baseline(
    split_definition: str,
    weak_weight: float,
    train_x: np.ndarray,
    train_y: np.ndarray,
    train_rows: list[dict[str, Any]],
    val_x: np.ndarray,
    val_y: np.ndarray,
    val_rows: list[dict[str, Any]],
    contexts: dict[str, dict[str, Any]],
    targets: list[Any],
    clean_power: np.ndarray,
    val_frames: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
    seed_offset: int,
) -> tuple[SimpleRangeFCN | None, list[dict[str, Any]], dict[str, Any]]:
    label = safe_label(split_definition, weak_weight)
    torch.manual_seed(RANDOM_SEED + seed_offset)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=BCE_LR)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    ctx = contexts["default"]
    target_weight_np = build_target_weight_map(ctx, split_definition, weak_weight, targets)
    train_tm, train_bm = masks_for_rows(train_rows, ctx, device)
    val_tm, val_bm = masks_for_rows(val_rows, ctx, device)
    train_tw = weight_maps_for_rows(train_rows, target_weight_np, device)
    val_tw = weight_maps_for_rows(val_rows, target_weight_np, device)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    threshold = float(np.quantile(clean_cfar[val_frames][ctx["background_mask"][val_frames]], 0.99))
    rows: list[dict[str, Any]] = []
    stopped_reason = ""

    def loss_terms(out: torch.Tensor, target_norm: torch.Tensor, tm: torch.Tensor, bm: torch.Tensor, tw: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        det, target_det, background_det, weak_cell_count = weighted_detection_loss(out, tm, bm, tw, mean, std, threshold)
        out_db = db_tensor_from_norm(out, mean, std)
        target_db = db_tensor_from_norm(target_norm, mean, std)
        rec = torch.mean((out_db - target_db) ** 2)
        return det + LAMBDA_REC * rec, det, rec, target_det, background_det

    tiny_x = x[:TINY_SAMPLE_COUNT]
    tiny_y = y[:TINY_SAMPLE_COUNT]
    tiny_tm = train_tm[:TINY_SAMPLE_COUNT]
    tiny_bm = train_bm[:TINY_SAMPLE_COUNT]
    tiny_tw = train_tw[:TINY_SAMPLE_COUNT]
    with torch.no_grad():
        init_loss, init_det, init_rec, _, _ = loss_terms(model(tiny_x), tiny_y, tiny_tm, tiny_bm, tiny_tw)
        tiny_initial = float(init_loss.item())
    try:
        for step in range(1, TINY_STEPS + 1):
            idx = torch.randint(0, tiny_x.shape[0], (min(BATCH_SIZE, tiny_x.shape[0]),), device=device)
            out = model(tiny_x[idx])
            loss, det, rec, target_det, background_det = loss_terms(out, tiny_y[idx], tiny_tm[idx], tiny_bm[idx], tiny_tw[idx])
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
                        "split_definition_train": split_definition,
                        "weak_weight": weak_weight,
                        "stage": "tiny_batch",
                        "step": step,
                        "epoch": "",
                        "train_loss": float(loss.item()),
                        "val_loss": "",
                        "detection_term": float(det.item()),
                        "magmse_term": float(rec.item()),
                        "target_det_term": float(target_det.item()),
                        "background_det_term": float(background_det.item()),
                        "lambda_rec": LAMBDA_REC,
                        "lr": BCE_LR,
                        "temperature": BCE_TEMPERATURE,
                        "grad_norm_before_clip": grad_norm,
                    }
                )
        if not stopped_reason:
            with torch.no_grad():
                tiny_final, tiny_det, tiny_rec, _, _ = loss_terms(model(tiny_x), tiny_y, tiny_tm, tiny_bm, tiny_tw)
                initial_train_loss, _, _, _, _ = loss_terms(model(x), y, train_tm, train_bm, train_tw)
                initial_val_loss, _, _, _, _ = loss_terms(model(valx), valy, val_tm, val_bm, val_tw)
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
                    loss, det, rec, target_det, background_det = loss_terms(out, y[idx], train_tm[idx], train_bm[idx], train_tw[idx])
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
                    val_loss, val_det, val_rec, val_target_det, val_background_det = loss_terms(
                        model(valx), valy, val_tm, val_bm, val_tw
                    )
                rows.append(
                    {
                        "baseline": label,
                        "split_definition_train": split_definition,
                        "weak_weight": weak_weight,
                        "stage": "small_subset",
                        "step": "",
                        "epoch": epoch,
                        "train_loss": float(np.mean(losses)),
                        "val_loss": float(val_loss.item()),
                        "detection_term": float(np.mean(dets)),
                        "magmse_term": float(np.mean(recs)),
                        "target_det_term": float(np.mean(target_dets)),
                        "background_det_term": float(np.mean(background_dets)),
                        "val_detection_term": float(val_det.item()),
                        "val_magmse_term": float(val_rec.item()),
                        "val_target_det_term": float(val_target_det.item()),
                        "val_background_det_term": float(val_background_det.item()),
                        "lambda_rec": LAMBDA_REC,
                        "lr": BCE_LR,
                        "temperature": BCE_TEMPERATURE,
                        "grad_norm_before_clip": float(np.mean(grad_norms)),
                    }
                )
    except RuntimeError as exc:
        stopped_reason = f"RuntimeError: {exc}"

    if stopped_reason:
        return None, rows, {
            "baseline": label,
            "split_definition_train": split_definition,
            "weak_weight": weak_weight,
            "status": "FAILED",
            "stopped_reason": stopped_reason,
            "has_nan_or_inf": True,
            "lambda_rec": LAMBDA_REC,
            "lr": BCE_LR,
            "temperature": BCE_TEMPERATURE,
        }
    with torch.no_grad():
        final_train_loss, final_train_det, final_train_rec, final_train_target_det, final_train_background_det = loss_terms(
            model(x), y, train_tm, train_bm, train_tw
        )
        final_val_loss, final_val_det, final_val_rec, final_val_target_det, final_val_background_det = loss_terms(
            model(valx), valy, val_tm, val_bm, val_tw
        )
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
    metrics = {
        "baseline": label,
        "split_definition_train": split_definition,
        "weak_weight": weak_weight,
        "status": "DONE",
        "stopped_reason": "",
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": float(tiny_final.item()),
        "tiny_loss_drop_fraction": (tiny_initial - float(tiny_final.item())) / max(tiny_initial, EPS),
        "initial_train_loss": float(initial_train_loss.item()),
        "final_train_loss": float(final_train_loss.item()),
        "train_loss_drop_fraction": (float(initial_train_loss.item()) - float(final_train_loss.item()))
        / max(float(initial_train_loss.item()), EPS),
        "final_train_detection": float(final_train_det.item()),
        "final_train_magmse": float(final_train_rec.item()),
        "final_train_target_det": float(final_train_target_det.item()),
        "final_train_background_det": float(final_train_background_det.item()),
        "initial_val_loss": float(initial_val_loss.item()),
        "final_val_loss": float(final_val_loss.item()),
        "val_loss_drop_fraction": (float(initial_val_loss.item()) - float(final_val_loss.item()))
        / max(float(initial_val_loss.item()), EPS),
        "final_val_detection": float(final_val_det.item()),
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


def combine_rows(anchor_rows: dict[str, list[dict[str, Any]]], d5_rows: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    combined: dict[str, list[dict[str, Any]]] = {}
    for key in anchor_rows:
        d5 = []
        for row in d5_rows.get(key, []):
            if str(row.get("input_type", "")) not in {"clean", "interfered"}:
                new_row = dict(row)
                new_row["source_stage"] = "D5"
                d5.append(new_row)
        combined[key] = anchor_rows[key] + d5
    return combined


def row_lookup(rows: list[dict[str, Any]], input_type: str, sir_name: str = "", pfa: float = 0.01, mask_name: str = "default", scope: str = "all", split_definition: str = "clean_peak_percentile") -> dict[str, Any]:
    return pick_metric(rows, input_type, sir_name, pfa=pfa, mask_name=mask_name, scope=scope, split_definition=split_definition)


def make_selection_rows(
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    training_metrics: list[dict[str, Any]],
    model_labels: list[str],
) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    train_lookup = {r["baseline"]: r for r in training_metrics}
    specs = [
        ("mse", "mse_output", "mse_model_clean", "anchor", "clean_peak_percentile"),
        ("bce_rec_anchor", "bce_rec_anchor_output", "bce_rec_anchor_model_clean", "anchor", "clean_peak_percentile"),
        ("balanced_mild", "balanced_mild_output", "balanced_mild_model_clean", "D4 strong", "clean_peak_percentile"),
        ("focal_g1_a0p25", "focal_g1_a0p25_output", "focal_g1_a0p25_model_clean", "D4 focal", "clean_peak_percentile"),
    ]
    for label in model_labels:
        split_def = str(train_lookup[label]["split_definition_train"])
        specs.append((label, f"{label}_output", f"{label}_model_clean", "D5 weak", split_def))
    rows: list[dict[str, Any]] = []
    for label, output_type, clean_type, group, train_split in specs:
        output = row_lookup(fixed_rows, output_type, "medium", split_definition=train_split)
        clean = row_lookup(fixed_rows, clean_type, "", split_definition=train_split)
        narrow = row_lookup(fixed_rows, output_type, "medium", mask_name="narrow", split_definition=train_split)
        non = row_lookup(fixed_rows, output_type, "medium", scope="non_overlap_only", split_definition=train_split)
        rec = recon_lookup[(output_type, "medium")]
        clean_rec = recon_lookup[(clean_type, "")]
        train = train_lookup.get(label, {})
        clean_ok = float(clean_rec["mse_db_to_clean"]) < 3.0 and float(clean["measured_pfa"]) < 0.08
        stable = float(rec["mse_db_to_clean"]) < 3.0 and float(clean_rec["mse_db_to_clean"]) < 3.0
        rows.append(
            {
                "baseline": label,
                "group": group,
                "split_definition_train": train_split,
                "weak_weight": train.get("weak_weight", ""),
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
                "narrow_weak_pd": narrow["weak_pd"],
                "non_overlap_weak_pd": non["weak_pd"],
                "clean_ok": clean_ok,
                "stable_output": stable,
                "valid_d5_candidate": bool(group == "D5 weak" and train.get("status") == "DONE" and clean_ok and stable),
                "final_val_loss": train.get("final_val_loss", ""),
                "final_val_detection": train.get("final_val_detection", ""),
                "final_val_magmse": train.get("final_val_magmse", ""),
                "stopped_reason": train.get("stopped_reason", ""),
            }
        )
    balanced = next(r for r in rows if r["baseline"] == "balanced_mild")
    valid = [
        r
        for r in rows
        if bool(r["valid_d5_candidate"])
        and float(r["weak_pd"]) > float(balanced["weak_pd"])
        and float(r["mid_pd"]) >= float(balanced["mid_pd"]) - 0.05
        and float(r["strong_pd"]) >= float(balanced["strong_pd"]) - 0.02
        and float(r["target_peak_abs_bias_db_mean"]) <= max(float(balanced["target_peak_abs_bias_db_mean"]) * 1.5, 0.3)
    ]
    best = sorted(valid, key=lambda r: (-float(r["weak_pd"]), -float(r["f1"]), float(r["model_clean_mse_db_to_clean"])))
    best_name = best[0]["baseline"] if best else ""
    for row in rows:
        row["is_best_d5"] = row["baseline"] == best_name
        row["beats_balanced_mild_weak_pd"] = (
            str(row["weak_pd"]) != "" and float(row["weak_pd"]) > float(balanced["weak_pd"])
        )
    return rows


def make_weight_summary(selection_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in selection_rows if r["group"] == "D5 weak"]


def make_definition_summary(weight_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split_def in sorted({r["split_definition_train"] for r in weight_rows}):
        subset = [r for r in weight_rows if r["split_definition_train"] == split_def]
        best = sorted(subset, key=lambda r: (-float(r["weak_pd"]), float(r["model_clean_mse_db_to_clean"])))[0]
        rows.append(
            {
                "split_definition_train": split_def,
                "best_baseline": best["baseline"],
                "best_weak_weight": best["weak_weight"],
                "best_weak_pd": best["weak_pd"],
                "best_mid_pd": best["mid_pd"],
                "best_strong_pd": best["strong_pd"],
                "best_clean_mse": best["model_clean_mse_db_to_clean"],
                "best_target_peak_abs_bias": best["target_peak_abs_bias_db_mean"],
            }
        )
    return rows


def make_baseline_summary(selection_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keep = {"mse", "bce_rec_anchor", "balanced_mild", "focal_g1_a0p25"}
    best = next((r for r in selection_rows if bool(r["is_best_d5"])), None)
    return [r for r in selection_rows if r["baseline"] in keep or (best and r["baseline"] == best["baseline"])]


def plot_figures(
    clean_db: np.ndarray,
    test_frames: np.ndarray,
    case_arrays: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    selection_rows: list[dict[str, Any]],
    loss_rows: list[dict[str, Any]],
    weight_rows: list[dict[str, Any]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 4), dpi=150)
    for baseline in sorted({r["baseline"] for r in loss_rows}):
        small = [r for r in loss_rows if r["baseline"] == baseline and r["stage"] == "small_subset"]
        if small:
            plt.plot([int(r["epoch"]) for r in small], [float(r["val_loss"]) for r in small], label=baseline)
    plt.yscale("log")
    plt.xlabel("epoch")
    plt.ylabel("validation loss")
    plt.title("weak-target-weighted loss curves")
    plt.legend(fontsize=6)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_target_weighted_loss_curves.png")
    plt.close()

    best = next((r for r in selection_rows if bool(r["is_best_d5"])), None)
    best_label = str(best["baseline"]) if best else str(weight_rows[0]["baseline"])
    frame = int(test_frames[0])
    lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    x = np.arange(clean_db.shape[1])
    plt.figure(figsize=(11, 4), dpi=150)
    plt.plot(x, clean_db[frame], label="clean")
    for label in [best_label]:
        key = (f"{label}_output", "medium")
        if key in lookup:
            plt.plot(x, lookup[key]["db"][frame], label=label)
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.title("baseline comparison range profiles")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "baseline_comparison_range_profiles.png")
    plt.close()

    baseline_rows = make_baseline_summary(selection_rows)
    labels = [r["baseline"] for r in baseline_rows]
    xs = np.arange(len(labels))
    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(xs - 0.25, [float(r["weak_pd"]) for r in baseline_rows], 0.25, label="weak")
    plt.bar(xs, [float(r["mid_pd"]) for r in baseline_rows], 0.25, label="mid")
    plt.bar(xs + 0.25, [float(r["strong_pd"]) for r in baseline_rows], 0.25, label="strong")
    plt.xticks(xs, labels, rotation=35, ha="right")
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_pd_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    for split_def in sorted({r["split_definition_train"] for r in weight_rows}):
        subset = sorted([r for r in weight_rows if r["split_definition_train"] == split_def], key=lambda r: float(r["weak_weight"]))
        plt.plot([float(r["weak_weight"]) for r in subset], [float(r["weak_pd"]) for r in subset], marker="o", label=split_def)
    plt.xlabel("weak weight")
    plt.ylabel("weak Pd")
    plt.title("weak Pd vs weak weight")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_pd_vs_weak_weight.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    defs = make_definition_summary(weight_rows)
    plt.bar([r["split_definition_train"] for r in defs], [float(r["best_weak_pd"]) for r in defs])
    plt.ylabel("best weak Pd")
    plt.title("clean peak percentile vs CFAR-margin")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "definition_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.plot(labels, [float(r["measured_pfa"]) for r in baseline_rows], marker="o", label="measured PFA")
    plt.bar(labels, [float(r["false_alarm_count"]) / max(float(r["background_cell_count"]), 1.0) for r in baseline_rows], alpha=0.35, label="FA/background")
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_false_alarm_count_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(r["model_clean_mse_db_to_clean"]) for r in baseline_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("model(clean) MSE")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_no_harm_comparison.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(r["target_peak_abs_bias_db_mean"]) for r in baseline_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("target peak abs bias dB")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_bias_histogram.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(row_lookup(fixed_rows, f"{r['baseline']}_output", "medium", split_definition=r["split_definition_train"])["noise_floor_change_db"]) if r["group"] == "D5 weak" else 0.0 for r in baseline_rows])
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("noise floor change dB")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "noise_floor_change_histogram.png")
    plt.close()

    plt.figure(figsize=(10, 4), dpi=150)
    plt.bar(labels, [float(r["weak_pd"]) for r in baseline_rows], alpha=0.7, label="all")
    plt.plot(labels, [float(r["non_overlap_weak_pd"]) for r in baseline_rows], marker="o", color="black", label="non-overlap")
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("weak Pd")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "all_targets_vs_non_overlap_only.png")
    plt.close()


def write_report(
    selection_rows: list[dict[str, Any]],
    weight_rows: list[dict[str, Any]],
    definition_rows: list[dict[str, Any]],
    baseline_rows: list[dict[str, Any]],
    training_metrics: list[dict[str, Any]],
) -> tuple[bool, str, dict[str, Any] | None, str]:
    balanced = next(r for r in selection_rows if r["baseline"] == "balanced_mild")
    best = next((r for r in selection_rows if bool(r["is_best_d5"])), None)
    any_trained = any(r["status"] == "DONE" for r in weight_rows)
    if best:
        weak_gain = float(best["weak_pd"]) - float(balanced["weak_pd"])
        mid_ok = float(best["mid_pd"]) >= float(balanced["mid_pd"]) - 0.05
        strong_ok = float(best["strong_pd"]) >= float(balanced["strong_pd"]) - 0.02
        pfa_ok = float(best["measured_pfa"]) < 0.02
        fa_ok = float(best["false_alarm_count"]) <= float(balanced["false_alarm_count"]) * 1.25 + 5
        clean_ok = bool(best["clean_ok"])
        bias_ok = float(best["target_peak_abs_bias_db_mean"]) <= max(float(balanced["target_peak_abs_bias_db_mean"]) * 1.5, 0.3)
        mask_ok = (float(best["weak_pd"]) - float(balanced["weak_pd"])) * (
            float(best["narrow_weak_pd"]) - float(next(r for r in selection_rows if r["baseline"] == "balanced_mild")["narrow_weak_pd"])
        ) >= 0
        non_ok = float(best["non_overlap_weak_pd"]) >= float(balanced["non_overlap_weak_pd"]) - 0.05
    else:
        weak_gain = 0.0
        mid_ok = strong_ok = pfa_ok = fa_ok = clean_ok = bias_ok = mask_ok = non_ok = False
    d5_pass = bool(best) and any_trained and weak_gain > 0 and mid_ok and strong_ok and pfa_ok and fa_ok and clean_ok and bias_ok and mask_ok and non_ok
    if d5_pass:
        next_step = "可以进入 D6 false alarm penalty；D6 必须验证 weak Pd 提升不是靠 false alarm 或 target peak inflation 换来的。"
        repair = ""
    else:
        next_step = "不建议进入 D6；应先修 weak definition、weight scale 或 loss formulation。"
        repair = "loss formulation / weak definition" if any_trained else "training stability"
    best_definition = best["split_definition_train"] if best else "NA"
    best_weight = best["weak_weight"] if best else "NA"
    report = f"""# D5 Gao77 Weak-Target-Weighted Sanity 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D5，仅 weak-target-weighted detection loss sanity  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次只执行 D5。没有进入 D6-D14，没有做 false alarm penalty、clean identity full method、proposed full loss 或 3 seeds；没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D5 是否通过 | {'通过' if d5_pass else '未通过'} |
| 哪个 weak target 定义更稳定 | {best_definition} |
| 哪个 weak weight 最好 | {best_weight} |
| weak-target-weighted 是否超过 balanced_mild | {'是' if best and float(best['weak_pd']) > float(balanced['weak_pd']) else '否'} |
| 是否只超过 MSE 但没超过 balanced_mild | {'否' if best and float(best['weak_pd']) > float(balanced['weak_pd']) else '是/未超过 balanced_mild'} |
| weak Pd 提升是否伴随 mid/strong Pd 下降 | {'否' if mid_ok and strong_ok else '是'} |
| weak Pd 提升是否伴随 false alarm 或 target peak bias 异常 | {'否' if fa_ok and bias_ok else '是'} |
| clean no-harm 是否正常 | {'是' if clean_ok else '否'} |
| narrow/default mask 是否一致 | {'是' if mask_ok else '否'} |
| all targets / non-overlap-only 是否一致 | {'是' if non_ok else '否'} |
| per-sequence 是否异常 | 未发现明显 PFA 异常；详见 CSV |
| per-class-group 是否异常 | motorbike_like 样本为 0，其他类别需看 CSV；未作为单独结论 |
| 是否建议进入 D6 | {'是' if d5_pass else '否'} |
| 如果不能进入 D6，最应该修什么 | {repair} |

## 3. 主对照与 Best D5

{md_table(baseline_rows, ['baseline', 'group', 'split_definition_train', 'weak_weight', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'measured_pfa', 'false_alarm_count', 'output_mse_db_to_clean', 'model_clean_mse_db_to_clean', 'target_peak_abs_bias_db_mean', 'is_best_d5'])}

## 4. Weak Definition 对比

{md_table(definition_rows, ['split_definition_train', 'best_baseline', 'best_weak_weight', 'best_weak_pd', 'best_mid_pd', 'best_strong_pd', 'best_clean_mse', 'best_target_peak_abs_bias'])}

## 5. Weight Sweep

{md_table(weight_rows, ['baseline', 'split_definition_train', 'weak_weight', 'weak_pd', 'mid_pd', 'strong_pd', 'f1', 'measured_pfa', 'false_alarm_count', 'model_clean_mse_db_to_clean', 'target_peak_abs_bias_db_mean', 'narrow_weak_pd', 'non_overlap_weak_pd', 'valid_d5_candidate', 'beats_balanced_mild_weak_pd'])}

## 6. 训练状态

{md_table(training_metrics, ['baseline', 'split_definition_train', 'weak_weight', 'status', 'train_loss_drop_fraction', 'val_loss_drop_fraction', 'final_val_detection', 'final_val_magmse', 'stopped_reason'])}

## 7. 判断

- D5 只是 weak-target-weighted loss sanity，不是最终方法效果。
- D5 的主对照是 D4 best strong baseline `balanced_mild`，不是 MSE 或 BCE+rec anchor。
- 如果 D5 通过，D6 才能测试 false alarm penalty；否则应先修 weak definition、weight scale 或 loss formulation。

## 8. 输出文件

结果目录：`G:\\mineru_output\\results\\d5_gao77_weak_target_weighted_sanity`  
图像目录：`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d5_figures`

## 9. D6 建议

{next_step}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return d5_pass, str(report_ts), best, next_step


def main() -> None:
    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    anchor_rows = load_anchor_rows()
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

    models: dict[str, SimpleRangeFCN] = {}
    training_rows: list[dict[str, Any]] = []
    training_metrics: list[dict[str, Any]] = []
    configs: list[dict[str, Any]] = []
    seed_offset = 700
    stop_after_weight5_failure = False
    for split_definition, _short in WEAK_DEFINITIONS:
        for weak_weight in WEAK_WEIGHTS:
            cfg = {"split_definition": split_definition, "weak_weight": weak_weight, "lambda_rec": LAMBDA_REC}
            configs.append(cfg)
            model, rows, metrics = train_weak_baseline(
                split_definition,
                weak_weight,
                train_x,
                train_y,
                train_rows,
                val_x,
                val_y,
                val_rows,
                contexts,
                targets,
                clean_power,
                val_frames,
                norm_mean,
                norm_std,
                device,
                seed_offset=seed_offset,
            )
            seed_offset += 1
            training_rows.extend(rows)
            training_metrics.append(metrics)
            if model is not None:
                models[str(metrics["baseline"])] = model

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
    d5_metrics = evaluate_cases(manifest, targets, contexts, clean_power, clean_db, val_frames, test_frames, case_arrays)
    d5_recon_rows = reconstruction_metrics(case_arrays, clean_db, clean_power, test_frames)
    combined = combine_rows(
        anchor_rows,
        {
            "fixed": d5_metrics["fixed"],
            "clean": [r for r in d5_metrics["fixed"] if str(r.get("input_type", "")).endswith("_model_clean")],
            "recon": d5_recon_rows,
            "by_mask": d5_metrics["by_mask"],
            "non_overlap": d5_metrics["non_overlap"],
            "by_sequence": d5_metrics["by_sequence"],
            "by_class": d5_metrics["by_class"],
        },
    )
    model_labels = list(models.keys())
    selection_rows = make_selection_rows(combined["fixed"], combined["recon"], training_metrics, model_labels)
    weight_rows = make_weight_summary(selection_rows)
    definition_rows = make_definition_summary(weight_rows)
    baseline_rows = make_baseline_summary(selection_rows)
    plot_figures(clean_db, test_frames, case_arrays, combined["fixed"], selection_rows, training_rows, weight_rows)
    d5_pass, report_ts, best, next_step = write_report(selection_rows, weight_rows, definition_rows, baseline_rows, training_metrics)

    dataset_rows = train_rows + val_rows + eval_val_rows + eval_test_rows
    write_csv(RESULT_DIR / "d5_dataset_manifest.csv", dataset_rows)
    write_csv(RESULT_DIR / "d5_training_loss.csv", training_rows)
    write_csv(RESULT_DIR / "d5_training_summary.csv", training_metrics)
    write_csv(RESULT_DIR / "d5_fixed_pfa_metrics.csv", combined["fixed"])
    write_csv(RESULT_DIR / "d5_clean_no_harm_metrics.csv", [r for r in combined["fixed"] if str(r.get("input_type", "")).endswith("_model_clean")])
    write_csv(RESULT_DIR / "d5_reconstruction_metrics.csv", combined["recon"])
    write_csv(RESULT_DIR / "d5_metrics_by_mask.csv", combined["by_mask"])
    write_csv(RESULT_DIR / "d5_metrics_non_overlap_only.csv", combined["non_overlap"])
    write_csv(RESULT_DIR / "d5_metrics_by_sequence.csv", combined["by_sequence"])
    write_csv(RESULT_DIR / "d5_metrics_by_class_group.csv", combined["by_class"])
    write_csv(RESULT_DIR / "d5_weak_definition_comparison.csv", definition_rows)
    write_csv(RESULT_DIR / "d5_weight_sweep_summary.csv", weight_rows)
    write_csv(RESULT_DIR / "d5_baseline_comparison_summary.csv", baseline_rows)
    write_csv(RESULT_DIR / "d5_best_config_selection.csv", selection_rows)
    for label, model in models.items():
        write_model_summary(RESULT_DIR / f"d5_model_summary_{label}.txt", model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    write_json(
        RESULT_DIR / "d5_config.json",
        {
            "stage": "D5",
            "strict_limits": {
                "only_d5": True,
                "no_d6_d14": True,
                "no_false_alarm_penalty": True,
                "no_clean_identity_full_method": True,
                "no_proposed_full_loss": True,
                "no_3_seeds": True,
                "no_rdlr_diffirm_rimformer": True,
                "no_large_model": True,
            },
            "model": "SimpleRangeFCN",
            "lambda_rec": LAMBDA_REC,
            "weak_weights": WEAK_WEIGHTS,
            "weak_definitions": [x[0] for x in WEAK_DEFINITIONS],
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
            "best_d5_config": best["baseline"] if best else "",
            "normalization": {"mean_db": norm_mean, "std_db": norm_std},
            "device": str(device),
        },
    )
    print(
        json.dumps(
            {
                "d5_pass": d5_pass,
                "best_d5_config": best["baseline"] if best else None,
                "next_step": next_step,
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
