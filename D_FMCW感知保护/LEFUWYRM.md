# Spatial-Domain Mutual Interference Mitigation for MIMO-FMCW Automotive Radar

Sian Jin , Pu Wang , Senior Member, IEEE, Petros T. Boufounos , Fellow, IEEE, Philip V. Orlik , Senior Member, IEEE, Ryuhei Takahashi , and Sumit Roy , Fellow, IEEE

Abstract—This paper considers mutual interference mitigation among automotive radars using frequency-modulated continuous wave (FMCW) signal and multiple-input multiple-output (MIMO) virtual arrays. For the first time, we derive a spatial-domain interference signal model that accounts for not only the time-frequency incoherence (e.g., different FMCW parameters and time offsets) but also the slow-time MIMO code incoherence and array configuration differences between the victim and interfering radars. Using the explicit interference signal model with the standard MIMO-FMCW object signal model, we turn the interference mitigation into a spatial-domain object detection under incoherent MIMO-FMCW interference. By exploiting the structural property of the derived interference model at both transmit and receive steering vector space, we derive a detector via beamforming optimization to achieve good detection performance and further propose an adaptive version of this detector to enhance its practical applicability. Performance evaluation using analytical closed-form expressions, synthetic-level simulation and system-level simulation confirms the effectiveness of our proposed detectors over selected baseline methods.

Index Terms—Automotive radar, FMCW, MIMO, interference mitigation, detection, beamforming, adaptive processing.

## I. INTRODUCTION

A <sup>DVANCED</sup> <sup>driver</sup> <sup>assistance</sup> <sup>systems</sup> <sup>(ADAS)</sup> <sup>and</sup> <sup>au-</sup>tonomous driving require high-resolution environment perception systems capable of detecting and identifying stationary (e.g., buildings, trees) and dynamic (e.g., vehicles and pedestrians) objects reliably in all weather conditions. Compared with other perception sensors such as cameras and LiDAR, radar offers the potential for operating in adverse weather and night-time conditions at lower cost and processing overhead [2].

Current automotive radars widely adopt frequency-modulated continuous wave (FMCW) techniques [1], [2], [3], [4], [5], [6], [7], [8], [9], since it enables receivers with low sampling rates while harnessing large sweep frequency bands for high resolution in range. On the other hand, they are limited in use for high-resolution perception tasks due to poor angular resolution, particularly in the elevation domain. To increase the angular resolution, automotive radar chip vendors take various approaches to form a large aperture for highly directional beams. Mechanically scanned FMCW radars, e.g., Navtech CTS350-X, have been used to collect 360<sup>◦</sup> bird’s-eye view (BEV) radar images in the range-azimuth domain but without the Doppler velocity [10]. Synthetic aperture radar (SAR) techniques create high-resolution two-dimensional images of the scene by coherently combining returned radar waveforms with the assumption of known ego vehicle motion [11]. Multiple-input multipleoutput (MIMO) radar is another cost-efficient approach to form a large virtual array with a reduced number of transmit (Tx) and receive (Rx) antennas and radio frequency (RF) chains. To achieve this, the transmitted waveforms from different Tx antennas need to be orthogonal. Orthogonal MIMO signaling schemes can be realized in time-division multiplexing (TDM), frequency-division multiplexing (FDM), and Doppler-division multiplexing (DDM) modes [9], [12], [13]. As of today, the combined MIMO-FMCW automotive radar has been commercialized by chip vendors to achieve tens of and even hundreds of virtual channels in the azimuth and elevation domains [14], [15], [16], [17], [18], [19].

![](images/e1f20d4869ced3c10334fa8377b98616b3af82688342e4b092013894c875cddb.jpg)  
Fig. 1. Illustration for mutual interference for MIMO-FMCW automotive radar, where both victim and interfering vehicles use MIMO arrays to transmit and receive waveform.

With the increasing adoption of MIMO-FMCW automotive radars (e.g., TI’s AWR chipsets [15]), co-channel interference in regulated frequency bands (e.g. 76 − 81 GHz) is anticipated to become of increasing concern, as shown in Fig. 1. Such mutual interference between multiple radars can be coherent or incoherent [20], [21], [22], depending on the nature of the waveforms between interfering and victim radars. Coherent interference arises when the received waveform and array parameters at the victim radar are identical to its own, leading to ghost targets and false object detection. In contrast, incoherent interference occurs when the waveform and array parameters differ, resulting in elevated noise floors at the victim radar, which is more frequently encountered [22] than the coherent interference.

Mutual radar interference mitigation can be achieved by borrowing ideas from multiple access scheduling used in wireless networking. Transmit-side scheduling techniques such as time-division multiple access (TDMA) [23] and chirp slope and frequency offset scheduling [24] have been proposed in this direction. However, scheduling typically requires coordination among the radars (for example, TDMA implies timing synchronization among the radars) and consumes side-channel communication bandwidth. A simpler approach to coherent interference mitigation is transmitter-side waveform randomization [25], [26]. An alternative to transmit-side methods for combating incoherent interference are receiver-side processing. Such approaches can be classified as follows:

1) Fast-time (range) domain: interference-zeroing [27], [28], sparse reconstruction [29], [30], adaptive noise cancellers [31], signal separation [32], [33], wavelet denoising [34], fast-time-frequency mode retrieval [35], fast-time neural network (NN) [36], [37], and fast-timefrequency NN [38];

2) Slow-time (Doppler) domain: ramp filtering [39] and slow-time NN [40];

3) Range-Doppler domain: range-Doppler NN [41], [42], [43], [44], [45].

For MIMO-FMCW automotive radar, interference mitigation can be done in the MIMO code domain [46], but it requires additional communication and coordination between the victim and interfering radars. On the other hand, spatial-domain mitigation approaches were considered to make use of additional degrees of freedom in the antenna or beamspace domain. Initial efforts include receiver beamforming-based approaches [47], [48], [49], [50], [51], null steering [52], and linear constraints minimum variance (LCMV) beamforming [53]. However, these previous efforts lack an explicit spatial-domain interference signal model. As a result, they have been unable to fully exploit the spatial structure of interference signals for effective mitigation.

Distinct from previous efforts, we explicitly model the interference signal to formulate a spatial-domain target detection problem under interference, analyze the limitations of existing detectors, and propose new detectors to account for the structure of interferences. While object detection approaches under mutual radar interference are widely studied using time-frequency representation [35], waveform randomization [25], and NN [36], [37], [38], [40], [41], [42], [43], [44], [45], they are conducted in the fast-time, slow-time, and range-Doppler domains. There is no formulation of object detection under mutual MIMO-FMCW interference in the spatial domain. Our unique contributions in this work are summarized below:

\- We derive a Kronecker-structured signal model for the spatial-domain MIMO-FMCW interference under the time-frequency incoherence, the MIMO code incoherence, and the array difference between the victim and interfering radars. This interference signal model provides a foundation for deriving and analyzing spatial-domain interference mitigation schemes.

Based on the derived interference signal model and insights from the clairvoyant detector, we propose a non-adaptive generalized subspace-based (GS) detector that exploits the structure of both Tx and Rx steering vectors of the interference provided that some interference statistics are given. We derive closed-form analytical expressions of probabilities of false alarm of the GS detector and show that it outperforms the existing non-adaptive receiver subspace detector (RS [3] or null-steering detector [52]) that only exploits the structure of the Rx steering vector of the interference.

We propose an adaptive version of the GS detector (AGS detector) via adaptively estimating the interference statistics of the GS detector. Compared to the adaptive LCMV [53] detector with sample matrix inversion (SMI) method [54], the proposed AGS detector is novel as it exploits the interference structure. Synthetic-level and more realistic system-level simulation show that the adaptive AGS detector outperforms the LCMV-SMI detector.

Throughout this paper, we use the following notations: The transpose is denoted by $( \cdot ) ^ { T }$ , the conjugate by $( \cdot ) ^ { * }$ , the conjugate transpose by $( \cdot ) ^ { H }$ , a set by {·}, the Kronecker product by $\otimes ,$ , the indicator function by 1<sup>[</sup>·<sup>]</sup>, and the generalized Marcum Q-function of order 1 [55] by $\mathcal { Q } _ { 1 } ( a , b )$ . We use $\mathbf { P _ { H } } \triangleq$ $\mathbf { H } ( \mathbf { H } ^ { \bar { H } } \mathbf { H } ) ^ { - 1 } \mathbf { H } ^ { H }$ to denote the projection matrix projecting to the column space of H. We use $\mathbf { P _ { H } ^ { \perp } } \triangleq \mathbf { I } - \mathbf { P _ { H } }$ to denote the projection matrix projecting to the space orthogonal to the column space of H. All indices are counted from 0.

## II. SIGNAL MODEL

In the following, we overview the object signal model, and derive the interference signal model in more detail, assuming the victim radar operates with Tx and Rx uniform linear arrays (ULAs) in the far-field.<sup>1</sup> We also show the convergence of the derived interference model in some special cases.

## A. MIMO-FMCW Waveform

As shown in Fig. 2, we consider a victim radar equipped with <sup>M</sup> Tx antennas over <sup>K</sup> pulses of a coherent processing interval (CPI). The FMCW waveform of the victim radar is

$$
s ( t ) = e ^ { j \pi \beta t ^ { 2 } } D _ { 0 , T } ( t ) ,\tag{1}
$$

where $\beta$ is the chirp rate, <sup>T</sup> is the chirp duration, and $D _ { a , b } ( t ) = 1$ if $a \leq t \leq b$ and $D _ { a , b } ( t ) = 0$ otherwise. The RF waveform on

![](images/6fceef02690223c795475a00872efe0f85fa13784c5e05e2fcfbe8d73eb153c7.jpg)  
Fig. 2. MIMO-FMCW waveforms with slow-time Tx-pulse code $\{ c _ { m , k } \}$ applied to the same FMCW waveform. The Tx-pulse codes can vary depending on the operation mode: DDM-MIMO (e.g., Hadamard or Chu sequences), TDM-MIMO (one-hot vectors), and phased array (all-one vectors).

Tx antenna <sup>m</sup> over <sup>K</sup> pulses is [9]

$$
s _ { m } ( t ) = \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } s ( t - k T _ { \mathrm { P R I } } ) e ^ { j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } ) } ,\tag{2}
$$

where $c _ { k , m }$ is the slow-time Tx-pulse code on <sup>m</sup>-th Tx antenna and <sup>k</sup>-th pulse, $T _ { \mathrm { P R I } }$ is the pulse repetition interval (PRI) of the victim radar and $f _ { c }$ is the carrier frequency. In (2), the slow-time Tx-pulse codes may vary depending on the operation mode [13], [57]:

DDM-MIMO mode: the code at Tx antenna <sup>m</sup> achieves zero/low cross-correlation to codes at other Tx antennas. One example is the binary Hadamard code $c _ { k , m } , k =$ $0 , 1 , \ldots , K - 1$ taken from the columns of a Hadamard matrix $( K > M )$ , where $\begin{array} { r } { \frac { 1 } { K } \sum _ { k } c _ { k , m } c _ { k , m ^ { \prime } } } \end{array}$ equals to 1 if $m = m ^ { \prime }$ and equals to 0 otherwise. Other choices include the Chu sequence and phase codes that spread the interantenna interference in the Doppler domain.

\- TDM-MIMO mode: the code at Tx antenna m is a onehot vector with $c _ { k , m } = 1$ and $c _ { k , m ^ { \prime } } = 0 , m ^ { \prime } \neq m$ if $m =$ <sup>mod</sup> <sup>(k, M)</sup>. That is, only 1 Tx antenna is active during one pulse and each Tx antenna takes turns transmitting.

\- Phased array mode: the code at Tx antenna m is an all-one vector, i.e., $c _ { k , m } = 1$ for all <sup>k</sup>. The Tx angle is controlled by an additional beamforming process which is omitted here.

## B. Object Signal Model

Following the receiver processing at the victim radar of Fig. 3, we provide a quick overview of the object signal model in the spatial domain, e.g., Tx and Rx angles. We assume the victim radar adopts a Tx ULA of <sup>M</sup> elements and an Rx ULA of <sup>N</sup> elements. Similar derivation of the object signal model can be found in [9], [58].

For an object of range <sup>R</sup> and relative radial velocity <sup>v</sup>, the round-trip propagation delay from victim radar’s <sup>m</sup>-th Tx antenna to its <sup>n</sup>-th Rx antenna at time <sup>t</sup> is $\begin{array} { r } { \tau _ { m , n } ( t ) = 2 \frac { R + v t } { c } + } \end{array}$ $\begin{array} { r } { m \frac { d _ { t } \sin ( \phi _ { t } ) } { c } + n \frac { d _ { r } \sin ( \phi _ { r } ) } { c } } \end{array}$ <sup>,</sup> where $d _ { t }$ and $d _ { r }$ are the Tx and Rx element spacings, $\overset { c } { \phi _ { t } }$ and $\phi _ { r }$ are the Tx and Rx angle for the object, and <sup>c</sup> is the speed of propagation. As the object is in the far-field, we have the approximation $\phi _ { t } = \phi _ { r }$

As shown in the upper right (victim Rx) of Fig. 3, the received signal goes through processing blocks such as local oscillator (LO), low-pass filtering (LPF), analog-to-digital converter (ADC), fast-time/range fast Fourier transform (FFT), slow-time/Doppler FFT, and MIMO waveform separation at each Rx antenna chain. A step-by-step derivation of the object signal model is included in Appendix A. At the output of the MIMO waveform separation, one can form an $M N \times 1$ virtual array signal for an object at a given pair of range bin $l ^ { \prime }$ and Doppler bin $k ^ { \prime }$ as

$$
\mathbf { y } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) = b ( l ^ { \prime } , k ^ { \prime } ) \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } .\tag{3}
$$

where $\mathbf { a } _ { t } \triangleq [ 1 , e ^ { - j 2 \pi f _ { \phi _ { t } } } , \hdots , e ^ { - j 2 \pi f _ { \phi _ { t } } ( M - 1 ) } ] ^ { T }$ is the object Tx steering vector with a spatial frequency of $f _ { \phi _ { t } } \triangleq d _ { t } \mathrm { s i n } ( \phi _ { t } ) / \lambda$ $\mathbf { a } _ { r } \triangleq [ \bar { 1 } , e ^ { - j 2 \pi f _ { \phi _ { r } } } , \hdots , \bar { e } ^ { - j 2 \pi f _ { \phi _ { r } } ( \bar { N } - 1 ) } ] ^ { \bar { T } }$ is the object Rx steering vector with a spatial frequency of $f _ { \phi _ { r } } \triangleq d _ { r } \mathrm { s i n } ( \phi _ { r } ) / \lambda , \lambda =$ $c / f _ { c }$ represents the wavelength, and $b ( l ^ { \prime } , k ^ { \prime } )$ is the complex amplitude. Thus, the spatial-domain object signal has a Kronecker structure between the object Tx and Rx steering vectors.

