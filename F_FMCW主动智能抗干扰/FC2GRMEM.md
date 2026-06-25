#

Arindam Bose<sup>∗</sup>, Student Member, IEEE, Bo Tang<sup>∗</sup>, Wenjie Huang, Student Member, IEEE

Mojtaba Soltanalian<sup>†</sup>, Senior Member, IEEE, Jian Li<sup>†</sup>, Fellow, IEEE

## Abstract

The mutual interference between similar radar systems can result in reduced radar sensitivity and increased false alarm rates. To address the synchronous and asynchronous interference mitigation problems in similar radar systems, we first propose herein two slow-time coding schemes to modulate the pulses within a coherent processing interval (CPI) for a single-input-single-output (SISO) scenario. Specifically, the first coding scheme relies on Doppler shifting and the second one is devised based on an optimization approach. We further extend our discussion to the more general case of multiple-input-multiple-output (MIMO) radars and propose an efficient algorithm to design waveforms to mitigate mutual interference in such systems. The proposed coding schemes are computationally efficient in practice and the incorporation of the coding schemes requires only a slight modification of the existing systems. Our numerical examples indicate that the proposed coding schemes can reduce the interference power level in a desired area of the cross-ambiguity function significantly.

## Index Terms

Automotive radar systems, mutual interference mitigation, slow-time coding, code optimization, MIMO.

## I. INTRODUCTION

The radar technology exhibits an unmatched performance in a variety of vehicular applications, owing to its excellent target resolving capabilities in bad weather and low visibility conditions in comparison with visible and infrared imaging techniques [2]–[6]. In recent years, due to the benefits of exploiting the millimeter-wave (mm wave) band such as increased bandwidth, high spatial resolution, smaller size and weight of mm-wave equipment compared to ultrasonic radar and lidar, the mm-wave radars (30-300 GHz) have gained significant popularity not only in automotive radar systems but also in drone radar applications and internet of things (IoT) [7]–[9]. For instance, mm-wave radar equipment is much simpler than lidar’s complex mirrors and lasers, but far faster and more accurate than ultrasonic radars, and may use highly directional, high-frequency EM waves to map the surrounding environment [10], [11]. Given the tendency to mass-produce radars for civilian applications (e.g., automotive radars), such systems, however, tend to be quite similar, or even almost identical. The increasing number of similar or identical radar systems increases the probability of mutual interference, which may result in severely reduced radar sensitivity and poor performance quality [12]–[14]. Thus it is vitally important to enhance radar signal processing performance in severe mutual interference scenarios [15]–[18].

In the literature, the effects of mutual interference and their corresponding methods of mitigation have been discussed widely, e.g., see [19]–[31] and the references within. A judicious signal separation method for synchronous and asynchronous interference mitigation is proposed in [19]. The authors in [20] study the impact of radar waveform design and the associated receiver processing on the statistics of radar-to-radar interference and further propose an approach based on pseudo-random cyclic orthogonal sequences (PRCOS), which enable sensors to rapidly learn the interference environment and avoid using frequency overlapping waveforms. An iterative filtering algorithm followed by matched filtering for each radar has been suggested in [21] to suppress the radar-to-radar interferences. Furthermore, in [27], the authors analyzed the mutual interference between frequency-modulated continuous-wave (FMCW) radar systems and proposed several techniques to mitigate the interference problem, including pre-possessing and finite impulse response (FIR) filtering. Contrary to addressing the mutual interference in the receiver side, the authors in [22]–[24] investigated the problems between automotive radar systems with different types of transmissions.

In this paper, we address the mutual interference mitigation problem for similar or identical radar systems by using smart transmit waveforms. In particular, we consider a scenario where the manufacturer of the radar systems present in the scene is essentially the same; as a result, the radar parameters such as carrier frequency, slope, and the number of the chirps are assumed to be similar. It is true that in the real world, such a scenario is currently relatively rare. However, as more cars are equipped with radars, this may occur more frequently; something that can be dealt with through future regulations and shared protocols. We further assume that in such radar systems, it is possible to modify the custom waveforms used for transmission on-the-fly. Note that such a scenario can be avoided simply by “orthogonalization” of radar parameters. Designing waveforms, however, can make such a process more optimal, particularly when more than two vehicles are involved. In this sense, this work lays the ground for future sensible solutions in multi-vehicle scenarios.

To this end, we first formulate the problem of waveform designing for a simple single-input-single-output (SISO) case. Particularly, we propose two slow-time coding schemes to reduce the interference power level. Next, we extend our approach to the more general multiple-input-multiple-output (MIMO) scenario. Recently, there has been considerable interest in radar systems employing multiple antennas at both the transmitter and receiver; thus,

• We begin our study with the SISO case and propose two coding schemes to reduce the interference power level. The first coding scheme aims to shift the Doppler frequency of the interference and separate it from the target in the Doppler region. The second coding scheme aims to minimize the discrete periodic cross-ambiguity function (PCAF) in the desired area.

• We further formulate the problem of minimizing the discrete PCAF for a general MIMO scenario and propose an efficient cyclic algorithm to design the transmit waveforms.

Note that a distributed and mutually cooperative design protocol can be adopted for the online design of such waveforms in a collaborative manner. The design can also be done offline where the radar codes can be designed and stored in a centralized radar codebook for later usage. The discussion of such design coordination protocols is, however, beyond the scope of this work.

The rest of this paper is organized as follows. In Section II, we discuss the mutual interference for two identical frequency modulated continuous wave (FMCW) radar systems. We propose two coding schemes for the SISO scenario in Section III. Section IV is devoted to waveform design for the more general MIMO scenario. Numerical simulation results are presented in Section V. Finally, Section VI concludes our work.

Notation: We use bold-lowercase and bold-uppercase letters to represent vectors and matrices, respectively. $x _ { i }$ denotes the i-th element of the vector x. The superscripts $( \cdot ) ^ { * } , ( \cdot ) ^ { T }$ , and $( \cdot ) ^ { H }$ represent the conjugate, the transpose, and the Hermitian operators, respectively. The set of complex matrices are denoted by <sup>C</sup>. <{·} signifies the real part of a complex variable. The $\ell _ { p } .$ -norm is represented by $\| \cdot \| _ { p }$ . The Frobenius norm of the matrix X is denoted by $\| \mathbf { X } \| _ { F } . \mathbf { I } _ { N }$ is the identity matrix of size $N \times N$ , while 0 denotes the all-zero vector/matrix of given size. Diag (x) denotes a diagonal matrix formed whose diagonal elements are determined by the vector x. Finally,  represents the Hadamard product of matrices.

## II. PRELIMINARIES

In this section, we start by formulating the problem for a SISO scenario. Consider two identical FMCW radar systems shown in Fig. 1(a), that are operating within the same frequency band and same $B / T _ { c }$ ratio where B and $T _ { c }$ are the FMCW signal bandwidth and chirp time, respectively, as shown in Fig. 1(b). The transmitted signal can be expressed as

$$
s ( t ) = \sum _ { n = 0 } ^ { C - 1 } u ( t - n T _ { c } )\tag{1}
$$

![](images/3f29a91d42800e0c15c7380f055526f7a7f316bb94208c1bccd699062b829c4b.jpg)

(a)  
![](images/12d556a3522e14caef27f226fd0f44a3eca2ea896bd3827bda84100447b2a01f.jpg)  
(b)  
Fig. 1. Mutual interference between automotive radars: (a) potential source of mutual interference; (b) time-frequency illustration of the transmit waveform, the target signal, and the interference.

where $\begin{array} { r } { u ( t ) = \frac { 1 } { \sqrt { T _ { c } } } \exp \left( j ( 2 \pi f _ { c } t + \pi K t ^ { 2 } ) \right) } \end{array}$ rect $\scriptstyle \left( { \frac { t - T _ { c } } { T _ { c } } } \right)$ $f _ { c }$ is the carrier frequency, $C$ is the number of chirps, $K = B / T _ { c } ,$ , and

$$
\operatorname { r e c t } ( t ) = { \left\{ \begin{array} { l l } { 1 , } & { 0 \leq t \leq 1 , } \\ { 0 , } & { { \mathrm { e l s e w h e r e } } . } \end{array} \right. }
$$

When the two radar systems are operating simultaneously, the received signal by one radar includes not only the target reflections but also the interference signal due to the transmission from the other radar system. As a result, we can express the received signal by one radar $( e . g .$ , the radar mounted on Car 1 in Fig. 1(a)) as,

$$
r ( t ) = y _ { T } ( t ) + y _ { I } ( t ) + w ( t )\tag{2}
$$

where $y _ { T } ( t ) = \alpha _ { T } s ( t - \tau _ { T } ) \exp ( j \pi f _ { d , T } t )$ is the target return, and $y _ { I } ( t ) = \alpha _ { I } s ( t - \tau _ { I } ) \exp ( j \pi f _ { d , I } t )$ is the interference signal with $\alpha _ { T } , \alpha _ { I }$ being the corresponding amplitudes, $\tau _ { T }$ is the two-way target propagation delay, $\tau _ { I }$ is the oneway delay associated with the interference, $f _ { d , T } , f _ { d , I }$ are the corresponding Doppler frequencies, and $w ( t )$ is the internal disturbance, including, $e . g .$ , the receiver noise.

Typically, FMCW radar systems collect the received signal from N consecutive pulses within a coherent processing interval (CPI) for target detection and parameter estimation. The received signal is then conjugately mixed with the transmitted signal to produce a low-frequency intermediate (de-chirped) signal. As a result, the de-chirped

version of $r ( t )$ for the $n ^ { t h }$ (slow-time) pulse is given by

$$
\begin{array} { l } { r _ { d c } ^ { n } ( t ) = \alpha _ { T } \exp ( j 2 \pi ( f _ { B , T } t + n f _ { d , T } T _ { c } ) ) } \\ { ~ } \\ { ~ + \alpha _ { I } \exp ( j 2 \pi ( f _ { B , I } t + n f _ { d , I } T _ { c } ) ) + w ^ { n } ( t ) } \end{array}\tag{3}
$$

where $f _ { B , T } = K \tau _ { T } + f _ { d , T } , f _ { B , I } = K \tau _ { I } + f _ { d , I }$ are the beat frequencies corresponding to the target and the interference signal, respectively, and to lighten the notations, we absorb the constant phase terms into $\alpha _ { T }$ and $\alpha _ { I } .$ and use $w ^ { n } ( t )$ to denote the de-chirped noise.

The de-chirped signal is then passed through analog-to-digital converters (ADCs) and the $m ^ { t h }$ (fast-time) digital sample can be expressed as,

$$
\begin{array} { l } { { r ( m , n ) = \alpha _ { T } \exp ( j 2 \pi ( \hat { f } _ { B , T } m + \hat { f } _ { d , T } n ) ) } } \\ { { \phantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } } } \\ { { \phantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } + \alpha _ { I } \exp ( j 2 \pi ( \hat { f } _ { B , I } m + \hat { f } _ { d , I } n ) ) + w ( m , n ) } } \end{array}\tag{4}
$$

where $\hat { f } _ { B , T } = f _ { B , T } T _ { s } , \ \hat { f } _ { B , I } = f _ { B , I } T _ { s }$ are the corresponding normalized beat frequencies, $\hat { f } _ { d , T } = f _ { d , T } T _ { c } , \ \hat { f } _ { d , I } =$ $f _ { d , I } T _ { c }$ are the corresponding normalized Doppler frequencies, and $T _ { s } = 1 / f _ { s }$ , with $f _ { s }$ being the sampling frequency.

Applying 2-D FFT to (4) for $m = 1 , \cdots , M$ and $n = 1 , \cdots , N$ , we can obtain the range-Doppler image as,

$$
\begin{array} { r l } & { \mathrm { R D } ( k , p ) = \alpha _ { T } D _ { M } ( \hat { f } _ { B , T } - k / M ) D _ { N } ( \hat { f } _ { d , T } - p / N ) } \\ & { ~ + \alpha _ { I } D _ { M } ( \hat { f } _ { B , I } - k / M ) D _ { N } ( \hat { f } _ { d , I } - p / N ) + W ( k , p ) } \end{array}\tag{5}
$$

where $D _ { n } ( x ) = \sin ( n \pi x ) / \sin ( \pi x )$ is the Dirichlet function and $W ( k , p )$ represents the 2-D FFT of noise.

One can observe from (5) that the interference signal will form a sharp peak in the range-Doppler image. In particular, it is worth noting that, although the interference might be attributable to the transmission from the antenna sidelobe of one radar and receiving by the antenna sidelobe of the other, the potential interference level can be significantly higher than the target reflections due to the non-ideal antenna sidelobe characteristic. This is attributable to the one-way propagation characteristic of the interference signal and the direct (without reflection) blast from $\mathrm { o n e ^ { \prime } s }$ transmission to the other’s reception [1]. Specifically, according to the radar range-equation, the power of the target returns $( i . e . , | \alpha _ { T } | ^ { 2 } )$ can be determined by

