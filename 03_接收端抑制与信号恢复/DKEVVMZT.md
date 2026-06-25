# CFAR-Based Interference Mitigation for FMCW Automotive Radar Systems

Jianping Wang, Member, IEEE

Abstract—In this paper, constant false alarm rate (CFAR) detector-based approaches are proposed for interference mitigation of Frequency modulated continuous wave (FMCW) radars. The proposed methods exploit the fact that after dechirping and low-pass filtering operations the targets’ beat signals of FMCW radars are composed of exponential sinusoidal components while interferences exhibit short chirp waves within a sweep. The spectra of interferences in the time-frequency (t-f) domain are detected by employing a 1-D CFAR detector along each frequency bin and then the detected map is dilated as a mask for interference suppression. They are applicable to the scenarios in the presence of multiple interferences. Compared to the existing methods, the proposed methods reduce the power loss of useful signals and are very computationally efficient. Their interference mitigation performances are demonstrated through both numerical simulations and experimental results.

Index Terms—Beat signal, Constant false alarm rate (CFAR) detector, FMCW radar, Interference mitigation, time-frequency speatrum.

## I. INTRODUCTION

N <sup>OWADAYS</sup> <sup>frequency</sup> <sup>modulated</sup> <sup>continuous</sup> <sup>wave</sup> (FMCW) radars have become a key device for automotive assistant/autonomous driving due to its operational capability in all day time and all weather conditions as well as its low cost. With the increase of vehicles equipped with radar sensors, the FMCW radar systems mounted on different cars in busy area will inevitably suffer from strong interfering influence from the radar systems on the neighboring cars as well as other radars on the same car when they operate at the same time. The strong interferences would cause significantly increased noise floor, weak target mask and reduced probability of target detection. Therefore, to overcome these risks, effectively mitigating interferences from other radars is critical to high-performance automotive radars.

Interference mitigation (IM) for automotive radar is a hot topic in recent years. In the literature, many approaches have been proposed and developed to suppress the interferences among different automotive radars, which can be classified into three categories: radar system coordination, radar system design and waveform design, and signal processing. For the radar system coordination approaches, a coordination scheme, which is either centralized [1] or distributed [2], [3], among different operational radars are devised to avoid conflicts by adjusting the operating parameters (i.e.,transmitting time, spectrum, etc.) of each radar within the interfering area.

Although these coordination schemes originated from communication network could effectively avoid certain interferences, they usually require to introduce an extra coordination unit to the the existing FMCW radar systems or need communication with a coordination center for a local distributed radar network.

On the other hand, some new radar system architectures and waveforms are proposed to benefit the interference mitigation [4]–[10]. The frequency-hopping random chirp (FHRC) FMCW technique [4], [5] and FMCW radar with random repetition interval [6] resets the parameters of the chirp signals (the bandwidth, sweep duration, center frequency, repetition interval) every cycle to result in noise-like frequency responses of mutual interferences after the received signals are downconverted and demodulated. Both techniques would mitigate partial interferences and avoid the appearance of ghost targets caused by mutual interferences. However, the randomized repetition intervals would cause the Fast Fourier transform, which is conventionally used, inapplicable for the fast Doppler processing. On the other hand, pseudo-random noise signals [8] and chaotic sequences [7] are proposed to mitigate mutual interferences for automotive radars. For these radar systems, the received signals are processed by the correlation operation and a high sampling frequency is generally required for the Analog-to-Digital Converter (ADC), which would increase the cost of the radar systems. To exploit the advantages of both noise-like signals and the FMCW radar system, phase modulated (PM) FMCW radar systems modulate the FMCW waveforms with orthogonal or random sequences as transmitted signals [9], [10]. In reception, the received PM-FMCW signals can be down-converted as the traditional FMCW radars and then decoded by correlation with the stored sequences used for transmission modulation. The scattered signals resulting from the transmitted signals generally result in high correlation peaks while the uncorrelated interferences would spread out and build up the noise floor after decoding. Consequently, the raised noise floor could overwhelm the weak targets and reduce the probability of detection. In addition, PM-FMCW radar requires to design a new radar architecture, which cannot be easily implemented with the existing FMCW radar chips.

Moreover, for the FMCW radars, a number of signal processing approaches to interference mitigation have been presented, which includes both traditional signal processing methods and deep-learning based methods. The traditional signal processing methods usually address the interference mitigation by filtering or separating the interferences from the received signals in various domains (i.e., space, time, frequency, time-frequency, etc). For array-based radar system, interference mitigation can be achieved by constructing nulls in the directions of arrival (DOA) of the interferences through beamforming [11]–[13]. However, these approaches would suppress targets’ signals scattered from the same DOAs of the interferences. In [14], the interference is detected based on a threshold and then suppressed by windowing in time. In [15], an iterative modified method based on empirical mode decomposition is proposed to decompose the low-pass filter output of an FMCW radar as a series of empirical modes in the time domain while in [16] the wavelet denoising method is used to separate interferences from the useful signals. Both approaches implicitly assume interferences are sparse in time in the received signals and their performances would degrade with the increase of the proportion of interferencecontaminated samples in the acquired signal. By contrast, the Adaptive Noise Canceller (ANC) [17] is utilized to suppress interferences in the frequency domain. Although it is computationally very efficient, its performance heavily depends on if a proper correlated reference input of the adaptive filter can be found. Meanwhile, in [18] the interference-contaminated signal samples of FMCW radars are first cut out in the shorttime-Fourier-transform (STFT) domain and then a Burg-based methods is developed to reconstruct the signal in the cutout region based on an auto-regressive (AR) model along each frequency bin. However, with the increase of the cut-out region in the signal, the accuracy of the recovered signals with this approach drops rapidly. Moreover, recently some deeplearning approaches are used for interference mitigation of FMCW radars [19], [20]. These approaches generally require a large volume of dataset acquired in various situations for training.

