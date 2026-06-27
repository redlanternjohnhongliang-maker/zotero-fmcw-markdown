# Neurally Augmented Deep Unfolding for Automotive Radar Interference Mitigation

Citation for published version (AF Citation for published version (APA):

Overdevest, J., Koppelaar, A. G. C., Youn, J., Wei, X., & van Sloun, R. J. G. (2024). Neurally Augmented Deep Unfolding for Automotive Radar Interference Mitigation. , , 712-724. Article 10634141. https://doi.org/10.1109/TRS.2024.3442692

Document license: TAVERNE

DOI: 10.1109/TRS.2024.3442692

Document status and date: Published: 01/01/2024

Document Version: Publisher’s PDF, also known as Version of Record (includes final page, issue and volume numbers)

Please check the document version of this publication:

• A submitted manuscript is the version of the article upon submission and before peer-review. There can be important differences between the submitted version and the official published version of record. People interested in the research are advised to contact the author for the final version of the publication, or visit the DOI to the publisher's website.

• The final author version and the galley proof are versions of the publication after peer review.

• The final published version features the final layout of the paper including the volume, issue and page numbers.

Link to publication

## General rights

Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognise and abide by the legal requirements associated with these rights.

• Users may download and print one copy of any publication from the public portal for the purpose of private study or research.

• You may not further distribute the material or use it for any profit-making activity or commercial gain

• You may freely distribute the URL identifying the publication in the public portal.

If the publication is distributed under the terms of Article 25fa of the Dutch Copyright Act, indicated by the “Taverne” license above, please follow below link for the End User Agreement:

www.tue.nl/taverne

## Take down policy

If you believe that this document breaches copyright please contact us at:

openaccess@tue.nl

providing details and we will investigate your claim.

# Neurally Augmented Deep Unfolding for Automotive Radar Interference Mitigation

Jeroen Overdevest , Student Member, IEEE, Arie G. C. Koppelaar , Jihwan Youn , Xinyi Wei , and Ruud J. G. van Sloun , Member, IEEE

Abstract— The proliferation of active radar sensors deployed in vehicles has increased the need for mitigating automotive radarto-radar interference. While simple avoidance and mitigation methods are still effective today, the expected crowded spectrum allocations pose new challenges that likely require more sophisticated techniques. In particular, interference mitigation methods that can handle significant levels of radar signal corruption are required. To this end, we propose neurally augmented analytically learned fast iterative shrinkage thresholding algorithm (NA-ALFISTA), which is a neural network-based solution for reconstructing time-domain radar signals by leveraging sparsity in the range–Doppler map (RDM). The neural augmentation network is deployed as a single gated recurrent unit (GRU) cell that captures the radar signal statistics along the unfolded layers of fast-iterative shrinkage thresholding algorithm (FISTA)-based sparse recovery, which significantly boosts the convergence rate. It estimates the next layer’s parameters necessary in ALFISTA based on the previous layer’s output. The proposed method is compared to state-of-the-art detect-and-repair methods and source separation methods in simulated data and real-world measurements.

Index Terms— Automotive radar, deep unfolding, interference mitigation.

## NOMENCLATURE

$f _ { C }$ Carrier frequency.

$B$ Chirp bandwidth.

$T _ { C }$ Chirp duration.

$T _ { \mathrm { P R I } }$ Pulse repetition interval.

$H , L$ Number of targets and interferers.

$s , i , w$ Source (target) signal, interference signal, and noise.

$k , K$ Iteration/layer index and total number of iterations/layers.

$h , l$ Target and interferer index.

n, m Tx and Rx antenna index.

Manuscript received 15 March 2024; revised 31 May 2024; accepted 6 August 2024. Date of publication 12 August 2024; date of current version 30 August 2024. This work was supported by the Robust AI for SafE Signal Processing (RAISE) Collaboration Framework between Eindhoven University of Technology and NXP Semiconductors N.V., including a Private-Public Partnerships Surcharge (PPPS)-supplement from the Dutch Ministry of Economic Affairs and Climate Policy. (Corresponding author: Jeroen Overdevest.)

Jeroen Overdevest is with NXP Semiconductors N.V., 5656 AG Eindhoven, The Netherlands, and also with the Signal Processing Systems (SPS) Group, Eindhoven University of Technology, 5612 AP Eindhoven, The Netherlands (e-mail: jeroen.overdevest@nxp.com).

Arie G. C. Koppelaar and Jihwan Youn are with NXP Semiconductors N.V., 5656 AG Eindhoven, The Netherlands.

Xinyi Wei and Ruud J. G. van Sloun are with the Signal Processing Systems (SPS) Group, Eindhoven University of Technology, 5612 AP Eindhoven, The Netherlands.

Digital Object Identifier 10.1109/TRS.2024.3442692

p, q Slow-time/fast-time index.

$d , D$ Number of clean samples in a single chirp/frame.

$N _ { C } , N _ { F }$ Number of slow-/fast-time samples.

$N _ { T } , N _ { R }$ Number of Tx/Rx antennas.

$\mathbf { Y } _ { m }$ mth antenna data matrix (slow/fast time). $\mathbf { S } _ { m }$ mth antenna target-only signal (slow/fast time).

$\mathbf { I } _ { m }$ mth antenna interference-only (slow/fast time).

$\mathbf { W } _ { m }$ mth antenna thermal noise (slow/fast time).

M Interference detection mask (slow/fast time).

$\mathbf { U } , \mathbf { V }$ Left and right unitary matrices in SVD.

$\mathbf { X } _ { m }$ mth antenna RDM.

$r$ Interference distortion ratio.

$\lambda$ Threshold scalar.

$\mu$ Step size.

$\rho$ Momentum term.

## I. INTRODUCTION

ADAR has become an essential sensor in advanced driver-assisted system (ADAS) applications and is indispensable for realizing full autonomous vehicles. Its direct velocity estimation capability and its robustness to extreme weather and light conditions are superior to other sensor modalities, such as camera or lidar [1]. A drawback of radar is its susceptibility to interfering signals from other nearby, active radar sensors that share similar time, frequency, and spatial resources [2], [3]. However, several ADAS applications request for high-performance automotive radars with enhanced azimuthal and elevational angular resolutions to achieve lidarlike performance [4], i.e., imaging radars, which has resulted in more enhanced waveforms that utilize dense time–frequency waveforms allocations. Along with these larger multipleinput–multiple-output (MIMO) implementations, the rapid deployment of multiple automotive radars per vehicle will soon result in scarce unoccupied time–frequency resources for the radars to operate on. Currently, frequency-modulated continuous-wave (FMCW) radars are actively used, and hence, academia and industry focused mainly on FMCW-to-FMCW radar interference mitigation [5], [6].

The collaborative IMIKO project proposed cooperative solutions for standardization to minimize the probability of mutual interference occurrence [7]. The adoption of cooperative methods has been explored and several co-existing methods are effective for avoiding radar interference, e.g., multihop communications [8], [9], compass method and random frequency hopping [10], and bat-inspired frequency hopping [11]. These coordination measures are mostly FMCW-oriented. However, in today’s market, the absence of standardization allows any radar to freely operate without conforming to the de facto chirp-like signals. In particular, digitally modulated radars can severely impact the performance of the legacy FMCW radars with its continuous and broadband transmission [12], when used in the 76–81-GHz spectrum allocation [13]. The transmit schemes of these digital waveforms (e.g., phase-modulated continuous wave (PMCW) and orthogonal frequency-division multiplexing (OFDM) [3], [14], [15]) can potentially pollute many consecutive time-domain samples in FMCW radars.

FMCW radar interference has been studied since its early deployment [5]. In several papers, extensive analysis and comparisons were provided for several digital signal processing (DSP) solutions [16], [17]. Moreover, a broad range of directions have been explored: monolithic microwave integrated circuit (MMIC) transceiver design [18], waveform design by phase coding [19], [20], dedicated detectors in the spatial domain [21] and range–Doppler map (RDM) [22], spatial beamforming [23], [24], detect-and-repair algorithms [25], [26], [27], [28], detect-and-repair after a domain transformation [29], [30], source separation solutions [31], [32], and slow-time filtering solutions [33]. Many of the abovementioned methods can effectively mitigate interference as of today [3], [34]. However, a trend from edge to centralized radar processing architectures will make more computational resources accessible. As a result, challenging interference scenarios that could not be handled using low-complexity interference mitigation algorithms come in reach with the deployment of more advanced interference solutions.

The recent success of data-driven deep learning across a wide range of applications gave rise to various neural network-aided interference cancellation methods, implemented using, e.g., convolutional neural network (CNN) [35], autoencoders [36], long short-term memory (LSTM) cells, recurrent neural network (RNN) [37], and generative adversarial network (GAN) [38]. While these networks have proven to be highly effective, their downside is their high computational complexity and memory requirements. Another disadvantage of deep learning models is their poor performance on outof-distribution data. The performance of the models degrades when applied to data that do not belong to or is unlikely to appear in the training data distribution. As opposed to these black-box deep learning networks, model-based deep learning proved to generalize well, even on unseen data [39], [40]. Convergence guarantees of the classical iterative methods may still hold for unfolded networks with trainable parameters [41]. Typically, these models can also achieve faster convergence compared to the analytic iterative methods, and on the other hand, they require fewer learnable parameters compared to black-box neural networks [42]. Therefore, these model-based networks provide benefits in the required computational load and memory footprint.

In this article, we propose a model-based deep learning technique that allows for reconstructing signals, leveraging the sparsity attribute of radar targets in the range–Doppler spectrum. Our main contributions are given as follows.

1) The introduction of a model-based neural network that effectively replaces interfered samples with reconstructed target-only signals in the time domain. A sparse prior on the range–Doppler spectrum is exploited. Despite being trained on simulated data, it shows robust performance on real-world measurements.

2) A neural augmentation network that allows for efficient data-dependent parameter estimation for the sparse reconstruction network.

3) We compare our proposed method to a broad range of existing interference mitigation techniques and propose two performance metrics for measured data, called the generalized target-to-noise ratio (gTNR) and normalized SINR (NSINR), which better capture the signal recovery performance in high dynamic range data. The measured data were collected with victim radars that were configured with Doppler division multiple access (DDMA) MIMO schemes.

The rest of this article is organized as follows. Section II introduces the signal model, comprising target signals and interference. A detailed overview of the current state of the art is provided in Section III. Section IV elaborates on the building blocks and design choices that have been made in the proposed neural network. Sections V and VI show the simulation and measurement results, respectively, and conclusions are drawn in Section VII.

Notations: Vectors are denoted by bold lowercase letters $( \mathrm { i } . \mathrm { e } . , \ \mathrm { \bf { X } } )$ , matrices are indicated by bold uppercase letters $( \mathrm { i } . \mathrm { e } . , \mathbf { A } )$ , and scalars are denoted by normal font $( \mathrm { i } . \mathrm { e } . , \mu )$ . Here, $( \cdot ) ^ { \mathrm { T } } , ( \cdot ) ^ { \mathrm { H } }$ , and $( \cdot ) ^ { + }$ refer to the transpose, Hermitian transpose, and Moore–Penrose inverse, respectively, and the vectorization operator is denoted by $\vec { \bf \Phi } ( \cdot ) = \mathrm { v e c } ( \cdot ) ( \mathrm { i . e . , ~ } \vec { \bf Y } )$ . Nomenclature presents the symbols used throughout this article and their explanation.

