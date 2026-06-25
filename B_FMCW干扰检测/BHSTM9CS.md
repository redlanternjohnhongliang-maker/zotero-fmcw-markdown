# On the Fractional Fourier Transform for FMCW Radar Interference Mitigation

Christian Oswald

Josef Kulmer

Franz Pernkopf

Graz University of Technology

Infineon Technologies Austria AG

Graz University of Technology

Graz, Austria

Graz, Austria

Graz, Austria

https://orcid.org/0009-0006-9898-5865

https://orcid.org/0000-0001-9667-3135

https://orcid.org/0000-0002-6356-3367

Abstract—In this paper, we extend our method [1] for FMCW radar mutual interference mitigation (IM) based on the discrete fractional Fourier transform (DFrFT). Firstly, we propose a radar signal processing chain including our DFrFT-based IM for real-valued receivers, which we compare to reference algorithms on a synthetic data set. We then reduce computational complexity by reformulating DFrFT-based IM in terms of sparse update signals, which enables mitigation of multiple interferences simultaneously. Finally, we conduct a case study on measurement data and show that our method is compatible with real-world environments.

Index Terms—Frequency modulated continuous wave (FMCW) radar, digital I/Q, fractional Fourier transform, chirp interference, interference mitigation

## I. INTRODUCTION

In the automotive industry, FMCW radar is an essential component of advanced driver assistance systems, enabling applications such as adaptive cruise control, forward collision or lane departure warning systems. However, multiple such sensors might interfere with each other when transmitting in the same frequency band. The sensor signal corruptions caused by mutual interference are manifold and range from increased noise floors to ghost objects [2]. This necessitates the development of mutual interference mitigation schemes.

Most radar architectures contain in-phase and quadrature (I/Q) receivers [3] for reliable detection of echoes. However, the large-scale deployment of automotive radar sensors has driven the development of real-valued receivers. Their production is much cheaper because they only need one receiver processing chain and circumvent common imperfections such as I/Q-imbalance [3]. Therefore, mutual interference mitigation algorithms should be compatible with such radar architectures when designed for the automotive industry. The standard signal processing chain for FMCW radar with real-valued receivers is shown in Fig. 1a.

![](images/bfd7a9949e33e03ba7490a57229d968b224e7cd759a5805c075a390801d0a3aa.jpg)  
Fig. 1. FMCW radar signal processing chain for real-valued receivers without (a) and with (b) our proposed IM scheme. Our algorithm outputs rangespectra, meaning that we can remove the range-FFTs. The yellow blocks depict additional processing steps for our padding scheme described in Sec. III and [1]. If our method is used without padding, the yellow blocks are omitted. The dashed box encompasses all processing steps which are included in Alg. 1.

Many countermeasures against FMCW radar mutual interference have already been proposed. Besides interference avoidance [4], possible IM schemes include zeroing interferences in the time-domain [5], nonlinear filtering of rangespectra [6], variational signal separation [7], adaptive noise cancellation [8] and data driven approaches [9]–[11], among others. A more comprehensive analysis of existing IM algorithms can be found in [12].

The main contributions of our paper are: (i) We review key background concepts necessary to understand our approach (Sec. II). (ii) We propose a novel processing chain for realvalued receivers that incorporates DFrFT-based IM (Sec. III). (iii) We enhance the computational efficiency of the proposed method (Sec. IV). (iv) We validate our approach through experiments on both synthetic real-valued data and measured I/Q data (Sec. V).

We denote matrices with boldface uppercase and vectors as well as sets with boldface lowercase letters. $A [ n , m ]$ references the element of A in row n and column m. $A [ : , m ]$ is a column vector consisting of the $m ^ { \mathrm { t h } }$ column of A. A[n] is a column vector constructed from the $n ^ { \mathrm { t h } }$ row of A. Our notation and symbols used are consistent with [1].

## II. BACKGROUND

## A. Signal Model

We model radar signals s of length $N$ as a superposition of an object signal $_ { s _ { O } }$ with $N _ { I }$ interferences $s _ { I }$ and noise $\pmb { s } _ { \mathcal { N } }$

$$
\pmb { s } = \pmb { s } _ { O } + \sum _ { m = 1 } ^ { N _ { I } } \pmb { s } _ { I _ { m } } + \pmb { s } _ { \mathcal { N } } .\tag{1}
$$

Our model assumes I/Q signals, where all terms in (1) are complex-valued; the corresponding signal from a real-valued receiver then simply is $\Re \{ s \}$ . An object signal $_ { s _ { O } }$ sampled in intervals $T _ { s }$ consists of a superposition of $N _ { O }$ objects,

