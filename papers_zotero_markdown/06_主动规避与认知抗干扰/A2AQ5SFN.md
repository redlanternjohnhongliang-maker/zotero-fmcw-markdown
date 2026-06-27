# Deep-Learning based Spectrum Prediction for Cognitive Automotive Radar Interference Mitigation

Marius Schwarz   
Bosch   
Corporate Research   
Renningen, Germany   
marius.schwarz@de.bosch.com

Axel Acosta Aponte

Bosch

Corporate Research\* Renningen, Germany axel.acosta@de.bosch.com

Gor Hakobyan   
Bosch   
Corporate Research   
Renningen, Germany   
gor.hakobyan@de.bosch.com

Abstract—Interference affects the robustness of driver assistance systems that rely on automotive radars. Today’s radar sensors use algorithms for suppression of interference in the received radar signal. In contrast, interference-aware cognitive radar (IACR) avoids interference based on spectral awareness, as opposed to suppressing it in post-processing. In this paper, we propose a machine learning (ML) based spectrum prediction model for IACR that infers the spectral occupation in the upcoming measurement cycle. Subsequently, interference is avoided by adapting the waveform to use the spectral resources with the least interference potential. By closing the cognitive loop, we show that IACR is capable of achieving an order of magnitude less average interference power compared to radars without a cognitive interference avoidance strategy.

Index Terms—cognitive radar, automotive radar, interference mitigation, deep learning, low-level radar AI

## I. INTRODUCTION

There is a growing share of vehicles on the road equipped with driver assistance functions for safety and comfort. Many of these functions rely on radars for surround sensing. With up to 12 radars being deployed in a single car, the cumulative number of radar sensors is growing substantially. Due to its active measurement principle, radars are susceptible to mutual interference when operating in the same environment. Radar interference poses a robustness issue for safetycritical driver assistance systems, as it can lead to reduced sensitivity to weak radar targets such as pedestrians. To avoid interference-induced performance degradation, interference mitigation measures are required.

Interference mitigation in state-of-the-art frequency modulated continuous wave (FMCW) automotive radars is done predominately in post-processing at the radar receiver [1], [2]. Such methods detect the corrupted samples in the timedomain signal based on a power detector and suppress interference by subtraction of the interference signal or dropping of the corrupted samples. These methods are effective for narrowband interference that affects a fraction of the radar time signal. However, with higher market penetration, rising modulation bandwidths and new wideband radar waveforms, spectral occupation increases, leading to more widespread interference in the radar signal. As a consequence, current interference suppression approaches become insufficient.

![](images/2be674f56a629c3c8a67dee85d3784686eceb1316f3711109af13923b27d3ce0.jpg)  
Fig. 1: Concept of the interference-aware cognitive radar

As interference is mutual in nature, interfering radars are affected on both ends, causing inevitable performance degeneration and requiring interference suppression for both systems. In contrast, avoidance of interference by one of the radars is sufficient to eliminate interference on both ends, and by that the need for post-processing. This makes the interferenceaware cognitive radar (IACR) concept proposed in [3] and shown in Fig. 1 an appealing solution for the radar interference problem. On the basis of sensed interference in the whole automotive radar band, the IACR predicts the spectrum occupation and identifies vacant spectral resources for interference-free waveform adaptation. In contrast to cooperation or rule based interference avoidance strategies, the cognitive adaptation of the IACR enables coexistence with legacy and non-cooperative radars [4].

A key component of IACR is the spectrum prediction module, which processes the information from the spectrum sensing block of the current spectral occupation and generates predictions of interfering radar modulations for the upcoming illumination cycle. In our work, we present an image-based deep neural network for prediction of the upcoming spectrum occupation pattern. We train the proposed model based on simulated interference scenarios using self-supervised learning (SSL). The predicted time-frequency images (TFI) are used by the waveform optimization module to obtain the illumination pattern with the least interference potential. We show that the proposed IACR approach is capable of interference mitigation by an order of magnitude in average interference power.

## II. RELATED WORK

The initial idea of cognitive radar was introduced by Haykin in [5], defined as an approach for improved target detection and tracking via cognitive adaptation based on the sensed environment. To this end, a receiver-transmitter feedback path is established to utilize sensed target information from previous measurements. Further works in [6] proposed the use of a sense-learn-adapt (SLA) cycle on multiple cognitive levels, such as fast interference mitigation on pulse-level timescale or long-acting radar scheduling. These works focus on the use of cognitive radar for improved radar sensing.

