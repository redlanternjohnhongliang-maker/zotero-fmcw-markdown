# SPATIAL-DOMAIN OBJECT DETECTION UNDER MIMO-FMCW AUTOMOTIVE RADAR INTERFERENCE

Sian Jin<sup>†</sup>, Pu Wang‡, Petros Boufounos‡, Ryuhei Takahashi<sup>⋆</sup>, and Sumit Roy<sup>+</sup>

<sup>†</sup>Princeton University, Princeton, NJ, 08544, USA ‡Mitsubishi Electric Research Laboratories (MERL), Cambridge, MA, 02139, USA <sup>⋆</sup>Mitsubishi Electric Information Technology R&D Center, Ofuna, Kamakura City, 247-8501, Japan <sup>+</sup>University of Washington, Seattle, WA, 98195, USA

## ABSTRACT

This paper considers spatial-domain detector design for mutual interference mitigation among automotive MIMO-FMCW radars. This detector design is based on our previously derived interference signal model that fully accounts for the time-frequency incoherence and the slow-time code incoherence between the victim and interfering radars. Compared with our previous spatial-domain detector in [1], the proposed detector further exploits the structural property of both transmit and receive steering vectors of the interference for stronger interference mitigation. Preliminary numerical results confirm the performance of our proposed detector and show advantages over baseline detectors.

Index Terms— Automotive radar, MIMO-FMCW, interference mitigation, spatial-domain detection.

## 1. INTRODUCTION

Automotive radars are one of the key perception sensors to obtain range, velocity, and angles of nearby objects (e.g., cars) in all-weather conditions. For realizing low-cost design, current automotive radar chips widely adopt the frequency-modulated continuous wave (FMCW) signaling scheme [1–9]. To achieve high angular resolution, multiple-input multiple-output (MIMO) technology is combined with FMCW to synthesize a large virtual array using relatively fewer radio frequency (RF) chains. The combined MIMO-FMCW radar becomes the main way to realize upcoming 4D (range-Doppler-azimuth-elevation) automotive radars [2, 3].

As more vehicles are equipped with radar sensors operating in the same frequency bands, e.g., 76−81 GHz, mutual interference becomes a challenging issue, as shown in Fig. 1. Mutual interference mitigation has been considered for FMCW radar in the fast-time domain [10–14], slow-time domain [15–17], and range-Doppler domain [18–21]. For the spatial-domain approach, initial efforts focused on receiver beamforming-based approaches for FMCW phased array automotive radar [22–24]. For the MIMO-FMCW automotive radar, except the null steering [1, 25] and linear constraints minimum variance (LCMV) beamforming [26], there are relatively few efforts focusing on the spatial-domain interference mitigation.

Noticeably different from these efforts in [25] and [26], our previous work in [1], for the first time, derived an explicit signal model for the spatial-domain MIMO-FMCW interference mitigation under the time-frequency incoherence, the MIMO code incoherence, and array configuration difference between the victim and interfering radars. Nevertheless, we only exploited the structure of the receiver steering vector of the MIMO-FMCW interference for a subspace-based object detector in [1]. In this paper, we further extend our previous study in [1] and, more explicitly, exploit the structure of both transmit (Tx) and receive (Rx) steering vectors of the incoherent interference. To this purpose, we decompose the incoherent MIMO-FMCW interference into two orthogonal components: one is completely aligned with the object Tx steering vector, and the other is in its orthogonal complement subspace. By treating the resulting complex-valued amplitude of the decomposed interference as unknown random variables and assuming its variance can be estimated from nearby range-Doppler bins, we propose a generalized subspace-based (GS) detector that minimizes the variance of interference-plus-noise with known statistics after beamforming, maintains a fixed gain at the object direction, and cancel the residual incoherent interference. We provide closed-form analytical performance in terms of probabilities of false alarm and detection, which leads to the conclusion that the proposed GS detector has the property of constant false alarm rate (CFAR). The analysis also sheds insight on its relationship to our previously proposed detector in [1] and the clairvoyant detector that assumes perfect knowledge of the interference. Finally, numerical performance comparison between the proposed GS detector and the state-of-the-art detectors in [1] and [26] is provided.

![](images/c7fe15cb4f3961d406e7e4cf978df70c524f939634dc8802388ff837d95133f4.jpg)  
Fig. 1: Object detection under MIMO-FMCW automotive radar interference, where both victim and interfering radars use MIMO arrays to transmit and receive FMCW waveforms.

## 2. PROBLEM FORMULATION

