# D5D Experiment Audit Report

**Date**: 2026-06-27  
**Auditor**: Codex subagent, xhigh, read-only file audit  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Trace**: `G:\mineru_output\.aris\traces\experiment-audit\2026-06-27_run02`

## Overall Verdict: WARN

## Integrity Status: warn

The D5D run is internally consistent and obeys the pre-registered D5D constraints, but the evidence type is `mixed_proxy`: GAO77 labels provide range/object targets, while RD Doppler boxes are projected from the clean RD peak within each labeled range interval. The result can support only a limited RD-only supplementary proxy sanity conclusion, not confirmed RD performance.

## Checks

### A. Ground Truth Provenance: WARN

Evidence: `experiments\d1a_gao77_clean_fixed_pfa_sanity.py:125`, `experiments\d5d_rd_only_supplementary.py:313`, `results\d5d_rd_only_supplementary\d5d_rd_config.json`, `experiments\d1b_gao77_synthetic_interference_sanity.py:141`.

Dataset labels provide range/object targets and ADC data generates radar maps. RD Doppler boxes are proxy-derived from the clean RD peak inside a label range interval. This is explicitly labeled as no Doppler GT / supplementary sanity. No model outputs are used as ground truth. Synthetic FMCW-like interference is honestly labeled as synthetic/sanity.

### B. Weak Threshold Leakage: PASS

Evidence: `experiments\d5d_rd_only_supplementary.py:166`, `results\d5d_rd_only_supplementary\d5d_rd_weak_thresholds.json`, `results\d5d_rd_only_supplementary\D5D_ANALYZE_RESULTS.md`.

Weak/mid/strong thresholds are computed from train-frame target peaks only. The reported flags are `threshold_leakage=false` and `used_test_clean_map_property_for_threshold=false`.

### C. Fixed-PFA Protocol: PASS

Evidence: `experiments\d5d_rd_only_supplementary.py:783`, `results\d5d_rd_only_supplementary\d5d_rd_eval_metrics.csv`, `results\d5d_rd_only_supplementary\d5d_rd_fixed_pfa_smoke.csv`.

Calibration thresholds come from validation background cells. Test PFA and false alarms are measured on test background cells. Raw threshold, measured PFA, false alarm, TP/FP/FN, and Pd values are saved.

### D. Baseline And Method Constraints: PASS

Evidence: `experiments\d5d_rd_only_supplementary.py:41`, `experiments\d5d_rd_only_supplementary.py:542`, `results\d5d_rd_only_supplementary\d5d_rd_config.json`, `results\d5d_rd_only_supplementary\d5d_rd_training_summary.csv`.

The main baseline is `balanced_mild`; weak weighting uses `weak_weight=2.0` and `lambda_rec=0.5`. The config records no D6, no false alarm penalty, no clean identity full method, no proposed full loss, no detector modification, no larger model, and no RA mainline.

### E. Score Normalization / Metric Validity: PASS

Evidence: `experiments\d5d_rd_only_supplementary.py:396`, `experiments\d5d_rd_only_supplementary.py:783`, `results\d5d_rd_only_supplementary\d5d_rd_eval_metrics.csv`, `results\d5d_rd_only_supplementary\d5d_rd_reconstruction_metrics.csv`.

The code uses standard mean/std normalization for tensor training and inference, not metric normalization by model-output extrema. Raw PFA, false alarm, hit, Pd, and reconstruction metrics are reported. Metric functions are called and outputs are saved.

### F. Result File Existence And Consistency: PASS

Evidence: `experiments\d5d_rd_only_supplementary.py:1451`, `results\d5d_rd_only_supplementary\d5d_rd_summary.md`, `results\d5d_rd_only_supplementary\D5D_ANALYZE_RESULTS.md`.

Required CSV/JSON/Markdown artifacts exist, and all six requested figures are present. Claimed smoke, seed, mean/std, and NO-GO numbers match CSV/JSON to displayed rounding. No substantive numeric mismatch was found.

### G. Scope And Claim Strength: WARN

Evidence: `experiments\d5d_rd_only_supplementary.py:41`, `results\d5d_rd_only_supplementary\d5d_rd_summary.md`, `results\d5d_rd_only_supplementary\D5D_ANALYZE_RESULTS.json`, `refine-logs\EXPERIMENT_TRACKER.md`.

Actual scope is 2 seeds, 96 train / 96 validation / 96 test frames, RD-only, medium-SIR eval, synthetic interference, and proxy RD boxes. Scope language is mostly honest and the final route obeys NO-GO, but any claim must remain proxy/sanity/limited.

## Evaluation Type

`mixed_proxy`

## Action Items

- Keep D5D claims limited to RD-only supplementary proxy sanity.
- Do not enter D6 from these results.
- Require true Doppler/velocity GT or a stronger pre-registered RD localization protocol before any real RD-performance claim.

## Claim Impact

- Supported: D5D ran end-to-end fixed-PFA RD proxy sanity and produced a no-gain result.
- Needs qualifier: any RD weak-target statement must mention range labels plus clean-RD Doppler projection, synthetic interference, 2 seeds, and limited scope.
- Unsupported: confirmed RD performance, robust weak-target improvement, or any GO-to-D6 claim.

## Numeric Mismatches

No substantive numeric mismatches found.