In this paper, we proposed two constant false alarm rate detector (CFAR) [21] based approaches to mitigate interferences for FMCW radars. In both approaches, the acquired beat signal is transformed into the time-frequency $\left( t \ – f \right)$ domain by using the STFT. Then a one-dimensional (1-D) CFAR detector is utilized to detect interferences and the detection map is dilated to generate a mask for interference suppression. Specifically, one approach is to zero out the interference-contaminated samples and the other one is to keep their phases unchanged but correct their amplitudes by the mean of the amplitudes of the interference-free samples in the corresponding frequency bin based on the dilated detection map, which are termed as the CFAR-Zeroing (CFAR-Z) and CFAR-Amplitude Correction (CFAR-AC) approaches in the paper. Compared to the existing approaches, the proposed approaches are capable to mitigate multiple interferences and minimize the power loss of useful signals. Their interference mitigation performance have been validated through both numerical simulations and experimental results. Moreover, they is very efficient and can be implemented for real-time interference mitigation of FMCW automotive radars.

The rest of the paper is organized as follows. Section II briefly describes the signal model of the FMCW radar. Then, the CFAR-based interference mitigation approaches are presented in section III.To demonstrate the interference mitigation performance of the proposed approach, numerical simulations and experimental results are shown in sections IV and $\mathrm { v . }$ Finally, some conclusions are drawn in section VI.

## II. SIGNAL MODEL AND CFAR-BASED INTERFERENCE MITIGATION METHOD

Assume that the transmitted signal $p ( t )$ by an FMCW radar is given by

$$
p ( t ) = \exp \left[ j 2 \pi \left( f _ { 0 } t + \frac { K } { 2 } t ^ { 2 } \right) \right]\tag{1}
$$

where $f _ { 0 }$ is the starting frequency of the FMCW sweep, and $K$ is the sweep slope. Considering the single bounce scattering, then the signals scattered back from point-like targets are the superposition of the time-delayed transmitted signals. Meanwhile, assume that the scattered signals from targets are contaminated by an interference $s _ { \mathrm { i n t } } ( t )$ during its reception. After dechirping and low-pass filtering operating on receiver, the acquired beat signals is represented as

$$
\begin{array} { l } { { \displaystyle s ( t ) = s _ { b } ( t ) + \tilde { s } _ { \mathrm { i n t } } ( t ) + n ( t ) } } \\ { { \displaystyle \quad = \sum _ { i = 1 } ^ { M } a _ { i } \exp \left( - j 2 \pi f _ { b , i } t \right) + \mathcal { F } _ { l p } \left( s _ { \mathrm { i n t } } ( t ) \cdot p ^ { * } ( t ) \right) + n ( t ) } } \end{array}\tag{2}
$$

where $\mathcal { F } _ { l p }$ is the low-pass filtering operator whose cut-off frequency is determined by the desired maximum detectable range of targets. $\begin{array} { r } { s _ { b } ( t ) = \dot { \sum _ { i = 1 } ^ { M } } a _ { i } \exp \left( - j 2 \pi f _ { b , i } t \right) } \end{array}$ is the beat signals of M scatterers, which is composed of M complex exponentials with the beat frequency $f _ { b , i }$ and scattering coefficient $a _ { i }$ for the $i ^ { \mathrm { { t h } } }$ scatterer. Note here a residual video phase term is subsumed by $a _ { i }$ for conciseness. $\tilde { s } _ { \mathrm { i n t } } ( t ) = \mathcal { F } _ { l p } ( s _ { \mathrm { i n t } } ( t )$ $p ^ { * } ( t ) )$ is the remaining interference after the low-pass filtering, and n(t) denotes the noise and measurement errors. According to the analysis in [22], the interference $\tilde { s } _ { \mathrm { i n t } } ( t )$ in (2) generally exhibits as some short chirp-like pulses in the time domain. Although FMCW interferences with the same sweep slope and frequencies falling into the receiving bandwidth would result in ghost targets, its probability is extremely small [23]. Therefore, After taking the STFT of $s ( t )$ , the time-frequency $\left( t \ – f \right)$ domain counterparts of the beat signals of scatterers show as straight lines along the corresponding frequency bins while interferences display as oblique lines, as illustrated in Fig. 1(b). These different distributions of useful beat signals and interferences motive us to proposed the CFAR-based interference mitigation approach in the following.

## III. CFAR-BASED INTERFERENCE MITIGATION APPROACH

Accurately detecting interferences is crucial for effective interference mitigation. Based on the above analysis of different distribution features of useful signals and interferences in the $t \mathrm { - } f$ domain, i.e., straight lines for useful signals along the frequency bin and oblique lines for interferences, detecting interferences can be converted to distinguish the signals distributed along oblique lines relative to the frequency axis. Therefore, we propose to utilize a 1-D CFAR detector along each frequency bin in the $t \mathrm { - } f$ domain to detect interferences and then suppress them.

The complete CFAR-based interference mitigation method is shown in Algorithm 1. In principle, it contains three major steps in implementation, which are described in detail as follows.

Algorithm 1: CFAR-based interference mitigation   
method.   
Data: Complex signal s in a sweep   
Result: Complex signal $\mathbf { s } _ { c }$ after interference mitigation   
begin   
$\mathbf { S } _ { t f } = \mathbf { S } \mathbf { T } \mathbf { F } \mathbf { T } ( \mathbf { s } ) ; [ N _ { r } , N _ { c } ] = \mathbf { s i z e } ( \mathbf { S } _ { t f } ) ;$   
$\begin{array} { r } { \dot { \mathbf { P } } _ { t f } = \mathbf { S } _ { t f } \odot \bar { \mathbf { S } } _ { t f } ; } \end{array}$   
for $k = 1$ to $\textstyle { N _ { r } } $ do   
D(k, :) = CFARDetector $[ \mathbf { P } _ { t f } ( k , : ) ] ;$   
end   
$\mathbf { D } _ { d l } =$ maskDilate(D);   
$\begin{array} { r } { \mathbf { S } _ { t f } ( \mathbf { D } _ { d l } ) = 0 ; } \end{array}$   
$\begin{array} { r } { \mathbf { s } _ { c } = \mathbf { I S T F T } ( \mathbf { S } _ { t f } ) ; } \end{array}$   
end

