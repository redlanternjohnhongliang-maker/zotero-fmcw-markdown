# D5G Literature Review: Representation Protocol Audit and Future Direction Study

**Date**: 2026-06-27  
**Project**: Fixed-PFA Weak-Target-Preserving Training for FMCW Radar Interference Mitigation  
**ARIS skills used**: `/research-lit`, `/experiment-plan`, `/result-to-claim`, `/kill-argument`  
**Local paper library**: no `papers/` or `literature/` directory found under `G:\mineru_output`; this review uses external web/arXiv/venue metadata plus local D5D/D5E result files.

## 1. Executive summary

当前失败更像是 **representation / annotation / evaluation protocol** 共同造成的不可判定问题，而不是一个可以直接归因给 simple FCN 容量不足的问题。

D5-check 到 D5B 说明 range-only weak weighting 的收益很不稳，修复 weak definition 后没有稳定过预注册门槛。D5D 的 RD-only supplement 没有显示 weak weighting gain，D5E 进一步证明当前 RD proxy 在 PFA=1e-2 下已经饱和：`balanced_mild` 本身就命中 `62/62` weak targets。更严格的 PFA=1e-3 没有救回 weak weighting，反而平均 `weak Pd delta=-0.0161`。

文献给出的信号很一致：FMCW interference mitigation 和 radar perception 很少只依赖 range-only；常见输入包括 beat-signal spectrogram、magnitude+phase、complex-valued tensor、RD/RAD、temporal RD/RAD 和 raw ADC/IF。也就是说，range-only 确实可能太弱。但 D5G 不能把这写成已证明的主因，因为当前项目没有 true Doppler/angle/RAD labels，RD 仍是 mixed proxy，RA 也没有通过自检。因此最稳的下一步不是训练新模型，而是做 no-training representation protocol audit。

## 2. Interference mitigation papers

