# Cognitive Interference Mitigation in Automotive Radars

Zora Slavik<sup>1</sup> and Kumar Vijay Mishra<sup>2</sup>

<sup>1</sup>FZI Research Center for Information Technology, Karlsruhe, Germany

<sup>2</sup>IIHR - Hydroscience and Engineering, The University of Iowa, Iowa City, IA 52242 USA

E-mail: slavik@fzi.de, kumarvijay-mishra@uiowa.edu

Abstract—In the cost sensitive automotive market, frequencymodulated continuous-wave (FMCW) radars are expected to persist for a long period of time because of their cheap and simple circuitry. Further, more autonomous driving systems use radars than before and are, therefore, increasingly susceptible to mutual interference. We propose a system that cognitively adapts its chirp bandwidth and transmission time slot in interference scenarios. The resolution and detection performance of this cognitive radar is similar to a standard FMCW radar. Our measurements using an actual automotive radar with a corner reflector in a complex parking house show that a reasonable signal separability is obtained after reducing the chirp bandwidth by 25% and simultaneously extending the range by a factor of 16.

Index Terms—automotive radar, cognitive radar, corner reflector, FMCW, interference

## I. INTRODUCTION

Research in autonomous driving systems (ADS) technology is defining a new era of mobility. While ADS has progressed to the stage of initial practical implementation, substantial progress is required to ensure its safety and reliability in real-time traffic environments [1], [2]. As an intermediate step, advanced driver assistance systems (ADAS) have been developed that partially take over single driving functions [3]. ADAS fulfill specific tasks that enable automated cyberphysical systems (ACPS) to recognize and react to traffic conditions, such as automated cruise control (ACC) or lane keeping. A number of sensor systems based on camera, radar, lidar or ultrasonic sensors provide either individual or joint information from the surroundings that are relevant to ADAS [4]. In addition to these classic sensor systems, other intelligent vehicles or even infrastructure act as external sensor systems to enhance ADAS decision making. A reliable implementation will be possible using 5G technology that could even be implemented while reusing radar hardware [5], [6].

Overall, the amount of sensor systems applied on the roads has already increased significantly [7] and is a trend that is certain to accelerate in the near future. The diversity in sensors is mainly due to the advantage of information gathering from different sensing technologies and complementing vulnerabilities of one sensor through other. Although camera systems are favorable for object detection and lidar systems come with high spatial resolution, so far only radar is able to perform well in unfavorable conditions such as harsh weather and low visibility [8].

While future trends indicate that frequency bands and data processing techniques for automotive radar are likely to change [9], the transmit waveform and receiver can be expected to be based on the frequency-modulated continuous-wave (FMCW) signal. Besides the simple circuitry, the ability to measure both range and Doppler velocity at a sufficient resolution makes FMCW radar widely used in automotive applications [10]. The FMCW radar receiver mixes the received signal with the transmitted frequency ramp. The result is the low-frequency difference or beat signal which is then processed using two-dimensional (2-D) Discrete Fourier Transform (DFT) to estimate the unknown target range and Doppler for a given azimuth. The

FMCW is a popular waveform even in much advanced automotive radar prototypes that also employ electronic beam steering or digital beamforming to cover specific driving situations such as passing a curve [11], [12]. In these conditions, straightforward scene illumination is not as interesting as detecting objects that are eventually located in the curve ahead.

With the increased uptake of automotive radars, the issue of their mutual interference has turned out be a serious challenge [13]. Apart from unintended interference along intersections or highways, malicious jamming of radar sensors may also occur. Each scenario requires individual mitigation approaches that include transmitting radar waveforms separated in time, frequency, space, and modulation. Spatial separation using digital beamforming was suggested in [14] where, instead of pausing the radar transmission completely in the presence of interference, the corrupted receive channels were eliminated. The phased array radar presented in [15] employed adaptive digital beamforming, where interference in the specific directions was cancelled out by adjusting weights of the beamforming algorithm. Automotive radar transmit signal separation in time domain was exploited for mitigating the interference in [16]. A threshold method was used for interference elimination in [17] by assuming that the interference components in the receive signal spectrum are usually stronger. A few studies [18] examine orthogonal frequency division multiplexing (OFDM) as a possible future radar waveform and analyze its impact on a FMCW-based radar system. Their findings show that OFDM waveforms introduce additional peaks to automotive systems that are currently on the market. While most approaches rely on first detecting the interference, a recent investigation [19] employs optimization to estimate beat signal in the presence of interference. The idea of a cognitive spectrum sharing solution was suggested and applied in [20] for a hardware architecture that enables an efficient signal acquisition and the received signals are processed using sub-Nyquist processing [21], [22].

