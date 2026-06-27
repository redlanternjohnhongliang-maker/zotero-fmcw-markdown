# Project Research Artifacts

这里存放当前 FMCW fixed-PFA weak-target preservation 项目中适合继续阅读和复核的材料。它不是完整数据集，也不是可直接复现实验环境，而是给 GPT 或研究者快速接手用的轻量归档。

## 内容

| 路径 | 内容 |
| --- | --- |
| `research_overview/` | 研究日志、idea/refine 记录、风险审稿和阶段性总结。 |
| `results/` | D5 系列诊断和 D5H-Exec 的 CSV、JSON、Markdown 结果。 |
| `experiment_scripts/` | 当前 `G:\mineru_output\experiments` 下的实验脚本快照。 |
| `figures/reports/` | Gao77 相关报告图、诊断图和 D5H sanity figures。 |
| `audit_traces/` | `experiment-audit` 与 `result-to-claim` 的审计 trace 快照。 |

## 关键阅读入口

1. `results/d5h_representation_protocol_audit_executed/D5H_EXECUTED_SUMMARY.md`
2. `results/d5h_representation_protocol_audit_executed/D5H_EXECUTED_DECISION.md`
3. `results/d5h_representation_protocol_audit_executed/EXPERIMENT_AUDIT.md`
4. `results/d5h_representation_protocol_audit_executed/RESULT_TO_CLAIM.md`
5. `research_overview/EXPERIMENT_LOG.md`
6. `experiment_scripts/d5h_representation_protocol_audit_executed.py`

## D5H-Exec 摘要

D5H-Exec 只做 no-training/minimal-computation audit，没有训练模型，没有进入 D6，没有加入 false alarm penalty，也没有继续 weak weighting。

| representation | label | 主要原因 |
| --- | --- | --- |
| `range_only` | `proxy-only` | 只能作为 reference，不能证明改进。 |
| `corrected_RD` | `proxy-only` | 依赖 Doppler proxy，D5E weak_n 小于 100，且主 PFA 下 baseline 饱和。 |
| `corrected_RA` | `proxy-only` | RA calibration 未解决，弱目标命中仍不可靠。 |
| `RAD` | `insufficient-labels` | Gao77 当前没有 true RAD boxes。 |
| `temporal_RD` | `insufficient-labels` | 没有 track IDs。 |
| `temporal_RA` | `insufficient-labels` | 没有 tracks，RA calibration 也未通过。 |
| `temporal_RAD` | `insufficient-labels` | RAD 和 temporal labels 都缺失。 |
| `STFT_spectrogram` | `proxy-only` | 可作信号诊断，但目标标签仍是 projection proxy。 |
| `complex_IQ` | `proxy-only` | raw complex ADC 存在，但 target/background label 仍是 proxy。 |
| `complex_RD` | `proxy-only` | RD label 限制仍在，phase 不解决 label validity。 |
| `raw_ADC` | `proxy-only` | 只做 memory/availability audit，目标定义仍依赖投影。 |
| `raw_ADC_learnable_FFT` | `insufficient-labels` | learnable FFT 涉及训练，D5H 禁止。 |
| `radar_point_cloud` | `proxy-only` | 点云生成前弱目标可能已丢失，只适合作辅助路线。 |

## 不要误读

- 不能把 RD/RA/RAD proxy 写成 confirmed performance。
- 不能把 RA inconclusive 写成 angle 无效。
- 不能把 input representation 写成唯一失败原因。
- 不能把当前结果当成训练有效性证据。
- 不能进入 D6 或继续 weak weighting。

## 下一步方向

当前最合理的 pivot 是先解决 label/protocol，而不是换大模型。候选方向包括：

- 寻找或构造具备 true Doppler、RAD boxes、track IDs、calibrated azimuth 的评估协议。
- 把 synthetic protocol 明确写成 protocol sanity，不冒充真实物理干扰性能。
- 重审 fixed-PFA 与 weak-target definition，避免 baseline saturation 和 proxy leakage。
- 从论文库中重点检索弱目标保持、任务保持、真实标注、雷达干扰评估协议相关工作。

## 边界

这里没有上传原始 `.mat` 数据、PDF、数据库、模型权重或完整训练输出。脚本是快照，复现时需要回到本地数据环境补齐路径和依赖。
