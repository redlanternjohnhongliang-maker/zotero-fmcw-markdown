# EXPERIMENT_PLAN：最小两周 Kill-Test 计划

**日期**：2026-06-25  
**模式**：REVISE / kill-test only  
**方向**：固定虚警率约束下的弱目标保护型 FMCW/4D 雷达干扰抑制训练  
**英文暂定**：Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation

## 0. Kill-Test 目标

本计划只回答一个问题：

**相比 ordinary differentiable CA-CFAR detection-aware BCE，weak-target-weighted task loss 能不能在固定 PFA 下提升 weak-target Pd，同时不增加 false alarm、不损坏 clean input？**

这不是完整论文实验计划，不在两周内强行做：

- 新 backbone；
- RDLR-Net / DiffRIM / RIMformer 主模型；
- 大规模真实车载 benchmark；
- random weak weights；
- strong-target weights；
- OS-CFAR / GO-CFAR；
- OOD / uncertainty / TTA；
- method selection；
- multi-model ensemble。

这些全部放到第二阶段，只有第一阶段 Go 后再考虑。

## 1. 固定边界

- **主贡献只看**：fixed-PFA weak-target preservation。
- **基础模型**：AENN 优先；如果第 1 天跑不通，立刻切 simple FCN。
- **ARIM-v2**：只作为数据或 benchmark 参考，不作为主方法依赖。
- **identity loss**：只作为防止 clean-input 副作用的约束，不包装成主贡献。
- **比较对象**：ordinary detection-aware BCE、MSE/MAGMSE、best balanced BCE 或 best focal loss、proposed loss。

## 2. Fixed PFA Evaluation Protocol

提前写死 fixed PFA，所有方法使用同一套 evaluation protocol：

1. 使用 **cell-level PFA**。
2. `background cells = clean RD/RDA 图中非目标区域`。
3. 在 validation set 上选择 detection threshold，使 background cells 的 PFA 达到：
   - `PFA = 1e-2`
   - `PFA = 1e-3`
4. 固定 validation 得到的 threshold，在 test set 上报告：
   - weak target Pd；
   - mid target Pd；
   - strong target Pd；
   - miss rate；
   - false alarm rate；
   - CFAR F1；
   - clean-input degradation；
   - SINR / MSE 仅作为辅助指标。
5. 所有方法必须使用相同 target mask、background mask、validation threshold selection 和 test reporting protocol。

## 2.1 Gao77 D1A 标签策略

D1A 使用本地子集：

`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

类别映射固定为：

```python
GAO77_LABEL_MAP = {
    0: "person",
    1: "cyclist_alias_or_bicycle",
    2: "car",
    3: "motorbike",
    5: "bus",
    7: "truck",
    80: "cyclist",
}

