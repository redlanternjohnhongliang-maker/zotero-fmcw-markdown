# D0 Gao 77GHz 数据接入与子集审计报告

生成时间：2026-06-26 15:15  
阶段：D0 数据接入与子集审计  
数据根目录：`G:\mineru_output\gao_77ghz_raw_adc`

## 1. 执行边界

本次只确认 Gao 77GHz Raw ADC 数据是否能进入 D1 fixed-PFA sanity。

本次没有执行：

- D1-D14；
- 模型训练；
- synthetic interference injection；
- CFAR；
- fixed-PFA threshold calibration；
- CARRADA / RADIal / ARIM-v2 下载；
- RDLR-Net / DiffRIM / RIMformer 引入；
- 大规模预处理缓存；
- 全量数据复制到 subset。

## 2. 数据包检查

| 项目 | 结果 |
|---|---|
| 是否找到 `Automotive.zip` | 是 |
| 数据包路径 | `G:\mineru_output\gao_77ghz_raw_adc\Automotive.zip` |
| 备注 | 用户手动放在数据根目录，不在 `downloads` 目录 |
| 数据包大小 | 14.713 GB |
| 文件字节数 | 15,798,165,115 |
| 是否像 HTML 小文件 | 否 |
| zip 是否可读 | 是 |
| zip CRC 检查 | 通过，`testzip_first_bad_file = null` |
| zip entry 数量 | 59,351 |

官方 DataPort 页面标称 `Automotive.zip` 为 14.71 GB，本地文件大小与其一致。

## 3. 解压与 sequence 选择

为避免不必要地全量解压 14.7 GB 数据包，本次只解压 D0 审计所需的一个 sequence 的 `radar_raw_frame` 和 `text_labels`，没有解压 `images_0`，也没有展开其它 sequence。

| 项目 | 结果 |
|---|---|
| 是否成功解压 | 是，选择性解压 |
| 解压后根目录 | `G:\mineru_output\gao_77ghz_raw_adc\raw` |
| zip 内发现 sequence 数量 | 22 |
| 优先候选 `2019_04_09_bms1000` | radar 897，label 895，存在缺失 |
| 优先候选 `2019_04_09_cms1000` | radar 898，label 898 |
| 最终选中 sequence | `2019_04_09_cms1000` |
| 解压内容 | `radar_raw_frame`、`text_labels` |
| 未解压内容 | `images_0` 和其它 sequence |

选中 `2019_04_09_cms1000` 的原因：它比 `2019_04_09_bms1000` 对齐更干净，更适合 D0 / D1 前的基础数据链路检查。

## 4. 小子集

| 项目 | 结果 |
|---|---|
| 子集路径 | `G:\mineru_output\gao_77ghz_raw_adc\subset\Automotive\2019_04_09_cms1000` |
| 子集帧数 | 896 |
| 子集 radar 文件数 | 896 |
| 子集 label 文件数 | 896 |
| 是否复制 images | 否 |
| 是否复制全量数据 | 否 |

原始解压出的 `2019_04_09_cms1000` 中：

- radar 编号范围：`000002.mat` 到 `000899.mat`
- label 编号范围：`0000000000.csv` 到 `0000000897.csv`
- 按数值编号真正对齐的是 2 到 897，共 896 帧
- radar-only：898, 899
- label-only：0, 1

因此 subset 只保留数值编号 2 到 897 的 radar-label 对齐帧。

## 5. `.mat` 文件检查

随机读取 5 个 `.mat` 文件，变量名和 shape 一致。

| 文件 | 变量名 | raw ADC shape | dtype | 是否复数 |
|---|---|---|---|---|
| `000881.mat` | `adcData` | `[128, 255, 4, 2]` | `complex128` | 是 |
| `000592.mat` | `adcData` | `[128, 255, 4, 2]` | `complex128` | 是 |
| `000107.mat` | `adcData` | `[128, 255, 4, 2]` | `complex128` | 是 |
| `000025.mat` | `adcData` | `[128, 255, 4, 2]` | `complex128` | 是 |
| `000011.mat` | `adcData` | `[128, 255, 4, 2]` | `complex128` | 是 |

README 期望 shape：

- samples = 128
- chirps = 255
- receivers = 4
- transmitters = 2

检查结果：符合 README 描述。

## 6. Label 文件检查

标签文件无 header，每行 6 列，格式为：

`uid, class, px, py, wid, len`

随机读取样例：

| 文件 | 非空行数 | 示例 |
|---|---:|---|
| `0000000695.csv` | 1 | `17,2,0.16145913,9.27109757,4.5,1.8` |
| `0000000093.csv` | 1 | `17,2,4.91319049,8.94748217,4.5,1.8` |
| `0000000792.csv` | 1 | `17,2,-0.53904314,9.29400938,4.5,1.8` |
| `0000000402.csv` | 1 | `17,2,3.02168526,9.08399518,4.5,1.8` |
| `0000000110.csv` | 1 | `17,2,4.87477855,8.9638635,4.5,1.8` |

