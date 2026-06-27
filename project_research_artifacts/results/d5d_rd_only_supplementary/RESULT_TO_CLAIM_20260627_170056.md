# D5D Result-to-Claim

**Date**: 2026-06-27  
**Reviewer**: Codex subagent, xhigh  
**Integrity status**: warn  
**Trace**: `G:\mineru_output\.aris\traces\result-to-claim\2026-06-27_run02`

## Verdict

`claim_supported: no`

Confidence: high for the NO-GO decision; medium for broader RD-suitability interpretation.

Final route: **NO-GO do not enter D6**.

## What Results Support

- RD fixed-PFA proxy pipeline ran end to end.
- Weak thresholds are train-only with `threshold_leakage=false`.
- At PFA `1e-2`, weak weighting did not increase measured PFA or false alarms: mean PFA delta `-1.396e-05`, mean false alarm delta `-41.5`.
- Clean no-harm passed in both seeds.
- D6 should remain forbidden.

## What Results Do Not Support

- RD weak weighting does not improve weak-target preservation: mean weak Pd delta `0.0000`, mean weak hit delta `0`, failing the `>=0.02` and `+5 hits` bars.
- PFA `1e-3` is not consistently safe: seed `200` reverses by `-0.0323` weak Pd and `-2` weak hits.
- RD is still a proxy/sanity result: boxes use range labels plus clean-RD Doppler peak projection, not Doppler ground truth.
- This does not overturn the prior range-only weak/negative evidence.

## Missing Evidence

- True Doppler/velocity ground truth, or a stronger pre-registered RD localization protocol.
- More seeds and broader SIR/PFA coverage.
- A non-saturated RD setting where weak Pd can show gain.
- Direct apples-to-apples RD vs range-only comparison under the same weak definition and fixed-PFA protocol.

## Suggested Claim Revision

In a 2-seed RD-only proxy sanity experiment, weak weighting did not improve weak-target preservation over `balanced_mild`; PFA/FA and clean no-harm were acceptable at PFA `1e-2`, but the pre-registered weak-gain bars failed and PFA `1e-3` showed reversal in one seed.

## Next Experiments Needed

- Do not run D6.
- Record D5D as limited/negative RD-only evidence.
- Only consider another RD supplement if it fixes the proxy issue or saturation issue first; it should not be treated as permission to continue weak weighting.
