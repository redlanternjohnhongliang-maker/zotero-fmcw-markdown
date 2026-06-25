# Variational Signal Separation for Automotive Radar Interference Mitigation

Mate Toth, Erik Leitinger, and Klaus Witrisal

Abstract—Algorithms for mutual interference mitigation and object parameter estimation are a key enabler for automotive applications of frequency-modulated continuous wave (FMCW) radar. In this paper, we introduce a signal separation method to detect and estimate radar object parameters while jointly estimating and successively canceling the interference signal. The underlying signal model poses a challenge, since both the coherent radar echo and the non-coherent interference influenced by individual multipath propagation channels must be considered. Under certain assumptions, the model is described as a superposition of multipath channels weighted by parametric interference chirp envelopes. Inspired by sparse Bayesian learning (SBL), we employ an augmented probabilistic model that uses a hierarchical Gamma-Gaussian prior model for each multipath channel. Based on this, an iterative inference algorithm is derived using the variational expectation-maximization (EM) methodology. The algorithm is statistically evaluated in terms of object parameter estimation accuracy and robustness, indicating that it is fundamentally capable of achieving the Cramer-Rao lower bound (CRLB) with respect to the accuracy of object estimates and it closely follows the radar performance achieved when no interference is present.

Index Terms—line spectral estimation, sparse Bayesian learning, variational expectation-maximization (EM), signal separation, automotive radar, interference.

## I. INTRODUCTION

The growing number of radar-equipped vehicles is expected to cause mutual interference, potentially compromising safetycritical automotive radar applications [1], [2]. As a result, this issue has received significant research attention in the past decade. Large industry research projects have been conducted to analyze interference mitigation methods and strategies for using the automotive radar spectrum [3], [4]. From an academic perspective, the interference problem presents a challenge in signal modeling and processing, making it an interesting area for algorithm design. Early analyses were conducted in [5]–[7], and since then, a significant amount of research has been published on the subject.

## A. State of the Art

Interference modeling efforts can be categorized into scenario-level and signal-level models. Works in the former category characterize the probability of interference occurring and the received interference power, whereas the latter models the specific form of interference in the received radar signal. Scenario-level modeling approaches include analyses via stochastic geometry [8], graph theory [9] as well as other extensive numerical simulation frameworks [10]. Signal-level models have been developed for different modulation schemes, including the most commonly used frequency-modulated continuous wave (FMCW) [11], [12] as well as phase-modulated continuous wave (PMCW) [13] and orthogonal frequency division multiplexing (OFDM) [14] radars. Experimental evaluations can be found e.g. in [15], [16]. Recent modeling efforts also consider the interference propagation channel [17], [18]. This paper focuses on the mutual interference of FMCW radars, taking into account the interference channel.

Approaches to mitigate interference include avoidance strategies using cognitive radar principles [19], [20] as well as exploiting vehicle-to-vehicle communication [21], [22]. In terms of signal processing algorithms to cancel the interference in the receiver, a vast number of algorithms have been proposed. As mutual FMCW interference is commonly of a short duration as compared to the total number of received samples, zeroing, optionally followed by interpolating the zeroed samples, has been discussed first in [6]. This method typically necessitates a separate prior interference detection step, e.g. [23]–[26]. Interpolation approaches include autoregressive modeling [27], time-frequency interpolation [28] and sparsity-based algorithms [29]–[31]. Alternative approaches to interpolation include spatial beamforming [32], [33], adaptive noise cancellers [34], [35], time-frequency [36], [37] and nonlinear filtering [38], [39]. Denoising based on signal decomposition and thresholding has been proposed in e.g. [40]. Additionally, many works are making use of deep learning [41] to detect [42] and mitigate interference [43]–[45].

If the interference signal is estimated, it may be canceled completely by subtraction. Proposed methods for this include [46]–[48]. However, if the useful radar return itself, here termed the object signal, is also explicitly considered in the estimation, the problem can be cast as signal separation. This problem is generally ill-posed, but can be solved by assuming that the object and interference signal components are represented by a sparse basis in different signal bases. In [49], the author applied the framework of morphological component analysis (MCA) [50] modeling the interference and object signals as being sparse in the discrete Fourier and discrete short-time Fourier domains, respectively. This assumption allows for the joint sparse recovery of the signals to be written as a modified dual basis pursuit optimization problem [51], for which an iterative algorithm was proposed. Similar algorithms can be found in [52]–[55].

## B. Contributions and Notations

Although the existing literature is extensive, we identify the following open topics for which our work provides novel insights. Previously proposed algorithms are applied as $p r e \_$ processing in a conventional range-Doppler processing chain. This approach is practical, but has inherent limitations. In general, the goal of radar sensing is to provide estimates of object parameters, which is equivalent to estimating the parameters of a multipath propagation channel containing static (such as buildings, traffics signs or trees) and moving objects (such as vehicles, bicycle or pedestrians). Note that parametric channel models typically represent multipath propagation as a linear superposition of weighted Dirac delta distributions - or spectral lines - with distinct supports in the underlying dispersion domain (range, angle of arrival, angle of departure, Doppler frequency, and combinations thereof). Therefore, estimating multipath parameters can be cast as a line spectral estimation (LSE) problem [56], for which sparse Bayesian learning (SBL) [57], [58] and related algorithms have been developed. An SBL-type method has been previously proposed as a preprocessing step to interpolate the received signal after interference zeroing [30], as referenced in Section I-A. Our proposed algorithm’s design and its aims are however distinct, as detailed in the remainder of this paper.

To achieve robust inference performance, it is necessary to consider the entire problem of parameter estimation under the influence of interfering signals. Previous methods are also often based on heuristics or require the prior setting of certain algorithm parameters. This makes it necessary to manually fine-tune the range-Doppler processing chain and makes it difficult to give performance guarantees. Our proposed algorithm is derived within a rigorous theoretical framework. Specific contributions are the following:

• We develop a new probabilistic signal model for the problem of mutual FMCW radar interference. The model incorporates the multipath propagation as line spectra for both the coherently received radar echo and the interference.

• We propose a novel inference algorithm inspired by SBL [58]–[60] for LSE that is able to infer the superposition of sparse line spectra. The algorithm is based on the variational EM approach. It jointly estimates the objects’ range-Doppler parameters with the parameters of the interference signal and multipath channel. This makes it explicitly robust to mutual interference. Note that the object parameters are estimated super-resolved in a gridless manner [56].

• We quantitatively show near-optimal multi-target detection and parameter estimation performance by statistically evaluating the proposed method in simulation, comparing it to the Cramer-Rao lower bound (CRLB) as well as to the interference-free case. We also showcase that the algorithm significantly outperforms a few established signal preprocessing methods for interference mitigation.

• We include investigations on difficult-to-handle scenarios of model mismatch and poor signal separability. We point out the relative resilience of the algorithm to these challenges, and provide an initial proof of concept based on measurement data.

Notation: The complex conjugate of the variable c is denoted by $c ^ { * }$ . Bold lowercase letters denote column vectors and bold uppercase letters denote matrices, respectively. For the vector v, v is its Euclidean norm; Diag(v) constructs a diagonal matrix from v. The matrix transpose of M is $M ^ { \mathrm { T } }$ $M ^ { \breve { \mathrm { H } } }$ is the Hermitian; $\mathrm { t r } ( M )$ is the trace of the matrix, and $\vert M \vert$ denotes the determinant. The notation $M [ m , n ]$ refers to the element $( m , n )$ of the matrix; I denotes the identity matrix. For the random variable x, $p ( { \pmb x } ) = \mathrm { C N } ( { \pmb x } | { \pmb \mu } , C )$ denotes a complex Gaussian probability density function (PDF) with mean $\pmb { \mu }$ and covariance matrix $C ; \ p ( x ) \ = \ \mathrm { G a } ( x | a , b )$ is a Gamma PDF with shape a and rate parameters b. The expectation of the probability distribution $p ( x )$ with respect to $q ( x )$ (denoted in shorthand as $p$ and $q )$ is written as $\begin{array} { r } { { \left. p \right. } _ { q } = \int p ( x ) q ( x ) \mathrm { d } x } \end{array}$ . The vertical bar denotes a conditional PDF $p ( { \pmb x } | { \pmb z } )$ ; the semicolon a parametrized PDF $p ( { \pmb x } ; { \pmb \theta } )$ $\tilde { \pmb { \theta } }$ denotes the vector containing the “true” parameters of the generative model and $\hat { \pmb { \theta } }$ denotes an estimate of the parameter vector θ.

## II. SIGNAL MODEL

## A. FMCW Radar under Interference

The victim radar transmits a transmit signal $x ( t )$ in an environment containing $M _ { \mathrm { I } }$ interferers with respective transmit signals ${ x _ { \mathrm { I } , i } ( t ) , i \in [ 0 , M _ { \mathrm { I } } - 1 ] }$ . The corresponding received intermediate frequency (IF) signal $r ( n , p )$ , where $n \in [ 0 , N -$ 1] denotes the fast-time index with sampling time $\mathrm { { T _ { s } } }$ and $p \in [ 0 , P - 1 ]$ is the slow-time ramp index<sup>1</sup>, is given by

$$
r ( t ^ { \prime } = n \mathrm { T } _ { \mathrm { s } } , p ) = r _ { \mathrm { O } } ( n , p ) + \sum _ { i = 0 } ^ { M _ { \mathrm { I } } - 1 } r _ { \mathrm { I } , i } ( n , p ) + \eta ( n , p ) .\tag{1}
$$

The first term $r _ { \mathrm { O } } ( n , p )$ refers to the coherently received radar echo, termed the object signal. The non-coherent received interference signal from the i-th interferer is denoted by $r _ { \mathrm { I } , i } ( \boldsymbol { n } , \boldsymbol { p } )$ . Finally, $\eta ( n , p )$ represents additive white Gaussian noise (AWGN) with precision (inverse variance) $\tilde { \lambda } .$ Fig. 1a illustrates an example interference scenario where $M _ { \mathrm { I } } = 1$ and Fig. 1e shows example signals for a single ramp.

The victim radar, a monostatic FMCW radar, transmits a sequence of linearly modulated chirp signals (ramps)

$$
x ( t ) = A \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } ) u ( t - T _ { \mathrm { p } } p ; f _ { 0 } , k )\tag{2}
$$

with

