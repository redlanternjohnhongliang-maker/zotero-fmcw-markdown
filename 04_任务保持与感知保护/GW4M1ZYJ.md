# Mutual Interference Mitigation for MIMO-FMCW Automotive Radar

Sian Jin, Pu Wang, Petros Boufounos, Philip V. Orlik, Ryuhei Takahashi, and Sumit Roy

Abstract—This paper considers mutual interference mitigation among automotive radars using frequency-modulated continuous wave (FMCW) signal and multiple-input multiple-output (MIMO) virtual arrays. For the first time, we derive a general interference signal model that fully accounts for not only the time-frequency incoherence, e.g., different FMCW configuration parameters and time offsets, but also the slow-time code MIMO incoherence and array configuration differences between the victim and interfering radars. Along with a standard MIMO-FMCW object signal model, we turn the interference mitigation into a spatial-domain object detection under incoherent MIMO-FMCW interference described by the explicit interference signal model, and propose a constant false alarm rate (CFAR) detector. More specifically, the proposed detector exploits the structural property of the derived interference model at both transmit and receive steering vector space. We also derive analytical closedform expressions for probabilities of detection and false alarm. Performance evaluation using both synthetic-level and phased array system-level simulation confirms the effectiveness of our proposed detector over selected baseline methods.

Index Terms—Automotive radar, FMCW, MIMO, interference mitigation, object detection, CFAR.

## I. INTRODUCTION

Advanced driver assistance systems (ADAS) and autonomous driving require a high-resolution environment perception system capable of detecting and identifying stationary (e.g., buildings, trees, and guardrails) and dynamic (e.g., vehicles and pedestrians) objects reliably in all weather conditions. Compared with other perception sensors such as cameras and LiDAR, radar offers the potential for operating in adverse weather and night-time conditions at lower cost and processing overhead [2].

Current automotive radars widely adopt frequencymodulated continuous wave (FMCW) techniques [1]–[9], since it enables receivers with low sampling rates while harnessing large sweep frequency bands for high resolution in range. On the other hand, they are limited in use for high-resolution perception tasks due to poor angular resolution, particularly in the elevation domain. To increase the angular resolution, automotive radar chip vendors take various approaches to form a large aperture for highly directional beams. Mechanically scanned FMCW radars, e.g., Navtech CTS350-X, have been used to collect 360<sup>◦</sup> bird’s-eye view (BEV) radar images in the rangeazimuth domain but without the Doppler velocity [10]. Synthetic aperture radar (SAR) techniques create high-resolution two-dimensional images of the scene by coherently combining returned radar waveforms with the assumption of known ego vehicle motion [11]. Multiple-input multiple-output (MIMO) radar is another cost-efficient approach to form a large virtual array with a reduced number of transmitting (Tx) and receiving (Rx) antennas and radio frequency (RF) chains. To achieve this, one needs to separate the corresponding waveform to each transmitter at each receiver, provided that the transmitting waveforms from different Tx antennas can be separable or orthogonal. Orthogonal MIMO signaling schemes can be realized in time-division multiplexing (TDM), frequency-division multiplexing (FDM), and Doppler-division multiplexing (DDM) (also referred to as slow-time MIMO) modes [9], [12], [13]. As of today, the combined MIMO-FMCW automotive radar has been commercialized by chip vendors to achieve hundreds and even thousands of virtual channels in the azimuth and elevation domains [14], [15].

![](images/ecf2be3de6d8b74e5cde230f4f6e52677e12d01b81b89a1aeca7d22d87d5376a.jpg)  
Fig. 1. Illustration for mutual interference mitigation for MIMO-FMCW automotive radar, where both victim and interfering vehicles use MIMO transmitter and receiver arrays to transmit and receive waveform.

When multiple automotive radars operate in the same regulated frequency bands, e.g., 76 − 81 GHz, it is anticipated that mutual radar interference becomes a serious issue, as shown in Fig. 1. Mutual interference mitigation has been considered for traditional FMCW radar and can be classified as:

1) Fast-time (range) domain: interference-zeroing [16]– [18], sparse reconstruction [19], [20], adaptive noise cancellers [21], signal separation [22], fast-time-frequency mode retrieval [23], and fast-time neural networks [24], [25];

2) Slow-time (Doppler) domain: waveform randomization [26], [27], ramp filtering [28], and slow-time neural network [29];

3) Joint range-Doppler domain: neural network based de-

noisers [30]–[33];

4) Communication-assisted scheduling, such as timedivision multiple access [34], and chirp slope and frequency offset scheduling [35].

For MIMO-FMCW automotive radar, interference mitigation can be done in the MIMO code domain [36] but it requires additional communication and coordination between the victim and interfering radars. On the other hand, spatialdomain mitigation approaches were considered to make use of additional degrees of freedom in the antenna or beamspace domain. Initial efforts include receiver beamforming-based approaches [37]–[41], null steering [42], and linear constraints minimum variance (LCMV) beamforming [43].

Different from all the above efforts, our approach is to understand the interference signal at the output of the range-Doppler and MIMO waveform separation of a standard automotive radar. With such a mathematical understanding of the interference signal, we are able to approximate the interference using a Kronecker subspace signal model in the spatial (object angles seen from both the transmitter and receiver) domain and turn the mutual interference mitigation into an object detection problem under a Kronecker subspace interference plus noise. Our contributions are summarized below:

• For the first time, we derive an explicit signal model for the spatial-domain MIMO-FMCW interference under the time-frequency incoherence, the MIMO code incoherence, and the array configuration difference between the victim and interfering radars.

• We also show that the derived interference signal model reduces to existing models used in the literature under special cases such as coherent interference, TDM-MIMO interference, and phased array interference.

• We exploit the structure of both Tx and Rx steering vectors of the incoherent interference. Particularly, we decompose the incoherent MIMO-FMCW interference into two orthogonal components: one is completely aligned with the object Tx steering vector, and the other is in its orthogonal complement subspace.

• We propose a generalized subspace-based (GS) detector that minimizes the variance of interference-plus-noise with known statistics after Rx beamforming, maintains a fixed gain at the object direction and cancels the residual incoherent interference.

• We derive closed-form analytical expressions of probabilities of false alarm and detection and confirm that the proposed detector has the property of constant false alarm rate (CFAR).

• We further show analytical convergence to existing receive-subspace-based detectors (RS detector or nullsteering detector) and the clairvoyant detector under certain conditions.

• We provide a comprehensive numerical comparison between the proposed detector and several baseline methods (including the state-of-the-art RS and LCMV detectors) using analytical performance curves, synthetic data, and more realistic data that accounts for element-wise array beampatterns.

![](images/d288be55de463111b62f318061307cb20d9d94b18d19d489dbfd24249a457db4.jpg)  
Fig. 2. MIMO-FMCW waveforms with Tx-pulse code $c _ { m , k }$ applied to the same source FMCW waveform. The Tx-pulse codes can vary depending on the operation mode: slow-time MIMO/DDM-MIMO (e.g., Hadamard or Chu sequences), TDM-MIMO (one-hot vectors), and phased array (all-one vectors with analog phase shifters).

Throughout this paper, we use $( \cdot ) ^ { T }$ to represent transpose, use $( \cdot ) ^ { * }$ to represent conjugate, and use ${ \bf \widehat { \mathbf { \Omega } } } ( \cdot ) ^ { H }$ to represent conjugate transpose. We use ${ \mathbf { P } } _ { \mathbf { H } } \triangleq { \mathbf { H } } ( { \mathbf { \bar { H } } } ^ { H } { \mathbf { H } } ) ^ { - 1 } { \mathbf { \bar { H } } } ^ { H }$ to denote the projection matrix projecting to the column space of H. We use $\mathbf { P _ { H } ^ { \perp } } \triangleq \mathbf { I } - \mathbf { P _ { H } }$ to denote the projection matrix projecting to the space orthogonal to the column space of H. $Q _ { 1 } ( x , y )$ denotes the Marcum Q-function of order 1 [44]. All indices are counted from 0.

## II. SIGNAL MODEL

In the following, we briefly overview the object signal model, derive the interference signal model in more detail, and show the convergence of the derived interference model to existing results in various operation modes, e.g., coherent interference, phased array interference, and TDM-MIMO interference.

## A. MIMO-FMCW Waveform

As shown in Fig. 2, we consider a victim radar of M Tx antennas collocated with N Rx antennas over K pulses within a coherent processing interval (CPI). The source FMCW waveform of the victim radar is

$$
s ( t ) = e ^ { j \pi \beta t ^ { 2 } } D _ { 0 , T } ( t ) ,\tag{1}
$$

where $\beta$ is the chirp rate, $T$ is the chirp duration, and

$$
\begin{array} { r } { D _ { a , b } ( t ) = \left\{ \begin{array} { l l } { 1 , } & { a \leq t \leq b } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{2}
$$

The RF waveform on Tx antenna m over K pulses is [9]

$$
s _ { m } ( t ) = \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } s ( t - k T _ { \mathrm { P R I } } ) e ^ { j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } ) } ,\tag{3}
$$

where $c _ { k , m }$ is the Tx-pulse code on m-th Tx antenna and k-th pulse, T is the pulse repetition interval of the victim radar and $f _ { c }$ is the carrier frequency. In (3), the Tx-pulse codes may vary depending on the operation mode [13]:

![](images/68a2376126c2530f65956a95fa07d9663122588597a82c24b2dc7e4068400cdf.jpg)  
Fig. 3. The receiver architecture (right) of a victim MIMO-FMCW automotive radar that captures both transmitted waveforms from its own transmitter (upper left) and an incoherent MIMO-FMCW interfering radar (lower left) with different FMCW configuration parameters, time offset, MIMO codes, and transmitter array configurations.

• slow-time MIMO/DDM-MIMO mode: the codes at Tx m are chosen to achieve zero/low cross-correlation over transmitted antennas. One example is the use of binary Hadamard code where $^ { c _ { k , m } }$ is taken from the columns of a Hadamard matrix of size K, assuming $K > M$

$$
{ \frac { 1 } { K } } \sum _ { k } c _ { k , m } c _ { k , m ^ { \prime } } = \left\{ { 1 \atop 0 } \right. \quad \mathrm { i f } \ m = m ^ { \prime } .\tag{4}
$$

Other choices include Chu sequence, optimized binary phase codes, and phase codes that spread the interantenna interference in the Doppler domain [13], [45].

• TDM-MIMO mode: the codes at Tx m is a one-hot vector where $c _ { k , m } = 1$ and $c _ { k , m ^ { \prime } } = 0 , m ^ { \prime } \neq m$ . In other words, only 1 Tx is active during one pulse and each Tx takes turns transmitting.

• phased array mode: the codes at Tx m are 1, i.e., $c _ { k , m } =$ 1 for all k. The beamforming angle is controlled by an additional beamforming process which is omitted here.

## B. Object Signal Model

Following the receiver processing at the victim radar of Fig. 3, we provide a quick overview of object signal model in the spatial domain, e.g., Tx transmitting and Rx receiving angles. Similar derivation of the object signal model can be found in [9], [46].

For an object of range R and relative radial velocity v, the round-trip propagation delay from victim radar’s m-th Tx antenna to its n-th receiving antenna is

$$
\tau _ { m , n } ( t ) = 2 \frac { R + v t } { c } + m \frac { d _ { t } \sin ( \phi _ { t } ) } { c } + n \frac { d _ { r } \sin ( \phi _ { r } ) } { c } ,\tag{5}
$$

where $d _ { t }$ and $d _ { r }$ are the Tx and Rx antenna element spacing, $\phi _ { t }$ and $\phi _ { r }$ are the Tx and Rx angle for the object, and c is the speed of propagation. If the object is in the far field, we have the approximation $\phi _ { t } = \phi _ { r }$

As shown in the upper right (victim Rx) of Fig. 3, the received signal goes through processing blocks such as local oscillator (LO), low-pass filtering (LPF), analog-to-digital converter (ADC), fast-time/range FFT, slow-time/Doppler FFT, and MIMO waveform separation at each receiver antenna chain. A step-by-step derivation of the object signal model is included in Appendix A. At the output of the MIMO waveform separation and by stacking $\{ y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) \}$ into a vector, one can form an M N × 1 virtual array signal for an object at a given pair of range bin $l ^ { \prime }$ and Doppler bin $k ^ { \prime }$ as

$$
\mathbf { y } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) = b ( l ^ { \prime } , k ^ { \prime } ) \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } .\tag{6}
$$

where $\mathbf { a } _ { t } \triangleq [ 1 , e ^ { - j 2 \pi f _ { \phi _ { t } } } , \hdots , e ^ { - j 2 \pi f _ { \phi _ { t } } ( M - 1 ) } ] ^ { T }$ is the object Tx steering vector with a spatial frequency of $f _ { \phi _ { t } } , \ \mathbf { a } _ { r } \ \triangleq$ $[ 1 , e ^ { - j 2 \pi f _ { \phi _ { r } } } , \ldots , e ^ { - j 2 \pi f _ { \phi _ { r } } ( N ^ { \bullet } - 1 ) } ] ^ { T }$ is the object Rx steering vector with a spatial frequency of $f _ { \phi _ { r } }$ , and ⊗ represents the Kronecker product. It is seen that the spatial-domain object signal has a Kronecker structure between the object Tx and Rx steering vectors.

