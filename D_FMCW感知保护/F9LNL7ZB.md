# SPATIAL-DOMAIN INTERFERENCE MITIGATION FOR SLOW-TIME MIMO-FMCW AUTOMOTIVE RADAR

Sian Jin<sup>†∗</sup>, Pu Wang<sup>†</sup>, Petros Boufounos<sup>†</sup>, Philip V. Orlik<sup>†</sup>, Ryuhei Takahashi<sup>⋆</sup>, and Sumit Roy<sup>+</sup>

<sup>†</sup>Mitsubishi Electric Research Laboratories (MERL), Cambridge, MA 02139, USA <sup>⋆</sup>Mitsubishi Electric Information Technology R&D Center, Ofuna, Kamakura City, 247-8501, Japan <sup>+</sup>University of Washington, Seattle, WA 98195, USA

## ABSTRACT

This paper considers mutual interference mitigation among automotive radars using frequency modulated continuous wave (FMCW) for the signaling scheme and multiple-input multiple-output (MIMO) for achieving a virtual array. For the first time, we derive a general interference signal model that fully accounts for not only the time-frequency incoherence, but also the slow-time code incoherence. Together with a standard MIMO-FMCW object signal model, we formulate the interference mitigation as a spatial-domain detection problem and propose a generalized likelihood ratio test (GLRT) detector. Moreover, we derive the exact theoretical performance of the proposed GLRT detector, proving that it is a constant false alarm rate (CFAR) detector against MIMO-FMCW mutual interference. Preliminary numerical results confirm the performance of our proposed detector and show advantages to baseline detectors.

Index Terms— Automotive radar, MIMO, Interference.

## 1. INTRODUCTION

Automotive radars are important for detecting the range, velocity and angles of various nearby objects (e.g., cars). For realizing lowcost design, current automotive radar chips widely adopt the frequency modulated continuous wave (FMCW) since it enables receivers with low sampling rates determined by the instantaneous frequency (IF) bandwidth [1–9]. For achieving high angular resolution, these chips further adopt the multiple-input multiple-output (MIMO) technology to synthesize a large virtual array using a few transmit (Tx) and receive (Rx) radio frequency (RF) chains. Undeniably, the MIMO-FMCW radar is the first choice of the upcoming 4D automotive radars and is currently under implementation in various chip vendors [1, 2].

Assuming the dominating role of the MIMO-FMCW automotive radar in the near future, mutual radar interference is a significant concern for driving safety as it raises noise floor, overwhelms object signals, and causes ghost objects. Mutual interference mitigation (MIM) has been traditionally considered in the context of traditional FMCW radar in the range domain, the Doppler domain, or both, and can be classified into the following categories: 1) fasttime domain MIM, such as interference-zeroing [10–12], adaptive noise cancellers [13], and fast-time mode reconstruction [14]; 2) slow-time domain MIM, such as waveform randomization [8, 15] and ramp filtering [16]; and 3) range-Doppler domain MIM, such as neural network-based denoiser [17–20]. In contrast, there are few efforts focusing on the spatial domain MIM. Spatial beamforming, e.g., least mean squares based beamforming, at the Rx phased array can be used to suppress the interference [21–25]. When the MIMO radar is used, null steering [26], Capon beamforming [27], and slowtime code design [28] by assuming interference FMCW configuration parameters can be used for more active MIM.

![](images/491ff887e51ee5e3be4bf45bf6456aaa05eef921b37ca2d79e948261eed0ed5f.jpg)  
Fig. 1: The slow-time MIMO-FMCW automotive radar architecture in the presence of incoherent MIMO-FMCW interference.

In this paper, we investigate the MIMO-FMCW mutual interference from a different perspective of spatial-domain object detection under interference by leveraging the well-developed adaptive detection literature. The key challenge here is to derive the unique interference signal model encountered in automotive radar scenarios and develop robust detectors, e.g., constant false alarm rate (CFAR) detectors. To this end, we derive a closed-form model for the first time for MIMO-FMCW mutual interference by explicitly considering time-frequency incoherence, e.g., differences between victiminterfering FMCW parameters such as time offset, pulse duration, chirp slope, etc., as well as spatial incoherence due to the slow-time code incoherence and MIMO array configuration differences. With such a closed-form interference model, the MIMO-FMCW MIM can be cast as a spatial-domain detection problem where the signal of interest is the object while the interference shares a Kronecker structure between a complicated Tx steering vector and a Fourier-based Rx steering vector. To derive a robust detector, we derive the generalized likelihood ratio test (GLRT) detector and analyze its theoretical performance in terms of the probabilities of false alarm and detection. With both theoretical and numerical validation, we show that the GLRT detector achieves better average detection performance than traditional automotive radar detectors under incoherent MIMO-FMCW mutual interference.

