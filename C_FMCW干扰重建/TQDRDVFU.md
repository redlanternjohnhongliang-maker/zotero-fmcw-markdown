#

Yunxuan Wang, Yan Huang , Member, IEEE, Cai Wen , Member, IEEE, Xiao Zhou, Jiang Liu, Student Member, IEEE, and Wei Hong , Fellow, IEEE

Abstract— Currently, the frequency-modulated continuouswave (FMCW) millimeter-wave (MMW) radar is a typical choice for automotive and transportation radar systems. As the number of FMCW radars explodes in the current vehicle market and the working frequency is limited in an open window of 76–81 GHz, FMCW radars on the road easily mutually interfere with each other, especially due to their wide bandwidth. Hence, in this article, we rigorously analyze the target echo, i.e., the beat signal, especially the sparsity of the interference signal in the time domain, and the row sparsity of the useful echo signal in the frequency domain. By taking advantage of this feature, we design an interference mitigation optimization problem to extract the target echoes with a row-sparse constraint. A closed-form solution is given in each iteration with specific derivations. Finally, numerical simulations and multiple practical scenes are provided to demonstrate the effectiveness of the proposed method.

Index Terms— Automotive frequency-modulated continuouswave (FMCW) radar, interference mitigation, low-rank recovery, row sparse.

## I. INTRODUCTION

ELF-DRIVING vehicles require an overall perception of Sthe surroundings by the control center in the driver system in full time [1], [2], [3]. Multiple kinds of sensors, including cameras, LiDAR, satellite navigation, network ranges, and infrared sensors with their respective features, have already shown great potential in different circumstances. However, most of them cannot robustly work in all conditions of weather and sunlight with accurate targets’ positions. Radar systems can analyze the echoes reflected by targets with the transmitted electromagnetic signal to obtain useful information about the target, such as range and velocity, or even the angle if the radar has multiple channels [4], [5]. The automotive radars, which are installed on cars, can provide signs of obstacles in a long working range, no matter the existence of rainy days or dark nights [6], making it a unique tool for real driving circumstances.

Currently, typical automotive radars operate on the mode of frequency-modulated continuous-wave (FMCW) signals [7], and their carrier frequencies are commonly within the millimeter-wave band, such as 76–81 GHz. The FMCW radar system transmits a sequence of analog-generated chirps that are then reflected from targets to the system’s receivers. After mixing with the local reference, the beat signal is obtained with its beat frequency, which is proportional to the target distance. The chirps in FMCW radar are commonly designed to be short enough so that the distance-induced component of the beat frequency predominates the received signal. However, since FMCW automotive radars are assigned to work in the same frequency band by the International Telecommunication Union (ITU), then the sudden surge in the number of FMCW radars currently raises serious concerns about their mutual interferences [8]. Because of the wide bandwidth and special characteristics of the FMCW signal, the mutual interference will generate ghost targets, mask weak targets, and disturb target returns. Previous researchers proposed many interference mitigation methods, which can be classified into two categories, i.e., system design approaches [9], [10] and signal processing methods.

System design approaches require specific hardware support. For example, delicate waveform designs [11] and antenna array designs [12] are common system design approaches, which require the waveform modulation capability at the transmitter [13], and will surely increase the complexity of the whole radar system. Signal processing methods, on the other hand, could be readily used for the existing FMCW systems, and the postprocessing progress can be integrated into the baseband processor. Note that the work presented in this article is a signal-processing method for mutual interference mitigation of the FMCW radar system.

In regard to signal processing methods, they can be further categorized into three classes: 1) filtering approaches [14], [15], [16], [17], including frequency domain filtering and space domain filtering; 2) interference nulling and reconstruction methods [19], [20], [21]; and 3) signal separation methods [22], providing feasible separation of the useful signal and interference in a certain domain.

Through the filtering approach, certain types of interference in a point-like target scenario can be perfectly mitigated [14]. The performance of filtering approaches is restricted to complicated scenarios with multiple targets or interference sources. For the adaptive filtering approach, a reference input is required to generate the correlated interference component for interference mitigation [15], [16]. Since the proper reference input signal is not often easy to be known before, the performance of the filtering approach cannot be guaranteed. Also, spatial filters, which take advantage of the spatial location of the targets and aggressor radars, are quite useful in the phased-array radar system [18] but not a universal solution for all automotive radar systems [17], [23]. Besides, when it comes to the case with unusual aggressors and targets, the spatial filter methods would degrade the performance [24], which indicates the vulnerability in unconventional scenes.

If the interference only contaminates a certain region of one specific domain, the intuitive way is to detect and cut out the interference-contaminated parts [19]. In fact, nulling methods [21], focusing on different nulling start and end time sample points, are effective in practical applications. However, nulling methods may affect the accuracy of further target detection due to the information loss of useful echo signals after nulling. Then, the reconstruction methods were proposed to recover the loss of useful signals. Common methods include model parameter estimation in fast time or slow time domain [25] and generative adversarial network (GAN) methods [26] to reconstruct the interference contaminated part. However, all these methods do perform not as well as the expectation once the contaminated duration is relatively longer than a threshold, like in multi-interference cases. In addition, the interference nulling relies on the detection performance, which is dependent on the detection threshold, making them unable to remove interference thoroughly without a proper threshold.

The signal separation methods are based on the assumption that useful signals and interferences can be separated in a different domain, such as the frequency domain and the time–frequency domain, for optimal decomposition. The separation methods require some prior information about the desired signal [22] for the finding of the bases, which is a tricky task. However, once the proper base is figured out, the performance would be robust for multiple interference sources. Previous studies were proposed based on different particular circumstances and signal features, such as sparse recovery [27], [28] and Hankel matrix [29]. Few of them focus on commercial real sampling automotive radar systems and analyze the differences between useful signals and interferences in detail.

Therefore, in this article, we propose a novel interference mitigation method, which belongs to the signal separation category, based on different characteristics of mutual interferences and useful echoes in different domains. Specifically, we first rigorously derive the formulations of useful echoes and mutual interferences. After that, we further explore their features in both time and frequency domains. Then, we construct an interference mitigation problem to decompose the interference and the useful echoes. Herein, the interference is observed to be sparse in the time domain under the assumption that the victim radar and aggressor radar have different chirp slopes that are commonly true in most cases. Also, the strong scatter in useful echoes is sparse in a row in the frequency domain since strong scatter stays in the same range cell within limited snapshots of one frame. For automotive radars, there are commonly 64 or 128 snapshots in one frame. Then, we introduce a row-sparse constraint to constrain the spectral sparsity of real echoes in the frequency domain and simultaneously constrain the sparsity of interferences in the time domain. Through the alternating direction method of multipliers (ADMM), the above optimization problem can be efficiently solved.

Instead of notching the contaminated part of the interferences pulse by pulse, we take all-pulse received signals together into consideration. It surely has greater potential for complicated interference scenarios and target detection. The proposed method is applied to both simulations and real experiments to demonstrate its effectiveness.

The main contributions of this article can be summarized in three aspects. First, we derive the formulations of useful echoes and mutual interferences. Then, we further explore their features in the time and frequency domains. Second, we construct a novel interference mitigation problem to decompose the sparse interference in the time domain and the row-sparse useful echoes in the frequency domain. Then, we solve the problem through the ADMM with full consideration of the characteristics of both interferences and echo signals. Third, we consider the effects of different SINRs, frequency slopes, and circumstances on the proposed method. We give the corresponding experimental results, where numerous field experiments are implemented to demonstrate the effectiveness of the proposed method.

Notations: Throughout this article, we denote matrices by boldface capital letters, e.g., A. Vectors are denoted by boldface lowercase letters, e.g., a, and scalars are denoted by lowercase letters, e.g., a. For a matrix $\mathbf { A } \in \mathbb { C } ^ { N _ { 1 } \times N _ { 2 } }$ , we denote its $( n _ { 1 } , n _ { 2 } )$ th entry as ${ \bf A } _ { n _ { 1 } , n _ { 2 } }$ . The notations $\mathbf { A } _ { j , \ l }$ : and $\mathbf { A } _ { : , j }$ are used to denote the jth row and column, respectively.

## II. SIGNAL MODEL

## A. Transmitted Signal and Target Echo

This section presents the signal model of a W -band automotive radar system transmitting the FMCW waveform. Rather than the pulse radar, the CW radar is commonly adopted for automotive radars, owing to the fact that the CW radar can provide high-range resolution at a low cost. The transmitted FMCW signal [30] in the ramp time can be presented as

$$
s _ { t } \left( t , \hat { t } \right) = \exp \left( j 2 \pi f _ { c } t + j \pi \gamma \hat { t } ^ { 2 } \right)\tag{1}
$$

where $\gamma$ is the chirp rate, $f _ { c }$ is the carrier frequency, t is the full time, t<sup>ˆ</sup> is the fast time, $t = t _ { m } + \hat { t }$ , and $t _ { m }$ is the slow time. Assuming that the radial velocity of the target relative to the radar is $v ,$ then the instantaneous range between the target and the radar is

$$
R ( \hat { t } , t _ { m } ) = R ( t _ { m } ) - v \hat { t }\tag{2}
$$

where $R ( t _ { m } ) = R _ { 0 } - v t _ { m }$ and $R _ { 0 }$ is the starting range. Then, the delay between the received signal and the transmitted signal can be expressed as

$$
\tau = \frac { 2 R ( \hat { t } , t _ { m } ) } { c }\tag{3}
$$

where $c$ is the speed of the electromagnetic wave. Accordingly, the echo signal can be given as

$$
\begin{array} { l } { s _ { r } ( t , \hat { t } ) = s _ { t } ( t - \tau , \hat { t } - \tau ) } \\ { \qquad = \exp \bigl [ j 2 \pi f _ { c } ( t - \tau ) + j \pi \gamma ( \hat { t } - \tau ) ^ { 2 } \bigr ] . } \end{array}\tag{4}
$$

In practical systems, the dechirp processing is necessary for CW signals and is commonly operated by mixing the received signals with the conjugate of the transmitted one. The resultant signal, named the beat frequency signal, can be formulated as

$$
\begin{array} { r l } & { s _ { \mathrm { \scriptscriptstyle { F } - e x h o } } ( \hat { t } , t _ { m } ) } \\ & { \quad = s _ { t } ( t - { \tau _ { \mathrm { e x h o } } } , \hat { t } - { \tau _ { \mathrm { e x h o } } } ) \times s _ { t } ^ { * } ( t , t _ { m } ) } \\ & { \quad = \mathrm { e x p } \Bigg [ - j 4 \pi f _ { c } \frac { R ( t _ { m } ) } { c } \Bigg ] \mathrm { e x p } \Bigg [ j \frac { 4 \pi \gamma } { c ^ { 2 } } R ^ { 2 } ( t _ { m } ) \Bigg ] } \\ & { \quad \quad \times \mathrm { e x p } \Bigg [ - j \frac { 4 \pi \gamma } { c } \hat { t } \bigg ( R ( t _ { m } ) - \frac { f _ { c } } { \gamma } v + 2 \frac { R ( t _ { m } ) v } { c } \bigg ) \Bigg ] } \\ & { \quad \quad \times \mathrm { e x p } \Bigg [ j \frac { 4 \pi \gamma v \hat { t } ^ { 2 } } { c } + j \frac { v ^ { 2 } 4 \pi \gamma } { c ^ { 2 } } \hat { t } ^ { 2 } \Bigg ] . } \end{array}\tag{5}
$$

