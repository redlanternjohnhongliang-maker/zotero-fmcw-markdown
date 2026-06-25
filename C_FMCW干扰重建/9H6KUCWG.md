# Autoregressive Model-Based Signal Reconstruction for Automotive Radar Interference Mitigation

Muhammad Rameez , , Mattias Dahl , , and Mats I. Pettersson ,

—Automotive radars have become an important part of sensing systems in vehicles and other traffic applications due to their accuracy, compact design, and robustness under severe light and weather conditions. The increased use of radars in various traffic applications has given rise to the problem of mutual interference, which needs to be mitigated. In this paper, we investigate interference mitigation in chirp sequence (CS) automotive radars via signal reconstruction based on autoregressive (AR) models in fast- and slowtime. The interference is mitigated by replacing the disturbed baseband signal samples with samples predicted using the estimated AR models. Measurements from 77 GHz frequency modulated continuous wave (FMCW) static and moving radars

![](images/305ccd9f4ff618d77a9459377aee31f280b8c160fd91a704906738c908a0092d.jpg)

are used to evaluate the signal reconstruction performance in terms of the signal-to-interference-plus-noise ratio (SINR), peak side-lobe level (PSLL), and mean squared error (MSE). The results show that the interference is suppressed down to the general noise floor, leading to an improvement in the SINR. Additionally, enhanced side-lobe suppression is achieved via AR signal reconstruction, which is compared to a commonly used inverse-cosine method. Furthermore, the paper notes that the slow-time signal reconstruction can be more beneficial for interference suppression in certain scenarios.

— Automotive radar, autoregressive (AR) modeling, chirp sequence (CS), frequency modulated continuous wave (FMCW), interference mitigation, signal reconstruction.

## I. INTRODUCTION

UTOMOTIVE radars are being increasingly employed in a variety of safety-critical advanced driver assistance systems (ADASs), e.g., automatic emergency braking (AEB), blind spot detection (BSD) and adaptive cruise control (ACC) [1]. In addition, these radars are being utilized in a number of security applications, e.g., for the surveillance of railroad crossings and buildings [2]. Due to the increasing number of radars in traffic and their limited operating frequency range (76-77 GHz for long-range and 77-81 GHz for short-range applications [3]–[5]), it has become more likely to end up in scenarios where multiple radar sensors are transmitting simultaneously and therefore interfering with each other. This interference results in reduced detection capabilities for the ego radar [6], and this performance degradation is more severe for far-distance or low back-scattering targets such

as pedestrians and cyclists [7]. For the safety of road users, interference from other radars operating in the same vicinity should be eliminated [8].

Several automotive radar interference mitigation methods have been proposed in recent years [9]. These methods can be classified into those operating at either the transmitter (TX) or the receiver (RX) end. Random chirp frequency hopping [10], bats-inspired frequency hopping [11], and PN-coded frequency modulated continuous wave (FMCW) radar signals [12] are some of the interference mitigation techniques that work mainly at the TX end. For these techniques, the radar system needs to have a built-in ability to transmit chirp signals of varying center frequency, bandwidth, and duration. In addition, radar communication (at both the TX and RX ends) has also been proposed as a method to avoid mutual interference [13], [14].

At the RX end, it is possible to mitigate the effect of interference by applying signal processing methods on the received signal. If antenna arrays are available, then interference can be suppressed in the spatial domain by using digital beamforming [15]–[17]. Interference can also be suppressed in the time domain by detecting and zeroing out the disturbed samples in the received signal [18]. A similar method is to apply an inverse raised cosine window on the disturbed section to suppress interference and smooth out For more information, see https://creativecommons.org/licenses/by/4.0/ discontinuities in the resulting time-domain signal [19]. Mitigation of interference by reconstructing the disturbed samples of the time-domain baseband signal by employing Kalman filtering is presented in [20]. Further interference mitigation techniques in the signal processing domain include simultaneous detection and mitigation using signal separation (decomposition) methods [21]–[23], comparison of the frequency spectra of multiple chirps [24], adaptive noise cancellation by comparing the positive and negative halves of the frequency spectrum [25], and deep learning methods [26], [27].

Signal modeling has also been used for FMCW radar interference mitigation. In [28], the received baseband signal is modeled as a sum of sinusoids. The model parameters (weights of the sinusoids) are determined using an adaptive method, and one-step prediction is recursively used to extrapolate the signal over the disturbed part to mitigate interference. Recently, autoregressive (AR) modeling has been used for reconstructing disturbed parts of the received baseband signal in the short-time Fourier transform (STFT) domain (in an X-band FMCW radar) [29] and in the time domain (in an automotive radar) [30], [31].

Current automotive radars generally use a chirp sequence waveform, and the received signal corresponding to a block of chirps is coherently related both in fast-time (the time within a single chirp) and slow-time (the time across chirps in a coherent processing interval). There is a clear indication in [28]–[31] that good interference mitigation performance can be achieved by signal reconstruction using AR modeling. However, to our knowledge, signal reconstruction in slow-time has not been investigated for automotive radar interference mitigation. In this work, we compare and evaluate the interference mitigation and signal reconstruction performance using AR modeling in fast- and slow-time with the help of real measurements from static and moving radars. Furthermore, we propose an AR model selection and parameter estimation methodology suited for signal reconstruction in FMCW automotive radars. The focus is sample prediction and how the prediction performance can be improved by choosing an appropriate model estimation dimension.

The main contributions of our work are listed below

-- In this work, a unique method using slow-time signal reconstruction for interference mitigation is presented. The method is evaluated using both simulation and experimental data. In previous works, AR model-based signal reconstruction techniques for automotive radar interference suppression are limited to fast-time signal reconstruction.

-- A comparison between fast-time and slow-time signal reconstruction is presented.

-- The proposed method is evaluated for dynamic scenarios, i.e., cases with static and moving radars as well as targets.

-- A systematic approach for interference suppression suited for FMCW automotive radars is proposed that includes the following steps: Interference detection, AR model order estimation, AR coefficients estimation, and estimation of final prediction values from forward and backward prediction values.

![](images/88722286def4fcc9d46361f511a09438bf61b1c22b48879044615fdf2fb3a6c4.jpg)  
(a)

![](images/8fcee5738ae1ce1485f838bf1e53b59dd32dab14255d0ac1c71bda42706475c8.jpg)  
(b)  
Fig. 1. Frequency ( ) vs time ( ) plot of transmitted ( ) and interfering $( - )$ chirps with identical parameters. τ is the time shift between the transmitted and interfering signals. The dashed lines above and below the TX chirp indicate the receiver’s bandwidth $B _ { \mathsf { R } \mathsf { X } }$ , which also determines the maximum time shift $\tau _ { \mathsf { m a x } }$ between the chirps for the appearance of ghost targets. (a) The interfering chirp falls within the receiver’s bandwidth and results in a ghost target. (b) The interfering chirp falls outside the receiver’s bandwidth. No interference is observed in the baseband signal.

In the next section, (Section II), we describe the mutual interference in chirp sequence radars followed by the signal model description in Section III. Subsequently, the interference mitigation and signal reconstruction methodology is presented in Section IV.

## II. MUTUAL INTERFERENCE

Automotive radars generally employ a chirp-sequence FMCW signal. Interference occurs when multiple radars transmit in the same time interval and there is a frequency overlap between the transmitted signals [6]. Different transmit chirp parameters (chirp duration T , center frequency $f _ { c }$ and bandwidth B) result in different interference properties (Fig. 1 and 2). When the transmitted and interfering chirps have identical parameters, there are two possibilities

