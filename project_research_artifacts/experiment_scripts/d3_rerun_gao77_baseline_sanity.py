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
from d3_rca_bce_failure_analysis import db_tensor_from_norm, detection_bce_terms


RESULT_DIR = ROOT / "results" / "d3_rerun_gao77_baseline_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d3_rerun_figures"
REPORT_PATH = ROOT / "refine-logs" / "D3_RERUN_GAO77_BASELINE_SANITY_REPORT.md"

RANDOM_SEED = 20260626
VALID_PFA_TARGETS = [1e-2, 1e-3]
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
MSE_LR = 1.5e-3
BCE_LR = 3e-4
BCE_TEMPERATURE = 1.0
LAMBDA_REC_VALUES = [0.1, 0.5, 1.0]


def safe_name(value: float) -> str:
    return str(value).replace(".", "p").replace("-", "m")


def train_mse_baseline(
    train_x: np.ndarray,
    train_y: np.ndarray,
    val_x: np.ndarray,
    val_y: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
) -> tuple[SimpleRangeFCN, list[dict[str, Any]], dict[str, Any]]:
    torch.manual_seed(RANDOM_SEED + 100)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=MSE_LR)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    rows: list[dict[str, Any]] = []
    tiny_x = x[:TINY_SAMPLE_COUNT]
    tiny_y = y[:TINY_SAMPLE_COUNT]
    with torch.no_grad():
        tiny_initial = float(torch.mean((model(tiny_x) - tiny_y) ** 2).item())
    for step in range(1, TINY_STEPS + 1):
        idx = torch.randint(0, tiny_x.shape[0], (min(BATCH_SIZE, tiny_x.shape[0]),), device=device)
        loss = torch.mean((model(tiny_x[idx]) - tiny_y[idx]) ** 2)
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0)
        opt.step()
        if step == 1 or step % 10 == 0 or step == TINY_STEPS:
            rows.append(
                {
                    "baseline": "mse_magmse",
                    "stage": "tiny_batch",
                    "step": step,
                    "epoch": "",
                    "train_loss": float(loss.item()),
                    "val_loss": "",
                    "bce_term": "",
                    "magmse_term": "",
                    "lambda_rec": "",
                    "lr": MSE_LR,
                    "temperature": "",
                }
            )
    with torch.no_grad():
        tiny_final = float(torch.mean((model(tiny_x) - tiny_y) ** 2).item())
        initial_train = float(torch.mean((model(x) - y) ** 2).item())
        initial_val = float(torch.mean((model(valx) - valy) ** 2).item())
    for epoch in range(1, SMALL_EPOCHS + 1):
        perm = torch.randperm(x.shape[0], device=device)
        losses: list[float] = []
        for start in range(0, x.shape[0], BATCH_SIZE):
            idx = perm[start : start + BATCH_SIZE]
            loss = torch.mean((model(x[idx]) - y[idx]) ** 2)
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0)
            opt.step()
            losses.append(float(loss.item()))
        with torch.no_grad():
            val_loss = float(torch.mean((model(valx) - valy) ** 2).item())
        rows.append(
            {
                "baseline": "mse_magmse",
                "stage": "small_subset",
                "step": "",
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "val_loss": val_loss,
                "bce_term": "",
                "magmse_term": "",
                "lambda_rec": "",
                "lr": MSE_LR,
                "temperature": "",
            }
        )
    with torch.no_grad():
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
        final_train = float(torch.mean((model(x) - y) ** 2).item())
        final_val = float(torch.mean((model(valx) - valy) ** 2).item())
    metrics = {
        "baseline": "mse_magmse",
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": tiny_final,
        "tiny_loss_drop_fraction": (tiny_initial - tiny_final) / max(tiny_initial, EPS),
        "initial_train_loss": initial_train,
        "final_train_loss": final_train,
        "train_loss_drop_fraction": (initial_train - final_train) / max(initial_train, EPS),
        "initial_val_loss": initial_val,
        "final_val_loss": final_val,
        "val_loss_drop_fraction": (initial_val - final_val) / max(initial_val, EPS),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
        "lr": MSE_LR,
    }
    return model, rows, metrics