## II. SIGNAL MODEL

We consider a monostatic MIMO FMCW automotive radar with $N _ { T }$ transmit antennas and $N _ { R }$ receive antennas. The chirps are excited in a pulse train of $N _ { C }$ chirps with a pulse repetition interval (PRI) $T _ { \mathrm { P R I } }$ . On receive, the signal arriving at the mth receive antenna is downconverted and filtered with an anti-aliasing filter. For the pth chirp, the FMCW demodulated signal of the mth Rx antenna $y _ { m , p } ( t )$ consists of target reflection signals $s _ { m , p } ( t )$ , inter-radar interference $i _ { m , p } ( t )$ as well as thermal noise $w _ { m , p } ( t )$

$$
y _ { m , p } ( t ) = s _ { m , p } ( t ) + i _ { m , p } ( t ) + w _ { m , p } ( t ) .\tag{1}
$$

For H target reflections, the desired sensing signal can be approximated by

$$
s _ { m , p } ( t ) \approx \sum _ { h = 1 } ^ { H } \alpha _ { h } \sin \bigl ( 2 \pi \left( f _ { B , h } t + f _ { D , h } ( t + p T _ { \mathrm { P R I } } ) + \phi _ { m , h } \right) \bigr )  \\  \cdot \mathrm { r e c t } \biggl ( \frac { t - p T _ { \mathrm { P R I } } } { T _ { C } } \biggr ) \qquad ( 2 \pi \int \arctan \biggl ( \frac { 2 \pi r } { T _ { C } } \biggr ) \biggr ) .\tag{2}
$$

where $\alpha _ { h } , f _ { B , h } , f _ { D , h }$ , and $T _ { C }$ refer to the complex amplitude, the beat frequency and the Doppler frequency of the hth target reflection, and the chirp duration, respectively. Here, $\phi _ { m , h }$ accounts for the arbitrary phase at which the signal is received while including the effects of the direction of arrival (DoA) and direction of departure (DoD).

Assuming L active interferers, $i _ { m , p } ( t )$ in (1) constitutes to the superposition of interference signals after downconversion that can be approximated by

$$
\begin{array} { r } { i _ { m , p } ( t ) \approx \displaystyle \sum _ { l = 1 } ^ { L } \beta _ { l } \sin \Biggl ( 2 \pi \Biggl [ \Biggl ( \frac { B ^ { ( l ) } } { 2 T _ { C } ^ { ( l ) } } - \frac { B } { 2 T _ { C } } \Biggr ) ( t + p T _ { \mathrm { P R I } } ) ^ { 2 } } \\ { + \theta t \Biggr ] \Biggr ) \cdot \mathrm { r e c t } \Biggl ( \frac { t - p T _ { \mathrm { P R I } } } { T _ { C } } \Biggr ) } \end{array}\tag{3}
$$

where $\theta \ : = \ : f _ { C } ^ { ( l ) } \ : - \ : f _ { C } \ : - \ : ( B ^ { ( l ) } / T _ { C } ^ { ( l ) } ) \tau _ { i } ^ { ( l ) }$ with $f _ { C } , \ B ,$ , and $\tau _ { i }$ denoting the carrier frequency, radio frequency (RF) chirp bandwidth, and the one-trip delay to the lth interfering radar, respectively. Note that $\alpha _ { k } \ \mathrm { ~ \ i ~ } \alpha \ R _ { T , k } ^ { - \bar { 2 } }$ and $\beta _ { l } \propto R _ { I , l } ^ { - 1 }$ , where $R _ { T , k }$ and $R _ { I , l }$ refer to the one-way distance from the radar to the target and from the interferer to the victim radar, respectively. The final term in (1), $w _ { m , p } ( t )$ , is expected to follow a normal distribution $\mathcal { N } ( 0 , \sigma _ { N } ^ { 2 } )$ with $\sigma _ { N } ^ { 2 }$ determining the radar’s thermal noise power.

After the analog-to-digital converter (ADC) stage, the received signal originating from the mth receive antenna and the pth chirp is sampled and quantized and consists of the following terms:

$$
\mathbf { y } _ { m , p } = \mathbf { s } _ { m , p } + \mathbf { i } _ { m , p } + \mathbf { w } _ { m , p }\tag{4}
$$

where $\mathbf { y } _ { m , p } \in \mathbb { R } ^ { N _ { F } }$ is collected $N _ { C }$ times to construct the data matrix $\dot { \mathbf { Y } _ { m } } = \left[ \mathbf { y } _ { m , 1 } \ldots \mathbf { y } _ { m , N _ { c } } \right] ^ { \mathrm { T } } \in \mathbb { R } ^ { N _ { c } \times N _ { F } }$

$$
{ \mathbf Y } _ { m } = { \mathbf S } _ { m } + { \mathbf I } _ { m } + { \mathbf W } _ { m } .\tag{5}
$$

After an interference detection step that identifies which samples have been corrupted, the interference is mitigated by masking these samples. In this article, we apply time-domain thresholding-based interference detection as proposed in [43]. However, instead of a fixed noise threshold, an adaptive threshold was used for detecting the interfered samples. Then, detect-and-repair methods aim at recovering $\mathbf { s } _ { m , p }$ from masked ADC samples $\widetilde { \mathbf { y } } _ { m , p } ,$ , as shown in Fig. 1

$$
\begin{array} { r } { \tilde { \mathbf { y } } _ { m , p } = \mathbf { A } _ { p } \mathbf { y } _ { m , p } = \mathbf { A } _ { p } \mathbf { s } _ { m , p } + \underbrace { \mathbf { A } _ { p } \mathbf { i } _ { m , p } } _ { = \mathbf { 0 } } + \mathbf { A } _ { p } \mathbf { w } _ { m , p } } \end{array}\tag{6}
$$

with $\tilde { { \bf y } } _ { m , p } ~ \in ~ \mathbb { R } ^ { d }$ and $\mathbf { A } _ { p } ~ \in ~ \{ 0 , 1 \} ^ { d \times N _ { F } }$ perfectly detecting $( N _ { F } - d )$ time-domain samples that are contaminated with interference; hence, d refers to the number of clean samples. The masking matrix $\mathbf { A } _ { p }$ is constructed from the interference detection mask $\mathbf { m } _ { p }$ under the constraint that each row of $\mathbf { A } _ { p }$ has a cardinality equal to one. Then, it follows that $\mathbf { A } _ { p } ^ { \mathrm { T } } \mathbf { A } _ { p } =$ $\mathrm { d i a g } ( \mathbf { m } _ { p } )$ , where ${ \bf m } _ { p }$ maps the contaminated samples one-toone to $\mathbf { y } _ { m , p }$ . Herein, a zero indicates a contaminated ADC sample, while a one indicates a clean ADC sample of $\mathbf { y } _ { m , p }$

![](images/d9c49a39aa4a9e9ed50377b1af530e43db515e962a91e6f57b1da379e58aad16.jpg)  
Fig. 1. Interference detect-and-repair methodology.

TABLE I  
COMPARISON OF STATE-OF-THE-ART METHODS. THE ASTERISK (∗) ENTAILS THAT A SUBSAMPLED RDM IS USED
<table><tr><td>Method</td><td>Intf. Det.</td><td>Dim</td><td>Sparse</td><td>Waveform Indep.</td></tr><tr><td>IMAT [25]</td><td></td><td>R</td><td></td><td></td></tr><tr><td>AR-ST [26]</td><td></td><td>R</td><td></td><td></td></tr><tr><td>BKCS [27]</td><td></td><td>RD*</td><td></td><td></td></tr><tr><td>SALSA [31]</td><td>X</td><td>R</td><td></td><td></td></tr><tr><td>LowRaS [32]</td><td>X</td><td>R</td><td></td><td>X</td></tr><tr><td>RFmin [33]</td><td>X</td><td>D</td><td></td><td></td></tr><tr><td>ALFISTA [28]</td><td></td><td>RD</td><td></td><td></td></tr><tr><td>NA-ALFISTA (ours)</td><td></td><td>RD</td><td></td><td></td></tr></table>

## III. STATE OF THE ART

In the following, we discuss a list of interference solutions that will be used for comparison to the proposed method in Section V, see Table I for an overview. It shows which methods require a priori knowledge of which samples contain interference, exploit sparsity, and which dimensions [e.g., range (R) and/or Doppler (D)] are utilized for interference mitigation. Also, it indicates which methods are waveform-independent and do not rely on particular interference signal properties. We categorize the methods explained in Sections III-B–III-D as detect-and-repair methods, Section III-E and III-F as source separation methods, and Section III-G as a filtering method.

## A. Zeroing

Zeroing is a cost-effective interference mitigation technique that removes the interference but also impacts the target signal and introduces undesirable artifacts. It is represented using an element-wise multiplication with the interference detection mask

$$
\begin{array} { r } { \hat { \bf s } _ { m , p } = { \bf A } _ { p } ^ { \mathrm { T } } \tilde { \bf y } _ { m , p } = { \bf m } _ { p } \odot { \bf y } _ { m , p } . } \end{array}\tag{7}
$$

## B. Iterative Method Adaptive Thresholding

Bechter et al. [25] applied iterative method adaptive thresholding (IMAT) on fast-time FMCW samples. The 1-D method recursively reconstructs time-domain samples from the following update rule:

$$
\begin{array} { r } { \mathbf { y } _ { m , p } ^ { ( k ) } = \mathbf { A } _ { p } ^ { \mathrm { T } } \tilde { \mathbf { y } } _ { m , p } + \bigl ( \mathbf { I } - \mathbf { A } _ { p } ^ { \mathrm { T } } \mathbf { A } _ { p } \bigr ) \mathbf { F } ^ { \mathrm { H } } { g } \bigl ( \mathbf { F } \mathbf { y } _ { m , p } ^ { ( k - 1 ) } , \boldsymbol { \lambda } ^ { ( k ) } \bigr ) } \end{array}\tag{8}
$$

where $g ( \mathbf { z } , \lambda )$ is the hard thresholding function that sets all values in z that have an absolute value below a threshold λ to zero, and F and $\mathbf { F } ^ { \mathrm { H } }$ stand for Fourier and inverse Fourier transform, respectively. Hence, the thresholding takes place in the distance spectrum. From [25], the number of iterations K is adaptively determined with $m _ { \mathrm { i t } } = 1 0$ being used in the experiments, which leads to $\hat { \mathbf { s } } _ { m , p } = \mathbf { y } _ { m , k } ^ { ( K ) }$

## C. Autoregressive Model

An autoregressive (AR) model-based solution, leveraging Burg’s method, was applied to either the slow-time or fasttime dimension [26]. The experimental results proved that slow-time processing was more effective, denoted as AR-ST.

## D. Block Kronecker Compressed Sensing

A 2-D framework is proposed in [27] to exploit sparsity in the RDM. YALL1 [44] was used to solve the 2-D optimization problem that is known for its large computational cost. However, to reduce computational expenses, the authors proposed to apply the method on a subset of the ADC samples, where the fast- and slow-time dimensions are reduced by factors $N _ { F , s }$ and $N _ { S , s }$ , respectively. The resulting optimization problem for the (u, v)th block, with $u \in \{ 1 , 2 , . . . , ( N _ { C } / N _ { C , s } ) \}$ and $v \in \{ 1 , 2 , \dotsc , ( N _ { F } / N _ { F , s } ) \}$ , is then formulated as follows:

$$
\hat { \vec { \bf X } } _ { m , u , v } = \operatorname* { m i n } _ { { \bf X } _ { m , u , v } } | | { \bf X } _ { m , u , v } | | _ { 1 } , \mathrm { s . t . } \vec { \tilde { \bf Y } } _ { m , u , v } = { \bf A } _ { u , v } \vec { \bf X } _ { m , u , v }\tag{9}
$$

where $\mathbf { A } _ { u , v }$ is the dictionary equal to the 2-D partial inverse Fourier matrix derived using the block Kronecker product. Solving (9) for all interfered blocks $\tilde { \mathbf { Y } } _ { m , u , v }$ results in $\hat { \bf S } _ { m }$ for which conventional FMCW processing steps apply. For evaluation in this article, $N _ { F , s } ~ = ~ 4$ and $N _ { C , s } ~ = ~ 1 2 8$ were used.

## E. Split Augmented Lagrangian Shrinkage Algorithm

In [31], a variation of basis pursuit denoising (BPDN) is proposed as a means of signal separation. Alternating direction method of multipliers (ADMM) was used to solve the following optimization problem, using fast Fourier transform (FFT) and short-time Fourier transform (STFT) as transform domains to more accurately represent the target-only signal $\mathbf { x } _ { m , p }$ and interference-only signal $\mathbf { i } _ { m , p }$

$$
\begin{array} { r } { \hat { \mathbf { s } } _ { m , p } , \hat { \mathbf { i } } _ { m , p } = \mathop { \arg \operatorname* { m i n } } _ { \mathbf { F } \mathbf { s } _ { m , p } , \mathbf { F } _ { i } \mathbf { i } _ { m , p } } | | \mathbf { y } _ { m , p } - \mathbf { s } _ { m , p } - \mathbf { i } _ { m , p } | | _ { 2 } ^ { 2 } \qquad } \\ { + \left. \lambda _ { s } \right| | \mathbf { F } \mathbf { s } _ { m , p } | | _ { 1 } + \left. \lambda _ { i } \right| | \mathbf { F } _ { i } \mathbf { i } _ { m , p } | | _ { 1 } } \end{array}\tag{10}
$$

where $\lambda _ { s }$ and $\lambda _ { i }$ trade sparsity in $\mathbf { F s } _ { m , p }$ against sparsity in $\mathbf { F } _ { i } \mathbf { i } _ { m , p }$ and $\mathbf { F } _ { i }$ denotes the STFT basis. In the experiments, $m _ { \mathrm { i t } } = 1 0 0 , \mu = 1 0 , \lambda _ { s } = 1$ , and $\lambda _ { a } = 0 . 2$ were obtained by optimizing the parameters for the given data.

## F. Sparse Low-Rank Hankel Matrix Decomposition

Wang et al. [32] formulated an optimization problem that exploits the low-rank Hankelized target signals $\mathcal { H } (  { \mathbf { s } } _ { m , p } )$ for decomposing the target and interference signal

