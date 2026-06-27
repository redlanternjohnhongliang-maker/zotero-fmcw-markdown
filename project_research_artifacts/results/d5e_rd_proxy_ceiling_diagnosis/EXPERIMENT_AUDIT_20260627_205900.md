# D5E Experiment Audit Report

**Date**: 2026-06-27  
**Auditor**: Codex subagent, xhigh, read-only file audit  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Trace**: `G:\mineru_output\.aris\traces\experiment-audit\2026-06-27_run04`

## Overall Verdict: WARN

## Integrity Status: warn

The D5E run is internally consistent and honestly scoped as a mixed RD proxy diagnosis. The warning is not about fabricated metrics; it is about claim ceiling and audit-time handoff completeness. D5E uses GAO77 range labels plus diagnostic Doppler proxy boxes, not true Doppler/velocity ground truth, so it cannot support confirmed RD performance.

## Checks

### A. Ground Truth / Proxy Provenance: PASS

Evidence: `experiments\d1a_gao77_clean_fixed_pfa_sanity.py:125`, `experiments\d1a_gao77_clean_fixed_pfa_sanity.py:416`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:340`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_config.json:55`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_rd_proxy_ceiling_summary.md:80`.

GAO77 labels are parsed from label files and converted to range bins. D5E explicitly labels RD boxes as diagnostic proxies and states that no Doppler ground truth is available.

### B. Threshold Leakage: PASS

Evidence: `experiments\d5e_rd_proxy_ceiling_diagnosis.py:153`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:207`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_weak_thresholds.json:9`.

Weak thresholds are computed from train split target properties only. Output flags report `threshold_leakage=false` and `used_test_clean_map_property_for_threshold=false`.

### C. Fixed-PFA Protocol: PASS

Evidence: `experiments\d5e_rd_proxy_ceiling_diagnosis.py:358`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:365`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:399`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_pfa_sensitivity.csv`.

D5E calibrates thresholds from validation background scores and measures PFA/false alarms on test background cells. Raw thresholds, measured PFA, false alarm counts, hits, and Pd are saved.

### D. Mask / Proxy Diagnostics: PASS

Evidence: `experiments\d5e_rd_proxy_ceiling_diagnosis.py:629`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:795`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:1377`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_rd_mask_width_sensitivity.csv`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_rd_proxy_label_dependence.csv`.

Mask-width and proxy-label diagnostics are computed through the evaluation path and written as CSVs, not hand-filled summaries.

### E. Score Normalization / Metric Validity: PASS

Evidence: `experiments\d5e_rd_proxy_ceiling_diagnosis.py:386`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:413`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:1316`.

No evidence was found of metrics being normalized by model-output extrema. The model uses train-data mean/std for tensor preprocessing; reported metrics are raw threshold hits, Pd, PFA, and false alarm counts.

### F. Result Existence And Numeric Consistency: WARN

Evidence: `results\d5e_rd_proxy_ceiling_diagnosis\d5e_ceiling_effect_audit.csv`, `results\d5e_rd_proxy_ceiling_diagnosis\D5E_ANALYZE_RESULTS.md`, `results\d5e_rd_proxy_ceiling_diagnosis\GPT_HANDOFF_D5E.md`.

Core D5E CSV/JSON/Markdown/PNG artifacts exist and key numbers match, including mean weak Pd `1.0` and weak hit delta `0`. At audit time, `GPT_HANDOFF_D5E.md` referenced `EXPERIMENT_AUDIT.md` and `RESULT_TO_CLAIM.md` before both files had been generated. This report resolves the audit half; `RESULT_TO_CLAIM` must still be generated before final handoff.

### G. Dead Code / Metric Path: PASS

Evidence: `experiments\d5e_rd_proxy_ceiling_diagnosis.py:1375`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:1396`, `experiments\d5e_rd_proxy_ceiling_diagnosis.py:1400`.

All required diagnostic functions are called and their outputs are written.

### H. Scope And Constraints: PASS

Evidence: `results\d5e_rd_proxy_ceiling_diagnosis\d5e_rd_proxy_ceiling_summary.md:5`, `results\d5e_rd_proxy_ceiling_diagnosis\d5e_config.json:45`, `refine-logs\EXPERIMENT_TRACKER.md`.

D5E is explicitly not D6, not a larger model, and not confirmed RD performance. Config constraints forbid D6, false alarm penalty, full loss, detector changes, large model, and confirmed RD wording.

## Evaluation Type

`mixed_proxy`

## Action Items

- Generate `RESULT_TO_CLAIM.md/json` before final handoff.
- Keep all claims phrased as limited RD-proxy ceiling diagnosis, not RD ground-truth performance.
- Do not proceed to D6 from this evidence; first repair RD proxy/task difficulty or add true Doppler/velocity localization evidence.

## Claim Impact

- Supported: D5E diagnoses a ceiling effect in the current RD proxy setup.
- Supported with qualifier: weak weighting has no demonstrated advantage under this proxy diagnosis.
- Unsupported: confirmed RD performance, robust weak-target improvement, D6, false alarm penalty, or full method continuation.
