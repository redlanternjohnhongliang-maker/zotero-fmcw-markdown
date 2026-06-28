# D5I Negative Result Positioning

**路线**: Route D  
**状态**: viable as conservative report, not as broad theory claim。  
**执行位置**: 立即维护为 failure ledger；不需要等待新训练。

## 1. 可以写成什么

当前 D5B-D5H 证据可以支撑一个保守的 negative / limitation study：

> 在 fixed-PFA weak-target preservation 协议下，naive weak weighting、range-only 表示和 mixed-proxy RD 补充实验没有产生可辩护的 weak-target preservation claim。进一步 audit 显示，label/proxy provenance、baseline saturation、weak_n、RA calibration 和 RAD/temporal label availability 会主导 claim validity。因此，在继续训练、扩大模型或进入 D6 前，必须先做 label-valid protocol/data pivot。

## 2. 不能写成什么

- 不能写 “weak weighting universally fails”。
- 不能写 “RD/RA/RAD representations are ineffective”。
- 不能写 “fixed-PFA protocol is wrong and should be changed”。
- 不能写 “model capacity is irrelevant”。
- 不能写 “synthetic protocol proves real-world mitigation”。

## 3. Reviewer 可能攻击点

| 攻击点 | 风险 | 修补 |
|---|---|---|
| 只有 negative result，没有 positive contribution | 高 | 把贡献定位为 evaluation/protocol audit，而不是方法 SOTA |
| 没有外部数据集可行性 | 高 | D5I_DATASET_FEASIBILITY_TABLE 已补 |
| classical baselines review 不够 | 中高 | 需要单独补 thresholding、STFT、RD、complex CNN、source-separation baselines |
| protocol diagram 不够清楚 | 中 | 画 fixed-PFA weak-target metric chain 和 label provenance 图 |
| Gao77 proxy 限制太局部 | 中 | 用 RADIal/RADDet/CARRADA 说明外部 label-valid 路线存在 |

## 4. 最小补强清单

1. 一页 protocol diagram：数据、label provenance、fixed-PFA threshold、weak/mid/strong PD、clean no-harm。
2. 一张 external dataset feasibility table。
3. 一节 classical baseline review：time-domain thresholding、STFT thresholding、RD denoising、complex-valued CNN、source separation。
4. 一节 limitations：Gao77 是 local proxy audit，不是普遍结论。
5. 一段 future work：controlled synthetic RAD unit test 和 RADIal/RADDet small-subset feasibility。

## 5. D5I 对 Route D 的判定

**GO as report/paper-positioning route and failure ledger.**  
最小可执行实验可走 Route B，但 Route D 应立即作为 README/roadmap 和后续论文骨架维护。如果 A/B 任一 stop 条件触发，应优先冻结负结果报告，而不是继续寻找新训练路线。
