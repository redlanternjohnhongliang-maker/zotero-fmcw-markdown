# Mutual Interference Suppression Using Wavelet Denoising in Automotive FMCW Radar Systems

Seongwook Lee , Member, IEEE, Jung-Yong Lee , and Seong-Cheol Kim , Senior Member, IEEE

Abstract— This paper presents an efficient mutual interference suppression method using wavelet denoising in automotive radar systems. When a radar signal transmitted from another radar-equipped vehicle flows into our radar system, it acts as an interference signal and degrades the target detection performance. With wavelet denoising, the interference signal can be extracted from the time-domain low-pass filter output. Then, the effect of the interference can be mitigated by subtracting the interference signal from the original low-pass filter output. As a result, the beat frequency containing the target information can be estimated accurately. Simulation results show that the proposed method can enhance the estimation accuracy of the target’s distance, velocity, and angle. In addition, the performance of the proposed method is verified through actual experiments using heterogeneous radars. In the measurement results, even though the exact specifications of the radar signal transmitted from the other vehicle are not identified, the interference is effectively suppressed. Unlike other existing methods, the proposed method using wavelet denoising does not need to generate a specific radar waveform and it can mitigate interference only by signal processing without changing the existing hardware.

Index Terms— Automotive frequency-modulated continuous wave (FMCW) radar, mutual interference suppression, wavelet denoising.

## I. INTRODUCTION

N RECENT years, there has been a growing interest in automotive sensors, such as ultrasonic, vision, lidar, and radar sensors, to provide safety and convenience to drivers. In addition, research has been being actively carried out to enable sharing of data acquired from each sensor between automobiles and traffic systems [1], [2]. Among these automotive sensors, the importance of radar sensors has been emphasized because they are robust under bad weather conditions and have longer detection ranges than other sensors. For the automotive radar, a frequency-modulated continuous wave (FMCW) radar operating at 77 GHz is widely used due to its low production costs and power consumption as well as small size [3]. This automotive FMCW radar can be used to estimate the range and velocity of the target, recognize road structures [4], [5], and identify the types of detected targets [6], [7].

As the number of radar-equipped vehicles increases, signal interference between automotive radar systems has become an important issue [8]. When an FMCW radar signal from another vehicle flows into our radar system, the signal can act as an interference signal. When the frequency difference between our transmitted signal and the interference signal is smaller than the cut-off frequency of the low-pass filter of our radar system, a signal with undesired frequency components is detected. This undesired signal appears as a pulse-like signal in the time domain and it then spreads over all frequency components in the frequency domain. Thus, the beat frequency containing the desired target information is buried by the interference, and the desired target cannot be detected [9]– [13]. Because misdetection of the target can be a great risk to a driver using an automotive radar function, such as adaptive cruise control, an efficient method to mitigate the effect of mutual interference is required.

Some studies have been proposed to suppress the mutual interference between automotive FMCW radar systems. In [14]–[20], methods to mitigate the interference by modifying the FMCW radar waveforms were proposed. Moreover, a few studies proposed to suppress the interference through signal processing techniques without changing the existing radar systems [9], [21]–[24]. In [9], the author removed the interference by substituting zeros for the period where the interference occurred in the entire signal. If the period is short, the interference can be effectively suppressed without loss of the desired target information; however, if the period is long, the information of the target may be damaged by the zeropadding. To overcome the loss of the target information caused by the zero-padding, the authors in [21], [22] reconstructed the interference signal by estimating its amplitude and phase and subtracted the reconstructed signal from the original signal; however, because the phase of the FMCW radar signal is often distorted by the phase noise in an actual environment [25], the phase information has low reliability. In [24], the advanced weighted-envelope normalization (AWEN) method effectively suppressed the mutual interference by sensing the interference signal and reducing its amplitude. In this method, some parameter values are determined empirically, so they have to be adjusted according to each FMCW radar system.

Therefore, we propose a simple but effective mutual interference suppression method using wavelet denoising, which is widely used to remove a noise component from a given signal [26]. In wavelet denoising, a given signal is decomposed by applying a wavelet transform. Then, to eliminate the noise component, the wavelet coefficients corresponding to the noise is thresholded [27]. In general, the time-domain low-pass filter output in the mutual interference situation consists of sinusoids which contain the information of the desired targets and the pulse-like signal caused by the interference. In this case, the intensity of the interference signal is usually more than 30 dB larger than those of the signals reflected from the desired targets because the interference signal comes directly from another vehicle [9]. Generally, wavelet denoising is used to remove the noise when the intensity of the signal we want to detect is stronger than that of the noise signal. However, in the case of mutual interference, the wavelet denoising process needs to be reversed because the intensity of the interference signal is much greater than those of the signals reflected from the targets. In other words, the low-intensity sinusoidal waves are regarded as the noise component to be removed and the high-intensity pulse-like interference signal is regarded as a signal to be left in. By applying a wavelet transform and thresholding the wavelet coefficients to the low-pass filter output, we can extract the pulse-like interference signal from which the sinusoids are removed. After that, if we subtract the interference signal from the original low-pass filter output, we can extract the desired target signals without the mutual interference.

The interference suppression method using wavelet denoising is similar to those in [21], [22] in that the interference signal is reconstructed and subtracted from the original signal; however, the interference suppression with wavelet denoising is not greatly affected by the phase noise. In addition, compared to the AWEN method in [24], large adjustments in the parameter values depending on the radar systems are not required in the wavelet denoising method. Moreover, unlike methods proposed in [14]–[20], we do not need to create new FMCW radar waveforms to mitigate the interference and can suppress the effect of the interference by simple post signal processing without changing the existing radar hardware. Since the amount of computation of the wavelet transform is almost the same as that of the Fourier transform, our proposed method can be used in real-time in practical automotive radar systems.

The remainder of this paper is organized as follows. In Section II, the method to estimate the distance and velocity of the target and the effect of mutual interference in the automotive FMCW radar system are explained. Then, the proposed mutual interference suppression method using wavelet denoising is introduced in Section III. Next, the performance of the proposed method is verified through simulations and

actual measurements in Sections IV and V, respectively.   
Finally, we conclude this paper in Section VI.

## II. EFFECT OF MUTUAL INTERFERENCE IN AUTOMOTIVE FMCW RADAR SYSTEM

A. Distance and Velocity Estimation in Automotive FMCW Radar System

In the FMCW radar system, the frequency of a transmitted signal varies linearly with time [28]. The transmitted frequency-modulated signal S(t) can be expressed as

$$
{ \cal S } ( t ) = A _ { T } \exp \biggl ( j \left( 2 \pi \left( f _ { c } - \frac { \Delta B } { 2 } \right) t + \pi \frac { \Delta B } { \Delta T } t ^ { 2 } \right) \biggr ) ( 0 \leq t \leq \Delta T ) ,\tag{1}
$$

