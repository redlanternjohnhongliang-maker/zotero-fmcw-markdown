# FUAS-Net: Feature-Oriented Unsupervised Network for FMCW Radar Interference Suppression

Hao Zhang , Student Member, IEEE, Shunjun Wei , Member, IEEE, Mou Wang , Yifei Hu, Student Member, IEEE, Jun Shi , Member, IEEE, and Guolong Cui , Senior Member, IEEE

Abstract— The widespread application of frequency-modulated continuous-wave (FMCW) radars leads to a significant increase in the risk of mutual interference. Conventional compressed sensing (CS)-based interference mitigation methods are limited by large computational capacity, troublesome parameter settings, and inefficient data processing. The supervised deep learning approach can overcome the above challenges; however, the measured data are hard to invert the labels. To address these problems, an effective framework, called the feature-oriented unsupervised adaptive suppression network (FUAS-Net), is proposed to suppress mutual interference between FMCW radars. FUAS-Net is mainly composed of an encoder and an interference restoration decoder. First, the signal model is constructed, and the task of interference suppression (IS) is modified into an optimization framework with regularizers. Then, the design of the encoder is inspired by approximate message passings (AMPs) by taking advantage of a priori information in the frequency domain to obtain targets. Second, the decoder is designed to complete the mapping from the target to the predicted interfered echo, alleviating the data dependency. FUAS-Net provides robust target extraction capabilities and optimizes parameters without ground truth. Finally, a novel training loss function is proposed that combines the mean square error (mse) and IS ratio (ISR) constraints to guarantee the power and sparsity of the targets. Both simulation and measured experiments validate the effectiveness of the proposed method, in comparison with existing state-of-the-art methods, and the results show that FUAS-Net can accomplish effective target extraction, expressing the potential for efficient IS.

Index Terms— Deep learning, frequency-modulated continuous-wave (FMCW) radar, interference suppression (IS), mutual interference.

## I. INTRODUCTION

accuracy for safer and simpler operation, and the all-weather and full-time characteristics allow it to perform in harsh environments, such as dense fog and dust [2]. As a result, FMCW radars are widely used for applications such as biological vitals detection, automotive radar, remote sensing target detection [3], weather forecasting [4], environmental monitoring [5], and military communications. However, FMCW radars sharing in the same carrier frequency [6] (typically 77 GHz) increase the risk of mutual interference, causing weak targets to be overwhelmed [7] and reducing target detection rates while increasing false alarm rates. Therefore, for collecting high-precision target information, it is of great significance to invest more effort in studying how to suppress interference between FMCW radars.

## A. Related Works

In recent years, the subject of mitigating FMCW radar interference has attracted the interest of many scholars around the world, leading to the emergence of a large number of methods. Early on, the transmitting and receiving antennas of the radar were set up to a specific polarization [8], avoiding the receipt of interference signals. Similarly, interference can be avoided by designing a reasonable FMCW radar transmit waveform. Uysal [9] proposed a phase-coded FMCW (PC-FMCW) system that utilizes a set of delay filters to achieve beat frequency signal alignment for interference mitigation; Xu et al. [10] based on linear FMCW to reduce mutual interference by employing a random subband spectrum technique. In [11], orthogonal waveforms were applied to suppress interference. However, the above methods place greater demands on the radar hardware [12], making it more difficult to produce radar.

Moreover, some scholars have made progress by exploiting the characteristics of the signal in the time domain [13]. Wang et al. [14] intercepted interfered regions on the time series based on the matrix-pencil principle and further reconstructed it. In [15], the Kalman filtering technique was adopted to reconstruct the time-domain signal region distorted by interference and restore the target information. Choi et al. [16] adopted the cropping and weighted envelope normalization method to remove interference in time series. Likewise, several methods are available in the frequency domain [17] to mitigate interference. A complex empirical mode decomposition (CEMD) method was proposed by Chen et al. [18] to transform the interference from the original signal into high-frequency range units and, finally, filter them out; Jin and Cao [19] proposed an adaptive noise canceller (ANC) that takes advantage of the special distribution of the positive half of the target in the frequency domain of the beat frequency signal to cancel out the negative half of the beat frequency signal with it, thus reducing the noise power around the target. Interference was also mitigated when the beat frequency signal was interpolated with a short-time Fourier transform (STFT) [20]. In addition, the interference can be extended over a wider spectrum for easy suppression [21]. Wang [22] proposed constant false alarm rate (CFAR) detector-based approaches that provide some suppression of interference. However, direct interference filtering in the frequency domain or in the time domain can, to a greater or lesser extent, result in the loss of target information.

Gradually, some scholars have made breakthroughs utilizing wavelet transforms. Lee et al. [23] extracted the interference signal from the output of the time-domain low-pass filter (LPF) by wavelet denoising. With the development of artificial intelligence technology, deep learning can also play a role [24]. Sang et al. [25] used 2-D convolutional neural networks to process the covariance matrix and chirp location information of signals extracted from regions of interest. Ristea et al. [26] presented a fully convolutional neural network that maps the time–frequency (T-F) domain of the original signal to the frequency domain of the target signal [27]. Wang et al. [28] presented a complex-valued convolutional neural network and built an end-to-end interference dataset in the T-F domain for training. However, these deep learning-based supervised training methods are more demanding on the data and lack generalization properties. In complex environments, the methods may not work well or even fail once the training data are not relevant to the scenario. To address this problem, some scholars have achieved some results in the field of radar target detection by adopting unsupervised learning without labeled data [29], [30]. In [31], unsupervised learning is used to automatically detect and localize radio frequency interference in synthetic aperture radar (SAR) images. In traditional computer vision, unsupervised learning is widely used in image denoising [32]. Based on this, Zou et al. [33] proposed a sparse recovery-based space–time adaptive processing method to suppress clutter received by radar; Jiang et al. [34] utilize an unsupervised adversarial framework to mitigate mutual interference between automotive radars. However, the principles of such methods are based on generative adversarial networks (GANs) for radar 2-D image denoising, and the methods will fail to learn target features when the noise power is too high flooding the target [35]. Therefore, it is necessary to investigate the extraction of target signals by unsupervised learning under high-power interference.

Naturally, compressed sensing (CS) [36] theory has been also applied to FMCW radar interference suppression (IS). Bechter et al. [37] first recovered the signal using sparse sampling. Chen et al. [38] estimated the posterior of the sparse representation of the signal using Bayesian learning and inferred the maximum sparse representation of the target signal by the expectation-maximization (EM) algorithm. Based on the alternating direction method of multipliers (ADMM) [39], the target was solved using the split-augmented Lagrangian shrinkage algorithm (SALSA) [40] by Uysal [41] and Uysal and Sanka [42]. Then, based on SALSA, an IS technique in the tunable Q-factor wavelet transform (TQWT) [43] domain was proposed. Based on the iterative shrinkage threshold algorithm (ISTA), Xu [44] proposed a method constrained by the $\mathrm { B i } { - } l _ { 1 }$ norm. A sparse low-rank decomposition of the Hankel matrix was constructed by lifting the measurement with ADMM [45]. These CS-based methods are good at extracting targets [46] but face difficulties such as the tedious process of tuning parameters and unsatisfactory processing efficiency. If the parameters are not set optimally, targets with weak scattering intensity may be lost [44].

In synthesis with the above discussion, the advantage of deep learning-based methods [47] lies in the adaptive IS, and correspondingly, the advantage of CS-driven methods lies in the powerful target extraction capabilities. Therefore, a suitable framework for solving targets while avoiding dependence on large amounts of data is essential. Inspired by this concept, we propose the feature-oriented unsupervised adaptive suppression network (FUAS-Net), which can utilize a priori information in the frequency domain to adaptively suppress mutual interference between FMCW radars. In summary, our innovations and contributions are outlined as follows.

1) An unsupervised learning method based on the encoder–decoder is proposed, which avoids manual annotation of data and greatly enhances the generalization performance of the network for application to interference scenarios.

2) The CS-driven encoder is designed to recover the target signal in linear measurements without interference and noise by leveraging priors in the frequency domain.

3) An interference decoder is designed to complete the mapping of the sparse representation of the target signal to the predicted interfered echo.

4) A novel loss function is proposed combining mean square error (mse) and IS ratio (ISR), which balances the target power and IS performance.

The remainder of this article is organized as follows. The signal model with interference is presented in Section II. The implementation principle of the proposed method is introduced in Section III. Section IV reports the relevant details of the simulations and the measured experiments, with the corresponding analysis of the results. Finally, a summary of the full article is given in Section V.

## II. SIGNAL MODEL WITH INTERFERENCE

In this section, we present the signal model for mutual interference of FMCW radars.

Typically, the signal ${ \bf R } _ { T } ( t )$ emitted by the FMCW radar propagates freely through space and eventually reflects from the targets, as shown in the following:

$$
\mathbf { R } _ { T } ( t ) = A _ { T } \cdot \exp \Biggl [ j \left\{ 2 \pi f _ { c } t + \frac { \pi B t ^ { 2 } } { T } \right\} \Biggr ] , \quad t \in ( 0 , T )\tag{1}
$$

where $A _ { T } , B , f _ { c } ,$ and T denote emission gain, signal bandwidth, carrier frequency, and chirp duration, respectively.

![](images/d7e3828d2a0514498c34c409efa5c53dbce0355145c3105d235e9f9c252be8ae.jpg)

![](images/9f7a89c02d1edd8b136c20dbd9c17f2b6ced97e7f3723c988d963869afe781f7.jpg)  
Fig. 1. Geometric illustration of FMCW radar interference.  
Fig. 2. RA diagram of the beat signal. (a) Without interference and thermal noise. (b) With interference and thermal noise.

The signal ${ \bf R } _ { Y } ( t )$ from the receiver of the FMCW radar subjected to interference can be indicated as

$$
\mathbf { R } _ { Y } ( t ) = \mathbf { R } _ { X } ( t ) + \sum _ { m = 1 } ^ { M } \mathbf { I } _ { m } ( t ) , t \in ( \tau , T + \tau )\tag{2}
$$

where M indicates the number of interference sources and $\mathbf { I } _ { m } ( t )$ denotes received interference signals. Besides, τ denotes the received delay. ${ \bf R } _ { X } ( t )$ represents the received target signal, which can be further expressed as

$$
\mathbf { R } _ { X } ( t ) = A _ { R } \cdot \exp \Biggl [ j \Biggl \{ 2 \pi f _ { c } ( t - \tau ) + \frac { \pi B ( t - \tau ) ^ { 2 } } { T } ) \Biggr \} \Biggr ]\tag{3}
$$

where $A _ { R }$ denotes the received gain. Moreover, $\mathbf { I } _ { m } ( t )$ can be further expressed as

$$
\begin{array} { r l } {  { \mathbf { I } _ { m } ( t ) = A _ { \mathrm { R i } } \cdot \mathrm { r e c t } ( \frac { t - \tau _ { \mathrm { i m } } - T _ { \mathrm { i m } } / 2 } { T _ { \mathrm { i m } } } ) } \quad } & { } \\ & { \times \exp [ j \{ 2 \pi f _ { c } ( t - \tau _ { \mathrm { i m } } ) + \frac { \pi B _ { \mathrm { i m } } ( t - \tau _ { \mathrm { i m } } ) ^ { 2 } } { T _ { \mathrm { i m } } } ) \} ] } \end{array}\tag{4}
$$

where rect(·) indicates the rectangular function and $A _ { \mathrm { { R i } } }$ denote interference gain. In addition, $\tau _ { \mathrm { i m } } , B _ { \mathrm { i m } } .$ , and $T _ { \mathrm { i m } }$ denote the time delay, bandwidth, and chirp duration of the mth interference, respectively. Accordingly, the geometric illustration [48] of the whole process is shown in Fig. 1.

Then, ${ \bf R } _ { Y } ( t )$ performed the complex conjugate mixing operation (called dechirping) in the analog domain, and the resulting dechirping signal ${ \bf Y } _ { D } ( t )$ can be calculated as