Herein, the first-order term of $\hat { t } ,$ which is related to not only $R ( t _ { m } )$ but also two additional terms $- ( f _ { c } / \gamma ) v \ + $ $2 ( ( R ( t _ { m } ) v ) / c )$ , determines the position of the target in each frequency sweep period. According to practical parameters, such as $f _ { c } = 7 6 . 5$ GHz, $B = 5 0 0$ MHz, $\gamma = 5 ~ \mathrm { M H z } / \mu \mathrm { s }$ $v \ < \ 1 0 0 \ \mathrm { m / s } ,$ and $R ~ < ~ 2 0 0 ~ \mathrm { ~ m ~ }$ , it can be calculated that $- ( f _ { c } / \gamma ) v \ \approx \ 0 . 3$ m and $2 ( ( R ( t _ { m } ) v ) / c )$ ≈ 0.01 m. Hence, the second term can be ignored. Basically, the second-order term of t<sup>ˆ</sup> will widen the mainlobe of the range profile. Herein, exp[ $j ( ( 4 \pi \gamma v ) / c ) t ^ { 2 } + j ( ( 4 \pi \gamma ) / c ^ { 2 } ) v ^ { 2 } \hat { t } ^ { 2 } ]$ corresponds to bandwidth $( 4 v / c ) B \approx 7 0$ Hz, and $\exp [ j ( ( 4 \pi \gamma ) / c ^ { 2 } ) v ^ { 2 } \hat { t } ^ { 2 } ]$ corresponds to bandwidth $( 4 v ^ { 2 } / c ^ { 2 } ) B \approx 1$ Hz. The frequency domain sampling interval is $( F _ { s } / N ) \approx 5 0$ kHz, which makes the range mainlobe broadening negligible. Therefore, (5) can be approximated as

$$
\begin{array} { r l r } & { } & { s _ { \mathrm { r - e c h o } } ( \hat { t } , t _ { m } ) \approx \exp \biggl [ - j 4 \pi f _ { c } \frac { R ( t _ { m } ) } { c } \biggr ] \exp \biggl [ j \frac { 4 \pi \gamma } { c ^ { 2 } } R ^ { 2 } ( t _ { m } ) \biggr ] } \\ & { } & { \times \exp \biggl [ - j \frac { 4 \pi \gamma } { c } \hat { t } \biggl ( R ( t _ { m } ) - \frac { f _ { c } } { \gamma } v \biggr ) \biggr ] . } \end{array}\tag{6}
$$

Received echo signals need preprocessing before parameter estimation. For FMCW signals, fast Fourier transform (FFT) on both fast time and slow time is essential for further signal processing [31]. We perform the inverse FFT (IFFT) on t<sup>ˆ</sup> in (6); then, we have

$$
\begin{array} { r l } & { s _ { \mathrm { r - e c h o } } ( f _ { r } , t _ { m } ) = \mathrm { F F T } _ { \hat { t } } \big \{ s _ { \mathrm { r - e c h o } } ( t , \hat { t } ) \big \} } \\ & { \qquad = \mathrm { s i n c } \Bigg ( T _ { p } \Bigg ( f _ { r } - 2 \frac { R ( t _ { m } ) - \frac { f _ { c } } { \gamma } v } { c } \Bigg ) \Bigg ) } \\ & { \qquad \times \exp \Bigg [ - j 4 \pi f _ { c } \frac { R ( t _ { m } ) } { c } \Bigg ] \exp \Bigg [ j \frac { 4 \pi \gamma } { c ^ { 2 } } R ^ { 2 } ( t _ { m } ) \Bigg ] } \end{array}\tag{7}
$$

![](images/cfd953d791589f6e97931d0d944d09dd8e77a62f52f16cfe5e510bd4560d4144.jpg)  
Fig. 1. FMCW RD map.

![](images/bc82dbcf193b08819cfbfe5086865f8cd133d2f22af78d4f934da68a3b34908c.jpg)  
Fig. 2. FMCW range and velocity estimation theory.

where $T _ { p }$ represents the chirp duration and the envelope term is offset with $( f _ { c } / \gamma ) v$ , which is corresponding to the Doppler frequency in a chirp duration $f _ { d } = - ( f _ { c } / c ) ( ( d R ( \widehat { t } , t _ { m } ) ) / ( d \widehat { t } ) )$ . We perform FFT on the slow time $t _ { m }$ as follows:

$$
\begin{array} { r l } & { s _ { \mathrm { r - e s h o } } ( f _ { r } , f _ { d } ) } \\ & { \quad = \mathrm { F F I } _ { t r } \left\{ s _ { \mathrm { r - e s h o } } ( f _ { r } , t _ { m } ) \right\} } \\ & { \quad = \mathrm { s i n c } \Bigg ( T _ { p } \Bigg ( f _ { r } - 2 \frac { R ( t _ { m } ) - \frac { f _ { c } } { \gamma } v } { c } \Bigg ) \Bigg ) } \\ & { \quad \quad \times \mathrm { s i n c } \Bigg ( T _ { a } \left( f _ { d } - \frac { 2 f _ { c } v } { c } \right) \Bigg ) } \\ & { \quad \quad \times \mathrm { e x p } \Bigg [ - j 4 \pi f _ { c } \frac { R _ { 0 } } { c } \Bigg ] \exp \Bigg [ j \frac { 4 \pi \gamma } { c ^ { 2 } } R ^ { 2 } ( t _ { m } ) \Bigg ] . } \end{array}\tag{8}
$$

Up until now, the range-Doppler (RD) image of the FMCW radar can be obtained, as shown in Fig. 1, where the bright points are targets. Herein, both range and velocity information can be obtained from (8) since the sinc(x) function reaches its maximum when $x = 0 ;$ ; then, we have

$$
f _ { r } ^ { * } = 2 \frac { R ( t _ { m } ) - \frac { f _ { c } } { \gamma } v } { c }
$$

$$
f _ { d } ^ { * } = \frac { 2 f _ { c } v } { c }\tag{9}
$$

(10)

where the notations $f _ { r } ^ { * }$ and $f _ { d } ^ { * }$ are frequency shifts on fast time and slow time, which are proportional to the distance and speed of the target, respectively. The results can be easily explained in Fig. 2, where the RD estimation theory of the FMCW signal is shown. Range is presented by time delay $\tau = ( 2 R / c )$ , and velocity can be calculated by the Doppler shift $f _ { D } = - ( 2 v / \lambda )$

## B. Mutual Interference Signal

Currently, automotive FMCW radars face various interferences due to the rapid increase in the number of automotive radars and the fixed allocation of legal frequency bands. As illustrated in Fig. 3, the mutual interferences can be roughly classified as three cases [32].

![](images/81a3cd240fd3736ef725c5251bd663f2a5d12f5f8693c1d9b8f72888a4dfc0d8.jpg)  
Fig. 3. Three cases of mutual interferences. The blue dotted line is the transmitted signal, the green solid line is the received echoes, and the red dashed line is the mutual interference. (a) Contaminated by FMCW interference with the same frequency slope. (b) Contaminated by FMCW interference with a different frequency slope. (c) Contaminated by CW interference with a constant frequency.

1) Case 1: FMCW radar contaminated by FMCW interfer ence with the same frequency slope.

2) Case 2: FMCW radar contaminated by FMCW interference with a different frequency slope.

3) Case 3: FMCW radar contaminated by CW interference.

In Case 1, the frequency slopes of target echoes and interferences are identical; hence, it might be mistaken as a strong ghost target. The common mitigation algorithm for this case involves clutter mitigation. Note that Fig. 3 just illustrates the relationship between the useful echo and interference. The “red dash” interference and the “green solid” echo may not synchronize with each other. Also, we have to point out that Case 2 presents all kinds of different frequency slopes of the aggressor radar, not only the negative frequency slope of the victim radar. Besides, in a more advanced system, Case 3 can be mitigated before downconversion. In Cases 2 and 3, since the frequency slope of the interference is different from that of the transmitted signal or is equal to 0, the beat frequency will not be a constant after the dechirp processing [33], [34].

In practical applications, we consider Case 2 as the most common circumstance [35], that is, another automotive FMCW radar with a different frequency slope transmits its signal directly to the victim radar without any reflection, as the red dotted interference line shown in Fig. 4. The green solid line is a presentation of the target echo of a pedestrian.

The weak target would be submerged under strong interferences and the delay of the interference $\tau _ { \mathrm { i n t e r } }$ that an interfering signal generated from an interferer at the same range as the target occurs at half the delay of the target signal [36], i.e., ${ \tau } _ { \mathrm { i n t e r } } = ( ( R _ { \mathrm { A } } ( \hat { t } , t _ { m } ) ) / c )$ . Thus, the interference signal can be expressed as

$$
\begin{array} { r l r } { \ } & { } & { s _ { r } ^ { \prime } ( t , \hat { t } ) = s _ { t } ( t - \tau _ { \mathrm { i n t e r } } , \hat { t } - \tau _ { \mathrm { i n t e r } } ) } \\ & { } & { ~ = \exp \bigl [ j 2 \pi f _ { c } ( t - \tau _ { \mathrm { i n t e r } } ) + j \pi \gamma ^ { \prime } ( \hat { t } - \tau _ { \mathrm { i n t e r } } ) ^ { 2 } \bigr ] } \end{array}\tag{11}
$$

where $\gamma ^ { \prime }$ is the frequency slope of the mutual interference. Since the echo signal and interference are in the same frequency band, the FMCW radar system will receive both of them and mix the interference signals with the conjugate of the transmitted one for the dechirp processing. The resultant signal can be formulated as

$$
\begin{array} { r l } & { s _ { \mathrm { r - i n t e r } } ( t , \hat { t } ) } \\ & { \quad = s _ { t } ( t - \tau _ { \mathrm { i n t e r } } , \hat { t } - \tau _ { \mathrm { i n t e r } } ) \times s _ { t } ^ { * } ( t , t _ { m } ) } \end{array}
$$

![](images/893a3810fdd590c275acb31415ba566440f8fecc0d967bf09422f892537b1d79.jpg)  
Fig. 4. Interference circumstance.

$$
\begin{array} { r l } & { = \mathrm { e x p } \Bigg [ - j 2 \pi f _ { c } \frac { R _ { \Lambda } ( t _ { n } ) } { c } \Bigg ] } \\ & { \quad \times \mathrm { e x p } \Bigg [ - j \frac { 2 \pi \gamma ^ { \prime } } { c } \hat { t } \bigg ( R _ { \Lambda } ( t _ { n } ) - \frac { f _ { c } } { \gamma ^ { \prime } } v + \frac { R _ { \Lambda } ( t _ { n } ) v } { c } \bigg ) \Bigg ] } \\ & { \quad \times \mathrm { e x p } \Bigg [ \frac { j 2 \pi \gamma ^ { \prime } v \hat { t } ^ { 2 } } { c } + j \frac { v ^ { 2 } \pi \gamma ^ { \prime } } { c ^ { 2 } } \hat { t } ^ { 2 } \Bigg ] \mathrm { e x p } \Bigg [ j \frac { \pi \gamma ^ { \prime } } { c ^ { 2 } } R _ { \Lambda } ^ { 2 } ( t _ { n } ) \Bigg ] } \\ & { \quad \times \mathrm { e x p } [ j \pi ( \gamma ^ { \prime } - \gamma ) \hat { t } ^ { 2 } ] } \\ & { \approx \mathrm { e x p } [ j \pi ( \gamma ^ { \prime } - \gamma ) \hat { t } ^ { 2 } ] \mathrm { e x p } \Bigg [ - j 2 \pi f _ { c } \frac { R _ { \Lambda } ( t _ { n } ) } { c } \Bigg ] } \\ & { \quad \times \mathrm { e x p } \Bigg [ - j \frac { 2 \pi \gamma ^ { \prime } } { c } \hat { t } \bigg ( R _ { \Lambda } ( t _ { n } ) - \frac { f _ { c } } { \gamma ^ { \prime } } v \bigg ) \Bigg ] \mathrm { e x p } \Bigg [ j \frac { \pi \gamma ^ { \prime } } { c ^ { 2 } } R _ { \Lambda } ^ { 2 } ( t _ { n } ) \Bigg ] . } \end{array}\tag{12}
$$

