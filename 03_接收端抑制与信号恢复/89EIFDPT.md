# A Dual-Recursive-Least-Squares Algorithm for Automotive Radar Interference Suppression

Ping Wang , Xuefeng Yin , Member, IEEE, José Rodríguez-Piñeiro , Member, IEEE, Zhuoyu Chen, Pengqi Zhu , and Gang Li, Member, IEEE

Abstract— Automotive radar sensors are widely used in vehicles so as to allow the “advanced driver assistance systems (ADAS)” to work. As far as we are concerned, no mandatory regulations were established so far for interference control in the cases where multiple vehicles equipped with automotive radars exist in close proximity. Consequently, those inter-vehicle crossinterference easily result in the radar performance degradation, e.g. incapability of target detection and identification. In this paper, an interference suppression algorithm is proposed which utilizes two Recursive-Least-Square (RLS) adaptive filters to estimate, the interference signals caused by the “aggressor” radar and the echo signals from the “ego” radar. The algorithm operates in the iterative mode with its initial input being the originally received beat signals involving interference. In each iteration, the estimates of the interference signals and of the clean signals are calculated sequentially by the two RLS filters, and the beat signal is updated with parts of the fragments substituted with their interference-mitigated counterparts. Such iterative operations stop when the convergence criterion, e.g. none of the fragments in the beat signals are considered being interfered, is achieved or the iteration number reaches the limit predefined due to the practical constraints. Simulation and measurement results demonstrate that the proposed dual-RLS-based algorithm outperforms the existing methods in terms of lower interferenceto-signal ratio resultant and superior capability of retrieving the original range-Doppler profile.

Index Terms— Frequency-modulated continuous wave (FMCW) radar, interference suppression, adaptive noise canceller, RLS adaptive algorithm.

## I. INTRODUCTION

as autonomous driving (AD) systems [1] are widely used in vehicles. To maintain the functionality of those systems, techniques based on environment sensings, such as automatic emergency braking (AEB), blind-spot detection (BSD), and adaptive cruise control (ACC) [2], are implemented which rely on the accuracy of the target detection performed by the automotive radar sensors. Millimeter automotive radars operating at a carrier frequency of 77 GHz, using the “frequency modulated continuous wave (FMCW)” signals for excitation, have been widely used for their low-complexity and performance robustness [3].

In the case where vehicles installed with millimeter FMCW radar systems are in close proximity, the signals transmitted by the aggressor radar can be received by the ego radar, leading to inter-radar interference. These interference are observable not only in the frequency domain due to the overlap of the two radars’ operational frequency bands, but also in the time domain repetitively since both radars work in periodic manners. In the case where the vehicles are driving, the time-variant environment results in rapidly changing interference. For these challenges, the ego radar performance may deteriorate significantly such that these aforementioned driverassistance techniques may malfunction and even lead to serious accidents. Currently in many countries, installing ADAS or AD systems become mandatory for vehicles. A dramatic increase in the number of automotive radar sensors on the road is expected. As predicted in [4] and [5], the inter-radar interference generated in various traffic environments would become the dominant threat to the driving safety in the near future.

To avoid the risks caused by inter-radar interference, the Europe research project “More Safety for All by Radar Interference Mitigation (MOSARIM)” [6] conducted the first assessment campaign on radar interference mitigation in January 2010. The project categorizes the existing interference mitigation techniques according to the suppression domains of six kinds. Since then, more signal processing techniques for interference mitigation were proposed and implemented for FMCW radars. Table I lists most of the techniques addressed in the literature. A brief review of the typical ones categorized by their suppression domains is as follows:

Time domain. These techniques make use of two different schemes: i) signal separation [7], [8], [9], [10]: The echo signal of the ego radar and the interference caused by the aggressor radar are separated using the wavelet transformation [7], geometric sequence decomposition [8] and matrix decomposition methods [9]. Some parameters used for signal separation need to be predetermined through experiments on actual roads, which weakens their applicability in real scenarios. ii) signal restoration [11], [12], [13], [14], [15], by applying Auto-Regressive modeling in fast- and slow-time domains [11], [12], Kalman filtering [13]parameter estimation technique [14] and iterative processing [15].

TABLE I  
SUMMARY OF INTERFERENCE SUPPRESSION ALGORITHMS/METHODS FOR AUTOMOTIVE RADARS
<table><tr><td>Suppression domain</td><td>Methods and algorithms (1) Signal separation techniques [7]-[10], including wavelet</td><td>Features and notes Advantages: (1) utilizing various digital signal processing</td></tr><tr><td>Time domain</td><td>transform [7], geometric sequence decomposition [8], and matrix decomposition [9]. (2) Signal restoration or reconstruc- tion [11]-[15], with auto-regressive model [11, 12], parameter estimation method [14], Kalman filtering [13] and iterative methods [15].</td><td>techniques without high hardware costs. (2) applicable to real- time interference suppression[11]. Disadvantages: (1) signal restoration requires experiments on actual roads to determine relevant parameter values [7] [9]. (2) algorithms need to be improved for complicated interference situations [8][15].</td></tr><tr><td>Frequency domain</td><td>Reconstructing interference replica [16], adaptive filtering in frequency[17, 18] and beat frequency interpolation [19].</td><td>High efficiency achievable by directly dealing with the fre- quency components resulting from interference, whereas, some limitations in the application, such as only for quadra- ture receivers [17, 18].</td></tr><tr><td>Code domain</td><td>Using coding and decoding techniques such as phase encod- ing [20] and orthogonal noise waveform [21].</td><td>No additional interference suppression is required, but the hardware and complex coding techniques are needed.</td></tr><tr><td>Space domain</td><td>Adaptive beamforming techniques are adopted [22, 23].</td><td>Applicable in MIMO radars while requiring hardware sup- port.</td></tr><tr><td>Polarization domain</td><td>Utilizing different polarimetric radars [24, 25]</td><td>Hardware-based design to improve the anti-interference per- formance.</td></tr><tr><td></td><td>Through different networking protocols, including the radar Operation mode domain medium access control (RadarMAC) [26], the radar and communication cooperation system (RadChat) [27] and the radar communications (RadCom) [28].</td><td>Hardware equipment in addition to radar systems is necessary for some of the methods in this category.</td></tr></table>

• Frequency domain. The interference replica are reconstructed and subtracted from the overall frequency spectrum for ghost-target suppression [16]. Interference filtering can be performed by applying adaptive noise canceler (ANC) in the frequency domain through the Fast-Fourier-Transform (FFT) [17], [18]. The cleaned signal can be reconstructed by frequency interpolation through short-time Fourier transformation [19].

• Code domain, such as the phase-coded FMCW radar system implemented in [20]. The interference from the neighbor radars is reduced by exploiting the orthogonality between the signals [21].

• Space domain, such as the adaptive techniques built based on digital beamforming designed for direction selection, which was shown being effective in enhancing the target signal-to-noise ratio [22], [23].

• Polarization domain. Two bi-cyclic linear-frequencymodulation (LFM)-signals propagating along orthogonal polarizations are used to reduce the interference in [24]. Antennas with high cross-polarization isolation can be used to avoid the interference among radar systems [25].

• Operation mode domain. The radar medium access control (RadarMAC) [26] the radar and communication cooperation system (RadChat) [27] and the radar communications (RadCom) [28] are used to guide the radars adapting operation modes for interference avoidance.

The investigation of the current interference mitigation methods indicates that applying the techniques in the time domain is a way with the lowest engineering cost and the least hardware limitation. However, there is a clear indication in [7] and [9] that necessary experiments are required on actual roads to determine relevant parameter values. In this paper, a timedomain interference suppression algorithm for FMCW automotive radar systemsutilizing a dual-Recursive Least Square (RLS)-based ANC structure is proposed to reconstruct the interference signal and the echo signal containing the contributions from the desirable targets sequentially. Since the interference signals are obtained by adaptive estimation with the original received signals and the interference-free signal samples as the primary input and reference input of ANC respectively, there is no a priori requirement on the type and number of the interference signals. It follows that the dual-RLS algorithm has a potential application in more scenarios with unknown structural interference. In addition, this algorithm can also be generalized for implementation in other domains, such as frequency, space, etc..

The performance evaluation by simulating and measurements in the two-vehicle cross-interference scenarios with 77- GHz millimeter automotive radar is considered in this work. The novelty in this paper lies in the following aspects:

\- An innovative proposal of two superimposed nested ANCs with RLS adaptive algorithm constitutes the dual-RLS structure for iterative filtering.

\- Benefiting from the RLS adaptive algorithm, a faster convergence and better tracking performance are yielded compared to the conventional approaches. Such an advantagemakes the dual-RLS structure significant for tackling the long-lasting problems of suppressing inter-radar interference in the rapidly changing scenarios due to vehicles high-speed movement.

\- Unlike the conventional methods, the dual-RLS technique proposed here does not require any prior knowledge of the interference signal [29]. This allows a feasible extension of application to more scenarios where unknown structural interference is present in temporal domains.

The remaining parts of the paper are organized as follows: Section II outlines the working principle of FMCW radar systems and signal models illustrating the interference generation mechanism. Section III provides a brief review of the ANC principle and compares the performance of some standard ANC algorithms. Section IV elaborates the proposed dual-

TABLE II  
DEFINITIONS OF THE SYMBOLS USED IN THE PAPER
<table><tr><td>Symbols</td><td>Definitions</td></tr><tr><td> $\overline { { s _ { t } ( t _ { s } , t _ { f } ) } }$ </td><td>transmitted chirp signal</td></tr><tr><td> $s _ { r } ( t _ { s } , t _ { f } )$ </td><td>received signal</td></tr><tr><td> $s _ { b } ( t _ { s } , t _ { f } )$ </td><td>beat signal after low-pass filtering</td></tr><tr><td> $T _ { \mathrm { c p } }$ </td><td>pulse repetition time (PRT)</td></tr><tr><td> $T _ { \mathrm { c h i r p } }$ </td><td>chirp signal duration</td></tr><tr><td> $T _ { d w }$ </td><td>interference duration</td></tr><tr><td> $s _ { b } ( l , n )$ </td><td>the nth fast-time samples in the lth slow-time chirp of the beat signal</td></tr><tr><td>7</td><td>slow-time sampling index in a chirp</td></tr><tr><td> $n$ </td><td>fast-time chirp index</td></tr><tr><td> $s _ { \mathbf { c l e a n } }$ </td><td>interference-free signal samples in vector notation</td></tr><tr><td> $s _ { \mathbf { r e a l } }$ </td><td>beat signal contributed by the ego radar</td></tr><tr><td> $\mathbf { \boldsymbol { s } } _ { i }$ </td><td>beat signal contributed by the aggressor radar</td></tr><tr><td> $\mathbf { e _ { 1 } }$ </td><td>output of the first ANC in the dual-RLS algorithm</td></tr><tr><td> $\mathbf { \epsilon } _ { e _ { 2 } }$ </td><td>output of the second ANC</td></tr><tr><td> $k$ </td><td>iteration index</td></tr><tr><td> $\ell$ </td><td></td></tr><tr><td> $_ B$ </td><td>slow-time index for signals with interference a location  $L \times N$  matrix with entries  $B ( l , n ) = 1$  or</td></tr><tr><td></td><td>0 indicating whether  $s _ { b } ( l , n )$  is interfered</td></tr><tr><td> $\hat { s }$   $P$ </td><td>estimate of the interference-free beat signal</td></tr><tr><td></td><td>threshold values used to stop the iterations operations</td></tr><tr><td> $K$ </td><td>maximum number of iterations allowed</td></tr><tr><td> $\gamma _ { i s r }$ </td><td>interference to signal ratio (ISR)</td></tr><tr><td> $\gamma _ { g l m r }$ </td><td>global to local maxima ratio (GLMR)</td></tr><tr><td> $\underline { { \gamma _ { t r f r } } }$ </td><td>time-to-radar-frame ratio (TRFR)</td></tr></table>

