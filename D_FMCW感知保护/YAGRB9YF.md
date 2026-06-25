#

Hao Zhang , Shunjun Wei , Senior Member, IEEE, Rui Min , Member, IEEE, Xiang Cai , Shuangqiao Li, Jin Li , Member, IEEE, Mou Wang , Member, IEEE, Jun Shi , Member, IEEE, and Guolong Cui , Senior Member, IEEE

Abstract—The widespread adoption of frequency-modulated continuous wave (FMCW) radar operating in microwave bands has made mutual interference inevitable. Currently, conventional hardware-based solutions increase microwave system complexity, while microwave signal-processing methods struggle with efective interference suppression under limited samples. To address these challenges, this article proposes a range-Doppler coupled learning and reconstruction network (RDLR-Net) for adaptive suppression of interference between FMCW radars. First, the interference suppression is reformulated as a microwave signal reconstruction problem with a coupled range-Doppler optimization. Subsequently, a novel regularization constraint model is introduced, which combines the l norm and target capture operator to efectively separate strong and weak scattering targets. A framework based on distributed optimization is designed and unfolded into a deep feedforward network to accelerate model training and inference. RDLR-Net adopts an unsupervised learning strategy to invert the target signal onto the original echo with interference, thus completing the loss term mapping. The simulation and multiple measured experiments demonstrate the proposed method achieves eficient interference suppression performance. Compared to state-of-the-art methods, the time required to process a single frame of measured data is only 0.0872 s, with the best interference suppression performance.

Index Terms—Frequency-modulated continuous wave (FMCW) radar, interference suppression, target capture, unsupervised learning.

## I. INTRODUCTION

N THE context of rapid advancements in modern I microwave radar systems, the frequency-modulated continuous wave (FMCW) radar operating in millimeter-wave bands (e.g., 77–81 GHz) has garnered significant attention due to its outstanding performance and extensive application potential [1]. However, as this technology becomes increasingly prevalent in fields, such as remote sensing [2], trafic monitoring, autonomous driving [3], industrial measurement [4], and target detection [5], the risk of mutual interference between radar systems has risen considerably. The occurrence of interference signals can lead to nonlinear distortions in beat-frequency signals during down conversion [6], resulting in false alarms in cluttered electromagnetic environments. These challenges are further exacerbated by microwave hardware limitations (e.g., fixed chirp parameters, limited dynamic range) and the realtime processing demands of embedded microwave platforms. To address these microwave-specific system-level bottlenecks, the advanced signal-level interference suppression techniques are urgently needed to ensure the reliable operation of FMCW radars in dense electromagnetic ecosystems.

## A. Related Works

In recent years, mitigating mutual interference among FMCW radars has become one of the primary research directions for scholars around the world. To address this challenge, a variety of solutions have been proposed. This article classifies these approaches into two categories: interference suppression based on radar hardware and system strategies and interference suppression based on signal processing.

The hardware and strategic interference mitigation techniques aim to address microwave system-level challenges in multiradar environments by optimizing millimeter-wave hardware architecture, antenna design, and system parameter coordination. First, in terms of antenna design, adjusting the polarization mode of the receiving antenna has been shown to efectively mitigate interference caused by polarization mismatch [7], [8]. Furthermore, the advancement of beamforming technology enables radar systems to flexibly control beam direction, thereby avoiding potential interference sources [9], [10]. To coordinate multiradar operations, centralized control strategies, such as preallocating chirp parameters (e.g., frequency ramps, transmit power) via a central radar console, have been proposed [11]. However, such approaches increase system complexity and require high bandwidth data exchange between radars. Cognitive radar systems [12] dynamically adapt parameters (e.g., carrier frequency, modulation bandwidth) to suppress interference but face challenges in real-time decision-making under embedded microwave hardware constraints. The time-frequency division multiple access (TFDMA) scheme [13] reduces mutual interference by coordinating chirp sequence scheduling in shared microwave bands. While efective, TFDMA’s performance is limited by fixed chirp parameter granularity and synchronization accuracy in dense radar networks. Other studies [14], [15], [16] propose orthogonal waveform encoding (e.g., phasecoded or noise-modulated signals) to enhance robustness in millimeter-wave channels. However, these methods increase hardware design complexity, requiring wideband mixers and high-speed ADCs, and are constrained by manufacturing costs and power consumption in automotive/embedded platforms [17].

In interference suppression based on signal processing, techniques are primarily implemented on the existing radar hardware through detailed processing and analysis of received signals. First, filters can be designed to selectively retain the frequency components of target signals while suppressing interference frequencies [18], [19], [20], [21]. Additionally, Rohman et al. [22] designed an adaptive filter based on the Hilbert transform using the least mean square (LMS) principle, which efectively mitigates interference efects and highlights the target signals. Moreover, a specific time-domain low-pass filter can be designed to extract interference signals [23], which can then be subtracted from the original echo to obtain the target signal. However, the filter-based suppression methods may inadvertently attenuate the energy of target signals while removing interference, posing a potential risk for protecting weak target signals. The frequency domain-based methods primarily process echo signals through spectrum analysis, thereby eliminating interference components in the frequency domain. Empirical mode decomposition (EMD) can decompose the echo signal into multiple frequency components [24], [25], enabling selective removal of specific interference frequencies. The short-time Fourier transform (STFT) can also be used for interference suppression, as it analyzes the frequency distribution of signals over diferent time intervals to achieve separation between target and interference signals [26], [27]. Additionally, constant false alarm rate (CFAR) detection can be utilized in the time-frequency domain for locating and filtering out interference signals [28], [29]. Moreover, since interference often exhibits instantaneous high-amplitude characteristics in the time sequence [30], this provides a feasible approach for time-domain interference removal, which has been efectively validated [31], [32]. However, when interference overlaps with the target signal in either the time or frequency domain, these methods may inadvertently remove useful information from the target signal while suppressing interference.

Deep learning techniques have been gradually applied to radar interference suppression [33]. Convolutional neural networks (CNNs), due to their powerful feature extraction capabilities, have shown potential in extracting target features from complex signals [34], in both the time-frequency and frequency domains [35], [36], [37], [38], [39]. However, these end-to-end learning methods sufer from limited interpretability and generalization capabilities, and their training often requires a large amount of labeled data, which is challenging to obtain in real-world interference scenarios.

In recent years, compressed sensing (CS) has demonstrated its unique advantages in radar imaging [40], angle-of-arrival estimation [41], interference suppression [42], [43], and other related fields. Chen et al. [44] employed sparse Bayesian inference to identify and filter out interference and noise components from target signals. Additionally, Uysal [45] introduced the sparse-augmented Lagrangian shrinkage algorithm (SALSA) to solve the sparse representations of target and interference signals in both the frequency and time-frequency domains. Building on SALSA, Xu and Yuan [46] proposed an interference suppression method in the tunable Q-factor wavelet transform (TQWT) domain. Yuan et al. [47] proposed a fast-convergence method based on fused least absolute shrinkage and selection operator (lasso), which efectively reduces computational overhead. What is more, it has also been shown that solving with sparse priors in both the time and frequency domains can efectively separate target and interference signals [48], [49]. Moreover, model optimization based on double $l _ { 1 }$ norms has been proven to help protect weak target signals [50]. Combining the low-rank and sparse characteristics of signals facilitates target extraction [51]. Wang et al. [52] further proposed a tensor decomposition method to eliminate interference in multiple chirp signals. To enhance the computational eficiency, a 2-D block Kronecker CS framework is [53] proposed, which plays a certain efect of interference suppression. Overall, CS-based methods perform well in separating interference signals, but their reliance on time-consuming parameter tuning limits their real time applicability in engineering contexts. Our previous work addressed these challenges [54] by innovatively combining deep learning with CS. However, while efective for suppressing single chirp interference, this approach may weaken the relationships between chirps and neglect weak scattering target extraction. Although some works [55], [56] have proposed supervised unfolded networks for processing 2-D radar data, they are still limited by labeled data and fixed application scenarios.

To address the aforementioned issues, this article proposes a novel range-doppler coupled learning and reconstruction network (RDLR-Net) that can efectively suppress multichirp interference between FMCW radars in parallel. First, a 2- D range-doppler strong coupling optimization is constructed, incorporating a joint constraint of the $l _ { 1 }$ norm and target capture operators to enhance the perception capability of weak target signals. Then, a framework based on distributed optimization is designed and integrated into a deep network with hierarchical learning capabilities to achieve flexible feature learning. Finally, the target signals output by RDLR-Net are mapped back to the original echoes to form the loss constraint in unsupervised learning, thereby reducing the reliance on labeled data and further improving the network’s generalization capability. The performance of RDLR-Net is validated through simulations and measured data. In summary, the innovations and contributions of this article are as follows.

1) A target capture operator is introduced and jointly constrained with the $l _ { 1 }$ norm, thereby simultaneously capturing on both strong and weak targets.

2) An improved multiconstraint sparse optimization framework is designed and extended into a deep feedforward network to accelerate the training and inference of the model.

3) An unsupervised learning strategy is adopted, for significantly reducing data dependency, to map the target signal back to the original echo containing interference, thereby achieving distance-energy loss term mapping and guiding the stable optimization of the model.

The remainder of this article is organized as follows. Section II introduces the signal model with interference. Section III provides an in-depth explanation of the proposed method, including the model framework, network architecture, and loss function design. Section IV presents the simulation and measured experiments, covering experimental metrics, implementation details, and result analysis. Finally, Section V concludes this article.

## II. SIGNAL MODEL WITH INTERFERENCE

In this section, we establish an interfered signal model based on the fundamental principles of FMCW radar operation. When multiple FMCW radars operate within the same millimeter-wave bands, mutual interference results in the detection radar (DR) receiving additional frequency components beyond the target echoes, as illustrated in the following:

$$
\mathbf { E } _ { Y , g } \left( t \right) = \mathbf { E } _ { X , g } \left( t \right) + \mathbf { E } _ { I , g } \left( t \right) + \mathbf { N }\tag{1}
$$

where $\mathbf { E } _ { Y } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ represents the received echo by the DR, consisting of $N _ { c }$ chirps, each with $N _ { r }$ sampling points. $\mathbf { E } _ { X } \in$ $\mathbb { C } ^ { N _ { r } \times N _ { c } }$ corresponds to the target echo, E $\mathbf { \bar { \Psi } } \in \mathbb { C } ^ { \mathbf { \overline { { N } } } _ { r } \times N _ { c } }$ refers to the interference signal, and $\mathbf { N } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ represents the system noise. The term ${ \bf E } _ { Y , g } ( t )$ represents the $g ^ { t h }$ chirp in $\mathbf { E } _ { Y }$ , and the other components in the equation follow the same convention. To further analyze the influence of signal parameters on system performance, $\mathbf { E } _ { X , g } ( t )$ can be refined as follows:

$$
\begin{array} { r l r } & { } & { { \bf E } _ { X , g } \left( t \right) = \sqrt { \frac { \lambda ^ { 2 } \sigma G _ { e } P _ { t } } { 4 \pi ^ { 3 } \left( 2 - D _ { t } \right) ^ { 4 } } } \cdot \mathrm { r e c t } \left( \frac { t - \tau _ { t } - \frac { T _ { y } } { 2 } } { T _ { y } } \right) } \\ & { } & { \quad \cdot \exp \left[ j \left( 2 \pi f _ { c } \left( t - \tau _ { t } \right) + \mu \pi \left( t - \tau _ { t } \right) ^ { 2 } \right) \right] } \end{array}\tag{2}
$$

where represents the transmitted wavelength, $G _ { e }$ denotes the total gain of DR system, and $P _ { t }$ refers to the transmitted power of the DR. The parameter $T _ { y }$ indicates the duration of the chirp signal, while $\tau _ { t }$ is the receive delay from target. $f _ { c }$ corresponds to the carrier frequency, and $\mu$ denotes the frequency modulation (FM) rate. Additionally, $D _ { t }$ represents the range between the DR and the target, and $\sigma$ stands for the radar cross section (RCS) of the target. It is important to note that the above formulation and the subsequent analysis are based on a monostatic radar scenario, where the transmitting and receiving antennas are co-located. Subsequently, the received interference for a single chirp in this monostatic configuration can be formulated as follows:

$$
\mathbf { E } _ { I , g } \left( t \right) ( t ) = \sqrt { \frac { \lambda _ { i } ^ { 2 } G _ { i } P _ { i } } { \left( 4 \pi D _ { i } \right) ^ { 2 } } } \cdot \mathrm { r e c t } \left( \frac { t - \tau _ { i } - \frac { T _ { y } } { 2 } } { T _ { y } } \right)
$$

![](images/e4ee95f6424abd4e11074a2c996f0bbde49617e9c5c149acfbaefe8276d57880.jpg)  
Fig. 1. Overall framework of the DR system, where TA and RA denote the transmitting and receiving antennas. Besides, LNA, PA, and VGA denote low-noise amplifier, power amplifier, and variable gain amplifier.

