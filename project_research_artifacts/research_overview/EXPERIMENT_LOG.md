# EXPERIMENT_LOG

## D1 Sanity — 2026-06-26 12:12

- **System**：preflight + fixed-PFA D1 sanity，未训练模型。
- **Config**：synthetic toy RD，shape `(48, 64, 128)`，PyTorch `1.12.0+cu113`，GPU `NVIDIA GeForce GTX 1650 4GB`，batch dry-run `2`。
- **Completed runs**：`R001-R003`。
- **Result**：D1 指标链路通过；hard CA-CFAR、differentiable CA-CFAR、target/background mask、weak/mid/strong split、cell-level PFA、fixed-PFA threshold calibration 均已跑通。
- **Caution**：未发现本地真实数值雷达 tensor 数据，本次结果只证明代码链路可运行，不代表真实雷达实验效果。
- **Artifacts**：
  - `refine-logs/HARDWARE_PREFLIGHT_REPORT.md`
  - `refine-logs/D1_FIXED_PFA_SANITY_REPORT.md`
  - `results/d1_sanity/preflight.json`
  - `results/d1_sanity/d1_metrics.json`
  - `results/d1_sanity/d1_metrics.csv`

## D1A Gao77 Clean Sanity — 2026-06-26 16:21

- **System**：Gao77 clean range-only map + objectness target/background mask + hard/differentiable CA-CFAR，未训练模型。
- **Config**：`subset_d1a_v1`，1500 frames，6168 targets，range-only 主链路；RD/RA 仅作 smoke visualization。
- **Result**：D1A 通过；projection hit rate `0.9878`，target/background ratio mean `12.20 dB`；fixed-PFA 校准跑通，`1e-2 -> 0.0106`，`1e-3 -> 0.0012`。
- **Class policy**：`class=1` 按 D0B 审计结果作为 cyclist-like 处理；objectness mask 使用所有合法目标类。
- **Artifacts**：
  - `refine-logs/D1A_GAO77_CLEAN_FIXED_PFA_SANITY_REPORT.md`
  - `results/d1a_gao77_clean_sanity/metrics_clean_fixed_pfa.json`
  - `results/d1a_gao77_clean_sanity/projection_quality_summary.csv`
  - `results/d1a_gao77_clean_sanity/target_split_summary.csv`
  - `gao_77ghz_raw_adc/reports/d1a_figures/`

## D1A+ Gao77 Mask Stress Test — 2026-06-26 16:52

- **System**：Gao77 range-only clean sanity 的 mask width / guard ring / fixed-PFA stability 补充检查，未训练模型，未进入 D1B。
- **Config**：`subset_d1a_v1`，narrow/default/wide 三种 target mask，guard=2/4/6，target PFA=`1e-2` 和 `1e-3`；RA projection 仅作轻量 sanity。
- **Result**：D1A+ 通过但需要谨慎；默认 mask 平均 target cells=`45.68`，比 narrow=`32.61` 偏宽；weak Pd/F1 对 mask 宽度敏感。默认口径下 PFA `1e-2 -> 0.0106`，`1e-3 -> 0.0012`，bootstrap 稳定；RA projection hit rate=`0.8763`，低于 range-only。
- **Caution**：target mask overlap 较重，overlapped target ratio=`0.7720`；D1B 应增加 `non-overlap only` 辅助统计，并同时报告 narrow/default mask。
- **Recommendation**：可以进入 D1B synthetic interference sanity，但第一版应先做 range-only D1B；RA 暂时只作为辅助可视化。
- **Artifacts**：
  - `refine-logs/D1A_PLUS_MASK_STRESS_TEST_REPORT.md`
  - `results/d1a_plus_mask_stress_test/mask_width_sensitivity.csv`
  - `results/d1a_plus_mask_stress_test/guard_sensitivity.csv`
  - `results/d1a_plus_mask_stress_test/mask_overlap_summary.csv`
  - `results/d1a_plus_mask_stress_test/pfa_stability_summary.csv`
  - `results/d1a_plus_mask_stress_test/pfa_by_sequence.csv`
  - `results/d1a_plus_mask_stress_test/pd_by_class_group.csv`
  - `results/d1a_plus_mask_stress_test/ra_projection_sanity.csv`
  - `gao_77ghz_raw_adc/reports/d1a_plus_figures/`

## D1B Gao77 Synthetic Interference Sanity — 2026-06-26 17:30

