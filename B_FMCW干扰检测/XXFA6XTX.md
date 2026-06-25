# An Interference Mitigation Technique for FMCW Radar Using Beat-Frequencies Interpolation in the STFT Domain

Sharef Neemat , Oleg Krasnov, and Alexander Yarovoy, Fellow, IEEE

Abstract— A frequency-modulated continuous-wave (FMCW) radar interference mitigation technique using the interpolation of beat frequencies in the short-time Fourier transform (STFT) domain, phase matching, and reconfigurable linear prediction coefficients estimation for Coherent Processing Interval processing is proposed. The technique is noniterative and does not rely on algorithm convergence. It allows the usage of the fast Fourier transform (FFT) as the radar’s beat-frequency estimation tool, for reasons such as real-time implementation, noise linearity after the FFT, and compatibility with legacy receiver architectures. Verification is done in range and in range-Doppler using radar experimental data in two ways: first by removing interferences from interference-contaminated data and second by using interference-free data as the reference data, and processing it—as if it had interferences—using the proposed technique, inverse cosine windowing and zeroing for comparison. We found that processing with the proposed technique closely matches the reference-data and outperforms the inverse cosine windowing and zeroing techniques in 2-D cross correlation, amplitude, and phase average errors and phase root-mean-square error. It is expected that the proposed technique will be operationally deployed on the TU Delft simultaneous-polarimetric PARSAX radar.

Index Terms— Frequency-modulated continuous wave (FMCW), linear prediction (LP), multiple-input and multipleoutput radars, polarimetric radars, radar interference mitigation techniques.

## I. INTRODUCTION

F <sup>REQUENCY-modulated</sup> <sup>continuous-wave</sup> <sup>(FMCW)</sup>radars might suffer from interferences from other radars radars might suffer from interferences from other radars operating within their vicinity, as in multiple-input and multiple-output radar networks and in automotive scenarios, or from themselves as in the case of fully polarimetric radars with dual-orthogonal signals [1], where there is a leakage between two mutually orthogonal channels (cross-channel interference).

In deramp FMCW radars (stretch-processing), targets range is deduced from beat-frequency estimation. Processing interference-contaminated beat frequencies with fast Fourier transforms (FFTs) yields poorer radar detection, due to undesired artifacts such as a noise-floor level increase in range profiles, which is significantly higher than the system noisefloor, masking weak targets; and spurious vertical lines in range-Doppler. The nature and effects of these interferences on range profiles have been widely studied in the past 10 years as in [2] and [3]. The FMCW interference dwell time derivations and interference shapes in an FMCW receiver due to different waveforms can be found in [4]. Analytical formulas for calculating the probability of the occurrence of ghost targets and the interference power per range bin was presented in [5]. Comprehensive studies of interferences for full polarimetric FMCW radars can be found in [6], and for FMCW radars, in general, in [7], where interference appearance in range-Doppler maps are illustrated. Interference detection was studied in [8] where the image processing techniques were used to detect the interference in the short-time Fourier transform (STFT) domain. In [9], the interference is detected by virtue of using a single-sideband (SSB) I/Q receiver. In an SSB, there usually is only noise in the image band of the radar, and therefore, any interference will be clearly visible in the image band and simple to detect using a threshold. Once the interference slope is known, its extension into the desired signal band can be deduced from the slope. To solve the interference problem, several approaches have been proposed. Among them:

1) zeroing or inverse windowing the interferencecontaminated parts of the signal in the time domain as in [10] and [11]. Inverse windowing the detected interference regions was proposed in [8];

2) using waveform-diversity and receiver-architecturediversity techniques to avoid the interference (e.g., frequency ramp modulation [12], frequency hopping [13], and [14], digital beam forming for interference suppression [15];

3) interference reconstruction and cancelation techniques [16];

4) sparse sampling techniques in [17] (where interference detection is done by monitoring target peakpower threshold levels against the interference-induced noise, then mitigation is done by reconstructing the interference-free signal using a sparse-signal recovery algorithm); and—most recently— in [18].

While zeroing a part of the beat-frequency signal is the simplest interference suppression method, it causes signal phase discontinuity, which results in—after performing the range-compression FFT—target-response broadening in range and high-residual sidelobes. This, in turn, causes worse range resolution and the masking of weak targets. Inverse windowing compromises interferences complete elimination and smoothing the area between the signal and the interference. Both zeroing and windowing cause signal-to-noise ratio (SNR) loss.

Despite all the aforementioned research studies on interference mitigation, there is still a need to develop an interference mitigation technique that: 1) relies on the FFT as the primary beat-frequency estimation tool in the radar system; 2) attempts to restore any SNR loss after mitigating the interference; 3) is usable for very extended-target scenarios (atmospheric observations, for example) where a single target peak-power threshold level—or any form of target detection—cannot be set to begin with. The justification for the emphasis on using the FFT is: 1) real-time implementation considerations and performance predictability; 2) compatibility with legacy receiver architectures; 3) linearity of the FFT in the sense that noise and clutter still maintain their statistical distribution further up the radar processing chain, beyond range-Doppler maps. This linearity is not guaranteed if the parametric frequency estimation algorithms are used instead of the FFT. The maintenance of such a statistical distribution for noise and clutter is beneficial for many detection algorithms.

Looking at the zeroed parts of beat-frequencies as a missing data frame or segment has lead us to consider model-based interpolation as a possible solution, similar to the problem in acoustics signal processing. McAulay’s (a member of the radar signal processing group at the Lincoln Laboratory) speech was proposed to be considered as a sum of sine waves with arbitrary amplitudes, frequencies, and phases [19]. As we will discuss in Section II, this analogy holds and is applicable for FMCW deramping beat frequencies by virtue of the radar’s transmitter linearity. Kauppinen showed a significantly related finding, being that a single frequency sinusoid can be linearly extrapolated by an impulse response of two coefficients [20]. He then generalizes to that the minimum number of coefficients should be twice the number of frequencies in a signal. Kauppinen showed that the extrapolation of missing sinusoidal data can be done forward and backward from the known samples, hence the term interpolation instead of just extrapolation from one side [21]. Interpolation of the FMCW time-domain beat signal at full bandwidth—typically in the megahertz, even after deramping—would then require a prohibitively high-order filter with thousands of coefficients [20]. Coefficients estimation for such a high-order filter would also typically require the usage of a number of samples at least twice the filter order, which would even further burden the radar.

Decomposing the FMCW time-domain signal in the STFT domain would, however, relieve the radar from the high-order extrapolation filter requirement, since each frequency (target) will theoretically be represented by a single slice in the STFT time–frequency axes. The idea of working in the STFT domain for speech was indeed also presented by McAulay in the 1980s for the purpose of speech analysis and synthesis (reconstruction) back to speech [22], and later presented for radar without further investigation [23]. The work was continued by McAulay andQuatieri for the purpose of audio cross-channel interference suppression using the aforementioned sinusoidal model in the STFT domain, followed by an inverse STFT (ISTFT) for synthesis [19], [24].

We note that in all the previously cited works, no strict linking of the extrapolated or interpolated data—in the STFT domain—from a phase-continuity point of view has been attempted. The methods suggest none or just the averaging of the forward and backward extrapolated amplitudes using a cross-fading window. The quality of these reconstruction methods was evaluated subjectively using listening tests. A momentary phase discontinuity might be negligible to the human ear in speech, but remains a limiting factor in radar. There is also no concept of a coherent processing interval (CPI) phase stability (coherence) across multiple sweeps in acoustics. In FMCW, however, the end goal would be to perform FFT operations on the reconstructed sinusoids— after an ISTFT—for range and Doppler information. Phase discontinuities after concatenating the original signal with the interpolated part would cause significantly high sidelobes after performing a range-compression FFT, and as a result, phase stability from pulse-to-pulse will subsequently degrade, resulting in additional high sidelobes after the Doppler (second) FFT.

Considering the suppression/removal of FMCW interferences in the STFT domain and their reconstruction (as in Fig. 1 for example), defines the problem as one of the nature of the reconstruction of an amplitude-modulated single-frequency sinusoid per target which was observed in two separate windows. The single-frequency amplitudemodulated sinusoid per target is the simplest beat-frequency signal model, as we will discuss how this varies for real scenarios in Section II. Inspired by acoustics, in this paper, we propose an interference mitigation technique in the STFT domain, tuned for deramping FMCW radar. In our technique, interference-contaminated parts of the beat frequencies within a sweep are then suppressed in the STFT domain. Useful beat frequencies are to be subsequently reconstructed based on a known signal model (being amplitude-modulated singlefrequency sinusoids). The STFT is the analysis tool for the signal model parameters estimation. LP coefficients for the signal parameters are then estimated using autoregression (AR). These coefficients are estimated for each STFT frequency slice from the interference-free parts of the sweep, or optionally, in a reconfigurable manner, from a previously known interference-free sweep in the CPI. Suppressed beat frequencies are then replaced by linear-predicted interpolated ones, followed by a phase matching procedure. The difference from the previous techniques and the novelty in this paper is highlighted.

1) The first ever interference mitigation technique for FMCW radar deramp receivers via model-based beatfrequencies interpolation in the STFT domain.

2) An optional LP interpolation coefficients reconfigurable estimation mode for CPI processing. Coefficients are estimated for the current observation scene using a known single interference-free sweep. These coefficients are then reused for the restoration of subsequent interference-contaminated sweeps in the CPI.

![](images/4854e645cdd46bd9bf0c9e34df33346953ac05ece353b4085aee96720300d5eb.jpg)

(a)  
![](images/715fb4d4ee823812422e91a57bd8bb507bce790dd88e0cafb75cbbc59e715f11.jpg)

(b)  
![](images/267f421ac8c47cc2ca91a6d89dcebf2a79565a1ab742dcaa61d46dc4db9d49e0.jpg)  
(c)  
Fig. 1. STFT for a single interference contaminated sweep as received using the FMCW radar’s double-sideband (DSB) receiver. This sweep is used for the experiment in Section V-B. (a) Interference contaminated. (b) Interference contaminated frames suppressed. (c) Beat frequencies interpolated using our proposed technique.

