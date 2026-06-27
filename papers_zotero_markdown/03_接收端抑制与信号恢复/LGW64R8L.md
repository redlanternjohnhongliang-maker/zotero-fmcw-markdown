RESEARCH

Open Access

#

![](images/c076237c06c72df41bce3f1bb18231b410f76ededf760e5d81f0c0b17b14fe9f.jpg)

Shengyi Chen<sup>1,2\*</sup> , Philipp Stockel<sup>3</sup>, Jalal Taghia<sup>2</sup>, Uwe Kühnau<sup>2</sup> and Rainer Martin<sup>1</sup>

\*Correspondence:   
shengyi.chen@rub.de   
<sup>1</sup> Institute of Communication Acoustics, Ruhr-Universität Bochum, Bochum, Germany Full list of author information is available at the end of the article

## Abstract

Compressive sensing has attracted considerable attention in automotive radar interference mitigation. However, these algorithms usually cannot be applied directly to commercial automotive radar as most of them are computationally intense. In this paper, we therefore introduce a computationally efcient two-dimensional masked residual updates (2D MRU) compressive sensing framework. By utilizing the sparsity of the beat signal in the frequency domain, the range-Doppler (RD) spectrum can be reconstructed with the help of undistorted samples in the beat signal. Unlike the other schemes, where a 2D signal measurement is vectorized into a 1D signal, the proposed 2D MRU can directly take a 2D signal measurement and reconstruct the corresponding RD spectrum. Furthermore, the 2D MRU framework can be easily integrated into wellknown optimization schemes such as basis pursuit, iterative hard thresholding, iterative soft thresholding, orthogonal matching pursuit, and approximate message-passing algorithm. In addition to the standard iterative thresholding algorithms, we propose a novel prior-model-based iterative thresholding method to further reduce the computation time and reconstruction error. Theoretical analysis shows that the proposed framework can successfully reconstruct the RD spectrum with high probability. Moreover, numerical experiments demonstrate the superiority of the proposed framework in terms of computational complexity.

Keywords: Automotive radar, Interference mitigation, 2D compressive sensing, Prior model based iterative thresholding

## 1 Introduction

Automotive radar plays an important role in advanced driver assistant systems as it can provide reliable safety support for modern vehicles under almost all weather conditions. To achieve a higher level of automated driving, the number of vehicles equipped with radar sensors and the number of radar sensors per vehicle are increasing rapidly. Tus, mutual interference between automotive radars increases due to the rising density of radar sensors on the road [1]. Since unexpected interference can impede the object detection by either reducing the signal-to-noise ratio (SNR) or creating ghost targets [2, 3]. Tus, mutual interference can afect the functionality of radar sensors if no countermeasures are taken.

## 1.1 Prior work

Diferent signal reconstruction algorithms, such as the zeroing method, autoregressive (AR) model-based interpolation and adaptive noise cancellation have been proposed as countermeasures for automotive radar interference mitigation [1, 4–6]. Te zeroing method [1] is a basic technique in which the signal segment disturbed by interference is simply set to zero. In [4], a complex band receiver and an adaptive noise canceller are utilized for interference mitigation, it cancels the interference in the positive half of the frequency spectrum ( 0, π normalized frequency), while it uses the correlated interference in the negative half of the frequency spectrum ( π, 0 normalized frequency) as a reference. Solving the mutual interference issue in the frequency domain for frequency-modulated continuous wave (FMCW) radar is also considered in [5], where the signal disturbed by interference is recovered by linear predictive coding (LPC) in the short-time Fourier transform (STFT) domain. However, the interference in real-world scenarios can contain much diversity and randomness, e.g., the chirp rates of diferent radar sensors can be similar to each other, and there can be multiple sources of interference. Hence, the samples disturbed by interference in some chirps may spread across the entire measurement. Tus, the number of available interference-free samples in these chirps is not sufcient for LPC to provide adequate recovery in the STFT domain. Different to [5], the AR model is used in [6] for the discrete beat signal interpolation in the positions which are disturbed by interference.

Recent research results have shown that compressive sensing (CS) approaches can be used to tackle this problem [7–10]. In [7], the samples disturbed by interference are frst substituted with zeros and these zeroed samples are further interpolated using the iterative method with an adaptive thresholding (IMAT) algorithm. In [8], the interference is removed by using the orthogonal matching pursuit (OMP) algorithm to project the interference-contaminated signals on a reduced chirplet basis which contains possible hypotheses for slopes and time-shifts of chirps. Te interference mitigation problem is defned as a dual-basis pursuit problem and the morphological component analysis is used in [9] for separating the interference from the discrete beat signal. In [10], the sparse Bayesian learning algorithm is adopted for automotive radar interference mitigation. Te range-Doppler (RD) spectrum can be acquired from the mean of the maximum a posteriori (MAP) estimate under the given remaining undistorted samples in the discrete beat signal. Most recently, the wavelet denoising technique was proposed to suppress the mutual interference in the time domain [11]. However, to apply this method in practical automotive radar systems, the threshold values related to the wavelet coeffcients need to be optimized on the basis of large amounts of real world data and the interference with similar amplitude as the echo signal of the target may still remain after reconstruction.

## 1.2 Motivation and contribution

As exemplifed above, CS algorithms usually provide better signal recovery than conventional algorithms but might require more computational resources.

Terefore, we propose a novel solution for the interference mitigation that can efciently reconstruct the RD spectrum by directly processing the two-dimensional (2D) discrete beat signal. Te proposed 2D masked residual updates (2D MRU) CS framework can be easily integrated into most existing CS schemes as well as the proposed novel prior-model-based iterative thresholding methods. Specifcally, the main contributions of this paper are as follows:

Firstly, we propose a novel prior-model-based iterative thresholding method that achieves smaller reconstruction error and computation time than corresponding baseline algorithms. Te update rate (typically 20 Hz) [12] in automotive radar systems indicates that rich prior information can be provided for interference mitigation, since the perceived environment may change only slightly during the short measurement cycles.

Secondly, a computationally efcient 2D MRU CS framework for RD spectrum recovery is introduced. 2D MRU avoids large vectors and high-dimensional matrix operations which typically come along with an increasing size of the measurement matrix.

Tirdly, the measurement transform matrix used in this paper is proven to satisfy the restricted isometry property (RIP) with high probability. In other words, the proposed framework can successfully reconstruct the RD spectrum with a high probability.

Fourthly, it is demonstrated that the proposed 2D MRU can be easily integrated to the established CS schemes e.g., basis pursuit, iterative soft thresholding (IST), iterative hard thresholding (IHT), OMP, approximate message-passing (AMP) and the proposed priormodel-based iterative thresholding algorithms. Te performance of diferent algorithms that incorporate 2D MRU is evaluated and the superiority of the proposed framework in terms of computational complexity is shown.

Finally, a detection method with a higher true-positive rate is proposed for the detection of interference-contaminated samples. Te detection method can be further combined with the state-of-the-art CS frameworks as well as with 2D MRU.

## 1.3 Organization and notations

Te organization of this paper is as follows. In Sect. 2, the frequency-modulated continuous wave radar signal model is introduced. Section 3 describes the details of the proposed prior-model-based iterative thresholding algorithms and 2D framework and we prove that the proposed framework can successfully reconstruct the RD spectrum with high probability. In Sect. 4, an algorithm for the detection of interference-contaminated samples is proposed. Te performance of the proposed method is evaluated through real measurements in Sect. 5. Finally, Sect. 6 concludes this paper.

Notations: We denote vectors by boldface lower-case symbols and matrices by boldface upper-case symbols. Te support set of a sparse signal is denoted as supp( ). Te empirical mean of a signal is denoted as  and the standard deviation is represented as std( ). F is the Frobenius norm and vec( ) denotes the vectorization of a matrix by stacking the columns. Te lower bound and upper bound on the complexity of an algorithm are represented by  and O, respectively.

## 2 Automotive FMCW radar signal model

Te chirp sequence modulation [13] which is a currently widespread variant of FMCW in automotive radar system, contains M consecutive chirps, and its transmit waveform can be represented as

$$
T _ { x } ( t ) = \sum _ { m = 0 } ^ { M - 1 } x ( t - m T ) .\tag{1}
$$

Te individual transmit chirp signal is given by

$$
\begin{array} { r } { \boldsymbol { x } ( t ) = \exp \biggl ( j 2 \pi \biggl ( f _ { c } t + 0 . 5 \alpha t ^ { 2 } \biggr ) \biggr ) \mathrm { r e c t } _ { T } ( t ) , } \end{array}\tag{2}
$$

$f _ { c }$ $\alpha = B / T$

$$
\begin{array} { r } { r _ { m } ( t ) = A _ { m } x ( t + ( t + m T ) d - \tau ) + \mathrm { v } _ { m } ( t ) , } \end{array}\tag{3}
$$

where $A _ { m }$ is the received amplitude, $\tau = 2 R / c , \ d = 2 \nu / c$ , and ${ \tt V } _ { m }$ denotes complex Gaussian noise. Here, R and v denote, respectively, the distance and relative radial velocity between the radar and the target, and c represents the speed of light. Te beat signal at the intermediate frequency can be obtained after stretch processing, namely mixing $r _ { m }$ with the complex conjugate of the transmitted signal: $\hat { y } _ { m } ( t ) = r _ { m } ( t ) x ^ { * } ( t )$ . After fltering and sampling with a period of $T _ { s }$ and collecting N samples per chirp, the discrete beat signal can be approximated as [2]

$$
\begin{array} { c } { { \hat { y } _ { n , m } \approx A _ { m } \exp \left( j 2 \pi \left( - \alpha \tau + f _ { c } d \right) n T _ { s } \right) } } \\ { { \mathrm { } \cdot \exp \left( j 2 \pi \left( f _ { c } d m T \right) \right) + \nu _ { n , m } n \in [ 0 , N - 1 ] . } } \end{array}\tag{4}
$$