$$
s _ { O } [ n ] = \sum _ { i = 1 } ^ { N _ { O } } A _ { i } e ^ { j \left( \omega _ { i } n T _ { s } + \phi _ { i } \right) } ,\tag{2}
$$

where each object is parameterized by its echo amplitude $A _ { i } ,$ frequency $\omega _ { i }$ and initial phase $\phi _ { i }$ . Mutual interference appears as a complex-valued linearly frequency modulated (LFM) chirp $s _ { I }$ with amplitude A and initial phase $\phi _ { 0 }$

$$
s _ { I } [ n ] = \left\{ \begin{array} { l l } { A e ^ { j ( - 2 \pi k \tau n T _ { s } + \pi k n ^ { 2 } T _ { s } ^ { 2 } + \phi _ { 0 } ) } } & { \frac { \tau - B / k } { T _ { s } } < n < \frac { \tau + B / k } { T _ { s } } , } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.\tag{3}
$$

where B is the bandwidth of the ideal anti-aliasing filter, k the chirp rate of the interference and τ the time delay when the interferer and the victim radar’s instantaneous transmit frequency cross. We collect all sources of noise and clutter in s<sub>N</sub> modelled as additive complex-valued white Gaussian noise. Our signal model is identical to [1].

## B. The Discrete Fractional Fourier Transform

The discrete fractional Fourier transform (DFrFT) of fractional order $2 \alpha / \pi , \alpha \in \mathbb { R }$ , is a generalization of the the discrete Fourier transform (DFT) W , which can constructed via its eigendecomposition

$$
W ^ { \frac { 2 \alpha } { \pi } } = V \Lambda ^ { \frac { 2 \alpha } { \pi } } V ^ { T } ,\tag{4}
$$

where V and Λ are the DFT eigenvectors and eigenvalues, respectively. For more concise notation, we write $\bar { W } _ { \alpha } : = W ^ { \frac { 2 \alpha } { \pi } }$ and $\Lambda _ { \alpha } : = \Lambda ^ { \frac { 2 \alpha } { \pi } }$ , where $\alpha$ is the so-called fractional angle. The DFT eigenvectors are not unique, but if V is chosen to approximate the Hermite-Gauss functions, $W _ { \alpha }$ compresses a complex-valued LFM chirp with chirp rate cot(α) into a small number of samples. Equivalently, such a DFrFT can be interpreted as rotating a signal’s time-frequency representation by α radians; an example can be seen in Fig. 2a and Fig. 2b. Surveys on the DFrFT and its applications can be found in [13], [14].

## C. Interference Mitigation using the DFrFT

In [1] we proposed a method that compresses, detects and subsequently zeroes LFM interference chirps in I/Q signals using the DFrFT. We simultaneously compute the DFrFTs of M, N mod $M ~ = ~ 0$ , fractional angles equally spaced between −π and π radians with our efficient multiangle DFrFT (EMDFrFT), which is an adaptation of the multiangle centered DFrFT in [15]. The EMDFrFT S of a signal s˜ is given as

$$
\begin{array} { r } { \pmb { \rho } = \pmb { V } ^ { T } \tilde { \pmb { s } } , } \end{array}\tag{5}
$$

$$
\bar { Z } [ p , n ] = { V } ^ { T } [ p , n ] \rho [ p ] ,\tag{6}
$$

$$
\pmb { S } [ m , n ] = \mathrm { F F T } _ { m } \left\{ \sum _ { l = 0 } ^ { \frac { N } { M } - 1 } \bar { \pmb { Z } } [ m + l M , n ] \right\} ,\tag{7}
$$

where $n , p \in \{ 0 , 1 , . . . , N - 1 \} , m \in \{ 0 , 1 , . . . , M - 1 \}$ , and $\mathrm { F F T } _ { m } \{ \cdot \}$ computes column-wise FFTs of its input matrix. Note that the algorithm by [15] efficiently computes the multiangle centered DFrFT; however, in [16] we derive the multiangle (standard) DFrFT with identical complexity.

We then search for the global maximum $S [ \hat { m } , \hat { n } ]$ within our search space,

$$
\hat { m } , \hat { n } = \arg \operatorname* { m a x } \{ M \odot | S [ m , n ] | \} ,\tag{8}
$$

where ⊙ denotes element-wise multiplication and M is a binary mask restricting the fractional angles in our search space such that they are bounded by $\pm \alpha _ { \mathrm { m a x } }$ , which is hyperparameter of our method. We then classify $S [ \hat { m } , \hat { n } ]$ using a least-of constant false alarm rate (LO-CFAR) detector. This detector uses Φ samples of $S [ \hat { m } ]$ surrounding $S [ \hat { m } , \hat { n } ]$ with a distance of $G$ guard cells as its noise estimation window. If the signal-to-noise ratio (SNR) corresponding to $S [ \hat { m } , \hat { n } ]$ is above the detector’s threshold $\beta ,$ we set $S [ \hat { m } , \hat { n } ]$ and the surrounding G guard cells to zero; we formalize this zeroing operation with a binary detection mask $^ { d , }$

$$
\pmb { d } = \mathrm { L O - C F A R } ( S [ \hat { m } ] , \hat { n } ) ,\tag{9}
$$

where $d [ n ]$ is 0 for n we want to zero and 1 otherwise, and restart the process at (5) with an updated $\tilde { \pmb { s } } \gets \pmb { d } \odot \pmb { S } [ \hat { m } ]$ . We loop this procedure of compression, detection and zeroing until the SNR corresponding to the global maximum is below $\beta ;$ then we terminate the algorithm and return the interference mitigated range-spectrum. We expect this algorithm to loop $N _ { I }$ -times on a fast-time sequence s contaminated by $N _ { I }$ interference chirps. Assuming $M \ \ll \ N .$ , the algorithm’s computational complexity is $\mathcal { O } ( N _ { I } N ^ { 2 } / 2 )$ , since the most expensive operation is the matrix-multiplication (5); as shown in [15], V is symmetric, which allows us to roughly halve the complexity from a dense matrix multiplication to $\mathcal { O } ( N ^ { 2 } / 2 )$ – the same optimization is possible for (6). Meanwhile, we showed in [16] that we only require approximately $N / 2$ instead of N FFTs to compute (7). A detailed explanation of our method as well as pseudo-code can be found in [1].

## III. REAL-VALUED INTERFERENCE MITIGATION

Since every real-valued signal is equivalent to the sum of a complex-valued signal and its complex conjugate, the socalled image component, the EMDFrFT of a real-valued signal is Hermite-symmetric about a fractional angle of 0 and 180 degrees. In other words, the DFrFT cannot compress realvalued LFM chirps into pulses because it has complex-valued LFM chirps as its basis functions. This fundamental problem is closely related to the reduced SNR in the output of matched filters applied to real-valued or I/Q-imbalanced signals, where the image component appears as an increased noise floor [3], [17]. Furthermore, a complex-valued interference chirp and its image component cannot be separated at any fractional angle, which means that zeroing one component alters the appearance of its image. The image therefore becomes an incomplete interference as discussed in [1], which renders it undetectable in the worst case. Therefore, we propose to use digital I/Q demodulation [3] as a preprocessing step before DFrFT-based interference mitigation. Our proposed processing chain is depicted in Fig. 1b.

(b)  
(a)  
![](images/a55048afa2e8a81f3a5fb15d80cfd6b4ac2a3fb9e9925297f02234466a917be1.jpg)

![](images/76fb71fac784966176ba67a70ce580fa5cb07d17da5bc9208a45bb85abf1830b.jpg)  
(c)  
(d)  
Fig. 2. (a) STFT of an interfered digital I/Q signal s and (b) STFT of $W _ { \hat { \alpha } } s$ with $\hat { \alpha } \approx - 5 0 ^ { \circ }$ rotating the time-frequency representation of $\mathbf { \index { s . } } ~ W _ { \hat { \alpha } } { \mathbf { \index { s } . } }$ compresses one of the LFM chirps into a pulse, which is also visible at the corresponding location in (c), the EMDFrFT magnitudes |S| of s. If we now zero that compressed chirp and recompute the EMDFrFT, we get (d); notice how the peak corresponding to the other chirp has not changed, as the two interference chirps are separable. Therefore, we can zero both chirps in the same iteration of our algorithm as explained in Sec. IV-A; s has been padded according to Sec. III. All plots are in dB and renormalized such that the maximum value is 0.

Digital I/Q demodulation generates I and Q components from a real-valued receive signal after A/D conversion; more specifically, it discards one sideband and centers its complementary half around DC. There exist various architectures which efficiently implement such a scheme [3], [18], [19]. After digital I/Q, real-valued interference chirps appear as two consecutive complex-valued chirps, which we can mitigate independently. An interfered signal after digital I/Q and its EMDFrFT are depicted in Fig. 2a and Fig. 2c, respectively. Hypothetically, the real-valued interference chirp’s components could also be separated by computing the receive signal’s analytic representation via a Hilbert-transform; however, these interference components do not span the entire bandwidth, i.e., they are again incomplete, meaning that they cannot be optimally compressed by any DFrFT. Therefore, digital I/Q is preferable to analytic signals as preprocessing for DFrFTbased IM. Since interferences mostly appear as V-shapes in the short-time Fourier transform (STFT) of the digital I/Q signal, we expect our DFrFT-based IM method to iterate, at maximum, twice as often as on the corresponding I/Q received data. We deal with this increased computational load in Sec. IV by reformulating our algorithm in terms of sparse update signals, enabling simultaneous processing of these separable chirps such that the number of iterations is the same as on the corresponding I/Q received signal.

In [1] we observed that signal components located at the corners of its time-frequency representation cannot be properly compressed by a DFrFT; therefore, we proposed increasing the A/D-converter’s sampling rate and zero-padding the input signal before computing its EMDFrFT. Oversampling can be implemented by adapting processing blocks within architectures such as [18], [19]. Such oversampling avoids that digital I/Q maps DC components of the real-valued receive signal to the Nyquist frequency. An example for a sufficiently padded digital I/Q signal can be seen in Fig. 2a.

## IV. INCREASED EFFICIENCY THROUGH MITIGATION INTHE DFT EIGENBASIS

In this section we reformulate our DFrFT-based IM algorithm [1] to mitigate separable interferences simultaneously while computing successive iterations more efficiently. As derived in [1], the time-domain signals $\mathbf { \boldsymbol { s } } _ { i }$ and $s _ { i + 1 }$ before iterations i and $i + 1$ of our algorithm are related by

$$
\begin{array} { r l } & { s _ { i + 1 } = W _ { - \hat { \alpha } _ { i } } \big ( { d _ { i } } \odot ( W _ { \hat { \alpha } _ { i } } s _ { i } ) \big ) } \\ & { \qquad = s _ { i } - W _ { - \hat { \alpha } _ { i } } \big ( ( 1 - { d _ { i } } ) \odot ( W _ { \hat { \alpha } _ { i } } s _ { i } ) \big ) , } \end{array}\tag{10}
$$

where the binary mask $\mathbf { \ b { d } } _ { i }$ zeroes some compressed interference chirp with chirp rate cot( ˆα<sub>i</sub>). We define $\gamma _ { i } = \left( 1 - d _ { i } \right) \odot \left( W _ { \hat { \alpha } _ { i } } \pmb { s } _ { i } \right)$ for more concise notation; the eigen-coefficients ${ \pmb \rho } _ { i } = { \pmb V } ^ { T } { \pmb s } _ { i }$ and $\pmb { \rho } _ { i + 1 } = \pmb { V } ^ { T } \pmb { s } _ { i + 1 }$ relate via

$$
\begin{array} { r l } & { \rho _ { i + 1 } = \pmb { \rho } _ { i } - \pmb { V } ^ { T } \pmb { W } _ { - \hat { \alpha } _ { i } } \gamma _ { i } } \\ & { \qquad \stackrel { ( 4 ) } { = } \pmb { \rho } _ { i } - \pmb { V } ^ { T } \pmb { V } \pmb { \Lambda } _ { - \hat { \alpha } _ { i } } \pmb { V } ^ { T } \gamma _ { i } } \\ & { \qquad = \pmb { \rho } _ { i } - \pmb { \Lambda } _ { - \hat { \alpha } _ { i } } \pmb { V } ^ { T } \gamma _ { i } , } \end{array}\tag{11}
$$

where $V ^ { T } V$ is the identity due to V being orthonormal [1]. This means that we can compute iterations of our algorithm by subtracting a scaled projection of the detected interference chirp from $\rho _ { i } .$ which has already been evaluated in the previous iteration. This is more efficient than the formulation presented in [1], because $V ^ { T } \gamma _ { i }$ has complexity ${ \mathcal { O } } ( ( 2 G + 1 ) \cdot N )$ $N \gg G , \mathrm { a s \ 1 } - d _ { i }$ sets all except $2 G + 1$ values of $W _ { \hat { \alpha } _ { i } } s _ { i }$ to zero; meanwhile, [1] evaluates $V ^ { T } ( d _ { i } \odot ( W _ { { \hat { \alpha } } _ { i } } \pmb { s } _ { i } ) )$ in every iteration which has complexity $\mathcal { O } ( ( N - 2 G - 1 ) \cdot N )$

(when ignoring the special structure of V ). In our experiments conducted in Sec. $\mathrm { v } , G = 1 0$ while $N = 8 9 6$ , which means that our new formulation results in a 42-fold reduction in the number of operations for computing $\rho _ { i + 1 }$ when $i \geq 1$ For $\begin{array} { r l r } { i } & { { } = } & { 0 , } \end{array}$ we still need to compute $\begin{array} { r } { \rho _ { 1 } ~ = ~ V ^ { T } s _ { 1 } } \end{array}$ with complexity $\mathcal { O } ( N ^ { 2 } / 2 )$ . Since $\pmb { \Lambda } _ { - \hat { \alpha } _ { i } }$ is a diagonal matrix, its product with $\dot { \boldsymbol { V } } ^ { T } \dot { \boldsymbol { \gamma } } _ { i }$ has negligible complexity. Overall, the computational complexity remains $\mathcal { O } ( \bar { N _ { I } } N ^ { 2 } / 2 )$ because of (6), which consists of $\dot { N ^ { 2 } } / 2$ multiplications [15] and is now the most expensive operation in our algorithm.

Since all $\rho$ are projections of time-domain signals, the circular shifting of the row indices in successive iterations as described in [1] vanishes. This is because in (11) the inverse DFrFT matrix $W _ { - \hat { \alpha } _ { i } }$ transforming $\gamma _ { i }$ back into the time-domain becomes the diagonal matrix $\pmb { \Lambda } _ { - \hat { \alpha } _ { i } }$ in the DFT eigenbasis.

## A. Mitigating multiple interferences simultaneously

As discussed in Sec. III, after digital I/Q, real-valued LFM chirp interference appears as two consecutive complex chirps which we can mitigate independently. In other words, there exists a fractional Fourier domain where these two chirps are separable since they do not cross in the time-frequency plane. For instance, if we zero out one interference component in Fig. 2b according to our method and then compute another EMD-FrFT depicted in Fig. 2d, we notice that the appearance of the other interference component has not changed. Therefore, we can simply zero both interference components in the same iteration. In fact, such separable interferences also appear in I/Q received data; examples would be a signal interfered by two chirps with the same chirp rate, or the interferences in Fig. 2c of [1]. We implement simultaneous mitigation by looping (8) and (9) until the detector returns no interference. After every iteration of this new inner loop we mask $S \gets M \odot S$ to only include chirps $S [ m , n ]$ that are separable from the previous global maximum<sup>1</sup>. M is constructed from a global maximum $S [ \hat { m } , \hat { n } ]$ by setting all $M [ m , n ]$ to zero where the chirp corresponding to $S [ \hat { m } , \hat { n } ]$ is present, while all other entries are one; we denote this mask construction procedure as NotSupportOfChirp() in Alg. 1. All possible M corresponding to all possible pairs of mˆ and nˆ can be precomputed and stored in lookup tables; we only need to store $N / 2$ such masks (where masks corresponding to neighboring column indices are almost identical) thanks to the rotation symmetry within the EMDFrFT. We collect all $N _ { p }$ separable interferences in their respective fractional domains $\hat { \pmb { \alpha } } _ { i }$ in $\mathbf { { { I } } } _ { i } .$ . All chirps are then mitigated simultaneously through

$$
\pmb { \rho } _ { i + 1 } = \pmb { \rho } _ { i } - \sum _ { k = 0 } ^ { N _ { p } - 1 } \pmb { \Lambda } _ { - \hat { \alpha } _ { i } [ k ] } \pmb { V } ^ { T } \pmb { \Gamma } _ { i } [ k ]\tag{12}
$$

replacing (11). Note that this parallelism is enabled by (11) and is not possible with the formulation in [1]. Mitigating separable interferences simultaneously using (12) is equivalent to mitigating one interference per iteration using (11). However, the LO-CFAR detector might return false negatives due to the increased noise estimate caused by the other interferences; in that case, the interference will only be detected in the next iteration. The false negative rate could be lowered by designing more elaborate detectors. Further optimizations are possible for digital I/Q signals where, due to their Vshape, the two peaks corresponding to the two LFM chirps always appear as predictable pairs within the EMDFrFT; we leave these ideas for further research. Our method’s overall computational complexity is $\mathcal { O } ( N ^ { 2 } / 2 )$ if all $N _ { I }$ interferences are separable and $\bar { \mathcal { O } } ( N _ { I } \bar { N } ^ { 2 } / 2 )$ if none of them are separable. Note that this improved formulation can still be combined with other potential speed-ups listed in [1], for example by using DFT eigenvectors with sparse and repeating entries [20] or eigenvectors such as [21] where the change-of-basis can be computed in O(N log N) [22].

## B. Algorithm

Our method including simultaneous processing of separable interferences is summarized in Alg. 1. The $M \times N$ matrix K implements the sum within (7) and consists of $N / M$ concatenated $M \times M$ identity matrices. We stack $\rho \ N / 2 \cdot$ −times resulting in the $N \times N / 2$ matrix $\left[ \rho \dots \rho \right]$ to implement (6) with optimizations from [15], while Rearrange() indicates the reconstruction of the full $M \times N$ EMDFrFT after computing $N / 2$ M-point FFTs as described in [16]. We apply the window function w to every s before DFrFT-based IM. All hyperparameters are listed in Tab. I.

```latex
Algorithm 1 Simultaneous IM in the DFT Eigenbasis
IMFRACV2(s): {s is possibly interfered}
initialize α {array of the fractional angles evaluated}
initialize M {mask for restricting S, see [1] and Sec. IV-A}
initialize m<sub>RS</sub> {row index of range-spectrum in S}
s ← s ⊙ w {apply window function}
s ← ZeroPad(s) {optional, see [1] and Sec. III}
$\rho = V ^ { T } s$ {initial change-of-basis}
do
$S \gets \mathrm { R e a r r a n g e } ( \mathrm { F F T } _ { m } \{ K ( V ^ { T } \odot [ \pmb { \rho } \ . . . \ \pmb { \rho } ] ) \} )$
do {All updates for ρ can be computed in parallel}
m,ˆ nˆ ← arg max|M ⊙ S|
d ← LO-CFAR(S[ ˆm], nˆ) {d is a binary mask}
$\pmb { \rho } \gets \pmb { \rho } - \pmb { \Lambda } _ { - \alpha [ \hat { m } ] } \pmb { V } ^ { T } ( ( 1 - \pmb { d } ) \odot \pmb { S } [ \hat { m } ] )$
M ← M ∧ NotSupportOfChirp( ˆm, nˆ)
while d contains a detection (i.e., a zero)
M ← reset(M ) {restrict S to angles α, see [1]}
while ρ has changed in previous iteration
$\pmb { s } _ { R S } \gets \mathrm { C r o p } ( S [ m _ { R S } ] )$ {optional, see [1] and Sec. III}
s<sub>RS</sub> ← LowPass(s<sub>RS</sub>) {optional, see [1] and Sec. III}
return $s _ { R S }$ {interference mitigated range-spectrum}
```

TABLE I PARAMETERS OF IMFRAC
<table><tr><td rowspan=1 colspan=2>Parameter</td></tr><tr><td rowspan=1 colspan=1># Computed fractional angles by EMDFrFT (M)</td><td rowspan=1 colspan=1>256</td></tr><tr><td rowspan=1 colspan=1>Maximum fractional angle $\overline { { ( \alpha _ { \mathrm { m a x } } ) } }$ </td><td rowspan=1 colspan=1>80°</td></tr><tr><td rowspan=1 colspan=1>Window-size interference detector (Φ)</td><td rowspan=1 colspan=1>N/2 − G − 1</td></tr><tr><td rowspan=1 colspan=1># Guard cells of interference detector (G)</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>Threshold of interference detector (β)</td><td rowspan=1 colspan=1>20 dB</td></tr></table>

## V. EXPERIMENTS

## A. Performance on synthetic digital I/Q dataset

We evaluate our proposed processing chain including IM for real-valued receivers, labelled IMfrac, on a synthetic dataset consisting of 250 interfered and ground-truth range-Doppler (RD) maps. The dataset has the same parameters as the dataset in [1], except that we increased the number of fasttime samples from 512 to 1024 and only use their real part. We generated the corresponding digital I/Q signals of length 512 by discarding the lower sideband via an intermediate forward and inverse FFT. Furthermore, we used a steep highpass filter to simulate the DC suppression of digital I/Q processing chains such as [18], [19] that eliminate the side effects of non-ideal mixers [3]. Furthermore, we generated padded digital I/Q signals of length 896 by oversampling and zero-padding. Fig. 2a is one interfered fast-time sequence from our dataset. In addition to Alg. 1 we evaluate an oracle variant of IMfrac, which we describe in [1] in more detail. We compare our processing chain to ramp filtering [6] and zeroing [5] with oracle as well as envelope change point interference detection and evaluate the mean squared error (MSE), the signal-to-interference-plus-noise (SINR) ratio, the error vector magnitude (EVM), the true positive rate (TPR), the false alarm rate (FAR) and the F1-score per RD map in the dataset. The hyperparameters of IMfrac in Tab. I, the reference IM methods and metrics are the same as in [1]. Compared to [1], zeroing has been altered such that interference detection is performed on the signals’ envelope.

The results are collected in Fig. 3. Our DFrFT-based IM algorithm outperforms the reference methods across all metrics. Compared to the results on I/Q received data in [1], padding becomes more important as digital I/Q data contains highenergy components with high negative frequencies (see Fig. 2a for instance). A low MSE does not necessarily lead to good object detection performance, as visible in Fig. 3a and Fig. 3f for zeroing with oracle detection.

## B. Case Study on Measurement Data

In this section we qualitatively analyze our DFrFT-based IM method on I/Q-modulated measurement data provided in [23]. We compare measurement frames #2001 and #2002 of the first receiver and assume that the object’s locations on the RD maps are the same. Since the sensor’s number of fast-time samples is 512, we can apply DFrFT-based IM with the parameter settings from Tab. I. We implement our padding scheme by upsampling the fast-time sequences before windowing and zero-padding, which results in 896 fast-time samples. Our findings are summarized in Fig. 4. The measured interference closely resembles an ideal complex-valued LFM chirp, which is easily detected and mitigated. Qualitatively, the interference mitigated and the reference RD-maps #2001 and #2002 closely match. We hypothesize that the fluctuations in amplitude of the interfered range-spectrum in Fig. 4h is caused by an imperfect anti-aliasing filter as well as multipath propagation of the interference. Although the range-spectra in Fig. 4h cannot be directly compared, the object peaks previously masked by interference have been reconstructed almost perfectly.

## VI. CONCLUSION

In this paper, we have extended our IM method based on the DFrFT [1] to real-valued receivers, presented a more efficient formulation and conducted a case study on measurement data. However, we did not yet discuss multipath channels and imperfections of the sensor, such as interferences saturating the receiver. Nevertheless, we are convinced that this paper is an important step towards a practical and performant algorithm for LFM chirp interference mitigation.

## REFERENCES

[1] C. Oswald and F. Pernkopf, “FMCW radar interference mitigation based on the fractional Fourier transform,” IEEE Transactions on Radar Systems, vol. 4, pp. 549–563, 2026.

[2] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical investigation of non-coherent mutual FMCW radar interference,” in 2018 15th European Radar Conference (EuRAD). IEEE, 2018, pp. 71–74.

[3] M. A. Richards et al., Fundamentals of radar signal processing. Mcgraw-hill New York, 2005, vol. 1.

[4] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in 2016 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM). IEEE, 2016, pp. 1–4.

