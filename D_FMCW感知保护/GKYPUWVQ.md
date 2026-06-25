# Improved Target Detection Through DNN-Based Multi-Channel Interference Mitigation in Automotive Radar

Shengyi Chen , Marvin Klemp, Jalal Taghia, Uwe Kühnau, Nils Pohl , Senior Member, IEEE, and Rainer Martin , Fellow, IEEE

Abstract— Deep learning methods have triggered significant progress in automotive radar-based object detection and classification. However, with an increasing number of radar sensors on the road, mutual interference is unavoidable since these sensors share the same frequency spectrum. Mutual interference affects the robustness of radar processing schemes and thereby the object detection accuracy. Unlike many recent works which focus on interference mitigation for a single receive channel, this paper proposes a multi-channel mitigation approach and seeks to analyze the effect of mutual interference in a multiple-input multiple-output (MIMO) radar. To this end, we first formulate a general signal model for multi-channel interference scenarios. Then, a novel signal separation neural network is proposed for multi-channel interference mitigation which eliminates the efforts of interference detection. We assess the impact of interference in terms of the reconstruction error, angle estimation error, and the target detection accuracy in both real-world and simulated interference scenarios. It is demonstrated that the proposed neural network can provide superior signal recovery, massively reduces the false-positive rate, and significantly improves the accuracy of object detection even in the presence of severe interference.

Index Terms— Automotive radar, interference mitigation, signal separation, target detection, deep learning.

## I. INTRODUCTION

R<sup>ADAR</sup> <sup>based</sup> <sup>environment</sup> <sup>analysis</sup> <sup>is</sup> <sup>receiving</sup> <sup>increas-</sup>ing attention in advanced driver assistance systems (ADAS) [1], [2]. In contrast to camera and lidar sensors, radar sensors are robust in adverse weather conditions such as snow, heavy rain, as the wavelength of millimeter-wave radar is longer than the particle size of hydrometeors. In order to achieve a 360-degree view, modern vehicles use multiple radar sensors for ADAS functions. However, due to frequency spectrum regulation, most radar sensors share the same frequency spectrum and the probability of mutual interference increases accordingly. Since unexpected interference can either reduce the signal-to-noise ratio (SNR) or create ghost targets [3], the accuracy of target detection can be impeded by interference if no countermeasures are taken.

In order to achieve an efficient sharing of the frequency bands dedicated to automotive radar, cooperative interference mitigation strategies [4], [5] have been proposed. However, additional coordination units are required to imple ment cooperation algorithms which will add extra costs and operating time to the existing radar system. Furthermore, several approaches based on waveform design have been introduced for tackling the interference issue [6], [7]. In [6], a waveform with random phase has been designed, where the consecutively transmitted waveforms are orthogonal to each other. Thus, interference signals can be reduced by matched filtering. A phase-coded frequency-modulated continuouswave (FMCW) and a phase-coded linear-frequency-modulated (LFM) continuous waveform are proposed in [7]. The main challenge for these cooperative interference mitigation strategies and waveform design approaches resides in its coexistence with the chirp sequence modulation radar, a widely used variant of the FMCW radar in automotive radar systems, as well as the older generations of automotive radars such as the continuous-wave (CW) radar.

Besides the cooperative interference mitigation strategies and the waveform design approaches exemplified above, various signal reconstruction algorithms have been developed for solving the interference problem. These signal recovery algorithms are mainly designed to recover four different signal types: the discrete-time beat signal [3], [8], [9], [10], [11], [12], [13], [14], [15], [16], the range profile (obtained after applying the fast Fourier transform (FFT) to fast-time samples in the discrete beat signal) [17], [18], [19], the frequency spectrum obtained after applying the short-time Fourier transform (STFT) to the discrete beat signal [20], and the range-Doppler (RD) spectrum (obtained after applying the second FFT to the range profile in the chirp direction) [17], [21], [22], [23], [24].

For eliminating the interference-contaminated discrete beat signal segments, the zeroing method is employed in [3] where the signal segments disturbed by interference are detected and simply set to zero. However, when the number of disturbed samples becomes large, the zeroing method results in the loss of target information in terms of both phase and amplitude. Different to [3], the autoregressive (AR) model-based method is used in [12] for the discrete beat signal interpolation in the sample positions which are disturbed by interference. An autoencoder was developed in [16] for the reconstruction of disturbed discrete beat signals, where the disturbed samples are detected by an edge detector as in [9] and the proposed autoencoder reconstructs interference-free samples. In general, most of these time-domain signal reconstruction algorithms require a reliable interference detection algorithm that can precisely determine the position of disturbed samples. In [25], a method was presented in which the interference is detected and suppressed by an iterative adaptive thresholding procedure, however, it is difficult to locate interferences which have a similar amplitude as the interference-free signal [13]. The signal strength of disturbed samples may vary largely due to the multi-path propagation and the distance between the interferer and the victim radar.

Similar to the approaches for time-domain signal recovery, the disturbed signal segments in the range profile or in the STFT frequency spectrum can be first detected and then interpolated. In [20], the interference-free signal segments are reconstructed in the STFT frequency spectrum by linear predictive coding (LPC). In [19] a generative adversarial network (GAN) is proposed to recover the interferencefree signal segments in the complex range profile. However, in some cases the signal segments disturbed by interference may spread across the entire STFT frequency spectrum and the range profile, therefore the available interference-free signal segments are not sufficient for these algorithms to provide adequate recovery.

Various deep learning techniques have also been proposed to reconstruct the disturbed RD spectrum [17], [21], [22], [23], [24]. In [17], a convolutional neural network (CNN) is employed for noise suppression in the range profile and the RD spectrum for a single receive channel. However, the target peak values may be distorted in the reconstructed RD spectrum [17]. The resource-efficient and complex-valued variants of CNN have been proposed in [22] and [24], respectively. A convolutional autoencoder is employed in [21] for the reconstruction of the RD spectrum, where the amplitude and phase components of the complex-valued RD spectrum are used as input. However, this approach cannot properly reconstruct the phase information, since the phase component of the target can resemble the phase of the noise (both vary in the same range) and is therefore more difficult for the neural network to acquire. The deep learning approaches have shown their strength in noise suppression in these studies when the amplitude of the target peaks is distinctly greater than the background noise level in the disturbed RD spectrum. However, when the weak target peaks are obscured by the background noise, it may be difficult to recover them directly from the disturbed RD spectrum [13].

In order to increase the resolution of the angle estimation of commercial automotive radar with a low hardware cost and small package size, the multiple-input multipleoutput (MIMO) [26], [27] radar technology has been receiving considerable attention recently. Environment perception using MIMO radar sensors has shown a comparable accuracy [1], [2], [28], [29] in the object detection and classification tasks with the camera- or lidar-based solutions. In [1], a complete processing pipeline was developed for a semantic segmentation of the radar point cloud obtained from measurements of multiple radar sensors. The performance of the object classification is improved in [28] by extracting the features of point cloud clusters from 98 handcrafted feature candidates. Due to the application of the constant false alarm rate (CFAR) algorithm for the extraction of target points, the point cloud returned from the commercial radar sensors is usually sparse which might cause the loss of target information. Most recently, the RadarResNet with one-stage anchor-based detector and a fully convolutional network are proposed in [2] and [30], respectively, for automotive radar object detection using the low-level radar signals, namely the Range-Azimuth-Doppler (RAD) data cube. It should be noted that the impact of mutual interference is not taken into account in the object detection accuracy achieved in these contributions.

The problem of mutual interference involving a single receive antenna has been extensively studied in the literature; yet, the propagation of interference across multiple receive antennas and its impact on the target detection need to be further explored. In this paper, we investigate the mitigation of mutual interference across multiple receive antennas and analyze how the interference affects the accuracy of target detection. The main contributions are summarized as follows:

• We formulate a general signal model for multi-channel interference scenarios.

• Using the above signal model, we create a data set<sup>1</sup> by simulating different types of interference and combining it with an existing data set of interference-free discrete beat signals acquired by a MIMO radar.

• We propose a signal separation neural network for sep arating the interference-free discrete beat signal and the interference. The proposed signal separation neural network can directly reconstruct the interference-free discrete beat signal of multiple receive channels.

• The proposed signal separation neural network is evaluated in terms of signal reconstruction, angle estimation error, and improvement of the target detection accuracy in comparison to state-of-the-art algorithms.

The organization of this paper is as follows. In Section II, the FMCW MIMO radar system model and the signal processing chain are introduced. Section III describes the proposed signal separation neural network for interference mitigation. In Section IV, the performance of the proposed method is evaluated and the influence of interference on the object detection accuracy is investigated. Section V concludes this paper.

## II. FMCW MIMO RADAR SIGNAL MODEL AND SIGNAL PROCESSING CHAIN

## A. Signal Model and Interference

Most commercial automotive radar systems currently use chirp sequence modulation [31]. Considering the time-division multiplexing (TDM) MIMO scheme<sup>2</sup> with M transmitters and N receivers [26], [27], each transmitter sends a sequence of Q chirps, where the active transmit antenna, enumerated by $m ,$ is changed after each single chirp. For an antenna configuration with M transmit antennas and N receive antennas, M N virtual receive channels can be synthesized (i.e., taking the receiver antenna array and placing it at the position of each transmitter antenna) [32, Chapter 3.1.2]. Fig. 1 shows an example of the TDM MIMO technique. The waveform emitted by M transmitters is given by

![](images/61b71c46d6edadb802c7a0cf4eda26bdc35bb6adcf47a5cfba83356cfdb77c76.jpg)  
Fig. 1. An example of TDM MIMO with two transmit antennas (TX) and four receive antennas (RX).