RLS algorithm. Section V validates the algorithm based on simulation studies and measurements, and a comparison of the performance among the proposed algorithm and conventional algorithms. Section VI analyzes the performance and complexity of the proposed algorithm. Finally, conclusive remarks are given in Section VII.

The definitions of the mathematical symbols used in this paper are shown in Tabel II.

## II. ANALYSIS OF THE INTERFERENCE BETWEEN FMCW AUTOMOTIVE RADARS

## A. The Operation Principle of FMCW Automotive Radar

In the FMCW radar system, the radar operates by periodically transmitting linear-frequency-modulation(LFM)-signals which are usually the chirp signals. As depicted in Fig. 1, the instantaneous frequency of a chirp signal varies linearly versus time instance. The transmitted signals $s _ { t } ( t _ { s } , t _ { f } )$ can be viewed as a function in two temporal domains, i.e. the so-called “slowtime” $t _ { s }$ and “fast-time” $\cdot _ { t _ { f } }$ referred to as respectively, the time instances at which the radar begins to transmit a chirp signal and the time instances of individual samples in the chirp signal. It can be expressed as

$$
s _ { t } ( t _ { s } , t _ { f } ) = \sum _ { l = 0 } ^ { L - 1 } \delta ( t _ { s } - l T _ { \mathrm { c p } } ) \alpha _ { t } \exp \left\{ \jmath 2 \pi ( f _ { c } t _ { f } + \frac { 1 } { 2 } k _ { s } t _ { f } ^ { 2 } ) \right\} ,\tag{1}
$$

where the discrete time instance $t _ { s } ~ = ~ l T _ { \mathrm { c p } }$ holds with $l \in$ [0, L − 1] being the sequential index of a chip signal and L the total number of the transmitted chirp signals, $T _ { \mathrm { c p } }$ is the socalled “pulse repetition time (PRT)” which is defined as the time interval between the beginnings of two consecutive chirp signals, δ(·) represents the Dirac delta function, $t _ { f } \in [ 0 , T _ { \mathrm { c h i r p } } ]$ denotes the discrete time instance with $T _ { \mathrm { c h i r p } }$ being the chirp duration and $t _ { f } = n / F _ { s }$ where $F _ { s }$ represents the sampling rate in fast-time domain and $n \in [ 0 , N { - } 1 ]$ is the sample index with $N = T _ { \mathrm { c h i r p } } F _ { s } , \alpha _ { t }$ represents the constant amplitude of the chirp signal, $f _ { c }$ is the carrier frequency, $k _ { s } = B W _ { \mathrm { s w } } / T _ { \mathrm { c h i r p } }$ denotes the frequency modulation (FM) slope of the chirp signal with $B W _ { \mathrm { s w } }$ representing the total sweep bandwidth of the chirp signal. Note that $T _ { \mathrm { c h i r p } } < T _ { \mathrm { c p } }$ always holds, ensuring the fasttime samples collected in one chirp signal not overlapped with those of the other chirp signals.

![](images/001df098aabcaddbd2a9775b836f460c2a0d86967a5ca5850732a85bd0ce49b3.jpg)  
Fig. 1. Beat frequency in FMCW radar signal processing.

Assuming that during the period of $L T _ { \mathrm { c p } } ,$ , multiple targets exist in the premise of the ego radar, the received signals, also called as “echo signals” in literature, can be represented as

$$
\begin{array} { c } { { s _ { r } ( t _ { s } , t _ { f } ) = \displaystyle \sum _ { l = 0 } ^ { L - 1 } \delta ( t _ { s } - l T _ { \mathrm { c p } } ) \sum _ { m = 1 } ^ { M } \alpha _ { r , m } } } \\ { { \displaystyle \exp \bigg \{ \jmath 2 \pi ( f _ { c } ( t _ { f } - \tau _ { m } ) + \frac { 1 } { 2 } k _ { s } ( t _ { f } - \tau _ { m } ) ^ { 2 } ) \bigg \} , } } \end{array}\tag{2}
$$

where $\alpha _ { r , m }$ represents the complex-valued amplitude of signals propagating along the path stemming from the transmitting antenna of the radar to the mth target and back to the receiving antenna of the radar, and $\tau _ { m }$ is the propagation delay of the chirp signal propagating along the path. Under the assumption that the transmitting antenna and receiving antenna are colocated and the spacing between them is far less than the distances from the radar to the targets, by neglecting the antenna spacing, the equality $\tau _ { m } = 2 R _ { m } / c$ holds approximately where $R _ { m }$ , the distance between the target and the radar receiving antenna, can be decomposed as

$$
R _ { m } = R _ { 0 , m } + v _ { m } ( t _ { s } + t _ { f } )\tag{3}
$$

with $R _ { 0 , m }$ being the path length observed at $t _ { s } ~ = ~ 0 ~ \mathrm { ~ s ~ }$ and $v _ { m }$ representing the relative radial velocity of the mth target with respect to the radar. According to the standard operation procedure of the FMCW radars, the received echo signals $s _ { r } ( t _ { s } , t _ { f } )$ need to be “mixed” with the transmitted signals $s _ { t } ( t _ { s } , t _ { f } )$ as follows:

$$
s _ { \mathrm { m i x } } ( t _ { s } , t _ { f } ) = s _ { t } ( t _ { s } , t _ { f } ) s _ { r } ^ { * } ( t _ { s } , t _ { f } ) ,\tag{4}
$$

where $s _ { \operatorname* { m i x } } ( t _ { s } , t _ { f } )$ is the output of this mixing operation and $( \cdot ) ^ { * }$ denotes the complex conjugate. Then, $s _ { \operatorname* { m i x } } ( t _ { s } , t _ { f } )$ is fed to an anti-alias filter (AAF) [30], such as an analog low-pass filter to remove the high-frequency components. After analog-digital conversion of the AAF output, the so-called “beat signals”, denoted with $s _ { b } ( t _ { s } , t _ { f } )$ , are obtained which can be written as

$$
s _ { b } ( t _ { s } , t _ { f } ) = \sum _ { l = 0 } ^ { L - 1 } \delta ( t _ { s } - l T _ { c p } ) \sum _ { m = 1 } ^ { M } \alpha _ { b , m }\tag{5}
$$

where $\alpha _ { b , m } ~ = ~ \alpha _ { t } \alpha _ { r , m } ^ { * }$ is the amplitude of the beat signal received along the mth path, $\tau _ { 0 , m } = \frac { 2 R _ { 0 , m } } { c }$ corresponds to the initial delay of the mth path at $t _ { s } = 0 ~ \mathrm { s } ,$ the frequency $f _ { r , m }$ is linearly proportional to $\tau _ { m }$ according to

$$
f _ { r , m } = k _ { s } \tau _ { m }\tag{6}
$$

and the frequency $f _ { d , m }$ is the Doppler frequency shift caused by the non-zero velocity of the mth target according to

$$
f _ { d , m } = \frac { 2 f _ { c } v _ { m } } { c } .\tag{7}
$$

It can be shown that by applying the Fourier transform on $s _ { b } ( t _ { s } , t _ { f } )$ with respect to the temporal domain $t _ { f }$ , the transfer function at the composite frequencies $f _ { r , m } + f _ { d , m }$ can be calculated. Similarly, applying the Fourier transform on $s _ { b } ( t _ { s } , t _ { f } )$ with respect to $t _ { s } ,$ the transfer function of the frequency domain involving $f _ { d , m }$ is obtained. For the FMCW automobile radars, the inequality $f _ { d , m } ~ \ll ~ f _ { r , m }$ is usually holds [30], thus $f _ { r , m } + f _ { d , m }$ can be approximated by $f _ { r , m } .$ From (6) and (7), it is readily to show that the estimates of $R _ { m }$ and $v _ { m }$ can be calculated based on the estimates of $f _ { d , r }$ m and $f _ { r , m }$ respectively as

$$
R _ { m } = \frac { c f _ { r , m } T _ { \mathrm { c h i r p } } } { 2 B W _ { \mathrm { s w } } } ,\tag{8}
$$

$$
v _ { m } = { \frac { c f _ { d , m } } { 2 f _ { c } } } .\tag{9}
$$

By conducting Fourier transformation on $s _ { b } ( t _ { s } , t _ { f } )$ with respect to $t _ { s }$ and $t _ { f }$ , with straightforward manipulation, we can obtain the two-dimensional transfer function and furthermore the power spectral density (PSD) function in the range R and the velocity v domains. Such a PSD function is usually called as “range-Doppler profile” according to the literature. By searching the maxima of the range-Doppler profile, the estimates of the range $\hat { R } _ { m }$ and of the velocity $\hat { v } _ { m }$ of the individual target can be obtained.

## B. The Effect of Interference Between FMCW Automotive Radars

When a 77 GHz millimeter-wave automotive radar, say the ego radar, operates, interference occurs if another automotive radar which can be defined as the aggressor radar transmits the signals which own frequency components in the passband of AAF of the ego radar. The interference can result in two situations: a ghost target not distinguishable from the true targets, and all true targets’ images blurred by a widely spread pattern in the range-Doppler profile due to the presence of cyclic interference signals in $s _ { b } ( t _ { s } , t _ { f } )$ [2].

The phenomenon that a ghost target is observed occurs when the two FMCW automotive radars have identical parameters except of the initial phases and the aggressor radar’s chirp falls in the passband $B W _ { \mathrm { A A F } }$ of the ego radar’s AAF demonstrated in Fig. 2(a). Although this is the extremely severe case, in reality the probability of observing ghost targets is considerably low [3], due to the low possibility of two vehicles equipped with exactly the same radar systems meeting on road.

![](images/62451d93a256b6d5cef1422129cd5f65ae9ad5305199d2c9595433f15d7fe78c.jpg)  
(a)

![](images/45c657da398f7a86011c777c2b6cd1cf4f387575f7f5c1d6ed597772c59863eb.jpg)  
(b)  
Fig. 2. Interference dwell time of beat signal in two interference chirps with different slopes.