The second-order phase term of the resultant interference cannot be accurately filtered, and the residual phase term would be clearly different from the original transmitted one. Next, we will analyze the time and frequency features of both interferences and target echoes.

## C. Time and Frequency Analysis

The received signal of interference-contaminated automotive FMCW radar can be expressed as

$$
\mathbf { Y } \bigl ( \hat { t } , t _ { m } \bigr ) = \mathbf { S } \bigl ( \hat { t } , t _ { m } \bigr ) + \mathbf { M } \bigl ( \hat { t } , t _ { m } \bigr ) + \mathbf { N } \bigl ( \hat { t } , t _ { m } \bigr )\tag{13}
$$

where S is the beat signal of targets, M is the mutual interference, which is the FMCW signal transmitted by other automotive radars, and N represents the white Gaussian noise. Suppose that there are N samples in one chirp and K chirps are recorded in one frame; then, we have

$$
\begin{array} { r l } & { \mathbf S = [ \mathbf s [ 0 ] , \mathbf s [ 1 ] , \dots , \mathbf s [ K - 1 ] ] \in \mathbb C ^ { N \times K } } \\ & { \mathbf M = [ \mathbf { m } [ 0 ] , \mathbf { m } [ 1 ] , \dots , \mathbf { m } [ K - 1 ] ] \in \mathbb C ^ { N \times K } } \\ & { \mathbf N = [ \mathbf { n } [ 0 ] , \mathbf { n } [ 1 ] , \dots , \mathbf { n } [ K - 1 ] ] \in \mathbb C ^ { N \times K } } \\ & { \mathbf Y = [ \mathbf { y } [ 0 ] , \mathbf { y } [ 1 ] , \dots , \mathbf { y } [ K - 1 ] ] \in \mathbb C ^ { N \times K } } \end{array}\tag{14}
$$

where y[k], s[k], m[k], and n[k] denote the received signal, real echoes, mutual interferences, and noise of the kth snapshot, respectively.

![](images/aaaba956ed4109f75d045cc0860eedff9627e120f84dae7d0b1f3f72a449c709.jpg)  
Fig. 5. Illustration of the received interference contaminated automotive radar signals in time and frequency domains. (a.i) Received mutual interference signal in the time domain: the contaminated time samples are sparse (interference contaminated signal in the time domain). (a.ii) Received mutual interference signa in the frequency domain [interference contaminated signal after FFT (negative)]. (a.iii) Interference contaminated signal after FFT (positive). (b.i) Expected useful signals in the time domain (interference-free signal in the time domain). (b.ii) Expected useful signals in the frequency domain: the target reflection frequency samples are sparse [interference-free signal after FFT (negative)]. (b.iii) Interference-free signal after FFT (positive). (c.i) Sparsity of interference in the time domain of simulated data (Simu). (c.ii) Sparsity of interference in the time domain of practical experimental data (Real Exp.). (d.i) Row-sparsity of target echo in the time domain of simulated data (Simu). (d.ii) Row-sparsity of target echo in the time domain of practical experimental data (Real Exp.).

The single-snapshot simulations of received interference-contaminated automotive radar signals in time and frequency domains are presented in Fig. 5(a) and (b). As we can see from the diagram, the interferences contaminate only a few time samples in the whole chirp. As for a set of K chirps illustrated in Fig. 5(c) and (d), the same scatterers are almost invariant within a small period of frame time, while the interferences hop by chirps due to different system parameters between the interference radar and the victim radar.

As can be seen from Fig. 5(c) and (d), the interferences are scattering randomly in the time domain received signal matrix, which indicates its sparsity in the time domain. Also, the strong target reflections occupy a few frequency cells in the frequency domain diagram. By combining all chirps, the useful echoes show special parallel lines in the frequency domain, which shows the row sparsity of useful signals in the frequency domain with either simulated or/and measured data. In Section II-D, we will take advantage of these characteristics and apply the decomposition method to mitigate mutual interferences.

## D. Interference Mitigation Model

As we analyzed before, the interference matrix M is sparse in the time domain, and the useful signal matrix S is a row sparse matrix in the frequency domain. We can compose an optimization problem as

$$
\begin{array} { r l } & { \underset { { \bf { S } } , { \bf { M } } } { \operatorname* { m i n } } ~ \| \mathcal { F } ( { \bf { S } } ) \| _ { 0 } + \lambda \| { \bf { M } } \| _ { 0 } } \\ & { \mathrm { ~ s . t . ~ } \| { \bf { Y } } - { \bf { S } } - { \bf { M } } \| _ { F } ^ { 2 } < \delta } \end{array}\tag{15}
$$

where $\mathcal { F } ( \cdot )$ denotes the FFT operation, $\lambda \geq 0$ is the hyperparameter, and ∥ · ∥<sub>0</sub> is the $\ell _ { 0 }$ norm of a matrix, which is used to represent the sparsity. The above problem is nonconvex, which is NP-hard to solve. According to our previous analysis, we relax the problem to a convex version as follows:

$$
\begin{array} { l } { \underset { { \bf { S } } , { \bf { M } } } { \operatorname* { m i n } } \ \| \mathcal { F } ( { \bf { S } } ) \| _ { 2 , 1 } + \lambda \| { \bf { M } } \| _ { 1 } } \\ { \mathrm { s } . \mathrm { t } . \ \| { \bf { Y } } - { \bf { S } } - { \bf { M } } \| _ { F } ^ { 2 } < \delta } \end{array}\tag{16}
$$

where $\lVert \cdot \rVert _ { 1 }$ is the convex relaxation of $\ell _ { 0 }$ norm, which is the sum of the amplitudes of all elements. As for the row sparsity of echo signals in the frequency domain, we relax the $\ell _ { 0 }$ norm into $\ell _ { 2 , 1 }$ norm, where $\begin{array} { r } { \| \bar { \mathbf { A } } \| _ { 2 , 1 } : = \sum _ { i = 1 } ^ { n } ( \sum _ { j = 1 } ^ { m } \mathbf { A } _ { i j } ^ { 2 } ) ^ { 1 / 2 } } \end{array}$ . In other words, $\ell _ { 2 , 1 }$ norm is the sum of $\ell _ { 2 }$ norms in each row, which makes as many elements as possible in each line to be 0, so we called it row sparse. The above optimization problem can be solved via ADMM by optimizing the target echoes and interferences.

## III. PROPOSED METHOD

As analyzed above, mitigating the interference can be regarded as the problem to figure out the corresponding sparse useful beat signal in the frequency domain. The augmented Lagrangian function of the optimization model in (16) is

$$
\begin{array} { l } { \displaystyle \mathcal { L } ( \mathbf { S } , \mathbf { M } , \mathbf { Y } _ { 1 } , \mu ) } \\ { \displaystyle \quad = \| \mathcal { F } ( \mathbf { S } ) \| _ { 2 , 1 } + \lambda \| \mathbf { M } \| _ { 1 } + \frac { \mu } { 2 } \bigg \| \mathbf { Y } + \frac { \mathbf { Y } _ { 1 } } { \mu } - \mathbf { S } - \mathbf { M } \bigg \| _ { F } ^ { 2 } } \end{array}\tag{17}
$$

where $\mu$ is the penalty parameter and $\mathbf { Y } _ { 1 }$ is the Lagrangian variable. We would like to alternately update one variable by

![](images/f84da2f7171f68e53cf402e79516585938a29f03b8de3bebdbcb4b61019c4de1.jpg)  
(a)

![](images/3f81f2a972f80320c925a855e4fffa631e5f444288318988bc91286eaa61a804.jpg)  
(b)

![](images/564230abac315b009d7745108bac8fa5eab950702827714c6ee23475ab30dab4.jpg)

![](images/1728d15b652b1dac7a14d33f7a8cf3a3dc482eefe557c3b2160362b43896b454.jpg)

![](images/24e13c40ebce87927dc36ece31d534c49f32c7c9596a58ae3f35584cf9647f61.jpg)  
(c)

![](images/822a2dd3799cca67e5cdbb2b79e1ab3238d5661322aeba65f6fde27f69ecdf4a.jpg)  
(e)

(d)  
![](images/938fb0e7c330de5e90933f664aaad272cd7f3b73095bf2b7c68bc0d07ce6ba1a.jpg)  
(f)

![](images/8bf74208dfd681aac2c32d2570508d16c3a6ce489c66b5b69e45ae5a0f11c469.jpg)

![](images/610a3e4033a7be7b28ae7dc211be72b0fa83a8feb389227fe920e14e56422cd2.jpg)

(h)  
(g)  
![](images/3a672cb745c75518c2983f096005ee1dd4f553da2c6d197a44395e82c5256411.jpg)  
(i)  
(i)

![](images/c01645c65ffa52899fee40f58356fc4f97c4c9ba4a45bd13b7eb98f931c71660.jpg)

![](images/abe1811253b03039efdbc2d0943253bf786702a231ba2fd8164a58c08cf69bfc.jpg)  
(1)

![](images/b83a0e3a1074b31af20b8c5cb2dc6b3769f6e00360eda3d3df315083b1800d8d.jpg)

(k)  
![](images/531b3c8846b8255e717b6a087d8bedd949e541a45dc3b85fdb5a68767c1cbb8e.jpg)  
(m)  
(n)

![](images/7bfe964decbdbfb960e63cc1fcf61b2fec29394bf5c93a572db3157c4d07a627.jpg)

![](images/d2ed0c5e7b7e385a39f94d506f3c5821448e89cdffae7b483268dcf8eb7ef1d9.jpg)  
(p)

![](images/1f1f125a5df3eeb58ecf64d0a57b966bc8c4bc7d4f0ba0f1e3093f39de23d252.jpg)  
(q)

(0)  
![](images/77bc1b3cf9d0dca995621bdebb193f5bd500bd1f4b88b2356ec4f20fbb50b7d1.jpg)  
(r)

![](images/42eb2130b4370fe2d51b47082badebc0cdd9e105eab5e520869a2dafd5ed31f3.jpg)  
(s)

![](images/25c9dd187578eb34c4204f99ae00bb86f1b9d8540a07b25c02012d8649e7de97.jpg)  
(t)  
Fig. 6. RD maps for different SINRs. The yellow frames enlarge the interference artifacts remains, and the lighter the more interference artifacts remains $\mathrm { ( a ) } { \overline { { - } } } \mathrm { ( d ) } \ \mathrm { S I N R } = { \overline { { - 2 0 \ } } } \mathrm { d } \mathrm { B } .$ . (e)–(h) $\mathrm { S I N R } = - \dot { 2 } 5$ dB. (i)–(l) SINR = −30 dB. (m)–(p) SINR = −35 dB. (q)–(t) SINR = −40 dB. First column: without any processing. Second column: Notch 1D. Third column: Notch 2D. Fourth column: row sparse.

fixing the other ones in each iteration. Next, we alternately update one variable and keep the others fixed.

## A. Update S

First, we update the variable S in the (t + 1)th iteration as follows:

= arg min $\| \mathcal { F } ( \mathbf { S } ) \| _ { 2 , 1 }$ S