Another prevalent research field for cognitive radar is spectrum sharing. In [7]–[9], the idea of wireless systems and radars coexisting within joint frequency bands is studied. Both primary user (PU) and secondary user (SU) operate in the same spectrum, while the SUs (commonly radars) use the vacant spectral resources not utilized by PUs (e.g. communication systems). As the spectrum access of the PU may not be affected at any time, the SU needs to predict the future spectral occupation using a statistical modelling of the PU’s behavior.

With respect to spectrum sensing, a common approach in previous works is the discretization of the spectrum over time into sub-channels of the size of a single communication channel and constant time slots. In [10], a hidden markov model (HMM) is used to predict the occupation of a channel for the next time slot, given the sequence of the past channel utilization. More recently, [11] proposed an long short-term memory (LSTM) based deep neural network for predicting the interference power in a sub-channel multiple time slots ahead. A more end-to-end spectrum sharing approach is presented in [12]. The proposed reinforcement learning method adapts carrier frequency and bandwidth of the FMCW radar modulation based on the spectrum forecast of the LSTM to maximize the expected reward.

The IACR concept for interference avoidance in automotive radars is proposed in [3]. An efficient method for spectrum sensing is presented in [13], which allows sensing of several GHz of bandwidth at a tens of MHz of sampling rate. Based on the captured ${ \mathrm { T F I s } } ,$ the spectral prediction module generates a prediction of all sensors’ future behavior. In a last step, the waveform adaptation changes the radar’s waveform to mitigate interference. Whereas these works presented concepts for spectrum sensing [13] and waveform adaptation [3], no particular implementation for the spectrum interpretation module was proposed.

## III. SIMULATION BASED RADAR INTERFERENCE DATASETGENERATION

Our solution for spectrum prediction module is based on a deep neural network, which processes the TFIs of the past cycles captured by the spectrum sensing block and generates a prediction for the upcoming cycle. Since no measured dataset was available for this task, we created a radar interference simulation framework to generate a dataset of different interference scenarios. The dataset consists of a few seconds long simulation scenes with multiple simultaneous interferers in a highway scenario. For every radar measurement cycle, a TFI is generated based on the sweep-based spectrum sensing (SBSS) approach from [13]. These images serve for one as input for the spectrum prediction model, for the other at every time instance the upcoming TFI serves as ground truth (GT) during training. This results in a SSL approach, as no additional labeling is needed. The same approach can analogously be applied to recorded measurement data. The true spectral occupation is available for performance evaluation of the closed-loop IACR interference avoidance in Section VI.

## A. Radar Interference Simulation

As state-of-the-art automotive radars all use FMCW waveforms, the interference dataset is constructed for FMCW radars only, containing both slow chirp (SC) and chirp sequence (CS) modulations. A simple physical propagation model is used, which takes only the free-space attenuation on the line-of-sight (LoS) path into account. Further influences on the physical model, such as angular dependencies of the antenna gain, multipath propagation and other channel effects are neglected. The physical modeling of the interference scene contains the simulation of oncoming and ongoing cars including their range and velocity (see Fig. 2). These values are randomly drawn from Table I, with $\mathcal { U } _ { [ a , b ] }$ and ${ \mathcal { N } } \left( { \boldsymbol { \mu } } , \sigma ^ { 2 } \right)$ denoting the underlying uniform and normal probability distributions.

For the generation of simulation data, we define a radar codebook with 140 different modulation schemes containing SC and CS waveforms with random values within the limits defined in Table II.

TABLE I: Distribution of phsyical parameters of interferers
<table><tr><td>Interferers</td><td>Lane</td><td> $P _ { \mathrm { l a n e } }$ </td><td>Range [m]</td><td>Velocity[m/s]</td></tr><tr><td> $N \sim [ 1 , 3 ]$ </td><td>oncoming same</td><td>0.5 0.5</td><td> $\mathcal { U } _ { [ 1 5 , 1 2 0 ] }$   $\tilde { \mathcal { N } } ( \tilde { 5 } 5 , \tilde { 1 0 } )$ </td><td> $\mathcal { N } \left( - 5 0 , 6 . 6 7 \right)$   $\mathcal { N } ( 0 , 3 . 3 3 )$ </td></tr></table>