| paper | year | input | output | model | loss | data type | evaluation | relevance to current project | limitation for current project |
|---|---:|---|---|---|---|---|---|---|---|
| [A Deep Learning Approach for Automotive Radar Interference Mitigation](https://ieeexplore.ieee.org/document/8515215) | 2018 | interfered beat/radar signal representation | mitigated signal/profile | early DNN/CNN-style mitigation | reconstruction-style | simulated automotive radar interference | signal reconstruction and interference suppression | Shows DL mitigation is plausible before detector. | Does not answer fixed-PFA weak-target preservation. |
| [An Interference Mitigation Technique for FMCW Radar Using Beat-Frequencies Interpolation in the STFT Domain](https://ieeexplore.ieee.org/document/8551288/) | 2019 | STFT time-frequency representation | reconstructed beat frequencies | classical interpolation | non-learning | FMCW radar | signal quality / target masking analysis | Directly addresses interference masking weak targets and STFT repair. | Classical method; not a learned weak-target objective. |
| [Deep Interference Mitigation and Denoising of Real-World FMCW Radar Signals](https://ieeexplore.ieee.org/document/9114627/) | 2020 | real measurements plus simulated interference | denoised / mitigated FMCW signal | CNN denoising | regression/reconstruction | real-world FMCW plus simulated interference | denoising and state-of-art comparison | Important because it evaluates real measurements, not only synthetic profiles. | Still not fixed-PFA weak-target metric. |
| [Fully Convolutional Neural Networks for Automotive Radar Interference Mitigation](https://arxiv.org/abs/2007.11102) | 2020 | beat-signal spectrogram | clean range profile | FCN | range-profile reconstruction | synthetic automotive-like ARIM | outperforms zeroing | Closest to current simple FCN range-profile style; shows spectrogram-to-range-profile pipeline. | It collapses output to range profile, so Doppler/angle weak-target ambiguity remains. |
| [Estimating the Magnitude and Phase of Automotive Radar Signals under Multiple Interference Sources with Fully Convolutional Networks](https://arxiv.org/abs/2008.05948) | 2020/2021 | interfered radar signal / range profiles under multiple interferers | magnitude and phase | FCN with pruning | magnitude and phase estimation | ARIM-v2 synthetic realistic multi-interference | phase error and magnitude reconstruction | Strong warning that phase is not disposable; current magnitude/range-only protocol may be lossy. | Synthetic-style dataset; no fixed-PFA detector gate. |
| [Automotive Radar Signal Interference Mitigation Using RNN with Self Attention](https://doi.org/10.1109/ICASSP40776.2020.9053013) | 2020 | sequential radar signal | mitigated signal | RNN + self-attention | reconstruction | automotive radar signals | reconstruction / mitigation metrics | Introduces temporal/sequential modeling as a mitigation route. | Not a reason to jump to a larger model before protocol validity. |
| [Automotive Radar Interference Mitigation With Unfolded Robust PCA Based on Residual Overcomplete Auto-Encoder Blocks](https://doi.org/10.1109/CVPRW53098.2021.00358) | 2021 | spectrogram / signal matrix | separated clean and interference components | unfolded robust PCA + autoencoder blocks | reconstruction / decomposition | ARIM-like simulated data | mitigation quality | Shows structured decomposition can exploit low-rank/sparse priors. | More complex method; does not solve our label/proxy uncertainty. |
| [Resource-efficient Deep Neural Networks for Automotive Radar Interference Mitigation](https://arxiv.org/abs/2201.10360) | 2021/2022 | radar signal tensors | mitigated/denoised signals | quantized CNNs | reconstruction | real-world FMCW plus interference | memory and denoising | Reminds us that model changes should consider radar hardware constraints. | Hardware efficiency is secondary to our current protocol failure. |
| [Prior-Guided Deep Interference Mitigation for FMCW Radars](https://arxiv.org/abs/2108.13023) | 2022 | complex-valued FMCW time-frequency signal | restored useful beat signal | complex-valued FCN with prior regularization | regression plus prior feature regularizer | simulated and measured radar | SINR / generalization | Strong evidence that complex-valued input and time-frequency priors matter. | It supports future complex input, not immediate model escalation. |
| [Interference Mitigation for FMCW Radar With Sparse and Low-Rank Hankel Matrix Decomposition](https://research.tudelft.nl/en/publications/interference-mitigation-for-fmcw-radar-with-sparse-and-low-rank-h/) | 2022 | dechirped time-domain measurements lifted to Hankel matrix | separated useful signal | sparse and low-rank ADMM | optimization objective | simulations and experiments | signal estimation and distributed targets | Shows classical structure can separate beat signals and chirp-like interference. | Not a detector/paper claim by itself for Gao77 fixed-PFA weak targets. |
| [Radar-STDA: A High-Performance Spatial-Temporal Denoising Autoencoder for Interference Mitigation of FMCW Radars](https://arxiv.org/abs/2307.09063) | 2023 | spatial-temporal radar maps, including temporal context | denoised radar map | spatial-temporal denoising autoencoder | reconstruction | FMCW radar | mitigation quality and efficiency | Supports temporal RD-style audit because weak targets may need cross-frame evidence. | Does not give Gao77 label validity; should not become main model now. |
| [RIMformer: An End-to-End Transformer for FMCW Radar Interference Mitigation](https://arxiv.org/abs/2407.11459) | 2024 | time-domain IF signals | restored target signals / mitigated interference | Transformer with dual attention and convolutional blocks | restoration losses | simulation and measurement | signal restoration | Shows raw IF end-to-end route is active and plausible. | Explicitly forbidden as immediate main model; expensive and does not fix labels. |

## 3. Radar representation papers

| paper | year | representation | label type | model | task | relevance | limitation |
|---|---:|---|---|---|---|---|---|
| [Vehicle Detection With Automotive Radar Using Deep Learning on Range-Azimuth-Doppler Tensors](https://openaccess.thecvf.com/content_ICCVW_2019/papers/CVRSUAD/Major_Vehicle_Detection_With_Automotive_Radar_Using_Deep_Learning_on_Range-Azimuth-Doppler_ICCVW_2019_paper.pdf) | 2019 | RA and RAD tensor projections | vehicle labels / spatial boxes | CNN/FPN-style RA/RAD model | vehicle detection | Early evidence that dense RAD tensors carry useful detection information beyond point clouds. | Dataset/protocol differs; no weak-target interference mitigation. |
| [CARRADA Dataset: Camera and Automotive Radar with Range-Angle-Doppler Annotations](https://arxiv.org/abs/2005.01456) | 2020/2021 | RA, RD, RAD | sparse points, boxes, dense masks | FCN segmentation baseline | radar semantic segmentation | Directly relevant to label-valid RA/RD/RAD protocol design. | Small controlled dataset; labels are semi-automatic, not Gao77 labels. |
| [RODNet: Radar Object Detection Using Cross-Modal Supervision](https://openaccess.thecvf.com/content/WACV2021/papers/Wang_RODNet_Radar_Object_Detection_Using_Cross-Modal_Supervision_WACV_2021_paper.pdf) | 2021 | temporal RA heatmaps / RF images | camera-radar fused pseudo labels | 3D conv autoencoder variants | object detection | Strong argument for temporal RA when human labels are scarce. | Pseudo-labels have their own bias; not an interference mitigation protocol. |
| [RODNet: A Real-Time Radar Object Detection Network Cross-Supervised by Camera-Radar Fused Object 3D Localization](https://arxiv.org/abs/2102.05150) | 2021 | RA RF image sequences | cross-supervised object localization | real-time radar network | object detection | Confirms temporal radar frames are useful for perception. | Does not validate current Gao77 RD proxy boxes. |
| [RADDet: Range-Azimuth-Doppler based Radar Object Detection for Dynamic Road Users](https://arxiv.org/abs/2105.00363) | 2021 | RAD tensor and Cartesian BEV | 3D boxes on RAD and 2D BEV boxes | one-stage anchor detector | dynamic road-user detection | The clearest RAD tensor precedent; includes annotation strategy. | Auto-annotation and public dataset differ from Gao77; not a free transfer. |
| [Raw High-Definition Radar for Multi-Task Learning / FFT-RadNet](https://arxiv.org/abs/2112.10646) | 2022 | raw HD radar, RD, learnable angle recovery | vehicle boxes, freespace labels | FFT-RadNet | detection and freespace segmentation | Shows raw/RD-to-angle learning can reduce explicit RAD cost. | HD radar/RADIal setup differs from current Gao77. |
| [T-FFTRadNet: Object Detection with Swin Vision Transformers from Raw ADC Radar Signals](https://openaccess.thecvf.com/content/ICCV2023W/BRAVO/html/Giroux_T-FFTRadNet_Object_Detection_with_Swin_Vision_Transformers_from_Raw_ADC_ICCVW_2023_paper.html) | 2023 | raw ADC, RD, RAD variants | dataset object labels | Swin Transformer radar detector | object detection | Directly compares ADC/RD/RAD-style inputs and motivates raw ADC as future route. | Larger model and different task; not appropriate before protocol audit. |
| [ADCNet: Learning from Raw Radar Data via Distillation](https://arxiv.org/html/2303.11420v3) | 2023 | raw ADC and RD/RAD generated views | distillation labels | raw-radar network | detection/freespace | Useful for longer-term raw ADC if labels become reliable. | Distillation does not solve weak-target ground truth by itself. |

## 4. What the literature suggests

- **为什么 range-only 可能太弱**：range-only 保留距离峰，但丢掉 Doppler、azimuth、phase 和 temporal persistence。当前项目的 range-only overlap contamination 正好说明多个目标/干扰容易在同一 range mask 内混在一起。
- **为什么 RD 有用但需要可信 Doppler protocol**：RD 能把相同 range 的不同 radial velocity 分开，理论上可以减少 overlap。但 D5D/D5E 的 RD boxes 来自 range labels + clean-RD Doppler peak projection，不是真 Doppler GT；所以 RD saturation 说明当前 proxy 不行，不说明 RD 本身不行。
- **为什么 RA 有用但依赖角度校准**：RA 可以区分同 range 不同 azimuth 的目标。CARRADA、RODNet 和 RA/RAD perception 文献都依赖相机-雷达校准或半自动标注。D5C/RA inconclusive 不能被写成 RA 无效，只能写 angle mapping / projection / label 未通过。
- **为什么 RAD 是自然下一步**：RAD 同时保留 range、azimuth、Doppler，是 dense radar tensor 中最完整的可解释表示。RADDet、Major et al. 和 CARRADA 都说明 RAD 是合理输入。但当前 Gao77 是否具备 RAD label feasibility 仍未知。
- **为什么 temporal RD/RAD 可能帮助 weak target**：弱目标在单帧中可能低于阈值或被干扰遮挡，但跨帧有 motion consistency。Radar-STDA 和 RODNet 都利用 temporal context；因此 temporal audit 应先看 projection hit rate、trajectory consistency 和 leakage。
- **为什么 raw ADC/IF 可能帮助但成本更高**：RIMformer、FFT-RadNet、T-FFTRadNet 和 ADCNet 都显示 raw/radar-native 输入可保留更多信息。但 raw ADC 需要更强 compute、更多校准和标签，不应该在 D5G 直接变成主方法。
- **为什么 complex phase 不能随便丢**：magnitude+phase 和 complex-valued CV-FCN 文献显示 phase 影响信号恢复和低 SINR 表现。当前只看 magnitude/range 的协议可能隐藏 phase 破坏，但这需要 protocol audit 验证。
- **fixed-PFA 仍应保留**：CFAR/constant false alarm rate 的核心是固定 false-alarm operating point 后比较 Pd。当前不能修改 fixed-PFA 主评价协议；要做的是让 labels、weak subsets 和 saturation 合格。

## 5. Mapping back to our D5 results

| stage | local result | literature alignment | D5G interpretation |
|---|---|---|---|
| D5-check | 原始 range-only weak weighting 只多约 1 个 weak hit，3 seeds 平均不稳 | range-only 丢 Doppler/angle/phase/temporal 信息 | 不能继续 claim weak weighting 有效；也不能只怪模型 |
| D5-diagnosis | weak definition instability 与 range-only overlap contamination | RD/RA/RAD 文献强调多维分离 | 输入表示和 weak-label protocol 都可疑 |
| D5B | repaired weak definitions 仍不过线 | weak subset 定义需要与评价表示一致 | range-only negative evidence 成立，但范围很窄 |
| D5C | RD feasibility smoke；RA inconclusive | RA/RAD 需要校准与标签 | 只能说有 RD smoke，不可说 RA/RD 已验证 |
| D5D | RD proxy weak weighting gain = 0；PFA=1e-3 有反向 | RD 可分离但需要真实 Doppler labels | RD proxy 结果是 negative/sanity，不是 confirmed RD performance |
| D5E | PFA=1e-2 下 RD proxy ceiling；q/mask/proxy variants 全部无收益 | fixed-PFA 必须避免 baseline saturation | 当前 RD protocol 不适合测 weak weighting 增益 |

## 6. Recommended future direction

1. **Conservative closure / negative-result narrative**：把 D5-check 到 D5E 写成“当前 range-only 和 mixed RD-proxy 协议下，weak weighting 没有稳定改善 fixed-PFA weak-target preservation”。不要写成通用理论。
2. **Representation protocol audit**：下一步只做 no-training 或 minimal-model audit，检查 label validity、weak_n、overlap、separability、saturation、PFA calibration 和 leakage。
3. **RAD / temporal RD sanity**：如果 Phase 0 证明能获得可信 Doppler/angle/RAD labels，再做 RAD 和 temporal RD/RAD sanity。
4. **Raw ADC / complex input longer-term**：只在 protocol gate 通过后，将 raw ADC/IF、complex IQ 或 learnable FFT 作为长期路线。
5. **Model/loss redesign only after protocol passes**：只有非饱和、label-valid、fixed-PFA 稳定的表示先通过，才考虑 loss 或模型。D6 继续 forbidden。

## Source URLs checked

- RIMformer: https://arxiv.org/abs/2407.11459
- Radar-STDA: https://arxiv.org/abs/2307.09063
- FCN spectrogram mitigation: https://arxiv.org/abs/2007.11102
- Magnitude and phase FCN: https://arxiv.org/abs/2008.05948
- Prior-guided complex-valued FCN: https://arxiv.org/abs/2108.13023
- Deep real-world FMCW mitigation: https://ieeexplore.ieee.org/document/9114627/
- Sparse and low-rank Hankel mitigation: https://research.tudelft.nl/en/publications/interference-mitigation-for-fmcw-radar-with-sparse-and-low-rank-h/
- STFT interpolation: https://ieeexplore.ieee.org/document/8551288/
- RADDet: https://arxiv.org/abs/2105.00363
- CARRADA: https://arxiv.org/abs/2005.01456
- RODNet WACV: https://openaccess.thecvf.com/content/WACV2021/papers/Wang_RODNet_Radar_Object_Detection_Using_Cross-Modal_Supervision_WACV_2021_paper.pdf
- RODNet J-STSP: https://arxiv.org/abs/2102.05150
- FFT-RadNet / RADIal: https://arxiv.org/abs/2112.10646
- T-FFTRadNet: https://openaccess.thecvf.com/content/ICCV2023W/BRAVO/html/Giroux_T-FFTRadNet_Object_Detection_with_Swin_Vision_Transformers_from_Raw_ADC_ICCVW_2023_paper.html
- Vehicle detection with RAD tensors: https://openaccess.thecvf.com/content_ICCVW_2019/papers/CVRSUAD/Major_Vehicle_Detection_With_Automotive_Radar_Using_Deep_Learning_on_Range-Azimuth-Doppler_ICCVW_2019_paper.pdf
