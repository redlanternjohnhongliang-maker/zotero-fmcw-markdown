Article

# Incoherent Interference Detection and Mitigation for Millimeter-Wave FMCW Radars

Zhihuo Xu <sup>1,2</sup> , Shuaikang Xue <sup>1,2</sup> and Yuexia Wang <sup>1,2,</sup>\*

1 Radar Remote Sensing Group, School of Transportation, Nantong University, Nantong 226019, China

School of Information Science and Technology, Nantong University, Nantong 226019, China

\* Correspondence: venus@ntu.edu.cn; Tel.: +86-0513-85962369

Abstract: Current automotive radar technology is almost exclusively implemented using frequency modulated continuous wave (FMCW) radar in the millimeter wave bands. Unfortunately, incoherent interference is becoming a serious problem due to the increasing number of automotive radars in dense traffic situations. To address this issue, this article presents a sparsity-based technique for mitigating the incoherent interference between FMCW radars. First, a low-pass filter-based technique is developed to detect the envelope of the interference. Next, the labeled regions where interference is present are considered as missing data. In this way, the problem of mitigating interference is further formulated as the restoration of the echo using L1 norm-regularized least squares. Finally, the alternating direction method of the multipliers-based technique is applied to restore the radar echoes. Extensive experimental results demonstrate the effective performance of the proposed approach. Compared to state-of-the-art interference mitigation methods, the proposed method remarkably improves the quality of radar targets.

Keywords: millimeter-wave radar; frequency modulated continuous wave (FMCW); incoherent interference; sparse optimization

![](images/5c5df57ad8f5bdc104ae760f98cb7c677c34b9eedbfa65512f073d26e3f93ca3.jpg)

Citation: Xu, Z.; Xue, S.; Wang, Y. Incoherent Interference Detection and Mitigation for Millimeter-Wave FMCW Radars. Remote Sens. 2022, 14, 4817. https://doi.org/10.3390/ rs14194817

Academic Editor: Piotr Samczynski

Received: 28 June 2022   
Accepted: 11 September 2022   
Published: 27 September 2022

Publisher’s Note: MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations.

![](images/4eb3956c17bcabd2efc1e140d791c75ba4a0892bd3ace0de1481aeae98ab26f2.jpg)

Copyright: © 2022 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

## 1. Introduction

Radar is a highly robust and reliable sensor for automotive applications [1]. First, automotive radars measure the relative distance, velocity, and angle of targets through time delay and phase shift of radio signals, and therefore can perform well in adverse weather conditions. Second, automotive radars operate in the millimeter wave band and have a large bandwidth; hence, a high range resolution of 3 cm can be achieved [2]. In addition, the radar system is both simple and effective, using linear frequency-modulated continuous wave (FMCW) technology [3]. Therefore, automotive FMCW radar has the advantageous benefits of small size, light weight, and low power consumption, and is widely used in self-driving vehicle applications [4].

Active signal transmission is one of the advantages of radar; however, it can cause serious interference problems with neighboring radars [5–7]. Similar to non-homogeneous clutter [8,9], radar target detection performance is degraded by incoherent interference. The interference probability can be reduced by alternating the parameters of radar waveforms [10]. Although different FMCW radars use different parameters, incoherent interference can occur when the spectrum of the interfering signal overlaps the transmitted wave of the radar under test. The incoherent interference produces strong noise and even ghost targets. Consequently, suppressing the incoherent interference in radar images is one of the most pressing issues for automotive FMCW radars.

Although the mitigation of incoherent interference remains an open problem, several interference mitigation approaches have been proposed. The first type of approach aims to design radar waveforms to overcome the drawbacks of FMCW radar with a fixed time–frequency relationship. Orthogonal pseudo-random noise waveforms can be designed to reduce the probability of interference [11,12]. Phase-modulated continuous wave (PMCW) [5] and phase-coded frequency-modulated continuous wave (PC-FMCW) [13] approaches have been successively proposed to avoid interference with FMCW radars. However, mutual interference can nevertheless appear between PMCW and FMCW radars.

In order to be applicable to FMCW radar images, signal post-processing techniques have been used to develop interference suppression methods [14]. Brooker [15] deals with interference by inverse cosine windowing and substituting zeros for the high-amplitude transient. Before removal of transient interference by substituting zeros over the period of interference, accurate interference detection is required in order to determine the location of the interference. Neemat et al. [16] first used image processing techniques to detect interference in the short-time Fourier transform (STFT) domain, then carried out beat signal model parameters estimation analysis using autoregression in the STFT. Finally, they replaced suppressed beat–frequency frames with linear-predicted interpolated ones. Jung et al. [17] applied an order statistics–constant false alarm rate (OS-CFAR) algorithm to identify the interference regions. Then, the Kalman filter was used to estimate the state and predict the signals in the interference region. After filtering of the signal, large peaks in the time domain beat signal were reduced and the target signal was estimated. Wang et al. [18] first cut out the interference-contaminated region of the received signal, then interpolated the signal samples in the cutout segment using the matrix-pencil method.

Unlike the above-mentioned methods of zeroing or reconstructing the signal for interference-contaminated areas, processing of the entire received signal is another technical route to interference suppression. Lee et al. [19] considered the low-intensity target signal as the noise component to be removed and the high-intensity pulse-like interference signal as the signal to be retained. Using a wavelet transform and thresholding the wavelet coefficients of the low-pass filter output, they were able to extract the pulse-like interference signal. Afterwards, the interference signal was subtracted from the original low-pass filter output to generate the desired target signals. The beat frequencies of real targets always present a positive frequency, whereas only the noise and the interference are in the negative half of the frequency spectrum. Thus, Jin and Cao [20] calculated the power of the negative frequency as a reference of interference and fed the positive frequency and negative frequency components into the primary and reference channel, respectively, of an adaptive noise canceler (ANC). Wu et al. [21] proposed an iterative modified threshold method based on empirical mode decomposition (IMT-EMD) for interference suppression in FMCW automotive radars, and applied the consecutive mean square error algorithm to determine the interference-dominated components after decomposing. Specifically, the interference problem can be considered as the sum of two component signals, i.e., the target signal plus the interfering signal. Therefore, interference reduction can be achieved by separating the interfering signal from the received signal. From this perspective, [22] developed an interference mitigation technique to successfully separate the interference from the received signal in the tunable Q-factor wavelet transform domain. Uysal [23] applied morphological component analysis (MCA) [24] theory to decompose the received signal into interference and target signals. Rock et al. [25] evaluated a convolution neural network (CNN)-based method for carrying out interference reduction on real FMCW radar measurements by combining real measurements with simulated interference in order to obtain input–output data suitable for training their CNN model.

In summary, the incoherent interference problem is a pressing problem in automotive FMCW radars that considerably negates the inherent advantages of radar by decreasing the detection probability and reliability of sensors. Although this challenge has been investigated and several aforementioned approaches have been developed in this field, there remains a need for an efficient solution that can help to mitigate the strong interference in radar images. The contributions of this work to this problem can be summarized as follows:

A simple yet effective interference detection technique using a low-pass filter is presented, and the presence of interference is further determined from the statistics of the output envelope of this filter. In this way, the results of interference detection can indicate the presence or absence of interference. We propose an interference mitigation algorithm that cannot be started in the absence of interference, which significantly increases real-time processing performance.

A sparsity model is presented to reduce the incoherent interference by considering the interference regions as missing data. Using L1 norm-regularized least squares, an alternating direction method of multipliers (ADMM)-based technique is been derived to restore the radar echoes.