## A. Time-Frequency Analysis with the STFT

Applying the STFT to the acquired signal in (2), its $t \mathrm { - } f$ spectrum is obtained as

$$
S ( \tau , f ) = \int _ { - \infty } ^ { \infty } s ( t ) w ( t - \tau ) e ^ { - j 2 \pi f t } d t\tag{3}
$$

where $w ( \tau )$ is the window function, for instance, a Gaussian window or Hann window. For N discrete signal samples $s [ k ] = s ( k \Delta t ) , k = 0 , 1 , \cdots , N - 1$ , the discrete $t \mathrm { - } f$ spectrum samples over a regular grid are generally computed by

$$
\begin{array} { l } { { S _ { t f } [ m , n ] = S ( m \Delta \tau , n \Delta f ) \nonumber } } \\ { { \nonumber } } \\ { { \displaystyle \ = \sum _ { k = 0 } ^ { N - 1 } s ( k \Delta t ) w ( k \Delta t - m \Delta \tau ) e ^ { - j 2 \pi n k \Delta f \Delta t } \Delta t } } \end{array}\tag{4}
$$

where $\Delta t$ is the time sampling interval, $\Delta \tau$ is the sliding step of the window and $\Delta f$ is the step of frequency samples. One can see that for a fixed time delay $m \Delta \tau$ of the window, (4) can be efficiently implemented by using the fast Fourier transform (FFT). For the convenience of computation, generally $\Delta \tau = l \cdot \Delta t$ and $l \geq 1$ is an integer. Sliding the window over the signal duration, the $t \mathrm { - } f$ spectrum is obtained as a two-dimensional matrix with dimensions of $N _ { t } \times N _ { f }$ along the time and frequency axes, respectively, where $\dot { N _ { t } }$ is the number of sliding steps of the time window and $N _ { f }$ is the number of FFT points.

Then, the spectrogram is obtained as the amplitude squared of the t-f spectrum, given by

$$
P _ { t f } [ m , n ] = \left| S _ { t f } [ m , n ] \right| ^ { 2 } = S _ { t f } [ m , n ] \cdot \bar { S } _ { t f } [ m , n ]\tag{5}
$$

where $\bar { S } _ { t f }$ is the complex conjugate of $S _ { t f }$

## B. CFAR Detection and Detection Mask Dilation

In this step, the interference detection is performed. After getting the power spectrogram, a Cell Averaging CFAR (CA-CFAR) detector [21] is utilized to the spectrum density along each frequency bin, resulting in a detection matrix D with the same size as the spectrogram. The detection matrix D has the entries of ones and zeros and the entries of one indicate the positions of the detected interferences. The numbers of guard cells and training cells, the probability of false alarm and the threshold factor of the CFAR detector can be set based on the different scenarios.

After acquiring the detection map with the CFAR detector, in principle it could be employed as a mask to suppress interferences. However, due to the possible existence of several interference-contaminated spectral samples in a frequency bin, a relatively large threshold value would be calculated; thus, it causes the missed detection of some edge cells of the interferences. To alleviate such problem, a dilation procedure [24], which is widely used for image processing, is introduced to slightly swell the detected mask of interferences. Considering the detection map D as a binary image, the one-valued pixels form a pattern of the detected interferences, denoted as I. To dilate the pattern I, a structuring element B is used and its origin is translated throughout the entire domain of the input image D. The dilation of the pattern I by the structuring element B is defined as the set operation

$$
I _ { d l } = I \oplus B = \left\{ z | ( \hat { B } ) _ { z } \cap I \neq \varnothing \right\}\tag{6}
$$

where $\hat { B }$ is the reflection of the structuring element B about its origin and z indicates the location that the origin of the structuring element is translated to. So the dilated pattern $I _ { d l }$ is the set of pixel locations z, where the reflected structuring element overlaps with at least one element in I when translated to z. Accordingly, at these locations of $z ,$ the output image $\mathbf { D } _ { d l }$ is 1, which contains the dilated pattern $I _ { d l }$ . Since the detected pattern of interferences is some oblique thick lines with possible round ends, the disk-shaped or octagonal structuring element can be used.

## C. Interference Mitigation and Signal Recovery

The dilated detection map of interferences can be used as a mask for interference mitigation. With the aid of the dilated detection map, a simplest interference mitigation approach is to zero out the interference-contaminated signal samples in the $t \mathrm { - } f$ spectrum $S _ { t f }$ , denoted as CFAR-Z for conciseness in the following. However, the zeroing operation suppresses not only interferences but also the useful signals, thus causing the power loss of the targets’ signals.

To circumvent the signal power loss of the CFAR-Z method, we suggest utilizing the amplitude correction method [25] to the interference-contaminated samples based on the CFAR detection map. The resultant approach is termed as CFAR-AC. The basic idea of this approach is to replace the amplitudes of the interference-contaminated samples with the average amplitude of the interference-free spectrum samples in the corresponding frequency bin but keep their phases invariant. The new value for a interference-contaminated sample $S _ { t f } [ m _ { i } , n _ { i } ]$ is given by

$$
\tilde { S } _ { t f } [ m _ { i } , n _ { i } ] = A _ { n _ { i } } e ^ { j \arg ( S _ { t f } [ m _ { i } , n _ { i } ] ) }\tag{7}
$$

where $\tilde { S } _ { t f } [ m _ { i } , n _ { i } ]$ is the new sample value at the position $[ m _ { i } , n _ { i } ]$ obtained after interference mitigation, and $\arg ( x )$ takes the phase of a complex number x. $A _ { n _ { i } }$ is the average amplitude of the interference-free samples in the $n _ { i } ^ { \mathrm { { t h } } }$ frequency bin. In this way, the strong power of the interferences is significantly suppressed.

