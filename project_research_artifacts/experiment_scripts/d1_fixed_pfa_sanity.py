import argparse
import csv
import json
import math
import os
import platform
import random
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    import torch
    import torch.nn.functional as F
except Exception as exc:  # pragma: no cover - reported in preflight
    torch = None
    F = None
    TORCH_IMPORT_ERROR = repr(exc)
else:
    TORCH_IMPORT_ERROR = None


@dataclass
class Target:
    frame: int
    y: int
    x: int
    amplitude: float
    strength: str


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=8)
        return out.strip()
    except Exception as exc:
        return f"ERROR: {exc!r}"


def discover_numeric_files(root: Path, max_items=50):
    exts = {".npy", ".npz", ".pt", ".pth", ".mat", ".h5", ".hdf5", ".pkl", ".pickle", ".bin", ".dat"}
    found = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in exts:
            found.append(str(path))
            if len(found) >= max_items:
                break
    return found


def generate_synthetic_rd(n=48, h=64, w=128, seed=7):
    rng = np.random.default_rng(seed)
    clean = rng.normal(0.0, 0.035, size=(n, h, w)).astype(np.float32)
    interfered = clean.copy()
    target_mask = np.zeros((n, h, w), dtype=bool)
    guard_mask = np.zeros((n, h, w), dtype=bool)
    targets = []

    strength_specs = [
        ("weak", (0.22, 0.42)),
        ("mid", (0.55, 0.95)),
        ("strong", (1.20, 2.00)),
    ]

    yy, xx = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    for i in range(n):
        num_targets = int(rng.integers(2, 6))
        for _ in range(num_targets):
            strength, (lo, hi) = strength_specs[int(rng.integers(0, 3))]
            amp = float(rng.uniform(lo, hi))
            y = int(rng.integers(8, h - 8))
            x = int(rng.integers(10, w - 10))
            sigma_y = float(rng.uniform(0.8, 1.5))
            sigma_x = float(rng.uniform(0.8, 1.8))
            blob = amp * np.exp(-(((yy - y) ** 2) / (2 * sigma_y**2) + ((xx - x) ** 2) / (2 * sigma_x**2)))
            clean[i] += blob.astype(np.float32)
            interfered[i] += blob.astype(np.float32)
            y0, y1 = max(0, y - 1), min(h, y + 2)
            x0, x1 = max(0, x - 1), min(w, x + 2)
            target_mask[i, y0:y1, x0:x1] = True
            gy0, gy1 = max(0, y - 4), min(h, y + 5)
            gx0, gx1 = max(0, x - 4), min(w, x + 5)
            guard_mask[i, gy0:gy1, gx0:gx1] = True
            targets.append(Target(i, y, x, amp, strength))

        severity = ["light", "medium", "severe"][i % 3]
        if severity == "light":
            line_amp, noise = 0.12, 0.03
        elif severity == "medium":
            line_amp, noise = 0.28, 0.05
        else:
            line_amp, noise = 0.55, 0.08
        interfered[i] += rng.normal(0.0, noise, size=(h, w)).astype(np.float32)
        for k in range(int(rng.integers(1, 4))):
            slope = float(rng.uniform(-0.55, 0.55))
            offset = float(rng.uniform(0, h))
            width = float(rng.uniform(1.2, 2.8))
            distance = np.abs(yy - (slope * xx + offset)) / math.sqrt(slope * slope + 1.0)
            line = line_amp * np.exp(-(distance**2) / (2 * width**2))
            interfered[i] += line.astype(np.float32)

    background_mask = ~guard_mask
    return clean, interfered.astype(np.float32), target_mask, background_mask, targets


def ca_cfar_score_np(rd, guard=2, train=6, eps=1e-6):
    if torch is None:
        raise RuntimeError("PyTorch is required for CA-CFAR score computation in this script.")
    x = torch.from_numpy(rd).float().unsqueeze(1)
    with torch.no_grad():
        score = ca_cfar_score_torch(x, guard=guard, train=train, eps=eps).squeeze(1).cpu().numpy()
    return score