$$
\cdot \exp \left[ j \left( 2 \pi f _ { c } \left( t - \tau _ { i } \right) + \mu _ { i } \pi \left( t - \tau _ { i } \right) ^ { 2 } \right) \right]\tag{3}
$$

in this context, $\tau _ { i }$ represents the time delay, and $D _ { i }$ denotes the range between the DR and the aggressor radar $( \operatorname { A R } ) . \mu _ { i } , G _ { i } ,$ and $P _ { i }$ refer to the FM rate, total gain, and transmitted power of the AR, respectively. The wavelength of the interference signal is denoted by $\lambda _ { i } ,$ which is equal to in this scenario. It is important to note that the likelihood of the FM rates $\mu$ and $\mu _ { i }$ being identical is very low, typically less than 0.1% [57], [58]. Consequently, this article primarily addresses the problem of interference suppression in cases where $\mu$ and $\mu _ { i }$ are diferent. <sup>µ µ</sup>In [59], the role of enhancing interference mitigation and system eficiency is highlighted in system design. The relative strength between interference and target echo depends on $D _ { i }$ $D _ { t }$ , and $\sigma$ of the target. For instance, a target with high $\sigma$ may still produce a dominant echo even at large $D _ { t }$ , whereas a low $\sigma$ could be overwhelmed by interference from a nearby source. To quantify the dynamic range requirement, the ratio of interference power to target echo can be calculated as: $( ( P _ { i } D _ { t } ^ { 4 } / \sigma P _ { t } D _ { i } ^ { 2 } ) ) ^ { \bar { 1 } / 2 }$

Fig. 1 gives the overall framework of the DR System. To more efectively extract useful information from the target signal, the received signal $\mathbf { E } _ { Y }$ needs to be downconverted. This process can also be referred to as a complex conjugate operation, as shown in the following:

$$
\begin{array} { r l } & { \mathbf { S } _ { Y } = \mathcal { F } _ { \mathrm { v g a } } \left( \mathcal { F } _ { \mathrm { l p f } } \left( \mathcal { M } _ { c } \left( \mathbf { E } _ { Y } , \mathbf { E } _ { T } \right) \right) \right) } \\ & { \quad \quad = \mathbf { S } _ { X } + \mathbf { S } _ { I } + \mathbf { S } _ { N } } \end{array}\tag{4}
$$

where $\mathcal { M } _ { c } ( \cdot , \cdot )$ represents the complex conjugate response function and $\mathbf { E } _ { T } \in \mathbb { C } ^ { N _ { r } \times N _ { p } }$ denotes the transmitted signal from DR. $\mathbf { S } _ { Y } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ is final obtained beat signal by DR. Correspondingly, $\mathbf { S } _ { X } \in \mathbb { C } ^ { N _ { r } \times N _ { c } } , \mathbf { S } _ { I } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ , and $\mathbf { \bar { S } } _ { N } \in \dot { \mathbb { C } } ^ { N _ { r } \times N _ { * } }$ refer to the target, interference, and noise beat signals, respectively. $\mathcal { F } _ { \mathrm { v g a } } ( \cdot )$ denotes variable gain amplifier function. $\mathcal { F } _ { \mathrm { l p f } } ( \cdot )$ represents the low-pass filter function, which is applied to remove high-frequency components from the beat signal to prevent spectral aliasing.

## III. PROPOSED METHOD

In this section, we introduce the proposed range-Doppler coupled learning and reconstruction (RDLR) algorithm, to suppress mutual interference between FMCW radars. First, we develop an optimization model that combines $l _ { 1 }$ norm and information capture operator. Second, multidimensional sparse priors are leveraged within an improved CS-based framework to enable target sensing. Finally, an unsupervised training approach is employed to adaptively optimize the interference suppression process.

## A. Interference Suppression Framework

As shown in (4), the mutual interference generated by FMCW radars is unintentional additive interference. Therefore, the interference term in (4) can be represented as independent components as follows:

$$
\mathbf { Y } = \mathbf { M } \mathbf { X } + \mathbf { I } + \mathbf { N }\tag{5}
$$

where matrices $\textbf { Y } ~ \in ~ \mathbb { C } ^ { N _ { r } \times N _ { c } }$ and $\textbf { N } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ represent the matrix forms of $\mathbf { S } _ { Y }$ and $\mathbf { S } _ { N } .$ , respectively. Besides, X ∈ $\mathbb { C } ^ { N _ { r } \times N _ { c } }$ represents the sparse coeficients of the target in the corresponding transform domain, with M $\mathbf { \Psi } \in \mathrm { ~ \mathbb { C } ^ { \cal N _ { r } \times \cal N _ { r } } ~ }$ as the measurement matrix. Typically, radar targets exhibit sparsity in the range dimension [45], [49], [50], [54], [60]. However, in the range dimension, the overlap between weak targets and interference signals can easily cause missed detections. The target also exhibits sparsity in the speed dimension [61]. Consequently, unlike the aforementioned work, we have improved the measurement matrix to compress the target signal simultaneously in both the fast-time and slow-time dimensions. Thus, (5) can be transformed into the following form:

$$
\mathbf { Y } = \mathbf { F } _ { 1 } \mathbf { X } \mathbf { F } _ { 2 } + \mathbf { I } + \mathbf { N }\tag{6}
$$

where both $\mathbf { F } _ { 1 } ~ \in ~ \mathbb { C } ^ { N _ { r } \times N _ { r } }$ and $\mathbf { F } _ { 2 } ~ \in ~ \mathbb { C } ^ { N _ { c } \times N _ { c } }$ represent the inverse Fourier transform (IFT) matrices. In scenarios with strong interference and noise, to solve for the target signal in (6), through integrating the signal’s sparsity and measurement fidelity, the following Lagrangian optimization model can be established:

$$
\hat { \mathbf { X } } = \arg \operatorname* { m i n } _ { \mathbf { X } } \frac { 1 } { 2 } \| \mathbf { Y } - \mathbf { F } _ { 1 } \mathbf { X } \mathbf { F } _ { 2 } \| _ { 2 } ^ { 2 } + \sum _ { N _ { g } } ^ { i = 1 } \lambda _ { i } \Omega _ { i } \left( \mathbf { X } \right)\tag{7}
$$

where $\| \cdot \| _ { 2 }$ denotes Euclidean norm, which ensures the data fidelity of the target signal. $\Omega _ { i } ( \mathbf { X } )$ denotes the regularization term for the target signal, with $N _ { g }$ being the number of constraints. Moreover, the regularization parameter $\lambda _ { i }$ balances signal sparsity and data fidelity.

In most cases, adopting only the $l _ { 1 }$ norm as a constraint can achieve focusing on strong scattering targets in the range dimension. However, it may overlook weak scattering targets that are submerged in interference signals. To address this issue, we propose a target capture regularization (TCR) to capture the efective information of weak scattering targets. As a result, the regularization term in (7) can be expressed in the following form:

$$
{ \hat { \mathbf { X } } } = \arg \operatorname* { m i n } _ { \mathbf { X } } { \frac { 1 } { 2 } } \| \mathbf { Y } - \mathbf { F } _ { 1 } \mathbf { X } \mathbf { F } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| \mathbf { X } \| _ { 1 } + \lambda _ { 2 } \| \mathbf { X } \| _ { \mathrm { T C R } }\tag{8}
$$

where $\| \cdot \| _ { 1 }$ represents the $l _ { 1 }$ norm, used to promote sparse solutions. $\| \mathbf { X } \| _ { \mathrm { T C R } }$ is the TCR regularization constraint, which can be further expressed as

