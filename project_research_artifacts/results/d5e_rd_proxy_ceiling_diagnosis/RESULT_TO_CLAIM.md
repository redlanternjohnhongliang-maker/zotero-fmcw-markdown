# D5E Result-to-Claim

**Date**: 2026-06-27  
**Reviewer**: Codex subagent, xhigh  
**Integrity status**: warn  
**Trace**: `G:\mineru_output\.aris\traces\result-to-claim\2026-06-27_run03`

## Verdict

`claim_supported: partial`

Confidence: medium.

Final route: **NEVER_ENTER_D6_IMMEDIATELY**.

## What Results Support

- D5E supports that the D5D default RD-proxy evaluation is saturated. At PFA `1e-2`, both seeds have `weak_n=62`, `balanced_mild_weak_hits=62`, `weak_pd=1.0`, and `0` missed weak targets.
- D5E supports that the current RD proxy task is too easy or too saturated for weak-weighting evaluation: q10/q20/q30/q40 subsets saturate, all mask-width variants saturate, and all tested proxy-label variants saturate.
- D5E supports a limited RD-proxy ceiling diagnosis, not confirmed RD performance.

## What Results Do Not Support

- D5E does not support continuing weak weighting. At PFA `1e-3`, mean weak Pd delta is `-0.0161` and mean hit delta is `-1`.
- D5E does not support entering D6.
- D5E does not prove ceiling effect is the only reason weak weighting fails: when the ceiling is partly relaxed by stricter PFA, weak weighting still fails or worsens.
- D5E does not support confirmed RD performance because the evaluation uses mixed proxy RD boxes from range labels and Doppler projections, not true Doppler/velocity ground truth.

## Missing Evidence

- A non-saturated RD task with validated target labels.
- True Doppler/velocity ground truth, or a proxy proven not to be clean-peak or overbroad-box optimistic.
- More seeds/splits, larger weak-target sample size, and robust positive weak-hit gains under fixed PFA.

## Suggested Claim Revision

D5E shows that the current RD-only proxy evaluation is saturated: the balanced baseline already detects all proxy weak targets at the main PFA, so D5D cannot measure incremental weak-weighting benefit. Additional diagnostics do not reveal a weak-weighting advantage. This is limited RD-proxy negative/diagnostic evidence, not confirmed RD performance.

## Next Experiments Needed

First repair RD proxy/task difficulty. Use harder, validated RD labels or true Doppler/velocity evidence; avoid clean-peak/overbroad proxy boxes; increase weak-target sample size. Only then rerun balanced vs weak weighting under fixed PFA, multiple seeds/splits, and pre-registered hit/Pd bars before reconsidering D6.

## Question Calls

| question | call |
|---|---|
| D5D NO-GO mainly affected by ceiling/task saturation | partial: strong for default proxy, not full causal proof |
| current RD proxy too easy/saturated | yes |
| continue weak weighting | no |
| enter D6 | no |
| conservative report conclusion | limited RD-proxy ceiling diagnosis plus negative weak-weighting evidence |
| fix first | RD proxy/task difficulty and label validity |