[5] C. Fischer, Untersuchungen zum Interferenzverhalten automobiler Radarsensorik. Cuvillier Verlag, 2016.

[6] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS). IEEE, 2018, pp. 1–4.

[7] M. Toth, E. Leitinger, and K. Witrisal, “Variational signal separation for automotive radar interference mitigation,” IEEE Transactions on Radar Systems, vol. 2, pp. 1007–1026, 2024.

[8] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[9] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall). IEEE, 2020, pp. 1–5.

[10] C. Oswald, M. Toth, P. Meissner, and F. Pernkopf, “Angle-equivariant convolutional neural networks for interference mitigation in automotive radar,” in 2023 20th European Radar Conference (EuRAD). EuMA, 2023.

[11] ——, “End-to-end training of neural networks for automotive radar interference mitigation,” in 2023 IEEE International Radar Conference (RADAR). IEEE, 2023, pp. 1–6.

[12] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in 2019 IEEE Radar Conference (RadarConf). IEEE, 2019, pp. 1–6.

[13] X. Su, R. Tao, and X. Kang, “Analysis and comparison of discrete fractional Fourier transforms,” Signal Processing, vol. 160, pp. 284– 298, 2019.

![](images/9c21da77134248cb96a5b917845659ef198110678f6a474e3709ae807d49b8ee.jpg)  
(a)

