Received 3 September 2025; accepted 12 September 2025. Date of publication 16 September 2025; date of current version 7 October 2025. The review of this article was coordinated by Editor Lei Chu. Digital Object Identifier 10.1109/OJVT.2025.3610715

# Signal Decomposition Based Mutual Interference Suppression in FMCW Radars

ABHILASH GAUR <sup>1,2</sup> (Member, IEEE), PO-HSUAN TSENG <sup>3</sup> (Member, IEEE), KAI-TEN FENG <sup>4</sup> (Senior Member, IEEE), AND SESHAN SRIRANGARAJAN <sup>1,5</sup> (Senior Member, IEEE)

<sup>1</sup>Bharti School of Telecommunication Technology and Management, Indian Institute of Technology Delhi, New Delhi 110016, India <sup>2</sup>International College of Semiconductor Technology, National Yang Ming Chiao Tung University, Hsinchu 300093, Taiwan <sup>3</sup>Department of Electronic Engineering, National Taipei University of Technology, Taipei 10608, Taiwan <sup>4</sup>Department of Electronics, Electrical Engineering, National Yang Ming Chiao Tung University, Hsinchu 300093, Taiwan <sup>5</sup>Department of Electrical Engineering, Indian Institute of Technology Delhi, New Delhi 110016, India

CORRESPONDING AUTHOR: KAI-TEN FENG (e-mail: ktfeng@nycu.edu.tw).

This work was supported in part by the National Science, Technology Council (NSTC) under Grant NSTC 114-2218-E-A49-019, Grant   
113-2221-E-A49-119-MY3, Grant 114-2218-E-A49-017, Grant 112UC2N006, and Grant 112UA10019, in part by the Higher Education Sprout Project of National Yang Ming Chiao Tung University (NYCU), the Ministry of Education (MoE), in part by the National Defense Science, Technology Academic Collaborative   
Research Projectins, in part by the Co-creation Platform of the Industry-Academia Innovation School, NYCU, through the National Key Fields Industry-University   
Cooperation, Skilled Personnel Training Act, funded by MoE, industry partners in Taiwan, in part by Realtek Semiconductor Corp., in part by Hon Hai Research Instituteins, in part by the National Science, Technology Council (NSTC) under Grant 112-2314-B-002-192-MY3, Grant 113-2221-E-027-047-MY3, and Grant 113-2221-E-027-078, and in part by the University System of Taipei Joint Research Program under Grant USTP-NTUT-NTPU-105-02 and Grant USTP-NTUT-NTPU-106-02.

ABSTRACT With the increasing use of frequency modulated continuous wave (FMCW) radars in autonomous vehicles, mutual interference among FMCW radars poses a serious challenge. In this work, we present a novel approach to effectively and elegantly suppress mutual interference in FMCW radars. We first decompose the received signal into modes using variational mode decomposition (VMD) and perform time-frequency analysis using Fourier synchrosqueezed transform (FSST). The interference-suppressed signal is then reconstructed by applying a proposed energy-entropy-based thresholding operation on the time-frequency spectra of the VMD modes. The effectiveness of the proposed method is measured in terms of signal-to-interference plus noise ratio (SINR), correlation coefficient, and probability of detection in the presence of FMCW interference. Furthermore, the interference suppression ability of the proposed VAFER scheme is evaluated for stationary and moving target scenarios by performing a range Doppler analysis in the presence of interference. Compared to the existing literature, the proposed method demonstrates significant improvement in the output SINR by at least 15.46 dB for simulated data and 9.87 dB for experimental data.

INDEX TERMS Interference suppression, variational mode decomposition, frequency modulated continuous wave radar (FMCW).

## I. INTRODUCTION

Automotive radars pave the way for advanced driver assistance systems (ADAS) development due to their robust operation under bad weather conditions and affordability. Frequency modulated continuous wave (FMCW) radars are preferred in the automotive industry due to their ability to measure range, angle, and velocity [1]. In addition to radars’ attractive performance and reliability, recent developments in integrated radio frequency complementary metal-oxidesemiconductor (RF-CMOS) technology have enabled lowcost radar-on-chip systems in the 76-81 GHz band [2].

As automotive radars find application in lane-change assistance, ADAS, automatic emergency braking, etc., the number of such radars on vehicles are expected to increase in the near future. With the increasing density of automotive FMCW radars, mutual interference among these radars will be severe [3], [4]. During FMCW data processing, targets appear in the form of tones (beat signal) at the baseband, whereas external FMCW interference with a different chirp slope would appear as a chirp. Strong interference increases the noise floor and reduces separability of the target return from the background, thus reducing the probability of detection.

In the existing literature, several methods have been proposed to suppress mutual interference among FMCW radars. In [5], [6], [7], different coordination methods are proposed for radar systems to avoid interference by modifying radar parameters. A phase-coded FMCW radar system is presented in [5] to mitigate interference. In [6], authors proposed a medium access control (MAC)-like approach that dynamically assigns radar parameters to multiple radars in the same area by communicating via a dedicated long-term evolution (LTE) link to a cloud-based system. A distributed networking protocol is proposed in [7] to avoid mutual interference. These coordination methods avoid FMCW radar interference at the cost of adding a coordination unit to existing FMCW radar systems.

Some researchers have also proposed various interference suppression methods by designing new transmit waveforms and modifying the radar system architecture [8], [9], [10], [11], [12], [13]. To improve detection performance in the presence of homogeneous Gaussian interference, adaptive detectors for frequency diverse array (FDA) radar is proposed in [8]. The authors in [9] use the frequency hopping technique learned from bats to avoid mutual interference. In [10], orthogonal noise waveforms based on the phase retrieval method are transmitted to reduce the probability of interference. A spatial interference mitigation circuit (SIMC) is proposed in [11] to alleviate interference before the signal reaches the receiver. In [12], authors propose a multi-carrier frequency random transmission chirp sequence to avoid interference for time-division multiplexing (TDM) multi-input multi-output (MIMO) FMCW radars. These new waveform designs and system level changes result in an increased noise floor and affect the performance of radar’s parameter estimation, including range, velocity, and angle.

In addition, several other signal processing-based algorithms have been proposed in the literature to suppress interference [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]. In [15], a radio frequency interference (RFI) suppression algorithm based on orthogonal projection filtering is presented, in which the interference is estimated from the negative range bins and mitigated by projecting positive range bins onto the interference subspace. The performance of these filtering-based methods depends on the availability of a proper reference input. In [16], interference suppressed signal is reconstructed using a matrix pencil-based algorithm applied to the detected interference-contaminated signal regions. Meanwhile, the reconstructed interference signal in [17] is subtracted from the interference corrupted signal using the proposed wavelet transform-based algorithm. A signal separation-based algorithm using tunable Q-factor wavelet transform is proposed in [18].

Among signal processing-based algorithms, compressed sensing (CS) based algorithms have attracted researchers attention in recent years due to their simple structure and compatibility with pre-existing radar hardware. CS-based algorithms help in mitigating interference by exploiting the sparsity of either FMCW radar signal or interference signal or both. An iterative method with adaptive thresholding (IMAT) is presented in [24]. However, the performance of this method severely degrades with increasing interference duration. In [25], sparsity of the FMCW radar signal in the range-Doppler domain is examined, leading to an algorithm based on sparse Bayesian learning. Nevertheless, the algorithm demonstrates poor performance when the interference power is high. The framework presented in [26] mitigates interference in FMCW radars using sparse and low-rank Hankel matrix decomposition. This scheme exploits the time sparsity of interference and the spectral sparsity of the useful radar signal and formulates interference mitigation as a signal separation problem. Recently, the framework presented in [27] reduces interference in FMCW radars by a bi-level $\ell _ { 1 }$ optimization model using - -norm penalized least squares.

Mutual interference suppression in FMCW radars is inherently a non-stationary signal processing problem due to the time-varying nature of interfering chirps. Several recent studies have addressed this challenge using advanced decomposition and transform-based techniques. For instance, a variational mode decomposition (VMD) based interference mitigation method is proposed in [28] to reconstruct the interference-free signal by selecting useful modes. The framework in [29] employed the fractional Fourier transform (FrFT) to isolate chirp-like interference components for suppression in the fractional domain. In [30], a hybrid empirical mode decomposition (EMD)-MUSIC approach is proposed for interference mitigation and direction-of-arrival estimation. These works individually leverage non-stationary analysis tools but do not incorporate joint mode separation, high-resolution time-frequency localization, and adaptive reconstruction.

Recent studies have demonstrated the efficacy of VMD for mitigating mutual interference in automotive FMCW radar systems. In [31], an outlier-detection–aided VMD framework was proposed, wherein the received signal was first preprocessed to identify high-power interference components, followed by VMD-based decomposition. The IMFs are then selected using correlation coefficients to preserve the target while suppressing interference. Additionally, [32] proposed a two-stage method that combines VMD with adaptive envelope detection for low-SNR environments, showing improved mode isolation and robustness compared to traditional EMD or wavelet-based approaches. These prior efforts underscore the advantages of VMD in resolving overlapping chirp-like structures inherent in FMCW radar interference scenarios.

Building on these insights, we propose a unique mutual interference suppression algorithm for FMCW radars using VMD, Fourier synchrosqueezed transform (FSST), and energy-entropy thresholding-based reconstruction, named the VAFER method. In the interference-contaminated signal, targets are present as single-tone beat frequencies, while interference appears as a chirp. We decompose the interferencecontaminated received signals by using VMD [33] in different modes, containing information about the target’s beat frequencies and interference. We emphasize using VMD as a decomposition tool due to the ability of VMD to map these single-tone frequencies into individual modes. We further adopt FSST [34] for time-frequency analysis to distinguish among the different modes. The property of FSST to focus on sinusoid-like signals allows us to represent the modes corresponding to the target’s beat frequencies as individual lines parallel to the time axis, while interference appears as noise. However, the combination of VMD and FSST still cannot identify the various modes corresponding to the beat frequencies. Therefore, we propose an energy-entropy-based threshold utilizing Wiener entropy, which works as a measure of the spectral variation for the spectra (i.e., spikiness of spectra) produced by the FSST of the modes. Finally, the remaining modes which fall within the proposed energy-entropy threshold are combined to reconstruct the interference-suppressed signal. The main contributions of this paper are listed as follows:

\- We present an analytical framework proposing the firstever interference suppression technique for FMCW radars utilizing VMD to decompose interferencecontaminated signals into different modes and then adopting FSST on these modes to perform timefrequency analysis.

\- We propose an energy-entropy-based threshold to discard those VMD modes containing interference, and consequently reconstruct the interference-suppressed signals.

The interference suppression ability of the proposed VAFER algorithm is demonstrated via both simulations and experimental data. Compared with the recently proposed ANC [14], sparse and low-rank Hankel matrix decomposition method (SPARKLE) [26], wavelet denoising (WD) scheme [17], and the short-time Fourier transform (STFT)-based version of the VAFER method, the VAFER scheme achieves the best target detection performance and improves the output signal-tointerference plus noise ratio (SINR) by at least 9.87 dB.

This paper is organized as follows. Section II presents the signal model and the problem formulation. In Section III, the proposed VAFER method for interference suppression is described. The simulation and experimental results demonstrating the effectiveness of the VAFER algorithm are presented in Section IV, followed by the conclusions in Section V.