## C. Interference Signal Model

In the lower left (blue shaded) of Fig. 3, a MIMO-FMCW interfering radar possibly employs different array configurations such as the number of Tx antennas $\widetilde { M }$ with Tx element spacing $\widetilde { d } _ { t }$ , slow-time Tx-pulse codes $\widetilde { c } _ { \widetilde { k } , \widetilde { m } }$ , FMCW parameters, time offsets, center frequency $\widetilde { f _ { c } }$ (or wavelength $\widetilde { \lambda } )$ , and bandwidth. The bands of the interference may partially or totally overlap with the band of the victim radar.

Transmitted MIMO-FMCW Waveform at Interfering Tx: The <sup>m</sup> -th interfering Tx antenna sends coded $\widetilde { K }$ pulses

$$
\widetilde { s } _ { \widetilde { m } } ( t ) = \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \widetilde { c } _ { \widetilde { k } , \widetilde { m } } \widetilde { s } ( t - \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } - \widetilde { \tau } _ { s y n } ) e ^ { j 2 \pi \widetilde { f } _ { c } ( t - \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } - \widetilde { \tau } _ { s y n } ) } ,\tag{4}
$$

where the source FMCM waveform $\widetilde s ( t )$ shares the same expression as (1) but with different chirp rate $\widetilde { \beta }$ and pulse duration $\widetilde { T } , \widetilde { \tau } _ { s y n }$ is the transmit synchronization delay (initial time offset) between the reference antennas of the victim radar and the interfering radar, $\widetilde { c } _ { \widetilde { k } , \widetilde { m } }$ is the slow-time Tx-pulse code of the interfering radar that likely are different from those used at the victim Tx, and $\widetilde { T } _ { \mathrm { P R I } }$ is the PRI at the interfering radar.

Interference at Receiving Antennas of Victim Rx: For an interfering radar at range $\tilde { R }$ and radial velocity <sup>v</sup> relative to the victim radar, the one-way propagation delay from its <sup>m</sup>-th Tx antenna to the <sup>n</sup>-th Rx antenna of victim radar is $\widetilde { \tau } _ { \widetilde { m } , n } ( t ) =$ $\begin{array} { r } { \frac { \widetilde { R } + \widetilde { v } t } { c } + \widetilde { m } \frac { \widetilde { d } _ { t } \sin ( \widetilde { \phi } _ { t } ) } { c } + n \frac { d _ { r } \sin ( \widetilde { \phi } _ { r } ) } { c } } \end{array}$ <sup>,</sup> where and $\widetilde { \phi } _ { t }$ and $\widetilde { \phi } _ { r }$ are the interference Tx and Rx angles with respect to the boresight of the interfering radar and the victim radar. At the victim Rx of Fig. 3, the <sup>n</sup>-th Rx antenna observes the RF signal from the interferer $\begin{array} { r } { s _ { n } ^ { i } ( t ) = \widetilde { \alpha } \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \widetilde { s } _ { \widetilde { m } } ( t - \widetilde { \tau } _ { \widetilde { m } , n } ( t ) ) } \end{array}$ <sup>)</sup>, where <sup>α</sup> is the received complex amplitude of the interference.

![](images/ebd60199eb332ff3d06b2845abb0e71c46569c64ff0de3754a53135aec132584.jpg)  
Fig. 3. The receiver architecture (right) of a victim MIMO-FMCW automotive radar that captures both transmitted waveforms from its transmitter (upper left) and an incoherent MIMO-FMCW interfering radar (lower left) with different FMCW configuration parameters, time offset, slow-time Tx-pulse codes, and transmit array configurations.

Interference after Dechirping, Sampling, Range-Doppler FFT and Waveform Separation at Victim Rx: Applying dechirping, sampling, range-Doppler FFT and waveform separation to the received interference signal $s _ { n } ^ { i } ( t )$ , we obtain its range-Doppler spectrum at the <sup>n</sup>-th Rx antenna, <sup>l</sup>-th range bin and <sup>k</sup>-th Doppler bin as $y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { a } _ { t , m } ^ { \prime } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } n }$ , where $\widetilde { f } _ { \phi _ { r } } =$ $d _ { r } \mathrm { s i n } \big ( \widetilde { \phi } _ { r } \big ) / \widetilde { \lambda }$ is the normalized spatial frequency of interference at victim Rx antennas, $\widetilde { a } _ { t , m } ^ { \prime }$ is the complex interference amplitude at its $( l ^ { \prime } , k ^ { \prime } )$ -th range-Doppler bin decoded using $c _ { k , m }$ , the victim radar’s slow-time Tx-pulse code at the <sup>m</sup>-th Tx antenna. The derivation of $y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ and the expression of $\widetilde { a } _ { t , m } ^ { \prime }$ is given in Appendix B.

Spatial-Domain Interference Steering Vector at Victim Rx: Stacking $\{ y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \}$ into a vector, we obtain the interference range-Doppler spectrum on an $M N \times 1$ virtual array

$$
\begin{array} { r } { \mathbf { y } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } . } \end{array}\tag{5}
$$

where

$$
\widetilde { \mathbf { a } } _ { t } ^ { \prime } \triangleq [ \widetilde { a } _ { t , 0 } ^ { \prime } , \widetilde { a } _ { t , 1 } ^ { \prime } , \dots , \widetilde { a } _ { t , M - 1 } ^ { \prime } ] ^ { T } ,\tag{6}
$$

is the $M \times 1$ decoded interference Tx steering signal seen at the victim Rx, and

$$
\widetilde { \mathbf { a } } _ { r } \triangleq [ 1 , e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } } , \hdots , e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } ( N - 1 ) } ] ^ { T }\tag{7}
$$

is the $N \times 1$ interference Rx steering vector.

From (5), it is seen that the spatial-domain interference steering vector also has the Kronecker structure between the Tx and Rx steering vectors, like the spatial-domain object steering vector in (3). The main difference lies in the decoded interference Tx steering vector of (6), which is a function of the transmitting power of the interfering radar, interfering-victim relative distance and Doppler frequency, FMCW time-frequency incoherence (e.g., chirp rate, pulse duration, pulse repetition interval), MIMO incoherence (e.g., slow-time Tx-pulse code and Tx array configuration), and timing offset between the interfering and victim radars. In other words, the object Tx/Rx steering vector and interference Rx steering vector are fully determined by the object-victim and interfering-victim directions due to their Fourier vector structure, while the decoded interference Tx steering vector is almost unknown because its direction in the <sup>M</sup>-dimensional subspace is not only determined by the relative interfering-victim direction but also the mentioned incoherence.

## D. Examples of MIMO-FMCW Interference Signal Model

In the following, we discuss how the MIMO-FMCW interference model in (5) can be applied to two special interference scenarios widely used in the existing literature when certain conditions are met. The detailed derivation in each of the following examples is in Appendix C.

1) Phased Array Radar Interference: When all radars are phased array radar [59] with the slow-time Tx-pulse code $( \{ c _ { k , m } = 1 \} )$ , the spatial-domain interference signal has a Fourier structure. That is, the interference range-Doppler spectrum on a $N \times 1 \ \mathrm { R x }$ array is

$$
\mathbf { y } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { a } _ { t } ^ { \prime } \widetilde { \mathbf { a } } _ { r } .\tag{8}
$$

Note that this interference structure also applies in the special case where all radars adopt a single Tx antenna.

2) TDM-MIMO Radar Interference: When all radars are TDM-MIMO radars [12], the spatial-domain interference signal has the same structure as in (5), i.e.,

$$
\begin{array} { r } { \mathbf { y } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } , } \end{array}\tag{9}
$$

since the TDM-MIMO codes can be regarded as a special case of slow-time Tx-pulse codes, as presented in Section II-A.

## III. PROBLEM FORMULATION

In this section, we formulate object detection as a composite hypothesis testing problem and review existing detectors.

## A. Spatial-Domain Detection Problem Under Interference

Given the target and interference signal models over a given range-Doppler bin, the spatial-domain object detection under mutual interference is formulated as a composite hypothesis testing problem

$$
\left\{ \begin{array} { l l } { \mathcal { H } _ { 0 } , } & { \mathbf { y } = \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } } \\ { \mathcal { H } _ { 1 } , } & { \mathbf { y } = b \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } + \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } , } \end{array} \right.\tag{10}
$$

where $\mathbf { y }$ is the complex-valued range-Doppler spectrum at a given range-Doppler bin, <sup>b</sup> is the complex-valued unknown object amplitude, $Q$ is the number of interference, $\mathbf { a } _ { t }$ and ${ \bf a } _ { r }$ are object Tx and Rx steering vectors defined below $( 3 ) , \widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ and $\widetilde { \mathbf { a } } _ { r , q }$ are the $q \mathrm { . }$ -th decoded interference Tx and Rx steering vectors given in the form of (6) and (7), and the noise $\mathbf z \sim \mathcal L \mathcal N ( \mathbf 0 , \sigma ^ { 2 } \mathbf I _ { M N } )$ <sup>)</sup> with $\sigma ^ { 2 }$ representing the noise variance for spatial-domain signal and IMN representing the identity matrix of size <sup>MN</sup>. The null hypothesis $\mathcal { H } _ { 0 }$ consists of interference and noise, and the alternative hypothesis $\mathcal { H } _ { 1 }$ consists of the object signal plus interference and noise. Note that the looking angle of $\mathbf { a } _ { t } \otimes \mathbf { a } _ { r }$ can be swept over different angle bins for the hypothesis testing and can therefore be considered as known.

## B. Existing Spatial-Domain Detectors

1) Clairvoyant Detector: Assuming the perfect knowledge of the decoded interference Tx steering vector $\{ \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \}$ , the clairvoyant detector is given by

$$
T ^ { C } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } ( \mathbf { y } - \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } ) \right| ^ { 2 } } { \left| \left| \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right| \right| ^ { 2 } } .\tag{11}
$$

It cancels all interference components $\begin{array} { r } { \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } } \end{array}$ before matched filtering to the object steering vector. The probabilities of false alarm and detection of (11) can be derived as

$$
P _ { F A } ^ { C } = e ^ { - \frac { 1 } { 2 } \gamma } , P _ { D } ^ { C } = \mathcal { Q } _ { 1 } \left( \sqrt { \lambda ^ { C } } , \sqrt { \gamma } \right) ,\tag{12}
$$

where $\gamma$ is the threshold used for detection, and the parameter $\lambda ^ { C }$ is given as

$$
\lambda ^ { C } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \left| | \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } | \right| ^ { 2 } = \frac { 2 M N | b | ^ { 2 } } { \sigma ^ { 2 } } .\tag{13}
$$

It is worth noting that the clairvoyant detector of (11) cannot be implemented in practice due to the strong assumption about the knowledge of $\{ \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \}$

2) Receiver Subspace (RS) Detector of [3]: Assuming perfect knowledge of the interference Rx steering vector $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ we can treat $\{ \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \}$ as a nuisance parameter in (10) and estimate it under both hypotheses. The resulting detector based on the generalized likelihood ratio test (GLRT) is given by [3]

$$
T ^ { R S } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left. \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right) ^ { H } \mathbf { y } \right. ^ { 2 } } { \left. \left. \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right. \right. ^ { 2 } } ,\tag{14}
$$

where $\widetilde { \mathbf { A } } _ { r } \triangleq [ \widetilde { \mathbf { a } } _ { r , 1 } , \widetilde { \mathbf { a } } _ { r , 2 } , \hdots , \widetilde { \mathbf { a } } _ { r , Q } ]$ is a stack of $Q$ interference Rx steering vectors. The RS detector suggests using a nullsteering beamformer $\mathbf { w } ^ { R S } = \frac { \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \sim } ^ { \perp } \mathbf { \Phi } \mathbf { a } _ { r } ) } { | | \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \sim } ^ { \perp } \mathbf { \Phi } \mathbf { a } _ { r } ) | | ^ { 2 } }$ that exploits the interference Rx subspace of $\widetilde { \mathbf { A } } _ { r }$ for interference mitigation. The probabilities of false alarm probability and detection of the RS detector are given by

$$
P _ { F A } ^ { R S } = e ^ { - \frac { 1 } { 2 } \gamma } , P _ { D } ^ { R S } = \mathcal { Q } _ { 1 } \left( \sqrt { \lambda ^ { R S } } , \sqrt { \gamma } \right) ,\tag{15}
$$

where

$$
\lambda ^ { R S } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \left| \left| \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right| \right| ^ { 2 } .\tag{16}
$$

3) LCMV Detector of [53]: In [53], a conventional linear constraint minimum variance (LCMV) beamformer is adopted. It models the combined interference and noise as a zero-mean colored Gaussian vector

$$
\sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \widetilde { \mathbf { R } } ) ,\tag{17}
$$

where $\widetilde { \bf R }$ is a normalized covariance matrix. Assuming the perfect knowledge of $\begin{array} { r } { \widetilde { \mathbf { R } } , } \end{array}$ the LCMV solves the following beamforming optimization problem [60]:

$$
\begin{array} { r l } { \underset { \mathbf { w } } { \mathop { \operatorname* { m i n } } } } & { \mathbf { w } ^ { H } \widetilde { \mathbf { R } } \mathbf { w } } \\ { s . t . } & { ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 , } \end{array}\tag{18}
$$

where w denotes a beamformer to be optimized. Problem (18) leads to the LCMV beamformer $\mathbf { w } ^ { L C M V } =$ $\frac { \widetilde { \mathbf { R } } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) } { \left| \left| \widetilde { \mathbf { R } } ^ { - \frac { 1 } { 2 } } \left( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right) \right| \right| ^ { 2 } }$ [60], and the corresponding LCMV detector

$$
{ \cal T } ^ { L C M V } ( { \bf y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \left( \widetilde { \bf R } ^ { - 1 } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right) ^ { H } { \bf y } \right| ^ { 2 } } { \left| \left| \widetilde { \bf R } ^ { - \frac { 1 } { 2 } } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| \right| ^ { 2 } } .\tag{19}
$$

Given the knowledge of $\widetilde { \mathbf { R } } ,$ , the probabilities of false alarm and detection of the LCMV detector are given by

$$
P _ { F A } ^ { L C M V } = e ^ { - \frac { 1 } { 2 } \gamma } , ~ P _ { D } ^ { L C M V } = \mathcal { Q } _ { 1 } \left( \sqrt { \lambda ^ { L C M V } } , \sqrt { \gamma } \right) ,\tag{20}
$$

where

$$
\lambda ^ { L C M V } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \left\| \widetilde { \mathbf { R } } ^ { - \frac { 1 } { 2 } } \big ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \big ) \right\| ^ { 2 } .\tag{21}
$$

