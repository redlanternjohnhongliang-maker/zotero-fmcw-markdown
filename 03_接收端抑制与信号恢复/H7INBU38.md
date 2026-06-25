# An Anti-collision Automotive FMCW Radar Using Time-domain Interference Detection and Suppression

Takuya Nozawa† Yuya Makino† Nobuyuki Takaya† Masahiro Umehira† Shigeki Takeda† Xiaoyan Wang† Hiroshi Kuroda‡

†Graduate School of Science and Engineering

‡Hitachi Automotive Systems, Ltd.

Ibaraki University 4-12-1 Nakanarusawa, Hitachi,

2520 Takaba, Hitachinaka,

Ibaraki 316-8511 Japan

Ibaraki 312-8503 Japan

Email: †{16nm668n, 13t8045h, 13t8053n, masahiro.umehira.dr, shigeki.takeda.tmkyo, xiaoyan.wang.shawn} @vc.ibaraki.ac.jp ‡hiroshi.kuroda.gy@hitachi-automotive.co.jp

Keywords: Automotive Radar, Frequency Modulated Continuous Wave (FMCW), Interference Suppression, Time-Domain

## Abstract

As the number of automotive radars in vehicles will rapidly increase for self-driving car applications in near future, mutual interference between radars would result in frequent false and miss detection of the target due to dense deployment of radars. This paper focuses on interference between frequency modulated continuous wave (FMCW) radars, and proposes a time domain interference detection and suppression scheme to achieve anti-collision capability. We conducted real-world experiments by using 77.5GHz FMCW radar to validate the proposed scheme. The experimental results show that the proposed scheme can achieve almost the same target detection rate as in interference-free environment, even in interference environment.

## 1 Introduction

The autonomous vehicle has been getting a great deal of interests and considerable research investment recently. A self-driving car must be able to see what is in front, behind and both sides, in other words, it needs a 360 degree view, just like a human driver. Compared to laser radar, infrared sensor, camera, etc., FMCW radar is one of the most attractive solutions, since it can measure the target’s relative distance and speed simultaneously, and has the advantage of lower cost and higher performance in dark or harsh environments. As the number of vehicles equipped with automotive radars is expected to increase in near future, mutual interference has become a crucial issue [1], [2], [3]. Specifically, it leads to the generation of ghost target, as well as the signal to noise ratio (SNR) degradation and thus the target detection failure. To mitigate the inter-radar interference, various techniques have been proposed for automotive radar systems [4], [5]. An interference suppression scheme using clipping and weighted-envelope normalization was proposed in [4]. However, the effect of phase noise on FMCW radar is not considered, which needs to be pre-processed before interference detection. Another anti-interference technique using randomized chirp rate and frequency range of FMCW radar was proposed in [5], which can avoid ghost target detection however still suffers from significant SNR degradation due to inter-radar interference.

This paper proposes a time-domain interference detection and suppression scheme for FMCW radar systems. Specifically, phase noise effect is firstly removed thus interference detection can be made by using a simple threshold based approach. Furthermore, time domain interference suppression is applied to improve SNR in interference environment. The proposed scheme postprocesses the mixer output signal, and thus could be used in any existing FMCW radar system by adding signal processing software. To validate the performance improvement of the proposed scheme, we conducted extensive experiments by using 77.5 GHz FMCW radars. The results show that the proposed scheme could improve the target detection rate in interference environment by approximately 30% compared to the baseline scheme.

## 2 Effect of inter-FMCW radar interference

In severe inter-FMCW radar interference environment, reflected signal from the target and the radar signal from other vehicles are received simultaneously, which results in false and miss detection of the target. Based on the relationship of the chirp slopes between the transmitted signal and interference signal, the FMCW radar interference could be classified into two categories, i.e., narrow band interference and wide band interference [2].

In the narrow band interference case, the interference comes with a small-time delay such that the chirp of the interference is in-phase with the chirp of the desired signal. As shown in Fig. 1, all the interference beat frequency leaks into the pass-band region of low pass filter (LPF) in FMCW radar. This narrow band interference causes ghost target, i.e. false detection of the target, and is hard to remove. However, the probability of this narrow interference is extremely low [1], and thus we do not tackle it in this paper and this problem is remained for future study.

