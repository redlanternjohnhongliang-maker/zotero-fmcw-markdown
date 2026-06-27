# REFINEMENT_REPORT

**日期**：2026-06-25  
**问题**：固定虚警率约束下的弱目标保护型 FMCW/4D 雷达干扰抑制训练  
**最终状态**：REVISE / kill-test  
**轮次**：1 次收窄，不进行多轮大论文 refine

## Output Files

- `refine-logs/FINAL_PROPOSAL.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `refine-logs/GO_NOGO_CHECKLIST.md`
- `refine-logs/PIPELINE_SUMMARY.md`
- `refine-logs/REVIEW_SUMMARY.md`

## Method Evolution Highlights

1. 从“weak-target-weighted differentiable CFAR loss”收窄为“fixed-PFA weak-target no-harm training protocol”。
2. 明确不声称新 detector、新 CFAR、新 backbone 或 safety guarantee。
3. 第一阶段只用 AENN/simple FCN，避免 RDLR-Net/DiffRIM/RIMformer 淹没 loss 贡献。
4. 实验从完整论文计划压缩为两周 kill-test。

## Remaining Weaknesses

- 贡献仍有被认为是 loss weighting trick 的风险；
- 弱目标定义可能被质疑为后验构造；
- 如果没有真实或半真实数据，期刊论文说服力有限；
- clean identity 是否改善检测而不只是改善 MSE，需要实验验证。

## Next Step

执行 kill-test 第一周实验表。只有通过 Go checklist 后，才进入完整论文计划或 `/run-experiment` 长周期执行。