![](images/5771a7be22c168fde09be05b65d3598b0ae3ad41ee483681fce4e85df84eadc8.jpg)

![](images/571d6c63eb9861c28d9b0275a184c029329c5378ecce9635ebfe678e6a735c1d.jpg)

![](images/1b12da81e8edfc637e548a0fafec33c81d76670a955003eca1e5113fa113e4fb.jpg)  
(d)

(c)  
(b)  
![](images/d23e7e69020c2d2bc4cd61d1195d8b4ef4f290fd5d233163479c205c41e66bde.jpg)

![](images/d0a9393368a85de3f503d7f883de7f3bbd63cd8c93d47b3a9dd74ca2fa8d8b2d.jpg)  
(f)

Fig. 3. Empirical cumulative density functions (ECDFs) of all evaluated metrics per range-Doppler map. The oracle methods are drawn with dashed lines. Note that we have zoomed into relevant parts of the ECDFs to better resolve close-by curves.  
![](images/2a0d9848a34165aad33a2818171968a9fee1011ea2973dec1981934fcf92b160.jpg)

![](images/39b1dd83804b1b4a177fef9f199e83f83b7b138d532c296884b6e04b05961d4d.jpg)

![](images/810a49fc67b534d3c4ebf183a805323786f998ae40d32e7bb264cda29c668773.jpg)