Nearly all of these approaches for interference mitigation cause degradation in radar reactivity because of their inherent transmission pauses. In this paper, we present a spectrum sharing and interference mitigation approach for a commercial 77 GHz FMCW radar system that transmits linear chirps. Our scenario and signal model includes realistic object models consisting of clustered point targets that represent extended scattering surfaces with non-flat topology. We performed hardware experiments with chirps that cover the full bandwidth as well as partial frequency bands within the full allocated spectrum. We show that the loss in resolution resulting from narrowing down the chirp bandwidth is compensated by superposition of the cognitively allocated chirps and spatial diversity of the phased array antenna. In addition, we analyze the impact of changing the relation of bandwidth and chirp duration on the radar performance.

The rest of the paper is organized as follows. In the next section, we introduce the underlying signal model. In Section III, we present the experimental set-up for the cognitive illumination and follow by measurement results in Section IV. We conclude in Section V.

## II. SIGNAL AND CHANNEL MODEL

Typical maximum unambiguous ranges and velocities for automotive radars are much lower than applications such as surveillance and airborne systems [7]. Depending on the scenario (urban, highway or intersection), the maximum range may lie in the range 10 −200 m. Automotive radar systems feature co-located transmit and receive antennas mounted on the ego-vehicle. In practice, the automotive targets follow an extended scatterer model [10].

Consider a scenario with K extended targets, each of which comprises $L _ { k }$ point scatterers. The transmit power $P _ { t }$ is amplified by the gain $G _ { T X }$ of the transmit antenna TX, the gain $G _ { R X }$ of the receive antenna RX and the gain $G _ { \sigma _ { l k } }$ of the reflecting target, while it is attenuated by the factor $\alpha _ { l k , F S }$ through free space (FS) propagation for path length $r _ { l k }$ to and from each target. The target gain depends on the radar cross section $\sigma _ { l k }$ and the wavelength λ of the carrier frequency. The two-way propagation Friis formula [23] relates the target gain from the radar cross section of the reflecting target with the attenuation α<sub>lk</sub>:

$$
\alpha _ { l k } = \frac { P _ { r , l k } } { P _ { t } } = G _ { T X } \cdot a _ { l k , F S } ^ { 2 } \cdot G _ { \sigma , l k } \cdot G _ { R X } = \frac { G _ { T X } G _ { R X } \lambda ^ { 2 } \sigma _ { l k } } { ( 4 \pi ) ^ { 3 } r _ { l k } ^ { 4 } } .\tag{1}
$$

In general, the transmit signal $s _ { T } ( t )$ is a train of P chirps spaced by the interval $T _ { p } { \mathrm { : } }$

$$
s _ { T } ( t ) = \sum _ { p = 0 } ^ { P - 1 } s _ { T , p } ( t - p T _ { p } ) , \ 0 \leq t \leq P T _ { p } .\tag{2}
$$

Accordingly, the receive signal incorporates the channel and target models as

$$
s _ { R } ( t ) = \sum _ { p = 0 } ^ { P - 1 } \sum _ { k = 0 } ^ { K - 1 } \sum _ { l _ { k } = 0 } ^ { L _ { k } - 1 } a _ { l k } s _ { T , p } ( t - \tau _ { r , l k } - p T _ { p } ) \cdot e ^ { - j 2 \pi p \frac { T _ { p } } { \tau _ { D , l k } } } .\tag{3}
$$

Channel delays for chirp based waveforms are stated as the sum of the propagation related delay $\tau _ { r , l k }$ and the relative velocity Doppler delay $\tau _ { D , l k }$ with $\begin{array} { r } { \tau _ { s , k } = \tau _ { r , l k } + \tau _ { D , l k } = \frac { 2 ( r _ { l k } - v _ { l k } t ) } { c _ { 0 } } } \end{array}$ . The velocity $v _ { l k }$ refers to the relative velocity between the ego-vehicle and reflecting target. Integrating the linear frequency ramp, results in the phase course $\varphi ( t )$ on the transmitter side for a single pulse. The quotient of the bandwidth B that is covered by the chirp and its duration $t _ { u p }$ gives the chirp rate $\begin{array} { r } { \alpha = \frac { B } { t _ { u v } } } \end{array}$ , thus resulting in the phase $\textstyle \varphi ( t ) = { \frac { \alpha } { 2 } } t ^ { 2 } + \varphi _ { 0 }$ Assuming $\varphi _ { 0 } = 0$ leads to the following transmit chirp train