$$
\bar { x } ( t ; T _ { \mathrm { s w } } ) = \left\{ \begin{array} { l l } { 1 } & { \mathrm { f o r ~ } 0 \leq t \leq T _ { \mathrm { s w } } } \\ { 0 } & { \mathrm { o t h e r w i s e } } \end{array} \right.\tag{3}
$$

$$
u ( t ; f _ { 0 } , k ) = \exp \bigl ( \mathrm { j } ( 2 \pi f _ { 0 } t + \pi k t ^ { 2 } ) \bigr )\tag{4}
$$

where we defined the parametrized rectangular function template $\bar { x } ( t ; T _ { \mathrm { s w } } )$ and the chirp $u ( t ; f _ { 0 } , k )$ . A is some complex transmit amplitude, P is the number of chirps, $f _ { 0 }$ is the chirp start frequency, k is the chirp slope and $T _ { \mathrm { p } }$ is the pulse duration which consists of the actual transmit chirp duration $T _ { \mathrm { s w } }$ plus an additional idle time.<sup>2</sup>

![](images/94b16a932795a7dce333199c1d37b0b5ffa378cb2a6b732ef2fdedfb5ab7eb89.jpg)

![](images/fdfbcac1fc8e4ee11d30a14f62e87a7decdf6f9a7759dc0981d7e0ba5e66ba58.jpg)

![](images/e66cfb2337a6edc86c73e65237612cedc610c7dc9ddfe98cc633e4411aef89ff.jpg)  
Fig. 1. Illustrations of the principles and signal modeling for a mutual automotive FMCW radar interference scenario. (a) A critical automotive radar scenari with a pedestrian to be detected and an interfering vehicle on the opposite lane. (b) Abstracted block diagram representing the applied signal model. (c)-(d) Time-frequency plots of the involved signals. (e) Plot of the received signal components from an interfered ramp.

The transmit signal $x ( t )$ in (2) propagates through a multipath channel, yielding a superposition of reflected signals that are coherently demodulated by multiplication with $x ^ { * } ( t )$ , and filtered by the receiver anti-aliasing filter (AAF) $G ( f )$ . This is indicated in Fig. 1b starting at the rectangle symbol. The according received object signal $r _ { \mathrm { O } } ( t ^ { \prime } , p )$ is given by

$$
\begin{array} { l } { { \displaystyle r _ { \mathrm { O } } ( t ^ { \prime } , p ) \approx H _ { \mathrm { O } } \bigl ( f _ { 0 } + k t ^ { \prime } , T _ { \mathrm { p } } p \bigr ) } } \\ { { \displaystyle \qquad = \sum _ { l = 0 } ^ { \tilde { L } - 1 } \tilde { \alpha } _ { l } \exp \left( - \mathrm { j } 2 \pi \bigl ( f _ { 0 } + k t ^ { \prime } \bigr ) \tilde { \tau } _ { l } \right) \exp \left( - \mathrm { j } 2 \pi \tilde { \nu } _ { l } T _ { \mathrm { p } } p \right) } } \end{array}\tag{5}
$$

with $H _ { \mathrm { O } } ( f , t )$ being the frequency-selective time-variant channel transfer function of the object channel made up of $\tilde { L }$ components<sup>3</sup> with respective amplitudes $\tilde { \alpha } _ { l } .$ . A detailed derivation of (5) can be found in Appendix A. An illustration of a single object component in the time-frequency plane can also be seen in Fig. 1c. The fast-time dimension with $t ^ { \prime } ~ = ~ t - T _ { \mathrm { p } } p ~ \in ~ ( 0 , T _ { \mathrm { s w } } ) \forall p$ corresponds to the beat frequencies or analogously the delays $\tilde { \tau } _ { l }$ proportional to the distances of the object components. The slow-time dimension with $p \in [ 0 , P - 1 ]$ corresponds to the Doppler frequencies ${ \tilde { \nu } } _ { l }$ proportional to object velocities. Sampling leads to the discretized fast-time domain with $t ^ { \prime } = n \mathrm { T } _ { \mathrm { s } }$

The transmit signal of the i-th interferer is given by

$$
\begin{array} { r } { x _ { \mathrm { I } , i } ( t ) = A _ { \mathrm { I } , i } \displaystyle \sum _ { p _ { \mathrm { I } } = 0 } ^ { P _ { \mathrm { I } , i } - 1 } \bar { x } ( t - \bar { T } _ { i } - T _ { \mathrm { p I } , i } p _ { \mathrm { I } } ; T _ { \mathrm { s w I } , i } ) } \\ { \times u ( t - T _ { \mathrm { p I } , i } p _ { \mathrm { I } } ; f _ { \mathrm { I } , i } , k _ { \mathrm { I } , i } ) } \end{array}\tag{6}
$$

where $\bar { T _ { i } }$ is some time offset between victim and interferer transmit sequences and other parameters are analogous to (2). Each interferer transmit signal propagates through a multipath channel. Within our formulation, considerations for this interference channel are analogous to the object channel. However, due to non-coherent demodulation the interferer transmit chirp sequence does not vanish, and the effect of the AAF cannot be neglected. The model is represented in Fig. 1b starting at the triangle symbol, and a time-frequency schematic is found in Fig. 1d. The result reads

$$
\begin{array} { r } { r _ { \mathrm { I } , i } ( t ^ { \prime } , p ) \approx \displaystyle \sum _ { p _ { \mathrm { I } } = 0 } ^ { P _ { \mathrm { I } , i } - 1 } \bar { u } _ { \mathrm { p I } , i } ( t ^ { \prime } , p ) H _ { \mathrm { I } , i } ( \bar { f } _ { \mathrm { I } , i } + k _ { \mathrm { I } , i } t ^ { \prime } , T _ { \mathrm { p I } , i } p _ { \mathrm { I } } ) } \\ { \times \bar { G } ( \bar { \Delta } f _ { 0 , i } + \Delta k _ { i } t ^ { \prime } ) } \end{array}\tag{7}
$$

where $\bar { u } _ { \mathrm { p I } , i } ( t ^ { \prime } , p )$ is the noncoherently demodulated interferer transmit chirp, and $H _ { \mathrm { I } , i } ( f , t )$ and $\bar { G } ( f )$ denote the interference channel and a modified AAF transfer function, respectively. For derivation details, see Appendix A.

## B. Inference Problem Statement

The objective is to jointly estimate the object parameters, including the number of objects (see (5)), as well as the interfering signal parameters and the interfering channel (see

(7)). Using the assumptions given in Appendix A, the generic model in (1) can be rewritten as

$$
\begin{array} { r l r } {  { r ( n , p ) = \sum _ { l = 0 } ^ { \tilde { L } - 1 } \tilde { \alpha } _ { l } \exp ( - \mathrm { j } 2 \pi \tilde { \phi } _ { l } \mathrm { T } _ { \mathrm { s } } n ) \exp ( - \mathrm { j } 2 \pi \tilde { \nu } _ { l } T _ { \mathrm { p } } p ) } } \\ & { } & { + \ u ( \mathrm { T } _ { \mathrm { s } } n ; \Delta \tilde { f } _ { 0 } ^ { ( p ) } , \Delta \tilde { k } ^ { ( p ) } ) \bar { G } ( \Delta \tilde { f } _ { 0 } ^ { ( p ) } + \Delta \tilde { k } ^ { ( p ) } \mathrm { T } _ { \mathrm { s } } n ) } \\ & { } & { \times \sum _ { k = 0 } ^ { \tilde { K } ^ { ( p ) } - 1 } \tilde { \beta } _ { k } ^ { ( p ) } \exp ( - \mathrm { j } 2 \pi \tilde { \vartheta } _ { k } ^ { ( p ) } \mathrm { T } _ { \mathrm { s } } n ) + \eta ( n , p ) . \quad } \end{array}\tag{8}
$$

The object signal described in (5) is simplified, noting that the object channel component beat frequency is equal to $\tilde { \phi } \ = \ k \tilde { \tau }$ The interference signal is recast with separate parameters for each ramp $p .$ For each ramp $p ,$ the delay-only interference channel is assumed to consist of $\tilde { K } ^ { ( p ) }$ components with respective amplitudes $\tilde { \beta } ^ { ( p ) }$ and beat frequencies $\tilde { \vartheta } ^ { ( p ) }$ Note that (8) constitutes a superposition of “source signals”, each represented by a linear combination of a limited number of components, corrupted by AWGN. Each of these source signals is traditionally referred to as a line spectrum. Inferring the underlying model parameters constitutes an instance of a LSE problem. The inference model in accordance to (8) is given as

$$
r = \Phi ( \zeta ) \alpha + U ( \theta ) \Psi ( \vartheta ) \beta + \eta\tag{9}
$$

where the vector $\pmb { r } ~ \in ~ \mathbb { C } ^ { P N \times 1 }$ is constructed from stacking the samples of $r ( p , n )$ and $p ( \pmb { \eta } ) \ = \ \mathrm { C N } ( \pmb { \eta } | 0 , \lambda ^ { - 1 } \pmb { I } )$ . This is an extension of the well-known model from compressed sensing [51] and also described for MCA [50]. $\Phi ( \zeta ) = $ $\left[ \phi ( \zeta _ { 0 } ) \ \cdot \ \cdot \ \phi ( \zeta _ { L - 1 } ) \right]$ is an $M \times L$ dictionary matrix with $M \leq L$ , typically $M \ll L$ . Note that the non-linear parameters in $\zeta ,$ which define the dictionary basis vectors, may be fixed on-grid or considered unknown and adaptively estimated, referred to as grid-less from here on.

The object signal dictionary $\Phi ( \zeta )$ consists of the basis vectors

$$
\begin{array} { r } { \phi ( \zeta _ { l } = [ \varphi _ { l } \mathrm { T _ { s } } ~ \nu _ { l } T _ { \mathrm { p } } ] ) = \displaystyle \frac { 1 } { \sqrt { P N } } ( \exp { \left( - \mathrm { j } 2 \pi \nu _ { k } T _ { \mathrm { p } } p \right) } } \\ { \otimes \exp { \left( - \mathrm { j } 2 \pi \varphi _ { l } \mathrm { T _ { s } } n \right) } ) } \end{array}\tag{10}
$$

where $\otimes$ denotes the Kronecker product. We estimate the normalized beat frequencies $\varphi _ { l } \mathrm { T _ { s } } \in [ - 1 / 2 , 1 / 2 )$ and normalized Doppler frequencies $\nu _ { l } T _ { \mathrm { p } } \in [ - 1 / 2 , 1 / 2 )$

As the interference $U ( \theta ) \Psi ( \vartheta ) \beta$ is modeled for every p separately, $U ( \pmb \theta ) \in \mathbb { C } ^ { P N \times P N }$ and $\Psi ( \pmb { \vartheta } ) \in \mathbb { C } ^ { P N \times P K }$ with $\pmb { \theta } ^ { - } = \ [ \pmb { \theta } ^ { 0 } \ \cdot \ \cdot \ \cdot \ \pmb { \theta } ^ { P - 1 } ]$ and $\pmb { \vartheta } ~ = ~ [ \pmb { \vartheta } ^ { 0 } ~ \cdot ~ \cdot ~ \pmb { \vartheta } ^ { P - 1 } ]$ are blockdiagonal matrices. I.e.,

$$
U ( \pmb \theta ) = \left[ \begin{array} { c c c c } { { U ( \pmb \theta ^ { ( p = 0 ) } ) } } & { { } } & { { } } & { { \bf 0 } } \\ { { } } & { { . . } } & { { } } & { { } } \\ { { { \bf 0 } } } & { { } } & { { } } & { { U ( \pmb \theta ^ { ( P - 1 ) } ) } } \end{array} \right]\tag{11}
$$

with $\pmb { \theta } ^ { ( p ) } = [ \Delta f _ { 0 } ^ { ( p ) } \Delta k ^ { ( p ) } ]$ and

$$
\begin{array} { r } { U ( \theta ^ { ( p ) } ) = \mathrm { D i a g } \big ( u ( \mathrm { T } _ { \mathrm { s } } { \pmb n } ; \Delta f _ { 0 } ^ { ( p ) } , \Delta k ^ { ( p ) } ) \qquad } \\ { \times \bar { G } ( \Delta f _ { 0 } ^ { ( p ) } + \Delta k ^ { ( p ) } \mathrm { T } _ { \mathrm { s } } { \pmb n } ) \big ) } \end{array}\tag{12}
$$

is an $N \times N$ diagonal matrix that contains the effect of the non-coherent demodulation and the AAF. The channel dictionary $\Psi ( \vartheta )$ is constructed analogously from blocks $\Psi ( \vartheta ^ { ( p ) } )$ of size $N \times K .$ , and on-grid basis vectors $\psi ( \vartheta _ { k } ) =$ $( 1 / \sqrt { N } ) \exp ( - \mathrm { j } 2 \pi \vartheta _ { k } \mathrm { T } _ { \mathrm { s } } \pmb { n } )$ , where $K \geq N$ is the chosen size of the grid. As the basis vectors are fixed, we do not write out the parameters $\vartheta$ in the sequel.

The ill-posed problem of estimating the weights α and $\beta$ and the according parameters $\zeta$ and θ may be solvable under the assumption of sparsity, stemming from $\tilde { L }$ and $\tilde { K }$ being small in (8). That is, we have some optimization problem of the form

$$
\begin{array} { r } { \hat { \alpha } , \hat { \beta } , \hat { \zeta } , \hat { \theta } = \underset { \alpha , \beta , \zeta , \theta } { \arg \operatorname* { m i n } } \left\| r - \Phi ( \zeta ) \alpha - U ( \theta ) \Psi \beta \right\| ^ { 2 } \quad } \\ { - f ( \alpha , \beta , \zeta , \theta ) \quad } \end{array}\tag{13}
$$

with $f ( \alpha , \beta , \zeta , \theta )$ being a sparsity-inducing penalty function. For a single-source model, cost functions of this form and computationally feasible solution algorithms can be derived in a probabilistic framework [61]. In particular, SBL [58] has been developed for LSE. Variational formulations [62] of SBL have been further developed for on-grid [59], as well as grid-less models [60], [63] that enable super-resolution estimation. The SBL-inspired framework is flexible, lending itself to extensions such as structured line spectra [64] and dense multipath channel models [56]. Our proposed algorithm extends the concept to a superposition of line spectra from different source signals.

## C. Probabilistic Modeling

Our probabilistic model has the weights α and $\beta$ and the noise sensitivity λ as latent variables. We apply a Gamma-Gaussian hierarchical model introducing the additional variables $\gamma _ { \alpha }$ and $\gamma _ { \beta }$ , which leads to a sparse estimate [61]. The non-linear parameters $\zeta$ and $\pmb \theta$ are considered as unknown parameters. Hence, the joint PDF reads

$$
\begin{array} { r l } & { p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb { \theta } ) } \\ & { \qquad = p ( r | \alpha , \beta , \lambda ; \zeta , \pmb { \theta } ) p ( \pmb { \alpha } | \gamma _ { \alpha } ) p ( \gamma _ { \alpha } ) } \\ & { \qquad \quad \times p ( \beta | \gamma _ { \beta } ) p ( \gamma _ { \beta } ) p ( \lambda ) } \end{array}\tag{14}
$$

The explicit forms of the terms in (14) are

$$
\begin{array} { l } { { \displaystyle p ( { \pmb r } | { \pmb \alpha } , { \pmb \beta } , \lambda ; \zeta , { \pmb \theta } ) = \mathrm { \bf C N } ( { \pmb r } | \Phi ( \zeta ) { \pmb \alpha } + { \pmb U } ( { \pmb \theta } ) \Psi { \pmb \beta } , \lambda ^ { - 1 } { \pmb I } ) } \ ~ } \\ { { \displaystyle p ( { \pmb \alpha } | \gamma _ { \alpha } ) p ( \gamma _ { \alpha } ) = \prod _ { l } \mathrm { \bf C N } ( \alpha _ { l } | 0 , \gamma _ { \alpha , l } ^ { - 1 } ) } \ ~ } \\ { { \displaystyle ~ \qquad \times \mathbf { G a } ( \gamma _ { \alpha , l } | a _ { 0 } , b _ { 0 } ) } \ ~ } \end{array}\tag{15}
$$

$$
p ( \beta | \gamma _ { \beta } ) p ( \gamma _ { \beta } ) = \prod _ { p } \prod _ { k } \mathbf { C } \mathbf { N } ( \beta _ { k } ^ { ( p ) } | 0 , \gamma _ { \beta , k } ^ { - 1 } ^ { ( p ) } )\tag{16}
$$

$$
\times \ : \mathrm { G a } ( \gamma _ { \beta , k } ^ { ( p ) } | c _ { 0 } , d _ { 0 } )
$$

$$
p ( \lambda ) = \mathbf { G a } ( \lambda | e _ { 0 } , f _ { 0 } ) .\tag{17}
$$

(18)

The likelihood function $p ( r | \alpha , \beta , \lambda ; \zeta , \pmb \theta )$ is described by a Gaussian distribution due to the AWGN assumption in (8). The weights α and $\beta$ are modeled as conditionally independent zero-mean Gaussian-distributed with individual precisions governed respectively by Gamma-distributed hyperparameters $\gamma _ { \alpha }$ and $\gamma _ { \beta }$ [58]. The Gamma distribution is the conjugate prior for the precision of a Gaussian [65] and is known to promote sparsity [61]. Consequently, the number of components, $\hat { K }$ and $\hat { L } ,$ can be indirectly estimated by inferring the parameters, $\gamma _ { \alpha }$ and $\gamma _ { \beta }$ . The prior PDF of the noise precision λ is also assumed to be Gamma distributed.

## III. INFERENCE ALGORITHM

## A. Variational Formulation

Directly solving the high-dimensional non-linear estimation problem of (13) by statistical inference on the probabilistic model of (14) is computationally infeasible. Therefore, we resort to the variational EM solution [62] to iteratively determine all marginal PDFs of the latent variables and maximum likelihood (ML) estimates of the unknown parameters.

Denoting the inferred proxy posterior distribution of the latent variables as $q ( \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda )$ , the EM framework iteratively maximizes the functional

$$
\begin{array} { r l } & { \mathcal { L } ( q ( \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ) ) } \\ & { \quad = \left. \log \frac { p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb { \theta } ) } { q ( \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ) } \right. _ { q ( \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ) } } \end{array}\tag{19}
$$

termed the evidence lower bound (ELBO).

For fixed parameter estimates $\hat { \zeta }$ and $\hat { \pmb \theta } ,$ the ELBO is maximized if $q$ is equal to the joint posterior PDF. As this posterior distribution is intractable, we first constrain the form of $q$ and maximize the ELBO under those constraints to obtain a tractable variational approximation. In line with variational SBL [59], [60], we use the structured mean-field approach [62]

$$
\begin{array} { l } { { \displaystyle q ( \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb { \theta } ) = q ( \alpha ) \prod _ { l } q ( \gamma _ { \alpha , l } ) } } \\ { { \displaystyle ~ \times q ( \beta ) \prod _ { k } q ( \gamma _ { \beta , k } ) q ( \lambda ) . } } \end{array}\tag{20}
$$

I.e., groups of variables are constrained to factorize in the PDF leading to a set of factors $\begin{array} { r } { \mathcal { Q } , q = \prod _ { \mathcal { Q } } q _ { i } } \end{array}$ , with $q _ { i }$ being the i-th proxy distribution. To be noted is that our model does not factorize elements of the weight vectors α and $\beta ,$ hence posterior correlations between these elements are taken into account. However, the proxy PDFs $q ( \alpha ) q ( \beta ) \neq q ( \alpha , \beta )$ , so that different source signals do in fact factorize, which is a simplifying assumption.<sup>4</sup>

It can be shown that the log-distribution of the i-th factor $q _ { i } ,$ when every other variable and parameter is fixed, is computed by

$$
\log q _ { i } = \left. \log p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \hat { \zeta } , \hat { \pmb \theta } ) \right. _ { \bar { q } _ { i } } + ~ \mathrm { c o n s t } .\tag{21}
$$

where ${ \bar { q } } _ { i }$ is shorthand notation for “proxy PDF of every factor except for the $- i \mathrm { \hbar } ^ { \mathrm { * } }$ . Hence, we obtain a set of interdependent implicit equations that are solved by iteratively updating the inferred PDFs. As long as the ELBO is increased at every step, the ordering of updates is in principle arbitrary. In practice though, certain update schemes are used to improve the convergence properties of the algorithm. In the proposed algorithm, we only directly use (21) for the noise precision $q _ { \lambda }$ . The proxies of the weights $q _ { \alpha }$ and $q _ { \beta }$ and the according unknown parameters $\zeta$ and $\pmb { \theta }$ are updated jointly [63], which is described in Section III-B. For the weight precision hyperparameter distributions $q _ { \gamma }$ the fast update scheme [59] is used, discussed in Section III-C. The complete resulting scheme is sketched as pseudo-code in Algorithm 1, making use of Algorithms 2-4 as subroutines. The details are discussed in the sequel.

## B. Estimation of Unknown Parameters

In the typical variational EM approach, the updates of unknown parameters are derived with the estimates of the proxy PDFs fixed [62]. However, in our application estimates of the object channel parameters $\hat { \zeta }$ are strongly tied to the inferred weight proxy PDF $q _ { \alpha } .$ Similarly, the estimation of interference chirp parameters ${ \hat { \pmb { \theta } } } ^ { ( p ) }$ at ramp $p$ strongly depends on the respective channel weights PDF $\bar { q } _ { \beta } ^ { ( p ) }$ . Term-wise optimization of the ELBO therefore leads to slower convergence as well as the algorithm being more prone to reach local optima. To mitigate this, the ELBO is maximized jointly for $\hat { \zeta }$ and $q _ { \alpha }$ as well as $\hat { \pmb { \theta } } ^ { ( p ) }$ and $q _ { \beta } ^ { ( p ) }$ for all $p .$ Rewriting (19), this yields the same update equations as (21) for the resulting proxy PDFs. For the parameters, however, we obtain

$$
\begin{array} { r l } & { \hat { \pmb { \theta } } ^ { ( p ) } = \underset { \pmb { \theta } ^ { ( p ) } } { \arg \operatorname* { m a x } } } \\ & { \quad ~ \displaystyle \int \exp \left. \log p ( \pmb { r } , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \hat { \zeta } , \hat { \pmb { \theta } } ) \right. _ { \bar { q } _ { \beta } ^ { ( p ) } } \mathrm { d } \beta ^ { ( p ) } } \end{array}\tag{22}
$$

for the chirp parameters ${ \hat { \pmb { \theta } } } ^ { ( p ) }$ . The result for the object channel dispersion parameter estimates $\hat { \zeta }$ is analogous, where estimates for the individual components $\hat { \zeta } _ { l }$ can be computed separately [63], [66] for each spectral line l. More details on the derivation are found in Appendix B.

## C. Fast Component Precision Update and Thresholding

In [59] it has been shown for variational SBL that with the other variables fixed, the estimates of the component precision hyper-parameters “at infinity” can be derived analytically, yielding a test for component convergence. Hence, at every iteration the dictionary may be adaptively pruned of divergent components, or possibly new components may be added. With this, algorithm convergence is much accelerated. Crucially, it can be seen that for our proposed extended model, the update equations for the factors corresponding to each source signal are identical to the single-source case except with r exchanged by the respective “residuals” $\hat { \pmb { r } } _ { \alpha }$ and $\hat { \pmb { r } } _ { \beta }$ . This means that the formulations of [59], [60] can be followed; Appendix B contains more details.

Using the estimates of the object signal parameters $\hat { \Phi } ,$ $\hat { \alpha } ,$ and $\hat { \gamma } _ { \alpha }$ , the update equation, the pruning of existing components, and the addition of new potential components (see Algorithm 4) are based on

$$
\rho _ { l } = \big ( \hat { \lambda } \hat { \phi } _ { l } ^ { \mathrm { H } } \hat { \phi } _ { l } - \hat { \lambda } ^ { 2 } \hat { \phi } _ { l } ^ { \mathrm { H } } \hat { \Phi } _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \hat { \Phi } _ { \bar { l } } ^ { \mathrm { H } } \hat { \phi } _ { l } \big ) ^ { - 1 }
$$

$$
\omega _ { l } ^ { 2 } = \big \lvert \big ( \hat { \lambda } \rho _ { l } \hat { \phi } _ { l } ^ { \mathrm { H } } \hat { \pmb { r } } _ { \alpha } - \hat { \lambda } ^ { 2 } \rho _ { l } \hat { \phi } _ { l } ^ { \mathrm { H } } \hat { \Phi } _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \hat { \Phi } _ { \bar { l } } ^ { \mathrm { H } } \hat { \pmb { r } } _ { \alpha } \big ) \big \rvert ^ { 2 } .\tag{23}
$$

