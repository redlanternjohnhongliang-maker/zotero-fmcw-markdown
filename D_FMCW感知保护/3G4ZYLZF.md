# Experimental Evaluation of Adaptive Beamforming for Automotive Radar Interference Suppression

Muhammad Rameez, Mattias Dahl and Mats I. Pettersson

Blekinge Institute of Technology, Karlshamn, 37441, Sweden

Abstract— Mutual interference between automotive radars can make it difficult to detect targets, especially the weaker ones, such as cyclists and pedestrians. In this paper, the interference suppression performance of a Least Mean Squares (LMS) algorithm-based adaptive beamformer is evaluated using measurements from a 77 GHz Frequency Modulated Continuous Wave (FMCW) radar in an outdoor environment. It is shown that the adaptive beamformer increases detection performance and that the interference is suppressed down to the noise floor of the radar in the Range-Doppler domain. In the paper, real baseband sampling and complex-baseband sampling (IQ) radar receivers are compared in the context of interference suppression. The measurements show that IQ receivers are more beneficial in the presence of interference.

## I. INTRODUCTION

The increase of radars in traffic and a limited frequency spectrum has led to a higher risk of mutual interference. A radar’s detection performance and accuracy of target parameter estimation are affected severely by interference from other Frequency Modulated Continuous Wave (FMCW) or Chirp Sequence (CS) radars [1]. Weaker targets in traffic, such as pedestrians and cyclists, may not be detected in the presence of interference [2]. Therefore, it is important to find techniques that can overcome the issue of mutual interference effectively, especially for safety purposes [3].

A Least Mean Squares (LMS) algorithm-based adaptive beamforming method for mutual interference mitigation between FMCW or CS automotive radars was presented in [4], and simulations were used to verify the proposed method. In this work, we validate this method with the help of radar measurements in an outdoor environment. We also show that the interference behaves differently in real and complex baseband (IQ) implementations of radar receivers. Due to this difference, receiver architecture plays an important role in a radar system’s detection performance, especially when spatial domain methods are employed for interference mitigation.

## II. INTERFERENCE SUPPRESSION

Mutual interference between radars transmitting nonidentical time-frequency chirps is considered, as this type of interference is most likely to occur in automotive radars [1]. The baseband signal received by the ego (victim) radar experiences a time-limited disturbance of duration $T _ { d }$ when interfering chirps overlap transmitted chirps in time and frequency (see Fig. 1).

Let baseband signal samples be represented by a vector,

$$
\mathbf { s } ( n ) = [ \ s _ { 0 } ( n ) \quad s _ { 1 } ( n ) \quad \ldots \quad s _ { M - 1 } ( n ) \ ] ^ { T } ,\tag{1}
$$

where n is the sample number ranging from 0 to $N - 1$ $M$ is the number of antennas in the receiving (RX) array and $[ \cdot ] ^ { T }$ is the matrix transpose operator. The interfered samples in the baseband signal, denoted by $\mathbf { s } _ { \mathrm { i n t } } ( n )$ , can be identified by using a detector, as described $\mathrm { e . g . }$ in [5]. The beamforming weights adaptation using LMS algorithm is illustrated in Fig. 2. The intermediate beamformed output

$$
s _ { \mathrm { b f } } ( n ) = \mathbf { w } ( n ) ^ { H } \mathbf { s } _ { \mathrm { i n t } } ( n ) ,\tag{2}
$$

where $\mathbf { w } ( n )$ is a complex beamforming weight vector and $[ \cdot ] ^ { H }$ represents matrix Hermitian operator.

The desired signal $d ( n )$ typically required in adaptive beamforming is usually not available in radar applications. It is derived by simply delaying the intermediate output of the beamformer by one sample, i.e. $d ( n ) = s _ { \mathrm { b f } } ( n - 1 )$ . The presence of interference in $s _ { \mathrm { b f } } ( n )$ is indicated by relatively large magnitudes of error $e _ { \mathrm { i n t } } ( n )$ [4]. The adaptive algorithm iteratively adjusts the beamforming weights in such a manner that the error starts converging to its minimum. If the maximum value of error

$$
e _ { \mathrm { m a x } } = \operatorname* { m a x } _ { n } | e _ { \mathrm { i n t } } ( n ) | ,\tag{3}
$$

after one iteration of weights adaptation using all interfered samples is lower than a threshold $e _ { t h }$ , the adaptation is stopped and the weights at this point are chosen as final beamforming weights ${ \bf w } _ { f }$ . Otherwise, the adaptation is performed again and the weights at the end of the previous iteration are set as the initial condition for the next iteration. The threshold $e _ { t h }$ is calculated by multiplying the number of receiving channels M with the maximum firstorder difference magnitude in the non-interfered section of a single channel, i.e.