$$
s _ { T } ( t ) = \sum _ { p = 0 } ^ { P - 1 } e ^ { j \pi \alpha ( t - p T _ { p } ) ^ { 2 } } .\tag{4}
$$

For K targets, each with $L _ { k }$ scatterers ,the receive waveform is

$$
s _ { R } ( t ) = \sum _ { p = 0 } ^ { P - 1 } \sum _ { k = 0 } ^ { K - 1 } \sum _ { l _ { k } = 0 } ^ { L _ { k } - 1 } a _ { l k } \cdot e ^ { j \pi \alpha \left( t - p T _ { p } - \tau _ { s , l k } \right) ^ { 2 } } .\tag{5}
$$

It is more convenient to consider the frequency over time aggregation that equals the derivative of the signal phase

$$
f _ { T } ( t ) = \sum _ { p = 0 } ^ { P - 1 } \alpha ( t - p T _ { p } ) \cdot \mathrm { r e c t } \left( \frac { t - t _ { u p } - p T _ { p } } { t _ { u p } } \right) ,\tag{6}
$$

where rect(·) is the rectangular window function that limits the frequency ramp to the chirp duration, which is usually less than the chirp length $T _ { p }$ . The received frequency ramp is shifted by the propagation time and pitched by the Doppler shift as

![](images/df9c4abb08512c24be751fddc1fe6cf4f811b1a474598fcbd38a296adba8198b.jpg)  
Fig. 1. LFMCW transmit (blue) and receive (green) frequency ramps $f _ { T } ( t )$ and $f _ { R } ( t )$ . Sampling is performed during the increasing frequency ramp. The beat frequency $f _ { B }$ is the difference between overlapping transmit and receive frequency ramps. After the time interval $T _ { I }$ , that included the wait time $T _ { w a i t }$ for initial configuration and signal processing, the next chirp train is transmitted.

![](images/8ff1caf69211349afeb7bc9938d5fc7894ad311a25fb784445af2891678190ef.jpg)  
Fig. 2. Interference between mid and long range radar systems. During decreasing ramps no sampling is performed. Shaded areas in the frequency over time aggregation below the scenario indicate interfering frequency ramps.

$$
\begin{array}{c} f _ { R } ( t ) = \sum _ { p , k = 0 } ^ { P , K - 1 } \sum _ { l _ { k } = 0 } ^ { L _ { k } - 1 } \left[ \alpha ( t - 2 \tau _ { r , l k } - p T _ { p } ) + f _ { D , l k } \right]  \\ { \cdot \mathrm { r e c t } \left( \frac { t - t _ { u p } - 2 \tau _ { r , l k } - p T _ { p } } { t _ { u p } } \right) } \end{array} .\tag{7}
$$

The beat frequency equals the difference $f _ { B } ( t ) = f _ { T } ( t ) - f _ { R } ( t )$ between transmit and receive signal (Figure 1) and, therefore, features significantly lower spectral components than the baseband signal:

$$
f _ { B } ( t ) = \sum _ { p , k = 0 } ^ { P , K - 1 } \sum _ { l _ { k } = 0 } ^ { L _ { k } - 1 } \left[ \alpha \tau _ { r , l k } - f _ { D , l k } \right] \cdot \mathrm { r e c t } \left( \frac { t - \tau _ { r , l k } - t _ { u p } - p T _ { p } } { t _ { u p } } \right)\tag{8}
$$

Alternatively, the beat frequency can be expressed as the sum of its range and Doppler components, i.e. $\begin{array} { r } { f _ { B } ( t ) \stackrel {  } { = } \sum _ { k , l _ { k } = 0 } ^ { K , L _ { k } - 1 } f _ { r , l k } + f _ { D , l k } } \end{array}$ with $\begin{array} { r } { f _ { r , l k } = \alpha \tau _ { r , l k } = \alpha \cdot \frac { 2 r _ { l k } } { c } } \end{array}$ representing the frequency component resulting from the signal propagation in FMCW systems and $f _ { D , l k } =$ $\begin{array} { r } { \alpha \cdot \frac { - 2 v _ { l k } \cdot p T _ { p } } { c } } \end{array}$ equals the Doppler component. The range and Doppler components of the beat frequency are extracted using DFTs in fasttime (signal samples within a ramp) and slow-time (signal samples within several ramps) domains [24].

## III. COGNITIVE ILLUMINATION EXPERIMENTS