## C. Interference Signal Model

In the lower left of Fig. 3, an interfering radar also employs the MIMO-FMCW signaling scheme with possibly different MIMO array configurations such as the number of Tx antennas ${ \widetilde { M } } ,$ inter-element spacing, and Tx-pulse codes $\widetilde { c } _ { \widetilde { k } , \widetilde { m } }$ , FMCW configuration parameters, and time offsets.

Transmitted MIMO-FMCW Waveform at Interfering TX: More specifically, the m -th interfering Tx antenna sends coded $\widetilde { K }$ pulses

$$
\widetilde { s } _ { \widetilde { m } } ( t ) = \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \widetilde { c } _ { \widetilde { k } , \widetilde { m } } \widetilde { s } ( t - \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } - \widetilde { \tau } _ { s y n } ) e ^ { j 2 \pi f _ { c } ( t - \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } - \widetilde { \tau } _ { s y n } ) } ,\tag{7}
$$

where the source FMCM waveform $\widetilde s ( t )$ shares the same expression as (1) but with different chirp rate $\widetilde { \beta }$ and pulse duration $\widetilde { T } , \widetilde { \tau } _ { s y n }$ is the transmit synchronization delay (initial time offset) between the reference Tx antennas of the victim radar and the interfering radar, $\widetilde { c } _ { \widetilde { k } , \widetilde { m } }$ is the Tx-pulse code of the interfering radar that likely are different from those used at the victim Tx), and $\widetilde { T } _ { \mathrm { P R I } }$ is the PRI at the interfering radar.

Interference Waveform at Receiving Antennas of Victim $R x \colon$ For an interfering radar of range R and radial velocity v relative to the victim radar, the one-way propagation delay from its m-th Tx antenna to the n-th Rx antenna of victim radar is

$$
\widetilde { \tau } _ { \widetilde { m } , n } ( t ) = \frac { \widetilde { R } + \widetilde { v } t } { c } + \widetilde { m } \frac { \widetilde { d } _ { t } \sin ( \widetilde { \phi } _ { t } ) } { c } + n \frac { d _ { r } \sin ( \widetilde { \phi } _ { r } ) } { c } ,\tag{8}
$$

where $\widetilde { d } _ { t }$ is the Tx antenna element spacing at the interferer, and $\ddot { \phi } _ { t }$ and $\phi _ { \tau }$ are the interference Tx and Rx angles with respect to the boresight of the interfering radar and the victim radar. At the victim Rx of Fig. 3, the n-th receiver observes the RF signal from the interferer

$$
\begin{array} { l } { { \displaystyle s _ { n } ^ { i } ( t ) = \widetilde \alpha \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \widetilde { s } _ { \widetilde { m } } ( t - \widetilde { \tau } _ { \widetilde { m } , n } ( t ) ) } } \\ { { \displaystyle \approx \widetilde \alpha e ^ { - j 2 \pi f _ { c } \widetilde { \tau } } \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \widetilde { c } _ { \widetilde { k } , \widetilde { m } } \widetilde { s } ( t - \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } - \widetilde { \tau } _ { s y n } - \widetilde { \tau } ) } } \\ { { \displaystyle \quad \times ~ e ^ { j 2 \pi f _ { c } ( t - \widetilde { k } \widetilde { T } _ { \mathrm { P H } } - \widetilde { \tau } _ { s y n } ) } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } e ^ { - j 2 \pi f _ { c } \frac { \widetilde { v } t } { c } } } , } \end{array}\tag{9}
$$

where α is the received complex amplitude of the interference, $\widetilde { \tau } = \widetilde { R } / c$ is the reference one-way propagation delay from interferer to the victim radar, and $\widetilde { f } _ { \phi _ { t } } ~ = ~ \widetilde { d } _ { t } \mathrm { s i n } ( \widetilde { \phi } _ { t } ) / \lambda$ and $\widetilde { f } _ { \phi _ { r } } = d _ { r } \mathrm { s i n } ( \widetilde { \phi } _ { r } ) / \lambda$ are the normalized spatial frequency at the interferer transmitting antennas and victim receiving antennas.

Interference Waveform after LO and LPF at Victim Rx: Since our goal is to derive the interference signal model seen at the victim Rx, we need to convert the interference time, i.e., $\widetilde { k } \widetilde { T } _ { \mathrm { P R I } } + \widetilde { \tau } _ { s y n } , \widetilde { k } = 0 , 1 , \dots , \widetilde { K } - 1$ to the reference of the victim radar. As details are shown in Appendix B and defining $\widetilde { \tau } _ { \boldsymbol { k } , \widetilde { \boldsymbol { k } } } ^ { \prime }$ as the time offset between the $\widetilde { k } { - } \mathrm { t h }$ pulse of the interfering radar relative to the k-th pulse at the victim radar, we can express the low-pass filtered interference signal $a _ { n } ^ { s , l o w } ( t )$ sampled at $t = k T _ { \mathrm { P R I } } + l \Delta T$ as

$$
\begin{array} { r l r } {  { a _ { n } ^ { i } ( l , k ) = a _ { n } ^ { i , l o w } \big ( k T _ { \mathrm { P R I } } + l \Delta T \big ) } } \\ & { } & { \quad = \widetilde { \alpha } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } } \overset { \widetilde { M } - 1 } { \widetilde { m } } \overset { \widetilde { K } - 1 } { \widetilde { k } = 0 } \widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } e ^ { j \pi \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) ^ { 2 } } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } } } \\ & { } & { \quad \times \ : e ^ { j \pi ( \widetilde { \beta } - \beta ) ( l \Delta T ) ^ { 2 } } e ^ { - j 2 \pi \widetilde { f } _ { r , k , \widetilde { k } } l } \mathbf { 1 } [ l \in \mathcal { L } _ { k , \widetilde { k } } ^ { i } ] } \\ & { } & { \quad \times \ : e ^ { - j 2 \pi \widetilde { f } _ { d } k } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } } \end{array}\tag{10}
$$

where $\widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } }$ is the slow-time code of the interfering radar ob-<sup>e</sup>served at k-th victim radar pulse and is defined in Appendix B, $\mathbf { 1 } [ \cdot ]$ is the indicator function,

$$
\begin{array} { r l r } & { } & { \mathcal { L } _ { k , \widetilde { k } } ^ { i } \triangleq \left\{ l : 0 < \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) - ( \widetilde { \beta } - \beta ) l \Delta T < f _ { L } , \qquad ( 1 1 ) \right. } \\ & { } & { \left. ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) < l \Delta T < \operatorname* { m i n } \left\{ T , \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } + \widetilde { T } \right\} \right\} } \end{array}
$$

is the set of interference contaminated sample indices, $\widetilde { f } _ { r , k , \widetilde { k } } \triangleq$ $\begin{array} { r } { ( \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) + \frac { \widetilde { v } } { \lambda } ) \Delta T } \end{array}$ is the normalized interference initial fast-time frequency, and $\widetilde { f } _ { d } ~ = ~ f _ { c } \widetilde { v } T _ { \mathrm { P R I } } / c$ is the normalized interference Doppler frequency.

Interference Waveform after range FFT at Victim Rx: Applying the range FFT to the sampled interference signal $a _ { n } ^ { i } ( l , k )$ we obtain its range spectrum at the n-th Rx antenna, l<sup>0</sup>-th range bin and k-th pulse as

$$
x _ { n } ^ { i } ( l ^ { \prime } , k ) = \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } e ^ { - j 2 \pi \widetilde { f } _ { d } k } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } ,\tag{12}
$$

where

$$
\begin{array} { l } { { \displaystyle \widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } \triangleq \widetilde { \alpha } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } } \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } e ^ { j \pi \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) ^ { 2 } } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } } } } \\ { { \displaystyle \quad \times \sum _ { l = 0 } ^ { L - 1 } e ^ { j \pi ( \widetilde { \beta } - \beta ) ( l \Delta T ) ^ { 2 } } \mathbf { 1 } \left[ l \in \mathcal { L } _ { k , \widetilde { k } } ^ { i } \right] e ^ { - j 2 \pi ( \widetilde { f } _ { r , k , \widetilde { k } } + \frac { l ^ { \prime } } { L } ) l } } } \end{array}\tag{13}
$$

is the coded complex interference amplitude from the m-th interfering Tx antenna at victim radar’s range bin l<sup>0</sup> and pulse k. It is worthy noting that $\widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } }$ varies with pulse index k since it is a function of $\widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime }$ . Moreover, $\widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } }$ is unknown at the victim Rx.

Interference Waveform after Doppler FFT and Waveform Separation at Victim Rx: For MIMO waveform separation, the victim Rx only applies the same procedure using the Tx-pulse code from the victim Tx and assumes no prior knowledge about the Tx-pulse code of the interfering Tx. As a result, the interference spectrum at l<sup>0</sup>-th range bin and k<sup>0</sup>-th Doppler bin of the victim Rx is given as

$$
\begin{array} { r l r } {  { y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \sum _ { k = 0 } ^ { K - 1 } x _ { n } ^ { i } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } e ^ { - j 2 \pi \frac { k ^ { \prime } } { K } k } } } \\ & { } & \\ & { } & { = \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { k = 0 } ^ { K - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } } \\ & { } & \\ & { } & { = \widetilde { a } _ { t , m } ^ { \prime } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } n } , \qquad ( \widetilde { \iota } } \end{array}\tag{14}
$$

where the Tx-pulse codes $c _ { k , m }$ used at the victim Tx are used for the waveform separation,

$$
\widetilde { a } _ { t , m } ^ { \prime } = \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { k = 0 } ^ { K - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { t } } \widetilde { m } } .\tag{15}
$$

Spatial-Domain Interference Steering Vector at Victim Rx: Stacking $\{ y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \}$ into a vector, we obtain the interference range-Doppler spectrum on an $M N \times 1$ virtual array

$$
\mathbf { y } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } .\tag{16}
$$

where

$$
\widetilde { \mathbf { a } } _ { t } ^ { \prime } \triangleq [ \widetilde { a } _ { t , 0 } ^ { \prime } , \widetilde { a } _ { t , 1 } ^ { \prime } , \dots , \widetilde { a } _ { t , M - 1 } ^ { \prime } ] ^ { T } ,\tag{17}
$$

is the $M \times 1$ interfering Tx steering signal seen at the victim Rx, and

$$
\widetilde { \mathbf { a } } _ { r } \triangleq [ 1 , e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } } , \hdots , e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } ( N - 1 ) } ] ^ { T }\tag{18}
$$

is the $N \times 1$ interfering Rx steering vector.

From (16), it is seen that the spatial-domain interference steering vector also has the Kronecker structure between the Tx and Rx steering vectors, like the spatial-domain object steering vector in (6). The main difference lies in the interference Tx steering vector of (15) which is a function of the transmitting power of the interfering radar, interferingvictim relative distance and Doppler frequency, FMCW timefrequency incoherence (e.g., chirp rate, pulse duration, pulse repetition interval), MIMO incoherence (e.g., MIMO code and Tx array configuration), and timing offset between the interfering and victim radars. In other words, the object Tx/Rx steering vectors and interfering Rx steering vector are fully determined by the object-victim and interfering-victim directions due to their Fourier vector structure, while the interfering Tx steering vector is almost unknown as its direction in the M-dimensional subspace is not only determined by the relative interfering-victim direction but also the mentioned incoherence.

## D. Examples of MIMO-FMCW Interference Signal Model

In the following, we show that our derived MIMO-FMCW interference model reduces to three special interference scenarios widely used in the existing literature when certain conditions are met.

1) Coherent Interference: In this part, we validate that when interferer and victim radar are synchronized $( \widetilde { \tau } _ { s y n } = 0 )$ have the same waveform parameters $( \widetilde { \beta } = \beta , \widetilde { T } _ { \mathrm { P R I } } = T _ { \mathrm { P R I } }$ $\widetilde { T } = T , \widetilde { K } = K )$ , number of Tx antennas $( { \tilde { M } } = M )$ and slow-time code $( \{ \widetilde { c } _ { \widetilde { k } , \widetilde { m } } \} = \{ c _ { k , m } \} )$ , the received interference <sup>e</sup>signal, referred to as the coherent interference signal, has the same structure as the object signal [26].

