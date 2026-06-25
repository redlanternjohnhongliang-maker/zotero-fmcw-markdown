# Interference Characterization in FMCW radars

Sandeep Rao and Anil Varghese Mani

Texas Instruments

Bangalore, India

s-rao@ti.com

Abstract— As the penetration levels of Automotive radars increase so will the problem of mutual interference. It is important to understand how this will affect the performance of current radar technology. The aim of this paper is the statistical characterization of interference in the context of fast chirp FMCW radar. We focus on two categories of interference: ‘Parallel’ and ‘Sweeping’. Through analysis and simulation we provide an insight into the mechanism of interference and also the inbuilt resilience of FMCW radars which help in interference mitigation. Monte Carlo simulations (of multiple radars at randomized distances) are used to provide a sense of radar performance in real-life scenarios. We discuss the performance difference between real and complex base-band FMCW architectures. For comparison we also present simulation results for PMCW radars.

Keywords— Automotive radar, FMCW radar, interference, mutual interference, PMCW radar

## I. INTRODUCTION

Interference can severely impair the performance of an automotive radar. This problem is expected to increase in the coming years due to two reasons. Firstly, the number of radars on the road will increase. Simultaneously, as we move towards automobiles with higher levels of driving autonomy, the performance requirements (longer range, better safety) for radars will also correspondingly increase. All of this demands a comprehensive solution to automotive radar co-existence.

The basic mechanisms of interference in the context of Frequency Modulated Continuous Wave (FMCW) radars are well understood [1]-[3]. While a comprehensive solution to interference still remains an open problem, there has been prior work ([4]-[8]) in the area of detection and mitigation algorithms. While FMCW remains the most prevalent modulation scheme for Automotive radar, alternate modulation schemes such as Phase Modulated Continuous Wave (PMCW) [9][10] have been proposed as a way to mitigate interference. A radar communication approach to combat interference has been proposed in [11]. However, this needs standardization and infrastructure, so it is important to characterize performance of autonomously operating radars.

The goal of the current paper is to statistically characterize interference between FMCW radars. Our study focuses on two categories of interference for FMCW radars:

Parallel Interferers: This refers to a scenario where all the interfering radars use a nominal signal configuration that is identical to the victim radar (except for deviations due to clock drift).

Sweeping Interferers: This refers to a scenario where the victim and the interfering radars have different chirp configurations – specifically widely differing chirp slopes. This can happen for e.g. when a Short Range Radar (SRR) interferes with a Long Range Radar (LRR); the SRR typically having a higher range resolution and thus a higher slope compared to the LRR.

In practice interferers can be a mix of the above categories and there could be interferers which fall in the continuum between ‘Parallel’ and ‘Sweeping’. Nevertheless a study of these two distinct classes of interferers is instructive.

There has been prior work in this area (most recently [6],[12]]). For the case of parallel interferers [12] focusses on the statistical characterization of false detection of ghost objects. In contrast this work also focusses on detection probabilities of real objects (we handle the problem of ghost objects using binary phase encoding across chirps in a frame, as is explained later). Additionally both our analysis and simulation considers the effect of important non-idealities such as clock drift and phase noise which are ignored in the previous works. For the case of sweeping interferers [6] characterizes the performance of various mitigation techniques. Both [6] and [12] assume the presence of a single interferer. Our work considers the effect of multiple radars at different distances and its effect on both interference and mitigation. This is essential to get a sense of radar performance in real-life scenarios. This paper also includes a discussion on the interference performance of real vs complex base-band architectures which to our knowledge has not been discussed elsewhere. Finally, the simulation results for FMCW radars are compared with corresponding results for PMCW radars. Thus this paper provides significant insight that is not found in earlier publications.

The outline of this paper is as follows. Section II and Section III study FMCW-to-FMCW interference under the categories of Parallel and Sweeping interferers respectively – covering both mathematical analysis and simulation results. Section IV is a discussion on real vs complex base-band architectures for FMCW radar. Section V contrasts the results of FMCW-to-FMCW interference with PMCW-to-PMCW interference. Section VI summarizes key learnings and outlines future work.

## II. PARALLEL INTERFERER

![](images/e2cd719e236d59cbc01ec0c75534d3abc1f5269f25885c9d53c50ca3e479bb21.jpg)  
Fig. 1: A 1TX-1RX FMCW Radar

