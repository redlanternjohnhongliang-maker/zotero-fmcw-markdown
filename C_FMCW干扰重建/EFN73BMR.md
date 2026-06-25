# Interference Compression and Mitigation for Automotive FMCW Radar Systems

Muhammad Rameez , Mats I. Pettersson , , and Mattias Dahl ,

—Millimeter-wave (mm-wave) frequency-modulated continuous wave (FMCW) radars are increasingly being deployed for scenario perception in various applications. It is expected that the mutual interference between such radars will soon become a significantproblem. Therefore,to maintain the reliability of the radar measurements, there must be procedures in place to mitigate this interference. This article proposes a novel interference mitigation technique that utilizes the pulse compression principle for interference compression and mitigation. The interference in the received time-domain signal is compressed using an estimated matched filter. Afterward, the compressed interference is discarded, and the signal is repaired in the pulse-compressed domain using an autoregressive (AR) model. Since the interference spans fewer samples after compression, the signal can be restored more accurately in the compressed domain. Real outdoor measurements show that the interference is effectively suppressed down to the noise floor using the proposed scheme. A signal to interference and noise ratio (SINR) gain of approximately 14 dB was achieved in the experimental data, supporting this study. Moreover, the results indicate that this method is also applicable to situations where multiple interference sources are present.

![](images/83178f863b7b1f6e5ab7168014356ca9db5bc347dff2b9392ccf71ef7677e23f.jpg)

— Automotive radar, interference cancellation, millimeter wave (mm-wave) radar, pulse compression, radar signal processing, signal reconstruction.

## I. INTRODUCTION

F <sup>REQUENCY-modulated</sup> <sup>continuous</sup> <sup>wave</sup> <sup>(FMCW)</sup>radars, operating at millimeter-wave (mm-wave), are capable of providing highly accurate position and velocity estimates under most weather conditions [1]. In recent years, thanks to the technological advancements in mmwave technology, these sensors have become low-cost, small-sized, and highly capable. Hence, radar has become an attractive sensor in numerous applications, for example, indoor and outdoor surveillance, industrial, and, most notably, automotive applications [2], [3]. Many advanced driver assistance systems (ADASs) and autonomous driving functions in modern vehicles depend on the automotive radar for 360<sup>◦</sup> situational awareness. However, the rapidly increasing deployment of automotive radars in modern cars and the shared frequency spectrum are giving rise to concerns regarding mutual interference, which affects the sensor reliability and, consequently, the autonomous vehicle safety [4].

Mutual interference can deteriorate the performance of the victim radar by increasing the noise floor of the receiver, which results in reduced sensitivity and degraded detection performance [5]. This directly impacts the functionality of ADAS and autonomous functions in vehicles, which may lead to hazardous situations considering the safety-related systems. The mutual interference problem can become more challenging if interference mitigation strategies are not developed and standardized. In the past decade, several studies have been conducted to understand interference mechanisms, develop countermeasures, and explore cooperative solutions [6]. However, to this date, thereis no scientific mutual interference mitigation standard for automotive radar or mm-wave radars operating in the 77–81 GHz band, in general [7]. Therefore, it is pertinent to investigate innovative interference mitigation strategies for the existing mm-wave radar systems, predominantly utilizing the FMCW waveform.

Interference mitigation techniques in FMCW radar systems can be classified into three main categories: avoidance, detect-and-repair, and more recent communication-based methods [7]. Interference avoidance methods employ techniques like frequency hopping [8], medium access control [9], and chirp randomization [10] to decrease the probability of occurrence of interference or to minimize its effects during postprocessing. Communication-based methods [11], [12] are based on the idea that radars operating in the same vicinity can communicate with each other and decide on transmit (Tx) intervals. Both avoidance and communication-based methods require changes in the existing radar systems at the hardware level. The existing systems usually drop the corrupted frames or employ detect-and-repair methods based on signal-processing techniques to minimize the effect of interference in the corrupted signal received by the radar [7].

The mutual interference in most cases is time-limited, meaning that the interference appears in short bursts in the received signal. Due to this, there has been an interest in developing time-domain signal-processing methods that mitigate interference by recovering the signal of interest from the corrupted signal. These methods include interference signal estimation and subtraction [13], sparse signal reconstruction using the iterative method with adaptive thresholding (IMAT) [14], inverse Fourier transformation using adaptively selected peaks in the range spectrum [15], Kalman filtering [16], and autoregressive (AR) modeling in fast and slow-time [17]. More recently, deep-learning methods [18], [19] have also been employed to recover the interference-free signal from the corrupted signal. All of the time-domain interference mitigation methods mentioned above show an excellent performance for relatively short interference intervals. For longer interference intervals, where a relatively large number of samples in the received signal get corrupted, the reconstruction performance tends to deteriorate.

This article proposes a novel approach that compresses the interference in the received time-domain signal to improve the signal reconstruction performance. The pulse (interference) compression is performed after detecting the interference and estimating the required interference parameters, that is, duration and chirp slope. As a result, a significant part of the interference spans relatively fewer samples in the compressed domain. These samples are discarded, and the signal is then reconstructed in the compressed domain by predicting the missing samples iteratively. Since fewer samples are predicted, the reconstruction error is reduced compared to the case where the missing samples are predicted directly in the time domain [17].

The main contributions of this study are: 1) estimation of required parameters for estimation of the interference signal; 2) using a combination of pulse compression, signal reconstruction, and pulse decompression for effective interference removal; and 3) verification of the proposed methodology using real measurements.

## II. THEORETICAL FRAMEWORK

## A. FMCW Radar

The Tx signal in an FMCW radar (see Fig. 1) is composed of a sequence of M linear frequency-modulated chirps for simultaneous range and velocity estimation [20]. The chirp duration T is the time it takes for a chirp signal to sweep across a bandwidth B. The time-domain expression of an individual Tx chirp in the radio-frequency (RF) domain with carrier frequency $f _ { c }$ and chirp slope $k = B / T$ is

![](images/76ba4477684795339760ce8b2a110224efe15178758f23e015032efa86e81c3d.jpg)  
Fig. 1. High-level block diagram of an FMCW radar with an in-phase and quadrature (IQ) receiver. Both receiver chains consist of a mixer, followed by a low-pass anti-aliasing filter (LP), and an ADC.

$$
s _ { \mathrm { R F , T x } } \left( t \right) = e ^ { j \left( 2 \pi \left( f _ { c } t + \frac { 1 } { 2 } \cdot k t ^ { 2 } \right) - \phi _ { 0 } \right) }\tag{1}
$$

where t represents the continuous time and $\phi _ { 0 }$ is the initial phase. Note that the frequency of the chirp signal increases with time. These types of chirps are often referred to as up-chirps.

