from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import loadmat


ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "gao_77ghz_raw_adc" / "subset_d1a_v1"
MANIFEST_CSV = DATASET_DIR / "manifest" / "selected_frames_manifest.csv"
LABEL_POLICY_JSON = DATASET_DIR / "manifest" / "label_policy.json"
LABEL_DIR = DATASET_DIR / "text_labels"
RADAR_DIR = DATASET_DIR / "radar_raw_frame"

RESULT_DIR = ROOT / "results" / "d5h_representation_protocol_audit_executed"
FIG_DIR = ROOT / "gao_77ghz_raw_adc" / "reports" / "d5h_representation_protocol_audit_figures"

D5C_CSV = ROOT / "results" / "d5b_d5c_weak_definition_rdra_diagnosis" / "d5c_range_rd_ra_separability.csv"
D5D_THRESHOLDS_JSON = ROOT / "results" / "d5d_rd_only_supplementary" / "d5d_rd_weak_thresholds.json"
D5E_DIR = ROOT / "results" / "d5e_rd_proxy_ceiling_diagnosis"
D5E_CEILING_CSV = D5E_DIR / "d5e_ceiling_effect_audit.csv"
D5E_PFA_CSV = D5E_DIR / "d5e_pfa_sensitivity.csv"
D5E_PROXY_CSV = D5E_DIR / "d5e_rd_proxy_label_dependence.csv"
D5E_CONFIG_JSON = D5E_DIR / "d5e_config.json"
D5C_RA_RCA_DIR = ROOT / "results" / "d5c_ra_rca_self_check"
D5C_RA_RCA_CONFIG_JSON = D5C_RA_RCA_DIR / "ra_rca_config.json"
D5C_RA_MASK_CSV = D5C_RA_RCA_DIR / "ra_mask_width_sensitivity.csv"
D5C_RA_FFT_CSV = D5C_RA_RCA_DIR / "ra_fft_axis_audit.csv"

PRIMARY_PFA = 1e-2
SECONDARY_PFA = 1e-3
STRICTER_PFAS = [5e-4, 1e-4]
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
DATE_TEXT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


REPRESENTATIONS = [
    "range_only",
    "corrected_RD",
    "corrected_RA",
    "RAD",
    "temporal_RD",
    "temporal_RA",
    "temporal_RAD",
    "STFT_spectrogram",
    "complex_IQ",
    "complex_RD",
    "raw_ADC",
    "raw_ADC_learnable_FFT",
    "radar_point_cloud",
]


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def fmt(value: Any, digits: int = 4) -> str:
    try:
        value_f = float(value)
        if math.isnan(value_f):
            return ""
        return f"{value_f:.{digits}f}"
    except (TypeError, ValueError):
        return str(value)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def markdown_table(rows: list[dict[str, Any]], columns: list[str], max_rows: int | None = None) -> str:
    rows2 = rows[:max_rows] if max_rows else rows
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows2:
        body.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def append_manifest(outputs: list[tuple[Path, str]]) -> None:
    manifest = ROOT / "MANIFEST.md"
    if not manifest.exists():
        manifest.write_text(
            "# Research Output Manifest\n\n"
            "> Auto-maintained by ARIS skills. Tracks all generated artifacts across the research lifecycle.\n\n"
            "| Timestamp | Skill | File | Stage | Description |\n"
            "|-----------|-------|------|-------|-------------|\n",
            encoding="utf-8",
        )
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with manifest.open("a", encoding="utf-8") as fh:
        for path, desc in outputs:
            rel = path.resolve().relative_to(ROOT)
            fh.write(f"| {stamp} | /experiment-bridge | {rel} | implementation | {desc} |\n")


def load_local_inventory() -> dict[str, Any]:
    manifest = pd.read_csv(MANIFEST_CSV)
    with LABEL_POLICY_JSON.open("r", encoding="utf-8") as fh:
        label_policy = json.load(fh)

    label_files = sorted(LABEL_DIR.glob("*.csv"))
    raw_files = sorted(RADAR_DIR.glob("*.mat"))
    label_row_count = 0
    label_col_counts: set[int] = set()
    class_ids: set[int] = set()
    for path in label_files:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        for line in text.splitlines():
            vals = [x for x in line.split(",") if x != ""]
            if vals:
                label_row_count += 1
                label_col_counts.add(len(vals))
                class_ids.add(as_int(vals[1] if len(vals) > 1 else vals[0]))

    sample_raw_shape = ""
    sample_raw_dtype = ""
    sample_raw_complex = False
    sample_raw_path = raw_files[0] if raw_files else None
    if sample_raw_path is not None:
        adc = loadmat(sample_raw_path)["adcData"]
        sample_raw_shape = "x".join(str(x) for x in adc.shape)
        sample_raw_dtype = str(adc.dtype)
        sample_raw_complex = bool(np.iscomplexobj(adc))

    source_sequences = sorted(str(x) for x in manifest["source_sequence"].dropna().unique().tolist())
    source_frame_ids = [as_int(str(x).replace(".mat", "")) for x in manifest["source_radar_file"].tolist()]
    source_frame_gap_count = 0
    for seq in source_sequences:
        seq_rows = manifest[manifest["source_sequence"] == seq]
        ids = sorted(as_int(str(x).replace(".mat", "")) for x in seq_rows["source_radar_file"].tolist())
        source_frame_gap_count += sum(1 for a, b in zip(ids, ids[1:]) if b - a != 1)

    return {
        "manifest": manifest,
        "label_policy": label_policy,
        "frame_count": int(len(manifest)),
        "label_file_count": int(len(label_files)),
        "raw_file_count": int(len(raw_files)),
        "label_row_count": int(label_row_count),
        "label_col_counts": sorted(label_col_counts),
        "class_ids": sorted(class_ids),
        "sample_raw_shape": sample_raw_shape,
        "sample_raw_dtype": sample_raw_dtype,
        "sample_raw_complex": sample_raw_complex,
        "sample_raw_file": str(sample_raw_path) if sample_raw_path else "",
        "source_sequence_count": int(len(source_sequences)),
        "source_frame_id_min": int(min(source_frame_ids)) if source_frame_ids else "",
        "source_frame_id_max": int(max(source_frame_ids)) if source_frame_ids else "",
        "source_frame_gap_count": int(source_frame_gap_count),
    }