Fig.1 shows the simplified block diagram of an FMCW radar with a single representative transmit (TX) and receive (RX) channel [13]. A Local Oscillator (LO) generates a chirp which is transmitted by the TX antenna. The signal received at the RX antenna (reflections of the transmit signal from objects in the scene) is mixed with the TX signal to generate an Intermediate Frequency (IF) signal. The mixer can be a real-mixer (as in traditional automotive radars) or complex [14]. This paper assumes a complex mixer. It can be shown that the frequency of the IF signal $( f _ { I F } )$ is directly proportional to the round trip delay (??) to the object and is given by $f _ { I F } = S \tau$ ; ?? being the slope of the chirp. Thus based on the maximum range of interest $( \operatorname { s a y } r _ { m a x } )$ , one can calculate the maximum round trip delay $\begin{array} { r } { ( \tau _ { m a x } = \frac { 2 r _ { m a x } } { c } ) } \end{array}$ and the corresponding maximum IF frequency of interest $( f _ { I F , m a x } = S \tau _ { m a x } )$ . The IF signal is low pass filtered (by an anti-aliasing filter) such that all frequencies greater than $f _ { I F , m a x }$ are filtered out. The filtered signal is then sampled by an ADC and then undergoes further digital processing. Typically multiple equispaced chirps are transmitted in a unit called a frame. The digitized received signal corresponding to the frame is then processed across multiple RX antennas to estimate the range, velocity and angle of targets.

![](images/729a8747fbec23d1394c383882e5ed1ac270aec8941ab0b39d5f9377d2337a79.jpg)

![](images/9c306a0da92a62ed6518f4e15b620478d7f5b85caf4e9d96060b8875915822e3.jpg)

![](images/b128d98c7f0089ea66ab2179c0f922ea6635a46dec33720e8e562775f1d84061.jpg)

![](images/5d2ea95fd2a6620ea48d3bbf67778d3f65e81dfa7ac4bd66c337f9d7e4b1b018.jpg)  
Fig (a) $\tau _ { i } < \tau _ { m a x }$  
Fig (b) $\tau _ { i } > \tau _ { m a x }$  
Fig. 2: In-band(a) and Out-of-band(b) interferers

Fig. 2 shows a chirp (blue) of duration $T _ { c } .$ If the maximum round trip delay of interest is $\tau _ { m a x }$ , then any interfering signal (red) with an offset $\tau _ { i } < \tau _ { m a x }$ will show up as peak (ghost object) in the IF spectrum at a frequency $f _ { I F , i } = S \tau _ { i }$ . This is illustrated in Fig. 2(a). However if an interfering signal has an offset $\tau _ { i } > \tau _ { m a x }$ then the corresponding IF frequency will be greater than the low pass filter cut-off $( f _ { I F , m a x } )$ and hence not affect the IF signal (Fig. 2(b)). Assuming a random offset between the victim chirp(blue) and interfering chirp (red), the probability of an interfering chirp being in-band to the victim chirp is:

$$
p _ { i } = \tau _ { m a x } / T _ { C } .\tag{1}
$$

Noting that $\begin{array} { r } { r _ { m a x } = \frac { c \tau _ { m a x } } { 2 } } \end{array}$ and $\begin{array} { r } { v _ { m a x } = \frac { \lambda } { 4 T _ { C } } [ 1 3 ] . } \end{array}$ , the probability of interference can be re-written as $p _ { i } =$ $\begin{array} { r } { \frac { \mathbf { \phi } ^ { \mathrm { { s } } } r _ { m a x } v _ { m a x } } { c \lambda } . } \end{array}$ Here $v _ { m a x }$ is the maximum measurable velocity of the radar. This equation nicely brings out the trade-off between radar performance and probability of interference => the larger the $r _ { m a x } X v _ { m a x }$ product the higher the probability of interference.

## A. Basic Analysis

The previous discussion calculated the probability of a chirp being affected by interference. However, note that an ideal parallel interferer creates a single tone in the IF frequency (e.g., Fig. 2(a)) and affects only a single range bin. So other range bins would still be ‘interference free’ (We ignore artefacts such as relative clock drift and phase noise which are considered later). It therefore seems more relevant to calculate the probability of a single range bin being corrupted by interference. This per-bin probability can be calculated by replacing $\tau _ { m a x }$ in eq(1) with the round trip delay interval $( \operatorname { s a y } \tau _ { b i n } )$ corresponding to a range bin (so if $r _ { b i n }$ is the resolution of a range bin, then $\tau _ { b i n } = \frac { 2 r _ { b i n } } { c } )$

