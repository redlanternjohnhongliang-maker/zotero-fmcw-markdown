# D5E Analyze Results

Generated: 2026-06-27 20:56:44

Input directory: `G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis`

## 1. Raw CSV Inventory

| file | row_count | column_count | columns_preview |
|---|---|---|---|
| d5e_ceiling_effect_audit.csv | 3.0000 | 35.0000 | balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_mid_miss_count, balanced_mild_mid_pd, balanced_mild_overall_miss_count, balanced_mild_overall_pd, balanced_mild_strong_miss_count, balanced_mild_strong_pd |
| d5e_interference_manifest.csv | 576.0000 | 8.0000 | achieved_sir_db, frame_id, frame_idx, interference_params_json, num_interferers, sir_name, source_sequence, target_sir_db |
| d5e_pfa_sensitivity.csv | 15.0000 | 26.0000 | balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_mid_pd, balanced_mild_overall_pd, balanced_mild_strong_pd, balanced_mild_weak_hits, balanced_mild_weak_pd, false_alarm_count_delta |
| d5e_rd_mask_width_sensitivity.csv | 36.0000 | 31.0000 | background_cell_count, balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_mid_pd, balanced_mild_overall_pd, balanced_mild_saturated, balanced_mild_strong_pd, balanced_mild_weak_hits |
| d5e_rd_proxy_label_dependence.csv | 18.0000 | 29.0000 | balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_mid_pd, balanced_mild_overall_pd, balanced_mild_strong_pd, balanced_mild_weak_hits, balanced_mild_weak_pd, doppler_box_mode |
| d5e_reconstruction_metrics.csv | 10.0000 | 7.0000 | input_type, magmse_db_to_clean, method, mse_db_to_clean, mse_power_to_clean, seed, sir_name |
| d5e_sample_size_stability.csv | 6.0000 | 23.0000 | balanced_mild_weak_pd, balanced_mild_weak_pd_ci_high, balanced_mild_weak_pd_ci_low, five_hit_pd_delta, hit_delta_confidence, one_hit_pd_delta, plus_0_hits_meaningful, plus_1_hit_meets_pd_bar_0p02 |
| d5e_training_loss.csv | 52.0000 | 20.0000 | background_det_term, detection_term, epoch, grad_norm_before_clip, lambda_rec, lr, magmse_term, method |
| d5e_training_summary.csv | 4.0000 | 34.0000 | final_train_background_det, final_train_detection, final_train_loss, final_train_magmse, final_train_target_det, final_val_background_det, final_val_detection, final_val_loss |
| d5e_weak_threshold_difficulty.csv | 12.0000 | 32.0000 | balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_mid_pd, balanced_mild_overall_pd, balanced_mild_strong_pd, balanced_mild_weak_hits, balanced_mild_weak_pd, false_alarm_count_delta |

## 2. Ceiling Effect

| seed | weak_n | balanced_mild_weak_hits | weak_weighting_weak_hits | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | balanced_mild_weak_miss_count | ceiling_effect_present |
|---|---|---|---|---|---|---|---|---|---|
| 42.0000 | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | True |
| 200.0000 | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | True |
| mean | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |  |

## 3. PFA Sensitivity

| target_pfa | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta |
|---|---|---|---|---|---|---|
| 0.0100 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -42.5000 |
| 0.0050 | 0.9839 | 0.9839 | 0.0000 | 0.0000 | -0.0000 | -12.5000 |
| 0.0010 | 0.6048 | 0.5887 | -0.0161 | -1.0000 | 0.0000 | 6.5000 |
| 0.0005 | 0.3226 | 0.3145 | -0.0081 | -0.5000 | -0.0000 | -6.5000 |
| 0.0001 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0000 | -5.0000 |

## 4. Mask Width Sensitivity

| range_mask_name | doppler_radius_bins | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta |
|---|---|---|---|---|---|---|---|
| narrow | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -61.0000 |
| narrow | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -69.0000 |
| narrow | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -51.0000 |
| narrow | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -58.5000 |
| default | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -65.5000 |
| default | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -42.5000 |
| default | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -76.0000 |
| default | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -78.0000 |
| wide | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -0.5000 |
| wide | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -52.0000 |
| wide | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -20.0000 |
| wide | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |

## 5. Weak Threshold Difficulty