-- Ghost targets appear when an interfering chirp falls within the receiver’s bandwidth (Fig. 1a).

-- No interference is observed when the interfering chirp falls outside the receiver’s bandwidth (Fig. 1b).

The probability of the appearance of ghost targets is low because the time window $\tau _ { \mathrm { m a x } }$ for the interfering chirp to fall within the receiver’s bandwidth is very small compared to the pulse repetition time T (Fig. 1) [6].

Interference is more probable when transmitting signals from interfering radars have nonidentical parameters $( \mathrm { F i g . } 2 )$ . This interference results in a time-limited disturbance in the received baseband signal [7]. The duration of

![](images/42e500fa8b4e54b7e699b3e49f65f9e385576187f06c19e180813f23ee5265bb.jpg)  
(a)

![](images/79d537a1c7b447dfe50f962eaae0c3269d3a30a8083acdf6fc585f125b95c624.jpg)  
Fig. 2. Radars with nonidentical transmit ( ) and interfering $( - )$ chirps. The area highlighted by the rectangles shows the interference duration $\tau _ { d } .$ (a) Large difference between transmitted chirp slopes of the two interfering radars. (b) Small difference between transmitted chirp slopes of the two interfering radars.

this disturbance

$$
T _ { d } = \frac { 2 \cdot B _ { \mathrm { R X } } } { \left| \frac { B } { T } - \frac { B _ { \mathrm { i n t } } } { T _ { \mathrm { i n t } } } \right| }\tag{1}
$$

is inversely proportional to the difference in the slopes of the interfering chirp signals. Here, $B _ { \mathrm { R X } }$ is the receiver’s bandwidth, determined by a low-pass anti-aliasing filter in the radar receiver. $B _ { \mathrm { i n t } }$ is the interfering chirp’s bandwidth, and $T _ { \mathrm { i n t } }$ is the interfering chirp’s duration. The noise in the baseband signal increases as a consequence of this disturbance, leading to a degradation in the ego radar’s detection performance.

## III. SIGNAL MODEL

The time-domain baseband signal is obtained by mixing the received radio frequency (RF) signal with the transmitted signal and passing the output through an anti-aliasing lowpass filter in the radar receiver. In the presence of interference, the time-domain baseband signal

$$
x _ { b } ( t ) = x _ { e } ( t ) + x _ { \mathrm { i n t } } ( t ) + n _ { 0 } ( t )\tag{2}
$$

consists of target echoes $x _ { e } ( t )$ , an interfering signal $x _ { \mathrm { i n t } } ( t )$ , and the receiver’s noise contribution $n _ { 0 } ( t )$ . The signal component corresponding to the echoes from k targets is defined as

$$
x _ { e } ( t ) = \sum _ { i = 1 } ^ { k } A _ { e , i } \cos \big ( 2 \pi \big ( \frac { 2 f _ { c } R _ { i } } { c } + \big ( \frac { 2 f _ { c } \upsilon _ { i } } { c } + \frac { 2 B R _ { i } } { T c } \big ) t \big ) \big ) ,\tag{3}
$$

where $c$ is the speed of light. $A _ { e , i } , \ R _ { i }$ and $v _ { i }$ are the signal amplitude, range and relative radial velocity corresponding to

the $i ^ { t h }$ target, respectively. During the interference interval $T _ { d }$ the signal contribution by an interfering source is

$$
\begin{array} { r l r } {  { x _ { \mathrm { i n t } } ( t ) = A _ { \mathrm { i n t } } \cos { ( 2 \pi ( ( f _ { \mathrm { i n t } } - f _ { c } ) t + \frac { 1 } { 2 } \big ( \frac { B _ { \mathrm { i n t } } } { T _ { \mathrm { i n t } } } - \frac { B } { T } \big ) t ^ { 2 }  } } } \\ & { } & { \quad \quad \quad \quad \quad \quad \quad \quad \quad  + \big ( \frac { B } { T } \tau - \frac { B _ { \mathrm { i n t } } } { T _ { \mathrm { i n t } } } \tau _ { \mathrm { i n t } } \big ) t ) + \Phi _ { \mathrm { i n t } } \big ) , } \end{array}\tag{4}
$$

where $A _ { \mathrm { i n t } }$ is the signal amplitude, $f _ { \mathrm { i n t } }$ is the center frequency of the interfering chirp, $\tau _ { \mathrm { i n t } }$ is the time delay between the start of the transmitted and interfering chirps, and $\Phi _ { \mathrm { i n t } }$ is the difference between the initial phases of the transmitted and interfering chirps [32].

The sampled baseband signal corresponding to the $m ^ { t h }$ chirp is represented as a vector of length $N .$

$$
\begin{array} { r } { \mathbf { x } _ { b , m } = \left[ x _ { b , m } ( 1 ) \quad \ldots \quad x _ { b , m } ( n ) \quad \ldots \quad x _ { b , m } ( N ) \right] . } \end{array}\tag{5}
$$

If M chirps are transmitted, then the baseband signal frame

$$
\mathbf { X } _ { b } = \left[ \begin{array} { c c c } { x _ { b , 1 } ( 1 ) } & { \hdots } & { x _ { b , 1 } ( N ) } \\ { x _ { b , 2 } ( 1 ) } & { \hdots } & { x _ { b , 2 } ( N ) } \\ { \vdots } & { \ddots } & { \vdots } \\ { x _ { b , M } ( 1 ) } & { \hdots } & { x _ { b , M } ( N ) } \end{array} \right]\tag{6}
$$

takes the form of a two-dimensional $M \times N$ matrix.

The samples in each row and column of the matrix above are also referred to as fast-time and slow-time samples, respectively. In further processing, a two-dimensional discrete Fourier transform (DFT) of the baseband signal frame is performed. The peaks in the resulting matrix (also known as the range-Doppler matrix) ideally correspond to the target ranges and velocities [33].

## IV. METHODOLOGY

The first step in interference mitigation is the detection of disturbed samples in the baseband signal. The interference that results in a significant reduction in the SINR has a higher power than that of the signal scattered by the targets of interest [7]. Moreover, beat frequencies ranging from $- { B } _ { \mathrm { R x } }$ to $B _ { \mathrm { R x } }$ are added to the baseband signal when a wideband interference is superimposed on this signal, resulting in a high variation in the amplitude of the baseband signal $\mathbf { X } _ { b , m }$ in the interval $T _ { d }$ . Therefore, it is possible to detect the interference by identifying baseband signal sections with high amplitude variations [34]. The high variations in the sampled baseband signal are detected by comparing the absolute value of the first-order difference

$$
d _ { x , m } ( n ) = x _ { b , m } ( n ) - x _ { b , m } ( n - 1 ) , ~ 2 \leq n \leq N ,\tag{7}
$$

with a threshold $\lambda _ { i }$ , which is based on the mean value of $| d _ { x , m } ( n ) |$ . The main advantage of this detector is that it works even for relatively low-power interfering signals [34] (Fig. 3).

After interference detection, the interfered samples are discarded from the baseband signal frame $\mathbf { X } _ { b }$ . Removing interfered samples in the time domain introduces discontinuities in the baseband signal frame, which results in the appearance of high side lobes in the corresponding radar image in the range-Doppler domain. In [19], these discontinuities are removed by utilizing an inverse-cosine window to reduce the side-lobe levels. Further improvements in the side-lobe reduction and target SINR gain can be achieved by reconstructing the received baseband signal in the interfered sample locations [28]–[31]. Wide sense stationarity (WSS) is an important underlying assumption for many of the common time series analysis methods, such as AR modeling [35], [36]. We extend the WSS assumption to the slow-time for AR signal modeling in the slow-time domain.

