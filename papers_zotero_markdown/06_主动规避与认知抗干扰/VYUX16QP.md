# RadChat: Spectrum Sharing for Automotive Radar Interference Mitigation

Canan Aydogdu, Musa Furkan Keskin, Nil Garcia, Henk Wymeersch and Daniel W. Bliss, Fellow, IEEE

Abstract—In the automotive sector, both radars and wireless communication are susceptible to interference. However, combining the radar and communication systems, i.e., radio frequency (RF) communications and sensing convergence, has the potential to mitigate interference in both systems. This article analyses the mutual interference of spectrally coexistent frequency modulated continuous wave (FMCW) radar and communication systems in terms of occurrence probability and impact, and introduces RadChat, a distributed networking protocol for mitigation of interference among FMCW based automotive radars, including self-interference, using radar and communication cooperation. The results show that RadChat can significantly reduce radar mutual interference in single-hop vehicular networks in less than 80 ms.

## I. INTRODUCTION

Among the main goals of intelligent transportation systems (ITS) are (i) safety: reduce safety threats encountered due to human impact, and (ii) efficiency: provide transportation opportunities in a way that is ecologically and economically sustainable. Two important technological components are automotive radar and vehicular communication, especially for advanced driver assistant systems and self-driving cars [1], [2], serving complementary purposes.

Automotive radar provides local situational awareness, giving the vehicle timely and reliable information of the surroundings in the form of radar detections with distance, velocity, angle information. The high localization sensitivity (e.g., up to 3 cm for 76–81 GHz operating radars) and robustness against a variety of conditions (snow/fog/rain [3] or optical effects) of radar, is unfortunately threatened by mutual radarto-radar (R2R) interference [4]. Such interference is expected to be exacerbated with tens of radars deployed on autonomous vehicles in the next decade. Mutual interference results in increased effective noise floor, reduced detection capability and non-existing so-called ghost detections [4]–[8]. Techniques for mitigating R2R interference include removing polluted radar waveforms, radar sniffing and avoiding transmission, using frequency diversity and digital beamforming [9]. However, none of these methods guarantees interference-free radar sensing in a cost-efficient and implementable way.

Vehicular communication provides remote situational awareness by receiving wireless data packets from other vehicles, even outside the immediate range of local sensors. The communication capabilities built into cars can be divided in cellular, e.g., 4G Long-Term Evolution (LTE); and short range systems, e.g., WiFi-based 802.11p used in Dedicated Short-Range Communications (DSRC) [10] in the USA and ITS-G5 in Europe. While LTE cellular services are suitable for long-term traffic information (e.g., route suggestions), DSRC is specifically dedicated to provide very low latency transmission, critical in communications-based active safety applications, including future collision warning, blind spot warning, braking ahead warning [11]. However, DSRC suffers from communication-to-communication (C2C) interference, especially when many vehicles emit warning messages, in turn affecting system-wide safety.

Finally, some bands allow for dual purpose use: the unlicensed 60 GHz or so-called mmWave band (57–66 GHz) is used for IEEE 802.11ad WiGig communication under restrictions in terms of power emissions, but also for radar [12], [13]. The convergence of radar and wireless communications in mmWave bands can provide benefits for both applications. However, a dual use system must account for four types of interference: not only R2R and C2C, but also communication-toradar (C2R) and radar-to-communication (R2C) interference.

In this paper, we propose RadChat, a radar and communication cooperation system [14] operating in the 77 GHz radar band, whose sole purpose is to control and coordinate automotive radar sensors among vehicles via wireless communications in order to mitigate radar interference. RadChat is an integrated system with both radar and communication functionality (i.e., using different waveforms on the same hardware), built with minimal modification from standard frequency modulated continuous-wave (FMCW) based automotive radar, which is the most common, cheap and robust radar format used in the automotive sector today [1]. Our main contributions are as follows:

• An R2R, C2R, and R2C interference analysis of an FMCW radar and narrowband communication system, which indicates that: (i) R2C and C2R interference impedes reliable communication and radar sensing concurrently. Hence, radar and communication signals with similar powers must not share the same time-frequency resources. (ii) It is possible to ensure negligible R2R interference among different automotive radars if the FMCW radar chirp sequences start sweeping the frequency band at different time slots.

• A protocol for the physical (PHY) and medium access (MAC) layers, which is able to essentially reduce R2R radar interference while meeting automotive radar sensing requirements (i) among both radars on different vehicles and radars mounted on the same vehicle, (ii) in a fairly short time (80 ms).

• An in-depth analysis of the performance of RadChat, compared to standard FMCW in a single-hop dense vehicular ad-hoc network (VANET).

The additional capabilities of RadChat to enable inter-vehicle communication is outside the scope of this article and therefore left as a future work.

The remainder of this paper is organized as follows. After a brief literature review in Section II, an FMCW-based radar and communication cooperation system model is introduced in Section III, which is followed by a detailed analysis of R2R, C2R and R2C interference in Section IV. The RadChat framework is described in Section V including MAC and PHY layers. The R2R interference mitigation and networking performance of RadChat is investigated and results are presented in Section VI.

## II. RELATED WORK

## A. Classification of Joint Radar and Communications Systems

Joint radar and communication systems can be grouped in three categories: coexistence, cooperation and co-design. Coexistence aims to mitigate inter-system interference without information exchange. In cooperation, information is explicitly shared among both systems to mitigate interference [14]. Finally, co-design methods require both systems to be designed jointly from the ground up, not necessarily using the same hardware [14], but generally using the same waveform [15].

1) Coexistence: Radar communication coexistence was shown to increase the efficiency of the underutilized radar spectrum and solve the spectrum scarcity of communication systems [16], [17], and was therefore used in many different ways [14], [18]–[20] with the aim of sharing the same frequency band without radar and communication interfering each other. Different from these studies, our primary goal is not the spectral efficiency but mitigation of R2R interference, which turns out to be a problem in VANETs. We target to achieve this goal by help of communications, using the same hardware but different waveforms, which falls into the scope of radar and communication cooperation, described next.

2) Cooperation: For vehicular applications, the combination of communication and radar has been considered in various forms [21]–[23]. Estimation and information theoretic approaches were conducted on pulsed radars [24] and FMCW radars [25] in the joint multiple-access channels. Radar and communication cooperation, using the same hardware but different waveforms for radar and communications, was used in the 79 GHz band with the goal of improving individual pulsed radar sensing accuracy through communications, where the radar and communications use the channel in a time-division-medium-access (TDMA) manner controlled by a central unit [26].

3) Co-design: There are several radar communication codesign methods proposed in the literature. IEEE 802.11ad preamble is used as a radar signal for a vehicular environment in the 60 GHz band [13], a monopulse radar with frequencyshift-keying is used to incorporate communication data in a time-division-multiplexed (TDM) manner [27] and minimum shift keyed linear frequency modulated spread spectrum signals (MSK-LFM/SS) are used [22]. Orthogonal frequency division multiplexing (OFDM) has been the most extensively investigated option for radar communications co-design [13], [23], [28]–[31] due to its high degree of flexibility and high performance under different propagation conditions [32]–[35]. However, due to the cost-efficient, low-rate analog-to-digital convertors (ADC) preferred in automotive radars today, OFDM cannot fully occupy the radar band (77–81 GHz), limiting its distance resolution capability.

![](images/abfe9a3ceea684fd64f5aaa4a0d2bae801dcc3e619bee08b764aa9e33a2e75ac.jpg)  
Fig. 1: Illustration of the hardware of a RadChat unit. The unit reuses most of the hardware for communication (blue) and radar (green) functionalities.

## B. Medium Access Control for Cooperation

Most studies on cooperation between radar and communication have focuses on the physical layer [18]. In our prior work [36], [37], we have shown the potential of higher-layer coordination of automotive radars through communications for decreased R2R interference. There are few other studies including the higher layers in radar and communication cooperation [38], [39]. A separate dedicated radio is used for communication control in addition to a radar communications unit employing OFDM for communications in [38] with an emphasis on data communications rather than interference mitigation. Another MAC approach employing time division multiplexing among radar and communications is introduced in [39], where a preamble is added just prior to the radar. As a result, the radar is treated as a packet in CSMAbased communications and radar sensing has no priority over communications, which might end up with low radar sensing duty cycle in case of radar congestion.

## III. SYSTEM MODEL

## A. RadChat Unit

A RadChat unit is a modified automotive FMCW radar hardware, where the input to the conventional FMCW radar transmitter is switched between radar and communication and likewise the receiver antenna output is switched between the radar and communication receiver module as illustrated in Fig. 1. We assume a homogeneous VANET with identical Rad-Chat units, where all vehicles have the same radar and communication parameters (radar frame time, radar slope, radar bandwidth/carrier frequency, communication bandwidth/carrier frequency/modulation scheme, etc). RadChat units transmit and receive either radar or communication signals, but not both radar and communication signals simultaneously. The communication input/output and radar output of the RadChat unit is connected to the MAC layer of RadChat, introduced in Sec. V where spectrum sharing among radar and communications as well as among different RadChat units is presented. We now describe the operation of the RadChat unit.

![](images/a44014a7949e4330e52d5742667b8b4cf8d14b28911062a23c52785d81178190.jpg)  
Fig. 2: FMCW sawtooth radar waveform occupying $B _ { \mathrm { r } }$ bandwidth with simultaneous communication occupying $B _ { \mathrm { c } }$ bandwidth. The transmitted radar chirp sequence (blue lines) are received (red lines) with a Doppler frequency shift of $\bar { \boldsymbol { f } } _ { D }$ . The radar receiver is tuned to process radar reflections arriving inside the green band, which corresponds to the bandwidth of interest $B _ { \mathrm { m a x } } .$

## B. RadChat Transmitter

The transmitter of the RadChat unit either transmits radar signals or communication signals, but not both at the same time as illustrated in Fig.1.

1) Radar Transmitter: We consider a sequence of frequency modulated continuous waves, i.e., chirps, transmitted by an FMCW radar,

$$
s _ { \mathrm { r } } ( t ) = \sqrt { P _ { \mathrm { r } } } \sum _ { k = 0 } ^ { N - 1 } c ( t - k T )\tag{1}
$$

where $c ( t )$ is a chirp of the form [1], [40]

$$
c ( t ) = \left\{ { \begin{array} { l l } { e ^ { j \phi ( t ) } , } & { \ 0 \leq t \leq T } \\ { 0 , } & { \ { \mathrm { o t h e r w i s e } } } \end{array} } \right.\tag{2}
$$

with $\begin{array} { r } { \phi ( t ) = 2 \pi \left( f _ { \mathrm { r } } + \frac { B _ { \mathrm { r } } } { 2 T } t \right) t , } \end{array}$ , where $P _ { \mathrm { r } }$ is the radar transmit power, B denotes the radar bandwidth (typically 1–4 GHz), $f _ { \mathrm r }$ is the carrier frequency (around 77 GHz), T is the chirp duration, and N is the number of chirps per frame. The frame time $T _ { f } ~ = ~ N T + T _ { \mathrm { i d l e } }$ comprises $N T$ plus the idle and processing time. The instantaneous frequency of $c ( t )$ is given by $\begin{array} { r } { f ( t ) { \stackrel { - } { = } } \frac { 1 } { 2 \pi } \frac { d \phi ( t ) } { d t } = f _ { \mathrm { r } } + \frac { B _ { \mathrm { r } } } { T } t } \end{array}$ . Fig. 2 illustrates a typical FMCW sawtooth radar waveform with a chirp sequence starting at $( t = 0 , f = f _ { \mathrm { r } } )$ in time-frequency domain. The reflected chirp sequences are received starting at $( t ^ { \prime } , f _ { \mathrm { r } } + f _ { D } )$ due to a round trip delay of $t ^ { \prime }$ and a Doppler frequency shift of $f _ { D }$ . The green band corresponds to the bandwidth $B _ { \mathrm { m a x } }$ , which is defined as the bandwidth of interest at the radar receiver. Note that $B _ { \operatorname* { m a x } } \ \leq \ f _ { s }$ , where $f _ { s }$ is the ADC bandwidth, assuming a complex baseband radar architecture [41]. The radar receiver filters out the radar reflections arriving with frequencies outside $\begin{array} { r } { ( f _ { \mathrm { r } } + \frac { B _ { \mathrm { r } } } { T } t ) + [ - B _ { \mathrm { m a x } } , 0 ] . ~ B _ { \mathrm { m a x } } } \end{array}$ is proportional to the maximum delay of radar reflections taken into account $( T _ { \mathrm { m a x } } )$ and the maximum detectable range $( d _ { \mathrm { m a x } } )$

Remark 1. The FMCW radar waveform parameters, such as $B _ { \mathrm { r } } , T , T _ { f }$ and $N _ { \ast }$ , are set to meet requirements on the maximum detectable range $( d _ { \operatorname* { m a x } } )$ and maximum detectable relative velocity $( v _ { \mathrm { m a x } } )$ , as well as range and velocity resolution.

2) Communication Transmitter: During communication mode, the transmitted bandpass signal is [42]

