# D5H Kill Argument

**Date**: 2026-06-27  
**Attack reviewer**: Codex subagent, xhigh  
**Trace**: `G:\mineru_output\.aris\traces\kill-argument\2026-06-27_run02`  
**Verdict**: WARN  
**Reason code**: `too_broad_and_label_starved`

## Attack memo

> The D5H plan should be rejected because it cannot adjudicate its central question under its own evidence constraints. It presents a broad representation audit, but Gao77 currently provides only 1500 selected complex ADC frames, text boxes with class/px/py/width/length, and manifest-derived range/azimuth. The protocol therefore proposes to evaluate Doppler, RAD, temporal, point-cloud, and learnable-FFT representations without the labels or ground-truth structure needed to validate them. That is not a conservative no-training audit; it is an exercise in assigning proxy confidence to objects whose supervision is missing.
>
> The failure mode is predictable. RD was already shown to saturate on a mixed proxy, RA fixed-PFA weak hit rate was poor, and D5G concluded that protocol/label failure is primary while representation limitation remains merely plausible. D5H does not add the missing information needed to separate those hypotheses. Its gates mostly ensure that any representation requiring Doppler, temporal consistency, RAD boxes, or learned transforms will be marked weak-evidence or infeasible, while range-only remains the only stable reference. The “minimal sanity” allowance is circular: it permits testing only after the audit has already found usable labels, no leakage, calibrated PFA, non-saturation, separability gains, no-harm feasibility, and 4GB viability. Passing those conditions would nearly decide the case before the sanity check begins.
>
> Thus D5H is too broad to be probative and too label-starved to be decisive. It will formalize uncertainty, not reduce it.

## Adjudication

| attack point | status | response |
|---|---|---|
| D5H is too broad | partially answered | The plan covers many representations because the user requested them, but output must rank priority and mark several as future-only or insufficient-labels. |
| Gao77 lacks Doppler/RAD/temporal labels | answered | Phase 0 explicitly marks Doppler, RAD boxes, temporal tracks, and velocity as absent or proxy-only. |
| Proxy confidence may replace real labels | partially answered | Gate labels must prevent this: `proxy-only` cannot enter training or confirmed claims. |
| D5H cannot identify a valid representation strongly | answered by narrowed claim | D5H should only identify eligibility for minimal sanity, not prove validity or superiority. |
| Minimal sanity gate is circular | partially answered | It is intentionally conservative. The gate screens for measurement validity, not method success. A later minimal model sanity would still test whether learning changes anything. |
| D5H may formalize uncertainty rather than reduce it | still unresolved | If all candidates become `proxy-only` or `insufficient-labels`, D5H should stop the route and write negative/protocol limitation instead of expanding scope. |

## Hard fixes applied to the plan

1. Add four-way gate: `pass / proxy-only / insufficient-labels / fail`.
2. Cap clean-RD Doppler peak projection at `proxy-only`.
3. Treat raw_ADC_learnable_FFT as `future-only` because learning is forbidden.
4. State that D5H selects **eligibility**, not a valid/best representation.
5. If no representation passes, stop weak weighting route.

## Safe conclusion

D5H survives as a conservative no-training gate, not as a decisive representation selection study. Its value is to prevent premature training and expose label gaps. It is not evidence that any richer representation solves weak-target preservation.
