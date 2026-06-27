# D5B-D5C Analyze Results

生成时间：2026-06-27 15:15:56

输入目录：`G:\mineru_output\results\d5b_d5c_weak_definition_rdra_diagnosis`

## 1. Raw CSV Inventory

| file | row_count | column_count | columns_preview |
|---|---|---|---|
| d5b_d5c_decision_rows.csv | 3 | 4 | decision_item, evidence, route, verdict |
| d5b_fixed_pfa_metrics.csv | 1624 | 45 | background_cell_count, background_energy_increase_db, bootstrap_pfa_ci_high, bootstrap_pfa_ci_low, bootstrap_pfa_std, f1, false_alarm_count, fn_cells |
| d5b_metrics_by_mask.csv | 812 | 45 | background_cell_count, background_energy_increase_db, bootstrap_pfa_ci_high, bootstrap_pfa_ci_low, bootstrap_pfa_std, f1, false_alarm_count, fn_cells |
| d5b_metrics_non_overlap_only.csv | 812 | 45 | background_cell_count, background_energy_increase_db, bootstrap_pfa_ci_high, bootstrap_pfa_ci_low, bootstrap_pfa_std, f1, false_alarm_count, fn_cells |
| d5b_reconstruction_metrics.csv | 29 | 6 | input_type, magmse_db_to_clean, mse_db_to_clean, mse_power_to_clean, sir_name, target_sir_db |
| d5b_repaired_definition_results.csv | 6 | 59 | all_targets_weak_pd_delta, all_vs_non_overlap_consistency, average_nearest_target_distance_bins, balanced_mild_false_alarm_count, balanced_mild_measured_pfa, balanced_mild_mid_pd, balanced_mild_overall_pd, balanced_mild_strong_pd |
| d5b_training_loss.csv | 147 | 27 | alpha, background_det_term, baseline, definition, det_term, detection_term, epoch, family |
| d5b_training_summary.csv | 7 | 40 | alpha, baseline, definition, family, final_train_background_det, final_train_det, final_train_detection, final_train_loss |
| d5b_weak_definition_audit.csv | 6 | 15 | average_nearest_target_distance_bins, definition, definition_display, interval_overlap_ratio, jaccard_with_clean_peak_percentile, mean_cfar_margin_db, mean_clean_peak_db, mean_peak_to_local_background_ratio_db |
| d5c_range_rd_ra_separability.csv | 3 | 21 | background_target_contrast_db, fixed_pfa_calibration_sanity, measured_pfa_at_target_pfa_1e_2, measured_pfa_at_target_pfa_1e_3, representation, scope_note, score_type, separability_proxy_db |

## 2. Delta vs balanced_mild

| definition | weak_n | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta | clean_input_no_harm | default_vs_narrow_mask_consistency | all_vs_non_overlap_consistency |
|---|---|---|---|---|---|---|---|---|---|---|
| clean_peak_percentile | 1851 | 0.35877862595419846 | 0.38549618320610685 | 0.026717557251908386 | 7 | -0.00021178962230850723 | -3 | True | True | True |
| clean_peak_non_overlap | 932 | 0.3544973544973545 | 0.37037037037037035 | 0.015873015873015872 | 3 | -7.059654076950299e-05 | -1 | True | True | True |
| clean_peak_overlap_aware | 1120 | 0.36818181818181817 | 0.38636363636363635 | 0.018181818181818188 | 4 | -0.00035298270384751147 | -5 | True | True | True |
| isolated_target_only | 932 | 0.3544973544973545 | 0.37037037037037035 | 0.015873015873015872 | 3 | 0.0 | 0 | True | True | True |
| peak_to_local_background_ratio | 1851 | 0.2796610169491525 | 0.2966101694915254 | 0.01694915254237289 | 4 | -0.00014119308153900598 | -2 | True | True | True |
| range_bin_unique_distance | 1580 | 0.3497942386831276 | 0.35390946502057613 | 0.004115226337448541 | 1 | 7.059654076950125e-05 | 1 | True | False | True |

## 3. RD/RA Smoke

| representation | weak_target_projection_hit_rate | weak_target_overlap_ratio | weak_separability_proxy_db | weak_separability_gain_vs_range_db | weak_projection_hit_delta_vs_range | fixed_pfa_calibration_sanity | supports_followup_rdra_training |
|---|---|---|---|---|---|---|---|
| range_only | 0.3511450381679389 | 0.2786259541984733 | 5.935464501424592 |  |  | pass | smoke_only_no |
| RD | 1.0 | 0.1946564885496183 | 30.8048958669182 | 24.86943136549361 | 0.6488549618320612 | pass | feasibility_smoke_yes |
| RA | 0.030534351145038167 | 0.0648854961832061 | 9.027531631120288 | 3.092067129695696 | -0.32061068702290074 | pass | feasibility_smoke_inconclusive |

## 4. Key Findings

### F1

- Observation: Only the original clean_peak_percentile row crosses the weak-weighting bar: weak Pd delta 0.0267, hit delta 7.
- Interpretation: The apparent gain is tied to the original overlap-contaminated definition, not to a repaired definition.
- Implication: Do not claim repaired weak definition gives stable weak-target weighting benefit.
- Next step: Treat original clean_peak result as a diagnostic upper bound and validate repaired definitions before any continuation.

### F2

- Observation: Best repaired row is clean_peak_overlap_aware with weak Pd delta 0.0182 and hit delta 4; 5/5 repaired rows miss the minimum gain or hit-count bar.
- Interpretation: Repairing overlap reduces contamination but also removes the only bar-clearing weak-weighting gain.
- Implication: Range-only weak weighting remains weak evidence / negative-result leaning under repaired definitions.
- Next step: Record the range-only result conservatively and avoid D6.

### F3

- Observation: RD smoke reduces weak overlap from 0.2786 to 0.1947 and raises weak separability proxy by 24.87 dB.
- Interpretation: RD gives the clearest feasibility signal for better separability, but this is a smoke proxy without Doppler ground-truth labels.
- Implication: RD can justify a narrow feasibility follow-up, not a confirmed method claim.
- Next step: Run a small RD representation confirmation audit before any training-scale decision.

### F4

- Observation: RA reduces weak overlap to 0.0649, but weak projection hit rate is 0.0305, below range-only 0.3511.
- Interpretation: RA geometry can separate overlaps but current rough angle projection misses many weak targets.
- Implication: RA is feasibility evidence only and weaker than RD for next-step priority.
- Next step: Keep RA as secondary smoke unless angle-label calibration is improved.

## 5. Noise / Robustness Flags

- Small hit-count noise: repaired rows top out at +4 hits, below the +5 bar.
- Mask inconsistency: range_bin_unique_distance.
- All vs non-overlap inconsistency: none.
- PFA or false alarm increase: range_bin_unique_distance.

## 6. Recommended Route

record range-only weak weighting as negative/weak evidence; optionally run a narrow RD feasibility confirmation; do not enter D6.