$$
\left\{ \begin{array} { l l l l l l l l l l } { \displaystyle | | \mathbf { X } | | _ { \mathrm { T C R } } = | | \mathbf { Q } \mathbf { X } | | _ { 1 } } & & & & & \\  \displaystyle { \mathbf { Q } = \sum _ { i = 1 } ^ { N - 1 } \mathbf { e } _ { i } \mathbf { e } _ { i } ^ { T } + \sum _ { i = 1 } ^ { N - 1 } \mathbf { e } _ { i } \mathbf { e } _ { i + 1 } ^ { T } } & & & & \\ { \displaystyle \mathbf { e } _ { i } = \left[ 0 , \quad 0 , \quad \ldots , \quad 0 , \quad 1 , \quad 0 , \quad \ldots , \quad 0 \right] ^ { T } } \end{array} \right.\tag{9}
$$

from the above equation, $\mathbf { e } _ { i }$ be the ith standard basis vector, i.e., a vector with 1 in the ith position and 0 elsewhere. Besides, $\mathbf { Q } \in \mathbb { C } ^ { N _ { r } \times N _ { r } }$ facilitates the accumulation of energy from adjacent elements, thereby enhancing the energy of weak scattering points while it amplifies the distinction between interference/clutter and the target.

Thus, the interference suppression problem is transformed into sparse recovery of the target across multiple domains. Equation (8) represents a convex optimization problem with multiple constraints. Here, the alternating direction method of multipliers (ADMMs) is employed to decompose the original problem into several subproblems that can be solved independently. First, an auxiliary variable $\mathbf { Z } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ is introduced to decouple the complex constraints as follows:

$$
\begin{array}{c} { \displaystyle \hat { \mathbf { X } } = \arg \operatorname* { m i n } _ { \mathbf { X } } \frac { 1 } { 2 } \| \mathbf { Y } - \mathbf { F } _ { 1 } \mathbf { X } \mathbf { F } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| \mathbf { X } \| _ { 1 } + \lambda _ { 2 } \| \mathbf { Z } \| _ { 1 } }  \\ { \mathbf { S u b j e c t ~ } t o \mathbf { \textbf { Z } } = \mathbf { Q } \mathbf { X } . } \end{array}\tag{10}
$$

Thus, the augmented Lagrangian function for (10) can be expressed as follows:

$$
\begin{array} { l } { { \displaystyle { \mathcal { L } } _ { \theta } \left( { \bf X } , { \bf Z } , { \bf P } \right) = \frac { 1 } { 2 } \| { \bf Y } - { \bf F } _ { 1 } { \bf X } { \bf F } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| { \bf X } \| _ { 1 } } \ ~ } \\ { { \displaystyle ~ + ~ \lambda _ { 2 } \| { \bf Z } \| _ { 1 } + \mathrm { T r } \left( { \bf P } ^ { H } \left( { \bf X } - { \bf Z } \right) \right) + \frac { \theta } { 2 } \| { \bf X } - { \bf Z } \| _ { 2 } ^ { 2 } } } .  \end{array}\tag{11}
$$

where Tr(·) represents the trace of the matrix and is the penalty parameter. P is the Lagrange multiplier, used to enforce the constraint $\mathrm { ~ \bf ~ X ~ } = \mathrm { ~ \bf ~ Z ~ }$ through penalty terms. To simplify the objective function, U is defined as $( \mathbf { P } / \theta ) ;$ consequently, (11) can be simplified to the following form:

$$
\begin{array} { l } { \displaystyle \mathcal { L } _ { \theta } \left( \mathbf { X } , \mathbf { Z } , \mathbf { U } \right) = \frac { 1 } { 2 } \| \mathbf { Y } - \mathbf { F } _ { 1 } \mathbf { X } \mathbf { F } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| \mathbf { X } \| _ { 1 } } \\ { \displaystyle \quad + \lambda _ { 2 } \| \mathbf { Z } \| _ { 1 } + \frac { 1 } { 2 } \| \mathbf { Z } - \mathbf { Q } \mathbf { X } + \mathbf { U } \| _ { 2 } ^ { 2 } + \frac { \theta } { 2 } \| \mathbf { U } \| _ { 2 } ^ { 2 } . } \end{array}\tag{12}
$$

Based on this, by alternately updating the variables in (12), the solution for (9) can be obtained, as shown in the following:

$$
\begin{array} { r l } & { \displaystyle \{ \tilde { \mathbf { X } } = \arg \operatorname* { m i n } _ { \mathbf { X } } \ \frac { 1 } { 2 } \| \mathbf { Y } - \mathbf { F } _ { 1 } \mathbf { X } \mathbf { F } _ { 2 } \| _ { 2 } ^ { 2 } + \lambda _ { 1 } \| \mathbf { X } \| _ { 1 }  } \\ & { \displaystyle  + \frac { 1 } { 2 } \| \mathbf { Z } - \mathbf { Q X } + \mathbf { U } \| _ { 2 } ^ { 2 }  } \\ & { \displaystyle \{ \tilde { \mathbf { Z } } = \arg \operatorname* { m i n } _ { \mathbf { Z } } \lambda _ { 2 } \| \mathbf { Z } \| _ { 1 } + \frac { 1 } { 2 } \| \mathbf { Z } - \mathbf { Q X } + \mathbf { U } \| _ { 2 } ^ { 2 }  } \\ & { \displaystyle  \{ \tilde { \mathbf { U } } = \arg \operatorname* { m i n } _ { \mathbf { U } } \ \mathcal { L } _ { \boldsymbol { \theta } } ( \mathbf { X } , \mathbf { Z } , \mathbf { U } )  } \end{array}\tag{13}
$$

The first term in (13) represents a typical sparse optimization model with $l _ { 1 }$ regularization. Based on the accelerated

gradient descent theory [62], the iterative process can be expressed as follows:

$$
\left\{ \begin{array} { l l } { { \mathbf { X } } ^ { t + 1 } = \delta _ { s } \left( \mathcal { G } , { \mathbf { T } } _ { a d p } \right) } \\ { \mathcal { G } ^ { t } } & { = { \mathbf { X } } ^ { t } - \boldsymbol { \zeta } \cdot { \mathbf { F } } _ { 1 } ^ { H } \left( { \mathbf { F } } _ { 1 } { \mathbf { X } } ^ { t } { \mathbf { F } } _ { 2 } - { \mathbf { Y } } \right) { \mathbf { F } } _ { 2 } ^ { H } } \\ { - \theta \boldsymbol { \zeta } { \mathbf { Q } } ^ { H } \left( { \mathbf { Z } } ^ { t } - { \mathbf { Q } } { \mathbf { X } } ^ { t } + { \mathbf { U } } ^ { t } \right) } \\ { { \mathbf { T } } _ { a d p } = \left[ \Vert { \mathbf { X } } ^ { t } \left[ \boldsymbol { : } , \boldsymbol { 1 } \right] \Vert _ { 1 } , \Vert { \mathbf { X } } ^ { t } \left[ \boldsymbol { : } , 2 \right] \Vert _ { 1 } , \dots , \Vert { \mathbf { X } } ^ { t } \left[ \boldsymbol { : } , N _ { c } \right] \Vert _ { 1 } \right] \cdot \boldsymbol { \lambda } _ { 1 } } \end{array} \right.\tag{14}
$$

where t is the current iteration, and $\zeta$ is used to scale the amplitude of X. Moreover, $\delta _ { s } ( \cdot ; \cdot )$ represents soft thresholding function, and it can be expressed by the following equation:

$$
\delta _ { s } \left( \mathbf { r } ; \varepsilon \right) = \operatorname { s g n } \left( \mathbf { r } \right) \cdot \operatorname* { m a x } \left( \left| \mathbf { r } \right| - \varepsilon , 0 \right)\tag{15}
$$

where sgn(·) represents the sign function, and max(· ·) rep-<sup>,</sup>resents the max function. For FMCW radar data, the range energy distribution varies across chirps. If a constant threshold is applied, weak scattering targets may not be separated from interference signals. Therefore, as shown in (14), an adaptive threshold $\mathbf { T } _ { a d p } \in \mathbb { C } ^ { 1 \times N _ { c } }$ is proposed, which independently estimates the energy of each range cell, thereby enhance the generalization capability.

Next, based on the second term of (13), the iteration of Z can be expressed by the following equation:

$$
\begin{array} { r } { \mathbf { Z } ^ { t + 1 } = \delta _ { s } \left( \mathbf { Q } \mathbf { X } ^ { t + 1 } - \mathbf { U } ^ { t + 1 } , \lambda _ { 2 } \right) . } \end{array}\tag{16}
$$

The Lagrange multiplier U ensures the consistency of the constraint between X and Z, as shown in the following:

$$
\mathbf { U } ^ { t + 1 } = \mathbf { U } ^ { t } + \rho \left( \mathbf { Z } _ { 2 } ^ { t + 1 } - \mathbf { Q } \mathbf { X } ^ { t + 1 } \right)\tag{17}
$$

where $\rho \in \mathbb { R }$ controls the step size of the iteration. Finally, the <sup>ρ</sup>solutions to the three subproblems in (18) can be obtained as follows:

$$
\left\{ \begin{array} { l l } { \mathbf { X } ^ { t + 1 } = \delta _ { s } \left( \pmb { \mathcal { G } } ^ { t } , \mathbf { T } _ { a d p } \right) } \\ { \mathbf { Z } ^ { t + 1 } = \delta _ { s } \left( \mathbf { Q } \mathbf { X } ^ { t + 1 } - \mathbf { U } ^ { t } , \lambda _ { 2 } \right) } \\ { \mathbf { U } ^ { t + 1 } = \mathbf { U } ^ { t } + \rho \left( \mathbf { Z } _ { 2 } ^ { t + 1 } - \mathbf { Q } \mathbf { X } ^ { t + 1 } \right) } \end{array} \right.\tag{18}
$$

Algorithm 1 RDLR for Mutual Interference Suppression   
Require: Input interfered signal Y $\begin{array} { r l } {  { \overline { { \ \in \mathrm { ~ \mathbb ~ C } ^ { N _ { r } \times N _ { c } } ; } } } } \end{array}$ Number of   
iterations L; IFT matrix $\mathbf { F } _ { 1 } ~ \in ~ \mathbb { C } ^ { N _ { r } \times N _ { r } }$ $\mathbf { F } _ { 2 } ~ \in ~ \mathbb { C } ^ { N _ { c } \times N _ { c } }$   
Adjustable scalar parameter <sub>1</sub>, <sub>2</sub>, , , ;   
Ensure: Target signal $\mathbf { \bar { X } } ^ { o p t } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ in RD domain;   
1: Initialize ${ \bf { X } } ^ { 0 } = { { \bf { F } } _ { 1 } } ^ { H } { \bf { Y } } { { \bf { F } } _ { 2 } } ^ { H } , { \bf { Z } } ^ { 0 } = { \bf { 0 } } _ { N _ { r } \times N _ { c } } ;$   
2: while $t \leq L$ do   
3: Calculate $\mathcal { G }$ and $\mathbf { T } _ { a d p }$ via (14);   
4: Estimate target signal $\mathbf { X } ^ { t + 1 }$ via (14);   
5: if $\frac { | | \mathbf { X } ^ { t + 1 } - \mathbf { X } ^ { t } | | _ { 2 } ^ { 2 } } { | | \mathbf { X } ^ { t + 1 } | | _ { \gamma } ^ { 2 } } <$ then   
6: $\ddot { \mathbf { X } } ^ { o p t } = \mathbf { X } ^ { t + 1 } \mathbf { ; }$   
7: return $\mathbf { X } ^ { o p t }$   
8: end if   
9: Update auxiliary variable $\mathbf { Z } ^ { t + 1 }$ via (16);   
10: Calculate Lagrange multiplier $\mathbf { U } ^ { t + 1 }$ via (17);   
11: end while   
12: $\mathbf { X } ^ { o p t } = \mathbf { X } ^ { L }$

The detailed implementation of RDLR is provided in Algorithm 1. The target signal X is inherently sparse in the RD domain, whereas noise and interference lack this property. By combining l<sub>1</sub>-norm sparsity $\left( \lambda _ { 1 } | | \mathbf { X } | | _ { 1 } \right)$ with TCR $( \lambda _ { 2 } | | \mathbf { Q X } | | _ { 1 } )$ our method selectively enhances weak targets through structured sparsity. The adaptive threshold $\mathbf { T } _ { a d p }$ in (14) further ensures target fidelity by dynamically adjusting to range-cell energy distributions.

Similar to traditional CS-based methods, RDLR faces challenges in hyperparameter tuning. In addition to the initialization of the matrices, appropriate hyperparameter settings are crucial. If the parameters $\lambda _ { 1 }$ and $\lambda _ { 2 }$ are set too large, it will cause excessive sparsity, leading to information loss; if $\lambda _ { 1 }$ and $\lambda _ { 2 }$ are set too small, it may result in signal overfitting. Moreover, and $\rho$ significantly afect the convergence of RDLR, which adds complexity to engineering applications. Given the neural networks’ ability to handle complex and nonlinear problems, we integrate RDLR with deep learning techniques to further explore eficient interference suppression performance.

## B. RDLR-Net

To address the aforementioned challenges, we aim to introduce deep learning techniques to automatically optimize hyperparameters, enabling to accurately remove the interference signal from Y. At the current stage, simulated interference/noninterference data can be obtained for supervised training of the network. However, due to the influence of ground noise and clutter, the simulated data often fail to capture the features of real-world scenarios. Moreover, supervised learning is highly dependent on data availability, and insuficient data may lead to a model that cannot efectively adapt to varying interference signal strength and noise levels. Considering these limitations, unsupervised learning strategy is introduced, improving RDLR into a hierarchical deep network, termed RDLR-Net, that adaptively learns optimal parameters to enhance generalization.

1) Network Structure: Fig. 2 illustrates the detailed structure of RDLR-Net. The network consists of L layers, where the input is the echo signal with interference, and the output represents the target signal in the RD domain. Additionally, D-E loss stands for distance-energy loss, and Ψ(·) denotes the original echo inversion module (OEIM), both of which will be elaborated in the following.

In RDLR-Net, each layer corresponds to one iteration of the optimization process. Specifically, X, Z, and U are optimized according to the resulting (18) derived from (13), and the optimized tensors are then passed to the next layer, ensuring that the model can progressively approach the global optimum. The weights in the network primarily represent the parameters involved in the updates of X, $\mathbf { Z } ,$ and U. To enhance the flexibility of the network, the parameters $\lambda _ { 1 } ,$ $\lambda _ { 2 } , ~ \zeta , ~ \theta ,$ and $\rho$ <sup>λ</sup>are set to be learnable parameters for each layer, collectively referred to as $\{ \lambda _ { 1 } ^ { t } , \lambda _ { 2 } ^ { t } , \zeta ^ { t } , \theta ^ { t } , \rho ^ { t } \} _ { t = 1 , 2 , \ldots , L } .$ . In this way, the model can autonomously adjust its weights and biases during training, progressively extracting higher level abstract features from Y. Unlike exhaustive grid searches, our method optimizes hyperparameters using gradient-based updates within a physics-constrained feasible domain. The Adam optimizer adaptively tunes $\{ \lambda _ { 1 } ^ { t } , \lambda _ { 2 } ^ { t } , \zeta ^ { t } , \theta ^ { t } , \rho ^ { t } \} _ { t = 1 , 2 , \ldots , L }$ by minimizing the loss calculated in (21). This approach avoids brute-force exploration by leveraging radar signal properties (e.g., sparsity in the RD domain) and the decoupled subproblem structure of ADMM.

![](images/351133ea104a66933a8df963f267cdc0ffe84ff5a5e0f2f5322e08460e28a6f6.jpg)  
Fig. 2. Structure of RDLR-Net, where the network consists of L layers, with Y as the input and $\mathbf { X } ^ { L }$ as the output. The black solid lines represent the data flow, while the blue dashed lines indicate the connections of the loss function.

2) Original Echo Inversion Module: Since unsupervised training lacks labeled data, the loss function primarily relies on the intrinsic structure and distribution of the data. To better guide the network in learning parameters, we design the OEIM, which inverts the target signal in the RD domain back to the time domain, generating the original echo with interference, as shown in the following:

$$
\begin{array} { r l } {  { \mathbf { Y } _ { \mathrm { i n v } } = \Psi ( \mathbf { X } ^ { L } ) } } \\ & { = \kappa ( \mathbf { M } _ { L } + \mathbf { F } _ { 1 } \mathbf { X } ^ { L } \mathbf { F } _ { 2 } ) } \end{array}\tag{19}
$$

where $\mathbf { Y } _ { \mathrm { i n v } } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ represents the inverted input echo, and $\kappa \in \mathbb { R }$ is a learnable parameter that allows the model to adapt to interference characteristics of varying strength, flexibly adjusting response to diferent signals. $\mathbf { M } _ { L } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ is the learnable interference matrix, which can be further expressed as follows:

$$
\mathbf { M } _ { L } = \exp \left[ j ( 2 \pi \mathbf { P } _ { N } ) \right]\tag{20}
$$

where $\mathbf { P } _ { N } ~ \in ~ \mathbb { R } ~ \sim ~ \mathcal { N } ( 0 , 1 )$ $\mathbf { M } _ { L }$ is generated once at the beginning of the training process and updated at each epoch guided by loss function. By introducing $\mathbf { M } _ { L }$ to dynamically simulate interference signals during the training process, the model can adjust the amplitude and phase of $\mathbf { Y } _ { \mathrm { i n v } }$ according to the characteristics of Y, thereby reducing the diference of both for loss computation.

3) Loss Function: To fully leverage the valid information from unlabeled data and adapt to diferent types of data distributions, D-E loss $\mathcal { L } _ { D - E }$ is proposed to provide stable optimization for the model from both distance and energy perspectives. Given a training set $\{ \mathbf { Y } _ { i } \} _ { i = 1 } ^ { N _ { \mathrm { t r a i n } } }$ with $N _ { \mathrm { t r a i n } }$ training samples, where $\mathbf { Y } _ { i }$ denotes the original echo. Afterward, $\{ { \mathbf { Y } _ { i } } \} _ { i = 1 } ^ { N _ { \mathrm { t r a i n } } }$ is taken as a model input, which correspondingly yields $\{ \mathbf { X } _ { i } ^ { L } \} _ { i = 1 } ^ { N _ { \mathrm { t r a i n } } } . ~ \mathcal { L } _ { D - E }$ can be defined as follows:

$$
\mathcal { L } _ { D - E } = \mathcal { L } _ { D } + \delta \mathcal { L } _ { E }\tag{21a}
$$

$$
\mathcal { L } _ { D } = \sum _ { i = 1 } ^ { N _ { t r a i n } } \left. \mathbf { Y } _ { i } - \kappa \left( \mathbf { M } _ { L } + \mathbf { F } _ { 1 } \mathbf { X } _ { i } ^ { L } \mathbf { F } _ { 2 } \right) \right. _ { 2 }\tag{21b}
$$

$$
\mathcal { L } _ { E } = \sum _ { i = 1 } ^ { N _ { t r a i n } } \left. \mathbf { X } _ { i } ^ { L } \right. _ { 1 }\tag{21c}
$$

from the above equations, $\mathcal { L } _ { D - E }$ consists of two parts, which are distance loss $\mathcal { L } _ { D }$ and energy loss $\mathcal { L } _ { E }$ , respectively. In addition, is the weighting factor used to balance $\mathcal { L } _ { E }$ and $\mathcal { L } _ { D } , \mathcal { L } _ { D }$ measures the distance diference between Y and $\mathbf { Y } _ { \mathrm { i n v } }$ In this context, the $l _ { 2 }$ norm is smooth and diferentiable, providing a stable gradient for model optimization. $\mathcal { L } _ { E }$ measures the energy of X, with the following benefits: first, it promotes multidimensional sparsity of the target; and second, it facilitates implicit feature selection by automatically filtering out irrelevant features through zero outputs.

The specific training details of RDLR-Net are provided in Algorithm 2, where the input interfered training data $\mathbf { Y } _ { \mathrm { t o t a l } }$ contains $N _ { s }$ frames of data, and the final output is the learned optimal hyperparameter set.

## C. Computational Load

The computational complexity per iteration of the proposed method is analyzed as follows. Given the complex-valued matrices $\mathbf { Y } \in \bar { \mathbb { C } ^ { N \times N } } , \mathbf { F } _ { 1 } \in \mathbb { C } ^ { N \times N }$ , and $\mathbf { F } _ { 2 } \in \mathbb { C } ^ { N \times N }$ , the arithmetic operations required for updating the variables {X Z U} in each iteration of Algorithm 1 can be categorized into the following components:

complex multiplications : $6 N ^ { 3 } + 3 N ^ { 2 }$

complex additions : $: 2 N ^ { 3 } + 3 N ^ { 2 } .$

(22)

Algorithm 2 Training Implementation of RDLR-Net   
Require: Training data $\mathbf { Y } _ { t o t a l } \in \mathbb { C } ^ { N _ { s } \times N _ { r } \times N _ { c } }$ ; Number of iter  
ations $L ;$ Number of training epochs $K ;$ IFT matrix   
$\mathbf { F } _ { 1 } \in \mathbb { C } ^ { N _ { r } \times N _ { r } } , \mathbf { F } _ { 2 } \in \mathbb { C } ^ { N _ { c } \times N _ { c } }$ , Initialize learnable parameters   
$\lambda _ { 1 } ^ { 0 } , \lambda _ { 2 } ^ { 0 } , \zeta ^ { 0 } , \theta ^ { 0 } , \rho ^ { 0 } ;$   
Ensure: Optimal parameter sets $\{ \lambda _ { 1 } ^ { t } , \lambda _ { 2 } ^ { t } , \zeta ^ { t } , \theta ^ { t } , \rho ^ { t } \} _ { t = 1 , 2 , \ldots , L } ;$   
1: Initialize ${ \bf { X } } ^ { 0 } = { { \bf { F } } _ { 1 } } ^ { H } { \bf { Y } } { { \bf { F } } _ { 2 } } ^ { H } , { \bf { Z } } ^ { 0 } = { \bf { \bar { 0 } } } _ { N _ { r } \times N _ { c } } ;$   
2: while $k \leq K$ do   
3: while $t \leq L$ do   
4: Calculate $\mathcal { G }$ and $\mathbf { T } _ { a d p }$ via (14);   
5: Estimate target signal $\mathbf { X } ^ { t + 1 }$ via (14);   
6: Update auxiliary variable $\mathbf { Z } ^ { t + 1 }$ via (16);   
7: Calculate Lagrange multiplier $\mathbf { U } ^ { t + 1 }$ via (17);   
8: end while   
9: Calculate $\mathbf { Y } _ { i n \nu }$ via $( 1 9 ) ;$   
10: Calculate total loss $\mathcal { L } _ { D - E }$ via (21);   
11: Optimization, Learn $\{ \lambda _ { 1 } ^ { t } , \lambda _ { 2 } ^ { t } , \zeta ^ { t } , \theta ^ { t } , \rho ^ { t } \} _ { t = 1 , 2 , \ldots , L } ;$   
12: end while

Based on the above equations, the computational complexity of each iteration step is dominated by matrix multiplication. Since the number of iterations layers is typically less than 10, which is significantly smaller than N, the overall complexity of RDLR-Net is $O ( N ^ { 3 } )$ ).

## IV. EXPERIMENTS

In this section, we conducted multiple experiments to validate the efectiveness of the proposed method, with detailed experimental deployment provided. The experiments were performed on a computer having an Intel i7 processor with 32- GB random access memory (RAM) and an NVIDIA Quadro RTX6000 GPU with 24-GB video RAM. Additionally, we compared the proposed method with the existing interference mitigation methods to further quantitatively and qualitatively evaluate performance.

## A. Evaluation Metrics

To comprehensively assess the performance of the proposed method, we adopt a series of common evaluation metrics, including signal-to-interference-plus-noise ratio, structural similarity index measure (SSIM), root mean square error (RMSE), detection probability $( P _ { D } )$ , and probability of false alarm $( P _ { f } a )$ , which are defined as follows:

$$
\mathrm { S I N R } = 1 0 \log _ { 1 0 } \left( { \frac { P _ { \mathrm { t a r g e t } } } { P _ { \mathrm { i n } } + P _ { \mathrm { n o s i e } } } } \right)\tag{23}
$$

$$
\mathrm { S S I M } \left( \mathbf { v } , \hat { \mathbf { v } } \right) = \frac { \left( 2 \mu _ { \mathbf { v } } \mu _ { \hat { \mathbf { v } } } + C _ { 1 } \right) \left( 2 \sigma _ { \mathbf { v } \hat { \mathbf { v } } } + C _ { 2 } \right) } { \left( \mu _ { \mathbf { v } } ^ { 2 } + \mu _ { \hat { \mathbf { v } } } ^ { 2 } + C _ { 1 } \right) \left( \sigma _ { \mathbf { v } } ^ { 2 } + \sigma _ { \hat { \mathbf { v } } } ^ { 2 } + C _ { 2 } \right) }\tag{24}
$$

$$
\mathrm { R M S E } \left( \mathbf { v } , \hat { \mathbf { v } } \right) = \mathbf { \nabla } \sqrt { \frac { \sum _ { i = 1 } ^ { L } \left( < \mathbf { v } > _ { i } - < \hat { \mathbf { v } } > _ { i } \right) ^ { 2 } } { L } }\tag{25}
$$

$$
P _ { D } = 1 - { \frac { \sum _ { k = 1 } ^ { N _ { f } } N _ { w d } ^ { ( k ) } } { N _ { \mathrm { f } } \cdot N _ { t o f } } }\tag{26}
$$

$$
P _ { f a } = \frac { \sum _ { k = 1 } ^ { N _ { f } } { \frac { N _ { f a } ^ { ( k ) } } { N _ { r } \times N _ { c } } } } { N _ { f } } .\tag{27}
$$

![](images/a26da977ce4f300eede233c66db681baa8e1a838f1d9bbbc04e3113b02d82833.jpg)  
Fig. 3. Trends in training loss.

In (23), $P _ { \mathrm { t a r g e t } } , P _ { i n } .$ , and $P _ { \mathrm { n o i s e } }$ represent the target signal power, interference power, and noise power, respectively. SINR represents the ratio of signal power to the sum of interference and noise power. Generally, a higher SINR indicates that the target is less afected by interference.

In (24), $\mathbf { v } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ and $\hat { \mathbf { v } } \in \mathbb { C } ^ { N _ { r } \times N _ { c } }$ stand for the input signal and reference signal, respectively. Besides, $\mu$ and denote the mean value and the variance, respectively. $\sigma _ { \mathbf { v } \hat { \mathbf { v } } }$ represents the covariance between v and $\hat { \mathbf { v } } . ~ C _ { 1 }$ and $C _ { 2 }$ are constants. SSIM is adopted to evaluate the similarity between the model output and the reference signal. Generally, the closer the SSIM is to 1, the better the performance of the method.

In $( 2 5 ) , < \cdot > _ { i }$ is the extraction operator of the ith element. L denotes the number of elements in v. RMSE is used to measure the diference between the model output and the reference signal. Generally, a smaller RMSE indicates better performance of the method.

In (26), $N _ { f }$ denotes the total number of received data frames, $N _ { w d } ^ { ( k ) }$ represents the number of missed targets per frame, and $N _ { \mathrm { t o f } }$ denotes the preset number of targets per frame. $P _ { D }$ can intuitively reflect the ability of a method to retain target signals in complex interference environments. Generally, a higher $P _ { D }$ indicates better performance. In the experiment, the CFAR detector is employed for target detection, with the initial false alarm rate set to $1 \times 1 0 ^ { - 5 }$

In (27), $N _ { f a } ^ { ( k ) }$ denotes the number of false alarm points in the 2-D spectrum per data frame. The probability of $P _ { f } a$ directly reflects the ability of a method to suppress false signals in complex interference environments. Generally, a smaller $P _ { f } a$ indicates better performance.

## B. Implementation Details and Dataset

The network was implemented on the PyTorch framework, incorporating both the Adam and Lookahead optimizers to ensure fast and stable parameter updates, where synchronization interval and slow weight update factor are set to 5 and 0.5, respectively. For the simulation experiments, we constructed a synthetic dataset, with its relevant parameters detailed in Table I. Here, $\mathcal { U } [ a , b ]$ denotes a uniform distribution between a and b, and the dataset consists of 220 samples in total (200 for train and 20 for test). For measured experiments, we used the first ten frames of radar data collected in each scenario as the training set. In addition, we performed maximum amplitude normalization on the radar training data to enhance the stability of the model, as shown in the following:

TABLE I  
PARAMETERS SETTING OF FMCW RADAR INTERFERENCE DATASET
<table><tr><td>Parameters</td><td>DR</td><td>AR</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td>Chirp Rate(MHz/µs) Speed(m/s)</td><td>U[6,8] 0</td><td>U[10,12] 0</td></tr><tr><td>Number of Targets</td><td>U[1,2]</td><td></td></tr><tr><td>Target Speed(m/s)</td><td>0</td><td></td></tr><tr><td>Range of Target(m)</td><td>U[1,10]</td><td></td></tr><tr><td>Number of Interference</td><td>U[1,2]</td><td></td></tr></table>

TABLE II

PERFORMANCE COMPARISON OF $\mathcal { L } _ { D - E }$ ON DIFFERENT DOMAINS  
![](images/099c0e901723084cbe3d88bb4d3defb8ac5981f032a48e823a9bfe8d234295d6.jpg)  
Fig. 4. Distribution of $\mathbf { T } _ { \mathrm { a d p } }$ across chirp indices at diferent iterations.

$$
\tilde { \mathbf { Y } } _ { \mathrm { t o t a l } } ^ { \prime } \left( i , \cdot , \cdot \right) = \frac { \mathbf { Y } _ { \mathrm { t o t a l } } \left( i , \cdot , \cdot \right) } { \operatorname* { m a x } _ { j , k } \left| \mathbf { Y } _ { \mathrm { t o t a l } } \left( i , j , k \right) \right| } , \quad \forall i \in \{ 1 , 2 , \ldots , N _ { s } \}\tag{28}
$$

where $\mathrm { m a x } _ { j , k } \vert \mathbf { Y } _ { \mathrm { t o t a l } } ( i , j , k ) \vert$ denotes the maximum amplitude of each sample.To further validate the convergence behavior of the $\mathcal { L } _ { D }$ loss in (21b) under diferent domains using $\mathcal { L } _ { D - E }$ loss defined in (21a), we set $\delta = 1 0 ^ { - 3 }$ . Fig. 3 presents the corresponding results when the learning rate reaches approximately $0 . 5 \times 1 0 ^ { - 4 }$ . The experimental results show that when LD-loss is applied in the time domain, the LD-E loss converges around epoch 240, while the LD-E loss still has not fully stabilized. In addition, we evaluated the numerical performance of LD-loss on the test set in both the time domain and the RD domain. As shown in Table II, the results indicate that the performance of LD loss is significantly better in the time domain compared to the RD domain.

Furthermore, we conducted statistical analysis on the iterative convergence characteristics of $\mathbf { T } _ { \mathrm { a d p } }$ in (14). With the iteration depth set to 9 and $N _ { c } = 1 2 8$ , Fig. 4 illustrates the energy distribution statistics along the range direction at diferent iteration levels. The x-axis represents the chirp index from 1 to $N _ { c }$ , while the y-axis denotes normalized energy values.

TABLE III  
RADAR PARAMETERS FOR SIMULATION EXPERIMENT
<table><tr><td>PARAMETERS</td><td>DR</td><td>AR#1</td><td>AR#2</td><td>AR#3</td></tr><tr><td>Carrier Frequency (GHz)</td><td>77</td><td>77</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth (MHz)</td><td>600</td><td>660</td><td>540</td><td>720</td></tr><tr><td>Chirp Duration (µs)</td><td>60</td><td>50</td><td>80</td><td>65</td></tr><tr><td>FM rate (MHz/µs)</td><td>10</td><td>13.2</td><td>6.75</td><td>11.07</td></tr><tr><td>Range (m)</td><td>0</td><td>3</td><td>6</td><td>9</td></tr><tr><td>Speed (m/s)</td><td>0</td><td>0</td><td>-5</td><td>2</td></tr></table>

Experimental results demonstrate that the energy attenuation trends of chirps across iterations exhibit remarkable consistency. Besides, energy deviations between iterations were observed, which aligns with our theoretical expectations. This is achieved through adaptive estimation of iteration thresholds by statistically analyzing energy distributions across chirps in range cells.

During the following simulation and measured training processes, we set the learning rate to 0.001. The initial hyperparameters of RDLR-Net, denoted as $\{ \lambda _ { 1 } ^ { 0 } , \lambda _ { 2 } ^ { 0 } , \zeta ^ { 0 } , \theta ^ { 0 } , \rho ^ { 0 } \}$ , were uniformly initialized to {1 1 1 1 1}. These hyperparameters can be adaptively adjusted according to specific application scenarios.

## C. Simulation Experiment

The simulation Section IV will be divided into two modules, focusing, respectively, on the experimental validation of uniform targets and the experimental validation of weak targets. In the simulation experiments, there are 128 chirps per frame and each chirp contains 800 sampling points.

1) Experiment for Uniform Targets: In this section, we first conduct simulation experiments for uniform targets. Two targets are set and assigned similar scattering coeficients, with Target#1 and Target#2 located 20 and 50 m from the DR, respectively. Target#1 remained stationary, while Target#2 moved at a speed of 5 m/s. Moreover, 3 ARs are set, with diferent FM rates, at distances of 3, 6, and 9 m from the DR, respectively. The motion states of the three ARs were stationary, approaching the DR at a speed of 5 m/s and moving away from the DR at a speed of 2 m/s, respectively. To verify the robustness of the proposed method, the three ARs emit interference signals at diferent power levels to ensure that the SINR is controlled within the range of –20 to 0 dB. Additionally, additive white Gaussian noise (AWGN) is introduced to make the experiment more realistic. The specific experimental parameter configurations are presented in Table III. Notably, all radar-related parameters in these experiments fall outside the distribution ranges defined in Table II.

Fig. 5 presents the RD results of the simulation experiments, where Fig. 5(a) shows the case without interference, Fig. 5(b) represents the case with interference, Fig. 5(c) illustrates the wavelet denoising method (WDM) [23], Fig. 5(d) depicts the SALSA-based method (SALSA) [45], [46], Fig. 5(e) displays FUAS-Net [54], Fig. 5(f) is BCD-DS [48], Fig. 5(g) is RDLR, and Fig. 5(h) shows RDLR-Net. In the absence of interference, the range and velocity information of both targets are visible. Due to the relative velocity between the three deployed ARs and DRs, the presence of interference masks the velocity profiles at –2, 0, and 5 m/s, significantly impacting the detection of the two targets. The WDM decomposes the beat frequency signal into multiple frequency components and selectively removes the interference-related components. As shown in Fig. 5(c), the interference power on the RD plane is somewhat reduced, and Target #1, at the 0-m/s profile, can be faintly observed, with Target #2 appearing more distinct compared to the case with interference. The SALSA-based method iteratively separates the interference and target signals in diferent domains. As shown in Fig. 5(d), it demonstrates better results than the WDM, with the further reduction of interference power. RDLR simultaneously extracts the target in both the range and speed dimensions. As shown in Fig. 5(e), FUAS-Net suppresses interference on a chirp-bychirp basis, but the results indicate that some weak energy points remain, which may lead to false alarms. Fig. 5(f) presents the results of BCD-DS, where suboptimal hyperparameters, likely due to the limitations of the processing of single chirp, result in some artifacts at the –2 m/s profile. Fig. 5(g) shows good interference suppression, but due to the dificulty in tuning, there are still some sidelobes around

![](images/bf60b272e86b0180efe2353abee6a860ce3f4d43cd1d15fdbf949f2c4131897d.jpg)  
(a)

![](images/ea99f4618aea953c7508ec32919b43ee3e6dd2960f07634745c2f6137f90c57d.jpg)  
(b)

![](images/f8de811fae2cb04d632c4fd70f23bfffcb15c3cf8ec4b78dc063e7de67f128f7.jpg)

![](images/a0c1446cbe25f78d720508b935731370c8ca7091d41784c8b7548dc682624832.jpg)

![](images/924bd83e76c4e3bc913b004d1b2e329ed1855f7679eca90176a68f80a0192f49.jpg)  
(e)

(c)  
(d)  
![](images/58cd497cb18930b4fa2a49434b5903beefc6ea4d3cba68cff8d291c9b22a391d.jpg)  
(f)

![](images/5ad07ab2a132e9da03ce4f980382837bf60d6d4d1261563a252e25ffe9756da4.jpg)  
(g)

![](images/b2263f33bd0575983be6d873cd31e9997a73edce74b971c4e2afb433691cc005.jpg)  
(h)  
Fig. 5. Results of simulation experiments at the SINR of -15 dB. Where (a) without interference and noise, (b) with interference, (c) WDM, (d) SALSA-based method, (e) FUAS-Net, (f) BCD-DS, (g) RDLR, and (h) RDLR-Net.

TABLE IV  
NUMERICAL COMPARISON IN SIMULATION EXPERIMENT FOR UNIFORM TARGETS AT DIFFERENT SINRS, USING RMSE, SSIM, AND RUNNING TIME
<table><tr><td>Method</td><td colspan="2">Interference</td><td colspan="2">WDM</td><td colspan="2">SALSA</td><td colspan="2">FUAS-Net</td><td colspan="2">BCD-DS</td><td colspan="2">RDLR</td><td colspan="2">RDLR-Net</td></tr><tr><td>SINR</td><td>SSIM</td><td>RMSE</td><td>SSIM</td><td>RMSE</td><td>SSIM</td><td>RMSE</td><td>SSIM</td><td>RMSE</td><td>SSIM</td><td>RMSE</td><td>SSIM</td><td>RMSE</td><td>SSIM</td><td>RMSE</td></tr><tr><td>-20 dB</td><td>0.9352</td><td>0.8847</td><td>0.9539</td><td>0.7888</td><td>0.9755</td><td>0.4504</td><td>0.9841</td><td>0.1832</td><td>0.9801</td><td>0.2034</td><td>0.9824</td><td>0.1857</td><td>0.9927</td><td>0.0930</td></tr><tr><td>-15 dB</td><td>0.9548</td><td>0.6451</td><td>0.9696</td><td>0.5012</td><td>0.9826</td><td>0.1943</td><td>0.9873</td><td>0.1521</td><td>0.9815</td><td>0.1987</td><td>0.9883</td><td>0.1411</td><td>0.9938</td><td>0.0851</td></tr><tr><td>-10 dB</td><td>0.9673</td><td>0.5035</td><td>0.9812</td><td>0.1934</td><td>0.9881</td><td>0.1457</td><td>0.9909</td><td>0.0998</td><td>0.9854</td><td>0.1787</td><td>0.9908</td><td>0.1012</td><td>0.9949</td><td>0.0739</td></tr><tr><td>-5 dB</td><td>0.9728</td><td>0.4972</td><td>0.9842</td><td>0.1880</td><td>0.9910</td><td>0.0993</td><td></td><td>0.9934 0.0884</td><td>0.9897</td><td>0.0997</td><td>0.9928</td><td>0.0924</td><td>0.9969</td><td>0.0614</td></tr><tr><td colspan="2">Running Time (s)</td><td></td><td>0.1560</td><td></td><td></td><td>70.3521</td><td></td><td>2.3241</td><td></td><td>2.5247</td><td></td><td>1.2345</td><td></td><td>0.1305</td></tr></table>

Targets #1 and #2. Furthermore, Fig. 5(h) demonstrates that RDLR-Net provides superior results, with interference and noise on the RD plane completely filtered out. This is because RDLR-Net can adaptively suppress interference, providing precise target information.

Next, a numerical analysis of the simulation results is conducted to further quantitatively evaluate the efectiveness of the proposed method. Table IV provides a numerical comparison, showing the SSIM and RMSE values of the time-domain results for diferent methods under SINR levels ranging from –20 to –5 dB. The impact of varying interference signal strengths on the target signal is evident in the presence of interference. For WDM, the SSIM reaches 0.9842 at an SINR of –5 dB, while the RMSE drops to a minimum of 0.1880. Similar to the RD results in Fig. 5, the SALSA-based method consistently outperforms WDM in terms of numerical results across diferent SINR levels. RDLR extracts target information in a multidimensional and synchronous manner. The results indicate smaller deviations from the reference signal, with optimal SSIM and RMSE values reaching 0.9928 and 0.0924, respectively. Some artifacts in the results of FUAS-Net and BCD-DS lead to slightly inferior numerical performance compared to RDLR. RDLR-Net more efectively suppresses interference, particularly low-energy artifacts around the target, achieving optimal results with an SSIM of 0.9927 and an RMSE of 0.0930 even at an SINR of –20 dB. In terms of runtime, the WDM algorithm has low computational complexity, requiring only 0.1560 s. The salsa-based method and FUAS-Net need to process each chirp individually, consuming significant runtime. Similarly, the CS-based RDLR and BCD-DS can directly handle multichirp matrices, taking only 1.2345 and 2.5247 s, respectively. RDLR-Net leverages the large-scale parallel computing capability of RDLR, processing one frame of data in just 0.1305 s, significantly improving interference suppression eficiency.

![](images/f6683f57885d170fa5a34768127b67cb321a52710770148d901db7bcc3dfe014.jpg)

(a)  
![](images/f9aefb3298cccda372f9b98ac2aca797ffffee43574416c97a7010343e6586db.jpg)  
(b)  
Fig. 6. Detection results of simulation experiment for uniform targets. (a) and (b) show the detection probability and probability of false alarm under diferent SINR conditions, respectively.

Furthermore, we employed the CFAR detector to perform target detection on the multiframe interference suppression results under diferent SINRs. To validate the stability and robustness of the proposed method, we also conducted multiple Monte Carlo experiments. Each experiment randomly selected 150 frames of data for target detection, and the relevant results are shown in Fig. 6. As illustrated in Fig. 6(a), interference indeed has a significant impact on the detection probability. As the SINR increases, all methods exhibit overall improvements in both $P _ { D }$ and $P _ { f a } .$ When SINR is below –5, each 5-dB increase in SINR leads to significant performance enhancement across all methods. However, when SINR reaches or exceeds –5 dB, the performance tends to stabilize, indicating that interference has minimal impact on each method under these conditions. However, the proposed method, leveraging its target extraction capability, achieved the optimal detection probability $P _ { D }$ and false alarm probability $P _ { f a }$ of 97.40% and 1.84e<sup>-6</sup>, respectively.

TABLE V  
RADAR PARAMETER SETTING IN THE SCENARIO WITH MOVING CLUTTER
<table><tr><td>Parameters</td><td>DR</td><td>AR</td></tr><tr><td>Carrier Frequency (GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth (MHz)</td><td>1058</td><td>970</td></tr><tr><td>Chirp Duration (µμs)</td><td>34</td><td>24</td></tr><tr><td>Chirp rate (MHz/µs)</td><td>31.12</td><td>40.456</td></tr><tr><td>Range (m)</td><td>0</td><td>6</td></tr></table>

2) Experiment for Weak Target: In this section, we primarily investigate the performance of the proposed method in extracting weak targets within an interference environment. Two targets are set up: a stationary strong Target #1 located at a distance of 20 m and a weak moving Target #2 traveling at 5 m/s with a distance of 30 m. The two targets exhibit significantly diferent scattering coeficients. Additionally, three ARs are deployed, with their parameters detailed in Table III. Fig. 7 presents the results of the experiment for weak targets. As shown in Fig. 7(a), without interference, the energy diference between the two targets in the RD map is 32 dB. When interference occurs, the RD map is overwhelmed by high-power energy, significantly afecting target detection. Fig. 7(c) shows the results of the proposed method without incorporating TCR, i.e., directly solving (7) using ADMM. The results indicate that compared to Fig. 7(a), the energy of Target #2 is not efectively preserved. In contrast, as shown in Fig. 7(d), the proposed method successfully retains the energy of Target #2, demonstrating the capability of TCR in extracting weak targets.

3) Experiment in the Scenario With Moving Clutter: To validate the performance of the proposed method in suppressing interference and accurately extracting targets in dynamic clutter scenarios, we simulated foliage micromotion efects by generating 100 randomly distributed scatter points at 9 m from the DR to emulate leaf clusters [63]. Besides, the simulated foliage exhibited an oscillatory motion with 0.1-m amplitude at 0.1–0.3-Hz frequency. Two targets were configured at 12.8 m (stationary) and 6.2 m (moving at 4.2 m/s), respectively, along with an AR whose parameters are detailed in Table V.