Consider a radar frame with $N _ { c h i r p s }$ chirps per frame. Consider a victim radar with n of these chirps overlapping with an aggressor radars frame. Additionally let the clock drift between the victim and the aggressor be ??. So if the clock drift is say 100ppm then $\delta { \bf \phi } = 1 0 0 e ^ { - 6 }$ . We wish to calculate the probability $( p _ { i , r a n g e } )$ that, during this overlap period, a specific range bin of the victim radar will be interfered with. Note that with clock-drift, the relative location of the aggressor chirp w.r.t the victim shifts by $\delta T _ { c }$ every consecutive chirp (Fig. 3). So with n overlapping chirps, the probability of the interferer corrupting any specific range bin is:

$$
\begin{array} { r } { p _ { i , r a n g e } ( n , \delta ) = \frac { \tau _ { b i n } + n | \delta | T _ { c } } { T _ { c } } . } \end{array}\tag{2}
$$

![](images/1892af6bde004d8fbe16c8bf45a05d1a9b68710f43fe9686bc545d9a213d444d.jpg)  
Fig. 3: Drift between Victim and Interferer chirps

We assume random alignment between the interferer and the victim. Also the relative clock drift between the aggressor and victim radar is assumed to be uniformly distributed between $[ - \delta _ { m a x } , \delta _ { m a x } ]$ , where $\delta _ { m a x }$ is the clock drift . Thus averaging across both ?? and $\delta$ , we get the average probability of interference to be

$$
\begin{array} { r } { p _ { i , r a n g e } = \frac { \tau _ { b i n } + 0 . 2 5 N _ { c h i r p s } \delta _ { m a x } T _ { c } } { T _ { c } } . } \end{array}\tag{3}
$$

