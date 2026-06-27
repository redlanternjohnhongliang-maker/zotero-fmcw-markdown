# D1B Gao77 Synthetic Interference Sanity 报告

生成时间：2026-06-26 17:30:18  
阶段：D1B，仅 synthetic FMCW-like interference injection sanity + fixed-PFA evaluation  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次只执行 D1B。没有训练模型，没有进入 D2-D14，没有做干扰抑制模型，没有引入 AENN / FCN / RDLR-Net / DiffRIM / RIMformer，也没有下载新数据集。

D1B uses a simplified synthetic FMCW-like mutual interference model for sanity only. 本报告不把 D1B 结果包装成方法效果，只判断 ADC 层 synthetic interference 注入和 fixed-PFA 指标链路是否可用。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D1B 是否通过 | 通过 |
| synthetic interference 是否成功注入 | 是 |
| achieved SIR 是否接近设定 | 是 |
| range profile 是否出现可见干扰 | 是，图像已保存 |
| background noise floor 是否合理上升 | 是（light 档 median 上升较轻微） |
| target peak 是否被明显污染 | 是，target peak bias 已统计 |
| Protocol A false alarm 是否增加 | 是 |
| Protocol A weak Pd 是否下降 | 是 |
| Protocol B fixed-PFA weak Pd 是否下降 | 是 |
| light / medium / severe 是否形成合理梯度 | 是 |
| narrow/default mask 趋势是否一致 | 是 |
| all targets 与 non-overlap-only 是否一致 | 是 |
| 当前是否建议进入 D2 | 是 |
| 下一步 | 可以进入 D2 simple FCN / AENN 小 batch overfit，但 D2 必须继续保留 narrow/default 与 non-overlap-only 辅助统计。 |

## 3. Achieved SIR

| sir_name | target_sir_db | num_interferers | clean_signal_power_mean | interference_power_mean | achieved_sir_db_mean | achieved_sir_db_std | achieved_sir_abs_error_db_mean |
|---|---|---|---|---|---|---|---|
| light | 10.0000 | 1.0000 | 1416.9483 | 141.6948 | 10.0000 | 0.0000 | 0.0000 |
| medium | 0.0000 | 2.0000 | 1416.9483 | 1416.9483 | 0.0000 | 0.0000 | 0.0000 |
| severe | -10.0000 | 3.0000 | 1416.9483 | 14169.4832 | -10.0000 | 0.0000 | 0.0000 |

## 4. Mask 口径

| mask_name | target_cells_mean | background_cells_mean | target_count | non_overlap_target_count |
|---|---|---|---|---|
| narrow | 32.6140 | 73.7380 | 6168.0000 | 2125.0000 |
| default | 45.6787 | 65.3673 | 6168.0000 | 1406.0000 |

## 5. Protocol A：clean-threshold degradation test

默认 mask、clean_peak_percentile、PFA=1e-2：

| input_type | sir_name | measured_pfa | false_alarm_count | background_cell_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 |
|---|---|---|---|---|---|---|---|---|---|
| clean |  | 0.0106 | 419.0000 | 39585.0000 | 0.4266 | 0.9377 | 1.0000 | 0.7968 | 0.1489 |
| interfered | light | 0.0148 | 587.0000 | 39585.0000 | 0.4266 | 0.9367 | 1.0000 | 0.7964 | 0.1475 |
| interfered | medium | 0.0225 | 892.0000 | 39585.0000 | 0.4145 | 0.9275 | 0.9822 | 0.7839 | 0.1416 |
| interfered | severe | 0.0207 | 821.0000 | 39585.0000 | 0.3580 | 0.8897 | 0.9481 | 0.7413 | 0.1270 |

Protocol A 的目的不是公平 fixed-PFA 比较，而是观察 clean threshold 固定后干扰是否造成虚警上升和检测退化。

## 6. Protocol B：fixed-PFA recalibrated test

默认 mask、clean_peak_percentile、PFA=1e-2：

