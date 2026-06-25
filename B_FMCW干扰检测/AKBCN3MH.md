# FMCW Interference Waveform Estimation Based on Intentional Local Interference for Automotive Radars

Sungpil Cheon ∙ Hyungwoo Kim ∙ Byungkwan Kim<sup>\*</sup>

## Abstract

We propose a new method to estimate the waveforms of frequency-modulated continuous-wave (FMCW) interferers by intentional interference. The proposed method utilizes the crossing interference of FMCW radar by adaptive waveform configuration. The victim radar analyzes the periodicity and frequency of the interference signal from the mixer at the FMCW receiver. The bandwidth, slope, and intervals of the interferer waveform are derived from multiple adaptive waveforms from interference detection results. The estimated time and frequency waveform parameters of the interferer can be utilized to generate an interference-free waveform. The proposed approach has been tested and validated using two different mmWave commercial off-the-shelf automotive FMCW radars: the AWR2243 and AWR2944 evaluation boards. In three different scenarios in indoor and outdoor environments, the proposed method successfully estimated interferer waveform parameters with 0.9 seconds of monitoring processing and less than 3% error.

<sup>Key</sup> <sup>Words</sup>: FMCW Radar, Multiple-input Multiple-output Radar, Radar Interference, Radar Remote Sensing, Radar Recognition, Signal Processing.

## I. INTRODUCTION

Millimeter wave (mmWave) frequency-modulated continuous-wave (FMCW) radars are installed in automotive vehicles for safety and driver assistant functions, such as collision mitigation, blind spot detection, land change assistance, and parking assistance. Radar is also utilized for autonomous driving due to its robustness in harsh weather and low cost [1].

Most recent radars installed in automotive vehicles adopt FMCW waveforms and utilize large bandwidths up to several GHz. According to the working principle of FMCW radar, a large bandwidth results in high range resolution, which can improve environment recognition performance [2]. A single vehicle utilizes front and multiple corner radars to monitor the driving environment [3]. For these safety and technical reasons, the number of mmWave FMCW radars and their sensing performance requirements are both increasing continuously.

As the number of FMCW radars increases, so does the possibility and frequency of radar interference. Much literature has studied automotive FMCW radar interference and classified it into two different cases: crossing and parallel interference [4]. Crossing interference in FMCW radar amplifies baseband noise and reduces the signal-to-noise ratio; on the other hand, parallel interference generates a ghost target and produces a false alarm to the system.

To avoid or suppress interference, several studies have suggested orthogonal noise waveforms based on the phase retrieval method [5], frequency hopping for each chirp signal [6], or changing the start time of each chirp signal, such as pulse repetition time dithering [7]. Mitigation by signal processing is an option [8]; however, the best method to deal with interference is to sense the spectrum and avoid interference.

Some research has presented effective methods for real-time wideband spectrum sensing; however, these techniques have a few limitations that prevent adopting them for automotive FMCW radar problems, such as low signal power [9], large computation time [10–12], and additional hardware requirements [13–15].

This paper presents an effective method for recognizing the waveform of a periodic FMCW interferer by intentional interference to the victim system. The adaptive configuration of the victim radar system monitors and analyzes interference with minimum signal processing. The proposed method first estimates the bandwidth, chirp interval, frame interval, slope, and relative time difference of the interference waveform with a commercial off-the-shelf (COTS) radar system.

This paper is organized as follows. Section Ⅱ describes the principle of the proposed method. Section Ⅲ presents the experimental results and analysis, and Section Ⅳ concludes the paper.

## II. METHODOLOGY

## 1. FMCW Radar Principles and Interferences

FMCW radar is a radar system that uses a linear frequencymodulated signal to measure the range and velocity of the target. The reflected signal from the target is received by the antenna and mixed with a transmitted signal replica, generating a new signal called a beat or intermediate frequency (IF) signal, as shown in Fig. 1. Range, Doppler, and angle processing can be performed with the beat signal, as described in [16].

The received signal power from the target reflection $P _ { r }$ can be estimated using Eq. (1):

