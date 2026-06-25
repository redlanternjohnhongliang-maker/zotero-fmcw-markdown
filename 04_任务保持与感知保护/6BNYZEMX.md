. LETTER .

September 2024, Vol. 67, Iss. 9, 199303:1–199303:2   
https://doi.org/10.1007/s11432-024-4110-4

# Interference mitigation and target detection for automotive FMCW radar with range-Doppler sparse regularization

Yan HUANG<sup>1\*</sup>, Yunxuan WANG<sup>1</sup>, Xiao ZHOU<sup>2</sup>, Hui ZHANG<sup>1</sup>, Yuan MAO<sup>1</sup>, Guisheng LIAO<sup>3</sup> & Wei HONG<sup>1</sup>

<sup>1</sup>State Key Lab of Millimeter Waves, Southeast University, Nanjing 210096, China; <sup>2</sup>Department of Computer Science, University College London, London WC1E 6BT, UK; <sup>3</sup>National Key Lab of Radar Signal Processing, Xidian University, Xi’an 710071, China

Received 26 January 2024/Revised 17 May 2024/Accepted 29 July 2024/Published online 16 August 2024

The invention of vehicles has shaped our modern society and accelerated our economy while causing many tragic incidents simultaneously. Some advanced driver-assistance systems (ADAS) based on surrounding environment sensors are widely applied and installed in modern vehicles to avoid possible casualty and property loss. Radar is one of the most promising sensors for its robustness in adverse weather and ability to work all day [1]. With the surge of automotive radar implementation, it is necessary to consider the co-existence of multiple automotive radars. The wide installment of automotive radars, especially the appliance of frequency modulated continuous wave (FMCW) radar, the original assigned frequency band, i.e., 76–79 GHz, is exhausted and mutual interference (MI) among automotive radars becomes a severe issue that undermines the performance of automotive radars.

Many studies have been proposed to mitigate MI among automotive radars. The methods can be categorized into four groups, i.e., joint radar-communication methods, waveform design methods, machine learning methods, and signal separation methods [2]. Among them, the signal separation method has the advantages of low cost, low time delay, and high portability; thus, it is one of the most promising methods and attacks much attention from both academic and commercial communities. A signal processing method usually follows the routine that transforms the signal under a certain base and then separates the interference signals and useful echo signals, making searching for bases crucial to the performance of interference mitigation [3]. However, previous signal processing techniques typically concentrate only on the received signals of a single chirp or one channel, disregarding the correlation of the received signal across channels. Therefore, in this study, we propose a novel range-Doppler (RD) sparse regularization-based interference mitigation, target detection, and 3-D parameters (range, velocity, and direction) estimation method for automotive radars. We first analyzed the low-rank characteristic of the strong single mutual interference in the time domain, then showed the feasibility of the principle component analysis (PCA) method in simple interference contaminated circumstances. Herein, we considered the sparsity of targets in the range-Doppler domain, proposed the optimization problem, and designed an alternating direction method of multipliers (ADMM) method to solve the problem. Numerical simulations and real-scene experiments are implemented to prove the feasibility and superiority of our method compared with the other methods.

Signal model. The transmitted FMCW chirp can be presented as [4]

$$
T \left( t \right) = A _ { t x } \exp \left( \mathrm { j } 2 \pi \left( f _ { c } + \gamma t \right) t \right) ,\tag{1}
$$

where $A _ { t x }$ is the amplitude of the transmitted signal, $f _ { c }$ is the carrier frequency, γ is the chirp rate, and t is the full time. For an FMCW radar system, the de-chirp processing is commonly accomplished by mixing the received signals with the conjugate of the transmitted one, i.e.,

$$
T ^ { \ast } \left( t , t _ { f } \right) = A _ { t x } \exp \left( - \mathrm { j } 2 \pi \left( f _ { c } + \gamma t \right) t \right) .\tag{2}
$$

After the de-chirp processing, the chirps are flattened, which significantly reduces the sampling rate requirement according to the Nyquist sampling theorem. The resultant signal of the de-chirp processing can be formulated as