Using a directional coupler, the Tx signal $s _ { \mathrm { R F } , \mathrm { T x } }$ is fed to a Tx antenna and a homodyne downconversion mixer. The receive (Rx) signal is a scaled and delayed version of the Tx signal and contains reflections from all targets in the radar’s field of view, that is,

$$
s _ { \mathrm { R F , R x } } \left( t \right) = \sum _ { k = 0 } ^ { K } A ^ { ( k ) } \cdot s _ { \mathrm { R F , T x } } \left( t - \tau ^ { ( k ) } \right)\tag{2}
$$

where K is the number of targets and $A ^ { ( k ) }$ and $\tau ^ { ( k ) }$ denote the scaling factor and the round trip delay corresponding to the kth target, respectively. In the receiver, the Rx signal is mixed (multiplied) with the transmitted signal (1), and the mixer output is downconverted using a low-pass filter, which also acts as an anti-aliasing filter in further processing, to obtain the complex baseband signal of the form

$$
s _ { \mathrm { C B } } \left( t \right) = \sum _ { k = 0 } ^ { K } A ^ { \left( k \right) } e ^ { j \left( 2 \pi f _ { B } ^ { \left( k \right) } t + \phi _ { B } ^ { \left( k \right) } \right) } .\tag{3}
$$

The beat frequency $f _ { B } ^ { ( k ) }$ and the phase $\phi _ { B } ^ { ( k ) }$ in the above expression contain the range and velocity information of the kth target in the radar’s field of view. The low-pass filter defines the maximum beat frequency expected by the radar system, which in turn corresponds to the maximum detectable range.

In further processing, a 2-D fast Fourier transform (2D-FFT) is applied to the sampled baseband signal over the sequence of M chirps to obtain a range-Doppler (RD) map, which enables the extraction of the range and the radial velocity of the targets, simultaneously.

![](images/5bfcff2142c0904a8e4c1369a72ccf7b288efb0bf334115a5c3b0623f010f4bb.jpg)  
Fig. 2. Noncoherent mutual interference between chirps from ego and interfering radars. The chirps from the ego radar are shown in blue and from interfering radar are shown in red. Green dashed lines define the bandwidth $\bar { B _ { \sf R X } }$ of the low-pass anti-aliasing filter. The target echo lies within the time interval $T _ { B _ { \mathrm { R } x } }$ . The interference duration is denoted by $\tau _ { d } .$

## B. FMCW-FMCW Interference

A single Tx chirp from the interfering radar has similar form as the ego radar but with bandwidth $B _ { \mathrm { i n t } }$ and duration $T _ { \mathrm { i n t } }$ (chirp slope $k _ { \mathrm { i n t } } ~ = ~ B _ { \mathrm { i n t } } / T _ { \mathrm { i n t } } )$ . The Tx chirp from the interfering radar is therefore represented as

$$
s _ { \mathrm { R F } , \mathrm { T x } , \mathrm { i n t } } \left( t \right) = e ^ { j \left( 2 \pi \left( f _ { \mathrm { c , i n t } } t + \frac { 1 } { 2 } \cdot k _ { \mathrm { i n t } } t ^ { 2 } \right) - \phi _ { 0 , \mathrm { i n t } } \right) }\tag{4}
$$

where $\phi _ { 0 , \mathrm { i n t } }$ is the starting phase and $f _ { c , \mathrm { i n t } }$ is the carrier frequency. The interference occurs when the Tx chirp falls within the time interval $t _ { B _ { \mathrm { R x } } }$ defined by the receiver’s bandwidth $B _ { \mathrm { R x } }$ (see Fig. 2).

The interference between FMCW radars can be classified into same-slope $~ ( k ~ = ~ k _ { \mathrm { i n t } } )$ and different-slope $( k \ \ne \ k _ { \mathrm { i n t } } )$ interference. The probability of occurrence of same-slope interference is small compared to the different-slope interference because the time interval $T _ { B _ { \mathrm { R x } } } ~ \ll ~ T _ { \mathrm { C R I } }$ (due to $B _ { \mathrm { R x } } \ll B )$ , where $T _ { \mathrm { C R I } }$ is the chirp repetition interval [21]. The different-slope interference appears in relatively short bursts in the downconverted baseband signal. The duration of the interference is directly proportional to $B _ { \mathrm { R x } }$ and inversely proportional to the difference between chirp slopes of both radars [22], that is,

$$
T _ { d } = \frac { 2 B _ { \mathrm { R x } } } { | k - k _ { \mathrm { i n t } } | } .\tag{5}
$$

The baseband signal during the interference interval is the sum of the contributions from target reflections and the interfering signal, that is,

$$
s _ { \mathrm { C B , t _ { d } } } \left( t \right) = s _ { \mathrm { C B } } \left( t \right) + s _ { \mathrm { i n t } } \left( t \right) , \quad t \in \left( t _ { 0 } - \frac { T _ { d } } { 2 } , t _ { o } + \frac { T _ { \mathrm { d } } } { 2 } \right)\tag{6}
$$

where $t _ { o }$ is the time instance where Tx and interfering chirps cross each other in the time-frequency domain. If $\tau _ { \mathrm { i n t } }$ is the time delay between the start of the Tx and the interfering chirps, the interference contribution is expressed as

$$
s _ { \mathrm { i n t } } \left( t \right) = A _ { \mathrm { i n t } } e ^ { j \phi _ { \mathrm { i n t } } \left( t \right) }\tag{7}
$$

![](images/e880df606a7fa2dc1d667a8530296d594f0e3867d8603a276e7e8a20d4a54862.jpg)  
(a)

![](images/aa2c26518f275590cec48901b9a501c8fb35adf71419d021f4b77770a25a5494.jpg)  
Fig. 3. Mutual interference between two chirp sequence radars. (a) Time-domain (real-part) plot of a single interfered chirp. (b) Instantaneous frequency versus time plot of the same chirp. The target beat frequency falls only on one side of the spectrum (0 to $B _ { \mathsf { R } \times } )$ , while the interference spans the complete spectrum $( - B _ { \mathsf { R } \mathsf { x } }$ to $B _ { \mathrm { R } \times } )$

where

$$
\phi _ { \mathrm { i n t } } \left( t \right) = \pi \left( k _ { \mathrm { i n t } } - k \right) t ^ { 2 } + \pi \left( f _ { c , \mathrm { i n t } } - f _ { c } \right) t + \phi _ { \mathrm { o f f s e t } } .\tag{8}
$$

The starting phase of $s _ { \mathrm { i n t } } ( t )$ in the interference interval is represented by $\phi _ { \mathrm { o f f s e t } }$ . The time-domain representation (real part) of an interfered baseband signal and the corresponding instantaneous frequencies are shown in Fig. 3.

## C. Pulse Compression

Pulse compression is utilized to improve the resolution as well as the detection and estimation performance of a typical pulse radar [23]. An example of a pulse compression waveform is the linearly frequency-modulated (LFM) waveform, which is defined as

