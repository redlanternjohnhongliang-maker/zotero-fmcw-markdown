# D1A Gao77 Clean Fixed-PFA Sanity 报告

生成时间：2026-06-26 16:20  
阶段：D1A clean radar map / target-background mask / fixed-PFA sanity  
数据子集：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

## 1. 执行边界

本次只执行 D1A。没有进入 D2-D14，没有训练模型，没有做 synthetic interference injection，没有做干扰抑制模型，没有使用 AENN / FCN / RDLR-Net / DiffRIM / RIMformer，也没有下载新数据集。

## 2. 总体结论

| 问题 | 结论 |
|---|---|
| D1A 是否通过 | 通过 |
| 使用 representation | range-only 为主；RD/RA 只做 smoke visualization |
| label projection 是否可信 | 基本可信 |
| target mask 是否可信 | 基本可信 |
| background mask 是否可信 | 基本可信 |
| guard ring 是否实现 | 已实现 |
| hard CA-CFAR 是否正常 | 正常 |
| differentiable CA-CFAR 是否正常 | 已实现 forward，soft target/background 有差异 |
| 是否建议进入 D1B | 可以进入 D1B synthetic interference sanity，但仍然只做 sanity |

## 3. class=1 处理

D1A 采用以下处理：

```python
GAO77_LABEL_MAP = {0: 'person', 1: 'cyclist_alias_or_bicycle', 2: 'car', 3: 'motorbike', 5: 'bus', 7: 'truck', 80: 'cyclist'}
GAO77_CLASS_GROUP = {0: 'pedestrian_like', 1: 'cyclist_like', 2: 'vehicle_like', 3: 'motorbike_like', 5: 'vehicle_like', 7: 'vehicle_like', 80: 'cyclist_like'}
```

class=1 is treated as cyclist-like for D1A sanity based on data audit and image inspection, not because it is explicitly defined in the official README.

本次已读取本地核查文件：

`G:\mineru_output\refine-logs\D0B_CLASS1_SEMANTICS_CHECK.md`

该处理不会影响 objectness mask sanity，因为 D1A 的 target mask 只关心合法目标区域，不做类别分类。objectness target classes 为 `[0, 1, 2, 3, 5, 7, 80]`。

## 4. Clean Representation

- `adcData` shape 检查：`{'128x255x4x2': 1500}`
- range resolution：0.2237 m/bin
- range-only profile：已生成，用于主 projection / mask / fixed-PFA sanity
- RD map：已生成抽样图，仅作 smoke test，不声称 RD target mask 是精确真值
- RA map：已生成抽样图，采用粗略 angle FFT 和 label projection，仅作可视化检查

## 5. Projection 质量

整体 projection：

| 指标 | 数值 |
|---|---:|
| target count | 6168 |
| valid projection count | 6168 |
| projection hit count | 6093 |
| projection hit rate | 0.9878 |
| target peak mean dB | 60.1354 |
| neighbor peak mean dB | 53.8333 |
| neighbor mean dB | 47.9397 |
| target/background ratio mean dB | 12.1956 |
| projection pass | True |

per-source-sequence projection hit rate：

| sequence | targets | valid | hit rate | ratio dB |
|---|---|---|---|---|
| 2019_05_09_cm1s003 | 1378 | 1378 | 1.0000 | 15.7635 |
| 2019_05_09_bm1s007 | 1484 | 1484 | 0.9987 | 10.8429 |
| 2019_04_30_mlms000 | 669 | 669 | 0.9836 | 9.0339 |
| 2019_05_09_mlms003 | 1896 | 1896 | 0.9800 | 13.2037 |
| 2019_04_30_mlms001 | 741 | 741 | 0.9676 | 8.5451 |

per-class projection hit rate：

| class id | targets | valid | hit rate | ratio dB |
|---|---|---|---|---|
| 0 | 1439 | 1439 | 0.9618 | 9.7090 |
| 1 | 77 | 77 | 1.0000 | 9.4556 |
| 2 | 3132 | 3132 | 0.9994 | 13.1196 |
| 80 | 1520 | 1520 | 0.9882 | 12.7847 |

per-class-group projection hit rate：

