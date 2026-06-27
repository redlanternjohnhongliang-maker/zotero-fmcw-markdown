# D5G Next Experiment Plan

**Date**: 2026-06-27  
**Plan type**: no-training representation/protocol audit first  
**Hard constraint**: D6 remains forbidden unless all protocol gates below pass.

## Claim map

| candidate claim | current status | minimum evidence before claim |
|---|---|---|
| Weak-target weighting improves weak-target preservation | not supported | non-saturated fixed-PFA weak Pd gain `>=0.02` and `>=+5` weak hits across seeds, no false-alarm rise, clean no-harm pass |
| Current failure is protocol/representation-driven | partially supported | label/proxy audit showing where representation collapse, proxy leakage, saturation, or weak_n limits measurement |
| RD/RAD/temporal representations are better | not yet supported | label-valid RD/RA/RAD comparison under same fixed-PFA protocol |

## Phase 0: Data/label feasibility

Purpose: decide which representations can be audited without inventing labels.

Required checks:

| item | question | pass condition | fail action |
|---|---|---|---|
| true Doppler / velocity | Can Gao77 provide true Doppler or reliable velocity labels? | explicit label or projection agreement validated without clean leakage | RD/RAD only proxy/sanity, no performance claim |
| angle / azimuth | Can range-angle mapping be calibrated? | RA projection hit rate high and stable across splits | do not train RA |
| RAD labels | Can RAD boxes/masks be generated without clean peak leakage? | target boxes cover known targets while background/overlap remains controlled | use CARRADA/RADDet as external protocol reference only |
| temporal labels | Can velocity/track consistency be estimated from consecutive frames? | tracks consistent without using clean test labels | temporal audit only, no training |
| external datasets | Can CARRADA/RADDet/RADIal be used for protocol sanity? | dataset access and label schema match enough for diagnostic comparison | keep as literature/protocol discussion |
| controlled synthetic RAD GT | Can controlled synthetic RAD ground truth be built honestly? | clearly labeled as controlled synthetic, not real physical interference | use only as method sanity, not main claim |

Deliverable: `PHASE0_LABEL_FEASIBILITY.md` with `PASS / WARN / FAIL` per representation.

## Phase 1: Representation audit

Only no-training or minimal deterministic baselines. No weak-weighting training.

Representations to audit:

| representation | audit target |
|---|---|
| range-only | keep as negative baseline; quantify overlap and saturation |
| corrected RD | verify Doppler label validity and non-saturation |
| corrected RA | verify angle projection and calibration |
| RAD | check if dense 3D boxes/masks are possible |
| temporal RD | check target persistence and leakage-free track consistency |
| STFT spectrogram | check interference/target separability before range collapse |
| raw ADC subset | verify availability, memory cost, and phase/no-harm diagnostics |

For each representation, compute:

- projection hit rate
- weak_n under train-only weak threshold
- overlap ratio between weak target boxes and other target/background regions
- target/background separability
- baseline saturation at PFA `1e-2`, `1e-3`, and stricter thresholds
- measured PFA calibration error
- label leakage risk, especially clean-peak leakage
- GPU memory / runtime estimate
- whether one hit changes Pd by more than `0.01`

Pass gate for a representation:

- weak_n large enough that `+5` hits is meaningful, preferably Pd delta `<0.05`
- baseline weak Pd not saturated, target range roughly `0.3 to 0.85` at main PFA
- no clean-label leakage into test evaluation
- projection hit rate high enough to trust labels, but not trivially 1.0 because boxes are overbroad
- PFA calibration stable across thresholds
- overlap ratio low enough to separate weak target preservation from neighboring strong target preservation

## Phase 2: Minimal model sanity

Only run after a representation passes Phase 1. This is still not D6.

Compared systems:

| system | purpose |
|---|---|
| no-op / interfered input | lower bound |
| balanced_mild | main strong baseline |
| weak weighting | only as diagnostic, not as continuing method |
| reconstruction anchor | check whether target/no-harm stability needs reconstruction pressure |
| clean no-harm | mandatory clean-input degradation check |

Metrics:

- weak/mid/strong Pd at fixed PFA
- weak hit count and miss count
- measured PFA and false alarm count
- clean no-harm MSE/CFAR F1/Pd
- target/background contrast
- seed and split stability

Minimal success condition before reconsidering weak weighting:

- `weak Pd delta >= 0.02`
- `weak hit delta >= +5`
- no measured PFA increase beyond calibration tolerance
- clean no-harm pass
- effect stable across at least 3 seeds and more than one PFA threshold

## Phase 3: Claim gate

Only if Phase 2 passes:

1. rerun `/result-to-claim`;
2. rerun `/experiment-audit`;
3. check that label/proxy status is not `mixed_proxy`;
4. require non-saturated baseline;
5. require no leakage;
6. require no false-alarm rise;
7. require clean no-harm.

If any gate fails:

- do not enter D6;
- do not add false alarm penalty;
- record as negative/protocol limitation.

## Run order

| Run ID | phase | purpose | status |
|---|---|---|---|
| R008G-P0 | Phase 0 | label feasibility for RD/RA/RAD/temporal/raw ADC | TODO |
| R008G-P1A | Phase 1 | range-only and corrected RD no-training audit | TODO |
| R008G-P1B | Phase 1 | RA self-check and angle projection audit | TODO |
| R008G-P1C | Phase 1 | RAD feasibility and external-protocol comparison | TODO |
| R008G-P1D | Phase 1 | temporal RD/RAD leakage-free consistency audit | TODO |
| R008G-P1E | Phase 1 | STFT/raw ADC availability and cost audit | TODO |
| R008G-GATE | Phase 3 | claim gate deciding whether any minimal model run is justified | TODO |

## What not to run

- No D6.
- No false alarm penalty.
- No clean identity full method.
- No proposed full loss.
- No RIMformer/DiffRIM/RDLR-Net as main method.
- No larger model switch.
- No detector modification.
- No fixed-PFA protocol modification.