$$
\begin{array} { r } { P _ { r } = P _ { t x } + G _ { t x } + G _ { r x } + \sigma - 1 0 \mathrm { l o g } 1 0 \Big ( \frac { ( 4 \pi ) ^ { 3 } R ^ { 4 } } { \lambda ^ { 2 } } \Big ) , } \end{array}\tag{1}
$$

$P _ { t x }$ is the transmitted signal power, $G _ { t x }$ and $G _ { r x }$ are the gains of the transmitter and receiver antennas, ?? is the radar cross section of the target, ?? is the wavelength of the center frequency of the FMCW signal, and ?? is the distance between the radar and the target.

The interference signal is received directly from the interferer radar in a one-way manner:

$$
\begin{array} { r } { P _ { I } = P _ { t x _ { I } } + G _ { I } + G _ { r x } - 1 0 \mathrm { l } 0 \mathrm { g } 1 0 \Big ( \frac { 4 \pi R } { \lambda } \Big ) ^ { 2 } , } \end{array}\tag{2}
$$

$P _ { t x _ { I } }$ and $G _ { I }$ are the transmitted power and antenna gain of the interferer, respectively.

Since the interfering signal propagates in one direction, the power level of the interfering signal may be higher than that of the signal reflected by the target [17]. When crossing type interference occurs, the amplitude of the analog-to-digital converter (ADC) output increases dramatically and increases the noise floor in the frequency domain. On the other hand, parallel interference rarely occurs in real situations, since the interference signal should be allocated within the IF bandwidth of the victim radar [18].

In this paper, focusing on crossing-type FMCW interference, we propose a method for recognizing and avoiding the periodic waveform of the interference signal.

## 2. Proposed Method

The proposed method estimates the interfering FMCW radar parameters by creating intentional interference from adaptive waveform reconfiguration. Intentional interference does not affect other FMCW radars due to the transmitter’s high attenuation. To avoid interference, the victim radar must be aware of the bandwidth, center frequency, and slope of the FMCW interfering signal. Assuming the interferer transmits an FMCW waveform without dithering techniques, the victim radar can estimate the chirp interval, frequency bandwidth, and slope by configuring different waveforms.

Fig. 2 shows the procedure of the proposed method, comprising six different steps. The first step is to detect crossing interference. Detection is performed by comparing the amplitude of the ADC output with the threshold from the cell averaging constant false alarm rate (CA-CFAR) algorithm. After the interference detection, the process of estimating the waveform parameter begins. Three estimation sequences for the chirp interval, bandwidth, and slope of the interference signal are presented in the following subsections and in Fig. 3.

![](images/bbccbb2c5df7e01d4fd44568d970d059f5c4053a80cfbd8785e10a35a9c28b6e.jpg)  
(a)

![](images/7c34c7af35e8614027cc5c698310bb31f516693dc4ad3a39a6b3ede18570b63b.jpg)  
(b)  
Fig. 1. Principle of FMCW radar: (a) basic FMCW radar system architecture and (b) FMCW radar Tx/Rx signals.

![](images/39a989e97674a3f9336bc6ee091746496c07eb2fbafa2ac8be038db95859091b.jpg)  
Fig. 2. Processing steps of the proposed method.

![](images/71b25d407fe3fb6a20b2f8ca697f19ce4dab7bd6a7dc9e0ea2a578a499886bad.jpg)  
Fig. 3. Time-frequency diagram of interference and victim FMCW signals. Each estimation requires a victim FMCW waveform update to enforce interference to the victim radar. The victim radar sets its parameter in the following order: slope as zero for the interferer interval, various start frequencies for the interferer bandwidth, and an arbitrary slope for the interferer slope.

## 2.1 Chirp interval estimation

To estimate the interval between successive chirps of the interferer FMCW radar, the victim radar must receive multiple interferences in one chirp signal. Therefore, the victim radar is configured with a maximum chirp time, and the frequency slope is set to zero, like continuous-wave radar. From the ADC sample indexes of multiple interferences, the chirp interval can be estimated by multiplying the sampling time and the difference between the sample indexes. The estimated chirp interval can be divided into chirp time and idle time, which requires accurate bandwidth and slope estimation.

