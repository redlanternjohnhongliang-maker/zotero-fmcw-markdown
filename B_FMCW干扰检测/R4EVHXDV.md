# FMCW Radar Interference Mitigation Based on the Fractional Fourier Transform

Christian Oswald and Franz Pernkopf , Senior Member, IEEE

Abstract—In this article, we propose a novel method for frequency modulated continuous wave (FMCW) radar mutual interference mitigation (IM) based on the discrete fractional Fourier transform (DFrFT). Interference chirps are detected and mitigated by compression and zeroing in the fractional domain. We provide an eficient implementation that can deal with multiple interferers, where we perform consecutive DFrFTs utilizing its angle-additivity property. For that purpose, we generalize and reduce the computational complexity of the multiangle centered DFrFT. Our algorithm is designed to be simple and fast such that it can be implemented in hardware. We evaluate our algorithm on a synthetic I/Q-modulated dataset and outperform reference methods in terms of the mean squared error (MSE), signalto-interference-plus-noise ratio (SINR), error vector magnitude (EVM), true positive rate (TPR), false alarm rate (FAR), and F1-score.

Index Terms—Constant false alarm rate (CFAR) detector, discrete fractional Fourier transform (DFrFT), frequency modulated continuous wave (FMCW) radar, interference mitigation (IM).

## I. INTRODUCTION

F <sup>REQUENCY</sup> <sup>modulated</sup> <sup>continuous</sup> <sup>wave</sup> <sup>(FMCW)</sup> <sup>radar</sup>has established itself as an indispensable component of has established itself as an indispensable component of advanced driver assistance systems and autonomous vehicles due to its low price, long range, velocity measuring abilities, independence from weather and lighting conditions, among other advantages. However, as the number of radar systems deployed increases, radar sensors interfering with one another becomes a pressing issue. If ignored, mutual interference may drastically deteriorate object detection performance, as it can appear as noise or even ghost objects in the radar sensor’s output.

FMCW radar mutual interference is a well-studied problem and has already been tackled with a multitude of countermeasures. Methods like frequency hopping [2] try to avoid interference altogether by switching the sensor’s transmit parameters as soon as interference has been detected. Other methods, including our proposed algorithm, mitigate interferences by removing them from the sensor’s output as a post hoc process. Such algorithms can be categorized by their placement in the FMCW radar signal processing chain visible in Fig. 1, i.e., whether they are applied to fasttime/slow-time sequences, range-spectra, range-Doppler (RD) maps, RD-angle maps, or any variations thereof. Zeroing [3] is a simple and popular interference mitigation (IM) technique, where interfered samples in a fast-time sequence are detected and zeroed. An iterative method with adaptive thresholding (IMAT) [4] can be used on a previously zeroed signal to reconstruct its sparse range-spectrum. Variational signal separation of a fast-time sequence based on sparse Bayesian learning is proposed in [5]. The short-time Fourier transform (STFT) of a fast-time sequence is processed in [6], [7], and [8]; in [6] they compute order-statistics while [7] uses a constant false alarm rate (CFAR) detector on the STFT followed by zeroing, and [8] transforms the STFT to a range-spectrum using a convolutional neural network (CNN). Ramp filtering [9] applies a nonlinear filter across a set of range-spectra. An adaptive noise canceler processing range-spectra is proposed in [10].

![](images/976fc817872b85a29a10db5b13067fb4f6c40572d981757a49fd07d4e7e073ec.jpg)  
Fig. 1. FMCW radar signal processing chain with our proposed IM algorithm in red, which replaces the range-FFT. It processes one fast-time sequence at a time and outputs a range-spectrum. The yellow boxes represent our padding scheme proposed in Section IV-C, which is optional and can be bypassed.

Rock et al. [11] and Fuchs et al. [12] use fully convolutional NNs on RD-maps with real-valued and complex-valued activations, respectively. An extension of the latter is described in [13], which jointly processes all receive antennae. In [14], a CNN with 3-D convolutions operating on RD-angle maps is proposed, which requires fewer parameters and generalizes better than [13]. An improvement of [14] is presented in [15], which introduces separable convolutions and propagates gradients through the object detector while training the NN. FMCW radar is a safety-critical technology, where faulty behavior must be avoided under all circumstances. In this work, we therefore prefer model-based over data-driven algorithms such as NNs, since their robustness has not yet been proven in this application.

The fractional Fourier transform (FrFT) and closely related techniques such as the chirplet transform and matched filtering have already been used for linearly frequency modulated (LFM) chirp interference mitigation. Global navigation satellite system (GNSS) chirp IM by estimating the interference chirp’s parameters with the FrFT is proposed in [16]; these are then used to generate a local LFM signal to dechirp and notch-filter the interfered GNSS signal. In [17], the timevarying Doppler shift in wireless communications of moving objects is mitigated using the discrete FrFT (DFrFT). Chirp IM in high-frequency surface wave radar is discussed in [18], where they null interferences in the fractional domain and then reconstruct the signal with an autoregressive (AR) model. Furthermore, they propose a recursive least-squares adaptive (RLS) filter in the fractional domain to treat interfered signals. In [19], interferences are suppressed by performing a singular value decomposition (SVD) of the Hankel matrix derived from the interfered signal’s optimal fractional representation. The parameters of LFM interferences with time-variant angles of arrival are estimated with the FrFT in [20], which are then suppressed using subspace projection techniques. FMCW mutual IM using a reduced chirplet transform and orthogonal matching pursuit (OMP) is proposed in [21]. FMCW interference in OFDM radars is filtered using coarse-to-fine dechirping in [22]. FMCW mutual interference is compressed and removed using an estimated matched filter in [23]. Recently, Chen et al. [24] have proposed a method for FMCW mutual IM using the fast approximate FrFT [25], where they use the goldensection search (GSS) to determine the interference’s chirp rate. We discuss the conceptual similarities and diferences between [24] and our approach in Section V-D, and compare their performance in Section VII. A summary of methods for pulsecompressing LFM chirp interferences is shown in Table I.

TABLE I  
COMPARISON OF PULSE-COMPRESSING METHODS FOR LFM CHIRP IM
<table><tr><td rowspan=1 colspan=1>Method</td><td rowspan=1 colspan=1>used technique forpulse-compression</td><td rowspan=1 colspan=1>Search for LFMChirp Parameters</td><td rowspan=1 colspan=1>Mitigation &amp; Interpolation</td><td rowspan=1 colspan=1>Inverse Transform after IM</td></tr><tr><td rowspan=1 colspan=1>[16]</td><td rowspan=1 colspan=1>approx. FrFT [25] &amp; dechirping</td><td rowspan=1 colspan=1>iterative</td><td rowspan=1 colspan=1>notch filter</td><td rowspan=1 colspan=1>rechirping</td></tr><tr><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>approx. FrFT [25]</td><td rowspan=1 colspan=1>chirp rate known</td><td rowspan=1 colspan=1>zeroing &amp; AR model or adaptive RLS</td><td rowspan=1 colspan=1>inverse approx. FrFT</td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1>approx. FrFT [25]</td><td rowspan=1 colspan=1>chirp rate known</td><td rowspan=1 colspan=1>projection &amp; SVD of Hankel matrix</td><td rowspan=1 colspan=1>inverse approx. FrFT</td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>approx. FrFT [25]</td><td rowspan=1 colspan=1>not discussed</td><td rowspan=1 colspan=1>subspace projection</td><td rowspan=1 colspan=1>not needed</td></tr><tr><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1>chirplet transform</td><td rowspan=1 colspan=1>OMP (iterative)</td><td rowspan=1 colspan=1>subtract reconstructed interference</td><td rowspan=1 colspan=1>not needed</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>dechirping</td><td rowspan=1 colspan=1>coarse-to-fine (iterative)</td><td rowspan=1 colspan=1>notch filter</td><td rowspan=1 colspan=1>rechirping</td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>matched filtering</td><td rowspan=1 colspan=1>duration-based estimation</td><td rowspan=1 colspan=1>zeroing &amp; AR model</td><td rowspan=1 colspan=1>matched filter</td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>approx. FrFT [25]</td><td rowspan=1 colspan=1>GSS (iterative)</td><td rowspan=1 colspan=1>zeroing &amp; average amplitude insertion</td><td rowspan=1 colspan=1>inverse approx. FrFT</td></tr><tr><td rowspan=1 colspan=1>ours</td><td rowspan=1 colspan=1>padded exact EMDFrFT</td><td rowspan=1 colspan=1>maximum of EMDFrFT</td><td rowspan=1 colspan=1>zeroing</td><td rowspan=1 colspan=1>absorbed into EMDFrFT</td></tr></table>

In this article, we propose a novel mitigation algorithm for FMCW radar mutual interference.

1) We generalize and reduce the computational complexity of the multiangle centered discrete fractional Fourier transform (MDFrFT) [1], resulting in our eficient MDFrFT (EMDFrFT).

2) We use the EMDFrFT as the core element for a new and simple IM algorithm that can deal with multiple interferences and integrates into the FMCW radar signal processing chain.

3) We consider the imperfections of current implementations of eigendecomposition-based discrete FrFTs (DFrFTs) and propose a simple signal padding scheme that greatly increases their chirp compression capabilities.

4) We conduct experiments comparing our algorithm to reference methods and show performance improvements across all metrics evaluated.

While the core idea of using the FrFT for LFM chirp signal processing is not new, our proposed method difers from existing literature by providing a concrete algorithm that is tailored to the requirements of automotive radar.

1) We use an exact DFrFT implementation and our new padding scheme (see Section IV-C) to increase reliability for safety-critical applications. Related work, as listed in Table I, uses the fast approximate FrFT without padding, which leads to inaccuracies as described in Section V-D.

2) We optimize our method for real-time and resourceconstrained applications. More concretely, we introduce the EMDFrFT, which reduces computational complexity and allows us to detect and compress interferences in a parallelized manner using the same computations; this replaces iterative search strategies and distinct interference detectors used in the literature. Furthermore, we absorb the computation of inverse DFrFTs and range-spectra into the EMDFrFT (see Section IV-B)—an optimization which is exclusive to our EMDFrFT.

This article is structured as follows. First, we give a brief introduction to the signal model and the DFrFT in Section II. In Section III, we develop a high-level algorithm, which we optimize and analyze in Section IV. We relate our algorithm to the landscape of IM methods in Section V, before describing and conducting experiments in Sections VI and VII, respectively. Finally, we conclude and describe potential future work in Section VIII.

Throughout this article, we use bold capital letters to denote matrices and bold lowercase letters for vectors and sets. A[n m] References the element in row n and column m of matrix A. A[n] indexes the entire nth row, while b[m] denotes the mth sample of time-discrete signal b.

## II. BACKGROUND

## A. FMCW Radar

An FMCW radar sends out LFM chirps, also called frequency ramps, and receives reflections from objects as timedelayed versions of its transmit signal. I/Q-mixing the transmit with the receive signal and sampling in intervals $T _ { s }$ reveals $N _ { O }$ objects as sinusoids [26]

$$
s _ { O } [ n ] = \sum _ { i = 1 } ^ { N _ { O } } A _ { i } e ^ { j ( \omega _ { i } n T _ { s } + \phi _ { i } ) }\tag{1}
$$

where $A _ { i } , \phi _ { i }$ are an object’s amplitude and initial phase, respectively; an object’s range is proportional to its frequency $\omega _ { i } .$ . The radial velocity of objects can then be determined by evaluating the object signal’s change of phase over consecutive chirps, which are also termed fast-time/slow-time sequences. The 2-D discrete Fourier transform (DFT) of a fast-time/slowtime sequence is a so-called RD-map, where objects appear as peaks with coordinates corresponding to their respective ranges and velocities. Azimuth and elevation of objects can be measured by jointly processing multiple receive antennae. In this article, clutter and all sources of noise are collected in $\mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta } \mathbf { \delta }$ , which is modeled as complex-valued zero-mean additive white Gaussian noise.

