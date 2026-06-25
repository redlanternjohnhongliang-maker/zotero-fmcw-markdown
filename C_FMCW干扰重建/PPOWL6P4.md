# Sparse Reconstruction of Chirplets for Automotive FMCW Radar Interference Mitigation

1<sup>st</sup> Aitor Correas-Serrano

Cognitive Radar

Fraunhofer FHR

Wachtberg, Germany

aitor.correas@fhr.fraunhofer.de

2<sup>nd</sup> Mar´ıa A. Gonzalez-Huici´

Cognitive Radar

Fraunhofer FHR

Wachtberg, Germany

maria.gonzalez@fhr.fraunhofer.de

Abstract—Mutual interference in automotive radar scenarios is going to become a major concern as the density of vehicles with radar sensors in the roads increases. The present work tackles the problem of frequency modulated continuous wave (FMCW) to FMCW and continuous wave interference. In this context, we propose a signal processing technique to blindly identify and remove interference by using the fast Orthogonal Matching Pursuit (OMP) algorithm to project the interference signals in a reduced chirplet basis, and separate it from the target signal with minimal loss of information. Significant reduction of the noise-plus-interference levels are observed in both simulated and measured data, the later acquired with state of the art automotive sensors.

Index Terms—Automotive radar, interference mitigation, Orthogonal Matching Pursuit, chirplet transform, FMCW.

## I. INTRODUCTION

Radar is a key enabling technology for advanced driving assistant systems (ADAS) and autonomous driving due to its ability to detect motion and localize targets at long distances regardless of the weather and lighting conditions. The rise of popularity of this technology in the automotive field, further motivated by the advances in the production of low-cost radar chips, will make radar sensors ubiquitous in vehicles with high levels of automation. As increasing amount of these vehicles share the roads, car-to-car interference will become an issue that needs to be dealt with. Car-to-car radar interference, if not mitigated or avoided, degrades the detection capabilities of the sensors, effectively disabling them in dense traffic scenarios with high interference [1] [2] [3].

State of the art automotive radars use FMCW modulations restricted to the band of 76 GHz to 81 GHz, with short range radars (SRR) occupying most of the available bandwidth. In these conditions, interference is bound to happen. After the interference is identified, it could be avoided with frequency hopping techniques, as shown in [4]. In crowded environments, however, there is no guarantee that the new band will be interference free, in particular given that SRR radars may use most of the available spectrum. Other methods try to reconstruct the original signal assuming an approximate knowledge of the interference time [5], in some cases removing the interfered portions and performing range estimation with the remaining signal [6]. The removal of the interfered samples not only assumes knowledge of the time of interference, but it is also impractical for scenarios in which the majority of the signal is corrupted, as the remaining fragmented signal might not be enough to achieve a good estimation. More recent work blindly separates the interference from the target signal by solving a dual basis pursuit problem in the short-time Fourier transform (STFT) and standard Fourier basis [7]. However, the STFT basis is not ideal for representing fast wide-band events such as FMCW interference, due to its inherent trade-off between frequency and time resolution. The proposed method in [7] also requires a joint estimation of target and interference signals, reducing the flexibility of the approach. Lastly, basis pursuit tends to be more computationally complex and less suitable for hardware acceleration when compared to matching pursuit approaches [8] [9] [10].

![](images/eafd0c110a8a9313b5e293f5e281eaa59b5c6fa12315854c245f1140035e8ec6.jpg)  
Fig. 1. Interference can potentially impede the detection capabilities of the radar sensors, creating dangerous situations.

In FMCW processing, targets take the form of tones in baseband, whereas external FMCW interference with different modulation rate appears as a chirp. The chirp-like shape of the interference can be exploited to blindly detect and eliminate the interference by reconstructing the signal on a reduced chirplet transform basis. The chirplet transform decomposes the signal in time-windowed chirps [11] defined by their time delay, duration, starting frequency and modulation rate. In the case of FMCW radar interference, the bandwidth is set by the anti-aliasing filter in the receiver. This results in a reduced basis in which only the time delay and the duration of the interference remain as unknown parameters, lowering the computational complexity of the transform.