$$
\mathbf { S } ^ { ( t + 1 ) } = \underset { \mathbf { S } } { \arg \operatorname* { m i n } } \ \mathcal { L } \big ( \mathbf { S } , \mathbf { M } ^ { ( t ) } , \mathbf { Y } _ { 1 } ^ { ( t ) } , \mu ^ { ( t ) } \big )
$$

$$
+  \frac { \mu ^ { ( t ) } } { 2 } \| \mathbf { Y } + \frac { \mathbf { Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } - \mathbf { S } - \mathbf { M } ^ { ( t ) } \| _ { F } ^ { 2 } .\tag{18}
$$

According to the Parseval theorem, the norm does not change after the Fourier transform, and the above formula

becomes

$$
\begin{array} { r l } & { { \bf S } ^ { ( t + 1 ) } } \\ & { = \underset { { \bf S } } { \arg \operatorname* { m i n } } ~ \| \mathcal { F } ( { \bf S } ) \| _ { 2 , 1 } + \frac { \mu ^ { ( t ) } } { 2 } \left\| \mathcal { F } \Bigg ( \mathbf { Y } + \frac { { \bf Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } - { \bf M } ^ { ( t ) } - { \bf S } \Bigg ) \right\| _ { F } ^ { 2 } } \\ & { = \underset { { \bf S } } { \arg \operatorname* { m i n } } ~ \| \mathcal { F } ( { \bf S } ) \| _ { 2 , 1 } + \frac { \mu ^ { ( t ) } } { 2 } \left\| \mathcal { F } ( { \bf Y } + \frac { { \bf Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } - { \bf M } ^ { ( t ) } ) - \mathcal { F } ( { \bf S } ) \right\| _ { F } ^ { 2 } . } \end{array}\tag{19}
$$

Then, the closed-form solution can be calculated by using the row-sparse St technique, that is,

$$
{ \bf S } ^ { ( t + 1 ) } = \mathcal { F } ^ { - 1 } \Bigg ( \mathrm { S t } _ { 2 , 1 } \Bigg ( \mathcal { F } \Bigg ( { \bf Y } + \frac { { \bf Y } _ { 1 } ^ { \mathrm { ( t ) } } } { \mu ^ { \mathrm { ( t ) } } } - { \bf M } ^ { \mathrm { ( t ) } } \Bigg ) , \frac { 1 } { \mu ^ { ( t ) } } \Bigg ) \Bigg )\tag{20}
$$

where $\mathrm { S t } _ { 2 , 1 } ( \cdot )$ is defined as

$$
[ \mathrm { S t } _ { 2 , 1 } ( \mathbf { A } , \delta ) ] _ { i , : } = \operatorname* { m a x } \{ | \mathbf { A } _ { i , : } | - \delta , 0 \} \frac { \mathbf { A } _ { i , : } } { | \mathbf { A } _ { i , : } | } .\tag{21}
$$

## B. Update M

Next, we update M by using newly updated useful echoes, and the Lagrangian function is

$$
\begin{array} { r l } & { \mathbf { M } ^ { ( t + 1 ) } = \underset { \mathbf { M } } { \mathrm { a r g } \mathrm { m i n } } \ \mathcal { L } _ { 1 } \big ( \mathbf { S } ^ { ( t + 1 ) } , \mathbf { M } , \mathbf { Y } _ { 1 } ^ { ( t ) } , \mu ^ { ( t ) } \big ) } \\ & { \qquad = \underset { \mathbf { M } } { \mathrm { a r g } \mathrm { m i n } } \ \lambda \| \mathbf { M } \| _ { 1 } + \frac { \mu ^ { ( t ) } } { 2 } \Bigg \| \mathbf { Y } + \frac { \mathbf { Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } - \mathbf { S } ^ { ( t + 1 ) } - \mathbf { M } \Bigg \| _ { F } ^ { 2 } . } \end{array}\tag{22}
$$

Then, the closed-form solution can be calculated by using the element-sparse St technique, that is,

$$
\mathbf { M } ^ { ( t + 1 ) } = \mathrm { S t } _ { 1 } \Bigg ( \mathbf { Y } + \frac { \mathbf { Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } - \mathbf { S } ^ { ( t + 1 ) } , \frac { 1 } { \mu ^ { ( t ) } } \Bigg )\tag{23}
$$

where $\mathrm { S t } _ { 1 } ( \cdot )$ is defined as

$$
[ \mathrm { S t } _ { 1 } ( \mathbf { A } , \delta ) ] _ { i , j } = \operatorname* { m a x } \{ | \mathbf { A } _ { i , j } | - \delta , 0 \} \frac { \mathbf { A } _ { i , j } } { | \mathbf { A } _ { i , j } | } .\tag{24}
$$

## C. Update $Y _ { I }$ and $\mu$

Next, we update the Lagrange multiplier $\mathbf { Y } _ { 1 }$ and factor µ by using the following equations:

$$
{ \bf Y } _ { 1 } ^ { ( t + 1 ) } = { \bf Y } _ { 1 } ^ { ( t ) } + \mu ^ { ( t ) } ( { \bf Y } - { \bf S } ^ { ( t + 1 ) } - { \bf M } ^ { ( t + 1 ) } )\tag{25}
$$

$$
\mu ^ { ( t + 1 ) } = \operatorname* { m i n } ( \eta \mu ^ { ( t ) } , \mu _ { \operatorname* { m a x } } ) .\tag{26}
$$

Finally, the iteration stops when the number of iterations reaches the expected limitation or the termination condition is met. The termination condition is given as

$$
\frac { \| \mathbf { Y } - \mathbf { S } - \mathbf { M } \| _ { F } ^ { 2 } } { \| \mathbf { Y } \| _ { F } ^ { 2 } } < \tau\tag{27}
$$

where τ presents the relative tolerance. Through row sparse matrix recovery, the target echoes will be separated through the algorithm. Herein, the solution is listed in Algorithm 1.

## Algorithm 1 Proposed Row Sparse Method

Input: Y   
User Parameter: µ   
1:Initialize: $\mathbf { M } ^ { ( t ) } , \mathbf { Y } _ { 1 } ^ { ( t ) }$   
2:while not converged do   
3: t ← t + 1   
4: S<sup>(t+1)</sup> = F <sup>−1</sup>St<sub>2,1</sub><sup></sup>F <sup></sup>Y + <sup>Y(t)1</sup><sub>µ(t)</sub> µ(t) − M<sup>(t)</sup> µ<sup>(t)</sup> 1   
5: M<sup>(t+1)</sup> = St<sub>1</sub>(Y + Y<sup>(t)</sup> − S<sup>(t+1)</sup>, 1   
µ<sup>(t)</sup> <sub>µ(t)</sub> )   
6: (t+1) = Y<sup>(t)</sup> + µ<sup>(t)</sup>(Y − S<sup>(t+1)</sup> − M<sup>(t+1)</sup>)   
7: µ<sup>(t+1)</sup> = min(ηµ<sup>(t)</sup>, µ<sub>max</sub>)   
8:end while   
Output: S  
TABLE I

PERFORMANCE MEASURE OF DIFFERENT SINRS: RMSES OF RD MAP UNDER DIFFERENT SINRS
<table><tr><td>SINR (dB)</td><td>-20</td><td>-25</td><td>-30</td><td>-35</td><td>-40</td></tr><tr><td>Notch 1D</td><td>9.30e-5</td><td>1.67e-4</td><td>1.72e-4</td><td>1.61e-4</td><td>1.42e-4</td></tr><tr><td>Notch 2D</td><td>9.19e-5</td><td>1.34e-4</td><td>1.07e-4</td><td>9.08e-5</td><td>8.49e-5</td></tr><tr><td>Row Sparse</td><td>0.74e-5</td><td>0.66e-5</td><td>0.58e-5</td><td>0.57e-5</td><td>0.57e-5</td></tr></table>

TABLE II

PERFORMANCE MEASURE OF DIFFERENT SINRS: SSIMS OF RD MAPS UNDER DIFFERENT SINRS
<table><tr><td>SINR (dB)</td><td>-20</td><td>-25</td><td>-30</td><td>-35</td><td>-40</td></tr><tr><td>Notch 1D</td><td>0.3011</td><td>0.1270</td><td>0.1223</td><td>0.1496</td><td>0.2346</td></tr><tr><td>Notch 2D</td><td>0.3063</td><td>0.1991</td><td>0.2501</td><td>0.3076</td><td>0.3400</td></tr><tr><td>Row Sparse</td><td>0.9897</td><td>0.9912</td><td>0.9924</td><td>0.9925</td><td>0.9923</td></tr></table>

TABLE III

PERFORMANCE MEASURE OF DIFFERENT CHIRP RATES: RMSE OF RD MAPS FOR DIFFERENT CHIRP RATES OF INTERFERENCES
<table><tr><td>Chirp Rate</td><td> $\gamma _ { 2 } = - \gamma _ { 1 }$ </td><td> $\overline { { \gamma = - 0 . 1 \gamma } }$ </td><td> $\overline { { \gamma = 0 . 1 \gamma } }$ </td><td> $\overline { { \gamma = 0 . 5 \gamma } }$ </td></tr><tr><td>Notch 1D</td><td>1.03e-5</td><td>1.63e-5</td><td>1.65e-5</td><td>3.71e-5</td></tr><tr><td>Notch 2D</td><td>1.06e-5</td><td>1.54e-5</td><td>1.60e-5</td><td>2.06e-5</td></tr><tr><td>Row Sparse</td><td>0.59e-5</td><td>0.65e-5</td><td>0.71e-5</td><td>1.15e-5</td></tr></table>

TABLE IV

PERFORMANCE MEASURE OF DIFFERENT CHIRP RATES: SSIM OF RD MAPS FOR DIFFERENT CHIRP RATES OF INTERFERENCES
<table><tr><td>Chirp Rate</td><td> $\gamma = - \gamma$ </td><td> $\overline { { \gamma = - 0 . 1 \gamma } }$ </td><td> $\overline { { \gamma = 0 . 1 \gamma } }$ </td><td> $\overline { { \gamma = 0 . 5 \gamma } }$ </td></tr><tr><td>Notch 1D</td><td>0.9277</td><td>0.8084</td><td>0.8090</td><td>0.4797</td></tr><tr><td>Notch 2D</td><td>0.9299</td><td>0.8334</td><td>0.8163</td><td>0.7235</td></tr><tr><td>Row Sparse</td><td>0.9923</td><td>0.9888</td><td>0.9875</td><td>0.9778</td></tr></table>

## IV. SIMULATIONS AND ALGORITHM ANALYSIS

## A. Quantified Evaluation Measurement

To quantify the performance of the proposed method, we consider two quantities for the performance measurement.

1) Root Mean Square Error (RMSE): RMSE is a frequently used measurement of the differences between values predicted by a model and the values observed [39], and it represents the square root of the differences between predicted values and observed values or the quadratic mean of these differences, that is,

$$
\mathrm { R M S E } = \frac { \Vert \mathbf { S } - \hat { \mathbf { S } } \Vert _ { \mathrm { F } } } { \Vert \mathbf { S } \Vert _ { \mathrm { F } } } .\tag{28}
$$

The smaller the RMSE is, the smaller the deviation between the predicted variable and the actual variable would be. Herein, we use the processed RD maps as the input of RMSE to measure the algorithms’ performances.

![](images/eaab99be268b70fbc9102ad1e016d3746e255a50f90b437008cf6d6863f1d7fe.jpg)

![](images/fd73dcfe2f7a63a07ecf02857651184e61a7e5cdc20e869414a959236f07b848.jpg)  
(a)

![](images/6e09c3a1b6782d265dac043f9c6dd85099907e780dd73a3695fce33d11314dc4.jpg)  
(e)

![](images/8e2f13eb938cea6e96d24a5d34aed92f60034d56af28362df3dbaa539c11c8bb.jpg)

![](images/c63536ea7acff2876ebeafddfa65bc420f0d1597323c902d111044d7d5a62463.jpg)  
(i)

![](images/e268ec82e7808dcf90eefe1868272d1581ecd4b5c7598d4774a7928f62a88e5f.jpg)

![](images/fbb5b48d87ac37384b58d6798e2f748dd92e91130d4c8de0fa347b0b76056965.jpg)  
(d)

(h)  
![](images/6b749e0c3a4cd5e0fd29f1c2ca154a52468734ed0fa2b76dcf87ef1c5fabf2f8.jpg)

![](images/5dde1b1017de99c6d8c918f720ce554d562681d3dcb681b038400286dbd2313c.jpg)  
(n)  
(m)

(1)  
(o)  
![](images/f79497de975df401b100485191ed808d91824af0eaa3248899f0b52a34ea84f4.jpg)  
(p)  
Fig. 7. RD maps for different frequency slope. The yellow arrows are pointing at the interference artifact remains. (a)–(d) $\gamma _ { 2 } = - \gamma _ { 1 }$ . (e)–(h) $\gamma _ { 2 } = - 0 . 1 \gamma _ { 1 }$ (i)–(l) $\gamma _ { 2 } = 0 . 1 \gamma _ { 1 }$ <sub>1</sub>. (m)–(p) $\gamma _ { 2 } = 0 . 5 \gamma _ { 1 }$ . First column: without any processing. Second column: Notch 1D. Third column: Notch 2D. Fourth column: row sparse.

2) Structural Similarity Index Measure (SSIM): SSIM index is calculated on various windows of an image [40]. The measure between two windows x and y is defined as

$$
\mathrm { S S I M } ( x , y ) = \frac { ( 2 \mu _ { x } \mu _ { y } + c _ { 1 } ) ( 2 \sigma _ { x y } + c _ { 2 } ) } { \left( \mu _ { x } ^ { 2 } + \mu _ { y } ^ { 2 } + c _ { 1 } \right) \left( \sigma _ { x } ^ { 2 } + \sigma _ { y } ^ { 2 } + c _ { 2 } \right) }\tag{29}
$$

where $\mu _ { x }$ is the average of $x , \ \mu _ { y }$ is the average of $y , \ \sigma _ { x } ^ { 2 }$ is the variance of $x , ~ \bar { \sigma } _ { \mathrm { v } } ^ { 2 }$ is the variance of $y , \ \sigma _ { x y }$ is the covariance of x and $y , { \overset { \cdot } { c } } _ { 1 } = ( k _ { 1 } L ) ^ { 2 }$ and $c _ { 2 } ~ = ~ ( k _ { 2 } L ) ^ { 2 }$ are two variables to stabilize the division with weak denominator, and L is the dynamic range of the pixel values. By default, $k _ { 1 } = 0 . 0 1$ and $k _ { 2 } = 0 . 0 3$ . It has to be pointed out that the windows x and y are real number matrices. SSIM measures the similarity between the predicted variable and the actual one. The larger the SSIM is, the better the prediction will be. Also, we use processed RD maps as the input of SSIM to measure the algorithms’ performances.

## B. Compared Methods

To prove the effectiveness of our method, the notched filtering methods, which are implemented in the 1-D time domain and the 2-D time–frequency domain, are also implemented in our simulation as the comparison. The notched filtering methods are named Notch 1D and Notch 2D [41], respectively.

1) Notch 1D: Through the Notch 1D method, the interference-contaminated time sampling points will be identified by the amplitude changes and replaced with zeros. Only when the amplitudes of the time sampling points are bigger than the threshold, the point in time would be replaced by zeros.

2) Notch 2D: As shown in Fig. 8, the interference in beat frequency is a V-shaped artifact in the time–frequency domain, as depicted by red dotted lines. The time–frequency transformation is obtained by short-time Fourier transform (STFT). A time domain signal can be transferred to the time–frequency domain by sliding a window function w[n] with length m over the original signal x[n] and then applying the discrete Fourier transform (DFT) over each windowed data, i.e.,

![](images/ab2463f4dce9d612b6cfe93bf48eb7b32dfd34e37ddeba863439c3fe390e0da3.jpg)  
(a)

![](images/0d56c412058a8a942413df1d7b16a59a075d66e46e73acea21b828ddb9c5ec88.jpg)

![](images/69485bf6c3f420add4d6ab93d1998b93ab015bcc0aa80ca0a8b47c7829255909.jpg)

(b)  
![](images/3e91df8a230bdb434c4c844cd41698f48af9475b4b5ab8c0dccb7ef9601fe7e9.jpg)

![](images/107eb23307d2dca671057f4795e270ba7ed7d8e2d7a98f29ee06664d7fc5b644.jpg)  
(e)  
(f)

![](images/0dd212420242c0e82a493ca92b64dbafa498254ca2ddfa9b7ed90afc1bcfb930.jpg)  
(d)

(c)  
![](images/905fd713347ffcddd71825681720facd3f8e304648d61c3f43dc4edeab8beee9.jpg)

![](images/b279e7b7e79f7c40ac57a42221b351b538b7121a23a7c3d811dd97a058bfd9a4.jpg)  
(h)

![](images/e8871a6b8b4cbaa6b901db0f2cdd1845b78d4eafb663b76652a3a3da62f19931.jpg)

(g)  
![](images/7d59052307b32a8d4e8da4d01d12e5f827562d78614f9b064c4854dac9f3283a.jpg)  
(i)  
i)

