# GPT Handoff: D5H Phase 0/1 No-Training Representation Protocol Audit Plan

**Date**: 2026-06-27  
**Give this file to GPT**: yes. This is the single-file D5H summary.  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Current stage**: D5H plan completed. No experiments run. D6 remains forbidden.

## 1. Actual ARIS skills used

- `/experiment-plan`
- `/result-to-claim`
- `/kill-argument`

No training was run. No new dataset was downloaded.

## 2. New files created

- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_EXPERIMENT_PLAN.md`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_REPRESENTATION_AUDIT_SCHEMA.csv`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_PHASE0_LABEL_FEASIBILITY.md`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_PHASE1_AUDIT_MATRIX.csv`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_GATE_CRITERIA.md`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_RESULT_TO_CLAIM.md`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_KILL_ARGUMENT.md`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\D5H_NEXT_STEP_DECISION.md`
- `G:\mineru_output\results\d5h_representation_protocol_audit_plan\GPT_HANDOFF_D5H.md`

## 3. D5H core conclusion

D5H is approved only as a **no-training eligibility gate**. It can decide which representation is eligible for later minimal model sanity. It cannot prove which representation is valid, best, or sufficient for weak-target recovery.

The plan must classify each representation as:

- `pass`: may later enter minimal model sanity;
- `proxy-only`: continue audit only, no training claim;
- `insufficient-labels`: stop for Gao77 unless external/controlled labels appear;
- `fail`: stop route.

## 4. Most worth Phase 1 audit

| representation | reason |
|---|---|
| range_only | baseline and known failure reference |
| corrected_RD | strongest D5C smoke signal, but D5E saturation must be fixed |
| corrected_RA | RA is inconclusive; angle calibration must be checked |
| STFT_spectrogram | signal-level separability before range collapse |
| complex_IQ / complex_RD | phase preservation and no-harm feasibility |
| raw_ADC | available locally; only memory/feasibility audit now |

## 5. Temporarily not worth primary audit

| representation | reason |
|---|---|
| RAD | no confirmed Gao77 RAD boxes/masks |
| temporal_RD / temporal_RA / temporal_RAD | no track IDs or true velocity labels |
| raw_ADC_learnable_FFT | implies learning, forbidden in D5H |
| radar_point_cloud | auxiliary only; weak targets may be below CFAR |

## 6. Gao77 current label support

Local evidence:

- complex raw ADC exists: `adcData` shape `128 x 255 x 4 x 2`;
- D1A subset has 1500 selected frames;
- text labels include class, `px`, `py`, width, length;
- manifest derives range and azimuth fields;
- RD/RA maps are computable from prior scripts.

Label status:

| label | status |
|---|---|
| class/objectness | available |
| range | available by projection/proxy |
| azimuth | proxy available, calibration unresolved |
| Doppler | not true label |
| RAD boxes | absent |
| temporal tracks | absent |
| velocity | absent/proxy only |
| raw complex ADC | available |

## 7. Proxy labels

Proxy labels include range projection, azimuth projection, clean-RD Doppler peak projection, local-window RD/RA peaks, train-only weak thresholds, and synthetic clean/interfered pairing. They must not be written as confirmed RD/RA/RAD performance.

Any representation relying mainly on clean-RD Doppler peak projection is capped at `proxy-only`.

## 8. External datasets

CARRADA, RADDet, and RADIal are useful as protocol references. D5H should not download or run them.

## 9. Controlled synthetic RAD

Controlled synthetic RAD can be used later as a small protocol unit test with true range/Doppler/angle GT. It must be described as controlled synthetic protocol sanity, not real physical interference and not Gao77 performance.

## 10. Gate criteria

Minimal model sanity is allowed only if all are true:

1. label/proxy source is explicit;
2. no test leakage;
3. test weak_n `>=100`, or evidence is downgraded;
4. baseline weak Pd is not saturated at PFA `1e-2`;
5. PFA `1e-2` and `1e-3` calibrate;
6. overlap improves vs range_only;
7. weak separability improves vs range_only;
8. clean no-harm can be defined;
9. sanity subset fits GTX1650 4GB;
10. no over-dependence on clean peak proxy.

## 11. Result-to-claim verdict

`claim_supported: partial`  
`plan_sufficient_for_no_training_gate: partial`  
`should_allow_training_after_plan_as_written: only_if_gate_passes`  
`should_allow_D6: no`  
`confidence: medium`

Reviewer warning: D5H mostly rejects invalid choices and ranks feasibility. It does not prove a valid next representation.

## 12. Kill-argument strongest objection

The strongest objection is that D5H is too broad and label-starved: Gao77 lacks true Doppler, RAD boxes, temporal tracks, and velocity labels, so the audit may formalize uncertainty rather than reduce it. The fix is to narrow D5H to an eligibility gate and enforce `pass / proxy-only / insufficient-labels / fail`.

## 13. Training / D6 decision

- Training allowed now: no.
- Continue weak weighting now: no.
- D6 allowed: no.
- Larger model allowed now: no.
- False alarm penalty allowed now: no.

## 14. Minimal next prompt

```text
/experiment-plan "Execute D5H Phase 0/1 no-training representation protocol audit only. Produce pass/proxy-only/insufficient-labels/fail labels for range_only, corrected_RD, corrected_RA, RAD, temporal RD/RA/RAD, STFT, complex IQ/RD, raw ADC, raw ADC learnable FFT, and radar point cloud. Do not train. Do not enter D6. Do not treat proxy labels as confirmed performance." -- effort: balanced, assurance: conference-ready
```

## 15. Plain-language summary

D5H 的作用不是马上找出“最好的输入”，而是先检查每种输入有没有资格进入下一轮最小模型 sanity。现在 Gao77 有 range/azimuth/raw ADC，但缺 Doppler/RAD/track 真标签，所以很多 representation 只能标成 `proxy-only` 或 `insufficient-labels`。只要没有 `pass`，就不能训练，也不能进 D6。