(24)

The notation of the subscript l means taking the l-th element or column corresponding to that component, and <sup>¯</sup>l denotes the vector or matrix with said element removed or computed as if it were removed. Existing components or new components are kept if and only if $\rho _ { l } / \bar { \omega _ { l } ^ { 2 } } > \dot { T }$ with $T = 1$ , where T denotes a threshold and $\omega _ { l } ^ { 2 } / \rho _ { l } - 1$ can be interpreted as an estimated component signal-to-noise ratio (SNR). Note that the original convergence test threshold given by $T = 1$ leads to positive bias in the number of estimated components [56], [59]. In [56], [67], the authors propose an adaptation of the threshold T for grid-less SBL-type methods based on extreme value analysis. Similar update equations are found for the interference parameters $\hat { \pmb { \theta } } ^ { ( \bar { p } ) } , \hat { \pmb { \Psi } } ^ { ( p ) } , \hat { \pmb { \beta } } ^ { ( p ) }$ , and $\hat { \gamma } _ { \beta } ^ { \left( p \right) }$ for all $p$ (see Algorithm 2).

## D. Algorithm Implementation

We have now derived structured mean-field variational EM update steps for inference of our model. As mentioned, these steps are interdependent and therefore to be applied iteratively. Explicit forms of the update equations are listed in Appendix B. The algorithm converges to an optimum of the ELBO corresponding to an approximate solution of our signal separation problem. However, it does not necessarily converge to the global optimum, nor is any rate of convergence guaranteed. In addition to the specific update schemes presented previously, the overall scheduling of steps as well as the initialization significantly influence the behavior of the algorithm.

Algorithm 1 Variational Signal Separation (Main)   
Require: Received signal $\mathbf { \nabla } r ;$ thresholds $\overline { { T _ { \alpha } , T _ { \beta } } }$   
▷ Bottom-up dictionary initialization:   
$\hat { \Phi }  [ ] , \hat { \gamma } _ { \alpha }  [ ] , \hat { \alpha }  [ ] , \hat { C } _ { \alpha }  [ ]$   
$\hat { \Psi } \gets \bar { [ ] } , \hat { \gamma } _ { \beta } \gets \bar { [ ] } , \hat { \beta } \gets \bar { [ ] } , \hat { C } _ { \beta } \gets \bar { [ ] }$   
▷ Noise precision initialization:   
$\hat { \lambda }  ( 2 ( N P - 1 ) ) / \| r \| ^ { 2 }$   
repeat ▷ Main iteration   
▷ Update interference estimate:   
for all $p$ do ▷ per-ramp update   
${ \hat { \pmb { \theta } } } ^ { ( p ) } \gets$ from (71)   
run Algorithm ${ 2 } ( \hat { r } _ { \beta } ^ { ( p ) } , { U } ^ { ( p ) } ( \hat { \pmb { \theta } } ) , \hat { \Psi } ^ { ( p ) } , \hat { C } _ { \beta } ^ { ( p ) } , \hat { \gamma } _ { \beta } ^ { ( p ) } , T _ { \beta } )$   
end for   
$\hat { \lambda } \gets$ from (65) ▷ update noise precision estimate   
$\hat { r } _ { \alpha } = r - U ( \hat { \pmb { \theta } } ) \hat { \pmb { \Psi } } \hat { \pmb { \beta } }$ ▷ update object signal residual   
$\hat { C } _ { \alpha } \gets$ from (59) ▷ update with new residual   
αˆ from (58)   
▷ Update object signal estimate:   
run Algorithm $3 ( \hat { r } _ { \alpha } , \hat { \Phi } , \hat { C } _ { \alpha } , \hat { \gamma } _ { \alpha } , T _ { \alpha } )$   
λ<sup>ˆ</sup>  from (65)   
$\hat { r } _ { \beta } = r - \hat { \Phi } \hat { \alpha }$   
$\hat { C } _ { \beta } \gets$ from (62)   
$\hat { \beta } \gets$ from (61)   
until convergence ▷ criterion or fixed number

Algorithm 1 describes the implementation of the proposed iterative algorithm. For notational simplicity, we consistently omit iteration counters; within the sequence of update steps, the algorithm uses the most recent values of other estimates. The proposed algorithm structure envisions a bottom-$u p$ scheme, i.e., that the dictionaries $\hat { \Phi }$ and analogously Ψ<sup>ˆ</sup> are initialized as empty. The noise precision is initialized as $\hat { \lambda } = ( 2 ( N P - 1 ) ) / | | \dot { \pmb { r } } | | ^ { 2 }$ , i.e., half the received signal power is assumed to be from noise initially.

The main iteration consists of two separated subroutines for the estimations of the respective object and interference signals, given in Algorithms 2 and 3. They are similar in structure and connected by computations of ${ \hat { r } } _ { \alpha } , { \hat { r } } _ { \beta } ,$ , as well as $\hat { \lambda } .$ I.e., the estimated residuals are used at every iteration as inputs to the respective subroutines. This scheme is obtained as the interference and object signals are additive and their components factorize according to (14) and (20). Furthermore, as interference is modeled independently over the ramps, separate steps over the index $p$ are applied. The estimation of multipath channels is based on the repeated addition and then update of line spectral components, in accordance with the bottom-up scheme, by applying (22) and Algorithm 4. The routine adds components it can “find” given the selected threshold, which are then refined or pruned using the now updated estimate of the weight covariance matrix.

Algorithm 2 Interference Signal Estimation (Subroutine)   
Require: Estimates $\hat { r } , \hat { \theta } , \hat { \Psi } , \hat { C } , \hat { \lambda } , \hat { \gamma } ;$ threshold $T$   
$\hat { k }  \mathrm { a r g }$ max<sub>k</sub>¯ $( \omega ^ { 2 } \bar { \kappa } / \rho _ { \bar { k } } )$ where $\bar { k } \in \bar { \mathcal { K } }$   
▷ find possible new component   
run Algorithm $4 ( \hat { r } , U ( \hat { \pmb { \theta } } ) \hat { \Psi } , \hat { C } , \hat { \gamma } , \hat { k } , U ( \hat { \pmb { \theta } } ) \hat { \psi } _ { \hat { k } } , T )$   
▷ add component if above threshold   
for all $k \in \mathcal { K }$ do ▷ update all existing components   
run Algorithm $4 ( \hat { r } , U ( \hat { \pmb { \theta } } ) \hat { \Psi } , \hat { C } , \hat { \gamma } , k , \hat { \psi } _ { k } , T )$   
end for   
$\hat { \beta } \gets$ from (61)   
θ<sup>ˆ</sup>  from (71) ▷ update chirp parameter estimates

$$
\hat { r } , \hat { \Phi } , \hat { C } , \hat { \lambda } , \hat { \gamma } ;
$$

$$
\boldsymbol { \hat { l } } \gets \boldsymbol { L }
$$

$$
\hat { \zeta } _ { \hat { l } } \gets
$$

$$
\phi _ { \hat { l } } \gets
$$

$$
4 ( \hat { r } , \hat { \Phi } , \hat { C } , \hat { \gamma } , \hat { l } , \hat { \phi } _ { \hat { l } } , T )
$$

$$
\hat { \textbf { \alpha } } 
$$

$$
\hat { \zeta } _ { l } \gets
$$

$$
\hat { \zeta } _ { l }
$$

$$
4 ( \hat { r } , \hat { \Phi } , \hat { C } , \hat { \gamma } , l , \hat { \phi } _ { l } , T )
$$

Algorithm 1 starts by estimating the interference as described by Algorithm 2. The interference channel is estimated on a grid. Hence, the possible “complete” set of basis vectors of the dictionary matrix is fixed, denoted by the index sets and $\bar { \mathcal { K } } = \{ [ 0 , K - 1 ] \backslash \mathcal { K } \}$ for the respective active and passive sets of basis vectors. At every iteration, we select the passive component with the largest estimated component SNR to potentially add to the active dictionary. Irrespective whether or not a new component was added, we proceed with updating all active components. Only a single component is potentially added per main iteration to avoid $\hat { \Psi }$ converging before the chirp parameter estimates θ<sup>ˆ</sup>. θ<sup>ˆ</sup> is updated once before and after this dictionary update process. The initial chirp parameter estimates are provided by evaluating the cost function on a coarse grid. Further estimates are obtained by applying any established constrained optimization algorithm, with possible values of θ<sup>ˆ</sup> constrained to a reasonable range.

Algorithm 4 Fast Component Precision Update (Subroutine)   
Require: Estimates rˆ, Φ<sup>ˆ</sup> , C<sup>ˆ</sup>, λ<sup>ˆ</sup>, γˆ; existing or new component   
index $l ,$ basis vector $\hat { \phi } _ { l } ,$ , threshold T   
$\rho _ { l } \gets$ from (23)   
$\omega _ { l } ^ { 2 } \gets$ from (24)   
if $\omega _ { l } ^ { 2 } / \rho _ { l } > T$ then   
$\hat { \gamma } _ { l } \gets ( 1 / ( \omega _ { l } ^ { 2 } - \zeta _ { l } ) )$   
if $l \notin { \mathcal { L } }$ then ▷ add new component   
$\hat { \gamma }  ( \hat { \gamma } \cup \hat { \gamma } _ { l } )$   
$\hat { \Phi }  ( \hat { \Phi } \cup \hat { \phi } _ { l } )$   
$L \gets L + 1$   
end if   
else   
if $l \in \mathcal L$ then ▷ prune existing component   
$\hat { \gamma }  ( \hat { \gamma } \setminus \hat { \gamma } _ { l } )$   
$\hat { \Phi }  ( \hat { \Phi } \setminus \hat { \phi } _ { l } )$   
$L \gets L - 1$   
end if   
end if   
C<sup>ˆ</sup> <sub>←</sub> from (59) using updated $\hat { \gamma }$ and $\hat { \Phi }$

For the grid-less object signal estimation of Algorithm 3, the basis vectors are generated and refined adaptively according to the respective estimates $\hat { \zeta } _ { l }$ . Also here, only at most a single component is added per iteration. In this way, the chance of converging to local optima by wrongly assigning part of the interference to the object estimate is minimized. Finally, note that the value of the component threshold for the coherently received object signal $T _ { \alpha }$ can be systematically set using the analysis in [67] to achieve a certain false alarm rate. This is not the case for its interference counterpart $T _ { \beta }$ due to the unknown θ. As the object signal is coherently processed over all ramps, $T _ { \alpha } > T _ { \beta }$ is reasonable. Empirical testing has shown that a low threshold between 0dB and 6dB for the interference is generally desirable.

## IV. ANALYSIS AND RESULTS

## A. Fundamental Object Estimation Performance

The main task of the radar sensor is to accurately determine the distances and velocities of surrounding objects. Therefore, we evaluate the proposed algorithm based on the quality of object parameter estimates. First, a comparison to the CRLB [68] on the estimation error variance is carried out. In order to simplify the analysis and numerical evaluations, a scenario with a single transmit ramp, and hence delayonly estimation, is set up. The object channel consists of a single line spectral component whereas the interference channel is constant, i.e., there is only direct-path interference corresponding to a single component at excess delay zero. The interference signal template is as described in Section II and Appendix A. The AAF frequency transfer function is a raised cosine with Nyquist bandwidth $f _ { \mathrm { s } } / 4$ and roll-off factor 0.25. Relevant signal parameters for this experiment are in Table I (column denoted Simulation I).

We study the expected root mean squared error (RMSE) of the normalized beat frequency estimate $\sqrt { \langle \| \hat { \varphi } - \tilde { \varphi } \| ^ { 2 } \rangle }$ over 500 simulated realizations. The expectation is replaced by the sample average, where only realizations with correct model order estimates $\hat { L } = \tilde { L } = 1$ are taken into account. Different realizations consist of varying the noise as well as the phases of the complex scalar weights $\tilde { \alpha }$ and ${ \tilde { \beta } } .$ The RMSE is analyzed for different SNRs and signal-to-interference ratios (SIRs), defined as

$$
\mathrm { S N R } = \lambda \| \Phi ( \tilde { \zeta } ) \tilde { \alpha } \| ^ { 2 }\tag{25}
$$

$$
\mathrm { S I R } = \| \Phi ( \tilde { \zeta } ) \tilde { \alpha } \| ^ { 2 } / \| U ( \tilde { \theta } ) \tilde { \Psi } \tilde { \beta } \| ^ { 2 } .\tag{26}
$$

Three algorithm variants are considered. First, mutual interference is completely neglected in the inference model, i.e., Algorithm 2 and associated steps are removed. Second, the factorized algorithm as proposed in this work can be applied. Third, as mentioned in Section III, it is possible to jointly model the interference and object channels within a larger concatenated dictionary by modeling the joint weight proxy $q ( \alpha , \beta )$ in (20). For all variants, component acceptance thresholds are set to $T _ { \alpha } = 9 \mathrm { d B }$ and $T _ { \beta } = \mathrm { 3 d B }$ . Results are compared to the root mean CRLB whose values are computed from the given signal model of (9). Fig. 2 shows an example result of the proposed algorithm.

![](images/5658b56fc104dfb04162ea185fea7b9d7003ee924c620ca5336bfedbae7555e4.jpg)  
Fig. 2. Example signal and object estimate at $\mathrm { S N R } = 3 0 \mathrm { d B }$ and $\mathrm { S I R = }$ 15dB. To reduce visual clutter, only certain signals are shown. The upper plot contains the fast-time view of the complete received signal r, the object source signal $_ { r _ { \mathrm { O } } }$ and its estimate $\scriptstyle { \hat { r } } _ { \mathrm { O } }$ . The lower plot contains the same signals in the delay domain, as well as the true object channel components (ζ<sup>˜</sup> and α˜ ), their estimates $( \hat { \zeta }$ and αˆ), and the estimated interference channel components (ϑ<sup>ˆ</sup> and $\hat { \beta } )$

In Fig. 3a it can be seen for a fixed SIR = 0dB that the algorithm jointly modeling object and interference channels achieves the CRLB once the SNR is high enough for the object channel component to be detected. The factorized algorithm only experiences a slight performance loss visible at high SNRs, whereas the “object only” algorithm, as expected, cannot achieve an estimation error below a certain value determined by the disturbing interference.