![](images/58e34ceb43a7dd5a239ce92eee8ea88ff48a80d71d38b53ad50557cb378fc67f.jpg)

![](images/374cd762cd681416e8c6ef3a1c0a934f9adce5b4c08b38dbed75358f4b3d75bf.jpg)  
Fig. 3. Example of a baseband signal $x _ { b , m } ( n )$ disturbed by interference from two different sources. Interference A has lower power than that of B. Interfered samples are identified by comparing their $| d _ { x , m } ( n ) |$ values against the threshold $\lambda _ { j } .$

Let s(k) be a general (fast-time or slow time) wide-sense stationary signal. In a $p ^ { t h } .$ -order AR process, the $k ^ { t h }$ sample

$$
s ( k ) = \sum _ { i = 1 } ^ { p } a _ { i } s ( k - i ) + \epsilon _ { k }\tag{8}
$$

is a linear regression of $p$ past samples. In $( 8 ) , a _ { i }$ denotes the weighting coefficients, and $\epsilon _ { k }$ are residuals with zero mean and variance $\sigma ^ { 2 }$ . AR model estimation involves the estimation of two parameters: 1) model coefficients $a _ { i } ,$ , and 2) the model order $p .$ . A wide range of methods are found in the literature both for the calculation of AR model coefficients [37] and the selection of AR model order [38].

In this investigation, the AR coefficients $a _ { i }$ for a given model order $p$ are calculated via Burg’s method [37], [39]. This method is based on the minimization of prediction errors both in the forward linear predictor

$$
{ \hat { s } } _ { f } ( k ) = \sum _ { i = 1 } ^ { p } a _ { i } s ( k - i )\tag{9}
$$

and backward linear predictor

$$
\hat { s } _ { b } ( k ) = \sum _ { i = 1 } ^ { p } a _ { i } s ( k + i ) .\tag{10}
$$

Common AR parameter estimation methods e.g. Yule-Walker’s equations [35] are based on autocorrelation matrix estimates. When the sample size is small, there can be an estimation bias in the autocorrelation matrix, which can lead to a large deviation in the estimated parameters. Therefore, we use Burg’s method, which correctly estimates the AR model parameters directly from the available data points and is not sensitive to autocorrelation matrix estimate bias [40].

![](images/07ef4aaf411ebe009fab49653d5d8fe1931158b96027efbc546abf57492f33ae.jpg)  
Fig. 4. A signal frame $\mathrm { X } _ { b }$ of size $1 2 8 \times 2 5 6$ (slow-time samples fast-time samples), where interfered samples are removed to create gaps (dark rectangles) in the signal frame. In this example, the fast-time gap size $G _ { \mathsf { F T } }$ is 20 samples, the slow-time gap size $\dot { G } _ { \mathsf { S T } }$ is 5 samples and the percentage of discarded samples is 8.2%.

The next step is to select a suitable AR model order p from multiple candidates. Following the recommendations for sample prediction purposes in [41], we chose the Akaike Information Criterion (AIC) [42] for AR model selection. According to this criterion, the model order $p$ is selected which minimizes

$$
\mathrm { A I C } ( p ) = N \cdot \log { ( \hat { \sigma } ^ { 2 } ) } + 2 p ,\tag{11}
$$

where N is the sample size,

$$
\hat { \sigma } ^ { 2 } = \frac { \sum _ { i = 1 } ^ { N } \hat { \epsilon } _ { i } ^ { 2 } } { N } ,\tag{12}
$$

and $\hat { \epsilon } _ { i }$ are the estimated residuals [43]. It can be observed in (11) that the higher-order models will suffer from larger penalties. In this work, a second order variant of the AIC (AIC<sub>c</sub>), defined as

$$
\mathrm { A I C } _ { \mathrm { c } } ( p ) = \mathrm { A I C } ( p ) + \frac { 2 p ( p + 1 ) } { N - p - 1 } ,\tag{13}
$$

is used for model selection. $\mathrm { { A I C } _ { \mathrm { { c } } } }$ adds a higher penalty to larger orders and is recommended for small data segments $( N / p ~ < ~ 4 0 )$ [43].

An example of a baseband signal frame $\mathbf { X } _ { b }$ , in which samples are interfered with and discarded, is shown in Fig. 4. The coherence of the baseband signal in the complete received frame makes it possible to estimate a signal model and perform prediction of the disturbed samples in either fast-time (within a single chirp) or slow-time (chirp to chirp). Moreover, to reconstruct a signal more efficiently, the missing samples are predicted in both the forward and backward directions $( { \mathrm { F i g . } } 5 )$

A complete signal frame is considered to be coherent in both fast- and slow-time. Therefore, it is sufficient to estimate one fast-time and one slow-time model for the complete baseband signal frame. Forward and backward prediction results in two estimates ${ \hat { x } } _ { f } ( n )$ and ${ \hat { x } } _ { b } ( n )$ , respectively, for each missing sample. The prediction performance decreases as the number of lost samples increases. Therefore, a weighted sum of ${ \hat { x } } _ { f } ( n )$ and ${ \hat { x } } _ { b } ( n )$ is used to compute the final prediction value x(n), i.e.,

$$
\hat { x } \left( n \right) = \hat { x } _ { f } \left( n \right) \cdot \gamma \left( n \right) + \hat { x } _ { b } ( n ) \cdot ( 1 - \gamma \left( n \right) ) ,\tag{14}
$$

where $\gamma \left( n \right) = { { { \left( G - n + 1 \right) } \mathord { \left/ { \vphantom { { \left( G - n + 1 \right) } } } \right. \kern - delimiterspace } \left( G + 1 \right) } }$ , with G being the gap size (number of missing samples) in the corresponding dimension.

![](images/74a6f026a7e61e06e525a3082bc4462a21bca49555894790db2285ea73b73b74.jpg)  
Fast Time  
Fig. 5. (BP: Backward Prediction, FP: Forward Prediction, ST: Slow-Time, FT: Fast-Time and G: Gap Size). The fast-time gap size $G _ { \mathsf { F T } } = 3 ,$ and the maximum slow-time gap size ${ \cal G } _ { \sf S T } = 2 .$ The arrows indicate the directions of sample prediction using the fast- and slow-time AR models.

![](images/510db5372da5bc4436c15563f8d29806b918138a36d772ddfa8d10e622a3a402.jpg)  
Fig. 6. Block diagram of the FMCW radar and the interference mitigation procedure. The signal frames disturbed by the interference are reconstructed via AR models before post-processing.

The interference mitigation procedure using AR signal reconstruction (Fig. 6) is summarized below

-- Interference is detected in each chirp $\mathbf { X } _ { b }$ as it is received using a first-order difference detector, and disturbed samples are discarded, creating gaps in the two-dimensional signal frame $\mathbf { X } _ { b }$

-- AR coefficients for candidate model orders are calculated using Burg’s method.

-- The most suitable model order is selected using the AIC.

-- Signal reconstruction is performed by forward and backward prediction via selected AR models.

In the next section, we evaluate the interference mitigation and signal reconstruction performance resulting from AR modeling in fast- and slow-time with the help of computer simulations. Real measurements are used to evaluate the signal reconstruction performance in both dimensions in Section VI.

TABLE I  
TARGET PARAMETERS. RCS STANDS FOR RADAR CROSS SECTION
<table><tr><td>Target</td><td>Range m</td><td>Velocity m/s</td><td>RCS dBsm</td></tr><tr><td>Target 1</td><td>8</td><td>3</td><td>1</td></tr><tr><td>Target 2</td><td>10</td><td>4</td><td>10</td></tr><tr><td>Target 3</td><td>25</td><td>-15</td><td>10</td></tr><tr><td>Target 4</td><td>45</td><td>11</td><td>10</td></tr><tr><td>Target 5</td><td>70</td><td>-10</td><td>10</td></tr></table>