With the above basics we are now ready to consider the following problem: A signal from a radar sensor has a frame length of $\setminus$ and a refresh rate of $1 / T _ { u }$ (i.e., one frame is transmitted every $T _ { u }$ seconds). Consider an interfering signal having an identical signal structure i.e., identical chirps with the same $S , T _ { c } , T _ { f }$ and $T _ { u } .$ We want to estimate the probability $p _ { I { \ ' } }$ , that in the presence of this single interferer, a particular range bin is affected by interference. This probability can be computed as the product of two probabilities: probability of interferer overlapping with victim and probability of an overlapping interferer falling in-band. The former probability is equal to $2 T _ { f } / T _ { u }$ (see Fig. 4) and the latter is equal to $p _ { i , r a n g e }$ . Thus

$$
\begin{array} { r } { p _ { 1 } = \frac { 2 T _ { f } } { T _ { u } } p _ { i , r a n g e } = \frac { 2 T _ { f } } { T _ { u } } \bigg ( \frac { \tau _ { b i n } + 0 . 2 5 N _ { c h i r p s } \delta _ { m a x } T _ { c } } { T _ { c } } \bigg ) . } \end{array}\tag{4}
$$

![](images/f78d11deaeaa44286f6b5e83cb6f8709a90388299e530284f7d514bb86595ed2.jpg)  
Fig. 4: Probability of frame overlap

The probability of a specific range bin being free from interference is thus $( 1 - p _ { 1 } )$ . Extending this to multiple

interferers we get the following expression for any range bin being free from interference in the presence of $N _ { i }$ interferers.

$$
\begin{array} { r } { p _ { n o - i n t e r f e r e n c e , N _ { i } } = ( 1 - p _ { 1 } ) ^ { N _ { i } } = } \\ { \bigg ( 1 - \frac { 2 T _ { f } } { T _ { u } } \Big ( \frac { \tau _ { b i n } + 0 . 2 5 N _ { c h i r p s } \delta _ { m a x } T _ { c } } { T _ { c } } \Big ) \bigg ) ^ { N _ { i } } . } \end{array}\tag{5}
$$

## B. More Refined Analysis

The previous analysis used a simple model to predict the probability of interference events (though as will be seen later in Section IID, this simple analysis does provide a good first approximation match to simulation performance). A more refined model needs to accommodate other effects. Specifically, two aspects that are important in order to estimate the effect of the interfering signal on target detection probabilities are (1) impact of phase noise of the interfering signal (2) in-band interference noise level esp. in the presence of clock drift (‘range-gate smearing’).

Phase Noise: Phase noise of the local oscillator results in noise side-bands (‘skirt’) around the peaks in the IF spectrum. This is true for peaks corresponding to detected objects as well as ghost objects corresponding to parallel interferers. In particular it is important to note that an out-ofband interferer can still have a significant portion of its phase-noise induced skirt in-band to the victim radar (Fig. 5). Thus out of band interferers can also impact performance.

![](images/b29658e29c8dd52f8a9e98adc5933c31d0443fe7e752f3eba87a253feac0612e.jpg)  
Fig. 5: Phase noise side-bands of interferer

Range gate smearing: In Section IIA we assumed that an interferer chirp remained parallel to the victim chirp even in the presence of clock drift. The implicit assumption being that the slopes of the interferer and victim are identical. However in reality, clock drift results in a slight difference in chirp slopes. If S is the nominal slope, a relative clock drift of ?? results in a slope difference of ???? between the victim and aggressor chirps (see left of Fig. 6). In the absence of a clock drift, the interferer would have shown up as a single peak (ghost object) in the IF frequency. However, in the presence of clock drift, the peak is ‘smeared’ across an IF frequency band of $S \delta T _ { c }$ . If P<sub>i</sub> is the power of the interferer, the spectral density after smearing will be $\frac { P _ { i } } { S \delta T _ { C } }$ dBc/Hz (Fig. 6).

![](images/6d22a56133608275d4fafa73397d7f4e177ed366d4ecbc41d4e56ba9bcbbc2e8.jpg)  
Fig. 6: Range gate smearing due to relative clock drift

## C. Note on Mitigation techniques

Range gate smearing smears a ghost object across the range dimension. Additionally one can employ binary phase encoding across transmitted chirps in a frame (i.e., each chirp is multiplied by a random binary phase (+/-1)). At the receiver this encoding is removed by multiplying each chirp with the corresponding binary phase. Since the binary code of the victim and interferer are assumed to be different, this ensures that the energy of the ghost object is spread across Doppler dimension. This not only prevents detection of ghost object (if a detection algorithm such as 2D-CFAR is used), but also gives an additional reduction in the interference induced noise floor by $1 0 \log _ { 1 0 } N _ { c h i r p s } .$ . This is a low-complexity interference mitigation technique and the results presented in the next sub-section include the effects of such binary encoding.

## D. Simulation Results

We performed Monte-Carlo simulations to assess the impact of multiple interferers. The goal was to characterize the performance of the victim radar in the presence of $N _ { i }$ interferers. All the radars had the same nominal chirp configuration, frame time $( T _ { f } )$ and update rate $( T _ { u } )$ No synchronization was assumed between the radars (update intervals were not aligned). Further each radar randomized its frame start time within its update interval. The phase noise is assumed to be -93dBc/Hz@1MHz and falling at the rate of 20dB/decade to a floor of -145dBc/Hz.

The simulations were performed as follows: For each run of the simulation, the timing of the various interferers w.r.t victim was randomly generated. The overlapping/in-band regions between the victim radar and the various interferers were identified. Both the effects discussed in Section IIB where incorporated while calculating the interference induced noise floor. The performance of the victim radar was characterized in terms of its capability to detect a car (RCS $5 \mathrm { m } ^ { 2 } )$ at different ranges with a CFAR detection threshold of 12dB. So a target was declared as undetected whenever the computed received signal power was less than the interference induced noisefloor+12dB. The signal parameters used in the simulation are listed in column titled ‘configuration $_ \mathrm { A } '$ in Table 1 below:

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Config A (Long RangeRadar LRR)</td><td rowspan=1 colspan=1>Config B(ShortRange Radar SRR)</td></tr><tr><td rowspan=1 colspan=1>Transmit Power</td><td rowspan=1 colspan=1>12dBm +20log10(3)</td><td rowspan=1 colspan=1>12dBm</td></tr><tr><td rowspan=1 colspan=1>Antenna Gain</td><td rowspan=1 colspan=1>10dB</td><td rowspan=1 colspan=1>5dB</td></tr><tr><td rowspan=1 colspan=1>Inter-chirp time (Tc)</td><td rowspan=1 colspan=1>20us</td><td rowspan=1 colspan=1>40us</td></tr><tr><td rowspan=1 colspan=1>Chirp Slope (S)</td><td rowspan=1 colspan=1>9.5 MHz/us</td><td rowspan=1 colspan=1>50 MHz/us</td></tr><tr><td rowspan=1 colspan=1>IF bandwidth</td><td rowspan=1 colspan=1>12.7 MHz</td><td rowspan=1 colspan=1>20MHz</td></tr><tr><td rowspan=1 colspan=1>Range Resolution</td><td rowspan=1 colspan=1>0.78m</td><td rowspan=1 colspan=1>7.5cm</td></tr><tr><td rowspan=1 colspan=1>Max range</td><td rowspan=1 colspan=1>200m</td><td rowspan=1 colspan=1>60m</td></tr><tr><td rowspan=1 colspan=1>Frame Time (Tf)</td><td rowspan=1 colspan=1> $\overline { { 5 \mathrm { m s } } }$ </td><td rowspan=1 colspan=1> $\underline { { 5 \mathrm { m s } } }$ </td></tr><tr><td rowspan=1 colspan=1>Update Period (Tu)</td><td rowspan=1 colspan=1> $2 0 \mathrm { m s }$ </td><td rowspan=1 colspan=1>20ms</td></tr></table>

Table 1: Chirp configurations used in this study

Fig. 7 shows the simulation results for the case of 20 interferers randomly distributed between 10m and 50m. We assume that 10m is a typical minimum distance in highway driving, and probability of line of sight reflection from ranges further than 50m is low. As can be seen the detection probability remains close to 90% up to about 140m. This is primarily because of the relatively low probability of the interferer falling in-band to the victim. The red line in Fig. 7 plots the predicted (range-independent) performance based on the simple model (given by eq(5)). Note that this model is able to accurately predict performance in the mid-ranges. The deviation (between simulation and eq(5)) at far ranges is because of the effects of phase-noise. At near-ranges the signal strength from the target is strong enough to be above the interference induced noise floor.

Note: The ‘probability of detection’ in Fig. 7,9,14 should be interpreted as the probability that the SNR of the target is greater than the CFAR detection threshold (12dB). The missed detection and false alarm rates associated with this threshold apply.

![](images/75ce6e2704740d0c8285461f798ab83967502562b5b5bee482fee0802ea4b4d4.jpg)  
Fig. 7: Prob of Detection vs range (Parallel Interferers)

## III. SWEEPING INTERFERER

In the previous section both the victim and interfering radar had the same nominal signal configuration. In this section we study the scenario where the victim and the interfering radars have different chirp configurations – specifically widely differing chirp slopes. This can happen for e.g. when an SRR interferes with an LRR (the SRR typically having a higher range resolution and thus a higher slope compared to the LRR).

![](images/3a78bcb900ddbea5609f271b446f5dfc2552f80da66507b815e127851af157dd.jpg)  
Fig. 8: Sweeping Interferers

We saw in Section II that the probability of interference in the case of parallel interferers eq(1) is given by the ratio of the delay to the furthest object to the chirping period and is typically a small number (ranging 0.5-5%). As shown in the Appendix, the probability of interference in the case of sweeping interferers is given by the ratio of the difference in slopes between the interferer and the victim to the slope of the interferer. Typical values for this probability are fairly high (60-80%). However, as depicted in Fig. 8 (left) a crossing interferer is typically in-band to the victim only for a small fraction $( T _ { i n t } )$ of the chirp duration $( T _ { c } )$ . This shows up as a temporary glitch in the time domain. This noise energy subsequently spreads across the entire range spectrum (after range processing) and across the entire range-Doppler spectrum (after range-Doppler processing). If $\mathbf { \nabla } ^ { \cdot } P _ { i }$ is the power of the interferer then the average interfering power (given by the average energy $P _ { i } T _ { i n t }$ divided by the observation time $T _ { c }$ ) is $\frac { P _ { i } T _ { i n t } } { T _ { c } }$ . Since this interferer is spread across the entire IF bandwidth, the corresponding Power Spectral Density (PSD) is $\frac { P _ { i } T _ { i n t } } { T _ { c } B _ { I F } } .$ . Accounting for a processing gain of the range-FFT (integration interval of $T _ { c } ) .$ , gives us the integrated noise in a single range bin as $\begin{array} { r } { \sigma _ { i } ^ { 2 } = \frac { P _ { i } \overline { { T } } _ { i n t } } { T _ { c } ^ { 2 } B _ { I F } } . } \end{array}$ In the presence of multiple interferers the noise contributions are combined as below:

$$
\begin{array} { r } { \sigma _ { i } ^ { 2 } = \frac { \Sigma _ { \mathbf { k } } P _ { i , k } T _ { i n t , k } } { T _ { c } ^ { 2 } B _ { I F } } , } \end{array}\tag{6}
$$

where $P _ { i . k }$ ?????? $T _ { i n t , k }$ are resp. the Power level and interference duration of the $k ^ { \mathrm { t h } }$ interferer.

## A. Simulation Results

We performed Monte-Carlo simulations. The set-up was similar to the one described in Section IID except that the chirp configuration of the victim radar and the interfering radar now differ. The victim radar retains the configuration of Table 1(config A) while all the interfering radars have the chirp configuration of Table 1 (config B).

![](images/145d8b080d12106f67bf2fa6a5ac511a6806a2448eda70a45c4e7b08d236dc79.jpg)  
Fig. 9: Prob of Detection vs range (Sweeping Interferers)

Fig. 9(red curve) shows the results for the case of 20 interferers randomly distributed between 10m and 50m. Beyond a certain range, the noise floor induced by the sweeping interferer prevents target detection. Consequently, (and unlike Fig. 7 for parallel interferers) there is a range threshold beyond which performance quickly drops. However, as noted earlier and depicted in Fig. 8 (left), the interference of a sweeping interferer is localized in time. Therefore it is possible to detect spikes of energy in the time domain ADC samples to localize the interferer, zero out the offending samples and then interpolate across them [8]. The results of such a strategy are shown in Fig. 9(blue curve). Note that in the absence of any mitigation scheme the detection probability falls to below 90% for a target beyond 100m. With this simple localization and interpolation strategy, the 90% detection probability extends to a target up to 170m.

## IV. REAL VS COMPLEX BASEBAND ARCHITECTURES

In this section we discuss the interference mitigation benefits of a complex base-band architecture compared to a ‘real-only’ architecture. The benefits of a complex base-band architecture in interference detection have already been described in [14]. Here we limit ourselves to comparison of raw performance in the presence of interference (without any mitigation scheme).

In a complex base-band architecture the signal band consists of only positive frequencies, while in a real-only architecture the signal band consists of both positive and negative frequencies. In the case of parallel interferers this translates to a doubling in the probability of interference events. This is depicted in Fig. 10(with the grey areas depicting the interference prone regions).

![](images/86a8b8597faf9b48e18e6cb63a913ae3fc0e5a5051472e54c4f0981a8503b462.jpg)

![](images/f01e51dd71af353497a749138d78323444e03d8af0b8cea72147fe35afcd9c1f.jpg)  
Complex architecture  
Real-only architecture

Fig. 10: Interference regions for real and complex architectures  
![](images/9350be15c1e51d7107f2d7536b48d6c0dcbb30d1d5f193d298eaf0d55b96f708.jpg)  
Fig. 11: Probability of no-interference for real-vs-complex

The probability analysis of parallel interferers in Section II was done assuming a complex baseband architecture. Fig. 11 contrasts this with the eq(3-5) suitably modified for a real-only chain. As can be seen the performance gap increases with increase in the number of interferers.

In the case of sweeping interferers, the probability of interference remains approximately the same (and given by eq(A3)) in both architectures However, the duration of interference doubles (Fig. 12). This results in a doubling of the interference induced noise floor (3dB). Since the received radar signal strength fall as the 4th power of the range, this results in a reduction of max range to 84% of original.

![](images/65dd92013ac7a86f0369d22df992a26473d6be3f94cd63e07d3b24cf9d868794.jpg)

![](images/752365724e444e7067354703d8d6558f8cff2f84828d0b17c40eadafcfc415f8.jpg)  
Fig. 12: Duration of interference for real-vs-complex

## V. PMCW TO PMCW INTERFERENCE

PMCW radar [10] is modulation scheme in which a transmitted signal consists of a pseudorandom binary code modulated on top of the carrier tone. The received signal (reflected from targets) is down-converted and correlated with the known transmit code. Such a correlation produces peaks corresponding to targets, the location of the peaks corresponding to the round trip delay to the target. An interferer will have a different binary code – and thus correlation of an interfering signal at the receiver will result in an increased noise floor arising due to the spreading of the interferer energy across the range-Doppler space. In a PMCW radar, the bandwidth of the transmit signal is determined by the chipping rate of the binary code. The ADC sampling rate at the receiver is also commensurate with this chipping rate. Thus unlike in an FMCW radar, the IF bandwidth of a PMCW radar is the same as its RF bandwidth.

Fig. 13 depicts two PMCW frames (victim and interferer) each with a frame period $T _ { f }$ overlapping for a duration $T _ { i n \mathrm { t \cdot } }$ Let the interferer power be ${ \dot { P } } _ { i } .$ The average interfering power is $\frac { P _ { i } T _ { i n t } } { T _ { f } }$ . Since this power is spread uniformly across the bandwidth $( B _ { R F } ) _ { : }$ , the resulting PSD of the interference induced noise is $\frac { P _ { i } T _ { i n t } } { T _ { f } B _ { R F } }$ The integrated noise, after accounting for the processing gain due to coherent integration across a frame is $\begin{array} { r } { \sigma _ { i } ^ { 2 } = \frac { \mathbf { \bar { \rho } } _ { P _ { i } T _ { i n t } } } { T _ { f } ^ { 2 } B _ { R F } } } \end{array}$ . In the presence of multiple interferers, the corresponding contributions can be summed up (similar to eq(6) of Section III).

![](images/57dbf09c283ad33259da2c5ab38cfce7fc799eefc65b5a1d71bdf0739e5c04be.jpg)  
Fig. 13: PMCW to PMCW Interference

Section II presented the results of simulations which characterized FMCW performance in the presence of $N _ { i }$ interferers, the victim and the interferer sharing the same nominal chirp configuration. In this section we repeat a similar characterization of co-existence with PMCW radars. The PMCW radars have the same transmit power, antenna gain , frame time and update period as described in Table 1 (config-A). Additionally all the PMCW radars have an RF bandwidth (and ADC sampling rate) of 2Gsps, since this seems like the current state of art sampling rate of PMCW radars [10]. The results are plotted in the graph of Fig. 14. There is 100% detection up to a certain threshold range, beyond which the detection probability quickly drops to zero. Notice that this curve looks almost identical to the curve for sweeping FMCW interferers without any mitigation (red curve in Fig. 14 reproduced from Fig. 9). This is expected since in both cases the interfering signal is spread and appears as a noise-floor across the entire range-Doppler bin. However, this is very unlike the performance of FMCW in the presence of parallel interferers (cyan curve in Fig. 14 reproduced from Fig. 7), where the detection probability is significant even at maximum range.

![](images/7d01996f5fb11f9181a35b758318ccb71e13ff42f51244be0be11e58cd4fcd0a.jpg)  
Fig. 14: Prob. Of detection vs Range (PMCW)

## VI. CONCLUSIONS AND FUTURE WORK

We presented analysis and simulations to characterize the performance of FMCW radars in the presence of multiple interferers. The simulations considered multiple interferers at randomized distances from the victim radar. We considered two categories of interferers: Parallel and Sweeping. Parallel interferers are low probability events, though the duration of each interference event is long. We demonstrated that in such situations the detection even at maximum range does not drop drastically (Fig. 7). In the case of Sweeping interferers, the probability of interference is relatively high. However, the interfering signal remains in-band only for a short duration and hence is easy to localize and repair. This minimizes the loss in probability of detection at maximum range (Fig. 9). We also presented simulation results for corresponding scenarios for PMCW radar (Fig. 14). Additionally the paper also discussed the statistical advantages of complex base-band architecture for interference mitigation.

FMCW radars typically have a low IF-to-RF bandwidth ratio. This not only reduces complexity (ADC sampling rate, processing power) but, as demonstrated in this paper, helps limit degradation due to interference. Future work includes broadening the characterization platform to include interferers in the continuum between parallel and sweeping.

## APPENDIX

Fig. 8 shows a interfering chirp $\mathrm { ( s l o p e = } S _ { i } )$ and a victim chirp (slope= S ) of duration $T _ { c } .$ The interferer has a timeoffset of to with respect to the victim. The instantaneous frequency (f<sub>i</sub> and $f _ { \nu } )$ vs time of the two chirps can be described by the two lines:

$$
\begin{array} { c } { { f _ { v } = S _ { v } t ; 0 < t < T _ { c } , } } \\ { { f _ { i } = S _ { i } ( t - t _ { o } ) ; t > t _ { o } . } } \end{array}\tag{A1}
$$

(A2)

The point of intersection of the two lines is $t _ { i n t e r s e c t } =$ $S _ { i } t _ { o } / S _ { \varDelta }$ , where $S _ { \varDelta } = S _ { i } - S _ { v } . \mathrm { ~ A ~ }$ valid interference event occurs whenever $0 < t _ { i n t e r s e c t } < T _ { c }$ . Using (A1,A2) we can then conclude that interference occurs whenever $0 < t _ { o } <$ $\frac { T _ { C } S _ { \varDelta } } { S _ { i } }$ . Assuming the interference event to be randomly distributed in $[ 0 , T _ { c } ]$ , the probability of interference is then given by:

$$
\begin{array} { r } { p _ { i } = \left( \frac { T _ { c } S _ { \Delta } } { S _ { i } } \right) / T _ { c } = \frac { S _ { \Delta } } { S _ { i } } . } \end{array}\tag{A3}
$$

## ACKNOWLEDGMENT

The authors thank Karthik S, Karthik R and Brian G for in-depth technical discussions and reviews that helped shape this paper.

## REFERENCES

[1] S. Alland, W. Stark, M. Ali and M. Hegde, "Interference in Automotive Radar Systems: Characteristics, Mitigation Techniques, and Current and Future Research," IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 45-59, Sept. 2019.

[2] M. Goppelt, H. -. Blöcher and W. Menzel, "Analytical investigation of mutual interference between automotive FMCW radar sensors," 2011 German Microwave Conference, Darmstadt, 2011, pp. 1-4.

[3] G. M. Brooker, "Mutual Interference of Millimeter-Wave Radar Systems," IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170-181, Feb. 2007.

[4] J. Bechter and C. Waldschmidt, "Automotive radar interference mitigation by reconstruction and cancellation of interference component," 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), Heidelberg, 2015, pp. 1-4.

[5] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein and J. Dickmann, "A method for interference cancellation in automotive radar," 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), Heidelberg, 2015, pp. 1-4.

