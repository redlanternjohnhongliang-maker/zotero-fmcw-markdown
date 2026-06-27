# D3-RCA ordinary BCE failure root-cause analysis 报告

生成时间：2026-06-26 21:59:07  
阶段：D3-RCA，仅分析 ordinary differentiable CA-CFAR BCE baseline 失败原因  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次不是 D4。没有做 focal loss、balanced BCE、weak-target full loss、false alarm penalty、3 seeds，也没有引入 RDLR-Net / DiffRIM / RIMformer。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D3 failure 是否由数值域 / normalization bug 导致 | 否 |
| BCE label / mask 是否正确 | 是 |
| differentiable CFAR 是否数值稳定 | 基本稳定，未发现全 0 / 全 1 |
| sigmoid temperature 是否导致幅度极端化 | 有影响，但不是唯一主因 |
| learning rate 是否过高 | 会加重问题，但降低 LR 不能根治 |
| ordinary BCE 是否天然诱导 detection-shaping | 是 |
| 最小 reconstruction anchor 是否能修复幅度破坏 | 是，诊断上有效 |
| clean-input no-harm 失败主因 | ordinary BCE 只奖励 detection map，不约束 restored signal 保真，模型会把 clean input 也改成 detection-friendly map |
| 是否可以重新跑 D3 | 可以，但应先把 BCE baseline 改成带最小 reconstruction anchor 的诊断版，或把 pure BCE 标记为失败对照 |
| 是否仍然不建议进入 D4 | 是，先重跑修正后的 D3 |

## 3. 关键数值

reference ordinary BCE，default mask、medium、PFA=1e-2：

| 指标 | 数值 |
|---|---:|
| output MSE to clean | 44.7549 |
| model(clean) MSE to clean | 28.8811 |
| weak Pd | 0.6324 |
| F1 | 0.2593 |
| target peak abs bias | 3.8083 |

## 4. Mask / Label 检查

| mask_name | target_cell_count_train | background_cell_count_train | ignored_guard_cell_count_train | target_background_overlap_count_train | target_bce_mean_val | background_bce_mean_val | target_background_bce_contribution_ratio_val |
|---|---|---|---|---|---|---|---|
| narrow | 4696.0000 | 23016.0000 | 5056.0000 | 0.0000 | 2.9247 | 0.0529 | 10.1182 |
| default | 7090.0000 | 20974.0000 | 4704.0000 | 0.0000 | 3.3092 | 0.0492 | 19.2810 |

判断：target/background label 没有反，guard ring 没有被当成 background，BCE 只在 target/background cells 上算。

## 5. Temperature Sweep 摘要

| temperature | val_bce | output_mse_db | model_clean_mse_db | weak_pd | false_alarm_count | target_peak_abs_bias_db_mean | output_min_db | output_max_db |
|---|---|---|---|---|---|---|---|---|
| 0.5000 | 1.0832 | 26.6024 | 15.8683 | 0.5441 | 75.0000 | 2.8541 | 29.3869 | 76.8364 |
| 0.7000 | 0.8058 | 20.8542 | 8.7873 | 0.7059 | 59.0000 | 2.2452 | 34.6634 | 79.1292 |
| 1.0000 | 0.6155 | 26.6142 | 11.0641 | 0.6618 | 72.0000 | 2.1934 | 38.5073 | 83.3545 |
| 2.0000 | 0.4928 | 58.9333 | 31.3373 | 0.5588 | 52.0000 | 3.0647 | 26.0642 | 94.2776 |
| 5.0000 | 0.5497 | 123.6539 | 73.6414 | 0.5735 | 81.0000 | 4.7959 | 16.2466 | 101.2890 |

## 6. Learning Rate Sweep 摘要

| lr | val_bce | output_mse_db | model_clean_mse_db | weak_pd | false_alarm_count | target_peak_abs_bias_db_mean | output_min_db | output_max_db |
|---|---|---|---|---|---|---|---|---|
| 0.0010 | 0.8101 | 31.3765 | 16.2287 | 0.5882 | 37.0000 | 2.7436 | 29.2621 | 84.4047 |
| 0.0003 | 0.8147 | 26.8809 | 10.4745 | 0.6029 | 63.0000 | 2.3978 | 34.6505 | 80.6800 |
| 0.0001 | 0.8194 | 11.0008 | 1.6368 | 0.6029 | 52.0000 | 1.0055 | 38.1055 | 76.5657 |
| 0.0000 | 0.9654 | 7.5719 | 0.0191 | 0.4559 | 68.0000 | 0.1093 | 40.0604 | 74.3276 |

## 7. Reconstruction Anchor 诊断

最佳 clean no-harm anchor：`lambda_rec=1.0`，model(clean) MSE=0.1062，weak Pd=0.5294。

| lambda_rec | val_bce | val_mse_db_to_clean | output_mse_db_to_clean | clean_model_mse_db_to_clean | weak_pd | false_alarm_count | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|---|---|
| 0.0000 | 0.7899 | 40.0812 | 45.7974 | 28.3735 | 0.5882 | 74.0000 | 3.4524 |
| 0.0100 | 0.8117 | 1.5218 | 2.4001 | 0.9162 | 0.6324 | 69.0000 | 1.1145 |
| 0.0500 | 0.8197 | 0.5895 | 0.9634 | 0.2314 | 0.5735 | 85.0000 | 0.5532 |
| 0.1000 | 0.8227 | 0.5202 | 0.8975 | 0.1265 | 0.5441 | 70.0000 | 0.5808 |
| 0.5000 | 0.8315 | 0.4098 | 0.6979 | 0.1336 | 0.5294 | 78.0000 | 0.2637 |
| 1.0000 | 0.8348 | 0.4234 | 0.6936 | 0.1062 | 0.5294 | 73.0000 | 0.2349 |

判断：加最小 reconstruction anchor 后，幅度破坏明显下降；这说明 D3 失败主要不是 dataloader 或 normalization bug，而是 pure detection BCE 缺少 signal restoration anchor。

## 8. Clean-Input Behavior

| case | residual_abs_mean_db | target_abs_residual_mean_db | background_abs_residual_mean_db | guard_abs_residual_mean_db | residual_concentrated_in_target | background_suppressed_or_shaped |
|---|---|---|---|---|---|---|
| reference_bce_model_clean | 4.2721 | 4.2812 | 3.9162 | 6.2201 | 1.0000 | 0.0000 |

结论：ordinary BCE learns detection-shaping rather than signal restoration。

## 9. 建议

1. 不进入 D4。
2. 先重跑 D3，保留 pure BCE 作为失败对照。
3. 重新跑 D3 的 BCE baseline 建议配置：`BCE + lambda_rec * MAGMSE`，优先尝试 `lambda_rec=1.0`；同时报告 pure BCE 的 clean no-harm 失败。
4. LR 可从 `3e-05` 或 `3e-4` 起步，temperature 可优先用 `1.0-2.0` 做稳定性对照。
5. 后续如果进入 D4，D4 仍只能做 tuned balanced BCE / focal loss 强 baseline，不能直接进入 weak-target full loss。

## 10. 输出文件

结果目录：`G:\mineru_output\results\d3_rca_bce_failure_analysis`  
图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d3_rca_figures`