The second situation is more commonly observed and this paper focuses on this interference. The situation occurs when only a part of the beat signals generated due to the chirp of aggressor radar pass through $B W _ { \mathrm { A A F } }$ , leading to an impulselike signal in time domains. Fig. 2(b) depicts an example of such a kind. We use $B W _ { i } , T _ { \mathrm { c h i r p , i } }$ and $k _ { i }$ to represent the sweep bandwidth, the duration of the chirp signal and the FM slope of the interference signals for the aggressor radar. It can be shown that the FM slope of the beat signal caused by the interference equals $| k _ { s } - k _ { i } |$ , and the duration $T _ { \mathrm { d w } }$ of the interference beat signal is calculated as

$$
T _ { \mathrm { d w } } = \frac { B W _ { \mathrm { A A F } } } { | k _ { s } - k _ { i } | } .\tag{10}
$$

It is obvious from (10) that $T _ { \mathrm { d w } }$ is inversely proportional to $| k _ { s } ~ - ~ k _ { i } |$ , implying that the closer FM slope of two chirp signals, the longer interference duration will be, which corresponds to the observations in Fig. 2 (a) and (b). Meanwhile, with the interference duration increasing, the sidelobe components in the range-Doppler spectrum increased more significantly, which reduces the detection possibility of the targets. Therefore, it is a necessity of applying interference suppression methods to restore the capability of target detection and identification.

![](images/8e3b41c3bc9b814f27bd7cfcaaa4ecbb3bed64174eff6b84b47157a37fe112f8.jpg)  
Fig. 3. Block diagram of adaptive noise canceller [29].

## III. A REVISIT OF ADAPTIVE ALGORITHMS FOR NOISE CANCELLATION

An adaptive noise canceler, as depicted in the dashed-line box in Fig. 3, consists of a summation operator and an adaptive filter. The primary input $d ( n )$ to the ANC is composed of a deterministic signal s(n) and a random noise component v<sub>0</sub>(n) where n is the discrete time index. The reference input $v _ { 1 } ( n )$ of the ANC is also a noise component uncorrelated with s(n). It is assumed that $v _ { 1 } ( n )$ is generated by the same source as v<sub>0</sub>(n), and thus, $v _ { 1 } ( n )$ and v<sub>0</sub>(n) are correlated with a certain form [29]. At the nth time instance, considering the adaptive filter has stored M latest reference inputs with M denoting the filter tap, the input can be written as a vector

$$
\pmb { v } ( n ) = [ v _ { 1 } ( n \ v _ { 1 } ( n - 1 ) \dots \ v _ { 1 } ( n - M + 1 ) ] ^ { \mathrm { T } } .\tag{11}
$$

The adaptive filter output in the ANC at time n is

$$
\boldsymbol { y } ( n ) = \boldsymbol { w } ^ { \mathrm { H } } ( n ) \boldsymbol { v } ( n )\tag{12}
$$

where $\pmb { w } ( n ) \in \mathbb { C } ^ { M \times 1 }$ is the filter weight vector. The output signal $y ( n )$ is an estimate of v<sub>0</sub>(n), calculated jointly from $v _ { 1 } ( n )$ and the noise-mitigated signal $e ( n )$ from the output of the ANC. It is obvious that e(n), viewed as an estimate of $s ( n )$ is calculated as

$$
\begin{array} { c } { { e ( n ) = d ( n ) - y ( n ) } } \\ { { = s ( n ) + v _ { 0 } ( n ) - y ( n ) . } } \end{array}\tag{13}
$$

Under the assumption that both $v _ { 0 } ( n )$ and y(n) are uncorrelated with s(n), it can be shown that the equality

$$
\operatorname { E } [ e ( n ) ^ { 2 } ] = \operatorname { E } [ s ^ { 2 } ( n ) ] + \operatorname { E } [ ( v _ { 0 } ( n ) - y ( n ) ) ^ { 2 } ]\tag{14}
$$

holds where E[·] represents the expectation. Applying the minimum mean square error (MMSE) criterion, the adaptive filter updates its weights iteratively to reduce $\mathrm { E } [ ( v _ { 0 } ( n ) - y ( n ) ) ^ { 2 } ]$ until $\operatorname { E } [ e ^ { 2 } ( n ) ] \approx \operatorname { E } [ s ^ { 2 } ( n ) ]$ ] holds.

There exist a few algorithms applicable in the adaptive filter, such as the Least Mean Square (LMS) proposed by Widrow and Hoff [31] which has a good convergence performance while retaining low computational complexity, and a Normalized LMS (NLMS) algorithm in [32] which adopts a variable step size in order to achieve a less steady-state error while shortening the adaptive convergence process. However, both LMS and NLMS algorithms exhibit poor performance in non-stationary environments [33]. In contrast, the adaptive algorithms derived based on the least-squares(LS) criterion can provide better tracking performance [34] and therefore are suitable for application in automotive radar. The Recursive Least Squares (RLS) adaptive algorithm is a typical algorithm derived based on the LS criterion. The cost functions J (n) to be minimized in RLS, can be written as [35]:

$$
\begin{array} { l } { { \displaystyle J ( n ) = \sum _ { i = 0 } ^ { n } \lambda ^ { n - i } | e ( i ) | ^ { 2 } } } \\ { { \displaystyle \ = \sum _ { i = 0 } ^ { n } \lambda ^ { n - i } | d ( i ) - w ^ { \mathrm { H } } ( n ) } { \boldsymbol v } ( i ) | ^ { 2 } . }  \end{array}\tag{15}
$$

where λ is the forgetting factor taking the value slightly less than one [36]. As the time index n grows, $\lambda ^ { ( n - i ) }$ can make the $\mathrm { \tilde { \Delta } o l d \vec { \Gamma } }$ signal (more historical in the past) less influential on the filter weight adjustment, while the newly arrived signals become more dominant. The optimal solution ${ \pmb w } _ { o p t } ( n )$ of w(n) for minimizing J (n) can be shown to be

$$
{ \pmb w } _ { o p t } ( { \pmb n } ) = { \pmb R } ^ { - 1 } ( { \pmb n } ) { \pmb r } ( { \pmb n } ) ,\tag{16}
$$

where

$$
R ( n ) = \sum _ { i = 0 } ^ { n } \lambda ^ { n - i } \pmb { v } ( i ) \pmb { v } ^ { \mathrm { H } } ( i ) ,\tag{17}
$$

$$
r ( n ) = \sum _ { i = 0 } ^ { n } \lambda ^ { n - i } \pmb { \upsilon } ( i ) d ^ { * } ( i ) ,\tag{18}
$$

with $[ \mathbf { \nabla } ] ^ { H }$ being the Hermitian operation. For notation convenience, $\pmb { P } ( n ) = \pmb { R } ^ { - 1 } ( n )$ is used in the sequel. The RLS adaptive algorithm<sup>1</sup> operates in two steps:

• Step 1. Initialization:

Initialize ${ \pmb w } ( 0 ) = { \pmb 0 } , { \pmb P } ( 0 ) = \eta ^ { - 1 } { \pmb I }$ with I being an Mdimensional unit matrix and η the regularization parameter. According to [38], η can take a small value such as $1 0 ^ { - 4 }$ in initialization.

• Step 2. For $n ~ = ~ 1 , 2 , 3 , . . . ,$ perform the following operations

$$
\begin{array} { r l } & { \mathrm { ~ \displaystyle ~ - ~ \ c a l c u l a t e ~ t h e ~ e x t i m a t i o n ~ e r r o r : ~ } } \\ & { \mathrm { ~ \displaystyle ~ e ( n ) = d ( n ) - w ^ { H } ( n - 1 ) v ( n ) ; } } \\ & { \mathrm { ~ \displaystyle ~ - ~ U p d a t e ~ t h e ~ g a i n ~ v e c t o r : ~ } } \\ & { \mathrm { ~ \displaystyle ~ \ } k ( n ) = \frac { P ( n - 1 ) v ( n ) } { \lambda + v ^ { \mathrm { H } } ( n ) P ( n - 1 ) v ( n ) } ; } \\ & { \mathrm { ~ \displaystyle ~ - ~ U p d a t e ~ t h e ~ i n v e r s e ~ } P ( n ) \mathrm { ~ o f ~ t h e ~ c o r r e l a t i o n ~ m a t r i x } } \\ & { \mathrm { ~ \displaystyle ~ \ } R ( n ) : } \\ & { P ( n ) = \lambda ^ { - 1 } ( P ( n - 1 ) - k ( n ) v ^ { \mathrm { H } } ( n ) P ( n - 1 ) ) ; } \\ & { \mathrm { ~ \displaystyle ~ - ~ U p d a t e ~ t h e ~ f i t e r ~ w e i g h t ~ v e c t o r : ~ } } \\ &  \mathrm { ~ \displaystyle ~ w ( n ) = w ( n - 1 ) + \} k ( n ) e ^ { * } ( n ) . } \end{array}
$$

A simulation was conducted to illustrate the different performances of some adaptive algorithms. In the simulation, the received signal is a sequence of ±1 randomly selected with equal probabilities, plus a white Gaussian noise component with signal-to-noise ratio (SNR) of 30 dB. With the same fixed filter taps $M = 4 ,$ , the root mean squared estimation error (RMSEE) obtained for the RLS, NLMS and LMS algorithms, versus the sequence sample index is presented in Fig. 4. The results are from 1000 Monte Carlo simulation runs. It can be observed that the convergence speed of the RLS algorithm is the fastest among all algorithms. Furthermore, the RLS algorithm returns less mean squared error in a shorter time than the other two algorithms. For its better performance, the RLS is selected for the adaptive filtering algorithm implemented in the ANC in the interference suppression technique proposed here.

![](images/b6d8b50b871dccfc90021c484e7c26a41d82e7b2eb91d284f1320e2cd095af1c.jpg)  
Fig. 4. Comparison RMSEE of different algorithms with $\mathrm { S N R } { } = 3 0 \mathrm { d B } { } .$

![](images/9cc3dbd8cb2acd35c345893296517971fc62183dd803a16191458f88a29b9f49.jpg)  
Fig. 5. Block diagram of the proposed algorithm.

## IV. THE PROPOSED INTERFERENCE SUPPRESSIONDUAL-RLS ALGORITHM

Fig. 5 illustrates the proposed algorithm sequence utilizing the dual-RLS structure. The operations conducted in a preprocessing step and the iteration steps that follow are introduced in Subsections IV-A and IV-B respectively.

## A. Interference Sample Signal Reconstruction Based on Interference Detection

For notation convenience, The beat signal $s _ { b } ( t _ { s } , t _ { f } )$ is rewritten as $s _ { b } ( l , n )$ with l and n being the slow-time sampling index and the fast-time sampling index, respectively. We further use vector $\mathbf { \Delta } \mathbf { s } _ { b }$ to represent all entries of $s _ { b } ( l , n )$ $l = [ 0 , L - 1 ]$ and $n = [ 0 , N - 1 ]$ concatenated as a sequence.

As analyzed in Section II, the interference from the aggressor radar is also chirp signals that are transmitted periodically, and hence, the regions of $s _ { b } ( l , n )$ where interference exists exhibit a cyclic pattern in the plane formed by the axes of slow-time index l and of fast-time index n. A method based on histogram analysis, which was originally applied in automated landmine detection of ground penetration radar [39] and micro-Doppler interference analysis of the rigid-body components [40], set a threshold to segment or separate them using the histogram method depending on the different frequency of occurrence between rigid body components and micro Doppler interference. The histogram analysis method is adopted to detect the interference position based on the large difference in amplitude between the interference signal and the target signal in time domain.