$$
x \left( t \right) = e ^ { j \pi \frac { \beta } { \Gamma } t ^ { 2 } } , \quad - \frac { \Gamma } { 2 } \leq t \leq \frac { \Gamma } { 2 }\tag{9}
$$

where $\beta$ is the pulse bandwidth and  is the pulse duration.

The time-domain response of an LFM pulse is plotted in Fig. 4(a), and the instantaneous frequency is plotted in Fig. 4(b). The compression can be performed by filtering the received echo using a matched filter defined as

$$
h \left( t \right) = x ^ { \ast } \left( - t \right)\tag{10}
$$

where ( ) is the complex conjugation operator. This filter choice maximizes the signal-to-noise ratio (SNR) in the output

$$
y \left( t \right) = h \left( t \right) * x \left( t \right)\tag{11}
$$

where (∗) represents the convolution operation. The Tx pulse energy is compressed in the center of the output y(t) (see Fig. 5). In this work, rather than improving the detection performance, pulse compression is utilized to shorten the duration of the interference contribution in the received baseband signal by compressing a significant portion of the interfering signal to a relatively small time interval.

![](images/f52cb1e89c77d64e1acce60b100b704ec4dc5a23dd2880610887df9e12f04d76.jpg)

(a)  
![](images/e14ec90c273482df929cf62d08b26b5a237f0c0d5f1694e73f9ed83fe67bc062.jpg)  
(b)

Fig. 4. (a) Time-domain response of the linear frequency-modulated pulse. (b) Instantaneous frequency plotted against time for an LFM waveform.  
![](images/2a5f8750e54a8597c8ca5a5c464f4e4354fc840214a9f55f23c75d8a0f28d9ad.jpg)  
Fig. 5. Matched filter response (compressed waveform) for a 20 MHz, 5 μs LFM pulse.

## D. AR Modeling

AR models [24], [25] can be used to predict future samples in a time series. The underlying assumption is that the time series is wide-sense stationary, which means its mean and autocorrelation functions are time-invariant. If a discrete time signal has some missing samples, the information from previous observations can be used to reconstruct the missing samples [17]. Formally, the kth sample of a signal s(k) is estimated using the AR model coefficients $a _ { i }$ as

$$
s \left( k \right) = \sum _ { i = 1 } ^ { p } a _ { i } s \left( k - i \right) + \epsilon _ { k }\tag{12}
$$

where $p$ denotes the AR model order, and $\epsilon _ { k }$ are residuals with zero mean and variance $\sigma ^ { 2 }$ . Several methods of AR coefficient $a _ { i }$ estimation [26] and AR model order $p$ selection [27], [28] are found in the literature. In this work, we use the Akaike information criterion (AIC) [29] to select the AR model order.

## III. INTERFERENCE MITIGATION

Comparing the instantaneous frequency versus time plots for the interfering signal (see Fig. 3) and the LFM waveform [see Fig. 4(b)], it can be observed that both signals have the same frequency versus time characteristics. Moreover, from (8) and (9), it can be seen that the phase progression of the interference in the baseband signal is the same as the phase progression in an LFM pulse. Therefore, similar to the pulse compression principle in the LFM waveform case, it is possible to compress the interference in the received baseband signal, provided that the interference phase $\phi _ { \mathrm { i n t } } ( t )$ is known for the design of the matched filter.

The complete interference mitigation method is composed of the following steps: interference parameter estimation, pulse compression, AR signal reconstruction, and pulse decompression. These steps are described in the sections that follow.

## A. Interference Parameter Estimation

Interference parameters (chirp slope, phase, and amplitude) can be estimated using the method described in [13], provided that the interference has a significantly higher amplitude compared to the target echoes and the interference duration is relatively long. In our work, the aim is to design a matched filter for interference compression. If the matched filter is shifted in phase by $\phi _ { \mathrm { n e w } }$ and scaled in amplitude by $A _ { \mathrm { n e w } }$ that $\mathrm { i } \mathrm { s } .$

$$
h _ { \mathrm { n e w } } \left( t \right) = A _ { \mathrm { n e w } } \cdot x ^ { \ast } \left( - t \right) \cdot e ^ { j \left( \phi _ { \mathrm { n e w } } \right) }\tag{13}
$$

then the corresponding compressed output will simply be shifted in phase and scaled in amplitude, that is,

$$
y _ { \mathrm { n e w } } \left( t \right) = h _ { \mathrm { n e w } } \left( t \right) * x \left( t \right) = A _ { \mathrm { n e w } } \cdot y \left( t \right) \cdot e ^ { j \left( \phi _ { \mathrm { n e w } } \right) }\tag{14}
$$

and there will be no effect on the SNR in the output. Therefore, contrary to [13], it is not essential to estimate accurate phase offset and amplitude of the interference for the purpose of pulse compression. However, it is still required that the estimation of $k _ { \mathrm { i n t } }$ , which determines the interference phase progression, is accurate.

The initial estimates of the interference slope are obtained from (5), which can be rewritten as

$$
k _ { \mathrm { i n t } } = \pm \frac { 2 B _ { \mathrm { R x } } } { T _ { d } } + k .\tag{15}
$$

The interference duration $T _ { d }$ in (15) is determined by identifying the start and end of the interference burst in the received baseband signal, for example, using the interference detection method described in [30]. The number of consecutive disturbed samples in the received baseband signal gives an estimate of $T _ { d }$ . If $T _ { d }$ is known, then using own radar parameters $( B _ { \mathrm { R x } }$ and $k )$ , the slope of the interference is estimated as $( 2 { B _ { \mathrm { R x } } } / { T _ { d } } ) + k ~ \mathrm { o r } - ( 2 { B _ { \mathrm { R x } } } / { T _ { d } } ) + k$ . Consider an own radar with chirp slope k = 800 MHz/40 μs, $\boldsymbol { B } _ { \mathrm { R X } } =$ 10 MHz, and analog to digital converter (ADC) sampling rate of 20 Msps. If the number of disturbed samples is 80, then the interference duration is $T _ { d } = 4 ~ \mu \mathrm { s }$ , and the interference chirp slope is computed to be $k _ { \mathrm { { i n t , + } } } ~ = ~ 2 5 ( \mathrm { { M H z } } / \mu \mathrm { { s } } )$ and $k _ { \mathrm { i n t , - } } = 1 5 ( \mathrm { M H z } / \mu \mathrm { s } )$

## B. Interference Compression

Once the interference chirp slope is estimated, the phase progression of the matched filter is determined by (8). Consequently, the matched filter for interference compression is

$$
h _ { \mathrm { i n t } } \left( t \right) = w \left( t \right) s _ { \mathrm { i n t } } ^ { \ast } \left( - t \right) , t \in \left( t _ { o } - \frac { T _ { d } } { 2 } , t _ { o } + \frac { T _ { d } } { 2 } \right)\tag{16}
$$

