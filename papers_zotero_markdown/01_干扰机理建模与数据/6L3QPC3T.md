# A Peer-to-Peer Interference Analysis for Automotive Chirp Sequence Radars

Geonu Kim , Member, IEEE, Jiwoo Mun , Student Member, IEEE, and Jungwoo Lee , Senior Member, IEEE

Abstract—Mutual interference between automotive radar sensors is becoming a major concern due to the rapid increase of vehicles equipped with such systems. While there has been a plenty of studies on the interference of frequency modulated continuous wave (FMCW) radars, no work on chirp sequence (CS) radars has been reported in the literature in spite of their growing popularity in the automotive field. In this regard, this work presents an investigation of mutual interference for automotive CS radars. We analytically derive formulas describing the probability of ghost target appearance, and the signal-to-interference mitigation gain for interference of different waveforms, including continuous wave, FMCW, and CS waveforms, with comparison to an equivalent FMCW radar model. The derived formulas on the signal-to-interference mitigation gain are also verified by simulation results.

Index Terms—Automotive radar, interference, chirp sequence, FMCW.

## I. INTRODUCTION

R <sup>ECENTLY,</sup> <sup>automotive</sup> <sup>radar</sup> <sup>sensors</sup> <sup>have</sup> <sup>become</sup> <sup>a</sup> <sup>key</sup>component for various comfort and safety functions, such component for various comfort and safety functions, such as adaptive cruise control and automatic emergency braking. Their rapid market penetration causes serious concern on the risk of mutual interference between automotive radars. There has been extensive literature on the analysis of this issue [1]–[6], (mainly) in the context of the frequency modulated continuous wave (FMCW) radar, which has been most widely employed in the automotive field due to its relatively simple hardware and processing requirements.

Even though the hardware complexity in both the analog and digital domain is substantially higher, chirp sequence (CS) radars are gaining more preference due to their inherent ability to resolve range and velocity unambiguously, which not only eliminates the ghost-prone association task between multiple chirps required for FMCW radars [7], [8], but also helps to detect targets out of strong stationary clutter. Reduced cycle time is another advantage (see Section II-C).

![](images/6d6246c915704c585b56378d7e54066c9f7e4b5d7a2e20cc9c884c72f9855c4e.jpg)  
Fig. 1. CS (and also FMCW) radar schematic diagram.

In this work, we present a peer-to-peer analytical investigation of mutual interference for automotive CS radars, where no prior work has been reported in the literature. While some recent work analyzes the received interference power (or signalto-interference ratio) at the antenna port of automotive radars based on scenario or statistical modeling [9], [10], the focus of our study is on the effect of interference in the range-velocity spectrum of a victim radar as in conventional work on automotive FMCW radars [1]–[6]. Studies on interference mitigation for CS radars can be found in [11]–[14].

This paper is organized as follows. In Section II, we describe our system model including CS radar operation principles and the definition of an equivalent FMCW radar model that is subsequently used for various comparisons. Section III first describes the notion of signal-to-interference mitigation gain, and makes use of it to evaluate interference from continuous (CW) and FMCW radars. Interference from CS radars is also analyzed in Section IV, including a simple calculation of ghost target probability, description on partially coherent cases, and characterization of the signal-to-interference mitigation gain for quasi-noise scenarios.

## II. SYSTEM MODEL

## A. CS Radar Operation Principle<sup>1</sup>

Referring to Fig. 2, the instantaneous frequency of the transmitted signal (or output signal of the VCO in Fig. 1) can be written as

$$
f _ { T } \left( t \right) = f _ { c } + \alpha r _ { t } ,\tag{1}
$$

![](images/8ae38d937283c727e1ff31cce30aab7b8eb41a788b15e5b57f490b4dc78a3b19.jpg)  
Fig. 2. Instantaneous frequency of transmitted and received CS waveforms.

where $f _ { c }$ is the carrier frequency, α is the chirp slope, and $r _ { t }$ is the time offset measured from the beginning of each chirp. The chirp slope is defined as $\alpha = B W _ { s w } / T _ { c p }$ , where $B W _ { s w }$ and $T _ { c p }$ are the chirp sweep bandwidth and the chirp duration, respectively. Note that $r _ { t }$ can be written as $r _ { t } = t - q _ { t } T _ { c p } ,$ , where $q _ { t } = \lfloor t / T _ { c p } \rfloor$ is the corresponding chirp number for current time t. The phase of the transmitted signal can be expressed as

$$
\begin{array} { l } { { \displaystyle { \phi _ { T } } ( t ) = 2 \pi \int _ { 0 } ^ { t } { f _ { T } } ( \zeta ) d \zeta = 2 \pi { f _ { c } } t + 2 \pi \alpha \int _ { 0 } ^ { t } { r _ { \zeta } } d \zeta } } \\ { ~ } \\ { { \displaystyle ~ = 2 \pi f _ { c } t + 2 \pi \alpha \left( \int _ { 0 } ^ { q _ { t } T _ { c p } } { r _ { \zeta } } d \zeta + \int _ { q _ { t } T _ { c p } } ^ { t } { r _ { \zeta } } d \zeta \right) } } \\ { ~ } \\ { { \displaystyle ~ = 2 \pi f _ { c } t + \pi \alpha T _ { c p } ^ { 2 } q _ { t } + \pi \alpha r _ { t } ^ { 2 } } . } \end{array}\tag{2}
$$

