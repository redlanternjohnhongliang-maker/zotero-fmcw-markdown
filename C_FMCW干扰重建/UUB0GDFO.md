# Matrix-Pencil Approach-Based Interference Mitigation for FMCW Radar Systems

Jianping Wang, Member, IEEE, Min Ding, and Alexander Yarovoy, Fellow, IEEE

Abstract—A novel matrix pencil-based interference mitigation approach for FMCW radars is proposed in this paper. The interference-contaminated segment of the beat signal is firstly cut out and then the signal samples in the cut-out region are reconstructed by modeling the beat signal as a sum of complex exponentials and using the matrix pencil method to estimate their parameters. The efficiency of the proposed approach for the interference with different parameters (i.e. interference duration, signal-to-noise ratio (SNR), and different target scenarios) is investigated by means of numerical simulations. The proposed interference mitigation approach is intensively verified on experimental data. Comparisons of the proposed approach with the zeroing and other beat-frequency interpolation techniques are presented. The results indicate the broad applicability and superiority of the proposed approach, especially in low SNR and long interference duration situations.

Index Terms—FMCW radar, interference mitigation, matrix pencil, signal fusion.

## I. INTRODUCTION

radars are widely used in both civilian and military applications due to its simple processing method, high accuracy and high reliability. With the explosive increase of wireless radio and sensing applications, FMCW radars face increasingly severe interference from other devices. For instance, modern cars are equipped with multiple FMCW radars to assist drivers and improve transportation safety, where the radars inevitably cause strong interference among each other. Moreover, FMCW weather radars also suffer from the radio frequency interference from the surrounding environment. In these situations, the strong interference leads to reduced radar sensitivity and resolution, weak target masking and probably ghost target detection. Therefore, to overcome these problems and alleviate performance degradation of the radar systems, it is crucial to take proper interference mitigation in practice.

So far, a number of approaches have been proposed for interference migration, which can be mainly classified into two categories: (i) system-level approaches; (ii) post-signal processing techniques. System-level approaches exploits temporal, spatial, polarization, frequency and code diversities in radar system, antenna array and waveform design. In [1], a circular polarized antenna architecture is design to combat the linear polarized interference. Meanwhile, the frequency hopping technique learned from bats is also generally used to counteract various interference caused by spectrum congestion [2]. To identify mutual interference, the predefined orthogonal patterns [3] are imposed on the frequency modulation slopes of each FMCW burst which consists of hundreds of sweeps. Medium Access Control (MAC)-like approach is proposed to regulate transmission time of the multiple radars in the same area [4], [5]. These approaches provide effective solution to interference mitigation, but they increase the complexity of radar system or antenna design for implementation and lead to costly systems.

On the other hand, the post-signal processing techniques utilize a range of digital signal processing approaches to mitigate interference probably at the expense of increased computational load. The signal processing methods can be further divided into three classes: filtering approaches [6], [7], signals separation [8], [9], and suppression and reconstruction approaches [10]–[12]. In [6], weighted-envelope normalization approaches are proposed to deal with strong spiky mutual interference by detecting the envelope variations within a sliding time window and inversely normalizing the detected interference. In [7], an adaptive noise canceller is devised for mutual interference suppression by exploiting the different distributions of frequency spectra of target’s signals and mutual interference in the frequency domain. However, both filtering approaches are only applicable to tackle certain type of interference or point-like targets scenario, which limits their wide applications. Meanwhile, the stability of the adaptive filter is hard to guarantee.

The signals separation methods generally exploit different features, i.e., distinct sparsity of targets’ signals and the interference in different transform domains to separate them [8], [9]. So these methods require some prior information about the sparsity of the desired signal and the related interference to construct proper bases for optimal separation. However, if the “off-grid” problem between the bases (e.g., the discrete Fourier basis and short-time Fourier transform basis [8]) and the signal to be represented exists, it would lead to some loss of the degree of sparsity, thus degrading the separation performance.

By contrast, as long as the extension of the interference is limited in a certain domain, the simplest but effective method to suppress the interference is, in practice, to directly cut the interference-contaminated samples out of the signal with various windows (e.g., zeroing and inverse cosine window) [13], [14]. However, the interference cutting-out not just eliminates the interference but also suppresses part of the useful signal of targets, which reduces the signal to noise ratio (SNR) of the targets after coherent processing and decreases the range resolution. To deal with the SNR loss problem, a Burg method-based interpolation was used to extrapolate the useful signal samples in the cut-out region in the timefrequency $\left( t \ – f \right)$ domain [11]. It uses the signal samples on both sides of the cut-out gap to separately extrapolate the cut-out data forward and backward. Then, the forward- and backwardextrapolated samples in the cut-out region are summed up with weights by a specifically designed cross-fading window. This method is generally applicable to mitigate various interference for FMCW radars (as indicated in Fig. 2 later). But its extrapolation accuracy degrades dramatically when the number of the cut-out samples of signals increases. In [12], the signal extrapolation with AR model was suggested using the instrumental variable method (IVM). However, this method is not very stable and cannot always get proper signal reconstruction.

![](images/41a481e21a4bd65705efff5617eeda8b309deb133b4abc9eb080730a44c4df86.jpg)  
Fig. 1. General block diagram of mono-static linear FMCW radar system.

To accurately extrapolate the cut-out data after cut-out operation (i.e., zeroing), we propose an iterative matrix-pencil (MP) method-based extrapolation for interference mitigation. Similar to the Burg method-based approach, the proposed approach first cuts the interference-contaminated samples out of the signals and then reconstruct/extrapolate the clipped samples of the useful signals. But the proposed approach simultaneously accounts for the signals before and after the clipped samples by using a unified all-pole model which is derived from the analytical model of the beat signals of targets. So it provides the potential to get more accurate extrapolation of the non-contaminated signal in the cut-out region. Before the extrapolation, the all-pole model is first estimated based on the interference-free samples with the matrixpencil method [15], [16]. However, in practice, the noise and the possible discontinuity of the interference-free samples would impact the accuracy of the estimated signal model, thus resulting in less accurate reconstruction of the cut-out samples of useful signals. To alleviate this effect, an iterative scheme is introduced to refine the model estimation and the extrapolation, which significantly improves the accuracy of the signals in the cut-out region. Moreover, we want to mention that a method similar to the one presented in this paper has been used for multi-band signal fusion for high-resolution imaging in [17], [18]. Actually, for interference mitigation, the measured signals become two or more separate segments after interference suppression. So, using the interference-free signal segments to reconstruct/extrapolate the cut-out region is in essence a signal fusion problem. The main difference is absence of the incoherence-correction between different signal segments needed for interference mitigation. Note this paper focuses on interference mitigation on sweeps in the time domain which would be flexible to be followed by other further processing. Nevertheless, we should mention that in the case of interference mitigation followed by some specific two dimensional (2-D) processing (e.g., range-Doppler processing, range-DOA estimation), the proposed interference mitigation approach could also be extended and implemented in the highdimensional space by exploiting the 2-D or high-dimensional MP approaches [19], [20], which would be considered in future.

The rest of this paper is organized as follows. Section II formulates the basic models of the signals received by FMCW radars. In Section III, the proposed iterative matrix-pencil method based interference mitigation approach is presented. Then, its performance of interference mitigation is demonstrated in different scenarios through the numerical simulations in section IV and the experimental results in section V. Finally, conclusions are drawn in section VI.

## II. FMCW RADAR SYSTEM MODEL

## A. Transmitted and received signals

The system diagram of an FMCW radar system is shown in Fig. 1. The transmitted FMCW signal can be expressed as

$$
p ( t ) = A _ { t x } \exp \left[ j 2 \pi \left( f _ { 0 } + \frac { 1 } { 2 } K t \right) t \right] ,\tag{1}
$$

for $\begin{array} { r } { 0 \ < \ t \ < \ T / 2 . } \end{array}$ , where $A _ { t x }$ is the amplitude of the transmitted signal, and $f _ { 0 }$ is the starting frequency of an FMCW sweep. $K = B / T$ is the chirp rate defined by the ratio of the signal bandwidth B and the sweep time T . The transmitted electromagnetic (EM) signal is intercepted by targets and scattered back to the receiver. Considering the quasi-monostatic configuration of the transmit and receive antennas and assuming single scattering process for each target, the back-scattered signal can be represented as

$$
s _ { r } ( t ) = \sum _ { i = 1 } ^ { M } A _ { r x , i } \exp \left[ j 2 \pi \left( f _ { 0 } ( t - t _ { i } ) + { \frac { K } { 2 } } ( t - t _ { i } ) ^ { 2 } \right) \right]\tag{2}
$$

where $t _ { i } ~ = ~ 2 d _ { i } / c$ is round-trip time delay of the scattered signal related to the $i ^ { \mathrm { { t h } } }$ target at a distance of $d _ { i } ,$ and $A _ { r x , i }$ is the corresponding amplitude of the signal which subsumes the scattering coefficient and propagation loss. c is the speed of light and M is the number of targets.

## B. Dechirp on receiver

In FMCW radar system, dechirp processing is commonly used due to its simple operation and low requirement of sampling rate for the Analog to Digital Converter (ADC). It is implemented by mixing the received signals with the conjugate of the transmitted one, which leads to beat signals.

Considering the occurrence of strong interference $s _ { \mathrm { i n t } } .$ , the beat signal after demodulating and filtering can be formulated as (3) on the top of next page, where the superscript  denotes complex conjugate and $\mathcal { F } _ { l p }$ is the low-pass filter operator. $\tilde { A } _ { r , i }$ is the amplitude of the received signal of the $i ^ { \mathrm { { t h } } }$ target and $M ^ { \prime } ( \leq M )$ is the number of observed scatterers within the

