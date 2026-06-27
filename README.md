# Zotero FMCW Markdown Research Hub

这个仓库把当前 FMCW 雷达干扰抑制项目中适合 GPT 阅读的材料放在一起，核心用途是后续继续做综述、问题定位和研究方向发现。

## 目录

| 路径 | 内容 |
| --- | --- |
| `papers_zotero_markdown/` | 从 Zotero 论文 PDF 转换得到的 Markdown 论文语料，共 133 篇，按主题单独存放。 |
| `project_research_artifacts/` | 当前项目的研究日志、实验结果、审计记录、脚本快照和关键图表。 |

## 推荐阅读顺序

1. 先读 `project_research_artifacts/README.md`，了解当前项目进度和不能继续夸大的结论。
2. 再读 `project_research_artifacts/results/d5h_representation_protocol_audit_executed/D5H_EXECUTED_SUMMARY.md`。
3. 接着读 `project_research_artifacts/results/d5h_representation_protocol_audit_executed/RESULT_TO_CLAIM.md` 和 `EXPERIMENT_AUDIT.md`。
4. 然后按问题去 `papers_zotero_markdown/` 查论文，优先看接收端抑制、任务保持、泛化可靠性相关目录。

## 当前保守结论

D5H-Exec 是一次 no-training representation protocol audit。结论很保守：

- 没有任何 representation 获得 `pass`。
- `range_only`、`corrected_RD`、`corrected_RA`、`STFT_spectrogram`、`complex_IQ`、`complex_RD`、`raw_ADC`、`radar_point_cloud` 只能算 `proxy-only`。
- `RAD`、`temporal_RD`、`temporal_RA`、`temporal_RAD`、`raw_ADC_learnable_FFT` 是 `insufficient-labels`。
- 当前不允许 minimal model sanity、不继续 weak weighting、不进入 D6。
- 下一步应优先做标签/协议 pivot，而不是直接训练或扩大模型。

## 边界

这个仓库只上传轻量、可读、可复核的文本、表格、脚本和图表。没有上传原始 `.mat` 数据、PDF、Zotero 数据库、模型权重或训练产物。Markdown 可能包含论文全文，建议保持私有仓库。
