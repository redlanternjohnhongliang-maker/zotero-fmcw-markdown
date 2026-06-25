Stephen Alland, Wayne Stark, Murtaza Ali, and Manju Hegde

# Interference in Automotive Radar Systems

Characteristics, mitigation techniques, and current and future research

![](images/33b4b99be1c785df6ff4597deb73aea9fc611858d0d33d19482945ecd2494646.jpg)  
©ISTOCKPHOTO.COM/TALA

his article examines the problem of interference in automotive radar. Different types of automotive radar as well as mechanisms and characteristics of interference and the effects of interference on radar system performance are described. The interference-to-noise ratio (INR) at the output of a detector is a measure of the susceptibility of a radar to interference. The INR is derived from different types of interfering and victim radars and depends on the location of both as well as parameters such as transmit power, antenna gain, and bandwidth. In addition, for victim radar with beamscanning, INR depends on the location of the target the victim radar is attempting to detect. Analysis is presented to show the effects of various interference scenarios on the INR. A review of the current state of the art in interference mitigation techniques previously deployed as well as areas of research currently being addressed is then provided. Finally, important future research directions are suggested.

## Vehicular sensors

Sensors for vehicular (automobiles, buses, trucks, and so on) applications are an important area of R&D. There are many different types of currently used sensors being considered for use in future vehicles, such as radars, cameras, lidars, and ultrasonics. Each of these sensors has strengths and weaknesses; good engineering judgment indicates that a combination of sensors, which complement the strengths and weaknesses of one with another, is required to maintain the integrity of safety-critical systems. For instance, radars are the best sensors for detecting range and radial velocity and have “all-weather” capability, but are weak for classification and angular resolution. Lidars, in general, have good angular resolution and range, but are limited in field of view (FOV) and have limited ability in adverse weather. Cameras have excellent color perception and classification capabilities but are limited in estimating velocity and range. Cameras also have difficulty in dark or adverse weather.

There are several different performance measures to consider when evaluating the vehicular sensors used to detect objects in the environment. A core set includes detection range, range resolution, velocity coverage, velocity resolution, FOV, angular resolution, latency (processing delay), robustness to adverse weather, night operation, target classification, and color detection for reading signs and traffic lights. In addition, the cost of a sensor is important to consider; a vehicle might need, and thus be equipped with, multiple sensors. The cost of an individual sensor is typically affected by a number of factors: the scan type (mechanical, solid state/electronic, or digital), radio-frequency (RF) circuitry, baseband and digital chipsets, the integration level of fundamental transmit and receive components, digital processing subsystem capabilities (bandwidth, throughput, and available memory), the associated packaging and required manufacturing processes, and the number of antennas used for transmission and reception. Figure 1 shows the strengths and weaknesses of different sensor systems in relation to different performance measures [1], [2]. Note that the spider plots in the figure illustrate characteristics of radar and vision systems as deployed today in millions of production automobiles, whereas for lidar, they show the potential characteristics—lidars have not been deployed in production automobiles to date.

The considerable sensor requirements for self-driving cars described previously dictate that multiple sensor modalities will be present and that radar will be an important part of that portfolio. Radars can be used to determine location and directly measure the Doppler velocity of objects in the environment. Furthermore, with the ongoing development of RF CMOS and multiple-input, multiple-output (MIMO) radar imaging technologies at 76–77 GHz and 77–81 GHz, automotive radar cost is rapidly decreasing, while overall performance and capability of radars for point cloud imaging, edge detection, and target classification will be substantially improved in the near future.

There are multiple automotive applications for radar sensors; consequently, automotive radar is an active research field [3]–[7]. Automatic cruise control, blind-spot detection, and collision-warning systems were some of the earliest applications of vehicular radar systems. Recently, other applications, including advanced driver-assistance systems, automatic emergency braking, lane-change assist, and vulnerable user detection have been implemented. Self-driving cars will increase the importance of systems that provide an accurate sensing of the environment. As such, it is certain that the number of sensors on vehicles will increase dramatically in the next 10 years. This makes the possibility of radar-to-radar interference in traffic much greater, as noted in [8] and [9].

![](images/db08e5ef6d5e468adca861aa4ea6bdfd6d797227ef9dd3819252b764cfe4ca71.jpg)  
FIGURE 1. A comparison of automotive sensors.

The problem of radar-to-radar interference will be a significant engineering challenge that the industry will have to address. There are several signal processing techniques that mitigate interference and some of these have already been implemented in radars deployed in today’s automobiles. With the increasing number of vehicles being equipped with radar and each vehicle having multiple radar sensors—several production models commercially available in the 2021–2023 time frame are investigating the possibility of deploying up to six radar systems per car—the capability of radar systems to operate in the presence of other radar systems in proximity is fast becoming a critical performance issue. As a result, interest in this area of research has increased significantly. For future radars, the ability to mitigate interference will be as critical as detection performance.

## Background

Radar systems operate by transmitting a signal; this signal is then reflected by an object or target in the environment. The radar system receiving the reflected signal compares the properties of the reflected signal to the transmitted signal [10]. A radar system with a single transmitter and receiver can estimate the range and velocity of an object in the environment; with mechanical or electronic scanning, the radar system can estimate the angle as well. A radar system with multiple receiver antennas can estimate the angle of an object via digital beamforming. With both multiple transmitter antennas and multiple receiver antennas, also known as a MIMO system, a radar can estimate the angle of an object via digital beamforming but with enhanced accuracy and resolution compared to more conventional (non-MIMO) radar [4], [6]. In general, radar can determine different object angles (e.g., azimuth and/or elevation) depending on the antenna scanning and/or the number and geometry of antenna-receiver channels.

Radar systems can be designed for different performance objectives. Some of the performance measures of a typical radar system include detection range, range resolution, maximum unambiguous range, velocity resolution, maximum unambiguous velocity, angular resolution, and FOV. An overview of various types of radars and estimation techniques for range, velocity, and direction in the absence of interference are given in [11]. Generally, with a fixed number of antennas, a radar with a broad FOV can be obtained at the expense of less angular resolution, while a narrow FOV can provide better angular resolution. The antenna configuration will determine the estimated target direction in the horizontal plane (azimuth), vertical plane (elevation), or in both. Multiple antennas at the transmitter and receiver can be used to beamform the signal or can be used in a MIMO configuration where different waveforms are transmitted from different antennas and the subsequent receive signals are processed to form a synthetic or virtual receive array. Early automotive radar used mechanically scanned antennas or several fixed antennas for one-dimensional (azimuth) angle-detection capability [12], [13]. Automotive radar is now beginning to incorporate MIMO antennas configured for 2D angle-detection capability (azimuth and elevation), with future systems moving to a greater number of transmit and receive antennas to support 2D point cloud imaging.

Fundamentally, the performance of a radar system depends on the bandwidth of the signal, the time duration over which the estimation is performed, and the geometry of the transmitter and receiver antennas. A tutorial on its performance in the absence of interference is discussed in detail in [11]. This article is focused on the effect of an interfering radar on a victim radar.

## Frequency-modulated continuous wave

One type of radar, and the most common in current automotive systems, is frequency-modulated continuous-wave (FMCW) radar. In FMCW radar, the transmitted signal is a sinusoidal signal in which the frequency of the signal varies with time. The transmitted signal is

$$
s _ { T } ( t ) = \sqrt { 2 P _ { t } } \cos ( 2 \pi ( f _ { c } + f _ { m } ( t ) ) t ) ,\tag{1}
$$

where $f _ { c }$ is the center frequency, $P _ { t }$ is the transmitted power, and $f _ { m } ( t )$ is the time-varying frequency. The frequency of the transmitted signal is then $f _ { T } ( t ) = f _ { c } + f _ { m } ( t )$ . There are different ways in which the frequency of an FMCW waveform varies. One way is via a ramp or sawtooth signal in which the frequency ramps from a minimum frequency to a maximum and then repeats. Alternatively, a signal that sweeps up in frequency (i.e., up-chirp) and then down in frequency (i.e., down-chirp) could be employed. Slopes for the up-chirp and down-chirp could vary in time as well. The time it takes for the up-chirp signal of the receiver to sweep over a bandwidth B Hz in frequency is sometimes called the chirp duration and is denoted by $T _ { c } .$ . In some cases, the frequency changes in a piece-wise linear fashion, although the times for the up-chirp and down-chirp can be different.

