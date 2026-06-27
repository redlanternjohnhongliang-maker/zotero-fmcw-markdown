# D5C-RA-RCA Analyze Results

生成时间：2026-06-27 17:01:57

输入目录：`G:\mineru_output\results\d5c_ra_rca_self_check`

## 1. Raw CSV Inventory

| file | row_count | column_count | columns_preview |
| --- | --- | --- | --- |
| ra_angle_axis_audit.csv | 4 | 14 | angle_axis_max_deg, angle_axis_min_deg, angle_bin_count, axis_name, bin0_angle_deg, center_angle_deg, center_bin, expected_monotonic_for_shifted_plot |
| ra_d1a_vs_d5c_consistency.csv | 6 | 10 | angle_mask_total_width_bins, formula, hit_count, hit_criterion, hit_rate, notes, range_mask, source |
| ra_fft_axis_audit.csv | 1 | 19 | angle_fft_axis_in_range_virt, angle_fft_shape, axis_bug_found, check, chirp_axis, range_fft_axis, range_fft_shape, range_virt_shape_after_chirp_mean |
| ra_label_azimuth_formula_audit.csv | 8 | 21 | axis_sign, azimuth_deg_max, azimuth_deg_mean, azimuth_deg_min, azimuth_deg_std, bin_mode, candidate, consistent_with_manifest_range |
| ra_mask_width_sensitivity.csv | 144 | 32 | angle_guard_total_width_bins, angle_total_width_bins, axis_sign, background_cell_count, bin_mode, candidate, excluded_area_ratio, false_alarm_count |
| ra_projection_hit_breakdown.csv | 864 | 14 | angle_total_width_bins, axis_sign, bin_mode, candidate, formula, hit_count, mean_abs_peak_angle_error_deg, mean_contrast_db |

## 2. Formula Ranking

| candidate | formula | unit_mode | bin_mode | axis_sign | within_minus90_to_90_ratio | d1a_style_projection_hit_rate_all_frames | d5c_fixed_pfa_weak_projection_hit_rate | mean_abs_peak_angle_error_deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atan2_px_py_unshifted_bins_on_shifted_map | atan2(px, py) | degrees_correct | unshifted_bins_on_shifted_map | normal | 1.0 | 0.9072632944228275 | 0.10305343511450382 | 62.70976450315221 |
| atan2_py_px_current | atan2(py, px) | degrees_correct | fftshift_linear_sin | normal | 0.4711413748378729 | 0.8899156939040207 | 0.04961832061068702 | 65.76688000102152 |
| atan2_px_py_degrees_treated_as_radians | atan2(px, py) | degrees_treated_as_radians | fftshift_linear_sin | normal | 1.0 | 0.8597600518806745 | 0.04580152671755725 | 53.05321569745104 |
| atan2_px_py_current | atan2(px, py) | degrees_correct | fftshift_linear_sin | normal | 1.0 | 0.8762970168612192 | 0.030534351145038167 | 34.67690749879233 |
| atan2_px_neg_py_current | atan2(px, -py) | degrees_correct | fftshift_linear_sin | normal | 0.0 | 0.8762970168612192 | 0.030534351145038167 | 34.67690749879233 |
| atan2_neg_px_py_current | atan2(-px, py) | degrees_correct | fftshift_linear_sin | normal | 1.0 | 0.8670557717250325 | 0.026717557251908396 | 40.94176390391078 |
| atan2_px_py_axis_reversed | atan2(px, py) | degrees_correct | fftshift_linear_sin | reversed | 1.0 | 0.8670557717250325 | 0.026717557251908396 | 40.94176390391078 |
| atan2_px_py_radians_treated_as_degrees | atan2(px, py) | radians_treated_as_degrees | fftshift_linear_sin | normal | 1.0 | 0.830739299610895 | 0.0 | 36.052508098851085 |

## 3. Physically Consistent Angle Width Sweep

| range_mask_name | angle_total_width_bins | target_projection_hit_rate | weak_target_projection_hit_rate | target_overlap_ratio | weak_target_overlap_ratio | excluded_area_ratio | mean_abs_peak_angle_error_deg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| default | 1 | 0.08527131782945736 | 0.003816793893129771 | 0.0 | 0.0 | 0.037851721290650404 | 34.67690749879233 |
| default | 2 | 0.09302325581395349 | 0.011450381679389313 | 0.015503875968992248 | 0.0 | 0.0430370299796748 | 34.67690749879233 |
| default | 3 | 0.09819121447028424 | 0.011450381679389313 | 0.12919896640826872 | 0.011450381679389313 | 0.048197726117886176 | 34.67690749879233 |
| default | 5 | 0.11627906976744186 | 0.030534351145038167 | 0.17054263565891473 | 0.03435114503816794 | 0.05847942073170732 | 34.67690749879233 |
| default | 7 | 0.11886304909560723 | 0.030534351145038167 | 0.21705426356589147 | 0.0648854961832061 | 0.06854277820121951 | 34.67690749879233 |
| default | 10 | 0.15762273901808785 | 0.07633587786259542 | 0.23255813953488372 | 0.0648854961832061 | 0.08312690548780488 | 34.67690749879233 |

## 4. Original Weak/Mid/Strong Breakdown

