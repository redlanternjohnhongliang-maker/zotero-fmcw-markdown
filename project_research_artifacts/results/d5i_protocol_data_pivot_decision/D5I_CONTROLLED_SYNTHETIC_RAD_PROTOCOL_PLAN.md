# D5I Controlled Synthetic RAD Protocol Plan

**路线**: Route B  
**状态**: GO for protocol unit test only, after Route A minimal feasibility table  
**禁止**: 不训练模型，不进入 D6，不写真实世界性能，不修改 detector/fixed-PFA 主协议。

## 1. 目的

构造一个小型、完全可控的 synthetic RAD 场景，用来验证 fixed-PFA weak-target metric chain 是否能闭环。它回答的是“协议能不能测”，不是“方法在真实数据上有没有效果”。D5I 已先完成外部数据集 feasibility 表；本文件只定义下一步可执行的 unit test。

## 2. 必须具备的 GT

| GT | 要求 |
|---|---|
| range | 每个 target 的 true range bin 和连续物理 range |
| Doppler | 每个 target 的 true Doppler bin / radial velocity |
| azimuth | 每个 target 的 true azimuth bin / angle |
| amplitude | weak / mid / strong 三档 target amplitude |
| interference | 可控 SIR、可控 overlap、可控干扰形态 |
| clean/interfered pairing | 同一 target scene 的 clean RAD 与 interfered RAD |
| background | 可生成 known background/noise cells |
| false alarm budget | 用 background distribution 校准 fixed PFA |

## 3. 最小场景设计

| scene group | 内容 | 用途 |
|---|---|---|
| S0 clean no target | noise/background only | 估计 PFA threshold 和 false alarm budget |
| S1 clean isolated target | weak/mid/strong separated | 验证 target mask 与 PD 计算 |
| S2 interfered isolated target | 不同 SIR | 验证干扰导致 weak target miss |
| S3 overlap target | weak target 近邻 strong target | 验证 weak preservation 不被 strong target 代替 |
| S4 clean no-harm | clean 输入经过任何处理仍不伤害 target | 后续方法前置 gate |

## 4. 指标链

1. 用 background cells 在 fixed PFA = `1e-2` 和 `1e-3` 下校准阈值。
2. 用 true target masks 计算 weak/mid/strong PD。
3. 记录 measured PFA、false alarm count、target hit/miss count。
4. 对 overlap subset 单独计算 weak PD。
5. 对 clean no-harm subset 计算 clean target miss 增量。
6. 输出每个 cell 的 label provenance：`true_synthetic_gt`，避免和 Gao77 proxy 混淆。

## 5. Pass Gate

协议单元测试通过需要满足：

- PFA 校准误差在预设 tolerance 内；
- weak/mid/strong target 分层能稳定区分；
- overlap 场景中 weak target mask 不被 strong target mask 覆盖；
- clean no-harm 可以定义并能输出；
- 每个指标都能追溯到 true synthetic GT；
- 所有输出显式标注 synthetic/protocol sanity。

## 6. 不允许的写法

- 不写 “proves real-world FMCW interference mitigation”。
- 不写 “confirmed RD/RA/RAD performance”。
- 不写 “synthetic result validates Gao77”。
- 不把 synthetic target 简化成只在 range 维度可见。
- 不把 toy 成功当作训练或 D6 许可。

## 7. 推荐文件输出

下一步 D5J 可输出：

- `D5J_SYNTHETIC_RAD_CONFIG.json`
- `d5j_synthetic_rad_scene_manifest.csv`
- `d5j_fixed_pfa_metric_chain.csv`
- `d5j_weak_target_hit_table.csv`
- `D5J_SYNTHETIC_RAD_PROTOCOL_UNIT_TEST.md`
- `D5J_GO_NOGO_DECISION.md`

## 8. D5I 对 Route B 的判定

**GO**。这是当前最小、最干净、最不容易引入外部工程风险的一步。但它只允许作为 protocol unit test，不允许作为真实世界性能或 D6 依据。

如果该 unit test 不能输出 measured PFA、weak/mid/strong PD、weak hit/miss、overlap weak PD 和 clean no-harm，则应 STOP 并转 Route D 负结果整理。