Throughout this paper, we use $( \cdot ) ^ { T } , \left( \cdot \right) ^ { \ast }$ , and $( \cdot ) ^ { H }$ to represent transpose, conjugate, and conjugate transpose, respectively. $\mathbf { P } _ { \mathbf { H } } ^ { \perp } \triangleq$ $\mathbf { I } - \dot { \mathbf { H } } ( \mathbf { H } ^ { H } \mathbf { H } ) ^ { - 1 } \mathbf { H } ^ { \dot { H } }$ denotes the projection matrix projecting to the space orthogonal to that spanned by the columns of H. $Q _ { F } ( \gamma )$ denotes the complementary cumulative distribution function (CCDF) of a distribution $F$ at a value $\gamma .$ . The rectangular window function $D _ { a , b } ( t ) = 1 { \mathrm { i f } } a \leq t \leq b ,$ , otherwise $D _ { a , b } ( t ) = 0$ . The indicator function $\mathbf { 1 } [ l \in { \mathcal { L } } ] = 1 { \mathrm { i f } } l \in { \mathcal { L } }$ , otherwise $\mathbf { 1 } [ l \in \mathcal { L } ] = 0$

## 2. OBJECT AND INTERFERENCE SIGNAL MODELS

## 2.1. MIMO-FMCW Source Waveform

As shown in Fig. 1, we consider a victim radar of M Tx antennas collocated with N Rx antennas over K pulses on each Tx antenna per coherent processing interval (CPI). The FMCW waveform of the victim radar is

$$
s ( t ) = e ^ { j \pi \beta t ^ { 2 } } D _ { 0 , T } ( t ) ,\tag{1}
$$

where $\beta$ is the chirp slope, and $T$ is the pulse duration. The RF waveform on Tx antenna m over K pulses is [7]

$$
s _ { m } ( t ) = \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } s ( t - k T _ { \mathrm { P R I } } ) e ^ { j 2 \pi f _ { c } ( t - k T _ { \mathrm { P R I } } ) } ,\tag{2}
$$

where ${ \mathit { c } } _ { k , m }$ is the slow-time MIMO code on the m-th Tx antenna and k-th pulse, T<sub>PRI</sub> is the pulse repetition interval (PRI) of the victim radar, and $f _ { c }$ is the carrier frequency. The incoherent interference of $\widetilde { M }$ Tx antennas shares the same waveform expressions as (1) and (2) but with different chirp slope ${ \widetilde { \beta } } ,$ pulse duration ${ \widetilde { T } } ,$ pulse number $\widetilde { K }$ PRI $\widetilde { T } _ { \mathrm { P R I } }$ , and MIMO code.

## 2.2. Object Signal Model

For an object of range R and velocity v, the round-trip propagation delay from victim radar’s m-th Tx antenna to its n-th Rx antenna is $\begin{array} { r } { \tau _ { m , n } ( t ) = 2 \frac { R + v t } { c } + m \frac { d _ { t } \sin ( \phi _ { t } ) } { c } + n \frac { d _ { r } \sin ( \phi _ { r } ) } { c } } \end{array}$ , where $d _ { t }$ and $d _ { r }$ are the Tx and Rx antenna element spacing, ϕ<sub>t</sub> and ϕ<sub>r</sub> are the Tx and Rx angle for the object, and c is the speed of propagation [7]. At the the n-th Rx antenna of the victim radar in Fig. 1, the backscattered object signal α $\begin{array} { r } { \sum _ { m = 0 } ^ { M - 1 } s _ { m } ( t - \tau _ { m , n } ( t ) ) } \end{array}$ is mixed with the conjugate of the local oscillator (LO) signal $\begin{array} { r } { \sum _ { k = 0 } ^ { \dot { K } - 1 } s ^ { * } ( t - k T _ { \mathrm { P R I } } ) e ^ { - j 2 \pi \dot { f } _ { c } ( t - k T _ { \mathrm { P R I } } ) } } \end{array}$ and sampled at $t = k T _ { \mathrm { P R I } } + l \Delta \ddot { T }$ with ∆T , leading to the dechirped and sampled baseband signal

$$
a _ { n } ^ { s } ( l , k ) = \alpha _ { \tau } ^ { \prime } e ^ { - j 2 \pi f _ { r } l } \mathbf { 1 } [ l \in \mathcal { L } ^ { s } ] \sum _ { m = 0 } ^ { M - 1 } c _ { k , m } e ^ { - j 2 \pi ( f _ { d } k + f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } ,\tag{3}
$$

where $\alpha _ { \tau } ^ { \prime } \triangleq \alpha e ^ { - j 2 \pi f _ { c } \tau } e ^ { j \pi \beta \tau ^ { 2 } }$ with α denoting the complex object amplitude, $\mathcal { L } ^ { s } \ \triangleq [ \tau / \Delta T , T / \Delta T ]$ is the set of fast-time sample indices, $f _ { \phi _ { t } } = d _ { t } \mathrm { { s i n } } ( \phi _ { t } ) / \lambda$ and $\dot { \boldsymbol { f } } _ { \phi _ { r } } = d _ { r } \mathrm { s i n } ( \phi _ { r } ) / \lambda$ are, respectively, the normalized spatial frequency at the Tx and Rx arrays with $\lambda = c / f _ { c }$ denoting the wavelength, $\tau = 2 R / c$ is the reference round-trip propagation delay, $f _ { r } \ \triangleq \ ( \beta \tau + 2 v / \lambda ) \Delta T$ is the normalized range frequency, and $f _ { d } \triangleq 2 f _ { c } T _ { \mathrm { P R I } } v / c$ is the normalized Doppler frequency. To separate $a _ { n } ^ { s } ( l , k )$ into M transmittercorresponding signals, one can first apply a range FFT to $a _ { n } ^ { s } ( l , k )$ leading to

$$
x _ { n } ^ { s } ( l ^ { \prime } , k ) = \alpha _ { l ^ { \prime } } \sum _ { m = 0 } ^ { M - 1 } c _ { k , m } e ^ { - j 2 \pi f _ { d } k } e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } ,\tag{4}
$$