At the receiver, the received signal is mixed with (multiplied by) the transmitted signal and filtered with a low-pass filter of a certain bandwidth $B _ { r }$ to remove the double-frequency components as well as some of the noise and interference. Additional processing is done after converting from analog to digital signals. The filter bandwidth limits the unambiguous range of an FMCW radar. The transmitter and receiver block diagram for an FMCW radar is shown in Figure 2.

The transmitted signal is reflected off of a target and received. The received signal, in the case of a stationary target, is an attenuated and time-shifted version of the transmitted signal. Based on propagation of signals at the speed of light, the delay x is related to the range by $R = \tau c / 2 \ \mathrm { o r } \ \tau = 2 R / c$ This is true for any type of radar signal, not just FMCW. The result of mixing the FMCW-transmitted signal with the received signal will be a signal with frequency proportional to the delay between the radar and the target. Filtering after mixing limits the range of targets that can be detected. The frequency of the signal after mixing and filtering is proportional to the delay between the transmitter and receiver and thus proportional to the range of the target. Suppose $R _ { \mathrm { m a x } }$ is the range of the furthest target to be detected. Then the corresponding maximum delay is $\tau _ { \operatorname* { m a x } } = 2 R _ { \operatorname* { m a x } } / c$ . The maximum frequency shift is then $f _ { \mathrm { m a x } } = 2 B R _ { \mathrm { m a x } } / ( c T _ { c } )$ . The minimum frequency shift is 0 corresponding to a target at distance 0. The filter must have a bandwidth at least as large as this maximum beat frequency. Equivalently, if the low-pass filter has bandwidth $\boldsymbol { B } _ { r }$ the largest range that can be detected is $R _ { \mathrm { m a x } } = c T _ { c } B _ { r } / ( 2 B )$ For example, if the chirp duration is 30 μs, the sweep bandwidth is 300 MHz and the filter bandwidth is $B _ { r } = 1 5 ~ \mathrm { M H z } ,$ then the maximum range is 225 m. For automotive applications, this might be considered a long-range radar (LRR). If the sweep bandwidth is 750 MHz, the sweep time is $5 0 \mu \mathrm { s }$ and the IF bandwidth is $B _ { r } = 4 . 5 ~ \mathrm { M H z }$ , then the maximum range is 45 m and would be considered a short-range radar (SRR). Generally, a larger bandwidth B will enable better range resolution in a radar. An SRR would typically require better range resolution than an LRR and thus, use a larger bandwidth.

## Phase-modulated continuous wave

Another type of radar is phase-modulated continuous-wave (PMCW) radar. In a PMCW radar system, the transmitted signal

![](images/586c980d657ea2d14f01f712145e207997bc7f9f9370498b77c662d6aa56d3c4.jpg)  
FIGURE 2. The block diagram of an FMCW system. DAC: digital-to-analog converter; ADC: analog-to-digital converter; VCO: voltage-controlled oscillator; PA: power amplifier; LNA: low-noise amplifier.

is a sinusoidal signal in which the phase varies with time. The transmitted signal for PMCW radar has the form

$$
s _ { T } ( t ) = \sqrt { 2 P _ { t } } \cos { ( 2 \pi f _ { c } t + \phi _ { m } ( t ) ) } ,\tag{2}
$$

where $\phi _ { m } ( t )$ is the modulated phase waveform. The total phase of the transmitted signal is $\phi _ { T } ( t ) = 2 \pi f _ { c } t + \phi _ { m } ( t )$ . One way of generating the phases is to begin with what is known as a spreading code. A spreading code consists of a sequence of chips $( \mathrm { e . g . , + l , + l , - l , + l , - l , } , \dots )$ with a chip duration $T _ { c } ,$ which is mapped $( \mathrm { e . g . , + 1 } \to 0 , - 1 \to \pi )$ into a sequence of phases $( \mathrm { e . g . , 0 , 0 , } \pi , 0 , \pi , \dots ) .$ , and the phases are used to modulate the RF sinusoidal signal. The phase can be limited to either 0 or r radians (180°) or it can be arbitrary. In the event that the signal phase is only either 0 or r radians, the signal is said to be a binary phase modulated signal. A binary phase modulated signal can also be generated by multiplying a binary (+1 and –1) signal $a ( t )$ with a carrier. In the case of binary spreading codes, the transmitted signal can be written as

$$
s _ { T } ( t ) = \sqrt { 2 P _ { t } } a ( t ) \cos \left( 2 \pi f _ { c } t \right) .\tag{3}
$$

The spreading code $a ( t )$ could be a periodic sequence with a short period or could be a pseudorandom sequence with a very long period so that it appears to be a nearly random sequence. Codes or sequences with good autocorrelation properties are important for use in PMCW-type radar systems. There are many possible spreading codes, including Barker sequences, m-sequences (also known as linear feedback shift register sequences), and gold codes, all of which are binary codes. There are also nonbinary codes such as the Zadoff–Chu codes. More information about spreading codes can be found in [14]. The resulting modulated RF signal has a bandwidth that is proportional to the rate at which the phases change, called the chip rate, which is the inverse of the chip duration, T<sub>c</sub>.

The receiver, as shown in Figure 3, first mixes the received signal s t<sub>R</sub> ( ) down to baseband and then filters the result to remove unwanted frequency components before converting it to digital signals. The digital signals are processed with a filter matched to the transmitted signal (as part of the digital signal process unit shown in Figure 4). A peak in the magnitude of the filter output is indicative of a target at a certain distance from the radar.

By comparing the return signal to the transmitted signal, the receiver can determine the range and velocity of objects in the environment. The digital signal processing block includes a matched filter, which correlates the received signal to all possible delays of the transmitted spreading code. For the delay that matches the delay of the reflected signal, the correlation will be high, and a target at a given distance corresponding to the delay will be detected. The wider the bandwidth, the finer the ability of the receiver to resolve two objects near each other. The matched filter will provide correlations to replicas of the transmitted spreading code of some length. The longer the length of the spreading code used to correlate, the greater the ability to detect—unambiguously—targets at a long distance.

Although there are other types of radar signals being considered for automotive applications (e.g., [15]), this article’s focus is only on these two types of radars (i.e., FMCW and PMCW) and how one or more radars of one type causes interference with another radar of either the same or a different type.

## Interference in automotive radar systems

One fundamental reality for automotive radar is the potential for mutual interference due to multiple radars operating simultaneously in “close proximity” and direct line of sight [16]. Analyses and test results involving automotive radar indicate that mutual interference can be substantial unless suitable mitigation is employed.

Figure 4 shows two scenarios where in each, a vehicle with an “interfering” radar is creating interference for a “victim” radar. Consider the leftmost example scenario shown in Figure $^ { 4 , }$ with a single interfering radar at a distance R mounted on a vehicle that also acts as a target for the victim radar. In this case, the distance from the target and the distance from the interferer are identical. The signal powers received by the victim radar for the vehicle target ( )P<sub>r</sub> and the interference ( )P<sub>I</sub> are given by

$$
P _ { r } = \frac { P _ { t } G ^ { 2 } \lambda ^ { 2 } \sigma } { ( 4 \pi ) ^ { 3 } R ^ { 4 } } , P _ { I } = \frac { P _ { t } G ^ { 2 } \lambda ^ { 2 } } { ( 4 \pi ) ^ { 2 } R ^ { 2 } } ,\tag{4}
$$

![](images/b8794a8e6a95ca022c900e2775dcb49487aab8374a06f7639c79c8455705bc2b.jpg)  
FIGURE 3. A block diagram of PMCW radar.

