# An MTI-Like Approach for Interference Mitigation in FMCW Radar Systems

LUIS A. LÓPEZ-VALCÁRCEL iD , Graduate Student Member, IEEE MANUEL GARCÍA SÁNCHEZ , Member, IEEE Universidade de Vigo, Vigo, Spain

D OLEG A. KRASNOV

TU Delft, Delft, The Netherlands

Mutual interference between automotive frequency-modulated continuous-wave (FMCW) radar systems has been a concern over recent years. Several interference mitigation (IM) techniques have been proposed to mitigate this phenomenon, which is deemed to grow in severity as more systems are deployed on the road. In this article, an inexpensive technique, based on well-known moving target indicator (MTI) processing, is proposed to separate interference from target signals. It exploits the contrast after stretch processing between uncorrelated FMCW interference (sparse and chirp-like) and beat signals (stable sinusoids). The interference is therefore marked and subtracted. This eliminates interference at the cost of introducing a distortion dependent on the relative radial velocity of the targets. To validate the proposed approach, called MTI-IM, numerical simulations and experiments with commercial-grade radars have been performed, with comparisons between MTI-IM and other IM techniques.

Manuscript received 4 July 2023; revised 17 October 2023; accepted 15 December 2023. Date of publication 21 December 2023; date of current version 12 April 2024.

DOI. No. 10.1109/TAES.2023.3345263

Refereeing of this contribution was handled by D. Pastina.

This work was supported in part by the Spanish Government, Ministry of Science and Innovation under Grant PID2020-112545RB-C52; in part by the Xunta de Galicia under Grant ED431C 2019/26 and Grant ED481A-2020/049(cofunded by the European Social Fund) and in part by the European Regional Development Fund.

Authors’ addresses: Luis A. López-Valcárcel and Manuel García Sánchez are with the Atlanttic Research Center, Universidade de Vigo, 36310 Vigo, Spain, E-mail: (lulopez@uvigo.es; manuel.garciasanchez@uvigo.gal); Francesco Fioranelli and Oleg A. Krasnov are with the Microwave Sensing, Signals and Systems (MS3) Group, Department of Microelectronics, TU Delft, Delft 2628, The Netherlands, E-mail: (F.Fioranelli@ tudelft.nl; o.a.krasnov@tudelft.nl). (Corresponding author: Luis A. López Valcárcel.)

This article has supplementary downloadable material available at https://doi.org/10.1109/TAES.2023.3345263, provided by the authors.

Results show good capabilities to fight the uncorrelated interference coming from more than one interfering radar. This is achieved at reduced computational cost, which is a key limiting factor in automotive systems.

## I. INTRODUCTION

Radar systems are routinely used in automotive, leveraging on their robustness in bad weather and low optical visibility conditions [1]. The conventional modulation scheme for automotive radars is frequency-modulated continuouswave (FMCW) [2], [3], [4]. With its dechirping operation, FMCW enables to use at the receivers analog-to-digital converters (ADCs) in the range of several Ms/s for transmitted radio frequency (RF) bandwidths of up to 4 GHz [5]. Furthermore, these sampling frequencies present advantages in terms of energy consumption and heat dissipation in comparison with higher rates.

Sharing bandwidth and time asynchronously, different automotive radar systems may produce mutual interference, an increasingly important issue as the number of vehicles equipped with radar increases as well as the number of radar sensors on each vehicle [6], [7]. Therefore, interference mitigation (IM) techniques for automotive radars have been investigated from multiple perspectives [8], [9], [10]. Despite a number of techniques having been proposed [2], [3], [7], [11], there is no standard, established approach that is applied in practical scenarios.

In this work, a simple yet effective IM signal processing approach is proposed. It aims at recreating and subtracting the interference signals from the beats. The proposed approach is inspired by classical moving target indication (MTI) processing, but aims in this work at isolating the uncorrelated interference in the received signals in the time domain. The technique, named MTI-IM onward, aims to achieve minimal computational cost, thereby offering a crucial advantage for automotive radar systems, which are typically complexity and cost driven. MTI-IM has an aggressive approach to mitigate interference, rendering a good suppression of the interference-induced noise floor. The performance of this is nearly perfect in scenarios with low radial velocity, but presents some form of degradation with its increase. Despite this degradation, we show that the proposed algorithm still outperforms other alternatives for velocities up to 80% in several useful automotive scenarios.

This article is organized as follows. In Section II, a literature review is given in order to provide less familiar readers with a quick glance at the state of the art in automotive radar IM. Section III describes the signal model for both desired and interfering chirp-sequence FMCW signals. MTI-IM is introduced in Section IV, with its specific advantages and drawbacks. A simulation framework is presented in Section V to compare MTI-IM with alternative techniques. Measurement results are shown in Section VI. Finally, Section VII concludes this article.

## II. STATE-OF-THE-ART

The multitude of IM techniques proposed during the recent years can be classified by their principles of © 2023 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/

operation. For instance, system level approaches include the strategic use of different operating parameters (frequency, time, polarization) or specific sets of waveforms in order to separate transmissions from different radars. Some of these strategies suggest the coordination between different radars so that conflict is avoided by dynamically adjusting those parameters. These coordination schemes can be either centralized [12], [13] or distributed [14], [15], [16]. More recently, Blasone et al. [17] have proposed the idea of using passive radars aboard vehicles in order to avoid mutual interference.

Related to system level approaches, waveform approaches include phase-modulated continuous wave [18], [19], [20], [21], [22], [23], [24] and orthogonal frequency division multiplexing schemes [25], [26], [27], [28]. Research lines exist that aim to combine the advantages of phase codes with those of FMCW, resulting in phase-coded FMCW systems [29] or the frequency shift keying-linear FMCW [30]. Some of the aforementioned approaches are also exploited for RadCom [31], [32], [33], [34], [35]. Other system level approaches make smaller modifications to the baseline FMCW waveform by varying the starting frequency of the sweep [36], [37], [38], [39] or the sweep repetition interval (SRI) [37], [40].

Signal processing approaches that do not impose changes to the classic FMCW architecture (chirp transmission + stretch processing at receiver) exist as well. These are implemented in one or more stages of the reception chain: just after sampling, after the first discrete Fourier transform (DFT) (typically range domain), after the second DFT (typically Doppler/velocity domain). A common idea is to first detect the interference in the time domain and then nullify the affected samples [6]. This is called zeroing and is often used as a baseline for comparison [41], [42], [43], [44], [45]. Smoothing the nullified samples with some form of simple windowing improves the applicability of this approach [46], although better performance is achieved with reconstruction methods such as the iterative method with adaptive threshold (IMAT) [47]. Other reconstruction methods include [48], [49], [50], [51], and [52]. Methods that focus on the detection stage include [53], [54], [55], [56]. In [43], constant false alarm rate (CFAR) was used in order to detect the uncorrelated interference in the STFT domain, followed by three mitigation options: zeroing, amplitude correction, and Burg-based interpolation.

Other alternative signal processing methods include separating signal and interference through the use of different transforms [57], [58], [59], the adaptive noise cancelling (ANC) of [60] and digital beamforming [61], [62], [63]. Techniques to parametrize, recreate, and subtract the interfering signal have been also proposed as in [64], [65], and [66]. Deep learning approaches have also been researched to mitigate interference [67], [68], [69], [70], [71].

MTI-IM, the technique proposed in this article, aims at recreating and subtracting the interference signals from the beats but, in contrast with [64], [65], and [66], it does not rely on any kind of parameterization. This eases implementation and computational costs while achieving satisfactory IM performances, as it will be seen in the following sections.

## III. SIGNAL MODEL

Let us assume a classic FMCW radar chirp waveform. A single sweep takes the following form:

$$
s _ { t } \left( t \right) = e ^ { j 2 \pi \left( f _ { c } t + \frac { S } { 2 } t ^ { 2 } \right) } , \ 0 \leq t < T _ { c }\tag{1}
$$

where $f _ { c }$ is the starting frequency of the sweep, $T _ { c }$ is its duration, and S is the slope $B / T _ { c }$ , with B the occupied bandwidth. Its amplitude has been considered to be 1. In a chirp-sequence (i.e., fast-ramp) FMCW radar, a train of multiple copies of (1) are transmitted with a given sweep repetition interval (SRI, T<sub>r</sub>). A sequence of $N _ { c }$ sweeps is called a burst (or train) and occupy a coherent processing interval (CPI). Each of the K objects in the radar’s field of view will reflect back each sweep of the burst with specific amplitude $a _ { k }$ and delay $\tau _ { k }$ so that: $s _ { r , e , k } ( t ) = a _ { k } \exp \{ j 2 \pi [ f _ { c } ( t - \tau _ { k } ) + { \cal S } / 2 ( t - \tau _ { k } ) ^ { 2 } ] \}$ The dechirping process, also called stretch processing, consists of mixing the received signals with a complex conjugated replica of the transmitted one. This produces the so-called beat signal that can be written for a burst of $N _ { C }$ sweeps in the form

$$
\begin{array} { r l } & { s _ { b , e } \ ( m T _ { r } , t ) = s _ { t } ^ { * } \left( t \right) \cdot s _ { r , e } \ ( m T _ { r } , t ) } \\ & { = \displaystyle \sum _ { k = 1 } ^ { K } a _ { k } e ^ { - j 2 \pi \left( f _ { c } \tau _ { k } ( m T _ { r } ) - \frac { S } { 2 } \tau _ { k } ^ { 2 } ( m T _ { r } ) + S \tau _ { k } ( m T _ { r } ) t \right) } } \end{array}\tag{2}
$$

where $m \in [ 0 , N _ { C - 1 } ]$ is the position of the sweep within the burst sequence, $T _ { r }$ is the sweep repetition time that is equal to the sum of $T _ { c }$ and any kind of idle time between sweeps and, thus, $m T _ { r }$ is the starting instant of each sweep. This way, (2) includes the dependence of the beat signals with both fast time (t ) and slow time $( m T _ { r } )$ . Note that the components of the beat signal (2) are complex sinusoids with constant frequency $S \tau _ { k } ( m T _ { r } )$ within a sweep. This frequency is directly dependent on the distance between radar and target through $\tau _ { k } ( m T _ { r } ) \ : = \ : 2 d _ { k } ( m T _ { r } ) / c$ , being c the speed of light. As the target moves with radial velocity $v _ { k } , \tau _ { k }$ varies from received sweep to received sweep. Under the stop-and-hop assumption [72], the variation of $\tau _ { k }$ between sweeps follows the form $\tau _ { k } ( ( m + 1 ) T _ { r } ) - \tau _ { k } ( m T _ { r } ) ~ = ~ 2 v _ { k } T _ { r } / c$ . If we assume that target movement is small in $T _ { c }$ with respect to the frequency resolution, its effect is negligible within a sweep. Nevertheless, from chirp to chirp, the phases of the sinusoids in (2) will change. If the variation of $v _ { k }$ is small within a burst, this phase shift will be approximately linear and define the associated with the kth target Doppler frequency.