where $A _ { T }$ is the amplitude of the transmitted signal, $f _ { c }$ is the carrier frequency of the modulated signal, B is the operating bandwidth, and $\Delta T$ is the sweep time. This transmitted signal is often referred to as an up-chirp signal because its frequency increases rapidly. For $\Delta T \ \leq \ t \ \leq \ 2 \Delta T$ , the radar transmits a signal whose frequency rapidly decreases from $\begin{array} { r } { f _ { c } + \frac { \Delta B } { 2 } } \end{array}$ to $\begin{array} { r } { f _ { c } - \frac { \Delta B } { 2 } } \end{array}$ , which is called a down-chirp signal. When the transmitted signal S(t) is reflected from L targets, the received signal R(t) is given as

$$
\begin{array} { l } { { \displaystyle R ( t ) = \sum _ { l = 1 } ^ { L } \left\{ A _ { R _ { l } } \exp \left( j ( 2 \pi ( f _ { c } + f _ { d _ { l } } - \frac { \Delta B } { 2 } ) ( t - t _ { d _ { l } } ) \right. \right. } } \\ { { \displaystyle \left. \left. + \pi \frac { \Delta B } { \Delta T } ( t - t _ { d _ { l } } ) ^ { 2 } ) \right) \right\} + n ( t ) } } \\ { { \displaystyle \left. = \sum _ { l = 1 } ^ { L } c _ { l } ( t ) + n ( t ) ( \operatorname* { m i n } t _ { d _ { l } } \le t \le \Delta T ) , \right. } } \end{array}\tag{2}
$$

where $A _ { R _ { l } } \left( l = 1 , 2 , \cdots , L \right)$ is the amplitude of the signal reflected from the $l _ { t h }$ target, $f _ { d _ { l } }$ is the Doppler frequency caused by the relative velocity between the $l _ { t h }$ target and the radar-equipped vehicle, and $t _ { d _ { l } }$ is the time delay caused by the relative distance between the $l _ { t h }$ target and the radar-equipped vehicle. In Eq. (2), $c _ { l } ( t )$ denotes the desired signal, which includes the distance and velocity information of the $l _ { t h }$ target, and $n ( t )$ represents the noise added at the receiving antenna.

Then, the received signal R(t) passes through the frequency mixer and is multiplied by the signal generated by the voltage controlled oscillator. The output of the frequency mixer $M ( t )$ is given by

$$
\begin{array} { l } { { \displaystyle M ( t ) = S ( t ) R ( t ) } } \\ { ~ = S ( t ) \left( \displaystyle \sum _ { l = 1 } ^ { L } c _ { l } ( t ) + n ( t ) \right) } \\ { ~ = S ( t ) \displaystyle \sum _ { l = 1 } ^ { L } c _ { l } ( t ) + S ( t ) n ( t ) ( \operatorname* { m i n } _ { l } t _ { d _ { l } } \le t \le \Delta T ) . } \end{array}\tag{3}
$$

Thereafter, $M ( t )$ becomes the input signal of the low-pass filter, whose output can be expressed as

$$
\begin{array} { l } { { \displaystyle { \cal L } ( { \cal M } ( t ) ) \cong A _ { T } \sum _ { l = 1 } ^ { L } A _ { R _ { l } } \exp \left( j ( 2 \pi ( ( \frac { \Delta B } { \Delta T } t _ { d _ { l } } - f _ { d _ { l } } ) t } } \\ { { \quad \quad \quad + ( f _ { c } + f _ { d _ { l } } - \frac { \Delta B } { 2 } ) t _ { d _ { l } } - \frac { \Delta B } { 2 \Delta T } { t _ { d _ { l } } } ^ { 2 } ) ) \right) } } \\ { { \displaystyle \quad \quad + L ( S ( t ) n ( t ) ) ( \operatorname* { m i n } t _ { d _ { l } } \leq t \leq \Delta T ) , } } \end{array}\tag{4}
$$

where $L ( \cdot )$ denotes the low-pass filter output in the time domain. The high-frequency components of $4 \pi f _ { c }$ or higher disappear when passing through the filter. Because $L ( M ( t ) )$ is expressed as a sum of sinusoid signals, the frequencies of each signal are extracted by applying the Fourier transform (in actual automotive radar systems, the fast Fourier transform (FFT) is used instead). The frequency extracted from the up-chirp signal by the Fourier transform is given by

$$
\begin{array} { l } { \displaystyle \hat { f } _ { l } ^ { u } = \frac { \Delta B } { \Delta T } t _ { d _ { l } } - f _ { d _ { l } } } \\ { \displaystyle = \frac { \Delta B } { \Delta T } \frac { 2 R _ { l } } { c } - \frac { 2 \upsilon _ { l } } { c } f _ { c } , ~ ( l = 1 , 2 , \cdot \cdot \cdot , L ) , } \end{array}\tag{5}
$$

where $R _ { l }$ and ${ \upsilon } _ { l }$ are the relative distance and relative velocity between the $l _ { t h }$ target and the radar-equipped vehicle, respectively, and c is the propagation velocity of the radar signal. These frequencies are called beat frequencies. Similarly, beat frequencies can be also extracted from the down-chirp signal as

$$
\begin{array} { l } { { \displaystyle { \hat { f } } _ { l } ^ { d } = \frac { \Delta B } { \Delta T } t _ { d _ { l } } + f _ { d _ { l } } } } \\ { { \displaystyle ~ = \frac { \Delta B } { \Delta T } \frac { 2 R _ { l } } { c } + \frac { 2 \upsilon _ { l } } { c } f _ { c } } . } \end{array}\tag{6}
$$

Thus, if we use beat frequencies extracted from both up-chirp and down-chirp signals in the FMCW radar system, we can estimate $R _ { l }$ and ${ \boldsymbol { v } } _ { l }$ by pairing $\hat { f } _ { l } ^ { u }$ and $\hat { f } _ { l } ^ { d }$ , as

$$
\begin{array} { l } { { \hat { R } _ { l } = \left( \hat { f } _ { l } ^ { u } + \hat { f } _ { l } ^ { d } \right) \times \frac { c \Delta T } { 4 \Delta B } , } } \\ { { \hat { \upsilon } _ { l } = \left( \hat { f } _ { l } ^ { d } - \hat { f } _ { l } ^ { u } \right) \times \frac { c } { 4 f _ { c } } . } } \end{array}\tag{7}
$$

Here, T , B, c, and $f _ { c }$ are fixed in the radar system.

## B. Effect of Mutual Interference on Beat Frequency Estimation

In this section, we analyze the effect of mutual interference between the FMCW radar signals on beat frequency estimation. As shown in Fig. 1, suppose that an FMCW radar-equipped vehicle (i.e., green car), which acts as an interferer, approaches our FMCW radar-equipped vehicle (i.e., red car). The FMCW radar installed on the interferer may be the same as our radar, or it may not be. In this interference scenario, the time-frequency slope of the interference signal received by our radar-equipped vehicle can have two different trends, as shown in Fig. 2. On one hand, as shown in Fig. 2 (a), the time-frequency slope of the interference signal has the same sign as the slope of the signal transmitted from our vehicle. On the other hand, two time-frequency slopes have different signs, as shown in Fig. 2 (b).