TABLE I  
SUMMARY OF RELEVANT SIGNAL PARAMETERS FOR THE ANALYSIS. c DENOTES THE SPEED OF LIGHT IN A VACUUM. Parameter Simulation I Simulation II Obj. Measurement Int. Measurement
<table><tr><td colspan="8"></td></tr><tr><td></td><td colspan="8">Victim Radar and Object Channel 79 79</td></tr><tr><td colspan="8">Ramp start frequency fo(GHz) Ramp slope</td><td colspan="2">76.2  $2 . 0 8 \times 1 0 ^ { 4 }$ </td></tr><tr><td>Ramp duration</td><td colspan="8"> $k ( \mathrm { G H z } / \mathrm { s } )$   $T _ { \mathrm { s w } } ( \mu \mathrm { s } )$ </td></tr><tr><td></td><td colspan="2">25 25</td><td colspan="2">25</td><td colspan="2"> $2 . 0 8 \times 1 0 ^ { 4 }$  6.39</td><td>24</td></tr><tr><td>Pulse duration  $T _ { \mathrm { p } } ( \mu \mathrm { s } )$ </td><td colspan="2"></td><td colspan="2">25</td><td colspan="2">44</td><td>44</td></tr><tr><td>No. of ramps P</td><td colspan="2">1</td><td colspan="2">16</td><td colspan="2">32</td><td>32</td></tr><tr><td>No. of samples N</td><td colspan="2">256</td><td colspan="2">128</td><td colspan="2">256</td><td>256</td></tr><tr><td>Sampling frequency  $\mathrm { f _ { s } = 1 / T _ { s } ( M H z ) }$ </td><td colspan="2">10.2</td><td colspan="2">5.1</td><td colspan="2">40</td><td>40</td></tr><tr><td>No. of components L</td><td>1</td><td colspan="2"></td><td>10</td><td colspan="2">unknown</td><td>unknown</td></tr><tr><td>Component weights α</td><td> $1 \exp { ( \mathrm { j } \varphi _ { \alpha } ) } ,$   $\varphi _ { \alpha } \sim \mathcal { U } ( 0 , 2 \pi )$ </td><td colspan="2"></td><td>log |α|2d [dB]  $= - 4 0 \log ( \tilde { \tau } \mathrm { c } _ { 0 } ^ { \ast } + 1 ) + x ,$  x ∼ U(−3, 3)</td><td colspan="2">unknown</td><td>unknown</td></tr><tr><td>Component delays  $\tilde { \tau } ( \mathrm { n s } )$ </td><td></td><td colspan="2">80.06</td><td>U(3.97, 127)</td><td colspan="2">unknown</td><td>unknown</td></tr><tr><td>Component Doppler frequencies ν(kHz)</td><td></td><td>0</td><td>U(−5,5) Interferer and Interference Channel</td><td colspan="2"></td><td>unknown</td><td>unknown</td></tr><tr><td colspan="8">Ramp start frequency f1(GHz) 79.01 {79.002, 79.004, 79.008} 76.1</td></tr><tr><td colspan="8">Ramp slope  $k _ { \mathrm { I } } { \mathrm { ( G H z / s ) } }$   $9 . 2 \times 1 0 ^ { 3 }$   $\{ 9 . 8 3 2 1 , 9 . 7 1 2 2 , 9 . 3 9 2 5 \} \times 1 0 ^ { 3 }$ </td></tr><tr><td colspan="2"></td><td colspan="2">25</td><td colspan="2">25.02</td><td colspan="2"></td><td> $2 . 6 9 2 3 \times 1 0 ^ { 4 }$ </td></tr><tr><td colspan="2">Ramp duration  $T _ { \mathrm { s w I } } ( \mu \mathrm { s } )$ </td><td colspan="2"></td><td colspan="2"></td><td colspan="2"></td><td>26</td></tr><tr><td colspan="2">Pulse duration  $T _ { \mathrm { p I } } ( \mu \mathrm { s } )$ </td><td colspan="2">25</td><td colspan="2">{75.01, 50.01, 25.02}</td><td colspan="2"></td><td>25</td></tr><tr><td colspan="2">No. of ramps P1 No. of components K</td><td colspan="2">1 1</td><td colspan="2">{2, 4, 8} 10</td><td colspan="2"></td><td>8</td></tr><tr><td colspan="2"></td><td colspan="2"> $| \beta | \exp { ( \mathrm { j } \varphi _ { \beta } ) } ,$ </td><td colspan="2"> $\log | \beta | _ { \mathrm { [ d B ] } } ^ { 2 }$ </td><td colspan="2">unknown</td><td colspan="2">unknown</td></tr><tr><td colspan="2">Component weights β</td><td colspan="2">[β| according to SIR,  $\varphi _ { \beta } \sim \mathcal { U } ( 0 , 2 \pi )$ </td><td colspan="2"> $\begin{array} { r } { = - 2 0 \log ( \tilde { \tau } _ { \mathrm { I } } \mathrm { c } _ { 0 } + 1 ) + x , } \\ { x \sim \mathcal { U } ( - 1 0 , 0 ) } \end{array}$  0 for first component,</td><td colspan="2"></td><td colspan="2">unknown</td></tr><tr><td colspan="8">中 4 10⁻2 É</td><td colspan="2"></td></tr><tr><td colspan="4" rowspan="3"></td><td rowspan="3">0 0</td><td colspan="4"></td><td colspan="2"></td></tr><tr><td colspan="2"></td><td colspan="2">10-3</td><td></td></tr><tr><td colspan="3">10-3 C</td><td colspan="2">e</td></tr><tr><td colspan="4" rowspan="2">10⁻4 0 00 0</td><td colspan="2"></td><td colspan="3" rowspan="2"></td><td rowspan="2">0 O Q</td></tr><tr><td colspan="3">0</td></tr><tr><td colspan="3">网</td><td colspan="4">Q</td><td></td><td>0</td></tr><tr><td colspan="4" rowspan="3">窗 </td><td colspan="4"></td><td></td></tr><tr><td colspan="2">0</td><td colspan="2">中</td></tr><tr><td colspan="4">0 网 网 圈 圈 日 10 4 ★ 圈</td></tr><tr><td colspan="4">四网 10 中 圈 8 1 40 60 -40</td><td colspan="4">0 -20</td></tr></table>

![](images/7396ccbeac4f8da3bcffef395d07e6346c1c32f91f1671588ebe3fabd41481fb.jpg)  
Object Detection Only Proposed Variant Joint Posterior Variant Root Mean CRLB  
Fig. 3. Statistical results of single-object delay estimation RMSE. (a) Evaluated over varying SNR at a fixed SIR of 0dB. (b) Evaluated over varying SIR at a fixed SNR of 30dB. (c) Evaluated for the AAF model error scenario.

We also observe the performance over varying SIR values, plotted in Fig. 3b for a fixed $\mathrm { S N R } = 3 0 \mathrm { d B }$ . The performance of object-only channel estimation strongly deteriorates with increasing interference power. Although the RMSE seemingly recovers at lower SIR, this is misleading as the estimate gets dominated by the interference signal and the number of missed detections is growing. Below around 30dB, the component cannot be detected at all. This is not the case for the signal separation-based methods. The proposed factorized algorithm shows its largest evaluated deviation from the theoretical optimum at <sub>−</sub>15dB (highlighted by a close-up). We observe that the worst case for the factorized algorithm is related to the condition

$$
\lVert \tilde { \Phi } ^ { \mathrm { H } } \tilde { \Phi } \tilde { \alpha } \rVert \approx \lVert \tilde { \Phi } ^ { \mathrm { H } } U ( \tilde { \pmb { \theta } } ) \tilde { \Psi } \tilde { \beta } \rVert\tag{27}
$$

measuring the similarity between object and interference signals when projected onto the object signal base Φ<sup>˜</sup> , with equality reached around $- 2 0 < \mathrm { S I R } < - 1 5 \mathrm { d B }$ . We hypothesize that such a condition has theoretical significance for the signal separation problem, but further rigorous analysis is necessary. The algorithm again tends to the CRLB at lower SIR. From a practical point of view, it is certainly most important in a radar application to achieve some guaranteed performance at critical low-SIR and low-SNR scenarios.

<table><tr><td></td><td>Received Signal</td><td></td><td>Object Signal</td></tr><tr><td></td><td>Object Signal Estimate</td><td>日</td><td>Object Components</td></tr><tr><td>O</td><td>Object Components Estimate</td><td></td><td></td></tr><tr><td></td><td>·Interference Components Estimate</td><td></td><td></td></tr></table>

## B. Robustness to Interference Model Error

Any model-based algorithm breaks down if the inference model is not sufficiently accurate to reality. In our application, it cannot for example be assumed that we have perfect knowledge of the AAF transfer function $G ( f )$ for specific radar hardware. Hence, we investigate the behavior of the algorithm when assuming, as previously, the raised cosine envelope for inference but in fact generating the tested interference signal using convolution with a Butterworth lowpass filter with equivalent filter parameters. This constitutes a small, but not negligible error in the filter’s assumed transfer function. An example result is shown in Fig. 4.

![](images/f6a9f6ed23d63d1dbb253e6ac026e793fd2bc7323ecd230e262743b0f68397f5.jpg)  
Fig. 4. Example signal and estimation results at SNR = 30dB and SIR = 15dB with model error. The included signals are the same as for Fig. 2. To note in particular is that the estimate for the interference channel is biased, meaning that it estimates more than a single component. This compensates for the model error, resulting in a more robust estimate of the object component.

Fig. 3c shows the same analysis as for Fig. 3b, but with the introduced model error. As expected, an increasing error in the object channel parameter estimate becomes visible below a certain SIR. Nevertheless, the algorithm does not abruptly break down and behaves robustly, reaching the CRLB for SIR 30dB. The reason for this adaptability is illustrated in Fig. 4. Note in Fig. 4 that several line spectral components are estimated for the interference channel, even though the signal is simulated with line-of-sight interference only. These additional components compensate for the AAF model error.

## C. Statistical Performance Comparison

We study the performance of the proposed algorithm in broader, more complex scenarios. Table I shows the relevant simulation parameters in the column denoted Simulation II. The radar system receives N = 128 fast-time samples from

$P ~ = ~ 1 6$ ramps each, with the task to estimate objects range and velocity parameters. The interferer transmit ramp parameters are chosen randomly for each realization from three different sets representing three scenarios. The three sets represent increasing interference burst durations while decreasing the number of interfered ramps, which arises naturally due to the form of FMCW transmit signals.

Both object and interference channels consist of $\tilde { L } \ =$ $\tilde { K } = 1 0$ line spectral components. Dispersion parameters are chosen randomly on a uniform distribution, while component magnitudes are set proportionately according to the radar equation [69] with some random variation to account for the radar cross section of different physical objects. Note also the different exponents in the radar equation for victim and interference channels [70]. For the interference, the first channel component is fixed to a delay of zero and relative magnitude of one. This is the direct path interference between sensors, which has been observed to dominate in power [71].

As these are multi-target scenarios, performance metrics appropriate for multi-target detection are selected. The generalized optimal subpattern assignment (GOSPA) metric [72] is suited to such cases. Its evaluation starts with an assignment of the estimated components to the true ones based on an upper-bounded estimation error metric. GOSPA can be split into a so-called localization and a cardinality error term. The former is the sum of estimation errors for the assigned components, while the latter penalizes non-assigned detections. The cardinality error can be further split into two terms proportional to the number of misdetections and false alarms, respectively. We use the assignment method of GOSPA and analyze variants of these three error terms, leading to an insightful set of performance metrics. For the localization error, we change the sum of errors of [72] to the mean of Euclidean distances. This yields a metric comparable to the single-component RMSE, here termed the mean assigned RMSE. For the two cardinality error terms, we evaluate the absolute number of misdetections and false alarms directly.

Our proposed algorithm is compared with two other methods for interference mitigation found in literature. Note that these are preprocessing methods to be employed prior to a separate object detection step in the automotive radar signal processing chain. In order to ensure a fair comparison, the “object only” algorithm of Section IV-A is applied after preprocessing, as well as in the No Mitigation and No Interference test cases. The two methods, both introduced in Section I, are:

• Zeroing - zeroing relies on the explicit prior detection of interfered samples, which is assumed perfect here. Comparison of different algorithms for the detection of interfered samples is out of the scope of this work.

• Morphological component analysis (MCA) - using the concept and model of [49]. Our implementation follows that of [73, Algorithm 30].

Figs. 5a-c depict the mean of the resulting metrics computed from 500 realizations over a varying SNR. Interference leads to a lower limit on the achievable estimation error and the number of misdetections, and causes false alarms. With preprocessing, the estimation error and number of misdetections improve, but the performance is still limited and improvements come at the cost of false alarms. This behavior can be explained by considering the effects of preprocessing on the form of the resulting signal. Zeroing merely exploits the time-limited nature of the interference, and hence leads to a signal with missing clusters of samples. MCA considers a signal separation problem, but does not employ a parametric model for the interference bursts and only applies single-ramp on-grid LSE for the object signal. Preprocessing therefore typically causes a distortion of the object signal that is a model error for the subsequent detector, primarily leading to false alarms. Our proposed method mitigates this behavior and reaches performance very close to the No Interference case. The estimation error and the number of misdetections decrease with increasing SNR, and the number of false alarms is constant according to the set detection threshold.

![](images/69189c294e5c6a22f79bd080f33d1159dafa22e8a90a272be94fbd1c722c51c1.jpg)  
(a)

![](images/8fd35b18f9d65483d39bf76ba77a32712444f253f5ffe3ac32c40e450916b44a.jpg)  
(b)

![](images/7cb431aa3e136149a2776fadadfc22e266d1f10b7422e3e53fb809bf6b1f1eaf.jpg)  
(c)

![](images/a0b6b122bf15868ac605f90788db9bd8b2fea72f79788839291538e6f79fca11.jpg)  
(d)

![](images/76e5421b80c5e81f7bc559a1ba332f221fa8743a6f6b8651d3780b1f54f2ea60.jpg)

![](images/72795569c9bdf68f61559b330806454a4f14c96fca3da32f9bb6eee0f775750c.jpg)  
(e)  
(f)

![](images/060f3adf3f89da5c1dd1b15bbac5a0347f03690170053246abae0abe8083b3e6.jpg)

![](images/c077fb4a68f94ce10b8145dc2577bf7d135a74b02047d61954a5ce0d70e28b26.jpg)

![](images/91b37af044b0c77fb30629f98a577dab687845c882f86be31eab73b3f9f05fa9.jpg)  
No Mitigation Zeroing MCA Proposed No Interference  
Fig. 5. Statistical results of multi-object simulation scenario. (a)-(c) Sample mean over varying SNR at a fixed SIR of 20dB. (d)-(f) Sample mean over varying SIR at a fixed SNR of 60dB. (g)-(i) Distribution of results at an SNR of 60dB and SIR of 15dB for each compared method, depicted in the form of box plots. Markers indicate outlier values, and the total number of outlier samples is additionally annotated.

Figs. 5d-f show mean results at a high SNR, over SIR levels ranging from highly interfered to weakly interfered object signals. Ideally, perfect interference cancellation leads to values identical to the No Interference case at SNR = 60dB. The proposed method approximately achieves this up until

SIR 0dB. Its performance then slightly decreases with decreasing interference power up until SIR 15dB, after which it slowly recovers. This is the same effect as discussed in Section IV-A. Note that unlike for the simulation scenario of Fig. 3, in the scenario of Fig. 5 the condition of (27) is met roughly at 5dB < SIR < 10dB. This strengthens our hypothesis on the significance of this condition. For the other evaluated methods, we see a bounded improvement in RMSE and misdetection rate at the cost of further false alarms. Naturally, perfect zeroing is independent of interference power while MCA performance is generally improved with increasing SIR.

Figs. 5g-i illustrate the distributions of the results at SNR = 60dB and SIR = 15dB using box plots, in order to evaluate the robustness of the tested methods. In particular for the proposed method, this further gauges the risk of the algorithm converging to a local optimum of the signal separation problem, which could significantly decrease object detection performance. We indeed observe some outliers with higher RMSE values and an increased number of false alarms.

![](images/35eda42c77403d6fffc99afadd846245fa7620a67c0477467baec4f8ada324f0.jpg)  
Fig. 6. Example signals and estimates of a single interfered ramp at $\mathrm { S N R = }$ 60dB and $\mathrm { S I \dot { R } = - 1 5 d B }$ . The included signals are the same as for Fig. 2.

However, the number of significant outliers, particularly when noting that the comparison is to be made to the ideal No Interference test case, is very small.

We also include in Fig. 6 an example plot analogous to Figs. 2 and 4. We typically observe $\hat { K } ~ > ~ \tilde { K }$ , i.e., the amount of interference channel line spectral components is overestimated in our interference estimation subroutine. This necessarily occurs when there are several relatively closelyspaced components, as we employ on-grid estimation on a small grid $( K = 2 N )$ with a relatively low detection threshold $T _ { \beta }$ . Nevertheless, it can be seen that the object signal is successfully estimated.

In summary, our algorithm statistically outperforms the investigated preprocessing methods across the whole investigated SNR/SIR space and only slightly diverges from optimal interference cancellation in a less critical high-SIR region of this exploration space.

## D. Measurement Examples

In order to illustrate the practical application of the proposed method, we apply it to radar measurement data from two different datasets. We select a single measurement each and showcase the results qualitatively; note that no ground truth of the channel parameters are available.

The first example was obtained as part of a measurement campaign in real traffic scenarios, details of which can be found in previous works [74], [75]. Measurement parameters are summarized in Table I (Obj. Measurement). These measurements do not inherently contain any interference. In prior work, simulated interference was added to the measured signals. In this work however, measured interference is added, as described in Appendix C, with parameters listed in Table I (Int. Measurement). The interference was obtained from a separate measurement, due to the difficulty of generating and measuring interference separately in the same inner city traffic environment. Nevertheless, the applied scheme enables a qualitative comparison of our mitigation result to an interference-free one, with both object and interference components obtained using actual radar sensors.

Fig. 7a shows a photo of the selected Obj. Measurement scene. Particularly, visible on the photo is the car in front and to the left of the ego-radar, as well as the facade of a row of buildings to the right. The interference-free spectrum in Fig. 7b hence contains a few close object components with a positive relative velocity, i.e., the car moving away from the sensor. The buildings lead to a large number of components distributed over distances, with negative relative velocities with respect to the measurement vehicle. Other detected components are reflections not easily associated with the camera image or false alarms due to noise. When strong interference is introduced, the range-Doppler spectrum becomes dominated by it, see Fig. 7c. Directly applying object detection onto this signal leads to no discernibly useful result. Finally, the spectrum of the measurement when subtracting the interference estimated by the proposed processing algorithm, and the estimated object components are shown in Fig. 7d. The resulting spectrum is visually very close to the interference-free one and the detected components correspond well to the significant parts of the described scene. A number of missed detections and false alarms are observed, but mostly of comparatively small magnitudes. These are likely in large part a result of an interference model error due to unknown measurement hardware characteristics, further discussed in Appendix C. We also qualitatively illustrate the fast-time signal of a single ramp in Fig. 8 as an example. The top graph shows a large interference burst not too dissimilar to, but distinct from the simulated ones of Figs. 2 and 4. The bottom plot provides a close-up view of the signal after subtraction of the interference estimate as well as shows the object signal estimate.

The second example measurement originates from [76], [77]. Measurement parameters and further details are found in the cited references. The measurement hardware and scenario are distinct from the previously presented measurement, in particular with respect to the interference. Here, the measurements inherently contain interference from two different sensors, so that no additional processing as described in Appendix C is necessary. The scenario is mostly static with significant reflections up to a distance of 20m, as well as a small drone flying around. Figs. 7e-h show the results for this example in an analogous manner to Figs. 7a-d. No exact ground truth is available, but the “clean” reference of Fig.7f is taken from the previous measurement frame, during which no interferer crossed the victim radar’s IF band. Similarly to the previous example, we can see that the mitigated spectrum as well as the detected components closely match the results for the interference-free measurement. We also observe a few false alarms, although no missed detections in contrast to the previous example measurement. This may largely be the consequence of the interference being significantly weaker in this scenario.

These very promising results are nevertheless only prelim inary, and a larger scale analysis with better known hardware and measurement environment is a necessary part of future work.

![](images/86561775b3ef69702c0ca4b3c6ade109734020ed7b2eebd09a55345703bf803b.jpg)  
(a)

![](images/a050b2ec94777d450856ff2d067ce10d6e97a2210a7fc6721e58df1bfcb5bdc6.jpg)

![](images/a5c7ecec0399a01710680abde740b4ebd2e4d255208111b9d4f43b8833c956ed.jpg)

![](images/f07ac5372cbf158d31538caa1607c4614f4d8083b022322b849a540a027fabb2.jpg)

![](images/f01e20db63d80005589aa41e0142e7e2e4e9e3cc41b3257f3a07f35237ee67c0.jpg)  
(e)

(b)  
![](images/ec3d5f599c01868a2f7cf219f5b7da5626328e0723245c16af4df5d405b2327a.jpg)  
(f)

(c)  
![](images/b502759c1a7950cc8cb5ab3f82c9ac29e43983bda275e1d2bb32e723204219ab.jpg)  
(g)

(d)  
![](images/5b56bb850f8a7f9ae8f6d19bbb91f21c0c6761bd97bb14b545ca794e89b948a8.jpg)  
(h)  
Fig. 7. Two examples of the proposed algorithm applied to real automotive radar measurement data. The first row is from the authors’ own combined object and interference measurements, while the second row is from a publicly available test dataset. White shaded rectangles indicate an object of interest that becomes undetectable due to interference. Detections are indicated by markers, where marker size represents component SNR. (a)/(e) Photo of the measurement scene. (b)-(c)/(f)-(g) Range-Doppler spectrum of the measured signal without/with interference and corresponding object detections. (d)/(h) Range-Doppler spectrum of the interference-cancelled signal and corresponding object detections as a result of the proposed algorithm. Estimated false alarms and missed detections, when taking the results for the non-interfered measurement as ground truth, are also indicated.

## V. CONCLUSION

This paper presents an algorithm to mitigate the mutual interference of automotive FMCW radars. We fully consider the underlying signal model and systematically design a modelbased inference algorithm. Our description of the interference considers both sensor-based effects and the multipath propagation environment. We propose to infer the delay-Doppler object channel and ramp-wise delay-only interference channels. The result is a superposition of LSE problems, with the noncoherent interference chirp envelopes modeled by additional unknown parameters. We extend the state-of-the-art sparse probabilistic inference approach to such a superposition within the variational EM framework. Our proposed inference model leads to an iterative algorithm consisting of subsequent object and interference estimation subroutines. This results in robust object detection performance that is often comparable to the interference-free case. Conventional interference mitigation preprocessing is shown to often lead to increasing false alarms in the object detection step, which the proposed algorithm is not susceptible to, in comparison. It is also shown that considering the estimation of interference as an LSE problem can offset minor model errors.

Specific choices in the proposed algorithm design, initialization and scheduling are essential for its performance. This includes employing grid-less estimation for the object channel, yielding super-resolution accuracy, while using an on-grid algorithm for the interference channels. Parameter optimization and inference of the respective channel weights are derived from a joint update, which decreases the probability of converging to a local optimum of the signal separation problem.

The proposed method has some limitations due to assumptions made in its derivation, as elaborated in the paper. Most prominently, at most a single interference chirp is assumed per ramp, and interference chirps are present over the full passband of the receiver’s AAF. While ways to adapt the algorithm are briefly discussed, more work is needed to verify their practical viability in different scenarios. Furthermore, we posit that signal separability is fundamentally limited by how distinct the involved signal bases are. Investigating such limits is also an interesting prospect for further work. Finally, note that although here presented for a specific application, the proposed algorithm is likely applicable to other signal separation problems of this kind.

![](images/9a3c68de803fcb82afc582c3c716913b4f268491664dea4cb0562039510d4562.jpg)  
Fig. 8. Qualitative example of the processed signal at a single interfered ramp and object signal estimation results. It shows a ramp of the measurement $^ { r , }$ of the mitigated signal being the object residual $\hat { r } _ { \alpha } ,$ and of the object signal estimate $\hat { r } _ { \mathrm { O } } = \hat { \Phi } \hat { \alpha }$ . The top and bottom graphs are the same result with different y-axis limits, the latter showing the much lower amplitude object signal.

## APPENDIX A DERIVATION OF SIGNAL MODEL

## A. Object Signal

To derive (5), we start with the transmit signal of (2). It propagates through the environment and reflects off of (moving) objects, i.e., a weighted sum of delayed transmit signals reach the receiver. The radar echo as a function of time t can be derived for ideal point reflections starting with $\begin{array} { r } { y _ { \mathrm { O } } ( t ) = \sum _ { l = 0 } ^ { L - 1 } \tilde { \alpha } _ { l } x ( t - \tilde { \tau } _ { l } ( t ) ) } \end{array}$ , where $\tilde { \tau } _ { l } ( t ) \approx 2 ( d _ { l } + v _ { l } t ) / \mathrm { c } _ { 0 }$ with $d _ { l }$ and v<sub>l</sub> being radial distance and velocity [78], and c<sub>0</sub> denotes the speed of light. In our derivations, we use an analogous formulation based on channel modeling [79]. I.e., the transmit signal propagates through the radar channel which can be described by the operation

$$
\begin{array} { l } { { \displaystyle y _ { \mathrm { O } } ( t ) = \int _ { \nu } \int _ { \tau } h _ { \mathrm { O } } ( \tau , \nu ) x ( t - \tau ) \exp { ( \mathrm { j } 2 \pi \nu t ) } \mathrm { d } \tau \mathrm { d } \nu } } \\ { { \displaystyle \quad = \sum _ { l } \tilde { \alpha } _ { l } x ( t - \tilde { \tau } _ { l } ) \exp { ( \mathrm { j } 2 \pi \tilde { \nu } _ { l } t } ) } } \end{array}\tag{28}
$$

with

$$
h _ { \mathrm { O } } ( \tau , \nu ) = \sum _ { l = 0 } ^ { \tilde { L } - 1 } \tilde { \alpha } _ { l } \delta ( \tau - \tilde { \tau } _ { l } ) \delta ( \nu - \tilde { \nu } _ { l } )\tag{29}
$$

where the channel is described by its spreading function $h _ { \mathrm { O } } ( \tau , \nu )$ in delay τ and Doppler frequency ν. The model assumes negligible coupling between delay and Doppler dispersion domains. Expanding on (28), we have

$$
\begin{array} { r } { y _ { \mathrm { { O } } } ( t ) = A \displaystyle \sum _ { l = 0 } ^ { \tilde { L } - 1 } \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p - \tilde { \tau } _ { l } ; T _ { \mathrm { s w } } ) \tilde { \alpha } _ { l } \exp { ( - \mathrm { j } 2 \pi \tilde { \nu } _ { l } t } ) } \\ { \times \exp { ( \mathrm { j } ( 2 \pi f _ { 0 } ( t - T _ { \mathrm { p } } p - \tilde { \tau } _ { l } ) + \pi k ( t - T _ { \mathrm { p } } p - \tilde { \tau } _ { l } ) ^ { 2 } ) ) } , } \end{array}\tag{30}
$$