Typically, automotive radar systems that tackle the challenges of increased noise floors and density of interfering sources, prefer those approaches that use commercial radar chips and do not disturb other conventional automotive radar systems. Radar systems meet these different application constraints by usually adapting bandwidth and chirp length. For instance, Figure 2 shows a mid-range radar system with a broad opening angle, wide bandwidth and reduced range interfering with a long range radar. This flexibility in design parameters enables implementation of a more sophisticated interference mitigation than simply pausing radar illumination in the presence of a second radar system. We implemented a cognitive approach according to Figure 3, which allocates chirps on free center frequencies within the complete allocated frequency range while adjusting chirp bandwidth and length to available frequency and time allocations, thus allowing a flexible and persistent radar usage during the presence of interfering radar systems. In the following subsections, we describe the radar hardware, experimental environment, measurements performed, and the impact of chirp rate adjustment on radar perception regarding range.

![](images/e29383951b85840d089e654f07c157f2804c610e80100663b2bafa9acbb79122.jpg)  
Fig. 3. The allocated frequency band for automotive radar stretches from 76 GHz to 81 GHz. Given a long range (blue) and mid range (orange) radar system with 500 MHz and 1 GHz bandwidth, a third cognitive radar system can allocate its frequency ramp either in between transmission pauses with chirp rates adopted to available resources or operate at the remaining bands that are outside of the bandwidth of the other radar receivers.

The experiments were performed using INRAS automotive radar development platform with Infineon RCC1010 processing chip. The hardware is capable of varying linear chirps in the range 76 −81 GHz. Even though this sweep covers 5 GHz, measurements with a maximum bandwidth of only 4 GHz are possible. Therefore, we used the frequency range 76 −80 GHz. The partial bandwidth $B _ { p }$ of each chirp was 1 GHz resulting in 15 cm range resolution. In modulated systems such as LFMCW radars, the range resolution $\Delta r$ depends directly on the bandwidth and corresponds to $\begin{array} { r } { \Delta r = \frac { c } { 2 B } } \end{array}$ with c being the signal propagation velocity through a medium. The propagation velocity in air equals the speed of light. Four transmit $( \mathrm { T X 1 } , . . . , \mathrm { T X 4 } )$ and eight receive (RX1, ..., RX8) antennas spaced by $7 \lambda / 2$ and $\lambda / 2$ , respectively, create a virtual antenna of 32 elements. We used the transmitting-receiving antenna sets {TX1, RX1, ..., RX8} and {TX3, RX1, ..., RX8}.

Different scenarios, such as intersections or highways, require parameter adaptations regarding bandwidth and timing that are partially restricted by hardware. The required sampling frequency in fasttime is related to the maximum beat frequency as $f _ { s } = 2 f _ { b , m a x }$ thereby setting an ultimate hardware constraint to the maximum range and velocity. The maximum range results from the number of samples N and the range resolution according to $\begin{array} { r l } { r _ { m a x } } & { { } = } \end{array}$ $\Delta r \cdot \frac { N } { 2 }$ . With the maximum range the maximum frequency shift due to range propagation is computed for LFMCW systems with $\begin{array} { r } { f _ { r , m a x } \ = \ \hat { \frac { B } { t _ { u p } } } \cdot \hat { \frac { N } { c } } \frac { \hat { \Delta } r } { c } \ = \ \frac { N } { 2 t _ { u p } } } \end{array}$ . The maximum relative velocity depends on the pulse period $\overset { \cdot } { T _ { p } } ,$ i.e. the slow-time sampling rate, and, therefore, equals $\mathsf { \bar { \Psi } } _ { v _ { p , m a x } } \mathsf { \bar { \Psi } } = f _ { D } \mathsf { \Psi } \cdot \frac { c t _ { u p } } { 2 T _ { p } }$ [25], [26]. Since the maximum Doppler shift is limited by the maximum bandwidth of the system, with the ADC input being the ultimate constraint, the maximum Doppler frequency is $f _ { D , m a x } = B / 2$ . This implies the maximum velocity is $\begin{array} { r } { v _ { p , m a x } = \frac { c t _ { u p } } { 4 T _ { p } } } \end{array}$ . The velocity resolution $\Delta v _ { p }$ depends on the maximum velocity per number of slow-time samples $\begin{array} { r } { \hat { N _ { p } } \colon \Delta v _ { p } = \frac { 2 | v _ { p , m a x } | } { N _ { n } } } \end{array}$

