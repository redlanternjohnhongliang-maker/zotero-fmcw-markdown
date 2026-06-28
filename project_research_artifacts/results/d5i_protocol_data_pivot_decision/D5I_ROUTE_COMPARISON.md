# D5I Route Comparison

**目标**: 在 D5H-Exec no-pass 后决定下一步 protocol/data pivot。  
**总排序**: A > B > D > C。  
**执行注释**: A 的最小 feasibility 表已在本轮完成，因此 D5I 之后的最小可执行实验是 B；这不代表 synthetic 证据高于真实数据证据。

## 1. 排序表

| rank | route | feasibility | scientific value | engineering cost | label validity | risk | recommended action |
|---:|---|---|---|---|---|---|---|
| 1 | Route A: External labeled dataset pivot | 中 | 高 | 高 | 中到高，取决于数据集 | 下载/预处理/无干扰配对 | 先完成 feasibility table 和读取脚本设计，不下载、不训练 |
| 2 | Route B: Controlled synthetic RAD protocol sanity | 高 | 中高 | 低中 | 高，因为 GT 可控 | toy overclaim | 在 A-feasibility 后作为最小实验，只写 protocol unit test，不写真实世界性能 |
| 3 | Route D: Negative-result / limitation consolidation | 高 | 中 | 低 | 高，因为只陈述当前负证据 | reviewer 质疑贡献不足 | 作为报告/论文方向准备，但需补 external dataset table、classical baseline review、protocol diagram |
| 4 | Route C: Gao77 RA calibration RCA | 中 | 低中 | 低 | 低到中，修好也仍是 proxy | 被误读成 RA 有效或无效 | 只做 appendix/diagnostic，不允许主结果或 minimal model sanity |

## 2. Route A: External Labeled Dataset Pivot

**可行性**: 中。RADIal、RADDet、CARRADA 都有比 Gao77 更强的 radar label/tensor 支持，但直接接入成本高。

**科学价值**: 高。它可以回答 Gao77 无法回答的问题：true Doppler / RAD boxes / calibrated RA / raw ADC 到 dense tensor 的协议是否能支撑 weak-target preservation。

**工程成本**: 高。CARRADA RAD tensor、RADDet gt/ADC、RADIal raw ADC 都不是小体量；且需要重新做读取、对齐、干扰注入、固定 PFA 校准。

**label validity**: RADIal 最接近当前需要，因为标签中有 radar R/A/D/power；RADDet 有 RAD tensor boxes；CARRADA 有 RAD annotation views。三者都没有天然 clean/interfered pairing。

**风险**: 一旦直接训练，很容易把“外部 perception benchmark 表现”误写成“干扰抑制 weak-target preservation 表现”。

**建议**: 不下载数据，不训练。先保留为 D5I-A feasibility route；等 B 的 metric chain 证明可行后，再选 RADIal 或 RADDet 做小规模读取器。

## 3. Route B: Controlled Synthetic RAD Protocol Sanity

**可行性**: 高。可以用小型可控场景生成 true range / Doppler / azimuth GT，不依赖 Gao77 标签缺口。

**科学价值**: 中高。它不能证明真实世界性能，但能证明 fixed-PFA weak-target metric chain 是否自洽：weak/mid/strong targets、overlap、SIR、clean no-harm、known false alarm budget 都能闭环。

**工程成本**: 低中。先做 no-training protocol unit test，只生成 clean/interfered RAD cube、mask、threshold calibration、PD/PFA 计算。

**label validity**: 高，因为 GT 是生成器真值；但必须明确 synthetic scope。

**风险**: 最大风险是 toy overclaim。解决方式是文件标题、图注、结论都写成 protocol unit test，不写 real-world mitigation。

**建议**: 作为 D5I 后的最小下一步。

## 4. Route C: Gao77 RA Calibration RCA

**可行性**: 中。可以继续检查 px/py 到 azimuth、sign convention、degrees/radians、FFT axis、RX dimension、mask width、D1A+ vs D5C discrepancy。

**科学价值**: 低中。即使 RA calibration 修好，Gao77 仍没有 true Doppler、RAD boxes、temporal tracks，因此不会自动获得 `pass`。

**工程成本**: 低。

**label validity**: 中低。修好后最多把 RA 从“未校准 proxy”变成“校准较好的 proxy”，不是 true label。

**风险**: 容易被误写成“RA 已证明有效”或“RA 无效”。两者都不允许。

**建议**: 只作为 appendix/diagnostic；不允许由它进入 minimal model sanity。

## 5. Route D: Negative-Result Consolidation

**可行性**: 高。已有 D5B-D5H 证据链足够写成 conservative report。

**科学价值**: 中。它的价值不在“证明 weak weighting 无效”，而在证明 naive weak weighting + proxy labels + saturated fixed-PFA evaluation 会产生不可靠 claim。

**工程成本**: 低。

**label validity**: 高，只要严格陈述当前证据范围。

**风险**: reviewer 会质疑没有足够 positive result，或者 classical baselines / external datasets / protocol diagram 不够。

**建议**: 作为报告线并行整理；先补 external dataset feasibility table、classical baseline review、protocol diagram，再决定是否写短论文/技术报告。

## 6. Stop / Go 条件

| route | GO 条件 | STOP 条件 |
|---|---|---|
| A | 至少一个候选数据集能明确映射 range / azimuth / Doppler 或 RAD label 到 fixed-PFA mask，并能说明 clean/interfered pairing 缺口 | 无法定义 weak subset、background cells、或标签 provenance 不可审计 |
| B | synthetic GT 能稳定产生 range/Doppler/azimuth/magnitude/overlap/SIR/false-alarm budget，并跑通 PFA/PD metric chain | 只能产生 toy visualization，不能产生 measured PFA、weak hit/miss、clean no-harm |
| C | 仅用于解释 Gao77 RA discrepancy | 任何人试图用它解锁训练、D6 或 confirmed RA claim |
| D | A 或 B 无法给出可继续实验的 gate，或项目需要先冻结负结果 | 负结果被写成普遍理论结论或否定 RD/RA/RAD 本身 |

## 7. 总决策

下一步不是 D6，不是继续 weak weighting，也不是调更大模型。D5I 的决策顺序是：**Route A 先锁定外部数据集标签边界；Route B 再作为最小可执行 protocol unit test；Route D 立即维护负结果报告骨架；Route C 降级为 Gao77 诊断附录。**

由于 A 的最小 feasibility 表已经在本轮输出，D5I 后的下一步最小 prompt 可以执行 Route B。
