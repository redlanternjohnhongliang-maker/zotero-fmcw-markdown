# GPT Handoff: D5G Representation Protocol Audit and Future Direction Study

**Date**: 2026-06-27  
**Give this file to GPT**: yes. This is the single-file summary for the next GPT discussion.  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**Current stage**: D5G study completed. D6 remains forbidden.

## 1. Actual ARIS skills used

- `/research-lit`: literature review on FMCW interference mitigation and radar representations.
- `/experiment-plan`: next-stage no-training protocol audit.
- `/result-to-claim`: independent claim gate, verdict `partial`, route `protocol study`.
- `/kill-argument`: adversarial stress test, verdict `WARN`.

## 2. Local evidence from D5D/D5E

### D5D RD-only supplementary result

- `claim_supported: no`
- RD fixed-PFA proxy ran end to end.
- Weak weighting did not improve weak targets:
  - mean weak Pd delta `0.0000`
  - mean weak hit delta `0`
  - PFA `1e-3` mean weak Pd delta `-0.0161`
  - seed 200 at PFA `1e-3`: weak Pd delta `-0.0323`, hit delta `-2`
- RD boxes use range label plus clean-RD Doppler peak projection, not true Doppler ground truth.
- Do not write confirmed RD performance.

### D5E RD proxy ceiling diagnosis

- `/analyze-results = NO-GO`
- `/experiment-audit = WARN`, `mixed_proxy`
- `/result-to-claim = partial/warn/medium`
- At PFA `1e-2`, both seeds have:
  - weak_n `62`
  - `balanced_mild` weak hits `62/62`
  - weak weighting weak hits `62/62`
  - weak Pd delta `0`
- q10/q20/q30/q40 weak thresholds all saturated.
- mask variants all saturated/no weak-weighting gain.
- proxy label variants all saturated/no weak-weighting gain.
- PFA `1e-3`: mean weak Pd delta `-0.0161`, hit delta `-1`.
- Conclusion: limited RD-proxy ceiling diagnosis, not confirmed RD performance.

## 3. Papers checked

| paper | year | why it matters |
|---|---:|---|
| A Deep Learning Approach for Automotive Radar Interference Mitigation | 2018 | early DL mitigation baseline |
| STFT beat-frequency interpolation for FMCW interference mitigation | 2019 | classical time-frequency target preservation route |
| Fully Convolutional Neural Networks for Automotive Radar Interference Mitigation | 2020 | closest FCN spectrogram/range-profile precedent |
| Deep Interference Mitigation and Denoising of Real-World FMCW Radar Signals | 2020 | real-world FMCW denoising evidence |
| Estimating Magnitude and Phase of Automotive Radar Signals under Multiple Interference Sources | 2020/2021 | phase should not be casually discarded |
| Prior-Guided Deep Interference Mitigation for FMCW Radars | 2022 | complex-valued/prior-guided mitigation |
| Sparse and Low-Rank Hankel Matrix Decomposition for FMCW interference mitigation | 2022 | classical structured decomposition |
| Radar-STDA | 2023 | temporal/spatial denoising route |
| RIMformer | 2024 | raw IF Transformer route, but not immediate main method |
| Vehicle Detection with Range-Azimuth-Doppler Tensors | 2019 | RAD tensor precedent |
| CARRADA | 2020/2021 | RA/RD/RAD labels and dense annotations |
| RODNet | 2021 | temporal RA and cross-modal labels |
| RADDet | 2021 | one-stage RAD object detector |
| FFT-RadNet / RADIal | 2022 | raw HD radar and learnable angle route |
| T-FFTRadNet | 2023 | raw ADC / Transformer detector |

## 4. Top 10 most relevant papers

| rank | paper | representation/input | relevance to D5G |
|---:|---|---|---|
| 1 | RADDet | RAD tensor | strongest precedent for RAD as next dense representation |
| 2 | CARRADA | RA/RD/RAD annotations | most relevant for label-valid protocol design |
| 3 | Fully Convolutional Neural Networks for Automotive Radar Interference Mitigation | spectrogram to range profile | closest to current FCN-style mitigation |
| 4 | Estimating Magnitude and Phase of Automotive Radar Signals | magnitude + phase | warns against magnitude/range-only collapse |
| 5 | Prior-Guided Deep Interference Mitigation for FMCW Radars | complex-valued signal | supports complex input as longer-term route |
| 6 | Radar-STDA | temporal radar maps | motivates temporal RD/RAD audit |
| 7 | RIMformer | raw IF | validates raw IF future direction but should not be immediate main method |
| 8 | RODNet | temporal RA | shows temporal/cross-modal radar labeling can help object detection |
| 9 | T-FFTRadNet | raw ADC | supports raw ADC and learnable transform future path |
| 10 | STFT beat-frequency interpolation | STFT | classical target-preserving interference repair |