3) The proposed technique is real-time implementable, with a predictable execution delay (latency), based on FFT banks and fixed-length extrapolation filters, as opposed to iterative methods relying on algorithm convergence.

4) An evaluation of the technique’s performance in the range-Doppler domain as opposed to range-only (rangeprofiles) as in previously cited work. The aim is to additionally showcase the maintenance of the radar’s coherence over a CPI after interference mitigation.

The rest of the paper is organized as follows. Section II presents the theoretical aspects related to the proposed technique. Section III describes the technique used for interference mitigation. Section IV presents technique simulations. Section V presents experimental results with real radar data and discusses the findings. Conclusions and final remarks are given in Section VI.

## II. THEORY

## A. Deramp Linear FMCW Receivers

In linear FMCW [25], the transmitted signal can be described as

$$
T ( t ) = A _ { t x } \cos { \left[ 2 \pi \left( f _ { c } t + \frac { 1 } { 2 } \alpha t ^ { 2 } \right) \right] }\tag{1}
$$

![](images/f96d0a6406fede79309be7e7553b5efa52f4cdee3c5495784308a0b9719421c4.jpg)

![](images/47b97e538c5e8132116e7549ecb92b8a43ebe8f113ec078d544ab774aaf6d3e3.jpg)

![](images/b1d10a7d066632ab374c262804aa96057bbcfbc823a83484f5e4b0cff3b35e5b.jpg)

![](images/d05adc3d1459286bb8e63a8475ce5c437ff4ed8a9c9982e226ba611700cc40de.jpg)  
(a)  
(b)  
Fig. 2. After [4], [6] and [18]. (a) Deramping linear FMCW operational overview. The transmitted and received chirps are mixed to produce beat frequencies which are usually bound by an LPF. (b) Simplified receiver architecture (top) where $R _ { b } ^ { \prime } ( t ) \dot { }$ from (6) is shown after the LPF. A victim/interferer FMCW interference example (bottom) where the shaded area represents interferences in a DSB receiver implementation.

for $- T _ { \mathrm { s w } } / 2 < t < T _ { \mathrm { s w } } / 2$ , where $T _ { \mathrm { s w } }$ is the duty cycle/sweeptime interval as in Fig. 2, $A _ { t { \cdot } }$ <sub>x</sub> is the transmitted amplitude, $f _ { c }$ the carrier center frequency, the chirp rate $\alpha = B _ { t x } / T _ { \mathrm { s w } }$ and $B _ { t . }$ <sub>x</sub> the transmitted bandwidth. The chirp rate sign determines an up or down chirp. The received signal is

$$
{ { R } _ { i } } \left( t \right) = { { A } _ { r x } } \cos \left[ 2 \pi \left( { { f } _ { c } } \left( t - { { \tau } _ { i } } \right) + \frac { 1 } { 2 } \alpha \left( t - { { \tau } _ { i } } \right) ^ { 2 } \right) \right]\tag{2}
$$

for $- ( T _ { \mathrm { s w } } / 2 ) + \tau _ { \mathrm { m a x } } < t < T _ { \mathrm { s w } } / 2$ , where $A _ { r x }$ is the received amplitude, τ<sub>i</sub> is a target’s response time delay, and $\tau _ { \mathrm { m a x } }$ is the maximum time delay corresponding to the FMCW radar’s desired maximum range. In deramping, the transmitted and received signals are mixed to produce beat-frequencies. This is illustrated in Fig. 2 where a receiver’s output can be considered as a sum of beat-frequencies. The receiver implementation can be an I/Q (SSB) or DSB. These beat frequencies are usually bound by a low-pass filter (LPF), limiting the maximum frequency in the beat-frequency interval to a desired maximum range. The beat frequencies are then typically sampled to a point that satisfies the Nyquist criterion for that maximum range. A beat frequency for a target return after mixing and filtration can also be expressed as [16]

$$
R _ { b , i } ( t ) = A _ { i } \cos [ \varphi _ { i } ( t ) ]\tag{3}
$$

and the receiver output for M multiple responses can be written as

$$
R _ { b } ( t ) = \sum _ { i = 0 } ^ { M } R _ { b , i } ( t )\tag{4}
$$

confirming that targets’ beat frequencies, like speech, can indeed be considered as a sum of sinusoids with arbitrary amplitudes, frequencies and phases. A full derivation showing all phase terms can be found in [26]. This insight lends itself to working with targets’ beat frequencies in the STFT domain. Each frequency (target) will theoretically be represented by a single slice in the STFT time–frequency axes. Targets with different velocities will later be resolvable in the Doppler domain after processing a CPI. It is worth noting that in the interference mitigation technique presented in this paper, we do not consider the case where a target might have a considerably high acceleration— causing a frequency change within a single sweep—as in ballistic missile applications, for example. The proposed technique can, however, work in radars experiencing targets range-migration phenomena, as this happens from sweep-to-sweep.

## B. FMCW Interference

In a victim deramp FMCW radar receiver like the one in Fig. 2(b), a received interference from a similar interferer FMCW radar can be described similar to (2) as

$$
{ R } _ { I } ( t ) = { A } _ { I } \cos \left[ 2 \pi \left( f _ { c } ( t - \Delta \tau ) + \frac { 1 } { 2 } \alpha _ { I } ( t - \Delta \tau ) ^ { 2 } \right) \right]\tag{5}
$$

where $A _ { I }$ is the interference amplitude, τ is the interferer’s transmission start time delay with respect to the victim radar transmit start time, and the interferer’s chirp rate $\alpha _ { I } ~ = ~ B _ { I } / T _ { \mathrm { s w } \_ I }$ . The interferer’s bandwidth is $B _ { I }$ and its sweep time interval is $T _ { \mathrm { s w } \_ I }$ . This interference will be mixed with the transmitted reference, along with useful received echoes. This means that the receiver output in (4) can be written as

$$
R _ { b } ^ { \prime } ( t ) = \left\{ \begin{array} { l l } { R _ { \mathrm { b e a t } } ( t ) , } & { - \left( \frac { T _ { \mathrm { s w } } } { 2 } \right) + \tau _ { \mathrm { m a x } } < t < t _ { 1 } } \\ { R _ { \mathrm { b e a t } } ( t ) + R _ { I } ( t ) , } & { t _ { 1 } \le t \le t _ { 2 } } \\ { R _ { \mathrm { b e a t } } ( t ) , } & { t _ { 2 } < t < T _ { \mathrm { s w } } / 2 } \end{array} \right.\tag{6}
$$

where the interference duration $T _ { \mathrm { I N T } } = t _ { 2 } - t _ { 1 } + 1$ following the derivations in [4], [16] and [18]. It has been demonstrated that after deramping, the instantaneous frequency of $R _ { I } ( t )$ can be expressed as $f _ { i } ( t ) = ( \alpha _ { I } - \alpha ) t - \alpha _ { I } \Delta \tau$ . The analysis in [18] show that since $f _ { i } ( t )$ is bound by the victim’s LPF as illustrated in Fig. 2(b), the interference duration will be $T _ { \mathrm { I N T } } ~ \leq ~ | 2 \cdot \mathrm { L P F } / ( \alpha _ { I } - \alpha ) |$ . Note that the factor 2 will not be present in an SSB receiver implementation. For a DSB receiver, the interference appears as a $\mathbf { \Delta ^ { 6 6 } V } ^ { , 5 }$ like shape intersecting across the beat frequencies band, as in Fig. 1(a).

## C. Linear Prediction of FMCW Beat Frequencies

In the STFT domain, FMCW target beat frequencies— as in (4) and Fig. 1—appear as horizontal (slices) in the time–frequency plane. The full derivation in [26] shows that— except for target range—contributing factors to the phase elements of (2) are usually very small in one sweep compared to π radians and can be neglected. It is expected that a noisefree single point target will have a single constant-amplitude frequency slice. In reality, we however observe amplitude fluctuations on each frequency slice which depend on factors as follows.q

1) target(s) radar-cross section (RCS) frequency dependence varying in response to swept instantaneous frequency (Swerling RCS models) in relation to target(s) behavior and nature (point/extended/stable/moving).

2) FFT leakage and resolution degradation due to the fact that the STFT window and hop sizes being typically smaller than the observed signal length;

3) ripple on beat frequencies as a result of imperfect digital filters’ passband-ripple.

There usually are one or more digital filters in an FMCW radar receiver chain (dc-block, I/Q demodulation, maximum-range, and so on).

Because of the aforementioned reasons, the beat frequencies in the STFT domain can be considered as time sinusoidal signals as well, but—as key—with a much lower frequency than the original time domain deramped signal. In Section III, we will show that we propose to suppress interference-contaminated beat-frequency frames in the spectrogram, and interpolate them. Since it has long been known in acoustics that time signals’ parameters can be modeled using AR, and further extrapolated using these parameters by LP, we propose to do so for FMCW radar beat-frequencies in the STFT domain in this paper.

In LP, future y values are estimated using a linear combination of previous ones, with the most common representation being

$$
\hat { x } [ y ] = \sum _ { i = 1 } ^ { L P _ { \mathrm { o r d } } } a _ { i } x [ y - i ]\tag{7}
$$

where $\hat { x } [ y ]$ is the predicted value, $L P _ { \mathrm { o r d } }$ is the prediction filter order, and $a _ { i }$ is the AR prediction coefficients. AR coefficients estimation algorithms recommend having available samples— to estimate from—at least twice $L P _ { \mathrm { o r d } }$ . Noting that when estimating from postinterference region samples, nothing changes, except that samples are flipped-around before being used. This will further be discussed in Section III. The coefficients are estimated following the Burg method [27] in our implementation. Several methods exist for AR parameters estimation, such as the least square and Yule-Walker [28]. These methods lead to approximately the same results for large data sets (typically more than 2048 points [29]). It has, however, been demonstrated that the Burg method is more reliable than the others [29].

## D. Beat-Frequencies in the STFT Domain

