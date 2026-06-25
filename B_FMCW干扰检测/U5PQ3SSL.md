Article

# FMCW Radar System Interference Mitigation Based on Time-Domain Signal Reconstruction

Zhengguang Xu \* and Shanyong Wei

School of Electronic Information and Communications, Huazhong University of Science and Technology, Wuhan 430074, China; weishanyong@hust.edu.cn

\* Correspondence: xray@hust.edu.cn

Abstract: In this study, an interference detection and mitigation method is proposed for frequencymodulated continuous-wave radar systems based on time-domain signal reconstruction. The interference detection method uses the difference in one-dimensional fast Fourier transform (1D-FFT) results between targets and interferences. In the 1D-FFT results, the target appears as a peak at the same frequency point for all chirps within one frame, whereas the interference appears as the absence of target peaks within the first or last few chirps within one frame or as a shift in the target peak position in different chirps. Then, the interference mitigation method reconstructs the interference signal in the time domain by the estimated parameter from the 1D-FFT results, so the interference signal can be removed from the time domain without affecting the target signal. The simulation results show that the proposed interference mitigation algorithm can reduce the amplitude of interference by about 25 dB. The experimental results show that the amplitude of interference is reduced by 20–25 dB, proving the effectiveness of the simulation results.

Keywords: frequency-modulated continuous-wave radar; time-domain signal reconstruction; interference detection; interference mitigation

![](images/070a5ae83701ca0aa5d26d9223c26cb1240bfea4cf9d047383b6c1d3c321cf11.jpg)

Citation: Xu, Z.; Wei, S. FMCW Radar System Interference Mitigation Based on Time-Domain Signal Reconstruction. Sensors 2023, 23, 7113. https://doi.org/10.3390/s23167113

Academic Editors: Federico Aliment and Roberto Vincenti Gatt

Received: 22 July 2023   
Revised: 5 August 2023   
Accepted: 8 August 2023   
Published: 11 August 2023

![](images/efdb76ba8c4bbe9ba8b5a4e8fcbd2131e03a08fcb8b14e841e2006e93eef089f.jpg)

Copyright: © 2023 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

## 1. Introduction

Frequency-modulated continuous-wave (FMCW) radars have become a key sensor in advanced driver assistance systems (ADAS) due to their high resolution, all-weather capability, and simple system structure. With the increasing number of vehicles equipped with radar sensors on the road and limited spectrum resources, FMCW radar systems installed on different vehicles will inevitably be affected by interference from adjacent vehicle radar systems and other FMCW radars on the same vehicle. The main purpose of FMCW radars in preventing traffic accidents is collision avoidance and target detection. If interference occurs between radars and affects the normal operation of the radar system, it may cause ADAS to make incorrect judgments, resulting in incalculable losses. Therefore, it is critical to keep the vehicle radar system operational and mitigate mutual radar interference.

FMCW radars obtain specific information about a target using the intermediate frequency (IF) signal between the transmitted signal and the target reflection signal. However, if the interfered frequency difference signal is directly processed using two-dimensional fast Fourier transform (2D-FFT), the target detection performance will be poor. Specifically, some noise levels will be elevated, drowning out weak targets and reducing the target detection rate. The appearance of ghost targets causes radar false alarms. Over the past fifteen years, the properties and impacts of these interferences have been extensively studied [1,2]. The derivation of the interference duration and the form of the interference in an FMCW radar receiver due to different waveforms can be found in [3]. When the modulation slopes of two FMCW radar signals are different, it causes an elevation of the noise floor. In [4], the influence of interference on range-Doppler imaging is studied in this case. When the modulation slopes are the same, ghost targets may appear. The analytical formula for calculating the probability of ghost target occurrence was presented in [5]. The appearance<sup>was</sup> <sup>presented</sup> <sup>in</sup> <sup>[5].</sup> <sup>The</sup> <sup>appearance</sup> <sup>of</sup> <sup>ghost</sup> <sup>targets</sup> <sup>is</sup> <sup>a</sup> <sup>more</sup> <sup>severe</sup> <sup>and</sup> <sup>critical</sup> of ghost targets is a more severe and critical anomaly for current ADAS systems compared<sup>anomaly</sup> <sup>for</sup> <sup>current</sup> <sup>ADAS</sup> <sup>systems</sup> <sup>compared</sup> <sup>to</sup> <sup>the</sup> <sup>elevation</sup> <sup>of</sup> <sup>the</sup> <sup>noise</sup> <sup>floor.</sup> <sup>The</sup> to the elevation of the noise floor. The scenario of ghost target interference is shown inscenario of ghost target interference is shown in Figure 1. The vehicle in the picture is Figure 1. The vehicle in the picture is equipped with two forward-facing radars. When theequipped with two forward-facing radars. When the signal transmitted by the left radar signal transmitted by the left radar is reflected by the vehicle in front and received by theis reflected by the vehicle in front and received by the right radar, ghost target right radar, ghost target interference will form.interference will form.

![](images/1f56e5c72c272e171294fc88672d2741c68d8ce68c31648bbba9025ef31288d4.jpg)  
<sup>Figure</sup> <sup>1.</sup> <sup>False</sup> <sup>target</sup> <sup>interference</sup> <sup>scenario.</sup><sub>Figure</sub> <sub>1. False</sub> <sub>target</sub> <sub>interference</sub> <sub>scenario.</sub>

From 2010 to 2012, the European Union project More Safety for All by Radar From 2010 to 2012, the European Union project More Safety for All by Radar Inter-Interference Mitigation (MOSARIM) [6] conducted extensive research on vehicle radar ference Mitigation (MOSARIM) [6] conducted extensive research on vehicle radar interinterference and divided interference mitigation (IM) methods into six categories: ference and divided interference mitigation (IM) methods into six categories: polarized polarized antenna, time-domain, frequency-domain, spatial-domain, coding, and antenna, time-domain, frequency-domain, spatial-domain, coding, and strategy coordinastrategy coordination methods. The above IM methods are to perform corresponding tion methods. The above IM methods are to perform corresponding signal processing at signal processing at the transmitting or receiving signal. Among them, the methods in the the transmitting or receiving signal. Among them, the methods in the polarized antenna polarized antenna and spatial-domain categories have a limitation in resolving and spatial-domain categories have a limitation in resolving interference issues in vehicleinterference issues in vehicle-mounted radars. Therefore, the methods in the mounted radars. Therefore, the methods in the time-domain, frequency-domain, coding, time-domain, frequency-domain, coding, and strategy-domain categories are mainly and strategy-domain categories are mainly considered to effectively solve the interference considered to effectively solve the interfeproblem of vehicle-mounted FMCW radars.

<sub>s.</sub>Time domain: Find the location of the interference in the time domain, and then <sub>Time</sub> <sub>domain:</sub> <sub>Find</sub> <sub>the</sub> <sub>location</sub> <sub>of</sub> <sub>the</sub> <sub>interference</sub> <sub>in</sub> <sub>the</sub> <sub>time</sub> <sub>domain,</sub> <sub>and</sub> <sub>then use</sub> use the windowing method [7,8] to mitigate the interference. Additionally, an adaptive the windowing method [7,8] to mitigate the interference. Additionally, an adaptive <sup>filtering</sup> <sup>method</sup> <sup>based</sup> <sup>on</sup> <sup>a</sup> <sup>phase-modulated</sup> <sup>continuous-wave</sup> <sup>radar</sup> <sup>system</sup> <sup>[9]</sup> <sup>and</sup> filtering method based on a phase-modulated continuous-wave radar system [9] and a <sup>a</sup> <sup>method</sup> <sup>based</sup> <sup>on</sup> <sup>morphological</sup> <sup>component</sup> <sup>analysis</sup> <sup>[10]</sup> <sup>for</sup> <sup>IM</sup> <sup>have</sup> <sup>already</sup> <sup>been</sup> <sub>method</sub> <sub>based</sub> <sub>on</sub> <sub>morphological</sub> <sub>component</sub> <sub>analysis</sub> <sub>[10]</sub> <sub>for</sub> <sub>IM</sub> <sub>have</sub> <sub>already</sub> <sub>been</sub> proposed elsewhere. In [11], a method is proposed to minimize the correlation between radar waveforms using the particle swarm optimization algorithm. The optimal filtering is achieved by the least mean squares (LMS) algorithm based on the reference signal to output interference suppression result. The main problem with time-domain methods is accurately locating the interference and then completely removing it from the signal.

Frequency domain: An adaptive noise cancellation IM method was proposed in [12]. A wavelet de-noising method [13] is also used to extract interference signals in the time domain and then suppress them to achieve IM. A two-stage approach for suppressing the mutual interference between FMCW radars was proposed in [14]. In the first stage, the signals corresponding to the strong interference components or targets are separated using the singular value decomposition (SVD) technique across the spatial domain. Following this, each separated signal at each receive channel is further decomposed into different frequency components using various mode decomposition techniques. In [15], IM is primarily achieved by cutting the interfered signal samples of FMCW radars in the shorttime Fourier transform domain and then reconstructing the signal in the interfered area using an auto-regressive (AR) model based on the signal that has not been interfered with. In [16], a constant false alarm rate (CFAR)-based framework is proposed to mitigate interference in FMCW radars. In this framework, a one-dimensional CFAR detector is used for interference detection (ID), and signal reconstruction is performed using the Burgs method in the AR model or the amplitude correction method. Frequency-domain methods mainly identify the interference position in the frequency domain and then suppress the interference. However, to suppress the interference frequency as much as possible, the detected interference area is typically extended in the frequency domain, which can have a significant impact on the power of the useful signal.

Coding domain: In [17], an effective method for reducing mutual interference is proposed by performing random sub-band spectral analysis. The main implementation method is to randomly split a large triangular wave voltage into multiple triangular waves in the signal control unit. In [18], a new phase-coded FMCW system is proposed, where the transmitted waveform uses bipolar phase coding, and a group delay filter is used to process the unaligned phase-coded radar echo signals. Moreover, the orthogonality of randomly coded chirp signals [19] is used for IM. Coding-domain methods require changes in the radar operating mode or the style of the transmitted signal, they have high implementation complexity, and it is difficult to establish unified standards.

Strategy methods, such as reinforcement learning techniques [20,21], deep learning techniques [22,23], and generative adversarial networks [24], have been used for IM in FMCW radars. These methods require a large amount of data for training, they have high computational complexity, and the hardware implementation is complex.

At present, there are many studies on radar IM, but there are few studies on ghost target IM as shown in Figure 1. This article focuses on the detection and mitigation of this interference. In this study, we propose a framework for interference detection and mitigation in FMCW radars based on time-domain signal reconstruction. In the proposed framework, both the interference and reflected signals from the target are mixed with the transmission signal of the victim radar, which is identical to the transmission signal of the aggressor radar. Then, target detection is performed based on the 1D-FFT result of the IF signal. Furthermore, the range index where the interference occurs is found according to the target result. The interference signal frequency is calculated based on the 1D-FFT results of the interference point and its two adjacent points. In addition, the amplitude and phase of the interference signal are calculated based on the interference signal frequency. After the interference signal is recovered, it is removed from the original data samples to suppress the influence of ghost targets. Compared with existing methods, our method can effectively remove ghost targets without affecting the target signal. The interference detection and mitigation effect of our method have been validated through simulation and experimental results making it suitable for real-time interference detection and mitigation in FMCW radars. The main contributions of the study may be summarized as follows:

Many relevant studies focus more on IM methods and neglect ID methods. This article proposes a clear and feasible ID method to distinguish between normal targets and interferences.

