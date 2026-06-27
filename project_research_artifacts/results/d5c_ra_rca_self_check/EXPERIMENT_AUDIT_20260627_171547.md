# Experiment Audit Report

**Date**: 2026-06-27  
**Auditor**: independent Codex subagent `Lagrange`, xhigh reasoning  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Scope**: `G:\mineru_output\results\d5c_ra_rca_self_check`

## Overall Verdict: WARN

## Integrity Status: warn

## Evaluation Type

`diagnostic_proxy`

This is a label-projection / mask / mapping smoke diagnostic. It is not calibrated RA performance, not real interference suppression, and not evidence that weak-target weighting succeeds.

## Checks

### A. Ground Truth / Proxy Provenance: WARN

Targets come from GAO77 dataset label files via `parse_label_file`; range/azimuth are computed from label `px, py`. No model outputs are used as target labels. However, weak/mid/strong strata are clean-map-derived proxy strata, and RA targets are label projections into a rough RA smoke map rather than calibrated angle ground truth.

Evidence: `experiments\d2a_gao77_small_model_sanity.py:98-132`, `experiments\d5c_ra_rca_self_check.py:180-217`, `experiments\d5c_ra_rca_self_check.py:237-252`, `experiments\d1a_plus_mask_stress_test.py:166-180`.

### B. Score Normalization: WARN

Fixed-PFA metrics are mechanically valid: thresholds are validation-background quantiles, measured PFA is false alarms divided by background cells, and hit rates use target-count denominators. The warning is that D1A-style RA projection is self-thresholded by each RA frame's percentile and local contrast, so it must remain a local projection sanity metric.

Evidence: `experiments\d5c_ra_rca_self_check.py:481-522`, `experiments\d5c_ra_rca_self_check.py:337-341`, `experiments\d1a_plus_mask_stress_test.py:584-588`.

### C. Result File Existence / Number Matching: PASS

All required result files exist, and key numbers in the Markdown/JSON reports match the CSV rows:

- Original D5C weak fixed-PFA hit rate: `0.030534351145038167`.
- D1A prior and recomputed all-target local projection hit rate: `0.8762970168612192`.
- D1A-style weak test-subset local hit rate: `0.683206106870229`.
- Best physically plausible weak hit rate: `0.09411764705882353`.
- Best empirical weak hit rate: `0.1843137254901961`.

Evidence: `ra_mask_width_sensitivity.csv`, `ra_d1a_vs_d5c_consistency.csv`, `ra_rca_summary.md`, `ra_rca_decision.md`, `ra_rca_config.json`, `D5C_RA_RCA_ANALYZE_RESULTS.md`.

### D. Dead Code / Metric Path: PASS

The metric path is live. `main()` calls fixed-PFA evaluation, sweeps 8 candidates x 3 range masks x 6 angle widths, writes all RCA CSVs, then writes summary, decision, figures, and config. Row counts match design: `144` mask rows and `864` breakdown rows.

Evidence: `experiments\d5c_ra_rca_self_check.py`, `ra_mask_width_sensitivity.csv`, `ra_projection_hit_breakdown.csv`.

### E. Scope / Claim Ceiling: PASS

The reports stay within the intended claim ceiling. They explicitly label the run as `diagnostic_proxy`, state that no model was trained and D6 was not entered, and say that higher sweep rows are not confirmed RA method performance or weak-target weighting success.

Evidence: `ra_rca_summary.md`, `ra_rca_decision.md`, `D5C_RA_RCA_ANALYZE_RESULTS.md`.

### F. RA-Specific Checks: WARN

The RCA covers formula/unit/sign/bin hypotheses, FFT axis, RX/virtual antenna axis, mask width, weak subset, and D1A-vs-D5C criterion alignment. Warnings remain: the RA map is explicitly a smoke map without TDM-MIMO phase compensation, the current linear shifted-sin axis differs from exact FFT-bin geometry, and the best empirical unshifted-bin row has much larger angle error. These warnings support RA inconclusive, not a fix.

Evidence: `ra_label_azimuth_formula_audit.csv`, `ra_angle_axis_audit.csv`, `ra_fft_axis_audit.csv`, `ra_mask_width_sensitivity.csv`, `ra_d1a_vs_d5c_consistency.csv`.

## Action Items

1. Add explicit `eval_type: diagnostic_proxy` to reports/config. **Applied.**
2. Add `candidate` and `bin_mode` to the D1A-vs-D5C consistency table. **Applied.**
3. Do not use `0.876297` or `0.683206` as fixed-PFA RA success. **Enforced in analysis text.**
4. Require calibrated RA validation before any RA performance claim. **Recorded as claim ceiling.**

## Claim Impact

Can claim:

- The prior D5C RA weak fixed-PFA value was reproduced.
- The D1A/D5C gap is largely criterion/scope: local contrast sanity vs weak-only fixed-PFA thresholding.
- No clear physical angle-coordinate bug is established.
- RA remains mask-sensitive and inconclusive.

Cannot claim:

- Confirmed RA method performance.
- Weak-target weighting success.
- Physical RA calibration correctness.
- That the empirical unshifted-bin row is a valid fix.

