from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "results" / "d5h_representation_protocol_audit_executed"
DATE_TEXT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def append_manifest(outputs: list[tuple[Path, str]]) -> None:
    manifest = ROOT / "MANIFEST.md"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with manifest.open("a", encoding="utf-8") as fh:
        for path, desc in outputs:
            rel = path.resolve().relative_to(ROOT)
            fh.write(f"| {stamp} | /analyze-results | {rel} | implementation | {desc} |\n")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def main() -> None:
    csv_files = sorted(RESULT_DIR.glob("*.csv"))
    csv_summary = []
    for path in csv_files:
        rows = read_csv_rows(path)
        csv_summary.append(
            {
                "file": path.name,
                "rows": len(rows),
                "columns": len(rows[0]) if rows else 0,
                "column_names": list(rows[0].keys()) if rows else [],
            }
        )

    audit_rows = read_csv_rows(RESULT_DIR / "d5h_phase1_representation_audit.csv")
    label_groups: dict[str, list[str]] = {}
    final_rows = []
    for row in audit_rows:
        label = row["final_eligibility_label"]
        rep = row["representation"]
        label_groups.setdefault(label, []).append(rep)
        final_rows.append(
            {
                "representation": rep,
                "final_eligibility_label": label,
                "weak_n_estimate": row.get("weak_n_estimate", ""),
                "pfa_1e_2": row.get("fixed_pfa_1e_2_feasible", ""),
                "pfa_1e_3": row.get("fixed_pfa_1e_3_feasible", ""),
                "main_reason": row.get("final_reason", ""),
            }
        )

    any_pass = bool(label_groups.get("pass"))
    should_allow_minimal_model_sanity = any_pass
    should_enter_d6 = False
    should_continue_weak_weighting = False

    findings = [
        {
            "id": 1,
            "finding": "No representation passed the D5H gate.",
            "evidence": f"pass={label_groups.get('pass', [])}",
            "implication": "Do not allow minimal model sanity from current Gao77 evidence.",
        },
        {
            "id": 2,
            "finding": "Corrected RD is computable and separable, but still proxy-only.",
            "evidence": "D5E weak_n=62, clean/interfered RD peak proxy, and PFA=1e-2 saturation.",
            "implication": "Do not write RD proxy as confirmed RD performance.",
        },
        {
            "id": 3,
            "finding": "Corrected RA remains calibration-inconclusive.",
            "evidence": "Original weak hit rate is low and best physical RCA row remains proxy evidence.",
            "implication": "Do not treat RA as invalid; treat it as unresolved.",
        },
        {
            "id": 4,
            "finding": "RAD and temporal routes are blocked by missing labels.",
            "evidence": "No RAD boxes, no velocity labels, and no track IDs found in the local Gao77 subset.",
            "implication": "Use a label/protocol pivot rather than more training.",
        },
    ]

    result = {
        "stage": "D5H analyze-results",
        "date": DATE_TEXT,
        "result_dir": str(RESULT_DIR),
        "csv_summary": csv_summary,
        "final_rows": final_rows,
        "label_groups": {
            "pass": label_groups.get("pass", []),
            "proxy-only": label_groups.get("proxy-only", []),
            "insufficient-labels": label_groups.get("insufficient-labels", []),
            "fail": label_groups.get("fail", []),
        },
        "any_pass": any_pass,
        "should_allow_minimal_model_sanity": should_allow_minimal_model_sanity,
        "should_continue_weak_weighting": should_continue_weak_weighting,
        "should_enter_d6": should_enter_d6,
        "findings": findings,
    }

    md = f"""# D5H Analyze Results

**Date**: {DATE_TEXT}  
**Input directory**: `{RESULT_DIR}`

## CSV inventory

{markdown_table(csv_summary, ['file', 'rows', 'columns'])}

## Final eligibility by representation

{markdown_table(final_rows, ['representation', 'final_eligibility_label', 'weak_n_estimate', 'pfa_1e_2', 'pfa_1e_3', 'main_reason'])}

## Grouped labels

- pass: `{result['label_groups']['pass']}`
- proxy-only: `{result['label_groups']['proxy-only']}`
- insufficient-labels: `{result['label_groups']['insufficient-labels']}`
- fail: `{result['label_groups']['fail']}`

## Decisions

| question | answer |
|---|---|
| any pass | {any_pass} |
| allow minimal model sanity now | {should_allow_minimal_model_sanity} |
| continue weak weighting now | {should_continue_weak_weighting} |
| enter D6 | {should_enter_d6} |

## Key findings

{markdown_table(findings, ['id', 'finding', 'evidence', 'implication'])}

## 大白话解释

这轮不是训练结果分析，而是协议资格审查。结果很干净也很保守：没有任何表示同时满足“标签有效、无泄漏、weak_n 足够、PFA 可校准、不饱和、相对 range-only 有改善、clean no-harm 可定义、4GB 可做 sanity”的全部条件。当前最该做的不是继续训练，而是修标签/协议：RD 需要真 Doppler 或不泄漏的 proxy，RA 需要校准，RAD/temporal 需要有相应标注的数据。
"""

    md_path = RESULT_DIR / "D5H_ANALYZE_RESULTS.md"
    json_path = RESULT_DIR / "D5H_ANALYZE_RESULTS.json"
    write_text(md_path, md)
    write_json(json_path, result)
    append_manifest([(md_path, "D5H analyze-results report"), (json_path, "D5H analyze-results JSON")])
    print(json.dumps({"any_pass": any_pass, "label_groups": result["label_groups"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