![](images/ee34a1dd48f5d6b2c81e43e6d759b608667603b466686d20625d29f502dd91b3.jpg)  
(a)

![](images/820cdf7ad4a6e38a95151f8060d584b7e6af4f37c7881e35462c2b57e6a2c712.jpg)  
(b)

![](images/9647bdaffeba9dac97a25e30156104389e83e4c78d09bec507b619fe2b4f50b2.jpg)  
(c)  
Fig. 2. Example of an FMCW radar signal with four objects and two interferences. The signal has been padded using the technique introduced in Section IV-C. (a) Real parts of the time-domain ground truth signal as well as the signals before and after IM using our method. (b) Corresponding normalized range-spectra. (c) Corresponding STFT of the interfered signal. The objects are visible as horizontal, and the interferences as tilted lines

## B. Mutual Interference in FMCW Radar

When multiple FMCW radar sensors transmit in the same frequency range, mutual interference might occur. More concretely, an interfering radar’s frequency course will be visible in the victim radar’s output signal while it crosses its receive frequency band. After I/Q-demodulation, ideal anti-aliasing filtering with bandwidth B and sampling, an interference chirp $s _ { I }$ is given as

$$
s _ { I } [ n ] = { \left\{ \begin{array} { l l } { A e ^ { j \left( - 2 \pi k \tau n T _ { s } + \pi k n ^ { 2 } T _ { s } ^ { 2 } + \phi _ { 0 } \right) } , } & { { \frac { \tau - B / k } { T _ { s } } } < n < { \frac { \tau + B / k } { T _ { s } } } } \\ { } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } } \end{array} \right. }\tag{2}
$$

where A, k, and $\phi _ { 0 }$ are the interference’s amplitude, chirp rate, and initial phase, respectively. denotes the point in time at which the frequency courses of the interferer and victim radar cross. An interference’s chirp rate k is calculated as $k = B _ { I } / T _ { I } - B _ { V } / T _ { V }$ , where $B _ { V } , B _ { I } , T _ { V } , T _ { I }$ are half of the victim and interferer transmit bandwidth and ramp duration, respectively. The interference is also an LFM chirp, which is suppressed as soon as its instantaneous frequency is greater than B. Sometimes, the interferer or victim fast-time sequence ends before the interference chirp crosses the entire receiver bandwidth; this case is not considered in (2), but we discuss such interferences and their efect on our proposed method in Section III-B. A more detailed description of FMCW mutual interference can be found in [27].

In this article, radar signals s are modeled as a superposition of $N _ { I }$ interferences $s _ { I } ,$ an object signal $s _ { O }$ and noise $\pmb { S } \mathcal { N }$

$$
s = \sum _ { m = 1 } ^ { N _ { I } } s _ { I _ { m } } + s _ { O } + s _ {  { \mathcal N } } .\tag{3}
$$

An example for such a signal can be seen in Fig. 2.

## C. Fractional Fourier Transform

The FrFT is a generalization of the Fourier transform (FT), as it interpolates between a time-domain signal and its spectrum. It is defined as the ath power of the FT operator ${ \mathcal { F } } , a \in \mathbb { R }$ being the so-called fractional order. For $a = 0 ,$ , the FrFT becomes the identity function, for $a = - 1$ the inverse FT, and for $a = 2$ the parity operator. $\mathcal { F }$ has a periodicity of 4, as $\mathcal { F } ^ { a + 4 h } = \mathcal { F } ^ { a } , \forall h \in \mathbb { Z }$ . Intuitively, a forward or inverse FT can be seen as a rotation of a signal’s Wigner–Ville distribution [28] by $9 0 ^ { \circ } \ \mathrm { o r } - 9 0 ^ { \circ }$ , respectively. The FrFT extends this notion of rotation to all other angles. The basis functions of the FrFT are LFM chirps with chirp rates parameterized by a. We define the fractional angle $\alpha = a \pi / 2$ such that we can describe a FrFT $\mathcal { F } ^ { 2 \alpha / \pi } : = \mathcal { F } _ { \alpha }$ by its rotation angle of the time–frequency plane. The estimation of LFM chirp rates and center frequencies using the FrFT was shown to be asymptotically unbiased and achieves the Cramer–Rao lower bound [29]. In addition to its reduction to the FT for $\alpha ~ = ~ 9 0 ^ { \circ }$ , the FrFT has two main properties, which we will use in the development of our algorithm as follows.

1) Angle-Additivity: $\mathcal { F } _ { \alpha _ { 1 } } \circ \mathcal { F } _ { \alpha _ { 2 } } = \mathcal { F } _ { \alpha _ { 2 } } \circ \mathcal { F } _ { \alpha _ { 1 } } = \mathcal { F } _ { \alpha _ { 2 } + \alpha _ { 1 } }$ , where ◦ indicates function composition.

2) Unitarity: $( \mathcal F _ { \alpha } ) ^ { - 1 } = \mathcal F _ { - \alpha } = ( \mathcal F _ { \alpha } ) ^ { H }$ , where H indicates Hermitian conjugation. It follows that Parseval’s theorem extends from the FT to the FrFT, i.e.,

$$
\int _ { - \infty } ^ { \infty } | x ( t ) | ^ { 2 } d t = \int _ { - \infty } ^ { \infty } | \mathcal { F } _ { \alpha } \{ x ( t ) \} ( u ) | ^ { 2 } d u\tag{4}
$$

for any $\alpha \in \mathbb { R } .$

The adaptation of the FrFT to time-discrete signals is called the DFrFT $W ^ { 2 \alpha / \pi } : = W _ { \alpha }$ , which is defined as the fractional <sup>α</sup>power of the DFT matrix W. However, there exist diferent implementations of the DFrFT as the eigendecomposition

$$
W ^ { \frac { 2 \alpha } { \pi } } = V \Lambda ^ { \frac { 2 \alpha } { \pi } } V ^ { \mathrm { T } }\tag{5}
$$

into the DFT eigenvectors V and eigenvalues Λ is not unique. Diferent implementations of the DFrFT provide diferent advantages and are still subject to current research. From an application point of view, the most important consideration when choosing a DFrFT implementation is its computational complexity and the properties needed in the application. Sampling-based DFrFT implementations such as [25] and [30] utilize FFTs and therefore have complexity O(N log N) for a signal of length $N ;$ however, they do not have the angleadditivity property, and the method in [25] is not unitary. On the other hand, implementations such as eigendecompositionbased DFrFTs [31], [32], [33], [34], [35] do retain these properties, but they are computed as a matrix multiplication and therefore have complexity $\mathcal { O } ( N ^ { 2 } )$ . A survey of existing DFrFT implementations can be found in [36] and [37]. There also exist algorithms where the eigendecomposition-based multiangle centered DFrFT (MDFrFT) can be computed in $\mathcal { O } ( N ^ { 2 } \log N )$ as opposed to a naive implementation with complexity $\mathcal { O } ( N ^ { 3 } )$ [1], [38]; we review the MDFrFT in Section IV as we generalize it for our algorithm. A comparative study of diferent centered DFrFTs can be found in [39].

![](images/2f4f21cdd0ec99c23301a5e8fd74d6844e9dfa50e336d731cdca20067bdf27db.jpg)  
Fig. 3. DFrFT magnitudes with angles of the signals in Fig. 2. All plots are <sup>α</sup>in dB and normalized such that the maximum value is 0. (a) Interfered signal s. The two peaks correspond to the two interferences. (b) Interference-mitigated signal. The angular resolution, as defined in Section IV-B, is $N _ { \alpha } = 1 1 3$

## III. IM USING THE DFRFT

We now introduce an algorithm that detects and zeroes one interference chirp at a time using the DFrFT. More precisely, our algorithm performs $N _ { I } + 1$ iterations for a radar signal (3) that is corrupted by $N _ { I }$ interference chirps (given that all interferences are detected and zeroed as intended). We first show how our method would compress a pure chirp signal $s _ { I }$ and then extend this approach to radar signals s which additionally contain objects, noise, and possibly other interference chirps.

As described in Section II-B, FMCW mutual interference consists of LFM chirps. Therefore, a DFrFT with a specific unknown fractional angle $\hat { \alpha } _ { I }$ will compress a pure interference chirp signal $s _ { I }$ into a pulse with its maximum located at index $\hat { n } _ { I }$ . Since the DFrFT is energy preserving (4), transforming the interference signal with $W _ { \hat { \alpha } _ { I } }$ will result in the highest possible peak $| W _ { \hat { \alpha } _ { I } } s _ { I } | [ \hat { n } _ { I } ]$ among all possible values for and n

$$
\hat { \alpha } _ { I } , \hat { n } _ { I } = \underset { \alpha , n } { \arg \operatorname* { m a x } } \left( \left| W _ { \alpha } s _ { I } \right| \left[ n \right] \right) .\tag{6}
$$

We perform a grid search for $\hat { \alpha } _ { I }$ and $\hat { n } _ { I }$ , that is, we search within $N _ { \alpha }$ <sup>α</sup>uniformly spaced fractional angles between $\alpha _ { \mathrm { m a x } }$ and $- \alpha _ { \mathrm { m a x } }$ , where $N _ { \alpha }$ and $\alpha _ { \mathrm { m a x } }$ are hyperparameters of our method. A grid search is suficient, as finding the exact value of $\hat { \alpha } _ { I }$ is desirable but not necessary for our algorithm; a deviation between the found and the optimal $\hat { \alpha } _ { I }$ simply corresponds to a weaker compression of the interference. We discuss and evaluate the influence of $N _ { \alpha }$ on our method’s performance in Sections IV-D and VII-B, respectively. We compute DFrFTs with angles using an eficient and generalized version of the MDFrFT [1], which we introduce in Section IV-A.

In our algorithm, we use (6) to compress and detect an interference chirp $s _ { I }$ within a radar signal s. For analysis purposes, we split s into the interference chirp we want to compress in a given iteration of our method and a residual signal $s _ { R } ,$ , i.e., $s = s _ { I } + s _ { R }$ . Equation (6) applied to s and $s _ { R }$ returns ˆ , ˆn, ˆ <sub>R</sub> and $\hat { n } _ { R } ,$ , respectively; note that in practice, we only have access to s. If

$$
\left| W _ { \hat { \alpha } _ { I } } \pmb { s } _ { I } \right| \left[ \hat { n } _ { I } \right] > \left| W _ { \hat { \alpha } _ { R } } \pmb { s } _ { R } \right| \left[ \hat { n } _ { R } \right] , \quad \hat { \alpha } _ { I } , \hat { \alpha } _ { R } \in \alpha\tag{7}
$$

then $\hat { \alpha } ~ \approx ~ \hat { \alpha } _ { I }$ and $\hat { n } ~ \approx ~ \hat { n } _ { I }$ , which means that applying (6) to s essentially returns the same result as when applied to $s _ { I } .$ The superposition of $s _ { I }$ and ${ \pmb S } _ { R }$ might cause deviations of the estimated $\hat { \alpha } , \hat { n }$ from the sought $\hat { \alpha } _ { I } , \hat { n } _ { I } ;$ however, these deviations are negligible if $| W _ { \hat { \alpha } _ { I } } s _ { I } | [ \hat { n } _ { I } ] \gg | W _ { \hat { \alpha } _ { I } } s _ { R } | [ \hat { n } _ { I } ]$ , which is mostly the case in practice. An example for a signal where (7) holds is depicted in Fig. 3(a).