![](images/5d8bf1d36ebf38f3e1bb6b6f020aa5ea41294ac6363e53701996eead9f77f755.jpg)  
Fig. 1. Mutual interference mechanism in an FMCW radar. $\boldsymbol { B } _ { r x }$ is the receiver’s bandwidth, B and $B _ { i n t }$ indicate the chirp bandwidths for the ego and interfering radars, respectively, and $T$ and $T _ { i n t }$ indicate chirp durations.

![](images/bc9a33d7d918e5dff7e1782a8ac6b64af8feb51dc0e31b1defc2a446d8b4c492.jpg)  
Fig. 2. Adaptation for computing the final beamforming weights $\mathbf { w } _ { f }$

$$
e _ { t h } = M \times \operatorname* { m a x } _ { k } | s _ { 1 } ( k ) - s _ { 1 } ( k - 1 ) | ,\tag{4}
$$

where k denotes baseband samples with no interference. The final beamforming weights ${ \bf w } _ { f }$ are used to suppress interference in the output signal

$$
s _ { \mathrm { o u t } } ( n ) = { \mathbf w } _ { f } { } ^ { H } { \mathbf s } ( n ) .\tag{5}
$$

## III. INTERFERENCE IN REAL AND IQ RECEIVERS

A radar receiver can have either a real or an IQ implementation (e.g., [6], [7]) which determines the type of baseband signal (real or complex) obtained at the receiver’s output. The Radio Frequency (RF) signal received by the RX antenna is the same in both receiver implementations (see Fig. 3a). The target information is present only on one side of the instantaneous carrier frequency $f _ { c } .$ The interference (or noise), however, spans the complete bandwidth of the receiver $( f _ { c } \pm f _ { \mathrm { c o } }$ in the positive band and $- f _ { c } \pm f _ { \mathrm { c o } }$ in the image band, where $f _ { \mathrm { c o } }$ is the cut-off frequency of the anti-aliasing bandpass filter that defines the receiver’s bandwidth).

Down-conversion from RF to the baseband domain in a real receiver results in image band fold-back (see Fig. 3b). Therefore, it is sufficient to perform target detection on one side of the spectrum, and the redundant information from the image band can be discarded. When interference is present, the image band fold-back results in an overlap of the interference contributions from both the positive and image bands. Consequently, it is not possible to eliminate interference from the image band by simply discarding one side of the baseband spectrum. In this case, the interference in the baseband signal appears to be incident from two directions: 1) the actual direction of the interference source, denoted $\theta _ { \mathrm { i n t } } .$ , and 2) the mirror direction, i.e., $- \theta _ { \mathrm { i n t } }$ . When using digital beamforming, complete interference suppression is achieved by notching out the antenna beam in two directions per interference source.

![](images/85614ae359856c29d8e636d7b71ec2d9bfd708b1bf9b111e3d0dd973a21f4622.jpg)  
(b) Frequency spectrum of the real signal. There is an overlap of interference from positive and image bands.

![](images/8ae1ddd68657d23fe28f683c282caaa7f8c9670a265356393d153717a3f5aeca.jpg)  
(c) Frequency spectrum of the complex baseband (IQ) signal.  
Fig. 3. Frequency spectra of instantaneous RF, real baseband and complex baseband signal.

The image band’s contribution to the interference can be avoided by using an IQ receiver. This receiver implementation makes it possible to separate the positive and image bands. In the complex baseband spectrum, the targets are present only on one side of the spectrum and image band fold-back does not take place (see Fig. 3c). With an IQ receiver, each interference source can be suppressed with one notch in the antenna beam pattern. Therefore, fewer degrees of freedom are required to suppress the interference completely compared to a real receiver.

## IV. EXPERIMENTAL EVALUATION

The interference mitigation performance of the adaptive beamformer is evaluated using outdoor measurements. The target and radar parameters are given in Table I and the experimental setup is shown in Fig 4. The RX antenna is comprised of a four-element linear array with inter-element spacings of $\lambda / 2$ , where λ denotes the wavelength of the transmitted signal.

The time-domain plot of the baseband signal corresponding to a single chirp that has been subject to interference is shown in Fig. 5. The interference duration $T _ { d }$ is approximately 5.9 µs, which corresponds to 59 samples of the baseband signal. The adaptation of beamforming weights is completed after four iterations of interfered samples (total $4 \times 5 9 = 2 3 6$ samples in this case) through the adaptive algorithm. Final beamforming weights ${ \bf w } _ { f }$ are computed using a single chirp with interference and then used for beamforming in one complete signal frame (128 chirps).