TABLE II: Modulation parameters of interferers
<table><tr><td>Modulation parameter</td><td>Min</td><td>Max</td></tr><tr><td>Detection period  $T _ { \mathrm { d e t } }$  [ms]</td><td>8</td><td>20</td></tr><tr><td>Processing period  $T _ { \mathrm { p r o c } }$  [ms]</td><td>30</td><td>40</td></tr><tr><td>Bandwidth  $\bar { B } _ { \mathrm { i n t } }$  [MHz]</td><td>100</td><td>2000</td></tr><tr><td>Transmit power  $P _ { \mathrm { T X } }$  [dBm]</td><td>20</td><td>40</td></tr></table>

![](images/cd70d910a0a8f84a996770153346acd6ff51e22f9d210a88ef911da8d4e73f98.jpg)  
Fig. 2: Radar interference scene

## B. Spectrum Sensing

For cost-efficient spectrum sensing, we use the SBSS method from [13]. To model the influence of the hardware components at the receiver, the simulated interference signal is amplified by the receiver antenna gain $G _ { \mathrm { R x } }$ and overlaid with Gaussian noise according to the receiver noise figure $N _ { \mathrm { F , R x } }$ . The resulting received signal is processed by mixing with a local oscillator (LO) signal that sweeps linearly the entire operational bandwidth, followed by a low-pass filtering to reduce the sampling rate of the analog-to-digital converter (ADC). By correlation of the sampled baseband signal with a bank of matched filters tuned to different FMCW slopes, a pulse compression of the interference at its corresponding frequency of intersection with the LO sweep is achieved. Subsequently, the best matching slope for every frequency cell is used to obtain a spectral image for the current sweep. By sensing a sequence of such sweeps over time, a TFI of the current spectral occupation is obtained.

TABLE III: SBSS parameters
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Sweep bandwidth  $B _ { \mathrm { s w e e p } }$ </td><td>3GHz</td></tr><tr><td>Sweep duration  $T _ { \mathrm { s w e e p } }$ </td><td>49 μs</td></tr><tr><td>LPF cutoff frequency  $f _ { \mathrm { c u t } }$ </td><td>40 MHz</td></tr><tr><td>Receiver antenna gain  $G _ { \mathrm { R x } }$ </td><td>10 dB</td></tr><tr><td>Receiver noise figure  $N _ { \mathrm { F , R x } }$ </td><td>15 dB</td></tr></table>

Based on the parametrization from Table III, the SBSS yields TFIs of the size $1 9 6 0 \times 1 0 0 0$ . Subsequently, these images are converted into logarithmic scale and clipped to an interval from −100 dB to −70 dB.

## C. Dataset Generation

The generated simulation dataset encompass 980 independent interference scenarios with up to three simultaneous interfering sensors from the radar codebook with varying range and velocity. Each interference scenario sample contains 10 TFIs of size $T _ { \mathrm { w i n } }$ after SBSS. Due to the lower chirp slopes and durations of SC radars, the individual chirps including bandwidth and duration are fully resolved, whereas CS modulation results in an undersampled image (see Fig 3).

## D. Simplified Dataset

Due to a high computational complexity of the radar simulation, the feasible size of a simulative generated dataset is limited. To facilitate convergence of the neural network, we generated a simplified dataset with more samples but limited modeling complexity. Instead of a baseband interference simulation, TFIs are generated directly by assuming linear or rectangular shapes for sensed SC and CS modulations, respectively. Further, no receiver noise and a constant interferer power within a scenario is assumed. Thus, a larger simplified dataset containing 82,000 independent scenarios with similar interferer parameters is generated in a fraction of the time (∼ 40 ms vs. 240 s computation time for one scenario with three interferers compared to full baseband simulation).

## IV. DL-BASED SPECTRUM PREDICTION

In contrast to the stochastic communication channel utilization in [7], [10], the spectral resource occupation of conventional automotive radars can be considered deterministic. Typically, sensors have a constant cycle duration comprising measurement and processing periods, i.e. a duty cycle. By inferring modulation parameters of the interferer, including its update rate from previous measurement cycles, prediction of the spectral occupation in the upcoming measurement cycle is possible. To this end, we pursue an end-to-end approach based on a deep neural network, as detailed below.

![](images/51e970452360a1b9a68ac6798c936a7bfa369b56a827ed8209a863b49ef2a77b.jpg)

