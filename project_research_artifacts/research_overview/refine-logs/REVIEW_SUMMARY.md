# REVIEW_SUMMARY

**日期**：2026-06-25  
**Final Verdict**：REVISE / kill-test  
**输入依据**：本地 idea-discovery、novelty-check、单子 agent research-review

## Problem Anchor

固定 false alarm budget / fixed PFA 条件下，提升低 SNR / 低 RCS / 低峰值目标的检测概率，同时避免 clean-input degradation 和强目标性能退化。

## 已吸收的评审结论

| Concern | Resolution |
|---|---|
| 可微 CA-CFAR detection-aware training 已有 | 不声称首次；只在其基础上研究 fixed-PFA weak-target no-harm |
| weak weighting 可能只是 trick | 必须对比 focal/balanced/random/strong weights |
| false alarm penalty 不是单独贡献 | 作为 fixed-PFA protocol 的组成部分，不单独包装 |
| clean identity 是常规项 | 只作为 no-harm 约束，必须用 clean-input detection 指标证明 |
| 方向可能过大 | 收窄成两周 kill-test，不进入完整论文计划 |

## 当前剩余风险

- 如果 full loss 只提升平均 F1，则 No-Go。
- 如果 focal loss / balanced BCE 调好后效果接近，则 No-Go。
- 如果换 CFAR 参数后效果消失，则 No-Go。
- 如果 random weights 接近 true weak weights，则 No-Go。