def ca_cfar_score_torch(x, guard=2, train=6, eps=1e-6):
    # x: [B, 1, H, W], nonnegative magnitude-like RD map.
    power = x.abs()
    k = 2 * (guard + train) + 1
    g = 2 * guard + 1
    outer = torch.ones((1, 1, k, k), dtype=power.dtype, device=power.device)
    inner = torch.ones((1, 1, g, g), dtype=power.dtype, device=power.device)
    outer_sum = F.conv2d(power, outer, padding=k // 2)
    inner_sum = F.conv2d(power, inner, padding=g // 2)
    n_train = float(k * k - g * g)
    noise = (outer_sum - inner_sum).clamp_min(0.0) / max(n_train, 1.0)
    return power / (noise + eps)


def differentiable_cfar_torch(x, threshold=4.0, temperature=0.5, guard=2, train=6):
    score = ca_cfar_score_torch(x, guard=guard, train=train)
    return torch.sigmoid((score - threshold) / temperature)


def calibrate_threshold(scores, background_mask, target_pfa):
    bg = scores[background_mask]
    if bg.size == 0:
        raise ValueError("No background cells available for PFA calibration.")
    q = max(0.0, min(1.0, 1.0 - target_pfa))
    return float(np.quantile(bg, q))


def object_pd(detections, targets, group_selector):
    selected = [t for t in targets if group_selector(t)]
    if not selected:
        return {"num_targets": 0, "pd": None, "miss_rate": None, "hits": 0}
    hits = 0
    h, w = detections.shape[1:]
    for t in selected:
        y0, y1 = max(0, t.y - 1), min(h, t.y + 2)
        x0, x1 = max(0, t.x - 1), min(w, t.x + 2)
        if detections[t.frame, y0:y1, x0:x1].any():
            hits += 1
    pd = hits / len(selected)
    return {"num_targets": len(selected), "pd": pd, "miss_rate": 1.0 - pd, "hits": hits}


def f1_cell(detections, target_mask, background_mask):
    tp = int(np.logical_and(detections, target_mask).sum())
    fp = int(np.logical_and(detections, background_mask).sum())
    fn = int(np.logical_and(~detections, target_mask).sum())
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def evaluate_fixed_pfa(scores_val, scores_test, bg_val, bg_test, target_mask_test, targets_test):
    rows = []
    amp_values = np.array([t.amplitude for t in targets_test], dtype=np.float32)
    p33, p66 = np.quantile(amp_values, [0.33, 0.66])
    for pfa in [1e-2, 1e-3]:
        threshold = calibrate_threshold(scores_val, bg_val, pfa)
        det = scores_test >= threshold
        far = float(np.logical_and(det, bg_test).sum() / max(bg_test.sum(), 1))
        split = {
            "weak": object_pd(det, targets_test, lambda t, p33=p33: t.amplitude <= p33),
            "mid": object_pd(det, targets_test, lambda t, p33=p33, p66=p66: p33 < t.amplitude <= p66),
            "strong": object_pd(det, targets_test, lambda t, p66=p66: t.amplitude > p66),
        }
        f1 = f1_cell(det, target_mask_test, bg_test)
        rows.append(
            {
                "target_pfa": pfa,
                "threshold": threshold,
                "observed_test_far": far,
                "weak_pd": split["weak"]["pd"],
                "weak_miss_rate": split["weak"]["miss_rate"],
                "weak_n": split["weak"]["num_targets"],
                "mid_pd": split["mid"]["pd"],
                "mid_miss_rate": split["mid"]["miss_rate"],
                "mid_n": split["mid"]["num_targets"],
                "strong_pd": split["strong"]["pd"],
                "strong_miss_rate": split["strong"]["miss_rate"],
                "strong_n": split["strong"]["num_targets"],
                "cell_precision": f1["precision"],
                "cell_recall": f1["recall"],
                "cell_f1": f1["f1"],
                "tp_cells": f1["tp"],
                "fp_cells": f1["fp"],
                "fn_cells": f1["fn"],
            }
        )
    return rows


def tensor_memory(shape, dtype=np.float32):
    return int(np.prod(shape) * np.dtype(dtype).itemsize)


def write_markdown(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8-sig")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="G:/mineru_output")
    parser.add_argument("--out", default="results/d1_sanity")
    parser.add_argument("--n", type=int, default=48)
    parser.add_argument("--h", type=int, default=64)
    parser.add_argument("--w", type=int, default=128)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    root = Path(args.root)
    out_dir = root / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    refine_dir = root / "refine-logs"
    refine_dir.mkdir(parents=True, exist_ok=True)

    random.seed(args.seed)
    np.random.seed(args.seed)
    if torch is not None:
        torch.manual_seed(args.seed)

    numeric_files = discover_numeric_files(root)
    nvidia = run_cmd(["nvidia-smi", "--query-gpu=name,memory.total,memory.used,driver_version", "--format=csv,noheader"])

    preflight = {
        "python_executable": sys.executable,
        "python_version": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "torch_available": torch is not None,
        "torch_import_error": TORCH_IMPORT_ERROR,
        "torch_version": getattr(torch, "__version__", None) if torch is not None else None,
        "torch_cuda_available": bool(torch.cuda.is_available()) if torch is not None else False,
        "torch_cuda_version": getattr(torch.version, "cuda", None) if torch is not None else None,
        "cuda_device_count": int(torch.cuda.device_count()) if torch is not None else 0,
        "nvidia_smi": nvidia,
        "numeric_data_files_found": numeric_files[:20],
        "numeric_data_file_count_sampled": len(numeric_files),
    }

    if torch is not None and torch.cuda.is_available():
        devices = []
        for i in range(torch.cuda.device_count()):
            p = torch.cuda.get_device_properties(i)
            devices.append({"index": i, "name": p.name, "total_memory_gb": p.total_memory / 1024**3})
        preflight["cuda_devices"] = devices

    sample_shape = (1, args.h, args.w)
    sample_bytes = tensor_memory(sample_shape)
    batch1_bytes = tensor_memory((1, 1, args.h, args.w))
    batch2_bytes = tensor_memory((2, 1, args.h, args.w))
    preflight["rd_tensor_shape"] = list(sample_shape)
    preflight["rd_tensor_dtype"] = "float32"
    preflight["rd_tensor_bytes_per_sample"] = sample_bytes
    preflight["rd_tensor_mib_per_sample"] = sample_bytes / 1024**2
    preflight["dry_run_batch_size"] = 2
    preflight["dry_run_tensor_mib_input_only"] = batch2_bytes / 1024**2
    preflight["conservative_config"] = {
        "batch_size": 1 if not preflight["torch_cuda_available"] else 2,
        "num_workers": 0,
        "mixed_precision": False,
        "large_sweeps": False,
    }

    dry_run = {"status": "not_run"}
    if torch is not None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        try:
            x = torch.rand((2, 1, args.h, args.w), dtype=torch.float32, device=device, requires_grad=True)
            y = differentiable_cfar_torch(x, threshold=4.0, temperature=0.7)
            loss = y.mean()
            loss.backward()
            grad_ok = x.grad is not None and torch.isfinite(x.grad).all().item()
            dry_run = {
                "status": "ok",
                "device": device,
                "input_shape": list(x.shape),
                "output_shape": list(y.shape),
                "loss": float(loss.detach().cpu()),
                "grad_finite": bool(grad_ok),
            }
            if device == "cuda":
                dry_run["cuda_memory_allocated_mib"] = torch.cuda.memory_allocated() / 1024**2
                dry_run["cuda_memory_reserved_mib"] = torch.cuda.memory_reserved() / 1024**2
        except Exception as exc:
            dry_run = {"status": "failed", "error": repr(exc)}
    preflight["dry_run"] = dry_run

    clean, interfered, target_mask, background_mask, targets = generate_synthetic_rd(args.n, args.h, args.w, args.seed)
    split = args.n // 2
    scores_val = ca_cfar_score_np(np.abs(interfered[:split]))
    scores_test = ca_cfar_score_np(np.abs(interfered[split:]))
    bg_val = background_mask[:split]
    bg_test = background_mask[split:]
    target_mask_test = target_mask[split:]
    targets_test = [
        Target(t.frame - split, t.y, t.x, t.amplitude, t.strength)
        for t in targets
        if t.frame >= split
    ]

    metrics = evaluate_fixed_pfa(scores_val, scores_test, bg_val, bg_test, target_mask_test, targets_test)
    strength_counts = {}
    for t in targets:
        strength_counts[t.strength] = strength_counts.get(t.strength, 0) + 1

    d1 = {
        "data_source": "synthetic_toy_rd",
        "real_numeric_radar_data_found": bool(numeric_files),
        "note": "No local numeric radar tensor dataset was found under G:/mineru_output; D1 validates the metric pipeline on synthetic RD maps.",
        "shape_clean": list(clean.shape),
        "shape_interfered": list(interfered.shape),
        "dtype": str(interfered.dtype),
        "num_targets_total": len(targets),
        "target_strength_counts_generator": strength_counts,
        "target_mask_cells": int(target_mask.sum()),
        "background_mask_cells": int(background_mask.sum()),
        "fixed_pfa_metrics_no_mitigation": metrics,
    }

    with (out_dir / "preflight.json").open("w", encoding="utf-8") as f:
        json.dump(preflight, f, indent=2, ensure_ascii=False)
    with (out_dir / "d1_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(d1, f, indent=2, ensure_ascii=False)
    with (out_dir / "d1_metrics.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics[0].keys()))
        writer.writeheader()
        writer.writerows(metrics)

    preflight_md = [
        "# HARDWARE_PREFLIGHT_REPORT",
        "",
        f"**Python**：`{preflight['python_executable']}`",
        f"**Python version**：{platform.python_version()}",
        f"**PyTorch available**：{preflight['torch_available']}",
        f"**PyTorch version**：{preflight['torch_version']}",
        f"**CUDA available in PyTorch**：{preflight['torch_cuda_available']}",
        f"**PyTorch CUDA version**：{preflight['torch_cuda_version']}",
        f"**nvidia-smi**：`{nvidia}`",
        "",
        "## 数据发现",
        "",
        f"- 本地数值雷达数据文件采样数量：{len(numeric_files)}",
        "- 结论：未在 `G:/mineru_output` 下发现 `.npy/.npz/.mat/.h5/.pt` 等雷达 tensor 数据；D1 使用合成 toy RD 数据验证指标链路。",
        "",
        "## 样本规模估算",
        "",
        f"- RD tensor shape：`{sample_shape}`",
        "- dtype：`float32`",
        f"- 单条 RD tensor 输入占用：{sample_bytes / 1024**2:.4f} MiB",
        f"- dry-run batch=2 输入占用：{batch2_bytes / 1024**2:.4f} MiB，仅为输入张量，不含中间激活。",
        "",
        "## Dry-Run",
        "",
        f"- conservative batch size：{preflight['conservative_config']['batch_size']}",
        f"- num_workers：{preflight['conservative_config']['num_workers']}",
        f"- mixed precision：{preflight['conservative_config']['mixed_precision']}",
        f"- dry-run status：{dry_run['status']}",
        f"- dry-run detail：`{json.dumps(dry_run, ensure_ascii=False)}`",
        "",
        "## 预判",
        "",
        "- D1：本地机器足够完成。",
        "- D2：simple FCN/AENN 小 batch overfit 可以本地先跑；建议 batch size 从 1 或 2 开始。",
        "- 后续 3 seeds、大 batch、长时间训练：GTX 1650 4GB 会非常吃紧，建议届时再租云 GPU。",
    ]
    write_markdown(refine_dir / "HARDWARE_PREFLIGHT_REPORT.md", "\n".join(preflight_md) + "\n")

    rows_md = []
    for row in metrics:
        rows_md.append(
            "| {target_pfa:g} | {threshold:.4f} | {observed_test_far:.5f} | {weak_n} | {weak_pd:.4f} | {weak_miss_rate:.4f} | {mid_n} | {mid_pd:.4f} | {strong_n} | {strong_pd:.4f} | {cell_f1:.4f} |".format(**row)
        )

    d1_md = [
        "# D1_FIXED_PFA_SANITY_REPORT",
        "",
        "**状态**：D1 sanity 已完成；未进入 D2。",
        "",
        "## 数据来源",
        "",
        "- 当前未发现本地真实数值雷达 tensor 数据。",
        "- 本报告使用合成 toy RD 数据验证 D1 指标链路。",
        "- 这不是方法效果结论，不能作为论文实验结果。",
        "",
        "## 已打通模块",
        "",
        "- 数据读取/生成：完成，synthetic RD maps。",
        "- hard CA-CFAR score：完成。",
        "- differentiable CA-CFAR：完成，dry-run 可反传。",
        "- target mask / background mask：完成。",
        "- weak / mid / strong target split：完成，当前按 target peak amplitude percentile。",
        "- cell-level PFA：完成。",
        "- fixed-PFA threshold calibration：完成，validation set 标定，test set 报告。",
        "",
        "## Tensor 与 Mask",
        "",
        f"- clean shape：`{tuple(clean.shape)}`",
        f"- interfered shape：`{tuple(interfered.shape)}`",
        f"- dtype：`{interfered.dtype}`",
        f"- targets total：{len(targets)}",
        f"- generator strength counts：`{strength_counts}`",
        f"- target mask cells：{int(target_mask.sum())}",
        f"- background mask cells：{int(background_mask.sum())}",
        "",
        "## Fixed-PFA No-Mitigation Metrics",
        "",
        "| target PFA | threshold | test FAR | weak n | weak Pd | weak miss | mid n | mid Pd | strong n | strong Pd | cell F1 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        *rows_md,
        "",
        "## 输出文件",
        "",
        "- `results/d1_sanity/preflight.json`",
        "- `results/d1_sanity/d1_metrics.json`",
        "- `results/d1_sanity/d1_metrics.csv`",
        "",
        "## D1 结论",
        "",
        "- D1 指标链路可以在本地完成。",
        "- 下一步若继续 D2，建议使用 `G:/Anaconda/envs/cnn_learn/python.exe`，batch size 从 1 或 2 开始。",
        "- 真实数据接入仍是后续瓶颈；当前只是 sanity，不代表真实雷达数据表现。",
    ]
    write_markdown(refine_dir / "D1_FIXED_PFA_SANITY_REPORT.md", "\n".join(d1_md) + "\n")

    print(json.dumps({"preflight": preflight, "d1": d1}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