where P<sub>t</sub> is the transmitted power of the victim radar, $\lambda = c / f _ { c }$ is the wavelength of the transmitted signal, the antenna gain in the direction of the target is $G ,$ and the radar cross section (RCS) of the target is v (i.e., the effective reflection area) [17]. The RCS is often stated in units of either square meters or “units” of dBsm, which refers to dB relative to $1 ~ \mathrm { m } ^ { 2 }$ [i.e., in v $\mathrm { d B s m } = 1 0 \log ( \sigma / m ^ { 2 } ) ]$ .  The received interference power in (4) assumes that the interfering radar has the same transmitter power and antenna gain as the victim radar and is located at the same range as the target. For example, the interferer could be colocated with the target. The signal-to-interference ratio (SIR) at the victim radar receiver is then

$$
\frac { P _ { r } } { P _ { I } } = \frac { \sigma } { 4 \pi R ^ { 2 } } , ~ \mathrm { S I R } = G _ { p } \frac { P _ { r } } { P _ { I } } = \frac { G _ { p } \sigma } { 4 \pi R ^ { 2 } } .\tag{5}
$$

Here, $G _ { p }$ is the processing gain of a matched filter in the victim radar, which improves the SIR. Still, the SIR can be low enough to inhibit target detection. For example, given a 10-dBsm RCS typically assumed for a small-to-midsize passenger car, and a processing gain of 50 dB, the SIR falls below 10 dB for a range greater than approximately 90 m. In practice, the RCS for a vehicle can vary substantially with the aspect angle. For example, the RCS can vary from 0 dBsm to as high as 30 dBsm at 77 GHz for midsize passenger cars, as shown in [18] for a Mazda 6. Even small changes in the aspect angle seen on a frame-toframe basis can lead to fluctuation in the observed RCS. Hence, statistical RCS models (e.g., the well-known Swerling models) are often used to predict automotive radar performance.

In general, the parameters of the victim and interfering radar are different, and the victim radar is required to detect targets of varying range and the RCS over a defined FOV. Furthermore, automotive radar processing gain is limited by a number of factors, including the required update time interval specified to cover the FOV (typically on the order of 50 ms).

For radar, a relevant performance metric is the INR after processing in the victim radar. In general, the INR depends on the parameters of the victim and interfering radars, signal modulation characteristics of the interfering radar, and demodulation/downconversion processing employed by the victim radar. For simplicity, consider noise-like interference spread uniformly over the passband of the victim radar. This is often the case and will result in the lowest overall INR. If the interfering radar has bandwidth B, then the power spectral density ( ) PSD $) _ { \mathrm { i n t } }$ of the interference at the victim radar is given by

$$
\mathrm { P S D } _ { \mathrm { i n t } } = \underbrace { \bigg [ \frac { P _ { t } G _ { T } \lambda L _ { T X } L _ { f } N _ { T X } } { B ( 4 \pi R ^ { 2 } ) } \bigg ] } _ { \mathrm { I n t e r f e r i n g ~ R a d a r } } \underbrace { \bigg [ \frac { G _ { R } \lambda L _ { R X } L _ { f } N _ { R X } } { 4 \pi } \bigg ] } _ { \mathrm { V i c t i m ~ R a d a r } } ( D _ { F } ) ( K ) ,\tag{6}
$$

$$
= \Bigg [ \frac { P _ { t } N _ { T X } G _ { T } L _ { T X } L _ { f } \lambda ^ { 2 } G _ { R } L _ { R X } L _ { f } N _ { R X } } { B ( 4 \pi R ) ^ { 2 } } \Bigg ] ( D _ { F } ) ( K ) ,\tag{7}
$$

where $G _ { T } ( G _ { R } )$ is the antenna gain for the interfering (victim) radar, m is the wavelength of the radar signal, $P _ { t }$ is the transmitted power of the interfering radar, $N _ { T X } ( N _ { R X } )$ is the number of transmitting (receiving) antennas for the interfering (victim) radar, $L _ { T X } ( L _ { R X } )$ is the transmit (receive) loss for the interfering (victim) radar, and $L _ { f }$ is the loss due to the fascia (e.g., the auto’s bumper) of both radars. The duty factor parameter $D _ { F }$ accounts for the fraction of time the interfering radar operates within the dwell time and band of the victim radar; hence, the value of $D _ { F }$ varies from 0 to 1.

The parameter K generally applies to the case of FMCW modulation for both the victim and interfering radars and is given by the inverse ratio of the interference PSD in the victim radar receiver at RF prior to downconversion versus the interference PSD at baseband after downconversion in the victim radar, i.e.,

![](images/570c2829d2a3bfeab0559ca479ca97026ec33b3e4d39434260d6b59f578143ff.jpg)  
FIGURE 4. Example interference scenarios for automotive radar.

$$
K = { \frac { \mathrm { P S D } _ { I } ^ { \mathrm { B B } } } { \mathrm { P S D } _ { I } ^ { \mathrm { R F } } } } = { \frac { \Delta F _ { I } ^ { \mathrm { R F } } } { \Delta F _ { I } ^ { \mathrm { B B } } } } ,\tag{8}
$$

where $\mathrm { P S D } _ { I } ^ { \mathrm { R F } }$ is the PSD of interference at RF prior to downconversion in the victim radar receiver, $\mathrm { P S D } _ { I } ^ { \mathbf { \hat { B } B } }$ is the PSD of interference after downconversion in the victim radar receiver, $\Delta F _ { I } ^ { \mathrm { R F } }$ is the RF sweep bandwidth of the FMCW interfering radar, and $\Delta F _ { I } ^ { \mathrm { B B } }$ is the interference bandwidth in the FMCW victim radar receiver after downconversion to baseband. The interference bandwidth at baseband after downconversion in the victim radar receiver depends on the FMCW slopes of the interfering and victim radars (as well as their time and frequency alignment) and, for “similar” FMCW slopes, can be significantly less than the RF sweep bandwidth of the FMCW interferer. In this situation, $K \gg 1$ as the FMCW interference is concentrated into a narrow bandwidth in the FMCW victim radar receiver, thereby increasing its PSD.

For situations with, e.g., PMCW employed by either the victim or interfering radar, K is generally equal to unity. Interference mechanisms and characteristics for both FMCW and PMCW modulations are discussed later in the “Mechanisms and Characteristics of Interference” section. In the case of FMCW modulation used by both the interferer and victim, the “Mechanisms and Characteristics of Interference” section includes equations and results for parameter K for two different examples of time and frequency alignment.

The PSD of the noise is $\mathrm { P S D } _ { \mathrm { n o i s e } } = k T _ { 0 } F _ { n } ,$ where k is Boltzman’s constant, $T _ { 0 } ,$ is the temperature in Kelvin, and $F _ { n }$ is the noise factor of the receiver. Finally, the INR is

$$
\mathrm { I N R } = \frac { \mathrm { P S D } _ { \mathrm { i n t } } } { \mathrm { P S D } _ { \mathrm { n o i s e } } } .\tag{9}
$$

Without mitigation, the resulting INR can be substantial depending on the range and RF bandwidth of the interfering radar.

In a dynamic on-road encounter, interference seen by a victim radar will vary depending on a number of factors, including the relative position of the interfering radar (range and cross range) and the orientation and shape of the victim and interfering radar antenna patterns, as illustrated in Figure 5. The evaluation of performance versus the geometry of victim and interferer is also addressed in [17].

Figure 5 shows contours of constant INR depending on the location of an interfering radar relative to a victim radar. The simulation is based on the theoretical equation for INR, i.e., (9). The situation depicted considers a victim radar facing an opposing interfering radar. The closer the interfering radar is to the victim radar, the larger the INR, and the worse the performance is. Parameters typical of MIMO automotive medium-range radar (MRR) were used. Both victim and interfering radars are assumed to be FMCW radars with “dissimilar fastcrossing” slopes such that K = 1. When the interfering radar is approximately 150 m downrange from the victim radar, the interference is roughly 10 dB above the thermal noise level. As such, without interference mitigation, the performance of the victim automotive radar may degrade considerably.