![](images/6fb2c9d0b38af513a43e49c6fa9eb6301fece6d85c686f3b57c6c02cc833f261.jpg)  
(a)

## 2.2 Bandwidth estimation

The bandwidth of the interfering signal can be estimated by changing the frequency of the zero-slope waveform used in the chirp interval estimation. However, the length of the waveform is shortened to have at least one interference in one chirp signal. In this study, we set the chirp time as 1.5 times the chirp interval estimated in the previous step.

An example waveform for bandwidth estimation is depicted in Fig. 4(a). The number of frequency steps is initially set to 12 MHz and 200 MHz separation. This is because the radar system (AWR2243 and AWR2944) supports four different waveform configurations during operation, and each configuration provides a maximum 450 MHz frequency variability for each chirp signal.

Theoretically, the bandwidth of an interfering signal can be estimated accurately to the order of a few kHz over several iterations only if the interfering signal is continuously received. However, in a real situation, the interferer and victim vehicle move independently within seconds. Therefore, in this study, two-step bandwidth estimation is considered for fast estimation, as shown in Fig. 4(a) and 4(b). The second estimation estimates the bandwidth with reduced frequency separations, which is determined by the result of the first stage.

## 2.3 Slope estimation

The theoretical FMCW radar system transmits the chirp signal continuously without any idle time so that the slope is the same as the total bandwidth divided by the chirp interval. However, in practice, FMCW waveforms have some idle times between consecutive chirps for signal quality, data transfer, or other purposes. If the interference FMCW signal ramps fast and has a sufficiently long idle time, the spectrum can be shared with other radar systems.

Like the previous step, the proposed method exploits the frequency and time differences of multiple interference incidents in one chirp. However, in this step, the slope of the adaptive waveform should be selected in the following range to estimate the slope of the interference signal. The minimum value of the slope of the victim radar $S _ { m i n }$ is derived from the sampling time of the victim radar, as described in Eq. (3).

![](images/18ad7cd5ebc5c6702008f0503b9911e5448940093a528627f4cfa88cc503278d.jpg)  
(b)  
Fig. 4. (a) Time–frequency FMCW waveform diagram of the initial bandwidth estimation. (b) Based on the result of (a), the estimation frequency range is adaptively decreased.

Compared to the chirp interval estimation, the slope estimation relies on an additional time delay from the increased frequency. If this time delay is shorter than the sampling time of the victim ADC, then the slope estimation fails.

$$
\begin{array} { r } { S _ { m i n } = \frac { B _ { I } t _ { s } } { t _ { I } ( t _ { I } + t _ { s } ) } , } \end{array}\tag{3}
$$

$B _ { I }$ is the bandwidth of the interference signal, $t _ { I }$ is the estimated chirp interval, and $t _ { s }$ is the sample time.

The maximum value of the slope is based on the fact that multiple interferences must occur during one victim chirp. This causes the bandwidth limitation of the listening waveform to be less than or equal to the interference bandwidth. Considering that the total time of the listening waveform is the same as twice the chirp interval, $t _ { I { \mathrm { : } } }$ , then the maximum slope can be expressed in an equation:

$$
\begin{array} { r } { S _ { m a x } = \frac { B _ { I } } { 2 t _ { I } } . } \end{array}\tag{4}
$$

After selecting an arbitrary slope as $S _ { v }$ in the valid range, the slope of the interference signal can be obtained with the following closed-form expression:

$$
\begin{array} { r } { { S _ { I } } = \frac { { N _ { s , 2 } } \times { S _ { v } } \times { t _ { s } } } { { { t _ { s } } \left( { N _ { s , 2 } } - { N _ { s , 1 } } \right) } } = \frac { { N _ { s , 2 } } \times { S _ { v } } } { { N _ { s , 2 } } - { N _ { s , 1 } } } , } \end{array}\tag{5}
$$