$$
s _ { \mathrm { c } } ( t ) = \sqrt { P _ { \mathrm { c } } } x ( t ) e ^ { j 2 \pi f _ { \mathrm { c } } t }\tag{3}
$$

where $x ( t )$ represents the complex baseband signal with a bandwidth of $B _ { \mathrm { c } }$ after pulse shaping<sup>1</sup> and $f _ { \mathrm { c } }$ is the communication carrier frequency. We consider a communication signal

$$
x ( t ) = \sum _ { k = 0 } ^ { N _ { \mathrm { c } } - 1 } a _ { k } p ( t - k ( 1 + \alpha ) / B _ { \mathrm { c } } ) ,\tag{4}
$$

where $p ( t )$ is a unit-energy pulse of bandwidth $B _ { \mathrm { c } }$ with roll-off $\alpha \geq 0 , a _ { k }$ are unit-energy transmit data symbol.

## C. RadChat Receiver

The receiver of the RadChat unit either receives radar signals or communication signals, not both at the same time.

1) Radar Receiver: Considering a single target at distance $d ,$ the received back-scattered bandpass radar signal (at the co-located receiver) is

$$
r _ { \mathrm { r } } ( t ) = \gamma _ { \mathrm { r } } \sum _ { k = 0 } ^ { N - 1 } c ( t - 2 d / c - k T ) + w ( t )\tag{5}
$$

where a Doppler shift will be observed due to a time-varying distance $d = d _ { 0 } - v t$ with relative radial velocity v and initial distance $d _ { 0 }$

$$
\gamma _ { \mathrm { r } } = { \sqrt { P _ { \mathrm { r } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \sigma \lambda _ { \mathrm { r } } ^ { 2 } / ( ( 4 \pi ) ^ { 3 } d ^ { 4 } ) } }\tag{6}
$$

for target radar cross section<sup>2</sup> (RCS) σ, transmitter and receiver antenna gains $G _ { \mathrm { t x } }$ and $G _ { \mathrm { r x } } , ~ w ( t )$ is additive white Gaussian noise (AWGN) with power spectral density $N _ { 0 } , \ c$ denotes the speed of light and $\lambda _ { \mathrm { r } }$ is the wavelength of the radar carrier. The received signal is processed by the following blocks [43]: a mixer, an ADC, and a digital processor (Fig. 1). Then, after processing the bandpass signal in (5) through the receive chain, the sampled baseband ADC output is as following for the chirp $k , t = n / f _ { \mathrm { s } } , n = 0 , \dots , \lfloor T f _ { \mathrm { s } } \rfloor$

$$
\begin{array} { r } { \widetilde { r } _ { \mathrm { r } } ( t , k T ) = \gamma _ { \mathrm { r } } e ^ { j 2 \pi t \left( - \frac { 2 d _ { 0 } } { c } \frac { B _ { \mathrm { r } } } { T } + 2 \frac { v } { c } f _ { \mathrm { r } } - 2 \frac { v } { c } \frac { B _ { \mathrm { r } } } { T } t \right) } } \\ { \times e ^ { j 2 \pi k T \left( 2 \frac { v } { c } f _ { \mathrm { r } } - 2 \frac { v } { c } \frac { B _ { \mathrm { r } } } { T } t \right) - \frac { 2 d _ { 0 } } { c } f _ { \mathrm { r } } } + w ( t , k T ) } \end{array}\tag{7}
$$

where $0 \leq t \leq T$ denotes the time from the beginning of the kth chirp. Assume that we have a narrowband signal, $\mathrm { i . e . }$ $B _ { \mathrm { r } } \ll f _ { \mathrm { r } } ,$ , and that target displacement during a chirp is much smaller than the wavelength, i.e., $v T \ll \lambda _ { \mathrm { r } }$ . Based on these assumptions, the signal in (7) can be approximated as [1]

$$
\begin{array} { r } { \widetilde { r } _ { \mathrm { r } } ( t , k T ) = \gamma _ { \mathrm { r } } e ^ { j 2 \pi \left[ - \frac { 2 d _ { 0 } } { c } \frac { B _ { \mathrm { r } } } { T } t + 2 f _ { D } k T - \frac { 2 d _ { 0 } } { c } f _ { \mathrm { r } } \right] } + w ( t , k T ) } \end{array}\tag{8}
$$

<sup>1</sup>The sampling rate satisfies $B _ { \mathrm { c } } \ \leq \ f _ { \mathrm { s } } ,$ , which is generally on the order of $1 0 - 5 0$ MHz for automotive radars.

![](images/789a62c8e9420a1b8783acb59c2015e4dd143277154386c63333329efc90857d.jpg)  
(a)

![](images/caa5cb0253dfd53a727bde5eb3d7e61ec28ce48eaa9c717d3ed6d6388f2e1b7e.jpg)  
(b)  
Fig. 3: Scenarios for investigation of a) R2R interference, b) C2R interference experienced at Vehicle 1 and R2C interference at Vehicle 2.

where $f _ { D } = v f _ { \mathrm { r } } / c$ is the Doppler shift. A common approach for range-Doppler retrieval in FMCW radar is to compute the fast Fourier transform (FFT) of the signal in (8) over both fast time t and slow time k (with windowing functions [44, Ch. 5.3.1]), yielding peaks at frequencies corresponding to $d _ { 0 }$ and $f _ { D }$ , respectively, and detect the peaks in the range-Doppler domain.

2) Communication Receiver: During communication mode, the complex baseband received signal is [42]

$$
\widetilde { r _ { \mathrm { c } } } ( t ) = \gamma _ { \mathrm { c } } x ( t - d / c ) e ^ { j 2 \pi \left( f _ { D , \mathrm { c } } t - f _ { \mathrm { c } } d _ { 0 } / c \right) } + w ( t )\tag{9}
$$

where

$$
\gamma _ { \mathrm { c } } = \sqrt { P _ { \mathrm { c } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \lambda _ { \mathrm { c } } ^ { 2 } / ( 4 \pi d ) ^ { 2 } }\tag{10}
$$

under the assumption of free-space propagation environment [42], [45], $f _ { D , \mathrm { c } } ~ = ~ v f _ { \mathrm { c } } / c$ and $\lambda _ { \mathrm { c } }$ is the wavelength of the communications carrier.

## IV. INTERFERENCE ANALYSIS

To gain understanding in the three types of interference (R2R, C2R and R2C), we consider two simple scenarios given in Fig. 3(a)–3(b). For the R2R interference, the scenario given in Fig. 3(a) demonstrates a case where two front-end radars of two vehicles illuminate each other’s field of view (FoV). For the C2R and R2C case, we consider the threevehicle scenario given in Fig. 3(b), where the rear-end radar of Vehicle 3 sends communication data to Vehicle 2 and receives acknowledgements<sup>3</sup> (ACK), while the front-end radar of Vehicle 1 is simultaneously performing radar sensing. This ends up with C2R interference at Vehicle 1, where the ACKs of communication disturb the radar signal of Vehicle 1. R2C interference is analyzed for the same scenario at Vehicle 2, where the communication data is affected by the radar of Vehicle 1.

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>SIR</td><td rowspan=1 colspan=1>Probability</td></tr><tr><td rowspan=1 colspan=1>R2R</td><td rowspan=1 colspan=1> $\overline { { \mathcal { O } ( \sigma / d ^ { 2 } ) } }$ </td><td rowspan=1 colspan=1> $\overline { { 4 U B _ { \mathrm { m a x } } / B _ { \mathrm { r } } } }$ </td></tr><tr><td rowspan=1 colspan=1>C2R</td><td rowspan=1 colspan=1> $\overrightarrow { \mathcal { O } ( P _ { \mathrm { r } } \sigma / ( P _ { \mathrm { c } } d ^ { 2 } ) ) }$ </td><td rowspan=1 colspan=1> $\overline { { U \operatorname* { m i n } \{ B _ { \mathrm { m a x } } + B _ { \mathrm { c } } , B _ { \mathrm { r } } \} / B _ { \mathrm { r } } } }$ </td></tr><tr><td rowspan=1 colspan=1>R2C</td><td rowspan=1 colspan=1> $\overline { { \mathcal { O } ( P _ { \mathrm { c } } / P _ { \mathrm { r } } ) } }$ </td><td rowspan=1 colspan=1> ${ \overline { { U \operatorname* { m i n } \{ B _ { \mathrm { c } } , B _ { \mathrm { r } } \} / B _ { \mathrm { r } } } } }$ </td></tr></table>

TABLE I: Signal-to-interference ratio and probability of interference values for the different interference cases, where radar target and interference sources are located at the same distance $d ,$ and U is the radar duty cycle.

We assume that all FMCW waveform parameters (frame time, chirp duration, slope, bandwidth, number of chirps per frame, duty cycle, etc.) are the same for all radars for the sake of simplicity. In all analyses, signals are assumed to be in the main beam of the respective antennas so that the antenna gains are taken equal. Table I provides a concise comparison of the different types of interference, which will be derived in the subsequent sections.

## A. R2R Interference Analysis

R2R interference might occur in two different ways, both of which are considered in this article: (i) direct line-ofsight (LoS) interference, (ii) bistatic radar returns or reflected interference, when either a victim vehicle receives a reflected interfering radar signal from another vehicle or one RadChat unit at the victim vehicle receives a reflected radar return of another RadChat unit on the same victim vehicle.

1) Impact and Power of R2R Interference: R2R interference affects radar performance in a number of ways: it leads to an increase of the effective noise floor or false alarms (ghost targets), which are apparent targets with high intensity that are not actually present. In our system where all radars have the same parameters, ghost targets will be the dominant effect, while effective noise floor increase occurs when radars have different chirp parameters [46].

Example: The range-Doppler plot illustrating the R2R interference for two vehicles approaching with v = 30 m/s relative speed at d = 100 m is given in Fig. 4. A ghost target with a high intensity is observed at half-speed and half distance, i.e. v = 15 m/s and d = 50 m.

If the interference comes from a LOS transmission, noting that the desired radar signal is always a backscattered signal, the signal to interference ratio (SIR) is