In this section, we briefly introduce object and interference signal models and define the spatial-domain object detection problem under MIMO-FMCW mutual interference. Then, we review the state-ofthe-art detectors for solving this detection problem.

## 2.1. Signal Model

Consider a victim MIMO-FMCW radar with M Tx antennas and N Rx antennas in Fig. 1. For an object, e.g., pedestrian and cars, its virtual MIMO steering vector at a range-Doppler bin is given by [3]

$$
\mathbf { y } ^ { s } = b \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ,\tag{1}
$$

where b is the unknown object amplitude, the object Tx and Rx steering vectors with the normalized spatial frequencies $f _ { \phi _ { t } }$ and $f _ { \phi _ { \tau } }$ are given, respectively, as

$$
\mathbf { a } _ { t } \triangleq [ 1 , e ^ { - j 2 \pi f _ { \phi _ { t } } } , \hdots , e ^ { - j 2 \pi f _ { \phi _ { t } } ( M - 1 ) } ] ^ { T } ,\tag{2}
$$

$$
\mathbf { a } _ { r } \triangleq [ 1 , e ^ { - j 2 \pi f _ { \phi _ { r } } } , \hdots , e ^ { - j 2 \pi f _ { \phi _ { r } } ( N - 1 ) } ] ^ { T } ,\tag{3}
$$

and $\otimes$ represents the Kronecker product. Meanwhile, an interfering radar in Fig. 1 sends its own FMCW waveforms from its own MIMO Tx array. The $M N \times 1$ virtual MIMO steering vector of the interference is given by [1]

$$
\mathbf { y } ^ { i } = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } ,\tag{4}
$$

where $\widetilde { \mathbf { a } } _ { r }$ is the interfering Rx steering vector that is the same as (3) except at the normalized frequency $\widetilde { f } _ { \phi _ { \imath } }$ of the interference, and

$$
\widetilde { \mathbf { a } } _ { t } ^ { \prime } \triangleq \left[ \widetilde { a } _ { t , 0 } ^ { \prime } , \widetilde { a } _ { t , 1 } ^ { \prime } , \dots , \widetilde { a } _ { t , M - 1 } ^ { \prime } \right] ^ { T }\tag{5}
$$

is the interfering Tx steering vector<sup>1</sup>.

From (4), it is seen that the interfering MIMO steering vector has the Kronecker structure between the Tx and Rx steering vectors, a property shared by the object MIMO steering vector in (1). The main difference lies in the interfering Tx steering vector of (5) which is a function of the transmitting power of the interfering radar, interfering-victim relative distance and Doppler frequency, FMCW time-frequency incoherence (e.g., chirp rate, pulse duration, pulse repetition interval), MIMO incoherence (e.g., MIMO code and Tx array configuration), and timing offset between the interfering and victim radars [1]. In other words, the object Tx/Rx steering vectors and interfering Rx steering vector are fully determined by the object-victim and interfering-victim directions due to their Fourier vector structure, while the interfering Tx steering vector is almost unknown as its direction in the M-dimensional subspace is not only determined by the relative interfering-victim direction but also the mentioned incoherence.

## 2.2. Spatial-domain Detection Problem

The spatial-domain object detection under mutual interference is a composite hypothesis testing problem [1]

$$
\left\{ \begin{array} { l l } { H _ { 0 } , } & { \mathbf { y } = \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } + \mathbf { z } } \\ { H _ { 1 } , } & { \mathbf { y } = b \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } + \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } + \mathbf { z } , } \end{array} \right.\tag{6}
$$

where $\mathbf { y }$ is the complex-valued virtual MIMO snapshot at a given range-Doppler bin, $\mathbf z \sim \mathcal L \mathcal N ( \mathbf 0 , \sigma ^ { 2 } \mathbf I _ { M N } )$ is the zero-mean complex white Gaussian noise with variance $\sigma ^ { 2 }$ and ${ \mathbf { I } } _ { M N }$ is the identity matrix of size M N . The null hypothesis $H _ { 0 }$ consists of MIMO-FMCW mutual interference and noise, while the alternative hypothesis $H _ { 1 }$ consists of the object signal plus interference and noise.

It is worth noting that, in (6), we assume the knowledge of the interfering Rx steering vector $\widetilde { \mathbf { a } } _ { r }$ . This assumption on $\widetilde { \mathbf { a } } _ { r }$ is motivated by the observation that it is a Fourier vector at the angle of the interfering radar. We assume the angle of arrival or $\widetilde { f } _ { \phi _ { \tau } }$ of interference in $\widetilde { \mathbf { a } } _ { r }$ can be estimated from nearby range-Doppler bins.

