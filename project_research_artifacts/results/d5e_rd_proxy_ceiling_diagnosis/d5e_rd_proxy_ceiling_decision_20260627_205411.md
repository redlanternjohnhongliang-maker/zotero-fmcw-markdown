# D5E RD proxy and ceiling-effect decision

Generated: 2026-06-27 20:54:11

Verdict: **NO-GO**

Final route: **Do not enter D6. Do not continue weak weighting from the current evidence.**

## Decision Checks

| check | result |
|---|---:|
| ceiling effect present | True |
| q30 weak threshold too easy | True |
| stricter PFA supports weak weighting | False |
| mask deformation supports weak weighting | False |
| harder q thresholds support weak weighting | False |
| RD proxy label overly optimistic | True |
| weak_n too small for strong claim | True |
| D6 allowed | False |

## Rationale

At PFA=1e-2, `balanced_mild` has no missed weak targets in the current RD proxy task, so D5D cannot demonstrate an incremental weak-weighting gain. The stricter and alternative diagnostics do not produce a robust positive weak-hit delta for weak weighting. Because RD Doppler boxes are still proxy-derived and not true Doppler ground truth, the evidence ceiling is a limited RD-proxy sanity conclusion only.
