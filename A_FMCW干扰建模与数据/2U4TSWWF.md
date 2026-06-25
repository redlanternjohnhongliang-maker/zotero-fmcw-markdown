# UNIVERSITYOF BIRMINGHAM University of Birmingham Research at Birmingham

# Phenomenology of automotive radar interference

Norouzian, Fatemeh; Pirkani, Anum; Hoare, Edward; Cherniakov, Mikhail; Gashinova, Marina

DOI: 10.1049/rsn2.12096

License: Creative Commons: Attribution (CC BY)

Document Version Publisher's PDF, also known as Version of record

Citation for published version (Harvard): Norouzian, F, Pirkani, A, Hoare, E, Cherniakov, M & Gashinova, M 2021, 'Phenomenology of automotive radar interference', IET Radar, Sonar & Navigation, vol. 15, no. 9, pp. 1045-1060. https://doi.org/10.1049/rsn2.12096

Link to publication on Research at Birmingham portal

## General rights

When citing, please reference the published version.

While the University of Birmingham exercises care and attention in making items available there are rare occasions when an item has been uploaded in error or has been deemed to be commercially or otherwise sensitive.

O R I G I N A L R E S E A R C H PA P E R

# Phenomenology of automotive radar interference

Fatemeh Norouzian | Anum Pirkani | Edward Hoare | Mikhail Cherniakov Marina Gashinova

Department of Electronic, Electrical, and Systems Engineering, University of Birmingham, Gisbert Kapp Building, Pritchatts Rd, Birmingham, UK

Correspondence

Fatemeh Norouzian, Department of Electronic, Electrical, and Systems Engineering, University of Birmingham, Gisbert Kapp Building, Pritchatts Rd, Birmingham, UK. Email: F.Norouzian@bham.ac.uk

Funding information   
Innovate UK United Kingdom, Grant/Award   
Number: 104526

## Abstract

Mutual interference in automotive radar is expected to become a major issue owing to the rapid increase in the number of vehicles on the road equipped with radar. The phenomenology of interference in frequency modulated continuous wave radar is presented. Interference is empirically analysed at every signal processing stage in the victim radar by means of experimentally verified simulation modelling. Knowledge of how interference manifests in different domains provides a useful tool to develop algorithms for interference detection, mitigation and/or avoidance. The receiver's filter response is analysed to minimise the interference duration and increase the effectiveness of time‐domain mitigation techniques. A innovative method of interference parameter extraction by using spectrograms is also introduced.

## 1 | INTRODUCTION

Until relatively recently, automotive radar was the domain of luxury vehicles. The introduction of low‐cost millimetre‐wave radar chipsets along with a strong demand for advanced driver assistance systems and the requirement of safety regulations established radar as a critical sensor for most vehicles [1]. Automotive radars are also a key sensor for autonomous vehicles owing to their ability to operate in all‐weather [2] and all‐light conditions and their inherent ability to provide direct range and radial speed measurements. Therefore, the rapid increase in the number of vehicles equipped with single or multiple radars [3], to provide full 360° situational awareness, will significantly increase the probability of mutual interference [4–9]. ‘Interference’ refers to the signal received from another source that overlaps with the host, or ‘victim’, radar in the frequency, time and spatial domains.

Figure 1 shows a typical road scenario in which multiple radars create interference among sensors operating within each other's field of view (FOV). Interference may have a higher power than the echo from targets and hence adversely affect the functionality of the victim radar. Possible effects of this interference are: (1) saturation of the receiver (which is outside the scope of this work), (2i) the appearance of a ghost target in the case of synchronous interference [10], and (3) a decrease in the detection performance and even complete a loss of targets owing to an increase in the interference level at the decisionmaking point [8].

This work focuses on mutual interference between frequency modulated continuous wave (FMCW) radars, the most common modulation format used in current automotive radar [8, 11, 12]. A comprehensive understanding of the sensor's frontend effects on the level of performance degradation caused by interference in the victim radar is essential. An extensive empirical analysis is needed for three main reasons: (1) to determine the effect of each signal processing block on the interference and optimise the block when necessary, (2) to form underlying knowledge of how various interference events appear in each domain, and (3) to determine the optimum domain for more effective interference detection, extraction of interference signal parameters, and mitigation and/or avoidance strategy development. The interference analysis presented here is conducted using a simulation developed in the MATLAB environment to enable a wide range of FMCW signal parameters to be used. The simulation results are compared with and verified by experimental data for selected use cases throughout the work.

The study is structured as follows: Section 2 summarises the background of FMCW automotive radar. Interference analysis at various stages of the FMCW radar signal processing chain is discussed in Section 3. Conclusions are given in Section 4. The experimental methodology used for simulation validation is described in the Appendix.

![](images/478932b45837946bc9ecb72846c81aca0d1eced954caad817e3bd68fbda9edba.jpg)  
F I G U R E 1 Typical automotive road scenario. Dark grey shows the field of view (FoV) of the victim radar and red illustrates the FoV of the interfering radars

## 2 | MUTUAL INTERFERENCEBETWEEN FREQUENCY MODULATEDCONTINUOUS WAVE RADARS

A simplified block diagram of an FMCW radar [13] is presented in Figure 2 with the new proposed signal processing block shown with a dashed line.

The signal generated by a voltage‐controlled oscillator is split into two parts, in which one is fed to the transmit antenna $\left( { { A } _ { T x } } \right)$ and the other to the homodyne downconversion mixer. Every transmitted signal chirp is composed of three parts: active time $( T _ { s v } )$ , fly‐back time, and idle time with a pulse repetition interval (PRI), hence, the duty cycle is defined as $D C _ { v } = T _ { s v } / P R I$ . A sequence of chirps is received at the receive antenna $\left( A _ { R x } \right)$ and two‐dimensional matrix data are formed with size $\mathrm { ~ N ~ } \times \mathrm { ~ M ~ } ,$ where N is the number of samples in each chirp (fast‐time samples) and M is the number of chirps (slow‐time samples). The output signal of the mixer is restricted in the frequency domain by a low‐pass filter (LPF1) with a cutoff frequency of $f _ { L P F } ,$ which corresponds to the maximum expected beat frequency in the radar. It also acts as an antialiasing filter for further digital signal processing. The first fast Fourier transform (FFT) converts the time domain signal into the range domain. The second FFT (slow FFT) allows the accumulation of energy over the coherent processing interval (CPI) and enables the extraction of the relative speed between the radar and the targets. The pulse repetition frequency acts as a Doppler sampling frequency and defines the maximum unambiguous velocity that can be estimated. The additional branch contains LPF2 and a short time Fourier transform (STFT). In Neemat et al. [14], Tullsson [15] and Uysal [16], the STFT is employed to mitigate interference. In this work, the STFT is used as an analysis tool for interference signal parameter extraction.

## 2.1 | Interference

Figure 3 illustrates the victim radar chirp (blue solid line), with the LPF passband (black dashed line), a target echo (blue dotted line) and interference chirp (red solid line). The victim and interference chirps have start frequencies of $\overline { { f } } _ { c v }$ and $f _ { c i n t } ,$ respectively. The victim radar transmits a signal with a bandwidth of $B W _ { v }$ and sweep time of $T _ { s v } .$ The interference chirp has a sweep time of $T _ { s i n t }$ and bandwidth of $B W _ { \mathrm { i n t } }$ . The chirp rate is the ratio of bandwidth over the sweep time, which is $k _ { v }$ for the victim radar and $k _ { \mathrm { i n t } }$ for the interference radar. The transmitted chirp is either up‐chirp, where frequency increases linearly with time, or down‐chirp, where frequency sweeps down. The victim and interference chirps shown in Figure 3(a) are both up‐chirps and are used in all analyses here.

