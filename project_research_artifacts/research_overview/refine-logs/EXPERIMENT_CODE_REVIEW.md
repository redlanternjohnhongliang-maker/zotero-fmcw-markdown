# EXPERIMENT_CODE_REVIEW

## D1B local-only code review — 2026-06-26

状态：`[local-only]`

本次 D1B 脚本审阅对象：

- `G:\mineru_output\experiments\d1b_gao77_synthetic_interference_sanity.py`

审阅结论：

- 未发现训练循环、optimizer、backbone、AENN / FCN / RDLR-Net / DiffRIM / RIMformer 引入。
- synthetic interference 在 raw ADC / IF 层注入，未直接在 range profile 上贴噪声。
- clean ADC 保留为 reference，interfered ADC 只在内存中用于 sanity 评估。
- narrow/default mask 均会输出，未只报告 default。
- Protocol A 使用 clean validation background threshold 固定评估 clean/interfered test。
- Protocol B 对每种输入类型和 SIR 在 validation background 上重新 fixed-PFA calibration。
- evaluation 使用 Gao77 标签生成的 target/background mask，未把另一个模型输出当 ground truth。
- 输出包含 CSV、JSON、图像和中文报告；报告明确 D1B 是 simplified synthetic FMCW-like sanity，不包装成方法效果。

非阻塞注意：

- 当前干扰模型是 first-order sanity model，不能代表完整真实互扰物理。
- severe SIR=-10 dB 可能过强；若 range profile 爆炸或 fixed-PFA 指标不可解释，应在报告中判定 D1B 未通过，而不是进入 D2。

## D2A local-only code review — 2026-06-26

状态：`[local-only]`

本次 D2A 脚本审阅对象：

- `G:\mineru_output\experiments\d2a_gao77_small_model_sanity.py`

审阅结论：

- 仅执行 D2A small model sanity，不包含 D3-D14 正式 baseline、focal / balanced BCE、weak-target full loss 或 3 seeds。
- 主模型为 `SimpleRangeFCN`，参数量小，输入输出均为 `batch x 1 x 128` range-only profile。
- 训练目标为 MSE reconstruction，加一个很小的 clean identity sanity loss；未包装成主贡献。
- train 使用 light + medium，test 使用 light + medium + severe；severe 只作为 stress test。
- fixed-PFA evaluation 复用 D1B 的 target/background mask、narrow/default、non-overlap-only、per-sequence 和 per-class-group 统计。
- evaluation 使用 Gao77 标签生成的 target/background mask，未把模型输出当 ground truth。
- 输出文件包含 CSV/JSON/图像/中文报告，便于 D3 前判断是否继续。

非阻塞注意：

- D2A 的 simple FCN 结果只能说明训练链路可跑，不应作为正式 baseline 或方法效果。
- 如果 model output 在 MSE 或 clean no-harm 上失败，应停止在 D2A，不进入 D3。

## D3 local-only code review — 2026-06-26

状态：`[local-only]`

本次 D3 脚本审阅对象：

- `G:\mineru_output\experiments\d3_gao77_baseline_sanity.py`

审阅结论：

- 仅执行 D3 Gao77 range-only baseline sanity，不包含 D4-D14。
- 只比较两个最小 baseline：MSE/MAGMSE reconstruction baseline 与 ordinary differentiable CA-CFAR BCE detection-aware baseline。
- 主模型沿用 D2A 的 `SimpleRangeFCN`，未引入新 backbone、attention、RDLR-Net、DiffRIM 或 RIMformer。
- ordinary BCE 训练目标使用 differentiable CA-CFAR soft detection map 与 target/background mask 构造普通 BCE；未加入 weak-target weighting、focal loss、balanced BCE、false alarm penalty 或 clean identity full method。
- train 使用 light + medium，test 使用 light + medium + severe；severe 只作为 stress test。
- evaluation 复用 Gao77 标签生成的 target/background mask，并输出 narrow/default、all targets、non-overlap-only、per-sequence 与 per-class-group 统计。
- fixed-PFA evaluation 报告 background cell count、false alarm count、measured PFA 与 frame/bootstrap 稳定性字段。
- 语法检查与 import 检查已通过；evaluation 使用标签生成的 mask，不把另一个模型输出当 ground truth。

非阻塞注意：

- BCE baseline 训练阶段使用 default mask；narrow mask 作为评估稳定性口径，不作为训练口径。
- D3 只能判断 ordinary BCE 是否可作为后续强 baseline 的入口，不能包装为 proposed method 效果。

## D3-RCA local-only code review — 2026-06-26

状态：`[local-only]`

本次 D3-RCA 脚本审阅对象：

- `G:\mineru_output\experiments\d3_rca_bce_failure_analysis.py`

审阅结论：