The maximum sampling frequency of the hardware is 20 MHz. With $\begin{array} { r } { f _ { s } = 2 f _ { r , m a x } = \frac { N } { t _ { u v } } } \end{array}$ the minimum required sampling frequency is given. Eventually, the frequency needs to be decreased, if the internal cascaded-integrator-comb (CIC) filter is applied for the sake of system robustness. The order of the CIC filter affects the number of samples N according to $\begin{array} { r } { N = t _ { u p } \frac { 2 0 \ \mathrm { M H z } } { N _ { d i v } } } \end{array}$ , where the filter order $N _ { d i v }$ corresponds to the frequency division. We applied a CIC filter of order $N _ { d i v } = 4$ and chose the minimum applicable ramp duration $t _ { u p }$ that is 71 µs for the partial bandwidth chirps. Two reference full FMCW radar implementations were used. The first employs the same chirp duration as the chirps covering only the partial bandwidth (thus, drastically lowering the maximum range). The second implementation features an increased up-time $t _ { u p } ~ = ~ 4 ~ \cdot ~ t _ { u p , m i n }$ . The aim is to determine the effect of cognitively reducing the chirp bandwidth in order to mitigate interference with other radar sensors, while still being able to sense the environment, whereas the separability in range direction should be preserved. Since the measurements capture static scenarios, only range profiles were evaluated.

## IV. MEASUREMENT RESULTS

Figure 4 shows the first experimental set-up with the corner reflector. The second scenario has two parked cars and several columns of the parking house. As mentioned earlier, bandwidth and chirp length affect the maximum range. Increasing the chirp length of the full bandwidth to $4 \cdot t _ { u p } = 4 \cdot 7 1 \mu s$ results in 1416 samples taken during the linear chirp and a maximum range of 26.5 m. Allowing only 71 µs for sweeping over a 4 GHz bandwidth results in 6.6 m of maximum range, while covering only a bandwidth of 1 GHz allows a maximum range of 106.2 m. Therefore, all measurements were performed for the range 1 m to 6 m and 2 m to 26 m to cover two different chirp rate configurations. The ultimate short range measurements allow to compare measurement results for a time-compensated full bandwidth with a configuration that foresees for each chirp the same chirp length without regarding the covered bandwidth.

Figure 5 shows the range profiles resulting from measurements with the corner reflector located at 16 m. Each subfigure plots all eight receive channels from the full receive array. Although only the corner reflector representing a RCS of $1 0 0 \mathrm { { m } ^ { 2 } }$ was placed in front of the radar, several repeating peaks are visible in the range profile that result from both, columns and multipath components of the rectangular parking house aisle. From left to right a slight decrease in received signal power can be observed, resulting from the increasing free space attenuation that originating from the increasing carrier frequency. Since the eight receive antennas are placed close to each other with the distance $\lambda / 2 ,$ , from the receive signals alone there is not much of spatial diversity, at least not in this range. However, the comparison between the upper and lower line, that belong to the transmit antennas TX1 and TX3 and are therefore spaced by 7λ, the spatial diversity becomes obvious and supports the detection of otherwise obscured peaks, such as the peaks at 6 m and 8 m.

Figure 6 depicts the measurement results for the parking house scenario in an analogous way. Significant reflectors are annotated by a laser rangefinder and matched to the range profiles. Increasing the carrier frequency results in peaks that are closer together thereby increasing the separability of objects that feature more complexity in their surface. The structure of the rear of the car that is closer to the radar features reflecting targets at 4.7 m and 4.9 m, which are best distinguishable in the band from 79 GHz to 80 GHz. Superposition of different bands therefore helps to compensate the decrease in range resolution caused by the decrease in bandwidth. Compared to the range profile in the same frequency band but received with TX3 instead of TX1, the two peaks show an almost equal level, which helps to recognize and cluster the object. The second car has two significant targets at the front and the rear wheel, i.e. 11.6 m and 14.2 m. This is best seen with TX1 in the lowest frequency band. Comparing TX1 and TX3 reveals that while the column located at 16 m is obscured by the rear wheel while evaluating TX1, the rear wheel vice versa is obscured by the column while using TX3. Hence, using spatial diversity helps to reveal the complete target scenario.

![](images/fea7981fe44d285a8d1e4be2978b09a38fd4ed1a50f30097a847ef593ac90434.jpg)