## IV. SPATIAL-DOMAIN NON-ADAPTIVE DETECTOR

In the following, we first demonstrate limitations inherited in the RS [3] and LCMV [53] detectors and gain insights through a reformulation of the clairvoyant detector. Then, we propose a generalized subspace (GS) detector that leverages both the Tx and Rx steering vectors of the interference, followed by a comprehensive theoretical performance analysis of its detection performance under mutual interference.

## A. Observations From Existing Detectors

For the RS detector of (14), it projects each interference signal $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } , q = 1 , 2 , \ldots , Q$ to 0, i.e.,

$$
\begin{array} { r } { ( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \widetilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ) ^ { H } ( \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = 0 , } \end{array}\tag{22}
$$

because the interference Rx steering vector $\widetilde { \mathbf { a } } _ { r , q }$ is projected to its orthogonal subspace, i.e., $( \mathbf { P } _ { \widetilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ^ { H } \widetilde { \mathbf { a } } _ { r , q } = \widetilde { 0 }$ . However, this operation fails to maintain the matched filtering gain for the object as

$$
\begin{array} { r } { ( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) = M \mathbf { a } _ { r } ^ { H } \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } < M N , } \end{array}\tag{23}
$$

where <sup>MN</sup> is the coherent matched filtering gain that can be achieved by the clairvoyant detector. This is undesirable, particularly when the interference power is small, as the RS detector may mitigate low-power interference at the price of losing object detection gain.

For the LCMV detector of (19), R is difficult to known a priori and $\sigma ^ { 2 } \widetilde { \mathbf { R } }$ is estimated using the sample covariance matrix [54]

$$
\widetilde { \mathbf { R } } ^ { S } = \frac { 1 } { | \mathcal { X } | } \sum _ { ( l ^ { \prime } , k ^ { \prime } ) \in \mathcal { X } } \widetilde { \mathbf { y } } ( l ^ { \prime } , k ^ { \prime } ) \widetilde { \mathbf { y } } ^ { H } ( l ^ { \prime } , k ^ { \prime } ) ,\tag{24}
$$

where $\widetilde { \mathbf { y } } ( l ^ { \prime } , k ^ { \prime } )$ is the spatial-domain sample at range-Doppler bin $( l ^ { \prime } , k ^ { \prime } )$ , and χ is the set of sample range-Doppler bins. As the LCMV detector in (19) inverses the covariance matrix, using $\frac { \widetilde { \mathbf { R } } ^ { S } } { \sigma ^ { 2 } }$ as the covariance is also known as the sample matrix inversion (SMI) method. The performance of the LCMV detector is sensitive to the estimation error of $\widetilde { \mathbf { R } } ^ { S }$ . However, obtaining an accurate estimate of $\widetilde { \mathbf { R } } ^ { S }$ requires excessive homogeneous samples, which may not be available in practice.

Finally, for the clairvoyant detector of (11), one can decompose the <sup>q</sup>-th decoded interference Tx steering vector along with the object Tx steering vector and its orthogonal complement direction

$$
\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } = \widetilde { b } _ { q } \mathbf { a } _ { t } + \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime }\tag{25}
$$

![](images/54f6f80647080eb08bdea83cbf3b76486cf2ce8b540be33a81179cacb565e2ef.jpg)  
Fig. 4. Decomposition o $\widehat { \mathbf { a } } _ { t , q } ^ { \prime }$ into $\widetilde { b } _ { q } \mathbf { a } _ { t }$ and $\mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ in a 3-D example, where the plane is the orthogonal subspace of $\mathbf { a } _ { t }$

as shown in Fig. 4, where the resulting complex amplitude along $\mathbf { a } _ { t }$ is given as

$$
\widetilde { b } _ { q } = \frac { \mathbf { a } _ { t } ^ { H } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } } { | | \mathbf { a } _ { t } | | ^ { 2 } } .\tag{26}
$$

With (25), the clairvoyant detector of (11) can be rewritten as

$$
T ^ { C } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } ( \mathbf { y } - \sum _ { q = 1 } ^ { Q } \widetilde { b } _ { q } \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) \right| ^ { 2 } } { | | \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } | | ^ { 2 } } ,\tag{27}
$$

which implies that the essential interference to cancel given $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ is a rank-<sup>Q</sup> interference with known directions $\mathbf { a } _ { t } \otimes$ $\widetilde { \mathbf { a } } _ { r , q } , q = 1 , 2 , \ldots , Q .$ , and the unknown parameters sufficient for interference cancellation are $\widetilde { b } _ { q } , q = 1 , 2 , \dots , Q$ . Thus, we call $\widetilde { b } _ { q } , q = 1 , 2 , \dots , Q$ the essential interference complex amplitudes.

## B. Proposed Generalized Subspace (GS) Detector

The exact knowledge of $\widetilde { b } _ { q }$ in the clairvoyant detector in (27) is difficult to determine. However, its power, denoted by $h _ { q } ^ { 2 } ,$ is easier to estimate. To overcome the drawback of the RS detector in Section IV-A, we propose a new detector that mitigates interference based on the interference power. We first assume perfect knowledge of $\{ h _ { q } ^ { 2 } \}$ and then relax this assumption in Section V.

We model $\widetilde { b } _ { q } \sim \mathcal { C N } ( 0 , h _ { q } ^ { 2 } )$ with variance $h _ { q } ^ { 2 }$ and $\widetilde { b } _ { q }$ is independent of the noise z. Similar to the RS detector, we assume perfect knowledge of the interference Rx steering vector $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ Then, the essential interference plus noise is

$$
\widetilde { \mathbf { z } } \triangleq \sum _ { q = 1 } ^ { Q } \widetilde { b } _ { q } \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \mathbf { R } ) ,\tag{28}
$$

and the normalized covariance of z is

$$
\mathbf { R } = \sum _ { q = 1 } ^ { Q } \frac { h _ { q } ^ { 2 } } { \sigma ^ { 2 } } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } + \mathbf { I } _ { M N } .\tag{29}
$$

To obtain a detector that leverages the statistics R, we first design an Rx beamformer w to satisfy the following criterion:

1) minimize the variance of interference-plus-noise with known covariance after beamforming, i.e., $\mathbf { w } ^ { H }$ Rw;

2) maintain a fixed gain at the object direction, i.e., $\left( \mathbf { a } _ { t } \otimes \right.$ $\begin{array} { r } { \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 ; } \end{array}$

3) force the unknown interference $\begin{array} { r } { \sum _ { q = 1 } ^ { Q } ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r , q } } \end{array}$ to zero for any $\widetilde { \mathbf { a } } _ { t } ^ { \prime } .$ , i.e.,

$$
\sum _ { q = 1 } ^ { Q } ( ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = 0 ,\tag{30}
$$

for any $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } , q = 1 , 2 , \ldots , Q$ , which is equivalent to force $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \mathbf { \tilde { a } } _ { r , q } ^ { \perp } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , q = 1 , 2 , \ldots , Q$ , where ${ \bf 0 } _ { M }$ denotes the <sup>M</sup>-dimensional column vector with all 0 elements.

As a result, one needs to solve the following beamforming optimization problem:

$$
\begin{array} { r l } { \underset { \mathbf { w } } { \mathop { \operatorname* { m i n } } } } & { \mathbf { w } ^ { H } \mathbf { R } \mathbf { w } } \\ { s . t . } & { ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 , } \\ & { ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , q = 1 , 2 , \dots , Q . } \end{array}\tag{31}
$$

Compared to the LCMV beamforming optimization problem in (18), the objective function of the problem in (31) is different in that it uses the essential interference plus noise covariance matrix R instead of the total interference plus noise covariance matrix R .

Theorem 1: The optimal solution of problem (31) is

$$
\mathbf { w } ^ { G S } = \frac { \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) } { \left| \left| \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right| \right| ^ { 2 } } = \frac { \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) } { M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } } ,\tag{32}
$$

where $\widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \triangleq \mathbf { I } _ { N } - \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda }$ with

$$
\widetilde { { \bf P } } _ { \widetilde { { \bf A } } _ { r } , \Lambda } \triangleq M \widetilde { { \bf A } } _ { r } ( \Lambda ^ { - 1 } + M \widetilde { { \bf A } } _ { r } ^ { H } \widetilde { { \bf A } } _ { r } ) ^ { - 1 } \widetilde { { \bf A } } _ { r } ^ { H }\tag{33}
$$

representing the regularized projection matrix, and

$$
\begin{array} { r } { \mathbf { \Lambda } \triangleq \operatorname { d i a g } \left[ \cfrac { h _ { 1 } ^ { 2 } } { \sigma ^ { 2 } } , \cfrac { h _ { 2 } ^ { 2 } } { \sigma ^ { 2 } } , \dots , \cfrac { h _ { Q } ^ { 2 } } { \sigma ^ { 2 } } \right] , } \end{array}\tag{34}
$$

is the essential-interference-to-noise-ratio (EINR) matrix with diagonal elements reflecting the power values of <sup>Q</sup> essential interferences over the noise.

Proof: This proof is based on the following observation:

$$
\mathbf { R } ^ { - 1 } = \mathbf { I } _ { M N } - \mathbf { P _ { a } } \otimes { \widetilde { \mathbf { P } } } _ { { \widetilde { \mathbf { A } } } _ { r } , { \pmb { \Lambda } } } .\tag{35}
$$

For more details, refer to Appendix D.

The beamformer $\mathbf { w } ^ { G S }$ suggests the following detector

$$
\begin{array} { l } { { \displaystyle { T ^ { G S } } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \left( \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right) ^ { H } \mathbf { y } \right| ^ { 2 } } { \left| \left| \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right| \right| ^ { 2 } } } \ ~ } \\ { { \displaystyle ~ = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \left( \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) \right) ^ { H } \mathbf { y } \right| ^ { 2 } } { M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } } } . } \end{array}\tag{36}
$$

Because $T ^ { G S } ( \mathbf { y } )$ uses the Rx-side interference information $\widetilde { \mathbf { A } } _ { \scriptscriptstyle \mathit { 1 } }$ and the Tx-side interference information Λ, we call the detector $T ^ { G S } ( \mathbf { y } )$ as the generalized subspace-based (GS) detector. From (36), the interference is mitigated using the Rx array, which is the same as the RS detector. Thus, the GS detector works when the number of interference $Q \leq N$

## C. Theoretical Performance Analysis

Theorem 2: Based on the assumption $\widetilde { b } _ { q } \sim \mathcal { C N } ( 0 , h _ { q } ^ { 2 } )$ with known $h _ { q } ^ { 2 } , q = 1 , 2 , \ldots , Q$ , the probabilities of false alarm and detection for the GS detector under problem (10) are given as

$$
P _ { F A } ^ { G S } = e ^ { - \frac { 1 } { 2 } \gamma } , P _ { D } ^ { G S } = \mathcal { Q } _ { 1 } \left( \sqrt { \lambda ^ { G S } } , \sqrt { \gamma } \right) ,\tag{37}
$$

where $\gamma$ is the detection threshold and

$$
\lambda ^ { G S } = \frac { 2 \lvert b \rvert ^ { 2 } } { \sigma ^ { 2 } } M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } } ^ { \perp } \mathbf { a } _ { r } .\tag{38}
$$

Proof: See Appendix E.

From the above closed-form expressions of probabilities of false alarm, we have the following Corollary:

Corollary 1: From (37), the proposed GS detector is a constant false alarm rate (CFAR) detector in the existence of MIMO-FMCW mutual interference.

Remark 1: This CFAR property is ensured by zero-forcing the unknown interference in the last condition in problem (31), i.e., $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , q = 1 , 2 , \ldots , Q$ , and the whitening of the essential interference plus noise using knowledge of R.

Corollary 2: The proposed GS detector reduces to the clairvoyant detector of (11) when the decoded interference Tx steering vectors $\{ \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \}$ are orthogonal to the object Tx steering vector $\mathbf { a } _ { t } , \mathrm { i . e . }$ , the EINR matrix $\begin{array} { r } { \Lambda = { \bf 0 } . } \end{array}$

Proof: Λ <sup>=</sup> 0 implies that $\widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } } ^ { \perp } = \mathbf { I } _ { N }$ . Thus,

$$
{ \cal T } ^ { G S } ( { \bf y } ) = { \cal T } ^ { C } ( { \bf y } ) = \frac { 2 | \left( { \bf a } _ { t } \otimes { \bf a } _ { r } \right) ^ { H } { \bf y } | ^ { 2 } } { \sigma ^ { 2 } M N }\tag{39}
$$

with $\lambda ^ { G S } = \lambda ^ { C } = 2 M N | b | ^ { 2 } / \sigma ^ { 2 }$

Corollary 3: The proposed GS detector reduces to the RS detector of (14) when the projected interference power along the object Tx steering vector approaches infinity, i.e., the EINR matrix $\pmb { \Lambda }  \mathrm { d i a g } [ \infty , \infty , \ldots , \infty ]$

Proof: In this case, we have $\widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } } = \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } } =$ $\widetilde { \mathbf { A } } _ { r } \big ( \widetilde { \mathbf { A } } _ { r } ^ { H } \widetilde { \mathbf { A } } _ { r } \big ) ^ { - 1 } \widetilde { \mathbf { A } } _ { r } ^ { H }$ and $\widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } } ^ { \perp } = \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } } ^ { \perp }$ . As a result, the proposed GS detector of (36) reduces to the RS detector of (14) with $\lambda ^ { G S } = \lambda ^ { R S } = 2 M | b | ^ { 2 } ( \mathbf { a } _ { r } ^ { H } \mathbf { P } _ { \widetilde { \mathbf { \Gamma } } } ^ { \perp } \mathbf { \Phi } \mathbf { a } _ { r } ) / \sigma ^ { 2 }$

Corollary 4: From the probabilities of false alarm and detection of the clairvoyant in (12), RS in (15) and the proposed GS detectors in Theorem 2, the detection performance is in the order of

$$
P _ { D } ^ { R S } \leq P _ { D } ^ { G S } \leq P _ { D } ^ { C }\tag{40}
$$

for a given probability of false alarm.

Proof: It is first noted that, for a given probability of false alarm, the detection threshold $\gamma$ holds the same for all three detectors. Then, from Corollary 2 and Corollary 3, we

$$
0 < \lambda ^ { R S } \leq \lambda ^ { G S } \leq \lambda ^ { C } ,\tag{41}
$$

