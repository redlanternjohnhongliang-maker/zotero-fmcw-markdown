# D5H Phase 1 No-Training Representation Audit Executed

**Date**: 2026-06-27 23:47:58  
**Scope**: deterministic/local evidence synthesis only. No model training, no D6, no detector change, no false alarm penalty.

## Final labels

| representation | weak_n_estimate | fixed_pfa_1e_2_feasible | fixed_pfa_1e_3_feasible | baseline_saturation_risk | clean_no_harm_definability | gtx1650_4gb_memory_feasible | final_eligibility_label | final_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| range_only | 262 | yes | warn | not_saturated_as_score_but_known_negative_baseline | definable as clean range no-harm, but only baseline | True | proxy-only | Baseline/reference only; does not improve over range-only by definition and cannot be a positive route. |
| corrected_RD | 62 | yes | yes | severe: balanced_mild weak Pd=1.0000, improvement_room=0 | definable only as RD proxy no-harm, not confirmed object performance | True | proxy-only | Relies on Doppler proxy, D5E weak_n=62<100, and main-PFA baseline is saturated. |
| corrected_RA | 262 | yes | yes | low saturation risk; primary issue is calibration/weak hit | definable only after calibrated RA mapping | True | proxy-only | Original weak hit=0.0305; best physical weak hit=0.0941; calibration unresolved. |
| RAD |  | not_available | not_available | not estimable without required labels | not definable for confirmed object no-harm | True | insufficient-labels | No true RAD boxes in Gao77 subset. |
| temporal_RD |  | not_available | not_available | not estimable without required labels | not definable for confirmed object no-harm | True | insufficient-labels | No track IDs; frame continuity alone is not a label. |
| temporal_RA |  | not_available | not_available | not estimable without required labels | not definable for confirmed object no-harm | True | insufficient-labels | No tracks and RA calibration does not pass. |
| temporal_RAD |  | not_available | not_available | not estimable without required labels | not definable for confirmed object no-harm | True | insufficient-labels | Both RAD and temporal labels are absent. |
| STFT_spectrogram |  | not_available | not_available | not estimable without required labels | proxy no-harm only | True | proxy-only | Can be signal diagnostic from raw ADC, but object labels are projected proxies. |
| complex_IQ |  | not_available | not_available | not estimable without required labels | proxy no-harm only | True | proxy-only | Raw complex ADC exists, but target/background labels remain projected. |
| complex_RD |  | not_available | not_available | not estimable without required labels | proxy no-harm only | True | proxy-only | Same RD label limit; phase preservation does not fix label validity. |
| raw_ADC |  | not_available | not_available | not estimable without required labels | proxy no-harm only | True | proxy-only | Memory/availability audit only; deterministic FFT projection remains proxy. |
| raw_ADC_learnable_FFT |  | not_available | not_available | not estimable without required labels | not definable for confirmed object no-harm | False | insufficient-labels | Learnable FFT implies training and is excluded from D5H. |
| radar_point_cloud |  | not_available | not_available | not estimable without required labels | proxy no-harm only | True | proxy-only | Auxiliary only; weak targets may be removed before point-cloud generation. |

Label counts: `{'proxy-only': 8, 'insufficient-labels': 5}`.

## Fixed-PFA feasibility

| representation | can_calibrate_pfa_1e_2 | measured_pfa_1e_2 | can_calibrate_pfa_1e_3 | measured_pfa_1e_3 | feasibility_note | final_eligibility_label |
| --- | --- | --- | --- | --- | --- | --- |
| range_only | yes | 0.010518884574655841 | warn | 0.0017649135192375574 | limited: PFA 1e-3 exists; stricter not rerun for range in D5H | proxy-only |
| corrected_RD | yes | 0.009759187772005412 | yes | 0.0010138314714122538 | yes as calibration; stricter PFA was tested in D5E but did not rescue weak weighting | proxy-only |
| corrected_RA | yes | 0.01026779626346652 | yes | 0.0009852720578208101 | yes as RA smoke; physically plausible best weak hit remains low | proxy-only |
| RAD | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | insufficient-labels |
| temporal_RD | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | insufficient-labels |
| temporal_RA | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | insufficient-labels |
| temporal_RAD | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | insufficient-labels |
| STFT_spectrogram | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | proxy-only |
| complex_IQ | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | proxy-only |
| complex_RD | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | proxy-only |
| raw_ADC | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | proxy-only |
| raw_ADC_learnable_FFT | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | insufficient-labels |
| radar_point_cloud | not_available |  | not_available |  | not executable as confirmed fixed-PFA object audit on Gao77 | proxy-only |

## Overlap / separability comparison