$$
\begin{array} { l } { \displaystyle \tilde { s } ( t ) = \mathcal { F } _ { l p } \{ \left[ s _ { r } ( t ) + s _ { \mathrm { i n t } } ( t ) \right] \cdot p ^ { * } ( t ) \} } \\ { \displaystyle = \mathcal { F } _ { l p } \left( s _ { \mathrm { i n t } } ( t ) \cdot p ^ { * } ( t ) \right) + \mathcal { F } _ { l p } \left\{ \sum _ { i = 1 } ^ { M } A _ { t x } A _ { r x , i } \exp \left[ - j 2 \pi \left( f _ { 0 } t _ { i } - \frac { K t _ { i } ^ { 2 } } { 2 } \right) \right] \cdot \exp \left( - j 2 \pi K t _ { i } t \right) \right\} } \\ { \displaystyle = \mathcal { F } _ { l p } \left( s _ { \mathrm { i n t } } ( t ) \cdot p ^ { * } ( t ) \right) + \sum _ { i = 1 } ^ { M ^ { \prime } } \tilde { A } _ { r , i } \exp \left[ - j 2 \pi \left( f _ { 0 } t _ { i } - \frac { K t _ { i } ^ { 2 } } { 2 } \right) \right] \exp \left( - j 2 \pi K t _ { i } t \right) } \end{array}\tag{3}
$$

desired unambiguous range. As exp $\begin{array} { r } { \left[ - j 2 \pi \left( f _ { 0 } t _ { i } - \frac { K t _ { i } ^ { 2 } } { 2 } \right) \right] } \end{array}$ is a constant phase term related to the ${ \bf \bar { \rho } } _ { i } \mathrm { { t h } }$ target which can be subsumed by the amplitude of the signal, one can present $\begin{array} { r } { a _ { i } = \tilde { A } _ { r , i } \exp \left\lceil - j 2 \pi \left. \tilde { f } _ { 0 } t _ { i } - \frac { K t _ { i } ^ { 2 } } { 2 } \right) \right\rceil } \end{array}$ as a new complex signal amplitude. Then, (3) can be rewritten as a sum of complex exponential functions

$$
\tilde { s } ( t ) = \mathscr { F } _ { l p } \big ( s _ { \mathrm { i n t } } ( t ) \cdot p ^ { * } ( t ) \big ) + \sum _ { i = 1 } ^ { M ^ { \prime } } a _ { i } \exp { ( - j 2 \pi f _ { b , i } t ) }\tag{4}
$$

where $f _ { b , i } = K t _ { i }$ is the beat frequency corresponding to the $i ^ { \mathrm { { t h } } }$ target. For moving targets, $t _ { i } = 2 d _ { i } / c = 2 ( d _ { i 0 } + v _ { i } t ) / c$ can be used to account for the Doppler shift, where $v _ { i }$ and $d _ { i 0 }$ are the velocity and the initial distance of the $i ^ { \mathrm { { t h } } }$ target relative to the radar. Generally, as $v _ { i } \ll c ,$ it has negligible impact on the target’s beat frequency within a short FMCW sweep. After getting beat frequencies, the ranges of different targets can be calculated as

$$
d _ { i } = \frac { c \cdot f _ { b , i } } { 2 K }\tag{5}
$$

As thermal noise and measurement errors always exist due to physical limitation of the practical radar system, the signal measurements can be modeled as

$$
\begin{array} { l } { { s ( t ) = \tilde { s } ( t ) + n ( t ) } } \\ { { \ } } \\ { { \displaystyle ~ = \sum _ { i = 1 } ^ { M ^ { \prime } } a _ { i } \exp ( - j 2 \pi f _ { b , i } t ) + \mathcal { F } _ { l p } \big ( s _ { i n t } ( t ) \cdot p ^ { * } ( t ) \big ) + n ( t ) } } \\ { { \ } } \\ { { \displaystyle ~ = \tilde { s } _ { \mathrm { t a r } } ( t ) + \tilde { s } _ { \mathrm { i n t } } ( t ) + n ( t ) } } \end{array}\tag{6}
$$

where $s ( t )$ represents the measured signal, n(t) denotes the noise and measurement errors, $\tilde { s } _ { \mathrm { i n t } } ( t ) ~ = ~ \mathcal { F } _ { l p } \big ( s _ { \mathrm { i n t } } ( t ) p ^ { * } ( t ) \big )$ is the signal resulting from the interference, and $\tilde { s } _ { \mathrm { t a r } } ( t ) ~ =$ $\begin{array} { r } { \sum _ { i = 1 } ^ { M ^ { \prime } } a _ { i } \exp ( - j 2 \pi f _ { b , i } t ) } \end{array}$ is the beat signal of targets within the desired detection range. Equation (6) gives the general model of the FMCW radar measurements contaminated by strong interference.

## C. Interference

Nowadays, radar systems face various types of interference due to the rapid increase of radio wireless applications. In particular, for FMCW radar systems, the related interference can be classified as the following four cases [21]–[23]: 1) FMCW interference with the same chirp rate; 2) FMCW interference with a different chirp rate; 3) CW interference; and 4) transient interference. These cases are illustrated in Fig. 2. In Case 1), the FMCW interference would result in a strong ghost target if it appears within the reception window of the system determined by the maximum detection range. In

![](images/3470c55e485204f3a84220984f16add2b5d59f2194f0cd37632a95d68d4015f3.jpg)  
Fig. 2. Four cases of interference which corrupt the FMCW radar system. Case 1: chirp interference with the identical sweep parameters as the victim radar; Case 2: chirp interference with different sweep parameters from the victim radar; Case 3: sinusoidal/narrowband continuous interference; and Case 4: instantaneous wideband interference.

Cases 2) and 3), the FMCW and CW interference have a long time duration and lead to the non-constant beat frequency after the dechirp processing. Thanks to the low-pass filtering, their occurrences are confined in a short time around the frequency intersecting moment. In Case 4), the spectrum of the transient (or pulse) interference with a rectangular amplitude in a short time can be considered as equidistant lines with a sin(x)/x envelope. Some of these frequency lines intersect with the reference FMCW signal of dechirp operation and then, as in Case 3), result in the short interference after low-pass filtering [22].

The above analysis indicates that the interference in Cases 2), 3) and 4) all cause contaminated measurements in certain time period within an FMCW sweep duration, which in principle can be tackled using the method described in this paper (Note the interference with a very small sweep slope difference from that of the victim radar (i.e., extreme situations in case 2) could make all the signal samples contaminated, in which case the proposed approach and other zeroing plus reconstruction methods would not be applicable). Without loss of generality, we consider the FMCW signal was contaminated by an FMCW interference with a different frequency slope, i.e., Case 2) in the following sections.

Assuming an interfering FMCW radar is located at a distance $d _ { I }$ away from the transceiver, the interference signal arriving at the receiving antenna can be expressed as

$$
s _ { \mathrm { i n t } } ( t ) = A _ { I } \exp \left[ j 2 \pi \left( f _ { I , 0 } ( t - t _ { I } ) + \frac { K _ { I } } { 2 } ( t - t _ { I } ) ^ { 2 } \right) \right]\tag{7}
$$

for $t _ { I } \ < \ t \ < \ T _ { I } + t _ { I }$ , where $A _ { I }$ is the amplitude of the interference. $t _ { I } = d _ { I } / c$ is the time delay of the interference signal relative to the starting time of the transmission of the victim radar. $f _ { I , 0 }$ is the starting frequency of the interference signal and $K _ { I } = B _ { I } / T _ { I }$ is the chirp rate of the interference signal with the bandwidth $B _ { I }$ and the sweep duration $T _ { I }$

Then, the interference signal $\tilde { s } _ { \mathrm { i n t } } ( t )$ obtained after dechirping and low-pass filtering can be explicitly expressed as

$$
\tilde { s } _ { \mathrm { i n t } } ( t ) = \mathcal { F } _ { l p } \left( s _ { \mathrm { i n t } } ( t ) p ^ { * } ( t ) \right) = \mathcal { F } _ { l p } \left\{ a _ { I } \exp \left[ j \Phi ( t ) \right] \right\}\tag{8}
$$

where

$$
\Phi ( t ) = 2 \pi \left[ \left( \frac { K _ { I } } { 2 } - \frac { K } { 2 } \right) t ^ { 2 } + \left( f _ { I , 0 } - f _ { 0 } - K _ { I } t _ { I } \right) t \right]\tag{9}
$$

$$
a _ { I } = A _ { I } A _ { t x } \exp \left[ j 2 \pi \left( \frac { K _ { I } } { 2 } t _ { I } ^ { 2 } - f _ { I , 0 } t _ { I } \right) \right]\tag{10}
$$

Taking the first derivative of the phase $\Phi ( t )$ with respect to time, one can get the instantaneous beat frequency

$$
f _ { b , I } ( t ) = - \frac { 1 } { 2 \pi } \frac { \partial \Phi _ { I } ( t ) } { \partial t } = ( K _ { 1 } t + K _ { 2 } )\tag{11}
$$

where $K _ { 1 } = ( K - K _ { I } )$ and $K _ { 2 } \ = \ ( f _ { 0 } - f _ { I , 0 } + K _ { I } t _ { I } )$ are constant coefficients. According to (11), the beat frequencies resulting from the interference are time-varying. After the lowpass filtering in (8), its frequency bandwidth and the time of occurrence are confined but the time-varying property is not affected. By contrast, the beat frequencies of targets are constant, as shown in (6). This difference between the beat frequencies of targets and interferer makes the interference mitigation can be done in either time or time-frequency (t-f) domain [13].

## III. MATRIX PENCIL METHOD BASED INTERFERENCEMITIGATION

A model-based interference mitigation approach for the FMCW radar system is presented in this section. This approach can operate in either the time domain or the timefrequency domain. Without loss of generality, its details are illustrated through the time-domain processing for the interference mitigation in the following sections.

## A. Discrete signal in the time domain

From (6), the discrete signal measurements can be written as

$$
\begin{array} { l } { { \displaystyle s [ k ] = \tilde { s } _ { \mathrm { t a r } } [ k ] + \tilde { s } _ { \mathrm { i n t } } [ k ] + n [ k ] } } \\ { { \displaystyle ~ = \sum _ { i = 1 } ^ { M ^ { \prime } } a _ { i } z _ { i } ^ { k } + \tilde { s } _ { \mathrm { i n t } } [ k ] + n [ k ] } } \end{array}\tag{12}
$$

