# Interference Mitigation for FMCW Radar With Sparse and Low-Rank Hankel Matrix Decomposition

Jianping Wang, Member, IEEE, Min Ding, and Alexander Yarovoy, Fellow, IEEE

Abstract—In this paper, the interference mitigation for Frequency Modulated Continuous Wave (FMCW) radar system with a dechirping receiver is investigated. After dechirping operation, the scattered signals from targets result in beat signals, i.e., the sum of complex exponentials while the interferences lead to chirp-like short pulses. Taking advantage of these different time and frequency features between the useful signals and the interferences, the interference mitigation is formulated as an optimization problem: a sparse and low-rank decomposition of a Hankel matrix constructed by lifting the measurements. Then, an iterative optimization algorithm is proposed to tackle it by exploiting the Alternating Direction of Multipliers (ADMM) scheme. Compared to the existing methods, the proposed approach does not need to detect the interference and also improves the estimation accuracy of the separated useful signals. Both numerical simulations with point-like targets and experiment results with distributed targets (i.e., raindrops) are presented to demonstrate and verify its performance. The results show that the proposed approach is generally applicable for interference mitigation in both stationary and moving target scenarios.

Index Terms—FMCW radar, interference mitigation, sparsity, low-rank, Hankel matrix.

## I. INTRODUCTION

W <sup>IDE</sup> <sup>spread</sup> <sup>of</sup> <sup>Frequency</sup> <sup>Modulated</sup> <sup>Continuous</sup> <sup>Wave</sup>(FMCW) radar (automotive radar, vital sign observation, intelligent light, etc.) has raised serious concerns about their mutual interference. It was shown that in FMCW radar external interference increases overall clutter level, might result in appearance of ghost targets, masks weak targets and disturbs target returns. Numerous approaches have been proposed to mitigate the interference. However, desired level of interference suppression at given signal processing costs has not been achieved.

In the literature, the interference mitigation (IM) of the FMCW radar systems is generally tackled through two ways: (1) system/signal (i.e., antenna array, waveform, etc) design methods [1]–[10] and (2) signal processing approaches [11]– [24]. The system/signal design related methods generally require that the radar system have the capability for agile waveform modulation, new radar architecture, spectrum sensing module or a coordination unit, etc.; thus, the radar system has to be modified or redesigned and the system complexity will increase. On the other hand, the signal processing approaches tackle the interference mitigation problem through post-processing, which could be readily used for the existing FMCW radar systems. The work presented in this paper falls into the latter group. The signal processing approaches to interference mitigation of radar system can be categorized into three classes: filtering approaches [11]– [13], [25], interference nulling and reconstruction methods [14]–[17], and signal separation approaches [18]–[24]. The filtering approaches usually exploit different distributions of interferences and useful signals in a specific domain (i.e., time, frequency or space) and design a proper filter to suppress the interferences. They work well for some fixed or slowly variant interferences. For complex scenarios, the interference could be transient or change rapidly between different sweeps. Then adaptive filtering could be utilized [13], which uses a reference input to generate the correlated interference component for interference mitigation. However, it is not easy to find a proper reference input signal in practice; thus, its performance of interference mitigation is of no guarantee.

The interference nulling and reconstruction methods is to first cut out the contaminated signal samples [14] and then reconstruct the signals in the cut-out region [15], [17]. To these methods, precise detection of the interference and accurate reconstruction of the cut-out signal samples are the key steps. As the amplitudes of interferences and the targets’ signals in the low-pass filter output of the FMCW radar systems are generally unknown, it makes the detection of the interference a challenging problem. If the interferences cannot be precisely detected, they will be removed partially, or the useful signals are excessively eliminated [16]. Moreover, even if the interferences are detected properly, the targets’ signals contaminated by the interferences are unavoidably to be cut out, resulting in the power loss of the targets’ signals. To fix this problem, model-based methods are proposed to reconstruct the useful signals in the cut-out region by using the Burg method [15] and Matrix pencil approach [17]. However, with the increase of the proportion of the contaminated samples in the full measurements, the accuracy of the reconstructed signals with these approaches would decrease significantly .

On the other hand, signal separation approaches tackle the interference mitigation by exploiting the sparsity of the interferences or the useful signals in some bases (or domains), which circumvents explicit detection of interferences.

For example, for ultra-wideband radar systems the useful signals of targets could exhibit as sparse spikes in time while the Radio Frequency Interferences (RFI) are generally sparse in the frequency domain [19]. For FMCW radars, the beat signals could be sparse in frequency domain. By contrast, the interferences after dechirping and anti-aliasing low-pass filtering operations generally exhibit as chirp-like signals which could be sparse in the time-, frequency- or time-frequency domain in various scenarios. To exploit the sparse representations of beat signals in the frequency domain and of the interferences in the time-frequency domain, the Discrete Fourier Transform (DFT) bases and the Short-Time Fourier Transform (STFT) bases, which are regular grids in the corresponding domains, are generally employed and the Split Augmented Lagrangian Shrinkage Algorithm (SALSA) could be used to solve the related morphological component analysis problem [18]. Although these representations are attractive for efficient implementation of the SALSA-based interference mitigation method by taking advantage of the Fast Fourier Transform (FFT), the inherent so-called “off-grid” problem, i.e., the mismatch between true frequency (or timefrequency) components with the discrete bases, could lead to less sparse representation and consequently degrade the interference mitigation performance.

Recently, transient interference or RFI suppression has also been tackled by formulating as a Robust Principle Component Analysis (RPCA) problem [26], [27], where a matrix constructed by the measurements is decomposed as the sum of a sparse matrix and a low-rank one [20]–[23]. The formulated RPCA problems are solved by using the singular valued thresholding (SVT) algorithm [20], [22], reweighted nuclear norm or reweighted Frobenius norm [23]. In these approaches, the operations are directly involved in the singular values of the matrix constructed with the signals. So the singular value decomposition (SVD) is required in these approaches, which is generally very computationally expensive, especially for large matrices. Moreover, as the signal matrix formed by the measurements in multiple pulse repetition intervals (PRI) for transient interference mitigation for synthetic aperture radar systems are typically not structured, the developed approaches scarcely exploit the structures of the matrices.

To circumvent the “off-grid” problem of traditional signal separation methods and heavy computational load of the existing RPCA-based approaches, we propose a novel Interference Mitigation approach for FMCW radars with SPArse and low-Rank HanKeL matrix dEcomposition (IM-SPARKLE). For the proposed approach, we formulate the interference mitigation for FMCW radars as a RPCA-like problem by exploiting the time sparsity of interferences and spectral sparsity of useful signals. Inspired by the matrix pencil approach for exponential component estimation [17], [28], the spectral sparsity of the useful signal is exploited by minimizing the rank of a Hankel matrix constructed with its samples in the time domain. The rank minimization problem is generally relaxed as a nuclear norm minimization problem. To circumvent the computationally expensive SVD used for the nuclear norm minimization, we utilized a Frobenius norm factorization [29]–[31] to relax the nuclear norm minimization; thus, much more efficient algorithm is developed compared to the traditional RPCAbased IM approaches. In addition, our formulation directly imposes the sparsiy of interferences on its time-domain samples and circumvents the nonuniform weighting effect on different samples when a Hankel matrix of interference components is used. Thus, naturally there is no need to use the reweighting operations as in [23].

The rest of the paper is organized as follows. In section II, the problem formulation of the interference mitigation as a signal separation problem is presented, which results in an optimization problem of a sparse and low rank decomposition of a Hankel matrix. Then, the proposed algorithm to solve this problem is provided in detail in section III. After that, section IV and section V show both numerical results and experimental measurements to demonstrate the performance of the proposed IM approach for FMCW radar systems. Finally, conclusions are drawn in section VI.

## II. PROBLEM FORMULATION

For an interference-contaminated FMCW radar system, target responses are received together with interferences. The signal acquired with a deramping receiver can be expressed as

$$
y ( t ) = x ( t ) + i ( t ) + n ( t ) ,\tag{1}
$$

where $\begin{array} { r } { \begin{array} { r c l } { x ( t ) } & { = } & { \sum _ { i = 1 } ^ { M } \sigma _ { i } \exp \left( - j 2 \pi f _ { b , i } t \right) } \end{array} } \end{array}$ is the beat signal of targets with complex amplitudes $\sigma _ { i }$ and beat frequencies $f _ { b , i }$ <sub>i</sub> after deramping operation. i(t) is the interference, which generally has a short duration after deramping and low-pass filtering operations and exhibits as a sum of chirp-like signals [17]. n(t) represents the additive white complex Gaussian noise (AWGN) and measurement errors. For the discrete signals sampled with intervals $\Delta t , ( 1 )$ can be rewritten as

$$
y [ k ] = x [ k ] + i [ k ] + n [ k ]\tag{2}
$$

where $k = 0 , 1 , \cdots , N - 1$ denotes the indices of the discretetime samples. Stacking all the measurements together, one can get

$$
\mathbf { y } = \mathbf { x } + \mathbf { i } + \mathbf { n }\tag{3}
$$

where

$$
\begin{array} { r l } & { \mathbf { x } = [ x [ 0 ] , x [ 1 ] , \cdots , x [ N - 1 ] ] ^ { T } \ \in \mathbb { C } ^ { N } , } \\ & { \mathbf { i } = [ i [ 0 ] , i [ 1 ] , \cdots , i [ N - 1 ] ] ^ { T } \ \in \mathbb { C } ^ { N } , } \\ & { \mathbf { n } = [ n [ 0 ] , n [ 1 ] , \cdots \ , n [ N - 1 ] ] ^ { T } \ \in \mathbb { C } ^ { N } , } \\ & { \mathbf { y } = [ y [ 0 ] , y [ 1 ] , \cdots \ , y [ N - 1 ] ] ^ { T } \ \in \mathbb { C } ^ { N } . } \end{array}
$$

Considering the different time-frequency properties of the “beat signals” resulting from targets’ responses and interferences, the targets’ beat signals are sparse in the frequency domain while the counterparts of interferences are sparse in the time-frequency domain, especially for point-like targets scenarios. Taking advantage of this feature, Uysal [18] has formulated the interference mitigation as a signal separation problem by pursuing sparse representations of targets’ beat signals and interferences in two different sets of bases. It can be explicitly expressed as an optimization problem