TABLE II

TRANSMIT SIGNAL PARAMETERS OF THE EGO AND INTERFERING RADARS
<table><tr><td>Parameter</td><td>Ego Radar</td><td>Radar-1</td><td>Radar-2</td></tr><tr><td>Center Frequency</td><td>77.5 GHz</td><td>77.5 GHz</td><td>77.5 GHz</td></tr><tr><td>Bandwidth</td><td>700 MHz</td><td>700 MHz</td><td>1000 MHz</td></tr><tr><td>Chirp Duration</td><td>41 μs</td><td>30 μs</td><td>20 μs</td></tr><tr><td>Chirp Repetition Interval</td><td>60 μs</td><td> $6 0 . 8 ~ \mu \mathrm { s }$ </td><td>60.03 μs</td></tr></table>

The results are also compared with those of the method in [19], where the time-domain disturbance in the received signal is suppressed using an inverse raised cosine window.

## V. SIMULATION RESULTS

The simulations are based on the target scenario in Table I and the radar configuration in Table II. The size of the signal frame $\mathbf { X } _ { b }$ is $5 1 2 \times 2 5 6$

Generally, mutual interference between two radars results in a time-limited disturbance in the baseband signal. The location of the disturbed samples in consecutive chirps is determined by the difference in the chirp repetition intervals (CRIs) of the interfering radars. If the CRIs of both radars are the same, the disturbance appears in the same samples in each chirp. However, if the CRIs differ, the interference appears at different sample locations. Therefore, the number of consecutively disturbed samples in slow-time is determined by the CRIs of the interfering radars.

For the evaluation of the interference mitigation method, two cases are simulated, and the missing samples are predicted using fast- and slow-time AR models in both cases. In the first case (interference between Ego Radar and Radar-1), more consecutive samples are disturbed in fast-time, leading to larger gaps in fast-time when disturbed samples are discarded. In the second case (interference between Ego Radar and Radar-2), a larger number of consecutive samples are disturbed in slow-time, leading to larger slow-time gaps.

## A. Larger Fast-Time Gaps

Mutual interference between Ego Radar and Radar-1 results in 79 interfered samples (15% of the total samples) per chirp in the received signal. The chirp repetition times for both radars are set such that the beginning of the disturbance is shifted by 10 samples in the sampled signals corresponding to consecutive chirps. This leads to a maximum of eight consecutive disturbed samples (3.1% of the total samples) along the slow-time at each fast-time sample location. After detecting the interference using the amplitude variation detector in (7), the interfered samples are removed (Fig. 7).

Based on the AIC, the selected model orders are $p _ { F T } = 2 0$ (fast-time) and $p _ { S T } = 3 1$ (slow-time). The signal reconstruction and interference mitigation performance is evaluated by

TABLE III  
TARGET SINR (dB) FOR THE CASE WITH A LARGER FAST-TIME GAPS
<table><tr><td>Target</td><td>Interference free</td><td>Interfered</td><td>Inverse cosine</td><td>AR (fast-time)</td><td>AR (slow-time)</td></tr><tr><td>Target 1</td><td>59.3</td><td>29.3</td><td>57.8</td><td>59.8</td><td>58.8</td></tr><tr><td>Target 2</td><td>64.7</td><td>35.7</td><td>42.8</td><td>55.8</td><td>63.0</td></tr><tr><td>Target 3</td><td>56.8</td><td>30.5</td><td>43.6</td><td>52.6</td><td>57.1</td></tr><tr><td>Target 4</td><td>48.4</td><td>19.2</td><td>46.6</td><td>48.0</td><td>48.1</td></tr><tr><td>Target 5</td><td>42.3</td><td>11.4</td><td>36.7</td><td>41.0</td><td>42.1</td></tr></table>

TABLE IV

PSLLS (dB) FOR ALL TARGETS FOR THE CASE WITH A LARGER FAST-TIME GAPS. HIGH SIDE LOBES ARE OBSERVED IN THE INVERSE-COSINE CASE
<table><tr><td>Target</td><td>Interference free</td><td>Interfered</td><td>Inverse cosine</td><td>AR (fast-time)</td><td>AR (slow-time)</td></tr><tr><td>Target 1</td><td>-45.1</td><td>-26.5</td><td>-19.9</td><td>-34.8</td><td>-44.5</td></tr><tr><td>Target 2</td><td>-50.4</td><td>-28.7</td><td>-19.5</td><td>-39.0</td><td>-45.1</td></tr><tr><td>Target 3</td><td>-45.1</td><td>-17.5</td><td>-28.2</td><td>-38.7</td><td>-44.4</td></tr><tr><td>Target 4</td><td>-42.3</td><td>-12.0</td><td>-19.7</td><td>-30.5</td><td>-34.6</td></tr><tr><td>Target 5</td><td>-36.0</td><td>-5.7</td><td>-26.0</td><td>-31.4</td><td>-33.0</td></tr></table>

![](images/699dff2fe2bb8c5413b19f016fe3efb147de6921914f634d0776edd23c236e49.jpg)

(a)  
![](images/f88ab0d03fd20aef9efd3b52c0899d105acd6a5aef4292f428a29f8eba412de7.jpg)  
Fig. 7. Diagonal lines indicate the locations of the interfered samples. In each chirp, 79 samples are affected by the interference $( G _ { \mathsf { F T } } = 7 9 )$ In slow-time, a maximum of eight consecutive samples are affected at each fast-time sample location $\mathsf { \bar { \Psi } } ( G _ { \mathsf { S T } } = 8 )$ .

![](images/3637adb79b551aa37b014030bef2ef4c73fef0f75c4d6062cb306c2b40e3d62a.jpg)  
(b)

## B. Larger Slow-Time Gaps

comparing the target SINRs and PSLLs in the range-Doppler maps in Fig. 8. A comparison between the target SINR and PSLL in the range-Doppler maps as a result of interference and different ways to suppress the interference are summarized in Tables III and IV. In the tables, it can be observed that the interference-induced noise is reduced after reconstructing the missing parts of the received baseband signal frame using the inverse-cosine window and AR models in fast- and slowtime. Additionally, the side lobe levels are reduced compared with the inverse-cosine window interference mitigation method. In fast-time signal reconstruction, the side lobes are not suppressed completely. Additionally, due to errors in the signal reconstruction, some phase noise can be observed in the Doppler domain (Fig. 8d). The range-Doppler map of the signal reconstructed in slow-time shows better side-lobe suppression (Fig. 8e). A comparison of the mean squared error in signal reconstruction using the fast- and slow-time AR models $( \mathrm { M S E } _ { \mathrm { F T } } = 5 . 1 \times 1 0 ^ { - 6 }$ and $\mathrm { \Delta } \mathrm { M S E _ { S T } } = 1 . 7 \times 1 0 ^ { - 5 } )$ also shows that better signal reconstruction is achieved with slow-time sample prediction.

Mutual interference between Ego Radar and Radar-2 results in 17 interfered samples (3.3% of the total samples) per chirp. The start of interference is shifted by one sample every third chirp. This results in 56 consecutive interfered samples (21.9% of the total samples) along the slow-time at each fast-time sample location. The signal matrix after removing the samples disturbed by interference is shown in Fig. 9.

![](images/83a42ea263c6a9113f154377da175ccf5e364a4454685b2bbc3f419f3d66fcf5.jpg)  
(c)