Fig. 8 presents the results for the moving clutter scenario. When no interference or clutter is present, both targets are clearly visible. However, when clutter and interference are introduced, both targets are significantly afected. Notably, the foliage-generated dynamic clutter completely covers the full Doppler region at ranges of 8–12 m. As shown in Fig. 8(c), the performance of the WDM method is unsatisfactory, demonstrating that the clutter still causes substantial interference. In contrast, consistent with the aforementioned simulation results, the proposed method remains unafected by the dynamic clutter, successfully extracting both targets while efectively suppressing the interference.

## D. Measured Experiment

We conduct a series of measured experiments to comprehensively validate the efectiveness of the proposed method. To meet the diverse scenario requirements, we divide the experiments into Scenarios A–E. Additionally, the target types, target locations, and radar parameter settings vary across the scenarios. The measured data comprise 128 chirp signals, each containing 512 sampling points.

![](images/c9716983a11e51710e425b584f68c5f2b8753b1f440f6753cb27235eaf92d219.jpg)  
(a)

![](images/0d2b8394fa3ab0770eeafe013cdcb81afc118716b35ec4f7e804e6b8a94d90db.jpg)  
(b)

![](images/42fc307bd5c004d9efaf2004e65af201d9eefac668a458d50582db01d7682f18.jpg)  
(c)