- **System**：Gao77 raw ADC / IF 层 simplified synthetic FMCW-like mutual interference 注入 + range-only fixed-PFA evaluation，未训练模型，未进入 D2。
- **Config**：`subset_d1a_v1`，SIR=`+10/0/-10 dB`，对应 light/medium/severe；narrow/default mask；Protocol A clean-threshold degradation 与 Protocol B input-specific fixed-PFA recalibration。
- **Result**：D1B 通过。Achieved SIR 与设定一致；Protocol A 下 false alarm 从 clean `419` 增至 light `587`、medium `892`、severe `821`；Protocol B default mask、PFA=`1e-2` 下 weak Pd 从 clean `0.4266` 降至 light `0.3795`、medium `0.1629`、severe `0.0000`。
- **Caution**：light 档 median noise floor 只轻微上升 `0.0641 dB`，但 background energy 上升 `0.5307 dB`；D2 必须继续保留 narrow/default 与 non-overlap-only 辅助统计。
- **Recommendation**：可以进入 D2 simple FCN / AENN 小 batch overfit；D2 不应把 D1B synthetic model 包装成完整真实物理互扰模型。
- **Artifacts**：
  - `refine-logs/D1B_GAO77_SYNTHETIC_INTERFERENCE_SANITY_REPORT.md`
  - `results/d1b_gao77_synthetic_interference_sanity/d1b_interference_config.json`
  - `results/d1b_gao77_synthetic_interference_sanity/d1b_achieved_sir_summary.csv`
  - `results/d1b_gao77_synthetic_interference_sanity/d1b_protocol_a_clean_threshold_metrics.csv`
  - `results/d1b_gao77_synthetic_interference_sanity/d1b_protocol_b_fixed_pfa_recalibrated_metrics.csv`
  - `results/d1b_gao77_synthetic_interference_sanity/d1b_metrics_non_overlap_only.csv`
  - `gao_77ghz_raw_adc/reports/d1b_figures/`

## D2A Gao77 Small Model Sanity — 2026-06-26 21:15

- **System**：Gao77 range-only simple FCN 小 batch / 小子集 overfit sanity，未进入 D3，未跑正式 baseline。
- **Config**：train `128` frames × light/medium = `256` samples；validation `64` frames × light/medium = `128` samples；test `64` frames with light/medium/severe stress；batch size `4`，device `cuda`。
- **Result**：D2A 通过。tiny loss `0.3037 -> 0.0014`；small subset val loss `0.1971 -> 0.0053`；val MSE 从 interfered `3.7046` 降到 model `0.0998`。
- **Fixed-PFA sanity**：default mask、PFA=`1e-2`、medium 干扰下，interfered weak Pd=`0.3971`，model output weak Pd=`0.5294`；model(clean) MSE=`0.0287`，clean no-harm 未明显失败。
- **Caution**：D2A 只证明 dataloader、simple FCN、loss 和 fixed-PFA evaluation 链路能跑通，不能作为正式方法效果或 baseline。
- **Recommendation**：可以进入 D3；D3 应先跑 MSE/MAGMSE baseline 和 ordinary differentiable CA-CFAR BCE，不要直接上 weak-target full loss。
- **Artifacts**：
  - `refine-logs/D2A_GAO77_SMALL_MODEL_SANITY_REPORT.md`
  - `results/d2a_gao77_small_model_sanity/d2a_config.json`
  - `results/d2a_gao77_small_model_sanity/d2a_dataset_manifest.csv`
  - `results/d2a_gao77_small_model_sanity/d2a_training_loss.csv`
  - `results/d2a_gao77_small_model_sanity/d2a_fixed_pfa_metrics.csv`
  - `results/d2a_gao77_small_model_sanity/d2a_clean_no_harm_metrics.csv`
  - `gao_77ghz_raw_adc/reports/d2a_figures/`

## D3 Gao77 Baseline Sanity — 2026-06-26 21:40