$$
{ \bf Y } _ { D } ( t ) = \mathcal { M } _ { c } ( { \bf R } _ { Y } ( t ) , { \bf R } _ { T } ( t ) )\tag{5}
$$

where $\mathcal { M } _ { c } ( \cdot , \cdot )$ denotes the conjugate mixer response function. Since ${ \bf Y } _ { D } ( t )$ contains high-frequency noise and spurious waves, and the beat frequency from ${ \bf Y } _ { D } ( t )$ is much smaller than B, the hardware of FMCW radar normally contains an analog LPF to limit the noise and interference duration, and the obtained beat frequency signal $\mathbf { S } _ { y }$ with interference is given as follows:

$$
\begin{array} { r } { \mathbf { S } _ { y } = \mathcal { L } _ { \mathrm { p f } } ( \mathbf { Y } _ { D } ( t ) ) } \\ { = \hat { \mathbf { s } } + \mathbf { S } _ { i } + \mathbf { S } _ { n } } \end{array}\tag{6}
$$

where $\mathcal { L } _ { \mathrm { p f } } ( \cdot )$ denotes the LPF response function. In addition, sˆ, S , and $\mathbf { S } _ { n }$ denote the target signal, the interference signal, and the system thermal noise, respectively. $\mathbf { S } _ { i }$ varies with the parameters of the ego-radar and the aggressor radar, and can be divided into the following two cases: 1) $( B / T ) = ( B _ { \mathrm { i m } } / T _ { \mathrm { i m } } )$ and 2) $( B / T ) \ne ( B _ { \mathrm { i m } } / T _ { \mathrm { i m } } )$ , or the source of the interference is CW. In response to 1), false targets will be generated, usually in the spatial domain, the strategy domain, and the encoding domain to cause the false alarm problem. However, case 1) occurs with a very low probability, generally less than 0.1% [49], [50]. If the interference is within the chirp duration of the FMCW radar, case 2) occurs. The range-amplitude (RA) diagram, which was obtained by the Fourier transform on the beat frequency signal, for case 2) is given in Fig. 2, where Fig. 2(a) shows without interference and Fig. 2(b) shows with interference and thermal noise. It is noticeable that the amplitude of the interference and noise floor rises significantly, and when the interference power increases further, it even drowns out the target. The proposed method in this article will focus on solving the problems caused by case 2).

## III. PROPOSED METHOD

In this section, we first outline a framework for integrating CS theory into IS, aiming to exploit approximate message passing (AMP) [51] to find targets. Then, combining deep learning techniques, the network structure of FUAS-Net, the unsupervised training implementation, and the loss function are introduced. Specifically, compared to traditional CS-based methods and supervised deep learning methods, difficult parameter settings and stringent training data requirements are avoided.

## A. AMP-Based Interference Suppression

The echo in (6) can be represented by the matrix, as shown in the following:

$$
\mathbf { y } = \mathbf { F } \mathbf { x } + \mathbf { i } + \mathbf { n }\tag{7}
$$

where $\mathbf y \in \mathbb C ^ { L \times 1 } , \mathbf i \in \mathbb C ^ { L \times 1 }$ , and $\mathbf { n } \in \mathbb { C } ^ { L \times 1 }$ denote the characteristic representations of $\mathbf { S } _ { y } , \mathbf { S } _ { i } ,$ , and $\mathbf { S } _ { n } ,$ respectively, with the length $L .$ Currently, much of the existing work demonstrates that, in FMCW systems, the target exhibits sparse properties in the frequency domain [41], [42], [44]. Thus, $\bar { \mathbf { F } } \in \mathbb { C } ^ { L \times L }$ denotes the normalized inverse Fourier transform (IFT) matrix, and $\mathbf { x } \in \mathbb { C } ^ { L \times 1 }$ denotes the sparse coefficient of the target. In CS-driven IS, with the introduction of the $l _ { 1 }$ norm as a constraint, (7) can be modeled as the following univariate optimization problem:

$$
\hat { \mathbf { x } } = \arg \operatorname* { m i n } _ { \mathbf { x } } \frac { 1 } { 2 } \| \mathbf { y } - \mathbf { F } \mathbf { x } \| _ { 2 } ^ { 2 } + \lambda \| \mathbf { x } \| _ { 1 }\tag{8}
$$

where $\lVert \cdot \rVert _ { 1 }$ is the $\ell _ { 1 }$ norm achieving feature sparsity for vectors and $\lVert \cdot \rVert _ { 2 }$ denotes the Euclidean norm. $\lambda \ \in \ \mathbb { R }$ controls the weights between the sparsity of x and penalty terms.

AMP as an efficient method with high convergence can be applied to solve (8) as follows:

$$
\left\{ \begin{array} { l l } { \displaystyle b _ { t } = \frac 1 L \| \mathbf { x } _ { t } \| _ { 0 } } \\ { \mathbf { v } _ { t } = \mathbf { y } - \mathbf { F } \mathbf { x } _ { t } + b _ { t } \mathbf { v } _ { t - 1 } } \\ { \displaystyle \lambda _ { t } = \frac { \alpha } { \sqrt L } \| \mathbf { v } _ { t } \| _ { 2 } } \\ { \displaystyle \mathbf { x } _ { t + 1 } = \mathcal { S } \big ( \mathbf { x } _ { t } + \mathbf { F } ^ { H } \mathbf { v } _ { t } ; \lambda _ { t } \big ) } \end{array} \right.\tag{9}
$$

where t denotes the iteration and $\begin{array} { r l r } { { \bf { v } } _ { - 1 } } & { { } = } & { { \bf { 0 } } . } \end{array}$ . Then, $\mathbf { x } _ { 0 } ~ =$ $\begin{array} { r } { \mathbf { F } ^ { H } \mathbf { y } . } \end{array}$ , where $\mathbf { F } ^ { H }$ denotes the conjugate transpose of F. In addition, α is a tuning parameter that corresponds to λ in (8) and controls the global energy threshold. Moreover, $S ( \mathbf { p } ; q )$ denotes the soft threshold function, as shown in the following:

$$
\left[ S ( \mathbf { p } ; q ) \right] _ { i } = { \frac { \mathbf { p } _ { i } } { | \mathbf { p } _ { i } | } } \operatorname* { m a x } ( | \mathbf { p } _ { i } | - q ; 0 ) , \quad i = 1 , 2 , \ldots , L .\tag{10}
$$

Among them, $\mathbf { p } _ { i }$ denotes the ith value of the vector p. In addition, |p<sub>i</sub> | denotes the amplitude of p<sub>i</sub> , and $[ \cdot ] _ { i }$ denotes the operator of extracting the ith element. The steps of AMP for FMCW radar IS are listed in Algorithm 1.

## B. Structure of FUAS-Net

Based on the analysis above, the final solution of x is, thus, the representation of the target in the frequency domain. The AMP approach, while promising to solve the problem, suffers from the problems of parameter settings and is unable to adaptively suppress interference. This is because, $\alpha$ is hardly optimal by setting, and even if it is, the process of setting is tedious; when α is suboptimal, IS is unsatisfactory. Consequently, we introduce deep learning techniques to automatically learn the hyperparameters in the CS-based method to accurately suppress interference from the input echoes. Furthermore, in the current FMCW fields, there is a lack of input-to-output interference datasets, and even when relevant datasets are available, supervised deep learning methods can only handle remote sensing scenes covered by the dataset.

Algorithm 1 AMP for Suppressing FMCW Radar Interference   
Require: Beat frequency signal y; Tuning hyperparameters   
α; IFT matrix F; Maximum number of iterations T ; Error   
value $\eta ;$   
Ensure: Final estimation target $\hat { \mathbf { x } } ;$   
1: Initialize $\mathbf { v } _ { - 1 } = \mathbf { 0 } ; \mathbf { x } _ { 0 } = \mathbf { F } ^ { H } \mathbf { y } ;$   
2: while $t \leq T$ do   
3: $b _ { t } = \frac { 1 } { L } \lVert \mathbf { x } _ { t } \rVert _ { 0 }$   
4: $\mathbf { v } _ { t } = \mathbf { y } - \mathbf { F } \mathbf { x } _ { t } + b _ { t } \mathbf { v } _ { t - 1 }$   
5: $\begin{array} { r } { \lambda _ { t } = \frac { \alpha } { \sqrt { L } } \lVert \mathbf { v } _ { t } \rVert _ { 2 } } \end{array}$   
6: $\mathbf { x } _ { t + 1 } = \mathbf { \mathcal { S } } ( \mathbf { x } _ { t } + \mathbf { F } ^ { H } \mathbf { v } _ { t } ; \lambda _ { t } )$   
7: if $\frac { \| \mathbf { x } _ { t + 1 } - \mathbf { x } _ { t } \| _ { 2 } ^ { 2 } } { \| \mathbf { x } _ { t } \| _ { 2 } ^ { 2 } } < \eta$ then   
8: $\hat { \mathbf { x } } = \mathbf { x } _ { t + 1 } ,$ break;   
9: end if   
10: end while

However, the scenarios for IS tasks are generalized, and supervised methods are insufficient to suppress interference intrinsically. To address these problems, FUAS-Net is designed to globally approximate the optimal hyperparameters for adaptive IS, and the specific implementation is described in the following. The overall framework of FUAS-Net is shown in Fig. 3(a) and mainly consists of two parts: 1) an AMP-inspired encoder for solving the problem in (8) by mapping the input time-domain signal with interference to the frequency-domain representation of the target without interference and 2) an interference decoder for mapping the frequency-domain representation of the target to the predicted interfered time-domain signal.

1) AMP-Inspired Encoder: In FUAS-Net, the encoder represents the adaptive IS operator that extracts the target x from y. Based on Algorithm 1, we construct a hierarchical network framework as the main structure of the encoder, which can learn the parameters autonomously. Fig. 3(b) gives the structure of the AMP-inspired encoder, where each layer in the encoder corresponds to one iteration in Algorithm 1. First, the update rule of v is implemented in the following way:

$$
\widetilde { \mathbf { v } } = \mathbf { y } - F _ { \mathrm { i t } } \{ \mathbf { x } \} + b _ { t } \mathbf { v }\tag{11}
$$

where $F _ { i t } \{ \cdot \}$ denotes the inverse fast Fourier transform (IFFT) operator. The update of $b _ { t } ~ \in ~ \mathbb { C } ^ { L \times 1 } ~ ( t ~ = ~ 0 , 1 , \dots , N )$ is modified as follows:

$$
b _ { t } = \sum _ { i = 1 } ^ { L } \frac { \mathrm { s i g n } ( | \mathbf { x } _ { i } | ) } { L }\tag{12}
$$

where sign(a), $a \in \mathbb { R }$ , indicates the sign function when $a \ >$ 0 returns $1 ; a = 0$ returns $0 ;$ and $a < 0$ returns −1. Moreover, the update rule for x is given in the following:

$$
\begin{array} { r l } & { \widetilde { { \mathbf x } } = F _ { s } \{ { \mathbf x } , { \mathbf v } \} } \\ & { \quad = Q _ { t } S ( { \mathbf x } + F _ { t } \{ { \mathbf v } \} , \Phi _ { t } ) } \\ & { \quad = Q _ { t } S ( { \mathbf Z } , \Phi _ { t } ) } \end{array}\tag{13}
$$

where Z is used to represent $\mathbf { x } + F _ { t } \{ \mathbf { v } \} . \ F _ { t } \{ \cdot \}$ indicates the fast Fourier transform (FFT) operator, and $F _ { s } \{ \cdot , \cdot \}$ denotes the target update operator. Besides, $Q _ { t }$ and $\Phi _ { t }$ are learnable parameters in FUAS-Net. $\Phi _ { t }$ is equal to $\lambda _ { t }$ in (9), with the difference that $\Phi _ { t }$ is optimized by data-driven in the network. The $Q _ { t }$ balances the target amplitude when excessive differences in the target amplitude of each layer output result in nonconvergence of the network and degradation of IS performance. $Q _ { t }$ is typically initialized to 1 in the network. The initial value of $\Phi _ { t }$ is typically determined by the average amplitude of $\mathbf { y }$ in the frequency domain as follows:

![](images/ad431a423893b6c3616c842aaf6101495eb63ae3ccaba70fc3c0c48f3b3ec4c4.jpg)  
Fig. 3. Structure diagram of FUAS-Net. (a) Overall framework of FUAS-Net. (b) Structure of the AMP-inspired encoder. (c) Structure of the decoder. In addition, the purple arrows indicate the message passing flow. $F _ { \mathrm { i t } }$ is explained in (11). Besides, $F _ { s }$ and $F _ { t }$ are provided in (13) to interpret.

$$
\Phi _ { t } = \mathrm { m e a n } \bigg ( \frac { | f _ { t } \{ \mathbf { y } \} | } { L } \bigg )\tag{14}
$$

where mean(·) denotes the mean value function. Furthermore, in FUAS-Net, we set $Q _ { t }$ and $\Phi _ { t }$ to vary in each layer in real time so that the network can be monitored globally according to y until convergence, allowing the network to achieve better training performance. In addition, the initial $\Phi _ { t }$ and $Q _ { t }$ can be adjusted according to the training performance. For more efficient complex-valued data processing, the rectified linear unit (ReLU) function will replace $\boldsymbol { S } ( \cdot )$ as follows:

$$
\begin{array} { r l } & { \widetilde { \mathbf { x } } = F _ { s } \{ \mathbf { x } , \mathbf { v } \} } \\ & { \quad = Q _ { t } \mathrm { m o d R e L U } ( \mathbf { Z } , \Phi _ { t } ) } \\ & { \quad = Q _ { t } \mathrm { R e L U } ( | \mathbf { Z } | - \Phi _ { t } ) e ^ { j \angle ( \mathbf { Z } ) } } \end{array}\tag{15}
$$

where modReLU(·, ·) and $\angle ( \cdot )$ denote the modReLu function [52] and the vector direction, respectively.

2) Decoder: The task of the decoder lies in the inverse mapping of x to $\mathbf { y } ^ { \dagger }$ . To fully exploit the prior information of the interference signal, according to (8), we design the decoder to cause the clean signal to be interfered with.

First, the obtained target x is transformed into the time-domain expression s

$$
\mathbf { s } = F _ { \mathrm { i t } } \{ \mathbf { x } \}\tag{16}
$$

with $\textbf { s } ~ \in ~ \mathbb { C } ^ { L \times 1 }$ playing a role as an input to the loss function. Since FUAS-Net is trained unsupervised, to allow s to approximate y to achieve network convergence with interference, the interference module (IM) is designed. IM is a linear module that maps the distributed feature representation of the target signal to the interference sample space, and the detailed implementation is shown in the following:

$$
\mathbf { y } ^ { \dagger } = \mathbf { W } _ { 2 } ( H _ { s } ( \mathbf { W } _ { 1 } \mathbf { s } + \mathbf { p } _ { 1 } ) ) + \mathbf { p } _ { 2 }\tag{17}
$$

where $H _ { s } ( \cdot )$ denotes the sigmoid response function. ${ \bf W } _ { 1 } \in \mathbf { \Sigma }$ $\mathbb { C } ^ { 2 L \times L }$ and $\begin{array} { r l r } { { \bf W } _ { 2 } } & { { } \in } & { \mathbb { C } ^ { L \times 2 L } } \end{array}$ represent the random weight matrixes. In addition, $ { \mathbf { p } } _ { 1 } ~ \in ~ \mathbb { C } ^ { 2 L \times 1 }$ and $\mathbf { p } _ { 2 } ~ \in ~ \mathbb { C } ^ { L \times 1 }$ indicate vector biases. Decoder enables FUAS-Net to learn parameters autonomously without ground truth, avoiding label data dependency.

## C. Computational Load

First, we calculate the complexity of the AMP optimization framework for IS, assuming $\textbf { x } ~ \in ~ \mathbb { C } ^ { N \times 1 }$ and $\textbf { v } ~ \in ~ \mathbb { C } ^ { N \times 1 }$

Recalling the iterative process of (9), updating the complex computational load of $\mathbf { x } , \lambda ,$ , and v can be summarized in the following way:

$$
\begin{array} { l } { { \mathrm { c o m p l e x ~ m u l t i p l i c a t i o n s : ~ } 2 N ^ { 2 } + 2 N } } \\ { { \mathrm { c o m p l e x ~ a d d i t i o n s : ~ } 2 N ^ { 2 } + 2 N - 1 . } } \end{array}\tag{18}
$$

According to (18), the complexity of AMP optimization framework is $O ( N ^ { 2 } )$ . Then, we calculate the complexity of the encoder in FUAS-Net, as it takes on the task of IS. Recalling (11) and (13), since $\Phi _ { t }$ is learnable in training, only x and v can be calculated in one layer of updates as

$$
{ \mathrm { c o m p l e x ~ m u l t i p l i c a t i o n s : ~ } } N \log _ { 2 } ^ { N }
$$

$$
\mathrm { c o m p l e x \ a d d i t i o n s : } 2 N { \log _ { 2 } ^ { N } } + 3 N .\tag{19}
$$

According to (19), the complexity of FUAS-Net is $O ( N \mathrm { l o g } _ { 2 } ^ { N } )$ Consequently, the encoder unfolded by AMP not only avoids difficult tuning but also provides less computational load.

## D. Loss Function

Since the unsupervised train is without labels, it can only continuously extract useful target information from y and then adopt x to reconstruct $\mathbf { y } ^ { \dagger }$ , which can also be regarded as the label corresponding to y. Therefore, the training strategy is designed based on IS performance and target power. The mse loss $\mathbf { L } _ { \mathrm { M S } }$ is applied to predict the distance between y and $\mathbf { y } ^ { \dagger }$ as defined in the following:

$$
\mathbf { L } _ { \mathrm { M S } } = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \left\| \mathbf { y } _ { k } ^ { \dagger } - \mathbf { y } _ { k } \right\| _ { F } ^ { 2 }\tag{20}
$$

where $\lVert \cdot \rVert _ { F }$ denotes the Fibonacci norm. (·) and K represent the kth set of training data and the number of datasets, respectively. In addition, we introduce the inverse of ISR [53] into the training strategy to control the interference and noise power for optimizing x, as shown in the following:

$$
\mathbf { L } _ { \mathrm { S I } } = { \frac { \| \mathbf { s } _ { k } \| _ { F } ^ { 2 } } { \| \mathbf { y } _ { k } \| _ { F } ^ { 2 } } }\tag{21}
$$

where $\mathbf { L } _ { \mathrm { S I } }$ indicates suppression interference loss. Therefore, the global MSI loss can be expressed as follows:

$$
{ \bf L } _ { \mathrm { M S I } } = { \bf L } _ { \mathrm { M S } } + \beta { \bf L } _ { \mathrm { S I } }\tag{22}
$$

where $\beta$ is a tunable parameter that balances target signal fidelity and power. $\mathbf { L } _ { \mathrm { M S I } }$ cleverly links $\mathbf { y } , \mathbf { y } _ { k } ^ { \dagger } ,$ , and s in Fig. 3 to act as a tradeoff in unsupervised training. Moreover, the gradient of $\mathbf { L } _ { \mathrm { M S I } }$ is given in Appendix A.

## E. Complex-Valued Data Processing

FMCW radar data are complex-valued; therefore, the processing of data by FUAS-Net should take into account the complex values. From the above analysis, it is impossible to avoid the addition and multiplication of complex-valued matrices and vectors. In particular, extra attention should be paid to the multiplication, given the vectors $\eta \in \mathbb { C } ^ { R \times 1 }$ and ϑ ∈ $\bar { \mathbb { C } } ^ { S \times 1 }$ , and the matrix $\boldsymbol { \theta } \in \bar { \mathbb { C } } ^ { R \times S }$ , which can be decomposed as

$$
\left[ \begin{array} { c } { R ( \eta ) } \\ { I ( \eta ) } \end{array} \right] = \left[ \begin{array} { c c } { R ( \theta ) } & { - I ( \theta ) } \\ { I ( \theta ) } & { R ( \theta ) } \end{array} \right] \cdot \left[ \begin{array} { c } { R ( \vartheta ) } \\ { I ( \vartheta ) } \end{array} \right]\tag{23}
$$

where $R ( \cdot )$ and I (·) denote the real and imaginary parts of the complex value, respectively. In the network, all vector and matrix multiplications are performed according to (23), which ensures the correct processing of complex data and the preservation of signal information.

## F. Learning Strategy

For learning strategies, unsupervised learning approaches are less data-dependent and less data-demanding. Due to the scarcity of FMCW radar interference datasets, in previous deep learning approaches [25], [26], [28], supervised training is commonly performed with labeled simulation data. However, the scenarios covered by the simulation data are not representative of the characteristics of the real-world data, and the data-driven network struggles to perform properly when processing the measured data. Thus, it appears that the unsupervised learning strategy is reasonable, and in the above, we provide detailed derivations of the equations used in the implementation of FUAS-Net. In addition, the IS results of the encoder output are not constrained by ground truth, which can greatly improve the generalization performance of the network and can be adaptive to arbitrary scenarios. At the same time, the proposed $\mathbf { L } _ { \mathrm { M S I } }$ introduces the target power as a reference, which balances the IS effectiveness and target power. In FUAS-Net, fewer parameters need to be learned, which avoids the information redundancy caused by a large number of parameters and simplifies the network structure. FUAS-Net can be trained directly on y without labels, and a well-trained network can efficiently suppress FMCW interference. In summary, the training steps for FUAS-Net are listed on Algorithm 2.

Algorithm 2 Training of FUAS-Net   
Given: Beat frequency signal y; Layer number T ;   
Output: Optimal parameters $\{ Q _ { t } , \Phi _ { t } \} _ { t = 1 } ^ { T } ;$   
1: Initialize $\mathbf { v } _ { - 1 } ; \mathbf { x } _ { 0 } ;$   
2: while $t \leq T$ do   
3: //Encoder Training   
4: $\mathbf { v } _ { t } = \mathbf { y } - F _ { i t } \{ \mathbf { x } _ { t } \} + b _ { t } \mathbf { v } _ { t - 1 } ;$   
5: $\widetilde { \mathbf { x } } = \dot { Q } _ { t } R e L \dot { U } ( | \mathbf { x } _ { t } + F _ { t } \{ \mathbf { v } _ { t } \} | - \Phi _ { t } ) e ^ { j \angle ( \mathbf { x } _ { t } + F _ { t } \{ \mathbf { v } _ { t } \} ) }$   
6: <sup>e</sup>Learn $\{ Q _ { t } , \Phi _ { t } \} ;$   
7: //Decoder Training   
8: $\begin{array} { r } { \mathbf { s } _ { t } = F _ { i t } \{ \widetilde { \mathbf { x } } \} ; } \end{array}$   
9: $\mathbf { y } _ { t } ^ { \dagger } = \mathbf { W } _ { 2 } ( H _ { s } ( \mathbf { W } _ { 1 } \mathbf { s } _ { t } + \mathbf { p } _ { 1 } ) ) + \mathbf { p } _ { 2 } ;$   
10: Calculate $\mathbf { L } _ { M S I } = \mathbf { L } _ { M S } ( \mathbf { y } _ { t } , \mathbf { y } _ { t } ^ { \dagger } ) + \beta \mathbf { L } _ { S I } ( \mathbf { s } _ { t } , \mathbf { y } _ { t } ^ { \dagger } )$   
11: Adam Optimization, Learn $\{ \mathbf { W } _ { 1 } , \mathbf { W } _ { 2 } , \mathbf { P } _ { 1 } , \mathbf { P } _ { 2 } \}$   
12: $t = t + 1 ;$   
13: end while