![](images/9769e02800734473af2cb7a85da4ad28001835114b0af4523f66dfdf736992ed.jpg)  
FIGURE 5. Example INR contours for representative MIMO automotive MRR receive beams at 0 and $^ { 2 ^ { \circ } , }$ , respectively (the x–y grid is in the position of interfering radar relative to the victim radar located at 0,0). MRR: medium-range radar.

![](images/a515b6c9e8155616277857e0aa4fd569e79dcef1d7bbd0da2e4425643a9cd3b1.jpg)

Spatial discrimination of MIMO beamforming offers mitigation of interference for beams not pointed in the direction of the interfering radar, as shown in Figure 5 for two beam positions of the MIMO victim radar, i.e., 0 and 2°, respectively. Of course, with the potential for multiple interfering radars to be spread across the FOV, the mitigation offered by beamforming may be substantially diluted.

As seen in Figure 5, the INR will increase as the interferer range decreases. Additionally, the interference level can be substantially greater for situations with interferers of higher radiated power density such as automotive LRR or traffic control radar. The MOre Safety for All by Radar Interference Mitigation (MOSARIM) project [16], [19], [20] concluded that: “For automotive radars, without any mitigation technique applied, the interference power can exceed the noise level by 20 to 50 dB. The achieved results show that for typical antenna and modulation parameters, an increase of noise in the victim receiver and thus a reduction of the usable measurement range is very likely, while the occurrence of ghost targets seems to be rather unlikely.” Note that, even in dense traffic with many interferers, the occurrence of ghost targets remains unlikely because any individual ghost target detections would, over time, be sporadic/random in nature and thereby mitigated by the tracking function in the victim radar. Mitigation can be further improved by the victim radar dither of relevant waveform timing parameters that help randomize the range and Doppler of ghost detections on a frame-to-frame basis. This technique has been implemented by a number of radar suppliers.

## Mechanisms and characteristics of interference

Here, we consider the two main modulation techniques described previously, i.e., FMCW and PMCW. Because the interference characteristics depend on which kinds of modulation the interferer and victim both have, we describe the various interference characteristics for the different types of interfering and victim radars.

## FMCW–FMCW

Consider a victim radar and interfering radar both using FMCW modulation. Figure 6(a) shows the mechanism of interference and the resulting time-domain and frequency-domain responses. For downconversion in the receiver, FMCW radar uses a replica (coupled version) of the transmitted FMCW signal. For the situation where the interfering FMCW signal crosses the victim FMCW signal, the interference appears as a linear chirp signal after downconversion in the victim radar receiver which, assuming “dissimilar, fast-crossing” slopes, covers a wide bandwidth as it sweeps through the victim radar passband. After bandpass filtering in the victim radar, the interference signal resembles an impulse-like signal in the time domain. The resulting frequency spectrum is broadband and often well above the background noise floor [Figure 6(b)] when representative automotive MRR parameters are used (i.e., 15–20 dB above noise).

The position and width of the impulse-like interference signal in the time domain following downconversion and bandpass filtering in the victim radar depends on the relative timing and slopes of the FMCW modulation of the interfering and victim radars. The resulting frequency spectrum characteristics of the interference in the victim radar, including the PSD, depend on the relative timing and FM slopes as well. For example, with slower FM rates and/or similar FM slopes for the victim and interfering radars (i.e., “slow-crossing” slopes), the time extent of interference in the victim radar passband and the associated PSD can increase significantly.

In (8), the parameter K for FMCW-to-FMCW interference is fundamentally the ratio of the chirp bandwidth transmitted by the interfering radar to the bandwidth of the interference chirp after downconversion in the victim radar. For FMCW, the bandwidth after downconversion in the victim radar depends on the difference in the FM sweep (i.e., modulation) rate between the interfering and victim radars. Assuming that the FM modulation rates of the interfering and victim radars produce “broadband” interference following downconversion in the victim radar, i.e., interference spread over no less than the baseband bandwidth of the victim radar, K generally ranges from a minimum value of 0.5 to a maximum value equal to the sweep bandwidth of the interfering radar divided by the baseband bandwidth of the victim radar.

![](images/65d405245d4793740cad1be27bea94d5340b5027c5fd262f6fe002f1c9890e13.jpg)

![](images/c40fb9c13152d15edf0c5c7429885898698c3f1427ecf0f842b2c617382ad643.jpg)  
FIGURE 6. (a) An FMCW-to-FMCW interference mechanism and (b) its simulated time–frequency domain characteristics. LO: local oscillator.

The parameter K for FMCW interference in (8) depends on the FMCW sweep rates of the interfering and victim radars as well as their time and frequency alignments, as demonstrated in the following examples.

■ Case 1: Interfering and victim radar sweeps with the same duration $T _ { S } ,$ start time, and start frequency

$$
K = \frac { \Delta F _ { I } ^ { \mathrm { R F } } } { \Delta F _ { I } ^ { \mathrm { B B } } } = \left| \frac { S _ { I } T _ { S } } { \left( S _ { V } - S _ { I } \right) T _ { S } } \right| = \left| \frac { S _ { I } } { \left( S _ { V } - S _ { I } \right) } \right| .\tag{10}
$$

■ Case 2: Interfering and victim radar sweeps with the same duration $T _ { S } ,$ start time, and center frequency

$$
K = 2 \bigg | \frac { S _ { I } T _ { S } } { \left( S _ { V } - S _ { I } \right) T _ { S } } \bigg | = 2 \bigg | \frac { S _ { I } } { \left( S _ { V } - S _ { I } \right) } \bigg | ,\tag{11}
$$

where $S _ { I } = \operatorname { F M }$ sweep (modulation) rate of the interfering radar and $S _ { V } = \operatorname { F M }$ sweep (modulation) rate of the victim radar.

Figure 7 shows parameter K and the corresponding interference in the time domain after downconversion and bandpass filtering in the victim radar for a situation where the FM sweeps of the victim and interfering radar are aligned in time and have the same center frequency (i.e., case 2). Two examples are shown in Figure 7; the FM sweep of the victim radar is shown in green. One example corresponds to $K = 1 \left( \mathrm { i . e . } \right.$ ., the FM sweep of interfering radar (blue) with a sweep rate, $S _ { I } ,$ equal in magnitude but opposite in sign to the sweep rate of the victim radar, $S _ { V } ) ;$ a second example corresponds to $K = 1 0 \ { \mathrm { ( i . e . } }$ , the FM sweep of interfering radar (red) with a sweep rate similar to the sweep rate of the victim radar). Compared to $\mathrm { a \ ^ { 6 6 } f a s t ^ { 7 } }$ (i.e., high) crossing rate for “dissimilar” FM sweeps (e.g., $K = 1 )$ , as the FM sweeps become more similar (e.g., $K = 1 0 )$ , the crossing rate decreases, resulting in interference with a longer time duration and higher PSD after downconversion and bandpass filtering in the victim radar. All else being equal, the $K = 1 0$ example results in interference with 10 times the PSD (and, correspondingly, 10 times the INR) compared to the K = 1 example.

![](images/8d67e99d9c6dfec935011dff325aa2dc92ff4e772b4e827f54df968d6f3e0454.jpg)

Early automotive FMCW radar typically used “slow-chirp” waveforms with one or several linear FM sweeps transmitted during a dwell or update interval and each chirp using a relatively slow sweep rate. Automotive radars using “fast-chirp” FMCW waveforms consisting of many identical linear FM chirps during a dwell, where each chirp has a relatively fast sweep rate, are becoming more prevalent. Fast-chirp FMCW radar converts the sampled time-domain data from each chirp to a 2D range-Doppler frequency spectrum, typically via a 2D fast Fourier transform (FFT) process.