where we will assume $A = 1$ for simplicity, without loss of generality.

To simplify this, we first note that in a continuous wave radar system, the maximum effective delay max(˜τ<sub>l</sub>) of the channel is much shorter than the duration of a transmit ramp $T _ { \mathrm { s w } }$ . We can hence approximately neglect the spreading of the ramp envelope itself. I.e., we swap the order of summations and apply $\bar { x } ( t { - } T _ { \mathrm { p } } p { - } \tilde { \tau } _ { l } ; T _ { \mathrm { s w } } ) \approx \bar { x } ( t { - } T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } )$ . Furthermore, the stop-and-go approximation $\tilde { \nu } _ { l } t ~ \approx ~ \tilde { \nu } _ { l } T _ { \mathrm { p } } p$ as commonly known in automotive radar [69] is applied. We obtain

$$
\begin{array} { c } { \displaystyle { y _ { \mathrm { O } } ( t ) \approx \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } ) \sum _ { l = 0 } ^ { \tilde { L } - 1 } \tilde { \alpha } _ { l } \exp { ( - \mathrm { j } 2 \pi \tilde { \nu } _ { l } T _ { \mathrm { p } } p ) } } } \\ { \displaystyle { \times \exp { ( \mathrm { j } ( 2 \pi f _ { 0 } ( t - T _ { \mathrm { p } } p - \tilde { \tau } _ { l } ) + \pi k ( t - T _ { \mathrm { p } } p - \tilde { \tau } _ { l } ) ^ { 2 } ) ) } . } } \end{array}\tag{31}
$$

Multiplying out and rearranging the terms in the chirp exponential straightforwardly leads to

$$
\begin{array} { l } { { \displaystyle y _ { \mathrm { O } } ( t ) = \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } ) } } \\ { { \displaystyle \qquad \times \exp ( \mathrm { j } ( 2 \pi f _ { 0 } ( t - T _ { \mathrm { p } } p ) + \pi k ( t - T _ { \mathrm { p } } p ) ^ { 2 } ) ) ) } } \\ { { \displaystyle \qquad \times \sum _ { l = 0 } ^ { \tilde { L } - 1 } \tilde { \alpha } _ { l } \exp \left( \mathrm { j } ( - 2 \pi ( f _ { 0 } + k ( t - T _ { \mathrm { p } } p ) \right) \tilde { \tau } _ { l } ) } } \\ { { \displaystyle \qquad \times \exp \left( \mathrm { j } ( \pi k \tilde { \tau } _ { l } ^ { 2 } ) \right) \exp \left( - \mathrm { j } 2 \pi \tilde { \nu } _ { l } T _ { \mathrm { p } } p \right) } . } \end{array}\tag{32}
$$

Reasoning again based on the short duration of the channel, we neglect the term $k \tilde { \tau } _ { l } ^ { 2 } \approx 0 \forall l$ . The rest of the expression in the last brackets is then the Fourier transform of the channel spreading function. Defining this as the object channel transfer function $H _ { \mathrm { O } } ( f , t )$ ), we write <sup>5</sup>

$$
\begin{array} { r } { y _ { \mathrm { O } } ( t ) \approx \displaystyle \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } ) \exp ( \mathrm { j } ( 2 \pi f _ { 0 } ( t - T _ { \mathrm { p } } p ) } \\ { + \pi k ( t - T _ { \mathrm { p } } p ) ^ { 2 } ) ) H _ { \mathrm { O } } ( f _ { 0 } + k ( t - T _ { \mathrm { p } } p ) , T _ { \mathrm { p } } p ) . } \end{array}\tag{33}
$$

Next, demodulation (demixing) according to stretch processing [80] is applied. Demixing is coherent for the object signal, so the transmit ramp envelope $\bar { x } ( t )$ over the ramp duration stays constant and the chirp term vanishes. I.e.,

$$
\begin{array} { l } { { \displaystyle y _ { \mathrm { O } } ^ { \prime } ( t ) = \biggl ( x ^ { * } ( t ) \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } ) \exp ( \mathrm { j } ( 2 \pi f _ { 0 } ( t - T _ { \mathrm { p } } p ) } } \\ { { \displaystyle \qquad + \pi k ( t - T _ { \mathrm { p } } p ) ^ { 2 } ) ) H _ { \mathrm { O } } \bigl ( f _ { 0 } + k ( t - T _ { \mathrm { p } } p ) , T _ { \mathrm { p } } p \bigr ) \biggr ) } } \\ { { \displaystyle \quad = \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { p } } p ; T _ { \mathrm { s w } } ) H _ { \mathrm { O } } \bigl ( f _ { 0 } + k ( t - T _ { \mathrm { p } } p ) , T _ { \mathrm { p } } p \bigr ) . } } \end{array}\tag{34}
$$

Finally, we assume that the object channel contains no significant amount of energy outside of the constant passband of the AAF, hence the convolution with $g ( t )$ can be neglected. The signal is projected onto the fast-time $t ^ { \prime } \in \mathsf { \Gamma } ( 0 , T _ { \mathrm { s w } } ) =$ $t - T _ { \mathrm { p } } p \forall p$ and slow-time p so that the explicit sum over $p$ vanishes as well. This leads to the result in (5).<sup>6</sup>

## B. Interference Signal

We derive the received interference signal from a single interferer, $r _ { \mathrm { I } , i } ( t ^ { \prime } , p )$ of (7), starting from the interferer transmit signal $x _ { \mathrm { I } , i } ( t )$ of (6). Note that for notational simplicity, we drop the explicit interferer subscript i in the sequel. First, propagation through a multipath channel leads to the expression

$$
\begin{array} { l } { { \displaystyle y _ { \mathrm { I } } ( t ) \approx x _ { \mathrm { I } } ( t ) \sum _ { k } ^ { \tilde { K } - 1 } \tilde { \beta } _ { k } \exp ( - \mathrm { j } 2 \pi \big ( f _ { \mathrm { I } } + k _ { \mathrm { I } } ( t - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } ) \big ) \tilde { \tau } _ { \mathrm { I } , k } \big ) } } \\ { { \displaystyle \qquad \times \exp \big ( - \mathrm { j } 2 \pi T _ { \mathrm { p I } } p _ { \mathrm { I } } \tilde { \nu } _ { \mathrm { I } , k } \big ) } } \\ { { \displaystyle = x _ { \mathrm { I } } ( t ) H _ { \mathrm { I } } \big ( f _ { \mathrm { I } } + k _ { \mathrm { I } } \big ( t - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } \big ) , T _ { \mathrm { p I } } p _ { \mathrm { I } } \big ) } } \end{array}
$$

analogously as for the object signal $y _ { \mathrm { O } } ( t )$ . However, this signal is non-coherently demodulated by multiplication with $x ^ { * } ( t )$ To elaborate, we explicitly write out the mixing, i.e.,

$$
\begin{array} { r l } { y _ { \mathrm { I } } ^ { \prime } ( t ) = } & { \bar { A } \displaystyle \sum _ { p = 0 } ^ { P - 1 } \bar { x } ( t - T _ { \mathrm { P } } p ; T _ { \mathrm { s w } } ) } \\ & { \times \exp ( - ( 2 \pi f _ { 0 } ( t - T _ { \mathrm { P } } p ) + \pi k ( t - T _ { \mathrm { P } } p ) ^ { 2 } ) ) } \\ & { \times \left( \displaystyle \sum _ { p = 0 } ^ { P _ { \mathrm { I } } - 1 } \bar { x } ( t - \bar { T } - T _ { \mathrm { P I } } p _ { \mathrm { I } } ; T _ { \mathrm { s w I } } ) \right. } \\ & { \quad \times \left. \exp ( \mathrm { j } ( 2 \pi f _ { \mathrm { I } } ( t - \bar { T } - T _ { \mathrm { P I } } p _ { \mathrm { I } } ) } \\ & { \quad \quad + \pi k _ { \mathrm { I } } ( t - \bar { T } - T _ { \mathrm { P I } } p _ { \mathrm { I } } ) ^ { 2 } ) ) \right. } \\ & { \times \left. H _ { \mathrm { I } } ( f _ { \mathrm { I } } + k _ { \mathrm { I } } ( t - \bar { T } - T _ { \mathrm { P I } } p _ { \mathrm { I } } ) , T _ { \mathrm { P I } } p _ { \mathrm { I } } ) \right) } \end{array}\tag{36}
$$

setting $\bar { A } = A _ { \mathrm { I } } A ^ { * } = 1$ without loss of generality in the sequel.

For convenience, we rewrite this in the fast- and slow-time domain description by substituting $t = t ^ { \prime } + T _ { \mathrm { p } } p$ , leading to

$$
\begin{array} { l l r } { { \displaystyle y _ { \mathrm { I } } ^ { \prime } ( t ^ { \prime } , p ) = \exp ( - \mathrm { j } ( 2 \pi f _ { 0 } t ^ { \prime } + \pi k t ^ { \prime 2 } ) ) } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \\ { { } } \end{array}\tag{37}
$$

noting again that the sum over p vanishes.

Carrying out the multiplication of the victim and interferer transmit chirps and rearranging the resulting phase terms with

respect to t<sup>′</sup>-dependency yields

$$
\begin{array} { r l } {  { y _ { \mathrm { I } } ^ { \prime } ( t ^ { \prime } , p ) = \sum _ { p _ { \mathrm { I } } = 0 } ^ { P _ { \mathrm { I } } - 1 } \bar { x } ( t ^ { \prime } + T _ { \mathrm { p } } p - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } ; T _ { \mathrm { s w I } } ) } } \\ & { \times \exp ( \mathrm { j } ( 2 \pi ( f _ { \mathrm { I } } + k _ { \mathrm { I } } ( T _ { \mathrm { p } } p - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } ) - f _ { 0 } ) t ^ { \prime } } \\ & { \quad \quad + \pi ( k _ { \mathrm { I } } - k ) t ^ { \prime 2 } ) ) } \\ & { \times \exp ( \mathrm { j } ( 2 \pi f _ { \mathrm { I } } ( T _ { \mathrm { p } } p - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } ) } \\ & { \quad \quad + \pi k _ { \mathrm { I } } ( T _ { \mathrm { p } } p - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } ) ^ { 2 } ) ) } \\ & { \times H _ { \mathrm { I } } ( f _ { \mathrm { I } } + k _ { \mathrm { I } } ( t ^ { \prime } + T _ { \mathrm { p } } p - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } } ) , T _ { \mathrm { p I } } p _ { \mathrm { I } } ) . } \end{array}\tag{38}
$$

Due to non-coherent demodulation, the effect of the AAF cannot be neglected for the interference. We can approximate the AAF for every slow-time index p separately as the convolution with an impulse response $g ( t ^ { \prime } )$ . We define $\bar { T } _ { 0 } = T _ { \mathrm { p } } p - \bar { T } - T _ { \mathrm { p I } } p _ { \mathrm { I } }$ to de-clutter notation, as well as the non-coherent demixed chirp