![](images/73e899acb86ef5cd2a48d766abcda7a9a35925df57d1c720c5ac4e63b2f292cf.jpg)  
(d)

Fig. 7. Results of the simulation experiment for weak target at the SINR of -15 dB. Where (a) without interference, (b) with interference, (c) without TCR, and (d) RDLR-Net.  
![](images/2d768b407ed49e210b09db5146a654185db5c7fbfefd8071d68b7b56bffcc448.jpg)  
(a)

![](images/737f86793a88be775660ec35913b32d957143ac4429141f29714199d108803c8.jpg)  
(b)

![](images/c47f7d79a8803fdc5ed02227650de6d3908dc21c08a3beae1cc1dd5430079a73.jpg)  
(c)

![](images/313575e7be2a6668bb2b48125f887a2f8abf20375b2f63f49bafa8c43d7cd6ce.jpg)  
(d)

Fig. 8. Results of the simulation experiment in the scenario with moving clutter. Where (a) without interference, (b) with interference and moving clutter, (c) WDM, and (d) RDLR-Net.  
![](images/8622adec501a5342401fd3b8ef057abaa0b3a4525971a2112694cd7f2f26a988.jpg)  
Fig. 9. Experimental setup for Scenario A.

TABLE VI  
PARAMETER SETTING OF SCENARIO A
<table><tr><td>Parameters</td><td>DR</td><td>AR#1</td><td>AR#2</td></tr><tr><td>Carrier Frequency (GHz)</td><td>77</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth (MHz)</td><td>823</td><td>750</td><td>910</td></tr><tr><td>Chirp Duration (µs)</td><td>54.46</td><td>41.52</td><td>10.2</td></tr><tr><td>Chirp rate (MHz/µs)</td><td>15.06</td><td>18.06</td><td>35.91</td></tr><tr><td>Transmitted Power (dBm)</td><td>13</td><td>12</td><td>13</td></tr></table>