The 2D frequency spectrum for a fast-chirp FMCW victim radar and slow-chirp FMCW interfering radar is shown in Figure 8 using typical automotive MRR parameters. The vertical axis has been scaled to show the INR. In Figure 6, the timedomain impulse-like interference seen by each chirp of the fast-chirp victim radar sweeps over the frequency in a linear fashion with respect to time. The corresponding interference frequency spectrum for each chirp of the victim radar (ranging frequency domain) sweeps through Doppler frequency in a linear fashion and then folds into the ambiguous Doppler interval of the victim radar. The resulting 2D range-Doppler frequency spectrum exhibits a “noise-like” response. For MRR, the simulation shows that the resulting INR is roughly 15–20 dB.

![](images/4cd9b5294a689db6f307b1ddaff4b81a01c9905b6c3ed4d9e734933cd766bb99.jpg)  
FIGURE 7. The influence of victim and interfering radar FMCW sweeps on interference in the victim radar passband.

To help illustrate the parameters $D _ { F }$ (and K) in (6) (i.e., the equation for determining the PSD of interference and ultimately the INR), consider the case of a fast-chirp FMCW victim radar with dwell parameters in Figure 9 and an interfering radar with the same type of signal. This example has four 16.67-ms fast-chirp dwells in 100 ms for an overall duty factor of 67%. There are two fast-chirp dwell types, A and B, sweeping 500 and 250 MHz, respectively. Each dwell type has two complementary dwells, i.e., 1 and 2, with 512 and 450 chirps, respectively. The four-dwell sequence therefore uses four different fast-chirp sweeps.

![](images/c01bab34619391f0a371e13b181b01238c95da7d4bb3caedd0dfb51509bd321f.jpg)  
FIGURE 8. A 2D range-Doppler spectrum for fast-chirp FMCW victim radar with slow-chirp FMCW interfering radar.

For the dwell sequence and timing shown in this section, the probability of the victim radar encountering interference with a different chirp slope (leading to crossing FMCW slopes that produce a wideband interference spectrum) is effectively unity with the different cases and their respective K factors.

■ Victim radar dwell A1—interfering radar dwell B1 (K = 4)

■ Victim radar dwell A1—interfering radar dwell A2 (K = 16)

■ Victim radar dwell A1—interfering radar dwell B2 (K = 3 5. )

■ Victim radar dwell B1—interfering radar dwell A2 (K = 4)

■ Victim radar dwell B1—Interfering Radar Dwell B2 (K = 16)

■ Victim radar dwell A2—interfering radar dwell B2 (K = 4).

As previously noted, K = 1 if the slopes are the same magnitude but opposite in sign. As the slopes become more similar, the crossing rate decreases and K increases. The factor D<sub>F</sub> equals the fractional overlap of the dwells and varies from roughly 0.002 for the overlap of a single chirp (1/512), to 1 for a complete overlap. For each of the aforementioned cases, the probability of at least one chirp overlap is 33% and the probability of at least a 50% overlap ( D<sub>F</sub> \$ 0 5. ) is 16.7%. Considering all of the cases, the composite probability of at least two dissimilar slopes with at least a 50% overlap is 83%.

![](images/3d70d13a422a7e4882f22b2b1b4a0ef4a175f6db10ab27d1b321de5f181ef8b6.jpg)  
FIGURE 9. An example of a fast-chirp FMCW dwell sequence and its associated parameters.

![](images/7a7af73eb60025beaacdfddad180ff5d8fdb206b393e9296fb90b76b6decd6a3.jpg)

The mechanism and characteristics of FMCW-to-FMCW interference in Figure 6(a) are shown for the single dwell/chirp of an interfering radar. In practice, the interference characteristics seen by an FMCW victim radar in the presence of multiple FMCW interfering radars of different types $( \mathrm { e . g . }$ SRR, MRR, LRR, or multimode using fast- and/or slow-chirp FMCW waveforms) can be quite complex with many impulselike signals of different amplitudes and widths spread across the time domain.

## PMCW–PMCW

Consider a victim and interfering radar, both of which utilize PMCW modulation. Figure 10(a) and (b) shows the mechanism of interference and the resulting time-domain and frequency-domain responses. PMCW interference with random, noise-like biphase coding using chip rate $\Delta f _ { i } = 1 / T _ { c }$ is assumed and appears as a spread-spectrum noise-like signal with bandwidth $\Delta f _ { i } = 1 / T _ { c }$ centered at carrier frequency $f _ { c } .$ In the example chip rate $\Delta f _ { i } = 1 / T _ { c }$ with bandwidth $\Delta f _ { \nu } = 1 / T _ { c }$ , the PMCW victim radar is likewise assumed to transmit a PMCW biphase-coded noise-like signal with the same chip rate, bandwidth, and carrier (center) frequency as the interfering PMCW radar but with an independent, uncorrelated spreading code. The victim PMCW radar downconverts the received signal with a constant local oscillator frequency at the common carrier frequency (shown as $f _ { 1 } = f _ { c } )$ and demodulates the received signal with a delayed copy of the PMCW biphase code (chip rate $\Delta f _ { i } = 1 / T _ { c }$ and bandwidth $\Delta f _ { \nu } = 1 / T _ { c } ,$ , assumed to be the same as the corresponding parameters of the PMCW interfering radar in the example shown). Following downconversion, demodulation, and bandpass filtering in the victim radar, the interference appears as a noise-like signal in both time and frequency domains. The resulting frequency spectrum is broadband and often well above the background noise floor, as illustrated in Figure 10(b) using representative parameters for automotive MRR (i.e., 15–20 dB above noise).

## PMCW–FMCW (or FMCW–PMCW)

Consider a victim radar with biphase PMCW modulation and interfering radar with FMCW modulation or vice versa. Figure 11 illustrates the interference mechanism and the resulting time-domain and frequency-domain responses. In both situations (i.e., PMCW victim/FMCW interferer or FMCW victim/PMCW interferer), the interference is noise like in the time and frequency domains and, all else being equal, the INR is the same.

## Comments on interference for PMCW versus FMCW modulation

Considering situations with FMCW or PMCW modulation for either the victim and/or interfering radars, the INR scales are

$$
\begin{array} { r c l } { { \mathrm { I N R } ~ \propto ~ \frac { P _ { i , \nu } } { B _ { i } } , ~ . . . . . . ~ \mathrm { P M C W ~ v i c t i m ~ o r ~ P M C W ~ i n t e r f e r e r } } } \\ { { \mathrm { I N R } ~ \propto ~ K \frac { P _ { i , \nu } } { B _ { i } } , ~ . . . . . ~ \mathrm { F M C W ~ v i c t i m ~ a n d ~ F M C W ~ i n t e r f e r e r } , } } \end{array}\tag{12}
$$

where $P _ { i , \nu }$ is the power of the interferer received at the victim radar. Downconversion/demodulation and subsequent signal processing in the victim radar generally result in spreading of the interference in a noise-like fashion over the passband and/ or detection band. The resulting INR is then given by the PSD of interference divided by the PSD of noise in the victim radar. The PSD of interference in the victim radar depends on the bandwidth of the interferer, B<sub>i</sub> (i.e., the frequency spread of interference), and the interference power received by the victim radar, $P _ { i , \nu }$ , which is determined by using the “one-way”

![](images/f8162a07cec2d977c425302e3ca6be517d9f2463868217245dee191001acc733.jpg)  
FIGURE 10. (a) An PMCW-to-PMCW interference mechanism with biphase noise coding and (b) its simulated time–frequency domain characteristics

radar equation. However, in the case of FMCW to FMCW, the frequency spread of interference after downconversion to baseband in the victim radar, and thus its PSD at baseband, depends on the relative FM sweep rates (FM slopes) of victim and interfering radars (reflected in the parameter K). If the FMCW victim and interfering radar slopes are similar, the interference power is downconverted into a narrow frequency band increasing the PSD compared to that of dissimilar slopes ( K 2 1). Hence, all else being equal, situations with phase modulation (PMCW) for either the victim or interfering radar generally results in lower INR levels.

## Interference mitigation

Interference analysis and interference mitigation techniques in radar systems have been investigated in a number of projects and reported in a number of papers. Recently, significant research has focused on a victim radar that employs FMCW modulation subject to interference from radars using FMCW modulation as well (see [17] and [21]–[24]). In this section, we focus on interference mitigation techniques.