when the diagonal elements of EINR matrix Λ is no smaller than 0 and finite. Finally, the probability of detection or, equivalently,

the generalized Marcum Q-function $\mathcal { Q } _ { 1 } ( \sqrt { \lambda } , \sqrt { \gamma } )$ of order 1 monotonically increases with $\sqrt { \lambda } \ [ 5 5 ]$ 

Remark 2: For the GS detector of (36), the projected <sup>q</sup>-th interference residual is

$$
\left( \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) \right) ^ { H } ( \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = \widetilde { b } _ { q } M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \widetilde { \mathbf { a } } _ { r , q } ,\tag{42}
$$

and the object correlation gain is

$$
\left( \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) \right) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) = M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } .\tag{43}
$$

Compared to the results of the RS detector in (22) and (23), the proposed GS detector achieves a balance between interference mitigation gain and object correction gain.

Remark 3: With perfect knowledge of $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ and Λ, the GS detector is equivalent to the LCMV detector with perfect knowledge of R in (17). This equivalence can be demonstrated by showing that $\mathbf { w } ^ { G S }$ in (32) is also the optimal solution to the LCMV beamforming optimization problem (18). Thus, according to (40), the ideal LCMV detector outperforms the RS detector. However, as we will show later, when the LCMV detector is used with the SMI method (LCMV-SMI), its performance can degrade significantly due to the estimation error of $\widetilde { \bf R }$ in (17).

## V. SPATIAL-DOMAIN ADAPTIVE DETECTOR

In the previous section, the proposed GS detector is shown to rely on the knowledge of essential interference plus noise covariance matrix R in (29). However, R depends on the power of essential interference $\{ h _ { q } ^ { 2 } \}$ , the interference Rx steering vector $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ , and the number of interferences $Q ,$ which are difficult to estimate accurately in practice. If the estimated number of interference is smaller than the actual number <sup>Q</sup>, the performance of interference mitigation degrades significantly. Thus, instead of explicitly estimating these parameters, we propose a novel variation of the interference covariance matrix reconstruction method [61]. This method reconstructs R over a broad interference region of interest based on the knowledge of $\widetilde { \mathbf { R } } ^ { S }$ in (24) and the interference structure. We refer to the GS detector with the reconstructed R as the adaptive GS (AGS) detector.

## A. Capon Spatial Power of Essential Interference

Before introducing the AGS detector, we present the following preliminary result. We first obtain spatial-domain samples $\{ \widetilde { \mathbf { y } } ( l ^ { \prime } , k ^ { \prime } ) , ( l ^ { \prime } , k ^ { \prime } ) \in \chi \}$ from adjacent range-Doppler bins, where χ and the range-Doppler bin of y are separated by guard bins to avoid including the sidelobe of target-of-interest [54]. This leads to

$$
\widetilde { \mathbf { y } } = \widetilde { \mathbf { z } } + \sum _ { q = 1 } ^ { Q } ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r , q } ,\tag{44}
$$

where the notation $( l ^ { \prime } , k ^ { \prime } )$ is omitted for convenience and $\widetilde { \mathbf { z } } \sim$ ${ \mathcal { C N } } ( \mathbf { 0 } , \sigma ^ { 2 } \mathbf { R } )$ is given in (28). Similar to the one in (31), we can design a Rx beamformer to find the <sup>q</sup>-th essential interference as follows:

$$
\begin{array} { r l } { \underset { \mathbf { w } } { \mathop { \operatorname* { m i n } } } } & { \mathbf { w } ^ { H } \mathbf { R } \mathbf { w } } \\ { s . t . } & { ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = 1 , } \\ & { ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , q = 1 , 2 , \dots , Q , } \end{array}\tag{45}
$$

where the first constraint ensures a fixed gain at the direction $\mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ,$ and the last constraint forces the unknown interference to be zero. The solution to (45) is given by

$$
\mathbf { w } _ { q } ^ { G S } = \frac { \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) } { \lVert \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) \rVert ^ { 2 } } .\tag{46}
$$

Then, we define the normalized Capon spatial power of the <sup>q</sup>-th essential interference as

$$
P _ { q } \triangleq \left( \mathbf { w } _ { q } ^ { G S } \right) ^ { H } \mathbf { R } \left( \mathbf { w } _ { q } ^ { G S } \right) ,\tag{47}
$$

which is an estimate of $h _ { q } ^ { 2 } / \sigma ^ { 2 }$ in (29).

Lemma 1: The normalized Capon spatial power of the <sup>q</sup>-th essential interference is equivalent to

$$
P _ { q } = \frac { 1 } { ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \widetilde { \mathbf { R } } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) } ,\tag{48}
$$

where $\widetilde { \bf R }$ is the normalized covariance matrix of the entire interference plus noise defined in (17).

Proof: See Appendix F.

Lemma 1 reveals the important connection between the normalized Capon spatial power $P _ { q }$ and $\widetilde { \bf R }$ , which inspires the design of the following adaptive GS detector.

## B. Proposed Adaptive Generalized Subspace (AGS) Detector

Inspired by Lemma 1, we estimate the essential interference power spectrum using a Capon spatial spectrum estimator

$$
\widehat { P } ( \theta ) = \frac { 1 } { \left( \mathbf { a } _ { t } \otimes \mathbf { \widetilde { a } } _ { r } ( \theta ) \right) ^ { H } \left( \widetilde { \mathbf { R } } ^ { S } \right) ^ { - 1 } \left( \mathbf { a } _ { t } \otimes \mathbf { \widetilde { a } } _ { r } ( \theta ) \right) } .\tag{49}
$$

By (29), we reconstruct the normalized essential interference plus noise covariance matrix as:

$$
\widehat { \mathbf { R } } = \sum _ { \theta \in \widetilde { \Theta } } \varrho \widehat { P } ( \theta ) \left( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ( \theta ) \right) \left( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ( \theta ) \right) ^ { H } + \mathbf { I } _ { M N } ,\tag{50}
$$

where $\widetilde { \Theta }$ is a set of potential interference angles of arrival and $\varrho$ is a scaling factor. One can form $\widetilde { \Theta }$ as a uniform grid by sampling from a coarse interference region $\widetilde { \Theta } ^ { I } \subset [ - \pi / 2 , \overline { { \pi } } / 2 ]$ with a grid size $\Delta \theta .$ . The coarse interference region $\widetilde { \Theta } ^ { I }$ can be determined by identifying all <sup>θ</sup> such that $\widehat P ( \boldsymbol { \theta } )$ is above the minimum eigenvalue of $\widetilde { \mathbf { R } } ^ { S }$ [62]. By replacing R in (32) and (36) by $\widehat { \mathbf { R } }$ , we obtain the AGS beamformer as

$$
\mathbf { w } ^ { A G S } = \frac { \widehat { \mathbf { R } } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) } { \lVert \widehat { \mathbf { R } } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \rVert ^ { 2 } } ,\tag{51}
$$

and the corresponding AGS detector as

$$
T ^ { A G S } ( { \bf y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { | ( \widehat { \bf R } ^ { - 1 } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) ) ^ { H } { \bf y } | ^ { 2 } } { \| \widehat { \bf R } ^ { - \frac { 1 } { 2 } } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \| ^ { 2 } } .\tag{52}
$$

Note that the performance of the proposed AGS scheme depends on the choice of scaling factor $\varrho .$ The larger the $\varrho ,$ the deeper null of the angle spectrum (defined as $\textstyle { \frac { \sigma ^ { 2 } } { 2 } } T ^ { A G S } ( \mathbf { y } ) )$ ) at the angles in ${ \widetilde { \Theta } } .$ . When $\widetilde { \Theta }$ is exactly the set of interference angles (an ideal case), we can set $\begin{array} { r } { \varrho = \frac { 1 } { \sigma ^ { 2 } } } \end{array}$ such that R is a good estimate of R. However, in more typical scenarios where $\widetilde { \Theta }$ contains more angles than the set of interference angles, $\varrho$ can be adjusted to balance interference mitigation and object correlation gain.

Algorithm 1: Proposed AGS Beamformer & Detector.   
Input: Spatial-domain signal of interest y, Capon spatial   
spectrum grid size $\Delta \theta ,$ Capon spatial spectrum scaling   
factors $\varrho ,$ spatial-domain samples $\{ \widetilde { \mathbf { y } } ( l ^ { \prime } , k ^ { \prime } ) , ( l ^ { \prime } , k ^ { \prime } ) \in \overset { \cdot } { \chi } \}$   
Output: Proposed AGS beamformer $\dot { \mathbf { w } } ^ { A G \dot { S } }$ , proposed   
AGS detector $T ^ { A G S } ( \mathbf { y } )$   
1: Calculate sample matrix $\widetilde { \mathbf { R } } ^ { S }$ in (24)   
2: Obtain Capon spatial spectrum estimator $\widehat { P } ( \theta )$ in (49)   
3: Detect coarse interference region $\widetilde { \Theta } ^ { I } \subset [ - \pi / 2 , \pi / 2 ]$   
from $\widehat P ( \boldsymbol { \theta } )$ using the minimum eigenvalue of $\widetilde { \mathbf { R } } ^ { S }$ as the   
threshold   
4: Obtain $\widetilde { \Theta }$ via sampling $\widetilde { \Theta } ^ { I }$ with grid size $\Delta \theta$   
5: Calculate R in (50)   
6: Obtain $\mathbf { w } ^ { A G S }$ in (51) and $T ^ { A G S } ( \mathbf { y } )$ in (52)

The AGS scheme is summarized in Algorithm 1. The AGS scheme combines the benefits of the non-adaptive GS scheme and the adaptive LCMV-SMI scheme, as it uses the sample covariance matrix to eliminate the requirement of the knowledge of $\{ h _ { q } ^ { 2 } \} , \{ \widetilde { \mathbf { a } } _ { r , q } \}$ and $Q$ and also exploits the structure of the essential interference plus noise matrix via (50).

Remark 4: The angle of $\mathbf { a } _ { t }$ and $\mathbf { a } _ { r }$ is swept over different angle bins to check the presence of targets. When the angle corresponds to an interference angle, we set $\widetilde { \Theta } ^ { I }$ to include the current angle to suppress the interference. Therefore, we do not further exclude the angle from $\widetilde { \Theta } ^ { I }$ as in [61]. When the angle is swept at the true target angle and the interference is in a different direction, $\widetilde { \Theta } ^ { I }$ typically does not contain the target angle due to the coarse interference region detection step in Algorithm 1, thus avoiding target self-suppression.

## VI. PERFORMANCE EVALUATION

In this section, simulation results are provided to demonstrate the performance of different spatial-domain schemes under incoherent MIMO-FMCW mutual interference. We compare the GS and AGS schemes with other spatial-domain schemes including clairvoyant scheme, RS scheme [3], and LCMV scheme [53] with SMI, in two simulation scenarios:<sup>2</sup>

\- Synthetic data: the spatial-domain object and interference signal models are directly synthesized according to the model derived in Section II. Specifically, the object signal model is generated according to (3), while the interference signal model is directly generated using (5).

\- System-level simulation data: the received object and interference waveforms go through all necessary steps (LO,

LPF, ADC, Rang/Doppler FFT, MIMO waveform separation) at the victim Rx of Fig. 3 with the help of MATLAB Phased Array System Toolbox<sup>TM</sup>. The simulation accounts for waveform generation, Tx/Rx antenna beampatterns, residuals due to the LPF and imperfect MIMO waveform separation, and spectrum leakage due to the presence of other objects and interferences.

## A. Performance Evaluation Using Synthetic Data

We consider a victim MIMO-FMCW radar with $M = 4$ Tx antennas and $N = 4$ Rx antennas. The inter-element spacing values at the victim Rx and Tx are $d _ { r } = 0 . 5 \lambda$ and $d _ { t } = N d _ { r }$ respectively. We generate the spatial-domain object signal in (3) by feeding an object angle at $\phi _ { t } = \phi _ { r } = 3 0 ^ { \circ }$ to the object Tx and Rx steering vectors, respectively.

We consider two mutually independent MIMO-FMCW interferences located at $4 0 ^ { \circ }$ and 10<sup>◦</sup>. We first construct the interference Rx steering vectors $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ according to (7) using the two interference angles. For the interference Tx steering vector, since it is incoherent and we have no prior knowledge about interference Tx, we generate it as a random $M \times 1$ vector pointing to an unknown direction in the <sup>M</sup>-dim subspace $\tilde { \mathbf { a } } _ { t , q } ^ { \prime } \sim \mathcal { \bar { C N } } ( \mathbf { 0 } , \widetilde { \sigma } _ { q } ^ { 2 } \widetilde { \mathbf { R } } _ { t , q } )$ , where $\widetilde { \sigma } _ { q } ^ { 2 }$ is the power of the <sup>q</sup>-th interference and $\widetilde { \mathbf { R } } _ { t , q }$ is the covariance matrix with diagonal of 1. Note that the direct and random generation of $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ ignores the interference Tx configurations and relative geometry between the interference and victim Rx. It provides a simple and computationally efficient way to emulate the interference Tx steering vector in all possible configurations (FMCW, array configurations, and relative interference-victim geometry) and verify our theoretical performance analysis. In our simulation, we set $\widetilde { \mathbf { R } } _ { t , q } \triangleq [ \widetilde { R } _ { q , i , j } \ ] _ { i , j = 0 } ^ { M - 1 } = [ \rho _ { q } ^ { | i - j | } ] _ { i , j = 0 } ^ { M - 1 }$ with $\rho _ { 1 } = 0 . 6$ and $\rho _ { 2 } = 0 . 5$ for the two interferences. We define the signal-tonoise-ratio (SNR) as $\mathrm { S N R } = | b | ^ { 2 } / \sigma ^ { 2 }$ and set it as −5 dB, while the interference-to-noise-ratio (INR) is set as $\mathrm { I N R } = \widetilde { \sigma } _ { q } ^ { 2 } / \sigma ^ { 2 }$ where $\sigma ^ { 2 }$ is the noise variance.

The performance is evaluated in terms of the receiver operating characteristic (ROC) by using $1 0 ^ { 6 }$ Monte Carlo trials. For each Monte Carlo run, the interference Tx steering vector and noise are randomly generated as specified above, while the interference Rx steering vector and object Tx/Rx steering vectors are fixed according to the specified interference and object angles. We compute $\bar { T } ^ { C } ( \mathbf { y } )$ with the knowledge of $\{ \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \}$ and $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ , compute $T ^ { R S } ( \mathbf { y } )$ with the knowledge of $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ , and compute ${ \dot { T } } ^ { G S } ( \mathbf { y } )$ with the knowledge of $\{ \widetilde { \mathbf { a } } _ { r , q } \}$ and $\{ h _ { q } ^ { \bar { 2 } } \}$ . On the other hand, the LCMV-SMI detector and the AGS detector require the knowledge of the sample matrix $\widetilde { \mathbf { R } } ^ { S }$ . We generate <sup>MN</sup> and 2<sup>MN</sup> of independently and identically distributed $\widetilde { \mathbf { y } }$ samples to calculate the two resulting $\widetilde { \mathbf { R } } ^ { S }$ and show their impact on the detection performance of the LCMV-SMI detector and the AGS detector.