Under the coherent interference step, by (68), we have $\tau _ { k , \widetilde k } ^ { \prime } = 0$ and ${ \mathcal { K } } _ { \widetilde { k } } = \{ \widetilde { k } \}$ . Then, by (69), we have $\widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } =$ $\widetilde { c } _ { k , \widetilde { m } } = c _ { k , \widetilde { m } } \mathrm { i f } k = \widetilde { k } ,$ , and otherwise $\widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } \ = \ 0 ;$ as <sup>e</sup>here we consider the coherent interference is dechirped into the victim radar, i.e., $0 ~ < ~ \widetilde { \beta } \widetilde { \tau } ~ < ~ f _ { L }$ , we have $\mathcal { L } _ { k , \widetilde { k } } ^ { i } \ =$ $\{ \lceil \widetilde { \tau } / \Delta T \rceil , \dots , \lfloor T / \Delta T \rfloor \}$ ; the normalized interference initial fast-time frequency reduces to $\begin{array} { r } { \widetilde { f } _ { r , k , \widetilde { k } } = ( \widetilde { \beta } \widetilde { \tau } + \frac { \widetilde { v } } { \lambda } ) \Delta T } \end{array}$ . Based on these $\widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } }$ in (13) becomes $\widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } = \widetilde { \alpha } _ { l ^ { \prime } } c _ { k , \widetilde { m } }$ , where $\widetilde { \alpha } _ { l ^ { \prime } } = \widetilde { \alpha } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } } e ^ { j \pi \widetilde { \beta } \widetilde { \tau } ^ { 2 } } \sum _ { l = 0 } ^ { L - 1 } { \bf 1 } \left[ l \in \mathcal { L } _ { k , \widetilde { k } } ^ { i } \right] e ^ { - j 2 \pi ( \widetilde { f } _ { r , k , \widetilde { k } } + \frac { l ^ { \prime } } { L } ) l }$ Then, the range-Doppler interference spectrum in (14) reduces to

$$
\begin{array} { r l r } {  { y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) } } \\ & { } & { = \widetilde { \alpha } _ { l ^ { \prime } } \sum _ { \widetilde { m } \neq m } ( \sum _ { k = 0 } ^ { K - 1 } c _ { k , \widetilde { m } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } ) e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } } \\ & { } & { + b ^ { i } ( l ^ { \prime } , k ^ { \prime } ) e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } m + \widetilde { f } _ { \phi _ { r } } n ) } , \qquad ( 1 9 ) } \end{array}
$$

where $\begin{array} { r } { b ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \ \triangleq \ \widetilde \alpha _ { l ^ { \prime } } \left( \sum _ { k = 0 } ^ { K - 1 } e ^ { - j 2 \pi ( \widetilde f _ { d } + \frac { k ^ { \prime } } { K } ) k } \right) } \end{array}$ . Notice that when $\begin{array} { r } { \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } \ \approx \ 0 , } \end{array}$ i.e., when the normalized interference Doppler frequency fall near the Doppler bin $k ^ { \prime } { . }$ , then $b ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \approx K \widetilde { \alpha } _ { l ^ { \prime } }$ indicating a peak on Doppler spectrum, and in this case

$$
y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \approx b ^ { i } ( l ^ { \prime } , k ^ { \prime } ) e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } m + \widetilde { f } _ { \phi _ { r } } n ) }\tag{20}
$$

due to (67). Comparing the object signal $y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } )$ in (65) and the interference signal $y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ in (20), we validate that under the coherent interference case, the interference model derived in Section II-C has a similar structure compared to the object signal model derived in Section II-B.

2) Phased Array Radar Interference: In this part, we show that when all radars are phased array radar [47] with slow-time code $( \{ c _ { k , m } = 1 \} )$ , the spatial-domain interference signal has a Fourier structure.

Under the phased array radar setup, $\{ c _ { k , m } = 1 \}$ implies that $\{ \widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } ~ = ~ 1 \}$ and $\{ c _ { k , m } ^ { * } ~ = ~ 1 \}$ . Then, $\widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } }$ in (13) <sup>e</sup>is independent of m and $y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ in (14) is independent of m. Rewriting $\widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } }$ as $\widetilde { \alpha } _ { l ^ { \prime } , k }$ and rewriting $y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ as $y _ { n } ^ { i } ( l ^ { \prime } , k ^ { \prime } )$ , the range-Doppler interference spectrum in (14) reduces to

$$
y _ { n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { a } _ { t } ^ { \prime } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } n } ,\tag{21}
$$

where

$$
\widetilde { a } _ { t } ^ { \prime } = \sum _ { k = 0 } ^ { K - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } \left( \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \widetilde { w } _ { \widetilde { m } } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { t } } \widetilde { m } } \right)\tag{22}
$$

and $\widetilde { w } _ { \widetilde { m } }$ is the Tx beamforming weights on m-th interference Tx antenna. Stacking $\{ y _ { n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \}$ into a vector, we obtain the interference range-Doppler spectrum on a $N \times 1 ~ \mathrm { R x }$ array

$$
\mathbf { y } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { a } _ { t } ^ { \prime } \widetilde { \mathbf { a } } _ { r } ,\tag{23}
$$

which is a Fourier vector. Notice that this interference structure also applies in the special case where all radars adopt a single Tx antenna.

3) TDM-MIMO Radar Interference: In this part, we show that when all radars are TDM-MIMO radars, the spatialdomain interference signal has the same structure as in (16).

Mathematically, the modification in the above derivation is in two folds. First, the slow-time phase code $^ { c _ { k , m } }$ is replaced as the slow-time code with $c _ { k , m } = 1 \mathrm { i f } \ m =$ mod $( k , M )$ and $c _ { k , m } = 0$ otherwise, for $k = 0 , 1 , \ldots , K - 1$ and m = $0 , 1 , \ldots , M - 1$ . Second, in the Doppler FFT equations (65)

and (14), $e ^ { - j 2 \pi { \frac { k ^ { \prime } } { K } } k }$ is replaced by $e ^ { - j 2 \pi } \frac { k ^ { \prime } } { \lfloor K / M \rfloor } k$ because only $\lfloor K / M \rfloor$ pulses are used in TDM-MIMO for each antenna. These two modifications do not affect the interference structure in (16).

## III. PROBLEM FORMULATION

In this section, we first formulate object detection as a composite hypothesis testing problem and review existing detectors.

## A. Spatial-domain Detection Problem under Interference

Given the target and interference signal models over a given range-Doppler bin, the spatial-domain object detection under mutual interference is formulated as a composite hypothesis testing problem

$$
\left\{ \begin{array} { l l } { H _ { 0 } , } & { \mathbf { y } = \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } } \\ { H _ { 1 } , } & { \mathbf { y } = b \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } + \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } , } \end{array} \right.\tag{24}
$$

where y is the complex-valued range-Doppler spectrum at a given range-Doppler bin $( l ^ { \prime } , k ^ { \prime } )$ , b is the complex-valued unknown object amplitude, Q is the number of interference, $\mathbf { a } _ { t }$ and ${ \bf a } _ { r }$ are object Tx and Rx steering vectors defined below $( 6 ) .$ $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ and $\widetilde { \mathbf { a } } _ { r , q }$ are the q-th decoded interference Tx and Rx steering vector given in the form of (17) and (18), and the noise $\mathbf z \sim \mathcal { C N } ( \mathbf 0 , \sigma ^ { 2 } \mathbf I _ { M N } )$ with ${ \mathbf { I } } _ { M N }$ denoting the identity matrix of size MN. The null hypothesis $H _ { 0 }$ consists of interference and noise, and the alternative hypothesis $H _ { 1 }$ consists of the object signal plus interference and noise.

It is worth noting that, in (24), we assume the knowledge of the interference Rx steering vector $\widetilde { \mathbf { a } } _ { r }$ . This assumption on $\widetilde { \mathbf { a } } _ { r , q }$ is motivated by the observation that it is a Fourier vector at the angle of the interfering radar. We assume the angle of arrival in $\widetilde { \mathbf { a } } _ { r , q }$ and the number of interference $Q$ can be estimated from nearby range-Doppler bins.

## B. Existing Detectors

1) Clairvoyant Detector: Assuming the perfect knowledge of $\widetilde { \mathbf { a } } _ { t } ^ { \prime } ,$ , the clairvoyant detector is given by

$$
T ^ { C } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } ( \mathbf { y } - \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } ) \right| ^ { 2 } } { \left| \left| \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right| \right| ^ { 2 } } .\tag{25}
$$

It is equivalent to removing all interference components $\begin{array} { r } { \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } } \end{array}$ before the matched filtering with respect to the object steering vector. The probabilities of false alarm and detection of (25) can be derived as

$$
P _ { F A } ^ { C } = e ^ { - \frac { 1 } { 2 } \gamma } , \quad P _ { D } ^ { C } = Q _ { 1 } \left( \sqrt { \lambda ^ { C } } , \sqrt { \gamma } \right) ,\tag{26}
$$

where $\gamma$ is the threshold used for detection, and the parameter $\lambda ^ { c }$ is given as

$$
\lambda ^ { C } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \left| | \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } | \right| ^ { 2 } = \frac { 2 M N | b | ^ { 2 } } { \sigma ^ { 2 } } .\tag{27}
$$

It is worthy noting that the clairvoyant detector of (25) cannot be implemented in practice due to the strong assumption about the incoherent interference Tx steering vector $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$

2) Receiver Subspace (RS) Detector of [3]: Assuming the number of Tx antennas is small, one can directly treat $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ as an nuisance parameter in (24) and estimate it under both hypotheses. The resulting generalized likelihood ratio test (GLRT) is given by [3]

$$
T ^ { R S } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right) ^ { H } \mathbf { y } \right| ^ { 2 } } { \left| \left| \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right| \right| ^ { 2 } } ,\tag{28}
$$

where $\widetilde { \mathbf { A } } _ { r } \triangleq [ \widetilde { \mathbf { a } } _ { r , 1 } , \widetilde { \mathbf { a } } _ { r , 2 } , \hdots , \widetilde { \mathbf { a } } _ { r , Q } ]$ is a stack of Q interference Rx steering vectors. It is clear to see that the GLRT only exploits the receiver subspace $\widetilde { \mathbf { A } } _ { r }$ of the interferences. Correspondingly, the probabilities of false alarm probability and detection are given by

$$
P _ { F A } ^ { R S } = e ^ { - \frac { 1 } { 2 } \gamma } , \quad P _ { D } ^ { R S } = Q _ { 1 } \left( \sqrt { \lambda ^ { R S } } , \sqrt { \gamma } \right) ,\tag{29}
$$

where

$$
\lambda ^ { R S } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \left| \left| \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \widetilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right| \right| ^ { 2 } .\tag{30}
$$

3) LCMV Detector of [43]: In [43], a conventional linear constraint minimum variance (LCMV) beamformer is adopted. It assumes that

$$
\sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \widetilde { \mathbf { R } } ) ,\tag{31}
$$

where $\widetilde { \bf R }$ is a normalized covariance matrix. Assuming the perfect knowledge of $\widetilde { \mathbf { R } } ,$ the LCMV solves the following optimization problem [48]:

$$
\begin{array} { l } { \displaystyle \operatorname* { m i n } _ { \mathbf { w } } ~ \mathbf { w } ^ { H } \widetilde { \mathbf { R } } \mathbf { w } } \\ { s . t . ~ \left( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right) ^ { H } \mathbf { w } = 1 . } \end{array}\tag{32}
$$

which leads to the LCMV detector [43]:

$$
{ \cal T } ^ { L C M V } ( { \bf y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \left( \widetilde { \bf R } ^ { - 1 } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right) ^ { H } { \bf y } \right| ^ { 2 } } { \left| \left| \widetilde { \bf R } ^ { - \frac { 1 } { 2 } } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| \right| ^ { 2 } } .\tag{33}
$$

Given the knowledge of $\widetilde { \mathbf { R } } .$ , the probabilities of false alarm and detection are given by

$$
P _ { F A } ^ { L C M V } = e ^ { - \frac { 1 } { 2 } \gamma } , \quad P _ { D } ^ { L C M V } = Q _ { 1 } \left( \sqrt { \lambda ^ { L C M V } } , \sqrt { \gamma } \right) ,\tag{34}
$$

where

$$
\lambda ^ { L C M V } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \left\| \widetilde { \mathbf { R } } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right\| ^ { 2 } .\tag{35}
$$

## IV. PROPOSED OBJECT DETECTION UNDER MIMO-FMCW MUTUAL INTERFERENCE

In the following, we first demonstrate limitations inherent in the RS and LCMV detectors and gain insights through an in-depth examination of the clairvoyant detector. Then, we propose a generalized subspace (GS) detector that leverages both the Tx and Rx steering vectors of the interference, followed by a comprehensive theoretical performance analysis of the detection performance under the mutual interference.

![](images/5834f4a379a1432d313121e297085ee0dc0336136e6572edf7485796d9c677df.jpg)  
Fig. 4. Decomposition of $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ into $\widetilde { b } _ { q } \mathbf { a } _ { t }$ and $\mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ in a 3-D example, where the plane is the orthogonal subspace of $\mathbf { a } _ { t } .$

## A. Observations from Existing Detectors

For the RS detector of (28), it projects each interference signal $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } , q = 1 , 2 , \ldots , Q$ to 0, i.e.,

$$
\begin{array} { r } { ( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \widetilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ) ^ { H } ( \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = 0 , } \end{array}\tag{36}
$$

because the interference Rx steering vector $\widetilde { \mathbf { a } } _ { r , q }$ is projected to its orthogonal subspace, i.e., $( \mathbf { P } _ { \widetilde { \mathbf { A } } _ { \alpha } } ^ { \perp } \mathbf { a } _ { r } ) ^ { H } \widetilde { \mathbf { a } } _ { r , q } = 0$ . However, this operation fails to maintain the matched filtering gain with respect to the object steering vector as

$$
\begin{array} { r } { ( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) = M \mathbf { a } _ { r } ^ { H } \mathbf { P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } \mathbf { a } _ { r } < M N , } \end{array}\tag{37}
$$

where MN is the coherent matched filtering gain. This is undesirable, particularly when the interference power is small, as the RS detector may mitigate low-power interference at the price of losing object detection gain.

For the LCMV detector of (33), it is sensitive to adaptive estimation error of $\widetilde { \bf R }$ when R is not known a priori. Obtaining an accurate estimate of R requires a large number of homogeneous and object-free training samples, which may be challenging in the presence of dense automotive radars.

Finally, for the clairvoyant detector of (25), one can decompose the $q { \mathrm { - t h } }$ interference Tx steering vector along with the object Tx steering vector and its orthogonal complement direction

$$
\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } = \widetilde { b } _ { q } \mathbf { a } _ { t } + \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime }\tag{38}
$$