$N _ { s , 2 }$ and $N _ { s , 1 }$ are the sample distance from the slope and the chirp interval estimation.

## III. EXPERIMENTAL SETUP AND RESULTS

## 1. Experimental Setup

## 1.1 FMCW radar setup

The proposed method was demonstrated with Texas Instruments’ automotive mmWave FMCW radar. The interfering radar was an AWR2944 evaluation board, and the victim was a cascaded AWR2243 board. Both operate in the same frequency bandwidth (i.e., 76–81 GHz). The proposed estimation method was implemented using built-in multiple profile and parameter variation functions. The validity of the proposed estimation was tested in an indoor laboratory environment, as shown in Fig. 5(a). Fig. 5(b) shows the experiment performed in an outdoor environment with a vehicle to assess the practicality of the proposed method.

![](images/cd4dea9f06c7df44b823964f8af3e5140e7abe1f2377501886a5326abf9f9370.jpg)  
(a)

The number of samples between high values implies periodicity, so the estimation accuracy is highly dependent on the sampling frequency of the victim radar. A higher sampling frequency may be required for accurate estimation, but the proposed method is also based on intentional interference with a long chirp time. Therefore, higher accuracy requires many samples and increases memory budgets. In this experiment, the sampling frequency of the victim radar was set to 2.5 Msps, considering the performance of the radar chipset.

## 1.2 Test cases

The estimation performance of the proposed method was tested in three different cases to prove the efficiency and limitations of the proposed method. Test case A provided the basic performance of the proposed method, and cases B and C were designed to test the limitations of the proposed method. The waveform parameters of case A were selected as a low slope, and a long chirp interval, which are highly likely to interfere with other FMCW radars.

Automotive radar interference changes quickly because both the interferer and victim radars are moving. Therefore, the total estimation time should be fast enough to avoid the interference signal. To test the total estimation time, a longer frame interval of the interferer radar was presented in case B. On the other hand, in case C, a higher slope and larger bandwidth led to an increased probability of crossing interference. The waveform parameters of the three test cases are summarized in Table 1.

![](images/ae44f218c92bcb6ef64879a27f74d378fd45809ed6038e1cc44a161dc93b25b1.jpg)  
(b)  
Fig. 5. (a) Interferer (AWR2944) and victim (AWR2243) radars and the indoor laboratory experiment’s environment. (b) Outdoor environment with increased distance and a stationary vehicle.

Table 1. Interference waveforms and estimation results in indoor and outdoor environments
<table><tr><td rowspan="2">Parameter</td><td colspan="3">Case A (standard)</td><td colspan="3">Case B (low FPS)</td><td colspan="3">Case C (high slope)</td></tr><tr><td>Interference Estimation Estimation waveform</td><td>in indoor</td><td>in outdoor</td><td>waveform</td><td>in indoor</td><td>Interference Estimation Estimation in outdoor</td><td>waveform</td><td>in indoor</td><td>Interference Estimation Estimation in outdoor</td></tr><tr><td>Start frequency (GHz)</td><td>77.5</td><td>77.5</td><td>77.5</td><td>77.5</td><td>77.5</td><td>77.5</td><td>77.5</td><td>77.5</td><td>77.5</td></tr><tr><td>Bandwidth (MHz)</td><td>540</td><td>580</td><td>510</td><td>540</td><td>510</td><td>510</td><td>1,350</td><td>1,305</td><td>1,305</td></tr><tr><td>Frequency slope (MHz/μs)</td><td>12</td><td>11.85</td><td>11.85</td><td>12</td><td>11.76</td><td>11.76</td><td>30</td><td>29.4</td><td>29.4</td></tr><tr><td>Idle time (μs)</td><td>10</td><td>54.8</td><td>54.8</td><td>10</td><td>54.8</td><td>54.8</td><td>10</td><td>54.8</td><td>54.8</td></tr><tr><td>Chirp time (μs)</td><td>45</td><td></td><td></td><td>45</td><td></td><td></td><td>45</td><td></td><td></td></tr><tr><td>Frame interval (ms)</td><td></td><td>100 62.56</td><td>53.93</td><td></td><td>200</td><td></td><td></td><td>100</td><td></td></tr><tr><td>Average of peak value (log)</td><td></td><td>5.4</td><td>53.08</td><td></td><td>64.34 3.91</td><td>47.08 53.11</td><td></td><td>62.28</td><td>50.95</td></tr><tr><td>Variation of peak value</td><td>一</td><td>0.9</td><td>0.9</td><td>一</td><td>2.1</td><td>2.1</td><td></td><td>13.68</td><td>63.92</td></tr><tr><td>Total estimation time (s)</td><td></td><td></td><td></td><td></td><td>2.65</td><td></td><td></td><td>0.9</td><td>0.9</td></tr><tr><td>Average estimation error (%)</td><td></td><td>2.85</td><td>2.39</td><td></td><td></td><td>2.65</td><td></td><td>1.9</td><td>1.9</td></tr></table>