The samples of a full CPI are arranged in an $N _ { S } \times N _ { C }$ matrix, where $N _ { S }$ is the number of samples per chirp or pulse and $N _ { C }$ the number of chirps per burst. Then, FFTs are applied across both dimensions of the matrix generating a so-called range-Doppler (RD) matrix with spectral peaks that appear at the range positions and radial velocities of the targets. To detect them, the CFAR algorithm can be employed [73]. In case of multiple-input multiple-output (MIMO) radar with $N _ { c h }$ channels, the phases of the peaks in the RD map can be used to estimate the direction of arrival (DoA) of the echo. The addition of the angular information converts in such a radar the 2-D signal matrix to the 3-D signal $N _ { S } \times N _ { C } \times N _ { c h }$ cube.

Besides the useful echoes present at the FMCW radar receiver, the received signal may also contain interference coming from other FMCW radars in the same frequency band. The interfering power may be significant in comparison with the useful echoes [6]. Nevertheless, as the interfering radar has its own set of parameters $S _ { i } , f _ { c , i } , T _ { c , i } ,$ and $T _ { r , i ; }$ , the behavior of interferences within the beat signal domain is, in general, different. In contrast with (2), the interfering signal $s _ { b , \mathrm { i n t } }$ does not consist, in general, in the sum of harmonic beat signals. Instead, we get a sum of other chirp-like waveforms, one per interference [74]. The slopes of these chirps are governed by the difference between the slopes of victim and interfering radars $( S - S _ { i } ) / 2$ . When it is not equal to zero, the interference is uncorrelated. Also considering receiver noise, $n ( t )$ , the resulting beat signal at the ADC input can be written as follows:

$$
\begin{array} { c } { { s _ { b } \ ( m T _ { r } , t ) = [ s _ { b , e } \ ( m T _ { r } , t ) + s _ { b , \mathrm { i n t } } \ ( m T _ { r } , t ) } } \\ { { { } } } \\ { { { } + n \ ( m T _ { r } , t ) ] \ * h _ { \mathrm { a f } } \ ( t ) } } \end{array}\tag{3}
$$

where $h _ { \mathrm { a f } } ( t )$ is an anti-aliasing filter placed just before the ADC. This filter limits the frequency swept by the uncorrelated interference at the receiver side and, therefore, suppresses it during most part of the sweep time. An example of a sweep in the presence of two interferences can be seen in Fig. 1(a). This figure shows the RF frequency variation with time of the transmitted chirp in solid blue line and the receiver filter limits in dashed lines, altogether with two interfering chirps in solid yellow and orange lines, respectively. As we are multiplying the received signal by a copy of the transmitted chirp before filtering [see (2)], it is, virtually, as if our effective filter of a few MHz is sweeping the radar passband synchronously to the transmitted chirp. The interference will appear in the baseband when the frequencies of the interfering and victim radars match. After downconversion, we obtain the spectrogram of Fig. 1(b) [see (3)], where it is shown how the instantaneous frequencies that are present in the received signal evolve with time. In the presented case, eight moving point-like targets and two independent interferers were simulated. The target-related beat signals can be seen in this plot as straight horizontal lines, while two interferences are seen as frequency-varying components (i.e., sweeps) that are cut from top and bottom by the antialiasing filter.

As both radars continuously transmit sweeps, the instantaneous frequency of the interference may fall into the receiver bandwidth often within a single burst or several consecutive ones. An example of an interfered CPI can be seen in Fig. 2, which is the full burst from where the sweep for the Fig. 1 was taken $( m = 1 2 , 0 . 7 8 \mathrm { m s } )$ . As can be seen in Fig. 2(a), where a 2-D (fast time–slow time) matrix of the beat signals’ amplitudes for the whole CPI is presented, the interferences take the form of short, high-power pulses in the time domain. In Fig. 2(b), the RD map of this CPI is displayed, and it can be compared with the interference-free version of the CPI in Fig. 2(c). It clearly demonstrates the impact of uncorrelated interferences on the noise floor.

![](images/86df3a5ce8f8c8c2d6ac5ecef241632eed10cc99ec0c0cc14335873c6d03b6ba.jpg)  
(a)

![](images/4d7f45bb744e1aaba25e5e5557aadbb1017652bc204c3bca35d4afd615080b62.jpg)  
(b)  
Fig. 1. Example of an interfered sweep. (a) shows a sketch of the RF sweep in the passband (77 GHz) and (b) shows the baseband spectrogram of the resulting beat signal.

If the slope of an interfering system matches to that of the victim radar (i.e., correlated interference), spurious beat signals are introduced instead of a sweeping interference [75]. These signals are not as clean as those originated by the own radar, due to the uncorrelated phase noise of the different hardware systems. They can, however, result in false alarms (i.e., ghost targets) after FFT processing. Nevertheless, the probability of this event is low [76]. In this work, only the uncorrelated interference (i.e., interference with different slope than the victim radar) is considered.

## IV. PROPOSED TECHNIQUE

## A. Technique Description

Consider the signal model described in Section III. The main objective of IM is to minimize the interference term while leaving the beat signals as unmodified as possible. By comparing (2) with the uncorrelated interference, we can see that the beats present a high stability in time in contrast to interference, which has a quick variation, sweeping around the whole receiver bandwidth. By taking the useful beats out of the mix, we can then detect the interference and subtract it from the original signal.

![](images/837a0b5925ebedcf438e57bcc28b4a714cd6e8e6862c9d22e006cf162a250da4.jpg)  
(a)

![](images/b071cd65e6e7e8ad1d8e80dcb04b0280db68cf6a05ec1eb50d4e36065fc7bc74.jpg)  
(b)

![](images/c57a4c1a427d16909ad74d548b266c2460074fff9d3282478e1862dc2ed8196d.jpg)  
(c)  
Fig. 2. Example of an interfered CPI. (a) shows the amplitude values in time domain; (b) shows its RD profile. In (c), the interference-free RD profile is shown for reference.

![](images/accb30e8c3a22cf6b9506b978733b930e0e75156b705059f4ea58b18faa1c22d.jpg)  
Fig. 3. Block diagram of the proposed technique.

In this work, we propose to exploit the sinusoidal nature of the beats to cancel them and, thus, isolate the interference. After dechirping and low-pass filtration, the uncorrelated FMCW interference is sparse in time, as well as quickly varying. In comparison, given the relative stability of the beats between adjacent chirp periods, the subtraction of adjacent ramps may lead to a signal where the echo content gets greatly diminished. In this resulting signal, the interference will remain comparatively untouched. This makes easier to point out interfered samples. This process is reminiscent to the idea behind classic MTI processing, used to separate useful targets from static clutter. After detecting interference in the resulting signal, the corresponding samples can be subtracted from the original ramp. This will mitigate interference at the cost of a varying distortion of the beat signals in the interfered interval; this distortion will be characterized in the upcoming sections.

The resulting algorithm works with the following steps. In Fig. 3, a block diagram of the scheme is presented, with its correspondence to each of the following steps marked:

1) Subtract adjacent chirps, i.e., perform a sliding subtraction across the slow-time axis of a CPI,

as follows:

$$
\begin{array} { c } { { s _ { \mathrm { s u b } } \left[ n , m ^ { \prime } \right] = s _ { b } \left[ n , m ^ { \prime } + 1 \right] - s _ { b } \left[ n , m ^ { \prime } \right] , } } \\ { { 0 \leq n \leq N _ { S } - 1 , \ 0 \leq m ^ { \prime } \leq N _ { C } - 2 . } } \end{array}\tag{4}
$$

2) The interference appears now in two consecutive columns of the matrix, creating an ambiguity. To solve this ambiguity, compare adjacent subtractions. The simplest way to automatize this is to take the absolute value of $s _ { \mathrm { s u b } }$ and to subtract again across columns. This new subtraction is done in both directions, forward and backward in slow time, so that interference in both the first and last chirps can be detected. This is shown in the following:

$$
s _ { \mathrm { s u b , b w } } \left[ n , m ^ { \prime \prime } \right] = \left| s _ { \mathrm { s u b } } \left[ n , m ^ { \prime \prime } + 1 \right] \right| - \left| s _ { \mathrm { s u b } } \left[ n , m ^ { \prime \prime } \right] \right| ,\tag{5}
$$

$$
\begin{array} { r l } & { s _ { \mathrm { s u b , f w } } \left[ n , m ^ { \prime \prime } \right] = \left| s _ { \mathrm { s u b } } \left[ n , m ^ { \prime \prime } \right] \right| - \left| s _ { \mathrm { s u b } } \left[ n , m ^ { \prime \prime } + 1 \right] \right| , } \\ & { \phantom { s s } 0 \leq n \leq N _ { S } - 1 , \ 0 \leq m ^ { \prime \prime } \leq N _ { C } - 3 . } \end{array}\tag{6}
$$

3) The resulting signals $s _ { \mathrm { s u b , b w } }$ and ${ \cal S } _ { \mathrm { s u b , f w } }$ are now aligned and combined. High positive values of these matrices represent samples where interference has occurred. Wherever both signals are available, a sample-by-sample maximum is taken. In the following, assume that the values of m where (5) and (6) are not defined are zero-padded:

$$
\begin{array} { r l r } & { } & { s _ { \mathrm { c o m b } } \left[ n , m \right] = \operatorname* { m a x } \left\{ s _ { \mathrm { s u b , f w } } \left[ n , m \right] , s _ { \mathrm { s u b , b w } } \left[ n , m - 2 \right] \right\} , } \\ & { } & { 0 \le n \le N _ { S } - 1 , \ 0 \le m \le N _ { C } - 1 . \ ( 7 ) \ } \end{array}
$$

4) A threshold is applied to $s _ { \mathrm { c o m b } }$ and samples above it are marked as interference. To obtain the threshold, we first compute the maximum value of each chirp of $s _ { b } ,$ obtaining a vector of $N _ { C }$ elements. Then, the threshold is set at a fixed distance between the minimum and maximum values of this vector. The value of 1/8 as the distance from the minimum value is empirically chosen, which is providing stable results in the performed study.

5) Finally, the values of $s _ { \mathrm { s u b } }$ in the marked locations are subtracted from $s _ { b }$ . This whole process is equivalent to replacing the interfered values of $s _ { b }$ with their equivalents of the adjacent ramp.