TABLE I  
PARAMETERS FOR NUMERICAL SIMULATIONS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>77GHz</td></tr><tr><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>600 MHz</td></tr><tr><td rowspan=1 colspan=1>Sweep duration of FMCW signal</td><td rowspan=1 colspan=1>100 µs</td></tr><tr><td rowspan=1 colspan=1>Maximum detection range</td><td rowspan=1 colspan=1>250 m</td></tr><tr><td rowspan=1 colspan=1>Sampling frequency</td><td rowspan=1 colspan=1>40 MHz</td></tr><tr><td rowspan=1 colspan=1>Distances of three point targets</td><td rowspan=1 colspan=1>30, 80, and 150 m</td></tr></table>

After that, an inverse STFT (ISTFT) is applied to the interference-mitigated $t \mathrm { - } f$ spectrum to recover the targets’ beat signals in the time domain.

In addition, we should mention that although the phases of the new sample values still surfer from the disturbance of interferences, their effects are negligible after taking further coherent range compression and/or Doppler processing. Moreover, for the array signals contaminated simultaneously by the same interferences, CFAR-AC approach has no impact on the beamforming performance as the phases of signals are kept unchanged.

## IV. NUMERICAL SIMULATIONS

Numerical simulations are presented to demonstrate the interference mitigation performance of the proposed approach. Meanwhile, the results are compared with two the state-ofthe-art efficient approaches, i.e., Wavelet Denoising (WD) approach [16] and the Adaptive Noise Canceller (ANC) approach [17].

## A. Performance Metrics

To facilitate the comparison among different IM approaches and quantitatively evaluate the accuracy of the beat signals recovered by each approach, we use as the metrics the Signal to Interference plus Noise Ratio (SINR) and correlation coefficient $( \rho )$ [22] of the beat signal obtained after IM processing relative to the clean reference signal. The SINR is defined in the same way as the relative signal to noise ratio (RSNR) in [22], which is inversely proportional to the error vector magnitude in [26]. For conciseness, the definition formulas of these metrics are omitted here.

## B. Point Target Simulation

Some typical automotive radar parameters were used for numerical simulations, as listed in Table I. Three point targets were placed in the scene of illumination at the distance of 30 m, 80 m and 150 m, respectively. The amplitudes of the scattered signals from the three targets are set as 1, 0.1, and 0.7 to emulate variations of scattering coefficients of different targets. The victim radar transmitted up-sweep FMCW signals and suffered from some strong FMCW interferences, and complex while Gaussian noise was also added to account for thermal noise and measurement errors of the radar system. The acquired signal at the output of the low-pass filter is shown in Fig. 1(a). Its signal to noise ratio (SNR) and signal to interference plus noise ratio (SINR) are 5 dB and −18.71 dB. Due to the strong interferences, the weak target at the distance of $8 0 \mathrm { m }$ is completely overwhelmed by the increased noise floor of the range profile formed by taking the FFT of the acquired signal (see Fig. 1(k)).

Using the proposed approaches to mitigate the interferences, the acquired time-domain signal is first transformed into the $t \mathrm { - } f$ domain by using the STFT. For discrete implementation, the length of the window of STFT is 256 sampling points and the overlap between adjacent window positions is 252 points. The obtained $t \mathrm { - } f$ spectrogram is shown in Fig. 1(b), where the strong spectrum along the oblique lines are the interferences while the three weak horizontal lines represent the useful beat signals.

Then, utilizing the CA-CFAR detector along each frequency bin, the non-horizontal patterns of interferences are detected (see Fig. 1(c)). As the threshold of CA-CFAR detector is computed based on the average of training cells and varies for each Cell Under Test (CUT), it causes the missed detection of the cells at the edges of the oblique lines of the interferences $( \mathrm { i . e . }$ the detected lines are thinner than that of the interferences), which leads to only partial mitigation of interferences in the following operations. To overcome this problem, the detection map of the CFAR detector was dilated by using the octagonal structuring element, as shown in Fig. 1(d). It is clear that the dilated detection map is much thicker compared to that in Fig. 1(c).

Next, the dilated detection map was employed as a mask to zero out the interference-contaminated samples by the CFAR-Z approach or to correct their amplitudes by using the CFAR-AC method. The resultant $t \mathrm { - } f$ spectra after interference mitigation are shown in Fig. 1(e) and (f). Finally, applying the ISTFT to the obtained $t \mathrm { - } f$ spectra, the corresponding beat signals are recovered, shown in Fig. 1(g) and (h). For comparison, the IM of the signal was also performed using the ANC [17] and the WD methods [16]. For the ANC method, the length of the adaptive filter was set 80. Meanwhile, for the WD approach, the level of the wavelet decomposition was four which was optimally selected and the Stein’s unbiased risk estimate was used to determine the threshold value. The beat signals recovered by the ANC and the WD methods are presented in Fig. 1(i) and (j). From Fig. 1(g), one can see that the CFAR-Z approach suppresses not only the interferences but also the targets’ beat signals at the time instances related to the intersection points of the $t \mathrm { - } f$ spectra of the interferences and useful signals. Similarly, the wavelet denoising method causes even more loss of useful signals, especially in the period between $3 5 \mu \mathrm { s }$ to $8 5 \mu \mathrm { s }$ in Fig. 1(j). By contrast, the CFAR-AC recovers the beat signals of targets with negligible power loss (Fig. 1(h)). From Fig. 1(i), the ANC method only suppresses part of the interferences between $3 5 \mu \mathrm { s }$ and $8 5 \mu \mathrm { s }$ and some chirp-like pulses of the interferences are still observed. This could be caused by the fact that the assumption of the complex conjugate symmetry of the interference spectrum around zeros used by the ANC method is not valid to the synthetic data. To quantitatively compare the accuracy of the recovered beat signals relative to the clean reference, the SINRs of the signals obtained with the ANC, WD, CFAR-Z and CFAR-AC methods are −6.96 dB, 1.27 dB, 4.03 dB and 6.47 dB, respectively. And the corresponding correlation coefficients are $0 . { \dot { 0 } } 7 3 2 e ^ { - { \dot { j } } 0 . 5 0 4 9 }$

![](images/9f0ab01ea9d13235682ac3704e8c6a220c17bc679ea06acf48f8c9e1f3b5b33a.jpg)  
(a)

![](images/77b555e03cfc0eff12780c483fa71e0171209fe4b30b443ace0feec7e5ceb56c.jpg)  
(b)