![](images/e06e187b87c49c2b4518b099c90ef150d8c852a4a95efb1e2c06176364b96dba.jpg)

![](images/00eee3f65c305f1d753734df609f2d0c8f707f8e6516460462340bf521fab12b.jpg)  
(1)

![](images/de7ae39a1f938e271feb2126feadbf99d0ec3a6e3c959dc5d6b299e1f7f0874e.jpg)  
(m)

![](images/38a7d75e276f5487aab4522b1c4f03203eef563cc41364195189fe639bbb3dc4.jpg)  
(n)

(k)  
![](images/48a643be40aece08269cf26a4cf76f04dcc0852f1a252fb5ba4755043f0c51c4.jpg)  
(0)

![](images/a82fae5fd5daf73ca54e7d0ddda549016e11e4ba419c71518bb75a902b143ba5.jpg)  
(p)  
Fig. 8. Beat signals in the time–frequency domain for different frequency slopes. (a)–(d) γ<sub>2</sub> = −γ<sub>1</sub>. (e)–(h) γ<sub>2</sub> = −0.1γ<sub>1</sub>. (i)–(l) γ<sub>2</sub> = 0.1γ<sub>1</sub>. (m)–(p) $\gamma _ { 2 } = 0 . 5 \gamma _ { 1 }$ . First column: without any processing. Second column: Notch 1D. Third column: Notch 2D. Fourth column: row sparse.

$$
\mathrm { S T F T } \{ x [ n ] \} ( m , \omega ) = \sum _ { n = 0 } ^ { m - 1 } x [ n ] w [ n - m ] e ^ { - j \omega n } .\tag{30}
$$

Herein, the window function that we used in this article is Hamming window. One threshold is set for the zero replacement; when the amplitude in one time–frequency unit is greater than the threshold, this unit would be nulled by zero.

## C. Performance Analysis for Different Input Signal-to-Interference-and-Noise Ratios (SINRs)

We usually assume that the mutual interference is much stronger than the useful target echoes because the aggressor radar directly illuminates the victim radar without any reflections. Hence, the low SINR condition is common for most cases, but, sometimes, the mutual interference signal is only a bit stronger than the useful signal or may even fail to dominate the received signal. We need to simulate the circumstances with different SINRs to demonstrate the performances. Numerical simulations on different SINRs [42], ranging from −40 to −20 dB, by applying four algorithms to mitigate interferences are shown in Fig. 6, where the mitigation results are presented in the RD domain.

TABLE V  
PERFORMANCE MEASUREMENTS OF MULTI-INTERFERENCE CIRCUM-STANCES
<table><tr><td>Algorithm</td><td>Notch 1D</td><td>Notch 2D</td><td>Row Sparse</td></tr><tr><td>RMSE</td><td>3.43e-5</td><td>2.18e-5</td><td>1.38e-5</td></tr><tr><td>SSIM</td><td>0.8386</td><td>0.8430</td><td>0.9648</td></tr></table>

3  
![](images/2f684c542da8241f52e3ebc9fc46baba2249c7d85fd93ca078dba7156ba55ffd.jpg)  
(a)

![](images/334404a28bdbe83d26ac56be0c696babb0f09bb3c4723b43bfa27e1f89d89446.jpg)  
(b)

![](images/30d34cf41d513ef6c2472a64067932c3733cc310cd592f1fda2deb0879ea9f30.jpg)  
(c)

![](images/64ab08584c1bcfccd6660bdcd9cfbdf7c5294f462c3c28457fcd3ae9ec416c35.jpg)  
(d)

Fig. 9. Beat signal in the time–frequency domain for multi-interference circumstances. (a) Without any processing. (b) Notch 1D. (c) Notch 2D. (d) Row sparse.  
![](images/6cea4817eef8d2e2c85b88d1a0cb86a825f311c386a31df7a8b96281408ee4c9.jpg)  
(a)

![](images/5f65baad79958f042bc4e7ed133d46081a5cb87662044a9cb97ff73c0f08baad.jpg)  
(b)

![](images/504467115121d796fa614d24046f5fd21ecfd04408cc73cdf0b0cf2c4c5cee23.jpg)  
(c)

![](images/ffc7c2876c808e0e8867c90792346635093e23bbddb7495a82ff39d835f80245.jpg)  
(d)

Fig. 10. RD maps for multi-interference circumstances. (a) Without any processing. (b) Notch 1D. (c) Notch 2D. (d) Row sparse.  
![](images/376d29d0487f95adbf1251cfa917f90701571133586c492f1b574315c0506541.jpg)  
Fig. 11. Field experiment setup 1.

TABLE VI  
CONFIGURATION IN STATIC EXPERIMENT
<table><tr><td>Configurations</td><td>Traffic Radar</td><td>Exp.1</td><td>Exp.2</td><td>Exp.3</td><td>Unit</td></tr><tr><td>Start Frequency</td><td>76.67</td><td>76.76</td><td>76.74</td><td>76.71</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>6</td><td>-0.6</td><td>0.6</td><td>3</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>25.6</td><td>34</td><td>34</td><td>34</td><td>µs</td></tr></table>

TABLE VII

RUNNING TIME OF THE IMPLEMENTED METHODS IN STATIC EXPERIMENT-
<table><tr><td>Algorithms</td><td>Running Time (s)</td><td>maximum iterations</td></tr><tr><td>Notch 1D Method</td><td>21.09</td><td>1</td></tr><tr><td>Notch 2D Method</td><td>1753.61</td><td>1</td></tr><tr><td>Hankel Method</td><td>960.37</td><td>446</td></tr><tr><td>LPC Method</td><td>0.84</td><td>1</td></tr><tr><td>Proposed Method</td><td>0.80</td><td>8</td></tr></table>

TABLE VIII  
CONFIGURATION IN MOVING EXPERIMENT
<table><tr><td>Configurations</td><td>Aggressor</td><td>Victim</td><td>Unit</td></tr><tr><td>Carrier Frequency</td><td>77.0</td><td>76.3</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>-24.414</td><td>24.414</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>29.6</td><td>29.6</td><td>µs</td></tr></table>