Fig. 5(a) verifies the derived theoretical performance (denoted by lines) in Theorem 1 of Section IV-B for the proposed GS detector and compares it with empirical ROC curves (denoted by markers) when the $\mathrm { I N R } = \{ - 1 5 , - 1 0 , - 5 \}$ dB. A good agreement between the theoretical and empirical ROC curves is observed in Fig. 5(a). When the INR decreases or, equivalently, the interference is weaker, the probability of detection increases for a given probability of a false alarm.

![](images/4036b419eef7eb68552a73130c01a1004cbbce299ff37fb8e1db8cfa9058227b.jpg)  
(a)

![](images/55a6cf572ffecb139d861eb97244d92b81fd39e723ea40c26b5fa99fac08c86f.jpg)  
(b)  
Fig. 5. Receiver operating characteristic (ROC) curves when $M = 4 , N = 4 ,$ and $\mathrm { S N R } = - 5 \mathrm { d B }$ in the presence of an object at $3 0 ^ { \circ }$ and two interferences at 40<sup>◦</sup> and 10<sup>◦</sup>: (a) Comparison of theoretical (lines) and empirical Monte Carlo (markers) ROC curves of the proposed GS detector when $\mathrm { I N R } { = \{ - 1 5 , - 1 0 , - 5 \} }$ dB; (b) Empirical Monte Carlo comparison between the proposed GS detector, the proposed AGS detector, and baseline methods.

![](images/24f54a1805a957814a5be563e678b6b5a1f867d311d01a4eb62481fe5d388cb0.jpg)  
Fig. 6. Qualitative comparison of the angle spectrums at a given range-Doppler bin.

Fig. 5(b) further compares the proposed GS detector and AGS detector (realized in Algorithm 1 at $\Delta \theta = 1 ^ { \circ } , \varrho = 1 0 )$ with the three baseline detectors in terms of ROC curves when the INR of the two interference is fixed to −10 dB. The clairvoyant detector, although not practical, gives the detection performance upper bound for all detectors. Compared with the RS detector, the proposed GS detector shows a significant improvement. For instance, when the probability of false alarm is 0.1, the probability detection is boosted from 0.2 of the RS detector to about 0.65 of the proposed GS detector. Compared to the GS detector and the LCMV-SMI detector, the proposed AGS detector achieves the performance in between and can approach the performance of the GS detector when the number of samples for calculating the sample matrix is large. When the number of samples drops to <sup>MN</sup>, the performance of the LCMV-SMI detector drops significantly and is even worse than the RS detector, while the performance of the proposed AGS detector is more robust.

TABLE I  
VICTIM AND INTERFERING MIMO-FMCW RADAR CONFIGURATION FOR SYSTEM-LEVEL SIMULATION
<table><tr><td rowspan=1 colspan=1>Setup</td><td rowspan=1 colspan=1>Explanations</td></tr><tr><td rowspan=1 colspan=1>RF wavelength</td><td rowspan=1 colspan=1>3.9 mm</td></tr><tr><td rowspan=1 colspan=1>Tx (Rx) array structure</td><td rowspan=1 colspan=1>Uniform linear array</td></tr><tr><td rowspan=1 colspan=1>MIMO Tx-pulse code</td><td rowspan=1 colspan=1>Chu sequence</td></tr><tr><td rowspan=1 colspan=1>Chirp bandwidth</td><td rowspan=1 colspan=1>460 MHz</td></tr><tr><td rowspan=1 colspan=1>IF bandwidth (ADC complex sample rate)</td><td rowspan=1 colspan=1>15 MHz (16.7 MHz)</td></tr><tr><td rowspan=1 colspan=1>Number of chirps in a CPI</td><td rowspan=1 colspan=1>256</td></tr><tr><td rowspan=1 colspan=1>Range, velocity, angle FFT sizes</td><td rowspan=1 colspan=1>1024, 256, 32</td></tr><tr><td rowspan=1 colspan=1>Object RCS model</td><td rowspan=1 colspan=1>Non-fluctuating 20dBsm</td></tr><tr><td rowspan=1 colspan=1>Object (interference) channel</td><td rowspan=1 colspan=1>Free-space two-way(one-way) channel</td></tr><tr><td rowspan=1 colspan=1>Victim radar chirp slope</td><td rowspan=1 colspan=1>15 MHz/us</td></tr><tr><td rowspan=1 colspan=1>Victim radar chirp (idle) duration</td><td rowspan=1 colspan=1>30.7 us (7 us)</td></tr><tr><td rowspan=1 colspan=1>Victim Tx (Rx) element spacing</td><td rowspan=1 colspan=1>15.6 mm (1.95 mm)</td></tr><tr><td rowspan=1 colspan=1>Victim Tx (Rx) antenna number</td><td rowspan=1 colspan=1>4 (8)</td></tr><tr><td rowspan=1 colspan=1>Interfering Tx (Rx) element spacing</td><td rowspan=1 colspan=1>3.9 mm (1.95 mm)</td></tr><tr><td rowspan=1 colspan=1>Interfering Tx (Rx) antenna number</td><td rowspan=1 colspan=1>8 (2)</td></tr></table>

## B. Performance Evaluation Using System-Level Simulation

We now consider a system-level simulation by generating the source MIMO-FMCW waveforms with all signal processing steps at the victim Rx sides using MATLAB Phased Array System Toolbox<sup>TM</sup>. In Table I, we specify the MIMO-FMCW radar configuration for both victim and interfering radar. We model the interference channel as a free-space one-way propagation channel and the object channel as a two-way channel. This makes the power of the received interference stronger than the power of the received object signal.

![](images/94dd5299e41034df88d2386b748309229ba29e8a122c90e82eee8db9d9dc89d2.jpg)  
(a)

![](images/94ba98a5fceca93838b4e38fe6a877b08140564e69855fa7b969c2dc08b788d2.jpg)  
(b)

![](images/22f6ddd580490ec49c2afb8d505c170e1b17f8b6d9aa515e608591e3364e1d07.jpg)  
(c)

![](images/24f5ce2694b09df688c804943886f8dfe8304727e61f74c87d1fbf1fa8481ed2.jpg)  
(d)

![](images/8fb9b81100ae6c32dc5b3076419e998720cda2caf81845cfb0111e760e621253.jpg)  
(e)

![](images/ca9bc4f92f2aeb5dc1183542f60406dd39be8cc3a6352a9daeda38b872978347.jpg)  
(f)  
Fig. 7. Qualitative comparison of the range-angle spectra (at the Doppler bin of object 1) with 2 objects and 2 interferences. (a) FFT. (b) Clairvoyant. (c) RS. (d) Proposed GS. (e) LCMV-SMI. (f) Proposed AGS.

![](images/2cbe06cb6acda997cdb9dd9e0c20621e7937d2b5787b4af9e3b7d7ceaf160e5c.jpg)  
Fig. 8. CDF of output interference power (OIP) at the interference angle region over 1000 Monte Carlo runs.

For the LCMV-SMI and AGS detectors, we choose the sample range-Doppler bin set χ as a set around the target-of-interest with the number of range (Doppler) guard bins on each side to be 8 (4) and the number of training range/Doppler bins on each side to be 4. This lead to $| x | = 6 4$ (equivalent to 2<sup>MN</sup>) range-Doppler bins for obtaining the sample matrix $\widetilde { \mathbf { R } } ^ { S }$ . The parameters of the AGS detector are $\Delta \theta = 1 ^ { \circ } , \varrho = 1 0$

We first provide qualitative results for all considered methods using the angle spectrum, which is defined as ${ \frac { \sigma ^ { 2 } } { 2 } } T ( \mathbf { y } )$ given the detection statistics $T ( \mathbf { y } )$ of a scheme. We consider a scenario of 2 objects and 2 incoherent interfering radars. The two objects are at $3 5 . 5 ~ \mathrm { m } , \ : - 2 . 9 ~ \mathrm { m } / \mathrm { s } , \ : - 1 . 2 ^ { \circ }$ and, respectively, 81.0 m, 4.2 m/s, 11<sup>.</sup>2<sup>◦</sup>. The two interfering radar are at 1.8 m, 1.3 m/s, $- 5 4 . 0 ^ { \circ }$ and, respectively, 2.3 m, −12<sup>.</sup>8 m/s, −48<sup>.</sup>1<sup>◦</sup>. Fig. 6 shows the angle spectrum of different detectors at the object 1’s range-Doppler bin. As a baseline, we include the angle FFT. It is seen that the interference-ignoring angle FFT yields strong sidelobes around the vicinity of the two interference angles. All other detectors show interference mitigation capability at the two interference angles. The LCMV-SMI detector shows a stronger sidelobes around these angles due to its sensitivity to the sample matrix estimation error. The RS, GS and AGS detectors show better interference mitigation performance at the region of interference angles, while the clairvoyant detector shows smaller sidelobes over all angles.

Fig. 7 shows range-angle spectrum of all detectors by varying both angle and range bins while fixing the Doppler bin at the object 1’s Doppler bin, under the same setup of Fig. 6. Fig. 7(a) shows that when the angle FFT is used, the interference is a wideband signal over the range bins, because the dechirped incoherent interference is a chirp-like signal and it significantly raises the noise level in the range-angle domain [35]. On the other hand, the clairvoyant detector in Fig. 7(b) provides the best benchmark performance and cancels two interferences completely. Fig. 7(c) to (f) show the range-angle spectrum of the RS, GS, LCMV-SMI, and AGS detectors. Compared to the angle FFT, the detectors in Fig. 7(c) to (f)(f) show improved spectrum with smaller sidelobes, lower noise floors, and suppressed interference around their angles. The proposed GS detector achieves approximately the same performance as the RS detector under strong interference, as stated in Corollary 3. The proposed AGS detector achieves deeper null at the interference angle and smaller interference residuals compared to the LCMV-SMI detector.

We further provide quantitative performance evaluation of all considered methods using the system-level simulation data with the Monte Carlo simulation of 1000 runs. For each Monte Carlo run, we consider one interference; we randomly select the interference angle in the interval of $[ - 8 0 ^ { \circ } , 8 0 ^ { \circ } ]$ and randomly select the interference range between [2,4] m (strong interference), while specifying other parameters in Table I. We define the interference angle region as 5 angle bins covering the true interference angle bin with the true interference angle bin at the center, and define the output interference power (OIP) as the averaged range-angle spectrum over all range bins at the interference angle region. It is expected that the better the interference mitigation performance, the lower the OIP over the interference angle region. Fig. 8 shows the cumulative distribution functions (CDFs) of the OIPs of all detectors. It is seen that in most regions of the CDFs of the OIPs, the clairvoyant detector is better than other detectors; the proposed GS detector, the RS detector, and the proposed AGS detector have similar performance in the middle OIP region; the proposed AGS detector outperforms the LCMV-SMI detector in all OIP regions; the AGS detector achieves 37.5dB gain over the LCMV-SMI detector in terms of the medium of the OIP (the point where its CDF is 0.5).

## VII. CONCLUSION

We investigated mutual radar interference mitigation for incoherent MIMO-FMCW automotive radar. By deriving an explicit incoherent MIMO-FMCW interference signal model, we formulated the mutual interference mitigation as a spatial-domain object detection problem. We proposed a non-adaptive GS detector by exploiting the Tx-side information and an adaptive version, the AGS detector, by leveraging the structure of the interference. Using synthetic and system-level simulation data, analytical and empirical performance evaluations confirmed the effectiveness of the proposed detectors compared to a range of baseline methods.

## APPENDIX A DERIVATION OF OBJECT SIGNAL MODEL

In the following, we show the derivation of the object signal model following the steps in the upper right of Fig. 3.

Local Oscillator (LO): At the <sup>n</sup>-th Rx antenna of the victim radar, the backscattered object signal <sup>α</sup> $\begin{array} { r } { \sum _ { m = 0 } ^ { M - 1 } s _ { m } ( t - \tau _ { m , n } ( t ) ) } \end{array}$ ) is mixed with the conjugate of the LO signal $\textstyle \sum _ { k = 0 } ^ { K - 1 } s ^ { * } ( t -$ $k T _ { \mathrm { P R I } } ) e ^ { - j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } ) }$ , leading to the dechirped baseband analog signal

$$
\begin{array} { r l r } {  { a _ { n } ^ { s } ( t ) = \alpha _ { \tau } \sum _ { m = 0 } ^ { M - 1 } e ^ { - j 2 \pi f _ { c } \frac { 2 v t } { c } } e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } } } \\ & { } & { \times \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } e ^ { - j 2 \pi \beta ( t - k T _ { \mathrm { P R I } } ) \tau } D _ { \tau , T } ( t - k T _ { \mathrm { P R I } } ) , } \end{array}\tag{53}
$$

where $\alpha _ { \tau } \triangleq \alpha e ^ { - j 2 \pi f _ { c } \tau } e ^ { j \pi \beta \tau ^ { 2 } }$ with <sup>α</sup> denoting the complex object amplitude, $f _ { \phi _ { t } } = d _ { t } \mathrm { s i n } ( \phi _ { t } ) / \lambda$ and $f _ { \phi _ { r } } = d _ { r } \mathrm { s i n } ( \phi _ { r } ) / \lambda$ are the Tx and Rx normalized spatial frequencies at wavelength $\lambda = c / f _ { c }$ , and $\tau = 2 R / c$ is the round-trip propagation delay at the 0-th Rx antenna (reference antenna).

Analog-to-Digital Converter (ADC) and Low-Pass Filter (LPF): Suppose the object beat frequency <sup>βτ</sup> is smaller than the cutoff frequency $f _ { L }$ of the anti-aliasing LPF. By passing $a _ { n } ^ { s } ( t )$ into the LPF and sampling it at $t = k T _ { \mathrm { P R I } } + l \Delta T$ with $\Delta T$ denoting the fast-time interval, we have the sampled object signal on fast-time sample <sup>l</sup> and pulse <sup>k</sup>, i.e.,