![](images/af0830568cbcf9219add8ebc92284b1dc036a540684f2108cc31a0ab875448a6.jpg)  
(c)

![](images/03a04d39a50b08fe529f8b373bdcaabb9a08ba463ce721c5eed0d78f9bca25da.jpg)

![](images/f6d2cb6c745085cc4399312d0dd5815a38f966a2da76ed5382f71b043ae251fb.jpg)

![](images/7732566c4458a7206e91baa99d9f4a19f08d62ffa0d77efd23e9b0cbd486773d.jpg)  
(e)  
(f)

(d)  
![](images/402e25334a85d2a496e3809d710f0c06440a3cf4c42a8e8e131c918423676f09.jpg)

![](images/3cd18bc04eb3cde7d8e9966f8592050dc4df78b84099f8e05901fd926e30810d.jpg)  
(g)  
(h)

![](images/5c00c6c1b0aa355ecf5e4567d8d2339d0e7ac86143fe9292e6d61ce91060dc12.jpg)

![](images/742de629061b1d606bf3f84ef22c4ae861e132225ba917d6573bd99adc7f7a4e.jpg)  
(j)

(i)  
![](images/542143bf031045c833a6f89ba9a931756cb31c381b5fc830d6af95a9c27e3e79.jpg)  
(k)

![](images/fad132786087fa2ff44251a0c60e5c935f4145d097349cef226855296ad2c3aa.jpg)  
(l)  
Fig. 1. Illustration of the CFAR-based interference mitigation and comparisons with the ANC and WD methods. (a) and (b) show the real part of the raw signal and its t-f spectrum after the STFT. (c) displays the map of the detected interferences and (d) is its dilated version. (e) and (f) are the t-f spectrum after interference mitigation with CFAR-Z and CFAR-AC approaches. (g) and (h) are the recovered beat signals after taking ISTFT of the spectra in (e) and (f). (i) and (j) show the recovered beat signal after interference mitigation by the ANC and WD methods. (k) and (l) present the range profiles of targets constructed by using the acquired raw signal and the recovered signals after IM, respectively.

$$
0 . 5 5 2 7 e ^ { j 0 . 0 1 6 7 } , 0 . 7 8 3 7 e ^ { - j 0 . 0 0 0 7 } , \mathrm { a n d } \ 0 . 8 9 6 5 e ^ { 0 . 0 2 9 7 } .
$$

Taking the FFT of the recovered beat signals, the targets range profiles in Fig. 1(l) are obtained. All the approaches except the ANC method significantly suppress the interferences and reduce the noise floor of the focused range profile compared to that in Fig. 1(k). The weak target at the distance of 80 m is clearly visible. However, compared to that of the WD method, the range profiles obtained with the CFAR-Z and CFAR-AC have lower noise floor and thus achieve better interference mitigation performance. Moreover, in contrast to CFAR-AC approach, both the WD method and CFAR-Z approach suppress some targets’ signals after mitigating the interferences, which not only decreases the signal power but also causes increased sidelobes in the focused range profile (see the inset in Fig. 1(l)). But as mentioned above, the range profile obtained with the CFAR-Z approach still has smaller power loss and lower sidelobes than that acquired with the WD method. Therefore, in terms of noise floor, power loss and sidelobe levels of the resultant range profile, the CFAR-AC achieves the best interference mitigation performance among the three approaches.

![](images/63ae148c967b836c90d7c96f147a71f0faab54c644d3eba67bbca7b2bf47ba26.jpg)  
(a)

![](images/d30a5897c580c08a8b41ad7d62c4ee0996c9ca48e3d7a95c4a3470a652f20a0e.jpg)  
(b)

![](images/598dcacbd9e8114414151400cad0164dd1e56a3db1a3571beecdab4205e55c15.jpg)  
(c)  
Fig. 2. Quantitative comparison of the interference mitigation performance of the ANC, WD, CFAR-Z and CFAR-AC methods at the different SNRs of the input signals. (a), (b) and (c) show the variations of SINRs, the magnitudes and phase angles of correlation coefficients of the recovered beat signals after interference mitigation, respectively.

## C. Effect of SNR on Interference Mitigation

The noise included in the acquired signal impacts the detection of interferences, thus affecting the interference mitigation. In this section, we used the same targets’ signals and the interferences as in section IV-B but changed the added noise levels to investigate the effect of SNR on the IM performance of the two proposed approaches and their competing counterparts, i.e., WD and ANC methods.

The noise levels with the SNR ranging from −25 dB to 10 dB were considered. At each noise level, 500 times Monte Carlo runs were implemented and the statistics of the performance metrics achieved by the four IM methods are presented as the box plot in Fig. 2. The bottom and top of each box indicate the $\mathrm { \bar { 2 5 } ^ { t h } }$ and $7 5 ^ { \mathrm { { t h } } }$ percentiles of the sample, respectively. Meanwhile, the lines extending above and below of each box show the range between the maximum and minimum values of the sample. From Fig. 2(a), one can see that the SINR of the recovered signals after IM increases with the increase of the SNR of input signal. Generally, the proposed CFAR-Z and CFAR-AC achieve better SINR than the WD and ANC approaches except at SNR = −25 dB in which case the interferences are almost overwhelmed by the noise. A large portion of the interferences were not detected by the CFAR-Z and CFAR-AC approaches; as a results, the interferences are not fully suppressed. Meanwhile, the WD method also fail to extra the interferences and leads to degraded SINR after IM. By contrast, the ANC method eliminates half of the frequency spectrum that does not contain targets’ signals and uses the complex conjugate symmetry of the interference spectra to suppress them; thus, it results in better SINR after IM. In addition, compared to CFAR-AC, the CFAR-Z obtains slightly higher SINRs when $\mathrm { S N R } \ < \ 0 \mathrm { d B }$ but lower ones when $\mathrm { S N R } > 0 \mathrm { d B }$ . This is because that when $\mathbf { S N R } < 0 \mathrm { d B }$ the values of targets’ signals at the interference-contaminated region are more closer to zero than to the amplitude-corrected values in which noise is the dominant component. Therefore, in terms of the SINR obtained after IM, the CFAR-Z approach is a better option than the CFAR-AC when the SNR of the input signal is lower than 0 dB.

