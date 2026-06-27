# 给 GPT 的单文件交接稿：D5E RD proxy and ceiling-effect diagnosis

你只需要把这个文件发给 GPT。它包含本轮 D5E 诊断的目标、约束、关键数据、文件路径和保守结论。

## 1. 本轮任务

D5E 用来解释 D5D 为什么出现 `balanced_mild weak Pd = 1.0`，导致 weak weighting 没有提升空间。D5E 是诊断，不是正式方法；不能进入 D6，不能加入 false alarm penalty，不能把 RD proxy 写成 confirmed RD performance。

## 2. 关键路径

- D5E 脚本：`G:\mineru_output\experiments\d5e_rd_proxy_ceiling_diagnosis.py`
- D5E 结果目录：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis`
- D5E 图像目录：`G:\mineru_output\gao_77ghz_raw_adc\reports\d5e_rd_proxy_ceiling_figures`
- 总结：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis\d5e_rd_proxy_ceiling_summary.md`
- 决策：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis\d5e_rd_proxy_ceiling_decision.md`
- 配置：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis\d5e_config.json`
- analyze-results：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis\D5E_ANALYZE_RESULTS.md`
- experiment-audit：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis\EXPERIMENT_AUDIT.md`
- result-to-claim：`G:\mineru_output\results\d5e_rd_proxy_ceiling_diagnosis\RESULT_TO_CLAIM.md`

## 3. 核心结果

- ceiling effect 是否成立：`True`
- q30 weak threshold 是否太容易：`True`
- stricter PFA 是否给 weak weighting 优势：`False`
- mask 变形是否给 weak weighting 优势：`False`
- RD proxy label 是否过度乐观：`True`
- weak_n 是否太小不适合强 claim：`True`
- 是否允许 D6：`False`
- 是否继续 weak weighting：`False`
- `/analyze-results` verdict：`NO-GO`
- `/experiment-audit` verdict：`WARN`，integrity_status=`warn`，evaluation_type=`mixed_proxy`
- `/result-to-claim` verdict：claim_supported=`partial`，integrity_status=`warn`，confidence=`medium`，final_route=`NEVER_ENTER_D6_IMMEDIATELY`

## 3.1 GPT 需要注意的边界

- D5E 只支持“有限 RD-proxy ceiling diagnosis”，不是 confirmed RD performance。
- D5E 支持：D5D 默认 RD proxy 在 PFA=1e-2 下已经饱和，balanced_mild 对 q30 weak targets 是 62/62 hits。
- D5E 不支持：继续 weak weighting、进入 D6、加入 false alarm penalty、写 full method。
- D5E 也不证明 ceiling effect 是 weak weighting 失败的唯一原因；因为在 PFA=1e-3 这种部分解除 ceiling 的情况下，weak weighting 仍然均值更差。
- 如果继续，必须先修 RD proxy / task difficulty / label validity，而不是继续堆 loss。

## 4. 关键表格摘要

### Ceiling effect

| seed | weak_n | balanced_mild_weak_hits | weak_weighting_weak_hits | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | balanced_mild_weak_miss_count | ceiling_effect_present |
|---|---|---|---|---|---|---|---|---|---|
| 42.0000 | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | True |
| 200.0000 | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | True |
| mean | 62.0000 | 62.0000 | 62.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |  |

### PFA sensitivity mean rows

| target_pfa | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta | measured_pfa_delta | false_alarm_count_delta |
|---|---|---|---|---|---|---|
| 0.0100 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -0.0000 | -42.5000 |
| 0.0050 | 0.9839 | 0.9839 | 0.0000 | 0.0000 | -0.0000 | -12.5000 |
| 0.0010 | 0.6048 | 0.5887 | -0.0161 | -1.0000 | 0.0000 | 6.5000 |
| 0.0005 | 0.3226 | 0.3145 | -0.0081 | -0.5000 | -0.0000 | -6.5000 |
| 0.0001 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | -0.0000 | -5.0000 |

### Mask sensitivity mean rows

| range_mask_name | doppler_radius_bins | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|
| narrow | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| narrow | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| narrow | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| narrow | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| default | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| default | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| default | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| default | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| wide | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| wide | 2.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| wide | 3.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| wide | 5.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

### Weak threshold difficulty mean rows

| q_weak | train_weak_threshold_db | train_weak_n | test_weak_n | mean_target_background_contrast_db | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|---|---|---|
| 0.1000 | 48.0669 | 21.0000 | 18.0000 | 31.2936 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.2000 | 49.2190 | 40.0000 | 37.0000 | 31.8631 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.3000 | 50.5937 | 56.0000 | 62.0000 | 32.4174 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| 0.4000 | 51.8927 | 77.0000 | 76.0000 | 32.7413 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

### RD proxy label dependence mean rows

| doppler_box_mode | weak_projection_hit_rate_against_clean_peak | overlap_ratio_vs_clean_peak_box | balanced_mild_weak_pd | weak_weighting_weak_pd | weak_pd_delta | weak_hit_delta |
|---|---|---|---|---|---|---|
| clean_peak | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| interfered_peak | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| local_window_peak | 0.9194 | 0.9194 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| nearest_high_energy | 0.9194 | 0.9194 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| vertical_stripe | 1.0000 | 0.0196 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| multi_bin_uncertainty | 1.0000 | 0.4545 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |

## 5. 保守结论，可写进项目报告

In the D5E diagnostic, the current RD-only proxy task shows a clear ceiling effect: under the D5D default clean-RD Doppler-peak projection and PFA=1e-2, `balanced_mild` already detects all weak targets, leaving no measurable room for weak weighting. Stricter PFA thresholds, mask-width perturbations, and harder train-only weak-target quantiles do not reveal a robust weak-weighting advantage. Because RD boxes are still proxy-derived from range labels and Doppler projections rather than true Doppler/velocity ground truth, D5E should be reported only as a limited RD-proxy diagnosis. The correct route remains NO-GO: do not enter D6 and do not claim confirmed RD performance.

## 6. 下一步建议

不要进入 D6。不要继续 weak weighting 当前路线。若还要做 RD 方向，下一步应先设计非饱和、可验证的 RD target protocol：更硬的 weak target 定义、避免过宽或 clean-peak 乐观 proxy、最好引入真实 Doppler/velocity GT 或强约束的替代标注协议，并增加 weak_n / seeds 后再重新比较 `balanced_mild` 与 weak weighting。