where $\begin{array} { r } { \alpha _ { l ^ { \prime } } \triangleq \sum _ { l = 0 } ^ { L - 1 } \alpha _ { \tau } ^ { \prime } \mathbf { 1 } [ l \in \mathcal { L } ^ { s } ] e ^ { - j 2 \pi ( f _ { r } + l ^ { \prime } / L ) l } } \end{array}$ is the range response of the object on range bin l<sup>′</sup>. Then, when $M \leq K ,$ , with an orthogonal MIMO code sequence $\begin{array} { r } { c _ { k , m } c _ { k , m } ^ { * } = 1 , \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m ^ { \prime } } ^ { * } = } \end{array}$ $0 , \forall \ : m ^ { \prime } \neq$ m and a near-orthogonality with a Doppler modulation (e.g., the Chu sequence) [2]

$$
\operatorname* { m a x } _ { f } \left| \sum _ { k = 0 } ^ { K - 1 } c _ { k , m } c _ { k , m ^ { \prime } } ^ { * } e ^ { - j 2 \pi f k } \right| \ll K , \forall m ^ { \prime } \neq m ,\tag{5}
$$

the m-th signal corresponding to the m-th Tx antenna can be decoded as a weighted Doppler FFT,

$$
\begin{array} { r } { y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) = \displaystyle \sum _ { k = 0 } ^ { K - 1 } [ x _ { n } ^ { s } ( l ^ { \prime } , k ) c _ { k , m } ^ { * } ] e ^ { - j 2 \pi \frac { k ^ { \prime } } { K } k } } \\ { \approx b ( l ^ { \prime } , k ^ { \prime } ) e ^ { - j 2 \pi ( f _ { \phi _ { t } } m + f _ { \phi _ { r } } n ) } , } \end{array}\tag{6}
$$

where $\begin{array} { r } { b ( l ^ { \prime } , k ^ { \prime } ) \triangleq \alpha _ { l ^ { \prime } } \sum _ { k = 0 } ^ { K - 1 } e ^ { - j 2 \pi ( f _ { d } + \frac { k ^ { \prime } } { K } ) k } } \end{array}$ is the range-Doppler response of the object at range bin $l ^ { \prime }$ and Doppler bin $\bar { k } ^ { \prime }$ , and the residual from other Tx antennas is ignored due to (5). We can stack $\{ y _ { m , n } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) \}$ } into an $M N \times 1$ virtual array for the object at range-Doppler bin $( \boldsymbol { l } ^ { \prime } , \boldsymbol { k } ^ { \prime } )$

$$
\mathbf { y } ^ { s } ( l ^ { \prime } , k ^ { \prime } ) = b ( l ^ { \prime } , k ^ { \prime } ) \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } .\tag{7}
$$

where $\mathbf { a } _ { t } \triangleq [ 1 , \dots , e ^ { - j 2 \pi f _ { \phi _ { t } } ( M - 1 ) } ] ^ { T }$ is the $M \times 1$ Tx steering vector of the object, and a<sub>r</sub> $\triangleq [ 1 , \dots , \dot { e } ^ { - j 2 \pi f _ { \phi _ { r } } ( N - 1 ) } ] ^ { T }$ is the $N \times 1$ Rx steering vector of the object.

## 2.3. Interference Signal Model

Similar to the above object signal model of $( 4 ) ,$ the range spectrum of the received interference signal on the n-th Rx antenna, l<sup>′</sup>-th range bin and k-th pulse of the victim radar is

$$
x _ { n } ^ { i } ( l ^ { \prime } , k ) = \sum _ { \tilde { m } = 0 } ^ { \widetilde { M } - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k , \tilde { m } } e ^ { - j 2 \pi \widetilde { f } _ { d } k } e ^ { - j 2 \pi ( \widetilde { f } _ { \phi _ { t } } \widetilde { m } + \widetilde { f } _ { \phi _ { r } } n ) } ,\tag{8}
$$

