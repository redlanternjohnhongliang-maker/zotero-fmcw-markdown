# Dual-Domain Feature-Oriented Interference Suppression for FMCW Automotive Radar

Hao Zhang , Student Member, IEEE, Shunjun Wei , Member, IEEE, Xiang Cai, Lin Nie, Student Member, IEEE, Mou Wang , Jun Shi , Member, IEEE, and Guolong Cui , Senior Member, IEEE

Abstract—Frequency-modulated continuous wave (FMCW) radar is an excellent sensor; however, the widespread popularity and application of millimeter-wave (mmW) automotive radar, greatly increases the risk of mutual interference between vehicles, weakening the abilities of automotive radar to sense the environment. As a result, efficiently suppressing interference has been a challenge. To address this issue, this article presents a modified block coordinate descent optimization with dual-domain sparsities named BCD-DS, to synchronously suppress mutual interference between automotive FMCW radars by jointly leveraging the priors in time and frequency domains. First, the sparsities of the target and the interference on

![](images/1906bff1120f270ca6abbf18de090b722e240d57842bea0e0c5acf1da33ede4a.jpg)

multiple transformation domains are analyzed. Then, the interference suppression problem is modified into an optimization framework with regularizers being sparse priors in dual domains subject to the $\pmb { L } _ { 1 }$ norm constraint. Based on the joint optimization model, the target and interference are cooperatively estimated by the alternating direction method of multipliers (ADMM) scheme. One iteration consists of two phases, with the solution obtained at each phase updating the echoes, promoting a good convergence performance. BCD-DS balances interference suppression and target signal power. Both simulated and measured experiments validate the effectiveness of the proposed algorithm. Compared to the state-of-the-art algorithms, the results show that BCD-DS achieves better interference suppression performance and increases the signal-to-interference and noise ratio (SINR) by at least 20 dB, simultaneously retrieving the speeds and ranges of multiple targets with less than 1% error.

Index Terms— Block coordinate descent, dual-domain sparsities, millimeter-wave (mmW) automotive radars, mutual interference.

## I. INTRODUCTION

ILLIMETER-WAVE (mmW) automotive radar is an acteristics, capable of operating in heavy fog, dense smoke, thick ash, and other harsh scenarios with poor visibility [3], [4]. Therefore, people take advantage of automotive radar to obtain real-time road information, including the location, angle, and speed of the target. However, with the pursuit for safer and more convenient driving, advanced driver-assistance systems and autonomous driving technologies have been vigorously developed, with each car being equipped with several or a dozen radars, resulting in a complex electromagnetic environment on the road [5]. Vehicles on the road emit frequency-modulated continuous waves (FMCWs) with different parameters to detect targets. Emitted signals sharing the same carrier frequency [6] (typically 77 GHz), there is a risk of mutual interference between the vehicles, and this unintentional interference enters the receiver along with the echoes [7]. If the chirp slope of the aggressor vehicle (AV) is the same as ego-vehicle, a false target is generated [8]; if it is different, the signal-to-noise ratio of the target is greatly reduced, and, in severe cases, the interference can even drown out the target. Therefore, for collecting high-accuracy road information, it is of great importance to devote more effort to the research on automotive radar interference suppression.

## A. Related Works

In recent years, the challenge of suppressing mutual interference between automotive radars has drawn the interest of numerous scholars and several excellent methods have been proposed. This article divides these methods into two categories: radar hardware [9] and radar signal.

For the hardware-based method, the earliest scholars started with the antenna [10], [11], utilizing the boundary conditions of the target surface electromagnetic field by setting up a suitable antenna polarization mode to receive the target echo. Khoury et al. [12] proposed a radar control center that assigns corresponding waveform parameters based on real-time information from individual radars to avoid mutual interference. Moreover, designing the radar emitting waveforms can also achieve ideal effect [13]. Based on linear FMCW, Xu et al. [14] proposed an effective method to reduce mutual interference through the use of random subband spectral techniques; In [15], an interference mitigation method based on orthogonal waveforms was proposed; Hakobyan et al. [16] suggested a method based on cognitive interference avoidance and demonstrated it on a digital orthogonal frequency-division multiplexing radar. In [17], a phase-coded FMCWs (PC-FMCWs) system was presented to suppress interference by utilizing a set of time-delay filters to achieve beat-frequency alignment. However, the hardware-based approach might generate some system noise and the high requirements for radar circuitry lead to increased radar production costs.

For signal-based methods, scholars have made breakthroughs in the time domain [18], [19]. Choi et al. [20] utilized clipping and weighted envelope normalization to remove interference in the time domain; Jung et al. [21] adopted the Kalman filtering technique to reconstruct the time domain signal regions distorted by mutual interference, correctly estimating the target information. In [22], the interfered part of the time domain is intercepted and further reconstructed based on the matrix-pencil principle. In addition, several methods in the frequency domain can also suppress interference [23]. Liu et al. [24] analyzed the effect of multipath propagation on target detection and proposed an effective algorithm to remove ghost targets. The adaptive noise canceller (ANC) [25] takes the negative half of the beat frequency signal spectrum as a reference signal and cancels it out with the positive half where the target is located, reducing the noise level power around the target. Neemat et al. [26] interpolated beat-frequency signals in the short-time Fourier transform (STFT) domain; Singh et al. [27] spread the interference power over a wider spectrum to mitigate interference. Chen et al. [28] presented a complex empirical mode decomposition (CEMD) method by transferring the original signal to a high-frequency range unit and finally mitigating interference. Gradually, methods based on wavelet transforms have also been effective in this application [29], [30].

Naturally, some academics have introduced deep learning methods [31], [32], [33]. However, these network-based methods require a large amount of training data to drive them, which is not always ideal for complex and changing road environments. Currently, compressed sensing methods have been applied to extract targets [34], which are based on morphological component analysis (MCA) [35]. Wang et al. [36] designed a target echo-solving algorithm with row sparsity constraints. Zhang et al. [2] proposed an

RPCA-based covariance matrix reconstruction algorithm for interference suppression. Wang et al. [37] constructed a sparse and low-rank decomposition of the Hankel matrix by lifting measurements. Xu [38] proposed a bi-level l1 optimization based on the iterative shrinkage threshold algorithm (ISTA). Then, an iterative optimization algorithm was proposed using alternating direction method of multipliers (ADMMs) [39]. In [29], [40], and [41], the split augmented Lagrangian shrinkage algorithm (SALSA) [42] was adopted as the solution framework to suppress interference over different transform domains. However, the target with weak scattering intensity is easily lost in SALSA [38].

## B. Contributions

Inspired by the above discussion, for high-precision target detection and low-complexity computation in practical road traffic, this article presents an efficient block coordinate descent optimization with dual-domain sparsities (BCD-DS), which combines time and frequency domains to synchronously suppress interference. In general, our contributions and innovations are arranged in the following.

1) An effective interference suppression framework is proposed to alternate solving for targets based on modified block coordinate descent.

2) A novel strategy to leverage priors in time and frequency domains to cooperatively estimate interference and targets by updating the beat frequency signals.

3) Simulated and measured experiments show that our method can simultaneously acquire range and velocity information from both static and moving targets, reducing the interference power.

The remainder of this article is structured in the following. Section II introduces the relevant theory. Section III illustrates the principle of BCD-DS. Section IV reports simulated and measured experiments and the corresponding results are shown. A summary of the full paper is provided in Section V. Finally, The convergence analysis of the proposed method is given in the Appendix.

## II. RELATED THEORY

In this section, we present the relevant theory involved in the proposed method. First, the mathematical background of the mutual interference between automotive radars will be briefly mentioned. Second, the sparse characteristics of the signals according to the FMCW system are analyzed.

## A. Signal Model of Mutual Interference

Radars equipped with vehicles generally transmit FMCW signal. Mutual interference may arise from radars operating in the same frequency band. Fig. 1 renders the mutual interference between vehicles in the daily driving scenario, where the signal $\mathbf { T } _ { \cal { S } } ( t )$ from ego-vehicle can be expressed by the following equation:

$$
\mathbf { T } _ { S } ( t ) = A _ { t } e ^ { j ( 2 \pi f _ { c } t + \pi B t ^ { 2 } / T ) } , t \in ( 0 , T ) .\tag{1}
$$

Among them, $A _ { t }$ denotes the transmit amplitude, $f _ { c }$ is the carrier frequency, B is the signal bandwidth, and T represents

![](images/3f3ef2a50bf6f5ab65863276ff74ae02204379b5af7220821db28d701dcefe7d.jpg)  
Fig. 1. Mutual interference in the real driving scenario of FMCW autodrive radars.

the chirp duration. The radar echo $\mathbf { S } ( t )$ received by the antenna can be expressed as [43]