The two simulated targets are marked with red solid frames in Fig. 6. The interference artifacts remains are zoomed in and enlarged by the yellow frames. The lighter the more interference artifacts remain in the algorithm processed results. As we can see from Fig. 6, notched filtering methods replace the interference-contaminated parts with zeros, leaving the RD to map a blur. On the other hand, the proposed sparse recovery methods can prevent blur with less noise left. Compared with the interference-free RD map shown in Fig. 1, the RMSEs and SSIMs are listed in Tables I and II. Since SSIM only accepts real number matrices, the RD maps are transformed into absolute values before being calculated as the input of SSIM. As can be seen, the SSIM and RMSE results show that the row sparse recovery method performs better than other algorithms, especially for the larger SINR, since the proposed method has constraints on the useful echoes to protect them from being mitigated.

TABLE IX  
CONFIGURATION IN FIELD EXPERIMENT WITH COMPARISON
<table><tr><td>Configurations</td><td>Aggressor</td><td>Victim</td><td>Unit</td></tr><tr><td>Carrier Frequency</td><td>77.0</td><td>79.47</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>32.23</td><td>-16.11</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>110</td><td>110</td><td>µs</td></tr></table>

## D. Performance Analysis for Different Interference Chirp Rates

As mentioned in Section II, we assume that the aggressor radar, mounted on another vehicle or next to the traffic camera, illuminates the victim automotive radar with a different waveform. It is obvious that the differences in carrier frequencies would be favorable for signal separation. Herein, waveforms with similar carrier frequencies but with different chirp rates, which are the focus of this article, would cause interference contamination. In this section, we simulate four cases of different frequency slopes: 1) $\gamma _ { 2 } = - \gamma _ { 1 } ; 2 ) \gamma _ { 2 } = - 0 . 1 \gamma _ { 1 } ;$ 3) $\gamma _ { 2 } ~ = ~ 0 . 1 \gamma _ { 1 }$ ; and 4) $\gamma _ { 2 } = 0 . 5 \gamma _ { 1 }$ . The input SINR is set to −30 dB. The abovementioned four algorithms are applied to mitigate all cases, and their mitigation results in the RD domain and the time–frequency domain are shown in Figs. 7 and 8, respectively.

![](images/1ac5c342e29ea59170262212b579d783d594e19d6b8cef4489e5b752d113b29d.jpg)  
(a)

![](images/b524946ee29e7f4cdd710c1f8e5b6a4ea7c7d06dc87914283b045b8f3ec46967.jpg)  
(b)

![](images/9d3c0a7a49dbe5f2e02bce67f447f6236d8ee1ecab65d63e10d4908a92ee6cf5.jpg)  
(c)

Fig. 12. Received signal in the STFT domain. (a) Exp. 1. (b) Exp. 2. (c) Exp. 3.  
![](images/abd381e01d600a95d241578f4606b0ed3af946e4348d1c22ec2e5fe826b274a1.jpg)  
Fig. 13. Real and complex sampling theories.

The two simulated targets are marked with red solid frames, and interference artifact remains are pointed by yellow arrows in Fig. 7. As we can see from Figs. 7 and 8, the notch filtering methods cause noisy backgrounds in RD maps even when the frequency slopes of both aggressor and victim radars are quite different. Both sparse recovery methods may generate bright strips at the targets’ ranges with quite a clean background. The RMSE and SSIM are also used to measure the performance, and the results are listed in Tables III and IV. As we can see, the SSIM indicates that the element sparse method outperforms both algorithms when the interference-contaminated time is long. The Notch 1D method is restricted by nulling a large region of the time–frequency spectrum.

## E. Performance Analysis for Multi-Interference Circumstances

In practical applications, multiple vehicles would drive by each other on the road, and it is necessary to analyze the circumstances in which multiple aggressor radars illuminate the victim radar in almost every sampling point. The interferences are set with different frequency slopes and SINRs to simulate the practical circumstances. The recovered results of these four algorithms in the time–frequency domain and the RD map domain are shown in Figs. 9 and 10. The two simulated targets are marked with red solid frames in Fig. 10.

As we can see, the Notch 1D method removes almost all the time–frequency spectra, leaving very few useful echo signals and causing blur in the RD map. Due to the restriction of the interferences detection threshold, the Notch 2D method removes strong interferences. As for some other interferences that cannot reach the threshold but still contaminate the useful signals, the Notch 2D method cannot mitigate them effectively. By paying attention to the essence of the useful echo signal, the sparse recovery methods can protect the echo signals from being removed. The RMSE and SSIM are also used to measure the performance of these four algorithms, and the results are listed in Table V. Both metrics show a significant improvement in the proposed method in this multi-interference circumstance. The proposed method is more applicable in complicated cases than notched filtering methods.

## V. EXPERIMENTAL RESULTS

In this section, the proposed algorithms are applied to real automotive radar data to test their performance.

## A. Static Aggressor Experiment

We adopted the TI AWR2243BOOST mmWave radar board for data capture in the field experiment. Fig. 11 shows the experiment setup in a front-door square in Nanjing, China. The aggressor radar, produced by Hawkeye Technology Corporation, is a long-range 77-GHz traffic radar. The victim radar was configured as a typical short-range radar (SRR) with a different frequency slope to test the performance of our algorithms. One adult was standing in front of the radar as a human pedestrian target [43].

The radar configurations set for the experiments and the relative configurations of the aggressor radar are listed in Table VI. Both the aggressor radar and the victim radar work at TDM so that only one transmitter works at the same time. The captured data was saved to disk and processed on MATLAB.

In each experiment, we select one typical polluted pulse, which contains obvious interference in the time–frequency domain, as shown in Fig. 12. As can be seen, when the difference in frequency slopes between the aggressor radar and victim radar becomes smaller, the slope of the slant line becomes more extensive, and the interferences’ contaminated time becomes longer. The interferences are much stronger than the echoes, but they look like slant lines that are not “V” shape patterns shown in previous simulations.

This phenomenon occurs in the time–frequency domain caused by the complex sampling that TI AWR2243BOOST applies. In previous research, we simulate all interference cases via real sampling. In fact, the hardware for real sampling is much cheaper and, therefore, prevails in commercial automotive radars. To explain the difference between complex sampling and real sampling, a schematic is given in Fig. 2, and real sampling is more like sampling all the radio signals within the bandwidth, which are symmetrical along the center of the transmitted signal as the red dotted frame shows, while the complex sampling is in half of the real sampling but overlaps and extends beyond the real sampling, as the yellow dotted frame shows in Fig. 13.

![](images/98fcb41000388a547cc91f4397a9bb00f330c9a3a76bf0b3de585f2ccf7fbd28.jpg)  
(a)

![](images/b419767be36445311ef8b1d81f710fb9717a138b5ee6d159e240e128ff915eaf.jpg)  
(b)

![](images/e3bd77d3ad3724b2950529195c2fff0826c11e637e9f925fde7107fd5f7a5e75.jpg)  
(c)

![](images/149dd82e5ae9afab7477dc55a03294794914a60b56b8206f1adc1b75cb155c99.jpg)  
(d)

![](images/7b5b3d20ec3c3ee0e14a4b8da79ca80081788a9c983a47a41f06b8cc90cb5370.jpg)  
(e)

![](images/69c7ea844a16af67df210e7581d187ee1fe8bbc0ee5985c1d0a39926beca49ba.jpg)  
(f)

Fig. 14. RD maps for different experiment configurations—Exp. 1. (a) Without any processing. (b) Notch 1D. (c) Notch 2D. (d) LPC method. (e) Hanke matrix method. (f) Proposed method.  
![](images/16fa0f3461611ad3c33d21461e785ea83791cdbe72f8974d350f1e1c1f3da9e1.jpg)  
(a)

![](images/323abbc0481d8ac117c7d7d1ffda0d54bbff11200cdbf70d41ea972c20ab2460.jpg)

![](images/aa2db7a779cfd4545b66107a375f9b6e518b50ab4a68ec6c95882580bd438857.jpg)  
(b)  
(c)

![](images/89394ee8090f6e819b855f1525adc906d3e56313401053b2f1b1b19ff21adcb3.jpg)  
(d)

![](images/598ca548d71943f95169211c6b022fc86d2f401d08bff302d518c7ca61f8a002.jpg)  
(e)

![](images/98e3f0d5400021a763d42224fe93de96c3987f8da58e348b1ba2dd22affdfee8.jpg)  
(f)  
Fig. 15. RD maps for different experiment configurations—Exp. 2. (a) Without any processing. (b) Notch 1D. (c) Notch 2D. (d) LPC method. (e) Hankel matrix method. (f) Proposed method.

In Figs. 14–16, we show the recovered RD maps of our proposed method and four previous methods, i.e., the Notch 1D method, the Notch 2D method, the LPC method [44], and the Hankel matrix method [29] for the aforementioned circumstances. We use a solid yellow frame to mark the target reflection and a dotted red frame to notify the algorithm errors and fake targets. As we can see from the figures, all the methods can work properly when the differences between the victim radar’s frequency-modulated slope and the aggressor radar’s frequency-modulated slope are large. Also, in practical experiments, Notch 1D and LPC methods always leave the RD map some blur in the Doppler dimension, regardless of the radars’ frequency-modulated slope differences. To be noted that in Fig. 16, all four previous methods are invalid due to the long-time occupation of the interferences in the time domain, which is essentially caused by the small difference between the victim radar’s and aggressor radar’s frequencymodulated slopes. Our proposed method, with the protection of useful targets’ echoes in the frequency domain, survives in this situation and proves its robustness and feasibility of practical applications.

![](images/70780d121d9d779d2d74295af5e84fed9545cb58a80162a996bc9bf2fc024941.jpg)  
(a)

![](images/becbb6ddd2a7c0ba27bbeb7801ab7d7810f2377f0826953a7ef255780f32a123.jpg)  
(b)

![](images/0ed4abafa9431fa9a04f370f8810b1f502b912322068e80f9403db9a0e088b62.jpg)  
(c)

![](images/aa707912d04e7ccf2904fd8ee48be9d24f0c4f94919becc5a579385c3480dfe9.jpg)  
(d)

![](images/dbbc304ceba7514d4cee253afae1fe484496bdd130a31a8d65abbf9fb6e7dbfe.jpg)  
(e)

![](images/aa41a373ea42dbfc51b48d0bbb161aec6703c8eb698665a536ec901b672ff9bb.jpg)  
(f)  
Fig. 16. RD maps for different experiment configurations—Exp. 3. (a) Without any processing. (b) Notch 1D. (c) Notch 2D. (d) LPC method. (e) Hankel matrix method. (f) Proposed method.

TABLE X  
RMSE AND SSIM OF THE METHODS’ RESULTS IN FIELD EXPERIMENT WITH COMPARISON
<table><tr><td>Algorithms</td><td>RMSE</td><td>SSIM</td></tr><tr><td>Notch 1D</td><td>3.5269e-04</td><td>0.1012</td></tr><tr><td>Notch 2D</td><td>2.9766e-04</td><td>0.2783</td></tr><tr><td>LPC Method</td><td>13.924e-04</td><td>0.0086</td></tr><tr><td>Hankel Matrix Method</td><td>6.3607e-05</td><td>0.8587</td></tr><tr><td>Proposed Method</td><td>4.4362e-05</td><td>0.9824</td></tr></table>

![](images/f8a4cd3d6d1411ccbf12ce8f053a9efbd7ef94daa0a76f78ac42949e21f54c5f.jpg)  
Fig. 17. Installment of the aggressor radar in the car.

![](images/efb295315bec49cb4e7bd953e82f8afd8ff03007c62555d5ce63c323cbaab089.jpg)  
Fig. 18. Field experiment setup 2.