1) Scenario A: Subsequently, we conduct a more complex experiment in Scenario A to further validate the efectiveness of the proposed method. As illustrated in Fig. 9, a TI AWR2243 is employed as the DR for target detection, with a TI MMWCASRF-EVM and TI AWR1443, respectively, serving as ARs, designated as AR#1 and AR#2, positioned 14 and 5 m from the DR. Additionally, two targets are configured: a stationary green electric vehicle (Target #1) located 13.8 m from the DR and a gray vehicle (Target #2) moving from point $P _ { 1 }$ along a blue trajectory, positioned 19 m from the DR. The experimental parameters for Scenario A are listed in Table VI.

TABLE VII  
TARGET DETECTION RESULTS FOR SCENARIO A
<table><tr><td colspan="2">Interference</td><td colspan="2">FUAS-Net</td><td colspan="2">BCD-DS</td><td colspan="2">RDLR-Net</td></tr><tr><td> $P _ { D }$ </td><td> $P _ { f a }$ </td><td> $P _ { D }$ </td><td> $P _ { f a }$ </td><td> $P _ { D }$ </td><td> $P _ { f a }$ </td><td> $P _ { D }$ </td><td> $P _ { f a }$ </td></tr><tr><td>45.4% 1.99e-3</td><td></td><td>94.4%4.62e-5</td><td></td><td>93.79%4.82e-5</td><td></td><td></td><td>95.92% 3.17e-6</td></tr></table>

Fig. 10 presents the experimental results for Scenario A. In the absence of interference, both targets are accurately detected, although some static clutter appears in the 0-m/s speed profile. When interference is introduced, the RD map is significantly degraded, making target detection challenging. With the WDM method, interference around Target #2 is suppressed; however, Target #1 remains obscured by interference signals. The SALSA-based method achieves partial interference suppression, but residual background noise in the RD map may lead to false alarms. FUAS-Net efectively extracts the target, but some stripe-like artifacts remain. As shown in Fig. 10(f), the interference in the BCD-DS results is partially suppressed. However, the optimal hyperparameters corresponding to each chirp may be diferent, and some residual artifacts are still present. As shown in Fig. 10(g) and (h), the proposed RDLR-Net efectively learns the latent features of target signals. Even when faced with multiple AR systems, it adaptively suppresses interference and demonstrates superior performance.

To facilitate CFAR detection, we manually annotated the position indices of Targets #1 and #2 within the range and velocity bounds highlighted in the RD map of Fig. 10, serving as the ground truth labels for detection. For visually comparing the detectability of Target #2 before and after interference suppression, we selected 200 consecutive frames starting from moment $P _ { 1 }$ as an input to the CFAR detector. As illustrated in Fig. 11, the detection results are represented by binary values (1 for successful detection and 0 for missed detection). The experimental results reveal that before interference suppression, Target #2 remained undetected in most time frames. In contrast, postsuppression detection probability demonstrates significant improvement. In addition, we conducted Monte Carlo experiments by performing three independent trials, each involving 150 randomly selected frames for CFARbased target detection. The experimental results are shown in Table VII. The proposed method achieves the highest average $P _ { D }$ and $P _ { f a } ,$ , respectively, 95.92% and $3 . 1 7 \mathrm { e } ^ { - 6 }$ . This performance enhancement indirectly validates the efectiveness of the proposed method in interference suppression while maintaining target detectability.

![](images/3a7841d81fc1894c2c881d8465099b80fe20336a3e63afb505635bac92004974.jpg)  
(a)

![](images/a041a10b2ab295058b83fb0f3faebca229fa3eef2095580b00aeb310050655c6.jpg)  
(b)

![](images/292781465b7250a44c5d3a306572a6b98edc083772da3ffc231e92ac6200d4df.jpg)

![](images/b96d09fbd2d1d4eccb29960a2a9853af201044f4063f835a7a7886ce619ba1ac.jpg)

![](images/931f1237edc6a67cb0ffa1bef21a03882dc791562bb6793dc0ceaf44a7850309.jpg)  
(e)

![](images/a0bdf341e676b4541ce063ee49942e5665746d1f4c607c72e53cb5f2f8434f6a.jpg)  
(f)

(c)  
(d)  
![](images/6295bd4fc4e9aed45908266157af6af78dcce75654e0c03e7b6358bffe61eb78.jpg)  
(g)

![](images/5a918968209f5a7ac2f4e6d26d9928d3b02b2c3b869af990082b4472e1c98077.jpg)  
(h)

Fig. 10. Results of the measured experiment in Scenario A. Where (a) without interference and noise, (b) with interference, (c) WDM, (d) SALSA-based method, (e) FUAS-Net, (f) BCD-DS, (g) RDLR, and (h) RDLR-Net.  
![](images/f6fec638da949f5f9afb347eb4f9a459986fb149ad5f27f60560cb97542ee3b0.jpg)  
Fig. 11. Detection status for Target#2 in Scenario A.

![](images/270c89551d554ddc388f28560389a01e16148ebeccc59d729eae74f6a17ecbdc.jpg)  
Fig. 12. Experimental setup for Scenario B.

TABLE VIII  
PARAMETER SETTING OF SCENARIO B
<table><tr><td>Parameters</td><td>DR</td><td>AR</td></tr><tr><td>Carrier Frequency (GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth (MHz)</td><td>858</td><td>728</td></tr><tr><td>Chirp Duration (µs)</td><td>58.72</td><td>38.42</td></tr><tr><td>Chirp rate (MHz/µs)</td><td>14.61</td><td>18.94</td></tr><tr><td>Transmitted Power (dBm)</td><td>13</td><td>13</td></tr></table>

2) Scenario B: Based on Scenario A, we experimented with Scenario B to better reflect real-world conditions. The experimental setup for Scenario B is shown in Fig. 12, where two targets were defined: a stationary gray car (Target #1) and a pedestrian (Target #2) moving at a speed of 3 m/s. Due to the significant diference in scattering characteristics between the pedestrian and the gray car, this experiment also serves to validate the efectiveness of the proposed method in detecting weak targets. Two AWR 2243 radars were used in the experiment as DR and AR. In contrast to the previous scenario,

(c)

(b)

(d)

![](images/c28ec0b298cc9be35dcfa4fa352b5ad70071ffd2e3e1ce6f0d9e5a8f94831bd2.jpg)  
(a)

![](images/6ba9e26d8bb7ad7b9f1ebcf4be6d74f6480a71898a390700f431865f049e2264.jpg)

![](images/d802fa6bcfe30a887c081c8624bff7d474e84aa11cb45b9872229022b2bc99cc.jpg)

![](images/dbdbc6e1ed0b0f51f818541f30f0625422bbddd25bc6e2943b051eeefd5b1fc1.jpg)

![](images/63b89ba78680a19c11ad1473c43ef11c1adf14957e141245cfea8b414017a621.jpg)  
(e)

![](images/f917309f13115053361b34044e3e5aad226c87bd970a444b40ddd475f6992875.jpg)

(f)  
![](images/049324817a26e676eb501234359d3476c61d59e699ac2783f45d85daef25cda6.jpg)

![](images/100a82baf80db206155b7d120846eeee3972951d5aa1d4ba1a395121b5c2cef0.jpg)  
Fig. 13. Results of the measured experiment in Scenario B. Where (a) without interference, (b) with interference, (c) WDM, (d) SALSA-based method, (e) FUAS-Net, (f) BCD-DS, (g) without TCR, and (h) RDLR-Net.

the AR was deployed directly on Target #1 to simulate a more realistic situation. The distances between DR and Targets #1 and #2 were 7 and 13.6 m, respectively. Additionally, the DR is closer to Target #1 than to Target #2, further emphasizing the power diference between the two targets. The experimental parameters are shown in Table VIII.

Fig. 13 presents the experimental results for Scenario B. As shown in Fig. 13(a), when AR is disabled, two targets are successfully detected with their range and velocity information consistent with the experimental setup, while some static clutter is observed at zero-Doppler. In Fig. 13(b), when the AR is activated, Target #1 is completely overwhelmed by highenergy interference, and the information for Target #2 becomes blurred. As illustrated in Fig. 13(c), although WDM efectively reduces the overall interference energy on the RD plane, the presence of numerous clutters in the measured scenario, coupled with the sensitivity of wavelet transform to such clutters, makes it challenging to clearly distinguish between the two targets. Fig. 13(d) presents the results obtained using the SALSA-based method, where interference is partially suppressed. However, residual artifacts remain on the RD plane, indicating that the chosen set of hyperparameters for the SALSA method may not be the optimal solution for all chirps within a single frame of data. As shown in Fig. 13(e), similar to the simulation results, FUAS-Net exhibits horizontal artifacts due to its independent processing of each chirp, which reduces interchirp correlation. BCD-DS successfully extracts Target #1 but introduces false targets near Target #2. Fig. 13(g) shows the results of the proposed method without TCR, where the energy of Target #2 is significantly weaker compared to Fig. 13(i) (with TCR included). This demonstrates TCR’s critical role in enhancing weak target detectability. Fig. 13(h) and (i) further reveals that the proposed RDLR-Net outperforms other methods by adaptively suppressing interference without introducing artifacts. Notably, the extracted target information, for both strong and weak targets, remains highly consistent with interference-free conditions.

![](images/1c7f74c09bb23b0ef6c8b39f99f4e81a1948aece0902067d612f54c629807677.jpg)  
Fig. 14. Experimental setup for Scenario C.

TABLE IX  
PARAMETER SETTING OF SCENARIO C
<table><tr><td>Parameters</td><td>DR</td><td>AR</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>1058.00</td><td>819.69</td></tr><tr><td>Chirp Duration(µs)</td><td>34.13</td><td>20.47</td></tr><tr><td>Chirp rate(MHz/µs)</td><td>30.99</td><td>40.02</td></tr><tr><td>Transmitted Power (dBm)</td><td>13</td><td>13</td></tr></table>

3) Scenario C: In the previous experiments, the ARs were always stationary. This experiment will explore the performance of the AR in a moving scenario. As shown in Fig. 14, we have set up two targets: Target #1 is a corner reflector located 10 m from the DR; Target #2 is a gray car approaching the DR at a speed of 2–3 m/s. The AR is also mounted on

