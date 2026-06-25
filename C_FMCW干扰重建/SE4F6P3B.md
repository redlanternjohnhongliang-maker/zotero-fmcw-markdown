# DIFFRIM: A DIFFUSION-DRIVEN MODEL FOR HIGH EFFICIENCY RADARINTERFERENCE MITIGATION

Lulu Liu<sup>\*1,3</sup>, Runwei Guan<sup>\*2,3</sup>, Kaishen Yuan<sup>\*2,4</sup>, Sheng Xu<sup>3,5</sup>, Fei Ma<sup>1</sup>, Yutao Yue<sup>†2,3,4</sup>

<sup>1</sup>XJTLU, <sup>2</sup>HKUST (GZ), <sup>3</sup>JITRI, <sup>4</sup>DI<sup>2</sup> Lab, <sup>5</sup>SEU

## ABSTRACT

Despite its all-weather superiority over optical sensors, the dense deployment of millimeter-wave radar in automotive applications causes severe vehicle-to-vehicle interference, degrading detection integrity and introducing safety risks. However, existing interference suppression methods are often limited by over-smoothing, we propose a Diffusion-based framework for real-time Radar Interference Mitigation (DiffRIM). Its stochastic forward process models the incremental addition of interference, and the learned reverse process conducts iterative removement, thereby significantly enhancing interpretability. We further introduce a Lightweight Autoencoder (LWAE) with Mobile Encoder and Decoder (ME/MD) modules, which extracts multi-scale spatial features through point-wise and hierarchical processing. A dual-residual (DualRes) connection mitigates gradient issues, while depthwise separable convolutions (DSC) and channel attention form an efficient spatio-temporal attention (STA) mechanism to extract sparse patterns. Extensive experimental evaluations demonstrate the superior mitigation and generalization performance of our approach in both synthetic and real-world datasets. To support the community, our implementation will be made publicly accessible on https://github.com/luluisthebest/DiffRim.

Index Terms— automotive Radar, interference mitigation, diffusion model, attention machenism, lightweight autoencoder

## 1. INTRODUCTION

Millimeter-wave radar (mmWave) has become indispensable in autonomous driving, particularly 77 GHz frequency-modulated continuous-wave (FMCW) systems, due to its robustness in adverse weather conditions, such as fog, rain, and low light, where cameras and LiDAR often underperform. Its compact form factor further facilitates integration into space-constrained vehicle architectures, underpinning critical functionalities including adaptive cruise control and collision avoidance. However, the automotive industry's shift toward higher levels of autonomy (L3-5) has markedly increased vehicular radar density, intensifying mutual interference within crowded spectral bands. This interference manifests as false positives and signal-to-noise ratio (SNR) degradation, culminating in unreliable detection and compromised path planning.

To address these challenges, mitigation strategies have evolved from hardware-based techniques, e.g., polarization diversity [1] and frequency hopping, to advanced digital signal processing methods, including adaptive filtering [2], wavelet denoising [3], signal-tointerference-plus-noise ratio (SINR) maximization, and Bayesian inference [4]. More recently, deep learning approaches have emerged, leveraging convolutional [5] and recurrent neural networks (CNNs and RNNs) to learn interference patterns directly from raw radar data or range-Doppler (RD) maps. Studies have incorporated waveletspatial domain fusion and optimized UNet++ architectures, with some employing self-attention (SA) mechanisms to improve feature discrimination [6] [7]. Nevertheless, these data-driven methods remain constrained by limited adaptability to real-world environments and a tendency toward oversmoothing, which attenuates critical high-frequency information and undermines recall performance.