where $\begin{array} { r l r } { \widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } } & { { } = } & { \sum _ { l = 0 } ^ { L - 1 } e ^ { j \pi ( \widetilde { \beta } - \beta ) ( l \Delta T ) ^ { 2 } } \sum _ { \widetilde { k } = 0 } ^ { \widetilde { K } - 1 } \widetilde { \alpha } _ { k , \widetilde { k } , \widetilde { m } } ^ { \prime } \mathbf { 1 } [ l \quad \in \widetilde { \Omega } _ { k , \widetilde { k } , \widetilde { m } } ] } \end{array}$ $\mathcal { L } _ { k . \widetilde { k } } ^ { i } \big ] e ^ { - j 2 \pi ( \widetilde { f } _ { r , k , \widetilde { k } } + \frac { l ^ { \prime } } { L } ) l }$ is the range response of the interference at range bin $l ^ { \prime } ,$ pulse k due to the interfering Tx channel ${ \widetilde { m } } ,$ $\begin{array} { r } { \widetilde { f } _ { d } \ = \ \ f _ { c } \frac { \widetilde { v } T _ { \mathrm { P R I } } } { c } } \end{array}$ is the normalized interference Doppler frequency, and $\widetilde { f } _ { \phi _ { t } }$ and $\widetilde { f } _ { \phi _ { \widetilde { \imath } } }$ are the normalized Tx and Rx interference spatial frequencies, $\widetilde { \alpha } _ { k , \widetilde { k } , \widetilde { m } } ^ { \prime } , \mathcal { L } _ { k , \widetilde { k } } ^ { i } .$ , and $\widetilde { f } _ { r , k , \widetilde { k } }$ are the complex amplitude, the set of fast-time samples, and the normalized interference initial fasttime frequency of the $\widetilde { k } { - } \mathrm { t h }$ interference pulse falling into the k-th victim radar’s pulse. Notice that $\widetilde { \alpha } _ { k , \widetilde { k } , \widetilde { m } } ^ { \prime } , \mathcal { L } _ { k , \widetilde { k } } ^ { i } ,$ , and $\widetilde { f } _ { r , k , \widetilde { k } }$ depend on <sup>e</sup>interfering radar’s system parameters, i.e., slow-time MIMO code, PRI $\widetilde { T } _ { \mathrm { P R I } }$ and chirp slope ${ \widetilde { \beta } } .$ After MIMO decoding and Doppler FFT, the interference spectrum on victim radar’s l<sup>′</sup>-th range bin and k<sup>′</sup>-th Doppler bin is

$$
y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { a } _ { t , m } ^ { \prime } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } n } ,\tag{9}
$$

where the decoded interference Tx steering signal is

$$
\widetilde { a } _ { t , m } ^ { \prime } = \sum _ { \widetilde { m } = 0 } ^ { \widetilde { M } - 1 } \sum _ { k = 0 } ^ { K - 1 } \widetilde { \alpha } _ { l ^ { \prime } , k , \widetilde { m } } c _ { k , m } ^ { * } e ^ { - j 2 \pi ( \widetilde { f } _ { d } + \frac { k ^ { \prime } } { K } ) k } e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { t } } \widetilde { m } } .\tag{10}
$$

Stacking $\{ y _ { m , n } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) \} _ { m , n }$ into a vector, we obtain the interference range-Doppler spectrum on a $M N \times 1$ virtual array

$$
\begin{array} { r } { \mathbf { y } ^ { i } ( l ^ { \prime } , k ^ { \prime } ) = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } , } \end{array}\tag{11}
$$

where we denote the $M \times 1$ decoded interference Tx steering vector and the $N \times 1$ interference Rx steering as

$$
\widetilde { \mathbf { a } } _ { t } ^ { \prime } \triangleq \left[ \widetilde { a } _ { t , 0 } ^ { \prime } , \widetilde { a } _ { t , 1 } ^ { \prime } , \dots , \widetilde { a } _ { t , M - 1 } ^ { \prime } \right] ^ { T } ,\tag{12}
$$

$$
\widetilde { \mathbf { a } } _ { r } \triangleq \big [ 1 , e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } } , \hdots , e ^ { - j 2 \pi \widetilde { f } _ { \phi _ { r } } ( N - 1 ) } \big ] ^ { T } .\tag{13}
$$

## 3. MIMO RADAR DETECTION UNDER INTERFERENCE

In the following, we formulate the MIM in the MIMO-FMCW automotive radar as a spatial-domain detection problem with the derived object and interference signal models. Given the detection problem of interest, the generalized likelihood ratio test (GLRT) detector is derived and its theoretical performance in terms of the probabilities of false alarm and detection is analyzed in closed-form expressions.

## 3.1. Problem Formulation

Given the object and interference signal models over a given range-Doppler bin, the spatial-domain object detection under MIMO-FMCW mutual interference is formulated as a composite hypothesis testing problem

$$
\left\{ \begin{array} { l l } { H _ { 0 } , } & { \mathbf { y } = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } + \mathbf { z } } \\ { H _ { 1 } , } & { \mathbf { y } = b \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } + \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } + \mathbf { z } , } \end{array} \right.\tag{14}
$$

where $\mathbf { y }$ is the complex-valued range-Doppler spectrum at a given range-Doppler bin $( \bar { l } ^ { \prime } , k ^ { \prime } )$ , b is the complex-valued unknown object amplitude, $\mathbf { a } _ { t }$ and ${ \bf a } _ { r }$ are given defined below $( 7 ) , \widetilde { \mathbf { a } } _ { t } ^ { \prime }$ and $\widetilde { \mathbf { a } } _ { r }$ are given by (12) and (13), and the noise $\mathbf z \sim \mathcal { C N } ( \mathbf 0 , \sigma ^ { 2 } \mathbf I _ { M N } )$ with ${ \mathbf { I } } _ { M N }$ denoting the identity matrix of size MN and $\sigma ^ { 2 }$ denoting the unknown noise power.

