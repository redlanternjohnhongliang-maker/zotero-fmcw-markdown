# 给 GPT 的单文件交接稿：D5D RD-only supplementary experiment

项目：Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation

任务：D5D-RD-only constrained supplementary experiment for FMCW fixed-PFA weak-target preservation

日期：2026-06-27

## 1. 请 GPT 重点判断什么

请判断 D5D 的 RD-only 补充实验是否支持继续 weak-target weighting，是否允许进入 D6，以及当前结果应该如何写成论文/项目结论。

预注册 GO 条件：

- weak Pd delta >= 0.02
- weak hit delta >= +5
- measured PFA 不上升
- false alarm count 不上升
- clean no-harm 通过
- default/narrow mask 方向一致
- all/non-overlap 方向一致
- PFA=1e-3 不明显反向
- 多 seed 平均 gain 不低于 balanced_mild
- 无 weak threshold leakage

## 2. 最终结论

结论：NO-GO。

D6 仍然禁止。

D5D 只支持这个保守说法：

在 2-seed RD-only proxy sanity experiment 中，weak weighting 没有比 `balanced_mild` 改善 weak-target preservation。PFA=1e-2 下 PFA/false alarm 没上升，clean no-harm 通过，但 weak Pd delta = 0、weak hit delta = 0，且 PFA=1e-3 在 seed 200 反向。因此不能进入 D6，也不能写成 confirmed RD performance。

## 3. 关键数字

主结果来自：

`G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_seed_summary.csv`

2 seeds：

| seed | balanced weak Pd | weak weighting weak Pd | weak Pd delta | weak hit delta | PFA delta | FA delta | PFA=1e-3 weak Pd delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| 42 | 1.0000 | 1.0000 | 0.0000 | 0 | -0.000019 | -57 | 0.0000 |
| 200 | 1.0000 | 1.0000 | 0.0000 | 0 | -0.000009 | -26 | -0.0323 |

mean/std：

`G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_seed_mean_std.csv`

- mean weak Pd delta = 0.0000
- mean weak hit delta = 0
- mean measured PFA delta = -1.396e-05
- mean false alarm count delta = -41.5
- mean PFA=1e-3 weak Pd delta = -0.0161

Weak threshold：

`G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_weak_thresholds.json`

- threshold source = train split only
- train weak threshold q30 = 50.5937 dB
- train weak_n = 56
- val weak_n = 64
- test weak_n = 62
- threshold_leakage = false
- used_test_clean_map_property_for_threshold = false

## 4. 审计结论

审计文件：

`G:\mineru_output\results\d5d_rd_only_supplementary\EXPERIMENT_AUDIT.md`

审计 verdict：WARN。

原因：

- 数字、文件、一致性、fixed-PFA、train-only threshold 都通过。
- 但 RD target boxes 使用的是 `range label + clean-RD Doppler peak projection`，不是真实 Doppler/velocity ground truth。
- 因此 evaluation type 是 `mixed_proxy`，只能称为 RD-only supplementary proxy sanity，不能称为 confirmed RD performance。

## 5. Result-to-Claim 结论

claim 文件：

`G:\mineru_output\results\d5d_rd_only_supplementary\RESULT_TO_CLAIM.md`

结论：

- claim_supported: no
- integrity_status: warn
- confidence: NO-GO decision high；broader RD suitability medium
- final_route: NO-GO do not enter D6

支持的内容：

- RD fixed-PFA proxy pipeline 能跑通。
- weak threshold 是 train-only frozen，没有 leakage。
- PFA=1e-2 下 PFA/FA 未上升。
- clean no-harm 通过。

不支持的内容：

- 不支持 RD weak weighting 改善 weak-target preservation。
- 不支持进入 D6。
- 不支持 confirmed RD performance。
- 不推翻此前 range-only weak weighting 的 weak/negative evidence。

## 6. 必要文件清单

如果只让 GPT 判断结论，给这些：

1. `G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_summary.md`
2. `G:\mineru_output\results\d5d_rd_only_supplementary\D5D_ANALYZE_RESULTS.md`
3. `G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_seed_summary.csv`
4. `G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_seed_mean_std.csv`
5. `G:\mineru_output\results\d5d_rd_only_supplementary\d5d_rd_weak_thresholds.json`
6. `G:\mineru_output\results\d5d_rd_only_supplementary\EXPERIMENT_AUDIT.md`
7. `G:\mineru_output\results\d5d_rd_only_supplementary\RESULT_TO_CLAIM.md`

如果让 GPT 审代码，再加：

8. `G:\mineru_output\experiments\d5d_rd_only_supplementary.py`
9. `G:\mineru_output\experiments\analyze_d5d_results.py`

## 7. 需要 GPT 注意的限制

- 本实验不是 D6。
- 没有 false alarm penalty。
- 没有 clean identity full method。
- 没有 proposed full loss。
- 没有 RDLR-Net / DiffRIM / RIMformer。
- 没有换大模型。
- 没有改 detector。
- 没有改 fixed-PFA 主评估协议。
- synthetic FMCW-like interference 不能写成真实物理干扰。
- RD 结果不能写成 confirmed RD performance。
- RD boxes 是 proxy：range label + clean-RD Doppler peak projection。

## 8. 建议让 GPT 回答的问题

请 GPT 回答：

1. D5D 是否支持继续 RD weak weighting？
2. D5D 是否允许进入 D6？
3. D5D 应该如何写成论文/项目结论？
4. range-only weak weighting 是否仍应写成 weak/negative evidence？
5. 如果还要补实验，必须先解决什么问题？

推荐答案应是保守的：

- 不继续 weak weighting。
- 不进入 D6。
- 记录 D5D 为 limited/negative RD-only proxy sanity。
- 如有后续，只能先解决 RD proxy/saturation 问题，不能直接做 D6。
