# PIPELINE_SUMMARY

**日期**：2026-06-25  
**Problem**：固定虚警率约束下的弱目标保护型 FMCW/4D 雷达干扰抑制训练  
**Final Method Thesis**：只验证 weak-target-weighted task loss 是否能相对 ordinary differentiable CA-CFAR BCE，在 fixed PFA 下提升 weak-target Pd，同时不增加 false alarm、不损坏 clean input。  
**Final Verdict**：REVISE / two-week kill-test only

## 当前执行文件

- Proposal：`refine-logs/FINAL_PROPOSAL.md`
- Minimal experiment plan：`refine-logs/EXPERIMENT_PLAN.md`
- Minimal tracker：`refine-logs/EXPERIMENT_TRACKER.md`
- Go/No-Go checklist：`refine-logs/GO_NOGO_CHECKLIST.md`

## 当前阶段只做什么

1. D1 打通数据、CA-CFAR、differentiable CA-CFAR、Pd/PFA。
2. D2 跑通 AENN 或 simple FCN；AENN 不通立刻切 simple FCN。
3. D3-D4 得到 ordinary BCE 和 tuned balanced/focal baseline。
4. D5-D7 逐步加入 weak weighting、false alarm penalty、clean identity，并做 clean input test。
5. D8-D14 做 3 seeds、两种 weak target 定义、clean no-harm、干扰强度、简单 CFAR 参数泛化和 Go/No-Go。

## 当前阶段不做什么

- 不换新 backbone；
- 不使用 RDLR-Net、DiffRIM、RIMformer 作为主模型；
- 不做 random weak weights 或 strong-target weights；
- 不做 OS-CFAR / GO-CFAR；
- 不做 OOD、TTA、uncertainty、method selection、ensemble；
- 不做完整论文实验计划。

## First Runs to Launch

1. `R001`：数据与 target/background mask sanity。
2. `R002`：CA-CFAR fixed-PFA sanity。
3. `R003`：differentiable CA-CFAR gradient sanity。
4. `R004`：AENN/simple FCN 小 batch overfit。

## Decision Rule

- **Soft Go**：weak Pd 提升、false alarm 不升、clean input 不退化。
- **Hard Go**：3 seeds 趋势一致，full loss 明显超过 tuned balanced/focal，fixed-PFA weak Pd 提升 5-10 个百分点或 miss rate 降 15-20%，CFAR 参数改动后趋势不消失。
- **No-Go**：只提升平均 F1，或提升来自 false alarm，或 tuned focal/balanced 接近 full loss，或 clean identity 不改善检测，或 CFAR 参数一改就失效。