Moreover, Fig. 2(b) shows that the magnitudes of correlation coefficients of the signals obtained with the CFAR-AC are constantly larger than that acquired by the other three methods. Moreover, with the rise of the SNRs of input signals, the phase angles of the correlation coefficients of the recovered signals by the WD, CFAR-Z and CFAR-AC are all increasingly concentrated around zero. So in terms of both the SINR and correlation coefficient of the recovered signals after IM, the proposed CFAR-Z and CFAR-AC outperform the other two approaches; however, in practice the better choice between them should be determined based on the SNR of the acquired signal.

## D. Computational Time

The computational complexities of the proposed CFAR-Z and CFAR-AC are dominated by the CFAR detection along each frequency bin. In section. IV-B, the synthetic beat signal in one sweep contains 3933 samples and was processed with the ANC, WD, CFAR-Z and CFAR-AC approaches by using MATLAB 2019b on a computer with Intel i5-3470 CPU and 8 GB. The computational time of the four IM approaches are summarized in Table II. One can see that the WD method is the most efficient one compared to the other three approaches. Meanwhile, when the number of overlapped samples of the STFT window decreases from 252 to 248 (i.e., the sliding step of the STFT window increases from 4 to 8), the computational time of both CFAR-Z and CFAR-AC decreases by about 50% as the number of samples in each frequency bin is halved for the CFAR detection. So by properly adjusting the processing parameter, the computational time of the CFAR-Z and CFAR-AC can be significantly reduced. Moreover, as the CFAR detection is carried out independently along each frequency bin in the $t \mathrm { - } f$ domain, these detection operations along different frequency bins can be implemented by using parallel computing, thus further reducing their computational time and improving the real-time processing capability.

TABLE II  
COMPUTATIONAL TIME OF THE ANC, WD, CFAR-Z AND CFAR-ACAPPROACHES FOR INTERFERENCE MITIGATION
<table><tr><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>ANC</td><td rowspan=2 colspan=1>WD</td><td rowspan=1 colspan=2>CFAR-Z</td><td rowspan=1 colspan=2>CFAR-AC</td></tr><tr><td rowspan=1 colspan=1>N9s</td><td rowspan=1 colspan=1>N25</td><td rowspan=1 colspan=1>N9s</td><td rowspan=1 colspan=1>N25</td></tr><tr><td rowspan=1 colspan=1>Time [ms]</td><td rowspan=1 colspan=1>73</td><td rowspan=1 colspan=1>9.64</td><td rowspan=1 colspan=1>214</td><td rowspan=1 colspan=1>109.3</td><td rowspan=1 colspan=1>228.5</td><td rowspan=1 colspan=1>116.4</td></tr></table>

$^ { 1 } N _ { 1 } ^ { \mathrm { o s } } = 2 5 2 ,$ $N _ { 2 } ^ { \mathrm { o s } } = 2 4 8$ are the number of overlapped samples of the sliding window at two adjacent positions for the STFT.

![](images/8fc6471792d432faa6e07323b13dfc1118e0cf190b77d3a3918dd4e6325cdb94.jpg)  
(a)

![](images/0400682d08a8a6b779893c5e7aa6c8f30219b071ec9a82792001589931252fd3.jpg)  
(b)  
Fig. 3. Experimental setup for interference mitigation with two TI automotive radar boards. (a) shows geometrical configuration and (b) the experimental setup.

## V. EXPERIMENTAL RESULTS

In this section, the experimental results are presented to demonstrate the performance of the proposed approach.

One Texas Instruments (TI) AWR1642BOOST radar board is used as the victim radar while another TI AWR1443BOOST radar board is utilized as the aggressor radar. Two Trihedral Corner Reflectors (TCRs) are used as targets. The geometrical configuration and picture of experimental setup are shown in Fig. 3(a) and (b). The system parameters used for the victim and aggressor radars are listed in Table III. The AWR1642 radar board is connected with a TI DCA1000EVM data capture card to collect raw ADC data which is then sent to a host laptop for data storage.

TABLE III  
PARAMETERS OF EXPERIMENTAL RADAR SYSTEMS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Victim radar</td><td rowspan=1 colspan=1>Aggressor radar</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>77.69</td><td rowspan=1 colspan=1>77.69</td><td rowspan=1 colspan=1>GHz</td></tr><tr><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>1380.18</td><td rowspan=1 colspan=1>1380</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>K</td><td rowspan=1 colspan=1>15.015</td><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1> $\mathrm { \overline { { { M H z } / \mu s } } }$ </td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>91.92</td><td rowspan=1 colspan=1>39.4337</td><td rowspan=1 colspan=1>µs</td></tr><tr><td rowspan=1 colspan=1>Sampling frequency</td><td rowspan=1 colspan=1>6.25</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>No. of Samples</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>一</td></tr></table>

Fig. 4(a) shows the acquired signal in one of the FMCW sweeps. Two large pulses are observed at the the beginning and end of the acquired data, which are caused by the strong interferences from the aggressor radar. After range compression, the interference-contaminated signal leads to a range profile with significantly increased noise floor (see Fig. 4(b)). For comparison, the range profile of targets obtained with a clean reference signal is also presented, where the first three peaks indicate the locations of the aggressor radar and two TCRs at the distance of 2.33 m, 6.95 m and 9.75 m, respectively. One can observe that in the range profile obtained with the interference-contaminated signal the two TCRs are almost overwhelmed by the increased noise floor. This made the TCR at the further distance not detectable when a CA-CFAR detector was employed for target detection (see Fig. 5(a)). The CA-CFAR detector was set with one guard cell and 10 training cells on each side of the CUT and the probability of false alarm of $1 \times 1 0 ^ { - 4 }$

