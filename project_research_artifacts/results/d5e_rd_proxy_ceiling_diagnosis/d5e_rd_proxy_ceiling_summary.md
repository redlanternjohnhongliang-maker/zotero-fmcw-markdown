# D5E RD proxy and ceiling-effect diagnosis

Generated: 2026-06-27 20:54:11

Input basis: D5D RD-only supplementary setup, re-run as a diagnostic only. This is not D6, not a new large model, and not a confirmed RD-performance evaluation.

## 1. Purpose

D5E diagnoses why D5D reported `balanced_mild weak Pd = 1.0` at the main PFA, leaving no room for weak weighting to show improvement.

## 2. Key Diagnostic Tables

### Ceiling Effect

| seed | weak_n | balanced_mild_weak_hits | weak_weighting_weak_hits | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | balanced_mild_weak_miss_count | ceiling_effect_present |
|---|---|---|---|---|---|---|---|---|---|
| 42.0000 | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | True |
| 200.0000 | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | True |
| mean | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |  |

### PFA Sensitivity

| target_pfa | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta |
|---|---|---|---|---|---|---|
| 0.0100 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -42.5000 |
| 0.0050 | 0.9839 | 0.9839 | 0.0000 | 0.0000 | -0.0000 | -12.5000 |
| 0.0010 | 0.6048 | 0.5887 | -0.0161 | -1.0000 | 0.0000 | 6.5000 |
| 0.0005 | 0.3226 | 0.3145 | -0.0081 | -0.5000 | -0.0000 | -6.5000 |
| 0.0001 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0000 | -5.0000 |

### Mask Width Sensitivity

| range_mask_name | doppler_radius_bins | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | background_cell_count |
|---|---|---|---|---|---|---|
| narrow | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2987468.0000 |
| narrow | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2982418.0000 |
| narrow | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2977368.0000 |
| narrow | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2967339.0000 |
| default | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2979365.0000 |
| default | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2972523.0000 |
| default | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2965681.0000 |
| default | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2952161.0000 |
| wide | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2968311.0000 |
| wide | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2959071.0000 |
| wide | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2949953.0000 |
| wide | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 2932024.0000 |

### Weak Threshold Difficulty

| q_weak | train_weak_threshold_db | train_weak_n | test_weak_n | mean_clean_rd_peak_db | mean_range_only_peak_db | mean_target_background_contrast_db | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1000 | 48.0669 | 21.0000 | 18.0000 | 93.5147 | 46.7701 | 31.2936 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.2000 | 49.2190 | 40.0000 | 37.0000 | 94.0908 | 47.7460 | 31.8631 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.3000 | 50.5937 | 56.0000 | 62.0000 | 94.6511 | 48.6145 | 32.4174 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.4000 | 51.8927 | 77.0000 | 76.0000 | 94.9766 | 49.0816 | 32.7413 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

### RD Proxy Label Dependence

| doppler_box_mode | weak_projection_hit_rate_against_clean_peak | target_box_area_mean_weak | overlap_ratio_vs_clean_peak_box | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|---|---|
| clean_peak | 1.0000 | 48.8710 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| interfered_peak | 1.0000 | 48.8710 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| local_window_peak | 0.9194 | 48.8710 | 0.9194 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| nearest_high_energy | 0.9194 | 48.8710 | 0.9194 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| vertical_stripe | 1.0000 | 2492.4194 | 0.0196 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| multi_bin_uncertainty | 1.0000 | 107.5161 | 0.4545 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## 3. Decision Summary

- Ceiling effect present: `True`
- q30 too easy under the current RD proxy: `True`
- Stricter PFA supports weak weighting: `False`
- Mask deformation supports weak weighting: `False`
- Harder q10/q20 subsets support weak weighting: `False`
- RD proxy label overly optimistic: `True`
- weak_n too small for strong claims: `True`

## 4. Conservative Interpretation

The D5D NO-GO is strongly affected by a ceiling effect in the current RD proxy task: the `balanced_mild` model already hits all weak targets at PFA=1e-2. D5E does not find a robust weak-weighting advantage under stricter PFA thresholds, narrower/wider masks, or harder train-only weak-threshold subsets. RD target boxes remain proxy labels derived from range labels and Doppler projections rather than true Doppler/velocity ground truth. Therefore D5E reinforces a conservative NO-GO: do not enter D6, do not claim confirmed RD performance, and treat weak weighting as unsupported until the RD proxy/task difficulty is repaired.