$$
\mathrm { S I R } _ { \mathrm { R 2 R } } = \frac { \gamma _ { \mathrm { r } } ^ { 2 } } { P _ { \mathrm { r } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \lambda _ { r } ^ { 2 } / ( 4 \pi d _ { I } ) ^ { 2 } } = \frac { \sigma d _ { I } ^ { 2 } } { 4 \pi d ^ { 4 } }\tag{11}
$$

where d is the target distance and $d _ { I }$ is the distance to the interferer. Since $d _ { I }$ and $d$ are of the same order, the interference is much stronger than the desired signal.

![](images/e09a1209cf109a053e4946a781ff95c80e0ce2afeffde48312aeb67c32a23a84.jpg)  
Fig. 4: Radar range-Doppler map in the presence of R2R interference, where $d \bar { = } 1 0 0 \mathrm { m } , v = \bar { 3 } 0$ m/s and $\begin{array} { r } { P _ { \mathrm { r } } = 5 \mathrm { m } \bar { \bf W } . } \end{array}$

2) Probability of R2R Interference: Let us assume that starting times of FMCW chirps are uniformly distributed for all vehicles. Vehicle 1 in Fig. 3(a) transmits the radar signal $s _ { \mathrm { r } } ( t )$ in (1) and Vehicle 2, which is d apart from Vehicle 1, transmits its FMCW signal with a delay τ with respect to Vehicle 1. The probability of R2R interference $( P _ { \mathrm { R 2 R } } ^ { \mathrm { i n t } } )$ is the probability that the received signal at the victim radar lies in the band $f _ { \mathrm { r } } + B _ { \mathrm { r } } T / t + [ - B _ { \mathrm { m a x } } , 0 ]$ given that the victim radar starts its transmission at time t. Hence, R2R interference occurs when at least one chirp of the victim radar is affected and $P _ { \mathrm { R 2 R } } ^ { \mathrm { i n t } }$ is the same as the fraction of the vulnerable time over the frame time, which is explained below.

Definition 1 (Vulnerable period V [36]). Given a victim vehicle radar that starts an FMCW transmission at time $t = 0$ and a facing vehicle radar with overlapping field-of-view that starts a transmission at time $t \ = \ \tau _ { : }$ , the vulnerable period V is the set of τ values within a chirp duration, for which interference to the victim vehicle radar occurs.

To quantify the interference, we can thus determine the vulnerable period and then compute the probability of interference occurring within the vulnerable period.

Proposition 2. Considering an interferer (either direct or reflected) at any distance up to $\alpha _ { d } 2 d _ { m a x }$ and at any relative velocity up $t o \pm v _ { m a x }$ , the vulnerable period for R2R interference is given by

$$
V \approx [ - \alpha _ { d } T _ { m a x } , T _ { m a x } ]\tag{12}
$$

where $T _ { m a x } = T B _ { m a x } / B _ { r } = 2 d _ { m a x } / c ,$ is the maximum delay of (intended) radar reflections and $\alpha _ { d }$ is a constant determined by the longest interference path.

## Proof: See Appendix A.

We note that the vulnerable period depends on the distance of the longest interference path. This implies that in sparse VANETS (where $\alpha _ { d } \gg 1 )$ , we have a long vulnerable period, but few interferers, while in dense VANETS (where $\alpha _ { d } \leq 1$ due to signal blockage), we have a short vulnerable period, but many potential interferers.

An FMCW radar transmits N successive chirps and R2R interference occurs if any two chirps of two different vehicles overlap in the vulnerable period of at least a single chirp. Hence, any radar chirp sequence starting $( N \mathrm { ~ - ~ } 1 ) T$ prior up to the end of the radar transmission may result in R2R interference due to one or more chirps overlapping. The vulnerable period taking a whole radar frame into account is

$$
V ^ { ( f ) } = \cup _ { k = - ( N - 1 ) } ^ { N - 1 } \left[ k T - \alpha _ { d } T _ { \operatorname* { m a x } } , k T + T _ { \operatorname* { m a x } } \right] ,\tag{13}
$$

and the vulnerable duration is $\vert V ^ { ( f ) } \vert ~ = ~ ( 2 N - 1 ) ( 1 +$ $\alpha _ { d } ) T _ { \mathrm { m a x } } \approx 2 ( 1 + \alpha _ { d } ) N T _ { \mathrm { m a x } } ,$ , since generally $N \gg 1$

The probability of R2R interference among two vehicles is easily found as

$$
P _ { \mathrm { R 2 R } } ^ { \mathrm { i n t } } = \frac { | V ^ { ( f ) } | } { T _ { f } } = \frac { ( 1 + \alpha _ { d } ) ( 2 N - 1 ) U B _ { \mathrm { m a x } } } { N B _ { \mathrm { r } } } \approx \frac { 2 ( 1 + \alpha _ { d } ) U B _ { \mathrm { m a x } } } { B _ { \mathrm { r } } }\tag{14}
$$

where $U = N T / T _ { f } \in \mathsf { ( 0 , 1 ] }$ is the radar duty cycle, indicating that R2R interference is minimized with reduced radar bandwidth of interest $B _ { \mathrm { m a x } }$ (or longer chirps).

3) Example: The R2R interference probability in (14) is verified in Fig. 5 with simulations for two radars within $2 d _ { \mathrm { m a x } }$ distance $( \mathrm { i } . \mathrm { e } . , \alpha _ { d } = 1 ) )$ for varying $B _ { \mathrm { m a x } }$ and U. $1 0 ^ { 6 }$ Monte Carlo simulations are performed using the parameters in Table II by assuming uniform distribution of radar starting times. For each simulation, we check if the interference is present within the bandwidth of the radar for at least one chirp within the frame. The number of occurrences of interference over the total number of simulations is the simulated interference probability. The simulations are observed to exactly match analysis in (14). A verification of the vulnerable period for various victim-interferer distances is also presented in [36].

![](images/42c32b75ecc8b67c95345dbc31f6dc269dd7aa770c4edc732a8eebbc2df78978.jpg)  
Fig. 5: Verification of R2R interference probability with simulations for $B r =$ 1 GHz and $N = 9 9$ for two radars.

## B. C2R Interference Analysis

To provide a theoretical analysis of C2R interference, we focus on a vehicular communication and sensing environment as depicted in Fig. 3(b), where Vehicle 1 receives simultaneously the communications interference and the desired radar return from Vehicle 2.

1) Impact and Power of C2R Interference: The interference will be spread over the entire bandwidth and lead to an increase of the effective noise floor. As the desired radar signal is always a backscattered signal while the interference can emanate from a direct transmission, the signal to interference ratio is

$$
\mathrm { S I R } _ { \mathrm { C 2 R } } = \frac { P _ { \mathrm { r } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \sigma \lambda ^ { 2 } / ( ( 4 \pi ) ^ { 3 } d ^ { 4 } ) } { P _ { \mathrm { c } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \lambda _ { \mathrm { c } } ^ { 2 } / ( 4 \pi d _ { I } ) ^ { 2 } } \approx \frac { P _ { \mathrm { r } } \sigma d _ { I } ^ { 2 } } { P _ { \mathrm { c } } 4 \pi d ^ { 4 } }\tag{15}
$$

When $d _ { I }$ and d are of the same order (which is typically the case if the communication transmitter of the vehicle to be

detected interferes with the victim radar), the SIR expression in (15) can be rewritten as

$$
\mathrm { S I R } _ { \mathrm { C 2 R } } \approx \frac { P _ { \mathrm { r } } \sigma } { P _ { \mathrm { c } } 4 \pi d ^ { 2 } } \ .\tag{16}
$$

This means that when communication and radar use similar transmission power, the interference will be much stronger than the desired signal since $4 \pi d ^ { 2 } \gg \sigma$ for typical RCS values at 77 GHz [43]. On the other hand, the effect of C2R interference on radar performance becomes less severe when (i) communication operates at a much smaller power than radar (i.e., $P _ { \mathrm { c } } \ll P _ { \mathrm { r } } \sigma / ( 4 \pi d ^ { 2 } ) \ll P _ { \mathrm { r } } )$ , and/or (ii) the interferer gets closer to the victim radar $( \mathrm { i . e . , }$ for small d).

2) C2R Interference Time Ratio: We investigate the percentage of time an FMCW radar receiver is disrupted by interference from a spectrally coexistent communications transmitter (i.e., C2R interference time ratio). Let $x ( t )$ denote the transmitted baseband communications signal from Vehicle 2, as defined in (4). Assume that Vehicle 2 continuously transmits data. Then, the received bandpass signal at Vehicle 1 radar in the presence of communications interference from Vehicle 2 can be written as [24], [47]

$$
r ( t ) = r _ { \mathrm { r } } ( t ) + \gamma _ { \mathrm { c } } x ( t ) e ^ { j 2 \pi [ ( f _ { \mathrm { c } } + f _ { D , \mathrm { c } } ) t - f _ { \mathrm { c } } d _ { 0 } / c ] }\tag{17}
$$

where $r _ { \mathrm { r } } ( t )$ is the received FMCW waveform of the form (5). After mixing as defined in Sec. III-C1, the baseband communications signal during chirp k at the radar receiver is given by

$$
\begin{array} { r } { x _ { \mathrm { c } } ( t , k T ) = \gamma _ { \mathrm { c } } x ( k T + t ) e ^ { j \theta _ { k } } e ^ { j 2 \pi \left( f _ { \mathrm { c } } + f _ { D , \mathrm { c } } - f _ { \mathrm { r } } + k B _ { \mathrm { r } } - \frac { B _ { \mathrm { r } } t } { 2 T } \right) t } } \end{array}\tag{18}
$$

where $\theta _ { k }$ is a phase that is irrelevant to the subsequent analysis. The instantaneous frequency of the baseband communications interference in (18) during chirp k is thus

$$
f ( k T , t ) = f _ { \mathrm { c } } + f _ { D , \mathrm { c } } - f _ { \mathrm { r } } + k B _ { \mathrm { r } } - B _ { \mathrm { r } } t / T\tag{19}
$$

with the bandwidth $B _ { \mathrm { c } }$ as defined in (4). Hence, the radar signal is subjected to communication interference when $f ( k T , t ) - B _ { \mathrm { c } } / 2 \leq 0$ and $f ( k T , t ) + B _ { \mathrm { c } } / 2 \geq - B _ { \mathrm { m a x } }$ . In turn, this implies non-zero interference for chirp k when

$$
t \in V _ { k , \mathrm { C 2 R } } \triangleq \left\{ t  { | } \ T _ { k , \mathrm { C 2 R } } \leq t \leq  { \widetilde { t } } _ { k , \mathrm { C 2 R } } + \Delta t _ { \mathrm { C 2 R } } \right\}\tag{20}
$$

over the interval [kT, (k + 1)T ], where

$$
\widetilde { t } _ { k , \mathrm { C 2 R } } = \biggl ( k + \frac { f _ { \mathrm { c } } + f _ { D , \mathrm { c } } - f _ { \mathrm { r } } - B _ { \mathrm { c } } / 2 } { B _ { \mathrm { r } } } \biggr ) T\tag{21}
$$

$$
\Delta t _ { \mathrm { C 2 R } } = \bigg ( \frac { \operatorname* { m i n } \{ B _ { \mathrm { m a x } } + B _ { \mathrm { c } } , B _ { \mathrm { r } } \} } { B _ { \mathrm { r } } } \bigg ) T .\tag{22}
$$

Hence, (20) defines a communications vulnerable period of $\Delta t _ { \mathrm { C 2 R } }$ seconds over a chirp duration of T seconds. Different from Definition 1 in Sec. IV-A, the radar receiver periodically suffers from this interference irrespective of the delay between radar and communication transmission times<sup>4</sup>. Using (22), the C2R interference time ratio is given by

$$
P _ { \mathrm { C 2 R } } ^ { \mathrm { i n t } } = \frac { \operatorname* { m i n } \{ B _ { \mathrm { m a x } } + B _ { \mathrm { c } } , B _ { \mathrm { r } } \} } { B _ { \mathrm { r } } } U .\tag{23}
$$

![](images/34fd95153f35e4a88fa5ea7b601b7f51f0d84e4627af22c9b9fe151fa6276f66.jpg)  
Fig. 6: Radar receiver operating characteristic curves for various values of distance d in the absence and presence of communications interference with $d _ { I } = d ,$ , where $P _ { \mathrm { r } } = 5 \mathrm { m W } ,$ $\mathrm { \dot { P } _ { c } } = 5 \mathrm { m W }$ $f _ { \mathrm { r } } = 7 7 \mathrm { G H z }$ , $f _ { \mathrm { c } } = 7 7 . 5 \mathrm { G H z } .$ $B _ { \mathrm { r } } = 1 { \mathrm { G H z } }$ and $B _ { \mathrm { c } } ~ = ~ 4 0 \mathrm { M H z }$ Solid (dashed) lines correspond to interference-free (interference) cases.

The time percentage of C2R interference can be minimized by choosing a small communication bandwidth $B _ { \mathrm { c } }$ or small radar bandwidth of interest $B _ { \mathrm { m a x } }$ or a high radar (sweep) bandwidth $B _ { \mathrm { r } }$

3) Example: We demonstrate the effect of interferer distance on probability of detection, $P _ { \mathrm { d } } .$ , and probability of false alarm, $P _ { \mathrm { f a } }$ , in Fig. 6, where $P _ { \mathrm { d } }$ is calculated from [44, Eq. (6.36)]