## IV. EXPERIMENTS

In this section, we will perform experiments on the proposed method, and the implementation details will be described in detail. The entire experiment is conducted on a platform equipped with the Intel Core i7 8700 processor (six cores and 12 threads) and an NVIDIA Quadro RTX6000 (24 GB of video memory). In addition, the FUAS-Net is implemented on the TensorFlow framework, and the adaptive moment estimation (Adam) is selected as the optimizer for the model. In addition, the β setting for $\mathbf { L } _ { \mathrm { M S I } }$ is 100, and the learning rate is set to 0.01. First, the numerical evaluation metrics are presented. Second, simulated and measured experiments are carried out to validate the performance of the proposed method compared with state-of-the-art algorithms.

## A. Numerical Evaluation Metrics

For numerical performance comparison of the different methods, the signal-to-interference plus noise ratio (SINR) [54] and the ISR will be selected as numerical evaluation metrics. SINR can be defined by the following equation:

$$
\mathrm { S I N R } = 1 0 1 \mathrm { g } \bigg ( { \frac { P _ { x } } { P _ { i } + P _ { n } } } \bigg )\tag{24}
$$

where $P _ { x } , P _ { i }$ , and $P _ { n }$ denote the effective power of the target, interference, and noise, respectively. SINR represents the ratio between the intensity of the target signal and the intensity of the received interference and noise signal, directly reflecting the IS effectiveness. A higher SINR value reflects better IS performance. In addition, ISR can be formulated as follows:

$$
\mathrm { I S R } = 1 0 \mathrm { l g } \bigg ( \frac { \| \mathbf { E } _ { y } \| _ { F } ^ { 2 } } { \| \mathbf { E } _ { x } \| _ { F } ^ { 2 } } \bigg ) .\tag{25}
$$

From the above equation, $\mathbf { E } _ { y }$ and ${ \bf E } _ { x }$ denote the echoes before and after IS, respectively. ∥·∥ indicates the Frobenius norm. ISR reflects the ability of the algorithm to mitigate strong interference. Generally, a higher ISR shows improved IS.

In addition, the signal correlation coefficient $\rho$ [45], root mse (RMSE), and power loss ratio (PLS) are employed to further evaluate the performance of the proposed method. ρ can be defined as follows:

$$
\rho = \left| \frac { \hat { \mathbf { s } } ^ { H } \mathbf { s } _ { w } } { \| \hat { \mathbf { s } } \| _ { 2 } \| \mathbf { s } _ { w } \| _ { 2 } } \right|\tag{26}
$$

where $\mathbf { s } _ { w }$ denotes the input signal and sˆ denotes the original target signal without any interference and noise. Typically, ρ ranges from 0 to 1, the closer $\rho$ is to 1, and then, the stronger the correlation between the two signals appears to be. Moreover, RMSE reflects the degree of deviation between signals and can be expressed as

$$
\mathrm { R M S E } = \sqrt { \frac { \sum _ { m = 1 } ^ { L } \mathopen { } \mathclose \bgroup \left( < \mathbf { s } _ { w } > _ { m } - < \hat { \mathbf { s } } > _ { m } \aftergroup \egroup \right) ^ { 2 } } { L } }\tag{27}
$$

where L denotes the signal length and $< \cdot >$ is the mth element of the signal. A smaller RMSE indicates a smaller deviation between signals. PLS indicates the ratio of power decrease between two signals, as defined in the following:

$$
\mathrm { P L S } = { \frac { 1 0 1 \mathrm { g } ( P _ { \mathrm { d x } } ) } { 1 0 1 \mathrm { g } ( P _ { \mathrm { d i } } ) } }\tag{28}
$$

where $P _ { \mathrm { d x } }$ denotes the decreasing power of the targets after IS and $P _ { \mathrm { d i } }$ denotes the decreasing power of the interference signal after IS. Typically, PLS less than 1 indicates that the target power loss strength is lower than the interference.

## B. Simulation Experiments

This section will be divided into two parts: point targets simulation and intensive targets’ simulation. For practical relevance, additive Gaussian white noise (AWGN) at 10-dB signal-to-noise ratio (SNR) is added to the entire system.

TABLE I  
PARAMETERS OF SIMULATION DATASET
<table><tr><td>Parameters</td><td>Ego-Radar</td><td>Aggressor Radar</td></tr><tr><td>Carrier Frequency(GHz)</td><td>[3, 10, 77]</td><td>[3, 10, 77]</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>D[1,100]</td><td>D[1,100]</td></tr><tr><td>Chirp Duration(µs)</td><td>D[5,100]</td><td>D[5,100]</td></tr><tr><td>Speed(m/s)</td><td>D[0,20]</td><td>D[0,100]</td></tr><tr><td>Number of targets</td><td></td><td>D[0,10]</td></tr><tr><td>Number of Interference</td><td></td><td>D[0,5]</td></tr><tr><td>Range of Target(m)</td><td></td><td>D[10,10000]</td></tr></table>

TABLE II

SIMULATION PARAMETERS FOR POINT TARGETS
<table><tr><td>PARAMETERS</td><td>Ego-Radar</td><td>Aggressor radar</td></tr><tr><td>Carrier Frequency(GHz)</td><td>10</td><td>10</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>600</td><td>[600, 720, 610]</td></tr><tr><td>Chirp Duration(µs)</td><td>100</td><td>[100, 100, 113]</td></tr><tr><td>Chirp Rate(MHz/µs)</td><td>6</td><td>[6.6, -7.2, 5.4]</td></tr><tr><td>Distance(m)</td><td>0</td><td>[1, 1.2, 1.5]</td></tr></table>

To verify the robustness of the method, we set the overall SINR $\displaystyle ( \mathrm { S I N R } _ { o } )$ before IS in the echo.

Due to the current lack of end-to-end FMCW radar interference data, an extensive simulation dataset has been created. FUAS-Net is an unsupervised training network, and the data contained in the dataset are all interfered echoes; therefore, there are no corresponding noninterfered echoes. The specific parameter settings for the dataset are shown in Table I, where D[a, b] denotes the uniform distribution of a to b. In addition, SINR ’s in the training set are −10, 0, and 10 dB.

First, the setting of the number of update layers needs to be considered. The effectiveness of FUAS-Net with different update layers is given in Fig. 4, where SINR, ISR, and running time are adopted as evaluation metrics. In addition, the test data are at the $\mathrm { S I N R } _ { o }$ of −20 dB; 50 Monte Carlo simulations were performed. As can be observed in Fig. 4, no results are obtained when the number of update layers is less than 3. When the number of update layers is more than or equal to 3, the interference starts to be suppressed, and the SINR and ISR tend to stabilize after the fourth update layer. Therefore, taking into account the network complexity, running time, and effectiveness of FUAS-Net, we decided to set the number of update layers to 4.

1) Point $T a r g e t s ^ { \prime }$ Simulation: First, discrete point targets simulation is carried out where three stationary targets are set up at 30, 100, and 200 m from the ego-radar. The chirp duration of the ego-radar is 100 $\mu \mathbf { S } ,$ , the bandwidth is 600 MHz, the chirp rate is 6 MHz/µs, and the speed is 0 m/s. In addition, three aggressor radars are set up, and their chirp rates are 1.1, −1.2, and 0.9 times the chirp rate of the egoradar, respectively. The corresponding parameters are shown in Table II. The time-domain diagrams before and after the interference are given in Fig. 5(a), where high-power interferences can be observed bursting out over the time series. Fig. 5(b) shows the RA diagram before and after the interference and the interference spread over the entire frequency domain almost drowning out the three targets. Fig. 5(c) and (d) shows the T-F diagrams before and after the interference, respectively, where the three targets are visible as horizontal lines, and the interferences are presented as diagonal lines. For a more visual comparison of the IS performance, Fig. 5(e) and (f) shows the T-F diagram and the RA diagram of the original target signal sˆ.

![](images/f7ee3ba9726359c808af2998eaa27bce2d58a824b8b47cb6f92ae4ed4c39d248.jpg)  
(a)

![](images/fc887db919a239d158c672b4d031c9e04cdb314e157baf45718304d7a2a80fd4.jpg)  
(b)

![](images/fad7f01da12e6e064056996f5521657f50dac93d715426bcbbf698cd87f01b8f.jpg)  
(c)

Fig. 4. Performance of FUAS-Net with different numbers of update layers. (a) ISR. (b) SINR. (c) Time.  
![](images/1015d8b7b48e836c7499d3303b71403aed448a8c9980ade4c947ed2f7fe44e94.jpg)

![](images/ef1015926ed6d1885e17ccc0eaabe24a5fb712ca5fa0254434c48e371394d272.jpg)  
(a)

![](images/9c6b2a5b47495f39ea18c21232442391e02ff5bc22bf148db3ad040b4e307573.jpg)

![](images/95d0dd1b9cf8079e96af892cffbc2f8a117e06ae0b1ee5f92071c5f245dbda35.jpg)  
(d)

(b)  
![](images/6ec43e38c00503715d1a61dc9b2b553a7e14477aaf9f3e3be7c5dd62fe731ffa.jpg)  
(e)

(c)  
![](images/8e17cf2429ba9c2f3671b1e242af59257be72467e9f792ceebc9f225eae33452.jpg)  
(f)  
Fig. 5. Results of point targets’ simulation with and without interference. (a) Time-domain diagram of with and without interference. (b) RA diagram of with and without interference. (c) T-F diagram of without interference. (d) T-F diagram of with interference. The results of (a)–(d) are added to the noise at an SNR of 10 dB. (e) and (f) T-F diagram and RA diagram of the original target signal sˆ without any interference and noise.

Next, the results of the simulation experiments are given in Fig. 6(a)–(d), where, in each subfigure, the left one is the TF result, the middle one is the time-domain result, and the right one is the RA result. In addition, Fig. 6(a) is the ANC [19], Fig. 6(b) is based on the wavelet transform method (WTM) [23], Fig. 6(c) denotes Uysal [41], and Fig. 6(d) indicates our FUAS-Net. ANC provides some IS by leveraging the distribution of the interference on negative frequencies and canceling out the positive frequency target of the echo signal as the primary channel with it. Due to the principle of the method, the T-F results of the ANC only retain the positive frequency part, but the diagonal-shaped interference remains. Besides, the time-domain results show that the amplitude of the interference signal is still much higher than that of the target. For the RA results of the ANC, there is some reduction of the interference power around the target, but the effectiveness is still not satisfactory. The WTM mitigates the interference by wavelet denoising, extracting the interference on the time domain from the LPF, and subtracting it from the original signal. In terms of the RA and time-domain results, WTM performs somewhat better than ANC, with the interference power reduced to around −30 dB, but it can be observed from the TF results that the subtraction means leads to information loss in the target signal. Uysal exploits the sparsity of the interference and the target in the T-F and frequency domains, respectively, to alternatively solve them in the optimization framework. Both time-domain and RA results of Uysal are better than before IS, with interference power floating around −30 dB. However, the sparsity of the interference in the T-F domain is not very significant, and the target also shows the same sparsity in the T-F domain on the target. Thus, in the T-F results, Uysal interference still exists, and the targets are faded in the interference part. FUAS-Net adaptively solves the target utilizing the prior information in the frequency domain. For time-domain and T-F results, the interference on the time series is completely filtered out. For the RA results, the three targets appear clearly, and the interference power is suppressed to levels below −50 dB.

![](images/195f7be0703c807ff8e6853ffbba6cb6fe4ac9eabcbeda57013760ea3bdc88d0.jpg)

![](images/3075301c94425898b4d8cdae2d02a9657770e9a7af833ff63361836f68fae9f7.jpg)

![](images/7f415aab830ad24b72cc1487bdd155f2dcc9a9a0c8549db9560665a174281447.jpg)

(a)  
![](images/e64416624081b31b26ef66dca89cc01c30049756e48adb694c479ad4c6e1cd94.jpg)

