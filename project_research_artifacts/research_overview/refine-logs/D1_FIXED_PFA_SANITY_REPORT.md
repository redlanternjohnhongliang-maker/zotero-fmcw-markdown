# D1_FIXED_PFA_SANITY_REPORT

**状态**：D1 sanity 已完成；未进入 D2。

## 数据来源

- 当前未发现本地真实数值雷达 tensor 数据。
- 本报告使用合成 toy RD 数据验证 D1 指标链路。
- 这不是方法效果结论，不能作为论文实验结果。

## 已打通模块

- 数据读取/生成：完成，synthetic RD maps。
- hard CA-CFAR score：完成。
- differentiable CA-CFAR：完成，dry-run 可反传。
- target mask / background mask：完成。
- weak / mid / strong target split：完成，当前按 target peak amplitude percentile。
- cell-level PFA：完成。
- fixed-PFA threshold calibration：完成，validation set 标定，test set 报告。

## Tensor 与 Mask

- clean shape：`(48, 64, 128)`
- interfered shape：`(48, 64, 128)`
- dtype：`float32`
- targets total：160
- generator strength counts：`{'weak': 51, 'strong': 60, 'mid': 49}`
- target mask cells：1440
- background mask cells：380371

## Fixed-PFA No-Mitigation Metrics

| target PFA | threshold | test FAR | weak n | weak Pd | weak miss | mid n | mid Pd | strong n | strong Pd | cell F1 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.01 | 4.7045 | 0.01012 | 28 | 0.6786 | 0.3214 | 27 | 0.9630 | 28 | 1.0000 | 0.3118 |
| 0.001 | 7.2904 | 0.00096 | 28 | 0.3214 | 0.6786 | 27 | 0.7778 | 28 | 0.9643 | 0.5412 |

## 输出文件

- `results/d1_sanity/preflight.json`
- `results/d1_sanity/d1_metrics.json`
- `results/d1_sanity/d1_metrics.csv`

## D1 结论

- D1 指标链路可以在本地完成。
- 下一步若继续 D2，建议使用 `G:/Anaconda/envs/cnn_learn/python.exe`，batch size 从 1 或 2 开始。
- 真实数据接入仍是后续瓶颈；当前只是 sanity，不代表真实雷达数据表现。