| input_type | sir_name | threshold | measured_pfa | false_alarm_count | background_cell_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 | bootstrap_pfa_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clean |  | 3.7472 | 0.0106 | 419.0000 | 39585.0000 | 0.4266 | 0.9377 | 1.0000 | 0.7968 | 0.1489 | 0.0005 |
| interfered | light | 4.1988 | 0.0108 | 428.0000 | 39585.0000 | 0.3795 | 0.8795 | 1.0000 | 0.7584 | 0.1354 | 0.0005 |
| interfered | medium | 7.0158 | 0.0103 | 408.0000 | 39585.0000 | 0.1629 | 0.5965 | 0.9630 | 0.5653 | 0.0841 | 0.0003 |
| interfered | severe | 25.2618 | 0.0096 | 379.0000 | 39585.0000 | 0.0000 | 0.1982 | 0.5956 | 0.2486 | 0.0233 | 0.0003 |

## 7. Noise Floor 与 Target Peak 污染

| mask_name | sir_name | noise_floor_change_db | background_energy_increase_db | clean_noise_floor_db_median | interfered_noise_floor_db_median |
|---|---|---|---|---|---|
| default | light | 0.0641 | 0.5307 | 45.0462 | 45.1103 |
| default | medium | 0.5052 | 3.4690 | 45.0462 | 45.5514 |
| default | severe | 2.5895 | 11.2032 | 45.0462 | 47.6356 |

| mask_name | sir_name | target_count | target_peak_bias_db_mean | target_peak_bias_db_std | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|
| default | light | 2397.0000 | 0.0010 | 0.0047 | 0.0020 |
| default | medium | 2397.0000 | 0.0120 | 0.0583 | 0.0134 |
| default | severe | 2397.0000 | 0.1127 | 0.2606 | 0.1152 |

## 8. All Targets vs Non-Overlap-Only

默认 mask、clean_peak_percentile、PFA=1e-2：

| input_type | sir_name | target_scope | weak_n | weak_pd | mid_n | mid_pd | strong_n | strong_pd | overall_n | overall_pd |
|---|---|---|---|---|---|---|---|---|---|---|
| clean |  | all | 743.0000 | 0.4266 | 979.0000 | 0.9377 | 675.0000 | 1.0000 | 2397.0000 | 0.7968 |
| clean |  | non_overlap_only | 389.0000 | 0.5141 | 139.0000 | 0.9424 | 39.0000 | 1.0000 | 567.0000 | 0.6526 |
| interfered | severe | all | 743.0000 | 0.0000 | 979.0000 | 0.1982 | 675.0000 | 0.5956 | 2397.0000 | 0.2486 |
| interfered | severe | non_overlap_only | 389.0000 | 0.0000 | 139.0000 | 0.1511 | 39.0000 | 0.1026 | 567.0000 | 0.0441 |

## 9. 异常检查

- per-sequence 指标已保存到 `d1b_metrics_by_sequence.csv`。D1A+ 已提示 per-sequence PFA 可能分化，因此 D2 前仍需持续观察。
- per-class-group 指标已保存到 `d1b_metrics_by_class_group.csv`。如果某类为空或目标数很少，不能单独解读成类别结论。
- narrow/default mask 均已输出；如果后续 D2 中二者趋势相反，应先回到 mask 设计，而不是训练模型。

## 10. 输出文件

结果目录：

`G:\mineru_output\results\d1b_gao77_synthetic_interference_sanity`

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\d1b_figures`

关键文件：

- `d1b_interference_config.json`
- `d1b_interference_params_per_frame.csv`
- `d1b_achieved_sir_summary.csv`
- `d1b_protocol_a_clean_threshold_metrics.csv`
- `d1b_protocol_b_fixed_pfa_recalibrated_metrics.csv`
- `d1b_metrics_by_mask.csv`
- `d1b_metrics_non_overlap_only.csv`
- `d1b_noise_floor_summary.csv`
- `d1b_target_peak_bias_summary.csv`
- `d1b_metrics_by_sequence.csv`
- `d1b_metrics_by_class_group.csv`

## 11. D2 建议

可以进入 D2 simple FCN / AENN 小 batch overfit，但 D2 必须继续保留 narrow/default 与 non-overlap-only 辅助统计。