It is worth noting that (14) assumes the knowledge of $\widetilde { \mathbf { a } } _ { r }$ but treats $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ as an unknown vector. The former assumption is motivated by the observation that it shares the same structure, i.e., a Fourier vector, as the object Rx steering vector (by comparing (13) with ${ \bf a } _ { r }$ defined below $( 7 ) )$ at the angle of the interference. The interference angle can be estimated when the victim radar does not actively transmit but passively detect the interference, e.g., in the victim radar’s idle duration between 2 CPIs. On the other hand, the latter assumption is justified by the expression of (10) as it depends on the interfering radar system parameters such as the FMCW parameters (chirp slopes and PRIs), MIMO codes, and MIMO Tx array configurations.

## 3.2. Clairvoyant Detector

If one assumes the perfect knowledge about the decoded interference Tx steering vector $ { \mathbf { \hat { a } } } _ { t } ^ { \prime }$ and the interference Rx steering vector $\widetilde { \mathbf { a } } _ { r }$ , a clairvoyant detector can be derived as

$$
{ \cal T } ^ { C } ( { \bf y } ) = \frac { 2 } { { \widehat \sigma } _ { C } ^ { 2 } } \frac { \left| ( { \bf y } - { \widetilde { \bf a } } _ { t } ^ { \prime } \otimes { \widetilde { \bf a } } _ { r } ) ^ { H } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| ^ { 2 } } { M N } ,\tag{15}
$$

where

$$
\widehat { \sigma } _ { C } ^ { 2 } = \frac { 2 } { M N - 1 } \left| \mathbf { P } _ { \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } } ^ { \perp } ( \mathbf { y } - \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } ) \right| ^ { 2 }\tag{16}
$$

is the unbiased estimator of the noise power $\sigma ^ { 2 } \ [ 2 9 ] .$ . The clairvoyant detector suggests subtracting the interference signal $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r }$

before correlation, as indicated in (15). This fully eliminates the interference $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r }$ , while keeps the object correlation gain (a ⊗ $\mathbf { a } _ { r } ) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) = M N$

Lemma 1 The probabilities of false alarm and detection for the clairvoyant solution in (15) are

$$
P _ { F A } ^ { C } = Q _ { F _ { 2 , 2 ( M N - 1 ) } } ( \gamma ) , \quad P _ { D } ^ { C } = Q _ { F _ { 2 , 2 ( M N - 1 ) } ( \lambda ^ { C } ) } ( \gamma ) ,\tag{17}
$$

where $\gamma$ is the detection threshold, $F _ { 2 , 2 ( M N - 1 ) ) }$ is the F-distribution with 2 and $2 ( M N - 1 )$ degrees of freedom, $F _ { 2 , 2 ( M N - 1 ) ) } ( \lambda ^ { C } )$ is the noncentral F-distribution with 2 and $2 ( M N - \mathrm { 1 } )$ degrees of freedom and noncentrality parameter

$$
\lambda ^ { C } = 2 M N | b | ^ { 2 } / \sigma ^ { 2 } .\tag{18}
$$

(17) shows that the clairvoyant detector is a CFAR detector.

## 3.3. Proposed GLRT Detector

Under the assumption that the decoded interference Tx steering vector $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ is unknown but interference Rx steering vector $\widetilde { \mathbf { a } } _ { r }$ is known, we solve the GLRT solution for Problem in (14). Define

$$
\begin{array} { r } { \pmb { \theta } _ { 0 } \triangleq \widetilde { \mathbf { a } } _ { t } ^ { \prime } , \quad \pmb { \theta } _ { 1 } \triangleq [ b , \pmb { \theta } _ { 0 } ^ { T } ] ^ { T } } \end{array}\tag{19}
$$

$$
\mathbf { H } _ { 0 } \triangleq \mathbf { I } _ { M } \otimes { \widetilde { \mathbf { a } } } _ { r } , \quad \mathbf { H } _ { 1 } \triangleq [ \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } , \mathbf { H } _ { 0 } ] ,\tag{20}
$$

where ${ \bf \theta } _ { { \bf \theta } _ { 0 } } ( { \bf \theta } _ { 1 } )$ is the unknown vector under $H _ { 0 } \left( H _ { 1 } \right)$ and ${ \cal { H } } _ { 0 } \left( { \bf { H } } _ { 1 } \right)$ is the known matrix under $H _ { 0 } \left( H _ { 1 } \right)$ ). Then, the likelihood functions under $H _ { 0 }$ and $H _ { 1 }$ are, respectively,

$$
p ( { \bf y } ; H _ { 0 } ) = \frac { \exp \left[ - \frac { 1 } { \sigma ^ { 2 } } ( { \bf y } - { \bf H } _ { 0 } \boldsymbol { \Theta } _ { 0 } ) ^ { H } ( { \bf y } - { \bf H } _ { 0 } \boldsymbol { \Theta } _ { 0 } ) \right] } { ( \pi \sigma ^ { 2 } ) ^ { M N } } ,\tag{21}
$$