In several comparison experiments, dynamic incoherent interference is generated; the case of dynamic interference is much closer to the real-world self-driving situation. In experiments with dynamic interference signals, the comparative performance of different algorithms is comprehensively evaluated and the potential use of the algorithms in real roads is further analyzed.

In addition, both the wavelet-based [19] and the MCA-based [23] methods are improved when using our proposed interference envelop detection approach.

Our extensive experiments demonstrate that the proposed method significantly outperforms the state-of-the-art methods on both simulated and real radar interference mitigation tasks.

The rest of this paper is outlined as follows. Section 2 introduces the formulations related to the incoherent interference between FMCW radars. Section 3 proposes detection and mitigation of incoherent interference. Section 4 demonstrates the extensive measurements used to compare the proposed techniques with state-of-the-art methods. Section 5 discusses sparsity-based methods, algorithm complexity, and the impact on performance of interference regions that lead to missing data components. Finally, we present our conclusions in Section 6.

## 2. Incoherent Interference

According to recommendations by the International Telecommunication Union (ITU), most automotive radars currently operate within the 76–81 GHz bandwidth with FMCW signals [26]. The transmitted radar signal $s _ { \mathrm { t x } } ( t )$ can be written as follows:

$$
s _ { \mathrm { t x } } ( t ) = A _ { \mathrm { t x } } { \cos } ( 2 \pi f _ { c } t + \pi k _ { r } t ^ { 2 } ) ,\tag{1}
$$

where t is time, $A _ { \mathrm { t x } }$ is the amplitude of the transmitted signal, $f _ { c }$ is the center frequency of the radar, and $k _ { r }$ is the chirp rate. Suppose a vehicle at a distance R meters from the radar is driving at a speed v m/s; then, the corresponding radar echo is described as

$$
s _ { \mathrm { r x } } ( t ) = A _ { \mathrm { r x } } \mathrm { c o s } [ 2 \pi f _ { c } ( t - \Delta t ) + \pi k _ { r } ( t - \Delta t ) ^ { 2 } ] ,\tag{2}
$$

where $A _ { \mathrm { r x } }$ is the amplitude of the echo, the delay time $\Delta t = 2 ( R + v t ) / c .$ , and c is the velocity of light.

After the dechirp operation, the received signal is expressed as

$$
r _ { t } ( t ) = A _ { t } \mathrm { c o s } ( 2 \pi \Delta t k _ { r } t + \phi _ { r } ) ,\tag{3}
$$

where $A _ { t }$ is the amplitude of the received signal and $\phi _ { r }$ is the phase that includes the target Doppler information. The frequency of the target signal with respect to time t is further derived as

$$
f _ { t } ( t ) = \Delta t k _ { r } .\tag{4}
$$

If the neighboring radars and the radar under test have the same transmit waveform, then coherent interference may appear; false targets are generated when this type of interference signal enters the radar receiver baseband. Fortunately, this kind of interference is very unlikely to happen because the phase noise between the radar under test and interfering radars is not correlated. The transmitted signal of a neighboring radar is formulated as

$$
s _ { \mathrm { t x i } } ( t ) = A _ { \mathrm { t x i } } \mathrm { c o s } [ 2 \pi f _ { i } ( t + t _ { 0 } ) + \pi k _ { i } ( t + t _ { 0 } ) ^ { 2 } ] ,\tag{5}
$$

where $t _ { 0 }$ is the time offset with the radar under test as the reference, $A _ { \mathrm { t x i } }$ is the amplitude, $f _ { i }$ is the center frequenc $\scriptstyle \mathrm { { y , } }$ and $k _ { i }$ is the chirp rate for the neighboring radar.

When the transmitted signal of the neighboring radar passes through the receiver of the radar under test, the interfering signal after dechirping is

$$
r _ { i } ( t ) = A _ { i } \mathrm { c o s } [ 2 \pi ( f _ { c } - f _ { i } ) t + \pi ( k _ { r } - k _ { i } ) t ^ { 2 } - 2 \pi k _ { i } t _ { 0 } t + \phi _ { i } ] ,\tag{6}
$$

where $A _ { i }$ and $\phi _ { i }$ are the amplitude and residual phase of the interfering signal, respectively. According to the above equation, the frequency of the interfering signal with respect to time t is

$$
f _ { i } ( t ) = f _ { c } - f _ { i } - k _ { i } t _ { 0 } + ( k _ { r } - k _ { i } ) t .\tag{7}
$$

It can be seen that the above interfering signal is a linear FM signal, which is called incoherent interference. The part of the interfering signal with a frequency below half of the radar receiver sampling frequency is fully sampled, and the rest above it is undersampled.

The total received signal can be considered as the sum of the target signal and the interfering signal, that is, $r ( t ) = r _ { t } ( t ) + r _ { i } ( t )$ , as shown in Figure 1. It is worth mentioning that the power of the target signal is proportional to $R ^ { - 4 }$ while the amplitude of the interference is proportional to $R _ { i } ^ { - a }$ , where a is a factor that describes the multi-path transmission of the interfering signal and $R _ { i }$ is the distance between the interfering radar and the radar under test. Low-intensity incoherent interference signals have little effect on radar performance, and only raise the noise floor. In this work, the intensity of the interfering signal is considered to be stronger than that of the target signal, which makes it difficult to suppress the interference. Therefore, $2 \leq a < 4 .$

![](images/97bfba935d0948c7b709fb5ffcd0cbf9eb7195ab01aa1c0af924cb6ed024b1db.jpg)  
Figure 1. Demonstration of incoherent interference.

## 3. Proposed Approaches

## 3.1. Interference Envelope Detection

Interference envelope detection is the first priority in interference mitigation. The precise location of the interference facilitates the reduction of interference with minimal computational complexity. After discrete-time quantization sampling, the received signal

can be described as $r ( n )$ , where n denotes the nth sample. First, the amplitude information is obtained by taking the modulus of the radar received signal as

$$
A _ { r } ( n ) = | r ( n ) | .\tag{8}
$$

Next, one low-pass finite impulse response filter (LP-FIR) is designed to detect the envelop. The frequency response of the filter is

$$
H ( \omega ) = \sum _ { n = 0 } ^ { K } h _ { n } e ^ { - j n \omega } ,\tag{9}
$$

where K is the order of the filter and $h _ { n }$ is a coefficient of the filter. Thus, the impulse response of the filter can be written as

$$
h ( n ) = \sum _ { i = 0 } ^ { K } h _ { i } \delta [ n - i ] = h _ { n } , 0 \leq n \leq K .\tag{10}
$$

There are many methods that can be used to solve the filter coefficients, such as the window function method and the frequency sampling method [27]. Here, a minimum mean square error (MMSE)-based method is applied to design the filter.

To simplify the design, $h ( n )$ is expected to be even symmetric and the order K is set as an odd number. Hence, the discrete-time Fourier transform (DTFT) of $h ( n )$ can be rewritten as

$$
H ( \omega ) = e ^ { - j \omega ( N + 1 ) / 2 } \sum _ { n = 0 } ^ { ( K + 1 ) / 2 } h _ { n } { \cos } \Bigg ( \omega \bigg ( \frac { K + 1 } { 2 } - n \bigg ) \Bigg ) ,\tag{11}
$$