To overcome the missed detection of the target caused by the strong interferences, the proposed approaches are applied to the acquired signal for interference mitigation. Firstly, the $t \mathrm { - } f$ spectrum of the acquired signal is computed through the STFT implemented by using a sliding Hamming window of length 128 with sliding step of one for signal segmentation and then taking the FFT of each signal segments. The obtained spectrum is shown in Fig. 4(c). One can see that the interferences exhibit as the two thick vertical lines in the $t \mathrm { - } f$ domain. Then, a 1-D CFAR detector is applied along each frequency bin to detect the interference-contaminated signal spectrum, and the detection map is presented in Fig. 4(d). Compared to Fig. 4(c), one can see that in Fig. 4(d) some interference-contaminated spectral samples are not detected, especially the ones at the edges of the two thick spectral lines. To tackle the missed detection of the interferences, the detection map is dilated with an octagonal structuring element and the result is displayed in Fig. 4(e). Note that three small patches appear between 40 µs and $8 0 \mu \mathrm { s } ,$ which reveals that some isolated spectral samples are falsely detected as the interference in Fig. 4(d). Next, using the dilated detection map as a mask, the zeroing and amplitude correction can be conducted to substantially mitigate the inferences, and the results of CFAR-Z and CFAR-AC approaches are given in Fig. 4(f) and (g). Finally, the $t \mathrm { - } f$ spectrum obtained after IM is inverted through the ISTFT to

![](images/90a8f9bbce2cb883b5b174ab117388f70b58c8aa856c7238fa50155372202713.jpg)  
(a)

![](images/52b0de9e4ab08f853a998a2fa09ed368304d0aea76ad6b0a827514f98abcd54d.jpg)  
(b)

![](images/fba14f0a15f121e5f98b5e9630db369233c66aca1b26dcd59174498fe2ba9a20.jpg)  
(c)

![](images/9ded1f51b1b496459e9d9dde884d7e86b3fe91519ae03abcc0f3f4401e9aa69d.jpg)  
(d)

![](images/ac0dac79f36d54c36281fe3fedcd24eb3165c3858632144811339d274d9250f6.jpg)  
(e)

![](images/b27eba811eb88770411babe774ad82c90b45fe63c5e489cbb34376e4581f2bd7.jpg)  
(f)

![](images/ace2e9475638e5624b61f698eaa1b40d4e86c4a036cb17844bc02d7ced6ffc16.jpg)  
(g)

![](images/d7e4965bf8add99d920f1c3eea3ec1ce993325382601cabb3f1dd336d2e2cebd.jpg)  
(h)

![](images/b6805b121ad4d9d7b8839205d5a4741316b706eb866afb1deb8ccc6d053578fa.jpg)  
(i)  
Fig. 4. Interference mitigation for the experimental radar measured with TI automotive radar. (a) shows the acquired beat signal contaminated by the interferences and (c) its time-frequency spectrum. (b) presents the range profiles of targets related to the beat signal in (a) and an interference-free reference. (d) shows the CFAR detection map of the interferences and (e) its dilation that will be used for interference mitigation. (f) and (g) give the results of interference mitigation with CFAR-Z and CFAR-AC approaches, respectively. (h) displays the range profiles obtained after interference mitigation and (i) shows the zoomed-in view of the range profiles at the distance of 5.5 m to 11 m.

## reconstruct the time-domain beat signal.

To demonstrate the IM performance of the proposed approaches, the targets’ range profiles resulting from their recovered beat signals are presented in Fig. 4(h). For comparison, the range profiles obtained with the reference signal and the beat signals recovered by the two IM methods, i.e. WD and ANC, are also presented, which are normalized by the maximum value of all the range profiles. From Fig. 4(h), the overall range profiles obtained with the WD, CFAR-Z and CFAR-AC have very good agreement with the reference one except that the one acquired by the ANC method has higher sidelobes. However, based on the zoomed-in view of the range profiles around the two TRCs (Fig. 4(i)), one can see that among the four IM methods, the CFAR-AC and ANC methods get the maximum peak values at the distances of two TCRs, whose values are also closest to the reference ones. However, the WD method results in lower peak amplitudes than the reference one and the other three methods as the wavelet-based denoising method not only eliminates the strong interferences but also suppresses part of the useful signal power. Meanwhile, as expected, the CFAR-Z leads to smaller peak values of the range profile at the positions of two TCRs compared to the CFAR-AC. So in terms of power conservation of useful signals, the CFAR-AC and ANC methods achieve the best performance in this case. However, the ANC method assumes strict complex conjugate symmetry of the interference spectrum in the positive and negative frequency bands. Otherwise, its performance degrades significantly as shown in the simulation. In addition, we want to mention that to avoid the weighting effect of the sliding window of the STFT on the reconstructed signal samples in the beginning and the end, 128 zeros were padded at both sides of the acquired signal before computing the STFT and then the extra zeros were removed after inverting the $t \mathrm { - } f$ spectrum through the ISTFT. Due to this operation before the STFT, it leads to the visually “increased” time duration of the $t \mathrm { - } f$ domain plots (i.e., Fig. 4(c)-(g)) compared to that of the acquired signal (Fig. 4(a)).

![](images/2da4f8d8b3a315c7b5077ddac3df80f9085e2d8ae9d7c1068785adc04bac9a0b.jpg)  
(a)

![](images/9cf2e8daa7669f930f1e3ed5dbd9d096e574511538fb565d2e389293fd4ddafc.jpg)  
(b)

![](images/7e095ebd558962c88987d040b62782fcc930d57732d299e42e8cc49c762cefa7.jpg)  
(c)

![](images/cccdce889c0c565953c00c8fc457c0244639f5bc539fd37013566b9002a84573.jpg)  
(d)

![](images/f951e6bac01102869169db8862de06570d5f9d869b26d16be1fa0f06c2809cae.jpg)  
(e)  
Fig. 5. The output results of the CFAR detection of the input range profiles before and after interference mitigation. (a) shows the detected results of the range profiles obtained with interference-contaminated signal. (b), (c), (d) and (e) are the corresponding detection results after taking interference mitigation with WD, ANC, CFAR-Z and CFAR-AC approaches, respectively.