At the output of a typical deramping FMCW receiver, similar to the one shown in Fig. 2, let a received sweep— as in (6)—have k samples, a sampling frequency $f _ { s }$ Hz, and a sampling time $t _ { s }$ (in seconds), yielding an observation time $T _ { \mathrm { o b s } } = k / f _ { s }$ (in seconds). The beat-frequency resolution of this signal would then be $\Delta f = 1 / T _ { \mathrm { o b s } }$ (in Hertz). In the STFT domain, the sweep can be represented as

$$
x _ { l } [ n ] = \sum _ { n = - \frac { W _ { \mathrm { l e n } } } { 2 } } ^ { \frac { W _ { \mathrm { l e n } } } { 2 } - 1 } h [ n ] x [ n + l \Delta \mathrm { h o p } ] e ^ { - i 2 \pi n / W _ { \mathrm { l e n } } }\tag{8}
$$

![](images/5547404f10007bb4d76511e71b0647c0b46ffd0e397dee04464489ef284ed4ab.jpg)  
Fig. 3. Recipe for the proposed interference mitigation technique, and the setup for the first experiment in Section V-B.

where l is the frame number in the STFT, and $W _ { \mathrm { l e n } }$ is the number of samples for each FFT forming the STFT. h is the analysis window function (Hamming in our case), and x is the input sweep fragment. hop is the number of samples from successive STFT windows to create an overlap, and ω the frequency index. The number of frames is defined as $l = 1 + \mathrm { H o o r } ( ( k - W _ { \mathrm { l e n } } ) / \Delta \mathrm { h o p } )$ , where floor is a round-towardzero operation. The observation time will be determined by $W _ { \mathrm { l e n } }$ as $T _ { \mathrm { o b s \_ S T F T } } = W _ { \mathrm { l e n } } / f _ { s }$ ( in seconds). The reduced observation time will yield an STFT frequency axis resolution being $\Delta f _ { \mathrm { S T F T } } = 1 / T _ { \mathrm { o b s \_ S T F T } }$ (in Hertz).  f<sub>STFT</sub> will be significantly coarser than $\Delta f$ of the original signal. On the STFT’s time axis, the time equivalent of the hop size is $T _ { \Delta \mathrm { h o p } } = \Delta \mathrm { h o p } / f _ { s } ,$ resulting in a different sampling frequency $f _ { \Delta \mathrm { h o p } } = 1 / T _ { \Delta \mathrm { h o p } } .$ To satisfy the Nyquist criterion, the maximum STFT beatfrequency-slice fluctuation that can then be unambiguously observed is $f _ { \Delta \mathrm { h o p } } / 2$ . Note that the STFT is the analysis tool for the signal model (beat-frequencies) parameters estimation.

## E. Beat-Frequency Fluctuation Model

We model the beat-frequency fluctuations discussed in Section II-C using a classical amplitude modulation defined with a depth and frequency where

$$
s _ { m } ( t ) = \frac { A _ { 0 } } { 1 + m } \left( 1 + m \cos ( \omega _ { m } t + \varphi _ { m } ) \right) \cos ( \omega _ { b } t + \varphi _ { b } ) + n ( t )\tag{9}
$$

for $0 < t < T _ { \mathrm { s w } }$ , where $s _ { m } ( t )$ is an amplitude modulated STFT beat-frequency slice, $A _ { 0 }$ its amplitude, m is the modulation depth, $\omega _ { m }$ is the modulation frequency, $\varphi _ { m }$ is the modulation phase, $\omega _ { b } = 2 \pi f _ { b }$ where $f _ { b }$ is the beat frequency, with an initial phase ϕ<sub>b</sub>, and $n ( t )$ is noise. The modulation frequency $\omega _ { m } = ( 2 \pi / T _ { \mathrm { s w } } ) \cdot g ,$ , where $g$ is the number of oscillations per observation period, and $f _ { m } \ = \ g / T _ { \mathrm { s w } }$ is the frequency (in hertz).

Any of the fluctuation reasons can lead to the following: 1) m possibly ranging from 0 to 1 in depth;

2) $f _ { m }$ being smaller than $\Delta f _ { \mathrm { S T F T } }$ , or being closely spaced to another frequency, and therefore be unresolvable by the STFT on a single-frequency slice;

3) fluctuations periodicity behavior not being captured by the LP coefficients when the number of oscillations $g$ is too small (depending on the interference duration being suppressed); and

4) the SNR affected by the noise amplitude. This model will assist in the tradeoffs for the selection of the $W _ { \mathrm { l e n } } .$ hop and $L P _ { \mathrm { o r d } }$ parameters in Section III-B, and for simulation in Section IV.

## III. METHOD

In the following, the steps for beat signal reconstruction, discusses the reconstruction parameters selection tradeoffs and CPI processing are presented.

## A. Beat Signal Reconstruction Steps

The proposed interference mitigation technique is illustrated in Fig. 3. This technique assumes a priori knowledge of the interference location in the sweep, or the usage of the simple method in [9] to identify that location. The steps are as follows.

1) A deramped sweep is received and taken to the STFT domain.

2) p interference-contaminated frames are then suppressed where $p$ is the index of the suppressed frames. The suppression is illustrated in Fig. 1(b).

3) IQ amplitude LP coefficients (a<sub>i</sub> in (7)) for each n frequency-slice are estimated from the interference-free parts. The coefficients estimation is done from the left and right sides of the suppressed frames. As illustrated in Fig. 4, in CPI processing, an optional mode allows for the retainment of estimated coefficients from a known interference-free sweep, and the reconfiguring of the LP filters with those coefficients from one CPI to another. This will further be discussed in Section III-B..

TABLE I  
INTERPOLATION PARAMETERS TRADEOFFS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Role/Effect</td><td rowspan=1 colspan=1>Size Increase Pros</td><td rowspan=1 colspan=1>Size Increase Cons</td><td rowspan=1 colspan=1>Limits / Requirement to Satisfy</td></tr><tr><td rowspan=1 colspan=1> $\overline { { W _ { l e n } } }$ </td><td rowspan=1 colspan=1>Determines numberof STFTfrequency-slices(frequency resolution)</td><td rowspan=1 colspan=1>Better resolution on the STFTfrequency grid (∆fSTFT). Moreimmunity against amplitudefluctuations. Decrease interpolationfilter operations computationalcomplexity</td><td rowspan=1 colspan=1>Less interference-freesamples l to interpolatefrom. Increase FFTcomputational complexity</td><td rowspan=1 colspan=1>Available samples l to be used forinterpolation have to be at least twicethe interpolation filter order</td></tr><tr><td rowspan=1 colspan=1>∆hop</td><td rowspan=1 colspan=1>Along with $\overline { { W _ { l e n } , \mathrm { i t } } }$ determines the timeresolution $T _ { \Delta h o p }$ andvalue of l</td><td rowspan=1 colspan=1>Interpolation filter operationscomputational complexity decrease</td><td rowspan=1 colspan=1>Less interference-freesamples l to interpolatefrom</td><td rowspan=1 colspan=1>Nyquist criterion for maximumunambiguously observed amplitudefluctuation for a single beat-frequencyslice $( f _ { \Delta h o p } ) .$ Available samples l tobe used for interpolation have to be atleast twice the interpolation filter order</td></tr><tr><td rowspan=1 colspan=1> $\overline { { L P _ { o r d } } }$ </td><td rowspan=1 colspan=1>Determines maximumnumber offrequencies to beinterpolated $( f _ { \Delta h o p } )$ (interpolation quality)</td><td rowspan=1 colspan=1>Better ability to interpolate moreamplitude fluctuations and betternoise immunity</td><td rowspan=1 colspan=1>Interpolation filteroperations computationalcomplexity increase</td><td rowspan=1 colspan=1>Order should be less than or equal to $l / 2$ </td></tr></table>

![](images/18dc2592263be1784649ad4c82bf860a7c29fa2c02de0fb66fcbc85ea5037150.jpg)  
Fig. 4. Optional reconfigurable LP coefficients scheme for CPI processing. Estimated LP coefficients are retained using a known interference-free sweep and then used for the interpolation operations in the rest of the CPI.

4) Extrapolation of IQ amplitudes of (8) is done from right and left following (7). (Noting that this is done on STFT data, which are made up of short FFTs, therefore IQ amplitudes of beat signals on the STFT grid are available. This should not be confused with sweep IQ deramped data from a radar’s SSB receiver.) A cross-fading window is used to merge the data from both extrapolations, hence the term interpolation. An interpolated frequency slice can be written as

$$
x _ { n } [ p ] = c w [ p ] x _ { p f w } [ p ] + ( 1 - c w [ p ] ) x _ { p b w } [ p ]\tag{10}
$$

where $x _ { p f w }$ and $x _ { p b w }$ are the forward and backward extrapolations, respectively. The cross-fading window cw adapted from [30] and [31] is defined as: cw p $c [ p ] ^ { r }$ , where $c [ p ] = 0 . 5 ( 1 + \cos ( \pi ( 1 + p / ( p _ { b } - p _ { e } ) ) ) )$ The contaminated frames’ beginning and end indices are $p _ { b }$ and $p _ { e }$ , respectively, and $r = \log ( 0 . 5 ) / 0 . 5 ( 1 +$ cos(π $( 1 + 0 . 5 / ( p _ { b } - p _ { e } ) ) )$ .

5) An extra sample $\left( p _ { e + 1 } \right)$ is predicted beyond the interference region, with the purpose of checking the predicted phase versus the actual phase at that point. The calculated phase error is then spread backwards in the interpolated data following [31] using the approximation

$$
\varphi _ { \mathrm { e r r o r } } = \hat { \varphi } _ { p _ { e + 1 } } - \varphi _ { p _ { e + 1 } }\tag{11}
$$

where $\hat { \varphi } _ { p _ { e + 1 } }$ is the phase of the extra predicted sample, $\varphi _ { p _ { e + 1 } }$ is the actual phase of the first sample of the interference-free part, and

$$
\hat { \varphi } [ p ] = \hat { \varphi } [ p ] + \frac { p - p _ { b } } { p _ { e } - p _ { b } } \varphi _ { \mathrm { e r r o r } }\tag{12}
$$