$$
\begin{array} { r } { \bar { u } _ { \mathrm { p I } } ( t ^ { \prime } , p ) = \exp ( \mathrm { j } ( 2 \pi \Delta f _ { 0 } t ^ { \prime } + \pi \Delta \tilde { k } { t ^ { \prime } } ^ { 2 } ) ) } \\ { \times \exp \bigl ( \mathrm { j } ( 2 \pi f _ { \mathrm { I } } \bar { T } _ { 0 } + \pi k _ { \mathrm { I } } \bar { T } _ { 0 } ^ { 2 } ) \bigr ) } \end{array}\tag{39}
$$

where $\Delta f _ { 0 } = f _ { \mathrm { I } } - f _ { 0 }$ and $\Delta \tilde { k } = k _ { \mathrm { I } } - k$ . This leads to the convolution integral expression

$$
\begin{array} { r l r } {  { r _ { \mathrm { I } } ( t ^ { \prime } , p ) = \sum _ { p _ { \mathrm { I } } = 0 } ^ { P _ { \mathrm { I } } - 1 } \bar { u } _ { \mathrm { p I } } ( t ^ { \prime } , p ) \biggl ( \int _ { \varsigma } \bar { x } ( t ^ { \prime } - \varsigma + \bar { T } _ { 0 } ; T _ { \mathrm { s w I } } ) } } \\ & { } & { \times \exp \bigl ( - \mathrm { j } ( 2 \pi ( \Delta f _ { 0 } + k _ { \mathrm { I } } \bar { T } _ { 0 } ) \varsigma + 2 \pi \Delta \tilde { k } t ^ { \prime } \varsigma - \pi \Delta \tilde { k } \varsigma ^ { 2 } ) \bigr ) } \\ & { } & { \times H _ { \mathrm { I } } \bigl ( f _ { \mathrm { I } } + k _ { \mathrm { I } } ( ( t ^ { \prime } - \varsigma ) + \bar { T } _ { 0 } ) , T _ { \mathrm { p I } } p _ { \mathrm { I } } \bigr ) g ( \varsigma ) \mathrm { d } \varsigma \biggr ) . } \end{array}
$$

Incorporating (40) directly into the inference model is possible, but leads to significantly increased complexity. In order to derive a simplified form used in this work, certain further approximations are considered. We introduce here the first two out of four main assumptions employed for inference:

Assumption 1 The envelope term $\bar { x } ( t ^ { \prime } - \varsigma + \bar { T } _ { 0 } ; T _ { \mathrm { s w I } } )$ can be neglected if it is assumed to be long enough in comparison to the filter impulse response. This assumption is correct in cases where the interferer’s transmit ramp is active during the whole time its frequency course would be inside the victim receiver’s IF bandwidth.

Assumption 2 We take the channel term $H _ { \mathrm { I } }$ outside the convolution integral, neglecting its dependence on ς. This is based on the reasoning that the chirp term $\bar { u } _ { p \mathrm { I } }$ dominates the result of the convolution.

We then rearrange the remaining chirp terms and obtain

$$
\begin{array} { r l r } {  { r _ { \mathrm { I } } ( t ^ { \prime } , p ) \approx \sum _ { p _ { \mathrm { I } } = 0 } ^ { P _ { \mathrm { I } } - 1 } \bar { u } _ { \mathrm { p I } } ( t ^ { \prime } , p ) H _ { \mathrm { I } } ( \bar { f } _ { \mathrm { I } } + k _ { \mathrm { I } } t ^ { \prime } , T _ { \mathrm { p I } } p _ { \mathrm { I } } ) \int _ { \varsigma } \exp ( \mathrm { j } ( \pi \Delta \tilde { k } \varsigma ^ { 2 } ) ) } } \\ & { } & { \times g ( \varsigma ) \exp ( - \mathrm { j } ( 2 \pi ( \Delta \tilde { f } _ { 0 } \varsigma + \Delta \tilde { k } t ^ { \prime } \varsigma ) ) ) \mathrm { d } \varsigma \qquad ( 4 1 ) } \end{array}
$$

where we have further defined $\bar { f } _ { \mathrm { I } } = f _ { \mathrm { I } } + k _ { \mathrm { I } } \bar { T } _ { 0 }$ and $\Delta \tilde { f } _ { 0 } =$ $\Delta f _ { 0 } + k _ { \mathrm { I } } \bar { T } _ { 0 }$

The non-coherently demixed signal with which the AAF impulse response is convolved is a chirp. Thus, similarly to the derivation for the multipath channel, we may describe the convolution result as approximately a multiplication with the AAF frequency transfer function evaluated over the frequency course of this chirp. However, the term $\exp ( \mathrm { j } ( \pi \Delta \tilde { k } \varsigma ^ { 2 } ) )$ cannot in general be neglected as the length of the AAF impulse response is long enough so that $\Delta \bar { \tilde { k } } \varsigma ^ { 2 } \not \approx 0 .$ Hence, we define the modified AAF impulse response as $\bar { g } ( t ^ { \prime } ) =$ $g ( t ^ { \prime } ) \exp ( \mathrm { j } ( \pi \Delta \tilde { k } { t ^ { \prime } } ^ { 2 } ) )$ and its frequency transfer function $\bar { G } ( f )$ In this way, the remaining expression is of an analogous form to (32), finally yielding (7).

## C. Inference Model

While our derivations yield parametric models for all terms of (1), the full model contains an unknown number of interferers. These cause interference bursts distributed over the received ramps depending on the victim and interferer transmit parameters as well as the propagation channel. To relax the resulting inference problem, we make the following further model assumptions in this work:

Assumption 3 We limit the maximum amount of interference bursts at a certain slow-time index $p$ to one, i.e., the sum over $p _ { \mathrm { I } }$ in (7) vanishes.

If the number of bursts is known or estimated apriori, our algorithm can be trivially adapted, although signal separation becomes increasingly illposed with a growing number of bursts. If it is unknown, it may be included in the inference model by considering a structured dictionary [81]. Algorithms for problems of this kind within the variational framework have been proposed in recent works [64], [82].

Assumption 4 We consider every interference burst over the slow-time independently. The channel term in (38) therefore becomes for every ramp p a different delay-only line spectrum with frequency transfer function $H _ { \mathrm { I } } ^ { ( p ) } ( n )$

For a single interferer, it is possible to consider the interference signal as the sequence of all received bursts propagating through a delay-Doppler channel. We have not investigated such an approach in this work, and note that more complex model assumptions can increase the risk of major model errors, as well as lead to increased algorithm complexity.

The above assumptions together mean that the sum $\begin{array} { r } { \sum _ { i = 0 } ^ { M _ { \mathrm { I } } - 1 } r _ { \mathrm { I } , i } ( n , p ) } \end{array}$ can be replaced by a single equivalent $r _ { \mathrm { I } } ( n , p )$ irrespective of $M _ { \mathrm { I } }$ . Furthermore, terms of this interference signal $r _ { \mathrm { I } } ( n , p )$ that do not explicitly depend on the fast-time index n become constants for inference. These terms include the second complex phasor factor of (39), as well as certain terms of the transfer functions $H _ { \mathrm { I } } ( f )$ and $\bar { G } ( f )$ . These constants are simply inferred within the complex channel weights $\beta ^ { ( p ) }$ . Hence, the model is finally rewritten as (8).

## APPENDIX B MEAN-FIELD VARIATIONAL EM UPDATES

For the structured mean-field proxy PDF $q = \prod _ { \mathcal { Q } } q _ { i }$ , the ELBO (19) can be recast to express its dependence of any

one factor $q _ { i }$ as [62], [65]

$$
\begin{array} { c } { { \mathcal { L } ( q ) = \left. \log p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb { \theta } ) \right. _ { q } - \left. \log q \right. _ { q } } } \\ { { { } } } \\ { { { } = \left. \left. \log p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb { \theta } ) \right. _ { \bar { q } _ { i } } \right. _ { q _ { i } } } } \\ { { { } } } \\ { { { } - \left. \log q _ { i } \right. _ { q _ { i } } - E _ { i } } } \\ { { { } = Z _ { i } + \left. \log \bar { p } _ { i } \right. _ { q _ { i } } - \left. \log q _ { i } \right. _ { q _ { i } } - E _ { i } } } \end{array}\tag{42}
$$

with

$$
E _ { i } = \sum _ { \mathcal { Q } \backslash q _ { i } } \left. \log q _ { j } \right. _ { q _ { j } }\tag{43}
$$

$$
\bar { p } _ { i } = { Z _ { i } } ^ { - 1 } \exp \Big ( \big \langle \log p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb \theta ) \big \rangle _ { \bar { q } _ { i } } \Big )\tag{44}
$$

$$
Z _ { i } = \int \exp \Big ( \big \langle \log p ( r , \alpha , \gamma _ { \alpha } , \beta , \gamma _ { \beta } , \lambda ; \zeta , \pmb \theta ) \big \rangle _ { \bar { q } _ { i } } \Big ) \mathrm { d } z _ { i }\tag{45}
$$

where $z _ { i }$ denotes the latent variables corresponding to the factor $q _ { i }$ . With all other latent variables ${ \bar { q } } _ { i }$ as well as parameters fixed, the term $E _ { i }$ and the normalization factor $Z _ { i }$ are both independent of $q _ { i }$ . The remaining terms form a negative Kullback-Leibler divergence (KLD), which is maximized for $q _ { i } \propto \bar { p } _ { i }$ , yielding (21). When only ${ \bar { q } } _ { i }$ are fixed (i.e., parameters are to be optimized jointly with $q _ { i } )$ $E _ { i }$ is still a constant, but $Z _ { i }$ is a function of the parameters. The properties of the negative KLD term remain, still yielding the solution $q _ { i } \propto \bar { p } _ { i }$ for the factor proxy PDF. Hence, the ELBO is maximized when $Z _ { i }$ is maximum, which directly leads to (22) for parameter estimation.

We proceed to summarize the solution steps needed to obtain the update equations for our model. To clarify the mathematical derivations to follow, we write out the logarithms of factor distributions in the joint PDF (14), i.e. (15) to (18), explicitly so that

$$
\begin{array} { l } { \log p ( \pmb { r } | \alpha , \beta , \lambda ; \zeta , \pmb { \theta } ) } \\ { = - P N \log \pi + P N \log \lambda } \\ { \qquad - \lambda ( \pmb { r } - \Phi \pmb { \alpha } - \pmb { U } \pmb { \psi } \beta ) ^ { \mathrm { H } } ( \pmb { r } - \pmb { \Phi } \pmb { \alpha } - \pmb { U } \pmb { \Psi } \beta ) } \end{array}\tag{46}
$$

$$
\log p ( \pmb { \alpha } | \gamma _ { \alpha } ) = \sum _ { l } \Bigl ( - \log \pi + \log \gamma _ { \alpha , l } - | \alpha _ { l } | ^ { 2 } \gamma _ { \alpha , l } \Bigr )\tag{47}
$$

$$
\begin{array} { r l } & { \log p ( \gamma _ { \alpha } ) = ( a _ { 0 } - 1 ) \log \gamma _ { \alpha , l } - b _ { 0 } \gamma _ { \alpha , l } } \\ & { \qquad + a _ { 0 } \log b _ { 0 } - \log ( \Gamma ( a _ { 0 } ) ) } \end{array}\tag{48}
$$

$$
\log p ( \beta | \gamma _ { \beta } ) = \sum _ { p } \sum _ { k } \Bigl ( - \log \pi + \log \gamma _ { \beta , k } ^ { ( p ) } - { | \beta _ { k } ^ { ( p ) } | } ^ { 2 } \gamma _ { \beta , k } ^ { ( p ) } \Bigr )\tag{49}
$$

$$
p ( \gamma _ { \beta } ) = ( c _ { 0 } - 1 ) \log \gamma _ { \beta , k } ^ { ( p ) } - d _ { 0 } \gamma _ { \beta , k } ^ { ( p ) }\tag{50}
$$

$$
\begin{array} { r l } & { p ( \lambda ) = \left( e _ { 0 } - 1 \right) \log \lambda - f _ { 0 } \lambda } \\ & { \qquad + e _ { 0 } \log f _ { 0 } - \log ( \Gamma ( e _ { 0 } ) ) . } \end{array}\tag{51}
$$

We refer back to Section II for the introduction of this probabilistic model and its components.

## A. Updates of Channel Weights

Using (21) to solve for the object channel weights $q _ { \alpha } ,$ first note that the expectation of (14) (i.e., the sum of (46) to (51)) with respect to $q _ { \lambda }$ and the $q _ { \gamma } \mathbf { \dot { s } }$ is obtained simply by applying

$\lambda  \hat { \lambda }$ and $\gamma  \hat { \gamma }$ . Neglecting constant terms independent of α, we are left with

$$
\begin{array} { r } { \log q _ { \alpha } \propto ^ { \mathrm { e } } - \hat { \lambda } \big \langle ( r - \hat { \Phi } \alpha - \hat { U } \hat { \Psi } \beta ) ^ { \mathrm { H } } ( r - \hat { \Phi } \alpha - \hat { U } \hat { \Psi } \beta ) \big \rangle _ { q _ { \beta } } } \\ { - \alpha ^ { \mathrm { H } } \hat { \Gamma } _ { \alpha } \alpha \quad ( 5 2 ) } \end{array}
$$

where $\propto ^ { \mathrm { e } }$ denotes proportionality after taking the exponential, and $\boldsymbol { \Gamma } = \mathrm { D i a g } ( \gamma )$ . For the remaining expectation we have, using the shorthand $\pmb { r } _ { \beta } = \pmb { r } - \hat { \Phi } \pmb { \alpha }$