$$
T _ { x } ( t ) = \sum _ { q = 0 } ^ { M Q - 1 } \sum _ { m = 0 } ^ { M - 1 } a _ { q , m } s ( t - \lfloor q / M \rfloor T _ { \mathrm { P R I } } - m T ) ,\tag{1}
$$

where $T _ { \mathrm { P R I } }$ is the pulse repetition interval (see Fig. 1), ⌊·⌋ the floor function, $T$ the chirp duration $( M T ~ \le ~ T _ { \mathrm { P R I } } )$ , q enumerates the transmitted chirps across all transmit antennas, and

$$
a _ { q , m } = { \left\{ \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } q { \mathrm { ~ m o d ~ } } M = m } \\ { 0 , } & { { \mathrm { o t h e r w i s e . } } } \end{array} \right. }\tag{2}
$$

The individual transmit chirp signal with a normalized amplitude is described as

$$
{ s } ( t ) = \mathrm { e } ^ { j \phi ( t ) } \mathrm { r e c t } \bigg ( \frac { t } { T } \bigg ) ,\tag{3}
$$

where $\phi ( t ) = 2 \pi f _ { c } t + \pi \kappa t ^ { 2 }$ is the phase of the local-oscillator, $f _ { c }$ the carrier frequency, $\kappa ~ = ~ B / T$ the chirp rate with B denoting the sweep bandwidth, and rect(·) the square pulse which is one in the interval [0, 1) and zero otherwise.

The q-th chirp of one target’s echo signal at the n-th receiver emitted from the m-th transmitter is delayed by $\tau _ { m , n }$ :

$$
\begin{array} { r } { r _ { q , m , n } ( t ) = \hphantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } } \\ { a _ { q , m } A _ { q , m , n } s ( t - \underbrace { ( \lfloor q / M \rfloor T _ { \mathrm { P R I } } + m T ) } _ { t _ { q , m } } - \tau _ { m , n } ) + \mathrm { v } ( t ) , } \end{array}\tag{4}
$$

where

$$
\tau _ { m , n } = \underbrace { \frac { 2 R } { c } } _ { \tau _ { 0 } } + \frac { 2 v t } { c } + \frac { m d _ { t } \sin ( \theta ) } { c } + \frac { n d _ { r } \sin ( \theta ) } { c } ,\tag{5}
$$

$d _ { t }$ and $d _ { r }$ are the inter-element spacing of the transmit and receive antennas, respectively, $A _ { q , m , n }$ is the received amplitude, θ the direction of arrival (DoA) of waves, $^ 3 \in \{ 0 :$ $M Q - 1 \} , m \ \in \ \{ 0 , M - 1 \} , n \ \in \ \{ 0 , N - 1 \}$ , and v denotes complex-valued white noise. Here, R and v denote, respectively, the distance and relative radial velocity between the radar sensor and the object, and c represents the speed of light.

The beat signal in the baseband can be obtained after stretch processing, namely mixing $r _ { q , m , n }$ conjugately with the transmitted signal:

$$
\hat { y } _ { q , m , n } ( t ) = r _ { q , m , n } ^ { * } ( t ) s ( t - t _ { q , m } ) ,\tag{6}
$$

where $t _ { q , m }$ has been defined in (4). Considering the phase term of ${ \hat { y } } _ { q , m , n } ( t )$ , we have

$$
\begin{array} { l } { \phi _ { q , m , n } ( t ) = \phi ( t - t _ { q , m } ) - \phi \bigl ( t - t _ { q , m } - \tau _ { m , n } \bigr ) } \\ { = 2 \pi \bigl ( f _ { c } \tau _ { m , n } + \kappa ( t - t _ { q , m } ) \tau _ { m , n } - 0 . 5 \kappa ( \tau _ { m , n } ) ^ { 2 } \bigr ) . } \end{array}\tag{7}
$$

After sampling with $f _ { s } = 1 / T _ { s }$ , and collecting P samples per chirp at time $t = t _ { q , m } + p T _ { s } \ ( p \in \{ 0 , P - 1 \} )$ , the discrete beat signal in the case of a single target can be described as [27]

$$
\begin{array} { r l } & { \hat { y } _ { m , n } ( p , q ) \approx a _ { q , m } A _ { q , m , n } { \mathrm e } ^ { j 2 \pi \left( \kappa \tau _ { 0 } + \frac { f _ { c } + \kappa t _ { q , m } } { c } 2 v \right) p T _ { s } } } \\ & { \quad \quad \quad \cdot { \mathrm e } ^ { j 2 \pi f _ { c } \frac { 2 v } { c } t _ { q , m } } { \mathrm e } ^ { j 2 \pi ( m d _ { t } + n d _ { r } ) \frac { \sin ( \theta ) } { \lambda } } { \mathrm e } ^ { j 2 \pi f _ { c } \tau _ { 0 } } + { \mathrm v } , } \end{array}\tag{8}
$$

where $\lambda ~ = ~ c / f _ { c }$ is the wavelength. Note that the second order terms are neglected [33]. The term $( f _ { c } + \kappa t _ { q , m } ) 2 v / c$ corresponds to the range migration and Doppler-frequency shift effects which are typically neglected as well [27]. The single-target MIMO signal model in (8) can now be further extended to L targets:

$$
\hat { y } _ { m , n } ( \boldsymbol { p } , \boldsymbol { q } ) \approx \sum _ { l = 1 } ^ { \ L } a _ { q , m } A _ { q , m , n } ^ { ( l ) } \mathrm { e } ^ { j 2 \pi \kappa \tau _ { l } p T _ { s } } \mathrm { e } ^ { j 2 \pi f _ { d _ { l } } t _ { q , m } }\tag{9}
$$

where $\tau _ { l } = 2 R _ { l } / c$ denotes the round-trip propagation delay of the l-th target with $R _ { l }$ and $v _ { l }$ denoting the distance and relative radial velocity of this target, $\begin{array} { r } { f _ { d _ { l } } = f _ { c } \frac { 2 v _ { l } } { c } } \end{array}$ , and $\theta _ { l }$ represents its DoA.

With the assumption that the interfering signal has the carrier frequency $f _ { c _ { I } }$ , the transmit waveform of an interferer radar is $\begin{array} { r } { T _ { \mathrm { i n t } } ( t ) = \sum _ { z = 0 } ^ { Z - 1 } s _ { \mathrm { i n t } } \big ( t - z \tilde { T } \big ) } \end{array}$ , where $\begin{array} { r } { s _ { \mathrm { i n t } } ( t ) = \tilde { A } \mathbf { e } ^ { j \tilde { \phi } ( t ) } \mathbf { r e c t } \big ( \frac { t } { \tilde { T } } \big ) } \end{array}$ with $\tilde { \phi } ( t ) = 2 \pi \bigl ( f _ { c _ { I } } t + 0 . 5 \tilde { \kappa } t ^ { 2 } \bigr )$ , A<sup>˜</sup> the amplitude, Z the number of transmitted chirps, $\tilde { \kappa } ~ = ~ \tilde { B } / \tilde { T }$ , B<sup>˜</sup> and $\tilde { T }$ denote the chirp slope, sweep bandwidth, and chirp duration of the interfering radar, respectively. It should be noted that this paper focuses on incoherent interference, hence $\tilde { \kappa }$ is not considered to be identical to κ. Assuming that the interferer has co-located antennas, and with the far-field approximation, it makes no difference to the receivers from which transmit antenna the interference chirp originates. Therefore, for the description of the transmitted waveform of the interferer, chirps are simply counted from 0 to Z − 1.

![](images/8248beb2caf3a99562a8c9719fb838bd2997b04465761fe75c7f960049fa75fe.jpg)  
Fig. 2. Examples of different interference scenarios.

Due to different chirp rates and bandwidths, the interference scenario can vary case by case as shown in Fig. 2. By using the transmitted chirp sequence as reference, $\overline { { \tau } } _ { I _ { i } } ^ { ( q ) }$ is used to denote the delay time between the start time of the i-th chirp from interferer and the q-th transmitted chirp. Note that the delay time $\tau _ { I _ { i } } ^ { ( q ) }$ is a negative number if the start time of the i -th interfering chirp is earlier than that of the q-th transmitted chirp. As shown in the scenario (c) in Fig. 2, during one chirp time T multiple positions in the chirp can be disturbed. In this case, $\tau _ { I _ { 0 } } ^ { ( 0 ) }$ and $\tau _ { I _ { 1 } } ^ { ( 0 ) }$ represent the delay time of the occurrence of first and second interfering chirp w.r.t. the first transmitted chirp, respectively. The phase of the interference signal after stretch processing is:

$$
\begin{array} { r l } & { \check { \phi } _ { I _ { i } } ^ { ( q ) } ( t ) = \tilde { \phi } \Big ( t - \tau _ { I _ { i } } ^ { ( q ) } \Big ) - \phi ( t ) } \\ & { \qquad = 2 \pi \Big ( ( f _ { c _ { I } } - f _ { c } ) t + 0 . 5 ( \tilde { \kappa } - \kappa ) t ^ { 2 } - \tilde { \kappa } \tau _ { I _ { i } } ^ { ( q ) } t } \\ & { \qquad + 0 . 5 \tilde { \kappa } \Big ( \tau _ { I _ { i } } ^ { ( q ) } \Big ) ^ { 2 } - f _ { c _ { I } } \tau _ { I _ { i } } ^ { ( q ) } \Big ) } \end{array}\tag{10}
$$

where $- f _ { \mathrm { L P F } } \leqslant \left( f _ { c _ { I } } + \tilde { \kappa } \left( t - \tau _ { I _ { i } } ^ { ( q ) } \right) \right) - ( f _ { c } + \kappa t ) \leqslant f _ { \mathrm { L P } } .$ <sub>F</sub>, f<sub>LPF</sub> is the cut-off frequency of the low-pass filter (LPF), indicating that only the interference signal segments falling within the