In practice, we do not have access to s<sub>I</sub> and $s _ { R }$ and therefore cannot verify whether (7) is true for a found peak $( W _ { \hat { \alpha } } { s } ) [ \hat { n } ]$ . In other words, we need a diferent approach to confirm that the global maximum $( W _ { \hat { \alpha } } { s } ) [ \hat { n } ]$ is caused by an interference and not by objects and noise. Therefore, we use a CFAR-detector: If the global maximum’s power exceeds a predefined threshold $\beta$ compared to a reference $\hat { \sigma } ^ { 2 }$ , we classify it as interference, that is, we determine that (7) holds. We choose the average power of ${ \pmb S } _ { R }$ as the reference $\hat { \sigma } ^ { 2 }$ , which is estimated by the CFAR detector using a window of size Φ to either side of $( W _ { \hat { \alpha } } { s } ) [ \hat { n } ]$

$$
\hat { \sigma } ^ { 2 } = \frac { 1 } { 2 \Phi } \sum _ { n \in \mathrm { w i n d o w } } \left( \vert W _ { \hat { \alpha } } s \vert \left[ n \right] \right) ^ { 2 } \approx \frac { 1 } { 2 \Phi } \sum _ { n \in \mathrm { w i n d o w } } \left( \vert W _ { \hat { \alpha } } s _ { R } \vert \left[ n \right] \right) ^ { 2 }\tag{8}
$$

$$
\approx \frac { 1 } { N } \sum _ { n = 0 } ^ { N - 1 } ( \vert W _ { \hat { \alpha } } s _ { R } \vert \left[ n \right] ) ^ { 2 } = \frac { 1 } { N } \sum _ { n = 0 } ^ { N - 1 } \vert s _ { R } [ n ] \vert ^ { 2 } .\tag{9}
$$

Note that in (9) we utilize the DFrFT’s unitary property; furthermore, within the CFAR detector’s window ${ \pmb W } _ { \hat { \alpha } } { \pmb s } \approx { \pmb W } _ { \hat { \alpha } } { \pmb s } _ { R }$ because $W _ { \hat { \alpha } } \pmb { s } _ { I }$ being sparse, which we use in (8). We estimate the average power of $s _ { R }$ instead of the noise $\pmb { S } \mathcal { N }$ , which helps us to distinguish between global maxima caused by interferences and objects, as we will explain in Section III-A. The estimate $\hat { \sigma } ^ { 2 }$ contains the energy of objects, noise, and <sup>σ</sup>other interferences. Objects increasing $\hat { \sigma } ^ { 2 }$ are not an issue in practice as they only lead to missed detections of interferences that are significantly weaker than these objects. To minimize the influence of other interferences on $\hat { \sigma } ^ { 2 }$ corrupting some regions of $W _ { \hat { \alpha } } \pmb { s }$ [see, for example, Fig. 3(a)], we use a <sup>α</sup>least-of CFAR (LO-CFAR) detector, where we compute a separate estimate for either side of $( W _ { \hat { \alpha } } { s } ) [ \hat { n } ]$ and then pick the lower one. We also place G guard cells on either side of the global maximum to deal with the imperfect compression of the interference, which is caused by windowing, the anti-aliasing filter, the DFrFT implementation, interferences not crossing the entire receiver bandwidth (as described in Section III-B), and the time-discrete nature of s. These guard

(a)

```tcl
Algorithm 1 IM Using the EMDFrFT
IMFRAC(s): {s is a possibly interfered fast-time sequence}
initialize M {row indices of DFrFTs with angles }
$\mathbf { \Delta } s \gets s \odot \boldsymbol { w }$ {apply window function}
s ← ZeroPad(s) {optional, see Section $\mathrm { I V - C } \}$
do
$S \gets \mathrm { E M D F r F T } ( s )$ {see Section IV-A}
$\hat { m } , \hat { n } \gets \arg \operatorname* { m a x } | M \odot S |$ {get indices of maximum}
$\pmb { d } \gets \mathrm { L O - C F A R } ( S [ \hat { m } ] , \hat { n } )$ {d is a binary mask}
$s \gets d \odot S [ \hat { m } ]$ {set interfered samples to zero}
$M , m _ { R S } \gets \mathrm { G e t R o w s } ( \hat { m } , d )$ {use angle additivity}
while d contains a detection {i.e., contains a zero}
$S [ m _ { R S } ] \gets \mathrm { C r o p } ( S [ m _ { R S } ] )$ {optional, see Section IV-C}
$S [ m _ { R S } ]  \mathrm { L o w P a s s } ( S [ m _ { R S } ] )$ {optional, see Section IV-C}
return $S [ m _ { R S } ]$ {interference mitigated range-spectrum}
```

cells are excluded from the estimation of the residual signal’s average power.

If the global maximum has been classified as interference, we can remove it by setting $( W _ { \hat { \alpha } } { s } ) [ \hat { n } ]$ and the surrounding guard cells to zero, i.e., we compute $\pmb { d } \odot ( W _ { \hat { \alpha } } \pmb { s } )$ , where  is an element-wise multiplication and d a binary mask returned by the CFAR detector. Note that by zeroing we also remove $( W _ { \hat { \alpha } } { \pmb { s } } _ { R } ) [ \hat { n } ]$ in addition to $( W _ { \hat { \alpha } } { \pmb { s } } _ { I } ) [ \hat { n } ]$ as a side efect.

After removing $s _ { I } ,$ we can retrieve the corresponding timedomain signal by evaluating $W _ { - \hat { \alpha } } ( \pmb { d } \odot ( \pmb { W } _ { \hat { \alpha } } \pmb { s } ) )$ , and then loop the process introduced above to search for more interference chirps within that signal. As described in Section IV, we simplify our algorithm by skipping the inverse DFrFT using its angle-additivity property and compute (6) directly on $\pmb { d } \odot ( W _ { \hat { \alpha } } \pmb { s } )$ in the next iteration of our method. We exit this loop and terminate our algorithm once it does not detect any other interference chirp, i.e., when the energy of the global maximum compared to $\hat { \sigma } ^ { 2 }$ drops below the CFAR detector’s threshold $\beta ;$ this is the case in Fig. 3(b). As we repeatedly search for the global maximum in a signal’s set of DFrFTs, the algorithm removes interference chirps sorted by their energy, starting with the most energetic. The complete algorithm, including all optimizations introduced in Section IV, is summarized in Algorithm 1.

## A. Distinguishing Objects From Interferences

In our algorithm, the only distinction between interference chirps and objects is their chirp rate, with objects having a chirp rate of zero, i.e., being constant frequencies. If we were to apply (6) to radar signal that only contains weak interferences or none at all, we would find that for $\alpha _ { \mathrm { m a x } } \geq 9 0 ^ { \circ }$ $\hat { \alpha } = \pm 9 0 ^ { \circ }$ <sup>α</sup>corresponding to the range-spectrum compressing objects into peaks. We prevent the false classification of objects as interferences by setting $\alpha _ { \mathrm { m a x } } < 9 0 ^ { \circ }$ . In other words, we shrink such that (7) also holds for s where the energy of $s _ { I }$ is smaller than some given fraction of the strongest object’s energy. From a statistical point of view, interferences with lower chirp rates become increasingly unlikely [40], which means that we can choose $\alpha _ { \mathrm { m a x } }$ slightly smaller than $9 0 ^ { \circ }$ and still suficiently compress most interferences. The choice of $\alpha _ { \mathrm { m a x } }$ is a tradeof between minimizing false positives versus false negatives. As an additional measure, we lower G of the CFAR detector to prevent false positives at fractional angles $\pm \alpha _ { \mathrm { m a x } }$ thanks to insuficient compression of objects. More concretely, objects $W _ { \pm \alpha _ { \mathrm { m a x } } } s _ { O }$ raise $\hat { \sigma } ^ { 2 }$ due to their spread larger than 2G, which keeps the CFAR detector’s computed energy diference below its detection threshold $\beta .$ In Fig. 3(b) we can observe how objects become more and more compressed as we approach $\alpha = \pm 9 0 ^ { \circ }$ ; however, $\alpha = \pm 9 0 ^ { \circ }$ is not included in the search space as $\alpha _ { \mathrm { m a x } } = 8 0 ^ { \circ }$ <sup>α</sup>in Fig. 3(b). A completely alternative approach would consist of unifying object and interference detection, treating detections at $\pm 9 0 ^ { \circ }$ diferently from detections at any other ; we leave this idea for further research.

![](images/a72a62ec6213e6afb19ec9438f08038a1af89f6ee54a7ae8fa4846d0501366d7.jpg)

![](images/d45f67110518456425baf5126d96cbd3935ff3938505efa764d6ccb0c66b032e.jpg)  
(b)  
Fig. 4. (a) STFT of a radar signal with an incomplete interference. (b) Magnitudes of the corresponding interference and ground truth signals after a DFrFT with $\hat { \alpha } \approx 4 5 ^ { \circ }$ . The signals have been normalized and padded <sup>α</sup>with the technique described in Section IV-C.

## B. Incomplete Interferences

Interferences have a certain starting and ending time, which are determined by the interferer and victim radars’ parameters. One of the radar’s fast-time sequences might end before the interference chirp crosses the entire receiver bandwidth, resulting in an incomplete interference. An interference also becomes incomplete if we zero another interference that crosses it in the time–frequency plane; we discuss this scenario in Section III-C. The fractional representation $W _ { \hat { \alpha } _ { I } } { \pmb { s } } _ { I }$ of such an interference does not contain all frequency components, i.e., it is not ideally compressed in the fractional domain. For very narrow interference bandwidths, our method fails to detect and therefore mitigate such interferences. Depending on the frequencies contained in $W _ { \hat { \alpha } _ { I } } { \pmb { s } } _ { I } ,$ , we can still detect incomplete interferences by increasing G of the CFAR interference detector to account for their larger spread. However, as explained in Section III-A, G should be as small as possible to avoid misclassifying objects as interferences. An example of an incomplete interference can be seen in Fig. 4.

## C. Crossing and Noncrossing Interferences

If the receive signal is corrupted by multiple interferences, we can distinguish between interference chirps that cross in the time–frequency domain and those that do not. Noncrossing interferences can be mitigated independently of one another, i.e., zeroing one interference chirp does not alter the appearance of the other. A prominent example of noncrossing interferences is the victim getting interfered by the same interferer multiple times within the same fast-time sequence, resulting in multiple interference chirps with the same chirp rate. If the interference chirps do cross in the time–frequency domain, then zeroing one interference will also zero a small portion of the other, resulting in an incomplete interference, complicating its subsequent detection and mitigation. While it is possible to construct scenarios where zeroing one interference would render another interference undetectable, e.g., crossing interferences with almost identical chirp rates, we argue that crossing interferences are not problematic in the vast majority of scenarios. This unintended partial zeroing is analogous to zeroing parts of the object signal that overlap with interferences. An example for the quantitative impact of this side efect can be seen in Fig. 2(b) by comparing the ground truth to the interference mitigated range-spectrum; in the interference mitigated range-spectrum, the objects are not as compressed as in the ground truth range-spectrum due to partial zeroing visible in Fig. 5(c) and (d). However, this efect is so small that the objects can still be detected by a CFAR detector. Furthermore, partially zeroed interferences could be interpolated in future work using the methods described in Section VIII-B. The runtime is identical for the crossing and the noncrossing case, namely $N _ { I } + 1$ iterations of computing DFrFTs, CFAR-detection, and zeroing.

(a)  
![](images/fdf39d569a1beb9c1807b15ec4f481d03e6cd752d87255b25fcd0b362ce50c12.jpg)  
(b)

![](images/b8e4780f94b5b66bb1f8861c8e005d8395014448643504e68132b3b719d38488.jpg)  
(c)

![](images/8bf4030df7f1ec665b83bd1bcc568cbb70e5edf921cd42adb1c1afc3835379f5.jpg)  
(d)  
Fig. 5. Interference component from Fig. 2 with (a) and without (b) the padding introduced in Section IV-C. STFTs of the interference mitigated signal from Fig. 2 without (c) and with (d) a smoothening kernel; (c) is the STFT of the interference mitigated signal in Fig. 2(a). All plots are normalized and in dB.