Diffusion models, which employ Markov chains for iterative denoising, have demonstrated remarkable success in generative tasks including image synthesis and sensor data simulation [8] [9]. Their potential for radar interference suppression, however, remains largely untapped. In this work, we introduce a lightweight Diffusionbased framework for real-time Radar Interference Mitigation (DiffRIM), comprising three key innovations: (1) a parameter-efficient architecture LightWeight AutoEncoder (LWAE) for multi-scale feature extraction and interference reconstruction; (2) a Spatio-Temporal Attention (STA) mechanism that dynamically weights features to retain interference while suppressing target coherence; and (3) two processes that explicitly model interference injection and iterative suppression. Extensive evaluations demonstrate a 9.23 dB SINR improvement on our largescale synthetic data, which merges real and simulated interference, and a nearly 2× mAP gain in real-world scenarios, all while sustaining 18.02 ms inference latency on an NVIDIA RTX A4000, confirming its suitability for automotive edge deployment.

## 2. METHODOLOGY

## 2.1. Radar Interference Problem Formulation

In fast chirp FMCW radar [10–12], the corrupted signal in time domain, formed by the linear superposition of multiple reflections and mutual interference, is given by:

$$
s = \sum _ { o = 1 } ^ { N _ { O } } s _ { 0 , o } + \sum _ { i = 1 } ^ { N _ { I } } s _ { I , i } + n ,\tag{1}
$$

where $N _ { O }$ and $N _ { I }$ denote the number of targets and interfering sensors, respectively. n represents the receiver thermal noise, modeled as complex-valued Gaussian white noise. Due to the linearity of the Fourier transform, the received signal I (referred to as RD map) in frequency domain obtained via a 2D Fourier transform exhibites the same linear superposition characteristics:

![](images/fdbb25b7c1f521a16a81d79e2d5d1e328f65b8bb525e1d195fe3cec4065d41db.jpg)  
Fig. 1: The architecture of DiffRIM comprises diffusion process, LWAE, and denoising process.

$$
I = \sum _ { o = 1 } ^ { N _ { O } } I _ { 0 , o } + \sum _ { i = 1 } ^ { N _ { I } } I _ { I , i } + N = I _ { 0 } + I _ { I } + N ,\tag{2}
$$

where $I _ { 0 , o } , I _ { I , i } ,$ , and $N$ represent the RD map of $s _ { 0 , o } , s _ { I , i } ,$ and $n .$ The challenge lies in accurately recovering the target location from interference while avoiding excessive smoothing and thus preserving high-frequency information. Firstly, we model interference injection with forward diffusion process. Given that the statistical distributions of the noise and target are known in training process, whereas the distribution of the interference are unknown, we secondly propose LWAE to learn the distribution of the interference signals $I _ { I } .$ This allows us to decouple the interference from the noise, followed by an iterative denoising process to ultimately recover the desired signal. The overall architecture is illustrated in Fig. 1.

## 2.2. LightWeight AutoEncoder

Mobile Encoder and Decoder. We propose a computationally efficient yet high-performance mobile encoder (ME) and decoder (MD) to predict interference signal following [13]. Each ME block processes the input tensor $\begin{array} { r } { I _ { i n } \in \mathbb { R } ^ { C \times H \times W } } \end{array}$ through two cascaded stages, where C, H and W represent the channel, height and width dimensions of the RD map, respectively. The first stage is F eatureF usion that captures point-wise and local spatial patterns through multi-scale convolutional kernels and short residual connection. The outputs of all branches are aggregated via element-wise summation and subsequently fed into the second stage F eatureSampling with a long residual connection. This dual residual (DualRes) is designed not only to alleviate the gradient vanishing or explosion but, more importantly, to preserve the high-frequency components of the interference features, promoting them to be removed by subsequent operations. Symmetric encoderdecoder pairs are linked via additive skip connections to enhance gradient flow and feature reuse. Furthermore, time embeddings $T _ { e m b } \in R ^ { d }$ are injected into each stage via affine transformations.

Spatio-Temporal Attention. Due to the sparse nature of radar maps, they are semantically less rich compared to optical image. Therefore, standard convolution exhibit high parameter redundancy, and the weight-sharing mechanism of convolutional kernels forces both targets and interference patterns to be processed through identical filters, which is suboptimal for interference suppression. To address these issues, we propose an efficient STA module that includes depthwise separable convolution (DSC) and channel attention to adaptively recalibrate feature maps by learning spatial and temporal channel dependencies. DSC are employed in each stage of ME/MD and channel attention is positioned after the ME/MD module, better extracting sparse features while simultaneously reducing computational complexity.

