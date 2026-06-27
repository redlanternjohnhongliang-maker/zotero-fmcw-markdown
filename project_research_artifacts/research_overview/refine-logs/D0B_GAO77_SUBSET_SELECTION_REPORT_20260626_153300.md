# D0B Gao 77GHz 子集重新筛选与构建报告

生成时间：2026-06-26 15:33  
阶段：D0B 子集重新筛选  
数据包：`G:\mineru_output\gao_77ghz_raw_adc\Automotive.zip`

## 1. 执行边界

本次只做 Gao 77GHz 子集重新筛选与构建，没有进入 D1-D14，没有训练模型，没有做 synthetic interference injection，没有做 CFAR，也没有做 fixed-PFA threshold calibration。

## 2. 总体结果

- 共发现 sequence：22
- 最终选择方式：multi-sequence subset
- 最终子集路径：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`
- radar 文件：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1\radar_raw_frame`
- label 文件：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1\text_labels`
- manifest：`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1\manifest\selected_frames_manifest.csv`
- 最终子集帧数：1500
- 最终子集目标数：6168
- 最终子集 class 分布：`0:1439;1:77;2:3132;80:1520`

## 3. 每个 sequence 的基本统计

| sequence | aligned | targets | empty | 1目标帧 | 2+目标帧 | class | range span | azimuth span | score |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| `2019_04_09_bms1000` | 894 | 894 | 0 | 894 | 0 | `80:894` | 9.59 | 51.22 | 51.58 |
| `2019_04_09_cms1000` | 896 | 895 | 1 | 895 | 0 | `2:895` | 1.37 | 37.24 | 46.33 |
| `2019_04_09_css1000` | 894 | 894 | 0 | 894 | 0 | `2:894` | 0.15 | 0.08 | 38.87 |
| `2019_04_09_pms1000` | 895 | 893 | 2 | 893 | 0 | `0:893` | 7.37 | 29.66 | 48.03 |
| `2019_04_09_pms2000` | 895 | 1790 | 0 | 0 | 895 | `0:1790` | 9.59 | 54.36 | 67.39 |
| `2019_04_09_pms3000` | 895 | 2014 | 0 | 52 | 843 | `0:2014` | 8.40 | 91.37 | 69.39 |
| `2019_04_30_cm1s000` | 896 | 88 | 808 | 88 | 0 | `2:88` | 18.81 | 44.59 | 46.76 |
| `2019_04_30_mlms000` | 897 | 1992 | 0 | 86 | 811 | `0:897;2:250;80:845` | 21.09 | 78.94 | 82.82 |
| `2019_04_30_mlms001` | 897 | 2361 | 0 | 40 | 857 | `0:1336;2:461;80:564` | 20.88 | 84.75 | 84.53 |
| `2019_04_30_pbms002` | 897 | 1755 | 0 | 39 | 858 | `0:897;80:858` | 17.26 | 50.34 | 73.00 |
| `2019_04_30_pbss000` | 897 | 1794 | 0 | 0 | 897 | `0:897;80:897` | 0.38 | 19.00 | 60.45 |
| `2019_04_30_pcms001` | 897 | 1525 | 0 | 330 | 567 | `0:897;2:628` | 20.67 | 75.38 | 72.18 |
| `2019_05_09_bm1s007` | 897 | 4379 | 0 | 0 | 897 | `1:6;2:3588;80:785` | 15.35 | 103.19 | 87.00 |
| `2019_05_09_cm1s003` | 897 | 3766 | 0 | 0 | 897 | `2:3766` | 10.44 | 76.09 | 84.35 |
| `2019_05_09_mlms003` | 897 | 5784 | 0 | 0 | 897 | `0:2228;1:100;2:863;80:2593` | 22.16 | 105.76 | 95.30 |
| `2019_05_09_pbms004` | 897 | 1321 | 0 | 478 | 419 | `0:554;80:767` | 7.49 | 50.39 | 58.21 |
| `2019_05_09_pcms002` | 896 | 1268 | 2 | 521 | 373 | `0:852;2:416` | 18.18 | 66.80 | 64.49 |
| `2019_05_29_bcms000` | 897 | 911 | 23 | 837 | 37 | `2:8;3:33;7:454;80:416` | 14.49 | 87.62 | 68.11 |
| `2019_05_29_cm1s014` | 897 | 137 | 760 | 137 | 0 | `2:105;3:32` | 15.37 | 78.95 | 50.52 |
| `2019_05_29_mlms006` | 897 | 1471 | 0 | 472 | 425 | `0:525;2:280;80:666` | 14.50 | 77.35 | 67.82 |
| `2019_05_29_pbms007` | 897 | 1965 | 0 | 6 | 891 | `0:1069;3:129;80:767` | 12.57 | 55.42 | 72.49 |
| `2019_05_29_pcms005` | 897 | 327 | 693 | 81 | 123 | `2:126;80:201` | 11.93 | 12.57 | 46.50 |

完整 CSV：

- `results\d0b_gao77_subset_selection\sequence_label_stats.csv`
- `results\d0b_gao77_subset_selection\sequence_score_table.csv`

## 4. 为什么旧的 `cms1000` 不适合作为唯一 D1A 子集

旧子集 `2019_04_09_cms1000` 可读、对齐质量好，但它作为唯一 D1A sanity 子集太单一：

- aligned 帧数：896
- 目标总数：895
- class 分布：`2:895`
- 2+ 目标帧数：0
- range span：1.37 m
- azimuth span：37.24 deg

它基本是单类别、单目标、几何变化有限的 sequence，适合检查读取链路，但不适合作为 weak / mid / strong target split 的主要 sanity 子集。

## 5. 排名前 5 的候选 sequence

| 排名 | sequence | score | aligned | targets | 2+目标帧 | range span | azimuth span | class | 风险 |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `2019_05_09_mlms003` | 95.30 | 897 | 5784 | 897 | 22.16 | 105.76 | `0:2228;1:100;2:863;80:2593` | 无空标签帧 |
| 2 | `2019_05_09_bm1s007` | 87.00 | 897 | 4379 | 897 | 15.35 | 103.19 | `1:6;2:3588;80:785` | 无空标签帧 |
| 3 | `2019_04_30_mlms001` | 84.53 | 897 | 2361 | 857 | 20.88 | 84.75 | `0:1336;2:461;80:564` | 无空标签帧 |
| 4 | `2019_05_09_cm1s003` | 84.35 | 897 | 3766 | 897 | 10.44 | 76.09 | `2:3766` | 无空标签帧；类别单一 |
| 5 | `2019_04_30_mlms000` | 82.82 | 897 | 1992 | 811 | 21.09 | 78.94 | `0:897;2:250;80:845` | 无空标签帧 |

## 6. 候选 radar 抽样检查

对排名前 5 的候选 sequence，每个抽样 30 个 radar `.mat` 文件，只做读取、range FFT、简单 Doppler FFT 和粗略 label-to-range-bin 检查。

| sequence | sample | ok | bad | range peak mean dB | RD energy mean dB | label projection hit |
|---|---:|---:|---:|---:|---:|---:|
| `2019_05_09_mlms003` | 30 | 30 | 0 | 67.78 | 62.48 | 0.851 |
| `2019_05_09_bm1s007` | 30 | 30 | 0 | 68.09 | 62.32 | 0.788 |
| `2019_04_30_mlms001` | 30 | 30 | 0 | 67.15 | 61.20 | 0.896 |
| `2019_05_09_cm1s003` | 30 | 30 | 0 | 67.99 | 61.98 | 1.000 |
| `2019_04_30_mlms000` | 30 | 30 | 0 | 67.23 | 61.14 | 0.892 |

完整 CSV：

- `results\d0b_gao77_subset_selection\candidate_radar_sample_stats.csv`

## 7. 最终子集组成

最终没有选择单个 sequence，而是从排名靠前的多个 sequence 中构建 multi-sequence subset。原因是单个 sequence 即使对齐好，也容易存在类别、距离或角度覆盖不足；multi-sequence 更适合作为 D1A weak/mid/strong sanity 输入。

选中 sequence：

`2019_05_09_mlms003`, `2019_05_09_bm1s007`, `2019_04_30_mlms001`, `2019_05_09_cm1s003`, `2019_04_30_mlms000`

按来源统计：

| source sequence | frames | targets | empty | single | multi |
|---|---:|---:|---:|---:|---:|
| `2019_04_30_mlms000` | 300 | 669 | 0 | 44 | 256 |
| `2019_04_30_mlms001` | 300 | 741 | 0 | 16 | 284 |
| `2019_05_09_bm1s007` | 300 | 1484 | 0 | 0 | 300 |
| `2019_05_09_cm1s003` | 300 | 1378 | 0 | 0 | 300 |
| `2019_05_09_mlms003` | 300 | 1896 | 0 | 0 | 300 |

最终子集总体统计：

| 指标 | 数值 |
|---|---:|
| frame count | 1500 |
| target total | 6168 |
| empty frames | 0 |
| single-target frames | 60 |
| multi-target frames | 1440 |
| range min | 1.49 |
| range max | 23.86 |
| range mean | 13.22 |
| range std | 6.25 |
| azimuth min | -59.12 |
| azimuth max | 48.41 |
| azimuth mean | 0.18 |
| azimuth std | 34.02 |
| target count min | 1 |
| target count mean | 4.11 |
| target count median | 5.0 |
| target count max | 8 |

## 8. 是否比 `cms1000` 更适合 weak/mid/strong split

结论：是。

原因：

1. 最终子集来自多个 sequence，不再依赖单一静态几何；
2. range 覆盖明显更宽；
3. azimuth / px 覆盖明显更宽；
4. target count per frame 不再过于单一；
5. 类别分布更丰富；
6. radar 抽样读取正常，range FFT / RD smoke test 正常；
7. 子集规模约 1500 帧，适合 GTX 1650 4GB 上做小规模 D1A sanity。

注意：这仍然不是论文级最终数据集，只是为了 D1A sanity 更合理。

补充审计备注：最终子集中出现 `class id = 1`，但官方 README 示例 label_map 没有列出 1。已做 D0B 语义核查：`class=1` 只出现在 `2019_05_09_mlms003` 和 `2019_05_09_bm1s007`，全量共 106 个，尺寸恒为 `0.6 × 1.7`，与 cyclist/bicycle 目标尺寸一致；抽样相机图也显示对应场景中存在自行车目标。因此 D1A sanity 中建议把 `class=1` 作为 `cyclist/bicycle` 的高置信别名处理，和 `class=80` 一起归入 cyclist-like 类。因为官方 README 未显式定义 1，报告和代码里仍应保留备注，不要把它包装成官方声明。

## 9. 可视化输出

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\d0b_figures`

