# D5G Kill Argument

**Date**: 2026-06-27  
**Attack reviewer**: Codex subagent, xhigh  
**Trace**: `G:\mineru_output\.aris\traces\kill-argument\2026-06-27_run01`  
**Verdict**: WARN  
**Reason code**: `protocol_study_needed_but_not_yet_publishable`

## Attack memo

> The core problem with D5G is that it converts an empirical failure into a methodological posture without first possessing the evidentiary substrate needed for either claim. The D5D/D5E results do not show that weak-target weighting is unhelpful under fixed PFA; they show that the current RD-only proxy setup is too saturated, too label-poor, and too indirect to measure the effect. At PFA=1e-2 the weak-hit metric is ceilinged at 62/62 across variants, while at PFA=1e-3 weak weighting is slightly worse; that pattern is compatible with a broken proxy, calibration mismatch, overlap contamination, insufficient weak_n, or an actually harmful loss, and D5G chooses the most publishable-sounding interpretation: “limitation study.” The range-only D5-check/D5B evidence is likewise unstable and fails the pre-registered bars after repaired weak definitions, so it cannot anchor a negative result. D5C only establishes that RD experiments can run, not that RD or RA protocols validly preserve weak targets. The proposed no-training representation audit is sensible engineering triage, but as a research direction it is mostly an admission that the project lacks reliable labels, separability diagnostics, and fixed-PFA calibration. Literature gestures toward RAD, temporal RD/RAD, and raw ADC do not solve this; they merely relocate the uncertainty to larger input spaces. A reviewer would see D5G as explaining away a failed intervention by proposing a protocol audit that may be necessary internally, but is not yet a publishable scientific contribution.

## Adjudication

| attack point | status | response |
|---|---|---|
| D5G may be explaining away failure | partially answered | Correct. Therefore D5G should not claim a positive method. It should state that weak weighting is not supported under current protocols and that protocol validity is the next bottleneck. |
| Negative result may not be publishable | still unresolved | A negative/limitation study can become paper-usable only if the audit itself produces transferable diagnostics or a clear checklist for fixed-PFA weak-target evaluation. D5G alone is not enough. |
| Current RD proxy is too saturated and label-poor | answered by current evidence | D5E explicitly shows saturation at PFA=1e-2 and labels the RD setup as mixed proxy. This is exactly why D6 is forbidden. |
| Range-only evidence cannot anchor a broad negative conclusion | answered by current scope | D5G must limit the claim to current range-only and mixed RD-proxy settings. It cannot generalize to all weak weighting or all radar representations. |
| Literature gestures do not solve labels | answered by planned protocol | D5G treats RAD/temporal/raw ADC as audit candidates, not as solved future methods. This must remain explicit. |
| Protocol audit may be internal engineering rather than research | partially answered | The audit becomes research only if it produces measurable failure taxonomy, representation gates, and reproducible diagnostics. Otherwise it is internal triage. |

## Required safe framing

Use:

> The current evidence supports a conservative protocol diagnosis: under range-only and mixed RD-proxy fixed-PFA evaluation, weak-target weighting did not yield robust gains, and the RD proxy was saturated. The next step is a label-valid representation audit before any new model or loss.

Do not use:

> Weak-target weighting is ineffective for FMCW radar interference mitigation.

Do not use:

> RD performance confirms no benefit.

Do not use:

> The project has proven that model capacity is not the issue.

## Reviewer objections to answer before paper submission

1. Are you only rationalizing a failed intervention?
2. Does the negative result have value beyond this dataset?
3. Is synthetic FMCW-like interference too weak or not physical enough?
4. Are Gao77 labels insufficient for RD/RA/RAD claims?
5. Is weak_n too small for stable Pd conclusions?
6. Is fixed-PFA enough without no-harm and label-valid checks?
7. Should weak weighting be stopped now?
8. Should the dataset be changed before further method work?
9. Should RA self-check come before RAD?
10. Should raw ADC/complex input be audited rather than trained immediately?

## Decision after kill-argument

D5G survives only as a **conservative internal-to-paper bridge**: it blocks D6, blocks further weak-weighting training, and redirects effort to protocol validation. It does not by itself create a full publishable positive method.