In the proposed dual-RLS interference suppression algorithm, with the input of $\mathbf { { \sigma } } _ { \mathbf { { \pmb { s } } } _ { b } } .$ , the histogram-based method yields a location $L \times N$ matrix B with entries $B ( l , n ) ~ = ~ 1$ and 0 indicating the status of $s _ { b } ( l , n )$ being interfered and noninterfered, respectively. Fig. 6 illustrates an example of the matrix B, where the fragments highlighted with bright yellow color are the regions with interference detected with entries $B = 1$ , and the remaining blue fragments indicate being noninterfered. The interference-free signal samples $s _ { \mathrm { c l e a n } } ,$ which are applied as the reference input to the ANC in the algorithm, are obtained with respect to B. It is preferable to choose a complete fast-time chirp sequence without interference as the s<sub>clean</sub>. The echo signals at the 4th and 20th slow-time indices marked by red dashed boxes in Fig. 6 are observed with no region highlighted with bright yellow color in the fast-time domain, indicating that they are not disturbed by interference.In practical application, only the indices of the row all with 0 value in the matrix B need to be calculated to determine the location of the non-interference samples. Thus, these signals without being interfered can be selected to be s<sub>clean</sub>.

However, it can happen that interference regions spread so densely that none of complete fast-time chirp signal is free of interference. In such a case, the cleaned signal $\pmb { s } _ { \mathbf { c l e a n } }$ can be reconstructed by selecting a chirp sequence with shorter interference segments than other sequences, and replacing the interference segments in this chirp with the clean segments of the same chirp signal. Fig. 7 illustrates such an example where the chirp signal received with interference at slow time index $l = 1 7$ as illustrated in Fig. 6, is used to generate $\mathbf { s _ { c l e a n } }$ . The interference segment existing to the left end of the abscissa n is replaced by the clean segment located close to it.

## B. Interference Suppression Based on Dual RLS Structure

For the practical application of automotive radars, it is difficult to construct the reference input signal $v _ { 1 } ( n )$ in Fig. 3 when the ANC is operated, due to the unknown information such as waveform and intensity of interference signal from the aggressor radar. Therefore, the Dual-RLS structure adopt two superimposed ANCs, where the role of ANC1 is to estimate the signals correlated with the interference and input them to ANC2 for interference suppression. The operations performed in iterations are introduced as follows.

![](images/d2a2e15ca2f282b50730dc613de39ce150f149842eb09acdc3895cd7441f2ca4.jpg)  
Fig. 6. A beat signal frame $s _ { b } ( l , n )$ of size 21 × 512(slow-time samples×fast-time samples), where the sample fragments highlighted with bright yellow color are interfered. In this example, the 4th and 20th slow-time indexed chirp signals circled with the dashed red box are detected without interference.

![](images/1740f07b11d42038cf1ceb8122b53d6d8d15cc12ae42b64baa5831beeb90c9c8.jpg)  
Fig. 7. Example of reconstructing a sample without interference. (a) The 17th slow-time indexed chirp signal with the shortest interference segments. (b) The constructed interference-free signal samples based on 17th slow-time indexed chirp signal.

$\hat { \pmb { s } } ^ { [ k ] }$ is uesd to denote the updated estimate of interferencesuppressed beat signal at the kth iteration. It contains both the beat signal $\pmb { S } _ { \mathbf { r e a l } }$ contributed merely by the ego radar and the mitigated interference $s _ { i }$ contributed by the aggressor radar. Note that in the initialization step, $\hat { \pmb { s } } ^ { [ 0 ] } = { \pmb { s } } _ { b }$ is specified.

To reduce the computational complexity, in each iteration the ANCs are only applied to remove the interference for the parts of $\hat { s } ^ { [ k ] }$ identified being interfered using the histogram interference detection method. $\ell ^ { [ k ] }$ is adopted to denote the slow-time index set of the chirps signals in $\hat { s } ^ { [ k ] }$ identified being disturbed with interference. Note that $\ell ^ { [ k ] }$ needs to be updated at the end of an iteration and is applied as a necessary input in the next iteration. In the kth iteration, all chirp signals with their slow-time indices specified in $\ell ^ { [ k ] }$ are processed individually. For the lth chirp signal with $l \in \ell ^ { [ k ] }$ the following operations are performed.

The selected beat signal without interference $\pmb { S } _ { \mathbf { c l e a n } }$ is applied as the reference input to the $\mathbf { A N C } _ { 1 } . \mathbf { \sigma } _ { S \mathbf { c l e a n } }$ is correlated with $\pmb { S } _ { \mathbf { r e a l } }$ with unknown forms while uncorrelated with s<sub>i</sub> . The primary input of $\mathbf { A N C } _ { 1 }$ is the lth row of $\hat { \pmb { s } } ^ { [ k - 1 ] } , \mathrm { i . e . } \hat { \pmb { s } } ^ { [ k - 1 ] } ( l , : ) ]$ . With both the reference and primary inputs, the adaptive filter in $\mathrm { A N C } _ { 1 }$ adapts the filter weights to optimize the estimation of $\mathbf { s _ { r e a l } }$ with the reference of $\mathbf { s _ { c l e a n } } .$ . Based on the estimated $\pmb { S } _ { \mathbf { r e a l } }$ , the $\mathbf { A N C } _ { 1 }$ outputs the signal $e _ { 1 } { \left[ k \right] }$ as the estimate of $s _ { i }$ in this iteration. In other words, the function of $\mathrm { A N C _ { 1 } }$ can be viewed as suppressing the ego radar’s contribution in the beat signal to obtain the estimate of the interference caused by the aggressor radar.

For the $\mathbf { A N C } _ { 2 } , \hat { s } ^ { [ k - 1 ] }$ remains as its primary input, and its reference input is ${ e _ { 1 } } ^ { [ k ] }$ which is the output of $\mathrm { A N C _ { 1 } }$ . Based on the predefined assumptions, $e _ { 1 } { \left[ k \right] }$ and $s _ { i }$ are correlated with a certain form and both of them are assumed to be uncorrelated with $\pmb { S } _ { \mathbf { r e a l } }$ . The adaptive filter in $\mathrm { A N C } _ { 2 }$ adapts the filter weights to optimize the estimation of $s _ { \mathrm { i } }$ with the reference of $e _ { 1 } { \left[ k \right] }$ . Based on the estimated $s _ { \mathrm { i } } ,$ the $\mathrm { A N C } _ { 2 }$ outputs the signal $e _ { 2 } { \left[ k \right] }$ as the estimate of $\pmb { S } _ { \mathbf { r e a l } }$ in the kth iteration. Thus, the $\mathrm { A N C } _ { 2 }$ functions as a conventional ANC that conducts denoising operation or interference suppressing operation.

The output $e _ { 2 } { \mathrm { [ } k \mathrm { ] } }$ of the $\mathrm { A N C } _ { 2 }$ is an interference-suppressed estimate of the lth slow time chirp of $\hat { s } ^ { [ k ] }$ , and is used to update the lth slow-time chirp signal in $\hat { \pmb { s } } ^ { [ k ] }$ in the kth iteration. Practically, in order to maintain low complexity, only the fragments that are identified being interfered by the histogrambased method are replaced by the according fragments in $e _ { 2 } { \left[ k \right] }$ $\mathrm { i } . \mathrm { e } . \hat { s } ^ { [ k ] } ( l , n ) = [ e _ { 2 } ^ { [ \hat { k } ] } ( n ) | n : \mathbf { \bar { \delta } } B ( l , n ) = 1 ] ^ { }$ . After all the fasttime sequences indexed with slow-time indices specified by $\ell ^ { [ k ] }$ are processed once using both the $\mathrm { A N C _ { 1 } }$ and $\mathbf { \bar { \Phi } } _ { \mathrm { A N C } _ { 2 } , ~ \hat { s } } ^ { 1 \check { k } ] }$ is yielded as the output of the kth iteration.

The index set $\ell ^ { [ k ] }$ needs to be updated for the next iteration. The following operations are adopted: the matrix $\hat { \pmb { s } } ^ { [ k ] }$ goes through threshold detection to determine whether the interference in each fast-time chirp signal has been effectively suppressed. The threshold applied is set to be the average power P of the interference-free chirps detected by the histogram method before the iterations start. If the power of a row in $\hat { \pmb { s } } ^ { [ k ] }$ , i.e. an interference-suppressed fast-time chirp, is lower than $P ,$ this chirp signal is considered to contain insignificant interference and as a consequence, further interference suppression operation is unnecessary; otherwise, it needs to be suppressed continuously in the new iteration, and the corresponding slow-time index is included in the set $\ell ^ { [ k + 1 ] }$ that collects all the slow-time indices of the chirps with nonnegligible interference after the kth iteration. Such an updating operation can be represented as

$$
\ell ^ { [ k ] } = \left[ \ell : = \sum _ { n = 1 } ^ { N } \bigl | \hat { s } ^ { [ k ] } ( l , n ) \bigr | ^ { 2 } > P , \ell \in [ 1 , L ] \right]\tag{19}
$$

The iterative operation may stop when either of the following two conditions holds: i) all the signals in $\hat { s } ^ { [ k ] }$ are considered to contain interference low enough such that $\ell ^ { [ k + 1 ] }$ becomes empty; ii) the total number K of iterations predetermined by considering realistic constraints is reached. When the iteration ends, the final updated $\hat { \boldsymbol s } ^ { [ k ] }$ is considered to be the output of the dual-RLS interference suppression algorithm. The detailed operations in the algorithm are articulated in the pseudo-code representation of “Algorithm 1”.