$$
\begin{array} { r l } & { \hat { \mathbf { s } } _ { m , p } , \hat { \mathbf { i } } _ { m , p } , \hat { \mathbf { U } } , \hat { \mathbf { V } } } \\ & { = \underset { { \mathbf { s } } _ { m , p } , \mathbf { i } _ { m , p } , \mathbf { U } , \mathbf { V } } { \mathrm { a r g } \operatorname* { m i n } } \quad \frac { 1 } { 2 } \big ( | | \mathbf { U } | | _ { \mathrm { F } } ^ { 2 } + | | \mathbf { V } | | _ { \mathrm { F } } ^ { 2 } \big ) } \\ & { \qquad + \textit { \textbf { \# } } | | \mathbf { i } _ { m , p } | | _ { 1 } } \\ & { \mathrm { s . t . } \ | | \mathbf { y } _ { m , p } - \mathbf { s } _ { m , p } - \mathbf { i } _ { m , p } | | _ { 2 } ^ { 2 } \leq \epsilon , \ \mathcal { H } \big ( \mathbf { s } _ { m , p } \big ) = \mathbf { U } \mathbf { V } ^ { \mathrm { H } } . } \end{array}\tag{11}
$$

Here, (11) is optimized using ADMM to circumvent the computationally expensive singular value decomposition (SVD) calculations, which iteratively estimates $\mathbf { U } ^ { ( k ) }$ and $\mathbf { V } ^ { ( k ) }$ , as well as $\mathbf { x } _ { m , p } ^ { ( k ) }$ and $\mathbf { i } _ { m , p } ^ { ( k ) } .$ The assumption is that the interference time-domain signal $\mathbf { i } _ { m , p }$ is sparse while exploiting the low-rank property in $\mathbf { s } _ { m , p }$ due to the limited presence of complex exponentials, i.e., $H \ll N _ { F }$ . The hyperparameters for sparse low-rank Hankel matrix decomposition (LowRaS) were set as proposed in [32].

## G. Ramp Filtering (RFmin)

Ramp filtering is introduced by applying a function $g ( \cdot )$ on the amplitude values of the slow-time samples, after range processing [33]. The proposed function is nonlinear, namely, $g ( \cdot ) \ = \ \operatorname* { m i n } ( \cdot )$ , hence generally referred to as RFmin. The original phase of the interfered range spectrum is maintained and not mitigated. Despite its simplicity, not mitigating the interference-induced phase distortion may propagate and result in inaccurate estimates of Doppler and DoAs.

## IV. PROPOSED METHOD

In this article, we propose neurally augmented ALFISTA (NA-ALFISTA) that combines the benefits of sparse recovery to robustly reconstruct missing time-domain samples with a neural augmentation network. The latter exploits the stochastics of the target and noise signals for estimating parameters for the next layer of analytically learned FISTA (ALFISTA). A block diagram of NA-ALFISTA is shown in Fig. 2 that illustrates how both are intertwined. In [28], the reconstruction parameters were learned in an end-to-end manner; however, in this section, we elaborate on why there is a need for data-dependent parameter estimation.

## A. Sparse Reconstruction

We formulate the signal recovery as a sparse compressive sensing problem, such as least absolute shrinkage and selection operator (LASSO), that is designed to maximize the data fit while penalizing the $\ell _ { 1 } \cdot$ -norm of $\vec { \mathbf { X } } _ { m }$

$$
\hat { \bar { \bf X } } _ { m } = \arg \operatorname* { m i n } _ { \vec { \bf X } _ { m } } \frac { 1 } { 2 } \big \| \vec { \tilde { \bf Y } } _ { m } - { \bf A } { \bar { \bf F } } ^ { \mathrm { H } } \vec { \bf X } _ { m } \big \| _ { 2 } ^ { 2 } + \lambda \big \| \vec { \bf X } _ { m } \big \| _ { 1 }\tag{12}
$$

where λ controls the amount of sparsity in $\hat { \mathbf { X } } _ { m } ,$ and the time-domain samples and range–Doppler samples are denoted by $\vec { \tilde { \bf Y } } _ { m } ~ \in ~ \mathbb { R } ^ { D \times 1 }$ and $\vec { \bf X } _ { m } \in \overline { { \mathbb { C } ^ { N _ { C } \hat { N _ { F } } \times 1 } } }$ , respectively. Hence, we exploit D clean fast- and slow-time samples available in a single measurement to recover $( N _ { C } N _ { F } - D )$ samples. The Nyquist–Shannon sampling theorem states that a bandlimited signal can be perfectly represented in case it suffices the uniform sampling rate criteria. However, a large portion of the samples may be lost due to interference removal through nulling, resulting in $\tilde { \mathbf { Y } } _ { m }$ from (7). In the proposed solution, we assume that the range–Doppler signal $\mathbf { X } _ { m }$ is compressible under a sparse signal model. Therefore, the missing signals can be robustly reconstructed using a compressive sampling theory.

The compressive sampling matrix $\mathbf { A } \bar { \mathbf { F } } ^ { \mathrm { H } }$ from (12) can be decomposed into the subsampling matrix A and the 2-D Fourier matrix F<sup>¯</sup> . A is constructed by concatenating $\underline { { \mathbf { A } } } _ { p }$ from (6) for $p ~ \in ~ \{ 1 , \dots , N _ { C } \}$ such that $\mathbf { A } ^ { \mathrm { T } } \mathbf { A } \ = \ \mathrm { d i a g } ( \vec { \mathbf { M } } )$ where $\mathbf { M } \in \{ 0 , 1 \} ^ { N _ { C } \times N _ { F } }$ is the 2-D binary masking matrix.

Unrolled Reconstruction Network  
![](images/c8071866f2bbb8d345c77bc2c0f8d2179cc4688b2215c33eba63cffad589a3b1.jpg)  
Fig. 2. Block diagram of the proposed NA-ALFISTA network with trainable parameters: $\mathbf { w } ^ { ( 0 ) } , \mathbf { h } ^ { ( 0 ) }$ , as well as the parameters inside the GRU cell and hidden layer.

The 2-D Fourier matrix $\bar { \bf F }$ is constructed from the Kronecker product of two Fourier matrices $\mathbf { F } _ { 1 } ~ \in ~ \mathbb { C } ^ { N _ { C } \times N _ { C } }$ and ${ \bf F } _ { 2 } \in  { }$ $\mathbf { \bar { \mathbb { C } } } ^ { N _ { F } \times N _ { F } } , \mathrm { i . e . , } \mathbf { \bar { F } } = \mathbf { F } _ { 1 } \otimes \mathbf { F } _ { 2 } \in \mathbb { C } ^ { N _ { C } N _ { F } \times N _ { C } N _ { F } }$ , required for radial distance and Doppler processing, respectively.

Consequently, (12) can be minimized using multiple algorithms that have been readily proposed for solving l -regularized optimization problems, e.g., using iterative shrinkage thresholding algorithm (ISTA) [45]. For recovering range–Doppler spectrum $\mathbf { X } _ { m }$ , the kth data-consistency step in ISTA is defined as follows:

$$
\vec { \mathbf { X } } _ { m } ^ { ( k ) } = \vec { \mathbf { X } } _ { m } ^ { ( k ) } - \mu \big ( \mathbf { A } \bar { \mathbf { F } } ^ { \mathrm { H } } \big ) ^ { \mathrm { H } } \big ( \mathbf { A } \bar { \mathbf { F } } ^ { \mathrm { H } } \vec { \mathbf { X } } _ { m } ^ { ( k ) } - \vec { \tilde { \mathbf { Y } } } _ { m } \big )\tag{13}
$$

$$
\mathbf { \bar { \rho } } = \vec { \mathbf { X } } _ { m } ^ { ( k ) } - \mu \bar { \mathbf { F } } \mathbf { A } ^ { \mathrm { H } } \big ( \mathbf { A } \bar { \mathbf { F } } ^ { \mathrm { H } } \vec { \mathbf { X } } _ { m } ^ { ( k ) } - \vec { \tilde { \mathbf { Y } } } _ { m } \big )\tag{14}
$$

that is followed by a proximal step of the ℓ<sub>1</sub>-norm, generally known as the soft thresholding operation, to promote sparsity

$$
\vec { \mathbf { X } } _ { m } ^ { ( k + 1 ) } = \mathop { \mathrm { p r o x } } _ { \lambda | | \cdot | | _ { 1 } } \left( \vec { \mathbf { X } } _ { m } ^ { ( k ) } \right)\tag{15}
$$

which has been implemented using the complex soft thresholding function $\mathcal { T } _ { \lambda } ( \mathbf { X } ) = \mathrm { p r o x } _ { \lambda | | \cdot | | _ { 1 } } ( \mathbf { X } ) = ( \mathbf { X } / | \mathbf { X } | ) ( | \mathbf { X } | - \lambda ) _ { + } .$

In addition, we consider fast-iterative shrinkage thresholding algorithm (FISTA), which is known for its faster convergence rate when compared to ISTA [46] such that the number of iterations can be reduced. The matrix-form update rule for FISTA is given as follows:

$$
\vec { \mathbf { X } } _ { m } ^ { ( k ) } = \mathcal { T } _ { \lambda } \big ( \vec { \mathbf { Z } } _ { m } ^ { ( k ) } - \mu \bar { \mathbf { F } } \mathbf { A } ^ { \mathrm { H } } \big ( \mathbf { A } \bar { \mathbf { F } } ^ { \mathrm { H } } \vec { \mathbf { Z } } _ { m } ^ { ( k ) } - \vec { \tilde { \mathbf { Y } } } _ { m } \big ) \big )\tag{16}
$$

$$
\vec { \mathbf { Z } } _ { m } ^ { ( k + 1 ) } = \vec { \mathbf { X } } _ { m } ^ { ( k ) } + \rho ^ { ( k ) } \bigl ( \vec { \mathbf { X } } _ { m } ^ { ( k ) } - \vec { \mathbf { X } } _ { m } ^ { ( k - 1 ) } \bigr )\tag{17}
$$

with $\begin{array} { r l r } { \rho ^ { ( k ) } } & { { } = } & { ( t ^ { ( k ) } - 1 / t ^ { ( k + 1 ) } ) } \end{array}$ and $t ^ { ( k + 1 ) } ~ = ~ ( 1 + ( 1 +$ $4 ( t ^ { ( k ) } ) ^ { 2 } ) ^ { 1 / 2 } / 2 )$ , where $t ^ { ( 0 ) } = 1$ is used for initialization. In (16), ${ \bf Z } ^ { ( 0 ) }$ is initialized with zeros.

## B. Complexity Reduction

Multiplying both sides of (16) with $\bar { \mathbf { F } } ^ { \mathrm { H } }$ allows us to shuffle the order of processing and reduce a few redundant processing steps, i.e., $\bar { \mathbf { F } } \mathbf { A } \mathbf { A } \bar { \mathbf { F } } \mathbf { H }$ . By performing the data-consistency step in the time domain, we can force the samples to be only updated if they were detected as contaminated with interference using (19). Both steps then lead to the following update rules from (14):

$$
\vec { \mathbf { Y } } _ { m } ^ { ( k ) } = \bar { \mathbf { F } } ^ { \mathrm { H } } T _ { \lambda } \bigl ( \bar { \mathbf { F } } \bigl ( \vec { \mathbf { Y } } _ { m } ^ { ( k ) } - \mu \bigl ( \vec { \mathbf { Y } } _ { m } ^ { ( k ) } - \mathbf { A } ^ { \mathrm { H } } \vec { \mathbf { Y } } _ { m } \bigr ) \bigr ) \bigr )\tag{18}
$$

$$
\vec { \mathbf { Y } } _ { m } ^ { ( k + 1 ) } = \mathbf { A } ^ { \mathrm { H } } \vec { \tilde { \mathbf { Y } } } _ { m } + \left( \mathbf { I } - \mathbf { A } ^ { \mathrm { H } } \mathbf { A } \right) \vec { \mathbf { Y } } _ { m } ^ { ( k ) } .\tag{19}
$$

Considering the dense vector and matrix shapes in (14), e.g., $N _ { C } N _ { F } \times N _ { C } N _ { F }$ , the resulting memory and computational load will put the real-time requirements of automotive radar signal processing at risk. Therefore, we propose to utilize an equivalent matrix form, by substituting the vectors in the update rule with their original slow- and fast-time shapes, i.e., $\mathbf { Y } \in \mathbb { R } ^ { N _ { C } \times N _ { I } }$

$$
{ \bf Y } _ { m } ^ { ( k ) } = \mathcal { F } ^ { \mathrm { H } } \big \{ \mathcal { T } _ { \boldsymbol \lambda } \big ( \mathcal { F } \big \{ { \bf Y } _ { m } ^ { ( k ) } - \mu \big ( { \bf Y } _ { m } ^ { ( k ) } - { \bf M } \odot { \bf Y } _ { m } \big ) \big \} \big ) \big \}\tag{20}
$$

$$
\mathbf { Y } _ { m } ^ { ( k + 1 ) } = \mathbf { M } \odot \mathbf { Y } _ { m } + ( 1 - \mathbf { M } ) \odot \mathbf { Y } _ { m } ^ { ( k ) }\tag{21}
$$

where ${ \mathcal { F } } \{ \cdot \}$ and ${ \mathcal { F } } ^ { \mathrm { H } } \{ \cdot \}$ denote the 2-D FFT and 2-D inverse FFT, respectively. The matrix-form update step reduces the computational complexity from $\mathcal { O } ( N ^ { \bar { 3 } } )$ to O(N log N) with $N ~ = ~ N _ { \cal C } N _ { \cal F }$ , which has floating-point operations (FLOPs) count

$$
\mathrm { F L O P } _ { \mathrm { v e c } } = 2 \cdot \ ( 2 N ^ { 3 } - N ^ { 2 } ) \ + \quad \underbrace { N ^ { 2 } - N } _ { \qquad \quad }\tag{22}
$$

$$
\mathrm { F L O P } _ { \mathrm { m a t } } = 2 \cdot \underbrace { N \log ( N ) } _ { \mathrm { 2 D F F T } } + \underbrace { N } _ { \mathrm { e l e m - w i s e ~ p r o d } . }\tag{23}
$$

and has been illustrated in Fig. 3 for a fixed $N _ { C } .$ Mainly, the load is dictated by FFT-based processing, which can be efficiently parallelized with hardware-accelerated implementations.

![](images/c5630e4c054ec1fed39feb9b891d6b487d8fad3f03207e029645c78a87b7113d.jpg)  
Fig. 3. Computational complexity of a data-consistency step of ISTA, comparing the vector form and matrix form [see (14) and (20)], where the number of chirps is fixed to $N _ { C } = 1 2 8$

## C. Algorithm Unrolling

In [28], we proposed to unroll the iterative algorithm of (16) and (17) for a fixed K number of layers. The parameters $\mu$ and λ are learned in an end-to-end manner for each layer independently, i.e., $\mu ^ { ( k ) }$ and $\lambda ^ { ( k ) }$ , resulting in 2K trainable parameters. The momentum multiplier $\rho ^ { ( k ) }$ is analytically determined, similar as in FISTA. Since the interference mask M is determined from the interfered samples in the current measurement frame, fully unfolded networks cannot be applied with fixed weight matrices, such as learned ISTA (LISTA) [47]. Due to the deterministic nature of the detection mask M, we are forced to combine a deterministic data-consistency step with trainable parameters, i.e., we use ALFISTA. The small number of network parameters entails a shallow memory footprint for storage of the weights as well as prompt convergence during training. However, despite its robust reconstruction performance, it suffers from several shortcomings. First, the parameters $\mu ^ { ( k ) }$ and $\lambda ^ { ( k ) }$ were trained and optimized for a broad range of scenarios, both for the target statistics and the interference occurrence. During inference, the learned parameters $\mu$ and λ are fixed and are generalized only for the radar signal statistics of the training set. However, λ is a function of the received signal statistics, e.g., the parameters of the Laplace distribution and Gaussian distribution, which can change during sensing, promoting a more data-adaptive approach. Furthermore, during training of the method in [28], the interference distortion ratio $\begin{array} { l l l } { r } & { = } & { 1 { - } D / ( N _ { C } N _ { F } ) } \end{array}$ was varied from 0% to 50%. Although the results indicate good performance on out-of-distribution r of the interference masks up to 80%, there is likely room for improvement by reducing the number of layers. Second, the target statistics can change radically, $\mathrm { e . g . }$ , when the radar is operational in an urban or highway environment. Third, the momentum multiplier $\rho ^ { ( k ) }$ was analytically determined. Improvements for these aspects will be addressed in Section IV-D.

## D. Neural Augmentation Network

To improve the adaptivity to highly fluctuating input data and to increase the convergence speed of the reconstruction method, we propose a small neural augmentation network $f _ { \pmb \theta } ( \cdot )$ parameterized by weights θ. It predicts the reconstruction weights, i.e., the step size $\mu ,$ threshold $\lambda ,$ and momentum multiplier $\rho$ for the concurrent layer of the unfolded reconstruction network, which was explained in Section IV-A. The augmentation neural network $f _ { \theta }$ runs next to the sparse reconstruction network and estimates the weights accordingly

$$
\mathbf { w } ^ { ( k ) } = f _ { \pmb { \theta } } \big ( \mathbf { q } ^ { ( k - 1 ) } \big )\tag{24}
$$

with $\mathbf { w } ^ { ( k ) } = \left[ \mu ^ { ( k ) } , \lambda ^ { ( k ) } , \rho ^ { ( k ) } \right]$ . Neurally augmenting LISTAbased neural networks were first proposed in [48]; however, we propose to use a gated recurrent unit (GRU) cell instead of an LSTM cell. GRUs are on par in terms of performance, but they require less memory and computational expenses. The augmentation network introduces long-term memory for estimating the reconstruction parameters of several consecutive layers. The vector $\mathbf { q } ^ { ( k ) }$ is defined as follows:

$$
\mathbf { q } ^ { ( k ) } = \left[ \mathbf { w } ^ { ( k - 1 ) } , \delta , \kappa , r \right]\tag{25}
$$

which indicates that the previous sparse reconstruction layer’s parameters are fed back into the GRU. Moreover, it takes the $\ell _ { 1 } { \mathrm { - n o r m } }$ of the residual of two consecutive estimates $\mathbf { X } ^ { ( k ) }$ and $\mathbf { X } ^ { ( k ) }$ from (17) as input: $\delta = | | \mathbf { X } ^ { ( k ) } \ - \mathbf { X } ^ { ( k - 1 ) } | | _ { 1 }$ . Furthermore, $\kappa = \mathrm { m a x } ( | \bar { \mathbf { X } } | )$ refers to the maximum magnitude of the RDM after time-domain zeroing to remove the interference, and r denotes the interference distortion ratio in the measurement frame. The initial hidden state $\mathbf { h } ^ { ( 0 ) }$ is introduced as trainable parameters along with the internal weights of the GRU cell itself. The number of trainable parameters of the GRU cell, assuming $N _ { I , 1 }$ and $N _ { O , 1 }$ input and output dimensions, respectively, equals $3 ( 2 { N _ { I , 1 } } + { N _ { I , 1 } } { N _ { O , 1 } } + { N _ { O , 1 } ^ { 2 } } )$ . The hidden output $\mathbf { h } ^ { ( k ) }$ is connected to a single fully connected layer with $N _ { \mathrm { F C } }$ nodes, which is capable of learning features from all the combinations of the GRU hidden output. Thereupon, the fully connected layer outputs $N _ { O , 2 }$ parameters: $\mu ^ { ( k ) } , \lambda ^ { ( k ) }$ and $\rho ^ { ( k ) }$ . Those will be used for sparse reconstruction in the kth layer. The total number of trainable parameters for the fully connected layer amounts to $N _ { \mathrm { F C } } ( N _ { O , 1 } + N _ { O , 2 } )$

Tuning the hyperparameters $N _ { O , 1 }$ and $N _ { \mathrm { F C } }$ resulted in the selection of $N o , \ i = 2 0$ and $N _ { \mathrm { F C } } ~ = ~ 2 0$ , while $N _ { O , 2 } ~ = ~ 3$ Then, the total number of trainable parameters in the neural augmentation network is limited to 2065, which is independent of the number of layers.

## E. Training Procedure

NA-ALFISTA is trained in an end-to-end supervised manner on simulated FMCW radar data. The training set comprises $N _ { D }$ radar measurements, including $N _ { D }$ different interference detection masks M and $N _ { D }$ independently simulated ADC measurements Y with $N _ { C } = 2 5 6$ and $N _ { F } = 1 0 2 4$ . The signal Y was generated using a realistic radar and channel model and contains a varying number of point-target reflections H of realistic signals strengths, i.e., its power decays with $R _ { T } ^ { - 4 }$ and the reflectivity is modeled according to RCS values. The following parameters were drawn from uniform distributions in the ranges: $H \in \{ 2 , \ldots , 5 0 \} , v _ { T } \in [ - v _ { \mathrm { u a } } / 2 , v _ { \mathrm { u a } } / 2 ] \mathrm { m } / \mathrm { s } .$ $R _ { T } ~ \in ~ \left[ \Delta R , R _ { \mathrm { u a } } \right]$ m, and $\mathsf { R C S } \ \in \ [ - 8 , 2 5 ]$ dB, where $v _ { \mathrm { u a } } ,$ $R _ { \mathrm { u a } } ,$ , and $\Delta R$ refer to the unambiguous radial velocity, unambiguous radial distance, and distance resolution of the radar, respectively.

The interference detection mask is artificially generated by placing repetitive gaps occurring along the fast time and slow time in the data matrix M, where r is drawn from a uniform distribution $\mathcal { U } ( 0 , 0 . 5 )$ . The clean range–Doppler spectrum X and reconstructed spectrum $\hat { \mathbf { X } }$ can be used for regression. The loss function that was applied is the mean squared error (mse) on the complex-valued spectra, minimizing the loss function $\mathcal { L } ( r , { \bf X } , \hat { \bf X } ) = ( 1 / r ) ( { \bf X } - \hat { \bf X } ) ^ { \mathrm { H } } ( { \bf X } - \hat { \bf X } )$ ). The loss function is inversely proportional to r to prevent the network from overfitting for extremely affected time-domain samples.

We train the network stochastically using the AdamW optimization procedure using the default settings for the learning rate $\mathrm { l r } = 4 \times 1 0 ^ { - 2 } , \beta _ { 1 } = 0 . 9 , \beta _ { 2 } = 0 . 9 9 9$ , and $\epsilon = 1 0 ^ { - 8 }$ [49]. AdamW is an enhanced optimization procedure based on Adam [50] and was introduced to generalize models better using weight decaying. The training and validation set sizes are 1000 and 200, respectively. Furthermore, 100 epochs were used for training.

## V. SIMULATION RESULTS

This section presents the signal reconstruction performance of the detect-and-repair methods listed in Table I on simulated FMCW radar data. This section considers perfect interference detection, where synthetic radar data are exploited to define the interference detection mask ${ \bf m } _ { p }$ perfectly. The interference detection mask M is equivalent for all methods in the comparison. Concurrently, the detect-and-repair with imperfect interference detection and source separation methods will be evaluated further on measured data in Section VI-B.

## A. Reconstruction Performance

The reconstruction performance after the contaminated samples have been zeroed is evaluated using the mse, which can be obtained accordingly using L(X, X<sup>ˆ</sup> ). The ground truth RDM X is available in the simulation evaluation, so the estimated magnitude and phase are implicitly evaluated in the RDMs using the complex mse. Therefore, this metric considers all range–Doppler bins and measures how well the zeroing-induced sidelobes are suppressed, as well as how accurately target signals are recovered in both magnitude and phase.

Fig. 4 shows the mse for zeroing, IMAT, AR-ST, block Kronecker compressed sensing (BKCS), and ALFISTA and NA-ALFISTA with $K = 5$ and $K \ = \ 1 5$ . One can observe that all methods except for zeroing are recovering the missing signal, resulting in lower mse compared to zeroing. Furthermore, IMAT and AR-ST achieve comparable performance, each utilizing the available 1-D data for recovering the zeroed signal, $\mathrm { i . e . }$ , fast time or slow time, respectively. The phase of $\hat { \mathbf { X } } _ { m }$ obtained with IMAT becomes less accurate when the number of zeroed samples increases [25]. While the error curve for BKCS with 500 iterations is significantly improved over the 1-D reconstruction methods, it does not reach the low error levels of ALFISTA and NA-ALFISTA. Both ALFISTA and NA-ALFISTA have exceptional reconstruction performance, especially seeing their small number of layers. It is observed that neural augmentation is specifically beneficial for

![](images/92eb8cf522c502774e1337e9a2beff4f0ccb0680f2e13ec9524a768761e1c29c.jpg)  
Fig. 4. Reconstruction performance in simulated RDMs and measured in mse.

$K = 5$ compared to $K = 1 5 .$ , which is explained by improved convergence speeds. For $K \ = \ 1 5$ , the difference is less apparent, but here, enhanced performance is observed when $r \geq 6 0 \%$ . As the distortion ratio is increased further, both ALFISTA and NA-ALFISTA deteriorate compared to BKCS as the number of layers is insufficient to recover the signal. The reduced coherent FFT processing gain, caused by an increasing $r ,$ results in the fact that sparsity is more difficult to exploit. BKCS benefits from the 500 iterations that allow for more accurate reconstructions when $r \geq 7 0 \%$

To compare all methods against a lower limit, we empirically calculated what the mse would measure in case there was perfect reconstruction after zeroing, which we refer to as the noiseless reconstruction bound

$$
\Omega ( r ) = r \cdot \sigma _ { N } ^ { 2 }\tag{26}
$$

which indicates that only the target reflections are reconstructed without recovering the thermal noise after it has been removed by zeroing. Hence, it is scaled by the number of affected time-domain samples divided by the total number of samples, i.e., r .

## B. Phase Recovery

The phase information of target bins in the RDMs is important for azimuthal and elevational DoA estimation and must not be affected by the interference removal. In Fig. 5, we evaluate the phase error explicitly with respect to a noncorrupted RDM, only for the target bins. Note that the differences in phase recovery for ALFISTA and NA-ALFISTA are less significant than for the overall mse results from Fig. 4.

## VI. MEASUREMENT RESULTS

## A. Experimental Setup

For experimental evaluation, two in-house designed radars $V _ { 1 }$ and $V _ { 2 }$ are used as victim radars, with $N _ { T } ~ = ~ 2$ and $N _ { R } = 4$ antennas. Both radars are mounted on the ego vehicle as forward-facing radars, as illustrated in Fig. 6(a).

Furthermore, four interfering radars, $I _ { 1 } { - } I _ { 4 }$ , are placed in the field at similar heights as the victim radars, see Fig. 6(b).

![](images/7e433a030879c32c39298dd316e3e6b9161e004f7210b3bfd3302217d4482b41.jpg)  
Fig. 5. Phase error of the target bins in RDM and measured in RMSE.

![](images/748d6a281bba665b5c129227a316b17bcd3f5f01c51eb34e31800cc856fc1963.jpg)

![](images/cce35fc9c3eef044a423e6806e29bc76d32b57aa33847c54ab24292482419a62.jpg)

(a)  
![](images/6404fb267694b7e05e6992b8121d79e64410e0d530bb2107df04d2596fc0d35a.jpg)  
(c)  
Fig. 6. Measurement setup with (a) ego vehicle with victim radars $V _ { 1 }$ and $V _ { 2 } ,$ (b) measurement scene with interfering radars $I _ { 1 } { - } I _ { 4 } ,$ and $( \mathrm { c } )$ waveform configurations with the instantaneous frequency of the victim and interfering radars over time, see Table II for the detailed parameters.

The chirp configurations of all radars, as well as the victimto-interferer distance $R _ { I }$ , have been listed in Table II. Victim $V _ { 1 }$ is configured such that no interference is perceived in the ADC samples by exploiting frequency diversity. Victim $V _ { 2 }$ perceives different kinds of interference from two downchirping radars, of which $T _ { \mathrm { P R I } }$ of $I _ { 3 }$ is equivalent to the victim radars. Interferer $I _ { 2 }$ has similar transmit configurations as $V _ { 2 } ,$ so it can be assigned as quasi-correlated. Therefore, different types of interference data can be collected for evaluation in Section VI-B.

All active radars transmit FMCW radar signals with 2-TX uniform DDMA MIMO transmit schemes. In total, $N _ { C } = 2 5 6$ chirps are transmitted, of which $N _ { F } = 1 0 2 4$ fast-time samples are acquired on receive. For the detect-and-repair methods, interference detection is done using [43]. The evaluation is performed on the noncoherently integrated RDMs.

TABLE II  
CONFIGURATIONS OF ALL RADARS
<table><tr><td></td><td> $V _ { 1 }$ </td><td> $V _ { 2 }$ </td><td> $I _ { 1 }$ </td><td> $I _ { 2 }$ </td><td> $I _ { 3 }$ </td><td> $I _ { 4 }$ </td></tr><tr><td>RI (m)</td><td></td><td></td><td>10</td><td>20</td><td>35</td><td>55</td></tr><tr><td>fc (GHz)</td><td>76.22</td><td>76.78</td><td>76.2</td><td>76.18</td><td>76.3</td><td>76.25</td></tr><tr><td>B (MHz)</td><td>440</td><td>440</td><td>512</td><td>425</td><td>410</td><td>300</td></tr><tr><td>TPRI (µS)</td><td>31.1</td><td>31.1</td><td>56.7</td><td>35.1</td><td>31.1</td><td>38.8</td></tr><tr><td>Chirp rate  $( \mathrm { M H z } / \mu \mathrm { s } )$ </td><td>14.38</td><td>14.38</td><td>-9.11</td><td>13.89</td><td>-13.4</td><td>7.83</td></tr></table>

## B. Performance Metrics on Measured Data

To evaluate the methods mentioned above on measured interference data, where the target scene is static and the interferers have been configured as shown in Table II, we have used the interference-free measurement for reference. Here, we established a set of RDM bins $\tau$ that belong to targets, which is obtained from an ordered statistic constant false alarm rate (OS-CFAR) detector [51] with configurations $N _ { \mathrm { N C I } } = 4$ and $P _ { \mathrm { F A } } = 1 0 ^ { - 6 }$ . The probability of detection $( P _ { D } )$ and false alarm $( P _ { \mathrm { F A } } )$ are analyzed on the interference-mitigated RDMs.

Generally, SINR calculated from (27) is used for evaluation; however, this metric causes the high SINR values to overshadow the low SINR values. Consequently, we calculate the NSINR instead, which is calculated for all target bins in $\tau$ by subtracting the expected SINR from the empirical SINR, using the following equations:

$$
\mathrm { S I N R } [ c , d ] = 1 0 \log _ { 1 0 } \left( \frac { | \hat { \mathbf { X } } [ c , d ] | ^ { 2 } } { \frac { 1 } { | B | } \sum _ { \{ p , q \} \notin { \cal T } } | \hat { \mathbf { X } } \big [ p , q \big ] | ^ { 2 } } \right)\tag{27}
$$

$$
\mathrm { S I N R } _ { \mathrm { r e f } } [ c , d ] = 1 0 \log _ { 1 0 } \left( \frac { \mathbb { E } \big [ | \mathbf { X } _ { \mathrm { c l e a n } } [ c , d ] | ^ { 2 } \big ] } { \frac { 1 } { | \mathcal { B } | } \sum _ { \{ p , q \} \notin T } \mathbb { E } \big [ | \mathbf { X } _ { \mathrm { c l e a n } } \big [ p , q \big ] | ^ { 2 } \big ] } \right)\tag{28}
$$

$$
\mathrm { N S I N R } [ c , d ] = \mathrm { S I N R } [ c , d ] - \mathrm { S I N R } _ { \mathrm { r e f } } [ c , d ] \forall \{ c , d \} \in \mathcal { T }\tag{29}
$$

where |B| refers to the total number of background bins, i.e., bins not belonging to $\tau$ . Moreover, we introduce a metric that originates from the medical imaging domain [52] that specifically analyzes how well the probability density function (pdf) of the target signals in $\tau$ is separated from the pdf of the noise-plus-interference signal. This metric is invariant to arbitrary dynamic range stretching, e.g., via nonlinear elementwise operations, and is therefore well suited for analyzing algorithms such as RFmin, as well as deep learning methods. We call this metric the gtnr. The gTNR is calculated using

$$
\mathrm { g T N R } = 1 - \int \mathrm { m i n } \{ p _ { t } ( x ) , p _ { n } ( x ) \} d x\tag{30}
$$

where $p _ { t } ( x )$ and $p _ { n } ( x )$ refer to the pdf of the target signal based on $\tau$ and its complement B, respectively. If $p _ { t } ( x )$ and $p _ { n } ( x )$ completely overlap $\mathrm { g T N R } = 0$ , while $\mathrm { g T N R } = 1$ when the distributions are completely separated. The latter case is most desired to have the target signals well separated from the thermal noise and interference signals. In Fig. 7, the distributions are presented for a clean and a contaminated range–Doppler power spectrum $| \mathbf { X } | ^ { 2 }$ . In this specific example, $\mathrm { g T N R } ( \mathbf X _ { \mathrm { c l e a n } } ) = 0 . 9 3$ and $\mathrm { g T N R } ( \mathbf { X } _ { \mathrm { n o - m i t } } ) = 0 . 6 5$

![](images/de9c520471b20bf72a91782e079f368d5e44354744f4ef240a063f31da6b32d7.jpg)  
Fig. 7. PDFs of the target power (solid) and noise power (dotted), calculated from the $\tau$ and B sets of RDM bins for an interference-free case (blue) and interference case without any applied mitigation (green).

## C. Discussion

First, we analyze the detection performance of the interference-mitigated signals, which addresses how well the target signals are recovered, whether the interference energy is suppressed, and whether the noise statistics are not impacted such that conventional constant false alarm rate (CFAR) detection strategies still apply. The CFAR detector is explicitly designed to operate under the additive white Gaussian noise (AWGN) assumption. In Fig. 8(a) and (b), $P _ { D }$ and $P _ { \mathrm { F A } }$ are shown for the before-mentioned mitigation strategies for the four-interferer scenario. All methods are effective in removing interference, partially or fully, proving a higher $P _ { D }$ and lower $P _ { \mathrm { F A } }$ compared to the case without any mitigation being applied. Besides, IMAT reduces the zeroing artifacts, but its performance is impacted by incorrect phase estimation whenever a large amount of fast-time samples is affected, degrading its reconstruction capabilities [25]. AR-ST benefits from the slow-time reconstruction with fewer consecutive contaminated samples; however, this comes at the cost of increased latency. RFmin can remove interference effectively but also harms weak target detection, and it alters the noise statistics significantly. Therefore, its false alarms are increased compared to the other baselines. Split augmented Lagrangian shrinkage algorithm (SALSA) and LowRaS do not show compelling interference removal capabilities, while BKCS does not improve the zeroing artifacts and shows worse detection performance than time-domain zeroing in this experiment. The 2-D sparse reconstruction methods, ALFISTA and NA-ALFISTA, are superior in mitigation performance and come close to the interference-free scenario, and NA-ALFISTA outperforms ALFISTA slightly.

Moreover, we present the empirical cumulative distribution function (cdf) of the NSINR, as calculated in (29), in Fig. 9. This metric shows how the SINR is altered, and ideally, it shall be on top or to the right of the NSINR of the clean signal that is depicted in black. Once again, it can be observed that the 2-D sparse signal recovery methods, ALFISTA and NA-ALFISTA, show better performance in reconstructing weaker target signals in the −10- to 0-dB range. Interestingly, NA-ALFISTA with $\ K \ = \ 5$ presents better NSINR than ALFISTA with K = 15 indicating that convergence is reached faster.

![](images/83ecd048c71e6136dd5d49548592dbdf8a6a7baf290b7db27d1be36a1e25d44a.jpg)

(a)  
![](images/3cb218c5905368163db8b9fe0e7151c12000fec9b7512676ec4f6ff82f00df28.jpg)  
(b)

Fig. 8. OS-CFAR detection performance in terms of (a) probability of detection $P _ { D }$ and (b) probability of false alarms $P _ { \mathrm { F A } }$ for the scenario with four active interferers.  
![](images/917c10761d8f92a0e37ece5a4bfc01d7db2acd3906a0ce4bce5e1bb16f9ed339.jpg)  
Fig. 9. Empirical cdf of NSINR in the scenario with four active interferers

Analogous to the detection performance results, NA-ALFISTA with $\begin{array} { r c l } { K } & { = } & { 1 5 } \end{array}$ is superior in separating the target signals from interference plus noise by inspecting the gTNR, as depicted in Table III. It is consistently better for every combination of interferers, showing its robustness against several types of interference, as well as different interference distortion ratios r . Therefore, we claim that the trained network generalizes well even though it was trained on simulated data. Many of the detect-and-repair methods do

## TABLE III

gTNR (↑) ON THE MITIGATED RDM s OF REAL MEASUREMENTS. THE MEAN AND STANDARD DEVIATION BASED ON 1000 FRAMES ARE PRESENTED FOR DIFFERENT INTERFERENCE CONFIGURATIONS. THE BEST AND SECOND-BEST gTNR MEAN AND STANDARD DEVIATION VALUES ARE HIGHLIGHTED USING BOLDFACE AND UNDERLINED FONTS, RESPECTIVELY  
![](images/6a8429970d44eb18f977fe9a030659aa07caf9a190458f6c313bd607b1d93579.jpg)

<table><tr><td colspan="10">Interferer Active I2</td><td colspan="7">Interference Mitigation Methods</td></tr><tr><td colspan="2">I1 X</td><td>I3 I4</td><td>No Mit  $\overline { { 0 . 9 7 0 \pm 0 . 0 0 5 } }$ </td><td> $\operatorname { Z e r o i n g }$ </td><td>IMAT  $\overline { { 0 . 9 6 5 \pm 0 . 0 0 5 } }$ </td><td>AR-ST  $\overline { { 0 . 9 7 0 \pm 0 . 0 0 5 } }$ </td><td></td><td>RFmin  $\overline { { 0 . 8 6 7 \pm 0 . 0 0 9 } }$ </td><td>SALSA  $\overline { { 0 . 9 6 9 \pm 0 . 0 0 5 } }$ </td><td>LowRaS  $\overline { { 0 . 9 6 7 \pm 0 . 0 0 5 } }$ </td><td>BKCS  $\overline { { 0 . 7 0 8 \pm 0 . 0 2 4 } }$ </td><td> $\mathrm { A L F I S T A } ( 1 5 )$   $\overline { { 0 . 9 6 2 \pm 0 . 0 0 8 } }$ </td><td> ${ \mathrm { N A } } { \mathrm { - A L F I S T A } } ( 5 )$ </td><td></td><td>NA-ALFISTA(15)</td></tr><tr><td></td><td></td><td>X x</td><td></td><td> $\overline { { 0 . 9 6 2 \pm 0 . 0 0 5 } }$ </td><td></td><td></td><td></td><td></td><td></td><td></td><td> $0 . 8 1 2 \pm 0 . 0 7 9$ </td><td> $0 . 9 5 2 \pm 0 . 0 1 0$ </td><td></td><td> $\overline { { 0 . 9 5 4 \pm 0 . 0 1 0 } }$ </td><td> $\mathbf { \overline { { 0 . 9 8 0 \pm 0 . 0 0 5 } } }$ </td></tr><tr><td></td><td></td><td></td><td> $\overline { { 0 . 6 9 5 \pm 0 . 1 5 5 } }$ </td><td> $0 . 9 1 4 \pm 0 . 0 3 2$ </td><td> $0 . 9 1 6 \pm 0 . 0 3 0$ </td><td></td><td> $0 . 9 3 7 \pm 0 . 0 1 8$ </td><td> $0 . 7 3 5 \pm 0 . 0 9 8$ </td><td> $0 . 7 8 9 \pm 0 . 1 0 7$ </td><td> $0 . 7 0 9 \pm 0 . 1 5 9$ </td><td></td><td></td><td></td><td> $0 . 9 5 3 \pm 0 . 0 1 5$ </td><td>0.963 ± 0.008</td></tr><tr><td></td><td></td><td></td><td> $0 . 9 1 4 \pm 0 . 0 4 7$ </td><td> $0 . 9 3 8 \pm 0 . 0 2 2$ </td><td> $0 . 9 3 9 \pm 0 . 0 2 4$ </td><td></td><td> $0 . 9 6 1 \pm 0 . 0 1 1$ </td><td> $0 . 8 6 2 \pm 0 . 0 0 9$ </td><td> $0 . 9 4 5 \pm 0 . 0 2 0$ </td><td> $0 . 9 1 2 \pm 0 . 0 4 8$ </td><td> $0 . 7 8 2 \pm 0 . 0 5 1$ </td><td></td><td> $\underline { { 0 . 9 7 2 \pm 0 . 0 0 7 } }$ </td><td> $\overline { { 0 . 9 7 1 \pm 0 . 0 1 0 } }$ </td><td>0.982 ± 0.004</td></tr><tr><td></td><td></td><td></td><td> $0 . 9 2 8 \pm 0 . 0 3 8$ </td><td>0.971 ± 0.010</td><td></td><td> $0 . 9 7 1 \pm 0 . 0 0 8$ </td><td> $\underline { { 0 . 9 7 6 \pm 0 . 0 0 8 } }$ </td><td> $0 . 8 4 4 \pm 0 . 0 3 1$ </td><td> $0 . 9 3 7 \pm 0 . 0 3 3$ </td><td> $0 . 9 2 9 \pm 0 . 0 3 8$ </td><td> $0 . 8 1 3 \pm 0 . 0 6 9$ </td><td></td><td> $\overline { { 0 . 9 7 5 \pm 0 . 0 0 7 } }$ </td><td> $0 . 9 7 4 \pm 0 . 0 1 0$ </td><td>0.984 ± 0.004</td></tr><tr><td></td><td></td><td></td><td> $\phantom { - } 0 . 9 2 7 \pm 0 . 0 1 4$ </td><td> $0 . 9 2 2 \pm 0 . 0 1 3$ </td><td></td><td>0.925 ± 0.013</td><td> $\overline { { 0 . 9 3 5 \pm 0 . 0 1 2 } }$ </td><td> $0 . 8 4 0 \pm 0 . 0 1 2$ </td><td> $0 . 9 3 2 \pm 0 . 0 1 2$ </td><td> $\begin{array} { c } { { \mathrm { 0 . 9 2 9 \_ } ^ { \mathrm { 1 } } \mathrm { 0 . 0 9 0 } } } \\ { { \mathrm { 0 . 9 2 7 + n . 0 1 2 } } } \end{array}$ </td><td> $0 . 6 7 7 \pm 0 . 0 2 1$ </td><td></td><td> $\underline { { 0 . 9 4 5 \pm 0 . 0 0 9 } }$ </td><td> $0 . 9 3 7 \pm 0 . 0 1 1$ </td><td> $\begin{array} { r } { \mathbf { 0 . } \mathbf { 0 0 4 } \pm \mathbf { 0 . } \mathbf { 0 U 4 } } \\ { \mathbf { 0 . } \mathbf { 0 7 0 } + \mathbf { n 0 } \mathbf { 0 } \mathbf { 6 } } \end{array}$  0.970 ± 0.006</td></tr><tr><td></td><td></td><td></td><td> $0 . 6 6 5 \pm 0 . 1 1 8$ </td><td> $0 . 8 7 3 \pm 0 . 0 4 4$ </td><td></td><td> $0 . 8 6 3 \pm 0 . 0 4 1$ </td><td> $0 . 9 0 1 \pm 0 . 0 3 5$ </td><td> $0 . 7 0 6 \pm 0 . 0 9 0$ </td><td> $0 . 7 4 6 \pm 0 . 0 8 9$ </td><td> $0 . 6 6 9 \pm 0 . 1 2 0$ </td><td> $0 . 8 3 7 \pm 0 . 0 3 4$ </td><td></td><td> $\overline { { 0 . 9 2 9 \pm 0 . 0 1 6 } }$ </td><td> $\underline { { 0 . 9 3 5 \pm 0 . 0 1 6 } }$ </td><td>0.936 ± 0.018</td></tr></table>

![](images/68e1edf902fa31522a53b07e2fcf1dc611dbcb639dfe403f8aaadef50d7b97c5.jpg)

![](images/be346560c70aa2d3ad9b8e611a6fb3df830e54b84427e01be25294c1c0b8d112.jpg)

![](images/0851947da5142d93c2481a2329a0c89206eacdfb88b3ebb4d86ca65c85ce9fce.jpg)

(a)  
![](images/4b0dfb34d9768401c2438b3a66d1ac4207621b7dae1554376978e66603f7ecf2.jpg)  
(e)

(b)  
![](images/3d871862474e463ee32c4c82162b0ab3405d720fa6d5594793517aae00146bb1.jpg)  
(f)

(c)  
![](images/f59a5904b81a5b80318a5ecbfa267cc047da77b0914e70361d5d655663fa4528.jpg)  
(d)

(i)  
![](images/b94e51049753a63e51b2478705adf160c62bfc66963644117e703d4db77f0a77.jpg)  
(j)

![](images/22f62e22bab63a16e24caf4cb9d8364a49aea52dccc65c151549b543f6f2f962.jpg)

![](images/57866b79395f5e7f40ba496a09c1ff94ccc69286486daa133b442995ad0c93a6.jpg)

(g)  
![](images/31505beeeaa6622890116971b803c1dd8a2997c6c4433577d762da074489f3a1.jpg)  
(k)

(h)  
![](images/8d0edf10bef504edf98ec13aa626e0699b6fd89ac1aab9fd82eaf8716e937925.jpg)  
(l)  
Fig. 10. Comparison of performance in RDM in a dynamic scenario with all four interferers active. (a) Clean. (b) No mitigation. (c) Zeroing. (d) IMAT. (e) AR-ST. (f) RFmin. (g) SALSA. (h) LowRaS. (i) BKCS. (j) ALFISTA(15). (k) NA-ALFISTA(5). (l) NA-ALFISTA(15).

not improve over time-domain zeroing when inspecting the gTNR.

In Fig. 10, we present a selection of the clean, raw, and mitigated RDMs for a dynamic scenario with the ego-vehicle moving past the static interferers, as shown in Fig. 6(b). In Fig. 10(b), an RDM is shown that showcases the effects of various types of interferes: 1) uncorrelated interference with the energy after postprocessing is distributed over a large number of bins and 2) semi-uncorrelated interference where the interference is present in similar fast-time bins across slow time causing the energy in the concentrate in specific range bins or velocity bins, i.e, the vertical and horizontal traces with interference energy. The 2TX-DDMA multiplexing divides the total number of unambiguous Doppler bins by $N _ { T }$ , inherently resulting in a less sparse RDM. This could harm BKCS that uses subsets of the ADC data $\mathbf { Y } _ { m } .$ , which can explain why the reconstruction performance degrades compared to the simulation results presented in Section V. The reconstruction performance of ALFISTA and NA-ALFISTA is similar to the clean RDM.