![](images/1f6ac186823a133ed3d1c8d7cb05d06a3d1698c7be68fda2eb6e1b7615dd35cc.jpg)

![](images/7b621dd11032a038a175a9142e1d794af7bb81a4013fbac63c9c7c8bc6c96083.jpg)  
(e)

(b)  
![](images/6b30144b9c3fde475ba5ae93b1e308b86b5b1c64b37ea29199fb2d764928a673.jpg)  
(f)

(c)  
![](images/b1f9f4204475dd928524959f56d717b59e2d185c576141e57f756e5ad9c5f1c2.jpg)  
(g)

(d)  
![](images/7c9931fe402cbde21d7641eb4664289e3a620b246b3b632ec31703690aa3b741.jpg)  
(h)  
Fig. 4. Case study on interfered measurement data from [23]. (a) Measurement setup; STFT of ramp #23 of frame #2001 before (b) and after (c) interference mitigation with our method. (d) overlay of interfered and interference mitigated range-spectra of frame #2001 ramp #23 with reference #2002 ramp #23. (e) fast-time/slow-time sequence and (f) RD map of the interfered measurement frame #2001. (g) RD map of the reference measurement frame #2002. (h) interference mitigated RD map #2001. All plots have been normalized such that the maximum value has 0 decibels.

[14] A. Gomez-Echavarr ´ ´ıa, J. P. Ugarte, and C. Tobon, “The fractional´ Fourier transform as a biomedical signal and image processing tool: A review,” Biocybernetics and Biomedical Engineering, vol. 40, no. 3, pp. 1081–1093, 2020.

