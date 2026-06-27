# D4 Gao77 Strong Baseline Sanity 报告

生成时间：2026-06-26 23:15:30  
阶段：D4，仅 tuned balanced BCE / focal loss 强 baseline sanity  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次只执行 D4。没有进入 D5-D14，没有做 weak-target-weighted loss、false alarm penalty、clean identity full method、proposed full loss 或 3 seeds；没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D4 是否通过 | 通过 |
| balanced BCE+rec 是否训练成功 | 是 |
| focal+rec 是否训练成功 | 是 |
| 最强 balanced/focal 配置 | balanced_mild |
| best balanced/focal 是否超过 MSE/MAGMSE | 是 |
| best balanced/focal 是否超过 BCE+rec | 是 |
| false alarm / measured PFA 是否正常 | 是 |
| clean no-harm 是否正常 | 是 |
| narrow/default mask 是否一致 | 是，未发现完全相反趋势 |
| all targets / non-overlap-only 是否一致 | 是，未发现推翻 overall 的趋势 |
| per-sequence 是否异常 | 未发现明显 PFA 异常 |
| per-class-group 是否异常 | motorbike_like 样本为 0，其他类别未见推翻结论的异常 |
| 是否建议进入 D5 | 是 |
| 下一步 | 可以进入 D5 weak-target-weighted loss；D5 必须把 best D4 strong baseline 作为主对照。 |

## 3. Baseline 对比

default mask、medium、PFA=1e-2：

| name | mse_db_to_clean | measured_pfa | false_alarm_count | background_cell_count | weak_pd | mid_pd | strong_pd | overall_pd | f1 | target_peak_abs_bias_db_mean |
|---|---|---|---|---|---|---|---|---|---|---|
| MSE output medium | 0.1681 | 0.0104 | 148.0000 | 14165.0000 | 0.3702 | 0.9756 | 1.0000 | 0.5685 | 0.1350 | 0.1008 |
| BCE+rec anchor output medium | 0.1728 | 0.0105 | 149.0000 | 14165.0000 | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1364 | 0.1294 |
| balanced_mild output medium | 0.1671 | 0.0106 | 150.0000 | 14165.0000 | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1369 | 0.1203 |
| balanced_full output medium | 0.1918 | 0.0104 | 148.0000 | 14165.0000 | 0.3626 | 0.9756 | 1.0000 | 0.5633 | 0.1350 | 0.1276 |
| focal_g1_a0p25 output medium | 0.1718 | 0.0102 | 145.0000 | 14165.0000 | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1366 | 0.0950 |
| focal_g1_a0p5 output medium | 0.1848 | 0.0103 | 146.0000 | 14165.0000 | 0.3702 | 0.9756 | 1.0000 | 0.5685 | 0.1332 | 0.0872 |
| focal_g2_a0p25 output medium | 0.1715 | 0.0101 | 143.0000 | 14165.0000 | 0.3588 | 0.9756 | 1.0000 | 0.5607 | 0.1338 | 0.0816 |
| focal_g2_a0p5 output medium | 0.1876 | 0.0102 | 144.0000 | 14165.0000 | 0.3588 | 0.9756 | 1.0000 | 0.5607 | 0.1314 | 0.1100 |

## 4. Best Strong Baseline 选择

| baseline | family | weak_pd | mid_pd | strong_pd | overall_pd | f1 | measured_pfa | output_mse_db_to_clean | model_clean_mse_db_to_clean | target_peak_abs_bias_db_mean | valid_strong_baseline | is_best_strong_baseline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mse | anchor | 0.3702 | 0.9756 | 1.0000 | 0.5685 | 0.1350 | 0.0104 | 0.1681 | 0.0484 | 0.1008 | 0.0000 | 0.0000 |
| bce_rec_anchor | anchor | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1364 | 0.0105 | 0.1728 | 0.0490 | 0.1294 | 0.0000 | 0.0000 |
| balanced_mild | balanced | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1369 | 0.0106 | 0.1671 | 0.0450 | 0.1203 | 1.0000 | 1.0000 |
| balanced_full | balanced | 0.3626 | 0.9756 | 1.0000 | 0.5633 | 0.1350 | 0.0104 | 0.1918 | 0.0818 | 0.1276 | 1.0000 | 0.0000 |
| focal_g1_a0p25 | focal | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1366 | 0.0102 | 0.1718 | 0.0564 | 0.0950 | 1.0000 | 0.0000 |
| focal_g1_a0p5 | focal | 0.3702 | 0.9756 | 1.0000 | 0.5685 | 0.1332 | 0.0103 | 0.1848 | 0.0602 | 0.0872 | 1.0000 | 0.0000 |
| focal_g2_a0p25 | focal | 0.3588 | 0.9756 | 1.0000 | 0.5607 | 0.1338 | 0.0101 | 0.1715 | 0.0381 | 0.0816 | 1.0000 | 0.0000 |
| focal_g2_a0p5 | focal | 0.3588 | 0.9756 | 1.0000 | 0.5607 | 0.1314 | 0.0102 | 0.1876 | 0.0463 | 0.1100 | 1.0000 | 0.0000 |

## 5. 训练状态

| baseline | family | status | train_loss_drop_fraction | val_loss_drop_fraction | final_val_det | final_val_magmse | pos_weight | alpha | gamma | stopped_reason |
|---|---|---|---|---|---|---|---|---|---|---|
| balanced_mild | balanced | DONE | 0.2517 | 0.3090 | 0.7551 | 0.1229 | 1.1852 |  |  |  |
| balanced_full | balanced | DONE | 0.2307 | 0.2832 | 0.8504 | 0.1424 | 1.4047 |  |  |  |
| focal_g1_a0p25 | focal | DONE | 0.5752 | 0.6081 | 0.1565 | 0.1243 |  | 0.2500 | 1.0000 |  |
| focal_g1_a0p5 | focal | DONE | 0.3664 | 0.4397 | 0.3042 | 0.1350 |  | 0.5000 | 1.0000 |  |
| focal_g2_a0p25 | focal | DONE | 0.5484 | 0.6042 | 0.1477 | 0.1257 |  | 0.2500 | 2.0000 |  |
| focal_g2_a0p5 | focal | DONE | 0.3846 | 0.4497 | 0.2903 | 0.1293 |  | 0.5000 | 2.0000 |  |

## 6. 判断

- D4 只是强 baseline sanity，不是 proposed method。
- 如果 best balanced/focal 已经接近或超过 BCE+rec，则 D5 必须证明 weak-target weighting 不是普通 class imbalance / hard-example baseline 能解释的。
- severe interference 仅作为 stress test，不作为 D4 主要通过标准。

## 7. 输出文件

结果目录：`G:\mineru_output\results\d4_gao77_strong_baseline_sanity`  
图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d4_figures`

## 8. D5 建议

可以进入 D5 weak-target-weighted loss；D5 必须把 best D4 strong baseline 作为主对照。
