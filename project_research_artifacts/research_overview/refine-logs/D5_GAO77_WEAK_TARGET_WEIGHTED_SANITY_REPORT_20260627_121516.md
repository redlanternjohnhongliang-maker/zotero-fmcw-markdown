# D5 Gao77 Weak-Target-Weighted Sanity 报告

生成时间：2026-06-27 12:15:16  
阶段：D5，仅 weak-target-weighted detection loss sanity  
数据：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次只执行 D5。没有进入 D6-D14，没有做 false alarm penalty、clean identity full method、proposed full loss 或 3 seeds；没有引入 RDLR-Net / DiffRIM / RIMformer，也没有使用大模型。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D5 是否通过 | 通过 |
| 哪个 weak target 定义更稳定 | clean_peak_percentile |
| 哪个 weak weight 最好 | 2.0 |
| weak-target-weighted 是否超过 balanced_mild | 是 |
| 是否只超过 MSE 但没超过 balanced_mild | 否 |
| weak Pd 提升是否伴随 mid/strong Pd 下降 | 否 |
| weak Pd 提升是否伴随 false alarm 或 target peak bias 异常 | 否 |
| clean no-harm 是否正常 | 是 |
| narrow/default mask 是否一致 | 是 |
| all targets / non-overlap-only 是否一致 | 是 |
| per-sequence 是否异常 | 未发现明显 PFA 异常；详见 CSV |
| per-class-group 是否异常 | motorbike_like 样本为 0，其他类别需看 CSV；未作为单独结论 |
| 是否建议进入 D6 | 是 |
| 如果不能进入 D6，最应该修什么 |  |

## 3. 主对照与 Best D5

| baseline | group | split_definition_train | weak_weight | weak_pd | mid_pd | strong_pd | overall_pd | f1 | measured_pfa | false_alarm_count | output_mse_db_to_clean | model_clean_mse_db_to_clean | target_peak_abs_bias_db_mean | is_best_d5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mse | anchor | clean_peak_percentile |  | 0.3702 | 0.9756 | 1.0000 | 0.5685 | 0.1350 | 0.0104 | 148.0000 | 0.1681 | 0.0484 | 0.1008 | 0.0000 |
| bce_rec_anchor | anchor | clean_peak_percentile |  | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1364 | 0.0105 | 149.0000 | 0.1728 | 0.0490 | 0.1294 | 0.0000 |
| balanced_mild | D4 strong | clean_peak_percentile |  | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1369 | 0.0106 | 150.0000 | 0.1671 | 0.0450 | 0.1203 | 0.0000 |
| focal_g1_a0p25 | D4 focal | clean_peak_percentile |  | 0.3817 | 0.9756 | 1.0000 | 0.5762 | 0.1366 | 0.0102 | 145.0000 | 0.1718 | 0.0564 | 0.0950 | 0.0000 |
| weak_peak_w2p0 | D5 weak | clean_peak_percentile | 2.0000 | 0.3855 | 0.9756 | 1.0000 | 0.5788 | 0.1388 | 0.0105 | 149.0000 | 0.1880 | 0.0453 | 0.1144 | 1.0000 |

## 4. Weak Definition 对比

| split_definition_train | best_baseline | best_weak_weight | best_weak_pd | best_mid_pd | best_strong_pd | best_clean_mse | best_target_peak_abs_bias |
|---|---|---|---|---|---|---|---|
| cfar_margin | weak_cfar_w5p0 | 5.0000 | 0.1777 | 1.0000 | 1.0000 | 0.0446 | 0.1487 |
| clean_peak_percentile | weak_peak_w2p0 | 2.0000 | 0.3855 | 0.9756 | 1.0000 | 0.0453 | 0.1144 |

## 5. Weight Sweep

| baseline | split_definition_train | weak_weight | weak_pd | mid_pd | strong_pd | f1 | measured_pfa | false_alarm_count | model_clean_mse_db_to_clean | target_peak_abs_bias_db_mean | narrow_weak_pd | non_overlap_weak_pd | valid_d5_candidate | beats_balanced_mild_weak_pd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| weak_peak_w2p0 | clean_peak_percentile | 2.0000 | 0.3855 | 0.9756 | 1.0000 | 0.1388 | 0.0105 | 149.0000 | 0.0453 | 0.1144 | 0.2716 | 0.3810 | 1.0000 | 1.0000 |
| weak_peak_w3p0 | clean_peak_percentile | 3.0000 | 0.3817 | 0.9756 | 1.0000 | 0.1384 | 0.0103 | 146.0000 | 0.0589 | 0.1150 | 0.2716 | 0.3757 | 1.0000 | 0.0000 |
| weak_peak_w5p0 | clean_peak_percentile | 5.0000 | 0.3817 | 0.9756 | 1.0000 | 0.1372 | 0.0100 | 141.0000 | 0.0682 | 0.1495 | 0.2798 | 0.3704 | 1.0000 | 0.0000 |
| weak_cfar_w2p0 | cfar_margin | 2.0000 | 0.1726 | 1.0000 | 1.0000 | 0.1378 | 0.0107 | 151.0000 | 0.0466 | 0.1280 | 0.0000 | 0.1690 | 1.0000 | 0.0000 |
| weak_cfar_w3p0 | cfar_margin | 3.0000 | 0.1726 | 1.0000 | 1.0000 | 0.1390 | 0.0100 | 142.0000 | 0.0491 | 0.1945 | 0.0000 | 0.1761 | 1.0000 | 0.0000 |
| weak_cfar_w5p0 | cfar_margin | 5.0000 | 0.1777 | 1.0000 | 1.0000 | 0.1371 | 0.0102 | 144.0000 | 0.0446 | 0.1487 | 0.0000 | 0.1831 | 1.0000 | 0.0000 |

## 6. 训练状态

| baseline | split_definition_train | weak_weight | status | train_loss_drop_fraction | val_loss_drop_fraction | final_val_detection | final_val_magmse | stopped_reason |
|---|---|---|---|---|---|---|---|---|
| weak_peak_w2p0 | clean_peak_percentile | 2.0000 | DONE | 0.2033 | 0.2305 | 0.9740 | 0.1295 |  |
| weak_peak_w3p0 | clean_peak_percentile | 3.0000 | DONE | 0.1655 | 0.1695 | 1.2104 | 0.1308 |  |
| weak_peak_w5p0 | clean_peak_percentile | 5.0000 | DONE | 0.1720 | 0.1590 | 1.5493 | 0.1498 |  |
| weak_cfar_w2p0 | cfar_margin | 2.0000 | DONE | 0.1988 | 0.2337 | 0.8970 | 0.1214 |  |
| weak_cfar_w3p0 | cfar_margin | 3.0000 | DONE | 0.1976 | 0.2092 | 1.0860 | 0.1197 |  |
| weak_cfar_w5p0 | cfar_margin | 5.0000 | DONE | 0.1848 | 0.1703 | 1.3821 | 0.1309 |  |

## 7. 判断

- D5 只是 weak-target-weighted loss sanity，不是最终方法效果。
- D5 的主对照是 D4 best strong baseline `balanced_mild`，不是 MSE 或 BCE+rec anchor。
- 如果 D5 通过，D6 才能测试 false alarm penalty；否则应先修 weak definition、weight scale 或 loss formulation。

## 8. 输出文件

结果目录：`G:\mineru_output\results\d5_gao77_weak_target_weighted_sanity`  
图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d5_figures`

## 9. D6 建议

可以进入 D6 false alarm penalty；D6 必须验证 weak Pd 提升不是靠 false alarm 或 target peak inflation 换来的。
