# Result To Claim: D5H-Exec

**Date**: 2026-06-27 23:55:01  
**Reviewer**: Codex subagent `gpt-5.5`, xhigh, read-only  
**Trace**: `G:\mineru_output\.aris\traces\result-to-claim\2026-06-27_run06`

## Structured Verdict

| field | judgment |
|---|---|
| claim_supported | yes |
| integrity_status | warn |
| confidence | medium |
| eligible_representations | [] |
| proxy_only_representations | ['range_only', 'corrected_RD', 'corrected_RA', 'STFT_spectrogram', 'complex_IQ', 'complex_RD', 'raw_ADC', 'radar_point_cloud'] |
| insufficient_label_representations | ['RAD', 'temporal_RD', 'temporal_RA', 'temporal_RAD', 'raw_ADC_learnable_FFT'] |
| failed_representations | [] |
| should_allow_minimal_model_sanity | False |
| should_continue_weak_weighting | False |
| should_enter_D6 | False |
| recommended_next_route | Protocol/data pivot to true Doppler/RAD/track labels or an explicitly synthetic protocol sanity test. |

## What Results Support

D5H was read-only/no-training; no representation passes all gates; RD/RA/raw-derived routes are proxy-only; RAD/temporal routes lack required Gao77 labels; current evidence blocks minimal model sanity, weak weighting, and D6.

## What Results Do Not Support

Confirmed Gao77 RD/RA/RAD performance, training eligibility, weak-target weighting continuation, false-alarm-penalty work, detector changes, or D6 entry.

## Missing Evidence

True Doppler/velocity labels, RAD boxes, temporal track IDs, calibrated RA ground truth, non-proxy weak-target evidence with adequate weak_n, and a second post-fix integrity review.

## Suggested Claim Revision

In the current Gao77 no-training audit, no representation is eligible for later minimal model sanity; all usable routes are proxy-only or label-insufficient, so the project should pivot labels/protocol before any training, weak weighting, or D6.

## Optional Kill-Argument

Not called. The trigger condition was not met because no representation has `pass` and minimal model sanity is not allowed.