![](images/33c734561d3bc7697ce6a87976216c27166ef75ea22df9083fa40876a66a4a02.jpg)

![](images/9a53dd05b8b6c1d21f8e63dcaa5b540faa0f3a9b5a8430f3fd8c9301fcad8302.jpg)

![](images/29b3df97bc09c6fdd2c90db967377bfe2cb23a6f4aa87133bf61a2238f5b3245.jpg)

(b)  
![](images/8986e5d9e293be5a7b3f354c4c3bb038d0fe2c31cca4728bde086597fa8539a4.jpg)  
(c)

![](images/e3dec729cef1678f7985a54b2c9067fb8becb5ad31462f20fa615a8729ebbd4c.jpg)

![](images/e1c8011d008e6c71b76d38264233b4be7a7e9b99576d9fe0636bfd04ffae6337.jpg)

![](images/f0224513d1425f7c60893846831754cd0cd0410809da6a40361af3a8c9bd29c4.jpg)  
(d)

![](images/a5b1324d44426569c1ef6a6671a028ad7ab052ea7e5ed01a285d49435e3d8056.jpg)  
Fig. 6. Comparisons of point targets’ simulation at the SINR<sub>o</sub> of −20 dB. (a) ANC. (b) WTM. (c) Uysal. (d) FUAS-Net. In each subfigure, the left one is the TF result, the middle one is the time-domain result, and the right one is the RA result.

TABLE III  
NUMERICAL COMPARISONS IN SIMULATION EXPERIMENT WITH DIFFERENT OVERALL SINRS USING ISR, TIME, AND SINR
<table><tr><td rowspan="2">Methods</td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } { - } 2 0 \ \mathrm { d B }$ </td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } { = } { - } 1 5 \ \mathrm { d B }$ </td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } { = } { \bf - } 1 0 ~ \mathrm { d B }$ </td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } 0 \ \mathrm { d B }$ </td><td colspan="2"> $\mathrm { S I N R } _ { o } { = } 1 0 ~ \mathrm { d B }$ </td><td rowspan="2">Time(s)</td></tr><tr><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td></tr><tr><td>ANC</td><td>-8.64</td><td>11.09</td><td>-9.13</td><td>12.21</td><td>-2.41</td><td>12.32</td><td>1.88</td><td>5.69</td><td>11.32</td><td>8.67</td><td>0.081</td></tr><tr><td>WTM</td><td>-7.11</td><td>21.35</td><td>-7.88</td><td>23.46</td><td>0.81</td><td>13.36</td><td>0.75</td><td>0.53</td><td>10.56</td><td>5.43</td><td>0.097</td></tr><tr><td>Uysal</td><td>0.47</td><td>22.34</td><td>0.81</td><td>24.66</td><td>1.01</td><td>24.56</td><td>2.81</td><td>26.45</td><td>13.48</td><td>5.28</td><td>0.392</td></tr><tr><td>FUAS-Net</td><td>14.34</td><td>48.02</td><td>16.15</td><td>49.37</td><td>18.96</td><td>52.94</td><td>20.47</td><td>53.81</td><td>22.45</td><td>54.37</td><td>0.158</td></tr></table>

Range Doppler (RD) is a necessary way to evaluate the performance of each method, which is obtained by performing FFT operations both within and between chirps, where the velocity resolution $V _ { R }$ can be expressed as

$$
V _ { R } = { \frac { c } { 2 f _ { c } \times T \times N _ { c } } }\tag{29}
$$

where $N _ { c }$ denotes the number of chirps. Therefore, the velocity grid on the RD map can be divided into $N _ { c } \times V _ { R } / 2 :$ $V _ { R } ~ : ~ ( N _ { C } - 1 ) ~ \times ~ V _ { R } / 2 .$ . The RD results for each method are given in Fig. 7, and each method sets the same energy display threshold, where Fig. 7(a) shows the RD diagram of without interference, Fig. 7(b) shows the R-D diagram of with interference, Fig. 7(c) shows the ANC, Fig. 7(d) shows the WTM, Fig. 7(e) shows the Uysal, and Fig. 7(f) shows the FUAS-Net. From Fig. 7(a) and (b), it can be seen that the high-power interference raises the false alarm rate, with the interference causing the loss of target information.

![](images/e2294a3bbdeda52d9997e2b7b9f74fb63e1e5e4554c14bbb3130f4e7952ffa41.jpg)  
(a)

![](images/65761b1600f4a73ed2ff40f39c22b008d480435201b1be802448cbaaab8a469a.jpg)

![](images/fffb17cc2d6b8a0870fa516b39e0f5c457cefd03c1eeb0cb6cefaec981ee5388.jpg)  
(b)  
(c)

![](images/f5d8826aa5e3af7f52cf16c68538529f4dcff36b945d7bc46fb001d4d3b7405f.jpg)  
(d)

![](images/6678573e317e17aafc9d528321cd7c681cc0fdb922a0411e805ed0854d333f70.jpg)  
(e)

![](images/c45828f24cf4f23954bf392f62e36a8430bc842303a133999fdb0ede9a1eced4.jpg)  
(f)

Fig. 7. RD results of the point targets’ simulation. (a) RD diagram of without interference. (b) R-D diagram of with interference. (c) ANC. (d) WTM. (e) Uysal. (f) FUAS-Net.  
![](images/b84ef3fff3df90ef13a512f79f96594ff7cbfac5c5cf5a31c196df1c07256148.jpg)  
(a)

![](images/51b70b3c7860a725569e64f922351a9cd555d424aa8567f94bc31db53844768a.jpg)  
(b)  
Fig. 8. Results of intensive targets’ simulation at SINR<sub>o</sub> of −10 dB. (a) With and without interference. (b) Result of FUAS-Net.

For ANC, two of the targets are only barely observable. For WTM and Uysal, although the targets are extracted, all of them are still surrounded by interference flaps and may be treated as false targets. For FUAS-Net, both the range and velocity information of the targets are presented in the RD plots, and the interference power is reduced to extremely low levels.

TABLE IV  
SIMULATION PARAMETERS FOR POINT TARGETS
<table><tr><td>PARAMETERS</td><td>Ego-Radar</td><td>Aggressor radar</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>600</td><td>[550, 720, 560, 560]</td></tr><tr><td>Chirp Duration(µs)</td><td>120</td><td>[100, 120, 140, 80]</td></tr><tr><td>Chirp Rate(MHz/µs)</td><td>5</td><td>[5.5, 6, -4, 7]</td></tr><tr><td>Distance(m)</td><td>0</td><td>[1, 2, 3, 4]</td></tr></table>

Table III presents numerical comparisons for different SINR<sub>o</sub>. Due to the limitations of the method principle, ANC is only effective at SINR greater than 0 dB. WTM with wavelet denoising works at different SINRo, but, when SINR is greater than 0, the results are less effective than Uysal. Compared to the three methods mentioned above, FUAS-Net achieves the highest SINR in all environments, demonstrating that the encoder design with a priori information has a strong target capture capability. Moreover, FUAS-Net obtains the highest ISR values, with an effective reduction in interference power. In terms of running time, both ANC and WTM are faster but less effective. In contrast, our method achieves the best IS with an average-running time of only 0.158 s for a finite number of update layers, faster than the CS-based Uysal.

2) Intensive Targets’ Simulation: To validate the extraction capability of the proposed method for successive dense targets, we carried out this experiment, where four aggressor radars are deployed with the experimental parameters shown in Table IV. In addition, 11 targets are set up, which are distributed at uniform range intervals of 0.2 m at a distance of 50–52 m from ego-radar. This range interval is less than the range resolution of the ego-radar of 0.25 m. The corresponding results for SINR<sub>o</sub> at −10 dB are given in Fig. 2, and it can be seen from Fig. 8(a) that the interference almost swamps these continuous targets. From Fig. 8(b), FUAS-Net can sense the intensive targets and suppress the interference around the targets. It is demonstrated that FUAS-Net can also acquire intensive targets by utilizing a priori information in the frequency domain.

![](images/c5a5e91c397d7af398a231e658aeb61224736cc46e7c4914d84f2f3f96340b8e.jpg)  
(a)

![](images/461b34069158273c5535d01793f609fdf1033c218a4a01c18ac71f3787f9e564.jpg)  
(b)

![](images/e76c76ce9e73b93ad19a7d841c19ffc50dc6640b270e06b195c14455df5576db.jpg)  
(c)  
Fig. 9. Performance evaluation of the proposed method under different SINR ’s. Consider sˆ as the reference. (a) ρ value comparison. (b) RMSE value comparison. (c) PLS value comparison.

3) Performance Analysis: Based on the above point targets simulation and intensive targets’ simulation, RMSE, $\rho ,$ and PLS are adopted to further evaluate the performance of FUAS-Net; 30 Monte Carlo simulations are performed to avoid chance results. Uysal, also based on CS, performed better than the other methods in the previous analysis and was selected for further comparison with FUAS-Net. The performance at different $\mathrm { S I N R } _ { o } ^ { \cdot } \mathrm { s }$ is given in Fig. 9, and sˆ is used as the reference, where Fig. 9(a) shows the $\rho$ value comparison, Fig. 9(b) shows the RMSE value comparison, and Fig. 9(c) shows the PLS value comparison. It can be seen that the interference has a very strong effect on sˆ. The signal with interference is poorly correlated with sˆ and has a large deviation. After IS, when $\mathrm { S I N R } _ { o }$ is below 10 dB, the results of Uysal deviate more from sˆ. The FUAS-Net results are very strongly correlated with sˆ, with the highest $\rho$ reaching 0.9987 and a small deviation with sˆ. The target decreasing average power and the interference decreasing average power are analyzed several times in the RA domain under different $\mathrm { S I N R } _ { o } ^ { \ , } \mathrm { s } ,$ and finally, Fig. 9(c) is obtained. As can be seen from Fig. 9(c), the target power loss is much lower than the interference power loss for both simulations.

## C. Measured Experiments

The interference data from outdoor experiments are difficult to obtain matched end-to-end data without interference; therefore, the unsupervised learning strategy of FUAS-Net is better adapted to this situation. In the measured experiments, two AWR2243 radars from Texas Instruments (TI) are first selected as ego-radar and aggressor radar, for detecting targets and emitting interference signals, respectively, both 1.8 m away from each other. Ego-radar, with a maximum detection range of 100 m, uses a DCA1000 card to collect data to facilitate computer processing, where the ADC bit count is set to 16 bits.

TABLE V  
PARAMETERS OF THE MEASURED EXPERIMENT
<table><tr><td>Case</td><td>PARAMETERS</td><td>Ego-Radar</td><td>Aggressor radar</td></tr><tr><td></td><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td></td><td>Signal Bandwidth(GHz)</td><td>0.750</td><td>0.682</td></tr><tr><td></td><td>Chirp Duration(µs)</td><td>29.56</td><td>72.31</td></tr><tr><td></td><td>Chirp Rate(MHz/s)</td><td> $2 9 . 3 \times 1 0 ^ { 6 }$ </td><td> $9 . 9 9 \times 1 0 ^ { 6 }$ </td></tr><tr><td></td><td>ADC Sample Rate(MHz)</td><td>20</td><td>15</td></tr><tr><td rowspan="3">case#1</td><td>Number of targets</td><td></td><td>3</td></tr><tr><td>Range of targets(m)</td><td></td><td>[10.50, 18.5, 67.8]</td></tr><tr><td>Speed of targets(m/s)</td><td></td><td>[0, 4.6, 0]</td></tr><tr><td rowspan="3">case#2</td><td>Number of targets</td><td>3</td><td></td></tr><tr><td>Range of targets(m)</td><td></td><td>[10.50, 12.1, 67.8]</td></tr><tr><td>Speed of targets(m/s)</td><td></td><td>[0, 1.8, 0]</td></tr></table>