## 2.3. State-of-the-art Detectors

## 2.3.1. Receiver Subspace Detector

In [1], the decoded interference Tx steering vector $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ is treated as an unknown vector, because it requires the knowledge of interfering radar system parameters such as the FMCW parameters, slow-time phase codes and MIMO Tx array configurations. Given this assumption, the receiver subspace-based (RS) detector operates on the Rxside steering vector to mitigate interference and is given by [1]

$$
T ^ { R S } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| \mathbf { y } ^ { H } \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right) \right| ^ { 2 } } { \left| \left| \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \tilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right| \right| ^ { 2 } } ,\tag{7}
$$

where $\mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp }$ denotes the projection matrix projecting to the orthogonal subspace of $\widetilde { \mathbf { a } } _ { r }$

The RS detector projects interference signal $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { \tau }$ to 0, i.e.,

$$
\left( \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } \right) ^ { H } \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right) = 0 ,\tag{8}
$$

because the interference Rx steering vector a<sub>r</sub> is projected to its orthogonal subspace, $\mathrm { i . e . , } \widetilde { \mathbf { a } } _ { r } ^ { H } ( \mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } ) = 0$ . This property is also referred to as the null steering in existing literature [25]. The null steering is independent of the interference power and is desirable when the interference power is large. However, this interference mitigation gain comes with a loss of object correlation gain, i.e.,

$$
\left( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right) ^ { H } \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \mathbf { \tilde { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right) < M N ,\tag{9}
$$

where $\left( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right) ^ { H } \left( \mathbf { a } _ { t } \otimes \left( \mathbf { P } _ { \widetilde { \mathbf { a } } _ { r } } ^ { \perp } \mathbf { a } _ { r } \right) \right)$ is the object correlation gain of <sup>e</sup>the RS detector, and MN is the ideal object correlation gain. This is undesirable when the interference power is small, because the RS detector mitigates low-power interference at the cost of losing object correlation gain.

## 2.3.2. LCMV Detector

In [26], a conventional linear constraints minimum variance (LCMV) beamformer [27] is adopted. Assume $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \sim \mathcal { C N } ( \mathbf { 0 } , \widetilde { \sigma } ^ { 2 } \widetilde { \mathbf { R } } _ { t } )$ with known interference power $\widetilde { \sigma } ^ { 2 }$ and normalized covariance matrix $\widetilde { \mathbf { R } } _ { t }$ . Further, assume $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ is independent of the noise z, we have the interference plus noise

$$
\widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } + \mathbf { z } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \widetilde { \mathbf { R } } ) ,\tag{10}
$$

with the normalized covariance

$$
\widetilde { \bf R } = \frac { \widetilde { \sigma } ^ { 2 } } { \sigma ^ { 2 } } \widetilde { \bf R } _ { t } \otimes ( \widetilde { \bf a } _ { r } \widetilde { \bf a } _ { r } ^ { H } ) + { \bf I } _ { M N } .\tag{11}
$$

The LCMV detector with knowledge of $\widetilde { \mathbf { R } }$ is given by [26, 27]

$$
{ \cal T } ^ { L C M V } ( { \bf y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| { \bf y } ^ { H } { \widetilde { \bf R } } ^ { - 1 } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| ^ { 2 } } { \left| \left| { \widetilde { \bf R } } ^ { - \frac { 1 } { 2 } } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| \right| ^ { 2 } } .\tag{12}
$$

A well-known drawback of LCMV detector is that it is sensitive to estimation error of R . However, obtaining an accurate estimate of R requires a large number of homogeneous and object-free training samples, which are generally not available or require large overhead to obtain [28]. Another well-known drawback of LCMV detector is the complexity. If the number of range-Doppler bins for estimating $\widetilde { \sigma } ^ { 2 } \widetilde { \mathbf { R } } _ { 1 }$ <sub>t</sub> is smaller than M , the estimated $\widetilde { \sigma } ^ { 2 } \widetilde { \mathbf { R } } _ { t }$ can be singular [29]. Also, the matrix inversion in (12) requires order of $\mathcal { O } ( \bar { M } ^ { 3 } N ^ { 3 } )$ operations, which are repeated for each range-Doppler bin.

![](images/f73798d3fa633622bab4342807cd6a14bf9015273e061760276781d46cc21b07.jpg)  
Fig. 2: Decomposition of $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ into $\widetilde { b } \mathbf { a } _ { t }$ and $\mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t } ^ { \prime }$ in a 3-D example, where the plane is the orthogonal subspace of a<sub>t</sub>.