![](images/cb3b44b1e73ccfd48cb6f092c7d74b0b62a7b35388691a9231684f62028de210.jpg)

![](images/619b51c652742a47c7ec5bbce7ecfba573bafe8f77c4a16780b09a97de56b194.jpg)

![](images/cb847ff9d0b543e42ff402dd8dd02c67706cbbf86f10d6f91c8a44726b383098.jpg)  
(e)

![](images/62803c5e3c4f74efaf324d0d5c8577c0406afea6b4e4f012ae97244960732a7e.jpg)  
(f)

![](images/3277b61b95e07d928cb1b3e05353d19ed27aff57f657a01dff18051fca0b036f.jpg)

![](images/4bbcb7637ccbe9866ef88909a9df81dba60615efa42239fcb72ef02549b9312f.jpg)  
(g)

![](images/31abb76423b38a96a05b3521215946cc86634cdea4546ce71cf7fb5b013eb45f.jpg)

![](images/913cac69755904cdf223792456cb1dd2080deec54b9ef1a962a17583830b7fd8.jpg)  
(h)

Fig. 15. Results of the measured experiment in Scenario C. Where (a) without interference, (b) with interference, (c) WDM, (d) SALSA-based method, (e) FUAS-Net, (f) BCD-DS, (g) RDLR, and (h) RDLR-Net.  
![](images/b01d058f2d02753f194f64d83faa571882e15770bc29f1aad1a59594b039697c.jpg)  
Fig. 16. Experimental setup for Scenario D.

Target #2. The relevant radar configuration parameters are listed in Table IX.

Fig. 15 illustrates the experimental results for Scenario C. In the absence of interference, Target #1 can be identified, while Target #2 moves at a velocity of –2.2 m/s to a position 15 m away from the DR. Additionally, static clutter remains present in the 0 m/s Doppler profile. When the AR system is activated, Target #1 becomes obscured by interference, and the RD signature of Target #2 becomes significantly degraded. WDM partially suppresses RD-plane interference but leaves residual clutter. While FUAS-Net and BCD-DS excel over SALSA in feature extraction, both exhibit artifacts (BCD-DS retains static clutter). The proposed RDLR-Net ofers nearcomplete sidelobe suppression and environmental adaptability.

4) Scenario D: The experimental setup, depicted in Fig. 16, involves the DR and the AR, both utilizing the TI AWR2243 model, spaced 2.2-m apart. In this arrangement, the DR is tasked with identifying a drone, defined as Target #1, while the AR generates interference signals. The drone moves at a speed of around 6 m/s, traversing a high-rise platform. Furthermore, within the DR’s beam range, there is a 1.4-m-high wall (Target #2) situated 12.5 m from the DR. Detailed radar configurations for Scenario D are outlined in Table X. Furthermore, the corresponding simulation experiment was conducted under identical target configurations and radar deployment parameters as defined in Scenario D, thereby validating the performance of the proposed method under controlled conditions.

TABLE X  
PARAMETER SETTING OF SCENARIO D
<table><tr><td>Parameters</td><td>DR</td><td>AR</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>850</td><td>720</td></tr><tr><td>Chirp Duration(µs)</td><td>55.72</td><td>37.95</td></tr><tr><td>Chirp rate(MHz/µs)</td><td>15.25</td><td>18.97</td></tr><tr><td>Transmitted Power (dBm)</td><td>13</td><td>13</td></tr></table>

TABLE XI

PARAMETER SETTING OF SCENARIO E
<table><tr><td>Parameters</td><td>DR</td><td>AR</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>750</td><td>682</td></tr><tr><td>Chirp Duration(µs)</td><td>29.56</td><td>72.31</td></tr><tr><td>Chirp rate(MHz/µs)</td><td>29.30</td><td>9.94</td></tr><tr><td>Transmitted Power (dBm)</td><td>13</td><td>13</td></tr></table>

Fig. 17 presents the experimental results for Scenario D. Under without-interference conditions, while both targets are observable, the measurement results reveal streak-like clutter along the zero-Doppler axis that is absent in the simulation outcomes. This is because the measured scene contains static clutter. As demonstrated in the comparative analysis, both Targets #1 and #2 exhibit significant performance degradation under interference conditions. Specifically, Fig. 17(c) and (g) illustrates the processing results of the FUAS-Net, which successfully extracts both targets but retains residual horizontal stripe artifacts in the RD map. In contrast, Fig. 17(d) and (h) demonstrates the performance of the proposed RDLR-Net, where interference signals are precisely suppressed while preserving clear target signatures. This quantitative comparison highlights the superior interference mitigation capability of the proposed method in maintaining target visibility.

![](images/f1a07678e49fd181b6c72ef0380868d71b786b6a614c8561dc79e23e94880363.jpg)  
(a)

![](images/b9a7bcfd401a0ead2c9215e36b1d25fb8e63e8c4129daf91fc3e1f037285f565.jpg)  
(b)

![](images/be5570bc0e08ef43e80a7deb1dc4d22b31ad3cf3de9b7309e25aa3c00335dbd5.jpg)

![](images/b9303807397f0c55accacf1450a6a5064807a9314f98653ad32123bf07f280a0.jpg)

![](images/75c16c8457695c81221d12bbf909f8bad1521480bb470422df79fc9d12563727.jpg)

(e)  
![](images/f54ce70bbe69650df1c4b7ec0683eba499b258930a6c746125df445a0bf82fcd.jpg)  
(f)

(c)  
(d)  
![](images/c93a89de5ec80310069408b554f78f5fd7d5d122ad070a4b8f0cd641442297e8.jpg)  
(g)

![](images/fc219319b9b01785f851c171529a48175c090a8239544bcdb779806b75e447ae.jpg)  
(h))

Fig. 17. Results of Scenario D. Where (a)–(d) simulation results (a) without interference, (b) with interference, (c) FUAS-Net, and (d) RDLR-Net. Besides, (e)–(h) measured results under the same conditions (e) without interference, (f) with interference, (g) FUAS-Net, and (h) RDLR-Net.  
![](images/e9bd50935b45fdf68cdb8b7b2294d2d271f940e28c3fab42b21c25aa03e19c32.jpg)  
(a)

![](images/89d809478cc483d7f755c62c4c64d7122952ed30e315f639a2aa619b358acea5.jpg)  
(b)

![](images/800b7dce0e54a5874fb9cdc769ce1bafc7a68779a8686c3014d4b0658dc7731b.jpg)  
(c)

![](images/d3841f6f310b33c3b6fb90ae4a7f0a676603b9fcf06b952132e12053b812ccf8.jpg)  
(d)

Fig. 18. Results of Scenario E. Where (a) with interference, (b) ANC, (c) LRS, and (d) RDLR-Net.  
TABLE XII  
NUMERICAL COMPARISON IN MEASURED EXPERIMENT IN DIFFERENT SCENARIOS, USING SSIM, SINR, AND RUNNING TIME
<table><tr><td>Method</td><td colspan="2">WDM</td><td colspan="2">SALSA</td><td colspan="2">FUAS-Net</td><td colspan="2">BCD-DS</td><td colspan="2">RDLR</td><td colspan="2">RDLR-Net</td></tr><tr><td>Scenario</td><td>SSIM</td><td>SINR(dB)</td><td>SSIM</td><td>SINR(dB)</td><td>SSIM</td><td>SINR(dB)</td><td>SSIM</td><td>SINR(dB)</td><td>SSIM</td><td>SINR(dB)</td><td>SSIM</td><td>SINR(dB)</td></tr><tr><td>Scenario A</td><td>0.8312</td><td>16.97</td><td>0.8246</td><td>19.73</td><td>0.9379</td><td>22.37</td><td>0.9427</td><td>23.49</td><td>0.9548</td><td>29.14</td><td>0.9731</td><td>39.27</td></tr><tr><td>Scenario B</td><td>0.7815</td><td>12.58</td><td>0.8032</td><td>17.76</td><td>0.9127</td><td>19.74</td><td>0.9367</td><td>27.33</td><td>0.9317</td><td>26.08</td><td>0.9660</td><td>35.91</td></tr><tr><td>Scenario C</td><td>0.8527</td><td>23.34</td><td>0.8574</td><td>26.73</td><td>0.9531</td><td>30.74</td><td>0.9604</td><td>31.53</td><td>0.9337</td><td>26.74</td><td>0.9772</td><td>41.42</td></tr><tr><td>Running Time (s)</td><td>0.0907</td><td></td><td>45.0317</td><td></td><td>1.5035</td><td></td><td>2.1746</td><td></td><td>0.8513</td><td></td><td></td><td>0.0872</td></tr></table>

5) Scenario E: Scenario E is derived from the open-source measured data presented in [18]. The experimental setup, as illustrated in [[18], Fig. 12], involves the deployment of an DR and an AR, with a target moving at a speed of 15 m/s. The parameters of Scenario E are summarized in Table XI. Fig. 18 presents the results of Scenario E. In particular, Fig. 18(b) and (c) shows two classical FMCW interference suppression methods: the adaptive noise canceller (ANC) [18] and the low-rank solution (LRS) method [51]. The ANC successfully extracts the target and suppresses the interference, but some background noise remains. In contrast, the LRS efectively reduces the background noise; however, noticeable sidelobes appear around the target, likely due to the selected hyperparameters not being optimal for all chirp signals. Fig. 18 shows the results obtained using the proposed method, which demonstrates efective suppression of both interference and noise while accurately detecting the target.

6) Numerical Comparison: To further quantitatively compare the performance of diferent methods in various realworld scenarios, SSIM and SINR are used to provide a more comprehensive evaluation of the structural similarity and energy diference in the interference suppression results. Here, we calculate the average power of the target signal in the RD domain to obtain the SINR. Table XII presents a numerical comparison of various methods under diferent scenarios. The proposed method consistently achieves the highest SSIM and SINR values in Scenarios A–C, demonstrating superior target extraction capabilities while achieving good interference suppression. In terms of average processing time, the method leverages the parallel computation advantage of the deep feedforward network, processing each scenario in only 0.0872 s, the fastest among all methods.

## E. Comprehensive Discussion

Both simulation and measured experiments demonstrate that the existing methods can suppress interference in FMCW radar systems, as they share the same mutual interference principle. However, measured scenarios introduce additional clutter that causes temporal aliasing with interference signals in the time domain, complicating target signature extraction and requiring more robust suppression algorithms. The proposed RDLR-Net achieves superior interference suppression performance in both scenarios. For RD results, it successfully recovers target features in all cases due to its adaptive focusing capability. Nevertheless, the measured results show slightly lower performance than simulations due to uncontrollable environmental clutter. In terms of computational eficiency, RDLR-Net exhibits the fastest runtime (0.0872 s for realworld data versus 0.1305 s for simulations) owing to its parallel feedforward architecture, where the diference stems from the higher number of chirp sampling points in simulation (800 versus 512 points). Detection performance shows $P _ { D }$ of 97.4% $( P _ { f a } = 1 . 8 \times 1 0 ^ { - 6 } )$ in simulation and 95.92% $( P _ { f a } =$ $3 . 1 7 \times 1 0 ^ { - 6 } )$ in Scenario A measurements. While measured metrics are marginally lower, they still outperform the stateof-the-art methods.

## V. CONCLUSION