FPS = frame per second.

## 2. Results Analysis

Fig. 6 shows the results of the proposed method from each estimation step for test case A in an indoor environment. The chirp interval, bandwidth, and slope estimation results are presented with the amplitude of the ADC samples from the adaptive waveforms. Using Eq. (5), the chirp interval is calculated as 54.8 μs, and the slope is obtained as 11.85 MHz/μs. The bandwidth is estimated as 580 MHz with 40 MHz error with a total 0.9-second bandwidth estimation time.

![](images/2ec25e1f3f62b1f3bfdb9281da3ad9d6b98b53b58acee655bfe694286a3815ce.jpg)  
(a)

![](images/79d99639cb674521ee1860ed931104eb97b898248433d1e796b2a1ccb607c03f.jpg)  
(c)

The total estimation results for the three test cases are summarized in Table 1. The results indicate that the proposed method effectively estimates the waveform with less than 3% error. The highest error is from the bandwidth estimation; however, the estimation provides the upper bound of the bandwidth, which is sufficient for interference avoidance.

(b)  
![](images/d2fdd65984c70afd5b356450cacb72ff5b2a0b191dfd17964f1a33d91bbca097.jpg)  
Fig. 6. Results of the proposed method from test case A: (a) the interferer chirp time is derived from the same sample distance of the periodic interference, (b) the interferer bandwidth is analyzed by checking the interference for each frequency, and (c) the interferer slope is estimated from the increased sample distance from the known victim slope.

When the frame interval of the interferer radar is increased, as in case B, the total estimation time increases to 2.1 seconds, while the errors do not increase. Test case C presented a higher bandwidth error compared to the other cases because the estimation frequency steps were larger than in the other cases.

The total estimation time for each case was measured as the time to interference occurrence, which triggered the next estimation step. In case A, the chirp interval estimation time was 153 ms, the bandwidth was 753 ms, and the slope was 6 ms. Bandwidth estimation takes the longest time because the estimation requires multiple start frequency changes, as presented in Fig. 3.

In an outdoor environment where the distance increases, not only does the received power decrease due to additional path loss, but the variance also significantly increases, as shown in Fig. 7(a) and 7(b). This difference occurs due to constraints in radar signal detection caused by environmental factors. These fluctuations can lead to errors if interference signals are not detected, but this can be redeemed by improving the detection CFAR algorithm.

The outdoor experiment confirmed that in the proposed method, the amplitude of the received signal only serves a detection role. Therefore, if only detection is performed, the algorithm’s performance is unaffected by the amplitude of the received signal.

The proposed method presents high estimation accuracy without any additional hardware, but it has a limitation that relies on the occurrence of interference, which is not always guaranteed. Also, the proposed method assumes that the interference is periodic; however, the interferer radar may use multiple waveforms to avoid interference. However, the proposed method can be utilized for wireless synchronization or extended spectrum sensing using FMCW radar.

## IV. CONCLUSION

This paper presented a method based on intentional local interference to estimate the interference waveform of FMCW radar. The proposed method detects interference and estimates the waveform of the interference signal through adaptive configuration of the victim radar and minimal signal processing. After estimation, the victim radar can configure a waveform to avoid the detected interference signal.