## 3. PROPOSED DETECTOR DESIGN

To overcome the drawbacks of the RS and LCMV detectors, we first obtain insights from the clairvoyant detector, and then propose a new and robust detector using the insights.

## 3.1. Insights from Clairvoyant Detector

The clairvoyant detector assuming the perfect knowledge of $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ is [1]

$$
{ \boldsymbol { T } } ^ { C } ( \mathbf { y } ) = { \frac { 2 } { \sigma ^ { 2 } } } { \frac { \left| ( \mathbf { y } - \widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { r } ) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right| ^ { 2 } } { \left| \left| \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right| \right| ^ { 2 } } } .\tag{13}
$$

The clairvoyant detector suggests subtracting the interference component $\widetilde { \mathbf { a } } _ { t } ^ { \prime } \otimes \widetilde { \mathbf { a } } _ { \eta }$ before correlation, as indicated in (13). The object signal correlation gain is ideal, i.e., $\bigl ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \bigr ) ^ { H } \bigl ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \bigr ) = \tilde { M } \tilde { N } .$

To further get insights from the clairvoyant detector, we decompose the decoded interference Tx steering vector [30]

$$
\widetilde { \mathbf { a } } _ { t } ^ { \prime } = \widetilde { b } \mathbf { a } _ { t } + \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t } ^ { \prime }\tag{14}
$$

as plotted in Fig. 2, where the projected complex amplitude onto $\mathbf { a } _ { t }$ is [30]

$$
\widetilde { b } = \frac { \mathbf { a } _ { t } ^ { H } \widetilde { \mathbf { a } } _ { t } ^ { \prime } } { \vert \vert \mathbf { a } _ { t } \vert \vert ^ { 2 } } .\tag{15}
$$

Substituting (14) into (13), we obtain the clairvoyant detector with clearer insights

$$
T ^ { C } ( \mathbf { y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| ( \mathbf { y } - \widetilde { b } \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ) ^ { H } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right| ^ { 2 } } { \left| \left| \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right| \right| ^ { 2 } } .\tag{16}
$$

Equation (16) shows that the essential interference to cancel is a rank-1 interference with known direction a<sub>t</sub> $\otimes \widetilde { \mathbf { a } } _ { r }$ , and the only unknown parameter sufficient for interference cancellation is ${ \widetilde { b } } .$ . This give us a guidance for advanced interference cancellation: we need to obtain the knowledge of ${ \widetilde { b } } .$

## 3.2. Proposed Detector

The exact knowledge of $\widetilde { b }$ is hard to know. In the following, we assume that we can estimate the power of ${ \widetilde { b } } ,$ denoted by $h ^ { 2 }$ , from nearby range-Doppler bins. Assume $\widetilde { b } \sim \mathcal { C N } ( 0 , h ^ { 2 } )$ has known variance $h ^ { 2 }$ and b is independent of z. Then, the essential interference plus noise is

$$
\widetilde { \mathbf { z } } = \widetilde { b } \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } + \mathbf { z } \sim \mathcal { C N } ( \mathbf { 0 } , \sigma ^ { 2 } \mathbf { R } ) ,\tag{17}
$$

and the normalized covariance of z is

$$
{ \bf R } = \frac { h ^ { 2 } } { \sigma ^ { 2 } } ( { \bf a } _ { t } \otimes \widetilde { { \bf a } } _ { r } ) ( { \bf a } _ { t } \otimes \widetilde { { \bf a } } _ { r } ) ^ { H } + { \bf I } _ { M N } .\tag{18}
$$

We design our Rx beamformer w to satisfy the following goals: 1) minimize the variance of interference-plus-noise with known covariance after beamforming, i.e., $\mathbf { w } ^ { H } \mathbf { R w } ; ~ 2 )$ maintain a fixed gain at the object direction, i.e., $( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) ^ { H } \mathbf { w } = 1 ; 3 )$ force the the unknown interference $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r }$ to zero for any $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ , i.e., $( ( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \widetilde { \mathbf { a } } _ { t } ^ { \prime } ) \otimes \widetilde { \mathbf { a } } _ { r } ) ^ { H } \mathbf { w } = 0$ for any $\widetilde { \mathbf { a } } _ { t } ^ { \prime } .$ , which is equivalent to force $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r } ) ^ { H } \mathbf { w } \ = \ \mathbf { 0 } _ { M }$ , where $\mathbf { 0 } _ { M }$ denotes the M-dimensional column vector with all 0 elements. These designing goals lead to the following beamforming optimization problem:

$$
\begin{array} { r l } & { \underset { \mathbf { w } } { \mathrm { m i n } } ~ \mathbf { w } ^ { H } \mathbf { R } \mathbf { w } } \\ & { ~ s . t . ~ \left( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } \right) ^ { H } \mathbf { w } = 1 , } \\ & { ~ \left( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \otimes \widetilde { \mathbf { a } } _ { r } \right) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M } , } \end{array}\tag{19}
$$

whose optimal solution is

$$
\mathbf { w } ^ { G S } = \frac { \mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) } { \left\| \mathbf { R } ^ { - \frac { 1 } { 2 } } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } ) \right\| ^ { 2 } } .\tag{20}
$$

This can be proved by showing that $\mathbf { w } ^ { G S }$ is the optimal solution of the relaxed problem: min<sub>w</sub> w<sup>H</sup>Rw, s.t. $( \mathbf { a } _ { t } \otimes \bar { \mathbf { a } } _ { r } ) ^ { H } \mathbf { w } = 1$ , and $\mathbf { w } ^ { G S }$ satisfies the relaxed constraint using the structure

$$
\mathbf { R } ^ { - 1 } = \mathbf { I } _ { M N } - \frac { h ^ { 2 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ) ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ) ^ { H } } { \sigma ^ { 2 } + h ^ { 2 } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ) ^ { H } ( \mathbf { a } _ { t } \otimes \widetilde { \mathbf { a } } _ { r } ) } .\tag{21}
$$

The beamformer $\mathbf { w } ^ { G S }$ suggests the following detection statistics

$$
{ \cal T } ^ { G S } ( { \bf y } ) = \frac { 2 } { \sigma ^ { 2 } } \frac { \left| { \bf y } ^ { H } { \bf R } ^ { - 1 } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| ^ { 2 } } { \left| \left| { \bf R } ^ { - \frac { 1 } { 2 } } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) \right| \right| ^ { 2 } } .\tag{22}
$$

Compared to $T ^ { L C M V } ( \mathbf { y } )$ in (12), $T ^ { G S } ( \mathbf { y } )$ is different in that it uses the essential interference plus noise covariance matrix R instead of the total interference plus noise covariance matrix $\widetilde { \mathbf { R } } .$ . Because $T ^ { G S } ( \mathbf { y } )$ not only uses the Rx-side interference information as the RS detector but also uses the Tx-side interference information, we call the detector $T ^ { G S } ( \mathbf { y } )$ as the generalized subspace-based (GS) detector. The GS detector suggests whitening using the known interference-plus-noise covariance matrix R before correlation.

## 3.3. Performance Analysis

Theorem 1 In Problem (6) and based on the assumption $\widetilde { b }$ ∼ $\mathcal { C N } ( 0 , h ^ { 2 } )$ with known $h ^ { 2 }$ , the false alarm probability and probability of detection performance for the GS detector in (22) are

$$
P _ { F A } ^ { G S } = e ^ { - \frac { 1 } { 2 } \gamma } , P _ { D } ^ { G S } = Q _ { 1 } \left( \sqrt { \lambda ^ { G S } } , \sqrt { \gamma } \right) ,\tag{23}
$$

where $Q _ { 1 } ( x , y )$ is the Marcum $Q$ function of order $1 \ : [ 3 I ] , \gamma$ is the detection threshold and

$$
\begin{array} { c } { { \displaystyle  \boldsymbol { \lambda } ^ { G S } = \frac { 2 | b | ^ { 2 } } { \sigma ^ { 2 } } | | { \bf R } ^ { - \frac 1 2 } ( { \bf a } _ { t } \otimes { \bf a } _ { r } ) | | ^ { 2 } } } \\ { { \displaystyle = \frac { 2 M N | b | ^ { 2 } } { \sigma ^ { 2 } } ( 1 - \frac { h ^ { 2 } M | { \widetilde { \bf a } } _ { r } ^ { H } { \bf a } _ { r } | ^ { 2 } } { \sigma ^ { 2 } N + h ^ { 2 } M N ^ { 2 } } ) . } } \end{array}\tag{24}
$$

The proposed GS detector has the following properties:

1. The proposed GS detector is a constant false alarm rate (CFAR) detector in the existence of interference, as shown in (23). This CFAR property is ensured by the last condition in problem (19), i.e., $( \mathbf { P } _ { \mathbf { a } _ { t } } ^ { \perp } \tilde { \otimes } \tilde { \mathbf { a } } _ { r } ) ^ { H } \mathbf { w } = \mathbf { 0 } _ { M }$ , and the knowledge of R.

