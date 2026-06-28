# D5I Kill Argument

**日期**: 2026-06-28  
**技能语义**: `/kill-argument`  
**对象**: D5I route decision  
**本地判定**: WARN but controllable  
**复核整合**: 独立 adversarial reviewer 指出两个关键修正：A-feasibility 不能只是并行项；B 必须降格为 protocol sanity check。

## 1. Strongest Rejection Memo

最强反对意见是：如果 D5I 把 Route B controlled synthetic RAD protocol 排在真实数据 feasibility 之前，它可能只是把真实数据标签不足的问题转移到 toy simulation。Synthetic GT 虽然干净，但它不能代表真实 FMCW 干扰、真实目标散射、真实天线阵列误差、真实 annotation noise，也不能证明 weak-target preservation 在外部数据上成立。Route A 才定义真实标签边界；若它只是“并行 review”，项目可能继续在自造任务里优化指标。Route D 的 negative-result 叙事也不能被无限延后，因为 D5H no-pass 已经是当前最诚实的项目结论。Route C 被降为 appendix 是合理的，但如果 RA calibration 仍参与解释链，就必须明确它只用于误差归因，不用于解锁训练。

## 2. Attack Points And Defense

| point | attack | severity | response | required fix |
|---|---|---|---|---|
| P1 | 合成协议不能承接核心结论 | critical | 成立。B 只能证明协议内一致性，不能证明真实 preservation。 | 将 B 明确降格为 protocol sanity check，并定义它能否产生 pass/fail 决策 |
| P2 | 外部可行性不应只是并行项 | major | 成立。真实标签边界必须先被写清楚。 | 将 A 排第一；本轮用 feasibility table 完成最小 A |
| P3 | D5H no-pass 没有被正面吸收 | major | 部分成立。D5I 必须把 no-pass 当作主前提。 | 在 D 中维护 failure ledger 和 forbidden claims |
| P4 | 负结果整理被不当延后 | major | 成立但可修。D 应立即作为报告骨架维护。 | 不等新实验才写 D；A/B 只作为补充证据 |
| P5 | RA calibration 的位置含混 | minor-major | 部分成立。C 只能用于误差归因。 | 明确 C 不解锁训练、D6 或 RA confirmed/invalid claim |
| P6 | 决策缺少停止条件 | critical | 成立。需要 route-level stop/go。 | 在 route comparison 和 next decision 中加入 A/B/D stop/go 条件 |

## 3. Net Assessment

D5I 决策能承受主要攻击，但必须改成更严格的表述：Route A 是第一优先级的 label/protocol feasibility；Route B 是 A-minimal table 之后的最小 unit test；Route D 立即维护 failure ledger；Route C 只做 diagnostic。最大未消除风险是 synthetic toy overclaim 和外部数据工程延迟。

## 4. Top Action Items

1. 在 README 和 D5I_NEXT_STEP_DECISION 中明确 “A first for label boundary; B next only because A-minimal feasibility table is now written”。
2. 把 `D5I_DATASET_FEASIBILITY_TABLE.csv` 作为 Route A 的保守证据，后续优先 RADIal small-subset reader design。
3. 在 D5J 开始前写 protocol diagram 和 stop/go gates，先验证 metric chain，再讨论模型。