![](images/74e4cd4156d985ad53c543cde08c466a7865086d64514963ef487eab7d2d9559.jpg)  
Fig. 6. Magnitude of the filter outputs corresponding to the two interference chirp slope estimations $( k _ { \mathrm { i n t . + } }$ and $k _ { \mathrm { i n t . - } } \big )$ , and the real part of the received baseband signal. The vertical dashed lines (red) represent the interference interval $\bar { T } _ { d } .$ The interference energy is compressed in the center of the interference interval when the matched filter is designed using the slope $k _ { \mathrm { i n t , + } } .$ No interference compression can be observed in filter output corresponding to the slope $k _ { \mathrm { i n t , - } } .$

where w(t) denotes a window function applied to the filter. In this work, we use a Kaiser window, which approximates the discrete prolate spheroidal sequence (DPSS) for maximizing the energy concentration in the main lobe [31]. The Kaiser window parameter $\beta$ determines the tradeoff between the mainlobe width and the sidelobe level. Given the complex baseband signal $s _ { \mathrm { C B } } ( t )$ , the compressed waveform is obtained using the following expression:

$$
y _ { c } \left( t \right) = h _ { \mathrm { i n t } } \left( t \right) * s _ { \mathrm { C B } } \left( t \right) .\tag{17}
$$

The correct interference chirp slope out of the two estimations from Section III-A can be decided by filtering the received signal using the corresponding filter estimates, which results in two different outputs (see Fig. 6). There is no interference compression in the output corresponding to the first estimation $( k _ { \mathrm { i n t , - } } )$ , because the duration of the disturbance in the output is not reduced. However, the interference is compressed in the output signal corresponding to the second estimation $( k _ { \mathrm { i n t , + } } )$ . Therefore, it can be concluded that $k _ { \mathrm { i n t , + } }$ is the correct interference chirp slope.

## C. Signal Reconstruction

The interference in the filter output is concentrated in the center of the interference interval. Moreover, more than 90% of the LFM pulse energy is contained in the mainlobe of the compressed waveform [23]. Therefore, it is possible to remove a significant portion of the interference by removing the mainlobe of the compressed waveform. When a windowed matched filter is used, the width of the mainlobe increases. As a result, the energy in the mainlobe increases further. More interference energy can be removed by discarding more samples from the compressed waveform. However, it would lead to a loss of information from the signal of interest. Discarding the interference-affected samples creates gaps in the resulting waveform, which can be filled by inserting new samples to obtain an interference-free waveform.

If the compressed waveform fulfills the wide sense stationarity condition, one option is to predict the missing samples by estimating an AR model for the compressed waveform [17]. Other sample prediction methods may achieve better signal reconstruction performance in the compressed domain. However, in this work, we use the AR-model-based sample prediction in order to compare the signal reconstruction performance in the fast time and the compressed domain using a well-established sample prediction method.

![](images/ceacb64f0bb47d803b3acd484ed294f9b501b599f5942f951aa4689028da9f70.jpg)  
Fig. 7. Frequency-domain representation of the matched filter and the regularized filter. The minimum magnitude of the regularized filter $H _ { \mathrm { i n t } , r } ( \hbar )$ is -. The phase of $H _ { \mathrm { i n t } , r } ( \hat { I } )$ is the same as of the matched filter $H _ { \mathrm { { i n t } } } ( f )$

After reconstruction, the next step is to decompress the repaired compressed waveform $\bar { y } _ { c } ( t )$ to obtain the baseband signal s¯<sub>CB</sub>(t) without interference. The decompression is performed by dividing the frequency response of $\bar { y } _ { c } ( t )$ by the frequency response of $h _ { \mathrm { i n t } } ( t )$ . This is equivalent to deconvolution in the time domain, which is numerically an ill-posed problem and can introduce unwanted effects in the output [32]. To overcome this problem, the matched filter is regularized for the purpose of decompression. In this work, the regularization is performed by modifying the minimum magnitude of $H _ { \mathrm { i n t } } ( f ) ~ = ~ \mathcal { F } ( h _ { \mathrm { i n t } } ( t ) )$ (here $\mathcal { F }$ represents the Fourier transform) to a threshold  as

