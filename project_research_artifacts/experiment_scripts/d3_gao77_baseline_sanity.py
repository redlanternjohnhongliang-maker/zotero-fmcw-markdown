from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F

from d1a_gao77_clean_fixed_pfa_sanity import (
    EXPECTED_ADC_SHAPE,
    ROOT,
    ca_cfar_score_1d_np,
    write_csv,
    write_json,
)
from d1b_gao77_synthetic_interference_sanity import (
    EPS,
    SIR_CONFIGS as D1B_SIR_CONFIGS,
    build_mask_context,
)
from d2a_gao77_small_model_sanity import (
    SimpleRangeFCN,
    build_frame_count_cache,
    db,
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
    normalize,
    power_from_db,
    sir_cfg,
    write_model_summary,
)


RESULT_DIR = ROOT / "results" / "d3_gao77_baseline_sanity"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d3_figures"
REPORT_PATH = ROOT / "refine-logs" / "D3_GAO77_BASELINE_SANITY_REPORT.md"

RANDOM_SEED = 20260626
VALID_PFA_TARGETS = [1e-2, 1e-3]
ACTIVE_MASK_NAMES = {"narrow", "default"}
TRAIN_SIR_NAMES = ["light", "medium"]
VAL_SIR_NAMES = ["light", "medium"]
TEST_SIR_NAMES = ["light", "medium", "severe"]
EVAL_SIR_NAMES = ["light", "medium", "severe"]

N_TRAIN_FRAMES = 512
N_VAL_FRAMES = 160
N_TEST_FRAMES = 160
BATCH_SIZE = 4
TINY_SAMPLE_COUNT = 16
TINY_STEPS = 220
SMALL_EPOCHS = 10
MSE_LR = 1.5e-3
BCE_LR = 8e-4
BCE_TEMPERATURE = 0.7


