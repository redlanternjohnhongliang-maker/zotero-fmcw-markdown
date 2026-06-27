# GO_NOGO_CHECKLIST：最小 Kill-Test 版

**日期**：2026-06-25  
**用途**：两周结束判断是否值得继续  
**主问题**：相比 ordinary differentiable CA-CFAR detection-aware BCE，full loss 是否能在 fixed PFA 下提升 weak-target Pd，同时不增加 false alarm、不损坏 clean input？

## Fixed PFA 定义

- 使用 cell-level PFA。
- background cells = clean RD/RDA 图中非目标区域。
- threshold 在 validation set 上选择，使 PFA 达到 `1e-2` 或 `1e-3`。
- test set 上报告 weak/mid/strong target Pd。
- 所有方法使用相同 evaluation protocol。

## Soft Go

| 条件 | 通过标准 | 状态 |
|---|---|---|
| weak-target Pd | fixed PFA 下有明显提升 | TODO |
| false alarm | 没有明显上升 | TODO |
| clean input | 没有明显退化 | TODO |

Soft Go 只表示值得继续第二周必要验证，不表示可以写论文。

## Hard Go

| 条件 | 通过标准 | 状态 |
|---|---|---|
| seeds | 3 seeds 趋势一致 | TODO |
| strong baseline | full loss 明显超过 tuned balanced BCE / focal loss | TODO |
| weak Pd / miss | fixed PFA 下 weak Pd 提升 5-10 个百分点，或 miss rate 降低 15-20% | TODO |
| false alarm | false alarm 不上升 | TODO |
| clean input | clean-input 检测指标几乎不退化 | TODO |
| CFAR robustness | 改 threshold/window/guard cell 后趋势不消失 | TODO |

Hard Go 才允许进入完整论文实验计划。

## No-Go

任一条成立，就不继续包装成方法论文：

- [ ] 只提升平均 F1；
- [ ] weak-target 提升来自 false alarm 增加；
- [ ] focal loss / balanced BCE 调好后效果接近 full loss；
- [ ] clean identity loss 只改善 MSE，不改善检测；
- [ ] 改 CFAR 参数后效果消失。

## 第一阶段不强制做

以下实验不作为两周 kill-test 必须项：

- random weak weights；
- strong-target weights；
- OS-CFAR / GO-CFAR；
- RDLR-Net / DiffRIM / RIMformer；
- 大规模真实车载 benchmark；
- OOD / uncertainty / TTA。

只有 Hard Go 后，才考虑把这些作为第二阶段补充。

## No-Go 后 Pivot

1. 如果 weak weighting 不赢 tuned focal/balanced：转向 fixed-PFA 评测协议或负结果分析。
2. 如果 weak Pd 靠 false alarm 换来：转向 threshold-aware calibration。
3. 如果 clean identity 只改善 MSE：转向 clean-input degradation benchmark。
4. 如果 CFAR 参数一改就失效：转向 CFAR-parameter robust training。

