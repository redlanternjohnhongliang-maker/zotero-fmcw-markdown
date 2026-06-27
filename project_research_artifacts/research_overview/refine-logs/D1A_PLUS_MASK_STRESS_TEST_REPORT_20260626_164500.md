# D1A+ Gao77 Mask Stress Test 与 Fixed-PFA 稳定性报告

生成时间：2026-06-26 16:45  
阶段：D1A+，仅 clean range-only / mask stress / fixed-PFA stability  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次没有进入 D1B，没有做 synthetic interference injection，没有训练模型，没有进入 D2-D14，没有下载新数据集，也没有引入任何 backbone。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D1A+ 是否通过 | 通过 |
| target mask 是否过宽 | 默认 mask 偏宽，建议 D1B 先用 narrow/default 双口径报告 |
| D1A 结果是否对 target mask 宽度敏感 | 是，weak Pd/F1 对宽度较敏感 |
| target mask overlap 是否严重 | 较严重 |
| weak/mid/strong split 是否受 overlap 影响 | 影响可控 |
| fixed-PFA 是否对 guard ring 敏感 | 不高度敏感 |
| PFA 统计是否稳定 | 稳定 |
| RA projection 是否比 range-only 更可信 | 当前 RA 未明显优于 range-only |
| 是否可进入 D1B | 可以进入，但 D1B 先做 range-only sanity，并保留 narrow/default mask 对照 |
| D1B 建议 | range-only D1B 优先；RA 仅作辅助可视化 |

## 3. Target Mask 宽度敏感性

target PFA = 1e-2 下的主要结果：

| mask_name | target_cells_mean | guard_cells_mean | background_cells_mean | projection_hit_rate | target_background_energy_ratio_db | weak_pd | mid_pd | strong_pd | overall_pd | test_measured_pfa | f1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| narrow | 32.6140 | 16.6613 | 73.7380 | 0.9763 | 10.3710 | 0.2614 | 0.7558 | 1.0000 | 0.6675 | 0.0103 | 0.2022 |
| default | 45.6787 | 12.0213 | 65.3673 | 0.9878 | 12.1956 | 0.4266 | 0.9377 | 1.0000 | 0.7968 | 0.0106 | 0.1489 |
| wide | 55.6453 | 10.5140 | 57.4020 | 0.9895 | 12.3317 | 0.4851 | 0.9656 | 1.0000 | 0.8269 | 0.0108 | 0.1268 |

完整结果：`G:\mineru_output\results\d1a_plus_mask_stress_test\mask_width_sensitivity.csv`

判断：默认 mask 平均 target cells 为 45.68，比 narrow 的 32.61 大不少。projection hit rate 在三种设置下都很高，但 weak Pd 和 F1 会随 mask 宽度变化，因此 D1B 不应只报告单一 mask 口径。

## 4. Mask Overlap 检查

| 指标 | 数值 |
|---|---:|
| overlap pair ratio | 0.3926 |
| overlap cell ratio | 0.3708 |
| overlapped target ratio | 0.7720 |
| weak overlap target ratio | 0.4965 |
| mid overlap target ratio | 0.8532 |
| strong overlap target ratio | 0.9395 |

判断：overlap 不是可以忽略的小问题。D1B 中 weak/mid/strong split 最好增加一个 `non-overlap only` 辅助统计，避免 weak/strong 结论被多目标重叠污染。

## 5. Guard Ring 敏感性

target PFA = 1e-2：

| guard_extra_bins | background_cells_mean | validation_threshold | test_measured_pfa | weak_pd | mid_pd | strong_pd | false_alarm_count | background_cell_count |
|---|---|---|---|---|---|---|---|---|
| 2.0000 | 70.7893 | 3.6922 | 0.0106 | 0.4307 | 0.9408 | 1.0000 | 452.0000 | 42787.0000 |
| 4.0000 | 65.3673 | 3.7472 | 0.0106 | 0.4266 | 0.9377 | 1.0000 | 419.0000 | 39585.0000 |
| 6.0000 | 60.3593 | 3.7812 | 0.0107 | 0.4172 | 0.9377 | 1.0000 | 391.0000 | 36607.0000 |

完整结果：`G:\mineru_output\results\d1a_plus_mask_stress_test\guard_sensitivity.csv`

判断：guard 改变会影响背景 cell 数和阈值，但 test PFA 仍接近目标 PFA；因此 fixed-PFA calibration 不算对 guard ring 高度敏感。

## 6. PFA 统计稳定性

| target_pfa | background_cell_count | false_alarm_count | measured_pfa | frame_level_pfa_std | bootstrap_pfa_std | bootstrap_pfa_ci_low | bootstrap_pfa_ci_high |
|---|---|---|---|---|---|---|---|
| 0.0100 | 39585.0000 | 419.0000 | 0.0106 | 0.0129 | 0.0005 | 0.0095 | 0.0116 |
| 0.0010 | 39585.0000 | 46.0000 | 0.0012 | 0.0039 | 0.0002 | 0.0008 | 0.0015 |

per-source-sequence PFA：`G:\mineru_output\results\d1a_plus_mask_stress_test\pfa_by_sequence.csv`  
per-class-group Pd：`G:\mineru_output\results\d1a_plus_mask_stress_test\pd_by_class_group.csv`

判断：整体 PFA 稳定；per-sequence 仍需在 D1B 中继续观察，因为干扰注入后不同 sequence 的背景统计可能分化。

## 7. RA Projection 补充检查

| 指标 | 数值 |
|---|---:|
| RA projection hit rate | 0.8763 |
| RA target/background ratio mean dB | 13.9188 |

判断：RA map 可以生成，RA projection sanity 可用，但当前没有明显比 range-only 更可信。D1B 优先做 range-only interference sanity，RA 作为辅助可视化和后续扩展。

## 8. 输出文件

结果目录：

`G:\mineru_output\results\d1a_plus_mask_stress_test`

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\d1a_plus_figures`

关键文件：

- `mask_width_sensitivity.csv`
- `guard_sensitivity.csv`
- `mask_overlap_summary.csv`
- `pfa_stability_summary.csv`
- `pfa_by_sequence.csv`
- `pd_by_class_group.csv`
- `ra_projection_sanity.csv`
- `d1a_plus_config.json`

## 9. 下一步建议

可以进入 D1B synthetic interference sanity，但建议只先做 range-only D1B，并且保留以下防护：

1. 同时报告 narrow/default mask 两套指标；
2. 输出 non-overlap-only 的 weak/mid/strong 辅助统计；
3. 固定 PFA 阈值必须继续报告 background cell count、false alarm count、bootstrap/frame-level std；
4. RA 只作为辅助 sanity，不要作为第一版 D1B 主指标。