[6] M. Toth, P. Meissner, A. Melzer and K. Witrisal, "Performance Comparison of Mutual Automotive Radar Interference Mitigation Algorithms," 2019 IEEE Radar Conference (RadarConf), Boston, MA, USA, 2019, pp. 1-6.

[7] T. Schipper, M. Harter, L. Zwirello, T. Mahler and T. Zwick, "Systematic approach to investigate and counteract interferenceeffects in automotive radars," 2012 9th European Radar Conference, Amsterdam, 2012, pp. 190-193.

[8] MOSARIM: “Recommendations on sensor design, mounting and operational parameters to minimize radar interference”, Report dated 6.12.2012.

[9] A. Bourdoux, K. Parashar and M. Bauduin, "Phenomenology of mutual interference of FMCW and PMCW automotive radars," 2017 IEEE Radar Conference (RadarConf), Seattle, WA, 2017, pp. 1709- 1714.

[10] A. Bourdoux, U. Ahmad, D. Guermandi, S. Brebels, A. Dewilde and W. Van Thillo, "PMCW waveform and MIMO technique for a 79 GHz CMOS automotive radar," 2016 IEEE Radar Conference (RadarConf), Philadelphia, PA, 2016, pp. 1-5.

[11] C. Aydogdu, N. Garcia, L. Hammarstrand and H. Wymeersch, "Radar Communications for Combating Mutual Interference of FMCW Radars," 2019 IEEE Radar Conference (RadarConf), Boston, MA, USA, 2019.

[12] K. Hahmann, S. Schneider and T. Zwick, "Evaluation of probability of interference-related ghost targets in automotive radars," 2018 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), Munich, 2018, pp. 1-4.

[13] C. Iovescu, S. Rao, “Fundamentals of mm-wave sensors”, Texas Instruments white paper (available on ti.com)

[14] S. Murali, K. Subburaj, B. Ginsburg and K. Ramasubramanian, "Interference detection in FMCW radar using a complex baseband oversampled receiver," 2018 IEEE Radar Conference (RadarConf18), Oklahoma City, OK, 2018, pp. 1567-1572.