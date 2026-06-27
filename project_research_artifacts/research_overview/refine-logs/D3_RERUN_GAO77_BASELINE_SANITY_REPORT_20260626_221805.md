# D3-Rerun Gao77 Baseline Sanity 报告

生成时间：2026-06-26 22:18:05  
阶段：D3-Rerun，仅修正后的 range-only baseline sanity  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次不是 D4。没有做 focal loss、balanced BCE、weak-target full loss、false alarm penalty、clean identity full method、3 seeds，也没有引入 RDLR-Net / DiffRIM / RIMformer。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D3-Rerun 是否通过 | 通过 |
| MSE/MAGMSE baseline 是否正常 | 是 |
| pure BCE failure control 是否复现 detection-shaping | 是 |
| BCE+rec 是否缓解幅度破坏 | 是 |
| 最稳 lambda_rec | 0.5 |
| BCE+rec 相比 MSE 的 fixed-PFA weak Pd | best=0.3817, MSE=0.3702 |
| BCE+rec 相比 pure BCE 的 clean no-harm | best model(clean) MSE=0.0490, pure BCE=53.1977 |
| BCE+rec 是否仍有 detection-shaping 副作用 | 轻微/可控 |
| clean-input no-harm 是否通过 | 是 |
| narrow/default mask 是否一致 | 是 |
| all targets / non-overlap-only 是否一致 | 是 |
| 是否建议进入 D4 | 是 |
| 下一步 | 可以进入 D4，但 D4 仍只应做 tuned balanced BCE / focal loss 强 baseline，不能直接进入 weak-target full loss。 |

## 3. Baseline 对比

default mask、clean_peak_percentile、PFA=1e-2：

| name | mse_db_to_clean | measured_pfa | false_alarm_count | background_cell_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.0000 | 0.0105 | 149.0000 | 14165.0000 | 0.3511 | 0.9756 | 1.0000 | 0.5556 | 0.1298 | 0.0000 |
| interfered medium | 6.3122 | 0.0102 | 145.0000 | 14165.0000 | 0.2290 | 0.9146 | 1.0000 | 0.4599 | 0.0958 | 0.0192 |
| MSE output medium | 0.1681 | 0.0104 | 148.0000 | 14165.0000 | 0.3702 | 0.9756 | 1.0000 | 0.5685 | 0.1350 | 0.1008 |
| pure BCE output medium | 63.1141 | 0.0115 | 163.0000 | 14165.0000 | 0.6489 | 0.8415 | 0.9535 | 0.7235 | 0.3029 | 4.4916 |
| MSE model(clean) | 0.0484 | 0.0106 | 150.0000 | 14165.0000 | 0.3550 | 0.9756 | 1.0000 | 0.5581 | 0.1312 | 0.0532 |
| pure BCE model(clean) | 53.1977 | 0.0107 | 152.0000 | 14165.0000 | 0.6412 | 0.8415 | 0.9535 | 0.7183 | 0.2974 | 4.3797 |
| BCE+rec lambda=0.1 output medium | 0.2182 | 0.0099 | 140.0000 | 14165.0000 | 0.4618 | 0.9878 | 1.0000 | 0.6331 | 0.1583 | 0.2754 |
| BCE+rec lambda=0.1 model(clean) | 0.0798 | 0.0104 | 148.0000 | 14165.0000 | 0.4656 | 0.9878 | 1.0000 | 0.6357 | 0.1562 | 0.2034 |
| BCE+rec lambda=0.5 output medium | 0.1728 | 0.0105 | 149.0000 | 14165.0000 | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1364 | 0.1294 |
| BCE+rec lambda=0.5 model(clean) | 0.0490 | 0.0108 | 153.0000 | 14165.0000 | 0.3855 | 0.9756 | 1.0000 | 0.5788 | 0.1372 | 0.0621 |
| BCE+rec lambda=1.0 output medium | 0.1935 | 0.0102 | 145.0000 | 14165.0000 | 0.3588 | 0.9756 | 1.0000 | 0.5607 | 0.1313 | 0.0884 |
| BCE+rec lambda=1.0 model(clean) | 0.0841 | 0.0107 | 152.0000 | 14165.0000 | 0.3626 | 0.9756 | 1.0000 | 0.5633 | 0.1325 | 0.0396 |

## 4. Lambda_rec 对比

| lambda_rec | final_val_loss | final_val_bce | final_val_magmse | output_mse_db_to_clean | model_clean_mse_db_to_clean | weak_pd | f1 | false_alarm_count | target_peak_abs_bias_db_mean | narrow_weak_pd | non_overlap_weak_pd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.1000 | 0.6789 | 0.6623 | 0.1663 | 0.2182 | 0.0798 | 0.4618 | 0.1583 | 140.0000 | 0.2754 | 0.3539 | 0.4709 |
| 0.5000 | 0.7296 | 0.6681 | 0.1231 | 0.1728 | 0.0490 | 0.3817 | 0.1364 | 149.0000 | 0.1294 | 0.2716 | 0.3757 |
| 1.0000 | 0.8177 | 0.6702 | 0.1475 | 0.1935 | 0.0841 | 0.3588 | 0.1313 | 145.0000 | 0.0884 | 0.2428 | 0.3545 |

## 5. 关键判断

- pure BCE 检测指标可能较高，但 clean no-harm 失败，因此只能作为 invalid detection-shaping failure control。
- BCE+rec 是修正后的 ordinary detection-aware baseline，不是 proposed method。
- severe interference 仍只作为 stress test，不作为 D3-Rerun 是否通过的唯一依据。

## 5.5 Per-Sequence / Per-Class 检查

best lambda=`0.5`，default mask、medium、PFA=1e-2：

| source_sequence | test_frame_count | target_count | false_alarm_count | measured_pfa | Pd |
|---|---:|---:|---:|---:|---:|
| 2019_04_30_mlms000 | 120 | 270 | 114 | 0.0105 | 0.6037 |
| 2019_04_30_mlms001 | 40 | 117 | 35 | 0.0105 | 0.5128 |

per-sequence 没有明显 PFA 异常。两个 sequence 的 Pd 有差异，但方向没有推翻 overall 结论。

| class_group | target_count | hit_count | Pd |
|---|---:|---:|---:|
| cyclist_like | 147 | 62 | 0.4218 |
| pedestrian_like | 194 | 122 | 0.6289 |
| vehicle_like | 46 | 39 | 0.8478 |
| motorbike_like | 0 | 0 | NA |

per-class-group 没有发现会推翻结论的异常；`motorbike_like` 在当前 test 子集中没有目标，不能单独解读。

## 6. 输出文件

结果目录：`G:\mineru_output\results\d3_rerun_gao77_baseline_sanity`  
图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d3_rerun_figures`

关键 CSV/JSON 已按要求生成，包括 fixed-PFA、clean no-harm、reconstruction、mask、non-overlap、per-sequence、per-class-group、baseline comparison 和 lambda_rec summary。

## 7. D4 建议

可以进入 D4，但 D4 仍只应做 tuned balanced BCE / focal loss 强 baseline，不能直接进入 weak-target full loss。