$$
\begin{array} { l } { { a _ { n } ^ { s } ( l , k ) = \alpha _ { \tau } e ^ { - j 2 \pi f _ { r } l } { \bf 1 } [ l \in \mathcal { L } ^ { s } ] } } \\ { { \mathrm { ~ } } } \\ { { \displaystyle \qquad \times \sum _ { m = 0 } ^ { M - 1 } c _ { k , m } e ^ { - j 2 \pi ( f _ { d } k + f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } , } } \end{array}\tag{54}
$$

where $\mathcal { L } ^ { s } \triangleq \left\{ \lceil \tau / \Delta T \rceil , \ldots , \lfloor T / \Delta T \rfloor \right\}$ is the integer sample index set, and $f _ { r } \triangleq ( \beta \tau + 2 v / \lambda ) \Delta T$ and $f _ { d } \triangleq 2 f _ { c } T _ { \mathrm { P R I } } v / c$ are the normalized range and Doppler frequencies, respectively.

Fast-Time/Range FFT: Applying the <sup>L</sup>-length fast-time fast Fourier transform (FFT) or range FFT to $a _ { n } ^ { s } ( l , k )$ , we can obtain the range-domain spectrum as

$$
x _ { n } ^ { s } ( l ^ { \prime } , k ) = \alpha _ { l ^ { \prime } } \sum _ { m = 0 } ^ { M - 1 } c _ { k , m } e ^ { - j 2 \pi f _ { d } k } e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } ,\tag{55}
$$

where $\begin{array} { r } { \alpha _ { l ^ { \prime } } \triangleq \sum _ { l = 0 } ^ { L - 1 } \alpha _ { \tau } { \bf 1 } [ l \in \mathcal { L } ^ { s } ] e ^ { - j 2 \pi ( f _ { r } + l ^ { \prime } / L ) l } } \end{array}$ is the complex amplitude of the object on range bin <sup>l</sup>.

Slow-Time/Doppler FFT and Waveform Separation: From (55), each Rx antenna combines the <sup>M</sup> coded transmitting waveforms via the weighted summation. To separate $x _ { n } ^ { s } ( l _ { } ^ { \prime } , k )$ into object signals from <sup>M</sup> Tx signals, a slow-time MIMO decoding is applied. To obtain the signal from the <sup>m</sup>-th Tx antenna, the complex conjugate of the code sequence $c _ { k , m } ^ { * } , k = 0 , 1 , \ldots , K - 1$ are multiplied on the range-domain response over <sup>K</sup> slow-time pulses. For a MIMO code sequence with orthogonal property $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m } ^ { * } = K } \end{array}$ and $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m ^ { \prime } } ^ { * } = 0 , \forall \ m ^ { \prime } \neq m } \end{array}$ , summing the decoded signal over <sup>K</sup> pulses $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } x _ { n } ^ { s } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } } \end{array}$ can well reconstruct the object signal with zero Doppler from <sup>m</sup>-th Tx antenna. For a general case where the slow-time phase is shifted by the non-zero object Doppler, the Doppler needs to be compensated. To reconstruct the object signal from the <sup>m</sup>-th Tx antenna, we can compensate the Doppler using a slow-time FFT (Doppler FFT) on the slow-time decoded signal $x _ { n } ^ { s } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } , k = 0 , 1 , \ldots , K - 1$

$$
\begin{array} { l } { { y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) = \displaystyle \sum _ { k = 0 } ^ { K - 1 } x _ { n } ^ { s } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } e ^ { - j 2 \pi \frac { k ^ { \prime } } { K } k } } } \\ { { = b ( l ^ { \prime } , k ^ { \prime } ) e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } + y _ { m , n } ^ { r } ( l ^ { \prime } , k ^ { \prime } ) , } } \end{array}\tag{56}
$$

where $\begin{array} { r } { b ( l ^ { \prime } , k ^ { \prime } ) \triangleq \alpha _ { l ^ { \prime } } \sum _ { k = 0 } ^ { K - 1 } e ^ { - j 2 \pi ( f _ { d } + \frac { k ^ { \prime } } { K } ) k } } \end{array}$ is the amplitude of the object signal from the <sup>m</sup>-th Tx antenna, and

$$
\begin{array} { r } { y _ { m , n } ^ { r } ( l ^ { \prime } , k ^ { \prime } ) = \alpha _ { l ^ { \prime } } \displaystyle \sum _ { m ^ { \prime } \neq m } \left( \displaystyle \sum _ { k = 0 } ^ { K - 1 } c _ { k , m ^ { \prime } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( f _ { d } + \frac { k ^ { \prime } } { K } ) k } \right) } \\ { \times e ^ { - j 2 \pi ( f _ { \phi _ { t } } m ^ { \prime } + f _ { \phi _ { r } } n ) } , } \end{array}\tag{57}
$$

is the waveform separation residual from other Tx antennas. At the Doppler bin $k ^ { \prime }$ closest to the object Doppler frequency <sup>f</sup>d,

![](images/6aac3f531d05aaabcb5ba139bc6765fb16bd502b160125fad07d402354a1eb29.jpg)  
Fig. 9. Two necessary conditions for the $\widetilde { k } { - } \mathrm { t h }$ pulse of the interfering radar to be dechirped by the <sup>k</sup>-th pulse of the victim radar with a counterexample for each condition shown in the figure.

i.e., $f _ { d } + k ^ { \prime } / K \approx 0$ , the amplitude $b ( l ^ { \prime } , k ^ { \prime } ) \approx K \alpha _ { l ^ { \prime } }$ approaches to a coherent gain of <sup>K</sup> due to the Doppler FFT in (56). Using the near-orthogonality of MIMO codes [13]

$$
\operatorname* { m a x } _ { f } \left| \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m ^ { \prime } } ^ { * } e ^ { - j 2 \pi f k } \right| \ll K , \forall m ^ { \prime } \neq m ,\tag{58}
$$

the waveform separation residual in (56) can be ignored. It is worth noting that object detection under imperfect waveform separation for MIMO radar was considered in [9]. By stacking $\{ y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) \}$ into a vector,we have (3).

## APPENDIX BDERIVATION OF INTERFERENCE SIGNAL MODEL

Since our goal is to derive the interference signal model seen at the victim radar, we need to convert the interference time, $\mathrm { i . e . , } \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } + \widetilde { \tau } _ { s y n } , \widetilde { k } = 0 , 1 , \ldots , \widetilde { K } - 1$ to the reference time of the victim radar. Define $\widetilde { \tau } _ { \boldsymbol { k } , \widetilde { \boldsymbol { k } } } ^ { \prime }$ as the time offset between the <sup>k</sup>-th pulse of the interfering radar relative to the <sup>k</sup>-th pulse at the victim radar. As shown in Fig. 9, the necessary condition for the <sup>k</sup>-th pulse of the interfering radar to be dechirped by the <sup>k</sup>-th pulse of victim radar is $- \widetilde { T } _ { \mathrm { P R I } } < \widetilde { \tau } _ { \boldsymbol { k } , \widetilde { \boldsymbol { k } } } ^ { \prime } < T _ { \mathrm { P R I } }$ . Define

$$
\begin{array} { r l r } {  { \mathcal { K } _ { \widetilde { k } } \triangleq \Big \{ k : \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } + \widetilde { \tau } _ { s y n } = k T _ { \mathrm { P R I } } + \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } , - \widetilde { T } _ { \mathrm { P R I } } < \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } < T _ { \mathrm { P R I } } , } } \\ & { } & { k = 0 , 1 , \ldots , K - 1 \big \} , \widetilde { k } = 0 , 1 , \ldots , \widetilde { K } - 1 , \qquad ( 5 9 ) } \end{array}
$$

as a set that groups all pulses of the victim radar that intercept with the <sup>k</sup> pulse by checking whether any time instant of the victim pulse falls within the <sup>k</sup> interfering pulse. Denote the slowtime code of the interfering radar’s <sup>k</sup> pulse and <sup>m˜</sup> -th Tx antenna observed at <sup>k</sup>-th victim radar pulse as $\widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } = \widetilde { c } _ { \widetilde { k } , \widetilde { m } } \mathrm { ~ i f ~ } k \in \mathcal { K } _ { \widetilde { k } }$ and $\tilde { c } _ { k , \widetilde { m } } ^ { k } = 0$ otherwise. Then, we rewrite $s _ { n } ^ { i } ( t )$ as

![](images/6d34cb4d54149860285a282d67a6e17537b9f2413fd7d9d9940a330fc7ce71e8.jpg)  
Fig. 10. Interference at victim radar’s pulse <sup>k</sup>.

$$
\begin{array} { r } { s _ { n } ^ { i } ( t ) = \widetilde { \alpha } e ^ { - j 2 \pi \widetilde { f } _ { c } \widetilde { \tau } } \displaystyle \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \displaystyle \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \displaystyle \sum _ { k \in { \widetilde { \cal K } _ { k } } } \widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } \widetilde { s } ( t - k T _ { \mathrm { P R I } } - \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } - \widetilde { \tau } ) } \\ { \times e ^ { j 2 \pi \widetilde { f } _ { c } ( t - k T _ { \mathrm { P R I } } - \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } ) } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } e ^ { - j 2 \pi \widetilde { f } _ { c } \frac { \tilde { v } t } { c } } , } \end{array}\tag{60}
$$

where $\widetilde { \tau } = \widetilde { R } / { \mathrm { - } }$ <sup>c</sup> is the one-way propagation delay from interferer to the victim radar’s reference antenna, and $\widetilde { f _ { \phi _ { t } } } = \widetilde { d _ { t } } \mathrm { s i n } ( \widetilde { \phi } _ { t } ) / \widetilde { \lambda }$ and $\widetilde { f } _ { \phi _ { r } } = d _ { r } \mathrm { s i n } ( \widetilde { \phi } _ { r } ) / \widetilde { \lambda }$ are the normalized spatial frequency at the interferer transmitting antennas and victim receiving antennas. The victim radar mixes $s _ { n } ^ { i } ( t )$ with the conjugate of its LO signal $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } s ^ { * } ( t - k T _ { \mathrm { P R I } } ) e ^ { - j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } ) } } \end{array}$ and passes the analog beat signal from the <sup>n</sup>-th Rx antenna into the LPF of bandwidth $f _ { L }$ . The resulting low-pass filtered IF interference signal is

$$
\begin{array} { l l } { \displaystyle { a _ { n } ^ { i , l o w } ( t ) = \sum _ { \overline { { { m } } } = 0 } ^ { \overline { { { M } } } - 1 } \sum _ { k = 0 } ^ { \overline { { { K } } } - 1 } \sum _ { k = 1 } ^ { \overline { { { K } } } } \widetilde { \alpha } _ { k , \overline { { { m } } } } ^ { \overline { { { k } } } } e ^ { j \pi ( \overline { { { \beta } } } - \beta ) ( t - k T _ { \mathrm { P M } } ) ^ { 2 } } } } \\ { \displaystyle { \quad \times e ^ { j 2 \pi ( \widetilde { f } _ { c } - f _ { c } ) ( t - k T _ { \mathrm { P H } } ) } e ^ { - j 2 \pi \widetilde { \beta } ( t - k T _ { \mathrm { P H } } ) ( \widetilde { \tau } _ { k , \overline { { { k } } } } ^ { \prime } + \widetilde { \tau } ) } } } \\ { \displaystyle { \quad \times e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { \mathrm { f } } } \widetilde { m } + \widetilde { f } _ { \phi _ { \mathrm { f } } } { n } ) } e ^ { - j 2 \pi \widetilde { f } _ { c } \frac { \pi \widetilde { \epsilon } } { c } } \mathbf { 1 } \left[ 0 < \widetilde { f } _ { k , \widetilde { k } } < f _ { L } \right] } } \\ { \displaystyle { \quad \times D _ { \widetilde { \tau } _ { k , \overline { { { k } } } } ^ { \prime } + \widetilde { \tau } , \mathrm { m i n } } \Big \{ T _ { \widetilde { \tau } _ { k , \overline { { { k } } } } ^ { \prime \prime } + \widetilde { \tau } } + \widetilde { T } \Big \} } } \end{array}
$$

where $\widetilde { \alpha } _ { k , \widetilde { m } } ^ { \widetilde { k } } = \widetilde { \alpha } e ^ { - j 2 \pi \widetilde { f } _ { c } \widetilde { \tau } } \widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } e ^ { j \pi \widetilde { \beta } ( \widetilde { \tau } _ { k , k } ^ { \prime } + \widetilde { \tau } ) ^ { 2 } } e ^ { - j 2 \pi \widetilde { f } _ { c } \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } } \widetilde { \alpha } _ { k , k } ^ { }$ is the pulse-dependent amplitude, and $\widetilde { f } _ { k , \widetilde { k } } \triangleq \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) - ( \widetilde { \beta } -$ $\beta ) ( t - k T _ { \mathrm { P R I } } ) - ( \widetilde { f } _ { c } - f _ { c } )$ is the instantaneous frequency of interference at pulse <sup>k</sup> shown in Fig. 10. Notice that we moved the Doppler term in (61) $( \mathrm { i . e . , } e ^ { - j 2 \pi \widetilde { f } _ { c } \frac { v t } { c } } )$ out of the definition of the instantaneous frequency as the Doppler frequency is typically small and can be neglected.

The low-pass filtered interference signal $a _ { n } ^ { s , l o w } ( t )$ sampled at $t = k T _ { \mathrm { P R I } } + l \Delta T$ is

$$
\begin{array} { r l r } {  { a _ { n } ^ { i } \big ( l , k \big ) = a _ { n } ^ { i , l o w } \big ( k T _ { \mathrm { P R I } } + l \Delta T \big ) } } \\ & { } & { = \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \widetilde { \alpha } _ { k , \widetilde { m } } ^ { \widetilde { k } } e ^ { - j 2 \pi \widetilde { f } _ { d } k } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } } \\ & { } & { \times e ^ { j \pi ( \widetilde { \beta } - \beta ) ( l \Delta T ) ^ { 2 } } e ^ { - j 2 \pi \widetilde { f } _ { r , k , \widetilde { k } } l } \mathbf { 1 } \Big [ l \in \mathcal { L } _ { k , \widetilde { k } } ^ { i } \Big ] } \end{array}\tag{62}
$$

where $\begin{array} { r } { \widetilde { f } _ { r , k , \widetilde { k } } \triangleq ( \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) + \frac { \widetilde { v } } { \widetilde { \lambda } } ) \Delta T } \end{array}$ is the normalized interference initial fast-time frequency, $\widetilde { f } _ { d } = \widetilde { f } _ { c } \widetilde { v } T _ { \mathrm { P R I } } / c$ is the normalized interference Doppler frequency, and

$$
\mathcal { L } _ { k , \widetilde { k } } ^ { i } \triangleq  l : ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) < l \Delta T < \operatorname* { m i n }  T , \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } + \widetilde { T } 
$$