$$
P _ { \mathrm { d } } = { \frac { 1 } { 2 } } \mathrm { e r f c } \left( \mathrm { e r f c } ^ { - 1 } \left( 2 P _ { \mathrm { f a } } \right) - \sqrt { \mathrm { S I N R } } \right)\tag{24}
$$

with SINR representing the signal-to-interference-plus-noiseratio of the range-Doppler cell containing the desired target echo for a given power and distance of interference. Due to $d ^ { 2 }$ and $d ^ { 4 }$ scaling laws, respectively, for communication and radar power attenuation, an interfering car (i.e., Vehicle 2 in Fig. 3(b)) at a larger distance induces more severe degradation in radar detection performance. Hence, in agreement with (16), spectral coexistence of FMCW radar and communication systems without significant performance reduction in radar receiver is possible only for close interferers (e.g., less than 50 m) in a scenario with $P _ { \mathrm { r } } = P _ { \mathrm { c } } = 5 \mathrm { m W } , B _ { \mathrm { r } } = 1$ GHz and $B _ { \mathrm { c } } = 4 0 \mathrm { M H z } . ^ { 5 }$

## C. R2C Interference Analysis

In this section, we investigate R2C interference effects on communication receivers. First, we provide a received signal model in the presence of FMCW radar interference. Then, we analyze the symbol error probability of a 16-QAM system under different parameter settings.

1) Impact and Power of R2C Interference: The FMCW radar signal will temporarily interfere with the communication signal. The SIR is now

$$
\mathrm { S I R } _ { \mathrm { R 2 C } } = \frac { P _ { \mathrm { c } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \lambda _ { \mathrm { c } } ^ { 2 } / ( 4 \pi d ) ^ { 2 } } { P _ { \mathrm { r } } G _ { \mathrm { t x } } G _ { \mathrm { r x } } \lambda ^ { 2 } / ( 4 \pi d _ { I } ) ^ { 2 } } \approx \frac { P _ { \mathrm { c } } d _ { I } ^ { 2 } } { P _ { \mathrm { r } } d ^ { 2 } } .\tag{25}
$$

Since $d _ { I }$ and d are of the same order and $P _ { \mathrm { r } }$ is generally larger than $P _ { \mathrm { c } }$ , the interference will be strong and cause loss of a fraction of the data.

![](images/2f220211f0039003b0c11810e574a72ba08a851e74dcdd70129008be47cde4e6.jpg)  
Fig. 7: Symbol error probability with respect to communication power for a 16-QAM scenario with and without radar interference for different values of communication bandwidth, where $d _ { I } = d = 1 0 0 \mathrm { { n } }$ m, $P _ { \mathrm { r } } = 5 \mathrm { m W } , f _ { \mathrm { r } } =$ 77 GHz, $f _ { \mathrm { c } } = 7 7 . 8$ GHz and $B _ { \mathrm { r } } = 1 { \mathrm { G H z } }$

2) R2C Interference Time Ratio: Consider the R2C interference scenario in Fig. 3(b), where Vehicle 2 receives communications signal from Vehicle 3 while simultaneously being corrupted by radar interference from Vehicle 1. The relative velocity of Vehicle 1 and Vehicle 2 is denoted by v<sub>I</sub> so that $d _ { I } = d _ { I , 0 } - v _ { I } t$ for an initial distance $d _ { I , 0 }$ . Using a similar type of analysis as for the C2R interference, the baseband radar interference signal due to the kth chirp of Vehicle 1 at the communications receiver of Vehicle 2 can be written as

$$
\begin{array} { r } { x _ { r } ( t , k T ) = \widetilde { \gamma } _ { r } e ^ { j \widetilde { \theta } _ { k } } e ^ { j 2 \pi \left[ ( f _ { \mathrm { r } } + f _ { D , I } - f _ { \mathrm { c } } ) t + \frac { B _ { \mathrm { r } } } { 2 T } ( t - k T - \frac { d _ { I , 0 } } { c } ) ^ { 2 } \right] } } \end{array}\tag{26}
$$

where $\widetilde { \gamma } _ { r }$ and $\widetilde { \theta } _ { k }$ are quantities irrelevant to our analysis, and $f _ { \cal D , I } ~ = ~ v _ { I } f _ { \mathrm { r } } / c .$ The signal in (26) is filtered out at the communications receiver when its instantaneous frequency is outside the interval $[ - B _ { \mathrm { c } } / 2 , B _ { \mathrm { c } } / 2 ]$ . Therefore, the k-th chirp of the radar interferes with the communication signal during a time, $V _ { k , \mathrm { R 2 C } }$ , the radar vulnerable period at the communications receiver, which can be expressed as

$$
V _ { k , \mathrm { R 2 C } } \triangleq \left\{ t \mid \widetilde { t } _ { k , \mathrm { R 2 C } } \leq t \leq \widetilde { t } _ { k , \mathrm { R 2 C } } + \Delta t _ { \mathrm { R 2 C } } \right\}\tag{27}
$$

where $\widetilde { t } _ { k , \mathrm { R 2 C } }$ and $\Delta t _ { \mathrm { R 2 C } }$ are defined as

$$
\widetilde { t } _ { k , \mathrm { R 2 C } } = \biggl ( k + \frac { f _ { \mathrm { c } } - f _ { \mathrm { r } } - f _ { D , I } - { B _ { \mathrm { c } } } / { 2 } } { B _ { \mathrm { r } } } \biggr ) T \ ,\tag{28}
$$

$$
\Delta t _ { \mathrm { R 2 C } } = \frac { \operatorname* { m i n } \{ B _ { \mathrm { c } } , B _ { \mathrm { r } } \} } { B _ { \mathrm { r } } } T .\tag{29}
$$

The R2C interference time ratio is then given by

$$
P _ { \mathrm { R 2 C } } ^ { \mathrm { i n t } } = \frac { \operatorname* { m i n } \{ B _ { \mathrm { c } } , B _ { \mathrm { r } } \} } { B _ { \mathrm { r } } } U\tag{30}
$$

which can be minimized by choosing small communication bandwidths or large radar bandwidths.

3) Example: Based on the scenario in Fig. 3(b), we investigate the symbol error rate (SER) of the communications receiver at Vehicle 2 versus the transmit power of Vehicle 3 in Fig. 7 for two different communication bandwidths<sup>6</sup>. The figure shows Monte Carlo simulation results of a 16-QAM system with and without radar interference along with the (semi-)analytically derived $P _ { \mathrm { { s } } }$ and $P _ { \mathrm { s , i n t } }$ values, where $P _ { \mathrm { s , i n t } }$ constitutes an upper bound on the theoretical SER value in the presence of radar interference, computed as<sup>7</sup>

![](images/eb5a74950b773c81bdb28c45701c8d3446836d44e186430b277568d386d6981a.jpg)  
Fig. 8: Interference-related degradation in symbol error probability with respect to communication power for a 16-QAM scenario for different values of communication bandwidth, where $d _ { I } ~ = ~ d ~ = ~ 1 0 0$ m, $P _ { \mathrm { { r } } } ~ = ~ 5 \mathrm { { m W } } ,$ $f _ { \mathrm { r } } = 7 7$ GHz, $f _ { \mathrm { c } } = 7 7 . 8$ GHz and $B _ { \mathrm { r } } = 1 \mathrm { G H z }$

$$
P _ { \mathrm { s , i n t } } = \alpha _ { \mathrm { i n t } } + P _ { \mathrm { s } } \left( 1 - \alpha _ { \mathrm { i n t } } \right)\tag{31}
$$

with $P _ { \mathrm { { s } } }$ and $\alpha _ { \mathrm { i n t } }$ denoting, respectively, the SER of 16- QAM without radar interference [42, Eq. (6.23)] and the ratio of symbols that are subjected to interference<sup>8</sup>. We also show $P _ { \mathrm { s , i n t } } - P _ { \mathrm { s } } ,$ i.e., SER performance degradation due to interference, in Fig. 8. From the figures, it is observed that larger communication bandwidths lead to higher interferencerelated degradation in SER performance due to an increase in the R2C interference time ratio, as stated in (30). In addition, the effect of radar interference becomes more severe as the SINR increases, in the sense that additional communication power in the interference case that is required to attain the same SER value as the interference-free case gets larger. At very high SINR values, $\alpha _ { \mathrm { i n t } }$ would become zero, implying that the SER performance of the interference case converges to that of the interference-free case. We conclude from Fig. 7 that in a scenario where radar and communication transmitters operate at the same power (i.e., $P _ { \mathrm { { r } } } = P _ { \mathrm { { c } } } = 5 \mathrm { { m W } ) }$ , R2C interference from an FMCW radar with $B _ { \mathrm { r } } = 1 { \mathrm { G H z } }$ leads to unacceptably high SER levels at a communication receiver with $B _ { \mathrm { c } } = 2 0 \mathrm { M H z }$ and $B _ { \mathrm { c } } = 4 0 \mathrm { M H z }$

## D. Interference Analysis Outcome

The communication SER performance loss due to radar interference (R2C) is non-negligible for $P _ { \mathrm { c } } / P _ { \mathrm r }$ ≈ 1 with $B _ { c } = 2 0 ~ \mathrm { M H z }$ and $B _ { c } = 4 0$ MHz (Fig. 7). The SER performance can be enhanced by increasing the $P _ { \mathrm { c } } / P _ { \mathrm r }$ ratio, which, in turn, leads to degradation of $\mathrm { S I R } _ { \mathrm { C 2 R } }$ (Table I) and thus radar detection performance (Fig. 6). This suggests that FMCW radar sensing and communication with similar powers should not occupy the same time-frequency resources. Additionally, R2R interference can be avoided if FMCW chirp sequences start transmission during non-overlapping vulnerable periods.

![](images/ce4132a8318beb066060177f7a56f5df310fe4ae51189da55c1739d83ba82e69.jpg)  
Fig. 9: Summary of the layered architecture of RadChat.

## V. RADCHAT: PROTOCOL DESCRIPTION

RadChat is proposed as a distributed radar and communication cooperation protocol, which avoids R2R interference by scheduling radar sensing to non-overlapping vulnerable periods and avoids R2C/C2R interferences by using a separate communication control channel in order to ensure non-conflicting time-frequency blocks for communication and radar. The layered architecture of RadChat is summarized in Fig. 9. A RadChat unit is responsible of data link control (DLC), MAC sublayer and PHY layer functions. Upper layer functions are assumed to be processed at a central unit at each vehicle, which combines data of all RadChat units, which are co-located on a vehicle looking toward different directions. The main service provided by the DLC layer is scheduling of radars, i.e. assigning non-overlapping vulnerable periods to radars, and is an unacknowledged connectionless service. Broadcast control packets are used to schedule radar packets<sup>9</sup> at non-overlapping time slots. In addition to scheduling radars, the DLC can provide basic communication services, but these are outside the scope of the current work.