## B. Running Time and Computational Complexity

In this section, the computational complexity and running time are analyzed in detail. For the received signal matrix $Y \in \mathbb { C } ^ { N \times K }$ , N is commonly 512 or 1024, and K is 256 or 128 in practical applications. Hence, we assume that $N > K$ for all the methods. Then, the Notch 1D method requires value comparisons in the time domain, and it requires at least $\mathcal { O } ( N K )$ . The Notch 2D method requires STFTs and value comparisons in the time–frequency domain; then, it requires at least $\mathcal { O } ( K ( 2 ( N - W + 1 ) W \log W + W ( N - W + 1 ) ) )$ ) when the STFT window length is W . The LPC method mainly requires the computation of least-square solutions of an autoregressive model, where the Levinson–Durbin algorithm is used to solve the Yule–Walker equations. Suppose that the prediction filter polynomial order is $( N / 2 ) \textrm { - } 1$ , then it requires at least $\mathcal { O } ( L ( N / 2 ) ^ { 2 } )$ ). The Hankel method requires one SVD and two soft-thresholding processes for each chirp and each iteration. Then, it requires at least $\mathcal { O } ( L ( ( N / 2 ) ^ { 3 } + 2 ( N / 2 ) ^ { 2 } ) )$ per iteration. The proposed method requires two soft-thresholding processes and two Fourier transforms in each iteration. Then, it requires at least $\mathcal { O } ( 4 N K + 2 N K \log N )$ ) per iteration. As can be seen, the proposed method and the Hankel method require multiple iterations to realize convergence. Therefore, their running times depend not only on the computational complexity but also on the convergence rate, i.e., the number of iterations.

![](images/69f133fe2ad1311deee08cf68f12b40d69f84277e3b52683f803c29c8b2c5f4a.jpg)  
(a)

![](images/8604a510e73c75fdc729f823fd77ef27c26be03a1b9e33560989939e5cffb8bb.jpg)  
(b)

![](images/4c10a24fd64c305974cc58c94dac4430cce956257d99ef0fbe7622e85e4fd458.jpg)  
(c)

![](images/f581d4f3a7985e4cecd3f2f194e9e308ee93c5ec4a088a77035a6a0ba85e5fe9.jpg)  
(d)

![](images/b716e4ab5f97af1e6440a82488aa4d427ee1e8e616f7e656257e91f5ea9d1f38.jpg)  
(e)

![](images/7d77f527ef5c33d0d0bc4d69b8c266aec8737ea294d6f02ae07d645a711b8d13.jpg)  
(f)

Fig. 19. RD maps for the simulated practical scene with partial enlargements. (a) Without any processing. (b) Notch 1D. (c) Notch 2D. (d) LPC method (e) Hankel matrix method. (f) Proposed method.  
![](images/7c702926bf0c401234ade2616e206b40312d90c9b15c64da231ad9af657ceb36.jpg)  
Fig. 20. Setup of a field experiment with comparison.

![](images/9db59aeac3952baea4fa26adea3a388120f459adc57db394a4e37016b652e420.jpg)  
(a)

![](images/14e2e9cb79b5b51fb40ee1f8be86fc09e74426e98ac89d26d19bc74225d89e35.jpg)  
(b)  
Fig. 21. RD maps for (a) interference-free and (b) mutual interference contaminated data.

To prove the superiority of our proposed method over the four methods in comparison, the running times of the five methods are listed in Table VII, where all the methods are applied to the data collected from “Static Experiment $3 ^ { \circ }$ and the computational platform is Lenovo Legion Y7000P2020H with MATLAB R2021a. As indicated in Table VII, our proposed method shows great superiority regarding the running time. Although the Notch 1D method has quite small computational complexity, it requires loops to calculate one chirp by one chirp without using parallel computing. Notch 2D requires the most time due to the computational burdens of both loops and STFT operations. The Hankel method is restricted by a large-scale Hankel matrix and multiple iterations for convergence, resulting in a large running time. The proposed method combines all chirps and converges fast, which, finally, has a comparable running time with the LPC method. It demonstrates its high efficiency in practical applications.

## C. Moving Aggressor Experiment

To further investigate the performance of the proposed method in the actual automotive radar case, another field experiment scene is set on an ordinary city road in Nanjing. The TI AWR2243BOOST mmWave radar board is also adopted for data capture. Fig. 17 shows the installment of the aggressor automotive radar at the front of a car, which works in the middle-range mode. The configuration of the transmitted signals is listed in Table VIII. Our victim radar’s configuration is set accordingly, as listed in Table VIII. The experiment setup is illustrated in Fig. 18, where the aggressor car, on which the aggressor radar is mounted, is driving toward us during the data sampling period. Another car is parking in front of our victim radar, serving as a strong target to set as a mark in the RD map [45], [46].

![](images/bed28e841cd633d6db244f51eef16fa44daa35a67bde63cc9c588968f669fab0.jpg)  
(a)

![](images/bb923f196a67f8e00e86efdb155aadd8046d914f9fbe112d4a08cbf5c05cdfc3.jpg)  
(b)

![](images/178e5251c081848a70d9dea19be3c99d9c130fa21b04b069f13a8439051e9ecc.jpg)  
(c)

![](images/92f20dfc022cd2280d1dbadea02a05e4867c7e0893888e849e14de87272ce2be.jpg)  
(d)

![](images/ffa707b1795819dc15e1fa3880532d78d44b93069fa3c9c48c2a689ece6b87f1.jpg)  
(e)

![](images/21af234dfcbafdc2bbae879454992a47d0173a0329abe16ef343b4d18fe8b140.jpg)  
(f)  
Fig. 22. RD maps for the field experiment with comparison. (a) Interference-free. (b) Notch 1D. (c) Notch 2D. (d) LPC method. (e) Hankel matrix method. (f) Proposed method.

The proposed method and the four previous methods are applied to remove the interference in this scene, and the results are shown in Fig. 19. The orange dotted rectangle indicates the black static car in Fig. 18, the green solid rectangle indicates the white moving vehicle, and the red solid frame indicates the ground reflection. Moving target and static target areas are enlarged in Fig. 19. Aligned with former experiments, Notch 1D and Notch 2D methods show blur across the Doppler dimension, and the moving vehicle target is invisible through the algorithm processing. The LPC method, the Hankel method, and our proposed algorithm can remove the majority of the interference. Among all the methods, our method is better in protecting the target echoes regarding the elimination of ground reflection. As can be seen in the enlarged subfigures, the proposed method can recover the targets better with higher output SINR. Both experiments demonstrate the effectiveness of the proposed method.

## D. Practical Experiment With Comparison

To better get behind our proposed method, we implemented the third practical experiment with no-interference ground truth as a comparison. To enhance the plausibility of this experiment, we perform the data collection in a fully parked parking lot to test our proposed method’s robustness when the targets’ sparse characteristic is not that typical. We turned off the aggressor radar and collected the interference-free data immediately after finishing the collection of interferencecontaminated data. The experiment setup is shown in Fig. 20. As can be seen, there is an aggressor radar, which is a middle-range automotive radar made by the Hawkeye Company, in front of the victim radar. The victim radar is still the TI AWR2243BOOST mmWave radar. The radar configurations of both aggressor and victim radar are listed in Table IX.

The RD maps of interference-free and mutual interference contaminated data are shown in Fig. 21. As we can see from the figures, they are huge differences, and the mutual interference is overwhelming the targets, making them impossible to detect. Then, we test all previous methods on this data, and the recovered RD maps are shown in Fig. 22. It is obviously observed that unexpected interference artifacts are left for Notch 1D, Notch 2D, and LPC methods. The background in Fig. 22(e) is noisy since the interference is not mitigated thoroughly. The targets located at about 400 range cells in Fig. 22(c) and (e) are enhanced, which are not correct according to the interference-free RD map. In Table X, we use RMSE and SSIM as the numerical metric to quantify the interference mitigation performance of the proposed method and the other state-of-the-art methods. The RMSE of our proposed method is smaller than the other methods, and SSIM is the largest, both of which indicate that the results processed by our method are more similar to interference-free RD maps and better performance. This experiment proves the feasibility of our proposed method in complicated circumstances, like a fully parked parking lot, when the sparsity of the targets is not that typical.

## VI. CONCLUSION

We proposed an interference mitigation method based on the special sparsity of the interferences and the useful echo signals in the FMCW automotive radar system. For the method, we constructed an interference mitigation problem and introduced a dictionary to constrain the sparsity of interferences with regularization. The mitigation problem was solved through the linear ADMM. We demonstrated numerical simulations to reveal the feasibility of the proposed method under many interference-contaminated scenarios while comparing the processing results with classic notch methods using RMSE and SSIM. The experimental results proved the effectiveness and robustness of the proposed method in practical applications. Our possible future research would emphasize universal mitigation methods under more complicated interference circumstances.

## REFERENCES

[1] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270–5283, Dec. 2021.

[2] D. Solomitckii et al., “Millimeter-wave radar scheme with passive reflector for uncontrolled blind urban intersection,” IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 7335–7346, Aug. 2021, doi: 10.1109/TVT.2021.3093822.

[3] D. Jianmin, Z. Kaihua, and S. Lixiao, “Road and obstacle detection based on multi-layer laser radar in driverless car,” in Proc. 34th Chin. Control Conf. (CCC), Jul. 2015, pp. 8003–8008, doi: 10.1109/ChiCC.2015.7260912.

[4] A. Hassanien and S. A. Vorobyov, “Transmit/receive beamforming for MIMO radar with colocated antennas,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., Apr. 2009, pp. 2089–2092, doi: 10.1109/ICASSP.2009.4960027.

[5] J.-M. Munoz-Ferreras, Z. Peng, R. Gomez-Garcia, and C. Li, “A frequency-multiplexed Doppler-plus-FMCW hybrid radar architecture: Theory and simulations,” in Proc. IEEE Topical Conf. Wireless Sensors Sensor Netw. (WiSNet), Jan. 2017, pp. 8–10, doi: 10.1109/WIS-NET.2017.7878742.

[6] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 32–44, Sep. 2019, doi: 10.1109/MSP.2019.2911722.

[7] H. Rohling and M. Kronauge, “New radar waveform based on a chirp sequence,” in Proc. Int. Radar Conf., Oct. 2014, pp. 1–4, doi: 10.1109/RADAR.2014.7060246.

[8] G. Hakobyan and B. Yang, “A novel intercarrier-interference free signal processing scheme for OFDM radar,” IEEE Trans. Veh. Technol., vol. 67, no. 6, pp. 5158–5167, Jun. 2018, doi: 10.1109/TVT.2017.2723868.

[9] Y. Kitsukawa, M. Mitsumoto, H. Mizutani, N. Fukui, and C. Miyazaki, “An interference suppression method by transmission chirp waveform with random repetition interval in fast-chirp FMCW radar,” in Proc. 16th Eur. Radar Conf. (EuRAD), Oct. 2019, pp. 165–168.

[10] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020, doi: 10.1109/TVT.2019.2953305.

[11] H. Zhou, P. Cao, and S. Chen, “A novel waveform design for multitarget detection in automotive FMCW radar,” in Proc. IEEE Radar Conf. (RadarConf), May 2016, pp. 1–5, doi: 10.1109/RADAR.2016.7485315.

[12] Y. Ju, Y. Jin, and J. Lee, “Design and implementation of a 24 GHz FMCW radar system for automotive applications,” in Proc. Int. Radar Conf., Oct. 2014, pp. 1–4, doi: 10.1109/RADAR.2014.7060385.