def cfar_score_torch(power: torch.Tensor, guard: int = 2, train: int = 10) -> torch.Tensor:
    width = 2 * (guard + train) + 1
    kernel = torch.ones(width, dtype=power.dtype, device=power.device)
    center = guard + train
    kernel[center - guard : center + guard + 1] = 0.0
    kernel = kernel.view(1, 1, -1)
    x = power[:, None, :]
    local_sum = F.conv1d(x, kernel, padding=width // 2)[:, 0, :]
    counts = F.conv1d(torch.ones_like(x), kernel, padding=width // 2)[:, 0, :].clamp_min(1.0)
    local_mean = local_sum / counts
    return power / (local_mean + EPS)


def differentiable_detection_map_from_norm(
    output_norm: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
    temperature: float = BCE_TEMPERATURE,
) -> torch.Tensor:
    db_out = output_norm[:, 0, :] * std + mean
    power = torch.pow(10.0, torch.clamp(db_out, -80.0, 100.0) / 10.0)
    score = cfar_score_torch(power)
    return torch.sigmoid((score - threshold) / temperature)


def detection_bce_loss(
    output_norm: torch.Tensor,
    target_mask: torch.Tensor,
    background_mask: torch.Tensor,
    mean: float,
    std: float,
    threshold: float,
) -> torch.Tensor:
    soft = differentiable_detection_map_from_norm(output_norm, mean, std, threshold)
    valid = target_mask | background_mask
    labels = torch.zeros_like(soft)
    labels[target_mask] = 1.0
    return F.binary_cross_entropy(soft[valid], labels[valid])


def masks_for_rows(rows: list[dict[str, Any]], ctx: dict[str, Any], device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    frame_indices = [int(row["frame_idx"]) for row in rows]
    target = torch.from_numpy(ctx["target_mask"][frame_indices].astype(bool)).to(device)
    background = torch.from_numpy(ctx["background_mask"][frame_indices].astype(bool)).to(device)
    return target, background


def train_mse_baseline(
    train_x: np.ndarray,
    train_y: np.ndarray,
    val_x: np.ndarray,
    val_y: np.ndarray,
    mean: float,
    std: float,
    device: torch.device,
) -> tuple[SimpleRangeFCN, list[dict[str, Any]], dict[str, Any]]:
    torch.manual_seed(RANDOM_SEED + 300)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=MSE_LR)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    batch_size = min(BATCH_SIZE, x.shape[0])
    rows: list[dict[str, Any]] = []

    tiny_x = x[:TINY_SAMPLE_COUNT]
    tiny_y = y[:TINY_SAMPLE_COUNT]
    with torch.no_grad():
        tiny_initial = float(torch.mean((model(tiny_x) - tiny_y) ** 2).item())
    for step in range(1, TINY_STEPS + 1):
        idx = torch.randint(0, tiny_x.shape[0], (min(batch_size, tiny_x.shape[0]),), device=device)
        pred = model(tiny_x[idx])
        loss = torch.mean((pred - tiny_y[idx]) ** 2)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step == 1 or step % 5 == 0 or step == TINY_STEPS:
            rows.append(
                {
                    "baseline": "mse",
                    "stage": "tiny_batch",
                    "step": step,
                    "epoch": "",
                    "train_loss": float(loss.item()),
                    "val_loss": "",
                    "detection_bce_loss": "",
                    "lr": MSE_LR,
                }
            )
    with torch.no_grad():
        tiny_final = float(torch.mean((model(tiny_x) - tiny_y) ** 2).item())
        initial_train = float(torch.mean((model(x) - y) ** 2).item())
        initial_val = float(torch.mean((model(valx) - valy) ** 2).item())

    for epoch in range(1, SMALL_EPOCHS + 1):
        perm = torch.randperm(x.shape[0], device=device)
        losses: list[float] = []
        for start in range(0, x.shape[0], batch_size):
            idx = perm[start : start + batch_size]
            pred = model(x[idx])
            loss = torch.mean((pred - y[idx]) ** 2)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.item()))
        with torch.no_grad():
            val_loss = float(torch.mean((model(valx) - valy) ** 2).item())
        rows.append(
            {
                "baseline": "mse",
                "stage": "small_subset",
                "step": "",
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "val_loss": val_loss,
                "detection_bce_loss": "",
                "lr": MSE_LR,
            }
        )

    with torch.no_grad():
        train_out = denormalize(model(x).detach().cpu().numpy()[:, 0, :], mean, std)
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
        final_train = float(torch.mean((model(x) - y) ** 2).item())
        final_val = float(torch.mean((model(valx) - valy) ** 2).item())
    metrics = {
        "baseline": "mse",
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": tiny_final,
        "tiny_loss_drop_fraction": (tiny_initial - tiny_final) / max(tiny_initial, EPS),
        "initial_train_loss": initial_train,
        "final_train_loss": final_train,
        "train_loss_drop_fraction": (initial_train - final_train) / max(initial_train, EPS),
        "initial_val_loss": initial_val,
        "final_val_loss": final_val,
        "val_loss_drop_fraction": (initial_val - final_val) / max(initial_val, EPS),
        "train_input_mse_db": mse_np(train_x, train_y),
        "train_output_mse_db": mse_np(train_out, train_y),
        "val_input_mse_db": mse_np(val_x, val_y),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
        "lr": MSE_LR,
    }
    return model, rows, metrics