![](images/430cfcae62e690f401acbb4c3133b19b0d2d6efd8ea0cee14f71c94aa34bed34.jpg)  
Fig. 1. Graphic illustration of the sparse and low-rank decomposition of a Hankel structured matrix from the interference-contaminated FMCW radar system.

$$
\begin{array} { r } { \{ \mathbf { a } _ { x } , \mathbf { a } _ { i } \} = \arg \underset { \mathbf { a } _ { x } , \mathbf { a } _ { i } } { \operatorname* { m i n } } \| \mathbf { a } _ { x } \| _ { 1 } + \lambda \| \mathbf { a } _ { i } \| _ { 1 } } \\ { \mathrm { s . t . } \quad \| \mathbf { y } - \mathbf { x } - \mathbf { i } \| _ { 2 } ^ { 2 } < \epsilon } \\ { \mathbf { x } = \mathbf { F } _ { x } \mathbf { a } _ { x } , \mathbf { i } = \mathbf { F } _ { i } \mathbf { a } _ { i } } \end{array}\tag{4}
$$

where $\mathbf { F } _ { x }$ and $\mathbf { F } _ { i }$ are the bases for the sparse representations of targets’ beat signals and interferences, respectively. $\mathbf { a } _ { x }$ and ${ \bf a } _ { i }$ are the corresponding coefficients. λ is the regularization parameter used to trade off between the two terms. Generally, the discrete Fourier transform basis is used as $\mathbf { F } _ { x }$ and the Short-Time Fourier Transform (STFT) basis is employed as $\mathbf { F } _ { i }$ [18]. Then, the optimization problem in (4) can be efficiently addressed by incorporating the fast Fourier transform (FFT). However, due to the possible grid-off problem related to the FFT, the spectrum of a target’s beat signal could spread over multiple Fourier grids. Thus, part of the signal spectrum may be erroneously decomposed to be interferences, which causes signal power low and degrades the interference suppression performance.

The matrix pencil method [28], [32], [33] is an accurate approach for parameter estimations of complex exponentials by lifting the measurements as a Hankel matrix.

Inspired by this idea, we lift the interference-contaminated measurements as a Hankel matrix (see Fig. 1). For the measurement vector $\mathbf { y } \in \mathbb { C } ^ { N \times 1 }$ , a Hankel matrix $\mathbf { Y } \in \mathbb { C } ^ { m \times n }$ can be constructed, where $N = m + n - 1 , m > M$ and $n \ > \ M$ . According to (3), the Hankel matrix Y can be explicitly expressed as

$$
\begin{array} { c } { \mathbf { Y } = \mathcal { H } ( \mathbf { y } ) = \mathcal { H } ( \mathbf { x } ) + \mathcal { H } ( \mathbf { i } ) + \mathcal { H } ( \mathbf { n } ) } \\ { \mathbf { \Pi } = \mathbf { X } + \mathbf { T } + \mathbf { N } } \end{array}\tag{5}
$$

where $\mathcal { H } ( \cdot )$ is the operator that lifts a vector as a Hankel matrix. $\mathbf { X } = \mathcal { H } ( \mathbf { x } ) , \mathbf { T } = \mathcal { H } ( \mathbf { i } )$ and $\mathbf { N } = \mathcal { H } ( \mathbf { n } )$ are the Hankel matrices formed by the useful beat signals, interference and noise components, respectively. The Hankel matrix X related to targets’ beat signals is generally a low-rank matrix. Its rank is determined by the number of complex exponentials, i.e., beat signals in our case, which is usually much smaller than the matrix dimension. Meanwhile, the interference, as mentioned above, has a short duration in time; thus it is considered to be sparse in the time domain. As the construction of a Hankel matrix from a vector is a linear operation, the time-sparse interference leads to a sparse Hankel matrix T. This important observation motivates us to exploit the sparse and low-rank decomposition of a Hankel structured matrix to separate the useful signal and the interference from the measurement data. It can be expressed as

$$
\begin{array} { r } { \{ \mathbf { X } , \mathbf { T } \} = \arg \underset { \mathbf { X } , \mathbf { T } } { \operatorname* { m i n } } ~ \mathrm { r a n k } \left( \mathbf { X } \right) + \tau \| \mathbf { T } \| _ { 0 } } \\ { \mathrm { s . t . } ~ \| \mathbf { Y } - \mathbf { X } - \mathbf { T } \| _ { F } ^ { 2 } \leq \varepsilon } \\ { \mathbf { X } , \mathbf { T } \in \mathcal { H } } \end{array}\tag{6}
$$

where rank $\begin{array} { r c l } { ( \mathbf { X } ) } & { = } & { \sum _ { t } | \sigma _ { t } | _ { 0 } } \end{array}$ is the number of non-zero singular values (i.e., rank) of the matrix X, and $\| \mathbf { T } \| _ { 0 } ~ =$ $\begin{array} { r } { \sum _ { p = 1 } ^ { \bar { m } } \sum _ { q = 1 } ^ { n } | T _ { p q } | _ { 0 } } \end{array}$ (with slight abuse of notation) denotes the number of non-zero entries $T _ { p q }$ in the matrix T.

As it is difficult to solve the minimization of the rank and $\ell _ { 0 } .$ -norm sparse problem directly, the rank operation and $\ell _ { 0 } -$ norm are generally replaced, respectively, by the nuclear norm and $\ell _ { 1 }$ -norm for relaxation. Then, (6) can be relaxed as

$$
\begin{array} { r l } { \{ \mathbf { X } , \mathbf { T } \} = \arg \underset { \mathbf { X } , \mathbf { T } } { \operatorname* { m i n } } } & { \left\| \mathbf { X } \right\| _ { * } + \tau \left\| \mathbf { T } \right\| _ { 1 } } \\ { \mathrm { s . t . } } & { \left\| \mathbf { Y } - \mathbf { X } - \mathbf { T } \right\| _ { F } ^ { 2 } \leq \varepsilon } \\ & { \mathbf { X } , \mathbf { T } \in \mathcal { H } } \end{array}\tag{7}
$$

where $\begin{array} { r } { \| \mathbf { X } \| _ { * } = \sum _ { t } | \sigma _ { t } | _ { 1 } } \end{array}$ denotes the nuclear norm, i.e., the sum of the singular values of the matrix X, and $\| \mathbf { T } \| _ { 1 } ~ =$ $\begin{array} { r } { \sum _ { p = 1 } ^ { m } \sum _ { q = 1 } ^ { n } | T _ { p q } ^ { \phantom { } } | _ { 1 } } \end{array}$ denotes the sum of absolute values (or, magnitudes) of the non-zeros entries of the matrix T.

One can note that the formulation in (7) is a typical RPCA problem [26]. So, the Hankel matrices X and T can be readily obtained by using the RPCA algorithm and then the separated beat signals and interferences can be extracted from their first columns and last rows, respectively. However, due to the different numbers of recurrence of the elements in the lifted Hankel matrix T, the interference samples located close to the main anti-diagonal are implicitly weighted by a larger factor when the sparsity constraint is imposed. To circumvent this problem, we advise not lifting the interference part, i.e., replacing the $\ell _ { 1 } { \mathrm { - n o r m } }$ of the lifted matrix T by the $\ell _ { 1 }$ -norm of the interference vector i. Meanwhile, the Hankel matrix X can be substituted by ${ \mathcal { H } } ( \mathbf { x } )$ to explicitly accounting for the Hankel structure constraint. As a result, (7) can be rewritten (with slight abuse of the notation ε) as

$$
\begin{array} { r l } { \{ \mathbf { x } , \mathbf { i } \} = \arg \underset { \mathbf { x } , \mathbf { i } } { \operatorname* { m i n } } } & { { } \left\| \mathcal { H } ( \mathbf { x } ) \right\| _ { * } + \tau \left\| \mathbf { i } \right\| _ { 1 } } \\ { \mathrm { s . t . } } & { { } \left\| \mathbf { y } - \mathbf { x } - \mathbf { i } \right\| _ { 2 } ^ { 2 } \leq \varepsilon } \end{array}\tag{8}
$$

The above optimization problem generally can be tackled by using the RPCA algorithm with some minor modifications. However, singular value decomposition is involved in the RPCA approach, which is very computationally expensive, especially for larger matrices.

Considering the complex exponential model of beat signals $x ( t )$ in (1), the Hankel matrix ${ \mathcal { H } } ( \mathbf { x } )$ can be decomposed as

$$
\mathcal { H } ( \mathbf { x } ) = \mathbf { Z _ { L } } \pmb { \Sigma _ { M } } \mathbf { Z _ { R } } ,\tag{9}
$$

where

$$
\mathbf { Z _ { L } } = \left[ \begin{array} { c c c c } { 1 } & { 1 } & { \ddots \cdot } & { 1 } \\ { z _ { 1 } } & { z _ { 2 } } & { \ddots \cdot } & { z _ { M } } \\ { \vdots } & { \vdots } & { \vdots } \\ { z _ { 1 } ^ { N - L - 1 } } & { z _ { 2 } ^ { N - L - 1 } } & { \ddots } & { z _ { M } ^ { N - L - 1 } } \end{array} \right] ,\tag{10}
$$

$$
\Sigma _ { \bf M } = \mathrm { d i a g } \{ \sigma _ { 1 } , \sigma _ { 2 } , \cdot \cdot \cdot , \sigma _ { M } \} ,\tag{11}
$$

$$
\begin{array} { r } { \mathbf { Z } _ { \mathbf { R } } = \left[ \begin{array} { c c c c } { 1 } & { z _ { 1 } } & { \cdots } & { z _ { 1 } ^ { L - 1 } } \\ { 1 } & { z _ { 2 } } & { \cdots } & { z _ { 2 } ^ { L - 1 } } \\ { \vdots } & { \vdots } & & { \vdots } \\ { 1 } & { z _ { M } } & { \cdots } & { z _ { M } ^ { L - 1 } } \end{array} \right] . } \end{array}\tag{12}
$$