![](images/3f5a3a2ba3b28f31ba927c8538e037b646450d8163b650f3eb22c6d920d459cf.jpg)  
(d)

![](images/dfb16e92554ded76880ef88365b513fad2189179d94255f2d726c008c8da9658.jpg)  
(e)  
Fig. 8. Range-Doppler maps for simulated and reconstructed signals. In this particular simulation, the simulated signal has longer disturbed sections in fast-time than in slow-time. After discarding the disturbed samples, $G _ { \mathsf { F T } } = 7 9$ and $G _ { \mathsf { S T } } = 1 0 .$ . (a) Interfered. (b) Interferencefree. (c) Interference mitigation using an inverse-cosine window on the interfered sections in fast-time. (d) Interference mitigation with signal reconstruction using the fast-time AR model. (e) Interference mitigation with signal reconstruction using the slow-time AR model.

A comparison of the mean squared error in signal reconstruction using the fast- and slow-time AR models $( \mathrm { M S E } _ { \mathrm { F T } } =$ $8 . 0 \times 1 0 ^ { - 5 }$ and $\mathrm { M S E } _ { \mathrm { S T } } = 2 . 4 \times 1 0 ^ { - 5 } )$ shows that better signal reconstruction is achieved with the fast-time sample prediction.

TABLE V  
TARGET SINR (dB) FOR THE CASE WITH A LARGER SLOW-TIME GAPS
<table><tr><td>Target</td><td>Interference free</td><td>Interfered</td><td>Inverse cosine</td><td>AR (fast-time)</td><td>AR (slow-time)</td></tr><tr><td>Target 1</td><td>59.4</td><td>36.0</td><td>54.5</td><td>58.7</td><td>58.5</td></tr><tr><td>Target 2</td><td>64.0</td><td>37.6</td><td>57.4</td><td>63.6</td><td>63.4</td></tr><tr><td>Target 3</td><td>57.0</td><td>32.4</td><td>56.1</td><td>56.5</td><td>56.9</td></tr><tr><td>Target 4</td><td>48.9</td><td>20.1</td><td>45.8</td><td>48.9</td><td>48.8</td></tr><tr><td>Target 5</td><td>42.3</td><td>13.2</td><td>40.9</td><td>42.3</td><td>42.1</td></tr></table>

TABLE VI

PSLLS (dB) FOR ALL TARGETS FOR THE CASE WITH A LARGER SLOW-TIME GAPS. HIGH SIDE LOBES ARE OBSERVED IN THE INVERSE-COSINE CASE
<table><tr><td>Target</td><td>Interference free</td><td>Interfered</td><td>Inverse cosine</td><td>AR (fast-time)</td><td>AR (slow-time)</td></tr><tr><td>Target 1</td><td>-42.3</td><td>-28.5</td><td>-28.8</td><td>-42.8</td><td>-42.5</td></tr><tr><td>Target 2</td><td>-45.5</td><td>-35.2</td><td>-30.9</td><td>-44.4</td><td>-45.4</td></tr><tr><td>Target 3</td><td>-43.7</td><td>-26.7</td><td>-28.3</td><td>-44.4</td><td>-42.9</td></tr><tr><td>Target 4</td><td>-42.3</td><td>-12.6</td><td>-28.4</td><td>-39.4</td><td>-38.2</td></tr><tr><td>Target 5</td><td>-36.0</td><td>-8.6</td><td>-28.1</td><td>-33.0</td><td>-36.8</td></tr></table>

![](images/16edabfcc1cbfba1c9f33c3a135097db4b7e67af8f4ba125b8d4bb7e62cf262f.jpg)  
Fig. 9. The diagonal line indicates the location of the interfered samples. In each chirp, 17 samples are affected by the interference $( G _ { \mathsf { F T } } = 1 7 )$ In slow-time, 56 consecutive samples are affected at each fast-time sample location $( G _ { \mathsf { S } \mathsf { T } } = 5 6 )$

Since the simulated signal is the same as in Section $\mathrm { V } { \cdot } \mathrm { A } .$ the slow-time and fast-time AR model orders are also the same. The SINR and PSLL from the range-Doppler maps of the interfered and reconstructed signals (Fig. 10) are summarized in Tables V and VI. Again, better SINR and side-lobe suppression is observed in the reconstructed signals than in the interfered and inverse-cosine cases. Although the gap sizes are different, there is not much difference in the SINR and PSLL of the reconstructed signals in fast- and slow-time.

The AR signal reconstruction in both cases shows a considerable improvement over the inverse-cosine method in terms of side-lobe suppression. In the range-Doppler maps (Fig. 8 and 10), the high side lobes resulting from interference suppression using the inverse-cosine method may lead to false detections. A part of the received signal is zeroed out in the inverse-cosine method, which results in a loss in the SINR for all targets. The results also show an improvement in the SINR using AR signal reconstruction in both cases. Comparing the two simulated cases, AR reconstruction in slow-time shows lower PSLLs when the slow-time gaps are smaller. Similarly, AR reconstruction in fast-time performs better when the fast-time gaps are smaller. Therefore, it can be concluded that a better signal reconstruction performance is achieved by choosing the dimension (fast-time or slow-time) with smaller gaps for signal reconstruction.

![](images/52194b374d969acbaf7159e62be84f41ec8e1f929030a099d65e8c9de9d8ff72.jpg)  
(a)

![](images/4921e1549d59fbc425788b8d5763b6fc45dd80b68ae03f65c479557880600aa7.jpg)  
(b)

![](images/7c54661333960aa435c2bef89b725529e89bb8184a4f4c10ea015c6c8ab7f279.jpg)  
(c)

![](images/822b1a3d49b09efb474d4e25b5d28e55b67a3f94ed97a056723b553e4440224d.jpg)  
(d)  
Fig. 10. Range-doppler maps for simulated and reconstructed signals. After discarding disturbed samples, $G _ { \mathsf { F T } } ~ = ~ 1 7$ and $G _ { \mathsf { S T } } ~ = ~ 5 { \bar { 6 } } .$ (a) Interfered. (b) Interference mitigation using an inverse cosine window on the interfered sections in fast-time. (c) Interference mitigation with signal reconstruction using fast-time AR model. (d) Interference mitigation with signal reconstruction using slow-time AR model.

## VI. MEASUREMENT RESULTS

The interference mitigation and signal reconstruction performance of the proposed method is verified with the help of real measurements. 77 GHz mm-wave radar evaluation kits (AWR1642EVM and AWR1243EVM) from Texas Instruments are used for the measurements, and DCA1000EVM is used to capture measurement data over the Ethernet (Fig. 11). One radar is mounted on a car driving towards the static radar. Both radars operate in the same time interval and interfere with each other (Fig. 12). As a result, we have measurement data from the static and moving radars. The transmit parameters of both radars are given in Table VII. Different chirp slopes are used to ensure that interference is encountered.

## A. Interference Mitigation Performance

Although interference is observed in both radars, the percentage of samples affected by interference is negligible in both cases (1.0% for moving radar and 1.6% for static radar). As a result, the degradation in the SINR in the range-Doppler maps is almost negligible. However, it is possible to see the degradation in the SINR when single interference-affected chirps are considered. Therefore, single interfered-affected chirps are considered in both cases (static and moving) to evaluate the interference mitigation performance.

![](images/77a6f4bb1fdbd65263a337d07321c03469f1cd727851068fd6a95caed9cdc3f6.jpg)

![](images/37bbdc1b4b0a032fd4d0a4000d21c6442691cf4d3133adf36b4b811e046a6029.jpg)