$$
\left\{ \begin{array} { l l } { \displaystyle \mathbf { S } ( t ) = \mathbf { R } _ { S } ( t ) + \sum _ { k = 1 } ^ { K } \mathbf { I } _ { k } ( t ) } \\ { \displaystyle \mathbf { R } _ { S } ( t ) = A _ { r } e ^ { j ( 2 \pi ( f _ { c } + f _ { d } ) ( t - \tau ) + \pi B ( t - \tau ) ^ { 2 } / T ) } } \\ { \displaystyle t \in ( \tau , T + \tau ) } \\ { \displaystyle \mathbf { I } _ { k } ( t ) = A _ { i k } e ^ { j ( 2 \pi f _ { c } ( t - \tau _ { i k } ) + \pi B _ { i k } ( t - \tau _ { i k } ) ^ { 2 } / T _ { i k } ) } } \\ { \displaystyle t \in ( \tau _ { i k } , T _ { i k } + \tau _ { i k } ) } \end{array} \right.\tag{2}
$$

where $\mathbf { I } _ { k } ( t )$ represents the interference signal and K refers to the number of interferences. $A _ { i k } , T _ { i k } , B _ { i k } .$ , and $\tau _ { i k }$ denote gain, chirp duration, chirp duration, and bandwidth of kth interference, respectively. Besides, ${ \bf R } _ { S } ( t )$ denotes the target returned signal, where $A _ { r }$ and $f _ { d }$ represent the received amplitude and Doppler shift, respectively. $\tau = 2 R _ { t } / c$ denotes time delay, with $R _ { t }$ being the range between its ego-vehicle and the target, and c being the speed of light.

## B. Interference and Target Signal Analysis

Ego-automotive radar adopts the orthogonal technique for conjugate mixer (also known as de-chirping) on $\mathbf { T } \mathbf { s } ( t )$ and S(t). Afterward, the low-pass filter (LPF) on the receiver removes some near-field spurious waves and high-frequency noise, as the above can be represented as follows:

$$
\begin{array} { l } { { \displaystyle { \bf S } _ { D } ( t ) = H _ { \mathrm { L P F } } ( H _ { \mathrm { m i x } } ( { \bf T } _ { S } ( t ) , { \bf S } ( t ) ) ) } } \\ { ~ = { \bf I } _ { F } ( t ) + \displaystyle \sum _ { k = 1 } ^ { K } { \hat { \bf I } _ { k } ( t ) } } \end{array}\tag{3}
$$

where $H _ { \mathrm { L P F } } ( \cdot )$ denotes LPF response function, $\mathbf { S } _ { D } ( t )$ stands for de-chirping signal, and $H _ { \mathrm { m i x } } ( \cdot , \cdot )$ refers to the mixer operation. In addition, $\hat { \mathbf { I } } _ { k } ( t )$ denotes the interference signals after de-chirping, and ${ \bf I } _ { F } ( t )$ denotes the target intermediate frequency (IF) signal.

Based on (1)–(3), the time-frequency illustration diagram of mutual interference between automotive radars is given in Fig. 2. It can be seen that $\mathbf { I } _ { F } ( t )$ with a fixed frequency only exists in the periods when $\mathbf { T } _ { \cal { S } } ( t )$ and $\mathbf { S } ( t )$ alternate, which is because the difference in frequency between the two is a constant after a time τ . Fig. 2(a) demonstrates that the LPF plays some role, however, if $\mathbf { I } _ { k } ( t )$ is in the scope of LFP, sharing the same period as the $\mathbf { T } _ { \cal { S } } ( t )$ and ${ \bf S } ( t ) , \hat { \bf I } _ { k } ( t )$ will appear in $\mathbf { S } _ { D } ( t ) . \ \mu _ { d i }$ as the slope of $\hat { \mathbf { I } } _ { k } ( t )$ can be expressed by the

following equation:

$$
\mu _ { d i } = { B } / { T } - \mu _ { i }\tag{4}
$$

where $\mu _ { i }$ denotes slope of $\mathbf { I } _ { k } ( t )$ . As shown in Fig. 2(b), both the target and the interference exhibit relatively sparse characteristics in the time-frequency analysis.

Next, we give the frequency-domain illustration diagram of $\mathbf { S } _ { \mathbf { D } } ( t )$ . As shown in Fig. 2(c), the target is relatively sparse in the frequency domain compared to the interference. From Fig. 2(d), ${ \bf I } _ { F } ( t )$ holds a fixed frequency, which we can interpret as a sinusoidal signal, therefore, the target is not sparse in the time domain. Conversely, the duration of $\hat { \mathbf { I } } _ { k } ( t )$ is extremely short relative to $\mathbf { I } _ { F } ( t )$ . Based on the above phenomenon, it can be concluded that the interference is emergent and only exists for a short period. Therefore, we can consider the interference to be sparse in the time domain.

## III. PROPOSED METHOD

In this section, we first apply MCA to characterize the de-chirping signal and then introduce the proposed BCD-DS in detail.

## A. Characteristic Representation

Since the interference caused by automotive radar is essentially unintentional additive interference, based on (3), we first characterize each independent component of ${ \bf S } _ { D } ( t )$

$$
\mathbf { S } _ { D } = \mathbf { S } _ { T } + \mathbf { S } _ { I }\tag{5}
$$

where $\mathbf { S } _ { D } ~ \in ~ \mathbb { C } ^ { N \times 1 } , ~ \mathbf { S } _ { \mathbf { T } } ~ \in ~ \mathbb { C } ^ { N \times 1 }$ , and $\mathbf { S _ { I } } ~ \in ~ \mathbb { C } ^ { N \times 1 }$ denote the time domain vector representation of ${ \bf S } _ { D } ( t ) , ~ { \bf I } _ { F } ( t )$ and $\hat { \mathbf { I } } _ { k } ( t )$ respectively, with the vector length being N . Based on the analysis of the sparse characteristics of the signals in Section II, our aim is to obtain the sparse coefficients of the interference or target in different transform domains, as shown in the following:

$$
\mathbf { S } _ { D } = \mathbf { A } _ { 1 } \mathbf { x } _ { 1 } + \mathbf { A } _ { 2 } \mathbf { x } _ { 2 }\tag{6}
$$

where $\mathbf { A } _ { 1 } \in \mathbb { C } ^ { N \times N }$ and $\mathbf { A } _ { 2 } \in \mathbb { C } ^ { N \times N }$ denote the measurement matrixes of the interference and target, respectively, with the length of N and the width of N . Moreover, $\mathbf { x } _ { 1 } \in \overset { \cdot } { \mathbb { C } } ^ { N \times 1 }$ and $\mathbf { x } _ { 2 } \in \mathbb { C } ^ { N \times 1 }$ denote the sparse coefficients corresponding to ${ \bf A } _ { 1 }$ and ${ \bf A } _ { 2 }$ , respectively. ${ \bf A } _ { 1 }$ and ${ \bf A } _ { 2 }$ can be represented as follows:

$$
A _ { 1 } = { \left[ \begin{array} { l } { 1 \ 0 \ \cdots \ 0 } \\ { 0 \ 1 \ \cdots \ 0 } \\ { \vdots \ \vdots \ \ddots \ \vdots } \\ { 0 \ 0 \ \cdots \ 1 } \end{array} \right] }\tag{7}
$$

$$
A _ { 2 } = \frac { 1 } { N } \left[ \begin{array} { c c c c } { 1 } & { 1 } & { \cdots } & { 1 } \\ { 1 } & { e ^ { \frac { j 2 \pi } { N } } } & { \cdots } & { e ^ { \frac { j ( L - 1 ) 2 \pi } { N } } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { 1 } & { e ^ { \frac { j ( L - 1 ) 2 \pi } { N } } } & { \cdots } & { e ^ { \frac { j ( L - 1 ) ( L - 1 ) 2 \pi } { N } } } \end{array} \right] .\tag{8}
$$

## B. Interference Suppression Scheme

At this point, the interference suppression task can be considered as the extraction of x<sub>2</sub> or the separation of $\mathbf { X } 1$ and $\mathbf { X } 2$ . However, (6) is an ill-conditioned problem with an infinite

number of solutions. To obtain the best solution, (6) can be modeled as the following multivariable optimization problem:

$$
\begin{array} { c } { ( \hat { \mathbf { x } } _ { 1 } , \hat { \mathbf { x } } _ { 2 } ) = \displaystyle \arg \underset { \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } } { \operatorname* { m i n } } \mathcal { L } ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } ) } \\ { \displaystyle \mathcal { L } ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } ) \triangleq \frac { 1 } { 2 } \| \mathbf { S } _ { D } - \mathbf { A } _ { 1 } \mathbf { x } _ { 1 } - \mathbf { A } _ { 2 } \mathbf { x } _ { 2 } \| _ { 2 } ^ { 2 } } \\ { + \lambda _ { 1 } \| \mathbf { x } _ { 1 } \| _ { 1 } + \lambda _ { 2 } \| \mathbf { x } _ { 2 } \| _ { 1 } } \end{array}\tag{9}
$$

where $\lVert \cdot \rVert _ { 2 }$ denotes Euclidean norm and $\lVert \cdot \rVert _ { 1 }$ is $\ell _ { 1 }$ norm showing the sparsity of vectors. $\lambda _ { i }$ controls the weights between penalty terms. The basic thought of the block coordinate descent method is to transform a multivariate optimization problem into an optimization problem with multiple univariate functions, so that each variable can be solved individually for optimization. Therefore, the block coordinate descent optimization framework is introduced to solve (9) by alternately estimating $\mathbf { X } 1$ and $\mathbf { X } 2 \cdot$ In one iteration, two simple single-variable optimization problems are included that bring down the overall gradients of the target and interference. The main steps of the block coordinates optimization framework are presented in Algorithm 1.

Algorithm 1 Block Coordinate Descent Optimization   
Require: De-chirping signal $\overline { { { \bf { S } } _ { D } ; } }$ System parameters $\overline { { \mathbf { P } ; } }$   
Ensure: Final estimation Interference sparsity coefficient $\hat { \mathbf { x } } _ { 1 } ;$   
Final estimation target sparsity coefficient $\hat { \bf x } _ { 2 } ;$   
1: while not converged do   
2: $\mathbf { x } _ { 1 } { } ^ { ( q ) } = \arg \operatorname* { m i n } _ { \mathbf { x } _ { 1 } } \mathcal { L } ( \mathbf { x } _ { 1 } , \mathbf { x } _ { 2 } ^ { ( q - 1 ) } )$   
3: $\begin{array} { r } { { \bf x } _ { 2 } ^ { ( q ) } = \arg \operatorname* { m i n } _ { { \bf x } _ { 2 } } \mathcal { L } ( { \bf x } _ { 1 } ^ { ( q ) } , { \bf x } _ { 2 } ) ; } \end{array}$   
4: end while

In the following, the solutions to the two problems of Algorithm 1 are given. Equation (9) holds bivariate variables and to obtain the results, we arrive at $\mathbf { X } 1$ and $\mathbf { X } _ { 2 }$ successively during one iteration. To solve for the first phase of the current iteration cycle in Algorithm 1, the following objective function can be constructed first:

$$
\left\{ \begin{array} { l l } { \hat { \mathbf { x } } _ { 1 } = \arg \operatorname* { m i n } _ { \mathbf { x } _ { 1 } } \frac { 1 } { 2 } \| \mathbf { S } _ { D 1 } - \mathbf { A } _ { 1 } \mathbf { x } _ { 1 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| \mathbf { x } _ { 1 } \| _ { 1 } } \\ { \mathbf { S } _ { D 1 } = \mathbf { S } _ { D 2 } - \mathbf { A } _ { 2 } \mathbf { x } _ { 2 } . } \end{array} \right.\tag{10}
$$

Under the theory of ADMM [44], a new auxiliary variable $\mathbf { z } _ { 1 } \in \mathbb { C } ^ { N \times 1 }$ is introduced in (10) to facilitate the separation of the penalty terms

$$
\hat { \mathbf { x } } _ { 1 } = \mathop { \arg \operatorname* { m i n } } _ { \mathbf { x } _ { 1 } } \frac { 1 } { 2 } \ : \| \mathbf { S } _ { D 1 } - \mathbf { A } _ { 1 } \mathbf { x } _ { 1 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| \mathbf { z } _ { 1 } \| _ { 1 }\tag{11}
$$

Furthermore, the augmented Lagrangian function for (11) can be written

$$
\begin{array} { l } { { \displaystyle \mathbb { L } _ { \theta _ { 1 } } \left( { \bf x } _ { 1 } , { \bf z } _ { 1 } , { \bf u } _ { 1 } \right) = \frac { 1 } { 2 } \left\| { \bf S } _ { \bf D 1 } - { \bf A } _ { 1 } { \bf x } _ { 1 } \right\| _ { 2 } ^ { 2 } + \lambda _ { 1 } \left\| { \bf z } _ { 1 } \right\| _ { 1 } } } \\ { { \displaystyle ~ + { \bf u } _ { 1 } ^ { H } \left( { \bf x } _ { 1 } - { \bf z } _ { 1 } \right) + \frac { \theta _ { 1 } } { 2 } \left\| { \bf x } _ { 1 } - { \bf z } _ { 1 } \right\| _ { 2 } ^ { 2 } } } \end{array}\tag{12}
$$

here, we define $\mathbf { u } _ { 1 } ^ { H }$ as the conjugate transpose of the vector $\mathbf { u } _ { 1 }$ Besides, $\mathbf { u } _ { 1 } \in \mathbb { C } ^ { \dot { N } \times 1 }$ denotes Lagrangian multiplier and $\theta _ { 1 } \in$

<sup>R</sup> represent penalty parameter. After separating the variables, (12) can be converted into solving the following problem:

$$
\left\{ \begin{array} { l l } { \mathbf { x } _ { 1 } ^ { ( q ) } = \underset { \mathbf { x } _ { 1 } } { \arg \operatorname* { m i n } } \mathbb { L } _ { \boldsymbol { \theta } _ { 1 } } \left( \mathbf { x } _ { 1 } , \mathbf { z } _ { 1 } ^ { ( q - 1 ) } , \mathbf { u } _ { 1 } ^ { ( q - 1 ) } \right) } \\ { \mathbf { z } _ { 1 } ^ { ( q ) } = \underset { \mathbf { z } _ { 1 } } { \arg \operatorname* { m i n } } \mathbb { L } _ { \boldsymbol { \theta } _ { 1 } } \left( \mathbf { x } _ { 1 } ^ { ( q ) } , \mathbf { z } _ { 1 } , \mathbf { u } _ { 1 } ^ { ( q - 1 ) } \right) } \\ { \mathbf { u } _ { 1 } ^ { ( q ) } = \mathbf { u } _ { 1 } ^ { ( q - 1 ) } + \boldsymbol { \theta } _ { 1 } \left( \mathbf { x } _ { 1 } ^ { ( q ) } - \mathbf { z } _ { 1 } ^ { ( q ) } \right) } \end{array} \right.\tag{13}
$$

where $q$ denotes the iteration index. The closed-form solutions of sub-problems in (13) can be expressed as the following:

$$
\left\{ \begin{array} { l } { { \displaystyle { \bf x } _ { 1 } ^ { ( q ) } = \left( { \bf A } _ { 1 } ^ { H } { \bf A } _ { 1 } + \theta _ { 1 } { \bf I } _ { N } \right) ^ { - 1 } } } \\ { ~ \left( { \bf A } _ { 1 } ^ { H } { \bf S } _ { D 1 } + \theta _ { 1 } { \bf z } _ { 1 } ^ { ( q - 1 ) } - { \bf u } _ { 1 } ^ { ( q - 1 ) } \right) } \\ { { \displaystyle { \bf z } _ { 1 } ^ { ( q ) } = { \cal S } \left( { \bf x } _ { 1 } ^ { ( q ) } + \frac { { \bf u } _ { 1 } ^ { ( q - 1 ) } } { \theta _ { 1 } } ; \frac { \lambda _ { 1 } } { \theta _ { 1 } } \right) } } \\ { { \displaystyle { \bf u } _ { 1 } ^ { ( q ) } = { \bf u } _ { 1 } ^ { ( q - 1 ) } + \theta _ { 1 } \left( { \bf x } _ { 1 } ^ { ( q ) } - { \bf z } _ { 1 } ^ { ( q ) } \right) } } \end{array} \right.\tag{14}
$$

where ${ \bf I } _ { N } \in \mathbb { R } ^ { N \times N }$ represents the identity matrix, and $\mathcal { S } \left( \mathbf { f } ; g \right)$ denotes the augmented soft threshold function, specified as follows:

$$
\left[ S \left( \mathbf { g } ; f \right) \right] _ { k } = \frac { \mathbf { g } _ { k } } { \left| \mathbf { g } _ { k } \right| } \operatorname* { m a x } \left( \left| \mathbf { g } _ { k } \right| - f ; 0 \right) , k = 1 , 2 , \ldots , L .\tag{15}
$$

Among them, g<sub>k</sub> and $L$ denote the kth value of the vector g and the length of ${ \bf g } ,$ respectively. Besides, |g<sub>k</sub>| is the amplitude of $\mathbf { g } _ { k }$ , and $[ \cdot ] _ { k }$ indicates the operator of extracting the $k$ element.

After arriving at $\mathbf { x } _ { 1 } ^ { ( q ) }$ during this iteration, we continue to solve for second phase by bringing $\mathbf { x } _ { 1 } ^ { ( q ) }$ into the following objective function:

$$
\left\{ \begin{array} { l l } { \hat { \mathbf { x } } _ { 2 } = \arg \operatorname* { m i n } _ { \mathbf { x } _ { 2 } } \frac { 1 } { 2 } \| \mathbf { S _ { D 2 } } - \mathbf { A } _ { 2 } \mathbf { x } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 2 } \| \mathbf { x } _ { 2 } \| _ { 1 } } \\ { \mathbf { S } _ { D } = \mathbf { S } _ { D } - \mathbf { A } _ { 1 } \mathbf { x } _ { 1 } ^ { ( q ) } . } \end{array} \right.\tag{16}
$$

Similarly, we introduce the auxiliary variable $\mathbf { z } _ { 2 } ~ \in ~ \mathbb { C } ^ { N \times 1 }$ to separate the penalty terms

$$
\begin{array} { l } { { \displaystyle { \mathbb { L } } _ { \theta _ { 2 } } ( { \bf x } _ { 2 } , { \bf z } _ { 2 } , { \bf u } _ { 2 } ) = \frac { 1 } { 2 } \| { \bf S } _ { D 2 } - { \bf A } _ { 2 } { \bf x } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 2 } \| { \bf z } _ { 2 } \| _ { 1 } } } \\ { { \displaystyle ~ + { \bf u } _ { 2 } ^ { H } ( { \bf x } _ { 2 } - { \bf z } _ { 2 } ) + \frac { \theta _ { 2 } } { 2 } \| { \bf x } _ { 2 } - { \bf z } _ { 2 } \| _ { 2 } ^ { 2 } . } } \end{array}\tag{17}
$$

According to (12) and (13), we can obtain the final solution of (17)

$$
\left\{ \begin{array} { l } { \mathbf { x } _ { 2 } ^ { ( q ) } = \left( \mathbf { A } _ { 2 } ^ { { \cal H } } \mathbf { A } _ { 2 } + \theta _ { 2 } \mathbf { I } _ { N } \right) ^ { - 1 } } \\ { \quad \quad \left( \mathbf { A } _ { 2 } ^ { { \cal H } } \mathbf { S } _ { D 2 } + \theta _ { 2 } \mathbf { z } _ { 2 } ^ { ( q - 1 ) } - \mathbf { u } _ { 2 } ^ { ( q - 1 ) } \right) } \\ { \mathbf { z } _ { 2 } ^ { ( q ) } = \mathcal { S } \left( \mathbf { x } _ { 2 } ^ { ( q ) } + \displaystyle \frac { \mathbf { u } _ { 2 } ^ { ( q - 1 ) } } { \theta _ { 2 } } ; \displaystyle \frac { \lambda _ { 2 } } { \theta _ { 2 } } \right) } \\ { \mathbf { u } _ { 2 } ^ { ( q ) } = \mathbf { u } _ { 2 } ^ { ( q - 1 ) } + \theta _ { 2 } \left( \mathbf { x } _ { 2 } ^ { ( q ) } - \mathbf { z } _ { 2 } ^ { ( q ) } \right) . } \end{array} \right.\tag{18}
$$

According to the analysis above, we exploit the sparsity of the interference and the target in the time and frequency domains, respectively. It follows that ${ \bf A } _ { 1 }$ is the identity matrix and ${ \bf A } _ { 2 }$ is the Fourier matrix, which are both tight transforms.

Algorithm 2 BCD-DS for Interference Mitigation   
Require: De-chirping signal ${ \bf s } _ { D } ;$ Interference measurement   
matrix ${ \bf A } _ { 1 }$ with regularization parameters $\theta _ { 1 }$ and $\lambda _ { 1 } ;$ ; Target   
measurement matrix ${ \bf A } _ { 2 }$ with regularization parameters   
$\theta _ { 2 }$ and $\lambda _ { 2 } ;$ Iteration $T ;$ Error value $\eta ;$   
Ensure: Final estimation Interference sparsity coefficient $\hat { \mathbf { x } } _ { 1 } ;$   
Final estimation target sparsity coefficient $\hat { \bf x } _ { 2 } ;$   
1: Initialize $\mathbf { x } _ { 2 } ^ { ( 0 ) } = \mathbf { z } _ { 1 } ^ { ( 0 ) } = \mathbf { \check { u } } _ { 1 } ^ { ( 0 ) } = \mathbf { \check { z } } _ { 2 } ^ { ( 0 ) } = \mathbf { u } _ { 2 } ^ { ( 0 ) } = \mathbf { \check { 0 } } ;$   
2: while $q \leq \bar { T }$ do   
3: $\begin{array} { r } { \mathbf { S } _ { D 1 } ^ { ( q ) } = \mathbf { S } _ { D } - \mathbf { A } _ { 2 } \mathbf { x } _ { 2 } ^ { ( q - 1 ) } \mathbf { ; } } \end{array}$   
4: $\begin{array} { r } { \mathbf { x } _ { 1 } ^ { ( q ) } = \frac { \left( \mathbf { A } _ { 1 } ^ { H } \mathbf { S } _ { D 1 } ^ { ( q ) } + \theta _ { 1 } \mathbf { \overline { { z } } } _ { 1 } ^ { ( q - 1 ) } - \mathbf { u } _ { 1 } ^ { ( q - 1 ) } \right) } { \theta _ { 1 } + 1 } ; } \end{array}$   
5: $\begin{array} { r } { \mathbf { z } _ { 1 } ^ { ( q ) } = \mathcal { S } \left( \mathbf { x } _ { 1 } ^ { ( q ) } + \frac { \mathbf { \dot { u } } _ { 1 } ^ { ( q - 1 ) } } { \theta _ { 1 } } ; \frac { \lambda _ { 1 } } { \theta _ { 1 } } \right) ; } \end{array}$   
6: $\mathbf { u } _ { 1 } ^ { ( q ) } = \mathbf { u } _ { 1 } ^ { ( q - 1 ) } + \theta _ { 1 } \left( \mathbf { x } _ { 1 } ^ { ( q ) } - \mathbf { \bar { z } } _ { 1 } ^ { ( q ) } \right) ;$   
7: $\mathbf { S } _ { D 2 } ^ { ( q ) } = \mathbf { S } _ { D } - \mathbf { A } _ { 1 } \mathbf { x } _ { 1 } ^ { ( q ) } ;$   
8: $\begin{array} { r } { \mathbf { x } _ { 2 } ^ { ( q ) } = \frac { \left( \mathbf { A } _ { 2 } ^ { H } \mathbf { S } _ { D 2 } ^ { ( q ) } + \theta _ { 2 } \mathbf { z } _ { 2 } ^ { ( q - 1 ) } - \mathbf { u } _ { 2 } ^ { ( q - 1 ) } \right) } { \theta _ { 2 } + 1 } } \end{array}$   
$\overline { { \theta _ { 2 } + 1 } }$   
9: $\begin{array} { r } { I _ { e } = \frac { \left\| \mathbf { x } _ { 2 } ^ { ( q ) } - \mathbf { x } _ { 2 } ^ { ( q - 1 ) } \right\| _ { 2 } ^ { 2 } } { \left\| \mathbf { x } _ { 2 } ^ { ( q - 1 ) } \right\| _ { 1 } ^ { 2 } . 6 2 } } \end{array}$   
10: if $I _ { e } { < } \eta$ then   
11: $\begin{array} { r } { \mathbf { x } _ { 2 } ^ { ( q - 1 ) } = \mathbf { x } _ { 2 } ^ { ( q ) } ; } \end{array}$   
12: else   
13: $\mathbf { x } _ { 2 } ^ { * } = \mathbf { x } _ { 2 } ^ { ( q ) }$ , break;   
14: end if   
15: $\begin{array} { r } { \mathbf { z } _ { 2 } ^ { ( q ) } = \mathcal { S } \left( \mathbf { x } _ { 2 } ^ { ( q ) } + \frac { \mathbf { u } _ { 2 } ^ { ( q - 1 ) } } { \theta _ { 2 } } ; \frac { \lambda _ { 2 } } { \theta _ { 2 } } \right) } \end{array}$   
16: ${ \bf u } _ { 2 } ^ { ( q ) } = { \bf u } _ { 2 } ^ { ( \bar { q } - 1 ) } + \theta _ { 2 } \left( { \bf x } _ { 2 } ^ { ( q ) } - \bf { \bar { z } } _ { 2 } ^ { ( q ) } \right) ;$   
17: $q = q + 1 ;$   
18: end while

To avoid complex matrix inversion operations [45], the estimations of $\mathbf { X } 1$ and $\mathbf { X } _ { 2 }$ can be simplified as follows:

$$
\begin{array} { r } { \mathbf { x } _ { 1 } ^ { ( q ) } = \frac { \left( \mathbf { A } _ { 1 } { } ^ { H } \mathbf { S } _ { D 1 } + \theta _ { 1 } \mathbf { z } _ { 1 } ^ { ( q - 1 ) } - \mathbf { u } _ { 1 } ^ { ( q - 1 ) } \right) } { \theta _ { 1 } + 1 } } \\ { \mathbf { x } _ { 2 } ^ { ( q ) } = \frac { \left( \mathbf { A } _ { 2 } { } ^ { H } \mathbf { S } _ { D 2 } + \theta _ { 2 } \mathbf { z } _ { 2 } ^ { ( q - 1 ) } - \mathbf { u } _ { 2 } ^ { ( q - 1 ) } \right) } { \theta _ { 2 } + 1 } } \end{array}\tag{19}
$$

Combining (14), (18), and (19), the BCD-DS algorithm can be reached, as summarized in Algorithm 2, where $I _ { e }$ denotes iteration error.

## C. Computational Load

We calculate the complexity of the proposed method, given $\begin{array} { r } { \begin{array} { r c l c r c l } { \mathbf { S } _ { D 1 } } & { \in } & { \mathbb { C } ^ { N \times 1 } , \ \mathbf { S } _ { D 2 } } & { \in } & { \mathbb { C } ^ { N \times 1 } , \ \mathbf { x } _ { 1 } } & { \in } & { \hat { \mathbb { C } } ^ { N \times 1 } , \ \mathbf { x } _ { 2 } } & { \in } & { \bar { \mathbb { C } } ^ { N \times 1 } } \end{array} } \end{array}$ $\begin{array}{c} \begin{array} { r l r } { \bar { \bf A } _ { 1 } } & { { } \in \mathrm { ~ \mathbb { C } ^ { N \times N } , ~ } \bar { \bf A } _ { 2 } } & { \in \mathrm { ~ \mathbb { C } ^ { N \times N } , ~ } \bar { \bf z } _ { 1 } } \end{array} \in \mathrm { ~ \mathbb { C } ^ { N \times N } , ~ } \mathrm { ~ \mathbb { Z } ^ { \bar { ~ } \bar { \bf ~ \chi } } _ 2 ~ } \in \mathrm { ~ \mathbb { C } ^ { N \times 1 } , ~ } \mathrm { ~ \mathbb { Z } ^ { \bar { ~ } \bar { \bf ~ \chi } } _ 2 ~ } \in \mathrm { ~ \mathbb { C } ^ { N \times 1 } ~ }  \end{array}$ $\mathbf { u } _ { 1 } \in \mathbb { C } ^ { N \times 1 }$ , and ${ \mathbf { u } } _ { 2 } \in \mathbb { C } ^ { N \times 1 }$ . Recalling the iterative process of (14), (18), and (19), the arithmetic operations for the first phase of updating $\mathbf { S } _ { D 1 } , \mathbf { x } _ { 1 } , \mathbf { z } _ { 1 }$ , and $\mathbf { u } _ { 1 }$ can be summarized as follows:

$$
\begin{array} { l } { \mathrm { c o m p l e x ~ m u l t i p l i c a t i o n s : } 2 N ^ { 2 } + 5 N } \\ { \mathrm { c o m p l e x ~ a d d i t i o n s : } 2 N ^ { 2 } + 4 N . } \end{array}\tag{20}
$$

According to (20), the complexity of BCD-DS is $O \left( N ^ { 2 } \right)$ Incidentally, we calculate the complexity of the comparison methods in the experiments below. The single Fourier method (SFM) is the second stage of the BCD-DS using only the Fourier transform. Since the arithmetic operations in the second phase are the same as in the first phase, the complexity of SFM is also $O \left( N ^ { 2 } \right)$ . Based on the minimum mean square error, the ANC method proposed in [25] optimizes each sample point on the chirp with complexity O (N ). Besides, Uysal [40] is based on the SALSA adopting STFT and Fourier transform, similarly with complexity $O \left( N ^ { 2 } \right)$ . Furthermore, for the compressed sensing-based methods, low-rank solving (LRS) methods [37] and Bi-L1 optimization (BLO) methods [38], have the same complexity $\bar { O } \left( N ^ { 2 } \right)$ . Therefore, in terms of computational load, BCD-DS and comparison methods are approximate in magnitude.

![](images/3e6a180d70b216931b149331540d51288f685a4c7035115483087616b996a959.jpg)

![](images/c41947ae2f13a0b5380fa1582fd6dad67e81ef55fae6ce205df0c2d5f68a29a0.jpg)  
Fig. 2. Time-frequency illustration diagram of mutual interference between automotive radars. (a) and (b) Time-frequency illustration diagrams of S(t) and ${ \cal { S } } _ { D } ( t ) ,$ respectively. (c) Frequency-domain illustration diagram of ${ \mathrm { \dot { \cal { S } } } } _ { D } ( t ) .$ (d) Time illustration diagram of ${ \mathit { S } } _ { D } ( t ) .$ Besides, the yellow dashed line shows the cutoff frequency of the LPF.

TABLE I  
PARAMETERS IN THE SIMULATION EXPERIMENT
<table><tr><td>Parameters</td><td>Ego-Vehicle</td><td>AV#1</td><td>AV#2</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(GHz)</td><td>0.3</td><td>0.3</td><td>0.3</td></tr><tr><td>Chirp Duration(µs)</td><td>30.6</td><td>6.1</td><td>10.2</td></tr><tr><td>Slope of chirp(MHz/µs)</td><td> $9 . 8 0 \times 1 0 ^ { 1 2 }$ </td><td> $4 . 9 0 \times 1 0 ^ { 1 3 }$ </td><td> $2 . 9 4 \times 1 0 ^ { 1 3 }$ </td></tr><tr><td>Position(m)</td><td> $[ 0 , 0 ]$ </td><td> $\left[ 5 , 7 . 4 8 \right]$ </td><td>[2.64, 3]</td></tr></table>

## IV. EXPERIMENTS

In this section, we will describe the details of the experimental implementation. A platform with a 3.20-GHz Intel i7-8700 processor and an NVIDIA Quadro RTX6000 (24-GB memory) is available for the entire experiment. First, the quantitative evaluation indicator will be given. Second, simulation and measured experiments will be performed, to verify the effectiveness of our method in comparison to the state-of-theart algorithms.

## A. Evaluation Indicator

To evaluate the interference suppression effectiveness of each method, we select the signal-to-interference and noise ratio (SINR) [46] to estimate the energy intensity of the target.

![](images/43aa05714890ed20c7452f1f480169ec6cc1a2f33ae11d5375dac93a07b52fe3.jpg)  
(a)

![](images/a88fb89bbc54e46f8e9ce478435af459c8b0e95c21e2b3a72a0b461beeb19e75.jpg)  
(b)

![](images/156ee52171b996c1fc4974fec6fb2e587d49188cd9f08299253ef23e189e5478.jpg)  
(c)

Fig. 3. Performance of the proposed method under different iterations (SINRo=10 dB). (a) $\mathsf { S l N R } _ { t } .$ (b) I<sub>e</sub>. (c) Running time.  
![](images/eca2037325aa3af88b6ea8f49c0bc7cb4990660be61e28f5071b291674180b58.jpg)

![](images/1256ddca9488d7631f1a44e59d0b7493bc9f5362043c6508e432af072c86295a.jpg)

![](images/1660dea5344f14a543c4c8a919a952c574c51f907b86f8bdaba5c3380d53b321.jpg)  
(a)

![](images/ec89a1f8c6aeb8d973702c095ef0bb8995b535a5bcc0ffe61387990ec8deae96.jpg)

![](images/5c648ba1c5749d0b9cef26f0aa85abfd39dd0ef8a2717052017dc4563c99cc3b.jpg)

(b)  
![](images/a6050db9c61f33af932a855d4c499f419a938752c6aa2a052b804a218d3dd1d5.jpg)

![](images/9125c51ee1d84c4e82e18b43b4e8f054d8fe708aef3be1f1f497a48a0befd265.jpg)

(c)  
![](images/fd9237e09177fea8fa7a2a8b5fb60b2a6d3a875c571455ac6851a120676728bb.jpg)

![](images/6c6ab9531ec4ddc89a2196efcb01df10915edf493ea1dbdbe954e32d47b1d58f.jpg)

![](images/d60e43698beda77733ea7331241407845fe1d2f05bceb0539e22d30e11f425dd.jpg)  
(e)

(d)  
![](images/3c65ad47da13fc1018109ba36012ff8830372cbda30a8ed8a1be66e5eef1ffcc.jpg)

![](images/0dd27c85393e8b931f3a7a2734cfd2e58a71566708641014c0141e56b66f6b30.jpg)  
(f)  
Fig. 4. Results of each method in the simulation experiments $( \mathsf { S } \mathsf { I N R } _ { o } = 1 0 \mathsf { d } \mathsf { B } )$ . (a) Without interference, (b) with interference, (c) ANC, (d) SFM, (e) Uysa, and (f) BCD-DS. In addition, the first row of each subplot is the time-domain result, and the second row is the RA result. Besides, ${ \sf T } _ { 1 }$ and ${ \sf T } _ { 2 } ,$ , denote Target#1 and Target#2, respectively.Authorized licensed use limited to: Beijing Jiaotong University. Downloaded on June 22,2026 at 07:10:13 UTC from IEEE Xplore. Restrictions apply.

![](images/d87f9806268ab143310183072b550ffa09f5b2d77f04b3b2a5b652efc5235c02.jpg)  
(a)

![](images/e7b0fc6f1b6b0742f9725287ffa26d42241cd7e0267a0c9f45f16f98d6dc3378.jpg)

![](images/a8f8ec9cfaaa4361c6d8197cc7f86c2de7a143c948b15780131ae5b5035435b8.jpg)

![](images/4bafbdb4db660e1602893136a5d26cabb420094242f551b218c3a90cb34cf353.jpg)  
(d)

(b)  
![](images/f3f9f480834494ac58187ebe6a35ed1ae92cc7fc5e976c2bf5869c0229184099.jpg)  
(e)

(c)  
![](images/c00da448ea0c7783378a17483692ac0b903acc0093c472a58fac632d80f5c582.jpg)  
(f)  
Fig. 5. RD results for simulation data $( \mathsf { S } \mathsf { I N R } _ { o } = \mathsf { I } 0 \mathsf { d } \mathsf { B } )$ . (a) Without interference, (b) with interference, (c) ANC, (d) SFM, (e) Uysal, and (f) BCD-DS.

SINR can be expressed by the following equation:

$$
\mathrm { S I N R } _ { \mathrm { t } } = \mathrm { l g } \left( { \frac { \mathrm { P T } _ { \mathrm { i } } } { \mathrm { P I } + \mathrm { P N } } } \right)\tag{21}
$$

where $\mathrm { S I N R } _ { \mathrm { t } }$ and PT denote the SINR value of the corresponding target and the effective power, respectively. Besides, PI and PN indicate the effective power of interference and noise. A higher SINR<sub>t</sub> value reflects better interference suppression performance.

The interference suppression ratio (ISR), which reflects intuitively the ability of the algorithm to suppress strong interference [47], formulated as follows:

$$
\mathrm { I S R } = 1 0 1 \mathrm { g } ( \frac { \Vert \mathbf { E _ { i } } \Vert _ { \mathrm { F } } ^ { 2 } } { \Vert \mathbf { E _ { s } } \Vert _ { \mathrm { F } } ^ { 2 } } )\tag{22}
$$

where $\| \cdot \| _ { F } ^ { 2 }$ denotes the Frobenius norm. Besides, $\mathbf { E } _ { i }$ and E refer to the echo with interference and the echo after interference suppression, respectively. Typically, a higher ISR indicates better interference suppression.

## B. Simulation Experiments

In this simulation experiment, we set up two targets (Target#1 and Target#2), one of which is stationary at a distance of 30 m from the ego-vehicle and one at a distance of 15 m from the ego-vehicle with a speed of 10 m/s. In addition, two other AVs were set up to affect the ego-vehicle, where AV#1 and AV#2 represent the first AV and the second AV, respectively, 9 and 4 m from the ego-vehicle. The setting of experimental parameters is given in Table I.

For closer alignment with practical applications, we add Gaussian white noise to the entire system. Moreover, to verify the effect of interference strength on the performance of different methods, we divided the overall SINR (SINR ) of the echo into four cases, −5, 0, 5, and 10 dB, respectively.

![](images/7ed9c1020c9d4b76bfafc920785ba66b19f18577e25cc7e04a8c13e353c43adc.jpg)

(a)  
![](images/c426948a3005c65f9aed21e61e4cf65d6557ffc171428d308faf046246134f3f.jpg)

(b)  
![](images/29e284d396745c99f371df5e177826c1c249ed5c623c7ddf9cdbd2a73f81dab5.jpg)  
(c)  
Fig. 6. Speed profile at Target#1. (a) Without interference, (b) with interference, and (c) interference suppression by BCD-DS.

1) Convergence Analysis: To analyze the convergence of the proposed method, $\mathrm { S I N R } _ { \mathrm { t } } , \ I _ { e }$ from Algorithm 2, and the running time are adopted as the criteria, in case of the different iterations. The analysis results are shown in Fig. 3 with $\mathrm { S I N R } _ { o }$ of 10 dB. For Fig. 3(a), SINR<sub>t</sub> of Targets 1 and 2 stabilize at iterations greater than 30. For Fig. 3(b), i.e., stabilizes at iterations greater than 30. For Fig. 3(c), runtime and iteration are positively correlated. In summary, in this experiment, BCD-DS converges at iterations greater than 30, and to improve the efficiency of the method, the number of iterations can be set to 30, which requires only 0.1331 s of running time.

TABLE II  
NUMERICAL COMPARISONS IN SIMULATION EXPERIMENT WITH DIFFERENT OVERALL SINRS, USING ISR AND SINRS FOR DIFFERENT TARGETS
<table><tr><td rowspan="2">Methods</td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } { - } 5 \mathrm { d B }$ </td><td rowspan="2"></td><td colspan="3"> $\mathrm { S I N R } _ { o } { = } 0 \mathrm { d B }$ </td><td rowspan="2"></td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } 5 \mathrm { d B }$ </td><td rowspan="2"> $\mathrm { S I N R } _ { o } { = } 1 0 \mathrm { d } \mathrm { B }$ </td><td colspan="2"></td><td rowspan="2">Time(s)</td></tr><tr><td>SINRt(dB)</td><td>-ISR(dB)</td><td>SINRt(dB)</td><td></td><td></td><td> $\mathrm { S I N R } _ { t } ( \mathrm { d B } )$ </td><td> $\mathrm { S I N R } _ { t } ( \mathrm { d B } )$ </td><td></td></tr><tr><td></td><td>Target#1</td><td>Target#2</td><td></td><td>Target#1</td><td>Target#2</td><td>ISR(dB)</td><td>Target#1</td><td>Target#2</td><td>ISR(dB)</td><td>Target#1</td><td>Target#2</td><td>- ISR(dB)</td><td></td></tr><tr><td>ANC</td><td>-1.14</td><td>-3.45</td><td>3.04</td><td>2.35</td><td>0.91</td><td>4.27</td><td>8.74</td><td>6.53</td><td>0.76</td><td>16.16</td><td>12.67</td><td>0.76</td><td>0.0235</td></tr><tr><td>SFM</td><td>31.43</td><td>28.77</td><td>3.38</td><td>38.34</td><td>30.07</td><td>3.23</td><td>41.64</td><td>34.12</td><td>3.18</td><td>45.79</td><td>36.53</td><td>3.07</td><td>0.0782</td></tr><tr><td>Uysal</td><td>39.34</td><td>32.81</td><td>3.54</td><td>43.85</td><td>38.49</td><td>3.49</td><td>48.65</td><td>42.09</td><td>3.14</td><td>51.97</td><td>45.14</td><td>3.05</td><td>0.3186</td></tr><tr><td>BCD-DS</td><td>52.14</td><td>45.43</td><td>5.12</td><td>53.01</td><td>45.91</td><td>5.24</td><td>54.03</td><td>48.78</td><td>4.78</td><td>58.09</td><td>51.31</td><td>4.51</td><td>0.1337</td></tr></table>

2) Simulation Results: Fig. 4 gives the results in the case of SINR at 10 dB, where Fig. 4(a) is without interference, Fig. 4(b) is with interference, Fig. 4(c) is ANC, Fig. 4(d) indicates SFM, Fig. 4(e) is Uysal, and Fig. 4(f) denotes BCD-DS. As we can observe that without interference the target amplitude at 15 m and at 30 m is close to 40 dB and the system noise amplitude fluctuates at −20 dB. The interference generated by AV#1 and AV#2 is bursty in the time domain and is also clearly characterized in the time-frequency plot. From the range-amplitude (RA) results of Fig. 4(a) and (b), the interference raises the noise to a level of 20 dB which seems to drown out the target. ANC takes the positive frequency target in the beat frequency signal as the primary channel and using the distribution of interference at negative frequencies does suppress some interference, where both the RA results. However, the time domain results show that the noise is still more pronounced. This is due to the limitations of the ANC principle, which can only filter interference and noise around the target in the positive frequency. SFM obtains the target sparse coefficients directly from only the frequency domain and performs significantly better than ANC, with the target waveform in the time domain being able to be restored, but with a few interference features left behind at some points in time domain. The RA results from Uysal suppress the noise to a level of −14 dB. Uysal is based on STFT and Fourier Transform using SALSA to solve for the target. However, according to the analysis above, the interference does not present significant sparsity in the time-frequency domain. Therefore, Uysal is more sensitive to the parameters when dealing with each chirp. Unlike SFM, which solves for targets from a single domain, BCD-DS solves for interference and targets simultaneously in the time and frequency domains. BCD-DS completely filters out the noise in the time domain. From RA results of BCD-DS, both two target amplitudes are close to the without interference, and the noise amplitude drops to about −20 dB.

Next, we will show the range-Doppler (RD) results of each method in the simulation experiments, which are obtained after the same iterations by performing matched filtering and Fourier transform processing on 128 chirps. The length of each chirp is 1224. In addition, for practical purposes, results should be obtained in such a way that each method takes the same set of parameters for each chirp. As shown in Fig. 5, the RD results of ANC demonstrate some reduction in the noise power around the two targets. For SFM and Uysal, there is a lot of noise remaining in the RD maps. In the RD results of BCD-DS, both moving and stationary targets are well presented.

![](images/822a9af8e4cab7d68e96fc1a758de48be4047510903b40ae8c2a06645e472bac.jpg)  
Fig. 7. Scene setting for the measured experiment.

TABLE III  
MEASURED EXPERIMENT PARAMETERS
<table><tr><td>Parameters</td><td>Ego-Radar</td><td>AR#1</td><td>AR#2</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(GHz)</td><td>0.823</td><td>0.75</td><td>0.91</td></tr><tr><td>Chirp Duration(µs)</td><td>54.46</td><td>41.52</td><td>10.2</td></tr><tr><td>Slope of chirp(MHz/µs)</td><td> $1 5 . 0 6 \times 1 0 ^ { 1 2 }$ </td><td> $1 8 . 0 6 \times 1 0 ^ { 1 2 }$ </td><td> $3 5 . 9 1 \times 1 0 ^ { 1 2 }$ </td></tr><tr><td>Range(m)</td><td>0</td><td>14</td><td>5</td></tr></table>

Next, we select the speed profile at Target#1 to analyze the effect of the interference on the speed and the performance of the proposed method. The corresponding analysis results are given in Fig. 6, from which it can be seen that the interference produces an incorrect speed for Target#1. After processing each chirp, BCD-DS can obtain the correct speed.

Table II gives the numerical comparisons at different $\operatorname { S I N R } _ { o } .$ Due to the limitations of the method, ANC is only valid if the $\mathrm { S I N R } _ { o }$ is above 0 dB. Compared to SFM and Uysal, for Target#1 and Target#2, BCD-DS achieves the highest SINR<sub>t</sub> , indicating a strong acquisition capability for the target. In addition, the BCD-DS also obtains the highest ISR values, with the dual-domain cooperative estimation causing a significant attenuation of the power from interference and noise. In terms of running time, ANC is the fastest but not very effective. Our method is faster than Uysal and takes only 0.1337 s on average to achieve the best interference suppression.

![](images/319014c33937b36bc6159a1c714ef0add2e290c38362631d939fc67dad31ecc4.jpg)

![](images/659f4deb1a3c3083cb9a984f54f149191117a75ddd11161aff014a92ad80fff1.jpg)  
(a)

![](images/3d5e9625c35e5436503c2c2087d5982bf52837ef1ee5525ec7d0d487c426b877.jpg)

![](images/85fb3f10ea62b335c0f6f15c38f36f9f8ab34add7dc2fcd0072ac7b9fb69ccf9.jpg)

![](images/cdaaf4042f50694dfb92d28d9921e51964ac52a35701392435e3c336061a5c23.jpg)

![](images/9b5626e58ab77030162b6e411c95d88c94a53389cdaa6013e5b8711f8a568701.jpg)

![](images/76f6c257ceef7570347fae89e84788b2f5bea8a1bf076ea3ed056a81f700c387.jpg)  
(c)

![](images/a0418a95fdd53c93506e805ce2e6e51102745197bc79acce1287712c4fe43182.jpg)

![](images/a4a09a2ed84f3200aeacf33e366c8ef88e10ae048e3779979e42b09841b7230d.jpg)

(d)  
![](images/a8bdd33fdb3c2e346e66d2d8712e968766ffbf087d090019b0642332b2f28508.jpg)

![](images/4749d2b22dd23363596d2f2139a8d9bd9693972c6ccdd857e3cb08e14953c0ac.jpg)  
(e)

![](images/57c2d06988b744cd78575d897ec06fde1ec45bc07407d370f2cce3ef74871cff.jpg)  
(f)  
Fig. 8. Results of each method in the measured experiment. (a) Without interference, (b) with interference, (c) ANC, (d) SFM, (e) Uysal, and (f) BCD-DS. Moreover, the first row of each subplot is the time-domain result and the second row is the RA result.

## C. Measured Experiments

Fig. 7 shows the scene we built for the measured experiment. Three TI radars, AWR2243 (ego-radar), MMWCAS-RF-EVM (aggressor radar, AR#1), and AWR1443 (aggressor radar, AR#2), are deployed to detect targets and emit the interference signals, respectively. AR#1 is 14.0 m away from ego-radar and AR#2 is 5 m away from ego-radar (Table III). In addition, two targets are set up, a stationary electric bicycle (Target#1) is 13.8 m away from ego-radar, and the other is a gray car (Target#2) is 25 m away from ego-radar moving at a speed of 5 m/s.

![](images/0257bbe6f6d153a4d1374529204a5c551f1789b35838825f9a05782e97bcfecf.jpg)  
(a)

![](images/089ab06d8ef1653f8b485b7e6c7a5bf7970a93e28617e377049fce5c3e9c2278.jpg)  
(b)

![](images/9dd7510e84a42436b58ebce914e1c7268ad402ae80615c55ced95af91992c768.jpg)  
(c)

![](images/5b3a19d281de3ada85e1cb9773d9bac08937f543d6dfaee8f5ad4921cf551b1a.jpg)  
(d)

![](images/dc34d3da7e8f9f75fd03717635570a318a38637a7d782c6b32fb27a8e2320945.jpg)  
(e)

![](images/f1ae24fc5ca37fdf966a42d6585ec1c415fa76e38fa614f66fce9cb331be7331.jpg)  
(f)  
Fig. 9. RD results of each method in the measured experiment. (a) Without interference, (b) without interference, (c) ANC, (d) SFM, (e) Uysal, and (f) BCD-DS.

There are 128 chirps in a frame of data and the length of each chirp is 512. By comparing the RA results for each chirp, we find that only half the chirps in a frame are affected by interference. The reason for this is as mentioned in Section II, and the interference is not in the range of the filter settings of the receiver at the current time slot. Fig. 8(a) shows the without interference, including only the system thermal noise and scene clutter, where both targets can be clearly observed from the RA results. The SINR<sub>t</sub> values for the two targets without interference are 9.26 dB, and 12.17 dB, respectively. Fig. 8(b) shows the with interference, which is one of the most severely affected chirps, including echoes, system thermal noise, and interference, compared with Fig. 8(a), with high-power bursts of interference in the time domain waveform. In the RA results, both targets are drowned out, where Target#1 is the most severely impaired and difficult to recognize. Both SINR<sub>t</sub> values for both drop to −1.24 and −1.01 dB, which shows that the effect of interference is significant.

Fig. 8(c)–(f) shows the interference suppression results of each method. For ANC, the amplitude of interference in the time domain is not satisfactorily reduced. In the RA result of ANC, Target#2 and Target#1 remains submerged in the interference, due to the principle of ANC which utilizes the high power presented by the target after the Fourier transform to suppress the surrounding interference. However, the power of Target#1 and Target#2 is already lower than the surrounding interference signal. In this case, the ANC is not as effective as expected. For SFM and Uysal, the amplitude of the interference is suppressed to a very low level in the time domain results. In their RA results, there are a lot of false targets, due to the limitations of the framework causing weak targets to be overwhelmed. Finally, BCD-DS achieves optimal performance. In the time domain results, compared to SFM and Uysal, the interference is hardly visible. In the RA results, both targets are apparently extracted and the noise level is reduced to around 10 dB.

Next, we further analyze all the chirps in a frame. Fig. 9 gives the corresponding RD results before and after interference suppression, where Fig. 9(b) shows RD results with interference, from which it can be viewed that the interference is scattered throughout the flat surface and the targets are not particularly visible. Similar to the simulation experiment, for a method, each chirp is treated with the same set of parameters. For ANC, interference and noise are still present in significant amounts. SFM utilizes only a priori information in the frequency domain to obtain the target, which requires a wide range of parameter settings for different chirp’s within a frame of data; therefore, in the line where the speed is 0 m/s, there are a large number of artifacts that cause the incorrect information to be passed on. The interference is not significantly sparse in the time-frequency domain, resulting in a more sensitive adjustment of the parameters. In the results of Uysal, similar artifacts and noise remain. BCD-DS alternately solves for interference and targets using prior information in both the time and frequency domains. Wherein, BCD-DS provides the best performance, interference is almost removed and both targets are perfectly rendered without artifacts.

To validate the performance of the proposed method in another scene, Xu [38] provide another set of measured data and the BLO algorithm. The whole experimental scene and parameters can be found in [38, Table II and Fig. 7]. In this scene, the ego-radar and the aggressor radar are 4 m away from each other, while the target is moving at a speed of 5 m/s. The corresponding RD results are given in Fig. 10, where Fig. 10(d) is BLO and Fig. 10(e) is LRS. From Fig. 10(d) to (f), it can be seen that BCD-DS is as effective

(a)

![](images/3e4fb3c6e5e498247ca57bd147535d88729104b8cb1819257dca19490daf8559.jpg)

![](images/833df8b8a72a2115b4cbd1379efa17f25fcc58bc744d208554c7f5c5e1825e31.jpg)

![](images/33926df92857a5b0fcdf36cfae7f0d3b8c2824ec059473c8979b8a61b1269f95.jpg)  
(d)

![](images/4c7a181c512fe139407c978f99286a1a9f5b4d40d37043bff40c52169d0cf97e.jpg)

![](images/4df5c889e33f26c241ff2b76bf740461f9431fe46c5b22942e1dce10ca8ce6ad.jpg)  
(e)

![](images/f94aba8cbdfb53173d0577cd77c18e50d57cba5a3f6c721173d2ad59f3d5c0d5.jpg)  
(f)  
Fig. 10. RD results of each method from the experimental scene in [38]. (a) Without interference, (b) with interference, (c) ANC, (d) BLO, (e) LRS, and (f) BCD-DS.

as BLO and LRS in suppressing the interference, and target information is accurately captured.

Finally, the advantages and disadvantages of each algorithm are summarized. ANC has low computational complexity and simple implementation, but the method is not satisfactory when the interference power exceeds the target. For compressed sensing-based methods, Uysal is more sensitive to the parameters as the interference is not sparse enough in the time-frequency domain. BLO, LRS, and BCD-DS have good interference suppression but possess more cumbersome parameter settings.

## V. CONCLUSION

This article presents an efficient modified dual-domain block coordinate descent algorithm, which can synchronously suppress mutual interference between automotive radars by jointly leveraging the priors in time and frequency domains. Both simulations and experiments validate the effectiveness of our method. In the simulation experiment, at different overall SINRs, our method is effective. The SINR<sub>t</sub> values of the two targets are improved by 47 and 42 dB on average, respectively. In the measured experiment, a moving target and a static target are set up. The results show great attenuation of interference power. Moreover, the RD results correctly present the velocity and distance information of the targets and the noise level is significantly reduced.

In future work, beyond the $l _ { 1 }$ norm, we will combine mathematical theory and target properties to design suitable optimization functions. Additionally, applying the framework in deep networks to adaptively learn the parameters.

## APPENDIX

## CONVERGENCE OF ITERATIONS

Since there are two phases in the iterations of the BCD-DS for solving the sparse coefficients of the interference and the target. In the first phase of the iterations, all subproblems

from (12) are convex optimization, given that

$$
H ( \mathbf { x } _ { 1 } , \mathbf { z } _ { 1 } ) = \frac { 1 } { 2 } \parallel \mathbf { S _ { D 1 } } - \mathbf { A _ { 1 } } \mathbf { x } _ { 1 } \parallel _ { 2 } ^ { 2 } + \lambda _ { 1 } \parallel \mathbf { z } _ { 1 } \parallel _ { 1 } .\tag{23}
$$

The results obtained from the first-order optimality conditions in the iteration $q + 1$ are shown as follows:

$$
\left\{ \begin{array} { l l } { \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } ) + \mathbf { u } _ { 1 } ^ { ( q ) } + \theta _ { 1 } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } - \mathbf { z } _ { 1 } ^ { ( q ) } ) = 0 } \\ { \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( q + 1 ) } ) - \mathbf { u } _ { 1 } ^ { ( q ) } - \theta _ { 1 } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } - \mathbf { z } _ { 1 } ^ { ( q + 1 ) } ) = 0 } \\ { \mathbf { u } _ { 1 } ^ { ( q + 1 ) } = \mathbf { u } _ { 1 } ^ { ( q ) } + \theta _ { 1 } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } - \mathbf { z } _ { 1 } ^ { ( q + 1 ) } ) } \end{array} \right.\tag{24}
$$