TABLE I  
TARGET AND RADAR PARAMETERS.
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Target_1</td><td rowspan=1 colspan=1>Target_2</td><td rowspan=1 colspan=1>Radarint</td><td rowspan=1 colspan=1>Radarego</td></tr><tr><td rowspan=1 colspan=1>Range (m)</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Angle</td><td rowspan=1 colspan=1>-3°</td><td rowspan=1 colspan=1>20°</td><td rowspan=1 colspan=1>-23°</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Frequency (GHz)</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>=</td><td rowspan=1 colspan=1>76.5</td><td rowspan=1 colspan=1>76.5</td></tr><tr><td rowspan=1 colspan=1>Slope (MHz/µs)</td><td rowspan=1 colspan=1>=</td><td rowspan=1 colspan=1>=</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>16</td></tr></table>

![](images/7505addd117d3a805058bf025ded61e9b468906aa0ff2d9a757ba59af77eec2b.jpg)  
Fig. 4. Experimental setup as seen from the ego radar. Two corner reflectors are used as targets.

![](images/cd340edca6d314aa5e40c9a6a07fccd4958a1e5dcca9d0b706e039497f06869e.jpg)  
Fig. 5. Time domain plot of the baseband signal corresponding to a chirp subject to interference (single channel). The dashed rectangle highlights the part of the signal subject to interference.

Receiving array radiation patterns obtained using the adapted weights for real and complex baseband signals are shown in Fig. 6. The radiation pattern corresponding to the complex baseband signal has one notch in the direction of the source of the interference i.e. −23°. The radiation pattern corresponding to the real signal has two symmetric notches at $- 2 3 ^ { \circ }$ and $+ 2 3 ^ { \circ }$ due to the image band’s contribution to the interference.

The difference between the interference in real and complex baseband signals can also be seen from their respective range profiles in Fig. 7 and 8. The interference in an IQ receiver results in a uniform increase in noise. Whereas, in the real receiver, the noise level varies with range. It is, however, not possible to detect the targets in any of the cases due to high noise levels. The noise is suppressed in the beamformed signal and previously undetected targets become visible (see Fig. 7 and 8).

Signal to Interference and Noise Ratio (SINR) of 14.8 dB and 11.8 dB is achieved for Target 1 in complexbaseband and real beamformed output, respectively. For Target 2, 8.2 dB SINR is achieved in the complexbaseband output. This target is undetected in the real beamformed output due to the second notch in the receiving array beam pattern at 23°.

![](images/0de6901498ff7963e5965aaf955b8bb7b48d7a583de13d31a84e88877eeea5e9.jpg)

Fig. 6. Receiving antenna beam patterns for final adapted weights.  
![](images/b64e15482d8a48097febad252c2713d7cb4c5bc30bb65227aa539e03d8380cc5.jpg)  
Fig. 7. Range profiles of interfered (single channel), beamformed and interference-free (single channel) signals for an IQ receiver.

![](images/6953acd85b6f4b45e05c0f2f04021496ae1fcc26041c91cae87f02a7c2c2d1a9.jpg)  
Fig. 8. Range profiles of interfered (single channel), beamformed and interference free (single channel) signals for a real receiver.

Interference mitigation performance of the adaptive beamformer is also evaluated using Range-Doppler maps of interfered (single channel), interference free (single channel) and beamformed signals (Fig. 9 and 10). SINR of various targets from the Range-Doppler maps is summarized in Table II. The noise suppression can be observed by comparing Range-Doppler maps in interfered (Fig. 9b and 10b) and beamformed cases (Fig. 9c and 10c). Any targets spatially coinciding with the interference source also get suppressed as a result of beamforming. Therefore, the interfering radar, visible at 8 m range in interference free Range-Doppler maps (Fig. 9a and 10a), is suppressed in beamformed cases. It can be observed that the SINR of Target 2 (at 19 m) is also reduced in the beamformed case for real baseband signal. This reduction is due to the second notch in the antenna beam pattern that aims to suppress the image component of the interference.

![](images/21dbbdcbb81aeb940cb4a6d69bc77810dc00d48fab559d344b6958af7b67803b.jpg)  
(a) No interference (single channel).

![](images/a4b2ff829e7792aaacabf66a7c7bea9502a4e674337d2956ffd4e7777e8126f4.jpg)  
(b) Interfered (single channel).