This article proposes a novel unsupervised target information mining algorithm, named RDLR-Net, which combines the interpretability of CS with the flexibility of deep networks to adaptively suppress mutual interference between FMCW radars. First, the interference suppression is reformulated as a microwave signal reconstruction problem with a coupled range-Doppler optimization. To efectively separate strong and weak scattering targets, a joint regularization constraint based on the $l _ { 1 }$ norm and the target capture operator is designed. Subsequently, a framework based on distributed optimization is designed and unfolded into a deep feedforward network to accelerate model training and inference. Considering the lack of labeled data and the limitations of manual parameter tuning in practical applications, an unsupervised learning strategy is employed to map the target signal inversion to the original echo with interference, completing the loss items mapping. Finally, a loss function is designed from both distance and energy perspectives to adapt to various interference distributions, thereby guiding the stable optimization of the model. Simulation and multiple measured experiments show that RDLR-Net can eficiently suppress interference, accurately extract target information, and demonstrate generalization.

Experimental results demonstrate that the proposed method achieves a processing time of 0.0872 s per frame for measured radar echoes, satisfying real-time processing requirements in known scenarios. However, the primary limitation of the proposed method lies in its dependency on network retraining when encountering novel scenarios, where emerging interference data exhibit a mismatch with pretrained models, resulting in temporal latency for processing tasks in unfamiliar environments. Current unsupervised networks still rely on training convergence to achieve cross-scenario generalization, making future research of accelerated neural network training techniques to enhance rapid model adaptation capabilities.

## REFERENCES

[1] L. Piotrowsky, T. Jaeschke, S. Kueppers, J. Siska, and N. Pohl, “Enabling high accuracy distance measurements with FMCW radar sensors,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 12, pp. 5360–5371, Dec. 2019.

[2] H. Yang, P. Lang, Y. He, X. Lu, Z. Liu, and J. Yang, “Lambda-1 detector: Adaptive interference detection in synthetic aperture radar images,” IEEE Trans. Geosci. Remote Sens., vol. 63, pp. 1–13, 2025, doi: 10.1109/TGRS.2025.3529623.

[3] X. Gao, S. Roy, and G. Xing, “MIMO-SAR: A hierarchical highresolution imaging algorithm for mmWave FMCW radar in autonomous driving,” IEEE Trans. Veh. Technol., vol. 70, no. 8, pp. 7322–7334, Aug. 2021.

[4] D.-H. Shin, D.-H. Jung, D.-C. Kim, J.-W. Ham, and S.-O. Park, “A distributed FMCW radar system based on fiber-optic links for small drone detection,” IEEE Trans. Instrum. Meas., vol. 66, no. 2, pp. 340–347, Feb. 2017.

[5] S. Ehsanfar, A. Bazzi, K. Moßner, and M. Chafii, “Hypothesis testing¨ on FMCW and OFDM for joint communication and radar in IEEE 802.11bd,” in Proc. IEEE Int. Conf. Commun. Workshops (ICC Workshops), May 2023, pp. 464–469.

[6] S. Wei, H. Zhang, X. Zeng, Z. Zhou, J. Shi, and X. Zhang, “CARNet: An efective method for SAR image interference suppression,” Int. J. Appl. Earth Observ. Geoinf., vol. 114, Nov. 2022, Art. no. 103019.

[7] J.-G. Kim, S.-H. Sim, S. Cheon, and S. Hong, “24 GHz circularly polarized Doppler radar with a single antenna,” in Proc. Eur. Microw. Conf., Oct. 2005, pp. 4–pp.

[8] Y. Yu, D. Yi, M.-C. Tang, Q. Ma, X.-C. Wei, and E.-P. Li, “Vertically polarized, electromagnetic interference suppressed millimeter-wave active heatsink antenna based on gap waveguide technology,” IEEE Trans. Antennas Propag., vol. 72, no. 1, pp. 433–444, Jan. 2024.

[9] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in Proc. IEEE Radar Conf., Apr. 2018, pp. 252–256.

[10] Z. Zheng, T. Yang, W.-Q. Wang, and H. C. So, “Robust adaptive beamforming via simplified interference power estimation,” IEEE Trans. Aerosp. Electron. Syst., vol. 55, no. 6, pp. 3139–3152, Dec. 2019.

[11] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun. 2016, pp. 1–9.

[12] G. Hakobyan, K. Armanious, and B. Yang, “Interference-aware cognitive radar: A remedy to the automotive interference problem,” IEEE Trans. Aerosp. Electron. Syst., vol. 56, no. 3, pp. 2326–2339, Jun. 2020.

[13] Y. Wang, Q. Zhang, Z. Wei, Y. Lin, and Z. Feng, “Performance analysis of coordinated interference mitigation approach for automotive radar,” IEEE Internet Things J., vol. 10, no. 13, pp. 11683–11695, 2023, doi: 10.1109/JIOT.2023.3244566.

[14] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[15] Z. Xu et al., “A novel method of mitigating the mutual interference between multiple LFMCW radars for automotive applications,” in Proc. IEEE Int. Geosci. Remote Sens. Symp., Jul. 2019, pp. 2178–2181.

[16] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[17] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[18] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[19] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 726–731.

[20] P. Wang, X. Yin, J. Rodr´ıguez-Pineiro, Z. Chen, P. Zhu, and G. Li, “A˜ dual-recursive-least-squares algorithm for automotive radar interference suppression,” IEEE Trans. Intell. Transp. Syst., pp. 1–15, 2023.

[21] Z. Xu, S. Xue, and Y. Wang, “Incoherent interference detection and mitigation for millimeter-wave FMCW radars,” Remote Sens., vol. 14, no. 19, p. 4817, Sep. 2022.

[22] B. P. A. Rohman, A. S. Satyawan, D. Kurniawan, R. Indrawijaya, C. B. A. Wael, and N. Armi, “Robust automotive radar interference mitigation using multiplicative-adaptive filtering and Hilbert transform,” Int. J. Electr. Comput. Eng. (IJECE), vol. 14, no. 1, p. 326, Feb. 2024.

[23] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[24] Z. Chen, F. Xie, C. Zhao, and C. He, “Radio frequency interference mitigation in high-frequency surface wave radar based on CEMD,” IEEE Geosci. Remote Sens. Lett., vol. 14, no. 5, pp. 764–768, May 2017.

[25] A. B. Baral, B. R. Upadhyay, and M. Torlak, “Automotive radar interference mitigation using two-stage signal decomposition approach,” in Proc. IEEE Radar Conf. (RadarConf), May 2023, pp. 1–6.

[26] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[27] R. Muja, A. Anghel, R. Cacoveanu, and S. Ciochina, “Real-time interference mitigation in automotive radars using the short-time Fourier transform and L-statistics,” IEEE Trans. Veh. Technol., vol. 73, no. 10, pp. 14617–14632, Oct. 2024.

[28] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

[29] H. Lee, S.-Y. Kwon, and S. Lee, “Restoration of automotive radar signals under mutual interference by digital in-painting,” IEEE Trans. Instrum. Meas., vol. 73, pp. 1–17, 2024.

[30] Z. Xu and S. Wei, “FMCW radar system interference mitigation based on time-domain signal reconstruction,” Sensors, vol. 23, no. 16, p. 7113, Aug. 2023.

[31] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approachbased interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[32] J.-H. Choi, H.-B. Lee, J.-W. Choi, and S.-C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Trans. Commun., vol. 99, no. 1, pp. 280–287, 2016.

[33] T. Oyedare, V. K. Shah, D. J. Jakubisin, and J. H. Reed, “Interference suppression using deep learning: Current approaches and open challenges,” IEEE Access, vol. 10, pp. 66238–66266, 2022.

[34] M. Delamou, A. Bazzi, M. Chafii, and E. M. Amhoud, “Deep learningbased estimation for multitarget radar detection,” in Proc. IEEE 97th Veh. Technol. Conf. (VTC-Spring), Jun. 2023, pp. 1–5.

[35] T.-H. Sang, K.-Y. Tseng, F.-T. Chien, C.-C. Chang, Y.-H. Peng, and J.- I. Guo, “Deep-learning-based velocity estimation for FMCW radar with random pulse position modulation,” IEEE Sensors Lett., vol. 6, no. 3, pp. 1–4, Mar. 2022.

[36] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153491–153507, 2021.

[37] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in Proc. IEEE 92nd Veh. Technol. Conf. (VTC-Fall), Nov. 2020, pp. 1–5.

[38] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for FMCW radars,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5118316.

[39] J. Wang, R. Li, X. Zhang, and Y. He, “Interference mitigation for automotive FMCW radar based on contrastive learning with dilated convolution,” IEEE Trans. Intell. Transp. Syst., vol. 25, no. 1, pp. 545–558, Jan. 2024.

[40] M. Wang, S. Wei, Z. Zhou, J. Shi, and X. Zhang, “Eficient ADMM framework based on functional measurement model for mmW 3-D SAR imaging,” IEEE Trans. Geosci. Remote Sens., vol. 60, pp. 1–17, 2022, doi: 10.1109/TGRS.2022.3165541.

[41] A. Bazzi, D. T. M. Slock, and L. Meilhac, “A Newton-type forward backward greedy method for multi-snapshot compressed sensing,” in Proc. 51st Asilomar Conf. Signals, Syst., Comput., Oct. 2017, pp. 1178–1182.

[42] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[43] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[44] S. Chen, J. Taghia, U. Kuhnau, T. Fei, F. Gr¨ unhaupt, and R. Martin,¨ “Automotive radar interference reduction based on sparse Bayesian learning,” in Proc. IEEE Radar Conf. (RadarConf), Sep. 2020, pp. 1–6.

[45] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[46] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270–5283, Dec. 2021.

[47] M. Yuan, C. Jiang, Y. Zhang, J. Bao, and C. Li, “Interference suppression for automotive millimeter-wave radars with fused lasso,” IEEE Trans. Intell. Transp. Syst., vol. 25, no. 7, pp. 7987–8002, Jul. 2024.

[48] H. Zhang et al., “Dual-domain feature-oriented interference suppression for FMCW automotive radar,” IEEE Sensors J., vol. 24, no. 5, pp. 6405–6417, Mar. 2024.

[49] Y. Wang, Y. Huang, C. Wen, X. Zhou, J. Liu, and W. Hong, “Mutual interference mitigation for automotive FMCW radar with time and frequency domain decomposition,” IEEE Trans. Microw. Theory Techn., vol. 71, no. 11, pp. 5028–5044, Nov. 2023.

[50] Z. Xu, “Bi-level l <sub>1</sub> optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, Jan. 2023.

[51] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[52] Y. Wang, Y. Huang, J. Liu, R. Zhang, H. Zhang, and W. Hong, “Interference mitigation for automotive FMCW radar with tensor decomposition,” IEEE Trans. Intell. Transp. Syst., 2024.

[53] T. Fei, H. Guang, Y. Sun, C. Grimm, and E. Warsitz, “An eficient sparse sensing based interference mitigation approach for automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 274–277.

[54] H. Zhang, S. Wei, M. Wang, Y. Hu, J. Shi, and G. Cui, “FUAS-net: Feature-oriented unsupervised network for FMCW radar interference suppression,” IEEE Trans. Microw. Theory Techn., vol. 72, no. 4, pp. 2602–2619, Apr. 2024.

[55] J. Overdevest, A. G. C. Koppelaar, M. J. G. Bekooij, J. Youn, and R. J. G. van Sloun, “Signal reconstruction for FMCW radar interference mitigation using deep unfolding,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Jun. 2023, pp. 1–5.

[56] N.-C. Ristea, A. Anghel, R. T. Ionescu, and Y. C. Eldar, “Automotive radar interference mitigation with unfolded robust PCA based on residual overcomplete auto-encoder blocks,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. Workshops (CVPRW), Jun. 2021, pp. 3203–3208.

[57] D. Oprisan and H. Rohling, “Analysis of mutual interference between automotive radar systems,” in Proc. Int. Radar Symp. (IRS), 2005, pp. 83–90.

[58] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[59] A. Bazzi and M. Chafii, “Low dynamic range for RIS-aided bistatic integrated sensing and communication,” IEEE J. Sel. Areas Commun., vol. 43, no. 3, pp. 912–927, Mar. 2025.

[60] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf. (RadarConf), Oklahoma City, OK, USA, Apr. 2018, pp. 405–410.

[61] A. De Maio, Y. C. Eldar, and A. M. Haimovich, Compressed Sensing in Radar Signal Processing. Cambridge, U.K.: Cambridge Univ. Press, 2019.

[62] D. Kim and J. A. Fessler, “Another look at the fast iterative shrinkage/thresholding algorithm (FISTA),” SIAM J. Optim., vol. 28, no. 1, pp. 223–250, Jan. 2018.

[63] P. Lei, “Comprehensive measurement and modeling in foliage environments using UHF UWB ground-based radar,” J. Electromagn. Waves Appl., vol. 33, no. 7, pp. 946–958, May 2019.