def train_bce_baseline(
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
) -> tuple[SimpleRangeFCN, list[dict[str, Any]], dict[str, Any], float]:
    torch.manual_seed(RANDOM_SEED + 400)
    model = SimpleRangeFCN(train_x.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=BCE_LR)
    x = make_tensor(train_x, mean, std, device)
    y = make_tensor(train_y, mean, std, device)
    valx = make_tensor(val_x, mean, std, device)
    valy = make_tensor(val_y, mean, std, device)
    default_ctx = contexts["default"]
    train_tm, train_bm = masks_for_rows(train_rows, default_ctx, device)
    val_tm, val_bm = masks_for_rows(val_rows, default_ctx, device)
    clean_cfar = ca_cfar_score_1d_np(clean_power)
    threshold = float(np.quantile(clean_cfar[val_frames][default_ctx["background_mask"][val_frames]], 0.99))
    batch_size = min(BATCH_SIZE, x.shape[0])
    rows: list[dict[str, Any]] = []

    tiny_x = x[:TINY_SAMPLE_COUNT]
    tiny_y = y[:TINY_SAMPLE_COUNT]
    tiny_tm = train_tm[:TINY_SAMPLE_COUNT]
    tiny_bm = train_bm[:TINY_SAMPLE_COUNT]
    with torch.no_grad():
        tiny_initial = float(detection_bce_loss(model(tiny_x), tiny_tm, tiny_bm, mean, std, threshold).item())
    for step in range(1, TINY_STEPS + 1):
        idx = torch.randint(0, tiny_x.shape[0], (min(batch_size, tiny_x.shape[0]),), device=device)
        out = model(tiny_x[idx])
        loss = detection_bce_loss(out, tiny_tm[idx], tiny_bm[idx], mean, std, threshold)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step == 1 or step % 5 == 0 or step == TINY_STEPS:
            rows.append(
                {
                    "baseline": "ordinary_bce",
                    "stage": "tiny_batch",
                    "step": step,
                    "epoch": "",
                    "train_loss": float(loss.item()),
                    "val_loss": "",
                    "detection_bce_loss": float(loss.item()),
                    "lr": BCE_LR,
                }
            )
    with torch.no_grad():
        tiny_final = float(detection_bce_loss(model(tiny_x), tiny_tm, tiny_bm, mean, std, threshold).item())
        initial_train = float(detection_bce_loss(model(x), train_tm, train_bm, mean, std, threshold).item())
        initial_val = float(detection_bce_loss(model(valx), val_tm, val_bm, mean, std, threshold).item())

    for epoch in range(1, SMALL_EPOCHS + 1):
        perm = torch.randperm(x.shape[0], device=device)
        losses: list[float] = []
        for start in range(0, x.shape[0], batch_size):
            idx = perm[start : start + batch_size]
            out = model(x[idx])
            loss = detection_bce_loss(out, train_tm[idx], train_bm[idx], mean, std, threshold)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(float(loss.item()))
        with torch.no_grad():
            val_loss = float(detection_bce_loss(model(valx), val_tm, val_bm, mean, std, threshold).item())
        rows.append(
            {
                "baseline": "ordinary_bce",
                "stage": "small_subset",
                "step": "",
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "val_loss": val_loss,
                "detection_bce_loss": float(np.mean(losses)),
                "lr": BCE_LR,
            }
        )

    with torch.no_grad():
        train_out = denormalize(model(x).detach().cpu().numpy()[:, 0, :], mean, std)
        val_out = denormalize(model(valx).detach().cpu().numpy()[:, 0, :], mean, std)
        final_train = float(detection_bce_loss(model(x), train_tm, train_bm, mean, std, threshold).item())
        final_val = float(detection_bce_loss(model(valx), val_tm, val_bm, mean, std, threshold).item())
    metrics = {
        "baseline": "ordinary_bce",
        "tiny_initial_loss": tiny_initial,
        "tiny_final_loss": tiny_final,
        "tiny_loss_drop_fraction": (tiny_initial - tiny_final) / max(tiny_initial, EPS),
        "initial_train_loss": initial_train,
        "final_train_loss": final_train,
        "train_loss_drop_fraction": (initial_train - final_train) / max(initial_train, EPS),
        "initial_val_loss": initial_val,
        "final_val_loss": final_val,
        "val_loss_drop_fraction": (initial_val - final_val) / max(initial_val, EPS),
        "train_input_mse_db": mse_np(train_x, train_y),
        "train_output_mse_db": mse_np(train_out, train_y),
        "val_input_mse_db": mse_np(val_x, val_y),
        "val_output_mse_db": mse_np(val_out, val_y),
        "output_min_db": float(np.min(val_out)),
        "output_max_db": float(np.max(val_out)),
        "output_std_db": float(np.std(val_out)),
        "has_nan_or_inf": bool(not np.isfinite(val_out).all()),
        "lr": BCE_LR,
        "bce_threshold": threshold,
        "bce_temperature": BCE_TEMPERATURE,
    }
    return model, rows, metrics, threshold