![](images/7d387f979ddc381088b820bb34614acc8e818dced4bff16ae918bb5660c70e18.jpg)  
(a) Validation: $\mathrm { I N R } = - 1 0 ~ \mathrm { d B }$ , perfect knowledge of interference statistics.

![](images/65c3d19672c244732436509a32c8ec14ca7ce74893742c77abb328a8ff64efab.jpg)  
(b) Evaluation: $\mathrm { I N R } = - 1 0$ dB, perfect and imperfect knowledge of interference statistics.

![](images/af7e7491c8b1a66801bf6817eca74816f4f95e73e7cd1de121ada54f4d571df6.jpg)  
(c) Evaluation: change INR, perfect knowledge of interference statistics.  
Fig. 3: Performance validation and evaluation of ROC curves when $M = 4 , N = 4$ , object at $3 0 ^ { \circ }$ , interferer at $4 0 ^ { \circ }$ , and $\mathrm { S N R } = - 5 \mathrm { d B }$

2. When $\begin{array} { r } { \frac { h ^ { 2 } } { \sigma ^ { 2 } } = 0 , } \end{array}$ , i.e., when the decoded interference Tx steering vector $\widetilde { \mathbf { a } } _ { t } ^ { \prime }$ falls into the orthogonal subspace of ${ \bf a } _ { t } ,$ we have

$$
T ^ { G S } ( { \bf y } ) = T ^ { C } ( { \bf y } ) , \mathrm { i f } \frac { h ^ { 2 } } { \sigma ^ { 2 } } = 0 ,\tag{25}
$$

which means that the proposed GS reduces to the clairvoyant detector. So, the GS detector does not loose object correlation gain when $\begin{array} { r } { \frac { h ^ { 2 } } { \sigma ^ { 2 } } = 0 } \end{array}$

3. When $\textstyle { \frac { h ^ { 2 } } { \sigma ^ { 2 } } } \to \infty$ , i.e., when the power of interference projected onto a<sub>t</sub> goes to infinity, we have

$$
T ^ { ^ { G S } } ( { \bf y } ) = T ^ { ^ { R S } } ( { \bf y } ) , \mathrm { i f } \frac { h ^ { 2 } } { \sigma ^ { 2 } }  \infty ,\tag{26}
$$

which means that the proposed GS detector reduces to the RS detector. So, the GS detector projects interference to 0 only when $\textstyle { \frac { h ^ { 2 } } { \sigma ^ { 2 } } } \to \infty$ , and in this case, the RS detector is desirable.

4. $\lambda ^ { G S }$ monotonically decrease with $\textstyle { \frac { h ^ { 2 } } { \sigma ^ { 2 } } }$ . This means that the detection probability of GS detector is in between the clairvoyant detector and the RS detector for a given false alarm probability. Also, when $\textstyle { \frac { h ^ { 2 } } { \sigma ^ { 2 } } }$ is closer to 0, the GS detector performance becomes close to the clairvoyant detector performance; otherwise, the GS detector performance becomes close to the RS detector performance.

Besides the advantage over the RS detector [1], another motivation of using the GS detector is its advantages over the LCMV detector [26]. First, the computational complexity of the GS detector is much reduced compared to the LCMV detector, because $\mathbf { R } ^ { - 1 } ( \mathbf { a } _ { t } \otimes$ $\mathbf { a } _ { r } )$ requires order of $\mathcal { O } ( M N )$ operations due to the closed-form in (21), while $\widetilde { \mathbf { R } } ^ { - 1 } ( \mathbf { a } _ { t } \otimes \mathbf { a } _ { r } )$ requires order of $\mathcal { O } ( M ^ { 3 } N ^ { 3 } )$ operations. More importantly, the GS detector is more robust to the interference statistics estimation error compared to the LCMV detector because the GS detector only need to estimate $h ^ { 2 }$ , while the LCMV detector needs to estimate ${ \dot { \sigma } } ^ { 2 }$ and $\widetilde { \mathbf { R } } _ { t }$ . We will validate this using simulation in the next section.

## 4. SIMULATION RESULTS