where $\hat { \varphi } [ p ]$ are the phase values of the $p$ previously interpolated samples and $p _ { b } \le p \le p _ { e }$ . Note that if the forward or backward parts of the sweep are completely contaminated, the technique will work, (10) will then only have one part and the phase correction step can be skipped.

6) After all p frames have been replaced, convert sweep back to the time domain using an ISTFT.

7) Normal CPI processing can now take place using a 2-D FFT—with Hamming windows, for example—to produce range-Doppler maps.

## B. Reconstruction Parameters Selection Trade-Offs and CPI Processing

Following the beat-frequency model discussion in Section II-E and (9), interpolation errors can be considered using the tradeoffs of the multidimensional dependence in

$$
\mathrm { e r r o r } = f ( \mathrm { S N R } , \mathrm { I N T } , g , m , k , W _ { \mathrm { l e n } } , \Delta \mathrm { h o p } , L P _ { \mathrm { o r d } } )\tag{13}
$$

where INT is the interference duration within a sweep. Some of these dependencies will be covered in the simulations in Section IV. Tradeoffs have to be then made for the selection of $W _ { \mathrm { l e n } }$ , hop, and $L P _ { \mathrm { o r d } }$ parameters. A guideline for these tradeoffs is presented in Table I.

Since the aforementioned fluctuations are not the same for different ranges, target types and different radars, an optimal

![](images/e9cee40f3d9e36d291fe445b235ae17832a42a9da14ce4c54d1220f18722e693.jpg)  
(a)

![](images/f8a2e07a21ae5ce848d63fd8262c4fd08cd1ff119f328e2b1a95bb1fb3e4dd38.jpg)

![](images/4a88c7bab40e37069ee751ce6001de5a5a5c7d6edc8d8f6f3d528120aa6ccbcf.jpg)  
(d)

(b)  
![](images/25672544ee2f54e95b291e5198a3af73c4dce8b119e8eb28fd95cae42b3cd2f1.jpg)  
(c)

![](images/bd2cdb01ba3b59be0e09c1b9eb505b64741cbef9919c3ee1baa4b9500e91e052.jpg)  
(e)

![](images/3cd028c54910ea04483598f6d78f605e54e9730c64ad291890a21ee640597dcc.jpg)

![](images/c5011e7d2bd74b24dd8921355b375bf7a959d68e53905895a3f0312e4a18f657.jpg)  
(g)

(f)  
![](images/6045952c29389dd405a76daeaedd6f4a34876262b3a1ff9d413490b1586d014c.jpg)

![](images/013b701fbd0d5276774724613238707c0092f87cb51675d8e94a77d49242b34c.jpg)

![](images/e01ab35d5bb88ce02daa1088ed54565441b7abf5fa553e00d8fe40efca0100dd.jpg)  
(j)

(h)  
(i)  
![](images/fd10b17a4f968fa12070329ffaad01c3c862f0849ff8e1e3a9d3fa59a8ba7922.jpg)  
(k)

![](images/c80d7c3751a5503d42576fa9d6f5457e2f5024d2cebe82ff64788ae5d1448634.jpg)  
(1)  
Fig. 5. Plots for simulation is Section IV. (a) Input beat signal in time domain. (b) STFT of input signal. (c) Amplitude of the 100-kHz frequency slice. (d)–(i) Box plots for average amplitude error percentages versus LP filter order for different permutations. Dots: outliers. Horizontal lines: median. Circles: mean. In the plots, m: modulation depth from (9); INT: interference duration percentage in relation to the time-domain beat signal. SNR values are given for the input time-domain signal. Number of samples used for coefficients estimation: 450.

$L P _ { \mathrm { o r d } }$ selection cannot be generalized and has to be estimated. This can be done by extrapolating known interferencefree samples (continuously from sweep-to-sweep as a radar background task, for example), and choosing an acceptable error percentage threshold against different LP filter orders. An average interpolation error percentage can be calculated as

$$
\mathrm { e r r o r } = \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \left| \frac { x _ { n } - \hat { x } _ { n } } { x _ { n } } \right| \times 1 0 0 \%\tag{14}
$$

where N is the number of samples interpolated, x is the interference-free samples, and x the interpolated samples. If the nature of the beat frequencies is not foreseen to significantly change from sweep-to-sweep, LP coefficients estimated from a known interference-free sweep can optionally be used for the restoration of an optional number of subsequent interference-contaminated sweeps, or for all subsequent interference-contaminated sweeps in a CPI. This compromise will relieve the radar from the coefficients estimation from sweep-to-sweep. The CPI coefficients retention mode is illustrated in Fig. 4 and has been used in the experiments presented in Section V.

## IV. SIMULATION RESULTS FOR PRESENTED TECHNIQUE

To characterize some of the multidimensional dependencies in (13) for the mitigation technique, a beat frequency is generated as shown in Fig. 5(a) following (9) with $m = 1$ $T _ { \mathrm { s w } } ~ = ~ 1 ~ \mathrm { m s } , ~ g ~ = ~ 2 5 , ~ \varphi _ { m } ~ = ~ 0$ , and $f _ { c } ~ = ~ 1 0 0$ kHz, $\varphi _ { b } = 0 ,$ and sampled at an $f _ { s } = 2 ~ \mathrm { M H z }$ . The additive white

![](images/4075663348e6b8819187c9991de42b3a94a72508d60995fb466826c16e593d0a.jpg)  
Fig. 6. Signal spectrum related to Fig. 5(h) after restoration. The difference in signal amplitude (loss) due to the restoration is represented by dP2P, and the difference in peak to SLL is represented by dPSL. Refer to Table II for these results for all simulated cases.

Gaussian noise is used in the simulations. The beat frequency is then taken to the STFT domain as shown in Fig. 5(b) with $W _ { \mathrm { l e n } } = 6 4 , \Delta \mathrm { h o p } = 4 ,$ , where the effects of $g$ and m are clearly visible. The STFT frequency slice at 100 kHz is then plotted in Fig. 5(c). For 100 Monte Carlo simulation runs, Fig. 5(d)–(i) presents the box plots for different beat frequencies with different dependencies of (13). SNR and INT percentages are related to the time-domain beat-frequency signal before the STFT (an INT of 50%, for example, would mean that 0.5 ms of the beat-frequency signal is interference contaminated). The duration of which the signal in Fig. 5(c) is to be suppressed in relation to different interference percentages is calculated using the equation for l STFT frames in Section II-D. The floor operation when calculating l is the reason the STFT beat frequency has a 0.94-ms duration as opposed to the 1-ms duration of its time-domain representation. Average amplitude errors are calculated using (14) and are related to the amplitudes of the specific frequency slice under test in the STFT domain.

From the simulations, we found that the interference duration and modulation depth have a great impact on the errors. As the input SNR is reduced, the fluctuations do not play a major role and the interference duration is more important. Despite that results are shown for a g value of 25, we found that high values of $g$ are better, as the periodicity behavior is easier than being captured by the LP coefficients. Note that—before reconstruction—the input beat-frequency SNR is improved by virtue of the typical STFT coherent integration gain proportional to $W _ { \mathrm { l e n } }$ (assuming white noise). This explains how the reconstruction is still possible for short INT durations at a 0-dB SNR. The average amplitude errors seem dramatic because they are calculated sample per sample without any thresholding, and therefore, random noise is also compared. To relate those errors to a detection scenario, Fig. 6 presents the signal spectrum related to Fig. 5(h) after restoration. The combination of $g$ and m appear as three targets. The difference in signal amplitude (loss) due to the restoration is represented by dP2P, and the difference in peak to sidelobe level (SLL) is represented by dPSL. Table II presents the results for all simulated cases in decibels, regardless of the probability of detection and false alarm.

TABLE II  
RESULTS RELATED TO FIG. 6 FOR THE STRONGEST TARGET. THE DIFFERENCE IN SIGNAL AMPLITUDE (LOSS) DUE TO THE RESTORATION IS REPRESENTED BY dP2P, AND THE DIFFERENCE IN PEAK TO SLL IS REPRESENTED BY dPSL
<table><tr><td rowspan=1 colspan=1>SNR (dB)</td><td rowspan=1 colspan=3>50</td><td rowspan=1 colspan=3>13</td><td rowspan=1 colspan=3>0</td></tr><tr><td rowspan=1 colspan=1>INT (%)</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>50</td></tr><tr><td rowspan=1 colspan=1>dP2P (dB)</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.3</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>1.0</td></tr><tr><td rowspan=1 colspan=1>dPSL (dB)</td><td rowspan=1 colspan=1>1.8</td><td rowspan=1 colspan=1>2.0</td><td rowspan=1 colspan=1>2.3</td><td rowspan=1 colspan=1>6.0</td><td rowspan=1 colspan=1>6.0</td><td rowspan=1 colspan=1>7.0</td><td rowspan=1 colspan=1>6.0</td><td rowspan=1 colspan=1>6.0</td><td rowspan=1 colspan=1>3.0</td></tr></table>

![](images/2120a211044bb095bda953f610b33c78e598ae056fe4fbd007559ac5b1c74cbe.jpg)  
Fig. 7. RSNR for simulations in Section IV. RSNR values indicate how much of the signal power (in the interference region) is restored due to the proposed mitigation technique. This is an advantage over merely suppressing the interferences in time domain. As the input SNR increases, the better the RSNR. Increasing interference durations give worst results.

In the simulation, the reference noise-free samples—before adding white noise—are known, therefore another way to evaluate the reconstruction results is to do so for the beatfrequency time-domain signal by calculating a restoration SNR (RSNR) [20] as

$$
{ \mathrm { R S N R } } = 1 0 \log { \frac { \sum _ { n = 1 } ^ { N } { z _ { n } } ^ { 2 } } { \sum _ { n = 1 } ^ { N } \left| \left( z _ { n } - z _ { n } ^ { \prime } \right) \right| ^ { 2 } } }\tag{15}
$$

where N is the number of interference-contaminated samples (in the beat-frequency time-domain signal), z is the reference noise-free samples, and $z ^ { \prime }$ is the reconstructed samples. The denominator represents the noise that is the error due to the reconstruction imperfection. The RSNR can also be interpreted as how much of the beat-frequency SNR is restored due to the reconstruction, and to show the reconstruction’s dependence on the input beat-frequency SNR. The RSNR is calculated only over the interference-contaminated region in the beat-frequency time signal and is presented in Fig. 7.