The proposed method was demonstrated with COTS FMCW radars in three different test cases. The proposed method does not require any additional hardware and can be implemented in an existing radar system with a simple algorithm.

The periodic interference signal parameters were estimated with a low error rate of 2.85% and a low sampling rate of 2.5 Msps in 0.9 seconds. The most time-consuming and inaccurate estimation was bandwidth estimation in all three cases, but this could be improved with a frequency selection strategy or a multiple independent receiver system. The average error rate of the proposed method is 2.85%, which is acceptable information for designing the waveform of the victim radar to avoid the interference signal.

In an outdoor environment, the estimation error and time do not exhibit substantial deviation compared to an indoor experiment but the average and the variation of the peak amplitude markedly deviate. However, if a peak amplitude by interference is detectable, the performance of the algorithm is hardly degraded.

This intentional interference technique can be used not only for interference avoidance but also for estimating the relative parallax of a distributed radar system for synchronization. In future, this estimation method will be expanded to interference signals with timing dithering and multiple configuration modes. In addition, the total estimation time will be decreased by improving the processing algorithm.

![](images/4f6fd5bc8952bc7b2ae73c1b00f91a32045d4ded361c614294d1f1f62d854503.jpg)  
(a)

![](images/b2699ee655d76f4587a8b2dc97dd83164b37811b8c895d7e66a72c1c84371787.jpg)  
(b)  
Fig. 7. Time domain diagram on a log scale: (a) consistent peaks were observed in the indoor experiment and (b) the outdoor experiment revealed smaller peaks compared to (a).

This work was supported by the Research Fund of Chungnam National University.

## REFERENCES

[1] C. Waldschmidt, J. Hasch, and W. Menzel, "Automotive radar: from first efforts to future systems," IEEE Journal of Microwaves, vol. 1, no. 1, pp. 135-148, 2021. https://doi.org/ 10.1109/JMW.2020.3033616

[2] G. M. Brooker, "Understanding millimetre wave FMCW radars," in Proceedings of the 1st International Conference on Sensing Technology, Palmerston North, New Zealand, 2005, pp. 152-157.

[3] S. Heuel, "Automotive radar technology, market and test requirements," Rohde & Schwarz, Munich, Germany, 2018.

[4] M. Goppelt, H. L. Blocher, and W. Menzel, "Automotive radar–investigation of mutual interference mechanisms," Advances in Radio Science, vol. 8, pp. 55-60, 2010. https:// doi.org/10.5194/ars-8-55-2010

[5] Z. Xu and Q. Shi, "Interference mitigation for automotive radar using orthogonal noise waveforms," IEEE Geoscience and Remote Sensing Letters, vol. 15, no. 1, pp. 137-141, 2018. https://doi.org/10.1109/LGRS.2017.2777962

[6] T. N. Luo, C. H. E. Wu, and Y. J. E. Chen, "A 77-GHz CMOS automotive radar transceiver with anti-interference function," IEEE Transactions on Circuits and Systems I: Regular Papers, vol. 60, no. 12, pp. 3247-3255, 2013. https:// doi.org/10.1109/TCSI.2013.2265974

[7] M. Alhumaidi and M. Wintermantel, "Interference avoidance and mitigation in automotive radar," in Proceedings of 2020 17th European Radar Conference (EuRAD), Utrecht, Netherlands, 2021, pp. 172-175. https://doi.org/10.1109/ EuRAD48048.2021.00053

[8] F. Uysal and S. Sanka, "Mitigation of automotive radar interference," in Proceedings of 2018 IEEE Radar Conference (RadarConf18), Oklahoma City, OK, USA, 2018, pp. 405-410. https://doi.org/10.1109/RADAR.2018.8378593

[9] M. LaManna, P. Monsurro, P. Tommasino, and A. Trifiletti, "Spectrum estimation for cognitive radar," in Proceedings of 2015

European Radar Conference (EuRAD), Paris, France, 2015, pp. 193-196. https://doi.org/10.1109/EuRAD.2015.7346270

