# D5H Experiment Plan: Phase 0/1 No-Training Representation Protocol Audit

**Date**: 2026-06-27  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Plan type**: no-training protocol audit only  
**Hard constraints**: no training, no D6, no false alarm penalty, no clean identity full method, no larger model, no detector modification, no fixed-PFA protocol modification.

## 1. Problem and thesis

### Problem

D5D/D5E showed that weak-target weighting is not supported under current fixed-PFA weak-target evaluation. The strongest current failure source is not model capacity, but label/proxy/evaluation protocol validity. D5E also showed the current RD proxy is saturated: at PFA `1e-2`, `balanced_mild` already reaches `62/62` weak hits.

### D5H thesis

Before any new training, D5H should identify which input representations have a label-valid, leakage-free, non-saturated, fixed-PFA-calibrated audit path. Only representations that pass this gate may later enter minimal model sanity.

## 2. Claims and anti-claims

| item | statement | status |
|---|---|---|
| Primary claim | A no-training protocol audit can decide which representation, if any, is safe to test next. | planning target |
| Supporting claim | Current Gao77 labels support range and approximate azimuth, but not confirmed Doppler/RAD/temporal claims. | supported by local metadata |
| Anti-claim | Representation change alone is already proven to solve weak-target preservation. | not supported |
| Anti-claim | A model/loss escalation should happen before label/proxy gates pass. | rejected |

## 3. Representations to audit

| representation | priority | reason |
|---|---|---|
| range_only | MUST | baseline and known failure surface; needed for all relative comparisons |
| corrected_RD | MUST | strongest D5C smoke signal, but D5E proxy saturated |
| corrected_RA | MUST | needs calibrated angle validation because D5C RA is inconclusive |
| RAD | SHOULD | natural complete dense tensor, but label feasibility uncertain |
| temporal_RD | SHOULD | may reduce weak-target ambiguity via persistence |
| temporal_RA | SHOULD | only after RA projection is validated |
| temporal_RAD | NICE | high value but likely high label and memory burden |
| STFT_spectrogram | SHOULD | no-training signal-level separability before range collapse |
| complex_IQ | SHOULD | phase preservation audit for raw/IF or IQ availability |
| complex_RD | SHOULD | RD with phase-consistency and no-harm checks |
| raw_ADC | SHOULD | available as complex `128x255x4x2`; high value but high cost |
| raw_ADC_learnable_FFT | NICE | future route only, no training in D5H |
| radar_point_cloud | NICE | useful as auxiliary diagnostic; weak targets may be below CFAR |

## 4. Phase 0: Data/label feasibility

Phase 0 checks whether each label source is true, proxy, absent, or unusable for claims.

| label/protocol item | current Gao77 status | D5H action |
|---|---|---|
| range | available/proxy-to-true from label `py` and manifest-derived range | verify mapping and mask widths |
| azimuth | available as label `px`/manifest-derived azimuth, but calibration uncertain | run RA projection and axis consistency audit |
| Doppler | not a true label | only use validated proxy; never claim confirmed RD performance |
| RAD box | absent | feasibility only; compare with CARRADA/RADDet schema conceptually |
| temporal tracking | absent | no-training track consistency only if frame continuity is reliable |
| velocity proxy | proxy only | estimate only for audit; no performance claim |
| weak target definition | proxy from clean/interfered peak, contrast, CFAR margin, or train-only percentile | require train-only threshold and weak_n check |
| clean/interfered pairing | available for synthetic FMCW-like interference pipeline | label as synthetic FMCW-like, not real physical interference |
| fixed-PFA calibration | available in earlier pipeline | recalibrate per representation and PFA level |

Phase 0 output: `D5H_PHASE0_LABEL_FEASIBILITY.md`.

## 5. Phase 1: No-training representation audit

Phase 1 computes deterministic diagnostics only. It does not train a model and does not compare weak weighting.

Required diagnostics for every representation:

1. projection hit rate;
2. weak target projection hit rate;
3. weak_n;
4. overlap ratio;
5. weak overlap ratio;
6. separability proxy;
7. target/background contrast;
8. fixed-PFA calibration at PFA `1e-2`;
9. fixed-PFA calibration at PFA `1e-3`;
10. stricter PFA sanity, suggested `5e-4` and `1e-4`;
11. baseline saturation risk;
12. label leakage risk;
13. proxy optimism risk;
14. clean no-harm feasibility;
15. memory/time cost on GTX1650 4GB.