and $z _ { i } = \exp ( - j 2 \pi f _ { b , i } \Delta t )$ is the signal poles with respect to the corresponding target. Note that $\bar { \mathbf { Z } _ { \mathbf { L } } } ~ \in ~ \mathbb { C } ^ { m \times M }$ and $\mathbf { Z _ { R } } \in \mathbb { C } ^ { M \times n }$ are two Vandermonde matrices formed with the signal poles. If we decompose $\pmb { \Sigma } _ { \mathbf { M } }$ as the square of a diagonal matrix $\bar { \Sigma } \ ( \mathrm { i . e . , \Sigma _ { M } = \bar { \Sigma } ^ { 2 } } )$ and denote $\bar { \bf U } = { \bf Z _ { L } } \bar { \bf \Sigma }$ and ${ \mathbf V } = \left( \bar { \Sigma } { \mathbf Z _ { \mathbf R } } \right) ^ { H }$ , then we have

$$
\mathcal { H } ( \mathbf { x } ) = \mathbf { Z _ { L } } \bar { \boldsymbol { \Sigma } } \bar { \boldsymbol { \Sigma } } \mathbf { Z _ { R } } = \mathbf { U } \mathbf { V } ^ { H }\tag{13}
$$

where both U and V are also Vandermonde matrices. So, the Hankel matrix ${ \mathcal { H } } ( \mathbf { x } )$ can be decomposed as the product of two low-rank matrices. According to Lemma 8 in [30], the following relation holds true

$$
\| \mathcal { H } ( \mathbf { x } ) \| _ { * } = \operatorname* { m i n } _ { \tilde { \mathbf { U } } , \tilde { \mathbf { V } } } \quad \frac { 1 } { 2 } \left( \| \tilde { \mathbf { U } } \| _ { F } ^ { 2 } + \| \tilde { \mathbf { V } } \| _ { F } ^ { 2 } \right)\tag{14}
$$

where $\tilde { \textbf { U } }$ and $\tilde { \mathbf { V } }$ has no constraint in their sizes; thus, they could be different from the U and V in (13).

Taking advantage of (14) as a factorization of the nuclear norm, the optimization problem (8) can be rewritten as

$$
\left\{ \mathbf { x } , \mathbf { i } , \mathbf { U } , \mathbf { V } \right\} = \arg \operatorname* { m i n } _ { \mathbf { U } , \mathbf { V } , \mathbf { x } , \mathbf { i } } \ \frac { 1 } { 2 } \left( \left\| \mathbf { U } \right\| _ { F } ^ { 2 } + \left\| \mathbf { V } \right\| _ { F } ^ { 2 } \right) + \tau \left\| \mathbf { i } \right\| _ { 1 }\tag{15}
$$

$$
\begin{array} { r l } { \mathrm { s . t . } } & { \| \mathbf { y } - \mathbf { x } - \mathbf { i } \| _ { 2 } ^ { 2 } \leq \varepsilon } \\ & { \mathcal { H } ( \mathbf { x } ) = \mathbf { U } \mathbf { V } ^ { H } } \end{array}
$$

Note that for simplicity of notation $\tilde { \textbf { U } }$ and $\tilde { \mathbf { V } }$ are replaced by U and V in (15). This problem is much easier to address in terms of the optimization process. It can be solved with the ADMM iterative scheme, which would result in an SVD-free optimization algorithm.

## III. SPARSE AND LOW-RANK DECOMPOSITION OF THE HANKEL MATRIX

## A. Algorithm Derivation

In this section, an ADMM-based optimization approach is derived to address the optimization problem (15). Its aug-

mented Lagrangian function can be written as

$$
\begin{array} { r l } & { \mathcal { L } ( { \mathbf { U } } , { \mathbf { V } } , { \mathbf { x } } , { \mathbf { i } } , { \mathbf { p } } , { \mathbf { Q } } ) } \\ & { \quad = \displaystyle \frac { 1 } { 2 } ( \| { \mathbf { U } } \| _ { F } ^ { 2 } + \| { \mathbf { V } } \| _ { F } ^ { 2 } ) + \tau \left\| { \mathbf { i } } \right\| _ { 1 } } \\ & { \quad + \displaystyle \frac { \beta } { 2 } \left\| { \mathbf { y } } - { \mathbf { x } } - { \mathbf { i } } \right\| _ { 2 } ^ { 2 } + \langle { \mathbf { p } } , { \mathbf { y } } - { \mathbf { x } } - { \mathbf { i } } \rangle } \\ & { \quad + \displaystyle \frac { \mu } { 2 } \left\| \mathcal { H } ( { \mathbf { x } } ) - { \mathbf { U } } { \mathbf { V } } ^ { H } \right\| _ { F } ^ { 2 } + \langle { \mathbf { Q } } , \mathcal { H } ( { \mathbf { x } } ) - { \mathbf { U } } { \mathbf { V } } ^ { H } \rangle . } \end{array}
$$

where $\mathbf { p }$ and $\mathbf { Q }$ are multipliers, and $\beta$ and $\mu$ are regularization parameters. Combining the linear and quadratic terms in the augmented Lagrangian function, the scaled dual form can be expressed as

$$
\begin{array} { r l } & { { \displaystyle \mathcal { L } ( { \bf U } , { \bf V } , { \bf x } , { \bf i } , { \bf p } , { \bf Q } ) = \frac { 1 } { 2 } ( \| { \bf U } \| _ { F } ^ { 2 } + \| { \bf V } \| _ { F } ^ { 2 } ) + \tau \| { \bf i } \| _ { 1 } } } \\ & { ~ +  \frac { \beta } { 2 } \| { \bf y } - { \bf x } - { \bf i } + \frac { 1 } { \beta } { \bf p } \| _ { 2 } ^ { 2 } } \\ & { ~ +  \frac { \mu } { 2 } \| \mathcal { H } ( { \bf x } ) - { \bf U } { \bf V } ^ { H } + \frac { 1 } { \mu } { \bf Q } \| _ { F } ^ { 2 } . } \end{array}\tag{16}
$$

Based on the augmented Lagrangian function (16), the minimization optimization problem in (15) can be solved using the following ADMM iterative scheme:

$$
\mathbf { x } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { x } } \mathcal { L } ( \mathbf { U } ^ { ( k ) } , \mathbf { V } ^ { ( k ) } , \mathbf { x } , \mathbf { i } ^ { ( k ) } , \mathbf { p } ^ { ( k ) } , \mathbf { Q } ^ { ( k ) } )\tag{17}
$$

$$
\mathbf { i } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { i } \mathcal { L } ( \mathbf { U } ^ { ( k ) } , \mathbf { V } ^ { ( k ) } , \mathbf { x } ^ { ( k + 1 ) } , \mathbf { i } , \mathbf { p } ^ { ( k ) } , \mathbf { Q } ^ { ( k ) } )\tag{18}
$$

$$
\mathbf { U } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { U } } \mathcal { L } ( \mathbf { U } , \mathbf { V } ^ { ( k ) } , \mathbf { x } ^ { ( k + 1 ) } , \mathbf { i } ^ { ( k + 1 ) } , \mathbf { p } ^ { ( k ) } , \mathbf { Q } ^ { ( k ) } )\tag{19}
$$

$$
\mathbf { V } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { V } } \mathcal { L } ( \mathbf { U } ^ { ( k + 1 ) } , \mathbf { V } , \mathbf { x } ^ { ( k + 1 ) } , \mathbf { i } ^ { ( k + 1 ) } , \mathbf { p } ^ { ( k ) } , \mathbf { Q } ^ { ( k ) } )\tag{20}
$$

$$
\mathbf { p } ^ { ( k + 1 ) } = \mathbf { p } ^ { ( k ) } + \beta \left( \mathbf { y } - \mathbf { x } ^ { ( k + 1 ) } - \mathbf { i } ^ { ( k + 1 ) } \right)\tag{21}
$$

$$
\mathbf { Q } ^ { ( k + 1 ) } = \mathbf { Q } ^ { ( k ) } + \mu \left\lceil \mathcal { H } \left( \mathbf { x } ^ { ( k + 1 ) } \right) - \mathbf { U } ^ { ( k + 1 ) } \left( \mathbf { V } ^ { ( k + 1 ) } \right) ^ { H } \right\rceil\tag{22}
$$

In this iterative scheme, the four simple optimization problems (17)-(20) have to be addressed, which are discussed below in detail.

## (1) Update x

To update the variable x, the optimization problem in (17) can be written as

$$
\begin{array} { c } { \displaystyle \mathbf { x } = \arg \underset { \mathbf { x } } { \mathrm { m i n } } \left[ \frac { \beta } { 2 } \left\| \mathbf { y } - \mathbf { x } - \mathbf { i } ^ { ( k ) } + \frac { 1 } { \beta } \mathbf { p } ^ { ( k ) } \right\| _ { 2 } ^ { 2 } \right. } \\ { \displaystyle \left. + \frac { \mu } { 2 } \left\| \mathcal { H } ( \mathbf { x } ) - \mathbf { U } ^ { ( k ) } ( \mathbf { V } ^ { ( k ) } ) ^ { H } + \frac { 1 } { \mu } \mathbf { Q } ^ { ( k ) } \right\| _ { F } ^ { 2 } \right] } \end{array}\tag{23}
$$

Taking the first derivative, one can get the updated x as

$$
\begin{array} { c } { { { \displaystyle { \bf x } ^ { ( k + 1 ) } = \frac { 1 } { \mu + \beta } \left\{ \beta \left( { \bf y } - { \bf i } ^ { ( k ) } + \frac { 1 } { \beta } { \bf p } ^ { ( k ) } \right) \right. } } \ ~ } \\ { { \left. + \mu \mathcal { H } ^ { \dagger } \left[ { \bf U } ^ { ( k ) } \left( { \bf V } ^ { ( k ) } \right) ^ { H } - \frac { 1 } { \mu } { \bf Q } ^ { ( k ) } \right] \right\} } } \end{array}\tag{24}
$$

where $\mathcal { H } ^ { \dagger } ( \mathbf { X } ) ~ = ~ [ \mathbf { X } ( : , 1 ) ^ { T } , \mathbf { X } ( M , 2 ~ : ~ N ) ] ^ { T }$ constructs a column vector x˜ by picking from a Hankel matrix $\mathbf { X } \in \mathbb { C } ^ { M \times N }$

all the entries in the first column $\mathbf { X } ( : , 1 )$ and all the entries in the last row except the first one, i.e., $\mathbf { X } ( M , 2 : N )$ , which denotes the Penrose-Moore pseudoinverse of $\mathcal { H } ( \tilde { \mathbf { x } } )$