Algorithm 1 Interference Suppression Algorithm Utilizing   
Dual-RLS-Structure   
Input: $s _ { b } ~ \in ~ \mathbb { C } ^ { L \times N }$ , radar beat signal with L being the   
number of chirps per frame and N being fast-time samples   
per chirp. $s _ { \mathbf { c l e a n } } \in \mathbb { C } ^ { 1 \times N }$ , the interference-free signal   
samples. B, a location $L \times N$ matrix indicating whether   
$s _ { b } ( l , n )$ is interfered.   
Output: $\hat { s } \in \mathbb { C } ^ { L \times N }$ , the interference-suppressed beat signal.   
1: Initialization Step: $k = 1$ with k denoting the iteration   
index. Specifying filter order $M _ { i }$ , forgetting factor $\lambda _ { i }$ and   
regularization parameter $\eta _ { i } ( i = 1 , 2 . )$   
2: Iteration Step: $\hat { \pmb { s } } ^ { [ 0 ] } = s _ { b } ;$   
3: $\begin{array} { r } { \ell ^ { [ 1 ] } \stackrel { \cdot } { = } \left[ \ell : = \sum _ { n = 1 } ^ { N } B ( l , n ) > 0 , \ell \in [ 1 , L ] \right] } \end{array}$   
4: for $k = 1  \bar { K }$ do   
5: for $l = 1  L$ do   
6: if ismember $( l , \ell ^ { [ k ] } ) = 1$ then   
7: $\begin{array} { r } { p _ { 1 } = \hat { s } ^ { [ k - 1 ] } ( l , : ) ; } \end{array}$   
8: $r _ { 1 } = s _ { \mathrm { c l e a n } } ;$   
9: for $i = 1  2$ do   
10: ${ \pmb w } _ { i } ^ { [ k ] } = [ 0 , 0 , \ldots , 0 ] ^ { T } ;$   
11: $\pmb { x _ { i } } ^ { [ k ] } = [ 0 , 0 , \ldots , 0 ] ^ { T } ;$   
12: ${ \pmb e } _ { i } { \bf \Psi } = [ 0 , 0 , \dots , 0 ] ^ { T } ;$   
13: $P _ { i } { } ^ { [ k ] } = \delta _ { i } ^ { - 1 } * I ;$   
14: for $j = \dot { 1 }  N$ do   
15: $\dot { \mathbf { x } } _ { i } { } ^ { [ k ] } = [ r _ { i } ( j ) \mathbf { x } _ { i } { } ^ { [ k ] } ( 1 : { \cal M } - 1 ) ] ;$   
16: $e _ { i } ^ { [ k ] } ( j ) = p _ { i } ( j ) - { \pmb w } _ { i } ^ { [ k ] ^ { T } } { \pmb x } _ { i } ^ { [ k ] } ;$   
[k] ${ P _ { i } } ^ { [ k ] } { x _ { i } } ^ { [ k ] }$   
17: $k _ { i } \mathrm {  ~ \Psi ~ } ^ { \star \star } = \frac { \ d } { \ d t } \frac { \ d } { \ d t } = \frac { \ d } { \ d t } \frac { ( \ d _ { k } ) ^ { T } P _ { i } ^ { \ [ k ] } x _ { i } ^ { \ [ k ] } } { \ d t } ;$   
18: $P _ { i } { } ^ { [ k ] } = \mathring { \lambda _ { i } } ^ { - 1 } ( P _ { i } { } ^ { [ k ] } - k _ { i } { } ^ { [ \ddot { k } ] } x _ { i } { } ^ { [ k ] }$   
$P _ { i } { ^ { [ k ] } } ) ;$   
19: ${ \pmb w } _ { i } ^ { [ k ] } = { \pmb w } _ { i } ^ { [ k ] } + { \pmb k } _ { i } ^ { [ k ] } e _ { i } ^ { * [ k ] } ( j ) ;$   
20: end for   
21: $\smash { p _ { 2 } = \hat { s } _ { r a p } ^ { [ k - 1 ] } ( l , : ) ; }$   
22: $\bar { r } _ { 2 } = e _ { 1 } ^ { [ k ] } ;$   
23: end for   
24: $\hat { s } ^ { [ k ] } ( l , n ) = \left\{ \begin{array} { l l } { e _ { 2 } ^ { [ k ] } ( n ) , n : { \cal B } ( l , n ) = 1 ; } \\ { \scriptstyle \wedge \lceil k - 1 \rceil \ , } \end{array} \right.$   
$\begin{array} { r } { \mathbf { \tilde { { s } } } ^ { - } ( \iota , n ) =  \{ \begin{array} { r l } { \hat { s } ^ { [ k - 1 ] } ( \iota , n ) , n : B ( \iota , n ) = 0 ; } \end{array}  } \end{array}$   
25: end if   
26: end for   
27: $\begin{array} { r } { \ell ^ { [ k + 1 ] } = \left[ \ell : = \sum _ { \ldots } ^ { N } \left| \hat { s } ^ { [ k ] } ( l , n ) \right| ^ { 2 } > P , \ell \in [ 1 , L ] \right] } \end{array}$   
28: if i sem pt y $\ell ^ { [ k + 1 ] } = 0$ then   
29: continue   
30: else   
31: break   
32: end if   
33: end for

## V. PERFORMANCE EVALUATION BASED ON SIMULATION AND EXPERIMENTS

The proposed algorithm was implemented in MATLAB. Simulation studies were performed on investigating the algorithm’s performance on interference suppression in the case of moving vehicles installed with millimeter-wave FMCW radars co-existing in a vicinity. Measurement data collected with radar equipment in a realistic vehicular environment was also processed to illustrate the performance difference between the proposed algorithm and the conventional methods.

![](images/d59f70158462674c966f02cc0b0adfcdc0890cef0b0898a7ceddd33970634ab9.jpg)  
Fig. 8. Interfered samples’ positions resultant from the histogram-based interference detection method.

TABLE III  
CONFIGURATION PARAMETERS OF THE EGO RADAR
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Ego radar</td></tr><tr><td rowspan=1 colspan=1>Carrier frequency $f _ { c }$ </td><td rowspan=1 colspan=1>77.8GHz</td></tr><tr><td rowspan=1 colspan=1>Sweeping bandwidth $B W _ { \mathrm { s w } }$ </td><td rowspan=1 colspan=1>400 MHz</td></tr><tr><td rowspan=1 colspan=1>Chirp duration $T _ { \mathrm { c h i r p } }$ </td><td rowspan=1 colspan=1>25 $. 6 \mu \mathrm { s }$ </td></tr><tr><td rowspan=1 colspan=1>Pulse repetition time $T _ { \mathrm { c p } }$ </td><td rowspan=1 colspan=1> $4 0 \mu \mathrm { s }$ </td></tr><tr><td rowspan=1 colspan=1>Sweep slope K</td><td rowspan=1 colspan=1>15.63MHz/µs</td></tr><tr><td rowspan=1 colspan=1>ADC sampling rate $F _ { s }$ </td><td rowspan=1 colspan=1>20MHz</td></tr><tr><td rowspan=1 colspan=1>Number of fast-time samplesL</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>Number of slow-time samplesN</td><td rowspan=1 colspan=1>256</td></tr></table>

TABLE IV  
RADAR CONFIGURATION USED IN THE SIMULATIONS
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Aggressor radar1</td><td rowspan=1 colspan=1>Aggressor radar2</td><td rowspan=1 colspan=1>Aggressor radar3</td></tr><tr><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>77.9GHz</td><td rowspan=1 colspan=1>77.8GHz</td><td rowspan=1 colspan=1>77.8GHz</td></tr><tr><td rowspan=1 colspan=1> $\overline { { B W _ { \mathrm { s w } } } }$ </td><td rowspan=1 colspan=1>600MHz</td><td rowspan=1 colspan=1>1GHz</td><td rowspan=1 colspan=1>400MHz</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c h i r p } }$ </td><td rowspan=1 colspan=1> $1 2 \mu s$ </td><td rowspan=1 colspan=1>21.5µs</td><td rowspan=1 colspan=1>400MHz</td></tr><tr><td rowspan=1 colspan=1> $\underline { { T _ { \mathrm { c p } } } }$ </td><td rowspan=1 colspan=1>30µs</td><td rowspan=1 colspan=1>32µs</td><td rowspan=1 colspan=1>84µs</td></tr><tr><td rowspan=1 colspan=1> $K$ </td><td rowspan=1 colspan=1>50MHz/µs</td><td rowspan=1 colspan=1>46.5MHz/µs</td><td rowspan=1 colspan=1>4.76MHz/µs</td></tr><tr><td rowspan=1 colspan=1>Range</td><td rowspan=1 colspan=1>10m</td><td rowspan=1 colspan=1>20m</td><td rowspan=1 colspan=1>15m</td></tr><tr><td rowspan=1 colspan=1>Veloctity</td><td rowspan=1 colspan=1>12m/s</td><td rowspan=1 colspan=1>-10m/s</td><td rowspan=1 colspan=1>5m/s</td></tr></table>

## A. Simulation Results

As mentioned in SectionII-B, the simulation focused on the common interference situation that the aggressor radar and the ego radar adopt different PRTs, FM slopes and bandwidths are considered. The specific configuration parameters for both ego and aggressor radars were shown in Table III and Table IV.

Fig. 8 depicted the B matrix, indicating the fast- and slow-time positions of the received samples identified being interfered by the aggressor radar using the histogram-based interference detection method.As three aggressor radar signals with different parameters were considered, the interfered fragments highlighted with bright yellow color in Fig. 8 had different duration in the time domain, among which the longer interfered fragments were caused by the aggressor radar 3. Due to the difference of FM slope between aggressor radar 3 and the ego radar was the least, according to (10), the interference duration was the longest. Some chirp signals were non-interfered detected by the histogram method, such as the chirp signal at the 10th slow-time index marked by red dashed boxes in Fig. 8, and thus it can be selected as s<sub>clean</sub>.

![](images/c70b9ab73cac4c78f3336fb40ef85882c9b31cf4d38ddb89869fd2dc313377b1.jpg)

(a)  
![](images/1f2ec55fd5b0b4185e36296e6f9211a5a0f06acd6739962634f46acee7225422.jpg)  
(b)  
Fig. 9. Simulation data validation. (a)Range Doppler profile of Original signal. (b)Range Doppler profile after interference suppression.

The range-Doppler profile calculated from the originally received beat signalsand the beat signals after interference suppression were demonstrated in Fig. 9. An index of the suppression performance was the interference-to-signal ratio (ISR) denoted with $\gamma _ { i s r } .$ , which was calculated by averaging the heights of all portions below −10 dB relative to the global maximal height of the profile. It can be observed from Fig. 10(a) that $\gamma _ { i s r }$ equals −31.22 dB in the case without interference suppression. Note that the values at the iteration 0 represented the case without interference suppression algorithm activated. By using the proposed dual-RLS algorithm, $\gamma _ { i s r }$ decreased rapidly to −43.14 dB in the first iteration, and converged to −47.07 dB at the fifth iteration, which effectively lowers the ISR.

Although the ISR of originally received beat signals below −30 dB was relatively low, the value only represented the average heights, and the heights of many portions above 20 dB depicted in Fig. 9(a) were relatively high, which obscured targets detection. For further illustrating the performance of interference suppression, the index “global to local maxima ratio (GLMR)” denoted with $\gamma _ { g l m r }$ was introduced, which was calculated as the ratio between the global maximum of the range-Doppler profile and a local maxima, i.e., the spectral height of a peak in the profiles. A larger GLMR, especially in the case where the local maxima were caused by the interference, indicates a lower possibility of detecting a false target, implying a better robustness of the performance. Fig. 10(a) depiced the variation of $\gamma _ { g l m r }$ in each iteration versus the “index” of the local maxima sorted in descendant order. It can be observed that $\gamma _ { g l m r }$ decreased from the original 11.53 dB approximately to below 29.78 dB in the first iteration with index=1, and the levels converged after five iterations.

![](images/ebf9c047c9808e72d7436d1cf039d4bc97e247b016f0e67be01d1db71667ce6b.jpg)

(a)  
![](images/b830e5e462f8827a3eb53754ed6eb16301dc66420c3baabcd9cb5592f7b510e8.jpg)  
(b)  
Fig. 10. Performance of iterative filtering.(a)Variation of AINSR $\gamma _ { i s r } .$ (b)Variation of GLMR $\gamma _ { g l m r }$