Techniques that mitigate interference in automotive radars include transmission techniques (e.g., frequency hopping and timing jitter) and receiver techniques (e.g., time-domain excision). Generally, transmission techniques rely on ensuring that different radars transmit in such a way that the signals are nearly orthogonal to each other in some domain (e.g., polarization, time, and frequency). Most of the studies on interference in automotive radar are focused on interference mitigation at the receiver for both the interfering radar and the victim radar (e.g., the FMCW interferer and victim). The MOSARIM project [19], [20] completed a comprehensive study of interference in automotive radar systems that focused on interference mitigation. Interference mitigation techniques were grouped into six different major domains/categories: polarization domain, time domain, frequency domain, coding domain, space domain (e.g., beamforming), and strategic approaches. Strategic approaches included detecting interference and changing waveform parameters and/or beamscanning in response, as well as detecting and excising interference with a subsequent repair of the received signal in either the time, frequency, or joint-time-frequency domains. Another strategic technique considered was the general concept of intervehicle communication that negotiates noninterfering radar parameters (e.g., time or frequency slots).

With the exception of the polarization domain, many of the techniques described in the MOSARIM project involved substantial signal processing for processing complex waveforms, adaptively nulling interference, and/or detecting and excising interference. Techniques with the highest level of signal processing complexity include digital beamforming with adaptive nulling, time-frequency transforming with detection and excision of interference, and space-time adaptive processing.

The MOSARIM project performed modeling, simulations, and tests of interference to automotive radar of the aforementioned mitigation techniques and concluded that [16]: “To assure an I/N level of 0 or −10 dB, reliable mitigation techniques in the order of (a minimum of) 50 dB mitigation margin are needed.” In assessing the capability of interference mitigation, MOSARIM concluded that individual mitigation techniques are not adequate, multiple techniques will need to be applied and, as automotive radar volumes increase, it may be beneficial to include, via regulatory means, the assignment of polarization and frequency bands depending on the radar application/type (e.g., SRR, MRR, or LRR) and on-vehicle mounting location. An example of this is using different subbands in various directions (front, back, and side) and using different polarizations.

![](images/a69b45b4fb32a5982c4eb750bdaf18559423a429ab9de1207ed47020b962fa69.jpg)  
FIGURE 11. The mechanism of biphase noise PMCW-to-FMCW interference.

Since the MOSARIM study concluded, research has continued on interference in automotive radar. As described in the “Mechanisms and Characteristics of Interference” section, an interfering radar with the same structure as the victim radar can create a “ghost target” if that signal, when received at the victim radar, begins a sweep within a small window of time proportional to the bandwidth of the filter. However, it is much more likely that the interfering radar creates a noise-like signal. In [17], a single FMCW interferer with a victim FMCW radar was considered. The SIR was derived as a function of the distance between the interferer and the victim radar and the distance between the target and the victim radar. Using these parameters, the region where the SIR was above some threshold (e.g., 10 dB) for a given target size was calculated. The effect of the FMCW chirp slopes on the SIR was determined. In [17], the conclusion noted a that interference can cause a victim radar to “lose a target.” As an example, an FMCW radar with a processing gain (time-bandwidth product) of 50 dB and an interferer that is 10 m away will cause the SIR to drop below 10 dB when the target is 30 m away. Because FMCW radars have been the dominant type of radar used in automotive applications, there are quite a few papers that analyze the performance of an FMCW radar interferer on a victim FMCW radar.

![](images/431c51bf3316e68ecc2cbebf818682b7d96b52d0e1bc807d7389d700b6221fc5.jpg)  
FIGURE 12. The simulated time-domain response before and after timedomain excision for FMCW interference (includes target + noise + interference).

Techniques that mitigate an FMCW interferer on an FMCW victim include time-domain excision of various forms [7], [21], [23], [25]–[27]. The results of a basic simulation with timedomain excision for a slow-chirp FMCW interferer and a fastchirp FMCW victim radar are shown in Figures 12 and 13. As previously discussed, with an interferer FMCW sweep crossing a victim radar FMCW sweep, the interference appears as a linear chirp signal after downconversion in the victim radar receiver. The linear chirp interference signal sweeps through the victim radar passband and, assuming “fast-crossing” sweeps, produces an “impulse-like” signal in the time domain after bandpass filtering in the victim radar receiver. Prior to 2D range-Doppler FFT-matched filtering in a fast-chirp victim radar, the target signal is typically well below the noise level while the impulselike interference signal is well above the noise level. Matched filtering provides substantial integration gain for a target-like constant frequency signal, while the impulse-like interference signal spreads in a noise-like fashion over the range-Doppler frequency spectrum.

Basic time-domain excision uses a threshold above the background noise level to remove interference. In other words, time-domain samples above the threshold are set to zero. Simulated results before and after time-domain excision are shown in Figure 12 for one chirp of the fast-chirp victim radar. Note that the simulated example includes target, interference, and noise. Time-domain excision is repeated for each chirp.

Simulated results for the range-Doppler frequency response of the fast-chirp victim radar are shown in Figure 13. Results correspond to the cases of target + noise (no interference) and for target + interference + noise, first without time-domain excision and then with time-domain excision. As shown, without any mitigation, the interference substantially raises the “noise” floor and masks the target. Time-domain excision is able to remove the FMCW interference while preserving the target signal; however, as expected, some signal loss and potential for artifacts occur depending on the amount and pattern of excision required.

The simulated example illustrates time-domain excision for the case of a single interferer. Overall effectiveness degrades as the number of interferers increases and the corresponding portion of the time domain to be excised becomes substantial. Although mitigation of a single FMCW interferer on an FMCW victim is fairly well understood, there is much ongoing research into other scenarios.

![](images/d39cc99e5cd1daaf4fad4764eaf1f1ad9f6e512f7e3ecdc5bce5e2ccb0f4ef13.jpg)  
FIGURE 13. The fast-chirp FMCW range-Doppler frequency response without and with time-domain excision for FMCW interference.

## Ongoing and future research

Although simple interference mitigation techniques are generally well understood—with some having been implemented in automotive radars—interference mitigation is an important and ongoing area of R&D. Typically, a radar system will have a receiver structure, as shown in Figure 14. The RF front end includes analog components such as a low-noise amplifier, mixers, and filters. The output of the RF front end is converted to digital by an analog-to-digital converter (ADC). The first process step is range processing, which is an FFT in an FMCW radar system and a matched filter in a PMCW radar system. Range processing is followed by Doppler processing, which is followed by beamforming, object detection, and tracking. Interference mitigation may be added to the block diagram, potentially at different points in the processing steps. One technique used to mitigate the effect of an interferer (either FMCW or PMCW) is isolating the part of the signal that does not have interference; this may be implemented using a time-domain notch filter in an FMCW system or a “zero-forcing” type of detector in a PMCW system (as discussed further in this section). However, these techniques also remove a portion of the desired signal and can become problematic as the number of interferers grow. Time excision would typically happen between the output of the ADC and the input of the range-matched filter.

In [23], the interference cancellation of a single FMCW interferer on an FMCW victim by identifying the interference location using techniques from image processing and then “zeroing out” those time locations with additional smoothing to avoid ringing effects, shows that without interference cancellation, the victim radar would not be able to detect a certain target due to the increase in noise level, but with interference cancellation, the radar is able to detect the target. In [25], the characteristics of an FMCW-interfering signal, which are much stronger than the desired signal reflected from the target on an FMCW victim radar, are estimated and then subtracted from the overall signal, thereby improving the receiver sensitivity. This technique would also work for multiple radars as long as the interference from one radar did not overlap in time with the interference from another radar. This interference mitigation would also occur before the range-FFT processing. In [7], interference mitigation not requiring a threshold (compared to normal time-domain excision) was considered and shown to be effective, even for multiple interfering radars. In [24], beamforming using multiple receiving antennas was considered for eliminating a single interferer. Simulations with a CW signal as the interference source and an 800-MHz bandwidth FMCW signal for the victim radar show that the interference reduced by 40 dB. Here, four receiving antennas were used with optimal weighting to remove the interference. Measurements corresponding to the simulation show that the resulting INR was under 2 dB [24, Table 1] for a single interferer. This interference mitigation technique would be applied in the beamforming processing unit. In [27], an FMCW interferer and victim were considered, where again, the interference is detected and zeroed out. Although this does reduce the noise level because of the interferer, it also removes the desired signal over a certain time period when the frequency of the interferer falls within a certain frequency range of the victim radar. To mitigate this effect, [27] considered a technique that regenerates the desired signal during the time when the received signal was zeroed out. An iterative algorithm was used for that purpose and allowed for smaller targets to be detected than would have otherwise been detected with just the zeroing-out approach (with or without additional smoothing).

