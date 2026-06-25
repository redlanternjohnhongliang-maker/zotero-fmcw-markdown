# Interference Mitigation for Automotive FMCW Radar With Tensor Decomposition

Yunxuan Wang, Yan Huang Member, IEEE, Jiang Liu, Student Member, IEEE, Ruizhe Zhang, Hui Zhang , Member, IEEE, and Wei Hong , Fellow, IEEE

Abstract— With the surge of vehicles and transportation, sensing obstacles and warning drivers to avoid accidents have become a great concern in recent years. In the current roadworthy electromagnetic environment, the number of frequency modulated continuous wave (FMCW) millimeter-wave (MMW) automotive radars has exploded due to their unique advantages in environmental sensing. However, the frequency band of the automotive radars is limited from 77 to 81 GHz, hence the burgeoning of radars on the road is bound to cause mutual interference and jeopardize further target detection and parameter estimation. In this paper, two basic schemes are considered to mitigate mutual interference of automotive radars. First, we consider the sparse characteristics of the mutual interference in the twodimensional (2-D) time domain and employ a sparse interference extraction (SIE) method to tackle the mutual interference. Next, we further consider the low-rank property of the useful echoes across multiple channels and propose a novel three-dimensional (3-D) tensor decomposition (TD) method to decompose the received signals into mutual interference and useful echoes. Several numerical simulations are fulfilled to test the robustness of the proposed TD method, especially for multiple input and multiple output (MIMO) systems under complex electromagnetic circumstances. Furthermore, more experiments are implemented to demonstrate its feasibility in practical applications in comparison to multiple state-of-the-art methods.

Index Terms— Automotive frequency modulated continuous wave (FMCW) radar, interference mitigation, sparse interference extraction, three-dimensional (3-D) tensor decomposition.

## I. INTRODUCTION

## A. Background

AKING advantage of the ability to estimate the range, velocity, and direction of a target in any weather and lighting conditions [3], automotive radar, as one of the most commonly-used sensors in advanced driver assistance system (ADAS) [1], helps to reduce the probability of car accidents, ensures transportation security [2] and is capable of working all day [4]. According to the research reports published by Allied Market Research in July 2021, the global automotive radar market is expected to exceed 10 billion US dollars by 2028, which makes the research on automotive radars increasingly attractive [5].

Meanwhile, the European Telecommunications Standards Institute (ETSI) and the US Federal Communications Commission (FCC) regulate the frequency band laws of automotive radar into the range of 76 - 81 GHz with a bandwidth of 5 GHz [6], which is accepted by many countries globally. In some countries, the bandwidth is even narrower. Given the regulation, the bandwidth seems to be wide currently, but each automotive radar requires a large bandwidth of around several hundred MHz. Moreover, when the automotive radar market expands and more vehicles are implemented with radars, the currently assigned bandwidth will not be sufficient and the overlaps in both frequency and time of automotive radars will be inevitable [7]. Meanwhile, the wide application of multiple input and multiple output (MIMO) system worsens the situation. These overlaps would cause strong mutual interference and make it hard to acquire essential information about targets. Therefore, with the widespread application of automotive radars, it is crucial to mitigate the mutual interference in practical scenarios [8].

## B. Existing Methods

Traditional interference mitigation methods for frequency modulated continuous wave (FMCW) radars can be generally classified into six categories [4], including polarization domain methods, time domain methods, frequency domain methods, coding domain methods, spatial domain methods, and strategic approaches. In recent years, research on FMCW radars mainly focused on three types of methods to mitigate interference, i.e., deep learning methods [9], [10], [11], [12], [13], [14], [15], [16], joint radar-communication methods [17], [18], [19], [20], [21], [22], [23], [24], and signal separation methods [25], [26], [27], [28], [32].

1) Deep Learning Methods: Prevailing deep learning methods for automotive radar interference mitigation often use autoencoder (AE) or generative adversarial network (GAN) as the basic models. AE is a common denoising tool where mutual interference is special noise for signals of automotive radar. Several AE-based methods have been developed, one is implemented by using the interference-contaminated range-Doppler (RD) map as the input and interference-free RD map as the expected output [9], and another uses two AE models to fulfill the interference detection and signal recovery in the time-frequency domain, respectively [10]. Research on GAN models typically first zeros the interference contaminated parts in the time domain or time-frequency domain, then trains the GAN models to recover the useful echo signals [11]. Other popular models include recurrent neural networks (RNN) and convolutional neural networks (CNN). In [12], an RNNbased method with self-attention modules removes the mutual interference by considering the time-sequence characteristics of the useful echo signals. The research group from the Graz University of Technology utilizes CNN and its variants [13], [14], [15] to remove the mutual interference in RD maps and use experimental signals as the dataset to train the network and obtain good performance. Another CNN method uses a fully connected neural network to process the interferencecontaminated RD maps and obtain interference-free time domain signals [16]. Above all, the deep learning methods aim to achieve end-to-end results via tremendous training data and labels, which may not perfectly match the properties of the true scene.

2) Joint Radar-Communication Methods: Instead of tackling the mutual interference and recovering the contaminated useful signal, joint radar-communication methods expect to avoid interference by assigning frequency bands, chirp rates, and time slits. The waveform assignment of radar signals is often accomplished by central dispatch base stations [17] or some sort of internet of vehicles formed by adjacent vehicles [18]. To avoid the capacity constraints of current centralized dispatch base stations, decentralization technology that balances system safety and efficiency is also another in-demand research direction [19]. For radars with extra communication functions, the signals transmitted by these radars are often modulated from classic communication signals and coding strategies, or classic radar signals with functional communication coding schemes, i.e., spread spectrum coding schemes [20], or even adaptive FMCW parameters allocation method [21]. Research on joint radar-communication often includes the design of hardware circuits [22]. To testify the efficiency of these joint radar-communication methods, stochastic geometry models are commonly proposed to describe the practical vehicular circumstances [23]. Although the joint radar-communication method is a very promising trend in the development of automotive radars, it requires radars to pre-modulate their signals [24], which will increase the cost of the hardware.

3) Signal Separation Methods: Signal separation methods often transform the received signals into different domains through proper bases, which makes the search of bases very crucial to the performance of interference mitigation [25]. A block Kronecker compressed sensing (BKCS) algorithm is proposed in [26] to mitigate the mutual interference in a 2D compressed sensing framework. A signal separation method that takes advantage of the interference’s symmetry in the frequency domain is proposed in [27], which requires complex sampling that does not always match practical situations. Previous researchers [28] also discovered a method that transforms the received signal into the time-frequency domain and exploits the low-rank and sparse components in received signals to achieve the separation of interference and useful echoes. The sparsity of the target’s signal in the tunable Q-factor wavelet transform (TQWT) domain can also be used to separate the interference and target echoes [29]. Novel orthogonal noise waveforms that are defined using an optimized Kaiser function can also help reduce such neighboring interference [30]. A novel interference mitigation technique is proposed in [31] and utilizes the pulse compression principle for interference compression and mitigation. However, previous signal processing methods usually only focus on the received signals of one single chirp or one channel, without consideration of the connection of the received signal across channels [32]. Although all the previous research has demonstrated a promising performance, they commonly do not consider the practical scenarios of automotive radars nor rigorously derive the properties of both mutual interference and useful echoes.

## C. Proposed Method

In this paper, we propose a novel three-dimensional (3-D) tensor decomposition (TD) method to mitigate the FMCW radars’ mutual interference based on two basic observations, i.e., the sparsity of the mutual interference in the time domain and the low-rank characteristics of the useful target echoes across channels. The structure of the 3-D tensor is aligned with the MIMO radar system received signals. The sparsity of the mutual interference always holds based on the assumption that the aggressor radar’s and the victim radar’s FMCW waveform parameters are not all identical. In this context, we employ the alternating direction method of multipliers (ADMM) to optimize the TD problem, alternately mitigating the interference and protecting the useful echo signals. More specifically, we first analyze the intrinsic signal features of both mutual interference and useful echoes in one-dimensional (1-D) time, two-dimensional (2-D) time, and 3-D spatial-time domains to illustrate the motivation of TD method. Then the sparse interference extraction (SIE) method is derived to extract the sparse interference in the 2-D time domain. By extending it to the 3-D spatial-time domain, we employ the tensor nuclear norm, build the augmented Lagrange function, and propose the whole TD optimization solutions. The relationship between the notch method, the SIE method, and the proposed TD method is analyzed in detail to demonstrate the effectiveness of the proposed method. Numerical simulations and real-scene experiments are implemented, where the notch method and the SIE method are also applied as comparisons, to prove the feasibility and superiority of our proposed TD method over the previous state-of-the-art methods.

The main contributions of this paper can be summarized in four aspects: first, we prove the sparsity of the mutual interference and the low-rank characteristics of the useful echo across channels. Second, we consider the suppression of interference in multi-channel MIMO automotive radar. Third, we propose a novel 3-D TD method for interference mitigation on automotive radar systems with specific derivations and closed-form solutions for each iteration. Fourth, we consider multiple common scenarios and complete the corresponding numerical experiments and simulations, which demonstrate the effectiveness and robustness of the proposed methods in practical automotive applications.

The rest of the contents of this paper are organized as follows. In Section II, we model the automotive FMCW radar system with detailed formulations of received signals and characteristics analysis of mutual interference. In Section III, the 3-D TD method is employed to solve the tensor optimization problem where the low-rank property of useful echoes and the sparsity of interference are both constrained. Section IV analyses three algorithms’ performance and their computational complexity. Then, their performance is demonstrated in simulated scenarios and a field experiment in Section V and Section VI. Finally, conclusions are drawn in Section VII.

Notations: Throughout this paper, we denote tensors by regular weight Euler script letters, e.g., A. Matrices are denoted by boldface capital letters, e.g., A, vectors are denoted by boldface lowercase letters, e.g., a, and scalars are denoted by the lowercase letters, e.g. a. For a three-dimensional tensor $\begin{array} { l } { A } { \mathrm { ~ \in ~ } } \end{array} { C } ^ { N _ { 1 } \times N _ { 2 } \times N _ { 3 } }$ , we denote its $( n _ { 1 } , n _ { 2 } , n _ { 3 } )$ -th entry as ${ \mathcal A } _ { n _ { 1 } , n _ { 2 } , n _ { 3 } } ~ \mathrm { o r } ~ a _ { n _ { 1 } , n _ { 2 } , n _ { 3 } }$ and use the MATLAB notation $\mathcal { A } ( i , : , : )$ $\mathcal { A } ( : , j , : )$ , and $\textstyle A ( : , : , k )$ to denote the i -th horizontal, j -th lateral, and k-th frontal slices, respectively. The frontal slice $\mathcal { A } ( : , : , k )$ is more often denoted compactly as $A ^ { ( k ) }$ . The entry notation of a matrix is similar to the three-dimensional tensor by reducing the dimension.

## II. SIGNAL MODEL

In this section, we rigorously derive the formulations of automotive FMCW radars’ target echo signals and mutual interference caused by aggressor radars. Through the analysis of the interference, its sparsity in the time domain is obtained. Then, a sparse convex optimization model is constructed and an SIE method is proposed accordingly. Next, through the analysis of the 3-D tensor of the received signal, the 2-D sparse characteristic of the mutual interference is reasonably extended to the sparse characteristic in the 3-D tensor. The low-rank characteristic of the received echoes across channels is also considered to build a tensor-based convex optimization model. More details are introduced in the following subsections.

## A. FMCW Signal Model With Mutual Interference

In practical applications, the automotive radars transmit FMCW waveforms in a set of chirps. The transmitted FMCW chirp can be presented as

$$
T ( t ) = A _ { t x } \exp ( j 2 \pi f _ { c } t + j \pi \gamma t ^ { 2 } ) ,\tag{1}
$$

where $A _ { t x }$ is the amplitude of the transmitted signal, $f _ { c }$ is the carrier frequency, $\gamma$ is the chirp rate, and t is the full time. Next, we introduce the concepts of slow time $t _ { s }$ and fast time $t _ { f }$ to explain the actual automotive FMCW radar signals. These time parameters have the following relationship:

$$
t = t _ { s } + t _ { f } .\tag{2}
$$

Herein, full time t is used to describe the absolute time of the received signals, and slow time $t _ { s }$ is mainly used to describe the time between chirps. As for fast time $t _ { f } .$ , it often describes the time in each chirp. For a set of FMCW chirps, the absolute time is the sum of all chirp duration, in other words, the slow time and the exact time in the chirp, i.e., the fast time. Then the transmitted signal of automotive FMCW radar with regard to full time and fast time can be rewritten as

$$
\begin{array} { r } { T ( t , t _ { f } ) = \exp ( j 2 \pi f _ { c } t + j \pi \gamma t _ { f } ^ { 2 } ) . } \end{array}\tag{3}
$$