$$
X \left( t _ { f } , t _ { s } \right) ~ = ~ R \left( t , t _ { f } \right) \times T ^ { * } \left( t , t _ { f } \right) ,\tag{3}
$$

where $t _ { f }$ is the fast time. As for the mutual interference transmitted by the aggressor radars and reaching the victim radar’s receiver antennas, the mutual interference after dechirp processing can be expressed as

$$
I \left( t _ { f } , t _ { s } \right) = T ^ { \prime } \left( t - \tau ^ { \prime } , t _ { f } - \tau ^ { \prime } \right) \times T ^ { * } \left( t , t _ { f } \right) .\tag{4}
$$

Herein, note that the interference directly arrives at the receivers of the victim radar, and then the time delay of in terference is a one-way delay.

Practical automotive radar systems often transmit a set of chirps to estimate the Doppler parameters. We assume that the number of chirps in one set is $L ,$ and the received signals of an automotive radar system can be expressed as

$$
Y = X + I + N ,\tag{5}
$$

![](images/72544233019a85315332e20c2d64bc79386d248d901aea8e8104cbbec167dbe3.jpg)  
Figure 1 (Color online) (a) Fast decay of singular values of mutual interference <sup>I</sup> matrix; (b) sparsity of useful echo signals <sup>X</sup> matrix in the RD domain.

where $Y , X , I , N \in \mathbb { C } ^ { K \times L }$ , K presents the sampling points of one single chirp. As shown in Figure 1(a), the sharp drop of singular values of a measured automotive radar signal polluted by MI reveals its low-rank property, which can be implemented to mitigate interference [5].

After performing a 2-D fast Fourier transform (FFT) to $\mathbf { Y } _ { \mathrm { ~ i ~ } }$ , the signal is transformed to the RD domain. Useful target echoes can be formulated as

$$
X _ { \mathrm { R D } } ( f _ { r } , f _ { d } ) = \mathrm { F F T } _ { t _ { s } } ( \mathrm { F F T } _ { t _ { f } } ( X ( t _ { f } , t _ { s } ) ) ) ,\tag{6}
$$

where $t _ { s }$ is the slow time. In this case, targets, including vehicles, pedestrians, and other scatterers, are focused within limited range-and-Doppler cells, as illustrated in Figure 1(b). In this domain, targets can be considered as sparse points.

Proposed range-Doppler sparse regularization method. Based on the low-rank property of the mutual interference and sparsity of targets in the RD domain, we propose an optimization problem as

$$
\begin{array} { r l } & { \underset { \boldsymbol { I } , \boldsymbol { X } _ { \mathrm { R D } } } { \operatorname* { m i n } } ~ \| \boldsymbol { I } \| _ { * } + \lambda \| \boldsymbol { X } _ { \mathrm { R D } } \| _ { 1 } } \\ & { \mathrm { s . t . } ~ \| \boldsymbol { Y } - \boldsymbol { I } - \mathcal { F } ^ { - 1 } \left( \boldsymbol { X } _ { \mathrm { R D } } \right) \| _ { \mathcal { F } } ^ { 2 } < \delta , } \end{array}\tag{7}
$$

where $\| \cdot \| _ { 1 }$ denotes the $\ell _ { 1 }$ norm, $X _ { \mathrm { R D } }$ denotes the useful echo signals <sup>X</sup> in RD domain, and $\mathcal F ( \cdot )$ denotes the 2-D FFT operation with its inverse operation being $\mathcal { F } ^ { - 1 } ( \cdot )$ . The problem above can be solved by alternating optimizing each variable with closed-form solutions using ADMM. The specific steps are shown in Appendix A. The algorithm of the proposed method is listed in Algorithm 1.

Experiment results in this study are shown in Appendix B.

Conclusion. In this study, we conducted a rigorous analysis of the signal characteristics of both the received echoes of targets and mutual interference. We then considered the low-rank property of strong mutual interference in the time domain, alongside the sparsity of targets within the RD domain. We then introduced a novel method predicated on RD sparse regularization for interference mitigation, target detection, and the estimation of three-dimensional parameters (range, velocity, and direction) for automotive radars. Detailed iteration deviation and experiment simulation can be found in Appendix B.