## IV. IMPLEMENTATION AND COMPUTATIONALCOMPLEXITY

As described in Section III, our algorithm removes one interference at a time by computing a bank of DFrFTs, finding and classifying the global maximum, followed by zeroing. The computational complexity is dominated by the bank of DFrFTs, which in turn depends on the DFrFT implementation used. We base our DFrFT implementation on the method introduced in [1], which we call the MDFrFT; they showed that for a signal with length N, a bank of eigendecompositionbased centered DFrFTs with N equally spaced fractional angles ¯ between $- 1 8 0 ^ { \circ }$ and 180<sup>◦</sup> has complexity $\mathcal { O } ( N ^ { 2 }$ log N) instead of $\mathcal { O } ( N ^ { 3 } )$ . The MDFrFT S<sup>¯</sup> of a signal s is computed as

$$
\bar { S } [ p , n ] = \mathrm { F F T } _ { p } \left\{ \bar { Z } [ p , n ] \right\}\tag{10}
$$

$$
\bar { \pmb { Z } } [ p , n ] = { \pmb { V } } ^ { \mathrm { T } } [ p , n ] \left( { \pmb { V } } ^ { \mathrm { T } } { \pmb { s } } \right) [ p ]\tag{11}
$$

where $\mathrm { F F T } _ { p } \{ \bar { \pmb { Z } } [ p , n ] \}$ represents column-wise FFTs of $\bar { \mathbf Z }$ and $V$ is the matrix of centered DFT eigenvectors. Each row $\bar { \mathbf { S } } [ p ]$ contains one of the DFrFTs with fractional angles ¯ . Note that evaluating the FFTs in (10) has complexity $\mathcal { O } ( N ^ { 2 }$ log N), while computing Z<sup>¯</sup> has complexity $\mathcal { O } ( N ^ { 2 } )$ . The MDFrFT returns the exact same result as distinct eigendecomposition-based DFrFTs with angles ¯ .

## A. EMDFrFT

As discussed in Sections IV-D and VII-B, the number of evaluated fractional angles can be significantly lower than N without impacting performance. However, the MDFrFT as proposed by [1] always computes N angles. We generalize and reduce the computational complexity of the MDFrFT by computing M equally spaced fractional angles $\alpha _ { M } ,$ where Nmod $M = 0 .$ <sup>α</sup>. This can easily be achieved by aliasing $\bar { \mathbf Z }$ along its columns, which is equivalent to downsampling $\bar { s }$ along its columns [41], i.e., $S [ m , n ] = \bar { S } [ m N / M , n ]$ , where

$$
S [ m , n ] = { \mathrm { F F T } } _ { m } \left\{ Z [ m , n ] \right\} , \quad m \in \{ 0 , 1 , \ldots , M - 1 \}
$$

$$
{ \cal Z } [ m , n ] = \sum _ { l = 0 } ^ { \frac { N } { M } - 1 } { \bar { \cal Z } } [ m + l M , n ] .\tag{12}
$$

(13)

As we have now replaced N-point by M-point FFTs, the computational complexity of the required FFTs is O(NM log M). For small M, the overall complexity of our EMDFrFT is $\mathcal { O } ( N ^ { 2 } )$ since it is now dominated by the computation of Z<sup>¯</sup> . However, Z<sup>¯</sup> can be calculated more eficiently by applying methods from [1], [42], [43], among others. Possible hardware architectures for such eficient eigendecompositionbased DFrFTs are described in [44]. Furthermore, Erseghe and Cariolaro [45] have proposed an algorithm for computing the DFT through its eigendecomposition with complexity O(N log N). If such an algorithm could be used to calculate (11), the MDFrFT and EMDFrFT would only consist of highly eficient divide-and-conquer-based algorithms. In [38], we halved the FFTs’ computational burden within the MDFrFT by considering the symmetries of the DFT eigenvectors. Analog implementations of the DFrFT, such as [46], are also promising directions for future research, as they completely circumvent the computational burden of digital DFrFT implementations.

## B. Using the EMDFrFT for IM

The EMDFrFT computes DFrFTs for M equally spaced fractional angles $\alpha _ { M }$ between $- 1 8 0 ^ { \circ }$ and $1 8 0 ^ { \circ }$ ; however, as described in Section III, we constrain our search space to $N _ { \alpha }$ angles  with $| \alpha | < \alpha _ { \mathrm { m a x } }$ . We therefore retrieve the DFrFTs we include in the grid-search from the EMDFrFT as

$$
\begin{array} { r } { \pmb { \alpha } = \left\{ \alpha \in \pmb { \alpha } _ { M } , | \alpha | < \alpha _ { \operatorname* { m a x } } \right\} . } \end{array}\tag{14}
$$

This means that

$$
N _ { \alpha } = \left\lfloor { \frac { 2 \cdot M \cdot \alpha _ { \mathrm { m a x } } } { 3 6 0 ^ { \circ } } } \right\rfloor\tag{15}
$$

with $\alpha _ { \mathrm { m a x } }$ in degrees.

If our algorithm performs multiple iterations, we can use the angle-additivity property of eigendecomposition-based DFrFTs to compute the next EMDFrFT directly on $\pmb { d } \circ ( \pmb { W } _ { \hat { \alpha } } \pmb { s } )$ , where ${ \hat { \alpha } } \in \alpha$ <sup>α</sup>is the found fractional angle in the previous iteration of our method. As $\alpha _ { M }$ consists of equally spaced fractional angles between $- 1 8 0 ^ { \circ }$ and 180<sup>◦</sup>, the set of angles evaluated in the subsequent iteration is invariant to ˆ and therefore remains $\alpha _ { M }$ <sup>α</sup>. This means that we can implement (14) by simply tracking the row indices of S that correspond to angles over consecutive iterations, which are cyclically row-<sup>α</sup>wise shifted within S depending on ˆ . More formally, in each iteration, we construct a binary matrix M such that rows of $M \odot S$ corresponding to <sup><</sup> are set to zero.

If M is a multiple of 4, the DFT of s is computed as part of the EMDFrFT. Therefore, the range-FFTs in the radar signal processing chain can be removed and absorbed into the EMDFrFT, as is depicted in Fig. 1. If our method performs multiple iterations, we additionally track the row index of the range-spectrum $m _ { \mathrm { R S } }$ within S.

## C. Padding the Time–Frequency Representation

In our implementation, we generate the DFT eigenvectors V as proposed in [47], which approximate the continuous FT eigenfunctions with concepts from quantum mechanics in finite dimensions. To deal with the approximation error, we found it helpful to zero-pad and oversample the input signals s. More concretely, we increase the sampling rate of the radar sensor’s analog-digital converter to about $\gamma \cdot 2 \ f _ { c } ,$ $\gamma = 1 . 3 2$ , where $f _ { c }$ is the cutof frequency of the anti-aliasing filter. Furthermore, we prepend and append all processed radar signals s with b · Nc zeroes after applying the windowing <sup>γ</sup>function. We derived heuristically by fitting a circle around the original signal’s time–frequency representation. Without padding, a DFrFT implementation using V from [47] fails to properly transform signal components which are located in the corners of the signal’s time–frequency representation. This results in suboptimal compression for LFM chirps that contain such components, as can be seen in Fig. 5(b). These artifacts occur when a signal does not decay to zero at its boundaries for all fractional angles. The same LFM chirp with our proposed padding scheme is shown in Fig. 5(a), which collapses to a single peak at approximately $- 6 0 ^ { \circ }$ as intended. We have also evaluated eigenvectors by [31] and [48] and observed the same issues, which we mitigated with our padding scheme.

TABLE II  
APPROXIMATE WORST CASE WIDTHS OF INTERFERENCES
<table><tr><td rowspan=1 colspan=1>M</td><td rowspan=1 colspan=1> $\overline { { N _ { \alpha } } }$  ${ \mathrm { i f ~ } } \alpha _ { \mathrm { m a x } } = 8 0 ^ { \circ }$ </td><td rowspan=1 colspan=1> $\alpha _ { \Delta , \mathrm { m a x } }$ </td><td rowspan=1 colspan=1> $| \sin ( \alpha _ { \Delta , \mathrm { m a x } } ) |$ </td><td rowspan=1 colspan=1> $\delta _ { \mathrm { m a x } }$  ${ \mathrm { i f ~ } } N = 5 1 2$ </td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1> $\overline { { 2 2 . 5 ^ { \circ } } }$ </td><td rowspan=1 colspan=1>38.27%</td><td rowspan=1 colspan=1>196</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1> $\overline { { 1 1 . 2 5 ^ { \circ } } }$ </td><td rowspan=1 colspan=1>19.51%</td><td rowspan=1 colspan=1>100</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1> $\overline { { 5 . 6 3 ^ { \circ } } }$ </td><td rowspan=1 colspan=1>9.80%</td><td rowspan=1 colspan=1>51</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1> $\overline { { 2 . 8 1 ^ { \circ } } }$ </td><td rowspan=1 colspan=1>4.91%</td><td rowspan=1 colspan=1>26</td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>57</td><td rowspan=1 colspan=1>1.41°</td><td rowspan=1 colspan=1>2.45%</td><td rowspan=1 colspan=1>13</td></tr><tr><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>113</td><td rowspan=1 colspan=1> $\overline { { 0 . 7 0 ^ { \circ } } }$ </td><td rowspan=1 colspan=1>1.23%</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>227</td><td rowspan=1 colspan=1>0.35°</td><td rowspan=1 colspan=1>0.61%</td><td rowspan=1 colspan=1>4</td></tr></table>

Zeroing an interference induces broadband components into the signal’s fractional representation $W _ { \hat { \alpha } } \pmb { s }$ , which might lead to artifacts after another subsequent DFrFT. Such artifacts with their circular-shaped appearance can be seen at the edges of Fig. 5(c). If we perform padding and oversampling as introduced above, these artifacts are temporally and spectrally separated from the signal, and can therefore be removed after termination of our algorithm by cropping and low-pass filtering the interference mitigated range-spectrum. Without padding, the artifacts overlap with the object signal and cannot be removed anymore. An alternative approach to deal with these artifacts consists of zeroing with a smoothening kernel, e.g., a raised cosine window, which depends on the location of the interference within the EMDFrFT. If we zero samples at fractional angles ${ \approx } 4 5 ^ { \circ }$ and close to the boundaries of the signal’s fractional representation, we widen the smoothening kernel such that only low frequencies are suppressed. Therefore, the smoothening kernel prevents artifacts, and subsequent cropping and filtering can be avoided. An example is visualized in Fig. 5(d). Our algorithm can be improved in future research by finding DFT eigenvectors that do not require such padding and oversampling.

## D. Influence of Angular Resolution on Compression Strength

Let $s _ { I } ( t )$ be a continuous time-limited LFM chirp signal with chirp rate k, which is compressed most strongly when applying an FrFT with fractional angle $\hat { \alpha } _ { I } = \operatorname { a r c c o t } ( k ) . ^ { 1 }$ Furthermore, let L be the width of ${ \mathcal { F } } _ { \tilde { \alpha } _ { I } } s _ { I } ( t )$ <sup>α</sup>, with $\tilde { \alpha } _ { I } = \hat { \alpha } _ { I } + 9 0 ^ { \circ }$ , which transforms $s _ { I } ( t )$ into a time-limited sinusoid. Because an FrFT is, in simple terms, a rotation of the time–frequency plane, the width of ${ \mathcal { F } } _ { \alpha } s _ { I } ( t )$ is approximately $L \cdot | \sin ( \alpha _ { \Delta } ) | .$ , where $\alpha _ { \Delta } =$ $| \hat { \alpha } _ { I } - \alpha |$ . Note that this approximation ignores the influence of side lobes which follow from $s _ { I } ( t )$ being time-limited; for instance, the actual width of $\mathcal { F } _ { \hat { \alpha } _ { I } S I } ( t )$ is 0. If we now assume an idealized DFrFT $W _ { a }$ <sup>α ></sup>which transforms a discrete LFM chirp signal $s _ { I } ,$ where $W _ { \tilde { \alpha } _ { I } } { \pmb S } _ { I }$ spans the entire signal length N, we find that the width of that interference is approximately $\delta : =$ $\lceil N \cdot | \sin ( \alpha _ { \Delta } ) | \rceil$ samples.

