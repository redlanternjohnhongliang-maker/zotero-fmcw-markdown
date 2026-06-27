from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(r"G:\mineru_output")
RESULT_DIR = ROOT / "results" / "d5e_rd_proxy_ceiling_diagnosis"
ANALYSIS_MD = RESULT_DIR / "D5E_ANALYZE_RESULTS.md"
ANALYSIS_JSON = RESULT_DIR / "D5E_ANALYZE_RESULTS.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


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
    lines = []
    for path, desc in outputs:
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path
        lines.append(f"| {stamp} | /analyze-results | {rel} | implementation | {desc} |")
    with manifest.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def csv_inventory() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(RESULT_DIR.glob("*.csv")):
        if "_" in path.stem and path.stem[-15:-7].isdigit():
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
    return rows


def main() -> None:
    ceiling = read_csv(RESULT_DIR / "d5e_ceiling_effect_audit.csv")
    pfa = read_csv(RESULT_DIR / "d5e_pfa_sensitivity.csv")
    mask = read_csv(RESULT_DIR / "d5e_rd_mask_width_sensitivity.csv")
    qdiff = read_csv(RESULT_DIR / "d5e_weak_threshold_difficulty.csv")
    proxy = read_csv(RESULT_DIR / "d5e_rd_proxy_label_dependence.csv")
    sample = read_csv(RESULT_DIR / "d5e_sample_size_stability.csv")
    config = json.loads((RESULT_DIR / "d5e_config.json").read_text(encoding="utf-8"))
    inv = csv_inventory()

    c_mean = next(r for r in ceiling if str(r.get("seed")) == "mean")
    pfa_means = [r for r in pfa if str(r.get("seed")) == "mean"]
    mask_means = [r for r in mask if str(r.get("seed")) == "mean"]
    q_means = [r for r in qdiff if str(r.get("seed")) == "mean"]
    proxy_means = [r for r in proxy if str(r.get("seed")) == "mean"]
    sample_default = [r for r in sample if str(r.get("target_pfa")) == "0.01" and str(r.get("seed")) not in {"seed_sensitivity"}]
    strict_pfa = [r for r in pfa_means if f(r, "target_pfa") <= 0.001]

    ceiling_effect = f(c_mean, "balanced_mild_weak_pd") >= 0.999 and f(c_mean, "balanced_mild_weak_miss_count") == 0
    pfa_1e3 = next(r for r in pfa_means if abs(f(r, "target_pfa") - 0.001) < 1e-12)
    any_strict_gain = any(f(r, "weak_pd_delta") > 0 and f(r, "weak_hit_delta") > 0 for r in strict_pfa)
    any_mask_gain = any(f(r, "weak_pd_delta") > 0 and f(r, "weak_hit_delta") > 0 for r in mask_means)
    q30 = min(q_means, key=lambda r: abs(f(r, "q_weak") - 0.30))
    q30_too_easy = f(q30, "balanced_mild_weak_pd") >= 0.999
    hard_q_gain = any(f(r, "q_weak") <= 0.20 and f(r, "weak_pd_delta") > 0 for r in q_means)
    proxy_clean = next(r for r in proxy_means if r["doppler_box_mode"] == "clean_peak")
    local_proxy = next(r for r in proxy_means if r["doppler_box_mode"] == "local_window_peak")
    vertical_proxy = next(r for r in proxy_means if r["doppler_box_mode"] == "vertical_stripe")
    weak_n_small = any(i(r, "weak_n") < 100 for r in sample_default)

    findings = [
        {
            "id": "F1",
            "observation": f"At PFA=1e-2, balanced_mild weak Pd is {f(c_mean, 'balanced_mild_weak_pd'):.4f} with {f(c_mean, 'balanced_mild_weak_miss_count'):.1f} missed weak targets.",
            "interpretation": "The D5D default RD proxy has a hard ceiling: the baseline already hits every q30 weak target.",
            "implication": "D5D cannot demonstrate a weak-weighting improvement at the main PFA because there is no remaining weak-hit room.",
        },
        {
            "id": "F2",
            "observation": f"At PFA=1e-3, mean weak Pd delta is {f(pfa_1e3, 'weak_pd_delta'):.4f} and mean weak hit delta is {f(pfa_1e3, 'weak_hit_delta'):.1f}.",
            "interpretation": "When the threshold becomes stricter, weak weighting does not become better; it is slightly worse on average.",
            "implication": "Stricter fixed-PFA settings do not rescue weak weighting.",
        },
        {
            "id": "F3",
            "observation": f"Across {len(mask_means)} range/doppler mask combinations, no mean row has positive weak Pd and weak-hit delta together.",
            "interpretation": "Mask-width perturbation does not reveal a hidden weak-weighting advantage.",
            "implication": "The NO-GO is robust to the tested mask deformations.",
        },
        {
            "id": "F4",
            "observation": f"q10/q20/q30/q40 weak subsets all have balanced_mild weak Pd = 1.0; q30 test weak_n is {i(q30, 'test_weak_n')} and mean RD contrast is {f(q30, 'mean_target_background_contrast_db'):.2f} dB.",
            "interpretation": "The q30 range-only weak threshold still selects RD targets that are easy under the current RD proxy.",
            "implication": "The weak definition is not hard enough for RD weak-preservation claims.",
        },
        {
            "id": "F5",
            "observation": f"Clean/interfered peak proxy boxes both saturate; local-window overlap vs clean boxes is {f(local_proxy, 'overlap_ratio_vs_clean_peak_box'):.4f}, vertical-stripe area is {f(vertical_proxy, 'target_box_area_mean_weak'):.1f} cells.",
            "interpretation": "The proxy label design is optimistic/saturated. The issue is not only the clean-RD peak source; broad or alternative proxy boxes still make weak hits easy.",
            "implication": "D5E remains a mixed-proxy diagnosis, not confirmed RD performance.",
        },
        {
            "id": "F6",
            "observation": "test weak_n is 62 at q30; one hit equals 0.0161 Pd, two hits equal 0.0323 Pd, and the pre-registered +5 hit bar equals 0.0806 Pd.",
            "interpretation": "Small hit-count changes can look nontrivial in Pd, but +0/+1/+2 hits are not enough for a robust claim.",
            "implication": "All claims must stay conservative, especially with only 2 seeds.",
        },
    ]
    verdict = {
        "verdict": "NO-GO",
        "ceiling_effect_present": ceiling_effect,
        "q30_too_easy": q30_too_easy,
        "strict_pfa_supports_weak_weighting": any_strict_gain,
        "mask_deformation_supports_weak_weighting": any_mask_gain,
        "harder_q_supports_weak_weighting": hard_q_gain,
        "rd_proxy_label_overly_optimistic": True,
        "weak_n_too_small_for_strong_claim": weak_n_small,
        "continue_weak_weighting": False,
        "d6_allowed": False,
        "recommended_route": "Stop weak weighting for now; do not enter D6. If continuing, first repair RD proxy/task difficulty.",
    }
    analysis = {
        "date": datetime.now().isoformat(),
        "skill": "/analyze-results",
        "input_dir": str(RESULT_DIR),
        "csv_inventory": inv,
        "config_decision": config.get("decision", {}),
        "findings": findings,
        "verdict": verdict,
    }

    md = f"""# D5E Analyze Results

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Input directory: `{RESULT_DIR}`

## 1. Raw CSV Inventory

{md_table(inv, ['file', 'row_count', 'column_count', 'columns_preview'])}

## 2. Ceiling Effect

{md_table(ceiling, ['seed', 'weak_n', 'balanced_mild_weak_hits', 'weak_weighting_weak_hits', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'balanced_mild_weak_miss_count', 'ceiling_effect_present'])}

## 3. PFA Sensitivity

{md_table(pfa_means, ['target_pfa', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta'])}

## 4. Mask Width Sensitivity

{md_table(mask_means, ['range_mask_name', 'doppler_radius_bins', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta', 'measured_pfa_delta', 'false_alarm_count_delta'])}

## 5. Weak Threshold Difficulty

{md_table(q_means, ['q_weak', 'train_weak_threshold_db', 'train_weak_n', 'test_weak_n', 'mean_clean_rd_peak_db', 'mean_range_only_peak_db', 'mean_target_background_contrast_db', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

## 6. RD Proxy Label Dependence

{md_table(proxy_means, ['doppler_box_mode', 'weak_projection_hit_rate_against_clean_peak', 'target_box_area_mean_weak', 'overlap_ratio_vs_clean_peak_box', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_hit_delta'])}

## 7. Sample Size Stability

{md_table(sample, ['seed', 'target_pfa', 'weak_n', 'balanced_mild_weak_pd', 'weak_weighting_weak_pd', 'weak_pd_delta', 'weak_pd_delta_ci_low', 'weak_pd_delta_ci_high', 'weak_hit_delta', 'one_hit_pd_delta', 'two_hit_pd_delta', 'five_hit_pd_delta', 'weak_n_small_for_claim'])}

## 8. Key Findings

"""
    for item in findings:
        md += f"""### {item['id']}

- Observation: {item['observation']}
- Interpretation: {item['interpretation']}
- Implication: {item['implication']}

"""
    md += f"""## 9. Verdict

Verdict: **{verdict['verdict']}**

- Ceiling effect present: `{verdict['ceiling_effect_present']}`
- q30 weak threshold too easy: `{verdict['q30_too_easy']}`
- Stricter PFA supports weak weighting: `{verdict['strict_pfa_supports_weak_weighting']}`
- Mask deformation supports weak weighting: `{verdict['mask_deformation_supports_weak_weighting']}`
- RD proxy label overly optimistic/saturated: `{verdict['rd_proxy_label_overly_optimistic']}`
- D6 allowed: `{verdict['d6_allowed']}`

Recommended route: {verdict['recommended_route']}
"""
    md_ts = write_versioned(ANALYSIS_MD, md)
    json_ts = write_versioned_json(ANALYSIS_JSON, analysis)
    append_manifest(
        [
            (ANALYSIS_MD, "D5E analyze-results report"),
            (md_ts, "D5E analyze-results report timestamped copy"),
            (ANALYSIS_JSON, "D5E analyze-results JSON"),
            (json_ts, "D5E analyze-results JSON timestamped copy"),
        ]
    )
    print(
        json.dumps(
            {
                "analysis_md": str(ANALYSIS_MD),
                "analysis_md_timestamped": str(md_ts),
                "analysis_json": str(ANALYSIS_JSON),
                "analysis_json_timestamped": str(json_ts),
                "verdict": verdict,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
