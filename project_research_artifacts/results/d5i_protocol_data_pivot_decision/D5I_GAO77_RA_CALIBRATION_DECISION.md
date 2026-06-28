# D5I Gao77 RA Calibration Decision

**路线**: Route C  
**状态**: diagnostic only  
**结论**: 值得作为附录继续查，但不值得作为主线继续推进。

## 1. 必须检查的 RCA 项

| 检查项 | D5I 判定 |
|---|---|
| px/py 到 azimuth | 可继续核对公式，但不能把 projection 当 true angle GT |
| sign convention | 可检查左右符号和坐标系 |
| degrees/radians | 可检查单位一致性 |
| angle FFT axis | 可检查 `fftshift`、bin ordering、FoV |
| RX channel / antenna dimension | 可检查 virtual array 维度是否使用正确 |
| mask width | 可做 sensitivity，但过宽 mask 会引入 label leakage |
| D1A+ RA projection hit rate vs D5C RA weak hit discrepancy | 值得保留为 RCA evidence |
| calibrated RA 是否能超过 proxy-only | 当前不能；Gao77 缺 true RAD/Doppler/track labels |

## 2. 为什么不能作为主线

RA calibration 即使修好，也只解决 angle projection 的一部分问题。D5H 的 no-pass 不是单一 RA bug 导致的：

- `corrected_RD` 仍依赖 Doppler proxy；
- `RAD` 缺 true RAD boxes；
- temporal routes 缺 track IDs；
- D5E 存在 weak_n 和 baseline saturation 问题；
- fixed-PFA metric chain 仍受 proxy label provenance 限制。

因此，Route C 不能解锁 minimal model sanity，也不能推翻 D5H-Exec no-pass。

## 3. 允许做什么

- 继续整理 Gao77 RA calibration RCA 表；
- 做一张 appendix figure，展示 angle mapping sanity；
- 把 RA 写成 “calibration unresolved / proxy diagnostic”；
- 作为 external dataset pivot 前的错误清单，帮助后续避免坐标系问题。

## 4. 不允许做什么

- 不写 “RA representation invalid”；
- 不写 “RA representation confirmed”；
- 不因为 RA hit rate 改善就进入训练；
- 不把 RA calibration 当作 D6 gate；
- 不把 Gao77 升级为主结果数据集。

## 5. D5I 对 Route C 的判定

**NO-GO as main route; GO only as appendix/diagnostic.**  
如果时间紧，先做 Route B，再回头把 Gao77 RA RCA 整理成附录。