## 2.3. Diffusion Model based Iterative interference suppression

Forward Diffusion Process. As analyzed in equation (2), the interfered RD map I is a superposition of the target signal (ground truth) $I _ { 0 } ,$ the interference signal $I _ { I } ,$ , and Gaussian noise $I _ { \mathrm { n } } \sim$ $\mathcal { N } ( 0 , \sigma ^ { 2 } \mathbf { I } _ { 3 \times H \times W } )$ . This process is modeled as a fixed Markov chain that progressively introduces interference and noise into the target signal. The transition from state $I _ { t - 1 }$ to $I _ { t }$ is defined as:

$$
I _ { t } = I _ { t - 1 } + \alpha _ { t } I _ { I } + \beta _ { t } ^ { 2 } I _ { \mathrm { n } } ,\tag{3}
$$

where $\alpha _ { t }$ and $\beta _ { t }$ are independent coefficient schedules that control the interference and noise diffusion, respectively. Following reparameterization techniques [14], I<sub>t</sub> is sampled directly from $I _ { 0 }$ via:

$$
I _ { t } = I _ { 0 } + \bar { \alpha } _ { t } I _ { I } + \bar { \beta } _ { t } I _ { \mathrm { n } } ,\tag{4}
$$

where $\begin{array} { r } { \bar { \alpha } _ { t } ~ = ~ \sum _ { i = 1 } ^ { t } { \alpha _ { i } } } \end{array}$ and $\bar { \beta } _ { t } ~ = ~ \sqrt { \sum _ { i = 1 } ^ { t } \beta _ { i } ^ { 2 } }$ . This formulation describes the forward diffusion process and provides the input to the LWAE module.

Denoising Process. In the reverse process, we iteratively remove the interference $\hat { I _ { I } }$ predicted by LWAE from $I _ { T }$ to $I _ { 0 }$ . Based on [15], $I _ { t - 1 }$ is sampled from $I _ { t }$ using:

$$
I _ { t - 1 } = I _ { t } - ( \bar { \alpha } _ { t } - \bar { \alpha } _ { t - 1 } ) \hat { I } _ { I } - ( \bar { \beta } _ { t } - \bar { \beta } _ { t - 1 } ) I _ { \mathrm { n } } .\tag{5}
$$

The loss function throughout this architecture is designed to optimize this denoising process as following:

$$
L _ { 2 } : = \mathbb { E } \left[ \left\| I _ { I } - \hat { I _ { I } } ( I _ { t } , t , I ) \right\| ^ { 2 } \right] .\tag{6}
$$

We leverage the forward and reverse processes to model the introduction and removal of interference, thereby enhancing the interpretability of the model. A comprehensive description of the overall workflow is provided in Algorithm 1.