## II. SIGNAL MODEL AND PROBLEM FORMULATION

It is considered that Q point targets and M interfering radars exist in the observation scene. As shown in Fig. 1, the normalized transmitted chirp signal s(t ) at time t of the victim radar is

$$
s ( t ) = \exp \left[ j 2 \pi \left( f _ { o } t + \frac { 1 } { 2 } \mu t ^ { 2 } \right) \right] ,\tag{1}
$$

where $f _ { o }$ is the starting frequency, $\begin{array} { r } { \mu = \frac { B } { T } } \end{array}$ represents the chirp slope with B as the sweep bandwidth of a single ramp and T as time duration for $t \in [ 0 , T ]$ . On the other hand, the reflected signal received at the victim radar from the Q targets is the superposition of delayed transmitted signal s(t ) which can be expressed as

![](images/b264937cb6bc3cbc5df0494f98807f8620a340923d5aa99ab3e5abda1cf6b73d.jpg)  
FIG. 1. Network scenario for interfering FMCW radars.

$$
s _ { r } ( t ) = \sum _ { q = 1 } ^ { Q } \alpha _ { q } \exp \left[ j 2 \pi \left( f _ { o } ( t - \tau _ { q } ) + \frac { 1 } { 2 } \mu ( t - \tau _ { q } ) ^ { 2 } \right) \right] ,\tag{2}
$$

where $\tau _ { q }$ is the propagation delay and $\alpha _ { q }$ denotes the complex amplitude for the $q ^ { \mathrm { t h } }$ target. Each of the Q targets is assumed to be located at a distance $R _ { q }$ and moving with velocity $V _ { q } .$ The time-dependent propagation delay for the $q ^ { \mathrm { t h } }$ moving target is $\begin{array} { r } { \tau _ { q } = \frac { 2 ( R _ { q } + V _ { q } ^ { \bullet } t ) } { c } } \end{array}$ . The received signal at the antenna of the victim radar $s _ { r } ( t )$ is first de-chirped by mixing with a conjugate copy of transmitted signal s(t ) to obtain beat signal $s _ { b } ( t )$ as

$$
\begin{array} { l } { { \displaystyle s _ { b } ( t ) = s _ { r } ( t ) \cdot s ^ { * } ( t ) } , } \\ { { \displaystyle s _ { b } ( t ) = \sum _ { q = 1 } ^ { Q } \alpha _ { q } \exp \left[ j 2 \pi \left( - f _ { o } \tau _ { q } - \mu t \tau _ { q } + \frac { \mu \tau _ { q } ^ { 2 } } { 2 } \right) \right] . } } \end{array}\tag{3}
$$

Meanwhile, let $s _ { i n t } ( t )$ be the interference signal from interfering radars that affects the reflected signal $s _ { r } ( t )$ received from targets. Considering the $m ^ { \mathrm { t h } }$ interfering FMCW radar with chirp slope $\beta _ { m }$ and starting frequency $f _ { m }$ with time delay $\tau _ { m } ^ { \prime }$ with respect to the transmitted chirp, the total interference signal from M interfering radars observed at the receiver of the victim radar can be modeled as

$$
s _ { i n t } ( t ) = \sum _ { m = 1 } ^ { M } \exp \left[ j 2 \pi \left( f _ { m } ( t - \tau _ { m } ^ { \prime } ) + \frac 1 2 \beta _ { m } ( t - \tau _ { m } ^ { \prime } ) ^ { 2 } \right) \right] .\tag{4}
$$

At the receiver of the victim radar, the interference signal in (4) is de-chirped by mixing with a conjugate copy of transmitted signal $s ( t )$ . The interference signal $s _ { b , i n t } ( t )$ , obtained after de-chirping is expressed as

$$
\begin{array} { c l r } { { s _ { b , i n t } ( t ) = \displaystyle \sum _ { m = 1 } ^ { M } \exp \left[ j 2 \pi \left( ( f _ { m } - f _ { o } ) t + \frac { 1 } { 2 } ( \beta _ { m } - \mu ) t ^ { 2 } \right) \right] . } } \\ { { \exp \left[ j 2 \pi \left( - f _ { m } \tau _ { m } ^ { \prime } - \beta _ { m } t \tau _ { m } ^ { \prime } + \frac { \beta _ { m } } { 2 } \tau _ { m } ^ { \prime 2 } \right) \right] , } } \end{array}
$$

This can be expressed as

$$
\begin{array} { l } { { \displaystyle s _ { b , i n t } ( t ) = \sum _ { m = 1 } ^ { M } \alpha _ { I } \exp \bigg [ j 2 \pi \bigg ( ( f _ { m } - f _ { o } - \beta _ { m } \tau _ { m } ^ { \prime } ) t } } \\ { { \displaystyle ~ + \frac { 1 } { 2 } ( \beta _ { m } - \mu ) t ^ { 2 } \bigg ) \bigg ] , } } \end{array}\tag{5}
$$

where $\begin{array} { r } { \alpha _ { I } = \exp [ j 2 \pi ( f _ { m } \tau _ { m } ^ { \prime } + \frac { \beta _ { m } } { 2 } \tau _ { m } ^ { \prime 2 } ) ] } \end{array}$ . Note that while amplitude terms are retained in (3) for generality, they are omitted in the combined expression in (5). The interference is already modeled with normalized amplitude in (4); hence, (5) represents a fully normalized signal model. This simplification allows us to focus on the time–frequency characteristics and structural behavior of the interference, without being affected by absolute scaling.

A typical interference scenario is depicted in Fig. 1, where the received signal at the receiving antenna of the victim radar is the sum of target reflections $s _ { r } ( t )$ and interference signal $s _ { i n t } ( t ) , \mathrm { i . e . , } r ( t ) = s _ { r } ( t ) + s _ { i n t } ( t )$ . Therefore, after the de-chirping process the interference contaminated beat signal at the receiver of victim radar $r _ { b } ( t )$ can be expressed as

$$
\begin{array} { c } { r _ { b } ( t ) = \left[ s _ { r } ( t ) + s _ { i n t } ( t ) \right] \cdot s ^ { * } ( t ) , } \\ { = s _ { b } ( t ) + s _ { b , i n t } ( t ) . } \end{array}\tag{6}
$$

Next, this de-chirped beat signal $r _ { b } ( t )$ is passed through an analog low-pass filter (LPF) having impulse response h(t ). Note that the main purpose of passing through an LPF is to limit the received interference signal’s instantaneous frequency.

Based on (3) and (5), the total beat signal at the receiver of victim radar $\tilde { r } _ { b } ( t )$ can be obtained after de-chirping for Q targets and M interferers and then passing through LPF as