[10] Z. Tian and G. B. Giannakis, "Compressed sensing for wideband cognitive radios," in Proceedings of 2007 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Honolulu, HI, USA, 2017, pp. 1357- 1360. https://doi.org/10.1109/ICASSP.2007.367330

[11] P. Stinco, M. Greco, F. Gini, and M. La Manna, "Compressed spectrum sensing in cognitive radar systems," in Proceedings of 2014 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Florence, Italy, 2014, pp. 81-85. https://doi.org/10.1109/ICASSP.2014.6853562

[12] J. A. Tropp, J. N. Laska, M. F. Duarte, J. K. Romberg, and R. G. Baraniuk, "Beyond Nyquist: efficient sampling of sparse bandlimited signals," IEEE Transactions on Information Theory, vol. 56, no. 1, pp. 520-544, 2010. https:// doi.org/10.1109/TIT.2009.2034811

[13] M. Mishali, A. Elron, and Y. C. Eldar, "Sub-Nyquist processing with the modulated wideband converter," in Proceedings of 2010 IEEE International Conference on Acoustics, Speech and Signal Processing, Dallas, TX, USA, 2010, pp. 3626-3629. https://doi.org/10.1109/ICASSP.2010.5495911

[14] M. Mishali and Y. C. Eldar, "Sub-Nyquist sampling," IEEE Signal Processing Magazine, vol. 28, no. 6, pp. 98-124, 2011. https://doi.org/10.1109/MSP.2011.942308

[15] G. Hakobyan, M. Fink, A. Soyolyn, N. Mansour, and D. Dahlhaus, "Sweep-based spectrum sensing method for interferenceaware cognitive automotive radar," in Proceedings of 2020 IEEE Radar Conference (RadarConf20), Florence, Italy, 2020, pp. 1-6. https://doi.org/10.1109/RadarConf2043947.2020.9266361

[16] A. Meta, "Signal processing of FMCW synthetic aperture radar data," Ph.D. dissertation, Delft University of Technology, Delft, Netherlands, 2006.

[17] Z. Yang and A. Mani, "Interference mitigation for AWR/ IWR devices," Texas Instruments Inc., Dallax, TX, USA, 2020.

[18] S. Rao and A. V. Mani, "Interference characterization in FMCW radars," in Proceedings of 2020 IEEE Radar Conference (RadarConf20), Florence, Italy, 2020, pp. 1-6. https:// doi.org/10.1109/RadarConf2043947.2020.9266283

![](images/14fa4d8f8fc88961132b5c4520dade1e92ce4d28101554b391796fa787b166dc.jpg)  
received a B.S. degree and an M.S degree in radio and information communications engineering from Chungnam National University, Daejeon, Republic of Korea, in 2022, 2024. His current research interests include focusing on research that includes FMCW radar interference and radar signal processing.

## Hyungwoo Kim https://orcid.org/0009-0004-2634-516X

![](images/3b40b18878abcc49653d9f8fc84a1e3f75c4d1418b25942e04e4bdc673c021c4.jpg)

received a B.S. degree in radio and information communications engineering from Chungnam National University, Daejeon, Republic of Korea, in 2023. Currently, he is pursuing an M.S. degree while focusing on research on radar signal processing and precise beamforming with radar.

Byungkwan Kim https://orcid.org/0000-0002- 2414-1292

![](images/0d13048fd76a62cc8f548bd6736820e2ecee4a697a3c450cceb2933e49e98397.jpg)

received a B.S. degree in information and communication engineering and M.S. and Ph.D. degrees in electrical engineering from the Korea Advanced Institute of Science and Technology (KAIST), Daejeon, Republic of Korea, in 2010, 2012, and 2017, respectively. From 2017 to February 2020, he was a senior researcher at the Samsung Advanced Institute of Technology, Suwon. He is currently an

assistant professor in the Department of Radio and Information Communications Engineering, Chungnam National University, Daejeon, Republic of Korea. His current research interests include mmWave radar system design and radar signal processing with machine learning.