类别统计：

| class id | 类别 | 数量 |
|---:|---|---:|
| 2 | car | 895 |

其它检查：

| 项目 | 结果 |
|---|---|
| 空标签帧数量 | 1 |
| 标签总行数 | 895 |
| 列数异常文件数 | 0 |
| `px` 范围 | -1.42410014 到 4.94858847 |
| `py` 范围 | 8.92818955 到 9.60894922 |
| `wid` 范围 | 4.5 到 4.5 |
| `len` 范围 | 1.8 到 1.8 |
| `px` 超出 README 合理范围数量 | 0 |
| `py` 超出 README 合理范围数量 | 0 |
| `wid` 或 `len` 非正数量 | 0 |

## 7. Radar Processing Smoke Test

本次只做最小 smoke test，没有做 CFAR 或 fixed-PFA。

处理步骤：

1. 读取 `adcData`；
2. 确认为 `samples × chirps × receivers × transmitters`；
3. 将 TDM 维度整理为虚拟阵列：`samples × chirps × 8`；
4. 对 samples 维做 range FFT；
5. 对 chirps 维做简单 Doppler FFT；
6. 对虚拟阵列通道求幅度平均，得到 RD map；
7. 保存 range profile、RD map 和粗略 range-only label projection。

检查文件：

| mat 文件 | label 文件 | virtual array shape | range profile shape | RD map shape | label 数 |
|---|---|---|---|---|---:|
| `000002.mat` | `0000000002.csv` | `[128, 255, 8]` | `[128]` | `[128, 255]` | 1 |
| `000226.mat` | `0000000226.csv` | `[128, 255, 8]` | `[128]` | `[128, 255]` | 1 |
| `000450.mat` | `0000000450.csv` | `[128, 255, 8]` | `[128]` | `[128, 255]` | 1 |
| `000674.mat` | `0000000674.csv` | `[128, 255, 8]` | `[128]` | `[128, 255]` | 1 |
| `000897.mat` | `0000000897.csv` | `[128, 255, 8]` | `[128]` | `[128, 255]` | 1 |

Smoke test 结果：

| 项目 | 结果 |
|---|---|
| range FFT 是否成功 | 是 |
| Doppler FFT 是否成功 | 是 |
| RD 图是否非空 | 是 |
| label 粗投影是否生成 | 是 |

图像目录：

`G:\mineru_output\gao_77ghz_raw_adc\reports\figures`

代表性图像：

- `G:\mineru_output\gao_77ghz_raw_adc\reports\figures\range_profile_000450.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\figures\rd_map_000450.png`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\figures\label_projection_range_only_000450.png`

补充 JSON：

- `G:\mineru_output\gao_77ghz_raw_adc\reports\d0_integrity_summary.json`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\d0_smoke_test_summary.json`

## 8. 当前是否足够进入 D1

结论：建议进入 D1 fixed-PFA sanity 的数据读取与基础处理阶段。

理由：

1. 官方数据包大小正确，zip 可读；
2. 已有一个干净对齐的小子集；
3. `.mat` 可读取；
4. raw ADC shape 与 README 一致；
5. `.csv` label 可读取；
6. range FFT / Doppler FFT 链路可以跑通；
7. RD map 可生成且非空。

需要注意的限制：

1. 当前只接入了一个 car sequence，类别和目标强度多样性很弱；
2. label 是物理坐标框，不是直接 RD/RDA cell mask；
3. D1 需要先实现并人工检查 label 到 range/RD 或 range-angle 区域的粗投影；
4. 弱/中/强目标划分不能只依赖这个单一 sequence 得出研究结论；
5. 这个 subset 适合做 D1 sanity，不适合直接做论文级实验。

## 9. 下一步建议

D1 可以继续，但第一步建议只做数据版 sanity：

1. 用当前 subset 读取 `adcData`；
2. 生成 RD 或 RDA 表示；
3. 根据 label 的 `px, py, wid, len` 生成粗 target mask；
4. 可视化检查 target mask 是否落在合理 range/angle 区域；
5. 再进入 D1 中的 fixed-PFA / target-background mask sanity。

不要直接进入训练。D1 仍然应该只做 sanity。

## 10. 简短结论

| 问题 | 答案 |
|---|---|
| Gao 77GHz 数据是否可读 | 是 |
| 小子集在哪里 | `G:\mineru_output\gao_77ghz_raw_adc\subset\Automotive\2019_04_09_cms1000` |
| raw ADC shape 是否正确 | 是，`adcData = [128, 255, 4, 2]` |
| label 是否可用 | 是，格式为 `uid, class, px, py, wid, len` |
| range/RD smoke test 是否成功 | 是 |
| 是否建议进入 D1 fixed-PFA sanity | 建议进入，但只进入 D1 sanity，不训练模型 |