![](images/1e5f458b7c48ca312b262496aab897fbd42cbc8ac06d350103ce4f16ec34ed61.jpg)

Fig. 1. Simple interference scenario with a desired target vehicle and an interferer.  
![](images/69078bd62fbf76540efaaf68a0824a0e2723146c838e462b9ecddab0dc76cc70.jpg)  
(a)

![](images/2cb89e494f76acf4515e604c2c96b68c4dfa93cd9b14f87538f12b8a6febc3ae.jpg)  
Fig. 2. Time-frequency slope trends of the interference signal: (a) same sign as the transmitted signal and (b) different sign to the transmitted signal.

Similar to $R ( t )$ in Eq. (2), the up-chirp interference signal in Fig. 2 (a) can be expressed as

$$
\begin{array} { c } { { I ^ { S S } ( t ) = \displaystyle \sum _ { i = 1 } ^ { I } \{ A _ { R _ { i } } \exp ( j ( 2 \pi ( f _ { c _ { i } } + f _ { d _ { i } } - \frac { \Delta B _ { i } } { 2 } ) ( t - t _ { d _ { i } } )   } } \\ { {   + \pi \frac { \Delta B _ { i } } { \Delta T _ { i } } ( t - t _ { d _ { i } } ) ^ { 2 } ) ) \} + n ( t ) } } \\ { {  \times ( \operatorname* { m i n } _ { i } t _ { d _ { i } } \le t \le \Delta T + \operatorname* { m a x } _ { i } t _ { d _ { i } } ) , } } \end{array}\tag{8}
$$

where $f _ { c _ { i } } , \ \Delta B _ { i } .$ , and $\Delta T _ { i }$ denote the carrier frequency, operating bandwidth, and sweep time of the interference signal transmitted from the $i _ { t h } ( i \ = \ 1 , \ : 2 , \ : \cdot \cdot \ , I )$ interferer, respectively. In addition, $f _ { d _ { i } }$ is the Doppler frequency caused by the relative velocity between the $i _ { t h }$ interferer and the radar-equipped vehicle, and $t _ { d _ { i } }$ is the time delay caused by the distance between the $i _ { t h }$ interferer and the radar-equipped vehicle. In other words, $t _ { d _ { i } }$ indicates the difference between the starting points of two time-frequency slopes, as indicated in Fig. 2 (a).

For the case where the time-frequency slopes of the transmitted and interference signals have same signs, the output of the low-pass filter is expressed as

$$
\begin{array} { r l r } {  { L ( S ( t ) I ^ { S S } ( t ) ) } } \\ & { } & { = A _ { T } \displaystyle \sum _ { i = 1 } ^ { L } \{ A _ { R _ { i } } \exp ( j ( 2 \pi ( ( f _ { c } - f _ { c _ { i } } ) }  \\ & { } & { - ( \frac { \Delta B } { 2 } - \frac { \Delta B _ { i } } { 2 } ) + ( \frac { \Delta B _ { i } } { \Delta T _ { i } } t _ { d _ { i } } - f _ { d _ { i } } ) ) t } \\ & { } & { + \pi ( \frac { \Delta B } { \Delta T } - \frac { \Delta B _ { i } } { \Delta T _ { i } } ) t ^ { 2 } } \\ & { } & { + 2 \pi ( f _ { c _ { i } } - \frac { \Delta B _ { i } } { 2 } + f _ { d _ { i } } ) t _ { d _ { i } } } \\ & { } & { - \pi \frac { \Delta B _ { i } } { \Delta T _ { i } } t _ { d _ { i } } ^ { 2 } ) ) \} + L ( S ( t ) n ( t ) ) ( \operatorname* { m a x } _ { l } t _ { d _ { l } } \le t \le \Delta T ) . } \end{array}\tag{9}
$$

In the same manner, when the time-frequency slopes of the transmitted and interference signals have different signs, the output of the low-pass filter can be also expressed as

$$
\begin{array} { r l } & { \displaystyle L ( S ( t ) I ^ { D S } ( t ) ) } \\ & { \quad = A _ { T } \displaystyle \sum _ { i = 1 } ^ { L } \lbrace A _ { R _ { i } } \exp ( j ( 2 \pi ( ( f _ { c } - f _ { c _ { i } } ) } \\ & { \quad - ( \frac { \Delta B } { 2 } + \frac { \Delta B _ { i } } { 2 } ) - ( \frac { \Delta B _ { i } } { \Delta T } _ { i } t _ { i _ { d } } + f _ { d _ { i } } ) ) t } \\ & { \quad \quad + \pi ( \frac { \Delta B } { \Delta T } + \frac { \Delta B _ { i } } { \Delta T _ { i } } ) t ^ { 2 } } \\ & { \quad \quad + 2 \pi ( f _ { c _ { i } } + \frac { \Delta B _ { i } } { 2 } + f _ { d _ { i } } ) t _ { d _ { i } } } \\ & { \quad \quad + \pi \frac { \Delta B _ { i } } { \Delta T } t _ { d _ { i } } ^ { 2 } ) ) \rbrace + L ( S ( t ) n ( t ) ) ( \operatorname* { m a x } _ { i } t _ { d _ { i } } \le t \le \Delta T ) . } \end{array}\tag{10}
$$

When these interference signals flow into our radar system, the beat frequency corresponding to the target cannot be accurately estimated in the frequency domain. For example, consider the case where the slopes of the transmitted and interference signals have different signs, as shown in Fig. 3 (a). In this case, a time interval where the frequency difference between the two signals is smaller than the cut-off frequency of the low-pass filter exists, which is indicated by T<sub>i</sub> in Fig. 3 (b). Therefore, the low-pass filter output contains undesired frequency components in addition to the beat frequency component corresponding to the target. If the frequency difference is not constant, the low-pass filter output includes frequency components from 0 to the cut-off frequency. Moreover, the intensity of the interference signal coming directly from the interferer does not suffer much loss, but the intensity of the signal reflected from the desired target is greatly attenuated [9]. Therefore, the undesired signal appears as a pulse-like signal in the time interval $T _ { i }$ , and it degrade the beat frequency estimation performance.