From Fig. 10, it is obvious that no interference leaks in due to proper interference detection. However, under nonideal interference detection, the sample-based interference detection scheme misclassifies clean signals from corrupted signals, which may lead to interference leakage when false negatives occur and target signal suppression when false positives in interference detection occur. The Appendix explains the impact of imperfect interference detection. To address this issue, the proposed method can be further improved for cases of imperfect interference detection by defining the interference detection mask ${ \bf m } _ { p }$ with soft samples, i.e., the values of $\mathbf { A } _ { p }$ being in the interval (0, 1). Consequently, the interference detection algorithm can be designed to give weight to its detection based on the uncertainty of interference being present. Inherently, our proposed sparse recovery method takes this sample-based a priori information, i.e., using $\mathbf { A } _ { p } ,$ into account in the data-consistency step. Therefore, this soft-sample approach supports interference removal whenever interference detection is expected to be imperfect.

![](images/788c18fbdd07ebad889a208d67a4159ba34e8408ee2d2f2b8b82382e0302c115.jpg)  
Fig. 11. Execution time of all algorithms used in the comparison.

Finally, the runtime of all algorithms is presented in Fig. 11, which indicates the total execution time of mitigating interference in the entire data cube of size $( N _ { R } \times N _ { C } \times$ $N _ { F } )$ . All experiments were executed on an NVIDIA Geforce RTX 3080 GPU, where parallel computation was maximized. Therefore, these results give an estimation, and implementation optimization may still be possible. The runtime of LowRaS and BKCS is immense, which will be a challenge to realize real-time operation. During this experiment, BKCS required to run for $4 \times 4 \times 1 2 8 ~ = ~ 2 0 4 8$ blocks, which makes it difficult to run in real time. Although ALFISTA and NA-ALFISTA last longer than time-domain zeroing, IMAT and RFmin, its performance increase may justify it. Furthermore, we have computed the actual number of FLOPs of the Pytorch implementations for ALFISTA and NA-ALFISTA using the DeepSpeed tool [53], which entails that the computational load per layer increases by $1 . 2 2 \times 1 0 ^ { - 5 } \%$ compared to ALFISTA due to the neural augmentation network. However, under the assumption that NA-ALFISTA achieves similar reconstruction performance with a reduced number of layers compared to ALFISTA, the total complexity of ALFISTA(15) and NA-ALFISTA(5) amounts to 1036.75 and 342.5 GFLOPs, respectively.