$$
| H _ { \mathrm { i n t } , r } \left( f \right) | = \left\{ \begin{array} { l l } { | H _ { \mathrm { i n t } } \left( f \right) | , } & { | H _ { \mathrm { i n t } } \left( f \right) | \ge \epsilon } \\ { \epsilon , } & { | H _ { \mathrm { i n t } } \left( f \right) | < \epsilon } \end{array} \right.\tag{18}
$$

while the phase is kept unchanged (see Fig. 7). The decompressed signal is obtained by frequency-domain deconvolution

$$
\hat { s } _ { C B } \left( t \right) = \mathcal { F } ^ { - 1 } \left( \frac { \mathcal { F } \left( \bar { y } _ { \mathrm { c } } \left( t \right) \right) } { H _ { \mathrm { i n t } , r } \left( f \right) } \right)\tag{19}
$$

where $\mathcal { F } ^ { - 1 }$ represents the inverse Fourier transform.

The complete interference mitigation process is summarized in Fig. 8 using a simulated received baseband signal with interference. The matched filter is estimated using the duration of the interference in s<sub>CB</sub>(t) [see Fig. 8(a)]. The interference is concentrated in the mainlobe of the filter output $y _ { c } ( t )$ [see Fig. 8(b)]. The mainlobe in the filter output is removed, and the remaining signal is repaired by employing an AR model to obtain $\bar { y } _ { c } ( t )$ [see Fig. 8(c)]. Finally, the repaired signal is decompressed using the regularized matched filter $H _ { \mathrm { i n t } , r } ( f )$ to obtain the baseband signal without interference.

## IV. RESULTS

The interference mitigation performance of the proposed method is verified using real radar data. The experimental setup consists of an ego radar mounted on a car moving toward two interfering radars (see Fig. 9). The radar parameters are summarized in Table I.

![](images/151a822aeab1c9e903ac8a224a812653cc336cad0736e575a68ff3f965c16e6f.jpg)

(a)  
![](images/2fe803fb1152d42b7808b3de3df2b1567f9f1c24dafffe9eac09a87e03aa256f.jpg)

(b)  
![](images/9951336069d2bcebb1b39b64ff7dd994985632fdf1fb54a1b1deb22b313ee84b.jpg)

(c)  
![](images/ea968ebd4d0266eaa539888d4f1865782000a5de10359bdc9af0780bf51aa426.jpg)  
(d)  
Fig. 8. Different stages in the interference mitigation process illustrated on a simulated received baseband signal. (a) Received complex baseband signal disturbed by interference. (b) Compressed signal obtained using the windowed matched filter. (c) Repaired signal in the compressed domain. The mainlobe where the interference is concentrated is removed and the signal is reconstructed using the estimated AR model. (d) Decompressed signal with interference removed.

![](images/ac029e8a2e00227a842fe44aa996989f6d9e3cd52cb8a33e0b35602cb7c12df6.jpg)  
Fig. 9. Experimental setup with an ego radar mounted on a moving car. The interfering radars and the reference targets are highlighted. The inset in the top right corner shows the experimental setup from the top. The arrow shows the direction of motion of the ego radar.

## A. Stationarity Test for AR Modeling

Kwiatkowski–Phillips–Schmidt–Shin (KPSS) test [33] is employed to check that the compressed waveforms are stationary and, therefore, can be modeled as AR processes. The test was performed on 2 048 000 real compressed waveforms with varying targets and simulated interference sources. The KPSS test was passed by 90.3% of the real compressed waveforms. Therefore, it can be argued that the compressed waveforms are indeed stationary and can be modeled sufficiently as AR processes.

TABLE I  
EGO AND INTERFERING RADAR PARAMETERS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Ego</td><td rowspan=1 colspan=1>radar</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>76.52 GHz</td></tr><tr><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>850.3MHz</td></tr><tr><td rowspan=1 colspan=1>Chirp duration</td><td rowspan=1 colspan=1> $\overline { { 5 1 . 2 \mu \mathrm { s } } }$ </td></tr><tr><td rowspan=1 colspan=1>Slope</td><td rowspan=1 colspan=1>16.6082 MHz/µs</td></tr><tr><td rowspan=1 colspan=1>Chirp repetition interval</td><td rowspan=1 colspan=1> $\overline { { 7 0 . 0 \mu \mathrm { s } } }$ </td></tr><tr><td rowspan=1 colspan=1>Receiver bandwidth</td><td rowspan=1 colspan=1>4.5 MHz</td></tr><tr><td rowspan=1 colspan=1>Sampling rate</td><td rowspan=1 colspan=1>10.0 Msps</td></tr><tr><td rowspan=1 colspan=1>Interfering r</td><td rowspan=1 colspan=1>adar 1</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>76.44 GHz</td></tr><tr><td rowspan=1 colspan=1>Slope</td><td rowspan=1 colspan=1>13.9529 MHz/µs</td></tr><tr><td rowspan=1 colspan=1>Chirp repetition interval</td><td rowspan=1 colspan=1>70.0 µs</td></tr><tr><td rowspan=1 colspan=1>Interfering r</td><td rowspan=1 colspan=1>adar 2</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>76.8GHz</td></tr><tr><td rowspan=1 colspan=1>Slope</td><td rowspan=1 colspan=1>10.8629 MHz/µs</td></tr><tr><td rowspan=1 colspan=1>Chirp repetition interval</td><td rowspan=1 colspan=1> $\overline { { 1 0 0 . 0 \mu \mathrm { s } } }$ </td></tr></table>

## B. Parameter Selection

In this section, we discuss the selection or estimation of various parameters in the proposed interference mitigation method.

1) Interference Duration $T _ { d } .$ In real situations, it might be difficult to accurately estimate the interference duration $T _ { d }$ from the received signal, due to the relative amplitude of the interference and low-pass filter characteristics. The initial estimate of $T _ { d } .$ , in terms of samples, is obtained by counting the number of disturbed samples based on the amplitude of the received signal. This estimate is then improved by comparing the output for a range of filters and selecting one that provides the maximum amplitude of the mainlobe in the compressed output. Using the criteria mentioned above, the number of disturbed samples is 34 for interference-1 and 17 for interference-2. Consequently, the estimated interfering chirp slopes are $k _ { \mathrm { i n t , } 1 } = 1 3 . 9 6 \mathrm { M H z } / \mu \mathrm { s }$ and $k _ { \mathrm { { i n t } , 2 } } = 1 0 . 6 1 \ \mathrm { M H z } / \mu \mathrm { s }$ (see Fig. 10).

Kaiser window parameter β is influenced by the window length and determines the tradeoff between the relative sidelobe attenuation and the mainlobe width. Different values were tested, and it was observed that $\beta \ : = \ : 5$ is suitable for the window length 17 and $\beta \ = \ 6$ is suitable for the window length 34. For lower $\beta$ values, a significant amount of interference energy started leaking into the sidelobes. For higher β values, a loss in interference compression gain was observed. However, the window parameter selection criteria for the purpose of interference mitigation need to be investigated further.

The threshold  for matched filter regularization is determined by computing the mean squared error (mse), which is

![](images/6168e9da996a77cf662034652befdc5076b7451bba1bb4ecd6a8f970659f8e5c.jpg)

![](images/8cb669d9b2ced05f88376e1c4e571354ed9e6f6b69bf6d3cd88f1358b21e227d.jpg)  
(a)  
(b)

Fig. 10. Interference chirp slope versus maximum amplitude of the compressed signal for the chirp slope estimation of (a) interference-1 and (b) interference-2. The vertical lines show the actual slope, and the red circles in both images show the estimated slopes, selected as the points where the compressed signal has the maximum amplitude.  
![](images/8428ac85838b2c342174ae8e1e3d5d73b5b925f0f20c971b2beece7b6fef96f1.jpg)  
Fig. 11. Magnitude threshold - versus mean squared signal reconstruction error in the decompressed signal corresponding to a frame with interference from “interfering radar $2 . ^ { \prime \prime }$ The error is calculated by comparing the reconstructed signal with the clean (undisturbed) sections of the received signal. The red circle shows the selected threshold after which the reconstruction error converges.

defined as

$$
\mathrm { m s e } = \frac { 1 } { N _ { c } } \sum _ { n \in \mathcal { C } } \left| s _ { \mathrm { C B } } \left[ n \right] - \hat { s } _ { C B } \left[ n \right] \right| ^ { 2 }\tag{20}
$$

where is a set of $N _ { c }$ clean samples in the received baseband signal. We selected  = −65 dB, because the MSE is not reduced further by increasing the threshold (see Fig. 11).

To illustrate the interference compression achieved in the output of the estimated filter, we compare the magnitudes of a sample interfered frame in the time domain and the corresponding frame in the compressed domain (see Fig. 12).

## C. Interference Mitigation—Real Data

The interference mitigation performance of the proposed method is evaluated using real interference data corresponding to three scenarios. In scenario-1, the interference in the received signal is caused by “interfering radar-1,” in scenario-2, the interference is caused by “interfering radar-2,” and in scenario-3, the interference is caused by both radars. The time-domain baseband signal and the RD maps corresponding to the three scenarios illustrate that the proposed method suppresses the interference while keeping the signal of interest unaffected (see Fig. 13). The target signal-tointerference-and-noise ratio (SINR) is used as a quantitative measure of interference mitigation performance (see Table II).

![](images/04d6bf1edf51bcb1998cae4c1e07e46a8aa687e3fcf5b22c2043464b65c9e39e.jpg)

