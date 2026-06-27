# D5G Paper Direction Notes

**Date**: 2026-06-27  
**Purpose**: Decide how to write the current negative/diagnostic evidence without overclaiming.

## Possible paper framing

### Safe framing

The paper can be framed as a **fixed-PFA weak-target preservation study** showing that apparent gains from weak-target weighting can disappear once weak definitions, overlap contamination, RD proxy saturation, and label validity are audited.

This is not a new state-of-the-art radar interference mitigation method yet. It is a protocol/limitation study unless future Phase 1/2 audits produce a stronger representation result.

### Unsafe framing

Do not frame as:

- a confirmed weak-target-preserving training method;
- a broad negative theory of weak weighting;
- an RD/RAD performance paper;
- a model-capacity comparison paper;
- a real physical interference benchmark if the interference is synthetic FMCW-like.

## Candidate title directions

- Fixed-PFA Weak-Target Evaluation for FMCW Radar Interference Mitigation: A Negative Protocol Study
- When Weak-Target Weighting Fails: Representation and Proxy Pitfalls in FMCW Radar Interference Mitigation
- Auditing Weak-Target Claims under Fixed-PFA Radar Evaluation

## Main paper-usable claim

> In our Gao77 synthetic FMCW-like interference setting, weak-target weighting did not produce robust weak-target preservation gains under fixed-PFA evaluation. Follow-up diagnostics show that range-only overlap contamination and saturated mixed-proxy RD labels can make weak-target claims unreliable. These findings motivate a representation and label-protocol audit before further model or loss escalation.

## Claims that require more evidence

| claim | needed evidence |
|---|---|
| RAD improves weak-target preservation | label-valid RAD boxes/masks, non-saturated baseline, multiple seeds |
| temporal RD/RAD helps weak targets | leakage-free temporal labels, track consistency, fixed-PFA gains |
| raw ADC/complex input fixes failure | raw/complex availability, no-harm, compute feasibility, label-valid weak metrics |
| model capacity is the bottleneck | passing protocol plus controlled capacity ablation |
| loss design is the bottleneck | passing protocol plus loss ablation under fixed PFA |

## English paper-usable conclusion

> Under the current fixed-PFA weak-target evaluation protocol, weak-target-weighted training does not provide a reliable improvement over the balanced baseline. The follow-up RD-only diagnostics reveal a saturated mixed-proxy evaluation: at the main operating point, the baseline already detects all proxy weak targets, while stricter PFA settings do not recover a benefit. These results should not be interpreted as confirmed RD performance or as a universal failure of weak-target weighting. Rather, they indicate that representation collapse, proxy label validity, task saturation, and weak-target sample size must be audited before new losses or larger radar models are introduced.

## Suggested next minimal prompt

```text
/experiment-plan "D5G Phase 0/1 no-training representation protocol audit for FMCW fixed-PFA weak-target preservation after D5E NO-GO. Audit range-only, corrected RD, corrected RA, RAD, temporal RD/RAD, STFT, complex IQ, and raw ADC only for label validity, weak_n, overlap, separability, saturation, fixed-PFA calibration, leakage, and GPU cost. Do not train. Do not enter D6." -- effort: balanced, assurance: conference-ready
```