## VII. CONCLUSION

In this work, we designed a neutrally augmented modelbased solution, NA-ALFISTA, for mitigating FMCW radar interference. Sparsity is leveraged in the range–Doppler spectra, which is utilized to reconstruct the zeroed ADC samples. The neural network was purely trained on simulated data, while evaluation was done on real-world measurements. Eminent performance was obtained by applying NA-ALFISTA, outscoring all the presented state-of-the-art methods in both simulated and measured data. Furthermore, it was shown that when a radar deploys DDMA MIMO, the amount of sparsity in the RDM is reduced and can impact the sparse recovery performance, e.g., in BKCS. The measurement results in terms of detection performance, i.e., probability of detection and false alarm, the generalized target-to-noise ratio, and NSINR, have substantiated that NA-ALFISTA outperforms the existing methods by significant margins. Therefore, exploitation of Authorized licensed use limited to: Eindhoven University of Technology. Downloa the 2-D data alongside the neural augmentation allows for fast convergence and accurate recovery even when a DDMA transmit scheme is used. Therefore, the proposed method will enable robust interference mitigation in scenarios with significant amounts of interference-corrupted time-domain samples.

![](images/15e8ed2f42a5fd579f2207fa64f3680f7771beb6804436e1b36975c0ae932281.jpg)  
Fig. 12. RDM showing that imperfect interference detection can lead to interference leakage after mitigation.