as shown in Fig. 4, where the resulting amplitude along $\mathbf { a } _ { t }$ is given

$$
\widetilde { b } _ { q } = \frac { \mathbf { a } _ { t } ^ { H } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } } { | | \mathbf { a } _ { t } | | ^ { 2 } } .\tag{39}
$$

With (38), the clairvoyant detector of (25) can be rewritten as

$$
T ^ { C } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } ( \mathbf { y } - \sum _ { q = 1 } ^ { Q } \widetilde { b } _ { q } \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) \right| ^ { 2 } } { | | \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } | | ^ { 2 } } ,\tag{40}
$$

which implies that the essential interference to cancel is a rank-Q interference with known directions $\mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } , q \ =$ $1 , 2 , \ldots , Q$ , and the unknown parameters sufficient for interference cancellation is $\widetilde { b } _ { q } , q = 1 , 2 , \dots , Q$

## B. Proposed Generalized Subspace (GS) Detector

Since the exact knowledge of $\widetilde { b } _ { q }$ is unknown in advance, we may estimate the power of $\widetilde { b } _ { q } .$ , denoted by $h _ { q } ^ { 2 } .$ , from nearby range-Doppler bins. Assume $\widetilde { b } _ { q } \ \sim \ C \mathcal { N } ( 0 , h _ { q } ^ { 2 } )$ with known

variance $h _ { q } ^ { 2 }$ and $\widetilde { b } _ { q }$ is independent of z. Then, the essential interference plus noise is

$$
\widetilde { \mathbf { z } } = \sum _ { q = 1 } ^ { Q } \widetilde { b } _ { q } \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \mathbf { R } ) ,\tag{41}
$$

and the normalized covariance of z is

$$
\mathbf { R } = \sum _ { q = 1 } ^ { Q } \frac { h _ { q } ^ { 2 } } { \sigma ^ { 2 } } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } + \mathbf { I } _ { M N } .\tag{42}
$$

We first design our Rx beamformer w to satisfy the following criterion:

1) minimize the variance of interference-plus-noise with known covariance after beamforming, i.e., $\mathbf { w } ^ { H } \mathbf { R w }$ ;

2) maintain a fixed gain at the object direction, i.e., $\left( \mathbf { a } _ { t } \otimes \right.$ $\begin{array} { r } { \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 ; } \end{array}$

3) force the the unknown interference $\textstyle \sum _ { q = 1 } ^ { Q } ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } )$ ⊗ $\widetilde { \mathbf { a } } _ { r , q }$ to zero for any $\widetilde { \mathbf { a } } _ { t } ^ { \prime } .$ , i.e.,

$$
\sum _ { q = 1 } ^ { Q } ( ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = 0 ,\tag{43}
$$

for any $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } , q \ = \ 1 , 2 , \ldots , Q .$ , which is equivalent to force $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , q = 1 , 2 , \ldots , Q .$ , where ${ \bf 0 } _ { M }$ denotes the M-dimensional column vector with all 0 elements.

As a result, one needs to solve the following optimization problem:

$$
\begin{array} { r l } & { \underset { \mathbf { w } } { \operatorname* { m i n } } ~ \mathbf { w } ^ { H } \mathbf { R } \mathbf { w } } \\ & { s . t . ~ ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 , } \\ & { ~ ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , q = 1 , 2 , . . . , Q . } \end{array}\tag{44}
$$

Compared to the LCMV beamforming optimization problem in (32), the objective function of the problem in (44) is different in that it uses the essential interference plus noise covariance matrix R instead of the total interference plus noise covariance matrix R .

Denote $\widetilde { \textbf { A } } \triangleq [ \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , 1 } , \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , 2 } , \dots , \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r , Q } ]$ as the stack of $Q$ essential interference virtual steering vectors, and denote

$$
\begin{array} { r } { \mathbf { \Lambda } \triangleq \operatorname { d i a g } \left[ \cfrac { h _ { 1 } ^ { 2 } } { \sigma ^ { 2 } } , \cfrac { h _ { 2 } ^ { 2 } } { \sigma ^ { 2 } } , \dots , \cfrac { h _ { Q } ^ { 2 } } { \sigma ^ { 2 } } \right] , } \end{array}\tag{45}
$$

as the essential-interference-to-noise-ratio (EINR) matrix with diagonal elements reflecting the power values of $Q$ interferences over the noise. Then, we have the important observation

$$
\begin{array} { r l } & { \quad \mathbf { R } ^ { - 1 } = \mathbf { I } _ { M N } - \widetilde { \mathbf { A } } ( \mathbf { A } ^ { - 1 } + \widetilde { \mathbf { A } } ^ { H } \widetilde { \mathbf { A } } ) ^ { - 1 } \widetilde { \mathbf { A } } ^ { H } } \\ & { = \mathbf { I } _ { M N } - \mathbf { P } _ { \mathbf { a } _ { t } } \otimes \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } , } \end{array}\tag{46}
$$

where the regularized projection matrix

$$
\widetilde { { \bf P } } _ { { \widetilde { { \bf A } } } _ { r } , { \Lambda } } = M \widetilde { { \bf A } } _ { r } ( \mathbf { { \Lambda } } \mathbf { { \Lambda } } ^ { - 1 } + M \widetilde { { \bf A } } _ { r } ^ { H } \widetilde { { \bf A } } _ { r } ) ^ { - 1 } \widetilde { { \bf A } } _ { r } ^ { H } .\tag{47}
$$

This special structure of $\mathbf { R } ^ { - 1 }$ implies that the optimal solution of the relaxed version of problem (44)

$$
\begin{array} { l } { \displaystyle \underset { \mathbf { w } } { \operatorname* { m i n } } ~ \mathbf { w } ^ { H } \mathbf { R } \mathbf { w } } \\ { s . t . ~ \left( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right) ^ { H } \mathbf { w } = 1 , } \end{array}\tag{48}
$$

which is

$$
\mathbf { w } ^ { G S } = \frac { \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) } { \left\| \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right\| ^ { 2 } } = \frac { \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) } { M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } } ,\tag{49}
$$

satisfies the last condition of problem (44), where $\widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \scriptscriptstyle \perp } \triangleq$ $\mathbf { I } _ { N } - \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } }$ . Thus, the optimal solution of problem (44) is $\mathbf { w } ^ { G S }$ given in (49).

The beamformer $\mathbf { w } ^ { G S }$ suggests the following detector

$$
T ^ { G S } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \left( \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \mathbf { A } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) \right) ^ { H } \mathbf { y } \right| ^ { 2 } } { M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \mathbf { A } } ^ { \perp } \mathbf { a } _ { r } } .\tag{50}
$$

Because $T ^ { G S } ( \mathbf { y } )$ uses the Rx-side interference information $\widetilde { \mathbf { A } } _ { r }$ and the Tx-side interference information Λ, we call the detector $T ^ { G S } ( \mathbf { y } )$ as the generalized subspace-based (GS) detector. From (50), the interference is mitigated using the Rx array, which is the same as the RS detector. Thus, the GS detector works when the number of interference $Q \leq N$

The GS detector achieves a balance between interference mitigation gain and object correction gain. After Rx beamforming, the q-th interference residual is

$$
\left( \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) \right) ^ { H } ( \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } ) = \widetilde { b } _ { q } M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \widetilde { \mathbf { a } } _ { r , q } ,\tag{51}
$$

and the object correlation gain is

$$
\left( \mathbf { a } _ { t } \otimes ( \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } ) \right) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) = M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \Lambda } ^ { \perp } \mathbf { a } _ { r } .\tag{52}
$$

## C. Theoretical Performance Analysis

Theorem 1: Based on the assumption $\widetilde { b } _ { q } \sim \mathcal { C N } ( 0 , h _ { q } ^ { 2 } )$ with known $h _ { q } ^ { 2 } , q = 1 , 2 , \ldots , Q$ , the probabilities of false alarm and detection for the GS detector under problem (24) are given as

$$
P _ { F A } ^ { G S } = e ^ { - \frac { 1 } { 2 } \gamma } , \quad P _ { D } ^ { G S } = Q _ { 1 } \left( \sqrt { \lambda ^ { G S } } , \sqrt { \gamma } \right) ,\tag{53}
$$

where $\gamma$ is the detection threshold and

$$
\lambda ^ { G S } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } M \mathbf { a } _ { r } ^ { H } \widetilde { \mathbf { P } } _ { \widetilde { \mathbf { A } } _ { r } , \mathbf { A } } ^ { \perp } \mathbf { a } _ { r } .\tag{54}
$$

Proof: See Appendix B.

From the above closed-form expressions of probabilities of false alarm, we have the following Corollary:

Corollary 1: The proposed GS detector is a constant false alarm rate (CFAR) detector in the existence of MIMO-FMCW mutual interference.

Proof: This CFAR property is ensured by the last condition in problem (44), i.e., $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r , q } ) ^ { H } \mathbf { w } \ = \ \mathbf { 0 } _ { M } , q \ =$ $1 , 2 , \ldots , Q$ , and the knowledge of R.

Corollary 2: The proposed GS detector reduces to the clairvoyant detector of (25) when the interference Tx steering vectors $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ are orthogonal to the object Tx steering vector $\mathbf { a } _ { t } .$

Proof: The orthorgonality between $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ and $\mathbf { a } _ { t }$ implies that the EINR matrix $\mathbf { \Lambda } \Lambda = \mathbf { 0 }$ in (45) and $\begin{array} { r } { \tilde { \mathbf { P } } _ { \tilde { \mathbf { A } } _ { r } , \mathbf { A } } ^ { \perp } = \mathbf { I } . } \end{array}$ . As a result,

$$
{ \cal T } ^ { G S } ( { \bf y } ) = { \cal T } ^ { C } ( { \bf y } ) = \frac { 2 | \left( { \bf a } _ { t } \otimes { \bf a } _ { r } \right) ^ { H } { \bf y } | ^ { 2 } } { \sigma ^ { 2 } M N }\tag{55}
$$

with $\begin{array} { r } { \lambda ^ { G S } = \lambda ^ { C } = 2 M N | b | ^ { 2 } / \sigma ^ { 2 } . } \end{array}$

Corollary 3: The proposed GS detector reduces to the RS detector of (28) when the projected interference power along the object Tx steering vector approach to infinity.

Proof: In this case, the EINR matrix $\Lambda \quad $ diag $[ \infty , \infty , \ldots , \infty ]$ . And we have $\begin{array} { c c c } { \displaystyle \widetilde { { \bf P } } _ { \widetilde { { \bf A } } _ { r } , { \bf A } } } & { = } & { \widetilde { { \bf P } } _ { \widetilde { { \bf A } } _ { r } } } \end{array} = \begin{array} { c c }  \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \begin{array} { c c } { \displaystyle \end{array} } } \end{array} } } \end{array} } } \end{array} } } } \end{array} } } \end{array} \end{array} \end{array} \end{array} \end{array} \end{array} \end{array}$ $\widetilde { \mathbf { A } } _ { r } \big ( \widetilde { \mathbf { A } } _ { r } ^ { H } \widetilde { \mathbf { A } } _ { r } \big ) ^ { - 1 } \widetilde { \mathbf { A } } _ { r } ^ { H }$ and $\widetilde { { \bf P } } _ { \widetilde { { \bf A } } _ { r } , { \Lambda } } ^ { \perp } \ = \ \widetilde { { \bf P } } _ { \widetilde { { \bf A } } _ { r } } ^ { \perp }$ . As a result, the <sup>e e</sup>proposed GS detector of (50) reduces to the GS detector of (28) with $\lambda ^ { G S } = \lambda ^ { R S } = 2 { \cal M } | b | ^ { 2 } ( { \bf a } _ { r } ^ { H } { \bf P } _ { \tilde { \bf a } } ^ { \perp } { \bf a } _ { r } ) / \sigma ^ { 2 }$

<sup>e</sup>Corollary 4: From the probabilities of false alarm and detection of the clairvoyant in (26), RS in (29) and the proposed GS detectors in Theorem 1, the detection performance is in the order of

$$
P _ { D } ^ { R S } \leq P _ { D } ^ { G S } \leq P _ { D } ^ { C }\tag{56}
$$

for a given probability of false alarm.

Proof: It is first noted that, for a given probability of false alarm, the detection threshold γ holds the same for all three detectors. Then, from Corollary 2 and Corollary 3, we

$$
0 < \lambda ^ { R S } \leq \lambda ^ { G S } \leq \lambda ^ { C } ,\tag{57}
$$