GAO77_CLASS_GROUP = {
    0: "pedestrian_like",
    1: "cyclist_like",
    2: "vehicle_like",
    3: "motorbike_like",
    5: "vehicle_like",
    7: "vehicle_like",
    80: "cyclist_like",
}
```

D1A 主任务不依赖细分类，target/background mask sanity 使用 objectness。objectness target classes 固定为：

```python
[0, 1, 2, 3, 5, 7, 80]
```

`class=1` 不是官方 README 明确定义的类别；D1A 暂按 `cyclist_alias_or_bicycle` 处理，并在类别统计中与 `class=80` 合并为 `cyclist_like`。该处理依据本地核查文件：

`G:\mineru_output\refine-logs\D0B_CLASS1_SEMANTICS_CHECK.md`

D1A 报告必须注明：`class=1 is treated as cyclist-like for D1A sanity based on data audit and image inspection, not because it is explicitly defined in the official README.`

如果输出 per-class projection hit rate，必须同时输出：

- 原始 class id 统计；
- 合并后的 class group 统计。

该处理不会影响 objectness mask sanity，因为 D1A 的 target mask 只关心合法目标区域，不做类别分类。

## 3. Weak Target 定义

两周内只比较两种定义：

### Definition A：CFAR-Margin Weak Target

clean RD/RDA 图中接近 CFAR threshold 的目标：

```text
margin = clean_target_peak - local_CFAR_threshold
```

margin 较小或处于低分位数的目标定义为 weak target。

### Definition B：Low-Peak / Low-SNR / Low-RCS Weak Target

使用 clean target peak、SNR、RCS 或 target peak percentile 定义弱目标。优先采用当前数据中最容易稳定获得的一种：

- low peak percentile；
- low SNR；
- low RCS。

如果 SNR/RCS 元信息不可稳定获得，则用 low peak percentile。

## 4. 最小训练目标集合

两周 kill-test 只跑以下必要方法：

1. **MSE / MAGMSE baseline**
2. **ordinary differentiable CA-CFAR detection-aware BCE**
3. **best balanced BCE 或 best focal loss**
4. **weak-target-weighted detection loss**
5. **weak-target-weighted detection loss + false alarm penalty**
6. **full loss：weak-target-weighted + false alarm penalty + clean-input identity**

其中 balanced BCE 和 focal loss 二选一作为强 baseline；如果时间允许再补另一个。不能只用默认参数，必须给合理调参预算。

## 5. 第一周：最小闭环

| Day | 任务 | 必须输出 | 当天判断 |
|---|---|---|---|
| D1 | 打通数据、CA-CFAR、differentiable CA-CFAR、Pd/PFA 指标 | weak/mid/strong target 数量；target/background mask 检查；cell-level PFA 统计 | mask 合理、PFA 计算可解释才进入 D2 |
| D2 | 跑通 simple FCN 或 AENN；AENN 若仍跑不通，直接切 simple FCN | 小 batch overfit；loss 下降曲线；基本 CFAR F1 | backbone 能训练，不追求最终性能 |
| D3 | 跑 MSE/MAGMSE baseline 和 ordinary diff-CA-CFAR BCE | MSE/MAGMSE vs ordinary BCE 的检测指标 | ordinary BCE 检测指标不能差于 MSE/MAGMSE |
| D4 | 跑一个强 baseline：balanced BCE 或 focal loss | best balanced/focal 的调参结果 | 记录最强 baseline，防止 proposed 假胜利 |
| D5 | 跑 weak-target-weighted detection loss | fixed PFA 下 weak Pd、miss rate、FAR | 看是否相对 ordinary BCE / best focal 有初步提升 |
| D6 | 加入 false alarm penalty | weak Pd、FAR、Pd@PFA=1e-2/1e-3 | 判断弱目标提升是否不是靠 false alarm 增加换来的 |
| D7 | 加入 clean-input identity loss，并做 clean input test | clean-input CFAR F1、FPR、Pd、SINR、SSIM、target amplitude bias | clean input 不能被修坏 |

### 第一周 Soft Checkpoint

第一周结束只做 Soft Go 判断：

- weak-target Pd 在 fixed PFA 下有明显提升；
- false alarm 没有明显上升；
- clean input 没有明显退化。

如果三条都不满足，不进入第二周大规模验证，直接 pivot 或重定义 weak target。

## 6. 第二周：必要验证

| Day | 任务 | 必须输出 | 判断 |
|---|---|---|---|
| D8-D9 | 对三组核心方法做 3 seeds：ordinary BCE、best balanced/focal、full loss | 3 seeds 的 weak/mid/strong Pd、miss rate、FAR、CFAR F1 | 趋势是否一致 |
| D10 | 比较两种 weak target 定义：CFAR-margin vs low peak/SNR/RCS/percentile | 两种定义下的 fixed-PFA weak Pd 和 miss rate | 至少一种定义有效，最好趋势一致 |
| D11 | clean-input no-harm test | clean-input CFAR F1、FPR、Pd、SINR、SSIM、target amplitude bias | full loss 不能损坏 clean input |
| D12 | light / medium / severe interference 分层测试 | 三种干扰强度下 weak Pd、FAR、miss rate | proposed 不能只在单一干扰强度有效 |
| D13 | 简单 CFAR 参数泛化：只改 threshold / window / guard cell | 改参数后的 weak Pd、FAR、CFAR F1 | 趋势不能消失 |
| D14 | Go / No-Go 总结 | 一页结果表和结论 | Soft Go / Hard Go / No-Go |

## 7. Soft Go / Hard Go / No-Go

### Soft Go

满足以下三条即可继续第二周或小范围追加：

- weak-target Pd 在 fixed PFA 下有明显提升；
- false alarm 没有明显上升；
- clean input 没有明显退化。

### Hard Go

进入完整论文计划前必须满足：

- 3 seeds 趋势一致；
- full loss 明显超过 tuned balanced BCE / focal loss；
- fixed PFA 下 weak-target Pd 提升 5-10 个百分点，或 miss rate 降低 15-20%；
- false alarm 不上升；
- clean-input 检测指标几乎不退化；
- 改 CFAR threshold/window/guard cell 后趋势不消失。

### No-Go

任一条成立，就不继续包装成方法论文：

- 只提升平均 F1；
- weak-target 提升来自 false alarm 增加；
- focal loss / balanced BCE 调好后效果接近 full loss；
- clean identity loss 只改善 MSE，不改善检测；
- 改 CFAR 参数后效果消失。

## 8. Kill-Test 失败后的 Pivot

如果 No-Go，优先 pivot 到以下方向之一：

1. **fixed-PFA evaluation protocol**：如果指标显示 MSE/SINR 与 weak-target Pd 明显脱钩，就写评测协议和负结果分析。
2. **threshold-aware calibration**：如果问题主要是 PFA 控不住，转向固定 PFA 校准/阈值感知训练。
3. **clean-input degradation benchmark**：如果 identity 对 clean no-harm 有价值但主方法弱，转向 clean-input degradation benchmark。
4. **weak target definition study**：如果两种 weak target 定义差异很大，先研究弱目标定义对训练和评测的影响。