$$
p ( { \bf y } ; H _ { 1 } ) = \frac { \exp \left[ - \frac { 1 } { \sigma ^ { 2 } } ( { \bf y } - { \bf H } _ { 1 } \boldsymbol { \Theta } _ { 1 } ) ^ { H } ( { \bf y } - { \bf H } _ { 1 } \boldsymbol { \Theta } _ { 1 } ) \right] } { ( \pi \sigma ^ { 2 } ) ^ { M N } } .\tag{22}
$$

The GLRT test statistics is [29]

$$
T ( \mathbf { y } ) = \frac { \left( \frac { \operatorname* { m a x } _ { \boldsymbol { \Theta } _ { 1 } , \boldsymbol { \sigma } ^ { 2 } } p ( \mathbf { y } ; H _ { 1 } ) } { \operatorname* { m a x } _ { \boldsymbol { \Theta } _ { 0 } , \boldsymbol { \sigma } ^ { 2 } } p ( \mathbf { y } ; H _ { 0 } ) } \right) ^ { \frac { 1 } { M N } } - 1 } { 1 / ( M N - M - 1 ) } ,\tag{23}
$$

where the likelihood functions maximized over the unknown variables are

$$
\operatorname* { m a x } _ { \boldsymbol { \Theta } _ { 0 } , \boldsymbol { \sigma } ^ { 2 } } p ( \mathbf { y } ; H _ { 0 } ) = \exp ( - M N ) \left( \frac { \pi } { M N } \mathbf { y } ^ { H } \mathbf { P } _ { \mathbf { H } _ { 0 } } ^ { \perp } \mathbf { y } \right) ^ { - M N } ,\tag{24}
$$

$$
\operatorname* { m a x } _ { \boldsymbol { \Theta } _ { 1 } , \boldsymbol { \sigma } ^ { 2 } } p ( \mathbf { y } ; H _ { 1 } ) = \exp ( - M N ) \left( \frac { \pi } { M N } \mathbf { y } ^ { H } \mathbf { P } _ { \mathbf { H } _ { 1 } \mathbf { y } } ^ { \perp } \right) ^ { - M N } ,\tag{25}
$$

and the projection matrices are

$$
\mathbf { P } _ { \mathbf { H } _ { 0 } } ^ { \perp } = \mathbf { I } _ { M } \otimes \mathbf { P } _ { \mathbf { \tilde { a } } _ { r } } ^ { \perp } ,\tag{26}
$$

$$
\mathbf { P } _ { \mathbf { H } _ { 1 } } ^ { \perp } = \mathbf { P } _ { \mathbf { H } _ { 0 } } ^ { \perp } - \frac { \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \mathbf { \widetilde { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \mathbf { \widetilde { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) ) ^ { H } } { \left| \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \mathbf { \widetilde { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) \right| ^ { 2 } } .\tag{27}
$$

By (23), (24), (25), (26) and (27), the GLRT test statistics is

$$
T ( \mathbf { y } ) = \frac { 2 } { \widehat { \sigma } ^ { 2 } } \frac { \left| \mathbf { y } ^ { H } \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \mathbf { \widetilde { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right) \right| ^ { 2 } } { \left| \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \mathbf { \widetilde { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right| ^ { 2 } } ,\tag{28}
$$

![](images/90e377230931c3331763be784eb9233a37952e00313966f26391bbc2cd47f5b2.jpg)  
(a) Validation: $N = 8 .$

![](images/eca1ef331db35324e41a058a558eb6097949033e1d11b46f8b2865586ec2f142.jpg)  
(b) Evaluation: change N.

![](images/4a20c529e2457fca4835281e095ccebee5eea84aa7214ff2086deae6ef552f18.jpg)  
(c) Comparison: $N = 1 0 .$  
Fig. 2: Performance evaluation of ROC curves when M = 4, SNR = −5 dB and ISR = 10 dB.

where $\widehat { \sigma } ^ { 2 } = 2 \left| \mathbf { P _ { H _ { 1 } } ^ { \perp } } \mathbf { y } \right| ^ { 2 } / ( M N - M - 1 )$ is the unbiased estimator of the noise power $\sigma ^ { 2 } [ 2 9 ] . ( 2 8 )$ indicates to project interference signal $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { i }$ <sub>r</sub> to 0, i.e., $( \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \bar { \mathbf { a } } _ { r } ) ^ { H } \left( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ^ { \star } ) \right) ^ { \sim } = \big ( ( \widetilde { \mathbf { a } } _ { t } ^ { \prime } ) ^ { H } \mathbf { a } _ { t } \big ) ($ ⊗ $( \widetilde { \mathbf { a } } _ { r } ^ { H } \mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp } ) \mathbf { a } _ { r } ~ = ~ 0 ,$ as the interference Rx steering vector is projected to its orthogonal subspace, i.e., $\widetilde { \mathbf { a } } _ { r } ^ { H } \mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp } = 0$ . However, such <sup>e</sup>projection leads to the loss of object correlation gain, i.e., $\left( \mathbf { a } _ { t } ~ \otimes \right)$ $\bar { \mathbf { a } } _ { r } \bar { ) } ^ { H } \left( \mathbf { a } _ { t } \otimes ( \mathbf { P } _ { \tilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) \right) = M N ( 1 - | g _ { r } / N | ^ { 2 } ) < \bar { M } N$ , where $g _ { r } =$ $\widetilde { \mathbf { a } } _ { r } ^ { H } \mathbf { a } _ { r }$ and MN is the ideal object correlation gain of the clairvoyant detector.

Lemma 2 For (14), the probabilities of false alarm and detection for the GLRT solution in (28) can be computed as

$$
P _ { F A } = Q _ { F _ { 2 , 2 ( M N - 1 ) ) } } ( \gamma ) , \quad P _ { D } = Q _ { F _ { 2 , 2 ( M N - 1 ) ) } ( \lambda ) } ( \gamma ) ,\tag{29}
$$

where γ is the detection threshold, $F _ { 2 , 2 ( M N - 1 ) ) }$ is the F -distribution with 2 and $2 ( M N - 1 ) _ { \ O }$ ) degrees of freedom, $F _ { 2 , 2 ( M N - 1 ) ) } ( \lambda )$ is the noncentral F -distribution with 2 and $2 ( M N { \stackrel { \cdot } { - } } 1 ) )$ ) degrees of freedom with noncentrality parameter