where $z _ { i } = \exp { ( j 2 \pi f _ { b , i } \Delta t ) }$ , ∆t is the sampling interval and $k = 0 , \ 1 , . . . , N - 1$ is the sampling indices of the N timedomain samples in an FMCW sweep. As analyzed above, the interference component $\tilde { s } _ { \mathrm { i n t } }$ appears in a short period in a sweep; thus, only some of the measured signal samples, e.g. from $N _ { 1 }$ to $N _ { 2 }$ are contaminated, where $0 \leq N _ { 1 } < N _ { 2 } \leq N -$ 1. Since the desired targets’ signal $\tilde { s } _ { \mathrm { t a r } }$ is a sum of exponential components, it is natural to suppress the interference by cutting out the contaminated samples from the measurements and then reconstructing the cut-out samples with the uncontaminated measurements and the model of the desired signal. As the clipped sample reconstruction is generally converted to an estimation problem of exponential components, it can be implemented with root-MUltiple SIgnal Classification (root-MUSIC), Prony’s method [24], etc. To more efficiently and accurately reconstruct the cut-out samples, we suggest using matrix pencil method in this paper, which leads to the proposed matrix-pencil method based interference mitigation.

## B. Interference mitigation

The flowchart of the matrix-pencil method based interference mitigation for FMCW radars is shown in Fig. 3. The detailed processing involves two main steps:

1) Interference detection and cutting out: Based on the analysis in the previous section, the beat frequencies of targets are generally constant in a sweep while the interference after de-chirping and low-pass filtering still exhibits non-stationary spectral property within its duration. Taking advantage of this spectral difference, the interference and its duration can be detected with many approaches, such as energy spikers detection [25], Constant False Alarm Rate (CFAR) thresholding [26], complex baseband oversampling [27] or other methods in time or time-frequency domain. After determining the location of the interference, the contaminated signal samples can be completely removed for interference suppression. However, it also eliminates part of the energy of the desired signals, which would cause signal to noise ratio (SNR) degradation of the resultant range profiles.

2) Signal extrapolation: To overcome the SNR degradation of the targets’ signals caused by the interference suppression, the removed signal samples can be reconstructed by using the interference-free samples and the corresponding signal model $\tilde { s } _ { \mathrm { t a r } } .$ Generally, the all-pole signal model $\tilde { s } _ { \mathrm { t a r } } [ k ]$ is unknown and has to be estimated from the interference-free samples. In this paper, matrix-pencil method is applied to estimate the model parameters (i.e., model order, signal poles and the coefficients) by simultaneously accounting for the interference-free samples in front of and behind the clipped ones. Moreover, to alleviate the impact of the noise and signal discontinuity of the interference-free samples on the estimation of signal model of targets, an iterative fusion process is introduced to minimize the estimation error of the signals on the both sides of the clipped region relative to the interference-free measurements. If the estimation error fulfills a desired requirement after a few iterations, the signals in the cut-out region are reconstructed.

![](images/a7be30ffd1e11fc9224964c48fa525122a4fddf0bde9eaffe89f7c6c660fb4f7.jpg)  
Fig. 3. Flowchart of the proposed MP-based interference mitigation approach.

## C. Signal fusion and reconstruction

After cutting out the interference-contaminated samples indexed from $N _ { 1 }$ to $N _ { 2 } ,$ the interference-free measurements in (12) can be represented as

$$
s [ k ] = \sum _ { i = 1 } ^ { M ^ { \prime } } a _ { i } z _ { i } ^ { k } + n [ k ]\tag{13}
$$

where $k = 0 , 1 , \cdots , N _ { 1 } - 1 , N _ { 2 } + 1 , N _ { 2 } + 2 , \cdots , N - 1$ Therefore, a gap is formed between the two signal sample segments from 0 to $N _ { 1 } \ - \ 1$ and from $N _ { 2 } + 1$ to $N ,$ as illustrated in the second plot on the right side of Fig. 3. As the useful signals in this gap are also eliminated due to the interference clipping, it would cause some SNR loss of the final coherent processing results (e.g., range profile, range-Doppler map, etc.). To overcome this problem, in the next step we try to reconstruct the useful signals in the gap based on the signal model (13) and the interference-free measurements on the both sides.

As mentioned in the introduction, here the signal reconstruction can be converted to a signal fusion problem. We suggest using the matrix-pencil based fusion method in [17], [18] to implement the signal reconstruction but no incoherence correction between different signal segments is needed.

For the convenience of description, we denote the signals before and after the clipped region as $s _ { 1 }$ and $s _ { 2 } ,$ given by

$$
\left\{ \begin{array} { l } { { s _ { 1 } [ k ] = s [ k ] , \quad k = 0 , 1 , \cdots , N _ { 1 } - 1 } } \\ { { s _ { 2 } [ k ] = s [ k + N _ { 2 } + 1 ] , \quad k = 0 , 1 , \cdots , N - N _ { 2 } - 2 } } \end{array} \right.\tag{14}
$$

Then, the detailed steps of the signal reconstruction are presented as follows.

(1) Estimate the all-pole signal model (13) with the matrix pencil method based on the front and back signal segments, i.e., $s _ { 1 }$ and $s _ { 2 }$

Generally, the signal model order $M ^ { \prime }$ is estimated according to the Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC), subspace-based automatic model order selection (SAMOS) [28], [29], etc. As SAMOS is considered to be one of the most general and robust approach to model order selection and outperforms the aforementioned methods based on the information theoretic criterion, it is used in this paper. The signal poles can be estimated with the matrix pencil method. Different from the signal pole estimation with continuous uniform signal samples, the Hankel matrices based on the discontinuous signals $s _ { 1 }$ and $s _ { 2 }$ are constructed in a slightly different way [17], [18]. Firstly, two Hankel matrices are constructed as

$$
\begin{array} { r l } { \mathbf { H } _ { i 0 } = } & { { } [ \mathbf { D } _ { 0 } ^ { i } , \mathbf { D } _ { 1 } ^ { i } , \cdots , \mathbf { D } _ { L - 1 } ^ { i } ] } \\ { \mathbf { H } _ { i 1 } = } & { { } \phantom { \mathbf { D } _ { 1 } ^ { i } , \mathbf { D } _ { 2 } ^ { i } , \cdots , \mathbf { D } _ { L } ^ { i } } [ \mathbf { D } _ { L } ^ { i } ] , } \end{array}\tag{15}
$$

with

$$
{ \bf D } _ { k } ^ { i } = [ s _ { i } [ k ] , s _ { i } [ k + 1 ] , \cdots , s _ { i } [ M _ { i } - L - 1 + k ] ] ^ { T } , \quad i = 1 , 2 .\tag{16}
$$

where $_ T$ denotes the transpose operation, $M _ { 1 } = N _ { 1 }$ and $M _ { 2 } =$ $N - N _ { 2 } - 1$ are the lengths of $s _ { 1 }$ and $s _ { 2 } ,$ respectively. $L$ is the matrix pencil parameter and $\hat { M } ^ { \prime } < L < \operatorname* { m i n } ( M _ { 1 } - \hat { M } ^ { \prime } , M _ { 2 } -$ $\hat { M } ^ { \prime } )$ , where $\hat { M ^ { \prime } }$ is the estimated signal model order (Without explicit statement, the ˆ· notation represents the estimated value of a corresponding parameter).

The Hankel matrices constructed above can be vertically stacked as

$$
\mathbf { X } _ { 0 } = \left[ \begin{array} { l } { \mathbf { H } _ { 1 0 } } \\ { \mathbf { H } _ { 2 0 } } \end{array} \right] , \quad \mathbf { X } _ { 1 } = \left[ \begin{array} { l } { \mathbf { H } _ { 1 1 } } \\ { \mathbf { H } _ { 2 1 } } \end{array} \right] .\tag{17}
$$

Then the matrix pencil $\mathbf { L } ( \lambda ) = \mathbf { X } _ { 1 } - \lambda \mathbf { X } _ { 0 }$ can be evaluated to get the estimates the signal poles $z _ { i }$ in (13) [17], [18]. To get the eigenvalues of this matrix pencil, we take advantage of the singular value decomposition (SVD)-based method in [15]. Taking the SVD of the matrix $\mathbf { X } _ { 0 }$ and $\mathbf { X } _ { 1 }$ , we get

$$
{ \bf { X } } _ { 0 } = [ { \bf { U } } _ { 0 } , { \bf { U } } _ { 0 } ^ { \prime } ] \left[ \begin{array} { c c } { { \Sigma _ { 0 , \hat { M } ^ { \prime } } } } & { { 0 } } \\ { { 0 } } & { { \Sigma _ { 0 , L - \hat { M } ^ { \prime } } } } \end{array} \right] [ { \bf { V } } _ { 0 } , { \bf { V } } _ { 0 } ^ { \prime } ] ^ { H }\tag{18}
$$

$$
\mathbf { X } _ { 1 } = [ \mathbf { U } _ { 1 } , \mathbf { U } _ { 1 } ^ { \prime } ] \left[ \begin{array} { c c } { \mathbf { \Sigma } _ { 1 , \hat { M } ^ { \prime } } } & { 0 } \\ { 0 } & { \mathbf { \Sigma } _ { \mathbf { 1 } , L - \hat { M } ^ { \prime } } } \end{array} \right] [ \mathbf { V } _ { 1 } , \mathbf { V } _ { 1 } ^ { \prime } ] ^ { H }\tag{19}
$$

where <sup>H</sup> denotes the conjugate transpose of a matrix, $H$ $\Sigma _ { 0 , \hat { M } ^ { \prime } }$ and $\Sigma _ { 1 , \hat { M } ^ { \prime } }$ are the diagonal matrices containing $\hat { M ^ { \prime } }$ dominant singular values of $\mathbf { X } _ { 0 }$ and $\mathbf { X } _ { 1 }$ , respectively. The columns of $\mathbf { U } _ { 0 } , \mathbf { U } _ { 1 } , \mathbf { V } _ { 0 }$ and $\mathbf { V } _ { 1 }$ are the left and right singular vectors related to the dominant singular values. $( \mathbf { U } _ { 0 } , \pmb { \Sigma } _ { 0 , \hat { M } ^ { \prime } } , \mathbf { V } _ { 0 } )$ and $( { \bf U } _ { 1 } , { \pmb { \Sigma } } _ { 1 , \hat { M } ^ { \prime } } , { \bf V } _ { 1 } )$ are the singular value systems related to the signal subspace in $\mathbf { X } _ { 0 }$ and $\mathbf { X } _ { 1 }$ ,respectively. The rest terms in (18) and (19) form the corresponding singular value systems related to the so-called noise subspace.

To suppress the impact of the noise on the signal pole estimation, $\mathbf { X } _ { 0 }$ and $\mathbf { X } _ { 1 }$ can be approximated by their truncated SVD as $\mathbf { X } _ { 0 T }$ and $\mathbf { X } _ { 1 T }$