when the diagonal elements of EINR matrix Λ is no smaller than 0 and finite. Finally, one realizes that the probability of detection or, equivalently, the Marcum Q-function $Q _ { 1 } ( { \sqrt { \lambda } } , { \sqrt { \gamma } } )$ of order 1 monotonically increases with respect to $\sqrt { \lambda }$ . As a result, the probabilities

Remark 1: The GS detector and the LCMV detector are equivalent when the interference statistics are perfectly known. This can be proved by showing $\mathbf { w } ^ { G S }$ in (49) is also the optimal solution of the LCMV beamforming optimization problem (32). However, the GS detector only needs to estimate EINRs for the interference Tx statistics, while the LCMV detector needs to estimate higher dimensional of unknowns in R .

Remark 2: When the interference statistics need to be estimated, the GS detector is more robust to the interference statistics estimation error compared to the LCMV detector, because the number of statistics to be estimated for the GS detector is much smaller. We will validate this property using simulation in the next section.

## V. PERFORMANCE EVALUATION

In this section, simulation results are provided to demonstrate the performance of the proposed GS detector under incoherent MIMO-FMCW mutual interference. We compare the proposed detector of (50) with

• Clairvoyant detector of (25),

• RS detector of (28) [3],

• LCMV detector of (33) [43],

in two simulation scenarios:

• Synthetic data: only the spatial-domain object and interference steering vectors are directly synthesized according to the model derived in Section II. More specifically, the object steering vector is generated according to (6), while the interference steering vector is directly generated using (16).

![](images/29ca3c6ba489d9b911bcc19daa195d1f03c5adf91ef59053f09dc0b71bf7a61b.jpg)  
(a)

![](images/c224a73a14f329cc9a0e20ac5ae70b8c09d54b61abd4b915990a6dcd3b7a9b60.jpg)  
(b)  
Fig. 5. Performance evaluation using synthetic data: Receiver operating characteristic (ROC) curves when $M = 4 , N = 4 ,$ and $\mathrm { S N R } = - 5$ dB in the presence of an object at $3 0 ^ { \circ }$ and two interferences at $4 0 ^ { \circ }$ and 10<sup>◦</sup>: (a) Comparison of theoretical (lines) and empirical Monte-Carlo (markers) ROC curves of the proposed GS detector when $\mathrm { I N R } { = \{ - 1 5 , - 1 0 , - 5 \} }$ dB; (b) Empirical Monte-Carlo comparison between the proposed GS detector and baseline methods under two levels of covariance matrix estimation errors.

• Realistic data: the received object and interference waveforms go through all necessary steps (LO, LPF, ADC, Rang/Doppler FFT, MIMO waveform separation) at the victim Rx of Fig. 3 with the help of the MATLAB Phased Array System Toolbox. The realistic data further accounts for Tx/Rx antenna beampatterns, waveform residuals due to the LPF and imperfect MIMO waveform separation due to the object Doppler modulation, and the noise contributed from spectrum leakage due to the presence of other objects and interferences.

## A. Performance Evaluation using Synthetic Data

We consider a victim MIMO-FMCW radar with M = 4 Tx antennas and $N = 4$ Rx antennas. The inter-element spacing values at the victim Rx and Tx are $d _ { r } = 0 . 5 \lambda$ and $d _ { t } = N d _ { r } ,$ respectively. We generate the spatial-domain object steering vector of (6) by feeding an object angle at $\phi _ { t } = \phi _ { r } = 3 0 ^ { \circ }$ to the object Tx and Rx steering vectors, respectively.

At the same time, we consider two mutually independent MIMO-FMCW interferences: one is located at 40<sup>◦</sup>, and the other at $1 0 ^ { \circ }$ as seen by the victim Rx. We first construct the interference Rx steering vector $\widetilde { \mathbf { a } } _ { r , q }$ according to (18) using the two interference angles. For the interference Tx steering vector, since it is incoherent and we have no prior knowledge about interference Tx, we generate it as a random M ×1 vector pointing to an unknown direction in the M-dim subspace

$$
\widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \sim \mathcal { C N } ( \mathbf { 0 } , \widetilde { \sigma } _ { q } ^ { 2 } \widetilde { \mathbf { R } } _ { t , q } ) .\tag{58}
$$

Note that the direct and random generation of $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ ignores the interference Tx configurations and relative geometry between the interference and victim Rx. It provides a simple and computationally efficient way to emulate the interference Tx steering vector in all possible configurations (FMCW/ array configurations and relative interference-victim geometry) and verify our theoretical performance analysis. In our simulation, we set $\widetilde { \mathbf { R } } _ { t , q } \triangleq [ \widetilde { R } _ { q , i , j } ] _ { i , j = 0 } ^ { M - 1 } = [ \rho _ { q } ^ { | i - j | } ] _ { i , j = 0 } ^ { M - 1 }$ with $\rho _ { 1 } = 0 . 6$ and $\rho _ { 2 } ~ = ~ 0 . 5$ for the two interferences. We define the SNR as $\mathrm { S N R } = | b | ^ { 2 } / \sigma ^ { 2 }$ and set it at −5 dB, while the INR is set as $\mathrm { I N R } = \dot { \widetilde { \sigma } } _ { q } ^ { 2 } / \dot { \sigma } ^ { 2 }$ dB, where $\sigma ^ { 2 }$ is the noise variance.

TABLE I  
VICTIM AND INTERFERING MIMO-FMCW RADAR CONFIGURATION FOR REALISTIC DATA GENERATION
<table><tr><td rowspan=1 colspan=1>Setup</td><td rowspan=1 colspan=1>Explanations</td></tr><tr><td rowspan=1 colspan=1>Simulation platform</td><td rowspan=1 colspan=1>MATLAB PhasedArray System Toolbox</td></tr><tr><td rowspan=1 colspan=1>RF wavelength</td><td rowspan=1 colspan=1>3.9 mm</td></tr><tr><td rowspan=1 colspan=1>Tx power (Rx noise figure)</td><td rowspan=1 colspan=1>5 dBm (4.5 dB)</td></tr><tr><td rowspan=1 colspan=1>Tx (Rx) antenna gain</td><td rowspan=1 colspan=1>36(42) dB</td></tr><tr><td rowspan=1 colspan=1>Tx (Rx) antenna element type</td><td rowspan=1 colspan=1>Backbaffled isotropic</td></tr><tr><td rowspan=1 colspan=1>Tx (Rx) array structure</td><td rowspan=1 colspan=1>Uniform linear array</td></tr><tr><td rowspan=1 colspan=1>MIMO Tx-pulse code</td><td rowspan=1 colspan=1>Chu sequence</td></tr><tr><td rowspan=1 colspan=1>Chirp bandwidth</td><td rowspan=1 colspan=1>460 MHz</td></tr><tr><td rowspan=1 colspan=1>IF bandwidth (ADC complex sample rate)</td><td rowspan=1 colspan=1>15 MHz (16.7 MHz)</td></tr><tr><td rowspan=1 colspan=1>Number of chirps in a CPI</td><td rowspan=1 colspan=1>256</td></tr><tr><td rowspan=1 colspan=1>Range, velocity, angle FFT sizes</td><td rowspan=1 colspan=1>1024, 256, 32</td></tr><tr><td rowspan=1 colspan=1>Object RCS model</td><td rowspan=1 colspan=1>Non-fluctuating</td></tr><tr><td rowspan=1 colspan=1>Object (interference) channel</td><td rowspan=1 colspan=1>Free-space two-way(one-way) channel</td></tr><tr><td rowspan=1 colspan=1>Victim radar chirp slope</td><td rowspan=1 colspan=1>15 MHz/us</td></tr><tr><td rowspan=1 colspan=1>Victim radar chirp (idle) duration</td><td rowspan=1 colspan=1>30.7 us (7 us)</td></tr><tr><td rowspan=1 colspan=1>Victim Tx (Rx) element spacing</td><td rowspan=1 colspan=1>15.6 mm (1.95 mm)</td></tr><tr><td rowspan=1 colspan=1>Victim Tx (Rx) antenna number</td><td rowspan=1 colspan=1>4 (8)</td></tr><tr><td rowspan=1 colspan=1>Interfering Tx element spacing</td><td rowspan=1 colspan=1>3.9 mm</td></tr><tr><td rowspan=1 colspan=1>Interfering Tx antenna number</td><td rowspan=1 colspan=1>8</td></tr></table>

The performance is evaluated in terms of the receiver operating characteristic (ROC) by using Monte Carlo trials. For each Monte-Carlo run, the interference Tx steering vector and noise are randomly generated as specified above, while the interference Rx steering vector and object Tx/Rx steering vectors are fixed according to the specified interference and object angles.

We can directly compute the detection statistics of the clairvoyant detector of (25) with the knowledge of $\widetilde { \mathbf { a } } _ { r , q }$ and $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ and the RS detector. On the other hand, the LCMV detector of (33) requires the knowledge of the normalized covariance matrix R . To mimic the covariance matrix estimation error due to the lack of homogeneous training data, we use the following perturbed interference Tx covariance matrix [49]

$$
\begin{array} { r } { \widetilde { \bf R } _ { t , q , e s t } = \widetilde \sigma _ { q } ^ { 2 } \widetilde { \bf R } _ { t , q } \odot ( { \bf 1 } _ { M } { \bf 1 } _ { M } ^ { H } + { \bf E } ) , } \end{array}\tag{59}
$$

where ${ \bf 1 } _ { M }$ is the all-one vector of dimension M , E is a M -by-M symmetric matrix and each entry in the upper triangular of E independently follows zero-mean Gaussian distribution with variance $\sigma _ { \mathrm { p e r t } } ^ { 2 }$ , and  is the Hadamard product. Consequently, the perturbed normalized covariance matrix of interferenceplus-noise used for the LCMV detector is given as

$$
\widetilde { \mathbf { R } } _ { e s t } = \sum _ { q = 1 } ^ { Q } \frac { \widetilde { \sigma } _ { q } ^ { 2 } } { \sigma ^ { 2 } } \widetilde { \mathbf { R } } _ { t , q , e s t } \otimes ( \widetilde { \mathbf { a } } _ { r , q } \widetilde { \mathbf { a } } _ { r , q } ^ { H } ) + \mathbf { I } _ { M N } .\tag{60}
$$

For a fair comparison, we also use the perturbed interference Tx covariance matrix for the estimation of $h _ { q } ^ { 2 }$ in (39) as

$$
h _ { q , e s t } ^ { 2 } = \frac { \mathbf { a } _ { t } ^ { H } \widetilde { \mathbf { R } } _ { t , q , e s t } \mathbf { a } _ { t } } { | | \mathbf { a } _ { t } | | ^ { 4 } } .\tag{61}
$$

Fig. 5 (a) verifies the derived theoretical performance (denoted by lines) in Theorem 1 of Section IV for the proposed GS detector and compares it with empirical ROC curves (denoted by markers) when the $\mathbf { I N R } = \{ - 1 5 , - 1 0 , - 5 \}$ dB. A good agreement between the theoretical and empirical ROC curves is observed in Fig. 5 (a). Second, when the INR decreases or, equivalently, the interference is weaker, the probability of detection increases for a given probability of a false alarm.

Fig. 5 (b) further compares the proposed GS detector with the three considered detectors in terms of ROC curves when INR is fixed to −10 dB. The clairvoyant detector, although not practical, gives the best detection performance among all detectors. Compared with our previously proposed RS detector, the proposed GS detector shows a significant improvement. For instance, when the probability of false alarm is 0.1, the probability detection is boosted from 0.2 of the RS detector to about 0.65 of the proposed GS detector. When the proposed GS detector is compared with the LCMV detector, we consider two levels of perturbation on the interference Tx covariance matrix in (59). Particularly, we consider $\sigma _ { \mathrm { p e r t } } ^ { 2 } = 0 . 5$ and $\sigma _ { \mathrm { p e r t } } ^ { 2 } ~ = ~ 1$ . When the relatively small perturbation is considered, i.e., $\sigma _ { \mathrm { p e r t } } ^ { 2 } ~ = ~ 0 . 5 .$ , the proposed GS detector is slightly better than the LCMV detector. When the perturbation is increased, the performance of the LCMV detector drops significantly and is even worse than the RS detector. On the other hand, the proposed GS detector maintains its detection performance under the perturbation on the interference Tx covariance matrix.

![](images/450f4afac2a24b1966b6328cc2f3a28b400f8df30119b8f1208d1be151be8eaf.jpg)  
Fig. 6. Comparison of angle-domain detection statistics of all considered detectors at a given range-Doppler bin.

