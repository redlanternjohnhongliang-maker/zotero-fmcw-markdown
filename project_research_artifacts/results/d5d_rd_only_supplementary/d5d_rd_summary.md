# D5D RD-only supplementary experiment

Generated: 2026-06-27 16:36:51

## 1. Scope

This is D5D only: RD representation, fixed-PFA calibration, train-only frozen weak definition, `balanced_mild` vs `weak_weighting_w2p0`.

Hard boundaries: no D6, no false alarm penalty, no clean identity full method, no proposed full loss, no detector modification, no large model, no RA mainline.

RD target boxes use dataset range labels plus a clean-RD peak Doppler projection. This is a constrained supplementary sanity result, not confirmed RD performance.

## 2. Frozen Weak Definition

| field | value |
|---|---:|
| train weak threshold q30 dB | 50.5937 |
| train q70 dB | 57.9233 |
| threshold target count | 226 |
| threshold leakage | False |
| used test clean-map property for threshold | False |

## 3. RD Fixed-PFA Smoke

| input_type | target_pfa | calibration_threshold | measured_pfa | weak_pd | overall_pd | false_alarm_count | validation_background_cell_count | test_background_cell_count | weak_separability_proxy_db |
|---|---|---|---|---|---|---|---|---|---|
| clean | 0.0100 | 74.0336 | 0.0098 | 1.0000 | 1.0000 | 29187.0000 | 2969203.0000 | 2972523.0000 | 32.4174 |
| clean | 0.0010 | 94.1625 | 0.0011 | 0.6129 | 0.8894 | 3129.0000 | 2969203.0000 | 2972523.0000 | 32.4174 |
| interfered_medium | 0.0100 | 77.9391 | 0.0098 | 1.0000 | 1.0000 | 29047.0000 | 2969203.0000 | 2972523.0000 | 32.4174 |
| interfered_medium | 0.0010 | 94.9424 | 0.0010 | 0.5484 | 0.8553 | 3084.0000 | 2969203.0000 | 2972523.0000 | 32.4174 |

## 4. Seed Summary

| seed | weak_n | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta | clean_no_harm_pass | default_vs_narrow_mask_consistency | all_vs_non_overlap_consistency | pfa_1e3_weak_pd_delta |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 42.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -57.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 |
| 200.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -26.0000 | 1.0000 | 1.0000 | 1.0000 | -0.0323 |

## 5. Mean / Std

| metric | n_seeds | mean | std | min | max |
|---|---|---|---|---|---|
| balanced_mild_weak_pd | 2.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| weak_weighting_weak_pd | 2.0000 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| weak_pd_delta | 2.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| weak_hit_delta | 2.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| measured_pfa_delta | 2.0000 | -0.0000 | 0.0000 | -0.0000 | -0.0000 |
| false_alarm_count_delta | 2.0000 | -41.5000 | 21.9203 | -57.0000 | -26.0000 |
| pfa_1e3_weak_pd_delta | 2.0000 | -0.0161 | 0.0228 | -0.0323 | 0.0000 |
| non_overlap_only_weak_pd_delta | 2.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## 6. Interpretation

Verdict: **NO-GO**.

Final route: NO-GO: do not enter D6; record RD-only result as limited/negative or weak evidence.

Mean weak Pd delta = 0.0000; mean weak hit delta = 0.00; mean PFA delta = -0.000014; mean false alarm delta = -41.50.

Failed criteria: mean_weak_pd_delta_ge_0p02, mean_weak_hit_delta_ge_5, pfa_1e3_not_reversed_all_seeds.

## 7. Output Files

| file | description |
|---|---|
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_fixed_pfa_smoke.csv | D5D RD fixed-PFA smoke |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_training_summary.csv | D5D RD training summary |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_training_loss.csv | D5D RD training loss |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_eval_metrics.csv | D5D RD fixed-PFA eval metrics |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_reconstruction_metrics.csv | D5D RD reconstruction metrics |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_seed_summary.csv | D5D RD seed summary |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_seed_mean_std.csv | D5D RD seed mean/std |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_interference_manifest.csv | D5D generated synthetic FMCW-like interference manifest |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_weak_thresholds.json | D5D train-only frozen weak thresholds |
| G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_config.json | D5D RD config |
| G:\mineru_output\gao_77ghz_raw_adc\reports\d5d_rd_only_figures\rd_weak_target_examples.png | D5D RD figure |
| G:\mineru_output\gao_77ghz_raw_adc\reports\d5d_rd_only_figures\rd_fixed_pfa_threshold_sanity.png | D5D RD figure |
| G:\mineru_output\gao_77ghz_raw_adc\reports\d5d_rd_only_figures\rd_balanced_vs_weak_weighting_weak_pd.png | D5D RD figure |
| G:\mineru_output\gao_77ghz_raw_adc\reports\d5d_rd_only_figures\rd_pfa_false_alarm_comparison.png | D5D RD figure |
| G:\mineru_output\gao_77ghz_raw_adc\reports\d5d_rd_only_figures\rd_training_loss_curve.png | D5D RD figure |
| G:\mineru_output\gao_77ghz_raw_adc\reports\d5d_rd_only_figures\rd_clean_no_harm_reconstruction_comparison.png | D5D RD figure |