Given that the PHY layer operates as described in the previous sections, the MAC layer of RadChat operates by FDM/rTDMA/cCSMA, which is a scheme based on frequency division multiplexing (FDM) between radar and communication, time division multiple access for radar transmissions (rTDMA), and carrier sense multiple access for communications (cCSMA). Fig. 10 illustrates the division of the frequency-time domain for the proposed DLC service w.r.t. two specific RadChat units $r _ { i }$ and $r _ { j }$ . Radars are scheduled by assigning each a different rTDMA slot, where rTDMA slots are defined as radar slots with disjoint vulnerable periods.

## A. Terminology and Assumptions

1) Network: For a general but fixed VANET topology, RadChat unit $r _ { i }$ is connected to/facing the RadChat unit $r _ { j }$ if $r _ { i }$ is able to receive/transmit communication signals from/to $r _ { j }$ , assuming symmetric communication links. Links may be established through LOS or reflected paths. Let $S _ { X }$ denote the set of RadChat units mounted on vehicle X , which are connected to one central processing unit at vehicle $X .$ Each $r _ { i } ~ \in ~ S _ { \mathrm { X } }$ uses a different rTDMA slot to handle R2R self-interference, which is the R2R interference among radars mounted on the same vehicle. All vehicles use a common radar band B and a common communication band $B _ { c } < B _ { \operatorname* { m a x } } .$ , in order to be able to reuse the radar ADC. We assume equal radar and communication transmit powers $( P _ { \mathrm { { c } } } ~ = ~ P _ { \mathrm { { r } } } )$ for simplicity and to ensure that RadChat provides long enough communication range to communication with all interferers within distance $\alpha _ { d } 2 d _ { \mathrm { m a x } }$ . Extensions to dynamically changing topologies, as well as power control, which adapts these powers independently for all RadChat units, are left for future work.

![](images/ac0b08b3f932bfdf9b176710522b3da3bd7b6a93ed503d775357dc3e96abd7e3.jpg)  
Fig. 10: RadChat Scheduling Radars scheme: FDM / rTDMA / cCSMA

2) Timing: We introduce time slots $T _ { k }$ (Fig. 10) of duration $( N { + } 1 ) T \leq T _ { f }$ , which corresponds to the duration of N chirps plus one idle chirp time accounting for the overflow of time shifted rTDMA slots. Let $U ^ { \prime } = ( N + 1 ) T / T _ { f }$ be defined as the modified radar duty cycle, then a radar frame is divided into $1 / U ^ { \prime }$ time slots. This slotted time is set to provide nonoverlapping chirp sequences within a radar frame and thereby maximize the number of vehicles with no mutual interference, denoted by $M _ { \mathrm { m a x } } \leq \lfloor 1 / U ^ { \prime } \rfloor \lfloor B _ { \mathrm { r } } / ( ( 1 + \alpha _ { d } ) B _ { \mathrm { m a x } } ) \rfloor$ . Each time slot $T _ { k }$ is further divided to slots called SlotTimes of duration $\delta ,$ which are large enough to detect channel activity by the carrier-sensing function of the CSMA mechanism. Vehicles are assumed to synchronize their clocks using GPS.

3) Data Structure: Each RadChat unit $r _ { i }$ on vehicle X has several MAC state variables that are broadcast to other vehicles:

$r _ { i } . \mathrm { I D } { \mathrm { : } }$ an identifier of the time reference, initialized to the vehicle index X.

$r _ { i } . S \mathrm { I } ;$ an rTDMA slot index in the local time reference, initialized to 0. During operation, $r _ { i } . { \mathrm { S I } } \in \{ 1 , \dots , M _ { \mathrm { m a x } } \}$

$r _ { i } . t _ { \mathrm { r s } } \mathrm { : }$ a radar start time, initialized uniformly in $[ 0 , T _ { f } ]$ incremented by $T _ { f }$ every frame.

$r _ { i }$ .strength: a priority indicator, coupled to $r _ { i } . \mathrm { I D }$ , initialized to 0.

All RadChat units mounted on the same vehicle use the same ID and strength values, whereas SI and $t _ { \mathrm { r s } }$ are specific to each RadChat unit assigned by the central processor at vehicle $X$ We will denote the set of all of the rTDMA slot indices used by RadChat units mounted on the vehicle X by $S _ { \mathrm { X } } . S \mathrm { I }$ , whereas the set of all of the radar start times are denoted by $S _ { \mathrm { X } } . t _ { \mathrm { r s } }$

Due to the distributed nature of the algorithm, each vehicle X will assign rTDMA slots according to its own time frame initially. The couple $\left( r _ { i } . \mathrm { I D } , r _ { i } . \mathrm { S I } \right)$ specifies a unique rTDMA slot index for all radars that have the same time reference $r _ { i } . \mathrm { I D }$ . The variable $r _ { i }$ .strength is used to give priority to the time reference which is shared the most in the network, in order to avoid fluctuations among different time references.

Communication functions are common to all $r _ { i } ~ \in ~ S _ { \mathrm { X } }$ Hence, a base RadChat unit $r _ { i } ^ { * } \in S _ { \mathrm { X } }$ on vehicle X is selected according to which timing of communication functions are conducted. Each vehicle also keeps track of these MAC state variables of the base RadChat unit $r _ { i } ^ { * }$ during operation, which are not broadcast:

$r _ { i } ^ { * }$ .counter: a binary exponential backoff (BEB) counter, initialized by a random integer rand $( [ 0 , 2 ^ { b } W _ { 0 } - 1 ] )$ , where b is the backoff stage and $W _ { 0 }$ is the maximum contention window size; b is incremented upon each busy carrier sense until $b \leq B$ , where B is the maximum backoff stage. b is reset at the end of $T _ { k - 1 }$

$r _ { i } ^ { * } . t _ { \mathrm { c s } } { \mathrm { : } }$ a communication starting time, initialized to $r _ { i } ^ { * } . t _ { \mathrm { c s } } = r _ { i } ^ { * } . t _ { \mathrm { r s } } - ( N + 1 ) T - T _ { \mathrm { p k t } } + \delta r _ { i } ^ { * }$ .counter, where $T _ { \mathrm { p k t } }$ is the duration of a control packet. $r _ { i } ^ { * } . t _ { \mathrm { c s } }$ is updated whenever the radar start time of the base RadChat unit on vehicle X, is changed.

## B. MAC Operation

In order to assign non-overlapping rTDMA slots among facing RadChat units, non-persistent CSMA with BEB is employed. rTDMA slots in $T _ { k }$ are generally determined by communication contention during slot $T _ { k - 1 } ~ ( \mathrm { F i g . ~ } 1 0 ) ^ { 1 0 }$ . Control packets are transmitted if the channel is sensed idle for one SlotTime δ or random BEB is employed if channel is sensed busy. Each vehicle X may prefer to allocate all radar transmissions of its mounted RadChat units in the same time slot $T _ { k } , \ S _ { \mathrm { X } } . t _ { \mathrm { r s } } \ \in \ T _ { k }$ (if the number of RadChat units on a single vehicle is $\leq \lfloor { B _ { \mathrm { r } } } / ( ( 1 + \alpha _ { d } ) B _ { \mathrm { m a x } } ) \rfloor )$ . It is not necessary to squeeze all radars of a vehicle to a single time slot $T _ { k } ,$ however at least one time slot $T _ { k - 1 }$ should be empty with no radars, so that it can be used for communication jointly by all $r _ { i } \in S _ { \mathrm { X } }$

Each vehicle X, which has a set of random radar start times $S _ { \mathrm { X } } . t _ { \mathrm { r s } } ,$ selects a contention period, preferably the prior time slot $T _ { k - 1 }$ where most of the radar start times reside in $T _ { k }$ and selects a base RadChat unit $r _ { i } ^ { * } , r _ { i } ^ { * } . t _ { \mathrm { r s } } \in T _ { k }$ according to which communication start time $r _ { i } ^ { * } . t _ { \mathrm { c s } }$ is calculated. $\forall r _ { i } \in S _ { \mathrm { X } }$ transmit a single communication control packet during $T _ { k - 1 } .$ This control packet is broadcast to all RadChat units connected to the Vehicle $X$ (as if omni-directional communication) and contains the following information: identity of the transmitter $( r _ { i } )$ , time reference frame $( r _ { i } . \mathrm { I D } )$ and the set of all rTDMA slot indices of RadChat units mounted on vehicle X $( S _ { \mathrm { X } } . S \mathrm { I } )$ , strength of this time reference frame $( r _ { i } . { \mathrm { s t r e n g t h } } )$ the base RadChat unit’s radar starting time and its slot index $( r _ { i } ^ { * } . t _ { \mathrm { r s } } , r _ { i } ^ { * } . \mathrm { S I } )$ . MAC functions of RadChat are presented next.

• RadChat Carrier Sensing: A RadChat unit $r _ { i }$ intends to start radar transmission at $r _ { i } . t _ { \mathrm { r s } } ~ \in ~ T _ { k }$ in Fig. 10. This

RadChat unit carrier-senses the communication channel $B _ { \mathrm { c } }$ during the entire radar frame except during $T _ { k }$ (as it is transmitting radar), and receives incoming control packets.

• RadChat Transmission at $T _ { k - 1 } .$ If a control packet transmission is scheduled at $r _ { i } ^ { * } . t _ { \mathrm { c s } } ~ \in ~ T _ { k - 1 }$ , carrier sensing is employed during $T _ { k - 1 } .$ . The control packet is sent if channel is sensed as idle, or backoff is employed if channel is sensed as busy (and $r _ { i } ^ { * } . t _ { \mathrm { c s } }  r _ { i } ^ { * } . t _ { \mathrm { c s } } + \delta r _ { i } ^ { * } . t _ { \mathrm { c o u n t e r } } ) .$ Upon completion of transmission of a control packet by the RadChat unit $r _ { i } , \mathrm { i f } \ r _ { i } . \mathrm { S I } = 0 , r _ { i }$ updates $r _ { i } . S \mathrm { I }$ to the assigned value by the central processor.

• RadChat Reception at $T _ { k - 1 } .$ Upon reception of a control packet from $r _ { i }$ by $r _ { j }$ (which was not transmitting radar at that time), $r _ { j }$ updates its state as described in Algorithm 1. Throughout the operation of RadChat, each RadChat units stores the received ID, SI and strength information in a local database $\mathcal { D } _ { j }$ . This is used to keep track of unused rTDMA slots for a time reference, and the priority of the time reference. In lines 5, 10, and 15 the SI should be selected within $T _ { k }$ if available, otherwise from the set of unused rTDMA slots in $T _ { f }$ . This algorithm ensures that $r _ { j } . S \mathrm { I }$ is assigned so that $\boldsymbol { r } _ { j } . \mathrm { S I } \neq S _ { \mathrm { X } } . \mathrm { S I } \cup \mathcal { D } _ { j } . \mathrm { \ } \boldsymbol { r } _ { j }$ .t<sub>rs</sub> and $r _ { j } . t _ { \mathrm { c s } }$ in Line 16 are set according to,

$$
r _ { j } . t _ { \mathrm { r s } }  - r _ { i } . t _ { \mathrm { r s } } + ( N + 1 ) T \{ K _ { j } - K _ { i } \} + | V | \{ \kappa _ { j } - \kappa _ { i } ) \}
$$

$$
r _ { j } . t _ { \mathrm { c s } }  r _ { j } ^ { * } . t _ { \mathrm { r s } } - ( N + 1 ) T - T _ { \mathrm { p k t } } + \delta r _ { j } ^ { * } . \mathrm { c o u n t e r } ,
$$

with $\begin{array} { r l r l r l } { \kappa _ { j } } & { { } \stackrel { } { = } } & { \mod ( r _ { j } . \mathrm { S I } , U ^ { \prime } M _ { \mathrm { m a x } } ) , } & { } & { { } K _ { j } } & { } & { { } = } & { } \end{array}$ $\left\lceil r _ { j } . S I / ( \bar { U } ^ { \prime } M _ { \mathrm { m a x } } ) \right\rceil$ , where $r _ { j } ^ { \ast }$ is the a base RadChat unit of the receiving vehicle.