- **System**：Gao77 range-only baseline sanity，只比较 MSE/MAGMSE reconstruction baseline 与 ordinary differentiable CA-CFAR BCE baseline；未进入 D4-D14。
- **Config**：train `512` frames cap，实际 `600` train samples；validation `320` samples；test `160` frames with light/medium/severe stress；batch size `4`，device `cuda`。
- **Result**：D3 未通过。MSE baseline 训练成功，tiny loss `0.2430 -> 0.0033`，val loss `0.0111 -> 0.0028`；ordinary BCE 训练也下降，tiny loss `1.0012 -> 0.6738`，val loss `1.2931 -> 0.7992`。
- **Fixed-PFA finding**：default mask、PFA=`1e-2`、medium 干扰下，MSE output weak Pd=`0.3626`、F1=`0.1322`；ordinary BCE output weak Pd=`0.7061`、F1=`0.3296`，检测指标不差于 MSE。
- **Failure reason**：ordinary BCE 的 clean-input no-harm 和幅度重建稳定性失败；BCE model(clean) MSE≈`96.65`，BCE output medium MSE≈`96.34`，target peak abs bias≈`4.56 dB`。
- **Recommendation**：暂不进入 D4；先检查 CFAR BCE loss 的数值尺度、mask 口径、temperature / learning rate，以及是否需要最小重建约束。
- **Artifacts**：
  - `refine-logs/D3_GAO77_BASELINE_SANITY_REPORT.md`
  - `results/d3_gao77_baseline_sanity/d3_config.json`
  - `results/d3_gao77_baseline_sanity/d3_training_loss_mse.csv`
  - `results/d3_gao77_baseline_sanity/d3_training_loss_bce.csv`
  - `results/d3_gao77_baseline_sanity/d3_fixed_pfa_metrics.csv`
  - `results/d3_gao77_baseline_sanity/d3_baseline_comparison_summary.csv`
  - `gao_77ghz_raw_adc/reports/d3_figures/`

## D3-RCA BCE Failure Analysis — 2026-06-26 21:59

- **System**：ordinary differentiable CA-CFAR BCE baseline failure root-cause analysis；未进入 D4，未做 focal / balanced BCE / weak-target full loss。
- **Config**：小规模复现 pure BCE，并做 temperature sweep、learning-rate sweep、`BCE + lambda_rec * MAGMSE` reconstruction-anchor 诊断；device `cuda`。
- **Result**：RCA 完成。未发现数值域 / normalization bug，未发现 target/background label 反转或 guard ring 被错误当 background；differentiable CFAR 未出现全 0 / 全 1。
- **Failure reason**：pure BCE 会学到 detection-shaping 而不是 signal restoration。reference pure BCE 下 output MSE=`44.75`，model(clean) MSE=`28.88`，weak Pd=`0.6324`。
- **Anchor diagnosis**：加入 reconstruction anchor 后幅度破坏显著下降；`lambda_rec=1.0` 时 model(clean) MSE=`0.1062`，output MSE=`0.6936`，weak Pd=`0.5294`。
- **Recommendation**：仍不进入 D4；先重跑修正后的 D3，保留 pure BCE 作为失败对照，同时测试带最小 MAGMSE anchor 的 BCE baseline。
- **Artifacts**：
  - `refine-logs/D3_RCA_BCE_FAILURE_ANALYSIS_REPORT.md`
  - `results/d3_rca_bce_failure_analysis/tensor_domain_check.csv`
  - `results/d3_rca_bce_failure_analysis/bce_mask_label_check.csv`
  - `results/d3_rca_bce_failure_analysis/diff_cfar_stability_check.csv`
  - `results/d3_rca_bce_failure_analysis/temperature_sweep.csv`
  - `results/d3_rca_bce_failure_analysis/learning_rate_sweep.csv`
  - `results/d3_rca_bce_failure_analysis/reconstruction_anchor_summary.csv`
  - `results/d3_rca_bce_failure_analysis/clean_input_behavior.csv`
  - `gao_77ghz_raw_adc/reports/d3_rca_figures/`

## D3-Rerun Gao77 Baseline Sanity — 2026-06-26 22:18