![](images/5ce4a3da83af6b6d5b67fff57ad9bb0ca26113b775cf3ffcff0545573eaba745.jpg)  
(c) Beamformed.  
Fig. 9. Range-Doppler maps corresponding to complex baseband signals.

![](images/7cd4497ba2e6b99b4e5d03b27638638a1b3ce732b7532523cb4738693b82ae03.jpg)  
(a) No interference (single channel).

![](images/0fc03ebff51ec932c263ad07ce987a1c922312ac9e35c1078c85f8ba26bac49e.jpg)  
(b) Interfered (single channel).

![](images/0e732213288776d73994521af1446e63f3d21d72a90d59ed7b2a89669c2471e1.jpg)  
Fig. 10. Range-Doppler maps corresponding to real signals.  
(c) Beamformed.

TABLE II  
TARGET SINRS (dB) IN RANGE-DOPPLER MAPS.
<table><tr><td rowspan=1 colspan=1>Case</td><td rowspan=1 colspan=1>Radarint</td><td rowspan=1 colspan=1>Target_1</td><td rowspan=1 colspan=1>Target_2</td></tr><tr><td rowspan=1 colspan=1>Complex: No interference</td><td rowspan=1 colspan=1>26.8</td><td rowspan=1 colspan=1>43.6</td><td rowspan=1 colspan=1>42.6</td></tr><tr><td rowspan=1 colspan=1>Complex: Interfered</td><td rowspan=1 colspan=1>20.4</td><td rowspan=1 colspan=1>34.7</td><td rowspan=1 colspan=1>34.5</td></tr><tr><td rowspan=1 colspan=1>Complex: Beamformed</td><td rowspan=1 colspan=1>7.0</td><td rowspan=1 colspan=1>50.0</td><td rowspan=1 colspan=1>38.1</td></tr><tr><td rowspan=1 colspan=1>Real: No interference</td><td rowspan=1 colspan=1>24.1</td><td rowspan=1 colspan=1>41.3</td><td rowspan=1 colspan=1>40.1</td></tr><tr><td rowspan=1 colspan=1>Real: Interfered</td><td rowspan=1 colspan=1>17.9</td><td rowspan=1 colspan=1>32.3</td><td rowspan=1 colspan=1>31.6</td></tr><tr><td rowspan=1 colspan=1>Real: Beamformed</td><td rowspan=1 colspan=1>9.9</td><td rowspan=1 colspan=1>46.2</td><td rowspan=1 colspan=1>29.0</td></tr></table>

## V. CONCLUSION

The interference suppression performance of an LMSbased adaptive beamformer is evaluated using outdoor measurements from a 77 GHz FMCW radar. Targets masked by high interference in range profiles corresponding to single chirps can be detected after beamforming. In the Range-Doppler domain, maximum SINR improvement of 15 dB is achieved in the tested scenario when four channels are used for beamforming. The adaptive beamformer works with both real and IQ receiver implementations.

However, due to the image band fold-back in real receivers, complete interference suppression in these receivers requires more degrees of freedom (i.e. additional notches in the receiving array radiation pattern) than needed for IQ receivers. It is also shown that the additional notch in the radiation pattern may lead to the SINR degradation of desired targets, depending on their azimuth position.

## REFERENCES

[1] M. Goppelt, H. L. Blocher, and W. Menzel, “Analytical investigation¨ of mutual interference between automotive fmcw radar sensors,” in 2011 German Microwave Conference, March 2011, pp. 1–4.

[2] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” International Journal of Microwave and Wireless Technologies, vol. 6, no. 3-4, p. 371378, 2014.

[3] M. Kunert, “The eu project mosarim: A general overview of project objectives and conducted work,” in 2012 9th European Radar Con ference, Oct 2012, pp. 1–5.

[4] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive fmcw radars,” in 2018 IEEE Radar Conference (RadarConf18), April 2018, pp. 0252– 0256.

[5] Y. Watanabe and K. Natsume, “Interference determination method and fmcw radar using the same,” Mar. 6 2007, uS Patent 7,187,321.

[6] M. Steinhauer, H. Ruob, H. Irion, and W. Menzel, “Millimeter-waveradar sensor based on a transceiver array for automotive applications,” IEEE Transactions on Microwave Theory and Techniques, vol. 56, no. 2, pp. 261–269, Feb 2008.

[7] V. H. Le, H. T. Duong, A. T. Huynh, C. M. Ta, F. Zhang, R. J. Evans, and E. Skafidas, “A cmos 77-ghz receiver front-end for automotive radar,” IEEE Transactions on Microwave Theory and Techniques, vol. 61, no. 10, pp. 3783–3793, Oct 2013.