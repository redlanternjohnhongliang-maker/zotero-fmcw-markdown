# D5H Next Step Decision

**Date**: 2026-06-27  
**Decision**: D5H plan is approved as a no-training audit plan only.

## Core conclusion

D5H should proceed only as Phase 0/1 planning and audit. It may decide whether a representation is eligible for later minimal model sanity, but it must not claim that a valid next representation has already been found.

## Most worth auditing in Phase 1

| representation | why |
|---|---|
| range_only | required baseline and known failure reference |
| corrected_RD | best D5C separability smoke, but must overcome D5E proxy saturation |
| corrected_RA | needed because RA remains inconclusive and angle calibration is unresolved |
| STFT_spectrogram | useful signal-level separability before range collapse |
| complex_IQ / complex_RD | phase preservation and no-harm feasibility are important |
| raw_ADC | available locally as complex `128x255x4x2`; audit feasibility and memory only |

## Temporarily not worth primary audit

| representation | reason |
|---|---|
| RAD | no confirmed RAD boxes/masks in Gao77 |
| temporal_RD / temporal_RA / temporal_RAD | no track IDs or true velocity labels |
| raw_ADC_learnable_FFT | implies learning; forbidden in D5H |
| radar_point_cloud | sparse CFAR points can discard weak targets; auxiliary only |

## Gao77 label support

| label | status |
|---|---|
| class/objectness | available |
| range | available through projection/manifest-derived fields |
| azimuth | proxy available, calibration unresolved |
| Doppler | absent as true label |
| RAD box | absent |
| temporal track | absent |
| velocity | absent/proxy only |
| raw complex ADC | available |

## External datasets

CARRADA, RADDet, and RADIal are useful as protocol references. Do not download or run them in D5H.

## Controlled synthetic RAD

Useful only as a small protocol unit test if Gao77 cannot support Doppler/RAD/temporal labels. It must be labeled controlled synthetic, not real physical interference and not Gao77 performance.

## Gate decision

Minimal model sanity is allowed only after a representation receives `pass`. `proxy-only`, `insufficient-labels`, and `fail` do not permit training.

## Training and D6

- Training allowed now: no.
- Weak weighting continuation allowed now: no.
- D6 allowed: no.

## Minimal next prompt

```text
/experiment-plan "Execute D5H Phase 0/1 no-training representation protocol audit only. Produce pass/proxy-only/insufficient-labels/fail labels for range_only, corrected_RD, corrected_RA, RAD, temporal RD/RA/RAD, STFT, complex IQ/RD, raw ADC, raw ADC learnable FFT, and radar point cloud. Do not train. Do not enter D6. Do not treat proxy labels as confirmed performance." -- effort: balanced, assurance: conference-ready
```
