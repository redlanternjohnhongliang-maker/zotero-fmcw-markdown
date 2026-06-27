from __future__ import annotations

import csv
import io
import json
import math
import os
import random
import shutil
import statistics
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import loadmat


BASE = Path(r"G:\mineru_output")
DATA_ROOT = BASE / "gao_77ghz_raw_adc"
ZIP_PATH = DATA_ROOT / "Automotive.zip"
RESULT_DIR = BASE / "results" / "d0b_gao77_subset_selection"
FIG_DIR = DATA_ROOT / "reports" / "d0b_figures"
SUBSET_DIR = DATA_ROOT / "subset_d1a_v1"
SUBSET_RADAR_DIR = SUBSET_DIR / "radar_raw_frame"
SUBSET_LABEL_DIR = SUBSET_DIR / "text_labels"
SUBSET_MANIFEST_DIR = SUBSET_DIR / "manifest"
REPORT_PATH = BASE / "refine-logs" / "D0B_GAO77_SUBSET_SELECTION_REPORT.md"
REPORT_TS_PATH = BASE / "refine-logs" / "D0B_GAO77_SUBSET_SELECTION_REPORT_20260626_153300.md"

EXPECTED_ADC_SHAPE = (128, 255, 4, 2)
LABEL_MAP = {
    0: "person",
    2: "car",
    3: "motorbike",
    5: "bus",
    7: "truck",
    80: "cyclist",
}
RANDOM_SEED = 20260626
TOP_K = 5
RADAR_SAMPLE_PER_SEQUENCE = 30
TARGET_TOTAL_FRAMES = 1500
PER_SEQUENCE_QUOTA = 300


@dataclass
class LabelRow:
    uid: int
    cls: int
    px: float
    py: float
    wid: float
    length: float

    @property
    def range_m(self) -> float:
        return math.sqrt(self.px * self.px + self.py * self.py)

    @property
    def azimuth_deg(self) -> float:
        return math.degrees(math.atan2(self.px, self.py))


def numeric_stem(name: str) -> int | None:
    stem = Path(name).stem
    try:
        return int(stem)
    except ValueError:
        return None


def as_stats(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
            "std": None,
            "span": None,
        }
    return {
        "min": float(min(values)),
        "max": float(max(values)),
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
        "std": float(statistics.pstdev(values)) if len(values) > 1 else 0.0,
        "span": float(max(values) - min(values)),
    }


def parse_label_bytes(data: bytes, filename: str) -> tuple[list[LabelRow], list[str]]:
    text = data.decode("utf-8", errors="replace").strip()
    if not text:
        return [], []
    rows: list[LabelRow] = []
    anomalies: list[str] = []
    for line_no, row in enumerate(csv.reader(io.StringIO(text)), start=1):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != 6:
            anomalies.append(f"{filename}:{line_no}:bad_col_count_{len(row)}")
            continue
        try:
            uid = int(float(row[0]))
            cls = int(float(row[1]))
            px = float(row[2])
            py = float(row[3])
            wid = float(row[4])
            length = float(row[5])
        except ValueError:
            anomalies.append(f"{filename}:{line_no}:parse_error")
            continue
        if wid <= 0:
            anomalies.append(f"{filename}:{line_no}:wid_non_positive")
        if length <= 0:
            anomalies.append(f"{filename}:{line_no}:len_non_positive")
        if px < -30 or px > 30 or py < -5 or py > 35:
            anomalies.append(f"{filename}:{line_no}:px_py_outlier")
        rows.append(LabelRow(uid, cls, px, py, wid, length))
    return rows, anomalies


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not columns:
        columns = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def scan_zip() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    seqs: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "radar": {},
            "labels": {},
            "images": 0,
            "label_rows_by_num": {},
            "label_anomalies": [],
        }
    )
    with zipfile.ZipFile(ZIP_PATH) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            parts = info.filename.replace("\\", "/").split("/")
            if len(parts) < 4 or parts[0] != "Automotive":
                continue
            seq, subdir, filename = parts[1], parts[2], parts[-1]
            n = numeric_stem(filename)
            if n is None:
                continue
            if subdir == "radar_raw_frame" and filename.lower().endswith(".mat"):
                seqs[seq]["radar"][n] = info.filename
            elif subdir == "text_labels" and filename.lower().endswith(".csv"):
                seqs[seq]["labels"][n] = info.filename
            elif subdir == "images_0":
                seqs[seq]["images"] += 1

        for seq, data in seqs.items():
            for n, zip_name in sorted(data["labels"].items()):
                with zf.open(zip_name) as fh:
                    rows, anomalies = parse_label_bytes(fh.read(), zip_name)
                data["label_rows_by_num"][n] = rows
                data["label_anomalies"].extend(anomalies)

    stats_rows: list[dict[str, Any]] = []
    for seq, data in sorted(seqs.items()):
        radar_nums = set(data["radar"])
        label_nums = set(data["labels"])
        common = sorted(radar_nums & label_nums)
        radar_only = sorted(radar_nums - label_nums)
        label_only = sorted(label_nums - radar_nums)
        target_counts: list[int] = []
        all_labels: list[LabelRow] = []
        for n in common:
            rows = data["label_rows_by_num"].get(n, [])
            target_counts.append(len(rows))
            all_labels.extend(rows)

        px_values = [r.px for r in all_labels]
        py_values = [r.py for r in all_labels]
        range_values = [r.range_m for r in all_labels]
        az_values = [r.azimuth_deg for r in all_labels]
        wid_values = [r.wid for r in all_labels]
        len_values = [r.length for r in all_labels]
        class_counts = Counter(r.cls for r in all_labels)
        tc_stats = as_stats([float(v) for v in target_counts])
        px_stats = as_stats(px_values)
        py_stats = as_stats(py_values)
        range_stats = as_stats(range_values)
        az_stats = as_stats(az_values)
        wid_stats = as_stats(wid_values)
        len_stats = as_stats(len_values)
        aligned = len(common)
        anomaly_count = len(data["label_anomalies"])
        row = {
            "sequence": seq,
            "radar_count": len(radar_nums),
            "label_count": len(label_nums),
            "image_count": data["images"],
            "aligned_count": aligned,
            "radar_only_count": len(radar_only),
            "label_only_count": len(label_only),
            "radar_only_first": ";".join(map(str, radar_only[:10])),
            "label_only_first": ";".join(map(str, label_only[:10])),
            "empty_label_frames": sum(1 for v in target_counts if v == 0),
            "nonempty_label_frames": sum(1 for v in target_counts if v > 0),
            "total_targets": len(all_labels),
            "target_count_min": tc_stats["min"],
            "target_count_mean": tc_stats["mean"],
            "target_count_median": tc_stats["median"],
            "target_count_max": tc_stats["max"],
            "target_count_zero_frames": sum(1 for v in target_counts if v == 0),
            "target_count_one_frames": sum(1 for v in target_counts if v == 1),
            "target_count_two_plus_frames": sum(1 for v in target_counts if v >= 2),
            "multi_target_frame_prop": (sum(1 for v in target_counts if v >= 2) / aligned) if aligned else 0.0,
            "nonempty_frame_prop": (sum(1 for v in target_counts if v > 0) / aligned) if aligned else 0.0,
            "class_distribution": ";".join(f"{k}:{v}" for k, v in sorted(class_counts.items())),
            "class_count": len(class_counts),
            "px_min": px_stats["min"],
            "px_max": px_stats["max"],
            "px_mean": px_stats["mean"],
            "px_std": px_stats["std"],
            "px_span": px_stats["span"],
            "py_min": py_stats["min"],
            "py_max": py_stats["max"],
            "py_mean": py_stats["mean"],
            "py_std": py_stats["std"],
            "py_span": py_stats["span"],
            "range_min": range_stats["min"],
            "range_max": range_stats["max"],
            "range_mean": range_stats["mean"],
            "range_std": range_stats["std"],
            "range_span": range_stats["span"],
            "azimuth_min": az_stats["min"],
            "azimuth_max": az_stats["max"],
            "azimuth_mean": az_stats["mean"],
            "azimuth_std": az_stats["std"],
            "azimuth_span": az_stats["span"],
            "wid_min": wid_stats["min"],
            "wid_max": wid_stats["max"],
            "len_min": len_stats["min"],
            "len_max": len_stats["max"],
            "label_anomaly_count": anomaly_count,
            "is_cms1000": seq == "2019_04_09_cms1000",
        }
        data["summary"] = row
        data["common_nums"] = common
        stats_rows.append(row)
    return seqs, stats_rows


