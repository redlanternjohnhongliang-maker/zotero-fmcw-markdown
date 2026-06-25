# Interference Mitigation for FMCW Radar Based on Filtering in Fractional Fourier Domain

Beijing Institute of Technology, Beijing, China Beijing Institute of Remote Sensing Equipment, Beijing, China

Beijing Institute of Remote Sensing Equipment, Beijing, China

HAOYANG SUN

Beijing Institute of Technology, Beijing, China

ZHENXING LI

Beijing Institute of Remote Sensing Equipment, Beijing, China

Beijing Institute of Radio Metrology and Measurement, Beijing, China

Beijing Institute of Technology, Beijing, China

In this article, we explore interference mitigation (IM) techniques for frequency-modulated continuous-wave (FMCW) radar by employing filtering in the fractional Fourier transform (FrFT) domain. The

Received 25 April 2024; revised 23 September 2024 and 25 November 2024; accepted 19 December 2024. Date of publication 26 December 2024; date of current version 11 June 2025.

DOI. No. 10.1109/TAES.2024.3523255

Refereeing of this contribution was handled by F. Uysal.

This work was supported in part by STI 2030—Major Projects under Grant 2022ZD0209600, in part by the National Natural Science Foundation of China under Grant 62201058 and Grant 62475016, and in part by Science and Technology on Electromechanical Dynamic Control Laboratory Funding under Grant 6142601012402.

Authors’ addresses: Qile Chen is with the School of Mechatronical Engineering, Beijing Institute of Technology, Beijing 100081, China, and also with the Beijing Institute of Remote Sensing Equipment, Beijing 100854, China, E-mail: (tomber\_2012@163.com); Shengkai Ren, Zhenxin Li, and Wei Liang are with the Beijing Institute of Remote Sensing Equipment, Beijing 100854, China, E-mail: (451969681@qq.com; 1257888356@qq.com; lwlevil@163.com); Haoyang Sun and Ruiheng Zhang are with the School of Mechatronical Engineering, Beijing Institute of Technology, Beijing 100081, China, E-mail: (sunhaoyang6789@ 163.com; ruiheng.zhang@bit.edu.cn); Caixia Qiao is with the Beijing Institute of Radio Metrology and Measurement, Beijing 100089, China, E-mail: (miemieqcx@126.com). (Corresponding author: Ruiheng Zhang.)

suggested approach capitalizes on the observation that the acquired beat signal of the FMCW radar consists of multiple individual tones, while the interference manifests as brief chirped pulses. By leveraging the aggregation of the chirp signal in the FrFT domain with the corresponding order, the interferences are identified through a constant false alarm rate detector along the fractional frequency axis and alleviated by reconfiguring the FrFT spectrum. Furthermore, an iterative algorithm is formulated based on the golden section search to diminish the computational load of the search process for the corresponding order. The effectiveness of our approach is validated through simulated and measured data. The findings suggest that our IM approach is effective even in scenarios where the input signal-tointerference-plus-noise ratio is below 23 dB.

## I. INTRODUCTION

Frequency-modulated continuous-wave (FMCW) radar systems demonstrate exceptional capabilities in environmental sensing for road conditions, combining versatility and adaptability to diverse and challenging scenarios while maintaining cost efficiency. Compared to vision sensors, which are susceptible to noise interference [1], FMCW radars, renowned for their outstanding performance characteristics, have become integral components in automotive assistance systems [2], [3], autonomous driving technologies, and smart city infrastructures [4], [5]. Within advanced driver assistance systems, FMCW radars play a pivotal role in detecting oncoming traffic, thereby preventing collisions. Similarly, in smart urban environments, these radars are instrumental in traffic flow monitoring and management, contributing to safer and more efficient road networks.

However, the rapid proliferation of wireless sensing technologies has significantly increased the susceptibility of FMCW radars to interference. The globally allocated civilian radar frequency band, spanning 77–81 GHz, has become increasingly congested as FMCW radars require bandwidths typically exceeding 500 MHz to achieve high range resolution. This widespread adoption is expected to exacerbate spectrum resource congestion and lead to mutual interference among radar systems. For instance, contemporary automobiles are often equipped with three to five FMCW radars to enhance transportation safety, inevitably resulting in substantial interference between devices [6]. Furthermore, the integration of radar systems within smart city infrastructures has intensified the density of radiation sources in confined environments, amplifying the likelihood of interference [7], [8]. Such interference, originating from colocated radar systems or external radiation sources, may compromise radar performance, manifesting as reduced detection range or the erroneous identification of phantom targets. To address these challenges, the implementation of robust interference mitigation (IM) strategies is imperative to safeguard the operational reliability and effectiveness of FMCW radars.

## A. Related Works

In recent years, the issue of IM in FMCW radar systems has attracted considerable research attention. Extensive studies have been conducted to address mutual interference, a prevalent challenge in FMCW radar systems, particularly within automotive applications [9]. To tackle this issue, a wide array of methods and algorithms has been developed, specifically designed to mitigate interference under various operational scenarios. These approaches can be broadly classified into two primary categories: system design methodologies and signal processing strategies.

System design methodologies often focus on refining the intricacies of transmission signal waveforms and the overall architecture of radar systems. These efforts include the development of phase-coded FMCW or agile transmission waveforms [10], [11], [12], [13], [14], [15], sophisticated antenna structures and polarization schemes [16], [17], [18], as well as the application of spectrum sensing and software-defined radio technologies [19], [20], [21], [22]. Among the most prominent techniques is the phase encoding of radar transmission signals, augmented by the implementation of unique identity authentication mechanisms for each radar, effectively mitigating cross-interference between systems [10], [11], [12], [13], [14]. In addition to phase encoding, researchers have explored the use of noisemodulated signals to enhance identity recognition [15]. Beyond waveform encoding, identity differentiation through advanced antenna polarization and array structure designs is also under investigation [16], [18]. These approaches aim to embed unique identifiers within radar systems, allowing for the distinction between target echoes and interference signals. While these strategies offer effective solutions for IM, they often require substantial modifications to the radar’s architecture, resulting in increased system complexity and higher financial costs.

Signal-processing approaches can be categorized into three main methods: linear time–frequency transformation and filtering, sparse feature extraction and convex optimization, and intelligent filtering through machine learning. Linear time–frequency transformation and filtering represent the most significant approaches for the comprehensive advancement of time–frequency analysis technology. These methods aim to decompose target echoes and interference into different harmonics and filter out the harmonics corresponding to interference. A wide array of time–frequency analysis or harmonic analysis algorithms, such as the shorttime Fourier transform (STFT), empirical mode decomposition (EMD) [23], and wavelet transform [24], have been employed in IM of radar systems. In [25], an adaptive noise canceler (ANC) is devised to eliminate interference based on the symmetry of the interference in the frequency domain. In [26], the wavelet transform is utilized to remove interferences from desired signals. In [27], the beat signal of an FMCW radar is decomposed into a series of empirical modes, and an iterative modified method is employed to suppress the interference. In [28], the interference-polluted signal of the FMCW radar is detected and removed in the STFT domain, and then, an autoregressive model along the frequency bin is utilized to recover the removed segment. However, the received interference often bears strong resemblance to the target echoes, making it impossible to completely separate them from the target echoes. This may result in residual interference or partial loss of the target echoes. For instance, the method proposed in [29], based on cutting out segments of the STFT spectrum, will significantly reduce the detection probability of the target with increased segment removal. The method proposed in [30], which is based on EMD, introduces distortion of echo signals due to mode mixing.

Lately, nonlinear algorithms leveraging the sparsity disparity between target echoes and interference have been under consideration for employment in IM of radar systems. As radar interference is typically of short duration, the simplest nonlinear approach involves directly removing the segment accompanied by interference in the time domain [31], [32]. However, these methods often lead to the attenuation of the power of the target echoes. To tackle this issue, certain iterative interpolation algorithms have been utilized to recover the removed target echoes. In [28], iterative Burg interpolation was employed to reconstruct the removed segment based on the related estimated autoregressive model. In [33], the removed segment was extrapolated using the instrumental variable method with the autoregressive model. In [2], the removed segment was extrapolated using adaptive thresholding, which exploits the potential spectral sparsity of the beat signals. With specific prior knowledge about the desired target echoes and the accompanying interference, blind source separation based on convex optimization, commonly known as compressed sensing, is also employed in IM for FMCW radars. In [34], a method based on the low rank of the target echoes and the sparsity of the interference is proposed to suppress the interference, separating the target echoes and interference with a robust principal component analysis algorithm. In [35], IM methods based on the sparsity of the targets in the range–Doppler domain are proposed for synthetic aperture radar. However, all these methods require a precise prior knowledge of the signal’s sparsity. An inaccurate prior could potentially disrupt the entire algorithm. Furthermore, these algorithms necessitate a large number of iterations or the solution of the Least Absolute Shrinkage and Selection Operator regression, resulting in high computational complexity.

Recent advancements in the field of deep learning have revealed promising potential in IM for radar systems, attributed to their formidable feature extraction capabilities. In [36], [37], and [38], the convolutional neural network has been deployed to eliminate the concurrent interference and noise present in the range–Doppler domain output by the radars. Building upon the accomplishments of the convolutional neural network, the fully convolutional networks [39], recurrent neural networks [40], residual networks [41], and generative adversarial networks [42] are being explored to tackle the IM challenges encountered by FMCW radar systems. Deep networks have the ability to uncover concealed features of interference and noise, thereby showcasing commendable performance in severe interference scenarios. However, the training of these networks necessitates a substantial dataset of radar signals, presenting challenges in practical applications. Inadequate training datasets make addressing the overfitting problem difficult. A novel concept that integrates the neural network with traditional optimization algorithms is anticipated to resolve this issue [43], [44]. Nonetheless, these methods still require a dataset of over 4000 samples.

## B. Motivation and Contribution

In summary, the extensive range of existing research methodologies has significantly advanced our understanding of radar interference suppression strategies. Among these, IM techniques based on linear time–frequency transformation are considered the most practical, attributed to their robust mathematical foundations and ease of implementation. The selection of an optimal transformation method that aligns with the specific characteristics of the interference is pivotal in achieving effective discrimination between interference signals and target echoes.

