# D5H Executed Summary

**Date**: 2026-06-27 23:47:58  
**Actual skill stage**: `/experiment-bridge` scoped to no-training execution.

## What ran

- Read local Gao77 subset manifest, text labels, label policy, and one raw MAT file to confirm label/data availability.
- Read prior no-training or diagnostic evidence tables from D5C, D5E, and D5C-RA-RCA.
- Generated D5H Phase 0/1 CSV, Markdown, JSON, and sanity figures.
- Did not train any model; did not enter D6; did not add false alarm penalty.

## Final representation labels

| representation | final_eligibility_label | final_reason |
| --- | --- | --- |
| range_only | proxy-only | Baseline/reference only; does not improve over range-only by definition and cannot be a positive route. |
| corrected_RD | proxy-only | Relies on Doppler proxy, D5E weak_n=62<100, and main-PFA baseline is saturated. |
| corrected_RA | proxy-only | Original weak hit=0.0305; best physical weak hit=0.0941; calibration unresolved. |
| RAD | insufficient-labels | No true RAD boxes in Gao77 subset. |
| temporal_RD | insufficient-labels | No track IDs; frame continuity alone is not a label. |
| temporal_RA | insufficient-labels | No tracks and RA calibration does not pass. |
| temporal_RAD | insufficient-labels | Both RAD and temporal labels are absent. |
| STFT_spectrogram | proxy-only | Can be signal diagnostic from raw ADC, but object labels are projected proxies. |
| complex_IQ | proxy-only | Raw complex ADC exists, but target/background labels remain projected. |
| complex_RD | proxy-only | Same RD label limit; phase preservation does not fix label validity. |
| raw_ADC | proxy-only | Memory/availability audit only; deterministic FFT projection remains proxy. |
| raw_ADC_learnable_FFT | insufficient-labels | Learnable FFT implies training and is excluded from D5H. |
| radar_point_cloud | proxy-only | Auxiliary only; weak targets may be removed before point-cloud generation. |

## Grouped decision

- pass: `[]`
- proxy-only: `['range_only', 'corrected_RD', 'corrected_RA', 'STFT_spectrogram', 'complex_IQ', 'complex_RD', 'raw_ADC', 'radar_point_cloud']`
- insufficient-labels: `['RAD', 'temporal_RD', 'temporal_RA', 'temporal_RAD', 'raw_ADC_learnable_FFT']`
- fail: `[]`

## Figures

- `G:\mineru_output\gao_77ghz_raw_adc\reports\d5h_representation_protocol_audit_figures\representation_overlap_comparison.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\d5h_representation_protocol_audit_figures\weak_separability_comparison.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\d5h_representation_protocol_audit_figures\fixed_pfa_feasibility_comparison.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\d5h_representation_protocol_audit_figures\ra_angle_mapping_sanity.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\d5h_representation_protocol_audit_figures\rd_proxy_saturation_illustration.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\d5h_representation_protocol_audit_figures\memory_cost_bar_chart.png`

## Plain-language conclusion

The audit did its job, but the answer is conservative: the local Gao77 setup does not currently provide a label-valid, non-saturated, leakage-bounded representation that can be moved into later minimal model sanity. RD looks useful as a signal representation, but the current Doppler boxes are proxy-derived and saturated. RA still needs calibration. RAD and temporal variants need labels Gao77 does not provide.
