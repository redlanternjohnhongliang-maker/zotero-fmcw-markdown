# D5-diagnosis：weak-target weighting 不稳定原因诊断

生成时间：2026-06-27 13:58:55  
阶段：D5-diagnosis。没有进入 D6，没有加入 false alarm penalty、clean identity full method 或 proposed full loss，没有引入 RDLR-Net / DiffRIM / RIMformer。

## 1. 总体结论

| 问题 | 结论 |
|---|---|
| 是否主要因为训练数据量不足 | 有一定迹象 |
| 增大 train size 后 gain 是否扩大 | best gain = 0.0229，best hit delta = 6 |
| 模型容量增大后 gain 是否扩大 | best capacity = current_simple_fcn_h128，gain = 0.0115 |
| clean_peak_percentile weak target 定义是否可靠 | overlap-mask ratio = 0.496；需谨慎 |
| CFAR-margin 是否仍不适合作为主定义 | 是；它与 clean_peak weak set 的 Jaccard = 0.545，且 D5 已显示 CFAR-margin 口径弱 Pd 很低 |
| weak targets 是否被 range-only overlap 污染 | 是，污染偏明显 |
| weak weighting 当前是否应视为负结果 | 是，当前 range-only 设置下更接近负结果 |
| 是否还建议进入 D6 | 否 |
| 下一步 | 不进入 D6；优先修 weak target 定义、升级 RD/RA 表示，或把当前 range-only weak weighting 记录为负结果。 |

## 2. Train Size 检查（主口径）

主口径：medium / default mask / all targets / PFA=1e-2。注意：D1A split 中非泄漏训练独立帧只有 300 帧；1000/1500 effective samples 使用重复训练帧生成新的 synthetic interference，因此检查的是训练样本/合成干扰样本量，不是新增真实 clean frame 多样性。

| actual_train_samples | train_unique_frames | train_uses_repeated_frames | balanced_weak_pd | weak_weighted_weak_pd | weak_pd_delta | weak_hit_delta | balanced_mid_pd | weak_weighted_mid_pd | balanced_strong_pd | weak_weighted_strong_pd | weak_weighted_measured_pfa | false_alarm_count_delta | weak_weighted_model_clean_mse_db_to_clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 600.0000 | 300.0000 | 1.0000 | 0.3740 | 0.3588 | -0.0153 | -4.0000 | 0.9756 | 0.9756 | 1.0000 | 1.0000 | 0.0108 | 3.0000 | 0.0715 |
| 1000.0000 | 300.0000 | 1.0000 | 0.4008 | 0.4008 | 0.0000 | 0.0000 | 0.9756 | 0.9756 | 1.0000 | 1.0000 | 0.0107 | -1.0000 | 0.0553 |
| 1500.0000 | 300.0000 | 1.0000 | 0.3702 | 0.3931 | 0.0229 | 6.0000 | 0.9756 | 0.9756 | 1.0000 | 1.0000 | 0.0105 | -3.0000 | 0.0320 |

## 3. 容量检查（主口径）

| capacity | actual_train_samples | balanced_weak_pd | weak_weighted_weak_pd | weak_pd_delta | weak_hit_delta | balanced_mid_pd | weak_weighted_mid_pd | balanced_strong_pd | weak_weighted_strong_pd | weak_weighted_measured_pfa | false_alarm_count_delta | weak_weighted_model_clean_mse_db_to_clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| current_simple_fcn_h128 | 600.0000 | 0.3779 | 0.3893 | 0.0115 | 3.0000 | 0.9756 | 0.9756 | 1.0000 | 1.0000 | 0.0104 | -3.0000 | 0.0679 |
| shallow_unet1d_c16 | 600.0000 | 0.3626 | 0.3550 | -0.0076 | -2.0000 | 0.9756 | 0.9756 | 1.0000 | 1.0000 | 0.0104 | -1.0000 | 0.0722 |
| wider_fcn_h256 | 600.0000 | 0.3969 | 0.3969 | 0.0000 | 0.0000 | 0.9756 | 0.9756 | 1.0000 | 1.0000 | 0.0105 | -2.0000 | 0.0376 |

## 4. Weak Target 定义诊断

| definition | weak_n | mid_n | strong_n | weak_overlap_with_other_definition_n | weak_overlap_jaccard | weak_non_overlap_n | weak_overlap_mask_n | weak_overlap_mask_ratio | weak_target_peak_db_mean | weak_cfar_margin_db_mean |
|---|---|---|---|---|---|---|---|---|---|---|
| clean_peak_percentile | 1851.0000 | 2466.0000 | 1851.0000 | 1306.0000 | 0.5448 | 932.0000 | 919.0000 | 0.4965 | 52.6466 | 5.1309 |
| cfar_margin | 1852.0000 | 2465.0000 | 1851.0000 | 1306.0000 | 0.5448 | 611.0000 | 1241.0000 | 0.6701 | 53.5468 | 4.1947 |

## 5. 判断

- 如果 train size 或容量增加后 gain 没有达到 0.02-0.03，不能说 weak weighting 有稳定贡献。
- 如果 non-overlap-only 或 PFA=1e-3 不同步支持，不能进入 D6。
- 当前更合理的方向是先修 weak target 定义，或者升级到 RD/RA 表示来减少 range-only overlap 污染。
- 如果后续仍要推进，D6 必须建立在通过 robust 口径的配置上，而不是沿用 D5 原始的 1 个 target 差异。

## 6. 输出文件

结果目录：`G:\mineru_output\results\d5_diagnosis_weak_weighting_failure`  
图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d5_diagnosis_figures`