def build_case_arrays(
    clean_power: np.ndarray,
    clean_db: np.ndarray,
    val_frames: np.ndarray,
    test_frames: np.ndarray,
    eval_val_inter_db: dict[str, dict[int, np.ndarray]],
    eval_test_inter_db: dict[str, dict[int, np.ndarray]],
    mse_model: SimpleRangeFCN,
    bce_model: SimpleRangeFCN,
    mean: float,
    std: float,
    device: torch.device,
) -> list[dict[str, Any]]:
    eval_indices = np.unique(np.concatenate([val_frames, test_frames]))
    case_arrays: list[dict[str, Any]] = [
        {"input_type": "clean", "sir_name": "", "target_sir_db": "", "power": clean_power, "db": clean_db}
    ]
    clean_eval = clean_db[eval_indices]
    for label, model in [("mse_model_clean", mse_model), ("bce_model_clean", bce_model)]:
        model_clean_eval = infer_db(model, clean_eval, mean, std, device)
        by_frame = {int(idx): model_clean_eval[i] for i, idx in enumerate(eval_indices.tolist())}
        power, db_arr = full_case_arrays(clean_power, clean_db, eval_indices, by_frame)
        case_arrays.append({"input_type": label, "sir_name": "", "target_sir_db": "", "power": power, "db": db_arr})

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
        for input_type, model in [("mse_output", mse_model), ("ordinary_bce_output", bce_model)]:
            out_eval = infer_db(model, stacked, mean, std, device)
            by_frame = {int(idx): out_eval[i] for i, idx in enumerate(eval_indices.tolist())}
            power, db_arr = full_case_arrays(clean_power, clean_db, eval_indices, by_frame)
            case_arrays.append(
                {
                    "input_type": input_type,
                    "sir_name": name,
                    "target_sir_db": float(cfg["sir_db"]),
                    "power": power,
                    "db": db_arr,
                }
            )
    return case_arrays


def reconstruction_metrics(case_arrays: list[dict[str, Any]], clean_db: np.ndarray, clean_power: np.ndarray, test_idx: np.ndarray) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in case_arrays:
        rows.append(
            {
                "input_type": case["input_type"],
                "sir_name": case.get("sir_name", ""),
                "target_sir_db": case.get("target_sir_db", ""),
                "mse_db_to_clean": mse_np(case["db"][test_idx], clean_db[test_idx]),
                "mse_power_to_clean": mse_np(case["power"][test_idx], clean_power[test_idx]),
                "magmse_db_to_clean": float(np.mean(np.abs(case["db"][test_idx] - clean_db[test_idx]) ** 2)),
            }
        )
    return rows