The transmitted signal travels through the air, is intercepted by targets, and then scattered back to the receivers of the automotive radar. The received signal reflected from one point target can be described as

$$
\begin{array} { l } { S _ { \mathrm { { r e c e i v e } } } ( t , t _ { f } ) = T ( t - \tau , t _ { f } - \tau ) } \\ { \qquad = \exp ( j 2 \pi f _ { c } ( t - \tau ) + j \pi \gamma ( t _ { f } - \tau ) ^ { 2 } ) , } \end{array}\tag{4}
$$

where τ is the delay between the received signal and the transmitted signal, caused by the distance between the point target and the radar. The instantaneous range is

$$
R ( t _ { f } , t _ { s } ) = R ( t _ { s } ) - v t _ { f } ,\tag{5}
$$

where $R ( t _ { s } ) = R _ { 0 } - v t _ { s }$ , and $R _ { 0 }$ is the starting range. The radial velocity of the target relative to the radar is v. Then the precise delay can be expressed as

$$
\tau = \frac { 2 R ( t _ { f } , t _ { s } ) } { c } ,\tag{6}
$$

where $c$ is the speed of the electromagnetic wave.

For an FMCW radar system, the dechirp processing is commonly accomplished by mixing the received signals with the conjugate of the transmitted one. After the dechirp processing, the carrier frequency is recalibrated, which significantly reduces the requirements of the sampling rate according to the Nyquist sampling theorem. The resultant signal can be approximately formulated as

$$
\begin{array} { l } { { \displaystyle { \cal S } _ { \mathrm { d e c h i r p } } ( t _ { f } , t _ { s } ) } } \\ { { \displaystyle ~ = { \cal S } _ { \mathrm { r e c e i v e } } ( t , t _ { f } ) \times { \cal T } ^ { * } ( t , t _ { f } ) } } \\ { { \displaystyle ~ \approx \exp [ - j 4 \pi f _ { c } \frac { R ( t _ { s } ) } { c } ] \exp [ - j \frac { 4 \pi \gamma } { c } t _ { f } ( R ( t _ { s } ) - \frac { f _ { c } } { \gamma } v ) ] } } \\ { { \displaystyle ~ \exp [ j \frac { 4 \pi \gamma } { c ^ { 2 } } R ^ { 2 } ( t _ { s } ) ] } . } \end{array}\tag{7}
$$

To obtain the RD map, we perform the inverse fast Fourier transform (IFFT) on fast time $t _ { f }$ and fast Fourier transform (FFT) on slow time $t _ { m }$ . The result can be expressed as

$$
\begin{array} { l } { \displaystyle { S _ { \mathrm { d e c h i r p } } ( f _ { r } , f _ { d } ) = \mathrm { s i n c } \left( T _ { p } \left( f _ { r } - 2 \frac { R ( t _ { s } ) - \frac { f _ { c } } { \gamma } v } { c } \right) \right) } } \\ { \displaystyle { \mathrm { s i n c } \left( T _ { a } \left( f _ { d } - \frac { 2 f _ { c } v } { c } \right) \right) } } \\ { \displaystyle { \mathrm { e x p } \left[ - j 4 \pi f _ { c } \frac { R _ { 0 } } { c } \right] \mathrm { e x p } \left[ j \frac { 4 \pi \gamma } { c ^ { 2 } } R ^ { 2 } ( t _ { s } ) \right] } . } \end{array}\tag{8}
$$

Since the sinc(x) function reaches its maximum when $x =$ 0, the range and velocity of the target can be estimated by

![](images/1c9d8bd53e5fb1e5127ddff87e3b1007abb6c020aa0ab1f32bbd4a5d54680c4f.jpg)  
Fig. 1. The illustrations of notch method, SIE method, and proposed tensor decomposition (TD) method.

positioning the coordinates of the strong points in the RD map, that is,

$$
\begin{array} { l } { f _ { r } ^ { * } = 2 \displaystyle \frac { R ( t _ { s } ) - \frac { f _ { c } } { \gamma } v } { c } , } \\ { f _ { d } ^ { * } = \displaystyle \frac { 2 f _ { c } v } { c } . } \end{array}\tag{9}
$$

(10)

As for the mutual interference transmitted from the aggressor radars to the receivers of the victim radar, it, after dechirp processing, can be expressed as

$$
\begin{array} { r l } & { I ( t _ { f } , t _ { s } ) } \\ & { \quad = T ( t - \tau ^ { \prime } , t _ { f } - \tau ^ { \prime } ) \times T ^ { * } ( t , t _ { f } ) } \\ & { \quad \approx \exp [ j \pi ( \gamma ^ { \prime } - \gamma ) t _ { f } ^ { 2 } ] \exp [ - j 2 \pi f _ { c } \frac { R ( t _ { s } ) } { c } ] } \\ & { \quad \quad \exp [ - j \frac { 2 \pi \gamma ^ { \prime } } { c } t _ { f } ( R ( t _ { s } ) - \frac { f _ { c } } { \gamma ^ { \prime } } v ) ] \exp [ j \frac { \pi \gamma ^ { \prime } } { c ^ { 2 } } R ^ { 2 } ( t _ { s } ) ] , } \end{array}\tag{11}
$$

where $\begin{array} { r } { \tau ^ { \prime } = \frac { R ( t _ { f } , t _ { s } ) } { c } } \end{array}$ is the delay of the electromagnetic wave traveling from aggressor radar to the victim radar, and $\gamma ^ { \prime }$ is the chirp rate of the aggressor radar.

## B. Sparsity of Mutual Interference in Time Domain

In practical situations, the useful radar signals need to be reflected by the targets within the detection range. However, the mutual interference that contaminates the useful echoes is commonly propagated to the receivers of the victim radars without any reflection, which may cause an increase in the noise level and degradation of the RD map. Then, the power difference between mutual interference and useful echoes makes it possible for the notch methods to null the time sampling points contaminated by interference and recover the needed echo signals, as shown in the pink frame in Fig. 1. As can be seen in Fig. 2, the mutual interference commonly dominates a very short period of one chirp time, demonstrating the sparsity of interference.

![](images/80b61ecb04553ee9d494fdb8fa4f8ee6fe2e0a628642dc35012d16684b1ef718.jpg)  
Fig. 2. FMCW radar signal processing in one chirp duration. The upper diagram shows the received signals and real sampling theory. The bottom diagram shows the dechirp processed signals.

Then, the received signals of an automotive radar system can be expressed as

$$
y ( t ) = s ( t ) + i ( t ) + n ( t ) ,\tag{12}
$$

where $s ( t )$ is the useful target echo signal, i (t) is the mutual interference caused by the aggressor radars, and $n ( t )$ is the background noise. Since the automotive radars are sampling discretely with a sampling interval 1t, Eq. (12) can be rewritten as

$$
y [ k ] = s [ k ] + i [ k ] + n [ k ] , k = 0 , 1 , \cdots , K - 1 ,\tag{13}
$$

where k is the indices of the discrete time samples and K is the sampling number in one chirp. For practical automotive radar systems, one frame has a set of chirps to estimate the Doppler parameters. We assume that the number of chirps in one frame is L, and a corresponding two-dimensional signal model, which indicates the range-velocity domain, is constructed as follows

$$
{ \bf Y } ( k , l ) = { \bf S } ( k , l ) + { \bf I } ( k , l ) + { \bf N } ( k , l ) ,\tag{14}
$$

where l denotes the l-th chirp, and the capital letters, i.e., Y, S and $\mathbf { I } \in \mathbb { C } ^ { K \times L }$ , have the same denotations as those lowercase ones in Eq. (13). For the above matrices, the l-th chirp denotes the slow time, and k-th time samples denote the fast time. Herein, the matrices are in the fast-time and slow-time domain. The sparse property of the mutual interference is illustrated in Fig. 3. The power difference is presented by the color differences. The yellow represents strong mutual interference, which can be seen in this figure, showing obvious sparsity in the fast-time and slow-time matrix [33]. Therefore, in practical automotive radar systems and vehicular circumstances, sparse assumption of the mutual interference commonly holds.

![](images/e242f178d7aba8107a188aa63950ca499eea0c254e3b5fba27f41f8b3376c468.jpg)  
Fig. 3. Sparsity of mutual interference I matrix in fast-time and slow-time domain.

Algorithm 1 SIE Method   
Input : Y   
User Parameter $: \mu$   
1:Initialize : ${ \bf I } _ { ( 0 ) } , { \bf Y } _ { 1 ( 0 ) }$   
2:while not converged do   
3: t ← t + 1   
4: $\begin{array} { r } { \mathbf { I } _ { ( t + 1 ) } = \operatorname { S r } \left( \mathbf { Y } _ { ( t ) } + { \frac { \mathbf { Y } _ { 1 ( t ) } } { \mu _ { ( t ) } } } - \mathbf { I } _ { ( t ) } , { \frac { 1 } { \mu _ { ( t ) } } } \right) } \end{array}$   
5: ${ \bf Y } _ { 1 ( t + 1 ) } = { \bf Y } _ { 1 ( t ) } + \mu _ { ( t ) } ( { \bf Y } _ { ( t ) } - \dot { \bf I } _ { ( t + 1 ) } )$   
6: $\mu _ { ( t + 1 ) } = \operatorname* { m i n } ( \eta \mu _ { ( t ) } , \mu _ { \operatorname* { m a x } } )$   
7:end while   
Output: $\mathbf { Y } - \mathbf { I }$

With the sparsity of mutual interference, we can constrain the mutual interference with the $\ell _ { 0 }$ norm, which yields

$$
\begin{array} { r l } & { \underset { \mathbf { I } } { \operatorname* { m i n } } ~ \| \mathbf { I } \| _ { 0 } } \\ & { \mathrm { s . t . } ~ \| \mathbf { Y } - \mathbf { I } \| _ { F } ^ { 2 } < \delta , } \end{array}\tag{15}
$$

where $\| \cdot \| _ { 0 }$ denotes the $\ell _ { 0 }$ norm of a matrix and $\delta \geq 0$ is the hyperparameter. To solve this optimization problem, the ℓ norm is replaced by $\ell _ { 1 }$ norm in order to relax it into a convex problem, i.e., the traditional least absolute shrinkage and selection operator (LASSO) problem, extracting a sparse component from the received signals as follows

$$
\begin{array} { l } { \underset { \mathbf { I } } { \mathrm { m i n } } \quad \| \mathbf { I } \| _ { 1 } } \\ { \mathrm { s . t . } \quad \| \mathbf { Y } - \mathbf { I } \| _ { F } ^ { 2 } < \delta , } \end{array}\tag{16}
$$

where ∥·∥<sub>1</sub> denotes the $\ell _ { 1 }$ norm. Herein, the solution is named the SIE method, which is listed in Algorithm 1. The light yellow frame in Fig. 1 is a schematic of the SIE method.

It is noted that the SIE method only considers the sparsity of interference in the fast-time and slow-time domain for one specific channel. Thanks to the development of multipleinput multiple-output (MIMO) technology and the decrease of sensors’ sizes, MIMO technologies are prevailing in automotive radars and improve the estimation resolution of the direction of arrival (DOA) [34]. MIMO radars share the major characteristics of being capable to transmit different signals on multiple transmitters and separate these signals on multiple receivers [35]. MIMO radar provides more information in one specific sampled time slit, relative research includes the enhancement of its spectral compatibility with optimization of the transmit waveforms and receive filter in a spectrally crowded environment [36], mitigation of mutual interference based on empirical mode decomposition (EMD) and multiple signal classification (MUSIC) to obtain an accurate DOA estimation [37]. Current MIMO automotive radars’ transmitters commonly work by time division multiplexing (TDM), which is also used for the cases in this paper. Next, we will consider multiple channels for the extra protection of useful echoes.

## C. 3-D Tensor Interference Mitigation Model

First, the basic tensor theory is introduced as follows: A multidimensional array has been named as a tensor, and the number of the dimensions is named as the order of the tensor. When the number of dimensions of the tensor is 0, 1, and 2, the tensor is a scale, vector, and matrix. For the received automotive radar signals, the tensor we propose here has three dimensions, those three dimensions are fast time, slow time, and spatial channel.

As we already discussed in the last subsection, the mutual interference, which we expect to exterminate, has sparse property in the 1-D time domain, or in the 2-D fast time and slow time domain. When it comes to the multiple transmitters and multiple receivers, the classic MIMO system is able to differentiate the signals from channels. Herein, the matrices in the fast time and slow time domain have similar useful echo components across channels while the mutual interference is different for adjacent chirps since the chirp duration of aggressor radar is commonly different from the victim radar. By projecting the received signals into a 3-D “fast-time & slow-time & channel” tensor, the sparsity of the interference can be better presented and the low-rank property of the useful echo is revealed. The light green solid frame in Fig. 1 is a schematic of the tensor projection. Then the tensor signal model can be expressed as

