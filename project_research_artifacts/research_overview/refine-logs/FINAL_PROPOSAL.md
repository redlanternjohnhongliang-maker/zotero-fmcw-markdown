# FINAL_PROPOSAL：固定虚警率约束下的弱目标保护型 FMCW/4D 雷达干扰抑制训练

**日期**：2026-06-25  
**模式**：REVISE / kill-test  
**英文暂定题目**：Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**最终状态**：REVISE，进入两周 kill-test，不进入完整论文计划

## Problem Anchor

- **Bottom-line problem**：现有 FMCW/4D 雷达接收端干扰抑制方法常优化 MSE、SINR、EVM 或普通检测图指标，但车载感知真正关心的是固定虚警率条件下弱目标是否还能被检测到，以及抑制过程是否引入额外虚警或损坏 clean input。
- **Must-solve bottleneck**：普通 detection-aware training 已经能提升整体 CFAR F1，但不一定保护低 SNR、低 RCS、低峰值目标，也不一定保证 false alarm budget 和 clean-input no-harm。
- **Non-goals**：不提出新 CFAR；不提出新 detector；不提出新 RIM backbone；不声称首次 detection-aware training；不声称首次弱目标增强；不提供 safety guarantee。
- **Constraints**：两周 kill-test；第一阶段优先 AENN，复现困难则 simple FCN；不使用 RDLR-Net、DiffRIM、RIMformer 作为主模型；ARIM-v2 只作为数据/benchmark 参考。
- **Success condition**：相对 ordinary differentiable CA-CFAR detection BCE，在 fixed PFA 下 weak-target Pd 提升 5-10 个百分点，或 weak-target miss rate 降低 15-20%；false alarm 不上升；clean-input 检测指标几乎不退化；3 个随机种子趋势一致；换 CFAR 参数后效果不消失。

## 最终 Thesis

在已有 differentiable CA-CFAR detection-aware training 基础上，研究一种**固定 false alarm budget 约束下的弱目标保护训练协议**：通过弱目标分层权重、背景虚警惩罚和 clean-input identity 约束，使接收端干扰抑制模型在低 SNR / 低 RCS / 低峰值目标上获得更高检测概率，同时避免 clean-input degradation 和强目标性能退化。

## Dominant Contribution

**主贡献不是某个单独 loss 项，而是 fixed-PFA weak-target no-harm training protocol。**

它包含三件必须同时成立的东西：

1. 弱目标分层定义和训练权重；
2. 固定 PFA 下的 false-alarm-aware 训练与评估；
3. clean-input no-harm 检验。

如果实验只证明其中一项有效，这个方向不够支撑方法论文。

## Explicit Non-Contributions

本文不主张：

- 新的 CA-CFAR 算法；
- 新的雷达 detector；
- 新的 AENN/FCN/RIM backbone；
- 新的大模型或 foundation model；
- 理论 safety guarantee；
- 全场景 4D radar perception 解决方案。

## Proposed Method

### Base Pipeline

第一阶段采用已有 detection-aware RIM pipeline：

```text
interfered radar input
  -> AENN 或 simple FCN mitigation model
  -> restored RD/RDA map
  -> differentiable CA-CFAR layer
  -> detection map
  -> task loss
```

训练时可使用 clean RD/RDA map、target mask、background mask 和 clean-input samples。推理时不需要弱目标标签或 clean target 强度。

### Weak Target Definitions

必须比较至少两种弱目标定义：

**定义 A：CFAR-margin weak target**

clean RD/RDA 图中，目标峰值与 CA-CFAR threshold 的 margin 较小：

```text
margin = target_peak_power - local_CFAR_threshold
```

margin 位于目标样本低分位数，或接近 0 的目标定义为 weak。

**定义 B：low-energy weak target**

按以下任一训练可得标签或仿真元信息定义：

- 低 SNR；
- 低 RCS；
- target peak 位于 clean target peak distribution 的低分位数；
- 目标幅度低于某个 percentile 阈值。

两种定义都要报告结果。若只有一种定义有效，结论必须收窄。

### Training Objectives to Compare

必须比较以下训练目标：

1. MSE / MAGMSE baseline；
2. ordinary differentiable CA-CFAR detection BCE；
3. balanced BCE；
4. focal loss；
5. weak-target-weighted detection loss；
6. weak-target-weighted detection loss + false alarm penalty；
7. weak-target-weighted detection loss + false alarm penalty + clean-input identity loss。

### Full Loss Candidate

最终候选 loss 只作为 kill-test 假设，不预设一定有效：

```text
L = L_rec
  + lambda_det * L_det
  + lambda_weak * L_weak_det
  + lambda_fa * L_false_alarm
  + lambda_id * L_clean_identity
```

其中：

- `L_rec`：MSE、MAGMSE 或幅相重建损失；
- `L_det`：ordinary differentiable CA-CFAR detection BCE；
- `L_weak_det`：对 weak target bins 或 weak target neighborhoods 加权的 detection loss；
- `L_false_alarm`：背景区域检测响应惩罚，目标是在 fixed PFA 条件下不增加 false alarm；
- `L_clean_identity`：clean input 经过模型后应保持检测结果和目标幅度，不被过度抑制。

### Inference Path

推理阶段仍然简单：

```text
input radar frame -> mitigation model -> restored map -> normal detector/evaluator
```

不引入额外 gate、uncertainty module、OOD detector、method selector 或多模型 ensemble。

## Why This Is the Smallest Adequate Route

审稿风险来自“这只是堆 loss”。因此第一阶段必须保持 backbone 和 pipeline 简单，让实验只回答一个问题：

**在普通 detection-aware BCE 已经存在的情况下，弱目标分层权重、虚警预算惩罚和 clean no-harm 是否带来不可由 balanced BCE / focal loss 解释的收益？**

如果不能，方向应被 kill 或 pivot。

## Claim-Driven Validation Sketch

### Claim 1：固定 PFA 下弱目标检测改善

- **最小实验**：同一 backbone、同一数据划分、同一 CFAR 参数，对比 ordinary detection-aware BCE 与 full loss。
- **决定性指标**：weak-target Pd@PFA=1e-2 / 1e-3，weak-target miss rate。
- **成功证据**：weak-target Pd 提升 5-10 个百分点，或 miss rate 降低 15-20%，false alarm 不上升。

### Claim 2：改进不是普通 loss weighting trick

- **最小实验**：对比 balanced BCE、focal loss、random weak weights、strong-target weights。
- **决定性指标**：weak/mid/strong 分层 Pd、FAR、clean-input degradation。
- **成功证据**：真实 weak-target weights 显著优于 random/strong weighting，且 focal/balanced BCE 调参后仍不能达到同样 fixed-PFA weak-target 改善。

### Claim 3：clean-input no-harm

- **最小实验**：无干扰 clean input 直接过模型，对比 detection-aware BCE 与 full loss。
- **决定性指标**：clean-input CFAR F1、AP、FPR、SINR、SSIM、target amplitude bias。
- **成功证据**：full loss 不降低 clean-input 检测质量，且不会抹掉弱目标。

## Kill-Test Verdict Before Running

- **当前 verdict**：REVISE，但值得两周 kill-test。
- **进入完整论文计划条件**：必须满足 Go checklist 中至少主要 Go 条件。
- **立即 No-Go 条件**：如果 focal loss / balanced BCE 调好后和 proposed full loss 差不多，则不应继续包装成方法论文。