| q_weak | train_weak_threshold_db | train_weak_n | test_weak_n | mean_clean_rd_peak_db | mean_range_only_peak_db | mean_target_background_contrast_db | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1000 | 48.0669 | 21.0000 | 18.0000 | 93.5147 | 46.7701 | 31.2936 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.2000 | 49.2190 | 40.0000 | 37.0000 | 94.0908 | 47.7460 | 31.8631 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.3000 | 50.5937 | 56.0000 | 62.0000 | 94.6511 | 48.6145 | 32.4174 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.4000 | 51.8927 | 77.0000 | 76.0000 | 94.9766 | 49.0816 | 32.7413 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## 6. RD Proxy Label Dependence

| doppler_box_mode | weak_projection_hit_rate_against_clean_peak | target_box_area_mean_weak | overlap_ratio_vs_clean_peak_box | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|---|---|
| clean_peak | 1.0000 | 48.8710 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| interfered_peak | 1.0000 | 48.8710 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| local_window_peak | 0.9194 | 48.8710 | 0.9194 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| nearest_high_energy | 0.9194 | 48.8710 | 0.9194 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| vertical_stripe | 1.0000 | 2492.4194 | 0.0196 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| multi_bin_uncertainty | 1.0000 | 107.5161 | 0.4545 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## 7. Sample Size Stability

| seed | target_pfa | weak_n | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_pd_delta_ci_low | weak_pd_delta_ci_high | weak_hit_delta | one_hit_pd_delta | two_hit_pd_delta | five_hit_pd_delta | weak_n_small_for_claim |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 42.0000 | 0.0100 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0161 | 0.0323 | 0.0806 | True |
| 200.0000 | 0.0100 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0161 | 0.0323 | 0.0806 | True |
| seed_sensitivity | 0.0100 |  |  |  | 0.0000 |  |  |  |  |  |  |  |
| 42.0000 | 0.0010 | 62.0000 | 0.5968 | 0.5968 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0161 | 0.0323 | 0.0806 | True |
| 200.0000 | 0.0010 | 62.0000 | 0.6129 | 0.5806 | -0.0323 | -0.0806 | 0.0000 | -2.0000 | 0.0161 | 0.0323 | 0.0806 | True |
| seed_sensitivity | 0.0010 |  |  |  | -0.0161 |  |  |  |  |  |  |  |

## 8. Key Findings

### F1

- Observation: At PFA=1e-2, balanced_mild weak Pd is 1.0000 with 0.0 missed weak targets.
- Interpretation: The D5D default RD proxy has a hard ceiling: the baseline already hits every q30 weak target.
- Implication: D5D cannot demonstrate a weak-weighting improvement at the main PFA because there is no remaining weak-hit room.

### F2

- Observation: At PFA=1e-3, mean weak Pd delta is -0.0161 and mean weak hit delta is -1.0.
- Interpretation: When the threshold becomes stricter, weak weighting does not become better; it is slightly worse on average.
- Implication: Stricter fixed-PFA settings do not rescue weak weighting.

### F3

- Observation: Across 12 range/doppler mask combinations, no mean row has positive weak Pd and weak-hit delta together.
- Interpretation: Mask-width perturbation does not reveal a hidden weak-weighting advantage.
- Implication: The NO-GO is robust to the tested mask deformations.

### F4

- Observation: q10/q20/q30/q40 weak subsets all have balanced_mild weak Pd = 1.0; q30 test weak_n is 62 and mean RD contrast is 32.42 dB.
- Interpretation: The q30 range-only weak threshold still selects RD targets that are easy under the current RD proxy.
- Implication: The weak definition is not hard enough for RD weak-preservation claims.

### F5

- Observation: Clean/interfered peak proxy boxes both saturate; local-window overlap vs clean boxes is 0.9194, vertical-stripe area is 2492.4 cells.
- Interpretation: The proxy label design is optimistic/saturated. The issue is not only the clean-RD peak source; broad or alternative proxy boxes still make weak hits easy.
- Implication: D5E remains a mixed-proxy diagnosis, not confirmed RD performance.

### F6

- Observation: test weak_n is 62 at q30; one hit equals 0.0161 Pd, two hits equal 0.0323 Pd, and the pre-registered +5 hit bar equals 0.0806 Pd.
- Interpretation: Small hit-count changes can look nontrivial in Pd, but +0/+1/+2 hits are not enough for a robust claim.
- Implication: All claims must stay conservative, especially with only 2 seeds.

## 9. Verdict

Verdict: **NO-GO**

- Ceiling effect present: `True`
- q30 weak threshold too easy: `True`
- Stricter PFA supports weak weighting: `False`
- Mask deformation supports weak weighting: `False`
- RD proxy label overly optimistic/saturated: `True`
- D6 allowed: `False`

Recommended route: Stop weak weighting for now; do not enter D6. If continuing, first repair RD proxy/task difficulty.