Using these approximations, we can now show that for a given number of fractional angles M we can aford to evaluate,

(b)

![](images/3d376375504b98421071ab0260fc395c4bc3ace99b5be2e3f0b4e5a28b4d0ab8.jpg)  
(a)  
Fig. 6. (a) EMDFrFT magnitudes of the interference component of Fig. 4. (b) EMDFrFT magnitudes of the signal in Fig. 5(a) after setting some timedomain samples to zero, turning it into an incomplete interference.

the uniform angular resolution of the MDFrFT and EMDFrFT minimizes the worst case interference width $\delta _ { \mathrm { m a x } }$ for all possible chirp rates k. For the MDFrFT and the EMDFrFT which evaluate fractional angles $\alpha _ { M }$ , a mismatch $\alpha _ { \Delta }$ is given by

$$
\alpha _ { \Delta } = \vert \hat { \alpha } _ { I } - \alpha _ { \mathrm { c l o s e s t } } \vert \le \alpha _ { \Delta , \mathrm { m a x } }
$$

where $\alpha _ { \mathrm { c l o s e s t } } ~ \in ~ \pmb { \alpha } _ { M }$ is the element minimizing the devia-<sup>α</sup>tion from $\hat { \alpha } _ { I }$ <sup>α</sup>. We have ${ \alpha _ { \Delta } } \ = \ { \alpha _ { \Delta , \mathrm { { m a x } } } }$ if $\hat { \alpha } _ { I }$ falls exactly in between the two closest elements of $\mathbf { \Omega } _ { \alpha _ { M } } ,$ which means that $\alpha _ { \Delta , \mathrm { { m a x } } } ~ = ~ 1 8 0 ^ { \circ } / M ;$ however, this also means that, by the pigeonhole principle on continuous spaces, $\alpha _ { \Delta , \mathrm { m a x } } > 1 8 0 ^ { \circ } / M$ for any nonuniform spacing between elements of $\alpha _ { M }$ as there exists some interference angle where the deviation to $\alpha _ { \mathrm { c l o s e s t } }$ is larger. Since $\delta _ { \mathrm { m a x } } = \lceil N \cdot | \sin ( \alpha _ { \Delta , \mathrm { m a x } } ) | \rceil$ is growing monotonously for $0 < \alpha _ { \Delta , \mathrm { m a x } } < \pi / 2$ <sup>α ,</sup>, this uniform spacing also minimizes $\delta _ { \mathrm { m a x } } .$ . Therefore, the uniform spacing of $3 6 0 ^ { \circ } / M$ provided by the MDFrFT and EMDFrFT minimizes $\delta _ { \mathrm { m a x } }$ for a given M (and, transitively, $N _ { \alpha } )$ such that all possible interferences are <sup>α</sup>suficiently compressed to be detectable. In Table II we can see the approximate worst case widths as percentages of $L ,$ as well as $\delta _ { \mathrm { m a x } }$ for diferent M and $N _ { \alpha }$

As already mentioned, these derivations only hold for idealized cases; in practical applications, the anti-aliasing filter and windowing are additional limiting factors for pulsecompressing interferences. If we extend our considerations to include the side lobes that follow from windowing or low-pass filtering chirps, we expect  to be less sensitive to $\alpha _ { \Delta }$ than in the idealized case, allowing us to lower M with smaller efects on $\delta _ { \mathrm { m a x } }$ than in Table II. More concretely, for a windowed and low-pass filtered chirp, the width of $W _ { \tilde { \alpha } _ { I } } { \pmb s } _ { I }$ decreases while the width of $W _ { \hat { \alpha } _ { I } } { \pmb { s } } _ { I }$ increases. The width of such an interference, depending on $\alpha ,$ can be seen in Fig. 5(a). The strength of this efect then depends on the low-pass filter’s cut-of frequency as well as the timing and chirp rate of the interference. In extreme cases, such chirps might look like the one shown in Fig. 4; as visible in Fig. $6 ( \mathrm { a } ) ,$ the width of these interferences is even less sensitive to $\alpha _ { \Delta } .$ . This in turn means that a small value <sup>α</sup>for M is suficient for treating such interferences, as none of the elements of $\alpha _ { M }$ can strongly compress the interference. In Fig. 6(b) we can see the EMDFrFT magnitudes of an incomplete interference which has partially been zeroed; this occurs if another interference, that had its maximum at that location, has previously been zeroed. Now, in addition to the peak, the interference is spread out across the fractional domain $\hat { \alpha } _ { I }$ with low energy. In general, it is dificult to estimate the width of incomplete interferences. In Section VII-B, we experimentally show that the EMDFrFT’s angular resolution can be reduced to $N _ { \alpha } = 2 9$ with only minor impacts on IM performance. For $N _ { \alpha } < 2 9$ , choosing $N _ { \alpha }$ becomes a tradeof between computational complexity and performance.

TABLE III  
PARAMETERS OF VICTIM RADAR
<table><tr><td rowspan=1 colspan=2>Parameter</td></tr><tr><td rowspan=1 colspan=1>Transmit starting frequency</td><td rowspan=1 colspan=1>79 GHz</td></tr><tr><td rowspan=1 colspan=1>Transmit bandwidth $\overline { { ( 2 { \cal B } _ { V } ) } }$ </td><td rowspan=1 colspan=1>0.25 GHz</td></tr><tr><td rowspan=1 colspan=1>Ramp duration $\overline { { ( 2 { T _ { V } } ) } }$ </td><td rowspan=1 colspan=1>12,8 µs</td></tr><tr><td rowspan=1 colspan=1>Window type (range &amp; Doppler)</td><td rowspan=1 colspan=1>Hann</td></tr><tr><td rowspan=1 colspan=1># Fast-time samples (N)</td><td rowspan=1 colspan=1>512</td></tr><tr><td rowspan=1 colspan=1># Slow-time samples</td><td rowspan=1 colspan=1>128</td></tr></table>

## E. Algorithm

The final algorithm labeled $I M f r a c ^ { 2 }$ that includes all optimizations is summarized in Algorithm 1.

## V. RELATIONSHIP TO OTHER METHODS

In this section, we elaborate on how our proposed algorithm fits into the landscape of IM methods, which we have already briefly introduced in Section I and Table I.

## A. Relationship to Zeroing

Zeroing [3] is one of the most common algorithms used for FMCW mutual IM due to its predictable and transparent behavior. It works by detecting interferences in the timedomain input signal and simply setting all afected samples to zero. In the context of our proposed algorithm, zeroing can be viewed as a special case with $\alpha ~ = ~ \{ 0 ^ { \circ } \}$ ; therefore, we argue that our method is an improved version of zeroing. The performance of zeroing highly depends on the interference detector. As the appearance of interferences in the time-domain is highly diverse, designing a robust interference detector is challenging; approaches include outlier or envelope changepoint detection [49], which assumes that interfered parts of the signal have higher amplitude compared to clean signal parts. By compressing the interference using the EMDFrFT, interference detection reduces to simple peak detection. In our method, we use the EMDFrFT as a means for both detecting and mitigating mutual interference; However, the EMDFrFT could also be used solely as an interference detector, which is then combined with some alternative treatment of the interference. We argue that, in fact, the EMDFrFT constitutes a highly performant LFM chirp interference detector due to its close relation to a bank of matched filters (see Section V-B).

Even with perfect interference detection, the performance of zeroing is still limited by the interference’s chirp rate. Assuming an interference that crosses the victim radar’s entire bandwidth, an interference with a lower chirp rate will afect a higher number of time-domain samples. Consequently, the number of zeroed time-domain samples increases, removing a larger proportion of the object signal as a side efect. When zeroing in the fractional domain, the loss of object signal components is much smaller and independent of the interference’s chirp rate. This independence is especially relevant for subsequent object detections on RD-maps. The efects of IM on RD-maps are exemplified in Fig. 7. Zeroing typically leads to highly increased side lobes along the Doppler axis of an RDmap, as visible in Fig. 7(d). This happens because the varying number of zeroed time-domain samples leads to object peaks having fluctuating amplitudes in the corresponding rangespectra. Computing the Doppler-FFT across these peaks then causes the aforementioned side lobes. IM based on the DFrFT does not sufer from this problem, strongly increasing object detection performance, as visible in Fig. 7(c) and (g).

(c)  
![](images/52c9a68473786e6d79245a03d8aebdb406b15ad7c497f947cb15fcc452c032eb.jpg)

![](images/05a7007b837170c6c2961fd84de5d0167119445d25e29323a032963e366c0436.jpg)  
(b)

![](images/d17195b23ead204783f20084f86f32ee801193154e43fc30488fee6ceba45f32.jpg)

![](images/7c29d6135e4476852999fde4cf4e400e92cd3e77db17b03b18b510580bd21a21.jpg)

![](images/8a3518938724b58ea13fda72ab20e0ff84ddf035802eef1699d92b64349b2ddf.jpg)  
(e)

![](images/734558b406187eb2e459a99c222189d8ff738b60faef681c9a551ba9b411ed48.jpg)  
(f)

![](images/5174fc15106a42bc7a0a7113f97894e4b17d3e527509cc84db9e306838d9b6f6.jpg)  
(g)

(d)  
![](images/71d1a7a7b178a3ef7425bc8a762b1523f78353ac76a0b4ccccf59a37d1643c31.jpg)  
(h)  
Fig. 7. Examples of RD-maps. (a) Interfered RD-map. (b) Corresponding ground truth RD-map. (c) Interference was mitigated in the RD-map using our method. (d) Interference mitigated RD-map using zeroing with perfect interference detection. (e)–(h) Object detection maps as retrieved by a CFAR object detector when applied to RD-maps (a)–(d). Gray, red, orange, and green bins correspond to true negatives, false negatives, false positives, and true positives, respectively.

TABLE IV  
PARAMETER RANGES FOR INTERFERENCE SIGNALS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>minimum</td><td rowspan=1 colspan=1>maximum</td></tr><tr><td rowspan=1 colspan=1># Interferers</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Transmit starting frequency</td><td rowspan=1 colspan=1>78.9 GHz</td><td rowspan=1 colspan=1>79.0 GHz</td></tr><tr><td rowspan=1 colspan=1>Transmit bandwidth $\overline { { ( 2 { \cal B } _ { I } ) } }$ </td><td rowspan=1 colspan=1>0.2 GHz</td><td rowspan=1 colspan=1>0.3 GHz</td></tr><tr><td rowspan=1 colspan=1>Ramp duration $\overline { { ( 2 T _ { I } ) } }$ </td><td rowspan=1 colspan=1>10 µs</td><td rowspan=1 colspan=1> $1 5 ~ \mu s$ </td></tr><tr><td rowspan=1 colspan=1># Slow-time samples</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>156</td></tr><tr><td rowspan=1 colspan=1>Dynamic range between interferers</td><td rowspan=1 colspan=1>0 dB</td><td rowspan=1 colspan=1>80 dB</td></tr></table>

TABLE V

## B. Relationship to Matched Filtering

Matched filtering is a well-established concept in signal processing and has a multitude of applications in fields like communications and radar. In pulse radar, matched filters are used to detect the presence of a transmit signal template in a noisy echo. In fact, one of the most common signal templates in pulse radar is LFM chirps, as their radar ambiguity function has desirable properties [50]. Since LFM chirps are also observed as FMCW mutual interference, an approach for IM inspired by matched filtering is worth investigating.