LPF-frequency limits are considered. Since the interference signal arrives at the n-th receive antenna with a time delay $n d _ { r } \sin ( \theta ) / c$ (compared to its arrival time at the first receive antenna), the additive in-band interference signal of the q-th chirp at the n-th receive antenna is

$$
\begin{array} { r l } & { \check { y } _ { q , n } ( t ) \approx \displaystyle \sum _ { i \in \tilde { Z } _ { q } } \tilde { A } _ { i , n } ^ { ( q ) } \mathrm { e } ^ { j 2 \pi ( f _ { c _ { I } } - f _ { c } ) t } \mathrm { e } ^ { - j 2 \pi n d _ { r } \sin ( \theta ) / \lambda _ { I } } } \\ & { \cdot \mathrm { e } ^ { j 2 \pi \Big ( 0 . 5 ( \tilde { \kappa } - \kappa ) t ^ { 2 } - \tilde { \kappa } \tau _ { I _ { i } } ^ { ( q ) } t + 0 . 5 \tilde { \kappa } \left( \tau _ { I _ { i } } ^ { ( q ) } \right) ^ { 2 } - f _ { c _ { I } } \tau _ { I _ { i } } ^ { ( q ) } \Big ) } \mathrm { r e c t } \left( \frac { t - q T } { T } \right) , } \end{array}\tag{11}
$$

where $\tilde { Z } _ { q }$ denotes the set of interfering chirps that disturb the q-th chirp at the n-th receiving antenna, $\begin{array} { r } { \frac { f _ { c } - f _ { \mathrm { L P F } } - f _ { c _ { I } } + \tilde { \kappa } \tau _ { I _ { i } } ^ { ( q ) } } { \tilde { \kappa } - \kappa } \leqslant t \leqslant } \end{array}$ $\frac { f _ { c } + f _ { \mathrm { L P F } } - f _ { c _ { I } } + \tilde { \kappa } \tau _ { I _ { i } } ^ { ( q ) } } { \tilde { \kappa } - \kappa }$ (extending the derivations in [8] for the case $f _ { c _ { I } } \neq f _ { c } )$ , and $\lambda _ { I } = c / f _ { c _ { I } }$ is the wavelength. $\tilde { Z } _ { q }$ is determined by several factors, namely the modulation parameters of the interferer and victim radars, and the collision time between the interferer and victim radars. $\tilde { Z } _ { q }$ is an empty set if no interfering chirps are present. When T<sub>PRI</sub> of the transmitted waveform of the victim radars is assumed to be equal to M T in (11), then rect $\textstyle \left( { \frac { t - q T } { T } } \right)$ can be used to denote the time span of the q-th chirp. It should be noted that the received additive interference varies only at different receive antennas due to the phase shift and is not related to the transmitters. After sampling with a period of $T _ { s }$ at each receive channel, we now use $\check { y } _ { m , n } ( p , \tilde { q } )$ to represent the additive in-band interference samples at the virtual receive channel $( m N + n )$ . The discrete beat signal $y _ { m , n } ( p , \tilde { q } )$ can be therefore summarized as