(a)  
![](images/99ce682e42629be4fb57481396034c6054a54402d7b8a707590c7b22b09bd772.jpg)  
(b)  
Fig. 12. Comparison of sample magnitudes of a (a) baseband signal frame disturbed by a single interference and the (b) corresponding frame in the compressed domain.

TABLE II  
TARGET SINRS IN THE RD MAPS
<table><tr><td>Scenario</td><td>Case</td><td>Target-1</td><td>Target-2</td></tr><tr><td>1</td><td>Interfered Reconstructed Clean</td><td>10.3 dB 24.6 dB 24.6 dB</td><td>29.2 dB 42.3 dB 41.7 dB</td></tr><tr><td>2</td><td>Interfered Reconstructed Clean</td><td>24.9 dB 27.3 dB 28.7 dB</td><td>39.2 dB 40.5 dB 41.8 dB</td></tr></table>

In the RD domain, the SINR is defined as

$$
\mathrm { S I N R } = 1 0 \log \frac { \frac { 1 } { N _ { T } } \sum _ { \left\{ n , m \right\} \in { \mathcal T } } \left| \mathrm { R D } \left[ n , m \right] \right| ^ { 2 } } { \frac { 1 } { N _ { N } } \sum _ { \left\{ n , m \right\} \in { \mathcal N } } \left| \mathrm { R D } \left[ n , m \right] \right| ^ { 2 } }\tag{21}
$$

where n and m are row and column indices of the RD matrix, respectively, is a set of target cells, and $\mathcal { N }$ is a set of noise plus interference cells (see Fig. 14). It can be observed that the interference is removed in the reconstructed signal and target SINRs comparable to the clean signal are obtained. In scenario-3, the interference noise is concentrated at around 4.5 m/s in the Doppler domain; therefore, there is no degradation in target SINRs.

Since the clean versions of the interfered frames are not available, we use the next frame in the sequence of frames as a clean reference. Similarly, in the case of the real baseband signal, we use a clean chirp from the same frame as a reference. In scenario-3, where interference from two sources is observed, both disturbances are removed by sequentially performing the pulse compression, reconstruction, and pulse decompression steps for each interference source.

For further quantitative evaluation of the proposed method (AR model-based signal reconstruction in the compressed domain, abbreviated hereinafter as AR-CD), the worst interference-affected regions in the RD maps corresponding to the three scenarios are identified and the noise levels are compared (see Table III). The first two rows of the table define the worst interference-affected RD map regions and the next three rows show the noise levels.

The signal reconstruction performance of the proposed method is compared with the AR model-based signal reconstruction in the fast-time domain [17] (abbreviated hereinafter as AR-TD) and the IMAT algorithm-based reconstruction [14]. As proposed in [14], the minimum threshold for the IMAT algorithm is set to 10 dB above the noise floor, which is estimated from the clutter-free image band.

![](images/761a9f0b48fbf2f9215b6374735ca09b371e8c26072cc238ce8645b029cac3e9.jpg)

![](images/c0de2f36b71f65dc878713a0b86834a37b28a52b51989ca01a48fe5d9d0768fd.jpg)  
(a)

![](images/328c80f79cea69f2cfa971d4e4083a6b20ca8a8954c79944a1081cebe8d6b31a.jpg)  
(b)

![](images/c8c0f17bea0cdfc2511528c3cc4de99bc773f9a657cc13666940102b25cfccd3.jpg)

(c)  
![](images/77e5f6ef7d52aa6ff028961e7fc2577bf2de353100e7a7159fcc6cc6bbb15e1c.jpg)  
(d)

![](images/610d290db7654d29706b1bbdfe9b188a2e4f1181e73f5cdda65a4324840b430f.jpg)

(e)  
![](images/3430706012c71191a00cf9baa0b78db953fb4536480d85b3eb32a097f3e34178.jpg)

(f)  
![](images/5b3fa56112e75d805fbf47c9ce8ccc0d4af27b59198c6fb5e573dac361ebc82a.jpg)

![](images/a7263c65dca72b427ca9b6a15599efea8e8890c0e3acdf806ba20edb7d60a5ca.jpg)

(g)  
![](images/d18404f20726e10f1d873a35b62f17f2eae6b64cd6d38753a249663643b299a3.jpg)

(h)  
(i)  
![](images/f7abbe715b52dcda8c24e7e7b804bc9726094b1e6b4b1f20cb4c813a74fb7449.jpg)  
(i)  
(k)

![](images/34c950b03ab2117319c41fc412d7e877737d0a6368a024c32a361c52ffcd628a.jpg)

![](images/98a0651a4047ebb145301b4b0e4ad3a13ba709641fbe11b4289095486c5ee24c.jpg)  
(m)

(l)  
![](images/843282bdae6f830ca16b407ba733aaf6ff092780e389a9651e6fab55b3473405.jpg)  
(n)

![](images/298e046d9adfad02c5ce25e1f21d2ca54033b3e09f410e838d26bd161c8a4d81.jpg)

![](images/36965006dc67faf01a8e7ed3c2e94332357e80398034e4540f0be7cf6abdbad5.jpg)

(p)  
![](images/e2b0c1a32a1c514db85d775fda0e4bdb36876d904d752b53630d74d18be3439c.jpg)  
(q)

(0)  
![](images/c41d5e3b19a6db0a4c4b238a08fc4c652ca14803dce4ebf2227ab10839e9a39c.jpg)  
(r)  
Fig. 13. Comparison of the RD maps and real part of the baseband signal (corresponding to a single chirp) for interfered (left), reconstructed (middle), and clean (right) signals. (a)–(f) Correspond to scenario-1. (g)–(l) Correspond to scenario-2. (m)–(r) Correspond to scenario-3. The relative position of target-1 and target-2 is highlighted in (c).

![](images/d02b8f1e510b28e2dedce4e7859880cc1690ffd617328afee007cf979ecec86d.jpg)  
Fig. 14. Principal setup of target cells <sub>T</sub> (green) and noise plus interference cells (red) for SINR calculation in the RD matrix. Guard cells (gray) are typically used to reduce the effect of target sidelobes or other nearby targets on SINR.

TABLE III  
NOISE LEVELS IN THE WORST AFFECTED REGIONS OF THE NORMALIZED RD MAPS
<table><tr><td></td><td>Scenario-1</td><td>Scenario-2</td><td>Scenario-3</td></tr><tr><td>Range (m) Doppler (m/s)</td><td>16- 34 0.0 - 0.4</td><td>7- 25 4.9 - 6.0</td><td>7- 25 3.6 - 5.1</td></tr><tr><td>Interfered Reconstructed Clean</td><td>-31.2 dB -47.0 dB -46.9 dB</td><td>-41.7 dB -46.3 dB -46.2 dB</td><td>-30.0 dB -44.7 dB -45.8 dB</td></tr></table>

TABLE IV