$$
0 < \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) - ( \widetilde { \beta } - \beta ) l \Delta T - ( \widetilde { f } _ { c } - f _ { c } ) < f _ { L } \Big \}\tag{63}
$$

is the set of interference contaminated sample indices.

Applying the range FFT, waveform separation and Doppler FFT to the sampled interference signal $a _ { n } ^ { i } ( l , k )$ , we obtain its spectrum at the <sup>m</sup>-th Tx antenna, <sup>n</sup>-th Rx antenna, <sup>l</sup>-th range bin and <sup>k</sup>-th pulse as

$$
\begin{array} { l } { { y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \displaystyle \sum _ { k = 0 } ^ { K - 1 } \sum _ { l = 0 } ^ { L - 1 } a _ { n } ^ { i } ( l , k ) e ^ { - j 2 \pi \frac { l ^ { \prime } } { L } l } c _ { k , m } ^ { * } e ^ { - j 2 \pi \frac { k ^ { \prime } } { K } k } } } \\ { { = \widetilde { a } _ { t , m } ^ { \prime } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } n } , } } \end{array}\tag{64}
$$

where

$$
\begin{array} { r l } & { \widetilde { a } _ { t , m } ^ { \prime } = \displaystyle \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \sum _ { k = 0 } ^ { K - 1 } \widetilde { \alpha } _ { k , \widetilde { m } } ^ { \widetilde { k } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { t } } \widetilde { m } } } \\ & { \qquad \times \displaystyle \sum _ { l = 0 } ^ { L - 1 } e ^ { j \pi ( \widetilde { \beta } - \beta ) ( l \Delta T ) ^ { 2 } } \mathbf { 1 } \left[ l \in \mathcal { L } _ { k , \widetilde { k } } ^ { i } \right] e ^ { - j 2 \pi ( \widetilde { f } _ { r , k , \widetilde { k } } + \frac { l ^ { \prime } } { L } ) l } . } \end{array}\tag{65}
$$

## APPENDIX C DERIVATION FOR EXAMPLES IN SECTION II-D

## A. Phased Array Radar Interference

Under the phased array radar setup, $\{ c _ { k , m } = 1 \}$ implies that $\{ \widetilde { c } _ { k , \widetilde { m } } ^ { k } = 1 \}$ and $\{ c _ { k , m } ^ { * } = 1 \}$ . Then, $\widetilde { \boldsymbol { a } } _ { t , m } ^ { \prime }$ is indepen-<sup>-</sup>dent of <sup>m</sup> and <sup>m</sup>. Rewriting $\widetilde { \boldsymbol { a } } _ { t , m } ^ { \prime }$ as $\widetilde { a } _ { t } ^ { \prime }$ and rewriting $y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ as $y _ { n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ , the range-Doppler interference spectrum in (64) reduces to $y _ { n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { a } _ { t } ^ { \prime } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } n }$ , where $\widetilde { a } _ { t } ^ { \prime } =$ $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } ( \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \widetilde { w } _ { \widetilde { m } } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { t } } \widetilde { m } } ) } \end{array}$ , and $\widetilde { w } _ { \widetilde { m } }$ is the beamforming weights on <sup>m</sup>-th interference Tx antenna. Stacking $\{ y _ { n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \}$ into a vector, we obtain (8).

## B. TDM-MIMO Interference

The modification in the above derivation is in two folds. First, the slow-time Tx-pulse code $c _ { k , m }$ is replaced as the slow-time Tx-pulse code with $c _ { k , m } = 1 \mathrm { i f } m =$ mod $( k , M )$ and $c _ { k , m } =$ 0 otherwise, for $k = 0 , 1 , \ldots , K - 1 { \mathrm { a n d } } m = 0 , 1 , \ldots , M - 1$

Second, in (64), $e ^ { - j 2 \pi \frac { k ^ { \prime } } { K } k }$ is replaced by $e ^ { - j 2 \pi } { \frac { k ^ { \prime } } { [ K / M ] } } k$ because only $\lfloor K / M \rfloor$ pulses are used in TDM-MIMO for each antenna. These two modifications do not affect the interference structure in (5).

## APPENDIX D PROOF OF THEOREM 1

By [60], the beamformer $\begin{array} { r } { \mathbf { w } ^ { * } = \frac { \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) } { \| \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \| ^ { 2 } } } \end{array}$ is the optimal solution of the relaxed version of problem (31):

$$
\operatorname* { m i n } _ { \mathbf { w } } \quad \mathbf { w } ^ { H } \mathbf { R } \mathbf { w } , \quad \mathrm { s . t . ~ } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 ,\tag{66}
$$

which is an LCMV beamforming optimization problem with covariance matrix R [60]. Next, we show that special structure of $\mathbf { R } ^ { - 1 }$ implies that $\mathbf { w } ^ { * }$ satisfies the last condition of problem (31). Denoting $\widetilde { \mathbf { A } } \triangleq [ \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , 1 } , \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , 2 } , \dots , \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , Q } ]$ as the stack of $Q$ essential interference virtual steering vectors, we write R of (29) in matrix form as $\mathbf { R } = \mathbf { I } _ { M N } + \widetilde { \mathbf { A } } \pmb { \Lambda } \widetilde { \mathbf { A } } ^ { H }$ . Using the Woodbury matrix identity, we have

$$
\begin{array} { r l } & { \mathbf { R } ^ { - 1 } = \mathbf { I } _ { M N } - \widetilde { \mathbf { A } } ( \mathbf { A } ^ { - 1 } + \widetilde { \mathbf { A } } ^ { H } \widetilde { \mathbf { A } } ) ^ { - 1 } \widetilde { \mathbf { A } } ^ { H } } \\ & { \quad \quad \quad = \mathbf { I } _ { M N } - \mathbf { P } _ { \mathbf { a } _ { t } } \otimes \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } } . } \end{array}\tag{67}
$$

Substituting (67) into $\mathbf { w } ^ { * }$ , we can find $\mathbf { w } ^ { * }$ satisfies the last condition of problem (31). Thus, $\mathbf { w } ^ { G S } = \mathbf { w } ^ { * }$

## APPENDIX E PROOF OF THEOREM 2

The following derivation is based on the form $T ^ { G S } ( \mathbf { y } ) =$ $\frac { 2 } { \sigma ^ { 2 } } \frac { \lvert ( \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ) ^ { \breve { H } } \mathbf { y } \rvert ^ { 2 } } { \lVert \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \rVert ^ { 2 } }$ suggested by $\mathbf { w } ^ { G S }$ in (32).

Under $\mathcal { H } _ { 0 }$ , we have $( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \mathbf { y } = ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \widetilde { \mathbf { z } } ,$ using the last condition in $( 3 1 ) . \operatorname { A s } \widetilde { \mathbf { z } } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \mathbf { R } )$ by (28), we have $( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \mathbf { y } \sim { \mathcal { C N } } ( \mathbf { 0 } , \sigma ^ { 2 } \left| \left| \mathbf { R } ^ { - { \frac { 1 } { 2 } } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right| \right| ^ { 2 } )$ . Thus, $T ^ { G S } ( \mathbf { y } )$ under $\mathcal { H } _ { 0 }$ follows chi-squared distribution with 2 degrees of freedom (DoF) [63], i.e.,

$$
T ^ { G S } ( \mathbf { y } ) \sim \chi _ { 2 } ^ { 2 } , \mathrm { u n d e r } \mathcal { H } _ { 0 } .\tag{68}
$$

Under $\mathcal { H } _ { 1 }$ , we have $( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \mathbf { y } \sim \mathcal { C N } ( b \Big | \Big | \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { \tau } _ { t } )$ $\mathbf { a } _ { r } ) \Big \vert \Big \vert ^ { 2 } , \sigma ^ { 2 } \Big \vert \Big \vert \mathbf { R } ^ { - \frac { 1 } { 2 } } \big ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \big ) \Big \vert \Big \vert ^ { 2 } )$ . Thus, $T ^ { G S } ( \mathbf { y } )$ under $\mathcal { H } _ { 1 }$ follows noncentral chi-squared distribution with 2 DoF and noncentrality parameter $\lambda ^ { \bar { G S } } \ [ 6 3 ]$ , i.e.,

$$
\begin{array} { r } { T ^ { G S } ( \mathbf { y } ) \sim { \chi ^ { \prime } } _ { 2 } ^ { 2 } ( \lambda ^ { G S } ) , \mathrm { u n d e r } \mathcal { H } _ { 1 } , } \end{array}\tag{69}
$$

where $\begin{array} { r } { \lambda ^ { G S } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \Big | \Big | { \bf R } ^ { - \frac { 1 } { 2 } } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \Big | \Big | ^ { 2 } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } M { \bf a } _ { r } ^ { H } \widetilde { \bf P } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } { \bf a } _ { r } . } \end{array}$ Then, given a detection threshold <sup>γ</sup>, the probability of false alarm $\breve { P } _ { F A } ^ { G S } \triangleq \mathrm { P r } [ T ^ { G S } ( \mathbf { y } ) \geq \gamma | \mathcal { H } _ { 0 } ]$ is the complementary CDF (CCDF) of exponential distribution with rate parameter $\mathbf { \frac { \check { 1 } } { 2 } }$ [63]; the probability of detection $P _ { D } ^ { G S } \triangleq \operatorname* { P r } [ T ^ { G S } ( \mathbf { y } ) \geq \gamma | \bar { \mathcal { H } } _ { 1 } ]$ is the CCDF of the noncentral chi-squared distribution with 2 DoF and noncentrality parameter $\lambda ^ { \hat { G } S }$ , which is equivalent to $\mathcal { Q } _ { 1 } ( \sqrt { \lambda ^ { G S } } , \sqrt { \gamma } )$ [55].

## APPENDIX F PROOF OF LEMMA 1

Substituting (46) into (47), we have

$$
P _ { q } = \frac { 1 } { ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) } .\tag{70}
$$

Next, we prove $( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = ( \mathbf { a } _ { t } \otimes$ $\widetilde { \mathbf { a } } _ { r , q } \big ) ^ { H } \widetilde { \mathbf { R } } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } )$ . For any $q \in \{ 0 , 1 , \ldots , Q \}$ , define $\begin{array} { r } { \widetilde { \mathbf { y } } _ { q } = \widetilde { \mathbf { z } } + \sum _ { q ^ { \prime } = 1 } ^ { q } \widetilde { \mathbf { a } } _ { v , q ^ { \prime } } } \end{array}$ with $\widetilde { \mathbf { a } } _ { v , q ^ { \prime } } \triangleq ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q ^ { \prime } } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r , q ^ { \prime } }$ and define the normalized covariance matrix of $\widetilde { \mathbf { y } } _ { q }$ as $\mathbf { R } _ { q }$ . Then, $\begin{array} { r } { { \bf R } _ { q } = { \bf R } _ { q - 1 } + \frac { 1 } { \sigma ^ { 2 } } \widetilde { { \bf a } } _ { v , q ^ { \prime } } \widetilde { { \bf a } } _ { v , q ^ { \prime } } ^ { H } , ~ { \bf R } _ { 0 } = { \bf R } } \end{array}$ , and $\mathbf { R } _ { Q } = \widetilde { \mathbf { R } }$ . By the Woodbury matrix identity, we have

$$
{ \bf R } _ { q } ^ { - 1 } = { \bf R } _ { q - 1 } ^ { - 1 } - \frac { { \bf R } _ { q - 1 } ^ { - 1 } \widetilde { \bf a } _ { v , q ^ { \prime } } \widetilde { \bf a } _ { v , q ^ { \prime } } ^ { H } { \bf R } _ { q - 1 } ^ { - 1 } } { \sigma ^ { 2 } + \widetilde { \bf a } _ { v , q ^ { \prime } } ^ { H } { \bf R } _ { q - 1 } ^ { - 1 } \widetilde { \bf a } _ { v , q ^ { \prime } } } .\tag{71}
$$

By (35) and (71), via induction, we can prove that

$$
\widetilde { \mathbf { a } } _ { v , q ^ { \prime } } ^ { H } \mathbf { R } _ { q } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q ^ { \prime \prime } } ) = 0\tag{72}
$$

holds for any $q , q ^ { \prime } , q ^ { \prime \prime } \in \{ 0 , 1 , \ldots , Q \}$ . Then, by (71) and (72), we can iteratively prove $( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = ( \mathbf { a } _ { t } \otimes$ $\widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { R } _ { 1 } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ^ { - 1 } ) ^ { H } \mathbf { R } _ { 2 } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ^ { - 1 } ) =$ $\dots = ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { R } _ { Q } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \widetilde { \mathbf { R } } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } )$ $\widetilde { \mathbf { a } } _ { r , q } )$

## REFERENCES

[1] S. Jin, P. Wang, P. Boufounos, R. Takahashi, and S. Roy, “Spatial-domain object detection under MIMO-FMCW automotive radar interference,” in Proc. IEEE Int. Conf. Acoustics, Speech, Signal Process., 2023, pp. 1–5.

[2] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[3] S. Jin, P. Wang, P. Boufounos, P. V. Orlik, R. Takahashi, and S. Roy, “Spatial-domain interference mitigation for slow-time MIMO-FMCW automotive radar,” in Proc. IEEE 12th Sensor Array Multichannel Signal Process. Workshop, 2022, pp. 311–315.

[4] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[5] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 20–31, Sep. 2019.

[6] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 32–44, Sep. 2019.

[7] P. Wang, D. Millar, K. Parsons, and P. V. Orlik, “Nonlinearity correction for range estimation in FMCW millimeter-wave automotive radar,” in Proc. IEEE MTT-S Int. Wireless Symp., 2018, pp. 1–3.

[8] P. Wang, D. Millar, K. Parsons, R. Ma, and P. V. Orlik, “Range accuracy analysis for FMCW systems with source nonlinearity,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2019, pp. 1–5.

[9] P. Wang, P. Boufounos, H. Mansour, and P. V. Orlik, “Slow-time MIMO-FMCW automotive radar detection with imperfect waveform separation,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., 2020, pp. 8634–8638.

[10] M. Sheeny, E. De Pellegrin, S. Mukherjee, A. Ahrabian, S. Wang, and A. Wallace, “RADIATE: A radar dataset for automotive perception in bad weather,” in Proc. IEEE Int. Conf. Robot. Automat., 2021, pp. 1–7.

[11] M. Mostajabi, C. M. Wang, D. Ranjan, and G. Hsyu, “High resolution radar dataset for semi-supervised learning of dynamic objects,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. Workshops, 2020, pp. 450–457.

[12] S. Rao, “White paper: MIMO radar,” Texas Instrum., Tech. Rep. SWRA554A, 2017.