where $\partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } )$ and $\partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( q + 1 ) } )$ denote the partial derivative result of $H ( \mathbf { x } _ { 1 } , \mathbf { z } _ { 1 } )$ for $\mathbf { X } _ { 1 }$ and $\mathbf { z } _ { 1 }$ , respectively. Assume that there exists at least one set of optimal solutions $\mathbf { x } _ { 1 } ^ { * } , \mathbf { z } _ { 1 } ^ { * }$ , and $\mathbf { u } _ { 1 } ^ { * }$ for (12)

$$
\left\{ \begin{array} { l l } { \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { * } ) + u _ { 1 } ^ { * } + \theta _ { 1 } ( \mathbf { x } _ { 1 } ^ { * } - \mathbf { z } _ { 1 } { } ^ { * } ) = 0 } \\ { \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { * } ) - u _ { 1 } ^ { * } - \theta _ { 1 } ( \mathbf { x } _ { 1 } ^ { * } - \mathbf { z } _ { 1 } ^ { * } ) = 0 } \\ { \mathbf { u } _ { 1 } ^ { * } = \mathbf { u } _ { 1 } { } ^ { * } + \theta _ { 1 } ( \mathbf { x } _ { 1 } ^ { * } - \mathbf { z } _ { 1 } ^ { * } ) . } \end{array} \right.\tag{25}
$$