- 当前阶段只做 D3 ordinary BCE failure root-cause analysis，不进入 D4-D14。
- 脚本只复现小规模 MSE/BCE 诊断模型，并执行数值域、mask/label、differentiable CFAR、temperature、learning rate、reconstruction anchor 与 clean-input behavior 检查。
- 未实现 focal loss、balanced BCE、weak-target full loss、false alarm penalty、3 seeds 或任何新 backbone。
- 仍使用 Gao77 标签生成的 target/background mask 作为评估依据，未把模型输出当 ground truth。
- `BCE + lambda_rec * MAGMSE` 只作为 RCA 诊断项，用来判断 pure BCE 是否缺少 signal restoration anchor；报告中不得包装为 proposed method。
- 语法检查与 import 检查已通过。

非阻塞注意：

- RCA sweep 使用小步数和小子集，结论只用于定位 D3 失败原因；不能替代正式重跑 D3。
- 如果发现数值域、label、mask 或 CFAR 全 0 / 全 1 bug，应停止并优先修 bug，不继续解释为方法问题。

## D3-Rerun local-only code review — 2026-06-26

状态：`[local-only]`

本次 D3-Rerun 脚本审阅对象：

- `G:\mineru_output\experiments\d3_rerun_gao77_baseline_sanity.py`

审阅结论：

- 当前阶段只重跑修正后的 D3 baseline sanity，不进入 D4-D14。
- 比较三类 baseline：MSE/MAGMSE、pure ordinary differentiable CA-CFAR BCE failure control、以及 `BCE + lambda_rec * MAGMSE` detection-aware baseline。
- `BCE + lambda_rec * MAGMSE` 只作为修正后的 ordinary detection-aware baseline，不包含 weak-target weighting、focal loss、balanced BCE、false alarm penalty 或 clean identity full method。
- `lambda_rec` 仅跑 `0.1/0.5/1.0`，BCE 参数为 `lr=3e-4`、`temperature=1.0`，未做大规模网格搜索。
- 主模型为 D2A 已跑通的 `SimpleRangeFCN`，未引入新 backbone、RDLR-Net、DiffRIM 或 RIMformer。
- evaluation 复用 Gao77 标签生成的 target/background mask 与 fixed-PFA 协议，输出 narrow/default、all/non-overlap、per-sequence、per-class-group 与 clean no-harm。
- 语法检查与 import 检查已通过。

非阻塞注意：

- 本次 D3-Rerun 仍是 range-only sanity；RA 不作为主指标。
- 如果 pure BCE 检测指标最高但 clean no-harm 失败，报告必须把它标记为 invalid detection-shaping failure control。

## D4 local-only code review — 2026-06-26

状态：`[local-only]`

本次 D4 脚本审阅对象：

- `G:\mineru_output\experiments\d4_gao77_strong_baseline_sanity.py`

审阅结论：

- 当前阶段只执行 D4 strong baseline sanity，不进入 D5-D14。
- MSE/MAGMSE 与 BCE+rec anchor 直接复用 D3-Rerun CSV 结果；D4 只训练 balanced BCE+rec 与 focal+rec 分支。
- balanced BCE+rec 包含 mild balance 与 full inverse-frequency balance；权重由 default mask 下 target/background cell 比例计算。
- focal+rec 仅测试 gamma=`1.0/2.0` 与 alpha=`0.25/0.5` 的小网格。
- 所有 D4 分支均使用 `lambda_rec=0.5`、`lr=3e-4`、`temperature=1.0`、`SimpleRangeFCN`。
- 未实现 weak-target-specific weights、CFAR-margin weak weights、low-peak weak weights、false alarm penalty、clean identity full method 或 proposed full loss。
- evaluation 复用 Gao77 标签生成的 target/background mask 与 fixed-PFA 协议，输出 narrow/default、all/non-overlap、per-sequence、per-class-group 与 clean no-harm。
- 语法检查与 import 检查已通过。

非阻塞注意：

- D4 的 baseline comparison range profile 只展示本次训练的 balanced/focal 输出；MSE/BCE+rec anchor 的数值比较来自 D3-Rerun CSV。
- 如果 balanced/focal 与 BCE+rec 接近或更强，D5 必须以 best D4 strong baseline 作为主对照。

## D5 local-only code review - 2026-06-27

状态：`[local-only]`

本次 D5 脚本审阅对象：
- `G:\mineru_output\experiments\d5_gao77_weak_target_weighted_sanity.py`