![](images/209463d2521318781906454c03abe0230f74d5547c0603d76831d6b8f95ab5af.jpg)  
F I G U R E 2 Simplified frequency modulated continuous wave radar architecture

![](images/131fc42421201c7b09f066b66454b95cdf1c38e25e0c7c2edde7de3098ba359d.jpg)  
F I G U R E 3 (a) Victim and interference chirp in the frequency‐time domain with highlighting in the region of the low‐pass filter; (b) Target and interference signal in the time domain

Interference occurs in the baseband signal of the victim radar if the received interference chirp falls into the victim radar receiver passband, defined by the LPF response, which is shown as a grey region in Figure 3(a). The interference component appears at the LPF output as a short pulse, with a duration of $\Delta T _ { \mathrm { i n t } } ,$ whereas the target appears as a sinusoidal signal, as shown in Figure 3(a).

Interference can be classified based on the relation between the victim and interference chirp rate; each group has a different effect on the overall system performance. The interference category is shown in Figure 4.

The three main groups are synchronous, semisynchronous and asynchronous interference. Synchronous interference, which is a relatively rare case [10, 17, 18], occurs when the victim and interference radars have identical waveform parameters $( k _ { v } = k _ { \mathrm { i n t } } )$ and operate within the same frequency band. Synchronous interference appears at the LPF output as a sinusoidal signal indistinguishable from a true target echo. This results in a high‐amplitude ghost target at an arbitrary distance. Semisynchronous interference refers to the case in which the victim and interference radar have similar but not identical chirp rates $( k _ { v } \approx k _ { \mathrm { i n t } } )$ . When the victim and interference chirps' parameters are different, $k _ { v } \neq k _ { \mathrm { i n t } } ,$ they are classified as asynchronous interference. The latter two, as will be shown in later, lead to a spread of interference across a number of range bins, and because the received interference power is normally high (owing to one‐way propagation), it can appear higher than the thermal noise floor of the system. This can be seen as an increase in the effective noise floor of the system, which affects target detection and overall system performance [19]. Asynchronous interference can be further divided into three subgroups: periodic, semiperiodic and aperiodic [20]. We define fractional times of interference appearance within each victim chirp as a vector $t _ { \mathrm { i n t } } = [ t _ { 1 } , t _ { 2 } , . . . , t _ { M } ] \colon$

(i) Periodic interference: all $t _ { i } \ \{ i = 1 . . . M \}$ are the same

(ii) Aperiodic interference: all $t _ { i } \ \left\{ i = 1 . . . M \right\}$ are different within the whole CPI duration

(iii) Semiperiodic interference: the $t _ { i }$ for first few victim chirps are different and then start to repeat, so that $[ t _ { 1 } , t _ { 2 } , . . . , t _ { m } ] = [ t _ { m n + 1 } , . . . , t _ { m n + n } ] , m \in N .$

The reason for considering these subgroups separately will be discussed subsequently during the interference analysis in the context of coherent integration.

## 2.2 | Simulation tool description

The analysis presented here is based on a computer simulation that was verified experimentally. The simulation tool consists of two main parts: road scenarios and radar signal modelling. The range to all targets $\left( R _ { t } \right)$ and interferers $\left( R _ { \mathrm { i n t } } \right)$ , as well as their velocity relative to the victim radar, are the inputs to the simulation. The radar transmit power, antenna radiation pattern and the target radar cross‐sections (RCSs), mainly cars and pedestrians [21], are predefined. Although the RCS of cars is aspect‐dependent and can fluctuate with small angle changes [3], we assume here that the RCS is non‐fluctuating within an interval of the coherent signal processing time (less than 10 ms). Various waveform parameters for victim and interference radars are incorporated at different stages of the analysis and are summarised in Table 1. The equations used to model FMCW signals are well‐described in the literature [7, 14, 22].

![](images/465bed09b873da064954396c1f65b12b5381f7a31d42944de9dadceb0ea4603f.jpg)  
F I G U R E 4 Interference type categories

## 3 | INTERFERENCE ANALYSIS IN VARIOUS DOMAIN

## 3.1 | Influence of low‐pass filter 1 impulse response on interference

Some reported techniques to reduce the effect of interference are based on suppressing interference in the time domain (such as zeroing or clipping [8]). By removing interference in time domain, part of the target signal will be removed as well; this results in signal‐to‐noise ratio (SNR) reduction. Therefore, a shorter duration of interference can result in better performance of mitigation techniques in the time domain. The LPF1 impulse response affects the interference duration and hence the effectiveness of the interference mitigation techniques that are applied in the time domain. To the best of our knowledge, a detailed analysis of the LPF1 impulse response on interference has not been presented before (apart from a brief statement in Sanka [7]) and the LPF1 parameters are generally specified without considering the presence of interference pulses.

The LPF1 can be considered a chain of low‐order analogue filters [23] followed by an analogue to digital converter (ADC) and, in some cases, digital filtering and decimation. Such lowpass filtering is used in FMCW radars to remove signals outside the expected beat frequency band and to limit the unambiguous range to $\begin{array} { r } { R _ { \operatorname* { m a x } } = \frac { c f _ { L P F } } { 2 k _ { \pi } } } \end{array}$ , where c is the speed of light. The interference duration that is limited by the cutoff frequency of the LPF1 is defined by [24]:

$$
\Delta T _ { \mathrm { i n t } } \approx \frac { 2 f _ { L P F } } { | k _ { v } - k _ { \mathrm { i n t } } | }\tag{ð1Þ}
$$

T A B L E 1 Waveform parameters incorporated in the analysis
<table><tr><td colspan="3">Victim</td><td colspan="3">Interference</td></tr><tr><td></td><td> $T _ { s v } ~ \mathrm { ( \mu s ) }$ </td><td> $B W _ { v }$  (GHz)</td><td></td><td> $T _ { s i n t } ~ \mathrm { ( \mu s ) }$ </td><td> $B W _ { \mathrm { i n t } } ~ \mathrm { ( G H z ) }$ </td></tr><tr><td> $\# V _ { 1 }$ </td><td>102.4</td><td>0.5</td><td> $\# I n t _ { 1 }$ </td><td>8</td><td>0</td></tr><tr><td> $\# V _ { 2 }$ </td><td>204.8</td><td>0.3</td><td> $\# I n t _ { 2 }$ </td><td>210</td><td>0.5</td></tr><tr><td></td><td></td><td></td><td> $\# I n t _ { 3 }$ </td><td>26</td><td>0.5</td></tr></table>