Algorithm 1 Training and validating (testing) procedure of DiffRIM   
Require: Interfered RD maps $I ~ \in ~ R ^ { 3 \times H \times W }$ , ground truth RD   
maps $I _ { 0 } \in R ^ { 3 \times H \times W }$ , iterations $N ,$ diffusion timesteps $T ,$ dif  
fusion coefficients α¯ and ${ \bar { \beta } } ,$ loss $L _ { 2 } ,$ time embeddings t   
Ensure: Predicted clean RD map $\hat { I _ { 0 } } \in R ^ { 1 \times H \times W }$   
▷ Training procedure   
1: for $n \gets \bar { 0 } \bar { \mathrm { t o } } N$ do   
2: $I _ { I }  I - I _ { 0 }$ ▷ Calculate residual (interference)   
3: ${ \cal I } _ { \mathrm { n } } \sim { \mathcal N } ( 0 , \sigma ^ { 2 } { \bf I } _ { 3 \times H \times W } )$ ▷ Generate Gaussian noise   
4: $I _ { \mathrm { T } }  I _ { 0 } + \bar { \alpha } * I _ { I } + \bar { \beta } * I _ { \mathrm { n } }$ ▷ Forward diffusion process   
with equation 4   
5: $\hat { I } _ { I } \gets \mathrm { L W A E }$ (concat $( I _ { \mathrm { T } } , I _ { I } ) , t )$ ▷ Predict interference   
6: $l o s s \gets L _ { 2 } ( I _ { I } , \hat { I _ { I } } )$ ▷ Calculate $L _ { 2 }$ loss with equation 6   
7: end for   
▷ Validating (testing) procedure   
8: $I ^ { \prime } \gets I + \mathcal { N } ( 0 , \sigma ^ { 2 } \mathbf { I } _ { 3 \times H \times W } )$ ▷ Add Gaussian noise   
9: for $t \gets T$ to 1 do ▷ Reverse diffusion process   
10: $\hat { I } _ { I } \gets \mathrm { L W A E } ( \mathrm { c o n c a t } ( I ^ { \prime } , I ) , t )$ ▷ Predict interference   
11: $\hat { I } _ { \mathrm { n } } \gets ( I ^ { \prime } - I _ { I } - \bar { \alpha } * \hat { I } _ { I } ) / \bar { \beta }$ ▷ Predict noise   
12: $\hat { I _ { 0 } } \gets I - \hat { I _ { I } }$ ▷ Update denoised map   
13: $I ^ { \prime }  I ^ { \prime } - ( \bar { \alpha } _ { t } - \bar { \alpha } _ { t - 1 } ) * \hat { I } _ { I } - ( \bar { \beta } _ { t } - \bar { \beta } _ { t - 1 } ) * \hat { I } _ { \mathrm { n } }$ ▷ Update   
inputs with equation 5   
14: end for   
15: return $\hat { I _ { 0 } }$

## 3. EXPERIMENTS AND RESULTS

## 3.1. Datasets

Synthetic dataset. Due to the scarcity of annotated real-world data and the limited realism of simulations, we propose a synthetic radar dataset generation strategy. Real victim signals are drawn from the RaDICaL dataset [16], providing environmental diversity and hardware-specific artifacts. Interferers are simulated via $\mathbf { M A T L A B } ^ { \otimes }$ Radar Toolbox<sup>™1</sup> with stochastic parameters. Interference power varies from -5 dB to 25 dB in 5 dB steps, while bandwidth, range, and velocity follow uniform distributions. The composite signal is formed by superimposing these components, followed by standard signal processing in equation (2). The resulting dataset comprises 384,685 RD maps of size 64×128, split into training (83%), validation (8.3%), and testing (8.3%).

Real-world dataset. We use the small-scale dataset from [17] for cross-domain validation comprising one victim radar and two interferers. Scenarios include static targets (e.g., traffic signals, a car, a barrier) and a dynamic target (a drone). Unfortunately, no ground truth is available for training; thus, we select a subset of 500 high-amplitude samples from the dataset and manually annotate to evaluate the pre-trained model.

## 3.2. Evaluation Metrics and Settings

Metrics. We rigorously evaluate the proposed method through ∆SINR that quantifies the enhancement in signal purity after interference suppression, calculated as:

$$
\Delta \mathrm { S I N R } = 1 0 \log ( \frac { \Vert I _ { 0 } \Vert ^ { 2 } } { \Vert \hat { I _ { 0 } } - I _ { 0 } \Vert ^ { 2 } } ) - 1 0 \log ( \frac { \Vert I _ { 0 } \Vert ^ { 2 } } { \Vert I - I _ { 0 } \Vert ^ { 2 } } )\tag{dB}
$$

(7)