Algorithm 1 Process control packet at unit $r _ { j }$   
1: Store $( r _ { i } . \mathrm { I D } , r _ { i } . \mathrm { S I } , r _ { i }$ .strength) in $\mathcal { D } _ { j }$   
2: if $r _ { j } . S \mathrm { I } = 0$ then   
3: $\mathbf { \bar { \Gamma } } _ { r _ { j } . \mathbf { I D }  \mathbf { \Gamma } r _ { i } . \mathbf { I D } }$   
4: r<sub>j</sub> .strength $ r _ { i }$ .strength + 1   
5: $r _ { j } . \mathrm { S I }  \mathrm { S I } \in T _ { k } \cup T _ { f } \setminus \{ S _ { \mathrm { X } } . \mathrm { S I } \}$   
6: else   
7: if $r _ { j } . \mathrm { I D } = r _ { i }$ .ID then . same time reference   
8: $r _ { j }$ .strength ← max(r<sub>j</sub>.strength, r<sub>i</sub>.strength) + 1   
9: $\bar { \textbf { i f } } r _ { j } . \mathrm { S I } \in S _ { \mathrm { X } } . \mathrm { S I }$ then   
10: $\mathsf { \check { r } } _ { j } . \mathsf { S I } \gets \mathsf { S I } \in T _ { k } \cup T _ { f } \setminus \{ r _ { i } . \mathsf { S I } | i \in \mathcal { D } _ { j } \}$   
11: else . different time reference   
12: if $r _ { i }$ .strength $> r _ { j }$ .strength then   
13: $r _ { j } . \mathrm { I D }  r _ { i } . \mathrm { I D }$   
14: $r _ { j }$ .strength $ r _ { i }$ .strength $+ 1$   
15: $r _ { j } . \mathrm { S I }  \mathrm { S I } \in T _ { k } \cup T _ { f } \setminus \{ S _ { \mathrm { X } } . \mathrm { S I } \}$   
16: Calculate $r _ { j } . t _ { \mathrm { r s } }$ and $r _ { j } . t _ { \mathrm { c s } }$ if $( r _ { j } . \mathrm { I D } , r _ { j } . \mathrm { S I } )$ has changed   
17: Update state of all other RadChat units on same vehicle

## C. Properties of RadChat

For a fixed connected network topology and with less than $M _ { \mathrm { m a x } }$ active radars, RadChat is guaranteed to eventually converge to a solution where each vehicle uses a distinct rTDMA slot and thus R2R interference is eliminated, when the following conditions are met:

• The radar duty cycle of RadChat must satisfy $U ^ { \prime } \leq 1 / 3$ Since RadChat units cannot receive control packets when radar is active, a higher radar duty cycle may end up with two disjoint interfering networks. Higher duty cycle necessitates the use of a separate communication module for mitigation of FMCW radar interference with RadChat.

• RadChat allows synchronization errors of at most $| V | / 2$ across vehicles, since it places each radar transmission in the middle of a vulnerable period leaving a guard time. Under perfect synchronization, RadChat can allocate up to $2 M _ { \mathrm { m a x } }$ non-interfering RadChat units by a time spacing of $| V | / 2$ (so that non-overlapping green-indicated radar bandwidths of $B _ { \mathrm { m a x } }$ fill the whole time-frequency domain in Fig. 2).

• Bandwidth reserved for communication $B _ { \mathrm { c } }$ should allow for at least one data packet during $T _ { k } = ( N + 1 ) T \mathrm { : }$

$$
( N + 1 ) T > T _ { \mathrm { p k t } } = \frac { 8 N _ { \mathrm { p k t } } / \log _ { 2 } ( | \Omega | ) } { B _ { \mathrm { c } } / ( 1 + \alpha ) }\tag{32}
$$

$$
B _ { \mathrm { c } } > \frac { 8 N _ { \mathrm { p k t } } ( 1 + \alpha ) } { ( N + 1 ) T \log _ { 2 } ( | \Omega | ) }\tag{33}
$$

where |Ω| is the constellation size.

Some properties of RadChat protocol are as follows:

• RadChat takes care of both R2R interference among vehicles and among radars mounted on the same vehicle, i.e., self-interference.

• RadChat eliminates any potential R2R interference within a distance $2 \alpha _ { d } d _ { \mathrm { { m a x } } }$ , provided $P _ { \mathrm { c } } ~ = ~ P _ { \mathrm { r } }$ is sufficient to ensure communication with these interferers. Interferers beyond $2 \alpha _ { d } d _ { \mathrm { { m a x } } }$ or beyond the maximum communication range cannot be eliminated by RadChat.

• RadChat ensures that R2R mitigation is completed in a short time and starts as soon as a potential interferer enters the communication range if radar interference and communication signals are subject to the same minimum signal to noise ratio at the RadChat receiver and $P _ { \mathrm { r } } = P _ { \mathrm { c } } .$

## VI. RADCHAT PERFORMANCE EVALUATION AND RESULTS

The performance of the proposed FMCW-based distributed RadChat protocol is evaluated through Matlab R2017b simulations using the phased array toolbox for a network of vehicles, where a single RadChat unit is mounted on each vehicle with the same FMCW sawtooth waveform parameters in a scenario with a large number of uncoordinated radars. Several performance metrics are considered in different dimensions: (i) the probability of R2R interference, (ii) the time it takes for RadChat to minimize interference, (iii) the effect of synchronization errors to RadChat; (iv) the radar jitter; (v) impact of RadChat penetration rate; (vi) effect of the communication parameters.

## A. Simulation Parameters

The main simulation parameters are summarized in Table II. The chirp sequence is designed so as to meet the maximum detectable relative velocity $v _ { \mathrm { m a x } } = 1 4 0 \mathrm { k m / h }$ , the maximum detectable range $d _ { \operatorname* { m a x } } \ = \ 1 5 0$ m when $B _ { \mathrm { c } } ~ = ~ 0$ (since it increases for RadChat), velocity resolution smaller than 1 m/s and range resolution of 15 cm. Radar front-end-hardware component parameters are taken as in [43]. The mean value for the radar cross section of a car is taken as 20 dBsm [43], [48]. Finally, greatest of cell averaging constant false alarm rate (GoCA-CFAR) thresholding with 50 training cells with 2 guard cells is used for radar detection. We will focus dense networks, so we set $\alpha _ { d } = 1$ , leading to a vulnerable duration for $B _ { \mathrm { c } } = 4 0 \mathrm { M H z }$ of $\left| V \right| = 2 . 0 8 \mu \mathrm { s } \ ( 1 3 )$ , leading to maximum 7 concurrent radar transmissions per $T _ { k }$ , resulting with $M _ { \mathrm { m a x } } = 7 0$ vehicles supported maximum by RadChat. A total of 10,000 Monte Carlo simulations are run to obtain interference probability results. The interference probability was calculated as follows: for each realization and each frame, we declare an occurrence of interference if there was at least 1 interferer present in the vulnerable period in at least 1 chirp within that frame. The interference probability is the number of such occurrences divided by 10,000 and can be visualized as a function of the frame index to show the convergence behavior.

TABLE II: Simulation parameters.
<table><tr><td></td><td>Parameter</td><td>Value</td></tr><tr><td></td><td>Chirp duration  $( T )$  Frame duration</td><td> $2 0 \mu \mathrm { s }$  20 ms</td></tr><tr><td>adar</td><td> $( T _ { f } )$ </td><td>0.1</td></tr><tr><td> $\dot { \simeq }$ </td><td>Modified duty cycle  $( U ^ { \prime } )$ </td><td></td></tr><tr><td></td><td>Radar bandwidth  $( B _ { r } )$ </td><td>0.96 GHz-1 GHz</td></tr><tr><td></td><td>Bandwidth of interest  $\left( B _ { \mathrm { m a x } } \right)$ </td><td>50 MHz</td></tr><tr><td></td><td> $d _ { \mathrm { m a x } }$  for  $B _ { \mathrm { c } } = 0$ </td><td>150 m</td></tr><tr><td></td><td> $v _ { \mathrm { m a x } }$ </td><td>140 km/h</td></tr><tr><td></td><td> $P _ { \mathrm { r } } , P _ { \mathrm { c } }$ </td><td>11 dB</td></tr><tr><td></td><td> $\mathrm { S N R }$ </td><td>10 dB</td></tr><tr><td></td><td>Number of chirps per frame (N)</td><td>99</td></tr><tr><td></td><td>Carrier frequency  $( f _ { \mathrm { r } } )$ </td><td>77 GHz</td></tr><tr><td></td><td> $T _ { s }$ </td><td>0.01 μs</td></tr><tr><td></td><td>Chebyshev low-pass filter order</td><td>13</td></tr><tr><td></td><td>Thermal noise temperature  $T _ { 0 }$ </td><td>290 K</td></tr><tr><td></td><td>Receiver&#x27;s noise figure</td><td>4.5 dB</td></tr><tr><td></td><td>Communication bandwidth  $B _ { \mathrm { c } }$ </td><td>40MHz</td></tr><tr><td>Coomm.</td><td>Packet size  $( N _ { \mathrm { p k t } } )$ </td><td>4800 Bits</td></tr><tr><td></td><td>Modulation</td><td>16-QAM</td></tr><tr><td></td><td>MAC</td><td>non-persistent CSMA</td></tr><tr><td></td><td>SlotTime  $\delta$ </td><td>10μs</td></tr><tr><td></td><td>Maximum contention window size  $( W _ { 0 } )$ </td><td>6</td></tr><tr><td></td><td>Maximum backoff stage (B)</td><td>3</td></tr></table>

## B. Results and Discussion

1) Time to minimize interference: Since radars employing RadChat exchange radar starting times, the R2R interference probability vanishes in the steady-state when all facing radars exchange information and select non-overlapping rTDMA slots. The time to reach negligible R2R interference (no interference among 10,000 simulations) is denoted as $t _ { \mathrm { f i n a l } }$ and its maximum, mean and minimum value in a network of M vehicles is shown in Fig. 11. RadChat is observed to eliminate interference in less than $T _ { f } / 2 = 1 0$ ms on the average, whereas the maximum time to mitigate the interference over 10,000 simulations is less than $1 3 T _ { f }$ , being less than 260 ms for $W _ { 0 } ~ = ~ 6 .$ . However, selection of a larger $W _ { 0 }$ is observed to decrease this maximum time to reach negligible R2R interference to 100 ms (Fig. 17).

![](images/bc534c2eeba1078ed6adafe420286a9a3efbbef5f91cf7ee37720dbf6bea7ae4.jpg)  
Fig. 11: The mean, maximum and minimum time to reach negligible R2R interference (no interference among 10,000 simulations) for varying number of vehicles M.

![](images/cc0b4ddca3f6594760d82e4cc3f30d4d5995e78f59b63f8ede871e35d9ba5a2d.jpg)  
Fig. 12: Comparison of R2R interference over time for varying M facing radars with RadChat and regular radar.

Fig. 12 shows how the R2R interference decreases over time with RadChat. It is observed that the R2R interference decreases sharply after one frame duration (by more than a factor of 25) and below $1 0 ^ { - 3 }$ within less than 10 frames (200 ms) for the case with 70 interfering radars.

2) Effect of synchronization error $\varepsilon _ { s y n c } .$ The R2R interference over time in a network of $M _ { = } 7 0$ vehicles is compared with various synchronization errors in Fig. 13. A uniformly distributed synchronization error with maximum values $\varepsilon _ { \mathrm { s y n c } } =$ $\pm \{ 0 . 6 , 1 . 2 , 1 . 3 , 1 . 6 , 2 , 2 0 \}$ µs is assumed, where each node is assumed to retain the same synchronization error during the simulation. Our simulations are based on a discrete time resolution of $0 . 2 \mu \mathrm { s } ,$ , which led to $V = 2 . 4 \mu \mathrm { s }$ after rounding. Hence, the impact of synchronization errors for $\varepsilon _ { \mathrm { s y n c } } \leq V / 2 =$ 1.2 µs is expected to be minor for RadChat, performing almost the same as with perfect synchronization. For $\varepsilon > 1 . 2 \mu \mathrm { s } .$ , the possibility of overlap of radar chirp sequences leads to a high floor of the interference probability.