A simple example of the case mentioned above is as follows. In the case of Fig. 1, we assume that radars of the interferer and the target vehicle have the different signs of time-frequency slopes but the same $f _ { c } , \ \Delta T$ , and $\Delta B$ , and the relative distances and velocities of them are given by $( R _ { I } , \upsilon _ { I } ) \ = \ ( 2 0 m , - 1 5 m / s )$ and $( R _ { T } , \upsilon _ { T } ) =$ (100 m, 10 m/s), respectively. The radar parameter values used in the simulation are given in Table I. For this case, the low-pass filter outputs including the interference signal (i.e, $L ( M ( t ) ) + L ( S ( t ) I ^ { D S } ( t ) ) )$ in the time domain and the frequency domain are shown in Fig. 4. In the time-domain, the low-pass filter output consists of a desired target signal (i.e., a sinusoid) and a pulse-like interference signal. To extract the beat frequency corresponding to the desired target, the FFT is applied to this time-domain low-pass filter output. As shown in Fig. 4 (b), when the interference signal does not exist, the beat frequency corresponding to the desired target is estimated well by a peak detection algorithm such as the constant false alarm rate (CFAR) algorithm [29]. However, when the interference signal flows into our radar system, the interference level over all the frequency components increases. This is because the FFT of a function having a single value in the time domain has all values in the frequency domain. In this case, because no significant difference between the magnitude of the beat frequency component and those of nearby frequency components exists, the CFAR algorithm does not work properly, which causes misdetection of the desired target. Because this misdetection of the target can lead to a dangerous situation, an effective but simple interference suppression method is required in automotive radar systems.

![](images/5fec49568e0ab30b2543c346295b4816da3ce1324988cf0e3a220d64f4f29669.jpg)

(a)  
![](images/fd889370bc74d103ab0d91c0761bccbaa8faec18588d8ff37474e1aadfd9d246.jpg)  
Fig. 3. (a) Time-frequency slopes of the transmitted and interference signals (different sign case). (b) Beat frequency between the transmitted and interference signals.

TABLE I  
PARAMETER VALUES USED IN THE SIMULATION
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Carrier frequency $\overline { { ( f _ { c } ) } }$ </td><td rowspan=1 colspan=1>76.5 GHz</td></tr><tr><td rowspan=1 colspan=1>Speed of light (c)</td><td rowspan=1 colspan=1> $\overline { { 3 \times 1 0 ^ { 8 } \ m / s } }$ </td></tr><tr><td rowspan=1 colspan=1>Bandwidth (∆B)</td><td rowspan=1 colspan=1>500 MHz</td></tr><tr><td rowspan=1 colspan=1>Sweep time (∆T)</td><td rowspan=1 colspan=1>5 ms</td></tr><tr><td rowspan=1 colspan=1>Sampling frequency $\overline { { ( f _ { s } ) } }$ </td><td rowspan=1 colspan=1>400 kHz</td></tr><tr><td rowspan=1 colspan=1>Cut-off frequency</td><td rowspan=1 colspan=1>1.5 MHz</td></tr></table>

![](images/258e42368fabad46d3bdcd9d27d6774a9ec2a18d9c47286f4d25be090165ad45.jpg)  
(a)

![](images/a7379c5722eb24758e256bab4cbd77c959d97621bc090114fdb3ebde98bf72ee.jpg)  
(b)  
Fig. 4. Low-pass filter output consisting of the desired target signal and a pulse-like interference signal: (a) in the time-domain and (b) in the frequencydomain.

## III. PROPOSED MUTUAL INTERFERENCE SUPPRESSIONMETHOD USING WAVELET DENOISING

In this section, we propose to suppress the mutual interference in the time domain using wavelet denoising. As mentioned in Section II, the low-pass filter output including the interference signal can be expressed as

$$
L _ { I } ( t ) = L ( M ( t ) ) + L ( S ( t ) I ^ { D S } ( t ) ) .\tag{11}
$$

As shown in Fig. 4 (a), $L _ { I } ( t )$ consists of a sinusoid and a pulse-like interference signal in the time domain. In general, wavelet denoising is widely used to effectively remove the noise component from a given signal [26]. Here, we consider the target signal (i.e., a sinusoid) as the noise component and remove it from the low-pass filter output using wavelet denoising. Then, by subtracting this denoised signal from the original low-pass filter output, we only leave the sinusoid corresponding to the target. In other words, we first reconstruct $L ( S ( t ) \bar { I } ^ { D S } ( t ) )$ ) using wavelet denoising and then subtract it from $L _ { I } ( t )$ to recover only $L ( M ( t ) )$ ). The proposed interference suppression method consists of the following steps.

## A. Decomposition of Low-Pass Filter Output Using Wavelet Transform

First, we decompose the low-pass filter output using the wavelet transform. For example, many wavelets such as the Haar, Daubechies, Coiflets, Symlets, Morlet, and Mexican Hat wavelets can be used. Among these wavelets, we use the Haar wavelet because it is the simplest among the wavelets, yet still effective [26]. The Haar wavelet’s mother wavelet function $\psi ( t )$ can be expressed as