The received signal with phase $\phi _ { R } ( t ) = \phi _ { T } ( t - \tau )$ , where $\tau$ is the two-way propagation delay between the radar and the target, is dechirped by the transmitted signal (with the mixers in Fig. 1) resulting in the beat signal whose phase is

$$
\begin{array} { l } { { \phi _ { B } ( t ) = \phi _ { T } ( t ) - \phi _ { R } ( t ) = \phi _ { T } ( t ) - \phi _ { T } ( t - \tau ) } } \\ { { \mathrm { } } } \\ { { \mathrm { } = 2 \pi f _ { c } \tau + \pi \alpha T _ { c p } ^ { 2 } ( q _ { t } - q _ { t - \tau } ) + \pi \alpha ( r _ { t } ^ { 2 } - r _ { t - \tau } ^ { 2 } ) . } } \end{array}\tag{3}
$$

By processing the beat signal only for $r _ { t } \ge \tau _ { \operatorname* { m a x } } \ge \tau$ , where $\tau _ { \mathrm { m a x } }$ corresponds to a target at maximum distance of interest, we have

$$
\begin{array} { l } { { q _ { t - \tau } = q _ { t } , } } \\ { { \nonumber } } \\ { { r _ { t - \tau } = t - \tau - q _ { t - \tau } T _ { c p } = r _ { t } - \tau , } } \end{array}\tag{4}
$$

hence

$$
\begin{array} { r } { \phi _ { B } ( t ) = 2 \pi f _ { c } \tau + 2 \pi \alpha \tau r _ { t } - \pi \alpha \tau ^ { 2 } . } \end{array}\tag{5}
$$

For a target at distance $R = R _ { 0 } + v t$ , where $R _ { 0 }$ and v are the initial distance and the relative radial velocity of the target, respectively, the propagation delay is expressed as

$$
\begin{array} { l } { \displaystyle \tau = \frac { 2 R } { c } = \tau _ { 0 } + \frac { 2 v } { c } t } \\ { \displaystyle \ } \\ { \displaystyle = \tau _ { 0 } + \frac { 2 v } { c } T _ { c p } q _ { t } + \frac { 2 v } { c } r _ { t } , } \end{array}\tag{6}
$$

where $\tau _ { 0 } = 2 R _ { 0 } / c$ with c denoting the speed of light. For typical automotive radar parameters, the second term in (5) is smooth compared to the first, and the third term is negligible, which

TABLE I  
TYPICAL PARAMETERS FOR AUTOMOTIVE CS RADARS
<table><tr><td> $f _ { c }$ </td><td> $B W _ { s w }$ </td><td> $T _ { c p }$ </td><td> $N _ { c p }$ </td><td> $f _ { s }$ </td></tr><tr><td>77 GHz</td><td>150 MHz 26 µsec 75 ea</td><td></td><td></td><td>16MHz</td></tr></table>

leads to the approximation of $\phi _ { B } ( t )$ as

$$
\begin{array} { c } { { \phi _ { B } ( t ) \approx 2 \pi f _ { c } \tau + 2 \pi \alpha \tau _ { 0 } r _ { t } } } \\ { { { } } } \\ { { = 2 \pi f _ { c } \tau _ { 0 } + 2 \pi ( f _ { R } + f _ { D } ) r _ { t } + 2 \pi f _ { D } T _ { c p } q _ { t } , } } \end{array}\tag{7}
$$

where

$$
f _ { R } = \alpha \tau _ { 0 } \approx \alpha \frac { 2 R } { c } ,\tag{8}
$$

$$
f _ { D } = { \frac { 2 v } { c } } f _ { c } = { \frac { 2 v } { \lambda } } .\tag{9}
$$

The beat signal is collected for a coherent processing interval (CPI) which consists of $N _ { c p }$ chirps, so that the CPI duration is

$$
T _ { C P I } = N _ { c p } T _ { c p } .\tag{10}
$$

Arranging the beat signal in two dimensions by $r _ { t }$ and q<sub>t</sub>, applying sampling with a sampling period of $T _ { s }$ such that $r _ { t } = n T _ { s }$ and changing variable as $q _ { t } = k , ( 7 )$ can be rewritten as

$$
\phi _ { B } [ n , k ] = 2 \pi f _ { c } \tau _ { 0 } + 2 \pi ( f _ { R } + f _ { D } ) T _ { s } n + 2 \pi f _ { D } T _ { c p } k .\tag{11}
$$

The variables n and k are called fast and slow-time, respectively. From the above expression, it is clear that applying twodimensional discrete Fourier transform (DFT) to the beat signal yields a peak in the spectrum at a position corresponding to the fast and slow-time frequencies $f _ { R } + f _ { D }$ and $f _ { D }$ . For CS automotive radars, it is usually the case that $f _ { R } \gg f _ { D }$ such that the contribution of $f _ { D }$ to the observed fast-time frequency can be ignored. Once a target peak is detected in the spectrum, the corresponding range and velocity can be calculated from $f _ { R }$ and $f _ { D }$ . Note that a complete measurement cycle consists of a single CPI, i.e., the cycle time duration is