$$
\mathcal { V } = \mathcal { S } + \mathcal { T } + \mathcal { N } ,\tag{17}
$$

where $\mathcal { V } \in \mathbb { C } ^ { K \times L \times M }$ is the received signals, $\mathcal { S } \in \mathbb { C } ^ { K \times L \times M }$ is useful echo signals, $\mathcal { T } \in \mathbb { C } ^ { K \times L \times M }$ is mutual interference, $\mathcal { N } \in \mathbb { C } ^ { K \times L \times M }$ is the noise, and M is the channel number of the automotive radar system. To constrain the rank of the useful echoes and take advantage of the sparsity of the mutual interference across channels, an optimization problem is proposed as

$$
\begin{array} { l l } { \displaystyle \operatorname* { m i n } _ { \mathcal { T } , \mathcal { S } } \mathrm { t r a n k } ( \mathcal { S } ) + \lambda \| \mathcal { T } \| _ { \mathrm { T e n s o r R } } , } \\ { \mathrm { s . t . } \quad \| \mathcal { V } - \mathcal { T } - \mathcal { S } \| _ { \mathrm { T e n s o r F } } < \delta , } \end{array}\tag{18}
$$

where trank(·) is the rank function for tensors, λ is a hyperparameter, $\lVert \cdot \rVert _ { \mathrm { T e n s o r R } }$ is the regularization term, and ∥ · ∥<sub>TensorF</sub> is the Frobenius norm for tensors, which is defined as

$$
\| \boldsymbol { \mathcal { A } } \| _ { \mathrm { T e n s o r F } } = \left( \sum _ { i = 1 } ^ { I _ { 1 } } \sum _ { j = 1 } ^ { I _ { 2 } } \sum _ { k = 1 } ^ { I _ { 3 } } a _ { i , j , k } ^ { 2 } \right) ^ { \frac { 1 } { 2 } } ,\tag{19}
$$

where $\mathcal { A } \in \mathbb { R } ^ { I _ { 1 } \times I _ { 2 } \times I _ { 3 } }$

Eq. (18) is similar to the classic low-rank and sparse decomposition model of matrices. Next, we will then discuss how to solve the above optimization problem.

## III. PROPOSED TENSOR DECOMPOSITION METHOD

## A. T-SVD

To solve this problem, it is relaxed to a convex one, that is,

$$
\begin{array} { l } { \displaystyle \operatorname* { m i n } _ { \mathcal { T } , \mathcal { S } } \| \mathcal { S } \| _ { \mathrm { T e n s o r * } } + \lambda \| \mathcal { T } \| _ { \mathrm { T e n s o r F } } , } \\ { \mathrm { s . t . } \quad \| \mathcal { V } - \mathcal { T } - \mathcal { S } \| _ { \mathrm { T e n s o r F } } < \delta , } \end{array}\tag{20}
$$

where $\parallel \cdot \parallel _ { \mathrm { T e n s o r * } }$ is the nuclear norm [38] of tensor and ∥ · ∥<sub>Tensor1</sub> is the $\ell _ { 1 }$ norm of tensor. The definition of the nuclear norm of the useful echo tensor is

$$
\lVert S \rVert _ { \mathrm { T e n s o r * } } = \frac { 1 } { M } \sum _ { k = 1 } ^ { M } \lVert \bar { S } ^ { ( k ) } \rVert _ { * } .\tag{21}
$$

where $\bar { S } ^ { ( k ) }$ is the frontal slice of $\bar { \mathcal { S } } .$ The $\ell _ { 1 }$ norm of the mutual interference tensor is defined as

$$
\| \mathcal { T } \| _ { \mathrm { T e n s o r 1 } } = \sum _ { n _ { 1 } , n _ { 2 } , n _ { 3 } } | \mathcal { T } _ { n _ { 1 } n _ { 2 } n _ { 3 } } | .\tag{22}
$$

To solve the matrix RPCA problem, the solution derivations use singular value decomposition (SVD) to update the lowrank component. As for a reasonable extension, the tensor decomposition problem in (20) is solved similarly by using the tensor singular value decomposition (T-SVD) [39]. The T-SVD is defined as

$$
\mathcal { A } = \mathcal { U } \ast \mathcal { D } \ast \mathcal { V } ^ { * } \in \mathbb { C } ^ { N _ { 1 } \times N _ { 2 } \times N _ { 3 } } ,\tag{23}
$$

where $\mathcal { D } \in { \mathbb C } ^ { N _ { 1 } \times N _ { 2 } \times N _ { 3 } }$ is a diagonal tensor, $\mathrm { i . e . , }$ each frontal slice of the tensor is a diagonal matrix, $\mathcal { U } \in \mathbb { C } ^ { N _ { 1 } \times N _ { 2 } \times N _ { 3 } }$ and $\boldsymbol { \mathcal { V } } \in \mathbb { C } ^ { N _ { 1 } \times N _ { 2 } \times N _ { 3 } }$ are the orthogonal tensors. An orthogonal tensor is defined as the tensor that satisfies the following expression

$$
{ \mathcal { Q } } ^ { * } * { \mathcal { Q } } = { \mathcal { Q } } * { \mathcal { Q } } ^ { * } = { \mathcal { E } } ,\tag{24}
$$

where $\mathcal { E }$ is the identity tensor [39]. The efficiency of this lowrank constraint and its equivalent to tubal rank constraint is rigorously derived in [40].

Then, by implementing the T-SVD into the optimization problem, the relaxed convex optimization problem can be solved by ADMM, the derivation process is formulated in detail in the following subsection.

## B. Tensor Decomposition (TD) Method

The augmented Lagrangian function of the optimization model in Eq. (20) can be expressed as

$$
\begin{array} { l } { \displaystyle \mathcal { L } ( \mathcal { T } , \mathcal { S } , \mathcal { V } _ { 1 } , \mu ) } \\ { \displaystyle \quad = \| S \| _ { \mathrm { T e n s o r * } } + \lambda \| \mathcal { Z } \| _ { \mathrm { T e n s o r 1 } } + \frac { \mu } { 2 } \| \mathcal { V } + \frac { \mathcal { V } _ { 1 } } { \mu } - \mathcal { T } - S \| _ { \mathrm { T e n s o r F } } ^ { 2 } , } \end{array}\tag{25}
$$

where $\mu$ is the hyperparameter and $\mathcal { \mathrm { V } } _ { 1 }$ is the Lagrangian variable.

1) Step 1 [Update $\mathit { S l } .$ To update $s ,$ the subproblem in the (t + 1)-th iteration is formulated as

$$
\begin{array} { r l r } {  { \mathcal { L } ( \mathcal { T } _ { ( t ) } , \mathcal { S } , \mathcal { V } _ { 1 ( t ) } , \mu _ { ( t ) } ) } } \\ & { } & { = \| \mathcal { S } \| _ { \mathrm { T e n s o r * } } + \frac { \mu _ { ( t ) } } { 2 } \| \mathcal { V } + \frac { \mathcal { V } _ { 1 ( t ) } } { \mu _ { ( t ) } } - \mathcal { T } _ { ( t ) } - \mathcal { S } \| _ { \mathrm { T e n s o r F } } ^ { 2 } . } \end{array}\tag{26}
$$

Then, based on Parseval’s theorem, it can be verified that

$$
\begin{array} { l } { \displaystyle \left. \mathcal { V } - \mathcal { T } - \mathcal { S } + \frac { \mathcal { V } _ { 1 } } { \mu } \right. _ { \mathrm { T e n s o r F } } ^ { 2 } } \\ { = \displaystyle \frac { 1 } { M } \left. \bar { \mathcal { V } } - \bar { \mathcal { T } } - \bar { \mathcal { S } } + \frac { \bar { \mathcal { V } } _ { 1 } } { \mu } \right. _ { \mathrm { T e n s o r F } } ^ { 2 } } \\ { = \displaystyle \frac { 1 } { M } \sum _ { k = 1 } ^ { M } \left. \bar { \mathcal { V } } ^ { ( k ) } - \bar { \mathcal { T } } ^ { ( k ) } - \bar { \mathcal { S } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 } ^ { ( k ) } } { \mu } \right. _ { \mathrm { F } } ^ { 2 } , } \end{array}\tag{27}
$$

where M is the number of slice in the tensor after ${ \mathrm { F F T } } ,$ ¯<sup>(k)</sup> is the k-th slice of the tensor after FFT, since FFT is a linear transformation, the results are equivalent to tensor operation. Hence the subproblem in (26) can be reformulated as

$$
\begin{array} { r l } & { \mathcal { L } \left( \mathcal { Z } _ { ( t ) } , \boldsymbol { S } , \mathcal { V } _ { 1 ( t ) } , \mu _ { ( t ) } \right) } \\ & { \ = \displaystyle \frac { 1 } { M } \sum _ { k = 1 } ^ { M } \left( \left\| \bar { \boldsymbol { S } } ^ { ( k ) } \right\| _ { * } + \frac { \mu _ { ( t ) } } { 2 } \left\| \bar { \mathcal { V } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { Z } } _ { ( t ) } ^ { ( k ) } - \bar { \mathcal { S } } ^ { ( k ) } \right\| _ { \mathrm { F } } ^ { 2 } \right) . } \end{array}\tag{28}
$$

The above low-rank tensor recovery subproblem can be transformed into several slices of low-rank matrix recovery subproblems, and the augmented Lagrange function of the $k \mathrm { - }$ th slice can be expressed as

$$
\begin{array} { r l } & { \mathcal { L } \left( \bar { \mathcal { T } } _ { ( t ) } ^ { ( k ) } , \bar { \mathcal { S } } ^ { ( k ) } , \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } , \mu _ { ( t ) } \right) } \\ & { \quad = \| \bar { S } ^ { ( k ) } \| _ { * } + \displaystyle \frac { \mu _ { ( t ) } } { 2 } \| \bar { \mathcal { V } } ^ { ( k ) } + \displaystyle \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { T } } _ { ( t ) } ^ { ( k ) } - \bar { \mathcal { S } } ^ { ( k ) } \| _ { F } ^ { 2 } . } \end{array}\tag{29}
$$

The closed-form solution of the above problem is given by using singular-value thresholding (SVT) method, that ${ \mathrm { i s } } ,$

$$
\begin{array} { r } { \bar { S } _ { ( t + 1 ) } ^ { ( k ) } = \bar { \mathcal { U } } _ { ( t ) } ^ { ( k ) } T _ { \frac { 1 } { \mu _ { ( t ) } } } ( \bar { \mathcal { D } } _ { ( t ) } ^ { ( k ) } ) ( \bar { \mathcal { V } } _ { ( t ) } ^ { ( k ) } ) ^ { H } , } \end{array}\tag{30}
$$

where

$$
\bar { \mathcal { U } } _ { ( t ) } ^ { ( k ) } \bar { \mathcal { D } } _ { ( t ) } ^ { ( k ) } ( \bar { \mathcal { V } } _ { ( t ) } ^ { ( k ) } ) ^ { H } = \bar { \mathcal { V } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { T } } _ { ( t ) } ^ { ( k ) } ,\tag{31}
$$

$$
[ T _ { \frac { 1 } { \mu _ { ( t ) } } } ( \bar { \mathcal { D } } _ { ( t ) } ^ { ( k ) } ) ] _ { q , q } = \operatorname* { m a x } \left\{ [ \bar { \mathcal { D } } _ { ( t ) } ^ { ( k ) } ] _ { q , q } - \frac { 1 } { \mu _ { ( t ) } } , 0 \right\} .\tag{32}
$$

Then the tensor $s$ in $( t + 1 )$ -th iteration can be updated by stacking the above updated matrices and taking the IFFT along the channel dimension, that is,

$$
S _ { ( t + 1 ) } = \mathrm { I F F T } ( \bar { S } _ { ( t + 1 ) } , [ \mathbf { \Omega } ] , 3 ) .\tag{33}
$$

2) Step 2 [Update I]: After updating S, we will update I by taking advantage of its sparsity across channels. The subproblem of the Lagrange function for updating $\mathcal { T }$ can be formulated as

$$
\begin{array} { r l } & { \mathcal { L } \left( \mathcal { T } , S _ { ( t + 1 ) } , \mathcal { V } _ { 1 ( t ) } , \mu _ { ( t ) } \right) } \\ & { \ = \lambda \| \mathcal { T } \| _ { \mathrm { T e n s o r 1 } } + \displaystyle \frac { \mu _ { ( t ) } } { 2 } \| \mathcal { V } + \displaystyle \frac { \mathcal { V } _ { 1 ( t ) } } { \mu _ { ( t ) } } - \mathcal { T } - S _ { ( t + 1 ) } \| _ { \mathrm { T e n s o r F } } ^ { 2 } . } \end{array}\tag{34}
$$

The above problem can be also solved similarly for each frontal slice as

