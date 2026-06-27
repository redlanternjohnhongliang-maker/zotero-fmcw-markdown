# D2A Gao77 Small Model Sanity 报告

生成时间：2026-06-26 21:14:58  
阶段：D2A，仅 range-only simple FCN / 小 batch overfit sanity  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次只执行 D2A。没有进入 D3-D14，没有跑正式 baseline，没有做 MSE vs BCE vs focal 对比，没有实现 weak-target full loss，没有做 3 seeds，没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D2A 是否通过 | 通过 |
| 使用模型 | simple FCN |
| 输入输出 shape 是否正确 | 是 |
| tiny batch 是否能 overfit | 是 |
| small subset loss 是否下降 | 是 |
| 输出是否有 NaN/Inf | 否 |
| model output 是否比 interfered 更接近 clean | 是 |
| fixed-PFA 是否能评估 model output | 是 |
| clean-input no-harm 是否明显失败 | 否 |
| narrow/default mask 趋势是否一致 | 是 |
| all targets 与 non-overlap-only 是否一致 | 是 |
| 当前是否建议进入 D3 | 是 |
| 下一步 | 可以进入 D3，但 D3 仍应先从 MSE/MAGMSE baseline 和 ordinary differentiable CA-CFAR BCE 开始，不要直接上 weak-target full loss。 |

## 3. 训练 Sanity

| stage | initial_loss | final_loss | loss_drop_fraction | input_mse_db | output_mse_db |
|---|---:|---:|---:|---:|---:|
| tiny_batch | 0.303683 | 0.001412 | 0.9954 | 5.708576 | 0.026537 |
| small_subset_train | 0.203344 | 0.003085 | 0.9848 | 3.822420 | 0.058001 |
| small_subset_val | 0.197078 | 0.005307 | 0.9731 | 3.704642 | 0.099761 |

## 4. Fixed-PFA Sanity

默认 mask、clean_peak_percentile、PFA=1e-2：

| input_type | sir_name | mse_db_to_clean | measured_pfa | false_alarm_count | background_cell_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 | noise_floor_change_db | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean |  | 0.0000 | 0.0130 | 74.0000 | 5675.0000 | 0.5294 | 0.9592 | 1.0000 | 0.7848 | 0.1838 | 0.0000 | 0.0000 |
| interfered | medium | 7.2726 | 0.0125 | 71.0000 | 5675.0000 | 0.3971 | 0.9184 | 1.0000 | 0.7152 | 0.1452 | 0.3123 | 0.0122 |
| model_output | medium | 0.1326 | 0.0130 | 74.0000 | 5675.0000 | 0.5294 | 0.9796 | 1.0000 | 0.7911 | 0.1838 | 0.0411 | 0.1109 |
| model_clean |  | 0.0287 | 0.0136 | 77.0000 | 5675.0000 | 0.5294 | 0.9592 | 1.0000 | 0.7848 | 0.1835 | 0.0047 | 0.0259 |

## 5. Clean-Input No-Harm

model(clean) 默认 mask、PFA=1e-2：

| mse_db_to_clean | measured_pfa | false_alarm_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 | noise_floor_change_db | target_peak_bias_db_mean | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.0287 | 0.0136 | 77.0000 | 0.5294 | 0.9592 | 1.0000 | 0.7848 | 0.1835 | 0.0047 | 0.0006 | 0.0259 |

## 6. 注意事项

- D2A 只说明训练链路、shape、loss 和 fixed-PFA evaluation 能跑通，不说明方法优于 baseline。
- severe interference 只作为 stress test，不作为 D2A 主要训练 sanity 判断。
- 后续 D3 必须单独跑 MSE/MAGMSE baseline 和 ordinary differentiable CA-CFAR BCE，不能把 D2A 的 simple FCN 结果当正式 baseline。

## 7. 输出文件

结果目录：

`G:\mineru_output\results\d2a_gao77_small_model_sanity`

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\d2a_figures`

关键文件：

- `d2a_config.json`
- `d2a_dataset_manifest.csv`
- `d2a_model_summary.txt`
- `d2a_training_loss.csv`
- `d2a_tiny_batch_overfit_metrics.csv`
- `d2a_small_subset_metrics.csv`
- `d2a_fixed_pfa_metrics.csv`
- `d2a_clean_no_harm_metrics.csv`
- `d2a_metrics_by_mask.csv`
- `d2a_metrics_non_overlap_only.csv`
- `d2a_metrics_by_sequence.csv`
- `d2a_metrics_by_class_group.csv`

## 8. D3 建议

可以进入 D3，但 D3 仍应先从 MSE/MAGMSE baseline 和 ordinary differentiable CA-CFAR BCE 开始，不要直接上 weak-target full loss。