According to the above equation, the phase response of the filter is $\phi ( \omega ) = e ^ { - j \omega ( K + 1 ) / 2 }$ Thus, a desired filter $H _ { d } ( \omega )$ can be predefined by combining the phase response $\phi ( \omega )$ with a desired amplitude response. The design of the filter can then be further expressed as an MMSE problem:

$$
\operatorname* { m i n } _ { h ( n ) } \biggl ( E ( \omega ) = \int _ { - \pi / 2 } ^ { \pi / 2 } \mid H ( \omega ) - H _ { d } ( \omega ) \mid ^ { 2 } d \omega \biggr ) .\tag{12}
$$

The above problem is minimized by applying the partial derivative of $E ( \omega )$ with respect to $h ( n )$ to obtain the solution,

$$
h ( n ) = \int _ { - \pi / 2 } ^ { \pi / 2 } \cos ( n \omega ) H _ { d } ( \omega ) d \omega .\tag{13}
$$

Because the frequency of the interference envelope is low, the normalized cutoff frequency of the filter is set to 0.2, the passband normalized frequency is 0.005, the order of the filter is set to 19, and a filter coefficient vector is designed: $h ( n ) = 0 . 0 1$ ∗ [0.59, 1.08, 1.91, 2.99, 4.25, 5.61, 6.94, 8.10, 8.97, 9.43, 9.43, 8.97, 8.10, 6.94, 5.61, 4.25, 2.98, 1.91, 1.08, 0.59]. The amplitude response of the filter is shown in Figure 2.

Applying the designed filter to the amplitude sequence, the envelope $A ( n )$ can be obtained:

$$
A ( n ) = \sum _ { k = 0 } ^ { N - 1 } h ( k ) A _ { r } ( n - k ) ,\tag{14}
$$

where N is the length of the received signal.

![](images/dabecae4765b6b28ea01e7707f364204f18f6d42aba0394c2393cdbf99411cd4.jpg)  
Figure 2. The amplitude response of the designed filter.

## 3.2. Generating Missing Data for Interference Regions

The method for detecting of the interference envelope described above applies to all the received signals. Next, it is necessary to determine whether there is interference in the received signal. Because the target echo signals are superimposed as complex sine waves, the mean and maximum values of the echo amplitude do not differ very much. However, according to a large number of experiments, the maximum value of the interfering signal amplitude is at least three times larger than the mean value of the echo amplitude; thus, the presence of interference is determined by