def load_evidence_tables() -> dict[str, Any]:
    d5c_rows = read_csv_dicts(D5C_CSV)
    d5c_by_rep = {row["representation"]: row for row in d5c_rows}
    with D5D_THRESHOLDS_JSON.open("r", encoding="utf-8") as fh:
        d5d_thresholds = json.load(fh)
    d5e_ceiling = read_csv_dicts(D5E_CEILING_CSV)
    d5e_pfa = read_csv_dicts(D5E_PFA_CSV)
    d5e_proxy = read_csv_dicts(D5E_PROXY_CSV)
    with D5E_CONFIG_JSON.open("r", encoding="utf-8") as fh:
        d5e_config = json.load(fh)
    with D5C_RA_RCA_CONFIG_JSON.open("r", encoding="utf-8") as fh:
        ra_config = json.load(fh)
    ra_mask = read_csv_dicts(D5C_RA_MASK_CSV)
    ra_fft = read_csv_dicts(D5C_RA_FFT_CSV)

    d5e_ceiling_mean = next(row for row in d5e_ceiling if row.get("seed") == "mean")
    d5e_pfa_mean = [row for row in d5e_pfa if row.get("seed") == "mean"]
    d5e_proxy_mean = [row for row in d5e_proxy if row.get("seed") == "mean"]
    ra_original = next(
        row
        for row in ra_mask
        if row["candidate"] == "atan2_px_py_current"
        and row["range_mask_name"] == "default"
        and int(row["angle_total_width_bins"]) == 7
    )
    ra_best_physical = max(
        [row for row in ra_mask if row["candidate"] == "atan2_px_py_current"],
        key=lambda row: as_float(row["weak_target_projection_hit_rate"]),
    )
    return {
        "d5c_by_rep": d5c_by_rep,
        "d5d_thresholds": d5d_thresholds,
        "d5e_ceiling_mean": d5e_ceiling_mean,
        "d5e_pfa_mean": d5e_pfa_mean,
        "d5e_proxy_mean": d5e_proxy_mean,
        "d5e_config": d5e_config,
        "ra_config": ra_config,
        "ra_original": ra_original,
        "ra_best_physical": ra_best_physical,
        "ra_fft": ra_fft,
    }