| representation | weak_overlap_ratio | weak_overlap_delta_vs_range_only | weak_separability_proxy_db | weak_separability_gain_vs_range_only_db | weak_projection_hit_rate | final_eligibility_label |
| --- | --- | --- | --- | --- | --- | --- |
| range_only | 0.2786259541984733 | 0.0 | 5.935464501424592 | 0.0 | 0.3511450381679389 | proxy-only |
| corrected_RD | 0.1946564885496183 | -0.08396946564885499 | 30.8048958669182 | 24.86943136549361 | 1.0 | proxy-only |
| corrected_RA | 0.0648854961832061 | -0.2137404580152672 | 9.027531631120288 | 3.092067129695696 | 0.030534351145038167 | proxy-only |
| RAD |  |  |  |  |  | insufficient-labels |
| temporal_RD |  |  |  |  |  | insufficient-labels |
| temporal_RA |  |  |  |  |  | insufficient-labels |
| temporal_RAD |  |  |  |  |  | insufficient-labels |
| STFT_spectrogram |  |  |  |  |  | proxy-only |
| complex_IQ |  |  |  |  |  | proxy-only |
| complex_RD |  |  |  |  |  | proxy-only |
| raw_ADC |  |  |  |  |  | proxy-only |
| raw_ADC_learnable_FFT |  |  |  |  |  | insufficient-labels |
| radar_point_cloud |  |  |  |  |  | proxy-only |

## Saturation risk

| representation | baseline_weak_pd_or_projection_hit_at_pfa_1e_2 | weak_n | baseline_weak_hits | improvement_room_weak_hits | saturation_risk | final_eligibility_label |
| --- | --- | --- | --- | --- | --- | --- |
| range_only | 0.3511450381679389 | 262 | 92 | 170 | not_saturated | proxy-only |
| corrected_RD | 1.0 | 62 | 62 | 0 | severe | proxy-only |
| corrected_RA | 0.030534351145038167 | 262 | 8 | 254 | not_saturated | proxy-only |
| RAD |  | 0 |  |  | unknown | insufficient-labels |
| temporal_RD |  | 0 |  |  | unknown | insufficient-labels |
| temporal_RA |  | 0 |  |  | unknown | insufficient-labels |
| temporal_RAD |  | 0 |  |  | unknown | insufficient-labels |
| STFT_spectrogram |  | 0 |  |  | unknown | proxy-only |
| complex_IQ |  | 0 |  |  | unknown | proxy-only |
| complex_RD |  | 0 |  |  | unknown | proxy-only |
| raw_ADC |  | 0 |  |  | unknown | proxy-only |
| raw_ADC_learnable_FFT |  | 0 |  |  | unknown | insufficient-labels |
| radar_point_cloud |  | 0 |  |  | unknown | proxy-only |

## GTX1650 4GB sanity estimate

| representation | input_shape_estimate | per_sample_mb_estimate | sanity_batch_tensor_mb_estimate | fits_gtx1650_4gb_sanity_subset | caveat |
| --- | --- | --- | --- | --- | --- |
| range_only | 128 | 0.0005 | 0.0312 | True | range profile only |
| corrected_RD | 128x255 | 0.1245 | 1.9922 | True | 2D RD smoke map |
| corrected_RA | 128x64 | 0.0312 | 0.5 | True | 2D RA smoke map |
| RAD | 128x64x255 | 7.9688 | 15.9375 | True | tensor memory feasible for tiny sanity, labels missing |
| temporal_RD | T4x128x255 | 0.498 | 1.9922 | True | tracks missing |
| temporal_RA | T4x128x64 | 0.125 | 0.5 | True | tracks and RA calibration missing |
| temporal_RAD | T4x128x64x255 | 31.875 | 31.875 | True | large but tiny subset fits; labels missing |
| STFT_spectrogram | rx/tx aggregated 255x128 | 0.1245 | 1.9922 | True | rough no-training score estimate |
| complex_IQ | 128x255x4x2 | 1.9922 | 7.9688 | True | raw MAT is complex128; conversion assumed for sanity |
| complex_RD | 128x255x2 | 0.249 | 1.9922 | True | phase retained but labels proxy |
| raw_ADC | 128x255x4x2 | 1.9922 | 7.9688 | True | memory feasible for tiny no-training audit |
| raw_ADC_learnable_FFT | 128x255x4x2 | 1.9922 | 7.9688 | False | training transform is forbidden in D5H |
| radar_point_cloud | variable sparse points | 0.1 | 6.4 | True | point labels missing; weak targets may be pre-filtered |

## Phase 1 decision

No representation receives `pass`. The closest computable routes are RD/RA/STFT/complex/raw/point-cloud, but they are proxy-only or auxiliary. Corrected RD has a strong separability smoke signal, yet D5E shows clean-peak proxy dependence, weak_n=62 under the train-only frozen weak definition, and PFA=1e-2 saturation. Corrected RA remains calibration-inconclusive. RAD and temporal variants are blocked by missing labels.