Interference caused by aggressive radar systems typically appears as an FMCW signal with a sweep rate distinct from that of the victim radar. In rare circumstances, when the modulation slopes of the interfering radar and the victim radar align, the victim radar may erroneously register phantom targets. Given the low occurrence of interference with matching sweep rates, this study aims to address the challenge of mitigating interference characterized by varying sweep rates while preserving the generality of the proposed solution. Based on this premise, the interference within the digital beat signal can be modeled as a chirp pulse with a brief duration, whereas the target echo consists of multiple distinct frequency tones. By exploiting this fundamental difference, we propose employing the fractional Fourier transform (FrFT) [45], [46] to effectively isolate and suppress interference, thereby maximizing the separation of interference signals from target echoes.

By applying the FrFT at the matched order of the interference, the interference signal is effectively converted into a Dirac delta function, representing its most compact form. Following this transformation, a 1-D constant false alarm rate (CFAR) detector [47] is employed as an interference detection mechanism. In addition, a technique involving the reconstruction of the amplitude and phase components of the FrFT spectrum is utilized to eliminate the energy associated with the interference. To address the computational complexity associated with determining the matched order of interference, an innovative iterative algorithm, referred to as the iterative golden section search (GSS), has been developed. This algorithm significantly reduces the computational burden without compromising accuracy. The effectiveness of the proposed methodology is validated through comprehensive simulation and experimental evaluations. The key contributions of this study are outlined as follows.

1) This article introduces the pioneering concept of IM for FMCW radar through filtering in the fractional Fourier domain. By capitalizing on the consolidation of interference in the FrFT domain, it can be effectively segregated from the target echoes, thereby offering considerable potential for IM.

2) We have introduced an innovative approach for detecting and mitigating interference in the FrFT domain. A 1-D CFAR detector is employed at the matched order of the FrFT spectrum to identify the location of the interference. The process of nullifying or adjusting the amplitude of the FrFT spectrum corresponding to the location of the interference is implemented to eliminate the energy of the interference.

3) We have proposed an iterative strategy based on the framework of the GSS to reduce the computational burden of searching for the matched order of the FrFT in scenarios with multiple interferences.

## II. MATHEMATICAL MODEL

For an interfered FMCW radar with the bandwidth B and chirp duration T , its received signal can be denoted as follows:

$$
s _ { \mathrm { r e } } ( t ) = s _ { \mathrm { e c h } } ( t ) + s _ { \mathrm { i n } } ( t ) + w ( t )\tag{1}
$$

where $s _ { \mathrm { e c h } } ( t )$ represents the target echoes; when $n T \le t <$ $( n + 1 ) T$ , it can be expressed as

$$
s _ { \mathrm { e c h } } ( t ) = \sum _ { k = 1 } ^ { K } \sigma _ { k } \exp \left[ j 2 \pi f _ { 0 } \left( t - \tau _ { k } \right) + j \pi \beta \left( t - \tau _ { k } \right) ^ { 2 } \right] .\tag{2}
$$

Here, K is the number of target points, $k \in [ 1 , K ]$ is the index of the target, $\sigma _ { k }$ is the complex amplitude of target k, $\tau _ { k }$ is the time delay of target $k , f _ { 0 }$ is the carrier frequency of the radar, ${ \mathrm { , } } \beta = B / T$ is the chirp rate of the transmitting waveform, w(t ) is the surrounding noise, $s _ { \mathrm { i n } } ( t )$ is the interference accompanied by the target echoes, and n is the index of the chirp pulses. The time delay $\tau _ { k }$ is decided by the radial distance $R _ { k }$ and relative velocity v<sub>k</sub> between radar and target $k ,$ and it can be calculated by $\begin{array} { r } { \dot { \tau _ { k } } = 2 \frac { R _ { k } - v _ { k } n T } { c } } \end{array}$ . Therefore, the obtained beat signal after dechirp is denoted as

$$
\begin{array} { l } { { \displaystyle s _ { \mathrm { b e } } ( t ) = \sum _ { k = 1 } ^ { K } \sigma _ { k } \exp \bigg ( j \phi _ { n , k } - j 2 \pi \frac { 2 f _ { 0 } v _ { k } } { c } n T - j 2 \pi \beta \tau _ { k } t \bigg ) } } \\ { { \displaystyle ~ + \left[ s _ { \mathrm { i n } } ( t ) \cdot s _ { \mathrm { r e } } ^ { * } ( t ) \right] \otimes h _ { l p } ( t ) + w ( t ) , n T \le t < ( n + 1 ) T } } \end{array}\tag{3}
$$

where $\begin{array} { r } { \phi _ { n , k } = 4 \pi f _ { 0 } \frac { 2 R _ { k } } { c } + \pi \beta \tau _ { k } ^ { 2 } } \end{array}$ is the phase resulting from the dechirping operation, $s _ { \mathrm { r e } } ^ { * } ( t )$ is the reference signal used for dechirping, <sup></sup> is the convolution operation, and $h _ { \mathrm { l p } } ( t )$ is a low-pass filter. In the absence of interference, the radar system accurately determines the target’s range by calculating the instantaneous frequency of the beat signal over a single chirp duration using a fast Fourier transform (FFT) with respect to time. The target’s velocity is then determined by measuring the Doppler shift across multiple chirp durations, applying an FFT with respect to chirp index. This process is commonly referred to as a 2-D FFT.

Interferences received by FMCW radars are classified into two types, i.e., noncoherent and coherent, as illustrated in Fig. 1. Noncoherent interferences may impair the sensitivity and resolution of the radar or mask the presence of weak targets. Conversely, coherent interferences are known to cause the emergence of strong ghost targets. This study focuses on IM for FMCW radars utilized in automotive assistance, with a primary emphasis on addressing noncoherent interferences that are emitted by other radar systems. Predominantly, these interferences are noncoherent; instances of coherent interferences are exceedingly rare [27], [28], [31]. In this condition, $[ s _ { \mathrm { i n } } ( t ) \cdot s _ { \mathrm { r e } } ^ { * } ( t ) ] \otimes h _ { \mathrm { l p } } ( t )$ represents a superposition of short-chirped pulses, which can be expressed as

![](images/d72f32f27e1acfabe6e178954ea28a84fc77578ce01b76dddbb9c7789711e0e5.jpg)

![](images/6128efa26ba720ea212f5614a2a7910ad2f52c9083ad16925a8742cf0a9d6a3d.jpg)  
Fig. 1. Interferences received by the FMCW radar. The left part is the diagram of noncoherent interference, while the right part is that of the coherent interference. In this article, we consider the IM approach for the former interference.

![](images/ab2489706d461cef09f13d549916ab376fafbf622a9feef34d8674648ff0e420.jpg)

![](images/577d97fa656a2b69ca0cba1ea056908c3945164d612519b379cc90727cdbee80.jpg)  
Fig. 2. Illustration of (a) the obtained beat signal polluted by interference and (b) its STFT spectrum. In the STFT spectrum of the beat signal, the three horizontal lines in the black dotted rectangle are the target echoes, while the five slashes are the interference received by radar systems.

$$
\begin{array} { r l } & { \left[ s _ { \mathrm { i n } } ( t ) \cdot s _ { \mathrm { r e } } ^ { * } ( t ) \right] \otimes h _ { \mathrm { l p } } ( t ) = \displaystyle \sum _ { m = 1 } ^ { M } \mathrm { r e c t } \left( t - \tau _ { 1 , m } , \tau _ { 1 , m } - \tau _ { 2 , m } \right) } \\ & { \displaystyle \exp \left( j 2 \pi f _ { i n , m } t + j \pi \beta _ { i n , m } t ^ { 2 } \right) . } \end{array}\tag{4}
$$

In this context, rect( $\ t - \tau _ { 1 } , \tau _ { 1 } - \tau _ { 2 } )$ represents a gating function with a time delay of $\tau _ { 1 }$ and a duration of $\tau _ { 1 } - \tau _ { 2 } .$ The variables $f _ { \mathrm { i n } , m }$ and $\beta _ { \mathrm { i n } , m }$ denote the initial frequency and chirp rate, respectively, of the remaining interference after dechirping. The chirp rate of the residual interference consistently equals the difference between the radar’s inherent chirp rate and that of the interfering signal. Fig. 2 depicts the acquired beat signal, from which it can be inferred that the target’s beat signal comprises several complex exponentials, while the remaining interference after dechirping appears several short-chirped pulses.

The distinctions in the STFT spectrum between the beat signal of the targets and the remaining interferences motivate us to propose an IM approach by filtering in the FrFT domain.

## III. IM APPROACH VIA FILTERING IN THE FRFT DOMAIN

Amplifying the characteristics of the remaining interferences and accurately detecting them is essential for the radar’s IM. Considering that the useful signals comprise multiple individual frequencies, while the remaining interferences manifest as a superimposition of brief chirped pulses, the FrFT can be leveraged to aggregate the remaining interferences, rendering them more conspicuous and readily detectable. Consequently, we posit an approach that employs a 1-D CFAR detector to discern the remaining interferences and eliminate them within the FrFT domain. The pivotal step in our proposed approach is the estimation of the chirp rate of the short-chirped pulses.

## A. FrFT and the Aggregation of the Remained Interferences in the FrFT Domain

The FrFT is a generalization of the traditional Fourier transform and exhibits notable superiority in processing chirp signals. The FrFT of a chirp signal s(t ) can be expressed as

$$
F _ { \alpha } \{ s ( t ) \} ( u ) = \int _ { - \infty } ^ { \infty } s ( t ) K _ { \alpha } ( t , u ) d t\tag{5}
$$

where $K _ { \alpha } ( t , u )$ is the kernel function of FrFT, which can be expressed as