| subset | target_count | hit_count | projection_hit_rate | overlap_ratio | mean_contrast_db | mean_abs_peak_angle_error_deg |
| --- | --- | --- | --- | --- | --- | --- |
| all | 387 | 46 | 0.11886304909560723 | 0.21705426356589147 | 9.581400218244054 | 34.67690749879233 |
| weak | 262 | 8 | 0.030534351145038167 | 0.0648854961832061 | 9.027531631120288 | 38.62352619330812 |
| mid | 82 | 19 | 0.23170731707317074 | 0.47560975609756095 | 10.13440141445253 | 27.152112705192977 |
| strong | 43 | 19 | 0.4418604651162791 | 0.6511627906976745 | 11.901573979577353 | 24.979676687443714 |
| non_overlap_only_weak | 245 | 7 | 0.02857142857142857 | 0.0 | 9.049545163524394 | 39.66128001273183 |
| overlap_only_weak | 17 | 1 | 0.058823529411764705 | 1.0 | 8.710277781767005 | 23.6676623251428 |

## 5. D1A+ vs D5C Consistency

| source | target_scope | hit_criterion | formula | range_mask | angle_mask_total_width_bins | target_count | hit_rate | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D1A+ prior ra_projection_sanity.csv | all valid targets / all frames | local RA target patch >= frame p70 and target-background ratio >= 0 | atan2(px, py) | fixed radius 2 bins | 5 | 6168 | 0.8762970168612192 | not fixed-PFA; not weak-only |
| D5C prior d5c_range_rd_ra_separability.csv | test split / weak targets | fixed-PFA 2D RA threshold at target PFA 1e-2 | atan2(px, py) | default object-size range interval | 7 | 262 | 0.030534351145038167 | weak-only D5C fixed-PFA smoke |
| D5C-RCA recomputed D1A-style | all valid targets / all frames | local RA target patch >= frame p70 and target-background ratio >= 0 | atan2(px, py) | fixed radius 2 bins | 5 | 6168 | 0.8762970168612192 | recomputed in this script as D1A+ path check |
| D5C-RCA recomputed D1A-style | D5C test split / weak targets | local RA target patch >= frame p70 and target-background ratio >= 0 | atan2(px, py) | fixed radius 2 bins | 5 | 262 | 0.683206106870229 | same weak subset but D1A-style criterion |
| D5C-RCA recomputed original fixed-PFA | D5C test split / weak targets | fixed-PFA 2D RA threshold at target PFA 1e-2 | atan2(px, py) | default | 7 | 262 | 0.030534351145038167 | should match D5C prior 0.0305 if metric path is aligned |
| D5C-RCA best fixed-PFA candidate | D5C test split / weak targets | fixed-PFA 2D RA threshold at target PFA 1e-2 | atan2(px, py) | wide | 10 | 255 | 0.1843137254901961 | best RCA sweep row; smoke-only, not confirmed RA method performance |

## 6. Key Findings

### F1

- Observation: Original D5C RA weak fixed-PFA hit rate was reproduced exactly: 0.030534.
- Interpretation: The 0.0305 number is not a dead-code artifact; it follows from the implemented fixed-PFA RA path.
- Implication: Do not dismiss the prior D5C RA result as a logging bug.
- Next step: Keep the original D5C RA row as the aligned baseline for any rerun.

### F2

- Observation: D1A+ local RA projection hit rate was 0.876297; on the D5C weak test subset, D1A-style hit rate was 0.683206, while D5C fixed-PFA weak hit rate was 0.030534.
- Interpretation: Most of the 0.8763 vs 0.0305 gap is criterion/scope: local contrast sanity vs weak-only fixed-PFA thresholding.
- Implication: The old D1A+ number cannot be used to claim D5C RA fixed-PFA success.
- Next step: Report both criteria side by side in any follow-up.

### F3

- Observation: `atan2(px, py)` is the only formula matching the manifest FOV and has lower mean angle error (34.68 deg) than empirical alternatives that increase weak hits.
- Interpretation: No physically justified sign, coordinate, or degrees/radians bug is established.
- Implication: Do not switch to `atan2(py, px)`, sign flip, radians misuse, or unshifted bins just because a sweep row is higher.
- Next step: If RA is revisited, calibrate the angle axis physically before changing mapping.

### F4

- Observation: Best physically plausible mask row improves weak hit rate only to 0.094118; best empirical row reaches 0.184314 but has mean angle error 63.17 deg.
- Interpretation: RA is mask-sensitive, but the improvement is not a clean restoration of projection quality.
- Implication: RA remains inconclusive; a wider mask is not enough to claim a bug fix.
- Next step: Prioritize RD; keep RA only as optional calibrated smoke follow-up.

### F5

- Observation: Raw ADC shape is 128x255x4x2; angle FFT uses axis 1 after RX/TX concatenation into 128x255x8.
- Interpretation: No sample/chirp axis mix-up was found, but the RA map is still a rough virtual-array smoke map.
- Implication: RA evidence should be qualified as smoke-only because no TDM-MIMO phase compensation/calibration is shown.
- Next step: Do not use RA for method claims without a separate calibrated RA validation.

## 7. Overall Interpretation

RA low hit rate is mainly a fixed-PFA/scope/mask-sensitivity issue, not a proven angle-coordinate bug.

## 8. Recommended Route

Keep RA inconclusive and prioritize RD-only supplementary work; do not enter D6.