(a) SC interferer  
![](images/799f05e1becf2ef52dba10eb16c56cd8b5372a801c3b70fcfb7e73e2973c9312.jpg)  
(b) CS interferer  
Fig. 3: Interferers with 500 MHz modulation bandwidth after SBSS

## A. Data Preprocessing

To reduce the input size for the neural network, we first downsample the TFI using $5 \times 1$ average pooling and $8 \times 4 0$ max pooling in both dimensions, which yields an image of size $4 9 \times 2 5$ . We further apply input normalization, by scaling the dB power values of the reduced TFI to the interval $[ 0 , 1 ]$ . To incorporate the history from the previous cycles, four reduced TFIs are concatenated along the temporal dimension forming a single reduced TFI of a size $4 9 \times 1 0 0$ and incorporating the history of the last 196 ms.

## B. Network Architecture

We propose an image-based encoder-decoder architecture for spectrum prediction. Similar to deep learning (DL) concepts for next-frame video prediction [15], [16] and image extrapolation [17], the proposed deep encoder-decoder architecture illustrated in Fig. 4 generates a high-abstractionlevel prediction in the latent space. By encoding the merged input TFI, larger scale dependencies are extracted that are not observable on a single TFI level. The encoder used for feature extraction is an adapted version of the ResNet18 architecture [18], [19]. In the latent space, the encoder feature vector is forwarded to three fully connected layers with rectified linear unit (ReLu) activation, which performs the prediction of the upcoming spectral image. Subsequently, the decoder transforms the latent space vector into a gray scale prediction of the upcoming TFI. The decoder consists of five transposed convolutional layers with a kernel size of $K _ { \mathrm { k e r n } } = 3$ with a ReLU activation and a single transposed convolutional layer with a kernel size of $K _ { \mathrm { k e r n } } ~ = ~ 1$ and a sigmoid activation. The model was implemented in Python using the TensorFlow platform [20] with Keras API [21].

![](images/374bdc3d10210ea34d38b101e06508dc6297e04ad410e2f2f6ff2d9f2913def9.jpg)  
Fig. 4: Visualization of neural spectrum prediction architecture using [14]

## C. Model Training

For training, simplified and simulation datasets are both split into train/validation/test by the ratio 0.8/0.1/0.1. We use a hierarchical model training in three steps, with fine-tuning in between each training step. First, the model is trained for 100 epochs on the simplified training dataset, whereas the simulated interference intensity is discarded and only training for binary resource occupation prediction is done. To enable thin contours in the predicted image for SC modulations, a loss term for crisp edge prediction [22] based on the commonly used Dice coefficients is used:

$$
L _ { \mathrm { c r i s p } } \left( y , \hat { y } \right) = \frac { \sum _ { i } ^ { N _ { \mathrm { t o t } } } y _ { i } ^ { 2 } + \sum _ { i } ^ { N _ { \mathrm { t o t } } } \hat { y } _ { i } ^ { 2 } } { 2 \sum _ { i } ^ { N _ { \mathrm { t o t } } } y _ { i } \hat { y } _ { i } } ,\tag{1}
$$

where $y _ { i }$ and $\hat { y } _ { i }$ denote the pixel values of the observed and predicted spectrum y and yˆ, respectively. For compensating the unequal distribution of occupied and vacant spectral resources, the loss function of the model optimization is selected to be:

$$
{ \cal L } _ { \mathrm { C W B C E } } \left( y , \hat { y } \right) = \lambda \cdot { \cal L } _ { \mathrm { W B C E } } \left( y , \hat { y } \right) + { \cal L } _ { \mathrm { c r i s p } } \left( y , \hat { y } \right) ,\tag{2}
$$

with $\boldsymbol { L } _ { \mathrm { W B C E } } \left( \boldsymbol { y } , \boldsymbol { \hat { y } } \right)$ being the batch-wise calculated weighted binary cross entropy (WBCE) and $\lambda = 0 . 1$

In a second step, the model is fine-tuned on the regular simplified dataset for 80 epochs. Finally, the pre-trained model is trained on the simulation dataset for 120 epochs. All training steps are carried out with a batch size of 16, using the Adam optimizer and a learning rate of 0.001.

## V. WAVEFORM ADAPTATION FOR IACR

