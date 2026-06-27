# D3 Gao77 Baseline Sanity 报告

生成时间：2026-06-26 21:40:01  
阶段：D3，仅 range-only baseline sanity  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次只执行 D3。没有进入 D4-D14，没有做 weak-target full loss、focal loss、balanced BCE、false alarm penalty、clean identity full method 或 3 seeds；没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D3 是否通过 | 未通过 |
| MSE/MAGMSE baseline 是否训练成功 | 是 |
| ordinary differentiable CA-CFAR BCE baseline 是否训练成功 | 是 |
| 两者 loss 是否下降 | 是 |
| 两者输出是否稳定 | 是 |
| BCE fixed-PFA 检测指标是否不差于 MSE | 是 |
| clean-input no-harm 是否有问题 | 是 |
| narrow/default mask 结论是否一致 | 是 |
| all targets 与 non-overlap-only 是否一致 | 是 |
| 是否建议进入 D4 | 否 |
| 下一步 | 不建议进入 D4；ordinary BCE 的 fixed-PFA 检测指标不差于 MSE，但 clean-input no-harm 和幅度重建稳定性失败，应先检查 CFAR BCE loss 的数值尺度、mask 口径、temperature / learning rate，以及是否需要最小重建约束。 |

## 3. 训练 Loss

| baseline | tiny_initial | tiny_final | tiny_drop | train_initial | train_final | train_drop | val_initial | val_final | val_drop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MSE/MAGMSE | 0.243000 | 0.003347 | 0.9862 | 0.026616 | 0.002951 | 0.8891 | 0.011100 | 0.002813 | 0.7466 |
| ordinary BCE | 1.001226 | 0.673825 | 0.3270 | 2.152940 | 1.384098 | 0.3571 | 1.293124 | 0.799237 | 0.3819 |

## 4. Baseline 对比

默认 mask、clean_peak_percentile、PFA=1e-2：

| name | mse_db_to_clean | measured_pfa | false_alarm_count | background_cell_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 | noise_floor_change_db | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.0000 | 0.0105 | 149.0000 | 14165.0000 | 0.3511 | 0.9756 | 1.0000 | 0.5556 | 0.1298 | 0.0000 | 0.0000 |
| MSE output medium | 0.0946 | 0.0104 | 147.0000 | 14165.0000 | 0.3626 | 0.9756 | 1.0000 | 0.5633 | 0.1322 | 0.0102 | 0.0795 |
| BCE output medium | 96.3379 | 0.0086 | 122.0000 | 14165.0000 | 0.7061 | 0.8537 | 0.8140 | 0.7494 | 0.3296 | 0.4059 | 4.5569 |
| MSE model(clean) | 0.0371 | 0.0105 | 149.0000 | 14165.0000 | 0.3550 | 0.9756 | 1.0000 | 0.5581 | 0.1307 | -0.0304 | 0.0331 |
| BCE model(clean) | 96.6465 | 0.0090 | 127.0000 | 14165.0000 | 0.7176 | 0.8902 | 0.8140 | 0.7649 | 0.3470 | -0.0828 | 4.6000 |

## 5. 判断

- D3 的判断对象是 ordinary BCE 是否至少不明显差于 MSE/MAGMSE，而不是 proposed method 是否有效。
- 如果进入 D4，D4 应只做 tuned balanced BCE 或 focal loss 强 baseline；weak-target-weighted loss 必须留到 D5。
- severe interference 仅作为 stress test，不作为 D3 主要训练判断。

## 6. 输出文件

结果目录：

`G:\mineru_output\results\d3_gao77_baseline_sanity`

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\d3_figures`

关键文件：

- `d3_config.json`
- `d3_dataset_manifest.csv`
- `d3_model_summary_mse.txt`
- `d3_model_summary_bce.txt`
- `d3_training_loss_mse.csv`
- `d3_training_loss_bce.csv`
- `d3_fixed_pfa_metrics.csv`
- `d3_clean_no_harm_metrics.csv`
- `d3_reconstruction_metrics.csv`
- `d3_metrics_by_mask.csv`
- `d3_metrics_non_overlap_only.csv`
- `d3_metrics_by_sequence.csv`
- `d3_metrics_by_class_group.csv`
- `d3_baseline_comparison_summary.csv`

## 7. D4 建议

不建议进入 D4；ordinary BCE 的 fixed-PFA 检测指标不差于 MSE，但 clean-input no-harm 和幅度重建稳定性失败，应先检查 CFAR BCE loss 的数值尺度、mask 口径、temperature / learning rate，以及是否需要最小重建约束。
