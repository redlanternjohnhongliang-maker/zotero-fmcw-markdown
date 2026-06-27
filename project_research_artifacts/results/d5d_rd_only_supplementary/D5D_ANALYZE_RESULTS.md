# D5D Analyze Results

Generated: 2026-06-27 16:38:43

Input directory: `G:\mineru_output\results\d5d_rd_only_supplementary`

## 1. Raw CSV Inventory

| file | row_count | column_count | columns_preview |
|---|---|---|---|
| d5d_rd_eval_metrics.csv | 80.0000 | 42.0000 | background_cell_count, bootstrap_pfa_ci_high, bootstrap_pfa_ci_low, bootstrap_pfa_std, f1, false_alarm_count, fn_cells, fp_cells |
| d5d_rd_fixed_pfa_smoke.csv | 4.0000 | 13.0000 | calibration_threshold, false_alarm_count, input_type, measured_pfa, overall_pd, scope_note, sir_name, target_background_contrast_db |
| d5d_rd_interference_manifest.csv | 576.0000 | 8.0000 | achieved_sir_db, frame_id, frame_idx, interference_params_json, num_interferers, sir_name, source_sequence, target_sir_db |
| d5d_rd_reconstruction_metrics.csv | 10.0000 | 7.0000 | input_type, magmse_db_to_clean, method, mse_db_to_clean, mse_power_to_clean, seed, sir_name |
| d5d_rd_seed_mean_std.csv | 8.0000 | 6.0000 | max, mean, metric, min, n_seeds, std |
| d5d_rd_seed_summary.csv | 2.0000 | 45.0000 | all_targets_weak_pd_delta, all_vs_non_overlap_consistency, balanced_mild_clean_mse_db_to_clean, balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_overall_pd, balanced_mild_weak_hits, balanced_mild_weak_pd |
| d5d_rd_training_loss.csv | 52.0000 | 20.0000 | background_det_term, detection_term, epoch, grad_norm_before_clip, lambda_rec, lr, magmse_term, method |
| d5d_rd_training_summary.csv | 4.0000 | 34.0000 | final_train_background_det, final_train_detection, final_train_loss, final_train_magmse, final_train_target_det, final_val_background_det, final_val_detection, final_val_loss |

## 2. Frozen Weak Threshold

| item | value |
|---|---:|
| train q30 weak threshold dB | 50.5937 |
| train q70 threshold dB | 57.9233 |
| train weak_n | 56 |
| val weak_n | 64 |
| test weak_n | 62 |
| threshold leakage | False |
| used test property for threshold | False |

## 3. Delta vs balanced_mild

| seed | weak_n | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta | clean_no_harm_pass | default_vs_narrow_mask_consistency | all_vs_non_overlap_consistency | pfa_1e3_weak_pd_delta |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 42.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -57.0000 | True | True | True | 0.0000 |
| 200.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -26.0000 | True | True | True | -0.0323 |

## 4. Mean / Std

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

## 5. Fixed-PFA Smoke

| input_type | target_pfa | calibration_threshold | measured_pfa | weak_pd | overall_pd | false_alarm_count | weak_separability_proxy_db |
|---|---|---|---|---|---|---|---|
| clean | 0.0100 | 74.0336 | 0.0098 | 1.0000 | 1.0000 | 29187.0000 | 32.4174 |
| clean | 0.0010 | 94.1625 | 0.0011 | 0.6129 | 0.8894 | 3129.0000 | 32.4174 |
| interfered_medium | 0.0100 | 77.9391 | 0.0098 | 1.0000 | 1.0000 | 29047.0000 | 32.4174 |
| interfered_medium | 0.0010 | 94.9424 | 0.0010 | 0.5484 | 0.8553 | 3084.0000 | 32.4174 |

## 6. Key Findings

### F1

- Observation: RD fixed-PFA ran end to end at PFA=1e-2 and 1e-3; the smoke CSV has 4 rows.
- Interpretation: The RD evaluation path is operational, but target boxes rely on clean-RD Doppler peak projection.
- Implication: This supports only a constrained RD supplementary sanity, not a confirmed RD performance claim.
- Next step: Keep RD claims proxy-limited unless Doppler/velocity ground truth or a stronger target localization protocol is added.

### F2

- Observation: Across 2 seeds, mean weak Pd delta is 0.0000 and mean hit delta is 0.00.
- Interpretation: Weak weighting does not improve over balanced_mild; weak Pd is saturated at the main PFA in this RD projection setup.
- Implication: The required weak Pd >= 0.02 and +5 hit bars are not met.
- Next step: Do not continue to D6 from this result.

### F3

- Observation: Mean PFA delta is -0.000014, mean false alarm delta is -41.50; clean no-harm passes in both seeds.
- Interpretation: The weak-weighting variant does not trade the missing weak gain for more PFA/FA in the main PFA setting.
- Implication: The negative result is due to no gain, not due to an obvious false-alarm explosion.
- Next step: Record as limited/negative RD-only weak-weighting evidence.

### F4

- Observation: PFA=1e-3 mean weak Pd delta is -0.0161, with seed 200 reversed by -0.0323 weak Pd and -2 hits.
- Interpretation: The stricter PFA setting does not consistently support weak weighting.
- Implication: This independently blocks GO under the pre-registered criteria.
- Next step: Any future RD follow-up must first address saturation/projection issues, not jump to D6.

## 7. GO / NO-GO

Verdict: **NO-GO**

Failed criteria: weak Pd delta < 0.02, weak hit delta < +5, PFA=1e-3 reversed

Recommended route: Do not enter D6; record RD-only result as limited/negative or weak evidence.