- **System**：修正后的 D3 range-only baseline sanity；比较 MSE/MAGMSE、pure BCE failure control、`BCE + lambda_rec * MAGMSE`，未进入 D4。
- **Config**：SimpleRangeFCN；train light+medium，test light/medium/severe；`lr=3e-4`，`temperature=1.0`；`lambda_rec={0.1,0.5,1.0}`；device `cuda`。
- **Result**：D3-Rerun 通过。pure BCE 复现 detection-shaping，output MSE=`63.11`，model(clean) MSE=`53.20`，但 weak Pd=`0.6489`，因此只作为 invalid failure control。
- **Best baseline**：`lambda_rec=0.5` 最稳；medium/default/PFA=1e-2 下 weak Pd=`0.3817`，MSE weak Pd=`0.3702`；model(clean) MSE=`0.0490`，target peak abs bias=`0.1294`。
- **Checks**：clean no-harm 通过；narrow/default 与 all/non-overlap 趋势一致；per-sequence PFA 无明显异常；motorbike_like 当前 test 子集为 0，不能单独解读。
- **Recommendation**：可以进入 D4，但 D4 仍只做 tuned balanced BCE / focal loss 强 baseline，不直接进入 weak-target full loss。
- **Artifacts**：
  - `refine-logs/D3_RERUN_GAO77_BASELINE_SANITY_REPORT.md`
  - `results/d3_rerun_gao77_baseline_sanity/d3_rerun_config.json`
  - `results/d3_rerun_gao77_baseline_sanity/d3_rerun_fixed_pfa_metrics.csv`
  - `results/d3_rerun_gao77_baseline_sanity/d3_rerun_lambda_rec_summary.csv`
  - `results/d3_rerun_gao77_baseline_sanity/d3_rerun_baseline_comparison_summary.csv`
  - `gao_77ghz_raw_adc/reports/d3_rerun_figures/`

## D4 Gao77 Strong Baseline Sanity — 2026-06-26 23:15

- **System**：tuned balanced BCE / focal loss 强 baseline sanity；未进入 D5，未做 weak-target-weighted loss。
- **Config**：MSE 与 BCE+rec anchor 复用 D3-Rerun；训练 `balanced_mild`、`balanced_full`、`focal_g1_a0p25`、`focal_g1_a0p5`、`focal_g2_a0p25`、`focal_g2_a0p5`；均使用 `lambda_rec=0.5`、`lr=3e-4`、`temperature=1.0`、SimpleRangeFCN。
- **Result**：D4 通过。所有 balanced/focal 分支都稳定训练，fixed-PFA evaluation 可跑，clean no-harm 未灾难性失败。
- **Best strong baseline**：`balanced_mild`。medium/default/PFA=1e-2 下 weak Pd=`0.3817`，F1=`0.1369`，model(clean) MSE≈`0.0450`，target peak abs bias=`0.1203`。
- **Comparison**：`balanced_mild` 的 weak Pd 与 BCE+rec anchor 相同，但 F1 和 clean MSE 略好；强于 MSE baseline。focal 中较强的是 `focal_g1_a0p25`，weak Pd=`0.3817`，但 F1 略低于 balanced_mild。
- **Recommendation**：可以进入 D5 weak-target-weighted loss；D5 必须把 `balanced_mild` 作为主强对照，避免被说成只是 class imbalance trick。
- **Artifacts**：
  - `refine-logs/D4_GAO77_STRONG_BASELINE_SANITY_REPORT.md`
  - `results/d4_gao77_strong_baseline_sanity/d4_config.json`
  - `results/d4_gao77_strong_baseline_sanity/d4_training_loss_balanced.csv`
  - `results/d4_gao77_strong_baseline_sanity/d4_training_loss_focal.csv`
  - `results/d4_gao77_strong_baseline_sanity/d4_fixed_pfa_metrics.csv`
  - `results/d4_gao77_strong_baseline_sanity/d4_best_baseline_selection.csv`
  - `gao_77ghz_raw_adc/reports/d4_figures/`

## D5 Gao77 Weak-Target-Weighted Sanity — 2026-06-27 12:15