Define the error between the results of the qth iteration and the set of optimal solutions as follows:

$$
\left\{ \begin{array} { l l } { \mathbf { R } _ { x _ { 1 } } ^ { ( q ) } = \mathbf { x } _ { 1 } ^ { ( q ) } - \mathbf { x } _ { 1 } ^ { * } } \\ { \mathbf { R } _ { z _ { 1 } } ^ { ( q ) } = \mathbf { z } _ { 1 } ^ { ( q ) } - \mathbf { z } _ { 1 } ^ { * } } \\ { \mathbf { R } _ { u _ { 1 } } ^ { ( q ) } = \mathbf { u } _ { 1 } ^ { ( q ) } - \mathbf { u } _ { 1 } ^ { * } . } \end{array} \right.\tag{26}
$$

Next, subtracting (24) by (25) can obtain

$$
\begin{array} { r } { \left\{ \begin{array} { l l } { \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( * ) } ) + \mathbf { R } _ { u _ { 1 } } ^ { ( q ) } = \theta _ { 1 } ( \mathbf { R } _ { z _ { 1 } } ^ { ( q ) } - \mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } ) } \\ { \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( * ) } ) - \mathbf { R } _ { u _ { 1 } } ^ { ( q ) } = \theta _ { 1 } ( \mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } - \mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) } ) } \\ { \mathbf { R } _ { u _ { 1 } } ^ { ( q + 1 ) } = \mathbf { R } _ { u _ { 1 } } ^ { ( q ) } + \theta _ { 1 } ( \mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } - \mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) } ) . } \end{array} \right. } \end{array}\tag{27}
$$