To further evaluate the quality of the beat signals recovered by the four IM approaches, the target detection performance of the constructed range profiles are tested by employing the same CFAR detector used for target detection in Fig. 5(a). Fig. 5(b)-(e) show the output results of the CFAR detector. One can see that the three peaks related to the aggressor radar and two TCRs are all detected after IM with all the four methods while the TCR at the further distance was missed based on the range profile before IM (Fig. 5(a)). So the four IM methods improve the targets’ probability of detection. Moreover, based on the range profiles obtained with the CFAR-Z and CFAR-AC, a fourth target, which is a stationary car at a distance of 22.5 m, is also detected (Fig. 5(d) and (e)) but missed when the RPs acquired with the WD and ANC methods were used (Fig. 5(b) and (c)). Therefore, the beat signals obtained with the CFAR-Z and CFAR-AC IM approaches provide higher target’s probability of detection than those recovered with the WD and ANC methods.

## VI. CONCLUSION

In the paper, we proposed two CFAR-based approaches, i.e., CFAR-Z and CFAR-AC, to mitigate inference for FMCW radars system, which exploit the CFAR detector to detect the large chirp-pulse like interferences in the time-frequency domain and then apply the zeroing and amplitude correction for mitigate them, respectively. Compared to the prior art methods, both approaches achieve better interference mitigation performance in terms of both SINR and correlation coefficient of the recovered signal after IM. Moreover, both CFAR-Z and CFAR-AC approaches are computationally efficient and could be implemented for real-time processing for automotive radars.

## ACKNOWLEDGMENT

The authors would like to thank Ms Y. Lu and Mr I. R. Montero for their help during the experimental measurement.

## REFERENCES

[1] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “Radarmac: Mitigating radar interference in self-driving cars,” in 2016 13th Annual IEEE International Conference on Sensing, Communication, and Networking (SECON), Conference Proceedings, pp. 1–9.

[2] S. Ishikawa, M. Kurosawa, M. Umehira, X. Wang, S. Takeda, and H. Kuroda, “Packet-based FMCW radar using CSMA technique to avoid narrowband interefrence,” in 2019 International Radar Conference (RADAR), Conference Proceedings, pp. 1–5.

[3] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “Radchat: Spectrum sharing for automotive radar interference mitigation,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–14, 2019.

[4] T. Luo, C. E. Wu, and Y. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Transactions on Circuits and Systems I: Regular Papers, vol. 60, no. 12, pp. 3247–3255, 2013.

[5] X. Hu, Y. Li, M. Lu, Y. Wang, and X. Yang, “A multi-carrier-frequency random-transmission chirp sequence for TDM MIMO automotive radar,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3672– 3685, 2019.

[6] Y. Kitsukawa, M. Mitsumoto, H. Mizutani, N. Fukui, and C. Miyazaki, “An interference suppression method by transmission chirp waveform with random repetition interval in fast-chirp fmcw radar,” in 2019 16th European Radar Conference (EuRAD), Conference Proceedings, pp. 165–168.

[7] E. Gambi, F. Chiaraluce, and S. Spinsante, “Chaos-based radars for automotive applications: Theoretical issues and numerical simulation,” IEEE Transactions on Vehicular Technology, vol. 57, no. 6, pp. 3858– 3863, 2008.

[8] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geoscience and Remote Sensing Letters, vol. 15, no. 1, pp. 137–141, 2018.

[9] F. Uysal, “Phase-coded fmcw automotive radar: System design and interference mitigation,” IEEE Transactions on Vehicular Technology, vol. 69, no. 1, pp. 270–281, 2020.

[10] E. H. Kim and K. H. Kim, “Random phase code for automotive MIMO radars using combined frequency shift keying-linear FMCW waveform,” IET Radar, Sonar & Navigation, vol. 12, no. 10, pp. 1090–1095, 2018.

[11] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Transactions on Microwave Theory and Techniques, vol. 65, no. 5, pp. 1727–1734, 2017.

[12] I. Artyukhin, V. Ermolaev, A. Flaksman, A. Rubtsov, and O. Shmonin, “Development of effective anti-interference primary signal processing for mmwave automotive radar,” in 2019 International Conference on Engineering and Telecommunication (EnT), Conference Proceedings, pp. 1–5.

[13] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in 2018 IEEE Radar Conference (RadarConf18), Conference Proceedings, pp. 0252–0256.

[14] T. Nozawa, Y. Makino, N. Takaya, M. Umehira, S. Takeda, X. Wang, and H. Kuroda, “An anti-collision automotive fmcw radar using time-domain interference detection and suppression,” in International Conference on Radar Systems (Radar 2017), Conference Proceedings, pp. 1–5.

[15] J. Wu, S. Yang, W. Lu, and Z. Liu, “Iterative modified threshold method based on emd for interference suppression in fmcw radars,” IET Radar, Sonar & Navigation, vol. 14, no. 8, pp. 1219–1228, 2020.

[16] S. Lee, J. Lee, and S. Kim, “Mutual interference suppression using wavelet denoising in automotive fmcw radar systems,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–11, 2019.

[17] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[18] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for fmcw radar using beat-frequencies interpolation in the stft domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, 2019.

[19] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using rnn with self attention,” in ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, Conference Proceedings, pp. 3802–3806.

[20] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world fmcw radar signals,” in 2020 IEEE International Radar Conference (RADAR), Conference Proceedings, pp. 624–629.

[21] P. D. Mark A. Richards, Fundamentals of Radar Signal Processing, Second Edition, 2nd ed. New York: McGraw-Hill Education, 2014.

[22] J. Wang, M. Ding, and A. Yarovoy, “Model-based interference mitigation for FMCW radar systems,” IEEE Transactions on Microwave Theory and Techniques, submitted.

[23] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8110–8117, 2018.

[24] R. C. Gonzalez, R. E. Woods, and S. L. Eddins, Digital Image Processing Using MATLAB. USA: Gatesmark Publishing, 2009.

[25] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive fmcw radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS), 2018, Conference Proceedings, pp. 1–4.

[26] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in 2019 IEEE Radar Conference (RadarConf), 2019, pp. 1–6.