In this paper, we present a method to mitigate the interference in FMCW automotive radar by reconstructing the interference in the reduced chirplet basis using the Orthogonal Matching Pursuit (OMP) [12] algorithm. In Section II we briefly explain the FMCW radar model in the presence of interference, illustrating how interference appears in the receiver after down-conversion and filtering. Subsequently, we justify the use of a reduced chirplet transform as basis for the interference, and propose a fast method to mitigate it applying OMP sparse reconstruction with the reduced chirplet basis in Section III. Simulated results are presented and discussed in Section IV. Section V and Section VI show respectively the experimental setup for the data acquisition and the results of applying the proposed method in interfered automotive radar signals, showing significant improvements in the signal to noise-plus-interference ratio (SNIR). Section VII concludes the paper.

## II. FMCW SIGNAL MODEL WITH INTERFERENCE

In this section we shortly describe the signal model for FMCW radar in the presence of FMCW interference. Automotive radar sensors operate generally with real-valued samples, hence we work with the sine function in time domain rather than complex exponential terms. The most common waveform in automotive FMCW radar is the linearly frequency modulated signal (chirp), defined as

$$
s _ { r e f } = \sin ( 2 \pi ( f _ { c } t + \frac { k } { 2 } t ^ { 2 } ) ) \mathrm { f o r } 0 < t < T\tag{1}
$$

with T being the chirp duration, k being the modulation rate defined as the $B / T$ , and B being the bandwidth. This signal also serves as reference signal for the down-conversion process in the receiver. The carrier frequency $f _ { c }$ lays in the reserved automotive radar band, from 76 GHz to 81 GHz.

If there are $N _ { i }$ chirp-like interference signals from another FMCW radars operating in the same band with modulation rate $k _ { i } ,$ and $N _ { t }$ echoes from target reflections, the signal at the receiver is the sum of the signal from the targets $s _ { R }$ and the interference signals $s _ { I } \colon$

$$
s _ { R } = \sum _ { t } ^ { N _ { t } } { P _ { t } \sin ( 2 \pi ( f _ { c } ( t - \tau _ { t } ) + \frac { k } { 2 } ( t - \tau _ { t } ) ^ { 2 } ) ) }\tag{2}
$$

$$
s _ { I } = \sum _ { i } ^ { N _ { i } } P _ { i } \sin ( 2 \pi ( f _ { c } ( t - \tau ) + \frac { k _ { i } } { 2 } ( t - \tau _ { i } ) ^ { 2 } ) )\tag{3}
$$

where $\tau$ is the propagation delay, the i sub-index corresponds to the parameters associated to the interference signals, and t sub-index to the ones associated to the targets. $P _ { t }$ stands for the amplitude of the target echo, whereas $P _ { i }$ refers to the amplitude of the signal from the interfering radar.

The received signal is converted to baseband through mixing with the complex conjugate (i.e., a phase delay of 180 degrees) of the reference signal (1)

$$
y ( t ) = ( s _ { R } + s _ { I } ) s _ { r e f } ^ { * } = y _ { R } + y _ { I }\tag{4}
$$

![](images/a7f990d516b693d4caea5683498919669a168e63afca1bbfde7c0d468445d995.jpg)  
Fig. 2. Simulated FMCW radar interference in baseband. The chirp-like time restricted nature of this type of interference is clear in the STFT representation of the signal. This transform, however, is not adequate for interference mitigation due to the trade-off between time and frequency accuracy inherent to the STFT basis.

where

$$
y _ { R } = \sum _ { t } ^ { N _ { t } } P _ { t } \sin ( \pi k ( \tau _ { t } ^ { 2 } - 2 t \tau _ { t } ) + 2 \pi f _ { c } \tau _ { t } )\tag{5}
$$

$$
y _ { I } = \sum _ { i } ^ { N _ { i } } P _ { i } \sin ( \pi ( k _ { i } - k ) t ^ { 2 } - 2 k _ { i } t \tau _ { i } + k _ { i } \tau _ { i } ^ { 2 } + 2 \pi f _ { c } \tau ) .\tag{6}
$$

The first term of the summation in (4) corresponds to a target echo, appearing as a tone at a particular beat frequency. The second term accounts for the interference, with a quadratic phase term that corresponds to a linearly modulated frequency (a chirp) in baseband. After down-conversion, the bandwidth of the signal is limited by an analog low-pass filter, with a pass frequency $f _ { r } = f _ { s } / 2$ , in order to avoid aliasing. In further derivations, we consider a perfect low-pass filter, so no components over the sampling frequency appear in the signal. The instantaneous frequency of the interference is, as a result, bounded by the receiver