The experimental scenario is constructed around a sample house, as shown in Fig. 10. In this case, a stationary corner reflector $( T _ { 1 } )$ is placed 10.5 m from the ego-radar, and another target (T<sub>2</sub>) is in motion along the moving trajectory in Fig. 10(e). To avoid being affected by the brushwood, the ego-radar is placed at a height of 1.4 m much higher than the 0.6-m-high brushwood. In addition, the sample house $( T _ { 3 } )$ is 67.8 m from the ego-radar. Besides, we selected two cases from the whole experiment according to the position of $T _ { 2 } ,$ as shown in Fig. 10(e), where case#1: $T _ { 2 }$ is 18.5 m away from ego-radar and moving at 4.6 m/s, and case#2: $T _ { 2 }$ is 12.1 m away from ego-radar and moving at 1.8 m/s. The parameters for the measured experiment are set as listed in Table V. Besides, to better visualize the comparison, while keeping the environment uniform, we performed experiments in case#1 and case#2 without interference.

Each frame consists of 128 chirps, with 512 sample points per chirp. Due to the memory limitation of the AWR2243 radar, data were collected ten times during the experiment; each time, 3200 frames were collected; the data were saved in about 10 s intervals in between; and the whole experiment lasted more than 3 min, in which case#1 and case#2 occurred in the fourth and seventh datasets, respectively. We adopt the first three sets of data as training inputs of FUAS-Net to verify the generalization performance of the method in the same experimental scene. We find that 30% of the chirps in one frame are without interference, which allows us to observe the adverse effects of interference. Moreover, to assess the noise resistance of each method, AWGN is added to the measured data. The strength of the noise is defined as the SNR of 2, 5, 10, and 15 dB.

![](images/6c4c11ac2dde113bb729517bfc3258239df139bd07a02142846dffeaf0f68504.jpg)  
(a)

![](images/f13452216c6f2726773da9cf3c17c90f5fbe8c79634ee1543159e30553946436.jpg)  
(b)

![](images/951b12507b6c0a39a60169082abca9416aad5f05caaf369327d902197845e1b4.jpg)  
c

![](images/b4bfd988208222c31902d8dc6f7b67b2b30e311dcf1154a9196b58b82a724676.jpg)  
(d)

![](images/d27d1b197b8529aefd2f74fffc66a3ac6b6ee70bf554c5f9e2144902791e12f8.jpg)  
(e)

Fig. 10. Experimental scene. (a) Target position, where T<sub>1</sub> is the stationary corner reflector. (b) FMCW radar used for the experiment. (c) T<sub>2</sub> with a speed of 4.6 m/s. (d) T immovable sample house. (e) Top view of the experimental scene.  
![](images/c4a38fa5c170bc547ec33d5299196fec7957a2005c6fa4d3700f508a0c069334.jpg)  
(a)

![](images/f44775db278f24e0f196ee563fd8e6dadcf8f2fc9993afb23e3016c2dcd3e1ce.jpg)

![](images/769e42cec05b265d60247425b0a9b6d3b5157cf7e27131735918fee52a60dda6.jpg)  
(c)

(b)  
![](images/8a3da20ff813c05e3ad36884564d9fded451a3f1e69ada70eec6cb21d35c72d7.jpg)  
(d)  
Fig. 11. Comparison of measured experiments in case#1 with and without interference. (a) Time-domain diagram of with and without interference. (b) RA diagram of with and without interference. (c) T-F diagram of without interference. (d) T-F diagram of with interference.

For case#1, the results for each method at SNR of 10 dB are given in Fig. 11, where Fig. 11(a) shows the effect caused by interference in the time domain, where high-power interference occurs at the time series with amplitudes of −400 to 400 mV, much higher than the target signal amplitude. Fig. 11(b) shows the RA results before and after the interference, from which it can be seen that, after the interference, the noise power rises from 45 to 65 dB, almost drowning out the targets. The T-F diagrams before and after the interference are shown in Fig. 11(c) and (d), with vertical lines of interference distributed over the frequency range. The results for ANC, WTM, Uysal, and FUAS-Net are given in Fig. 12. Although ANC attenuates the interference energy, it is only effective if the target power is too high above a certain threshold of interference; therefore, for this case, ANC is not effective, and all three targets are difficult to discern. The measured environment is more complex than the simulated environment, with a lot of clutter, so it is difficult for the WTM to filter this clutter better in the time domain. For Uysal, the time-domain results show that the interference is almost suppressed; however, in the T-F results, there are several high-power artifacts, and the targets are difficult to distinguish. Correspondingly, in the RA results, there are also two false targets around $T _ { 3 }$ , increasing the false alarm rate. This is because both interference and targets are sparse in the TF domain and, thus, can lead to several weak targets being hard to separate. FUAS-Net achieves optimum performance. For the time-domain results, no interference is visible at all on the time series. For the T-F results, compared to Uysal, the targets are visible, and no other false targets appear. For the RA results, all three targets are brought up, and the noise power is silenced to a very low level.

![](images/16bc729f1321e3088e3b774e6257668cf117de59b2257a464be43924edd7469e.jpg)

![](images/7e9c6d60ca4b26b2b5dbf01aed6442192a6a1202962d3b443d5615e82148cb9a.jpg)  
(a)

![](images/389170bdae87237c4e0490628a42cafc631a1f8258ecb146297014692117dce7.jpg)

![](images/6ca0ea106e9f9e0e0150ecedd38120c98f9b473d33e4d443319110933800ddd6.jpg)

![](images/31d12b0661192fa11279fe20a8e0b3a22e9c655fad6b3bbab46a3e6f05675a53.jpg)

![](images/e61ff05c3a539fd722dc5b2f834031fb826ba56e01a3c444f2f09aa7074e2807.jpg)

![](images/9239768be86d2dd298c24300fb6714769238fce61da7e4bbc01107a141fc76d8.jpg)

(b)  
![](images/7fec5b60ee9b3fd47d2ff2b13b00c9589d1729d688699e64ad10812c9f0962c4.jpg)  
(c)

![](images/b24e45e27a0614b0db753078e5405d8da8cf81ad40818a0dcc2bbdb4891da283.jpg)

![](images/d96223588d15264c5f7b57b044e4bce63633f32caaefedc64ddb3f0f8a9efd5f.jpg)

![](images/6248acbb4fee39ddaf4586bd5990ff1dd5351d77396fe091b902f1467b571a32.jpg)  
(d)

![](images/a1ddc183b49ed960e1ce630359912607bc6c9938f1d5f471fad6ab70b07a36cd.jpg)  
Fig. 12. Comparison of measured experiments in case#1. (a) ANC. (b) WTM. (c) Uysal. (d) FUAS-Net. In each subfigure, the left one is the TF result, the middle one is the time-domain result, and the right one is the RA result.

TABLE VI  
NUMERICAL COMPARISONS IN MEASURED EXPERIMENT WITH DIFFERENT SNRS USING ISR, TIME, AND SINR IN CASE#1
<table><tr><td rowspan="2">Methods</td><td colspan="2">SNR=2dB</td><td colspan="2">SNR=5dB</td><td colspan="2">SNR=10dB</td><td colspan="2">SNR=15dB</td><td rowspan="2">Time(s)</td></tr><tr><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td><td>SINR(dB)</td><td>ISR(dB)</td></tr><tr><td>ANC</td><td>-0.59</td><td>1.87</td><td>-0.71</td><td>2.22</td><td>-0.31</td><td>2.15</td><td>-0.27</td><td>2.21</td><td>0.073</td></tr><tr><td>WTM</td><td>0.04</td><td>19.21</td><td>0.10</td><td>18.12</td><td>0.21</td><td>18.44</td><td>0.24</td><td>18.49</td><td>0.088</td></tr><tr><td>Uysal</td><td>9.73</td><td>5.51</td><td>9.81</td><td>5.43</td><td>9.89</td><td>5.65</td><td>9.84</td><td>5.59</td><td>0.291</td></tr><tr><td>FUAS-Net</td><td>16.51</td><td>41.62</td><td>17.81</td><td>39.97</td><td>17.29</td><td>38.49</td><td>17.30</td><td>38.55</td><td>0.118</td></tr></table>

![](images/20bd59dc1e3ad3a0b0208517f42f6a75317eb890e707e03ec6cdd4c3cd95b123.jpg)  
(a)

![](images/92fdeaf58f5d7fc7d5a8be22d68b23cc54a890fefa45a300b4b72e8f2ece325a.jpg)  
(b)

![](images/ab70c69382efc09a574a45a8c090d5a9e658f89ffb92a65b6112163e1b0ec85f.jpg)  
(c)

![](images/1efe8ba6613e42482d65d41151f87e3c57f1e1d312ab036aff7ea96d1209bbcd.jpg)  
(d)

![](images/3ff6f3da296a8ca1ac83518ba3eefcec9e5272afc85957fa2367977c3dc554d3.jpg)  
(e)

![](images/5c35989dd7fbfb3f0e15db6331e93d688cc38317d8d056bf0bc7358ec4788fc2.jpg)  
(f)

Fig. 13. RD results in the measured experiment in case#1. (a) Without interference. (b) With interference. (c) ANC. (d) WTM. (e) Uysal. (f) FUAS-Net.  
![](images/826e0601e686cec8b9facabe015e2e34e3b1610c737d1a1ab9f39fb79363e304.jpg)  
(a)

![](images/e5bdc0479c283275764603f33a92c174eea6001c618b495f9aa6fe18d1c4a2a5.jpg)

![](images/f1a9493d804104345c5f12786ffbeae91169836dd97d8868cb38c329e6708f8f.jpg)

(b)  
![](images/e3e3af322773a1dbd95b213da2228620647e68ca3d703978ebf99384c76c8acf.jpg)  
(d)

![](images/ce97a0ff5954e4ea1cc2ef068c9b33da1826e6667741ff5a16e9ed4142e200f9.jpg)  
(e)

(c)  
![](images/1635308658e7b3fb0d596af072d2f544882e2aed669146ba008a541cb8c8ed09.jpg)  
(f)  
Fig. 14. RD results in the measured experiment in case#2. (a) Without interference. (b) With interference. (c) ANC. (d) WTM. (e) Uysal. (f) FUAS-Net.

TABLE VII  
EXPERIMENTAL PARAMETERS IN [44]
<table><tr><td>PARAMETERS</td><td>Ego-Radar</td><td>Aggressor radar</td></tr><tr><td>Carrier Frequency(GHz)</td><td>77</td><td>77</td></tr><tr><td>Signal Bandwidth(MHz)</td><td>547.5</td><td>547.5</td></tr><tr><td>Chirp Duration(µs)</td><td>36.5</td><td>18.25</td></tr><tr><td>Chirp Rate(MHz/µs)</td><td>15</td><td>30</td></tr></table>

TABLE VIII  
PROS AND CONS OF DIFFERENT ALGORITHMS
<table><tr><td>Algorithm</td><td>Computational Complexity IS performance</td><td></td><td>Generalization</td><td>Pros</td><td>Cons</td></tr><tr><td>ANC</td><td>v√√√√</td><td> $\checkmark$ </td><td>vv√</td><td>Easy operation</td><td>Not good in strong interference</td></tr><tr><td>WTM</td><td>vvv√√</td><td>√√</td><td>√r</td><td>Easy operation</td><td>Not good with much clutter waves</td></tr><tr><td>Uysal</td><td>vvr</td><td>vvr</td><td>vvvr</td><td>Good target extraction</td><td>Parameter settings</td></tr><tr><td>BLIR</td><td>vvvr</td><td>vvvr</td><td>vvvr</td><td>Good target extraction</td><td>Parameter settings</td></tr><tr><td>FUAS-Net</td><td>vvvr</td><td>vvvvr</td><td>vvv√</td><td>Good target extraction</td><td>New scenes require retraining</td></tr></table>

![](images/d8cc812f1ca86dcf94cf811c509551df0c0e9211dd16528d7aff57ddd30b48d0.jpg)  
Fig. 15. Deployment of the experimental scene in [44].