Fig. 11. Radar used for measurements. AWR1642EVM is mounted on a car and used for dynamic measurements. AWR1243EVM is mounted on a stand and used for static measurements.  
![](images/b5e891db57be10f0aa4282d14e5691948507e1b419dc701f8b6b3d7137714237.jpg)  
Fig. 12. Experimental setup. The car equipped with AWR1642EVM is moving towards the static AWR1243EVM. A trihedral corner reflector is placed behind the static radar (at a distance of 18.1 m away from the car), which serves as a strong reflector.

TABLE VII  
TRANSMIT SIGNAL PARAMETERS OF THE TWO RADARS USED IN THE FIELD MEASUREMENTS
<table><tr><td>Parameter</td><td>Static Radar</td><td>Moving Radar</td></tr><tr><td>Center frequency</td><td>77.5 GHz</td><td>77.5 GHz</td></tr><tr><td>Bandwidth</td><td>896 MHz</td><td>255 Mhz</td></tr><tr><td>Slope</td><td>35 MHz/μs</td><td>10 MHz/μs</td></tr><tr><td>Chirp repetition interval</td><td>55μs</td><td>120μs</td></tr></table>

The estimated AR model orders for the static radar using the AIC are $p _ { F T } = 2 0$ and $p _ { S T } = 2 1$ . The length of the interfered section in fast-time is approximately 18 samples $( G _ { F T } = 1 8 )$ and every fourth chirp is affected by the interference, which leads to only one-sample slow-time gaps. The range profiles for the reconstructed signals have a lower noise floor compared to the signal with interference (Fig. 13a). The SINR for the target (car) at 6.6 m is 12.5 dB, 21.3 dB, and 20.8 dB for the interfered, fast-time reconstructed and slow-time reconstructed signals, respectively. The target SINR for the inverse-cosine case is 20.8 dB. As a reference, the SINR of a neighboring noninterfered chirp is 21.3 dB.

For the moving radar, $p _ { F T } = 2 7$ and $p _ { S T } = 1 0$ . The length of the interfered section in fast time is 10 samples $( G _ { F T } = 1 0 )$

![](images/d29ea40ea83610bc5ee37764be65bdec3ac871692265234c1a53aaa9b8642d26.jpg)  
(a)

![](images/e15df01902af225d80089f15874fc1fc94017d649ad8533e0ea606e347a6a846.jpg)  
(b)  
Fig. 13. Range profiles for the interfered, fast-time reconstructed and slow-time reconstructed signals. (a) Static radar. (b) Moving radar.

and only 15 chirps are affected by interference. The range profiles for the reconstructed signals have a lower noise floor compared to the signal with interference (Fig. 13b). The SINR for the target (trihedral corner reflector) at 18.1 m is 14.0 dB, 20.5 dB, and 20.5 dB for interfered, fast-time and slow-time reconstructed signals, respectively. The target SINR for the inverse-cosine case is 19.4 dB. As a reference, the SINR of a neighboring noninterfered chirp is 21.1 dB.

## B. Signal Reconstruction Performance

As mentioned earlier, signal frames in the measurement data do not have a sufficient number of disturbed samples to observe the effect of signal reconstruction in different domains. The signal reconstruction performance is therefore assessed by creating gaps of different sizes in the noninterfered signal frames at random locations (as done in Fig. 4) and then comparing the range-Doppler maps and MSE in the reconstructed signals. Randomly generated gaps of different sizes can be seen as equivalent to the gaps created in an interfered signal frame $\mathbf { X } _ { b }$ when the interfered samples are discarded. The availability of noninterfered signal frames also makes it possible to compute the MSEs by comparing the reconstructed signals with the clean ones. The main aim of this evaluation is to show a relation between gap size and AR reconstruction performance in fast- and slow-time. For this evaluation, we use measurements from both static and moving radars.

In this experiment, a small drone (DJI Phantom 4) is flown away from the static radar (AWR1243EVM) at a $0 ^ { \circ }$ azimuth angle. The signal frame captured when the drone is 4.8 m from the radar and moving with a velocity of $1 . 2 \mathrm { m } / \mathrm { s }$ is used for visualizing the range-Doppler maps. The drone is used to generate a moving target that can clearly be identified in the range-Doppler domain, separate from the static clutter. By removing samples from the signal frame (of size $2 5 6 \times 2 5 5 )$ , the gaps of 51 (20%) samples are created in both fast- and slow-time. To compare the reconstruction performance, the same model order $( p _ { F T } = p _ { S T } = 2 0 )$ is chosen for the AR model parameter estimation.

![](images/644b841fa3f7e9772772eef515cb50022c52006f17a471efb383b1772f3d8750.jpg)  
(a)

![](images/f425fee0dadc21956023e7531f68e7a63c7f3984d9cd55861733967649c96987.jpg)

![](images/8fbb2132a3b238840b4a99a9a0ff77935eabf4bbe83cdbe01b98c6d4e8ef16c8.jpg)  
(c)

(b)  
![](images/96d596f070023b5eebce02e2cca347119dd23bbbbcfcff7c0597cfdc8af701b4.jpg)  
(d)  
Fig. 14. Range-Doppler maps in the static ego radar case. The target is a drone at a distance of 4.8 m moving away from the radar with a velocity of 1.2 m/s. $G _ { F T } = G _ { S T } = 5 1$ samples. (a) Interference free. (b) Signal reconstruction using an inverse-cosine window on the discarded sections in fast-time to remove discontinuities. The highest side-lobes are observed in this case. (c) Signal reconstruction using the fast-time AR model. Side lobes are suppressed compared to the inverse-cosine case. (d) Signal reconstruction using the slow-time AR model.

The quality of signal reconstruction is determined by comparing the range-Doppler maps in Fig. 14. It can be observed that the range-Doppler map corresponding to the signal frame reconstructed in slow-time (Fig. 14d) is the most similar to the range-Doppler map corresponding to the clean signal (Fig. 14a). There are some artifacts in the Doppler domain in the fast-time case (Fig. 14c), showing that the reconstructed signal has some errors. Further degradation is observed both in the range and Doppler domains in the case where spaces are filled in fast-time by using an inverse raised cosine window (Fig. 14b). The calculated MSE values (0.031 for the fast-time reconstruction and 0.014 for the slow-time reconstruction) also show that the signal reconstruction in slow-time performs better than that in fast-time.

The signal reconstruction performance is also assessed by computing the MSEs. 50 frames of the received signal are considered for this evaluation. Gaps of fixed size are introduced in all frames by removing samples from random locations in all 50 frames. All 50 frames are then reconstructed in fast-time and slow-time dimensions. The MSE is computed by comparing all reconstructed frames with the corresponding original frames. The computed MSE values are then used to plot the graphs in Fig. 15. It can be observed from the graphs that the MSE increases with increasing gap sizes in both dimensions. However, for the tested scenario, the error is higher in the fast-time scenario than in the slow-time scenario. Therefore, for the static radar case where the velocity spectrum is less dense, it is better to perform signal reconstruction in slow-time.

![](images/2daf8d29b947fc212dca8f5189de13d234ff06e190e59dd69c5cd7b565dc6da0.jpg)  
Fig. 15. The relation between gap sizes in fast- and slow-time and MSEs for the measurements from a static radar. In slow-time AR reconstruction, lowest MSE is observed for $G _ { S T } = 2 ,$ and highest MSE is observed for $G _ { S T } = 8 0 .$ . The last data points corresponding to $G _ { S T } = 6 0 $ and $G _ { S T } = 8 0 \mathrm { i n } \mathsf { A R }$ (slow-time) are missing because, in some frames, whole columns are removed when discarding sample blocks.

