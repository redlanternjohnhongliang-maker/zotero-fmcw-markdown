# D5I Literature And Dataset Review

**日期**: 2026-06-28  
**任务**: D5H-Exec no-pass 后的 protocol/data pivot 文献与数据集复核  
**结论级别**: conservative / conference-ready  
**边界**: 本轮没有训练、没有进入 D6、没有下载新数据集、没有修改 detector 或 fixed-PFA 主协议。

## 1. 当前项目证据

D5H-Exec 已经给出最关键的前提：当前 Gao77 路线没有任何 representation 获得 `pass`。

| 类别 | representation |
|---|---|
| `proxy-only` | `range_only`, `corrected_RD`, `corrected_RA`, `STFT_spectrogram`, `complex_IQ`, `complex_RD`, `raw_ADC`, `radar_point_cloud` |
| `insufficient-labels` | `RAD`, `temporal_RD`, `temporal_RA`, `temporal_RAD`, `raw_ADC_learnable_FFT` |
| `pass` | 无 |

这说明当前失败不应被写成“模型太小”或“range-only 唯一失败原因”。更稳的解释是：label/proxy protocol、fixed-PFA 下的 saturation、weak_n、RA calibration、RAD/temporal label 缺失共同限制了当前 claim。

## 2. 本地文献证据

本地 Zotero Markdown 中已有材料支持以下判断：

- 接收端干扰抑制文献常使用 time-domain、STFT、RD map、complex RD 或 raw ADC 作为输入，但很多评价依赖 clean/interfered pairing 或 clean peak proxy，不能自动等价于真实 RD/RA/RAD GT。
- detector-less PD/PFA 或 RD-domain PDF 评价方法说明：固定 PFA 的 operating point 本身是合理的，问题不是要改 fixed-PFA，而是需要更可信的 target/background mask 和 label provenance。
- 多通道 MIMO 干扰抑制工作说明 raw ADC / multi-channel / RAD pipeline 在科学上有价值，但通常需要充足硬件参数、真实或可控的标签、以及较大工程成本。

关键本地文件：

- `papers_zotero_markdown/04_任务保持与感知保护/GKYPUWVQ.md`
- `papers_zotero_markdown/05_泛化安全与可靠性/FDBGFCJ9.md`
- `papers_zotero_markdown/03_接收端抑制与信号恢复/5G9DLYBJ.md`
- `papers_zotero_markdown/03_接收端抑制与信号恢复/JD4AG48A.md`
- `papers_zotero_markdown/01_干扰机理建模与数据/Q3E96J2V.md`

## 3. 外部数据集复核

本轮只做资料读取，不下载数据集。

| 数据集 | 主要价值 | 对 D5I 的限制 |
|---|---|---|
| RADIal | 官方说明提供 raw ADC、SignalProcessing 库，可生成 power spectra、point cloud、Range-Azimuth map；车辆标签含 `radar_R_m`, `radar_A_deg`, `radar_D`, `radar_P_db`。 | 没有直接 clean/interfered pairing；需要 synthetic interference injection；下载与预处理成本较高。 |
| RADDet | 官方说明提供 RAD tensor `(256,256,64)`、3D boxes、cartesian boxes、多类 road-user labels，并有额外 ADC 数据入口。 | gt/ADC 体量很大；auto-annotation 和 stationary capture 需要谨慎；没有天然干扰配对。 |
| CARRADA | 官方说明提供 camera images、raw radar data、generated annotations，另包 RAD tensors；论文定位为 Range-Angle-Doppler annotations。 | RAD tensor 包很大；半自动 annotation pipeline 不等于真实干扰恢复 GT；没有 clean/interfered pairing。 |
| Gao77 local | 当前已有 raw ADC 和本地脚本，最便宜。 | D5H 已确认 Doppler/RAD/track labels 不足，RA calibration 未通过；只能 diagnostic，不能主结果。 |
| RadarScenes / View-of-Delft / Astyx / RADIATE / Oxford Radar RobotCar | 可作为雷达 perception/annotation 参考。 | 多为 point cloud、polar scan、3D detection 或 adverse-weather perception，不直接解决 FMCW weak-target clean/interfered fixed-PFA preservation。 |

## 4. 外部来源

- CARRADA official GitHub: https://github.com/valeoai/carrada_dataset
- CARRADA arXiv: https://arxiv.org/abs/2005.01456
- RADDet official GitHub: https://github.com/ZhangAoCanada/RADDet
- RADDet arXiv: https://arxiv.org/abs/2105.00363
- RADIal official GitHub: https://github.com/valeoai/RADIal
- RADIal CVPR paper page: https://openaccess.thecvf.com/content/CVPR2022/html/Rebut_Raw_High-Definition_Radar_for_Multi-Task_Learning_CVPR_2022_paper.html
- Oxford Radar RobotCar arXiv: https://arxiv.org/abs/1909.01300

Semantic Scholar API 本轮返回 HTTP 429，因此没有把 S2 metadata 当作主要证据；arXiv helper 成功返回 CARRADA、RADDet、Oxford Radar RobotCar、RaDelft 等结构化条目。

## 5. D5I 文献结论

最稳的路线不是“马上换数据集训练”，也不是“继续修 Gao77 RA 后进入模型 sanity”。外部数据集确实说明 label-valid RAD/RD/RA protocol 是可行方向，尤其 RADIal、RADDet、CARRADA 值得保留；但它们都不能直接给出当前任务所需的 clean/interfered weak-target preservation 证据。

因此，D5I 的保守顺序应写成：**先完成 Route A 的外部数据集 label/protocol feasibility，作为真实标签边界；再执行 Route B 的 controlled synthetic RAD protocol sanity，作为 metric-chain unit test**。本目录已经用 `D5I_DATASET_FEASIBILITY_TABLE.csv` 完成 A 的最小 feasibility 表，所以 D5I 之后的最小可执行动作可以是 B，但 B 只能验证协议链条，不能替代真实数据证据。