$$
\begin{array} { c c c } { { \tilde { r } _ { b } ( t ) = \displaystyle { \sum _ { q = 1 } ^ { Q } \alpha _ { q } \exp \left[ j 2 \pi \left( - f _ { o } \tau _ { q } - \mu t \tau _ { q } + \frac { \mu \tau _ { q } ^ { 2 } } { 2 } \right) \right] * h ( t ) } } } & { { } } & { { } } \\ { { } } & { { { } } } & { { { } } } \\ { { { } } } & { { { { } + \displaystyle { \sum _ { m = 1 } ^ { M } \alpha _ { I } \exp \left[ j 2 \pi \left( ( f _ { m } - f _ { o } - \beta _ { m } \tau _ { m } ^ { \prime } ) t \right. \right. } } } } \\ { { { } } } & { { { } } } & { { { } } } \\ { { { } } } & { { { } } } & { { { \left. \left. + \displaystyle { \frac { 1 } { 2 } ( \beta _ { m } - \mu ) t ^ { 2 } } \right) \right] * h ( t ) + \eta ( t ) . } } } & { { ( 7 \left. \right. } } \end{array}
$$

where ∗ denotes the convolution operation [35]. Note that the total received signal in (7) consists of three terms: (i) the first term represents the target echo appearing as a tone at a particular beat frequency, (ii) the second term corresponds to the interference appearing as a chirp in the baseband signal, and (iii) the third term η(t ) represents the additive white Gaussian noise. (7) also shows the dependency of interference on the starting frequencies and chirp slopes of the victim and interfering radar.

Furthermore, instantaneous beat frequency of the interference is obtained by taking the first derivative of phase in (5)

$$
\begin{array} { l c r } { { f _ { b , i n t } ( t ) = \displaystyle \frac { 1 } { 2 \pi } \frac { d } { d t } 2 \pi \left( ( f _ { m } - f _ { o } - \beta _ { m } \tau _ { m } ^ { \prime } ) t + \frac { 1 } { 2 } ( \beta _ { m } - \mu ) t ^ { 2 } \right) , } } \\ { { \displaystyle ~ = ( f _ { m } - f _ { o } - \beta _ { m } \tau _ { m } ^ { \prime } ) + ( \beta _ { m } - \mu ) t . } } \end{array}\tag{8}
$$

whereas, instantaneous beat frequency of the target signal is

$$
\begin{array} { l } { f _ { b } ( t ) = \displaystyle \frac { 1 } { 2 \pi } \frac { d } { d t } 2 \pi \left( - f _ { o } \tau _ { q } - \mu t \tau _ { q } + \frac { \mu \tau _ { q } ^ { 2 } } { 2 } \right) , } \\ { = - \mu \tau _ { q } . } \end{array}\tag{9}
$$

Note that in (8) the instantaneous beat frequency of the interference signal is time-varying whereas the beat frequencies corresponding to targets are constant. This time-varying characteristic of the interference signal motivates us to design a signal processing-based solution for interference mitigation involving time-frequency analysis. Our objective is to develop a method to alleviate the effect of interference terms as shown in (7), which will be elaborated in the following section.

## III. PROPOSED VAFER SCHEME

Our main objective is to effectively detect the existence of point target based on an FMCW radar by suppressing surrounding interference from interfering radars. In the following subsections, we will provide detailed explanation of the proposed VAFER algorithm, which consists of mode decomposition of interference-contaminated signal using VMD, time-frequency analysis with FSST, and energyentropy thresholding for signal reconstruction.

## A. VARIATIONAL MODE DECOMPOSITION (VMD)

To decompose the interference-contaminated noisy signal, we adopt an adaptive signal decomposition method, i.e., VMD [33], that decomposes a signal into K narrowband variational mode functions (VMFs). VMD is a signal processing tool to decompose a multi-frequency signal into modes known as VMFs where an individual VMF is a cosine function of a certain frequency and amplitude. In FMCW radar systems, the beat signal is complex-valued, comprising in-phase and quadrature components. However, the essential information related to target reflections and interference, particularly beat frequencies and energy content, is primarily captured in the real component. Since VMD is designed for real-valued signals, we apply it to $R e \{ \tilde { r } _ { b } ( t ) \}$ , which retains the key spectral features necessary for effective interference suppression without significant loss of performance.

Let $\{ u _ { k } \} : = \{ u _ { 1 } ( t ) , . . . , u _ { K } ( t ) \}$ and $\{ \omega _ { k } \} : = \{ \omega _ { 1 } , . . . , \omega _ { K } \}$ denote collections of K VMFs and their center frequencies, respectively. For each VMF $u _ { k }$ , VMD uses Hilbert transform to compute the associated analytic signal. Then, the estimated center frequency is used to shift the frequency spectrum of VMFs to the baseband, followed by applying Gaussian smoothing for bandwidth estimation. Thus, VMD decomposes a signal into its narrowband components by considering bandwidth as sparsity prior in the spectral domain, where bandwidth is estimated by the squared $\ell _ { 2 }$ norm of the gradient. The resulting constrained variational problem is stated as [33]

$$
\begin{array} { l } { \displaystyle \operatorname* { m i n } _ { \{ \omega _ { k } \} , \{ u _ { k } \} } \left\{ \sum _ { k = 1 } ^ { K } \bigg \| \partial _ { t } \left[ \left( \delta ( t ) + \frac { j } { \pi t } \right) * u _ { k } ( t ) \right] e ^ { - j \omega _ { k } t } \bigg \| _ { 2 } ^ { 2 } \right\} } \\ { \displaystyle \mathrm { s . t . } \quad \sum _ { k = 1 } ^ { K } u _ { k } ( t ) = \tilde { r } _ { b } ( t ) , } \end{array}\tag{10}
$$

where $\partial _ { t }$ denotes partial derivative with respect to t and $\delta ( \cdot )$ is the unit impulse function. In (10), VMD minimizes the bandwidth over the central frequency $\omega _ { k }$ for $k = 1 , 2 , \ldots , K$ of each VMF subject to the condition that the sum of all the VMFs must be equal to the original signal. The bandwidth of the $k ^ { \mathrm { t h } }$ mode is kept minimum around the center frequency $\omega _ { k }$ by employing Weiner filtering. The term $\begin{array} { r } { [ ( \delta ( t ) + \frac { j } { \pi t } ) * u _ { k } ( t ) ] } \end{array}$ denotes the analytic signal of mode $u _ { k }$ which is computed with the help of Hilbert transform (obtained by convolving a signal with $\textstyle { \frac { 1 } { \pi t } } )$ and it is applied on the VMF $u _ { k } ( t )$ . Further properties and detailed analysis of the Hilbert transform are described in [36]. The partial derivative ∂ keeps the bandwidth narrow and close to zero, and ${ { e } ^ { - j { \omega } _ { k } t } }$ ensures that the bandwidth of the VMF is centered around $\omega _ { k }$

In order to obtain the optimal solution to the constrained variational problem in (10), it is transformed into an unconstrained optimization problem using a quadratic penalty factor α and the Lagrange multiplier λ following [33] as

$$
\begin{array} { l } { { { \cal L } \left( \{ \omega _ { k } \} , \{ u _ { k } \} , \lambda \right) = } } \\ { { \displaystyle ~ \propto \sum _ { k = 1 } ^ { K } \left\| \partial _ { t } \left[ \left( \delta ( t ) + \frac { j } { \pi t } \right) * u _ { k } ( t ) \right] e ^ { - j \omega _ { k } t } \right\| _ { 2 } ^ { 2 } } } \\ { { \displaystyle ~ + ~ \left\| \tilde { r } _ { b } ( t ) - \sum _ { k = 1 } ^ { K } u _ { k } ( t ) \right\| _ { 2 } ^ { 2 } + \left. \lambda ( t ) , \tilde { r } _ { b } ( t ) - \sum _ { k = 1 } ^ { K } u _ { k } ( t ) \right. , } } \end{array}\tag{11}
$$

where the operator $\langle \cdot , \cdot \rangle$ denotes inner product. The optimization of (11) is carried out in the Fourier domain, and is solved via the alternating direction method of multipliers (ADMM) for iterative updates of VMFs in frequency domain and frequencies, i.e., $\bar { u } _ { k } ^ { n + 1 } ( \omega )$ and $\omega _ { k } ^ { n + 1 }$ , by adopting the convergence criterion $\begin{array} { r } { \sum _ { k } \| \tilde { \mu } _ { k } ^ { n + 1 } - \hat { \mu } _ { k } ^ { n } \| _ { 2 } ^ { 2 } / \| \hat { \mu } _ { k } ^ { n + 1 } \| _ { 2 } ^ { 2 } < \xi } \end{array}$ with convergence tolerance ξ, as [33]

$$
\hat { u } _ { k } ^ { n + 1 } ( \omega ) = \frac { \tilde { r } _ { b } ( \omega ) - \displaystyle \sum _ { i = 1 } ^ { k - 1 } \hat { u } _ { i } ^ { n + 1 } ( \omega ) - \displaystyle \sum _ { i = k + 1 } ^ { K } \hat { u } _ { i } ^ { n } ( \omega ) + \hat { \lambda } ( \omega ) / 2 } { 1 + 2 \alpha ( \omega - \omega _ { k } ^ { n } ) ^ { 2 } }\tag{12}
$$

$$
\omega _ { k } ^ { n + 1 } = \frac { \int _ { 0 } ^ { \infty } \omega \left| \hat { u } _ { k } ^ { n + 1 } ( \omega ) \right| ^ { 2 } d \omega } { \int _ { 0 } ^ { \infty } \left| \hat { u } _ { k } ^ { n + 1 } ( \omega ) \right| ^ { 2 } d \omega }\tag{13}
$$

where $( \cdot ) ^ { n + 1 }$ denotes the $( n + 1 ) ^ { \mathrm { t h } }$ iteration, $\tilde { r } _ { b } ( \omega )$ and $\hat { \lambda } ( \omega )$ represent the Fourier transforms of $\tilde { r } _ { b } ( t )$ and $\lambda ( t )$ , respectively, with ω indicating the frequency variable. VMFs $u _ { k }$ and their corresponding center frequencies $\omega _ { k }$ are initialized as 0, and the most recent VMFs and their corresponding center frequencies are utilized for the following updates.

With the designed VMD method, the signal of interest and interference signals are distributed in different VMFs. Because beat frequencies corresponding to targets are present as single-tone frequencies, target reflections are contained in a few VMFs as sinusoidal variations of constant frequency. In contrast, the interference appears as a chirp-like variation. Note that the choice of VMD in this work is due to its superior mode separation capabilities and robustness compared to other signal decomposition techniques such as empirical mode decomposition (EMD), ensemble EMD (EEMD), and wavelet-based methods. Unlike EMD-based approaches, which often suffer from mode mixing, sensitivity to noise, and lack of a clear mathematical foundation, VMD formulates signal decomposition as a constrained variational problem aimed at extracting modes with compact spectral support. This ensures stable and repeatable decomposition even under strong interference or low-SNR conditions. Moreover, VMD allows explicit control over the number of modes and their bandwidth, making it especially suitable for isolating chirplike interference components from desired target returns in FMCW radar systems.

VMD minimizes the bandwidth of each mode by solving a constrained optimization problem, mapping sinusoidal or single-tone components (such as beat frequencies in the FMCW radar) into distinct modes. Also, VMD avoids mode mixing and ensures spectral compactness through nonrecursive, concurrent mode extraction. These characteristics of VMD make it a suitable signal decomposition tool to decompose interference-contaminated FMCW radar beat signal, consisting of well-separated sinusoids and chirps [33], [37].

## 1) TUNING VMD PARAMETERS

In the VMD algorithm described above, the choice of the number of VMFs (K) influences the decomposition performance and optimization. To identify optimal number of VMFs, we first construct a Hankel matrix of the interference contaminated signal as

$$
\mathcal { H } ( \tilde { r } _ { b } ) = \left[ \begin{array} { c c c c } { x _ { 1 } } & { x _ { 2 } } & { \cdot \cdot \cdot } & { x _ { j } } \\ { x _ { 2 } } & { x _ { 3 } } & { \cdot \cdot \cdot } & { x _ { j + 1 } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { x _ { p } } & { x _ { p + 1 } } & { \cdot \cdot } & { x _ { J } } \end{array} \right] ,\tag{14}
$$

where J and $p$ denotes the total number of samples $( j =$ $J - p + 1 )$ and window length, respectively. Singular value decomposition (SVD) of $\dot { \mathbf { r } } = \mathcal { H } ( \tilde { r } _ { b } ) \mathcal { H } ( \tilde { r } _ { b } ) ^ { T }$ is computed as $\mathbf { \Psi } \mathbf { \tilde { { r } } } = \pmb { U } \mathbf { \tilde { { \Sigma } } } \mathbf { \pmb { V } } ^ { T }$ to obtain singular values  in the decreasing order. Since most of the signal energy is contained in the larger singular values, we consider top 50% singular values and compute their ratio as

$$
\varrho ( j ) = \frac { \pmb { \Sigma } ( j ) } { \pmb { \Sigma } ( j + 1 ) } .\tag{15}
$$

K is chosen as the index of the largest ( j). Apart from K, algorithm performance also depends on the choice of α, which controls the bandwidth of each VMF. Since the target’s beat frequency is a single tone frequency, larger α is desirable to achieve a narrower bandwidth for each VMF.

## B. TIME-FREQUENCY ANALYSIS WITH FSST

In this step, we propose to perform a time-frequency analysis of K VMFs using FSST. Note that we prefer FSST over the conventional time-frequency analysis tool STFT because FSST sharpens the time-frequency representation by shifting energy to the instantaneous frequency because of its reassignment capability [34]. This property is particularly crucial for FMCW radars, where target reflections appear as horizontal lines, and interference as chirps in the time-frequency spectrum. FSST sparsely represents VMFs that contain information about target reflections as a single frequency in the time-frequency representation. First of all, we calculate the STFT of the $\dot { k } ^ { \mathrm { { t h } } }$ VMF as

$$
V _ { u _ { k } } ^ { g } ( t , \omega ) = \int _ { \mathbb R } u _ { k } ( \tau ) g ^ { * } ( \tau - t ) e ^ { - j \omega \tau } d \tau ,\tag{16}
$$

where R is the set of real numbers and $g ^ { * } ( t )$ is the complex conjugate of g(t ) denoting the window function [34]. The FSST is obtained from frequency domain reassignment of the STFT to its spectrogram centroid $\hat { \omega } _ { u _ { k } } ( t , \omega )$ over each time instant t [38]. The centroid of STFT spectrogram is given by

$$
\hat { \omega } _ { u _ { k } } ( t , \omega ) = \omega - \Im \left\{ \frac { V _ { u _ { k } } ^ { g ^ { \prime } } ( t , \omega ) } { V _ { u _ { k } } ^ { g } ( t , \omega ) } \right\} ,\tag{17}
$$

where $V _ { u _ { k } } ^ { g ^ { \prime } } ( t , \omega )$ denotes the STFT of the $k ^ { \mathrm { t h } }$ VMF obtained with the derivative of $g ( t )$ , and 	 represents imaginary part of the argument [39]. Therefore, based on (17), the FSST of the $k ^ { \mathrm { t h } }$ VMF obtained after the reassignment of STFT is

$$
U _ { k } ( t , \omega ) = \frac { \int _ { \mathbb { R } } V _ { u _ { k } } ^ { g } ( t , z ) e ^ { j \omega t } \delta ( \omega - \hat { \omega } _ { u _ { k } } ( t , z ) ) d z } { 2 \pi g ^ { * } ( 0 ) } .\tag{18}
$$

Note that the modes acquired by VMD are transformed into time-frequency spectra by applying FSST scheme in (18). The property of FSST to emphasize sinusoid-like signals allows us to characterize single-tone beat frequencies corresponding to targets, i.e., frequency line parallel to the time axis; whereas interference appears as a noisy blob in the spectra. We will evaluate the effectiveness of the proposed FSST method in performance evaluation.

## C. ENERGY-ENTROPY THRESHOLDING AND RECONSTRUCTION

After obtaining the time-frequency spectrum for K VMFs, we propose to adopt the Wiener entropy to distinguish whether a particular mode contains information about target reflections or interference based on their specific characteristics. Note that Wiener entropy provides a measure of the spikiness of a vector [40]. We compute the Wiener entropy $W ( U _ { k } ( t , \omega ) )$ from the power spectrum of the FSST representation of each

VMF as

$$
W \left( U _ { k } ( t , \omega ) \right) = \frac { \left[ \underset { i = 1 } { N } \underset { j = 1 } { \overset { F } { \prod } } \ | U _ { k } ( t _ { i } , \omega _ { j } ) | ^ { 2 } \right] ^ { 1 / N F } } { \frac { 1 } { N F } \underset { i = 1 } { \overset { N } { \sum } } \underset { j = 1 } { \overset { F } { \sum } } | U _ { k } ( t _ { i } , \omega _ { j } ) | ^ { 2 } } ,\tag{19}
$$

where N and $F$ represent the number of time and frequency samples, respectively. This formulation yields a scalar Wiener entropy value for each mode, which captures the spectral flatness of the FSST power distribution. Note that target reflections appear as single-tone components in the FSST domain characterized by their lower amplitude but extended duration over time, which leads to higher Wiener entropy. In contrast, interference due to its chirp-like or multi-tone nature exhibits strong energy concentration in localized regions, resulting in lower entropy values.

We propose an energy-entropy-based threshold to identify and suppress interference-contaminated VMFs. Based on (19), the proposed threshold $T _ { \beta }$ is calculated as

$$
T _ { \beta } = \frac { \sum _ { k = 1 } ^ { K } E _ { k } \cdot W ( U _ { k } ( t , \omega ) ) } { \sum _ { k = 1 } ^ { K } E _ { k } } ,\tag{20}
$$

where $E _ { k }$ denotes the energy of the $k ^ { \mathrm { t h } }$ VMF computed as

$$
E _ { k } = \int _ { - \infty } ^ { \infty } \mid u _ { k } ( t ) \mid ^ { 2 } d t .\tag{21}
$$

The proposed energy-entropy threshold formulation acts as a weighted mean of spectral spikiness, enabling more precise mode selection without relying on hardcoded cut-offs. By weighting the Wiener entropy with the corresponding mode energy, the threshold reflects the concentration of signal energy in narrow frequency bands, making it suitable for detecting single-tone target signatures.

Finally, we reconstruct the interference-suppressed signal by choosing elements of the family of VMFs as

$$
\mathbb { V } = \left\{ U _ { k } ( t , \omega ) : W ( U _ { k } ( t , \omega ) ) \geq T _ { \beta } , \forall k \in \mathbb { K } \right\} ,\tag{22}
$$

where K is the index set containing the maximum number as K. (22) denotes the set V of $U _ { k } ( t , \omega )$ whose Wiener entropy passes the threshold $T _ { \beta }$ . As a result, the interferencesuppressed signal is reconstructed by taking the inverse FSST of these VMFs as

$$
\hat { r } _ { b } ( t ) = I F S S T \left( \sum _ { \mathbb { V } } U _ { k } ( t , \omega ) \right) .\tag{23}
$$

The complete algorithm of the proposed VAFER scheme is shown in Algorithm 1.

## IV. PERFORMANCE EVALUATION

In this section, we present both simulation and experimental results to validate the effectiveness of the proposed interference suppression method for mutual interference between FMCW radars. The results of the proposed VAFER method are compared with recently proposed state-of-the-art methods, i.e., the adaptive interference mitigation method called ANC [14], WD scheme [17], CS-based SPARKLE method [26], and CS-based $\mathrm { B i } { - } \ell _ { 1 }$ method [27]. In existing literature, interference in time-frequency spectra is detected via STFT [19], [23]. In order to show advantages of using FSST instead of STFT, we compare the proposed VAFER scheme against a variant of the VAFER scheme, referred to as VAFER-STFT, in which the time-frequency analysis is performed via STFT instead of FSST. The simulations and processing of experimental data are carried out in MATLAB, and experimental data have been taken from [14].

Algorithm 1: Proposed VAFER Algorithm.   
Input $: \tilde { r } _ { b } ( t ) :$ the interference contaminated signal   
1 Set $K , \alpha$   
2 Compute Hankel matrix using (14)   
3 Compute SVD $\Gamma = \pmb { U } \pmb { \Sigma V } ^ { T }$   
4 Compute number of VMFs (K) using (15)   
5 Initialize $\mu _ { k } ^ { 1 } , \omega _ { k } ^ { 1 } , \lambda , n = 0$   
6 Repeat $n \gets n + 1$   
7 for $k \in { 1 } : K$ do   
8 begin   
9 update $u _ { k }$   
$\tilde { r } _ { b } ( \omega ) - \sum _ { i = 1 } ^ { k - 1 } \hat { u } _ { i } ^ { n + 1 } ( \omega ) - \sum _ { i = k + 1 } ^ { K } \hat { u } _ { i } ^ { n } ( \omega ) + \hat { \lambda } ( \omega ) / 2$   
10 $\hat { u } _ { k } ^ { n + 1 } ( \omega ) \gets$ $\overline { { 1 + 2 \alpha ( \omega - \omega _ { k } ^ { n } ) ^ { 2 } } }$   
11 update $\omega _ { k }$   
12 $\begin{array} { r } { \omega _ { k } ^ { n + 1 }  \frac { \int _ { 0 } ^ { \infty } \omega | \hat { u } _ { k } ^ { n + 1 } ( \omega ) | ^ { 2 } d \omega } { \int _ { \mathbb { \Lambda } ^ { \infty } } ^ { \infty } | \hat { u } _ { \cdot } ^ { n + 1 } ( \omega ) | ^ { 2 } d \omega } } \end{array}$ for all $\omega \ge 0$   
$\overline { { \int _ { 0 } ^ { \infty } \left| \hat { u } _ { k } ^ { n + 1 } ( \omega ) \right| ^ { 2 } d \omega } }$   
13 update λ   
14 $\begin{array} { r } { \hat { \lambda } ^ { n + 1 } ( \omega ) \gets \hat { \lambda } ^ { n } ( \omega ) + \tau \left( \tilde { r } _ { b } ( \omega ) - \sum _ { k } \hat { u } ^ { n + 1 } ( \omega ) \right) } \end{array}$   
15 repeat until $\begin{array} { r } { \sum _ { k } \| \hat { \mu } _ { k } ^ { n + 1 } - \hat { \mu } _ { k } ^ { n } \| _ { 2 } ^ { 2 } / \| \overline { { \hat { \mu } _ { k } ^ { n + 1 } } } \| _ { 2 } ^ { 2 } < \xi } \end{array}$   
16 end   
17 Compute time-frequency spectra $U _ { k } ( t , \omega )$   
using (16), (17), and (18)   
18 Calculate wiener entropy W $( U _ { k } ( t , \omega ) )$   
1/NF   
19 $ W \left( U _ { k } ( t , \omega ) \right) = \frac { \left[ \prod _ { i = 1 } ^ { N } \prod _ { j = 1 } ^ { F } | U _ { k } ( t _ { i } , \omega _ { j } ) | ^ { 2 } \right] } { N ~ F }$   
NF $\sum _ { i = 1 } ^ { N } \sum _ { j = 1 } ^ { F } | U _ { k } ( t _ { i } , \omega _ { j } ) | ^ { 2 }$   
20 Calculate energy-entropy threshold $T _ { \beta }$   
21 $\begin{array} { r } { T _ { \beta } = \frac { \sum _ { k = 1 } ^ { K } E _ { k } \cdot W \left( U _ { k } ( t , \omega ) \right) } { \sum _ { \mathbf { \beta } } ^ { K } { \mathbf { \beta } } _ { { \cal { F } } : \mathbf { \beta } } } } \end{array}$   
$\overline { { \sum _ { k = 1 } ^ { K } E _ { k } } }$   
22 for $k \in { 1 } : K$ do   
23 begin   
24 if W $( U _ { k } ( t , \omega ) ) \ge T _ { \beta }$   
25 then $\mathbb { V }  \{ U _ { k } ( t , \omega ) \}$   
26 else discard VMF ;   
27 end   
28 Signal reconstruction via inverse FSST   
29 $\begin{array} { r } { \hat { r } _ { b } ( t ) = I F S S T \left( \sum _ { \mathbb { V } } U _ { k } ( t , \omega ) \right) } \end{array}$   
Output: ${ \hat { r } } _ { b } ( t ) \colon$ reconstructed interference-suppressed   
signal

## A. PERFORMANCE METRICS

We evaluate and compare the performance of the proposed VAFER scheme with other methods quantitatively in terms of

TABLE 1. Simulation Parameters
<table><tr><td>Parameter</td><td>Victim radar</td></tr><tr><td>Carrier frequency  $f _ { o }$ </td><td>77 GHz</td></tr><tr><td>Bandwidth B</td><td>540 MHz</td></tr><tr><td>Chirp duration  $T$ </td><td>45  $\mu \mathrm { s }$ </td></tr><tr><td>Sampling frequency  $f _ { s }$ </td><td>22 MHz</td></tr><tr><td>Maximum beat frequency  $f _ { b , m a x }$ </td><td>10 MHz</td></tr><tr><td>Number of chirps</td><td>64</td></tr></table>

SINR and correlation coefficient $\rho$ . The SINR of interferencecontaminated received signal is defined as

$$
S I N R _ { I } = 2 0 \log _ { 1 0 } \frac { \| s _ { r } \| _ { 2 } } { \| s _ { i n t } + \eta \| _ { 2 } } ,\tag{24}
$$

where $s _ { r }$ is the reference signal from (2), $s _ { i n t }$ is the interference signal from (4), and $\eta$ represents noise. The SINR of reconstructed signal after interference suppression is given by

$$
S I N R _ { O } = 2 0 \log _ { 1 0 } \frac { \| s _ { r } \| _ { 2 } } { \| s _ { r } - \hat { r } _ { b } \| _ { 2 } } ,\tag{25}
$$

where $\hat { r } _ { b }$ is the reconstructed interference-suppressed signal from (6). In (25), the denominator $\lVert s _ { r } - \hat { r } _ { b } \rVert _ { 2 }$ represents the error between interference-free signal and the reconstructed signal. Hence, a lower value of error leads to higher $S I N R _ { O } \mathrm { . }$ characterizing better interference suppression. Furthermore, the correlation coefficient between the interference-free signal and the reconstructed signal is defined as

$$
\rho = \frac { { s _ { r } } ^ { H } { \hat { r } _ { b } } } { \| s _ { r } \| _ { 2 } \cdot \| \hat { r } _ { b } \| _ { 2 } } ,\tag{26}
$$

where the correlation coefficient $\rho \in [ 0 , 1 ]$ and $( \cdot ) ^ { H }$ denotes conjugate transpose. A higher $\rho$ indicates a higher correlation between the reference signal $s _ { r }$ and reconstructed signal $\hat { r } _ { b }$

## B. SIMULATION RESULTS

## 1) SIMULATION SETUP

In simulations, we have considered Q = 4 point targets in the field of view (FOV) of the victim radar at the ranges $R = [ 1 0 , 1 6 , 3 0 , 5 0 ]$ m. The parameters of radar used in simulations are shown in Table 1. Note that the maximum beat frequency $f _ { b , \mathrm { m a x } }$ is the cutoff frequency of the LPF. The reflected signal received at the victim radar experiences interference from $M = 2$ interfering radars transmitting chirp signals with starting frequency $f _ { m } = 7 7$ GHz $( m = 1 , 2 )$ and chirp slopes $\beta _ { 1 } = 2 ~ \mu$ and $\beta _ { 2 } = - 2 ~ \mu$ , where $\begin{array} { r } { \mu = { \frac { B } { T } } } \end{array}$ is the slope of the victim radar. STFT and FSST are configured with a Hanning window of length 256. Fig. 2 shows the beat signals of four point targets without (left-column plots) and with (right-column plots) interference, along with their corresponding time-frequency (t-f) domain spectra and range discrete Fourier transform (DFT). Fig. 2(b) illustrates that 80% of the entire signal time sequence is specified to be contaminated with interference. Fig. 2(f) shows that target 4 present at 50 m distance is buried under interference, and the interference has a chirp-like nature, as shown in Fig. 2(d).

![](images/8764ad6e7ae4797e4eb649b233f29cb7ed73466b2a9ef86eb84164942967a9ba.jpg)  
(a)

![](images/345475d6d099d7bb6f058c3c349f50f4a061805af90bb016dff5f4915b98ded3.jpg)  
(b)

![](images/85878b2349a4b3155a976841b940e08efe6c9e2e6cf88583ea03d65481c9517b.jpg)  
(c)

![](images/dd0f50e3423fdaea05b5cdcb26f85b68046fc7e9954115c586bfec419a002d36.jpg)  
(d)

![](images/8d9652328e7c9ffe2f24642cbb26ceb96c8e733e0b192cb94e5e7f0251395da7.jpg)  
(e)

![](images/a2b2bebafd83912624131ea02e4d3001b4822fe65ab6bd88f080bd209ef3a0dc.jpg)  
(f)  
FIG. 2. Illustration of (a) Beat signal of targets, (b) Interference corrupted beat signal, (c) t-f spectra of pure beat signal, (d) t-f spectra of interference-corrupted beat signal, (e) Range DFT of target-only signal, and (f) Range DFT of interference-corrupted beat signal.

With such strong interference, the interference-contaminated received signal has an $S I N R _ { I }$ of −1.1047 dB in simulations. The four point targets appear as horizontal lines, each representing a single-tone frequency as shown in Fig. 2(c) and (d) in the time-frequency spectra. Note that the target with the lowest frequency possesses the largest signal magnitudes illustrated with yellow color. Furthermore, Fig. 2(e) and (f) show the four peaks in range DFT of the received radar data indicating the four point targets.

## 2) SIMULATION RESULTS OF PROPOSED VAFER METHOD

In the proposed VAFER method, we start with decomposing time domain interference-contaminated received signal by applying the proposed VMD algorithm. For mode selection, the Hankel matrix was formed with $J = 9 9 0$ samples $( T = 4 5 \ \mu \mathrm { s }$ $f _ { s } = 2 2$ MHz) and window length $\begin{array} { r } { p = \lfloor \frac { J } { 3 } \rfloor = 3 3 0 } \end{array}$ , with the estimated number of modes $K = 8$ . The VMD penalty parameter $\alpha = 2 0 0 0$ controls the smoothness of the decomposed modes, providing a trade-off between resolution and noise suppression. The effectiveness of VMD scheme can be seen in Fig. 3 where the VMFs with sinusoid-like variations (mode-1, mode-2, mode-7, and mode-8) represent beat frequencies corresponding to 4 targets; while the remaining 4 modes (mode-3, mode-4, mode-5, and mode-6) show interference contaminating the target signal. As observed from the topmost plot of Fig. 3, mode-1 possesses the lowest beat frequency with the largest magnitude, which reflects the largest signal magnitudes in Fig. 2(c) and (d) with yellow color.

Subsequently, the obtained t-f spectra are shown in Fig. 4 by applying FSST on the VMFs. As seen in the top-two and bottom-two subplots of Fig. 4 representing the t-f spectra of mode-1, mode-2, mode-7, and mode-8 in Fig. 3, each subplot contains a horizontal line parallel to the time axis. The reason is that the proposed FSST sparsely represents VMFs that contain information about target reflections as a single-tone beat frequency in the t-f representation. On the other hand, remaining four subplots show the t-f spectra of the remaining 4 VMFs, which reveal high-power noise representing interference that can be separated from the original interference-contaminated signal using the proposed VMD algorithm.

Thus, in order to identify the four correct modes from the VMD result in Fig. 4, the energy of VMFs and Wiener entropy of time-frequency spectra of VMFs is calculated using (20), which results in a threshold of $T _ { \beta } = 0 . 9 6 8 1$ for the considered scenario. With the proposed method, interference-contaminated modes are discarded using the computed energy-entropy-based threshold, and interference suppressed signal is reconstructed using the remaining modes. Fig. 5 shows the t-f spectrum of reconstructed signal obtained after applying the proposed interference suppression method on the interference-contaminated signal shown in Fig. 2(d). Fig. 5 demonstrates that interference shown within the box in Fig. 2(d) is well suppressed by the proposed VAFER method, and the reconstructed t-f spectrum contains only beat frequencies corresponding to the four point targets. Finally, we take inverse FSST of the t-f spectra (shown in Fig. 5 for the VAFER method) to recover the corresponding beat signals.

![](images/06a0fbc98e49e83293fbed29df72f33f2d577ad4176d6c5a5abe9f43e3f10053.jpg)  
FIG. 3. VMFs of the received signal containing interference.

To further evaluate and validate the robustness of the proposed method, we simulate a more challenging scenario with $Q = 5$ targets positioned at ranges $R = [ 1 0 , 2 1 , 3 0 , 3 8 , 5 0 ] \mathrm { m }$ and $M = 2$ interfering radars with chirp slopes $\beta _ { 1 } = 2 ~ \mu$ and $\beta _ { 2 } = - 3 . 5 ~ \mu$ . The interferers are randomly located within the maximum detection range of the victim radar, resulting in varying time delays and increased spectral overlap as shown in Fig. 6(a) and (b). Under this setting, the interferencecontaminated signal exhibits a low input SINR of $S I N R _ { I }$ of −6.7267 dB in simulations. The results in Fig. 6(c) and (d) show that after applying the proposed VAFER method, the interference is effectively mitigated and all the five peaks are accurately detected, achieving an output SINR of $S I N R _ { O } =$ 5.9209 dB and $\rho = 0 . 9 7 3 9$ . These results demonstrate the robustness and effectiveness of the VAFER method under challenging conditions.

## 3) RECONSTRUCTED INTERFERENCE-SUPPRESSED SIGNAL COMPARISON

Fig. 7 shows the range DFT of the reconstructed signal obtained after applying different interference suppression methods on the interference-contaminated signal in Fig. 2.

![](images/b2091f10f6db232722cbb488dcd136538f03c5c2221d0ea2ff1bf9855c87740b.jpg)

![](images/94ab83589832c611cefad9d73e7fe64e26c4171d46b8772c29a521aed57a1daf.jpg)

![](images/343b8219e78fc04690bec05db2a8146535ca2c9e9d58416e3dd68455cbd78c0c.jpg)

![](images/2e1bfef35a877c3987fe823d773df71705e8e9e7f5c216fee315dd960f14dca0.jpg)

![](images/32688f7fff1f44028be18c8b2587cc9adbddce0eefaa0a58786d4ac954d73f68.jpg)

![](images/56685a57c1f2b714d8d8301bbe751fc7a19c01beb6d13f46d4e0e0a8c64cf873.jpg)

![](images/dbab8bb3055cb5b890ef07b41735c8548050b4de0b6648c979e093424c3a5c43.jpg)

![](images/a06dd3023e5076c6be5793d3dc07d6d1fd05d9a9d73fbb105a5a0596db3cdf7e.jpg)  
FIG. 4. Time-frequency spectra obtained by applying FSST to 8 separated modes after adopting VMD on the interference-contaminated received signal.

![](images/7b4a17d5a385654fb8016a04e3aaa2b4ea64d8eeec9aa16e8833ea90c31292f2.jpg)  
FIG. 5. Reconstructed interference-suppressed time-frequency spectrum using the proposed VAFER method.

Due to interference, it can be observed in Fig. 2(f) that the noise floor has increased to raise the challenge of detecting the correct target range. The results in Fig. 7 show that after applying the proposed VAFER method noise floor has been reduced significantly around the target peak at 50 m. It can be seen that the proposed VAFER scheme detects the four peaks accurately with a reduction in noise floor as well. Residual interference is observed in the range DFT plot of SPARKLE and $\mathrm { B i } { - } \ell _ { 1 }$ around the peak of the target located at 50 m. On the other hand, the performance of the ANC method is poor due to the assumption in [14] about the beat frequency occupying only the positive half of the spectrum, and interference in the negative half of the spectrum is conjugate symmetric to the positive spectrum. Significant residual interference is observed in the reconstructed interference-suppressed signal via the VAFER-STFT method due to the improper selection of modes by energy-entropy threshold. Also, benefiting from the property of FSST to focus more on sinusoid-like beat signals [34], the performance of VAFER is superior to the VAFER-STFT as shown in Fig. 7.

![](images/c56b9be364cb4d04cf53544099c95efdbe6ff62d2212521f2025e6c8be631418.jpg)

![](images/6f0d029955a69bb4db249912abecac74f8a3f8fbaf03cc65960a1d13e60247c4.jpg)

![](images/2babc7ac296f7afa8eb2a9124a111abfe8c269492b93d2c6c706ca94fd23f7d2.jpg)

![](images/5d692570eb8838fffb82a56859bced3f06286395ec5116e9c37a87223e9fecb1.jpg)  
FIG. 6. Interference mitigation performance of the proposed VAFER method for a challenging scenario with Q 5 targets and M 2 interfering radars (a), (b) range DFT and time frequency spectra of interference-contaminated signal, (c), (d) range DFT and time-frequency spectra of interference suppressed signal.

![](images/947dc7a48719b613b91f0165b3d1b54c5eff7800436cb78e6d928438bac98c16.jpg)

![](images/f8606bbab3ac5b0a1247c225498bbb6d2991b3b3f8e55df9b00486dfd048f3a2.jpg)

![](images/e6c7b76ad03a2151ae61b8dba7923b2f511d66d27175751f87a9898eabc8e5ef.jpg)

![](images/e7036a821489191c830180adf1e22f332d6001d563fc7abe698b3695c3ca08b3.jpg)

![](images/b962e61cbe6d90ba6ff54b29ae34f8de92722a8252ee2829a141901da807d3f2.jpg)

![](images/1c984d1d6f1e8a94f960b1221170bfd9de99542575fbd6eacb6136aabb903162.jpg)  
FIG. 7. Performance comparison of range DFT plots using SPARKLE [26], ANC [14], VAFER-STFT, WD [17], the proposed VAFER scheme, and Bi- [27] for reconstructed interference-suppressed signals.

To study the effect of interference on targets in the range-Doppler domain, in simulations, we consider $Q = 4$ point targets in the field of view (FOV) of victim radar at the ranges $R = [ 1 0 , 1 6 , 3 0 , 5 0 ]$ m with velocities $V =$ $[ 1 0 , 5 , - 5 , 0 ]$ m/s. Note that, three moving targets and one stationary target are considered for simulation. Fig. 8 shows range-Doppler map plotted as amplitude (in dB) versus range and speed in the absence and in the presence of interference. It is seen that the target present at 50 m is affected by interference and cannot be identified clearly. Fig. 9 shows a comparison of range-Doppler maps generated after interference suppression using SPARKLE, ANC, VAFER-STFT, WD, $\mathrm { B i } { - } \ell _ { 1 }$ , and the proposed VAFER scheme. It is seen that the $\mathrm { A N C }$ method fails to suppress the interference, resulting in the targets becoming unobservable in the range-Doppler map. The results of SPARKLE, $\mathrm { B i } { - } \ell _ { 1 }$ , and WD show residual interference in the range-Doppler maps, and with these schemes’ target present at 50 m is buried under the interference. The proposed VAFER scheme effectively reduces interference, and all four targets are clearly identified in the range-Doppler map shown in Fig. 9.

![](images/6659faf575026210c634a9e65ccd50183e08a8188873df89d40d21222c49a95c.jpg)

![](images/4f87a6f20faa5c13bd0a334583dc5c6446eb675af4b92c5ffe8dc18edcdd3c48.jpg)  
FIG. 8. Range-Doppler map (a) in the absence of interference, (b) in the presence of interference.

TABLE 2. Comparison of SINR and Correlation Coefficient of the Reconstructed Signals, and CPU Time Using SPARKLE, ANC, WD, VAFER-STFT, and Proposed VAFER Scheme
<table><tr><td>Method</td><td> $S I N R _ { o } \ ( \mathrm { { d B } ) }$ </td><td>Correlation coefficient (ρ)</td><td>CPU time (s)</td></tr><tr><td>SPARKLE</td><td>3.0170</td><td>0.7272</td><td>1.61</td></tr><tr><td>ANC</td><td>-8.3798</td><td>0.0014</td><td>0.02</td></tr><tr><td>WD</td><td>-1.1328</td><td>0.6509</td><td>0.29</td></tr><tr><td>VAFER-STFT</td><td>1.5186</td><td>0.7317</td><td>1.65</td></tr><tr><td> $\mathrm { B i } { - } \ell _ { 1 }$ </td><td>1.8436</td><td>0.7012</td><td>4.52</td></tr><tr><td>VAFER</td><td>14.3621</td><td>0.9818</td><td>0.72</td></tr></table>

Furthermore, we evaluate $S I N R _ { O }$ using (25) and correlation coefficient $\rho$ using (26) for the reconstructed signals with the same settings as in Section IV-B1. The corresponding results are shown in Table 2. Compared to the SPARKLE, ANC, WD, $\mathrm { B i } { - } \ell _ { 1 }$ and VAFER-STFT methods, it can be clearly observed that the proposed VAFER algorithm results in the highest $S I N R _ { O } = 1 4 . 3 6 2 1$ dB and $\rho = 0 . 9 8 1 8$ demonstrating superior interference suppression capability. The VAFER scheme significantly improves the reconstructed signal’s SINR by 15.46 dB based on the original interferencecontaminated received signal with $S I N R _ { I } = - 1 . 1 0 4 7$ dB. It is seen that the proposed VAFER scheme outperforms VAFER-STFT. The main reason for the poor performance of VAFER-STFT is that the energy-entropy threshold fails to discard some of the modes containing interference in VAFER-STFT, leading to lower $S I N R _ { O }$ and $\rho$ values. These results validate that our proposed VAFER method can suppress interference and improve signal quality compared to existing methods.

![](images/dde3dcd61f4d03e52cbdab6e23539f9100b50d95f9257a478523b0391eff1ba5.jpg)  
(a)

![](images/df6109c5492c098b4ec6201a4b2a022b40f51542e649a20eab12a38dfcedfd64.jpg)

![](images/067fe07bfd109e9353ecc7c5237152b09477bc9b73e60be28c5b9aa677230e88.jpg)  
Range (m)  
Speed (m/s)  
(b)

Range (m)  
(c)  
![](images/8d93206b2aa437570bc252476061a825f4f3adf6ae903f1d8616369904d90111.jpg)

![](images/18e8f8e2c0e7aea57633af2db0b9d3ae0e94e0e423f74a4bb40cdea61e02d150.jpg)  
(e)

Range (m)  
(d)  
![](images/806747f53fc2fb103ebc2a657d089c8bc1a1ba7a261588ab8f0ae9f4759ad5c3.jpg)  
(f)  
FIG. 9. Range-Doppler map after interference suppression using (a) SPARKLE, (b) ANC, (c) STFT-VAFER, (d) wavelet denoising (WD), (e) proposed VAFER scheme, and (f) Bi- method.

## 4) EFFECT OF SNR

We examine the effect of signal-to-noise ratio (SNR) on interference suppression performance by varying the AWGN noise level for the proposed VAFER method. We consider $Q = 3$ targets located at $R = [ 2 0 , 4 0 , 7 0 ]$ m and perform 300 Monte Carlo runs at each SNR varying from −20 dB to 10 dB. The radar is simulated following the parameters in Table 1. The results in terms of $S I N R _ { O }$ using (25) for the reconstructed signal are shown in Fig. 10(a). The bar chart in Fig. 10(b) shows the correlation coefficient $\rho$ as the SNR is varied from −20 dB to 10dB. We observe from Fig. 10 that both output SINR and correlation coefficient increase with SNR of the input signal for all schemes except ANC. Compared to the other methods, the proposed VAFER method achieves the highest output SINR and correlation coefficient for different SNR of the input signal.

## 5) PERFORMANCE EVALUATION FOR VARYING INTERFERENCE DURATION

We evaluate the performance of VAFER algorithm by varying the percentage of interference-contaminated samples in the simulated signal using the same setting as in Section IV-B1. We vary the percentage of interference-contaminated samples from 10% to 70% at constant $S I N R _ { I }$ of 9.1814 dB and compute the resulting $S I N R _ { O }$ and $\rho .$ Performance comparison is shown in Fig. 11(a) and (b) where we show output SINR and correlation coefficient $\rho ,$ respectively, as a function of the percentage of received signal that is contaminated by interference. It can be observed in Fig. 11(a) that $S I N R _ { O }$ for ANC method is almost constant and is the lowest compared to the other schemes. On the other hand, Fig. 11(b) shows that the correlation coefficient for SPARKLE, VAFER-STFT, and proposed VAFER method are almost similar, whereas for $\mathrm { B i } { - } \ell _ { 1 } , \rho$ is almost constant and lower than the proposed VAFER method and the ANC scheme results in the least $\rho$ value. It can be seen from Fig. 11 that the proposed VAFER scheme achieves the highest $S I N R _ { O }$ and $\rho .$

Furthermore, in Fig. 11 we observe that the performance of VAFER-STFT is poor compared to the VAFER scheme. In the proposed VAFER scheme, the energy-entropy threshold perfectly identifies and discards modes corresponding to interference in the t-f spectrum generated by FSST whereas, the energy-entropy threshold fails to discard some of the modes containing interference in VAFER-STFT, leading to lower $S I N R _ { O }$ and $\rho$ values. Here we also observe that as the number of interference-contaminated samples in the signal increases, $S I N R _ { O }$ and $\rho$ decrease slightly due to presence of some residual interference in the VMD modes corresponding to targets in the proposed VAFER method. Similar behavior is observed in Fig. 7 where residual interference due to improper selection of modes in the reconstructed interferencesuppressed signal via the VAFER-STFT method leads to poor performance of VAFER-STFT compared to the VAFER scheme. On the other hand, the assumption of interference in the negative half of spectrum being conjugate symmetric of the positive spectrum for ANC leads to a slight increase in $\rho$

![](images/b47d8e059b6af93b09e3d9b8ce3b136a63cdb7ddecf57a1d51e0be337d923aed.jpg)  
(a)

![](images/883100f494b6dfe4a66fdc99ae1dc27a67fce8fd01ae1305648e887c94cc536e.jpg)  
(b)  
FIG. 10. Quantitative analysis of interference suppression performance of the SPARKLE, ANC, WD, VAFER-STFT, the proposed VAFER method, and $\bar { \mathbf { B i } } \mathbf { - } \boldsymbol { \ell } _ { 1 }$ method as a function of input SNR. (a) SINR , and (b) correlation coefficient $\rho _ { \pmb { \mathscr { r } } }$ of the reconstructed interference-suppressed signal.

## 6) PROBABILITY OF DETECTION

To evaluate the performance of the proposed VAFER algorithm, the probability of detection as a function of SNR at a false alarm rate of $1 0 ^ { - 5 }$ is shown in Fig. 12. In this simulation, the probability of detection is computed for the target located at 50 m which is most affected by the interference. SNR is varied from −20 dB to 10 dB and 300 Monte Carlo simulations are performed to compute the probability of detection. It is seen in Fig. 12 that the proposed VAFER scheme stands out and offers superior performance compared to SPARKLE, ANC, WD, $\mathrm { B i } { - } \ell _ { 1 }$ and VAFER-STFT. Notice that while the output SINR for the WD method improves with increasing input SNR in Fig. 10, the corresponding detection probability in

![](images/3b8a64309ea57e49c6c704c0d6bf94e4d573cbfc35f14638a272f30da55dd162.jpg)  
(a)

![](images/217594820c30e8873f89174ea619a205ac7a6b45a5bc7e264c10f7bd2b477ff1.jpg)  
(b)

FIG. 11. Quantitative analysis of the interference suppression performance of the SPARKLE, ANC, VAFER-STFT, WD, Bi- , and the proposed VAFER method at different percentages of interference duration. (a) Output SINR, and (b) correlation coefficient $\rho$ of the reconstructed interference-suppressed signal.  
![](images/ea05e35851f7cec504c745969bd8d33d3f02d3a9b62aec6bf2a516f5425e340a.jpg)  
FIG. 12. Probability of detection versus SNR at false alarm rate of 10−<sup>5</sup>.

Fig. 12 does not follow a strictly monotonic trend. This is due to residual spectral broadening and peak distortion introduced by WD, which affect the consistency of peak-based detection even when overall interference is suppressed. In particular, the target’s peak amplitude may fall below the detection threshold despite improved SINR.

## C. COMPUTATIONAL COMPLEXITY ANALYSIS

The computational complexity of the proposed scheme depends on the computations required for K VMFs, FSST, and inverse FSST. Assuming I is the number of ADMM iterations required to solve the unconstrained VMD optimization, the computational complexity of the VMD step is (IK(J log J )) where J is the number of signal samples. The computational complexity of FSST, which is applied to each VMF for timefrequency analysis, is (KJ log J ), and the time complexity of the energy-entropy thresholding step is (KJ ). Hence, the overall computational complexity of the proposed VAFER scheme is (IK(J log J )). Additionally, for mode selection, a Hankel matrix $\mathcal { H } ( \tilde { r } _ { b } ) \in \mathbb { R } ^ { p \times j }$ is first constructed from the interference-corrupted signal. The cost of computing the matrix product $\Gamma = \mathcal { H } \mathcal { H } ^ { T } \in \mathbb { R } ^ { p \times p }$ is $\mathcal { O } ( p ^ { 2 } J )$ , followed by SVD of , which adds $\mathcal { O } ( p ^ { 3 } )$ complexity. Hence, the total computational complexity of the VAFER scheme with mode adaptivity is $\mathcal { O } ( I K ( J \log J ) )$ , along with a one-time preprocessing cost of $\mathcal { O } ( p ^ { 2 } J + p ^ { 3 } )$ for determining the number of VMFs.

The computational complexity of ANC is determined by the computation of the Fourier transform, inverse Fourier transform, and updates of adaptive filter coefficients, due to which it is computationally less intensive with overall computational complexity of (J log J). The WD method performs interference mitigation by applying a 3-level Haar wavelet with hard thresholding, which is also computationally less expensive than the proposed scheme with computational complexity of (J). The SPARKLE method employs the decomposition of the Hankel matrix and iterative optimization of Vandermonde matrices, resulting in time complexity of $\mathcal { O } ( m n ( 4 p + 5 ) + 2 ( m + n + 1 ) p ^ { 2 } + \bar { 2 } p ^ { 3 } )$ for one iteration, where m × n is size of Hankel matrix and $p$ is maximum rank of the SVD of Hankel matrix. In general, the proposed VAFER scheme and the SPARKLE scheme have similar computational complexity. The total computational complexity of the $\mathrm { B i } { - } \ell _ { 1 }$ method is given by $\mathcal { O } ( \Lambda \cdot ( J S + S ^ { 2 } ) )$ , where  denotes the number of sparse recovery iterations and S is the number of atoms in the dictionary. For quantitative comparison, the average CPU time of the different methods is listed in Table 2. All methods were implemented with MATLAB and on a PC with an Apple M1 processor and 8 GB RAM. It is seen that the ANC is the most computationally efficient method, and the proposed VAFER scheme is faster than SPARKLE and VAFER-STFT but slower than the WD scheme. To achieve real-time processing using the VAFER scheme, FSST is computed in parallel for all obtained VMFs using the MATLAB parallel computing toolbox, which improves the computational efficiency by approximately 40%, i.e., from 1.28 s to 0.72 s.

It is seen that using VMD followed by time-frequency transformation increases the computational complexity. However, the proposed VAFER scheme achieves the highest improvement in SINR as shown in Table 2 and a higher probability of detection across SNRs as shown in Fig. 12.

## D. EXPERIMENTAL RESULTS

The experimental radar data and radar parameters for this section have been taken from the recent work by Jin and Cao in [14].<sup>1</sup> The experimental setup used in [14] is shown in Fig. 13.

![](images/80c959d044ae79bd0b5f235f88cc4cbfab4c28cb15dff8a782387245e9560c18.jpg)

FIG. 13. Experimental setup used in [14]. TABLE 3. Experimental Parameters
<table><tr><td>Radar type</td><td>Parameter</td><td>Value</td></tr><tr><td rowspan="4">Victim radar</td><td>Carrier frequency  $f _ { o }$ </td><td>77 GHz</td></tr><tr><td>Bandwidth B</td><td>750 MHz</td></tr><tr><td>Chirp duration  $T$ </td><td>29.56  $\mu \mathrm { s }$ </td></tr><tr><td>Sampling frequency  $f _ { s }$ </td><td>20 Msps</td></tr><tr><td rowspan="4">Interfering radar</td><td>Carrier frequency  $f _ { m }$ </td><td>77 GHz</td></tr><tr><td>Bandwidth  $B _ { i n t }$ </td><td>682 MHz</td></tr><tr><td>Chirp duration  $T _ { i n t }$ </td><td>72.31 µs</td></tr><tr><td>Sampling frequency  $f _ { s , i n t }$ </td><td>15 Msps</td></tr></table>

In their experimental setup, interference-contaminated data is obtained by considering a car traveling with a speed of 15 m/s towards the victim FMCW radar operating at 77 GHz while experiencing interference from another FMCW radar operating at the same 77 GHz ad at a distance of 2 m from the victim radar. The experimental parameters are listed in Table 3. The performance of the proposed VAFER scheme is evaluated using simulations as well as experimentally. In the simulation setup, we have considered 4 point targets assuming sparsity whereas, in the experimental setup, the target is a moving car violating the sparsity assumption. For mode selection, the Hankel matrix was formed with $J = 5 9 1$ samples $( T = 2 9 . 5 6 \mu \mathrm { s } , f _ { s } = 2 0 $ MHz) and window length $p =$ $\lfloor \frac { J } { 3 } \rfloor = 1 9 7$ , with the estimated number of modes $K = 4$ . For real-world experimental analysis, the penalty factor $\alpha = 2 0 0 0$ is retained to maintain consistency and ensure stable mode decomposition across recorded signals.

The interference-contaminated time domain signal and range profiles are shown in Fig. 14(a) and (b), respectively, where the interference is visible as high fluctuating peaks from 3 μs to $6 ~ \mu \mathrm { s }$ in Fig. 14(a). Notice that the target is located at 14.8 m which is not clearly revealed in Fig. 14(b). For this study, we have compared the proposed VAFER scheme with ANC, SPARKLE, WD, VAFER-STFT, and $\mathrm { B i } { - } \ell _ { 1 }$ methods. Fig. 15 shows the results of time domain reconstructed interference-suppressed signals shown as the linear amplitude of received signal versus time, and the range profiles obtained by performing DFT on fast-time shown as DFT amplitude (in dB) versus range in Fig. 16. The results of the ANC scheme are shown in Figs. 15(a) and 16(a), which still indicate the presence of some interference, and a number of additional peaks are detected in the range profile, showing false or ghost targets. The interference suppression results for the SPARKLE algorithm are shown in Figs. 15(b) and 16(b). Results show that although the SPARKLE method performs well in suppressing the interference in time domain, still the range profile shows the presence of false targets. In the range profiles obtained by ANC, SPARKLE, and $\mathrm { B i } { - } \ell _ { 1 }$ in Fig. 16(a), (b), and (e), respectively, it can be observed that they also detect the presence of interfering radar at 2 m as an additional target which limits their performance and reduces the output SINR. Results corresponding to the WD method are shown in Figs. 15(c) and 16(c). Although the performance of the WD method is better than ANC, the smallest peak amplitude of the target is observed with the WD method, which is attributed to signal distortion and energy leakage inherent in wavelet decomposition, rather than residual interference. Moreover, the results in Figs. 15(d) and 16(d) show that the VAFER-STFT method is ineffective in suppressing interference, resulting in excessive time domain peaks. The results of the $\mathrm { B i } { - } \ell _ { 1 }$ method in Figs. 15(e) and 16(e) show the presence of residual interference and a number of additional peaks in the range profile. Figs. 15(f) and 16(f) illustrate the ability of the proposed VAFER method for interference suppression. Specifically, Fig. 15(f) shows that the peak fluctuations caused by interfering radar are significantly suppressed and only a single peak is observed in Fig. 16(f) corresponding to the actual target located at 14.8 m.

![](images/9020ab01b42a17c4a66b96fa0deff95c9eb8bbb24bd5beccf1e18e2a7e806a7a.jpg)  
(a)

![](images/d4257bb26740b14f53d960414ec0dd816834980e94c8e042dad5c91d3368a40c.jpg)  
(b)

FIG. 14. Illustration of (a) Time-domain interference-contaminated signal, and (b) Range profile of interference-contaminated signal.  
![](images/f6d9ba66d2131a8d517039d0d36b06db735307675099f19af963c6838685d505.jpg)  
(a)

![](images/3e4f4257a7f2f8c60f3f08ce4c063fa2a7e033f81ed0fe2ea234539a1e0f66ff.jpg)  
(b)

![](images/ba2f2f9b7ef73513bb0793e9183c976a60bffe7a6a32081177991a6d1c54f973.jpg)  
(c)

![](images/819ce78f1d37f5554c6048d6911bde899636331e49f15123262d8336d9b677bf.jpg)  
(d)

![](images/25fea9dbe8a8f02ceb4d1862c4351ae6918551619a5dcec20f1723108e627d49.jpg)  
(e)

![](images/53ac87f726b3c00d9e5980abf369213d9844eb024404ee0641c0fdb6160f60e2.jpg)  
(f)  
FIG. 15. Performance comparison via experimental results showing time-domain representation of reconstructed interference-suppressed signals (a) ANC, (b) SPARKLE, (c) WD, (d) VAFER-STFT, (e) Bi- method, and (f) proposed VAFER method.

![](images/76b124168baf6853eb3660f027c8e8b18d567edcae4ebff9bc3437600f268d45.jpg)

![](images/753d3e0fae169f615156a9675fe286b0256fe761d93108bb5cb21aaa39136d66.jpg)  
(b)

(a)  
![](images/e6f71f0537651aff0f2d5f37e57c76a5cfc78e4891392d790aaba96e38e4fc0b.jpg)  
(c)

![](images/ff23711829dc9190ffe37ef589391843567ae327f2ae46d6b4d97d9b97a60654.jpg)  
(d)

![](images/5e3ff032bf21b34ff83f7a40b099de9ead1723f0b91a8b07289eb1222bdc6189.jpg)  
(e)

![](images/290f8f33c9e8dfd5df55e9b401033287bd1bbc60469e941910791ac42637bd37.jpg)  
(f)  
FIG. 16. Performance comparison via experimental results showing range profiles (a) ANC, (b) SPARKLE, (c) WD, (d) VAFER-STFT, (e) Bi- method, and (f) proposed VAFER method.

For quantitative performance evaluation, we compare the SINR values computed by following the formulation in [14] on their experimental data after applying the compared schemes. Here we compute SINR based on their predefined empirical parameters such as guard cells and reference cells defined around the point target. Notice that the SINR computation using (25) requires a reference signal and it is computed for the entire signal and not just around the target peak. Note that due to the unavailability of raw interference-free data, the computation of the correlation coefficient is not feasible for this experimental setup. As a result, the SINR of interference-contaminated data is 2.94 dB; whereas that of the interference-suppressed signal after applying the ANC method is 4.97 dB, which is an improvement of 2.03 dB. In [14], ANC achieved an improvement of 7.6 dB in terms of signal-to-interference ratio (SIR). In contrast, we uniformly report SINR improvements across all methods for both simulation and experimental evaluations. Furthermore, while [14] employed an ANC filter with a step size of $\begin{array} { r } { \frac { 2 } { 3 0 \cdot p } , } \end{array}$ where P denotes reference signal power, we adopt a filter with a step size of $\frac { 2 } { 2 0 \cdot p }$ in our implementation. This setting improves robustness and steady-state suppression when the interference is strong or persists over longer pulse durations. Although this choice may slightly under-represent short-term gains in SIR, it provides a fairer and more stable basis for SINRbased comparison. The output SINR of SPARKLE method is 9.62 dB with an improvement of 6.67 dB, and the VAFER-STFT method improves SINR by 6.66 dB resulting in an output SINR of 9.61 dB. The WD method improves SINR by 5.79 dB, resulting in an output SINR of 8.73 dB. The Bi- $\cdot \ell _ { 1 }$ method improves SINR by 4.45 dB, resulting in an output SINR of 7.39 dB. The proposed VAFER method improves the SINR by 9.87 dB, resulting in an output SINR of 12.81 dB. In Fig. 16(e), we observe a target located at 0 m, this strong target is probably related to the reflected signal from the aggressor radar board, tripod, or some other target nearby. Notice that even though there can be some other target at 0 m, the proposed VAFER scheme outperforms other methods with a 9.87 dB improvement in SINR. The merits of the VAFER scheme can therefore be clearly observed.

## V. CONCLUSION

In this paper, we propose an interference suppression method, VAFER, based on VMD and FSST for FMCW radars. After a time-frequency analysis of VMD modes, we use an energy entropy-based threshold to eliminate interferencecontaminated modes. The effectiveness of the proposed VAFER scheme has been verified by comparing it with stateof-the-art methods such as ANC, SPARKLE, WD, Bi--<sub>1</sub>, and has been found to significantly improve the output SINR with a higher correlation coefficient for both simulated and experimental data. Also, the effect of varying the time duration of interference on output SINR and correlation coefficient has been studied. It is inferred that the proposed VAFER method can significantly suppress the interference without any observable degradation in performance. The proposed approach is expected to pave the way for a new paradigm in mutual interference suppression for FMCW radars.

## REFERENCES

[1] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 20–31, Sep. 2019.

[2] T.-N. Luo, C.-H. E. Wu, and Y.-J. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[3] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[4] A. Bourdoux, K. Parashar, and M. Bauduin, “Phenomenology of mutual interference of FMCW and PMCW automotive radars,” in Proc. IEEE Radar Conf., 2017, pp. 1709–1714.

[5] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[6] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw., 2016, pp. 1–9.

[7] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[8] L. Lan et al., “GLRT-based adaptive target detection in FDA-MIMO radar,” IEEE Trans. Aerosp. Electron. Syst., vol. 57, no. 1, pp. 597–613, Feb. 2021.

[9] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2016, pp. 1–4.

[10] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote. Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[11] R. W. Irazoqui and C. J. Fulton, “Spatial interference nulling before RF frontend for fully digital phased arrays,” IEEE Access, vol. 7, pp. 151261–151272, 2019.

[12] X. Hu, Y. Li, M. Lu, Y. Wang, and X. Yang, “A multi-carrier-frequency random-transmission chirp sequence for TDM MIMO automotive radar,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3672–3685, Apr. 2019.

[13] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in Proc. 9th Eur. Radar Conf., 2012, pp. 1–5.

[14] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[15] Z. Chen, F. Xie, C. Zhao, and C. He, “Radio frequency interference cancellation in high-frequency surface wave radar using orthogonal projection filtering,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 9, pp. 1322–1326, Sep. 2018.

[16] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[17] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst, vol. 22, no. 2, pp. 887–897, Feb. 2021.

[18] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Tech., vol. 69, no. 12, pp. 5270–5283, Dec. 2021.

[19] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Tech., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[20] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[21] Z. Liu, W. Lu, J. Wu, S. Yang, and G. Li, “A PELT-KCN algorithm for FMCW radar interference suppression based on signal reconstruction,” IEEE Access, vol. 8, pp. 45108–45118, 2020.

[22] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process., 2020, pp. 3802–3806.

[23] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

[24] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf., 2017, pp. 90–93.

[25] S. Chen, J. Taghia, U. Kühnau, T. Fei, F. Grünhaupt, and R. Martin, “Automotive radar interference reduction based on sparse Bayesian learning,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[26] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[27] Z. Xu, “Bi-level l optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, Jan. 2023.

[28] Y. Li, B. Feng, and W. Zhang, “Mutual interference mitigation of millimeter-wave radar based on variational mode decomposition and signal reconstruction,” Remote Sens., vol. 15, no. 3, 2023, Art. no. 557.

[29] Y. Weng et al., “FRFT-based interference suppression for automotive FMCW radars,” IEEE Trans. Veh. Technol., vol. 74, no. 6, pp. 8953–8965, Jun. 2025.

[30] Z. Liu, J. Wu, S. Yang, and W. Lu, “DOA estimation method based on EMD and MUSIC for mutual interference in FMCW automotive radars,” IEEE Geosci. Remote Sens. Lett., vol. 19, 2022, Art. no. 3504005.

[31] W. Zhou, X. Hao, J. Yang, L. Duan, Q. Yang, and J. Wang, “Interference mitigation method for millimeter-wave frequency-modulation continuous-wave radar based on outlier detection and variational modal decomposition,” Remote Sens., vol. 15, no. 14, 2023, Art. no. 3654.

[32] A. B. Baral, B. R. Upadhyay, and M. Torlak, “Automotive radar interference mitigation using two-stage signal decomposition approach,” in Proc. IEEE Radar Conf., 2023, pp. 1–6.

[33] K. Dragomiretskiy and D. Zosso, “Variational mode decomposition,” IEEE Trans. Signal Process., vol. 62, no. 3, pp. 531–544, Feb. 2014.

[34] G. Thakur and H.-T. Wu, “Synchrosqueezing-based recovery of instantaneous frequency from nonuniform samples,” SIAM J. Math. Anal., vol. 43, no. 5, pp. 2078–2095, 2011.

[35] A. Gaur, S. Srirangarajan, P.-H. Tseng, and K.-T. Feng, “Hough transform and time-frequency ridge-based interference mitigation in automotive FMCW radars,” inProc. IEEE 99th Veh. Technol. Conf., 2024, pp. 1–7.

[36] S. L. Hahn, “Hilbert transforms in signal processing,” inSignal Process., Norwood, MA, USA: Artech House, 1996.

[37] A. V. Oppenheim, Discrete-Time Signal Processing. Hoboken, NJ, USA: Pearson Education India, 1999.

[38] F. Auger et al., “Time-frequency reassignment and synchrosqueezing: An overview,” IEEE Signal Process. Mag., vol. 30, no. 6, pp. 32–41, Nov. 2013.

[39] T. Oberlin, S. Meignen, and V. Perrier, “The Fourier-based synchrosqueezing transform,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process., 2014, pp. 315–319.

[40] S. Dubnov, “Generalization of spectral flatness measure for non-Gaussian linear processes,” IEEE Signal Process. Lett., vol. 11, no. 8, pp. 698–701, Aug. 2004.

![](images/33ba3a04fa3e0eea8ab670debb1d97e803489240e38839dabc13fe29573aa05f.jpg)

ABHILASH GAUR (Member, IEEE) received the Bachelor of Technology degree in electronics and telecommunication engineering from the Sardar Vallabhbhai National Institute of Technology Surat, Surat, India, and the Master of Technology degree in signal processing and digital design from Delhi Technological University, New Delhi, India. He is currently working toward the Ph.D. degree jointly with the Bharti School of Telecommunication Technology and Management, Indian Institute of Technology Delhi, New Delhi, India and Inter-

national College of Semiconductor Technology, National Yang Ming Chiao Tung University Hsinchu, Taiwan, under IIT Delhi—NYCU Taiwan Joint Doctoral Program. His research interests include signal processing, interference management, and multi-modal sensor fusion for autonomous/intelligent vehicles.

![](images/7255d03ab3b69de522b6e55d52c18f48edd6eac08577093f20ab724a3d8babfa.jpg)

PO-HSUAN TSENG (Member, IEEE) received the B.S. and Ph.D. degrees in communication engineering from the National Chiao Tung University, Hsinchu, Taiwan, in 2005 and 2011, respectively. From Jan. 2010 to Oct. 2010, he was a Visiting Researcher with the University of California, Davis, Davis, CA, USA. He was an Associate Professor, from 2012 to 2017 and Assistant Professor from 2017 to 2022 with the Department of Electronic Engineering, National Taipei University of Technology, Taipei, Taiwan, where he has been a Full

Professor since 2022. His current research interests include signal processing for networking and communications, including wireless localization and sensing, networking for the Internet of Things, software-defined networks, and medical image analysis.

![](images/1048ead95abac939e7002ac05f98c36dc4b7af1e62dfe0a0059a9e19ca0efe0c.jpg)

KAI-TEN FENG (Senior Member, IEEE) received the B.S. degree from the National Taiwan University, Taipei, Taiwan, in 1992, the M.S. degree from the University of Michigan, Ann Arbor, MI, USA, in 1996, and the Ph.D. degree from the University of California, Berkeley, CA, USA, in 2000. During 2000–2003, he was an In-Vehicle Development Manager or Senior Technologist with OnStar Corporation, a subsidiary of General Motors Corporation, where he was working on the design of future Telematics platforms and in-vehicle net-

works. From 2003 to 2007, he was an Assistant Professor with National Yang Ming Chiao Tung University (NYCU), Hsinchu, Taiwan. From 2009 to 2010, he was a Visiting Research Fellow with the Department of Electrical and Computer Engineering, University of California at Davis, Davis, CA, USA. From 2007 to 2011, he was an Associate Professor with National Chiao Tung University (NCTU), Taipei, Taiwan. Since 2011, he has been a Full Professor with the Department of Electronics and Electrical Engineering, NCTU and NYCU. His current research interests include AI-empowered broadband wireless networks, wireless indoor localization and tracking, and device-free wireless sensing technologies. Dr. Feng was the recipient of Best Paper Award from the Spring 2006 IEEE Vehicular Technology Conference, which ranked his paper first among the 615 accepted papers, FutureTech Award in 2022 from National Science and Technology Council (NSTC), Outstanding Electrical Engineering Professor Award and Outstanding Youth Electrical Engineer Award in 2023 and 2007, respectively, from the Chinese Institute of Electrical Engineering, and Distinguished Researcher Award from NCTU in 2008, 2010, and 2011, respectively. He was on the technical program committees in various international conferences.

![](images/88f1a69cd00fef366d48d6921440f50a288a23b7b106e8610769bf25c97f244c.jpg)

SESHAN SRIRANGARAJAN (Senior Member, IEEE) received the B.E. degree in electrical engineering from the University of Mumbai, Mumbai, India, in 2001, and the M.S. and Ph.D. degrees in electrical engineering from the University of Minnesota, Minneapolis, MN, USA, in 2005 and 2008, respectively. He was an IRCSET/Intel Postdoctoral Fellow with the Nimbus Centre for Embedded Systems Research, Cork Institute of Technology, Cork, Ireland. From 2005 to 2006, he was with Wireless Technologies Group, Honeywell Technology

Center, Minneapolis, MN, USA, as an Intern. From 2008 to 2011, he was a Research Fellow with Intelligent Systems Center, Nanyang Technological University, Singapore. Since 2015, he has been with the Department of Electrical Engineering, Indian Institute of Technology Delhi, New Delhi, India, where he is currently an Associate Professor and Soumitra Dutta Chair Professor of artificial intelligence. His research interests include signal processing and wireless communications with current focus being on radar signal processing, positioning in wireless networks, and sensor networks.