$$
\begin{array} { l } { \displaystyle \mathcal { L } \left( \bar { \boldsymbol { \mathcal { T } } } ^ { ( k ) } , \bar { \mathcal { S } } _ { ( t + 1 ) } ^ { ( k ) } , \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } , \boldsymbol { \mu } _ { ( t ) } \right) } \\ { \displaystyle = \lambda \| \bar { \boldsymbol { \mathcal { Z } } } ^ { ( k ) } \| _ { 1 } + \frac { \mu _ { ( t ) } } { 2 } \| \bar { \mathcal { V } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { T } } ^ { ( k ) } - \bar { \mathcal { S } } _ { ( t + 1 ) } ^ { ( k ) } \| _ { F } ^ { 2 } . } \end{array}\tag{35}
$$

Then the closed-form solution is given as follows:

$$
\bar { \mathcal { T } } _ { ( t + 1 ) } ^ { ( k ) } = \mathrm { S r } \Bigg ( \bar { \mathcal { V } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { S } } _ { ( t + 1 ) } ^ { ( k ) } , \frac { \lambda } { \mu _ { ( t ) } } \Bigg ) ,\tag{36}
$$

where

$$
[ \mathrm { S r } ( \mathbf { O } , \delta ) ] _ { p , q } = \operatorname* { m a x } \left\{ \left| \mathbf { O } _ { p , q } \right| - \delta , 0 \right\} \frac { \mathbf { O } _ { p , q } } { \left| \mathbf { O } _ { p , q } \right| } .\tag{37}
$$

3) Step 3 [Update the Lagrangian Multiplier $\mathcal { V } _ { I } \boldsymbol { { l } } ;$ The Lagrangian multiplier $\mathcal { V } _ { 1 }$ needs to update by the following equation

$$
\bar { \mathcal { V } } _ { 1 ( t + 1 ) } ^ { ( k ) } = \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } + \mu _ { ( t ) } ( \bar { \mathcal { V } } ^ { ( k ) } - \bar { \mathcal { Z } } _ { ( t + 1 ) } ^ { ( k ) } - \bar { \mathcal { S } } _ { ( t + 1 ) } ^ { ( k ) } ) .\tag{38}
$$

4) Step 4 [Update the Hyperparameter $\mu J .$ : The hyperparameter $\mu$ can be updated by

$$
\mu _ { ( t + 1 ) } = \operatorname* { m i n } ( \eta \mu _ { ( t ) } , \mu _ { \operatorname* { m a x } } ) ,\tag{39}
$$

where $\eta$ is the penalty parameter and $\mu _ { \mathrm { m a x } }$ is the maximum value of $\mu .$ . When the iteration number reaches the limits or the termination criterion holds, the iteration will end. The termination criterion is

$$
\frac { \| \mathcal { V } + \frac { \mathcal { V } _ { 1 } } { \mu } - \mathcal { T } - \mathcal { S } \| _ { \mathrm { T e n s o r F } } ^ { 2 } } { \| \mathcal { V } \| _ { \mathrm { T e n s o r F } } } < \tau ,\tag{40}
$$

where τ is the stop threshold. The algorithm of the proposed TD method is shown in Algorithm 2. The light blue frame in Fig. 1 is a schematic of the proposed tensor decomposition (TD) method.

## IV. ALGORITHM ANALYSIS

In this section, the performance and the computational complexity of the classic notch method, the SIE method, and the proposed TD method are analyzed in detail.

Algorithm 2 TD Method   
Input : $\mathcal { V }$   
User Parameter $: \lambda , \mu$   
1:Initialize : $ { \boldsymbol { S } } _ { ( 0 ) }$   
2:while not converged do   
3: $t \gets t + 1$   
4: $\bar { S } _ { ( t ) } = \mathrm { F F T } ( S _ { ( t ) } , [ ] , 3 ) ,$   
5: $\begin{array} { r } { \bar { \mathcal { U } } _ { ( t ) } ^ { ( k ) } \bar { \mathcal { D } } _ { ( t ) } ^ { ( k ) } ( \bar { \mathcal { V } } _ { ( t ) } ^ { ( k ) } ) ^ { H } = \bar { \mathcal { V } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { T } } _ { ( t ) } ^ { ( k ) } } \end{array}$   
6: $\hat { S } _ { ( t + 1 ) } ^ { ( k ) } = \hat { \mathcal { U } } _ { ( t ) } ^ { ( k ) } T _ { \frac { 1 } { \mu _ { ( t ) } } } ( \hat { \mathcal { D } } _ { ( t ) } ^ { ( k ) } ) ( \hat { \mathcal { V } } _ { ( t ) } ^ { ( k ) } ) ^ { H }$   
7: $S _ { ( t + 1 ) } = \mathrm { I F F T } ( \bar { S } _ { ( t + 1 ) } , [ \mathbf { \Omega } ] , \mathbf { 3 } )$   
8: $\begin{array} { r } { \bar { \mathcal { T } } _ { ( t + 1 ) } ^ { ( k ) } = \mathrm { S r } \left( \bar { \mathcal { V } } ^ { ( k ) } + \frac { \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( k ) } } { \mu _ { ( t ) } } - \bar { \mathcal { S } } _ { ( t + 1 ) } ^ { ( k ) } , \frac { \lambda } { \mu _ { ( t ) } } \right) } \end{array}$   
9: $\bar { \mathcal { V } } _ { 1 ( t + 1 ) } ^ { ( k ) } = \bar { \mathcal { V } } _ { 1 ( t ) } ^ { ( \bar { k } ) } + \mu _ { ( t ) } ( \bar { \mathcal { V } } ^ { ( k ) } - \bar { \mathcal { Z } } _ { ( t + 1 ) } ^ { ( k ) } - \bar { \mathcal { S } } _ { ( t + 1 ) } ^ { ( \bar { k } ) } )$   
10: $\mu _ { ( t + 1 ) } = \operatorname* { m i n } ( \eta \mu _ { ( t ) } , \mu _ { \operatorname* { m a x } } )$   
11:end while   
Output: S, I

## A. Performance Analysis

As the most easily implemented method for interference mitigation in practical scenarios, the notch method is discussed first. The pink frame in Fig. 1 is a schematic of the classic notch method. As it is shown in the schematic, the received data are extracted chirps by chirps and a certain threshold is given for the interference detection in the fasttime domain. The classic notch method takes advantage of the power difference between the interference and the echoes, and notches the time samples that are contaminated by the interference. Once the interference dominates the majority of the time samples, then the notch method will also remove most of the useful echoes simultaneously. Though the notch method loses part of the information from target echoes, it is still the mainstream interference mitigation method for most cases in practical applications.

In fact, the three methods in Fig. 1 have a straightforward connection by extending the data dimension. The notch method considers the received signals as a 1-D vector in the fast-time domain. In other words, the sparsity of mutual interference always holds in the fast-time domain. Then we extend the nulling operation within one chirp into a whole set of chirps, i.e., in the fast time and slow time domain, and relax the nulling operation, i.e., $\ell _ { 0 }$ norm, into a convex constraint, i.e., $\ell _ { 1 }$ norm. As a result, the mutual interference can be extracted in this 2-D matrix under the relaxed constraint. Till now, only the mutual interference’s sparsity has been taken into consideration in both the 1-D and 2-D time domains. For current automotive radars, the prevailing MIMO framework is necessary to improve the system performance, which makes it possible to extend the received signal to a 3-D tensor. In a 3-D tensor, the low-rank property of the useful target reflection is highlighted across channels. By taking advantage of this feature, the useful echoes can be protected with a low-rank constraint in the tensor and the mutual interference tensor is still constrained as a strong sparse signal. Then the tensor decomposition model is thereby proposed to mitigate the mutual interference in the tensor scale, as shown in the light blue frame in Fig. 1. As it can be seen that these three methods are connected by the extension of the data dimension, the characteristics of the components are consistent throughout the whole extension process, which makes the proposed TD method firmly supported in principle.

To illustrate the excellent performance of the TD method, we need to point out the main difference between the TD method and the other methods. The notch method and SIE method are the intuitive usage of the interference’s sparsity in one specific channel based on the power difference between the mutual interference and useful echo signals, which naturally appear to be conceivable, but also disabled its application when the power difference is not that large. However, their performance is limited for only considering received signals one channel at a time. Without considering the useful underneath connections between channels, the intrinsic property of the useful echoes cannot be revealed and we can hardly protect the real echoes from the wrong extraction of interference. For the TD method, the 3-D tensor ensures the low-rank property of the useful echoes, therefore, the characteristics of the connection between channels extracted by our method correspond to the actual physical meaning, which guarantees the robust performance of the TD method.

It is worth noting that the proposed TD method is the first work to combine all MIMO channels for interference mitigation. It is helpful for the following target detection and direction-of-arrival (DOA) estimation, which will be further tested in Section V. In addition, the proposed method can also be used on the sparse MIMO array, which is the typical choice for current automotive radar products.

## B. Compuational Complexity

In this section, the computational complexities of the Notch method, SIE method and TD method are compared in detail. In addition, both the SIE method and TD method require multiple iterations to realize the convergence. Herein, we only focus on the computational complexity of one iteration.

First, we assume that the received signal $Y \in \mathbb { C } ^ { K \times L \times P } .$ where K is the number of the sampling points per chirp, which is normally 1024 or 512 in practical application. L is the number of chirps per set, which is normally 256 or 128 in practical application. P is the number of channel per device, which is normally 12 or 1 depends on the structure of the radar. Herein, we consider a MIMO radar with 3 transmitter and 4 receiver, so the channels’ number is 12.

The Notch method requires one comparing for each sampling point, so the computational complexity of this method is $\mathcal { O } \left( K L P \right)$ . The SIE method requires one soft-thresholding operation for each channel matrix in each iteration, then the total computational complexity per iteration is at least $\mathcal { O } \left( 2 K L P \right)$

The proposed TD method requires P SVDs and P SVT operations for each frontal slice, and K L P-point FFTs for the entire signal tensor in each iteration. Then the total computational complexity per iteration is at least $\mathcal { O } \left( P ( K L ^ { 2 } + \mathbf { \bar { \Phi } } ^ { } \mathbf { \bar { K } } L ) + 2 K L l o \bar { g } ( P ) \right)$

![](images/a4c4e120ea9988379fe23af631b5283dd5dcfc15c9d1f40d4aedcb3937da72a4.jpg)  
(a)

![](images/d6540ffcc9846ff208c99dfdc87e6b042d50a63c5dac656e66e4c090b563d195.jpg)  
(b)

![](images/1f3f7383f8717f6db99c54f59a8e0ba3b33475308e26c4db19b603b19dfa3b7f.jpg)  
(c)

![](images/18655cfbaaf828ab11432757f29c2ddf2d7febbcf33cc30cb7e72cfcdbaf84b5.jpg)  
(d)

![](images/8e77108c5715413193f7074ba11d2190c91ef1843b9c864ce9b04316169d2749.jpg)  
(e)  
Fig. 4. The RD map of scenario 1. The yellow frame label the targets and the red arrows point out the fake targets and sidelobes. (a) Interference-polluted (b) Method 1: notch method. (c) Method 2: SIE method. (d) Method 3: TD method. (e) Interference-free.

## V. SIMULATIONS & MEASUREMENT

In this section, numerical experiments for different scenarios are tested with simulated automotive data with mutual interference. The data is simulated based on an FMCW automotive radar system with three transmitters and four receivers, which can be equivalent to 12 transceivers, i.e., virtual array, according to the MIMO technology. Without generality, the virtual array is a uniform linear array with interval being half of the wavelength. We then form the tensor by stacking the received signals through channels.

To prove the feasibility of the TD methods quantitatively, the output root-mean-square error (RMSE) is used with the following formulation,

$$
\operatorname { R M S E } ( \mathbf { X } , { \hat { \mathbf { X } } } ) = { \frac { \| \mathbf { X } - { \hat { \mathbf { X } } } \| _ { F } } { \| \mathbf { X } \| _ { F } } } ,\tag{41}
$$

where X is the interference-free signals, $\hat { \mathbf { X } }$ is the recovered signals. The smaller the RMSE, the more similar the recovered signals and the original signals are, and the better the recovered performance of the TD method is. Also, we use signal interference noise ratio (SINR) as a performance measurement, which is defined as

$$
\mathrm { S I N R } = 2 0 \log _ { 1 0 } \left( \frac { \| \mathbf { X } \| _ { F } } { \| \mathbf { X } - \hat { \mathbf { X } } \| _ { F } } \right)\tag{42}
$$

The bigger the SINR, the better the interference suppression performance. In the following experiments, we implement the interference mitigation algorithms before generating RD maps. In the following, we will discuss two scenarios: 1) interference of one aggressor automotive radar with low SINR and multiple (here are five) vehicles, 2) interference of multiple (here are four) aggressor automotive radars with low SINR and few (here are two) vehicular targets. These two scenarios are typical for mutual interference mitigation.