Perform the inner product operations on $\mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } , \mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) }$ , and $\mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) }$ for each of the three equations in (27)

$$
2 \theta _ { 1 } \langle \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { * } ) , \mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } \rangle + \theta _ { 1 } ^ { 2 } \left\| \mathbf { R } _ { z _ { 1 } } ^ { ( q ) } \right\| _ { 2 } ^ { 2 }
$$

$$
\begin{array} { r l r } { \ } & { } & { + \ 2 \theta _ { 1 } \langle \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { * } ) , \mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) } \rangle - \theta _ { 1 } ^ { 2 } \left\| \mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } } \\ & { } & { = \left\| \mathbf { R } _ { u _ { 1 } } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } - \theta _ { 1 } ^ { 2 } \left\| \mathbf { R } _ { u _ { 1 } } ^ { ( q ) } \right\| _ { 2 } ^ { 2 } + \left\| \theta _ { 1 } \mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } - \theta _ { 1 } \mathbf { R } _ { z _ { 1 } } ^ { ( q ) } \right\| _ { 2 } ^ { 2 } } \\ & { } & { + \left\| \theta _ { 1 } \mathbf { R } _ { x _ { 1 } } ^ { ( q + 1 ) } - \theta _ { 1 } \mathbf { R } _ { z _ { 1 } } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } , \qquad ( 2 8 . } \end{array}
$$