Table 1: Quantitative comparison results on the synthetic dataset.
<table><tr><td>Method</td><td>Params (M)</td><td>Lat. (ms)</td><td>∆SINR↑</td><td>LPIPS↓</td></tr><tr><td>Zeroing [18]</td><td>=</td><td>-</td><td>-2.39</td><td>0.52</td></tr><tr><td>IMAT [19]</td><td></td><td></td><td>-0.71</td><td>1.11</td></tr><tr><td>SSC-VAE [20]</td><td>22.82</td><td>13.52</td><td>-4.72</td><td>0.49</td></tr><tr><td>RD [21]</td><td>33.95</td><td>62.19</td><td>4.29</td><td>0.15</td></tr><tr><td>FConvNet [22]</td><td>1.88</td><td>2.38</td><td>5.60</td><td>0.96</td></tr><tr><td>CAE [23]</td><td>0.26</td><td>0.66</td><td>7.63</td><td>0.67</td></tr><tr><td>imRICnn [24]</td><td>0.01</td><td>1.05</td><td>8.81</td><td>0.27</td></tr><tr><td>DiffRIM</td><td>0.34</td><td>18.02</td><td>9.29</td><td>0.26</td></tr></table>

Table 2: Quantitative comparison results on the real-world dataset.
<table><tr><td>Method</td><td>NM</td><td>RD [21]</td><td>CAE [23]</td><td>imRICnn [24]</td><td>DiffRIM</td></tr><tr><td>mAP (%)</td><td>28.27</td><td>16.18</td><td>23.94</td><td>43.28</td><td>47.91</td></tr><tr><td>mAR (%)</td><td>13.86</td><td>12.29</td><td>10.34</td><td>50.11</td><td>52.83</td></tr></table>

Learned Perceptual Image Patch Similarity (LPIPS) [25] measures perceptual similarity between denoised and reference RD maps using deep feature correlations from a pretrained VGG network:

$$
\mathrm { L P I P S } = \frac { 1 } { N } \sum _ { l = 1 } ^ { L } \sum _ { i , j } \frac { \| \phi _ { l } ( I _ { 0 } ) _ { i , j } - \phi _ { l } ( \hat { I _ { 0 } } ) _ { i , j } \| _ { 2 } ^ { 2 } } { H _ { l } W _ { l } C _ { l } } ,\tag{8}
$$

where $\phi _ { l }$ represents layer $l ^ { \circ } \mathrm { s }$ activations, and $H _ { l } , W _ { l } , C _ { l }$ are the corresponding feature map dimensions. Owing to the absence of ground-truth labels in the real-world dataset, we additionally report mean Average Precision (mAP) and mean Average Recall (mAR) to assess detection accuracy and recall following interference mitigation. For detection, a CA-CFAR detector [26] was employed, using 8 training cells in both range and velocity dimensions, with guard cells set to 5 in range and 3 in velocity.

Settings. We conduct all experiments on a single NVIDIA RTX A4000 GPU using the synthetic dataset for both training and inference, with a batch size of 128 for 150,000 steps, using the Adam optimizer with an initial learning rate of $8 \times \mathrm { 1 0 ^ { - 5 } }$ . The diffusion process uses 1 sampling timestep, and three consecutive RD maps are used to incorporate temporal context under real-time constraints.

## 3.3. Results and Analysis

Quantitative Results. As summarized in Table 1, the proposed DiffRIM model achieves the highest ∆SINR on the synthetic dataset, outperforming all baseline methods. Conventional algorithms such as Zeroing [18] and IMAT [19] result in negative ∆SINR due to overly aggressive thresholding that introduces signal distortion. While CAE [23] and FConvNet [22] offer limited improvement, likely owing to insufficient network structure. SSC-VAE [20] is a variational autoencoder and attention machenism based network for image reconstruction, showing inappropriate on our task. ImRICnn [24] attains competitive performance with relatively few parameters. Radar-Diffusion (RD) [21] applied to generate dense Radar point cloud via cross-modal fusion achieves the best LPIPS, attributed to its LPIPS-based loss function; however, it yields a 37.2% lower ∆SINR gain than DiffRIM despite using 100× more parameters. Furthermore, DiffRIM enables real-time processing with an inference latency of 18.02 ms and only 0.34M parameters. As shown in Table 2, DiffRIM also generalizes robustly to the real-world data under intense inference. Comparisons under the no mitigation (NM) scenario reveal that both RD and CAE fail to improve performance, primarily because of excessive oversmoothing of target peaks. Although ImRICnn enhances detection accuracy, it still falls short of DiffRIM by 4.63% in precision and 1.72% in recall, demonstrating our model<sup>′</sup>s superior ability to suppress interference while preserving structural details.

