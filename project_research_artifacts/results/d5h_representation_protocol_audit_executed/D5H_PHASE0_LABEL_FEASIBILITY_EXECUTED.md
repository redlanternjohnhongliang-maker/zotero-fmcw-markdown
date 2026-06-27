# D5H Phase 0 Label Feasibility Executed

**Date**: 2026-06-27 23:47:58  
**Scope**: Gao77 local subset only; no data download; no training.

## Local file confirmation

- subset: `G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`
- frames in manifest: `1500`
- radar MAT files: `1500`
- text label CSV files: `1500`
- object label rows scanned: `6168`
- text label column counts observed: `[6]`
- raw `adcData` sample shape/dtype: `128x255x4x2` / `complex128`, complex=`True`
- source sequence count: `5`; no track-ID file/column found.

## Label inventory

| label_or_protocol_item | status | true_label_available | proxy_available | claim_ceiling |
| --- | --- | --- | --- | --- |
| class/objectness | available | True | False | objectness/class sanity only |
| range | available_by_projection_proxy | False | True | range-only/projection sanity, not full physical GT |
| azimuth | proxy_available_calibration_unresolved | False | True | RA calibration audit only |
| Doppler | absent_as_true_label | False | True | RD proxy only; no confirmed RD performance |
| RAD boxes | absent | False | False | insufficient labels for Gao77 RAD claims |
| temporal track IDs | absent | False | frame_continuity_only | no temporal target performance claim |
| velocity | absent_proxy_only | False | True | diagnostic proxy only |
| raw complex ADC | available | True | False | availability and deterministic transform audit |
| clean/interfered synthetic pairing | available_as_synthetic_pairing | False | True | synthetic proxy only, not real physical interference |
| weak target definition | proxy_train_only_threshold_available_but_small | False | True | weak evidence; fails D5H pass threshold weak_n>=100 for RD proxy |

## Representation label requirements

| representation | available_true_labels | proxy_labels | missing_labels | gao77_support | final_label_blocker |
| --- | --- | --- | --- | --- | --- |
| range_only | class/objectness | range; weak target; background mask |  | supported baseline | baseline only; range collapse/proxy |
| corrected_RD | class/objectness; range | clean/interfered RD peak Doppler | true Doppler/velocity | computable proxy audit | no true Doppler and D5E saturation |
| corrected_RA | class/objectness; range | px/py azimuth projection | calibrated radar angle GT | calibration audit only | angle calibration unresolved |
| RAD | class/objectness; range proxy | possible constructed proxy | true Doppler; RAD boxes | not supported for confirmed Gao77 claims | missing RAD boxes |
| temporal_RD | range proxy | sequence continuity; RD peak proxy | track IDs; true velocity/Doppler | insufficient without tracks | missing track IDs |
| temporal_RA | range proxy | azimuth projection; frame continuity | track IDs; calibrated RA | insufficient while RA unresolved | missing tracks and RA calibration |
| temporal_RAD | range proxy | none sufficient | track IDs; RAD boxes; Doppler | not supported | missing RAD and temporal labels |
| STFT_spectrogram | raw ADC | range/frequency projection | true signal-domain target labels | signal diagnostic only | labels project only to range/frequency |
| complex_IQ | raw complex ADC | range/azimuth projections | phase-aware object GT | availability/proxy audit | no phase/object GT |
| complex_RD | raw complex ADC | clean/interfered RD peak proxy | true Doppler | proxy audit only | no true Doppler |
| raw_ADC | raw complex ADC | downstream FFT/range projection | raw-domain target labels | availability/proxy audit | no raw-domain target mask |
| raw_ADC_learnable_FFT | raw complex ADC | none allowed in D5H | training route labels/validated objective | future only | learned FFT implies forbidden training |
| radar_point_cloud | range/azimuth proxy | CFAR point-to-label matching | point labels/tracks | auxiliary diagnostic only | weak targets may disappear before point cloud |

## Proxy risk table

| representation | proxy_source | leakage_risk | proxy_optimism_risk | claim_ceiling |
| --- | --- | --- | --- | --- |
| range_only | range projection + train-only weak threshold | low_to_medium | range collapse/overlap hides targets | proxy-only |
| corrected_RD | clean/interfered RD Doppler peak projection | high | clean peak boxes and saturated baseline are over-optimistic | proxy-only |
| corrected_RA | px/py to azimuth projection | medium | axis/sign/mask width can inflate/deflate hits | proxy-only |
| RAD | constructed 3D boxes if attempted | high | invented boxes can encode clean peaks | insufficient-labels |
| temporal_RD | sequence continuity + RD proxy | high | future-frame/clean-frame association can leak | insufficient-labels |
| temporal_RA | sequence continuity + RA proxy | high | inherits RA and tracking leakage | insufficient-labels |
| temporal_RAD | constructed RAD tracks | high | combines missing labels and temporal leakage | insufficient-labels |
| STFT_spectrogram | range/frequency projection from spatial labels | medium | signal separability may not map to object hits | proxy-only |
| complex_IQ | projected object labels on raw complex samples | medium | phase no-harm can be underdefined | proxy-only |
| complex_RD | complex RD with same Doppler proxy | high | phase may be useful but labels remain proxy | proxy-only |
| raw_ADC | downstream deterministic projection | medium | raw domain has no direct object mask | proxy-only |
| raw_ADC_learnable_FFT | learned spectral transform | not_allowed | would require training | insufficient-labels |
| radar_point_cloud | CFAR-derived sparse points | medium | sub-threshold weak targets may be discarded | proxy-only |

## Phase 0 decision

Gao77 can support range-only baseline and raw/complex availability checks. It does not provide true Doppler, true velocity, RAD boxes, temporal track IDs, or point-cloud labels. Therefore RD/RA/STFT/complex/raw/point-cloud routes are capped at proxy or auxiliary audit, while RAD and temporal routes are label-insufficient for confirmed Gao77 claims.