$$
\lambda = 2 M N | b | ^ { 2 } ( 1 - | g _ { r } / N | ^ { 2 } ) / \sigma ^ { 2 } .\tag{30}
$$

It is easily seen from (29) that the proposed GLRT detector is CFAR in the existence of interference. With the two Lemmas, one can calculate performance loss from the clairvoyant detector of (15) to the proposed GLRT detector of (28) $\lambda = \lambda ^ { C } \dot { ( 1 - | g _ { r } / N | ^ { 2 } ) }$ given by (18) and (30). Moreover, the performance loss stays the same when $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ changes and is reduced when N increases.

## 3.4. Existing Automotive Radar Detector

The existing automotive radar detector follows a standard correlation over the virtual array and compares the test statistic with the noise power estimates [30, Chapter 9],

$$
T ^ { M F } ( \mathbf { y } ) = \frac { 2 } { \widehat { \sigma } _ { M F } ^ { 2 } } \frac { 1 } { M N } | \mathbf { y } ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) | ^ { 2 } ,\tag{31}
$$

where $\begin{array} { r } { \widehat { \sigma } _ { M F } ^ { 2 } = \frac { \sum _ { j = 0 } ^ { N _ { c } - 1 } \widehat { \sigma } _ { M F , j } ^ { 2 } } { N _ { c } } } \end{array}$ is the cell-average noise power estimated from $N _ { c }$ neighboring training cells (range-velocity bins), and $\begin{array} { r } { \widehat { \sigma } _ { M F , j } ^ { 2 } = \frac { 2 } { M N } \left| \mathbf { y } _ { j } \right| ^ { 2 } } \end{array}$ is estimated by the range-Doppler spectrum $\mathbf { y } _ { j }$ on the j-th training cell. In other words, the existing detector relies on an i.i.d. noise distribution over training cells and ignores the presence of the unique MIMO-FMCW mutual interference. For this reason, we refere to the existing detector of (31) as the mismatched filter.

## 4. SIMULATION RESULTS

To evalute the performance, we set $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \sim \mathcal { C N } ( \mathbf { 0 } , \widetilde { \sigma } ^ { 2 } \mathbf { R } )$ , where $\widetilde { \sigma } ^ { 2 }$ is the interference power, and $\textbf { R } \triangleq [ R _ { i , j } ] _ { 0 } ^ { M - 1 }$ is the correlation matrix with correlation coefficient ρ and $R _ { i , j } = \rho ^ { | i - j | }$ . We define signal-to-noise ratio (SNR) as $| b | ^ { 2 } / \sigma ^ { 2 }$ and interference-to-signal ratio (ISR) as $\widetilde { \sigma } ^ { 2 } / | b | ^ { 2 }$

<sup>e</sup>The theoretical performance is validated first using receiver operating characteristics (ROC) in Fig. 2. We consider a victim MIMO-FMCW radar with M = 4 Tx antennas, Tx and Rx antenna element spacing $d _ { r } ~ = ~ 0 . 5 \lambda$ and $d _ { t } \ = \ N d _ { r } ;$ an object at 33<sup>◦</sup> with SNR $= - 5 \mathrm { d B }$ ; an interferer with $\rho = 0 . 3$ and $\mathrm { I S R } = 1 0 \mathrm { d B }$ . We simulate Fig. 2 (a) and Fig. 2 (b) for a given realization of $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ and Rx interference angle at $4 5 ^ { \circ }$ . We simulate Fig. 2 (c) over 100 realizations of $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ , and for each realization of $\widetilde { \mathbf { a } } _ { t } ^ { \prime } ,$ , we average the ROC performance over 100 uniformly sampled Rx angles in $[ - 9 0 ^ { \circ } , 9 0 ^ { \circ } ]$ . For the mismatched filter, we set the number of training cells for estimating noise power to be 4, and $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ is generated randomly on each training cell.

Fig. 2 (a) validates the theoretical ROC performance of the clairvoyant detector and the proposed GLRT detector using Monte-Carlo simulation over $1 0 ^ { 6 }$ runs. Fig. 2 (b) shows that the ROC performance of the proposed GLRT detector, in general, performs better with the increase of Rx array size $N _ { \ast }$ , and is close to that of the performance of the clairvoyant detector when N is moderately large. Fig. 2 (c) shows that the average performance of the proposed GLRT detector performs in between the clairvoyant detector and the mismatched filter.