## A. Scenario 1

In this scenario, the mutual interference is transmitted by one single aggressor radar with the input SINR being −20 dB. Five vehicles are scattered within the field of view (FOV) of our victim radar. All these targets are set with individual range, azimuth, and velocity values. The RD map contaminated by the mutual interference and the interferencefree RD map are shown in Fig. 4 (a) and (e), respectively, where we use yellow solid rectangles to mark the five targets. As we can see from these two diagrams, the targets can be clearly observed without interference pollution, while the vehicular targets are totally submerged by the strong mutual interference.

![](images/0f80f45942d5c96ba8b3b524c3e7288beabb490bd4ccca19dbf81263a37cb5e2.jpg)  
Fig. 5. The time-frequency spectrum of scenario 2.

![](images/7fa4d2b88a1417dd7272fefba4dab5acd835329b492f1c019b5bc0e22e68359e.jpg)  
Fig. 6. Sparsity of mutual interference I matrix in fast-time and slow-time domain of scenario 2.

Then we implement the mutual interference mitigation methods on the contaminated received signals. The results of the notch method, the SIE method, and the TD method are compared under scenario 1 in Fig. 4 (b),(c), and (d), where we use yellow solid rectangles to mark the five targets and red arrows to point out the blurry parts in RD map. Herein, the differences between the results of the notch method and the other two can be seen clearly from the figures, the red arrows pointed the pixels which have a horizontal line of a blur. Also, the edges of the RD map of the notch method have a blurry pattern. RMSE [41] is applied to quantify the interference mitigation performance of the three methods and the results are listed in Table I. The RMSE of TD method is smaller than the others, which is also consistent with the previous analysis.

![](images/44f0080d38e83b4568afaac4f40abc7f23b5b1e3df89091a3f2c896617f5f02a.jpg)  
(a)

![](images/52ae1c8f5e220566207d9ce881662c4f137f4afadc6ac70b5b423b89f38e726a.jpg)  
(b)

![](images/23fb4aa7f1d6157b45f9ee9b34a1ee1a1ac7d1c860b45677d35d489bf8e10b62.jpg)  
(c)

![](images/c2db1db3af4827f1e04d1bb47080eb4777b4b7efd74685c07c18e4f7e762b7e8.jpg)  
(d)

![](images/acd664f3fc9917a3161cc76919b59e734066b55d32a86c71b94ac4722e94f82e.jpg)  
(e)

Fig. 7. The RD map of scenario 2. The yellow frame label the targets and the red arrows point out the fake targets and sidelobes. (a) Interference-polluted. (b) Method 1: notch method. (c) Method 2: SIE method. (d) Method 3: TD method. (e) Interference-free.  
![](images/83cfa2310533fb80cf505e4444bf0367256cc8106395d5bc6468ce730439817c.jpg)  
Fig. 8. Setup of static aggressor field experiment.

TABLE I  
THE RMSE & SINR OF THE THREE METHODS’ RESULT IN SCENARIO 1
<table><tr><td>Algorithms</td><td>RMSE</td><td>SINR</td></tr><tr><td>Before</td><td>1.7028e-04</td><td>37.6883</td></tr><tr><td>Notch Method</td><td>1.6524e-05</td><td>47.8189</td></tr><tr><td>Sparse Interference Extraction Method</td><td>6.0589e-06</td><td>52.1760</td></tr><tr><td>Tensor Decomposition Method</td><td>4.1639e-06</td><td>53.8050</td></tr></table>

## B. Scenario 2

In this scenario, the mutual interference is transmitted by four aggressor radars, and two vehicular targets are set in front of our victim radar. Each target is also set with a given parameter pair of range, azimuth, and velocity values. We assume that the four aggressor radars transmit different types of FMCW signals with different carrier frequencies, powers, and chirp rates. The time-frequency spectrum of the received signal [42] is shown in Fig. 5.

As we can clearly see from Fig. 5, the interference have different chirp rates and powers in the time-frequency domain. The RD map contaminated by the mutual interference and the interference-free RD map are shown in Fig. 7 (a) and (e), respectively, where we use yellow solid rectangles to mark the target. In these two diagrams, the vehicular targets are totally overwhelmed by the mutual interference. The interferencecontaminated RD map is vaguer than that in scenario 1 shown in Fig. 7 (a), which is aligned to the fact that the more the aggressors are, the harder it is to extract useful signal from the received ones.

Then we implement the notch method, SIE method, and TD method on the interference-contaminated signals. The results of the SIE method and the TD method are compared under scenario 2 in Fig. 7 (b)-(d), where we use yellow solid rectangles to mark the targets and red arrows to mark the fake targets. Herein, both the notch method and the SIE method leave the RD map with a bunch of fake targets, as pointed by the red arrows, though removing the majority of the interference. The RD map of the SIE method even has a background pattern just like the mutual interference-contaminated RD map does in Fig. 7 (a). The degraded performance of the SIE method can be explained vividly in Fig. 6, the mutual interference matrix in scenario 2 is not as sparse as scenario 1. However, with the protection of the useful signals by the low-rank property, TD method shows great performance. There is no blur in velocity estimation of the RD map, and also very similar to the interference-free one.

TABLE II  
THE RMSE & SINR OF THE THREE METHODS’ RESULT IN SCENARIO 2
<table><tr><td>Algorithms</td><td>RMSE</td><td>SINR</td></tr><tr><td>Before</td><td>1.7028e-04</td><td>37.4980</td></tr><tr><td>Notch Method</td><td>3.7666e-05</td><td>44.2405</td></tr><tr><td>Sparse Interference Extraction Method</td><td>4.1552e-05</td><td>43.8141</td></tr><tr><td>Tensor Decomposition Method</td><td>8.6644e-06</td><td>50.6226</td></tr></table>

The RMSE metric is also applied to quantify the interference mitigation performance of the three methods and the values are listed in Table II. The RMSE of TD method is smaller than the compared methods, and SINR is larger, which indicates that our method processed results are more similar to interference-free RD map as well as better performance.

These two scenarios simulate the two common scenes when the mutual interference dominate the received signals and both simulations demonstrate the robust performance of TD method. But it should be noted that the above experiments are based on simulated scenes, which show the effectiveness of TD method in theory. Then in the next section, the practical experimental data will be given to further illustrate the superiority of the performance.

## VI. EXPERIMENTAL RESULTS

## A. Static Aggressor Field Experiment

To prove the robustness of the proposed method, physical experiments are performed and the setup is shown in Fig. 8. In the field experiment, we adopted the TI AWR2243BOOST mmWave radar development board for data capture. Fig. 8 shows the experiment setup in front of the square of the Purple Mountain Laboratory in China Wireless Valley, Nanjing,

![](images/6561f6774e31739a00853ea868b988ce6534b6b4e0331b53b18e9cfaba990f6b.jpg)  
(a)

![](images/0f88be81ec052af813717d2d72e0611df8421613dfc63774c4932da36d8d51a1.jpg)  
(b)

![](images/98311c26c4611c63e8d1f26647762ecacabf0ca7c3dcc1ebb9f14de244225ba0.jpg)

![](images/4a34fcd2501351b8f86f3476e46d2ced9e8e6ea7a456fed5fd04b196418bfa15.jpg)  
(d)

![](images/cad5a79fd20da858ee80916941bea74cf7540ecd4a21251b46c375c5ece0d9f8.jpg)  
(e)

(c)  
![](images/54929be0c38ba1f06a14d2d8c7b48508577ce73c10b30b6aa5b22f40bd5a9298.jpg)  
(f)

![](images/f5e47302ad5d7516a3b7021345d37a2ea0e9589adb90ca5fa9d8db60a6c92276.jpg)  
(g)

![](images/5471121231f3e6020a052210a1f49b2d203954935983ccf34ded4f4dfa9d8163.jpg)  
(h)

Fig. 9. Static aggressor field experiment results with waveform 1. (a) Interference-contaminated RD map. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method. (g) SIE method. (h) Proposed TD method.  
![](images/550396d13684b3ffe75963ac48fb0a74978d1ba036be097e2a7314cb2e912c08.jpg)

![](images/ab3b5787f3a8de115e832fe05ccb8eb3990386010fc9746347b05f94628c74ad.jpg)  
(a)  
(b)

![](images/e80d72ee6a9179ebb3ac53258d622b8c3d0efe9618efb38894df8805de2082bc.jpg)

![](images/33e8e9d4b5ca06dea74e8ee3685feb3460a884ac528eaa6594054e5082bd7234.jpg)  
(d)

![](images/94aad30cc61f1cd1b77c1b7818a931eecccafc935a59a742e47330bfa511b2e8.jpg)  
(e)

(c)  
![](images/2e7c170656b47084d795c994e23076f944efd7cb6072c5bf23818ca11dc56a26.jpg)  
(f)

![](images/b9dbb1ea1aaa5d1726f37f5cd6eca9744a184916664fc3941d3371c3368267ce.jpg)  
(g)

![](images/ed070a84fb40cdf8cac4e317677916a64710eb7a3683a9779e25aa229aca42f2.jpg)  
(h)  
Fig. 10. Static aggressor field experiment results with waveform 2. (a) Interference-contaminated RD map. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method. (g) SIE method. (h) Proposed TD method.

China. The victim radar was configured as a typical shortrange radar (SRR) with different frequency slopes to test the performance of our algorithms. The aggressor radar, provided promptly by Hawkeye Technology Corporation, is a long-range radar (LRR) operating within a frequency band from 76 GHz to 81 GHz.

In this experiment, we set three different waveform parameters to test the robustness of the proposed method. All the configurations set for the experiments are listed in Table III. Both the aggressor radar and the victim radar work at TDM so that only one transmitter of each radar works at the same time. The captured data was saved to disk and processed on Matlab. To testify the superiority of our proposed method, several previous classic methods, including Hankel matrix optimization method [28], the CFAR-based dilate mask method [43], the adaptive noise canceller (ANC) method [27], and the BKCS method [26], are implemented as comparisons. The interference-polluted RD maps and processed results for the three waveforms are respectively shown in Fig. 9, Fig. 10, and Fig. 11.

As shown in Fig. 9, Fig. 10, and Fig. 11, we use orange rectangles to frame out the interference patterns that still remain in the RD maps after applying the notch method, ANC method, and BKCS method. We can clearly see from these figures, that there are still interference artifacts that cannot be removed thoroughly. Among the three methods, the notch method keeps as much target reflection as possible in the RD map, but the other two methods remove the majority of useful target reflections and few useful echoes are left in the final map. The loss of effectiveness of these two methods may be explained by the fact that not every chirp is contaminated by the aggressor radars in practical applications. Also, we use red rectangles to frame out the fake targets in the RD map processed by the ANC method, since the difference between the real part and the imaginary part in the real experiments is randomly distributed rather than the simulated results, which makes the ANC method fail to work.

![](images/fe4409c9b18be7ea5923753cfcc1ef544f86abd4609746849836748862708746.jpg)  
(a)

![](images/58b787dfdea9431926b362e2074de13ed909c1788315cd3032a929d0a33f4233.jpg)  
(b)

![](images/defa1ce16fd4e53857d8621e707cfcc9db95469b0cb6fc25e9f9caaafb42eedc.jpg)

![](images/64101df9b7a43e1b1ec389cf574f40814984ca8b6cdd39dcf0161a68ee9675e1.jpg)  
(d)  
(c)

![](images/165e4d6768f435fa587d5c8323d908a4b6bd36b222ba283e5da96016bea8c40f.jpg)  
(e)

![](images/bc1cfaaa057ba67f4ba53dc8b9b06c3ddb7e992eb870147102f6db316bd0b01c.jpg)  
(f)

![](images/111253469b77500360a2de2eb2efb79d987bcec193270c829eb1cc6abc259889.jpg)  
(g)

![](images/4ccf7bbf97bc5245758f02dc498440b3d140e1f069a38dad38593ae48ae33792.jpg)  
(h)  
Fig. 11. Static aggressor field experiment results with waveform 3. (a) Interference-contaminated RD map. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method. (g) SIE method. (h) Proposed TD method.

TABLE III  
CONFIGURATION IN STATIC AGGRESSOR FIELD EXPERIMENT (WAV. = WAVEFORM)
<table><tr><td>Configurations</td><td>Aggressor Radar</td><td>Wav. 1</td><td> $\overline { { \mathrm { W a v . ~ } 2 } }$ </td><td>Wav. 3</td><td>Unit</td></tr><tr><td>Start Frequency</td><td>76.67</td><td>76.76</td><td>76.74</td><td>76.71</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>6</td><td>-0.6</td><td>0.6</td><td>3</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>25.6</td><td>34</td><td>34</td><td>34</td><td> $\mu \mathrm { s }$ </td></tr><tr><td>Number of Fast Time Samples</td><td>512</td><td>512</td><td>512</td><td>512</td><td></td></tr><tr><td>Number of Slow Time Samples</td><td>64</td><td>64</td><td>64</td><td>64</td><td></td></tr></table>