To evaluate the performance, we set $\widetilde { \mathbf { R } } _ { t } \triangleq [ \widetilde { R } _ { i , j } ] _ { 0 } ^ { M - 1 }$ is the correlation matrix with correlation coefficient ρ and $\widetilde { R } _ { i , j } = \rho ^ { | i - j | }$ . We define signal-to-noise ratio (SNR) as $| b | ^ { 2 } / \sigma ^ { 2 }$ and interference-tonoise ratio (INR) as ${ \widetilde { \sigma } } ^ { 2 } / { \sigma } ^ { 2 }$ . Under the imperfect knowledge of the interference statistics, we consider the estimation of $\widetilde { \sigma } ^ { 2 } \widetilde { \mathbf { R } } _ { t }$ as [32]

$$
\widetilde { \mathbf { R } } _ { t , q , e s t } = \widetilde { \sigma } _ { q } ^ { 2 } \widetilde { \mathbf { R } } _ { t , q } \odot ( \mathbf { 1 } _ { M } \mathbf { 1 } _ { M } ^ { H } + \mathbf { E } ) ,\tag{27}
$$

where ${ \bf 1 } _ { M }$ is the M-dimensional column vector with all 1 elements, E is a M -by-M symmetric matrix and each entry in the upper triangular of E independently follows zero-mean Gaussian distribution with variance 6.25, and ⊙ is the Hadamard product. For fair comparison between LCMV detector and GS detector, by (15), we consider the estimation of $h ^ { 2 }$ as

$$
h _ { e s t } ^ { 2 } = \frac { \mathbf { a } _ { t } ^ { H } \widetilde { \mathbf { R } } _ { t , e s t } \mathbf { a } _ { t } } { | | \mathbf { a } _ { t } | | ^ { 4 } } .\tag{28}
$$

We consider a victim MIMO-FMCW radar with M = 4 Tx antennas and $N = 4$ Rx antennas. The Tx and Rx antenna element spacing are $d _ { r } = 0 . 5 \lambda$ and $d _ { t } = N d _ { r }$ . An object locates at $3 0 ^ { \circ }$ with SNR = −5dB and an interferer with $\rho = 0 . 6$ locates at $4 0 ^ { \circ }$ . The receiver operating characteristics (ROC) performance of different detectors under this setup is shown in Fig. 3, with $P _ { D }$ denoting the probability of detection and $P _ { F A }$ denoting the probability of false alarm.

In Fig. 3 (a), we validate the theoretical performance of different detectors using Monte-Carlo simulation over $1 0 ^ { 6 }$ runs. Fig. 3 (a) shows that the performance of GS detector and the LCMV detector is in between the clairvoyant detector and RS detector. Also, under the perfect knowledge of the interference statistics, the GS detector and the LCMV detector achieve the same ROC performance, as if the GS detector knows the perfect second-order interference statistics of $\widetilde { \mathbf { a } } _ { t } ^ { \prime } .$ However, Fig. 3 (b) shows that under the imperfect knowledge of the interference statistics, the GS detector is robust to the imperfect knowledge of the interference statistics, but the performance of LCMV detector significantly degrades and may be even worse than the performance of RS detector. Fig. 3 (c) shows that the performance of GS detector is closer to the RS detector as INR increases, and is closer to the clairvoyant detector as INR decreases.

## 5. CONCLUSION

This paper investigated spatial-domain detector design for MIMO-FMCW automotive radar mutual interference mitigation. Specifically, we proposed a GS detector which is inspired by the clairvoyant detector. We showed that the proposed GS detector reduces to the clairvoyant detector and the RS detector in special cases, and outperforms the RS detector. We also showed that the GS detector outperforms the LCMV detector in the robustness to the interference statistics estimation error and computational complexity.

## 6. REFERENCES

[1] Sian Jin, Pu Wang, Petros Boufounos, Philip V. Orlik, Ryuhei Takahashi, and Sumit Roy, “Spatial-domain interference mitigation for slow-time MIMO-FMCW automotive radar,” in SAM, 2022, pp. 311–315.

[2] Sujeet Patole et al., “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 22–35, 2017.

[3] Shunqiao Sun, Athina P. Petropulu, and H. Vincent Poor, “MIMO radar for advanced driver-assistance systems and autonomous driving: Advantages and challenges,” IEEE Signal Processing Magazine, vol. 37, no. 4, pp. 98–117, 2020.

[4] Igal Bilik, Oren Longman, Shahar Villeval, and Joseph Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 20–31, 2019.

[5] Gor Hakobyan and Bin Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 32–44, 2019.

[6] Pu Wang, David Millar, Kieran Parsons, and Philip V. Orlik, “Nonlinearity correction for range estimation in FMCW millimeter-wave automotive radar,” in IWS, 2018, pp. 1–3.