For the permutations in these simulations, LP orders from 18 to 34 were sufficient to achieve stable error results. Similar simulations can be done for different FMCW radars to determine acceptable error thresholds as discussed in Section III-B.

![](images/2eaea26b15c07bfa23cc892ad5b89c83317319b11c9121a7cbf6d01b972d964a.jpg)  
Fig. 8. Experimental setup. (a) PARSAX radar. (b) Industrial chimney as a stable-target in experiment 1. (c) Location of highway in relation to PARSAX for experiment 2. (d) Photograph of the illuminated highway area for experiment 2.

## V. EXPERIMENTS AND RESULTS

## A. Experimental Setup

The performance of the proposed interference mitigation technique is demonstrated experimentally using the full-polarimetric TU Delft PARSAX [32] radar depicted in Fig. 8(a). PARSAX is mounted on the roof of the Electrical Engineering, Mathematics, and Computer Science Building at the TU Delft. The radar operates in S-band (3.1315 GHz) and uses an intermediate frequency (IF) of 125 MHz. The radar is equipped with a horizontal and a vertical polarization transmit channels. PARSAX has four receiver channels providing for cross and copolarization configurations. A simplified PARSAX block diagram is depicted in Fig. 9. On every receiver channel, transmitted and received signals are sampled at IF using a pair of analog-to-digital converters (ADCs) on an Innovative Integrations X5-400M Xilinx Virtex5SX95T field-programmable gate array (FPGA) card. The ADCs are 14-bit devices with sampling rates up to 400 MSamples/s. Deramping signal processing is performed digitally on the FPGAs. Beat frequencies are transferred to a computer via the PCI-express bus for interference mitigation and range-Doppler processing.

PARSAX can be used to create FMCW interferences in the form of cross-channel interferences. This is done by simultaneously generating an upchirp and a downchirp on the horizontal and vertical polarization channels, respectively. This waveform will cause a leakage around the time when the upchirup and downchirp intersect. The interference is in agreement with the theory in Section II-B, except that the interferer and victim radars are different polarization channels within the same radar. This is illustrated in Fig. 9 (bottom right) for the SSB receiver case used in the second experiment. The interference duration in PARSAX for DSB and SSB receivers is approximately 20% and 10%, respectively [6].

![](images/36ef91dd65e9179acb498b600a8c8d1967096668b6f16aba06c9f19cf0b99de9.jpg)  
Fig. 9. Simplified simultaneous polarimetric PARSAX radar block diagram. The radar has two copolarized and two cross-polarization channels. FPGAs allow for implementing a DSB or an SSB receiver. Data transfer to the PC via PCI-express. The interference scenario in the bottom right represents the simultaneous polarimetric mode and an SSB receiver.

PARSAX can also be used in an interference-free mode where only a single chirp is generated on a single polarization channel.

Experiments were conducted using the configuration options shown in Table III. The filter order was selected after analyzing the radar data STFT frequency-slices following the discussion in Section III-B. The lowest filter order which gives stable minimum errors for the worst case frequency slice (target) was selected. The worst case frequency slices for both experiments are illustrated in Fig. 10. For simplicity, that filter order was used for all frequency slices in both experiments.

## B. Experiment 1: Interference Mitigation for a Single Sweep (Range Profile)

The setup for the first experiment is illustrated in Fig. 3. In this experiment, we observe an industrial factory chimney in a stable targets scene, using the simultaneous transmission on the horizontal and vertical polarization channels, and using the radar’s copolarimetric receiver (R-HH) with a DSB imple mentation for an interference duration of 20%. The chimney is depicted in Fig. 8(b). This will result in an interferencecontaminated sweep due to the vertical channel’s leakage into the horizontal one. The aim is to use our interference mitigation technique for this sweep and illustrate the results for a range profile. We observe the interference in the STFT domain shown in Fig. 1(a). The data are then processed using the proposed technique, inverse cosine windowing, and zeroing for comparison. The inverse cosine window is applied to the interference region in the time domain and is defined as

![](images/106085a962014336afae982acd17ddc515b7e65f40baadeecbf4a936f3b46824.jpg)  
(a)

![](images/19672ff8c4535d1b0782b274a8be233c980dfa92f61243e8c6fd3e63b00dd5a9.jpg)  
(b)

![](images/afcb890264e791e7f4a22940178f35c81f4bf66263f4a01e36ff9673ff6b589c.jpg)  
(c)

![](images/b410b5c0df86ef7e51ea226e73233410042722947bf67ecd8b4ac7c1a5fca96f.jpg)  
(d)

Fig. 10. Filter order selection based on average interpolation errors of interference-free beat-frequency-slice amplitude fluctuations. (a) and (b) For radar-measured data, beat-frequency-slice amplitude fluctuation for the worst case-targets in experiments 1 and 2 respectively. (c) and (d) A filter order of 75 was selected for both experiments, because it is the lowest order that gives stable error results.  
![](images/3d2698fae42c5587206d87ffc199674b8be69c3febd723ea4c9b21d00a978be4.jpg)  
Fig. 11. Setup for the second experiment in Section V-C. The zeroing, inverse cosine windowing, and the proposed techniques are compared in range-Doppler against the reference interference-free data. W-2-D-FFT indicates performing a windowed (Hamming, in our implementation) range-Doppler 2-D FFT.

$$
W _ { c } ( t ) = \frac { 1 - \cos \left( \pi \left( \frac { 1 + 2 t } { T _ { \mathrm { s w } } } \right) \right) } { 2 }\tag{16}
$$

where $t _ { 1 } \leq t \leq t _ { 2 }$ as in (6) and $T _ { \mathrm { I N T } } = t _ { 2 } - t _ { 1 } + 1$

## C. Experiment 2: Interference Mitigation

## in a Range-Doppler CPI

The experiment setup is illustrated in Fig. 11. In this experiment, we observe automobiles on a highway, transmitting on only the radar’s horizontal channel, and using the radar’s copolarimetric receiver (R-HH) with an SSB implementation.

![](images/b86ac7f1b731948fd72924d6467d1889dafef70e3a78cf71769b507215755a69.jpg)

![](images/e1e3bb7550cdb0e38b9a7b8806cc926dc5a6fa44578b1867daf12e6fab0d041c.jpg)  
(b)

(a)  
![](images/cbfbe51cb8ab3b49f856b5fc4a4b4aad94f0367ef205ef8419ff6726852d7bdb.jpg)

![](images/27fb53b4b543ce5d8f3d6ad52d35a39693414f9245c873472481d9e35c687e8f.jpg)

(c)  
![](images/de22c90c5d3fd432511b37f516e9e6f3bf344f8d0ece253158b438d4e2cf26a0.jpg)  
(e)

(d)  
![](images/556323ed3836c73f2f1dc9224436f0cc2835edea340860591be6cb2b885b85a0.jpg)

![](images/16413cf1edf92ad3dda8569cac3f43bfb1c578ded3f3f241ec04a75bdaf8913e.jpg)  
(g)

(f)  
![](images/6a7980b668a7daf031259d6a9baebf53cbadeda96147f21d590c1e81f3b63de0.jpg)  
(h)  
Fig. 12. Range-Doppler maps used in the second experiment (Section $\mathrm { V - C } ) ,$ and illustrated in Fig. 11. (a) Reference data. (b) Reference data thresholded at 30 dB from its strongest peak. (c) Zeroing technique processing of the reference data. (d) Zeroing technique processing of the reference data thresholded at 30 dB from its strongest peak. (e) Inverse cosine window technique processing of the reference data. (f) Inverse cosine window technique processing of the reference data thresholded at 30 dB from its strongest peak. (g) STFT interpolation technique processing of the reference data. (h) STFT interpolation technique processing of the reference data thresholded at 30 dB from its strongest peak.

This will result in interference-free sweeps. The highway and its location are depicted in Fig. 8(c) and (d). These interference-free sweeps are used as reference data. The data are then processed—as if it had interferences—using the proposed technique, inverse cosine windowing, and zeroing for comparison. The aim is to evaluate our proposed technique on range-Doppler maps for a CPI in the case of a moving targets scene. Three copies of the data are made available. On the first, a section of each interference-free sweep is removed by the zeroing technique. On the second, the inverse cosine window is applied to that same section. On the third copy, the same section is removed and interpolated by the proposed technique.

![](images/4d3d301022237de199f61aeacafa70124b1bcf2011312236ebb8be24e3c2ef45.jpg)  
Fig. 13. Range profile for the sweep in Fig. 1 (first experiment, Section V-B) after processing with zeroing, inverse cosine windowing and the proposed interpolation technique. A drop in the interference-induced noise floor is visible and weak targets emerge after processing.

TABLE III  
SETUP PARAMETERS FOR EXPERIMENTS IN SECTION V
<table><tr><td rowspan=1 colspan=3>Experiments 1 and 2</td></tr><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>PRF</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>kHz</td></tr><tr><td rowspan=1 colspan=1>Maximum beat-frequency</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>Total number of samplesper sweep</td><td rowspan=1 colspan=1>16384</td><td rowspan=1 colspan=1>Samples</td></tr><tr><td rowspan=1 colspan=1>STFT window length</td><td rowspan=1 colspan=1>3072</td><td rowspan=1 colspan=1>Samples</td></tr><tr><td rowspan=1 colspan=1>STFT hop size</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>Samples</td></tr><tr><td rowspan=1 colspan=1>Linear prediction filterorder</td><td rowspan=1 colspan=1>75</td><td rowspan=1 colspan=1>n/a</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Experiment 1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Receiver type</td><td rowspan=1 colspan=1>DSB</td><td rowspan=1 colspan=1>n/a</td></tr><tr><td rowspan=1 colspan=1>Waveform</td><td rowspan=1 colspan=1>Simultanious up/down chirpson horizontal and verticalpolarization channels</td><td rowspan=1 colspan=1>n/a</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Experiment 2</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Receiver type</td><td rowspan=1 colspan=1>SSB</td><td rowspan=1 colspan=1>n/a</td></tr><tr><td rowspan=1 colspan=1>Waveform</td><td rowspan=1 colspan=1>Up-chirp on horizontalchannel</td><td rowspan=1 colspan=1>n/a</td></tr><tr><td rowspan=1 colspan=1>Retain linear predictioncoefficients for entire CPI</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>n/a</td></tr><tr><td rowspan=1 colspan=1>CPI length</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>Sweeps</td></tr><tr><td rowspan=1 colspan=1>CPI time</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>ms</td></tr></table>

