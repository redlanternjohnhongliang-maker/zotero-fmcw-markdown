# D5H Result-to-Claim

**Date**: 2026-06-27  
**Reviewer**: Codex subagent, xhigh  
**Trace**: `G:\mineru_output\.aris\traces\result-to-claim\2026-06-27_run05`  
**Verdict**: `claim_supported: partial`  
**Confidence**: medium

## Structured verdict

| field | judgment |
|---|---|
| claim_supported | partial |
| plan_sufficient_for_no_training_gate | partial |
| should_allow_training_after_plan_as_written | only_if_gate_passes, and only after quantitative thresholds and proxy limits are enforced |
| should_allow_D6 | no |
| highest_risk_assumption | A no-training audit using incomplete Gao77 labels and proxy-derived Doppler/weak evidence can identify a valid next representation rather than merely identify invalid or infeasible options. |

## What the plan supports

D5H is sufficient to decide whether a representation is **eligible for later minimal model sanity**. It directly targets the known D5G failure mode: label/proxy/evaluation ambiguity. It also correctly blocks:

- weak-weighting continuation;
- D6;
- larger models;
- detector changes;
- false alarm penalty;
- proxy results being written as confirmed performance.

## What the plan does not support

D5H does not yet identify a “valid next representation” in the strong sense. Without true Doppler labels, confirmed RAD boxes, temporal tracks, or a firm weak-target definition independent of clean-peak proxies, D5H can mostly reject bad representations and rank feasibility. It cannot prove that corrected_RD, RAD, temporal, raw_ADC, or point-cloud representations are semantically valid for weak-target recovery.

## Required plan revision

The plan must use four gate labels:

| gate label | meaning | allowed next action |
|---|---|---|
| `pass` | label/proxy is explicit, leakage bounded, PFA calibrated, non-saturated, weak_n sufficient, clean no-harm definable, memory feasible | later minimal model sanity may be planned |
| `proxy-only` | representation is computable, but key labels are proxy and not independently validated | continue audit only; no training claim |
| `insufficient-labels` | required Doppler/RAD/temporal/velocity labels are missing | stop for Gao77; use external protocol reference or controlled synthetic unit test only |
| `fail` | leakage, saturation, PFA failure, impossible memory, or no useful weak evidence | stop route |

## Missing evidence or plan gaps

- Hard thresholds for “overlap/separability improves vs range-only”.
- Exact weak target definition independent of clean peak proxy.
- Rule for proxy-only representations.
- Pre-registered split/leakage rules for frame subsets and clean/interfered pairing.
- Minimum sample counts and confidence intervals beyond `weak_n >= 100`.
- Explicit handling for unavailable Doppler, RAD boxes, temporal tracks, and velocity.
- Fixed-PFA audit procedure for no-training scores/features.
- Separation between “representation is label-feasible” and “representation contains useful signal”.

## Recommended revision

Keep D5H, but narrow its claim:

> D5H selects representations eligible for later minimal model sanity; it does not prove which representation is valid or best.

Any candidate relying mainly on clean-RD Doppler peak projection must be capped at `proxy-only` unless independent evidence supports it.

## Final route

Proceed with D5H as a no-training audit plan. Do not train. Do not enter D6.