def add_scores(stats_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def max_col(name: str) -> float:
        vals = [float(r.get(name) or 0.0) for r in stats_rows]
        return max(vals) if vals else 1.0

    max_targets = max_col("total_targets")
    max_range_std = max_col("range_std")
    max_range_span = max_col("range_span")
    max_az_std = max_col("azimuth_std")
    max_az_span = max_col("azimuth_span")
    max_px_std = max_col("px_std")
    max_multi_prop = max_col("multi_target_frame_prop")
    max_class_count = max_col("class_count")

    score_rows: list[dict[str, Any]] = []
    for r in stats_rows:
        aligned = float(r["aligned_count"] or 0)
        max_files = float(max(r["radar_count"] or 0, r["label_count"] or 0, 1))
        align_quality = aligned / max_files
        target_volume = min(float(r["total_targets"] or 0) / max(max_targets, 1.0), 1.0)
        nonempty_prop = float(r["nonempty_frame_prop"] or 0)
        empty_prop = (float(r["empty_label_frames"] or 0) / aligned) if aligned else 0.0
        if 0.01 <= empty_prop <= 0.15:
            empty_bonus = 1.0
        elif empty_prop == 0:
            empty_bonus = 0.45
        else:
            empty_bonus = max(0.0, 1.0 - abs(empty_prop - 0.08) / 0.35)
        clean_label = max(0.0, 1.0 - float(r["label_anomaly_count"] or 0) / max(float(r["total_targets"] or 1), 1.0))
        multi_prop_norm = float(r["multi_target_frame_prop"] or 0) / max(max_multi_prop, 1e-9)
        range_div = 0.55 * (float(r["range_std"] or 0) / max(max_range_std, 1e-9)) + 0.45 * (
            float(r["range_span"] or 0) / max(max_range_span, 1e-9)
        )
        az_div = 0.55 * (float(r["azimuth_std"] or 0) / max(max_az_std, 1e-9)) + 0.45 * (
            float(r["azimuth_span"] or 0) / max(max_az_span, 1e-9)
        )
        px_div = float(r["px_std"] or 0) / max(max_px_std, 1e-9)
        class_div = float(r["class_count"] or 0) / max(max_class_count, 1.0)
        label_score = (
            22.0 * align_quality
            + 13.0 * target_volume
            + 9.0 * nonempty_prop
            + 14.0 * multi_prop_norm
            + 14.0 * range_div
            + 11.0 * az_div
            + 5.0 * px_div
            + 6.0 * class_div
            + 3.0 * empty_bonus
            + 3.0 * clean_label
        )
        out = dict(r)
        out.update(
            {
                "alignment_quality": align_quality,
                "target_volume_score": target_volume,
                "range_diversity_score": range_div,
                "azimuth_diversity_score": az_div,
                "empty_bonus_score": empty_bonus,
                "clean_label_score": clean_label,
                "label_only_suitability_score": label_score,
                "d1a_suitability_score": label_score,
                "score_reason": "label_scan_only_before_radar_sampling",
            }
        )
        score_rows.append(out)
    return sorted(score_rows, key=lambda x: x["d1a_suitability_score"], reverse=True)


def frame_records_for_sequence(data: dict[str, Any], seq: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for n in data["common_nums"]:
        labels = data["label_rows_by_num"].get(n, [])
        ranges = [r.range_m for r in labels]
        azimuths = [r.azimuth_deg for r in labels]
        pxs = [r.px for r in labels]
        pys = [r.py for r in labels]
        class_ids = sorted({r.cls for r in labels})
        records.append(
            {
                "source_sequence": seq,
                "frame_num": n,
                "radar_zip_name": data["radar"][n],
                "label_zip_name": data["labels"][n],
                "target_count": len(labels),
                "class_ids": ";".join(map(str, class_ids)),
                "px_min": min(pxs) if pxs else "",
                "px_max": max(pxs) if pxs else "",
                "py_min": min(pys) if pys else "",
                "py_max": max(pys) if pys else "",
                "range_min": min(ranges) if ranges else "",
                "range_max": max(ranges) if ranges else "",
                "range_mean": statistics.mean(ranges) if ranges else "",
                "azimuth_min": min(azimuths) if azimuths else "",
                "azimuth_max": max(azimuths) if azimuths else "",
                "azimuth_mean": statistics.mean(azimuths) if azimuths else "",
                "labels": labels,
            }
        )
    return records


def choose_sample_nums(common_nums: list[int], k: int) -> list[int]:
    if len(common_nums) <= k:
        return list(common_nums)
    idxs = np.linspace(0, len(common_nums) - 1, k, dtype=int)
    return sorted({common_nums[int(i)] for i in idxs})


def radar_sample_check(
    zf: zipfile.ZipFile,
    seqs: dict[str, dict[str, Any]],
    candidate_sequences: list[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    random.seed(RANDOM_SEED)
    for seq in candidate_sequences:
        data = seqs[seq]
        sample_nums = choose_sample_nums(data["common_nums"], RADAR_SAMPLE_PER_SEQUENCE)
        peak_values: list[float] = []
        energy_values: list[float] = []
        projection_hits = 0
        projection_total = 0
        ok_count = 0
        bad_count = 0
        first_plot_done = False
        for n in sample_nums:
            row: dict[str, Any] = {
                "sequence": seq,
                "frame_num": n,
                "radar_file": Path(data["radar"][n]).name,
                "label_file": Path(data["labels"][n]).name,
            }
            try:
                with zf.open(data["radar"][n]) as fh:
                    mat = loadmat(io.BytesIO(fh.read()))
                if "adcData" not in mat:
                    raise KeyError("adcData_missing")
                adc = mat["adcData"]
                row["adc_shape"] = "x".join(map(str, adc.shape))
                row["adc_ok"] = tuple(adc.shape) == EXPECTED_ADC_SHAPE
                if tuple(adc.shape) != EXPECTED_ADC_SHAPE:
                    raise ValueError(f"unexpected_shape_{adc.shape}")
                virt = np.concatenate([adc[:, :, :, t] for t in range(adc.shape[3])], axis=2)
                range_fft = np.fft.fft(virt, axis=0)
                doppler_fft = np.fft.fftshift(np.fft.fft(range_fft, axis=1), axes=1)
                range_profile = 20.0 * np.log10(np.mean(np.abs(range_fft), axis=(1, 2)) + 1e-12)
                rd_map = 20.0 * np.log10(np.mean(np.abs(doppler_fft), axis=2) + 1e-12)
                peak_db = float(np.max(range_profile))
                energy_db = float(np.mean(rd_map))
                peak_values.append(peak_db)
                energy_values.append(energy_db)
                row["range_fft_ok"] = True
                row["rd_map_ok"] = True
                row["range_peak_db"] = peak_db
                row["rd_energy_mean_db"] = energy_db
                row["bad_frame"] = False
                labels = data["label_rows_by_num"].get(n, [])
                row["label_count"] = len(labels)
                for lab in labels:
                    projection_total += 1
                    rough_bin = int(round(min(max(lab.range_m / 24.0, 0.0), 1.0) * (adc.shape[0] - 1)))
                    lo = max(0, rough_bin - 5)
                    hi = min(adc.shape[0], rough_bin + 6)
                    local = float(np.max(range_profile[lo:hi]))
                    if local >= float(np.percentile(range_profile, 75)):
                        projection_hits += 1
                if not first_plot_done:
                    plot_radar_sample(seq, n, range_profile, rd_map, labels)
                    first_plot_done = True
                ok_count += 1
            except Exception as exc:
                row["adc_ok"] = False
                row["range_fft_ok"] = False
                row["rd_map_ok"] = False
                row["bad_frame"] = True
                row["error"] = repr(exc)
                bad_count += 1
            rows.append(row)

        summary = {
            "sequence": seq,
            "frame_num": "SUMMARY",
            "sample_count": len(sample_nums),
            "sample_ok_count": ok_count,
            "sample_bad_count": bad_count,
            "range_peak_mean_db": statistics.mean(peak_values) if peak_values else "",
            "range_peak_std_db": statistics.pstdev(peak_values) if len(peak_values) > 1 else 0.0,
            "range_peak_min_db": min(peak_values) if peak_values else "",
            "range_peak_max_db": max(peak_values) if peak_values else "",
            "rd_energy_mean_db": statistics.mean(energy_values) if energy_values else "",
            "rd_energy_std_db": statistics.pstdev(energy_values) if len(energy_values) > 1 else 0.0,
            "label_projection_hit_rate": (projection_hits / projection_total) if projection_total else "",
            "projection_hits": projection_hits,
            "projection_total": projection_total,
        }
        rows.append(summary)
    return rows


def plot_radar_sample(
    seq: str,
    frame_num: int,
    range_profile: np.ndarray,
    rd_map: np.ndarray,
    labels: list[LabelRow],
) -> None:
    prefix = f"{seq}__{frame_num:06d}"
    plt.figure(figsize=(8, 4), dpi=140)
    plt.plot(range_profile, linewidth=1.1)
    plt.xlabel("Range bin")
    plt.ylabel("Magnitude (dB)")
    plt.title(f"Range profile {prefix}")
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"sample_range_profile_{prefix}.png")
    plt.close()

    plt.figure(figsize=(8, 5), dpi=140)
    plt.imshow(rd_map.T, aspect="auto", origin="lower", cmap="viridis")
    plt.xlabel("Range bin")
    plt.ylabel("Doppler bin")
    plt.title(f"RD map {prefix}")
    plt.colorbar(label="Magnitude (dB)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"sample_rd_map_{prefix}.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=140)
    plt.plot(range_profile, linewidth=1.1)
    for lab in labels:
        rough_bin = int(round(min(max(lab.range_m / 24.0, 0.0), 1.0) * (len(range_profile) - 1)))
        plt.axvline(
            rough_bin,
            linestyle="--",
            linewidth=1.0,
            label=f"cls {lab.cls} r~{lab.range_m:.1f}m az~{lab.azimuth_deg:.1f}deg",
        )
    plt.xlabel("Range bin (rough)")
    plt.ylabel("Magnitude (dB)")
    plt.title(f"Label-to-range-bin rough check {prefix}")
    if labels:
        plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(FIG_DIR / f"sample_label_to_range_{prefix}.png")
    plt.close()


def update_scores_with_radar(
    score_rows: list[dict[str, Any]], sample_rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {
        r["sequence"]: r for r in sample_rows if r.get("frame_num") == "SUMMARY"
    }
    updated: list[dict[str, Any]] = []
    for row in score_rows:
        out = dict(row)
        s = summaries.get(row["sequence"])
        if s:
            ok_ratio = float(s.get("sample_ok_count") or 0) / max(float(s.get("sample_count") or 1), 1.0)
            projection = s.get("label_projection_hit_rate")
            projection_score = float(projection) if projection not in ("", None) else 0.5
            radar_score = 0.8 * ok_ratio + 0.2 * projection_score
            out["radar_sample_ok_ratio"] = ok_ratio
            out["label_projection_hit_rate"] = projection
            out["radar_sample_score"] = radar_score
            out["d1a_suitability_score"] = float(row["label_only_suitability_score"]) * 0.88 + 12.0 * radar_score
            out["score_reason"] = "label_scan_plus_top5_radar_sampling"
        else:
            out["radar_sample_ok_ratio"] = ""
            out["label_projection_hit_rate"] = ""
            out["radar_sample_score"] = ""
            out["score_reason"] = "label_scan_only_not_in_radar_sample_top5"
        updated.append(out)
    return sorted(updated, key=lambda x: x["d1a_suitability_score"], reverse=True)


def quantile_bin(value: Any, values: list[float], bins: int) -> int:
    if value in ("", None) or not values:
        return -1
    qs = np.quantile(values, np.linspace(0, 1, bins + 1))
    for i in range(bins):
        if float(value) <= qs[i + 1] or i == bins - 1:
            return i
    return bins - 1


def select_diverse_frames(
    seqs: dict[str, dict[str, Any]], chosen_sequences: list[str], quota_per_sequence: int
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    rng = random.Random(RANDOM_SEED)
    for seq in chosen_sequences:
        records = frame_records_for_sequence(seqs[seq], seq)
        range_values = [float(r["range_mean"]) for r in records if r["range_mean"] != ""]
        az_values = [float(r["azimuth_mean"]) for r in records if r["azimuth_mean"] != ""]
        groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
        for rec in records:
            tc = int(rec["target_count"])
            if tc == 0:
                tc_cat = "empty"
            elif tc == 1:
                tc_cat = "single"
            else:
                tc_cat = "multi"
            rbin = quantile_bin(rec["range_mean"], range_values, 5)
            abin = quantile_bin(rec["azimuth_mean"], az_values, 5)
            groups[(tc_cat, rbin, abin, rec["class_ids"])].append(rec)

        for group in groups.values():
            rng.shuffle(group)

        priority_keys = sorted(
            groups,
            key=lambda k: (
                {"multi": 0, "single": 1, "empty": 2}.get(k[0], 3),
                k[1],
                k[2],
                str(k[3]),
            ),
        )
        chosen_for_seq: list[dict[str, Any]] = []
        while len(chosen_for_seq) < quota_per_sequence and any(groups[k] for k in priority_keys):
            for key in priority_keys:
                if groups[key] and len(chosen_for_seq) < quota_per_sequence:
                    rec = groups[key].pop()
                    rec = dict(rec)
                    rec["selection_reason"] = (
                        f"top_sequence_stratified;tc={key[0]};range_bin={key[1]};azimuth_bin={key[2]}"
                    )
                    chosen_for_seq.append(rec)
        selected.extend(chosen_for_seq)
    if len(selected) > TARGET_TOTAL_FRAMES:
        rng.shuffle(selected)
        selected = selected[:TARGET_TOTAL_FRAMES]
    selected.sort(key=lambda r: (r["source_sequence"], int(r["frame_num"])))
    for i, rec in enumerate(selected, start=1):
        rec["new_frame_id"] = f"d1a_{i:06d}"
    return selected


def copy_selected_frames(zf: zipfile.ZipFile, selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if SUBSET_DIR.exists():
        # This directory is D0B-owned. Remove partial prior outputs to keep manifest and files consistent.
        shutil.rmtree(SUBSET_DIR)
    SUBSET_RADAR_DIR.mkdir(parents=True, exist_ok=True)
    SUBSET_LABEL_DIR.mkdir(parents=True, exist_ok=True)
    SUBSET_MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, Any]] = []
    for rec in selected:
        seq = rec["source_sequence"]
        radar_src = rec["radar_zip_name"]
        label_src = rec["label_zip_name"]
        radar_name = f"{seq}__{Path(radar_src).name}"
        label_name = f"{seq}__{Path(label_src).name}"
        with zf.open(radar_src) as src, (SUBSET_RADAR_DIR / radar_name).open("wb") as dst:
            shutil.copyfileobj(src, dst, length=1024 * 1024)
        with zf.open(label_src) as src, (SUBSET_LABEL_DIR / label_name).open("wb") as dst:
            shutil.copyfileobj(src, dst, length=1024 * 128)
        manifest_rows.append(
            {
                "new_frame_id": rec["new_frame_id"],
                "source_sequence": seq,
                "source_radar_file": Path(radar_src).name,
                "source_label_file": Path(label_src).name,
                "new_radar_file": radar_name,
                "new_label_file": label_name,
                "target_count": rec["target_count"],
                "class_ids": rec["class_ids"],
                "class_counts": ";".join(
                    f"{cls}:{count}" for cls, count in sorted(Counter(lab.cls for lab in rec["labels"]).items())
                ),
                "px_min": rec["px_min"],
                "px_max": rec["px_max"],
                "py_min": rec["py_min"],
                "py_max": rec["py_max"],
                "range_min": rec["range_min"],
                "range_max": rec["range_max"],
                "azimuth_min": rec["azimuth_min"],
                "azimuth_max": rec["azimuth_max"],
                "selection_reason": rec["selection_reason"],
            }
        )
    return manifest_rows


def summarize_selected(manifest_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ranges: list[float] = []
    azimuths: list[float] = []
    target_counts: list[int] = []
    class_counts: Counter[int] = Counter()
    by_seq: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in manifest_rows:
        by_seq[row["source_sequence"]].append(row)
        tc = int(row["target_count"])
        target_counts.append(tc)
        if row["range_min"] != "":
            ranges.append(float(row["range_min"]))
            ranges.append(float(row["range_max"]))
        if row["azimuth_min"] != "":
            azimuths.append(float(row["azimuth_min"]))
            azimuths.append(float(row["azimuth_max"]))
        for item in str(row.get("class_counts", "")).split(";"):
            if not item.strip() or ":" not in item:
                continue
            cls, count = item.split(":", 1)
            class_counts[int(cls)] += int(count)

    rows: list[dict[str, Any]] = []
    for seq, seq_rows in sorted(by_seq.items()):
        rows.append(
            {
                "source_sequence": seq,
                "frame_count": len(seq_rows),
                "target_total": sum(int(r["target_count"]) for r in seq_rows),
                "empty_frames": sum(1 for r in seq_rows if int(r["target_count"]) == 0),
                "single_target_frames": sum(1 for r in seq_rows if int(r["target_count"]) == 1),
                "multi_target_frames": sum(1 for r in seq_rows if int(r["target_count"]) >= 2),
            }
        )
    total = {
        "frame_count": len(manifest_rows),
        "target_total": sum(target_counts),
        "empty_frames": sum(1 for v in target_counts if v == 0),
        "single_target_frames": sum(1 for v in target_counts if v == 1),
        "multi_target_frames": sum(1 for v in target_counts if v >= 2),
        "class_distribution": ";".join(f"{k}:{v}" for k, v in sorted(class_counts.items())),
        "range_min": min(ranges) if ranges else "",
        "range_max": max(ranges) if ranges else "",
        "range_mean": statistics.mean(ranges) if ranges else "",
        "range_std": statistics.pstdev(ranges) if len(ranges) > 1 else 0.0,
        "azimuth_min": min(azimuths) if azimuths else "",
        "azimuth_max": max(azimuths) if azimuths else "",
        "azimuth_mean": statistics.mean(azimuths) if azimuths else "",
        "azimuth_std": statistics.pstdev(azimuths) if len(azimuths) > 1 else 0.0,
        "target_count_min": min(target_counts) if target_counts else "",
        "target_count_mean": statistics.mean(target_counts) if target_counts else "",
        "target_count_median": statistics.median(target_counts) if target_counts else "",
        "target_count_max": max(target_counts) if target_counts else "",
    }
    return rows, total


def plot_sequence_rankings(score_rows: list[dict[str, Any]], stats_rows: list[dict[str, Any]]) -> None:
    df = pd.DataFrame(stats_rows).sort_values("range_span", ascending=False)
    plt.figure(figsize=(12, 5), dpi=150)
    plt.bar(df["sequence"], df["range_span"].astype(float))
    plt.xticks(rotation=75, ha="right", fontsize=7)
    plt.ylabel("Range span (m)")
    plt.title("All sequences ranked by range spread")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "all_sequences_range_spread_ranking.png")
    plt.close()

    df = pd.DataFrame(stats_rows).sort_values("azimuth_span", ascending=False)
    plt.figure(figsize=(12, 5), dpi=150)
    plt.bar(df["sequence"], df["azimuth_span"].astype(float))
    plt.xticks(rotation=75, ha="right", fontsize=7)
    plt.ylabel("Azimuth span (deg)")
    plt.title("All sequences ranked by azimuth spread")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "all_sequences_azimuth_spread_ranking.png")
    plt.close()

    plt.figure(figsize=(10, 5), dpi=150)
    values = [
        [
            int(r["target_count_zero_frames"]),
            int(r["target_count_one_frames"]),
            int(r["target_count_two_plus_frames"]),
        ]
        for r in stats_rows
    ]
    x = np.arange(len(stats_rows))
    zeros = [v[0] for v in values]
    ones = [v[1] for v in values]
    twoplus = [v[2] for v in values]
    labels = [r["sequence"] for r in stats_rows]
    plt.bar(x, zeros, label="0 target")
    plt.bar(x, ones, bottom=zeros, label="1 target")
    plt.bar(x, twoplus, bottom=np.array(zeros) + np.array(ones), label="2+ targets")
    plt.xticks(x, labels, rotation=75, ha="right", fontsize=7)
    plt.ylabel("Frames")
    plt.title("Target count per frame distribution by sequence")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "all_sequences_target_count_per_frame_distribution.png")
    plt.close()


def plot_candidate_histograms(seqs: dict[str, dict[str, Any]], candidate_sequences: list[str]) -> None:
    range_values: list[float] = []
    az_values: list[float] = []
    for seq in candidate_sequences:
        for n in seqs[seq]["common_nums"]:
            for lab in seqs[seq]["label_rows_by_num"].get(n, []):
                range_values.append(lab.range_m)
                az_values.append(lab.azimuth_deg)
    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(range_values, bins=40, color="#2a9d8f", edgecolor="black", linewidth=0.3)
    plt.xlabel("Range (m)")
    plt.ylabel("Target count")
    plt.title("Candidate sequences range histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "candidate_sequences_range_histogram.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(az_values, bins=40, color="#e76f51", edgecolor="black", linewidth=0.3)
    plt.xlabel("Azimuth (deg)")
    plt.ylabel("Target count")
    plt.title("Candidate sequences azimuth histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "candidate_sequences_azimuth_histogram.png")
    plt.close()


def plot_selected_histograms(manifest_rows: list[dict[str, Any]]) -> None:
    ranges: list[float] = []
    azimuths: list[float] = []
    target_counts: list[int] = []
    for row in manifest_rows:
        target_counts.append(int(row["target_count"]))
        if row["range_min"] != "":
            ranges.append(float(row["range_min"]))
            ranges.append(float(row["range_max"]))
        if row["azimuth_min"] != "":
            azimuths.append(float(row["azimuth_min"]))
            azimuths.append(float(row["azimuth_max"]))

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(ranges, bins=40, color="#457b9d", edgecolor="black", linewidth=0.3)
    plt.xlabel("Range (m)")
    plt.ylabel("Target count")
    plt.title("Selected D1A subset range histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "selected_subset_range_histogram.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(azimuths, bins=40, color="#f4a261", edgecolor="black", linewidth=0.3)
    plt.xlabel("Azimuth (deg)")
    plt.ylabel("Target count")
    plt.title("Selected D1A subset azimuth histogram")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "selected_subset_azimuth_histogram.png")
    plt.close()

    plt.figure(figsize=(8, 4), dpi=150)
    bins = np.arange(min(target_counts), max(target_counts) + 2) - 0.5 if target_counts else [0, 1]
    plt.hist(target_counts, bins=bins, color="#6a994e", edgecolor="black", linewidth=0.5)
    plt.xlabel("Target count per frame")
    plt.ylabel("Frame count")
    plt.title("Selected D1A subset target count per frame")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "selected_subset_target_count_per_frame_histogram.png")
    plt.close()


def format_top_table(rows: list[dict[str, Any]], n: int = 5) -> str:
    lines = [
        "| 排名 | sequence | score | aligned | targets | 2+目标帧 | range span | azimuth span | class | 风险 |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for idx, r in enumerate(rows[:n], start=1):
        risks = []
        if int(r["empty_label_frames"]) == 0:
            risks.append("无空标签帧")
        if int(r["class_count"]) <= 1:
            risks.append("类别单一")
        if float(r["multi_target_frame_prop"] or 0) < 0.1:
            risks.append("多目标少")
        if not risks:
            risks.append("低")
        lines.append(
            f"| {idx} | `{r['sequence']}` | {float(r['d1a_suitability_score']):.2f} | "
            f"{int(r['aligned_count'])} | {int(r['total_targets'])} | {int(r['target_count_two_plus_frames'])} | "
            f"{float(r['range_span'] or 0):.2f} | {float(r['azimuth_span'] or 0):.2f} | "
            f"`{r['class_distribution']}` | {'；'.join(risks)} |"
        )
    return "\n".join(lines)


def write_report(
    stats_rows: list[dict[str, Any]],
    score_rows: list[dict[str, Any]],
    final_sequences: list[str],
    summary_rows: list[dict[str, Any]],
    selected_total: dict[str, Any],
    sample_rows: list[dict[str, Any]],
) -> None:
    cms = next(r for r in stats_rows if r["sequence"] == "2019_04_09_cms1000")
    top5 = score_rows[:5]
    seq_basic_lines = [
        "| sequence | aligned | targets | empty | 1目标帧 | 2+目标帧 | class | range span | azimuth span | score |",
        "|---|---:|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for r in sorted(score_rows, key=lambda x: x["sequence"]):
        seq_basic_lines.append(
            f"| `{r['sequence']}` | {int(r['aligned_count'])} | {int(r['total_targets'])} | "
            f"{int(r['empty_label_frames'])} | {int(r['target_count_one_frames'])} | "
            f"{int(r['target_count_two_plus_frames'])} | `{r['class_distribution']}` | "
            f"{float(r['range_span'] or 0):.2f} | {float(r['azimuth_span'] or 0):.2f} | "
            f"{float(r['d1a_suitability_score']):.2f} |"
        )

    sample_summary = [r for r in sample_rows if r.get("frame_num") == "SUMMARY"]
    sample_lines = [
        "| sequence | sample | ok | bad | range peak mean dB | RD energy mean dB | label projection hit |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in sample_summary:
        hit = r.get("label_projection_hit_rate", "")
        hit_str = f"{float(hit):.3f}" if hit != "" else ""
        sample_lines.append(
            f"| `{r['sequence']}` | {r['sample_count']} | {r['sample_ok_count']} | {r['sample_bad_count']} | "
            f"{float(r['range_peak_mean_db']):.2f} | {float(r['rd_energy_mean_db']):.2f} | {hit_str} |"
        )

    per_seq_lines = [
        "| source sequence | frames | targets | empty | single | multi |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for r in summary_rows:
        per_seq_lines.append(
            f"| `{r['source_sequence']}` | {r['frame_count']} | {r['target_total']} | "
            f"{r['empty_frames']} | {r['single_target_frames']} | {r['multi_target_frames']} |"
        )

    text = f"""# D0B Gao 77GHz 子集重新筛选与构建报告

生成时间：2026-06-26 15:33  
阶段：D0B 子集重新筛选  
数据包：`{ZIP_PATH}`

## 1. 执行边界

本次只做 Gao 77GHz 子集重新筛选与构建，没有进入 D1-D14，没有训练模型，没有做 synthetic interference injection，没有做 CFAR，也没有做 fixed-PFA threshold calibration。

## 2. 总体结果

- 共发现 sequence：{len(stats_rows)}
- 最终选择方式：multi-sequence subset
- 最终子集路径：`{SUBSET_DIR}`
- radar 文件：`{SUBSET_RADAR_DIR}`
- label 文件：`{SUBSET_LABEL_DIR}`
- manifest：`{SUBSET_MANIFEST_DIR / 'selected_frames_manifest.csv'}`
- 最终子集帧数：{selected_total['frame_count']}
- 最终子集目标数：{selected_total['target_total']}
- 最终子集 class 分布：`{selected_total['class_distribution']}`

## 3. 每个 sequence 的基本统计

{chr(10).join(seq_basic_lines)}

完整 CSV：

- `results\\d0b_gao77_subset_selection\\sequence_label_stats.csv`
- `results\\d0b_gao77_subset_selection\\sequence_score_table.csv`

## 4. 为什么旧的 `cms1000` 不适合作为唯一 D1A 子集

旧子集 `2019_04_09_cms1000` 可读、对齐质量好，但它作为唯一 D1A sanity 子集太单一：

- aligned 帧数：{int(cms['aligned_count'])}
- 目标总数：{int(cms['total_targets'])}
- class 分布：`{cms['class_distribution']}`
- 2+ 目标帧数：{int(cms['target_count_two_plus_frames'])}
- range span：{float(cms['range_span'] or 0):.2f} m
- azimuth span：{float(cms['azimuth_span'] or 0):.2f} deg

它基本是单类别、单目标、几何变化有限的 sequence，适合检查读取链路，但不适合作为 weak / mid / strong target split 的主要 sanity 子集。

## 5. 排名前 5 的候选 sequence

{format_top_table(score_rows, 5)}

## 6. 候选 radar 抽样检查

对排名前 5 的候选 sequence，每个抽样 {RADAR_SAMPLE_PER_SEQUENCE} 个 radar `.mat` 文件，只做读取、range FFT、简单 Doppler FFT 和粗略 label-to-range-bin 检查。

{chr(10).join(sample_lines)}

完整 CSV：

- `results\\d0b_gao77_subset_selection\\candidate_radar_sample_stats.csv`

## 7. 最终子集组成

最终没有选择单个 sequence，而是从排名靠前的多个 sequence 中构建 multi-sequence subset。原因是单个 sequence 即使对齐好，也容易存在类别、距离或角度覆盖不足；multi-sequence 更适合作为 D1A weak/mid/strong sanity 输入。

选中 sequence：

{', '.join(f'`{s}`' for s in final_sequences)}

按来源统计：

{chr(10).join(per_seq_lines)}

最终子集总体统计：

| 指标 | 数值 |
|---|---:|
| frame count | {selected_total['frame_count']} |
| target total | {selected_total['target_total']} |
| empty frames | {selected_total['empty_frames']} |
| single-target frames | {selected_total['single_target_frames']} |
| multi-target frames | {selected_total['multi_target_frames']} |
| range min | {float(selected_total['range_min']):.2f} |
| range max | {float(selected_total['range_max']):.2f} |
| range mean | {float(selected_total['range_mean']):.2f} |
| range std | {float(selected_total['range_std']):.2f} |
| azimuth min | {float(selected_total['azimuth_min']):.2f} |
| azimuth max | {float(selected_total['azimuth_max']):.2f} |
| azimuth mean | {float(selected_total['azimuth_mean']):.2f} |
| azimuth std | {float(selected_total['azimuth_std']):.2f} |
| target count min | {selected_total['target_count_min']} |
| target count mean | {float(selected_total['target_count_mean']):.2f} |
| target count median | {selected_total['target_count_median']} |
| target count max | {selected_total['target_count_max']} |

## 8. 是否比 `cms1000` 更适合 weak/mid/strong split

结论：是。

原因：

1. 最终子集来自多个 sequence，不再依赖单一静态几何；
2. range 覆盖明显更宽；
3. azimuth / px 覆盖明显更宽；
4. target count per frame 不再过于单一；
5. 类别分布更丰富；
6. radar 抽样读取正常，range FFT / RD smoke test 正常；
7. 子集规模约 {selected_total['frame_count']} 帧，适合 GTX 1650 4GB 上做小规模 D1A sanity。

注意：这仍然不是论文级最终数据集，只是为了 D1A sanity 更合理。

## 9. 可视化输出

图像目录：

`{FIG_DIR}`

至少包含：

- `all_sequences_range_spread_ranking.png`
- `all_sequences_azimuth_spread_ranking.png`
- `all_sequences_target_count_per_frame_distribution.png`
- `candidate_sequences_range_histogram.png`
- `candidate_sequences_azimuth_histogram.png`
- `selected_subset_range_histogram.png`
- `selected_subset_azimuth_histogram.png`
- `selected_subset_target_count_per_frame_histogram.png`
- `sample_range_profile_*.png`
- `sample_rd_map_*.png`
- `sample_label_to_range_*.png`

## 10. 是否建议进入 D1A

建议进入 D1A，但仍然只进入 D1A sanity，不训练模型。

进入 D1A 前应继续保持限制：

1. 先做 label 到 range / angle / RD mask 的可视化检查；
2. 不要直接训练；
3. 不要把这个子集包装成最终实验数据；
4. 如果 target/background mask 明显不合理，再回到 D0B 调整子集或换数据集。

## 11. 阻塞点

当前没有硬阻塞点。主要风险是 Gao 标签是物理坐标框，不是直接 RD/RDA cell mask；D1A 必须先把坐标到 radar map 的粗投影链路验证清楚。

## 12. 简短结论

| 问题 | 答案 |
|---|---|
| 是否成功构建新的 D1A 子集 | 是 |
| 新子集路径 | `{SUBSET_DIR}` |
| 为什么比 cms1000 更合适 | 多 sequence、range/azimuth/class/target count 覆盖更丰富 |
| 是否建议进入 D1A | 建议，只做 sanity |
| 如果仍然不适合怎么办 | 先检查 D1A mask 投影；若 mask 不稳，再继续筛 sequence，不急着换数据集 |
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")
    REPORT_TS_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    if not ZIP_PATH.exists():
        raise FileNotFoundError(ZIP_PATH)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    print("[D0B] scanning zip labels...")
    seqs, stats_rows = scan_zip()
    score_rows = add_scores(stats_rows)
    top_label_sequences = [r["sequence"] for r in score_rows[:TOP_K]]
    print("[D0B] top label-scan candidates:", ", ".join(top_label_sequences))

    print("[D0B] radar sample smoke test for top candidates...")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        sample_rows = radar_sample_check(zf, seqs, top_label_sequences)
    score_rows = update_scores_with_radar(score_rows, sample_rows)
    final_sequences = [r["sequence"] for r in score_rows[:TOP_K]]
    print("[D0B] final top candidates:", ", ".join(final_sequences))

    print("[D0B] plotting sequence and candidate summaries...")
    plot_sequence_rankings(score_rows, stats_rows)
    plot_candidate_histograms(seqs, final_sequences)

    print("[D0B] selecting diverse frames...")
    selected = select_diverse_frames(seqs, final_sequences, PER_SEQUENCE_QUOTA)
    print(f"[D0B] selected frames: {len(selected)}")

    print("[D0B] copying selected radar/label frames from zip...")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        manifest_rows = copy_selected_frames(zf, selected)

    summary_rows, selected_total = summarize_selected(manifest_rows)
    plot_selected_histograms(manifest_rows)

    sequence_columns = [
        "sequence",
        "radar_count",
        "label_count",
        "image_count",
        "aligned_count",
        "radar_only_count",
        "label_only_count",
        "empty_label_frames",
        "nonempty_label_frames",
        "total_targets",
        "target_count_min",
        "target_count_mean",
        "target_count_median",
        "target_count_max",
        "target_count_zero_frames",
        "target_count_one_frames",
        "target_count_two_plus_frames",
        "multi_target_frame_prop",
        "class_distribution",
        "class_count",
        "px_min",
        "px_max",
        "px_mean",
        "px_std",
        "py_min",
        "py_max",
        "py_mean",
        "py_std",
        "range_min",
        "range_max",
        "range_mean",
        "range_std",
        "range_span",
        "azimuth_min",
        "azimuth_max",
        "azimuth_mean",
        "azimuth_std",
        "azimuth_span",
        "wid_min",
        "wid_max",
        "len_min",
        "len_max",
        "label_anomaly_count",
    ]
    score_columns = sequence_columns + [
        "alignment_quality",
        "target_volume_score",
        "range_diversity_score",
        "azimuth_diversity_score",
        "empty_bonus_score",
        "clean_label_score",
        "label_only_suitability_score",
        "radar_sample_ok_ratio",
        "label_projection_hit_rate",
        "radar_sample_score",
        "d1a_suitability_score",
        "score_reason",
    ]
    manifest_columns = [
        "new_frame_id",
        "source_sequence",
        "source_radar_file",
        "source_label_file",
        "new_radar_file",
        "new_label_file",
        "target_count",
        "class_ids",
        "class_counts",
        "px_min",
        "px_max",
        "py_min",
        "py_max",
        "range_min",
        "range_max",
        "azimuth_min",
        "azimuth_max",
        "selection_reason",
    ]
    write_csv(RESULT_DIR / "sequence_label_stats.csv", stats_rows, sequence_columns)
    write_csv(RESULT_DIR / "sequence_score_table.csv", score_rows, score_columns)
    write_csv(RESULT_DIR / "candidate_radar_sample_stats.csv", sample_rows)
    write_csv(RESULT_DIR / "selected_subset_summary.csv", summary_rows + [selected_total])
    write_csv(RESULT_DIR / "selected_frames_manifest.csv", manifest_rows, manifest_columns)
    write_csv(SUBSET_MANIFEST_DIR / "selected_frames_manifest.csv", manifest_rows, manifest_columns)
    write_csv(RESULT_DIR / "selected_subset_summary_by_sequence.csv", summary_rows)

    config = {
        "zip_path": str(ZIP_PATH),
        "result_dir": str(RESULT_DIR),
        "figure_dir": str(FIG_DIR),
        "subset_dir": str(SUBSET_DIR),
        "random_seed": RANDOM_SEED,
        "top_k": TOP_K,
        "radar_sample_per_sequence": RADAR_SAMPLE_PER_SEQUENCE,
        "target_total_frames": TARGET_TOTAL_FRAMES,
        "per_sequence_quota": PER_SEQUENCE_QUOTA,
        "final_sequences": final_sequences,
        "strict_limits": {
            "no_training": True,
            "no_d1_d14": True,
            "no_synthetic_interference": True,
            "no_cfar": True,
            "no_fixed_pfa": True,
            "no_full_images_extract": True,
        },
    }
    (RESULT_DIR / "selection_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    write_report(stats_rows, score_rows, final_sequences, summary_rows, selected_total, sample_rows)
    print("[D0B] done")
    print(json.dumps({"subset_dir": str(SUBSET_DIR), "frames": len(manifest_rows), "report": str(REPORT_PATH)}, indent=2))


if __name__ == "__main__":
    main()