Fig. 12. The bird-eye view of the static aggressor field experiment with two interference sources.  
![](images/993df2d65024a89b0aa1106223b5c436c61cca85c682e7349e4a9d828cf900d6.jpg)

![](images/5b7da946700c40f0d0ce807ee959af54b9360716ebcb90631c4fa12822f09f78.jpg)  
Fig. 13. The front view of the static aggressor field experiment with two interference sources.

Basically, the Hankel matrix optimization method, CFARbased dilate mask method, and the SIE method can remove most of the interference and keep the background clean. But the residual interference still submerges the weak scatters in the far field, which are marked by the green rectangles in RD maps in the subfigures (e), (f), and (g) of Fig. 9, Fig. 10, and Fig. 11. Among all previous state-of-the-art methods, the proposed TD method shows the feasibility of mitigating the mutual interference effectively, protecting the useful echoes from being removed.

## B. Static Aggressor Field Experiment With Two Interference Sources

In realistic transportation circumstances, there are probably two or even more vehicles with automotive radars that work in the same frequency band. Therefore, we perform another experiment that has two aggressor radars as the interference sources. The experiment is performed in a square in Nanjing, the aggressor radars, i.e., the Ali Cloud traffic radar and the D08 radar are both provided by Hawkeye Technology Corporation. The radar parameters of the three radars are shown in Table. IV. As shown in Fig. 12 and 13, the two aggressor radars, as well as the targets for they both have metal reflective surfaces, are marked by red solid rectangles. We employed the same comparing methods and the results are shown in Fig. 14.

![](images/ae2156a8231e1a99aec42249c41ce45c2e97efea0426a8333e57c6241b4d0b8a.jpg)  
(a)

![](images/d5e5f6301ffc9e647a46a8b4b1a10dc0fc4d72b238b1c0ca75ee91e8455f540a.jpg)  
(b)

![](images/bba3a6acb07dde42f556cbeab83d4eb912b9563c52bebc698042ccdcefe696ef.jpg)

![](images/e789265d5342f7812377c597557bfcba555b473dcf04b6bd6d751185b93dd74f.jpg)

![](images/bcadb2a65d2be59bf4b78ce1028b65cde53d81ac187d8c525ba609e5cbdfee47.jpg)

(e)  
![](images/dedc23f15508e997ca0987543dfbc615eb06e3cadcea22efa3a2be7b1bb86fdd.jpg)  
(f)

(c)  
(d)  
![](images/b00c9c155c85d7d80d31385d2aa87de22bec05ec004a6400df0c6b8469b0f0fc.jpg)  
(g)

![](images/69e57326d56f786711846c4774f7adfb551c1bf47bf6114656da5a3b0a72a0bc.jpg)  
(h)

Fig. 14. RD maps of the automotive radar signals contaminated by two aggressor radars. (a) Interference-contaminated RD map. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method. (g) SIE method. (h) Proposed TD method.  
![](images/0d2141f4d8172bce6c931c2cbeeb95df8b75ffef7ecc633ad8022ce93383b1ec.jpg)  
Fig. 15. The front view of the complex scenario of the static interference source.

![](images/bb546ad248fc7eb8e93beb80049363b8be85e6b94fba1e81dbf00b5df16dacbc.jpg)  
Fig. 16. The side view of the complex scenario of static interference source.

As can be seen in Fig. 14, we used rectangles to mark the targets in the RD maps, solid ones for detectable targets, and dotted ones for unrecoverable targets. As can be seen in Fig. 14 (a), two aggressor radars overwhelm the RD map even more severely. Most methods are invalid under this circumstance and only our proposed TD method can recover the two targets in the RD map. This experiment proves the superiority of our proposed method again.

## C. Static Aggressor Experiment Under Complex Circumstance

To better testify our proposed method’s feasibility and robustness under complex scenarios, we performed another field experiment in a parking lot with three different commercial radars, i.e., short-range radar (SRR), mid-range radar (MRR), and long-range radar (LRR), which are provided by Hawkeye Technology Corporation. The experiment photo is shown in Figure 15 and 16. We select three methods with good performance in previous experiments and compare the proposed method with them. The experimental results are illustrated in Fig. 17 and 18.

The RMSEs of the above methods are listed in Table V. As can be seen in Fig. 17, 18, and Table V, under three different types of aggressor radars’ contamination, the proposed TD method still outperforms the other three methods. This experiment shows the robustness and feasibility of proposed TD methods under complex circumstances.

## D. Static Aggressor Field Experiment With Target Positioning

To better get behind our proposed methods, we implemented the practical experiment with no-interference comparison. To enhance the plausibility of this experiment, we perform the data collection with static targets. We turned off the aggressor radar and collected the interference-free data immediately after finishing the collection of interference contaminated data. The experiment setup is shown in Fig. 19. As can be seen, there are three static targets in front of the victim radar and one of them is the aggressor radar, which is a middle-range automotive radar made by the Hawkeye Company. The victim radar is still the TI AWR2243BOOST mmWave radar. The radar configurations of both aggressor and victim radar are listed in Table VI.

![](images/c0db68f0800a04d838caf3ab05ddbab0699d11cdff7ffa0259f1a33cdd271f0c.jpg)  
(a)

![](images/ce4c1f447845a858cf9ae6c69a6701ead78865e8230e83dd53c39b0da792c5d6.jpg)  
(b)

![](images/3a14e4d954f3efbf5a63e407cdca34a9a51c99d7e860074c225125124dfba85b.jpg)  
(c)

![](images/10fb437657e21fb719d6aad13e6166d36b31f959f2cacb805f6d8888ab7c16cf.jpg)  
(d)

Fig. 17. RD maps of the automotive radar signals contaminated by different types of aggressor radars. (a) Interference free. (b) Short-range radar. (c) Middle-range radar. (d) Far-range radar.  
![](images/6d35460ed110c5a192333daf13c42c266cd812433da636f01b9672e914be3e9b.jpg)  
(a)

![](images/5bbda4c551fa4db39037c1cf3310ad3ea22f1b9e167f9f6a05c48bf3b29fbce7.jpg)

![](images/b1d12e8e93ae60965e5f89b64fcff1379d8349dfdba939b71636e1ba88a2ec30.jpg)

![](images/34a331e4c64058d3bfea167908136592072095706cd2a7ca2a2c6b390ca8b73c.jpg)

![](images/98fbbd428df771f20f5c996d4f8a9e09cd6b41177dcae498a6472a3195654758.jpg)

(b)  
![](images/d58ddc3d694e20d0f5b417d7b16816767c6632d1d1d2600fab69f61ecd2c95f5.jpg)  
(e)

(c)  
(d)  
![](images/6ad84ced2393f38c06bd5b7ed5a92a0fbc1582694d69858b800119056d391790.jpg)  
(f)

![](images/c4fa40fdc7e185a7f5d515283e74c7dfdc3201dc200418d7a0b94d0eda6594cb.jpg)

![](images/7ea8ea5a61cd234f0191cee6d6d41f8ec2a3713723c0c9fd5493de4c4340e0e4.jpg)  
(h)

(i)  
![](images/77efe3cf614a3dfd08b72fc9ccb14f0c3e4b16ab8ababed87627afd0e7b845ca.jpg)  
(j)

(g)  
![](images/aafafbe9d3baa5156af433e6118afc74e53ed9acd89186bddc95b90cf1adb14a.jpg)  
(k)

![](images/b809f9571e0ebc79feeb6fc7567bf3d65168d31d07ad54b21fa3812068b1b870.jpg)  
(1)  
Fig. 18. RD maps of the automotive radar signals contaminated by different types of aggressor radars. First row: Short-range radar. (a) BKCS method (b) Hankel method. (c) SIE method. (d) Proposed TD method. Second row: Middle-range radar. (e) BKCS method. (f) Hankel method. (g) SIE method. (h) Proposed TD method. Third row: Far-range radar. (i) BKCS method. (j) Hankel method. (k) SIE method. (l) Proposed TD method.

TABLE IV  
CONFIGURATION IN STATIC AGGRESSOR FIELD EXPERIMENT WITH TWO INTERFERENCE SOURCES (WAV. = WAVEFORM)
<table><tr><td>Configurations</td><td>Aggressor 1</td><td>Aggressor 2</td><td>Victim</td><td>Unit</td></tr><tr><td>Start Frequency</td><td>76.67</td><td>77</td><td>76.5</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>6</td><td>32.23</td><td>-66.67</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>25.6</td><td>110</td><td>30</td><td> $\mu \mathrm { s }$ </td></tr><tr><td>Number of Fast Time Samples</td><td>512</td><td>512</td><td>512</td><td></td></tr><tr><td>Number of Slow Time Samples</td><td>64</td><td>64</td><td>64</td><td></td></tr></table>

![](images/5d1eafc18d8214db7e811c2296421fb544faf5499c4b356707f34f7e8fba90b1.jpg)  
Fig. 19. Setup of practical experiments with comparison.

![](images/84069cac2e7adcf31e41cce3ef5f3eb2d81fc8880d1be8219aa05311ee8d4236.jpg)  
(a)

![](images/e66608266ceb8f7370159b4b4950802f9bdfed6e46c990aedb58a92faaf4d238.jpg)  
(b)  
Fig. 20. The RD maps for (a) interference-free, (b) mutual interference contaminated data.

![](images/41ab680d4d4a7ecea5f4a4660c9a6b83e3d87f894a51824de4acc52461a43308.jpg)  
(a)

![](images/b1bafa13f3221052519707c40c19ea11a4f0ceb78f9c68111f3a8be7890ea0cf.jpg)  
(b)

![](images/d8a35ce4088c60c260ed6fb627c302a48f889f0fa164288dc9a6a1d2e3703dbf.jpg)

![](images/74661670edbcb44f6c2c1419c2f39f51b2ea747a1f916301a3f8e2c92012d0d4.jpg)  
(c)  
(d)

![](images/8744eb184fd6394a702e29faf4949bad249aa8a48dd8cb53c6d59a0ca262d2cd.jpg)  
(e)

![](images/f0836683ea64d4a4c2b4f98c5bd3ddaaea960069d60de05b24b85d68b64f1433.jpg)  
(f)

![](images/50943756388641297521d61a6a1186db053e9d4b4f76835a95c6de4deed0b3e2.jpg)  
(g)

![](images/f252fd57ea661e066135596ddad83fd0670ee9ca211fc4a4f9234c4b16701d1a.jpg)  
(h)

Fig. 21. Practical experiments with comparison results. The numbers are C-FAR detected targets. (a) Interference-free. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method. (g) SIE method. (h) Proposed TD method.  
![](images/b382410c247cc21a6c72cf76066a90c418221113c8b84bf58530f414dd4843b6.jpg)  
(a)

![](images/1f015c60834f098267e63b7574a879e2d375378e31d0bd9d680430d75bd2934c.jpg)  
(b)

![](images/69a032d49669f931ccfefaa51094d52312fe1e35fd3619e2602f07972550d950.jpg)

![](images/a92027d9860fcdd54c62577d7400eb57668dadc4a7a6dfdc0f375c7722bd1841.jpg)  
(d)

![](images/336d66760ebe7fb4d57c175c0517b1f3e6044e872381adb96e555899b033225c.jpg)  
(e)

![](images/2c23dbf176a83d49ebdfc4c65c4dc09b8e539ad456e7dcf764a4569d6e6bb56a.jpg)  
(f)

(c)  
![](images/c2f0d88aed487a3ae552a33d19f5b537b4aa66bbd835bd56dfb7cb846218f3a2.jpg)  
(g)

![](images/ef4993e79824732a865039149cc6d654025d1c9db02401f2cda7127cd4b5a939.jpg)  
(h)  
Fig. 22. Targets detection and parameters estimation of the practical experiments with comparison. The red stars present the three targets estimated from the interference-free data, and the yellow circles present the targets that are detected and estimated from mutual interference contaminated and algorithms processed data. (a) Interference-free. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method. (g) SIE method. (h) Proposed TD method.

TABLE V  
THE RMSE OF THE FOUR METHODS’ RESULT UNDER THREE DIFFERENT TYPES OF AGGRESSOR RADARS
<table><tr><td>Algorithms</td><td>Short-Range</td><td>Middle-Range</td><td>Far-Range</td></tr><tr><td>Before</td><td>3.6678e-04</td><td>8.8163e-04</td><td>1.0589e-03</td></tr><tr><td>BKCS</td><td>4.5875e-05</td><td>4.3841e-05</td><td>3.7749e-05</td></tr><tr><td>Hankel</td><td>3.3403e-05</td><td>3.6358e-05</td><td>3.9044e-05</td></tr><tr><td>SIE</td><td> $4 . 7 0 8 7 \mathrm { e } { - } 0 5$ </td><td> $4 . 3 8 4 1 { \mathrm { e } } { \mathrm { - } } 0 5$ </td><td>3.7749e-05</td></tr><tr><td>Proposed TD</td><td>2.8313e-05</td><td> $2 . 8 2 5 9 \mathrm { e } { - } 0 5$ </td><td> $2 . 8 2 0 0 \mathrm { e } { - } 0 5$ </td></tr></table>