$$
\begin{array} { r l } & { \big \langle ( \pmb { r } _ { \beta } - \hat { U } \hat { \Psi } \beta ) ^ { \mathrm { H } } ( \pmb { r } _ { \beta } - \hat { U } \hat { \Psi } \beta ) \big \rangle _ { \pmb { q } _ { \beta } } } \\ & { = \pmb { r } _ { \beta } ^ { \mathrm { H } } \pmb { r } _ { \beta } - \pmb { r } _ { \beta } ^ { \mathrm { H } } \hat { U } \hat { \Psi } \hat { \beta } - \hat { \beta } ^ { \mathrm { H } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \pmb { r } _ { \beta } + \big \langle \beta ^ { \mathrm { H } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \hat { U } \hat { \Psi } \beta \big \rangle _ { \pmb { q } } } \end{array}\tag{53}
$$

We can further rewrite this, as

$$
\begin{array} { r } { \left. \beta ^ { \mathrm { H } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \hat { U } \hat { \Psi } \beta \right. _ { q _ { \beta } } = \left. ( \beta - \hat { \beta } ) ^ { \mathrm { H } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \hat { U } \hat { \Psi } ( \beta - \hat { \beta } ) \right. _ { q _ { \beta } } } \\ { + \left. \hat { \beta } ^ { \mathrm { H } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \hat { \beta } \right. \qquad ( 5 ^ { d } } \end{array}
$$

and

4)

$$
\begin{array} { r l } & { \left. ( \beta - \hat { \beta } ) ^ { \mathrm { H } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \hat { U } \hat { \Psi } ( \beta - \hat { \beta } ) \right. _ { q _ { \beta } } } \\ & { \qquad = \mathrm { t r } \Big ( \hat { U } \hat { \Psi } \big \langle ( \beta - \hat { \beta } ) ( \beta - \hat { \beta } ) ^ { \mathrm { H } } \big \rangle _ { q _ { \beta } } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \Big ) } \\ & { \qquad = \mathrm { t r } \Big ( \hat { U } \hat { \Psi } \hat { C } _ { \beta } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \Big ) . } \end{array}\tag{55}
$$

The trace term of (55) is independent of α and can be neglected, hence defining $\hat { r } _ { \alpha } = r - \hat { U } \hat { \Psi } \hat { \beta }$ and recasting the rest of the terms in the form of a complex normal log-PDF yields

$$
\begin{array} { c } { { \log q _ { \alpha } \propto ^ { \mathrm { e } } - \hat { \lambda } ( \hat { r } _ { \alpha } - \hat { \Phi } \alpha ) ^ { \mathrm { H } } ( \hat { r } _ { \alpha } - \hat { \Phi } \alpha ) - \alpha ^ { \mathrm { H } } \hat { \Gamma } _ { \alpha } \alpha } } \\ { { = - \alpha ^ { \mathrm { H } } \left( \hat { \lambda } \hat { \Phi } ^ { \mathrm { H } } \hat { \Phi } + \hat { \Gamma } _ { \alpha } \right) \alpha + 2 \Re ( \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \alpha ) } } \\ { { - \hat { \lambda } ^ { 2 } \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \left( \hat { \lambda } \hat { \Phi } ^ { \mathrm { H } } \hat { \Phi } + \hat { \Gamma } _ { \alpha } \right) ^ { - 1 } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha } } } \\ { { + \hat { \lambda } ^ { 2 } \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \left( \hat { \lambda } \hat { \Phi } ^ { \mathrm { H } } \hat { \Phi } + \hat { \Gamma } _ { \alpha } \right) ^ { - 1 } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha } } } \\ { { = \log \mathrm { C N } ( \alpha | \hat { \omega } , \hat { C } \alpha ) + \log | \hat { C } _ { \alpha } | } } \\ { { + \hat { \lambda } ^ { 2 } \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \hat { C } _ { \alpha } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha } } } \end{array}\tag{56}
$$

where by coefficient comparison we obtain the result

$$
q ( \alpha ) = \mathrm { C N } ( \alpha | \hat { \alpha } , \hat { C } _ { \alpha } )\tag{57}
$$

$$
\hat { \alpha } = \hat { \lambda } \hat { C } _ { \alpha } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha }\tag{58}
$$

$$
\begin{array} { r } { \hat { C } _ { \alpha } = \left( \hat { \lambda } \hat { \Phi } ^ { \mathrm { H } } \hat { \Phi } + \hat { \Gamma } _ { \alpha } \right) ^ { - 1 } . } \end{array}\tag{59}
$$

The derivations for the interference channel weights $\beta$ are analogous, leading to

$$
q ( \beta ) = \mathrm { C N } ( \beta | \hat { \beta } , \hat { C } _ { \beta } )\tag{60}
$$

$$
\hat { \beta } = \hat { \lambda } \hat { C } _ { \beta } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \hat { r } _ { \beta }\tag{61}
$$

$$
\begin{array} { r } { \hat { \pmb { C } } _ { \beta } = \left( \hat { \lambda } \hat { \pmb { { \Psi } } } ^ { \mathrm { H } } \hat { \pmb { U } } ^ { \mathrm { H } } \hat { \pmb { U } } \hat { \pmb { { \Psi } } } + \hat { \pmb { { \Gamma } } } _ { \beta } \right) ^ { - 1 } . } \end{array}\tag{62}
$$

## B. Update of Noise Precision

Similarly for the noise precision update, noting only λ- dependent terms we have

$$
\begin{array} { r l } & { \log q _ { \lambda } \propto ^ { \mathrm { e } } \left( e _ { 0 } + P N - 1 \right) \log \lambda - f _ { 0 } \lambda } \\ & { \phantom { \log p q _ { \lambda } \propto } - \lambda \Big \langle \big \langle ( r - \hat { \Phi } \alpha - \hat { U } \hat { \Psi } \beta ) ^ { \mathrm { H } } ( r - \hat { \Phi } \alpha - \hat { U } \hat { \Psi } \beta ) \big \rangle _ { q _ { \beta } } \Big \rangle _ { q _ { \alpha } } . } \end{array}
$$

The expectations are analogous to the one in (52), denoting

$\hat { \pmb { r } } _ { \lambda } = \pmb { r } - \hat { \pmb { \Phi } } \hat { \pmb { \alpha } } - \hat { U } \hat { \pmb { \Psi } } \hat { \pmb { \beta } } .$ , leading to

$$
\begin{array} { r l } & { \log q _ { \lambda } } \\ & { \quad \propto ^ { \mathrm { e } } \left( e _ { 0 } + P N - 1 \right) \log \lambda - f _ { 0 } \lambda } \\ & { \quad \quad - \lambda \big ( \hat { r } _ { \lambda } ^ { \mathrm { H } } \hat { r } _ { \lambda } + \mathrm { t r } \big ( \hat { \Phi } \hat { C } _ { \alpha } \hat { \Phi } ^ { \mathrm { H } } \big ) + \mathrm { t r } \big ( \hat { U } \hat { \Psi } \hat { C } _ { \beta } \hat { \Psi } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } \big ) \big ) } \end{array}\tag{63}
$$

and therefore

$$
\begin{array} { r } { q ( \lambda ) = { \bf G a } ( \lambda | e , f ) \qquad \quad ( 6 4 ) } \\ { \hat { \lambda } = \displaystyle \frac { e } { f } = \frac { e _ { 0 } + P N } { f _ { 0 } + \hat { r } _ { \lambda } ^ { \mathrm { H } } \hat { r } _ { \lambda } + \mathrm { t r } ( \hat { \pmb { \Phi } } \hat { \pmb { C } } _ { \alpha } \hat { \pmb { \Phi } } ^ { \mathrm { H } } ) + \mathrm { t r } ( \hat { U } \hat { \pmb { \Psi } } \hat { \pmb { C } } _ { \beta } \hat { \pmb { \Psi } } ^ { \mathrm { H } } \hat { U } ^ { \mathrm { H } } ) } . } \end{array}\tag{65}
$$

For the hyper-parameters of the Gamma distribution we let $e _ { 0 } = f _ { 0 } = 0$ that is the non-informative Jeffery’s improper hyper-prior.

## C. Estimations of Parameters

The cost function for the object channel dispersion parameters ζ is $Z _ { \alpha }$ as in (45). For optimization, the equivalent log $Z _ { \alpha }$ will be used. The expectation term is identical to the solution for $q _ { \alpha } .$ , except that $\Phi ( \zeta )$ -dependent terms are to be explicitly considered. The result in (56) contains all these non-constant terms. Then, marginalization of α integrates out $\mathrm { C N } ( \alpha | \hat { \alpha } , \hat { C } _ { \alpha } )$ to one as it is a valid PDF. I.e.,

$$
\begin{array} { c } { { \log Z _ { \alpha } \propto ^ { \mathrm { e } } \log \displaystyle \int \exp \Big ( \log \mathrm { C N } ( \alpha | \hat { \alpha } , \hat { C } _ { \alpha } ) + \log | \hat { C } _ { \alpha } | } } \\ { { + \hat { \lambda } ^ { 2 } \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \hat { C } _ { \alpha } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha } \Big ) \mathrm { d } \alpha } } \\ { { = \log | \hat { C } _ { \alpha } | + \hat { \lambda } ^ { 2 } \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \hat { C } _ { \alpha } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha } } } \\ { { + \log \displaystyle \int \mathrm { C N } ( \alpha | \hat { \alpha } , \hat { C } _ { \alpha } ) \mathrm { d } \alpha } } \end{array}\tag{66}
$$

and hence the result

$$
\hat { \zeta } = \underset { \zeta } { \arg \operatorname* { m a x } } \Big ( \log \vert \hat { C } _ { \alpha } ( \zeta ) \vert + \hat { \lambda } ^ { 2 } \hat { r } _ { \alpha } ^ { \mathrm { H } } \Phi ( \zeta ) \hat { C } _ { \alpha } ( \zeta ) \Phi ^ { \mathrm { H } } ( \zeta ) \hat { r } _ { \alpha } \Big )\tag{67}
$$

where we explicitly noted all ζ-dependencies including inside the covariance matrix estimate $\hat { C } _ { \alpha } ( \zeta )$ . This result can be recast to express the cost function for the parameters of a single component $\zeta _ { l }$ with all other parameters fixed. We order the components so that the index l is last and denote all others by <sup>¯</sup>l, i.e., $\Phi ( \zeta ) = \Phi ( [ \zeta _ { \bar { l } } \zeta _ { l } ] ^ { \mathrm { T } } ) = [ \Phi _ { \bar { l } } \phi _ { l } ]$ . Then, $\hat { C } _ { \alpha }$ can be written as the block matrix

$$
\hat { C } _ { \alpha } = \left[ \begin{array} { c c } { { \hat { C } _ { \alpha , \bar { l } } ^ { - 1 } } } & { { \hat { \lambda } \Phi _ { \bar { l } } ^ { \mathrm { H } } \phi _ { l } } } \\ { { \hat { \lambda } \phi _ { l } ^ { \mathrm { H } } \Phi _ { \bar { l } } } } & { { \hat { c } _ { \alpha , l } ^ { - 1 } } } \end{array} \right] ^ { - 1 }\tag{68}
$$

$$
\mathbf { \Sigma } = \left[ \begin{array} { c c } { \hat { C } _ { \alpha , \bar { l } } + } & { - \hat { \lambda } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } \phi _ { l } \hat { c } _ { \alpha , l } ^ { \prime } } \\ { \hat { \lambda } ^ { 2 } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } \phi _ { l } \hat { c } _ { \alpha , l } ^ { \prime } \phi _ { l } ^ { \mathrm { H } } \Phi _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } } \\ { - \hat { \lambda } \hat { c } _ { \alpha , l } ^ { \prime } \phi _ { l } ^ { \mathrm { H } } \Phi _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } } & { \hat { c } _ { \alpha , l } ^ { \prime } } \end{array} \right]
$$

where we have applied the formula for block matrix inversion and defined $\begin{array} { r l r } { \hat { C } _ { \alpha , \bar { l } } ~ = } & { { } \big ( \hat { \lambda } \Phi _ { \bar { l } } ^ { \mathrm { H } } \Phi _ { \bar { l } } + \hat { \Gamma } _ { \alpha , \bar { l } } \big ) ^ { - 1 } , ~ \hat { c } _ { \alpha , l } } & { { } = } & { } \end{array}$ $\big ( \hat { \lambda } \phi _ { l } ^ { \mathrm { H } } \phi _ { l } + \hat { \gamma } _ { \alpha , l } \big ) ^ { - 1 }$ and $\hat { c } _ { \alpha , l } ^ { \prime } = \left( \hat { c } _ { \alpha , l } ^ { - 1 } - \hat { \lambda } ^ { 2 } \phi _ { l } ^ { \mathrm { H } } \pmb { \Phi } _ { \bar { l } } \pmb { \hat { C } } _ { \alpha , \bar { l } } \pmb { \Phi } _ { \bar { l } } ^ { \mathrm { H } } \phi _ { l } \right) ^ { - 1 }$

In (67), for the log-determinant of the block matrix we simply obtain log $| \hat { C } _ { \alpha } | = \log | \hat { c } _ { \alpha , l } ^ { \prime } | + \log | \hat { C } _ { \alpha , \bar { l } } | . \hat { C } _ { \alpha , \bar { l } } $ is independent of $\zeta _ { l }$ and hence can be neglected in the resulting cost function. Concerning the other term of (67), noting that

$$
\begin{array} { r l r } {  { \Phi \hat { C } _ { \alpha } \Phi ^ { \mathrm { H } } = \Phi _ { l } \hat { C } _ { \alpha , l } \Phi _ { l } ^ { \mathrm { H } } + \hat { \lambda } ^ { 2 } \hat { c } _ { \alpha , l } ^ { \prime } \Phi _ { l } \hat { C } _ { \alpha , l } \Phi _ { l } ^ { \mathrm { H } } \phi _ { l } \Phi _ { l } ^ { \mathrm { H } } \Phi _ { l } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } } } \\ & { } & { ~ - 2 \Re \big ( \hat { \lambda } \hat { c } _ { \alpha , l } ^ { \prime } \Phi _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } \phi _ { l } \phi _ { l } ^ { \mathrm { H } } \big ) + \phi _ { l } \hat { c } _ { \alpha , l } ^ { \prime } \phi _ { l } ^ { \mathrm { H } } } \\ & { } & { = \Phi _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } } \\ & { } & { ~ + \big ( \hat { \lambda } \Phi _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } - \mathbf { I } \big ) ^ { \mathrm { H } } \phi _ { l } \hat { c } _ { \alpha , l } ^ { \prime } \phi _ { l } ^ { \mathrm { H } } \big ( \hat { \lambda } \Phi _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } - \mathbf { I } \big ) } \end{array}
$$

with the first term being a constant, we finally arrive at the result

$$
\begin{array} { r l } & { \hat { \zeta } _ { l } = \underset { \zeta _ { l } } { \arg \operatorname* { m a x } } \bigg ( \log \vert \hat { c } _ { \alpha , l } ^ { \prime } ( \zeta _ { l } ) \vert } \\ & { \qquad + \left. \hat { \lambda } ^ { 2 } \hat { c } _ { \alpha , l } ^ { \prime } ( \zeta _ { l } ) \vert \vert \phi _ { l } ^ { \mathrm { H } } ( \zeta _ { l } ) ( \hat { \lambda } \Phi _ { l } \hat { C } _ { \alpha , \bar { l } } \Phi _ { \bar { l } } ^ { \mathrm { H } } - \mathbf { I } ) \hat { r } _ { \alpha } \vert \right. ^ { 2 } \bigg ) . } \end{array}\tag{70}
$$

For the interference chirp parameter estimates the derivations are analogous to (67) for every ramp independently, i.e.,

$$
\begin{array} { r l } & { \hat { \pmb { \theta } } = \underset { \pmb { \theta } } { \arg \operatorname* { m a x } } \bigg ( \log \vert \hat { C } _ { \beta } ( \pmb { \theta } ) \vert } \\ & { \qquad + \hat { \lambda } ^ { 2 } \hat { r } _ { \beta } ^ { \mathrm { H } } \pmb { U } ( \pmb { \theta } ) \hat { \Psi } \hat { C } _ { \beta } ( \pmb { \theta } ) \hat { \Psi } ^ { \mathrm { H } } \pmb { U } ( \pmb { \theta } ) ^ { \mathrm { H } } \hat { r } _ { \beta } \bigg ) } \end{array}\tag{71}
$$

where the dependence of variables on the ramp index $p$ has been left out to reduce notational clutter.

## D. Fast Updates of Component Precisions

As discussed in Section III-C, for our proposed algorithm we also apply the “fast update rule” for components as derived in [59]. Applying (21) yields

$$
\log q _ { \gamma _ { \alpha , l } } \propto ^ { \mathrm e } a _ { 0 } \log \gamma _ { \alpha , l } - \bigl ( b _ { 0 } + \bigl \langle \left| \alpha _ { l } \right| ^ { 2 } \bigr \rangle _ { q _ { \alpha } } \bigr ) \gamma _ { \alpha , l }\tag{72}
$$

$$
\propto ^ { \mathrm { e } } a _ { 0 } \log \gamma _ { \alpha , l } - ( b _ { 0 } + | \hat { \alpha } _ { l } | ^ { 2 } + \hat { C } _ { \alpha } [ l , l ] ) \gamma _ { \alpha , l }\tag{73}
$$

which leads to the solution

$$
\begin{array} { r } { q ( \gamma _ { \alpha , l } ) = \mathbf { G a } ( \gamma _ { \alpha , l } | a _ { l } , b _ { l } ) } \end{array}\tag{74}
$$

$$
\hat { \gamma } _ { \alpha , l } = \frac { a _ { l } } { b _ { l } } = \frac { a _ { 0 } + 1 } { b _ { 0 } + \left( \left| \hat { \alpha } _ { l } \right| ^ { 2 } + \hat { C } _ { \alpha } [ l , l ] \right) }\tag{75}
$$

where we take $a _ { 0 } = b _ { 0 } = 0$ . However, we can further investigate the behavior of this implicit equation when repeatedly updating $q _ { \alpha }$ and $q _ { \gamma _ { \alpha , l } }$ . We insert (58) into (75) and recast the resulting terms to “isolate” the l-th component as already shown for the derivation of (70). I.e.,

$$
\begin{array} { r l } & { \hat { \gamma } _ { \alpha , l } ^ { - 1 } = \big ( \hat { \lambda } ^ { 2 } \hat { C } _ { \alpha } \hat { \Phi } ^ { \mathrm { H } } \hat { r } _ { \alpha } \hat { r } _ { \alpha } ^ { \mathrm { H } } \hat { \Phi } \hat { C } _ { \alpha } ^ { \mathrm { H } } + \hat { C } _ { \alpha } \big ) [ l , l ] } \\ & { \quad \quad \quad = \hat { \lambda } ^ { 2 } | c _ { \alpha , l } ^ { \prime } \hat { \phi } _ { l } ^ { \mathrm { H } } \hat { r } _ { \alpha } - \lambda c _ { \alpha , l } ^ { \prime } \hat { \phi } _ { l } ^ { \mathrm { H } } \hat { \Phi } _ { \bar { l } } \hat { C } _ { \alpha , \bar { l } } \hat { \Phi } _ { \bar { l } } ^ { \mathrm { H } } \hat { r } _ { \alpha } | ^ { 2 } + c _ { \alpha , l } ^ { \prime } } \end{array}\tag{76}
$$

and by defining (23) and (24), and hence $c _ { \alpha , l } ^ { \prime } = \hat { \gamma } _ { \alpha , l } ^ { - 1 } \rho _ { l } / ( \hat { \gamma } _ { \alpha , l } ^ { - 1 } +$ $\rho _ { l } )$ , this can be further rewritten as

$$
\begin{array} { r l } & { \hat { \gamma } _ { \alpha , l } ^ { - 1 } = { | c _ { \alpha , l } ^ { \prime } | } ^ { 2 } \rho _ { l } ^ { - 2 } \omega _ { l } ^ { 2 } + c _ { \alpha , l } ^ { \prime } } \\ & { \qquad = \frac { \hat { \gamma } _ { \alpha , l } ^ { - 2 } \left( \omega _ { l } ^ { 2 } + \rho _ { l } \right) + \hat { \gamma } _ { \alpha , l } ^ { - 1 } \rho _ { l } ^ { 2 } } { { | \hat { \gamma } _ { \alpha , l } ^ { - 1 } + \rho _ { l } | } ^ { 2 } } . } \end{array}\tag{77}
$$

By analyzing (77) in the context of iterative updates as a rational map, it can be found that its stationary points are located at $\{ 0 , \omega _ { l } ^ { 2 } - \rho _ { l } \}$ . It can furthermore be proven that the non-zero stationary point is reached (i.e., the estimate $\hat { \gamma } _ { \alpha , l }$ converges) if and only if $\rho _ { l } / \omega _ { l } ^ { 2 } \ > \ T$ with $T \ = \ 1$ which leads to the thresholding scheme with threshold T (see Algorithm 4). For a detailed discussion see [59], [83]. The component precisions of the interference channel $\hat { \gamma } _ { \beta , k }$ can be found in a similar manner.

## APPENDIX CMEASUREMENT OF INTERFERENCE