[13] L. Lan, J. Xu, G. Liao, Y. Zhang, F. Fioranelli, and H. C. So, “Suppression of mainbeam deceptive jammer with FDA-MIMO radar,” IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 11584–11598, Oct. 2020, doi: 10.1109/TVT.2020.3014689.

[14] Z. Chen, F. Xie, C. Zhao, and C. He, “Radio frequency interference cancelation in high-frequency surface wave radar using orthogonal projection filtering,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 9, pp. 1322–1326, Sep. 2018, doi: 10.1109/LGRS.2018.2850777.

[15] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019, doi: 10.1109/TVT.2019.2901493.

[16] Y. Li, C. Wang, F. Li, X. Han, and Y. Song, “An adaptive interference cancellation method for automotive FMCW radar based on waveform optimization,” in Proc. IET Int. Radar Conf. (IET IRC), 2021, pp. 666–670, doi: 10.1049/icp.2021.0741.

[17] J. Bechter, K. Eid, F. Roos, and C. Waldschmidt, “Digital beamforming to mitigate automotive radar interference,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4, doi: 10.1109/ICMIM.2016.7533914.

[18] F. Gumbmann and L.-P. Schmidt, “Millimeter-wave imaging with optimized sparse periodic array for short-range applications,” IEEE Trans. Geosci. Remote Sens., vol. 49, no. 10, pp. 3629–3638, Oct. 2011.

[19] J. R. Van Der Merwe, F. Garzia, A. Rugamer, I. C. Vidal, and W. Felber, “Adaptive notch filtering against complex interference scenarios,” in Proc. Eur. Navigat. Conf. (ENC), Nov. 2020, pp. 1–10, doi: 10.23919/ENC48637.2020.9317518.

[20] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019, doi: 10.1109/TMTT.2018.2881154.

[21] M. Umehira, T. Nozawa, Y. Makino, X. Wang, S. Takeda, and H. Kuroda, “A novel iterative inter-radar interference reduction scheme for densely deployed automotive FMCW radars,” in Proc. 19th Int. Radar Symp. (IRS), Jun. 2018, pp. 1–10, doi: 10.23919/IRS.2018.8448223.

[22] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf., Apr. 2018, pp. 0405–0410, doi: 10.1109/RADAR.2018.8378593.

[23] Z. Liu, J. Wu, S. Yang, and W. Lu, “DOA estimation method based on EMD and MUSIC for mutual interference in FMCW automotive radars,” IEEE Geosci. Remote Sens. Lett., vol. 19, pp. 1–5, 2022, doi: 10.1109/LGRS.2021.3058729.

[24] M. Rameez, M. Dahl, and M. I. Pettersson, “Experimental evaluation of adaptive beamforming for automotive radar interference suppression,” in Proc. IEEE Radio Wireless Symp. (RWS), Jan. 2020, pp. 183–186, doi: 10.1109/RWS45077.2020.9049982.

[25] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive modelbased signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021, doi: 10.1109/JSEN.2020.3042061.

[26] S. Chen, W. Shangguan, J. Taghia, U. Kuhnau, and R. Martin, “Automotive radar interference mitigation based on a generative adversarial network,” in Proc. IEEE Asia–Pacific Microw. Conf. (APMC), Dec. 2020, pp. 728–730, doi: 10.1109/APMC47863.2020.9331379.

[27] F. Uysal and S. Orru, “Phase-coded FMCW automotive radar: Application and challenges,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 478–482, doi: 10.1109/RADAR42522. 2020.9114798.

[28] T. Fei, H. Guang, Y. Sun, C. Grimm, and E. Warsitz, “An efficient sparse sensing based interference mitigation approach for automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 274–277, doi: 10.1109/EuRAD48048.2021.00077.

[29] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022, doi: 10.1109/TSP.2022.3147863.

[30] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, Sep. 2018, doi: 10.1109/TVT.2018.2848898.

[31] K. U. Mazher, R. W. Heath, K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in Proc. IEEE Radar Conf., Sep. 2020, pp. 1–6, doi: 10.1109/ RadarConf2043947.2020.9266425.

[32] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021, doi: 10.1109/TMTT.2021.3090798.

[33] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007, doi: 10.1109/TEMC.2006.890223.

[34] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, nos. 3–4, pp. 371–378, 2014.

[35] M. Younis, J. Maurer, J. Fortuny-Guasch, R. Schneider, W. Wiesbeck, and A. J. Gasiewski, “Interference from 24-GHz automotive radars to passive microwave earth remote sensing satellites,” IEEE Trans. Geosci. Remote Sens., vol. 42, no. 7, pp. 1387–1398, Jul. 2004.

[36] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320, doi: 10.1109/RADAR42522.2020.9114641.

[37] N. Kehtarnavaz, Digital Signal Processing System Design: LabVIEW-Based Hybrid Programming, 2nd ed. Cambridge, MA, USA: Academic Press, 2008, pp. 175–196, doi: 10.1016/B978-0-12-374490-6.00007-6.

[38] L. Stankovic, I. Orovic, S. Stankovic, and M. Amin, “Compressive sensing based separation of nonstationary and stationary signals overlapping in time-frequency,” IEEE Trans. Signal Process., vol. 61, no. 18, pp. 4562–4572, Sep. 2013, doi: 10.1109/TSP.2013.2271752.

[39] R. Amiri, F. Behnia, and M. A. M. Sadr, “Exact solution for elliptic localization in distributed MIMO radar systems,” IEEE Trans. Veh. Technol., vol. 67, no. 2, pp. 1075–1086, Feb. 2018, doi: 10.1109/TVT.2017.2762631.

[40] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: From error visibility to structural similarity,” IEEE Trans. Image Process., vol. 13, no. 4, pp. 600–612, Apr. 2004, doi: 10.1109/TIP.2003.819861.

[41] S.-C. Pei, B.-Y. Guo, W.-Y. Lu, G. E. Sobelman, and Y.-D. Huang, “Improved design of digital 1-D and 2-D notch filters using general feedback structure,” in Proc. IEEE Int. Symp. Circuits Syst. (ISCAS), May 2016, pp. 2182–2185, doi: 10.1109/ISCAS.2016.7539014.

[42] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2019, pp. 1–6, doi: 10.1109/RADAR.2019.8835681.

[43] Y. Cheng and Y. Liu, “Person reidentification based on automotive radar point clouds,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5101913, doi: 10.1109/TGRS.2021.3073664.

[44] W. Xu, W. Xing, C. Fang, P. Huang, and W. Tan, “RFI suppression based on linear prediction in synthetic aperture radar data,” IEEE Geosci. Remote Sens. Lett., vol. 18, no. 12, pp. 2127–2131, Dec. 2021, doi: 10.1109/LGRS.2020.3015205.

[45] M. Lehtomäki et al., “Object classification and recognition from mobile laser scanning point clouds in a road environment,” IEEE Trans. Geosci. Remote Sens., vol. 54, no. 2, pp. 1226–1239, Feb. 2016.

[46] S. Chen, Z. Zhang, R. Zhong, L. Zhang, H. Ma, and L. Liu, “A dense feature pyramid network-based deep learning model for road marking instance segmentation using MLS point clouds,” IEEE Trans. Geosci. Remote Sens., vol. 59, no. 1, pp. 784–800, Jan. 2021.

![](images/628c909e89f738bbe8bfc694cb62f28464c53fa4ebf2d0491fd7a376f73fc60d.jpg)  
Yunxuan Wang received the B.Eng. degree from Southeast University, Nanjing, China, in 2022.  
She is currently a Research Assistant with the University of Colorado Boulder, Boulder, CO, USA. Her research interests include signal processing, machine learning, and convex optimization.

![](images/26b9a9102d41bb29412a335a39e6379fe6f538f9a628fd0935f4dc1024833dce.jpg)

Yan Huang (Member, IEEE) received the B.S. degree in electrical engineering and the Ph.D. degree in signal and information processing from Xidian University, Xi’an, China, in 2013 and 2018, respectively.

He was studying as a Visiting Ph.D. Student at the Electrical and Computer Engineering Department, University of Florida, Gainesville, FL, USA, from September 2016 to July 2017, and the Electrical and Systems Engineering Department, Washington University in St. Louis, St. Louis, MO, USA, from

July 2017 to August 2018. He is currently an Associate Professor with the State Key Laboratory of Millimeter Waves, Southeast University, Nanjing, China. His research interests include machine learning, synthetic aperture radar, image processing, and remote sensing.

![](images/a4a63e3ce1617efdc31fa7f3e066ba9d397a936acc25a8e5cd34f9e699654bb8.jpg)

Cai Wen (Member, IEEE) received the B.E. degree from the School of Electronic Engineering, Xidian University, Xi’an, China, in 2009, and the Ph.D. degree from the National Laboratory of Radar Signal Processing, Xidian University, in 2014.

He was a Research Scientist with the China NOR-INCO Group, Beijing, China, from January 2015 to October 2016. Since November 2016, he has been with the School of Information Science and Technology, Northwest University, Xi’an, where he is currently an Associate Professor. In November 2019,

he became a full-time Post-Doctoral Research Fellow at the Department of Electrical and Computer Engineering, McMaster University, Hamilton, ON, Canada. His current research interests include sensor array signal processing, multiple input multiple output (MIMO) radar signal processing, integrated radar and communication, and mathematical optimization.

![](images/95eff7be9a99893faf4989dcee5bb144c7cbb34b35f3b7710c75729551b933e8.jpg)

Xiao Zhou is currently pursuing the B.Sc. degree in mathematics at The University of British Columbia, Vancouver, BC, Canada.

His learning interests include mathematical computing, machine learning, graph theory, and applied statistics.

![](images/6737b553e3229d977feff99fbcd69eb6538f2e41bab09f8a57396aaec3c91234.jpg)

Jiang Liu (Student Member, IEEE) received the B.S. degree in information engineering from Southeast University, Nanjing, China, in 2021, where he is currently pursuing the Ph.D. degree in electromagnetic fields and microwaves.

His main research interests are millimeter-wave radar signal processing and artificial intelligence information processing.

![](images/a075c532a4b1ea12d5637cf17e85220b22fffd659cb8d76abe2e99f729adf365.jpg)

Wei Hong (Fellow, IEEE) received the B.S. degree from the University of Information Engineering, Zhengzhou, China, in 1982, and the M.S. and Ph.D. degrees from Southeast University, Nanjing, China, in 1985 and 1988, respectively, all in radio engineering.

Since 1988, he has been with the State Key Laboratory of Millimeter Waves, Southeast University, where he has been the Director since 2003 and is currently a Professor with the School of Information Science and Engineering. In 1993 and from 1995 to 1998, he was a short-term Visiting Scholar with the University of California at Berkeley, Berkeley, CA, USA, and the University of California at Santa Cruz, Santa Cruz, CA, USA. He has been engaged in numerical methods for electromagnetic problems, millimeter-wave theory and technology, antennas, RF technology for wireless communications, and so on. He has authored or coauthored over 300 technical publications and two books.

Dr. Hong was an elected IEEE MTT-S AdCom Member from 2014 to 2016. He is a Fellow of Chinese Institution of Electronics (CIE). He was twice awarded the National Natural Prizes, thrice awarded the first-class Science and Technology Progress Prizes issued by the Ministry of Education of China and the Jiangsu Province Government, and so on. He also received the Foundations for China Distinguished Young Investigators and for Innovation Gro sued by the NSF of China. He is the Vice-President of the CIE Microwave Society and Antenna Society and the Chair of the IEEE MTT-S/AP-S/EMC-S Joint Nanjing Chapter. He has served as an Associate Editor for the IEEE TRANSACTIONS ON MICROWAVE THEORY AND TECHNIQUES from 2007 to 2010.