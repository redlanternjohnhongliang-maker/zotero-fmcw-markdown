# D5G Failure Cause Analysis

**Date**: 2026-06-27  
**Scope**: Judge why weak-target weighting has not produced defensible gains from D5-check through D5E.

## Bottom line

当前失败的最稳解释不是“simple FCN 太小”，而是 **label / proxy / evaluation protocol 不够可靠，加上 range-only representation 信息不足**。模型容量和 loss design 可能有影响，但现有证据不足以把它们排在前面。

## Cause ranking

| rank | cause | likelihood | evidence | what is not proven |
|---:|---|---|---|---|
| 1 | label/proxy protocol | high | D5D RD boxes use range labels + clean-RD Doppler peak projection; D5E labels are mixed proxy and saturated across proxy variants. | 不能说 true RD/RAD labels 下也会失败。 |
| 2 | evaluation/task saturation | high | D5E PFA=1e-2: `balanced_mild` already reaches weak hits `62/62`, weak Pd `1.0`; q/mask/proxy variants show no remaining gain room. | 不能说 ceiling effect 是唯一失败原因，因为 PFA=1e-3 仍不支持 weak weighting。 |
| 3 | input representation limitation | medium-high | range-only loses Doppler/angle/phase/temporal cues; D5-diagnosis found overlap contamination; literature strongly prefers RD/RA/RAD/temporal/raw or complex inputs. | 还没有 label-valid representation comparison，所以不能把 input 写成 confirmed primary bottleneck。 |
| 4 | data limitations / weak_n | medium | D5E q30 test weak_n is 62; one hit equals Pd 0.0161; small sample makes +1/+2 hits fragile. | 不能仅用 weak_n 小来解释所有负结果。 |
| 5 | loss design | medium-low | weak weighting was too coarse and did not survive repaired definitions or stricter PFA. | 不能证明所有 weak-target-aware loss 都无效。 |
| 6 | model capacity | low-to-uncertain | D5B capacity probes did not produce robust gain; wider FCN did not solve the issue; shallow U-Net was negative in earlier checks. | 不能排除 better model 在 valid protocol 下有用，但不应现在换大模型。 |
| 7 | detector / fixed-PFA protocol | low as a change target | Fixed-PFA is the right operating-point comparison; the problem is label/saturation validity, not the existence of fixed-PFA itself. | 不应修改 fixed-PFA main evaluation protocol。 |

## Question-by-question answers

### 1. 除了 RD 和 RA，是否应考虑 RAD / temporal / raw ADC / complex input？

应该考虑，但顺序必须保守：

1. 先做 RD/RA/RAD label feasibility。
2. 再做 no-training representation audit。
3. 只有通过 label-valid、non-saturated、fixed-PFA stable gate 后，才进入 minimal-model sanity。
4. raw ADC / complex input 属于 longer-term，不是当前 D5 继续训练路线。

### 2. 当前失败是否主要来自 range-only 输入太简单？

只能说 **plausible but not proven**。range-only 的确丢了 Doppler/angle/phase/temporal 信息，也出现 overlap contamination。但 D5E 的更强证据指向 RD proxy saturation 和 label protocol failure。因此 primary cause 应写成 protocol/label/evaluation，input representation 是 secondary plausible cause。

### 3. RD proxy saturation 是否说明 RD 本身不行？

不说明。它说明 **当前 RD protocol 不行**。D5D/D5E 的 RD boxes 是 mixed proxy，不是真 Doppler GT；baseline 已饱和也让 weak weighting 无法展示增量。不能写 confirmed RD performance，也不能写 RD 无用。

### 4. RA inconclusive 是否可能是 angle mapping / projection / label 问题？

是。RA 依赖 angle calibration、sensor geometry 和 label projection。D5C 的 RA inconclusive 更像 protocol self-check 未通过，不是 RA representation 的负结论。

### 5. simple FCN 是否可能是瓶颈？

可能，但不是当前最可信瓶颈。只有在一个通过 Phase 1 的 non-saturated、label-valid representation 上，balanced baseline 与 weak weighting 都跑不动，并且 minimal capacity probes 显示更强模型确实改善 no-harm 和 weak Pd，才值得谈模型替换。

### 6. weak weighting loss 是否本身太粗？

可能。它目前只是按 weak subset 加权，不能保证 low-SNR target preservation、false alarm control、clean no-harm 和 label validity 同时成立。但现在不应继续调 loss，因为协议本身还不能可靠测量收益。

### 7. 最小可信下一步是什么？

**No-training representation protocol audit**。不训练新模型，不加 false alarm penalty，不进入 D6。检查每种 representation 的 label validity、weak_n、overlap、separability、baseline saturation、fixed-PFA calibration 和 leakage。

### 8. 如果不继续，如何写成 negative result / limitation study？

可写成：

> Under a fixed-PFA weak-target preservation protocol, range-only weak-target weighting and a mixed-proxy RD supplement did not provide robust gains. The failure analysis shows that target definition, representation collapse, proxy label design, and task saturation can dominate apparent weak-target improvements. This motivates a representation-protocol audit before further loss or model escalation.

### 9. 哪些 claims 不能写？

- 不能写 weak weighting improves weak-target preservation。
- 不能写 RD performance is confirmed。
- 不能写 RD 不行。
- 不能写 ceiling effect 是唯一失败原因。
- 不能写 synthetic FMCW-like interference 是真实物理干扰。
- 不能写 simple FCN 容量是主因。
- 不能写 fixed-PFA protocol 应被修改。
- 不能写 RIMformer/DiffRIM/RDLR-Net 是下一步主方法。

### 10. 哪些 future directions 最稳？

1. conservative negative / limitation narrative。
2. no-training representation protocol audit。
3. label-valid RAD / temporal RD sanity。
4. raw ADC / complex input feasibility as longer-term route。
5. only-after-gate model/loss redesign。

## Decision

**Do not continue weak weighting now. Do not enter D6. Pivot to D5G representation protocol audit.**