More study results not shown here indicate that when the interference detection was accurate, the algorithm can converge rapidly in less than 10 iterations. However, when the interference segments’ location detected deviated even slightly from the true locations, the number of iterations after which the convergence was achieved increases, and the significant fluctuations of $\gamma _ { i s r }$ and $\gamma _ { g l m r }$ with respect to the iteration index were observed. This posed the necessity of maintaining the detection accuracy of interference and the successful identification of their existence regions.

## B. Measurement Results

Measurements campaign for car-to-car cross-interference investigation were conducted on road using the 77 GHz millimeter wave radar evaluation kits from Texas Instruments, i.e. AWR1243BOOST board, AWR2243BOOST board [42] and MMWCAS-RF-EVM board [43]. Two scenarios were adopted in the measurement: the ego radar remained static in the closed road segment(Fig. 11) and ego radar moved in the open city road segment(Fig. 12), with the aggressor radar approaching towards the ego radar at a certain speed. Different PRTs and FM slopes were used in ego and aggressor radar to ensure that interference is encountered.

![](images/5f9747e318edc3408739bc3b444ab01317a2a788d3bf0cfa7b20e6fe0f10defe.jpg)  
Fig. 11. The measured scenario 1.

![](images/6aa0f6bb229ce50992e77d7246d4cb06fb32bce78eda3aa59b5d63323abd54df.jpg)  
Fig. 12. The measured scenario 2.

TABLE V  
RADAR CONFIGURATION IN MEASURED SCENARIO 1
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Ego radar</td><td rowspan=1 colspan=1>Aggressor radar</td></tr><tr><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>77.6GHz</td><td rowspan=1 colspan=1>77.6GHz</td></tr><tr><td rowspan=1 colspan=1> $B W _ { \mathrm { s w } }$ </td><td rowspan=1 colspan=1>400MHz</td><td rowspan=1 colspan=1>400MHz</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c h i r p } }$ </td><td rowspan=1 colspan=1> $5 1 . 2 \mu \mathrm { s }$ </td><td rowspan=1 colspan=1> $2 5 6 \mu \mathrm { s }$ </td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c p } }$ </td><td rowspan=1 colspan=1> $8 0 \mu \mathrm { s }$ </td><td rowspan=1 colspan=1> $3 0 0 \mu \mathrm { s }$ </td></tr><tr><td rowspan=1 colspan=1> $k$ </td><td rowspan=1 colspan=1>7.81MHz/µs</td><td rowspan=1 colspan=1>1.56MHz/µs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { F _ { s } } }$ </td><td rowspan=1 colspan=1>10MHz</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> $L$ </td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>/</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N } }$ </td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>1</td></tr></table>

1) Staic Ego Radar: Fig.11 illustrated the first measured scenario setup in the closed road where the AWR2243BOOST board was static as the ego radar and the AWR1243BOOST board (shown in Fig.11), being the aggressor radar, was attached to the window of a van which moves towards the ego radar with a velocity of about 20km/h-30km/h, i.e. about 5m/s-8m/s. The values of the radar parameters were shown in Table V.

Fig. 13 depictd the slow-time and fast-time locations B f the signals received by the ego radar where the interference was found to exist in the highlighted positions. Interference detection with histogram method illustrated that 77 chirps out of 128 were interfered, and the complete chirp signals without being interfered are selected as $\pmb { s } _ { \mathbf { c l e a n } }$ in the dual-RLS algorithm. The range-Doppler profile calculated from the original signal without interference suppression shown in Fig. 14(a) depicted a widely spread pattern caused by the interference, which yielded an ISR of −29.2 dB. Although the ISR appeared to be low, many high lobes existing in the proximity of the targets can easily mislead the target detection. With the proposed dual-RLS algorithm implemented, the ISR reduced to −39.7dB, i.e. 10.5 dB lower than the level without interference suppression, within two iterations achieving the convergence. Fig. 14(b) exhibited that the peaks indicating the existence of the targets in the range-Doppler profile can be clearly appreciated with the surrounding interference-resultant lobes suppressed substantially.

![](images/b029925df635d54d99a0e250d1af997dfa83fd7b4c065cec2a6a0875c0686dcd.jpg)  
Fig. 13. Interfered samples positions marked using the histogram-based interference detection method.

TABLE VI  
THE AVERAGE INTERFERENCE TO SIGNAL RATIOS (ISRS) $\gamma _ { i s r }$ IN DB FOR THE RANGE-DOPPLER PROFILES RESULTED BY USING DIFFERENT ALGORITHMS
<table><tr><td rowspan=1 colspan=1>Suppression algorithms</td><td rowspan=1 colspan=1>ISR $\gamma _ { i s r } ( \mathrm { d B } )$ </td></tr><tr><td rowspan=1 colspan=1>Without interference suppression</td><td rowspan=1 colspan=1>-29.219</td></tr><tr><td rowspan=1 colspan=1>The dual-RLS algorithm proposed</td><td rowspan=1 colspan=1>-39.745</td></tr><tr><td rowspan=1 colspan=1>The KF algorithm [13]</td><td rowspan=1 colspan=1>-39.135</td></tr><tr><td rowspan=1 colspan=1>The RLS denoising method [44]</td><td rowspan=1 colspan=1>-38.621</td></tr><tr><td rowspan=1 colspan=1>The LMS-ANC algorithm [17]</td><td rowspan=1 colspan=1>-36.694</td></tr><tr><td rowspan=1 colspan=1>The WD algorithm [7]</td><td rowspan=1 colspan=1>-36.426</td></tr></table>

The suppression performance,comprising ISR, GLMR and range Doppler profiles, of the proposed algorithm was compared with some traditional methods, including the Kalman filter (KF) algorithm [13], the wavelet denoising (WD) algorithm [7] and the LMS-ANC algorithm [17]. In addition, a denoising method [44] with RLS adaptive filter was also incorporated into the performance comparison. The RLS denoising method was applied to suppress interference, where the input signal and the desired signal of the adaptive filter were set as the received beat signal $\mathbf { \Delta } \mathbf { s } _ { b }$ and the interferencefree signal samples $s _ { \mathrm { c l e a n } } ,$ , respectively. Same as the proposed algorithm, the RLS denoising method was only executed to remove the interference parts of $\mathbf { \Delta } \mathbf { s } _ { b }$ identified being interfered. Fig. 14(a) to 14(f) depicted range-Doppler profiles obtained with the original received signal, and suppressed with the dual-RLS algorithm, the KF algorithm, the RLS denoising method, the WD algorithm and the LMS-ANC algorithm implemented, respectively, which an enlarged view of the portion where some moving targets exist was also provided in these figures. It can be observed that the LMS-ANC algorithm and the WD algorithm still retained significant interference spreading in the profile, while the RLS denoising method, the KF algorithm and the proposed dual-RLS algorithms outperformed these methods by suppressing the interference to lower levels. By scrutinizing at the enlarged pictures in Fig. 14, a more clear observation showed that the interference components around the targets are lower for the dual-RLS, the RLS denoising method, and the KF algorithms than for the other methods. Table VI demonstrated that all the considered algorithms reduced ISR effectively, and the reduction of the proposed dual-RLS algorithm was about 0.6dB, 1.1dB, 3dB and 3.3dB more than using the KF algorithm, RLS denoising method, the LMS-ANC and WD algorithms, respecrively.

![](images/aff28db87505429dbc455584847f33ea1bf0ad787757425a7437f17b6a61c417.jpg)  
(a)

![](images/35164b5b98976318aaf47f4c77bc40c4e86d07b20ee1ff923b96513f90e2e20c.jpg)  
(b)

![](images/1dfae7da7f3a24083712f5a2c4a8775392f08ad399c0ac3b4d5a4c7b5184fdf0.jpg)  
(c)

![](images/a59c82f2053d99f78815fe13e9af15951b3dceb8c70912d004dfab809a732ef9.jpg)  
(d)

![](images/3da909b633332367ba393291633d492962ab52e9280662d3f201b59667159b77.jpg)  
(e)

![](images/87979b815ec91b4c62a21f133a5d2f81778b8832b6c0c38a994e55ef21e0b119.jpg)  
(f)

Fig. 14. Range Doppler profiles for (a) measured signal with interference, (b) dual RLS algorithm, (c) the KF algorithm [13], (d) the RLS denoising method [44], (e) the LMS-ANC algorithm [17], (f) the WD algorithm [7].  
![](images/70db4beb1d00c9e5b8e2bcc6bc7e398f6b171f38093ef4a50e6e32d207e050bd.jpg)  
Fig. 15. The GLMR $\gamma _ { g l m r }$ versus local maxima indices for different algorithms.

Besides, the GLMR $\gamma _ { g l m r }$ versus the indices of the local maxima sorted in descending order shown in Fig 14, exhibiting that for the indices beyond 30, the spectral height differences obtained by using the proposed dual-RLS algorithm become the largest among all methods,and specifically, they were 3 dB and 2dB larger than those observed for the KF algorithm and the RLS denoising method, respectively. While the indices beyond 120, the $\gamma _ { g l m r }$ of the RLS denoising method is gradually less than that of the KF algorithm.

2) Moving Ego Radar: In this experiment, measurement was conducted along a city road with multiple vehicles parking on either side. The AWR2243BOOST board still acted as ego radar to capture measurement data, except that it changed from static to moving state. To ensure the successful acquisition of interference signals while ego radar moved in the road, the large-scale cascades MMWCAS-RF-EVM with 12 transmitting and 16 receiving was adopted as the aggressor radar for more signal capacity. Fig. 12 showed the measurement setup where the ego radar (AWR2243BOOST board) and the aggressor radar (MMWCAS-RF-EVM board) were mounted on two moving vehicles separately: one was fixed on the hood of a car and the other on the roof of a van. These two radars moved at the velocity of about 30km/h-40km/h individually, resulting a relative velocity up to 60km/h-80km/h as they moved towards each other. The values of the radar parameters were described in Table VII.

In this measured scenario, the slow-time and fast-time locations B based on histogram method where the highlighted fragments with bright yellow color and the fragments marked with blue color in Fig. 17 refer to being interfered and non-interfered, respectively. The interference locations observed in the Fig. 17 were not periodic, which was due to the reason that the two radars moved fast and meanwhile, the interference signals becamed randomly fluctuated for the fast fading. Furthermore, the vehicles on the road sides caused multipath propagation which resulted in small-scale fading for the received signals.