$$
P _ { T , r } = \frac { P _ { t } G _ { T } ^ { 2 } \lambda ^ { 2 } \sigma _ { t } L _ { t } } { ( 4 \pi ) ^ { 3 } R _ { T } ^ { 4 } } ,\tag{6}
$$

where $P _ { t }$ is the system transmit power, $G _ { T }$ is the antenna gain in the target direction, $\lambda = c / f _ { c }$ is the wavelength, c is the light speed, $\sigma _ { t }$ is the radar cross section (RCS) of the target, $L _ { t }$ is the propagation loss, and $R _ { T }$ denotes the target range. The power of interference $( i . e . , | \alpha _ { I } | ^ { 2 } )$ is given by

$$
P _ { I , r } = \frac { P _ { t } G _ { t , I } G _ { r , I } \lambda ^ { 2 } L _ { I } } { ( 4 \pi ) ^ { 2 } R _ { I } ^ { 2 } } ,\tag{7}
$$

where we have assumed the two automotive radar systems have the same transmit power, $G _ { t , I }$ and $\boldsymbol { G } _ { r , I }$ denote the transmit and receive antenna gains associated with the interference, respectively, $L _ { I }$ denotes the propagation loss, and $R _ { I }$ is the range between the two radar systems. Thus, considering a target with RCS of $\mathrm { 1 m ^ { 2 } }$ and ignoring the propagation loss, we have the power ratio at the receiver input as,

$$
\frac { P _ { I , r } } { P _ { T , r } } = \frac { 4 \pi R _ { T } ^ { 4 } G _ { t , I } G _ { r , I } } { G _ { T } ^ { 2 } R _ { I } ^ { 2 } } .\tag{8}
$$

![](images/40f76067cc8aba5648a69d74c46efc56d4ca7c818c2ae45106ee87194dd7a56a.jpg)  
Fig. 2. An illustration of the SISO coding scheme for two radar systems operating under same FMCW parameters.

Therefore, the non-negligible interference power will result in serious interference for both automotive radar systems. In the following, we formulate the problem of mutual interference mitigation for a simple SISO scenario and then extend it to the MIMO case.

## III. SISO MUTUAL INTERFERENCE MITIGATION

$\mathbf { x } = [ x _ { 1 } , x _ { 2 } . \cdot \cdot , x _ { N } ] ^ { T } \mathrm { a n d } \mathbf { y } = [ y _ { 1 } , y _ { 2 } . \cdot \cdot , y _ { N } ] ^ { T }$ $n ^ { t h }$ $x _ { n } u ( t )$ $y _ { n } u ( t )$ $| x _ { n } | = | y _ { n } | = 1 , n = 1 , 2 , \cdot \cdot \cdot ~ ,$ $m ^ { t h }$ $n ^ { t h }$

$$
\begin{array} { r l } & { r ^ { c } ( m , n ) = \alpha _ { T } \exp ( j 2 \pi ( \hat { f } _ { B , T } m + \hat { f } _ { d , T } n ) ) } \\ & { ~ + ~ \alpha _ { I } x _ { n } ^ { * } y _ { ( n + l ) \bmod ~ N } \exp ( j 2 \pi ( \hat { f } _ { B , I } m + \hat { f } _ { d , I } n ) ) } \\ & { ~ + ~ w ( m , n ) . } \end{array}\tag{9}
$$

for correlation lags $l \in \{ - N { + } 1 , \cdots , N { - } 1 \}$ . The term l has been introduced here in order to allow for asynchronous transmission of two radars. The corresponding range-Doppler image, is thus given by

$$
\begin{array} { r } { \mathbf { R } \mathbf { D } ^ { c } ( k , p ) = \alpha _ { T } D _ { M } ( \hat { f } _ { B , T } - k / M ) D _ { N } ( \hat { f } _ { d , T } - p / N ) } \\ { + \alpha _ { I } D _ { M } ( \hat { f } _ { B , I } - k / M ) r _ { x y } ^ { l } ( \hat { f } _ { d , I } - p / N ) + W ( k , p ) , } \end{array}\tag{10}
$$

![](images/e3fd61c14e84f9151532d662ba23d2c0de3d7fee0341a914e4b1399c493be04e.jpg)  
(a)

![](images/8bfd586e8d1bb4073606c8d12ee05f0607d440ff980a2de3a78edc684244b00f.jpg)  
(b)  
Fig. 3. (a) The Doppler spectra of target and interference without coding and (b) the Doppler spectra of target and interference with Dopplershifting coding.

where

$$
r _ { x y } ^ { l } ( f ) = \sum _ { n = 1 } ^ { N } x _ { n } ^ { * } y _ { ( n + l ) \mathrm { m o d } \ N } \exp ( j 2 \pi n f )\tag{11}
$$

is the periodic cross-ambiguity function (PCAF) of x and y, and is to be minimized [37]–[39].

To suppress the interference power in the range-Doppler image, we aim at designing x and y to minimize $r _ { x y } ^ { l } ( f )$ within a range of interest for $f .$ To this end, we propose two methods to design x and y in the following subsections.

## A. The Doppler-Shifting Scheme

$f _ { D , I } \in [ - f _ { d , \operatorname* { m a x } } , f _ { d , \operatorname* { m a x } } ]$ $f _ { d , \mathrm { m a x } }$ $T _ { c } ,$

$$
\frac { - f _ { r } } { 2 } \leq f _ { d } \leq \frac { f _ { r } } { 2 } ,\tag{12}
$$

with $f _ { r } = 1 / T _ { c }$ (we can treat $f _ { r }$ as the pulse repetition frequency (PRF)). Assuming that $f _ { d , \mathrm { m a x } } \ \leq \ f _ { r } / 2$ , the possibly occupied Doppler frequencies of the interference signal can be illustrated in Fig. 3(a). We can observe that, without slow-time coding, the Doppler frequency of target reflections and interference signal might occupy the same area and it results in mutual interference.

In order to mitigate the interference in the Doppler region, we introduce a coding scheme to shift the Doppler spectrum of the interference signal into the high frequency area $( > f _ { d , \operatorname* { m a x } { } } \ \mathrm { o r } < - f _ { d , \operatorname* { m a x } { } } )$ . We call the resulting code the Doppler-shifting code. With such a coding scheme, it is possible to separate the target reflections and interference signal in the Doppler domain. As a result, we can apply low-pass filtering in the Doppler domain to mitigate the interference. To this end, we propose using the following codes to shift the Doppler spectrum of the interference signal:

$$
\mathbf { x } = [ 1 , 1 , \cdots , 1 ] ^ { T } ,\tag{13}
$$

$$
\begin{array} { r } { \mathbf { y } = \left\{ \begin{array} { l l } { [ 1 , - 1 , \cdots , - 1 , 1 ] ^ { T } , \mathrm { i f } \ N \ \mathrm { i s ~ o d d } , } \\ { [ 1 , - 1 , \cdots , 1 , - 1 ] ^ { T } , \mathrm { i f } \ N \ \mathrm { i s ~ e v e n } . } \end{array} \right. } \end{array}\tag{14}
$$

Note that, the two sequences are orthogonal for even N and quasi-orthogonal for odd N. It is easy to verify that,

$$
\begin{array} { l } { \displaystyle r _ { x y } ^ { l } | = \left| \sum _ { n = 1 } ^ { N } \exp ( j n \pi ) \exp ( j 2 \pi ( \hat { f } _ { d , I } - p / N _ { f } ) n ) \right| } \\ { \displaystyle ~ = \left| \sum _ { n = 1 } ^ { N } \exp ( j 2 \pi ( ( \hat { f } _ { d , I } + \frac 1 2 ) - p / N _ { f } ) n ) \right| } \\ { \displaystyle ~ = \left| \frac { \sin ( N \pi ( \hat { f } _ { d , I } + 1 / 2 - p / N _ { f } ) ) } { \sin ( \pi ( \hat { f } _ { d , I } + 1 / 2 - p / N _ { f } ) ) } \right| . } \end{array}\tag{15}
$$

Therefore, the above codes enable the automotive radar to shift the Doppler frequency of interference signal from $f _ { d , I }$ to $f _ { d , I } + f _ { r } / 2$ , as shown in Fig. 3(b). In particular, if $f _ { r }$ satisfies

$$
4 f _ { d , \operatorname* { m a x } } < f _ { r } ,\tag{16}
$$

we can isolate the target reflections and the interference signal in the Doppler domain with any Doppler frequency $f _ { D , I } \in [ - f _ { d , \operatorname* { m a x } } , f _ { d , \operatorname* { m a x } } ]$

On the other hand, note that the maximum value of the first sidelobe of the function $| \sin ( N \pi f ) / \sin ( \pi f ) |$ | equals

$$
\mathrm { S L L _ { 1 } } = { \frac { 1 } { \sin ( { \frac { 3 \pi } { 2 N } } ) } } \approx { \frac { 2 N } { 3 \pi } } ( \mathrm { f o r ~ l a r g e ~ } N ) .\tag{17}
$$

As a result, although the Doppler shifting coding scheme is simple, it may suffer from large sidelobes and the interference signal may not be extensively canceled. Furthermore, the condition in (16) may constrain the radar system to identify only the slow-moving vehicles.

## B. Optimized Coding Scheme for SISO Radars

In this subsection, we seek to optimize x and y such that the corresponding $| r _ { x y } ^ { l } ( f ) |$ has small values in a desired area. Given that the two radar systems usually have unsynchronized transmissions, the desired area should include all possible delays. Hence, we consider the following optimization problem with respect to (w.r.t.) the two codes x and y:

$$
\begin{array} { l } { \displaystyle \operatorname* { m i n } _ { { \bf x } , { \bf y } } \sum _ { l = - ( N - 1 ) } ^ { N - 1 } \sum _ { p = - P } ^ { P } | r _ { l p } | ^ { 2 } \qquad } \\ { \mathrm { s . t . } \qquad | x _ { n } | = 1 , ~ | y _ { n } | = 1 , ~ \forall n , } \end{array}\tag{18}
$$

where

$$
r _ { l p } = \sum _ { n = 1 } ^ { N } x _ { n } ^ { * } y _ { ( n + l ) \mathrm { m o d } \ N } \exp ( - j 2 \pi n p / N _ { f } )\tag{19}
$$

is the discrete PCAF with $N < N _ { f } , 0 < P < N _ { f } , N _ { f }$ is the overall number of discrete (Doppler) frequencies, and the value of P is closely related to the maximum Doppler frequency of interest and has to be chosen carefully so that multiple interferers can form peaks given they are all in the unambiguous region. After some algebraic manipulation, the criterion in (18) can be reformulated as

$$
\begin{array} { l } { { \displaystyle \operatorname* { m i n } _ { \mathbf { x } , \mathbf { y } } \sum _ { l = - ( N - 1 ) } ^ { N - 1 } \sum _ { p = - P } ^ { P } | \mathbf { x } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } \mathbf { y } | ^ { 2 } } } \\ { { \mathrm { s } . \mathrm { t } . \qquad | x _ { n } | = 1 , ~ | y _ { n } | = 1 , ~ \forall n , } } \end{array}\tag{20}
$$

where $\mathbf { C } _ { l } = \mathbf { C } _ { - l } ^ { T } = \left\lceil \mathbf { 0 } \quad \mathbf { I } _ { N - l } \right\rceil$ is a circular shift matrix and $n ^ { t h }$ element of $\mathbf { f } _ { p }$ is $\exp ( - j 2 \pi n p / N _ { f } )$

$s ^ { t h }$ $\mathbf { y } ^ { ( s - 1 ) }$ $\mathbf { x } ^ { ( s ) }$ $\mathbf { y } ^ { ( s - 1 ) }$ $\mathbf { x } ^ { ( s ) }$

## • Optimization of x for fixed y:

The associated optimization problem can be recast as

$$
\begin{array} { l } { \displaystyle \operatorname* { m i n } _ { \mathbf { x } } \mathbf { x } ^ { H } \mathbf { B } _ { y } \mathbf { x } , } \\ { \mathrm { s } . \mathrm { t } . } \end{array}\tag{21}
$$

where

$$
\mathbf { B } _ { y } = \sum _ { l = - N + 1 } ^ { N - 1 } \sum _ { p = - P } ^ { P } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } \mathbf { y } \mathbf { y } ^ { H } \mathbf { C } _ { l } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) ^ { H } .\tag{22}
$$

