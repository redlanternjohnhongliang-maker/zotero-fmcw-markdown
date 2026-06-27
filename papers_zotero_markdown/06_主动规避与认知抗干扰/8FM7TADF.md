Article

# Automotive Frequency Modulated Continuous Wave Radar Interference Reduction Using Per-Vehicle Chirp Sequences

Youn-Sik Son, Hyuk-Kee Sung and Seo Weon Heo \* <sup>ID</sup>

Electronics and Electrical Engineering, Hongik University, 72-1 Sangsu-Dong, Mapo-Gu, Seoul 04066, Korea; yoonsic2005@naver.com (Y.-S.S.); hksung@hongik.ac.kr (H.-K.S.)

Correspondence: seoweon.heo@hongik.ac.kr; Tel.: +82-2-320-3081

Received: 12 July 2018; Accepted: 24 August 2018; Published: 27 August 2018

![](images/41b02e922eda94058c5d6485e16e7b5dd075636dabc832f7543db10fac6bca6d.jpg)

Abstract: Recently, many automobiles adopt radar sensors to support advanced driver assistance system (ADAS) functions. As the number of vehicles with radar systems increases the probability of radar signal interference and the accompanying ghost target problems become serious. In this paper, we propose a novel algorithm where we deploy per-vehicle chirp sequence in a frequency modulated continuous wave (FMCW) radar to mitigate the vehicle-to-vehicle radar interference. We devise a chirp sequence set so that the slope of each vehicle’s chirp sequence does not overlap within the set. By assigning one of the chirp sequences to each vehicle, we mitigate the interference from the radar signals transmitted by the neighboring vehicles. We confirm the performance of the proposed method stochastically by computer simulation. The simulation results show that the detection and false alarm performance is improved significantly by the proposed method.

Keywords: FMCW radar; automotive radar; radar mutual interference; multi-target situation

## 1. Introduction

However, as the number of vehicles equipped with radar and the number of radars mounted per vehicle increases, so does the radar-to-radar interference, since the radars are concurrently operating in the same frequency band [2–4]. The most intuitive way to avoid this problem is to use a different frequency band, which is difficult to apply considering the wide bandwidth of the radar signal. Another method is to detect and remove the signal interference from other vehicles [5]. To determine the interference signals, the transmitter switches off the transmission signal. The problem is that it wastes the transmission opportunity during the interference measurement period and that it measures a delayed interference.

does not work properly if either the power of the interference signal is strong compared with the desired signal or the frequency slope difference between the desired and interferer is small. There is a way to reduce the mutual interference of automotive radar through adaptive beamforming [7]. The problem of the method proposed in [7] is that the computational complexity is significant because the adaptive weight should be obtained using the steepest-descent method. Furthermore, it needs a certain convergence time so it cannot cope well with the rapidly time-varying interferences. Due to these problems it is not easy to apply this method to autonomous vehicles. The method proposed in [8] uses morphological component analysis (MCA) to separate the interference from the received signal. The problem of this method is that the interference cannot be separated when the slope of the transmitted chirp signal and the slope of the chirp signal of interference are the same. The authors in [9] proposed a method where they apply a filter to differentiate the transmitted radar signal from the interference signals of other radars. They process the received signal iteratively until the desired signal is extracted. Their method is computationally complex and takes long time, which is not recommendable to the autonomous vehicle where the real time response is critical. There is also a method to reduce the radar-to-radar interference using the characteristics of multiple-input multiple-output (MIMO) radar [10]. It cannot be applied to the automobile radar since most of them use multi-antenna for beamforming purposes rather than MIMO purposes.

We have extensively reviewed the previous works on radar interference mitigation methods and have found that most of the methods mentioned did not consider the multi-target situation which occurs frequently in real traffic environments. Also, the fact that the power of the interference signal can vary widely is overlooked. In this paper, we propose a novel method to reduce the radar-to-radar interference in multi-target situation which works well even when the interfering signal power is high. The proposed method is based on the idea of per-vehicle transmission waveform sequence of the FMCW to reduce the radar-to-radar interference.

## 2. System Description

## 2.1. Frequency Modulated Continuous Wave Radar System

In Figure 1 the frequency modulated continuous wave (FMCW) radar system block diagram is shown. The transmitter generates the FMCW waveform and the same waveform is used for the demodulation of the signal from the receiver antenna. After sampling the down-converted quadrature received signal we apply a fast Fourier transform (FFT) and process the signal in the frequency domain to remove the interference and detect the target [11–13].