$$
\psi ( t ) = \left\{ \begin{array} { l l } { 1 \quad ( 0 \leq t < 1 / 2 ) } \\ { - 1 \quad ( 1 / 2 \leq t < 1 ) } \\ { 0 \quad ( t < 0 , t \geq 1 ) . } \end{array} \right.\tag{12}
$$

As you can see in Eq. (12), $\psi ( t )$ is discontinuous at the middle point $\begin{array} { r } { ( \mathrm { i } . \mathrm { e } . , t = \frac { 1 } { 2 } ) } \end{array}$ and resembles a step function.

Then, we apply the Haar wavelet transform to $L _ { I } ( t )$ to find the wavelet coefficients, which are expressed as

$$
W _ { a , b } = \int _ { - \infty } ^ { \infty } L _ { I } ( t ) \psi _ { a , b } ^ { * } ( t ) d t ,\tag{13}
$$

where

$$
\psi _ { a , b } ( t ) = 2 ^ { \frac { a } { 2 } } \psi ( 2 ^ { a } t - b ) , ~ ( a = 1 , 2 , \cdot \cdot \cdot , a _ { T } ) .\tag{14}
$$

Here, a and b are the scaling and time factors for the mother wavelet $\psi ( t )$ , respectively. Using these factors, $\psi ( t )$ can be expanded or contracted by a and can be shifted by b. To decompose $L _ { I } ( t )$ with the wavelet, we have to choose a<sub>T</sub> , which is called a decomposition level. The decomposition level is an index of how small the mother wavelet is made. When a higher level wavelet is used, the signal can be decomposed more finely. Thus, we have to choose the proper decomposition level considering the computational complexity. After applying the wavelet transform, the coefficients corresponding to each a-level Haar wavelet can be obtained.

## B. Thresholding for Extracting Wavelet Coefficients of Interference Signal

For each level from 1 to a<sub>T</sub> , we threshold the wavelet coefficients to extract only the significant components of the interference signal. In general, two thresholding methods can be used: soft thresholding and hard thresholding. Each thresholding method is expressed as

$$
\begin{array} { r l } & { f _ { s } ( W _ { a , b } ) = \left\{ \begin{array} { l l } { W _ { a , b } - \mathrm { s g n } ( W _ { a , b } ) \lambda , } & { \mathrm { i f } ~ \left| W _ { a , b } \right| \ge \lambda } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. } \\ & { f _ { h } ( W _ { a , b } ) = \left\{ \begin{array} { l l } { W _ { a , b } , } & { \mathrm { i f } ~ \left| W _ { a , b } \right| \ge \lambda } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. } \end{array}\tag{15}
$$

where sgn(·) is the signum function and λ is the threshold value. The graphs for these two thresholding methods are given in Fig. 5. Through this thresholding, the wavelet coefficients whose magnitudes are smaller than λ are eliminated. In other words, the components corresponding to the sinusoid $L ( M ( t ) )$ that are regarded as noise components are removed, and the components corresponding to the interference signal $L ( S ( t ) I ^ { \bar { D S } } ( t ) )$ are maintained. There are many ways to determine the threshold value λ. For instance, we can use the universal threshold [30] or Stein’s unbiased risk estimate [31]. When the universal threshold is used, it has been proven that the risk of thresholding is sufficiently low and the threshold meets the requirements of most applications [32]. Thus, we use the modified universal threshold in [33], which can be expressed in a fixed-form:

![](images/6d0f613c64591a4e03c9b188b1797a2a30da52c5e5620b9c5ad1111e4a4cabd0.jpg)  
(a)

![](images/6c2ab6376c6ad0ba6974d8fe96cd7498fcad8d53f5d475b60f98f993896e88b9.jpg)  
Fig. 5. Two thresholding methods for wavelet coefficients: (a) soft thresholding and (b) hard thresholding.

$$
\lambda = \hat { \sigma } _ { a } \sqrt { 2 \log ( N _ { I } ) } ,\tag{16}
$$

where $\hat { \sigma } _ { a }$ is the rescaling factor for the threshold value that is derived from a level-dependent estimation of the noise level and $N _ { I }$ is the length of the data.

## C. Reconstruction of Interference Signal

Using the thresholded wavelet coefficients of levels from 1 to a<sub>T</sub> , we reconstruct the interference signal, $\hat { L } ( S ( t ) I ^ { D S } ( t ) )$ . For the low-pass filter output given in Fig. 4 (a), we reconstruct the interference signal using a three-level Haar wavelet with the hard thresholding method, as shown in Fig. 6. In this case, because the interference signal has a simple pulse-like shape, it is easily reconstructed with only three-level Haar wavelet denoising process. Depending on the shape of the interference signal, we have to determine which level of the wavelet to use for the interference signal reconstruction.

## D. Subtracting Reconstructed Interference Signal From Original Low-Pass Filter Output

Finally, we can extract only the desired target signal by subtracting the reconstructed interference signal $\hat { L } ( \overline { { S } } ( t ) I ^ { \hat { D } S } ( t ) )$ ) from the original low-pass filter output $L _ { I } ( t )$ , which can be expressed as

$$
\hat { L } ( M ( t ) ) = L _ { I } ( t ) - \hat { L } ( S ( t ) I ^ { D S } ( t ) ) .\tag{17}
$$

We can expect that $\hat { L } ( M ( t ) )$ contains only a sinusoid corresponding to the desired target because the reconstructed interference signal is subtracted from the original filter output. Therefore, if we use the interference-suppressed signal $\hat { L } ( M ( t ) )$ , an enhanced beat frequency estimation can be achieved. Fig. 7 shows the frequency-domain low-pass filter output with the proposed interference suppression method applied. As shown in the figure, the interference level is reduced and the beat frequency corresponding to the target is accurately estimated by the CFAR algorithm. We also verified the performance of the proposed method by using the Daubechies, Coiflets, and Symlets wavelets. Regardless of the type of the wavelet, they showed almost identical suppression results. In addition, information of each desired target exists throughout the time domain and the interference signal exists only in a specific time region. Because the proposed method only eliminates the interference signal in the specific time region, the information of each desired target is hardly distorted. Thus, it can be applied regardless of the number of desired targets.

![](images/ac0fbb281af39af7545f348553a20cd64c4767c969ac81536cccd68437197ff9.jpg)  
Fig. 6. Reconstructed pulse-like interference signal in the time domain from wavelet denoising.

![](images/353180ca0276a1c8feced9c2f76def919e726c6768b3caf3f5e29f07ef874f4d.jpg)  
Fig. 7. Low-pass filter output with the proposed interference suppression in the frequency-domain.

## IV. SIMULATION RESULTS

We also simulated the case when two targets and one interferer exist in the field of view (FOV) of our radar system. The relative distances, relative velocities, and angles of the two targets are given by $( R _ { T _ { 1 } } , \upsilon _ { T _ { 1 } } , \theta _ { T _ { 1 } } ) = ( 1 0 0 m , 2 0 m / s , 1 ^ { \circ } )$ and $( R _ { T _ { 2 } } \upsilon _ { T _ { 2 } } , \theta _ { T _ { 2 } } ) \ = \ ( 8 0 m , 5 m / s , 1 0 ^ { \circ } )$ , respectively. In addition, the relative distance, relative velocity, and angle of an interferer are given by $( R _ { I } , \upsilon _ { I } , \theta _ { I } ) = ( 1 5 m , - 1 5 m / s , - 3 ^ { \circ } )$ Here, we assume that the time-frequency slopes of the transmitted and interference signals have different signs, and we use the three-level Haar wavelet transform and hard thresholding to reconstruct the interference signal. The parameter values used in the simulation is given in Table II. The frequency-domain low-pass filter outputs with and without the proposed interference suppression are given in Fig. 8. Fig. 8 (b) is an enlargement of the part near the beat frequencies in Fig. 8 (a). As shown in Fig. 8, when the interference suppression is not applied, the two beat frequencies cannot be identified by the CFAR algorithm because their magnitudes are little bigger than those of the nearby frequency components. In other words, the two beat frequencies corresponding to the targets are buried by the interference. However, when the interference signal is reconstructed and subtracted from the original low-pass filter output in the time domain, two dominant beat frequencies are extracted by the CFAR algorithm in the frequency domain, and it shows similar beat frequency estimation result for the case when no mutual interference exists.

TABLE II  
PARAMETER VALUES USED IN THE SIMULATION
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>∆B used by our radar</td><td rowspan=1 colspan=1>500 MHz</td></tr><tr><td rowspan=1 colspan=1>∆T used by our radar</td><td rowspan=1 colspan=1>5 ms</td></tr><tr><td rowspan=1 colspan=1>∆B used by the interferer</td><td rowspan=1 colspan=1>750 MHz</td></tr><tr><td rowspan=1 colspan=1>∆T used by the interferer</td><td rowspan=1 colspan=1>3 ms</td></tr></table>

![](images/4fccb307fb41f9b549a08e8a989472dfcdd1edb37ae16ac3a29d5240f2a4e957.jpg)  
(a)

![](images/25f9f1ed5ce3ca5f55f3df0d5e30622a05d96dbc52e95b380e4f48bf8dead7c2.jpg)  
(b)  
Fig. 8. Low-pass filter output with the proposed interference suppression in the frequency-domain: (a) for entire FFT indices and (b) for FFT indices near beat frequencies.

After applying the interference suppression method, the target angle estimation result also shows a different pattern. In general, to estimate the direction of arrival (DOA) of the signal reflected from the target, an array antenna system is usually used in automotive radar systems [34]. When the reflected signal is received at each antenna elements, the DOA information is included in the phase difference caused by the antenna spacing [35]. Using this phase difference, the DOA can be estimated by the Bartlett, estimation of signal parameters via rotational invariance techniques (ESPRIT), and multiple signal classification (MUSIC) algorithms [35]. These methods all use the correlation matrix of the received signals, which is expressed as

$$
\begin{array} { l } { { \displaystyle { \bf R } = \frac { 1 } { P } [ L _ { I , 1 } ( t ) , L _ { I , 2 } ( t ) , \cdot \cdot \cdot , L _ { I , P } ( t ) ] ^ { T } } \ ~ } \\ { { \displaystyle ~ \times [ L _ { I , 1 } ( t ) , L _ { I , 2 } ( t ) , \cdot \cdot \cdot , L _ { I , P } ( t ) ] } , } \end{array}\tag{18}
$$

where $L _ { I , p } ( t ) ( p = 1 , 2 \cdot \cdot \cdot , P )$ is the low-pass filter output of the $p _ { t h }$ antenna element. Without the mutual interference, the angle of the target can be estimated using the correlation matrix. Otherwise, we expect that the angle of the target cannot be accurately estimated and that of the interferer will be estimated instead. Fig. 9 shows the target angle estimation results from the MUSIC algorithm when the interference exists and when it is suppressed. In this simulation, we used the four-element receiving uniform linear array antenna and set the spacing between adjacent elements as 0.5 λ. As shown in the MUSIC pseudospectrum, if the proposed interference suppression is not applied, the angles of the interferer and one target are estimated, which are $- 3 ^ { \circ }$ and $9 . 5 ^ { \circ }$ , respectively. The angle of one target that is further from our radar-equipped vehicle cannot be found in the estimation result. However, if we suppress the mutual interference for all $L _ { I , p } ( t )$ with the proposed method, we can estimate the DOAs of the two targets. When we used the interference-suppressed correlation matrix R<sup>ˆ</sup> with the MUSIC algorithm, we could identify the two accurate DOAs corresponding to the two desired targets, which were $0 . 6 ^ { \circ }$ and $9 . 4 ^ { \circ }$ , respectively. Thus, the target angle estimation result showed a different pattern when the proposed interference suppression was applied.

Moreover, we also simulated the case where more than one chirp of the interference signal interfered with our transmitted signal, as shown in Fig. 10. In other words, mutual interference with the fast-ramp FMCW radar [36] is considered in this simulation. In this case, the time-frequency slopes of the transmitted and interference signals can have both same signs and different signs, as shown in Fig. 10 (a). Thus, the lowpass filter output consists of $L ( S ( t ) I ^ { \bar { S } S } ( t ) )$ and $L ( S ( t ) I ^ { D S } ( t ) )$ in Eq. (9) and Eq. (10). In addition, it can be expected that several pulse-like interference signals will appear where the frequency difference between the transmitted and interference signals is smaller than the cut-off frequency of the low-pass filter, as shown in Fig. 10 (b). In this simulation, the relative distances and velocities of the interferer and the target vehicle are given by $( R _ { I } , \upsilon _ { I } ) \ = \ ( 8 0 m , - 1 0 m / s )$ and $( R _ { T } , \upsilon _ { T } ) \ =$ (100m, 0m/s), respectively. In addition, the parameters values used in this simulation is given in Table III. Fig. 11 shows the low-pass filter output consisting of the desired target signal (i.e., a sinusoid) and the pulse-like interference signals in the time domain. As predicted through Fig. 10 (b), the interference signals appear in the time interval where the frequency difference is smaller than the cut-off frequency. In addition, the frequency-domain low-pass filter output for the same signal is shown in Fig. 12. As shown in the figure, the beat frequency corresponding to target is buried by the interference. For this low-pass filter output, we applied our proposed suppression method using the three-level Haar wavelet transform and hard thresholding, and the result is also shown in Fig. 12. Even when the interference is caused by the fast-ramp FMCW radar, the beat frequency corresponding to the target is accurately estimated by the CFAR algorithm after applying our proposed suppression method. Moreover, if there a few vehicles generating interference signals, the trend of the time-domain received signal is almost similar to Fig. 11. In this case, the detection performance also can be restored by eliminating each pulse-like signals with large amplitudes.

(a)  
![](images/61fb140af5455015a86b7a6304d5b874cacf9f3353cbc61e0a333e0424b44862.jpg)  
Fig. 9. MUSIC pseudospectrum for the low-pass filter output with the proposed interference suppression in the frequency-domain.

![](images/726ee73cd299409488a30fa0eb7ab5ec8494dbcc2f181ddbe7dd67d2e7e63081.jpg)

![](images/48b83fb080208d96a3fa1c4d167eba11b6bf0767520d71b1e604e0f67154d18d.jpg)  
Fig. 10. (a) Time-frequency slopes of the transmitted and interference signals (same signs + different signs case). (b) Beat frequency between the transmitted and interference signals.

TABLE III
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>∆B used by our radar</td><td rowspan=1 colspan=1>500 MHz</td></tr><tr><td rowspan=1 colspan=1>∆T used by our radar</td><td rowspan=1 colspan=1>5 ms</td></tr><tr><td rowspan=1 colspan=1>∆B used by the interferer</td><td rowspan=1 colspan=1>500 MHz</td></tr><tr><td rowspan=1 colspan=1>∆T used by the interferer</td><td rowspan=1 colspan=1>0.5 ms</td></tr></table>

PARAMETER VALUES USED IN THE SIMULATION

![](images/596c4e58e2e805dd5194c59e7459b509289b33338198058d6d536df86606a605.jpg)  
Fig. 11. Low-pass filter output consisting of the desired target signal and a pulse-like interference signal in the time-domain.

![](images/9e1a46004e75d3b51b9555637fc1b953197a97d7b4e65220c3a88ab9c41aa3e2.jpg)  
Fig. 12. Low-pass filter output with the proposed interference suppression in the frequency-domain.

## V. MEASUREMENT RESULTS

We also conducted actual measurements using commercial automotive radar systems to verify the performance of the proposed interference suppression method. To implement the mutual interference scenario, two different commercial automotive radars were used; one is a radar produced by the Mando Corporation (i.e., LRR 20) and the other is a radar made by the Delphi Corporation. The Mando and Delphi radars act as the radar-equipped vehicle and the interferer, respectively, as shown in Fig. 1. The target simulator in the anechoic chamber created a virtual target with a radar cross section of 10 dBsm and a distance of 145 m. In addition, the Delphi radar is located 5 m away from the Mando radar.

![](images/0f462ffbadb4e6af8f2e7b7255fb7c916c17b7c57c30f9caef91788fd018a23e.jpg)  
Fig. 13. Low-pass filter output of the Mando radar with interference signals from the Delphi radar.

For the antenna system of the Mando radar, a single-element transmit antenna and a four-element receiving uniform linear array antenna are used. In addition, the FOV of the Mando radar ranges from $- 1 0 ^ { \circ }$ to 10<sup>◦</sup>. This antenna system transmits the FMCW radar signal in 10-ms signal transmission interval. During the 10 ms of the signal transmission interval, 5 ms is allocated to the transmission times of each up-chirp and down-chirp signal. This transmitted signal is reflected by the target in the FOV and the reflected signal is received by the array antenna. In the measurements, $f _ { c } , \ \Delta B$ , and $\Delta T$ in Eq. (1) are set to $7 6 . 5 G H z$ , 500 M H z, and 5 ms, respectively. The exact specifications of the Delphi radar are unknown.

Fig. 13 shows the low-pass filter output $L _ { I } ( t )$ of the Mando radar. In the figure, many pulse-like interference signals appear in the low-pass filter output. As mentioned in Section IV, this phenomenon occurs because the sweep time of the Delphi radar is much shorter than that of our Mando radar. Through this result, we can guess that the Delphi radar uses the fast-ramp FMCW radar signal. To extract the exact beat frequency from this signal, we apply our proposed suppression method. Similar to the simulation, we used a three-level Haar wavelet and hard thresholding method. Using the wavelet denoising method, we reconstructed the interference signal, as shown in Fig. 14. Then, this reconstructed signal is subtracted from the original low-pass filter output $L _ { I } ( t )$ that is given in Fig. 13 and the FFT is applied to the interference-suppressed filter output to extract the beat frequency corresponding to the target.

As shown in Fig. 15, without the proposed interference suppression, the beat frequency corresponding to target is buried by the interference, and thus the location of the target cannot be estimated appropriately. However, the beat frequency corresponding to the target is clearly revealed in the interference-suppressed filter output. In addition, the distance estimated from this beat frequency is 143.6 m, which is almost equal to the actual distance. We also compared the interference suppression performance to the AWEN algorithm proposed in [24]. Compared to our proposed method using wavelet denoising, the AWEN method shows similar interference suppression result, as shown in Fig. 15. However, in the AWEN method, to find the interval where the interference occurs, denoted by $T _ { i }$ in Fig. 3, both forward-sliding and backward-sliding windows are applied to the low-pass filter output. In other words, the stored low-pass filter output must be processed twice. In addition, after identifying $T _ { i } ,$ we have to determine the envelope threshold empirically based on the measurement data to suppress the amplitudes corresponding to the pulse-like interference signals. When this threshold was set inappropriately, we confirmed that the interference was not effectively suppressed. On the other hand, the proposed method using wavelet denoising can be applied more generally because only the level of the wavelet needs to be set.

![](images/19b0abd88e7904357e954b4dc123a0855efe03a21ef5f5198be5ef4ec5b859d7.jpg)  
Fig. 14. Reconstructed pulse-like interference signal in the time domain.

![](images/81036ebe244f461cfc516742d082ad7c794418e1bc6421dd92e87aa729db9a38.jpg)  
Fig. 15. Low-pass filter output with the proposed interference suppression in the frequency-domain.

## VI. CONCLUSION

In this paper, we proposed a method to suppress the mutual interference caused by other radar-equipped vehicles in automotive radar systems. When the radar signal transmitted from the other radar-equipped vehicle flows into our radar system, the beat frequency cannot be estimated accurately because it is buried by the increased interference level in the frequency domain. To mitigate the effect of the mutual interference, we proposed to use the wavelet denoising method. Through this proposed method, the interference signal was reconstructed and the effect of the interference was mitigated by subtracting the reconstructed signal from the original low-pass filter output. The performance of our proposed method was verified through simulations and actual measurements using heterogeneous automotive radars. In the simulation results, the proposed method worked properly when multiple targets existed or the mutual interference with a fast-ramp FMCW radar occurred. In addition, through the proposed interference suppression, accurate angle information of the targets could be extracted. Moreover, even though the exact specifications of the FMCW radar signal transmitted from the other radar were not identified, the mutual interference was effectively suppressed and the distance to the target was estimated accurately in the measurement results. To effectively utilize the proposed method in practical automotive radar systems, the parameter values related to wavelet denoising should be searched through a lot of experiments on actual roads.

## REFERENCES

[1] X. Cheng, C. Chen, W. Zhang, and Y. Yang, “5G-enabled cooperative intelligent vehicular (5GenCIV) framework: When Benz meets Marconi,” IEEE Intell. Syst., vol. 32, no. 3, pp. 53–59, May/Jun. 2017.

[2] X. Cheng, R. Zhang, and L. Yang, “Wireless toward the era of intelligent vehicles,” IEEE Internet Things J., vol. 6, no. 1, pp. 188–202, Feb. 2019.

[3] M. Schneider, “Automotive radar—Status and trends,” in Proc. IEEE German Microw. Conf. (GeMiC), Apr. 2005, pp. 144–147.

[4] J.-E. Lee, H.-S. Lim, S.-H. Jeong, H.-C. Shin, S.-W. Lee, and S.-C. Kim, “Harmonic clutter recognition and suppression for automotive radar sensors,” Int. J. Distrib. Sensor Netw., vol. 13, no. 9, pp. 1–11, Sep. 2017.

[5] S. Lee and S.-C. Kim, “Distribution-based iron road structure recognition method using automotive radar sensor,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 0212–0217.

[6] S. Lee, Y.-J. Yoon, J.-E. Lee, and S.-C. Kim, “Human-vehicle classification using feature-based SVM in 77-GHz automotive FMCW radar,” IET Radar, Sonar Navigat., vol. 11, no. 10, pp. 1589–1596, Oct. 2017.

[7] S. Lee, B.-H. Lee, J.-E. Lee, and S.-C. Kim, “Statistical characteristicbased road structure recognition in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 20, no. 7, pp. 2418–2429, Jul. 2019.

[8] T.-N. Luo, C.-H. E. Wu, and Y.-J. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[9] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[10] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Automotive radarinvestigation of mutual interference mechanisms,” Adv. Radio Sci., vol. 8, pp. 55–60, Sep. 2010.

[11] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in Proc. German Microw. Conf. (GeMiC), Mar. 2011, pp. 1–4.

[12] A. Bourdoux, K. Parashar, and M. Bauduin, “Phenomenology of mutual interference of FMCW and PMCW automotive radars,” in Proc. IEEE Radar Conf. (RadarConf), May 2017, pp. 1709–1714.

[13] S. Heuel, “Automotive radar interference test,” in Proc. 18th Int. Radar Symp. (IRS), Jun. 2017, pp. 1–7.

[14] L. Mu, T. Xiangqian, S. Ming, and Y. Jun, “Research on key tchnologies for collision avoidance automotive radar,” in Proc. IEEE Intell. Vehicles Symp., Jun. 2009, pp. 233–236.

[15] F. Torres, C. Frank, W. Weidmann, T. Mahler, T. Schipper, and T. Zwick, “The norm-interferer—An universal tool to validate 24 and 77 GHz band automotive radars,” in Proc. 9th Eur. Radar Conf. (EuRAD), Oct./Nov. 2012, pp. 6–9.

[16] J. Bechter, C. Sippel, and C. Waldschimidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility (ICMIM), May 2016, pp. 1–4.

[17] T.-H. Liu, M.-L. Hsu, and Z.-M. Tsai, “Mutual interference of pseudorandom noise radar in automotive collision avoidance application at 24 GHz,” in Proc. IEEE 5th Global Conf. Consum. Electron., Oct. 2016, pp. 1–2.

[18] X. Yang, K. Zhang, T. Wang, and Y. Zhao, “Anti-interference waveform design for automotive radar,” in Proc. IEEE 2nd Adv. Inf. Technol., Electron. Automat. Control Conf. (IAEAC), Mar. 2017, pp. 14–17.

[19] M. A. Hossain, I. Elshafiey, and A. Al-Sanie, “Mutual interference mitigation in automotive radars under realistic road environments,” in Proc. 8th Int. Conf. Inf. Technol. (ICIT), May 2017, pp. 895–900.

[20] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[21] J. Betcher and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2015, pp. 1–4.

[22] J. Betcher, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in Proc. 18th Int. Radar Symp. (IRS), Jun. 2017, pp. 1–10.

[23] C. Fischer, H. L. Blöcher, J. Dickmann, and W. Menzel, “Robust detection and mitigation of mutual interference in automotive radar,” in Proc. 16th Int. Radar Symp. (IRS), Jun. 2015, pp. 143–148.

[24] J.-H. Choi, H.-B. Lee, J.-W. Choi, and S.-C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Trans. Commun., vol. E99-B, no. 1, pp. 280–287, Jan. 2016.

[25] S. Ayhan, S. Scherr, A. Bhutani, B. Fischbach, M. Pauli, and T. Zwick, “Impact of frequency ramp nonlinearity, phase noise, and SNR on FMCW Radar accuracy,” IEEE Trans. Microw. Theory Techn., vol. 64, no. 10, pp. 3290–3301, Oct. 2016.

[26] J. C. Goswami and A. K. Chan, Fundamentals Wavelets. Hoboken, NJ, USA: Wiley, 1999.

[27] C. Taswell, “The what, how, and why of wavelet shrinkage denoising,” Comput. Sci. Eng., vol. 2, no. 3, pp. 12–19, May/Jun. 2000.

[28] A. G. Stove, “Linear FMCW radar techniques,” IEE Proc. F-Radar Signal Process., vol. 139, no. 5, pp. 343–350, Oct. 1992.

[29] B. R. Mahafza, Radar Systems Analysis and Design Using MATLAB, Boca Raton, FL, USA: CRC Press, 2000.

[30] D. L. Donoho and I. M. Johnstone, “Ideal spatial adaptation by wavelet shrinkage,” Biometrika, vol. 81, no. 3, pp. 425–455, Sep. 1994.

[31] C. M. Stein, “Estimation of the mean of a multivariate normal distribution,” Ann. Statist., vol. 9, no. 6, pp. 1135–1151, 1981.

[32] D. Baleanu, Advances in Wavelet Theory and Their Applications in Engineering, Physics and Technology. Rijeka, Croatia: InTech, 2012.

[33] I. M. Johnstone and B. W. Silverman, “Wavelet threshold estimators for data with correlated noise,” J. Roy. Stat. Soc. B, Stat. Methodol., vol. 59, no. 2, pp. 319–351, 1997.

[34] S. Lee, Y.-J. Yoon, J.-E. Lee, H. Sim, and S.-C. Kim, “Two-stage DOA estimation method for low SNR signals in automotive radars,” IET Radar, Sonar Navigat., vol. 11, no. 11, pp. 1613–1619, Nov. 2017.

[35] H. Krim and M. Viberg, “Two decades of array signal processing research: The parametric approach,” IEEE Signal Process. Mag., vol. 13, no. 4, pp. 67–94, Jul. 1996.

[36] V. Winkler, “Range Doppler detection for automotive FMCW radars,” in Proc. Eur. Radar Conf. (EuRAD), Oct. 2007, pp. 166–169.

![](images/7269669baa76a102f10a66f313c939568fe7f8d153a8ba3bade554898180d2b2.jpg)

Seongwook Lee (M’14) received the B.S. and Ph.D. degrees in electrical and computer engineering from Seoul National University (SNU), Seoul, South Korea, in 2013 and 2018, respectively. Since September 2018, he has been a Staff Researcher with the Samsung Advanced Institute of Technology (SAIT), Suwon, South Korea. He published more than 30 articles on radar signal processing. He is a Reviewer of international journals, such as Elsevier Ad Hoc Networks, Elsevier ICT Express, IEEE ACCESS, the IEEE COMMUNICATIONS LET-

TERS, the IEEE SENSORS JOURNAL, the IEEE SYSTEMS JOURNAL, the IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS, the IEEE TRANSACTIONS ON SIGNAL PROCESSING, IET Radar, Sonar & Navigation, MDPI Algorithms, MDPI Electronics, MDPI Remote Sensing, and MDPI Sensors. His research interests include automotive radar signal processing techniques, such as improved angle estimation, target recognition and classification, clutter suppression, mutual interference mitigation, and target tracking. He received the Distinguished Ph.D. Dissertation Award from the Department of Electrical and Computer Engineering, SNU.

![](images/090b116498cebfa3a64846cc4f19285290fbcb9744a68162e09015b08b39bf8a.jpg)

Jung-Yong Lee received the B.S. and Ph.D. degrees in electrical and computer engineering from Seoul National University (SNU), Seoul, South Korea, in 2013 and 2019, respectively. He is currently a Senior Professional with Samsung Research, Samsung Electronics Company, Ltd., Seoul. His current research interests include wireless channel modeling, localization algorithms, and deep learning applications.

![](images/fc84d4a2edb750c268d447c36dfdf36e3e149ae4792d7917227966b26b4b9864.jpg)

Seong-Cheol Kim (M’91–SM’14) received the B.S. and M.S. degrees in electrical engineering from Seoul National University, Seoul, South Korea, in 1984 and 1987, respectively, and the Ph.D. degree in electrical engineering from the Polytechnic Institute of NYU, Brooklyn, NY, USA, in 1995. From 1995 to 1999, he was with the Wireless Communications Systems Engineering Department, AT&T Bell Laboratories, Holmdel, NJ, USA. Since 1999, he has been a Professor with the Department of Electrical and Computer Engineering, Seoul

National University. His current research area covers system engineering of wireless communications, including millimeter wave channel modeling, localization algorithms, power line communications, and automotive radar signal processing techniques.