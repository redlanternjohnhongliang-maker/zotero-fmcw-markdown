# Experiment Audit Report

**Date**: 2026-06-27  
**Auditor**: independent Codex subagent, xhigh reasoning  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Scope**: `G:\mineru_output\results\d5b_d5c_weak_definition_rdra_diagnosis`

## Overall Verdict: WARN

## Integrity Status: warn

## Checks

### A. Ground Truth Provenance: WARN
Targets come from GAO77 radar files and label files, not model outputs. However, weak definitions are clean-map-derived proxy strata, and D5C is explicitly clean-map projection smoke without precise RD/RA ground truth.

Evidence: `experiments\d1b_gao77_synthetic_interference_sanity.py:73-126`, `experiments\d1b_gao77_synthetic_interference_sanity.py:166-173`, `experiments\d1b_gao77_synthetic_interference_sanity.py:198-222`, `experiments\d1b_gao77_synthetic_interference_sanity.py:490-515`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5c_range_rd_ra_separability.csv:2-4`.

### B. Score Normalization: PASS
No misleading normalization by the model output's own max/min/mean was found. PFA/Pd/F1 use counts or validation quantiles; reconstruction metrics compare raw dB/power arrays to clean references.

Evidence: `experiments\d2a_gao77_small_model_sanity.py:505-535`, `experiments\d3_gao77_baseline_sanity.py:399-410`, `experiments\d2a_gao77_small_model_sanity.py:246-259`.

### C. Result File Existence: PASS
All audited D5B-D5C files exist. CSV inventory matches analyze JSON; summary and decision numbers match the CSV rows.

Evidence: `results\d5b_d5c_weak_definition_rdra_diagnosis\D5B_D5C_ANALYZE_RESULTS.json:5-65`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_summary.md:30`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_summary.md:37`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_repaired_definition_results.csv:2`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_decision_rows.csv:2-4`.

### D. Dead Code / Metric Code: PASS
The key metric paths are called into the generated outputs: fixed-PFA evaluation, reconstruction metrics, repaired-result rows, RD/RA smoke rows, and decision rows.

Evidence: `experiments\d2a_gao77_small_model_sanity.py:469-577`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:1103-1112`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:1113`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:1114-1116`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:1118-1146`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:1147`.

### E. Wrong Baseline: PASS
D5B-D5C uses `balanced_mild`, not MSE, as the primary baseline. MSE is used only as a reconstruction / clean no-harm guardrail.

Evidence: `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:367-381`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:405-432`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_summary.md:9`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:394-398`.

### F. PFA Threshold Leakage: PASS
Fixed-PFA thresholds are calibrated on validation background and measured on test background. No test-background threshold calibration was found.

Evidence: `experiments\d2a_gao77_small_model_sanity.py:505-535`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:477-487`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:607-613`.

### G. Weak Target Split Leakage: WARN
Weak/mid/strong splits are derived globally from clean target values before train/test usage; D5B extends context splits across all targets before training/evaluation. This limits claim scope because test clean-map properties help define the evaluated weak stratum.

Evidence: `experiments\d1b_gao77_synthetic_interference_sanity.py:490-515`, `experiments\d5b_d5c_weak_definition_rdra_diagnosis.py:1030-1034`, `experiments\d5_gao77_weak_target_weighted_sanity.py:185-190`.

### H. Mask / Non-overlap Consistency: WARN
Reported consistency fields match CSVs, but one repaired definition is mask-inconsistent and has PFA/false-alarm increase. Non-overlap consistency is reported as OK for D5B rows.

Evidence: `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_repaired_definition_results.csv:7`, `results\d5b_d5c_weak_definition_rdra_diagnosis\D5B_D5C_ANALYZE_RESULTS.md:73-76`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_repaired_definition_results.csv:2-7`.

### I. Claim Scope: WARN
D5B-D5C reports are mostly conservative, but prior D5 consistency is weak: D5-check found only +1 hit and negative 3-seed mean gain; D5-diagnosis reports overlap contamination and no D6.

Evidence: `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_summary.md:5`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_summary.md:12-13`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_go_nogo_decision.md:15-18`, `results\d5b_d5c_weak_definition_rdra_diagnosis\d5b_d5c_config.json:41-48`, `refine-logs\D5_CHECK_IMPROVEMENT_SIGNIFICANCE_REPORT.md:11-21`, `refine-logs\D5_CHECK_IMPROVEMENT_SIGNIFICANCE_REPORT.md:29-32`, `refine-logs\D5_CHECK_IMPROVEMENT_SIGNIFICANCE_REPORT.md:53-58`, `refine-logs\D5_DIAGNOSIS_WEAK_WEIGHTING_FAILURE_REPORT.md:13-18`.

## Evaluation Type Classification

- D5B range-only evaluation: `synthetic_proxy`, using real GAO77 projected labels plus synthetic ADC interference.
- Weak target definitions: `self_supervised_proxy` / clean-map-derived difficulty strata.
- D5C RD/RA: `synthetic_proxy` smoke only; RD lacks Doppler GT, RA uses rough label azimuth projection.
- Not a `real_gt` evaluation of real interference suppression or confirmed RD/RA performance.

## Action Items

1. Mark D5B-D5C claims as proxy/smoke only; do not claim confirmed improvement or D6 readiness.
2. Recompute weak definitions using train-only or pre-registered thresholds, then apply frozen definitions to validation/test.
3. Require multi-seed and split robustness before treating the original clean-peak gain as real.
4. For RD/RA, obtain independent Doppler/angle labels or keep all statements as projection-feasibility only.
5. Update tracker/logs so the older D5 “enter D6” recommendation is clearly superseded by D5-check, D5-diagnosis, and D5B-D5C NO-GO.

## Claim Impact

- D5B-D5C result-file integrity: supported.
- Range-only weak weighting improvement: weak diagnostic evidence only.
- Repaired weak definitions improving weak weighting: unsupported.
- RD follow-up: smoke-feasibility only, not confirmed RD improvement.
- RA follow-up: inconclusive smoke evidence.
- D6 readiness: unsupported / NO-GO.