$$
T _ { c y c } = T _ { C P I } .\tag{12}
$$

The range resolution $\Delta R$ and the velocity resolution $\Delta v$ of a CS radar measurement are related to the fast-time frequency resolution $\Delta f _ { R }$ and the slow-time frequency resolution $\Delta f _ { D }$ by (8) and (9), respectively, while each frequency resolution is determined by its corresponding observation time:

$$
\Delta R = \frac { c } { 2 \alpha } \Delta f _ { R } = \frac { c } { 2 \alpha } \cdot \frac { 1 } { T _ { c p } } = \frac { c } { 2 B W _ { s w } } ,\tag{13}
$$

$$
\Delta v = { \frac { \lambda } { 2 } } \Delta f _ { D } = { \frac { \lambda } { 2 } } \cdot { \frac { 1 } { T _ { C P I } } } .\tag{14}
$$

Table I denotes typical waveform and system parameters for automotive CS radars. The resulting range and velocity resolutions (ΔR and $\Delta v )$ are 1 m and 3.6 km/h, respectively [17]. The sampling frequency $f _ { s } = 1 / T _ { s }$ is chosen to unambiguously detect targets up to a maximum range $( R _ { \mathrm { m a x } } )$ of 208 m according to the Nyquist sampling criterion and (8):

$$
f _ { s } = 2 f _ { R , \mathrm { m a x } } = \frac { 4 \alpha R _ { \mathrm { m a x } } } { c } .\tag{15}
$$

![](images/198e14de0b37302d57f7ede57c058b895d996f3817a8ba548f6f427a5949fc01.jpg)  
(a)  
(b)  
Fig. 3. Target signal case. (a) Range-velocity spectrum. (b) Color map for normalized power (dB).

## B. Simulation Platform

To validate our analysis, we show various simulation results based on the waveform and system parameters in Table I. Referring to Fig. 1, the baseband waveforms in the analog frontend are simulated at a sample rate of $8 \times B W _ { s w }$ , and the antialiasing filter (AAF) is modeled as an 8th order Butterworth low pass filter using impulse invariance [18]. In the DSP, 512-by-128-DFT with zero padding is performed to obtain the rangevelocity spectrum. Windowing in front of DFT is not performed in our simulations to make comparisons to analytical calculation easier. Noise is not included in the simulations to clearly present the effect of interference in the victim spectrum. The signal power is normalized such that the target signal case results in a 0 dB peak as shown in Fig. $3 ( \mathrm { a } ) . ^ { 2 }$ Note that the range-velocity spectrum is shown only for positive range since the spectrum corresponding to negative range can be ignored. While our simulation results agree well with analysis, it is worth mentioning that major simulation error sources include non-ideal AAF and straddle loss [19]. Specifically, the non-ideal AAF produces aliasing in high frequency, and it results in slightly higher simulated interference levels. The straddle loss of the reference target peak level makes normalization weaker, so it also leads to a small increase of simulated interference power.

## C. Equivalent FMCW Radar Model

FMCW radars measure range and velocity using only the fasttime frequency. In particular, chirps of much longer duration are used such that $f _ { D }$ becomes significant in the observed fast-time frequency. Furthermore, the slow-time dimension is not utilized, and both $f _ { R }$ and $f _ { D }$ are determined by the fast-time frequency measurement corresponding of a single chirp. The ambiguity of $f _ { R }$ and $f _ { D }$ by the single chirp measurement, which can be described by a straight line (for each target) in the range-velocity plane, is resolved by using $L _ { c p }$ chirps of different slopes and performing an intersection process in the range-velocity plane [7], [20]. While coherent DFT processing is done in a chirp by chirp basis, a complete measurement cycle therefore consists of (incoherently processed) $L _ { c p }$ chirps:

![](images/54087ed83e7c320afba9e2e495d22a6f4cdf7401386066bd34022e82f1a44e4a.jpg)  
Fig. 4. Instantaneous frequency of transmitted and received FMCW waveforms.

$$
T _ { C P I } = T _ { c p } ,\tag{16}
$$

$$
\begin{array} { r } { T _ { c y c } = L _ { c p } T _ { c p } . } \end{array}\tag{17}
$$

Typically a small number of up and down-chirp pairs are used as in Fig. 4. To have different chirp slopes, the chirp durations are usually chosen to be different, i.e., $T _ { 1 } \neq T _ { 2 }$ . In our work, however, we assume that $T _ { 1 } \approx T _ { 2 }$ and use a single parameter $T _ { c p }$ (or $T _ { C P I } )$ for simplicity. For chirp durations of significant difference, our analysis can be understood in an average sense by having $T _ { c p } = ( T _ { 1 } + T _ { 2 } ) / 2$

From (16), it is easy to see that the expressions for the range and the velocity resolution of FMCW radars are identical to (13) and (14), respectively. Therefore, assuming equal range and velocity resolutions for CS and FMCW radars operating in the same band, the following relation on their CPIs can be derived:

$$
T _ { C P I } ^ { F M C W } = T _ { C P I } ^ { C S } .\tag{18}
$$

On the other hand, their measurement cycle durations are different by

$$
T _ { c y c } ^ { F M C W } = L _ { c p } ^ { F M C W } T _ { c y c } ^ { C S } .\tag{19}
$$