Three durations of 15%, 25%, and 50% are selected to examine the effects of different possible interference durations. All three techniques are then compared against the reference data in range Doppler. A segment—representing a cluster of targets—of the range-Doppler maps from the compared cases is presented in Fig. 12, before and after applying a threshold of <sub>−</sub>30 dB lower than the strongest target peak in each map (different thresholds will also be considered as will be seen in the next section). This range-Doppler segment/cluster will be used for further comparisons.

## D. Results and Discussion

For the first experiment, the results are shown in Fig. 1(c) for our technique in the STFT domain where the “V”-shaped interference is removed. In Fig. 13, the range profile for the compared techniques is shown. The range profile shows that weaker targets clearly emerge after the reduction of the interference-induced noise floor. The inverse cosine window does not perform as well as zeroing—throughout the range profile—because of it being a compromise between completely eliminating the interferences and smoothing the area between the signal and the interference to reduce SLLs in the frequency domain. The “V”-shaped interference will not completely be removed by the inverse cosine window. The zeroing technique, however, suffers from higher residual sidelobes due to the discontinuity in the FFT frequency estimation.

For the second experiment, the results are calculated on the previously mentioned thresholded range-Doppler maps in Fig. 12(b), (d), (f), and (h) for multiple threshold levels. The range-Doppler maps show high sidelobes and signal energy spread in the case of zeroing and inverse cosine windowing, whereas a fine restoration is achieved after interpolation. This is also evident in the range and Doppler cuts illustrated in Figs. 14 and 15. The figures correspond to the interference duration of 15% in Table IV.

The results in Table IV measure performance criteria from different points of view. We found that if we were to evaluate only at target peaks—even after data normalization—it would not be a fully representative restoration accuracy measure, since the zeroing technique can cause peak-deformation into more than one. While this might not be very evident in simulation data, we found it to be so for experiments with the radar. We therefore calculate the performance criteria on the thresholded range-Doppler maps—instead of just at normalized peaks—for more representative results.

A 2-D correlation coefficient [33] calculated as

$$
r = \frac { \sum _ { s = 1 } ^ { S } \sum _ { j = 1 } ^ { J } ( x _ { s j } - \bar { x } ) \big ( x _ { s j } ^ { \prime } - \bar { x } ^ { \prime } \big ) } { \sqrt { \sum _ { s = 1 } ^ { S } \sum _ { j = 1 } ^ { J } ( x _ { s j } - \bar { x } ) ^ { 2 } \sum _ { s = 1 } ^ { S } \sum _ { j = 1 } ^ { J } \big ( x _ { s j } ^ { \prime } - \bar { x } ^ { \prime } \big ) ^ { 2 } } }\tag{17}
$$

where x is the reference interference-free data, x its mean, $x ^ { \prime }$ is the data processed by the mitigation technique being evaluated and ${ \bar { x } } ^ { \prime }$ its mean. The 2-D matrix indices are s and j .

TABLE IV  
RESULTS OF THE SECOND EXPERIMENT (SECTION V-C) FOR DIFFERENT INTERFERENCE DURATIONS, THRESHOLD VALUES, AND MITIGATION TECHNIQUES. T1: ZEROING TECHNIQUE. T2: INVERSE COSINE WINDOW TECHNIQUE. T3: PROPOSED STFT INTERPOLATION TECHNIQUE
<table><tr><td rowspan=1 colspan=1>Interference Duration (%)</td><td rowspan=1 colspan=15>15</td></tr><tr><td rowspan=1 colspan=1>Threshold from StrongestPeak (dB)</td><td rowspan=1 colspan=3>-10</td><td rowspan=1 colspan=3>-20</td><td rowspan=1 colspan=3>-30</td><td rowspan=1 colspan=3>-40</td><td rowspan=1 colspan=3>-50</td></tr><tr><td rowspan=1 colspan=1>Mitigation Technique</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td></tr><tr><td rowspan=1 colspan=1>2-D Correlation Coefficient</td><td rowspan=1 colspan=1>0.62</td><td rowspan=1 colspan=1>0.78</td><td rowspan=1 colspan=1>0.97</td><td rowspan=1 colspan=1>0.66</td><td rowspan=1 colspan=1>0.74</td><td rowspan=1 colspan=1>0.95</td><td rowspan=1 colspan=1>0.54</td><td rowspan=1 colspan=1>0.72</td><td rowspan=1 colspan=1>0.90</td><td rowspan=1 colspan=1>0.44</td><td rowspan=1 colspan=1>0.69</td><td rowspan=1 colspan=1>0.79</td><td rowspan=1 colspan=1>0.37</td><td rowspan=1 colspan=1>0.62</td><td rowspan=1 colspan=1>0.71</td></tr><tr><td rowspan=1 colspan=1>Amplitude Average Error (%)</td><td rowspan=1 colspan=1>40.98</td><td rowspan=1 colspan=1>24.50</td><td rowspan=1 colspan=1>4.81</td><td rowspan=1 colspan=1>47.37</td><td rowspan=1 colspan=1>26.53</td><td rowspan=1 colspan=1>5.53</td><td rowspan=1 colspan=1>62.67</td><td rowspan=1 colspan=1>38.46</td><td rowspan=1 colspan=1>7.99</td><td rowspan=1 colspan=1>109.97</td><td rowspan=1 colspan=1>79.74</td><td rowspan=1 colspan=1>18.26</td><td rowspan=1 colspan=1>194.53</td><td rowspan=1 colspan=1>110.53</td><td rowspan=1 colspan=1>36.79</td></tr><tr><td rowspan=1 colspan=1>Phase Average Error (%)</td><td rowspan=1 colspan=1>111.66</td><td rowspan=1 colspan=1>32.47</td><td rowspan=1 colspan=1>4.87</td><td rowspan=1 colspan=1>157.96</td><td rowspan=1 colspan=1>85.54</td><td rowspan=1 colspan=1>19.83</td><td rowspan=1 colspan=1>170.94</td><td rowspan=1 colspan=1>100.47</td><td rowspan=1 colspan=1>21.80</td><td rowspan=1 colspan=1>272.56</td><td rowspan=1 colspan=1>118.55</td><td rowspan=1 colspan=1>61.94</td><td rowspan=1 colspan=1>247.97</td><td rowspan=1 colspan=1>107.29</td><td rowspan=1 colspan=1>67.14</td></tr><tr><td rowspan=1 colspan=1>Phase RMSE (radian)</td><td rowspan=1 colspan=1>0.74</td><td rowspan=1 colspan=1>0.24</td><td rowspan=1 colspan=1>0.05</td><td rowspan=1 colspan=1>0.91</td><td rowspan=1 colspan=1>0.59</td><td rowspan=1 colspan=1>0.08</td><td rowspan=1 colspan=1>1.00</td><td rowspan=1 colspan=1>0.69</td><td rowspan=1 colspan=1>0.17</td><td rowspan=1 colspan=1>1.12</td><td rowspan=1 colspan=1>0.73</td><td rowspan=1 colspan=1>0.37</td><td rowspan=1 colspan=1>1.29</td><td rowspan=1 colspan=1>0.73</td><td rowspan=1 colspan=1>0.52</td></tr><tr><td rowspan=1 colspan=1>Interference Duration (%)</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=3>25</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=3></td></tr><tr><td rowspan=1 colspan=1>Threshold from StrongestPeak (dB)</td><td rowspan=1 colspan=3>-10</td><td rowspan=1 colspan=3>-20</td><td rowspan=1 colspan=2>-30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>-40</td><td rowspan=1 colspan=3>-50</td></tr><tr><td rowspan=1 colspan=1>Mitigation Technique</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td></tr><tr><td rowspan=1 colspan=1>2-D Correlation Coefficient</td><td rowspan=1 colspan=1>0.42</td><td rowspan=1 colspan=1>0.66</td><td rowspan=1 colspan=1>0.89</td><td rowspan=1 colspan=1>0.54</td><td rowspan=1 colspan=1>0.75</td><td rowspan=1 colspan=1>0.79</td><td rowspan=1 colspan=1>0.49</td><td rowspan=1 colspan=1>0.77</td><td rowspan=1 colspan=1>0.70</td><td rowspan=1 colspan=1>0.40</td><td rowspan=1 colspan=1>0.72</td><td rowspan=1 colspan=1>0.64</td><td rowspan=1 colspan=1>0.32</td><td rowspan=1 colspan=1>0.60</td><td rowspan=1 colspan=1>0.53</td></tr><tr><td rowspan=1 colspan=1>Amplitude Average Error (%)</td><td rowspan=1 colspan=1>44.84</td><td rowspan=1 colspan=1>34.45</td><td rowspan=1 colspan=1>12.93</td><td rowspan=1 colspan=1>49.61</td><td rowspan=1 colspan=1>38.63</td><td rowspan=1 colspan=1>14.97</td><td rowspan=1 colspan=1>59.27</td><td rowspan=1 colspan=1>46.68</td><td rowspan=1 colspan=1>22.26</td><td rowspan=1 colspan=1>93.31</td><td rowspan=1 colspan=1>67.67</td><td rowspan=1 colspan=1>59.25</td><td rowspan=1 colspan=1>162.15</td><td rowspan=1 colspan=1>63.86</td><td rowspan=1 colspan=1>108.76</td></tr><tr><td rowspan=1 colspan=1>Phase Average Error (%)</td><td rowspan=1 colspan=1>116.89</td><td rowspan=1 colspan=1>77.98</td><td rowspan=1 colspan=1>18.53</td><td rowspan=1 colspan=1>242.93</td><td rowspan=1 colspan=1>96.49</td><td rowspan=1 colspan=1>32.92</td><td rowspan=1 colspan=1>256.18</td><td rowspan=1 colspan=1>221.83</td><td rowspan=1 colspan=1>80.18</td><td rowspan=1 colspan=1>293.25</td><td rowspan=1 colspan=1>162.07</td><td rowspan=1 colspan=1>125.27</td><td rowspan=1 colspan=1>268.86</td><td rowspan=1 colspan=1>107.66</td><td rowspan=1 colspan=1>127.19</td></tr><tr><td rowspan=1 colspan=1>Phase RMSE (radian)</td><td rowspan=1 colspan=1>0.93</td><td rowspan=1 colspan=1>0.56</td><td rowspan=1 colspan=1>0.16</td><td rowspan=1 colspan=1>1.24</td><td rowspan=1 colspan=1>0.81</td><td rowspan=1 colspan=1>0.27</td><td rowspan=1 colspan=1>1.36</td><td rowspan=1 colspan=1>0.91</td><td rowspan=1 colspan=1>0.48</td><td rowspan=1 colspan=1>1.47</td><td rowspan=1 colspan=1>1.00</td><td rowspan=1 colspan=1>0.68</td><td rowspan=1 colspan=1>1.50</td><td rowspan=1 colspan=1>0.85</td><td rowspan=1 colspan=1>0.83</td></tr><tr><td rowspan=1 colspan=1>Interference Duration (%)</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=12>50</td></tr><tr><td rowspan=1 colspan=1>Threshold from StrongestPeak (dB)</td><td rowspan=1 colspan=3>-10</td><td rowspan=1 colspan=3>-20</td><td rowspan=1 colspan=2>-30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>-40</td><td rowspan=1 colspan=3>-50</td></tr><tr><td rowspan=1 colspan=1>Mitigation Technique</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>T3</td></tr><tr><td rowspan=1 colspan=1>2-D Correlation Coefficient</td><td rowspan=1 colspan=1>0.40</td><td rowspan=1 colspan=1>0.68</td><td rowspan=1 colspan=1>0.72</td><td rowspan=1 colspan=1>0.51</td><td rowspan=1 colspan=1>0.76</td><td rowspan=1 colspan=1>0.70</td><td rowspan=1 colspan=1>0.51</td><td rowspan=1 colspan=1>0.77</td><td rowspan=1 colspan=1>0.64</td><td rowspan=1 colspan=1>0.40</td><td rowspan=1 colspan=1>0.72</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1>0.57</td><td rowspan=1 colspan=1>0.42</td></tr><tr><td rowspan=1 colspan=1>Amplitude Average Error (%)</td><td rowspan=1 colspan=1>45.78</td><td rowspan=1 colspan=1>38.35</td><td rowspan=1 colspan=1>25.57</td><td rowspan=1 colspan=1>49.27</td><td rowspan=1 colspan=1>41.97</td><td rowspan=1 colspan=1>33.13</td><td rowspan=1 colspan=1>55.05</td><td rowspan=1 colspan=1>52.19</td><td rowspan=1 colspan=1>47.18</td><td rowspan=1 colspan=1>89.54</td><td rowspan=1 colspan=1>71.92</td><td rowspan=1 colspan=1>112.47</td><td rowspan=1 colspan=1>165.10</td><td rowspan=1 colspan=1>72.36</td><td rowspan=1 colspan=1>156.15</td></tr><tr><td rowspan=1 colspan=1>Phase Average Error (%)</td><td rowspan=1 colspan=1>234.58</td><td rowspan=1 colspan=1>107.62</td><td rowspan=1 colspan=1>52.70</td><td rowspan=1 colspan=1>282.78</td><td rowspan=1 colspan=1>162.61</td><td rowspan=1 colspan=1>103.44</td><td rowspan=1 colspan=1>366.70</td><td rowspan=1 colspan=1>156.21</td><td rowspan=1 colspan=1>155.07</td><td rowspan=1 colspan=1>337.11</td><td rowspan=1 colspan=1>174.41</td><td rowspan=1 colspan=1>194.67</td><td rowspan=1 colspan=1>287.42</td><td rowspan=1 colspan=1>125.77</td><td rowspan=1 colspan=1>180.74</td></tr><tr><td rowspan=1 colspan=1>Phase RMSE (radian)</td><td rowspan=1 colspan=1>1.09</td><td rowspan=1 colspan=1>0.67</td><td rowspan=1 colspan=1>0.43</td><td rowspan=1 colspan=1>1.45</td><td rowspan=1 colspan=1>0.88</td><td rowspan=1 colspan=1>0.71</td><td rowspan=1 colspan=1>1.51</td><td rowspan=1 colspan=1>0.91</td><td rowspan=1 colspan=1>0.80</td><td rowspan=1 colspan=1>1.57</td><td rowspan=1 colspan=1>0.91</td><td rowspan=1 colspan=1>1.00</td><td rowspan=1 colspan=1>1.62</td><td rowspan=1 colspan=1>0.79</td><td rowspan=1 colspan=1>1.08</td></tr></table>