3) Radar Jitter: The periodicity of radar is observed to be distorted at most by one $T _ { f }$ during the initialization stage and the radar experiences no jitter afterwards (result not shown).

4) RadChat Deployment: We investigate the R2R interference probability in heterogeneous network setting where not all nodes are equipped with RadChat. The R2R interference experienced by a vehicle is compared for a network of $M = 7 0$ vehicles with changing percentages of RadChat equipped vehicles in Fig. 14, where $B _ { \mathrm { r } } = 1 \mathrm { G H z }$ for radar only case and $B _ { \mathrm { r } } = 0 . 9 6 \operatorname { G H z }$ for RadChat. The results show that 100% deployment of RadChat results with almost total elimination of R2R interference, though these benefits diminish very quickly with reduced deployment. When no vehicles are equipped with RadChat, the reduction of the available radar bandwidth $B _ { \mathrm { r } }$ increases R2R interference due to (14).

![](images/1b2289dbf01828be7e34daf038df5a17e2f00381df7d700fdd740ee10ab80e6a.jpg)  
Fig. 13: Comparison of the R2R interference probability for the regular radar with RadChat with zero and varying synchronization error, for $M = 7 0$

![](images/864ac18fa6156c2207d1528dae0101b5a49db58f1df73a08eabbdde75b15ac24.jpg)  
Fig. 14: R2R interference probability versus percentage of RadChat deployment for a network of $M \stackrel { - } { = } 7 0$ facing radars.

5) Effect of Communication Parameters: The effect of $B _ { \mathrm { c } }$ on R2R interference is investigated for $W _ { 0 } ~ = ~ \{ 6 , 6 4 \}$ in Fig. 15. In order for RadChat to converge, a large enough bandwidth must be assigned to the control channel. With a larger bandwidth, convergence is slightly faster, while with a small bandwidth, there is a floor in the interference probability. Note that allocation of a portion of bandwidth to communication comes with a cost of degradation in the radar range estimation performance. However, the radar performance degradation is negligible for automotive applications for the considered communication bandwidths (0.63 cm radar range resolution reduction and 1.64 cm range estimation error increase [36]). In Fig. 16, the maximum value of $t _ { \mathrm { f i n a l } }$ is observed to be highly affected by maximum contention window size $W _ { 0 }$ for $M = 7 0$ . Maximum value of $t _ { \mathrm { f i n a l } }$ is observed to decrease from $1 0 T _ { f }$ to $4 T _ { f }$ with a change of maximum contention window size from 6 to 64. Both the communication bandwidth and the contention window size affect the convergence time considerably due to the CSMAbased contention scheme.

![](images/a58b2b93cd76bf15f75a37e0c27398ebb2bc572783b06e33fdf333b2be0ad6b2.jpg)  
Fig. 15: R2R interference probability versus time for changing $B _ { \mathrm { c } }$ and $W _ { 0 }$ for $M = 7 0 .$

![](images/6c79c9de9495a1ecee6eeff6df26768f96e9d9c012a14fd93ef25fd1734cbe23.jpg)  
Fig. 16: R2R interference probability versus time for varying $W _ { 0 }$ for $M = 7 0$

![](images/9ced740053af0281e0223cb923992321777cb648f3c36e4fe6755313752b0fa2.jpg)  
Fig. 17: The maximum time to reach negligible R2R interference (no interference among 10,000 simulations) for varying M and $W _ { 0 } .$

The maximum value of $t _ { \mathrm { f i n a l } }$ for varying M and $W _ { 0 }$ is given in Fig.17. It is observed that there is an optimum $W _ { 0 }$ for reaching the steady-state as quickly as possible in the worst case, which depends on M. RadChat converges in at most $t _ { \mathrm { f i n a l } } = 1 T _ { f }$ for $M \leq 1 0$ with $W _ { 0 } = \{ 4 8 , 6 4 \}$ , whereas $t _ { \mathrm { f i n a l } } =$ $5 T _ { f }$ for $M = 7 0$ with $W _ { 0 } \geq 4 8$ . This indicates that the best choice for the maximum contention window size for the given parameters in Table II is $W _ { 0 } = 6 4$ , which ensures that RadChat is able to reduce R2R interference below $1 0 ^ { - 3 }$ in 80 ms and a reduction of an order of magnitude is achieved almost in one radar frame time (not shown in results) for a newly formed 70-vehicle VANET. This duration is expected to be shorter when multiple radars are mounted per vehicle and VANET connectivity changes slowly.

## VII. CONCLUSION

Based on interference analyses for spectrum sharing of automotive radar and vehicular communications, we propose guidelines for mitigation of interference and designed the radar and communication cooperation system RadChat for FMCW-based automotive radar interference mitigation. Rad-Chat builds upon the same hardware for radar and communications and a MAC, which is a combination of FDM, TDMA for radar, and CSMA for communication. RadChat exploits the low utilization of time and frequency of a typical radar with the limited impact of a small bandwidth loss on the radar performance. Extensive network simulations show that automotive radar interference probability is reduced significantly, by about one order of magnitude every radar frame time in dense VANETs. RadChat is expected to mitigate R2R interference even in sparse networks by adaptation of the vulnerable period in combination with fewer interfering vehicles. With our proposed approach, we are able to mitigate interference by shifting radar transmissions in time with higher penetration rate. Future work will consider larger-scale scenarios for heterogeneous FMCW radars with different bandwidths and chirp parameters, as well as the additional use of RadChat for inter-vehicle data communication.

## APPENDIX A

## VULNERABLE PERIOD FOR R2R INTERFERENCE

The transmission by Vehicle 2, which starts at time $\tau$ is received by Vehicle 1 in $\mathrm { F i g } . 3 ( \mathrm { a } )$ at time $t ^ { \prime }$ and is equivalent to a chirp reception starting at $t ^ { \prime } - \tau _ { D }$ without any Doppler shift. $\tau _ { D }$ is the perceived Doppler time delay and is obtained as follows after applying the triangle proportionality theorem to one FMCW chirp in Fig. 2

$$
\tau _ { D } = T f _ { D } / B _ { \mathrm { r } } = T v f _ { \mathrm { r } } / ( B _ { \mathrm { r } } c )
$$

$$
\in [ - T | v | f _ { \mathrm { r } } / ( B _ { \mathrm { r } } c ) , + T | v | f _ { \mathrm { r } } / ( B _ { \mathrm { r } } c ) ]\tag{34}
$$

$$
\subset [ - T | v _ { \mathrm { m a x } } | f _ { \mathrm { r } } / ( B _ { \mathrm { r } } c ) , + T | v _ { \mathrm { m a x } } | f _ { \mathrm { r } } / ( B _ { \mathrm { r } } c ) ]\tag{35}
$$

$$
\approx [ - 1 / ( 4 { B _ { \mathrm { r } } } ) , + 1 / ( 4 { B _ { \mathrm { r } } } ) ]\tag{36}
$$

(37)

where we have made use of the fact that the maximum radar detectable relative velocity is given by $v _ { \mathrm { m a x } } = c / ( 4 f _ { \mathrm { r } } T )$ [49], and that vehicles may approach or recede.

R2R interference at the first chirp occurs when $t ^ { \prime } - \tau _ { D } \in$ $[ 0 , T _ { \mathrm { m a x } } ]$ , i.e.. when the first red chirps falls inside the greencoloured region in Fig. 2, where $T _ { \mathrm { m a x } } ~ = ~ T B _ { \mathrm { m a x } } / B _ { \mathrm { t } }$ corresponds to the maximum delay for detectable radar targets. Considering all possible distances, $d / c ~ \in ~ [ 0 , \alpha _ { d } T _ { \operatorname* { m a x } } ]$ , then vulnerable period is given by

$$
V = [ - \alpha _ { d } T _ { \mathrm { m a x } } - 1 / ( 4 B _ { \mathrm { r } } ) , T _ { \mathrm { m a x } } + 1 / ( 4 B _ { \mathrm { r } } ) ]\tag{38}
$$

In practice, $B _ { \mathrm { r } } \gg 1 / T _ { \operatorname* { m a x } }$ so this term may be ignored. Hence, the vulnerable period is approximately $V = [ - \alpha _ { d } T _ { \mathrm { m a x } } , T _ { \mathrm { m a x } } ] ,$ assuming a radar that can sample in-phase and quadrature samples and has perfect low-pass filtering.

## REFERENCES

[1] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 22–35, 2017.

[2] L. Kong, M. K. Khan, F. Wu, G. Chen, and P. Zeng, “Millimeter-wave wireless communications for IoT-cloud supported autonomous vehicles: Overview, design, and challenges,” IEEE Communications Magazine, vol. 55, no. 1, pp. 62–68, January 2017.

[3] J. Ryde and N. Hillier, “Performance of laser and radar ranging devices in adverse environmental conditions,” Journal of Field Robotics, vol. 26, no. 9, pp. 712–727, 2009. [Online]. Available: https: //onlinelibrary.wiley.com/doi/abs/10.1002/rob.20310

[4] I. M. Kunert, “Project final report, MOSARIM: More safety for all by radar interference mitigation,” 2012. [Online]. Available: http://cordis.europa.eu/docs/projects/cnect/1/248231/ 080/deliverables/001-D611finalreportfinal.pdf

[5] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Automotive radar - investigation of mutual interference mechanisms,” Advances in Radio Science, vol. 8, pp. 55–60, Sep. 2010.

[6] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in GermanMicrowave Conference (GeMIC). IEEE, 2011, pp. 1–4.

[7] A. Bourdoux, K. Parashar, and M. Bauduin, “Phenomenology of mutual interference of FMCW and PMCW automotive radars,” in IEEE Radar Conference (RadarConf), May 2017, pp. 1709–1714.

[8] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[9] W.Buller, B. Wilson, J. Garbarino, J. Kelly, N. Subotic, B. Thelenand, and B. Belzowski, “Radar congestion study,” (Report No. DOT HS 812 632). Washington, DC: National Highway Traffic Safety Administration, Tech. Rep., Sept. 2018.

[10] J. B. Kenney, “Dedicated short-range communications (dsrc) standards in the united states,” Proceedings of the IEEE, vol. 99, no. 7, pp. 1162– 1182, 2011.

[11] K. Sjöberg, P. Andres, T. Buburuzan, and A. Brakemeier, “Cooperative intelligent transport systems in europe: Current deployment status and outlook,” IEEE Vehicular Technology Magazine, vol. 12, no. 2, pp. 89– 97, 2017.

[12] T. Yamawaki and S. Yamano, “60-GHz millimeter-wave automotive radar,” Fujitsu technical review, vol. 15, no. 2, pp. 9–18, 1998.

[13] P. Kumari, N. Gonzalez-Prelcic, and R. W. Heath, “Investigating the IEEE 802.11ad standard for millimeter wave automotive radar,” in IEEE 82nd Vehicular Technology Conference (VTC), Sept 2015, pp. 1–5.

[14] B. Paul, A. R. Chiriyath, and D. W. Bliss, “Survey of RF communications and sensing convergence research,” IEEE Access, vol. 5, pp. 252–270, 2017.

[15] A. Herschfelt and D. W. Bliss, “Spectrum management and advanced receiver techniques (SMART): Joint radar-communications network performance,” in 2018 IEEE Radar Conference (RadarConf18), April 2018, pp. 1078–1083.