PARAMETERS OF IMFRAC
<table><tr><td rowspan=1 colspan=2>Parameter</td></tr><tr><td rowspan=1 colspan=1># Evaluated fractional angles $\overline { { ( N _ { \alpha } ) } }$ </td><td rowspan=1 colspan=1>113</td></tr><tr><td rowspan=1 colspan=1>Maximal fractional angle $\left( \alpha _ { \mathrm { m a x } } \right)$ </td><td rowspan=1 colspan=1>80°</td></tr><tr><td rowspan=1 colspan=1>Window-size interference detector (Φ)</td><td rowspan=1 colspan=1> $\overline { { N / 2 - G - 1 } }$ </td></tr><tr><td rowspan=1 colspan=1># Guard cells of interference detector (G)</td><td rowspan=1 colspan=1> $\overline { { 2 0 } }$ </td></tr><tr><td rowspan=1 colspan=1>Threshold of interference detector (β)</td><td rowspan=1 colspan=1>20 dB</td></tr></table>

Our proposed method can be thought of as a bank of time-varying matched filter approximations, where each of the filters is tuned to an LFM chirp with a specific rate. While in theory one single filter would sufice to detect chirps with diferent rates, we use multiple filters in parallel and pick the one that compresses the interference the most to ensure reliable detection and precise mitigation. The filters are timevarying because DFrFT matrices are not Toeplitz matrices. Finally, matched filters are not necessarily invertible, which is a requirement for our approach based on multiple consecutive DFrFTs.

## C. Relationship to STFT-Based Methods

The STFT is one of the most popular transforms for processing nonstationary signals. Therefore, the STFT has also been used against FMCW mutual interference–examples include [6], [7], [8], among others. Conceptually, the STFT compresses an interference chirp into a line in its 2-D signal representation [e.g., see Fig. 4(a)]; in contrast, like a matched filter, the DFrFT compresses a chirp into an impulse in its 1-D signal representation [e.g., see Fig. 4(b)], given that the $\mathrm { D F r F T ^ { \circ } s }$ fractional angle matches the chirp’s rate. We argue that with the DFrFT, one can detect and null LFM chirp interference more accurately than with the STFT, as the STFT’s time and frequency resolution is upper bounded by the Gabor uncertainty principle [51]; by contrast, when computing a DFrFT, the transformed signal’s resolution remains the input signal length. Therefore, in opposition to Fig. 3(b), the STFTs of the signals after IM in Fig. 5(c) and (d) cannot capture the precision of zeroing in the fractional Fourier domain. However, the STFT may be used to treat any generic nonstationary interference, while the DFrFT, as used in our method, can only detect LFM chirp interference.

![](images/fcddc1753cab46e751004cd531c46bef7f9fb1255dedce6aa7f70704a3722aaa.jpg)

(a)  
![](images/bec1c2b6dac024ae3b206a1500e0cc600690b7272e5bdc7cc4b518502c794d78.jpg)

![](images/ebf9cecf1e19eb4f58e2c1aff5ef81c84251719ee74608b157c74109eebebd5b.jpg)

(b)  
![](images/b3e7fce8a766c4f1dd8ed5d6a9af60eb03378212ae0f1ea08e41e5dfc3fdfeeb.jpg)

![](images/f4913c3155126791f7d644f16dbbe118b3ddaab8a247f85fa616d5796f834351.jpg)

(c)  
![](images/4323954480a88b8225f5ae7fd57003aa25d2cdc332ce99105476d9e552e4c672.jpg)  
Fig. 8. Empirical cumulative density functions (ECDFs) of all evaluated metrics per RD-map. The oracle methods are drawn with dashed lines. Note that we have zoomed into relevant parts of the ECDFs to better resolve close-by curves. (a) MSE. (b) SINR. (c) EVM. (d) TPR. (e) FAR. (f) F1-score.

## D. Relationship to Method by Chen et al. [24]

Independent of our work, Chen et al. [24] recently proposed a method for FMCW mutual IM, which also compresses, detects, and zeroes interference chirps utilizing the FrFT. To iteratively compute approximate forward and inverse DFrFTs, the authors rely on the fast approximate FrFT [25], which has lower computational complexity than an exact eigendecomposition-based DFrFT, but does not ofer angleadditivity, unitarity, and reversibility. While unitarity could in principle be restored by renormalizing the transformed signal, the lack of reversibility accumulates additional errors in the processed radar signal during successive iterations of [24].

![](images/1f63634d00bb8dfc28e859609de6a34a91fac7297fa3b76753f6408c833ac3ec.jpg)  
(a)

![](images/d179b9b7a0cd54d38102552a01900d11ce825a70a2ca06ee671699cef7ca69e5.jpg)  
(b)  
Fig. 9. EMDFrFT magnitudes of the interfered signal in Fig. 2 with (a) $\begin{array} { r l r } { N _ { \alpha } } & { { } = } & { 2 9 } \end{array}$ and (b) $\begin{array} { r l r } { N _ { \alpha } } & { { } = } & { 7 . } \end{array}$ Even though the angular <sup>α α</sup>resolution has been reduced compared to Fig. 3(a), where $\begin{array} { r l r } { N _ { \alpha } } & { { } = } & { 1 1 3 , } \end{array}$ the interferences are still suficiently compressed in <sup>α</sup>(a) so that they can be detected by the LO-CFAR detector. However, in (b), the chirp rates of the interferences do not closely match any of the evaluated fractional angles, such that the interferences are not suficiently compressed, leading to the performance degradation observed in Fig. 10. As we are downsampling the angular resolution in (13) when computing an EMDFrFT, the fractional angles evaluated in (b) are a subset of the fractional angles evaluated in (a), which in turn are a subset of the fractional angles evaluated in Fig. 3(a).

By contrast, we utilize the angle-additivity property of exact DFrFT implementations to skip the inverse DFrFT altogether. Moreover, using the EMDFrFT [1] allows us to compute exact DFrFTs more eficiently whilst absorbing the range-FFTs of the FMCW radar signal processing chain into our algorithm. Both of these optimizations reduce the computational complexity of our method. We argue that for the safety-critical application of automotive radar, it is preferable to use exact DFrFT implementations, as the errors induced by approximate

FrFT implementations reduce the trustworthiness of the IM algorithm’s output.

Chen et al. [24] search for ˆ in an iterative manner using the GSS algorithm; in contrast, our method implements a gridsearch utilizing our EMDFrFT. As in [24], the signals are not renormalized after a fast approximate FrFT; the fractional angle found by the GSS in [24] is not guaranteed to be a maximum due to the lack of unitarity, i.e., it does not necessarily compress an interference optimally. Furthermore, max $( | W _ { \alpha } \pmb { s } | )$ as a function of $\alpha ,$ is not unimodal for any s except for pure LFM chirps, as s may contain objects, noise and multiple interferences. In that case, the GSS only finds a local maximum, which could be caused by weaker interferences, objects, noise, or a superposition thereof. Meanwhile, our method does not make any assumptions on $\operatorname* { m a x } ( | W _ { \alpha } { \pmb s } | )$ , and always returns its approximate global maximum; in Section VII-B we have shown that this approximation of the global maximum does not lead to performance degradation. Finally, we argue that our grid search, which is computed in parallel, is more suitable than the iterative GSS for real-time mutual IM.

Both [24] and our approach mitigate interferences in a loop until all interferences have been removed. However, Chen et al. [24] sets the maximum number of iterations a priori based on the number of interferences in the input signal; our method does not have such a hyperparameter, as we solely rely on the LO-CFAR detector for terminating the algorithm. In [24], they also terminate the algorithm when $\hat { \alpha } \ = \ \pi / 2$ <sup>α π/</sup>With this termination condition, however, interferences with energies lower than the strongest object peak are not detected (assuming a unitary DFrFT implementation and that the GSS finds the global maximum). By contrast, as described in Section III-A, we detect interferences which are weaker than objects by tuning the hyperparameters $\alpha _ { \mathrm { m a x } }$ and the number of guard cells G of the LO-CFAR detector.

After transforming s into the fractional domain with angle ˆ , both methods use a CFAR detector to determine the interfered samples. Chen et al. [24] uses a cell-averaging (CA) CFAR detector on the entire transformed signal, while we use a LO-CFAR detector on its maximum only. By classifying the global maximum only, we ensure that we detect and mitigate exactly one interference chirp per loop, and that this chirp is optimally compressed. Furthermore, we use a LO-CFAR detector instead of a CA-CFAR detector to minimize the influence of other interferences on the CFAR detector’s noise floor estimate.

We compare [24] with our approach in terms of their performance in Section VII.

## VI. EXPERIMENTAL SETUP

## A. Dataset

We evaluate our method using a synthetic I/Q-modulated dataset consisting of 250 fast-time/slow-time sequences. The parameter values for the victim radar are collected in Table III. For every fast-time/slow-time sequence, we generate interferences by uniformly sampling from the interferer parameter ranges summarized in Table IV. Note that the number of interference chirps $N _ { I }$ might be higher than the number of interferers, which is the case if the interferer and victim radars frequency courses cross multiple times within the same victim radar fast-time sequence. We uniformly distribute between 0 and 20 objects across each RD-map with a maximum dynamic range of 60 dB between objects. We retrieve the ground truth object detection maps by running a CA-CFAR detector on the ground truth RD-maps, such that perfect reconstruction of the ground truth RD-maps results in a true positive rate and false negative rate of 1 and 0, respectively. As our simulated dataset does not contain objects with negative ranges, we only consider positive ranges for all metrics described in Section VI-C. An example for an RD-map from our dataset is shown in Fig. 7(a) and (b). The dataset’s distribution of SNRs and signal-to-interference-plus-noise ratios (SINRs) per RDmap can be seen in Fig. 8(b) as ground truth and no mitigation, respectively.

## B. Evaluated Methods

1) IMfrac: We evaluate our proposed method with the parameters summarized in Table V. Furthermore, we compare an oracle that has access to the isolated interference signals $s _ { I }$ as well as the ground truth clean signal $\mathbf { \boldsymbol { s o } } + \mathbf { \boldsymbol { s } } _ { \mathcal { N } } .$ . For each interference chirp $s _ { I } ,$ we find $\hat { \alpha } _ { I }$ using the EMDFrFT. Then, we set all samples $( W _ { \hat { \alpha } _ { I } } s ) [ n ]$ to zero where

$$
\left. W _ { \hat { \alpha } _ { I } } s _ { I } \right. [ n ] > \left. W _ { \hat { \alpha } _ { I } } \left( s _ { O } + s _ { \mathcal { N } } \right) \right. [ n ] .\tag{16}
$$

An example for such a comparison can be seen in Fig. 4(b). The oracle establishes a performance upper bound for our algorithm that can be achieved if we estimate the objectplus-noise floor $\hat { \sigma } ^ { 2 }$ perfectly and choose G optimally for each interference. We compare variants with and without the padding scheme introduced in Section IV-C. Padding the dataset described in Section VI-A results in $N \ = \ 8 9 6$ . To make results comparable, we crop the padded output signals in the time and spectral domains such that $N = 5 1 2$ for further processing. Note that we do not use a smoothing kernel for zeroing. For both variants, we set the CFAR detector’s window size Φ such that the 2Φ covers the entire signal except for the cell under test and the guard cells. The CFAR detector’s window is wrapped around the signal’s edges. The parameters in Table V have been set heuristically. $N _ { \alpha }$ is derived using (15) from an EMDFrFT with $M \ : = \ : 2 5 6$ . We evaluate both variants of our method with $N _ { \alpha } = 1 1 3$ for better comparison, even though $M \ = \ 2 5 6$ does not divide $N ~ = ~ 8 9 6$ for the padded variant as required by the EMDFrFT. Therefore, when evaluating the padded variant, we replace the EMDFrFT with 113 distinct DFrFTs.