## (2) Update i

The corresponding optimization problem in (18) can be explicitly written as

$$
\mathbf { i } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { i } } \ \tau \left\| \mathbf { i } \right\| _ { 1 } + \frac { \beta } { 2 } \left\| \mathbf { y } - \mathbf { x } ^ { ( k + 1 ) } - \mathbf { i } + \frac { 1 } { \beta } \mathbf { p } ^ { ( k ) } \right\| _ { 2 } ^ { 2 } ,\tag{25}
$$

which is a typical Lasso (Least absolute shrinkage and selection operator) regression problem. Its solution is given by

$$
\mathbf { i } ^ { ( k + 1 ) } = S _ { \tau / \beta } \left( \mathbf { y } - \mathbf { x } ^ { ( k + 1 ) } + \frac { 1 } { \beta } \mathbf { p } ^ { ( k ) } \right)\tag{26}
$$

where $S _ { \lambda } ( x ) = e ^ { j \mathrm { a r g } ( x ) } ( | x | - \lambda ) .$ <sub>+</sub> denotes the complex soft thresholding operator.

## (3) Update U

The optimization problem in (19) for U update can be simply expressed as

$$
\mathbf { U } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { U } } \frac { 1 } { 2 } \left\| \mathbf { U } \right\| _ { F } ^ { 2 } + \frac { \mu } { 2 } \left\| \mathcal { H } ( \mathbf { x } ^ { ( k + 1 ) } ) - \mathbf { U } ( \mathbf { V } ^ { ( k ) } ) ^ { H } \right\| _ { F } ^ { 2 }\tag{27}
$$

By taking the first derivative, the minimizer can be obtained

$$
\begin{array} { r } { \mathbf { U } ^ { ( k + 1 ) } = \mu \left( \mathcal { H } ( \mathbf { x } ^ { ( k + 1 ) } ) + \displaystyle \frac { 1 } { \mu } \mathbf { Q } ^ { ( k ) } \right) \mathbf { V } ^ { ( k ) } } \\ { \mathbf { \cdot } \left( \mathbf { I } + \mu ( \mathbf { V } ^ { ( k ) } ) ^ { H } \mathbf { V } ^ { ( k ) } \right) ^ { - 1 } } \end{array}\tag{28}
$$

## (4) Update V

By performing the similar manipulations to update U, one can get the solution to (20) to update V, which is given by

$$
\begin{array} { r l } { \displaystyle \mathbf { V } ^ { ( k + 1 ) } = \arg \operatorname* { m i n } _ { \mathbf { V } } \left( \frac { 1 } { 2 } \| \mathbf { V } \| _ { F } ^ { 2 } \right. } & { } \\ { \displaystyle \left. + \frac { \mu } { 2 } \left\| \mathcal { H } \left( \mathbf { x } ^ { ( k + 1 ) } \right) - \mathbf { U } ^ { ( k + 1 ) } \mathbf { V } ^ { H } \right\| _ { F } ^ { 2 } \right) } & { } \\ { \displaystyle = \mu \left( \mathcal { H } \left( \mathbf { x } ^ { ( k + 1 ) } \right) + \frac { 1 } { \mu } \mathbf { Q } ^ { ( k ) } \right) ^ { H } \mathbf { U } ^ { ( k + 1 ) } } & { } \\ { \mathbf { \cdot } \left( \mathbf { I } + \mu ( \mathbf { U } ^ { ( k + 1 ) } ) ^ { H } \mathbf { U } ^ { ( k + 1 ) } \right) ^ { - 1 } } & { } \end{array}\tag{29}
$$

Based on (24), (26), (28), (29), (21) and (22), one can successively update x, i, U, V, p and Q in a loop. After several iterations, x and i are recovered from the measurements with an expected relative error δ.

Note in the iterative updates three regularization parameters $\beta , \mu$ and τ are involved and they should be set before starting the iterations. The choice of their values generally depends on specific problems. In implementation, to accelerate the convergence of the algorithm, $\beta$ and $\mu$ could be gradually increased to improve the regularization penalties of the data consistency and the signal model constraint, respectively. Empirically, the hyper-parameter $\mu$ could be increased by a factor of $k _ { \mu } ( \geq 1 )$ to smoothly tight the constraint of signal model while $\beta$ grows $k _ { \beta } ( \geq 1 )$ times every a few (e.g., L) iterations to enhance the

consistency between the measured data and recovered signal.   
The overall algorithm is summarized in Algorithm 1.

## IV. NUMERICAL SIMULATIONS

In this section, numerical simulations are presented to demonstrate the interference mitigation performance of the proposed approach. Meanwhile, the results are also compared with that of three state-of-the-art approaches: the adaptive noise canceller (ANC) [13], SALSA-based approach [18] and RPCA-based method [26], where the first one is a filtering approach while the latter two mitigate interferences through signal separation. Note that for the SALSA-based approach and the RPCA-based method, the formulations in (4) and (7) are respectively used for interference mitigation below.

## A. Evaluation metric

To quantitatively evaluate the interference mitigation performance of the proposed approach and facilitate its comparison with other methods in the following, we first introduce two metrics: signal-to-interference-plus-noise ratio (SINR) and correlation coefficient $\rho .$ The SINR is defined as

$$
\mathrm { S I N R } = 2 0 \log _ { 1 0 } { \frac { \| \mathbf { s } \| _ { 2 } } { \| \mathbf { i } + \mathbf { n } \| _ { 2 } } }\tag{30}
$$

where s is the interference- and noise-free (or reference) signal, and i and n are the interference and noise, respectively. For the recovered signal ˆs after interference mitigation, the SINR is obtained by replacing the term i + n in (30) with s − ˆs, which is the reciprocal of the relative error of the recovered signal in decibel scale. So the higher the SINR of

Algorithm 1: Interference mitigation with sparse and   
low-rank decomposition of the Hankel matrix   
Data: signal ${ \bf y } ;$ initialization of x, i, p, U, V, and Q;   
Set the relative error δ.   
Set the count of iterations k = 0.   
Set the (initial) values of the regularization   
parameters $\mu , \beta$ and τ .   
Result: x and i   
1 while $\| \mathbf { y } - \mathbf { x } - \mathbf { i } \| _ { 2 } \geq \delta \| \mathbf { y } \| _ { 2 }$ do   
2 k = k + 1;   
3 if 0 ≡ k (mod L) then   
4 $\beta  \beta \cdot k _ { \beta } \ ; \quad / / \beta$ increased every L   
iterations   
5 end   
6 1) Update x by using Equ. (24);   
7 2) Update i by using Equ. (25);   
8 3) Update U by using Equ. (27);   
9 4) Update V by using Equ. (29);   
10 5) Update p by using Equ. (21);   
11 6) Update Q by using Equ. (22);   
12 $\mu  \mu \cdot k _ { \mu }$ ; // µ increased every   
iteration   
13 end

![](images/f6af08325bc3ad814437b58e21dc605c56cc421bb056eaea42f24abfc9342c5e.jpg)  
(a)

![](images/0b7a6b10b5e22f7fa352c1daea1a63821e1ae40a6bb53c661a3790a08697b8fb.jpg)  
(b)  
Fig. 2. Illustration of interference mitigation for FMCW signals contaminated by multiple interferences. (a) the real part of the interference-contaminated beat signal, (b) the recovered signals after interference mitigation with the four methods, where the upper panel shows the recovered beat signal in a whol sweep and the lower panel gives a close-up of the signal segment within the interval [250, 255]µs.

TABLE I  
SYSTEM PARAMETERS FOR FMCW RADAR SIMULATIONS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Center frequency</td><td>3GHz</td></tr><tr><td>Sweep time of FMCW signal</td><td>400 µs</td></tr><tr><td>Signal bandwidth</td><td>40 MHz</td></tr><tr><td>Cutoff frequency of the LPF</td><td>5.33 MHz</td></tr><tr><td>Sampling frequency</td><td>12MHz</td></tr><tr><td>Waveform</td><td>Up-sweep chirp</td></tr></table>

TABLE II

SINR AND CORRELATION COEFFICIENT OF THE RECOVERED SIGNALS FOR POINT TARGET SIMULATION
<table><tr><td></td><td>SINR[dB]</td><td> $\rho$ </td><td>running time[s]</td></tr><tr><td>ANC</td><td>-9.69</td><td> $0 . 3 3 9 4 e ^ { - j 0 . 0 4 7 1 }$ </td><td>0.0013</td></tr><tr><td>SALSA</td><td>11.70</td><td> $0 . 9 6 6 9 e ^ { - j 0 . 0 1 6 4 }$ </td><td>15.2008</td></tr><tr><td>RPCA</td><td>14.20</td><td> $0 . 9 8 1 5 e ^ { - j 0 . 0 0 8 5 }$ </td><td>1050.0966</td></tr><tr><td>Proposed</td><td>29.95</td><td> $0 . 9 9 9 5 e ^ { - j 0 . 0 0 0 6 }$ </td><td>70.6254</td></tr></table>

the recovered signal, the better the interference mitigation. To avoid possible confusion, in the following we use $\mathrm { S I N R } _ { \mathrm { 0 } }$ and SINR to denote the signal to noise ratios of a signal before and after IM processing, respectively. The correlation coefficient between the signal s and its recovered counterpart ˆs is defined as

$$
\rho = \frac { \hat { \mathbf { s } } ^ { H } \mathbf { s } } { \left\| \mathbf { s } \right\| _ { 2 } \cdot \left\| \hat { \mathbf { s } } \right\| _ { 2 } } .\tag{31}
$$

Generally, $\rho$ is a complex number with its modulus $0 \le | \rho | \le$ 1. A larger modulus of $\rho$ indicates a higher correlation between ˆs and s while its phase represents a relative phase different between them.

## B. Point target Simulations

Firstly, an FMCW radar contaminated by multiple FMCW interferences is considered. The parameters of the FMCW radar system used for the simulations are listed in Table I. Three point targets are placed at a distance of 2 km, 3.5 km and 5 km, respectively, away from the radar system.