![](images/7fc63ccd039cfcbcffa064ccb5e05fe824fa8b0e298a732b4aaf2dede84fe4de.jpg)  
Fig. 4. Example of the proposed MTI-IM technique. (a) and (d) Real part and modulus of four consecutive chirps of the original signal. (b) and (e) Result of applying the first step of the technique over the signal in (a) and (d). (c) and (f) Second step of the technique, where we compare adjacent subtractions. (g) Interference threshold applied to the interfered chirp #12. (h) and (i) Recovered interference and the result of correcting the interfered chirp #12, compared with the simulated interference-free signal.

As an example, recall the interfered CPI shown in Section III. Its chirps 10 to 13 are represented in Fig. 4(a) and (d), with chirp #12 presenting two independent interferences. After applying the first step of MTI-IM, we obtain the signals in Fig. 4(b) and (e), where it is seen that the contrast between the interference and signal plus noise has been increased. The aforementioned ambiguity can be seen as well. The purpose of step 2 of the proposed algorithm is to solve this ambiguity by means of a comparison, which is shown in Fig. 4(c) and (g). By aligning and combining these two comparisons, we obtain a signal [see Fig. 4(g)] where the interfered samples are easier to isolate with respect to the original ones. The corresponding samples from $s _ { \mathrm { s u b } }$ can be used to repair the interfered chirp #12 by subtracting the isolated interference [see Fig. 4(h)], and then obtaining the corrected signal shown in Fig. 4(i). As a possible drawback of this approach, phase differences between consecutive returns from the same target will produce a distortion, discussed in the next section.

## B. Specific Drawbacks of MTI-IM

For the proposed MTI-IM approach, we must take into account that target velocity results in an imperfect cancellation of its beat signals. As such, when subtracting consecutive chirps the phase difference may result in echoes that are not totally cancelled or even amplified. This has two visible effects. The first one is a harder detection of interference, as the residual contribution from the subtracted beats makes it more difficult to isolate the interfered region of the signal. The second effect is a distortion in the interfered region after the interference has been subtracted from the signal. This is related to the phase difference between consecutive beats and may degrade the noise floor after both FFTs.

Considering the first step of the technique in (4), and the definition of a single beat from (2), let us obtain an expression of how the beat contribution of $S _ { \mathrm { s u b } } , S _ { \mathrm { s u b } , e }$ works. Assuming a series of chirps with period $T _ { r }$ and that $a _ { k }$ does not change from chirp to chirp, the samples of the kth target contribution, sampled with sampling frequency $f _ { s } ,$ are as follows:

$$
\begin{array} { r } { s _ { \mathrm { s u b } , e , k } \left[ n , m ^ { \prime } \right] = a _ { k } \ e ^ { j 2 \pi \left( \left( S \frac { n } { f _ { s } } + f _ { c } \right) \tau _ { k } \left[ m ^ { \prime } + 1 \right] - \frac { S } { 2 } \tau _ { k } ^ { 2 } \left[ m ^ { \prime } + 1 \right] \right) } } \\ { - a _ { k } e ^ { j 2 \pi \left( \left( S \frac { n } { f _ { s } } + f _ { c } \right) \tau _ { k } \left[ m ^ { \prime } \right] - \frac { S } { 2 } \tau _ { k } ^ { 2 } \left[ m ^ { \prime } \right] \right) } . } \end{array}\tag{8}
$$

The frequency $S \tau _ { k }$ will barely change from chirp to chirp. As such, we can neglect the changes in this term, meaning that

$$
\begin{array} { r } { s _ { \mathrm { s u b } , e , k } \left[ n , m ^ { \prime } \right] = a _ { k } \ e ^ { j 2 \pi \left( S \tau _ { k } \left[ m ^ { \prime } \right] n + f _ { c } \tau _ { k } \left[ m ^ { \prime } \right] - \frac { S } { 2 } \tau _ { k } ^ { 2 } \left[ m ^ { \prime } \right] \right) } } \\ { \cdot e ^ { j 2 \pi \varphi _ { \mathrm { d i s } , k } \left[ m ^ { \prime } \right] } 2 j \mathrm { s i n } \left( 2 \pi \varphi _ { \mathrm { d i s } , k } \left[ m ^ { \prime } \right] \right) } \\ { = s _ { b , e , k } \ \left[ n , m ^ { \prime } \right] \ } \\ { \cdot e ^ { j 2 \pi \varphi _ { \mathrm { d i s } , k } \left[ m ^ { \prime } \right] } 2 j \mathrm { s i n } \left( 2 \pi \varphi _ { \mathrm { d i s } , k } \left[ m ^ { \prime } \right] \right) } \end{array}\tag{9}
$$

with

$$
\varphi _ { \mathrm { d i s } , k } \left[ m ^ { \prime } \right] = \left( f _ { c } - S \tau _ { k } \left[ m ^ { \prime } \right] \right) \ \frac { T _ { r } v _ { k } } { c } - { \mathrm { S } } \left( \frac { T _ { r } v _ { k } } { c } \right) ^ { 2 }\tag{10}
$$

where the identity $\tau _ { k } [ m ^ { \prime } + 1 ] - \tau _ { k } \left[ m ^ { \prime } \right] = 2 T _ { r } v _ { k } / c$ has been used. This can be further simplified by substituting the velocity term by a fraction $\rho _ { k }$ of the maximum unambiguous speed [77] detectable by the radar

$$
\varphi _ { \mathrm { d i s } , k } \left[ { m ^ { \prime } } \right] = \left( { f _ { c } - S \tau _ { k } \left[ { m ^ { \prime } } \right] } \right) \ \frac { { \rho _ { k } } } { { 4 f _ { c } } } - S { \left( { \frac { { \rho _ { k } } } { { 4 f _ { c } } } } \right) ^ { 2 } } .\tag{11}
$$

After sampling, the product $S \tau _ { k } [ m ^ { \prime } ]$ will be bounded by the sampling frequency, which will always be far below $f _ { c } .$ On the other hand, S alone will always be greatly surpassed by $1 6 f _ { c } ^ { 2 }$ . Hence, these terms will be negligible compared with 2π. This aspect allows us to further simplify into $\varphi _ { \mathrm { d i s } , k } = \rho _ { k } \ / 4$ , where the dependence with m has disappeared

We can see that the subtraction produces a signal which is equal to our original beats, but with a modification in phase and amplitude dependent on $\varphi _ { \mathrm { d i s } }$ . The kth beat present in $S _ { \mathrm { { s u b } , \it { e } } }$ will be nullified when $\rho _ { k } = ~ 0$ . The simplest case is a completely static scenario $( \ v _ { k } = \ 0 , \ \forall k \in [ 0 , K - 1 ] )$ This is uncommon but can sometimes be approximated. For example, when vehicles are platooning, the relative velocity between radar and the main targets is almost equal. On the other hand, targets with velocities that are equal to the maximum unambiguous speed of the radar $( \mathrm { i . e . , ~ } \rho _ { k } = ~ 1 )$ will see their amplitude duplicated. Its desirable that $S _ { \mathrm { { s u b } , \it { e } } }$ is minimized as much as possible, leaving only interference in $s _ { \mathrm { s u b } }$

The greater the value of $s _ { \mathrm { s u b } , e } ,$ the less ideal will be the detection of interference, as discussed above. Moreover, the signal-to-noise-and-interference ratio (SNIR) after IM will be impacted as well. In the mitigation part, we are subtracting (9) (or, more precisely, the sum $\begin{array} { r } { \dot { \sum _ { k } ^ { K } } _ { 1 } s _ { \mathrm { s u b } , e , k } ) } \end{array}$ to (2) at interfered intervals. This is equivalent to adding a copy of each beat, with a different scaling factor and phase constant, multiplied by a rectangular window with duration equal to the interfered interval. After the range FFT, these windowed copies will introduce an amplitude and phase error in the target bins, which will be greater the longer the interfered interval. This error is not always destructive in the range profile, as it can produce higher target peaks (due to the possibility of coherent addition). Nonetheless, the inherent rectangular window will produce sidelobes which will always be detrimental for the SNIR. In the slow-time FFT, both these effects (target peak error, range profile sidelobes) are localized in the chirps which were interfered. This is very similar to the behavior of the interference-induced degradation, thereby causing an increase in the noise floor of the RD map. Due to beat signals being in general much fainter than interfering ones, this increase will not surpass the interference-induced noise floor. In case that the interference level is low enough such that this could happen, it will in general be masked by the terms in (9) and not marked by the technique. Hence, this postmitigation degradation will not apply in this case. Nonetheless, in general, the lower the modulus of (9), the more mitigation will be achieved.

TABLE I  
Victim and Interfering Radars Parameters
<table><tr><td>Parameter</td><td>Victim radar</td><td>Int. radars {1, 2}</td></tr><tr><td>Centre frequency [GHz]</td><td>77</td><td>77</td></tr><tr><td>Bandwidth [MHz]</td><td>1.2</td><td>1.2</td></tr><tr><td>Slope [MHz/µs]</td><td>20</td><td> $l o g \mathcal { U } ( 8 , 4 0 )$ </td></tr><tr><td>Chirp duration [μs]</td><td>60</td><td> $B _ { i } / S _ { i }$ </td></tr><tr><td>Idle time [μs]</td><td>5</td><td> $^ { 5 }$ </td></tr><tr><td>SRI [µs]</td><td>65</td><td> $B _ { i } / S _ { i } + 5 \mu \mathrm { s }$ </td></tr><tr><td>Sampling frequency [MHz]</td><td>10</td><td></td></tr><tr><td>Samples per chirp</td><td>512</td><td></td></tr><tr><td>Chirps per frame</td><td>128</td><td></td></tr><tr><td>Noise power [dBm]</td><td>{-20, 10, 0, 10, 20}</td><td></td></tr><tr><td>Signal power [dBm]</td><td>[-26, 0]</td><td> $\{ 2 2 , 2 6 , 3 2 \}$ </td></tr><tr><td>Arrival time [μs]</td><td></td><td> $\underline { { \mathcal { U } ( - T _ { P R I , i } , 0 ) } }$ </td></tr></table>

Another specific drawback of MTI-IM is related to the potential overlap of interferences when subtracting. If there are interfered regions in adjacent chirps that share overlapping sample indexes, the interference will not be properly mitigated. This might not only happen when there are multiple independent interferers. With a certain combination of parameters $( T _ { r , i } , T _ { c , i } ) _ { : }$ , a single interference can be present in the same samples of consecutive chirps. Note that this last drawback only affects interferences that share sample indexes across consecutive chirps. If the interference overlap happens in the same chirp, no issues are caused, as MTI-IM operates blindly (i.e., no parameterization of interference happens).

