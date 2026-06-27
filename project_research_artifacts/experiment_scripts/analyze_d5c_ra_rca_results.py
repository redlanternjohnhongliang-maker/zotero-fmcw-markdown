from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(r"G:\mineru_output")
RESULT_DIR = ROOT / "results" / "d5c_ra_rca_self_check"
ANALYSIS_MD = RESULT_DIR / "D5C_RA_RCA_ANALYZE_RESULTS.md"
ANALYSIS_JSON = RESULT_DIR / "D5C_RA_RCA_ANALYZE_RESULTS.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_versioned_text(path: Path, text: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_path = path.with_name(f"{path.stem}_{stamp}{path.suffix}")
    path.write_text(text, encoding="utf-8-sig")
    ts_path.write_text(text, encoding="utf-8-sig")
    return ts_path


def write_versioned_json(path: Path, data: dict[str, Any]) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_path = path.with_name(f"{path.stem}_{stamp}{path.suffix}")
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
    ts_path.write_text(text, encoding="utf-8")
    return ts_path


def f(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value in ("", None):
        return default
    return float(value)


def md_table(rows: list[dict[str, Any]], columns: list[str], max_rows: int | None = None) -> str:
    shown = rows[:max_rows] if max_rows is not None else rows
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in shown:
        vals = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                vals.append(f"{value:.4f}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def csv_inventory() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(RESULT_DIR.glob("*.csv")):
        if any(ch.isdigit() for ch in path.stem.split("_")[-1]):
            continue
        data = read_csv(path)
        rows.append(
            {
                "file": path.name,
                "row_count": len(data),
                "column_count": len(data[0]) if data else 0,
                "columns_preview": ", ".join(list(data[0].keys())[:8]) if data else "",
            }
        )
    for path in sorted(RESULT_DIR.glob("*.json")):
        if any(ch.isdigit() for ch in path.stem.split("_")[-1]):
            continue
        rows.append(
            {
                "file": path.name,
                "row_count": 1,
                "column_count": "",
                "columns_preview": "json artifact used by analysis" if path.name == "ra_rca_config.json" else "json artifact",
            }
        )
    return rows


def main() -> None:
    formula = read_csv(RESULT_DIR / "ra_label_azimuth_formula_audit.csv")
    axis = read_csv(RESULT_DIR / "ra_angle_axis_audit.csv")
    fft = read_csv(RESULT_DIR / "ra_fft_axis_audit.csv")
    masks = read_csv(RESULT_DIR / "ra_mask_width_sensitivity.csv")
    breakdown = read_csv(RESULT_DIR / "ra_projection_hit_breakdown.csv")
    consistency = read_csv(RESULT_DIR / "ra_d1a_vs_d5c_consistency.csv")
    config = json.loads((RESULT_DIR / "ra_rca_config.json").read_text(encoding="utf-8"))

    original = next(
        r
        for r in masks
        if r["candidate"] == "atan2_px_py_current"
        and r["range_mask_name"] == "default"
        and int(r["angle_total_width_bins"]) == 7
    )
    best_empirical = max(
        masks,
        key=lambda r: (
            f(r, "weak_target_projection_hit_rate"),
            f(r, "target_projection_hit_rate"),
            -f(r, "excluded_area_ratio"),
        ),
    )
    best_physical = max(
        [r for r in masks if r["candidate"] == "atan2_px_py_current"],
        key=lambda r: (
            f(r, "weak_target_projection_hit_rate"),
            f(r, "target_projection_hit_rate"),
            -f(r, "excluded_area_ratio"),
        ),
    )
    formula_rank = sorted(
        formula,
        key=lambda r: (
            f(r, "d5c_fixed_pfa_weak_projection_hit_rate"),
            -f(r, "mean_abs_peak_angle_error_deg"),
        ),
        reverse=True,
    )
    current_formula = next(r for r in formula if r["candidate"] == "atan2_px_py_current")
    fft_row = fft[0]
    d1a_prior = next(r for r in consistency if r["source"] == "D1A+ prior ra_projection_sanity.csv")
    d1a_weak = next(
        r
        for r in consistency
        if r["source"] == "D5C-RCA recomputed D1A-style"
        and r["target_scope"] == "D5C test split / weak targets"
    )
    d5c_prior = next(r for r in consistency if r["source"] == "D5C prior d5c_range_rd_ra_separability.csv")

    current_breakdown = [
        r
        for r in breakdown
        if r["candidate"] == "atan2_px_py_current"
        and r["range_mask_name"] == "default"
        and int(r["angle_total_width_bins"]) == 7
    ]
    physical_angle_sweep = [
        r for r in masks if r["candidate"] == "atan2_px_py_current" and r["range_mask_name"] == "default"
    ]
    physical_angle_sweep = sorted(physical_angle_sweep, key=lambda r: int(r["angle_total_width_bins"]))

    findings = [
        {
            "id": "F1",
            "observation": (
                f"Original D5C RA weak fixed-PFA hit rate was reproduced exactly: "
                f"{f(original, 'weak_target_projection_hit_rate'):.6f}."
            ),
            "interpretation": "The 0.0305 number is not a dead-code artifact; it follows from the implemented fixed-PFA RA path.",
            "implication": "Do not dismiss the prior D5C RA result as a logging bug.",
            "next_step": "Keep the original D5C RA row as the aligned baseline for any rerun.",
        },
        {
            "id": "F2",
            "observation": (
                f"D1A+ local RA projection hit rate was {f(d1a_prior, 'hit_rate'):.6f}; "
                f"on the D5C weak test subset, D1A-style hit rate was {f(d1a_weak, 'hit_rate'):.6f}, "
                f"while D5C fixed-PFA weak hit rate was {f(d5c_prior, 'hit_rate'):.6f}."
            ),
            "interpretation": "Most of the 0.8763 vs 0.0305 gap is criterion/scope: local contrast sanity vs weak-only fixed-PFA thresholding.",
            "implication": "The old D1A+ number cannot be used to claim D5C RA fixed-PFA success.",
            "next_step": "Report both criteria side by side in any follow-up.",
        },
        {
            "id": "F3",
            "observation": (
                f"`atan2(px, py)` is the only formula matching the manifest FOV and has lower mean angle error "
                f"({f(current_formula, 'mean_abs_peak_angle_error_deg'):.2f} deg) than empirical alternatives that increase weak hits."
            ),
            "interpretation": "No physically justified sign, coordinate, or degrees/radians bug is established.",
            "implication": "Do not switch to `atan2(py, px)`, sign flip, radians misuse, or unshifted bins just because a sweep row is higher.",
            "next_step": "If RA is revisited, calibrate the angle axis physically before changing mapping.",
        },
        {
            "id": "F4",
            "observation": (
                f"Best physically plausible mask row improves weak hit rate only to "
                f"{f(best_physical, 'weak_target_projection_hit_rate'):.6f}; best empirical row reaches "
                f"{f(best_empirical, 'weak_target_projection_hit_rate'):.6f} but has mean angle error "
                f"{f(best_empirical, 'mean_abs_peak_angle_error_deg'):.2f} deg."
            ),
            "interpretation": "RA is mask-sensitive, but the improvement is not a clean restoration of projection quality.",
            "implication": "RA remains inconclusive; a wider mask is not enough to claim a bug fix.",
            "next_step": "Prioritize RD; keep RA only as optional calibrated smoke follow-up.",
        },
        {
            "id": "F5",
            "observation": (
                f"Raw ADC shape is {fft_row['raw_adc_shape']}; angle FFT uses axis {fft_row['angle_fft_axis_in_range_virt']} "
                f"after RX/TX concatenation into {fft_row['virtual_array_shape_after_tx_concat']}."
            ),
            "interpretation": "No sample/chirp axis mix-up was found, but the RA map is still a rough virtual-array smoke map.",
            "implication": "RA evidence should be qualified as smoke-only because no TDM-MIMO phase compensation/calibration is shown.",
            "next_step": "Do not use RA for method claims without a separate calibrated RA validation.",
        },
    ]

    analysis = {
        "date": datetime.now().isoformat(),
        "skill": "/analyze-results",
        "input_dir": str(RESULT_DIR),
        "eval_type": config.get("eval_type", "diagnostic_proxy"),
        "csv_inventory": csv_inventory(),
        "key_rows": {
            "original": original,
            "best_physical": best_physical,
            "best_empirical": best_empirical,
        },
        "decision_from_config": config.get("decision", {}),
        "findings": findings,
        "overall_interpretation": "RA low hit rate is mainly a fixed-PFA/scope/mask-sensitivity issue, not a proven angle-coordinate bug.",
        "recommended_route": "Keep RA inconclusive and prioritize RD-only supplementary work; do not enter D6.",
    }

    md = f"""# D5C-RA-RCA Analyze Results

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

输入目录：`{RESULT_DIR}`

Evaluation type：`{analysis['eval_type']}`

## 1. Raw CSV Inventory

{md_table(analysis['csv_inventory'], ['file', 'row_count', 'column_count', 'columns_preview'])}

## 2. Formula Ranking

{md_table(formula_rank, ['candidate', 'formula', 'unit_mode', 'bin_mode', 'axis_sign', 'within_minus90_to_90_ratio', 'd1a_style_projection_hit_rate_all_frames', 'd5c_fixed_pfa_weak_projection_hit_rate', 'mean_abs_peak_angle_error_deg'])}

## 3. Physically Consistent Angle Width Sweep

{md_table(physical_angle_sweep, ['range_mask_name', 'angle_total_width_bins', 'target_projection_hit_rate', 'weak_target_projection_hit_rate', 'target_overlap_ratio', 'weak_target_overlap_ratio', 'excluded_area_ratio', 'mean_abs_peak_angle_error_deg'])}

## 4. Original Weak/Mid/Strong Breakdown

{md_table(current_breakdown, ['subset', 'target_count', 'hit_count', 'projection_hit_rate', 'overlap_ratio', 'mean_contrast_db', 'mean_abs_peak_angle_error_deg'])}

## 5. D1A+ vs D5C Consistency

{md_table(consistency, ['source', 'target_scope', 'hit_criterion', 'candidate', 'formula', 'bin_mode', 'range_mask', 'angle_mask_total_width_bins', 'target_count', 'hit_rate', 'notes'])}

## 6. Key Findings

"""
    for item in findings:
        md += f"""### {item['id']}

- Observation: {item['observation']}
- Interpretation: {item['interpretation']}
- Implication: {item['implication']}
- Next step: {item['next_step']}

"""
    md += f"""## 7. Overall Interpretation

{analysis['overall_interpretation']}

## 8. Recommended Route

{analysis['recommended_route']}
"""

    md_ts = write_versioned_text(ANALYSIS_MD, md)
    json_ts = write_versioned_json(ANALYSIS_JSON, analysis)
    print(
        json.dumps(
            {
                "analysis_md": str(ANALYSIS_MD),
                "analysis_md_timestamped": str(md_ts),
                "analysis_json": str(ANALYSIS_JSON),
                "analysis_json_timestamped": str(json_ts),
                "recommended_route": analysis["recommended_route"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