TARGET SINR COMPARISON FOR DIFFERENT SIGNAL RECONSTRUCTION METHODS
<table><tr><td>Method</td><td>Target-1</td><td>Target-2</td></tr><tr><td>AR-TD</td><td>36.2 dB</td><td>26.4 dB</td></tr><tr><td>AR-CD IMAT</td><td>38.0 dB 38.0 dB</td><td>28.0 dB 28.1 dB</td></tr></table>

A comparison of the time-domain signal frames (see Fig. 15) shows that AR-TD struggles to predict the samples directly in the fast-time domain. We can also observe a clear discontinuity in the sample magnitudes of the frame reconstructed using the IMAT algorithm. The signal reconstruction performance improves with AR-CD since there is no clearly visible discontinuity in the reconstructed frame.

The sidelobe levels in the region highlighted using the orange rectangles in the corresponding RD maps (see Fig. 16) indicate a better signal reconstruction performance using AR-CD and IMAT compared to AR-TD. For strong scatterers, a comparable signal reconstruction performance is achieved with IMAT and AR-CD (see SINR values in Table IV). However, the proposed method is better able to recover the relatively weak scatterers (highlighted with white rectangles in Fig. 16) in the RD map.

## V. DISCUSSION

Repairing the received baseband signal by AR reconstruction in the time domain means that all samples of the signal of interest within the interference duration are lost. The proposed method compresses the interference, but the signal of interest does not undergo any compression. Therefore, when the interference is removed in the compressed domain, only a small portion of the signal of interest is lost. As a consequence, AR-CD outperforms AR-TD, especially when a relatively large percentage of the samples are affected by the interference (see Fig. 17). When a small percentage of the received samples are disturbed, the time-bandwidth product would be small, leading to a lower compression gain. In such situations, it might be better to perform the signal reconstruction directly in the fast-time domain.

![](images/d988a5f62ea6cc7c239adfd1498f96aed71f8562fa99ac7b9891a426a2f0645d.jpg)

(a)  
![](images/70f51f556c6387805c2afd9dc040898f807e4c131dd7726da2b770311fe0c4fa.jpg)  
(b)

![](images/be36ce1c5e796f000ab252e1cc0bffeb94b395bdbaf75573d76b67ea747452e9.jpg)  
(c)  
Fig. 15. Comparison of sample magnitudes of a signal frame reconstructed using (a) AR-TD, (b) AR-CD, and (c) IMAT.

![](images/3594c3b974f8fcaab7d7f456784d2f54e2455c0b5a534edd840357917818f3db.jpg)  
(a)

![](images/72128301d2f10a0a0350b460c6dacc08a4dba8b4bd3dcaa92c0ced9a3606b957.jpg)  
(b)

![](images/a5d0f5b5b4e5a4535d872d7c382ad5e3f9bc1e1a7ba14dddf81e35010e2fcc7f.jpg)  
(c)  
Fig. 16. Comparison of the RD maps corresponding to the baseband signal frames in Fig. 15. The frame reconstructed using (a) AR-TD, (b) AR-CD, and (c) IMAT. The orange and white rectangles highlight the strong and weak scatterers, respectively.

An important prerequisite for the proposed method to successfully suppress interference is that the interference is detected and the disturbed samples are identified correctly. This task becomes more complicated when there is interference from multiple sources because the samples identified as interfered have to be assigned to a particular interfering radar. In this study, we use the prior information that there are two interference sources to assign disturbed samples to either interference-1 or interference-2 based on the number of consecutive disturbed samples. However, when there is an unknown number of interfering radars, more sophisticated interference detection methods need to be applied.

![](images/9f52fb87d8c48dfeb53d6dc44e266495907de36fef6426960cad2d07346da90b.jpg)

(a)  
![](images/d816d5f492adc50aa8867548c39a6c4ef5931fa859f1d9aa539fc37572dd7742.jpg)  
(b)

![](images/4457b931d37137c634b02272e5af302c4ba6ae3671f97e5ea9b505c6a27c70ae.jpg)  
(c)

![](images/8f411c2c5500f810bd940d8a3393a2ad4642b8a4ef708c59ac40cf52291cab3e.jpg)  
(d)  
Fig. 17. Simulation-based comparison of AR-TD and AR-CD when approximately 7% and 35% of the baseband signal samples are disturbed by the interference. (a) Time-domain plots, long-duration interference. (b) Range profiles, long-duration interference. (c) Time-domain plots, short-duration interference. (d) Range profiles, short-duration interference. The difference in the signal reconstruction performance can be seen in the range profiles in (b) and (d). Targets in (b) for the signal reconstructed in TD have lower SINR and higher side lobes, especially the ones further than 10 m. There is no significant difference in the signal reconstruction performance for the short-duration interference, at least in the range profiles.

The performance of the slope estimation method proposed in this study depends directly on the efficiency of the interference detection method used and may have some limitations in certain scenarios. Therefore, more research should be done to find a better method rather than evaluating the performance of the proposed one.

## VI. CONCLUSION

This article describes a method for mutual interference mitigation in mm-wave FMCW radar, which is validated using real measurements. After detecting interference in the received signal, the chirp slope of the interfering signal is estimated using the interference dwell time and the receiver bandwidth. A matched filter is designed using the estimated slope, and pulse compression is performed to compress interference in the filter output. In the compressed output, most of the interference energy is concentrated in the center of the interference interval. The interference is mitigated by removing the interference-related mainlobes from the compressed waveform and restoring the missing samples using AR model-based sample prediction. The advantage of performing sample prediction in the compressed domain instead of the time domain is a significant reduction in the number of samples to be predicted. However, if the interference duration is relatively short, it may be better to predict signal samples directly in the time domain. The interference-free baseband signal is retrieved by decompressing the restored compressed waveform using a regularized matched filter, which ensures numerical stability. Results from real outdoor measurements show that interference is effectively suppressed down to the noise floor, and for this particular experiment, the pulse compression-aided AR signal reconstruction achieves a target SINR gain of about 14 dB. The results also demonstrate that this method can be applied to situations where the interference is caused by multiple sources.

## ACKNOWLEDGMENT

The authors would like to thank Dr. Saleh Javadi for his support during the radar experiment.

## REFERENCES

[1] J. Dickmann, J. Klappstein, H.-L. Blöcher, M. Muntzinger, and H. Meinel, “Automotive radar—‘Quo vadis?”’ in Proc. 9th Eur. Radar Conf., 2012, pp. 18–21.

[2] C. Waldschmidt, P. Hügler, and M. Geiger, “Radar as an emerging and growing technology for industrial applications: A short overview,” in Proc. Sensor, 2017, pp. 460–465.

[3] P. D. L. Beasley, “Advances in millimetre wave FMCW radar,” in Proc. Microw., Radar Remote Sens. Symp., Sep. 2008, pp. 246–249.