## 5. CONCLUSION

This paper investigated mutual interference mitigation among MIMO-FMCW automotive radars. Specifically, we derived the MIMO-FMCW interference signal model which motivated us to formulate the problem of interest as a spatial-domain detection problem. The proposed GLRT detector has been verified both numerically and theoretically that it achieved the CFAR against the MIMO-FMCW mutual interference and yield consistently better average detection performance than the existing automotive radar detector.

## 6. REFERENCES

[1] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 22–35, 2017.

[2] S. Sun, A. P. Petropulu, and H. V. Poor, “MIMO radar for advanced driver-assistance systems and autonomous driving: Advantages and challenges,” IEEE Signal Processing Magazine, vol. 37, no. 4, pp. 98–117, 2020.

[3] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 20–31, 2019.

[4] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 32–44, 2019.

[5] P. Wang, D. Millar, K. Parsons, and P. V. Orlik, “Nonlinearity correction for range estimation in FMCW millimeter-wave automotive radar,” in 2018 IEEE International Wireless Symposium (IWS), 2018, pp. 1–3.

[6] P. Wang, D. Millar, K. Parsons, R. Ma, and P. V. Orlik, “Range accuracy analysis for FMCW systems with source nonlinearity,” in ICMIM, 2019, pp. 1–5.

[7] P. Wang, P. Boufounos, H. Mansour, and P. V. Orlik, “Slowtime MIMO-FMCW automotive radar detection with imperfect waveform separation,” in 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 8634–8638.

[8] S. Jin and S. Roy, “FMCW radar network: Multiple access and interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 968–979, 2021.

[9] Y. Xia, P. Wang, K. Berntorp, L. Svensson, K. Granstrom,¨ H. Mansour, P. Boufounos, and P. V. Orlik, “Learning-based extended object tracking using hierarchical truncation measurement model with automotive radar,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 1013– 1029, 2021.

[10] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in 2015 IEEE International Conference on Microwaves for Intelligent Mobility (ICMIM), 2015, pp. 1–4.

[11] J. Wang, “Cfar-based interference mitigation for fmcw automotive radar systems,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–10, 2021.

[12] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the stft domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, 2019.

[13] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[14] S. Jin, P. Wang, P. Boufounos, P. Orlik, and S. Roy, “Automotive radar interference mitigation with fast-time-frequency mode retrieval,” in 2022 IEEE Radar Conference (Radar-Conf22), 2022, pp. 1–6.

[15] F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, and M. Gashinova, “Automotive radar waveform parameters randomisation for interference level reduction,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–5.

[16] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS), 2018, pp. 1–4.

[17] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Au-¨ tomotive radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR), 2020, pp. 315–320.

[18] C. Jiang, T. Chen, and B. Yang, “Adversarial interference mitigation for automotive radar,” in 2021 IEEE Radar Conference (RadarConf21), 2021, pp. 1–6.

[19] A. Dubey, J. Fuchs, V. Madhavan, M. Lubke, R. Weigel, and¨ F. Lurz, “Region based single-stage interference mitigation and target detection,” in 2020 IEEE Radar Conference (Radar-Conf20), 2020, pp. 1–5.

[20] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resource-efficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 927–940, 2021.

[21] C. Fischer, M. Goppelt, H.-L. Blocher, and J. Dickmann, “Min-¨ imizing interference in automotive radar using digital beamforming,” Advances in Radio Science, vol. 9, pp. 45–48, 2011.

[22] J. Bechter, A. Demirlika, P. Hugler, F. Roos, and C. Wald-¨ schmidt, “Blind adaptive beamforming for automotive radar interference suppression,” in 2018 19th International Radar Symposium (IRS), 2018, pp. 1–10.

[23] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in 2018 IEEE Radar Conference (Radar-Conf18), 2018, pp. 0252–0256.

[24] ——, “Experimental evaluation of adaptive beamforming for automotive radar interference suppression,” in 2020 IEEE Radio and Wireless Symposium (RWS), 2020, pp. 183–186.

[25] T. Pernstal, J. Degerman, H. Brostr˚ om, V. T. Vu, and M. I.¨ Pettersson, “GIP test for automotive FMCW interference detection and suppression,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–6.

[26] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Transactions on Microwave Theory and Techniques, vol. 65, no. 5, pp. 1727–1734, 2017.

[27] H. Chahrour, S. Rajan, R. Dansereau, and B. Balaji, “Hybrid beamforming for interference mitigation in MIMO radar,” in 2018 IEEE Radar Conference (RadarConf18), 2018, pp. 1005– 1009.

[28] A. Bose, B. Tang, M. Soltanalian, and J. Li, “Mutual interference mitigation for multiple connected automotive radar systems,” IEEE Transactions on Vehicular Technology, vol. 70, no. 10, pp. 11 062–11 066, 2021.

[29] S. M. Kay, Fundamentals of Statistical Signal Processing: Detection Theory. Prentice Hall, 1998.

[30] G. L. Charvat, Small and Short-Range Radar Systems, 1st ed. USA: CRC Press, Inc., 2014.