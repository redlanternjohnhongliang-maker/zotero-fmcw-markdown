# D5D RD-only GO / NO-GO decision

Generated: 2026-06-27 16:36:51

## Verdict

**NO-GO**

Route: NO-GO: do not enter D6; record RD-only result as limited/negative or weak evidence

## Mechanical Criteria

| criterion | pass |
|---|---|
| mean_weak_pd_delta_ge_0p02 | False |
| mean_weak_hit_delta_ge_5 | False |
| measured_pfa_not_up_all_seeds | True |
| false_alarm_not_up_all_seeds | True |
| clean_no_harm_all_seeds | True |
| default_narrow_consistent_all_seeds | True |
| all_non_overlap_consistent_all_seeds | True |
| pfa_1e3_not_reversed_all_seeds | False |
| mean_gain_not_below_balanced | True |
| weak_threshold_leakage | False |

## Evidence

| seed | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta | clean_no_harm_pass | default_vs_narrow_mask_consistency | all_vs_non_overlap_consistency | pfa_1e3_not_reversed |
|---|---|---|---|---|---|---|---|---|
| 42.0000 | 0.0000 | 0.0000 | -0.0000 | -57.0000 | True | True | True | True |
| 200.0000 | 0.0000 | 0.0000 | -0.0000 | -26.0000 | True | True | True | False |

## Conservative Note

D5D remains a limited RD-only supplementary sanity experiment. It does not authorize D6 unless all bars pass. Because RD boxes use clean-RD Doppler peak projection rather than Doppler ground truth, any positive result must still be written as preliminary.