In spite of these drawbacks, the technique has good potential in a range of situations. Asynchronous nonperiodic interference is the most common type of automotive interference [75], so that the aforementioned overlap problem will not be a dominant issue. Furthermore, if the SRI is short enough, the velocity-induced degradation may not be as severe as to impede the usage of the technique. This, together with arguably low implementation and computational costs, which are key factors in automotive systems, make MTI-IM a candidate worth of consideration for automotive radar IM. The following sections will characterize its performance.

## V. NUMERICAL SIMULATIONS AND RESULTS

To demonstrate the performance of MTI-IM, a typical FMCW processor has been simulated. Echo signals, interference, and noise are generated at beat stage after sampling the signal described in (3) and assuming an ideal filter at stretch processing. Receiver noise has been considered an additive white Gaussian noise (AWGN) process with variance $P _ { n } .$ . The proposed technique is applied just before FFT-processing. Hanning windows are used for both FFTs. After that, a 2-D cell averaging CFAR (CA-CFAR) detector is applied over the range-Doppler map to detect the pointlike targets.

By using a Monte Carlo approach [78], it was possible to generate an arbitrarily high number of scenarios. The configuration of the Monte Carlo framework is depicted in Tables I and II. The guard cells of the CFAR detector are counted including both sides of the cell under test (CUT). Several parameters are fixed, meanwhile others are generated from random distributions (where means uniform). The decision of which parameters to generate randomly was taken considering the tradeoff between simulation complexity, required number of iterations for convergence, and interpretability of the results on one hand and statistical significance of the results on the other hand. A total of $3 { \cdot } 1 0 ^ { 5 }$ iterations were run per each combination of three parameters: noise power, maximum velocity of the targets, and number of interfering radars. The maximum velocity of the targets, $v _ { \mathrm { m a x } } ,$ is considered as a fraction of the maximum unambiguous speed detectable by the radar. This way, in each simulation, the targets can have a random speed between 0 m/s and a fraction of the maximum unambiguous radial velocity. This fraction is varied between 0 and 1 during the different simulations, progressively increasing the degradation.

TABLE II  
Targets and CA-CFAR Parameters
<table><tr><td colspan="2">Targets</td><td colspan="2">Detector</td></tr><tr><td>No of targets</td><td>8</td><td>Range guard cells</td><td>11</td></tr><tr><td>Initial range [m]</td><td> $\mathcal { U } ( 2 , 6 7 )$ </td><td>Velocity guard cells</td><td>5</td></tr><tr><td>Range [m]</td><td> $d _ { 0 , k } + v _ { k } * t$ </td><td>Range training cells</td><td>16</td></tr><tr><td>Velocity [m/s]</td><td> $\mathcal { U } ( - v _ { m a x } , v _ { m a x } )$ </td><td>Velocity training cells</td><td>16</td></tr><tr><td>RCS</td><td></td><td>False alarm probability</td><td>10-6</td></tr></table>

It should be noted that modeling realistic propagation conditions (e.g., RCS models, channel attenuation models) goes beyond the scope of these simulations. The amplitudes of the beats are generated from a uniform distribution (0.05, 1.00). This results in the presence of beat powers in the interval [–26, 0] dBm. The powers of the interferences follow two configurations: 1) interfering radar received with +32 dBm power and 2) interfering radars with +26 and +22 dBm power, respectively. Note that the total interfering power is inferior in the latter scenario. This has been designed so that the IM faces a situation with, in general, worse SNIR but easier to detect interferences, and another case with smoother spurious parts.

In the following section, the outputs of the Monte Carlo simulation are described. A list of techniques other than the proposed one is also given for comparison.

## A. Performance Metrics for Comparisons

Due to the number of iterations of the simulation, computation speed was prioritized in the selection of the compared techniques. The following techniques are compared:

1) MTI-IM.

2) Zeroing: In the current work, this technique uses the detection step of the proposal. It will thus be referred as MTI-Z.

3) ANC from [60]: The threshold is computed based in the noise variance. The LMS filter order was set as 80.

4) WD from [66]: The Haar wavelet with five levels of decomposition was used. The threshold was computed with the block James–Stein estimator.

5) IMAT from $I 4 7 ] \colon$ This is applied after zeroing. As such, it will be referred as MTI-IMAT. A maximum of six iterations was set.

In order to quantify the performance of the techniques, the following metrics are proposed, in a similar way to the following [79].

1) Signal-to-noise-and-interference ratio (SNIR): This measures the difference in power between the target signals and the combination of noise and interference. We can compute this metric by comparing the mean level of the expected peaks (target echoes) in the RD profile with the mean level of all the other bins. Let be the set of coefficients associated to target peaks in the range-Doppler (s<sub>RD</sub>) matrix. Then one can define SNIR as follows:

$$
\mathrm { S N I R } = 1 0 \mathrm { l o g } \frac { \sum _ { \{ n , m \} \in { \cal K } } \left| s _ { \mathrm { R D } } \left[ n , m \right] \right| ^ { 2 } / N _ { \cal K } } { \sum _ { \{ n , m \} \not \in { \cal K } } \left| s _ { \mathrm { R D } } \left[ n , m \right] \right| ^ { 2 } / \left( N _ { S } N _ { C } - N _ { \cal K } \right) } .\tag{12}
$$

2) Error vector magnitude (EVM): This measures how much the peaks are modified with respect to the reference signal, which in this case is the noise-andinterference-free RD profile. Noise, interference, and IM techniques might affect target peaks. Although in the current work we detect the targets in the range-Doppler matrix, the phase information of the peaks might be used to obtain angular information of the channel in MIMO radars. Therefore, this metric becomes relevant

$$
\mathrm { E V M } = \sqrt { \frac { \sum _ { \{ n , m \} \in K } \left| s _ { \mathrm { R D , r e f } } \left[ n , m \right] - s _ { \mathrm { R D } } \left[ n , m \right] \right| ^ { 2 } } { \sum _ { \{ n , m \} \in K } \left| s _ { \mathrm { R D , r e f } } \left[ n , m \right] \right| ^ { 2 } } } \ .\tag{13}
$$

3) Probability of detection: CA-CFAR is applied in the range-Doppler bins of the generated targets. Interference may mask some targets. An interesting result is the number of targets recovered after applying IM methods, in comparison with the interfered range-Doppler map.

4) Computational cost: As automotive radars must operate in real time, the computational delay that each IM technique imposes is a crucial performance aspect for their applicability.

## B. Results

1) SNIR: In Fig. 5, the median SNIRs obtained after applying the different techniques are shown. Alongside them, the SNR of the clean signal and the SNIR of the interfered one can be seen for reference. The plots of the left column show static scenarios, whereas the middle column shows scenarios with target velocities ranging from 0 m/s to the maximum unambiguous velocity of the radar. The plots on the right show the performance of the proposed technique for different values of the maximum allowed velocities, from 0 m/s to maximum unambiguous velocity.

(c)  
![](images/699326f1956a78cc3e55ea96ce260880103a8075b1f5d025eb212d2f9d00241d.jpg)

![](images/101d3adee8856d9e90268f915c581290c9566d4291178638a6919baf268299e6.jpg)

![](images/07f07097696cebdf690fa844f81c7f238d495e9161a2f18f123113cbe1166faa.jpg)

![](images/83f4ed7f01f48d852a90fd71f4c2ae6cb74967c24a5d45bed33308f79a57e5c7.jpg)  
(d)

![](images/0785d0fd929c266ff1df800b7164c46fe5d9924f362044b0d97c39dafde163d0.jpg)  
(e)

![](images/a5a9bf5ba40c97850f09dae5a3265bfc8c6f504c6b9374b26ba750bf1b108fe7.jpg)  
(f)  
Fig. 5. SNIR of the RD profile. (a)–(c) correspond to a single interferer, while (d)–(f) present two interfering radars. Furthermore, (a) and (d) compare clean signal, interfered signal, and corrected signal using MTI-IM, MTI-Z, ANC, WD, and MTI-IMAT in a static scenario. (b) and (e) show the same comparison of different IM techniques, but for full range of velocities from 0 m/s to the maximum unambiguous velocity. (c) and (f) compare the proposed MTI-IM for different velocities, indicated as a fraction of the maximum unambiguous velocity.

For the lowest values of the SNR, none of the considered IM methods provides a significant advantage. This is expected, as the degradation of the SNIR is completely dominated by noise power, instead of interference. As noise level decreases, differences appear and an upper limit can be seen in the SNIR of the interfered signals. ANC improves the SNIR, albeit by a small margin, especially in the scenario with multiple interferences. As happens with the interfered signal, an upper SNIR limit is discernible when noise power decreases, revealing significant remaining interference or distortion. This technique relies on the assumption that the frequency spectrum of the interference presents Hermitian symmetry, or at least a high degree of correlation between negative and positive side, which might not be the case for the simulated system.

WD achieves a better result than ANC, but this improvement shows an upper limit as well. Despite reducing interference, WD sometimes attenuates the signal of interest, reducing the peak value in the frequency domain. MTI-Z also reduces target peak levels in the RD maps. This reduction is directly proportional to interference duration. It also introduces spectral artefacts, but these are in general small compared to the interference. Despite these inconveniences, MTI-Z is achieving a noticeable correction. MTI-IMAT, which repairs the signal after zeroing, follows the baseline set by the clean signal almost perfectly. MTI-IM has the best performance in the static scenarios, but degrades quickly with increasing velocities, as anticipated in Section IV-B.

A comparison of the techniques against velocity can be seen in Fig. 7. There, only the results for two interferers have been plotted, as these followed the same trend as the one-interferer case. The plots, Fig. 7(a)–(c) show the SNIR; the plots, Fig. 7(d)–(f) will be discussed in the next section. Here, it can be seen how there are no significant differences for the cases with lower SNR [see Fig. 7(a)]. MTI-IM is the most affected technique when the SNR is good [see Fig. 7(c)], although it can outperform the simpler zeroing approach, at least until when the simulated target velocity is up to 80% the maximum unambiguous measurable speed.

2) EVM: Moving on to the EVM, the results are shown in Fig. 6. The same structure of the subfigures has been used as with the results of the SNIR in Fig. 5. As explained in Section V-A, the noise-and-interference-free signal has been used as a reference to compute this metric. This way, the value of the EVM for the signal labeled as “clean” corresponds to the error introduced by the noise alone.

As with the SNIR, no effect of interference or corrections can be appreciated for the highest simulated noise levels. The clean signal achieves the lowest values, following smoothly the decline in noise power. MTI-IM has the same behavior in the static scenarios, but quickly degrades with increasing velocities, as can be seen in Fig. 7(d)–(f). As with the SNIR, MTI-IM is less effective only around 80% of the maximum speed. Interestingly, in contrast with the SNIR case, some degradation in the performance of MTI-IMAT appears, but this is still very consistent and close to the baseline. ANC and WD present the worst results in the EVM aspect, with WD slightly outperforming ANC. This can be explained by the reasons stated in Section V-B1. It should be noted that, in the two interferences case, they worsen the EVM of the interfered signal. This implies that these attenuate the noise-and-interference floor, but they also increase the distortion of the peak value with respect to the interference, which could be harmful for a possible subsequent DoA estimation.