TABLE IIOBJECTS AND INTERFERER SETUP.
<table><tr><td rowspan=1 colspan=1>Setup</td><td rowspan=1 colspan=1>Explanations</td></tr><tr><td rowspan=1 colspan=1>Objects&#x27;RCS</td><td rowspan=1 colspan=1>20dBsm</td></tr><tr><td rowspan=1 colspan=1>Object 1&#x27;s distance, velocity, angle</td><td rowspan=1 colspan=1> $\overline { { 3 5 . 5 ~ \mathrm { m } , ~ - 2 . 9 ~ \mathrm { m } / \mathrm { s } , ~ - 1 . 2 ^ { \circ } } }$ </td></tr><tr><td rowspan=1 colspan=1>Object 2&#x27;s distance, velocity, angle</td><td rowspan=1 colspan=1>81.0 m, 4.2 m/s, 11.2°</td></tr><tr><td rowspan=1 colspan=1>Interferer 1&#x27;s distance, velocity, angle</td><td rowspan=1 colspan=1>1.8 m, 1.3 m/s, −54.0°</td></tr><tr><td rowspan=1 colspan=1>Interferer 2&#x27;s distance, velocity, angle</td><td rowspan=1 colspan=1>2.3 m, −12.8 m/s, −48.1°</td></tr><tr><td rowspan=1 colspan=1>Interferer 1 (2)&#x27;s chirp slope</td><td rowspan=1 colspan=1>14.6 MHz/us (12.4 MHz/us)</td></tr><tr><td rowspan=1 colspan=1>Interferer 1 (2)&#x27;s chirp duration</td><td rowspan=1 colspan=1>31.6 us (37.2 us)</td></tr><tr><td rowspan=1 colspan=1>Interferer 1 (2)&#x27;s inter-chirp idle duration</td><td rowspan=1 colspan=1>7.5 us (7.3 us)</td></tr><tr><td rowspan=1 colspan=1>Initial time offset betweenvictim radar and interferer 1 (2)</td><td rowspan=1 colspan=1>20.8 us (17.6 us)</td></tr></table>

## B. Performance Evaluation using Realistic Data

In the above synthetic performance evaluation, the object and interference steering vectors were directly generated without considering the presence of Tx/Rx antenna beampatterns, and the presence of waveform residuals due to the LPF and waveform separation. In the following, we consider a systemlevel performance evaluation by generating the source FMCW-MIMO waveforms at both victim and interference Tx sides, accounting for antenna beampatterns, and including all steps at the victim Rx sides with the help of the MathWorks Phased Array System Toolbox. Particularly, in Table I, we specify the MIMO-FMCW radar configuration for both victim and interfering radar to synthesize the object and interference steering vectors.

We consider a scenario of 2 objects and 2 interfering radars in Table II. The detection statistics for all detectors are computed at the range bin of 517 and the Doppler bin of 128. Similar to the synthetic data case, the LCMV and proposed GS detectors require the estimation of the noise and interference statistics at the test range-Doppler bin. In this case, we adaptively estimate those statistics from neighboring range-Doppler bins. More specifically, we choose the range-Doppler bins in the range of $ \overrightarrow { \mathcal { L } } = \{ 5 1 9 , 5 1 5 \}$ and $\widetilde { K } = \{ 1 2 6 , 1 3 0 \}$ with a one-side guard interval of 2 bins. The implemented adaptive estimation steps are listed in Appendix D.

Fig. 6 shows qualitative detection statistics over the onedimensional angle at the specified range-Doppler bin. We also include a simple angular-domain FFT by ignoring the presence of mutual interference. It is seen that the interference-ignoring angle FFT yields strong sidelobes around the vicinity of the two interference angles at −48.1<sup>◦</sup> and, respectively, −54<sup>◦</sup>. All other detectors show interference mitigation capability at the two interference angles. The LCMV detector shows a relatively stronger sidelobe around these angles potentially due to the interference-plus-noise estimation error. The RS and proposed GS detectors show better interference mitigation at this region of interference angles, while the clairvoyant shows significantly fewer sidelobes over all angles.

![](images/38b745b6ff9146e0933b3f0f1e1dd2c95c8d6c9a47fc50b86d5f677c2a25bc06.jpg)  
(a) Angular spectrum

![](images/044c4a6d8fbf2ff4438dc40562deebb3b1de46aa6877a954b4597e4d623e0b76.jpg)  
(b) LCMV detector

![](images/4f0088e8b5ca2c310968867ded432a0125e80222548276a840f25e6f1f0bfc9f.jpg)  
(c) RS detector

![](images/3b84b5e8f17132d212181c71d1f7ac8cb8b815c709b9eb782192eb156f633d88.jpg)  
(d) Proposed GS detector

![](images/b4747464df40315bca85642372e7c9c2ae04315b6f8ff48cc11a5ec2912c98bc.jpg)  
(e) Clairvoyant detector  
Fig. 7. Qualitative detection heatmaps of the proposed detector and baseline detectors in a realistic dataset with 2 objects and 2 interferences. All heatmaps are shown over the range-angle domain at the Doppler bin of Object 1.

Fig. 7 show two-dimensional (2D) detection statistics of all detectors by varying both angle and range bins while fixing the Doppler bin at 128. In Fig. 7 (a) of the angle FFT, it is seen that the interference is a wideband signal over the range bins due to the resulting interference at the victim Rx is a chirp-like signal and, hence, it significantly raises the noise level over the detection statistics in the range-angle domain. On the other hand, the LCMV detector of Fig. 7 (b) shows an improved detection heatmap with smaller sidelobes, lower noise floors, and suppressed interferences around their angles. Stronger interference residuals show up at larger range values, e.g., larger than 100 m, around the angle of −50<sup>◦</sup>. Fig. 7 (c) and (d) show the 2D detection statistics of the RS and, respectively, the proposed GS detectors. They both show improved interference mitigation than the LCMV detector at larger distances. The proposed GS detector is further better than the RS detector at smaller distances, particularly on the range bin of Object 1. Finally, the clairvoyant detector of Fig. 7 (e) provides the best benchmark performance and cancels two interferences completely.

We further provide quantitative performance evaluation of all considered detection using the realistic data with the Monte-Carlo simulation of 1000 runs. For each Monte-Carlo run, we randomly select the interference angle in the interval of [−80<sup>◦</sup>, 80<sup>◦</sup>] and its range between 1 m and 3 m, while keeping other parameters the same as specified in Table II. With randomly selected interference angle and range, we compute the detection statistics at the true interference rangeangle bin and refer to it as output interference power (OIP). It is expected that the better the detection performance is, the lower the OIP at the true interference range-angle bin. Fig. 8 shows the cumulative distribution function (CDF) of the OIP of all detectors. It is seen that the proposed GS detector outperforms the RS and LCMV detectors with smaller output interference powers. For instance of the zoom-in window, at the 80th percentile of the CDF, the output interference powers of the RS and LCMV detectors are 2.5 dB and 4 dB higher than that of the proposed GS detector. In other words, the proposed GS detector has better mitigation capability with smaller sidelobes over the interference angles. The clairvoyant detector shows significantly smaller output interference power than the GS detector which implies further improvements are needed to reduce the performance gap.

## VI. CONCLUSION

We investigated mutual radar interference mitigation from incoherent MIMO-FMCW automotive radar. By deriving an explicit expression of the incoherent MIMO-FMCW interference that accounts for FMCW incoherence as well as MIMO array differences, we formulated the mutual interference mitigation as a spatial-domain object detection under Kronecker structured interference. Compared with existing spatial-domain detectors, e.g., the LCMV and RS detectors, we proposed a GS detector that exploits the structure of both transmit and receiver steering vectors of the incoherent interference and proved that it is a CFAR detector. Both analytical and empirical performance evaluations using directly generated synthetic data and realistic data with the help of the phased array toolbox confirmed the performance improvements in terms of detection performance and output interference power.

![](images/48bea2deeec391e0f469ed312bfd46f662318528b6cd6fe451f124c55d711f79.jpg)  
Fig. 8. CDF of output interference power at the true interference range-angle bin over 1000 Monte-Carlo runs with a realistic setting.

## APPENDIX A DERIVATION OF OBJECT SIGNAL MODEL

In the following, we show the detaied derivation of the object signal model following the steps in the upper right of Fig. 3.

Local Oscillator (LO): At the n-th Rx antenna of the victim radar, the backscattered object signal α $\textstyle \langle \sum _ { m = 0 } ^ { M - 1 } s _ { m } ( t - \tau _ { m , n } ( t ) )$ is mixed with the conjugate of the LO signal $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } s ^ { * } ( t - } \end{array}$ $k T _ { \mathrm { P R I } } ) e ^ { - j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } ) }$ , leading to the dechirped baseband analog signal

$$
\begin{array} { r l r } {  { a _ { n } ^ { s } ( t ) = \alpha _ { \tau } \sum _ { m = 0 } ^ { M - 1 } e ^ { - j 2 \pi f _ { c } \frac { 2 v t } { c } } e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } } } \\ & { } & { \times \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } e ^ { - j 2 \pi \beta ( t - k T _ { \mathrm { P R I } } ) \tau } D _ { \tau , T } ( t - k T _ { \mathrm { P R I } } ) , } \end{array}\tag{62}
$$

where $\alpha _ { \tau } \triangleq \alpha e ^ { - j 2 \pi f _ { c } \tau } e ^ { j \pi \beta \tau ^ { 2 } }$ with α denoting the complex object amplitude, $f _ { \phi _ { t } } = d _ { t } \mathrm { s i n } ( \phi _ { t } ) / \lambda$ and $f _ { \phi _ { r } } = d _ { r } \mathrm { s i n } ( \phi _ { r } ) / \lambda$ are the Tx and Rx normalized spatial frequencies at wavelength $\lambda = c / f _ { c } ,$ and $\tau = 2 R / c$ is the round-trip propagation delay at the 0-th Rx antenna (reference antenna).

Analog-to-Digital Converter (ADC) and Low-Pass Filter (LPF): Suppose the object beat frequency βτ is smaller than the cutoff frequency $f _ { L }$ of the anti-aliasing LPF. By passing $a _ { n } ^ { s } ( t )$ into the LPF and sampling it at $t = k T _ { \mathrm { P R I } } + l \Delta T$ with $\Delta T$ denoting the fast-time interval, we have the sampled object signal on fast-time sample l and pulse k, i.e.,

$$
\begin{array} { r l } & { a _ { n } ^ { s } ( l , k ) = \alpha _ { \tau } e ^ { - j 2 \pi f _ { r } l } \mathbf { 1 } [ l \in \mathcal { L } ^ { s } ] } \\ & { \quad \quad \times \displaystyle \sum _ { m = 0 } ^ { M - 1 } c _ { k , m } e ^ { - j 2 \pi ( f _ { d } k + f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } , } \end{array}\tag{63}
$$

where $\mathcal { L } ^ { s } \triangleq \{ \lceil \tau / \Delta T \rceil , \dots , \lfloor T / \Delta T \rfloor \}$ is the set of integer sample indices, $f _ { r } \triangleq ( \beta \tau + 2 v / \lambda ) \Delta T$ is the normalized range frequency, and $f _ { d } \triangleq 2 f _ { c } T _ { \mathrm { P R I } } \dot { v } / c$ is the normalized Doppler frequency.

Fast-Time/Range FFT: Applying the L-length fast-time fast Fourier transform (FFT) or range FFT to $a _ { n } ^ { s } ( l , k )$ , we can obtain the range-domain spectrum as

$$
x _ { n } ^ { s } ( l ^ { \prime } , k ) = \alpha _ { l ^ { \prime } } \sum _ { m = 0 } ^ { M - 1 } c _ { k , m } e ^ { - j 2 \pi f _ { d } k } e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } ,\tag{64}
$$

where $\begin{array} { r } { \alpha _ { l ^ { \prime } } \triangleq \sum _ { l = 0 } ^ { L - 1 } \alpha _ { \tau } { \bf 1 } [ l \in \mathcal { L } ^ { s } ] e ^ { - j 2 \pi ( f _ { r } + l ^ { \prime } / L ) l } } \end{array}$ is the complex amplitude of the object on range bin l<sup>0</sup>.

Slow-Time/Doppler FFT and Waveform Separation: From (64), each Rx antenna combines the M coded transmitting waveforms via the weighted summation. To separate $x _ { n } ^ { s } ( l ^ { \prime } , k )$ into object signals from M Tx signals, a slow-time MIMO decoding is applied. To obtain the signal from m-th Tx antenna, the complex conjugate of the code sequence $c _ { k , m } ^ { * } , k = 0 , 1 , \ldots , K - 1$ are multiplied on the range-domain response over K slow-time pulses. For a MIMO code sequence with orthogonal property $\begin{array} { r } { \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m } ^ { * } \ = \ K , \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m ^ { \prime } } ^ { * } \ = \ 0 , \forall \ m ^ { \prime } \ \ne \ m , } \end{array}$ summing the decoded signal over K pulses $\begin{array} { r l } { } & { { } \sum _ { k = 0 } ^ { K - 1 } \bar { x _ { n } ^ { s } } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } } \end{array}$ can well reconstruct the object signal with zero Doppler from m-th Tx antenna. For a general case where the slow-time phase is shifted by the non-zero object Doppler, the Doppler needs to be compensated. To reconstruct the object signal from the m-th Tx antenna, we can compensate the Doppler using a slow-time FFT (Doppler FFT) on the slow-time decoded signal $x _ { n } ^ { s } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } , k = 0 , 1 , . . . , K - 1 ;$

$$
\begin{array} { l } { { y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) = \displaystyle \sum _ { k = 0 } ^ { K - 1 } x _ { n } ^ { s } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } e ^ { - j 2 \pi \frac { k ^ { \prime } } { K } k } ~ ( } } \\ { { = } b ( l ^ { \prime } , k ^ { \prime } ) e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } + y _ { m , n } ^ { r } ( l ^ { \prime } , k ^ { \prime } ) , }  \end{array}\tag{65}
$$