## III. INTERFERENCE FROM CW AND FMCW RADARS

Interference typically results in increased noise floor in the victim radar spectrum [1], [2], [4]–[6]. In such a quasi-noise scenario, its effect can be quantified in terms of the signal-tointerference mitigation gain $G _ { S / I }$ [1], [6], which refers to the relative power gain of a target signal over interference measured from the antenna port up to the DFT processed frequency spectrum, where target detection is to be applied. In other words, $G _ { S / I }$ measures how well interference is suppressed in the victim radar compared to targets. The basic formula is

$$
G _ { S / I } = \frac { T _ { C P I } } { T _ { d w } } \cdot G _ { s p } ,\tag{20}
$$

where the terms $T _ { C P I } / T _ { d w }$ and $G _ { s p }$ are due to AAF and DFT, respectively. In particular, $T _ { d w }$ is the interference dwell time, which denotes the time extent where the interfering signal is in the AAF pass-band as shown in Fig. 5. The bandwidth of the AAF, denoted by $B W _ { A A F }$ , is determined by $\tau _ { \mathrm { m a x } } = 2 R _ { \mathrm { m a x } } / c$ such that $B W _ { A A F } = \alpha \tau _ { \mathrm { m a x } }$ . On the other hand, the signal processing gain $G _ { s p } [ 1 9 ]$ results from the integration by DFT, which is coherent for target signals but noncoherent for quasi-noise interference. It equals the number of samples integrated over a CPI:

![](images/e054970f9b0f6e775d636479c7baf5925ec0cdaa71d9fa60a22579f3f021d0cb.jpg)

Fig. 5. Interference dwell time.  
![](images/b36f36f7cd1543d91b349c44346571d924c9243fbd31b102942be2478e957340.jpg)  
Fig. 6. CW interference.

$$
G _ { s p } = \frac { T _ { C P I } } { T _ { s } } .\tag{21}
$$

## A. CW Interferer

Assuming noncoherent integration for CW interference, the signal-to-interference mitigation gain can be derived from (20), Fig. 5, and (21):

$$
G _ { S / I } = \frac { B W _ { s w } } { 2 B W _ { A A F } } \cdot \frac { T _ { C P I } } { T _ { s } } = B W _ { s w } T _ { C P I } ,\tag{22}
$$

where Nyquist rate sampling is assumed. Due to (18), the mitigation gain on CW interference for CS and FMCW radars seems identical. While the expression above is indeed valid for FMCW radars [6], the DFT integration over slow-time in CS radars is in fact coherent, since the phase increment of the beat signal per slow-time sample, i.e., the instantaneous frequency of the beat signal integrated over the chirp duration, is constant. This results in a line peak in the spectrum as shown in Fig. 6 rather than a flat quasi-noise floor. Since the interfering signal receives a coherent signal processing gain of $N _ { c p } ,$ the mitigation gain for this spectral line peak can be expressed as<sup>3</sup>

$$
G _ { S / I } = B W _ { s w } T _ { c p } ,\tag{23}
$$

![](images/1aa88daeeb80c452fbaece2f0a925d562de5a42a8e5fc0dd8cdbab06fa007da6.jpg)  
Fig. 7. FMCW interference.

which is $N _ { c p }$ times smaller than (22). The simulated line peak in Fig. 6 with the power level of −35 dB conforms with the calculated mitigation gain of 35.9 dB according to (23). The line peak would result in ghost target detection in situations where the mitigation gain is not enough to suppress the interference down to the noise floor.

## B. FMCW Interferer

Unlike CW interference, noncoherent DFT integration in the slow-time dimension is observed for FMCW interference, as shown in Fig. 7. The signal-to-interference mitigation gain for CS radars, as well as FMCW radars, can be derived as

$$
G _ { S / I } = B W _ { s w } T _ { C P I } S F ,\tag{24}
$$

where the additional scale factor [5], compared to (22), is due to the variation in dwell time of the FMCW interference over CW interference and is expressed as

$$
S F = \left| \frac { \alpha ^ { I } - \alpha } { \alpha } \right| ,\tag{25}
$$

where $\alpha ^ { I }$ denotes the FMCW interference chirp slope. The simulated interference floor level in Fig. 7 is about −53.5 dB by averaging over the entire spectrum, which is consistent with the calculated mitigation gain of 54.6 dB according to (24).<sup>4</sup>

An interesting observation is that the mitigation gains of CS and FMCW radars with respect to each other are identical, given that they are equivalent in the sense described in Section II-C. Specifically, the mitigation gain of the CS radar as victim can be derived by (24), (18), and (10) as

$$
\begin{array} { c } { { G _ { S / I } ^ { C S } = B W _ { s w } N _ { c p } ^ { C S } T _ { c p } ^ { C S } \left| \frac { \alpha ^ { F M C W } - \alpha ^ { C S } } { \alpha ^ { C S } } \right| } } \\ { { = B W _ { s w } T _ { c p } ^ { C S } ( N _ { c p } ^ { C S } \mp 1 ) , } } \end{array}\tag{26}
$$

where the sign in the expression turns into plus if the sweep directions of the victim and the interferer are opposite. Similarly,

![](images/ce2fe737485f0ab4dbce30dde73215ab9e83adc2db9a509d91fe8178de8ff42e.jpg)