The final step in the IACR cognitive loop is the waveform optimization based on the predicted spectrum. In this work, we consider the own radar to use CS modulation. The methods used for CS waveform adaptation are adopted from [3]. With respect to optimization strategy, we use a simple grid-search over the frequency, starting time, and slope of the own CS waveform. Both the adaptation methods and optimization strategy are summarized below.

## A. Adaptation Methods

Carrier frequency: The center frequency of the radar modulation is adapted over the available frequency band. Since the available bandwidth is much smaller than the carrier frequency, the radar sensing performance remains vastly unaffected [3].

• Linear frequency adaptation: Adaptation of the center frequency of each chirp in the CS waveform by equidistant shifts. This adaptation has implications on the range-Doppler sensing characteristics, although the increased bandwidth is in fact favorable for the radar range resolution.

• Starting time: Shift of the modulation start within the fixed duty cycle. This results in a non-equidistant measurement cycles, although the update rate is kept same, i.e. there is a measurement in every fixed-length cycle.

## B. Optimization Strategy

Based on the predicted TFI of the upcoming cycle, a metric to quantify the interference power for every waveform choice is needed. We define the cumulated interference within the time-frequency space occupied by the radar waveform as mean interference intensity (MII):

$$
I _ { \mathrm { M I I } } = \frac { 1 } { \sum _ { h = 1 } ^ { H } \sum _ { w = 1 } ^ { W } m _ { h , w } } \sum _ { h = 1 } ^ { H } \sum _ { w = 1 } ^ { W } m _ { h , w } \cdot p _ { h , w } ,\tag{3}
$$

where $m _ { h , w } \in \{ 0 , 1 \}$ is the binary mask of occupied resources for the waveform adaptation and $p _ { h , w } \in [ 0 , 1 ]$ is the normalized interference intensity of a pixel. W and H denote the number of pixels in the spectral image in x and y dimension.

![](images/a33aa50f130a8e4c7a9a2856e39f1ca2484a20afe05c11b873ae0d0a45b8fa6f.jpg)  
(a) Input sequence

![](images/37e268a018ae8f37f08f8dd65d99da5e56d4cfb086d9a0770f6e1f98c43a0c54.jpg)  
Time (ms)  
(b) Prediction

![](images/02d0de9967bbf000996f91f2b67c86250507ab42f84add3c4e969bbd3f6d785b.jpg)  
Time (ms)  
(c) Error

![](images/cd8aa91e1bea2079b2f451f5bc5de07805fdf4d8cbb206f028cf76019447bc6e.jpg)  
Time (ms)  
(d) GT + Adaptation  
Fig. 5: Spectrum prediction and waveform adaptation for an CS modulation with 500 MHz bandwidth on simulation data

The optimal adaptation $( x _ { i } , y _ { i } , \alpha _ { i } )$ is then obtained by a gridsearch minimization of the MII as depicted in Fig 6. The grid size is chosen to be one pixel in x and y dimension and $\alpha = 1 0 ^ { \circ }$ in angular dimensions for the intra-modulation linear frequency adaptation.

## VI. SIMULATION RESULTS

## A. Next Cycle Interference Prediction Performance

For quantitative analysis of the proposed spectrum prediction, the generated TFIs of the upcoming cycle can be evaluated by the similarity to the actually observed spectrum. To this end, we use the following three metrics: the structural similarity index measure (SSIM), peak signal-to-noise ratio (PSNR) and the mean squared error (MSE) between the two images. All trainings are performed on a NVIDIA V100 graphics processing unit (GPU). The inference time for a batch size of six takes approximately 30 ms.

Table IV shows the results on the test datasets for each training step of the hierarchical training. Clearly, models trained from scratch have a substantially lower performance in all examined metrics as compared to the ones that use hierarchical training. Specifically, the model trained on simplified data profits from using pre-trained weights. Although in both cases models are trained until convergence, the fine-tuning approach obtains better performance based on a domain-specific learning gain. Furthermore, overfitting in training adversely affects the SSIM due to increasing sharpness of generated TFIs.