## 6. Core audit blocks

### Block A: Range-only baseline audit

- Purpose: preserve known negative baseline and quantify why range collapse is fragile.
- Checks: weak_n, overlap, separability, PFA calibration, saturation.
- Success: none needed for continuation; it is baseline only.
- Failure interpretation: range-only remains a negative/diagnostic surface.

### Block B: Corrected RD audit

- Purpose: determine if RD has a non-saturated, non-leaky Doppler protocol.
- Checks: Doppler proxy source, clean-peak dependence, local-window alternatives, weak_n, PFA `1e-2/1e-3`.
- Pass requires no clean-peak leakage and non-saturated baseline.
- Failure interpretation: RD remains proxy-only and cannot justify training.

### Block C: Corrected RA audit

- Purpose: decide if RA is physically calibrated enough for fixed-PFA weak-target evaluation.
- Checks: angle formula, axis sign, fftshift mode, projection hit under fixed-PFA, weak target hit, mean angle error, mask sensitivity.
- Pass requires physically plausible mapping and weak fixed-PFA hit rate not near zero.
- Failure interpretation: RA stays inconclusive, not invalid.

### Block D: RAD and temporal feasibility audit

- Purpose: decide whether RAD/temporal labels can be constructed without leakage.
- Checks: target boxes/masks, track consistency, label source, weak_n, memory estimate.
- Pass requires label source and no leakage.
- Failure interpretation: use external datasets only as protocol references, not direct continuation.

### Block E: STFT / complex / raw ADC audit

- Purpose: check whether richer signals preserve phase/time-frequency information with feasible memory.
- Checks: input shape, complex availability, signal-level separability, clean no-harm definition, 4GB footprint.
- Pass requires a deterministic scoring path and clean no-harm feasibility.
- Failure interpretation: raw/complex stays longer-term, not immediate training.

## 7. Gate to minimal model sanity

A representation may enter later minimal model sanity only if all conditions hold:

1. label or proxy source is explicit and documented;
2. no test leakage;
3. test weak_n `>=100`; if `<100`, mark as weak evidence and do not use for main claim;
4. baseline is not saturated at main PFA; reject if weak Pd is `1.0` or close enough that `+5` hits is impossible;
5. PFA `1e-2` and `1e-3` calibrate;
6. overlap ratio improves over range_only;
7. weak separability improves over range_only;
8. clean no-harm can be defined;
9. a sanity subset fits GTX1650 4GB;
10. protocol does not rely on overly optimistic clean peak proxy.

If no representation passes, stop weak weighting and write the project as negative/protocol limitation.

## 8. Run order

| Run ID | block | action | status |
|---|---|---|---|
| R008H-P0 | Phase 0 | inventory labels, raw ADC shape, range/azimuth/Doppler/RAD/temporal support | TODO |
| R008H-P1A | Block A | range-only baseline audit | TODO |
| R008H-P1B | Block B | corrected RD no-training audit | TODO |
| R008H-P1C | Block C | corrected RA calibration and fixed-PFA audit | TODO |
| R008H-P1D | Block D | RAD and temporal feasibility audit | TODO |
| R008H-P1E | Block E | STFT/complex/raw ADC cost and no-harm audit | TODO |
| R008H-GATE | Gate | decide whether any representation may enter minimal model sanity | TODO |

## 9. Compute and data budget

- No GPU training.
- CPU-first metric computation where possible.
- GTX1650 4GB check is only a memory estimate or tiny tensor dry-run, not model training.
- No new dataset downloads.
- External datasets CARRADA/RADDet/RADIal are protocol references only unless a later task explicitly requests acquisition.

## 10. Final checklist

- [ ] All representations have explicit labels/proxies.
- [ ] Every proxy has leakage and optimism risk marked.
- [ ] PFA `1e-2` and `1e-3` are calibrated per representation.
- [ ] Saturation is detected before training.
- [ ] weak_n is sufficient or claims are downgraded.
- [ ] GPU feasibility is estimated before any future model.
- [ ] D6 remains forbidden.