Equation (1) shows that $\Delta T _ { \mathrm { i n t } }$ is linearly proportional to $f _ { L P F }$ and inversely proportional to the difference between victim and interference chirp rates. However, $\Delta T _ { \mathrm { i n t } }$ also depends on the order of filter (n), which is not included in Equation (1). The filter order effect on interference duration is analysed by fixing the victim and interference radars' parameters as well as $f _ { L P F }$ to 10 ${ \mathrm { M H z } } ,$ and only changing the filter order. In this analysis, we considered receiving interference from $\# I n t _ { 1 }$ into $\# V _ { 1 }$ as the victim radar (Table 1). The normalized envelope of interference at the output of LPF1 in dB scale for filter orders 3 and 6 are shown in Figure 5(a) and (b), respectively. Because the signal is a linear frequency modulated pulse, its waveform in the time domain follows the frequency response of the filter. The interference duration varies depending on selected threshold levels, which have been chosen $\mathrm { a s } - 1 0 , - 3 0$ and −50 dB (red dotted, blue dashed and green dashed‐dotted vertical lines, respectively). For the −10 dB level, $\Delta T _ { \mathrm { i n t } }$ is around 4.8 and 4.4 µs for LPF1 of orders 3 and $^ { 6 , }$ respectively. At the −50 dB level, $\Delta T _ { \mathrm { i n t } }$ becomes $1 6 . 7 \mu \mathrm { s }$ for $\mathrm { n } = 3$ and is reduced to $7 . 7 \mu \mathrm { s }$ when the filter order increases to 6. The results show that the duration of interference is reduced by increasing the filter order when a lower threshold level is selected. The simulation result for $\mathrm { ~ n ~ } = \ 3$ is compared and validated by measured experimental data shown in Figure 5(c) and (d), respectively, demonstrating close agreement.

However, a blind increase in the order of the filter does not necessarily lead to a reduction in the duration of interference. The dependences of $\frac { \Delta T _ { \mathrm { i n t } } } { T _ { s v } }$ for various filter orders and threshold levels are shown in Figure 6(a). The general trend of interference duration shows a decrease as the filter order increases (steeper roll‐off) for all threshold levels for ${ \mathfrak { n } } = 1 - 5 ;$ however, in higher‐order filters, the transient response time (ringing) becomes more pronounced, which leads to the increased duration of interference pulses. To illustrate this ringing effect, the simulated interference signal after filter orders $\mathrm { ~ n ~ } = ~ 5$ (red line) and $\mathrm { \Omega } _ { \mathrm { n } } = \mathrm { \Omega } 8$ (black line) are shown in Figure 6(b). This example clearly shows higher ringing in the case of filter of order ${ \mathrm { ~ n ~ } } = ~ 8 ,$ which means additional time domain samples are corrupted by interference compared with the result of filter order $\mathrm { ~ n ~ } = \ 5$ . For this specific case, order $\mathrm { ~ n ~ } = \ 5$ may be considered the optimum filter order from the perspective of interference mitigation. LPF1 parameter optimization can be undertaken for other automotive radars cases, with different parameters, using a similar analysis.

## 3.2 | Interference analysis in time‐frequency domain and its parameter extraction

A spectrogram, obtained by applying STFT [25], reveals useful information about interference in the time‐frequency domain and can be used for interference detection, parameter estimation and the development of adaptive mitigation algorithms [14, 15]. The interference chirp pulses appear as a V‐shape signal [14, 26] whereas target reflections, which are a harmonic signal, appear as a horizontal line in the spectrogram. The amplitude and phase of the interfering signal are estimated in [27, 28]. The estimated parameters are used to reconstruct the interference signal and subtracted from the received instantaneous frequency (IF) signal. However, as stated by the authors, the accuracy of the proposed techniques in Bechter and Waldschmidt [27] and Bechter et al. [28] requires high calculation efforts and largely depends on the interference amplitude and the number of interfered samples: the higher the amplitude and the larger number of samples affected by interference, the better the accuracy of interference parameter estimation is. Here, an extra signal processing chain in the receiver with wideband LPF2 and STFT is proposed at the output of the mixer to analyse the spectrogram across the entire spectrum to extract a different set of interference parameters such as the start frequency, bandwidth, sweep time, chirp rate and idle time.

## 3.2.1 | Interference parameter extraction

The range of interference parameters that can be extracted from the spectrogram depends on the cutoff frequency of LPF, because this LPF2 is introduced. To illustrate this, two cutoff frequencies for LPF2 are used, $f _ { L P F 2 ( 1 ) } = 1 0 M H z$ (which is typical for automotive radar) and much wider $f _ { L P F 2 ( 2 ) } = 5 0 0 M H z$ (chosen to be equal to $B W _ { v } )$ . The simulated spectrogram of the received signal in # $V _ { 1 }$ from $\# I n t _ { 3 }$ is shown in Figure 7(a) and (b) using $f _ { L P F 2 ( 1 ) }$ and $f _ { L P F 2 ( 2 ) } ,$ respectively. The reflection from a target is clearly visible as a horizontal line in Figure $7 ( { \mathrm { a } } ) ;$ it is also present in Figure 7(b), but because of the wide scale of the spectrum, it is not clearly visible. Noise is not considered in this simulation. A sharp and narrow spectrogram appears for $f _ { L P F 2 ( 1 ) }$ because only a small fraction of the interference spectrum is passing through the filter. Figure $7 ( \mathrm { a } )$ can be used to detect interference and its exact time of appearance, which are crucial for further interference mitigation along the signal processing chain. However, a wider interference spectrogram is observed for $f _ { L P F 2 ( 2 ) }$ which contains more information about the interference. This can be used for interference parameter extraction, such as its sweep time, bandwidth and carrier frequency. However, using a conventional technique, a higher sampling frequency will also be required when a wider LPF2 is used, and there must be a trade‐off between its bandwidth and sampling/computational complexity, or alternative signal processing schemes to extract wide bandwidth data such as frequency discriminators, in which the ADC is placed after the discriminator, will require only a modest sampling rate and may also be considered.

(a)  
![](images/a390d128cf57bcaba56d7c1c20bb16bb8b4d26a14353153397215b0a463e0426.jpg)

(b)  
![](images/ec32809e1c3e890b410684fa96eba4d505ad788561e1c8d6461f3ef905d0b8f4.jpg)  
(d)

(c)  
![](images/22fc8d34a545a9e7f8a743c8778b0e2deea59d4a4afb664ecc3f52ddd157c56c.jpg)

![](images/c3b377226d5bfefd43393f0d8ce49039236391fd6bda5bfdd1be8ae4e13c8601.jpg)  
F I G U R E 5 Envelope of the interference signal for (a) n = 3 and (b) n = 6 interference amplitude (real part) in time domain at low‐pass filter 1 of thirdorder output (c) modelling results and (d) experimental results

(a)  
![](images/0e2234b6670dfcff480a3389483804534a18b4f60fbea0f23860a59cb3027f4f.jpg)

(b)  
![](images/2cd373d2ff905016cba1f985f3bd5985ec43bea81013dbeb4ecd1315c90df3a3.jpg)  
F I G U R E 6 (a) Interference ratio as a function of filter order of low‐pass filter 1; (b) observed ringing for higher‐order filter

The range of interference parameters that can be extracted from the spectrogram also depends on the relation of $T _ { s i n t }$ and

$T _ { s v } .$ . Two cases are considered here: case 1: $T _ { s v } > T _ { s i n t }$ (Figure 7(b)) and case 2: $T _ { s v } < T _ { s i n t }$ (Figure 8).

For case $1 , T _ { s i n t } ,$ interference idle time $( T _ { i d l e - i n t } ) , B W _ { \mathrm { i n t } }$ and $f _ { c i n t }$ can be estimated as:

(a)  
![](images/c5892e8f0f526214824821dc4b427b78b3cd245592e051701b4f4a7a5ebd96a5.jpg)

(b)  
![](images/c4eed69f5af429087e85e94167d8f531d855bed717476f1b25fa822ec6f7465d.jpg)  
F I G U R E 7 Spectrogram of interference with $( \mathrm { a } ) f _ { L P F 1 }$ and $\left( \mathrm { b } \right) f _ { L P F 2 }$

(a)  
(b)  
![](images/82e342d0bf71a7012849ea6a35bd5ad72e0c3a7d149090220bbd1cd55abb226e.jpg)

![](images/c8fff7861cbcad0f3c355e8d40ff831bf12870194a0e3aa3d6eb48d787849675.jpg)  
F I G U R E 8 Spectrogram of interference #Int in the victim (a) chirp 1 and (b) chirp 2

$$
\begin{array} { r } { T _ { s i n t } = t _ { S T F T } ( c _ { I } ) - t _ { S T F T } ( a _ { I } ) \qquad } \\ { T _ { i d l e - i n t } = t _ { S T F T } ( a _ { 2 } ) - t _ { S T F T } ( c _ { I } ) \qquad } \\ { B W _ { i n t } = f _ { v } ( c _ { I } ) - f _ { v } ( a _ { l } ) + f _ { S T F T } ( c _ { I } ) + f _ { S T F T } ( a _ { I } ) } \\ { f _ { c i n t } = f _ { v } ( a _ { I } ) - f _ { S T F T } ( a _ { I } ) \qquad } \end{array}\tag{ð2Þ}
$$

where t<sub>STFT</sub> and $\mathbf { \Psi } _ { f r F T }$ are the time and frequency of the signal in the spectrogram and $f _ { v }$ is the frequency of the victim chirp at the selected time, for example, $c _ { 1 } .$ . In the case where $B W _ { v } < B W _ { \mathrm { i n t } } .$ , there may be ambiguity in the estimated value of $B W _ { \mathrm { i n t } }$ . Different values of $B W _ { \mathrm { i n t } }$ could be calculated from consecutive interference chirps observed in the successive spectrograms. The larger value of $B W _ { \mathrm { i n t } }$ can be considered as the value closer to the actual $B W _ { \mathrm { i n t } } .$ For case 2, that is, $T _ { s v } < T _ { s i n t } ,$ a number of consecutive signal chirps are analysed. An example is presented here using $\# I n t _ { 2 }$ with a sweep time of $2 1 0 ~ \mu \mathrm { s }$ and a bandwidth of 0.5 GHz into $\# V _ { 1 }$ with a sweep time of 102 4 µs and a bandwidth of 0.5 GHz. Two consecutive victim chirps that received interference from the same source, as shown in Figure 8, are required to extract the interference parameters for this specific case. The interference parameters can be calculated as:

$$
\begin{array} { r l } & { T _ { s i n t } = t _ { S T F T } ( c _ { I } ) - t _ { S T F T } ( a _ { I } ) + t _ { S T F T } ( c _ { 2 } ) } \\ & { \qquad - t _ { S T F T } ( a _ { 2 } ) + t _ { i d l e - v } } \\ & { T _ { i d l e - i n t } = t _ { S T F T } ( a _ { 3 } ) - t _ { S T F T } ( c _ { 2 } ) } \\ & { B W _ { i n t } = B W _ { v } \pm f _ { S T F T } ( c _ { I } ) m f _ { S T F T } ( a _ { I } ) } \\ & { \qquad f _ { c i n t } = f _ { v } ( a _ { I } ) \pm f _ { S T F T } ( a _ { I } ) } \end{array}\tag{ð3Þ}
$$

The idle time of the victim radar $( T _ { i d l e - v } )$ should be considered to obtain the sweep time of the interference in case 2. The accuracy of the estimated $B W _ { \mathrm { i n t } }$ reduces for case 2 when interference has a wider bandwidth than the victim radar bandwidth. With these examples, it has been shown that the parameters of interference can be directly extracted from the spectrogram and such estimated parameters using Equations (2) and $( 3 ) ,$ shown in Table $^ { 2 , }$ together with the actual interference parameters. The estimated values for interference sweep time and idle time for both cases are reasonably accurate. High accuracy is observed for the interference bandwidth and the start frequency for shorter interference; however, there is some ambiguity for these two values for a longer interference sweep time. A comprehensive algorithm to enable extraction of interference parameters for wider cases and in more complex scenarios (downchirp, multiple interference, etc.) is the subject of ongoing future work.

## 3.2.2 | Effect of wideband low‐pass filter 2 on spectrogram background level

Our analysis shows that it is possible to extract interference parameters using an extra wideband channel after the mixer. However, the wide bandwidth lead to larger thermal noise power at the wideband LPF2 output, which could result in less efficient interference parameter extraction. To analyse this, interference from $\# I n t _ { 2 }$ with an amplitude of the same order as the thermal noise (weak interference [29]) into $\# V _ { 1 }$ is considered and plotted in Figure 9(a). The spectrogram at the output of the filter with $f _ { L P F 2 ( 1 ) }$ and $f _ { L P F 2 ( 2 ) }$ filters is shown in Figure 9(b) and (c), respectively. The V‐shape spectrograms of interference appeared well above the noise for both cases, and interference parameter extraction would be possible using Figure 9(c).

## 3.2.3 | Experimental validation

To validate the simulated results, the spectrograms of the measured data are compared with the simulation results. The experimental data obtained by two off‐the‐shelf automotive radars: radar 1 with $f _ { L P F } = 3 . 5 M H z$ and radar 2 $f _ { L P F } = 1 0 M H z$ (shown in Table A1 in Appendix); the victim radars are shown in Figure 10. Their waveform parameters correspond to $\# V _ { 1 }$ (Table 1) and interference is from $\# I n t _ { 1 }$ These data also show the influence of LPF2 characteristics on the appearance of interference in the time‐frequency domain. The signal obtained by victim radar 1 shows a sharp and narrow V from interference Figure 10(a) and (b) compared with the results obtained from victim radar 2 in Figure 10(c) and (d). The simulation results coincide well with the experimental results.

## 3.3 | Interference analysis in range domain