2) Method by Chen Et Al. [24]: In Section V-D, we analyzed the conceptual similarities as well as diferences between our approach and [24]. We chose the same parameter values for the CA-CFAR interference detector within [24] as for our LO-CFAR peak classifier, which are listed in Table V. We set the maximum number of iterations per fast-time sequence (labeled M in [24]) to three to match the maximum number of interferers in our dataset. We also evaluate a variant of [24] which includes our padding scheme described in Section IV-C.

![](images/56fec643b9fdfd5a73658c052ec07a41172aee56a76427f3cd3704b7528356f5.jpg)  
Fig. 10. Performance of our proposed method for diferent $N _ { \pmb { \alpha } } .$ . Note that we zoomed into relevant portions of the ECDFs to better resolve close-by curves. (a) MSE. (b) SINR. (c) EVM. (d) TPR. (e) FAR. (f) F1-score.

3) Zeroing: We compare zeroing utilizing an envelope change-point interference detector. We also evaluate an oracle with perfect interference detection that zeroes all samples s[n] where |s<sub>I</sub>|[n] |s<sub>O</sub> + s<sub>N</sub> |[n].

4) Ramp Filtering: We evaluate ramp filtering [9] by applying a median filter to the magnitudes of consecutive range-spectra.

## C. Evaluation Metrics

To gauge the performance of various IM methods, we evaluate their impact on object detections and the reconstruction of interference-free RD-maps.

1) Mean-Squared Error: We use the MSE to compare the interference mitigated RD-map $\tilde { S } _ { \mathrm { R D } }$ to the ground truth $S _ { \mathrm { R D } }$ The MSE is defined as

$$
\mathrm { m s e } = \frac { 1 } { K } \sum _ { K } \left| \tilde { S } _ { \mathrm { R D } } - S _ { \mathrm { R D } } \right| ^ { 2 }\tag{17}
$$

where K is the total number of RD-bins.

2) Signal-to-Interference-Plus-Noise Ratio: We compute the SINR as

$$
\begin{array} { r } { \mathrm { S I N R } = 1 0 \log \frac { \frac { 1 } { N _ { \ O } } \sum _ { \{ r , d \} \in \mathcal { O } } \left| \tilde { S } _ { \mathrm { R D } } [ r , d ] \right| ^ { 2 } } { \frac { 1 } { K - N _ { \ O } } \sum _ { \{ r , d \} \notin \mathcal { O } } \left| \tilde { S } _ { \mathrm { R D } } [ r , d ] \right| ^ { 2 } } } \end{array}\tag{18}
$$

where $\mathcal { O }$ is the set of all ground truth object bin locations $\{ r , d \}$ containing $N _ { \mathcal { O } }$ objects bins. O is aquired by running a CA-CFAR object detector on $S _ { \mathrm { R D } }$

3) Error Vector Magnitude: The EVM describes the average proportion of the error vector to the ground truth object vector

$$
\mathrm { E V M } = \frac { 1 } { N _ { \mathcal { O } } } \sum _ { \{ r , d \} \in \mathcal { O } } \frac { \left| \tilde { S } _ { \mathrm { R D } } [ r , d ] - S _ { \mathrm { R D } } [ r , d ] \right| } { \left| S _ { \mathrm { R D } } [ r , d ] \right| } .\tag{19}
$$

4) False Alarm Rate: The false alarm rate (FAR) of a predicted binary object detection map is computed as

$$
\mathrm { F A R } = \frac { N _ { \mathrm { F P } } } { N _ { \mathrm { F P } } + N _ { \mathrm { T N } } } .\tag{20}
$$

The number of false positives $N _ { \mathrm { F P } }$ and true negatives $N _ { \mathrm { T N } }$ are acquired through a bin-wise comparison of the ground truth to the predicted object detection maps.

5) True Positive Rate: In analogy to the FAR, the TPR is given by

$$
\mathrm { T P R } = \frac { N _ { \mathrm { T P } } } { N _ { \mathrm { T P } } + N _ { \mathrm { F N } } }\tag{21}
$$

where $N _ { \mathrm { T P } }$ is the number of true positives and $N _ { \mathrm { F N } }$ the number of false negatives.

6) F1-Score: The F1-score is a common metric to summarize the overall performance of a binary classifier. It is computed as

$$
F 1 = { \frac { 2 N _ { \mathrm { T P } } } { 2 N _ { \mathrm { T P } } + N _ { \mathrm { F P } } + N _ { \mathrm { F N } } } } .\tag{22}
$$

## A. Performance

As we can see in Fig. 8, our proposed IMfrac performs best across all metrics. Padding generally improves the performance of our method, as interferences are detected more easily and artifacts can be removed after termination of our algorithm. Performance improvements are larger for the oracle variants than for the CFAR-detection-based variants, as the oracle without padding sometimes falsely zeroes a high number of samples if an interference has not been properly compressed. On some metrics, the performances of the oracles are closely matched by the CFAR-based implementations. The method by Chen et al. [24] also outperforms zeroing and ramp filtering by a large margin, which highlights the overall potential of the FrFT for FMCW mutual IM. Furthermore, our padding scheme also improves the performance of [24], as the approximation error of the fast approximate FrFT is smaller when the signal’s energy is confined to the center of the time–frequency plane [25]. We observe the typical efects of zeroing as explained in Section V-A, where zeroing with oracle detection leads to a high TPR, but also a high FAR; an example can be seen in Fig. 7(h). The performance gap between zeroing with oracle and envelope change-point detection highlights the dificulty of designing robust interference detectors in the time domain. Ramp filtering outperforms zeroing with envelope change-point detection in our experiment.

## B. Number of Fractional Angles $N _ { \alpha }$

In this experiment, we evaluate our method for diferent $N _ { \alpha }$ We set $M = \{ 2 5 6 , 1 2 8 , 6 4 , 3 2$ 16} and derive the corresponding $N _ { \alpha } = \{ 1 1 3 , 5 7 , 2 9 , 1 5 , 7 \}$ using (15), while keeping all other <sup>α , , , ,</sup>parameters the same as in Table V. We apply the padding scheme from Section IV-C without a smoothening kernel. The results for $N _ { \alpha } = 1 1 3$ are the same as in Section VII-A and can be seen in Fig. 10. As expected, the performance of the oracles is steadily worsening with decreasing $N _ { \alpha } { \mathrm { ; } }$ ; however, when a CFAR detector is used for interference detection, performance remains roughly constant for $N _ { \alpha } = \{ 1 1 3 , 5 7 , 2 9 \}$ Therefore, for $N = 8 9 6$ , M can be reduced from 896 to 64 while only marginally reducing performance. This corresponds to a reduction of the number of operations for the FFTs in (12) from roughly $7 . 8 7 \cdot 1 0 ^ { 6 }$ for the MDFrFT [1] to $3 . 4 4 \cdot 1 0 ^ { 5 }$ <sup>. .</sup>for the EMDFrFT, i.e., by a factor of approximately 23. For $N _ { \alpha } = \{ 1 5 , 7 \}$ , the performance gap between the oracle and the CFAR interference detector steadily widens; this gap could be narrowed by developing a more elaborate interference detector in future research, so that M can be reduced even further. For decreasing $N _ { \alpha }$ , our method becomes more and more similar to zeroing, which explains its increasingly high FAR. An interfered signal’s EMDFrFT for diferent $N _ { \alpha }$ can be seen in Fig. 9.

## VIII. CONCLUSION AND FUTURE WORK

In this work, we have presented a novel method for FMCW radar mutual IM, which is based on the DFrFT. Our method performs multiple consecutive DFrFTs to detect and null interferences in the fractional domain. We have analyzed the properties of our method, and also provided an implementation optimized for real-time, resource-constrained, and safety-critical applications which makes use of our new EMD-FrFT and the angle-additivity property of the DFrFT. We also proposed a practical method to improve the chirp compression capabilities of the eigendecomposition-based DFrFT by [31], [47], and [48], among others. All of these contributions lead to a simple algorithm which achieves competitive performance across all our considered metrics on an I/Q-modulated dataset. Throughout this article, we have indicated potential future improvements for our method. In future work, we plan comparisons to data-driven approaches such as [52] and [12]. We plan to extend our algorithm to real-valued radar data, where the interferences appear as real-valued LFM chirps. Even though real-valued chirps are not basis functions of the FrFT, the exact same Algorithm 1 can, in principle, be applied to real-valued radar data.

## A. Extension to More Realistic Signal Models

In Section II-B, we have introduced a signal model which neglects multipath components as well as imperfections of real radar systems. More realistic signal models could be evaluated in future research; in this section, we briefly describe how we expect our method to generalize to real-world environments and radar sensors.

Our model could be extended to multipath environments, where instead of an impulse we find the channel’s impulse response in an interference’s optimal fractional domain.

Our algorithm could also be used with nonideal anti-aliasing filters, where the aliased components of the interference chirp may be included in the kernel of the CFAR interference detector.

Another common imperfection of radar systems is phase noise; we expect that phase noise in an interference chirp leads to a widening of the compressed interference after a DFrFT with the optimal fractional angle, which is akin to the spectral regrowth of sinusoids. As long as this widening of the interference peak is not excessive, we conjecture that our method can be applied to interferences corrupted by phase noise.

The dynamic range of real-world radar systems is finite, and strong interferences might saturate the receiver. If we model the receiver as a static nonlinearity which clips at some given input level, an interference saturating the receiver would induce intermodulation products as well as spectral regrowth [53]. The intermodulation products appear as additional LFM chirps with chirp rates depending on the original interferences; therefore, we argue that our method could also mitigate these intermodulation products. Spectral regrowth, on the other hand, widens the spectrum of the interference chirps, hindering optimal compression with the DFrFT. More research is necessary to determine acceptable levels of saturation. An additional strategy could be to replace the LO-CFAR interference detector with a more elaborate detector that operates on the entire bank of DFrFTs S, as the diferent peaks in |S| corresponding to the diferent harmonics always appear in predictable patterns.

## B. Interpolating the Zeroed Signal Components

In our method, we set the compressed interferences to zero; However, as described in Section III, we also unintentionally remove object signal components in the process. Meanwhile, publications such as [4], [54], and [55], among others, propose schemes to interpolate zeroed components using estimates of the object signal; more concretely, they are used as a postprocessing step, typically after time-domain zeroing using some interference detector [3]. Our method could be improved in future research by combining it with such an interpolation scheme. In the case of time-domain interpolation algorithms, however, we would first need to adapt these algorithms to zeroing the fractional Fourier domain. For instance, a wellknown interpolation scheme is IMAT [4], where the previously zeroed time-domain samples are interpolated using object peak detections in the range-spectrum. While IMAT, in its original formulation, iteratively computes inverse and forward DFTs interpolating the signal gaps as object peaks are detected, we can adapt this procedure to our method by simply replacing the DFTs with DFrFTs; we would therefore iterate between the range-spectrum and the fractional domain where zeroing was performed, and generate an interpolation signal which consists of a slice of LFM chirps instead of sinusoids. This approach could even be extended to interpolate interferences that have previously been partly zeroed, such that they are not incomplete anymore. A weakness of IMAT and related methods is that the interpolation’s quality depends on the number of previously zeroed time-domain samples, as object signal estimates are formed from the remainder of the radar signal; however, this portion of the signal is short if the interference is long in the time domain, e.g., if its chirp rate is low. As discussed in Section V-A, the number of zeroed samples is lower and also practically independent of the interference’s chirp rate when using our method. Therefore, we expect this adapted version of IMAT to have better and more constant performance for all possible interference chirp rates compared to its original formulation.

## REFERENCES