$$
\mathrm { l a b e l } _ { \mathrm { i n t e r } } = \left\{ \begin{array} { l l } { 1 } & { \operatorname* { m a x } ( | A ( n ) | ) > 3 * \operatorname { m e a n } ( | A ( n ) | ) , } \\ { 0 } & { \mathrm { o t h e r w i s e } . } \end{array} \right.\tag{15}
$$

In addition, the $\mathrm { l a b e l _ { i n t e r } }$ label indicates whether the proposed data interpolation algorithm is stopped or started, reducing the processing complexity. Then, the nth received signal sample is further determined as either an affected or unaffected sample according to the following equation:

$$
z ( n ) = { \left\{ \begin{array} { l l } { 1 } & { { \mathrm { l a b e l } } _ { \mathrm { i n t e r } } \& { | A ( n ) | } > \beta * { \mathrm { m e a n } } ( | A ( n ) | ) , } \\ { 0 } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{16}
$$

where $\beta$ is a parameter that depends on the power of the interference.

The interfering areas are then set to be missing data:

$$
y ^ { * } ( n ) = { \left\{ \begin{array} { l l } { 0 } & { z ( n ) = 1 , } \\ { r ( n ) } & { z ( n ) = 0 . } \end{array} \right. }\tag{17}
$$

In keeping with the above equations, Figure $^ 3$ presents the detected interference envelope and the received signal with missing data. As can be seen from the plots, the proposed method is able to effectively detect four interference regions and accurately identify the affected samples. As plotted in Figure 4, in the absence of interference the proposed approach accurately sets $\mathrm { l a b e l } _ { \mathrm { i n t e r } }$ as $0 ,$ the received signal is identified as the target signal, and no further interference detection or mitigation is required.

![](images/24c544b8cd21fabc9529fba9fc490ba2ede4ece13893582c69ba3dac3bb35269.jpg)  
(a)

![](images/c99133abf5de51f99f6311f3e4f81be7d0ea8f560582273d518086b14c8338e4.jpg)  
(b)

![](images/23a0a7db0472ac0b67524eeaaae79c7f7a43334dadd1c67a39e5bdf096066694.jpg)  
(c)

![](images/96f8328070ac3bb7f33e8a04134e46f9c06f64e89c916bf9194fac0e0f6bcbab.jpg)  
(d)  
Figure 3. In the presence of interference $( \mathrm { l a b e l _ { \mathrm { i n t e r } } } = 1 )$ : (a) the real part of the received signal; (b) the amplitude of the received signal; (c) the interference envelope detected by LPF; and (d) the received signal containing the affected samples. The dashed line in the subplots indicates the mean value of the corresponding signal.

![](images/237aba93ca18cdcf7fd439682f8ea96f4e4ec864cf8ed7b4f66ccff7a7ac2fcf.jpg)  
(a)

![](images/ecb49822ee2e0a90310de8f710a1b0d00fbb8c343992c7c853e36aa4e4c6be5f.jpg)

(b)  
![](images/98d6258815d3f934b92b539d76a6201a27908829e10809a054e9730ab24daf80.jpg)  
(c)

![](images/b61baf83dad4ea91c13c6bcd799d4bbfefffa6d72ac7edd6521b9714419be722.jpg)  
(d)  
Figure 4. In the absence of interference $( \mathrm { l a b e l } _ { \mathrm { i n t e r } } = 0 )$ : (a) the real part of th received signal; (b) the amplitude of the received signal; (c) the echo envelope detected by LPF; and (d) the received signal that does not contain affected samples. The dashed line in the sub-figures indicates the mean value of the corresponding signal.

## 3.3. Data Interpolation Using L1 Norm Least Squares Method

Suppose the length of a signal $y ( n )$ is $N ;$ then, the M-point $( M \geq N )$ inverse DFT of the signal $y ( n )$ is defined as follows:

$$
\mathbf { y } = \mathbf { W } \mathbf { x } ,\tag{18}
$$

where

$$
\mathbf { W } = \frac { 1 } { M } \left[ \begin{array} { c c c c } { 1 } & { 1 } & { \hdots } & { 1 } \\ { 1 } & { e ^ { \frac { j 2 \pi } { M } } } & { \hdots } & { e ^ { \frac { j ( M - 1 ) 2 \pi } { M } } } \\ { \vdots } & { \vdots } & { } & { \vdots } \\ { 1 } & { e ^ { \frac { j ( N - 1 ) 2 \pi } { M } } } & { \hdots } & { e ^ { \frac { j ( N - 1 ) ( M - 1 ) 2 \pi } { M } } } \end{array} \right] ,
$$

$\mathbf { y } = [ y ( 0 ) , y ( 1 ) , \cdot \cdot \cdot , y ( N - 1 ) ] ^ { \mathsf { T } }$ , and the DFT coefficients $\mathbf { x } = [ x ( 0 ) , x ( 1 ) , \cdot \cdot \cdot , x ( M - 1 ) ] ^ { \mathsf { T } }$ Therefore, the DFT coefficient is expressed as

$$
\begin{array} { r } { \mathbf { x } = \mathbf { W } ^ { \mathsf { H } } \mathbf { y } , } \end{array}\tag{19}
$$

with

$$
\begin{array} { r } { \mathbf { W } ^ { \mathsf { H } } = \left[ \begin{array} { c c c c } { 1 } & { 1 } & { \cdots \cdots } & { 1 } \\ { 1 } & { e ^ { \frac { - j 2 \pi } { M } } } & { \cdots \thinspace } & { e ^ { \frac { - j ( N - 1 ) 2 \pi } { M } } } \\ { \vdots } & { \vdots } & { \vdots } \\ { 1 } & { e ^ { \frac { - j ( M - 1 ) 2 \pi } { M } } } & { \cdots \thinspace } & { e ^ { \frac { - j ( M - 1 ) ( N - 1 ) 2 \pi } { M } } } \end{array} \right] , } \end{array}
$$

and $\mathbf { W } \mathbf { W } ^ { \mathsf { H } } = \mathbf { I } .$

In the above discussion the target signal is in the form of a complex sine wave, and is therefore sparse in the DFT domain. Thus, the problem of missing data imputation can be formulated with the L1 norm as

$$
\begin{array} { r } { \frac { \mathrm { a r g m i n } } { \mathbf { \boldsymbol { x } } } \quad \| \mathbf { \boldsymbol { x } } \| _ { 1 } , } \\ { \mathrm { s . t . } \quad \mathbf { \boldsymbol { y } } ^ { * } = \mathbf { \boldsymbol { z } } ( \mathbf { \boldsymbol { W } } \mathbf { \boldsymbol { x } } ) , } \end{array}\tag{20}
$$

where y<sup>∗</sup> = [y<sup>∗</sup>(0), y<sup>∗</sup>(1), · · · , y<sup>∗</sup>(N − 1)]<sup>T</sup>, and z = [z(0), z(1), · · · , z(N − 1)]<sup>T</sup>.

The target signal with missing data can be reconstructed by minimizing the objective function:

$$
J ( \mathbf { x } ) = \frac { 1 } { 2 } \| \mathbf { y } ^ { * } - \mathbf { z } ( \mathbf { W } \mathbf { x } ) \| _ { 2 } ^ { 2 } + \lambda \| \mathbf { x } \| _ { 1 } ,\tag{21}
$$

where λ is the parameter for the L1 norm term.

The above object function can be further rewritten as

$$
\begin{array} { r } { \begin{array} { c } { \arg \operatorname* { m i n } \quad J ( \mathbf { x } ) , } \\ { \mathbf { x } } \\ { \mathbf { s . t . } \quad \mathbf { x - v } = 0 , } \end{array} } \end{array}\tag{22}
$$

where v is a new variable vector.

Using the augmented Lagrangian method, the above problem is formulated as

$$
L _ { A } ( \mathbf { x } , \lambda , \mu ) = J ( \mathbf { x } ) + \lambda ( \mathbf { x } - \mathbf { v } ) + \frac { \mu } { 2 } \| \mathbf { x } - \mathbf { v } \| _ { 2 } ^ { 2 } ,\tag{23}
$$

where $\mu \geq 0$ is a penalty parameter. ADMM is applied to perform minimization with respect to each of x and v to obtain the following iterations:

$$
\begin{array} { r } { \displaystyle \mathbf { x } _ { k } = \arg \operatorname* { m i n } _ { \mathbf { x } } \lambda \| \mathbf { x } \| _ { 1 } + \frac { \mu } { 2 } \| \mathbf { x } - \mathbf { v } _ { k } - \mathbf { d } _ { k } \| _ { 2 } ^ { 2 } , } \\ { \displaystyle \mathbf { v } _ { k } = \arg \operatorname* { m i n } _ { \mathbf { v } } \frac { 1 } { 2 } \| \mathbf { y } ^ { * } - \mathbf { z } ( \mathbf { W } \mathbf { x } _ { k } ) \| _ { 2 } ^ { 2 } + \frac { \mu } { 2 } \| \mathbf { x } _ { k } - \mathbf { v } - \mathbf { d } _ { k } \| _ { 2 } ^ { 2 } , } \\ { \mathbf { d } _ { k + 1 } = \mathbf { d } _ { k } - ( \mathbf { x } _ { k } - \mathbf { v } _ { k } ) , } \end{array}\tag{24}
$$

where k is the iteration number and ${ \bf d } _ { k }$ is an intermediate variable vector.

First, minimization with respect to x is implemented using a soft thresholding:

$$
\mathbf { x } _ { k } = \operatorname { s o f t } \left( \mathbf { v } _ { k } + \mathbf { d } _ { k } , { \frac { \lambda } { 2 \mu } } \right) ,\tag{25}
$$

where the soft thresholding operation is defined as

$$
\mathrm { s o f t } ( \mathbf { x } , \boldsymbol { \omega } ) = \mathbf { x } \cdot \mathrm { m a x } ( 1 - \boldsymbol { \omega } / | \mathbf { x } | , 0 ) .
$$

Next, minimization with respect to v is a constrained least squares regularization. Because $\mathbf { W } \mathbf { W } ^ { \mathsf { H } } = \mathbf { I } ,$ , the solution can be simplified as

$$
\mathbf { v } _ { k } = \mathbf { W } ^ { \mathsf { H } } ( \mathbf { y } ^ { * } - \mathbf { z } ( \mathbf { W } \mathbf { x } _ { k } ) ) .\tag{26}
$$

Finally, after convergence of the solution, the estimated received signal is obtained by

$$
{ \widehat { \mathbf { y } } } = \mathbf { W } \mathbf { x } _ { k } .\tag{27}
$$

## 3.4. Implementation Details

Figure 5 summarizes the procedures of the proposed techniques. Each echo is processed one by one, then the DFT-based image focusing algorithm is used to focus the radar target, and finally a radar image without interference contamination is obtained. In the radar image focusing algorithm, the data focus is directed to the the ranging and Doppler domains by applying the Fast Fourier Transform (FFT) method. The vectors $\mathbf { v } _ { k }$ and ${ \bf d } _ { k }$ are set as zero for the first iteration. Because the intensity of radar echoes is small, the parameters in Equation (24) can be set according to the mean value of the radar echoes; specifically, λ can be set to 1 and $\mu$ can be set to be proportional to the inverse of the mean intensity of the received signal. Additionally, the iteration number for missing data imputation can be set as 20, which produces satisfactory performance.

![](images/82a584e5a8a19181b1c44803c54fc4f00e0cd914b6a24ca0b8a51fc79e6393c8.jpg)  
Figure 5. The procedures of the proposed techniques.

## 4. Validation Experiments

In the following experiments, the proposed technique is compared with three stateof-the-art methods. The first approach is one of the simplest ubiquitous signal processing methods, substituting zeros for the interference regions [15]. The second one represents a more advanced signal processing method using a three-level Haar wavelet with the hard thresholding approach [19]. The final comparison is a sparsity-based MCA method that uses DFT and STFT bases to separate the interfering and target signals, respectively [23]. In the following comparison experiments, the parameters of the wavelet-based and MCA-based methods are set according to references [19] and [23], respectively.

Furthermore, both the wavelet-based [19] and MCA-based [23] methods are improved using the proposed interference envelop detection. Specifically, based on the results of our proposed interference envelope detection method, only the signals in the interference regions are replaced by the outputs of the wavelet and MCA methods.

The comparisons are divided into three groups: stationary interference experiments, dynamic interference experiments, and real radar interference experiments. The first two types of experiments are implemented by simulations. In the following experiments, both the radar under test and the interfering radar are static and the targets are moving. For the stationary interference experiments, the timing between the victim and interfering radars is synchronized, and the jamming appears in the same area of the received signal. In practice, timing synchronization between radars rarely occurs due to relative motion between the radar under test and the interfering radar, making dynamic interference common. As a result, interference appears in different regions in the received signal of the radar under test. Due to the constraints of the experimental conditions, the radar senors in the described experiments are static; however, the timing between the victim and interfering radars is set asynchronously in order to simulate dynamic interference.

Additionally, thermal noise is added to the simulated signals. The power of the noise was calculated as $\mathrm { P _ { n o s i e } } = \kappa T _ { e } B$ , where κ is Boltzman’s constant, T<sub>e</sub> is the noise temperature, and B is the bandwidth of the radar receiver.

In the case of one-dimensional signals, the signal to interference plus noise ratio (SINR) is used to objectively evaluate the performance of interference suppression. However, for two-dimensional radar images, the radar target is focused through two dimensional range and Doppler domains. Therefore, the peak intensity of the target to interference plus noise ratio (PTINR) is defined here as an objective evaluation index for interference mitigation. Using the peak intensity of the focused target, the PTINR is defined as

$$
\mathrm { P T I N R } = \frac { \mathrm { P _ { t a r g e t } } } { \mathrm { P _ { i n t e r f e r e n c e } + P _ { n o i s e } } } ,\tag{28}
$$

where $\mathrm { P _ { t a r g e t } }$ is the peak intensity (power) of the focused target and $\mathrm { P _ { i n t e r f e r e n c e } }$ is the power of the interference.

In addition, the subjective evaluation of radar images is mainly based on the quality of the focused target, sidelobes of the focused target, noise floor level, and residual interference distribution as comparative details.

## 4.1. Simulations

Table 1 provides the simulation parameters for the incoherent interference experiments. Two interfering sources are developed with different start frequencies and chirp rates. The distances of the two interfering sources are 30 m and 50 m from the radar under test, respectively. All the radar sensors are active at the same time. The RCS is 1 $\mathrm { m } ^ { 2 }$ and $3 \mathrm { m } ^ { 2 }$ for two radar targets at 15 m and 30 m, respectively. The target located at 15 m is moving at 5 m/s, while the other target is static. As shown in Figure 6, there are four interference regions present in the received signal.

Figure 7 illustrates the comparative stationary interference experiments. According to Figure $^ { 7 } \mathsf { a } ,$ the stationary interference is distributed on the axis of zero velocity of the focused image, causing the second target to be completely swamped by the large amount of strong noise generated on this axis. Traditional signal processing-based methods such as the ANC and wavelet-based methods are able to suppress the interfering signal to a certain extent. However, the interfering signal is much stronger than the target signal, making it difficult to suppress the interference by traditional signal processing methods, as shown in the plots. Figure 7c illustrates that the wavelet-based approach has difficulty suppressing this strong interference. Using the proposed interference envelope method, the improved wavelet-based method does not perform better; see Figure 7d. This means that the reference regions have not been successfully recovered. Although the MCA method provides slightly better results (Figure 7e), there is a considerable amount of interference energy left in the zero velocity axis, resulting in failure to detect the second radar target. After introducing the proposed interference envelope detection method to improve the MCA method, both targets are successfully recovered and the interference signal energy is more effectively eliminated, as shown in Figure 7f. Figure 7g shows that the simple zero-setting method avoids the interfering signal. However, due to the loss of the target signal in the interfering regions, it leads to strong sidelobes in the focused image. According to Figure 7h, the proposed method produces a promising focused image that is very close to the ground truth. In many real-world vehicle scenarios, the primary and interfering radars have relative motion, producing dynamic interference. Compared with stationary interference, the interference energy from dynamic interference is distributed in different areas on the focused image; see Figure 8a. As the interference energy is distributed in different regions of the image, the interference intensity is relatively lower, and the different interference suppression algorithms consequently have better performance for dynamic interference suppression, as shown in Figure 8. Similarly, the proposed interference envelope detection approach greatly improves the performance of the MCA method; see Figure 8f. Again, as illustrated in Figure 8h, the proposed approach produces the most focused radar image.

Table 1. Simulation parameters for interference experiments.
<table><tr><td>Radars</td><td>Parameters</td><td>Values</td></tr><tr><td rowspan="2">Common parameters</td><td>Bandwidth Sampling rate</td><td>500 MHz</td></tr><tr><td>Chirp number</td><td>10 Msps 128</td></tr><tr><td rowspan="3">Radar under test</td><td>Start frequency</td><td>77 GHz</td></tr><tr><td>Chirp duration</td><td></td></tr><tr><td>Chirp rate</td><td>51.2 μs  $9 . 7 6 \times 1 0 ^ { 1 2 } \mathrm { H z } / s$ </td></tr><tr><td rowspan="3">Interferer 1</td><td>Start frequency</td><td>77.7 GHz</td></tr><tr><td>Chirp duration</td><td>25.6 μs</td></tr><tr><td>Chirp rate</td><td> $1 . 9 5 \times 1 0 ^ { 1 3 } \mathrm { H z } / s$ </td></tr><tr><td rowspan="3"></td><td>Distance</td><td>30 m</td></tr><tr><td>Start frequency Chirp duration</td><td>76.9 GHz</td></tr><tr><td></td><td>17.07 μs</td></tr><tr><td rowspan="3">Interferer 2</td><td>Chirp rate</td><td> $2 . 9 3 \times 1 0 ^ { 1 3 } \mathrm { H z } / s$ </td></tr><tr><td>Distance</td><td></td></tr><tr><td></td><td></td></tr></table>

![](images/0f8177361f9b6bf216cb7dda2d8e50c612e2f0afa64cd34326243d6a6927980d.jpg)

(a)  
![](images/abab57be75cd319770954fce802a184516fe4bf21c43d7c1828f6824d76a0a33.jpg)  
(b)  
Figure 6. The received signal with interference: (a) the real part of the received signal and (b) the magnitude of the received signal. The regions marked by circles in (b) are the envelopes in which interference appears.

![](images/8530f7016f3061556db32b31907006ffe38d85cb053c8fe18591768cadd1c4c7.jpg)  
(a)

![](images/4b57df6a0c19e2fcc3a96fd8bde74bdb1cfce56fd7176d4cb7f1c23096aee281.jpg)  
(b)

![](images/ba6eae22d959134b24fa415276d5714cea7878912a419c41c508822aae07b9ad.jpg)  
(c)

![](images/4f568593ea3c325e2622ca065f7ffc49c2fbb2ab86be11a6a6f1d81a7e0e46ca.jpg)  
(d)

![](images/bcd798f3b416b02c410e700392324f4694cd82f20ea4351336f4da784b43a203.jpg)  
(e)

![](images/e708699b503e98e948be36a0ba1656352063e09fc44d502114c9755e9743f8e6.jpg)  
(f)

![](images/cf63234d7bfa3b04e89fc6f2b5f13ed35db3c8998e7b08ba4f7d4c75d3e1f57c.jpg)  
(g)

![](images/c7bb7542896986d9afabc97f6ce7bd8f442285cbf21b7327654db94e7635ea64.jpg)  
(h)  
Figure 7. Comparisons on stationary interference simulations. (a) Original image; (b) Interferencefree image; (c) Lee et al. [19]; (d) Lee et al. [19] + Proposed interference detection; (e) Uysal [23]; (f) Uysal [23] + Proposed interference detection; (g) Brooker [15]; and (h) The proposed method.

![](images/f9dda012c852a7ff243738f5185fc8bb8b7b6180b1724df969b06d4b676776e9.jpg)  
(a)

![](images/4bf30bb3f9e623c56b87c024b7bbf43ba00f7c371327d2a6f917596a9549b807.jpg)  
(b)

![](images/3da696a30d02e239a50cf40a740ad8a36cb0642a245452715c975aba95b2023a.jpg)  
(c)

![](images/54866224b7684f5fd4dd2efdc4fd8a68fa5d7a43371fef36ca96a9eeb636fe47.jpg)  
(d)

![](images/3baddd16f5feb4747c9dd074e95c1649776afe4878ed1058f6d2d28eac751dab.jpg)  
(e)

![](images/ed8366adff920bfb305eaf0a0a1cf80529b66a40e259b45291c67f4135605503.jpg)

![](images/6edf739fcf8b662dc097c4d944f5e2c457a4be36a690c1bb5a2a56c31d41a3ca.jpg)  
(g)

(f)  
![](images/0bfbab20fb1f7523e9a36f124fd14ca797a114f255f8d5b000ed2553a33b7125.jpg)  
(h)  
Figure 8. Comparisons on dynamic interference simulations. (a) Original image; (b) Interferencefree image; (c) Lee et al. [19]; (d) Lee et al. [19] + Proposed interference detection; (e) Uysal [23]; (f) Uysal [23] + Proposed interference detection; (g) Brooker [15]; and (h) The proposed method.

Comparisons of object evaluation were conducted as well. The results are reported in Table 2. The larger PTINRs along with the absence of ghost targets indicate the better suppression performance of the associated method. The proposed method has the best performance index in the simulated experiments. Because the static target appears on the zero velocity line axis of the focused image, and is therefore covered by strong interference energy, its PTINR value is −6.1 dB. The wavelet-based method and MCA-based method have limited improvement on this index, while the proposed method can realize an improvement of up to 19.1 dB, a total improvement of 25.2 dB, which is beneficial for subsequent target detection and tracking.

Table 2. Comparisons of PTINRs via simulations. The first number in each term is the result of stationary interference and the second number is the result of dynamic interference.
<table><tr><td>Methods</td><td>Target 1 (dB)</td><td>Target 2 (dB)</td></tr><tr><td>Original image</td><td>25.6, 29.8</td><td>-6.1, 6.2</td></tr><tr><td>Ground truth without interference</td><td>36.8</td><td>25.5</td></tr><tr><td>Lee et al. [19]</td><td>24.9, 30.2</td><td>-3.3, 14.9</td></tr><tr><td>Lee et al. [19] + the proposed</td><td>26.5, 30.8</td><td>-2.7, 20.3</td></tr><tr><td>interference detection Uysal [23]</td><td>26.4, 28.9</td><td>3.1, 12.5</td></tr><tr><td>Uysal [23] + proposed</td><td>28.6, 35.8</td><td>17.7,23.7</td></tr><tr><td>interference detection</td><td></td><td></td></tr><tr><td>Brooker [15] The proposed method</td><td>19.2, 19.3 31.2, 36.4</td><td>15.1, 23.1</td></tr><tr><td></td><td></td><td>19.1, 24.2</td></tr></table>

## 4.2. Real Radar Field Experiments

As shown in Figure 9, real radar interference experiments were conducted using two Texas Instruments AWR1642 mm wave radars and an electric bicycle traveling at approximately 5 m/s forward or backward relative to the radar under test. The distance of the interfering radar was 4 m. The experiment parameters are presented in Table 3.

Figure 10 demonstrates the collected radar data with strong interference. The signal of the sine wave in the plot is the radar target signal, and the signal that changes suddenly and quickly with high intensity is the interfering signal. This coincides with the theoretical derivation in Section 2.

Table 3. Radar parameters used for measurements.
<table><tr><td>Radars</td><td>Parameters</td><td>Values</td></tr><tr><td>Common parameters</td><td>Start frequency Bandwidth</td><td>77 GHz 547.5 MHz</td></tr><tr><td>Radar under test</td><td>Chirp number Sampling rate Chirp duration Chirp rate</td><td>128 10 Msps 36.5 μs 1.5 × 1013 Hz/s 18.25 μs</td></tr><tr><td>Interferer</td><td>Chirp duration Chirp rate Sampling rate Distance</td><td>3.0 × 1013 Hz/s 6.25 Msps 4m</td></tr></table>

![](images/bfe6e62650442975d9af05ec3cb13ebffdcd2ceebed1f173a22e86e419602866.jpg)  
Figure 9. Real radar field experiments.

![](images/a87ba4ef6164ebfb013b75b032e140b5d12afab300e19e71efb161a072a715fa.jpg)

![](images/6135891fc99582666ee7709921b9241320284090025756a8850480a058017622.jpg)  
Figure 10. The received signal during the measurement experiments: the plots on the top row is the real part of the signal, and the plots on the bottom row is the magnitude of the received signal.

Figure 11 presents the comparison results of the real radar interference experiments. The stationary targets are distributed on the axis of zero velocity of the focused image, however the moving target is not visible due to strong interference. Compared to the other approaches, the proposed method has the best performance. As shown in Figure 11a, the strong interference energy is distributed over the focused radar image. The main reason for this is that the interfering signal does not repeat at the same location in each received signal with dynamic interference. Compared to the simulated results, the zeroing method produces stronger sidelobes on the focused image, which leads to difficulty in distinguishing between real moving targets; see Figure 11g. The evaluation results reported in Table 4 indicate that the proposed method has the best performance index in the real radar experiments.

![](images/ae7c178273681816f092a7ce8ce198bbc9d6e097b65dbe627c6cb3e36cee61dc.jpg)  
(a)

![](images/7a582a44fc5a72e39b983b1f401afa607e0b55af95f6e6c5304c5d4023fb339e.jpg)  
(b)

![](images/fa16a8d4b9954f6ddd4eab2a6f10a7f0504d35f3673cd7e4b9417f7f50cbc0f6.jpg)  
(c)

![](images/285922153374d1e460a23ad4ae0779bf366108237cda38d0c31b445ae001fb5a.jpg)  
(d)

![](images/dead5af96a23e7eee71c39421e55797940f1e6cb9dcde137830c880c0d1ab61b.jpg)  
(e)

![](images/33e39e7b037cb5275159e6ed4abe785d74f14fd03f950bd052758ff14f5553d8.jpg)  
(f)

![](images/d203c47f0a68233b0d1990b3485d1fceea161ab55574dff2c3ce82d0184cb68e.jpg)

![](images/d933f81f8f34771112790299136b300b31abc1c25c7264a87a6e261f765cad37.jpg)  
(h)  
Figure 11. Comparisons using real radar data. (a) Original image; (b) Interference-free image; (c) Lee et al. [19]; (d) Lee et al. [19] + Proposed interference detection; (e) Uysal [23]; (f) Uysal [23] + Proposed interference detection; (g) Brooker [15]; and (h) The proposed method.

Table 4. Comparisons using measured real radar data.
<table><tr><td>Methods</td><td>PTINRs (dB)</td><td>Ghost Targets</td></tr><tr><td>Original image</td><td>5.1</td><td>Yes</td></tr><tr><td>Ground truth</td><td>24.6</td><td>No</td></tr><tr><td>Lee et al. [19]</td><td>5.9</td><td>No</td></tr><tr><td>Lee et al. [19] + the proposed interference detection</td><td>10.3</td><td>Yes</td></tr><tr><td>Uysal [23]</td><td>3.4</td><td>Yes</td></tr><tr><td>Uysal [23] + the proposed interference detection</td><td>15.7</td><td>No</td></tr><tr><td>Brooker [15]</td><td>15.1</td><td>Yes</td></tr><tr><td>The proposed method</td><td>21.2</td><td>No</td></tr></table>

## 5. Discussion

## 5.1. Beyond Sparsity-Based Methods

Certain radar targets have a large radar cross-section (RCS), such as metal buildings on the side of a road, while others have a small RCS, such as pedestrians. All in all, the dynamic range of the received signal is large. Therefore, it is difficult to extract weak targets in an interference environment. Unfortunately, sparsity-based methods have a general drawback in that they tend to remove weak signals as noise. As shown in Figures 7, 8 and 10, the traditional sparsity-based method [23] can only recover strong targets, and loses weak targets. The proposed method, although retaining a sparse framework, proposes an interference detection method that enables signal recovery only for the region where the interference occurs, thus effectively maintaining the signal energy and suppressing the interference signal at the same time.

## 5.2. Computational Complexity

The complexity of the interference suppression algorithm needs to be as small as possible in order to be suitable for the signal processor of existing automotive millimeter wave radar chips. Therefore, interference-contaminated region detection-based methods have advantages in terms of computing complexity. Zero-based detection methods simply set the interference-contaminated regions to zero, and thus have the least complexity. However, the focused target obtained with such methods loses information and has many sidelobes.

Except for the zeroing method, the wavelet-based method [19], the MCA-based method [23], and the proposed technique are all transform-based approaches, meaning that the computational complexity depends mainly on forward and inverse transformation. In general, the wavelet-based method has the lowest complexity, followed by the proposed method. The MCA method has the highest computational complexity due to the use of both STFT and DFT [23].

## 5.3. What Is the Percentage of Samples Affected by Interference for Which the Proposed Technique Remains Valid?

In the proposed technique, a greater proportion of interfering samples produce fewer effective received samples, thereby reducing range resolution and signal-to-noise ratio. Therefore, we conducted experiments to investigate the performance of the proposed technique with respect to the differing percentage of interfering samples. According to Figures 12 and 13, when the percentage of interfering samples is below 50%, the performance of the proposed method is satisfactory. The interference signal is generally in the shape of a burst in the time domain, and rarely occupies most of the received signal, allowing the proposed method to cope with the interference in most cases.

![](images/104529904d5d9105ca3fe6126822602aad639cb4c4fcfa2c323d76ffe5ff9152.jpg)

![](images/76ba24cbcf5971fa5373d61d12a68bbe9e99fd775ddcb7fddf85d5184dbeeb68.jpg)

![](images/8cbeba4dbafe5ab2f71046b12912d44d7a3815f74edac39e62483aaed375f33c.jpg)

![](images/ea9bd402688553582cfa31ca27af7fbe3cddc9cb391c8aa47b2664be5ceb4501.jpg)

![](images/29ee134b9b38c7f3a9de2eb188eb87d46e8d28a46f37da083c1e29b3b3e02be1.jpg)

![](images/618f3cf1cab87d333ec1dd4b73e2acdf3529daa3a67aefcb2130e110203f88ea.jpg)

![](images/b3478c60395c5245b797097e837e3cfacd9e797a2d924b79f6ce4bfbd2e34463.jpg)

![](images/3bac3493ee4efa561c810e9edb362c5636b255f504ad152a5468bc65aedcdf02.jpg)

![](images/e57a21ac9d762df44c9d34de7d97c300bf9bc21ff4773db68c47d73d2352727a.jpg)

![](images/f4469167a5a4f2d1ad343326f08e0c8e9386f26cd0425d6b12d8e7f3d73b6685.jpg)

![](images/7e4a99979de23484d02a4bfeaaacdc350560c0959210a04e4e6833e74893d965.jpg)

![](images/7381244dabd75cc3640cd0b8fb50f3e8d6c378ed7e81d223315dd629a1678ef1.jpg)  
Figure 12. The performance of the proposed technique with respect to different percentages of interfering samples.

![](images/4da5ff2c49820e7644f148f1ad58a818dfe6284aff6708e72c83efcac4672aad.jpg)

![](images/2ff66c4f7b95eb3b7b4fe4fcfff5f3c69c20c0439b620718f03c0e7e45f8eacb.jpg)

![](images/6481e81c29133bcaf9a70f9e3989cd76053fba6462632cc5a3e7de71737672a3.jpg)

![](images/f13cb1d40d113adfccbf3f7d529ab35cdfeea536463ee86c889129339d975b7f.jpg)

![](images/ad81e81f9284d342de0a1812237fdc93744a3f2f3dbf4fc76e05ecacac8df8d0.jpg)

![](images/c3f8c4e8617e67def0f91783b6897c7813eb696403f76504a270a51620bc221e.jpg)

![](images/9b6bc52cf955be146ce2b0efd701f731faed855555bb0a127d9919e68da75d71.jpg)

![](images/d3b99fbba690016bc9d274fff43170d7d8d392f0bf03cdd1512c3f9517fee8d5.jpg)

![](images/ffcd16815853ba9bf7e64b6549089718175920202a75ecb8624bac8b39cd97fb.jpg)

![](images/ddd66ba9b0be35a8f872f7d8e437856ea978efaa9c27809955922eb118dd6952.jpg)

![](images/7004e50b210d0935d6d3c4f519234506f285352e17ca883760d1a3378d2a70c0.jpg)

![](images/4a415e80a7e6eee975abe8e2b16427d3523db18145c1bbb1c0c9237b60876889.jpg)  
Figure 13. Comparison of range and Doppler profiles in terms of different percentages of interfering samples.

## 6. Conclusions

In this paper, an effective and feasible interference suppression technique is proposed for the currently important and challenging issue of incoherent interference between automotive FMCW radars. A detailed derivation of the processing of incoherent interference signals is presented. A precise interference envelope detection method is proposed based on a well-designed low-pass filter. This method can avoid interference suppression in cases where the signal is received without interference, thereby reducing the required amount of computation. This work considered the interference problem as a missing radar data problem; the radar target signal is superimposed in complex sinusoidal waves with good sparse characteristics in the DFT domain. Thus, the radar target signal polluted by the incoherent interference can be successfully recovered based on the L1 norm least squares method. Using the proposed method, the radar target can be perfectly focused even in cases of strong interference. Moreover, two current state-of-the-art methods, namely, the wavelet-based and MCA-based methods, are improved when using the proposed interference envelope detection method. Extensive experiments demonstrate the promising performance of the proposed techniques.

This work shows the effectiveness of suppressing interference in the range and Doppler domains. However, this work does have limitations; in particular, it does not investigate interference in spatial multi-channel data. Our future work will focus on interference reduction for spatial multi-channel radar data.

Author Contributions: Conceptualization, Z.X.; methodology, Z.X. and Y.W.; software, Y.W.; validation, S.X. and Y.W.; experimental analysis, S.X.; data collection, Z.X., S.X. and Y.W.; writing—original draft preparation, Y.W.; writing—review and editing, Z.X.; supervision, Z.X. All authors have read and agreed to the published version of the manuscript.

Funding: This work was supported by the National Natural Science Foundation of China (Grant number 42005100) and by the Nantong Science and Technology for Social and Livelihood Key Project (Grant number MS22022016).

Data Availability Statement: Not applicable.

Acknowledgments: Although this work was supported by two projects, the remaining costs of the project did not cover article processing charges for the paper. The editorial team of Remote Sensing has been very supportive and helpful. The authors would like to give special thanks to Nancy Yang, Marko Mladenovic, Elenor Wang and the others editors for their generous support, which enabled the paper to be published. Your journal’s timely help made us feel sunshine and warmth in the midst of much-needed help, and and we will continue to do meaningful and interesting works and apply for relevant grants in return for our scientific journal and the kind people and well-wishers around the world. In addition, the authors would like to express their sincere gratitude to the editors and reviewers whose insightful comments have further enhanced the quality of the paper.

Conflicts of Interest: The authors declare no conflict of interest.

## References

1. Gardill, M.; Schwendner, J.; Fuchs, J. An Approach to Over-the-air Synchronization of Commercial Chirp-Sequence Automotive Radar Sensors. In Proceedings of the 2020 IEEE Topical Conference on Wireless Sensors and Sensor Networks (WiSNeT), San Antonio, TX, USA, 26–29 January 2020; pp. 46–49. [CrossRef]

2. Jasteh, D.; Hoare, E.G.; Cherniakov, M.; Gashinova, M. Experimental Low-Terahertz Radar Image Analysis for Automotive Terrain Sensing. IEEE Geosci. Remote. Sens. Lett. 2016, 13, 490–494. [CrossRef]

3. Xu, Z.; Baker, C.J.; Pooni, S. Range and Doppler Cell Migration in Wideband Automotive Radar. IEEE Trans. Veh. Technol. 2019, 68, 5527–5536. [CrossRef]

4. Patole, S.M.; Torlak, M.; Wang, D.; Ali, M. Automotive radars: A review of signal processing techniques. IEEE Signal Process. Mag. 2017, 34, 22–35. [CrossRef]

5. Alland, S.; Stark, W.; Ali, M.; Hegde, M. Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research. IEEE Signal Process. Mag. 2019, 36, 45–59. [CrossRef]

6. Tovar Torres, L.L.; Steiner, M.; Waldschmidt, C. Channel Influence for the Analysis of Interferences Between Automotive Radars. In Proceedings of the 2020 17th European Radar Conference (EuRAD), San Antonio, TX, USA, 26–29 January 2020; pp. 266–269. [CrossRef]

7. Torres, L.L.T.; Roos, F.; Waldschmidt, C. Simulator Design for Interference Analysis in Complex Automotive Multi-User Traffic Scenarios. In Proceedings of the 2020 IEEE Radar Conference (RadarConf20), Florence, Italy, 21–25 September 2020; pp. 1–6. [CrossRef]

8. Hua, X.; Ono, Y.; Peng, L.; Xu, Y. Unsupervised Learning Discriminative MIG Detectors in Nonhomogeneous Clutter. IEEE Trans. Commun. 2022, 70, 4107–4120. [CrossRef]

9. Rosenberg, L.; Bocquet, S. Non-coherent Radar Detection Performance in Medium Grazing Angle X-Band Sea Clutter. IEEE Trans. Aerosp. Electron. Syst. 2017, 53, 669–682. [CrossRef]

10. Xu, Z.; Shi, Q.; Shi, J.; Wang, H.; Wei, M.; Gao, R.; Shao, Y.; Tao, H. A novel method of mitigating the mutual interference between multiple LFMCW radars for automotive applications. In Proceedings of the IGARSS 2019–2019 IEEE International Geoscience and Remote Sensing Symposium, Yokohama, Japan, 28 July–2 August 2019; pp. 2178–2181.

11. Xu, Z.; Shi, Q. Interference mitigation for automotive radar using orthogonal noise waveforms. IEEE Geosci. Remote Sens. Lett. 2018, 15, 137–141. [CrossRef]

12. Xu, Z.; Shi, Q.; Sun, L. Novel Orthogonal Random Phase-Coded Pulsed Radar for Automotive Application. J. Radars 2018, 7, 364–375. [CrossRef]

13. Uysal, F. Phase-coded FMCW Automotive Radar: System Design and Interference Mitigation. IEEE Trans. Veh. Technol. 2019, 69, 270–281. [CrossRef]

14. Yuan, M.; Xu, Z.; Shi, Q. Wiener filter based automotive millimeter wave radar interference adaptive reduction. J. Electron. Meas. Instrum. 2021, 35, 194–201. [CrossRef]

15. Brooker, G.M. Mutual Interference of Millimeter-Wave Radar Systems. IEEE Trans. Electromagn. Compat. 2007, 49, 170–181. [CrossRef]

16. Neemat, S.; Krasnov, O.; Yarovoy, A. An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain. IEEE Trans. Microw. Theory Techn. 2019, 67, 1207–1220. [CrossRef]

17. Jung, J.; Lim, S.; Kim, J.; Kim, S.C.; Lee, S. Interference Suppression and Signal Restoration Using Kalman Filter in Automotive Radar Systems. In Proceedings of the 2020 IEEE International Radar Conference (RADAR), Washington, DC, USA, 28–30 April 2020; pp. 726–731.

18. Wang, J.; Ding, M.; Yarovoy, A. Matrix-Pencil Approach-Based Interference Mitigation for FMCW Radar Systems. IEEE Trans. Microw. Theory Techn. 2021, 69, 5099–5115. [CrossRef]

19. Lee, S.; Lee, J.Y.; Kim, S.C. Mutual Interference Suppression Using Wavelet Denoising in Automotive FMCW Radar Systems. IEEE Trans. Intell. Transp. Syst. 2021, 22, 887–897. [CrossRef]

20. Jin, F.; Cao, S. Automotive Radar Interference Mitigation using Adaptive Noise Canceller. IEEE Trans. Veh. Technol. 2019, 68, 3747–3754. [CrossRef]

21. Wu, J.; Yang, S.; Lu, W.; Liu, Z. Iterative modified threshold method based on EMD for interference suppression in FMCW radars. IET Radar Sonar Navig. 2020, 14, 1219–1228. [CrossRef]

22. Xu, Z.; Yuan, M. An Interference Mitigation Technique for Automotive Millimeter Wave Radars in the Tunable Q-Factor Wavelet Transform Domain. IEEE Trans. Microw. Theory Techn. 2021, 69, 5270–5283. [CrossRef]

23. Uysal, F. Synchronous and asynchronous radar interference mitigation. IEEE Access 2018, 7, 5846–5852. [CrossRef]

24. Afonso, M.V.; Bioucas-Dias, J.M.; Figueiredo, M.A. Fast image recovery using variable splitting and constrained optimization. IEEE Trans. Image Process. 2010, 19, 2345–2356. [CrossRef]

25. Rock, J.; Roth, W.; Toth, M.; Meissner, P.; Pernkopf, F. Resource-Efficient Deep Neural Networks for Automotive Radar Interference Mitigation. IEEE J. Sel. Top. Signal Process. 2021, 15, 927–940. [CrossRef]

26. International Telecommunication Union. Systems Characteristics of Automotive Radars Operating in the Frequency Band 76–81 GHz for Intelligent Transport Systems Applications; Mobile, Radiodetermination, Amateur and Related Satellite Service; International Telecommunication Union: Geneva, Switzerland, 2018.

27. Kidambi, S. Design of Noise Transfer Functions for Delta–Sigma Modulators Using the Least-pth Norm. IEEE Trans. Circuits Syst. II Express Briefs 2019, 66, 707–711. [CrossRef]