$\gamma _ { y }$ $\mathbf { B } _ { y }$ ${ \bf D } _ { y } = \gamma _ { y } { \bf I } _ { N } - { \bf B } _ { y } \succ { \bf 0 } \ ( i . e . , { \bf D } _ { y }$

$$
\begin{array} { l } { { \displaystyle \operatorname* { m a x } _ { \bf x } { \bf x } ^ { H } { \bf D } _ { y } { \bf x } } , } \\ { ~ } \\ { { \displaystyle \mathrm { s . t . } ~ | x _ { n } | = 1 , ~ n = 1 , 2 , \cdots , N } . } \end{array}\tag{23}
$$

In the $t ^ { t h }$ (inner) iteration, we update x by using the following power-method-like iterations (PMLI):

$$
\mathbf { x } ^ { ( s , t ) } = \exp ( j \arg ( \mathbf { D } _ { y } \mathbf { x } ^ { ( s , t - 1 ) } ) ) .\tag{24}
$$

• Optimization of y for fixed x:

The optimization of y for fixed x is formulated as follows:

$$
\begin{array} { l } { { \displaystyle \operatorname* { m i n } _ { \mathbf { y } } \mathbf { y } ^ { H } \mathbf { B } _ { x } \mathbf { y } } , } \\ { ~ } \\ { { \displaystyle \mathrm { s . t . } ~ | y _ { n } | = 1 , n = 1 , 2 , \cdots , N } , } \end{array}\tag{25}
$$

where

$$
\mathbf { B } _ { x } = \sum _ { l = - N + 1 } ^ { N - 1 } \sum _ { p = - P } ^ { P } \mathbf { C } _ { l } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) ^ { H } \mathbf { x x } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } .\tag{26}
$$

Similar to the previous case, we can tackle the optimization problem in (25) iteratively. Specifically, the solution in the $t ^ { t h }$ (inner) iteration is given by

$$
\mathbf { y } ^ { ( s , t ) } = \exp ( j \arg ( \mathbf { D } _ { x } \mathbf { y } ^ { ( s , t - 1 ) } ) ) ,\tag{27}
$$

where ${ \bf D } _ { x } = \gamma _ { x } { \bf I } _ { N } - { \bf B } _ { x }$ and $\gamma _ { x }$ is a positive constant larger than the maximum eigenvalue of $\mathbf { B } _ { x }$ to ensure $\mathbf { D } _ { x } \succ \mathbf { 0 }$ Finally, the steps of the proposed algorithm to minimize the discrete PCAF for two identical SISO systems is summarized in Algorithm 1.

Remark 1. (Optimality and the Convergence): The optimization problem in (20) is NP-hard and multimodal, i.e., the objective has multiple local optima [47]. Due to the non-convex nature of the objective function, one usually settles for an approximation algorithm that yields local optima. In the proposed approach, we tackle the non-convexity of the problem by resorting to a cyclic minimization algorithm. In each half of the cycle, we optimize for one set of variables keeping the other fixed, and these two subproblems are solved based on a local optimization method, namely PMLI for UQP, that yields good local optima [43]. From (20), it can be deduced that the objective value is lower bounded at 0. Furthermore, from (21) and (25), we know that for s-th iteration

$$
\mathbf { x } ^ { ( s + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { x } \in \Omega _ { x } } \mathbf { x } ^ { H } \mathbf { B } _ { y } ^ { ( s ) } \mathbf { x } , \mathrm { ~ a n d }\tag{28}
$$

$$
\mathbf { y } ^ { ( s + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { y } \in \Omega _ { y } } \ \mathbf { y } ^ { H } \mathbf { B } _ { x } ^ { ( s + 1 ) } \mathbf { y } .\tag{29}
$$

where $\Omega _ { z } ~ = ~ \{ { \bf z } ~ | ~ | z _ { n } | ~ = ~ 1 , \forall n \}$ . Therefore, one can conclude that, in each iteration the objective value is monotonically decreasing, and that the algorithm converges. 

Remark 2. (Computational Complexity): Note that, in the code optimization, one needs to calculate $\mathbf { B } _ { x }$ and $\mathbf { B } _ { y }$ at each iteration. Specifically, in the computation of $\mathbf { B } _ { y }$ , we need N complex multiplications to obtain Diag $( \mathbf { f } _ { p } )$ C<sub>l</sub>y (whose $n ^ { t h }$ element is $e ^ { - j 2 \pi n p / N _ { f } } y _ { ( n + l ) }$ <sub>mod N</sub> ). As a result, the overall computational complexity of computing $\mathbf { B } _ { y }$ is of the order $\mathcal { O } \left( N _ { f } ( 2 N - 1 ) ( N ^ { 2 } + N ) \right)$ . Similarly, the overall computational complexity of computing $\mathbf { B } _ { x }$ is of the order $\mathcal { O } \left( N _ { f } ( 2 N - 1 ) ( N ^ { 2 } + N ) \right)$ , which seems to be quite high. In Appendix A, we provide a computationally fast and inexpensive way to calculate $\mathbf { B } _ { x }$ and $\mathbf { B } _ { y }$ 

In what follows, we extend our discussion to the more general case of MIMO automotive radar systems.

Algorithm 1 Automotive Radar Waveform Design Algorithm for Mutual Interference Mitigation (SISO Case)   
Initialize: $\mathbf { x } ^ { ( 0 ) } , \mathbf { y } ^ { ( 0 ) } , s = 0$   
Output: $\mathbf { x } ^ { \star } , \mathbf { y } ^ { \star }$   
1: repeat   
2: $s \gets s + 1$   
Update of $\mathbf { x } ^ { ( s ) } \colon$   
3: Calculate $\mathbf { B } _ { y } ^ { ( s ) }$ with (22)   
4: $t = 0 , \mathbf { x } ^ { ( s , t ) } = \mathbf { x } ^ { ( s - 1 ) }$   
5: repeat   
6: $\mathbf { x } ^ { ( s , t ) } = \exp ( j \arg ( ( \gamma _ { y } ^ { ( s ) } \mathbf { I } _ { N } - \mathbf { B } _ { y } ^ { ( s ) } ) \mathbf { x } ^ { ( s , t - 1 ) } ) )$   
7: $t \gets t + 1$   
8: until convergence   
9: $\mathbf { x } ^ { ( s ) } = \mathbf { x } ^ { ( s , t ) }$   
Update of $\mathbf { y } ^ { ( s ) } ;$   
10: Calculate $\mathbf { B } _ { x } ^ { ( s ) }$ with (26)   
11: $t = 0 , \mathbf { y } ^ { ( s , t ) } = \mathbf { y } ^ { ( s - 1 ) }$   
12: repeat   
13: ${ \bf y } ^ { ( s , t ) } = \exp ( j \arg ( ( \gamma _ { x } ^ { ( s ) } { \bf I } _ { N } - { \bf B } _ { x } ^ { ( s ) } ) { \bf y } ^ { ( s , t - 1 ) } ) )$   
14: t ← t + 1   
15: until convergence   
16: $\mathbf { y } ^ { ( s ) } = \mathbf { y } ^ { ( s , t ) }$   
17: until a pre-defined stop criterion is satisfied, e.g., $| J ^ { ( s ) } - J ^ { ( s - 1 ) } | \le \epsilon ,$ , for some $\epsilon > 0$ where J denotes the   
objective function of the problem (20)   
18: $\mathbf { x } ^ { \star } = \mathbf { x } ^ { ( s ) } , \mathbf { y } ^ { \star } = \mathbf { y } ^ { ( s ) }$

## IV. EXTENSION TO THE GENERALIZED MIMO SCENARIO

In a MIMO scenario, the mutual interference stems not only from the waveforms of a similar radar system nearby, but also from the various waveforms transmitted by the same radar system. In this case, our optimization problem for radar waveform design can be formulated as

$$
\begin{array} { r l } & { \underset { \{ \mathbf { x } _ { m } \} , \{ \mathbf { y } _ { k } \} } { \operatorname* { m i n } } \sum _ { m , k } \underset { l = - ( N - 1 ) } { \sum } \overset { N - 1 } { \underset { p = - P } { \sum } } \left\{ | \mathbf { x } _ { m } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } \mathbf { y } _ { k } | ^ { 2 } + \right. } \\ & { \qquad \left. | \mathbf { x } _ { m } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } \mathbf { x } _ { m } | ^ { 2 } + | \mathbf { y } _ { k } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } \mathbf { y } _ { k } | ^ { 2 } \right\} } \\ & { \mathrm { s . t . } \quad \quad \mathbf { x } _ { m } \mathrm { a n d } \mathbf { y } _ { k } \mathrm { a r e } \mathrm { u n i m o d u l a r } \mathrm { f o r } \mathrm { a l l } m , k , } \end{array}\tag{30}
$$

in which $\{ \mathbf { x } _ { m } \} _ { m = 1 } ^ { M }$ and $\{ \mathbf { y } _ { k } \} _ { k = 1 } ^ { K }$ are the codes used for modulation on different antennas of the two radar systems. Note that the first term of (30) accounts for the mutual interference of different radar systems while the second and

third terms account for the self-interference among the waveforms transmitted in the same radar systems. Let

$$
\mathbf { A } _ { l , p } \triangleq \operatorname { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } ,\tag{31}
$$

$$
\mathbf { X } = [ \mathbf { x } _ { 1 } , \cdots , \mathbf { x } _ { M } ] ,\tag{32}
$$

$$
\mathbf { Y } = [ \mathbf { y } _ { 1 } , \dots , \mathbf { y } _ { K } ] ,\tag{33}
$$

and note that the objective in (30) can be written in a compact form as

$$
\begin{array} { r l } {  { Q ( \mathbf { X } , \mathbf { Y } ) } } \\ & { = \sum _ { l , p } \| { \mathbf { X } } ^ { H } \mathbf { A } _ { l , p } \mathbf { X } \| _ { F } ^ { 2 } + \| \mathbf { Y } ^ { H } \mathbf { A } _ { l , p } \mathbf { Y } \| _ { F } ^ { 2 } + \| \mathbf { X } ^ { H } \mathbf { A } _ { l , p } \mathbf { Y } \| _ { F } ^ { 2 } . } \end{array}\tag{34}
$$

Tackling (34) appears to be more difficult than the optimization problem formulated in the SISO case in (18), as the new objective is quartic in both radar codes (X and Y) and the fact that the number of PCAF values to be suppressed is growing more quickly in terms of the problem dimension than the number of design variables. In the following, we formulate a quadratic alternative to (30) that can be tackled more efficiently.

## A. The Quartic to Quadratic Transformation

In order to recast the problem in a quadratic form, let

$$
\begin{array} { l } { { \displaystyle { \bf A } _ { l , p } ^ { r } = \frac { 1 } { 2 } ( { \bf A } _ { l , p } + { \bf A } _ { l , p } ^ { H } ) } , } \\ { { \displaystyle { \bf A } _ { l , p } ^ { i } = \frac { 1 } { 2 } ( { \bf A } _ { l , p } - { \bf A } _ { l , p } ^ { H } ) } } \end{array}\tag{35}
$$

and note that

1) Both matrices $\mathbf { A } _ { l , p } ^ { r }$ and $j \mathbf { A } _ { l , p } ^ { i }$ are Hermitian [47].

2) For any generic vector z,

$$
\mathbf { z } ^ { H } \mathbf { A } _ { l , p } \mathbf { z } = \mathbf { z } ^ { H } \mathbf { A } _ { l , p } ^ { r } \mathbf { z } + \mathbf { z } ^ { H } \mathbf { A } _ { l , p } ^ { i } \mathbf { z }\tag{36}
$$

where

$$
\begin{array} { r } { \mathbf { z } ^ { H } \mathbf { A } _ { l , p } ^ { r } \mathbf { z } \in \mathbb { R } , \qquad j \mathbf { z } ^ { H } \mathbf { A } _ { l , p } ^ { i } \mathbf { z } \in \mathbb { R } . } \end{array}\tag{37}
$$

In particular it follows from the above that

$$
\begin{array} { r } { | { \bf z } ^ { H } { \bf A } _ { l , p } { \bf z } | ^ { 2 } = | { \bf z } ^ { H } { \bf A } _ { l , p } ^ { r } { \bf z } | ^ { 2 } + | { \bf z } ^ { H } j { \bf A } _ { l , p } ^ { i } { \bf z } | ^ { 2 } . } \end{array}\tag{38}
$$

We particularly observe that the quartic behavior of (30) and (34) stems from self-interference terms:

$$
\{ | \mathbf { x } _ { m } ^ { H } \mathbf { A } _ { l , p } \mathbf { x } _ { m } | ^ { 2 } \} , \{ | \mathbf { y } _ { k } ^ { H } \mathbf { A } _ { l , p } \mathbf { y } _ { k } | ^ { 2 } \}\tag{39}
$$