Interference in cellular communication systems has been the subject of considerable investigation. Code-division multiple access (CDMA)—the communication version of a PMCW radar—has been widely deployed in 2G and 3G cellular systems. The processing gain associated with PMCW signals, similar to the CDMA signals used for communications, allows for multiple radars to be used simultaneously.

In a PMCW–PMCW scenario, the large number of spreading codes generally ensures the interference will be a wideband, noise-like signal because each radar can use a different spreading code. There are a number of techniques that can be used in PMCW–PMCW situations to improve the interference mitigation capability. Although some of these techniques require knowing the spreading codes of other radars, there are also “blind” techniques that work without that knowledge [28]. These are the same techniques that are useful in a communications context (e.g., CDMA). These techniques do not completely eliminate interference but may drastically reduce its effect, especially in a near-far scenario similar to multiple interferers versus a victim receiver, and work best when the interference is periodic in nature, i.e., the spreading codes repeat after a certain number of chips (in much the same way an FMCW type of radar would have a repetitive signal). The interference mitigation in CDMA systems (i.e., PMCW) is based on the cyclostationary structure of the interfering signal. These interference mitigation techniques are based on estimating the correlation matrix of the received signal, then employing an “orthogonalizing matched filter” [29]. Note that the radar problem is easier to correct than the communication problem, because for the communication problem, there is an additional unknown (i.e., the data).

![](images/e3e7d56d5018b4147c890a34fe2164bda789d29fc653faeecc0b7dcee61910ca.jpg)  
FIGURE 14. A generic receiver structure for radar.

An FMCW interferer on a victim PMCW radar is very similar to a jammer in a spread-spectrum system. This type of interference, as well as effective mitigation techniques, has been well studied. An FMCW interferer signal to a PMCW victim is the same as that of a “swept-tone jammer” in spread-spectrum communication systems discussed in [30] and [31]. The performance measure in a spread-spectrum communication system is typically bit error rate, rather than the typical performance measures used in a radar system. Nevertheless, the mitigation techniques would be similar.

A PMCW interferer on a victim FMCW radar system can appear as just additional noise that might seem difficult to mitigate in the time domain. However, the PMCW signal’s spectral characteristics can be estimated and used to improve the filtering that may reject wideband color noise [32]. Certain short-term time-frequency processing techniques may be able to mitigate this interference [33]. As with other classes of interferer and victim radars, transmission techniques such as polarization or frequency separation can be applied here.

Because both FMCW and PMCW types of radar are essentially spread-spectrum types of systems, interference mitigation techniques applicable to spread-spectrum communication systems may potentially be of use in radar systems. One technique for mitigating strong interference in the presence of a weak signal is based on locally optimum Bayesian detection. For example, [34] considers a spread-spectrum signal in the presence of different types of interference and noise. Although the focus of these techniques is on communication systems, they have potential for application in radar systems as well.

Future research that addresses interference to automotive radar sensors includes joint radar/communication systems [35], decentralized multiple-access protocols, and alternative modulation techniques (and the corresponding matched-filter signal processing) that limit the potential for, and subsequent level of, interference. Further development of joint, multiple-domainadaptive signal processing algorithms that excise/null interference within the polarization-spatial-temporal-frequency domains must be explored as well.

One aspect of interference mitigation to consider is multiple-access techniques at the transmitter. In other words, by coordinating transmission (e.g., in the time domain, frequency domain, and polarization domain), interference can be prevented from occurring. We note that this type of problem has been studied extensively in the context of communication systems, where information-theoretic formulations can be used to determine the possible rates of data transmission for different users. Of course, the radar problem is different in that data are not transmitted and targets are detected. Nevertheless, approaches to multiple access must be investigated.

## Conclusions

In general, automotive radar systems include a substantial level of inherent resistance to interference by virtue of a large timebandwidth product. The time-bandwidth product is the processing gain of a radar system (i.e., the time-bandwidth product is related to its ability to reject interference). Regardless, with an increasing number of radars deployed per vehicle and an increase in the number of vehicles having radars, interference levels, especially in certain situations such as rush-hour traffic, will likely be quite severe. Automotive radar manufacturers have been active in developing and implementing many of the mitigation techniques described in this article that reduce the impact of mutual interference.

Because radars are becoming pervasive and ubiquitous on automobiles and perform safety-critical functions, there is a need to optimize interference mitigation both at the transmitter and receiver by limiting the amount of interference so that victim radar performance can be affected only up to a prescribed amount. To this end, developing standards will make the engineering of interference mitigation easier and more effective.

## Authors

Stephen Alland (swalland@uhnder.com) received his B.S. and M.S. degrees in electrical engineering from Rensselaer Polytechnic Institute, Troy, New York, in 1976 and 1977, respectively. He is a radar consultant with more than 40 years of experience in radar systems, including 22 years in automotive radar systems. Previously, he was a technical fellow and manager for advanced radar development with Delphi Electronics and Safety in Malibu, California. From 1995 to 2014, he worked for Delphi to develop automotive radar systems. Prior to Delphi, he worked for Hughes to develop air defense radar systems, beginning in 1977. He holds 21 U.S. patents related to radar systems. His technical areas of expertise include radar system design and simulation, radar waveform design, radar signal processing, and target tracking.

Wayne Stark (stark@eecs.umich.edu) received his B.S., M.S., and Ph.D. degrees in electrical engineering from the University of Illinois, Urbana, in 1978, 1979, and 1982, respectively. Since 1982, he has been a faculty member in the Department of Electrical Engineering and Computer Science at the University of Michigan, Ann Arbor. He was selected by the National Science Foundation as a 1985 Presidential Young Investigator. He received the IEEE Military Communications Conference (MILCOM) Board 2002 Technical Achievement Award for sustained contributions to military communications. In 2009, he was corecipient of the IEEE MILCOM Ellersick Prize for best paper in the Unclassified Technical Program. In 2010, he received the Journal of Communications and Networks Best Paper Award. He is on the editorial board of IEEE Journal on Selected Areas of Communications. His research interests include the areas of coding and communication theory, spread-spectrum systems, wireless communication networks, and radar systems. He is a Fellow of the IEEE.

Murtaza Ali (murtaza@uhnder.com) received his B.S. degree in electrical engineering from Bangladesh University of Engineering and Technology, Dhaka, in 1989, and his

Ph.D. degree in electrical engineering from the University of Minnesota, Twin Cities, in 1995. He is currently the director of systems engineering at Uhnder, Inc. Prior to joining Uhnder, he was a Distinguished Member of Technical Staff, and manager of the Perception and Analytics Lab at Texas Instruments (TI). At TI, he led R&D teams for millimeterwave radar, mobile WiMAX, and asymmetric digital subscriber line systems. He also represented TI in various standards organizations including Telecommunications Industry Association, the International Telecommunication Union, HomePlug, Home Phone line Networking As - sociation, and the IEEE. His research interests include development of novel communications and signal processing systems. He holds 32 U.S. patents and has published more than 40 papers in refereed and invited forums. He is a Senior Member of the IEEE.