Table 3: Ablation study quantifying component contributions to interference suppression performance.
<table><tr><td>No.</td><td>ChannelN</td><td>T1</td><td>DualRes</td><td>STA</td><td>Branch3</td><td>Frames3</td><td>DM</td><td>Params (M)</td><td>Lat. (ms)</td><td>∆SINR ↑</td><td>LPIPS↓</td></tr><tr><td>0</td><td>√</td><td></td><td>√</td><td></td><td>√</td><td>√</td><td>√</td><td>0.662</td><td>102.265</td><td>-0.554</td><td>0.554</td></tr><tr><td>1</td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>0.139</td><td>17.422</td><td>8.190</td><td>0.290</td></tr><tr><td>2</td><td>√</td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td>0.141</td><td>12.944</td><td>8.381</td><td>0.293</td></tr><tr><td>3</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td>√</td><td>0.340</td><td>19.175</td><td>8.702</td><td>0.224</td></tr><tr><td>4</td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td>√</td><td>√</td><td>0.313</td><td>42.458</td><td>8.791</td><td>0.221</td></tr><tr><td>5</td><td>√</td><td>√</td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td>0.268</td><td>35.828</td><td>8.828</td><td>0.241</td></tr><tr><td>6</td><td>√</td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>0.341</td><td>49.733</td><td>9.292</td><td>0.259</td></tr><tr><td>7</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>0.341</td><td>18.023</td><td>9.289</td><td>0.257</td></tr></table>

![](images/aab959eade40e21b88b366c0707bd11d385ce4a3f63b11a38af6859208206f4d.jpg)  
(a) Camera images

![](images/b28e51fe3ecd9fc5f29453575d135d0329563d4717b47486610497c15c43af66.jpg)  
(b) Ground truth

![](images/f20894af51be2f02e5a844b5a6d30051a3c6a371921a45a1c3b8ddba65d18a35.jpg)  
(c) Interfered

![](images/edcccc1fa26952d9fd4cef64c9cdc5ac8f91eb904f6a261bc0e89b40f4e45d21.jpg)  
(d) imRICnn

![](images/34d6ea404873d5ea7d4cbf0e95956cf0733b1438bc127bac2011f85d3bbccac6.jpg)  
(e) Our DiffRIM

Fig. 2: Qualitative interference mitigation results with color-coded detection boxes.  
![](images/01b329345ca43203f414b9ef2248fd8e5ba9d76355dc6a7b32f9820634b3d697.jpg)  
(a) ∆SINR under 7 levels

![](images/bb5b49067564dca5c5c7131f871fa2f60ea6457533a1faa68d5a67db524dfa6d.jpg)  
(b) LPIPS under 7 levels  
Fig. 3: ∆SINR and LPIPS under all levels of interference power.

Ablation Study. As summarized in Table 3, our ablation study systematically evaluates key components of DiffRIM. Replacing the STA with SA results in significant performance degradation, confirming STA’s superior efficiency in sparse feature enhancement. Halving the number of channels causes a 1.10 dB drop in ∆SINR, demonstrating that model capacity is critical. Removing the diffusion module (DM) reduces ∆SINR by 0.91 dB, underscoring its importance for high-precision interference suppression. Using single-frame input instead of temporal frames lead to a 0.59 dB decline, highlighting the benefit of leveraging inter-frame correlations. Reducing the parallel branches in the first stage from three to two decreases performance by 0.50 dB, and removing the long skip connection in DualRes results in a 0.46 dB reduction, validating our architectural design. Increasing diffusion timesteps from 1 to 3 yields negligible performance gains but triples the inference delay.