According to Table I, the radar transmits FMCW waveform with the sweep slope of $K _ { r } = 1 \times 1 0 ^ { 5 } \mathrm { M H z / s }$ . Assume that it is interfered by three FMCW aggressor radars with sweep slopes of $3 K _ { r } , - 2 K _ { i }$ <sub>r</sub> and $- 1 . 5 K _ { r } .$ . The received signals are mixed with the transmitted FMCW waveform for dechirping and then pass through an anti-aliasing low-pass filter (LPF) with the cut-off frequency of 5.33 MHz. The acquired beat signal of the point targets is shown in Fig. 2(a), where about 38% of the signal samples are contaminated by the three strong FMCW interferences. Meanwhile, white Gaussian noise is added with the signal to noise ratio (SNR) of 15 dB to consider the system thermal noise and the measurement errors. As a result, the synthesized signal has a $\mathrm { S I N R _ { 0 } }$ of −12.7 dB.

Taking advantage of the proposed interference mitigation approach as well as three other state-of-the-art methods, i.e., ANC, SALSA- and RPCA-based methods, the useful beat signals are recovered, which are shown in Fig. 2(b). For comparison, the reference signal is also presented. In the implementation, a filter of length 50 was used for the ANC method. For the morphological component analysis formulation in (4), the regularization parameters $\lambda ~ = ~ 0 . 8 5$ and $\mu ~ = ~ 1$ (accounting for the constraint of data consistency) [18] were used for the SALSA-based method where the STFT utilized a 128-sample window with 122 samples of overlap between neighboring segments and a 128-point FFT. The maximum number of iteration for the SALSA method was set to be 1000. For the RPCA-based method, the regularization parameter $\tau$ was set as $1 / \sqrt { d _ { \mathbf { X } } }$ where $d _ { \mathbf { X } }$ is the maximum of the lengths of the row and column dimensions of the matrix X and $\mu = 0 . 0 5$ was chosen for the data consistency constraint. Regarding the proposed approach, $\tau = 0 . 0 2$ was used, and $\beta$ and $\mu = 0 . 0 2$ were initialized with 0.1 and 0.02, respectively; then, $\beta$ was increased by a factor of $k _ { \beta } = 1 . 6$ every $L = 1 0$ iterations and $\mu$ grew $k _ { \mu } = 1 . 2$ times in each iteration. Moreover, the termination of both the RPCA-based method and the proposed approach were determined by setting $\delta = 1 \times 1 0 ^ { - 6 }$ . Note that the parameters related to each method have been empirically tuned for their optimal performance (without explicit statement, these (hyper-)parameters will be used for all the simulations below).

![](images/320dfdd74b40cb9ebaf754fb57357c742352aa65bafc86eb9defc9c3c880aecd.jpg)  
(a)

![](images/c11de88ea6d2146bf0c47d7dbb9a25516fd1abbd98cda11273c445e1e013d721.jpg)  
(b)

![](images/6cbfa8a7c0e788007830ee4be670be1723e6a14bb7578e6c3f3e3a6d4a1ceaaa.jpg)  
(c)  
Fig. 3. Range profile of the point targets. (a) shows the range profiles of targets obtained before and after interference mitigation with the four methods (b) and (c) are the zoomed-in views of the parts indicated by the rectangles in (a), i.e., the range profiles of targets at the distance of 2 km and 3.5 km, respectively.

TABLE III  
QUANTITATIVE COMPARISON OF THE SINR AND CORRELATION COEFFICIENT OF THE RECOVERED SIGNALS BY THE ANC, SALSA-, RPCA-BASEDMETHODS AND THE PROPOSED INTERFERENCE MITIGATION APPROACH.
<table><tr><td></td><td colspan="3"> $\mathbf { S I N R _ { 0 } } = \mathbf { - 2 0 d B }$ </td><td colspan="3"> $\mathbf { S I N R _ { 0 } } = - \mathbf { 1 0 } \mathbf { d B }$ </td><td colspan="3"> $\mathbf { S I N R _ { 0 } } = \mathbf { 0 } \mathbf { d B }$ </td></tr><tr><td></td><td>SINR[dB]</td><td> $\rho$ </td><td>running time[s]</td><td>SINR[dB]</td><td>ρ</td><td>running time[s]</td><td>SINR[dB]</td><td> $\rho$ </td><td>running time[s]</td></tr><tr><td>ANC</td><td>-16.9939</td><td> $0 . 1 4 7 4 e ^ { - j 0 . 0 0 9 8 }$ </td><td>0.0052</td><td>-7.0345</td><td> $0 . 4 0 8 9 e ^ { j 0 . 0 1 4 9 }$ </td><td>0.0012</td><td>3.0288</td><td> $0 . 8 1 6 1 e ^ { - j 0 . 0 1 7 7 }$ </td><td>0.0010</td></tr><tr><td>SALSA</td><td>-7.4778</td><td> $0 . 3 4 8 4 e ^ { - j 0 . 0 0 8 1 }$ </td><td>15.4845</td><td>12.4891</td><td> $0 . 9 7 5 2 e ^ { j 0 . 0 0 6 4 }$ </td><td>15.1590</td><td>12.7830</td><td> $0 . 9 7 7 4 e ^ { - j 0 . 0 0 5 7 }$ </td><td>15.5027</td></tr><tr><td>RPCA</td><td>-11.1290</td><td> $0 . 2 5 4 5 e ^ { - j 0 . 0 6 5 4 }$ </td><td>862.2684</td><td>15.2970</td><td> $0 . 9 8 5 2 e ^ { j 0 . 0 0 9 1 }$ </td><td>836.8579</td><td>16.6967</td><td> $0 . 9 8 9 3 e ^ { - j 0 . 0 0 6 6 }$ </td><td>318.6887</td></tr><tr><td>Proposed</td><td>24.2185</td><td> $\mathbf { 0 . 9 9 8 7 e ^ { j 0 . 0 0 4 2 } }$ </td><td>50.5626</td><td>27.7170</td><td> $\mathbf { 0 . 9 9 9 2 e ^ { j 0 . 0 0 4 0 } }$ </td><td>78.7157</td><td>28.4259</td><td> $\mathbf { 0 . 9 9 9 4 e ^ { - j 0 . 0 0 2 2 } }$ </td><td>70.0923</td></tr></table>

From Fig. 2(b), all the SALSA-, PRCA-based methods and the proposed approach successfully mitigate the interferences and outperform the ANC. By constrast, ANC suppresses only half of the interferences compared to the signal in Fig. 2(a). As the ANC assumes that the spectra of interferences in the positive and negative frequency bands are conjugate symmetric while the useful beat signals are only located in the positive spectrum, which generally is not fulfilled in practice, the negative spectrum is filtered out and then utilized as a reference to eliminate the interference in the positive spectra. As the conjugate symmetry of the spectrum of interferences is not satisfied in this case, the gain of the interference mitigation of ANC is mainly attributed to the spectrum filtering; thus, one can see that half of the interferences are suppressed by ANC compared to Fig. 2(a). From the bottom panel in Fig. 2(b), visually the recovered beat signal obtained with the proposed approach shows the best agreement with the reference one. For quantitative evaluation, the SINRs and $\rho \mathbf { \dot { s } }$ of the recovered signals with the ANC, SALSA, RPCA and the proposed approaches are shown in Table II. Compared to the three existing methods, the proposed approach significantly supresses the interference, improving the SINR and $\rho$ of the recovered signal relative to the reference.

Applying the FFT operation of the recovered signal with respect to time, the range profile of targets is obtained, as shown in Fig. 3(a). For comparison, the range profiles of the reference signal (i.e., denoted by “ref”) and the beat signal before interference mitigation (i.e., “sig Interf”) are illustrated as well. One can see that the ANC only partially removes the strong interference and the remaining interference still causes very high “noise” floor in the resultant range profile. By contrast, the SALSA-, RPCA-based methods and the proposed approach all substantially mitigate the interferences; thus, they make clearly visible the weak target at 3.5 km that is almost completely immersed in the high “noise” floor caused by strong interferences (see the “sig Interf” in Fig. 3(a)). Moreover, compared to SALSA- and the RPCAbased methods, the proposed approach leads to lower “noise” floor in the obtained range profile after interference mitigation, which confirms the high SINR of its recovered beat signal in Fig. 2(b). Meanwhile, the range profiles of targets obtained with the proposed approach show the best agreement with the reference one (see the zoomed-in views in Fig. 3(b) and (c)).

## C. Effect of interference strength and duration on the IM performance

To examine the effects of the strength and the duration of the interference (equivalently, the percentage of the interferencecontaminated signal samples) on the interference mitigation performance of the proposed approach, two sets of simulations are performed. Firstly, we keep the duration of the interferences the same as in Fig. 2(a) relative to the duration of the beat signal but change the strengths of the interferences. The synthetic interference-contaminated beat signals with the $\mathrm { S I N R _ { \mathrm { 0 } } }$ of −20 dB, −10 dB and 0 dB were synthesized and processed with the ANC, SALSA-, RPCA-based methods and the proposed approach. For each $\mathrm { S I N R _ { 0 } }$ case, 20 Monte Carlo simulation runs were performed. The averages of the SINRs and correlation coefficients of the recovered signals are listed in Table III. Compared to the ANC, the SALSA-, RPCAand the proposed approaches achieve much better interference mitigation performance in terms of both SINR and correlation coefficient in all three $\mathrm { S I N R _ { \mathrm { 0 } } }$ cases. Meanwhile, they all noticeably eliminate the interferences and improve the SINR of the recovered signal and its correlation coefficient relative to the reference signal in the case of $\mathrm { S I N R _ { 0 } } \ = \ - 1 0 \mathrm { d B }$ Moreover, at all the three $\mathrm { S I N R _ { 0 } }$ levels the proposed approach constantly outperforms the other three methods, especially, in terms of SINR of the recovered signal by a significant margin.

Then, the effects of interference duration on the SINR and $\rho$ are investigated by using interference-contaminated beat signals with various interference durations but a constant $\mathrm { S I N R _ { 0 } }$ . The interference-contaminated beat signals were synthesized by simultaneously changing the sweep slopes of the interferences relative to the transmitted FMCW waveform, which leads to various interference durations after dechirping and low-pass filtering operations, and their magnitudes. The $\mathrm { S I N R _ { 0 } }$ of the synthetic beat signals was kept to be almost constant, i.e., about −16.5 dB. Then, they were processed with the four interference mitigation approaches. For each interference duration case 20 Monte Carlo simulations were run, and the averages of SINRs and correlation coefficients of the recovered signals were computed.

