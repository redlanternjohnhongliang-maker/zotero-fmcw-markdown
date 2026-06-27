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
| R003C | D1B | Gao77 synthetic interference sanity | raw ADC synthetic FMCW-like interference + range-only fixed-PFA eval | val / test | achieved SIR, Protocol A/B, weak/mid/strong Pd, PFA, noise floor, non-overlap stats | DONE | D1B 通过；SIR 精确可控；Protocol B default mask PFA=1e-2 下 weak Pd clean→light→medium→severe 为 0.4266→0.3795→0.1629→0.0000；light 噪声地板上升较轻微；未训练 |
| R004 | D2A | small model overfit sanity | simple FCN range-only | tiny train / small subset / fixed-PFA eval | loss drop, MSE, clean no-harm, fixed-PFA metrics | DONE | D2A 通过；tiny loss 0.3037→0.0014，small val loss 0.1971→0.0053；val MSE interfered 3.7046→model 0.0998；clean no-harm 未明显失败；未进入 D3 |
| R005 | D3 | reconstruction baseline | MSE/MAGMSE | train/val/test | MSE, SINR, CFAR F1, Pd@PFA | DONE | MSE baseline 训练成功；tiny loss 0.2430→0.0033，val loss 0.0111→0.0028；medium/default/PFA=1e-2 下 weak Pd=0.3626，clean no-harm 正常 |
| R006 | D3 | main baseline | ordinary diff-CA-CFAR BCE | train/val/test | weak/mid/strong Pd, FAR, F1 | FAILED | ordinary BCE 训练和 fixed-PFA evaluation 可跑，检测指标不差于 MSE；但 clean-input no-harm 与幅度重建稳定性失败，model(clean) MSE≈96.65，暂不进入 D4 |
| R006A | D3-RCA | ordinary BCE failure root-cause analysis | pure BCE / temperature / LR / reconstruction-anchor diagnosis | small train/val/test | numeric domain, mask/label, diff-CFAR stability, clean no-harm, weak Pd | DONE | 未发现数值域或 mask/label bug；pure BCE 学到 detection-shaping；lambda_rec=1.0 诊断上把 model(clean) MSE 降到 0.1062，建议先重跑修正 D3，不进入 D4 |
| R006B | D3-Rerun | corrected baseline sanity | MSE / pure BCE failure control / BCE+rec | train/val/test | fixed-PFA weak Pd, clean no-harm, MSE, target peak bias | DONE | D3-Rerun 通过；pure BCE 复现 detection-shaping；best lambda_rec=0.5，weak Pd=0.3817 vs MSE=0.3702，model(clean) MSE=0.0490 vs pure BCE=53.1977；可以进入 D4 强 baseline |
| R007 | D4 | strong baseline tuning | balanced BCE or focal loss sweep | train/val/test | weak Pd@PFA, FAR, F1 | DONE | D4 通过；balanced_mild 为 best strong baseline，weak Pd=0.3817、F1=0.1369、model(clean) MSE≈0.0450；略强于 BCE+rec anchor，D5 必须以 balanced_mild 为主对照 |
| R008 | D5 | weak-target loss | weak-target-weighted detection loss | train/val/test | weak Pd@PFA, miss, FAR | DONE | D5 原始 sanity 通过；best=`weak_peak_w2p0`，medium/default/PFA=1e-2 下 weak Pd=0.3855，略高于 D4 `balanced_mild`=0.3817；但后续 R008A 显示提升只多 hit 1 个 weak target，不能直接进入 D6 |
| R008A | D5-check | improvement significance | balanced_mild vs weak_peak_w2p0 | same split 3 seeds + alternate split mini-check | hit-count delta, weak Pd mean/std, mask/scope/PFA robustness | DONE | 不建议进入 D6；原始提升仅 +1 weak hit；3 seeds 平均 weak Pd gain=-0.0076，D5 std=0.0172，提升不大于随机波动；narrow/non-overlap/PFA=1e-3 不稳定；clean no-harm 正常 |
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
