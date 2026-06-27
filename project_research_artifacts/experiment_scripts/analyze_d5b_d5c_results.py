from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(r"G:\mineru_output")
RESULT_DIR = ROOT / "results" / "d5b_d5c_weak_definition_rdra_diagnosis"
ANALYSIS_MD = RESULT_DIR / "D5B_D5C_ANALYZE_RESULTS.md"
ANALYSIS_JSON = RESULT_DIR / "D5B_D5C_ANALYZE_RESULTS.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_versioned(path: Path, text: str) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_path = path.with_name(f"{path.stem}_{stamp}{path.suffix}")
    ts_path.write_text(text, encoding="utf-8-sig")
    path.write_text(text, encoding="utf-8-sig")
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


def md_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for row in rows:
        vals = []
        for col in cols:
            val = row.get(col, "")
            if isinstance(val, float):
                vals.append(f"{val:.4f}")
            else:
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
    weak_audit = read_csv(RESULT_DIR / "d5b_weak_definition_audit.csv")
    repaired = read_csv(RESULT_DIR / "d5b_repaired_definition_results.csv")
    d5c = read_csv(RESULT_DIR / "d5c_range_rd_ra_separability.csv")
    decision = read_csv(RESULT_DIR / "d5b_d5c_decision_rows.csv")
    csv_summary = summarize_csvs()

    done = [r for r in repaired if r.get("status") == "DONE"]
    repaired_only = [r for r in done if r["definition"] != "clean_peak_percentile"]
    best_all = max(done, key=lambda r: (f(r, "weak_pd_delta"), i(r, "weak_hit_delta")))
    best_repaired = max(repaired_only, key=lambda r: (f(r, "weak_pd_delta"), i(r, "weak_hit_delta")))
    failing_repaired = [
        r
        for r in repaired_only
        if f(r, "weak_pd_delta") < 0.02 or i(r, "weak_hit_delta") < 5
    ]
    mask_inconsistent = [r for r in done if str(r.get("default_vs_narrow_mask_consistency")) != "True"]
    non_overlap_inconsistent = [r for r in done if str(r.get("all_vs_non_overlap_consistency")) != "True"]
    pfa_or_fa_increase = [
        r
        for r in done
        if f(r, "measured_pfa_delta") > 0 or i(r, "false_alarm_count_delta") > 0
    ]
    rd = next(r for r in d5c if r["representation"] == "RD")
    ra = next(r for r in d5c if r["representation"] == "RA")
    range_only = next(r for r in d5c if r["representation"] == "range_only")

    findings = [
        {
            "id": "F1",
            "observation": (
                f"Only the original clean_peak_percentile row crosses the weak-weighting bar: "
                f"weak Pd delta {f(best_all, 'weak_pd_delta'):.4f}, hit delta {i(best_all, 'weak_hit_delta')}."
            ),
            "interpretation": "The apparent gain is tied to the original overlap-contaminated definition, not to a repaired definition.",
            "implication": "Do not claim repaired weak definition gives stable weak-target weighting benefit.",
            "next_step": "Treat original clean_peak result as a diagnostic upper bound and validate repaired definitions before any continuation.",
        },
        {
            "id": "F2",
            "observation": (
                f"Best repaired row is {best_repaired['definition']} with weak Pd delta "
                f"{f(best_repaired, 'weak_pd_delta'):.4f} and hit delta {i(best_repaired, 'weak_hit_delta')}; "
                f"{len(failing_repaired)}/{len(repaired_only)} repaired rows miss the minimum gain or hit-count bar."
            ),
            "interpretation": "Repairing overlap reduces contamination but also removes the only bar-clearing weak-weighting gain.",
            "implication": "Range-only weak weighting remains weak evidence / negative-result leaning under repaired definitions.",
            "next_step": "Record the range-only result conservatively and avoid D6.",
        },
        {
            "id": "F3",
            "observation": (
                f"RD smoke reduces weak overlap from {f(range_only, 'weak_target_overlap_ratio'):.4f} to "
                f"{f(rd, 'weak_target_overlap_ratio'):.4f} and raises weak separability proxy by "
                f"{f(rd, 'weak_separability_gain_vs_range_db'):.2f} dB."
            ),
            "interpretation": "RD gives the clearest feasibility signal for better separability, but this is a smoke proxy without Doppler ground-truth labels.",
            "implication": "RD can justify a narrow feasibility follow-up, not a confirmed method claim.",
            "next_step": "Run a small RD representation confirmation audit before any training-scale decision.",
        },
        {
            "id": "F4",
            "observation": (
                f"RA reduces weak overlap to {f(ra, 'weak_target_overlap_ratio'):.4f}, but weak projection hit rate is "
                f"{f(ra, 'weak_target_projection_hit_rate'):.4f}, below range-only {f(range_only, 'weak_target_projection_hit_rate'):.4f}."
            ),
            "interpretation": "RA geometry can separate overlaps but current rough angle projection misses many weak targets.",
            "implication": "RA is feasibility evidence only and weaker than RD for next-step priority.",
            "next_step": "Keep RA as secondary smoke unless angle-label calibration is improved.",
        },
    ]

    analysis = {
        "date": datetime.now().isoformat(),
        "skill": "/analyze-results",
        "input_dir": str(RESULT_DIR),
        "csv_summary": csv_summary,
        "best_all_definition": best_all,
        "best_repaired_definition": best_repaired,
        "mask_inconsistent_definitions": [r["definition"] for r in mask_inconsistent],
        "non_overlap_inconsistent_definitions": [r["definition"] for r in non_overlap_inconsistent],
        "pfa_or_false_alarm_increase_definitions": [r["definition"] for r in pfa_or_fa_increase],
        "findings": findings,
        "overall_interpretation": "repaired weak definitions do not robustly support continuing range-only weak weighting; RD has smoke-only feasibility evidence.",
        "recommended_route": "record range-only weak weighting as negative/weak evidence; optionally run a narrow RD feasibility confirmation; do not enter D6.",
    }

    md = f"""# D5B-D5C Analyze Results

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

输入目录：`{RESULT_DIR}`

## 1. Raw CSV Inventory

{md_table(csv_summary, ['file', 'row_count', 'column_count', 'columns_preview'])}

## 2. Delta vs balanced_mild

{md_table(done, ['definition', 'weak_n', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta', 'clean_input_no_harm', 'default_vs_narrow_mask_consistency', 'all_vs_non_overlap_consistency'])}

## 3. RD/RA Smoke

{md_table(d5c, ['representation', 'weak_target_projection_hit_rate', 'weak_target_overlap_ratio', 'weak_separability_proxy_db', 'weak_separability_gain_vs_range_db', 'weak_projection_hit_delta_vs_range', 'fixed_pfa_calibration_sanity', 'supports_followup_rdra_training'])}

## 4. Key Findings

"""
    for item in findings:
        md += f"""### {item['id']}

- Observation: {item['observation']}
- Interpretation: {item['interpretation']}
- Implication: {item['implication']}
- Next step: {item['next_step']}

"""
    md += f"""## 5. Noise / Robustness Flags

- Small hit-count noise: repaired rows top out at +{i(best_repaired, 'weak_hit_delta')} hits, below the +5 bar.
- Mask inconsistency: {', '.join([r['definition'] for r in mask_inconsistent]) or 'none'}.
- All vs non-overlap inconsistency: {', '.join([r['definition'] for r in non_overlap_inconsistent]) or 'none'}.
- PFA or false alarm increase: {', '.join([r['definition'] for r in pfa_or_fa_increase]) or 'none'}.

## 6. Recommended Route

{analysis['recommended_route']}
"""

    md_ts = write_versioned(ANALYSIS_MD, md)
    json_ts = ANALYSIS_JSON.with_name(f"{ANALYSIS_JSON.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ANALYSIS_JSON.suffix}")
    json_text = json.dumps(analysis, ensure_ascii=False, indent=2)
    json_ts.write_text(json_text, encoding="utf-8")
    ANALYSIS_JSON.write_text(json_text, encoding="utf-8")

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