where $\begin{array} { r } { b ( l ^ { \prime } , k ^ { \prime } ) \triangleq \alpha _ { l ^ { \prime } } \sum _ { k = 0 } ^ { K - 1 } e ^ { - j 2 \pi ( f _ { d } + \frac { k ^ { \prime } } { K } ) k } } \end{array}$ is the amplitude of the object signal from the m-th Tx antenna, and

$$
\begin{array} { r } { y _ { m , n } ^ { r } ( l ^ { \prime } , k ^ { \prime } ) = \alpha _ { l ^ { \prime } } \displaystyle \sum _ { m ^ { \prime } \neq m } \left( \displaystyle \sum _ { k = 0 } ^ { K - 1 } c _ { k , m ^ { \prime } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( f _ { d } + \frac { k ^ { \prime } } { K } ) k } \right) } \\ { \times e ^ { - j 2 \pi ( f _ { \phi _ { t } } m ^ { \prime } + f _ { \phi _ { r } } n ) } , \qquad ( 6 \pi ^ { \prime } ) } \end{array}\tag{66}
$$

is the waveform separation residual from other Tx antennas. At the Doppler bin $k ^ { \prime }$ closest to the object Doppler frequency $f _ { d } ,$ i.e., $f _ { d } { + } k ^ { \prime } / K \approx 0$ , the amplitude $b ( l ^ { \prime } , k ^ { \prime } ) \approx K \alpha _ { l ^ { \prime } }$ approaches to a coherent gain of K due to the Doppler FFT in (65). Using the near-orthogonality of MIMO codes [13]

$$
\operatorname* { m a x } _ { f } \left. \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m ^ { \prime } } ^ { * } e ^ { - j 2 \pi f k } \right. \ll K , \forall \ m ^ { \prime } \neq m ,\tag{67}
$$

the waveform separation residual in (65) can be ignored. It is worthy noting that object detection under imperfect waveform separation for MIMO radar has been considered in [9] and [50].

![](images/bed04d981cb65f38b7f9c6c6ec1a0ebfc8e2ff2f3bb1925e4d3d94267b5d40de.jpg)  
Fig. 9. Two necessary conditions for the $\widetilde { k } { - } \mathrm { t h }$ pulse of the interfering radar to be dechirped by the k-th pulse of the victim radar with a counterexample for each condition shown in the figure.

## APPENDIX BDERIVATION OF INTERFERENCE SIGNAL MODEL

Two necessary conditions for the $\widetilde { k } { - } \mathrm { t h }$ pulse of the interfering radar be dechirped by the k-th pulse of victim radar are $- \overline { { \widetilde { \tau } } } _ { k , \widetilde { k } } ^ { \prime } - \widetilde { T } _ { \mathrm { P R I } } < 0$ and $\tilde { \tau } _ { k , \tilde { k } } ^ { \prime } < T _ { \mathrm { P R I } }$ , which in combination lead to $- \widetilde { T } _ { \mathrm { P R I } } < \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } < \widetilde { \tau }$ T<sub>PRI</sub>. If any of these two conditions does not satisfy, as shown in Fig. 9, the k-th pulse of the interfering radar cannot be dechirped by the k-th pulse of victim radar.

Define

$$
\begin{array} { r l r } & { } & { \mathcal { K } _ { \widetilde { k } } \triangleq \Big \{ k : \widetilde { k } \widetilde { T } _ { \mathrm { P R I } } + \widetilde { \tau } _ { s y n } = k T _ { \mathrm { P R I } } + \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } , - \widetilde { T } _ { \mathrm { P R I } } < \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } < T _ { \mathrm { P R I } } , } \\ & { } & { k = 0 , 1 , \ldots , K - 1 \Big \} , ~ \widetilde { k } = 0 , 1 , \ldots , \widetilde { K } - 1 , \qquad ( 6 8 ) } \end{array}
$$

as a set that groups all pulses of the victim radar that intercept with the <sup>˜</sup>k pulse by checking whether any time instant of the victim pulse falls within the <sup>˜</sup>k interfering pulse. Denote the slow-time code of the interfering radar observed at k-th victim radar pulse as

$$
\begin{array} { r } { \widehat { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } \triangleq \left\{ \begin{array} { l l } { \widetilde { c } _ { \widetilde { k } , \widetilde { m } } , } & { k \in { \mathcal { K } } _ { \widetilde { k } } } \\ { 0 , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. } \end{array}\tag{69}
$$

Then, we rewrite $s _ { n } ^ { i } ( t )$ as

$$
\begin{array} { r l } & { s _ { n } ^ { i } ( t ) = \widetilde { \alpha } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } } \displaystyle \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \displaystyle \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \displaystyle \sum _ { k \in { \widetilde { K } _ { \widetilde { k } } } } \widetilde { c } _ { k , \widetilde { m } } ^ { \widetilde { k } } \widetilde { s } ( t - k T _ { \mathrm { P R I } } - \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } - \widetilde { \tau } ) } \\ & { \times \ e ^ { j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } - \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } ) } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } e ^ { - j 2 \pi f _ { c } \frac { \widetilde { v } t } { c } } . \qquad ( 7 0 ) } \end{array}
$$

The victim radar mixes $s _ { n } ^ { i } ( t )$ with its LO signal, and obtains

![](images/f2c99fedca21037f8b070fb826f99a5ae8bf89dde0f9d34a5c319b5dddcc081e.jpg)  
Fig. 10. Interference at victim radar’s pulse k.

the analog beat signal from the n-th Rx antenna

$$
\begin{array} { r l } & { a _ { n } ^ { i } ( t ) = s _ { n } ^ { i } ( t ) \displaystyle \sum _ { k = 0 } ^ { K - 1 } s ^ { * } ( t - k T _ { \mathrm { P R } } ) e ^ { - j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R } } ) } } \\ & { = \widetilde { \alpha } e ^ { - j 2 \pi f _ { c } \pi } \displaystyle \sum _ { \widetilde m = 0 } ^ { \widetilde M - 1 } \displaystyle \sum _ { \widetilde k = 0 } ^ { K - 1 } \displaystyle \sum _ { k \in \widetilde K _ { \widetilde { k } , \widetilde m } } \widetilde c _ { k , \widetilde m } ^ { k } e ^ { j \pi ( \widetilde \beta - \beta ) ( t - k T _ { \mathrm { P R } } ) / 2 } } \\ & { \quad \times \ e ^ { j \pi \widetilde \beta ( \widetilde \gamma _ { c , \widetilde { k } } ^ { i } + \widetilde \gamma ) ^ { 2 } } e ^ { - j 2 \pi \widetilde \beta ( t - k T _ { \widetilde { k } \widetilde { k } } ) ( \widetilde \gamma _ { c , \widetilde { k } } ^ { i } + \widetilde \gamma ) } } \\ & { \quad \times \ e ^ { - j 2 \pi f _ { c } \widetilde \gamma _ { c , \widetilde { k } } ^ { i } } e ^ { - j 2 \pi ( \widetilde \gamma _ { c , \widetilde { m } } + \widetilde \gamma _ { \widetilde { c } , \widetilde { m } } ) } e ^ { - j 2 \pi f _ { c } \frac { \widetilde \gamma _ { c } ^ { i } } { c } } } \\ & { \quad \times \ D _ { \widetilde { \gamma } _ { c , \widetilde { k } } ^ { i } + \widetilde \gamma , \widetilde { m } \operatorname* { i n } } \{ T _ { \widetilde { c } _ { k , \widetilde { k } } ^ { i } + \widetilde \gamma } ^ { \pi } \} ( t - k T _ { \mathrm { P R } } ) . } \end{array}\tag{71}
$$

From (71), we can see that the instantaneous frequency of interference at pulse k is $\widetilde { \beta } ( \widetilde { \tau } _ { k . \widetilde { k } } ^ { \prime } { + \widetilde { \tau } } )  - ( \widetilde { \beta } { - \beta } ) ( t { - \} T _ { \mathrm { P R I } } ^ { \mathrm { ~ } } ) }$ . Then, passing $a _ { n } ^ { i } ( t )$ into the LPF of bandwidth $f _ { L }$ , the interference residential time on pulse k with interference is

$$
0 < \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) - ( \widetilde { \beta } - \beta ) ( t - k T _ { \mathrm { P R I } } ) < f _ { L } .\tag{72}
$$

Fig. 10 provides an illustrative example showing the interference residential time. The low-pass filtered IF interference signal is

$$
\begin{array} { l } { { \displaystyle a _ { n } ^ { i , l o w } ( t ) = \widetilde { \alpha } e ^ { - j 2 \pi f _ { c } \widetilde { \tau } } \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \sum _ { \widetilde { k } \widetilde { k } } \widetilde { c } _ { \widetilde { k } , \widetilde { m } } ^ { \widetilde { k } } e ^ { j \pi ( \widetilde { \beta } - \beta ) ( t - k T _ { \mathrm { P M } } ) ^ { 2 } } } } \\ { { \displaystyle \qquad \widetilde { m } = 0 \widetilde { \gamma } \widetilde { \tau } - \sum _ { \widetilde { k } \widetilde { k } } \widetilde { c } _ { \widetilde { k } } \widetilde { c } _ { \widetilde { k } } \widetilde { c } _ { \widetilde { k } } } } \\ { { \displaystyle \qquad \times e ^ { j \pi \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) ^ { 2 } } e ^ { - j 2 \pi \widetilde { \beta } ( t - k T _ { \mathrm { P M } } ) ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) } } } \\ { { \displaystyle \qquad \times e ^ { - j 2 \pi f _ { c } \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } } e ^ { - j 2 \pi ( \widetilde { f } _ { \widetilde { \phi } _ { t } } \widetilde { m } + \widetilde { f } _ { \widetilde { \phi } _ { r } } n ) } e ^ { - j 2 \pi f _ { c } \frac { \widetilde { \tau } _ { c } } { c } } } } \\ { { \displaystyle \qquad \times \ 1 \left[ 0 < \widetilde { \beta } ( \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } ) - ( \widetilde { \beta } - \beta ) ( t - k T _ { \mathrm { P H } } ) < f _ { L } \right] } } \\   \displaystyle \qquad \times \ D _ { \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde { \tau } , \operatorname* { m i n } } \Big \{ T _  \widetilde { \tau } _ { k , \widetilde { k } } ^ { \prime } + \widetilde  \end{array}
$$

APPENDIX C PROOF OF THEOREM 1

The following derivation is based on the form $T ^ { G S } ( \mathbf { y } ) =$ $\frac { 2 } { { \sigma } ^ { 2 } } \frac { \left. \left( \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right) ^ { H } \mathbf { y } \right. ^ { 2 } } { \left. \left. \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right. \right. ^ { 2 } }$ suggested by $\mathbf { w } ^ { G S }$ in (49).

Under $H _ { 0 } ,$ , we have $( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \mathbf { y } = ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \widetilde { \mathbf { z } } ,$ using the last condition in (44). As $\widetilde { \mathbf z } \sim \mathcal { C N } ( \mathbf 0 , \sigma ^ { 2 } \mathbf R )$ by (41),

we have $( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { R } ^ { - 1 } \mathbf { y } \sim { \mathcal { C N } } \left( \mathbf { 0 } , \sigma ^ { 2 } \Big | \Big | \mathbf { R } ^ { - \frac { 1 } { 2 } } \big ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \big ) \Big | \Big | ^ { 2 } \right)$ Thus, $T ^ { G S } ( \mathbf { y } )$ under $H _ { 0 }$ follows chi-squared distribution with 2 degrees of freedom (DoF), i.e.,

$$
T ^ { G S } ( { \bf y } ) \sim \chi _ { 2 } ^ { 2 } , \ \mathrm { u n d e r } \ H _ { 0 } .\tag{74}
$$

Under $H _ { 1 }$ , we have $\begin{array} { r l r } { ( { \bf a } _ { t } } & { { } \otimes } & { { \bf a } _ { r } ) ^ { H } { \bf R } ^ { - 1 } { \bf y } } \end{array}$ ∼ $\mathcal { C N } ( b \Big | \Big | \mathbf { R } ^ { - \frac { 1 } { 2 } } \big ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \big ) \Big | | ^ { 2 } , \sigma ^ { 2 } \Big | \Big | \mathbf { R } ^ { - \frac { 1 } { 2 } } \big ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \big ) \Big | \Big | ^ { 2 } )$ Thus, $T ^ { G S } ( \mathbf { y } )$ under $H _ { 1 }$ follows noncentral chi-squared distribution with 2 DoF and noncentrality parameter $\lambda ^ { \bar { G } S }$ , i.e.,

$$
T ^ { G S } ( { \bf y } ) \sim { \chi ^ { \prime } } _ { 2 } ^ { 2 } ( \lambda ^ { G S } ) , \ \mathrm { u n d e r \ } H _ { 1 } ,\tag{75}
$$