![](images/0c1e726906277ae452b9bb00b3a5af6425c8b38152eeaabcff64392501334c41.jpg)  
(a)

![](images/e77a6870b3e25de8ab32f20593d249e1b72bef0f16d6476d510cff20f4e67ad2.jpg)  
(b)

![](images/f4a9eb01acf4dd580ee30db5cd3eae4fec0aaf50a7d4152ca50ba35a884f5772.jpg)  
(c)

![](images/e1fab14a0266b48e9e1319c44e75531a22250cb4adf1e5035a749a2fde410ef7.jpg)  
(d)

![](images/9b4ff639b81f1dcf07d84dd6fec197d2218bcefd012259dbf2dc5afaa68653ab.jpg)  
(e)

![](images/2f70831775f679a49d4ace026cd7c6c0f7d29eb886ad11acf4692d87d0fd2bbc.jpg)  
(f)

Fig. 6. EVM of the target peaks in the RD profile. The same structure of the subfigures as in Fig. 5 has been used.  
![](images/6f2efc8433dc09035071d729e3f6aac2161cb79b0e6f03407a8b3ea8aea3c24a.jpg)  
(a)

![](images/fbe76f4e34a3e7babbce0ad29a8f859ccd6d3e46498e7c877fb837f3994c8f9e.jpg)  
(b)

![](images/3ab327ccfbab42d3b9aaf032169f3fd65685da2f93727849028088445a78968d.jpg)  
(c)

![](images/65d55d58d9b1385a3efaa4c533efc5640604db168203a86428f47dc4e71c97f3.jpg)  
(d)

![](images/92afc61dd97babf3e36c6dff1bf6afbf0d15ed7327a2e06b44b7ccab92dc43ff.jpg)  
(e)

![](images/77c40b7aecc4e06a6e22d7d4fc931b1cddbeeeb941b8141083cf5b22a05f497f.jpg)  
(f)  
Fig. 7. SNIR and EVM achieved with different techniques against velocity (2 interferers). (a)–(c) show the SNIR, (d)–(f) the EVM. (a) and (d) have a noise power of +20 dBm, (b) and (e) of 0 dBm, and in (c) and (f) the noise level was at –20 dBm.

3) Probability of Detection: Another important performance metric is the probability of detection of an existing target. In Table III, the ratios between generated and detected targets are listed for a single interferer. These are shown for the different IM techniques and levels of noise. Note that even in the interference-free scenario some targets are missed. For the situation with two interfering radars, the results shown in Table IV were computed. The detector described in Table II was used. All of these results correspond to scenarios where the maximum simulated velocity is equal to the maximum unambiguous velocity of the radar.

TABLE III  
Probability of Detection [%] (1 Interferer)
<table><tr><td rowspan=1 colspan=1> $\overline { { { P _ { n } } } }$ </td><td rowspan=1 colspan=5>20 dBm  10 dBm   0 dBm  -10 dBm -20 dBm</td></tr><tr><td rowspan=1 colspan=1>Clean</td><td rowspan=1 colspan=1>72.7</td><td rowspan=1 colspan=1>93.5</td><td rowspan=1 colspan=1>97.9</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr><tr><td rowspan=1 colspan=1>Interfered</td><td rowspan=1 colspan=1>70.9</td><td rowspan=1 colspan=1>88.9</td><td rowspan=1 colspan=1>92.2</td><td rowspan=1 colspan=1>92.5</td><td rowspan=1 colspan=1>92.5</td></tr><tr><td rowspan=1 colspan=1>MTI-IM</td><td rowspan=1 colspan=1>71.9</td><td rowspan=1 colspan=1>93.4</td><td rowspan=1 colspan=1>97.8</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr><tr><td rowspan=1 colspan=1>MTI-Z</td><td rowspan=1 colspan=1>72.0</td><td rowspan=1 colspan=1>93.4</td><td rowspan=1 colspan=1>97.9</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr><tr><td rowspan=1 colspan=1>ANC</td><td rowspan=1 colspan=1>70.4</td><td rowspan=1 colspan=1>91.9</td><td rowspan=1 colspan=1>96.9</td><td rowspan=1 colspan=1>97.3</td><td rowspan=1 colspan=1>97.3</td></tr><tr><td rowspan=1 colspan=1>WD</td><td rowspan=1 colspan=1>72.0</td><td rowspan=1 colspan=1>93.2</td><td rowspan=1 colspan=1>97.8</td><td rowspan=1 colspan=1>98.1</td><td rowspan=1 colspan=1>98.1</td></tr><tr><td rowspan=1 colspan=1>MTI-IMAT</td><td rowspan=1 colspan=1>71.9</td><td rowspan=1 colspan=1>93.5</td><td rowspan=1 colspan=1>97.8</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr></table>

TABLE IV

Probability of Detection [%] (2 Interferers)
<table><tr><td rowspan=1 colspan=1> $\underline { { P } } _ { n }$ </td><td rowspan=1 colspan=5>20 dBm  10 dBm   0 dBm   -10 dBm-20 dBm</td></tr><tr><td rowspan=1 colspan=1>Clean</td><td rowspan=1 colspan=1>72.7</td><td rowspan=1 colspan=1>93.5</td><td rowspan=1 colspan=1>97.9</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr><tr><td rowspan=1 colspan=1>Interfered</td><td rowspan=1 colspan=1>72.0</td><td rowspan=1 colspan=1>91.7</td><td rowspan=1 colspan=1>95.7</td><td rowspan=1 colspan=1>96.2</td><td rowspan=1 colspan=1>96.2</td></tr><tr><td rowspan=1 colspan=1>MTI-IM</td><td rowspan=1 colspan=1>71.7</td><td rowspan=1 colspan=1>93.0</td><td rowspan=1 colspan=1>97.8</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr><tr><td rowspan=1 colspan=1>MTI-Z</td><td rowspan=1 colspan=1>71.9</td><td rowspan=1 colspan=1>93.1</td><td rowspan=1 colspan=1>97.8</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr><tr><td rowspan=1 colspan=1>ANC</td><td rowspan=1 colspan=1>70.6</td><td rowspan=1 colspan=1>91.9</td><td rowspan=1 colspan=1>97.1</td><td rowspan=1 colspan=1>97.5</td><td rowspan=1 colspan=1>97.6</td></tr><tr><td rowspan=1 colspan=1>WD</td><td rowspan=1 colspan=1>72.1</td><td rowspan=1 colspan=1>93.0</td><td rowspan=1 colspan=1>97.7</td><td rowspan=1 colspan=1>98.1</td><td rowspan=1 colspan=1>98.1</td></tr><tr><td rowspan=1 colspan=1>MTI-IMAT</td><td rowspan=1 colspan=1>71.8</td><td rowspan=1 colspan=1>93.0</td><td rowspan=1 colspan=1>97.8</td><td rowspan=1 colspan=1>98.2</td><td rowspan=1 colspan=1>98.2</td></tr></table>

TABLE V  
Time Consumption of Each IM Technique
<table><tr><td></td><td>MTI-IM</td><td>MTI-Z</td><td>ANC</td><td>WD</td><td>MTI-IMAT</td></tr><tr><td>Median time [ms]</td><td>3.173</td><td>2.960</td><td>46.444</td><td>15.294</td><td>15.514</td></tr></table>

As expected, there is an increasing trend in detections as $P _ { n }$ goes down. Some target amplitudes are so low that are never detected. In the considered setups, the IM techniques manage to raise the probability of detection in almost every case, with some exceptions at the lowest SNR.

When $P _ { n } \leq 1 0$ dBm, MTI-IMAT, MTI-Z, and MTI-IM, perform comparably with very little differences. WD stays very close to these two. ANC improves detection but does not converge to the detections of the interference-free signal within these parameters. These observations are valid for both tables. If we look at the differences between the two tables, we can see that only ANC increases its own performance against multiple interferences, albeit slightly. The interfered signal also presents a higher probability of detection in the lower table. This is due to the fact that the combined interferences have a lower level, which has been explained at the start of the section and is further shown by the SNIR plots of Fig. 5.

4) Time Consumption: Regarding the time consumption as a measure of computational complexity for each technique, we have to take into account that all of these have been simulated in MATLAB R2022b on a computer with a set of commercial components (Intel i7-8700 CPU @ 3.20 GHz, 16 GB RAM). This implies that the numbers may probably change if techniques were run in other platforms, especially if we introduce hardware optimizations.

The information related to the time consumption of each technique is shown in Table V. The median value from the Monte Carlo simulations has been taken in order to nullify spurious effects of the computer hardware/software over isolated iterations of the Monte Carlo. Several aspects have to be taken into consideration in order to interpret these results.

First, times are measured over whole CPIs of 128 chirps and 512 samples per chirp. Different sizes may affect these times. Apart from that, both MTI-Z and MTI-IMAT are using the detection stage of MTI-IM. Furthermore, MTI-IMAT operates over the zeroed signal. The median time for the detection stage of the proposed approach was measured as 2.082 ms, which is implicitly included in the MTI-IM, MTI-Z, and MTI-IMAT entries of the table. Thereby, the use of other interference detection schemes prior to these may also affect their total times.

On the other hand, the parameters of ANC, WD, and MTI-IMAT present varying degrees of impact over their execution times. For reference, using a wavelet decomposition level of 2 for WD reduced the median time to 11.125 ms. For MTI-IMAT, the number of iterations had a more significant effect. In the current setup, lowering by 1 the maximum number of iterations reduced the median time by approximately 2 ms each time, down to a minimum of 5.244 ms when n = 1. Finally, ANC presented the highest variability between the considered techniques. As a threshold is set up in order to decide whether the ramp is interfered or not, the number of interfered ramps has a significant effect in the amount of time devoted to mitigation in ANC. Higher noise levels play a role here as well, possibly making ANC perform more corrections than needed. By splitting ANC running times ramp by ramp, it has been obtained that, when it does not detect an interference, it takes less than 0.5 ms per chirp (due to the process of estimating the energy of the ramp). On the other hand, when ANC performs the correction, the median time per sweep increases to 1.671 ms.

From these results, we can conclude that MTI-IM produces decent mitigation results with minimal computational load. The degradation of the technique due to target radial velocity certainly exists, but it has not been found to be an undermining factor. When velocities are uniformly distributed within the maximum unambiguous velocity of the radar, the technique is slightly worse overall than MTI-Z. However, even in this case, the proposal achieves good metrics. If there is some oversampling in the slow-time domain (i.e., the SRI is quick in comparison with the highest velocities in the environment), the performance is improved. This is not uncommon, as in low-speed environments we still want to detect sudden appearances of quick mobile targets.