[13] S. Sun, A. P. Petropulu, and H. V. Poor, “MIMO radar for advanced driverassistance systems and autonomous driving: Advantages and challenges,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 98–117, Jul. 2020.

[14] NXP B.V., “SAF86xx RFCMOS automotive radar SoC fact sheet,” FACT SHEET SAF86XXFS Rev 1, 2023.

[15] Texas Instruments Incorporated, “AWR2943/44 single-chip 76 to 81 GHz FMCW radar sensor,” Texas Instruments (TI), Tech. Rep. SWRS273B, 2024. Online]. Available: https://www.nxp.com/docs/en/ fact-sheet/SAF86XX-FS.pdf

[16] A. Och, C. Pfeffer, J. Schrattenecker, S. Schuster, and R. Weigel, “A scalable 77 GHz massive MIMO FMCW radar by cascading fully-integrated transceivers,” in Proc. Asia-Pacific Microw. Conf., 2018, pp. 1235–1237.

[17] O. Bialer, A. Jonas, and T. Tirer, “Super resolution wide aperture automotive radar,” IEEE Sensors J., vol. 21, no. 16, pp. 17846–17858, Aug. 2021.

[18] Texas Instruments Incorporated, “Design guide: TIDEP-01012 - imaging radar using cascaded mmWave sensor reference design,” Texas Instrum., Tech. Rep. TIDUEN5A, 2020.

[19] Arbe Robotics Ltd, “Best-in-class radar performance through chipset innovation,” Arbe Brochures, 2024.

[20] S. Rao and A. V. Mani, “Interference characterization in FMCW radars,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[21] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[22] C. Aydoglu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[23] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[24] K. U. Mazher, R. W. Heath, K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[25] S. Jin and S. Roy, “FMCW radar network: Multiple access and interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 968–979, Jun. 2021.

[26] F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, and M. Gashinova, “Automotive radar waveform parameters randomisation for interference level reduction,” in Proc. IEEE Radar Conf., 2020, pp. 1–5.

[27] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2015, pp. 1–4.

[28] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

[29] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf., 2017, pp. 90–93.

[30] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[31] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[32] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf., 2018, pp. 0405–0410.

[33] A. Correas-Serrano and M. A. Gonzalez-Huici, “Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation,” in Proc. IEEE MTT-S Int. Conf. Microwaves Intell. Mobility, 2019, pp. 1–4.

[34] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[35] S. Jin, P. Wang, P. Boufounos, P. Orlik, and S. Roy, “Automotive radar interference mitigation with fast-time-frequency mode retrieval,” in Proc. IEEE Radar Conf., 2022, pp. 1–6.

[36] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in Proc. IEEE 92nd Veh. Technol. Conf., 2020, pp. 1–5.

[37] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for FMCW radars,” IEEE Trans. Geosci. Remote Sens., vol. 60, pp. 1–16, 2022.

[38] J. Wang, R. Li, X. Zhang, and Y. He, “Interference mitigation for automotive FMCW radar based on contrastive learning with dilated convolution,” IEEE Trans. Intell. Transp. Syst., vol. 25, no. 1, pp. 545–558, Jan. 2024.

[39] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in Proc. IEEE Int. Symp. Circuits Syst., 2018, pp. 1–4.

[40] S. Chen, W. Shangguan, J. Taghia, U. Kühnau, and R. Martin, “Automotive radar interference mitigation based on a generative adversarial network,” in Proc. IEEE Asia-Pacific Microw. Conf., 2020, pp. 728–730.

[41] J. Fuchs, A. Dubey, M. Lübke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf., 2020, pp. 315–320.

[42] C. Jiang, T. Chen, and B. Yang, “Adversarial interference mitigation for automotive radar,” in Proc. IEEE Radar Conf., 2021, pp. 1–6.

[43] A. Dubey, J. Fuchs, V. Madhavan, M. Lübke, R. Weigel, and F. Lurz, “Region based single-stage interference mitigation and target detection,” in Proc. IEEE Radar Conf., 2020, pp. 1–5.

[44] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021.

[45] J. Overdevest, A. Koppelaar, M. Bekooij, J. Youn, and R. v. Sloun, “Signal reconstruction for FMCW radar interference mitigation using deep unfolding,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., 2023, pp. 1–5.

[46] A. Bose, B. Tang, M. Soltanalian, and J. Li, “Mutual interference mitigation for multiple connected automotive radar systems,” IEEE Trans. Veh. Technol., vol. 70, no. 10, pp. 11062–11066, Oct. 2021.

[47] C. Fischer, M. Goppelt, H.-L. Blöcher, and J. Dickmann, “Minimizing interference in automotive radar using digital beamforming,” Adv. Radio Sci., vol. 9, pp. 45–48, 2011.

[48] J. Bechter, A. Demirlika, P. Hügler, F. Roos, and C. Waldschmidt, “Blind adaptive beamforming for automotive radar interference suppression,” in Proc. 19th Int. Radar Symp., 2018, pp. 1–10.

[49] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in Proc. IEEE Radar Conf., 2018, pp. 0252–0256.

[50] T. Pernstål, J. Degerman, H. Broström, V. T. Vu, and M. I. Pettersson, “GIP test for automotive FMCW interference detection and suppression,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[51] M. Rameez, M. Dahl, and M. I. Pettersson, “Experimental evaluation of adaptive beamforming for automotive radar interference suppression,” in Proc. IEEE Radio Wireless Symp., 2020, pp. 183–186.

[52] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Techn., vol. 65, no. 5, pp. 1727–1734, May 2017.

[53] A. Pirkani, F. Norouzian, E. Hoare, M. Chemiakov, and M. Gashinova, “Automotive interference suppression in MIMO and phased array radar,” in Proc. 18th Eur. Radar Conf.,2022, pp. 413–416.

[54] W. Melvin, “A STAP overview,” IEEE Aerosp. Electron. Syst. Mag., vol. 19, no. 1, pp. 19–35, Jan. 2004.

[55] Y. Sun, A. Baricz, and S. Zhou, “On the monotonicity, logconcavity, and tight bounds of the generalized Marcum and Nuttall <sup>q</sup>-functions,” IEEE Trans. Inf. Theory, vol. 56, no. 3, pp. 1166–1186, Mar. 2010.

[56] M. Cui, Z. Wu, Y. Lu, X. Wei, and L. Dai, “Near-field MIMO communications for 6G: Fundamentals, challenges, potentials, and future directions,” IEEE Commun. Mag., vol. 61, no. 1, pp. 40–46, Jan. 2023.

[57] R. Feger, H. Haderer, and A. Stelzer, “Optimization of codes and weighting functions for binary phase-coded FMCW MIMO radars,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2016, pp. 1–4.

[58] B. Friedlander, “On signal models for MIMO radar,” IEEE Trans. Aerosp. Electron. Syst., vol. 48, no. 4, pp. 3655–3660, Oct. 2012.

[59] J. Li and P. Stoica, “MIMO radar with colocated antennas,” IEEE Signal Process. Mag., vol. 24, no. 5, pp. 106–114, Sep. 2007.

[60] H. L. Van Trees, Optimum Array Processing: Part IV of Detection, Estimation, and Modulation Theory. Hoboken, NJ, USA: Wiley, 2004.

[61] Y. Gu and A. Leshem, “Robust adaptive beamforming based on interference covariance matrix reconstruction and steering vector estimation,” IEEE Trans. Signal Process., vol. 60, no. 7, pp. 3881–3885, Jul. 2012.

[62] Z. Zheng, T. Yang, W.-Q. Wang, and H.C. So, “Robust adaptive beamforming via simplified interference power estimation,” IEEE Trans. Aerosp. Electron. Syst., vol. 55, no. 6, pp. 3139–3152, Dec. 2019.

[63] S. M. Kay, Fundamentals of Statistical Signal Processing: Detection Theory. Englewood Cliffs, NJ, USA: Prentice Hall, 1998.

![](images/c91d3b6cf11d8c07f20a8a313747a63e9d29e34e326e9e1fe2950aa8748e1637.jpg)

Sian Jin received the B.E. degree in electronic information engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2016, and the Ph.D. degree in electrical and computer engineering from the University of Washington, Seattle, WA, USA, in 2022. During 2022 spring and summer, he was with Princeton University, Princeton, NJ, USA, as a Postdoc. Since 2022 fall, he has been with Phased Array and Radar Team, MathWorks, developing state-of-the-art signal processing algorithms. His research interests include array processing, statistical signal processing, wireless localization, sensor fusion and tracking, and wireless communication.

![](images/b1e4e5ef2571e1eabad94bb558c18335814ccbe6f759bf2fc4bf00c95835337f.jpg)

Pu (Perry) Wang (Senior Member, IEEE) received the Ph.D. degree in electrical engineering from the Stevens Institute of Technology, Hoboken, NJ, USA, in 2011. He was a Research Scientist with Schlumberger-Doll Research, Cambridge, MA, USA, contributing to developments and commercialization of next-generation logging-while-drilling Acoustics/NMR products. He is currently a Senior Principal Research Scientist with the Mitsubishi Electric Research Laboratories (MERL), Cambridge, MA, USA, where he was an Intern during the summer of 2010.

His research interests include signal processing, deep learning, and their applications in wireless sensing and radar perception. Dr. Wang was the recipient of the IEEE Vehicular Technology Society Jack Neubauer Memorial Award in 2013 and was also recognized as the Society of Petrophysicists and Well Log Analysts (SPWLA) Distinguished Speaker in 2017. He was an Associate Editor/Senior Area Editor for IEEE SIGNAL PROCESSING LETTERS, and a Guest Editor of IEEE Signal Processing Magazine, IEEE JOURNAL OF SELECTED TOPICS IN SIGNAL PROCESSING, and IEEE SENSORS JOURNAL. He is a member of the IEEE SPS Signal Processing Theory and Methods (SPTM) Technical Committee, and Voting Member of the IEEE 802.11 Standards Association.

![](images/00d0603c8a567a355449605827932ea7b34fc42fb5cf1c8e099500c23a6b3512.jpg)

Petros T. Boufounos (Fellow, IEEE) received the Undergraduate and Graduate degrees from the Massachusetts Institute of Technology, Cambridge, MA, USA, the S.B. degree in economics in 2000, the S.B. and M.Eng. degrees in electrical engineering and computer science in 2002, and the Sc.D. degree in electrical engineering and computer science in 2006. Between September 2006 and December 2008, he was a Postdoctoral Associate with Digital Signal Processing Group, Rice University, Houston, TX, USA. In January 2009, he joined Mitsubishi Electric

Research Laboratories (MERL), where he has been heading the Computational Sensing Team since 2016. He is currently a Distinguished Research Scientist, the Deputy Director, and the Computational Sensing Senior Team Leader with MERL. He has more than 40 patents granted and more than ten pending, and more than 100 peer reviewed journal and conference publications in his research interests which include signal acquisition and processing, computational sensing, inverse problems, quantization, data representations, and focusing on how signal acquisition interacts with other fields that use sensing extensively, such as machine learning, robotics, and dynamical system theory. Dr. Boufounos was a General Co-Chair of the ICASSP 2023 organizing committee and is also a Regional Director-at-Large in the IEEE Signal Processing Society’s Board of Governors. He was an Area Editor and a Senior Area Editor of IEEE SIGNAL PROCESSING LETTERS, an AE for IEEE TRANSACTIONS ON COMPUTATIONAL IMAGING, and a member of the SigPort Editorial Board and the IEEE Signal Processing Society Theory and Methods Technical Committee. Dr. Boufounos was an IEEE SPS Distinguished Lecturer for 2019–2020.

![](images/790b66c3f45da82348450f48ffb0ef7a5c5cc5454aef65a534aa56d05be7dc72.jpg)

Philip V. Orlik (Senior Member, IEEE) was born in New York, NY, USA, in 1972. He received the B.E. and M.S. degrees in 1994 and 1997, respectively, and the Ph. D. degree in electrical engineering from the State University of New York at Stony Brook, Stony Brook, NY, USA, in 1999. Since 2000, he has been with Mitsubishi Electric Research Laboratories Inc., Cambridge, MA, USA, where he is currently the Vice President and Research Director responsible for research in the areas of signal processing, data analytics, robotics, and electronic devices. His re-

search interests include advanced wireless and wired communications as well as sensor/IoT networks, vehicular/car-to-car communications, mobility modeling, network performance analysis, and queuing theory. He is also a contributor to various IEEE 802 standards including 802.11n and 802.15.4a where he was also a Technical Editor of the UWB Physical Layer and was Network Layer Technical Editor of the initial version of ZigBeeTM.

![](images/889e61ce3fb28487c591ec93579d4d324c0292bcd86a6deca5967513a27ce592.jpg)

![](images/d76a949f8fbf6c8e923881cc332652d0712bce00a898a01f27d32d96ccf4fb62.jpg)

was a Program Lead with the US Department of Defense Innovate Beyond 5G. His research interests include next-gen WLANs and cellular networks, spectrum sharing, vehicular, and sensor networking. He was also a IEEE ComSoc Distinguished Lecturer and an Associate Editor for all the major ComSoc journals. He is on the Executive Committee of the National Spectrum Consortium dedicated to efficient spectrum sharing between Federal licensed and civilian sectors. He was elevated to IEEE Fellow by Communications Society in 2007 for “contributions to multi-user communications theory and cross-layer design of wireless networking standards”.

Sumit Roy (Fellow, IEEE) received the B. Tech. degree from the Indian Institute of Technology (Kanpur), Kanpur, Uttar Pradesh, India, in 1983, the M. S. and Ph. D. degrees in electrical engineering from the University of California (Santa Barbara), Santa Barbara, CA, USA, in 1985 and 1988 respectively, and the M. A. degree in statistics and applied probability in 1988. He is currently Professor of electrical & computer engineering, appointed to a term Distinguished Professorship for Integrated Systems between 2014– 2019. Between September 2020 – August 2022, he

ing a wide range of radar signal processing techniques. He is currently a Group Manager leading research in advanced sensor signal processing. From 2013 to 2018, he was an Associate Editor for IEICE Transactions on Communications. From 2016 to 2021, he was also a member of the Technical Committees for Space, Aeronautical and Navigational Electronics of the IEICE.

Ryuhei Takahashi received the B.S. degree in electrical engineering from Tokyo Science University, Tokyo, Japan, in 1993. Since 1993, he has been with the Kamakura works of Mitsubishi Electric Corporation, Kamakura, Japan, as a Radar System Engineer mainly developing ground-based and shipboard active phased array radar systems. From 1993 to 1998, he worked on developing the signal processing algorithm for an experimental airborne magnetic anomaly detector. Since 2007, he has been with the Information Technology R&D Center of the corporation, research-