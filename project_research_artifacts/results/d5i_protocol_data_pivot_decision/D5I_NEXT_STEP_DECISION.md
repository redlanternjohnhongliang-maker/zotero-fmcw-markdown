# D5I Next Step Decision

**日期**: 2026-06-28  
**最终路线排序**: A > B > D > C  
**下一步最小动作**: D5J controlled synthetic RAD protocol unit test。  
**原因**: A 的最小 feasibility table 已在 D5I 输出；B 是其后的最小可执行 unit test，不是更高等级的真实证据。

## 1. Route Ranking

| rank | route | decision |
|---:|---|---|
| 1 | External labeled dataset pivot | GO for feasibility/design, no download now |
| 2 | Controlled synthetic RAD protocol sanity | GO after A-minimal table, protocol unit test only |
| 3 | Negative-result consolidation | GO as report/roadmap, not next experiment |
| 4 | Gao77 RA calibration RCA | diagnostic appendix only |

## 2. Go / No-Go

| item | verdict |
|---|---|
| 训练模型 | No |
| minimal model sanity | No now |
| D6 | No |
| weak weighting | No |
| false alarm penalty | No |
| detector/fixed-PFA 主协议修改 | No |
| Gao77 作为主结果 | No |
| Gao77 作为 diagnostic evidence | Yes |
| controlled synthetic RAD protocol | Yes |
| external dataset feasibility | Yes |
| 新数据集下载 | No |

## 3. Stop / Go 决策线

| 路线 | GO | STOP / 转向 |
|---|---|---|
| A external feasibility | RADIal/RADDet/CARRADA 至少能映射到可审计的 range/azimuth/Doppler/RAD 标签候选 | 如果 weak subset、background、PFA mask、label provenance 无法定义，禁止外部数据训练 |
| B synthetic protocol | 能输出 measured PFA、PD、weak hit/miss、overlap weak PD、clean no-harm | 如果只能画图或 toy demo，不能形成 pass/fail gate，转 D 写负结果 |
| D negative report | D5H no-pass、A/B stop 条件触发，或项目需要冻结阶段性结论 | 如果被写成普遍否定 weak weighting/RD/RA/RAD，则停止并降级 claim |
| C Gao77 RA RCA | 只用于定位 angle/projection bug | 如果被用来解锁训练或 confirmed RA claim，立即停止 |

## 4. 小白能懂的中文解释

现在的问题不是“再训练一下可能就好了”。更像是尺子还没有校准好：我们想测弱目标有没有被保护住，但当前 Gao77 的 Doppler、角度、RAD、轨迹标签都不够硬，有些只能算投影或 proxy。拿这把尺子继续训练，只会得到更难解释的数字。

所以本轮先把外部数据集的“真标签边界”列出来：哪些有 raw ADC，哪些有 RAD tensor，哪些有 Doppler/角度标签，哪些没有 clean/interfered pairing。这个 feasibility 表已经写完。下一步再做一个小的、完全可控的 synthetic RAD 测试。这个测试不是为了证明真实世界性能，而是为了证明我们的 fixed-PFA 弱目标评价链条能不能正常工作：目标在哪里、速度是多少、角度是多少、弱目标是否被打中、背景 false alarm 是否固定，这些都先在真值可控的环境里跑通。

## 5. 项目管理版结论

- D5H-Exec no-pass 保持不变。
- 当前禁止训练、D6、weak weighting、false alarm penalty、detector/fixed-PFA 主协议修改。
- D5I 决策完成：A-feasibility 排第一并已完成最小表；下一步进入 D5J controlled synthetic RAD protocol unit test。
- Route A 外部数据集暂不下载，但保留 RADIal/RADDet/CARRADA feasibility 表和后续 reader design。
- Route D 立即作为技术报告骨架维护。
- Route C 只作为 Gao77 RA 诊断附录。

## 6. Paper-Usable English Conservative Conclusion

The D5H-Exec no-training audit did not identify any representation that is eligible for training escalation under the current Gao77 protocol. The evidence points to a label/protocol bottleneck rather than a simple model-capacity bottleneck. We therefore pivot to a protocol-first path: external datasets such as RADIal, RADDet, and CARRADA are first assessed for label-valid future experiments, while a controlled synthetic RAD unit test is used only to validate the fixed-PFA weak-target metric chain with known range, Doppler, azimuth, target strength, overlap, and false-alarm budget. Neither path currently supports real-world mitigation claims or D6 escalation.

## 7. Next Smallest Prompt

```text
请使用 ARIS / Auto-claude-code-research-in-sleep 的 Codex CLI skill workflow 继续当前项目。

本次任务是 D5J: Controlled Synthetic RAD Protocol Unit Test after D5I.

严格限制：
1. 不训练模型；
2. 不进入 D6；
3. 不继续 weak weighting；
4. 不加入 false alarm penalty；
5. 不下载新数据集；
6. 不把 synthetic protocol 写成真实世界性能。

目标：
构造一个小型 controlled synthetic RAD scene generator，用 true range / Doppler / azimuth / amplitude / weak-mid-strong labels / overlap / SIR / clean-interfered pairing / known background false-alarm budget，验证 fixed-PFA weak-target metric chain。

输出目录：
G:\mineru_output\results\d5j_controlled_synthetic_rad_protocol_unit_test

至少输出：
1. D5J_SYNTHETIC_RAD_CONFIG.json
2. d5j_synthetic_rad_scene_manifest.csv
3. d5j_fixed_pfa_metric_chain.csv
4. d5j_weak_target_hit_table.csv
5. D5J_SYNTHETIC_RAD_PROTOCOL_UNIT_TEST.md
6. D5J_GO_NOGO_DECISION.md

最终必须回答：
- fixed-PFA calibration 是否可运行；
- weak/mid/strong target PD 是否可定义；
- overlap weak target 是否可独立评估；
- clean no-harm 是否可定义；
- 是否仍禁止训练和 D6；
- 下一步是否允许只做 external dataset reader feasibility。
```