## VI. EXPERIMENTAL TESTS AND RESULTS

## A. Setup of the Experiments

To validate the proposed technique, a series of experiments were conducted. A Texas Instruments (TI) AWR1443BOOST radar board was used as the victim radar. Two interfering radars were set up, both of the model TI AWR1642BOOST. The field of view of the victim radar in azimuth covers the interval [–50°, 50°]. One interfering radar was placed at around –15°. The other was placed at approximately +30°. In Table VI, the parameters of victim and interfering radars are shown. The victim radar was connected to a laptop using the TI DCA1000EVM data capture card. The computer could then store the time-domain samples captured by the victim radar using the software mmWave Studio. These samples were then analyzed with MATLAB. The different IM techniques were applied, and the range-Doppler profiles were input to a CA-CFAR detector. As the background contribution was dense in the 0 velocity bin, and the targets cannot be assumed to be point-like such as in the simulation, different parameters were used for this detector with respect to Table II. The probability of false alarm indicated in that table, which is used to produce a dynamic detection threshold by escalating the mean noise around each range-velocity bin, produces an undesirably low threshold in this scenario, and some false detections due to multipath and clutter appear. As such, we used a power margin of 18 dB over the noise floor to detect targets. The CUT size was reduced, with eight training cells in both range and velocity. The guard cells were 5 in range and 3 in velocity.

TABLE VI  
Parameters of the Radar Systems for the Experimental Verification
<table><tr><td rowspan=1 colspan=4>Interfering   InterferingVictim radarradar #1     radar #2</td></tr><tr><td rowspan=1 colspan=1>Board model</td><td rowspan=1 colspan=1>AWR1443BOOST</td><td rowspan=1 colspan=1>AWR1642BOOST</td><td rowspan=1 colspan=1>AWR1642BOOST</td></tr><tr><td rowspan=1 colspan=1>Centre frequency [GHz]</td><td rowspan=1 colspan=1>77.0</td><td rowspan=1 colspan=1>77.0</td><td rowspan=1 colspan=1>77.0</td></tr><tr><td rowspan=1 colspan=1>Bandwidth [MHz]</td><td rowspan=1 colspan=1>2730.7</td><td rowspan=1 colspan=1>2598.4</td><td rowspan=1 colspan=1>2998.2</td></tr><tr><td rowspan=1 colspan=1>Sweep slope [MHz/µs]</td><td rowspan=1 colspan=1>19.505</td><td rowspan=1 colspan=1>19.988</td><td rowspan=1 colspan=1>29.982</td></tr><tr><td rowspan=1 colspan=1>Chirp duration [μs]</td><td rowspan=1 colspan=1>140.0</td><td rowspan=1 colspan=1>130.0</td><td rowspan=1 colspan=1>100.0</td></tr><tr><td rowspan=1 colspan=1>Idle time [μs]</td><td rowspan=1 colspan=1>5.0</td><td rowspan=1 colspan=1>5.0</td><td rowspan=1 colspan=1>18.0</td></tr><tr><td rowspan=1 colspan=1>Sampling frequency [MHz]</td><td rowspan=1 colspan=1>6.0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Samples per chirp</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>一</td><td rowspan=1 colspan=1>一</td></tr><tr><td rowspan=1 colspan=1>Chirps per CPI</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>CPI repetition period [ms]</td><td rowspan=1 colspan=1>19.0</td><td rowspan=1 colspan=1>57.0</td><td rowspan=1 colspan=1>57.0</td></tr></table>

As the radars are totally asynchronous, the presence of the two independent interferences is not guaranteed in every single burst. Therefore, a high number of frames were captured. This way, it was possible to search for CPIs with the simultaneous presence of the two interferences.