Fig. 4 shows the effect of interference duration on the SINR and $\rho$ of their recovered signals. As one can see, the ANC and SALSA-based method achieve almost constant SINR while the performance of the RPCA-based and the proposed approaches degrade with the increase of the interference duration(see Fig. 4(a)). This is because the SALSA-based method exploits the sparse features of useful signal and interferences in the frequency domain and time-frequency domain, respectively. So the time durations of a few interferences have marginal impact on its interference mitigation performance. By contrast, the RPCA-based method and the proposed approach assume that the interferences are sparse in time. Consequently, a rapid decline of their performance is observed when the interference duration is longer than 50% of the signal duration. Nevertheless, when the interference duration is less than 50%, both the RPCA-based method and the proposed approach perform better than the other two methods. Meanwhile, the proposed approach gains about 10 dB improvement of the SINR of the recovered signal compared to the RPCA-based method. From Fig. 4(b), one can see that the moduli of $| \rho |$ of the recovered signals by the SALSA-, RPCA-based methods and the proposed approach are all close to 1 and the corresponding phases are near 0 when the interference duration is less than 50%; thus, they get more accurate recovered signals than the ANC. Compared to the other three methods, the proposed approach recovers the useful beat signals with the best correlation coefficient |ρ| (i.e., highest moduli and nearzero phase) with respect to the reference ground-truth signal when the interference is sparse in time. However, when the interference duration increases to 50% or more, the assumption of sparse interference in the time domain is violated and then the performance of the proposed approach gradually drops, which results in the decrease of the modulus of $| \rho |$ and the rise of the deviation of its phases from zero.

![](images/c5af5f3c0a6f80b014ec7d9166923734d33e42b95311da43177d724b11119b57.jpg)  
(a)

![](images/77870b8779db4ee30382909d5af78f89a375d3f1fa4f9d90e02682573e3a9c7a.jpg)  
(b)

Fig. 4. Impact of the interference duration on the interference mitigation performance. (a) shows the variation of SINR with the interference durations. (b)shows the variation of the correlation coefficients with different interference durations.  
![](images/c3bcc6674b2b33f768a2eeb058849206dc6f6730aeb3dfd72f32ae9daab062d2.jpg)  
Fig. 5. Illustration of the convergence of the proposed IM method with the increase of the running iterations.

## D. Algorithm convergence and hyperparameter selections

The proposed algorithm is developed based on the ADMM framework. The theoretical analysis of the convergence of ADMM has been discussed in many papers [34], [35]. Considering the limited scope and for the sake of conciseness, we omit the theoretical analysis of the convergence of the developed ADMM-based algortihm but instead illustrate its convergence based on the numerical simulations. Extensive numerical simulations show that the developed algorithm generally converges to a relatively good result in a few tens of iterations by properly choosing the values of hyper-parameters $\beta , \mu$ and τ . For the simulation in section IV-B, the relative error of the estimation signal with respect to the number of operating iteration of the proposed algorithm is shown in Fig. 5. Although the relative error had a fluctuation from iteration 3 to iteration 4, it does not affect the final convergence of the algorithm. After 40 iterations, the relative error has already dropped below $1 0 ^ { - 4 }$

![](images/ee3261e4cea718cf75a8fef46e015c4393cb76993c004b590118e3599ebde37c.jpg)  
(a)

![](images/93d6a5f0b561b782278c0735476faea3dccbc67781da03203c9b75d4edc212ae.jpg)  
(b)

![](images/4213b07be2f4f133da1290035ea5fa4dc6a69352c84ceee04886c4f57fcd9563.jpg)  
(c)

![](images/3788215faecada17c4421bdffed7e59a3165121567327188bc5bf16dab6bc808.jpg)  
(d)  
Fig. 6. The number of iterations used by the proposed approach to get the estimated signal with predefined relative error $1 0 ^ { - 6 }$ in different combinations of the values of the hyperparameters β, µ and $\begin{array} { r } { \tau . \tau = \frac { l _ { 1 } } { \sqrt { \operatorname* { m a x } ( m , n ) } } } \end{array}$ and $\begin{array} { r } { { \bf \Pi } \overline { { \mu } } = l _ { 2 } \frac { 1 0 0 } { \| { \bf Y } \| _ { 2 } } } \end{array}$ with $l _ { 1 } , l _ { 2 } \in \{ 0 . 1 , 0 . 5 , 1 , 5 , 1 0 , 5 0$ , 100}. Moreover, in (a) $\begin{array} { r } { \beta = \frac { 0 . 1 } { 1 0 ^ { \mathrm { { S N R } } / 1 0 } } , } \end{array}$ (b) $\beta = \frac { 1 } { 1 0 ^ { \mathrm { S N R } / 1 0 } }$ , ( $\begin{array} { r } { \mathbf { c } ) ~ \beta = \frac { 1 0 } { 1 0 ^ { \mathrm { S N R } } / 1 0 } } \end{array}$ and $\begin{array} { r } { \beta = \frac { 1 } { 1 0 ^ { \mathrm { S N R } } / 1 0 } . } \end{array}$

The hyperparameters $\beta , \tau$ and $\mu$ impose the trade-off between data consistancy, time domain sparsity of interferences and spectral sparsity of the useful signals, respectively. For the data consistency constraint, it is natural to use a larger penalty $\beta$ when the SNR of the data is high while a smaller one when the SNR is low. Due to this observation, we recommend to choose $\begin{array} { r } { \tau = \frac { l _ { 0 } } { 1 0 ^ { \mathrm { S N R } / 1 0 } } } \end{array}$ , where $l _ { 0 }$ is a constant factor. For the time-domain sparse component, which corresponds to the sparse component in the canonical RPCA problem, the related hyperparameter τ can take the similar choice suggested in [26], i.e., $\begin{array} { r } { \tau = \frac { l _ { 1 } } { \sqrt { \operatorname* { m a x } ( m , n ) } } } \end{array}$ with m and n are the row and column dimensions of the constructed Hankel matrix, and $l _ { 1 }$ is a constant factor. Meanwhile, the spectral sparsity constraint of useful signals is characterized by the Frobenius norm of the difference between its Hankel matrix and the product of two low-rank matrices. Thus, similar in [23], we recommend $\begin{array} { r } { \mu = \frac { 1 0 0 \cdot l _ { 2 } } { \Vert \mathbf { Y } \Vert _ { 2 } } } \end{array}$ , where $\| \mathbf { Y } \| _ { 2 }$ is the $\ell _ { 2 }$ norm of the matrix Y, i.e., its largest singular value, and $l _ { 2 }$ is a constant multiplier. In practice, the multiplication factors $l _ { 0 } , l _ { 1 }$ and $l _ { 2 }$ could be tuned for specific signals to get satisfactory results. To investigate the effect of the hyperparameters on the convergence of the proposed method, we used the synthetic data in section IV-B as an example and took $l _ { 1 } ~ \in ~ \{ 0 . 1 , 1 , 1 0 , 1 0 0 \}$ and $l _ { 1 } , l _ { 2 } \in$ $\{ 0 . 1 , 0 . 5 , 1 , 5 , 1 0 , 5 0 , 1 0 0 \}$ to form various combinations of the three hyperparameters. By setting $k _ { \mu } = 1 . 2 , k _ { \beta } = 1 . 6 , L = 1 0$ and the relative error $\delta = 1 \times 1 0 ^ { - 6 }$ , the number of iterations needed to get a desired result with different combinations of the hyperparameters are shown in Fig. 6. It is clear that a larger multiplication factor for $\mu$ and $\beta$ and a smaller one for $\tau$ would make the proposed method converge fast when an estimation of the useful signal with a certain relative error is expected.

## E. Computational complexity and time

Generally, the ANC takes advantage of an adaptive filtering technique for interference mitigation and is a very efficient method. By contrast, the SALSA- and RPCA-based methods as well as the proposed approach are iterative algorithms and their computational complexities depend on the number of iterations in practice. Specifically, the SALSA-based method could exploit the FFT for efficient implementation while the RPCA-based approach has to deal with the SVD of a large matrix in each iteration, which generally is very computationally heavy. By contrast, the proposed approach is an SVDfree algorithm and its computational complexity should be significantly reduced compared to the RPCA-based method. The computational complexity of the proposed approach is mainly determined by the six update steps and the number of iterations. Assuming the maximum rank of U and V is $p ,$ the computational complexity for updating x, i, U, V, p and Q in one iteration are $O ( N + m n ( p + 1 ) ) , O ( N )$ $O ( m n ( 1 + p ) + ( m + n + 1 ) p ^ { 2 } + p ^ { 3 } ) , O ( m n ( 1 + p ) + ( m +$ $n + 1 ) p ^ { 2 } + p ^ { 3 } ) , O ( N )$ , and $O ( m n ( p + 2 ) ) ,$ ), respectively. So, in one iteration the computational complexity of the proposed method is $O ( m n ( 4 p + 5 ) + 2 ( m + n + 1 ) p ^ { 2 } + 2 p ^ { 3 } )$ , which is much smaller than that of the SVD-based method, i.e., $O ( m n ^ { 2 } ) { } ~ ( m \geq n )$ considering the fact $p \ll m , n$

As an example, the average computation time of the four methods for the simulations in section IV-B are listed in Table II and Table III, respectively. All the methods were implemented with MATLAB and run on a PC with an Intel i5-3470 Cnetral Processing Unit (CPU) @ 3.2 GHz and 8 GB Random Access Memory (RAM). It is clear that the ANC is the most efficient method among them and the proposed method is much faster than the RPCA-based approach but slower than the SALSA-based one.

## V. EXPERIMENTAL RESULTS

In this section, the application of the proposed method to real radar data is presented. The same measurement setups and data sets (i.e., the chimney and rain data) as in [17] are used to verify the proposed approach here. The data was collected with the TU Delft full-polarimetric PARSAX radar by simultaneously transmitting up- and down-chirp signals at the Horizontal (H-) and Vertical (V-) polarization channels for full scattering matrix measurements. The PARSAX radar was designed with a good isolation between receiver and transmitter, i.e., -100 dB for HH (Horizontally polarized transmission and Horizontally polarized reception) and -85 dB for VV (Vertically polarized transmission and Vertically polarized reception), and polarization channel isolation better than 30 dB [36]. For convenience, the parameters for experimental measurements are listed in Table IV. The interference of strong co-polarized, i.e., VV-pol signal on the cross-polarized, i.ge., HV-pol (Horizontally polarized transmission and Vertically polarized reception) signals is considered below.