Manju Hegde (manju@uhnder.com) received his B.S. degree in electrical engineering from the Indian Institute of Technology, Bombay, and his Ph.D. degree in computer information and control engineering from the University of Michigan, Ann Arbor, in 1987 and 1979, respectively. He is the chief executive officer (CEO) of Uhnder Inc. Previously, he was the corporate vice president at Advanced Micro Devices (AMD), where he was responsible for driving and executing AMD’s strategy across technology and marketing functions into the client and server computing ecosystems. He also cofounded and led AMD Ventures before joining AMD. He was vice president of Compute Unified Device Architecture technical marketing at Nvidia, where he focused on training and enabling researchers and developers to leverage the parallel architecture and performance of global processing units for general purpose applications. He was cofounder and CEO of AGEIA Technologies from its inception in 2002.

## References

[1] B. Schoettle, “Sensor fusion: A comparison of sensing capabilities of human drivers and highly automated vehicles,” Univ. of Michigan Transportation Res. Inst., Ann Arbor, Tech. Rep. SWT-2017-12, 2017.

[2] G. Rudolph and U. Voelzke, “Three sensor types drive autonomous vehicles,” Sensors Mag., Nov. 2017. [Online]. Available: https://www.sensorsmag.com/ components/three-sensor-types-drive-autonomous-vehicles

[3] I. Bilik, O. Bialer, S. Villeval, H. Sharifi, K. Kona, M. Pan, D. Persechini, M. Musni et al., “Automotive MIMO radar for urban environments,” in Proc. IEEE Radar Conf., 2016. pp. 1–6. doi: 10.1109/RADAR.2016.7485215.

[4] I. Bilik, S. Villeval, D. Brodeski, H. Ringel, O. Longman, P. Goswami, C. Y. Kumar, S. Rao et al., “Automotive multi-mode cascaded radar data processing embedded system,” in Proc. IEEE Radar Conf., 2018, pp. 0372–0376.

[5] F. Engels, P. Heidenreich, A. M. Zoubir, F. K. Jondral, and M. Wintermantel, “Advances in automotive radar: A framework on computationally efficient high-resolution frequency estimation,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 36–46, 2017.

[6] F. Engels, M. Wintermantel, and P. Heidenreich, “Automotive MIMO radar angle estimation in the presence of multipath,” in Proc. IEEE Radar Conf. (EURAD), 2017, pp. 82–85.

[7] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in Proc. IEEE Int. Symp. Circuits and Systems, 2018, pp. 1–4.

[8] H. H. Meinel and J. Dickman, “Automotive radar: From its origin to future directions,” Microw. J., vol. 56, no. 9, pp. 24–40, Sept. 2013.

[9] H. H. Meinel, “Evolving automotive radar: From the very beginnings into the future,” in Proc. European Conf. Antennas and Propagation (EuCAP), 2014, pp. 3107–3114.

[10] M. I. Skolnik, Introduction to Radar. New York: McGraw-Hill, 1962

[11] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, 2017.

[12] M. Schneider, “Automotive radar—status and trends,” in Proc. German Microwave Conf., 2005, pp. 144–147.

[13] E. G. Hoare and R. Hill, “System requirements for automotive radar antennas,” in Proc. IEEE Colloq. Antennas for Automotives, Mar. 2000, pp. 1–11.

[14] E. Garcia, J. A. Paredes, F. J. Álvarez, M. C. Pérez, and J. J. García, “Spreading sequences in active sensing: A review,” Signal Process., vol. 106, pp. 88–105, Jan. 2015.

[15] N. Levanon, “Multifrequency complementary phase-coded radar signal,” IEE Proc.—Radar, Sonar Navigation, vol. 147, no. 6, pp. 276, 2000.

[16] M. Kunert, “Final report,” European Commission: MOre safety for all by radar interference mitigation (MOSARIM), Luxembourg, Tech. Rep. 248231, 2010. [Online]. Available: https://cordis.europa.eu/project/rcn/94234/reporting/en

[17] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, no. 3–4, pp. 371–378, 2014.

[18] J. Hasch, E. Topak, R. Schnabel, T. Zwick, R. Weigel, and C. Waldschmidt, “Millimeter-wave technology for automotive radar sensors in the 77 GHz frequency band,” IEEE Trans. Microw. Theory Techn., vol. 60, no. 3, pp. 845–860, 2012.

[19] M. Ahrholdt, F. Bodereau, C. Fischer, M. Goppelt, R. Pietsch, A. John, A. Ossowska, and M. Kunert, “D12.1-Study report on relevant scenarios and applications and requirements specification,” European Commission: MOre Safety for All by Radar Interference Mitigation (MOSARIM), 2010. [Online]. Available: https:/ cordis.europa.eu/project/rcn/94234/reporting/en

[20] M. Kunert, F. Bodereau, M. Goppelt, C. Fischer, A. John, T. Wixforth, A. Ossowska, T. Schipper et al., “D1.5-Study on the state-of-the-art interference mitigation techniques,” Technical report, European Commission: MOre Safety for Al by Radar Interference Mitigation (MOSARIM), 2010. [Online]. Available: https:// cordis.europa.eu/project/rcn/94234/reporting/en

[21] M. Umehira, T. Nozawa, Y. Makino, X. Wang, S. Takeda, and H. Kuroda, “A novel iterative inter-radar interference reduction scheme for densely deployed automotive FMCW radars,” in Proc. 19th Int. Radar Symp. (IRS), 2018, pp. 1–10. doi: 10.23919/IRS.2018.8448223.

[22] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutua interference between automotive FMCW radar sensors,” in Proc. 6th German Microwave Conf., 2011, pp. 1–4.

[23] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in Proc. IEEE MTT-S Int. Conf. Microwaves for Intelligent Mobility (ICMIM), 2015, pp. 1–4.

[24] J. Bechter, K. Eid, F. Roos, and C. Waldschmidt, “Digital beamforming to mitigate automotive radar interference,” in Proc. IEEE MTT-S Int. Conf. Microwaves for Intelligent Mobility (ICMIM), 2016, pp. 1–4.

[25] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference,” in Proc. IEEE MTT-S Int. Conf. Microwaves for Intelligent Mobility (ICMIM), 2015, pp. 1–4.

[26] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogona noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, 2018.

[27] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. European Radar Conf., 2017, pp. 90–93.

[28] U. Madhow, “Blind adaptive interference suppression for direct-sequence CDMA,” Proc. IEEE, vol. 86, no. 10, pp. 2049–2069, 1998.

[29] K. Fukawa and H. Suzuki, “Orthogonalizing matched filter (OMF) detection for DS-CDMA mobile radio systems,” in Proc. Global Telecommunications Conf., Communications: The Global Bridge., 1994, pp. 385–389.

[30] G. Saulnier, P. Das, and L. Milstein, “An adaptive digital suppression filter for direct-sequence spread-spectrum communications,” IEEE J. Sel. Areas Commun., vol. 3, no. 5, pp. 676–686, 1985.

[31] L. B. Milstein, “Interference rejection techniques in spread spectrum communications,” Proc. IEEE, vol. 76, no. 6, pp. 657–671, 1988.

[32] L. Milstein and P. Das, “An analysis of a real-time transform domain filtering digital communication system—part II: Wide-band interference rejection,” IEEE Trans. Commun., vol. 31, no. 1, pp. 21–27, 1983.

[33] V. C. Chen and H. Ling, Time-Frequency Transforms for Radar Imaging and Signal Analysis, Norwood, MA: Artech, 2002.

[34] S. N. Batalama, M. J. Medley, and I. N. Psaromiligkos, “Adaptive robust spread-spectrum receivers,” IEEE Trans. Commun., vol. 47, no. 6, pp. 905–917, 1999.

[35] A. R. Chiriyath, B. Paul, G. M. Jacyna, and D. W. Bliss, “Inner bounds on performance of radar and communications co-existence,” IEEE Trans. Signal Process., vol. 64, no. 2, pp. 464–474, 2016.

![](images/436217c472398b12e9b39243553258752dff1657b174dd62a50e59b48e087ae5.jpg)