The RD maps of interference-free and mutual interference contaminated data are shown in Fig. 20. As we can see from the figures, there are huge differences and the mutual interference is overwhelming the targets, making them impossible to detect nor estimate. Then we test all previous methods on this data and the recovered RD maps are shown in Fig. 21. And in Table. VII, we applied RMSE and SINR as the numerical measurements to qualify the interference mitigation performance of the proposed methods and the previous ones for comparison. The RMSE of TD method is smaller than the compared methods and SINR is larger, both of which indicate that the results processed by our method are more similar to interference-free RD map as well as better performance.

TABLE VI  
THE CONFIGURATION IN PRACTICAL EXPERIMENTS WITH COMPARISON
<table><tr><td>Configurations</td><td>Aggressor Radar</td><td>Victim Radar</td><td>Unit</td></tr><tr><td>Start Frequency</td><td>77</td><td>77.83</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>32.23</td><td>16.11</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>110</td><td>29.5</td><td>µs</td></tr><tr><td>Number of Fast Time Samples</td><td>512</td><td>512</td><td></td></tr><tr><td>Number of Slow Time Samples</td><td>64</td><td>64</td><td></td></tr></table>

TABLE VII

THE RMSE & SINR OF THE METHODS’ RESULT IN PRACTICAL EXPERIMENTS WITH COMPARISON
<table><tr><td>Algorithms</td><td>RMSE</td><td>SINR (dB)</td></tr><tr><td>Before</td><td>5.3440e-04</td><td>32.7213</td></tr><tr><td>Notch Method</td><td>8.7647e-05</td><td>40.5726</td></tr><tr><td>ANC Method</td><td>4.2373e-05</td><td>43.7291</td></tr><tr><td>BKCS Method</td><td>9.8068e-05</td><td>40.0847</td></tr><tr><td>Hankel Matrix Optimization Method</td><td>3.4328e-05</td><td>44.6336</td></tr><tr><td>CFAR-based Dilate Mask Method</td><td>9.2232e-04</td><td>40.3512</td></tr><tr><td>Sparse Interference Extraction Method</td><td>9.8068e-05</td><td>40.0847</td></tr><tr><td>Tensor Decomposition Method</td><td>2.8968e-05</td><td>45.3808</td></tr></table>

Also, we test the following steps, including target detection by a constant false alarm ratio (CFAR) detector and directionof-arrival (DOA) estimation by digital beamforming (DBF), on the recovered RD maps. The detected results are marked in RD maps and the DOA estimation results are shown in 22.

The numbers in Fig. 21 are CFAR detected targets. Since three targets are static, we omitted the velocity estimation here. It is easy to see from the RD maps that the points are in the middle of the diagrams and their velocity remains zero. To avoid repeated description of the RD maps, we will focus on discussion about DOA estimation of targets. As we can see from Fig. 22, the red stars present the three targets estimated from the interference-free data, and the blue circles present the targets that are detected and estimated from recovered RD maps in Fig. 21. The DOA estimation is mainly awful for those previous methods under this serve situation. However, the proposed TD method with protection of phase through low-rank restraints across the channel dimension, shows great superiority when it comes to parameter estimation.

## E. Vehicular Aggressor Field Experiment

Next, we implement a practical vehicular circumstance to testify the robustness of TD method in a more realistic environment. This experiment simulates the case that when a pedestrian moves in front of the victim radar and the other vehicles are running towards us in the other side of the road, as shown in Fig. 23. As we can see from Fig. 23, The aggressor radar, which is a middle-range automotive radar provided also by Hawkeye Technology Corporation, is implemented at the front bumper of the red car, as shown in Fig. 24. The victim radar is still the TI AWR2243BOOST mmWave radar, which is mounted in the other side of the road.

The radar configurations of both aggressor radar and victim radar for the experiment are listed in Table VIII. Both the aggressor radar and the victim radar still work at TDM. Similar to the above experiment, we also test all the aforementioned methods to testify the superiority of our proposed method. The interference-contaminated RD map and processed results are shown in Fig. 25.

![](images/14fc2b1c9543166a71cfd91fcd59c0aed04a1624f47adeaafe45a3e6b3c669ff.jpg)

Fig. 23. Setup of vehicular aggressor field experiment.  
![](images/ebb08b5a3dfc9285b624fc7f214e5b84aa8d3d45dde66ea6704b2aabfc28fd89.jpg)  
Fig. 24. The installment of the aggressor radar on the car.

Herein, we simplify the scene and park the red vehicle on the road as an aggressor radar. As shown in Fig. 25, we use red circles to frame out the aggressor car in the RD maps and yellow ones for the pedestrian. As we can see from Fig. 25 (a), the interference contaminates the whole RD map, leaving no differentiable bright points that may present the targets. Due to the complex interference circumstances, the amplitudes of the mutual interference are varying among chirps. After the processing of the notch method, as we can see from Fig. 25 (b), the notch method can removes most of interference effectively, but the noise floor is still too high to make targets bright enough for accurate detection. Also, the losses of target echoes in Fig. 25 (c) and (d) show the ineffectiveness of the ANC method and BKCS method in complex practical vehicular circumstances. Then in Fig. 25 (e), the Hankel matrix optimization method can remove most of the interference and reveal the targets, which has lower noise floor than the notch method. But there are still weak interference artifacts in the background, which still affects the target detection. Furthermore, the interference artifact backgrounds are severer in Fig. 25 (f) and (g), indicating that CFARbased dilate mask method and SIE method can not remove the interference completely. But the SIE method can make the true targets brighter than the background, which is very helpful for the following target detection. Regarding to the proposed TD method, it can not only remove the majority of the interference but also reveal targets in our experiment. As we can see from Fig. 25 (h), the point that represents the aggressor car is brighter, which is align to the fact that vehicle have much stronger reflection than the pedestrian. Also, the points that present the pedestrian are not positioned in the middle of the RD map, which indicates the velocity of the pedestrian. Both the pedestrian and the aggressor vehicle can be clearly seen and easily detected by the following Constant False Alarm Rate (CFAR) operation. The TD method processed RD map results across 12 channels is shown in Fig. 26.

TABLE VIII  
THE CONFIGURATION IN VEHICULAR AGGRESSOR FIELD EXPERIMENT
<table><tr><td>Configurations</td><td>Aggressor Radar</td><td>Victim Radar</td><td>Unit</td></tr><tr><td>Start Frequency</td><td>76.25</td><td>77</td><td>GHz</td></tr><tr><td>Frequency Slope</td><td>3</td><td>-20</td><td>MHz/µs</td></tr><tr><td>Chirp Duration</td><td>150</td><td>29.5</td><td>µs</td></tr><tr><td>Number of Fast Time Samples</td><td>512</td><td>512</td><td></td></tr><tr><td>Number of Slow Time Samples</td><td>64</td><td>64</td><td></td></tr></table>

![](images/9117b3496873c0ac4dad108bcb3ec96ba0afbb4bd25d80f9ab902cbdc041475e.jpg)  
(a)

![](images/9b1281a92416497629dd1416c8fbeeb18db6b1d06218e9fd4fab1f387826044b.jpg)  
(b)

![](images/0c02295d7f551577bc0dc6f8a135032a1321a563ff203ff005cf7c132be884eb.jpg)  
(c)

![](images/eeae55196ee1cfd8d95494b0e4d0aea9ada5c4d3500fedd2c79d054171e7eaf3.jpg)  
(d)

![](images/ae1a84f4abff73a8ec5792231580fc288dd4d16448da070c6275cd0789df4087.jpg)  
(e)

![](images/84fc06e49d0beb5048ba237ee46df1df57584a49c8da62894d46eaf25934af0b.jpg)  
(f)

![](images/78389d7fd219311eec6fd02cbad4b1e0bee39a376c4a5f94f56d07b66700fbe8.jpg)  
(g)

![](images/756674f08e5d514d92e07b0c5d5b2cf1a896ab200fd40f8cd1977e37d6239d17.jpg)  
(h)  
Fig. 25. Vehicular aggressor field experiment results. The red circles label the aggressor car and the yellow circles label the pedestrian. (a) Interference– contaminated RD map. (b) Notch method. (c) ANC method. (d) BKCS method. (e) Hankel matrix optimization method. (f) CFAR-based dilate mask method (g) SIE method. (h) Proposed TD method.

TABLE IX  
RUNNING TIME OF THE IMPLEMENTED METHODS IN VEHICULAR AGGRESSOR FIELD EXPERIMENT
<table><tr><td>Algorithms</td><td>Running Time (s)</td></tr><tr><td>Notch Method</td><td>0.812121</td></tr><tr><td>ANC Method</td><td>0.123829</td></tr><tr><td>BKCS Method</td><td>0.48691</td></tr><tr><td>Hankel Matrix Optimization Method</td><td>2504.827379</td></tr><tr><td>CFAR-based Dilate Mask Method</td><td>19.096195</td></tr><tr><td>Sparse Interference Extraction Method</td><td>0.477673</td></tr><tr><td>Tensor Decomposition Method</td><td>9.008966</td></tr></table>

## F. Running Time

Herein, the running times of the seven methods worked under the vehicular aggressor field experiment are listed in Table IX. As indicated in Table IX, good performance is obtained at the expense of a large amount of computational complexity. TD method, as an ADMM-based method, requires multiple iterations to reach convergence. Therefore, it has a heavier computational burden and requires a longer running time than the SIE method. The notch method requires detecting interference chirp by chirp and cannot process the data in a matrix, which would cause extra delay for MATLAB programming. Other methods that require no iteration can be fast but perform poorly. Besides, for methods that work chirp by chirp, the running time is much longer, especially for the Hankel matrix optimization method which iterates chirp by chirp and the running time is significantly larger than all the other methods.

![](images/3136ec11dbae8d003d4bbfde42d36de53ee34867b67ba188e694f194d6db4e47.jpg)  
(a)

![](images/cd3274bc056c963d701a538b428aa2664dd9316286ddd438cb80c27a43f28d1d.jpg)  
(b)

![](images/0cdf56840fb15a3590e078dbe2146ed59c2bd69320851ce01a4f1aac67789ab9.jpg)  
(e)

![](images/8cc7c11ff2c1a564cf686ba773bd9b13122d983edd9880fb07b44cd547dfd672.jpg)

![](images/26346450d55153f67701b1fed7fe56d5b67140d7fe1bb715c36700ce8a3e83e5.jpg)  
(f)  
(c)

(d)  
![](images/64e3bd3664b41c3ddfcf1715b9b86cf30737ab6cf91098b660c9245a6f764c98.jpg)

![](images/c78959728e37e54687805c93911b12e43d15821b53c547f75ba8d88578d0d33f.jpg)

![](images/04a4a30a4153e7dcc79db3f162118285625ffeccd197d09c9a1d4883ceeafbea.jpg)

![](images/4dd31e60491baeee69ddd62b0da3022548424e84f13b31e09a7c9f6cff4fe21c.jpg)  
(i)

(h)  
![](images/7186e950828635221158ef6e07d317e7b5519ad088966f7ebb9bb820cf76302a.jpg)  
(j)

(g)  
![](images/6b42b3b7f568bb56c693f9dce013d8662960061c807bc0deb5a02a052d132cda.jpg)  
(k)

![](images/49a4dad614129519b914df6594484449744428b7f53c132b81a87cd803e99a16.jpg)  
(1)  
Fig. 26. Vehicular aggressor field experiment results of the TD method across 12 channels.

## VII. CONCLUSION

In this paper, we rigorously derived the signal features of received signals and mutual interference in detail. As a result, we considered the sparsity of the mutual interference in the time domain and the low-rank property of the useful echo signals across multiple channels of the automotive multipleinput multiple-output (MIMO) radar, and then proposed a novel spatial-time three-dimensional (3-D) tensor decomposition (TD) method to mitigate the mutual interference and protect useful echoes. Based on the sparsity of mutual interference, we also proposed the SIE method as a comparison to demonstrate a better representation of the TD method in both theory and application. Finally, we implemented several practical experiments to testify the feasibility of the TD method compared with other state-of-the-art methods in real automotive circumstances.

## REFERENCES

[1] K. A. Brookhuis, D. De Waard, and W. H. Janssen, “Behavioural impacts of advanced driver assistance systems—An overview,” Eur. J. Transp. Infrastruct. Res., 2019, doi: 10.18757/ejtir.2001.1.3.3667.

