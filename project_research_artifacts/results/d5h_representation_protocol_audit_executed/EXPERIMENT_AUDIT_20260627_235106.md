# Experiment Audit Report

**Date**: 2026-06-27 23:51:06  
**Auditor**: Codex subagent `gpt-5.5`, xhigh, read-only  
**Trace**: `G:\mineru_output\.aris\traces\experiment-audit\2026-06-27_run05`  
**Overall Verdict**: WARN  
**Integrity Status**: warn

## Checks

### A. No-Training / Boundary Compliance: PASS
D5H-Exec loads local files and prior tables only. `D5H_EXECUTED_CONFIG.json` records `no_training=true`, `entered_d6=false`, `false_alarm_penalty=false`, `detector_modified=false`, `fixed_pfa_protocol_modified=false`, and `new_dataset_downloaded=false`.

### B. Ground Truth And Proxy Provenance: PASS
Gao77 local labels support objectness/class plus projected range/azimuth. True Doppler, velocity, RAD boxes, and temporal track IDs are absent. RD/RA/STFT/complex/raw/point-cloud routes are marked proxy/auxiliary, not confirmed performance.

### C. Fixed-PFA Consistency: WARN
Reviewer found the first pass too loose for fixed-PFA feasibility and too broad in stricter-PFA columns. I applied local fixes and reran: `range_only` at PFA=1e-3 is now `warn`, and stricter-PFA details are only populated for `corrected_RD`. Status remains WARN because this post-review patch was not sent for a second independent review.

### D. Result Existence / Phantom Results: PASS
Required D5H CSV/MD/JSON outputs exist. `D5H_ANALYZE_RESULTS.md/json` reads the generated CSVs and preserves the no-pass decision.

### E. Dead Code / Metric Mismatch: WARN
Reviewer noted Phase 0 weak-threshold text was hard-coded despite loading D5D thresholds. I patched it to parse `d5d_rd_weak_thresholds.json` and reran. Status remains WARN pending any future external re-review.

### F. Scope And Claim Inflation: PASS
The outputs consistently say no representation passed, no minimal model sanity is allowed, weak weighting should not continue, and D6 remains forbidden. RD/RA/RAD proxy evidence is not written as confirmed performance.

## Post-Review Fixes Applied

- Tightened fixed_pfa_flag to a 25%/1e-4 absolute tolerance and reran D5H-Exec.
- Range-only PFA=1e-3 is now marked warn rather than yes.
- Stricter-PFA diagnostic dictionaries are blank for non-RD/non-executable rows.
- Phase 0 weak-threshold evidence is parsed from d5d_rd_weak_thresholds.json and rerun.

## Eligibility-Label Conservatism

Conservative. `proxy-only` is acceptable as a provenance label, but it is ineligible for confirmed Gao77 performance or D6/minimal model sanity. No representation should be upgraded to `pass`.

## Claim Impact

- No-training boundary claim: supported.
- No-go/no-pass D5H decision: supported with WARN status.
- RD/RA/RAD confirmed-performance claims: unsupported.
- Continuing weak weighting or entering D6: unsupported.