| group | targets | valid | hit rate | ratio dB |
|---|---|---|---|---|
| cyclist_like | 1597 | 1597 | 0.9887 | 12.6242 |
| pedestrian_like | 1439 | 1439 | 0.9618 | 9.7090 |
| vehicle_like | 3132 | 3132 | 0.9994 | 13.1196 |

projection 最好的 sequence：`2019_05_09_cm1s003`。projection 最差的原始 class：`0`。

## 6. Mask 统计

| 指标 | 数值 |
|---|---:|
| target cells mean | 45.68 |
| target cells min/max | 7 / 76 |
| guard cells mean | 12.02 |
| background cells mean | 65.37 |
| background cells min/max | 36 / 108 |

规则：

- target mask：range-only 投影窗口；
- guard ring：target window 外扩 4 bins；
- background：valid FOV 内排除 target mask 与 guard ring；
- DC / leakage：排除 range bin `< 2`；
- 边缘：排除 range bin `> 124`。

## 7. Weak / Mid / Strong Split

| definition | group | count | mean | std | min | max |
|---|---|---|---|---|---|---|
| clean_peak_percentile | weak | 1851 | 52.6466 | 3.0831 | 43.4717 | 57.2429 |
| clean_peak_percentile | mid | 2466 | 60.5181 | 2.9379 | 57.2447 | 64.6164 |
| clean_peak_percentile | strong | 1851 | 67.1144 | 2.3220 | 64.6177 | 83.3971 |
| cfar_margin | weak | 1852 | 4.1947 | 2.2095 | -4.9543 | 7.0924 |
| cfar_margin | mid | 2465 | 10.3192 | 2.2946 | 7.0925 | 14.2857 |
| cfar_margin | strong | 1851 | 16.2814 | 1.4187 | 14.2861 | 25.3829 |

clean peak percentile split 和 CFAR-margin split 都能产生数量可用的 weak/mid/strong 分组。当前只能说明代码链路和分布切分可用，不能把 clean-only 结果包装成抗干扰结论。

## 8. Fixed-PFA Clean Baseline

| split | target PFA | threshold | test PFA | weak Pd | mid Pd | strong Pd | overall Pd | F1 |
|---|---|---|---|---|---|---|---|---|
| clean_peak_percentile | 0.0100 | 3.7472 | 0.0106 | 0.4266 | 0.9377 | 1.0000 | 0.7968 | 0.1489 |
| cfar_margin | 0.0100 | 3.7472 | 0.0106 | 0.3347 | 1.0000 | 1.0000 | 0.7968 | 0.1489 |
| clean_peak_percentile | 0.0010 | 5.8261 | 0.0012 | 0.2624 | 0.6691 | 0.9970 | 0.6354 | 0.1037 |
| cfar_margin | 0.0010 | 5.8261 | 0.0012 | 0.0000 | 0.8554 | 1.0000 | 0.6354 | 0.1037 |

说明：当前只有 clean input，没有 interfered 或 mitigated 输出。这里报告的是 clean baseline fixed-PFA sanity，不是干扰抑制效果。

## 9. Differentiable CA-CFAR

| 指标 | 数值 |
|---|---:|
| threshold used | 3.7472 |
| temperature | 0.7000 |
| hard/soft score correlation | 0.9642 |
| soft target mean | 0.1051 |
| soft background mean | 0.0341 |

当前只验证 forward 和指标计算，没有训练任何模型。

## 10. 输出文件

结果目录：

`G:\mineru_output\results\d1a_gao77_clean_sanity`

关键文件：

- `metrics_clean_fixed_pfa.csv`
- `metrics_clean_fixed_pfa.json`
- `target_split_summary.csv`
- `mask_cell_counts.csv`
- `projection_quality_summary.csv`
- `projection_quality_by_sequence.csv`
- `projection_quality_by_class.csv`
- `projection_quality_by_class_group.csv`
- `cfar_params.json`
- `dataset_split.json`
- `d1a_config.json`

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\d1a_figures`

## 11. 下一步建议

建议进入 D1B synthetic interference injection sanity。D1B 仍然只做 sanity：先验证 synthetic interference 注入、clean/interfered pair、mask 与 fixed-PFA 指标链路，不训练模型。