TABLE IV  
EXPERIMENTAL SETUP PARAMETERS FOR EXPERIMENT 1 AND EXPERIMENT 2
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Center frequency</td><td>3.1315 GHz</td></tr><tr><td>Bandwidth</td><td>40 MHz</td></tr><tr><td>Sweep time</td><td>1 ms</td></tr><tr><td>Number of samples per sweep</td><td>16384</td></tr><tr><td>Maximum range</td><td>18.75 km</td></tr><tr><td>Number of sweeps per CPI</td><td>512</td></tr><tr><td>Waveforms</td><td>Up-chirp for H-pol channel; Down-chirp for V-pol channel</td></tr></table>

![](images/29bd70785145d0a645dbad7786968a00d8de9c3ea96ebbd825248938a7e3936c.jpg)  
(a)

![](images/6838ad9e67f914b6119cc9e63136681f87de2b3f06e3a20e5cb130c8c9ac23a7.jpg)  
(b)  
Fig. 7. (a) The beat signals with and without the interference, where the dashed-line rectangle indicates the region of interference-contaminated samples. (b) The recovered beat signals of the chimney observation after interference mitigation. The upper panel shows the beat signals recovered by the MP-, ANC, SALSA-, RPCA-based methods and the proposed approach while the lower panel is the close-up of the beat signals in the interval of [440, 460]µs in the upper panel.

## A. Experiment 1: Stationary isolated target (Chimney)

In this experiment, the PARSAX radar was set to observe a tall industrial chimney which is about 1.07 km away. The acquired HV-pol beat signal with the interference caused by the VV-pol component scattered from the illuminated scene is shown in Fig. 7(a), where the interference-contaminated samples are indicated by a dashed-line rectangle. For comparison, the beat signal without interference was also collected by using only the H-pol transmitting channel to transmit upchirp signal but turning off the V-pol transmitting channel in a consecutive sweep with a time delay of 1 ms, which is presented as a reference (i.e., “ref sig” in Fig. 7(a)). Note as the experimental data were collected for a wild real scene where some dynamic objects may exist, the reference signal acquired after a time delay of 1 ms may be, strictly speaking, not exactly the same as the useful signals due to the change of the scene. Nevertheless, for a slow-changing scene as in our case, the impact of the change of the scene in such a short time delay is almost negligible; thus, the acquired beat signal without interferences can be a “valid” reference.

![](images/1940e1a1b08c199ed972ab9aec060f135ccc67a43360225090e656af402b0614.jpg)  
(a)

![](images/cc6d7207eba531e8eae536487b95df241a6ead41f6658058198e228fab6a2a30.jpg)  
(b)

![](images/bf1e9aa474fc2fb7082734c262cdb4d3717a44574ded5bdabf6a4aeeb151431f.jpg)  
(c)  
Fig. 8. (a) The range profiles of the chimney scenario obtained with the interference-contaminated beat signal, clean reference signal, and the recovered signals after interference mitigation with the ANC, MP-, SALSA-, RPCA-based methods, and the proposed approach. (b) and (c) show the zoomed-in view of the range profiles of targets at the distance of 1.07 km and 4.3 km in (a), respectively.

Then, the interference-contaminated beat signal was processed with the ANC, SALSA-, RPCA-based methods and the proposed approach with empirically chosen optimal (hyper-) parameters. Specifically, the ANC used a 200-sample adaptive filter and the SALSA-based method utilized the same parameters as in section IV-B except for a different regularization parameter $\lambda = 0 . 5 .$ . For the RPCA-based method, $\mu ~ = ~ 0 . 0 0 0 1$ was used for the data consistency constraint and $\delta ~ = ~ 1 \times 1 0 ^ { - 6 }$ for controlling the termination of the iterative algorithm. Meanwhile, for the proposed approach, almost the same parameters in section IV-B were used except that $\tau , \beta$ and $\mu$ were initialized with 10, 0.125, and 0.0001, respectively. After handling the interference mitigation by the ANC, SALSA-, RPCA-based methods and the proposed approach, the acquired beat signals are shown in Fig. 7(b). As only one interference appears in the acquired beat signal, the reconstructed beat signal with the matrix pencil (MP)-based method in [17] is presented for comparison. Visually, the MP-, SALSA-, RPCA-based methods and the proposed approach all get satisfactory results which have very good agreement with the reference signal in contrast to that obtained with the ANC (see the lower panel in Fig. 7(b)). Quantitatively, the SINRs of the recovered beat signals with the ANC, MP-, SALSA-, RPCA-based methods and the proposed approach are 2.93 dB, 21.40 dB, 17.87 dB, 20.77 dB and 20.78 dB, respectively. The corresponding correlation coefficients $| \rho |$ are 0.7008, 0.9964, 0.9919, 0.9958, and 0.9958. So according to the values of the SINR and $| \rho | ,$ , the MP-based method gets the most accurate result, which is slightly better than that acquired with the RPCA-based method and the proposed one. However, the MP-based method requires to first detect the location of the interference in a sweep, and then cut out the interferencecontaminated signal samples and reconstruct them based on the rest. Although we assume the location of the interference is accurately detected in this experiment, it is generally a challenge to precisely distinguish the interference from the useful signal. By contrast, the RPCA-based method and the proposed approach have no such requirement, which can tackle the interference mitigation blindly.

To further illustrate the accuracy of the recovered beat signals, the corresponding range profiles of targets are obtained by taking the FFT of them with respect to time, as shown in Fig. 8(a). Compared to the range profile of the reference signal, both the MP-based method and the proposed approach significantly suppress the interference and reduce the “noise” floor (Fig. 8(a)). Their resultant range profiles have a very good agreement with the reference one (see the zoomed-in range profiles of the chimney and the weak scattering object in Fig. 8(b) and (c), respectively). Although both the SALSAand RPCA-based methods effectively mitigate the interference, the range profiles produced by their recovered signals have slightly higher “noise” floor compared to that obtained with the MP-based method and the proposed approach (Fig. 8(a)). Moreover, the signal acquired by handling the interference mitigation with the SALSA-based method leads to small (i.e., about 0.2 dB) loss of the peak power of the range profile of the chimney $( \mathrm { F i g . ~ } 8 ( \mathrm { b } ) )$ while the ANC completely suppresses the signal of the weak scattering object at the distance of 4.3 km $( \mathrm { F i g . ~ } 8 ( \mathrm { c } ) )$ .

## B. Experiment 2: Distributed target (Rain)

A rain storm was observed by steering the PARSAX radar pointing to the zenith. The fully polarimetric data were acquired by simultaneously transmitting and receiving both horizontally and vertically polarized signals. Here we use the same HV-polarimetric data in [17] to demonstrate the interference mitigation, which are contaminated by the strong VV-polarimetric signals arriving at the receiver at the same time. This rain dataset contains radar signals measured in one coherent processing interval, i.e., 512 FMCW sweeps. As the rain droplets are moving targets, the range Doppler (R-D) map is generally used to characterize their distribution. Considering the relatively stable interference location in each sweeps and avoiding possible negative effects of the inaccuracy of the interference suppression, the processing flow we take is: first take the FFT of the HV signals along the slow time and then handling interference mitigation of the signals in each Doppler frequency bin followed by an FFT operation along the fast time to get the focused R-D map [17].

To perform interference mitigation for signals in each Doppler bin, the ANC was tuned to utilize a 50-sample adaptive filter. For the SALSA-based method, the regularization parameters λ and $\mu$ took the values of 0.875 and 1, respectively; meanwhile, the STFT in its each iteration used a 256-sample rectangular window with 243 samples (i.e., 95%) of overlap between adjacent segments and 256-point FFT. Moreover, the RPCA was implemented by using the same parameters as in section V-A except for $\mu ~ = ~ 0 . 0 0 5$ For the proposed approach, $\beta = 1 , \ \mu = 8 , \ \tau = 0 . 0 8$ and $\delta = 1 \times 1 0 ^ { - 6 }$ were initialized. To speed up the convergence of the algorithm, $\mu$ and $\beta$ were gradually increased with the parameters $k _ { \mu } = 1 . 1 , k _ { \beta } = 1 . 8$ and L = 10. Fig. 9 shows the raw beat signal in a Doppler frequency bin and the recovered counterparts after dealing with interference mitigation with the ANC, SALSA-, RPCA-based methods and the proposed approach. Similar to Experiment 1, the result of the MP-based method in [17] is also presented for comparison. One can see that the ANC almost fails to suppress the interference in this experiment while all the other approaches significantly mitigate the interference. As the MP-based method only cuts out the interference-contaminated measurements and then reconstructs the samples of useful signals in the cut-out region, the rest of signal samples keeps the same as the original signal (see the insets in Fig. 9). By contrast, the SALSA-, RPCA-based methods and the proposed approach tackle the interference mitigation as a signal separation problem, and both the interference and noise could be separated and removed from the useful signals. Thus, the recovered signal samples in the interference-free region could slightly deviate from the original ones due to the de-noising effect. As the ground truth signal is unavailable, it is difficult to directly evaluate the accuracy of these recovered signals.

Nevertheless, with the signals recovered by each method, the R-D maps can be reconstructed and compared to assess their performance of interference mitigation. Fig. 10 shows the focused R-D maps with the recovered signals as well as the original ones. It is clear that the R-D map of the rain droplets is still completely masked by the strong interference (see Fig. 10(c)). Comparing Fig. 10(b), (d), (e) and (f), one can see that the MP-, SALSA-based method and the proposed approach get cleaner range-Doppler distribution of rain droplets than the RPCA-based method, especially in the area above the range of 2 km with Doppler frequency larger than 50 Hz. Meanwhile, the R-D map obtained with the MP-based method has the most uniform background than that of the RPCA-, SALSA-based methods and the proposed approach. Although some remaining weak interference streaks can be observed in Fig. 10(f), the proposed approach leads to lower background noise floor compared to that in Fig. 10(b). This is attributed to the denoising effect of the proposed approach during the signal separation. In principle, the remaining weak interference can be further suppressed by searching the optimal regularization parameters $\mu , ~ \beta$ and $\tau .$ In addition, the proposed approach effectively suppresses the zero-Doppler interference compared to the MP-, SALSA-, and the RPCA-based methods.