The experiments were carried out in the vicinity of the Radio Systems laboratory at the School of Telecommunications Engineering of the University of Vigo. In Fig. 8, the setup of the experiment can be seen. The picture was taken from behind the victim radar, mounted over a stool, using a zoom lens. The interfering radars can be seen to the left (#1) and right (#2) of the image, mounted over stools as well. The victim radar is aimed toward the end of the alley. There, some reflective objects can be seen. These include a couple of traffic signals (one of which has its broadside almost parallel to the angle of incidence of the radar wave), a barrier, a couple of lamplights, and a car. Behind the victim radar, a drone can be seen. Its size can be compared with the board. This was used as a mobile target with controlled speed and low RCS.

Notice the metallic drains as well in the middle of the alley. Due to its mild inclination toward the radar, we noticed that the farthest one produced a strong backscattering component, which will be seen in the results shown in the following. The closest one, which is a little bit outside the half-power beamwidth of the radar antenna, gets mixed with the stool of radar #1 without using further angular information.

![](images/3052bbc47ab39298034532a6cd83fdc221b027d531ed6715dabe71f351006324.jpg)  
Fig. 8. Picture with the setup of the experiment.

## B. Results

In Fig. 9 and Table VII, the results of the experiments are displayed. Two consecutive CPIs were taken from the whole capture, one of them [see Fig. 9(a)] with significantly more interference than the other used for reference [see Fig. 9(b)]. Their respective RD heatmaps are shown in Fig. 9(c) and (d), with the detections superimposed. The two independent interferences are easily spotted in the time domain. The one introduced by radar #2 is more recurrent but has a shorter duration. During the interfered burst, the drone was moving against the victim radar at approximately 1.5 m/s. Its distance was of approximately 4.2 m. There is a difference of 19 ms between both bursts, so the drone moves around 32% of a range bin between them. The second CPI has a very small amount of interference, and only from the interfering radar #2, which apart from affecting less samples, is farther away from the victim radar. Furthermore, only seven chirps are affected, and these are close to one extreme of the slow-time axis. As Hanning windows are being applied, these interferences get scaling factors in the interval of [0, 0.31]. This way, the detection map of Fig. 9(d) can be used as a kind of ground truth. Note that every RD heatmap is displayed within the same color range.

The IM techniques are applied over the interfered CPI. The results can be seen in Fig. 9(e)–(i). By looking at the heatmaps, different levels of interference mitigation can be seen. For MTI-IM, MTI-Z, and MTI-IMAT, relatively small levels of interference can be seen in the background, especially by looking at the closest range bins. This is likely missed interference due to the detection scheme (which is the one of MTI-IM, as explained in the former section).

(e)  
![](images/64470944d6f8332ed836515c9e28d30079e4346a66c7dbc0dd413607a1487f1d.jpg)  
(a)

![](images/4abf39cc49992406e36e160d3e93c596e920acfa2aecc4f67c618344e5a68414.jpg)  
(d)

![](images/1aaddd91df2794e230262830b15863d86d3b292609472b784bc59cf643d4dd37.jpg)

![](images/2c90d5c81c662460581a1d32b94ba7d1623b495adfaa141a1884af80dd5f2de1.jpg)

![](images/3d343ba8e3d1585b3ceb34d829d824cfdd36bab9ed1f935c73c7ce4c49b59d5b.jpg)  
(c)

![](images/85ec5ab9e1c2de7c8a5fbb753e33ef0366f9e4cefe00bf76f955d0f526e6a018.jpg)

![](images/422e8633f3f5973c73fa38f1ac2299908b5c71d8f836586523b5caccff600f09.jpg)  
(g)

(f)  
![](images/2c55ced346b86a0a5b9f252d255f91d503d267a3545db7092c58edf5bdffc519.jpg)  
(h)

![](images/17e8f9f58066ecdc308a6323c5f3156df2a80222c4d4c9aead39b5e55c7e8b29.jpg)  
(i)  
Fig. 9. Results of the experiment. (a) displays the modulus of the interfered CPI while (b) shows the immediately anterior CPI as reference. (c) and (d) are their respective RD profiles. (e)–(i) shows the effects of applying the different IM approaches, namely proposed (e) MTI-IM, (f) MTI-Z, (g) ANC, (h) WD, and (i) MTI-IMAT.

TABLE VII  
Estimated SNIR From Measurements
<table><tr><td></td><td>Reference</td><td>Interfered</td><td>MTI-IM</td><td>MTI-Z</td><td>ANC</td><td>WD</td><td>MTI-IMAT</td></tr><tr><td>SNIR [dB]</td><td>38.003</td><td>28.889</td><td>37.667</td><td>37.462</td><td>32.038</td><td>32.810</td><td>37.665</td></tr></table>

Some differences can be seen between these techniques. In MTI-Z, a higher artefact level is visible in the range bins corresponding to the most powerful peaks of the range-Doppler map. These artefacts are typical in zeroing [47]. The resulting SNIR values are provided in Table VII. These have been computed using the detections from the reference CPI in order to estimate the peak locations (performing a correction to the drone location). For the computation of the noise floor, the guard interval of the CFAR detector was left around the expected peak location. It can be seen how the three aforementioned techniques produce a very similar result, greatly increasing the SNIR.

If we look at the detections, these three techniques report the same ones. By comparing with Fig. 9(c) and (d), we can see that the drone is now detected. Two static targets are also reported at 8.1 and 15.5 m. These correspond to the stool with radar #2 and the parking signal whose broad side is slightly parallel to the radial axis of the radar, respectively. The object reflection that appeared in Fig. 9(d) at 14.1 m, corresponding to a metallic drain (due to the road being mildly inclined to the radar), was not recovered in this CPI.

ANC seems to have significant residual interference and some powerful artefacts [see Fig. 9(c) and (g)]. This may be due to the potential presence of weak object peaks in the negative frequency band of the range profile. ANC assumes that this band only contains interference and noise [60]. Complex-valued radar modules can, however, use the full range of frequencies [0, f<sub>s</sub>) to acquire beat signals. Therefore, targets placed such that their reflected signal results in a beat frequency in the interval $[ f _ { s } / 2 , f _ { s } )$ hinder the performance of ANC. Thus, it needs an oversampling factor of at least 2 with respect to the farthest significant reflection present in the environment in order to work flawlessly.

WD successfully recovers the same three targets as MTI-Z, MTI-IMAT, and MTI-IM. Nonetheless, it introduces some distortion, especially in the closest range bins. Every heatmap has a strong detection at range bin 0. This peak is probably spurious and introduced by the HW of the board. WD introduces a great attenuation at those bins, deleting this peak. Nevertheless, this distortion results in WD producing a ghost target at around 0.5 m [see Fig. 9(d) and (h)].

## VII. CONCLUSION

In this work, a simple yet effective IM technique called MTI-IM was proposed. This technique focuses in fighting the uncorrelated interference using an approach inspired by MTI techniques. A subtraction in slow time is followed by a thresholding operation in order to isolate the interference and then subtract it to the baseband signal in time domain.

To validate the proposed approach, extensive Monte Carlo simulations were performed comparing MTI-IM with other four common IM techniques: zeroing, ANC, WD, and IMAT. This comparison was based on several performance metrics, namely SNIR, EVM, detection probability, and computation time. MTI-IM and IMAT have shown a better performance than all the others considered. The proposed technique may suffer from some degradation under highly mobile scenarios, which in the limit cases provided results similar to those of zeroing. However, MTI-IM has a clear computational advantage over IMAT, which makes it valuable in complexity-constrained systems such as automotive radar.

After the simulations, experiments were conducted to complement the above analysis, and the full measurements are available at [80]. Specifically, two interfering radars were deployed outdoor with several static targets and a controlled mobile target of low RCS (drone). MTI-IM was proven to be very effective at fighting interference from two different sources. In the supplementary data, an animation of the full experiment can be seen, and the results of the different techniques are compared side to side.

Summarizing, the performance of MTI-IM can arguably be challenged by targets with high relative speeds present in some automotive environments. However, there are practical cases where this issue may not be too detrimental, which include any situation where there is certain oversampling in the Doppler domain with respect to the most prevalent Doppler components. In the simulations, it was found that for a uniform velocity distribution, the proposed technique obtained the best results among the considered techniques (except IMAT) for speeds up to near 80% of the maximum unambiguous speed of the radar. Nevertheless, measurements in more dynamically dense environments are desirable for a full validation of the technique in such scenarios.

## ACKNOWLEDGMENT

The authors would like to acknowledge J. Wang for providing a dataset for earlier tests of the proposal, and thank I. R. Montero, L. Lamberti, B. Sánchez-Rama, M. R. Prieto, and I. Boubeta for helping with the hardware and data acquisition.

## REFERENCES

[1] H. Winner, “Automotive RADAR,” in Handbook of Driver Assistance Systems: Basic Information, Components and Systems for Active Safety and Comfort, H. Winner, S. Hakuli, F. Lotz, and C. Singer, Eds. Cham, Switzerland: Springer, 2016, pp. 325–403, Accessed: Feb. 17, 2023. [Online]. Available: https://link.springer. com/referencework/10.1007/978-3-319-12352-3

[2] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[3] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: Modulation schemes and interference mitigation,” IEEE Microw., vol. 20, no. 9, pp. 58–72, Aug. 2019.

[4] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[5] “R-REC-M.2057-1-201801-I: Systems characteristics of automotive radars operating in the frequency band 76-81 GHz for intelligent transport systems applications,” ITU-R, Geneva, Switzerland, M.2057-1, Jan. 2018. Accessed: Feb. 15, 2023. [Online]. Available: https://www.itu.int/dms\_pubrec/itu-r/rec/m/R-REC-M.2057-1-201801-I!!PDF-E.pdf

[6] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[7] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in Proc. IEEE German Microw. Conf., 2011, pp. 1–4, Accessed: Nov. 08, 2021. [Online]. Available: https://ieeexplore.ieee.org/abstract/ document/5760761

[8] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in Proc. 9th Eur. Radar Conf., 2012. Accessed: Jan. 19, 2023, pp. 1–5, [Online]. Available: https://ieeexplore.ieee.org/abstract/document/6450766

[9] W. Buller, B. Wilson, J. Garbarino, J. Kelly, B. Thelen, and B. M. Belzowski, “Radar congestion study,” Nat. Highway Traffic Safety Administration, Washington, DC, USA, Tech. Rep. DOT HS 812 632, Sep. 2018. Accessed: Jan. 20, 2023. [Online]. Available: https: //rosap.ntl.bts.gov/view/dot/38820

[10] F. Engels, P. Heidenreich, M. Wintermantel, L. Stacker, M. Al Kadi, and A. M. Zoubir, “Automotive radar signal processing: Research directions and practical challenges,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 865–878, Jun. 2021.

[11] C. Waldschmidt, J. Hasch, and W. Menzel, “Automotive radar — From first efforts to future systems,” IEEE J. Microw., vol. 1, no. 1, pp. 135–148, Jan. 2021.

[12] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw., 2016, pp. 1–9, doi: 10.1109/SAHCN.2016.7733011.

[13] K. U. Mazher, R. W. Heath, K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in Proc. IEEE Radar Conf., 2020, pp. 1–6, doi: 10.1109/Radar-Conf2043947.2020.9266425.

[14] S. Ishikawa, M. Kurosawa, M. Umehira, X. Wang, S. Takeda, and H. Kuroda, “Packet-based FMCW radar using CSMA technique to avoid narrowband interference,” in Proc. Int. Radar Conf., 2019, pp. 1–5, doi: 10.1109/RADAR41533.2019.171379.

[15] Z. Slavik and K. V. Mishra, “Cognitive interference mitigation in automotive radars,” in Proc. IEEE Radar Conf., 2019, pp. 1–6, doi: 10.1109/RADAR.2019.8835643.

[16] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[17] G. P. Blasone, F. Colone, and P. Lombardo, “Passive radar concept for automotive applications,” in Proc. IEEE Radar Conf., 2022, pp. 1–5, doi: 10.1109/RadarConf2248738.2022.9764316.

[18] H. Haderer, R. Feger, C. Pfeffer, and A. Stelzer, “Millimeter-wave phase-coded CW MIMO radar using zero- and low-correlation-zone sequence sets,” IEEE Trans. Microw. Theory Techn., vol. 64, no. 12, pp. 4312–4323, Dec. 2016.

[19] A. Bourdoux, U. Ahmad, D. Guermandi, S. Brebels, A. Dewilde, and W. Van Thillo, “PMCW waveform and MIMO technique for a 79 GHz CMOS automotive radar,” in Proc. IEEE Radar Conf., 2016, pp. 1–5, doi: 10.1109/RADAR.2016.7485114.

[20] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[21] E. Gambi, F. Chiaraluce, and S. Spinsante, “Chaos-based radars for automotive applications: Theoretical issues and numerical simulation,” IEEE Trans. Veh. Technol., vol. 57, no. 6, pp. 3858–3863, Nov. 2008.

[22] T.-H. Liu, M.-L. Hsu, and Z.-M. Tsai, “Mutual interference of pseudorandom noise radar in automotive collision avoidance application at 24 GHz,” in Proc. IEEE 5th Glob. Conf. Consum. Electron., 2016, pp. 1–2, doi: 10.1109/GCCE.2016.7800400.

[23] R. Singh, D. Saluja, and S. Kumar, “Spread spectrum coded radar for R2R interference mitigation in autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 10418–10426, Aug. 2022.

[24] A. Vázquez Alejos, M. García Sánchez, Í. C. Gómez, and D. Muhammad, “Wideband noise radar based in phase coded sequences,” in Radar Technology, 1st ed. G. Kouemou, Ed. Vukovar, Croatia: In-Tech, 2009, pp. 39–60.

[25] C. Knill, B. Schweizer, P. Hugler, and C. Waldschmidt, “Impact of an automotive chirp-sequence interferer on a wideband OFDM radar,” in Proc. 15th Eur. Radar Conf., 2018, pp. 34–37, doi: 10.23919/Eu-RAD.2018.8546524.

[26] J. Overdevest, F. Laghezza, F. Jansen, and A. Filippi, “Radar waveform coexistence: Interference comparison on multiple-frame basis,” in Proc. 17th Eur. Radar Conf., 2021, pp. 168–171, doi: 10.1109/Eu-RAD48048.2021.00052.

[27] G. K. Carvajal et al., “Comparison of automotive FMCW and OFDM radar under interference,” in Proc. IEEE Radar Conf., 2020, pp. 1–6, doi: 10.1109/RadarConf2043947.2020.9266449.

[28] G. Hakobyan, K. Armanious, and B. Yang, “Interference-aware cognitive radar: A remedy to the automotive interference problem,” IEEE Trans. Aerosp. Electron. Syst., vol. 56, no. 3, pp. 2326–2339, Jun. 2020.

[29] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[30] E. H. Kim and K. H. Kim, “Random phase code for automotive MIMO radars using combined frequency shift keying-linear FMCW waveform,” IET Radar, Sonar Navig., vol. 12, no. 10, pp. 1090–1095, Oct. 2018, doi: 10.1049/iet-rsn.2018.5075.

[31] F. Lampel et al., “System level synchronization of phasecoded FMCW automotive radars for RadCom,” in Proc. 14th Eur. Conf. Antennas Propag., 2020, pp. 1–5, doi: 10.23919/Eu-CAP48036.2020.9135417.

[32] K. B. S. A. Dapa, G. Point, S. Bensator, and F. E. Boukour, “Vehicular communications over OFDM radar sensing in the 77 GHz mmWave band,” IEEE Access, vol. 11, pp. 4821–4829, 2023.

[33] P. M. McCormick, C. Sahin, S. D. Blunt, and J. G. Metcalf, “FMCW implementation of phase-attached radarcommunications (PARC),” in Proc. IEEE Radar Conf., 2019, pp. 1–6, doi: 10.1109/RADAR.2019.8835668.

[34] L. Giroto de Oliveira, B. Nuss, M. B. Alabd, A. Diewald, M. Pauli, and T. Zwick, “Joint radar-communication systems: Modulation schemes and system design,” IEEE Trans. Microw. Theory Techn., vol. 70, no. 3, pp. 1521–1551, Mar. 2022.

[35] F. D. S. Moulin, C. Oestges, and L. Vandendorpe, “Characterisation and cancellation of interference with multiple phasecoded FMCW dual-function RADAR communication systems,” in Proc. IEEE 95th Veh. Technol. Conf., 2022, pp. 1–7, doi: 10.1109/VTC2022-Spring54318.2022.9860642.

[36] X. Hu, Y. Li, M. Lu, Y. Wang, and X. Yang, “A multi-carrierfrequency random-transmission chirp sequence for TDM MIMO automotive radar,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3672–3685, Apr. 2019.

[37] M. Wintermantel and H. Goelz, “Radar system for detecting the surroundings with compensation of interfering signals,” EP 2057480 B1, Jun. 4, 2014. Accessed: Feb. 17, 2023. [Online]. Available: https://worldwide.espacenet.com/patent/ search/family/038982855/publication/EP2057480A1?q=pn% 3DEP2057480B1%3F

[38] T.-N. Luo, C.-H. E. Wu, and Y.-J. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[39] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2016, pp. 1–4, doi: 10.1109/ICMIM.2016.7533928.

[40] Y. Kitsukawa, M. Mitsumoto, H. Mizutani, N. Fukui, and C. Miyazaki, “An interference suppression method by transmission chirp waveform with random repetition interval in fast-chirp FMCW radar,” in Proc. 16th Eur. Radar Conf., 2019, pp. 165–168, Accessed: Feb. 17, 2023. [Online]. Available: https://ieeexplore.ieee. org/document/8904555

[41] M. Toth, J. Rock, P. Meissner, A. Melzer, and K. Witrisal, “Analysis of automotive radar interference mitigation for real-world environments,” in Proc. 17th Eur. Radar Conf., 2021, pp. 176–179, doi: 10.1109/EuRAD48048.2021.00054.

[42] R. Muja, A. Anghel, R. Cacoveanu, and S. Ciochina, “Assessment of RF interference mitigation methods for automotive radars using real data,” in Proc. 14th Int. Conf. Commun., 2022, pp. 1–5, doi: 10.1109/COMM54429.2022.9817371.

[43] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

[44] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in Proc. 22th Int. Conf. Inf. Fusion, 2019, pp. 1–8, doi: 10.23919/FUSION43075.2019.9011164.

[45] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Slow-time mitigation of mutual interference in chirp sequence radar,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2020, pp. 1–4, doi: 10.1109/ICMIM48759.2020.9298996.

[46] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2015, pp. 1–4, doi: 10.1109/ICMIM.2015.7117925.

[47] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf., 2017, pp. 90–93, doi: 10.23919/EU-RAD.2017.8249154.

[48] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[49] M. Alhumaidi and M. Wintermantel, “Interference avoidance and mitigation in automotive radar,” in Proc. 17th Eur. Radar Conf., 2021, pp. 172–175, doi: 10.1109/EuRAD48048.2021.00053.

[50] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf., 2020, pp. 726–731, doi: 10.1109/RADAR42522.2020.9114723.

[51] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sens. J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[52] S. Lim, S. Lee, J.-H. Choi, J. Yoon, and S.-C. Kim, “Mutual interference suppression and signal restoration in automotive FMCW radar systems,” IEICE Trans. Commun., vol. E102.B, no. 6, pp. 1198–1208, Jun. 2019, doi: 10.1587/transcom.2018EBP3175.

[53] F. Laghezza, F. Jansen, and J. Overdevest, “Enhanced interference detection method in automotive FMCW radar systems,” in Proc. 20th Int. Radar Symp., 2019, pp. 1–7, doi: 10.23919/IRS.2019.8767459.

[54] S. Murali, K. Subburaj, B. Ginsburg, and K. Ramasubramanian, “Interference detection in FMCW radar using a complex baseband oversampled receiver,” in Proc. IEEE Radar Conf., 2018, pp. 1567–1572, doi: 10.1109/RADAR.2018.8378800.

[55] T. Shimura, M. Umehira, Y. Watanabe, X. Wang, and S. Takeda, “An advanced wideband interference suppression technique using envelope detection and sorting for automotive FMCW radar,” in Proc. IEEE Radar Conf., 2022, pp. 1–6, doi: 10.1109/Radar-Conf2248738.2022.9764275.

[56] Z. Liu, W. Lu, J. Wu, S. Yang, and G. Li, “A PELT-KCN algorithm for FMCW radar interference suppression based on signal reconstruction,” IEEE Access, vol. 8, pp. 45108–45118, 2020.

[57] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf., 2018, pp. 0405–0410, doi: 10.1109/RADAR.2018.8378593.

[58] A. Correas-Serrano and M. A. Gonzalez-Huici, “Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2019, pp. 1–4, doi: 10.1109/ICMIM.2019.8726758.

[59] J. Wu, S. Yang, W. Lu, and Z. Liu, “Iterative modified threshold method based on EMD for interference suppression in FMCW radars,” IET Radar, Sonar Navig., vol. 14, no. 8, pp. 1219–1228, Aug. 2020, doi: 10.1049/iet-rsn.2020.0092.

[60] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[61] C. Fischer, H. L. Blocher, J. Dickmann, and W. Menzel, “Robust detection and mitigation of mutual interference in automotive radar,” in Proc. 16th Int. Radar Symp., 2015, pp. 1–6, doi: 10.1109/IRS.2015.7226239.

[62] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Techn., vol. 65, no. 5, pp. 1727–1734, May 2017.

[63] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in Proc. IEEE Radar Conf., 2018, pp. 0252–0256, doi: 10.1109/RADAR.2018.8378566.

[64] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in Proc. 18th Int. Radar Symp., 2017, pp. 1–10, doi: 10.23919/IRS.2017.8008126.

[65] M. Rameez, M. I. Pettersson, and M. Dahl, “Interference compression and mitigation for automotive FMCW radar systems,” IEEE Sens. J., vol. 22, no. 20, pp. 19739–19749, Oct. 2022.

[66] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[67] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc. IEEE Int. Radar Conf., 2020, pp. 624–629, doi: 10.1109/RADAR42522.2020.9114627.

[68] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., 2020, pp. 3802–3806, doi: 10.1109/ICASSP40776.2020.9053013.

[69] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153491–153507, 2021.

[70] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf., 2020, pp. 315–320, doi: 10.1109/RADAR42522.2020.9114641.

[71] S. Chen, W. Shangguan, J. Taghia, U. Kuhnau, and R. Martin, “Automotive radar interference mitigation based on a generative adversarial network,” in Proc. IEEE Asia-Pac. Microw. Conf., 2020, pp. 728–730, doi: 10.1109/APMC47863.2020.9331379.

[72] M. A. Richards, “The stop-and-hop approximation and phase history,” in Fundamentals of Radar Signal Processing, 2nd ed. New York, NY, USA: McGraw-Hill, 2014, pp. 152–155.

[73] M. A. Richards, “Constant false alarm rate detection,” in Fundamentals of Radar Signal Processing, 2nd ed. New York, NY, USA: McGraw-Hill, 2014, pp. 496–535.

[74] U. Kumbul, F. Uysal, C. S. Vaucher, and A. Yarovoy, “Automotive radar interference study for different radar waveform types,” IET Radar, Sonar Navig., vol. 16, no. 3, pp. 564–577, Mar. 2022, doi: 10.1049/rsn2.12203.

[75] F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, and M. Gashinova, “Phenomenology of automotive radar interference,” IET Radar, Sonar Navig., vol. 15, no. 9, pp. 1045–1060, Sep. 2021, doi: 10.1049/rsn2.12096.

[76] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, Sep. 2018.

[77] M. A. Richards, “Doppler and range ambiguities,” in Fundamentals of Radar Signal Processing, 2nd ed. New York, NY, USA: McGraw-Hill Education, 2014, pp. 188–192.

[78] JCGM, Sèvres Cedex, France, “Evaluation of measurement data — Supplement 1 to the ‘Guide to the expression of uncertainty in measurement’ Propagation of distributions using a Monte Carlo method,” Tech. Rep. JCGM 102:2011, 2008.

[79] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in Proc. IEEE Radar Conf., 2019, pp. 1–6, doi: 10.1109/RADAR.2019.8835681

[80] L. A. López-Valcárcel, M. García Sánchez, F. Fioranelli, and O. A. Krasnov, “Raw ADC data from FMCW radar at 77 GHz with interference,” IEEE DataPort, Jun. 30, 2023, doi: 10.21227/E47T-P857.

![](images/fdf157b40bd46cb10b8102075906059508d720d1f9fc17de8e8f29427c0c3d58.jpg)  
Luis A. López-Valcárcel (Graduate Student Member, IEEE) received the B.Sc. and M.Sc. degrees in telecommunication engineering from the Universidade de Vigo, Vigo, Spain, in 2017 and 2019, respectively. He is currently working toward the Ph.D. degree in radio technologies in the automotive field in the Radio Systems group, Universidade de Vigo.  
modeling, and radar.

Since 2017, he has been working as a Researcher with the Universidade de Vigo. His research interests include radio systems, channel

![](images/7ea2a9d94f6aa1501495f85a55a8d234289221e140a5d6deb135904db484f05d.jpg)

Manuel García Sánchez (Member, IEEE) received the Telecommunication Engineering degree from the Universidade de Santiago de Compostela, Spain, in 1990, and the Ph.D. degree in telecommunication engineering from the Universidade de Vigo, Vigo, Spain, in 1996.

He is currently a Professor with the Department of Signal Theory and Communications, Universidade de Vigo. He was the Head of the department from 2004 to 2010. His research interests include radio systems, indoor and out-

door radio channels, channel sounding and modeling for narrowband and wideband applications, interference detection and analysis, design of impairment mitigation techniques, and radio systems design.

![](images/119ef0371ea4991be64f7958e4ef83b47e5336b7a2ba72f637427bba58f30ff1.jpg)

Francesco Fioranelli (Senior Member, IEEE) received the Laurea (B.Eng., cum laude) and Laurea Specialistica (M.Eng., cum laude) degrees in telecommunication engineering from the Università Politecnica delle Marche, Ancona, Italy, in 2007 and 2010, respectively, and the Ph.D. degree in electronic engineering from Durham University, Durham, U.K., in 2014.

He is currently an Associate Professor with TU Delft, Delft, The Netherlands, and was an Assistant Professor with the University of Glas-

gow, Glasgow, U.K. (2016–2019), and a Research Associate with the University College London, London, U.K. (2014–2016). His research interests include the development of radar systems and automatic classification for human signatures analysis in healthcare and security, drones and UAVs detection and classification, automotive radar, and sea clutter. He has authored more than 160 publications between book chapters, journal, and conference papers, edited the books on Micro-Doppler Radar and Its Applications and Radar Countermeasures for Unmanned Aerial Vehicles published by IET-Scitech in 2020.

Dr. Fioranelli was the recipient of four best paper awards.

![](images/f9163bef2ec6accc023cd9376e4338a05518004947a852875bffb9d4bcd9c7a8.jpg)

Oleg A. Krasnov received the M.S. degree in radio physics from Voronezh State University, Voronezh, Russia, in 1982, and the Ph.D. degree in radio technique from National Aerospace University “Kharkiv Aviation Institute,” Kharkiv, Ukraine, in 1994.

In 1999, he joined the International Research Center for Telecommunications and Radar, Delft University of Technology, Delft, The Netherlands. Since 2009, he has been a Senior Researcher with the Microwave Sensing, Signals

and Systems Section, Faculty of Electrical Engineering, Mathematics, and Computer Science, Delft University of Technology, where he became a Universitair Docent (Assistant Professor) in 2012. He has authored or coauthored more than 120 scientific or technical papers and holds a few patents. His research interests include radar waveforms, signal and data processing algorithms for polarimetric radars and distributed radar systems, multisensor atmospheric remote sensing, and optimal resource management of adaptive radar sensors and distributed systems.