[7] Pu Wang, David Millar, Kieran Parsons, Rui Ma, and Phillip V. Orlik, “Range accuracy analysis for FMCW systems with source nonlinearity,” in ICMIM, 2019, pp. 1–5.

[8] Pu Wang, Petros Boufounos, Hassan Mansour, and Philip V. Orlik, “Slow-time MIMO-FMCW automotive radar detection with imperfect waveform separation,” in ICASSP, 2020, pp. 8634–8638.

[9] Yuxuan Xia, Pu Wang, and et. al., “Learning-based extended object tracking using hierarchical truncation measurement model with automotive radar,” IEEE J. Sel. Top. Signal Process., vol. 15, no. 4, pp. 1013–1029, 2021.

[10] Michael others Barjenbruch, “A method for interference cancellation in automotive radar,” in ICMIM, 2015, pp. 1–4.

[11] Jianping Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–10, 2021.

[12] Sharef Neemat, Oleg Krasnov, and Alexander Yarovoy, “An interference mitigation technique for FMCW radar using beatfrequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, 2019.

[13] Feng Jin and Siyang Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[14] Sian Jin, Pu Wang, Petros Boufounos, Phil Orlik, and Sumit Roy, “Automotive radar interference mitigation with fast-timefrequency mode retrieval,” in RadarConf, 2022, pp. 1–6.

[15] Sian Jin and Sumit Roy, “FMCW radar network: Multiple access and interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 968–979, 2021.

[16] Fatemeh Norouzian et al., “Automotive radar waveform parameters randomisation for interference level reduction,” in RadarConf, 2020, pp. 1–5.

[17] Matthias Wagner et al., “Threshold-free interference cancellation method for automotive FMCW radar systems,” in ISCAS, 2018, pp. 1–4.

[18] Chenming Jiang, Tianyi Chen, and Bin Yang, “Adversarial interference mitigation for automotive radar,” in RadarConf, 2021, pp. 1–6.

[19] Anand Dubey et al., “Region based single-stage interference mitigation and target detection,” in RadarConf, 2020, pp. 1–5.

[20] Johanna Rock et al., “Resource-efficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 927– 940, 2021.

[21] Chenming Jiang, Zhibo Zhou, and Bin Yang, “Unsupervised deep interference mitigation for automotive radar,” in SAM, 2022, pp. 296–300.

[22] Clement Fischer et al., “Minimizing interference in automotive´ radar using digital beamforming,” Advances in Radio Science, vol. 9, pp. 45–48, 2011.

[23] Muhammad Rameez, Mattias Dahl, and Mats I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in RadarConf, 2018, pp. 0252– 0256.

[24] Thomas Pernstal et al., “GIP test for automotive FMCW inter-˚ ference detection and suppression,” in RadarConf, 2020, pp. 1–6.

[25] Jonathan Bechter, Muhammad Rameez, and Christian Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Transactions on Microwave Theory and Techniques, vol. 65, no. 5, pp. 1727–1734, 2017.

[26] Anum Pirkani et al., “Automotive interference suppression in MIMO and phased array radar,” in EuRAD, 2022, pp. 413–416.

[27] Harry L Van Trees, Optimum array processing: Part IV of detection, estimation, and modulation theory, John Wiley & Sons, 2004.

[28] M.C. Wicks, M. Rangaswamy, R. Adve, and T.B. Hale, “Space-time adaptive processing: a knowledge-based perspective for airborne radar,” IEEE Signal Processing Magazine, vol. 23, no. 1, pp. 51–65, 2006.

[29] M. A. Richards, Fundamentals of radar signal processing, McGraw-Hill, second edition, 2014.

[30] Mehrez Souden, Jacob Benesty, and Sofiene Affes, “A study of\` the LCMV and MVDR noise reduction filters,” IEEE Transactions on Signal Processing, vol. 58, no. 9, pp. 4925–4935, 2010.

[31] Yin Sun, Arp <sup>´</sup> ad Baricz, and Shidong Zhou, “On the mono- ´ tonicity, log-concavity, and tight bounds of the generalized marcum and nuttall q-functions,” IEEE Transactions on Information Theory, vol. 56, no. 3, pp. 1166–1186, 2010.

[32] Petre Stoica, Jian Li, Xumin Zhu, and Joseph R. Guerci, “On using a priori knowledge in space-time adaptive processing,” IEEE Transactions on Signal Processing, vol. 56, no. 6, pp. 2598–2602, 2008.