def train_detection_baseline(
    name: str,
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
    lambda_rec: float,
    seed_offset: int,
) -> tuple[SimpleRangeFCN, list[dict[str, Any]], dict[str, Any]]:
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
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    threshold = float(np.quantile(clean_cfar[val_frames][ctx["background_mask"][val_frames]], 0.99))
    rows: list[dict[str, Any]] = []
    tiny_x = x[:TINY_SAMPLE_COUNT]
    tiny_y = y[:TINY_SAMPLE_COUNT]
    tiny_tm = train_tm[:TINY_SAMPLE_COUNT]
    tiny_bm = train_bm[:TINY_SAMPLE_COUNT]

    def composite_loss(out: torch.Tensor, target_norm: torch.Tensor, tm: torch.Tensor, bm: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        bce, _, _, _ = detection_bce_terms(out, tm, bm, mean, std, threshold, BCE_TEMPERATURE)
        out_db = db_tensor_from_norm(out, mean, std)
        target_db = db_tensor_from_norm(target_norm, mean, std)
        magmse = torch.mean((out_db - target_db) ** 2)
        return bce + lambda_rec * magmse, bce, magmse

    with torch.no_grad():
        initial_loss, initial_bce, initial_rec = composite_loss(model(tiny_x), tiny_y, tiny_tm, tiny_bm)
        tiny_initial = float(initial_loss.item())
    for step in range(1, TINY_STEPS + 1):
        idx = torch.randint(0, tiny_x.shape[0], (min(BATCH_SIZE, tiny_x.shape[0]),), device=device)
        out = model(tiny_x[idx])
        loss, bce, rec = composite_loss(out, tiny_y[idx], tiny_tm[idx], tiny_bm[idx])
        opt.zero_grad()
        loss.backward()
        grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
        opt.step()
        if step == 1 or step % 10 == 0 or step == TINY_STEPS:
            rows.append(
                {
                    "baseline": name,
                    "stage": "tiny_batch",
                    "step": step,
                    "epoch": "",
                    "train_loss": float(loss.item()),
                    "val_loss": "",
                    "bce_term": float(bce.item()),
                    "magmse_term": float(rec.item()),
                    "lambda_rec": lambda_rec,
                    "lr": BCE_LR,
                    "temperature": BCE_TEMPERATURE,
                    "grad_norm_before_clip": grad_norm,
                }
            )
    with torch.no_grad():
        tiny_final_loss, tiny_final_bce, tiny_final_rec = composite_loss(model(tiny_x), tiny_y, tiny_tm, tiny_bm)
        initial_train_loss, _, _ = composite_loss(model(x), y, train_tm, train_bm)
        initial_val_loss, _, _ = composite_loss(model(valx), valy, val_tm, val_bm)
    for epoch in range(1, SMALL_EPOCHS + 1):
        perm = torch.randperm(x.shape[0], device=device)
        losses: list[float] = []
        bces: list[float] = []
        recs: list[float] = []
        grad_norms: list[float] = []
        for start in range(0, x.shape[0], BATCH_SIZE):
            idx = perm[start : start + BATCH_SIZE]
            out = model(x[idx])
            loss, bce, rec = composite_loss(out, y[idx], train_tm[idx], train_bm[idx])
            opt.zero_grad()
            loss.backward()
            grad_norm = float(torch.nn.utils.clip_grad_norm_(model.parameters(), 20.0).detach().cpu().item())
            opt.step()
            losses.append(float(loss.item()))
            bces.append(float(bce.item()))
            recs.append(float(rec.item()))
            grad_norms.append(grad_norm)
        with torch.no_grad():
            val_loss, val_bce, val_rec = composite_loss(model(valx), valy, val_tm, val_bm)
        rows.append(
            {
                "baseline": name,
                "stage": "small_subset",
                "step": "",
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "val_loss": float(val_loss.item()),
                "bce_term": float(np.mean(bces)),
                "magmse_term": float(np.mean(recs)),
                "val_bce_term": float(val_bce.item()),
                "val_magmse_term": float(val_rec.item()),
                "lambda_rec": lambda_rec,
                "lr": BCE_LR,
                "temperature": BCE_TEMPERATURE,
                "grad_norm_before_clip": float(np.mean(grad_norms)),
            }
        )
    with torch.no_grad():
        final_train_loss, final_train_bce, final_train_rec = composite_loss(model(x), y, train_tm, train_bm)
        final_val_loss, final_val_bce, final_val_rec = composite_loss(model(valx), valy, val_tm, val_bm)
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
    metrics = {
        "baseline": name,
        "lambda_rec": lambda_rec,
        "threshold": threshold,
        "temperature": BCE_TEMPERATURE,
        "lr": BCE_LR,
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": float(tiny_final_loss.item()),
        "tiny_loss_drop_fraction": (tiny_initial - float(tiny_final_loss.item())) / max(tiny_initial, EPS),
        "tiny_final_bce": float(tiny_final_bce.item()),
        "tiny_final_magmse": float(tiny_final_rec.item()),
        "initial_train_loss": float(initial_train_loss.item()),
        "final_train_loss": float(final_train_loss.item()),
        "train_loss_drop_fraction": (float(initial_train_loss.item()) - float(final_train_loss.item())) / max(float(initial_train_loss.item()), EPS),
        "final_train_bce": float(final_train_bce.item()),
        "final_train_magmse": float(final_train_rec.item()),
        "initial_val_loss": float(initial_val_loss.item()),
        "final_val_loss": float(final_val_loss.item()),
        "val_loss_drop_fraction": (float(initial_val_loss.item()) - float(final_val_loss.item())) / max(float(initial_val_loss.item()), EPS),
        "final_val_bce": float(final_val_bce.item()),
        "final_val_magmse": float(final_val_rec.item()),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
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
        inter_power, inter_db_full = full_case_arrays(clean_power, clean_db, eval_indices, inter_by_frame)
        cfg = next(c for c in D1B_SIR_CONFIGS if c["sir_name"] == sir_name)
        case_arrays.append(
            {
                "input_type": "interfered",
                "sir_name": sir_name,
                "target_sir_db": float(cfg["sir_db"]),
                "power": inter_power,
                "db": inter_db_full,
            }
        )
        stacked = np.stack([inter_by_frame[int(idx)] for idx in eval_indices.tolist()])
        for label, model in models.items():
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


def make_summary_rows(fixed_rows: list[dict[str, Any]], recon_rows: list[dict[str, Any]], lambda_values: list[float]) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    specs = [
        ("clean", "clean", ""),
        ("interfered medium", "interfered", "medium"),
        ("MSE output medium", "mse_output", "medium"),
        ("pure BCE output medium", "pure_bce_output", "medium"),
        ("MSE model(clean)", "mse_model_clean", ""),
        ("pure BCE model(clean)", "pure_bce_model_clean", ""),
    ]
    for lam in lambda_values:
        label = f"bce_rec_l{safe_name(lam)}"
        specs.append((f"BCE+rec lambda={lam} output medium", f"{label}_output", "medium"))
        specs.append((f"BCE+rec lambda={lam} model(clean)", f"{label}_model_clean", ""))
    rows: list[dict[str, Any]] = []
    for display, input_type, sir_name in specs:
        metric = pick_metric(fixed_rows, input_type, sir_name, pfa=0.01, mask_name="default", scope="all")
        rec = recon_lookup[(input_type, sir_name)]
        rows.append({"name": display, **metric, **rec})
    return rows


def make_lambda_summary(
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    training_metrics: dict[str, dict[str, Any]],
    lambda_values: list[float],
) -> list[dict[str, Any]]:
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    rows: list[dict[str, Any]] = []
    for lam in lambda_values:
        label = f"bce_rec_l{safe_name(lam)}"
        output = pick_metric(fixed_rows, f"{label}_output", "medium", pfa=0.01, mask_name="default", scope="all")
        clean = pick_metric(fixed_rows, f"{label}_model_clean", "", pfa=0.01, mask_name="default", scope="all")
        narrow = pick_metric(fixed_rows, f"{label}_output", "medium", pfa=0.01, mask_name="narrow", scope="all")
        non = pick_metric(fixed_rows, f"{label}_output", "medium", pfa=0.01, mask_name="default", scope="non_overlap_only")
        rec = recon_lookup[(f"{label}_output", "medium")]
        rec_clean = recon_lookup[(f"{label}_model_clean", "")]
        rows.append(
            {
                "lambda_rec": lam,
                "baseline_label": label,
                "final_val_loss": training_metrics[label]["final_val_loss"],
                "final_val_bce": training_metrics[label]["final_val_bce"],
                "final_val_magmse": training_metrics[label]["final_val_magmse"],
                "output_mse_db_to_clean": rec["mse_db_to_clean"],
                "model_clean_mse_db_to_clean": rec_clean["mse_db_to_clean"],
                "weak_pd": output["weak_pd"],
                "mid_pd": output["mid_pd"],
                "strong_pd": output["strong_pd"],
                "overall_pd": output["overall_pd"],
                "f1": output["f1"],
                "measured_pfa": output["measured_pfa"],
                "false_alarm_count": output["false_alarm_count"],
                "target_peak_abs_bias_db_mean": output["target_peak_abs_bias_db_mean"],
                "clean_weak_pd": clean["weak_pd"],
                "clean_f1": clean["f1"],
                "clean_target_peak_abs_bias_db_mean": clean["target_peak_abs_bias_db_mean"],
                "narrow_weak_pd": narrow["weak_pd"],
                "non_overlap_weak_pd": non["weak_pd"],
            }
        )
    return rows


def choose_best_lambda(lambda_rows: list[dict[str, Any]], mse_metric: dict[str, Any]) -> dict[str, Any]:
    candidates = [
        r
        for r in lambda_rows
        if float(r["model_clean_mse_db_to_clean"]) < 3.0
        and float(r["output_mse_db_to_clean"]) < 3.0
        and float(r["weak_pd"]) >= float(mse_metric["weak_pd"]) - 0.05
    ]
    if not candidates:
        candidates = lambda_rows
    return sorted(
        candidates,
        key=lambda r: (
            float(r["model_clean_mse_db_to_clean"]),
            float(r["output_mse_db_to_clean"]),
            -float(r["weak_pd"]),
        ),
    )[0]


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


def plot_outputs(
    clean_db: np.ndarray,
    test_frames: np.ndarray,
    case_arrays: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    loss_rows: dict[str, list[dict[str, Any]]],
    lambda_rows: list[dict[str, Any]],
    best_label: str,
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 4), dpi=150)
    for name, rows in loss_rows.items():
        small = [r for r in rows if r["stage"] == "small_subset"]
        if small:
            plt.plot([int(r["epoch"]) for r in small], [float(r["val_loss"]) for r in small], label=name)
    plt.yscale("log")
    plt.xlabel("epoch")
    plt.ylabel("validation loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "loss_curves.png")
    plt.close()

    frame = int(test_frames[0])
    lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    x = np.arange(clean_db.shape[1])
    plt.figure(figsize=(11, 4), dpi=150)
    for label, key in [
        ("clean", ("clean", "")),
        ("interfered", ("interfered", "medium")),
        ("MSE", ("mse_output", "medium")),
        ("pure BCE", ("pure_bce_output", "medium")),
        ("BCE+rec", (f"{best_label}_output", "medium")),
    ]:
        plt.plot(x, lookup[key]["db"][frame], label=label)
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_vs_interfered_vs_outputs_range_profile.png")
    plt.close()

    plt.figure(figsize=(11, 4), dpi=150)
    for label, key in [
        ("clean", ("clean", "")),
        ("MSE clean", ("mse_model_clean", "")),
        ("pure BCE clean", ("pure_bce_model_clean", "")),
        ("BCE+rec clean", (f"{best_label}_model_clean", "")),
    ]:
        plt.plot(x, lookup[key]["db"][frame], label=label)
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "model_clean_comparison.png")
    plt.close()

    key_types = [
        ("MSE", "mse_output", "medium"),
        ("pure BCE", "pure_bce_output", "medium"),
        ("BCE+rec", f"{best_label}_output", "medium"),
    ]
    metric_rows = [pick_metric(fixed_rows, input_type, sir_name, pfa=0.01, mask_name="default", scope="all") for _, input_type, sir_name in key_types]
    labels = [x[0] for x in key_types]
    xs = np.arange(len(labels))
    width = 0.25
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(xs - width, [float(r["weak_pd"]) for r in metric_rows], width, label="weak")
    plt.bar(xs, [float(r["mid_pd"]) for r in metric_rows], width, label="mid")
    plt.bar(xs + width, [float(r["strong_pd"]) for r in metric_rows], width, label="strong")
    plt.xticks(xs, labels)
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_pd_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot(labels, [float(r["measured_pfa"]) for r in metric_rows], marker="o", label="PFA")
    plt.bar(labels, [float(r["false_alarm_count"]) / max(float(r["background_cell_count"]), 1.0) for r in metric_rows], alpha=0.35, label="FA/background")
    plt.ylabel("rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_false_alarm_count_comparison.png")
    plt.close()

    rec_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(rec_lookup[(input_type, sir_name)]["mse_db_to_clean"]) for _, input_type, sir_name in key_types])
    plt.ylabel("MSE dB to clean")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "mse_magmse_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(r["target_peak_abs_bias_db_mean"]) for r in metric_rows])
    plt.ylabel("target peak abs bias (dB)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_bias_histogram.png")
    plt.close()

    clean_rows = [
        pick_metric(fixed_rows, "mse_model_clean", pfa=0.01, mask_name="default", scope="all"),
        pick_metric(fixed_rows, "pure_bce_model_clean", pfa=0.01, mask_name="default", scope="all"),
        pick_metric(fixed_rows, f"{best_label}_model_clean", pfa=0.01, mask_name="default", scope="all"),
    ]
    clean_labels = ["MSE clean", "pure BCE clean", "BCE+rec clean"]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(clean_labels, [float(r["mse_db_to_clean"]) for r in clean_rows])
    plt.ylabel("model(clean) MSE dB to clean")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_input_no_harm_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot([float(r["lambda_rec"]) for r in lambda_rows], [float(r["model_clean_mse_db_to_clean"]) for r in lambda_rows], marker="o", label="model(clean) MSE")
    plt.plot([float(r["lambda_rec"]) for r in lambda_rows], [float(r["weak_pd"]) for r in lambda_rows], marker="s", label="weak Pd")
    plt.xlabel("lambda_rec")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "lambda_rec_tradeoff_plot.png")
    plt.close()

    pure_res = lookup[("pure_bce_model_clean", "")]["db"][frame] - clean_db[frame]
    best_res = lookup[(f"{best_label}_model_clean", "")]["db"][frame] - clean_db[frame]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(pure_res, bins=40, alpha=0.65, label="pure BCE residual")
    plt.hist(best_res, bins=40, alpha=0.65, label="BCE+rec residual")
    plt.xlabel("model(clean)-clean residual (dB)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "detection_shaping_visualization_pure_bce.png")
    plt.close()


def write_report(
    mse_metrics: dict[str, Any],
    pure_metrics: dict[str, Any],
    rec_training_metrics: dict[str, dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    lambda_rows: list[dict[str, Any]],
) -> tuple[bool, str, dict[str, Any]]:
    mse = pick_metric(fixed_rows, "mse_output", "medium", pfa=0.01, mask_name="default", scope="all")
    pure = pick_metric(fixed_rows, "pure_bce_output", "medium", pfa=0.01, mask_name="default", scope="all")
    pure_clean = pick_metric(fixed_rows, "pure_bce_model_clean", pfa=0.01, mask_name="default", scope="all")
    best = choose_best_lambda(lambda_rows, mse)
    best_label = str(best["baseline_label"])
    best_output = pick_metric(fixed_rows, f"{best_label}_output", "medium", pfa=0.01, mask_name="default", scope="all")
    best_clean = pick_metric(fixed_rows, f"{best_label}_model_clean", pfa=0.01, mask_name="default", scope="all")
    best_narrow = pick_metric(fixed_rows, f"{best_label}_output", "medium", pfa=0.01, mask_name="narrow", scope="all")
    mse_narrow = pick_metric(fixed_rows, "mse_output", "medium", pfa=0.01, mask_name="narrow", scope="all")
    best_non = pick_metric(fixed_rows, f"{best_label}_output", "medium", pfa=0.01, mask_name="default", scope="non_overlap_only")
    mse_non = pick_metric(fixed_rows, "mse_output", "medium", pfa=0.01, mask_name="default", scope="non_overlap_only")
    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    pure_rec = recon_lookup[("pure_bce_output", "medium")]
    pure_clean_rec = recon_lookup[("pure_bce_model_clean", "")]
    best_rec = recon_lookup[(f"{best_label}_output", "medium")]
    best_clean_rec = recon_lookup[(f"{best_label}_model_clean", "")]

    mse_ok = float(mse_metrics["train_loss_drop_fraction"]) > 0.2 and not bool(mse_metrics["has_nan_or_inf"])
    pure_failure_control_ok = (
        float(pure_clean_rec["mse_db_to_clean"]) > 3.0
        and float(pure_rec["mse_db_to_clean"]) > 3.0
        and float(pure["weak_pd"]) >= float(mse["weak_pd"]) - 0.05
    )
    rec_train_ok = all(float(v["train_loss_drop_fraction"]) > 0.05 and not bool(v["has_nan_or_inf"]) for v in rec_training_metrics.values())
    rec_stable = (
        float(best_rec["mse_db_to_clean"]) < float(pure_rec["mse_db_to_clean"]) * 0.2
        and float(best_clean_rec["mse_db_to_clean"]) < float(pure_clean_rec["mse_db_to_clean"]) * 0.2
        and float(best_output["target_peak_abs_bias_db_mean"]) < float(pure["target_peak_abs_bias_db_mean"]) * 0.5
        and float(best_rec["mse_db_to_clean"]) < 3.0
        and float(best_clean_rec["mse_db_to_clean"]) < 3.0
    )
    weak_not_worse_than_mse = float(best_output["weak_pd"]) >= float(mse["weak_pd"]) - 0.05
    clean_no_harm = float(best_clean_rec["mse_db_to_clean"]) < 3.0 and float(best_clean["measured_pfa"]) < 0.08
    mask_consistent = (float(best_output["weak_pd"]) - float(mse["weak_pd"])) * (
        float(best_narrow["weak_pd"]) - float(mse_narrow["weak_pd"])
    ) >= 0
    non_overlap_consistent = (float(best_output["weak_pd"]) - float(mse["weak_pd"])) * (
        float(best_non["weak_pd"]) - float(mse_non["weak_pd"])
    ) >= 0
    output_stable = float(best["model_clean_mse_db_to_clean"]) < 3.0 and float(best["output_mse_db_to_clean"]) < 3.0
    d3_rerun_pass = all(
        [
            mse_ok,
            pure_failure_control_ok,
            rec_train_ok,
            rec_stable,
            weak_not_worse_than_mse,
            clean_no_harm,
            mask_consistent,
            non_overlap_consistent,
            output_stable,
        ]
    )
    next_step = (
        "可以进入 D4，但 D4 仍只应做 tuned balanced BCE / focal loss 强 baseline，不能直接进入 weak-target full loss。"
        if d3_rerun_pass
        else "不建议进入 D4；应先检查 BCE+rec 的训练稳定性、lambda_rec 选择或 fixed-PFA/mask 口径。"
    )
    report = f"""# D3-Rerun Gao77 Baseline Sanity 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D3-Rerun，仅修正后的 range-only baseline sanity  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次不是 D4。没有做 focal loss、balanced BCE、weak-target full loss、false alarm penalty、clean identity full method、3 seeds，也没有引入 RDLR-Net / DiffRIM / RIMformer。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D3-Rerun 是否通过 | {'通过' if d3_rerun_pass else '未通过'} |
| MSE/MAGMSE baseline 是否正常 | {'是' if mse_ok else '否'} |
| pure BCE failure control 是否复现 detection-shaping | {'是' if pure_failure_control_ok else '否'} |
| BCE+rec 是否缓解幅度破坏 | {'是' if rec_stable else '否'} |
| 最稳 lambda_rec | {best['lambda_rec']} |
| BCE+rec 相比 MSE 的 fixed-PFA weak Pd | best={float(best_output['weak_pd']):.4f}, MSE={float(mse['weak_pd']):.4f} |
| BCE+rec 相比 pure BCE 的 clean no-harm | best model(clean) MSE={float(best_clean_rec['mse_db_to_clean']):.4f}, pure BCE={float(pure_clean_rec['mse_db_to_clean']):.4f} |
| BCE+rec 是否仍有 detection-shaping 副作用 | {'轻微/可控' if clean_no_harm else '仍明显'} |
| clean-input no-harm 是否通过 | {'是' if clean_no_harm else '否'} |
| narrow/default mask 是否一致 | {'是' if mask_consistent else '否'} |
| all targets / non-overlap-only 是否一致 | {'是' if non_overlap_consistent else '否'} |
| 是否建议进入 D4 | {'是' if d3_rerun_pass else '否'} |
| 下一步 | {next_step} |

## 3. Baseline 对比

default mask、clean_peak_percentile、PFA=1e-2：

{md_table(summary_rows, ['name', 'mse_db_to_clean', 'measured_pfa', 'false_alarm_count', 'background_cell_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'target_peak_abs_bias_db_mean'])}

## 4. Lambda_rec 对比

{md_table(lambda_rows, ['lambda_rec', 'final_val_loss', 'final_val_bce', 'final_val_magmse', 'output_mse_db_to_clean', 'model_clean_mse_db_to_clean', 'weak_pd', 'f1', 'false_alarm_count', 'target_peak_abs_bias_db_mean', 'narrow_weak_pd', 'non_overlap_weak_pd'])}

## 5. 关键判断

- pure BCE 检测指标可能较高，但 clean no-harm 失败，因此只能作为 invalid detection-shaping failure control。
- BCE+rec 是修正后的 ordinary detection-aware baseline，不是 proposed method。
- severe interference 仍只作为 stress test，不作为 D3-Rerun 是否通过的唯一依据。

## 6. 输出文件

结果目录：`G:\\mineru_output\\results\\d3_rerun_gao77_baseline_sanity`  
图像目录：`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d3_rerun_figures`

关键 CSV/JSON 已按要求生成，包括 fixed-PFA、clean no-harm、reconstruction、mask、non-overlap、per-sequence、per-class-group、baseline comparison 和 lambda_rec summary。

## 7. D4 建议

{next_step}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return d3_rerun_pass, str(report_ts), best, next_step


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

    mse_model, mse_rows, mse_metrics = train_mse_baseline(train_x, train_y, val_x, val_y, norm_mean, norm_std, device)
    pure_model, pure_rows, pure_metrics = train_detection_baseline(
        "pure_bce",
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
        lambda_rec=0.0,
        seed_offset=200,
    )
    models: dict[str, SimpleRangeFCN] = {"mse": mse_model, "pure_bce": pure_model}
    rec_loss_rows: list[dict[str, Any]] = []
    rec_training_metrics: dict[str, dict[str, Any]] = {}
    for i, lam in enumerate(LAMBDA_REC_VALUES):
        label = f"bce_rec_l{safe_name(lam)}"
        model, rows, metrics = train_detection_baseline(
            label,
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
            lambda_rec=lam,
            seed_offset=300 + i,
        )
        models[label] = model
        rec_loss_rows.extend(rows)
        rec_training_metrics[label] = metrics

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
    metrics = evaluate_cases(manifest, targets, contexts, clean_power, clean_db, val_frames, test_frames, case_arrays)
    recon_rows = reconstruction_metrics(case_arrays, clean_db, clean_power, test_frames)
    summary_rows = make_summary_rows(metrics["fixed"], recon_rows, LAMBDA_REC_VALUES)
    all_training_metrics = {"mse": mse_metrics, "pure_bce": pure_metrics, **rec_training_metrics}
    lambda_rows = make_lambda_summary(metrics["fixed"], recon_rows, all_training_metrics, LAMBDA_REC_VALUES)
    mse_metric = pick_metric(metrics["fixed"], "mse_output", "medium", pfa=0.01, mask_name="default", scope="all")
    best_lambda = choose_best_lambda(lambda_rows, mse_metric)
    best_label = str(best_lambda["baseline_label"])
    plot_outputs(
        clean_db,
        test_frames,
        case_arrays,
        metrics["fixed"],
        recon_rows,
        {"mse": mse_rows, "pure_bce": pure_rows, "bce_rec": rec_loss_rows},
        lambda_rows,
        best_label,
    )

    dataset_rows = train_rows + val_rows + eval_val_rows + eval_test_rows
    write_csv(RESULT_DIR / "d3_rerun_dataset_manifest.csv", dataset_rows)
    write_csv(RESULT_DIR / "d3_rerun_training_loss_mse.csv", mse_rows)
    write_csv(RESULT_DIR / "d3_rerun_training_loss_pure_bce.csv", pure_rows)
    write_csv(RESULT_DIR / "d3_rerun_training_loss_bce_rec.csv", rec_loss_rows)
    write_csv(RESULT_DIR / "d3_rerun_fixed_pfa_metrics.csv", metrics["fixed"])
    clean_no_harm = [r for r in metrics["fixed"] if str(r["input_type"]).endswith("_model_clean")]
    write_csv(RESULT_DIR / "d3_rerun_clean_no_harm_metrics.csv", clean_no_harm)
    write_csv(RESULT_DIR / "d3_rerun_reconstruction_metrics.csv", recon_rows)
    write_csv(RESULT_DIR / "d3_rerun_metrics_by_mask.csv", metrics["by_mask"])
    write_csv(RESULT_DIR / "d3_rerun_metrics_non_overlap_only.csv", metrics["non_overlap"])
    write_csv(RESULT_DIR / "d3_rerun_metrics_by_sequence.csv", metrics["by_sequence"])
    write_csv(RESULT_DIR / "d3_rerun_metrics_by_class_group.csv", metrics["by_class"])
    write_csv(RESULT_DIR / "d3_rerun_baseline_comparison_summary.csv", summary_rows)
    write_csv(RESULT_DIR / "d3_rerun_lambda_rec_summary.csv", lambda_rows)
    write_csv(RESULT_DIR / "d3_rerun_training_summary.csv", list(all_training_metrics.values()))
    write_model_summary(RESULT_DIR / "d3_rerun_model_summary_mse.txt", mse_model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    write_model_summary(RESULT_DIR / "d3_rerun_model_summary_pure_bce.txt", pure_model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    for label, model in models.items():
        if label.startswith("bce_rec"):
            write_model_summary(RESULT_DIR / f"d3_rerun_model_summary_{label}.txt", model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)

    d3_pass, report_ts, best, next_step = write_report(
        mse_metrics,
        pure_metrics,
        rec_training_metrics,
        metrics["fixed"],
        recon_rows,
        summary_rows,
        lambda_rows,
    )
    write_json(
        RESULT_DIR / "d3_rerun_config.json",
        {
            "stage": "D3-Rerun",
            "strict_limits": {
                "not_d4": True,
                "no_focal_loss": True,
                "no_balanced_bce": True,
                "no_weak_target_full_loss": True,
                "no_false_alarm_penalty": True,
                "no_clean_identity_full_method": True,
                "no_3_seeds": True,
                "no_rdlr_diffirm_rimformer": True,
                "no_d5": True,
            },
            "model": "SimpleRangeFCN",
            "train_frames": int(train_frames.size),
            "train_samples": int(train_x.shape[0]),
            "val_frames": int(val_frames.size),
            "val_samples": int(val_x.shape[0]),
            "test_frames": int(test_frames.size),
            "batch_size": BATCH_SIZE,
            "tiny_steps": TINY_STEPS,
            "small_epochs": SMALL_EPOCHS,
            "mse_lr": MSE_LR,
            "bce_lr": BCE_LR,
            "bce_temperature": BCE_TEMPERATURE,
            "lambda_rec_values": LAMBDA_REC_VALUES,
            "best_lambda_rec": best["lambda_rec"],
            "normalization": {"mean_db": norm_mean, "std_db": norm_std},
            "device": str(device),
        },
    )
    print(
        json.dumps(
            {
                "d3_rerun_pass": d3_pass,
                "best_lambda_rec": best["lambda_rec"],
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