- **System**：weak-target-weighted detection loss sanity；只执行 D5，未进入 D6-D14，未加入 false alarm penalty、clean identity full method 或 proposed full loss。
- **Config**：SimpleRangeFCN；train/val 使用 light+medium，test 使用 light/medium/severe；loss=`weak_target_weighted_detection_loss + 0.5 * MAGMSE`；weak 定义测试 `clean_peak_percentile` 和 `cfar_margin`，weak weight=`2/3/5`；单 seed。
- **Result**：D5 通过。best 配置为 `weak_peak_w2p0`，medium/default/PFA=`1e-2` 下 weak Pd=`0.3855`，高于 D4 strong baseline `balanced_mild` 的 `0.3817`。
- **Safety checks**：`weak_peak_w2p0` 的 mid Pd=`0.9756`、strong Pd=`1.0000` 未降；measured PFA=`0.0105`、false alarm=`149`，没有高于 `balanced_mild` 的 `150`；model(clean) MSE=`0.0453`，target peak abs bias=`0.1144`，clean no-harm 正常。
- **Caution**：提升幅度很小，仍是 Gao77 + synthetic interference + range-only sanity；不能包装成最终方法效果。CFAR-margin weak 定义表现差，不建议作为 D6 主口径。
- **Recommendation**：可以进入 D6 false alarm penalty，但 D6 必须验证 weak Pd 提升不是靠 false alarm 或 target peak inflation 换来的。
- **Artifacts**：
  - `experiments/d5_gao77_weak_target_weighted_sanity.py`
  - `refine-logs/D5_GAO77_WEAK_TARGET_WEIGHTED_SANITY_REPORT.md`
  - `refine-logs/D5_GAO77_WEAK_TARGET_WEIGHTED_SANITY_REPORT_20260627_121516.md`
  - `results/d5_gao77_weak_target_weighted_sanity/d5_config.json`
  - `results/d5_gao77_weak_target_weighted_sanity/d5_best_config_selection.csv`
  - `results/d5_gao77_weak_target_weighted_sanity/d5_weight_sweep_summary.csv`
  - `results/d5_gao77_weak_target_weighted_sanity/d5_fixed_pfa_metrics.csv`
  - `results/d5_gao77_weak_target_weighted_sanity/d5_clean_no_harm_metrics.csv`
  - `gao_77ghz_raw_adc/reports/d5_figures/`

## D5-check Improvement Significance — 2026-06-27 12:46

- **System**：D5 weak-target-weighted improvement significance check；只比较 D4 `balanced_mild` 和 D5 `weak_peak_w2p0`，未进入 D6。
- **Config**：原始 split 上做 3 seeds mini-check；额外做一个 alternate split 轻量检查；不加入 false alarm penalty、clean identity full method、proposed full loss 或新 backbone。
- **Hit-count finding**：原始 D5 主口径 medium/default/all/PFA=`1e-2` 只从 `100/262` weak hits 提到 `101/262`，只多 hit `1` 个 weak target，属于 statistically weak signal。
- **3 seeds result**：`balanced_mild` weak Pd mean=`0.3766`、std=`0.0058`；`weak_peak_w2p0` weak Pd mean=`0.3690`、std=`0.0172`；平均 gain=`-0.0076`，没有超过随机波动。
- **Robustness**：narrow/default 不一致，all/non-overlap-only 不一致，PFA=`1e-3` 不稳定；clean no-harm 正常。
- **Decision**：不建议进入 D6。下一步应先修 weak target 定义，检查模型容量，或升级 RD/RA 表示；当前 range-only weak weighting 更接近弱证据/负结果。
- **Artifacts**：
  - `experiments/d5_check_improvement_significance.py`
  - `refine-logs/D5_CHECK_IMPROVEMENT_SIGNIFICANCE_REPORT.md`
  - `refine-logs/D5_CHECK_IMPROVEMENT_SIGNIFICANCE_REPORT_20260627_124618.md`
  - `results/d5_check_improvement_significance/d5_check_decision_summary.csv`
  - `results/d5_check_improvement_significance/d5_check_hit_count_comparison.csv`
  - `results/d5_check_improvement_significance/d5_check_seed_summary.csv`
  - `results/d5_check_improvement_significance/d5_check_mask_robustness.csv`
  - `results/d5_check_improvement_significance/d5_check_split_robustness.csv`
  - `gao_77ghz_raw_adc/reports/d5_check_figures/`

## D5-diagnosis Weak Weighting Failure Diagnosis — 2026-06-27 13:58