至少包含：

- `all_sequences_range_spread_ranking.png`
- `all_sequences_azimuth_spread_ranking.png`
- `all_sequences_target_count_per_frame_distribution.png`
- `candidate_sequences_range_histogram.png`
- `candidate_sequences_azimuth_histogram.png`
- `selected_subset_range_histogram.png`
- `selected_subset_azimuth_histogram.png`
- `selected_subset_target_count_per_frame_histogram.png`
- `sample_range_profile_*.png`
- `sample_rd_map_*.png`
- `sample_label_to_range_*.png`

## 10. 是否建议进入 D1A

建议进入 D1A，但仍然只进入 D1A sanity，不训练模型。

进入 D1A 前应继续保持限制：

1. 先做 label 到 range / angle / RD mask 的可视化检查；
2. 不要直接训练；
3. 不要把这个子集包装成最终实验数据；
4. 如果 target/background mask 明显不合理，再回到 D0B 调整子集或换数据集。

## 11. 阻塞点

当前没有硬阻塞点。主要风险是 Gao 标签是物理坐标框，不是直接 RD/RDA cell mask；D1A 必须先把坐标到 radar map 的粗投影链路验证清楚。

## 12. 简短结论

| 问题 | 答案 |
|---|---|
| 是否成功构建新的 D1A 子集 | 是 |
| 新子集路径 | `G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1` |
| 为什么比 cms1000 更合适 | 多 sequence、range/azimuth/class/target count 覆盖更丰富 |
| 是否建议进入 D1A | 建议，只做 sanity |
| 如果仍然不适合怎么办 | 先检查 D1A mask 投影；若 mask 不稳，再继续筛 sequence，不急着换数据集 |