Fig. 4. Experiment setups: (a) Corner reflector placed at 16 m and (b) 3 m distance. (c) The corner reflector and its positioning details. (d) Profile of the measurement setup. (e) Second experiment features parked cars and columns of the parking house with annotated distance in range. The monitor of the host PC that is used to operate the radar shows the range profile and the range-Doppler map generated online from the measurements.  
![](images/91fa2bce0eaf300cd9147de8c03ec9423a8fc3a921aa706a78043fff63359c65.jpg)  
Fig. 5. Range profile for corner reflector located at 16 m. The upper line shows the range profile measured while TX1 is activated and the bottom line while TX3 is active. The columns display the range profiles from chirps covering the frequency ranges (from left to right) 76-77 GHz, 77-78 GHz, 78-79 GHz and 79-80 GHz. Besides the peak at 16 m that indicates the position of the corner reflector, other peaks result from the surroundings, such as the columns of the parking house or multipath reflections from the ceiling and the floor.

For a corner reflector is placed at a range of 3 m, Figure 7 shows the range profile of TX1 measurements on left side. Again, the slightly different frequency bands help to compensate the loss in range resolution by limiting the chirp bandwidth. The plots on the right compare the range profiles obtained from the full bandwidth of 4 GHz. The first column contains the measurement results of the minimum chirp length $t _ { u p }$ with 71 µs and the second column the results from the four times longer chirp length. Increasing the chirp length increases the received peak level, while also widening the peak. Comparing TX1 and TX3 reveals also here the benefit of spatial diversity by sharpening the peaks below 2 m.

The increased peak power related to a longer chirp duration is even more significant in the more complex parking house scenario, whose results are depicted in Figure 8. The resolution of the full bandwidth provides clearly distinguishable peaks from the column at 4.2 m and also from the first car’s surface topology that produces peaks at 4.7 m and 4.9 m. The acquisition results using the reduced bands that are depicted on the left hand side for TX1 measurements, show the complementary range profiles for the four different carrier frequencies. While the separation of the 4.7 m and 4.9 m components are lost for the 1 GHz frequency band around 77.5 GHz, both peaks are separated for the lower and higher neighbor frequency bands.

![](images/6a6d60c47c801a8f36e5c4a29f84db2a768ee7e26a148149d75ed0a7840a9436.jpg)

![](images/2f549e35f73f517df7a23c056e0cfb8677bc2ab26b0c432b8f2e10ca791e6385.jpg)

![](images/ba6549b10f0afaf69ab5e764e693760a2269109e9eaba07e0f3b027f3f91f1f8.jpg)

![](images/34a7a9665489bceedbed8cb6ca38f6bb52c36f0aa5eae941dcdb17481cad12fc.jpg)

![](images/f52e7441689fcfef54d628ab2040e8d04761992893ee49f2f844e40212f3a606.jpg)

![](images/178585080e873e852e357f90f7887dc372e0a75945a7dfe69f0abde8de57e0b9.jpg)

![](images/faef2db7eaae5d3c422a128806800846f73146ce6ff2e1b4e9d7dd806c9d91f0.jpg)

![](images/d523c701917e0fd2cce7dbf2fa7127309217e7d36b498ca45d6b26d4777de8ea.jpg)  
Fig. 6. Range profile of parking house scenario with two cars and several columns. The surface of the closest car reflects at 4.7 m and 4.9 m. The second car reflects at 11.6 m and 14.2 m. Columns are located at 4.2 m, 16.0 m, 22.0 m and 19.0 m. The column at 9.0 m features an additional metal sheet that is 25 cm deep. The first line belongs to an active TX1 and the lower to TX3. Each column represents the measurement of one partial bandwidth.

![](images/5420289cfd6b26fe26d1c5144ef8964305f3fc03759c9428e49ee1f5ca9c2514.jpg)

![](images/fc3943784419db3a7b4bda5814fceb144194a43860fab1ad653b28be6954fa5a.jpg)

![](images/b850560915cdeb64909e6c9415a255bbc32859ec1a9c3af19221e79243e6ffb2.jpg)

![](images/642ce51c1b0cdf759437815a53149b834b1e71afc4014e57cad06cab6af9be97.jpg)

![](images/96f39d8fe282312ee646b0755831ce5ceac89d54e50ff2024f4f84b65f226538.jpg)

![](images/00b12621407c49f4362d12cb4e35455d3867a45886be74ef1d235c25fed68bd0.jpg)

![](images/80a5e34440d3a860696c900f5cf2f6938803806c219d06030221982ae07ec83d.jpg)

![](images/58ace60232759d4826b01f37ac1e89f273ce325294b5fa0d5eac3b1b8435a45a.jpg)  
Fig. 7. Range profile of corner reflector located at 3 m. The range profiles obtained from partial bandwidth coverage are displayed in a) from TX1. b) shows the range profile for the full bandwidth, whereas the first column represents $t _ { u p } = 7 1$ µs. The first line results from TX1 illumination and the second from an active TX3.