In the wide band interference case, the frequency of desired signal increases while the one of interference signal decreases, or vice versa. As illustrated in Fig. 2, the beat frequency lies in both in-band and out-of-band regions. In this case, the outof-band beat frequency can be cut by LPF, and the remaining interference leaks into pass-band of LPF and results in impulse-like interference signal. Usually, the received level of the interfering radar signal is much higher than the reflected signal from the target when the interferer is located near the desired FMCW radar. This interference signal can be regarded as an impulse signal in time domain. The received signal of FMCW radar is converted into frequency domain signal by FFT (Fast Fourier Transform) to detect the peak frequency, i.e. distance from the target. As impulse is equivalent to white noise in frequency domain, the wide band interference leads to miss detection of the target due to the increase of noise level in frequency domain.

## 3 Proposed time-domain interference detection and suppression method

In this section, we present the proposed FMCW radar interference suppression method. Figure 3 shows the block diagram of the proposed FMCW radar system. Principle of the proposed interference suppression method is to detect the timing of the impulse noise caused by the interfering radar signal and to suppress it in time domain before FFT processing in the FMCW radar. However, we found that DC component drift appears at the mixer output of FMCW radar because of large phase noise of the high frequency oscillator used in FMCW radar. This DC component drift should be removed before setting the threshold for impulse noise detection. Therefore, firstly, we propose a phase noise suppression method to remove the DC component drift at the mixer output. Then we propose a time domain interference suppression method which detects the position of the impulse noise caused by the interference and suppresses it in the mixer output signals. Finally, we conduct FFT and detect the target from the beat frequency peak power in frequency domain.

As shown in Fig. 3, we assume that triangle chirp signal is transmitted from VCO and the received signal reflected from the target is mixed with the output of VCO to obtain the beat signals. Low pass filtering and A/D conversion is performed, then all the signal processing i.e., removing DC component drift, interference pulse noise detection and suppression, FFT and target detection, is performed in the digital signal processor of the FMCW radar.

## 3.1 Phase noise suppression method

Based on our experiment (details are presented in Section 4), we found that the DC component of the mixer output varies in time due to large phase noise in a millimetre wave oscillator using PLL (Phase Locked Loop) technique. An example of actual measured mixer output is illustrated as the red line in Fig. 4 (a), when the target signal and the interfering signal are simultaneously received. Impulse noise caused by the interfering radar appears around the time of 0.0294(s) and the received level of the beat signals is much lower than the impulse noise as well as DC drift component. Therefore, DC component drift needs to be removed first to set the threshold to detect the impulse signal due to interference.

To solve this problem, we propose a phase noise suppression method which removes the DC component from the mixer output by using LPF, and subtracts the DC component from the mixer output signal. Here, the LPF is implemented by using simple moving average. An example of the mixer outputs after removing phase noise by the proposed method is shown as the blue line in Fig. 4(a) and (b). Peak-to –peak amplitude of the desired beat signals is as small as 40 while that of impulse noise is as large as 300, i.e. about 20dB higher. Amplitude of DC component drift is as large as 5000 and is much higher than the desired beat signals and the impulse noise. By using the proposed method, it is obvious that the phase noise is perfectly removed and the detection and suppression of the interference pulse becomes possible by setting an appropriate threshold.

![](images/d536d6efb85e081b6073b4de6f5534baa293545f31f31b54d4df1bda48fec3d0.jpg)

Fig. 1. Narrow band interference in FMCW radar.  
![](images/5d0c2819d7f14c1784c0084a6c96290e2b658f610481054743700c4c759f638c.jpg)  
Fig. 2. Wide band interference in FMCW radar.

![](images/7708f4c5bf16eef6b056187373b90b1994e17ad4b85256337e957a74ac1d2617.jpg)  
Fig. 3. Block diagram of the proposed FMCW radar system

![](images/20cb481301bdd7a9599ad375b57cbd0306c2bf0d84d545779216479ee76178cb.jpg)

(a) Mixer output  
![](images/993cc1461f0a244b555b1d0799a409bcfa0453f91c9743c5fe747ac9e7906579.jpg)  
(b) Enlarged view with phase noise suppression  
Fig. 4. Mixer outputs with phase noise suppression

It is necessary to optimize the number of moving average in the proposed method. As larger moving average number results in lower power level in low frequency region and smaller moving average number results in higher power level in low frequency region in its power spectrum, the variation caused by phase noise should be minimized. Therefore, we performed parameter optimization by using actual measured mixer output to find the number of moving average processing which minimizes the variation of power spectrum after FFT processing. Figure 5 shows FFT signal variation according to the number of moving average. As shown in Fig. 5, number of moving average of 32 gives minimized spectrum variation. Therefore, number of moving average of 32 is used in our FMCW radar experiments. Note that the optimized number of moving average might be different in another FMCW radar.

## 3.2 Interference detection and suppression method