TABLE IV: Evaluation DL-based spectrum predictor
<table><tr><td>Datasets:</td><td>Training:</td><td>SSIM</td><td>PSNR [dB]</td><td>MSE</td></tr><tr><td>Binary synth. dataset</td><td>scratch</td><td>0.786</td><td>15.21</td><td>0.0354</td></tr><tr><td rowspan="2">Simplified dataset</td><td>scratch</td><td>0.768</td><td>19.05</td><td>0.0156</td></tr><tr><td>pre-trained</td><td>0.795</td><td>19.51</td><td>0.0140</td></tr><tr><td rowspan="2">Simulation dataset</td><td>scratch</td><td>0.455</td><td>19.39</td><td>0.0160</td></tr><tr><td>pre-trained</td><td>0.597</td><td>21.86</td><td>0.0095</td></tr></table>

## B. Closed-Loop IACR Performance Analysis

Fig. 5 shows qualitatively the individual steps of the cognitive cycle for a scenario with two interfering CS radars.

![](images/70e97f6ff791772c443ed9245c25e79c24efe5c3b74ab94a702bdf7bb1f43ae3.jpg)  
Fig. 6: Waveform parameter optimization

Based on the predicted spectrum, the own modulation (orange) is adapted to minimize interference in the next cycle. The brightness of the green and red pixels in Fig. 5c corresponds to the matching of prediction and GT intensities for truly and falsely forecast interference shapes, respectively.

For quantitative performance evaluation of closed-loop IACR with respect to its interference mitigation capability, Fig. 7 compares the MII for cognitive waveform adaptation to static and random waveform choice. The optimal interference mitigation limit is depicted by a waveform adaptation on GT data. We set the measurement duration of the modulation to $T _ { \mathrm { m e a s } } = 1 9 . 2 \ : \mathrm { m s }$ . The performance is presented over a different number of interferers for two radar bandwidths: 500 MHz and 2000 MHz. The total available operational bandwidth is 3 GHz and the adaptation time window is $T _ { \mathrm { w i n } } ~ = ~ 4 9$ ms. The simulation encompass 200 samples for each number of interferers for up to 7 simultaneous interferers in a single scene. MII is evaluated based on the noiseless GT spectrum, while the prediction is generated on basis of the noisy sensed spectrum.

Clearly, IACR avoids interference by an order of magnitude for all considered scenes for the 500 MHz bandwidth configuration. Whereas for a low spectral occupation (1-3 interferers) a high probability of interference-free operation is obtained, even for seven simultaneous interferers, the MII reduces by approximately a factor of 16 on average. Even for the configuration that uses 2000 MHz out of the total

![](images/dccdaaf762869a14d371e69f91ebeb98cd607d5e7375d83ff37798b28cac5f96.jpg)

(a) MII simulation for 500 MHz modulation bandwidth  
![](images/b43e5123c929ffdf54969c7fadd1fabedd185bc21692062e9a3c0ac82316a77e.jpg)  
(b) MII simulation for 2000 MHz modulation bandwidth  
Fig. 7: MII evaluation over different number of interferers

3000 MHz, a substantial interference mitigation is achieved, including for the heavily crowded scenes. Furthermore, since during training only scenarios with three simultaneous interferers were used, the model is able to generalize to a higher number of interferers. The rather small deviation of IACR from the optimum waveform adaptation on GT data indicates the reliability of the interference prediction. However, it needs to be noted that increasing spectral occupation leads to less precise forecasts, which is seen based on increasing deviation from the optimum in Fig. 7.

## VII. CONCLUSION

We proposed a deep neural encoder-decoder architecture for spectrum prediction for IACR. The presented image-based prediction model is trained in a self-supervised manner based on simulated radar interference dataset. The cognitive cycle was closed using an optimization algorithm for adaptation of the ego modulation in the upcoming measurement cycle. The closed-loop performance evaluation shows a reduction of the MII up to an order of magnitude for IACR in comparison to baseline approaches. Moreover, the concept is compatible with legacy sensors. Conventional, non-adaptive radars on the roads profit from the reduction of mutual interference.

## REFERENCES

[1] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: Modulation schemes and interference mitigation,” IEEE Microwave Magazine, vol. 20, no. 9, pp. 58–72, 2019.

[2] C. Fischer, H. L. Blcher, J. Dickmann, and W. Menzel, “Robust detection and mitigation of mutual interference in automotive radar,” in 2015 16th International Radar Symposium (IRS), 2015, pp. 143–148.

[3] G. Hakobyan, K. Armanious, and B. Yang, “Interference-aware cognitive radar: A remedy to the automotive interference problem,” IEEE Transactions on Aerospace and Electronic Systems, vol. 56, no. 3, pp. 2326–2339, 2020.

