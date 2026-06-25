# Interference Mitigation Evaluation Methodology for Automotive Radar

Jihwan Youn<sup>#1</sup>, Jun Li<sup>\$2</sup>, Ryan Wu<sup>\$3</sup>, Jeroen Overdevest<sup>#4</sup>

<sup>#</sup>NXP Semiconductors, The Netherlands

<sup>\$</sup>NXP Semiconductors, USA

{<sup>1</sup>jihwan.youn, <sup>2</sup>jun.li\_5, <sup>3</sup>ryan.wu, <sup>4</sup>jeroen.overdevest}@nxp.com

Abstract — Interference mitigation is crucial to restore the degraded detection performance of interfered radars. For developing advanced interference mitigation methods, a well-defined evaluation methodology is required to assess the performance of different methods thoroughly and appropriately. In this paper, we propose to evaluate interference mitigation methods by measuring detection performance and signal-to-noise ratio in the range-Doppler domain. We especially suggest measuring the performance analytically without involving any detector but based on the estimated probability density functions of the target and background to isolate the effect of the detector in the performance evaluation. The time-domain thresholding and time-frequency domain thresholding methods are compared to validate the proposed methodology on simulated data.

Keywords — interference mitigation, time-frequency domain analysis, radar-to-radar interference

## I. INTRODUCTION

Automotive radar has proven its effectiveness in supporting drivers with advanced driver assistance systems (ADAS), including emergency brake, blind spot detection, adaptive cruise control, and line change assistance. With the development of automotive four-dimensional imaging radar, a higher angular resolution can be achieved, making it a critical component in autonomous driving (AD). However, as the utilization of automotive radar becomes more pervasive, radar-to-radar interference is likely to increase.

Interference can degrade the detection performance of radars, which can result in limiting the downstream ADAS or AD applications. Therefore, it is important to mitigate interference properly to guarantee the capability of these systems. To develop advanced interference mitigation methods, a well-defined evaluation methodology for capturing the detection performance is essential. Such evaluation methodology will help to ensure the detection performance is recovered to an acceptable level, thus enhancing road safety.

Various interference mitigation methods have been proposed recently [1]–[10], and their effectiveness has been evaluated by measuring discrepancies between the interference-free signal and its corresponding interfered signal after interference mitigation. However, these evaluations were often performed on fast-time samples, which can be misleading since they neglect artifacts that can appear after the Doppler processing [6], [11]. Such artifacts will be observable only in the range-Doppler (RD) domain, where actual detection is performed. Some works evaluated the RD map [11], [12], but these evaluations depend on the ability of the detector since the metrics are calculated based on the detections estimated by a detector, such as a constant false alarm rate (CFAR) detector.

![](images/bfe85adafb3b3af1a7e41c501d231be6e77e81485f8b18f9c8e1ad7b4fa5a3a0.jpg)  
Fig. 1. Overview of the transmitted signal (blue), received target signal (green), and interference signal (red).

Here, we propose a new methodology to evaluate interference mitigation that satisfies the requirements of measuring performance in the RD domain without requiring any detector. This involves estimating the probability density functions (PDFs) of the target and background powers with knowing target positions. The background includes noise and potential interference that is not fully canceled by the mitigation methods. Then probability of detection (PD), probability of false alarm (PFA), and signal-to-noise ratio (SNR) are measured from the estimated PDFs. Using the proposed methodology, we evaluate three different thresholding-based interference mitigation methods on simulated data in the highway environment with two different types of interference: uncorrelated interference and highly-correlated interference [12].

## II. BACKGROUND

In this section, we briefly review the frequency modulated continuous wave (FMCW) radar signal model and thresholding-based interference mitigation methods. An overview of the transmitted signal, received target signal, and interference signal is illustrated in Fig. 1.

## A. Signal Model

FMCW automotive radars transmit the linear frequency modulation (LFM) waveform