审阅结论：
- 当前阶段只执行 D5 weak-target-weighted detection loss sanity，不进入 D6-D14。
- D5 只训练 `clean_peak_percentile` 和 `cfar_margin` 两种 weak 定义，每种只测 weak weight `2/3/5`。
- 训练 loss 为 `weak_target_weighted_detection_loss + 0.5 * MAGMSE`，没有加入 false alarm penalty、clean identity full method、proposed full loss、random weak weights、strong-target weights 或 3 seeds。
- 主模型仍为 `SimpleRangeFCN`，输入/输出均为 range-only profile；没有引入 RDLR-Net / DiffRIM / RIMformer 或大模型。
- D5 主对照直接复用 D4 的 `balanced_mild`，同时保留 MSE/MAGMSE、BCE+rec anchor 和 best focal 作为辅助对照。
- fixed-PFA、narrow/default mask、all/non-overlap-only、per-sequence、per-class-group、clean no-harm、MSE/MAGMSE、target peak bias 和 noise floor change 均复用前序真实 target/background mask 评估链路，没有把模型输出当 ground truth。
- 已修正 `build_target_weight_map`：现在按每个 target 的 `target_id`、`frame_idx` 和 interval 精确赋权，避免同一 range 区间跨帧串权重。
- 语法检查、import 检查通过；权重图自检显示 background 权重保持 0，target cells 只包含 `1.0` 和指定 weak weight。

非阻塞注意：

- D5 仍是 Gao77 + synthetic interference + range-only sanity，结论不能包装为最终方法效果。
- 如果 weak Pd 只超过 MSE/BCE+rec 但没有超过 `balanced_mild`，D5 应判为未通过。
- 如果提升伴随 false alarm、target peak bias、clean no-harm 或 non-overlap-only 退化，不能进入 D6。

## D5-check local-only code review - 2026-06-27

状态：`[local-only]`

本次 D5-check 脚本审阅对象：
- `G:\mineru_output\experiments\d5_check_improvement_significance.py`

审阅结论：
- 当前阶段只执行 D5-check，用于验证 D5 中 `weak_peak_w2p0` 相对 D4 `balanced_mild` 的微小 weak Pd 提升是否稳定。
- 脚本没有进入 D6，没有实现 false alarm penalty、clean identity full method、proposed full loss、random weak weights、strong-target weights 或新 backbone。
- 训练对象严格限制为两个配置：`balanced_mild` 和 `weak_peak_w2p0`。
- 3 seeds mini-check 固定原始 train/val/test 与 synthetic interference 数据流水线，只改变训练随机种子，用于估计初始化/训练随机性。
- split robustness 只做一个轻量 alternate split，每个配置各一次，不作为正式 D6 证据。
- hit-count、mask robustness、PFA=1e-2/1e-3、all/non-overlap-only、narrow/default 均直接从 D5 已保存 fixed-PFA CSV 或本次真实 target/background mask 评估中读取。
- evaluation 继续使用 Gao77 标签生成的 target/background mask；没有把模型输出当 ground truth。
- 语法检查和 import 检查通过。

非阻塞注意：

- 如果原始主口径只多 hit 1 个 weak target，即使 seed 均值略好，也应按用户规则标记为 statistically weak signal。
- 只有平均提升超过 seed std，且 narrow/default、non-overlap-only、PFA=1e-3、clean no-harm 都支持时，才建议进入 D6。

## D5-diagnosis local-only code review - 2026-06-27

状态：`[local-only]`

本次 D5-diagnosis 脚本审查对象：
- `G:\mineru_output\experiments\d5_diagnosis_weak_weighting_failure.py`

审查结论：
- 当前阶段只执行 D5-diagnosis，用于判断 `weak_peak_w2p0` 相对 `balanced_mild` 不稳定的来源；不进入 D6。
- 脚本只训练两个 loss 配置：`balanced_mild` 和 `weak_peak_w2p0`；没有训练 focal、balanced_full、其它 weak weight 或 proposed full loss。
- false alarm 只作为评估指标读取和输出，没有实现 false alarm penalty；clean MSE 只作为 no-harm 诊断指标，没有实现 clean identity full method。
- 模型容量检查只限 `SimpleRangeFCN(hidden=128)`、`SimpleRangeFCN(hidden=256)` 和一个很小的 residual 1D U-Net sanity model；没有引入 RDLR-Net / DiffRIM / RIMformer 或大模型。
- train size 检查固定 validation/test split；由于 D1A split 中非泄漏训练独立帧只有 300 帧，1000/1500 effective samples 通过重复训练帧生成新的 synthetic interference 实现，报告中必须注明这不是新增真实 clean frame 多样性。
- evaluation 继续复用 Gao77 标签生成的 target/background mask、fixed-PFA、narrow/default、all/non-overlap-only、PFA=1e-2/1e-3 和 clean no-harm 口径；没有把其它模型输出当作 ground truth。
- 语法检查通过：`python -m py_compile experiments/d5_diagnosis_weak_weighting_failure.py`。

非阻塞注意：
- 容量检查中的 shallow 1D U-Net 只是轻量 sanity，不应包装成新 backbone 或论文贡献。
- 如果 gain 只在重复 synthetic samples 下出现，不能外推为真实数据量充分时一定有效。