$$
K _ { \alpha } ( t , u ) = \left\{ \begin{array} { l l } { A _ { \alpha } \exp \left[ j \pi \left( t ^ { 2 } \cot \alpha + u ^ { 2 } \cot \alpha - 2 u t \csc \alpha \right) \right] } \\ { \qquad \alpha \neq z \pi } \\ { \delta ( t - u ) , \quad \alpha = 2 n \pi } \\ { \delta ( t + u ) , \quad \alpha = ( 2 n \pm 1 ) \pi } \end{array} \right.\tag{6}
$$

where $\delta ( \cdot )$ represents the Dirac function, α represents the rotation angle of the FrFT in the time–frequency plane with the unit radian, and $A _ { \alpha } = \sqrt { 1 - j \cot \alpha } \ \mathrm { F r F T }$ can be conceptualized as a rotation in the time–frequency plane, as illustrated in Fig. 3. In the case that the rotation angle of FrFT equals the chirp rate of s(t ), the signal manifests as a spike in the fractional domain.

The motivation for filtering in the FrFT domain for the IM issue arises from its ability to condense a chirp signal into the most concise form within the corresponding FrFT domain. For analytical purposes, we initially assume $M = 1$ in (4). Then, (3) can be reformulated as

$$
\begin{array} { l } { { \displaystyle F _ { \alpha } \{ s ( t ) \} ( u ) = \int _ { - \infty } ^ { \infty } \sum _ { k = 1 } ^ { K } \sigma _ { k } \exp \left( j \phi _ { n , k } - j 2 \pi \beta \tau _ { k } t \right) } } \\ { ~ + ~ } \\ { { \displaystyle + \mathrm { r e c t } ( t - \tau _ { 1 , 1 } , \tau _ { 1 , 1 } - \tau _ { 2 , 1 } ) \exp \left( j 2 \pi f _ { \mathrm { i n } , 1 } t + j \pi \beta _ { \mathrm { i n } , 1 } t ^ { 2 } \right) } } \\ { ~ + ~ w ( t ) K _ { \alpha } ( t , u ) d t . } \end{array}\tag{7}
$$

Our objective is to condense the remaining interference into its most succinct form. Accordingly, the order of the FrFT should be established as $\alpha = - \mathrm { a r c c o t } ( \beta _ { \mathrm { i n } , 1 } )$ . Then, (5) can

![](images/1b06552876643ff77c62e05690f457c8327b1f9b46c1b2ba63b907be6a35c7ca.jpg)  
Fig. 3. Rotation of FrFT in the time–frequency plane. The red line is the FrFT spectrum of a chirp signal with the matched order, while the black line is the FFT spectrum of the same signal. It can be seen that the FrFT spectrum is more compact.

be formulated as

$$
\begin{array} { r l } & { F _ { \alpha } \left\{ s _ { \mathrm { b e } } ( t ) \right\} ( u ) = \displaystyle \int _ { - \infty } ^ { \infty } \sum _ { k = 1 } ^ { K } \sigma _ { k } \exp \left( j \phi _ { n , k } - j 2 \pi \beta \tau _ { k } t \right) A _ { \alpha } } \\ & { \displaystyle \exp [ j \pi ( - t ^ { 2 } \beta _ { \mathrm { i n } , 1 } - u ^ { 2 } \beta _ { \mathrm { i n } , 1 } - 2 t u \sqrt { 1 + \beta _ { \mathrm { i n } , 1 } ^ { 2 } } ) ] d t + } \\ & { \displaystyle \delta ( j 2 \pi f _ { \mathrm { i n } , 1 } t - j 2 \pi t u \sqrt { 1 + \beta _ { \mathrm { i n } , 1 } ^ { 2 } } ) + \displaystyle \int _ { - \infty } ^ { + \infty } w ( t ) K _ { \alpha } ( t , u ) d t . } \end{array}\tag{8}
$$

With the matching order, the remaining interference is transformed into a Dirac function in the fractional frequency domain $u = f _ { \mathrm { i n , 1 } } / \sqrt { 1 + \beta _ { \mathrm { i n , 1 } } ^ { 2 } }$ , whereas the beat signal of the targets and the noise are spread throughout the entire FrFT domain.

## B. Interference Mitigation by Cell Averaging CFAR and Reconfiguration in the FrFT Spectrum

The energy of the interferences at the matched order of FrFT is consistently stronger than the desired signal (otherwise, IM would be less crucial). To detect the remaining interference along the fractional frequency axis, a 1-D CFAR detector is utilized. Specifically, we employ a cell averaging CFAR (CA-CFAR) detector on the FrFT spectrum, and a flag vector marking the index of the interference in the fractional frequency axis can be obtained. The entries are 1 and 0, where 1 corresponds to the positions of the interference in the fractional frequency axis. The parameters of the CA-CFAR, such as the probability of false alarms, can be configured based on the requirements of the applications.

After applying CA-CFAR, the resulting flag vector can be used to guide the interference. Using the flag vector, the simplest approach for IM is to zero out the FrFT spectra corresponding to the ones in, referred to as FrFT-ZO. However, this method filters out not only the remaining interference but also parts of the useful signals, potentially leading to grating lobes from other interferences and subsequently increasing the required number of cycles in Algorithm 1. To address this issue, we consider employing the amplitude correction method at the position of the interference, known as FrFT-AC. The fundamental concept of amplitude correction involves replacing the amplitudes of the FrFT spectra corresponding to the ones with the average amplitude of the FrFT spectra corresponding to the zeros, while retaining their original phases. The recovered FrFT spectra of the acquired beat signal can be expressed as

Algorithm 1: IM Approach via Filtering in the FrFT   
Domain.   
Input: beat signal $s _ { \mathrm { b e } } ( t )$ of the radar in a sweep;   
Output: the interference-free;   
1: while m $< = \mathbf { M } \| \alpha _ { m } \neq \frac { \pi } { 2 }$ do   
2: Estimating the matched order $\beta _ { \mathrm { i n } , m }$ of   
interference m;   
3: Obtaining the FrFT spectra $F _ { \alpha } \{ s _ { \mathrm { b e } ( t ) } \} ( u )$ by   
transforming the beat signal into the FrFT   
domain at order $\alpha _ { m } = - \operatorname { a r c c o t } ( \beta _ { \mathrm { i n } , m s } ) ;$   
4: Do CA-CFAR on $| F _ { \alpha } \{ s _ { \mathrm { b e } ( t ) } \} ( u ) |$ to obtain the   
flag vector;   
5: Zero out the interference or reconstruct the beat   
signal by:   
$\widetilde { F } _ { \alpha } \{ s _ { \mathrm { b e } } ( t ) \} u ( \mathbf { v } ) = A _ { \mathrm { a v } } \exp [ j 2 \pi \arg ( F _ { \alpha } \{ s _ { \mathrm { b e } } ( t ) \}$   
u(v))]   
$A _ { \mathrm { { a v } } } = \operatorname* { m e a n } \{ | F _ { \alpha } \{ s _ { \mathrm { { b e } } } ( t ) \} u ( \sim \mathbf { v } ) | \} ;$   
6: Transform $F _ { \alpha } \{ s _ { \mathrm { b e } } ( t ) \} ( u ( \mathbf { v } ) )$ into the time domain   
by inverse FrFT;   
7: end while

$$
\begin{array} { r l r } & { } & { \widetilde { F } _ { \alpha } \left\{ s _ { \mathrm { b e } } ( t ) \right\} u ( { \bf v } ) = A _ { \mathrm { a v } } \exp \left[ j 2 \pi \arg \left( F _ { \alpha } \left\{ s _ { \mathrm { b e } } ( t ) \right\} u ( { \bf v } ) \right) \right] } \\ & { } & { A _ { \mathrm { a v } } = \mathrm { m e a n } \left\{ | F _ { \alpha } \left\{ s _ { \mathrm { b e } } ( t ) \right\} u ( \sim { \bf v } ) | \right\} \qquad ( } \end{array}\tag{9}
$$

where u(v) represents the fractional frequency corresponding to the ones in v, and ∼ v is the bit-reversed form of v. $\widetilde { F } _ { \alpha } \{ s _ { \mathrm { b e } } ( t ) \} u ( \mathbf { v } )$ denotes the recovered value of the FrFT spectra at the index u(v), and arg $( F _ { \alpha } \{ s _ { \mathrm { b e } } ( t ) \} u ( \mathbf { v } ) )$ is the phase of the FrFT spectra at the index u(v). “mean” indicates the average operation. Through amplitude correction, interferences are significantly mitigated. It should be noted that the phases of FrFT spectra corresponding to the interference may still be disturbed. For a more precise reconstruction of the beat signal, the Burg-based extrapolation method can be employed to overcome potential phase disturbances. However, we will not delve into a detailed analysis of this method as the primary focus of this article is to filter out interference in the FrFT domain. After filtering out the interference and the reconstruction of the beat signal, the inverse FrFT is adopted to transform the interference-free beat signal back into the time domain. The traditional FFT-based ranging method is applied to obtain the range profiles of the target. In the cases where there are M > 1 interferences accompanying the acquired beat signal (assuming that their chirp rates are all different from each other), the aforementioned steps should be repeated M times. The complete IM approach is outlined in Algorithm 1.

![](images/ad737402a5a6f899eefc1cbe7529db87495f6ef9d951cc56bdef1e7b584305ef.jpg)  
(a)

![](images/564dabbd510e70861e997c6908e0e17e7c1e3613b49f5ef8702667355350857b.jpg)  
(b)

![](images/d26017a47e73a17874c559762ed4da00c80e97d9310e216169231c90a61ea133.jpg)  
(c)  
Fig. 4. Process of the GSS. (a) Initial iteration. (b) Second iteration. (c) Third iteration.

The unresolved issue in Algorithm 1 concerns the estimation of the matched order of the interferences. While this challenge can be addressed by conducting a peak search in the α-domain of the FrFT, it leads to a significant computational burden, even with the application of a coarse-to-fine strategy. Therefore, alternative strategies are essential to enable the real-time implementation of the IM approach. An iterative algorithm for the estimation of the matched order in the FrFT domain is the GSS. The GSS is an iterative process specifically designed to identify the maximum value of an unimodal continuous function by progressively narrowing the search scope with a minimal number of iterations [46]. Recent research [47] has confirmed that the α-domain represents an unimodal function. Consequently, we consider employing the GSS to search for the matched order of the interferences.

The process of GSS is depicted in Fig. 4. It commences with a predetermined search scope $[ \alpha _ { 1 } ^ { 0 } , \bar { \alpha } _ { 2 } ^ { 0 } ]$ and a specified tolerance 	. The gold ratio $r = ( \sqrt { 5 } - 1 ) / 2$ is used to calculate the order of the first iteration point as follows:

$$
\begin{array} { r } { \alpha _ { 1 } ^ { 1 } = \alpha _ { 2 } ^ { 0 } - r \left( \alpha _ { 2 } ^ { 0 } - \alpha _ { 1 } ^ { 0 } \right) } \\ { \alpha _ { 2 } ^ { 1 } = \alpha _ { 1 } ^ { 0 } + r \left( \alpha _ { 2 } ^ { 0 } - \alpha _ { 1 } ^ { 0 } \right) . } \end{array}\tag{10}
$$

Based on the monotonicity of FrFT with respect to the rotation angle α, we can select the peak value of the FrFT spectra with the rotation angle α, $P ( \alpha ) = \mathrm { m a x } _ { u } | F _ { \alpha } \{ s _ { \mathrm { b e } } ( t ) \} ( u ) |$ , as the cost function. The optimization direction is determined by calculating $P ( \alpha _ { 1 } ^ { 1 } )$ and $P ( \alpha _ { 2 } ^ { 1 } )$ . If $P ( \alpha _ { 1 } ^ { 1 } ) < P ( \alpha _ { 2 } ^ { 1 } )$ ), the search scope is updated to $( \alpha _ { 1 } ^ { 0 } , \alpha _ { 2 } ^ { 0 } ]$ , and the order of the second iteration point is then determined as follows:

$$
\begin{array} { l } { \alpha _ { 1 } ^ { 2 } = \alpha _ { 1 } ^ { 1 } - r \left( \alpha _ { 2 } ^ { 0 } - \alpha _ { 1 } ^ { 1 } \right) } \\ { \alpha _ { 2 } ^ { 2 } = \alpha _ { 2 } ^ { 1 } . } \end{array}\tag{11}
$$

If $P ( \alpha _ { 1 } ^ { 1 } ) > P ( \alpha _ { 2 } ^ { 1 } )$ , the search scope is updated to $[ \alpha _ { 1 } ^ { 0 } , \alpha _ { 2 } ^ { 0 } )$ and the order of the second iteration point is determined by

$$
\begin{array} { l } { { \alpha _ { 1 } ^ { 2 } = \alpha _ { 1 } ^ { 1 } } } \\ { { \alpha _ { 2 } ^ { 2 } = \alpha _ { 1 } ^ { 0 } + r \left( \alpha _ { 2 } ^ { 1 } - \alpha _ { 1 } ^ { 0 } \right) . } } \end{array}\tag{12}
$$

By continuously updating the search scope until the condition $| \alpha _ { 1 } ^ { i t } - \alpha _ { 2 } ^ { i t } | < \varepsilon$ is satisfied, the matched order of the interference can be calculated as $\begin{array} { r } { \alpha _ { \mathrm { i n } } = \frac { \alpha _ { 1 } ^ { i t } + \alpha _ { 2 } ^ { i t } } { 2 } } \end{array}$ , where ${ \mathrm { i t } } = 1 , 2 . .$ . represents the index of iterations. The designed iterative algorithm is presented in Algorithm 2. Introducing Algorithm 2 to Step 1 of Algorithm 1 accelerates the IM approach.

Algorithm 2: Iterative Algorithm for Estimating the   
Matched Order of the Interference Based on GSS.   
Initialize: $\alpha _ { 0 } ^ { 0 } , \alpha _ { 2 } ^ { 1 } , \mathrm { i t } = 1 ,$ €   
object function: $\begin{array} { r } { P ( \alpha ) = \operatorname* { m a x } _ { u } \{ | F _ { \alpha } [ s _ { \mathrm { b e } } ( t ) ] ( u ) | \} } \end{array}$   
$\alpha _ { 1 } ^ { 1 }  \alpha _ { 2 } ^ { 0 } - r ( \alpha _ { 2 } ^ { 0 } - \alpha _ { 1 } ^ { 0 } )$   
$\alpha _ { 2 } ^ { \bar { 1 } }  \alpha _ { 1 } ^ { \bar { 0 } } + r ( \alpha _ { 2 } ^ { \bar { 0 } } - \alpha _ { 1 } ^ { \bar { 0 } } )$   
while $| \alpha _ { 1 } ^ { i t } - \alpha _ { 2 } ^ { i t } | > \varepsilon$ do   
Calculate the objective function $P _ { ( } \alpha _ { 1 } ^ { i t } ) , P _ { ( } \alpha _ { 2 } ^ { i t } )$   
if $P ( \alpha _ { 1 } ^ { i t } ) < P _ { ( } \alpha _ { 2 } ^ { i t } )$ then   
$\alpha _ { 1 } ^ { i t + \bar { 1 } } = \alpha _ { 1 } ^ { i t } \stackrel {  } { - } r ( \alpha _ { 2 } ^ { i t - 1 } - \alpha _ { 1 } ^ { i t } )$   
$\alpha _ { 2 } ^ { i t + 1 } = \alpha _ { 2 } ^ { i t }$   
else   
$\alpha _ { 1 } ^ { i t + 1 } = \alpha _ { 1 } ^ { i t }$   
$\alpha _ { 2 } ^ { i t + 1 } = \alpha _ { 1 } ^ { i t - 1 } + r ( \alpha _ { 2 } ^ { i t } - \alpha _ { 1 } ^ { i t - 1 } )$   
end if   
end while

In the GSS, the loop terminates when $| \alpha _ { 1 } ^ { i t } - \alpha _ { 2 } ^ { i t } | < \varepsilon .$ Consequently, the number of iterations required by GSS is determined by 	. Assuming that the number of the iterations that the GSS needed to converge is denoted as $I T _ { \mathbf { \alpha } }$ , Serbes and Aldimashki [46] have demonstrated that IT satisfies the following formula:

$$
I T = \left\lceil \frac { \log \left[ \varepsilon / \left( \alpha _ { 1 } ^ { 0 } - \alpha _ { 2 } ^ { 0 } \right) \right] } { \log r } \right\rceil .\tag{13}
$$

Assuming that the sampling rate of the analog-to-digital converter (ADC) is $f _ { s } ,$ , Aldimashki and Serbes [48] have calculated the theoretical accuracy of the matched angle achieved by FrFT to be of $O [ ( T f _ { s } ) ^ { - 5 } ]$ . To attain this accuracy, the desired tolerance 	 should satisfy $\epsilon ^ { 2 }$ reaching an order of $O [ ( T f _ { s } ) ^ { - 5 } ]$ . There are an infinite number of choices for $\epsilon ;$ here, we select the following value:

$$
\varepsilon = \frac { \pi } { 2 } \left( T f _ { s } \right) ^ { - 3 } .\tag{14}
$$

Here, the optional multiplier $\pi / 2$ is added to make the following derivation more convenient. With $\epsilon$ selected by (13), the total number of iterations can be calculated as

follows:

$$
I T = 3 \left\lceil { \frac { \log _ { 2 } T f _ { s } } { \log _ { 2 } ( 1 / r ) } } \right\rceil .\tag{15}
$$

When there are 4096 samples of the beat signal, the total number of iterations is 48. In the application of the IM approach proposed in this article, achieving the theoretical estimation accuracy of the matched order is unnecessary. Consequently, the total number of iterations can be reduced.

## IV. NUMERICAL SIMULATIONS

In this section, the IM performance of FrFT-ZO and FrFT-CA is demonstrated through numerical simulations. Simultaneously, they are compared with three other approaches: the iterative modified threshold method based on empirical mode decomposition (IMT-EMD) approach [27], the ANC approach [25], and the wavelet denoising (WD) approach [26]. For the sake of convenient comparison among the five IM approaches, the correlation coefficient ρ between the beat signal after IM and a reference signal is utilized as the metric. The correlation coefficient is defined as follows:

$$
\rho \left( s , s _ { \mathrm { r e } } \right) = 1 0 \log _ { 1 0 } { \frac { s ^ { H } s _ { \mathrm { r e } } } { \left\| s \right\| _ { 2 } ^ { 2 } \left\| s _ { \mathrm { r e } } \right\| _ { 2 } ^ { 2 } } }\tag{16}
$$

where $s ^ { H }$ is the vectors of the beat signal before IM, and $s _ { \mathrm { r e } }$ is the vector of the reference signal.

## A. Point Target Simulation

Three point targets were strategically positioned in the illuminated scene at distances of 320, 510, and 790 m, respectively. The FMCW radar transmitted up-ramp signals, and the reflection coefficients of the three targets were set at 0.7, 0.3, and 1.2.

Here, we define the received signal-to-noise ratio (SNR) as

$$
\mathrm { S N R } = \frac { \left\| \sum _ { k = 1 } ^ { K } \sigma _ { k } \exp \left( j \phi _ { n , k } - j 2 \pi \frac { 2 f _ { 0 } v _ { k } } { c } n T - j 2 \pi \beta \tau _ { k } t \right) \right\| _ { 2 } ^ { 2 } } { \| w ( t ) \| _ { 2 } ^ { 2 } } .
$$

$$
n T \leq t < ( n + 1 ) T .\tag{17}
$$

Complex white Gaussian noise with an SNR of 10 dB was introduced to the target echoes of the victim radar.

Furthermore, the signal-to-interference-plus-noise ratio (SINR) is defined as

$$
\begin{array} { r l r } & { } & { \mathrm { S I N R } = \frac { \left\| \sum _ { k = 1 } ^ { K } \sigma _ { k } \exp \Big ( j \phi _ { n , k } - j 2 \pi \frac { 2 f _ { 0 } v _ { k } } { c } n T - j 2 \pi \beta \tau _ { k } t \Big ) \right\| _ { 2 } ^ { 2 } } { \| w ( t ) \| _ { 2 } ^ { 2 } + \left\| \left[ S _ { \mathrm { i n } } ( t ) \cdot s _ { r e } ^ { * } ( t ) \right] \otimes h _ { l p } ( t ) \right\| _ { 2 } ^ { 2 } } , } \\ & { } & { n T \leq t < ( n + 1 ) T . \qquad ( 1 8 ) } \end{array}
$$

The victim radar received three strong FMCW interferences with power levels of 120, 100, and 140, resulting in a beat signal with an SINR of −25.5 dB. The simulation parameters are detailed in Table I.

The range profile of the victim radar is depicted in Fig. 5(f) (brown dashed line) without the implementation of an IM approach. Due to substantial interferences, the two less prominent targets positioned at 320 and 510 m are completely obscured. When the proposed IM approach is employed for the victim radar, Algorithm 1 necessitates a minimum of three cycles to eliminate the three interferences. In the initial phase of our simulation, the obtained beat signal is initially transformed into the FrFT domain at the matched order. $\begin{array} { r } { \dot { \alpha _ { \mathrm { i n } , 3 } } = - \operatorname * { a r c c o t } ( \frac { 1 4 0 \mathrm { M H z } } { 1 0 \mu \mathrm { s } } ) } \end{array}$

TABLE I  
Simulation Parameters
<table><tr><td>Parameters</td><td>Victim radar</td><td>Inf1</td><td>Inf2</td><td>Inf3</td></tr><tr><td>Carrier frequency/GHz</td><td>79</td><td>79</td><td>79</td><td>79</td></tr><tr><td>Sweep duration/us</td><td>30</td><td>10</td><td>30</td><td>15</td></tr><tr><td>Bandwidth/MHz</td><td>100</td><td>100</td><td>60</td><td>140</td></tr><tr><td>Radar detection range/m</td><td>0 2000</td><td>1</td><td>1</td><td>1</td></tr><tr><td>ADC sampling frequency/MHz</td><td>200</td><td>1</td><td>1</td><td>/</td></tr></table>

The FrFT spectrum of the beat signal before and after IM, alongside the flag vector generated by CA-CFAR, is presented in Fig. 5(a). In Fig. 5(a), Inf3 manifests at two peaks located at fractional frequencies of 69.9 and 125.6 MHz. The presence of two peaks is a result of the interference’s sweep duration being half that of the transmitted signal from the victim radar, causing the interference to consist of two segments with different fractional frequencies [as depicted in Fig. 5(b)]. Following IM using FrFT-CA and FrFT-ZO, the resulting FrFT spectrum and its local zoom are displayed in Fig. 5(b) and (c).

FrFT-ZO creates a notch in the FrFT spectrum at the location of Inf 2. In contrast, FrFT-AC reconstructs the FrFT spectra corresponding to the location of the interference with a constant. This reconstruction of the FrFT spectrum mitigates jump discontinuities, which could otherwise lead to spectral leakage of target echoes and other interference, consequently reducing the loops required in Algorithm 1 (analyzed in Section IV-C). Algorithm 1 would need to be iterated at least three times to eliminate all interferences. Detailed information about other loops is not provided here.

After Algorithm 1 converges, the beat signals post-IM are illustrated in Fig. 5(d) and (e). In Fig. 5(d), the red line represents the beat signal after FrFT-AC, while the black line corresponds to FrFT-ZO. The majority of the three interferences are effectively suppressed by both FrFT-AC and FrFT-ZO. Some residuals of the interferences still appear as short pulses caused by the edge of the interference signal. Still, their impact on the radar is minimal due to their low power and short duration. In Fig. 5(e), the time–frequency domain of the red line is displayed. Compared with the time–frequency domain before IM [as shown in Fig. 5(b)], the interferences, represented as oblique lines, have been effectively removed. The range profiles of the beat signal post-IM are presented in Fig. 5(g). After IM, the three targets are visible and can be successfully detected by the radar. For comparison, the range profiles with different IM approaches are shown in Fig. 5(g) and (h). In these figures, the length of the adaptive filter for ANC is set to 160, the wavelet decomposition level is 8 for the WD approach, and the iterative modified threshold of the IMT-EMD is empirically set to 0.5.

![](images/4bc16f868093dd268ed654d02ad97e67e1646bd21b3e356f2474ecf6cf74b110.jpg)  
(a)

![](images/aa5c280ba19ab35a37d22937565b879218914fa84abd0c61a8ca2b428c2d2b79.jpg)

![](images/f697f91ab63aad07e50bcade45b467d683440b4f0001901cbc1b73772faf7555.jpg)  
(b)

![](images/5fdf6a93d0047c4ecc424c38e4d7cdc92ce1278e2b55cd974483924147b70af1.jpg)  
(d)

(c)  
![](images/95514e834b7a64fba6cc35760a587a895c557836831f9226c16cbdb43676c706.jpg)

![](images/367755c62742b496d954ea9afd75fb9de8861a952593008d4611155c82edcc7e.jpg)  
(e)  
(f)

![](images/3a0bbfeb41e240901425fc20f29c90d3fccb06e7f3492e59f91784f91bb36142.jpg)  
(g)

![](images/ea47f3a2cb14030f1cc508b5b7d3c942e2b2d2e03034264ac6224cede720e104.jpg)  
(h)

![](images/0e55e53ba56221c249f7dff83b7e167f46a071d5e4ef5bfcc91fc39c1ad074cb.jpg)  
(i)  
Fig. 5. Illustration of the proposed IM approaches and comparisons with other IM methods. (a) FrFT spectra of the beat signal at the matched order of interference 3 and the flag vector obtained by CA-CFAR. (b) and (c) FrFT spectra after IM with the FrFT-CA and FrFT-ZO. (d)–(f) Time domain, t– f domain, as well as the range profiles after IM with the FrFT-CA and FrFT-ZO. (g) and (h) Comparisons of the range profiles after IM with the five approaches. (i) Convergence process of the GSS in the triple loops of Algorithm 1.

In Fig. 5(g), only interference 2 is received by the victim radar, referred to as a weak interference case. Meanwhile, in Fig. 5(h), all three interferences are received by the victim radar, termed as a strong interference case. It is observed that under severe interference in our simulation, the WD and ANC approaches cannot eliminate the interference in both cases. The IMT-EMD can uncover the three targets; however, the power of the targets decreases by more than 3 dB in both cases. The proposed FrFT-AC and FrFT-ZO effectively suppress the interference in both cases while maintaining the original power of the targets. Finally, the convergence process of the GSS in the first three loops of FrFT-AC is shown in Fig. 5(h). It can be seen that the GSS in each loop converges after ten iterations, significantly reducing the cost of searching for the matched order of the interferences.

To evaluate the impact of the proposed method on the Doppler profile, Fig. 6 presents the range–Doppler plane derived from a 2-D FFT. The simulated environment includes two ideal point targets located at coordinates (800, 0) and (300, −5), both approaching the radar at velocities of 30 and 50 m/s, respectively. The radar system consists of three transmitters and four receivers, with each transmission frame containing 128 chirp pulses. Fig. 6(a)–(c) illustrates the case with interference 2 affecting target 1, while Fig. 6(d) and (e) includes both interferences 2 and 3, affecting targets 1 and 2, respectively. From Fig. 6(a) and (d), it is evident that the interference produces a linear false target group spanning multiple range units. However, as shown in Fig. 6(b), (c), (e), and (f), both the FrFT-AC and FrFT-ZO methods effectively suppress the interference. Since the FrFT and its inverse are linear operations, the Doppler characteristics of the targets are well preserved. Fig. 6(h) and (i), which depicts the Doppler profile of target 2, demonstrates that the proposed methods successfully suppress interference without exacerbating the sidelobes. In addition, Fig. 7 provides point cloud representations of the targets in Cartesian coordinates. In this simulation, the proposed approaches were applied across the four receiver channels of the radar system. In Fig. 7(a), interference results in a large number of false scattering points. However, in Fig. 7(b) and (c), these false scattering points are effectively removed. Fig. 7 further demonstrates that the proposed method does not affect radar angle measurement accuracy.

![](images/5ac00960f08c4e3bb2a2db7afb8401ef75a9bfe0f249f92c89a88773e4b988b3.jpg)  
(a)

![](images/884e87931b075b2f61dceadb2c3e50b900c333930d38fb5d72c00c1c41f41f79.jpg)

![](images/1930d675302d9e7d30abfc6c8c995c94717d24fab7bd29e8fb5b3aad817b8b5d.jpg)  
(d)

(b)  
![](images/c4bd41404080f3459babedc4c528ddc07718c2b0e3f880c6d602a9bc8baa0ee3.jpg)

![](images/cd31d436ab14cbd8ca9daf1ce8b219678bb4c86e3272bcad08da68ec90d744a4.jpg)

(c)  
![](images/723973a3f7f20c5d50d44c5f7829240e57d2539f2acb79c18ca9010489e45def.jpg)  
(f)

(e)  
![](images/4b6836a272707300d3aa52d7ae3080c00e69214035a21462c9a5382840e993d0.jpg)  
(g)

![](images/722e32d531eef1bef890cf16bf885044ec52bf650a0091a5cc64399ca70b11e6.jpg)  
(h)

Fig. 6. Range–Doppler plane obtained by the 2-D FFT under the condition of (a) one interference without the IM approach, (b) one interference with FrFT-ZO, (c) one interference with FrFT-AC, (d) two interferences without the IM approach, (e) two interferences with FrFT-ZO, (f) two interferences with FrFT-AC, (g) Doppler profile of target 2 with one interference, and (h) Doppler profile of target 2 with two interferences.  
![](images/59b71a2dab9290843ca4b48b7ef587cda409bd122554922ea9fc308c955dc12c.jpg)  
(a)

![](images/e97c61ccdd2c67220b225294fbc4e189d3821f995382d38741066ac705b49ee2.jpg)  
(b)

![](images/e004360747ed49c16b3ec0bbf76fbd244e24e21c1b3dcaf0716ffa8a0d2ff211.jpg)  
(c)  
Fig. 7. Cartesian coordinate system-based target point cloud image. (a) Without IM. (b) With FrFT-ZO. (c) With FrFT-AC.

## B. Effects of SNR and Interferences on IM

The IM performance of the proposed approaches is influenced by the number of interferences and the intensity of noise. In this section, we maintain the parameters listed in Table I while varying the added noise or the number of interferences to analyze the performance of the five IM approaches. The correlation coefficient, defined in (16), is used to assess the IM performance. Two scenarios are implemented, involving all three interferences or only interference 2. The SNR varies from −20 to 10 dB, and we conduct 100 Monte Carlo simulations to calculate the statistical average. The corresponding results are shown in Fig. 8.

![](images/d7930d76f6c55ea49d982a7e1cd77826ee76835df9433e6e353013fc34e1c9c1.jpg)

![](images/097320c9a9dabd8e40022c66444e25a8c1330e8cdc5e8ae6f075c1b1cb909e60.jpg)  
Fig. 8. Quantitative comparison of the five approaches. (a) Obtained correlation coefficient in the scenario with only interference 2. (b) Obtained correlation coefficient in the scenario with all three interferences.

It is evident that FrFT-AC and FrFT-ZO exhibit superior correlation coefficients in comparison to the other three IM methods when the SNR exceeds −10 dB. This can be attributed to the FrFT’s capacity for efficient interference aggregation, thereby enabling easier detection of interference under challenging SNR conditions. As the SNR drops below −10 dB, the sharp decrease in the correlation coefficient is attributed to target echoes being completely masked by noise, rather than indicating a failure of the proposed IM approach. However, this indicates that the proposed methods are unable to effectively filter out the noise. In scenarios involving three interferences or only Inf 2, ANC and WD demonstrate almost no ability to filter out the energy of the interferences in severe situations. Furthermore, the performance of IMT-EMD significantly deteriorates. Nevertheless, FrFT-AC and FrFT-ZO consistently maintain their performance.

## C. Effects of the Interference’ Chirp Rate

In addition to the number and intensity of interferences and noise, the chirp rate of the interference signal plays a critical role in the performance of the proposed IM approach. To explore this effect, we conducted simulations to evaluate the performance of the FrFT-ZO and FrFT-AC algorithms. In these simulations, only interference 2 was received by the radar system, with its chirp rate varying from 1.5 to 5 MHz/μs, corresponding to an interference bandwidth range of 45–150 MHz. The radar’s transmitted signal, on the other hand, had a chirp rate of 3.3333 MHz/μs. Fig. 9 illustrates the CFAR detection results for the FrFT spectrum of the beat signal. When the interference chirp rate is 1.1639 MHz/μs, the interference and target are clearly separated in the FrFT spectrum, allowing the CFAR detector to accurately identify the interference’s location. However, as the interference chirp rate approaches 3.3333 MHz/μs, the target echoes begin to cluster in the FrFT spectrum, as shown in Fig. 9(b) and (c). This clustering results in the IM approach mistakenly removing the target echoes. Once the interference chirp rate exceeds 3.6024 MHz/μs, the interference and target echoes are again distinctly separated in the FrFT spectrum.

To further quantify the impact of chirp rate on the performance of the proposed approach, we conducted 500 Monte Carlo simulations at each chirp rate, with a step variation of 0.01 MHz/μs. The chirp rate was varied from 1 to 5 MHz/μs, and the initial frequency of the interference signal was randomly selected within the 0–10 MHz range. To evaluate the effectiveness of the proposed approach, we defined the processing gain (PG) as the ratio of the output SINR to the input SINR

TABLE II  
Time Consumptions of the Five Approaches
<table><tr><td>Approaches</td><td>WD</td><td>ANC</td><td>EEMD</td><td>FrFT-AC</td><td>FrFT-ZO</td></tr><tr><td>Time[s]</td><td>0.13</td><td>0.78</td><td>13.9</td><td>1.13</td><td>3.18</td></tr></table>

$$
\mathrm { P G } = \frac { \mathrm { S I N R } _ { \mathrm { o u t p u t } } } { \mathrm { S I N R } _ { \mathrm { i n p u t } } } .\tag{19}
$$

Fig. 10(a) presents the average power across 500 Monte Carlo simulations at each chirp rate after applying the FrFT-ZO and FrFT-AC algorithms. The results indicate that the power of the target echoes remains relatively stable, around 2 dB, when the interference chirp rate is significantly different from that of the transmitted signal (3.3333 MHz/μs). However, as the interference chirp rate approaches 3.3333 MHz/μs, the power of the target echoes rapidly decreases, suggesting that the target echo is mistakenly suppressed by the proposed approach. Fig. 10(b) shows the PG, target echo loss, output SNR, and output SINR for the FrFT-AC algorithm. The results for the FrFT-ZO algorithm are similar and are thus not duplicated here. The loss of the target echo remains below 0.5 dB when the interference chirp rate deviates from the transmitted signal’s chirp rate by more than 0.06 MHz/μs. In these cases, the PG remains constant at approximately 30 dB, implying a 30-dB increase in the output SINR compared to the input SINR. Conversely, when the chirp rate of the interference signal closely matches that of the transmitted signal, the power of the target echo is significantly reduced, leading to a marked decrease in PG.

## D. Computation Time

The computational complexity of both the FrFT-AC and FrFT-ZO algorithms is primarily determined by the execution of the digital FrFT and the iterations of the GSS algorithm, which is employed to identify the matched order of the interference signals. Ozaktas et al. [49] proposed an efficient algorithm for computing the digital FrFT with a time complexity of approximately O(NlogN ). The GSS algorithm, on the other hand, typically requires eight to ten iterations to determine the correct matching order. For interference signals with identical slopes, regardless of whether they originate from a single radiation source, the proposed methodology incurs an estimated computational time of 10 O(NlogN ), effectively mitigating such interferences.

In our simulations, the digital beat signal comprises 6000 samples. Five IM approaches were implemented using MATLAB 2021b on a laptop with an Intel i7-9750H CPU @ 2.60 GHz and 16 GB of DDR 4. Their time consumption is presented in Table II. The WD has the minimum time consumption of 0.13 s compared to the other four approaches. FrFT-AC has a time consumption of 1.13 s, significantly lower than that of FrFT-ZO. This is because the zeroing-out operation in FrFT-ZO causes grating lobes of the other interferences, leading to a significant increase in the loops in Algorithm 1. If the stop conditions for the loops in Algorithm 1 are set as $\alpha _ { m } \neq \pi / 2 .$ , 29 loops are needed for the stop of FrFT-ZO, while only seven loops are needed for FrFT-AC.

(a)  
(b)  
![](images/67f09429dc020d1d5e0435ba4f0906730253aa2311031b1530f73f44ba38ea79.jpg)  
(a)

![](images/fcfe9fd38ced006f28e1caf2e94f3585b48644cbecd801d8a8c5801111a7fdd7.jpg)  
(b)

![](images/dc26f576679764647d20841efcbeafdec98187e91f0f07422f947e5172fba75f.jpg)  
(c)

![](images/413fb7e5c9a99e516bed480487ae085079a7d1194babac482b9a357a2df6efb9.jpg)  
(d)  
Fig. 9. FrFT spectrum of the beat signal with varying chirp rates of the interference. (a) Spectrum for an interference signal with a chirp rate of 1.1639 MHz/μs. (b) Spectrum for an interference signal with a chirp rate of 3.2357 MHz/μs. (c) Spectrum for an interference signal with a chirp rate of 3.33 MHz/μs. (d) Spectrum for an interference signal with a chirp rate of 3.6024 MHz/μs.

![](images/e69e923050df9b6ceba7247267f6abb92a9173d7c1fe83b08ff184e768c361f6.jpg)

![](images/66e141a102c5636b00266ec6441d77052b58e7bcb6650792bb6b43463c11fdd4.jpg)  
Fig. 10. Monte Carlo experiments of the proposed approach.  
(a) Average power of the 500 Monte Carlo experiments at each chirp rate. (b) PG, loss of the target echo, output SNR, and output SINR of the proposed FrFT-AC.

In these simulations, we dealt with three interference signals, each with distinct chirp rates. Despite this, the proposed FrFT-AC algorithm required seven cycles, resulting in a processing time of 1.13 s on our laptop. This extended runtime is attributed to the fact that even minimal residual interference can prompt further iterations of the algorithm. In practical applications, the number of iterations can be reduced by setting constraints on the iteration count or incorporating additional termination criteria. These modifications would effectively decrease the computational complexity of the algorithm.

## V. EXPERIMENTS

## A. Point Target Experimental Analysis

Some experimental data are utilized to validate our approaches. An IWR2243 radar with a power of 13 dBm is designated as the victim radar, while a self-developed radar with a power of 30 dBm is employed as the aggressor radar. Table III provides the detailed parameters of the two radars. Two corner reflectors with edges of 5 and 15 cm are utilized as two point targets. Test scenario diagrams are shown in Fig. 11(a) and (b). The acquired beat signal from the victim radar is processed by the laptop introduced in Section IV-C.

TABLE III  
Time Consumptions of the Five Approaches
<table><tr><td>Parameters</td><td>victim radar</td><td>aggressor radar</td></tr><tr><td>Center frequency/GHz</td><td>77</td><td>77</td></tr><tr><td>Bandwidth/MHz</td><td>500</td><td>600</td></tr><tr><td>Chirp rate/(MHz/us)</td><td>5</td><td>6</td></tr><tr><td>Sweep duration/us</td><td>100</td><td>100</td></tr><tr><td>Sampling rate/MHz</td><td>45/MHz</td><td>1</td></tr></table>

![](images/6de3e4969758f0551706f47cfc9f0aebd43dc159c3cabcc7a6fcefac94f13a31.jpg)  
(a)

![](images/1f239f32a105b49e5d7f0ee5385f20eadce34957d4ced8fec1cf20e547399e2a.jpg)  
Fig. 11. Experimental scenario of point targets. (a) Test scenario. (b) Geometrical configuration.

The time series of the beat signal obtained by the victim radar before IM is depicted in Fig. 12(a), where the interference appears as a short pulse chirp signal occupying 200 sampling units. Its corresponding range profiles are displayed in Fig. 12(c) (brown line), wherein the two trihedral corner reflectors are completely obscured by the interference. Since there is only one interference, we set the cycle number of Algorithm 1 to one. The time series after IM is presented in Fig. 12(b), indicating that most of the interference has been removed. In fact, the residual interference can be further eliminated by increasing the loops of Algorithm 1. The range profiles after IM are shown in Fig. 12(c), where they are compared with the reference range profile obtained by shutting down the aggressor radar. It is evident that both FrFT-ZO and FrFT-AC effectively remove the interference, allowing the two trihedral corner reflectors to form two peaks at 4.7 and 9.4 m. The peak at 11.5 m is formed by the tripod and chair used to support the aggressor radar.

![](images/7cd65c817b7fc2dd1869f29c5e1897830f008cb1004584fa19e95f1250a375b1.jpg)  
(a)

![](images/f3d79482596dfaa7cb885f280c3074b948817149b8b1158c1fe13f9c3dd22a18.jpg)  
(b)

![](images/fa5035969a771bfe3dd106ae0dda2318115138e662f052a81c9d41c5099ec601.jpg)  
(c)  
Fig. 12. Experimental results of the proposed IM approaches. (a) Time series before IM. (b) Time series after IM. (c) Range profile after IM.

![](images/e0816c08331f902a91a990a1b22a65e6a52e70378fe35ea553b4edd677b853c6.jpg)  
(a)

![](images/6616323dc7a78b7fac22718901588ee67d4ce8a34bdce4e7a7582ffab5f2fbbd.jpg)  
(b)  
Fig. 13. Experimental scenario of outdoor experiments. (a) Test scenario. (b) Geometrical configuration.

## B. Outdoor Experiments

To further validate the efficacy of the proposed method, we conducted outdoor experiments. The experimental setup and its corresponding geometrical configuration are depicted in Fig. 13, where two cars, positioned approximately 5 m in front of the radar, were simulated as targets. An aggressor radar was placed between the two cars. The aggressor radar operated with a bandwidth of 4585 MHz and a chirp duration of approximately 65 $\mu \mathbf { S } .$ The victim radar was a multiple-input multiple-output radar system with four transmitters and four receivers, operating with a bandwidth of 3398 MHz and a chirp duration of 50 μs. Each transmission frame consisted of 255 chirp pulses. To simulate the motion characteristics of the targets, the radar system was mounted on a track and controlled by a stepper motor, moving at a velocity of 0.2 m/s. The primary radiation lobe of the victim radar’s antenna beam is oriented orthogonally to its direction of motion, effectively aligning with both the intended target and the aggressor radar. In contrast, the main radiation lobe of the aggressor radar’s antenna is deliberately directed toward the victim radar.

The time series of the beat signal and the corresponding range profiles are shown in Fig. 14. In Fig. 14(a), it is clear that interference from the aggressor radar’s short chirp pulse contaminates the samples between indices 150 and 250. After applying the proposed IM approach, the interference is effectively removed. As depicted in the range profiles in Fig. 14(b), the interference raises the radar noise floor, masking distant targets. Once the proposed method is applied, the interference is eliminated, allowing for accurate detection of distant targets.

![](images/474c0ccda9788891161673411ad4671f71a356fce4a574c9bde9e0a338336a84.jpg)

(a)  
![](images/56cd6b2a96779958e158254e29fcf960f9f39fe44ac4a0e678fd2d3a0443ebdc.jpg)  
(b)  
Fig. 14. Experimental results of the proposed IM approaches. (a) Time series. (b) Corresponding range profiles.

Fig. 15 illustrates the range–Doppler plane generated using 255 chirp pulses from a single antenna channel and the range–azimuth plane obtained after applying various IM techniques to the 16 virtual channels formed by the arrangement of four transmitting and four receiving antennas. In addition to our proposed FrFT-ZO and FrFT-AC methods, we have replicated the WD approach introduced by Lee et al. [26], the STFT approach proposed by Wang [50], and the bilevel L1 approach suggested by Xu [51] for comparative evaluation. The range–Doppler plane without IM is depicted in Fig. 15(a), where the interference significantly elevates the radar noise floor to approximately 95 dB, obscuring most scattering points. Fig. 15(b) presents the range–Doppler plane after applying the WD approach, revealing that only a limited number of prominent scattering points are distinguishable above the noise floor. Fig. 15(e) and (f) shows the range–Doppler planes resulting from the STFT and bilevel L1 approaches, respectively. While both methods demonstrate effective anti-interference capabilities, noticeable residual interference persists. In contrast, Fig. 15(i) and (j) illustrates the substantial interference suppression achieved with our proposed method. Even weak scattering points become discernible, and the noise floor is reduced to approximately 70 dB, showcasing the effectiveness of the proposed approach.

(a)  
![](images/74012083beac14486447cd3277083ba7012f28dd966e470a53e4825475abd0f8.jpg)

![](images/415b381b379e99b849524b2c53378b2a162d8cc5e8ec20a102a77de1a130e7f5.jpg)

![](images/deeb54a325d221de25b7836294282819f74cb7a52b0a3c564805ea3955473662.jpg)  
(e)

![](images/8eac0c9874182ab64eab7f49cc8eab7658a97dcfa1b70df321b6bd34fcbe9f5d.jpg)

![](images/4d2ad7723fc66754fc318a068820f52745f0e7d62e180ba0e914565b2b35d3d0.jpg)  
(i)

(f)  
![](images/b6d64bc04de350901e600735e320846690968b01ab4e0a753d3cfded894a61fa.jpg)  
(j)

![](images/7bd6a1ca1a700b54300c7049504636bb0f4fef50b585a618e388b91c8d3a374b.jpg)  
(c)

![](images/ecff9cb49c11831c2567d6d7c0a06f8208a314534268a1088ff4e5876dd1f05e.jpg)

![](images/46d27234cb49329f2b3d2addb268a8d7e0a1a3b0711ae44ea2091d3c81534720.jpg)

(d)  
![](images/161f3454ad383ce69ba921872be81d6d2fe75b8fc5bab17048380416432f0437.jpg)

![](images/07110a9596477fce472f47f76a263bf2ca7d83ac46eeb03fb0b7de042cc334f1.jpg)  
(k)

![](images/4e5710bb7de0d83d632d5f7e05b16962e6c92baa2f2048842eb5cb2483f29aa9.jpg)  
(1)  
Fig. 15. Obtained range–Doppler and range–azimuth planes with different IM approaches. (a) and (c) Without IM. (b) and (d) With WD proposed by Lee et al. [26]. (e) and (g) With STFT proposed by Wang [50]. (f) and (h) With bilevel L1 proposed by Xu [51]. (i) and (k) With FrFT-ZO. (j) and (l) With FrFT-AC.

In Fig. 15(c), it is evident that the interference results in a 60<sup>◦</sup> fan-shaped noise floor centered in the azimuth direction. For a radar system with only four effective receiving channels, the interference spans a significant portion of the radar field of view. Fig. 15(d), (g), and (h) displays the range– azimuth planes obtained using the WD approach, STFT approach, and bilevel L1 approach, respectively. While these methods achieve some level of interference suppression, the noise floor around the location of the aggressor radar remains notably elevated to varying extents.

In contrast, Fig. 15(k) and (l) demonstrates the results of our proposed method, which significantly suppresses the interference. This improvement enhances the clarity and resolution of the radar imagery, enabling better detection of scattering points within the range–azimuth plane.

## VI. CONCLUSION

In this article, we propose FrFT-based approaches, specifically FrFT-ZO and FrFT-CA, designed to mitigate short-chirped pulse interference in FMCW radars. These approaches leverage the CFAR detector to identify interference at the corresponding matched order of the FrFT domain. FrFT-ZO employs the operation of zeroing out, while FrFT-CA applies amplitude correction in the FrFT domain to filter out interference. The performance of our approaches is compared with that of the other three methods. The results demonstrate that our approaches show outstanding IM in complex electromagnetic environments, as measured by the correlation coefficient between the recovered signal post-IM and the interference-free signal. In addition, FrFT-AC is more efficient than FrFT-ZO at the cost of a minor offset. In future research, we will introduce deep learning methods to achieve IM recognition more closely and may consider limited sample scenarios [52], [53] to match more practical application scenarios.

[1] R. Zhang et al., “Detail-aware network for infrared image enhancement,” IEEE Trans. Geosci. Remote Sens., vol. 63, 2025, Art. no. 5000314.

[2] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[3] C. S. Chaves, R. Geschke, M. Shargorodskyy, R. Brauns, R. Herschel, and C. Krebs, “Polarimetric UAV-deployed FMCW radar for buried people detection in rescue scenarios,” in Proc. 18th Eur. Radar Conf., 2022, pp. 5–8.

[4] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[5] R. Zhang, L. Xu, Z. Yu, Y. Shi, C. Mu, and M. Xu, “Deep-IRTarget: An automatic target detector in infrared imagery using dual-domain feature extraction and allocation,” IEEE Trans. Multimedia, vol. 24, pp. 1735–1749, 2022.

[6] Z. Ren, Y. Xiong, S. Li, D. Wang, and Z. Peng, “Sub-sampled twodimensional SAR imaging method based on MIMO FMCW radar,” in Proc. Int. Conf. Sens., Meas. Data Analytics Era Artif. Intell., 2020, pp. 221–223.

[7] S.D. Kim et al., “A new proposal of smart lighting system based on radar and camera sensors for smart city,” in Proc. Int. Conf. Comput. Sci. Comput. Intell., 2018, pp. 1448–1449.

[8] Q. Liu, H. Shu, L. Peng, L. Lv, O. Zhang, and G. Yuan, “Research and practice on the construction of connected vehicle in the greater bay area under the smart city,” in Proc. IEEE 25th Int. Conf. Intell. Transp. Syst., 2022, pp. 1882–1885.

[9] U. Kumbul, Y. Chen, N. Petrov, C. S. Vaucher, and A. Yarovoy, “Impacts of mutual interference analysis in FMCW automotive radar,” in Proc. 17th Eur. Conf. Antennas Propag., 2023, pp. 1–5.

[10] U. Kumbul, N. Petrov, C. S. Vaucher, and A. Yarovoy, “Smoothed phase-coded FMCW: Waveform properties and transceiver architecture,” IEEE Trans. Aerosp. Electron. Syst., vol. 59, no. 2, pp. 1720–1737, Apr. 2023.

[11] Q.-L. Chen, X.-H. Hao, X.-P. Yan, and P. Li, “A high performance waveform and a new ranging method for the proximity detector,” Defence Technol., vol. 16, no. 4, pp. 834–845, 2020.

[12] Q. Liu, J. Xu, Z. Ding, and H. C. So, “Target localization with jammer removal using frequency diverse array,” IEEE Trans. Veh. Technol., vol. 69, no. 10, pp. 11685–11696, Oct. 2020.

[13] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 201.

[14] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[15] Y. Kitsukawa, M. Mitsumoto, H. Mizutani, N. Fukui, and C. Miyazaki, “An interference suppression method by transmission chirp waveform with random repetition interval in fast-chirp FMCW radar,” in Proc. 16th Eur. Radar Conf., 2019, pp. 165–168.

[16] L. Lan, G. Liao, J. Xu, Y. Zhang, and B. Liao, “Transceive beamforming with accurate nulling in FDA-MIMO radar for imaging,” IEEE Trans. Geosci. Remote Sens., vol. 58, no. 6, pp. 4145–4159, Jan. 2020.

[17] I. Artyukhin, V. Ermolaev, A. Flaksman, A. Rubtsov, and O. Shmonin, “Development of effective anti-interference primary signal processing for mmWave automotive radar,” in Proc. Int. Conf. Eng. Telecommun., 2019, pp. 1–5.

[18] W. Li, Y. M. Wang, Y. Hei, B. Li, and X. Shi, “A compact low-profile reconfigurable metasurface antenna with polarization and pattern diversities,” IEEE Antennas Wireless Propag. Lett., vol. 20, no. 7, pp. 1170–1174, Jul. 2021.

[19] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[20] S. Ishikawa, M. Kurosawa, M. Umehira, W. Xiaoyan, S. Takeda, and H. Kuroda, “Packet-based FMCW radar using CSMA technique to avoid narrowband interference,” in Proc. Int. Radar Conf., 2019, pp. 1–5.

[21] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw., 2016, pp. 1–9.

[22] J.-H. Choi, H.-B. Lee, J.-W. Choi, and S.-C. Kim, “Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,” IEICE Trans. Commun., vol. 99, no. 1, pp. 280–287, 2016.

[23] I. Daubechies, J. Lu, and H.-T. Wu, “Synchrosqueezed wavelet transforms: An empirical mode decomposition-like tool,” Appl. Comput. Harmon. Anal., vol. 30, no. 2, pp. 243–261, 2011.

[24] S.-C. Pei, W.-L. Hsue, and J.-J. Ding, “Discrete fractional Fourier transform based on new nearly tridiagonal commuting matrices,” IEEE Trans. Signal Process., vol. 54, no. 10, pp. 3815–3828, Oct. 2006.

[25] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[26] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[27] J. Wu, S. Yang, W. Lu, and Z. Liu, “Iterative modified threshold method based on EMD for interference suppression in FMCW radars,” IET Radar, Sonar Navigat., vol. 14, no. 8, pp. 1219–1228, 2020.

[28] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[29] J. Ren, T. Zhang, J. Li, L. H. Nguyen, and P. Stoica, “RFI mitigation for UWB radar via hyperparameter-free sparse spice methods,” IEEE Trans. Geosci. Remote Sens., vol. 57, no. 6, pp. 3105–3118, Jun. 2019.

[30] N. E. Huang et al., “The empirical mode decomposition and the hilbert spectrum for nonlinear and non-stationary time series analysis,” Proc. Roy. Soc. London. Ser. A: Math., Phys. Eng. Sci., vol. 454, no. 1971, pp. 903–995, 1998.

[31] G. Babur, “Processing of dual-orthogonal CW polarimetric radar signals,” Ph.D. dissertation, Univ. Delft Univ. Technol., Delft, The Netherlands, pp. 73–75, 2009.

[32] G. Babur, Z. Wang, O. A. Krasnov, and L. P. Ligthart, “Design and implementation of cross-channel interference suppression for polarimetric LFM-CW radar,” Proc. SPIE, vol. 7745, 2010, Art. no. 774520.

[33] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in Proc. IEEE Radar Conf., 2019, pp. 1–6.

[34] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822–834, 2022.

[35] Y. Huang, G. Liao, J. Li, and J. Xu, “Narrowband RFI suppression for SAR system via fast implementation of joint sparsity and lowrank property,” IEEE Trans. Geosci. Remote Sens., vol. 56, no. 5, pp. 2748–2761, May 2018.

[36] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in Proc. 22th Int. Conf. Inf. Fusion, 2019, pp. 1–8.

[37] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world FMCW radar signals,” in Proc. IEEE Int. Radar Conf., 2020, pp. 624–629.

[38] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Top. Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021.

[39] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in Proc. IEEE 92nd Veh. Technol. Conf., 2020, pp. 1–5.

[40] C. Jiang, T. Chen, and B. Yang, “Adversarial interference mitigation for automotive radar,” in Proc. IEEE Radar Conf., 2021, pp. 1–6.

[41] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process., 2020, pp. 3802–3806.

[42] W. Fan et al., “Interference mitigation for synthetic aperture radar based on deep residual network,” Remote Sens., vol. 11, no. 14, 2019, Art. no. 1654.

![](images/e8454ad34926737a4a8619e9334512e4dfc502d1648e15b2238363dda366fb6f.jpg)

[43] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for FMCW radars,” IEEE Trans. Geosci. Remote Sens., vol. 60, 2022, Art. no. 5118316.

[44] N.-C. Ristea, A. Anghel, R. T. Ionescu, and Y. C. Eldar, “Automotive radar interference mitigation with unfolded robust PCA based on residual overcomplete auto-encoder blocks,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., 2021, pp. 3209–3214.

[45] M. A. Richards et al. Fundamentals of Radar Signal Processing, vol. 1. New York, NY, USA: Mcgraw-Hill, 2005.

[46] A. Serbes and O. Aldimashki, “A fast and accurate chirp rate estimation algorithm based on the fractional Fourier transform,” in Proc. 25th Eur. Signal Process. Conf., 2017, pp. 1105–1109.

[47] Y. Ye, L. Qing-Fu, and F. Ying, “Detection and parameter estimation of multicomponent LFM signals based on Hilbert-Huang Hough transform,” in Proc. Asia-Pacific Conf. Comput. Intell. Ind. Appl., vol. 1, 2009, pp. 476–479.

[48] O. Aldimashki and A. Serbes, “Performance of chirp parameter estimation in the fractional Fourier domains and an algorithm for fast chirp-rate estimation,” IEEE Trans. Aerosp. Electron. Syst., vol. 56, no. 5, pp. 3685–3700, Oct. 2020.

[49] H. M. Ozaktas, O. Arikan, M. A. Kutay, and G. Bozdagt, “Digital computation of the fractional Fourier transform,” IEEE Trans. Signal Process., vol. 44, no. 9, pp. 2141–2150, Sep. 1996.

[50] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 23, no. 8, pp. 12229–12238, Aug. 2022.

![](images/a5a623edf27e8810988d21a74da7034c0a129ace5cabbd62e626d1bf562bf170.jpg)

[51] Z. Xu, “Bi-level l1 optimization-based interference reduction for millimeter wave radars,” IEEE Trans. Intell. Transp. Syst., vol. 24, no. 1, pp. 728–738, Jan. 2023.

![](images/f62a7c9c1c8b831a85a531272a1492630986d6898c375264d04b63b4dbfb57b3.jpg)

[52] R. Zhang et al., “Cognition-driven structural prior for instance-dependent label transition matrix estimation,” IEEE Trans. Neural Netw. Learn. Syst., 2024, early access, doi: 10.1109/TNNLS.2023.3347633.

[53] R. Zhang et al., “Part-aware correlation networks for few-shot learning,” IEEE Trans. Multimedia, vol. 26, pp. 9527–9538, 2024.

![](images/fea2e37edb5da5e4e148784f01a09cd7665c77b3e312a43302b84e8c8e085e2e.jpg)

![](images/9d5a18850d0cfa594fee19d4b2658bc22ad3f82051f66847f145cd27d5629e5c.jpg)  
Qile Chen received the B.Sc. degree in detection guidance and control and the Ph.D. degree in armament science and technology from the Beijing Institute of Technology, Beijing, China, in 2015 and 2021, respectively.  
He is currently an Engineer with the Beijing Institute of Remote Sensing Equipment, Beijing. His main research interests include radar signal processing, digital signal processing, and deep learning.

![](images/de37b8fe66ec549dd70ecc54cf1318746f983dbab920ad73db6aea4c38ddf51c.jpg)

Shengkai Ren received the B.Sc. and M.Sc. degrees in information engineering from Xidian University, Xi’an, China, in 2011 and 2014, respectively.

He is currently a Senior Engineer with the Beijing Institute of Remote Sensing Equipment, Beijing, China. His main research interests include radar signal processing and passive detection.

Haoyang Sun received the M.S. degree in weapon engineering from the Department of Equipment Engineering, Shenyang Ligong University, Shenyang, China, in 2019. He is currently working toward the Ph.D. degree with the Beijing Institute of Technology, Beijing, China.

His research interests include radar signal processing, multimodality learning, and object detection.

Wei Liang received the B.Sc. and M.Sc. degrees in electromechanical engineering from the Beijing Institute of Technology, Beijing, China, in 1999 and 2002, respectively.

He is currently a Professorial Fellow with the Beijing Institute of Remote Sensing Equipment, Beijing. His main research interests include radar signal processing and array signal processing.

Zhenxing Li received the M.Sc. degree in control science and engineering from Beihang University, Beijing, China, in 2020.

He is currently an Engineer with the Beijing Institute of Remote Sensing Equipment, Beijing. His main research interests include radar signal processing and electronic countercountermeasures.

Caixia Qiao received the M.Sc. degree in weapon enginnering from the Beijing Institute of Technology, Beijing, China, in 2021.

She is currently an Engineer with the Beijing Institute of Radio Metrology and Measurement, Beijing. Her main research interests include digital signal processing and time–frequency analysis.

![](images/9a96a4d9291c42ab791518458d1b38494f7f7584f9b79561b149c383a016beb0.jpg)

Ruiheng Zhang (Member, IEEE) received the B.E. degree in information engineering from the Beijing Institute of Technology, Beijing, China, in 2014, and the Dual-Ph.D. degree in information systems from the University of Technology Sydney, Ultimo, NSW, Australia, and the Beijing Institute of Technology.

He is currently an Associate Professor with the Beijing Institute of Technology. He is the author of more than 50 research papers, including IEEE TRANSACTIONS ON NEURAL NETWORKS

AND LEARNING SYSTEMS, IEEE TRANSACTIONS ON MULTIMEDIA, IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS FOR VIDEO TECHNOLOGY, IEEE TRANSACTIONS ON GEOSCIENCE AND REMOTE SENSING, Remote Sensing of Environment, International Conference on Learning Representations, International Conference on Machine Learning, European Conference on Computer Vision, and so on. His current research interests include object understanding and multimodal learning.

Dr. Zhang is a Member of the Editorial Board of Frontiers in Robotics and AI. He was an Area Chair/Technical Program Committee Member of ACM Multimedia Conference, IEEE International Conference on Data Mining, Asia Symposium on Image Processing, and International Conference on Video, Signal and Image Processing.