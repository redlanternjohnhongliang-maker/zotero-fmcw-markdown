# D5H Analyze Results

**Date**: 2026-06-27 23:48:05  
**Input directory**: `G:\mineru_output\results\d5h_representation_protocol_audit_executed`

## CSV inventory

| file | rows | columns |
| --- | --- | --- |
| d5h_fixed_pfa_feasibility.csv | 13 | 9 |
| d5h_gpu_memory_feasibility.csv | 13 | 8 |
| d5h_overlap_separability_comparison.csv | 13 | 9 |
| d5h_phase0_label_inventory.csv | 10 | 7 |
| d5h_phase1_representation_audit.csv | 13 | 26 |
| d5h_proxy_label_risk_table.csv | 13 | 6 |
| d5h_representation_label_requirements.csv | 13 | 7 |
| d5h_saturation_risk.csv | 13 | 8 |

## Final eligibility by representation

| representation | final_eligibility_label | weak_n_estimate | pfa_1e_2 | pfa_1e_3 | main_reason |
| --- | --- | --- | --- | --- | --- |
| range_only | proxy-only | 262 | yes | warn | Baseline/reference only; does not improve over range-only by definition and cannot be a positive route. |
| corrected_RD | proxy-only | 62 | yes | yes | Relies on Doppler proxy, D5E weak_n=62<100, and main-PFA baseline is saturated. |
| corrected_RA | proxy-only | 262 | yes | yes | Original weak hit=0.0305; best physical weak hit=0.0941; calibration unresolved. |
| RAD | insufficient-labels |  | not_available | not_available | No true RAD boxes in Gao77 subset. |
| temporal_RD | insufficient-labels |  | not_available | not_available | No track IDs; frame continuity alone is not a label. |
| temporal_RA | insufficient-labels |  | not_available | not_available | No tracks and RA calibration does not pass. |
| temporal_RAD | insufficient-labels |  | not_available | not_available | Both RAD and temporal labels are absent. |
| STFT_spectrogram | proxy-only |  | not_available | not_available | Can be signal diagnostic from raw ADC, but object labels are projected proxies. |
| complex_IQ | proxy-only |  | not_available | not_available | Raw complex ADC exists, but target/background labels remain projected. |
| complex_RD | proxy-only |  | not_available | not_available | Same RD label limit; phase preservation does not fix label validity. |
| raw_ADC | proxy-only |  | not_available | not_available | Memory/availability audit only; deterministic FFT projection remains proxy. |
| raw_ADC_learnable_FFT | insufficient-labels |  | not_available | not_available | Learnable FFT implies training and is excluded from D5H. |
| radar_point_cloud | proxy-only |  | not_available | not_available | Auxiliary only; weak targets may be removed before point-cloud generation. |

## Grouped labels

- pass: `[]`
- proxy-only: `['range_only', 'corrected_RD', 'corrected_RA', 'STFT_spectrogram', 'complex_IQ', 'complex_RD', 'raw_ADC', 'radar_point_cloud']`
- insufficient-labels: `['RAD', 'temporal_RD', 'temporal_RA', 'temporal_RAD', 'raw_ADC_learnable_FFT']`
- fail: `[]`

## Decisions

| question | answer |
|---|---|
| any pass | False |
| allow minimal model sanity now | False |
| continue weak weighting now | False |
| enter D6 | False |

## Key findings

| id | finding | evidence | implication |
| --- | --- | --- | --- |
| 1 | No representation passed the D5H gate. | pass=[] | Do not allow minimal model sanity from current Gao77 evidence. |
| 2 | Corrected RD is computable and separable, but still proxy-only. | D5E weak_n=62, clean/interfered RD peak proxy, and PFA=1e-2 saturation. | Do not write RD proxy as confirmed RD performance. |
| 3 | Corrected RA remains calibration-inconclusive. | Original weak hit rate is low and best physical RCA row remains proxy evidence. | Do not treat RA as invalid; treat it as unresolved. |
| 4 | RAD and temporal routes are blocked by missing labels. | No RAD boxes, no velocity labels, and no track IDs found in the local Gao77 subset. | Use a label/protocol pivot rather than more training. |

## 大白话解释

这轮不是训练结果分析，而是协议资格审查。结果很干净也很保守：没有任何表示同时满足“标签有效、无泄漏、weak_n 足够、PFA 可校准、不饱和、相对 range-only 有改善、clean no-harm 可定义、4GB 可做 sanity”的全部条件。当前最该做的不是继续训练，而是修标签/协议：RD 需要真 Doppler 或不泄漏的 proxy，RA 需要校准，RAD/temporal 需要有相应标注的数据。