TABLE VII  
RADAR CONFIGURATION IN MEASURED SCENARIO 2
<table><tr><td rowspan=1 colspan=1>Parameters</td><td rowspan=1 colspan=1>Ego radar</td><td rowspan=1 colspan=1>Aggressor radar</td></tr><tr><td rowspan=1 colspan=1> $f _ { c }$ </td><td rowspan=1 colspan=1>77.8GHz</td><td rowspan=1 colspan=1>77.8GHz</td></tr><tr><td rowspan=1 colspan=1> $B W _ { \mathrm { s w } }$ </td><td rowspan=1 colspan=1>400MHz</td><td rowspan=1 colspan=1>400MHz</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c h i r p } }$ </td><td rowspan=1 colspan=1> $2 5 . 6 \mu \mathrm { s }$ </td><td rowspan=1 colspan=1> $5 1 . 2 \mu \mathrm { s }$ </td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c p } }$ </td><td rowspan=1 colspan=1> $4 0 \mu \mathrm { s }$ </td><td rowspan=1 colspan=1> $2 5 6 \mu \mathrm { s }$ </td></tr><tr><td rowspan=1 colspan=1> $k$ </td><td rowspan=1 colspan=1> $1 5 . 6 3 \mathrm { M H z } / \mu \mathrm { s }$ </td><td rowspan=1 colspan=1>7.81MHz/µs</td></tr><tr><td rowspan=1 colspan=1> $\overline { { F _ { s } } }$ </td><td rowspan=1 colspan=1>10MHz</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> $L$ </td><td rowspan=1 colspan=1>255</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1> $\overline { { N } }$ </td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>1</td></tr></table>

![](images/068b6b83edb2a092f04bdb9ce33052033aa4f157bee7c0f6749a3168d8e0ebd9.jpg)

(a)  
![](images/1aed8e9f3f82b4e1b4d0442193bcbd09c16909ba86c0101bca8ae5b68a8f9618.jpg)

(b)  
![](images/c064aae5e2c6760b668f5a229c35e2757e79ba0105042e50d9b606ed52b8b2c5.jpg)  
(c)

![](images/99e431ce7fc056ca591d6a1c9dd9e7353b6b0267e757fa10a490060006705b23.jpg)  
(d)  
Fig. 16. Range Doppler profiles for (a) measured signal with interference, (b) dual RLS algorithm, (c) the KF algorithm [13], (d) the RLS denoising method [44].

![](images/4fefb16fce6629898315aaffc906430457a05c631cf6cabd18dad965e3567d85.jpg)  
Fig. 17. Interfered samples positions marked using the histogram-based interference detection.

![](images/4117d8cf783cd05d46665d250fcb94cfc0e818b03a56f5b82af293b577354bf8.jpg)  
Fig. 18. The GLMR $\gamma _ { g l m r }$ versus local maxima indices for different algorithms.

The range-Doppler profile of the received signal in Fig. 16(a) demonstrated that there are consecutive target peaks at a velocity of about −10m/s within the detection range, which were contributed by static roadside buildings that, compared with the ego radar, moved in opposite directions at the same velocity. Accordingly, the velocity of the ego radar was about 10m/s, i.e. 36km/h, at the moment shown in Fig. 16(b). The target peaks observed in the Fig. 16(a) with different intensity between −10m/s and 0m/s were contributed by other moving vehicles and pedestrians, which moving in the same direction as the ego radar but with lower velocity. In addition, the target peak contributed by the attack radar was located at range and velocity of about 15m and 18m/s in the Fig. 16(a).

It can be observed from Fig. 16(a) that the range-Doppler profile exhibits many stripes, due to the existence of interference. Fig. 16(d) demonstrated that with the proposed dual-RLS algorithm implemented, the stripe lobes in the range-Doppler profile can be suppressed effectively and the algorithm achieved the convergence within one iteration. However, by using the KF algorithm and the RLS denoising method, the stripe lobes still remained in the range-Doppler profile, and in addition, some new stripe lobes were generated by the KF algorithm within the detection range of 0 to 5 m. The new stripe lobes were illustrated as well as GLMR γ<sub>glmr</sub> in Fig. 18 where the $\gamma _ { g l m r }$ of the KF algorithm was larger than the measured data within the first 100 indices, indicating that the new spreading sidelobes were raised in the profile. The performance of the $\gamma _ { g l m r }$ processed by RLS denoising method is slightly better than that of KF algorithm, but the $\gamma _ { g l m r }$ is also greater than the measured data within the first 70 indices, and there are still sidelobes that are not suppressed. The $\gamma _ { g l m r }$ implemented by the proposed algorithm still suppress the whole interference sidelobes well in the motion situation, exhibiting its superior performance in the dynamic scene.

TABLE VIII  
COMPARISON OF THE COMPUTATION TIME WITH DIFFERENT ADAPTIVE FILTERING ALGORITHM AND INTERFERENCE SUPPRESSION ALGORITHMS
<table><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>Algorithms</td><td rowspan=1 colspan=2>Time</td></tr><tr><td rowspan=5 colspan=1>Adaptivefiltering</td><td rowspan=1 colspan=1>LMS</td><td rowspan=1 colspan=2>73us</td></tr><tr><td rowspan=1 colspan=1>NLMS</td><td rowspan=1 colspan=2>81 us</td></tr><tr><td rowspan=1 colspan=1>RLS</td><td rowspan=1 colspan=2>455 us</td></tr><tr><td rowspan=1 colspan=1>KF</td><td rowspan=1 colspan=2>538 us</td></tr><tr><td rowspan=1 colspan=1>Dual-RLS</td><td rowspan=1 colspan=2>802 us</td></tr><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>Algorithms</td><td rowspan=1 colspan=1>Time</td><td rowspan=1 colspan=1>TRFR $\gamma _ { t r f r }$ </td></tr><tr><td rowspan=4 colspan=1>Interferencesuppression</td><td rowspan=1 colspan=1>The KF algorithm [13]</td><td rowspan=1 colspan=1>34.4ms</td><td rowspan=1 colspan=1>2.7</td></tr><tr><td rowspan=1 colspan=1>The RLS denoising method [44]</td><td rowspan=1 colspan=1>53.7ms</td><td rowspan=1 colspan=1>4.2</td></tr><tr><td rowspan=1 colspan=1>The dual RLS algorithm proposed</td><td rowspan=1 colspan=1>79.3ms</td><td rowspan=1 colspan=1>6.2</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { f r a m e } }$ </td><td rowspan=1 colspan=1>12.8ms</td><td rowspan=1 colspan=1>1</td></tr></table>

## VI. DISCUSSION

Both the simulation study results and the analysis based on measurements demonstrated that the proposed dual-RLS algorithm is an effective interference suppression approach applicable in the scenarios with multiple vehicles equipped with automotive radars. Compared to traditional interference suppression methods, the dual-RLS algorithm suppresses the interferences side lobe to a lower level and restores the original desired signals with higher stability. This effect is more evident in the ego-radar-moving case where the side lobes caused by interference signals reduce to negligible levels in the Dopplerfrequency domain.

From the comparisons among these methods we also observed that the proposed dual-RLS algorithm even owns better performance than the widely-used KF algorithm which outperforms most of the conventional methods. The performance of the RLS denoising method is the closest to that of the KF algorithm in the two measured scenarios, where the KF algorithm performs better in scenario 1 with a more regular interference distribution, while the RLS denoising method slightly outperforms the KF algorithm in scenario 2 with the interference fragments demonstrating random behavior. This result may be due to the reduced length of undistorted signal samples required in signal restoration in the case that the KF algorithm proposed in [13] applied in the scenario 2, and thus the interference suppression performance decreases.

Theoretically, the KF-based method requires $\mathcal { O } ( N ^ { 2 . 3 7 6 } )$ [46] operations per iteration, yielding a complexity higher than the RLS algorithm with $\mathcal { O } ( N ^ { 2 } )$ operations per sample (N being the filter length) [45]. This can be illustrated from the computation time of the different filtering algorithms shown in Table VIII, which provides the average filtering time of a 256-sample chirp signal for a personal computer. Furthermore, Table VIII provides the CPU execution time of the interference suppression algorithm and the time-to-radar-frame $T _ { \mathrm { f r a m e } }$ ratio (TRFR) denoted with $\gamma _ { t r f r }$ . In the proposed dual-RLS algorithm, due to the RLS-nested structure, a higher complexity and a longer execution time are resulted compared to the KFbased algorithm [13] and the RLS-based method [44]. The RLS method with sequential filtering of chirp sequences takes longer time than KF algorithm being implemented with chirp fragments in a frame vectorized concatenated as a long temporal sequence. According to the $\gamma _ { t r f r } .$ , the great performance of the proposed algorithm is obtained with the longer computing time. A possible way to reduce the complexity of the dual-RLS algorithm is to consider replacing the original RLS with fast RLS algorithms [45] or similar kinds. This is considered to be a future work as the study here continues.

## VII. CONCLUSION

In this paper, an interference suppression algorithm utilizing two superposition ANC with RLS filters is proposed for application of interference suppression for FMCW automotive radar systems. The fast convergence property of the RLS allows this algorithm to be applied where vehicles move in proximity at high speeds. Simulation studies and measurements conducted with 77 GHz millimeter-wave FMCW automotive radar systems in vehicular cross-interference scenarios were conducted for performance evaluation. The results demonstrate that the proposed dual-RLS algorithm outperforms some widely-used conventional interference suppression algorithms in terms of lowering interference suppression levels and enhancing the capability of retrieving the original range-Doppler profile, especially in the ego-radar-moving case. Meanwhile, the dual-RLS structure of the algorithm does not require any prior information of the interference signal, which makes the algorithm potentially applicable in the cases with other types of interference present in the ego radar beat signals. Future studies on complexity optimization will continue. By appropriately extending to the automobile industry, the safer driving and fewer traffic accidents can be achieved as the benefits of effectively suppressing interference by using the proposed dual-RLS technique.

## REFERENCES

[1] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[2] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[3] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[4] S. Lee, Y. Yoon, J. Yoon, H. Sim, and S. Kim, “Periodic clutter suppression in iron road structures for automotive radar systems,” IET Radar, Sonar Navigat., vol. 12, no. 10, pp. 1146–1153, Oct. 2018.

[5] M. Umehira, Y. Watanabe, X. Wang, S. Takeda, and H. Kuroda, “Interradar interference in automotive FMCW radars and its mitigation challenges,” in Proc. IEEE Int. Symp. Radio-Freq. Integr. Technol. (RFIT), Sep. 2020, pp. 220–222.

[6] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in Proc. 9th Eur. Radar Conf., 2012, pp. 1–5.

[7] S. Lee, J. Lee, and S. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[8] W.-H. Lee and S. Lee, “Geometric sequence decomposition-based interference cancellation in automotive radar systems,” IEEE Access, vol. 10, pp. 4318–4327, 2022.

[9] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[10] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf., Apr. 2018, pp. 405–410.

[11] Z. Liu, W. Lu, J. Wu, S. Yang, and G. Li, “A PELT-KCN algorithm for FMCW radar interference suppression based on signal reconstruction,” IEEE Access, vol. 8, pp. 45108–45118, 2020.

[12] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[13] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 726–731.

[14] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[15] M. Umehira, T. Okuda, X. Wang, S. Takeda, and H. Kuroda, “An adaptive interference detection and suppression scheme using iterative processing for automotive FMCW radars,” in Proc. IEEE Radar Conf., Sep. 2020, pp. 1–5.

[16] D. Ammen, M. Umehira, X. Wang, S. Takeda, and H. Kuroda, “A ghost target suppression technique using interference replica for automotive FMCW radars,” in Proc. IEEE Radar Conf., Sep. 2020, pp. 1–5.