- **System**：D5 weak-target weighting 不稳定原因诊断；只比较 `balanced_mild` 和 `weak_peak_w2p0`，未进入 D6，未加入 false alarm penalty、clean identity full method 或 proposed full loss。
- **Config**：使用 `cuda` / GTX 1650；固定 validation/test；train-size 检查使用 `600/1000/1500` effective train samples。由于 D1A split 中非泄漏训练独立帧只有 `300` 帧，1000/1500 effective samples 是重复训练帧生成新的 synthetic interference，不是新增真实 clean frame 多样性。
- **Train-size finding**：600 samples 下 weak Pd gain=`-0.0153`；1000 samples 下 gain=`0.0000`；1500 samples 下 gain=`0.0229`、多 hit `6` 个 weak target，且 false alarm count delta=`-3`。这说明训练样本量可能是瓶颈之一，但证据仍不够稳。
- **Capacity finding**：600 samples 容量检查中，current SimpleRangeFCN gain=`0.0115`，wider FCN gain=`0.0000`，shallow 1D U-Net gain=`-0.0076`；容量增大没有系统性扩大 weak-weighting 收益。
- **Weak-definition finding**：`clean_peak_percentile` weak targets 的 overlap-mask ratio=`0.4965`；`cfar_margin` weak targets overlap-mask ratio=`0.6701`；两种 weak set 的 Jaccard=`0.5448`。range-only weak target 定义明显受 mask overlap 污染。
- **Decision**：不建议进入 D6。原因是 PFA=`1e-3` 不支持，容量检查不支持，weak 定义受 range-only overlap 污染；下一步优先修 weak target 定义或升级 RD/RA 表示，也可以把当前 range-only weak weighting 作为负结果记录。
- **Artifacts**：
  - `experiments/d5_diagnosis_weak_weighting_failure.py`
  - `refine-logs/D5_DIAGNOSIS_WEAK_WEIGHTING_FAILURE_REPORT.md`
  - `refine-logs/D5_DIAGNOSIS_WEAK_WEIGHTING_FAILURE_REPORT_20260627_135855.md`
  - `results/d5_diagnosis_weak_weighting_failure/d5_diagnosis_decision_summary.csv`
  - `results/d5_diagnosis_weak_weighting_failure/d5_scale_gain_by_train_size.csv`
  - `results/d5_diagnosis_weak_weighting_failure/d5_capacity_check_summary.csv`
  - `results/d5_diagnosis_weak_weighting_failure/d5_weak_definition_diagnostics.csv`
  - `results/d5_diagnosis_weak_weighting_failure/d5_weak_target_overlap_analysis.csv`
  - `gao_77ghz_raw_adc/reports/d5_diagnosis_figures/`

## D5B-D5C Weak Definition / RD-RA Diagnosis — 2026-06-27 15:32

- **System**：D5B weak definition repair + D5C RD/RA feasibility smoke；未进入 D6，未加入 false alarm penalty、clean identity full method 或 proposed full loss，未修改 detector/CFAR 主评价协议。
- **Config**：主 baseline 为 `balanced_mild`；weak weighting 只做 `weak_peak_w2p0` 最小 sanity；比较 `clean_peak_percentile`、non-overlap-only、overlap-aware、isolated-only、peak/local-background ratio、range-bin uniqueness 等 weak definitions；RD/RA 只做 projection/fixed-PFA smoke。
- **D5B result**：只有未修复的 `clean_peak_percentile` 达到 weak Pd delta=`0.0267`、hit delta=`+7`；repaired definitions 未同时达到 weak Pd gain >=`0.02` 和 hit delta >=`+5`。best repaired row `clean_peak_overlap_aware` 为 weak Pd delta=`0.0182`、hit delta=`+4`。
- **D5C result**：RD smoke 显示 weak separability proxy 明显高于 range-only，且 fixed-PFA sanity 可跑；RA overlap 下降但 weak projection hit rate 很低，判为 inconclusive。RD/RA 均只能写 feasibility evidence，不能写 confirmed improvement。
- **Audit / claim gate**：`/experiment-audit` verdict=`WARN`，主要因为 weak strata 是 clean-map-derived proxy、D5C 是 smoke proxy；`/result-to-claim` verdict=`partial`、integrity=`warn`、confidence=`medium`。
- **Decision**：记录 range-only weak weighting 为 weak/negative evidence；允许后续只做受限 RD-only feasibility confirmation；D6 继续 NO-GO。
- **Artifacts**：
  - `experiments/d5b_d5c_weak_definition_rdra_diagnosis.py`
  - `experiments/analyze_d5b_d5c_results.py`
  - `results/d5b_d5c_weak_definition_rdra_diagnosis/d5b_weak_definition_audit.csv`
  - `results/d5b_d5c_weak_definition_rdra_diagnosis/d5b_repaired_definition_results.csv`
  - `results/d5b_d5c_weak_definition_rdra_diagnosis/d5c_range_rd_ra_separability.csv`
  - `results/d5b_d5c_weak_definition_rdra_diagnosis/D5B_D5C_ANALYZE_RESULTS.md`
  - `results/d5b_d5c_weak_definition_rdra_diagnosis/EXPERIMENT_AUDIT.md`
  - `results/d5b_d5c_weak_definition_rdra_diagnosis/RESULT_TO_CLAIM.md`
  - `gao_77ghz_raw_adc/reports/d5b_d5c_figures/`