Ideally, the signal at the LPF1 output would contain an almost monochromatic target echo and, in some cases, time‐limited interference pulses. After fast‐FFT processing, the target echo will appear over a small number of range bins, whereas the interference being frequency modulated will spread over a number of range bins. The latter appears as an increase in the noise floor of the system, referred to here as the interference noise level. To analyse the interference spread for the three main interference groups (synchronous, semisynchronous and asynchronous), the victim radar parameters are fixed $( \# V _ { 2 } )$ and the interferer parameters are varied to provide different interference cases. In this analysis, the target is placed at about 20 m from the victim radar and interference at a range of 70 m. The simulation results for the synchronous case in the time and range domains are shown in Figure 11.

T A B L E 2 Estimated and actual interference parameters
<table><tr><td rowspan="2"></td><td colspan="2"> $T _ { s v } > T _ { s i n t }$ </td><td colspan="2"> $T _ { s v } < T _ { s i n t }$ </td></tr><tr><td>Estimated (2)</td><td>Actual</td><td>Estimated (3)</td><td>Actual</td></tr><tr><td> $T _ { s i n t } ~ \mathrm { ( \mu s ) }$ </td><td>26</td><td>25.6</td><td>209.6</td><td>210</td></tr><tr><td> $T _ { i d l e - i n t } ~ ( \mu \mathrm { { s } ) }$ </td><td>3.2</td><td>3</td><td>11</td><td>10</td></tr><tr><td> $B W _ { \mathrm { i n t } } ~ \mathrm { ( G H z ) }$ </td><td>0.51</td><td>0.5</td><td>0.36, 0.5</td><td>0.5</td></tr><tr><td> $f _ { \mathrm { o i n t } } ~ \mathrm { ( G H z ) }$ </td><td>75.99</td><td>76</td><td>76.1, 75.9</td><td>75.9</td></tr></table>

The interference looks to be close to a monochromatic signal and acts similarly to a target echo, which results in the appearance of a ghost target in the range domain. Synchronous interference is difficult to differentiate from a real target return; however, the probability of this type of interference occurring is small [10, 17, 18].

The time and range domain data for the semisynchronous interference $\left( k _ { v } \approx k _ { \mathrm { i n t } } \right)$ case are plotted in Figure 12(a) and (b), respectively. Figure 12(b) shows that this interference is spread over a number of range bins, leading to a significant increase in the interference noise level, masking the target at 20 m. There is a higher probability of occurrence of this type of interference compared with synchronous interference. Mitigation techniques that apply in the time domain, such as zeroing [8], will not be as effective for this type of interference because by replacing zeros for interference duration, almost all of the target signal will be removed, too.

The third and most common group is asynchronous interference $( k _ { v } \neq k _ { \mathrm { i n t } } )$ . The interference radar has the same bandwidth as the victim radar (0.3 GHz), but the sweep time of interference is $6 5 ~ \mu \mathrm { s }$ whereas the victim radar sweep time is 204.8 µs. Interference occurs as short, double‐sided chirp modulated pulses (Figure 13(a)) and results in a broader spread in the range domain compared with the semisynchronous interference group; consequently, the interference level is lower, considering the same received interference power (Figure 13(b)).

Considering the case in which only the interference signal transmitted from another FMCW radar is present in the receiver of the victim radar, the instantaneous frequency $( f _ { I F } )$ of the received interference can be written as:

$$
f _ { I F } = \frac { 1 } { 2 \pi } \frac { d } { d t } \phi ( t ) = ( k _ { v } - k _ { \mathrm { i n t } } ) t + ( f _ { c v } - f _ { c i n t } + k _ { \mathrm { i n t } } \tau _ { \mathrm { i n t } } )\tag{ð4Þ}
$$

where $\tau _ { \mathrm { i n t } }$ is the time delay between the victim and interference chirp. The first term defines the spread of interference spread in the range domain and the second term is the frequency at which the pedestal is formed. Using the first term, the number of range bins $( N _ { \mathrm { i n t } } )$ that the interference spread can be obtained. The number of range bins corrupted by the interference multiplied by the beat frequency resolution should be equal to $| \bar { k _ { v } } - \bar { k _ { \mathrm { i n t } } } \ | \ T _ { s v } ;$ therefore, $N _ { \mathrm { i n t } }$ depends on the victim and interferer chirp rates and the sweep time of the victim radar:

(a)  
![](images/78f633946fc0abe2e0e0f6896740174404f63746bb48783e24f42c2ac5f047af.jpg)

(b)  
![](images/270788890a7cc348d18bf7a608b8d587fb29dd2dd7fe16124640167d65e9e2c9.jpg)

(c)  
![](images/4e1948684491a01f41a5be7430ccae64d288ba40f1440a0abf21a8e89a8c9716.jpg)  
F I G U R E 9 Appearance of weak interference signal in (a) time domain spectrogram of signal using (b) $f _ { L P F 1 }$ and $\left( \mathrm { c } \right) f _ { L P F 2 }$

$$
N _ { i n t } = \mid k _ { v } - k _ { i n t } \mid T _ { s v } ^ { 2 }\tag{ð5Þ}
$$

This can be used to obtain the interference noise level as ${ V _ { \mathrm { i n t } } } ^ { 2 } / { \sqrt { N _ { \mathrm { i n t } } } }$ where $V _ { \mathrm { i n t } }$ is the interference level into the receiver of the victim radar. Equation (5) shows the spread of interference before LPF. The number of bins will be reduced depending on $f _ { L P F }$ with no changes in the interference noise level. Equation $( 5 )$ shows two important factors that define the spread of interference in the range domain and consequently the interference noise level. Closer victim and interferer chirp rates, such as a semisynchronous case, means less interference spread (with a corresponding higher interference level), and a longer victim sweep time means a larger interference spread (with a corresponding lower interference level). Figure 14(a) shows the interference spread for various values of $k = | k _ { v } - k _ { \mathrm { i n t } } |$ in a victim radar $( \# V _ { 2 } )$ . The result shows an increased interference spread and a lower interference level as k increases. Figure 14(b) illustrates the influence of the sweep time of the victim radar on the spread of interference in the range domain, where k is kept constant (0.005) and the sweep time of the victim is changed. The range profile of four different values of $T _ { s v }$ in Figure 14(b) shows an increased spread and a lower interference level for a longer victim sweep time as indicated in Equation (5). The observed bow shape in the spectrum of the signal for k ¼ 0:5 in Figure 14(a) and $T _ { s v } = 1 ~ m s$ in Figure 14(b) corresponds to asynchronous interference when $T _ { s v } < T _ { s i n t }$

## 3.4 | Coherent signal integration

To increase the SNR, a number of chirps are integrated over the CPI, which is a characteristic of the individual radar design, but typically, it has an order of milliseconds. If the target reflections remain coherent during a CPI consisting of M chirps, the signal power increases as $M ^ { 2 }$ , whereas the thermal noise power increases as M. As for the interference, its power after integration depends on its correlation property during CPI [20]. Schipper et al. [24] estimate a gain in the signal to interference ratio (SIR) as a function of the time‐bandwidth product, scaling factor, and windowing, and if an in‐phase and quadrature component receiver is used. However, in this subsection, the effect of coherent signal integration on the SIR for various types of interference is analysed. The analysis of the effect of coherent integration of different subcategories of asynchronous interferers (periodic, semiperiodic and periodic [Figure 4]) is discussed by the trend of interference level after integration during CPI as well as an evaluation of interference correlation during this time (Figure 15). For this analysis, a bandwidth of 0.3 GHz and carrier frequency of 76 GHz are used for the victim and interference radars, and only the sweep time of the interference is changed to provide different interference classes. The sweep times of the victim and interferer radars are shown in Table 3.

(a)  
![](images/b197eff40fb07b2c6955de94d3f98f663a70bd38b1b444dae9d805babbf827cf.jpg)

(b)  
![](images/20604f0baa9314495f9666f175832b1b462a8a95d348628de867ad4e391960ce.jpg)

(c)  
![](images/82cabf4f6a04582761df262034f72774fd862926d102661aae44a5e07cd6d2f7.jpg)

(d)  
![](images/c4f088dc1b9f4fef072d64d40f9c46785fe6b3c72b816b7df017e48a9061b1bf.jpg)  
F I G U R E 1 0 Spectrogram of collected signal by victim radar 1 in presence of #Int (zoomed version): (a) simulation and (b) experiment; and by victim radar 2: (c) simulation and (d) experiment

![](images/8d350ca739af40e3cca9a6b1f5a9fc6d4ba38d62f2cd795be10e5164acdf8c32.jpg)  
(b)

![](images/0aa051c2f551edb7ef384ddaa4140dce04dbe62a8ec070b86555f9392b4c7505.jpg)  
F I G U R E 1 1 Amplitude (real‐part) of target and synchronous interference: (a) time domain and (b) range domain

Figure 15(a) shows an increase in the interference level as a function of the number of integrated chirps, normalized to the first chirp, for all three types of asynchronous interferences. The trend for fully correlated and uncorrelated cases is also plotted for reference. The average correlation coefficient, presented in Figure 15(b), is calculated as $\rho _ { a v } = \rho _ { s } / M ,$ where $\rho _ { s }$ is the sum of correlation coefficients between interference pulses across all of the victim chirps.

The highest increase in interference level during CPI corresponds to periodic interference, which is the fully

![](images/7ccabe626718ca96cc2cbccd1bfd83d886d6d685f14107769235a5888d572893.jpg)  
(b)

![](images/ee6a98b091b45f5365f6b555bc702cf15fc815e6d27fd342e941a4b5573be97f.jpg)  
F I G U R E 1 2 Amplitude (real‐part) of target and semisynchronous interference: (a) time domain and (b) range domain

![](images/c47a8f3157eab67af57fc4fe5ae40ce2d972773bde403dd6519cfb8e9d8232bd.jpg)  
(b)

![](images/a028827786daac4d883c2e75ae347671ac389f563847561778e4b96d56c462f2.jpg)  
F I G U R E 1 3 Amplitude (real‐part) of target and asynchronous interference $( T _ { s v } > T _ { s i n t } ) :$ (a) time domain and (b) range domain

(a)  
![](images/a923a2cbc639d4154270bb19d517f16c2b409c1833171941a6ca4275b1db5867.jpg)

(b)  
![](images/003b182808a6eb76e1b255d22b9e2cf5bcb65680be4178ed90220b3660226aaa.jpg)  
F I G U R E 1 4 Interference spread in range domain for various (a) k and (b) $T _ { s v }$ for k = 0.005

(a)  
![](images/ad480a68149fa63c6d4905fe142410d28a9d083db063c45568cc1c8a87e51a56.jpg)

(b)  
![](images/30259e01c1f6396cdf8d3ed15bdc2b12a9069144e52a466737d0061af76f5465.jpg)  
F I G U R E 1 5 (a) Interference level and (b) average correlation coefficient over number of integrated chirps for three asynchronous interference cases

T A B L E 3 Victim and interferer parameters
<table><tr><td></td><td>Victim</td><td>Periodic</td><td>Semiperiodic</td><td>Aperiodic</td></tr><tr><td>Sweep time (μs)</td><td>100</td><td>30</td><td>32</td><td>31.9</td></tr><tr><td>Chirp rate (MHz/μs)</td><td>3</td><td>10</td><td>9.37</td><td>9.4</td></tr></table>

correlated case; hence, no improvement in SIR occurs by integration. Because of the periodicity of interference among the victim radar chirps for periodic interference, the average correlation coefficient equals 1 for the whole CPI. Aperiodic interference shows the lowest increase in the interference level because it is the uncorrelated case; therefore, the improvement in SIR corresponds to the number of integrated pulses. The semiperiodic interference shows zero correlation between interference at the beginning of integration, the first six chirps for this specific case, and the trend of interference level following the uncorrelated case. After this, the average correlation increases to 1 (as the interference repeats) and the interference level increases to become similar to the correlated case. Hence, the SIR improvement falls between these two extreme cases. This analysis shows that destroying the interference coherency can decrease the interference level and may maximise SIR improvement. The effectiveness of waveform randomisation to reduce the detrimental effect of periodic and semiperiodic interferences was shown in our earlier work [20].

## 3.5 | Interference effect in range‐Doppler map

Understanding of how various categories of interference manifest in the range‐Doppler (R‐D) domain is important to assess the effects on target parameter (i.e., range and velocity) estimation. The target Doppler frequency is estimated across multiple returns from multiple transmitted chirps during CPI.

## 3.5.1 | Interference in range‐Doppler map

The appearance of interference cases (categorised in Figure 4) in the R‐D map for $( \# V _ { 2 } )$ is presented using two targets (cars) with an RCS of 10 dBsm, with a range and relative speed of 20 m and 12 km/h for target 1 and 60 m and −10 km/h for target 2. The interference source is placed on target 2. The parameters of the victim radar are fixed and only the interferer parameters are changed to provide various interference types, as summarised in Table 4. The expected appearance of different types of interference in the R‐D map are also summarised in Table 4.

The R‐D maps in the presence of synchronous and semisynchronous interference are shown in Figure 16. For synchronous interference, a ghost target appears in the R‐D map at an arbitrary distance and relative speed. The semisynchronous interference case appears differently in the R‐D map depending on the interference pulse periodicity within the victim chirps during CPI. If the interference appears periodically during the whole CPI, the interference power spreads across the range bins at only half of the true relative speed of the interference (Figure 16(b)). However, the small chirps result in wider spread along the range axis (owing to a shift in pedestal in each victim chirp (Figure 12(b)) and

Doppler axis (owing to different Doppler shifts across the victim chirps) (Figure 16(c)).

Figures 17–19 illustrate the R‐D maps in the presence of asynchronous interference corresponding to three groups: periodic, semiperiodic and aperiodic interference, respectively. In all of these cases, $T _ { s v } < T _ { s i n t }$ and $T _ { s v } > T _ { s i n t }$ are considered. There is no Doppler spread for the periodic case, and thus two distinctive lines are expected at positive and negative Doppler frequencies for this type of interference. Small peaks and nulls are observed for the periodic case with shorter interference. This results from the presence of more than one interference chirp within one victim chirp (similar to Figure 13(c)). The amplitude of the interference line in the R‐D map depends on the interference spread as defined in Equation (5). Semiperiodic interference results in an increased number of parallel lines across the R‐D map in Figure 18. Interference spread along Doppler bins depends on the position of interference chirps during CPI, and hence a larger number of lines for shorter interference. The peaks and nulls are visible for both cases, $T _ { s v } < T _ { s i n t }$ and $T _ { s v } > T _ { s i n t }$ , as the interference become periodic after first few victim chirps; however, they have a more random appearance for shorter interference. This is due to the presence of more than one interference chirp within each victim chirp.

Finally, the most common group of interference, aperiodic interference, in which aperiodicity between the victim and interference chirps during CPI, results in the random spread of interference over all of the R‐D map (Figure 19). The presence of visible bows and nulls for interference with a longer sweep

T A B L E 4 Victim and interferer parameters
<table><tr><td rowspan="2"></td><td rowspan="2"></td><td colspan="2">Interferer parameter</td><td rowspan="2"></td></tr><tr><td> $T _ { s i n t } ( \mu \mathrm { s } )$ </td><td> $B \ W _ { i n t } ( \mathrm { G H z } )$ </td></tr><tr><td>Synchronous</td><td> $k _ { v } = k _ { \mathrm { i n t } }$ </td><td>204.8</td><td>0.3</td><td>Ghost target at arbitrary distance and Doppler of interference</td></tr><tr><td>Figure 16(a)</td><td></td><td></td><td></td><td></td></tr><tr><td>Semisynchronous Figure 16(b)</td><td> $k _ { v } \approx k _ { \mathrm { i n t } }$ </td><td>204.8</td><td>0.299</td><td>Short spread of interference energy across range bins Wide spread of interference energy across range</td></tr><tr><td></td><td></td><td></td><td></td><td>and Doppler bins</td></tr><tr><td>Asynchronousk  $\triangleq { k _ { i n t } }$  Periodic Figure 17</td><td></td><td>204.8</td><td></td><td>Two distinctive line in range-Doppler map</td></tr><tr><td></td><td>TAnd  $B W _ { v } \neq B W _ { \mathrm { i n t } } \mathrm { O R } \ T _ { s i n t } \sim \infty$   $T _ { s v } / T _ { s i n t } > 1 T _ { s v } = n T _ { s i n t }$ </td><td>25.6</td><td>0.25 0.3</td><td>Two distinctive line in range-Doppler</td></tr><tr><td>Semiperiodic Figure 18  $m T _ { s v } = n T _ { s i n t }$ </td><td></td><td></td><td></td><td>map with small peaks and nulls</td></tr><tr><td></td><td> $T _ { s v } / T _ { s i n t } < 1$   $T _ { s v } / T _ { s i n t } > 1$ </td><td>1400 46.5</td><td>0.3 0.3</td><td>Multiple parallel line with bow shape Multiple parallel line with more random appearance</td></tr><tr><td></td><td></td><td></td><td></td><td>peaks and nulls in each line</td></tr><tr><td>Aperiodic Figure  $1 9 ~ m T _ { s v } \neq n T _ { s i n t }$ </td><td> $T _ { s v } / T _ { s i n t } < 1$   $T _ { s v } / T _ { s i n t } > 1$ </td><td>702.4 46.2</td><td>0.3</td><td>Diagonal ridges Small diagonal ridges that get more random appearance</td></tr><tr><td></td><td></td><td></td><td></td><td>when the number of interference chirps increases in each victim chirp</td></tr><tr><td>Aperiodic experimental</td><td></td><td>35.6</td><td></td><td></td></tr></table>

(a)  
![](images/09895fec1c2888ded895fd10a765dd20501f67068d1b0d8d7bf98ea0212ab9ba.jpg)  
(c)

(b)  
![](images/309a56dce37561bc7ae8b98141d24413754b1a0fb2d87af84f63e792bc76a005.jpg)

![](images/16fb1b84164c5515cc6162fc13998142ff46b44a20f94457b121e7d416c4a3a3.jpg)  
F I G U R E 1 6 Range‐Doppler map in the presence of (a) synchronous interference, and semi‐synchronous (b) periodic and (c) aperiodic interference

(a)  
![](images/df1c00a5cd010ee6e1beba02c02674fd45bfe31e83f2bea76405fc1ab2ffb743.jpg)  
(b)

![](images/ccc2affa3a3ca5ffec6e2f6a57e737924b3c6b45e7350c11b27395e0e0720bcc.jpg)  
F I G U R E 1 7 Range‐Doppler map in the presence of periodic asynchronous interference: (a) longer and (b) shorter interference chirp

time (Figure 14) and their integration result in the presence of diagonal ridges in the R‐D map. For a shorter interference case, the peaks and nulls appear more randomly. This randomness increases when the number of interference chirps increases per victim chirp.

## 3.5.2 | Experimental validation

A number of experiments were conducted to obtain R‐D maps for various interference cases. One example, which corresponds to aperiodic interference and $T _ { s v } > T _ { s i n t }$ , uses radar 1 (Appendix) as the victim radar with parameters defined as $( \# V _ { 2 } )$ in Table 1 with a duty cycle of 78%. The interference radar (radar 2) has a 35.6‐µs sweep time, 0.4‐GHz bandwidth and 40% duty cycle. A corner reflector (CR) is used as a reference target and is placed 6 m from the victim radar. The interference radar is placed at 8 m. Multiple reflections from walls and room furniture are also observed in the measured data. The victim radar, targets and interference radar are all static. Not all victim radar chirps received interference owing to the different PRIs of the victim and interference radars. The R‐D map obtained from experiment and simulation is shown in Figure 20. The R‐D map shows a rise in the noise floor and a diagonal line as expected (three interference chirps per victim chirp). The comparison between the modelling and experimental R‐D maps confirms the accuracy of the modelling results.

(a)  
![](images/6632c7dcb8716a267ec1ecb92597206680332d3fbd8e2f5e4ae3ce9196d69d70.jpg)

(b)  
![](images/8cfbb54fcc643f0664e0694773b1438096b6400a8ae97d97abbba71d917b0d00.jpg)  
F I G U R E 1 8 Range‐Doppler map in the presence of semiperiodic asynchronous interference: (a) longer and (b) shorter interference chirp

(a)  
![](images/87f44a1339dad92f94ba68dd2067f3050851733ca796ff91abbf24625daa3d17.jpg)  
(b)

![](images/82b11e9df4beb9336a275720e5a57d902c856321e874b11b55802deaec4958c8.jpg)  
F I G U R E 1 9 Range‐Doppler map in the presence of aperiodic asynchronous interference: (a) longer interference and (b) shorter interference

(a)  
![](images/98957567e443af3cd7af39d3f40170c145a664fa396a323382a460cf3bc79769.jpg)

(b)  
![](images/9f20ba741902b770494d50df97d624529b91eb2cb8bb5b5865902e2a015a265f.jpg)  
F I G U R E 2 0 Range‐Doppler map in the presence of aperiodic interference: (a) measurement and (b) simulation

The interference analysis in the various domains showed that the SIR increases along the signal processing chain. Initially, the LPF rejects part of the interference. In the next stage, the interference spreads across various range bins after fast‐FFT processing. Finally, the SIR is improved owing to coherent signal integration in the slow‐FFT, depending on the type of interference. All of the simulation and experimental analysis on the effect of various types of interference in different stages of FMCW radar signal processing shows that the effect of interference strongly depends on the victim and interference radar parameters. This illustrates the importance of a universal tool to identify the expected effects of interference [30].

## 4 | CONCLUSION

This work provides an analysis of interference behaviour at various stages in an FMCW radar signal processing chain by simulation modelling and experimental validation. The analysis shows how interference manifests in each domain and reveals how interference affects the functionality of the victim radar. The analysis shows the need to optimize the LPF1 impulse response to improve the effectiveness of interference mitigation techniques that apply in the time domain. The spectrogram is shown to be a useful tool to detect interference and to extract interference parameters. The effect of different interference types after coherent integration on the SIR is also studied. The R‐D map in the presence of different interference types are explained. This level of analysis is required for other types of modulation that are used or are proposed for implementation in future automotive radars, such as phase modulated continuous wave radars as part of future work.

## ACKNOWLEDGEMENTS

This work is supported by Innovate UK Grant 104526 and is part of the Co‐existence Simulation Modelling of Radars for Self‐Driving (COSMOS) project.

## ORCID

Fatemeh Norouzian https://orcid.org/0000-0003-2713- 9929

Anum Pirkani https://orcid.org/0000-0002-6968-0206

## REFERENCES

1. Bilik, I., et al.: The rise of radar for autonomous vehicles: signal processing solutions and future research directions. IEEE Signal Process Mag. 36(5), 20–31 (2019)

2. Ryde, J., Hillier, N.: Performance of laser and radar ranging devices in adverse environmental conditions. J. Field Robotics. 26(9), 712–727 (2009)

3. Hasch, J., et al.: Millimetre‐wave technology for automotive radar sensors in the 77 GHz frequency band. IEEE Trans. Microwave Theory Techn. 60(3), 845–860 (2012)

4. Meinel, H.H.: Evolving automotive radar—from the very beginnings into the future. In: European Conference on Antennas and Propagation (EuCAP), pp. 3107–3114. The Hague (2014)

5. Goppelt, M., Blöcher, H.‐L., Menzel, W.: Analytical investigation of mutual interference between automotive FMCW radar sensors. In: German Microwave Conference, pp. 1–4.Darmstadt (2011)

6. Alland, S., et al.: Interference in automotive radar systems: characteristics, mitigation techniques, and current and future research. IEEE Signal Process Mag. 36(5), 45–59 (2019)

7. Sanka, S.: Radar to Radar Interference for 77GHz Automotive Radar. Master thesis, Delft University of Technology (2017)

8. Brooker, G.M.: Mutual interference of millimetre‐wave radar systems. IEEE Trans. Electromagn. Compat. 49(1), 170–181 (2007)

9. Murali, S., et al.: Interference detection in fmcw radar using a complex baseband oversampled receiver. In: IEEE Radar Conference (Radar-Conf18), pp. 1567–1572 (2018)

10. Jin, F., Cao, S.: Automotive radar interference mitigation using adaptive noise canceller. IEEE Trans. Veh. Technol. 68(4), 3747–3754 (2019)

11. Patole, S.M., et al.: Automotive radars: a review of signal processing techniques. IEEE Signal Process. Mag. 34(2), 22–35 (2017)

12. Levanon, N.: Radar Principles. Wiley & Sons, New York (1988)

13. Stove, A.G.: Linear FMCW radar techniques. In: IEE Proceedings F ‐ Radar and Signal Processing, vol. 139, pp. 343–350 (1992)

14. Neemat, S., Krasnov, O., Yarovoy, A.: An interference mitigation technique for FMCW radar using beat‐frequencies interpolation in the STFT domain. IEEE Trans. Microwave Theory Techn. 67(3), 1207–1220 (2019)

15. Tullsson, B.: Procedure for the elimination of interference in a radar unit of the fmcw type. US Patent 6,469,662 (2002)

16. Uysal, F.: Synchronous and asynchronous radar interference mitigation. IEEE Access. 7, 5846–5852 (2019)

17. Khoury, J., et al.: RadarMAC: mitigating radar interference in self‐driving cars. In: IEEE International Conference on Sensing, Communication, and Networking (SECON), pp. 1–9. London (2016)

18. The MOSARIM Consortium: Generation of an Interference Susceptibility Model for the Different Radar Principles. Workpackage: General Interference Risk Assessment (2010)

19. Overdevest, J., et al.: Uncorrelated interference in 79 GHz FMCW and PMCW automotive radar. In: International Radar Symposium (IRS), pp. 1–8. Ulm (2019)

20. Norouzian, F., et al.: Automotive radar waveform parameters randomisation for interference level reduction. In: IEEE Radar Conference (RadarConf20), pp. 1–5. Florence (2020)

21. Matsunami, G., Nakamura, R., Kajiwara, A.: RCS measurements for vehicles and pedestrian at 26 and 79GHz. In: 6th International Conference Signal Processing and Communication Systems (ICSPCS), pp. 1–4. Gold Coast (2012)

22. Kim, G., Mun, J., Lee, J.: A peer‐to‐peer interference analysis for automotive chirp sequence radars. IEEE Trans. Veh. Technol. 67, 8110–8117 (2018)

23. Xie, S.: Practical filter design challenges and considerations for precision ADCs. Analog Dialogue. 50‐04, 1–5 (2016)

24. Schipper, T., et al.: Discussion of the operating range of frequency modulated radars in the presence of interference. Int. J. Microw. Wireless Technol. 6, 371–378 (2014)

25. Mitra, S.K.: Digital Signal Processing: A Computer‐Based Approach, 2nd ed. McGraw‐Hill, New York (2001)

26. De Luca, A., et al.: FSR velocity estimation using spectrogram. In: International Radar Symposium (IRS), pp. 1–5. Krakow (2016)

27. Bechter, J., Waldschmidt, C.: Automotive radar interference mitigation by reconstruction and cancelation of interference component. In: IEEE MTT‐S International Conference on Microwaves for Intelligent Mobility (ICMIM), pp. 1–4. Heidelberg (2015)

28. Bechter, J., Biswas, K.D., Waldschmidt, C.: Estimation and cancelation of interferences in automotive radar signals. In: 18th International Radar Symposium (IRS), pp. 1–10. Prague (2017)

29. Laghezza, F., Jansen, F., Overdevest, J.: Enhanced interference detection method in automotive FMCW radar systems. In: International Radar Symposium (IRS), pp. 1–7. Ulm (2019)

## A | APPENDIX: Experiment Description

Three different radars are used during the experiments. The parameters of these radars are presented in Table A1. Radars 1 and 2 are off‐the‐shelf automotive radars and are used as both

30. Norouzian, F., et al.: A graphical heatmap tool to analyse the effects of interference in automotive radar. In: IEEE Radar Conference (Radar-Conf20), pp. 1–6. Florence (2020)

How to cite this article: Norouzian F, Pirkani A, Hoare E, Cherniakov M, Gashinova M. Phenomenology of automotive radar interference. IET Radar Sonar Navig. 2021;1–16. https://doi.org/10.1049/rsn2.12096

victim and interferer radars with reconfigurable waveform parameters (sweep time, bandwidth, etc.). A non‐modulated continuous wave, radar 3, is also used as a source of interference. A CR with RCS of 14 dBsm is the main calibrated target.

<table><tr><td>Radar</td><td>#1</td><td>#2</td><td>#3 (Transmit only)</td></tr><tr><td>Start frequency (GHz)</td><td>76</td><td>76</td><td>76.1</td></tr><tr><td>Bandwidth (GHz)</td><td>0.2~2</td><td>0.1~2</td><td>0</td></tr><tr><td>Sweep time (μs)</td><td>25.6~200</td><td>25.6~200</td><td>8</td></tr><tr><td>Antenna type</td><td>Patch</td><td>Patch</td><td>Waveguide horn</td></tr><tr><td rowspan="2">Receive antenna gain GRx (dBi)</td><td>15</td><td>15</td><td>NA</td></tr><tr><td>17</td><td>17</td><td>20</td></tr><tr><td>Rx antenna</td><td>12 × 76</td><td>12 × 76</td><td>NA</td></tr><tr><td colspan="4">Beam-width  $\mathrm { ( A \times E ) ( ^ { o } ) }$ </td></tr><tr><td>Transmitter antennaBeam width (A × E) (°)</td><td>13 × 51</td><td>13 × 51</td><td>20 × 20</td></tr><tr><td>Number of chirps</td><td>128</td><td>128</td><td>NA</td></tr></table>

Abbreviations: NA, not available.

T A B L E A1 Parameters of radars used in the experiments