Visualized Results. As shown in line 1 of Fig. 2, DiffRIM effectively suppresses interference while preserving structural details, successfully recovering obscured target peaks with minimal distortion. In contrast, imRICnn incompletely removes interference and attenuates targets. In scenario 2 with no targets, only DiffRIM suppresses clutter effectively, thereby reducing false alarms. Furthermore, comparative analysis (line 3) reveals an inherent limitation of RD map, low Radar detectable radial velocity, e.g., 23.02 m/s in RaDICaL, results in fast moving targets existing the field of view. These results demonstrate DiffRIM’s balanced performance across various sensing scenarios. As depicted in Fig. 3, ∆SINR decreases with increasing interference power in all methods. However, our approach consistently maintain much higher performance even under strong interference than others. Regarding LPIPS metrics, only CAE, imRICnn, and our model exhibit decreasing trends because stronger interference presents more distinct and sparse features, enabling the model to more effectively identify, characterize, and separate interference components from the signal. Consequently, the purified output more closely resembles the original clean signal, resulting in lower LPIPS values.

## 4. CONCLUSION

This work introduces DiffRIM, a diffusion-based framework for efficient radar interference mitigation which enhances the interpretability of the approach by leveraging iterative diffusion and recover processes. A lightweight architecture integrating with STA, DualRes and ME/MD, enabling sparse spatio-temporal feature extraction while reducing overhead. To bridge the data availability gap, a large-scale synthetic dataset was crafted by integrating real radar captures with simulated interference patterns, thus providing accurate ground-truth. Comprehensive validation demonstrates state-ofthe-art performance on both synthetic and real-world benchmarks, validating the method’s efficiency in real-time inference capability and generalization. Results demonstrate superior noise suppression and target recovery without oversmoothing, supporting embedded deployment in autonomous systems. Future work will extend to multi-interferer scenarios to simulate more congested traffic.

## 5. REFERENCES

[1] Zhihuo Xu and Quan Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geoscience and Remote Sensing Letters, vol. 15, no. 1, pp. 137– 141, 2017.

[2] Alexander Fuchs, Johanna Rock, Mate Toth, Paul Meissner, and Franz Pernkopf, “Complex-valued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in 2021 IEEE Radar Conference (RadarConf21). IEEE, 2021, pp. 1–6.

[3] Seongwook Lee, Jung-Yong Lee, and Seong-Cheol Kim, “Mutual interference suppression using wavelet denoising in automotive fmcw radar systems,” IEEE Transactions on Intelligent Transportation Systems, vol. 22, no. 2, pp. 887–897, 2019.

[4] Mate Toth, Erik Leitinger, and Klaus Witrisal, “Variational signal separation for automotive radar interference mitigation,” IEEE Transactions on Radar Systems, 2024.

[5] Johanna Rock, Mate Toth, Paul Meissner, and Franz Pernkopf, “Cnns for interference mitigation and denoising in automotive radar using real-world data,” in Machine Learning for Autonomous Driving Workshop at the 33rd Conference on Neural Information Processing Systems (NeurIPS 2019), 2019, pp. 1–9.

[6] Yu Zhou, Ronggang Cao, Anqi Zhang, and Ping Li, “An interference mitigation method for fmcw radar based on time– frequency distribution and dual-domain fusion filtering,” Sensors, vol. 24, no. 11, pp. 3288, 2024.

[7] Ziang Zhang, Guangzhi Chen, Youlong Weng, Shunchuan Yang, Zhiyu Jia, and Jingxuan Chen, “Rimformer: An end-toend transformer for fmcw radar interference mitigation,” IEEE Transactions on Geoscience and Remote Sensing, 2024.

[8] Guoxuan Chi, Zheng Yang, Chenshu Wu, Jingao Xu, Yuchong Gao, Yunhao Liu, and Tony Xiao Han, “Rf-diffusion: Radio signal generation via time-frequency diffusion,” in Proceedings of the 30th Annual International Conference on Mobile Computing and Networking, 2024, pp. 77–92.

[9] Ethan Pronovost, Meghana Reddy Ganesina, Noureldin Hendy, Zeyu Wang, Andres Morales, Kai Wang, and Nick Roy, “Scenario diffusion: Controllable driving scenario generation with diffusion,” Advances in Neural Information Processing Systems, vol. 36, pp. 68873–68894, 2023.