![](images/bd333a81705b11ed67750ec12abddb0b57128141a34d212840189989fb48b386.jpg)  
Fig. 9. Signal in a Doppler frequency bin. Both the signals before (i.e., orig sig) and after interference mitigation are presented.

## VI. CONCLUSION

In this paper, an approach based on sparse and low-rank decomposition of the Hankel matrix is proposed for interference mitigation of FMCW radars. Compared with the existing interference nulling and reconstruction methods, the proposed approach does not need to detect the location of interferences and is able to blindly handle complex interference mitigation problem with multiple interferers. In contrast to the FFTbased signal separation methods (for instance, the SALSAbased method) which exploit the sparsity of the signals and the interference on the regular discrete grids of Fourier bases, the proposed algorithm utilizes the gridless optimization. So it improves the accuracy of the recovered signal by avoiding the possible mismatch between the spectrum of the signal and the discrete grid. Moreover, the numerical simulations demonstrate that the proposed approach can substantially suppress the interferences with the duration up to 50% of the signal sweep based on the time sparsity assumption. Note that the proposed approach is readily to be extended to exploit the sparsity of the interference in a transformed domain by replacing the regularization term $| \mathbf { i } | _ { 1 }$ with the corresponding transformed counterpart $| \mathcal { T } ( \mathbf { i } ) | _ { 1 }$ . Finally, it should be mentioned that the three regularization parameters involved in the proposed approach affect both the convergence rate and its interference mitigation performance, which are usually empirically selected in practice. However, choosing the optimal values for them may be not trivial for practical applications. So how to automatically select the optimal values of these regularization parameters would be a further research topic in future.

![](images/ad7e7b6da9af299093c512a5a19edac7fb6c526d6017228ecca3b2e0d3462f86.jpg)  
(a)

![](images/d05456202565c2bd46a35410e20c46c4fab17063c5d7c402ffb4cebb32b2b3cc.jpg)  
(b)

![](images/16093a6729662620838810d91cac2f26f552915118f82d665d95bb27fd2d2f9b.jpg)  
(c)

![](images/8d46372d5c91187547d212eae74c4338342ca54628b3d494e1751ac0544cdc57.jpg)  
(d)

![](images/fd9cbbc0ba5749e29fdff65720b2f761cae2a2f384d481e7618aff8223b957e7.jpg)  
(e)

![](images/7e5b12d3bc9bb434cae921cd26d5592823312934400c64b5e1d94e7ab723b38a.jpg)  
(f)  
Fig. 10. Range-Doppler map of the rain. (a) is obtained with the raw data, (b) is formed with the signals recovered by the MP-based method, (c) ANC, (d)the RPCA-based method, (e) the SALSA-based method, and (f) the proposed approach.

## REFERENCES

[1] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geoscience and Remote Sensing Letters, vol. 15, no. 1, pp. 137–141, 2018.

[2] X. Zhang, D. Cao, and L. Xu, “Joint polarisation and frequency diversity for deceptive jamming suppression in MIMO radar,” IET Radar, Sonar Navigation, vol. 13, no. 2, pp. 263–271, 2019.

[3] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Transactions on Vehicular Technology, vol. 69, no. 1, pp. 270–281, 2020.

[4] Y. Kitsukawa, M. Mitsumoto, H. Mizutani, N. Fukui, and C. Miyazaki, “An interference suppression method by transmission chirp waveform with random repetition interval in fast-chirp FMCW radar,” in 2019 16th European Radar Conference (EuRAD), pp. 165–168.

[5] I. Artyukhin, V. Ermolaev, A. Flaksman, A. Rubtsov, and O. Shmonin, “Development of effective anti-interference primary signal processing for mmwave automotive radar,” in 2019 International Conference on Engineering and Telecommunication (EnT), pp. 1–5.

[6] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “Radchat: Spectrum sharing for automotive radar interference mitigation,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–14, 2019.

[7] S. Ishikawa, M. Kurosawa, M. Umehira, X. Wang, S. Takeda, and H. Kuroda, “Packet-based FMCW radar using CSMA technique to avoid narrowband interefrence,” in 2019 International Radar Conference (RADAR), pp. 1–5.

[8] R. W. Irazoqui and C. J. Fulton, “Spatial interference nulling before rf frontend for fully digital phased arrays,” IEEE Access, vol. 7, pp. 151261–151272, 2019.

[9] B. H. Kirk, J. W. Owen, R. M. Narayanan, S. D. Blunt, A. F. Martone, and K. D. Sherbondy, “Cognitive software defined radar: waveform design for clutter and interference suppression,” in Radar Sensor Technology XXI (K. I. Ranney and A. Doerry, eds.), vol. 10188, pp. 446 – 461, International Society for Optics and Photonics, SPIE, 2017.

[10] G. Solodky, O. Longman, S. Villeval, and I. Bilik, “CDMA-MIMO radar with the tansec waveform,” IEEE Transactions on Aerospace and Electronic Systems, vol. 57, no. 1, pp. 76–89, 2021.

[11] Z. Chen, F. Xie, C. Zhao, and C. He, “Radio frequency interference cancelation in high-frequency surface wave radar using orthogonal projection filtering,” IEEE Geoscience and Remote Sensing Letters, vol. 15, no. 9, pp. 1322–1326, 2018.

[12] T. Nozawa, Y. Makino, N. Takaya, M. Umehira, S. Takeda, X. Wang, and H. Kuroda, “An anti-collision automotive FMCW radar using time-domain interference detection and suppression,” in International Conference on Radar Systems (Radar 2017), pp. 1–5.

[13] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[14] G. Babur, Z. Wang, O. A. Krasnov, and L. P. Ligthart, “Design and implementation of cross-channel interference suppression for polarimetric LFM-CW radar,” Photonics Applications in Astronomy, Communications, Industry, and High-Energy Physics Experiments 2010, vol. 7745, p. 774520, 2010.

[15] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, pp. 1207–1220, March 2019.

[16] J. H. Choi, H. B. Lee, J. W. Choi, and S. C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Transactions on Communications, vol. E99B, no. 1, pp. 280–287, 2016.

[17] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Transactions on Microwave Theory and Techniques, pp. 1–1, 2021.

[18] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[19] J. Ren, T. Zhang, J. Li, L. H. Nguyen, and P. Stoica, “RFI mitigation for UWB radar via hyperparameter-free sparse SPICE methods,” IEEE Transactions on Geoscience and Remote Sensing, vol. 57, pp. 3105– 3118, June 2019.

[20] L. H. Nguyen and T. D. Tran, “RFI-radar signal separation via simultaneous low-rank and sparse recovery,” in 2016 IEEE Radar Conference (RadarConf), pp. 1–5, May 2016.

[21] J. Su, H. Tao, M. Tao, L. Wang, and J. Xie, “Narrow-band interference suppression via RPCA-based signal separation in time–frequency domain,” IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, vol. 10, no. 11, pp. 5016–5025, 2017.

[22] M. Li, Z. He, and S. Yang, “Transient interference and noise suppression by complex matrix recovery with hankel constraint,” IET Radar, Sonar & Navigation, vol. 9, no. 4, pp. 437–446, 2015.

[23] Y. Huang, G. Liao, Y. Xiang, Z. Zhang, J. Li, and A. Nehorai, “Reweighted nuclear norm and reweighted frobenius norm minimizations for narrowband RFI suppression on SAR system,” IEEE Transactions on Geoscience and Remote Sensing, pp. 1–14, 2019.

[24] S. Lee, J. Lee, and S. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Transactions on Intelligent Transportation Systems, pp. 1–11, 2019.

[25] Z. Liu, W. Lu, J. Wu, S. Yang, and G. Li, “A PELT-KCN algorithm for FMCW radar interference suppression based on signal reconstruction,” IEEE Access, vol. 8, pp. 45108–45118, 2020.

[26] E. J. Candes, X. Li, Y. Ma, and J. Wright, “Robust principal component\` analysis?,” J. ACM, vol. 58, pp. 11:1–11:37, June 2011.

[27] X. Ding, L. He, and L. Carin, “Bayesian robust principal component analysis,” IEEE Transactions on Image Processing, vol. 20, no. 12, pp. 3419–3430, 2011.

[28] Y. Hua and T. K. Sarkar, “Matrix pencil method for estimating parameters of exponentially damped/undamped sinusoids in noise,” IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 38, pp. 814–824, May 1990.

[29] K. H. Jin and J. C. Ye, “Sparse and low-rank decomposition of a Hankel structured matrix for impulse noise removal,” IEEE Transactions on Image Processing, vol. 27, pp. 1448–1461, March 2018.

[30] N. Srebro, Learning with Matrix Factorizations. Dissertation, 2004.

[31] M. Signoretto, V. Cevher, and J. A. K. Suykens, “An SVD-free approach to a class of structured low rank matrix optimization problems with application to system identification,” in CDC 2013.

[32] T. K. Sarkar and O. Pereira, “Using the matrix pencil method to estimate the parameters of a sum of complex exponentials,” IEEE Antennas and Propagation Magazine, vol. 37, pp. 48–55, Feb 1995.

[33] J. Wang, P. Aubry, and A. Yarovoy, “Wavenumber-domain multiband signal fusion with matrix-pencil approach for high-resolution imaging,” IEEE Transactions on Geoscience and Remote Sensing, vol. 56, pp. 4037–4049, July 2018.

[34] S. Boyd, N. Parikh, E. Chu, B. Peleato, and J. Eckstein, “Distributed optimization and statistical learning via the alternating direction method of multipliers,” Found. Trends Mach. Learn., vol. 3, p. 1–122, Jan. 2011.

[35] Z. Lin, M. Chen, and Y. Ma, “The augmented lagrange multiplier method for exact recovery of corrupted low-rank matrices,” 2010, arXiv:1009.5055.

[36] O. A. Krasnov, L. P. Ligthart, Z. Li, G. Babur, Z. Wang, and F. van der Zwan, “PARSAX: High-resolution doppler-polarimetric FMCW radar with dual-orthogonal signals,” in 18-th International Conference on Microwaves, Radar and Wireless Communications, pp. 1–5, 2010.