$$
\mathbf { X } _ { 0 } \approx \mathbf { X } _ { 0 T } = \mathbf { U } _ { 0 } \mathbf { \Sigma } _ { 0 , \hat { M } ^ { \prime } } \mathbf { V } _ { 0 } ^ { H }\tag{20}
$$

$$
\mathbf { X } _ { 1 } \approx \mathbf { X } _ { 1 T } = \mathbf { U } _ { 1 } \mathbf { \Sigma } \mathbf { \Sigma } _ { 1 , \hat { M } ^ { \prime } } \mathbf { V } _ { 1 } ^ { H }\tag{21}
$$

Then the signal poles $z _ { i }$ can be estimated by solving the generalized eigenvalue problem det $( { \bf L } ( \lambda ) ) = 0$ of the matrix

pair $\{ \mathbf { X } _ { 0 } ; \mathbf { X } _ { 1 } \}$ , which is equivalent to the ordinary eigenvalue problem

$$
\operatorname* { d e t } \left( \boldsymbol { \Sigma } _ { 0 , \hat { M } ^ { \prime } } ^ { - 1 } \mathbf { U } _ { 0 } ^ { H } \mathbf { U } _ { 1 } \boldsymbol { \Sigma } _ { 1 , \hat { M } ^ { \prime } } \mathbf { V } _ { 1 } ^ { H } \mathbf { V } _ { 0 } - \boldsymbol { \lambda } \mathbf { I } \right) = 0\tag{22}
$$

The signal pole estimations $\hat { z } _ { i } = \lambda _ { i } , i = 1 , 2 , \cdots , \hat { M } ^ { \prime }$ are obtained.

After that, using the estimated signal model order $\hat { M ^ { \prime } }$ and the signal poles ${ \hat { z } } _ { i } ,$ the complex amplitude $a _ { i }$ can be cast as the least-square problem $\mathbf { m } = \mathbf { Z } \mathbf { a } .$ , where $\dot { \bf m } = [ s _ { 1 } , s _ { 2 } ] ^ { T }$ is the measured interference-free data, Z is the matrix formed by signal poles and ${ \bf a } = [ a _ { 1 } , a _ { 2 } , \cdots , a _ { \hat { M } ^ { \prime } } ]$ is the vector of the coefficients. Explicitly, it is represented as