## APPENDIX

## IMPERFECT INTERFERENCE DETECTION

Fig. 12 presents an RDM of a scenario where interference detection fails partially. From (6), one can observe that when $\mathbf { A } _ { p } \mathbf { i } _ { m , p } \neq \mathbf { 0 }$ for the pth chirp, the interference energy will partially leak into further postprocessing steps and can affect the detection performance of the radar. Then, any detectand-repair method will suffer and cannot fully suppress the interference. In this example, we illustrate the output of NA-ALFISTA(5).

## REFERENCES

[1] I. Bilik, “Comparative analysis of radar and LiDAR technologies for automotive applications,” IEEE Intell. Transp. Syst. Mag., vol. 15, no. 1, pp. 244–269, Jan. 2023.

[2] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[3] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[4] K. Doris, A. Filippi, and F. Jansen, “Reframing fast-chirp FMCW transceivers for future automotive radar: The pathway to higher resolution,” IEEE Solid State Circuits Mag., vol. 14, no. 2, pp. 44–55, Jul. 2022.

[5] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in Proc. German Microw. Conf., Mar. 2011, pp. 1–4.

[6] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[7] A. Ossowska et al., “IMIKO-radar: Interference measurements of today’s automotive radar sensors,” in Proc. 21st Int. Radar Symp. (IRS), Berlin, Germany, Jun. 2021, pp. 1–6.

[8] C. Aydogdu, M. F. Keskin, and H. Wymeersch, “Automotive radar interference mitigation via multi–hop cooperative radar communications,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 270–273.