![](images/69d087faf3f61c4de99286aa236db750eee987f6eb87596f3d4b9c0b736ac53b.jpg)  
Fig. 8. Ghost targets. (a) CS radar case. (b) FMCW radar case.

the mitigation gain of the FMCW radar is

$$
\begin{array} { r l } & { G _ { S / I } ^ { F M C W } = B W _ { s w } T _ { c p } ^ { F M C W } \left| \frac { \alpha ^ { C S } - \alpha ^ { F M C W } } { \alpha ^ { F M C W } } \right| \cdot \frac { 1 } { N _ { c p } ^ { C S } } } \\ & { = B W _ { s w } \frac { T _ { c p } ^ { F M C W } } { N _ { c p } ^ { C S } } ( N _ { c p } ^ { C S } \mp 1 ) } \\ & { = G _ { S / I } ^ { C S } , } \end{array}\tag{27}
$$

where the additional factor of $1 / N _ { c p } ^ { C S }$ reflects the noncoherent integration of $N _ { c v } ^ { C S }$ interfering CS chirps crossing into the victim FMCW chirp [21].

## IV. INTERFERENCE FROM CS RADARS

## A. Ghost Target Probability

To analyze the occurrence of ghost targets by interference, we assume that both of the victim and the interfering radars are identical systems, but with uniformly random time shifts as in [2], [5]. We further assume that measurement cycles are continuous without stopping intervals. Referring to Fig. 8(a), the probability of ghost targets in CS radars can be identified as

$$
P _ { g h o s t } ^ { C S } = \frac { N _ { c p } ^ { C S } \tau _ { \mathrm { m a x } } } { T _ { c y c } ^ { C S } } = \frac { \tau _ { \mathrm { m a x } } } { T _ { c p } ^ { C S } } .\tag{28}
$$

In comparison, the ghost probability for FMCW radars has been described in [2], [5] as

$$
P _ { g h o s t } ^ { F M C W } = \frac { \tau _ { \mathrm { m a x } } } { T _ { c y c } ^ { F M C W } } = \frac { \tau _ { \mathrm { m a x } } } { L _ { c p } ^ { F M C W } T _ { c p } ^ { F M C W } } ,\tag{29}
$$

where the principal difference is that every chirp in a measurement cycle has a different slope as shown in Fig. 8(b). Therefore, for equivalent CS and FMCW radars, we get

$$
\begin{array} { r } { P _ { g h o s t } ^ { C S } = P _ { g h o s t } ^ { F M C W } \times N _ { c p } ^ { C S } L _ { c p } ^ { F M C W } , } \end{array}\tag{30}
$$

which shows that CS radars are more susceptible to the risk of ghost targets than FMCW radars in the ideal scenario of perfectly identical victim and interfering radars. Note that, however, variation in the chirp duration can easily break coherence in the DFT integration over slow-time of CS radars such that sharp ghost peaks smooth down as later shown in Fig. 9(d). On the contrary, variation in the chirp duration has little effect on ghost target appearance in FMCW radars.

## B. Partially Coherent Cases

As mentioned above, in the case of interference with identical chirp slope but different chirp duration (or sweep bandwidth), there is no significant difference in both the mechanism and appearance of ghost targets for FMCW radars. On the other hand, the integration in slow-time results in different effects for CS radars as shown in Fig. 9, where

$$
\gamma _ { c p } = \frac { T _ { c p } ^ { I } } { T _ { c p } } ,\tag{31}
$$

with $T _ { c p } ^ { I }$ denoting the interference chirp duration. In Fig. 9(a), $\gamma _ { c p }$ in terms of minimum integer ratio is $6 / 5$ , which results in a periodic chirp pattern with a period of 6 victim chirps. During such a single period, only one interference chirp happens to lie in the AAF pass-band of the victim. The fast-time frequency of this chirp corresponds to the range value of the 6 ghost peaks appearing in the figure. The resulting spectrum can be understood as passing the slow-time signal at the corresponding fast-time frequency through a downsampler followed by an expander [18], whose factors are both 6. In case of Fig. 9(b), since the minimum integer ratio of $\gamma _ { c p }$ is 113/100, the chirp pattern repeats itself after every 113 victim chirps, which exceeds the total number of chirps in a CPI, i.e., $N _ { c p } = 7 5$ . Therefore, each interfering chirp lying in the AAF pass-band generates a single slow-time sample at its fast-time frequency, which results in a flat slow-time spectrum at the corresponding range. When $\gamma _ { c p }$ gets close to 1, the line peaks in Fig. 9(b) become closer and start to interact as shown in Fig. 9(c) and 9(d), eventually forming a target peak.

On the other hand, while interferers with non-identical chirp slopes make fast-time integration noncoherent, identical chirp durations keep integration in slow-time coherent in CS radars. The CW interference case described in Section III-A is a special case where the interference chirp slope is zero. Non-zero interference chirp slopes that are sufficiently different from the slope of the victim, result in spectrums similar to the CW interference case shown in Fig. 6, and can be simply described by taking the scale factor in (25) further into account. As the difference in chirp slope decreases, the spectral line peak along the fasttime frequency not only rises according to the variation in the scale factor, but also starts to get concentrated when the slope difference becomes smaller than a specific amount, eventually forming a target peak [21], [22]. The condition corresponding to this specific amount of slope difference is called critically dwelling. It is characterized by full dwelling of the interference chirp both in time and frequency as shown in Fig. 10. By defining

