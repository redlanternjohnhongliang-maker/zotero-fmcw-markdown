# D5I Result To Claim

**日期**: 2026-06-28  
**技能语义**: `/result-to-claim`  
**输入**: D5H-Exec no-pass、D5G failure analysis、D5I dataset feasibility、D5I route comparison  
**Integrity status**: conservative / no-training

## 1. Structured Verdict

| field | judgment |
|---|---|
| claim_supported | partial |
| confidence | medium-high |
| integrity_status | pass for no-training boundary; warn for external dataset facts not fully executable locally |
| supported_claim | D5H-Exec 后应先做 protocol/data pivot，而不是训练、D6、weak weighting 或模型放大 |
| unsupported_claim | 当前不能支持 confirmed RD/RA/RAD performance，也不能支持 weak weighting effectiveness |
| recommended_route | Route A feasibility first; Route B protocol unit test after A-minimal table; Route D report ledger; Route C diagnostic |

> Independent reviewer note: 本判定只基于 D5H/D5G/D5I 上下文和公开 README/arXiv metadata；没有训练、没有下载数据集、没有外部数据实跑。

## 2. What The Evidence Supports

当前证据支持以下 claim：

1. D5H-Exec 没有 representation 通过 gate。
2. 当前 Gao77 路线不能进入 minimal model sanity。
3. 继续 weak weighting、进入 D6、加入 false alarm penalty、修改 detector/fixed-PFA 主协议都没有证据支持。
4. 外部数据集方向有科学价值，应先作为 Route A 完成 label/protocol feasibility，不能直接跳到训练。
5. Controlled synthetic RAD protocol 是在 A-feasibility 后的最小可执行 metric-chain unit test。

## 3. What The Evidence Does Not Support

当前证据不支持：

- “RD/RA/RAD 真实性能已经验证”；
- “RA inconclusive 说明 angle 无效”；
- “range-only 是唯一失败原因”；
- “simple FCN 容量是唯一瓶颈”；
- “negative result 可推广为普遍理论结论”；
- “synthetic protocol 成功后即可宣称真实世界性能”。

## 4. Missing Evidence

| missing evidence | why it matters |
|---|---|
| true Doppler / velocity labels | 支撑 RD/RAD hit 的真实速度维 |
| true RAD boxes or dense masks | 支撑 RAD representation 评估 |
| calibrated azimuth GT | 支撑 RA/RAD angle claim |
| temporal track IDs | 支撑 temporal RD/RA/RAD route |
| clean/interfered pairing | 支撑 mitigation 与 clean no-harm |
| non-saturated fixed-PFA baseline | 让 weak-target gain 有可见空间 |
| adequate weak_n | 避免一两个 hit 造成 fragile claim |

## 5. Go / No-Go

| question | verdict |
|---|---|
| 是否允许训练 | No |
| 是否允许 minimal model sanity | No under current Gao77/D5H; only reconsider after protocol-unit-test gate |
| 是否允许 D6 | No |
| 是否继续 weak weighting | No |
| 是否继续 Gao77 作为主结果 | No |
| 是否只把 Gao77 作为 diagnostic evidence | Yes |
| 是否进入 controlled synthetic protocol | Yes, protocol unit test only |
| 是否进入 external dataset feasibility | Yes, table/design only; no download now |

## 6. Route Claim Ranking

| rank | route | decision | supported claim | unsupported claim |
|---:|---|---|---|---|
| 1 | A External labeled dataset feasibility | GO for protocol audit / dataset selection; NO-GO for download/training | RADIal/RADDet/CARRADA are label-protocol candidates beyond Gao77 proxy | No dataset has confirmed D5 weak-target mitigation performance yet |
| 2 | B Controlled synthetic RAD sanity | GO as unit test | It can validate metric code, thresholding, mask alignment, PFA/PD computation on known GT | It cannot prove real-world preservation or model effectiveness |
| 3 | D Negative/limitation consolidation | GO immediately as report ledger | D5H blocks current method claims under current protocol | It cannot claim fixed-PFA weak-target training universally fails |
| 4 | C Gao77 RA calibration RCA | Conditional diagnostic only | RA calibration may explain local confounds | It cannot explain all no-pass results or unlock training |

## 7. Conservative Claim Wording

中文：

> D5H-Exec 的 no-training audit 没有发现可直接进入训练或 D6 的 representation。当前最可信的下一步是先进行 protocol/data pivot：用 RADIal/RADDet/CARRADA 等数据集做 label feasibility，锁定真实标签边界；随后用 controlled synthetic RAD protocol 作为评估管线单元测试，而不是继续在 Gao77 proxy labels 上扩大模型或继续 weak weighting。

English:

> The D5H-Exec no-training audit did not identify any representation that is eligible for model-training escalation. The defensible next step is a protocol/data pivot: first assess external radar datasets for label-valid future experiments, then use a controlled synthetic RAD unit test to validate the fixed-PFA weak-target metric chain. Current Gao77 evidence should remain diagnostic and should not be reported as confirmed RD/RA/RAD performance.