[4] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 32–44, 2019.

[5] S. Haykin, “Cognitive radar: a way of the future,” IEEE Signal Processing Magazine, vol. 23, no. 1, pp. 30–40, 2006.

[6] J. R. Guerci, R. M. Guerci, M. Ranagaswamy, J. S. Bergin, and M. C. Wicks, “Cofar: Cognitive fully adaptive radar,” in 2014 IEEE Radar Conference, 2014, pp. 0984–0989.

[7] M. S. Greco, F. Gini, and P. Stinco, “Cognitive radars: Some applications,” in 2016 IEEE Global Conference on Signal and Information Processing (GlobalSIP), 2016, pp. 1077–1082.

[8] A. F. Martone, K. D. Sherbondy, J. A. Kovarskiy, B. H. Kirk, R. M. Narayanan, C. E. Thornton, R. M. Buehrer, J. W. Owen, B. Ravenscroft, S. Blunt, A. Egbert, A. Goad, and C. Baylis, “Closing the loop on cognitive radar for spectrum sharing,” IEEE Aerospace and Electronic Systems Magazine, vol. 36, no. 9, pp. 44–55, 2021.

[9] C. E. Thornton, M. A. Kozy, R. M. Buehrer, A. F. Martone, and K. D. Sherbondy, “Deep reinforcement learning control for radar detection and tracking in congested spectral environments,” IEEE Transactions on Cognitive Communications and Networking, vol. 6, no. 4, pp. 1335– 1349, 2020.

[10] P. Stinco, M. S. Greco, and F. Gini, “Spectrum sensing and sharing for cognitive radars,” IET Radar, Sonar & Navigation, vol. 10, no. 3, pp. 595–602, 2016. [Online]. Available: https://ietresearch.onlinelibrary.wiley.com/doi/abs/10.1049/ietrsn.2015.0372

[11] B. S. Shawel, D. Hailemariam Woledegebre, and S. Pollin, “Deeplearning based cooperative spectrum prediction for cognitive networks,” in 2018 International Conference on Information and Communication Technology Convergence (ICTC), 2018, pp. 133–137.

[12] C. E. Thornton, M. A. Kozy, R. M. Buehrer, A. F. Martone, and K. D. Sherbondy, “Deep reinforcement learning control for radar detection and tracking in congested spectral environments,” IEEE Transactions on Cognitive Communications and Networking, vol. 6, no. 4, pp. 1335– 1349, 2020.

[13] G. Hakobyan, M. Fink, A. Soyolyn, N. Mansour, and D. Dahlhaus, “Sweep-based spectrum sensing method for interference-aware cognitive automotive radar,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–6.

[14] H. Iqbal, “Harisiqbal88/plotneuralnet v1.0.0,” Dec. 2018. [Online]. Available: https://doi.org/10.5281/zenodo.2526396

[15] S. Oprea, P. Martinez-Gonzalez, A. Garcia-Garcia, J. A. Castro-Vargas, S. Orts-Escolano, J. Garcia-Rodriguez, and A. Argyros, “A review on deep learning techniques for video prediction,” IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 44, no. 6, pp. 2806– 2826, 2022.

[16] Y. Zhou, H. Dong, and A. El Saddik, “Deep learning in next-frame prediction: A benchmark review,” IEEE Access, vol. 8, pp. 69 273– 69 283, 2020.

[17] Y. Wang, X. Tao, X. Shen, and J. Jia, “Wide-context semantic image extrapolation,” in 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 1399–1408.

[18] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” 2015. [Online]. Available: https://arxiv.org/abs/1512.03385

[19] J. Wu, “resnet18-tf2,” GitHub Accessed May 1, 2022. [Online]. Available: https://github.com/jimmyyhwu/resnet18-tf2

[20] M. Abadi, A. Agarwal, P. Barham, E. Brevdo, Z. Chen, C. Citro, and G. S. Corrado, “TensorFlow: Large-scale machine learning on heterogeneous systems,” 2015, software available from tensorflow.org. [Online]. Available: https://www.tensorflow.org/

[21] F. Chollet et al. (2015) Keras. [Online]. Available: https://github.com/fchollet/keras

[22] R. Deng, C. Shen, S. Liu, H. Wang, and X. Liu, “Learning to predict crisp boundaries,” 2018. [Online]. Available: https://arxiv.org/abs/1807.10097