[9] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[10] L. L. Tovar Torres, T. Grebner, and C. Waldschmidt, “Automotive radar interference avoidance strategies for complex traffic scenarios,” in Proc IEEE Radar Conf., May 2023, pp. 1–6.

[11] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[12] J. Overdevest, F. Jansen, F. Laghezza, F. Uysal, and A. Yarovoy, “Uncorrelated interference in 79 GHz FMCW and PMCW automotive radar,” in Proc. 20th Int. Radar Symp. (IRS), Jun. 2019, pp. 1–8.

[13] W. Buller et al., “Radar congestion study,” Nat. Highway Traffic Saf. Admin., Washington, DC, USA, Tech. Rep. DOT HS 812 632, 2018.

[14] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: Modulation schemes and interference mitigation,” IEEE Microw. Mag., vol. 20, no. 9, pp. 58–72, Sep. 2019.

[15] J. Overdevest, F. Jansen, F. Uysal, and A. Yarovoy, “Doppler influence on waveform orthogonality in 79 GHz MIMO phase-coded automotive radar,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 16–25, Jan. 2020.

[16] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in Proc. IEEE Radar Conf., Apr. 2019, pp. 1–6, doi: 10.1109/RADAR.2019.8835681.

[17] M. Toth, J. Rock, P. Meissner, A. Melzer, and K. Witrisal, “Analysis of automotive radar interference mitigation for real-world environments,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 176–179.

[18] T.-N. Luo, C. E. Wu, and Y. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[19] U. Kumbul, N. Petrov, C. S. Vaucher, and A. Yarovoy, “Smoothed phasecoded FMCW: Waveform properties and transceiver architecture,” IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 2, pp. 1720–1737, Apr. 2023.

[20] F. Lampel et al., “System level synchronization of phase-coded FMCW automotive radars for RadCom,” in Proc. 14th Eur. Conf. Antennas Propag. (EuCAP), Mar. 2020, pp. 1–5.

[21] S. Jin, P. Wang, P. Boufounos, P. V. Orlik, R. Takahashi, and S. Roy, “Spatial-domain interference mitigation for slow-time MIMO-FMCW automotive radar,” in Proc. IEEE 12th Sensor Array Multichannel Signal Process. Workshop (SAM), Jun. 2022, pp. 311–315.

[22] A. Dubey, J. Fuchs, V. Madhavan, M. Lübke, R. Weigel, and F. Lurz, “Region based single-stage interference mitigation and target detection,” in Proc. IEEE Radar Conf., Sep. 2020, pp. 1–5.

[23] J. Bechter, K. Eid, F. Roos, and C. Waldschmidt, “Digital beamforming to mitigate automotive radar interference,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4, doi: 10.1109/ICMIM.2016. 7533914.

[24] C. Fischer, M. Goppelt, H.-L. Blöcher, and J. Dickmann, “Minimizing interference in automotive radar using digital beamforming,” Adv. Radio Sci., vol. 9, pp. 45–48, Jul. 2011.

[25] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[26] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[27] T. Fei, H. Guang, Y. Sun, C. Grimm, and E. Warsitz, “An efficient sparse sensing based interference mitigation approach for automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 274–277, doi: 10.1109/EuRAD48048.2021.00077.

[28] J. Overdevest, A. G. C. Koppelaar, M. J. G. Bekooij, J. Youn, and R. J. G. V. Sloun, “Signal reconstruction for FMCW radar interference mitigation using deep unfolding,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Jun. 2023, pp. 1–5.

[29] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” Proc. IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Jul. 2019.

[30] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[31] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[32] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[33] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in Proc. IEEE Int. Symp. Circuits Syst. (ISCAS), May 2018, pp. 1–4.

[34] C. Waldschmidt, J. Hasch, and W. Menzel, “Automotive radar— From first efforts to future systems,” IEEE J. Microw., vol. 1, no. 1, pp. 135–148, Jan. 2021.

[35] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 624–629, doi: 10.1109/RADAR42522.2020.9114627.

[36] S. Chen, J. Taghia, U. Kuhnau, N. Pohl, and R. Martin, “A twostage DNN model with mask-gated convolution for automotive radar interference detection and mitigation,” IEEE Sensors J., vol. 22, no. 12, pp. 12017–12027, Jun. 2022.

[37] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2020, pp. 3802–3806.

[38] C. Jiang, Z. Zhou, and B. Yang, “Unsupervised deep interference mitigation for automotive radar,” in Proc. IEEE 12th Sensor Array Multichannel Signal Process. Workshop (SAM), Jun. 2022, pp. 296–300.

[39] A. Shultzman, E. Azar, M. R. D. Rodrigues, and Y. C. Eldar, “Generalization and estimation error bounds for model-based neural networks,” 2023, arXiv:2304.0980.

[40] N. Shlezinger, J. Whang, Y. C. Eldar, and A. G. Dimakis, “Model-based deep learning,” Proc. IEEE, vol. 111, no. 5, pp. 465–499, May 2023.

[41] A. Balatsoukas-Stimming and C. Studer, “Deep unfolding for communications systems: A survey and some new directions,” in Proc. IEEE Int. Workshop Signal Process. Syst., Jun. 2019, pp. 1–22.

[42] V. Monga, Y. Li, and Y. C. Eldar, “Algorithm unrolling: Interpretable, efficient deep learning for signal and image processing,” IEEE Signal Process. Mag., vol. 38, no. 2, pp. 18–44, Mar. 2021.

[43] F. Laghezza, F. Jansen, and J. Overdevest, “Enhanced interference detection method in automotive FMCW radar systems,” in Proc. 20th Int. Radar Symp. (IRS), Jun. 2019, pp. 1–7.

[44] W. Deng, W. Yin, and Y. Zhang, “Group sparse optimization by alternating direction method,” in Wavelets and Sparsity XV, vol. 8858. Bellingham, WA, USA: SPIE, 2013, pp. 242–256.

[45] I. Daubechies, M. Defrise, and C. De Mol, “An iterative thresholding algorithm for linear inverse problems with a sparsity constraint,” Commun. Pure Appl. Math., vol. 57, no. 11, pp. 1413–1457, Nov. 2004.

[46] A. Beck and M. Teboulle, “A fast iterative shrinkage-thresholding algorithm with application to wavelet-based image deblurring,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., Apr. 2009, pp. 693–696.

[47] K. Gregor and Y. LeCun, “Learning fast approximations of sparse coding,” in Proc. 27th Int. Conf. Mach. Learn. (ICML), Jun. 2010, pp. 399–406.

[48] F. Behrens, J. Sauder, and P. Jung, “Neurally augmented ALISTA,” 2020, arXiv:2010.01930.

[49] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” 2019, arXiv:1711.05101.

[50] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” 2017, arXiv:1412.6980.

[51] H. Rohling, “Ordered statistic CFAR technique—An overview,” in Proc. 12th Int. Radar Symp. (IRS), Sep. 2011, pp. 631–638.

[52] A. Rodriguez-Molares, O. M. H. Rindal, J. D’Hooge, S. Måsøy, A. Austeng, and H. Torp, “The generalized contrast-to-noise ratio,” in Proc. IEEE Int. Ultrason. Symp. (IUS), Oct. 2018, pp. 1–4.

[53] J. Rasley, S. Rajbhandari, O. Ruwase, and Y. He, “DeepSpeed: System optimizations enable training deep learning models with over 100 Billion parameters,” in Proc. 26th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, 2020, pp. 3505–3506.

![](images/442665e4d8550bc035a98460c2176cde18d3af791c29f2d14abc2777dad97e5a.jpg)

Jeroen Overdevest (Student Member, IEEE) was born in ’s-Gravenhage, The Netherlands, in 1993. He received the B.Sc. and M.Sc. degrees in electrical engineering from the Delft University of Technology, Delft, The Netherlands, in 2015 and 2018, respectively.

After completing the M.Sc. at NXP Semiconductors, he joined the Signal Processing Algorithms Group of NXP Semiconductors, Eindhoven, The Netherlands, in 2018. In 2021, he started the Ph.D. with SPS within the RAISE program, where he applies model-based deep learning to mitigate real-world radar artifacts. His research interests include signal processing, model-based deep learning, and waveform design for mm-wave automotive radar.

![](images/57867636596bce306eaccd7b64f9aa4cddb8a2891a910f2e75323ddd178129da.jpg)

Arie G. C. Koppelaar was born in 1966. He received the master’s degree in electrical engineering from the Eindhoven University of Technology, Eindhoven, The Netherlands, in March 1992.

From 1992 to 2000, he was a scientific worker at Philips Research Laboratories, Eindhoven, where he worked in the field of error-correcting codes and digital modulation. In 2000, he joined Philips Semiconductors, Eindhoven, where he worked on baseband algorithms for IEEE802.11b and TVon-Mobile. Since 2006, he has been with NXP

![](images/d2827749798dee71135c92de80101e8ea65272cad6eb3f8d55e0647acd5fe45c.jpg)

Xinyi Wei received the B.Sc. degree from Shanghai Maritime University, Shanghai, China, and the M.Sc. degree in electrical engineering from the Eindhoven University of Technology (TU/e), Eindhoven, The Netherlands.

She is currently working toward the Ph.D. degree with TU/e. Her research interests include automotive radar interference mitigation and deep learning.

Semiconductors in Eindhoven and worked on Car-to-Car communication and communication for Passive Keyless Entry systems. From 2019 onwards, he worked on digital signal processing algorithms for automotive MIMO FMCW radar.

![](images/9cbd69eeef1bb2baec089903c035a2b719cb7f88e9c2fe1c5423a5b9dbe72edb.jpg)

Jihwan Youn received the M.Sc. degree in robotics, systems and control from ETH Zurich, Zurich, Switzerland, in 2018, and the Ph.D. degree in health technology from the Technical University of Denmark, Kongens Lyngby, Denmark, in 2021.

After completing the Ph.D., he continued as a Postdoctoral Researcher at the Department of Electrical Engineering, Technical University of Eindhoven, Eindhoven, The Netherlands. Since 2023, he has been working as a Radar Signal Processing Engineer at NXP Semiconductors, Eindhoven. His research interests include signal processing, compressed sensing, and model-based AI for radar and array sensors.

![](images/71d0f9dc61c01a8e212d79600f989f524ee8681b3d637078e3fc2a6a969c865e.jpg)

Ruud J. G. van Sloun (Member, IEEE) received the M.Sc. and Ph.D. degrees (cum laude) in electrical engineering from Eindhoven University of Technology, Eindhoven, The Netherlands, in 2014 and 2018, respectively.

Currently, he is an Associate Professor with the Department of Electrical Engineering, Eindhoven University of Technology, Eindhoven. From 2019 to 2020, he served as a Visiting Professor with the Department of Mathematics and Computer Science, Weizmann Institute of Science, Rehovot, Israel.

From 2020 to 2023, he was a Kickstart AI Fellow with Philips Research. His current research interests include closed-loop image formation, deep learning for signal processing and imaging, active signal acquisition, model-based deep learning, compressed sensing, ultrasound imaging, and probabilistic signal, and image reconstruction.

Dr. Sloun has been honored with an ERC Starting Grant, an NWO VIDI Grant, an NWO Rubicon Grant, and a Google Faculty Research Award.