$$
y _ { m , n } ( p , \tilde { q } ) = \left\{ \begin{array} { l l } { \hat { y } _ { m , n } ( p , \tilde { q } ) + \mathrm { v } } & { ( p , \tilde { q } ) \in H _ { m , n } } \\ { \hat { y } _ { m , n } ( p , \tilde { q } ) + \check { y } _ { m , n } ( p , \tilde { q } ) + \mathrm { v } } & { ( p , \tilde { q } ) \notin H _ { m , n } , } \end{array} \right.\tag{12}
$$

where $( p , \tilde { q } )$ denotes the sample index $( p$ indicates the sample position inside the chirp and $\tilde { q }$ the chirp index within a chirp sequence transmitted by the same TX) and $H _ { m , n }$ is the set of sample indices without interference at the virtual receive channel $( m N + n )$

## B. Signal Processing Chain

We now explain the signal processing chain in the automotive radar system for target detection with the RAD data cube in the presence of interference. To obtain the range, velocity, and DoA information of targets, few signal processing steps need to be applied to the received discrete beat signal. Fig. 3 shows the signal processing chain of a FMCW TDM MIMO radar system with two transmit antennas and four receive antennas. Since in this paper the interference mitigation method is applied to the disturbed multi-channel discrete beat signal, the RAD data cube is obtained based on the recovered discrete beat signal. Finally, the RAD data cube is utilized for the object detection and classification. For a better comparison, the classical point cloud-based object detection is also shown in Fig. 3.

![](images/2bda546f439ef25d90f64b552ff4e4c6420be062d62c48badc8c7962fd2c4777.jpg)  
Fig. 3. Signal processing pipeline in FMCW TDM MIMO radar system in the presence of interference.

![](images/061def9dc0f300a75eb9e82ffe5af5249a22af58d5acd33eafb7aadf0d3483e5.jpg)  
Fig. 4. Signal separation neural network (SeparationNet) for interference mitigation. For clarity, only the real part of the input data is shown.

## III. SIGNAL SEPARATION NEURAL NETWORK FORINTERFERENCE MITIGATION

In this section we introduce the proposed signal separation neural network for separating target’s echo signals from the interference.

## A. Neural Network Architecture

The architecture of the proposed signal separation neural network (SeparationNet) shown in Fig. 4 is based on convolutional neural network layers [34]. In contrast to state-of-the-art neural networks using the disturbed signal of a single receive channel for interference mitigation, SeparationNet is designed to reconstruct multi-channel receive signals, as depicted in Fig. 4 and 5. The echo signals from targets in different receive channels have a relationship in terms of DoA-dependent phase shifts, which help to determine the target components. By including signals from multiple receive channels in the training process, the neural network can acquire this phase relationship across multiple receive channels and hence utilize this additional information for improving signal reconstruction. Furthermore, the convolutional neural network is inherently proficient in learning the signal features directly from multiple channels (see Fig. 5). The kernels in various filters extract the signal features in each input channel (yellow for the real signal part and green for the imaginary signal part) and the filters summarize outputs of kernels into feature maps that can later be employed for signal reconstruction. Note that the number of filters per layer corresponds to the number of its output channels. Thus, the more filters used in a convolutional layer, the more signal features can be extracted (i.e., more channels in feature maps).

To this end, the complex disturbed discrete beat signal in (12) is rearranged into a tensor of the form $\mathbf { Y } _ { s } \in \mathbb { R } ^ { P \times Q \times M N \times 2 }$ consisting of the real and imaginary parts as the input for the neural network. The first four convolutional layers (denoted as Conv3D) extract signal features from the mixed signals. The signal features of interference-free samples and interference samples are supposed to be the output of the first half and the second half of the filters in the fourth convolutional layer, respectively. Then, each half of the extracted signal features are utilized to reconstruct the corresponding interference-free signal segments and the interference segments. The recovered interference-free signal can be used for further processing steps as shown in Figure 3. In the meantime, based on the separated interference signal, the operating frequency band of the interferer can be estimated, the victim radar can therefore change its operating frequency to other frequency bands which are free of interference [35]. Thus, the effort for interference mitigation for the next measurement cycle can be saved, if the interferer occupies the current frequency band for its further measurements and there are no new interferers. The kernel size is set to 1x9x3 for increasing the receptive field by including more samples in different chirps and receive channels.<sup>4</sup> The number of filters per layer and the kernel size can be adjusted in case of different input dimensions.

![](images/bc2f905511a49dd4968788835c38d80bf5b3589373e9387d8259cf50b7674c88.jpg)  
Fig. 5. An example of a Conv3D employed in SeparationNet. The number of filters per layer corresponds to the number of its output channels. The real and imaginary signal parts are convolved with the distinct kernels in each filter (the real part with the kernel displayed in yellow and the imaginary part with the kernel displayed in green) and the filter summerizes the output of each kernel into feature maps. The kernels are swept over all signal samples in 3 directions with a given stride during convolution.

## B. Loss Function

The loss function is defined as the mean absolute error loss of the reconstructed discrete beat signal and the reconstructed interference signal.

$$
\mathcal { L } _ { A B S } = \frac { 1 } { \epsilon } \sum \Bigl ( \Bigl | \widetilde { \mathbf { Y } } _ { s } - \widehat { \mathbf { Y } } _ { s } \Bigr | + \Bigl | \widetilde { \mathbf { Y } } _ { I } - \check { \mathbf { Y } } _ { I } \Bigr | \Bigr ) ,\tag{13}
$$

![](images/df981cff650186ad16ef09f5784c55d3adcb34db7b4658b5b180effac34f89e1.jpg)  
Fig. 6. Radar sensor employed for the measurement of multi-channel interference-free discrete beat signals.

where ϵ denotes the total number of samples in the input data cube, $\widetilde { \mathbf { Y } } _ { s } , \widehat { \mathbf { Y } } _ { s } , \widetilde { \mathbf { Y } } _ { I }$ , and $\check { \mathbf { Y } } _ { I } \in \mathbb { R } ^ { P \times Q \times M N \times 2 }$ are the tensor form of the recovered discrete beat signal, the interference-free discrete beat signal, the reconstructed interference signal, and the true interference signal, respectively.

Alternatively, we also consider the root mean-squared error (RMSE) loss which is defined as

$$
\mathcal { L } _ { R M S E } = \sqrt { \frac { 1 } { \epsilon } \sum \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \left( \left( \widetilde { \mathbf { Y } } _ { s } - \widehat { \mathbf { Y } } _ { s } \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \right) ^ { 2 } + \left( \widetilde { \mathbf { Y } } _ { I } - \check { \mathbf { Y } } _ { I } \right) ^ { 2 } \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \right) } .\tag{14}
$$

## C. Data Set and Training Details

Since the effort of collecting a large number of interferencecontaminated measurements with various interference sources is prohibitive, a viable approach is to simulate the interference [17]. Different to [17], where the discrete beat signals are simulated only for one receive channel, we simulate several types of multi-channel interference based on the real-world measured discrete beat signals of a FMCW MIMO radar (TI AWR1843BOOST<sup>5</sup>) [2] according to its signal parameters as shown in Table I. Fig. 6 shows the radar sensor employed for measurement of the real-world discrete beat signals. It integrates the phase-locked loop (PLL), transmitter, receiver, and analog-to-digital converter (ADC) in a single chip. The AWR1843BOOST device has three transmit and four receive channels and it is capable of operation in bands ranging from 76 to 81 GHz. The two TXs at the same elevation are activated for the radar measurements.

Since the measurements are recorded on the street, the measured targets are distributed in the radar sensor’s field of view and vary from scenario to scenario. The DoA of the simulated interferer corresponds to the field of view of the victim radar.

The signal separation neural network is trained using an NVIDIA RTX<sup>TM</sup> 3060 for 100 epochs with a batch size of four. It is found that 100 training epochs are sufficient for providing satisfactory signal reconstructions. The stride of the convolution is one. The learning rate is set to 0.0001 and the ADAM optimizer [36] is used during training. The ELU activation function was chosen because it avoids the “dying ReLU” problem [37]. According to our experiments, the reconstruction accuracy could be slightly improved by increasing the number of filters in each layer and adding more layers to the current neural network architecture (see Fig. 4). However, the training and inference time will also increase if more filters and layers are included. The inference time of the proposed SeparationNet is about five milliseconds (corresponding to ca. 57.60 giga floating point operations) on NVIDIA $\mathbf { \mathrm { R T X } } ^ { \mathrm { T M } }$ 3060. The data set contains 20374 realworld measured interference-free complex discrete beat signals having a size of [P, Q, M N ] which is split into training data set and the evaluation data set containing a subset of 18342 and 2532 (including 500 highway and country road scenarios) respectively. During the training process, the interference signals are randomly simulated in each training epoch and thus the interference scenario is completely new for the neural network in each epoch. We therefore do not specifically prepare a validation data set. During the training and evaluation processes, the complex discrete beat signal is then separated into real and imaginary parts, resulting in a tensor of the form [ P, Q, M N , 2]. In each training iteration, the additive interference of randomly one to four interferers are simulated based on (11), where each interferer has different signal parameters that vary randomly according to Table I. The amplitude of the additive interference varies between 50 and 10000. For normalization, each sample of the input data is divided by 250. This value is chosen based on the observation that the maximum amplitude of the undisturbed discrete beat signals in the training data set is about 250 (i.e., the maximum amplitude of the target signal segment).

TABLE I  
RADAR PARAMETERS OF THE VICTIM RADAR ANDTHE SIMULATED INTERFERER
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Victim Radar</td><td rowspan=1 colspan=1>Interfering Radar</td></tr><tr><td rowspan=1 colspan=1>Carrier frequency</td><td rowspan=1 colspan=1>77 GHz</td><td rowspan=1 colspan=1> $7 6 . 5 \ : \mathrm { G H z } \sim 7 7 . 5 \ : \mathrm { G H z }$ </td></tr><tr><td rowspan=1 colspan=1>Chirp duration</td><td rowspan=1 colspan=1>72.5 µs</td><td rowspan=1 colspan=1>20 µs ~ 150 µs</td></tr><tr><td rowspan=1 colspan=1>Sweep bandwidth</td><td rowspan=1 colspan=1>768 MHz</td><td rowspan=1 colspan=1>100 MHz ~ 1 GHz</td></tr><tr><td rowspan=1 colspan=1>LPF cut-off frequency</td><td rowspan=1 colspan=1>10 MHz</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Samples per chirp</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>一</td></tr><tr><td rowspan=1 colspan=1>Chirps per TX</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Number of transmitters</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Number of receivers</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>–</td></tr><tr><td rowspan=1 colspan=1>Field of view</td><td rowspan=1 colspan=1>±60°</td><td rowspan=1 colspan=1>–</td></tr><tr><td rowspan=1 colspan=1>Angular resolution</td><td rowspan=1 colspan=1>0.3516°</td><td rowspan=1 colspan=1>一</td></tr><tr><td rowspan=1 colspan=1>Maximum unambiguous range</td><td rowspan=1 colspan=1>50 m</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Range resolution</td><td rowspan=1 colspan=1>0.20 m</td><td rowspan=1 colspan=1>–</td></tr><tr><td rowspan=1 colspan=1>Maximum unambiguous velocity</td><td rowspan=1 colspan=1>±13.43 m/s</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Velocity resolution</td><td rowspan=1 colspan=1>0.42 m/s</td><td rowspan=1 colspan=1>–</td></tr></table>

Fig. 7 shows examples of real-world measured and simulated disturbed discrete beat signals. In our simulation, we simulated not only the strong interference (Fig. 7 (b)) which has an interferer at a distance of about 2 meters but also interference with medium amplitude (Fig. 7 (c)). In order to imitate more complex interference scenarios (e.g., intersection and congestion scenarios), we simulated interference from multiple interferers (Fig. 7 (d)) at different distances.

Based on the signal model formulated in (11), the simulated interference can appropriately imitate the real-world measured interference. The simulated interference is proven to be effective as the trained neural network can later handle the real-world interference scenarios even though the interference is purely simulated during training.

(a) Real-world interference  
![](images/57479f417afe2a87e12a5112fd37ee9173884654b5d4a64f5f7d346ece6394f6.jpg)

(c) Simulated interference  
![](images/bb90d050d26a08fde018b4d5bd596bee6c1f9fff7bde72bb40deec77f1f2715f.jpg)

(b) Simulated interference  
![](images/1af2a01f0c2684d68a4ea72e76091fe045b4a6e88ed38f50139fe12433f30eba.jpg)

(d) Simulated interference  
![](images/94d9e0e21965c462c8b56cbeeead177b23d3bbe858d3d5b4224f0d7b106b6f1a.jpg)  
Fig. 7. Interference in the discrete beat signal domain: (a) Real-world measured disturbed discrete beat signal, (b) simulated disturbed discrete beat signal with a single interferer at a distance of about 2 meters, (c) simulated disturbed discrete beat signal with a single interferer at a distance of about 20 meters, (d) simulated disturbed discrete beat signal with four different interferers at different distances. For an intuitive visualization, only the real part of the complex discrete beat signal is shown.

## IV. EVALUATION METHODS AND RESULTS

In this section, we first briefly analyze the convergence of the two loss components (i.e., the loss of the reconstructed signal segment and the loss of the reconstructed interference segment) in (13). Then, the performance of the proposed signal separation neural network is evaluated and compared to the state-of-the-art algorithms. The neural network trained on $\mathcal { L } _ { A B S }$ is used for the evaluation, since $\mathcal { L } _ { A B S }$ and $\mathcal { L } _ { R M S E }$ perform similarly in our experiments. The signal-to-interferenceplus-noise ratio (SINR) [13], the false-positive rate (FPR), the true-positive rate (TPR), the peak phase mean-squared error (PPMSE) [24], the mean absolute percentage error (MAPE) [13], and the F1-score are used as evaluation metrics. The F1-score is defined as $F _ { 1 } = \frac { 2 \mathrm { T P } } { 2 \mathrm { T P } + \mathrm { F P } + \mathrm { F N } }$ where TP, FP and FN denote the number of true-positive, false-positive, and false-negative estimates. The true positive rate and false positive rate are defined as $\mathrm { T P R } \ = \ \frac { \mathrm { T P } } { \mathrm { T P } + \mathrm { F N } }$ and $\mathrm { F P R \ = }$ $\frac { \mathrm { F P } } { \mathrm { F P } + \mathrm { T N } }$ , respectively, where TN denotes the true-negative estimates. A cell averaging CFAR (CA-CFAR) target detection algorithm is used to automatically detect the peak positions in both the interference-free and interference-contaminated RD spectra. The peak positions detected in the interference-free RD spectra are then used as the ground truth for the calculation of TP, FP, TN, and FN. If a peak detection is found only in the reconstructed RD spectrum but not in the interferencefree RD spectrum, this detection is classified as FP. If a peak detection is found in both the reconstructed RD spectrum and the interference-free RD spectrum, this detection is recognized as TP. The SINR, FPR, TPR, PPMSE, MAPE, and F1-score are calculated in each receive channel. Then, the mean values of these evaluation metrics of all receive channels are used for the performance assessment.

![](images/00da9c4beb88b266328de46e0a0f9a237de5396165c1cdef2e846edfd57c1adc.jpg)  
Fig. 8. Training loss curves of the reconstructed signal segment and the reconstructed interference segment.

Moreover, based on the reconstructed discrete beat signals of these algorithms, the corresponding RAD data cubes can be obtained (see Fig. 3) and the accuracy of target detection and classification is further evaluated based on a state-of-the-art automotive radar object detection neural network [2]. Finally, the benefits of applying the proposed interference mitigation approach are demonstrated.

## A. Convergence Analysis Based on Training Loss Curve

The loss curves of the reconstructed signal segment and the reconstructed interference segment are presented in Fig. 8, where we calculated the loss of signal and interference (see (13)) separately. Compared to the loss of the reconstructed interference segment, the loss of the reconstructed signal segment has a smaller value and a faster convergence rate. This is due to the fact that the amplitude of the interference segment fluctuates in a larger range than the signal segment, as described in section III-C. As a result, the error value of the reconstructed interference segment may deviate to a greater extent. Both losses converge to a steady state after about 100 training iterations.

## B. Performance Evaluation on Signal Reconstruction With Measured Interference

Recent research results have shown that the zeroing method [3], the AR model [12], and deep learning algorithms like the CNN-based RD spectrum reconstruction [17], [22] can be utilized for interference mitigation. We first evaluate the SINR, F1-score, FPR, and TPR of the reconstructed RD spectra that obtained by applying the proposed SeparationNet and the state-of-the-art algorithms. In this real-world interference scenario, the interfering radar which has a chirp rate of 1/3 of the victim radar, is placed at a distance of 2 meters in front of the victim radar.

Fig. 9 shows the undisturbed and disturbed RD spectra as well as the recovered RD spectra. The target peaks are completely obscured by the high level of background noise in the disturbed RD spectrum. The target peak at a distance of 13.8 m with a velocity of −10.08 m/s can be easily detected in the RD spectra recovered by the zeroing method [3], AR [12], and the proposed SeparationNet, while it is absent in the RD spectrum recovered by CNN [22]. The SeparationNet can reconstruct the target peak more accurately than the zeroing and AR methods, as shown in Fig. 10, which gives the range profile of the recovered RD spectra at velocity −10.08 m/s.

TABLE II  
ANALYSIS RESULTS OF THE RECONSTRUCTION IN TERMS OF SINR, F1-SCORE, FPR, AND TPR FOR DIFFERENT MITIGATION TECHNIQUES.THE RESULTS OF THE PROPOSED METHOD AREHIGHLIGHTED IN BLUE
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Undisturbed</td><td rowspan=1 colspan=1>Disturbed</td><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>AR</td><td rowspan=1 colspan=1>CNN</td><td rowspan=1 colspan=1>SeparationNet</td></tr><tr><td rowspan=1 colspan=1>SINR</td><td rowspan=1 colspan=1>24.36269</td><td rowspan=1 colspan=1>-0.45493</td><td rowspan=1 colspan=1>23.34727</td><td rowspan=1 colspan=1>23.75675</td><td rowspan=1 colspan=1>16.05215</td><td rowspan=1 colspan=1>24.36058</td></tr><tr><td rowspan=1 colspan=1>F1-score</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0.01835</td><td rowspan=1 colspan=1>0.83393</td><td rowspan=1 colspan=1>0.86400</td><td rowspan=1 colspan=1>0.09906</td><td rowspan=1 colspan=1>0.95769</td></tr><tr><td rowspan=1 colspan=1>FPR</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.01140</td><td rowspan=1 colspan=1>0.00219</td><td rowspan=1 colspan=1>0.00134</td><td rowspan=1 colspan=1>0.00633</td><td rowspan=1 colspan=1>0.00025</td></tr><tr><td rowspan=1 colspan=1>TPR</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0.05923</td><td rowspan=1 colspan=1>0.91214</td><td rowspan=1 colspan=1>0.91708</td><td rowspan=1 colspan=1>0.73347</td><td rowspan=1 colspan=1>0.94867</td></tr></table>

The mean value of SINR, F1-score, FPR, and TPR of all receiving channels are summarized in Table II. Although SeparationNet is trained with purely simulated interference, it can still provide the best signal recovery in this realworld measured interference scenario. The FPR of SeparationNet is two orders of magnitude less than the FPR for the disturbed RD spectra and one order of magnitude less than the state-of-the-art interference mitigation algorithms. Note that all interference-contaminated samples are assumed to be perfectly detected for the zeroing method and the AR model in our evaluation. Based on our experiments, when 1% of interference-contaminated samples are not detected, the SINR of the RD spectra reconstructed by the zeroing and AR methods significantly reduces to ca. 16.35 dB and 17.21 dB in this real-world interference scenario, respectively.

## C. Performance Evaluation on Signal Reconstruction With Simulated Interference

Since it is quite difficult to obtain reference measurements for all real-world measured interference scenarios, we further evaluate the performance of these interference mitigation algorithms with simulated interference (11), where the discrete beat signals are measured in the real world [2]. In this section, the performance of proposed method along with the simple zeroing method [3], the AR model [12], and the CNN-based RD spectra reconstruction [22] are evaluated in terms of SINR, PPMSE, MAPE, and F1-score. Here, all interference-contaminated samples are also assumed to be perfectly detected for the zeroing method and the AR model in our evaluation. To demonstrate the advantages of training the neural network with multi-channel discrete beat signals as input, the proposed SeparationNet is also trained with only one receive channel and then used to reconstruct multi-channel discrete beat signals. For distinction, the SeparationNet trained with single-channel discrete beat signals is referred to as SeparationNet-S and the SeparationNet trained with multichannel discrete beat signals is referred to as SeparationNet-M.

(a) Undisturbed - SINR 25.06 dB  
![](images/af062878ba51c86d740bfa73b4da183d0e9c577e255aa0e8f321871995b6e680.jpg)

(c) CNN - SINR 21.25 dB  
![](images/3db07edff3cd3bbe248c2bee1a8ad9c5c110dab80a9888dfb57cfdd0eb16c0b1.jpg)

![](images/5fbe1e9e9b68ee604cf8aa3e439798234715ed988418327981133223c8bc1eb4.jpg)

(b) Disturbed - SINR 0.19 dB  
![](images/e68e11e560464f84bc440551ee6b5e6ae1f9c8b5ea6cd410a2675eab4c722ac0.jpg)

(d) Zeroing - SINR 21.71 dB  
![](images/ec98792e7d78ab12f44c26ab58af5ad2d4acd468bd98e1d702ffdd1609789d40.jpg)

(f) SeparationNet - SINR 24.75 dB  
![](images/04b3ee25bb592577ff65d4008fea321356d1def361e28ccb5af31b81443da5aa.jpg)  
Fig. 9. (a) Undisturbed RD spectrum, (b) disturbed RD spectrum, and RD spectra recovered by (c) CNN, (d) the zeroing method, (e) AR, (f) SeparationNet

![](images/66ac402565161f01adcde9d2dd7e1f3e13a95d10c95d51693a550f016c0b546b.jpg)  
Fig. 10. Range profile of RD spectra at velocity −10.08 m/s.

Due to the diversity of chirp rate, the collision time between interferer and victim radar, the number of interferers, the number of disturbed samples, and the signal strength of interference can vary in different interference scenarios. In order to evaluate the performance of these aforementioned algorithms, three classes of interference scenarios are simulated: weak, medium, and strong, corresponding to a degradation of ca. −5 dB, −10 dB, and −15 dB SINR of the RD spectra (compared to the interference-free scenario), respectively. The empirical mean and standard deviation of the SINR of the interference-free RD spectra in the evaluation data set are 26.67 dB and 3.44 dB, respectively. Note that the proposed neural network is trained with the interference scenarios that cause -10 dB to -5 dB SINR degradation of the RD spectra.

Fig. 11 shows the SINR of the recovered RD spectra of three reference algorithms: AR [12], CNN [22], and the zeroing method [3], as well as the proposed SeparationNet. Note that we have extended the input channel of the original single-channel CNN implementation in [22] to reconstruct the multi-channel RD spectra. For the reconstruction of a multichannel discrete beat signal, the zeroing method, AR, and the SeparationNet trained with single-channel interference are applied in each signal channel and the reconstructed signal in each individual channel is then combined for the further analysis. The SINR of RD spectra recovered by the AR and zeroing methods decreases as the interference intensity increases, while the CNN and SeparationNet are less affected by the interference intensity. The CNN has shown its strength in RD spectra denoising and provides the best SINR of the recovered RD spectra. However, when the interference magnitude becomes very large (e.g., in the real-world measured interference which causes a degradation of ca. −25 dB SINR of the RD spectrum), the SINR provided by CNN degrades to the suppression of both strong and weak target peaks in the reconstructed RD spectrum.

As shown in Fig. 12, the proposed SeparationNet can deliver a superior F1-score under different interference intensities. Due to the absence of some weak target peaks in the reconstructed RD spectra (see Fig. 9 (c)), the CNN therefore does not provide an optimal F1-score. The SeparationNet trained with single-channel interference outperforms the state-of-theart interference mitigation algorithms, while the SeparationNet trained with multi-channel interference further improves the F1-score by 3 - 5%. Fig. 13 shows the evaluation results of the MAPE of reconstructed target peaks detected by the CA-CFAR. For all signal reconstruction methods, the MAPE increases with increasing interference intensity. The target peaks reconstructed by the proposed method have the smallest MAPE. Similar results can also be found in the PPMSE of the reconstructed target peaks in Fig. 14, where the proposed SeparationNet (both SeparationNet-S and SeparationNet-M)

![](images/83d888e9cc2abcac4344d7eac8c6aae6fcbc8602b588ab3711b827fa37473fae.jpg)  
Fig. 11. SINR of the reconstructed RD spectra of different interference mitigation methods in the presence of weak, medium, and strong interference.

![](images/78924d6b8c42b19a2c86e4b71c79fbdea14c518fba33bebe8b32e41343f3fcc0.jpg)  
Fig. 12. F1-score for the target peak detection in the reconstructed RD spectra of different interference mitigation methods in the presence of weak, medium, and strong interference.

Mean absolute percentage error  
![](images/82a8ac2737a9696e6a84fdb58f0b809779ef0cce2d0de9a3f5fbaf45ee8d4cb6.jpg)  
Fig. 13. MAPE of target peaks in the reconstructed RD spectra of different interference mitigation methods in the presence of weak (‘w’), medium (‘m’), and strong (‘s’) interference.

Peak phase mean squared error  
![](images/a679a76c9ec873aaf06ae1047abf5ef7476cf84e2ebf92767fbab70a70aec063.jpg)  
Fig. 14. PPMSE of target peaks in the reconstructed RD spectra of different interference mitigation methods in the presence of weak (‘w’), medium (‘m’), and strong (‘s’) interference.

provides superior reconstruction under different interference intensities. Different from the evaluation related to SINR, the weak target peaks can cause a similar MAPE or PPMSE as the strong target peaks. Therefore, the absence of weak target peaks in the reconstructed RD spectra significantly degrades the results of CNN. Even though the AR and zeroing methods provide lower MAPE and PPMSE than the CNN under the assumption of a perfect detection of disturbed samples, it should be noted that this assumption does not hold in most real-world interference scenarios. Thus, the recovered results of the AR and zeroing methods might deteriorate in realworld scenarios due to the imperfect detection of the disturbed samples.

Compared to the strong target peaks such as cars or trucks, the relatively weak target peaks usually represent the vulnerable road users (e.g., pedestrians and bicyclists) whose signals are more likely to be affected by mutual interference. To evaluate the quality of the reconstructed target peaks at different interference densities, an intersection scenario is chosen where pedestrians, bicyclists, and cars are present, which well represent the targets with low, medium, and high SNR. The SNR of the weak target peaks is about 3 dB below the medium target peaks, while the SNR of the medium target peaks is about 4 dB smaller than the strong target peaks. The angle estimation error of the weak, medium and strong target peaks as well as the receiver operating characteristic (ROC) of the detection of these target peaks are further evaluated in this section.

Table III shows the evaluation results of the RMSE of the angle estimation of the proposed method compared with other state-of-the-art interference mitigation algorithms. When the power of interference increases, the angle estimation of weak targets based on the reconstructed signals of all methods contains more errors, while the proposed SeparationNet provides the smallest RMSE. For the targets with medium and strong SNR, the angle estimation errors of the SeparationNet, Zeroing, and AR methods are smaller than the angle estimation error for the weak targets. As the results presented in Fig. 14 show, SeparationNet can provide the smallest phase errors for the detected target peaks. Thus, the angle estimations of

TABLE III  
ROOT MEAN SQUARED ERROR (IN RADIANS) OF ANGLE ESTIMATION OF WEAK, MEDIUM, AND STRONG TARGETS UNDER DIFFERENT INTERFERENCE SCENARIOS. THE RESULTS OF THE PROPOSED METHOD ARE HIGHLIGHTED IN BOLD
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>weak</td><td rowspan=1 colspan=3>interference</td><td rowspan=1 colspan=5>medium interference</td><td rowspan=1 colspan=5>strong interference</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Undisturbed</td><td rowspan=1 colspan=1>Disturbed</td><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>AR</td><td rowspan=1 colspan=1>CNN</td><td rowspan=1 colspan=1>SeparationNet</td><td rowspan=1 colspan=1>Disturbed</td><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>AR</td><td rowspan=1 colspan=1>CNN</td><td rowspan=1 colspan=1>SeparationNet</td><td rowspan=1 colspan=1>Disturbed</td><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>AR</td><td rowspan=1 colspan=1>CNN</td><td rowspan=1 colspan=1>SeparationNet</td></tr><tr><td rowspan=1 colspan=1>weak target</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.01522</td><td rowspan=1 colspan=1>0.01305</td><td rowspan=1 colspan=1>0.00520</td><td rowspan=1 colspan=1>0.17896</td><td rowspan=1 colspan=1>0.005137</td><td rowspan=1 colspan=1>1.14869</td><td rowspan=1 colspan=1>0.02146</td><td rowspan=1 colspan=1>0.02018</td><td rowspan=1 colspan=1>0.18979</td><td rowspan=1 colspan=1>0.010210</td><td rowspan=1 colspan=1>1.733239</td><td rowspan=1 colspan=1>0.06153</td><td rowspan=1 colspan=1>0.05548</td><td rowspan=1 colspan=1>1.43080</td><td rowspan=1 colspan=1>0.011085</td></tr><tr><td rowspan=1 colspan=1>medium target</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.00756</td><td rowspan=1 colspan=1>0.00674</td><td rowspan=1 colspan=1>0.00507</td><td rowspan=1 colspan=1>0.24294</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.10514</td><td rowspan=1 colspan=1>0.01317</td><td rowspan=1 colspan=1>0.00606</td><td rowspan=1 colspan=1>0.24950</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.150338</td><td rowspan=1 colspan=1>0.014620</td><td rowspan=1 colspan=1>.00807</td><td rowspan=1 colspan=1>0.25922</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>strong target</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.21522</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.00874</td><td rowspan=1 colspan=1>0.00210</td><td rowspan=1 colspan=1>0.00179</td><td rowspan=1 colspan=1>0.21208</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0.00443</td><td rowspan=1 colspan=1>0.00667</td><td rowspan=1 colspan=1>0.00440</td><td rowspan=1 colspan=1>0.22146</td><td rowspan=1 colspan=1>0</td></tr></table>

ROC in strong interference scenarios  
![](images/99bb08563ce4b41655b2b7951b0af67c9d557fcb280c5fdf789258a75573373a.jpg)  
Fig. 15. The ROC for the detection of target peaks by CA-CFAR in the reconstructed RD spectra of different interference mitigation methods in the presence of strong interference.

SeparationNet for the medium and strong targets are identical to the angle estimations based on the undisturbed RD spectra.

Fig. 15 shows the ROC for the detection of target peaks by CA-CFAR in the reconstructed RD spectra of different interference mitigation methods in the presence of strong interference. The area under the ROC (AUC) is an indicator of the target detection performance. The maximum value of AUC is 1, which means that true-positive rate is high regardless of false-positive rate. The proposed SeparationNet provides the largest AUC, which means that most of the target peaks (including the weak target peaks) can be recovered after the interference mitigation has been applied.

## D. Performance Evaluation of Reconstructed Discrete Beat Signal on Target Detection

In this subsection, we evaluate the impact of interference reduction on the object detection accuracy using a state-ofthe-art RAD-based object detection neural network (RadarRes-Net) [2]. Note that the phase compensation [38] for the moving target is not applied in the RAD-based object detection developed in [2]. Since the aim of this work is to improve the object detection accuracy in the presence of interference, we use the RadarResNet as is. The proposed signal separation neural network is integrated into the processing pipeline as shown in Fig. 16. The RadarResNet [2] is based on ResNet [39] which consists of two types of blocks, namely the residual blocks and downsampling blocks. The coordinate transformation layer takes the feature maps extracted by RadarResNet and generates Cartesian feature maps which can then be used for object detection in Cartesian coordinates with the YOLO detection head. The YOLO detection head is an anchor-based method proposed in [40]. The output of the YOLO detection head is the predicted bounding boxes for the detected objects. More details regarding the RAD-based object detection neural network can be found in [2]. To evaluate object detection performance, the average precision (AP) [41] is used which indicates the percentage of ground-truth objects among all detected objects. A detection can be classified as true positive or false positive by comparing the intersection over union (IoU) of the ground-truth and predicted bounding boxes with a predefined threshold. The IoU is used to measure how well the ground-truth and predicted boxes match and is defined as

$$
{ \mathrm { I o U } } = { \frac { { \mathrm { A r e a ~ o f ~ i n t e r s e c t i o n } } } { \mathsf { A r e a ~ o f ~ u n i o n } } } = { \frac { | C \cap D | } { | C \cup D | } } ,
$$

where C and D are the prediction and ground truth bounding boxes. Since multiple object classes are defined, the mean AP (mAP) is employed as a metric to measure the accuracy of object detection across all classes. A higher mAP score indicates a more accurate detection.

The mAP of the object detection based on interference-free RADs is compared with the mAP of the object detection based on the disturbed RADs (with three interference intensities) and the RADs reconstructed by the proposed SeparationNet. Table IV shows the mAP of the object detection for three object classes (car, person, and truck) at four different IoUs (0.1, 0.3, 0.5, and 0.7). Even with weak interference, the mAP drops significantly for these four IoUs. However, with the proposed signal reconstruction method, the mAP can be significantly improved even in the presence of strong interference.

## E. Discussion

With the proposed signal model and the corresponding data generation framework, a wide variety of interference scenarios can be considered in the training process. However, since each manufacturer of automotive radar sensors has its own specific modulations of the radar signal, a comprehensive collection of all interference scenarios for training is almost impossible. By simulating the radar signal parameters of the interferer randomly in each training epoch, which can be considered as a data augmentation technique [42], the trained neural network can properly handle a wide range of interference scenarios and avoid overfitting. However, new modulation techniques may emerge. In this context it should be noted that the interference between the digital modulated radar and the chirp sequence radar is not considered in this work.

(f)  
![](images/29bde99d968cb98485b25f54a3bc89701a386587710e310f6c7c26b2987bb163.jpg)  
Fig. 16. Dataflow of RAD-based object detection in the presence of interference extended based on [2] with the proposed signal separation neural network  
TABLE IV

MEAN AVERAGE PRECISION OF RAD-BASED OBJECT DETECTION AT DIFFERENT IOUS WITH UNDISTURBED RADS, INTERFERENCE-CONTAMINATED RADS, AND THE CORRESPONDING RADS RECON-STRUCTED BY THE PROPOSED SEPARATIONNET
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mAP@0.1</td><td rowspan=1 colspan=1>mAP@0.3</td><td rowspan=1 colspan=1>mAP@0.5</td><td rowspan=1 colspan=1>mAP@0.7</td></tr><tr><td rowspan=1 colspan=1>RAD, undisturbed</td><td rowspan=1 colspan=1>0.765042</td><td rowspan=1 colspan=1>0.667906</td><td rowspan=1 colspan=1>0.460166</td><td rowspan=1 colspan=1>0.181864</td></tr><tr><td rowspan=1 colspan=1>RAD with weakinterference</td><td rowspan=1 colspan=1>0.244871</td><td rowspan=1 colspan=1>0.188723</td><td rowspan=1 colspan=1>0.110997</td><td rowspan=1 colspan=1>0.029118</td></tr><tr><td rowspan=1 colspan=1>RAD with mediuminterference</td><td rowspan=1 colspan=1>0.092436</td><td rowspan=1 colspan=1>0.053226</td><td rowspan=1 colspan=1>0.02352</td><td rowspan=1 colspan=1>0.003041</td></tr><tr><td rowspan=1 colspan=1>RAD with stronginterference</td><td rowspan=1 colspan=1>0.047182</td><td rowspan=1 colspan=1>0.016736</td><td rowspan=1 colspan=1>0.003706</td><td rowspan=1 colspan=1>0.000068</td></tr><tr><td rowspan=1 colspan=1>RAD recovered fromweak interference</td><td rowspan=1 colspan=1>0.745441</td><td rowspan=1 colspan=1>0.650962</td><td rowspan=1 colspan=1>0.460448</td><td rowspan=1 colspan=1>0.163794</td></tr><tr><td rowspan=1 colspan=1>RAD recovered frommedium interference</td><td rowspan=1 colspan=1>0.729371</td><td rowspan=1 colspan=1>0.633844</td><td rowspan=1 colspan=1>0.424185</td><td rowspan=1 colspan=1>0.156491</td></tr><tr><td rowspan=1 colspan=1>RAD recovered fromstrong interference</td><td rowspan=1 colspan=1>0.717172</td><td rowspan=1 colspan=1>0.619417</td><td rowspan=1 colspan=1>0.419968</td><td rowspan=1 colspan=1>0.150402</td></tr></table>

In comparison to the proposed method, the zeroing and AR methods are limited not only in the quality of the reconstructed signal but also in the accuracy of the detected interference segments, since the positions of the disturbed samples must first be detected and the signal segments in these disturbed positions can then be reconstructed. However, it is difficult to accurately detect all disturbed samples, as also discussed in [22], where a detection accuracy of 90% is assumed. As shown in Fig. 17, if the amplitude of the disturbed signal samples is in the same range as the amplitude of the interference-free signal samples, these disturbed samples are difficult to detect by the classical amplitudebased thresholding algorithms. Although the amplitude of these disturbed samples is relatively small (compared to the interference scenarios shown in Fig. 7), the disturbance in the RD spectrum is not negligible (see Fig. 17(e)). Nevertheless, the proposed method can reconstruct the target signal samples well (see Fig. 17(c) and (f)). In contrast to the zeroing and AR methods, the proposed method and the CNN for RD spectra reconstruction [22] avoid the additional detection process.

The performance difference between the proposed method and the CNN [22] is mainly caused by two factors, namely the type of input signal and the number of channels of the input signal used during training. Even if only a few discrete beat signal samples are disturbed by strong interference, the energy of the interference spreads to the whole RD spectrum after FFT, so that the weak target peaks are obscured by the high levels of background noise. However, reconstructing these few disturbed discrete beat signal samples in the time domain is easier and yields better results. Utilizing the signal features learned from multiple receive channels can further improve signal reconstruction results. For an imaging radar with multiple TXs at different elevations, the input of the proposed neural network can be formulated as a tensor in the form [P, Q, N, M, 2] instead of stacking all virtual channels on top of each other (i.e., [P, Q, M N, 2]). Then, a 3D convolution can be applied in the first three dimensions to extract the phase information from the received signals of RXs (at the same elevation) coming from the same TX for interference mitigation. In this way, the phase offsets between the virtual antenna elements of different transmitters would not affect the reconstruction performance.

(a)  
![](images/4202a58ad975392c449a2bf1a37bad83cee116d351723ce414345dc027017d7e.jpg)

[dB]  
(d)  
![](images/d086e5224e85cec4dc1168faed07fc991054b7c410c5faf8d2f7dbf582cb4ce1.jpg)

![](images/5be5635277dead254ee9285825145e5ad15b86ff4c29d23cc6e210f87c56552b.jpg)

![](images/add6d8e6804607a1f92e71518a798a70a694c7c3ce1e012e34219f7d70fb417d.jpg)

![](images/dd538bd7032e504c7c58c81589b51efbfc14326a2d1cd22d406c7ab79aba7de5.jpg)

![](images/0f4ce8356b682b1ae06ec336ddce59fed71fb6ba67857ed0fc6dca31bb7928a8.jpg)  
Fig. 17. Examples of discrete beat signals and RD spectra in a real-world measured dynamic scenario: (a) without interference, (b) with interference (which is difficult to be detected with the classical amplitude-based thresholding algorithm), and (c) recovered by the proposed method. The corresponding RD spectra of (a), (b), and (c) are presented in (d), (e), and (f), respectively. The target peaks are circled in red ellipses. For an intuitive visualization, only the real part of the complex discrete beat signal is shown in (a), (b), and (c).

Most commercial automotive radar sensors have dedicated antenna patterns for the intended applications (e.g., adaptive cruise control). Thus, the antenna gain may vary on different receive channels. The amplitude of the received signal can therefore vary and result in different signal distributions on each receive channel. By considering the received multichannel signals as the input, the neural networks can learn the joint distribution and reconstruct the interference-free signal segments properly.

Since the TDM-MIMO scheme has the disadvantage of a reduced unambiguous speed [43], [44], i.e., if the target’s true radial velocity exceeds the maximum unambiguous velocity range of the TDM waveform, the measured velocity will be incorrect and aliased. It is of interest to investigate the performance of the proposed algorithm in the cases of ambiguous speed in future work.

## V. CONCLUSION

In this paper, we present a signal separation neural network for interference mitigation in FMCW MIMO radar. The network estimates not only an interference-free multi-channel beat signal but also the multi-channel interference. By synthesizing interference signals using a novel interference model and adding them to real-world radar measurements at multiple receive antennas, we create a new interference-contaminated discrete beat signal data set. The evaluation demonstrates that the proposed method yields superior recovery in terms of SINR, FPR, F1-score, angle estimation, MAPE, and PPMSE compared to the other reconstruction algorithms in this evaluation. Thus, this data-driven pre-processing approach provides an effective countermeasure against interference. In addition, the evaluation with real-world interference demonstrates the effectiveness of the proposed interference signal model. Although the neural network has been trained only with simulated interference, it also properly handles real-world measurements. With the help of the proposed method, the accuracy of target detection in the presence of interference (evaluated in terms of the mean average precision) is also significantly improved. Finally, the proposed neural network could also be combined with the classical frequency hopping algorithm for interference mitigation, since the interference signal segments are available as well. Since the data set used in this work was measured with TX antennas on the same elevation, the proposed algorithm still needs to be verified on data sets measured with TX antennas on different elevations in future work.

## REFERENCES

[1] O. Schumann, J. Lombacher, M. Hahn, C. Wöhler, and J. Dickmann, “Scene understanding with automotive radar,” IEEE Trans. Intell. Vehicles, vol. 5, no. 2, pp. 188–203, Jun. 2020.

[2] A. Zhang, F. E. Nowruzi, and R. Laganiere, “RADDet: Range-Azimuth-Doppler based radar object detection for dynamic road users,” in Proc. 18th Conf. Robots Vis. (CRV), May 2021, pp. 95–102.

[3] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[4] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun. 2016, pp. 1–9.

[5] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[6] Z. Xu and Q. Shi, “Interference mitigation for automotive radar using orthogonal noise waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137–141, Jan. 2018.

[7] F. Uysal, “Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[8] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf. (RadarConf18), Apr. 2018, pp. 405–410.

[9] S. Chen, J. Taghia, U. Kühnau, T. Fei, F. Grünhaupt, and R. Martin, “Automotive radar interference reduction based on sparse Bayesian learning,” in Proc. IEEE Radar Conf. (RadarConf), Sep. 2020, pp. 1–6.

[10] S. Lee, J. Lee, and S. Kim, “Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887–897, Feb. 2021.

[11] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2020, pp. 3802–3806.

[12] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[13] S. Chen, J. Taghia, U. Kühnau, N. Pohl, and R. Martin, “A twostage DNN model with mask-gated convolution for automotive radar interference detection and mitigation,” IEEE Sensors J., vol. 22, no. 12, pp. 12017–12027, Jun. 2022.

[14] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approachbased interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[15] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[16] S. Chen, J. Taghia, T. Fei, U. Kühnau, N. Pohl, and R. Martin, “A DNN autoencoder for automotive radar interference mitigation,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2021, pp. 4065–4069.

[17] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in Proc. 22th Int. Conf. Inf. Fusion (FUSION), Jul. 2019, pp. 1–8.

[18] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747–3754, Apr. 2019.

[19] S. Chen, W. Shangguan, J. Taghia, U. Kühnau, and R. Martin, “Automotive radar interference mitigation based on a generative adversarial network,” in Proc. IEEE Asia–Pacific Microw. Conf. (APMC), Dec. 2020, pp. 728–730.

[20] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[21] J. Fuchs, A. Dubey, M. Lübke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320.

[22] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021.

[23] C. Jiang, T. Chen, and B. Yang, “Adversarial interference mitigation for automotive radar,” in Proc. IEEE Radar Conf. (RadarConf), May 2021, pp. 1–6.

[24] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Complexvalued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in Proc. IEEE Radar Conf. (RadarConf), May 2021, pp. 1–6.

[25] M. Umehira, T. Okuda, X. Wang, S. Takeda, and H. Kuroda, “An adaptive interference detection and suppression scheme using iterative processing for automotive FMCW radars,” in Proc. IEEE Radar Conf. (RadarConf), Sep. 2020, pp. 1–5.

[26] S. Sun, A. P. Petropulu, and H. V. Poor, “MIMO radar for advanced driver-assistance systems and autonomous driving: Advantages and challenges,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 98–117, Jul. 2020.

[27] F. Engels, P. Heidenreich, M. Wintermantel, L. Stäcker, M. Al Kadi, and A. M. Zoubir, “Automotive radar signal processing: Research directions and practical challenges,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 865–878, Jun. 2021.

[28] N. Scheiner, N. Appenrodt, J. Dickmann, and B. Sick, “Radar-based road user classification and novelty detection with recurrent neural network ensembles,” in Proc. IEEE Intell. Vehicles Symp. (IV), Jun. 2019, pp. 722–729.

[29] N. Scheiner, F. Kraus, N. Appenrodt, J. Dickmann, and B. Sick, “Object detection for automotive radar point clouds—A comparison,” AI Perspect., vol. 3, no. 1, pp. 1–23, Nov. 2021.

[30] A. Ouaknine, A. Newson, J. Rebut, F. Tupin, and P. Pérez, “CARRADA dataset: Camera and automotive radar with range-angle-Doppler annotations,” in Proc. 25th Int. Conf. Pattern Recognit. (ICPR), Jan. 2021, pp. 5068–5075.

[31] M. Kronauge and H. Rohling, “New chirp sequence radar waveform,” IEEE Trans. Aerosp. Electron. Syst., vol. 50, no. 4, pp. 2870–2877, Oct. 2014.

[32] K. Rambach, Direction of Arrival Estimation Using a Multiple-Input-Multiple-Output Radar With Applications to Automobiles. Stuttgart, Germany: Universität Stuttgart, 2017.

[33] J. Gamba, Radar Signal Processing for Autonomous Driving, 1st ed. Cham, Switzerland: Springer, 2019.

[34] Y. LeCun and Y. Bengio, Convolutional Networks for Images, Speech, and Time Series. Cambridge, MA, USA: MIT Press, 1998, pp. 255–258.

[35] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in IEEE MTT-S Int. Microw. Symp. Dig., May 2016, pp. 1–4.

[36] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in Proc. 3rd Int. Conf. Learn. Represent., (ICLR), San Diego, CA, USA, May 2015.

[37] L. Lu, Y. Shin, Y. Su, and G. E. Karniadakis, “Dying ReLU and initialization: Theory and numerical examples,” 2019, arXiv:1903.06733.

[38] J. Bechter, F. Roos, and C. Waldschmidt, “Compensation of motion-induced phase errors in TDM MIMO radars,” IEEE Microw. Wireless Compon. Lett., vol. 27, no. 12, pp. 1164–1166, Dec. 2017.

[39] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2016, pp. 770–778.

[40] A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, “YOLOv4: Optimal speed and accuracy of object detection,” 2020, arXiv:2004.10934.

[41] R. Padilla, S. L. Netto, and E. A. B. da Silva, “A survey on performance metrics for object-detection algorithms,” in Proc. Int. Conf. Syst., Signals Image Process. (IWSSIP), Jul. 2020, pp. 237–242.

[42] A. Mikolajczyk and M. Grochowski, “Data augmentation for improving deep learning in image classification problem,” in Proc. Int. Interdiscipl. PhD Workshop (IIPhDW), May 2018, pp. 117–122.

[43] F. Roos, J. Bechter, N. Appenrodt, J. Dickmann, and C. Waldschmidt, “Enhancement of Doppler unambiguity for chirp-sequence modulated TDM-MIMO radars,” in IEEE MTT-S Int. Microw. Symp. Dig., Apr. 2018, pp. 1–4.

[44] M. Dikshtein, O. Longman, S. Villeval, and I. Bilik, “Automotive radar maximum unambiguous velocity extension via high-order phase components,” IEEE Trans. Aerosp. Electron. Syst., vol. 58, no. 1, pp. 743–751, Feb. 2022.

![](images/c3cc635dae3bf8c25daf793442ddd1f4fce714309a38a12131ed18b20a2f68a7.jpg)

Shengyi Chen received the B.Sc. degree in electrical and computer engineering from the Technical University of Kaiserslautern, Germany, Fuzhou University, China, in 2016, and the M.Sc. degree in electrical and computer engineering from the Technical University of Munich, Germany. He is currently pursuing the Dr.-Ing. degree in electrical engineering and information technology with the Ruhr-Universität Bochum, Germany.

His research interests are automotive radar signal processing, machine learning, and compressive sensing.

![](images/4e7c7a7fd484af38a6e7527eb7b2428b223542af3540eb197aaafdaca7a7e093.jpg)

Marvin Klemp received the B.Sc. and M.Sc. degree in computer science from the Hochschule Bonn-Rhein-Sieg, Sankt Augustin, Germany, in 2018 and 2021, respectively. He is currently pursuing the Ph.D. degree with the Institute of Measurement and Control Systems, Karlsruhe Institute of Technology, Karlsruhe, Germany.

His research interests include deep learning based perception systems for intelligent transportation systems.

![](images/f8b819c7be02bc39cad641aab5e2ac7bc2b94ff6226c0d55abe88c99d9f006a1.jpg)

Jalal Taghia received the B.Sc. degree in electrical engineering from Azad University, Ghazvin, Iran, in 2006. He pursued further studies in electrical engineering and M.Sc. degree from Shahid Beheshti University, Tehran, Iran, in 2009, and the Dr.-Ing. degree from the Institute of Communication Acoustics (IKA), Ruhr-Universität Bochum, Bochum, Germany, in 2016.

From 2009 to 2012, he served as a Research Fellow in the EU Marie Curie Initial Training Network AUDIS, focusing on “Digital Signal Processing in

Audiology”. During his time at IKA from 2016 to 2018, he worked as a Postdoctoral Researcher specializing in instrumental assessment of speech intelligibility, speech enhancement, and information theory for signal processing. Subsequently, from 2018 to 2022, he served as a Signal Processing Engineer at HELLA GmbH & Co. KGaA, Lippstadt, Germany. His primary responsibility was the development of robust signal processing algorithms for automotive radar systems. Since 2022, he has been working as a Senior SW developer and Radar Expert at HELLA Aglaia Mobile Vision GmbH in Berlin. In this role, he focuses on the development of embedded software for Automotive Radar Systems.

Uwe Kühnau received the Diploma degree in physics and the Dr. rer. nat. degree in solid state physics from the University of Leipzig, Leipzig, Germany, in 1993 and 1998, respectively.

He started his industrial career in pre-development for automotive sensors at Hella in 2000 and later headed the advanced engineering for radar systems. He is currently Head of Radar Systems at Forvia.

![](images/e54cac963753841530d0498a8b8fab5745fb68b332f9c3cfd1948efdd350d104.jpg)

Nils Pohl (Senior Member, IEEE) received the Dipl.-Ing. and Dr.Ing. degrees in electrical engineering from Ruhr University Bochum, Bochum, Germany, in 2005 and 2010, respectively.

From 2006 to 2011, he was a Research Assistant with Ruhr University Bochum, where he was involved in integrated circuits for millimeterwave (mm-wave) radar applications. In 2011, he became an Assistant Professor with Ruhr University Bochum. In 2013, he became the Head of the Department of mm-wave Radar and High Frequency

Sensors with the Fraunhofer FHR, Wachtberg, Germany. In 2016, he became a Full Professor for Integrated Systems with Ruhr University Bochum. In parallel, he is head of the Research group for Integrated Radar Sensors at Fraunhofer FHR. He has authored or coauthored more than 200 scientific papers and has issued several patents. His current research interests include ultra-wideband mm-wave radar, design, and optimization of mm-wave integrated SiGe circuits and system concepts with frequencies up to 500 GHz and above, as well as frequency synthesis and antennas.

Prof. Pohl is a member of IEEE, VDE, ITG, EUMA, and URSI. He was a co-recipient of the 2009 EEEfCom Innovation Award, and a recipient of the Karl-Arnold Award of the North Rhine-Westphalian Academy of Sciences, Humanities and the Arts in 2013 and the IEEE MTT Outstanding Young Engineer Award in 2018. Additionally, he was co-recipient of the best paper award at EUMIC 2012, best demo award at RWW 2015, and best student paper awards at RadarConf 2020, RWW 2021 and EUMIC 2021.

![](images/61943bb2c39349c61f6cc5740fd2d7f682ad42331b24d8b4b80ac60c7c1312ff.jpg)

Rainer Martin (Fellow, IEEE) received the M.S.E.E. degree from Georgia Institute of Technology, Atlanta, in 1989, and the Dipl.-Ing. and Dr.-Ing. degrees from RWTH Aachen University, Aachen, Germany, in 1988 and 1996, respectively.

From 1996 to 2002, he was a Senior Research Engineer with the Institute of Communication Systems and Data Processing, RWTH Aachen University. From April 1998 to March 1999, he was a Technology Consultant at the AT&T Speech and Image Processing Services Research Lab (Shannon

Labs), Florham Park, NJ. From April 2002 until October 2003, he was a Professor of Digital Signal Processing at the Technische Universität Braunschweig, Braunschweig, Germany. Since October 2003, he has been a Professor of Information Technology and Communication Acoustics at Ruhr-Universität Bochum, Bochum, Germany, and from October 2007 to September 2009, the Dean of the Electrical Engineering and Information Sciences Department. He is coauthor with P. Vary of Digital Speech Transmission – Enhancement, Coding and Error Concealment (Wiley, 2006) and coeditor with U. Heute and C. Antweiler of Advances in Digital Speech Transmission (Wiley, 2008). His main research interests are signal processing, estimation and machine learning with applications in voice communication systems, hearing instruments, human–machine interfaces, and sensor networks.