for all $m \in \{ 1 , \cdots , M \}$ and $k \in \{ 1 , \cdots , K \}$

Based on (35)-(38), one can write

$$
\begin{array} { l } { { \displaystyle \sum _ { l , p } \left. \mathbf { x } _ { m } ^ { H } \mathbf { A } _ { l , p } \mathbf { x } _ { m } \right. ^ { 2 } = \sum _ { l , p } \vert \mathbf { x } _ { m } ^ { H } \mathbf { A } _ { l , p } ^ { r } \mathbf { x } _ { m } \vert ^ { 2 } + \vert \mathbf { x } _ { m } ^ { H } j \mathbf { A } _ { l , p } ^ { i } \mathbf { x } _ { m } \vert ^ { 2 } } } \\ { ~ = \sum _ { l , p } \vert \mathbf { x } _ { m } ^ { H } ( \mathbf { A } _ { l , p } ^ { r } + \zeta \mathbf { I } _ { N } ) \mathbf { x } _ { m } - \zeta N \vert ^ { 2 } } \\ { ~ + \vert \mathbf { x } _ { m } ^ { H } ( j \mathbf { A } _ { l , p } ^ { i } + \zeta \mathbf { I } _ { N } ) \mathbf { x } _ { m } - \zeta N \vert ^ { 2 } } \\ { ~ = \sum _ { l , p } \vert \mathbf { x } _ { m } ^ { H } \tilde { \mathbf { A } } _ { l , p } ^ { r } \mathbf { x } _ { m } - \zeta N \vert ^ { 2 } } \\ { ~ + \vert \mathbf { x } _ { m } ^ { H } \tilde { \mathbf { A } } _ { l , p } ^ { i } \mathbf { x } _ { m } - \zeta N \vert ^ { 2 } , } \end{array}\tag{40}
$$

where

$$
\begin{array} { r l } & { \tilde { \mathbf { A } } _ { l , p } ^ { r } = \mathbf { A } _ { l , p } ^ { r } + \zeta \mathbf { I } _ { N } , } \\ & { } \\ & { \tilde { \mathbf { A } } _ { l , p } ^ { i } = j \mathbf { A } _ { l , p } ^ { i } + \zeta \mathbf { I } _ { N } , } \end{array}\tag{41}
$$

and $\zeta \in \mathbb { R }$ is chosen such that

$$
\zeta > - \operatorname* { m i n } \left( \bigcup _ { l , p } \left\{ \gamma _ { \mathrm { m i n } } \left( \mathbf { A } _ { l , p } ^ { r } \right) , \gamma _ { \mathrm { m i n } } \left( j \mathbf { A } _ { l , p } ^ { i } \right) \right\} \right)\tag{42}
$$