[1] J. G. Vargas-Rubio and B. Santhanam, “On the multiangle centered discrete fractional Fourier transform,” IEEE Signal Process. Lett., vol. 12, no. 4, pp. 273–276, Apr. 2005.

[2] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[3] C. Fischer, Untersuchungen Zum Interferenzverhalten Automobiler Radarsensorik. Gottingen, Germany: Cuvillier Verlag, 2016.¨

[4] F. Marvasti et al., “Sparse signal processing using iterative method with adaptive thresholding (IMAT),” in Proc. 19th Int. Conf. Telecommun. (ICT), Apr. 2012, pp. 1–6.

[5] M. Toth, E. Leitinger, and K. Witrisal, “Variational signal separation for automotive radar interference mitigation,” IEEE Trans. Radar Syst., vol. 2, pp. 1007–1026, 2024.

[6] R. Muja, A. Anghel, R. Cacoveanu, and S. Ciochina, “Interference mitigation in FMCW automotive radars using the short-time Fourier transform and L-statistics,” in Proc. IEEE Radar Conf. (RadarConf22), Mar. 2022, pp. 1–6.

[7] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

[8] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in Proc. IEEE 92nd Veh. Technol. Conf. (VTC-Fall), Nov. 2020, pp. 1–5.

[9] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in Proc. IEEE Int. Symp. Circuits Syst. (ISCAS), May 2018, pp. 1–4.

[10] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[11] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceeficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021.

[12] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Complexvalued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in Proc. IEEE Radar Conf. (RadarConf21), May 2021, pp. 1–6.

[13] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Multiantenna radar signal interference mitigation using complex-valued convolutional neural networks,” IEEE Trans. Syst., Man, Cybern., Syst., vol. 55, no. 3, pp. 1997–2008, Mar. 2025.

[14] C. Oswald, M. Toth, P. Meissner, and F. Pernkopf, “Angle-equivariant convolutional neural networks for interference mitigation in automotive radar,” in Proc. 20th Eur. Radar Conf. (EuRAD), Sep. 2023, pp. 135–138.

[15] C. Oswald, M. Toth, P. Meissner, and F. Pernkopf, “End-to-end training of neural networks for automotive radar interference mitigation,” in Proc. IEEE Int. Radar Conf. (RADAR), Nov. 2023, pp. 1–6.

[16] K. Sun, B. Yu, L. Xu, M. Elhajj, and W. Yotto Ochieng, “A novel GNSS anti-interference method using fractional Fourier transform and notch filtering,” IEEE Trans. Instrum. Meas., vol. 73, pp. 1–17, 2024.

[17] A. R. Nafchi, M. Esmaeili, A. Ghasempour, E. Hamke, B. Santhanam, and R. Jordan, “Mitigating the time-varying Doppler shift in highmobility wireless communications using multi-angle centered discrete fractional Fourier transform,” in Proc. IEEE 12th Annu. Ubiquitous Comput., Electron. Mobile Commun. Conf. (UEMCON), Jordan, Dec. 2021, pp. 0607–0612.

[18] Q. Wang, Z. Chen, Q. Zhou, and X. Wu, “Mitigation of radio frequency interference in HFSWR using fractional Fourier transform based filtering algorithms,” IEEE Geosci. Remote Sens. Lett., vol. 18, no. 2, pp. 261–265, Feb. 2021.

[19] Q. Zhou, H. Zheng, X. Wu, X. Yue, Z. Chen, and Q. Wang, “Fractional Fourier transform-based radio frequency interference suppression for high-frequency surface wave radar,” Remote Sens., vol. 12, no. 1, p. 75, Dec. 2019.

[20] Y. Cui and J. Wang, “Wideband LFM interference suppression based on fractional Fourier transform and projection techniques,” Circuits, Syst., Signal Process., vol. 33, no. 2, pp. 613–627, Feb. 2014.

[21] A. Correas-Serrano and M. A. Gonzalez-Huici, “Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2019, pp. 1–4.

[22] A. Maeda-Magalhaes, D. Delbecq, and G. Ferre, “FMCW interference suppression technique in OFDM automotive radar using grid dechirping,” in Proc. IEEE Int. Radar Conf. (RADAR), Nov. 2023, pp. 1–6.

[23] M. Rameez, M. I. Pettersson, and M. Dahl, “Interference compression and mitigation for automotive FMCW radar systems,” IEEE Sensors J., vol. 22, no. 20, pp. 19739–19749, Oct. 2022.

[24] Q. Chen et al., “Interference mitigation for FMCW radar based on filtering in fractional Fourier domain,” IEEE Trans. Aerosp. Electron. Syst., vol. 61, no. 3, pp. 5799–5813, Jun. 2025.

[25] H. M. Ozaktas, O. Arikan, M. A. Kutay, and G. Bozdagt, “Digital computation of the fractional Fourier transform,” IEEE Trans. Signal Process., vol. 44, no. 9, pp. 2141–2150, Sep. 1996.

[26] A. G. Stove, “Linear FMCW radar techniques,” IEE Proc. F (Radar Signal Process.), vol. 139, no. 5, pp. 343–350, 1992.

[27] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical investigation of non-coherent mutual FMCW radar interference,” in Proc. 15th Eur. Radar Conf. (EuRAD), Sep. 2018, pp. 71–74.

[28] B. Boashash, Time-Frequency Signal Analysis and Processing: A Comprehensive Reference. New York, NY, USA: Academic, 2015.

[29] O. Aldimashki and A. Serbes, “Performance of chirp parameter estimation in the fractional Fourier domains and an algorithm for fast chirp-rate estimation,” IEEE Trans. Aerosp. Electron. Syst., vol. 56, no. 5, pp. 3685–3700, Oct. 2020.

[30] S.-C. Pei and J.-J. Ding, “Closed-form discrete fractional and afine Fourier transforms,” IEEE Trans. Signal Process., vol. 48, no. 5, pp. 1338–1353, May 2000.

[31] C. Candan, M. A. Kutay, and H. M. Ozaktas, “The discrete fractional Fourier transform,” IEEE Trans. Signal Process., vol. 48, no. 5, pp. 1329–1337, May 2000.

[32] S.-C. Pei, M.-H. Yeh, and C.-C. Tseng, “Discrete fractional Fourier transform based on orthogonal projections,” IEEE Trans. Signal Process., vol. 47, no. 5, pp. 1335–1348, May 1999.

[33] A. Serbes and L. Durak-Ata, “The discrete fractional Fourier transform based on the DFT matrix,” Signal Process., vol. 91, no. 3, pp. 571–581, Mar. 2011.

[34] J. R. de Oliveira Neto and J. B. Lima, “Discrete fractional Fourier transforms based on closed-form Hermite–Gaussian-like DFT eigenvectors,” IEEE Trans. Signal Process., vol. 65, no. 23, pp. 6171–6184, Dec. 2017.

[35] A. Serbes and L. Durak-Ata, “Eficient computation of DFT commuting matrices by a closed-form infinite order approximation to the second diferentiation matrix,” Signal Process., vol. 91, no. 3, pp. 582–589, Mar. 2011.

[36] X. Su, R. Tao, and X. Kang, “Analysis and comparison of discrete fractional Fourier transforms,” Signal Process., vol. 160, pp. 284–298, Jul. 2019.

[37] A. Gomez-Echavarr´ ´ıa, J. P. Ugarte, and C. Tobon, “The fractional´ Fourier transform as a biomedical signal and image processing tool: A review,” Biocybern. Biomed. Eng., vol. 40, no. 3, pp. 1081–1093, Jul. 2020.

[38] C. Oswald and F. Pernkopf, “On multiangle discrete fractional periodic transforms,” 2025, arXiv:2505.05388.

[39] D. J. Peacock and B. Santhanam, “Comparison of centered discrete fractional Fourier transforms for chirp parameter estimation,” in Proc. IEEE Digit. Signal Process. Signal Process. Educ. Meeting (DSP/SPE), Aug. 2013, pp. 65–68.

[40] K. Hahmann, S. Schneider, and T. Zwick, “Evaluation of probability of interference-related ghost targets in automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2018, pp. 1–4.

[41] A. V. Oppenheim, Discrete-Time Signal Processing. London, U.K.: Pearson, 1999.

[42] J. R. de Oliveira Neto, J. B. Lima, G. J. da Silva, and R. M. Campello de Souza, “Computation of an eigendecomposition-based discrete fractional Fourier transform with reduced arithmetic complexity,” Signal Process., vol. 165, pp. 72–82, Dec. 2019.

[43] D. Majorkowska-Mech and A. Cariow, “A low-complexity approach to computation of the discrete fractional Fourier transform,” Circuits, Syst., Signal Process., vol. 36, no. 10, pp. 4118–4144, Oct. 2017.

[44] B. C. Bispo, J. R. de Oliveira Neto, and J. B. Lima, “Hardware architectures for computing eigendecomposition-based discrete fractional Fourier transforms with reduced arithmetic complexity,” Circuits, Syst., Signal Process., vol. 43, no. 1, pp. 593–614, Jan. 2024.

[45] T. Erseghe and G. Cariolaro, “Eficient DFT architectures based upon symmetries,” IEEE Trans. Signal Process., vol. 54, no. 10, pp. 3829–3838, Oct. 2006.

[46] R. Keshavarz, N. Shariati, and M.-A. Miri, “Real-time discrete fractional Fourier transform using metamaterial coupled lines network,” IEEE Trans. Microw. Theory Techn., vol. 71, no. 8, pp. 3414–3423, Aug. 2023.

[47] B. Santhanam and T. S. Santhanam, “On discrete Gauss–Hermite functions and eigenvectors of the discrete Fourier transform,” Signal Process., vol. 88, no. 11, pp. 2738–2746, Nov. 2008.

[48] S. Clary and D. H. Mugler, “Shifted Fourier matrices and their tridiagonal commutors,” SIAM J. Matrix Anal. Appl., vol. 24, no. 3, pp. 809–821, Jan. 2003.

[49] T. Shimura, M. Umehira, Y. Watanabe, X. Wang, and S. Takeda, “An advanced wideband interference suppression technique using envelope detection and sorting for automotive FMCW radar,” in Proc. IEEE Radar Conf. (RadarConf22), Mar. 2022, pp. 1–6.

[50] M. A. Richards et al., Fundamentals of Radar Signal Processing, vol. 1. New York, NY, USA: McGraw-Hill, 2005.

[51] L. Cohen, Time-Frequency Analysis: Theory and Applications. Upper Saddle River, NJ, USA: Prentice-Hall, 1995.

[52] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 624–629.

[53] S. C. Cripps et al., RF Power Amplifiers for Wireless Communications, vol. 250. Norwood, MA, USA: Artech House, 2006.

[54] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[55] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

Christian Oswald received the M.Sc. (Dipl.-Ing.) degree in information and computer engineering from Graz University of Technology, Graz, Austria, in 2022, where he is currently pursuing the Ph.D. degree with the Signal Processing and Speech Communication Laboratory.

He is a Research Associate with the Signal Processing and Speech Communication Laboratory, Graz University of Technology. His research is focused on robust and explainable artificial intelligence as well as signal processing for automotive radar applications.

Franz Pernkopf (Senior Member, IEEE) received the M.Sc. (Dipl.-Ing.) degree in electrical engineering from Graz University of Technology, Graz, Austria, in 1999, and the Ph.D. degree from the University of Leoben, Leoben, Austria, in 2002.

In 2002, he was awarded the Erwin Schrodinger Fellowship. He was a¨ Research Associate with the University of Washington, Seattle, WA, USA, from 2004 to 2006. From 2010 to 2019, he was an Associate Professor with the Laboratory of Signal Processing and Speech Communication. Since 2019, he has been a Professor of intelligent systems with Graz University of Technology. His research is focused on pattern recognition, machine learning, and computational data analytics with applications in various fields ranging from signal processing to medical data analysis and industrial applications.