With the assumption that $\check { y } _ { m , n }$ represents the additive in-band interference, which can be induced by various sources of interference [14, 15], the discrete beat signal $\mathbf { y } = \{ y _ { ( m \cdot N + n ) } \}$ for $0 \leq m \leq M - 1$ and $0 \leq n \leq N - 1$ can be therefore summarized as

$$
y _ { ( m \cdot N + n ) } = \left\{ \begin{array} { l l } { \hat { y } _ { n , m } + \mathbf { v } _ { n , m } \qquad m \cdot N + n \in H } \\ { \hat { y } _ { n , m } + \check { y } _ { n , m } + \mathbf { v } _ { n , m } \quad m \cdot N + n \not \in H , } \end{array} \right.\tag{5}
$$

where H is the set of sample indices without interference and m $N + n \not \in H$ denotes the indices of the samples containing interference. Figure 1 shows examples of interferencefree and interference-contaminated discrete beat signals.

We now explain the two diferent signal models which will play an essential role in this paper.

![](images/20585fe3d8b6c0f5cc25137ddfd1002bfce8ab6b9baf8943f1f17e2f5bcce9f9.jpg)

![](images/513bafda3e6dc3884bcc83931a21182705eba3238bd2d93834cd05e78386f2cf.jpg)  
Fig. 1 Example of a discrete beat signal without (a) and with (b) interference

## 2.1 Summary of signal model in matrix form

To obtain target range and velocity, the 2D discrete Fourier transform (DFT) can be applied on the discrete beat signal matrix $\mathbf { Y } = \{ y _ { n , m } \} \in \mathbb { C } ^ { N \times M }$

$$
\mathbf { X } = \mathbf { W } _ { N } \cdot \mathbf { Y } \cdot \mathbf { W } _ { M } ^ { T }\tag{6}
$$

where $\mathbf { W _ { N } } \in \mathbb { C } ^ { N \times N } , \mathbf { W _ { M } } \in \mathbb { C } ^ { M \times M }$ are DFT matrices (as defned in Appendix A), and $\mathbf { X } \in \mathbb { C } ^ { N \times M }$ denotes the 2D RD spectrum. Figure  4a shows an example RD spectrum without interference and Fig. 4b shows an example RD spectrum with interference.

## 2.2 Summary of signal model in vector form

Based on the 2D signal model in matrix form, the one-dimensional (1D) vector form of the signal model can be formulated. $\mathbf { x } \in \mathbb { C } ^ { M N \times 1 }$ denotes the vector form of the RD spectrum and can be obtained by

$$
\begin{array} { r } { \mathbf { x } = ( \mathbf { W _ { M } } ^ { T } \otimes \mathbf { W _ { N } } ) \cdot \mathbf { y } , } \end{array}\tag{7}
$$

where  represents the Kronecker product and $\mathbf { y } = ( y _ { O } , . . . , y _ { M N - 1 } ) ^ { T } \in \mathbb { C } ^ { M N \times 1 }$

## 3 Compressive sensing framework for radar interference mitigation

## 3.1 Compressive sensing

Compressive sensing has shown its strength in reconstructing sparse signals using far fewer samples than required by the Nyquist sampling theorem [16]. It requires a transform domain that provides a sparse representation of the observed signal. Its sensing structure, i.e. the measurement transform matrix, has to satisfy the restricted isometry property [17]. Te transform domain with the low-dimensional representation is called sparse domain. A signal having k nonzero coefcients in the sparse domain is called k-sparse. Generally, the sparsity of the signal y is measured by the $l _ { 0 }$ pseudo norm of its representation vector x where the $l _ { 0 }$ pseudo norm denotes the cardinality of the support of x [18]:

![](images/96d7bce3de8ae2991a0378ede3b666b4985c4ff1bbdb2ff88e748c609faac051.jpg)  
Fig. 2 Compressive sensing framework adopted to radar interference mitigation

$$
\| \mathbf { x } \| _ { 0 } = \mathrm { c a r d } \{ \mathrm { s u p p } ( \mathbf { x } ) \} = k .\tag{8}
$$

Te representation of the beat signal in most automotive radar application scenarios is sparse in the RD spectrum. Hence, the interference-pruned discrete beat signal can be seen as the beat signal with a reduced sampling rate and its sparse representation can be restored by the CS algorithm. Te 1D signal model in vector form can be easily connected to the CS framework. Te measurement transform matrix can be written as $\tilde { \mathbf { W } } = \tilde { \mathbf { W } } _ { \mathbf { M } } \otimes \tilde { \mathbf { W } } _ { \mathbf { N } } \in \mathbb { C } ^ { M N \times M N }$

Te dimensions of the inverse DFT (IDFT) matrices $\tilde { \mathbf { W } } _ { \mathbf { N } }$ and $\tilde { \mathbf { W } } _ { \mathbf { M } }$ are $N \times N$ and $M \times M$ (see Appendix $\mathrm { A } ) ,$ respectively.

Assume that the number of all undisturbed samples across all chirps in (5) is $q .$ Tus, the resulting beat signal vector is given by $\tilde { \mathbf { y } } = ( y _ { i _ { 0 } } , . . . , y _ { i _ { q - 1 } } ) ^ { T }$ with $0 < q < M N$ and $\{ i _ { 0 } , . . . , i _ { q - 1 } \} \subset \{ 0 , . . . , M N - 1 \}$ , and $\tilde { \Psi } = \left( \psi _ { i _ { 0 } } ^ { T } , . . . , \psi _ { i _ { q - 1 } } ^ { T } \right)$ where $\pmb { \psi } _ { i _ { q - 1 } }$ denotes the $i _ { q }$ -th row vector in matrix $\tilde { \mathbf { W } }$ . Te radar interference mitigation problem can be rephrased as the reconstruction of the sparse vector x from the noisy measurement $\tilde { \mathbf { y } } = \tilde { \Psi } \mathbf { x }$ . Tis problem is equivalent to solving an underdetermined set of linear equations. An illustration of how to utilize the 1D CS framework for the interference mitigation of the automotive radar signal is presented in Fig. 2.

Under the condition that x is sparse, the problem can be reduced to a minimization problem:

$$
\mathrm { P } _ { 0 } : \hat { \mathbf { x } } = \underset { \mathbf { x } \in \mathbb { C } ^ { \mathbf { M N } } } { \operatorname { a r g m i n } } \ : \bigg \{ \frac { 1 } { 2 } | | \tilde { \mathbf { y } } - \tilde { \Psi } \mathbf { x } | | _ { 2 } ^ { 2 } + \nu | | \mathbf { x } | | _ { 0 } \bigg \} ,\tag{9}
$$

$l _ { 0 } .$ $\mathrm { P } _ { 0 }$ $l _ { 1 } .$ $l _ { 0 } .$ $l _ { 1 } .$

$$
\mathrm { P } _ { 1 } : \hat { \mathbf { x } } = \operatorname * { a r g m i n } _ { \mathbf { x } \in \mathbb { C } ^ { \mathbf { M N } } } \bigg \{ \frac { 1 } { 2 } | | \tilde { \mathbf { y } } - \tilde { \Psi } \mathbf { x } | | _ { 2 } ^ { 2 } + \nu | | \mathbf { x } | | _ { 1 } \bigg \} .\tag{10}
$$

Since $\mathrm { P _ { 1 } }$ is convex, efcient solvers can be used, such as iterative shrinkage-thresholding pursuit [20]. Alternative reconstruction algorithms include greedy-type methods such as OMP [21, 22], as well as thresholding-based methods [23–25] and the AMP algorithm [26]. Tese algorithms can be easily integrated in the framework shown in Fig. 2. However, the efciency of this framework is limited as it vectorizes the 2D signal measurement in automotive radar system to a 1D vector of dimension MN.

## 3.2 Restricted isometry property

In order to successfully recover a good estimate of signal x, the measurement transform matrix $\tilde { \Psi }$ in (10) should satisfy the restricted isometry property [17].

Te selection of the measurement transform matrix has been analyzed in [18, 27]. It is shown that a random partial Fourier matrix satisfes a near-optimal RIP with high probability [27, 28]. In this work, the theoretical analysis on RIP of the measurement transform matrix $\tilde { \Psi }$ is further conducted in Lemma 1 and Teorem 1 given in Appendix B. Teorem 1 shows that $\tilde { \Psi }$ satisfes the RIP with high probability.

## 3.3 Structure of 1D algorithms for RD spectrum recovery

In this subsection we introduce the novel prior-model-based iterative sparsity-promoting algorithms employed in conjunction with the 1D formulation of our interference mitigation approach.

## 3.3.1 Prior‑model‑based iterative thresholding

$$
\begin{array} { r } { \mathbf { r } _ { t } = \tilde { \mathbf { y } } - \tilde { \Psi } \mathbf { x } _ { t } , } \\ { \mathbf { x } _ { t + 1 } = \mathcal { T } _ { \lambda } ( \mathbf { x } _ { t } + \vartheta \tilde { \mathbf { y } } ^ { T } \mathbf { r } _ { t } ) . } \end{array}\tag{11}
$$

Here $\tilde { \Psi } ^ { T } \mathbf { r } _ { t } = \tilde { \Psi } ^ { T } ( \tilde { \mathbf { y } } - \tilde { \Psi } \mathbf { x } _ { t } )$ represents the gradient of the approximation error (residual $\mathbf { r } _ { t } )$ in the t-th iteration of the algorithm. $\mathcal { T } _ { \lambda } ( \cdot )$ denotes a nonlinear function that promotes the sparsity of the solution. Te parameter $0 < \vartheta \leq 1$ infuences the convergence speed. Hard thresholding and soft thresholding have been shown to be two possibilities for the nonlinear function $\tau _ { \lambda } ( \cdot ) ,$ where <sup></sup> denotes the threshold value.

For the algorithms to run as efciently as possible, the choice of the threshold value <sup></sup> is crucial. It can remain constant for all iterations, decrease by a fxed multiplicative factor in each iteration, or be adaptively adjusted to the signal properties in each iteration. An adaptive adjustment can be derived by considering the gradient term $\tilde { \Psi } ^ { T } \mathbf { r } _ { t }$ Assuming that the values in this term correspond to a Gaussian distribution with zero mean and standard deviation std $( \tilde { \Psi } ^ { T } \mathbf { r } _ { t } )$ , the threshold is given by

$$
\lambda _ { t } = \beta \cdot \mathrm { s t d } ( \tilde { \Psi } ^ { T } \mathbf { r } _ { t } ) ,\tag{12}
$$

where $\beta$ is the threshold control parameter, typically in the range $2 < \beta < 4 \left[ 3 0 \right]$ . Tis efectively reduces the noise in the representation by assuming that small signal values are part of the noise.

Since the typical measurement cycle of an automotive radar sensor is around 50 milliseconds [12], the observed movements of the targets in the RD spectra of successive measurement cycles are rather small in most application scenarios. Terefore, the prior information about the positions of the targets can be utilized to expedite the update steps of the iterative thresholding algorithms described in (11).

Instead of using the standard IST [16, 31] and IHT [32], we incorporate prior information into the thresholding process for solving (9) and (10). Te prior-model-based soft thresholding function is defned as:

$$
\begin{array} { c } { { \mathcal { S } _ { \lambda } ( \theta _ { i } ) = \operatorname { s i g n } \left( \theta _ { i } \right) \operatorname * { m a x } ( | \theta _ { i } | - ( 1 - \xi ( p _ { i } ) ) \cdot \lambda , 0 ) , } } \\ { { \mathrm { f o r } i = 0 , . . . , M N - 1 , } } \end{array}\tag{13}
$$

where i denotes the index of the elements of vector θ. Te prior probability $p _ { i }$ ensures that if a sparse maximum is likely at the i-th position, the threshold <sup></sup> is scaled down accordingly by $( 1 - \zeta ( p _ { i } ) )$ . Tis helps to reduce the number of iterations for searching an optimal estimate of x and facilitates the detection of local maxima, thereby reducing the reconstruction error. Te mapping function

$$
\zeta : \mathbb { R } \to \mathbb { R } , \ \zeta ( p _ { i } ) = \frac { a \cdot p _ { i } + b } { e }\tag{14}
$$

is introduced for regulating the prior model, where $a , b , e \in \mathbb { R }$ are the control parameters. Similarly, the prior-model-based hard thresholding function is defned as:

$$
\begin{array} { r } { \mathcal { H } _ { \lambda } ( \theta _ { i } ) = \{ \theta _ { i } , ~ | \theta _ { i } | \geq ( 1 - \zeta ( p _ { i } ) ) \cdot \lambda  , } \\ { 0 , ~ | \theta _ { i } | < ( 1 - \zeta ( p _ { i } ) ) \cdot \lambda   } \\ {   \mathrm { f o r } i = 0 , . . . , M N - 1 ,  } \end{array}\tag{15}
$$

where i denotes the index of the elements of vector θ.

## 3.3.2 Determination of the prior probability

Te prior of the presence of the target at the i-th position of x is assumed to follow a normal distribution whose expected value $\mu _ { i }$ and variance $\sigma _ { i } ^ { 2 }$ are equal to the empirical mean and variance of the peak values at this position in the latest Q-measurements:

$$
p ( x _ { i } ) \sim \mathcal { N } ( \mu _ { i } , \sigma _ { i } ^ { 2 } ) , i \in \xi ,\tag{16}
$$

where $\xi = \xi _ { 0 } \cup \xi _ { 1 } . . . \cup \xi _ { Q - 1 }$ represents the set of positions of target peaks detected by a cell averaging constant false alarm rate (CA-CFAR) algorithm in the (original or recovered) RD spectra<sup>1</sup> of the latest Q measurements. ξ0 and $\xi _ { Q - 1 }$ denote the sets of detected positions of target peaks in the RD spectrum of the current measurement $\mathbf { x } _ { \eta }$ and the measurement at time $\eta - Q + 1$ , respectively. Te prior probability for the presence of the target at the i-th position $( i \in \xi )$ of the next measurement $\mathbf { x } _ { \eta + 1 }$ is determined by $x _ { i }$ in $\mathbf { x } _ { \eta } .$ . Because the presence of target peaks at other positions $( i \notin \xi )$ was not observed in the latest $\mathrm { Q } \mathrm { \mathrm { . } }$ -measurements, the prior probability of the these positions is initially set to zero. Ten, a prior probability matrix $\tilde { \mathbf { P } } \in \mathbb { R } ^ { N \times M }$ can be constructed. However, since the targets may move slightly in the next measurement cycle, the prior probability should optimally be propagated from the historical target positions to the neighboring positions surrounding them. Te new prior probability matrix is then recalculated as $\mathbf { P } = \mathbf { G } \circledast \tilde { \mathbf { P } } ,$ where G represents a 2D window function and $\circledast$ denotes the convolution operator. $p _ { i }$ is then the i-th element of vec(P).

## 3.4 Integration of 2D masked residual updates

Since the multiplication of a vector with the Fourier matrix can utilize the fast Fourier transform (FFT), it can signifcantly improve the efciency of recovery algorithms. Te microcontrollers of most automotive radar sensors have an accelerator for FFT processing with reduced computational latency. However, the previously discussed radar interference mitigation framework that vectorizes the radar measurement to match the general CS framework cannot take advantage of this beneft. More precisely, recalling the framework illustrated in Fig.  2, by removing the interference-contaminated measurement samples in y, the corresponding rows of the measurement transform matrix W˜ are pruned. Ten, the remaining measurement signal $\tilde { \mathbf { y } }$ and the pruned measurement transform matrix $\tilde { \Psi }$ are used with diferent CS solvers to compute a sparse solution of x. Terefore, the FFT operator cannot be directly incorporated. In order to utilize the computational advantage of the FFT, a 2D masked residual updates framework is proposed that can be easily incorporated into existing CS solvers.

Recalling the residual updates in (11), the choice of $\tilde { \Psi } \in \mathbb { C } ^ { q \times M N }$ and $\mathbf { r } _ { t } \in \mathbb { C } ^ { q }$ have a clear dependency on the q-rows of interference-free samples. As the positions of interference-contaminated samples can be random [33], the size of $\tilde { \Psi }$ can vary with interference scenarios. However, the residual updates always correspond to the remaining interference-free samples. Terefore, it is possible to control the residual updates using a mask and to keep the size of the measurement transform matrix fxed. In other words, by tracking the residual updates at exact positions of the interference-free samples in y with a mask, the measurement transform matrix will always have the original size of $\tilde { \mathbf { w } } \in \mathbb { C } ^ { M N \times M N }$ . Te advantage of a fxed size of the measurement transform matrix is that the matrix-vector multiplications for Fourier transforms can be replaced by the FFT or inverse FFT (IFFT) operations on a 2D signal matrix.

After the detection of distorted samples, the position of interference-free samples in the m-th column of the discrete beat signal matrix Y is stored in an index vector $ { \mathbf { b } } _ { m } \in \{ 0 , 1 \} ^ { N }$ , the value one is used to indicate the position of the interference-free samples. Ten, by grouping the individual index vectors $\mathbf { b } _ { m } ,$ a mask matrix $\mathbf { B } = [ \mathbf { b } _ { 1 } \cdot \cdot \cdot \mathbf { b } _ { M } ] \in \{ 0 , 1 \} ^ { N \times M }$ is created. Te notation $\mathbf { Y } [ \mathbf { B } = 1 ]$ then describes the selection of all elements from Y whose places in B have the value one. We use the notation $\mathbf { Y } [ \mathbf { B } = 1 ] \xrightarrow { p \cdot M } \tilde { \mathbf { Y } }$ for drawing p elements from each of M columns in Y, whose index is equal to one in B, then storing their elements in $\tilde { \mathbf { Y } } \in \mathbb { C } ^ { p \times M }$ . Since the interference may generate extended segments of disturbed data in various positions of diferent chirps, this operation guarantees the matrix form of the computation during the pursuit of the sparse solution and it also adds additional randomness to the measurement transform matrix. Correspondingly, we use the notation $\mathbf { Z } [ \mathbf { B } = 1 ] \overset { p \cdot M } { \longleftarrow } \tilde { \mathbf { Y } }$ for indicating the mapping of elements from each of M columns in $\tilde { \mathbf { Y } } \in \mathbb { C } ^ { p \times M }$ to the positions in a zero matrix $\mathbf { Z } \in \mathbb { C } ^ { N \times M }$ , whose indices in B have the value one. Te mask matrix B is used for tracking the residual updates at the exact positions of interference-free samples. Consequently, the update step in (11) becomes

$$
\begin{array} { r } { \begin{array} { r l } & { \mathbf { R } _ { t } = \tilde { \mathbf { Y } } - \bigg ( \mathbf { Y } _ { \mathrm { r e c } } [ \mathbf { B } = 1 ] \xrightarrow { p \cdot M } \mathbf { Y } _ { t } \bigg ) , } \\ & { } \\ & { \mathbf { X } _ { t + 1 } = { \mathcal { T } } _ { \boldsymbol { \lambda } } \bigg ( \mathbf { X } _ { t } + \boldsymbol { \vartheta } \cdot \mathbf { W } _ { \mathbf { N } } \cdot \mathbf { R } _ { \mathrm { r e c } } \cdot \mathbf { W } _ { \mathbf { M } } ^ { T } \bigg ) , } \end{array} } \end{array}\tag{17}
$$

where $\mathbf { Y } _ { \mathrm { r e c } } = \tilde { \mathbf { W } } _ { \mathbf { N } } \cdot \mathbf { X } _ { t } \cdot \tilde { \mathbf { W } } _ { \mathbf { M } } ^ { T }$ and $\mathbf { R } _ { \mathrm { r e c } } = \mathbf { Z } [ \mathbf { B } = 1 ] \ \overset { p \cdot M } { \longleftarrow } \mathbf { R } _ { t }$ . We refer to this residual updates process as 2D masked residual updates.

From Teorem 1 (see Appendix B), it is known that a random row sub-matrix of $\tilde { \mathbf { W } }$ satisfes a near-optimal RIP with high probability. For the analysis of the RIP condition of the 2D MRU framework, we consider the equation $\mathbf { Y } _ { \mathrm { r e c } } = \tilde { \mathbf { W } } _ { \mathbf { N } } \cdot \mathbf { X } _ { t } \cdot \tilde { \mathbf { W } } _ { \mathbf { M } } ^ { T }$ instead of the 1D formulation $\mathbf { y } _ { \mathrm { r e c } } = \tilde { \mathbf { w } } \cdot \mathbf { x } _ { t } .$ . Te theoretical guarantee of successful RD spectrum recovery discussed in Teorem 1 also applies to 2D algorithms, where $q$ is now substituted by $p \cdot M$ . More concretely, with the help of the mask matrix B, $\mathbf { Y } _ { t }$ obtains values from $\mathbf { Y } _ { \mathrm { r e c } }$ only at the selected $p$ positions in each chirp, meaning that the valid updates of $\mathbf { Y } _ { \mathrm { r e c } }$ are preserved in these $p \cdot M$ entries (the same for $\mathbf { y } _ { \mathrm { r e c } } )$ . In this way, the rows with the same indices as the indices of these $p \cdot M$ entries are “subsampled” from $\tilde { \mathbf { W } }$ in this particular manner for the 2D case. Te advantage of incorporating 2D MRU is that the matrix-vector multiplications for Fourier transforms can be solved quickly with hardware acceleration in the automotive radar system. Algorithm 1 describes the incorporation of 2D MRU with prior-model-based IST/IHT (PM-IHT/PM-IST) for RD spectrum recovery, where ǫ is the threshold parameter of the relative residual update.

```latex
Algorithm 1: 2D MRU PM-IHT/PM-IST for RD
spectrum recovery
Input:
Discrete beat signal $\tilde { \mathbf { Y } } \in \mathbb { C } ^ { p \times M }$
Mask matrix B ∈ {0, 1}N×M
Zero matrix $\mathbf { Z } \in \overset { \mathbf { \bar { \rho } } } { \mathbb { C } } ^ { N \times M }$
Residual: $\mathbf { \bar { R } } _ { 0 } ^ { - } = \mathbf { 0 } \in \mathbb { C } ^ { p \times M }$
Prior probability matrix: $\tilde { \mathbf { P } } \in \mathbb { R } ^ { N \times M }$
Output:' Recovered RD spectrum $\mathbf { X } \in \mathbb { C } ^ { N \times M }$
Initialize:
$\mathbf { X } _ { 0 } : = \mathbf { Z } $
P = G *P // Calculate prior model
for $j = 1 , . . . , \infty$ do
$\begin{array} { r } { \mathbf { Y } _ { \mathrm { r e c } } = \tilde { \mathbf { W } } _ { \mathbf { N } } \cdot \mathbf { X } _ { j - 1 } \cdot \tilde { \mathbf { W } } _ { \mathbf { M } } ^ { T } } \end{array}$
$\mathbf { R } _ { j } : = \tilde { \mathbf { Y } } - \left( \mathbf { Y } _ { \mathrm { r e c } } [ \mathbf { B } = 1 ] \xrightarrow { \boldsymbol { p } \cdot \boldsymbol { M } } \mathbf { Y } _ { j } \right)$ // Update residual
$\mathbf { R } _ { \mathrm { r e c } } = \mathbf { Z } [ \mathbf { B } = 1 ] \xleftarrow { p \cdot M } \mathbf { R } _ { j }$
$\mathbf { \Gamma } \mathbf { \Gamma } = \mathbf { W } _ { \mathbf { N } } \cdot \mathbf { R } _ { \mathrm { r e c } } \cdot \mathbf { W } _ { \mathbf { M } } ^ { T }$ // Gradient
$\lambda _ { j } : = { \boldsymbol { \beta } } \cdot \operatorname { s t d } ( \mathbf { \boldsymbol { \Gamma } } )$ // Update threshold
PM-IST
1 $\mathbf { X } _ { j } = \mathcal { S } _ { \mathsf { X } _ { j } } \left( \mathbf { X } _ { j - 1 } + \vartheta \cdot \mathbf { r } \right)$ // Soft thresholding
end
PM-IHT
$\mathbf { X } _ { j } = \mathcal { H } _ { \mathsf { A } _ { j } } \left( \mathbf { X } _ { j - 1 } + \vartheta \cdot \mathbf { r } \right)$ // Hard thresholding
end
$\mathbf { i f } \ ( | | \mathbf { R } _ { j } | | _ { F } - | | \mathbf { R } _ { j - 1 } | | _ { F } ) / | | \mathbf { R } _ { j } | | _ { F } < \epsilon$ then
1 return X
end
end
```

## 3.4.1 Computational complexity

$$
\begin{array} { r l } { { \cal O } \big ( M N \log ( N ) + N M \log ( M ) \big ) ~ } & { } \\ { ~ } & { = { \cal O } \big ( M N ( \log ( N ) + \log ( M ) ) \big ) } \\ { ~ } & { = { \cal O } \big ( M N ( \log ( N M ) ) \big ) . } \end{array}\tag{18}
$$

Te computational efort of 1D solvers in each iteration loop can be described by O(qMN ), where q denotes the number of all undisturbed samples across all chirps. With the proposed approach the complexity is reduced considerably by a factor of $O \big ( \log ( N M ) / q \big )$ . Considering a discrete beat signal $\mathbf { Y } \in \mathbb { C } ^ { 1 2 8 \times 2 5 6 }$ where 10% samples are disturbed by interference (i.e., q equals 29491), lo $\mathfrak { z } ( N M ) / q \approx 1 / 6 5 3 1$

(a) Discrete beat signal with interference  
![](images/eba07574887ab0585fe54b53cae3647978031e0dd44aae778aaf4010f7bebff5.jpg)

(b) Estimated position of distorted samples  
![](images/d847224f4a4fd162fa098efd30541c72121b35373293b7a1ab605efeb728ebaa.jpg)  
Chirp  
Fig. 3 a An example discrete beat signal with interference; b The positions of the distorted samples detected by the Laplacian flter with iterative adaptive thresholding are indicated by 1. For an intuitive visualization, the amplitude of the measurement in (a) is normalized between <sup>1</sup> and 1

Table 1 Evaluation of interference detection methods
<table><tr><td>Detection method</td><td>F-measure (%)</td><td>Recall (%)</td></tr><tr><td>Laplacian filter based thresholding</td><td>82.34</td><td>71.52</td></tr><tr><td>Iterative adaptive thresholding</td><td>81.69</td><td>88.20</td></tr><tr><td>Combined method</td><td>79.00</td><td>95.73</td></tr></table>

![](images/761386c7bd77c1a2417a4448ec3a08145e8e16516e4b98d78cd6a00f87b90268.jpg)  
(b) Distorted - SINR 12.17 dB

![](images/fd109859cdd0b57607d716941afc5680e9f0ce4666f32383fc7395c6efa6dbed.jpg)  
(d) AR - SINR 23.79 dB

![](images/9f01423c2e20fb9de485143ba3cf5c6d4f7e8cb6c3b132c9978b67eb56d35ed4.jpg)

![](images/6fb1fe6e1bd706c199d1ce5518ef6330792c1acd1575d76dfd2d4b16efea8b5c.jpg)  
(f) YALL1 - SINR 24.90 dB (h) PM-IHT - SINR 112.24 dB [dB

![](images/e31354f806904564c29c45b17a56a857e6b2925d8ff2723276ccc83909abc159.jpg)

![](images/aeefb286f7c651f33f3eb1c3590b6a092ea3fc873ac62a8f51e775a408b13263.jpg)

![](images/590b79ec70896d9f34137c2956c6acb156ea21e6352688688a28c9f096d5b8f1.jpg)

![](images/2134d30df0b34ee97ec5e2cc65cba51237c2f11b01e38096dcd247d770ad7a80.jpg)  
Fig. 4 a Original RD spectrum, b Distorted RD spectrum and RD spectra recovered by c the zeroing method, d AR, e IMATCS, f YALL1, g PM-IST, and h PM-IHT, in the case that the number of discarded samples is about 10% of the total measurement

## 4 Detection of disturbed samples

In [36], a method was presented in which the interference is detected by iterative adaptive thresholding. Samples from a signal vector y of length L are considered to be interference-contaminated samples when their absolute values exceed a threshold and the detected

samples are then set to zero. $\bar { \bf y }$ is used to represent the new signal padded with zeros. Ten, with the number of detected samples D, a new threshold value can be calculated as:

$$
T _ { D } = \gamma \left( \sqrt { \frac { 1 } { L - D } \sum _ { l = 1 } ^ { L } \bar { y } _ { l } ^ { 2 } } \right) ,\tag{19}
$$

$T _ { D }$ $\Delta \boldsymbol { T } _ { D } ,$ $T _ { D }$ $\Delta _ { T _ { D } }$

In [10], a classical edge detector, namely, a Laplacian flter [37] is used to identify the anomalies and the interference-contaminated samples. Te Laplacian flter based method is fast and hardly deletes interference-free samples. Still, it misses some interference-contaminated samples, since the Laplacian flter assigns a larger weight to edges. Tus, if the interference-contaminated samples are grouped, the distorted samples in the middle often cannot be detected completely. However, this faw can be compensated by a combination with the iterative adaptive thresholding detection method. To quantitatively analyze the detection performance of diferent algorithms, the recall and F-measure are introduced, which are calculated as: Recall $\begin{array} { r } { = \frac { \mathrm { T P } } { \mathrm { T P + F N } } } \end{array}$ and $\begin{array} { r } { F = \frac { 2 \mathrm { T P } } { 2 \mathrm { T P } + \mathrm { F P } + \mathrm { F N } } } \end{array}$ where TP, FP, and FN denote the number of true-positive, false-positive, and false-negative estimates.

Since the interference-contaminated samples are the minority in the discrete beat signal, the F-measure is theoretically more important for evaluating the detection performance. However, in radar interference mitigation with CS, the amount of correctly detected interference positions has a greater impact on the recovery results. If a small amount of interference-free samples is accidentally discarded, this results in a small change in the compression ratio as defned in Sect. 5 and does not have a large impact on the recovery results. Te evaluation results in Table 1 show that the combination of the two methods can correctly detect about 96% of the interference-contaminated samples. Te combined method is therefore more suitable for interference mitigation with CS approaches. Te undetected 4% of the interference-contaminated samples should have low amplitudes, as they would otherwise have been detected by the iterative adaptive thresholding method. Tus, these distorted samples may also generate little additional noise in the frequency domain and therefore do not afect the weak targets.

## 5 Evaluation methods and results

In this section, the performance of algorithms incorporating 2D MRU is analyzed and the evaluation results are further discussed. Firstly, the reconstruction performance of RD spectrum of real radar measurements is evaluated in terms of the run time and signal-to-interference-plus-noise ratio (SINR) in comparison with the state-of-theart algorithms. Secondly, the time consumption and the relative reconstruction error are evaluated under diferent metrics, namely, the compression ratio, the amount of remaining interference-contaminated samples used in reconstruction, and the sparsity level ratio. Te compression ratio δ and the sparsity level ratio $\rho$ are defned as

$$
\delta = p / N , \quad \rho = k / ( M N ) ,\tag{20}
$$

$p$ $( \mathrm { i } . \mathrm { e } . , Q = 5$

## 5.1 Performance evaluation on real radar measurements

Recent research results have shown that the AR model [6] and CS algorithms like the iterative method with an adaptive thresholding for compressed sensing (IMATCS) [7] or the YALL1 algorithm [38] provide satisfactory recovery results of the discrete beat signal for interference mitigation. Te performance of these methods along with the simple zeroing method [1], and the prior-model-based iterative thresholding algorithms (PM-IHT and PM-IST) are evaluated in terms of the run time and SINR on a real radar measurement. Te real radar measurement is recorded in a test chamber with radiationabsorbent materials and the targets (at distances of 27m, 50m, 73m, 95m and 120m) are created by a target generator. Te interference is produced by a radar that emits signals in the same frequency band with a larger slope than the victim radar.

Figure 4 shows the recovered RD spectra after the elimination of the severely distorted samples (ca. 10% of the total measurement) for four reference algorithms, AR, IMATCS, $\mathrm { Y A L L } \mathrm { L } 1 ^ { 2 }$ and the zeroing method, as well as for the proposed prior-model-based iterative thresholding algorithms. Te recovery performance of IMATCS may vary slightly when diferent thresholds are selected. It should be clarifed that the parameters of IMATCS for implementation are chosen according to [7], where the value of the highest peak is used to initialize the linear threshold. Te targets in the distorted RD spectrum are hard to detect, however, the targets in the recovered RD spectra can be found easily. Here, the threshold parameter of relative residual update ǫ of the CS algorithms is set to $1 0 ^ { - 6 } .$ Te AR, IMATCS, and YALL1 algorithms can properly restore the RD spectra, while the zeroing method produces many artifact peaks. Te prior-model-based iterative thresholding algorithms, however, produce superior recoveries. Since the proposed 1D and 2D prior-model-based iterative thresholding algorithms difer only in their computational load, the recovered RD spectra of the prior-model-based iterative thresholding algorithms in Fig. 4 are solely presented for the 2D case.

Since the amount of disturbed samples in the discrete beat signal may vary under different types of interference, the robustness of the algorithms will be further evaluated by eliminating more samples. Table  2 shows the performance comparison of diferent algorithms in terms of the run time and SINR for diferent amounts of interference and correspondingly discarded interference-contaminated samples. For interference detection, the combined method discussed in Sect. 4 is used in this evaluation. Te run time of algorithms is estimated with MATLAB based on an Intel(R) Core(TM) i5-8350U

<sub>f</sub> <sub>the</sub> <sub>reconstruct</sub>i<sub>on</sub> i<sub>n</sub> <sub>terms</sub> <sub>of</sub> <sub>the</sub> <sub>run</sub> <sub>t</sub>im<sup>e</sup> <sup>and</sup> <sup>S</sup>I<sup>NR</sup> <sup>for</sup> <sup>d</sup>i<sup>ferent</sup> <sup>percentage</sup> <sup>(P)</sup> <sup>of</sup> <sup>d</sup>i<sup>scarded</sup> <sup>samp</sup>l<sup>es</sup> <sup>a</sup>
<table><tr><td rowspan="2">P (%)</td><td colspan="10">CPU Time in Seconds</td><td colspan="6">SINR in dB</td></tr><tr><td>T1</td><td>T2</td><td>T3.1</td><td>T4.1</td><td>T5.1</td><td>T3.2</td><td>T4.2</td><td>T5.2</td><td>T6</td><td>T1</td><td>T2</td><td>T3</td><td>T4</td><td>T5</td><td>T6</td></tr><tr><td>7</td><td>1.3414</td><td>510.8916</td><td>2.1774</td><td>3.3097</td><td>29.9928</td><td>0.0146</td><td>0.0243</td><td>0.0883</td><td></td><td>23.73</td><td>27.65</td><td>108.82</td><td>94.96</td><td>24.78</td><td>22.10</td></tr><tr><td>10</td><td>1.8021</td><td>526.8254</td><td>1.4430</td><td>2.9986</td><td>29.0580</td><td>0.0229</td><td>0.0232</td><td>0.1031</td><td></td><td>23.79</td><td>27.27</td><td>112.24</td><td>96.88</td><td>24.90</td><td>18.55</td></tr><tr><td>15</td><td>2.1152</td><td>504.6283</td><td>1.4211</td><td>2.7368</td><td>27.9085</td><td>0.0232</td><td>0.0260</td><td>0.1090</td><td></td><td>24.05</td><td>26.77</td><td>113.62</td><td>98.48</td><td>25.11</td><td>16.36</td></tr><tr><td>20</td><td>2.6769</td><td>503.9345</td><td>2.0143</td><td>2.6963</td><td>25.9270</td><td>0.0237</td><td>0.0271</td><td>0.1062</td><td></td><td>23.92</td><td>25.65</td><td>113.29</td><td>98.31</td><td>25.20</td><td>13.21</td></tr><tr><td>25</td><td>3.0952</td><td>469.0456</td><td>1.7363</td><td>2.6766</td><td>25.7869</td><td>0.0248</td><td>0.0272</td><td>0.1080</td><td></td><td>24.15</td><td>25.41</td><td>114.10</td><td>99.75</td><td>25.38</td><td>12.96</td></tr><tr><td>30</td><td>3.5708</td><td>455.4435</td><td>1.3364</td><td>2.4638</td><td>22.2691</td><td>0.0275</td><td>0.0287</td><td>0.1210</td><td></td><td>24.61</td><td>25.57</td><td>114.59</td><td>107.36</td><td>25.68</td><td>11.78</td></tr></table>

<sub>D);</sub> <sub>T3</sub>.<sub>1,</sub> <sub>PM-</sub>I<sub>HT</sub> <sub>(1D);</sub> <sub>T3</sub>.<sub>2,</sub> <sub>PM-</sub>I<sub>HT</sub> <sub>(2D);</sub> <sub>T4,</sub> <sub>P</sub>M<sup>-</sup>I<sup>ST</sup> <sup>(1D/2D);</sup> <sup>T4</sup>.<sup>1,</sup> <sup>PM-</sup>I<sup>ST</sup> <sup>(1D);</sup> <sup>T4</sup>.<sup>2,</sup> <sup>PM-</sup>I<sup>ST</sup> <sup>(2D);</sup> <sup>T5,</sup> <sup>YALL1</sup> <sup>(1D/2D);</sup> <sup>T5</sup>.<sup>1,</sup> <sup>YALL1</sup> <sup>(1D);</sup> <sup>T5</sup>.<sup>2,</sup> <sup>YALL1</sup> <sub>( 1)</sub> <sub>are</sub> i<sub>ncorporated</sub> <sub>w</sub>i<sub>th</sub> <sub>the</sub> <sub>proposed</sub> <sub>2D</sub> <sub>MRU</sub> <sup>framework</sup> <sup>and</sup> <sup>the</sup> <sup>ana</sup>l<sup>ys</sup>i<sup>s</sup> <sup>resu</sup>l<sup>ts</sup> <sup>of</sup> <sup>these</sup> <sup>2D</sup> <sup>CS</sup> <sup>so</sup>l<sup>ve</sup>

![](images/c14051c877097b34ddd1560e944411c93e52bf2dfe12b5345b170ca7e4760876.jpg)  
Fig. 5 Velocity cut of RD spectra at range <sup>R 73</sup> m

![](images/4ee16b0b21b5fe5dcfe39bbf2a3531ede16dab4a22da2afb45d26d68ed93e354.jpg)  
Fig. 6 Computation time of 2D algorithms vs. compression ratio δ

CPU@1.70GHz. It is found that the run time of the algorithms PM-IST and PM-IHT incorporating 2D MRU is less than 50 milliseconds for a dimension of $\tilde { \mathbf Y }$ up to $1 2 8 \times 2 5 6 .$ while the run time of the 1D implementation requires seconds to complete the recovery. Te code implementation of $\mathrm { I M A T C S } ^ { 3 }$ is modifed based on [39] in which every iteration step needs the eigenvalue decomposition of the measurement transform matrix. Tus, the IMATCS algorithm takes more time for recovery as the size of the measurement transform matrix is large. Te size of the measurement transform matrix decreases accordingly when the size of the remaining discrete beat signal decreases. Tis explains why the run time of IMATCS decreases as more samples are discarded. Te run time of the zeroing method is instantaneously fast and therefore difcult to measure accurately. Te other advantage of the prior-model-based iterative thresholding algorithms is that they provide superior SINR improvement, since the proposed PM-IST and PM-IHT can strongly suppress the measurement noise. Tis can be verifed in Fig. 5, where the velocity cut of the recovered RD spectrum of the target at 73 meter is shown. Te signal peak of the target at 73 m is much easier to detect in the recovered RD spectra provided by the PM-IHT and PM-IST methods.

![](images/71844a9be4a89364ee0d79767be9bba3fd0a87ff062f50173d2f72a1a9deb020.jpg)  
Fig. 7 Mean relative absolute error of 2D algorithms vs. compression ratio δ

## 5.2 Performance evaluation of 2D algorithms on diferent metrics

Since diferent metrics such as the amount of interference-free samples used for reconstruction, the sparsity level of RD spectrum and the amount of remaining interferencecontaminated samples all have an impact on the performance of diferent CS solvers [40], the performance of 2D algorithms are therefore further evaluated under these metrics. In this evaluation part, the representative greedy algorithm CoSaMP [22] and AMP with the proposed 2D extension are also included.

Firstly, the computation time and the mean relative absolute error (MRAE) of 2D algorithms for diferent compression ratio (20) is examined. Te diferent amount of interference-free samples is used to recover the RD spectrum. Te value of δ is set between 0.1 and 1. For each δ, the simulation is repeated ffty times and the threshold parameter ǫ is set to $1 0 ^ { - 3 } .$ . Te MRAE is defned as the mean of the relative absolute error between the target peaks in the interference-free RD spectrum $\mathbf { X } _ { \mathrm { c l e a n } }$ and in the reconstructed RD spectrum $\mathbf { X } _ { \mathrm { r e c } } .$

$$
\mathrm { M R A E } = \frac { 1 } { \tilde { \# } _ { \mathcal { Z } } } \sum _ { \{ \tilde { n } , \tilde { m } \} \in \mathcal { Z } } \frac { | \mathbf { X } _ { \mathrm { c l e a n } } [ \tilde { n } , \tilde { m } ] - \mathbf { X } _ { \mathrm { r e c } } [ \tilde { n } , \tilde { m } ] | } { | \mathbf { X } _ { \mathrm { c l e a n } } [ \tilde { n } , \tilde { m } ] | } ,\tag{21}
$$

where n and m are row and column indices of the RD matrix, <sup>Z</sup> is the set of target peaks.   
$\# z$ denotes the cardinality of set <sup>Z</sup>.

![](images/d3a63dd6a7d52950c1f61721bde75d884e8f82c273c4bdc3d26fe2c46100f4d7.jpg)  
Fig. 8 Number of iterations of 2D algorithms vs. percentage of interference-contaminated samples used in the reconstruction

![](images/8099a15290a10bcc3b5669a3b402b77e0326f7faab15462e920410f7a502f41d.jpg)  
Fig. 9 Mean relative absolute error of 2D algorithms vs. percentage of interference-contaminated samples used in the reconstruction

required in order to fnd an optimal solution when fewer interference-free samples remain.

Figure 7 shows that MRAE of all target peaks (except for the target peaks recovered by YALL1, which aims to achieve a high accuracy and therefore also tries to reconstruct some noise [34]) in the restored RD spectra becomes smaller as the value of δ increases. Tis shows that the more interference-free samples are left, the more accurately the target peaks will be restored. Te proposed PM-IHT and PM-IST further improve the MRAE of the standard IHT and IST, although the improvements in run time are not signifcant. It should be noted that MRAE provides a measure of the restoration quality of target peaks, namely the sparse representations. Tere is therefore no direct connection between MRAE and SINR, since it is possible that an algorithm recovers the target peak with a small MRAE but a high background noise level, so that the SINR is small.

![](images/6a16ae7f381ed20c8931c7e23e4e6859bf7f4556467d34a6f33f30a12b5d3a9e.jpg)  
Fig. 10 Mean relative absolute error of 2D algorithms vs. sparsity level ratio ρ

![](images/a49aab0d80316b979c7643c215f4b784499a1485442f8f73a284662149fae9ba.jpg)  
Fig. 11 Concordance of local maxima of recovered RD spectrum vs. sparsity level ratio ρ

Since it is difcult to accurately identify all interference-contaminated samples, in some scenarios few interference-contaminated samples may remain after the interference detection. Terefore, we secondly evaluate the robustness of the algorithms in the case that some of the remaining samples contain interference. To simulate the reconstruction on these scenarios, diferent interference-free beat signals with an average sparsity level ratio $( \rho = 0 . 0 0 5 )$ are generated and superimposed with interference. Te simulations are performed with a δ that is always adjusted to use the maximum number of interference-free samples for reconstruction. Amounts of interference-contaminated samples between 0.1% to 15% of total remaining samples are tested. Since the distorted sample usually contains larger amplitudes, it changes the SINR of the RD spectrum of the input data. Empirically, it is shown that when the percentage of distorted samples in $\tilde { \mathbf Y }$ ranges from 0.1 to 15%, the SINR (originally ca. 32 dB) decreases accordingly by a value ranging from 7 dB to 25 dB. Furthermore, as shown in Fig.  8, the number of iterations increases slightly for all algorithms, as the increasing interference quantity can infuence the search direction of the sparse solution of the algorithm. Although CoSaMP requires the smallest number of iterations, its run time is still longer than that of iterative thresholding algorithms due to the relatively long computation time in each iteration. In general, the run time of the iterative thresholding algorithms is less than 20 milliseconds.

![](images/ce4a8ca458ba2648061a2dba8744edc6efce3530d2784e881126b5907081d176.jpg)

![](images/41bf11fdb4b0e605cc89d4683324292c44ed914df8d77e91b13add5e204cf1f3.jpg)

![](images/c462e4a327e00348e8f960ed68a0167b53075c85998e595a928de9dfd774a9e6.jpg)

![](images/57db8d5c8d4bbfe3a12130f56a4aa11cf84f9f055a852f09f30d289b7cfa1961.jpg)

![](images/01da6587a40ac30e791d3218c5796434e6f5260caca1fb0cefa562f0d81d5c51.jpg)  
Fig. 12 a Ground truth, b Distorted RD spectrum, c RD spectrum from previous measurement and RD spectra recovered by d Standard IHT and e PM-IHT

Figure  9 shows that the MRAE of all target peaks also increases slightly with the amount of remaining interference-contaminated samples. Tis is due to the fact that the remaining interference is also used for reconstruction, thus the recovery contains more errors. Overall, the relative errors are nevertheless low with values below 6% and CoSaMP has the smallest MRAE. Tirdly, the concordance of the local maxima and the MRAE of 2D algorithms for diferent sparsity level (20) is examined. Te value of δ is set to 0.5. Te sparsity level $\rho$ is set between 0.001 to 0.1. For each $\rho$ the simulation is repeated ffty times and the threshold parameter ǫ is set to $1 0 ^ { - 3 }$ . Figure  10 shows that the MRAE of PM-IHT, PM-IST and AMP increases slightly as $\rho$ increases. Te value of $\rho$ has more efect on CoSaMP, and interestingly, the MRAE of YALL1 decreases while $\rho$ increases. Another metric worth evaluating is the concordance of the local maxima. It is important to check whether all local maxima are reconstructed, since the local maxima represent the individual targets. Moreover, for radar target tracking, the position of targets in the RD spectrum is decisive. To generate an evaluation criterion from this context, all local maxima are determined in the RD spectrum of the interference-free signal as well as in the RD spectrum of the reconstructed signal. Ten, the percentage of the maxima from the interferencefree signal that are present in the reconstruction is calculated. As shown in Fig.  11, the concordance of local maxima decreases as the sparsity level ratio $\rho$ increases, i.e., more valid targets are present. Te concordance of the local maxima of PM-IHT can achieve around 86% when $\rho$ equals 0.1 while concordance of the local maxima of the other algorithms are still better than 80%. Tis means that more than 80% of the targets are still recognizable after recovery. Tis shows the robustness of these 2D CS solvers. Note that $\rho$ is determined by the reference signal without interference, and $\rho = 0 . 1$ actually corresponds to a large number of target peaks, since the denominator in $\rho$ (see (20)) is large.

## 5.3 Discussion

In comparison with the 2D framework, the 1D framework is limited not only in computation time but also in hardware resources in terms of memory, since the measurement transform matrix $\tilde { \Psi }$ typically has a large size. For example, for a radar measurement of dimension $\mathbf { Y } \in \mathbb { C } ^ { 5 1 2 \times 1 2 8 } \left[ 4 \right]$ , where 10% samples of the total measurement are distorted, the corresponding matrix $\tilde { \Psi } \in \mathbb { C } ^ { 5 8 9 8 2 \times 6 5 5 3 6 }$ becomes excessively large. In contrast to the 1D case, the 2D framework avoids additional memory for the measurement transform matrix by utilizing the built-in FFT operator. Although 2D MRU can also be integrated into the baseline method YALL1, its performance in terms of SINR and the run time is still worse than the greedy algorithms (CoSaMP) and the proposed prior-model-based iterative thresholding algorithms in general. Te prior-model-based IHT shows its robustness both in the evaluation of real radar measurements and in the evaluation of CS metrics. Its run time can be even faster when the threshold parameter ǫ is relaxed to $1 0 ^ { - 2 }$ , for example.

Besides the benefts in terms of run time and reconstruction error, the prior-modelbased iterative thresholding algorithm also has the potential to help in the reconstruction of weak targets. As shown in Fig. 12, a weak target (within the red dashed square with a power of ca. 5 dB) is slightly shifted from its position in Fig. 12c to the new position in Fig. 12a. Since its power is relatively close to the background noise compared to the other target peaks, which range from about 7 dB (bottom left) to 37 dB (top left), it cannot be properly reconstructed with the standard IHT algorithm. However, in the prior-model-based IHT, due to the presence of the target peak (ca. 9 dB) in the previous measurement, the probability of the presence of the target in the red dotted square area is increased for the next measurement cycle (namely, the probability of the presence of the target is propagated to the whole red dotted square area by convolution with a window function) and the thresholds for this area are decreased accordingly. Tis weak target is therefore properly reconstructed, and in the meantime, the false-positive prior information does not afect the reconstruction result, as shown in Fig. 12e.

Tus, the proposed 2D framework in conjunction with prior-model-based IHT can be a good candidate for automotive radar interference mitigation.

## 6 Conclusion

In this paper, an efective 2D masked residual updates compressive sensing framework as well as the prior-model-based iterative thresholding algorithms are proposed for automotive radar interference mitigation. 2D masked residual updates can be easily incorporated into the state-of-the-art compressive sensing algorithms and reduces the computational complexity of these algorithms. In particular, the proposed 2D masked residual updates helps these algorithms to take advantage of hardware acceleration for FFT/IFFT operations and thus massively reduces the run time for RD spectrum reconstruction. Te theoretical analysis shows that the proposed framework can successfully reconstruct the RD spectrum with high probability. Te superiority of the proposed framework in terms of the run time and SINR is demonstrated by incorporating the 2D masked residual updates into several baseline compressive sensing algorithms. It is shown that the proposed prior-model-based iterative thresholding algorithms improve the reconstruction results of these algorithms in terms of run time and reconstruction error. Te robustness of the proposed prior-model-based iterative thresholding algorithms in conjunction with the 2D framework is also investigated in terms of several compressive sensing metrics. To improve the prior model, more sophisticated statistical models may be explored in future works.

## Appendix

## Proof of Lemma 1

<sup>Defnition</sup> <sup>1</sup> (DFT matrix and IDFT matrix). Te DFT matrix $\mathbf { W _ { N } } \in \mathbb { C } ^ { N \times N }$ is defned as the unitary matrix

$$
\mathbf { w _ { N } } : = \frac { 1 } { \sqrt { N } } \left[ \begin{array} { c c c c c } { 1 } & { 1 } & { 1 } & { \cdots } & { 1 } \\ { 1 } & { \omega _ { N } ^ { 1 } } & { \omega _ { N } ^ { 2 } } & { \cdots } & { \omega _ { N } ^ { N - 1 } } \\ { 1 } & { \omega _ { N } ^ { 2 } } & { \omega _ { N } ^ { 4 } } & { \cdots } & { \omega _ { N } ^ { 2 ( N - 1 ) } } \\ { \vdots } & { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { 1 } & { \omega _ { N } ^ { N - 1 } } & { \omega _ { N } ^ { 2 ( N - 1 ) } } & { \cdots } & { \omega _ { N } ^ { ( N - 1 ) ( N - 1 ) } } \end{array} \right]
$$

where $\begin{array} { r } { \omega _ { N } : = \exp \left( - \frac { 2 \pi j } { N } \right) } \end{array}$ is the $N ^ { t h }$ root of unity. Te IDFT matrix $\tilde { \mathbf { w } } _ { \mathbf { N } } \in \mathbb { C } ^ { N \times N }$ can be obtained by replacing the $\omega _ { N }$ with $\begin{array} { r } { \omega _ { N } ^ { * } : = \exp \left( \frac { 2 \pi j } { N } \right) } \end{array}$

<sup>Lemma</sup> <sup>1</sup> Given two unitary IDFT (or DFT) matrices $\tilde { \mathbf { w } } _ { \mathbf { N } } \in \mathbb { C } ^ { N \times N }$ and $\tilde { \mathbf { W } } _ { \mathbf { M } } \in \mathbb { C } ^ { M \times M }$ the Kronecker product of these two IDFT (or DFT) matrices $\tilde { \mathbf { w } } = \tilde { \mathbf { w } } _ { \mathbf { M } } \otimes \tilde { \mathbf { w } } _ { \mathbf { N } }$ is also a unitary matrix.

Proof Since the IDFT (or DFT) matrices $\tilde { \mathbf { W } } _ { \mathbf { M } } \in \mathbb { C } ^ { M \times M }$ and $\tilde { \mathbf { w } } _ { \mathbf { N } } \in \mathbb { C } ^ { N \times N }$ are both invertible, also their Kronecker product $\tilde { \mathbf { w } } = \tilde { \mathbf { w } } _ { \mathbf { M } } \otimes \tilde { \mathbf { w } } _ { \mathbf { N } }$ is invertible [41] and $\tilde { \mathbf { W } } ^ { - 1 } = ( \tilde { \mathbf { W } } _ { \mathbf { M } } \otimes \tilde { \mathbf { W } } _ { \mathbf { N } } ) ^ { - 1 } = \tilde { \mathbf { W } } _ { \mathbf { M } } ^ { - 1 } \otimes \tilde { \mathbf { W } } _ { \mathbf { N } } ^ { - 1 }$ . As shown in Defnition 1, $\tilde { \mathbf { W } } _ { \mathbf { M } }$ and $\tilde { \mathbf { w } } _ { \mathbf { N } }$ are both unitary matrices, thus $\tilde { \mathbf { W } } _ { \mathbf { M } } ^ { * } = \tilde { \mathbf { W } } _ { \mathbf { M } } ^ { - 1 }$ and $\tilde { \mathbf { W } } _ { \mathbf { N } } ^ { * } = \tilde { \mathbf { W } } _ { \mathbf { N } } ^ { - 1 }$ . As conjugate transposition is distributive over the Kronecker product, it follows that $\tilde { \mathbf { W } } ^ { - 1 } = \tilde { \mathbf { W } } _ { \mathbf { M } } ^ { * } \otimes \tilde { \mathbf { W } } _ { \mathbf { N } } ^ { * } = ( \tilde { \mathbf { W } } _ { \mathbf { M } } \otimes \tilde { \mathbf { W } } _ { \mathbf { N } } ) ^ { * } = \tilde { \mathbf { W } } ^ { * }$ . Tis means that W˜ is a unitary matrix. <sup></sup>

## Proof of Theorem 1

<sup>Defnition</sup> <sup>2</sup> A complex matrix $ { \mathbf { A } } \in \mathbb { C } ^ { M \times N }$ satisfes the restricted isometry property of order k with restricted isometry constant $\delta _ { k } > 0 _ { : }$ , if

$$
( 1 - \delta _ { k } ) | | { \mathbf { x } } | | _ { 2 } \leq | | { \mathbf { A } } { \mathbf { x } } | | _ { 2 } \leq ( 1 + \delta _ { k } ) | | { \mathbf { x } } | | _ { 2 }\tag{22}
$$

holds for any k-sparse signal x.

Theorem 1 <sub>Given</sub> <sub>are</sub>

• two unitary IDFT (or DFT) matrices $\tilde { \mathbf { w } } _ { \mathbf { N } } \in \mathbb { C } ^ { N \times N }$ and $\tilde { \mathbf { W } } _ { \mathbf { M } } \in \mathbb { C } ^ { M \times M } ;$

• the matrix $\tilde { \mathbf { w } } = \tilde { \mathbf { w } } _ { \mathbf { M } } \otimes \tilde { \mathbf { w } } _ { \mathbf { N } }$ with $\tilde { \mathbf { w } } \in \mathbb { C } ^ { M N \times M N }$ satisfying $| \tilde { \mathbf { W } } | | _ { \infty } \leq O ( 1 / \sqrt { M N } ) ;$

• a sufciently large MN and k , a sufciently small $\delta _ { k } > 0 .$

$q = O ( \log ^ { 2 } ( 1 / \delta _ { k } ) \delta _ { k } ^ { - 2 } \cdot k \cdot \log ^ { 2 } ( k / \delta _ { k } ) \cdot \log ( M N ) ) ;$ $\tilde { \Psi } \in \mathbb { C } ^ { q \times M N }$ $\sqrt { M N / q } \cdot \tilde { \mathbf { w } }$ $\tilde { \Psi }$ $1 - 2 ^ { - \Omega ( \log ( M N ) \cdot \log ( k / \delta _ { k } ) ) }$

## Abbreviations

## Acknowledgements

We acknowledge support by the Open Access Publication Funds of the Ruhr-Universität Bochum.

## Authors’ contributions

SC participated in the design of the study, performs literature review, and implemented the simulations and tests, besides writing the manuscript. PS participated in the design of the study, implemented the simulations and tests, and helped to review the manuscript. JT, UK, and RM participated in the design of the study and coordination and helped to draft and review the manuscript. All authors read and approved the fnal manuscript.

## Funding

Open Access funding enabled and organized by Projekt DEAL.

## Availability of data and materials

Not available online. Please contact the authors for data requests.

## Declarations

## Ethics approval and consent to participate

The authors declare that they have no human participants, their data, or biological material used in this work.

## Consent for publication

Informed consent was obtained from all authors included in the study.

## Competing interests

The authors declare that they have no competing interests.

## Author details

<sup>1</sup>Institute of Communication Acoustics, Ruhr-Universität Bochum, Bochum, Germany. <sup>2</sup>HELLA GmbH & Co. KGaA, Lippstadt, Germany. <sup>3</sup>Fraunhofer Institute for High Frequency Physics and Radar Techniques FHR, Wachtberg, Germany.

Received: 29 December 2021 Accepted: 14 March 2022

Published online: 07 April 2022

## References

1. G.M. Brooker, Mutual interference of millimeter-wave radar systems. IEEE Trans. Electromag. Compat. 49(1), 170 (2007)

2. C. Aydogdu, M.F. Keskin, G.K. Carvajal, O. Eriksson, H. Hellsten, H. Herbertsson, E. Nilsson, M. Rydstrom, K. Vanas, H. Wymeersch, Radar interference mitigation for automated driving: Exploring proactive strategies. IEEE Signal Process. Mag. 37(4), 72 (2020)

3. S. Chen, W. Shangguan, J. Taghia, U. Kühnau, R. Martin, Automotive radar interference mitigation based on a genera tive adversarial network, in Proceedings of the 2020 IEEE Asia-Pacifc Microwave Conference (APMC) (2020), pp. 728–730. https://doi.org/10.1109/APMC47863.2020.9331379

4. F. Jin, S. Cao, Automotive radar interference mitigation using adaptive noise canceller. IEEE Trans. Veh. Technol. 68(4), 3747 (2019)

5. S. Neemat, O. Krasnov, A. Yarovoy, An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain. IEEE Trans. Microw. Theory Tech. 67(3), 1207 (2019)

6. M. Rameez, M. Dahl, M.I. Pettersson, Autoregressive model-based signal reconstruction for automotive radar interference mitigation. IEEE Sens. J. 21(5), 6575 (2021). https://doi.org/10.1109/JSEN.2020.3042061

7. J. Bechter, F. Roos, M. Rahman, C. Waldschmidt, Automotive radar interference mitigation using a sparse sampling approach, in Proceedings of the 2017 European Radar Conference (EURAD) (2017), pp. 90–93

8. A. Correas-Serrano, M.A. Gonzalez-Huici, Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation, in Proceedings of the 2019 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM) (2019), pp. 1–4

9. F. Uysal, S. Sanka, Mitigation of automotive radar interference, in Proceedings of the 2018 IEEE Radar Conference (RadarConf18) (2018), pp. 0405–0410. https://doi.org/10.1109/RADAR.2018.8378593

10. S. Chen, J. Taghia, U. Kühnau, T. Fei, F. Grünhaupt, R. Martin, Automotive radar interference reduction based on sparse Bayesian learning, in Proceedings of the 2020 IEEE Radar Conference (RadarConf20) (2020), pp. 1–6. https://doi. org/10.1109/RadarConf2043947.2020.9266706

11. S. Lee, J. Lee, S. Kim, Mutual interference suppression using wavelet denoising in automotive FMCW radar systems. IEEE Trans. Intell. Transport. Syst. (2019). https://doi.org/10.1109/TITS.2019.2961235

12. M. Schiementz, Postprocessing Architecture for an Automotive Radar Network (Cuvillier, Göttingen, 2005)

13. M. Kronauge, H. Rohling, New chirp sequence radar waveform. IEEE Trans. Aerosp. Electron. Syst. 50(4), 2870 (2014)

14. F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, M. Gashinova, Phenomenology of automotive radar interference. IET Radar Sonar Navig. 15(9), 1045 (2021). https://doi.org/10.1049/rsn2.12096

15. G. Kim, J. Mun, J. Lee, A peer-to-peer interference analysis for automotive chirp sequence radars. IEEE Trans. Veh. Technol. 67(9), 8110 (2018)

16. Y. Eldar, G. Kutyniok, Compressed Sensing: Theory and Applications (Cambridge University Press, Cambridge, 2012)

17. E.J. Candes, J.K. Romberg, T. Tao, Stable signal recovery from incomplete and inaccurate measurements. Commun. Pure Appl. Math. 59(8), 1207–1223 (2006)

18. S. Foucart, H. Rauhut, A Mathematical Introduction to Compressive Sensing (Birkhäuser Basel, Basel, 2013)

19. S.S. Chen, D.L. Donoho, M.A. Saunders, Atomic decomposition by basis pursuit. Soc. Ind. Appl. Math. 43, 1 (2001). https://doi.org/10.1137/S003614450037906X

20. A. Beck, M. Teboulle, A fast iterative shrinkage-thresholding algorithm with application to wavelet-based image deblurring, in Proceedings of the 2009 IEEE International Conference on Acoustics, Speech and Signal Processing (2009), pp. 693–696. https://doi.org/10.1109/ICASSP.2009.4959678

21. J.A. Tropp, A.C. Gilbert, Signal recovery from random measurements via orthogonal matching pursuit. IEEE Trans. Inf. Theory 53(12), 4655 (2007)

22. D. Needell, J.A. Tropp, CoSaMP: Iterative signal recovery from incomplete and inaccurate samples. Appl. Comput. Harmon. Anal. 26(3), 301 (2009)

23. T. Blumensath, M.E. Davies, Iterative thresholding for sparse approximations. J. Fourier Anal. Appl. 14, 629–654 (2004)

24. T. Blumensath, M.E. Davies, Iterative hard thresholding for compressed sensing. Appl. Comput. Harmon. Anal. 27(3), 265 (2008)

25. H. Liu, R.F. Barber, Between hard and soft thresholding: Optimal iterative thresholding algorithms. arXiv:1804.08841 v4 (2019)

26. A. Maleki, Approximate message passing algorithms for compressed sensing. Ph.D. thesis (2011)

27. E.J. Candes, T. Tao, Near-optimal signal recovery from random projections: Universal encoding strategies? IEEE Trans. Inf. Theory 52(12), 5406 (2006). https://doi.org/10.1109/TIT.2006.885507

28. I. Haviv, O. Regev, The restricted isometry property of subsampled Fourier matrices, in Proceedings of the 2016 Annual ACM-SIAM Symposium on Discrete Algorithms, pp. 288–297. https://doi.org/10.1137/1.9781611974331.ch22

29. J.R. Shewchuk, An Introduction to the Conjugate Gradient Method Without the Agonizing Pain (Carnegie Mellon University, Pittsburgh, 1994)

30. A. Maleki, D.L. Donoho, Optimally tuned iterative reconstruction algorithms for compressed sensing. IEEE J. Select. Top. Signal Process. 4(2), 330 (2010). https://doi.org/10.1109/JSTSP.2009.2039176

31. K. Bredies, D. Lorenz, Linear convergence of iterative soft-thresholding. J. Fourier Anal. Appl. 14, 813–837 (2008). https://doi.org/10.1007/s00041-008-9041-1

32. T. Blumensath, M. Yaghoobi, M.E. Davies, Iterative hard thresholding and l0 regularisation, in Proceedings of the 2007 IEEE International Conference on Acoustics, Speech and Signal Processing - ICASSP ’07, vol. 3 (2007), pp. III–877–III–880. https://doi.org/10.1109/ICASSP.2007.366820

33. M. Toth, P. Meissner, A. Melzer, K. Witrisal, Slow-time mitigation of mutual interference in chirp sequence radar, in Proceedings of the 2020 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM) (2020), pp. 1–4. https://doi.org/10.1109/ICMIM48759.2020.9298996

34. J. Yang, Y. Zhang, Alternating direction algorithms for l -problems in compressive sensing. SIAM J. Sci. Comput. 33, 1 (2009)

35. S. Rangan, Generalized approximate message passing for estimation with random linear mixing, in Proceedings of the 2011 IEEE International Symposium on Information Theory Proceedings (2011), pp. 2168–2172. https://doi.org/10. 1109/ISIT.2011.6033942

36. M. Umehira, T. Nozawa, Y. Makino, X. Wang, S. Takeda, H. Kuroda, A novel iterative inter-radar interference reduction scheme for densely deployed automotive FMCW radars, in Proceedings of the 2018 19th International Radar Symposium (IRS) (2018), pp. 1–10. https://doi.org/10.23919/IRS.2018.8448223

37. X. Wang, Laplacian operator-based edge detectors. IEEE Trans. Pattern Anal. Mach. Intell. 29(5), 886 (2007)

38. T. Fei, H. Guang, Y. Sun, C. Grimm, E. Warsitz, An efcient sparse sensing based interference mitigation approach for automotive radar, in Proceedings of the 2020 17th European Radar Conference (EuRAD) (2021), pp. 274–277. https://doi. org/10.1109/EuRAD48048.2021.00077

39. M. Azghani, F. Marvasti, Iterative methods for random sampling and compressed sensing recovery. in 10th International Conference on Sampling Theory and Applications (SAMPTA 2013) (2013)

40. F. Salahdine, E. Ghribi, N. Kaabouch, Metrics for evaluating the efciency of compressing sensing techniques, in Proceedings of the 2020 International Conference on Information Networking (ICOIN) (2020), pp. 562–567. https://doi. org/10.1109/ICOIN48656.2020.9016490

41. C.F. van Loan, The ubiquitous Kronecker product. J. Comput. Appl. Math. 123(1), 85 (2000). https://doi.org/10.1016/ S0377-0427(00)00393-9

## Publisher’s Note

Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional afliations.

## Submit your manuscript to a SpringerOpen® journal and benefit from:

▶Convenient online submission

▶Rigorous peer review

▶Open access: articles freely available online

High visibility within the field

▶Retaining the copyright to your article

Submit your next manuscript atspringeropen.com