$$
| f _ { i } ( t ) | = | ( k _ { i } - k ) t - 2 k _ { i } \tau ^ { 2 } | \leq f _ { r } ,\tag{7}
$$

as is the duration

$$
T _ { i } \leq \left| \frac { 2 f _ { r } } { ( k _ { i } - k ) } \right| .\tag{8}
$$

After establishing the time and frequency bounds of the interference signal through the receiver bandwidth, we can finally write the received signal in baseband as

$$
y ( t ) = { \left\{ \begin{array} { l l } { y _ { R } + y _ { I } } & { { \mathrm { i f } } ~ { \frac { k _ { i } \tau _ { i } - f _ { r } } { k _ { i } - k } } \leq t \leq { \frac { k _ { i } \tau _ { i } + f _ { r } } { k _ { i } - k } } } \\ { y _ { R } } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{9}
$$

Fig. 2 shows a simulated scenario in which we can observe interference in both time domain as well as the corresponding short time Fourier transform (STFT) domain. The signal is even in frequency, as we consider real-valued samples. The chirp-like, time limited nature of the interference becomes clear in the STFT representation.

## III. METHOD FOR INTERFERENCE IDENTIFICATION ANDMITIGATION

The proposed method relies on a projection of the received signal in a reduced chirplet transform basis. To find this projection, we use the Orthogonal Matching Pursuit (OMP) [12] algorithm, as it is fast and it can be further accelerated through embedded programming, making it a great choice to achieve real time computation with actual automotive radars.

## A. Reduced chirplet transform basis

The chirplet transform reconstructs a signal as a summation of time limited chirps of varying characteristics and amplitude. Traditionally, the chirplet transform is a 4-parameter transform. The atoms of the chirplet basis are

$$
c _ { \nu , \tau , \delta , \kappa } ( t ) = \sin ( 2 \pi ( f _ { \nu } t + \frac { k _ { \kappa } } { 2 } t ^ { 2 } ) ) \quad T _ { \tau } < t < ( T _ { \tau } + T _ { \delta } ) ,\tag{10}
$$

with the four parameters characterized in the sub-indexes $[ \nu , \tau , \delta , \kappa ]$ representing the different possible values of frequency-shift, time-shift, duration and modulation-rate of the chirp hypothesis. Such a transform is costly to compute. In the context of FMCW interference, however, we can define a reduced chirplet transform in which some of these parameters are defined by the characteristic of the receiver. Namely, the frequency shift is set to be the cut-off frequency of the low pass filter $f _ { r } ,$ , whereas slope and duration turn into coupled parameters also defined by the bandwidth of the receiver, as per (8), eliminating the need to estimate one of them. As a result, we define a new, reduced chirplet basis, whose chirplets are defined as

$$
c _ { \tau , \kappa } ( t ) = \sin ( 2 \pi ( f _ { r } t + \frac { k _ { \kappa } } { 2 } t ^ { 2 } ) ) \quad T _ { \tau } < t < ( T _ { \tau } + T _ { i } ) ,\tag{11}
$$

Selecting $M _ { \kappa }$ hypothesis for the slopes and M<sub>τ</sub> hypotheses of the time-shift, we can create a dictionary for our reduced chirplet transform

$$
A = [ c _ { 1 1 } , . . . , c _ { \tau 1 } , . . . , c _ { 1 \kappa } , . . . , c _ { \tau \kappa } ] \in \mathbb { R } ^ { N \times M } .\tag{12}
$$

with $M = M _ { \kappa } M _ { \tau }$ . For the reconstruction of the interference, we choose values of $| k _ { \kappa } | > 0$ , as we do not want to include the actual targets in our dictionary.

## B. Orthogonal Matching Pursuit for interference mitigation

OMP is well known for its use in sparse reconstruction problems in compressed sensing, and has seen some use in the radar field. It is a fast greedy algorithm suitable for hardware accelerated implementations [13] [14], making it ideal for automotive radar, where cost and computational resources are main limiting factors.

OMP finds a solution to $y = A x$ in x, where $\boldsymbol { y } \in \mathbb { R } ^ { N }$ is the measurement (the samples corresponding to a chirp), A is our chirplet basis and $\boldsymbol { x } \in \mathbb { C } ^ { M }$ is the interference reconstruction in the chirplet basis. For an M-long grid of hypotheses, OMP first estimates hypothesis m of the dictionary A with the maximum correlation with the current residual

$$
\begin{array} { r } { \operatorname * { a r g m a x } _ { i } \quad m : = A ^ { H } r _ { i t - 1 } , } \end{array}\tag{13}
$$

where i is the hypothesis index, and it is the iteration counter, with $r _ { i t }$ being the residual signal, initialized as $r _ { 0 } = y$ . The grid point m is stored in a set $\mathsf { \bar { \Pi } } ^ { i t } = I ^ { i t - 1 } \mathsf { \cup } m$ . The columns of A listed in $I ^ { i t }$ are selected to form the partial sensing matrix $E ,$ through which the complex coefficients for the selected hypothesis are calculated by finding $m i n _ { w } | | y - E w | | _ { 2 }$ . The residual is updated as

$$
r _ { i t } = y - E w ,\tag{14}
$$

and the algorithm continues to the next iteration. The algorithm stops once $r _ { i t }$ falls below a given threshold, or after a predefined number of iterations. The reconstructed signal x is obtained by setting the entries indexed in $I ^ { i t }$ to the corresponding value of $w _ { i t }$ , leaving the rest of entries of x at zero.

By setting A as our reduced chirplet basis, we can see how we obtain information about the interference based on the reconstructed x. More importantly, given a successful approximation of the interference, the residual after the application of the algorithm will have the interference components removed in (14), leaving only the target related components to apply any posterior processing. The Doppler and direction of arrival phase components in the target signals are preserved. Note that OMP could be used to estimate also the targets using a fitting model $\hat { \mathsf A }$ with beat frequency tones as hypotheses. We choose to use OMP to reconstruct only the interference (i.e. not including target echo hypothesis in our model) with the intention of accurately showing the extent of the interference mitigation through the comparison of the spectral power density of the signals before and after the mitigation.

## IV. SIMULATIONS

To test our approach we build a simulation environment in which we can generate interfered signals based on the presented model. Interference is a complicated event to measure in a controlled scenario, specially so in the case of multiple simultaneous interference. This simulation environment allows us to test our interference mitigation algorithm in a variety of hypothetical scenarios. We generate the interference offgrid, but we do not take into account the non-idealities in the receiver of a real sensor. Fig. 3 and Fig. 4 show the time and frequency domain of two synthetic received signals before and after the application of our interference mitigation algorithm.

![](images/670ffa76529e358f30b7c02c0ef37f832a356ae84997557257e1926a58c8e0ac.jpg)

![](images/c65e287af99ce4981db9b3de1738ad9202e4b33f43b376cd3ab6f63138f850fe.jpg)  
Fig. 3. Interference mitigation in a simulated scenario with two targets and a strong interferer. We achieve an improvement of the SNIR to levels close to the non interfered signal.

![](images/4f798733bc1d7d4b29c52ec2c03ece68f9a0b7cb8d5effc19008136d488524e4.jpg)  
Fig. 4. Interference mitigation in a simulated scenario with one target, four strong interferers, and interference overlapping. The improvement of 50 dB in the SNIR is good enough to discern the target from the noise-plus-interference.

We apply a two step search using the proposed method: a first search over a coarse grid in the whole range of possible time-shifts and slopes, and a second search with a fine grid defined in the regions where interference is likely, according to the first search. For the first search, we use $M _ { \kappa } = 2 0 0$ slope hypotheses and $M _ { \tau } = 6 0 0$ time-shift hypotheses. In the second search we set $M _ { \kappa } = 4 0$ and $M _ { \tau } = 4 0$ . The synthetic signal has $N = 2 0 0 0$ samples in both cases. We use bigger values of $M _ { \kappa }$ and $M _ { \tau }$ in the first step as we search over a wider variety of time-delay and slope hypothesis. A measure of the variation of the energy in the residual term is used as stopping criteria for OMP.

Fig. 3 represents a relatively easy scenario, in which there is one strong interference that completely masks the target beat frequencies. After mitigation of the interference through the restricted chirplet transform we observe an estimation of similar quality to that of the synthetic signal without added interference. This represents an average improvement in the SNIR of over 35 dB. Fig. 4 depicts a more complex scenario with four interferers, each of them of higher power than the interferers in Fig. 3, and with two of the interference signals overlapping in time. This scenario is particularly challenging due to the full overlapping between two independent interference signals and the high interference power, around 40 dB over the power of the echo from the target. The result of applying our interference mitigation algorithm is an increase of the SNIR level of an average of 50 dB, enough to distinguish the target over the remaining noise and nonmitigated interference.

While these case studies show the potential of our approach to mitigate interference in a variety of scenarios, there are a multitude of non-idealities occurring in real sensors that we are not accounting for. With this as motivation, we set up a simple measurement campaign to test our approach with actual

![](images/a5d8feffdc5bfbc5d9b475a9651bb6fc461313976b39d616e560bf59c47dfcd2.jpg)  
Fig. 5. On the top, a picture of the measured scenario, with a target and an interference source. Radarbook (reference) on the bottom left and NXP Eagle (interference) on the bottom right.

measurements.

## V. EXPERIMENTAL SETUP

To capture automotive radar interference, we set up an experiment in which we confront two different automotive radar sensors, simultaneously transmitting and receiving in the band of 76-77 GHz. The data used for the validation of our algorithm is captured by the 4Tx/8Rx Radarbook system, commercialized by Inras [15]. The interfering sensor is a prototype NXP 76-81 GHz Eagle RaceRunner Ultra based on NXP MR3003 / S32R274 chipset. We use a corner reflector as reference. Both sensors, in addition to the measured scenario, are shown in Fig. 5. The FMCW waveform parameters in both sensors are shown in table I. As a target we use a trihedral corner reflector of estimated radar cross section of 6 square meters at the operating band.

## VI. RESULTS AND DISCUSSION

To demonstrate the validity of our approach we choose a heavily interfered measurement, with the target buried below the signal-plus-interference level. As a preliminary step, we apply a digital high-pass filter to the sampled signal to reduce the effect of cross-talk between elements, as it is several orders of magnitude higher than the expected power from target reflections. Then, we apply the same filter to the hypotheses in our model, to avoid introducing a mismatch.

TABLE I  
FMCW WAVEFORM PARAMETERS OF REFERENCE AND INTERFERENCE
<table><tr><td rowspan=1 colspan=1>ChirpParam.</td><td rowspan=1 colspan=1>Radarbook - Reference(Up Chirp / Down Chirp)</td><td rowspan=1 colspan=1>NXP Eagle - Interference(Up Chirp / Down Chirp)</td></tr><tr><td rowspan=1 colspan=1>k</td><td rowspan=1 colspan=1>37 THz s⁻¹/ -111 THz s⁻¹</td><td rowspan=1 colspan=1>33.7 THz s -¹/ -11.6 THz s ¹</td></tr><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>27 μs/9μs</td><td rowspan=1 colspan=1>29.6 μs / 85 μs</td></tr><tr><td rowspan=1 colspan=1>Freq.</td><td rowspan=1 colspan=1>76 Ghz - 77 GHz</td><td rowspan=1 colspan=1>76 Ghz – 77 GHz</td></tr><tr><td rowspan=1 colspan=1>fs</td><td rowspan=1 colspan=1>10 MHz / -</td><td rowspan=1 colspan=1></td></tr></table>

![](images/4f3b87276a93440dfdfea833f9b525fbf5a5507f7a967648812a91835f4f65e6.jpg)  
Fig. 6. Interference mitigation applied to the interfered signal after high-pass filtering. We see a reduction of the SNIR level of up to 20 dB after mitigation, enough to recover our target.

For the interference mitigation algorithm we assume no prior knowledge about the time of characteristics of the interference, other than it being a CW or FMCW signal. We use the same two step search applied to the synthetic measurements. For the first search, $M _ { \kappa } = 2 0$ slope hypotheses and $M _ { \tau } = 3 0 0$ time-shift hypotheses. For the second search we use $M _ { \kappa } = 2 0$ and $M _ { \tau } = 1 0 0$ . The received signal has $N = 2 2 9$ samples. If we assume the possible models A are stored in memory and do not need to be computed, the total execution time approximates the execution time of OMP, which takes around 0.07 seconds in a MATLAB CPU implementation.

In Fig. 6 we observe the range estimation of an interfered chirp. The target in the received, interfered signal can not be detected, as its power level is below the noise-plus-interference floor. After applying the proposed mitigation approach, the contribution of the interference is reduced and the target appears around 18 dB over the new signal-plus-interference floor. While a degradation in the SNIR can still be appreciated with the non-interfered measurement, the proposed method achieves an improvement of around 20 dB. The reduction in performance when compared to the synthetic cases is likely caused by hardware non-idealities in the receiver that are not captured by our model. Further research in this direction is likely to help increase the amount of interference removed.

## VII. CONCLUSIONS

In this paper a method to identify and mitigate interference in an automotive scenario is presented. The interference signal is reconstructed using a reduced chirplet basis and the interference contribution is subsequently removed by sparse reconstruction using the OMP algorithm. Results with synthetic and real data show that we can greatly diminish the effect of the interference, recovering targets that would otherwise be masked by it. OMP can be accelerated by hardware, making it a good choice for real time automotive applications.

## ACKNOWLEDGMENT

We thank our colleagues David Mateos-Nu´nez and Carlos˜ Moreno-Leon for fruitful discussions and their help during the´ measurement campaigns, and NXP Semiconductors for their assistance by providing one of the sensors for our tests.

## REFERENCES

[1] M. Goppelt, H. L. Blocher, W. Menzel, “Automotive radar investigation¨ of mutual interference mechanisms,“ Advances in Radio Science, 8(B. 3),2010, pp. 55-60.

[2] M. Goppelt, H. L. Blocher, W. Menzel, “Analytical investigation of¨ mutual interference between automotive FMCW radar sensors,“ In Microwave Conference (GeMIC), 2011, pp. 1-4.

[3] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,“ IEEE Transactions on Electromagnetic Compatibility, 49(1), 2007, pp. 170-181.

[4] J. Bechter, C. Sippel, C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,“ in Microwaves for Intelligent Mobility (ICMIM), 2016, pp. 1-4.

[5] J. Bechter, C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,“ in Microwaves for Intelligent Mobility (ICMIM), 2015, (pp. 1-4).

[6] J. Bechter, F. Roos, M. Rahman, C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,“ in European Radar Conference (EuRAD), 2017, pp. 90-93.

[7] F. Uysal, S. Sanka, “Mitigation of automotive radar interference,“ in Radar Conference (RadarConf18), 2018, pp. 405-410.

[8] S. Kunis, H. Rauhut, “Random sampling of sparse trigonometric polynomials, ii. orthogonal matching pursuit versus basis pursuit,“ Foundations of Computational Mathematics, 8(6), 2008, pp. 737-763.

[9] A. Correas-Serrano, M.A. Gonzalez-Huici, “Experimental Evaluation of´ Compressive Sensing for DoA Estimation in Automotive Radar,“ in 2018 19th International Radar Symposium (IRS), 2018. pp. 1-10.

[10] Y. Quan, Y. Li, X. Gao, M. Xing, “FPGA implementation of realtime compressive sensing with partial Fourier dictionary,“ International Journal of Antennas and Propagation, 2016.

[11] A. Bultan, “A four-parameter atomic decomposition of chirplets,” IEEE Transactions on Signal Processing, vol. 47, 1999, pp. 731-745.

[12] J. Tropp, A. C. Gilbert, “Signal recovery from partial information via orthogonal matching pursuit,“ IEEE Trans. Inform. Theory, 53(12), 2007, pp. 4655-4666.

[13] P. Blache, H. Rabah, A. Amira, “High level prototyping and FPGA implementation of the orthogonal matching pursuit algorithm,“ in Information Science, Signal Processing and their Applications (ISSPA), 11th International Conference, 2012, pp. 1336-1340.

[14] H. Rabah, A. Amira, A., B. K. Mohanty, S. Almaadeed, P. K. Meher, “FPGA implementation of orthogonal matching pursuit for compressive sensing reconstruction,“ IEEE Transactions on very large scale integration (VLSI) Systems, 23(10), 2015, pp. 2209-2220.

[15] Radarbook product page, http://www.inras.at/en/products/radarbook

[16] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,“ IEEE Transactions on Electromagnetic Compatibility, 2007, pp. 170- 181.