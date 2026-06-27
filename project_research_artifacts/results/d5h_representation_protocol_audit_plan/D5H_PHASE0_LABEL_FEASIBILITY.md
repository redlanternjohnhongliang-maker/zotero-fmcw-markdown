# D5H Phase 0 Label Feasibility

**Date**: 2026-06-27  
**Scope**: local Gao77 data and prior D5 outputs only. No data download, no training.

## 1. Local Gao77 inventory

| item | observed local evidence | interpretation |
|---|---|---|
| raw ADC | `adcData` shape `128 x 255 x 4 x 2`, complex128 in D0 integrity summary | raw complex ADC exists locally |
| D1A selected subset | 1500 selected frames in `subset_d1a_v1` manifest | enough for no-training audit, not necessarily enough for final claims |
| text labels | CSV rows contain class, `px`, `py`, width, length | labels encode object class and spatial coordinates, but not explicit Doppler |
| range fields | manifest includes derived `range_min`, `range_max` | range is available through label projection/proxy |
| azimuth fields | manifest includes derived `azimuth_min`, `azimuth_max` | azimuth proxy exists, but RA fixed-PFA remains inconclusive |
| RD map | previous scripts create RD maps with shape `128 x 255` | RD representation is computable |
| RA map | previous scripts create RA smoke maps from virtual array | RA is computable, but calibration is not confirmed |
| RAD tensor | no confirmed local RAD label file found | feasibility only |
| temporal tracks | no confirmed track IDs found | proxy only if consecutive frames can be matched |
| synthetic interference pairing | prior pipeline uses synthetic FMCW-like interference | can support controlled audit, not real physical interference claim |

## 2. True/proxy/absent label classification

| target information | status | can be used for confirmed performance? | notes |
|---|---|---|---|
| class/objectness | true-ish dataset label | yes for objectness sanity, with class policy note | class=1 is treated as cyclist-like by local audit, not official README |
| range | proxy from spatial labels and projection | limited | enough for range-only baseline, not enough for full physical claim |
| azimuth | proxy from `px/py` geometry and manifest | no confirmed RA performance | D5C RA fixed-PFA weak hit rate was poor |
| Doppler | absent as true label | no | clean-RD peak projection is proxy and can leak optimism |
| velocity | absent | no | can only be temporal proxy if sequence continuity is audited |
| RAD box/mask | absent | no | may be constructed only as controlled proxy |
| weak target identity | proxy | no broad claim | train-only weak threshold and weak_n required |
| clean target signal | proxy via clean synthetic-pair generation | limited | must avoid using clean test peak to define evaluation labels |
| background / non-target | derived mask | limited | depends on target-mask width and overlap |

## 3. Gao77 support by representation

| representation | current support | reason |
|---|---|---|
| range_only | supported as baseline | range projection exists and prior pipeline already works |
| corrected_RD | supported only as proxy audit | RD maps exist, true Doppler labels do not |
| corrected_RA | supported only as calibration audit | azimuth proxy exists, but fixed-PFA RA weak hit is inconclusive |
| RAD | not supported for confirmed claims | no true RAD boxes/masks |
| temporal_RD | proxy only | no track IDs or velocity labels |
| temporal_RA | proxy only | no track IDs and RA calibration unresolved |
| temporal_RAD | not supported for current claims | combines missing RAD and missing tracks |
| STFT_spectrogram | supported for signal-level audit | raw ADC exists, but object labels remain spatial proxies |
| complex_IQ | supported for availability/no-harm audit | raw complex ADC exists |
| complex_RD | supported for phase-consistency audit if complex FFT retained | needs phase-preserving pipeline check |
| raw_ADC | supported for feasibility/cost audit | complex raw ADC exists, but labels are not raw-domain targets |
| raw_ADC_learnable_FFT | not supported for D5H beyond cost estimate | learnable transform implies training, forbidden |
| radar_point_cloud | auxiliary only | CFAR points may discard weak targets |

## 4. External datasets

| dataset | use in D5H | decision |
|---|---|---|
| CARRADA | protocol reference for RA/RD/RAD annotations | recommend as reference only, no download |
| RADDet | protocol reference for RAD boxes and dense tensor labels | recommend as reference only, no download |
| RADIal | protocol reference for raw HD radar and FFT-RadNet style labels | recommend as reference only, no download |
| other RA/RD/RAD datasets | possible later comparison | not needed for D5H planning |

## 5. Controlled synthetic RAD

Small controlled synthetic RAD may be useful as a protocol unit test because it can provide true range/Doppler/angle GT. But it must be clearly labeled:

- controlled synthetic scene;
- protocol sanity only;
- not real physical interference;
- not Gao77 performance.

Recommended use: only if Gao77 RAD/Doppler labels remain absent after Phase 0.

## 6. Phase 0 decision

Gao77 can support range-only baseline and raw/complex availability audits. It can support RD/RA only as **proxy/calibration audits**, not confirmed performance. RAD and temporal variants require new proxy design or external protocol references. Therefore Phase 1 should be no-training and gate-based.
