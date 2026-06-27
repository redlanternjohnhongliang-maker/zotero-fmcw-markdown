# D5G Project Decision

**Date**: 2026-06-27  
**Decision**: NO-GO for D6; pivot to representation/protocol audit.

## Decision table

| question | answer |
|---|---|
| Continue weak weighting training now? | No |
| Enter D6? | No |
| Add false alarm penalty? | No |
| Add clean identity full method? | No |
| Switch to larger model? | No |
| Make RIMformer/DiffRIM/RDLR-Net the main method? | No |
| Modify detector or fixed-PFA protocol? | No |
| Treat RD proxy as confirmed RD performance? | No |
| Treat ceiling effect as the only failure cause? | No |
| Pivot to protocol study? | Yes |

## Failure cause ranking

1. Label/proxy protocol failure.
2. Evaluation/task saturation.
3. Input representation limitation.
4. Data limitations and small weak_n.
5. Loss design weakness.
6. Model capacity, uncertain and not primary under current evidence.

## Recommended future route

1. Close D5 as conservative negative/diagnostic evidence.
2. Run D5G Phase 0 data/label feasibility.
3. Run D5G Phase 1 no-training representation audit.
4. Only if the audit passes, run minimal-model sanity on the passing representation.
5. Re-run `/result-to-claim` and `/experiment-audit` before any D6 discussion.

## Stop conditions

Stop and do not train if any of these holds:

- weak_n too small for stable hit-count interpretation;
- baseline already saturated at PFA `1e-2`;
- labels use clean-peak leakage or overbroad proxy boxes;
- RA/RAD projection cannot be validated;
- measured PFA is unstable across thresholds;
- clean no-harm cannot be assessed.

## Current project status line

`D5G = DONE as study; D6 = HOLD/FORBIDDEN; next allowed work = Phase 0/1 representation protocol audit only.`