This article proposes an IM method with strong suppression ability, which can achieve higher anti-interference performance and interference intensity reduction than other methods under high signal–noise ratio (SNR) conditions.

This article proposes a complete framework for an FMCW radar system, which includes three steps: target detection, interference detection, and interference mitigation.

The rest of this paper is organized as follows: Section 2 briefly introduces the signal model of FMCW radars. Then, the proposed interference detection and mitigation method based on time-domain signal reconstruction is presented in Section 3. Simulation and experimental results are presented in Sections 4 and $5 ,$ respectively, to demonstrate the antiinterference performance of our proposed method. Finally, the conclusions and outlook are presented in Section 6.

## 2. Signal Model

Assume that the transmitted signal $s _ { c } ( t )$ of the victim radar A in one chirp is as follows:

$$
s _ { c } ( t ) = e ^ { j 2 \pi ( f _ { 0 } t + \frac { 1 } { 2 } S t ^ { 2 } + \varphi ) } 0 \leq t < T _ { c }\tag{1}
$$

where $f _ { 0 }$ denotes the initial frequency of the transmitted signal of radar $\mathbf { A } , S$ denotes the modulation slope, $\varphi$ denotes the initial phase of the transmitted signal of radar $\mathbf { A } ,$ and $T _ { c }$ denotes the duration of the chirp. As depicted in Figure 2, the transmitted signal $s ( t )$ of radar A in one frame is as follows:

$$
s _ { f } ( t ) = \left\{ \begin{array} { c c } { s _ { c } ( t - m T _ { c } ) } & { m T _ { c } \leq t < ( m + 1 ) T _ { c } , m = 0 , 1 , \cdots , M - 1 } \\ { 0 } & { M T _ { c } \leq t < T _ { f } } \end{array} \right.\tag{2}
$$

where M represents the number of chirps within a frame, m represents the number of chirps, and $T _ { f }$ denotes the duration of a frame.

![](images/b7cf7374e21b7ca98b87c41d71777228115d1976ba4aede7c3288f417e50f890.jpg)  
Figure 2. <sup>Schematic</sup> <sup>of</sup> <sup>an</sup> <sup>FMCW</sup> <sup>radar</sup> <sup>signa</sup>Figure 2. Schematic of an FMCW radar signal.

If the transmitted signal of aggressor radar B is consistent with that of radar A, When the modulation slope of the signal transmitted by the aggressor radar is the same as that of the victim radar, the aggressor radar signal is received by radar $\mathbf { A } ,$ and the interfering signal $s _ { \mathrm { i n t } } ( t ) = s ( t - \tau _ { d } ( t ) )$ , where $\tau _ { d } ( t )$ is a time delay function, consists of delay and time drift. For the convenience of research, we assume that each frame of radar <sup>the</sup> <sup>2D-FFT</sup> <sup>results</sup> <sup>of</sup> <sup>x</sup> <sup>t(</sup> <sup>)</sup> <sup>.</sup> data is independent. When analyzing in one chirp, we consider the frequency difference between the received signal and interference signal to be approximately constant, neglecting the minor effects of time drift. Considering $P$ multiple targets and $Q$ multiple interfering signals simultaneously, the signal collected by radar A after mixing and low-pass filtering can be expressed as follows:

$$
x ( t ) = s _ { b } ( t ) + \tilde { s } _ { \mathrm { i n t } } ( t ) + n ( t ) \quad 0 \leq t < T _ { f } ,\tag{3}
$$

where

$$
s _ { b } ( t ) = \sum _ { p = 1 } ^ { P } \alpha _ { p } e ^ { j 2 \pi ( S \tau _ { p } t + f _ { 0 } \tau _ { p } ) }\tag{4}
$$

denotes the echo signal of P multiple targets, and

$$
\tilde { s } _ { \mathrm { i n t } } ( t ) = \left[ s ^ { * } ( t ) \sum _ { q = 1 } ^ { Q } s _ { \mathrm { i n t } } ( t , q ) \right] * h _ { l p } ( t )\tag{5}
$$

denotes the residual interference signal after mixing and low-pass filtering. Here, $s ^ { * } ( t )$ represents the complex conjugate of $s ( t )$ used for signal mixing. The qth interfering signal is defined as $s _ { \mathrm { i n t } } ( t , q ) = s _ { q } ( t - \tau _ { d } ( t ) )$ , where $\tau _ { d } ( t )$ denotes a time delay function composed of delay and time drift. Then, $h _ { l p } ( t )$ denotes a low-pass filter with a threshold of <sup>Figure</sup> <sup>3.</sup> <sup>The</sup> <sup>2D-FFT</sup> <sup>result</sup> <sup>diagram</sup> <sup>of</sup> <sup>x</sup> <sup>t(</sup> <sup>)</sup> <sup>(including</sup> <sup>moving</sup> <sup>target,</sup> <sup>stationary</sup> <sup>target,</sup> bandwidth (BW). If the mixed frequency is not within the BW of the low-pass filter, the interfering signal). interference signal does not affect radar A. Finally, n(t) indicates the system noise and measurement error.

x t m m M( ), , 0,1,..., 1= −If the transmitted signal of aggressor radar B is consistent with that of radar $\scriptstyle \mathbf { A } ,$ the output result $\widetilde { s } _ { \mathrm { i n t } } ( t )$ is similar to the target after mixing and low-pass filtering. As depicted

in Figure 3, we cannot effectively distinguish the target and interference from the 2D-FFTthe 2D-FFT results of x t<sub>( )</sub> .   
results of x(t).

![](images/28956091888e25c9a3d118b543b1b6395de3853995b48c3be4190a548bb752de.jpg)  
Figure 3. The 2D-FFT result diagram of x t( ) (including moving target, stationary target, andFigure 3. The 2D-FFT result diagram of x(t) (including moving target, stationary target, and interferinterferinging signal).

The IF signals $x ( t , m ) , m = 0 , 1 , \ldots , M - 1$ of all chirps in a frame after mixing pro-<sup>The</sup> <sup>IF</sup> <sup>signals</sup> <sup>of</sup> <sup>all</sup> <sup>chirps</sup> <sup>in</sup> <sup>a</sup> cessing are sampled at N points to obtain the sampling signal of $x ( n , m ) = x ( n \Delta t , m )$ $n = 0 , \overset { \cdot } { 1 } , \ldots , N - \overset { \cdot } { 1 }$ <sup>sampled</sup> <sup>at</sup> <sup>N</sup> <sup>poin</sup>, and the sampling rate is $\mathrm { f } _ { \mathrm { s } } ,$ <sup>to</sup> <sup>obtain</sup> <sup>the</sup> <sup>sampling</sup> <sup>signal</sup> <sup>of</sup> the sampled signal is processed by 1D-FFT <sup>x n m</sup> <sup>x n</sup> <sup>t m</sup> <sup>n</sup> <sup>N</sup> <sup>(</sup> <sup>,</sup> <sup>)</sup> <sup>(</sup> <sup>,</sup> <sup>),</sup> <sup>0,1,...,</sup> <sup>1</sup> <sup>= ∆</sup> <sup>=</sup> <sup>−</sup> <sub>,</sub> <sub>and</sub> <sub>the</sub> <sub>sampling</sub> <sub>rate</sub> <sub>is</sub> <sub>f ,</sub> <sub>the</sub> <sub>sam</sub>in the range dimension, and the corresponding 1D-FFT result is as follows:

$$
X ( k , m ) = \sum _ { n = 0 } ^ { N - 1 } x ( n , m ) e ^ { - j 2 \pi { \frac { n k } { N } } } ,\tag{6}
$$

where $k = 0 , 1 , 2 \ldots N - 1$

Because of signal sampling and the existence of time delay functions, the frequency k N <sup>=</sup> <sup>−</sup> 0,1, 2... 1difference between the interference and transmitted signals of the victim radar is constantly changing. The time delay function is determined by the delay and time drift, where the delay represents the time difference between the interference signal and the victim radar. Due to the delay, in the 1D-FFT domains, the peaks introduced by the interference radar are absent in the first or last few chirps within one frame. The time drift affects the alignment of the two radar clocks, which changes the frequency difference between the two signals, and $\eta$ represents the time drift rate. When the frequency difference between two signals exceeds the frequency resolution $\Delta f = f _ { s } / N$ within a continuous frame of time, where $f _ { s }$ is the sampling rate of the FMCW radar, a change in the target frequency will be detected in the 1D-FFT result. At this time, the interference signal in the 1D-FFT result behaves similarly to a fast-moving object. Additionally, the critical time drift rate $\eta _ { 0 }$ is as follows:

$$
\eta _ { 0 } = \frac { f _ { s } } { N M T _ { c } S }\tag{7}
$$

Assume that the clocks of the two radars are aligned at a certain moment, as depicted in Figure 4a, and the first frequency difference between the two signals after mixing is 0. Due to the time drift, the frequency difference between the two signals keeps increasing, as depicted in Figure 4b; when the frequency difference exceeds BW (blue dotted line in Figure 4), the interfering signal will not affect radar A because of the low-pass filter. Over time, as shown in Figure 4c, the interfering signal aligns with the later chirp, the frequency difference between the two signals slowly decreases within the range of the low-pass filter, and the interfering signal again affects radar A. As expressed in (2), there is a long idle time for the radar after sending all chirp signals in one frame, as shown in Figure 4d. Over time, if all chirp signals emitted by radar B are aligned with the idle time of radar A, the interfering signal will not affect the victim radar.

![](images/f86b850aa5bb01e526948ac0e168e63eafb2c816e35dca03c22c77908478a757.jpg)  
(a)

![](images/31af1a31b6c7dd2356e18be568ffbed9980ee18c739f4c5cd514f3737d72549d.jpg)  
(b)

![](images/88c51782f3ea3c2b96c57e320c55ee79340b0a4a3b9eb52ae37f67d0e34edd72.jpg)  
(c)

![](images/2155fd3008c1ba9145915837b1a25bbc19b39900cf1c70456702b832c6252ad4.jpg)  
(d)  
<sup>re</sup> <sup>4.</sup> <sup>Schematic</sup> <sup>of</sup> <sup>aggressor</sup> <sup>and</sup> <sup>victim</sup> <sup>radar</sup> <sup>signals</sup> <sup>whe</sup>Figure 4. Schematic of aggressor and victim radar signals when $\eta \leq \eta _ { 0 } \colon ( \mathbf { a } )$ <sup>(a)</sup> <sup>shows</sup> <sup>that</sup> <sup>the</sup> <sup>cloc</sup> shows that the clocks of aggressor and victim radars are aligned at the beginning; (b) shows that the frequ<sub>the</sub> <sub>aggressor</sub> <sub>and</sub> <sub>victim</sub> <sub>radars</sub> <sub>are</sub> <sub>aligned</sub> <sub>at</sub> <sub>the</sub> <sub>beginning;</sub> <sub>(</sub>b<sub>)</sub> <sub>shows</sub> <sub>that</sub> <sub>the</sub> <sub>frequency</sub> <sub>difference</sub> erence between the aggressor and victim radar signals exceeds BW; (c) shows that the chi<sub>between</sub> <sub>the</sub> <sub>aggressor</sub> <sub>and</sub> <sub>victim</sub> <sub>radar</sub> <sub>signals</sub> <sub>exceeds</sub> <sub>BW;</sub> <sub>(c)</sub> <sub>shows</sub> <sub>that</sub> <sub>the</sub> <sub>chirp</sub> <sub>of</sub> <sub>the</sub> <sub>aggressor</sub> aggressor radar signal is aligned with the idle time of the victim radar; (d) shows that all ch<sub>radar</sub> <sub>signal</sub> <sub>is</sub> <sub>aligned</sub> <sub>with</sub> <sub>the</sub> <sub>idle</sub> <sub>time</sub> <sub>of</sub> <sub>the</sub> <sub>victim</sub> <sub>radar;</sub> <sub>(d)</sub> <sub>shows</sub> <sub>that</sub> <sub>all</sub> <sub>chirps</sub> <sub>of</sub> <sub>the</sub> <sub>aggressor</sub> <sup>e</sup> <sup>aggressor</sup> <sup>radar</sup> <sup>signal</sup> <sup>are</sup> <sup>aligned</sup> <sup>with</sup> <sup>the</sup> <sup>idle</sup> <sup>time</sup> <sup>o</sup>radar signal are aligned with the idle time of the victim radar.

In Figure 5, the 1D-FFT and target detection results under two interference scenarios $\eta \leq \eta _ { 0 }$ and $\eta > \eta _ { 0 }$ are shown, respectively. The figure shows stationary targets, moving targets, and two types of interference. The x-axis represents the chirp number, and the y-axis represents the range. Figure 5a,b is a decibel plot, and its specific dB values can be referred to the color bar in Figure 3. Figure 5c,d is a binary plot, where 1 represents the presence of the target and 0 represents the absence of the target. Figure 5a shows the 1D-FFT result of a delayed signal in one frame when $\eta < \eta _ { 0 }$ . For $\eta > \eta _ { 0 } ,$ the frequency difference between the two signals exceeds $\Delta f ,$ as shown in the 1D-FFT result in Figure 5b, and we can observe that the frequency of the interfering signal has changed. Next, we will design the ID scheme according to the property of the interference signal shown in Figure 5.

![](images/db26e1f469dfaab2009c28e98a9399d383e2b389c43b45d9d1fa22e04160cf30.jpg)  
(a)

![](images/d41ac6fcb661236a1cd967628cf064a15fd8ce7161e9e23b0228ed01d1ac89a0.jpg)  
(b)

![](images/f0abab76bd88f663fc5c07cfe40508704c586607be08c77b5e1770406b82ac39.jpg)  
(c)

![](images/627af2e9d3e24732a5112054cd4ecfd902f66c435a19d182eef4d80524a3d8d5.jpg)  
(d)  
Figure 5. The 1D-FFT result and the target detection result of the signal x t( ) : (aFigure 5. The 1D-FFT result and the target detection result of the signal x(t): (a,c) represent the result when $\eta \leq \eta _ { 0 } ; ( \mathbf { b } , \mathbf { d } )$ <sub>sult</sub> <sub>when</sub> ≤ <sub>;</sub> <sub>(b,d)</sub> <sub>re</sub> represent the result when $\eta > \eta _ { 0 } .$

## 3. Interference Detection and Mitigation Method

The ability to accurately detect interference is a key factor in effectively suppressing it. <sup>The</sup> <sup>ability</sup> <sup>to</sup> <sup>accurately</sup> <sup>detect</sup> <sup>interference</sup> <sup>is</sup> <sup>a</sup> <sup>key</sup> <sup>factor</sup> <sup>in</sup> <sup>effective</sup>Based on the analysis of the different distribution characteristics of targets and interferences <sup>it.</sup> <sup>Based</sup> <sup>on</sup> <sup>the</sup> <sup>analysis</sup> <sup>of</sup> <sup>the</sup> <sup>different</sup> <sup>distribution</sup> <sup>characteristics</sup> in the 1D-FFT results, targets appear as peaks at the same frequency point for all chirps <sup>interferences</sup> <sup>in</sup> <sup>the</sup> <sup>1D-FFT</sup> <sup>results,</sup> <sup>targets</sup> <sup>appear</sup> <sup>as</sup> <sup>peaks</sup> <sup>at</sup> <sup>the</sup> <sup>same</sup> <sup>f</sup>in a frame, the delay appears as the absence of target peaks in the first or last few chirps <sup>for</sup> <sup>all</sup> <sup>chirps</sup> <sup>in</sup> <sup>a</sup> <sup>frame,</sup> <sup>the</sup> <sup>delay</sup> <sup>appears</sup> <sup>as</sup> <sup>the</sup> <sup>absence</sup> <sup>of</sup> <sup>target</sup> <sup>peaks</sup> <sup>in</sup>within one frame, and the time drift appears as a deviation in the peak position of the <sup>few</sup> <sup>chirps</sup> <sup>within</sup> <sup>one</sup> <sup>frame,</sup> <sup>and</sup> <sup>the</sup> <sup>time</sup> <sup>drift</sup> <sup>appears</sup> <sup>as</sup> <sup>a</sup> <sup>deviatio</sup>target in different chirps. Therefore, by applying a 1D-CFAR detector to the 1D-FFT results <sup>position</sup> <sup>of</sup> <sup>the</sup> <sup>target</sup> <sup>in</sup> <sup>different</sup> <sup>chirps.</sup> <sup>Therefore,</sup> <sup>by</sup> <sup>applying</sup> <sup>a</sup> <sup>1D-CF</sup>and summing the target results in the range dimension, interference can be detected based <sup>the</sup> <sup>1D-FFT</sup> <sup>results</sup> <sup>and</sup> <sup>summing</sup> <sup>the</sup> <sup>target</sup> <sup>results</sup> <sup>in</sup> <sup>the</sup> <sup>range</sup> <sup>dimensio</sup>on the number of chirps in which the target exists and then is suppressed. The flowchart <sup>can</sup> <sup>be</sup> <sup>detected</sup> <sup>based</sup> <sup>on</sup> <sup>the</sup> <sup>number</sup> <sup>of</sup> <sup>chirps</sup> <sup>in</sup> <sup>which</sup> <sup>the</sup> <sup>target</sup> <sup>exi</sup>of the proposed interference detection and mitigation method is shown in Figure 6. The<sup>8</sup> <sup>of</sup> <sup>suppressed.</sup> <sup>The</sup> <sup>flowchart</sup> <sup>of</sup> <sup>the</sup> <sup>proposed</sup> <sup>interference</sup> <sup>detection</sup> <sup>and</sup> <sup>miti</sup>algorithm can be divided into three steps: target detection, interference detection, and <sup>is</sup> <sup>show</sup>interference mitigation.

![](images/08d9fc653967eaedba921320c4eb1b1ebf149aa42d7e5be9bb804d2c764def56.jpg)  
<sup>igure</sup> <sup>6.</sup> <sup>Flowchart</sup> <sup>of</sup> <sup>the</sup> <sup>proposed</sup> <sup>IM</sup> <sup>method</sup>Figure 6. Flowchart of the proposed IM method.

## 3.1. Target Detection

A cell-averaging CFAR (CA-CFAR) detector [25] is used for target detection, which detects the target peak in the 1D-FFT result and sets a threshold G to limit the target peak. The selection of reference cells, protected cells, the false alarm rate, etc., can be based on a specific scenario. Applying the CA-CFAR detector to each chirp results in a target matrix B(k, m), whose size is the chirp number M multiplied by sampling point number N, as depicted in Figure $5 c , \mathrm { d }$ . In each chip, the targets detected by the CFAR are represented by yellow dots. In Figure 5c, there is a target absence for the interference signal, and in Figure 5d, the targets introduced by the interference appear at different frequency points.

Compared with the normal targets in the 1D-FFT results, the interfering targets show different properties because of the time drift between the victim radar and the aggressor radar. The differences between the target and the interference prompt us to propose the interference detection and mitigation method, as shown in Algorithm 1.

Algorithm 1. IM Method Based on Time-domain Signal Reconstruction   
Data: complex signal x(n, m) after mixing   
Results: complex signal $x ^ { \prime } ( n , m )$ after IM   
Begin   
X(k, m) = FFT(x(n, m));[N, M] = size(X(k, m));   
B = CA − CFARDetector(X);   
For k = 1 to N   
If $\sum _ { m = 0 } ^ { M - 1 } B ( k _ { 0 } , m ) + \operatorname* { m a x } \left( \sum _ { m = 0 } ^ { M - 1 } B ( k _ { 0 } + 1 , m ) , \sum _ { m = 0 } ^ { M - 1 } B ( k _ { 0 } - 1 , m ) \right) < K$   
For m = 1 to M   
If B(k , m ) == 1   
I(k , m ) = 1;   
x (n, m) = TimeReconstruction(X, x); i = i + 1;   
End   
End   
End   
$\mathop { x _ { I F } } ^ { \mathbf { \theta } } ( n , m ) = \sum _ { i = 1 } ^ { C } x _ { i } ( n , m ) ;$   
$x ^ { \prime } ( n , m ) = x ( n , m ) - x _ { I F } ( n , m ) ;$   
End   
End

## 3.2. Interference Detection

After the above processing, the target result $B ( k ,$ m) is detected in the range dimension. For the current frequency point $k _ { 0 } ,$ , the ID formula is as follows:

$$
\sum _ { m = 0 } ^ { M - 1 } B ( k _ { 0 } , m ) + \operatorname* { m a x } \left( \sum _ { m = 0 } ^ { M - 1 } B ( k _ { 0 } + 1 , m ) , \sum _ { m = 0 } ^ { M - 1 } B ( k _ { 0 } - 1 , m ) \right) < K\tag{8}
$$

where $K$ is an empirical parameter with values ranging from 0 to $M ,$ and max() represents the maximum value of the content in parentheses. If the number of targets at the frequency point satisfies (8), it is judged that the frequency point is an interference frequency point; otherwise, it is a target. Considering that the target may jitter in the range dimension, we consider the number of targets in the adjacent range dimension when calculating the number of targets.

After detection in the Doppler dimension, an ID result $I ( k ,$ m) with the same size as the target detection result is obtained.

## 3.3. Interference Mitigation

After obtaining the interference result $I ( k , m )$ through the above steps, we suppress the interference. Specifically, assuming that the total number of interference points is

$C , \ i = \ 0 , 1 . . . C ,$ we traverse all interference points $\left( k _ { i } , m _ { i } \right)$ in turn to reconstruct the interference signal. According to the 1D-FFT results of the chirp where the interference point is located, the interference signal $x _ { i } ( n , m )$ in the time domain is reconstructed. Now, the time-domain interference reconstruction (TIR) scheme is detailed below.

The interference frequency is calculated by

$$
f _ { i } = ( k _ { i } + \Delta k _ { i } ) \frac { f _ { s } } { N } ,\tag{9}
$$

where $\Delta k _ { i }$ denotes the index deviation as follows:

$$
\Delta k _ { i } = \left\{ \begin{array} { c c } { \frac { \left| X ( k _ { i } + 1 , m _ { i } ) \right| } { \left| X ( k _ { i } + 1 , m _ { i } ) \right| + \left| X ( k _ { i } , m _ { i } ) \right| } } & { \left| X ( k _ { i } + 1 , m _ { i } ) \right| > \left| X ( k _ { i } - 1 , m _ { i } ) \right| } \\ { - \frac { \left| X ( k _ { i } - 1 , m _ { i } ) \right| } { \left| X ( k _ { i } - 1 , m _ { i } ) \right| + \left| X ( k _ { i } , m _ { i } ) \right| } } & { \left| X ( k _ { i } + 1 , m _ { i } ) \right| < \left| X ( k _ { i } - 1 , m _ { i } ) \right| } \\ { 0 } & { \left| X ( k _ { i } + 1 , m _ { i } ) \right| = \left| X ( k _ { i } - 1 , m _ { i } ) \right| } \end{array} \right.\tag{10}
$$

which is calculated by the 1D-FFT results at the interference point and the two adjacent points.

The amplitude $A _ { i }$ and phase $\varphi _ { i }$ of the interference signal can be obtained using

$$
\begin{array} { r } { A _ { i } = \frac { 1 } { N } \bigg | \displaystyle \sum _ { n = 0 } ^ { N - 1 } x ( n , m _ { i } ) e ^ { - j 2 \pi f _ { i } n } \bigg | \phantom { \frac { 1 } { 1 } } } \\ { \varphi _ { i } = A r g \bigg ( \displaystyle \sum _ { n = 0 } ^ { N - 1 } x ( n , m _ { i } ) e ^ { - j 2 \pi f _ { i } n } \bigg ) , } \end{array}\tag{11}
$$

where | | represents the amplitude of the complex number, and $A r g ( )$ represents the phase of the complex number.

According to $f _ { i } , A _ { i } ,$ , and $\varphi _ { i } ,$ the interference signal $x _ { i } ( n , m )$ corresponding to the frequency point in its chirp is reconstructed.

$$
x _ { i } ( n , m ) = A _ { i } e ^ { j ( 2 \pi f _ { i } n + \varphi _ { i } ) } n = 0 , 1 \ldots N - 1\tag{12}
$$

After reconstructing all interference signals, obtain the sum of all interference signals $x _ { I F } ( n , m )$ . The time-domain signals $x ^ { \prime } ( m , n )$ after IM are, respectively,

$$
x _ { I F } ( n , m ) = \sum _ { i = 1 } ^ { C } x _ { i } ( n , m ) ,\tag{13}
$$

$$
x ^ { \prime } ( n , m ) = x ( n , m ) - x _ { I F } ( n , m ) ,\tag{14}
$$

where $m = 0 , 1 \ldots M - 1 , n = 0 , 1 \ldots N - 1 .$

## 4. Numerical Simulations

The numerical simulation results validate the IM performance of the proposed method. Meanwhile, the results are compared with the two commonly used IM methods in CFAR: the zeroing method (ZM) and the amplitude correction method (AC) [16].

## 4.1. Performance Metrics

To facilitate the comparison of different IM methods and quantitatively evaluate the accuracy of each method in recovering the target signal, the signal-to-interference-plusnoise ratio (SINR) and correlation coefficient $\rho$ of the signal relative to the clean reference signal are used as performance metrics. The SINR and $\rho$ are defined as follows [26]:

$$
\mathrm { S I N R } ( s _ { b } , \hat { s } ) = 2 0 \log _ { 1 0 } \frac { \Vert s _ { b } \Vert _ { 2 } } { \Vert \hat { s } - s _ { b } \Vert _ { 2 } } ,\tag{15}
$$

$$
\rho ( s _ { b } , \hat { s } ) = \frac { { { \hat { s } } ^ { H } } { s _ { b } } } { \left\| { s _ { b } } \right\| _ { 2 } \left\| { \hat { s } } \right\| _ { 2 } } ,\tag{16}
$$

where $s _ { b }$ and sˆ denote the vectors of the reference signal and the reconstructed signal after IM, respectively, $\hat { s } ^ { H }$ represents the conjugate transpose of ${ \hat { s } } ,$ and $\Vert \mathbf { \Omega } \Vert _ { 2 }$ is the 2-norm of a vector.

## 4.2. Simulation Experiment

To better describe the interference situation in question, we built a simulation scenario in the Windows 11 system using MATLAB R2018b software. In this simulation scenario, two targets, T1 and ${ \mathrm { T } } 2 ,$ two invasion radars, B1 and B2, and one victim radar A are set. The simulation radar parameters are listed in Table 1, and the simulation target and radar position parameters are listed in Table 2. According to the parameters in Table 1, we can obtain $\mathsf { \Pi } _ { \eta _ { 0 } } ^ { - } = 2 . 9 1 \times 1 0 ^ { - 7 }$ according to (7) and the maximum applicable speed $v _ { \mathrm { m a x } } = c / 2 B M T _ { c } = 4 3 . 6 2 \ : \mathrm { m / s }$ for this method, where $B = S N / f _ { s }$ and c is the speed of light. When the target’s speed is less than $v _ { \mathrm { m a x . } }$ , there will be no change in target frequency in the 1DFFT result. In this simulation scenario, a normal driving vehicle will not cause a change in the target frequency. All parameters in Table 2 are relative to radar $\scriptstyle \mathbf { A } ,$ and the velocity is selected as the positive direction in the direction close to radar A. To better demonstrate the IM ability of the proposed method, the delay and time drift are simulated in one scenario. Radar B1 only has a delay $C _ { o } = 3 0 T _ { c } = 1 . 0 5$ ms and no time drift; radar B2 only has a time drift $\eta = 2 \times 1 0 ^ { - 6 }$ and no delay. Considering the thermal noise and measurement errors of the radar system, complex white Gaussian noise with an SNR of 10 dB is added to the simulation scenario.

Table 1. Simulated radar parameters.
<table><tr><td>Parameter</td><td>A</td><td>B1</td><td>B2</td></tr><tr><td>Starting frequency (f0) (GHz)</td><td>77</td><td>77</td><td>77</td></tr><tr><td>Modulation slope (S) (MHz/µs)</td><td>29.982</td><td>29.982</td><td>29.982</td></tr><tr><td>Duration of one chirp (Tc) (μs)</td><td>35</td><td>35</td><td>35</td></tr><tr><td>Duration of one frame (Tf) (ms)</td><td>50</td><td>50</td><td>50</td></tr><tr><td>Sampling rate (fs) (MHz)</td><td>12.5</td><td>10</td><td>10</td></tr><tr><td>Sampling points (N)</td><td>256</td><td>256</td><td>256</td></tr><tr><td>Number of chirps in one frame (M)</td><td>128</td><td>128</td><td>128</td></tr><tr><td>Number of simulation frames</td><td>1000</td><td>1000</td><td>1000</td></tr></table>

Table 2. Target and radar position parameters in the simulation.
<table><tr><td>Parameter</td><td>T1</td><td>T2</td><td>B1</td><td>B2</td></tr><tr><td>Distance (m)</td><td>40</td><td>22</td><td>6</td><td>15</td></tr><tr><td>Speed (m/s)</td><td>0</td><td>15</td><td>0</td><td>0</td></tr><tr><td>Echo amplitude</td><td>0.8</td><td>1</td><td>2.1</td><td>1.3</td></tr></table>

In the simulation scenario, Figure 7a shows the time-domain signal at the 40th chirp. According to the proposed method, first, 256-point 1D-FFT is performed on the signal in each chirp, that is, the range dimension to obtain 1D-FFT results, as depicted in Figure 7b. From the figure, there is a horizontal straight line at 40.26 m and 22.28 m, which are the stationary and moving targets, respectively; there is a missing straight line at 12.12 m; and there is a straight line with five times of peak position offset near 6.45 m, which are two interference signals. Then, 128-point FFT is performed on the Doppler dimension for 1D-FFT results to obtain 2D-FFT results, as depicted in Figure 7c. From the figure, there are four peaks corresponding to four target signals. From the 2D-FFT result graph, if the distance and velocity parameters of the target are unknown in advance, the target and interference cannot be effectively distinguished. After the 1D-FFT spectrum is detected by

CA-CFAR, the target results required for interference detection can be obtained, as depicted in Figure 7d. The number of reference cells in the CA-CFAR detector is nine; the number of protective cells is five; the false alarm rate is 10<sup>−6</sup>; and the threshold is 40 dB. Then, the target results $B ( m , n ^ { \prime } )$ are summed in the range dimension to obtain the number of targets at each frequency point. According to the threshold $K = 1 2 4$ , the corresponding frequency peaks of all interference signals are obtained. After obtaining the frequency peaks of the interference signal, the reconstruction of the interference signals is completed according to (9)–(12). Then, according to the chirp numbers of the interference signals, the corresponding interference signals are eliminated.

![](images/3a768dc4b3969c0c2f50fe99fc42a44749ef4b99edc46a93d3d9aea371f2bffa.jpg)

![](images/68c4c752bcefb49d38224e4eac25221a3519a87aa7564cb1680e5a8a2225f56e.jpg)

(a)  
![](images/2985b0b53805d2b6c90a19aa9406569862df486dddd40ffb4a5ae61cdf12a398.jpg)  
(c)

(b)  
![](images/c8bd4eda905be9700ab08165be891073473073602777699a43b237d07e92702f.jpg)  
(d)

![](images/9afd3456bca7b6d39bb5ee9964c2cda2993cac100b0d0d1a5722f0b9697a2f14.jpg)  
(e)

![](images/df74369351508904e5c45ef29820da484d57fd095ab539531890953d69d4314f.jpg)  
(f)

![](images/69e0bf795c0dfda0d07c6d369c44accedcfee4fde2d7ca12000780a014f2a84c.jpg)  
(g)

![](images/75449c140c1a58fde3190ac4cf9bdabbaa56fcdfa322996c7a6bf88a0d97a834.jpg)  
(h)  
<sup>igure</sup> <sup>7.</sup> <sup>Simulation</sup> <sup>results.</sup> <sup>(a)</sup> <sup>Time-domain</sup> <sup>diagram</sup> <sup>at</sup> <sup>the</sup> <sup>40th</sup> <sup>chirp</sup> <sup>before</sup> <sup>IM.</sup> <sup>(b)</sup> <sup>The</sup> <sup>1D-FFT</sup> Figure 7. Simulation results. (a) Time-domain diagram at the 40th chirp before IM. (b) The 1D-FFT result before IM. (c) Target result before IM. (d) The 2D-FFT result before IM. (e) Time-domain <sub>D-FFT</sub> <sub>result</sub> <sub>after</sub> <sub>IM.</sub>diagram at the 40th chirp after IM. (f) The 1D-FFT result after IM. (g) Target result after IM. (h) The 2D-FFT result after IM.

Figure 7e shows the time-domain signal at the 40th chirp after IM. The clear signal can be transformed using 1D-FFT, CA-CFAR detector, and 2D-FFT to observe the effect of IM. The 1D-FFT result without interference is shown in Figure 7f; the target result is shown in Figure 7g; and the 2D-FFT result is shown in Figure 7h. In Figure 7f–h, the interferences at 12.12 m and 6.45 m have been suppressed, indicating that the IM effect has been achieved. In Figure 7c,h, it can be seen that the amplitude of the interference signal is reduced by approximately 25 dB.

## 4.3. Effect of SNR on Interference Mitigation

Due to the noise in the collected signal, the target detection effect is affected, which in<sup>ets</sup> <sup>and</sup> <sup>interferences</sup> <sup>as</sup> <sup>in</sup> <sup>Section</sup> <sup>4.2</sup> <sup>and</sup> <sup>change</sup> <sup>the</sup> <sup>noise</sup> <sup>level</sup> <sup>to</sup> <sup>investigate</sup> <sup>the</sup> turn affects the IM effect of the proposed method. In this section, we use the same targets<sup>changes</sup> <sup>in</sup> <sup>the</sup> <sup>IM</sup> <sup>ability</sup> <sup>of</sup> <sup>the</sup> <sup>three</sup> <sup>methods</sup> <sup>at</sup> <sup>different</sup> <sup>SNRs.</sup> and interferences as in Section 4.2 and change the noise level to investigate the changes in<sup>We</sup> <sup>consider</sup> <sup>noise</sup> <sup>levels</sup> <sup>ranging</sup> <sup>from</sup> <sup>−20</sup> <sup>to</sup> <sup>20</sup> <sup>dB</sup> <sup>and</sup> <sup>perform</sup> <sup>1000</sup> <sup>Monte</sup> <sup>Carlo</sup> <sub>the</sub> <sub>IM</sub> <sub>ability</sub> <sub>of</sub> <sub>the</sub> <sub>three</sub> <sub>methods</sub> <sub>at</sub> <sub>different</sub> <sub>SNRs.</sub><sup>runs</sup> <sup>at</sup> <sup>each</sup> <sup>noise</sup> <sup>level.</sup> <sup>The</sup> <sup>performance</sup> <sup>indicators</sup>

<sub>We</sub> <sub>consider</sub> <sub>noise</sub> <sub>levels</sub> <sub>ranging</sub> <sub>from −20</sub> <sub>to</sub> <sub>20</sub> <sub>dB</sub> <sub>and</sub> <sub>perform</sub> <sub>1000</sub> <sub>Monte</sub> <sub>Carlo</sub>igure 8. The bottom and top of each rectangular box in the figure represent the 25th runs at each noise level. The performance indicators of the three IM methods are depicted<sup>and</sup> <sup>75th</sup> <sup>percentiles</sup> <sup>of</sup> <sup>the</sup> <sup>samples,</sup> <sup>respectively,</sup> <sup>and</sup> <sup>the</sup> <sup>lines</sup> <sup>extending</sup> <sup>above</sup> <sup>and</sup> in Figure 8. The bottom and top of each rectangular box in the figure represent the 25th<sup>below</sup> <sup>the</sup> <sup>rectangular</sup> <sup>box</sup> <sup>represent</sup> <sup>the</sup> <sup>range</sup> <sup>between</sup> <sup>the</sup> <sup>maximum</sup> <sup>and</sup> <sup>minimum</sup> and 75th percentiles of the samples, respectively, and the lines extending above and below<sup>values</sup> <sup>of</sup> <sup>the</sup> <sup>samples.</sup> <sup>As</sup> <sup>depicted</sup> <sup>in</sup> <sup>Figure</sup> <sup>8a,</sup> <sup>the</sup> <sup>profile</sup> <sup>of</sup> <sup>the</sup> <sup>TIR</sup> <sup>method</sup> <sup>shows</sup> <sup>an</sup> <sub>the</sub> <sub>rectangular</sub> <sub>box</sub> <sub>represent</sub> <sub>the</sub> <sub>range</sub> <sub>between</sub> <sub>the</sub> <sub>maximum</sub> <sub>and</sub> <sub>minimum</sub> <sub>values</sub> <sub>of</sub> <sub>the</sub>approximately straight line, with the SINR continuously increasing as the SNR increases. samples. As depicted in Figure 8a, the profile of the TIR method shows an approximately<sup>However,</sup> <sup>when</sup> <sup>SNR</sup> <sup>≤</sup> <sup>0</sup> <sup>dB,</sup> <sup>the</sup> <sup>ZM</sup> <sup>and</sup> <sup>AC</sup> <sup>methods</sup> <sup>can</sup> <sup>maintain</sup> <sup>an</sup> <sup>increase</sup> <sup>in</sup> <sup>SINR.</sup> straight line, with the SINR continuously increasing as the SNR increases. However, when<sup>When</sup> <sup>SNR</sup> <sup>></sup> <sup>0</sup> <sup>dB,</sup> <sup>the</sup> <sup>increase</sup> <sup>in</sup> <sup>SINR</sup> <sup>becomes</sup> <sup>slower</sup> <sup>and</sup> <sup>slower</sup> <sup>as</sup> <sup>SNR</sup> <sup>increases.</sup> $\mathrm { S N R } \leq 0 \mathrm { d B } ,$ , the ZM and AC methods can maintain an increase in SINR. When SNR > 0 dB, = 15 dB, the SINR obtained by the TIR method is 10 dB higher than that the increase in SINR becomes slower and slower as SNR increases. Whenobtained by the ZM and AC methods. In the current simulation envi $\mathrm { S N R } = 1 5 \mathrm { d B } ,$ the TIR SINR obtained by the TIR method is 10 dB higher than that obtained by the ZM and ACmethod obtains a better SINR than the ZM and AC methods when SNR > 0 dB. When methods. In the current simulation environment, the TIR method obtains a better SINRSNR ≤ 0 dB, the TIR method also obtains an SINR similar to the two comparison methods. than the ZM and AC methods whenThe target detection effect is better $\mathrm { S N R } > 0 \mathrm { d B }$ . Whenf the Z $\mathrm { S N R } \leq 0 \mathrm { d B } ,$ the TIR method alsoethods at high SNR obtains an SINR similar to the two comparison methods. The target detection effect isdue to the low noise intensity. The ZM method is the simplest method to suppres better than those of the ZM and AC methods at high SNRs due to the low noise intensity.interference; however, although it can suppress interference, it also removes useful The ZM method is the simplest method to suppress interference; however, although itsignals, resulting in the risk of missed alarms. With regard to the AC method, although can suppress interference, it also removes useful signals, resulting in the risk of missedthe adjacent FFT results are used for spectrum recovery, its effect is slightly better than alarms. With regard to the AC method, although the adjacent FFT results are used forthat of the ZM method under high SNR conditions. Finally, using the TIR method, under spectrum recovery, its effect is slightly better than that of the ZM method under high SNRhigh SNR conditions, interference can be accurately detected, and the frequency, conditions. Finally, using the TIR method, under high SNR conditions, interference can be accurately detected, and the frequency, amplitude, and phase of the interference target<sub>interference</sub> <sub>can</sub> <sub>be</sub> <sub>accurately</sub> <sub>removed</sub> <sub>in</sub> <sub>the</sub> <sub>time</sub> <sub>domain,</sub> <sub>and</sub> <sub>useful</sub> <sub>signals</sub> <sub>can</sub> <sub>be</sub> can be accurately estimated so that the interference can be accurately removed in the time<sub>maximally</sub> <sub>preserved.</sub> domain, and useful signals can be maximally preserved.

![](images/4da998fd5745869c7f2611e189b2628f0e670776c676a537d877717e46aa7427.jpg)  
(a)

![](images/f9b133b1dc44c9857555352894935052bee826b0e0f4cd7f64184bb4bed11601.jpg)  
(b)

![](images/87f31fb36d5883464e827e150fbb482133debdaec9ed46c86db5e1482db8f716.jpg)  
(c)  
Figure 8. Quantitative comparison of the interference mitigation performance of the TIR, ZM, and AC methods under different input signal SNR conditions. (a–c) show the variations in SINR, the magnitudes, and phase angles of correlation coefficients of the recovered beat signals after IM, respectively.

Figure 8b shows that when the SNR changes from −20 t to 20 dB, the magnitude of correlation coefficients of the TIR method increases from 0.1 to 1, while with the ZM and AC methods it can only increase from 0.1 to 0.7 and 0.8, respectively, and is almost stable under high SNR conditions. We can conclude that at high SNRs, the amplitude of the signal correlation coefficient obtained by the TIR method is higher than those of the other two methods, and is almost the same as the other two methods at low SNRs. Figure 8c shows that as the input SNR increases, the phase of the correlation coefficient of the three methods gradually tends to zero. Therefore, in terms of the evaluation indicators, the proposed method is superior to the other two methods.5. Experimental Results

## 5. Experimental Results

This section presents experimental results to verify the performance of the proposed method. Two experimental scenarios were set up: one was a direct interference experiment to verify the correctness of the simulation results, and the other was a reflection interference experiment to verify the authenticity of the proposed research background. In the experimental part, two Texas Instruments IWR1843 radar boards were used as the victim radar A and attacker radar B. Radar data were collected using the DCA1000EVM data collection board. The radar board burning software was UniFlash6.1.0, and the radar board configuration software was mmWave Studio 02.01.00.00.

## 5.1. Direct Interference Experiment<sup>5.1.</sup> <sup>Direct</sup> <sup>Interferen</sup>

The experimental scenario is depicted in Figure 9. The parameter settings of the two radar boards are the same, as listed in Table 3. The position parameters between the two<sup>radar</sup> <sup>boards</sup> <sup>are</sup> <sup>the</sup> <sup>same,</sup> <sup>as</sup> <sup>listed</sup> <sup>in</sup> <sup>Table</sup> <sup>3.</sup> <sup>The</sup> <sup>position</sup> <sup>parameters</sup> <sup>bet</sup> radar boards and the corner reflector are listed in Table 4. The horizontal angle in Table 4<sup>radar</sup> <sup>boards</sup> <sup>and</sup> <sup>the</sup> <sup>corner</sup> <sup>reflector</sup> <sup>are</sup> <sup>listed</sup> <sup>in</sup> <sup>Table</sup> <sup>4.</sup> <sup>The</sup> <sup>horizontal</sup> <sup>ang</sup> is measured clockwise based on the connecting line between the victim radar and the<sup>is</sup> <sup>measured</sup> <sup>clockwise</sup> <sup>based</sup> <sup>on</sup> <sup>the</sup> <sup>connecting</sup> <sup>line</sup> <sup>between</sup> <sup>the</sup> <sup>victim</sup> <sup>r</sup> stationary target, while the elevation angle is measured clockwise based on the horizontal<sup>stationary</sup> <sup>target,</sup> <sup>while</sup> <sup>the</sup> <sup>elevation</sup> <sup>angle</sup> <sup>is</sup> <sup>measured</sup> <sup>clockwise</sup> <sup>ba</sup> direction of the victim radar, and downward is positive. For the parameter settings of radar<sup>horizontal</sup> <sup>direction</sup> <sup>of</sup> <sup>the</sup> <sup>victim</sup> <sup>radar,</sup> <sup>and</sup> <sup>downward</sup> <sup>is</sup> <sup>positive.</sup> <sup>For</sup> <sup>th</sup> A, we can obtain<sup>sett</sup> $\eta _ { 0 } = 2 . 9 1 \times 1 0 ^ { - 7 }$ according to (7).<sup>e</sup> <sup>can</sup> <sup>obtain</sup> 0

![](images/bca7c09efd1ff67938fe3f66e0bbbfaeee5f421ec2b0b8e7c933328bb0545372.jpg)

![](images/d55a10976bfb43660a3b3a45fbd06c530aef3d275eacd00f3a593ff0f9dc23bb.jpg)  
<sup>Figure</sup> <sup>9.</sup> <sup>Direct</sup> <sup>interference</sup> <sup>experimental</sup> <sup>scenario:</sup> <sup>(a)</sup> <sup>schematic</sup> <sup>and</sup> <sup>(b)</sup> <sup>phy</sup>Figure 9. Direct interference experimental scenario: (a) schematic and (b) physical diagram.

Table 3. IWR1843 Radar board setting parameters in the direct interferenTable 3. IWR1843 Radar board setting parameters in the direct interference experiment.
<table><tr><td>Parameter</td><td>A</td><td>B</td></tr><tr><td>Starting frequency (f0) (GHz)</td><td>77</td><td>77</td></tr><tr><td>Modulation slope (S) (MHz/μs)</td><td>29.982</td><td>29.982</td></tr><tr><td>Duration of one chirp (Tc) (μs)</td><td>35</td><td>35</td></tr><tr><td>Duration of one frame (Tf) (ms)</td><td>50</td><td>50</td></tr><tr><td>Sampling rate (fs) (MHz)</td><td>10</td><td>10</td></tr><tr><td>Sampling points (N)</td><td>256</td><td>256</td></tr><tr><td>Number of chirps in one frame (M)</td><td>128</td><td>128</td></tr><tr><td>Number of frames</td><td>1000</td><td>1000</td></tr></table>

Table 4. IWR1843 Radar board positional parameters in the direct interference experiment.
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Distance between two radars (m)</td><td>2.3</td></tr><tr><td>Linear distance from radars to target (m)</td><td>5.0</td></tr><tr><td>Distance from radars to ground (m)</td><td>1.7</td></tr><tr><td>Azimuth between the victim radar and stationary target (°)</td><td>0</td></tr><tr><td>Azimuth between the victim radar and aggressor radar (°)</td><td>20</td></tr><tr><td>Elevation angle between the victim radar and stationary target (°)</td><td>13.5</td></tr><tr><td>Elevation angle between the victim radar and aggressor radar (°)</td><td>0</td></tr></table>

According to the proposed method, the first step is to extract the signal collected by radar A. The signal collected by radar A is transformed from the time domain to the frequency domain through 1D-FFT, and the frequency spectrum is shown in Figure 10a. The figure shows interference as a diagonal line near 9.77 m and a stationary target as a straight line near 3.32 m. After CFAR detection and threshold selection (threshold $G = 9 5 \mathrm { d B } )$ , the target detection result is illustrated in Figure 10b. The 2D-FFT result of the signal is shown in Figure 10c, showing a large amplitude environment noise floor elevation next to the sta-<sup>Elevation</sup> <sup>angle</sup> <sup>between</sup> <sup>the</sup> <sup>victim</sup> <sup>radar</sup> <sup>and</sup> <sup>aggressor</sup> <sup>radar</sup> <sup>(°)</sup> <sup>0</sup> tionary target. The peak value at the range of 0 m and speed of $0 \mathrm { m } / \mathrm { s }$ in the figure is the interference of the radar board itself, which can be ignored in the set scenario. In Figure 10b, it<sup>According</sup> <sup>to</sup> <sup>the</sup> <sup>proposed</sup> <sup>method,</sup> <sup>the</sup> <sup>first</sup> <sup>step</sup> <sup>is</sup> <sup>to</sup> <sup>extract</sup> <sup>the</sup> <sup>signal</sup> <sup>collected</sup> <sup>by</sup> can be seen that the interference lasts from the 1st chirp to the 55th chirp, and the frequency<sup>radar</sup> <sup>A.</sup> <sup>The</sup> <sup>signal</sup> <sup>collected</sup> <sup>by</sup> <sup>radar</sup> <sup>A</sup> <sup>is</sup> <sup>transformed</sup> <sup>from</sup> <sup>the</sup> <sup>time</sup> <sup>domain</sup> <sup>to</sup> <sup>the</sup> <sub>point</sub> <sub>changes</sub> <sub>from</sub> <sub>the</sub> <sub>44th</sub> <sub>to</sub> <sub>the</sub> <sub>56th.</sub> <sub>The</sub> <sub>time</sub> <sub>drift</sub>frequency domain through 1D-FFT, and the frequency sp $\eta _ { 1 } = f _ { s } / m _ { 1 } \bar { N } T _ { c } S = 7 . 1 1 \bar { \times } 1 0 ^ { - 6 }$ can be obtained in this scenario, where<sup>The</sup> <sup>figure</sup> <sup>shows</sup> <sup>interference</sup> <sup>as</sup> <sup>a</sup> <sup>dia</sup> $m _ { 0 } = ( 5 5 - 1 + 1 ) / ( 5 6 - 4 4 ) = 4 . 5 8$ represents the<sup>ry</sup> <sup>target</sup> <sup>as</sup> <sup>a</sup> number of chirps required for the target frequency to appear offset. Then, the target result<sup>straight</sup> <sup>line</sup> <sup>near</sup> <sup>3.32</sup> <sup>m.</sup> <sup>After</sup> <sup>CFAR</sup> <sup>detection</sup> <sup>and</sup> <sup>threshold</sup> <sup>selection</sup> <sup>(threshold</sup> <sub>is</sub> <sub>summed</sub> <sub>up</sub> <sub>in</sub> <sub>the</sub> <sub>range</sub> <sub>dimension</sub> <sub>to</sub> <sub>obtain</sub> <sub>the</sub> <sub>number</sub> <sub>of</sub> <sub>targets</sub> <sub>at</sub> <sub>each</sub> <sub>frequency</sub>G = 95 dB ), the target detection result is illustrated in Figure 10b. The 2D-FFT result of point. The frequency points corresponding to all interference signals are found based on<sup>the</sup> <sup>signal</sup> <sup>is</sup> <sup>shown</sup> <sup>in</sup> <sup>Figure</sup> <sup>10c,</sup> <sup>showing</sup> <sup>a</sup> <sup>large</sup> <sup>amplitude</sup> <sup>environment</sup> <sup>noise</sup> <sup>floor</sup> <sub>the</sub> <sub>threshold</sub>elevation next $K = 1 2 4$ . After obtaining the frequency points of the interference signal,<sup>tionary</sup> <sup>target.</sup> <sup>The</sup> <sup>peak</sup> <sup>value</sup> <sup>at</sup> <sup>the</sup> <sup>range</sup> <sup>of</sup> <sup>0</sup> <sup>m</sup> <sup>and</sup> <sup>speed</sup> <sup>of</sup> <sup>0</sup> the reconstruction of the interference signal is completed according to (9)–(12). Then, the<sup>m/s</sup> <sup>in</sup> <sup>the</sup> <sup>figure</sup> <sup>is</sup> <sup>the</sup> <sup>interference</sup> <sup>of</sup> <sup>the</sup> <sup>radar</sup> <sup>board</sup> <sup>itself,</sup> <sup>which</sup> <sup>can</sup> <sup>be</sup> <sup>ignored</sup> <sup>in</sup> <sup>the</sup> interference is removed separately according to the chirps where it is located.<sup>set</sup> <sup>scenario.</sup> <sup>In</sup> <sup>Figure</sup> <sup>10b,</sup> <sup>it</sup> <sup>can</sup> <sup>be</sup> <sup>seen</sup> <sup>that</sup> <sup>the</sup> <sup>interference</sup> <sup>lasts</sup> <sup>from</sup> <sup>the</sup>

At this time, the 1D-FFT and target results are re-obtained, as depicted in Figure 10d,e.5th chirp, and the frequency point changes from the 44th to the 56th. The time drift In the figures, the interference signal at 9.77 m is suppressed, and the stationary target<sup>6</sup>/ 7.11 10  f m NT S <sup>−</sup> = = × m = − + (55 1 1) / at 3.32 m is preserved. The 2D-FFT results are shown in Figure 10f, where there is no significant change in the peak value of the stationary target, and the interference only<sup>represents</sup> <sup>the</sup> <sup>number</sup> <sup>of</sup> <sup>chirps</sup> <sup>required</sup> <sup>for</sup> <sup>the</sup> <sup>target</sup> <sup>frequency</sup> <sup>to</sup> leaves a portion of the signal that can be considered noise.<sup>appear</sup> <sup>offset.</sup> <sup>Then,</sup> <sup>the</sup> <sup>target</sup> <sup>result</sup> <sup>is</sup> <sup>summed</sup> <sup>up</sup> <sup>in</sup> <sup>the</sup>

The direct interference experiment verifies the rationality of the simulation experiment<sup>ber</sup> <sup>of</sup> <sup>targets</sup> <sup>at</sup> <sup>each</sup> <sup>frequency</sup> <sup>point.</sup> <sup>The</sup> <sup>frequency</sup> <sup>points</sup> <sup>corresponding</sup> <sup>to</sup> <sup>all</sup> and also proves the effectiveness of the proposed algorithm in detecting and suppressing<sup>interference</sup> <sup>signals</sup> <sup>are</sup> <sup>found</sup> <sup>based</sup> <sup>on</sup> <sup>the</sup> <sup>threshold</sup> <sup>K</sup> <sup>=</sup> <sup>124</sup> <sup>.</sup> <sup>After</sup> <sup>obtaining</sup> <sup>the</sup> <sub>interference.</sub> <sub>From</sub> <sub>Figure</sub> <sub>9c,f</sub> <sub>it</sub> <sub>can</sub> <sub>be</sub> <sub>seen</sub> <sub>that</sub> <sub>the</sub> <sub>amplitude</sub> <sub>of</sub> <sub>the</sub> <sub>interference</sub> <sub>signal</sub>frequency points of the interference signal, the reconstruction of the interference signal is <sub>is</sub> <sub>reduced</sub> <sub>by</sub> <sub>approximately</sub> <sub>20</sub> <sub>dB,</sub> <sub>which</sub> <sub>provides</sub> <sub>a</sub> <sub>good</sub> <sub>foundation</sub> <sub>for</sub> <sub>subsequent</sub>completed according to (9)–(12). Then, the interference is removed separately according data processing.<sup>to</sup> <sup>the</sup> <sup>chirps</sup> <sup>wh</sup>

![](images/99d708a810f562954f85bf0bb0898adfbf8022b29301eb63a00f7cc60eebf170.jpg)  
Figure 10. Cont.  
(a)

![](images/b6930dc5e354b6a51150eb3b2532d23311f4391dc06f20cbb9a8572bbe1565eb.jpg)  
(b)

![](images/967075e7ee3fbfcd72a389188aa1bf62011da6ce4f0128833ce710ced69da911.jpg)  
(c)

![](images/fe8addaf4bbdf9348d00da4f3bac9c49e94eb66e5b32503cb73e773329f299ee.jpg)  
(d)  
2DFFT Result by using TIR in Direct Interference Experimen

![](images/38d21e6bb0e85c08bc74779ef71f530bbae1ad12a1fec40a42eebaa3b6793cc4.jpg)  
(e)

![](images/8b3b726975ad7d5ee22d5eaf095686d2bc490938999805a04c8de5eab9c97d10.jpg)  
(f)  
Figure 10. <sup>Direct</sup> <sup>interference</sup> <sup>experimental</sup> <sup>results:</sup> <sup>(</sup>a<sup>–</sup>c<sup>)</sup> <sup>represent</sup> <sup>the</sup> <sup>1D-FFT,</sup> <sup>2D-FFT,</sup> <sup>and</sup> <sup>target</sup> <sub>Figure</sub> <sub>10.</sub> <sub>Direct</sub> <sub>interference</sub> <sub>experimental</sub> <sub>results:</sub> <sub>(a–c)</sub> <sub>represent</sub> <sub>the</sub> <sub>1D-FFT,</sub> <sub>2D-FFT,</sub> <sub>and</sub> <sub>tar-</sub>interference signal is reduced by approximately 20 dB, which provides get results before IM, respectively; (d–f) represent the 1D-FFT, 2D-FFT, and target results after<sup>foundation</sup> <sup>for</sup> <sup>subsequent</sup> <sup>data</sup> <sup>processing.</sup> IM, respectively.

## At this time, the 1D-FFT and t5.2. Reflection Interference Experiment

. In the figures, the interference signal at 9.77 m is suppressed, and the stationary <sub>The</sub> <sub>experimental</sub> <sub>results</sub> <sub>presented</sub> <sub>in</sub> <sub>this</sub> <sub>section</sub> <sub>verify</sub> <sub>the</sub> <sub>performance</sub> <sub>of</sub> <sub>the</sub> <sup>target</sup> <sup>at</sup> <sup>3.32</sup> <sup>m</sup> <sup>is</sup> <sup>preserved.</sup> <sup>The</sup> <sup>2D-FFT</sup> <sup>results</sup> <sup>are</sup> <sup>shown</sup> <sup>in</sup> <sup>Figure</sup> <sup>10f,</sup> <sup>where</sup> <sup>there</sup> <sup>is</sup> proposed method in a real environment. The experimental scenario is shown in Figure 11. <sup>no</sup> <sup>significant</sup> <sup>change</sup> <sup>in</sup> <sup>the</sup> <sup>peak</sup> <sup>value</sup> <sup>of</sup> <sup>the</sup> <sup>stationary</sup> <sup>target,</sup> <sup>and</sup> <sup>the</sup> <sup>interference</sup> <sup>only</sup> A stationary car is parked in front of the radar boards. This creates a simple road experiment <sup>leaves</sup> <sup>a</sup> <sup>portion</sup> <sup>of</sup> <sup>the</sup> <sup>signal</sup> <sup>that</sup> <sup>can</sup> <sup>be</sup> <sup>considered</sup> <sup>noise.</sup>scenario. The parameter settings of the two radar boards are the same as listed in Table 5. <sup>The</sup> <sup>direct</sup> <sup>interference</sup> <sup>experiment</sup> <sup>verifies</sup> <sup>the</sup> <sup>rationality</sup> <sup>of</sup> <sup>the</sup> <sup>simulation</sup> The position parameters between the two radar boards and the vehicle are listed in Table 6. <sup>experiment</sup> <sup>and</sup> <sup>also</sup> <sup>proves</sup> <sup>the</sup> <sup>effectiveness</sup> <sup>of</sup> <sup>the</sup> <sup>proposed</sup> <sup>algorithm</sup> <sup>in</sup> <sup>detecting</sup> <sup>and</sup> The horizontal angle in Table 6 is measured clockwise based on the connecting line between <sup>suppressing</sup> <sup>interference.</sup> <sup>From</sup> <sup>Figure</sup> <sup>9c,f</sup> <sup>it</sup> <sup>can</sup> <sup>be</sup> <sup>seen</sup> <sup>that</sup> <sup>the</sup> <sup>amplitude</sup> <sup>of</sup> <sup>the</sup> the victim radar and the stationary target, while the elevation angle is measured clockwise <sup>interference</sup> <sup>signal</sup> <sup>is</sup> <sup>reduced</sup> <sup>by</sup> <sup>approximately</sup> <sup>20</sup> <sup>dB,</sup> <sup>which</sup> <sup>provides</sup> <sup>a</sup> <sup>good</sup> based on the horizontal direction of the victim radar, and downward is positive. For the<sub>−</sub> foundation for subsequent <sub>parameter</sub> <sub>settings</sub> <sub>of</sub> <sub>radar</sub>is po itive. For the $\mathrm { A } , \eta _ { 0 } = 2 . 9 1 \times 1 0 ^ { - 7 }$ according to (7).<sup>f</sup> <sup>radar</sup> <sup>A,</sup> <sup>0</sup>

![](images/e6d9879cf8fb3f856c54e2078dcae5346b826cbdccc4370da3a527ff6b926d7e.jpg)  
(a)

![](images/04b8535156cfff75d17fd38eb254c815cc7c86e15c0260b1aacc0f070607e264.jpg)  
(b)  
Figure 11. Reflection interference experimental scenario: (<sup>Figure</sup> <sup>11.</sup> <sup>Reflection</sup> <sup>interference</sup> <sup>experimental</sup>a <sup>scenario:</sup> <sup>(a)</sup> <sup>schematic</sup> <sup>and</sup> <sup>(b)</sup> <sup>physic</sup>) schematic and (b) physical diagram.

Table 5. IWR1843 Radar board setting parameters in the reflection interference experiment.
<table><tr><td>Parameter</td><td>A</td><td>B</td></tr><tr><td>Starting frequency (f0) (GHz)</td><td>77</td><td>77</td></tr><tr><td>Modulation slope (S) (MHz/µs)</td><td>29.982</td><td>29.982</td></tr><tr><td>Duration of one chirp (Tc) (μs)</td><td>35</td><td>35</td></tr><tr><td>Duration of one frame (Tf) (ms)</td><td>50</td><td>50</td></tr><tr><td>Sampling rate (fs) (MHz)</td><td>10</td><td>10</td></tr><tr><td>Sampling points (N)</td><td>256</td><td>256</td></tr><tr><td>Number of chirps in one frame (M)</td><td>128</td><td>128</td></tr><tr><td>Number of frames</td><td>1000</td><td>1000</td></tr></table>

Table 6. IWR1843 Radar board positional parameters in the reflection interference experiment.
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Distance between two radars (m)</td><td>1.4</td></tr><tr><td>Linear distance from radars to vehicle (m)</td><td>1.8</td></tr><tr><td>Distance from radar to ground (m)</td><td>1.0</td></tr><tr><td>Azimuth between the victim radar and stationary target (°)</td><td>0</td></tr><tr><td>Azimuth between the victim radar and aggressor radar (°)</td><td>90</td></tr><tr><td>Elevation angle between the victim radar and stationary target (°)</td><td>0</td></tr><tr><td>Elevation angle between the victim radar and aggressor radar (°)</td><td>0</td></tr></table>

According to the proposed method, the first step is to extract the signal collected by radar A. The signal collected by radar A is transformed from the time domain to the frequency domain through 1D-FFT, and the frequency spectrum is shown in Figure 12a. The figure shows interference as a diagonal line near 5.08 m and a stationary target as a<sup>straight</sup> <sup>line</sup> <sup>at</sup> <sup>1.95</sup> <sup>m.</sup> <sup>After</sup> <sup>CFAR</sup> <sup>detection</sup> <sup>and</sup> <sup>threshold</sup> <sup>selection</sup> <sup>(threshold</sup> straight line at 1.95 m. After CFAR detection and threshold selection (threshold<sup>G</sup> <sup>=</sup> <sup>50</sup> <sup>dB ),</sup> <sup>the</sup> <sup>target</sup> <sup>detection</sup> <sup>result</sup> <sup>is</sup> <sup>illustrated</sup> <sup>in</sup> <sup>Figure</sup> <sup>12b.</sup> <sup>The</sup> <sup>2D-F</sup> $G = 5 0 \mathrm { d B } )$ the target detection result is illustrated in Figure 12b. The 2D-FFT result of the signal<sup>the</sup> <sup>signal</sup> <sup>is</sup> <sup>shown</sup> <sup>in</sup> <sup>Figure</sup> <sup>12c,</sup> <sup>showing</sup> <sup>a</sup> <sup>large</sup> <sup>amplitude</sup> <sup>environment</sup> <sup>noise</sup> <sup>floor</sup> <sub>is</sub> <sub>shown</sub> <sub>in</sub> <sub>Figure</sub> <sub>12c,</sub> <sub>showing</sub> <sub>a</sub> <sub>large</sub> <sub>amplitude</sub> <sub>environment</sub> <sub>noise</sub> <sub>floor</sub> <sub>elevation</sub>elevation next to the stationary target. In Figure 12b, it can be seen that the interference next to the stationary target. In Figure 12b, it can be seen that the interference lasts from<sup>lasts</sup> <sup>from</sup> <sup>the</sup> <sup>1st</sup> <sup>chirp</sup> <sup>to</sup> <sup>the</sup> <sup>74th</sup> <sup>chirp</sup> <sup>and</sup> <sup>the</sup> <sup>frequency</sup> <sup>point</sup> <sup>changes</sup> <sup>from</sup> <sup>the</sup> <sup>23rd</sup> <sup>to</sup> the 1st chirp to the 74th chirp and the frequency point changes from the 23rd to the<sub>the</sub> <sub>35th.</sub> <sub>The</sub> <sub>time</sub> <sub>drift</sub> 2 2<sup>/</sup> <sup>6.04</sup> <sup>10</sup> s c <sup>f</sup> <sup>m</sup> <sup>NT</sup> <sup>S</sup>  <sup>=</sup> <sup>=</sup> <sup>×</sup> <sub>can</sub> <sub>be</sub> <sub>obtained</sub> <sub>in</sub> <sub>this</sub> <sub>scenario,</sub> 35th. The time drift<sub>= − +</sub> $\eta _ { 2 } = f _ { s } / m _ { 2 } N T _ { c } S = 6 . 0 4 \times 1 0 ^ { - 6 }$ can be obtained in this scenario, where $m _ { 2 } = ( 7 4 - 1 + 1 ) / ( 3 5 - 2 3 ) = 6 . 1 7 .$ . Then, the target result is summed up in the range dimension to obtain the number of targets at each frequency point. The frequency points corresponding to all interference signals are found based on the threshold $K = 1 2 4$ After obtaining the frequency points of the interference signal, the reconstruction of the<sup>obtaining</sup> <sup>the</sup> <sup>frequency</sup> <sup>points</sup> <sup>of</sup> <sup>the</sup> <sup>interference</sup> <sup>signal,</sup> <sup>the</sup> <sup>reconstruction</sup> <sup>of</sup> <sup>the</sup> interference signal is completed according to (9)–(12). Then, the interference is mitigated according to the chirps where it is located.

![](images/030169c11e19ea55f6e9316cac377e9e7da7c9870c4f4493353cb17bf7f7dd0d.jpg)  
Figure 12. Cont.  
(a)

![](images/96aa6af7090a9b6b35cb98ea12f51ba3f2fdd265e6b0d6b04d5ceeb0fb63871e.jpg)  
(b)

![](images/94ef477b05a0f06a2afe2c1fd18c4c8fb853088fb4c3cf29b83971551f6e4de3.jpg)  
(c)

![](images/63426110e797d316f7f3e75c1a3d5d4ceeb42e114c40ec7e2a9f4468b74f2ffd.jpg)  
(d)  
2DFFT Result by using TIR in Reflection Interference Experiment

![](images/d1b5dd5315eeba4c87822a681c77f9ae8a51dbea00a8c601573db218a9aa2919.jpg)  
(e)

![](images/939afc3bc55634d7578932af281f0617c11442471b13ada848350d6ab124a756.jpg)  
(f)  
<sup>Figure</sup> <sup>12.</sup> <sup>Reflection</sup> <sup>interference</sup> <sup>experimental</sup> <sup>results:</sup> <sup>(a–c)</sup> <sup>represent</sup> <sup>the</sup> <sup>1D-FFT,</sup> <sup>2D-FFT,</sup> <sup>and</sup> <sub>Figure</sub> <sub>12.</sub> <sub>Reflection</sub> <sub>interference</sub> <sub>experimental</sub> <sub>results:</sub> <sub>(a–c)</sub> <sub>represent</sub> <sub>the</sub> <sub>1D-FFT,</sub> <sub>2D-FFT,</sub> <sub>and</sub> target results before IM, respectively; (d–f) represent the 1D-FFT, 2D-FFT, and target results after IM, respectively.

At this time, the 1D-FFT and target results are re-obtained, as depicted in Figure $^ { 1 2 \mathrm { d } , \mathrm { e } }$ In the figures, the interference signal at 5.08 m is suppressed, and the stationary target at 1.95 m is preserved. The 2D-FFT result is shown in Figure 12f, where the peak value of the <sup>value</sup> <sup>of</sup> <sup>the</sup> <sup>stationary</sup> <sup>target</sup> <sup>does</sup> <sup>not</sup> <sup>change</sup> <sup>considerably.</sup> <sup>Although</sup> <sup>a</sup> <sup>portion</sup> <sup>of</sup> <sup>the</sup> stationary target does not change considerably. Although a portion of the signal remains <sup>signal</sup> <sup>remains</sup> <sup>after</sup> <sup>suppressing</sup> <sup>interference,</sup> <sup>it</sup> <sup>is</sup> <sup>sufficient</sup> <sup>to</sup> <sup>be</sup> <sup>considered</sup> <sup>noise</sup> <sup>and</sup> after suppressing interference, it is sufficient to be considered noise and will not affect the <sup>will</sup> <sup>not</sup> <sup>affec</sup>target signal.

<sup>The</sup> <sup>reflection</sup> <sup>interference</sup> <sup>experiment</sup> <sup>proves</sup> <sup>the</sup> <sup>existence</sup> <sup>of</sup> <sup>the</sup> <sup>proposed</sup> The reflection interference experiment proves the existence of the proposed interfer-<sup>interference</sup> <sup>scenario</sup> <sup>in</sup> <sup>real</sup> <sup>life.</sup> <sup>From</sup> <sup>Figure</sup> <sup>12c,f,</sup> <sup>it</sup> <sup>can</sup> <sup>be</sup> <sup>seen</sup> <sup>that</sup> <sup>the</sup> <sup>proposed</sup> ence scenario in real life. From Figure 12c,f, it can be seen that the proposed method can <sup>method</sup> <sup>can</sup> <sup>reduce</sup> <sup>the</sup> <sup>amplitude</sup> <sup>of</sup> <sup>the</sup> <sup>interference</sup> <sup>signal</sup> <sup>by</sup> <sup>about</sup> <sup>25</sup> reduce the amplitude of the interference signal by about 25 dB in this scenario.

## 6. Conclusions and Outlook

## 6. Conclusions 6.1. Conclusions

onclusionsThis study proposes a method for interference detection and mitigation based on 1D-FFT results for FMCW radar systems. The proposed method uses the difference in 1D-FFT results between targets and interferences. Then, by reconstructing the interference signal in the time domain using the information about the interference from the 1D-FFT results, the interference signal can be removed from the time domain without affecting the target signal. In the simulation and experimental results, the detection and mitigation of interference targets showed good results. No interferences were observed in the 2D-FFT results of both after IM. Subsequently, this method was compared with the ZM and AC methods. Under high SNR conditions, the SINR of the TIR method increases linearly with the increase in the SNR, while the increased speed of the ZM and AC methods is significantly slower than that of the TIR method. When SNR = 15 dB, the SINR obtained by the TIR method is 10 dB higher than that obtained by the ZM and AC methods The magnitude of the correlation coefficient of the TIR method can approach 1, while with the ZM and AC methods it can only stabilize at 0.7 and 0.8, respectively. In simulation scenarios, this method can achieve an interference suppression effect of 25 dB. In direct interference experiments, this method can achieve a 20 dB interference suppression effect, and in reflection interference experiments, this method can achieve a 25 dB interference suppression effect.

## 6.2. Outlook

The methods outlined in this article still have some problems that can be further studied. In the simulation and experiments presented in this article, a maximum of two targets and two interferences are considered. In further work, we will add more interferences and different types of targets in the simulation, and add more experimental scenarios in the experiment, constantly approaching the actual road situation. We only conducted numerical analysis on the performance indicators SINR and ρ mentioned in the paper, and we will investigate the performance indicators theoretically in the future. Moreover, we will discuss more performance indicators, such as the gain in saving computational resources, implementation costs, processing delay, computational complexity, and detection accuracy.

Author Contributions: Conceptualization and methodology, Z.X.; validation and writing—original draft preparation, S.W.; writing—review and editing, Z.X. and S.W. All authors have read and agreed to the published version of the manuscript.

Funding: This research received no external funding.

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: Data are available upon request.

Conflicts of Interest: The authors declare no conflict of interest.

## Abbreviations

The following abbreviations are used in this manuscript: The following abbreviations are used in this manuscript:

1D-FFT one-dimensional fast Fourier transform   
FMCW frequency-modulated continuous-wave   
ADAS advanced driver assistance systems   
IF intermediate frequency   
2D-FFT two-dimensional fast Fourier transform   
MOSARIM More Safety for All by Radar Interference Mitigation   
IM interference mitigation   
LMS least mean squares   
SVD singular value decomposition   
AR auto-regressive   
CFAR constant false alarm rate   
ID interference detection   
BW bandwidth   
CA-CFAR cell-averaging constant false alarm rate   
TIR time-domain interference reconstruction   
ZM zeroing method   
AC amplitude correction method   
SINR signal-to-interference-plus-noise ratio   
SNR signal-to-noise ratio

## References

1. Brooker, G.M. Mutual Interference of Millimeter-Wave Radar Systems. IEEE Trans. Electromagn. Compat. 2007, 49, 170–181. [CrossRef]

2. Goppelt, M.; Blöcher, H.-L.; Menzel, W. Automotive radar—Investigation of mutual interference mechanisms. Adv. Radio Sci. 2010, 8, 55–60. [CrossRef]

3. Schipper, T.; Harter, M.; Mahler, T.; Kern, O.; Zwick, T. Discussion of the operating range of frequency modulated radars in the presence of interference. Int. J. Microw. Wirel. Technol. 2014, 6, 371–378. [CrossRef]

4. Kumbul, U.; Chen, Y.; Petrov, N.; Vaucher, C.S.; Yarovoy, A. Impacts of Mutual Interference Analysis in FMCW Automotive Radar. In Proceedings of the 17th European Conference on Antennas and Propagation (EuCAP), Florence, Italy, 26–31 March 2023; pp. 1–5.

5. Goppelt, M.; Blöcher, H.-L.; Menzel, W. Analytical investigation of mutual interference between automotive FMCW radar sensors. In Proceedings of the 2011 German Microwave Conference, Darmstadt, Germany, 14–16 March 2011; pp. 1–4.

6. Kunert, M. The EU project MOSARIM: A general overview of project objectives and conducted work. In Proceedings of the 9th EuRAD European Radar Conference, Amsterdam, The Netherlands, 31 October–2 November 2012; pp. 1–5.

7. Nozawa, T.; Makino, Y.; Takaya, N.; Umehira, M.; Takeda, S.; Wang, X.; Kuroda, H. An anti-collision automotive FMCW radar using time-domain interference detection and suppression. In Proceedings of the International Conference on Radar Systems (Radar 2017), Belfast, UK, 23–26 October 2017; pp. 1–5.

8. Umehira, M.; Nozawa, T.; Makino, Y.; Wang, X.; Takeda, S.; Kuroda, H. A Novel Iterative Inter-Radar Interference Reduction Scheme for Densely Deployed Automotive FMCW Radars. In Proceedings of the 19th International Radar Symposium (IRS), Bonn, Germany, 20–22 June 2018; pp. 1–10.

9. Harris, F.; Trager, D.; Davis, C.; Rao, R.K. Adaptive Filtering for FMCW Interference Mitigation in PMCW Radar Systems. U.S. Patent 9989638B2, 27 September 2018.

10. Uysal, F.; Sanka, S. Mitigation of automotive radar interference. In Proceedings of the IEEE Radar Conference (RadarConf18), Oklahoma City, OK, USA, 23–27 April 2018; pp. 405–410.

11. Li, Y.; Wang, C.; Li, F.; Han, X.; Song, Y. An adaptive interference cancellation method for automotive FMCW radar based on waveform optimization. In Proceedings of the IET International Radar Conference (IET IRC 2020), Online, 4–6 November 2020; pp. 666–670.

12. Jin, F.; Cao, S. Automotive Radar Interference Mitigation Using Adaptive Noise Canceller. IEEE Trans. Veh. Technol. 2019, 68, 3747–3754. [CrossRef]

13. Lee, S.; Lee, J.-Y.; Kim, S.-C. Mutual Interference Suppression Using Wavelet Denoising in Automotive FMCW Radar Systems. IEEE Trans. Intell. Transp. Syst. 2021, 22, 887–897. [CrossRef]

14. Baral, A.B.; Upadhyay, B.R.; Torlak, M. Automotive Radar Interference Mitigation Using Two-Stage Signal Decomposition Approach. In Proceedings of the IEEE Radar Conference (RadarConf23), San Antonio, TX, USA, 1–5 May 2023; pp. 1–6.

15. Neemat, S.; Krasnov, O.; Yarovoy, A. An Interference Mitigation Technique for FMCW Radar Using Beat-Frequencies Interpolation in the STFT Domain. IEEE Trans. Microw. Theory Tech. 2019, 67, 1207–1220. [CrossRef]

16. Wang, J. CFAR-Based Interference Mitigation for FMCW Automotive Radar Systems. IEEE Trans. Intell. Transp. Syst. 2022, 23, 12229–12238. [CrossRef]

17. Xu, Z.; Shi, Q.; Wang, H.; Wei, M.; Gao, R.; Shao, Y.; Tao, H. A novel method of mitigating the mutual interference between multiple LFMCW radars for automotive applications. In Proceedings of the IEEE International Geoscience and Remote Sensing Symposium, Yokohama, Japan, 28 July–2 August 2019; pp. 2178–2181.

18. Uysal, F. Phase-Coded FMCW Automotive Radar: System Design and Interference Mitigation. IEEE Trans. Veh. Technol. 2020, 69, 270–281. [CrossRef]

19. Kim, E.H.; Kim, K.H. Random phase code for automotive MIMO radars using combined frequency shift keying-linear FMCW waveform. IET Radar. Sonar Navig. 2018, 12, 1090–1095. [CrossRef]

20. Liu, P.; Liu, Y.; Huang, T.; Lu, Y.; Wang, X. Decentralized Automotive Radar Spectrum Allocation to Avoid Mutual Interference Using Reinforcement Learning. IEEE Trans. Aerosp. Electron. Syst. 2021, 57, 190–205. [CrossRef]

21. Mun, J.; Ha, S.; Lee, J. Automotive Radar Signal Interference Mitigation Using RNN with Self Attention. In Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Barcelona, Spain, 4–8 May 2020; pp. 3802–3806.

22. Overdevest, J.; Koppelaar, A.G.C.; Bekooij, M.J.G.; Youn, J.; van Sloun, R.J.G. Signal Reconstruction for FMCW Radar Interference Mitigation Using Deep Unfolding. In Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Rhodes Island, Greece, 4–10 June 2023; pp. 1–5.

23. Mun, J.; Kim, H.; Lee, J. A Deep Learning Approach for Automotive Radar Interference Mitigation. In Proceedings of the IEEE 88th Vehicular Technology Conference, Chicago, IL, USA, 27–30 August 2018; pp. 1–5.

24. Chen, S.; Shangguan, W.; Taghia, J.; Kühnau, U.; Martin, R. Automotive Radar Interference Mitigation Based on a Generative Adversarial Network. In Proceedings of the IEEE Asia-Pacific Microwave Conference (APMC), Hong Kong, 8–11 December 2020; pp. 728–730.

25. Richards, M.A. Fundamentals of Radar Signal Processing, 2nd ed.; McGraw-Hill: New York, NY, USA, 2014.

26. Wang, J.; Ding, M.; Yarovoy, A. Matrix-Pencil Approach-Based Interference Mitigation for FMCW Radar Systems. IEEE Trans. Microw. Theory Tech. 2021, 69, 5099–5115. [CrossRef]

Disclaimer/Publisher’s Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.