## 5. Failure cause ranking

1. Label/proxy protocol failure: most likely.
2. Evaluation/task saturation: very likely.
3. Input representation limitation: plausible and important, but not proven primary.
4. Data limitations / weak_n too small: medium.
5. Loss design too coarse: possible but not first to fix.
6. Model capacity: uncertain, not primary under current evidence.

## 6. Is it a model problem?

Not primarily under current evidence. A larger model might help after a valid protocol exists, but current D5D/D5E failure is dominated by mixed proxy labels, saturation, and weak-definition issues. Do not switch to RIMformer/DiffRIM/RDLR-Net now.

## 7. Is it an input problem?

Partly yes, but not proven as the sole cause. Literature strongly suggests range-only is too weak because it drops Doppler, angle, phase, and temporal cues. However, current RD evidence is proxy-saturated, so the next step is representation audit, not a claim that RD/RAD/raw ADC already solves it.

## 8. Is it a label/evaluation problem?

Yes. This is the strongest current conclusion. RD labels are mixed proxy, weak_n is small, range-only has overlap contamination, and D5E shows baseline saturation at the main PFA.

## 9. Continue weak weighting?

No. Do not continue weak weighting now. Do not add false alarm penalty. Do not enter proposed full loss.

## 10. Enter D6?

No. D6 remains forbidden.

## 11. Recommended future route

1. Record D5 as conservative negative/diagnostic evidence.
2. Run Phase 0 data/label feasibility.
3. Run Phase 1 no-training representation audit across range-only, corrected RD, corrected RA, RAD, temporal RD/RAD, STFT, complex IQ, and raw ADC.
4. Only if a representation passes non-saturation, label validity, no leakage, weak_n, and fixed-PFA calibration gates, run minimal-model sanity.
5. Re-run result-to-claim before any D6 discussion.

## 12. Minimal next prompt

```text
/experiment-plan "D5G Phase 0/1 no-training representation protocol audit for FMCW fixed-PFA weak-target preservation after D5E NO-GO. Audit range-only, corrected RD, corrected RA, RAD, temporal RD/RAD, STFT, complex IQ, and raw ADC only for label validity, weak_n, overlap, separability, saturation, fixed-PFA calibration, leakage, and GPU cost. Do not train. Do not enter D6." -- effort: balanced, assurance: conference-ready
```

## 13. Plain-language explanation

现在不是“模型不够聪明所以失败”，更像是“考试卷本身不够可靠”。range-only 把很多雷达信息压掉了；RD 版本又用了不够真实的 Doppler proxy，而且 baseline 已经满分，weak weighting 没地方涨。更严格的 PFA 下 weak weighting 也没有变好。所以现在最稳的做法是先检查题目、标签和评分方式，再决定是否值得训练新模型。

## 14. English paper-usable conclusion

Under the current fixed-PFA weak-target evaluation protocol, weak-target-weighted training does not provide a reliable improvement over the balanced baseline. The follow-up RD-only diagnostics reveal a saturated mixed-proxy evaluation: at the main operating point, the baseline already detects all proxy weak targets, while stricter PFA settings do not recover a benefit. These results should not be interpreted as confirmed RD performance or as a universal failure of weak-target weighting. Rather, they indicate that representation collapse, proxy label validity, task saturation, and weak-target sample size must be audited before new losses or larger radar models are introduced.

## 15. Files produced in this D5G run

- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_LITERATURE_REVIEW.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_REPRESENTATION_TAXONOMY.csv`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_FAILURE_CAUSE_ANALYSIS.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_NEXT_EXPERIMENT_PLAN.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_RESULT_TO_CLAIM.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_KILL_ARGUMENT.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_PROJECT_DECISION.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\D5G_PAPER_DIRECTION_NOTES.md`
- `G:\mineru_output\results\d5g_representation_protocol_study\GPT_HANDOFF_D5G.md`

## 16. Give GPT only this file

If GPT asks for evidence, then additionally provide `D5G_LITERATURE_REVIEW.md`, `D5G_NEXT_EXPERIMENT_PLAN.md`, and the D5E analyze/result-to-claim files. Otherwise this handoff file is enough.