![](images/e61bbd4abc1c1e589884cee4df23388cf3a8d7c3782d3f0eb1fb62db036ad434.jpg)  
Figure 1. Block diagram of frequency modulated continuous wave (FMCW) radar system. FFT: fast Fourier transform; CFAR: constant false alarm rate.

The transmitted signal is a FMCW signal whose frequency increases linearly as given by:

$$
s _ { T } ( t ) = \mathrm { R e } \Big \{ e ^ { j 2 \pi ( f _ { c } + a / 2 \cdot t ) t } \Big \} = \cos \Big ( 2 \pi ( f _ { c } + \frac { a } { 2 } \cdot t ) t \Big ) ,\tag{1}
$$

where $f _ { c }$ is the center frequency and a is the slope of the frequency domain ramp signal [4]. The received signal from several targets can be described by:

$$
s _ { R } ( t ) = \sum _ { m = 1 } ^ { N } A _ { m } s ( t - \tau _ { m } ) + w ( t ) ,\tag{2}
$$

where N is number of the targets, $A _ { m } , \tau _ { m }$ are the attenuation and time delay from the $m ^ { t h }$ target, respectively, and $w ( t )$ is the AWGN signal. After down-conversion we get the beat frequency signal given by:

$$
s _ { b } ( t ) = \sum _ { n = 1 } ^ { N } A _ { m } e ^ { j 2 \pi ( f _ { b m } \cdot t + \phi _ { m } ) } + n ( t ) ,\tag{3}
$$

where $f _ { b _ { m } } , \phi _ { m }$ are the beat frequency and phase between the transmitted and received signal from the target, respectively, and $n ( t )$ is the additive white Gaussian noise (AWGN) signal. The maximum beat frequency is determined by the maximum distance from the target $R _ { m a x }$ such that $\begin{array} { r } { f _ { b _ { m a x } } = \frac { 2 R _ { m a x } } { c } \cdot \frac { B } { T } } \end{array}$ where B is the signal bandwidth, T is the sweep time. Sampling frequency $F _ { S }$ should be larger than twice the maximum beat frequency to avoid the aliasing, i.e.:

$$
F _ { S } > 2 \cdot f _ { b _ { \mathrm { m a x } } } \ = 2 \cdot \frac { 2 R _ { \mathrm { m a x } } } { c } \cdot \frac { B } { T } .\tag{4}
$$

After the FFT operation, we apply the constant false alarm rate (CFAR) detection algorithm to determine the existence of the valid beat frequency. To decide the proper threshold value, several CFAR algorithms such as the CA-CFAR and OS-CFAR were proposed [14].

## 2.2. Multi-Target Problem

The basic waveform that the FMCW radar transmits and receives is the triangle waveform and it is shown in Figure 2.

![](images/8a1afff67e00bb7a38f93cc2d08d3a2861b586cc9d44c5f38dea98ac3c118bb1.jpg)  
Figure 2. Basic waveform of FMCW radar.

The waveform consists of an up-ramp and a down-ramp, and the beat frequencies available in each ramp are denoted by $f _ { b u }$ and $f _ { b d }$ . The time delay between the transmitted and the received signal is denoted by $t _ { d } ,$ and $f _ { d }$ is the Doppler frequency caused by the relative velocity of the target.

The bandwidth of the waveform, the period of one ramp and the carrier frequency are represented by $B , T$ and $f _ { c } ,$ respectively. The beat frequency of each ramp $( f _ { b u } , f _ { b d } )$ can be expressed by the distance (R) and the relative velocity (v) of the target as shown by:

$$
\left\{ \begin{array} { c } { f _ { b u } = f _ { r } - f _ { d } = t _ { d } \frac { B } { T } + 2 \frac { v } { c } f _ { c } = \frac { 2 R } { c } \frac { B } { T } + 2 \frac { v } { c } f _ { c } } \\ { f _ { b d } = f _ { r } + f _ { d } = t _ { d } \frac { B } { T } - 2 \frac { v } { c } f _ { c } = \frac { 2 R } { c } \frac { B } { T } - 2 \frac { v } { c } f _ { c } } \end{array} \right. .\tag{5}
$$

If where exists only a single target, we can get exact range and relative velocity of the target using Equation (5) without any problem. However, where multiple targets exist, there is a problem in obtaining the range and the relative velocity of the target through the beat frequencies.

$( f _ { b u } , f _ { b d } )$

$$
\left\{ \begin{array} { l l } { R = - f _ { c } \frac { T } { B _ { 1 } } v + f _ { b u } \frac { c T } { 2 B _ { 1 } } } \\ { R = + f _ { c } \frac { T } { B _ { 2 } } v + f _ { b d } \frac { c T } { 2 B _ { 2 } } } \end{array} \right. .\tag{6}
$$

According to the Equation (6), we get several targets from each of the combinations of the up and down beat frequency. Some combinations give a true and others give a ghost target. In Figure 3, we have shown the case where there exist two true targets. Since each target generates its own up and down beat frequency, there exists four intersection points from A to D. Among them A and C corresponds to the true target, however, the other two corresponds to the ghost target, i.e., B and D. In this case, there’s only two ghost targets. However, as the number of targets increases, otherwise as the number of $f _ { b u }$ and $f _ { b d }$ increases, the possible combination of the up and down beat frequency increases, the ghost-target problem becomes very difficult to solve.

![](images/24ad70372af5f153a81e613fdb700c90aea7c2687fe190b3be47c210cd4269eb.jpg)  
Figure 3. Example of multi-target problem in R-v plane.

To differentiate the true target from the ghost one, sometimes the system adds additional chirp signals with different slope $( \pm f _ { c } T / B )$ to the existing waveform [15–17]. This adds additional line with different slope in R-v plane as shown in Figure 4. By detecting the intersection points of the 3 lines, we can differentiate the true targets (A and C) from the ghost ones (B and D). One thing to mention is that though we explained the algorithm assuming the triangular waveform here, we can use a ramp waveform with different frequency slopes which will be shown in the following section.

![](images/c8fd2d6031c52e1e1e57a1ea9ac8c1a3f209e45cb6d286ec33f847b18b07be7e.jpg)  
Figure 4. Detection of true target by adding a waveform with different slope.

## 3. Proposed Method

$( \pm B / T )$

In the proposed method, a single period of chirp sequence is composed of four short chirp sequences with different frequency slopes. Figure 5 shows an example of two possible chirp sequences. To minimize the interference between the radars of adjacent vehicles, which might not be time synchronized, we impose two constraints in choosing the slope sequences. First, we do not allow any two slope indices match in the same time interval. For example, if $( a _ { 1 } , \ a _ { 2 } , \ a _ { 3 } , \ a _ { 4 } )$ is a possible slope sequence then $( a _ { 1 } , ~ a _ { 3 } , ~ a _ { 4 } , ~ a _ { 2 } )$ is not allowed since $a _ { 1 }$ occupies the same slot. Second, we do not allow any cyclic permutation of a given slope sequence. For example, if $( a _ { 1 } , \ a _ { 2 } , \ a _ { 3 } , \ a _ { 4 } )$ is a possible slope sequence then $( a _ { 2 } , \ a _ { 3 } , \ a _ { 4 } , \ a _ { 1 } )$ is not allowed since the delayed waveform of the transmitted sequence $( a _ { 1 } , \ a _ { 2 } , \ a _ { 3 } , \ a _ { 4 } )$ coincides with the second one. The two sequences in Figure 5 do not violate these constraints.

![](images/001c7a8f4d9629bc8261ccd21c43086536e064412dd37b217adfab218beaa22b.jpg)  
Figure 5. Example of the waveform of the generated waveform set.

The transmitted signal between the time interval of 0\~NT can be described by:

$$
s _ { T } ^ { i } ( t ) = \mathrm { R e } \left\{ \sum _ { k = 0 } ^ { N - 1 } e ^ { j 2 \pi ( f _ { c } + a _ { k } ^ { i } / 2 \cdot ( t - k T ) ) \cdot ( t - k T ) } \cdot r e c t \biggl ( \frac { t - ( k + 1 / 2 ) T } { T } \biggr ) \right\} ,\tag{7}
$$

where $s _ { T } ^ { i } ( t )$ denotes the transmitted signal of the vehicle using i-th slope sequence, $a _ { k } ^ { i }$ is a k-th slope of chirp signal, N is the number of the slope sequence in a single chirping interval (four in Figure 5) and T is the time duration of a short chirp sequence. The received signal can be described by:

$$
s _ { R } ( t ) = \sum _ { n = 1 } ^ { L _ { i } } A _ { n } s _ { T } ^ { i } ( t - \tau _ { n } ) + \sum _ { m = 1 } ^ { M } \sum _ { l _ { m } = 1 } ^ { L _ { m } } B _ { m } ^ { l } s _ { T } ^ { i _ { m } } ( t - \tau _ { l _ { m } } ) + w ( t ) ,\tag{8}
$$

where $A _ { n } , B _ { m } ^ { l }$ are attenuation coefficients, $\tau _ { n }$ is the time delay, M is the number of interfering signals, $i _ { m }$ is the slope sequence index, $L _ { i }$ and $L _ { m }$ are the number of the targets and interferences, and w(t) is the AWGN signal. That is, the first part is from the true targets and the second part is from the interferences.

Then, the signal processing process shown in Figure 1 is performed using Equations (7) and (8) resulting in the following output signal after mixing $s _ { R } ( t )$ and $s _ { T } ( t )$ , as is given by:

$$
\begin{array} { r l } & { L P F \big \{ s _ { T } ^ { i } ( t ) \cdot s _ { R } ( t ) \big \} = s _ { b } ( t ) + i _ { b } ( t ) + n ( t ) } \\ & { = \operatorname { R e } \big \{ \displaystyle \sum _ { n = 1 } ^ { L _ { i } } \bigg ( \displaystyle \sum _ { k = 0 } ^ { N - 1 } A _ { n } e ^ { j 2 \pi ( a _ { k } ^ { i } \cdot \tau _ { n } - f _ { a _ { n } } ) \cdot ( t - k T - \tau _ { n } ) } \cdot r e c t \bigg ( \frac { t - ( ( k + 1 / 2 ) T + \tau _ { n } / 2 ) } { T - \tau _ { n } } \bigg ) \bigg ) + } \\ & { \displaystyle \sum _ { m = 1 } ^ { M } \sum _ { l = 0 } ^ { L _ { m } } \bigg ( \displaystyle \sum _ { k = 0 } ^ { N - 1 } B _ { m } ^ { l } e ^ { j 2 \pi ( ( ( \frac { a _ { k } ^ { i } - a _ { k } ^ { i m } } { 2 } ) \cdot ( t - k T ) + a _ { k } ^ { i m } \cdot \tau _ { m } - f _ { a _ { m } } ) \cdot ( t - k T - \tau _ { m } ) ) } \cdot r e c t \bigg ( \frac { t - ( ( k + 1 / 2 ) T + \tau _ { m } / 2 ) } { T - \tau _ { l _ { m } } } \bigg ) \bigg ) \} + n ( t ) , } \end{array}\tag{9}
$$

where $s _ { b } ( t ) , i _ { b } ( t )$ are the signal and interference beat signal, respectively, and $n ( t )$ is the AWGN signal. 5

To obtain the beat frequencies of the targets, we apply the CFAR algorithm to each of the N short chirp sequences. The number of detected beat frequencies can be different in each sequence. Let $N _ { k }$ denote the number of beat frequencies extracted in the k-th short sequence where k can be 1 to N. The process of detecting true targets using the beat frequencies extracted from CFAR is composed of the following three steps. First, to generate candidates for the true targets, we draw straight lines on the R-v plane using beat frequencies of two periods with the largest $N _ { k }$ value. The reason for using the beat frequency of the period with the largest $N _ { k }$ value is to increase the detection probability. This can also increase the false alarm rate, but this problem can be amended by the second step. If the k values at this time are expressed as $k _ { 1 }$ and $k _ { 2 }$ , the straight lines on the R-v plane expressed using Equation (6) are expressed by:

$$
\left\{ \begin{array} { l l } { R _ { i j } = - f _ { c } \frac { T } { B _ { k _ { 1 } } } v _ { i j } + f _ { i } ^ { k _ { 1 } } \frac { c T } { 2 B _ { k _ { 1 } } } } \\ { R _ { i j } = - f _ { c } \frac { T } { B _ { k _ { 2 } } } v _ { i j } + f _ { j } ^ { k _ { 2 } } \frac { c T } { 2 B _ { k _ { 2 } } } } \end{array} \right. ,\tag{10}
$$

where $f _ { i } ^ { k } , B _ { k }$ refers to the i-th beat frequency and bandwidth of the k-th short sequence, respectively. So, the R and v profiles of the true target candidates using Equation (10) are expressed by:

$$
R _ { i j } = { \frac { c T } { 2 } } \cdot { \frac { f _ { i } ^ { k _ { 1 } } - f _ { j } ^ { k _ { 2 } } } { B _ { k _ { 1 } } - B _ { k _ { 2 } } } } , v _ { i j } = { \frac { c } { 2 f _ { c } } } \cdot { \frac { f _ { j } ^ { k _ { 2 } } B _ { k _ { 1 } } - f _ { i } ^ { k _ { 1 } } B _ { k _ { 2 } } } { B _ { k _ { 1 } } - B _ { k _ { 2 } } } } ,\tag{11}
$$

where $k _ { 1 } , k _ { 2 } \in \left\{ 1 , 2 , \ldots , N \right\}$ and $i \in \left\{ 1 , 2 , \ldots , N _ { k _ { 1 } } \right\} , j \in \left\{ 1 , 2 , \ldots , N _ { k _ { 2 } } \right\}$

$N _ { k _ { 1 } } \times N _ { k _ { 2 } }$

Since a single chirp sequence is composed of multiple short chirp sequences, there could be different number of beat frequencies available (or many different $N _ { k } { } ^ { \prime } { \mathbf { s } } . )$ . For this purpose, in the third step, the value $N _ { k }$ of the period with the smallest INR (interference-to-noise ratio) value is set as the total number of true targets and denote the value as $N _ { T }$ . In this paper, we define $\begin{array} { r } { I N R _ { d B } = 1 0 \log _ { 1 0 } \left( \frac { P _ { I n t e r f e r e n c e } } { P _ { A W G N } } \right) } \end{array}$ where $P _ { I n t e r f e r e n c e }$ and $P _ { A W G N }$ are signal power of the interference and AWGN. So, in the final step, $N _ { T }$ candidates with the smallest average distance among the true target candidates are regarded as true ones.

When the slope sequence of the neighboring vehicles differs, the frequency of the beat signal varies with time as shown by:

$$
f r e q ( i _ { b } ( t ) ~ ) = 2 \pi \frac { d } { d t } \left( \left( \left( \frac { a _ { k } ^ { i } - a _ { k } ^ { i _ { m } } } { 2 } \right) \cdot ( t - k T ) + a _ { k } ^ { i _ { m } } \cdot \tau _ { l _ { m } } - f _ { d _ { m } } \right) \cdot ( t - k T - \tau _ { l _ { m } } ) \right) .\tag{12}
$$

$i _ { m }$ $i _ { b } ( t )$ $\left( a _ { k } ^ { i _ { m } } \cdot \tau _ { l _ { m } } - f _ { d _ { m } } \right)$ $f r e q ( i _ { b } ( t ) )$

$( a _ { 1 } , \ a _ { 2 } , \ a _ { 3 } , \ a _ { 4 } )$ $( a _ { 2 } , \ a _ { 4 } , \ a _ { 1 } , \ a _ { 3 } )$ $T$ $a _ { 2 }$

![](images/6253669f4f2010c7434ccddb47086f36c38510d6921f337766ab17dd8e792c8c.jpg)  
Figure 6. Fast Fourier Transform result of Equation (9). $( i \neq i _ { m } )$

## 4. Simulation Results

The block diagram of the radar simulation is shown in Figure 7. In this simulation we consider the environment where five targets exist, and six interference signals are mixed with the true target signal. Each target and interference were randomly generated within the range of 0–150 m and relative velocity was randomly set between $- 1 0 0 \ \mathrm { m / s } \ ( - 3 6 0 \ \mathrm { k m / h } ) { - } 5 0 \ \mathrm { m / s }$ (180 km/h). The simulation parameters are shown in Table 1. The SNR of the AWGN versus the beat signal of the target used in the simulation was calculated based on the path loss model of reference [2]. We use a hybrid of OS-CFAR and CA-CFAR algorithm to improve the detection accuracy [18].

![](images/21c08031f2c8829d8827dbbb1cb4eeb0af5af86d64e59c14e71bbdd29ee5a7a4.jpg)  
Figure 7. FMCW radar simulation block diagram.

Table 1. Simulation parameters.
<table><tr><td>Specification</td><td>Value</td></tr><tr><td>Carrier Frequency  $( f _ { c } )$ </td><td>77 GHz</td></tr><tr><td>Sampling Frequency  $( F _ { s } )$ </td><td>10 MHz</td></tr><tr><td>FFT point</td><td>8192</td></tr><tr><td>CFAR window</td><td>16</td></tr><tr><td>CA-CFAR Guard Cell</td><td>2</td></tr><tr><td>OS-CFAR Rank Selection (r)</td><td>4</td></tr></table>

In the simulation, a single period of a chirp sequence is composed of four short chirp sequences with different frequency slopes. Each short chirp sequence lasts 0.5 ms (the total chirp sequence is 2 ms) with the frequency slopes selected from the four different values of ±1200, ±900, ±600, ±300 MHz/msec. If we do not allow the overlap of the same frequency slopes in the same short chirp interval, only eight short chirp sequence patterns are available as shown in Table 2. All short chirp sequences except the short chirp sequence of Table 2 do not satisfy the constraint for choosing the short chirp sequence described above. To verify the performance of the proposed method, we compare with the case where all the vehicles share the same short chirp sequences (which we denote as a conventional method) and where each vehicle use their own chirp sequence (which we denote as a proposed method).

Table 2. Example of chirp sequence patterns.
<table><tr><td rowspan=1 colspan=1>Chirp Sequences (MHz/ms)</td></tr><tr><td rowspan=1 colspan=1>(1200, 900, 600, 300)(900, 300, 1200, 600)(600, 1200, 300, 900)(300, 600, 900, 1200)</td></tr><tr><td rowspan=1 colspan=1>-(1200, 900, 600, 300)-(900, 300, 1200, 600)-(600, 1200, 300, 900)-(300, 600, 900, 1200)</td></tr></table>

Before, we defined INR as an interference to noise ratio, which is the power ratio between the total interference and AWGN signal in dB. We compared the performance of the proposed method and the conventional method in terms of detection probability and the number of false alarms while varying the INR value from −30 dB to 0 dB. The INR range is determined based on the real traffic environment. Though the INR 0 dB may seem small, however, since interference is concentrated in a specific frequency components, it is not small compared with the transmitted signal. Each simulation was performed 10,000 times and the average value was compared in the comparisons.

In Figure 8, we have shown the detection probability of the true target in comparison with the conventional method. In this paper, we define detection probability as $\begin{array} { r l } { P _ { D } ( \% ) } & { { } = } \end{array}$ Number of matching Number of total true $\frac { \mathrm { t a r g e t s } } { \mathrm { t a r g e t s } } \times 1 0 0$ . Here, the matching target means a detected target whose range and velocity difference with the true target is below a certain threshold. In Figure 8, the x-axis represents the INR defined in the previous section and y-axis represents the detection probability. When the INR value is less than −20 dB, the effect of interference is very small, so the difference of the detection probability between the proposed and conventional method is small. When the INR is greater than −20 dB, the detection probability of the conventional method decreases whereas that of the proposed method hardly changes as the INR increases. As INR approaches 0 dB, the interference signal power increases significantly compared with the signal power from the true target. In this case the detection probability of both the two methods decreases, however, the proposed system still outperforms the conventional one.

![](images/98b19bcb27c383292e09408d3f1b8d4d620a3483e681d853e55edafd933bbcad.jpg)  
<sup>Figure</sup> <sup>8.</sup> <sup>Detection</sup> <sup>probability</sup> <sup>of</sup> <sup>the</sup> <sup>proposed</sup> <sup>and</sup> <sup>conventional</sup> <sup>methods.</sup> <sub>Figure</sub> <sub>8. Detection</sub> <sub>probability</sub> <sub>of</sub> <sub>the</sub> <sub>proposed</sub> <sub>and</sub> <sub>conventional</sub> <sub>methods.</sub>

<sub>When</sub> <sub>the</sub> <sub>INR</sub> <sub>value</sub> <sub>is</sub> <sub>−30</sub> <sub>dB,</sub> <sub>the</sub> <sub>performance</sub> <sub>of</sub> <sub>the</sub> <sub>proposed</sub> <sub>method</sub> <sub>is</sub> <sub>very</sub> <sub>similar</sub> <sub>to</sub> <sub>that</sub> <sub>of</sub> <sub>the</sub> In Figure 9, we show the average number of the false targets detected as we increase the INR. conventional method in terms of false alarms. As the INR value increases the number of false targets When the INR value is −30 dB, the performance of the proposed method is very similar to that of increases accordingly. However, the number of the false targets of the conventional method is the conventional method in terms of false alarms. As the INR value increases the number of false <sup>significantly</sup> <sup>larger</sup> <sup>than</sup> <sup>the</sup> <sup>proposed</sup> <sup>method.</sup> <sup>In</sup> <sup>the</sup> <sup>proposed</sup> <sup>method,</sup> <sup>though</sup> <sup>the</sup> <sup>INR</sup> <sup>value</sup> targets increases accordingly. However, the number of the false targets of the conventional method <sup>increases</sup> <sup>up</sup> <sup>to</sup> <sup>−10</sup> <sup>dB,</sup> <sup>the</sup> <sup>interference</sup> <sup>is</sup> <sup>filtered</sup> <sup>through</sup> <sup>the</sup> <sup>CFAR,</sup> <sup>and</sup> <sup>the</sup> <sup>false</sup> <sup>alarm</sup> <sup>rarely</sup> <sup>occurs.</sup> is significantly larger than the proposed method. In the proposed method, though the INR value increases up to −10 dB, the interference is filtered through the CFAR, and the false alarm rarely occurs. If the INR value is greater than −10 dB, the number of false alarms generated in the proposed method starts to increase. However, the performance of the proposed method is still much better than the conventional method. This shows that the proposed method effectively removes the false targets unlike the conventional method which is susceptible to the interference generated by other neighboring vehicles.

![](images/73e6e9502a6377accffab7fdf4a1f9d05967b45adeb153afa5e4d1f0c75a839b.jpg)  
<sup>Figure</sup> <sup>9.</sup> <sup>Average</sup> <sup>number</sup> <sup>of</sup> <sup>the</sup> <sup>false</sup> <sup>targets</sup> <sup>of</sup> <sup>the</sup> <sup>proposed</sup> <sup>and</sup> <sup>conventional</sup> <sup>methods.</sup> <sub>Figure</sub> <sub>9.</sub> <sub>Average</sub> <sub>number</sub> <sub>of</sub> <sub>the</sub> <sub>false</sub> <sub>targets</sub> <sub>of</sub> <sub>the</sub> <sub>proposed</sub> <sub>and</sub> <sub>conventional</sub> <sub>methods.</sub>

## 5. Conclusions

Y.-S.S. made the verification code and wrote the draft version of this paper. H.-K.S. verified the details of the <sub>Author</sub> <sub>Contributions:</sub> <sub>S.W.H.</sub> <sub>conceived</sub> <sub>the</sub> <sub>problem,</sub> <sub>proposed</sub> <sub>the</sub> <sub>ideas</sub> <sub>on</sub> <sub>this</sub> <sub>paper</sub> <sub>and</sub> <sub>revised</sub> <sub>manuscript.</sub> Y.-S.S. made the verification code and wrote the draft version of this paper. H.-K.S. verified the details of the <sub>Funding:</sub> <sub>This</sub> <sub>work</sub> <sub>was</sub> <sub>supported</sub> <sub>partly</sub> <sub>by</sub> <sub>the</sub> <sub>Nationa</sub>proposed method and reviewed the manuscript for revision.

<sup>Grants</sup> <sup>NRF-2016R1D1A1B03930910</sup> <sup>and</sup> <sup>by</sup> <sup>the</sup> <sup>Korea</sup> <sup>Electric</sup> <sup>Power</sup> <sup>Corporation</sup> <sup>(Grant</sup> <sup>number:</sup> <sup>R18XA02).</sup> Funding: This work was supported partly by the National Research Foundation of Korea (NRF) under the Grants NRF-2016R1D1A1B03930910 and by the Korea Electric Power Corporation (Grant number: R18XA02).

<sup>suggestions</sup> <sup>that</sup> <sup>helped</sup> <sup>improve</sup> <sup>the</sup> <sup>manuscript.</sup> Acknowledgments: We appreciate all the anonymous reviewers for their constructive comments and suggestions that helped improve the manuscript.

Conflicts of Interest: The authors declare no conflict of interest.

## <sub>1. G</sub>References

1. Gustafsson, F. Automotive Safety Systems. IEEE Signal Proc. Mag. 2009, 26, 32–47. [CrossRef]

2. Brooker, G.M. Mutual Interference of Millimeter-Wave Radar Systems. IEEE Trans. Electromagn. Compat. 2007, 49, 170–181. [CrossRef]

3. Goppelt, M.; Blöcher, H.-L.; Menzel, W. Analytical Investigation of Mutual Interference between Automotive 4. Beise, H.-P.; Stifter, T.; Schröder, U. Virtual Interference Study for FMCW and PMCW Radar. In FMCW Radar Sensors. In Proceedings of the IEEE German Microwave Conference, Darmstadt, Germany, Proceedings of the IEEE 2018 11th German M14–16 March 2011; IEEE: Piscataway, NJ, USA, 2011.

4. 12–14 March 2018; IEEE: Piscataway, NJ, USA, 2018. Beise, H.-P.; Stifter, T.; Schröder, U. Virtual Interference Study for FMCW and PMCW Radar. In Proceedings of the IEEE 2018 11th German Microwave Conference (GeMiC), Freiburg, Germany, 12–14 March 2018; IEEE: Piscataway, NJ, USA, 2018.

5. Gurgel, K.-W.; Barbin, Y.; Schlick, T. Radio Frequency Interference Suppression Techniques in FMCW Modulated HF Radars. In Proceedings of the IEEE OCEANS Conference, Aberdeen, UK, 18–21 June 2007; IEEE: Piscataway, NJ, USA, 2007.

6. Wagner, M.; Sulejmani, F.; Melzer, A.; Meissner, P.; Huemer, M. Threshold-Free Interference Cancellation Method for Automotive FMCW Radar Systems. In Proceedings of the 2018 IEEE International Symposium on Circuits and Systems (ISCAS), Florence, Italy, 27–30 May 2018; IEEE: Piscataway, NJ, USA, 2018.

7. Rameez, M.; Dahl, M.; Pettersson, M.I. Adaptive Digital Beamforming for Interference Suppression in Automotive FMCW Radars. In Proceedings of the 2018 IEEE Radar Conference (RadarConf18), Oklahoma City, OK, USA, 23–27 April 2018; IEEE: Piscataway, NJ, USA, 2018.

8. Uysal, F.; Sanka, S. Mitigation of Automotive Radar Interference. In Proceedings of the 2018 IEEE Radar Conference (RadarConf18), Oklahoma City, OK, USA, 23–27 April 2018; IEEE: Piscataway, NJ, USA, 2018.

9. Wang, W.; Shao, H. Radar-to-Radar Interference Suppression for Distributed Radar Sensor Networks. Remote Sens. 2014, 6, 740–755. [CrossRef]

10. Bechter, J.; Rameez, M.; Waldschmidt, C. Analytical and Experimental Investigation on Mitigation of Interference in a DBF MIMO Radar. IEEE Trans. Microw. Theory Tech. 2017, 65, 1727–1734. [CrossRef]

11. Ding, F.; Huang, X.; Wen, B.; Yan, Z. Aliasing Radar Receiver in FMICW System. IEICE Electron. Express 2010, 7, 697–703. [CrossRef]

12. Kronauge, M.; Rohling, H. New Chirp Sequence Radar Waveform. IEEE Trans. Aerosp. Electron. Syst. 2014, 50, 2870–2877. [CrossRef]

13. Hyun, E.; Jin, Y.; Lee, J. A Pedestrian Detection Scheme Using a Coherent Phase Difference Method Based on 2D Range-Doppler FMCW Radar. Sensors 2016, 16, 124. [CrossRef] [PubMed]

14. Rohling, H. Radar CFAR Thresholding in Clutter and Multiple Target Situations. IEEE Trans. Aerosp. Electron. Syst. 1983, 4, 608–621. [CrossRef]

15. Hyun, E.; Oh, W.; Lee, J.-H. Multi-Target Detection Algorithm for FMCW Radar. In Proceedings of the IEEE Radar Conference, Atlanta, GA, USA, 7–11 May 2012; IEEE: Piscataway, NJ, USA, 2012.

16. Zhou, H.; Cao, P.; Chen, S. A Novel Waveform Design for Multi-Target Detection in Automotive FMCW Radar. In Proceedings of the IEEE Radar Conference, Philadelphia, PA, USA, 2–6 May 2016; IEEE: Piscataway, NJ, USA, 2016.

17. Lee, T.-Y.; Jeon, S.-Y.; Han, J.; Skvortsov, V.; Nikitin, K.; Ka, M.-H. A Simplified Technique for Distance and Velocity Measurements of Multiple Moving Objects Using a Linear Frequency Modulated Signal. IEEE Sens. J. 2016, 16, 5912–5920. [CrossRef]

18. Kok, D.; Fu, J.S. Signal Processing for Automotive Radar. In Proceedings of the IEEE International Radar Conference, Arlington, VA, USA, 9–12 May 2005; IEEE: Piscataway, NJ, USA, 2005.