def pick_metric(
    rows: list[dict[str, Any]],
    input_type: str,
    sir_name: str = "",
    mask_name: str = "default",
    split_definition: str = "clean_peak_percentile",
    pfa: float = 0.01,
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


def plot_outputs(
    mse_loss_rows: list[dict[str, Any]],
    bce_loss_rows: list[dict[str, Any]],
    clean_db: np.ndarray,
    test_frames: np.ndarray,
    case_arrays: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for name, rows, path in [
        ("MSE baseline loss curve", mse_loss_rows, "mse_baseline_loss_curve.png"),
        ("ordinary BCE baseline loss curve", bce_loss_rows, "ordinary_bce_baseline_loss_curve.png"),
    ]:
        tiny = [r for r in rows if r["stage"] == "tiny_batch"]
        small = [r for r in rows if r["stage"] == "small_subset"]
        plt.figure(figsize=(8, 4), dpi=150)
        if tiny:
            plt.plot([int(r["step"]) for r in tiny], [float(r["train_loss"]) for r in tiny], label="tiny train")
        if small:
            plt.plot([int(r["epoch"]) for r in small], [float(r["train_loss"]) for r in small], label="small train")
            plt.plot([int(r["epoch"]) for r in small], [float(r["val_loss"]) for r in small], label="small val")
        plt.yscale("log")
        plt.xlabel("Step / epoch")
        plt.ylabel("loss")
        plt.title(name)
        plt.legend()
        plt.tight_layout()
        plt.savefig(FIG_DIR / path)
        plt.close()

    sample_frame = int(test_frames[0])
    lookup = {(c["input_type"], str(c.get("sir_name", ""))): c for c in case_arrays}
    x = np.arange(clean_db.shape[1])
    plt.figure(figsize=(10, 4), dpi=150)
    plt.plot(x, clean_db[sample_frame], label="clean")
    plt.plot(x, lookup[("interfered", "medium")]["db"][sample_frame], label="interfered medium")
    plt.plot(x, lookup[("mse_output", "medium")]["db"][sample_frame], label="MSE output")
    plt.plot(x, lookup[("ordinary_bce_output", "medium")]["db"][sample_frame], label="BCE output")
    plt.xlabel("Range bin")
    plt.ylabel("Power (dB)")
    plt.title("Clean vs interfered vs MSE output vs BCE output")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_vs_interfered_vs_mse_vs_bce_range_profile.png")
    plt.close()

    key_types = [("interfered", "medium"), ("mse_output", "medium"), ("ordinary_bce_output", "medium")]
    metric_rows = [
        pick_metric(fixed_rows, input_type, sir_name)
        for input_type, sir_name in key_types
    ]
    labels = ["interfered", "MSE", "BCE"]
    xs = np.arange(len(metric_rows))
    width = 0.25
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(xs - width, [float(r["weak_pd"]) for r in metric_rows], width, label="weak")
    plt.bar(xs, [float(r["mid_pd"]) for r in metric_rows], width, label="mid")
    plt.bar(xs + width, [float(r["strong_pd"]) for r in metric_rows], width, label="strong")
    plt.xticks(xs, labels)
    plt.ylim(0, 1.05)
    plt.ylabel("Pd")
    plt.title("Weak/mid/strong Pd comparison")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "weak_mid_strong_pd_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.plot(labels, [float(r["measured_pfa"]) for r in metric_rows], marker="o")
    plt.ylabel("Measured PFA")
    plt.title("PFA comparison")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pfa_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(r["false_alarm_count"]) for r in metric_rows])
    plt.ylabel("False alarm count")
    plt.title("False alarm count comparison")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "false_alarm_count_comparison.png")
    plt.close()

    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(recon_lookup[k]["mse_db_to_clean"]) for k in key_types])
    plt.ylabel("MSE dB to clean")
    plt.title("MSE/MAGMSE comparison")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "mse_magmse_comparison.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(r["target_peak_abs_bias_db_mean"]) for r in metric_rows])
    plt.ylabel("Mean abs target peak bias (dB)")
    plt.title("Target peak bias histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "target_peak_bias_histogram.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(labels, [float(r["noise_floor_change_db"]) for r in metric_rows])
    plt.ylabel("Noise floor change (dB)")
    plt.title("Noise floor change histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "noise_floor_change_histogram.png")
    plt.close()

    clean_rows = [pick_metric(fixed_rows, "clean"), pick_metric(fixed_rows, "mse_model_clean"), pick_metric(fixed_rows, "bce_model_clean")]
    clean_labels = ["clean", "MSE clean", "BCE clean"]
    plt.figure(figsize=(8, 4), dpi=150)
    plt.bar(clean_labels, [float(r["mse_db_to_clean"]) for r in clean_rows])
    plt.ylabel("MSE dB to clean")
    plt.title("Clean-input no-harm comparison")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "clean_input_no_harm_comparison.png")
    plt.close()


def write_report(
    mse_metrics: dict[str, Any],
    bce_metrics: dict[str, Any],
    fixed_rows: list[dict[str, Any]],
    recon_rows: list[dict[str, Any]],
) -> tuple[bool, str]:
    mse_medium = pick_metric(fixed_rows, "mse_output", "medium")
    bce_medium = pick_metric(fixed_rows, "ordinary_bce_output", "medium")
    mse_clean = pick_metric(fixed_rows, "mse_model_clean")
    bce_clean = pick_metric(fixed_rows, "bce_model_clean")
    mse_narrow = pick_metric(fixed_rows, "mse_output", "medium", mask_name="narrow")
    bce_narrow = pick_metric(fixed_rows, "ordinary_bce_output", "medium", mask_name="narrow")
    mse_non = pick_metric(fixed_rows, "mse_output", "medium", scope="non_overlap_only")
    bce_non = pick_metric(fixed_rows, "ordinary_bce_output", "medium", scope="non_overlap_only")
    clean = pick_metric(fixed_rows, "clean")

    mse_train_ok = float(mse_metrics["train_loss_drop_fraction"]) > 0.2 and not bool(mse_metrics["has_nan_or_inf"])
    bce_train_ok = float(bce_metrics["train_loss_drop_fraction"]) > 0.05 and not bool(bce_metrics["has_nan_or_inf"])
    fixed_ok = len(fixed_rows) > 0 and all(str(r.get("measured_pfa", "")) != "" for r in fixed_rows)
    bce_not_worse = (
        float(bce_medium["weak_pd"]) >= float(mse_medium["weak_pd"]) - 0.05
        and float(bce_medium["overall_pd"]) >= float(mse_medium["overall_pd"]) - 0.05
        and float(bce_medium["f1"]) >= float(mse_medium["f1"]) - 0.03
    )
    clean_no_harm_ok = (
        float(mse_clean["mse_db_to_clean"]) < 1.0
        and float(bce_clean["mse_db_to_clean"]) < 3.0
        and float(mse_clean["measured_pfa"]) < 0.05
        and float(bce_clean["measured_pfa"]) < 0.08
    )
    mask_consistent = (float(bce_medium["weak_pd"]) - float(mse_medium["weak_pd"])) * (
        float(bce_narrow["weak_pd"]) - float(mse_narrow["weak_pd"])
    ) >= 0
    non_overlap_consistent = (float(bce_medium["weak_pd"]) - float(mse_medium["weak_pd"])) * (
        float(bce_non["weak_pd"]) - float(mse_non["weak_pd"])
    ) >= 0
    output_stable = (
        float(mse_metrics["output_std_db"]) > 1e-4
        and float(bce_metrics["output_std_db"]) > 1e-4
        and float(mse_metrics["output_max_db"]) < 150
        and float(bce_metrics["output_max_db"]) < 150
    )
    d3_pass = all(
        [
            mse_train_ok,
            bce_train_ok,
            fixed_ok,
            bce_not_worse,
            clean_no_harm_ok,
            mask_consistent,
            non_overlap_consistent,
            output_stable,
        ]
    )
    next_step = (
        "可以进入 D4，但 D4 只能做 tuned balanced BCE 或 focal loss 强 baseline，不要跳到 weak-target full loss。"
        if d3_pass
        else "不建议进入 D4；应先分析 ordinary BCE 为什么差于 MSE/MAGMSE，优先检查 CFAR BCE loss、mask 和学习率。"
    )

    recon_lookup = {(r["input_type"], str(r.get("sir_name", ""))): r for r in recon_rows}
    summary_rows = [
        {"name": "clean", **clean, **recon_lookup[("clean", "")]},
        {"name": "MSE output medium", **mse_medium, **recon_lookup[("mse_output", "medium")]},
        {"name": "BCE output medium", **bce_medium, **recon_lookup[("ordinary_bce_output", "medium")]},
        {"name": "MSE model(clean)", **mse_clean, **recon_lookup[("mse_model_clean", "")]},
        {"name": "BCE model(clean)", **bce_clean, **recon_lookup[("bce_model_clean", "")]},
    ]

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

    report = f"""# D3 Gao77 Baseline Sanity 报告

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
阶段：D3，仅 range-only baseline sanity  
数据：`G:\\mineru_output\\gao_77ghz_raw_adc\\subset_d1a_v1`

## 1. 执行边界

本次只执行 D3。没有进入 D4-D14，没有做 weak-target full loss、focal loss、balanced BCE、false alarm penalty、clean identity full method 或 3 seeds；没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D3 是否通过 | {'通过' if d3_pass else '未通过'} |
| MSE/MAGMSE baseline 是否训练成功 | {'是' if mse_train_ok else '否'} |
| ordinary differentiable CA-CFAR BCE baseline 是否训练成功 | {'是' if bce_train_ok else '否'} |
| 两者 loss 是否下降 | {'是' if mse_train_ok and bce_train_ok else '否'} |
| 两者输出是否稳定 | {'是' if output_stable else '否'} |
| BCE fixed-PFA 检测指标是否不差于 MSE | {'是' if bce_not_worse else '否'} |
| clean-input no-harm 是否有问题 | {'否' if clean_no_harm_ok else '是'} |
| narrow/default mask 结论是否一致 | {'是' if mask_consistent else '否'} |
| all targets 与 non-overlap-only 是否一致 | {'是' if non_overlap_consistent else '否'} |
| 是否建议进入 D4 | {'是' if d3_pass else '否'} |
| 下一步 | {next_step} |

## 3. 训练 Loss

| baseline | tiny_initial | tiny_final | tiny_drop | train_initial | train_final | train_drop | val_initial | val_final | val_drop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MSE/MAGMSE | {mse_metrics['tiny_initial_loss']:.6f} | {mse_metrics['tiny_final_loss']:.6f} | {mse_metrics['tiny_loss_drop_fraction']:.4f} | {mse_metrics['initial_train_loss']:.6f} | {mse_metrics['final_train_loss']:.6f} | {mse_metrics['train_loss_drop_fraction']:.4f} | {mse_metrics['initial_val_loss']:.6f} | {mse_metrics['final_val_loss']:.6f} | {mse_metrics['val_loss_drop_fraction']:.4f} |
| ordinary BCE | {bce_metrics['tiny_initial_loss']:.6f} | {bce_metrics['tiny_final_loss']:.6f} | {bce_metrics['tiny_loss_drop_fraction']:.4f} | {bce_metrics['initial_train_loss']:.6f} | {bce_metrics['final_train_loss']:.6f} | {bce_metrics['train_loss_drop_fraction']:.4f} | {bce_metrics['initial_val_loss']:.6f} | {bce_metrics['final_val_loss']:.6f} | {bce_metrics['val_loss_drop_fraction']:.4f} |

## 4. Baseline 对比

默认 mask、clean_peak_percentile、PFA=1e-2：

{md_table(summary_rows, ['name', 'mse_db_to_clean', 'measured_pfa', 'false_alarm_count', 'background_cell_count', 'weak_pd', 'mid_pd', 'strong_pd', 'overall_pd', 'f1', 'noise_floor_change_db', 'target_peak_abs_bias_db_mean'])}

## 5. 判断

- D3 的判断对象是 ordinary BCE 是否至少不明显差于 MSE/MAGMSE，而不是 proposed method 是否有效。
- 如果进入 D4，D4 应只做 tuned balanced BCE 或 focal loss 强 baseline；weak-target-weighted loss 必须留到 D5。
- severe interference 仅作为 stress test，不作为 D3 主要训练判断。

## 6. 输出文件

结果目录：

`G:\\mineru_output\\results\\d3_gao77_baseline_sanity`

图像目录：

`G:\\mineru_output\\gao_77ghz_raw_adc\\reports\\d3_figures`

关键文件：

- `d3_config.json`
- `d3_dataset_manifest.csv`
- `d3_model_summary_mse.txt`
- `d3_model_summary_bce.txt`
- `d3_training_loss_mse.csv`
- `d3_training_loss_bce.csv`
- `d3_fixed_pfa_metrics.csv`
- `d3_clean_no_harm_metrics.csv`
- `d3_reconstruction_metrics.csv`
- `d3_metrics_by_mask.csv`
- `d3_metrics_non_overlap_only.csv`
- `d3_metrics_by_sequence.csv`
- `d3_metrics_by_class_group.csv`
- `d3_baseline_comparison_summary.csv`

## 7. D4 建议

{next_step}
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_ts = REPORT_PATH.with_name(f"{REPORT_PATH.stem}_{timestamp}{REPORT_PATH.suffix}")
    report_ts.write_text(report, encoding="utf-8-sig")
    REPORT_PATH.write_text(report, encoding="utf-8-sig")
    return d3_pass, str(report_ts), summary_rows


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

    rng = np.random.default_rng(RANDOM_SEED + 500)
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

    mse_model, mse_loss_rows, mse_metrics = train_mse_baseline(train_x, train_y, val_x, val_y, norm_mean, norm_std, device)
    bce_model, bce_loss_rows, bce_metrics, bce_threshold = train_bce_baseline(
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
    )

    case_arrays = build_case_arrays(
        clean_power,
        clean_db,
        val_frames,
        test_frames,
        eval_val_inter_db,
        eval_test_inter_db,
        mse_model,
        bce_model,
        norm_mean,
        norm_std,
        device,
    )
    metrics = evaluate_cases(manifest, targets, contexts, clean_power, clean_db, val_frames, test_frames, case_arrays)
    recon_rows = reconstruction_metrics(case_arrays, clean_db, clean_power, test_frames)
    plot_outputs(mse_loss_rows, bce_loss_rows, clean_db, test_frames, case_arrays, metrics["fixed"], recon_rows)

    dataset_rows = train_rows + val_rows + eval_val_rows + eval_test_rows
    write_csv(RESULT_DIR / "d3_dataset_manifest.csv", dataset_rows)
    write_csv(RESULT_DIR / "d3_training_loss_mse.csv", mse_loss_rows)
    write_csv(RESULT_DIR / "d3_training_loss_bce.csv", bce_loss_rows)
    write_csv(RESULT_DIR / "d3_fixed_pfa_metrics.csv", metrics["fixed"])
    clean_no_harm = [r for r in metrics["fixed"] if r["input_type"] in {"mse_model_clean", "bce_model_clean"}]
    write_csv(RESULT_DIR / "d3_clean_no_harm_metrics.csv", clean_no_harm)
    write_csv(RESULT_DIR / "d3_reconstruction_metrics.csv", recon_rows)
    write_csv(RESULT_DIR / "d3_metrics_by_mask.csv", metrics["by_mask"])
    write_csv(RESULT_DIR / "d3_metrics_non_overlap_only.csv", metrics["non_overlap"])
    write_csv(RESULT_DIR / "d3_metrics_by_sequence.csv", metrics["by_sequence"])
    write_csv(RESULT_DIR / "d3_metrics_by_class_group.csv", metrics["by_class"])
    write_csv(RESULT_DIR / "d3_mse_training_summary.csv", [mse_metrics])
    write_csv(RESULT_DIR / "d3_bce_training_summary.csv", [bce_metrics])
    write_model_summary(RESULT_DIR / "d3_model_summary_mse.txt", mse_model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    write_model_summary(RESULT_DIR / "d3_model_summary_bce.txt", bce_model, EXPECTED_ADC_SHAPE[0], device, norm_mean, norm_std)
    d3_pass, report_ts, summary_rows = write_report(mse_metrics, bce_metrics, metrics["fixed"], recon_rows)
    write_csv(RESULT_DIR / "d3_baseline_comparison_summary.csv", summary_rows)
    config = {
        "stage": "D3",
        "strict_limits": {
            "only_d3": True,
            "no_d4_d14": True,
            "no_weak_target_full_loss": True,
            "no_focal_loss": True,
            "no_balanced_bce": True,
            "no_false_alarm_penalty": True,
            "no_clean_identity_full_method": True,
            "no_3_seeds": True,
            "no_rdlr_diffirm_rimformer": True,
            "no_large_model": True,
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
        "bce_threshold": bce_threshold,
        "bce_temperature": BCE_TEMPERATURE,
        "normalization": {"mean_db": norm_mean, "std_db": norm_std},
        "valid_pfa_targets": VALID_PFA_TARGETS,
        "mask_names": sorted(ACTIVE_MASK_NAMES),
        "device": str(device),
    }
    write_json(RESULT_DIR / "d3_config.json", config)
    print(
        json.dumps(
            {
                "d3_pass": d3_pass,
                "result_dir": str(RESULT_DIR),
                "figure_dir": str(FIG_DIR),
                "report": str(REPORT_PATH),
                "timestamped_report": report_ts,
                "device": str(device),
                "train_samples": int(train_x.shape[0]),
                "val_samples": int(val_x.shape[0]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