![](images/d24cea0f200279dd43b7fe843a2e303adf1e01e2c6455461e23e1fadaf0b11d4.jpg)

![](images/7f161760a434d8b068d308d42c7b0ab35490e1b35a996ae6088c98f1df8d7cc2.jpg)

![](images/fe79472a847807427eb952a6864182d9508863950ce66b8aed742f00b7209c13.jpg)

![](images/3bd1b0757f4cd1e3d0d7c48302922cea3ecec2489d18c7b6db0ecd2812a940f1.jpg)

![](images/032671f0b3f100ab0436fcd736f549d4be70c821e1f7722d72b5b68efac28354.jpg)

![](images/d0e1315c1e633506744be272fb16ceb1f1290116ca7cb654bd090a69d8851b0c.jpg)

![](images/08b07ae9538a3f6ae8e8acee8e00db9a6d1c34f80c3e1510d964081f501f3eb1.jpg)

![](images/6d614cf68b5b46846ff463a6a04d10fad7235c2fe55f35e8350ee49184aee0d1.jpg)  
Fig. 8. Range profile of parking house scenario up to 6 m. Therefore, only the car at 4.7 m and 4.9 m is visible together with the column at 4.2 m. In a) the range profiles obtained from TX1 are displayed, while 1 GHz chirps were applied. The range profiles from the whole bandwidth are displayed in b). As previously, the first column represents $t _ { u p } = \bar { 7 } 1$ µs and the second $4 \cdot t _ { u p } = 2 8 4 \bar { \mu }$ s. The first line results from TX1 illumination and the second from an active TX3.

The measurements show, that by cognitive selection of chirp bandwidth and carrier frequency the radar performance can be sustained compared to a chirp covering the complete designated bandwidth. In addition, the chirps that cover only parts of the complete bandwidth can be reduced in chirp length by 25 % compared to the full bandwidth chirp and still extend the range from 26.5 m to 106.2 m. In comparison to the range of the full bandwidth chirp while keeping the chirp duration of 71 µs, the range is even increased by a factor of 16, since the range is otherwise limited to 6.6 m. Superposition of measurements obtained from the different partial frequency bands can compensate the loss in range resolution and obtain with only 25 % of the bandwidth an approximately equal separability compared to the full bandwidth. Using also the spatial diversity of antenna arrays, the superposition of measurements reveals reflecting targets that are otherwise obscured. Therefore, not only the signal-to-noiseratio (SNR) is increased, but also the separation of targets that occur within an object, which results from different angle-of-arrivals (AoA). Using partial bandwidth chirps and applying them to a MIMO frontend therefore allows to reduce the chirp duration and increase the radar range while preserving the range resolution by superposing different frequency bands.

## V. SUMMARY

In order to meet the requirements on robustness towards interference while acknowledging the persistence of commercial automotive radar systems, we demonstrated the operation of a cognitive LFMCW radar system using the state-of-the-art radar chip for automotive 77 GHz radar systems. Our measurements show that chirps of a reduced bandwidth mitigate frequency bands that are occupied by other radar systems and allow reduction of the chirp duration while increasing the radar perception range by a factor of 16. This facilitates not only an additional time division multiplexing by transmitting the reduced chirps in radar transmission pauses that are implemented on a regular hardware for configuration and signal processing, but also allows a four times faster signal acquisition.

## ACKNOWLEDGEMENTS

This work has been conducted within the ENABLE-S3 project that has received funding from the ECSEL Joint Undertaking under Grant Agreement no. 692455. This Joint Undertaking receives support from the European Unions HORIZON 2020 research and innovation programme and national funding from participating countries. Additionally, this work was partially supported under the Federal Ministry of Education and Research (BMBF) grant 16ESE0132. K. V. M. was supported by the Iowa Flood Center.

## REFERENCES

[1] H. Hartenstein and L. Laberteaux, “A tutorial survey on vehicular ad hoc networks,” IEEE Communications Magazine, vol. 46, no. 6, pp. 164–171, 2008.

[2] N. Lu, N. Cheng, N. Zhang, X. Shen, and J. W. Mark, “Connected vehicles: Solutions and challenges,” IEEE Internet of Things Journal, vol. 1, no. 4, pp. 289–299, 2014.

[3] Y. Zhao and Y. Su, “Vehicles detection in complex urban scenes using Gaussian mixture model with FMCW radar,” IEEE Sensors Journal, vol. 17, no. 18, pp. 5948–5953, 2017.