where ⟨·⟩ denotes the inner product operation. Accumulating all terms in (28) from $q = 0$ to +∞

$$
\begin{array} { l } { \displaystyle \left\| \mathbf { R } _ { : 1 } ^ { ( 0 ) } \right\| _ { 2 } ^ { 2 } + \left\| \mathbf { R } _ { u _ { 1 } } ^ { ( 0 ) } \right\| _ { 2 } ^ { 2 } } \\ { + \displaystyle \sum _ { j = 0 } ^ { + \infty } 2 b _ { 1 } \langle \partial H _ { N _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { N _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( s ) } ) , \mathbf { R } _ { \mathbf { x } _ { 1 } } ^ { ( q + 1 ) } \rangle } \\ { + \displaystyle \sum _ { j = 0 } ^ { + \infty } } \\ { + \displaystyle \sum _ { q = 0 } ^ { + \infty } 2 \theta _ { 1 } \langle \partial H _ { N _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { N _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( s ) } ) , \mathbf { R } _ { \mathbf { x } _ { 1 } } ^ { ( q + 1 ) } \rangle } \\ { = \displaystyle \sum _ { q = 0 } ^ { + \infty } \left\| \theta _ { 1 } \mathbf { R } _ { \mathbf { x } _ { 1 } ^ { ( q + 1 ) } } ^ { ( q + 1 ) } - \theta _ { 1 } \mathbf { R } _ { \mathbf { x } _ { 1 } ^ { ( q + 1 ) } } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } + \left\| \mathbf { R } _ { \mathbf { z } _ { 1 } } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } } \\ { + \displaystyle \sum _ { j = 0 } ^ { + \infty } \left\| \theta _ { 1 } \mathbf { R } _ { \mathbf { x } _ { 1 } ^ { ( q + 1 ) } } ^ { ( q + 1 ) } - \theta _ { 1 } \mathbf { R } _ { \mathbf { z } _ { 1 } } ^ { ( q ) } \right\| _ { 2 } ^ { 2 } + \left\| \mathbf { R } _ { \mathbf { u } _ { 1 } } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } . } \end{array}\tag{29}
$$

Since all terms of (29) are non-negative, it follows that $\begin{array} { r } { \sum _ { q = 0 } ^ { + \infty } 2 \theta _ { 1 } \langle \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { \mathbf { x } _ { 1 } } ( \mathbf { x } _ { 1 } ^ { * } ) , \bar { \mathbf { B } _ { x _ { 1 } } ^ { ( q + 1 ) } } \rangle \ < \ + \infty } \end{array}$ , which leads to:

$$
\begin{array} { r } { \langle \partial H _ { { \bf x } _ { 1 } } ( { \bf x } _ { 1 } ^ { ( q + 1 ) } ) - \partial H _ { { \bf x } _ { 1 } } ( { \bf x } _ { 1 } ^ { * } ) , { \bf R } _ { x _ { 1 } } ^ { ( q + 1 ) } \rangle = 0 . } \end{array}\tag{30}
$$

As the gradient at $\mathbf { x } _ { 1 } ^ { * }$ is 0, (30) can be simplified

$$
\begin{array} { r } { \langle \partial H _ { { \bf x } _ { 1 } } ( { \bf x } _ { 1 } ^ { ( q + 1 ) } ) , { \bf x } _ { 1 } ^ { ( q + 1 ) } - { \bf x } _ { 1 } ^ { ( * ) } \rangle = 0 . } \end{array}\tag{31}
$$

In the same way, we can get

$$
\begin{array} { r } { \langle \partial H _ { \mathbf { z } _ { 1 } } ( \mathbf { z } _ { 1 } ^ { ( q + 1 ) } ) , \mathbf { z } _ { 1 } ^ { ( q + 1 ) } - \mathbf { z } _ { 1 } ^ { ( * ) } \rangle = 0 . } \end{array}\tag{32}
$$

Furthermore, according to the convex optimization function qualities, since $\mathbf { x } _ { 1 } ^ { ( * ) }$ and $\mathbf { z } _ { 1 } ^ { ( * ) }$ are optimal, we can combine (31) and (32) to obtain

$$
\begin{array} { l } { { \displaystyle \operatorname* { l i m } _ { q \to \infty } \left( \frac { 1 } { 2 } \left\| \mathbf { S _ { D 1 } } - \mathbf { A _ { 1 } } \mathbf { x } _ { 1 } ^ { ( q + 1 ) } \right\| _ { 2 } ^ { 2 } + \lambda _ { 1 } \left\| \mathbf { z } _ { 1 } ^ { ( q + 1 ) } \right\| _ { 1 } \right) } } \\ { - \left( \frac { 1 } { 2 } \left\| \mathbf { S _ { D 1 } } - \mathbf { A _ { 1 } } \mathbf { x } _ { 1 } ^ { * } \right\| _ { 2 } ^ { 2 } + \lambda _ { 1 } \left\| \mathbf { z } _ { 1 } ^ { * } \right\| _ { 1 } \right) = 0 . } \end{array}\tag{33}
$$

We can conclude that (12) can be optimally solved after several iterations. The second stage is solved in the same way as the first stage, therefore the iterations of (17) also show the convergence.

## REFERENCES

[1] M. Wang, S. Wei, Z. Zhou, J. Shi, X. Zhang, and Y. Guo, “CTV-Net: Complex-valued TV-driven network with nested topology for 3-D SAR imaging,” IEEE Trans. Neural Netw. Learn. Syst., Sep. 2022.

[2] L. Zhang, L. Su, D. Wang, Y. Luo, and Q. Zhang, “Mainlobe interference suppression for radar network via RPCA-based covariance matrix reconstruction,” IEEE Sensors J., vol. 23, no. 5, pp. 5094–5108, Mar. 2023.