In this case, the data is captured by a radar fixed on a car moving towards the static radar. There is no disturbance in the received signal since the static radar is not transmitting. The signal frame used for generating range-Doppler maps is captured when the car is at a 4.4 m distance from the static radar and moving with a velocity of $1 . 7 \mathrm { m } / \mathrm { s }$ . The size of the baseband signal frame is $2 5 6 \times 1 2 8$ Gaps of 25 (10%) and 25 (20%) samples are created in fast-time and slow-time, respectively. The model orders are again kept constant $( p _ { F T } = p _ { S T } = 2 0 )$

The range-Doppler maps (Fig. 16) show that the side-lobes are suppressed when the signal is constructed in fast-time or slow-time. However, when compared with the interference-free case, there is a marginal degradation in image quality. The inverse-cosine method again shows the most degradation (Fig. 16b).

Similar to the static radar case, we also assess the signal reconstruction performance for the moving radar using MSEs. Gaps of fixed sizes are introduced in 50 interference-free signal frames captured by the moving radar. The velocity of the car changes from 2.5 m/s to $1 . 5 \mathrm { m } / \mathrm { s } ,$ and the distance changes from 6.5 m to 3.2 m in these 50 frames. The MSE is computed by comparing all reconstructed frames with the corresponding original frames. In the moving radar case, the difference in MSE in the fast- and slow-time reconstructed signals is smaller than in the static radar case (Fig. 17). Furthermore, the slowtime reconstruction performance is worse for larger slow-time gaps in the signal frame.

## VII. DISCUSSION

The results from the simulations and measurements show that AR signal reconstruction can be an effective interference mitigation approach in automotive radars. The time-domain interference mitigation techniques in the literature mainly focus on signal reconstruction in fast-time. With the help of simulations and outdoor experiments, we have shown that slow-time signal reconstruction can also be an effective approach for interference mitigation. Both the simulation and experimental results show significant side-lobe suppression in the range-Doppler maps when the signals are reconstructed using the AR models. The side lobes can be further reduced by reconstructing the signal in the dimension (slow-time or fast-time) with smaller gaps (a smaller number of consecutive disturbed samples).

![](images/8f321ab7a8b41dc567d26f39a1d7fec43cbff827579b19bb1fc2a4623472a0b1.jpg)  
(a)

![](images/6f916ec7ac9a179028486ac6848bba5c10d8888e33e5f91fa30c702d437b74ab.jpg)  
(b)

![](images/7f3b7db1304d630a1b7f45ff1395d697fea4ad4962606a3570fcb24df8ca2357.jpg)  
(c)

![](images/69576d552a1ca667c7db8a3f38216e4d223590ce2af0991497d9b72b04f2b62b.jpg)  
(d)  
Fig. 16. Range-Doppler maps for measured and reconstructed signals in the case of a moving radar. A static radar (with a laptop on an iron stand) at 4.4 m and a trihedral corner reflector at 15m are the strong targets in this case. $G _ { F T } = G _ { S T } = 2 5$ samples. (a) Interference free. (b) Signal reconstruction using an inverse-cosine window in fast-time. High side lobes are observed in this case. (c) Signal reconstruction using the fast-time AR model. The side lobes are suppressed compared with the inverse-cosine case. However, the side lobes are still visible when compared with the interference-free case. (d) Signal reconstruction using the slow-time AR model. The side lobe levels are similar to those in the signal reconstructed in fast-time.

×10-3  
![](images/3a43827dcbaf8faf563679211486947b01e625f0a34c878f6ad5b4ac4dd37327.jpg)  
Fig. 17. The relation between gap sizes in fast- and slow-time and MSEs for the measurements from a moving radar. The last data points corresponding to $G _ { S T } = 3 0$ and $G _ { S T } = 4 0 \mathrm { i n } \mathsf { A R }$ (slow-time) are missing because, in some frames, whole columns are removed when discarding sample blocks.

When comparing the fast-time and slow-time signal reconstruction performances in a static radar, it is observed that the MSEs are generally lower in the signals reconstructed in slow-time, even for larger gap sizes (Fig. 15). The reason for the better signal reconstruction in slow-time is probably that the Doppler spectrum is less dense compared to the range spectrum for the static radar case. Therefore, especially in surveillance radars that are generally static, AR signal reconstruction in slow time can be an effective interference mitigation approach. The main drawback of slow-time signal reconstruction is that the whole signal frame needs to be received before starting model estimation. A direct relation is observed between the signal reconstruction dimension and gap size in the case of measurements with a moving radar. In our measurements, the Doppler spectrum is much denser than in the static radar case with one moving target.

The focus in this work has remained on interference mitigation performance evaluation in terms of the SINR and PSLL in the range-Doppler domain. The angle estimation performance is also an important factor for automotive radar applications. Inaccurate AR signal reconstruction on multiple receiving channels may lead to phase errors that can deteriorate the angle estimation performance. Therefore, the effect of fast- and slow-time AR signal reconstruction on the angle estimation performance requires further investigation.

## VIII. CONCLUSION

Mutual interference in automotive radars impairs the detection capabilities of ego radar. For the safety of road users, it is important to mitigate the effect of interference. In this paper, a method for interference mitigation in chirp sequence automotive radars is proposed. The method is based on the AR modeling of the received signal in the time domain. After model estimation, the interfered samples are replaced with sample values predicted using the estimated models. Signal coherence in the complete baseband signal frame makes it possible to perform signal reconstruction in fast- or slowtime. The proposed method is evaluated using simulations and measurements from 77 GHz FMCW chirp sequence radars. The results are compared with a well-known interference mitigation technique, in which the disturbed part of the baseband signal is suppressed in the time domain using an inverse-cosine window. In comparison to the inverse-cosine method, the SINR is improved, and better suppression of the side lobes is achieved when AR models are used for signal reconstruction. For the static radar, the slow-time signal reconstruction performs better (in terms of the side-lobe suppression and MSE) than the fast-time reconstruction for the same number of missing samples. The drawback of slow-time signal reconstruction is that the whole signal frame needs to be received before starting model estimation, leading to longer processing delays. However, the frame used is the same as that used for Doppler processing, so the drawback is not significant in many applications. For the moving radar, the signal reconstruction performance is better in the dimension with smaller gaps. The SINR results show an improvement of <sub>∼</sub>30 dB (for a complete signal frame) in a simulated scenario and <sub>∼</sub>7.8 dB (for a single chirp) in a real scenario. It should be noted that the SINR improvement in real measurements is equal to suppressing the interference down to the radar noise floor, which is a notable result. Unfortunately, the interference level in the experiment was low. In an experiment with higher interference power, the suppression is expected down to the noise floor, and therefore, it would increase the measured SINR improvement.

## ACKNOWLEDGMENT

The authors would like to thank Saleh Javadi for the drone support during the radar experiment.

## REFERENCES

[1] J. Dickmann et al., “‘Automotive radar the key technology for autonomous driving: From detection and ranging to environmental understanding,”’ in Proc. IEEE Radar Conf. (RadarConf), May 2016, pp. 1–6.

[2] B.-E. Tullsson, “Alternative applications for a 77 GHz automotive radar,” in Proc. Rec. IEEE Int. Radar Conf., May 2000, pp. 273–277.

[3] Short Range Devices; Transport and Traffic Telematics (TTT); Short Range Radar equipment operating in the 77 GHz to 81 GHz band; Harmonised Standard covering the essential requirements of article 3.2 of Directive 2014/53/EU, document EN 302 264 V2.1.1, ETSI, Sophia Antipolis, France, 2017.