[15] J. G. Vargas-Rubio and B. Santhanam, “On the multiangle centered

discrete fractional Fourier transform,” IEEE Signal Processing Letters, vol. 12, no. 4, pp. 273–276, 2005.

[16] C. Oswald and F. Pernkopf, “On multiangle discrete fractional periodic transforms,” in ICASSP 2026 - 2026 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2026, pp. 581–585.

[17] A. I. Sinsky and P. C. Wang, “Error analysis of a quadrature coherent detector processor,” IEEE Transactions on Aerospace and Electronic Systems, no. 6, pp. 880–883, 1974.

[18] C. M. Rader, “A simple method for sampling in-phase and quadrature components,” IEEE Transactions on Aerospace and Electronic Systems, no. 6, pp. 821–824, 1984.

[19] G. A. Shaw and S. Pohlig, “I/Q baseband demodulation in the RASSP SAR benchmark,” 1995.

[20] J. R. de Oliveira Neto, J. B. Lima, G. J. da Silva Jr, and R. M. C. de Souza, “Computation of an eigendecomposition-based discrete fractional Fourier transform with reduced arithmetic complexity,” Signal Processing, vol. 165, pp. 72–82, 2019.

[21] T. Erseghe and G. Cariolaro, “An orthonormal class of exact and simple DFT eigenvectors with a high degree of symmetry,” IEEE transactions on signal processing, vol. 51, no. 10, pp. 2527–2539, 2003.

[22] ——, “Efficient DFT architectures based upon symmetries,” IEEE transactions on signal processing, vol. 54, no. 10, pp. 3829–3838, 2006.

[23] L. A. Lopez-Valc ´ arcel, M. Garc ´ ´ıa Sanchez, F. Fioranelli,´ and O. A. Krasnov, “Raw ADC data from FMCW radar at 77 GHz with interference,” 2023. [Online]. Available: https://dx.doi.org/10.21227/e47t-p857