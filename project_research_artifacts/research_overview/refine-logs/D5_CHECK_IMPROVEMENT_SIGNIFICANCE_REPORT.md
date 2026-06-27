# D5-check Improvement Significance 报告

生成时间：2026-06-27 12:46:18  
阶段：D5-check，仅检查 D5 weak-target-weighted improvement significance  
边界：没有进入 D6，没有加入 false alarm penalty、clean identity full method 或 proposed full loss。

## 1. 总体结论

| 问题 | 结论 |
|---|---|
| D5 的 weak Pd 提升对应多检测了几个 weak target | 1 个 |
| 是否可能只是 1 个或少数目标造成 | 是 |
| 是否标记为 statistically weak signal | 是 |
| 3 seeds 下 D5 平均是否超过 balanced_mild | 否 |
| 提升是否大于随机 seed std | 否 |
| narrow/default mask 是否一致 | 否 |
| all/non-overlap-only 是否一致 | 否 |
| PFA=1e-3 下是否仍有提升 | 否 |
| clean no-harm 是否正常 | 是 |
| 是否建议继续 D6 | 否 |
| 下一步 | 暂不建议进入 D6；优先修 weak target 定义，并检查模型容量或升级 RD/RA 表示，当前 weak weighting 更接近弱证据/负结果 |

## 2. Hit-count 差异

主口径：medium / default mask / all targets / PFA=1e-2。

| 指标 | balanced_mild | weak_peak_w2p0 | 差异 |
|---|---:|---:|---:|
| weak target 总数 | 262 | 262 | 0 |
| weak target hit count | 100 | 101 | 1 |
| weak target miss count | 162 | 161 | -1 |
| weak Pd | 0.3817 | 0.3855 | 0.0038 |
| mid hit count | 80 | 80 | 0 |
| strong hit count | 43 | 43 | 0 |

结论：这个 D5 原始提升只多 hit `1` 个 weak target，应视为统计上很弱的信号。

## 3. Mask / Scope / PFA Robustness

| mask_name | target_scope | target_pfa | balanced_weak_pd | d5_weak_pd | weak_pd_delta | weak_hit_delta | d5_beats_balanced | evidence_level |
|---|---|---|---|---|---|---|---|---|
| narrow | all | 0.0100 | 0.2716 | 0.2716 | 0.0000 | 0.0000 | 0.0000 | weak |
| default | all | 0.0100 | 0.3817 | 0.3855 | 0.0038 | 1.0000 | 1.0000 | weak |
| default | all | 0.0010 | 0.2366 | 0.2405 | 0.0038 | 1.0000 | 1.0000 | weak |
| default | non_overlap_only | 0.0100 | 0.3757 | 0.3810 | 0.0053 | 1.0000 | 1.0000 | weak |

## 4. 3 Seeds Mini-check

主口径 3 seeds 聚合：

| method | n_seeds | weak_pd_mean | weak_pd_std | mid_pd_mean | mid_pd_std | strong_pd_mean | strong_pd_std | measured_pfa_mean | false_alarm_count_mean | model_clean_mse_db_to_clean_mean | target_peak_abs_bias_db_mean_mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| balanced_mild | 3.0000 | 0.3766 | 0.0058 | 0.9756 | 0.0000 | 1.0000 | 0.0000 | 0.0105 | 148.6667 | 0.0427 | 0.1262 |
| weak_peak_w2p0 | 3.0000 | 0.3690 | 0.0172 | 0.9756 | 0.0000 | 1.0000 | 0.0000 | 0.0105 | 148.3333 | 0.0448 | 0.1135 |

3 seeds 平均 weak Pd gain = `-0.007634`。  
balanced std = `0.005830`，D5 std = `0.017211`。  
是否大于两者 std：`False`。

## 5. Split Robustness Mini-check

| mask_name | target_scope | target_pfa | balanced_weak_pd | d5_weak_pd | weak_pd_delta | weak_hit_delta | d5_beats_balanced |
|---|---|---|---|---|---|---|---|
| narrow | all | 0.0100 | 0.3316 | 0.3422 | 0.0107 | 2.0000 | 1.0000 |
| narrow | all | 0.0010 | 0.1176 | 0.1176 | 0.0000 | 0.0000 | 0.0000 |
| narrow | non_overlap_only | 0.0100 | 0.3140 | 0.3471 | 0.0331 | 4.0000 | 1.0000 |
| narrow | non_overlap_only | 0.0010 | 0.1488 | 0.1488 | 0.0000 | 0.0000 | 0.0000 |
| default | all | 0.0100 | 0.4615 | 0.4923 | 0.0308 | 6.0000 | 1.0000 |
| default | all | 0.0010 | 0.2718 | 0.2821 | 0.0103 | 2.0000 | 1.0000 |
| default | non_overlap_only | 0.0100 | 0.5263 | 0.5526 | 0.0263 | 3.0000 | 1.0000 |
| default | non_overlap_only | 0.0010 | 0.3509 | 0.3596 | 0.0088 | 1.0000 | 1.0000 |

## 6. 决策

按照你给的进入 D6 条件，当前 **不建议进入 D6**。

核心原因：

- 原始 D5 主口径只多 hit `1` 个 weak target；
- 这是 statistically weak signal；
- mask / non-overlap / PFA=1e-3 只要有一个口径不支持，就不能把 D5 当成稳定有效信号；
- 下一步更应该先修 weak target 定义，或检查模型容量 / 升级 RD/RA 表示；也可以把当前 range-only weak weighting 记录为负结果。

## 7. 输出文件

结果目录：`G:\mineru_output\results\d5_check_improvement_significance`  
图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d5_check_figures`