![](images/7471abdd2272fbf05ae84e8391bd4e3e5b22f240571a4e084140c0c1bf9f7fa5.jpg)  
Fig. 14. Cut through the range-Doppler maps in Fig. 12 before any thresholding, at 17.34-m/s velocity. The interpolation technique outperforms the zeroing and inverse cosine window techniques in terms of signal energy spread and SLL.

For the <sub>−</sub>10-dB threshold case, a correlation of 0.97 is calculated compared to 0.78 and 0.62 for the interpolation, inverse cosine windowing and zeroing techniques, respectively. A close correlation (the closer to 1 the better) between the original and restored range-Doppler maps for the proposed technique is observed. 2-D correlation coefficients are indicators of how well SLL is reduced. It is worthwhile noting that the results are slightly biased toward inverse cosine windowing in the second experiment. Inverse cosine windowing performs considerably better than zeroing—and in a few instances even better than interpolation—because it is applied to reference interference-free data. There is—in this case—no “V”-shaped interference to battle against, and no compromise has to be made between completely eliminating interferences and smoothing the area between the signal and the interference.

![](images/b6b91837166a2522bf95908b890c5154c31032991a278feabbdbfa0524b3cbaf.jpg)  
Fig. 15. Cut through the range-Doppler maps in Fig. 12 before any thresholding, at 3.27-km range. The interpolation technique outperforms the zeroing and inverse cosine window techniques in terms of signal energy spread and SLL.

An average error percentage is used to quantify accuracy for amplitudes and phases using (14) where N is the number of elements in a range-Doppler map, x<sub>ref</sub> is the reference interference-free data, and $x ^ { \prime }$ is the data processed by the mitigation technique being evaluated. The results show that—for the <sub>−</sub>10-dB threshold case—the interpolation technique reduces the amplitude and phase errors from 40.98% and 24.5%—for zeroing and inverse cosine windowing respectively–- to 4.81% and from 111.66% and 32.47%— for zeroing and inverse cosine windowing, respectively—to 4.87%. The differences in the results confirms peaks power spread and high sidelobes in the case of the zeroing and inverse cosine windowing techniques, which is also in agreement with the 2-D correlation coefficients’ results. A phase root-meansquare error (RMSE, in radians) is added as an additional method for phases evaluation. The RMSE is calculated using

$$
\mathrm { R M S E } = \sqrt { \frac { 1 } { N } \sum _ { n = 1 } ^ { N } | x _ { n } - \hat { x } _ { n } | ^ { 2 } }\tag{18}
$$

where N is the number of samples, x is the reference interference-free data phases (in radians), and $x ^ { \prime }$ is the phases (in radians) for data processed by the mitigation technique being evaluated. The interpolation technique offers better phase maintenance. Phase stability is of great importance in polarimetric radars, where target polarimetric information is directly dependent on phase variations between the copolarimetric and cross-polarimetric receiver channels (as in the configuration in Fig. 9). At high threshold levels, results are more related to target peaks, but as the threshold drops, sidelobes and noise become more evident, and therefore have greater effects in worsening the results. At the lowest threshold of 50 dB, we are already marginally comparing noise and the results are not very representative.

Conforming to simulations observations, as interference durations increases, the interpolation quality decreases because of errors accumulating over time. In such cases, we observed worst target sidelobes in range and in Doppler. We observed neither the introduction of new/false strong target peaks nor a rise in the noise floor. We believe this to be due to the $\mathrm { L P } ^ { * } \mathrm { s }$ linear nature in the sense that its extrapolated values depend on a linear combination of previous ones. This is also evident in that no new targets falsely appear in the noise regions between targets. On the other hand, zeroing or inverse cosine windowing should be selected—at low SNR scenarios—if the error in (14) exceeds a selected threshold by the radar designer, as motivated in the discussion in Section III-B.

## VI. CONCLUSION

A novel interference mitigation technique for FMCW radar using beat-frequencies interpolation and phase matching in the STFT domain has been presented. After the suppression of interference-contaminated frames of beat frequencies in a sweep in the STFT domain, useful beat-frequencies are subsequently reconstructed based on a known beat-signal model. The beat signal model parameters estimation analysis is done using the STFT. LP coefficients for the signal parameters are then estimated using AR for the current observation scene—for each STFT frequency-slice—from the interference-free parts of each slice, or optionally—in a reconfigurable manner—from a previously known interference-free sweep in the CPI. Suppressed beat-frequency frames are then replaced by the linear-predicted interpolated ones, followed by a phase matching procedure. The proposed technique satisfies our requirement to keep using the FFT as the radar’s beatfrequency estimation tool. It furthermore does not require target detection/thresholding—at the strongest target peak— to begin with, nor algorithm convergence. The technique is real-time implementable with a predictable execution delay (latency), based on FFT banks and fixed-length extrapolation filters. We have demonstrated the technique’s performance improvement with respect to the known zeroing and inverse cosine windowing solutions, against interference for a stable targets scenario. We have then evaluated the technique’s performance in range-Doppler for a moving targets scenario, where an interference-free reference-data CPI is processed using the zeroing technique and versus inverse cosine windowing in comparison to ours. Our technique has shown significant improvements in 2-D correlation coefficients, amplitude, and phase average error percentages and phase RMSE.

