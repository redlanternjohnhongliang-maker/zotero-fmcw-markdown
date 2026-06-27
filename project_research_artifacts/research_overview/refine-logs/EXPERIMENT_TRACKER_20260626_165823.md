# EXPERIMENT_TRACKER：最小两周 Kill-Test

**日期**：2026-06-25  
**状态说明**：TODO / RUNNING / DONE / FAILED / KILLED  
**原则**：只跑第一阶段 kill-test 必要实验；不跑 random/strong weights、OS/GO-CFAR、RDLR-Net、DiffRIM、RIMformer。

| Run ID | Day | Purpose | System / Variant | Split | Primary Metrics | Status | Notes |
|---|---|---|---|---|---|---|---|
| R001 | D1 | 数据与 mask sanity | synthetic toy RD, no mitigation | train/val | weak/mid/strong counts, target/background mask | DONE | 真实雷达 tensor 未找到；合成数据 mask 链路已通 |
| R002 | D1 | CA-CFAR sanity | CA-CFAR + clean/interfered RD | val/test | cell-level PFA, Pd, FAR | DONE | validation threshold 已标定 PFA=1e-2/1e-3 |
| R003 | D1 | differentiable CA-CFAR sanity | diff-CA-CFAR layer | tiny batch | differentiable output, gradients | DONE | CUDA dry-run batch=2 可反传 |
| R003A | D1A | Gao77 clean sanity | range-only clean map + objectness mask + CA-CFAR | train placeholder / val / test | projection hit rate, weak/mid/strong Pd, fixed-PFA PFA/F1 | DONE | 真实 Gao77 子集通过；projection hit rate=0.9878；PFA 1e-2→0.0106，1e-3→0.0012；未训练 |
| R003B | D1A+ | Gao77 mask stress test | range-only mask width / guard sensitivity / RA projection sanity | val / test | mask width sensitivity, overlap, guard sensitivity, PFA stability, RA projection | DONE | 默认 mask 偏宽且 weak Pd/F1 对宽度敏感；overlap 较重；guard/PFA 整体稳定；RA hit=0.8763；建议 D1B 先 range-only，保留 narrow/default 双口径；未训练 |
| R004 | D2 | backbone overfit | AENN or simple FCN | tiny train | loss, CFAR F1 | TODO | AENN 不通立即切 simple FCN |
| R005 | D3 | reconstruction baseline | MSE/MAGMSE | train/val/test | MSE, SINR, CFAR F1, Pd@PFA | TODO | 辅助 baseline |
| R006 | D3 | main baseline | ordinary diff-CA-CFAR BCE | train/val/test | weak/mid/strong Pd, FAR, F1 | TODO | 主对照 |
| R007 | D4 | strong baseline tuning | balanced BCE or focal loss sweep | train/val/test | weak Pd@PFA, FAR, F1 | TODO | 给合理调参预算 |
| R008 | D5 | weak-target loss | weak-target-weighted detection loss | train/val/test | weak Pd@PFA, miss, FAR | TODO | 对比 R006/R007 |
| R009 | D6 | false alarm control | weak-target loss + FA penalty | train/val/test | weak Pd@PFA, FAR | TODO | 检查提升是否靠虚警 |
| R010 | D7 | full loss and clean test | weak + FA + identity | train/val/test/clean | clean F1, FPR, Pd, SINR, SSIM | TODO | 第一周 Soft Go |
| R011 | D8-D9 | seed 1 core | ordinary BCE / best balanced-focal / full | test | weak Pd@PFA, FAR, clean | TODO | 3 seeds |
| R012 | D8-D9 | seed 2 core | ordinary BCE / best balanced-focal / full | test | weak Pd@PFA, FAR, clean | TODO | 3 seeds |
| R013 | D8-D9 | seed 3 core | ordinary BCE / best balanced-focal / full | test | weak Pd@PFA, FAR, clean | TODO | 3 seeds |
| R014 | D10 | weak definition A | CFAR-margin weak target | test | weak Pd, miss, FAR | TODO | 定义 A |
| R015 | D10 | weak definition B | low peak/SNR/RCS/percentile weak target | test | weak Pd, miss, FAR | TODO | 定义 B |
| R016 | D11 | clean no-harm | clean input through core models | clean test | CFAR F1, FPR, Pd, SINR, SSIM, amplitude bias | TODO | 必须不退化 |
| R017 | D12 | interference severity | light/medium/severe | test | weak Pd, FAR, miss | TODO | 三档干扰 |
| R018 | D13 | CFAR parameter robustness | changed threshold/window/guard | test | weak Pd, FAR, CFAR F1 | TODO | 不做 OS/GO-CFAR |
| R019 | D14 | final decision | aggregate results | all | Soft/Hard Go checklist | TODO | 输出 Go/No-Go |