After DC components drift caused by the phase noise is removed, impulse noise caused by the interfering FMCW radar is detected and suppressed in the proposed scheme. This paper proposes a time-domain interference detection and suppression method by detecting the interference impulse signal position and suppressing it using window function in time domain. The detailed algorithm is described as follows.

## STEP1: Received signal level detection

Calculate the averaged absolute value, $m _ { a \nu e }$ of the mixer output, m(n) $( n { = } 1 { \sim } N )$ after suppressing DC component drift and $m _ { a \nu e }$ is given as:

$$
m _ { _ { a v e } } = 1 / N \sum _ { n = 1 } ^ { N } \lvert m ( n ) \rvert \cdot\tag{1}
$$

where N is the number of mixer output signals sampled by A/D converter. As the received signal level can vary according to the distance from the target, we need a reference level to set the threshold for impulse noise detection. This method is simple but effective to calculate the received signal level for threshold setting to detect impulse noise caused by interfering radar.

STEP2: Threshold setting for impulse noise detection Set the threshold $m _ { \mathrm { t h r e s h o l d } }$ by the following equation (2):

$$
m _ { t h r e s h o l d } = m _ { a \nu e } \times k ,\tag{2}
$$

![](images/a8d2178cc96c49f0c3d9b8a4e5362cc519109c32d1be03ef64632cca969d2f8f.jpg)  
Fig. 5. Spectrum variation according to number of moving average.

where k is threshold parameter. The threshold, m is used to detect impulse noise where reference amplitude is $m _ { \mathrm { a v e } }$ given by equation (1). There is a trade-off to set the parameter, k. Specifically, small k leads to false-detection of interference impulse noise signal, thus the desired beat signal is also suppressed and miss-detection rate increases since the desired signal can be recognized as interference impulse signal. Meanwhile, large k leads to miss-detection of interference impulse noise signal, thus noise level cannot be suppressed.

## STEP 3: Impulse noise detection

Find the position of impulse noise, $N _ { \mathrm { i } }$ where the level of impulse noise signal is higher than m , and calculate a new signal, $m _ { \mathrm { { s u p } } } ( n )$ that is weighted by window function, w(n) as follows:

$$
m _ { \mathrm { s u p } } ( n ) = m ( n ) \times w ( n ) .\tag{3}
$$

Though there are many alternatives for $w ( n )$ , we employ raised cosine weighting function, w<sub>R</sub>(n) and zero weighting function, w (n), which are given below:

$$
w _ { R } ( N _ { i } ) = \left\{ \begin{array} { c c } { { ( 1 - \cos ( 2 \pi ( n - N _ { i } / M ) ) / 2 } } & { { ( \mid n - N _ { i } \mid < M / 2 ) } } \\ { { 1 } } & { { ( e l s e ) } } \end{array} \right.\tag{4}
$$

$$
w _ { 0 } ( N _ { i } ) = 0 .\tag{5}
$$

Raised cosine function has a design parameter, M, which is the width of raised cosine function. M is related to the interference pulse signal duration. Large M leads to beat signal suppression resulting in decrease of desired signal power, and small M leads to less suppression of impulse noise signal resulting in increase of noise power.

## 3.3 Design of threshold parameter, k

Threshold parameter, k is used for impulse noise detection and its design is a trade-off issue as described before. Figure 6 shows simulation results of signal power at the beat frequency of the target and averaged noise power according to the parameter, k where the experimental data of the FMCW radar is used. As shown here, the signal power drastically decreases when k is smaller than 5 since the desired beat frequency signal can be effectively suppressed. On the other hand, when k is larger than 20, the noise power level increases since impulse noise is not suppressed. Therefore, the threshold

![](images/4bd6c6fdd62e2b1acb6cb869c2ffbf647abf8a0fca5f32e2d76631f00dc417b9.jpg)

Fig. 6. Signal and noise power level according to threshold parameter, k.  
![](images/e7e0d2d8f2be93dde8a2af122604219afb1c2f6f74e8ed7f435d0fb274fd7cf4.jpg)  
Fig. 7. Signal power level according to raised cosine window width, M.

parameter, k should be set in the range from 5 to 20. Considering the margin of threshold level, the parameter, k is set at 10 in this paper.

## 3.4 Design of window width, M

As shown in equation (4), the width of raised cosine function, M, is a design parameter. M is related to the interference pulse signal width. Large M can remove relevant impulse noise caused by the interfering radar, but also reduce desired signal power. Figure 7 shows signal power according to raised cosine window width, M. As a design trade-off, M=32 is chosen since no significant decrease of signal power is observed if M is less than or equal to 32.

## 4 Performance evaluation of the proposed anticollision FMCW radar

The proposed anti-collision FMCW radar is evaluated by real-world experiments to demonstrate the anti-collision capability by suppressing the interference impulse noise in time domain. We used two FMCW radars as the observing

radar and the interfering radar and both of them have the same parameters such as chirp rate and center frequency. We used a reflector target which has the same RCS (Radar Cross Section) of a mid-size car. Figure 8 shows the experimental setup where distance between the observing radar and target is set to 15 and 25 [m], and that between the observing radar and the interference radar is 5 [m]. Major parameters of the experimental FMCW radar are summarized in Table 1.

Table. 1. Major experiment parameters.
<table><tr><td>Parameter</td><td>value</td><td>unit</td></tr><tr><td>Sweep frequency Center frequency</td><td>560 76.5</td><td>MHz GHz</td></tr><tr><td>Sweep time Sampling rate</td><td>3</td><td>ms</td></tr><tr><td>FFT size</td><td>781.25</td><td>kHz</td></tr><tr><td>FFT window SNR threshold</td><td>2048 blackman</td><td></td></tr></table>

![](images/a0d2d2d4bf1511bf712092b5b3818c298b1ab82f3db77c6a9ae6cbd876ae5c0b.jpg)  
Fig. 8. Exprimental set-up.

![](images/f620f9d5886e465cfc096c93edd764bce664c8c9419966b0ce114abe2f40dec2.jpg)

(a) w/o interference suppression  
![](images/c2ddf4b71ea2046c0eba2677065833d177da42807abc3e70047310f41e3f6a9f.jpg)  
(b) with interference suppression

Fig. 9. Examples of mixer output without and with interference suppression.  
![](images/e9ca533fc1bbaf14b95338ac7127f23f24b09ed48caefa550d9fece51396e636.jpg)  
Fig. 10. Mixer output in frequency domain.

Figure 9 shows an example of mixer output without and with the proposed interference suppression method. We can observe that large interference impulse noise is successfully suppressed by the proposed method. Figure 10 shows the power spectrum of these two mixer signals in frequency domain. It is clear that the noise level is reduced by using the proposed method.

Figure 11 compares the target detection rate of FMCW radar without interference suppression in non-interference condition and interference condition as described above where 50 trials were conducted. It also compares the target detection rate of FMCW radar using the proposed interference suppression with raised cosine weighting function and zero weighting function in interference condition. As shown here, the proposed method improves the target detection rate from 0.5\~0.6 to 0.75\~0.8, which are almost the same as that in noninterference condition. No significant difference between raised cosine weighting function and zero weighting function was observed.

## 5 Conclusion

This paper proposed an anti-collision automotive FMCW radar using time-domain interference detection and suppression, which consists of a phase noise suppression method to remove the DC component, and an interference suppression method to detect and suppress the interference impulse signal in time domain. We conducted design optimization regarding the design parameters such as the number of moving average, threshold parameter, k, and window parameter, M. We also conducted extensive experiments and confirmed that the proposed method can improve the target detection rate by approximately 30% compared to the baseline scheme.

Future work includes further performance evaluation in multiple interference scenario since more interference radars around a car are expected in actual automotive scenarios.

## Acknowledgements

This research and development work was supported by the MIC/SCOPE # 175003004. The authors also appreciate continuous support for this work by Hitachi Automotive Systems, Ltd, Japan.

## References

[1] G.M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol.49, no.1, pp.170-181, 20007

[2] M. Goppelt, H.–L. Blöcher, W. Menzel, ”Automotive radar – investigation of mutual interference mechanisms”, Advances in Radio Science., vol.8, 2010-1, pp.55-61

[3] Li Mu, Tong Xiangqian, Shen Ming, Yin Jun, “Research on Key Technologies for Collision Avoidance Automotive Radar”, IEEE Intelligent Vehicles Symposium, June 2009, pp.233-236

[4] Jung-Hwan Choi, Han-Byul Lee, Jiwon Choi, Seong-Cheol Kim, “Mutual Interference Suppression Using Clipping and Weighted-Envelope Normalization for Automotive FMCW Radar Systems”, IEICE TRANS. COMMUN., vol.E99-B, No.1 2016-1, pp.280-287

[5] Tang-Nian Luo, Chi-Hung Evelyn Wu, and Yi-Jan Emery Chen, “A 77-GHz CMOS Automotive Radar Transceiver With Anti-Interference Function”, IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS., vol.80, No.12, 2013-12 pp.3247-3255.

![](images/33e5ff9cdca2c5b3f431c9862eb46811fe3d9bfcfcaacf2c30d953f8fe94389d.jpg)  
Fig. 11. Evaluated results of target detection rate