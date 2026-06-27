# D5G Result-to-Claim

**Date**: 2026-06-27  
**Reviewer**: Codex subagent, xhigh  
**Trace**: `G:\mineru_output\.aris\traces\result-to-claim\2026-06-27_run04`  
**Verdict**: `claim_supported: partial`  
**Confidence**: medium

## Structured judgment

| field | judgment |
|---|---|
| failure_cause_primary | Current evidence does not validate weak-target gains because the evaluation/protocol is too limited: range-only evidence is unstable, RD proxy labels are mixed, and D5E shows saturation at `PFA=1e-2`. |
| failure_cause_secondary | Input representation may be limiting because range-only drops Doppler/angle/phase/temporal information, but D5G only makes this plausible from literature. It is not proven as the primary bottleneck. |
| should_continue_weak_weighting_now | no |
| should_enter_D6 | no |
| should_pivot_to_protocol_study | yes |
| is_model_capacity_primary_bottleneck | uncertain |
| is_input_representation_primary_bottleneck | uncertain |
| is_label_protocol_primary_bottleneck | yes |
| recommended_next_route | Pivot to a protocol/representation study: define label-valid RD/RA/RAD or temporal evaluation protocols with defensible weak-target ground truth, then test whether representation changes help before changing the core model or adding new loss terms. |

## What results support

- The D5 series supports a conservative negative/diagnostic claim: current range-only and RD-proxy weak weighting does not reliably improve weak-target preservation under fixed-PFA evaluation.
- D5G supports that the next scientific bottleneck is likely protocol and representation validity, not immediate algorithm escalation.
- D5E supports a limited RD-proxy ceiling diagnosis: at PFA `1e-2`, `balanced_mild` already reaches weak hits `62/62`.

## What results do not support

- No confirmed RD performance.
- No real weak-target improvement claim.
- No broad theory that weak weighting fails generally.
- No claim that ceiling effect is the only failure cause.
- No justification for jumping to RIMformer/DiffRIM/RDLR-Net, larger models, false-alarm penalties, or clean-identity full-method training.

## Missing evidence

- True RD/RA/RAD labels or defensible proxy validation.
- Unsaturated fixed-PFA weak-target metrics.
- More seeds and larger weak-target sample.
- Representation comparisons under the same valid protocol.
- Evidence separating label/protocol failure from representation failure and model-capacity limits.

## Final route

**D5G should pivot to a representation/protocol audit. D6 remains forbidden.**