![](images/f258d1df72cc6b6ea30512b738a252435f87d01989ae1f9f19422e6dae7d50c7.jpg)  
(a)

![](images/756fd69f3354f9e33e05882a24f6cf2e521eef62ced53d78cb63ed6436b22131.jpg)  
(c)

![](images/f1a769cee4f8b88576fe3e76234b2228a5b02fd4dd27104189a65f2b89edfba9.jpg)  
(b)

![](images/e2c3c1bc5af3de4a5d910cc22411fca926461c93860df4d31c7dbc1410d7f08e.jpg)  
(d)

Fig. 9. Interference with identical chirp slope but different chirp durations. (Interference time offset adjusted for better illustration.) (a) $\gamma _ { c p } = 1 . 2 . ( \mathsf { b } ) \gamma _ { c p } = 1 . 1 3 .$ $\begin{array} { r } { \dot { \left( \mathrm { c } \right) } \gamma _ { c p } = 1 . 0 0 1 . \left( \mathrm { d } \right) \gamma _ { c p } = 1 . 0 0 0 1 } \end{array}$  
![](images/8f4fb60cee048a9f71a797c3bc4fd80917b6379ad92066302bd1ac5c6306f6d8.jpg)  
Fig. 10. Interference with different chirp slope but identical chirp duration.

$$
\delta = \frac { \alpha ^ { I } } { \alpha } - 1 ,\tag{32}
$$

the slope difference in terms of δ satisfies

$$
B W _ { s w } \left( 1 + \delta \right) \pm 2 \alpha \tau _ { \mathrm { m a x } } = B W _ { s w } ,\tag{33}
$$

from which we get

$$
| \delta | = \frac { 2 \tau _ { \mathrm { m a x } } } { T _ { c p } } .\tag{34}
$$

Assuming a maximum range of 208 m, we have $| \delta | \approx 0 . 1$ for a CS radar with parameters in Table I, which is $N _ { c p } = 7 5$ times larger than $| \delta | = 0 . 0 0 1 \AA$ 4 for an equivalent FMCW radar. Therefore, while only a slight variation in chirp slope is sufficient for FMCW radars to avoid ghost targets [21], [22], difference in chirp slopes should be relatively large for CS radars, putting slow-time coherence aside. However, this strong requirement in slope difference becomes much more relaxed when variation in chirp duration further exists, as shown in Section IV-C.

Finally, even if both of the chirp slopes and chirp durations are different, partial coherence in slow-time can produce line peaks in the spectrum as shown in Fig. 11(a), which can be described by noncoherent integration in fasttime as in Fig. 6, followed by downsampling and expanding as in Fig. 9(a).

## C. Quasi-Noise Effects

Analyzing quasi-noise effects due to noncoherence both in fast and slow-time is a very complicated task. To make the problem more tractable, we make the following assumptions, which can be justified in the sense that we are focusing on the worst case scenario.

1) Chirp slopes of the victim and interferer are similar. In particular, we assume that $- 1 \leq \delta \leq 1$

2) Both time and frequency offsets of the interfering waveform are center aligned such that maximal dwelling occurs both in time and frequency.

For further simplification, we first consider the case where the sweep bandwidth is exactly equal for both the victim and the interferer, as denoted in Fig. 12. Note that the beat signal can be approximately characterized by multiple virtual chirps of slope $\boldsymbol { \alpha } ^ { I } - \boldsymbol { \alpha } = \boldsymbol { \alpha } \boldsymbol { \delta }$ and vertical spacing $B W _ { s w }$ . Furthermore, their horizontal spacing can be expressed as $B W _ { s w } / | \alpha ^ { I } - \alpha | =$

![](images/676f1f0208bfe8a4257408b38e5b8f2627d3b99c65cb5781842d98354c57f26b.jpg)  
(a)

![](images/faf4ea596674897370e0f4d8c4e82f6aa4eeb9ca2cf54470733e0aab7807b4d9.jpg)  
(b)

![](images/859a24fd16d1e4d3ddf1fbd52d509fa6a65c7c637f1f0b60e7df07c46de16355.jpg)  
(c)  
Fig. 11. Interference with different chirp slope and different chirp duration. $\bar { ( \mathrm { a ) } } \bar { \delta } = 0 . 1 3 , \gamma _ { c p } = 1 . 2 . \ : ( \mathrm { b } )$ Same bandwidth, $\bar { \delta } = 0 . 1 3 \left( \mathrm { c } \right) \delta = - 0 . 0 5 , \gamma _ { c p } =$ 1.13.

$T _ { c p } / | \delta |$ , which results in

$$
\begin{array} { l } { { \displaystyle m _ { d w } \approx \left\lceil \frac { T _ { C P I } } { T _ { c p } / | \delta | } \right\rceil = \lceil N _ { c p } \| \delta \| } } \\ { { \le N _ { c p } } } \end{array}\tag{35}
$$

dwelling virtual chirps. The contribution of a single virtual chirp to the total dwell time is $2 B W _ { A A F } / | \alpha \delta |$ , hence

