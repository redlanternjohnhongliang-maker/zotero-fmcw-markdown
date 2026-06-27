# D5H Gate Criteria

**Date**: 2026-06-27  
**Purpose**: Decide whether any representation may enter later minimal model sanity.

## 1. Non-negotiable stop rules

Stop immediately for a representation if any condition holds:

| stop rule | reason |
|---|---|
| label source cannot be named | no valid audit target |
| test labels depend on clean test peaks | clean-peak leakage risk |
| weak_n is too small and not marked weak evidence | hit-count deltas become unstable |
| baseline weak Pd is saturated at main PFA | no room to measure improvement |
| PFA cannot be calibrated at `1e-2` and `1e-3` | fixed-PFA comparison invalid |
| overlap is not improved over range_only | representation does not solve the known contamination |
| weak separability is not improved over range_only | no evidence representation helps weak targets |
| clean no-harm cannot be defined | cannot verify target preservation/no degradation |
| 4GB sanity subset cannot fit | not feasible for current hardware |
| result requires changing detector or fixed-PFA protocol | outside allowed D5H scope |

## 2. Pass criteria for minimal model sanity

A representation passes only if all of these are true:

1. label/proxy source is explicit;
2. leakage risk is `low` or mitigated by train-only/proxy-independent construction;
3. test weak_n `>=100`, or explicitly downgraded to weak evidence with no main claim;
4. baseline weak Pd at PFA `1e-2` is below saturation, target range `0.3 to 0.85`;
5. PFA calibration error is acceptable at PFA `1e-2` and `1e-3`;
6. overlap ratio improves versus range_only by at least a meaningful margin;
7. weak separability proxy improves versus range_only;
8. clean no-harm metric can be computed;
9. memory estimate fits GTX1650 4GB on a sanity subset;
10. proxy optimism is not dominated by clean-RD/clean-RA peak selection.

## 3. Representation-specific gates

| representation | pass gate | fail gate |
|---|---|---|
| range_only | baseline only; no continuation gate | cannot be used as positive route unless all prior negatives are overturned |
| corrected_RD | Doppler proxy validated without clean test leakage; non-saturated PFA | clean-peak projection or weak Pd saturation repeats D5E |
| corrected_RA | physical angle mapping, acceptable fixed-PFA weak hit, angle error controlled | D5C-like weak fixed-PFA hit near zero or unphysical mapping |
| RAD | source for RAD boxes/masks documented | boxes are invented from clean peaks or overbroad proxies |
| temporal_RD | track/velocity proxy does not use future clean test labels | temporal linkage leaks label or only smooths clean peaks |
| temporal_RA | RA gate passes first, then temporal consistency passes | RA still inconclusive |
| temporal_RAD | RAD and temporal gates both pass | either RAD or temporal label absent |
| STFT_spectrogram | deterministic signal-level target/background separability and no-harm possible | cannot map weak targets to STFT evidence |
| complex_IQ | complex data retained and phase no-harm definable | phase discarded or only magnitude available |
| complex_RD | complex RD available and phase consistency stable | phase proxy not reproducible |
| raw_ADC | memory feasible and labels can be projected without leakage | raw input exists but no valid weak target audit |
| raw_ADC_learnable_FFT | not allowed in D5H because it implies training | any learned transform proposed now |
| radar_point_cloud | auxiliary diagnostic only | used as primary weak-target route, since weak targets may be below CFAR |

## 4. Decision outcomes

| outcome | action |
|---|---|
| one or more representation passes | design a later minimal model sanity plan, still not D6 |
| only proxy/WARN representations pass | do not train; refine labels/proxies |
| no representation passes | stop weak weighting route and write negative/protocol limitation |
| raw/complex only passes availability but not labels | keep as future dataset/protocol direction |

## 5. D6 condition

D6 remains forbidden. D6 can only be discussed after:

1. Phase 1 gate passes;
2. later minimal model sanity passes;
3. `/experiment-audit` does not report `mixed_proxy`;
4. `/result-to-claim` supports a real claim;
5. false alarms and clean no-harm are safe without changing the main fixed-PFA protocol.