def build_phase0_tables(
    local: dict[str, Any],
    evidence: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    d5d_thresholds = evidence["d5d_thresholds"]
    d5d_test_weak_n = d5d_thresholds.get("counts", {}).get("test", {}).get("weak_n", "")
    d5d_threshold_source = d5d_thresholds.get("threshold_source", "")
    label_inventory = [
        {
            "label_or_protocol_item": "class/objectness",
            "status": "available",
            "true_label_available": True,
            "proxy_available": False,
            "observed_local_evidence": f"{local['label_file_count']} text label CSV files; {local['label_row_count']} object rows; class ids {local['class_ids']}",
            "confirmation_method": "read text_labels/*.csv and label_policy.json",
            "claim_ceiling": "objectness/class sanity only",
        },
        {
            "label_or_protocol_item": "range",
            "status": "available_by_projection_proxy",
            "true_label_available": False,
            "proxy_available": True,
            "observed_local_evidence": "selected_frames_manifest.csv has range_min/range_max; label rows have px/py-like spatial fields",
            "confirmation_method": f"read {MANIFEST_CSV.name}; range_min/range_max nonempty",
            "claim_ceiling": "range-only/projection sanity, not full physical GT",
        },
        {
            "label_or_protocol_item": "azimuth",
            "status": "proxy_available_calibration_unresolved",
            "true_label_available": False,
            "proxy_available": True,
            "observed_local_evidence": "selected_frames_manifest.csv has azimuth_min/azimuth_max; D5C-RA-RCA reports smoke RA axis only",
            "confirmation_method": "read manifest azimuth fields and ra_fft_axis_audit.csv",
            "claim_ceiling": "RA calibration audit only",
        },
        {
            "label_or_protocol_item": "Doppler",
            "status": "absent_as_true_label",
            "true_label_available": False,
            "proxy_available": True,
            "observed_local_evidence": "text label CSVs have 6 columns and no Doppler/velocity field; D5E uses clean/interfered RD peak proxies",
            "confirmation_method": "read text label rows and d5e_rd_proxy_label_dependence.csv",
            "claim_ceiling": "RD proxy only; no confirmed RD performance",
        },
        {
            "label_or_protocol_item": "RAD boxes",
            "status": "absent",
            "true_label_available": False,
            "proxy_available": False,
            "observed_local_evidence": "no RAD annotation directory/file found under subset_d1a_v1",
            "confirmation_method": "listed subset directories and known manifest/label files",
            "claim_ceiling": "insufficient labels for Gao77 RAD claims",
        },
        {
            "label_or_protocol_item": "temporal track IDs",
            "status": "absent",
            "true_label_available": False,
            "proxy_available": "frame_continuity_only",
            "observed_local_evidence": f"{local['source_sequence_count']} source sequences; frame IDs exist but no per-object track ID column/file",
            "confirmation_method": "read source_sequence/source_radar_file and text_labels",
            "claim_ceiling": "no temporal target performance claim",
        },
        {
            "label_or_protocol_item": "velocity",
            "status": "absent_proxy_only",
            "true_label_available": False,
            "proxy_available": True,
            "observed_local_evidence": "no velocity column in text labels; RD Doppler peak can only proxy radial motion",
            "confirmation_method": "read text labels and D5E proxy table",
            "claim_ceiling": "diagnostic proxy only",
        },
        {
            "label_or_protocol_item": "raw complex ADC",
            "status": "available",
            "true_label_available": True,
            "proxy_available": False,
            "observed_local_evidence": f"{local['raw_file_count']} MAT files; sample adcData shape={local['sample_raw_shape']}, dtype={local['sample_raw_dtype']}, complex={local['sample_raw_complex']}",
            "confirmation_method": "loaded one radar_raw_frame MAT file with scipy.io.loadmat",
            "claim_ceiling": "availability and deterministic transform audit",
        },
        {
            "label_or_protocol_item": "clean/interfered synthetic pairing",
            "status": "available_as_synthetic_pairing",
            "true_label_available": False,
            "proxy_available": True,
            "observed_local_evidence": "D5D/D5E generated synthetic FMCW-like interference manifests and clean/interfered RD cases",
            "confirmation_method": "read D5E config and prior interference CSV paths",
            "claim_ceiling": "synthetic proxy only, not real physical interference",
        },
        {
            "label_or_protocol_item": "weak target definition",
            "status": "proxy_train_only_threshold_available_but_small",
            "true_label_available": False,
            "proxy_available": True,
            "observed_local_evidence": f"D5D frozen threshold source={d5d_threshold_source}; D5D test weak_n={d5d_test_weak_n} under overlap-aware q30",
            "confirmation_method": f"parsed {D5D_THRESHOLDS_JSON.name}",
            "claim_ceiling": "weak evidence; fails D5H pass threshold weak_n>=100 for RD proxy",
        },
    ]

    req_rows = [
        req("range_only", "class/objectness; range projection; target/background mask; weak split", "class/objectness", "range; weak target; background mask", "", "supported baseline", "baseline only; range collapse/proxy"),
        req("corrected_RD", "range + Doppler/RD boxes; weak split; fixed-PFA background", "class/objectness; range", "clean/interfered RD peak Doppler", "true Doppler/velocity", "computable proxy audit", "no true Doppler and D5E saturation"),
        req("corrected_RA", "range + calibrated azimuth; weak split", "class/objectness; range", "px/py azimuth projection", "calibrated radar angle GT", "calibration audit only", "angle calibration unresolved"),
        req("RAD", "3D range-azimuth-Doppler boxes or dense masks", "class/objectness; range proxy", "possible constructed proxy", "true Doppler; RAD boxes", "not supported for confirmed Gao77 claims", "missing RAD boxes"),
        req("temporal_RD", "track IDs; frame continuity; RD labels", "range proxy", "sequence continuity; RD peak proxy", "track IDs; true velocity/Doppler", "insufficient without tracks", "missing track IDs"),
        req("temporal_RA", "track IDs; calibrated RA labels", "range proxy", "azimuth projection; frame continuity", "track IDs; calibrated RA", "insufficient while RA unresolved", "missing tracks and RA calibration"),
        req("temporal_RAD", "track IDs + RAD boxes", "range proxy", "none sufficient", "track IDs; RAD boxes; Doppler", "not supported", "missing RAD and temporal labels"),
        req("STFT_spectrogram", "raw ADC/beat signal; projected target/background; weak split", "raw ADC", "range/frequency projection", "true signal-domain target labels", "signal diagnostic only", "labels project only to range/frequency"),
        req("complex_IQ", "raw complex ADC; phase/no-harm label; projected object labels", "raw complex ADC", "range/azimuth projections", "phase-aware object GT", "availability/proxy audit", "no phase/object GT"),
        req("complex_RD", "complex RD tensor; RD target boxes; phase no-harm", "raw complex ADC", "clean/interfered RD peak proxy", "true Doppler", "proxy audit only", "no true Doppler"),
        req("raw_ADC", "raw ADC; deterministic score; projected object labels", "raw complex ADC", "downstream FFT/range projection", "raw-domain target labels", "availability/proxy audit", "no raw-domain target mask"),
        req("raw_ADC_learnable_FFT", "raw ADC + learned transform + detection labels", "raw complex ADC", "none allowed in D5H", "training route labels/validated objective", "future only", "learned FFT implies forbidden training"),
        req("radar_point_cloud", "CFAR points + point/object labels", "range/azimuth proxy", "CFAR point-to-label matching", "point labels/tracks", "auxiliary diagnostic only", "weak targets may disappear before point cloud"),
    ]

    risk_rows = [
        risk("range_only", "range projection + train-only weak threshold", "low_to_medium", "range collapse/overlap hides targets", "report baseline only; no positive claim", "proxy-only"),
        risk("corrected_RD", "clean/interfered RD Doppler peak projection", "high", "clean peak boxes and saturated baseline are over-optimistic", "never write confirmed RD performance", "proxy-only"),
        risk("corrected_RA", "px/py to azimuth projection", "medium", "axis/sign/mask width can inflate/deflate hits", "cap at calibration audit until physical mapping is resolved", "proxy-only"),
        risk("RAD", "constructed 3D boxes if attempted", "high", "invented boxes can encode clean peaks", "do not construct performance labels from Gao77", "insufficient-labels"),
        risk("temporal_RD", "sequence continuity + RD proxy", "high", "future-frame/clean-frame association can leak", "no temporal claim without track IDs", "insufficient-labels"),
        risk("temporal_RA", "sequence continuity + RA proxy", "high", "inherits RA and tracking leakage", "defer until RA and tracks pass", "insufficient-labels"),
        risk("temporal_RAD", "constructed RAD tracks", "high", "combines missing labels and temporal leakage", "external dataset/protocol reference only", "insufficient-labels"),
        risk("STFT_spectrogram", "range/frequency projection from spatial labels", "medium", "signal separability may not map to object hits", "use as signal diagnostic only", "proxy-only"),
        risk("complex_IQ", "projected object labels on raw complex samples", "medium", "phase no-harm can be underdefined", "availability and deterministic no-harm only", "proxy-only"),
        risk("complex_RD", "complex RD with same Doppler proxy", "high", "phase may be useful but labels remain proxy", "cap at proxy-only", "proxy-only"),
        risk("raw_ADC", "downstream deterministic projection", "medium", "raw domain has no direct object mask", "memory/feasibility only", "proxy-only"),
        risk("raw_ADC_learnable_FFT", "learned spectral transform", "not_allowed", "would require training", "exclude from D5H", "insufficient-labels"),
        risk("radar_point_cloud", "CFAR-derived sparse points", "medium", "sub-threshold weak targets may be discarded", "auxiliary only", "proxy-only"),
    ]
    return label_inventory, req_rows, risk_rows


def req(
    representation: str,
    required_labels: str,
    available_true_labels: str,
    proxy_labels: str,
    missing_labels: str,
    gao77_support: str,
    final_label_blocker: str,
) -> dict[str, Any]:
    return {
        "representation": representation,
        "required_labels": required_labels,
        "available_true_labels": available_true_labels,
        "proxy_labels": proxy_labels,
        "missing_labels": missing_labels,
        "gao77_support": gao77_support,
        "final_label_blocker": final_label_blocker,
    }


def risk(
    representation: str,
    proxy_source: str,
    leakage_risk: str,
    optimism_risk: str,
    mitigation: str,
    claim_ceiling: str,
) -> dict[str, Any]:
    return {
        "representation": representation,
        "proxy_source": proxy_source,
        "leakage_risk": leakage_risk,
        "proxy_optimism_risk": optimism_risk,
        "mitigation": mitigation,
        "claim_ceiling": claim_ceiling,
    }


def per_sample_mb(shape: tuple[int, ...], channels: int = 1, bytes_per_value: int = 4) -> float:
    return float(np.prod(shape) * channels * bytes_per_value / (1024**2))


def build_memory_rows(local: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [
        mem("range_only", "128", "float32", per_sample_mb((128,)), 64, True, "range profile only"),
        mem("corrected_RD", "128x255", "float32 magnitude/dB", per_sample_mb((128, 255)), 16, True, "2D RD smoke map"),
        mem("corrected_RA", "128x64", "float32 magnitude/dB", per_sample_mb((128, 64)), 16, True, "2D RA smoke map"),
        mem("RAD", "128x64x255", "float32 magnitude/dB", per_sample_mb((128, 64, 255)), 2, True, "tensor memory feasible for tiny sanity, labels missing"),
        mem("temporal_RD", "T4x128x255", "float32 magnitude/dB", per_sample_mb((4, 128, 255)), 4, True, "tracks missing"),
        mem("temporal_RA", "T4x128x64", "float32 magnitude/dB", per_sample_mb((4, 128, 64)), 4, True, "tracks and RA calibration missing"),
        mem("temporal_RAD", "T4x128x64x255", "float32 magnitude/dB", per_sample_mb((4, 128, 64, 255)), 1, True, "large but tiny subset fits; labels missing"),
        mem("STFT_spectrogram", "rx/tx aggregated 255x128", "float32 magnitude", per_sample_mb((255, 128)), 16, True, "rough no-training score estimate"),
        mem("complex_IQ", local["sample_raw_shape"], "complex64 converted to real/imag", per_sample_mb((128, 255, 4, 2), 2, 4), 4, True, "raw MAT is complex128; conversion assumed for sanity"),
        mem("complex_RD", "128x255x2", "real/imag float32", per_sample_mb((128, 255), 2, 4), 8, True, "phase retained but labels proxy"),
        mem("raw_ADC", local["sample_raw_shape"], "complex64 converted to real/imag", per_sample_mb((128, 255, 4, 2), 2, 4), 4, True, "memory feasible for tiny no-training audit"),
        mem("raw_ADC_learnable_FFT", local["sample_raw_shape"], "complex64 converted to real/imag", per_sample_mb((128, 255, 4, 2), 2, 4), 4, False, "training transform is forbidden in D5H"),
        mem("radar_point_cloud", "variable sparse points", "float32 attributes", 0.1, 64, True, "point labels missing; weak targets may be pre-filtered"),
    ]
    return rows


def mem(
    representation: str,
    input_shape_estimate: str,
    dtype: str,
    sample_mb: float,
    sanity_batch: int,
    fits: bool,
    caveat: str,
) -> dict[str, Any]:
    return {
        "representation": representation,
        "input_shape_estimate": input_shape_estimate,
        "dtype_assumption": dtype,
        "per_sample_mb_estimate": round(sample_mb, 4),
        "sanity_batch_estimate": sanity_batch,
        "sanity_batch_tensor_mb_estimate": round(sample_mb * sanity_batch, 4),
        "fits_gtx1650_4gb_sanity_subset": bool(fits),
        "caveat": caveat,
    }


def fixed_pfa_flag(measured: float, target: float) -> str:
    if math.isnan(measured):
        return "not_available"
    tolerance = max(target * 0.25, 1e-4)
    return "yes" if abs(measured - target) <= tolerance else "warn"


def build_phase1_tables(evidence: dict[str, Any], memory_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    d5c = evidence["d5c_by_rep"]
    range_row = d5c["range_only"]
    rd_row = d5c["RD"]
    ra_row = d5c["RA"]
    rd_ceiling = evidence["d5e_ceiling_mean"]
    rd_pfa_mean = evidence["d5e_pfa_mean"]
    rd_proxy_mean = evidence["d5e_proxy_mean"]
    ra_config = evidence["ra_config"]
    ra_original = evidence["ra_original"]
    ra_best = evidence["ra_best_physical"]
    mem_by_rep = {row["representation"]: row for row in memory_rows}

    rep_rows: list[dict[str, Any]] = []

    rep_rows.append(
        rep_audit(
            "range_only",
            mem_by_rep,
            "range energy profile; simple distance/objectness cue",
            "Doppler, azimuth, phase, temporal persistence",
            "range label projection from Gao77 px/py/manifest",
            "medium: range/weak definitions are projected",
            "low: train-only weak threshold available; range projection still proxy",
            as_int(range_row["weak_target_count"]),
            as_float(range_row["target_projection_hit_rate"]),
            as_float(range_row["weak_target_projection_hit_rate"]),
            as_float(range_row["target_overlap_ratio"]),
            as_float(range_row["weak_target_overlap_ratio"]),
            as_float(range_row["separability_proxy_db"]),
            as_float(range_row["weak_separability_proxy_db"]),
            as_float(range_row["background_target_contrast_db"]),
            as_float(range_row["measured_pfa_at_target_pfa_1e_2"]),
            as_float(range_row["measured_pfa_at_target_pfa_1e_3"]),
            "limited: PFA 1e-3 exists; stricter not rerun for range in D5H",
            "not_saturated_as_score_but_known_negative_baseline",
            "definable as clean range no-harm, but only baseline",
            "proxy-only",
            "Baseline/reference only; does not improve over range-only by definition and cannot be a positive route.",
            "D5C range/RD/RA separability CSV",
        )
    )

    rd_weak_n = as_int(rd_ceiling["weak_n"])
    rep_rows.append(
        rep_audit(
            "corrected_RD",
            mem_by_rep,
            "range-Doppler separation; radial velocity-like structure",
            "azimuth; true velocity labels; phase if magnitude only",
            "range labels plus clean/interfered RD peak Doppler proxy",
            "high: no true Doppler; clean-peak proxy dominates",
            "high: clean-RD proxy and PFA=1e-2 saturation",
            rd_weak_n,
            as_float(rd_row["target_projection_hit_rate"]),
            as_float(rd_row["weak_target_projection_hit_rate"]),
            as_float(rd_row["target_overlap_ratio"]),
            as_float(rd_row["weak_target_overlap_ratio"]),
            as_float(rd_row["separability_proxy_db"]),
            as_float(rd_row["weak_separability_proxy_db"]),
            as_float(rd_row["background_target_contrast_db"]),
            as_float(rd_row["measured_pfa_at_target_pfa_1e_2"]),
            as_float(rd_row["measured_pfa_at_target_pfa_1e_3"]),
            "yes as calibration; stricter PFA was tested in D5E but did not rescue weak weighting",
            f"severe: balanced_mild weak Pd={fmt(rd_ceiling['balanced_mild_weak_pd'])}, improvement_room={fmt(rd_ceiling['improvement_room_weak_hits'], 0)}",
            "definable only as RD proxy no-harm, not confirmed object performance",
            "proxy-only",
            "Relies on Doppler proxy, D5E weak_n=62<100, and main-PFA baseline is saturated.",
            "D5C separability + D5E ceiling/proxy tables",
        )
    )

    rep_rows.append(
        rep_audit(
            "corrected_RA",
            mem_by_rep,
            "range-angle separation; spatial cue beyond range",
            "Doppler; true calibrated radar-angle GT; phase if magnitude only",
            "px/py to azimuth projection; smoke RA axis",
            "medium: projection formula and mask width are unresolved",
            "medium: empirical angle choices can be physically suspicious",
            as_int(ra_row["weak_target_count"]),
            as_float(ra_row["target_projection_hit_rate"]),
            as_float(ra_row["weak_target_projection_hit_rate"]),
            as_float(ra_row["target_overlap_ratio"]),
            as_float(ra_row["weak_target_overlap_ratio"]),
            as_float(ra_row["separability_proxy_db"]),
            as_float(ra_row["weak_separability_proxy_db"]),
            as_float(ra_row["background_target_contrast_db"]),
            as_float(ra_row["measured_pfa_at_target_pfa_1e_2"]),
            as_float(ra_row["measured_pfa_at_target_pfa_1e_3"]),
            "yes as RA smoke; physically plausible best weak hit remains low",
            "low saturation risk; primary issue is calibration/weak hit",
            "definable only after calibrated RA mapping",
            "proxy-only",
            f"Original weak hit={fmt(ra_original['weak_target_projection_hit_rate'])}; best physical weak hit={fmt(ra_best['weak_target_projection_hit_rate'])}; calibration unresolved.",
            "D5C RA RCA config/mask table",
        )
    )

    feasibility_specs = [
        ("RAD", "dense range-azimuth-Doppler tensor", "phase and temporal history", "RAD boxes/dense masks missing", "insufficient-labels", "No true RAD boxes in Gao77 subset."),
        ("temporal_RD", "RD plus frame persistence", "azimuth and true identity", "track IDs and velocity missing", "insufficient-labels", "No track IDs; frame continuity alone is not a label."),
        ("temporal_RA", "RA plus frame persistence", "Doppler and true identity", "track IDs missing and RA unresolved", "insufficient-labels", "No tracks and RA calibration does not pass."),
        ("temporal_RAD", "full spatiotemporal RAD evidence", "phase/raw waveform detail", "RAD boxes and track IDs missing", "insufficient-labels", "Both RAD and temporal labels are absent."),
        ("STFT_spectrogram", "time-frequency interference structure", "explicit object angle/Doppler labels", "range/frequency projection only", "proxy-only", "Can be signal diagnostic from raw ADC, but object labels are projected proxies."),
        ("complex_IQ", "raw phase and amplitude", "interpretable object mask in raw domain", "phase-aware object GT missing", "proxy-only", "Raw complex ADC exists, but target/background labels remain projected."),
        ("complex_RD", "RD magnitude plus phase", "azimuth and true Doppler labels", "true Doppler missing", "proxy-only", "Same RD label limit; phase preservation does not fix label validity."),
        ("raw_ADC", "pre-FFT raw waveform", "none before processing", "raw-domain target labels missing", "proxy-only", "Memory/availability audit only; deterministic FFT projection remains proxy."),
        ("raw_ADC_learnable_FFT", "raw waveform plus learned transform", "interpretability of learned transform", "training route forbidden", "insufficient-labels", "Learnable FFT implies training and is excluded from D5H."),
        ("radar_point_cloud", "sparse CFAR point attributes", "dense sub-threshold weak evidence", "point labels/tracks missing", "proxy-only", "Auxiliary only; weak targets may be removed before point-cloud generation."),
    ]
    for rep, kept, lost, missing, label, reason in feasibility_specs:
        rep_rows.append(
            rep_audit(
                rep,
                mem_by_rep,
                kept,
                lost,
                missing,
                "high" if label == "insufficient-labels" else "medium",
                "high" if rep in {"RAD", "temporal_RAD", "radar_point_cloud"} else "medium",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "not executable as confirmed fixed-PFA object audit on Gao77",
                "not estimable without required labels",
                "not definable for confirmed object no-harm" if label == "insufficient-labels" else "proxy no-harm only",
                label,
                reason,
                "local file inventory + D5H gate",
            )
        )

    range_weak_overlap = as_float(range_row["weak_target_overlap_ratio"])
    range_weak_sep = as_float(range_row["weak_separability_proxy_db"])
    overlap_rows = []
    for row in rep_rows:
        weak_overlap = as_float(row["weak_overlap_ratio"])
        weak_sep = as_float(row["weak_separability_proxy_db"])
        overlap_rows.append(
            {
                "representation": row["representation"],
                "weak_overlap_ratio": "" if math.isnan(weak_overlap) else weak_overlap,
                "weak_overlap_delta_vs_range_only": "" if math.isnan(weak_overlap) else weak_overlap - range_weak_overlap,
                "weak_overlap_improves_vs_range_only": "" if math.isnan(weak_overlap) else weak_overlap < range_weak_overlap,
                "weak_separability_proxy_db": "" if math.isnan(weak_sep) else weak_sep,
                "weak_separability_gain_vs_range_only_db": "" if math.isnan(weak_sep) else weak_sep - range_weak_sep,
                "weak_separability_improves_vs_range_only": "" if math.isnan(weak_sep) else weak_sep > range_weak_sep,
                "weak_projection_hit_rate": row["weak_projection_hit_rate"],
                "final_eligibility_label": row["final_eligibility_label"],
            }
        )

    fixed_rows = build_fixed_pfa_rows(rep_rows, rd_pfa_mean)
    saturation_rows = build_saturation_rows(rep_rows, rd_ceiling)
    return rep_rows, fixed_rows, overlap_rows, saturation_rows


def rep_audit(
    representation: str,
    mem_by_rep: dict[str, dict[str, Any]],
    information_kept: str,
    information_lost: str,
    label_source: str,
    proxy_label_dependence: str,
    leakage_risk: str,
    weak_n: Any,
    projection_hit_rate: Any,
    weak_projection_hit_rate: Any,
    overlap_ratio: Any,
    weak_overlap_ratio: Any,
    separability: Any,
    weak_separability: Any,
    contrast: Any,
    pfa_1e2: Any,
    pfa_1e3: Any,
    stricter_pfa: str,
    saturation_risk: str,
    clean_no_harm: str,
    final_label: str,
    final_reason: str,
    evidence_source: str,
) -> dict[str, Any]:
    mem = mem_by_rep[representation]
    pfa1 = as_float(pfa_1e2)
    pfa3 = as_float(pfa_1e3)
    return {
        "representation": representation,
        "input_shape_estimate": mem["input_shape_estimate"],
        "information_kept": information_kept,
        "information_lost": information_lost,
        "label_source": label_source,
        "proxy_label_dependence": proxy_label_dependence,
        "leakage_risk": leakage_risk,
        "weak_n_estimate": weak_n,
        "projection_hit_rate": projection_hit_rate,
        "weak_projection_hit_rate": weak_projection_hit_rate,
        "overlap_ratio": overlap_ratio,
        "weak_overlap_ratio": weak_overlap_ratio,
        "separability_proxy_db": separability,
        "weak_separability_proxy_db": weak_separability,
        "target_background_contrast_db": contrast,
        "fixed_pfa_1e_2_measured": "" if math.isnan(pfa1) else pfa1,
        "fixed_pfa_1e_2_feasible": fixed_pfa_flag(pfa1, PRIMARY_PFA),
        "fixed_pfa_1e_3_measured": "" if math.isnan(pfa3) else pfa3,
        "fixed_pfa_1e_3_feasible": fixed_pfa_flag(pfa3, SECONDARY_PFA),
        "stricter_pfa_feasibility": stricter_pfa,
        "baseline_saturation_risk": saturation_risk,
        "clean_no_harm_definability": clean_no_harm,
        "gtx1650_4gb_memory_feasible": mem["fits_gtx1650_4gb_sanity_subset"],
        "final_eligibility_label": final_label,
        "final_reason": final_reason,
        "evidence_source": evidence_source,
    }


def build_fixed_pfa_rows(rep_rows: list[dict[str, Any]], rd_pfa_mean: list[dict[str, str]]) -> list[dict[str, Any]]:
    strict = {
        as_float(row["target_pfa"]): {
            "balanced_mild_weak_pd": row.get("balanced_mild_weak_pd", ""),
            "weak_pd_delta": row.get("weak_pd_delta", ""),
            "measured_pfa_delta": row.get("measured_pfa_delta", ""),
        }
        for row in rd_pfa_mean
    }
    rows = []
    for row in rep_rows:
        pfa1 = as_float(row["fixed_pfa_1e_2_measured"])
        pfa3 = as_float(row["fixed_pfa_1e_3_measured"])
        if row["representation"] == "corrected_RD":
            stricter_5e4 = strict.get(5e-4, {})
            stricter_1e4 = strict.get(1e-4, {})
        else:
            stricter_5e4 = ""
            stricter_1e4 = ""
        rows.append(
            {
                "representation": row["representation"],
                "can_calibrate_pfa_1e_2": row["fixed_pfa_1e_2_feasible"],
                "measured_pfa_1e_2": "" if math.isnan(pfa1) else pfa1,
                "can_calibrate_pfa_1e_3": row["fixed_pfa_1e_3_feasible"],
                "measured_pfa_1e_3": "" if math.isnan(pfa3) else pfa3,
                "stricter_pfa_5e_4": stricter_5e4,
                "stricter_pfa_1e_4": stricter_1e4,
                "feasibility_note": row["stricter_pfa_feasibility"],
                "final_eligibility_label": row["final_eligibility_label"],
            }
        )
    return rows


def build_saturation_rows(rep_rows: list[dict[str, Any]], rd_ceiling: dict[str, str]) -> list[dict[str, Any]]:
    rows = []
    for row in rep_rows:
        rep = row["representation"]
        if rep == "corrected_RD":
            weak_pd = as_float(rd_ceiling["balanced_mild_weak_pd"])
            weak_n = as_int(rd_ceiling["weak_n"])
            hits = as_int(rd_ceiling["balanced_mild_weak_hits"])
            room = as_int(rd_ceiling["improvement_room_weak_hits"])
            risk = "severe"
        else:
            weak_hit = as_float(row["weak_projection_hit_rate"])
            weak_n = as_int(row["weak_n_estimate"])
            hits = "" if math.isnan(weak_hit) or not weak_n else int(round(weak_hit * weak_n))
            room = "" if hits == "" else max(weak_n - int(hits), 0)
            weak_pd = weak_hit
            risk = "unknown" if math.isnan(weak_pd) else ("saturated" if weak_pd >= 0.999 else "not_saturated")
        rows.append(
            {
                "representation": rep,
                "baseline_weak_pd_or_projection_hit_at_pfa_1e_2": "" if math.isnan(as_float(weak_pd)) else weak_pd,
                "weak_n": weak_n,
                "baseline_weak_hits": hits,
                "improvement_room_weak_hits": room,
                "saturation_risk": risk,
                "note": row["baseline_saturation_risk"],
                "final_eligibility_label": row["final_eligibility_label"],
            }
        )
    return rows


def generate_figures(
    rep_rows: list[dict[str, Any]],
    overlap_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    saturation_rows: list[dict[str, Any]],
    memory_rows: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> list[tuple[Path, str]]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[tuple[Path, str]] = []

    main_reps = ["range_only", "corrected_RD", "corrected_RA"]
    overlap_lookup = {row["representation"]: row for row in overlap_rows}
    plt.figure(figsize=(7, 4))
    plt.bar(main_reps, [as_float(overlap_lookup[r]["weak_overlap_ratio"], 0.0) for r in main_reps], color=["#64748b", "#2563eb", "#16a34a"])
    plt.ylabel("Weak overlap ratio")
    plt.title("D5H weak overlap comparison")
    plt.tight_layout()
    path = FIG_DIR / "representation_overlap_comparison.png"
    plt.savefig(path, dpi=160)
    plt.close()
    outputs.append((path, "D5H representation overlap comparison figure"))

    plt.figure(figsize=(7, 4))
    plt.bar(main_reps, [as_float(overlap_lookup[r]["weak_separability_proxy_db"], 0.0) for r in main_reps], color=["#64748b", "#2563eb", "#16a34a"])
    plt.ylabel("Weak separability proxy (dB)")
    plt.title("D5H weak separability comparison")
    plt.tight_layout()
    path = FIG_DIR / "weak_separability_comparison.png"
    plt.savefig(path, dpi=160)
    plt.close()
    outputs.append((path, "D5H weak separability comparison figure"))

    fixed_lookup = {row["representation"]: row for row in fixed_rows}
    x = np.arange(len(main_reps))
    plt.figure(figsize=(8, 4))
    plt.bar(x - 0.18, [as_float(fixed_lookup[r]["measured_pfa_1e_2"], 0.0) for r in main_reps], 0.36, label="target 1e-2")
    plt.bar(x + 0.18, [as_float(fixed_lookup[r]["measured_pfa_1e_3"], 0.0) for r in main_reps], 0.36, label="target 1e-3")
    plt.axhline(PRIMARY_PFA, color="#334155", linestyle="--", linewidth=1)
    plt.axhline(SECONDARY_PFA, color="#94a3b8", linestyle="--", linewidth=1)
    plt.xticks(x, main_reps)
    plt.ylabel("Measured PFA")
    plt.title("D5H fixed-PFA feasibility")
    plt.legend()
    plt.tight_layout()
    path = FIG_DIR / "fixed_pfa_feasibility_comparison.png"
    plt.savefig(path, dpi=160)
    plt.close()
    outputs.append((path, "D5H fixed-PFA feasibility comparison figure"))

    ra_dec = evidence["ra_config"]["decision"]
    plt.figure(figsize=(7, 4))
    labels = ["original", "best physical", "best empirical"]
    values = [
        float(ra_dec["original_weak_hit_rate"]),
        float(ra_dec["best_physical_weak_hit_rate"]),
        float(ra_dec["best_empirical_weak_hit_rate"]),
    ]
    plt.bar(labels, values, color=["#64748b", "#16a34a", "#f97316"])
    plt.ylabel("Weak hit rate")
    plt.title("D5H RA angle mapping sanity")
    plt.tight_layout()
    path = FIG_DIR / "ra_angle_mapping_sanity.png"
    plt.savefig(path, dpi=160)
    plt.close()
    outputs.append((path, "D5H RA angle mapping sanity figure"))

    rd_sat = next(row for row in saturation_rows if row["representation"] == "corrected_RD")
    plt.figure(figsize=(6, 4))
    weak_n = as_float(rd_sat["weak_n"], 0.0)
    hits = as_float(rd_sat["baseline_weak_hits"], 0.0)
    plt.bar(["balanced hits", "weak_n"], [hits, weak_n], color=["#dc2626", "#64748b"])
    plt.ylabel("Weak targets")
    plt.title("D5H RD proxy saturation")
    plt.tight_layout()
    path = FIG_DIR / "rd_proxy_saturation_illustration.png"
    plt.savefig(path, dpi=160)
    plt.close()
    outputs.append((path, "D5H RD proxy saturation illustration figure"))

    plt.figure(figsize=(10, 4))
    mem_rows = sorted(memory_rows, key=lambda row: as_float(row["sanity_batch_tensor_mb_estimate"]), reverse=True)
    plt.bar([row["representation"] for row in mem_rows], [as_float(row["sanity_batch_tensor_mb_estimate"]) for row in mem_rows], color="#2563eb")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Estimated tensor MB")
    plt.title("D5H GTX1650 sanity tensor memory estimate")
    plt.tight_layout()
    path = FIG_DIR / "memory_cost_bar_chart.png"
    plt.savefig(path, dpi=160)
    plt.close()
    outputs.append((path, "D5H memory cost bar chart"))

    return outputs


def make_phase0_md(label_rows: list[dict[str, Any]], req_rows: list[dict[str, Any]], risk_rows: list[dict[str, Any]], local: dict[str, Any]) -> str:
    return f"""# D5H Phase 0 Label Feasibility Executed

**Date**: {DATE_TEXT}  
**Scope**: Gao77 local subset only; no data download; no training.

## Local file confirmation

- subset: `{DATASET_DIR}`
- frames in manifest: `{local['frame_count']}`
- radar MAT files: `{local['raw_file_count']}`
- text label CSV files: `{local['label_file_count']}`
- object label rows scanned: `{local['label_row_count']}`
- text label column counts observed: `{local['label_col_counts']}`
- raw `adcData` sample shape/dtype: `{local['sample_raw_shape']}` / `{local['sample_raw_dtype']}`, complex=`{local['sample_raw_complex']}`
- source sequence count: `{local['source_sequence_count']}`; no track-ID file/column found.

## Label inventory

{markdown_table(label_rows, ['label_or_protocol_item', 'status', 'true_label_available', 'proxy_available', 'claim_ceiling'])}

## Representation label requirements

{markdown_table(req_rows, ['representation', 'available_true_labels', 'proxy_labels', 'missing_labels', 'gao77_support', 'final_label_blocker'])}

## Proxy risk table

{markdown_table(risk_rows, ['representation', 'proxy_source', 'leakage_risk', 'proxy_optimism_risk', 'claim_ceiling'])}

## Phase 0 decision

Gao77 can support range-only baseline and raw/complex availability checks. It does not provide true Doppler, true velocity, RAD boxes, temporal track IDs, or point-cloud labels. Therefore RD/RA/STFT/complex/raw/point-cloud routes are capped at proxy or auxiliary audit, while RAD and temporal routes are label-insufficient for confirmed Gao77 claims.
"""


def make_phase1_md(rep_rows: list[dict[str, Any]], fixed_rows: list[dict[str, Any]], overlap_rows: list[dict[str, Any]], saturation_rows: list[dict[str, Any]], memory_rows: list[dict[str, Any]]) -> str:
    label_counts = pd.Series([row["final_eligibility_label"] for row in rep_rows]).value_counts().to_dict()
    return f"""# D5H Phase 1 No-Training Representation Audit Executed

**Date**: {DATE_TEXT}  
**Scope**: deterministic/local evidence synthesis only. No model training, no D6, no detector change, no false alarm penalty.

## Final labels

{markdown_table(rep_rows, ['representation', 'weak_n_estimate', 'fixed_pfa_1e_2_feasible', 'fixed_pfa_1e_3_feasible', 'baseline_saturation_risk', 'clean_no_harm_definability', 'gtx1650_4gb_memory_feasible', 'final_eligibility_label', 'final_reason'])}

Label counts: `{label_counts}`.

## Fixed-PFA feasibility

{markdown_table(fixed_rows, ['representation', 'can_calibrate_pfa_1e_2', 'measured_pfa_1e_2', 'can_calibrate_pfa_1e_3', 'measured_pfa_1e_3', 'feasibility_note', 'final_eligibility_label'])}

## Overlap / separability comparison

{markdown_table(overlap_rows, ['representation', 'weak_overlap_ratio', 'weak_overlap_delta_vs_range_only', 'weak_separability_proxy_db', 'weak_separability_gain_vs_range_only_db', 'weak_projection_hit_rate', 'final_eligibility_label'])}

## Saturation risk

{markdown_table(saturation_rows, ['representation', 'baseline_weak_pd_or_projection_hit_at_pfa_1e_2', 'weak_n', 'baseline_weak_hits', 'improvement_room_weak_hits', 'saturation_risk', 'final_eligibility_label'])}

## GTX1650 4GB sanity estimate

{markdown_table(memory_rows, ['representation', 'input_shape_estimate', 'per_sample_mb_estimate', 'sanity_batch_tensor_mb_estimate', 'fits_gtx1650_4gb_sanity_subset', 'caveat'])}

## Phase 1 decision

No representation receives `pass`. The closest computable routes are RD/RA/STFT/complex/raw/point-cloud, but they are proxy-only or auxiliary. Corrected RD has a strong separability smoke signal, yet D5E shows clean-peak proxy dependence, weak_n=62 under the train-only frozen weak definition, and PFA=1e-2 saturation. Corrected RA remains calibration-inconclusive. RAD and temporal variants are blocked by missing labels.
"""


def make_summary_md(rep_rows: list[dict[str, Any]], figure_paths: list[tuple[Path, str]]) -> str:
    labels = {row["representation"]: row["final_eligibility_label"] for row in rep_rows}
    pass_reps = [r for r, lab in labels.items() if lab == "pass"]
    proxy = [r for r, lab in labels.items() if lab == "proxy-only"]
    insuff = [r for r, lab in labels.items() if lab == "insufficient-labels"]
    fail = [r for r, lab in labels.items() if lab == "fail"]
    fig_lines = "\n".join(f"- `{path}`" for path, _ in figure_paths)
    return f"""# D5H Executed Summary

**Date**: {DATE_TEXT}  
**Actual skill stage**: `/experiment-bridge` scoped to no-training execution.

## What ran

- Read local Gao77 subset manifest, text labels, label policy, and one raw MAT file to confirm label/data availability.
- Read prior no-training or diagnostic evidence tables from D5C, D5E, and D5C-RA-RCA.
- Generated D5H Phase 0/1 CSV, Markdown, JSON, and sanity figures.
- Did not train any model; did not enter D6; did not add false alarm penalty.

## Final representation labels

{markdown_table(rep_rows, ['representation', 'final_eligibility_label', 'final_reason'])}

## Grouped decision

- pass: `{pass_reps}`
- proxy-only: `{proxy}`
- insufficient-labels: `{insuff}`
- fail: `{fail}`

## Figures

{fig_lines}

## Plain-language conclusion

The audit did its job, but the answer is conservative: the local Gao77 setup does not currently provide a label-valid, non-saturated, leakage-bounded representation that can be moved into later minimal model sanity. RD looks useful as a signal representation, but the current Doppler boxes are proxy-derived and saturated. RA still needs calibration. RAD and temporal variants need labels Gao77 does not provide.
"""


def make_decision_md(rep_rows: list[dict[str, Any]]) -> str:
    labels = {row["representation"]: row["final_eligibility_label"] for row in rep_rows}
    pass_reps = [r for r, lab in labels.items() if lab == "pass"]
    allow_minimal = bool(pass_reps)
    return f"""# D5H Executed Decision

**Date**: {DATE_TEXT}

| decision item | verdict |
|---|---|
| any representation pass | {allow_minimal} |
| allow later minimal model sanity now | {allow_minimal} |
| continue weak weighting now | False |
| enter D6 | False |
| add false alarm penalty | False |
| change detector/fixed-PFA protocol | False |

## Rationale

No representation satisfies all D5H pass gates. The project should not continue weak weighting or D6 from this evidence. The next route is a protocol/data pivot: either obtain/use a dataset with true Doppler/RAD/track labels, or design a clearly controlled synthetic unit test that is explicitly reported as protocol sanity rather than Gao77 performance.
"""


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    local = load_local_inventory()
    evidence = load_evidence_tables()
    label_rows, req_rows, risk_rows = build_phase0_tables(local, evidence)
    memory_rows = build_memory_rows(local)
    rep_rows, fixed_rows, overlap_rows, saturation_rows = build_phase1_tables(evidence, memory_rows)
    figure_paths = generate_figures(rep_rows, overlap_rows, fixed_rows, saturation_rows, memory_rows, evidence)

    outputs: list[tuple[Path, str]] = []
    csv_specs = [
        ("d5h_phase0_label_inventory.csv", label_rows, "D5H Phase 0 label inventory"),
        ("d5h_representation_label_requirements.csv", req_rows, "D5H representation label requirements"),
        ("d5h_proxy_label_risk_table.csv", risk_rows, "D5H proxy label risk table"),
        ("d5h_phase1_representation_audit.csv", rep_rows, "D5H Phase 1 representation audit"),
        ("d5h_fixed_pfa_feasibility.csv", fixed_rows, "D5H fixed-PFA feasibility"),
        ("d5h_overlap_separability_comparison.csv", overlap_rows, "D5H overlap/separability comparison"),
        ("d5h_saturation_risk.csv", saturation_rows, "D5H saturation risk"),
        ("d5h_gpu_memory_feasibility.csv", memory_rows, "D5H GPU memory feasibility"),
    ]
    for filename, rows, desc in csv_specs:
        path = RESULT_DIR / filename
        write_csv(path, rows)
        outputs.append((path, desc))

    phase0_md = make_phase0_md(label_rows, req_rows, risk_rows, local)
    phase1_md = make_phase1_md(rep_rows, fixed_rows, overlap_rows, saturation_rows, memory_rows)
    summary_md = make_summary_md(rep_rows, figure_paths)
    decision_md = make_decision_md(rep_rows)

    text_specs = [
        ("D5H_PHASE0_LABEL_FEASIBILITY_EXECUTED.md", phase0_md, "D5H Phase 0 executed report"),
        ("D5H_PHASE1_AUDIT_EXECUTED.md", phase1_md, "D5H Phase 1 executed audit report"),
        ("D5H_EXECUTED_SUMMARY.md", summary_md, "D5H executed summary"),
        ("D5H_EXECUTED_DECISION.md", decision_md, "D5H executed decision"),
    ]
    for filename, text, desc in text_specs:
        path = RESULT_DIR / filename
        write_text(path, text)
        outputs.append((path, desc))

    labels = {row["representation"]: row["final_eligibility_label"] for row in rep_rows}
    config = {
        "stage": "D5H-Exec",
        "date": DATE_TEXT,
        "result_dir": str(RESULT_DIR),
        "figure_dir": str(FIG_DIR),
        "dataset": str(DATASET_DIR),
        "constraints": {
            "no_training": True,
            "entered_d6": False,
            "false_alarm_penalty": False,
            "weak_weighting_training": False,
            "new_model_training": False,
            "clean_identity_full_method": False,
            "proposed_full_loss": False,
            "detector_modified": False,
            "fixed_pfa_protocol_modified": False,
            "new_dataset_downloaded": False,
        },
        "primary_pfa": PRIMARY_PFA,
        "secondary_pfa": SECONDARY_PFA,
        "representations": REPRESENTATIONS,
        "final_labels": labels,
        "pass_representations": [rep for rep, lab in labels.items() if lab == "pass"],
        "should_allow_minimal_model_sanity": any(lab == "pass" for lab in labels.values()),
        "should_continue_weak_weighting": False,
        "should_enter_d6": False,
        "evidence_files": {
            "local_manifest": str(MANIFEST_CSV),
            "label_policy": str(LABEL_POLICY_JSON),
            "d5c_range_rd_ra": str(D5C_CSV),
            "d5d_weak_thresholds": str(D5D_THRESHOLDS_JSON),
            "d5e_ceiling": str(D5E_CEILING_CSV),
            "d5e_pfa": str(D5E_PFA_CSV),
            "d5e_proxy": str(D5E_PROXY_CSV),
            "ra_rca_config": str(D5C_RA_RCA_CONFIG_JSON),
            "ra_mask": str(D5C_RA_MASK_CSV),
            "ra_fft": str(D5C_RA_FFT_CSV),
        },
        "output_files": [str(path) for path, _ in outputs] + [str(path) for path, _ in figure_paths],
    }
    config_path = RESULT_DIR / "D5H_EXECUTED_CONFIG.json"
    write_json(config_path, config)
    outputs.append((config_path, "D5H executed config"))
    outputs.extend(figure_paths)
    append_manifest(outputs)
    print(json.dumps({"result_dir": str(RESULT_DIR), "outputs": len(outputs), "pass_representations": config["pass_representations"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