[17] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[18] Y. Li, C. Wang, F. Li, X. Han, and Y. Song, “An adaptive interference cancellation method for automotive FMCW radar based on waveform optimization,” in Proc. IET Int. Radar Conf., 2021, pp. 666–670.

[19] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[20] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[21] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[22] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in Proc. IEEE Radar Conf., Apr. 2018, pp. 0252–0256.

[23] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Techn., vol. 65, no. 5, pp. 1727–1734, May 2017.

[24] G. P. Babur, O. A. Krasnov, and L. P. Ligthart, “Inter-period compensation algorithm in full-polarimetric FMCW radar,” in Proc. 7th Eur. Radar Conf., 2010, pp. 156–159.

[25] M. Wahab, Y. P. Saputera, Y. Wahyu, and A. Munir, “Isolation improvement for X-band FMCW radar transmit and receive antennas,” in Proc. Int. Conf. Radar, Antenna, Microw., Electron., Telecommun. (ICRAMET), Oct. 2016, pp. 110–114.

[26] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun. 2016, pp. 1–9.

[27] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[28] C. Aydogdu, N. Garcia, L. Hammarstrand, and H. Wymeersch, “Radar communications for combating mutual interference of FMCW radars,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2019, pp. 1–6.

[29] B. Widrow et al., “Adaptive noise cancelling: Principles and applications,” Proc. IEEE, vol. 63, no. 12, pp. 1692–1716, Apr. 1975.

[30] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, Sep. 2018.

[31] S. D. Stearns, “Fundamentals of adaptive signal processing,” in Advanced Topics in Signal Processing. Upper Saddle River, NJ, USA: Prentice-Hall, 1987, pp. 246–288.

[32] D. Wu, L. Shen, J. Xie, and Y. Wang, “Improved LMS algorithm and its application in direct path and multipath cancellation for passive radar,” in Proc. IEEE 14th Int. Conf. Commun. Technol., Nov. 2012, pp. 1301–1305.

[33] F. Ling and J. Proakis, “Nonstationary learning characteristics of least squares adaptive estimation algorithms,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process., Apr. 1984, pp. 118–121.

[34] F. Ling and J. Proakis, “Adaptive lattice decision-feedback equalizerstheir performance and application to time-variant multipath channels,” IEEE Trans. Commun., vol. COM-33, no. 4, pp. 348–356, Oct. 1985.

[35] C. Elisei-Iliescu, C. Paleologu, J. Benesty, C. Stanciu, C. Anghel, and S. Ciochina, “Recursive least-squares algorithms for the identification of low-rank systems,” IEEE/ACM Trans. Audio, Speech, Language Process., vol. 27, no. 5, pp. 903–918, May 2019.

[36] S. Sukhumalchayaphong and C. Benjangkaprasert, “Variable forgetting factor RLS algorithm for adaptive echo cancellation,” in Proc. 14th Int. Conf. Control, Autom. Syst. (ICCAS), Oct. 2014, pp. 971–974.

[37] E. Eleftheriou and D. Falconer, “Tracking properties and steady-state performance of RLS adaptive filter algorithms,” IEEE Trans. Acoust., Speech, Signal Process., vol. ASSP-34, no. 5, pp. 1097–1110, Oct. 1986.

[38] X. Cheng, Y. He, and M. Guizani, “OFDM de-noising with RLS adaptive filter,” in Proc. 19th Int. Symp. Wireless Pers. Multimedia Commun. (WPMC), 2016, pp. 395–399.

[39] K. Tbarki, S. Ben Said, and N. Ellouze, “Non-linear filtering for landmine detection on ground penetration radar data,” in Proc. 2nd Int. Conf. Adv. Technol. Signal Image Process. (ATSIP), Mar. 2016, pp. 200–205.

[40] R. Z. Rui Zhang and G. L. Gang Li, “A histogram based method for micro-Doppler interference removal,” in Proc. IET Int. Radar Conf., 2015, pp. 1–5.

[41] E. Temlioglu, I. Erer, and D. Kumlu, “Histograms of dominant orientations for anti-personnel landmine detection using ground penetrating radar,” in Proc. 4th Int. Conf. Electr. Electron. Eng. (ICEEE), Apr. 2017, pp. 329–332.

[42] P. Zhu, X. Yin, J. Rodriguez-Pineiro, Z. Chen, P. Wang, and G. Li, “Measurement-based wideband space-time channel models for 77 GHz automotive radar in underground parking lots,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 10, pp. 19105–19120, Oct. 2022.

[43] AWRx Cascaded Radar RF Evaluation Module, Texas Instruments, Dallas, TX, USA, 2019. [Online]. Available: https://www.ti. com/tool/MMWAVE-STUDIO

[44] G. Xing and Y. Zhang, “Analysis and comparison of RLS adaptive filter in signal de-noising,” in Proc. Int. Conf. Electr. Control Eng., Yichang, China, Sep. 2011, pp. 5754–5758.

[45] Y. V. Zakharov, G. P. White, and J. Liu, “Low-complexity RLS algorithms using dichotomous coordinate descent iterations,” IEEE Trans. Signal Process., vol. 56, no. 7, pp. 3150–3161, Jul. 2008.

[46] C. Montella, “The Kalman filter and related algorithms: A literature review,” 2011. [Online]. Available: https://www.researchgate.net/ publication/236897001\_The\_Kalman\_Filter\_and\_Related\_Algorithms\_ A\_Literature\_Review

![](images/13e65d465c66f9c8508b3297294e1f2245adcd768464179b453b2776d1d0627f.jpg)  
Ping Wang received the M.Sc. degree in electronic information from the College of Electronics and Information Engineering, Tongji University, Shanghai, China, in 2023. Her research interests include millimeter-wave automotive radar interference identification and suppression, radar waveform design, wireless channel simulation modelling and algorithm design for complex scenarios.

![](images/2223eb7e1a4a4b4d651ebc0b57b042ee5a27a0a11e2cdabc1c1941b27fa8e9a7.jpg)

Xuefeng Yin (Member, IEEE) received the B.S. degree in optoelectronics engineering from the Huazhong University of Science and Technology, China, in 1995, and the M.Sc. degree in digital communications and Ph.D. degree in wireless communications from Aalborg University, Aalborg, Denmark, in 2002 and 2006, respectively. From 2006 to 2008, he was an Assistant Professor with Aalborg University. In 2008, he joined the College of Electronics and Information Engineering, Tongji University, Shanghai, China. He became a Full Professor in 2016 and has been the Vice Dean of the College from 2016 to 2021. In 2021, he was appointed the Vice Director of the division of development and disciplinary construction of Tongji University. He has authored or coauthored more than 150 technical articles, four books, 12 PCT patents, and 20 China patents. His research interests include the propagation channel characterization and modelling, high-resolution parameter estimation, positioning, localization, passive target tracking, and 5G/B5G/6G communications.

![](images/c3ce9f3eb29b3cb00c05049fdcb5be0633bcdb42664e323a5654ea0ca3ba7bdc.jpg)

José Rodríguez-Piñeiro (Member, IEEE) received the B.Sc. degree (Hons.) in telecommunications and M.Sc. degree (Hons.) in signal processing applications for communications from the University of Vigo, Pontevedra, Spain, in 2009 and 2011, respectively, and the Ph.D. degree (Hons.) in 2016. Between June 2008 and July 2011, he was a Researcher at the Department of Signal and Communications, University of Vigo. In 2011 he joined the Group of Electronics Technology and Communications of the University of A Coruña, Spain, as a

Researcher. After obtaining his Ph.D. degree, he continued working as a Post-Doctoral Researcher at the same group until July 2017. On August 2017, he joined the College of Electronics and Information Engineering, Tongji University, China, as a Post-Doctoral Researcher, becoming an Assistant Professor in 2020. He performed several research stays at the Technische Universität Wien, Vienna, Austria, and the National University of Asunción, Paraguay. From November 2012, he collaborates with the Department of Power and Control Systems, National University of Asunción in both teaching and research, and he has been an External Researcher of the Group of Electronics Technology and Communications of the University of A Coruña since 2018. He is the coauthor of more than 70 papers in peer-reviewed international journals and conferences, as well as three patents. He is also the leader or a member of the research team in more than 40 international, national and regional research projects funded by public organizations and private companies. His research interests include experimental evaluation of digital mobile communications, especially for high mobility environments, including terrestrial and aerial vehicular scenarios. He was awarded with two national- and regional-level predoctoral grants, two national-level Post-Doctoral fellowships and three national-level research stay grants, as well as with a Post-Doctoral award and a teaching quality award. Since 2023, he has been an Elected Member of the Propagation Committee of the IEEE Vehicular Technology Society (VTS).

![](images/1603eb1901cf6a802e0ae5e1bc0cc18d2ece7b3074ef282ed7c0406341d47835.jpg)  
Zhuoyu Chen received the B.S. degree in electronics and information engineering from the Tongji University, Shanghai, China, in 2019, and the M.Sc. degree from the College of Electronics and Information Engineering, Tongji University in 2022. His research interests include millimeter-wave vehicular radar signal processing and MIMO radar waveform design, and mutual interference detection and mitigation for the automotive radar applications.

![](images/199e68ed39d47d417fdeba08ebde6506aa9e826fa31c5e553d1ab4d7123c474b.jpg)

Pengqi Zhu received the B.S. degree in automotive engineering from the Tongji University, Shanghai, China, in 2020, where he is currently pursuing the Ph.D. degree in control science and engineering with the College of Electronics and Information Engineering. His research interests include millimeterwave vehicular radar signal processing and target recognition, time-variant channel modeling, and high-resolution parameter estimation algorithm for propagation channels.

![](images/2d55c4ae358291f932ca33f9d5c9a6794767356ca11d17054f7b85bbe355961f.jpg)

Gang Li (Member, IEEE) was born in Yingkou, China, in 1978. He received the Dipl.-Ing. degree in information technology from the Clausthal University of Technology, Clausthal-Zellerfeld, Germany, in 2007, and the Ph.D. degree in radar engineering from the Friedrich-Alexander-University of Erlangen–Nuremberg, Erlangen, Germany, in 2015. From 2007 to 2011, he joined the Institute of Electrical Information Technology, Clausthal University of Technology, where he was involved in wireless local positioning and synthetic aperture radar. From 2011

to 2015, he was with the Institute of Microwaves and Photonics, Friedrich-Alexander University of Erlangen–Nuremberg. From 2015 to 2019, he has been with Valeo Schalter und Sensor GmbH, Bietigheim–Bissingen, Germany, as a Radar System Engineer and leading R&D in 77 GHz automotive radar area. From 2019 to 2021, he joined Shanghai ZongMu Technology Co.,Ltd. as Director/Research Scientist and leading the automotive radar product line, he was singled out as the professor of engineering in artificial intelligence in 2019. Since 2022, he joined Saien Lingdong (Shanghai) Intelligent Technology Co., Ltd. as co-founder and now is leading the whole R&D team and automotive imaging radar product line. He has more than 30 international publications and more than 25 patens. His current research interests include imaging radar, sequential Monte Carlo methods, wireless local positioning, and automotive radar. The main research areas were sensor signal processing, bayes-based environment perception, multiple sensor fusion.