[3] J. Lien et al., “Soli: Ubiquitous gesture sensing with millimeter wave radar,” ACM Trans. Graph., vol. 35, no. 4, pp. 1–19, 2016.

[4] Y. Ding, J. Tang, X. Xu, and J. Zhang, “Echo interference suppression approach for Doppler through-wall radar,” IEEE Sensors J., vol. 15, no. 6, pp. 3395–3402, Jun. 2015.

[5] D. M. Grimes and T. O. Jones, “Automotive radar: A brief review,” Proc. IEEE, vol. 62, no. 6, pp. 804–822, Jun. 1974.

[6] T. Doi et al., “Frequency hopping ultra wideband inter-vehicle radar system using chirp waveforms,” in Proc. Int. Workshop Ultra Wideband Syst. Joint With Conf. Ultra Wideband Syst. Technolog. Joint (UWBST IWUWBS), May 2004, pp. 386–390.

[7] S. Wei, H. Zhang, X. Zeng, Z. Zhou, J. Shi, and X. Zhang, “CARNet: An effective method for SAR image interference suppression,” Int. J. Appl. Earth Observ. Geoinformation, vol. 114, Nov. 2022, Art. no. 103019.

[8] Z. Guan, Y. Chen, P. Lei, D. Li, and Y. Zhao, “Application of hash function on FMCW based millimeter-wave radar against DRFM jamming,” IEEE Access, vol. 7, pp. 92285–92295, 2019.

[9] G. Feinberg, S. Mulleti, E. Shoshan, and Y. C. Eldar, “Hardware prototype demonstration of a cognitive sub-Nyquist automotive radar,” Electron. Lett., vol. 55, no. 9, pp. 556–558, May 2019.

[10] J.-G. Kim, S.-H. Sim, S. Cheon, and S. Hong, “24 GHz circularly polarized Doppler radar with a single antenna,” in Proc. Eur. Microw. Conf., 2005, p. 1386.

[11] X. Zhang, D. Cao, and L. Xu, “Joint polarisation and frequency diversity for deceptive jamming suppression in MIMO radar,” IET Radar, Sonar Navigat., vol. 13, no. 2, pp. 263–271, Feb. 2019.

[12] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun. 2016, pp. 1–9.

[13] M. A. Hossain, I. Elshafiey, and A. Al-Sanie, “Waveform diversity for mutual interference mitigation in automotive radars under realistic traffic environments,” Signal, Image Video Process., vol. 13, no. 1, pp. 1–8, Feb. 2019.

[14] Z. Xu et al., “A novel method of mitigating the mutual interference between multiple LFMCW radars for automotive applications,” in Proc. IEEE Int. Geosci. Remote Sens. Symp., Jul. 2019, pp. 2178–2181.

[15] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[16] G. Hakobyan, K. Armanious, and B. Yang, “Interference-aware cognitive radar: A remedy to the automotive interference problem,” IEEE Trans. Aerosp. Electron. Syst., vol. 56, no. 3, pp. 2326–2339, Jun. 2020.

[17] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[18] T. Nozawa et al., “An anti-collision automotive FMCW radar using time-domain interference detection and suppression,” in Proc. Int. Conf. Radar Syst. (Radar), Oct. 2017, pp. 1–5.

[19] M. Umehira, T. Nozawa, Y. Makino, W. Xiaoyan, S. Takeda, and H. Kuroda, “A novel iterative inter-radar interference reduction scheme for densely deployed automotive FMCW radars,” in Proc. 19th Int. Radar Symp. (IRS), Jun. 2018, pp. 1–10.

[20] J.-H. Choi, H.-B. Lee, J.-W. Choi, and S.-C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Trans. Commun., vol. E99.B, no. 1, pp. 280–287, 2016.

[21] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 726–731.

[22] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[23] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[24] C. Liu, S. Liu, C. Zhang, Y. Huang, and H. Wang, “Multipath propagation analysis and ghost target removal for FMCW automotive radars,” in Proc. IET Int. Radar Conf. (IET IRC), Nov. 2020, pp. 330–334.

[25] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[26] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[27] R. Singh, D. Saluja, and S. Kumar, “Spread spectrum coded radar for R2R interference mitigation in autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 10418–10426, Aug. 2022.

[28] Z. Chen, F. Xie, C. Zhao, and C. He, “Radio frequency interference mitigation in high-frequency surface wave radar based on CEMD,” IEEE Geosci. Remote Sens. Lett., vol. 14, no. 5, pp. 764–768, May 2017.

[29] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270–5283, Dec. 2021.

[30] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[31] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[32] J. Mun, H. Kim, and J. Lee, “A deep learning approach for automotive radar interference mitigation,” in Proc. IEEE 88th Veh. Technol. Conf. (VTC-Fall), Aug. 2018, pp. 1–5.

[33] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153491–153507, 2021.

[34] N. Jayant, J. Johnston, and R. Safranek, “Signal compression based on models of human perception,” Proc. IEEE, vol. 81, no. 10, pp. 1385–1422, Oct. 1993.

[35] J. Bobin, J.-L. Starck, J. M. Fadili, Y. Moudden, and D. L. Donoho, “Morphological component analysis: An adaptive thresholding strategy,” IEEE Trans. Image Process., vol. 16, no. 11, pp. 2675–2681, Nov. 2007.

[36] Y. Wang, Y. Huang, C. Wen, X. Zhou, J. Liu, and W. Hong, “Mutual interference mitigation for automotive FMCW radar with time and frequency domain decomposition,” IEEE Trans. Microw. Theory Techn., vol. 71, no. 11, pp. 5028–5044, Nov. 2023.

[37] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[38] Z. Xu, “Bi-level ℓ<sub>1</sub> optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, Jan. 2023.

[39] S. Boyd, “Distributed optimization and statistical learning via the alternating direction method of multipliers,” Found. Trends Mach. Learn., vol. 3, no. 1, pp. 1–122, 2010.

[40] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[41] F. Uysal, I. Selesnick, and B. M. Isom, “Mitigation of wind turbine clutter for weather radar by signal separation,” IEEE Trans. Geosci. Remote Sens., vol. 54, no. 5, pp. 2925–2934, May 2016.

[42] M. V. Afonso, J. M. Bioucas-Dias, and M. A. T. Figueiredo, “Fast image recovery using variable splitting and constrained optimization,” IEEE Trans. Image Process., vol. 19, no. 9, pp. 2345–2356, Sep. 2010.

[43] X. Li, J. Ran, H. Zhang, and S. Wei, “MCSNet: A radio frequency interference suppression network for spaceborne SAR images via multidimensional feature transform,” Remote Sens., vol. 14, no. 24, p. 6337, Dec. 2022.

[44] J. Sun, H. Li, and Z. Xu, “Deep ADMM-net for compressive sensing MRI,” in Proc. Adv. Neural Inf. Process. Syst., vol. 29, 2016.

[45] M. Wang, S. Wei, Z. Zhou, J. Shi, and X. Zhang, “Efficient ADMM framework based on functional measurement model for mmW 3-D SAR imaging,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 3165541.

[46] A. Pascual-Iserte, A. I. Perez-Neira, and M. A. Lagunas, “On power allocation strategies for maximum signal to noise and interference ratio in an OFDM-MIMO system,” IEEE Trans. Wireless Commun., vol. 3, no. 3, pp. 808–820, May 2004.

[47] X. Huang, A. Tuyen Le, and Y. J. Guo, “Transmit beamforming for communication and self-interference cancellation in full duplex MIMO systems: A trade-off analysis,” IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 3760–3769, Jun. 2021.

![](images/a41401d68e42f75957d6a33a69db07c81caa02047af6951362180cfbf95c0de7.jpg)

Shunjun Wei (Member, IEEE) received the B.S., M.S., and Ph.D. degrees in electronic engineering from the University of Electronic Science and Technology of China (UESTC), Chengdu, China, in 2006, 2009, and 2013, respectively.

In 2014, he joined UESTC, where he is currently a Professor. His research interests include radar signal processing and synthetic aperture radar (SAR) systems.

His research interests include 3-D synthetic aperture radar (SAR) imaging, non-line-of-sight imaging, and radar signal processing.

Xiang Cai received the B.S. degree in information and communication engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2023, where he is currently pursuing the M.S. degree with the School of Information and Communication Engineering.

![](images/e6f54d4a1ef83cd79df9e7da9ec97bd853a0e51f2b0d8cf97cf41746c4ef13af.jpg)

Lin Nie (Student Member, IEEE) is currently pursuing the M.S. degree with the University of Electronic Science and Technology, Chengdu, Sichuan, China.

His research interests include synthetic aperture radar (SAR) jamming technique and SAR interference suppression.

![](images/6be69cdb1c44a7664a73c8f7707032f94d6eddcebe74a4a4966b9abd228f6fe4.jpg)

![](images/1716e71dba8187997c4ce9b9a07a94b38d8407deb6622f374d750c2d4b4d9fbc.jpg)

![](images/6a678199831dd0cd42e27e13457517ea3fc39de056b5fd168a9a01e33fc50ab0.jpg)  
Hao Zhang (Student Member, IEEE) received the B.S. degree from the Southwest University of Science and Technology of China, Mianyang, China, in 2021. He is currently pursuing the M.S. degree with the School of Information and Communication Engineering, University of Electronic Science and Technology of China, Chengdu, China.

Mou Wang received the B.S. degree in communication engineering from the Chongqing University of Posts and Telecommunications, Chongqing, China, in 2018, and the Ph.D. degree from the School of Information and Communication Engineering, University of Electronic Science and Technology of China (UESTC), Chengdu, China.

In 2023, he joined UESTC. He is currently a Lecturer with UESTC.

![](images/5d1827f483574548e027c60dc85dc4a0eabfdfed090718b8e3780ab69fb1ce3e.jpg)

Jun Shi (Member, IEEE) received the B.S., M.S., and Ph.D. degrees in electronic engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2002, 2005, and 2009, respectively.

His research interests include radar interference suppression and machine learning.

He is currently an Associate Professor at the University of Electronic Science and Technology of China. His research interests include radar signal processing and synthetic aperture radar systems.

![](images/73506f5aa7113ca969621d300cd4df46fcb04ecacf2fed8b11fc65879c5340e3.jpg)

Guolong Cui (Senior Member, IEEE) received the B.S., M.S., and Ph.D. degrees in electronic information engineering from the University of Electronic Science and Technology of China (UESTC), Chengdu, China, in 2005, 2008, and 2012, respectively.

From September 2013 to July 2018, he was an Associate Professor with UESTC, where he has been a Professor since August 2018. His research interests include cognitive radar, array signal processing, multi-in multiout (MIMO)

radar, and through-the-wall radar.