$$
T _ { d w } = 2 B W _ { A A F } / | \alpha \delta | \times m _ { d w } .\tag{36}
$$

Having noncoherent integration both over fast and slow-time, the signal-to-interference mitigation gain can be derived by substituting (36), (21), and $| \delta | = S F$ into (20):

$$
\begin{array} { r } { G _ { S / I } = \frac { N _ { c p } T _ { c p } | \alpha | | \delta | } { 2 B W _ { A A F } m _ { d w } } \cdot \frac { T _ { C P I } } { T _ { s } } } \\ { = B W _ { s w } T _ { C P I } S F \cdot \frac { N _ { c p } } { m _ { d w } } , } \end{array}\tag{37}
$$

![](images/e3810b0bba433ee4c6dc354c0218185c62e2177baef24fcde1c396c4340f5ce5.jpg)  
Fig. 12. Interference with different chirp slope and duration but identical bandwidth. The upper part shows the instantaneous frequency of the dechirped beat signal.

which is $N _ { c p } / m _ { d w } \ge 1$ times larger than the mitigation gain of the $\mathrm { F M C W - t o - F M C W }$ interference case denoted by (24). The simulated interference floor level in Fig. 11(b) is about −53.8 dB, which matches with the calculated mitigation gain of 55.0 dB according to (37) and (35).

Note that the slope difference resulting in the critically dwelling condition satisfies

$$
| \alpha \delta | \cdot T _ { C P I } = 2 B W _ { A A F } ,\tag{38}
$$

and therefore

$$
| \delta | = \frac { 2 \tau _ { \mathrm { m a x } } } { T _ { C P I } } ,\tag{39}
$$

which is equally small to the FMCW-to-FMCW interference case given by (34). Moreover, since $m _ { d w } = 1$ , there is an $N _ { c p } -$ fold advantage in terms of the mitigation gain.

If the sweep bandwidths are not identical, short chirp segments that otherwise would have formed a single virtual chirp are no longer aligned and must be considered individually. However, (37) is still valid since there is no fundamental difference when considering a specific fast-time frequency bin. The key difference is that $m _ { d w }$ now varies from bin to bin, and the interference floor is therefore no longer uniform but may fluctuate along the fast-time frequency axis as shown in Fig. 11(c). A useful observation in characterizing $m _ { d w }$ is that the short chirp segments do not overlap inside a single victim chirp interval, which is obvious for negative δ. Even for positive δ, the frequency gap between two continuous chirp segments is at least

$$
\begin{array} { r l } & { B W _ { s w } ^ { I } - 2 \times | \alpha | \delta \cdot T _ { c p } ^ { I } = \{ | \alpha ^ { I } | - 2 | \alpha | \delta \} T _ { c p } ^ { I } } \\ & { \qquad = \{ | \alpha | ( 1 + \delta ) - 2 | \alpha | \delta \} T _ { c p } ^ { I } } \\ & { \qquad = ( 1 - \delta ) | \alpha | T _ { c p } ^ { I } } \\ & { \qquad \geq 0 , } \end{array}\tag{40}
$$

as shown in Fig. 13. Therefore, we again have $m _ { d w } \leq N _ { c p }$ for every fast-time frequency bin, resulting in a larger mitigation gain compared to the FMCW-to-FMCW interference case.

![](images/5dd42e190fc540811a5c971d165febd1065227be7ddd9d501efa2dbea892a0ab.jpg)  
Fig. 13. Nonoverlapping short chirp segments of a dechirped beat signal in a single victim chirp interval.

## V. CONCLUSION

In this work, we have made an analytical investigation on mutual interference for automotive CS radars. The probability of ghost target appearance and the signal-to-interference mitigation gain for interference of several waveforms have been considered with comparison to an equivalent FMCW radar model. Various analytical formulations have been validated by simulation results. Our study shows that CS radars, compared to FMCW radars, are more robust to interference in general, but have a lot more corner cases including ghost target appearance. Interference effects between CS and FMCW radars are shown to be equivalent.

## REFERENCES

[1] D. Oprisan and H. Rohling, “Analysis of mutual interference between automotive radar systems,” in Proc. Int. Radar Sympo., Sep. 2005, pp. 1–4.

[2] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[3] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in Proc. 9th Eur. Radar Conf., Oct. 2012, pp. 1–5.

[4] M. Goppelt, H.-L. Blocher, and W. Menzel, “Automotive radar– ¨ investigation of mutual interference mechanisms,” Advances Radio Sci., vol. 8, pp. 55–60, 2010.

[5] M. Goppelt, H. L. Blocher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in Proc. German Microw. Conf., Mar. 2011, pp. 1–4.

[6] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, no. 3–4, pp. 371– 378, Jun. 2014.

[7] V. Winkler, “Range doppler detection for automotive FMCW radars,” in Proc. Eur. Radar Conf., Oct. 2007, pp. 166–169.

[8] S. Lutz, D. Ellenrieder, T. Walter, and R. Weigel, “On fast chirp modulations and compressed sensing for automotive radar applications,” in Proc. 15th Int. Radar Sympo., Jun. 2014, pp. 1–6.