[10] Stephen Alland, Wayne Stark, Murtaza Ali, and Manju Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 45–59, 2019.

[11] Canan Aydogdu, Gisela K Carvajal, Olof Eriksson, Hans Hellsten, Hans Herbertsson, Musa Furkan Keskin, Emil Nilsson, Mats Rydstrom, Karl Van ¨ as, and Henk Wymeersch, “Radar¨ interference mitigation for automated driving,” arXiv preprint arXiv:1909.09441, 2019.

[12] Markus Goppelt, H-L Blocher, and Wolfgang Menzel, “Au-¨ tomotive radar–investigation of mutual interference mechanisms,” Advances in Radio Science, vol. 8, pp. 55–60, 2010.

[13] PKA Vasu, J Gabriel, J Zhu, O Tuzel, and A Ranjan, “An improved one millisecond mobile backbone. arxiv 2022,” arXiv preprint arXiv:2206.04040, 2022.

[14] Diederik P Kingma and Max Welling, “Auto-encoding variational bayes,” arXiv preprint arXiv:1312.6114, 2013.

[15] Jiawei Liu, Qiang Wang, Huijie Fan, Yinong Wang, Yandong Tang, and Liangqiong Qu, “Residual denoising diffusion models,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2024, pp. 2773–2783.

[16] Teck-Yian Lim, Spencer A Markowitz, and Minh N Do, “Radical: A synchronized fmcw radar, depth, imu and rgb camera data dataset with low-level fmcw radar signals,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 941–953, 2021.

[17] Luis A Lopez-Valc ´ arcel, Manuel Garc ´ ´ıa Sanchez, Francesco ´ Fioranelli, and Oleg A Krasnov, “An mti-like approach for interference mitigation in fmcw radar systems,” IEEE Transactions on Aerospace and Electronic Systems, vol. 60, no. 2, pp. 1985–2000, 2023.

[18] Christoph Fischer, Untersuchungen zum interferenzverhalten automobiler radarsensorik, Cuvillier Verlag, 2016.

[19] Farokh Marvasti, Arash Amini, Farzan Haddadi, Mahdi Soltanolkotabi, Babak Hossein Khalaj, Akram Aldroubi, Saeid Sanei, and Janathon Chambers, “A unified approach to sparse signal processing,” EURASIP journal on advances in signal processing, vol. 2012, no. 1, pp. 44, 2012.

[20] Hao Wang, Lu Wang, Zhongyu Wang, Lixin Ma, and Ye Luo, “Ssc-vae: Structured sparse coding based variational autoencoder for detail preserved image reconstruction,” in Proceedings of the AAAI Conference on Artificial Intelligence, 2025, vol. 39, pp. 7665–7673.

[21] Ruibin Zhang, Donglai Xue, Yuhan Wang, Ruixu Geng, and Fei Gao, “Towards dense and accurate radar perception via efficient cross-modal diffusion model,” IEEE Robotics and Automation Letters, 2024.

[22] Nicolae-Cat˘ alin Ristea, Andrei Anghel, and Radu Tudor˘ Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153491– 153507, 2021.

[23] Marcio Luiz Lima de Oliveira and Marco Jan Gerrit Bekooij, “Deep convolutional autoencoder applied for noise reduction in range-doppler maps of fmcw radars,” in IEEE Radar Conference 2020. IEEE, 2020, pp. 630–635.

[24] Johanna Rock, Mate Toth, Elmar Messner, Paul Meissner, and Franz Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in 2019 22th International Conference on Information Fusion (FUSION). IEEE, 2019, pp. 1–8.

[25] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang, “The unreasonable effectiveness of deep features as a perceptual metric,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2018, pp. 586–595.

[26] Jianping Wang, “Cfar-based interference mitigation for fmcw automotive radar systems,” IEEE Transactions on Intelligent Transportation Systems, vol. 23, no. 8, pp. 12229–12238, 2021.