to ensure the positive definiteness of $\{ \tilde { \mathbf { A } } _ { l , p } ^ { r } \}$ and $\{ \tilde { \mathbf { A } } _ { l , p } ^ { i } \}$ , where $\gamma _ { \mathrm { m i n } } ( \cdot )$ denotes the minimum eigenvalue of its matrix argument. Observe that the quantity in (40) is still quartic w.r.t. $\mathbf { x } _ { m } .$ , which in fact is difficult to minimize. A quadratic alternative, however, can be proposed in the following manner. Note that the quantity in (40) will be made small when the quadratic quantities $\{ \mathbf { x } _ { m } ^ { H } \tilde { \mathbf { A } } _ { l , p } ^ { r } \mathbf { x } _ { m } \}$ and $\{ \mathbf { x } _ { m } ^ { H } \tilde { \mathbf { A } } _ { l , p } ^ { i } \mathbf { x } _ { m } \}$ are close to $\zeta N$ . This is only possible when unit-norm vectors $\{ \mathbf { u } _ { l , p , m } ^ { r } \}$ and $\{ \mathbf { u } _ { l , p , m } ^ { i } \}$ exist such that $( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { x } _ { m }$ is close to $\sqrt { \zeta N } \mathbf { u } _ { l , p , m } ^ { r }$ , and likewise $( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { x } _ { m }$ is close to $\sqrt { \zeta N } \mathbf { u } _ { l , p , m } ^ { i }$ . As a result, minimization of (40) can be approached by a reformulation, in the form of the following alternative quadratic optimization problem [48]–[51]:

$$
\begin{array} { r l } { \operatorname* { m i n } } & { \displaystyle \sum _ { l , p } \bigg \{ \bigg \| ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { x } _ { m } - \sqrt { \zeta N } \mathbf { u } _ { l , p , m } ^ { r } \bigg \| _ { 2 } ^ { 2 } } \\ & { \qquad + \left\| ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { x } _ { m } - \sqrt { \zeta N } \mathbf { u } _ { l , p , m } ^ { i } \right\| _ { 2 } ^ { 2 } \bigg \} } \end{array}
$$

s.t. ${ \bf x } _ { m }$ are unimodular for all $m _ { \colon }$

$$
\lVert \mathbf { u } _ { l , p , m } ^ { r } \rVert _ { 2 } = \lVert \mathbf { u } _ { l , p , m } ^ { i } \rVert _ { 2 } = 1 \mathrm { ~ f o r ~ a l l ~ } l , p , m .\tag{43}
$$

Thus the criteria in (40) and (43) are “almost equivalent” in the sense that their minimization is likely to lead to signals with similar properties in terms of mutual interference. Interestingly, one can observe that (43) is quadratic instead of quartic— a transformation that was made possible by judicious over-parametrization. In a similar manner,

we argue that $\{ | \mathbf { y } _ { k } ^ { H } \mathbf { A } _ { l , p } \mathbf { y } _ { k } | ^ { 2 } \}$ can be made small by solving the alternative problem:

$$
\begin{array} { r l } { \operatorname* { m i n } } & { \displaystyle \sum _ { l , p } \bigg \{ \Big \| ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { y } _ { k } - \sqrt { \zeta N } \mathbf { v } _ { l , p , k } ^ { r } \Big \| _ { 2 } ^ { 2 } } \\ & { \qquad + \left\| ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { y } _ { k } - \sqrt { \zeta N } \mathbf { v } _ { l , p , k } ^ { i } \right\| _ { 2 } ^ { 2 } \bigg \} } \end{array}
$$

s.t. $\mathbf { y } _ { k }$ are unimodular for all $k ,$

$$
\lVert \mathbf { v } _ { l , p , k } ^ { r } \rVert _ { 2 } = \lVert \mathbf { v } _ { l , p , k } ^ { i } \rVert _ { 2 } = 1 \mathrm { ~ f o r ~ a l l ~ } l , p , k .\tag{44}
$$

As a result, the objective in (30) can be recast in its almost-equivalent quadratic form as described in (45) which is shown on the top of the next page. Note that the optimization problem in (45) is still non-convex, especially

$$
\begin{array} { r l } { \underset { \{ \mathbf { u } _ { l , p , k } ^ { \prime } \} , \{ \mathbf { v } _ { k } ^ { k } \} , \ n } { \operatorname* { m i n } } \ } & { \displaystyle \sum _ { l , p } \sum _ { m \neq k } \{ | \mathbf { x } _ { m } ^ { H } \mathbf { A } _ { l , p } \mathbf { x } _ { k } | ^ { 2 } + | \mathbf { y } _ { m } ^ { H } \mathbf { A } _ { l , p } \mathbf { y } _ { k } | ^ { 2 } \} + \displaystyle \sum _ { l , p } \sum _ { m , k } \{ | \mathbf { x } _ { m } ^ { H } \mathbf { A } _ { l , p } \mathbf { y } _ { k } | ^ { 2 } \} } \\ { \{ \mathbf { u } _ { l , p , k } ^ { \prime } \} , \{ \mathbf { u } _ { l , p , k } ^ { \prime } \} } \\ & { + \ \displaystyle \sum _ { l , p } \left[ \displaystyle \sum _ { m } \left\{ \left\| ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { x } _ { m } - \sqrt { \zeta N } \mathbf { u } _ { l , p , m } ^ { r } \right\| _ { 2 } ^ { 2 } + \left\| ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { x } _ { m } - \sqrt { \zeta N } \mathbf { u } _ { l , p , m } ^ { i } \right\| _ { 2 } ^ { 2 } \right\} \right] } \\ & { + \displaystyle \sum _ { k } \left\{ \left\| ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { y } _ { k } - \sqrt { \zeta N } \mathbf { v } _ { l , p , k } ^ { r } \right\| _ { 2 } ^ { 2 } + \left\| ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { y } _ { k } - \sqrt { \zeta N } \mathbf { v } _ { l , p , k } ^ { i } \right\| _ { 2 } ^ { 2 } \right\} } \end{array}
$$

s.t. $\mathbf { x } _ { m }$ and $\mathbf { y } _ { k }$ are unimodular for all $m , k .$

$$
\begin{array} { r l } & { \| \mathbf { u } _ { l , p , m } ^ { r } \| _ { 2 } = \| \mathbf { u } _ { l , p , m } ^ { i } \| _ { 2 } = 1 \mathrm { ~ f o r ~ a l l ~ } l , p , m , } \\ & { \| \mathbf { v } _ { l , p , k } ^ { r } \| _ { 2 } = \| \mathbf { v } _ { l , p , k } ^ { i } \| _ { 2 } = 1 \mathrm { ~ f o r ~ a l l ~ } l , p , k . } \end{array}\tag{45}
$$

because of the unimodular constraints imposed on $\left\{ { \bf x } _ { m } \right\}$ and $\left\{ \mathbf { y } _ { k } \right\}$ . In the following subsection, we provide an efficient way to tackle the above problem for all individual optimization variables.

## B. The Optimization Procedure

In order to efficiently tackle the problem in (45), we resort to a cyclic optimization framework. Namely, we iteratively optimize the criterion with respect to one of the variables while keeping the rest of them fixed. In $s ^ { t h }$ iteration, we separate each variable $\{ \mathbf { x } _ { m } \} , \{ \mathbf { y } _ { k } \} , \{ \mathbf { u } _ { l , p , m } ^ { c } \} , \{ \mathbf { v } _ { l , p , k } ^ { c } \}$ for all $m \in \{ 1 , \cdots , M \} , k \in \{ 1 , \cdots , K \} , l \in$ $\{ - ( N - 1 ) , \cdots , N - 1 \} , p \in \{ - P , \cdots , P \} , c \in \{ r , i \}$ from the objective function in (45) and optimize them individually while fixing all other variables to their values from $( s - 1 ) ^ { t h }$ iteration. In the following subsections, we describe such a process of variable separation and the corresponding solution techniques. We drop the superscript (s) for notational simplicity.

## • Optimization of $\lbrace \mathbf { x } _ { m } \rbrace _ { m = 1 } ^ { M } \colon$

We begin by reformulating the optimization problem in (45) w.r.t. each of $\mathbf { x } _ { m }$ for all $m$ . Eliminating all the other variables that do not depend on $\mathbf { x } _ { m }$ , the objective function in (45) becomes what is described in (46), shown on the top of the next page, or simply,

$$
\begin{array} { r l } & { Q _ { \mathbf { x } _ { m } } = \underbrace { \mathbf { x } _ { \underbrace { m } } ^ { H } \left( \sum _ { m ^ { \prime } \neq m } \sum _ { l , p } { \mathbf { A } _ { l , p } \mathbf { x } _ { m ^ { \prime } } \mathbf { A } _ { l , p } ^ { H } } \right) \mathbf { x } _ { m } } _ { M - 1 \mathrm { ~ t r m s } } + \underbrace { \mathbf { x } _ { m } ^ { H } \left( \sum _ { k } \sum _ { l , p } { \mathbf { A } _ { l , p } \mathbf { y } _ { k } \mathbf { y } _ { k } ^ { H } \mathbf { A } _ { l , p } ^ { H } } \right) \mathbf { x } _ { m } } _ { K \mathrm { ~ t e m s } } + \mathbf { x } _ { m } ^ { H } \left( \sum _ { l , p } { \tilde { \mathbf { A } } _ { l , p } ^ { r } } + { \tilde { \mathbf { A } } _ { l , p } ^ { i } } \right) \mathbf { x } _ { m } } \\ & { \qquad - 2 \sqrt { \zeta N } \Re \left\{ \mathbf { x } _ { m } ^ { H } \sum _ { l , p } ^ { \mathrm { ( } } \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { H / 2 } \mathbf { u } _ { l , p , m } ^ { r } \right\} - 2 \sqrt { \zeta N } \Re \left\{ \mathbf { x } _ { m } ^ { H } \sum _ { l , p } ^ { \mathrm { ( } } \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { H / 2 } \mathbf { u } _ { l , p , m } ^ { i } \right\} + \mathrm { c o n s t . } \qquad ( 4 6 ) } \end{array}
$$

$$
Q _ { { \bf { x } } _ { m } } = { \bf { x } } _ { m } ^ { H } { \bf { R } } _ { { \bf { x } } _ { m } } { \bf { x } } _ { m } + 2 \Re \{ { \bf { x } } _ { m } ^ { H } { \bf { s } } _ { { \bf { x } } _ { m } } \} + \mathrm { c o n s t . } ,\tag{47}
$$

where

$$
\begin{array} { l } { { \displaystyle { \bf R } _ { { \bf x } _ { m } } = \sum _ { m ^ { \prime } \neq m } \sum _ { l , p } { \bf A } _ { l , p } { \bf x } _ { m ^ { \prime } } { \bf x } _ { m ^ { \prime } } ^ { H } { \bf A } _ { l , p } ^ { H } + \sum _ { k } \sum _ { l , p } { \bf A } _ { l , p } { \bf y } _ { k } { \bf y } _ { k } ^ { H } { \bf A } _ { l , p } ^ { H } } } \\ { { \displaystyle \qquad + \sum _ { l , p } \tilde { \bf A } _ { l , p } ^ { r } + \tilde { \bf A } _ { l , p } ^ { i } } } \end{array}\tag{48}
$$

and

$$
\begin{array} { r l } {  { \mathbf { s } _ { \mathbf { x } _ { m } } = } } \\ & { - \sqrt { \zeta N } \sum _ { l , p } ( ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { H / 2 } \mathbf { u } _ { l , p , m } ^ { r } + ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { H / 2 } \mathbf { u } _ { l , p , m } ^ { i } ) . } \end{array}\tag{49}
$$

By dropping the constant term in (47), the objective function can be reformulated as,

$$
\begin{array} { r l } & { { { Q } _ { { \bf { x } } _ { m } } } = { { \bf { x } } _ { m } ^ { H } } { { \bf { R } } _ { { \bf { x } } _ { m } } } { { \bf { x } } _ { m } } + 2 \Re \{ { { \bf { x } } _ { m } ^ { H } } { { \bf { s } } _ { { \bf { x } } _ { m } } } \} } \\ & { ~ = \left[ { { { \bf { x } } _ { m } } } \right] ^ { H } \left[ \begin{array} { c c } { { { \bf { R } } _ { { \bf { x } } _ { m } } } } & { { { \bf { s } } _ { { \bf { x } } _ { m } } } } \\ { { { \bf { \bf { s } } } _ { { \bf { x } } _ { m } } ^ { H } } } & { 0 } \end{array} \right] \left[ \begin{array} { c } { { { \bf { x } } _ { m } } } \\ { 1 } \end{array} \right] } \\ & { ~ = \bar { { { \bf x } } } _ { m } ^ { H } { { \bf { B } } _ { { \bf { x } } _ { m } } } \bar { { { \bf x } } } _ { m } } \end{array}\tag{50}
$$

where

$$
\begin{array} { r } { \bar { \mathbf x } _ { m } \triangleq [ \mathbf x _ { m } ~ 1 ] ^ { T } , } \end{array}\tag{51}
$$

$$
\begin{array} { r } { \mathbf { B } _ { \mathbf { x } _ { m } } \triangleq \left[ \begin{array} { c c } { \mathbf { R } _ { \mathbf { x } _ { m } } } & { \mathbf { s } _ { \mathbf { x } _ { m } } } \\ { \mathbf { s } _ { \mathbf { x } _ { m } } ^ { H } } & { 0 } \end{array} \right] . } \end{array}\tag{52}
$$

Hence, the minimization of (45) w.r.t. $\mathbf { x } _ { m }$ is equivalent to the following,

$$
\begin{array} { l } { \underset { \bar { \mathbf { x } } _ { m } } { \mathrm { m i n } } ~ \bar { \mathbf { x } } _ { m } ^ { H } \mathbf { B } _ { \mathbf { x } _ { m } } \bar { \mathbf { x } } _ { m } } \\ { \mathrm { s } . \mathrm { t } . ~ | x _ { n } ( m ) | = 1 , ~ n = 1 , \cdots , N , } \end{array}
$$

$$
\bar { \mathbf { x } } _ { m } = \left[ \mathbf { x } _ { m } \right] .\tag{53}
$$

As a result of the unimodular constraint on $\mathbf { x } _ { m } ,$ the term $\bar { \mathbf { x } } _ { m }$ also has a constant $\ell _ { 2 } { \mathrm { - n o r m } }$ , and hence, a diagonal loading of $\mathbf { B } _ { \mathbf { x } _ { m } }$ will not change the solution to the above problem [47]. Therefore, (53) can be rewritten in the following equivalent form:

$$
\begin{array} { r l } & { \underset { { { \bar { \mathbf { x } } } _ { m } } } { \operatorname* { m a x } } ~ { \bar { \mathbf { x } } } _ { m } ^ { H } \mathbf { D } _ { \mathbf { x } _ { m } } { \bar { \mathbf { x } } } _ { m } } \\ & { \mathrm { s } . \mathrm { t } . ~ | x _ { n } ( m ) | = 1 , ~ n = 1 , \cdots , N , } \end{array}
$$

$$
\bar { \mathbf { x } } _ { m } = \left[ \mathbf { x } _ { m } \right] ,\tag{54}
$$

where

$$
\mathbf { D } _ { \mathbf { x } _ { m } } \triangleq \gamma _ { \mathbf { x } _ { m } } \mathbf { I } _ { ( N + 1 ) } - \mathbf { B } _ { \mathbf { x } _ { m } } ,\tag{55}
$$

with $\gamma _ { \mathbf { x } _ { m } }$ being larger than the maximum eigenvalue of $\mathbf { B } _ { \mathbf { x } _ { m } }$ . Note that the above problem similarly belongs to the family of UQPs [43], and can be efficiently tackled in an iterative manner using power-method-like iterations of the form [47]:

$$
\mathbf { x } _ { m } ^ { ( s , t ) } = \exp \left\{ j \arg \left( \left[ \mathbf { I } _ { N \times N } \right] ^ { T } \mathbf { D } _ { \mathbf { x } _ { m } } \bar { \mathbf { x } } _ { m } ^ { ( s , t - 1 ) } \right) \right\} ,\tag{56}
$$

where the iterations can be initialized with the latest design of $\mathbf { x } _ { m }$ (used as $\mathbf { x } _ { m } ^ { ( s , 0 ) } )$ and t denotes the inner iteration number.

## • Optimization of $\{ \mathbf { y } _ { k } \} _ { k = 1 } ^ { K } ;$

In order to solve (45) for $\mathbf { y } _ { k }$ for all $k ,$ we follow the same algebraic manipulation with slight modifications. In this case, the objective function, $Q _ { \mathbf { y } _ { k } }$ , becomes

$$
Q _ { { \bf { y } } _ { k } } = { \bf { y } } _ { k } ^ { H } { \bf { R } } _ { { \bf { y } } _ { k } } { \bf { y } } _ { k } + 2 \Re \{ { \bf { y } } _ { k } ^ { H } { \bf { s } } _ { { \bf { y } } _ { k } } \} + \mathrm { c o n s t . }\tag{57}
$$

where

$$
\begin{array} { l } { { \displaystyle { \bf R } _ { { \bf y } _ { k } } = \sum _ { k ^ { \prime } \neq k } \sum _ { l , p } { \bf A } _ { l , p } { \bf y } _ { k ^ { \prime } } { \bf y } _ { k ^ { \prime } } ^ { H } { \bf A } _ { l , p } ^ { H } } + \sum _ { m } \sum _ { l , p } { \bf A } _ { l , p } ^ { H } { \bf x } _ { m } { \bf x } _ { m } ^ { H } { \bf A } _ { l , p } } \\ { { \displaystyle \quad \quad \quad + \sum _ { l , p } { \tilde { \bf A } } _ { l , p } ^ { r } + { \tilde { \bf A } } _ { l , p } ^ { i } } } \end{array}\tag{58}
$$

and

$$
\begin{array} { l } { { \displaystyle { \bf s _ { y } } _ { k } = } } \\ { { \displaystyle - \sqrt { \zeta N } \sum _ { l , p } \left( ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { H / 2 } { \bf v } _ { l , p , k } ^ { r } + ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { H / 2 } { \bf v } _ { l , p , k } ^ { i } \right) . } } \end{array}\tag{59}
$$

As a result, we can formulate a UQP for each $\mathbf { y } _ { k }$ in a similar manner. The corresponding solution can be approached iteratively using the power-method-like recursions of the form

$$
\mathbf { y } _ { k } ^ { ( s , t ) } = \exp \left\{ j \arg \left( \left[ \mathbf { I } _ { N \times N } \right] ^ { T } \mathbf { D } _ { \mathbf { y } _ { k } } \bar { \mathbf { y } } _ { k } ^ { ( s , t - 1 ) } \right) \right\} ,\tag{60}
$$

where

$$
\mathbf { D } _ { \mathbf { y } _ { k } } \triangleq \gamma _ { \mathbf { y } _ { k } } \mathbf { I } _ { ( N + 1 ) } - \mathbf { B } _ { \mathbf { y } _ { k } }\tag{61}
$$

with $\gamma _ { \mathbf { y } _ { k } }$ being larger than the maximum eigenvalue of $\mathbf { B } _ { \mathbf { y } _ { k } }$ , and

$$
\bar { \mathbf { y } } _ { k } \triangleq [ \mathbf { y } _ { k } \mathbf { \Theta } ^ { 1 } ] ^ { T }\tag{62}
$$

$$
\begin{array} { r } { \mathbf { B } _ { \mathbf { y } _ { k } } \triangleq \left[ \begin{array} { c c } { \mathbf { R } _ { \mathbf { y } _ { k } } } & { \mathbf { s } _ { \mathbf { y } _ { k } } } \\ { \mathbf { s } _ { \mathbf { y } _ { k } } ^ { H } } & { 0 } \end{array} \right] . } \end{array}\tag{63}
$$

• Optimization of $\{ \mathbf { u } _ { l , p , m } ^ { c } \}$ and $\{ \mathbf { v } _ { l , p , k } ^ { c } \}$

Solving (45) w.r.t. $\{ \mathbf { u } _ { l , p , m } ^ { c } \}$ and $\{ \mathbf { v } _ { l , p , k } ^ { c } \}$ for $c \in \{ r , i \}$ is immediate and resolves into closed-form solution as follows:

$$
\widehat { \mathbf { u } } _ { l , p , m } ^ { r } = \frac { ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { x } _ { m } } { \| ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { x } _ { m } \| _ { 2 } } ,\tag{64}
$$

$$
\widehat { \mathbf { u } } _ { l , p , m } ^ { i } = \frac { ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { x } _ { m } } { \| ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { x } _ { m } \| _ { 2 } } ,\tag{65}
$$

$$
\widehat { \mathbf { v } } _ { l , p , k } ^ { r } = \frac { ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { y } _ { k } } { \| ( \tilde { \mathbf { A } } _ { l , p } ^ { r } ) ^ { 1 / 2 } \mathbf { y } _ { k } \| _ { 2 } } ,\tag{66}
$$

$$
\widehat { \mathbf { v } } _ { l , p , k } ^ { i } = \frac { ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { y } _ { k } } { \| ( \tilde { \mathbf { A } } _ { l , p } ^ { i } ) ^ { 1 / 2 } \mathbf { y } _ { k } \| _ { 2 } } ,\tag{67}
$$

for all $m \in \{ 1 , \cdots , M \} , k \in \{ 1 , \cdots , K \} , l \in \{ - ( N - 1 ) , \cdots , N - 1 \} , p \in \{ - P , \cdots , P \}$

Finally, the steps of the proposed algorithm for interference mitigation in the MIMO setting is summarized in Algorithm 2.

Remark 3. (Convergence): As mentioned earlier for Algorithm 1, the Algorithm 2 as well resorts to a cyclic optimization method to tackle the non-convexity of the problem (45). For each iteration of Algorithm 2, one can observe that the objective value is monotonically decreasing and bounded from below, leading to the convergence of the algorithm. Note that the final output of the cyclic algorithms often depends on the initialization of all the optimization variables. Different initial points in the search space may lead to different final designs due to the non-convexity of the landscape. For this reason, it is desirable to run Algorithm 2 multiple times. A good candidate can be using the output of the current design as the initialization for the next design. 

Remark 4. (Computational Complexity and Parallelization): Note that, in the step 3 of the Algorithm 2, the calculation of $\tilde { \mathbf { A } }$ requires $\mathcal { O } \left( N _ { f } ( 2 N - 1 ) ( N + N ^ { 3 } ) \right)$  number of complex multiplications. The term $N ^ { 3 }$ comes from the eigenvalue decomposition of the $N \times N$ matrix A. Furthermore, the overall computational complexity of calculating $\mathbf { D } _ { \mathbf { x } _ { m } }$ and $\mathbf { D } _ { \mathbf { y } _ { k } }$ is $\mathcal { O } \left( ( M + K ) N _ { f } ( 2 N - 1 ) [ ( M + K - 1 ) N + N ^ { 3 } ] \right)$ . However, it is interesting to note that the computation of A<sup>˜</sup> is required only once in the entire optimization procedure and can be performed in parallel. Moreover, in the $s ^ { t h }$ iteration of the algorithm, solving for $\{ \mathbf { u } _ { l , p , m } ^ { c ( s ) } \} , \{ \mathbf { v } _ { l , p , k } ^ { c ( s ) } \}$ can also be done in paralle making the algorithm significantly more efficient from a computational viewpoint. 

It is interesting to note that the SISO objective considered in (20) is not a special case of the MIMO counterpart in (30) as the objective in (20) does not take the self-interference terms into account. However, (30) can be reduced to a SISO scenario assuming $M = K = 1$ as stated in the following:

$$
\underset { \ b { x } , \mathbf { y } } { \mathop { \operatorname* { m i n } } } \underset { l = - ( N - 1 ) } { \sum } \sum _ { p = - P } ^ { N - 1 } \left\{ | \mathbf { x } ^ { H } \mathrm { D i a g } \left( \mathbf { f } _ { p } \right) \mathbf { C } _ { l } \mathbf { y } | ^ { 2 } + \right.
$$

s.t. x and y are unimodular,

(68)

where both the self-interference and mutual interference terms are included in the objective, and can be minimized efficiently using Algorithm 2. In the next section, several numerical examples are provided to showcase the performance and efficiency of the proposed waveform design schemes.

## V. NUMERICAL EXAMPLES

In the following, we begin with demonstrating the effectiveness of the two coding schemes described in Section III for the SISO scenario using several examples. We then provide a similar numerical analysis for the MIMO case detailed in Section IV.

## A. The SISO Scenario

Consider two identical FMCW radar systems with the same carrier frequency of $f _ { \mathrm { c } } = 2 4 ~ \mathrm { G H z } .$ . The bandwidth of the chirp signal is B = 150 MHz. The sweep time is $T _ { c } = 5 0 ~ \mu \mathrm { s }$ . The number of periods within a CPI is $N = 2 5 6 .$ we initialize our algorithm with normally distributed randomly generated codes (for x and y, respectively,) in the optimized coding scheme.

In Fig. 4(a) and 4(b), the discrete PCAFs are shown for a pair of Doppler-shifting codes, and the optimized codes, respectively, where $P = 2 0 0$ and $N _ { f } = 5 1 2$ (which implies that the maximum Doppler frequency of interest should be lower than 3906.25 Hz, corresponding to a maximum relative radial velocity of 87.9 km/h). In addition, Fig. 4(c) and 4(d) show the PCAFs when one of the vehicles uses an optimized code and the other uses a non-cooperative code such as the all-one vector. It is clear from the figure that a non-cooperating interfering radar present in the scenario may ultimately fail to decrease the sidelobe in the desired region.

Fig. 5 compares the discrete periodic cross-ambiguity functions at the zero-delay cut for the above scenarios. One can observe that both Doppler shifting and optimized coding schemes achieve very low sidelobes in the desired area compared to random codes. Moreover, although the optimized scheme achieves lower sidelobes in the desired area, the sidelobe increases in the regions outside the desired area. However, for the Doppler shift coding, the sidelobes are spread evenly throughout the entire region. Therefore, they can be used to effectively suppress the interference. Further note that the peak side-lobe level (PSL) corresponding to the optimized codes is approximately 3.55 dB lower than that of the Doppler-shifting, within the desired range of Doppler frequency of interest. Interestingly, if we fix $\mathbf { y } = \mathbf { 1 } _ { N }$ and only optimize x, we obtain similar results, which corresponds to a scenario where no coordination between the two radar systems is required.

![](images/7c74b5df28f1530b37daddbb9780f138151c3ddc039810b95c1a4d89747fb6b7.jpg)  
(a)

![](images/6db7e0968378072978a2e3feeac70d258ddae5fea87514564896f8e5b4c36710.jpg)  
(b)

![](images/12bd0c44308a40451531db42b4f541d716bb89a03fc7be6ed1ee3016f59a02a9.jpg)  
(c)

![](images/ab78bbc8c87af47ce5a0bb8e3ee49f200a24848646e21c0fb9eb28a3d120dcd4.jpg)  
(d)

Fig. 4. Discrete periodic cross-ambiguity functions for (a) a pair of Doppler-shift codes, (b) a pair of the optimized codes x and y, (c) optimized code x and an all-one code, and (d) an all-one code and optimized code y, for N = 256, $P = 2 0 0$ and $N _ { f } = 5 1 2 .$  
![](images/87d89c29f97af5a923557bebfcb443d36d7778948d93180a8f9d2e060d0f2835.jpg)  
Fig. 5. Comparison of the discrete periodic cross-ambiguity functions at the zero-delay cut for different scenarios for $N = 2 5 6 , P = 2 0 0$ and $N _ { f } = 5 1 2 .$ . Although the optimized scheme achieves lower sidelobes in the desired area, the sidelobe increases in the regions outside the desired area.

Next, we examine the performance of the optimized SISO codes for different values of P . In order to preserve the fairness in this experiment, we fix the maximum outer iteration number of Algorithm 1 to 1000 for each P .

![](images/25d83da374dba77a76a43781530a482e36c6faf64325b124b7a5ce262bd752c2.jpg)  
Fig. 6. Comparison of the discrete PCAFs at the zero-delay cut for the optimized SISO codes with $P \in \{ 5 0 , 1 0 0 , 1 5 0 , 2 0 0 , 2 5 0 \}$ , $N = 2 5 6$ and $N _ { f } = 5 1 2$

$P \in \{ 5 0 , 1 0 0 , 1 5 0 , 2 0 0 , 2 5 0 \}$

We, next, apply these coding schemes to mitigate the mutual interference for two identical automotive radar systems operating in a typical scenario: The range of target and interference are at 50 m and 70 m, respectively. The speeds associated with them are 10.12 m/s and 23.45 m/s. The signal-to-noise ratios (SNR) are 30 dB and 60 dB, respectively. The sampling frequency is $f _ { s } = 4 ~ \mathrm { M H z } .$ $M = 1 0 0$ samples are collected for each period. Fig. 7 (a-c) show the range-Doppler image in this scenario without slow-time coding, using Doppler-shifting code, and the optimized coding scheme, respectively. Furthermore, Fig. 7 (d-e) show the same for Doppler-shifting code and the optimized coding scheme when the SNRs are 10 dB and 20 dB for the target and interferer, respectively. We can observe that the power of the interference is much stronger than that of the target such that a false alarm occurs. When our slow-time coding schemes are applied, the interference power level is significantly reduced and the target can be easily detected without suffering from false alarm problems.

## B. The MIMO Scenario

$\mathcal { X } = \{ \mathbf { x } _ { m } \} _ { m = 1 } ^ { 2 } \mathrm { a n d } \ \mathcal { Y } = \{ \mathbf { y } _ { k } \} _ { k = 1 } ^ { 3 }$ $N = 2 5 6 .$ $f _ { c } = 2 4$ $B = 1 5 0 ~ \mathrm { M H z }$ $T _ { c } = 5 0 ~ \mu \mathrm { s }$

![](images/c471b93a717832da708f179b5bc198a53eace7c09718500ed1210be99f4afcda.jpg)  
(a)

![](images/a393ea3afcbaafded44404fa4c490062b9abba511db35624a8ac2441ef0e331b.jpg)  
(b)

![](images/65f9a8912d8e297a5808157f3e59cafeeaa884642399d6d1f4a3451238ae44bb.jpg)  
(c)

![](images/7961b7f9f639eebdab1cd26bdd34eb793d965b2884c8198de0a0f2a7a09adeb2.jpg)

(d)  
![](images/87b63d2175c994082807bd8f72257dcb7a58c0dc0b95e389b0e36f353726bbcc.jpg)  
(e)  
Fig. 7. The range-Doppler image for (a) randomly generated code without slow-time coding, (b) Doppler-shift coding, and (c) the optimized coding scheme for the SNRs of target and interferer as 30 dB and 60 dB, respectively. Furthermore, the same for (d) Doppler-shift coding, and (e) the optimized coding scheme for the SNRs of target and interferer as 10 dB and 20 dB, respectively: represents the target and <sup></sup> represents the interference.

all optimization variables: $\{ \mathbf { x } _ { m } \} , \{ \mathbf { y } _ { k } \} \ \{ \mathbf { u } _ { l , p , m } ^ { c } \} , \{ \mathbf { v } _ { l , p , k } ^ { c } \}$ , for $c \in \{ r , i \}$ . After running the algorithm once, we use the output codes $\{ \mathbf { x } _ { m } \} , \{ \mathbf { y } _ { k } \}$ as the initial codes for the next run but we still use random initialization for other variables, $\{ \mathbf { u } _ { l , p , m } ^ { c } \} , \{ \mathbf { v } _ { l , p , k } ^ { c } \}$ , and repeat the process multiple times.

Figs. 8-10 show the periodic (cross) ambiguity functions for the radar systems: $\{ \mathcal { X } \} , \{ \mathcal { V } \}$ , and $\{ \mathcal { X } , \mathcal { Y } \}$ where $P = 2 0 0$ and $N _ { f } = 5 1 2$ . It is evident from each of these figures that for each set of sequences, the unambiguous regions are well separated (within the range of -40dB to -60dB), and hence, these sequences can be reliably used in MIMO FMCW radar systems that require mutual interference mitigation.

In the next example for the MIMO case, we apply the optimized coding scheme to mitigate the mutual interference in the presence of multiple targets. For this scenario, we use three targets and one interfering radar system. The ranges of the targets and interference are at 50, 20, 60 m, and 70 m, respectively. The speeds associated with them are 10.12, −5.75, 7.34 m/s and 23.45 m/s. The SNRs are 30 dB and 60 dB for the targets and interference, respectively. The sampling frequency is similarly $f _ { s } = 4 ~ \mathrm { M H z }$ as assumed in the SISO case. Fig. 11 shows the range-Doppler (RD) image for different scenarios. The RD images are shown for randomly generated MIMO codes without slow-time coding, and the optimized MIMO coding scheme in Fig. 11(a) and 11(b), respectively. It is clea from the figure that the interference power level for the optimized codes is significantly reduced and all three of the targets are easily detected without suffering from false alarm issues. Furthermore, Fig. 11(c) shows the RD image when the interferer uses a non-cooperating all-one vector code as described in the SISO case. It is interesting to see that the presence of a strong interferer that does not respect the code usage protocol may significantly hinder the target detection capabilities.

![](images/0f4a5dd6918c69c49294f75f4eb612b7b407539614ae3d1ab54286f5d2c624dd.jpg)

![](images/cb6badbf38ce44088438462d17065e555c7964190be27973eaa1cd28c6d0b434.jpg)

![](images/8808a3223526619a11740d91662c217b63a0ea808c9b7dee53de050b7b8a57c1.jpg)

![](images/8afa406f9f716afd763087ffd9a0960cd15b9389b12837acbcc829665bb5a303.jpg)  
Fig. 8. Discrete periodic (cross) ambiguity functions between different MIMO sequences from the set ${ \mathcal X } = \{ \mathbf { x } _ { m } \} _ { m = 1 } ^ { 2 }$ for $N = 2 5 6$ $P = 2 0 0$ and $N _ { f } = 5 1 2$ . Note that for identical sequences, the ambiguity function always assumes larger values near zero.

![](images/47071a02e43ea8d35f523d08e229d6b5b3f10d0271a9b0aedb39adb6db700aea.jpg)

![](images/8a0a01d88cbec9e77ab8a557776c9e51a744f0f516ce5add0a88b5ce23226bab.jpg)

![](images/91227dd4c8e7c8833adf404cc9e3855cf2b061d5adec8c525411f6b3e0e27367.jpg)

![](images/ecee37c15e6e68cdfd5ca777eab64320425c6754291b644630c3f444a8f364af.jpg)

![](images/539891f2375ed4e743ef4c2d96a97b87cff263ae3eca431bcacdd0ac26b98df9.jpg)

![](images/d27129ff907170f79f85dbd3852d37d98cbd9d74f986a60badadc4822b8e0fbe.jpg)

![](images/41c6db30e63576ad8dc486f118a0c40c1cdc29fbb1f2ee8182f6f2bcff6d0bdd.jpg)

![](images/4bce7775c300519900ab1c09ae2373b60c97ede6e1487e83042a56b7a526e41c.jpg)

![](images/038d596efce4a40fb2d9e9511ed5c24e91be551ee47a58e190b1ebe81c198753.jpg)  
Fig. 9. Discrete periodic (cross) ambiguity functions among different MIMO sequences from the set $\mathcal { Y } = \{ \mathbf { y } _ { k } \} _ { k = 1 } ^ { 3 }$ for $N = 2 5 6$ , P = 200 and $N _ { f } = 5 1 2$

![](images/54b1cdc800eeb52971badba90f08e89c34d5dc0b2cc6caba46d6788229affc92.jpg)  
Fig. 10. Discrete periodic cross-ambiguity functions between different MIMO sequences from the set $\mathcal { X } = \{ \mathbf { x } _ { m } \} _ { m = 1 } ^ { 2 }$ and $\mathcal { Y } = \{ \mathbf { y } _ { k } \} _ { k = 1 } ^ { 3 }$ for N = 256, P = 200 and $N _ { f } = 5 1 2$

## VI. CONCLUSION

In this paper, we discussed the problem of mutual interference mitigation in identical or similar radar system employed in automotive applications. We proposed two slow-time coding schemes for the SISO case. Specifically, the first coding scheme is designed through Doppler shifting and the second one is devised based on an efficient cyclic optimization approach. We further extended the problem formulation and proposed another efficient algorithm to generate the radar codes in the more general MIMO scenario. We showed that these coding schemes can be used to reduce the interference power level significantly. Note that these coding schemes are highly effective when the radar parameters are nearly identical, however, the requirement of having identical parameters is not necessary.

![](images/c5934e2ade519f7e9f2398fb7010fa87c7f961f431e5edc8edfe43002780e9a7.jpg)  
(a)

![](images/3d05feb76284e2342e0d6e0f114c25b917118d63bf1ed0204ae463d77a352eaa.jpg)

(b)  
![](images/dc1210af50b8f269e3dde9a96b49eaff0e25d0d1618c94ef9280fedeef36e700.jpg)  
(c)  
Fig. 11. The range-Doppler image for (a) randomly generated MIMO codes without slow-time coding, (b) the optimized MIMO coding scheme, and (c) optimized MIMO scheme, however the interferer uses a non-cooperating all-one vector code: $\bigcirc$ represents the targets and <sup></sup> represents the interference.

## APPENDIX A

## EFFICIENT COMPUTATION OF $\mathbf { B } _ { x }$ AND $\mathbf { B } _ { y }$

Note that $\mathbf { B } _ { y }$ in (22) can be rewritten as

$$
\mathbf { B } _ { y } = \sum _ { p = - P } ^ { P } \operatorname { D i a g } \left( \mathbf { f } _ { p } \right) \left( \sum _ { l = - N + 1 } ^ { N - 1 } \mathbf { C } _ { l } \mathbf { y } \mathbf { y } ^ { H } \mathbf { C } _ { l } ^ { H } \right) \operatorname { D i a g } \left( \mathbf { f } _ { p } \right) ^ { H } .\tag{69}
$$

Define $\begin{array} { r } { { \mathbf { R } } = \sum _ { l = - N + 1 } ^ { N - 1 } { \mathbf { C } _ { l } } { \mathbf { y } } { \mathbf { y } } ^ { H } { \mathbf { C } } _ { l } ^ { H } } \end{array}$ . It is easy to verify ${ \bf R } _ { y } = 2 { \bf R } _ { 0 } - { \bf y } { \bf y } ^ { H }$ , considering that for $l < 0 , \mathbf { C } _ { l } \mathbf { y } = \mathbf { C } _ { N - l } \mathbf { y }$ and $\begin{array} { r } { { \bf R } _ { 0 } = \sum _ { l = 0 } ^ { N - 1 } { \bf C } _ { l } { \bf y } { \bf y } ^ { H } { \bf C } _ { l } ^ { H } } \end{array}$ . Moreover, we can write ${ \bf R } _ { 0 }$ as

$$
\mathbf { R } _ { 0 } = \mathbf { Y } \mathbf { Y } ^ { H } ,\tag{70}
$$

where

$$
\mathbf { Y } = \left[ \begin{array} { c c c c c c } { y _ { 1 } } & { y _ { 2 } } & { \cdots } & { y _ { N - 1 } } & { y _ { N } } \\ { y _ { 2 } } & { y _ { 3 } } & { \cdots } & { y _ { N } } & { y _ { 1 } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } & { \vdots } \\ { y _ { N } } & { y _ { 1 } } & { \cdots } & { y _ { N - 2 } } & { y _ { N - 1 } } \end{array} \right] .\tag{71}
$$

As a result, $\mathbf { R } _ { 0 }$ can be written as

$$
\mathbf { R } _ { 0 } = \left[ \begin{array} { c c c c c c } { c _ { y , 0 } } & { c _ { y , 1 } } & { \cdots } & { c _ { y , N - 2 } } & { c _ { y , N - 1 } } \\ { c _ { y , 1 } ^ { * } } & { c _ { y , 0 } } & { \cdots } & { c _ { y , N - 3 } } & { c _ { y , N - 2 } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } & { \vdots } \\ { c _ { y , N - 1 } ^ { * } } & { c _ { y , N - 2 } ^ { * } } & { \cdots } & { c _ { y , 1 } ^ { * } } & { c _ { y , 0 } } \end{array} \right] ,
$$

where $\begin{array} { r } { c _ { y , l } = \sum _ { n = 1 } ^ { N } y _ { n } y _ { ( n + l ) \mathrm { m o d } N } ^ { * } , l = 0 , 1 , \cdots , N - 1 } \end{array}$ . It should be noted that ${ \bf R } _ { 0 }$ is a circulant matrix and its elements are determined by the values of the sequence $\{ c _ { y , l } \} _ { l = 0 } ^ { N - 1 }$ . Moreover, this sequence can be seen as the circular convolution between $\{ y _ { n } \} _ { n = 1 } ^ { N }$ and $\{ y _ { n } \} _ { n = 1 } ^ { N }$ , and hence can be efficiently computed via FFT operations. Therefore, the computation of $\mathbf { R } _ { y }$ requires $\mathcal { O } \left( N ^ { 2 } \right)$ flops (mainly due to the computation of $\mathbf { y } \mathbf { y } ^ { H } )$ ).

It follows that $\mathbf { B } _ { y }$ can be calculated efficiently using the following result:

$$
\begin{array} { r l } & { { \bf B } _ { y } = \displaystyle \sum _ { p = - P } ^ { P } \mathrm { D i a g } \left( { \bf f } _ { p } \right) R _ { y } \mathrm { D i a g } \left( { \bf f } _ { p } \right) ^ { H } } \\ & { \quad = \displaystyle \sum _ { p = - P } ^ { P } { \bf R } _ { y } \odot \left( { \bf f } _ { p } { \bf f } _ { p } ^ { H } \right) } \\ & { \quad = { \bf R } _ { y } \odot \left( { \bf F } _ { P } { \bf F } _ { P } ^ { H } \right) , } \end{array}\tag{72}
$$

where $\mathbf { F } _ { P } = [ \mathbf { f } _ { - P } , \therefore \cdot \cdot , \mathbf { f } _ { P } ] \in \mathbb { C } ^ { N \times ( 2 P + 1 ) }$

Finally, we consider reducing the computational complexity of computing $\mathbf { B } _ { x }$ . To this end, we note that

$$
\begin{array} { r l } & { \mathbf { B } _ { x } = \displaystyle \sum _ { l = - N + 1 } ^ { N - 1 } { \mathbf { C } _ { l } ^ { H } \left( \displaystyle \sum _ { p = - P } ^ { P } { \mathrm { D i a g } \left( { \mathbf { f } _ { p } } \right) ^ { H } \mathbf { x x } ^ { H } \mathrm { D i a g } \left( { \mathbf { f } _ { p } } \right) } \right) \mathbf { C } _ { l } } } \\ & { \quad \quad = \displaystyle \sum _ { l = - N + 1 } ^ { N - 1 } { \mathbf { C } _ { l } ^ { H } \left( \left( \mathbf { x x } ^ { H } \right) \odot \left( \mathbf { F } _ { P } ^ { * } \mathbf { F } _ { P } ^ { T } \right) \right) \mathbf { C } _ { l } } . } \end{array}\tag{73}
$$

Let $\mathbf { R } _ { x } = ( \mathbf { x } \mathbf { x } ^ { H } ) \odot ( \mathbf { F } _ { P } ^ { * } \mathbf { F } _ { P } ^ { T } )$ . We can observe that ${ \bf C } _ { l } ^ { H } { \bf R } _ { x } { \bf C } _ { l }$ can be computed very efficiently, since it only involves the permutation of the rows and columns of $\mathbf { R } _ { x }$ . Therefore, the computation of $\mathbf { B } _ { y }$ only requires $\mathcal { O } \left( N ^ { 2 } \right)$ flops.

## REFERENCES

[1] B. Tang, W. Huang, and J. Li, “Slow-time coding for mutual interference mitigation,” in 2018 IEEE International Conference on Acoustics Speech and Signal Processing (ICASSP), 2018, pp. 6508–6512.

[2] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 22–35, 2017.

[3] Martin Schneider, “Automotive radar: Status and trends,” in In Proceedings of the German Microwave Conference GeMIC 2005, 2005, pp. 144–147.

[4] H. Rohling, “Milestones in radar and the success story of automotive radar systems,” in 11-th International Radar Symposium, 2010, pp. 1–6.

[5] J. Dickmann, J. Klappstein, M. Hahn, N. Appenrodt, H. Bloecher, K. Werber, and A. Sailer, “Automotive radar the key technology for autonomous driving: From detection and ranging to environmental understanding,” in IEEE Radar Conference (RadarConf), 2016, pp 1–6.

[6] Fulvio Gini, Antonio De Maio, and Lee Patton, Waveform design and diversity for advanced radar systems, Institution of engineering and technology, London, 2012.

[7] Jaime Lien, Nicholas Gillian, M. Emre Karagozler, Patrick Amihood, Carsten Schwesig, Erik Olson, Hakim Raja, and Ivan Poupyrev, “Soli: Ubiquitous gesture sensing with millimeter wave radar,” ACM Trans. Graph., vol. 35, no. 4, July 2016.

[8] Saiwen Wang, Jie Song, Jaime Lien, Ivan Poupyrev, and Otmar Hilliges, “Interacting with soli: Exploring fine-grained dynamic gesture recognition in the radio-frequency spectrum,” in Proceedings of the 29th Annual Symposium on User Interface Software and Technology, New York, NY, USA, 2016, UIST ’16, p. 851–860, Association for Computing Machinery.

[9] Sergio Saponara, Maria Sabrina Greco, and Fulvio Gini, “Radar-on-chip/in-package in autonomous driving vehicles and intelligent transport systems: opportunities and challenges,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 71–84, 2019.

[10] Maria S Greco, Jian Li, Teng Long, and Abdelhak Zoubir, “Advances in radar systems for modern civilian and commercial applications: Part 1 [from the guest editors],” IEEE Signal Processing Magazine, vol. 36, no. 4, pp. 13–15, 2019.

[11] Maria S Greco, Jian Li, Teng Long, and Abdelhak Zoubir, “Advances in radar systems for modern civilian and commercial applications: Part 2 [from the guest editors],” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 16–18, 2019.

[12] F. Engels, P. Heidenreich, A. M. Zoubir, F. K. Jondral, and M. Wintermantel, “Advances in automotive radar: A framework on computationally efficient high-resolution frequency estimation,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 36–46, 2017.

[13] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 20–31, 2019.

[14] Shahin Khobahi, Arindam Bose, and Mojtaba Soltanalian, “Deep radar waveform design for efficient automotive radar sensing,” in 11th IEEE Sensor Array and Multichannel Signal Processing Workshop, 2020.

[15] S. H. Dokhanchi, B. S. Mysore, K. V. Mishra, and B. Ottersten, “A mmwave automotive joint radar-communications system,” IEEE Transactions on Aerospace and Electronic Systems, vol. 55, no. 3, pp. 1241–1260, 2019.

[16] S. Sedighi, B. Shankar, K. V. Mishra, and B. Ottersten, “Optimum design for sparse FDA-MIMO automotive radar,” in 2019 53rd Asilomar Conference on Signals, Systems, and Computers, 2019, pp. 913–918.

[17] S. H. Dokhanchi, M. R. Bhavani Shankar, K. V. Mishra, and B. Ottersten, “Multi-constraint spectral co-design for colocated MIMO radar and MIMO communications,” in Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 4567–4571.

[18] M. Alaee-Kerahroodi, B. Shankar, M. M. Naghsh, and B. Ottersten, “CDM-MIMO in next-generation mmWave automotive radar sensors,” in Proceedings of URSI AP-RASC, 2019.

[19] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[20] Sruthy Skaria, Akram Al-Hourani, Robin J Evans, Kandeepan Sithamparanathan, and Udaya Parampalli, “Interference mitigation in automotive radars using pseudo-random cyclic orthogonal sequences,” Sensors (Basel, Switzerland), vol. 19, no. 20, pp. 4459, Oct 2019.

[21] Wen-Qin Wang and Huaizong Shao, “Radar-to-radar interference suppression for distributed radar sensor networks,” Remote Sensing, vol. 6, no. 1, pp. 740–755, 2014.

[22] M. Goppelt, H. L. Blocher, and W. Menzel, “Automotive radar - investigation of mutual interference mechanisms,” ¨ Advances in Radio Science, vol. 8, pp. 55–60, Sept. 2010.

[23] M. Goppelt, H. L. Blocher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,”¨ in 2011 German Microwave Conference, 2011, pp. 1–4.

[24] A. Bourdoux, K. Parashar, and M. Bauduin, “Phenomenology of mutual interference of FMCW and PMCW automotive radars,” in 201 IEEE Radar Conference (RadarConf), 2017, pp. 1709–1714.

[25] M. A. Hossain, I. Elshafiey, and A. Al-Sanie, “Mutual interference mitigation in automotive radars under realistic road environments,” in 2017 8th International Conference on Information Technology (ICIT), 2017, pp. 895–900.

[26] Canan Aydogdu, Musa Furkan Keskin, Gisela K. Carvajal, Olof Eriksson, Hans Hellsten, Hans Herbertsson, Emil Nilsson, Mats Rydstrom Karl Vanas, and Henk Wymeersch, “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Processing Magazine, vol. 37, no. 4, pp. 72–84, 2020.

[27] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[28] S. Rao and A. V. Mani, “Interference characterization in FMCW radars,” in 2020 IEEE Radar Conference (RadarConf20), 2020, pp. 1–6.

[29] P. Wang, D. Millar, K. Parsons, and P. V. Orlik, “Nonlinearity correction for range estimation in FMCW millimeter-wave automotive radar,” in IEEE MTT-S International Wireless Symposium (IWS), 2018, pp. 1–3.

[30] P. Wang, P. Boufounos, H. Mansour, and P. V. Orlik, “Slow-time MIMO-FMCW automotive radar detection with imperfect waveform separation,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 8634–8638.

[31] M. Soltanalian and P. Stoica, “Design of perfect phase-quantized sequences with low peak-to-average-power ratio,” in Proceedings of the 20th European Signal Processing Conference (EUSIPCO), 2012, pp. 2576–2580.

[32] B. Friedlander, “Waveform design for MIMO radars,” IEEE Transactions on Aerospace and Electronic Systems, vol. 43, no. 3, pp. 1227–1238, 2007.

[33] B. Tang, J. Tuck, and P. Stoica, “Polyphase waveform design for MIMO radar space time adaptive processing,” IEEE Transactions on Signal Processing, vol. 68, pp. 2143–2154, 2020.

[34] J. Li, P. Stoica, L. Xu, and W. Roberts, “On parameter identifiability of MIMO radar,” IEEE Signal Processing Letters, vol. 14, no. 12, pp. 968–971, 2007.

[35] R. Lin, M. Soltanalian, B. Tang, and J. Li, “Efficient design of binary sequences with low autocorrelation sidelobes,” IEEE Transactions on Signal Processing, vol. 67, no. 24, pp. 6397–6410, 2019.

[36] A. Bose and M. Soltanalian, “Constructing binary sequences with good correlation properties: An efficient analytical-computational interplay,” IEEE Transactions on Signal Processing, vol. 66, no. 11, pp. 2998–3007, 2018.

[37] Augusto Aubry, Antonio De Maio, Bo Jiang, and Shuzhong Zhang, “Ambiguity function shaping for cognitive radar via complex quartic optimization,” IEEE Transactions on Signal Processing, vol. 61, no. 22, pp. 5603–5619, 2013

[38] Chun-Yang Chen and PP Vaidyanathan, “MIMO radar ambiguity properties and optimization using frequency-hopping waveforms,” IEEE Transactions on Signal Processing, vol. 56, no. 12, pp. 5926–5936, 2008.

[39] Hao He, Petre Stoica, and Jian Li, “On synthesizing cross ambiguity functions,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2011, pp. 3536–3539.

[40] Meisam Razaviyayn, Mingyi Hong, and Zhi-Quan Luo, “A unified convergence analysis of block successive minimization methods for nonsmooth optimization,” SIAM Journal on Optimization, vol. 23, no. 2, pp. 1126–1153, 2013.

[41] A. Aubry, A. De Maio, A. Zappone, M. Razaviyayn, and Z. Luo, “A new sequential optimization procedure and its applications to resource allocation for wireless systems,” IEEE Transactions on Signal Processing, vol. 66, no. 24, pp. 6518–6533, 2018.

[42] M. Soltanalian, B. Tang, Jian Li, and P. Stoica, “Joint design of the receive filter and transmit sequence for active sensing,” IEEE Signal Processing Letters, vol. 20, no. 5, pp. 423–426, 2013.

[43] M. Soltanalian and P. Stoica, “Designing unimodular codes via quadratic optimization,” IEEE Transactions on Signal Processing, vol. 62, no. 5, pp. 1221–1234, 2014.

[44] Bo Tang, M. M. Naghsh, and Jun Tang, “Relative entropy-based waveform design for MIMO radar detection in the presence of clutter and interference,” IEEE Transactions on Signal Processing, vol. 63, no. 14, pp. 3783–3796, 2015.

[45] Bo Tang and Jun Tang, “Joint design of transmit waveforms and receive filters for MIMO radar space-time adaptive processing,” IEEE Transactions on Signal Processing, vol. 64, no. 18, pp. 4707–4722, 2016.

[46] Mohammad Mahdi Naghsh, Mahmoud Modarres-Hashemi, Shahram ShahbazPanahi, Mojtaba Soltanalian, and Petre Stoica, “Unified optimization framework for multi-static radar code design using information-theoretic criteria,” IEEE Transactions on Signal Processing, vol. 61, no. 21, pp. 5401–5416, 2013.

[47] H. Hu, M. Soltanalian, P. Stoica, and X. Zhu, “Locating the few: Sparsity-aware waveform design for active radar,” IEEE Transactions on Signal Processing, vol. 65, no. 3, pp. 651–662, 2017.

[48] H. He, P. Stoica, and J. Li, “Designing unimodular sequence sets with good correlations—including an application to MIMO radar,” IEEE Transactions on Signal Processing, vol. 57, no. 11, pp. 4391–4405, 2009.

[49] J. A. Tropp, I. S. Dhillon, R. W. Heath, and T. Strohmer, “Designing structured tight frames via an alternating projection method,” IEEE Transactions on Information Theory, vol. 51, no. 1, pp. 188–209, 2005.

[50] J. Li, P. Stoica, and X. Zheng, “Signal synthesis and receiver design for MIMO radar imaging,” IEEE Transactions on Signal Processing vol. 56, no. 8, pp. 3959–3968, 2008

[51] Mojtaba Soltanalian, Heng Hu, and Petre Stoica, “Single-stage transmit beamforming design for MIMO radar,” Signal Processing, vol. 102, pp. 132 – 138, 2014.

Algorithm 2 Automotive Radar Waveform Design Algorithm for Interference Mitigation (MIMO Case)   
Initialize: $\{ \mathbf { x } _ { m } ^ { ( 0 ) } \} , \ \{ \mathbf { y } _ { k } ^ { ( 0 ) } \} , \ \{ \mathbf { u } _ { l , p , m } ^ { r ( 0 ) } \} , \ \{ \mathbf { u } _ { l , p , m } ^ { i ( 0 ) } \} , \ \{ \mathbf { v } _ { l , p , k } ^ { r ( 0 ) } \} , \ \{ \mathbf { v } _ { l , p , k } ^ { i ( 0 ) } \} , \ \mathrm { f o r } \ m \ \in \ \{ 1 , \cdots , M \} , k \ \in \ \{ 1 , \cdots , K \} , l \ \in$   
$\{ - ( N - 1 ) , \cdots , N - 1 \} , p \in \{ - P , \cdots , P \} , s = 0$   
Output: $\{ \mathbf { x } _ { m } ^ { \star } \} _ { m = 1 } ^ { M } , \{ \mathbf { y } _ { k } ^ { \star } \} _ { k = 1 } ^ { K }$   
1: repeat   
2: $s \gets s + 1$   
3: Calculate $\tilde { \mathbf { A } } _ { l , p } ^ { r ( s ) } , \tilde { \mathbf { A } } _ { l , p } ^ { i ( s ) }$ for all $l , p$ following (31), (35), and (41)   
4: Calculate $\zeta ^ { ( s ) }$ using (42)   
Update of $\{ \mathbf { x } _ { m } ^ { ( s ) } \} _ { m = 1 } ^ { M } \colon$   
5: for $m = 1$ to M do   
6: Calculate $\mathbf { R } _ { \mathbf { x } _ { m } } ^ { ( s ) } , \mathbf { s } _ { \mathbf { x } _ { m } } ^ { ( s ) }$ using (48) and (49)   
7: Calculate $\bar { \mathbf { x } } _ { m } ^ { ( s ) } , \mathbf { B } _ { \mathbf { x } _ { m } } ^ { ( s ) }$ using (51) and (52)   
8: Calculate $\mathbf { D } _ { \mathbf { x } _ { m } } ^ { ( s ) }$ using (55)   
9: $t = 0 , \mathbf { x } _ { m } ^ { ( s , t ) } = \mathbf { x } _ { m } ^ { ( s - 1 ) }$   
10: repeat   
11: Calculate $\mathbf { x } _ { m } ^ { ( s , t ) }$ using (56)   
12: $t \gets t + 1$   
13: until convergence   
14: $\mathbf { x } _ { m } ^ { ( s ) } = \mathbf { x } _ { m } ^ { ( s , t ) }$   
15: end for   
Update of $\{ \mathbf { y } _ { k } ^ { ( s ) } \} _ { k = 1 } ^ { K } \colon$   
16: for $k = 1$ to K do   
17: Calculate $\mathbf { R } _ { \mathbf { y } _ { k } } ^ { ( s ) } , \mathbf { s } _ { \mathbf { y } _ { k } } ^ { ( s ) }$ using (58) and (59)   
18: Calculate $\bar { \mathbf { y } } _ { k } ^ { ( s ) } , \mathbf { B } _ { \mathbf { y } _ { k } } ^ { ( s ) }$ using (62) and (63)   
19: Calculate $\mathbf { D } _ { \mathbf { y } _ { k } } ^ { ( s ) }$ using (61)   
20: $t = 0 , \mathbf { y } _ { k } ^ { ( s , t ) } = \mathbf { y } _ { k } ^ { ( s - 1 ) }$   
21: repeat   
22: Calculate $\mathbf { y } _ { k } ^ { ( s , t ) }$ using (60)   
23: $t \gets t + 1$   
24: until convergence   
25: $\mathbf { y } _ { k } ^ { ( s ) } = \mathbf { y } _ { k } ^ { ( s , t ) }$   
26: end for   
Update of $\{ \mathbf { u } _ { l , p , m } ^ { c ( s ) } \}$ and $\{ \mathbf { v } _ { l , p , k } ^ { c ( s ) } \}$ for all $c \in \{ r , i \}$   
27: Calculate $\mathbf { u } _ { l , p , m } ^ { r ( s ) } , \mathbf { u } _ { l , p , m } ^ { i ( s ) } , \mathbf { v } _ { l , p , k } ^ { r ( s ) } , \mathbf { v } _ { l , p , k } ^ { i ( s ) }$ for each $m \in \{ 1 , \cdots , M \} , k \in \{ 1 , \cdots , K \} , l \in \{ - ( N - 1 ) , \cdots , N -$   
$1 \} , p \in \{ - P , \cdot \cdot \cdot , P \}$ using (64)-(67)   
28: until a pre-defined stop criterion is satisfied, $e . g . , | \bar { J } ^ { ( s ) } - \bar { J } ^ { ( s - 1 ) } | \le \epsilon ,$ , for some $\epsilon > 0$ where $\bar { J }$ denotes the   
objective function of the problem (45)   
29: $\{ \mathbf { x } _ { m } ^ { \star } \} _ { m = 1 } ^ { M } = \{ \mathbf { x } _ { m } ^ { ( s ) } \} _ { m = 1 } ^ { M } , \{ \mathbf { y } _ { k } ^ { \star } \} _ { k = 1 } ^ { K } = \{ \mathbf { y } _ { k } ^ { ( s ) } \} _ { k = 1 } ^ { K }$