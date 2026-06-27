# D5B-D5C Result-to-Claim Verdict

**Date**: 2026-06-27  
**Reviewer**: independent Codex subagent, xhigh reasoning  
**Integrity status**: warn  
**Confidence**: medium

## Structured Verdict

- `claim_supported`: partial
- `integrity_status`: warn
- `confidence`: medium
- `final route`: conditional supplementary experiment

## Claim Questions

1. **Repaired weak definition gives stable weak-target gain**: no. Best repaired row is `clean_peak_overlap_aware`: weak Pd delta `0.0182`, hit delta `+4`, below both bars. Zero repaired rows clear `>=0.02` and `>=+5`.
2. **Range-only weak weighting negative result**: yes. The only bar-clearing row is unrepaired `clean_peak_percentile` with `0.0267` / `+7`, but it has high overlap contamination. Prior D5 history also shows only `+1` hit and 3-seed mean gain `-0.0076`.
3. **RD/RA next-stage follow-up**: partial. RD has feasibility-smoke evidence: weak separability `30.80 dB` vs range-only `5.94 dB`, gain `+24.87 dB`, fixed-PFA sanity pass. RA is inconclusive: lower overlap but weak projection hit rate drops to `0.0305`.
4. **D6 remains forbidden**: yes. No stable repaired gain, no formal 3-seed confirmation, proxy/smoke-only RD/RA, and audit status is `warn`.

## what_results_support

The results support recording range-only weak weighting as weak or negative evidence, and support a narrow RD feasibility confirmation. They do not support continued range-only weak weighting as a main path.

## what_results_dont_support

They do not support a claim that repaired weak definitions make weak weighting stable. They also do not support confirmed RD/RA improvement, RA readiness, or D6 entry.

## missing_evidence

Multi-seed repaired-definition runs with frozen/train-only weak thresholds; robust default/narrow and all/non-overlap gains; PFA `1e-3` support; independent RD/RA labels or a stronger projection audit; fixed-PFA RD training smoke, not just projection smoke.

## suggested_claim_revision

“Under repaired weak-target definitions, range-only weak-target weighting does not show stable preservation gains. RD projection smoke suggests possible separability advantages and warrants a narrow representation follow-up; RA remains inconclusive. D6 is not permitted.”

## next_experiments_needed

Run one constrained RD-only supplementary experiment: fixed-PFA, same detector protocol, no D6, no false-alarm penalty yet, multi-seed if feasible. Re-run result-to-claim afterward.