[4] Short Range Devices; Transport and Traffic Telematics (TTT); Radar Equipment Operating in the 76 GHz to 77 GHz Range; Harmonised Standard Covering the Essential Requirements of Article 3.2 of Directive 2014/53/EU; Part 1: Ground Based Vehicular Radar, document EN 301 091-1 V2.1.1, ETSI, Sophia Antipolis, France, 2017.

[5] Short Range Devices; Transport and Traffic Telematics (TTT); Radar Equipment Operating in the 76 GHz to 77 GHz Range; Harmonised Standard Covering the Essential Requirements of Article 3.2 of Directive 2014/53/EU; Part 2: Fixed Infrastructure Radar Equipment, document EN 301 091-2 V2.1.1, ETSI, Sophia Antipolis, France, 2017.

[6] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Automotive radarinvestigation of mutual interference mechanisms,” Adv. Radio Sci., vol. 8, pp. 55–60, Jan. 2010.

[7] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, nos. 3–4, pp. 371–378, Jun. 2014.

[8] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in Proc. 9th Eur. Radar Conf., Oct./Nov. 2012, pp. 1–5.

[9] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[10] T.-N. Luo, C.-H.-E. Wu, and Y.-J.-E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[11] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[12] L. Mu, T. Xiangqian, S. Ming, and Y. Jun, “Research on key tchnologies for collision avoidance automotive radar,” in Proc. IEEE Intell. Vehicles Symp., Jun. 2009, pp. 233–236.

[13] C. Aydogdu, N. Garcia, L. Hammarstrand, and H. Wymeersch, “Radar communications for combating mutual interference of FMCW radars,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2019, pp. 1–6.

[14] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[15] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Techn., vol. 65, no. 5, pp. 1727–1734, May 2017.

[16] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 252–256.

[17] M. Rameez, M. Dahl, and M. I. Pettersson, “Experimental evaluation of adaptive beamforming for automotive radar interference suppression,” in Proc. IEEE Radio Wireless Symp. (RWS), Jan. 2020, pp. 183–186.

[18] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[19] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2015, pp. 1–4.

[20] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 726–731.

[21] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 405–410.

[22] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[23] A. Correas-Serrano and M. A. Gonzalez-Huici, “Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2019, pp. 1–4.

[24] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in Proc. IEEE Int. Symp. Circuits Syst. (ISCAS), May 2018, pp. 1–4.

[25] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[26] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 624–629.

[27] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2020, pp. 3802–3806.

[28] B.-E. Tullsson, “Topics in FMCW radar disturbance suppression,” in Proc. Radar Syst. (RADAR), Oct. 1997, pp. 1–5.

[29] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[30] Z. Liu, W. Lu, J. Wu, S. Yang, and G. Li, “A PELT-KCN algorithm for FMCW radar interference suppression based on signal reconstruction,” IEEE Access, vol. 8, pp. 45108–45118, 2020.

[31] S. Lim, S. Lee, J.-H. Choi, J. Yoon, and S.-C. Kim, “Mutual interference suppression and signal restoration in automotive FMCW radar systems,” IEICE Trans. Commun., vol. 102, no. 6, pp. 1198–1208, 2019.

[32] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2015, pp. 1–4.

[33] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[34] Y. Watanabe and K. Natsume, “Interference determination method and FMCW radar using the same,” U.S. Patent 7 187 321, Mar. 6, 2007.

[35] C. Chatfield, The Analysis of Time Series: An Introduction, 6th ed. Boca Raton, FL, USA: CRC Press, 2004.

[36] D. A. Dickey and W. A. Fuller, “Distribution of the estimators for autoregressive time series with a unit root,” J. Amer. Stat. Assoc., vol. 74, no. 366a, pp. 427–431, Jun. 1979.

[37] S. M. Kay and S. L. Marple, “Spectrum analysis—A modern perspective,” Proc. IEEE, vol. 69, no. 11, pp. 1380–1419, Nov. 1981.

[38] J. R. Dickie and A. K. Nandi, “A comparative study of AR order selection methods,” Signal Process., vol. 40, nos. 2–3, pp. 239–255, Nov. 1994.

[39] M. H. Hayes, Statistical Digital Signal Processing and Modeling. Hoboken, NJ, USA: Wiley, 2009.

[40] M. J. L. de Hoon, T. H. J. J. van der Hagen, H. Schoonewelle, and H. van Dam, “Why yule-walker should not be used for autoregressive modelling,” Ann. Nucl. Energy, vol. 23, no. 15, pp. 1219–1228, Oct. 1996.

[41] J. Ding, V. Tarokh, and Y. Yang, “Model selection techniques: An overview,” IEEE Signal Process. Mag., vol. 35, no. 6, pp. 16–34, Nov. 2018.

[42] H. Akaike, “Information theory and an extension of the maximum likelihood principle,” in Selected Papers of Hirotugu Akaike, E. Parzen, K. Tanabe, and G. Kitagawa, Eds. New York, NY, USA: Springer, 1998, pp. 199–213. [Online]. Available: https://doi.org/10.1007/978-1-4612- 1694-0\_15, doi: 10.1007/978-1-4612-1694-0\_15.

[43] K. P. Burnham, D. R. Anderson, and K. P. Huyvaert, “AIC model selection and multimodel inference in behavioral ecology: Some background, observations, and comparisons,” Behav. Ecol. Sociobiol., vol. 65, no. 1, pp. 23–35, Jan. 2011.

![](images/131d724a3fcedbcf2d297dcee1e0aec593fe37576269fd3bfb6904f802149f6e.jpg)  
Muhammad Rameez (Student Member, IEEE) received the B.E. degree in electrical engineering from the National University of Sciences and Technology, Islamabad, Pakistan, in 2010, and the M.Sc. degree in communications technology from the University of Ulm, Ulm, Germany, in 2016. He is currently pursuing the Ph.D. degree in systems engineering with the Blekinge Institute of Technology, Karlshamn, Sweden. His research interests include radar signal processing and automotive radar interference mitigation techniques.

![](images/f5a6ec7c83d56ee5db53b8ce33b5a3c939d6998c1424fd8677396ab4d777cb9a.jpg)

Mats I. Pettersson (Member, IEEE) received the M.Sc. degree in engineering physics, the Licentiate degree in radio and space science, and the Ph.D. degree in signal processing from the Chalmers University of Technology, Gothenburg, Sweden, in 1993, 1995, and 2000, respectively. For some years, he worked with mobile communication research at Ericsson and for ten years, he was employed at Swedish Defence Research Agency (FOI). At FOI, he focused on ultrawide band low frequency SAR systems. Since 2005, he has been with the Blekinge Institute of Technology (BTH), where he is a Full Professor. His research is related to remote sensing, and his main interests include SAR processing, space time adaptive processing (STAP), high resolution SAR change detection, automotive radar, radio occultation, and computer vision.

![](images/a4b150564cb22f0c9780b53d9447af38a8098e44ddb1b812d71f9d0729e3338a.jpg)

Mattias Dahl (Member, IEEE) received the M.Sc. degree in computer engineering from the Luleå Institute of Technology in 1993, the Licentiate in Engineering degree from Lund University in 1997, and the Ph.D. degree in applied signal processing from the Blekinge Institute of Technology (BTH) in 2000. Since 2005, he has been with the Department of Mathematics and Natural Sciences, BTH, where he is currently a Professor of Systems Engineering. He has authored over 100 scientific publications and patents, and received several awards from the Sweden’s Innovation Agency and the Swedish Foundation of Technology Transfer.