As introduced in Section IV-D, a measurement scheme whereby a separate interference signal is made available was devised. The parameters of the interference measurement can be found as Int. Measurement in Table I. The measurement took place in an indoor office with the victim and interfering sensors on a desk opposite each other. Crucially, the scenario was therefore completely static with no movement of objects. First, the location and duration of the interference bursts received by the victim radar were identified manually. The static object signal could then be estimated by taking the sample mean of the non-interfered data. This estimate was subtracted from the measured signal, approximately removing the object signal, leaving interference and measurement noise. Then, the time-limited interference bursts were cut out to exclude irrelevant noise-only sections.

In Section II, the effect of the AAF in the sensor hardware on the resulting interference burst was discussed (see the term $\bar { G } ( f )$ in (7)). This is typically assumed to be known to some precision in the application by the algorithm designers of an automotive radar manufacturer. Section IV-B investigated the resilience of the proposed algorithm to a minor inaccuracy of this kind in the inference model. However, because the used hardware was a radar evaluation board from an external supplier, no details on the transfer function of the system was accessible to the authors. This can lead to a major model error. To mitigate this, the signal was additionally filtered digitally with a filter whose magnitude response dominates that of the sensor hardware. The concatenation of a high- and a lowpass was applied, both being 8-th order Butterworth filters with respective cut-off frequencies of 0.5 MHz and 5 MHz. The known response of this digital filter chain was then used in our inference model, noting that this still constitutes a rather significant model error. Finally, the interference signal prepared in this way was added onto the measurement from Obj. Measurement, yielding our test radar signal.

## REFERENCES

[1] M. Kunert, H. Meinel, C. Fischer, and M. Ahrholdt, “D16.1 - Report on interference density increase by market penetration forecast,” the MOSARIM Consortium, Tech. Rep., 2010.

[2] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: modulation schemes and interference mitigation,” IEEE Microw. Mag., vol. 20, no. 9, pp. 58–72, Sep. 2019.

[3] M. Kunert, “The EU project MOSARIM: a general overview of project objectives and conducted work,” in Proc. 9th European Radar Conf. (EuRAD), Oct. 2012, pp. 1–5.

[4] F. Borngraber, A. John, W. S¨ orgel, R. K¨ orber, T. Vogler, E. Miel,¨ F. Torres, M. Kritzner, H. Golz, J. Moss, M. Behrens, A. Ossowska, L. T.¨ Torres, A. Giere, C. Waldschmidt, and T. Zwick, “Gesamtbewertung und Empfehlung fur Standardisierung,” the IMIKO Consortium, Deliverable¨ AP09, May 2022, in German.

[5] M. Hischke, “Collision warning radar interference,” in Proc. IEEE Intell. Veh. Symp., 1995, pp. 13–18.

[6] B. E. Tullsson, “Topics in FMCW radar disturbance suppression,” in Proc. Radar 97 (Conf. Publ. No. 449), 1997, pp. 1–5.

[7] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, 2007.

[8] A. Al-Hourani, R. J. Evans, S. Kandeepan, B. Moran, and H. Eltom, “Stochastic geometry methods for modeling automotive radar interference,” IEEE Trans. Intell. Transp. Syst., pp. 1–11, 2017.

[9] L. L. T. Torres and C. Waldschmidt, “Analysis of automotive radar interference in complex traffic scenarios using graph theory,” in Proc. 23rd Int. Radar Symp. (IRS), Sep. 2022, pp. 269–274.

[10] T. Schipper, S. Prophet, M. Harter, L. Zwirello, and T. Zwick, “Simulative prediction of the interference potential between radars in common road scenarios,” IEEE Trans. Electromagn. Compat., vol. 57, no. 3, pp. 322–328, 2015.

[11] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical investigation of non-coherent mutual FMCW radar interference,” in Proc. 15th European Radar Conf. (EuRAD), 2018, pp. 71–74.

[12] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, 2018.

[13] A. Bourdoux and M. Bauduin, “PMCW waveform cross-correlation characterization and interference mitigation,” in Proc. 17th European Radar Conf. (EuRAD), Jan. 2021, pp. 164–167.

[14] B. Schweizer, C. Knill, D. Werbunat, S. Stephany, and C. Waldschmidt, “Mutual interference of automotive OFDM radars — analysis and countermeasures,” IEEE J. Microw., vol. 1, no. 4, pp. 950–961, 2021.

[15] M. Rameez, M. Dahl, and M. I. Pettersson, “Experimental evaluation of adaptive beamforming for automotive radar interference suppression,” in Proc. 2020 IEEE Radio and Wireless Symp. (RWS), Jan. 2020, pp. 183–186.

[16] A. Ossowska, L. Sit, S. Manchala, T. Vogler, K. Krupinski, and U. Luebbert, “IMIKO-Radar project: laboratory interference measurements of automotive radar sensors,” in Proc. 21st Int. Radar Symp. (IRS), Oct. 2020, pp. 334–338.

[17] L. L. T. Torres, M. Steiner, and C. Waldschmidt, “Channel influence for the analysis of interferences between automotive radars,” in Proc. 17th European Radar Conf. (EuRAD), 2021, pp. 266–269.

[18] N. Cardona, J. S. Romero, W. Yang, and J. Li, “Integrating the sensing and radio communications channel modelling from radar mutual interference,” in Proc. IEEE Int. Conf. Acoustics, Speech and Signal Process. (ICASSP), Jun. 2023, pp. 1–5.

[19] G. Hakobyan, K. Armanious, and B. Yang, “Interference-Aware cognitive radar: a remedy to the automotive interference problem,” IEEE Trans. Aerosp. Electron. Syst., vol. 56, no. 3, pp. 2326–2339, 2020.

[20] L. L. Tovar Torres, T. Grebner, and C. Waldschmidt, “Automotive radar interference avoidance strategies for complex traffic scenarios,” in Proc. IEEE Radar Conf. (RadarConf23), May 2023, pp. 1–6.

[21] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sensing, Commun. Networking (SECON), 2016, pp. 1–9.

[22] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416– 429, 2021.

[23] C. Fischer, H. L. Blocher, J. Dickmann, and W. Menzel, “Robust¨ detection and mitigation of mutual interference in automotive radar,” in Proc. 16th Int Radar Symp. (IRS), Jun. 2015, pp. 143–148.

[24] Z. Liu, W. Lu, J. Wu, S. Yang, and G. Li, “A PELT-KCN algorithm for FMCW radar interference suppression based on signal reconstruction,” IEEE Access, vol. 8, pp. 45 108–45 118, 2020.

[25] T. Pernstal, J. Degerman, H. Brostr˚ om, V. T. Vu, and M. I. Pettersson,¨ “GIP test for automotive FMCW interference detection and suppression,” in Proc. IEEE Radar Conf. (RadarConf20), Sep. 2020, pp. 1–6.

[26] T. Shimura, M. Umehira, Y. Watanabe, X. Wang, and S. Takeda, “An advanced wideband interference suppression technique using envelope detection and sorting for automotive FMCW radar,” in Proc. IEEE Radar Conf. (RadarConf22), Mar. 2022, pp. 1–6.

[27] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, 2021.

[28] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[29] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. 14th European Radar Conf. (EuRAD), 2017, pp. 90–93.

[30] S. Chen, J. Taghia, U. Kuhnau, T. Fei, F. Gr¨ unhaupt, and R. Martin,¨ “Automotive radar interference reduction based on sparse Bayesian learning,” in Proc. IEEE Radar Conf. (RadarConf20), Sep. 2020, pp. 1–6.

[31] J. Wang, M. Ding, and A. Yarovoy, “Matrix-Pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Feb. 2021.

[32] J. Bechter, A. Demirlika, P. Hugler, F. Roos, and C. Waldschmidt, “Blind¨ adaptive beamforming for automotive radar interference suppression,” in Proc. 19th Int. Radar Symp. (IRS), Jun. 2018, pp. 1–10.

[33] M. Rameez, M. Dahl, and M. I. Pettersson, “Adaptive digital beamforming for interference suppression in automotive FMCW radars,” in Proc. IEEE Radar Conf. (RadarConf18), 2018, pp. 252–256.

[34] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[35] P. Wang, X. Yin, J. Rodr´ıguez-Pineiro, Z. Chen, P. Zhu, and G. Li, “A˜ dual-recursive-least-squares algorithm for automotive radar interference suppression,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 10, pp. 10 603–10 617, 2023.

[36] M. Rameez, M. I. Pettersson, and M. Dahl, “Interference compression and mitigation for automotive FMCW radar systems,” IEEE Sensors J., vol. 22, no. 20, pp. 19 739–19 749, Oct. 2022.

[37] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Slow-Time mitigation of mutual interference in chirp sequence radar,” in Proc. IEEE MTT-S Int. Conf. Microw. for Intell. Mobility (ICMIM), Nov. 2020, pp. 1–4.

[38] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in Proc. IEEE Int. Symp. Circuits and Syst. (ISCAS), 2018, pp. 1–4.

[39] R. Muja, A. Anghel, R. Cacoveanu, and S. Ciochina, “Interference mitigation in FMCW automotive radars using the short-time Fourier transform and L-statistics,” in Proc. IEEE Radar Conf. (RadarConf22), Mar. 2022, pp. 1–6.

[40] J. Wu, S. Yang, W. Lu, and Z. Liu, “Iterative modified threshold method based on EMD for interference suppression in FMCW radars,” IET Radar, Sonar & Navigation, vol. 14, no. 8, pp. 1219–1228, 2020.

[41] T. Oyedare, V. K. Shah, D. J. Jakubisin, and J. H. Reed, “Interference suppression using deep learning: current approaches and open challenges,” IEEE Access, vol. 10, pp. 66 238–66 266, 2022.

[42] J. Hille, D. Auge, C. Grassmann, and A. Knoll, “FMCW radar2radar interference detection with a recurrent neural network,” in Proc. IEEE Radar Conf. (RadarConf22), Mar. 2022, pp. 1–6.

[43] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resource-Efficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021.

[44] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ radar interference mitigation using a convolutional autoencoder,” in Proc. 2020 IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320.

[45] C. Oswald, M. Toth, P. Meissner, and F. Pernkopf, “End-to-End training of neural networks for automotive radar interference mitigation,” in Proc. IEEE Int. Radar Conf. (RADAR), Nov. 2023, pp. 1–6.

[46] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in Proc. Int. Radar Symp., 2017, pp. 1–10.

[47] A. Correas-Serrano and M. A. Gonzalez-Huici, “Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation,” in Proc. IEEE MTT-S Int. Conf. Microw. for Intell. Mobility (ICMIM), Apr. 2019, pp. 1–4.

[48] L. L. T. Torres, T. Grebner, D. Werbunat, and C. Waldschmidt, “Automotive radar interference mitigation by subtraction of the interference component,” IEEE Microw. Wireless Technology Lett., vol. 33, no. 9, pp. 1397–1400, 2023.

[49] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[50] J.-L. Starck, M. Elad, and D. Donoho, “Redundant multiscale transforms and their application for morphological component separation,” Advances in Imaging and Electron Physics, vol. 132, pp. 287–348, Jan. 2004.

[51] S. S. Chen, D. L. Donoho, and M. A. Saunders, “Atomic decomposition by basis pursuit,” SIAM Review, vol. 43, no. 1, pp. 129–159, 2001.

[52] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270– 5283, 2021.

[53] Z. Xu, “Bi-Level \$l 1\$ optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, 2023.

[54] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[55] Y. Wang, Y. Huang, C. Wen, X. Zhou, J. Liu, and W. Hong, “Mutual interference mitigation for automotive FMCW radar with time and frequency domain decomposition,” IEEE Trans. Microw. Theory Techn., vol. 71, no. 11, pp. 5028–5044, 2023.

[56] S. Grebien, E. Leitinger, K. Witrisal, and B. H. Fleury, “Super-resolution estimation of UWB channels including the dense component – An SBLinspired approach,” IEEE Trans. Wireless Commun., Feb. 2024.

[57] M. Tipping, “The relevance vector machine,” in Proc. Advances in Neural Inf. Proc. Syst., S. Solla, T. Leen, and K. Muller, Eds., vol. 12.¨ MIT Press, 1999.

[58] M. E. Tipping and A. C. Faul, “Fast marginal likelihood maximisation for sparse Bayesian models,” in Proc. 9th Int. Workshop on Artificial Intelligence and Statistics, ser. Proceedings of Machine Learning Research, C. M. Bishop and B. J. Frey, Eds., vol. R4. PMLR, 03–06 jan 2003, pp. 276–283, reissued by PMLR on 01 April 2021.

[59] D. Shutin, T. Buchgraber, S. R. Kulkarni, and H. V. Poor, “Fast variational sparse Bayesian learning with automatic relevance determination for superimposed signals,” IEEE Trans. Signal Process., vol. 59, no. 12, pp. 6257–6261, Dec. 2011.

[60] D. Shutin, W. Wand, and T. Jost, “Incremental sparse Bayesian learning for parameter estimation of superimposed signals,” in Proc. 10th Int. Conf. Sampling Theory and Application, Jul. 2013, pp. 513–516.

[61] D. P. Wipf, B. D. Rao, and S. Nagarajan, “Latent variable Bayesian models for promoting sparsity,” IEEE Trans. Image Process., vol. 57, no. 9, pp. 6236–6255, Sep. 2011.

[62] D. G. Tzikas, A. C. Likas, and N. P. Galatsanos, “The variational approximation for Bayesian inference,” IEEE Signal Process. Mag., vol. 25, no. 6, pp. 131–146, Nov. 2008.

[63] M.-A. Badiu, T. L. Hansen, and B. H. Fleury, “Variational Bayesian inference of line spectra,” IEEE Trans. Signal Process., vol. 65, no. 9, pp. 2247–2261, May 2017.

[64] J. Moderl, F. Pernkopf, K. Witrisal, and E. Leitinger, “Variational¨ inference of structured line spectra exploiting group-sparsity,” ArXiv e-prints, 2023. [Online]. Available: https://arxiv.org/abs/2303.03017

[65] C. M. Bishop, Pattern Recognition and Machine Learning, 8th ed., M. Jordan, J. Kleinberg, and B. Scholkopf, Eds. Springer-Verlag, 2009.¨

[66] T. L. Hansen, B. H. Fleury, and B. D. Rao, “Superfast line spectral estimation,” IEEE Trans. Signal Process., vol. 66, no. 10, pp. 2511– 2526, May 2018.

[67] E. Leitinger, S. Grebien, B. Fleury, and K. Witrisal, “Detection and estimation of a spectral line in MIMO systems,” in Proc. 54th Asilomar Conf. Signals, Syst. and Computers, Nov. 2020, pp. 1090–1095.

[68] S. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory. Prentice Hall, 1993.

[69] M. A. Richards, Fundamentals of Radar Signal Processing, 2nd ed. McGraw-Hill Education, 2014.

[70] T. Schipper, T. Mahler, M. Harter, L. Reichardt, and T. Zwick, “An estimation of the operating range for frequency modulated radars in the presence of interference,” Proc. 10th European Radar Conf. (EuRAD), pp. 227–230, 2013.

[71] T. Schipper, “Simulation of effects and impact of environment, traffic participants and infrastructure,” the MOSARIM Consortium, Tech. Rep., 2012.

[72] A. S. Rahmathullah, A. F. Garcia-Fernandez, and L. Svensson, “Generalized optimal sub-pattern assignment metric,” in Proc. 20th Int. Conf. on Information Fusion (FUSION), Jul. 2017, pp. 1–8.

[73] J.-L. Starck, F. Murtagh, and J. M. Fadili, Sparse Image and Signal Processing: wavelets, curvelets, morphological diversity. Cambridge University Press, 2010.

[74] M. Toth, J. Rock, P. Meissner, A. Melzer, and K. Witrisal, “Analysis of automotive radar interference mitigation for real-world environments,” in Proc. 17th European Radar Conf. (EuRAD), 2021, pp. 176–179.

[75] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc. IEEE Int. Radar Conf. (RADAR), 2020, pp. 624–629.

[76] L. A. Lopez-Valc ´ arcel, M. Garc ´ ´ıa Sanchez, F. Fioranelli, and O. A.´ Krasnov, “Raw ADC data from FMCW radar at 77 GHz with interference,” 2023. [Online]. Available: https://dx.doi.org/10.21227/ e47t-p857

[77] ——, “An MTI-like approach for interference mitigation in FMCW radar systems,” IEEE Trans. Aerosp. Electron. Syst., vol. 60, no. 2, pp. 1985–2000, 2024.

[78] A. Stove, “Linear FMCW radar techniques,” IEE Proc. F Radar Signal Process., vol. 139, no. 5, p. 343, 1992.

[79] F. Hlawatsch and G. Matz, Eds., Wireless Communications Over Rapidly Time-Varying Channels. Elsevier, 2011.

[80] W. J. Caputi, “Stretch: a time-transformation technique,” IEEE Trans Aerosp. Electron. Syst., vol. 7, no. 2, pp. 269–278, Mar. 1971.

[81] D. Wipf, “Sparse estimation with structured dictionaries,” in Proc. Advances in Neural Inf. Proc. Syst., vol. 24, 2011.

[82] J. Moderl, F. Pernkopf, K. Witrisal, and E. Leitinger, “Fast variational¨ block-sparse bayesian learning,” ArXiv e-prints, 2023. [Online]. Available: https://arxiv.org/abs/2306.00442

[83] T. Buchgraber, “Variational sparse Bayesian learning: centralized and distributed processing,” Ph.D. dissertation, Graz University of Technology, 2013.