Subsequently, we further analyze the RD results of each method in case#1, and each method sets the same energy display threshold. Fig. 13(a) shows the RD diagram when there is no interference, and although there is some noise present, the three targets are relatively obvious. Fig. 13(b) shows the RD diagram before IS, from which it can be seen that the interference almost drowns out the target, resulting in a loss of useful information. Fig. 13(c) gives the results for ANC, where the interference power is reduced, but the target is difficult to discern. Fig. 13(d) and (e) shows the results for WTM and Uysal, respectively, where all three targets appear but are accompanied by some false targets, and in addition, the velocity information for $T _ { 2 }$ is not accurately presented. Fig. 13(f) shows the RD results from FUAS-Net, where the three targets are extracted and the accurate range and velocity information is retained. In addition, all noises on the RD map are filtered out compared to before IS.

Since it is difficult to determine the SINR<sub>o</sub> from the measured data, to quantitatively assess the performance and robustness of different methods, AWGN with different SNRs is added to the measured data, and the corresponding results for case#1 are shown in Table VI. For four cases with SNR at 2, 5, 10, and 15 dB, FUAS-Net achieves the highest SNR and ISR values, where SINR and ISR are 16.51 and 41.62 dB, respectively, at the SNR of 2 dB, demonstrating that the AMP-inspired encoder is effective in suppressing interference subject to $\mathbf { L } _ { \mathrm { M S I } }$ constraint. Furthermore, under the best IS performance, FUAS-Net achieves an average running time of 0.118 s for the measured data, which is close to the fastest ANC.

For case#2, since T1 and T2 are very close to each other, for better line-of-sight observation, the top-view RD results for case#2 are given in Fig. 14, and each method sets the same energy display threshold. As can be seen from the results, when there is no interference, the three targets are visible. When with interference, the targets are flooded resulting in a loss of useful information. ANC reduces the interference power, but the targets are still difficult to observe. WTM and Uysal suppress most of the interference, but there are many false targets in the RD results, raising the false alarm rate. FUAS-Net achieves optimal IS, where interference and noise are filtered out from the RD map and the three targets are visible.

To further validate the generalization performance of the proposed method, we are very grateful to Xu [44] for providing their Bi-Level l1 Optimization-Based Interference Reduction (BLIR) algorithm and measured data. As shown in Fig. 15, both the ego-radar and the aggressor radar are AWR1642 vehicle-mounted radars, both are 4 m apart, and the ego-radar starts collecting data when an electric bicycle is traveling at approximately 5 m/s. The experimental parameters are listed in Table VII, and more details can be found in [44, Sec. III]. The corresponding RD results are given in Fig. 16, where it can be seen from Fig. 16(a) and (b) that the interference causes a large effect that overwhelms the targets. For Fig. 16(c) and (d), ANC and WTM suppress some interference on the RD maps, but the target is still difficult to observe. For Fig. 16(e), BLIR shows good results, and the target information is clearly presented. Compared with BLIR, FUAS-Net achieves the best performance with less noise on the RD map and no false targets. Finally, from the above simulation and measured experiments, combining the results and the principles of the algorithms, we have scored the computational complexity, IS performance, and generalization of each algorithm with scores ranging from <sup>✓</sup> to $\surd \ V \ V \ V$ . The pros and cons of each algorithm are summarized, as shown in Table VIII.

![](images/2cddf74cbbed7624cd2b8e3a14c7accf72b236913cf8234706f3bddebc8de318.jpg)  
(a)

![](images/44a2cecfb4a8b20a1b8b251e190e4f89a519349a618957f7f4f0f07cf7b9ee3f.jpg)

![](images/992b8dc1e594671f9ef723e5009c6b1e93e18e39ebe484bc73aaec901134fe40.jpg)

![](images/8aab5f7c62271c995dbab115909c7fa905678841733bff47acf2af920966f997.jpg)  
(d)

(b)  
(c)  
![](images/cfb61a3498c3f3ed43069d19dd448f94158dc97d9d5cf5192dc14e928dfa690b.jpg)  
(e)

![](images/dae597b3a2088bda8bcafdae3152704d3bda322a229fa2c1ce945bfeb744e2ac.jpg)  
(f)  
Fig. 16. RD results in the measured experiment. (a) Without interference. (b) With interference. (c) ANC. (d) WTM. (e) BLIR. (f) FUAS-Net.

## V. CONCLUSION

In this article, we propose an efficient feature-oriented unsupervised adaptive IS network called FUAS-Net that can perform adaptive suppression of mutual interference between FMCW radars by integrating the data-driven properties of deep learning and the advantages of CS-based interpretable optimization. FUAS-Net is an unsupervised learning model based on the encoder–decoder with powerful generalization performance, where the encoder is an AMP-inspired deep unfolding network that can recover the target signal from linear measurements with interference and noise by utilizing prior information in the frequency domain. Besides, the interference decoder, which consists mainly of the IM, maps the sparse representation of the target into the predicted interfered echo under the constraints of the system. FUAS-Net provides robust target extraction capabilities and optimizes parameters without ground truth. Moreover, the proposed loss function balances the target power and IS performance considering mse and ISR as subterms. Simulation experiments and measured experiments show that the proposed FUAS-Net can suppress interference within a short time and achieve optimal numerical results with good robustness.

The limitation of the proposed method is that, for measured experiments, if a new set of interfered data is obtained from a new scene, the encoder will fail when the network model previously learned from the last scene does not match this new set of data. Therefore, the network needs to be retrained with the interference data in the new scene until the network converges. The generalization performance of unsupervised networks in multiple scenarios also requires network training. At present, it is not possible to use unsupervised networks to immediately handle tasks in unknown environments in a short period because training takes time. Many scholars are studying the topic of accelerated neural network training, such as from the data calculation method, learning rate scaling, and other directions. In addition, if the difference in energy intensity between a strong and a weak target is too large, it is difficult for the CS-based method to recover the weak targets from the interference. We will also consider these issues in our future work.

## APPENDIX A GRADIENT OF THE LOSS FUNCTION

$\mathbf { L } _ { \mathrm { M S I } }$ is available for both complex- and real-valued data, the gradient of which can be formulated as

$$
\nabla { \mathbf { L } } _ { \mathrm { M S I } } ( \mathbf { x } ) = { \frac { \partial { \mathbf { L } } _ { \mathrm { M S I } } } { \partial \mathbf { x } } } = { \frac { \partial { \mathbf { L } } _ { \mathrm { M S } } } { \partial \mathbf { x } } } + \beta { \frac { \partial { \mathbf { L } } _ { \mathrm { S I } } } { \partial \mathbf { x } } }\tag{30}
$$

where $( \partial \Gamma / \partial \varphi )$ denotes the result of the partial derivative of $\Gamma$ for $\varphi .$ Observing the two subterms of $\mathbf { L } _ { \mathrm { M S I } }$ , the sparsity coefficient of the target x is not directly mathematically related to $\mathbf { L } _ { \mathrm { M S } }$ and $\mathbf { L } _ { \mathrm { S I } }$ , where s as the time-domain representation of x plays exactly this role; thus, the partial derivative for s as a variable is derived, as shown in the following equation:

