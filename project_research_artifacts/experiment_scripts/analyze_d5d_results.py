from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(r"G:\mineru_output")
RESULT_DIR = ROOT / "results" / "d5d_rd_only_supplementary"
ANALYSIS_MD = RESULT_DIR / "D5D_ANALYZE_RESULTS.md"
ANALYSIS_JSON = RESULT_DIR / "D5D_ANALYZE_RESULTS.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_versioned(path: Path, text: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_path = path.with_name(f"{path.stem}_{stamp}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8-sig")
    path.write_text(text, encoding="utf-8-sig")
    return ts_path


def write_versioned_json(path: Path, obj: Any) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_path = path.with_name(f"{path.stem}_{stamp}{path.suffix}")
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    ts_path.write_text(text, encoding="utf-8")
    path.write_text(text, encoding="utf-8")
    return ts_path


def f(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key, default)
    if value in ("", None):
        return default
    return float(value)


def i(row: dict[str, Any], key: str, default: int = 0) -> int:
    value = row.get(key, default)
    if value in ("", None):
        return default
    return int(float(value))


def b(row: dict[str, Any], key: str) -> bool:
    value = row.get(key, "")
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in rows:
        vals = []
        for col in cols:
            val = row.get(col, "")
            if isinstance(val, bool):
                vals.append("True" if val else "False")
                continue
            try:
                vals.append(f"{float(val):.4f}" if val not in ("", None) else "")
            except Exception:
                vals.append(str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def summarize_csvs() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(RESULT_DIR.glob("*.csv")):
        data = read_csv(path)
        rows.append(
            {
                "file": path.name,
                "row_count": len(data),
                "column_count": len(data[0]) if data else 0,
                "columns_preview": ", ".join(list(data[0].keys())[:8]) if data else "",
            }
        )
    return rows


def main() -> None:
    smoke = read_csv(RESULT_DIR / "d5d_rd_fixed_pfa_smoke.csv")
    seed_rows = read_csv(RESULT_DIR / "d5d_rd_seed_summary.csv")
    mean_rows = read_csv(RESULT_DIR / "d5d_rd_seed_mean_std.csv")
    training = read_csv(RESULT_DIR / "d5d_rd_training_summary.csv")
    recon = read_csv(RESULT_DIR / "d5d_rd_reconstruction_metrics.csv")
    thresholds = json.loads((RESULT_DIR / "d5d_rd_weak_thresholds.json").read_text(encoding="utf-8"))
    csv_summary = summarize_csvs()

    mean_lookup = {row["metric"]: row for row in mean_rows}
    mean_gain = f(mean_lookup["weak_pd_delta"], "mean")
    mean_hit_delta = f(mean_lookup["weak_hit_delta"], "mean")
    mean_pfa_delta = f(mean_lookup["measured_pfa_delta"], "mean")
    mean_fa_delta = f(mean_lookup["false_alarm_count_delta"], "mean")
    pfa1e3_mean = f(mean_lookup["pfa_1e3_weak_pd_delta"], "mean")
    failed = []
    if mean_gain < 0.02:
        failed.append("weak Pd delta < 0.02")
    if mean_hit_delta < 5:
        failed.append("weak hit delta < +5")
    if any(not b(row, "pfa_not_increased") for row in seed_rows):
        failed.append("measured PFA increased")
    if any(not b(row, "false_alarm_not_increased") for row in seed_rows):
        failed.append("false alarm count increased")
    if any(not b(row, "clean_no_harm_pass") for row in seed_rows):
        failed.append("clean no-harm failed")
    if any(not b(row, "default_vs_narrow_mask_consistency") for row in seed_rows):
        failed.append("default/narrow mask inconsistent")
    if any(not b(row, "all_vs_non_overlap_consistency") for row in seed_rows):
        failed.append("all/non-overlap inconsistent")
    if any(not b(row, "pfa_1e3_not_reversed") for row in seed_rows):
        failed.append("PFA=1e-3 reversed")
    if thresholds.get("threshold_leakage"):
        failed.append("weak threshold leakage")

    findings = [
        {
            "id": "F1",
            "observation": f"RD fixed-PFA ran end to end at PFA=1e-2 and 1e-3; the smoke CSV has {len(smoke)} rows.",
            "interpretation": "The RD evaluation path is operational, but target boxes rely on clean-RD Doppler peak projection.",
            "implication": "This supports only a constrained RD supplementary sanity, not a confirmed RD performance claim.",
            "next_step": "Keep RD claims proxy-limited unless Doppler/velocity ground truth or a stronger target localization protocol is added.",
        },
        {
            "id": "F2",
            "observation": f"Across {len(seed_rows)} seeds, mean weak Pd delta is {mean_gain:.4f} and mean hit delta is {mean_hit_delta:.2f}.",
            "interpretation": "Weak weighting does not improve over balanced_mild; weak Pd is saturated at the main PFA in this RD projection setup.",
            "implication": "The required weak Pd >= 0.02 and +5 hit bars are not met.",
            "next_step": "Do not continue to D6 from this result.",
        },
        {
            "id": "F3",
            "observation": f"Mean PFA delta is {mean_pfa_delta:.6f}, mean false alarm delta is {mean_fa_delta:.2f}; clean no-harm passes in both seeds.",
            "interpretation": "The weak-weighting variant does not trade the missing weak gain for more PFA/FA in the main PFA setting.",
            "implication": "The negative result is due to no gain, not due to an obvious false-alarm explosion.",
            "next_step": "Record as limited/negative RD-only weak-weighting evidence.",
        },
        {
            "id": "F4",
            "observation": f"PFA=1e-3 mean weak Pd delta is {pfa1e3_mean:.4f}, with seed 200 reversed by -0.0323 weak Pd and -2 hits.",
            "interpretation": "The stricter PFA setting does not consistently support weak weighting.",
            "implication": "This independently blocks GO under the pre-registered criteria.",
            "next_step": "Any future RD follow-up must first address saturation/projection issues, not jump to D6.",
        },
    ]
    analysis = {
        "date": datetime.now().isoformat(),
        "skill": "/analyze-results",
        "input_dir": str(RESULT_DIR),
        "csv_summary": csv_summary,
        "thresholds": thresholds,
        "seed_summary": seed_rows,
        "seed_mean_std": mean_rows,
        "training_summary": training,
        "reconstruction_metrics": recon,
        "findings": findings,
        "failed_go_criteria": failed,
        "verdict": "NO-GO",
        "recommended_route": "Do not enter D6; record RD-only result as limited/negative or weak evidence.",
    }

    md = f"""# D5D Analyze Results

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Input directory: `{RESULT_DIR}`

## 1. Raw CSV Inventory

{md_table(csv_summary, ['file', 'row_count', 'column_count', 'columns_preview'])}

## 2. Frozen Weak Threshold

| item | value |
|---|---:|
| train q30 weak threshold dB | {thresholds['train_target_peak_db_q30_weak_threshold']:.4f} |
| train q70 threshold dB | {thresholds['train_target_peak_db_q70_strong_threshold']:.4f} |
| train weak_n | {thresholds['counts']['train']['weak_n']} |
| val weak_n | {thresholds['counts']['val']['weak_n']} |
| test weak_n | {thresholds['counts']['test']['weak_n']} |
| threshold leakage | {thresholds['threshold_leakage']} |
| used test property for threshold | {thresholds['used_test_clean_map_property_for_threshold']} |

## 3. Delta vs balanced_mild

{md_table(seed_rows, ['seed', 'weak_n', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta', 'clean_no_harm_pass', 'default_vs_narrow_mask_consistency', 'all_vs_non_overlap_consistency', 'pfa_1e3_weak_pd_delta'])}

## 4. Mean / Std

{md_table(mean_rows, ['metric', 'n_seeds', 'mean', 'std', 'min', 'max'])}

## 5. Fixed-PFA Smoke

{md_table(smoke, ['input_type', 'target_pfa', 'calibration_threshold', 'measured_pfa', 'weak_pd', 'overall_pd', 'false_alarm_count', 'weak_separability_proxy_db'])}

## 6. Key Findings

"""
    for item in findings:
        md += f"""### {item['id']}

- Observation: {item['observation']}
- Interpretation: {item['interpretation']}
- Implication: {item['implication']}
- Next step: {item['next_step']}

"""
    md += f"""## 7. GO / NO-GO

Verdict: **NO-GO**

Failed criteria: {', '.join(failed)}

Recommended route: {analysis['recommended_route']}
"""

    md_ts = write_versioned(ANALYSIS_MD, md)
    json_ts = write_versioned_json(ANALYSIS_JSON, analysis)
    print(
        json.dumps(
            {
                "analysis_md": str(ANALYSIS_MD),
                "analysis_md_timestamped": str(md_ts),
                "analysis_json": str(ANALYSIS_JSON),
                "analysis_json_timestamped": str(json_ts),
                "verdict": analysis["verdict"],
                "failed_go_criteria": failed,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