[16] F. Paisana, J. P. Miranda, N. Marchetti, and L. A. DaSilva, “Databaseaided sensing for radar bands,” in 2014 IEEE International Symposium on Dynamic Spectrum Access Networks (DYSPAN), April 2014, pp. 1–6.

[17] L. Wang, J. McGeehan, C. Williams, and A. Doufexi, “Radar spectrum opportunities for cognitive communications transmission,” in 2008 3rd International Conference on Cognitive Radio Oriented Wireless Networks and Communications (CrownCom 2008), May 2008, pp. 1–6.

[18] Y. Han, E. Ekici, H. Kremo, and O. Altintas, “Spectrum sharing methods for the coexistence of multiple RF systems: A survey,” Ad Hoc Networks, vol. 53, pp. 53 – 78, 2016. [Online]. Available: http://www.sciencedirect.com/science/article/pii/S1570870516302153

[19] M. Labib, V. Marojevic, A. F. Martone, J. H. Reed, and A. I. Zaghloui, “Coexistence between communications and radar systems: A survey,” URSI Radio Science Bulletin, vol. 2017, no. 362, pp. 74–82, Sep. 2017.

[20] A. M. Voicu, L. Simic, and M. Petrova, “Survey of spectrum sharing for inter-technology coexistence,” IEEE Communications Surveys Tutorials, pp. 1–1, 2018.

[21] M. Takeda, T. Terada, and R. Kohno, “Spread spectrum joint communication and ranging system using interference cancellation between a roadside and a vehicle,” in IEEE 48th Vehicular Technology Conference, vol. 3, May 1998, pp. 1935–1939.

[22] Z. Dou, X. Zhong, and W. Zhang, “Radar-communication integration based on MSK-LFM spread spectrum signal,” International Journal of Communications, Network and System Sciences, vol. 10, pp. 108–117, 2017.

[23] C. Sturm and W. Wiesbeck, “Waveform design and signal processing aspects for fusion of wireless communications and radar sensing,” Proceedings of the IEEE, vol. 99, no. 7, pp. 1236–1259, July 2011.

[24] A. R. Chiriyath, B. Paul, G. M. Jacyna, and D. W. Bliss, “Inner bounds on performance of radar and communications co-existence.”

IEEE Transactions on Signal Processing, vol. 64, no. 2, pp. 464–474, 2016.

[25] B. Paul and D. W. Bliss, “Extending joint radar-communications bounds for FMCW radar with doppler estimation,” in 2015 IEEE Radar Conference (RadarCon), May 2015, pp. 0089–0094.

[26] Y. Han, E. Ekici, H. Kremo, and O. Altintas, “Optimal spectrum utilization in joint automotive radar and communication networks,” in 2016 14th International Symposium on Modeling and Optimization in Mobile, Ad Hoc, and Wireless Networks (WiOpt), May 2016, pp. 1–8.

[27] I. Yattoun, T. Labia, A. Peden, G. Landrac, M. Ney, M. Resibois, J. Bonnin, A. Baghdadi, N. Montavont, M. Fujise, and Y. Le Roux, “A millimetre communication system for IVC,” in 2007 7th International Conference on ITS Telecommunications, June 2007, pp. 1–6.

[28] B. J. Donnet and I. D. Longstaff, “Combining MIMO radar with OFDM communications,” in European Radar Conference, Sept 2006, pp. 37–40.

[29] D. Garmatyuk, J. Schuerger, and K. Kauffman, “Multifunctional software-defined radar sensor and data communication system,” IEEE Sensors Journal, vol. 11, no. 1, pp. 99–106, Jan 2011.

[30] J. Choi, V. Va, N. Gonzalez-Prelcic, R. Daniels, C. R. Bhat, and R. W. Heath, “Millimeter-wave vehicular communication to support massive automotive sensing,” IEEE Communications Magazine, vol. 54, no. 12, pp. 160–167, December 2016.

[31] C. Wang, C. D. Ozkaptan, E. Ekici, and O. Altintas, “Multi-carrier modulation on FMCW radar for joint automotive radar and communication,” in 2018 IEEE Vehicular Networking Conference (VNC), Dec 2018, pp. 1–2.

[32] Y. L. Sit, B. Nuss, and T. Zwick, “On mutual interference cancellation in a MIMO OFDM multiuser radar-communication network,” IEEE Transactions on Vehicular Technology, vol. 67, no. 4, pp. 3339–3348, 2018.

[33] P. Falcone, F. Colone, C. Bongioanni, and P. Lombardo, “Experimental results for OFDM WiFi-based passive bistatic radar,” in IEEE Radar Conference, May 2010, pp. 516–521.

[34] L. Reichardt, C. Sturm, F. Grunhaupt, and T. Zwick, “Demonstrating the use of the IEEE 802.11p car-to-car communication standard for automotive radar,” in 6th European Conference on Antennas and Propagation (EUCAP), March 2012, pp. 1576–1580.

[35] Y. L. Sit, B. Nuss, S. Basak, M. Orzol, and T. Zwick, “Demonstration of interference cancellation in a multiple-user access OFDM MIMO radarcommunication network using USRPs,” in IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), May 2016, pp. 1–4.

[36] C. Aydogdu, N. Garcia, L. Hammarstrand, and H. Wymeersch, “Radar communication for combating mutual interference of FMCW radars,” in IEEE Revolutions in Radar, Boston, USA, 22-26 Apr. 2019.

[37] C. Aydogdu, N. Garcia, and H. Wymeersch, “Improved pedestrian detection under mutual interference by FMCW radar communications,” in IEEE International Symposium on Personal, Indoor and Mobile Radio Communications (PIMRC), Workshop on 5G V2X Communications for Connected Autonomous Driving, Sept. 2018.

[38] Y. Han, E. Ekici, H. Kremo, and O. Altintas, “Automotive radar and communications sharing of the 79-GHz band,” in Proceedings of the First ACM International Workshop on Smart, Autonomous, and Connected Vehicular Systems and Services, ser. CarSys ’16. New York, NY, USA: ACM, 2016, pp. 6–13. [Online]. Available: http://doi.acm.org/10.1145/2980100.2980106

[39] V. Petrov, G. Fodor, J. Kokkoniemi, D. Moltchanov, J. Lehtomäki, S. Andreev, Y. Koucheryavy, M. J. Juntti, and M. Valkama, “On unified vehicular communications and radar sensing in millimeter-wave and low terahertz bands,” CoRR, vol. abs/1901.06980, 2019. [Online]. Available: http://arxiv.org/abs/1901.06980

[40] A. G. Stove, “Linear FMCW radar techniques,” IEE Proceedings F - Radar and Signal Processing, vol. 139, no. 5, pp. 343–350, Oct 1992.

[41] K. Ramasubramanian, “Using a complex baseband architecture in FMCW radar systems,” Texas Instruments, Tech. Rep., May 2017.

[42] A. Goldsmith, Wireless Communications. Cambridge University Press, 2005.

[43] C. Karnfelt, A. Paden, A. Bazzi, G. E. H. Shhade, M. Abbas, and T. Chonavel, “77 GHz ACC radar simulation platform,” in 9th International Conference on Intelligent Transport Systems Telecommunications (ITST), Oct 2009, pp. 209–214.

[44] M. A. Richards, Fundamentals of Radar Signal Processing. Tata McGraw-Hill Education, 2005.

[45] A. F. Molisch, Wireless communications. John Wiley & Sons, 2012, vol. 34.

[46] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8110–8117, Sep. 2018.

[47] L. Zheng, M. Lops, X. Wang, and E. Grossi, “Joint design of overlaid communication systems and pulsed radars,” IEEE Transactions on Signal Processing, vol. 66, no. 1, pp. 139–154, Jan 2018.

[48] S. Lee, S. Kang, S. C. Kim, and J. E. Lee, “Radar cross section measurement with 77 GHz automotive FMCW radar,” in IEEE 27th Annual International Symposium on Personal, Indoor, and Mobile Radio Communications (PIMRC), Sept 2016, pp. 1–6.

[49] M. I. Skolnik, Radar Handbook, 3rd ed. New York: McGraw-Hill Education, 2008.

![](images/ea97a81a26512a40939583b4b5b94bfaa4a46a015fda09598eddcd3674dd7d9c.jpg)

![](images/49c55afcc5ab702d48dae3a40725995f9777c630afef0e33d4b5c60801fcee11.jpg)  
Canan Aydogdu is a Marie Sklodowska-Curie Fellow at Chalmers, working on cross-layer multi-hop sensing systems for the future energy-efficient selfdriving car networks. Formerly, she was an associate professor at Izmir Institute of Technology, Turkey. She received the Ph.D. degree from Bilkent University, Turkey, in 2011.

![](images/1f206b2d15bf6994d4003e2e00d31ba82052fca8693d3ca4c705150226d9212e.jpg)

radar, precision positioning, and medical monitoring. Dan has been the principal investigator on numerous programs including sponsored programs with DARPA, ONR, Google, Airbus, and others. He is responsible for foundational work in electronic protection, adaptive multiple-input multipleoutput (MIMO) communications, MIMO radar, distributed-coherent systems, and RF convergence. Before moving to ASU, Dan was a Senior Member of the Technical Staff at MIT Lincoln Laboratory (1997-2012). Between his undergraduate and graduate degrees, Dan was employed by General Dynamics (1989-1993), where he designed avionics for the Atlas-Centaur launch vehicle, and performed magnetic field optimization for high-energy particle-accelerator superconducting magnets. His doctoral work (1993-1997) was in the area of high-energy particle physics and lattice-gauge-theory calculations. Dan is a member of the IEEE AES Radar Systems Panel and is a member of the IEEE Signal Processing Magazine editorial board.

Musa Furkan Keskin is a postdoctoral researcher at Chalmers University of Technology. He obtained the B.S., M.S., and Ph.D degrees from the Department of Electrical and Electronics Engineering, Bilkent University, Ankara, Turkey, in 2010, 2012, and 2018, respectively. His current research interests include intelligent transportation systems, radar signal processing and radar communications coexistence.

![](images/11109b8ca6474538c86229525abd9a8ddbd437661acbfdc885231a1d90ac1f13.jpg)

Nil Garcia (S’14–M’16) received the Telecommunications Engineer degree from the Polytechnic University of Catalonia (UPC), Barcelona, Spain, in 2008; and the double Ph.D. degree in electrical engineering from the New Jersey Institute of Technology, Newark, NJ, USA, and from the National Polytechnic Institute of Toulouse, Toulouse, France, in 2015.

He is currently a postdoctoral researcher of Communication Systems with the Department of Signals and Systems at Chalmers University of Technology,

Sweden. In 2009, he worked was an engineer in the Centre National d’Études Spatiales (CNES). In 2008 and 2009, he had internships in CNES and NASA. Hi research interests are in the areas of localization, intelligent transportation systems and 5G.

![](images/11090265218ca4f4e220d15e71eae18ff423ee5a20b4fff115ecef912440e439.jpg)

Henk Wymeersch (S’01, M’05) obtained the Ph.D. degree in Electrical Engineering/Applied Sciences in 2005 from Ghent University, Belgium. He is currently a Professor of Communication Systems with the Department of Electrical Engineering at Chalmers University of Technology, Sweden and Distinguished Research Associate with Eindhoven University of Technology, the Netherlands. Prior to joining Chalmers, he was a postdoctoral researcher with the Laboratory for Information and Decision Systems at the Massachusetts Institute of Technol-

Daniel W. Bliss Daniel W. Bliss is an Associate Professor in the School of Electrical, Computer, and Energy Engineering at ASU and a Fellow of the IEEE. He is also the Director of Arizona State University’s Center for Wireless Information Systems and Computational Architectures. Dan received his Ph.D. and M.S. in Physics from the University of California at San Diego (1997 and 1995), and his B.S. in Electrical Engineering from Arizona State University (1989). His current research focuses on advanced systems in the areas of communications,

ogy. His current research interests include cooperative systems and intelligent transportation.