$$
\left\{ \begin{array} { l l } { \displaystyle \mathbf { s } = F _ { \mathrm { i t } } \{ \mathbf { x } \} } \\ { \nabla \mathbf { L } _ { \mathrm { M S I } } ( \mathbf { s } ) = \displaystyle \frac { \partial \mathbf { L } _ { \mathrm { M S I } } } { \partial \mathbf { s } } . } \end{array} \right.\tag{31}
$$

Since s is not included in the $\mathbf { L } _ { \mathrm { M S } }$ , the second term of (31) can be further expanded in the following way:

$$
\begin{array} { r l r } {  { \nabla { \mathbf { L } } _ { \mathrm { M S I } } ( { \mathbf { s } } ) = \frac { \partial { \mathbf { L } } _ { \mathrm { M S } } } { \partial { \mathbf { s } } } + \beta \frac { \partial { \mathbf { L } } _ { \mathrm { S I } } } { \partial { \mathbf { s } } } } } \\ & { } & { = \frac { \partial { \mathbf { L } } _ { \mathrm { M S } } } { \partial { \mathbf { y } } ^ { \dagger } } \frac { \partial { \mathbf { y } } ^ { \dagger } } { \partial { \mathbf { s } } } + \beta \frac { \partial { \mathbf { L } } _ { \mathrm { S I } } } { \partial { \mathbf { s } } } . } \end{array}\tag{32}
$$

Combining (17), it can be deduced that

$$
\left\{ \begin{array} { l l } { \displaystyle { \frac { \partial { \bf L } _ { M S } } { \partial { \bf y } ^ { \dagger } } \frac { \partial { \bf y } ^ { \dagger } } { \partial { \bf s } } = \frac { \partial { \bf L } _ { M S } } { \partial { \bf y } ^ { \dagger } } \frac { \partial { \bf y } ^ { \dagger } } { \partial \nu ( { \bf s } ) } \frac { \partial \nu ( { \bf s } ) } { \partial { \bf s } } } } \\ { \nu ( { \bf s } ) = H _ { s } ( { \bf W } _ { 1 } { \bf s } + { \bf p } _ { 1 } ) . } \end{array} \right.\tag{33}
$$

It follows that $H _ { s } ( \mathbf { a } )$ can be expressed as

$$
H _ { s } ( \mathbf { a } ) = \frac { 1 } { 1 + e ^ { - \mathbf { a } } } .\tag{34}
$$

According to (33) and (34), it leads to

$$
\begin{array} { l } { \displaystyle \frac { \partial { \bf { L } } _ { \mathrm { { M S } } } } { \partial { \bf { s } } } = 2 \big ( { { \bf { y } } ^ { \dag } } - { \bf { y } } \big ) { \bf { y } } ^ { \dag } { \bf { W } } _ { 1 } { \bf { W } } _ { 2 } } \\ { \displaystyle \times \frac { 1 } { 1 + e ^ { - ( { \bf { W } } _ { 1 } { \bf { s } } + { \bf { p } } _ { 1 } ) } } \bigg ( 1 - \frac { 1 } { 1 + e ^ { - ( { \bf { W } } _ { 1 } { \bf { s } } + { \bf { p } } _ { 1 } ) } } \bigg ) . } \end{array}\tag{35}
$$

Next, the partial derivative results for the other term of the L can be obtained

$$
\beta \frac { \partial \mathbf { L } _ { S I } } { \partial \mathbf { s } } = \beta \frac { 2 \mathbf { s } } { \| \mathbf { y } \| _ { 2 } ^ { 2 } } .\tag{36}
$$

Consequently, summing (35) and (36) can obtain the final representation for the gradient of the proposed loss function

$$
\begin{array} { c } { \displaystyle \frac { \partial { \bf { L } } _ { \mathrm { { M S I } } } } { \partial { \bf { s } } } = \beta \frac { 2 { \bf { s } } } { \| { \bf { y } } \| _ { 2 } ^ { 2 } } + 2 \big ( { \bf { y } } ^ { \dagger } - { \bf { y } } \big ) { \bf { y } } ^ { \dagger } { \bf { W } } _ { 1 } { \bf { W } } _ { 2 } } \\ { \displaystyle \times \frac { 1 } { 1 + e ^ { - ( { \bf { W } } _ { 1 } { \bf { s } } + { \bf { p } } _ { 1 } ) } } \bigg ( 1 - \frac { 1 } { 1 + e ^ { - ( { \bf { W } } _ { 1 } { \bf { s } } + { \bf { p } } _ { 1 } ) } } \bigg ) . } \end{array}\tag{37}
$$

## REFERENCES

[1] M. Wang et al., “TPSSI-Net: Fast and enhanced two-path iterative network for 3D SAR sparse imaging,” IEEE Trans. Image Process., vol. 30, pp. 7317–7332, 2021.

[2] J. Lien et al., “Soli: Ubiquitous gesture sensing with millimeter wave radar,” ACM Trans. Graph., vol. 35, no. 4, pp. 1–19, 2016.

[3] N. Kumchaiseemak et al., “Toward ant-sized moving object localization using deep learning in FMCW radar: A pilot study,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5112510.

[4] A. Prabaswara, A. Munir, and A. B. Suksmono, “GNU radio based software-defined FMCW radar for weather surveillance application,” in Proc. 6th Int. Conf. Telecommun. Syst., Services, Appl. (TSSA), Oct. 2011, pp. 227–230.

[5] S. Kolpuke et al., “Airborne UWB FMCW radar for snow depth measurements,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 2008115.

[6] T. Doi et al., “Frequency hopping ultra wideband inter-vehicle radar system using chirp waveforms,” in Proc. Int. Workshop Ultra Wideband Syst. Joint Conf. Ultra Wideband Syst. Technologies. Joint UWBST, 2004, pp. 386–390.

[7] S. Wei, H. Zhang, X. Zeng, Z. Zhou, J. Shi, and X. Zhang, “CARNet: An effective method for SAR image interference suppression,” Int. J. Appl. Earth Observ. Geoinf., vol. 114, Nov. 2022, Art. no. 103019.

[8] J.-G. Kim, S.-H. Sim, S. Cheon, and S. Hong, “24 GHz circularly polarized Doppler radar with a single antenna,” in Proc. Eur. Microw. Conf., 2005, p. 1386.

[9] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[10] Z. Xu et al., “A novel method of mitigating the mutual interference between multiple LFMCW radars for automotive applications,” in Proc. IEEE Int. Geosci. Remote Sens. Symp., Jul. 2019, pp. 2178–2181.

[11] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[12] G. Feinberg, S. Mulleti, E. Shoshan, and Y. C. Eldar, “Hardware prototype demonstration of a cognitive sub-Nyquist automotive radar,” Electron. Lett., vol. 55, no. 9, pp. 556–558, May 2019.

[13] T. Nozawa, Y. Makino, N. Takaya, M. Umehira, and S. Takeda, “An anti-collision automotive FMCW radar using time-domain interference detection and suppression,” in Proc. Int. Conf. Radar Syst., 2017, pp. 1–5.

[14] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[15] J. Jung, S. Lim, J. Kim, S.-C. Kim, and S. Lee, “Interference suppression and signal restoration using Kalman filter in automotive radar systems,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 726–731.

[16] J.-H. Choi, H.-B. Lee, J.-W. Choi, and S.-C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Trans. Commun., vol. 99, no. 1, pp. 280–287, 2016.

[17] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[18] Z. Chen, F. Xie, C. Zhao, and C. He, “Radio frequency interference mitigation in high-frequency surface wave radar based on CEMD,” IEEE Geosci. Remote Sens. Lett., vol. 14, no. 5, pp. 764–768, May 2017.

[19] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[20] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[21] R. Singh, D. Saluja, and S. Kumar, “Spread spectrum coded radar for R2R interference mitigation in autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 10418–10426, Aug. 2022.

[22] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

[23] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[24] T. Oyedare, V. K. Shah, D. J. Jakubisin, and J. H. Reed, “Interference suppression using deep learning: Current approaches and open challenges,” IEEE Access, vol. 10, pp. 66238–66266, 2022.

[25] T.-H. Sang, K.-Y. Tseng, F.-T. Chien, C.-C. Chang, Y.-H. Peng, and J.-I. Guo, “Deep-learning-based velocity estimation for FMCW radar with random pulse position modulation,” IEEE Sensors Lett., vol. 6, no. 3, pp. 1–4, Mar. 2022.

[26] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153491–153507, 2021.

[27] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in Proc. IEEE 92nd Veh. Technol. Conf. (VTC-Fall), Nov. 2020, pp. 1–5.

[28] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for FMCW radars,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5118316.

[29] Z. Wang, R. Wang, X. Fu, and K. Xia, “Unsupervised ship detection for single-channel SAR images based on multiscale saliency and complex signal kurtosis,” IEEE Geosci. Remote Sens. Lett., vol. 19, pp. 1–5, 2022.

[30] Z. Zhang, Z. Tian, Y. Zhang, M. Zhou, and B. Wang, “U-DeepHand: FMCW radar-based unsupervised hand gesture feature learning using deep convolutional auto-encoder network,” IEEE Sensors J., vol. 19, no. 16, pp. 6811–6821, Aug. 2019.

[31] K. A. Sørensen, A. Kusk, P. Heiselberg, and H. Heiselberg, “Finding ground-based radars in SAR images: Localizing radio frequency interference using unsupervised deep learning,” IEEE Trans. Geosci. Remote Sens., vol. 61, 2023, Art. no. 4704215.

[32] R. Ke and C.-B. Schönlieb, “Unsupervised image restoration using partially linear denoisers,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 9, pp. 5796–5812, Sep. 2022.

[33] B. Zou, X. Wang, W. Feng, H. Zhu, and F. Lu, “DU-CG-STAP method based on sparse recovery and unsupervised learning for airborne radar clutter suppression,” Remote Sens., vol. 14, no. 14, p. 3472, Jul. 2022. [Online]. Available: https://www.mdpi.com/2072-4292/14/14/3472

[34] C. Jiang, Z. Zhou, and B. Yang, “Unsupervised deep interference mitigation for automotive radar,” in Proc. IEEE 12th Sensor Array Multichannel Signal Process. Workshop (SAM), Jun. 2022, pp. 296–300.

[35] X. Chen, J. Guan, Z. Bao, and Y. He, “Detection and extraction of target with micromotion in spiky sea clutter via short-time fractional Fourier transform,” IEEE Trans. Geosci. Remote Sens., vol. 52, no. 2, pp. 1002–1018, Feb. 2014.

[36] Z. Zhou et al., “SAF-3DNet: Unsupervised AMP-inspired network for 3-D MMW SAR imaging and autofocusing,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5234915.

[37] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[38] S. Chen, J. Taghia, U. Kühnau, T. Fei, F. Grünhaupt, and R. Martin, “Automotive radar interference reduction based on sparse Bayesian learning,” in Proc. IEEE Radar Conf., Sep. 2020, pp. 1–6.

[39] M. Wang, S. Wei, Z. Zhou, J. Shi, and X. Zhang, “Efficient ADMM framework based on functional measurement model for mmW 3-D SAR imaging,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5226417.

[40] F. Uysal, I. Selesnick, and B. M. Isom, “Mitigation of wind turbine clutter for weather radar by signal separation,” IEEE Trans. Geosci. Remote Sens., vol. 54, no. 5, pp. 2925–2934, May 2016.

[41] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[42] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf., Apr. 2018, pp. 0405–0410.

[43] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270–5283, Dec. 2021.

![](images/ceea74eb83d496b0d7be1e453338b4bf2a3439af33ad44712d1985d2bbb5eebc.jpg)

[44] Z. Xu, “Bi-level l<sub>1</sub> optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, Jan. 2023.

[45] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[46] J. Bobin, J.-L. Starck, J. M. Fadili, Y. Moudden, and D. L. Donoho, “Morphological component analysis: An adaptive thresholding strategy,” IEEE Trans. Image Process., vol. 16, no. 11, pp. 2675–2681, Nov. 2007.

[47] Y. LeCun, Y. Bengio, and G. Hinton, “Deep learning,” Nature, vol. 521, no. 7553, pp. 436–444, 2015.

[48] X. Li, J. Ran, H. Zhang, and S. Wei, “MCSNet: A radio frequency interference suppression network for spaceborne SAR images via multi-dimensional feature transform,” Remote Sens., vol. 14, no. 24, p. 6337, Dec. 2022. [Online]. Available: https://www.mdpi.com/2072- 4292/14/24/6337

[49] D. Oprisan and H. Rohling, “Analysis of mutual interference between automotive radar systems,” in Proc. Int. Radar Symp. (IRS), 2005, pp. 83–90.

[50] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[51] S. Wei, J. Liang, M. Wang, J. Shi, X. Zhang, and J. Ran, “AF-AMPNet: A deep learning approach for sparse aperture ISAR imaging and autofocusing,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5206514.

[52] M. Arjovsky, A. Shah, and Y. Bengio, “Unitary evolution recurrent neural networks,” in Proc. 33rd Int. Conf. Mach. Learn., in Proceedings of Machine Learning Research, vol. 48, M. F. Balcan and K. Q. Weinberger, Eds. New York, NY, USA, Jun. 2016, pp. 1120–1128. [Online]. Available: https://proceedings.mlr.press/v48/arjovsky16.html

[53] X. Huang, A. Tuyen Le, and Y. J. Guo, “Transmit beamforming for communication and self-interference cancellation in full duplex MIMO systems: A trade-off analysis,” IEEE Trans. Wireless Commun., vol. 20, no. 6, pp. 3760–3769, Jun. 2021.

[54] A. Pascual-Iserte, A. I. Perez-Neira, and M. A. Lagunas, “On power allocation strategies for maximum signal to noise and interference ratio in an OFDM-MIMO system,” IEEE Trans. Wireless Commun., vol. 3, no. 3, pp. 808–820, May 2004.

![](images/8ad61163dcecc8a784651f23ec9542bcc3c49d6bd077eef684e4610fce9eb95d.jpg)

In 2014, he joined UESTC, where he is currently a Professor. His research interests include radar signal processing and synthetic aperture radar (SAR) systems.

![](images/faf2a9a3bc38bda6b2ae29f86f89ee0a9af5bdd131b3a29c155780adfce636c7.jpg)

Shunjun Wei (Member, IEEE) received the B.S., M.Sc., and Ph.D. degrees in electronic engineering from the University of Electronic Science and Technology of China (UESTC), Chengdu, China, in 2006, 2009, and 2013, respectively.

Mou Wang received the B.S. degree in communication engineering from the Chongqing University of Posts and Telecommunications, Chongqing, China, in 2018. He is currently pursuing the Ph.D. degree with the School of Information and Communication Engineering, University of Electronic Science and Technology of China, Chengdu, China.

His current research interests include compressed sensing, synthetic aperture radar (SAR) imaging, and machine learning.

Yifei Hu (Student Member, IEEE) received the B.S. degree in information and communication engineering from the University of Electronic and Science Technology of China (UESTC), Chengdu, China, in 2018, respectively, where he is currently pursuing the M.S. degree.

![](images/3489999f401befaa6680e3202097a56d6f0be8251ae12c07c995fbb17aa22e15.jpg)

His research interests include machine learning on millimeter-wave radar anti-interference and radar point cloud 3-D reconstruction.

Jun Shi (Member, IEEE) received the B.S., M.S., and Ph.D. degrees in electronic engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2002, 2005, and 2009, respectively.

He is currently an Associate Professor with the University of Electronic Science and Technology of China. His research interests include radar signal processing and synthetic aperture radar systems.

![](images/6ee24f27d7b644bbea1a7da956a376cc9975bde4ce9916fa861a75ca59b76752.jpg)  
Hao Zhang (Student Member, IEEE) received the B.S. degree from the Southwest University of Science and Technology of China, Mianyang, China, in 2021. He is currently pursuing the M.S. degree at the School of Information and Communication Engineering, University of Electronic Science and Technology of China, Chengdu, China.

His research interests include radar interference suppression and machine learning.

![](images/8c4de59e53d0e03ad6bd297ebca608b6d3c0a985538ed00c371ec9368b05cd30.jpg)

Guolong Cui (Senior Member, IEEE) received the B.S., M.S., and Ph.D. degrees in electronic information engineering from the University of Electronic Science and Technology of China (UESTC), Chengdu, China, in 2005, 2008, and 2012, respectively.

From September 2013 to July 2018, he was an Associate Professor with UESTC, where he has been a Professor since August 2018. His research interests include cognitive radar, array signal processing, Multiple Input Multiple Output (MIMO) radar, and through-the-wall radar.