[2] U. Z. A. Hamid et al., “Autonomous emergency braking system with potential field risk assessment for frontal collision mitigation,” in Proc. IEEE Conf. Syst., Process Control (ICSPC), Dec. 2017, pp. 71–76, doi: 10.1109/SPC.2017.8313024.

[3] R. Singh, D. Saluja, and S. Kumar, “Blind cancellation in radarbased self driving vehicles,” IEEE Trans. Veh. Technol., vol. 69, no. 7, pp. 6977–6986, Jul. 2020.

[4] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019, doi: 10.1109/MSP.2019.2908214.

[5] Allied Market Research Automotive RADAR Market by Application. Accessed: 2021. [Online]. Available: https://www.alliedmarketresearch. com/automotive-radar-market

[6] Operation Radar Services 76–81 GHz Band, Federal Commun. Commission, Washington, DC, USA, 2015.

[7] G. Hakobyan and B. Yang, “A novel intercarrier-interference free signal processing scheme for OFDM radar,” IEEE Trans. Veh. Technol., vol. 67, no. 6, pp. 5158–5167, Jun. 2018, doi: 10.1109/TVT.2017.2723868.

[8] M. Alhumaidi and M. Wintermantel, “Interference avoidance and mitigation in automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 172–175, doi: 10.1109/EuRAD48048.2021.00053.

[9] J. Fuchs, A. Dubey, M. Lübke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320, doi: 10.1109/RADAR42522.2020.9114641.

[10] S. Chen, J. Taghia, U. Kühnau, N. Pohl, and R. Martin, “A twostage DNN model with mask-gated convolution for automotive radar interference detection and mitigation,” IEEE Sensors J., vol. 22, no. 12, pp. 12017–12027, Jun. 2022, doi: 10.1109/JSEN.2022.3173129.

[11] S. Chen, W. Shangguan, J. Taghia, U. Kühnau, and R. Martin, “Automotive radar interference mitigation based on a generative adversarial network,” in Proc. IEEE Asia–Pacific Microw. Conf. (APMC), Dec. 2020, pp. 728–730, doi: 10.1109/APMC47863.2020.9331379.

[12] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2020, pp. 3802–3806, doi: 10.1109/ICASSP40776.2020.9053013.

[13] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 624–629, doi: 10.1109/RADAR42522.2020.9114627.

[14] J. Rock, W. Roth, P. Meissner, and F. Pernkopf, “Quantized neural networks for radar interference mitigation,” 2020, arXiv:2011.12706.

[15] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021, doi: 10.1109/JSTSP.2021.3062452.

[16] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in Proc. IEEE 92nd Veh. Technol. Conf. (VTC-Fall), Nov. 2020, pp. 1–5, doi: 10.1109/VTC2020-Fall49728.2020.9348690.

[17] K. U. Mazher, R. W. Heath Jr., K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in Proc. IEEE Radar Conf., Sep. 2020, pp. 1–6, doi: 10.1109/Radar-Conf2043947.2020.9266425.

[18] M. Zhang, S. He, C. Yang, J. Chen, and J. Zhang, “VANETassisted interference mitigation for millimeter-wave automotive radar sensors,” IEEE Netw., vol. 34, no. 2, pp. 238–245, Mar. 2020, doi: 10.1109/MNET.001.1900271.

[19] P. Park, H. Khadilkar, H. Balakrishnan, and C. Tomlin, “Hybrid communication protocols and control algorithms for NextGen aircraft arrivals,” IEEE Trans. Intell. Transp. Syst., vol. 15, no. 2, pp. 615–626, Apr. 2014, doi: 10.1109/TITS.2013.2285116.

[20] R. Singh, D. Saluja, and S. Kumar, “Spread spectrum coded radar for R2R interference mitigation in autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 10418–10426, Aug. 2022, doi: 10.1109/TITS.2021.3094199.

[21] R. Singh, D. Saluja, and S. Kumar, “TRAP: Traffic-based adaptive ramp packing for blind cancellation in autonomous vehicles,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 13884–13889, Aug. 2022, doi: 10.1109/TITS.2021.3091505.

[22] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021, doi: 10.1109/TITS.2019.2959881.

[23] A. Al-Hourani, R. J. Evans, S. Kandeepan, B. Moran, and H. Eltom, “Stochastic geometry methods for modeling automotive radar interference,” IEEE Trans. Intell. Transp. Syst., vol. 19, no. 2, pp. 333–344, Feb. 2018, doi: 10.1109/TITS.2016.2632309.

[24] L. Lan, J. Xu, G. Liao, Y. Zhang, F. Fioranelli, and H. C. So, “Suppression of mainbeam deceptive jammer with FDA-MIMO radar,” IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 11584–11598, Oct. 2020, doi: 10.1109/TVT.2020.3014689.

[25] F. Uysal and S. Orru, “Phase-coded FMCW automotive radar: Application and challenges,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 478–482, doi: 10.1109/RADAR42522.2020.9114798.

[26] T. Fei, H. Guang, Y. Sun, C. Grimm, and E. Warsitz, “An efficient sparse sensing based interference mitigation approach for automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 274–277, doi: 10.1109/EuRAD48048.2021.00077.

[27] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019, doi: 10.1109/TVT.2019.2901493.

[28] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022, doi: 10.1109/TSP.2022.3147863.

[29] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270–5283, Dec. 2021, doi: 10.1109/TMTT.2021.3121322.

[30] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018, doi: 10.1109/LGRS.2017.2777962.

[31] M. Rameez, M. I. Pettersson, and M. Dahl, “Interference compression and mitigation for automotive FMCW radar systems,” IEEE Sensors J., vol. 22, no. 20, pp. 19739–19749, Oct. 2022, doi: 10.1109/JSEN.2022.3204505.

[32] J. Li and P. Stoica, MIMO Radar Signal Processing. Hoboken, NJ, USA: Wiley, 2009.

[33] Z. Xu, “Bi-level l1 optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, Jan. 2023, doi: 10.1109/TITS.2022.3215636.

[34] A. Hassanien and S. A. Vorobyov, “Transmit/receive beamforming for MIMO radar with colocated antennas,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., Apr. 2009, pp. 2089–2092, doi: 10.1109/ ICASSP.2009.4960027.

[35] R. Feger, C. Wagner, S. Schuster, S. Scheiblhofer, H. Jager, and A. Stelzer, “A 77-GHz FMCW MIMO radar based on an SiGe singlechip transceiver,” IEEE Trans. Microw. Theory Techn., vol. 57, no. 5, pp. 1020–1035, May 2009, doi: 10.1109/TMTT.2009.2017254.

[36] Y. Yao, H. Liu, P. Miao, and L. Wu, “MIMO radar design for extended target detection in a spectrally crowded environment,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 9, pp. 14389–14398, Sep. 2022, doi: 10.1109/TITS.2021.3127727.

[37] Z. Liu, J. Wu, S. Yang, and W. Lu, “DOA estimation method based on EMD and MUSIC for mutual interference in FMCW automotive radars,” IEEE Geosci. Remote Sens. Lett., vol. 19, pp. 1–5, 2022, doi: 10.1109/LGRS.2021.3058729.

[38] F. Wu, Y. Li, C. Li, and Y. Wu, “A fast tensor completion method based on tensor QR decomposition and tensor nuclear norm minimization,” IEEE Trans. Comput. Imag., vol. 7, pp. 1267–1277, 2021, doi: 10.1109/TCI.2021.3130977.

[39] M. E. Kilmer and C. D. Martin, “Factorization strategies for thirdorder tensors,” Linear Algebra its Appl., vol. 435, no. 3, pp. 641–658, Aug. 2011.

[40] C. Lu, J. Feng, Y. Chen, W. Liu, Z. Lin, and S. Yan, “Tensor robust principal component analysis: Exact recovery of corrupted low-rank tensors via convex optimization,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Las Vegas, NV, USA, Jun. 2016, pp. 5249–5257.

[41] R. Amiri, F. Behnia, and M. A. M. Sadr, “Exact solution for elliptic localization in distributed MIMO radar systems,” IEEE Trans. Veh. Technol., vol. 67, no. 2, pp. 1075–1086, Feb. 2018, doi: 10.1109/TVT.2017.2762631.

[42] N. Kehtarnavaz, Frequency Domain Processing, Digital Signal Processing System Design (Second Edition), 2nd ed. New York, NY, USA: Academic, 2008, ch. 7, pp. 175–196, doi: 10.1016/B978-0-12-374490- 6.00007-6.

[43] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022, doi: 10.1109/TITS.2021.3111514.

![](images/b40d322f758f43217c83257db1b1e07d33b6ba65be2638aaaa832866ef401055.jpg)  
Yunxuan Wang received the B.Eng. degree from Southeast University, Nanjing, China, in 2022. She is currently pursuing the Ph.D. degree with the Department of Electrical and Electronic Engineering, Imperial College London, London, U.K. She was a Research Assistant with the University of Colorado at Boulder, Boulder, CO, USA, for one year. Her research interests include tensor algebra, machine learning, and convex optimization.

![](images/628cc49ee932125bbd5684b5209b1fdeef62567b6d92e31b6d04b9163ecc0a03.jpg)

Yan Huang (Member, IEEE) received the B.S. degree in electrical engineering and the Ph.D. degree in signal and information processing from Xidian University, Xi’an, China, in 2013 and 2018, respectively.

He is currently an Associate Professor with the State Key Laboratory of Millimeter Waves, Southeast University. His research interests include machine learning, synthetic aperture radar, image processing, and remote sensing.

![](images/bbc68d098f212095bf96938f1cf7416984069273a15e9d150232ebeb043dadfd.jpg)

Jiang Liu (Student Member, IEEE) received the B.S. degree in information engineering from Southeast University, Nanjing, China, in 2021, where he is currently pursuing the Ph.D. degree in electromagnetic fields and microwaves.

His main research interests include millimeterwave radar signal processing and artificial intelligence information processing.

![](images/d44d390d3f1f770c61132332435d1ad8877f7cc3133a3486e98fdd2c0e6a5a63.jpg)

Ruizhe Zhang received the bachelor’s degree in electromagnetic fields and wireless technology from Northwestern Polytechnical University, Xi’an, China, in 2018, and the master’s degree in electronic information from Southeast University, Nanjing, China, in 2023. His expertise lies in developing robust interference mitigation algorithms to enhance radar performance and reliability, contributing to safer, and more efficient driving experiences. His current work focuses on advancing millimeter-wave radar signal processing and data processing algorithms for future automotive and industrial applications.

![](images/98a89c884d12f285357134de730e7a2dd846c8c81a6bc33a5abd75820167c645.jpg)

Hui Zhang (Member, IEEE) was born in Suzhou, Anhui, China, in 1980. He received the B.S. degree from Southeast University, Nanjing, China, in 2002, the M.S. degree from the University College of Kalmar, Kalmar, Sweden, in 2007, and the Ph.D. degree from Southeast University in 2016. He is currently an Associate Professor with the State Key Laboratory of Millimeter Waves, Southeast University. His research interests include multibeam antennas, millimeter-wave imaging, and millimeterwave radar systems.

![](images/8f6f9f1ef005f8f1b458c80a26bd2d04aa854bb81e2e15b7f1bfb6ad345ed31c.jpg)

Wei Hong (Fellow, IEEE) received the B.S. degree from the University of Information Engineering, Zhengzhou, China, in 1982, and the M.S. and Ph.D. degrees from Southeast University, Nanjing, China, in 1985 and 1988, respectively, all in radio engineering.

Since 1988, he has been with the State Key Laboratory of Millimeter Waves, Southeast University, where he has been serving as the Director since 2003 and is currently a Professor with the School of Information Science and Engineering. In 1993,

1995, 1996, 1997, and 1998, he was a short-term Visiting Scholar with the University of California at Berkeley, Berkeley, CA, USA, and the University of California at Santa Cruz, Santa Cruz, CA, USA. He has been engaged in numerical methods for electromagnetic problems, millimeter-wave theory and technology, antennas, and RF technology for wireless communications. He has authored or coauthored more than 300 technical publications and two books.

Dr. Hong is a fellow of CIE, the Vice President of the CIE Microwave Society and Antenna Society, and the Chair of the IEEE MTT-S/AP-S/EMC-S Joint Nanjing Chapter. He was an elected IEEE MTT-S AdCom Member from 2014 to 2016. He was awarded twice the National Natural Prizes and thrice the First-Class Science and Technology Progress Prizes issued by the Ministry of Education of China and Jiangsu Province Government. Besides, he also received the Foundations for China Distinguished Young Investigators and for “Innovation Group” issued by NSF, China. He has served as an Associate Editor for the IEEE TRANSACTIONS ON MICROWAVE THEORY AND TECHNIQUES (TMTT) from 2007 to 2010.