[4] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[5] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[6] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[7] C. Waldschmidt, J. Hasch, and W. Menzel, “Automotive radar—From first efforts to future systems,” IEEE J. Microw., vol. 1, no. 1, pp. 135–148, Jan. 2021.

[8] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility (ICMIM), May 2016, pp. 1–4.

[9] M. Zhang, S. He, C. Yang, J. Chen, and J. Zhang, “VANET-assisted interference mitigation for millimeter-wave automotive radar sensors,” IEEE Netw., vol. 34, no. 2, pp. 238–245, Mar. 2020.

[10] F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, and M. Gashinova, “Automotive radar waveform parameters randomisation for interference level reduction,” in Proc. IEEE Radar Conf. (RadarConf), Sep. 2020, pp. 1–5.

[11] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[12] C. Wang, J. Tong, G. Cui, X. Zhao, and W. Wang, “Robust interference cancellation for vehicular communication and radar coexistence,” IEEE Commun. Lett., vol. 24, no. 10, pp. 2367–2370, Oct. 2020.

[13] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, Apr. 2015, pp. 1–4.

[14] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[15] M. Alhumaidi and M. Wintermantel, “Interference avoidance and mitigation in automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 172–175.

[16] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 726–731.

[17] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[18] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2020, pp. 3802–3806.

[19] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320.

[20] V. Winkler, “Range Doppler detection for automotive FMCW radars,” in Proc. Eur. Microw. Conf., 2007, pp. 166–169.

[21] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Automotive radar—Investigation of mutual interference mechanisms,” Adv. Radio Sci., vol. 8, pp. 55–60, Sep. 2010. [Online]. Available: https://www.advradio-sci.net/8/55/2010/

[22] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, pp. 371–378, Mar. 2014.

[23] M. A. Richards, Principles of Modern Radar: Basic Principles (Radar, Sonar Navigation). London, U.K.: Institution of Engineering and Technology, 2010. [Online]. Available: https://digitallibrary.theiet.org/content/books/ra/sbra021e

[24] C. Chatfield, The Analysis of Time Series: An Introduction, 6th ed. Boca Raton, FL, USA: CRC Press, 2004.

[25] D. Dickey and W. Fuller, “Distribution of the estimators for autoregressive time series with a unit root,” J. Amer. Stat. Assoc., vol. 74, pp. 427–431, Jun. 1979.

[26] S. M. Kay and S. L. Marple, “Spectrum analysis—A modern perspective,” Proc. IEEE, vol. 69, no. 11, pp. 1380–1419, Nov. 1981.

[27] J. R. Dickie and A. K. Nandi, “A comparative study of AR order selection methods,” Signal Process., vol. 40, nos. 2–3, pp. 239–255, Nov. 1994.

[28] J. Ding, V. Tarokh, and Y. Yang, “Model selection techniques: An overview,” IEEE Signal Process. Mag., vol. 35, no. 6, pp. 16–34, Nov. 2018, doi: 10.1109/MSP.2018.2867638.

[29] H. Akaike, “Information theory and an extension of the maximum likelihood principle,” in Selected Papers of Hirotugu Akaike, E. Parzen, K. Tanabe, and G. Kitagawa, Eds. New York, NY, USA: Springer, 1998, pp. 199–213, doi: 10.1007/978-1-4612-1694-0\_15.

[30] Y. Watanabe and K. Natsume, “Interference determination method and FMCW radar using the same,” U.S. Patent 7 187 321, Mar. 6, 2007.

[31] D. M. Gruenbacher and D. R. Hummels, “A simple algorithm for generating discrete prolate spheroidal sequences,” IEEE Trans. Signal Process., vol. 42, no. 11, pp. 3276–3278, Nov. 1994.

[32] R. N. Neelamani, H. Choi, and R. Baraniuk, “ForWaRD: Fourier-wavelet regularized deconvolution for ill-conditioned systems,” IEEE Trans. Signal Process., vol. 52, no. 2, pp. 418–433, Feb. 2004.

[33] D. Kwiatkowski, P. C. B. Phillips, P. Schmidt, and Y. Shin, “Testing the null hypothesis of stationarity against the alternative of a unit root: How sure are we that economic time series have a unit root?” J. Econometrics, vol. 54, nos. 1–3, pp. 159–178, Dec. 1992. [Online]. Available: http://www.sciencedirect.com/science/article/pii/030440769290104Y

![](images/7969121da4f062202bd74b39217ea5e0f8ec0bd85981d9a4d0cd49ca6b5016bd.jpg)

Muhammad Rameez received the B.E. degree in electrical engineering from the National University of Sciences and Technology, Islamabad, Pakistan, in 2010, and the M.Sc. degree in communications technology from the University of Ulm, Ulm, Germany, in 2016. He is currently pursuing the Ph.D. degree in systems engineering with the Blekinge Institute of Technology, Karlshamn, Sweden.

His research interests include radar signal processing and automotive radar interference mitigation techniques.

![](images/78bd0f0f8f04b6a13fbe4ea2c4ad5faed15c25d66230d6386f00755c346d8761.jpg)

Mats I. Pettersson (Senior Member, IEEE) received the M.Sc. degree in engineering physics, the Licentiate degree in radio and space science, and the Ph.D. degree in signal processing from the Chalmers University of Technology, Gothenburg, Sweden, in 1993, 1995, and 2000, respectively.

He worked with Mobile Communication Research at Ericsson, Stockholm, Sweden. He was with the Swedish Defense Research Agency (FOI) for ten years. At FOI, he focused on

ultrawide band low-frequency synthetic aperture radar (SAR) systems. Since 2005, he has been with the Blekinge Institute of Technology (BTH), Karlskrona, Sweden, where he is currently a Full Professor. He has authored or coauthored over 200 scientific publications, of which approximately 60 are in peer-reviewed scientific journals. His research is related to radar surveillance and remote sensing. His main research interests include SAR processing, space–time adaptive processing (STAP), high-resolution SAR change detection, automotive radar, radio occultation, THz SAR, and computer vision.

![](images/830c5076698a58d6f3d973cd667ffba08a2b11780a8d8da4fa312dd0fb94d886.jpg)

Mattias Dahl (Member, IEEE) received the B.Sc. degree in electrical engineering from the Chalmers University of Technology, Gothenburg, Sweden, in 1989, the M.Sc. degree in computer science from the Luleå Institute of Technology, Luleå, Sweden, in 1993, the Licentiate degree in signal processing engineering from Lund University, Lund, Sweden, in 1996, and the Ph.D. degree in applied signal processing from the Blekinge Institute of Technology, Karlskrona, Sweden, in 2000.

Since 2018, he has been a Full Professor with the Blekinge Institute of Technology. He has authored more than 100 scientific publications and five patents (the latest filed in 2018).

Dr. Dahl has received several awards from Sweden’s Innovation Agency and the Swedish Foundation of Technology Transfer.