$$
s _ { l } ( t ) = \left\{ \begin{array} { l l } { \exp \left( j \pi \alpha t ^ { 2 } \right) , } & { \mathrm { i f ~ } 0 < t < T _ { \mathrm { r a m p } } } \\ { 0 , } & { \mathrm { o t h e r w i s e } } \end{array} \right. ,\tag{1}
$$

where $T _ { \mathrm { r a m p } }$ is the chirp duration and $\begin{array} { r } { \alpha = \frac { B } { T _ { \mathrm { r a m p } } } } \end{array}$ is the chirp slope with the sweep bandwidth B. Assuming M chirps are used per coherent processing interval (CPI), the transmitted signal can then be formulated by

$$
\begin{array} { c } { { s _ { t } ( t ) = \displaystyle \sum _ { m = 1 } ^ { M } \bigg \{ s _ { l } \left( t - \left( m - 1 \right) T _ { \mathrm { P R I } } \right) } } \\ { { \exp \left( j 2 \pi f _ { c } \left( t - \left( m - 1 \right) T _ { \mathrm { P R I } } \right) \right) \bigg \} , } } \end{array}\tag{2}
$$

where $f _ { c }$ is the carrier frequency, T<sub>PRI</sub> is the pulse repetition interval (PRI).

## 1) Target Signal

Consider the received signal by a single point target, which is the transmitted signal delayed by $\begin{array} { r } { \tau ( t ) = \frac { \dot { 2 } ( r + v _ { r } t ) } { c } } \end{array}$ and scaled by a complex attenuation factor a. Here, r and $v _ { r }$ denote the radial distance and the relative radial velocity of the target, and $c$ is the speed of light. The received signal can be modeled as follows with approximating the round-trip time to the target as $\begin{array} { r } { \tau ( t ) \approx \tau _ { m } = \frac { 2 ( r + v _ { r } ( m - \overline { { 1 } } ) T _ { \mathrm { P R I } } ) } { c } } \end{array}$

$$
s _ { r } ( t ) = \sum _ { m = 1 } ^ { M } a s _ { t } \left( t - \tau \left( t \right) \right) \approx \sum _ { m = 1 } ^ { M } a s _ { t } \left( t - \tau _ { m } \right) .\tag{3}
$$

At the radar front end (RFE), the received signal is dechirped through the mixer by $s _ { \mathrm { I F } } ( t ) ~ = ~ s _ { r } ( t ) s _ { t } ^ { * } ( t )$ . The dechirped signal is then filtered by a low-pass filter (LPF) and sampled by an analog-to-digital converter (ADC) with a sampling interval of $T _ { s }$ . Let the ADC samples be sampled at time $t = \left( m - 1 \right) T _ { \mathrm { P R I } } + \left( n - 1 \right) T _ { s } ,$ , where $m = \{ 1 , 2 , \cdots , M \}$ $n = \{ 1 , 2 , \cdots , N \}$ , and N is the number of active samples per PRI. The ADC samples for a frame S with a size of $M \times N$ can be represented by

$$
{ \bf S } = ( s _ { m n } ) = a \exp \left( - j 2 \pi \left( \frac { 2 r } { c } f _ { c } + m f _ { d } + n f _ { r } \right) \right) ,\tag{4}
$$

where $\begin{array} { r } { f _ { r } = \frac { 2 r \alpha } { f _ { s } c } } \end{array}$ is the normalized range frequency and $f _ { d } =$ $\frac { 2 f _ { c } T _ { \mathrm { P R I } } v _ { r } } { c }$ is the normalized Doppler frequency.

## 2) Interference Signal

The received interference signal follows the transmitted signal model (2) with different chirp parameters as

$$
\begin{array} { r l r }   { \widetilde { s } _ { r } ( t ) = \sum _ { m = 1 } ^ { \tilde { M } } \Big \{ \widetilde { a } \widetilde { s } _ { l } ( t - ( m - 1 ) \widetilde { T } _ { \mathrm { P R I } } - \widetilde { t } _ { 0 } ) } \\ & { } & { \exp ( j 2 \pi \widetilde { f } _ { c } ( t - ( m - 1 ) \widetilde { T } _ { \mathrm { P R I } } - \widetilde { t } _ { 0 } ) ) \Big \} , } \end{array}\tag{5}
$$

where a˜ is the complex scaling factor, $\tilde { s } _ { l } ( \cdot ) , \tilde { M } ,$ , and $\tilde { f } _ { c }$ are the LFM waveform, the number of chirps per CPI, and the carrier frequency of the interfering radar, respectively, and $\tilde { t } _ { 0 }$ is the time offset between the interfering and victim radars.

Consider one chirp of the perfectly aligned interfered signal at the victim radar’s RFE, i.e., $M = \tilde { M } = 1 , \tilde { f } _ { c } = f _ { c }$ and $\tilde { t } _ { 0 } =$ 0. The dechirped received interference signal is represented by

$$
\begin{array} { r } { \tilde { s } _ { \mathrm { I F } } \left( t \right) = \tilde { s } _ { r } ( t ) s _ { t } ^ { \ast } ( t ) = \tilde { a } \exp \left( j \pi \left( \tilde { \alpha } - \alpha \right) t ^ { 2 } \right) , } \end{array}\tag{6}
$$

![](images/14c9ff065f36e318d2e5d5edb0a9a20626dc3fb8a7d2896797a30276c0eb02fa.jpg)

![](images/b85a0d01e1d4ca8bcae885a0d57ec273c552e40bf27df02467b323b9d111b20e.jpg)

![](images/5c73ce35a8c9b1c3d04e4993904201ff09033e1c4bff7e5f37b642a3acf0ae83.jpg)  
(a)

![](images/f456f6bcb131b44cc80d9c6d49472fe124fdd2ed5fa5f2897b45f8cda36b763f.jpg)  
(b)  
Fig. 2. Received radar signals interfered by (a) highly-correlated interference and (b) uncorrelated interference, represented in the time domain (top) and the time-frequency domain (bottom).

where α˜ is the chirp slope of the interfering radar. From (6), we know that the dechirped interference signal is a chirp signal with a slope of ${ \tilde { \alpha } } - \alpha ,$ which is the chirp slope difference between the interfering and the victim radars. The dechirped interference chirp slope $\tilde { \alpha } - \alpha$ defines the correlation of the interference signal. Based on the degrees of correlation, the interference signals can be categorized into uncorrelated, semi-correlated, or highly-correlated interference [12]. The number of interfered fast-time samples increases as the correlation increases [2], as presented in Fig. 2.

In reality, the timing and duration of interference depend on various factors, such as the chirp parameters of both the victim and interfering radars and the position of the interfering radar, etc. A frame of the interference signal after the ADC, denoted as $\tilde { \mathbf { S } } ,$ can be generalized using a generic function $g \left( \cdot \right)$ [12] by

$$
\begin{array} { c } { \tilde { \mathbf { S } } = ( \tilde { s } _ { m n } ) = \tilde { a } \exp \left( j \pi \left( \tilde { \alpha } - \alpha \right) ( n T _ { s } ) ^ { 2 } \right) } \\ { g \left( m , n , \alpha , \tilde { \alpha } , T _ { \mathrm { P R I } } , \tilde { T } _ { \mathrm { P R I } } , \tilde { t } _ { 0 } \right) . } \end{array}\tag{7}
$$

## 3) Received Signal

The ADC samples of the received target and interference signals for a frame $\mathbf { X } \in \mathbb { R } ^ { M \times N }$ can be represented by

$$
\begin{array} { r } { \mathbf { X } = \mathbf { S } + \tilde { \mathbf { S } } + \mathbf { E } , } \end{array}\tag{8}
$$

where $\mathbf { E } \in \mathbb { R } ^ { M \times N }$ is the white Gaussian noise. Subsequently, the corresponding RD map, represented by $\mathbf { R } \in \mathbb { C } ^ { \bar { N } _ { d } \times N _ { r } }$ is derived through the execution of the range and Doppler processing on the received data X, where $N _ { d }$ is the number of Doppler bins and $N _ { r }$ is the number of range bins.

## B. Thresholding-based Interference Mitigation

Thresholding-based interference mitigation finds thresholds that discriminate interference from target signals and nulls the signals above the thresholds. A CFAR detector [4], [8] or L-statistics [5], [9] can be used to estimate the thresholds, and adaptive thresholding [7], [10] can improve the interference detection. The thresholding-based methods are not only the basis for many advanced interference mitigation methods but also practical as they satisfy the real-time requirements of hardware thanks to their efficiency.

![](images/2a5cdf9dfe5591cc202b663a04818e4bd675313745ce495f6eb490a465f5b406.jpg)  
Fig. 3. Illustration of the proposed detection capability evaluation.

Interference detection and thresholding can be applied in both the time domain (TD) and the time-frequency domain (TFD). Dechirped interference signals have a more organized structure in the TFD since they are still chirps. Therefore, TFD thresholding can minimize the nulling of target signals during interference mitigation, which helps reduce the SNR degradation, especially when interference is highly correlated. As shown in Fig. 2a, many fast-time samples need to be nulled to remove interference in the TD. However, in the TFD, the interference signal can be more selectively nulled. Therefore, TFD thresholding is more robust to the interference correlation, though it does require more computational resources due to the transformation between the TD and TFD.

## III. PERFORMANCE EVALUATION METHODOLOGY

## A. Detection capability

Consider a RD map of the $k ^ { \mathrm { { t h } } }$ test data $\mathbf { R } ^ { k } \in \mathbb { C } ^ { N _ { d } \times N _ { r } }$ Using the true target positions, we can define two masks for detection metric calculation: the target mask $\mathbf { T } ^ { k } \in \mathbb { B } ^ { N _ { d } \times N _ { r } }$ and the background mask $\mathbf { B } ^ { k } \in \mathbb { B } ^ { \breve { N _ { d } } \times N _ { r } }$ , where $\mathbb { B } = \{ 0 , 1 \}$ represents the Boolean domain. The target mask consists of elements representing whether the cells belong to the target or not, represented by 1 or 0. Similarly, the background mask represents the background cells. To ensure that target signals are not regarded as background, guard cells are placed around the targets when defining the background mask. Also, the target masks do not include weak targets whose powers are below the noise level. Therefore, there are a few cells neither target nor background, i.e., $\mathbf { T } ^ { k } + \mathbf { B } ^ { k } \neq \mathbf { 1 }$

The background noise levels can vary across the range bins. Detectors are not affected by these changes as they consider background noise locally along the Doppler dimension. However, when estimating PDFs, we need to look at the entire RD map. Therefore, we first equalize the background levels across the range bins by normalizing each column of the RD map by its background mean power. The background mean power is calculated after removing outliers to exclude any target sidelobes induced by nulling. To calculate the mean without outliers, we can use the trimmean function in MATLAB or the trim\_mean function in the Scipy package in Python as follows:

$$
\begin{array} { r } { { \bf z } ^ { k } = \left( z _ { j } ^ { k } \right) = t r i m m e a n \left( \boldsymbol { B } _ { j } ^ { k } \right) , \forall j = \left\{ 1 , 2 , \cdots , N _ { r } \right\} , } \end{array}\tag{9}
$$

where $\mathbf { z } ^ { k }$ is the mean background powers of the $k ^ { \mathrm { { t h } } }$ test data along the Doppler dimension and $B _ { j } ^ { k }$ is the set of background cell powers for the $j ^ { \mathrm { t h } }$ range bin, i.e.,

$$
\begin{array} { r } { \mathcal { B } _ { j } ^ { k } = \left\{ \left| r _ { i j } ^ { k } \right| ^ { 2 } \Big | 1 \leq i \leq N _ { d } , b _ { i j } ^ { k } = 1 \right\} . } \end{array}\tag{10}
$$

Here, $r _ { i j } ^ { k }$ and $t _ { i j } ^ { k }$ represent the $i ^ { \mathrm { { t h } } }$ row (Doppler) and $j ^ { \mathrm { t h } }$ column (range) element of $\mathbf { R } ^ { k }$ and $\mathbf { T } ^ { k }$ . The equalized RD map $\tilde { \mathbf { R } } ^ { k }$ is obtained by

$$
\tilde { \mathbf { R } } _ { : j } ^ { k } = \frac { \mathbf { R } _ { : j } ^ { k } } { \sqrt { z _ { j } } } , \forall j = \left\{ 1 , 2 , \cdots , N \right\} .\tag{11}
$$

After the equalization, two sets $\tilde { \tau }$ and ${ \tilde { B } } ,$ comprised of the target cell powers and the background cell powers, respectively, are created by

$$
\tilde { \mathcal { T } } = \left\{ \left| \tilde { r } _ { i j } ^ { k } \right| ^ { 2 } \Big | 1 \leq i \leq N _ { d } , 1 \leq j \leq N _ { r } , 1 \leq k \leq K , t _ { i j } = 1 \right\}\tag{12}
$$

and

$$
\tilde { \mathcal { B } } = \left\{ \left| \tilde { r } _ { i j } ^ { k } \right| ^ { 2 } \Big | 1 \leq i \leq N _ { d } , 1 \leq j \leq N _ { r } , 1 \leq k \leq K , b _ { i j } = 1 \right\} ,\tag{13}
$$

where K is the number of frames. Then the target power PDF $f _ { \tilde { T } } \left( \cdot \right)$ and the background power PDF $f _ { \tilde { B } } \left( \cdot \right)$ can be estimated from the histograms created using $\tilde { \tau }$ and B<sup>˜</sup>.

Now we can calculate PD and PFA from the estimated PDFs. Firstly, we find the threshold $\rho$ that achieves the desired operating PFA, at which we want to calculate PD, by solving

$$
\rho = 1 - F _ { \tilde { \cal B } } ^ { - 1 } \left( p _ { f a } \right) ,\tag{14}
$$

where $F _ { \tilde { B } } \left( b \right)$ is the cumulative distribution function (CDF) of the background powers [13]. And then, PD can be calculated by

$$
p _ { d } = \int _ { \rho } ^ { \infty } f _ { \widetilde { \gamma } } \left( t \right) \mathrm { d } t = 1 - F _ { \widetilde { \gamma } } \left( \rho \right) ,\tag{15}
$$

where $F _ { \widetilde { T } } \left( t \right)$ is the CDF of the target powers [13]. The proposed detection capability calculation overview is presented in Fig. 3.

We focus on measuring PDs at required PFAs, which allows for comparing the detection performance at the same operating points. However, the estimated PDFs can be utilized in various ways. For instance, it is possible to obtain the receiver operating characteristic (ROC) curve from the estimated PDF and measure the area under the ROC curve.

## B. Signal-to-noise Ratio

For SNR calculation, we employ target masks that include all the ground true targets, denoted as $\bar { \mathbf { T } } ,$ without background equalization, unlike detection metrics. Given RD maps and their corresponding target and background masks, another two sets of target and background cell powers are created by

$$
\mathcal { T } = \left\{ \left| r _ { i j } ^ { k } \right| ^ { 2 } \Big | 1 \leq i \leq N _ { d } , 1 \leq j \leq N _ { r } , 1 \leq k \leq K , \bar { t } _ { i j } = 1 \right\}\tag{16}
$$

and

$$
\begin{array} { r } { \mathcal { B } = \left\{ \left| r _ { i j } ^ { k } \right| ^ { 2 } \Big | 1 \leq i \leq N _ { d } , 1 \leq j \leq N _ { r } , 1 \leq k \leq K , b _ { i j } = 1 \right\} . } \end{array}\tag{17}
$$

Then the target and background power PDFs, $f _ { T } \left( \cdot \right)$ and $f _ { B } \left( \cdot \right)$ are estimated from $\tau$ and $B ,$ , and SNR is calculated as follows:

$$
\frac { \mathbb { E } \left[ \mathcal { T } \right] } { \mathbb { E } \left[ \mathcal { B } \right] } = \frac { \int _ { - \infty } ^ { \infty } t f _ { \mathcal { T } } \left( t \right) \mathrm { d } t } { \int _ { - \infty } ^ { \infty } b f _ { \mathcal { B } } \left( b \right) \mathrm { d } b } ,\tag{18}
$$

where $\mathbb { E } \left[ \cdot \right]$ is the expectation operator.

Clean (S1)   
Interfered (S1)   
TD (S1)   
ATD (S1)   
ATFD (S1) Clean (S2)   
Interfered (S2) TD (S2)   
ATD (S2) <sub>5 6 7</sub>ATFD (S2)

![](images/977fe6214a141a355e79f2057cc8a07aa27a83974490496b85c492fae1fcc6fb.jpg)  
(a)

![](images/4763249b260293b1386e67a4fa3a2822a11a34cd91710eb541f4275668fc965a.jpg)  
(b)

![](images/d1b3e0e16785154c5bf185e720e1f3a9295ff791fb296d94cd17d357ab6f8539.jpg)  
(c)  
Fig. 4. Evaluation results on different numbers of interference with time-domain thresholding (TD), adaptive time-domain thresholding (ATD), and adaptive time-frequency domain thresholding (ATFD): the detector-less PD at the PFA of (a) $1 1 \times 1 0 ^ { - 4 }$ and (b) $1 \times 1 0 ^ { - 3 }$ , and (c) SNR. The dashed line and solid line represent the first Scenario (S1) and the second scenario (S2), respectively. Note that the dashed and solid blue lines are aligned.

## IV. NUMERICAL RESULTS

We have evaluated three different interference mitigation methods using the proposed evaluation methodology on a large set of simulated data. The evaluated methods are TD thresholding, adaptive TD thresholding, and adaptive TFD thresholding. We simulated the data using two highway scenarios from a previous study by Li et al. [12]. The first scenario (S1) involved uncorrelated interference, while the second scenario (S2) involved highly-correlated interference. In each scenario, the number of interfering radars varied from zero to nine, and 100 frames were generated for each number of interference.

The detection capabilities and SNR obtained by the proposed evaluation methodology are presented in Fig. 4. As the number of interfering radars increases, the interference signal becomes more complex, making it more challenging to mitigate. All the metrics show a decrease in performance as the number of interfering radars increases.

Comparing different methods, adaptive TFD thresholding is overall the most effective with adaptive TD thresholding performing better than TD thresholding. Moreover, the performance gap between the TFD method and TD methods is more notable in S2 than in S1. This is because the TFD method is capable of handling both uncorrelated and highly-correlated interference, unlike the TD methods.

While SNR in Fig. 4c provides a great overview, PD and PFA provides a more detailed view of the performance of different methods. Specifically, for S1, the detection-less PD in Fig. 4a indicates that the TFD method is beneficial when the tolerance for false detection is low, whereas the TD methods and TFD method perform similarly when the tolerance for false detection is high as seen in Fig. 4b.

## V. CONCLUSION

We have developed an evaluation methodology to assess the effectiveness of interference mitigation methods in automotive radar systems. Our methodology considers any potential distortions that may occur in the RD domain, and removes the effects of detection to ensure a fair assessment of the interference mitigation methods. To achieve this, the target and background power PDFs are estimated from the RD maps, and then the detection metrics at the required operating point and SNR are extracted from the estimated PDFs. We validated the evaluation methodology by comparing three different interference mitigation techniques. The results showed that as the interference correlation increased, the TFD thresholding method performed better than the TD methods, which was in line with our expectations. Our proposed evaluation methodology can be used to compare different interference mitigation methods and help the development of advanced algorithms for interference mitigation in automotive radar systems.

## ACKNOWLEDGEMENT

This result is part of the IPCEI ME/CT and is funded by the Dutch Ministry of Economic Affairs and Climate Policy.

## REFERENCES

[1] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” IEEE, Oct. 2017, pp. 90–93.

[2] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in 2018 IEEE Radar Conference (RadarConf18), 2018, pp. 0405–0410.

[3] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” IEEE, May 2018, pp. 1–4.

[4] F. Laghezza, F. Jansen, and J. Overdevest, “Enhanced interference detection method in automotive FMCW radar systems,” IEEE, Jun. 2019, pp. 1–7.

[5] R. Muja, A. Anghel, R. Cacoveanu, and S. Ciochina, “Interference mitigation in FMCW automotive radars using the short-time Fourier transform and L-statistics,” IEEE, Mar. 2022, pp. 1–6.

[6] J. Overdevest, A. Koppelaar, M. Bekooij, J. Youn, and R. van Sloun, “Signal reconstruction for FMCW radar interference mitigation using deep unfolding,” IEEE, Jun. 2023, pp. 1–5.

[7] J. Overdevest and F. Laghezza, “Radar interference detection,” U.S. Patent 18 081 169, Aug. 10, 2023.

[8] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Transactions on Intelligent Transportation Systems, vol. 23, pp. 12 229–12 238, 8 Aug. 2022.

[9] R. H. Wu, J. Li, M. Brett, and M. A. Staudenmaier, “Radar communication with interference suppression,” U.S. Patent 17 245 613, Nov. 3, 2022.

[10] R. H. Wu, J. Li, and C. Tuschen, “Radar communication with interference suppression,” U.S. Patent 18 453 931, Dec. 7, 2023.

[11] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” IEEE, Apr. 2019, pp. 1–6.

[12] J. Li, J. Youn, R. Wu, J. Overdevest, and S. Sun, “Performance evaluation and analysis of thresholding-based interference mitigation for automotive radar systems,” 2024. arXiv: 2402.14018 [eess.SP].

[13] M. A. Richards, Fundamentals of Radar Signal Processing. McGraw-Hill Professional, 2005.