Algorithm 1 Proposed method   
Input: $\mathbf { } Y , \lambda , \mu ;$   
1: Initialize ${  \boldsymbol { X } } _ { \mathrm { R D } } ^ { ( 0 ) } ;$   
2: while not converged do   
3: $t \gets t + 1 ;$   
4: $\begin{array} { r } { { \boldsymbol { U } } \boldsymbol { \Lambda } { \boldsymbol { V } } ^ { \mathrm { H } } = { \boldsymbol { Y } } - \mathcal { F } ^ { - 1 } ( { \boldsymbol { X } } _ { \mathrm { R D } } ^ { ( t ) } ) + \frac { \mathbf { Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } ; } \end{array}$   
5: $\begin{array} { r } { \pmb { I } ^ { ( t + 1 ) } = \pmb { U } \mathrm { S V T } _ { \frac { 1 } { \mu ^ { ( t ) } } } \left( \pmb { Y } - \mathcal { F } ^ { - 1 } ( \pmb { X } _ { \mathrm { R D } } ^ { ( t ) } ) + \frac { \pmb { Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } \right) \pmb { V } ^ { \mathrm { H } } ; } \end{array}$   
6: $\begin{array} { r } { \pmb { X } _ { \mathrm { R D } } ^ { ( t + 1 ) } = \mathrm { S T } \left( \pmb { Y } - \pmb { I } ^ { ( t + 1 ) } + \frac { \pmb { Y } _ { 1 } ^ { ( t ) } } { \mu ^ { ( t ) } } , \frac { \lambda } { \mu ^ { ( t ) } } \right) ; } \end{array}$   
7: $\mathbf { \boldsymbol { X } } ^ { ( t + 1 ) } = \mathcal { F } ^ { - 1 } ( \mathbf { \boldsymbol { X } } _ { \mathrm { R D } } ^ { ( t + 1 ) } ) ;$   
8: ${ \pmb Y } _ { 1 } ^ { ( t + 1 ) } = { \pmb Y } _ { 1 } ^ { ( t ) } + \tilde { \mu ^ { ( t ) } } ( { \pmb Y } - { \pmb I } ^ { ( t + 1 ) } - { \pmb X } ^ { ( t + 1 ) } ) ;$   
9: $\mu ^ { ( t + 1 ) } = \operatorname* { m i n } ( \eta \mu ^ { ( t ) } , \mu _ { \operatorname* { m a x } } ) ;$   
10: end while   
11: Output: <sup>I</sup>, <sup>X</sup>.

Acknowledgements This work was supported by National Natural Science Foundation of China (Grant No. 62271142).

Supporting information Appendixes A and B. The supporting information is available online at info.scichina.com and link.springer.com. The supporting materials are published as submitted, without typesetting or editing. The responsibility for scientific accuracy and content remains entirely with the authors.

## References

1 Alland S, Stark W, Ali M, et al. Interference in automotive radar systems: characteristics, mitigation techniques, and current and future research. IEEE Signal Process Mag, 2019, 36: 45–59

2 Wang Y, Huang Y, Liu J, et al. Interference mitigation for automotive FMCW radar with tensor decomposition. IEEE Trans Intell Transp Syst, 2024, 25: 9204–9223

3 Zhou R, Chen J X, Huang Y, et al. A compact MIMO automotive radar using phase-aligned daisy-chain cascading topology and elevation compensation for 2D angle estimation. Sci China Inf Sci, 2023, 66: 162305

4 Wang Y, Huang Y, Wen C, et al. Mutual interference mitigation for automotive FMCW radar with time and fre quency domain decomposition. IEEE Trans Microwave Theor Techn, 2023, 71: 5028–5044

5 Sappl J, Meissner P, Haltmeier M. Low-rank approximation for FMCW automotive radar. In: Proceedings of International Conference on Sampling Theory and Applications (SampTA), Tallinn, 2017. 590–594