where $\begin{array} { r } { \lambda ^ { G S } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } \Big | \Big | { \bf R } ^ { - \frac { 1 } { 2 } } \big ( { \bf a } _ { t } \otimes { \bf a } _ { r } \big ) \Big | \Big | ^ { 2 } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } M { \bf a } _ { r } ^ { H } \widetilde { \bf P } _ { \tilde { \bf A } _ { r } , \Lambda } ^ { \perp } { \bf a } _ { r } } \end{array}$ By $\begin{array} { r l r } { P _ { F A } ^ { G S } } & { { } = } & { \mathrm { P r } [ T ^ { G S } ( \mathbf { y } ) \geq \stackrel {  } { \gamma } | H _ { 0 } ] } \end{array}$ and $P _ { D } ^ { \dot { G } \dot { S } ^ { \cdots } } =$ Pr $\left[ T ^ { G S } ( \mathbf { y } ) \geq \gamma | H _ { 1 } \right]$ , we have (53).

## APPENDIX D

## ADAPTIVE ESTIMATION OF INTERFERENCE AND NOISESTATISTICS IN THE CASE OF REALISTIC DATA

Similar to the synthetic data case, the LCMV and GS detectors need the interference-plus-noise covariance matrix and, particularly, the interference Tx covariance matrix to compute the detection statistics. Unlike the synthetic data case, we do not have the access to the true interference covariance and, hence, its perturbation. As a result, we need to adaptive estimate the interference-plus-noise covariance matrix or, equivalently, $h _ { q } ^ { 2 } , \widetilde { \sigma } _ { q } ^ { 2 } \widetilde { \mathbf { R } } _ { t , q }$ and $\scriptstyle { \dot { \sigma } } ^ { 2 }$ , from neighboring range-Doppler bins.

At an object-free range-Doppler bin $( l ^ { \prime } , k ^ { \prime } )$ of the victim radar, the received spatial-domain signal is $\mathbf { y } ( l ^ { \prime } , k ^ { \prime } ) =$ $\begin{array} { r } { \sum _ { q = 1 } ^ { Q } \widetilde { \mathbf { a } } _ { t , q } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r , q } + \mathbf { z } } \end{array}$ . The noise power $\sigma ^ { 2 }$ at the same range-Doppler bin can be estimated as

$$
\widehat { \sigma } ^ { 2 } ( l ^ { \prime } , k ^ { \prime } ) = \frac { 2 } { M ( N - Q ) } | | ( { \bf I } _ { M } \otimes { \bf P } _ { \tilde { \mathbf { A } } _ { r } } ^ { \perp } ) { \bf y } ( l ^ { \prime } , k ^ { \prime } ) | | ^ { 2 } ,\tag{76}
$$

the $q \mathrm { - t h }$ interference Tx steering vector $\widetilde { \mathbf { a } } _ { t , q } ^ { \prime }$ can be estimated as

$$
\widehat { \mathbf { a } } _ { t , q } ^ { \prime } ( l ^ { \prime } , k ^ { \prime } ) = \left( \mathbf { I } _ { M } \otimes ( \widetilde { \mathbf { A } } _ { r } \mathbf { b } _ { q } ) ^ { H } \right) \mathbf { y } ( l ^ { \prime } , k ^ { \prime } ) ,\tag{77}
$$

where ${ \mathbf { b } } _ { q }$ is the $q \mathrm { . }$ -th column of $( \widetilde { \mathbf { A } } _ { r } ^ { H } \widetilde { \mathbf { A } } _ { r } ) ^ { - 1 }$ , and $\widetilde { b } _ { q }$ can be estimated as

$$
\widehat { b } _ { q } ( l ^ { \prime } , k ^ { \prime } ) = \frac { \mathbf { a } _ { t } ^ { H } \widehat { \mathbf { a } } _ { t , q } ^ { \prime } ( l ^ { \prime } , k ^ { \prime } ) } { | | \mathbf { a } _ { t } | | ^ { 2 } } .\tag{78}
$$

As a result, by collecting a set of range-Doppler bins, e.g., $\widetilde { \mathcal { L } }$ and $\tilde { \kappa }$ , we can average out the noise power estimate as

$$
\widehat { \sigma } ^ { 2 } = \frac { 1 } { | \widetilde { \mathcal { L } } | | \widetilde { \mathcal { K } } | } \sum _ { l ^ { \prime } \in \widetilde { \mathcal { L } } , k ^ { \prime } \in \widetilde { \mathcal { K } } } \widehat { \sigma } ^ { 2 } ( l ^ { \prime } , k ^ { \prime } ) .\tag{79}
$$

In a similar fashion,, we have

$$
\widehat { h } _ { q } ^ { 2 } = \frac { 1 } { | \widetilde { \mathcal { L } } | | \widetilde { \mathcal { K } } | } \sum _ { l ^ { \prime } \in \widetilde { \mathcal { L } } , k ^ { \prime } \in \widetilde { \mathcal { K } } } | \widehat { b } _ { q } ( l ^ { \prime } , k ^ { \prime } ) | ^ { 2 } ,\tag{80}
$$

and

$$
\widehat { \mathbf { R } } _ { t , q } = \frac { 1 } { | \widetilde { \mathcal { L } } | | \widetilde { \mathcal { K } } | } \sum _ { l ^ { \prime } \in \widetilde { \mathcal { L } } , k ^ { \prime } \in \widetilde { \mathcal { K } } } \widehat { \mathbf { a } } _ { t , q } ^ { \prime } ( l ^ { \prime } , k ^ { \prime } ) \widehat { \mathbf { a } } _ { t , q } ^ { \prime H } ( l ^ { \prime } , k ^ { \prime } ) .\tag{81}
$$

## REFERENCES

[1] S. Jin, P. Wang, P. Boufounos, R. Takahashi, and S. Roy, “Spatial-domain object detection under MIMO-FMCW automotive radar interference,” in 2023 IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP), 2023.

[2] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 45–59, 2019.

[3] S. Jin, P. Wang, P. Boufounos, P. V. Orlik, R. Takahashi, and S. Roy, “Spatial-domain interference mitigation for slow-time MIMO-FMCW automotive radar,” in 2022 IEEE 12th Sensor Array and Multichannel Signal Processing Workshop (SAM), 2022, pp. 311–315.

[4] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 22–35, 2017.

[5] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 20–31, 2019.

[6] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 32–44, 2019.

[7] P. Wang, D. Millar, K. Parsons, and P. V. Orlik, “Nonlinearity correction for range estimation in FMCW millimeter-wave automotive radar,” in IWS, 2018, pp. 1–3.

[8] P. Wang, D. Millar, K. Parsons, R. Ma, and P. V. Orlik, “Range accuracy analysis for FMCW systems with source nonlinearity,” in ICMIM, 2019, pp. 1–5.

[9] P. Wang, P. Boufounos, H. Mansour, and P. V. Orlik, “Slow-time MIMO-FMCW automotive radar detection with imperfect waveform separation,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 8634–8638.

[10] M. Sheeny, E. De Pellegrin, S. Mukherjee, A. Ahrabian, S. Wang, and A. Wallace, “RADIATE: A radar dataset for automotive perception,” arXiv preprint arXiv:2010.09076, 2020.

[11] M. Mostajabi, C. M. Wang, D. Ranjan, and G. Hsyu, “High resolution radar dataset for semi-supervised learning of dynamic objects,” in CVPR Workshops), 2020, pp. 450–457.

[12] S. Rao, “Introduction to mmWave sensing: FMCW radars,” Texas Instruments (TI) mmWave Training Series, 2017.

[13] S. Sun, A. P. Petropulu, and H. V. Poor, “MIMO radar for advanced driver-assistance systems and autonomous driving: Advantages and challenges,” IEEE Signal Processing Magazine, vol. 37, no. 4, pp. 98– 117, 2020.

[14] S. Rao, “White paper: MIMO radar,” Texas Instruments (TI) Technical Report SWRA554A, 2017.

[15] A. Och, C. Pfeffer, J. Schrattenecker, S. Schuster, and R. Weigel, “A scalable 77 GHz massive MIMO FMCW radar by cascading fullyintegrated transceivers,” in 2018 Asia-Pacific Microwave Conference (APMC), 2018, pp. 1235–1237.

[16] M. Barjenbruch et al., “A method for interference cancellation in automotive radar,” in 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), 2015, pp. 1–4.

[17] J. Wang, “CFAR-based interference mitigation for fmcw automotive radar systems,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–10, 2021.

[18] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the stft domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, 2019.

[19] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in 2017 European Radar Conference (EURAD), 2017, pp. 90–93.

[20] A. Correas-Serrano and M. A. Gonzalez-Huici, “Sparse reconstruction of chirplets for automotive fmcw radar interference mitigation,” in 2019 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), 2019, pp. 1–4.

[21] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[22] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in 2018 IEEE Radar Conference (RadarConf18), 2018, pp. 0405–0410.

[23] S. Jin, P. Wang, P. Boufounos, P. Orlik, and S. Roy, “Automotive radar interference mitigation with fast-time-frequency mode retrieval,” in 2022 IEEE Radar Conference (RadarConf22), 2022, pp. 1–6.

[24] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall), 2020, pp. 1–5.

[25] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for FMCW radars,” arXiv:2108.13023, 2021.

[26] S. Jin and S. Roy, “FMCW radar network: Multiple access and interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 968–979, 2021.

[27] F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, and M. Gashinova, “Automotive radar waveform parameters randomisation for interference level reduction,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–5.

[28] M. Wagner et al., “Threshold-free interference cancellation method for automotive FMCW radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS), 2018, pp. 1–4.

[29] S. Chen, W. Shangguan, J. Taghia, U. Kuhnau, and R. Martin, “Auto-¨ motive radar interference mitigation based on a generative adversarial network,” in 2020 IEEE Asia-Pacific Microwave Conference (APMC), 2020, pp. 728–730.

[30] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR), 2020, pp. 315–320.

[31] C. Jiang, T. Chen, and B. Yang, “Adversarial interference mitigation for automotive radar,” in 2021 IEEE Radar Conference (RadarConf21), 2021, pp. 1–6.

[32] A. Dubey, J. Fuchs, V. Madhavan, M. Lubke, R. Weigel, and F. Lurz,¨ “Region based single-stage interference mitigation and target detection,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–5.

[33] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 927–940, 2021.

[34] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Transactions on Intelligent Transportation Systems, vol. 22, no. 1, pp. 416–429, 2021.

[35] K. U. Mazher, R. W. Heath, K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–6.

[36] A. Bose, B. Tang, M. Soltanalian, and J. Li, “Mutual interference mitigation for multiple connected automotive radar systems,” IEEE Transactions on Vehicular Technology, vol. 70, no. 10, pp. 11 062– 11 066, 2021.

[37] C. Fischer, M. Goppelt, H.-L. Blocher, and J. Dickmann, “Minimizing¨ interference in automotive radar using digital beamforming,” Advances in Radio Science, vol. 9, pp. 45–48, 2011.

[38] J. Bechter, A. Demirlika, P. Hugler, F. Roos, and C. Waldschmidt, “Blind¨ adaptive beamforming for automotive radar interference suppression,” in 2018 19th International Radar Symposium (IRS), 2018, pp. 1–10.

[39] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in 2018 IEEE Radar Conference (RadarConf18), 2018, pp. 0252–0256.

[40] ——, “Experimental evaluation of adaptive beamforming for automotive radar interference suppression,” in 2020 IEEE Radio and Wireless Symposium (RWS), 2020, pp. 183–186.

[41] T. Pernstal, J. Degerman, H. Brostr˚ om, V. T. Vu, and M. I. Pettersson,¨ “GIP test for automotive FMCW interference detection and suppression,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–6.

[42] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Transactions on Microwave Theory and Techniques, vol. 65, no. 5, pp. 1727–1734, 2017.

[43] A. Pirkani, F. Norouzian, E. Hoare, M. Chemiakov, and M. Gashinova, “Automotive interference suppression in MIMO and phased array radar,” in 2021 18th European Radar Conference (EuRAD), 2022, pp. 413–416.

[44] Y. Sun, A. Baricz, and S. Zhou, “On the monotonicity, log-concavity, and tight bounds of the generalized marcum and nuttall q-functions,” IEEE Transactions on Information Theory, vol. 56, no. 3, pp. 1166– 1186, 2010.

[45] R. Feger, H. Haderer, and A. Stelzer, “Optimization of codes and weighting functions for binary phase-coded FMCW MIMO radars,” in 2016 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), 2016, pp. 1–4.

[46] B. Friedlander, “On signal models for MIMO radar,” IEEE Transactions on Aerospace and Electronic Systems, vol. 48, no. 4, pp. 3655–3660, 2012.

[47] J. Li and P. Stoica, “MIMO radar with colocated antennas,” IEEE Signal Processing Magazine, vol. 24, no. 5, pp. 106–114, 2007.

[48] H. L. Van Trees, Optimum array processing: Part IV of detection, estimation, and modulation theory. John Wiley & Sons, 2004.

[49] P. Stoica, J. Li, X. Zhu, and J. R. Guerci, “On using a priori knowledge in space-time adaptive processing,” IEEE Transactions on Signal Processing, vol. 56, no. 6, pp. 2598–2602, 2008.

[50] P. Wang and H. Li, “Target detection with imperfect waveform separation in distributed MIMO radar,” IEEE Transactions on Signal Processing, vol. 68, pp. 793–807, 2020.