[9] T. Schipper, S. Prophet, M. Harter, L. Zwirello, and T. Zwick, “Simulative prediction of the interference potential between radars in common road scenarios,” IEEE Trans. Electromagn. Compat., vol. 57, no. 3, pp. 322– 328, Jun. 2015.

[10] A. Al-Hourani, R. J. Evans, S. Kandeepan, B. Moran, and H. Eltom, “Stochastic geometry methods for modeling automotive radar interference,” IEEE Trans. Intell. Transp. Syst., vol. 19, no. 2, pp. 333–344, Feb. 2018.

[11] C. Fischer, H. L. Blocher, J. Dickmann, and W. Menzel, “Robust detection and mitigation of mutual interference in automotive radar,” in Proc. 16th Int. Radar Sympo., Jun. 2015, pp. 143–148.

[12] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, Apr. 2015, pp. 1–4.

[13] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in Proc. IEEE MTT-S Int. Conf. Microwaves Intell. Mobility, Apr. 2015, pp. 1–4.

[14] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in Proc. 18th Int. Radar Sympo., Jun. 2017, pp. 1–10.

[15] A. G. Stove, “Linear FMCW radar techniques,” IEE Proc. F - Radar Signal Proc., vol. 139, no. 5, pp. 343–350, Oct. 1992.

[16] M. Song, J. Lim, and D. J. Shin, “The velocity and range detection using the 2D-FFT scheme for automotive radars,” in Proc. 4th IEEE Int. Conf. Netw. Infrastructure Digital Content, Sep. 2014, pp. 507–510.

[17] F. Folster, and H. Rohling, “Signal processing structure for automotive ¨ radar,” Frequency, vol. 60, no. 1–2, pp. 20–24, Jan./Feb. 2006.

[18] A. Oppenheim, R. Schafer, and J. Buck, Discrete-time Signal Processing (Prentice Hall International Editions). Englewood Cliffs, NJ, USA: Prentice Hall, 1999.

[19] M. Richards, Fundamentals of Radar Signal Processing, 2nd ed. New York, NY, USA: McGraw-Hill Education, 2013.

[20] H. Rohling and M. M. Meinecke, “Waveform design principles for automotive radar systems,” in Proc. CIE Int. Conf. Radar, 2001, pp. 1–4.

[21] T. Schipper, “Radar interference phenomena at receiver stage,” presented at MOSARIM Workshop at European Microwave Week, Amsterdam, Netherlands, Nov. 2012.

[22] R. Pietsch et al., “Impact study of the interference with respect to ASIL,” the MOSARIM consortium, European Commission, Tech. Rep. D1.4, May 2011.

![](images/afe663f262433503df8496d5c9d4d4b5839fdad9368ea88d905f527495244beb.jpg)

Geonu Kim (M’18) received the B.S. and M.S. degrees in electrical engineering from Korea Advanced Institute of Science and Technology, Daejeon, South Korea, in 2004 and 2007, respectively, and the Ph.D. degree in electrical engineering and computer science from Seoul National University, Seoul, South Korea, in 2017. He is currently a Senior Manager with the NAND Technology Development Division, SK Hynix, Icheon, South Korea. His research interests include codes for distributed storage, VLSI signal processing, and error correction and signal process-D Flash memory.

ing algorithms for NAN

![](images/ee9ceac21a0008ddc3ba4fa618c22fb80ff4910de35fa8841eaa3524e74f13de.jpg)

Jiwoo Mun (S’18) received the B.S. degree in electrical engineering, in 2016, from Seoul National University, Seoul, South Korea, where he is currently working toward the Ph.D. degree with the Department of Electrical and Computer Engineering. His research interests include radar system and machine learning.

![](images/71e258f590f258923fc58a48e722dfe50b016e78c108462f1aae58db0ee16126.jpg)

Jungwoo Lee (S’88–M’94–SM’07) received the B.S. degree in electronics engineering from Seoul National University, Seoul, South Korea, in 1988, and the M.S.E. and Ph.D. degrees in electrical engineering from Princeton University, Princeton, NJ, USA, in 1990 and 1994, respectively. He is currently a Professor with the Department of Electrical and Computer Engineering, Seoul National University. From 1994 to 1999, he was a member of technical staff working on multimedia signal processing at SRI (Sarnoff), where he was a team leader (PI) for an \$18M NIST

ATP program. He has been with Wireless Advanced Technology Lab, Lucent Technologies Bell Labs, Murray Hill, NJ, USA, since 1999, and worked on W-CDMA base station algorithm development as a team leader, for which he received two Bell Labs technical achievement awards. His research interests include wireless communications, information theory, distributed storage, and machine learning. He holds 21 U.S. patents. He has been an Editor for the IEEE WIRELESS COMMUNICATIONS LETTERS, since 2017. He was an Associate Editor for the IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY (2008 to 2011) and Journal of Communications and Networks (2012–2016). He has also been a Chief Editor for KICS journal, and an Executive Editor for Elsevier-KICS ICT Express since 2015. He has also been a Track Chair for IEEE ICC SPC (2016–2017), and was a TPC/OC member for Globecom’18, ICC’15, ITW’15, VTC’15s, ISIT’09, PIMRC’08, ICC’05, and ISITA’05. He was the recipient of the Qualcomm Dr. Irwin Jacobs Award in 2014 for his contributions in wireless communications.