$$
\left[ \begin{array} { c } { s _ { 1 } [ 0 ] } \\ { s _ { 1 } [ 1 ] } \\ { \vdots } \\ { s _ { 1 } [ M _ { 1 } - 1 ] } \\ { s _ { 2 } [ 0 ] } \\ { \vdots } \\ { s _ { 2 } [ M _ { 2 } - 1 ] } \end{array} \right] = \left[ \begin{array} { c c c c c } { 1 } & { 1 } & { \cdots } & { 1 } \\ { z _ { 1 } } & { z _ { 2 } } & { \cdots } & { z _ { \hat { M } ^ { \prime } } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { z _ { 1 } ^ { N _ { 1 } - 1 } } & { z _ { 2 } ^ { N _ { 1 } - 1 } } & { \cdots } & { z _ { \hat { M } ^ { \prime } } ^ { N _ { 1 } - 1 } } \\ { z _ { 1 } ^ { N _ { 2 } } } & { z _ { 2 } ^ { N _ { 2 } - 1 } } & { \cdots } & { z _ { \hat { M } ^ { \prime } } ^ { N _ { 2 } } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { z _ { 1 } ^ { N _ { 2 } - 1 } } & { z _ { 1 } ^ { N - 1 } } & { \cdots } & { z _ { 1 } N - 1 } \end{array} \right] \left[ \begin{array} { c } { a _ { 1 } } \\ { a _ { 2 } } \\ { \vdots } \\ { a _ { \hat { M } ^ { \prime } } } \end{array} \right]\tag{23}
$$

(2) After inserting the estimated signal poles $\hat { z } _ { i }$ and the coefficients $\hat { a } _ { i }$ into (13), the full beat signal in the sweep can be estimated by

$$
\hat { s } [ k ] = \sum _ { i = 1 } ^ { \hat { M } ^ { \prime } } \hat { a } _ { i } \hat { z } _ { i } ^ { k } , \qquad k = 0 , 1 , \cdots , N - 1\tag{24}
$$

The estimated full beat signal indicates

$$
\left\{ \begin{array} { c } { \hat { s } _ { 1 } [ k ] = \hat { s } [ k ] , \qquad k \in [ 0 , N _ { 1 } - 1 ] } \\ { \hat { s } _ { g } [ k - N _ { 1 } ] = \hat { s } [ k ] , \qquad k \in [ N _ { 1 } , N _ { 2 } ] } \\ { \hat { s } _ { 2 } [ k - N _ { 2 } - 1 ] = \hat { s } [ k ] , \qquad k \in [ N _ { 2 } + 1 , N - 1 ] } \end{array} \right.\tag{25}
$$

(3) To improve the estimation of the full beat signal, we replace the $\hat { s } _ { 1 }$ and $\hat { s } _ { 2 }$ parts in sˆ with the measurements $s _ { 1 }$ and $s _ { 2 }$ . Then the reconstructed full beat signal can be modified as

$$
\begin{array} { r } { \hat { s } [ k ] = \left\{ \begin{array} { l } { s _ { 1 } [ k ] , \qquad \quad k \in [ 0 , N _ { 1 } - 1 ] } \\ { \hat { s } _ { g } [ k - N _ { 1 } ] , \qquad \quad k \in [ N _ { 1 } , N _ { 2 } ] } \\ { s _ { 2 } [ k - N _ { 2 } - 1 ] , \qquad \quad k \in [ N _ { 2 } + 1 , N - 1 ] } \end{array} \right. } \end{array}\tag{26}
$$

Next, the reconstructed signal sˆ in (26) are used as a set of contiguous samples to re-estimate the signal poles $z _ { i }$ and the coefficients $a _ { i }$ in (13) by using the traditional matrix-pencil method [15].

(4) Repeat steps (2) and (3) to update the reconstructed results. After the step (2) in each iteration, the $l ^ { 2 }$ -norm of the differences between the estimated signals and their measured counterparts is examined to quantify the signal estimation accuracy

$$
\epsilon _ { i } = \| \hat { s } _ { 1 } ^ { ( i ) } - s _ { 1 } \| _ { 2 } + \| \hat { s } _ { 2 } ^ { ( i ) } - s _ { 2 } \| _ { 2 } ,\tag{27}
$$

where $\hat { s } _ { 1 } ^ { ( i ) }$ and $\hat { s } _ { 2 } ^ { ( i ) }$ are the estimated counterparts of the measurements $s _ { 1 }$ and $s _ { 2 }$ in the $i ^ { \mathrm { { t h } } }$ iteration. If the signal difference in the $i ^ { \mathrm { { t h } } }$ iteration satisfies the requirement

$$
\epsilon _ { i } > \epsilon _ { i - 1 } ,\tag{28}
$$

then iteration will stop. Otherwise, it continues to improve the estimated model parameters.

TABLE I  
PARAMETERS USED FOR SIMULATIONS FOR POINT-LIKE AND DISTRIBUTED TARGET SCENARIOS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>GHz</td></tr><tr><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>FMCW sweep duration</td><td rowspan=1 colspan=1>500</td><td rowspan=1 colspan=1>µs</td></tr><tr><td rowspan=1 colspan=1>Sweep slope</td><td rowspan=1 colspan=1> $\overline { { 8 \times 1 0 ^ { 1 0 } } }$ </td><td rowspan=1 colspan=1>Hz/s</td></tr><tr><td rowspan=1 colspan=1>Transmit Power</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Watt</td></tr><tr><td rowspan=1 colspan=1>Sampling frequency</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>Maximum unambiguous range</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>km</td></tr><tr><td rowspan=1 colspan=1>Point target scenari</td><td rowspan=1 colspan=1>o</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Distances of three targets</td><td rowspan=1 colspan=1> ${ \overline { { 2 , 5 , } } }$ and 5.1</td><td rowspan=1 colspan=1>km</td></tr><tr><td rowspan=1 colspan=1>Interference duration</td><td rowspan=1 colspan=1>10-50%</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>Extended targets scen</td><td rowspan=1 colspan=1>ario</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Number of point targets</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>Distance between adjacent targets</td><td rowspan=1 colspan=1>1 &lt; d &lt; 1.8</td><td rowspan=1 colspan=1>m</td></tr><tr><td rowspan=1 colspan=1>Interference duration relative to thesweep duration</td><td rowspan=1 colspan=1>24.3%</td><td rowspan=1 colspan=1>N/A</td></tr></table>

After several iteration cycles, we get the most accurate recovery of the full beat signal. Finally, by taking corresponding operations on the reconstructed full beat signal, the range profile and Doppler information of targets can be obtained with substantially improved dynamic range and suppressed “noise” floor.

## IV. NUMERICAL SIMULATIONS

To analyze performance of the proposed MP-based method to interference mitigation, several sensing scenarios have been simulated. Its results are also compared with the traditional zeroing and two of the state-of-the-art methods, i.e., Burgbased approach [11] and the IVM-based method [12].

## A. Evaluation metric

To facilitate quantitative evaluation of the accuracy of the reconstructed beat signals by different methods, we introduce two evaluation metrics: the Relative Signal-to-Noise Ratio (RSNR) and the correlation coefficient $\rho .$ The RSNR and the correlation coefficient are defined as

$$
\mathrm { R S N R } ( \mathbf { s } _ { 0 } , \hat { \mathbf { s } } ) = 2 0 \log _ { 1 0 } \frac { \left\| \mathbf { s } _ { 0 } \right\| _ { 2 } } { \left\| \mathbf { s } _ { 0 } - \hat { \mathbf { s } } \right\| _ { 2 } }\tag{29}
$$

$$
\rho _ { \mathbf { s } _ { 0 } , \hat { \mathbf { s } } } = \frac { \hat { \mathbf { s } } ^ { H } \mathbf { s } _ { 0 } } { \left\| \mathbf { s } _ { 0 } \right\| _ { 2 } \cdot \left\| \hat { \mathbf { s } } \right\| _ { 2 } }\tag{30}
$$

where ${ \bf s } _ { 0 }$ is the vector of a clean reference beat signal (without interferences and noise) and ˆs is the beat signal formed by the measured interference-free samples and the reconstructed signal samples in the cut-out region. $\lVert \cdot \rVert _ { 2 }$ denotes the $\ell ^ { 2 }$ norm operator. If the signal samples in the cut-out region are reconstructed with sufficient accuracy, a RSNR larger than the SNR of the input signal can be obtained according to (29). So the larger the obtained RSNR is, the more accurate the recovered signal samples are.

The correlation coefficient is commonly used to evaluate the similarity of two signals. Its formulation in (30) is a normalized inner product between the reconstructed signal and the reference one, which specifically represents the rotation angle between the two signals. The correlation coefficient satisfies $0 \leq | \rho _ { \mathbf { s } _ { 0 } , \hat { \mathbf { s } } } | \leq 1 . \mathrm { I f } \ | \rho _ { \mathbf { s } _ { 0 } , \hat { \mathbf { s } } } | = 1$ , then the reconstructed signal ˆs is a linear function of the reference signal $\mathbf { s } _ { 0 }$ with phase difference of $\angle \rho _ { { \bf { s } } _ { 0 } , \hat { \bf { s } } }$ (i.e., argument of $\rho _ { \mathbf { s } _ { 0 } , \hat { \mathbf { s } } } )$ . That is to say, a correlation coefficient with a larger modulus and a smaller argument indicates a better recovery performance.

## B. Point target scenario

Firstly, we demonstrate the performance of the proposed MP-based interference mitigation approach in the point target scenario. The parameters of the FMCW radar system used for the simulation are shown in Table I. Three point targets are placed at a distance of 2 km, 5 km and 5.1 km, respectively, away from the transceiver. The amplitudes of the scattered signals from the three targets from the near to further distances are set to be 1, 0.2, and 0.1, respectively.

The victim FMCW radar system suffers from a strong interference from an aggressor FMCW radar with the same operational center frequency but an opposite sweep slope and a time advancement of $7 5 \mu s$ relative to the starting time of the victim sweep. After dechirping, the interference-contaminated beat signal is acquired and illustrated in Fig. $4 ( \mathrm { a } )$ . The strong interference appears at the interval from $1 6 5 \mu \mathrm { s }$ to 265 µs (indicated by the red solid-line rectangle), which still exhibits as a chirp-like signal (see the bottom-right inset in Fig. 4(a)). Meanwhile, for clarity, part of the interference-free beat signal (from $3 5 0 \mu \mathrm { s }$ to $3 7 0 \mu \mathrm { s }$ indicated by the blue dash-dotted rectangle) is zoomed in and shown in the top-right inset. It is clear that the beat signal of targets is composed of the sinusoidal components. Moreover, white Gaussian noise with the SNR of 15 dB is added to the signal to account for the thermal noise and measurement errors of the radar system.

The interference-contaminated beat signal produces a range profile with significantly increased noise floor (see “sig Int” in Fig. 5(a) where the two targets at the further distances are almost shadowed by the raised noise floor) if the range compression is performed directly by using the fast Fourier transform (FFT). To mitigate the interference by using the proposed MP-based approach, the interference-contaminated samples of the signal are firstly detected and cut out (i.e., zeroing with a rectangular window [14]). Zeroing the interferencecontaminated samples results in two separate signal segments with a gap inbetween (see the top panel in Fig. 4(c)), which causes not only power loss of targets’ signals but also high sidelobes of the range profile, thus degrading the performance of target detection. To overcome these effects, the proposed MP-based interference mitigation method is used to reconstruct the signal samples in the cut-out gap based on the signal model (24) and the rest interference-free ones in front and back. Before reconstruction, the model order was estimated to be three by using the SAMOS method (see Fig. 4(b)), which agrees with the true value. Then, by exploiting the proposed iterative scheme, the signal samples in the gap were recovered with sufficient accuracy, as shown in the middle plot and a close-up of them in the bottom panel in Fig. 4(c). For comparison, the interference-free reference signal (with the noise) and the recovered signals with the Burg-based method and the IVM, which used the same model order as that of the MP-based method, are also shown in the middle and bottom panels. One can see that both the signal recovered with the proposed MP-based method has the best agreement with the reference one. Meanwhile, the IVM method achieves more accurate reconstruction of the signals in the cut-out region than the Burg-based method in this case.

![](images/6ae48d19e451df3a1a45bd20c8ceda1a011e8ac045ae13aa7e8392ac02c6c39d.jpg)  
(a)

![](images/8919095e81b7859c4358a8d675ad81d62a26f951a30844bbd6f66bd0f6f9ff97.jpg)  
(b)

![](images/9f6177dd21c43c09159b1454048c9e83bf41d80a665d8ca0b883af0579c6a246.jpg)

![](images/f3dbb0daf552b761eab79300c17915893dcec683ca230dd1bdba8b44b9cd542d.jpg)

![](images/9e8069266caa5ea9892c996f2fae11a36e69c9ef23dc39a3f9faa303d9e3f5d9.jpg)  
(c)  
Fig. 4. Numerical simulation for interference mitigation in the point target scenario. (a) shows the interference-contaminated beat signal. (b) presents the metric values of SAMOS for model order estimation. (c) displays the results after interference mitigation.

![](images/46a2e37bc26d8b36a6b8538378f059759f84215685c51c693ad40fe77a1f20a4.jpg)  
(a)

![](images/7de4c91e1e7521f08cd75aed16ed0d106c3195fb28554d4c17ddb0c638b1877d.jpg)  
(b)

![](images/983f61326e08bcf7325a604b6db413efedeccc146ca0106e29362ef405e6e1f2.jpg)  
(c)  
Fig. 5. (a) displays the range profiles of the targets obtained with the interference-contaminated signal, interference-free reference signal, and the signals processed with the zeroing, Burg- and MP-based methods; (b) and (c) are the close-ups of the range profile around the distances of targets, respectively.

To further examine the accuracy of the reconstructed signals, the range profiles of targets are constructed by taking the FFT of them and shown in Fig. 5. For comparison, the range profiles obtained with the interference-contaminated [i.e., “sig Int” in Fig. 5(a)] and interference-free reference beat signals [i.e., “Ref” in Fig. 5(a)] are also presented. Note all the range profiles in Fig. 5 are normalized by the maximum of the range profile acquired with the interference-contaminated signal.

According to Fig. 5(a), all the interference mitigation methods, i.e., zeroing, Burg-, IVM- and MP-based methods, significantly reduce the “noise” floor of the range profile and thus increase its dynamic range compared to the one obtained with the interference-contaminated signal. Among them, the zeroing method is computationally most efficient by simply replacing the interference-contaminated samples with zeros, however, resulting in a gap between the front and rear signal samples. Consequently, it causes high sidelobes and some SNR loss in the range profile compared to that obtained with the reference signal. Specifically, from the insets in Fig. 5(b) and (c), the peaks of targets’ range profiles obtained after zeroing are 1.9 dB lower than those formed with the reference signal and the signal reconstructed with the MP-based method. Although the Burg- and IVMbased method efficiently interpolate the samples in the cut-out gap and result in comparable/identical range profiles as the reference signal for the target at the short distance, they fail to overcome the power loss for the two weak targets at the further distances and get range profiles close to that of the zeroing method (see the insets in Fig. 5(c)). By contrast, the

MP-based method not only conquers the power loss of the range profile for all the targets but also accurately reconstructs their range profiles in terms of both main lobe and the sidelobes. Quantitatively, for the beat signals in Fig. 4(c) recovered with the Burg-, IVM- and MP-based methods, their RSNRs are 14.55 dB, 18.86 dB and 28.68 dB, and the corresponding correlation coefficients are $0 . 9 8 3 0 e ^ { - j 0 . 0 0 1 8 }$ , 0.9935e<sup>j0.0044</sup> and 0.9993e<sup>j0.0003</sup>, respectively, relative to the clean reference signal. Therefore, it recovers the signal samples in the cutout region more accurately than the Burg- and IVM-based methods.

## C. Extended target scenario

Here we consider the applicability of the proposed method to extended target scenarios. The parameters used for the simulation are shown in Table I. An extended target formed by 15 point scatterers with adjacent inter-distances less than the range resolution of the radar system (i.e., 3.75 m in ours simulation) was simulated. The target was located at the range of 3 – 3.025 km away from the transceiver. The amplitudes and phases of the scattered signals from these closely spaced scatterers were random values with uniform distribution in [0, 0.05] and uniform distribution in [0, 2π], respectively. A beat signal with the SNR of 15 dB was synthesized by adding white Gaussian noise to consider measurement errors and thermal noise of the system and also contaminated by a strong interference with the same center frequency but a sweep slope of -0.98 times of that of the victim radar. The resultant beat signal is illustrated in Fig. 6(a).

Similar to the point target scenario, the interferencecontaminated samples are first detected and cut out. The result is shown in the top panel in Fig. 6(d). Then, the signal model order was estimated by using the SAMOS method based on the other interference-free samples. However, due to the strong correlation among the beat signals scattered by the closely spaced scatterers, the model order was selected to be two by using the SAMOS method, which is significantly different from the theoretical value fifteen (see Fig. 6(b)). So the SAMOS method cannot work properly in such scenarios. To investigate the reason of the failure of the SAMOS, we checked the singular value distribution of the matrix used for model order selection, as shown in Fig. 6(c). Based on Fig. 6(c), it is obvious that a proper model order should be not smaller than four. Taking the model order of four, the signal samples in the cut-out region were recovered by using the Burg-, IVM- and MP-based methods, which are shown in the two bottom plots in Fig. 6(d) and Fig. 6(e), respectively. It is clear that the IVM-based interpolation is not stable and a blowup is observed in Fig. 6(e). Meanwhile, compared to the Burgbased method, the proposed MP-based method reconstructed the signal samples with the best agreement with the reference signal (see the bottom plot in Fig. 6(d)). Taking the FFT of the signal obtained after zeroing and the recovered signals with Burg- and MP-based methods, the related range profiles of targets were constructed and shown in Fig. 7(a). As expected, the range profile of the targets constructed with the signal recovered with the MP-based method has the best agreement with that formed using the reference signal. For quantitative evaluation, the RSNRs of the beat signals recovered with the Burg- and MP-based methods are obtained as 7.07 dB and 10.66 dB, respectively. Their correlation coefficients relative to the reference signal are $0 . 8 9 7 5 e ^ { - 0 . 0 3 1 1 }$ and 0.9584e<sup>0.0443</sup>. So the RSNRs and correlation coefficients confirm that the MP-based method gets more accurate signal reconstruction in the cut-out region than the Burg-based method.

![](images/de19268b474e9fecd9eed1602e78753354f42a588b7591f8c830a4864687985c.jpg)  
(a)

![](images/5fb532c3f6fadc7445087ca9558e9636035d31c0e619c0c838cbb21446e4b97e.jpg)  
(b)

![](images/bc3b1da26ed8b6469d7707738a073a0f8952aae2950e02874c8edb09911ad0e2.jpg)  
(c)

![](images/a150a6228259676e51bc75a55b9c9b324b5bd525b2242d3d12cf42a9a97fc720.jpg)

![](images/659ee6dfe8975f7048cb50fce327b677c165aa4e07573401008f6d32df9fc90b.jpg)

![](images/8385e5e8371c1093cb02f26716ee59bc9cb48bde0397fa3372006798ecace43e.jpg)

![](images/84676fc42f8915a71330f61b4e5a78aa34f8ce6d3b0aca4a612cd7d243c2a335.jpg)  
(d)

(e)  
![](images/aef021f20164ac70af2dcfc20d57c290628de2fe9994b453d19c3bfbcdb57a56.jpg)  
(f)  
Fig. 6. Numerical simulation for interference mitigation in the extended target scenario. (a) shows the interference-contaminated beat signal of an extended target. (b) shows the metric values of SAMOS approach for model order selection while (c) presents the singular values distribution of the matrix constructed for model order selection. (d) shows the results after interference mitigation, where the top panel gives the beat signal after zeroing; the middle panel presents the reference beat signal and the beat signals recovered with the Burg- and MP-based methods with the model order of four; and the bottom panel is the close-up view of the recovered samples in the cut-out region. (e) shows the beat signal recovered by the IVM with the model order of four and (f) displays the recovered beat signals with the model order of 15.

Moreover, we also reconstructed the signal samples in the cut-out region using the three methods by setting the model order to be fifteen. Again, a blow-up as in Fig. 6(e) is observed in the recovered signal by the IVM-based method (here the figure is omitted for conciseness). So it indicates that the instability of the IVM-based method may not be caused by the underestimation of the signal model order. Meanwhile, the recovered signal by the Burg-based method is still less accurate than that obtained with the MP-based method (see Fig. 6(f) and Fig. 7(b)). The RSNR and correlation coefficient of the recovered signal by the Burg-based method are 5.98 dB and $0 . 8 7 7 9 e ^ { 0 . 0 3 2 \bar { 4 } }$ and their counterparts for the signal reconstructed with the MP-based method are 11.48 dB and 0.9663e<sup>0.0639</sup>, which further confirms that the MP-based method is superior to the Burg-based one in term of the signal reconstruction accuracy.

Finally, we want to mention that when multiple point targets in the same range bin are very close to each other, the Burg-based method could occasionally outperform the proposed MP-based method (for conciseness, we do not show it here). As the close targets in a range bin results in highly correlated beat frequencies, the characteristic polynomial of the corresponding AR model has many closely spaced roots. The proposed MP-based method tends to estimate some dominant sinusoidal components (i.e., roots) that are close to the real roots in the mean square error sense while the Burgbased method attempts to estimate the coefficients of the characteristic polynomial of the AR model. Apparently, the latter operation is easier in such cases; thus, the Burg-based method results in more accurate signal estimation.

![](images/176e5cb86766a2ca8386c411d766b1d237a945602ba9ad7e0b65617990e9363b.jpg)

(a)  
![](images/15371ef54891516c3faf3feb4c660be764637a21b9fa03ef74adab924a6ee045.jpg)  
(b)  
Fig. 7. Range profile of the extended target obtained with the reference signal, interference-contaminated beat signal, the signals obtained with zeroing, and the signals recovered by the Burg- and MP-based methods with (a) the model order of four and (b) the model order of fifteen.

## D. Effect of the length of interferences and SNR

The impact of the interference duration (equivalently, the size of the cut-out gap caused by interference suppression) and the SNR on the performance of the proposed MP-based method for signal recovery is investigated in this section. For generality, the size of a cut-out gap is denoted by the ratio between the number of the removed interference-contaminated samples and the number of all signal samples in a sweep. The parameters for section IV-B point target scenario simulation were used here. In the simulation, the SNR changes from −30 dB to 10 dB with steps of 10 dB and at each SNR the interference duration increases from 10% to 50% with steps of 10%. To investigate the statistical performance of the proposed MP-based approach, 100 Monte Carlo runs were conducted at each SNR. The average RSNRs and correlation coefficients of the signals recovered by Burg- and MP-based methods are shown in Fig. 8 (due to the blow-ups of signals recovered the IVM-based method, the corresponding RSNRs and correlation coefficients cannot be computed and are omitted here).

From Fig. 8(a), one can see that the RSNRs of the signals reconstructed with the Burg- and MP-based methods are almost identical when the SNR is smaller than 0 dB. Meanwhile, they gradually improve and are larger than the SNRs with the increase of the size of the cut-out region. By contrast, when the SNR is equal to/larger than 0 dB the RSNRs of the signals obtained with the Burg- and MP-based methods show different changing trends (i.e., increase for MP-based method while keep steady/decrease for Burg-based method) with the widening of the cut-out gap. This is because that the cut-out operation eliminates not only the interference but also the noise in the interference-contaminated signal samples. When $\mathrm { S N R } < 0 \mathrm { d B } .$ , the eliminated noise power is larger than that of the useful signals; thus, the RSNR would be larger than the SNR as long as the useful signal samples in the cutout region can be recovered with certain accuracy with either Burg- and MP-based methods. However, when $\mathrm { S N R } \geq 0 \mathrm { d B } ,$ more signal power is suppressed than the noise power. The MP-based method jointly uses the signal samples at both sides of the gap to accurately recover the data in the cutout region via an iterative scheme. The recovered signal could be equivalently regarded as the filtered samples, getting higher RSNR than the SNR of the original signal. In particular, when the cut-out gap occupies 50% of the whole sweep, almost half of the noise power is suppressed; thus, 3 dB improvement of RSNR relative to the SNR of the input signal can be obtained as long as the useful signal samples in the cut-out region are accurately reconstructed (see Fig. 8(a)). On the other hand, the Burg-based method separately extrapolates the signal samples in the cut-out gap from both sides. Its extrapolation accuracy degrades rapidly with the widening of the cut-out region, which causes larger signal difference (especially, large phase differences) between the reconstructed signal and the reference and thus makes its RSNR even worse than the original SNR. Therefore, in terms of the RSNR of the recovered signal, the Burg- and MP-based obtain comparable results when SNR < 0 dB while the latter one outperforms the former one when $\mathrm { S N R } \geq 0 \mathrm { d B }$

However, Fig. 8(b) shows that the MP-based method constantly obtains comparable/better signal reconstruction compared to the Burg-based method regarding the modulus of the correlation coefficient. Moreover, with the increase of the SNR and the interference duration, the performance advantage of the MP-based method to the Burg-based one becomes larger. However, the phase of the correlation coefficient between the recovered signals with both methods and the reference are comparable when the interference duration is smaller than 40% (Fig. 8(c)). It gradually reduces to zero with the increase of the SNR of the original signal. Therefore, according to the above analyses, the MP-based method generally gets more accurate signal reconstruction than the Burg-based method in terms of both RSNR and correlation coefficient of the recovered signal.

## E. Computational Efficiency

Both Burg- and IVM-based methods are very computational efficient as they just separately extrapolate the data in the gap from both sides. By contrast, the proposed MP-based method uses the SVD and an iterative scheme to jointly recover the signal in the cut-out region. So its computational load is slightly heavier than that of the Burg- and IVM based methods, which depends on the number of iterations in practice. For a scenario with moderate interference duration (20%-30%) and SNR, the MP-based method generally needs several iterations. Specifically, for the simulation in section IV-B, it took 0.02 s, 0.15 s and 27.05 s for the Burg-, IVM- and MP-based methods, respectively, when they were implemented in MATLAB and run on a computer with Intel Core i5-3470 Central Unit Processor (CPU) @ 3.2GHz and 8GB Random Access Memory (RAM). In this case, four iterations were executed in the MPbased method. To accelerate the MP-based method, Lanczos iteration [30] or randomized algorithm [31] for the SVD could be exploited in future.

![](images/781f3b99c97a2bc81c358f3b5e9969b30169f9a66286caebcaf0f4e43fafadbd.jpg)  
(a)

![](images/3b76b59ae493aab019b35fedf693c41a634df2a08e39f19ea7068d4cb77fb863.jpg)  
(b)

![](images/323cdb728f5f4b1f4b43bee735f1d2fa94e68f3d07215627d7ba01f9c6708910.jpg)  
(c)  
Fig. 8. Impact of gap duration and SNR on the accuracy of the reconstructed signals with the Burg- (dashed blue lines) and MP-(solid red lines) based methods. (a) shows the RSNRs with different gap durations. (b) and (c) show the moduli and phases of the correlation coefficients with respect to different gap durations.

## V. EXPERIMENTAL RESULTS

In this section, experimental results with radar observations of an industrial chimney and raindrops are presented to demonstrate the effectiveness and accuracy of the proposed MP-based interference mitigation method.

## A. Experimental Setups

The experiments used the TU Delft PARSAX [32] Sband (3.1315 GHz) radar system which is a full-polarimetric FMCW radar with two independent highly linear polarimetric RF channels in both transmitter and receiver. In the experiments, we consider the interference problem among the different polarimetric signals scattered from targets when the full-polarimetric radar simultaneously emits both horizontally and vertically polarized signals through the two transmitting channels and simultaneously acquires the scattered fullpolarimetric signals. Specifically, we use the up- and downchirp signals for simultaneous transmission on the horizontal (H-pol) and vertical (V-pol) polarization channels of the PARSAX radar, respectively. Then, the HV- (H-pol transmission, V-pol reception) and VV-(V-pol transmission, V-pol reception) polarimetric signals scattered from the same target would arrived at the V-pol receiving antenna at the same time. Although the up- and down-chirp waveforms are of great help to distinguish the scattered HV-pol and VV-pol signals, the strong VV-pol signal would still cause strong interference in the output of the HV-pol receiving channel. This kind of the interferences is categorized as Case 2 in Fig. 2.

In Experiment 1, we considered an industrial chimney as a stationary target and took measurements for a single sweep. The chimney is about 1.07 km away from PARSAX radar, which is installed on the roof of the building of the faculty of Electrical Engineering, Mathematics & Computer Science (EEMCS), TU Delft. The PARSAX radar is shown in Fig. 9(a) and an image of the chimney captured by a camera with the same orientation as the radar is presented in Fig. 9(b). In Experiment 2, we observed a rain storm, which can be considered as a distributed target, by pointing the PARSAX radar vertically. The parameters for experimental measurements are listed in Table II.

TABLE II  
EXPERIMENTAL SETUP PARAMETERS FOR EXPERIMENT 1 AND EXPERIMENT 2
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Center frequency</td><td rowspan=1 colspan=1>3.1315 GHz</td></tr><tr><td rowspan=1 colspan=1>Bandwidth</td><td rowspan=1 colspan=1>40 MHz</td></tr><tr><td rowspan=1 colspan=1>Time duration of a sweep</td><td rowspan=1 colspan=1>1 ms</td></tr><tr><td rowspan=1 colspan=1>Number of samples per sweep</td><td rowspan=1 colspan=1>16384</td></tr><tr><td rowspan=1 colspan=1>Maximum range</td><td rowspan=1 colspan=1>18.75 km</td></tr><tr><td rowspan=1 colspan=1>Number of sweeps per CPI</td><td rowspan=1 colspan=1>512</td></tr><tr><td rowspan=1 colspan=1>Waveform</td><td rowspan=1 colspan=1>Simultaneous up- and down-chirps on the H-pol andV-pol polarization channels</td></tr></table>

![](images/1c6d4e1579e781c55adc86a629eee7b450b6e88e09fda69acb4b114ded5d8427.jpg)  
(a)

![](images/121be94280dcae77396e56bdd25d9559e0c1faddb0b809ba3f346268af269e6f.jpg)  
(b)  
Fig. 9. Experimental measurement setup. (a) shows PARSAX radar on the roof of EEMCS Faculty building and (b) the industrial chimney used as a stationary target.

## B. Experiment 1: Stationary isolated target (Chimney)

Fig. 10(a) shows the acquired HV-pol beat signal (i.e., “sig Int” in the solid red line) when the transmitter simultaneously emitted the up- and down-chirp signals with opposite chirp rates through the two transmitting channels with horizontal and vertical polarizations, respectively. The acquired HV-pol beat signal was polluted by the strong VVpol signal arrived together at the receiving antenna, and the interference-contaminated samples are indicated by the dashed red rectangle in Fig. 10(a). For comparison, the reference HVpol signal (i.e., “ref sig” in the dashed blue line) acquired by transmitting a single H-pol up-chirp signal is also presented.

To suppress the VV-pol interference, the received signal was processed by using the zeroing, Burg-, IVM- and the proposed MP-based interference mitigation methods and the results are shown in Fig. 10(c) and (d). Comparing the signals obtained by all four interference mitigation methods with the reference signal, the MP-based method almost accurately reconstructs the clipped samples in the interference-contaminated region while the Burg-based method recovers these samples with underestimated amplitudes. By contrast, the IVM-based method leads to a blow-up in the recovered beat signal (Fig. 10(d)), which again shows its instability. In addition, before applying the Burg-, IVM- and MP-based methods to recover the signal samples in the cut-out region, SAMOS was used to estimate the signal model order and a model order of two was selected, which is highly underestimated considering the complex environment surrounding the chimney. Hence, we decided to select the model order empirically based on the normalized singular value distribution of the matrix used by SAMOS (see Fig. 10(b)). With a threshold of 10<sup>−2</sup> (i.e., 20 dB) for the normalized SVs, a model order of 40 was selected and used by the three methods for signal reconstruction.

![](images/a3658e3f8716774f78d548216e9c2392fd0e50a87a952e0ac497aa41d4237dfc.jpg)  
(a)

![](images/e664262947d5d643ab56f026984561a10e39b4c39efd50e3b76ee4ce1f5bc747.jpg)  
(b)

![](images/028ca5ed11aee99dee19b98d4409aabc2980ed97f2c415033d588c9c562764e6.jpg)  
(c)

![](images/a19e311d7835238a875b111c342cc6803b516025b99a2f1332da9440e30f439d.jpg)  
(d)

Fig. 10. The beat signal acquired in one FMCW sweep for the chimney observation. (a) shows the measured beat signals with (i.e., “sig Int” in the solid red line) and without the cross-polarimetric interference (i.e., “ref sig” in the dashed blue line). (c) presents the signals around the interference-contaminated region after interference mitigation using zeroing, Burg- and MP-based methods while (d) shows the recovered beat signal with the IVM-based method.  
![](images/e4268dd715ea9dda11b4489877440d6d14b4a5f9a606d38da98b112346ecafe8.jpg)  
(a)

![](images/14df523c4c2abadd1319c0e0eaa88ed49cd5c15e668c2194567e52e22d389cc3.jpg)  
(b)

![](images/3f8e3d37cbc2ad00d164796d947374557f43c0af66beea29a998fd55a1d13865.jpg)  
(c)  
Fig. 11. The range profiles of the Chimney scenario obtained with the signals before and after interference mitigation. (a) shows the range profiles of the scenario within 10 km from the radar. (b) and (c) are the zoomed-in views of the range profiles of the targets at the distances of 1.07 km and 4.3 km from the radar, respectively.

Moreover, the range profiles constructed with the interference-contaminated signal, reference signal, the signals acquired after interference mitigation are displayed in Fig. 11(a) (due to invalid signal recovery of the IVM-based method, its RP is omitted). It is clear that the range profile obtained with the interference-contaminated signal has higher “noise floor” in contrast to that formed with other signals, which would mask weak targets. For the convenience of comparison, the close-ups of the range profiles of the chimney at the distance of 1.07 km and some weak targets at the distance of 4.3 km in Fig. 11(a) are shown in Fig. 11(b) and (c). From Fig. 11(c), a clear peak for a weak target at the distance of 4.24 km can be observed in the range profiles generated with the reference signals and the signals acquired after interference mitigation. By contrast, a deep null is seen at the same position in the range profile formed with the interference-contaminated signal, which could be caused by the destructive interference between the interference and the target’s signal. Moreover, the range profiles obtained with signals after mitigating the interference by using Burg- and MP-based methods are comparable to the reference one and have lower sidelobes for the weak targets around the distance of 4.3 km. On the other hand, the range profile of the chimney acquired after processing with the proposed

![](images/ee99b0da9afe55308425989649157afb009e05094786d9adfcb43758a51c1c22.jpg)

Fig. 12. The signals of all the sweeps scattered from rain droplets.  
![](images/9a153ad997d73590a191d889f52166219eab0632a1f03922f3bb30221960e9cc.jpg)

(a)  
![](images/e314eae69f83380a1af0b56f7f453b16104b1ab8d2fe9a46e94dfd14ad344f3a.jpg)  
(b)  
Fig. 13. The time signals at a Doppler bin after taking FFT along the slowtime dimension. (a) and (b) show the time signal before and after interference mitigation.

MP-based interference mitigation is almost identical to the one formed with the reference signal. However, the zeroing caused a void of signal samples and the Burg-based method underestimated signal amplitude in the cut-out region; thus, they cause higher sidelobes and power loss in the constructed range profiles (see the insets in Fig. 11(b)).

## C. Experiment 2: Distributed target (Rain)

In this experiment, we used 512 sweeps as a Coherent Processing Interval (CPI) for full-polarimetric measurements of rain droplets. After simple preprocessing to suppress the direct coupling, the acquired HV-pol signals in all the sweeps are shown in Fig. 12, where the interference-contaminated samples are located in the time interval from 0.4 ms to 0.6 ms. The interference was caused by the VV-pol signals, which are generally much stronger than the desired HV-pol signals (see the much larger amplitudes of the interference-contaminated samples relative the rest ones). So after the range-Doppler (R-D) processing, the formed R-D map of the rain droplets is completely overwhelmed by the interference, as shown in Fig. 14(a).

As the raindrops are moving targets, we suggest first taking the FFT with respect to the slow time in a CPI and then performing the interference mitigation to the time signal along each Doppler bin to avoid the possible detrimental impact of errors caused by interference mitigation on the Doppler information. Fig. 13(a) shows the time signal in a Doppler bin after taking the FFT along the slow time and the interference is still observed in the interval from 0.4 ms to 0.6 ms. Applying the proposed MP-based interference mitigation method, zeroing, Burg- and IVM-based methods to this time signal, the resultant signals are presented in Fig. 13(b). The MPbased method successfully recovers the missing signals in the gap resulting from interference suppression while the Burgand IVM-based methods reconstruct only the missing samples which are close to the front and rear available measurements with underestimated amplitudes. Note that for the rain data set, the SAMOS method could not estimate proper model orders, either. So we empirically determine the model order of the signal in each Doppler bin based on the normalized singular value distribution of the matrix used by SAMOS with a threshold of $1 0 ^ { - 4 }$ . The estimated signal model order was used by the Burg-, IVM- and MP-based methods to reconstruct the signal in the cut-out region.

After mitigating the interferences for the time signals in all Doppler bins, an FFT is taken along the fast time to get the R-D map of the rain drops. Fig. 14(b)-(e) present the obtained R-D maps in logarithmic scale of the moduli of signals after interference mitigation with zeroing, the Burg-, IVM- and MP-based methods, respectively. Except the R-D maps obtained with the IVM-based method, the other three R-D maps are visually almost identical and their qualities are noticeably improved compared to that obtained without interference mitigation (Fig. 14(a)).

Due to the lack of ground truth reference, we alternatively assess the improvement of the R-D maps obtained with the Burg-, IVM- and MP-based methods relative to the one got with zeroing by computing the power differences between the pixels of the R-D maps of the three signal reconstruction methods and zeroing method. The results are shown in linear scale in Fig. 14(f)-(h). One can see that the power difference between the R-D maps of MP-based method and zeroing in Fig. 14(h), compared with that in Fig. 14(f), presents a pattern much closer to the R-D maps in Fig. 14(b), (c), and (e). As in the rain data set the strong VV-pol interferences appear at the similar time interval in all the sweeps within the CPI, the zeroing method eliminates the signal samples within this time interval (i.e., between about 0.4 ms to 0.6 ms) in all the sweeps. So the power difference of the R-D maps of zeroing and the other three methods are determined by the contribution of the beat signal samples in the cut-out region. Theoretically, the beat signals of rain droplets in the cut-out time interval in a CPI can be considered as the acquired data by using an FMCW radar with narrower bandwidth (i.e., shorter FMCW sweep duration) but keep other system parameters unchanged; thus, they can form a similar R-D map as that constructed with the full-sweep signals in the CPI but with lower range resolution. Namely, the more accurate the signal samples recovered by the Burg-, IVM- and MP-based methods in the cut-out region are, the closer to the actual R-D map the pattern of the power difference between the R-D maps of these methods and the zeroing approach. Therefore, the MPbased method gets more accurate estimation of the signals in the cut-out region than the Burg-based method. Furthermore, large portions of the positive power difference in Fig. 14(f) and (h) reveal that compared to the zeroing technique, both Burg- and MP based method improve the signal powers by reconstructing the missing signals in the cut-out region. In addition, due to the instability of the IVM-based method, the blow-ups in its reconstructed signals cause the streaks with very large amplitudes in many Doppler bins (Fig. 14(d)). So the accuracy of the recovered signals by the IVM-based method is worse than that of the Burg- and MP-based methods.

![](images/6866beda0b5589950eebb1b24eea96b789e96fb34d61a958a0ee066b94b50eaa.jpg)  
(a)

![](images/8b5bdc72d0862464d1c32112c8bbd3074d8d3c92e227c14236c733602a80f517.jpg)  
(b)

![](images/7135a4f03c2e689006edda4673f389e85db457407643b58a6b22c0bfe3876df0.jpg)

![](images/fac8d0707c08c628bf7e8e212ad8b956bf4624d8b17971f8e69480024a9da137.jpg)  
(d)

![](images/140ab84cbe15d8bd154fe85707694992458fda75e331b1f2e4a594bd4398e949.jpg)  
(e)

(c)  
![](images/f4d9a43e9e025fd2bdda8de02d22c87f65f503a4e238f99fa249cc058f16335e.jpg)  
(f)

![](images/8cecfa56b4200ab26f40c900857612f040950d551bd8d0d720cb3c4780c23783.jpg)  
(g)

![](images/9e85bb2ad4ade1944b51e48fd1e3b7a658281a3f6a48407999dd8b2e408df022.jpg)  
(h)  
Fig. 14. The range-Doppler processing results of the rain data. (a) is the RD map obtained with the original interference-contaminated signals. (b), (c), (d), and (e) are formed by the signals after interference mitigation by using the zeroing, Burg-, IVM- and MP-based methods, respectively. (f), (g), and (h) show the corresponding power differences between the RD maps in (c)-(e) and (b).

## VI. CONCLUSION

In this paper, we present a matrix-pencil based interference mitigation method for FMCW radar systems. The proposed method exploits the feature of the desired beat signals as a sum of exponential sinusoidal components, which is different from the chirp-like waveforms of interferences after dechirping on reception, for interference suppression. The method is implemented in two steps by first detecting and cutting out the interference-contaminated samples and then recovering the signal samples in the cut-out region based on the exponential sinusoidal model of desired beat signals. It addresses the discontinuity of the signals caused by traditional zeroing technique and overcomes the power loss of useful signals. Meanwhile, it results in lower sidelobes of the range profile of a target. Moreover, compared to the Burg-based method, it significantly improves the accuracy of the estimated signals in the cut-out region by an iterative estimation scheme, which has demonstrated through both numerical simulations and experimental results. The numerical simulations also reveal that the proposed method can robustly work in the scenarios with a low signal to noise ratio (down to 0dB) and with a long interference duration (up to 50% of a sweep). In addition, the proposed MP-based method can be extended to 2D or high-dimensional cases to mitigate interferences directly in a higher dimensional space (e.g., RD or range-DOA domains), especially for point-target scenarios, which would be considered in future work.

## ACKNOWLEDGMENT

The authors acknowledge the contribution of N. Cancrinus to this research by testing applicability of the matrix pencil method to the beat signal reconstruction.

## REFERENCES

[1] J. G. Kim, S. H. Sim, S. Cheon, and S. Hong, “24 GHz circularly polarized Doppler radar with a single antenna,” in 35th European Microwave Conference 2005 - Conference Proceedings, 2005.

[2] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in 2016 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility, ICMIM 2016, 2016.

[3] Y. Kim, “Identification of FMCW radar in mutual interference environments using frequency ramp modulation,” 2016 10th European Conference on Antennas and Propagation, EuCAP 2016, pp. 1–3, 2016.

[4] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “Radchat: Spectrum sharing for automotive radar interference mitigation,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–14, 2019.

[5] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “Radarmac: Mitigating radar interference in self-driving cars,” in 2016 13th Annual IEEE International Conference on Sensing, Communication, and Networking (SECON), June 2016, pp. 1–9.

[6] J. H. Choi, H. B. Lee, J. W. Choi, and S. C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Transactions on Communications, vol. E99B, no. 1, pp. 280–287, 2016.

[7] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, April 2019.

[8] F. Uysal, “Synchronous and Asynchronous Radar Interference Mitigation,” IEEE Access, 2019.

[31] H. Li, G. C. Linderman, A. Szlam, K. P. Stanton, Y. Kluger, and M. Tygert, “Algorithm 971: An implementation of a randomized algorithm for principal component analysis,” ACM Trans. Math. Softw., vol. 43, no. 3, Jan. 2017.

[9] J. Ren, T. Zhang, J. Li, L. H. Nguyen, and P. Stoica, “RFI mitigation for UWB radar via hyperparameter-free sparse spice methods,” IEEE Transactions on Geoscience and Remote Sensing, vol. 57, no. 6, pp. 3105–3118, June 2019.

[32] O. A. Krasnov, G. P. Babur, Z. Wang, L. P. Ligthart, and F. van der Zwan, “Basics and first experiments demonstrating isolation improvements in the agile polarimetric FM-CW radar – PARSAX,” International Journal of Microwave and Wireless Technologies, vol. 2, no. 3-4, p. 419–428, 2010.

[10] B. Tullsson, “Topics in fmcw radar disturbance suppression,” in Radar 97 (Conf. Publ. No. 449), Conference Proceedings, pp. 1–5.

[11] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for fmcw radar using beat-frequencies interpolation in the stft domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, March 2019.

[12] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in 2019 IEEE Radar Conference (RadarConf), Conference Proceedings, pp. 1–6.

[13] G. Babur, “Processing of dual-orthogonal cw polarimetric radar signals,” Ph.D. dissertation, Delft University of Technology, 2009.

[14] G. Babur, Z. Wang, O. A. Krasnov, and L. P. Ligthart, “Design and implementation of cross-channel interference suppression for polarimetric LFM-CW radar,” Photonics Applications in Astronomy, Communications, Industry, and High-Energy Physics Experiments 2010, vol. 7745, p. 774520, 2010.

[15] T. K. Sarkar and O. Pereira, “Using the matrix pencil method to estimate the parameters of a sum of complex exponentials,” IEEE Antennas and Propagation Magazine, vol. 37, no. 1, pp. 48–55, Feb 1995.

[16] Y. Hua and T. K. Sarkar, “Matrix pencil method for estimating parameters of exponentially damped/undamped sinusoids in noise,” IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 38, no. 5, pp. 814–824, May 1990.

[17] Y. Q. Zou, X. Z. Gao, and X. Liand Yong Xiang Liu, “A matrix pencil algorithm based multiband iterative fusion imaging method,” Scientific Reports, vol. 6, p. 19440, 01 2016.

[18] J. Wang, P. Aubry, and A. Yarovoy, “Wavenumber-domain multiband signal fusion with matrix-pencil approach for high-resolution imaging,” IEEE Transactions on Geoscience and Remote Sensing, vol. 56, no. 7, pp. 4037–4049, July 2018.

[19] Y. Hua, “Estimating two-dimensional frequencies by matrix enhancement and matrix pencil,” IEEE Transactions on Signal Processing, vol. 40, no. 9, pp. 2267–2280, 1992.

[20] F. Chen, C. C. Fung, C. Kok, and S. Kwong, “Estimation of twodimensional frequencies using modified matrix pencil method,” IEEE Transactions on Signal Processing, vol. 55, no. 2, pp. 718–724, 2007.

[21] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, 2007.

[22] G. M. Brooker, “Automotive radar-investigation of mutual interference mechanisms,” Advances in Radio Science, 2010.

[23] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” International Journal of Microwave and Wireless Technologies, 2014.

[24] M. H. Hayes, Statistical digital signal processing and modeling. New York: John Wiley & Sons, 1996, pp. 129–198.

[25] M. Kunert, “The eu project mosarim: A general overview of project objectives and conducted work,” in 2012 9th European Radar Conference, Oct 2012, pp. 1–5.

[26] C. Fischer, H. L. Blocher, J. Dickmann, and W. Menzel, “Robust¨ detection and mitigation of mutual interference in automotive radar,” in 2015 16th International Radar Symposium (IRS), June 2015, pp. 143– 148.

[27] S. Murali, K. Subburaj, B. Ginsburg, and K. Ramasubramanian, “Interference detection in fmcw radar using a complex baseband oversampled receiver,” in 2018 IEEE Radar Conference (RadarConf18), April 2018, pp. 1567–1572.

[28] J. Papy, L. D. Lathauwer, and S. V. Huffel, “A shift invariance-based order-selection technique for exponential data modelling,” IEEE Signal Processing Letters, vol. 14, no. 7, pp. 473–476, 2007.

[29] Y. Sun, T. Fei, and N. Pohl, “Two-dimensional subspace-based model order selection methods for fmcw automotive radar systems,” in 2018 Asia-Pacific Microwave Conference (APMC), Conference Proceedings, pp. 1247–1249.

[30] G. Golub and C. Van Loan, Matrix Computations, ser. Johns Hopkins Studies in the Mathematical Sciences. Johns Hopkins University Press, 2013.