[4] K. V. Mishra, S. S. Ram, S. Vishwakarma, and G. Duggal, “Dopplerresilient 802.11ad-based ultra-short range automotive radar,” arXiv preprint arXiv:1902.01306, 2019.

[5] Z. Slavik, O. Bringmann, W. Rosenstiel, and Y. C. Eldar, “Implications and methods for co-existing automotive radar and communication systems,” in 2018 52nd Asilomar Conference on Signals, Systems, and Computers, Oct 2018, pp. 952–956.

[6] G. R. Muns, K. V. Mishra, C. B. Guerra, Y. C. Eldar, and K. R. Chowdhury, “Beam alignment and tracking for autonomous vehicular communication using IEEE 802.11ad-based radar,” in IEEE Infocom Workshops - Hot Topics in Social and Mobile Connected Smart Objects, 2019, in press.

[7] D. Kissinger, Radar Fundamentals. Boston, MA: Springer US, 2012, pp. 9–19.

[8] Z. Slavik and K. V. Mishra, “Phenomenological modeling of millimeterwave automotive radar,” in URSI Asia-Pacific Radio Science Conference, 2019, in press.

[9] H. H. Meinel, “Evolving automotive radar From the very beginnings into the future,” in IEEE European Conference on Antennas and Propagation, 2014, pp. 3107–3114.

[10] S. H. Dokhanchi, B. S. Mysore, K. V. Mishra, and B. Ottersten, “A mmWave automotive joint radar-communications system,” IEEE Trans Aerosp. Electron. Syst., 2019, in press.

[11] F. Meinl, M. Stolz, M. Kunert, and H. Blume, “An experimental high performance radar system for highly automated driving,” in IEEE International Conference on Microwaves for Intelligent Mobility, 2017, pp. 71–74.

[12] M. Dudek, I. Nasr, G. Bozsik, M. Hamouda, D. Kissinger, and G. Fischer, “System analysis of a phased-array radar applying adaptive beamcontrol for future automotive safety applications,” IEEE Transactions on Vehicular Technology, vol. 64, no. 1, pp. 34–47, 2015.

[13] H. Bloecher and J. Dickmann, “Automotive radar sensor interference Thread and probable countermeasures,” in International Radar Symposium, 2018, pp. 1–7.

[14] M. Goppelt, H. Bloecher, and W. Menzel, “Automotive radar - Investigation of mutual interference mechanisms,” Advances in Radio Science, vol. 8, no. B. 3, pp. 55–60, 2010.

[15] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in IEEE Radar Conference, 2018, pp. 252–256.

[16] C. Aydogdu, N. Garcia, and H. Wymeersch, “Radar communication for combating mutual interference of FMCW radars,” arXiv preprint arXiv:1807.01497, 2018.

[17] B. Nuss, L. Sit, and T. Zwick, “A novel technique for interference mitigation in OFDM radar using compressed sensing,” in IEEE International Conference on Microwaves for Intelligent Mobility, 2017, pp. 143–146.

[18] C. Knill, J. Bechter, and C. Waldschmidt, “Interference of chirp sequence radars by OFDM radars at 77 GHz,” in IEEE International Conference on Microwaves for Intelligent Mobility, 2017, pp. 147–150.

[19] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in IEEE Radar Conference, 2018, pp. 405–410.

[20] K. V. Mishra, A. Zhitnikov, and Y. C. Eldar, “Spectrum sharing solution for automotive radar,” in IEEE Vehicular Technology Conference - Spring, 2017, pp. 1–5.

[21] K. V. Mishra, Y. C. Eldar, E. Shoshan, M. Namer, and M. Meltsin, “A cognitive sub-Nyquist MIMO radar prototype,” arXiv preprint arXiv:1807.09126, 2018.

[22] O. Bar-Ilan and Y. C. Eldar, “Sub-Nyquist radar via Doppler focusing,” IEEE Transactions on Signal Processing, vol. 62, pp. 1796–1811, 2014.

[23] M. Skolnik, Radar handbook. McGraw-Hill Education, 1970.

[24] K. V. Mishra and Y. C. Eldar, “Sub-Nyquist radar: Principles and prototypes,” arXiv preprint arXiv:1803.01819, 2018.

[25] K. V. Mishra, V. Chandrasekar, C. Nguyen, and M. Vega, “The signal processor system for the NASA dual-frequency dual-polarized Doppler radar,” in IEEE International Geoscience and Remote Sensing Symposium, 2012, pp. 4774–4777.

[26] K. V. Mishra, “Frequency diversity wideband digital receiver and signal processor for solid-state dual-polarimetric weather radars,” Master’s thesis, Colorado State University, 2012.