The proposed technique is also applicable for radars experiencing targets range-migration phenomena, but not applicable to applications where targets might have a considerably high acceleration—causing a frequency change within a single sweep—as in ballistic missile applications, for example.

## ACKNOWLEDGMENT

The authors would like to thank the editors and anonymous reviewers for their valuable comments and suggestions. The authors would also like to thank F. van der Zwan for his assistance with the measurements.

## REFERENCES

[1] D. Giuli, M. Fossi, and L. Facheris, “Radar target scattering matrix measurement through orthogonal signals,” Proc. Inst. Elect. Eng.— Signal Process., vol. 140, no. 4, pt. F, pp. 233–242, Aug. 1993.

[2] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[3] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Automotive radar— Investigation of mutual interference mechanisms,” Adv. Radio Sci., vol. 8, pp. 55–60, Sep. 2010.

[4] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, pp. 371–378, Mar. 2014.

[5] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in Proc. German Microw. Conf., 2011, pp. 1–4.

[6] G. Babur, “Processing of dual-orthogonal CW polarimetric radar signals,” Ph.D. dissertation, Dept. Elect. Eng., Math. Comput. Sci., Delft Univ. Technol., Delft, The Netherlands, 2009.

[7] S. Sasanka, “Radar to radar interference for 77GHz automotive radar,” M.S. thesis, Dept. Elect. Eng., Math. Comput. Sci., Delft Univ. Technol., Delft, The Netherlands, 2017.

[8] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, Apr. 2015, pp. 1–4.

[9] S. Murali, K. Subburaj, B. Ginsburg, and K. Ramasubramanian, “Interference detection in FMCW radar using a complex baseband oversampled receiver,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 1567–1572.

[10] O. A. Krasnov, G. P. Babur, Z. Wang, L. P. Ligthart, and F. van der Zwan, “Basics and first experiments demonstrating isolation improvements in the agile polarimetric FM-CW radar—PARSAX,” Int. J. Microw. Wireless Technolog., vol. 2, pp. 419–428, Aug. 2010.

[11] G. Babur, Z. Wang, O. A. Krasnov, and L. P. Ligthart, “Design and implementation of cross-channel interference suppression for polarimetric LFM-CW radar,” Proc. SPIE, vol. 7745, p. 774520, Sep. 2010.

[12] Y. Kim, “Identification of FMCW radar in mutual interference environments using frequency ramp modulation,” in Proc. Eur. Conf. Antennas Propag. (EuCAP), 2016, pp. 1–3.

[13] T.-N. Luo, C.-H. E. Wu, and Y.-J. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[14] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, May 2016, pp. 1–4.

[15] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Techn., vol. 65, no. 5, pp. 1727–1734, May 2017.

[16] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, Apr. 2015, pp. 1–4.

[17] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), 2017, pp. 90–93.

[18] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 0405–0410.

[19] R. J. McAulay and T. Quatieri, “Speech analysis/synthesis based on a sinusoidal representation,” IEEE Trans. Acoust., Speech, Signal Process., vol. ASSP-34, no. 4, pp. 744–754, Aug. 1986.

[20] I. Kauppinen, J. Kauppinen, and P. Saarinen, “A method for long extrapolation of audio signals,” J. Audio Eng. Soc., vol. 49, no. 12, pp. 1167–1180, 2001.

[21] I. Kauppinen and J. Kauppinen, “Reconstruction method for missing or damaged long portions in audio signal,” J. Audio Eng. Soc., vol. 50, pp. 594–602, Jul. 2002.

[22] R. J. McAulay and T. F. Quatieri, “Speech processing based on a sinusoidal model,” Lincoln Lab. J., vol. 1, no. 2, pp. 153–168, 1988.

[23] B.-E. Tullsson, “Topics in FMCW radar disturbance suppression,” in Proc. Radar Conf. (RadarConf), 1997, pp. 1–5.

[24] T. F. Quatieri and R. G. Danisewicz, “An approach to co-channel talker interference suppression using a sinusoidal model for speech,” IEEE Trans. Acoust., Speech, Signal Process., vol. 38, no. 1, pp. 56–69, Jan. 1990.

[25] A. G. Stove, “Linear FMCW radar techniques,” IEE Proc. F-Radar Signal Process., vol. 139, no. 5, pp. 343–350, 1992.

[26] K. Peek, “An analysis of the effects of digital phase errors on the performance of a FMCW-Doppler radar,” M.S. thesis, Dept. Appl. Math., Univ. Twente, Enschede, The Netherlands, 2011.

[27] S. M. Kay, Modern Spectral Estimation: Theory and Application. Upper Saddle River, NJ, USA: Prentice-Hall, 1999.

[28] S. Haykin, Nonlinear Methods of Spectral Analysis. Berlin, Germany: Springer-Verlag, 1983.

[29] M. J. L. de Hoon, T. H. J. J. van der Hagen, H. Schoonewelle, and H. van Dam, “Why Yule–Walker should not be used for autoregressive modelling,” Ann. Nucl. Energy, vol. 23, no. 15, pp. 1219–1228, 1996.

[30] P. Saarinen, “New tools in spectral analysis,” Ph.D. dissertation, Opt. Spectrosc., Univ. Turku, Turku, Finland, 1996.

[31] M. Lagrange, S. Marchand, and J.-B. Rault, “Long interpolation of audio signals using linear prediction in sinusoidal modeling,” J. Audio Eng. Soc., vol. 53, no. 10, pp. 891–905, 2005.

[32] O. A. Krasnov, L. P. Ligthart, Z. Li, G. Babur, Z. Wang, and F. van der Zwan, “PARSAX: High-resolution Doppler-polarimetric FMCW radar with dual-orthogonal signals,” in Proc. 18th Int. Conf. Microw. Radar Wireless Commun. (MIKON), 2010, pp. 1–5.

[33] D. Salomon, A Guide to Data Compression Methods. New York, NY, USA: Springer, 2013.

![](images/9f38e0e46b1821367b062281e2db0a23550b053358cfab05228bda93ff6ee513.jpg)

Sharef Neemat received the B.S. degree in computer engineering from King Saud University, Riyadh, Saudi Arabia, and the M.Sc. degree in electrical engineering from the University of Cape Town, Cape Town, South Africa. He is currently pursuing the Ph.D. degree at the Microwave Sensing, Signals and Systems Section, Faculty of Electrical Engineering, Mathematics, and Computer Science, Delft University of Technology, Delft, The Netherlands.

He was involved in secondary surveillance radar identification friend or foe, airborne radios, especially in the design, development, and test of field-programmable gate array/digital signal processor (DSP) drivers and application layer SW for radio housekeeping and scheduling. The DSP designs and code were developed to comply with DO-178B level C (Software Considerations in Airborne Systems and Equipment Certification) and Motor Industry Software Reliability Association C Standard. He was also involved in system engineering/project management of asset-tracking-systems’ development, which included writing system engineering management plans and requirements documentation for systems and their subsystems, complying with MIL-STD-490 and MIL-STD-491.

![](images/c4360ccd4f76547a7a2c13c898cd0c55ccf4645b80a7bebe901688a7971b3136.jpg)

Oleg Krasnov received the M.S. degree in radio physics from Voronezh State University, Voronezh, Russia, in 1982, and the Ph.D. degree in radiotechnique from National Aerospace University—Kharkov Aviation Institute, Kharkiv, Ukraine, in 1994.

In 1999, he joined the International Research Center for Telecommunications and Radar, Delft University of Technology, Delft, The Netherlands. Since 2009, he has been a Senior Researcher with the Microwave Sensing, Signals and Systems

Section, Faculty of Electrical Engineering, Mathematics, and Computer Science, Delft University of Technology, where he was an Assistant Professor in 2012. His current research interests include radar waveforms, signal and data processing algorithms for polarimetric radars and distributed radar systems, multisensory atmospheric remote sensing, optimal resource management of adaptive radar sensors, and distributed systems.

Dr. Krasnov served as the Secretary for the 9th European Radar Conference (EuRAD’12), Amsterdam, The Netherlands.

![](images/f856da38d392ad7937dcdec059b10fcd89c428863df5cc7ba0af1b5346148f14.jpg)

Alexander Yarovoy (F’15) received the diploma degree (Hons.) in radiophysics and electronics, the Candidate Phys. and Math. Sci. degree in radiophysics, and the Doctor Phys. and Math. Sci. degree in radiophysics from Kharkov State University, Kharkov, Ukraine, in 1984, 1987, and 1994, respectively.

In 1987, he joined the Department of Radiophysics, Kharkov State University, as a Researcher, where he became a Professor in 1997. From 1994 to 1996, he was with the Technical University of Ilmenau, Ilmenau, Germany, as a Visiting Researcher. Since 1999, he has been with the Delft University of Technology, Delft, The Netherlands, where he has been the Chair of Microwave Sensing, Signals, and Systems since 2009. He has authored or coauthored over 250 scientific or technical papers and 14 book chapters. He holds 4 patents. His current research interests include ultra-wideband (UWB) microwave technology and its applications (particularly radars) and applied electromagnetics (particularly UWB antennas).

Dr. Yarovoy has been the Director of the European Microwave Association since 2008. He has served as the Chair and the TPC Chair for the Fifth European Radar Conference, Amsterdam, The Netherlands, and the Secretary for the First European Radar Conference, Amsterdam. He has also served as the Co-Chair and the TPC Chair for the 10th International Conference on Ground Penetrating Radar, Delft. He was a co-recipient of the European Microwave Week Radar Award for the paper that best advances the state of the art in radar technology in 2001 (with L. P. Ligthart and P. van Genderen) and in 2012 (with T. Savelyev) and the Best Paper Award of the Applied Computational Electromagnetic Society in 2010 (with D. Caratelli). He has served as a Guest Editor for five special issues of IEEE TRANSACTIONS and other journals. Since 2011, he has been an Associate Editor of the International Journal of Microwave and Wireless Technologies.