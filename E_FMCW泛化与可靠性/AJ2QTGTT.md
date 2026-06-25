# Prior-Guided Deep Interference Mitigation for FMCW Radars

Jianping Wang, Runlong Li, Yuan He, and Yang Yang

Abstract—A prior-guided deep learning (DL) based interference mitigation approach is proposed for frequency modulated continuous wave (FMCW) radars. In this paper, the interference mitigation problem is tackled as a regression problem. Considering the complex-valued nature of radar signals, the complex-valued convolutional neural network is utilized as an architecture for implementation, which is different from the conventional real-valued counterparts. Meanwhile, as the useful beat signals of FMCW radars and interferences exhibit different distributions in the time-frequency domain, this prior feature is exploited as a regularization term to avoid overfitting of the learned representation. The effectiveness and accuracy of our proposed complex-valued fully convolutional network (CV-FCN) based interference mitigation approach are verified and analyzed through both simulated and measured radar signals. Compared to the real-valued counterparts, the CV-FCN shows a better interference mitigation performance with a potential of half memory reduction in low Signal to Interference plus Noise Ratio (SINR) scenarios. Moreover, the CV-FCN trained using only simulated data can be directly utilized for interference mitigation in various measured radar signals and shows a superior generalization capability. Furthermore, by incorporating the prior feature, the CV-FCN trained on only 1/8 of the full data achieves comparable performance as that on the full dataset in low SINR scenarios, and the training procedure converges faster.

Index Terms—Deep learning, Complex-Valued Convolutional Neural Network, prior feature, interference mitigation, FMCW

## I. INTRODUCTION

REQUENCY modulated continuous wave (FMCW) radars are widely used for automotive radar, vital sign detection, smart building surveillance, weather monitoring, etc. With the rapid expansion of the applications, the mutual interference among FMCW radars as well as surrounding wireless devices becomes an increasingly severe problem, which would mask weak targets, degrade target detection and even cause ghost targets.

A number of methods have been proposed for FMCW radar interference mitigation (IM), including radar system coordination, radar system design and waveform design, and signal processing. Radar system coordination can operate at both the transmitter (Tx) and receiver (Rx) end [1], which may introduce an additional communication module in the radar system. In contrast, at the Tx end, a new radar system or waveform can be designed to transmit the chirp signal with varying parameters (e.g., center frequency) to avoid the appearance of interferences. Besides, the interference can be suppressed in the RX end by applying the traditional signal processing approaches or the latest deep learning (DL) based approaches to the received radar signals. The signal postprocessing method does not require to design a new radar system and is easier to fit into existing radar chips.

Specifically, the traditional signal processing approaches can be classified into three categories: zeroing and reconstruction, estimation and subtraction, and digital beamforming. In [2], the amplitudes of interfered radar signals are replaced with zero, and the useful beat signals are reconstructed by an iterative method in the Fourier domain. However, the reconstruction algorithm would be inapplicable especially in the long interference duration situations. By contrast, the parameters of interfering signals can be estimated, and only the interference components are subtracted from the received signals [3], which requires more computational effort and long processing time. Meanwhile, an adaptive noise canceller (ANC) utilizing the symmetry of interferences in the frequency domain is used to remove the interferences in the positive frequency with lower computational complexity [4]. In [5], the interferences are reconstructed and subtracted by wavelet denoising (WD), whose performance would degrade as the proportion of interferences increases. Furthermore, the filtering can also be used for IM, which has a distortion of object peak values due to its non-linear nature [6]. Finally, in multiantenna systems, the interference from certain directions can be removed in the space domain by digital beamforming [7]. However, the targets’ signals scattered from the same directions are also suppressed.

The traditional signal processing approaches can effectively suppress the interferences and improve the targets’ detection probability for FMCW radars. However, these approaches generally require high computational complexity, and the performance depends on the manually selected parameters. Besides, most of the traditional approaches have made many assumptions to simplify the calculation and obtain analytical solutions, whose performance would significantly degrade in more complex scenarios.

Recent development in deep learning has shown its ability in feature extraction, and DL-based approaches are increasingly used for various signal processing problems [8], including interference mitigation for radar signals. In [9]–[11], a simple Convolutional Neural Network (CNN) with few parameters is used to suppress the interference and noise by operating on the range-doppler (RD) maps for FMCW radars. Then more complex network structures including Fully convolutional network (FCN) [12], Autoencoder [13] and U-Net [14] are proposed to process the frequency spectra or the RD maps of radar signals. These approaches extract the feature of interferences and subtract it from received signals. Similarly, in [15], the CNN and residual network (ResNet) are built to detect and remove the interference components respectively for synthetic aperture radars. Moreover, the Generative Adversarial Network (GAN) can be used to recover the missing signals after interference detection and zeroing [16]. Besides, Recurrent Neural Networks (RNNs) are also implemented in the time domain with low processing time [17], [18].

Compared to the traditional signal processing methods, the DL-based approaches require building a training dataset and designing the neural network architecture, which can automatically extract the critical features through training, distinguishing the targets’ scattered signals and interferences. The experimental results have shown its powerful interference mitigation ability. Moreover, the DL-based approaches can apply in more complex situations by learning a causal model from data instead of building a specific signal model. On the other hand, due to the limitation of a large-scale dataset including radar signals in various scenarios, it is hard to acquire satisfactory results for DL-based approaches. Additionally, with the existence of the overfitting problem, the features extracted by the network may be affected by noise. As a result, the performance of existing DL-based approaches is limited by the number of radar signals that are difficult to collect, and the total parameters may exceed the capacity of existing small memory-constrained radar sensors.

Generally, the beat signals of FMCW radars are acquired as complex-valued samples with I/Q receivers. The existing DLbased IM approaches all separate the complex-valued samples as real and imaginary parts and handle them as independent real-valued data with real-valued neural networks. Thus the implicit relationship between the real and imaginary parts of radar signals is not considered, which may cause the loss of the phase information that is necessary for further signal processing steps, for instance, classification and tracking. On the other hand, complex-valued convolutional neural network [19]–[21], which handles complex-valued data with the algebraic rules of complex numbers, can achieve better performance than the real-valued counterparts. Moreover, the complex-valued network has a more powerful representation ability and is robust to noise [22]. Its potential for faster learning, easier optimization, and better generalization performance has received increasing attention in various domains [23].

In this paper, considering the complex-valued nature of beat signals of FMCW radars, an interference mitigation approach based on complex-valued convolutional neural networks is proposed (see Fig. 1). Specifically, a complex-valued fully convolutional network (CV-FCN) is designed to suppress the interference and noise, which operates on the spectrogram in the time-frequency $\left( t \ – f \right)$ domain obtained by taking a shorttime Fourier transform (STFT) of a beat signal. Moreover, accounting for that the beat signals are shown as straight lines parallel to the time axis in the spectrogram while interferences exhibit as oblique lines in the $t \mathrm { - } f$ domain, we exploit this prior feature as a regularization term combined with the mean square error (MSE) loss function for training.

The contributions of this paper are summarized as follows:

Firstly, a CV-FCN-based approach is proposed for interference mitigation. By using complex convolutions and the activation function CReLU, a better interference mitigation performance with a potential of half memory reduction compared to the real-valued counterparts in low SINR scenarios is achieved.

Secondly, a prior-guided loss function is proposed by accounting for both data consistency between labels and the predicted $t \mathrm { - } f$ spectra and the expected prior frequency-sparse feature of the predicted spectra. A hyper-parameter is used to trade off between the data consistency and the expected prior feature of the predicted spectra. By adjusting the hyperparameter, the overfitting problem can be avoided, and the networks can be trained with a smaller dataset and faster convergence.

Thirdly, the proposed approach to IM can process radar signals with an arbitrary length in a sweep. Its performance is verified through both simulated and measured data, showing its effectiveness and superior generalization capability.

The remainder of this paper is organized as follows. Section II introduces the signal modelling and analysis. Section III elaborates the prior-guided interference mitigation approach based on complex-valued convolutional neural networks. The setups of numerical simulations for data synthesis and experimental measurements are described in Section IV. After that, the experimental results of the proposed method on the simulated and measured radar signals are presented in Sections V and VI. Finally, conclusions are drawn in Section VII.

## II. SIGNAL MODELLING AND ANALYSIS

Dechirping receiver is widely used for FMCW radar system to reduce the sampling requirement to the analog to digital

![](images/5ac1bbe4aa55f5c784e624985608bd41b179013aca67d4fa9a4b8d614f2a9311.jpg)  
Fig. 1. Signal processing flow of our propose approach for interference mitigation (IM).

![](images/d2dab24829b20784ac3cac008da9a8e3ed298f30449ca008adbd30ef3b429b72.jpg)  
Fig. 2. t-f diagram of beat signals contaminated by mutual interferences.

converters (ADC). After dechirping, the acquired beat signals contaminated by interferences can be written as [24]:

$$
y ( t ) = s ( t ) + f ( t ) + n ( t )\tag{1}
$$

where n(t) represents the thermal noise and measurement errors. $s ( t )$ is the useful beat signals and $f ( t )$ denotes the interferences, which are explicitly given by

$$
s ( t ) = \sum _ { k = 1 } ^ { N } \sigma _ { k } \exp \left[ j 2 \pi \left( - f _ { c } \tau _ { k } - K \tau _ { k } t + \frac 1 2 K \tau _ { k } ^ { 2 } \right) \right]\tag{2}
$$

$$
f ( t ) = \mathcal { F } _ { l p } \left[ p ^ { * } ( t ) \sum _ { m = 1 } ^ { M } f _ { m } ( t ) \right]\tag{3}
$$

where $0 < t < T _ { \mathrm { s w } }$ with sweep duration $T _ { \mathrm { s w } } . ~ f _ { c }$ is the center frequency, K is the chirp rate of the FMCW waveform, and $\tau _ { k }$ is the time delay of the scattered signal from the $k ^ { \mathrm { { t h } } }$ target relative to the transmitted one. $p ^ { * } ( t )$ is the reference signal used for dechirping, $f _ { m } ( t )$ denotes the $m ^ { \mathrm { t h } }$ interference and $\mathcal { F } _ { l p }$ is the low-pass filtering (LPF) operator.

In practice, the interference component $f ( t )$ could result from aggressor FMCW radars or other neighboring wireless devices. As analyzed in [24], the interferences can be, generally classified as four categories: (i) interference signal with the same chirp rate; (ii) interference signal with different chirp rate; (iii) CW interference; and (iv) transient interference. In case (i), when the beat signals resulting from interferences fall in the effective bandwidth of the LPF, it would result in horizontal lines along the time axis same as that of real targets’ signals in the $t \mathrm { - } f$ spectrum; thus, it would cause ghost targets, degrading the probability of detection and the false alarm rate. It is difficult to mitigate this kind of interference in the time or frequency domain, and this problem may be solved by designing a specific radar system or waveform in the space domain. In cases (ii)-(iv), the interferences lead to inclined thick lines or superposition of inclined thick lines in the $t \mathrm { - } f$ spectrum, which are different from the beat signals of targets. Therefore, without loss of generality, we consider interferences in case (ii) for demonstration in this paper. Note the approach is also applicable to handle interferences in cases (iii) and (iv).

Fig. 2 shows the $t \mathrm { - } f$ spectrum of an interferencecontaminated beat signal, where the horizontal lines along the time axis are the spectra of targets’ signal components while the inclined thick lines are the interferences. The interferences show different distributions determined by their amplitudes, chirp rates, duration times, and time delays relative to the reference signal for dechirping. Moreover, due to the positive time delay caused by wave propagation, the spectra of beat signals always exist in negative frequency (the sweep slope of the victim radar is positive). In contrast, the spectra of interferences spread in both positive and negative frequency in the $t \mathrm { - } f$ spectrum. Considering the different temporal and spectral features of targets’ signals and interferences, it is natural to investigate possible approaches to mitigate the interferences in the $t \mathrm { - } f$ domain by processing, for instance, the STFT spectrum.

Based on the differences, the interference mitigation problem can be tackled as a two-step interference detection and suppression problem by using the positive-frequency spectrum to detect if interferences exist or not. Besides, the recent development in deep learning techniques substantially improves the detection performance by exploiting multi-layer CNN. As a result, this problem is tackled as a single-stage regression problem based on deep learning in this paper, which means detecting and mitigating the interferences can be completed by only an end-to-end neural network.

## III. PRIOR-GUIDED DEEP INTERFERENCE MITIGATION

In this section, some basic modules used in the complexvalued convolutional neural network are first reviewed. Then the complex-valued fully convolutional network architecture and the prior-guided loss function proposed for FMCW radar interference mitigation are introduced, followed by the detailed description of the training procedure.

## A. Complex-valued modules

A complex-valued convolutional neural network is generally composed of various complex-valued modules, including complex convolution, complex-valued activation functions and complex batch normalization [22].

To take advantage of the existing deep learning platform developed for real-valued NN (e.g., TensorFlow [25]), a complex convolution can be implemented by explicitly performing realvalued convolutions among the real and imaginary parts of the related terms. Specifically, the complex convolution between a complex filter $\mathbf { W } = \mathbf { A } + j \mathbf { B }$ and a complex vector $\mathbf { h } = \mathbf { x } + j \mathbf { y }$ can be expressed as:

$$
\mathbf { W } * \mathbf { h } = ( \mathbf { A } * \mathbf { x } - \mathbf { B } * \mathbf { y } ) + j ( \mathbf { A } * \mathbf { y } + \mathbf { B } * \mathbf { x } )\tag{4}
$$

where $j$ is the imaginary unit. A and B are real matrices, and x and $\mathbf { y }$ are real vectors, respectively.

Similar to the activation functions for real-valued CNNs, complex-valued activation functions introduce nonlinearity to complex-valued CNNs to increase their representation capabilities [22], [26], [27]. Complex Rectified Linear Unit (CReLU) is one of the most popular activation functions used in complex-valued CNNs [22], which applies traditional realvalued ReLU on both real and imaginary parts of a complexvalued input and is expressed as:

$$
\mathrm { C R e L U } ( z ) = \mathrm { R e L U } ( \Re ( z ) ) + j \mathrm { R e L U } ( \Im ( z ) )\tag{5}
$$

![](images/87ee54d084b349b745f5b98d3fd152e440c29ba52c3cc1f4d46be57180ae25fa.jpg)

Fig. 3. Proposed complex-valued fully convolutional network architecture (CV-FCN). It uses complex-valued activation function CReLU and the complex convolution operation (ComplexConv), where the kernel size is 3×3 and the number of filters is x except for the last layer.  
![](images/ccdf790c319bdd4573e5ff58979c5bb0e8cf12b5f27702403824a7e06debe263.jpg)  
Fig. 4. Proposed real-valued fully convolutional network architecture (RV-FCN) for comparison. It uses traditional real-valued ReLU and the convolution operation (Conv), where the kernel size is 3×3 and the number of filters is 2x except for the last layer.

where <(x) and =(x) extract the real and imaginary parts of a complex number x. Compared to other complex-valued activation functions (e.g., zReLU [27] and modReLU [26]), CReLU generally achieves the best performance in inverse problems. Therefore, it is utilized in this paper as well.

## B. Network Architecture

The interference mitigation problem is tackled as a regression problem. As targets’ beat signals and interferences show distinct distributions in the $t \mathrm { - } f$ domain, the $t \mathrm { - } f$ domain spectral diagram obtained with the STFT algorithm is naturally used for IM. Considering the complex-valued nature of FMCW radar signals in the $t \mathrm { - } f$ domain, a complex-valued fully convolutional network architecture is designed for interference mitigation with the basic complex-valued modules (see Fig. 3). The proposed CV-FCN is composed entirely of complex convolution layers, each of which except the last convolution layer is followed by the complex-valued activation function CReLU. The number of filters is fixed to one in the last convolution layer, which is used only to produce the output.

The t-f spectrum of the interfered radar signal is set as the input of the network, and its counterpart of the associated reference (i.e., the clean signal) is used as the label. Since the existing deep learning tools do not support the complex-valued input data, the real and imaginary parts of input samples are separated into two channels. Meanwhile, the square kernels with size 3×3 are used to deal with the two-dimensional input samples, and the zero-padding is used in the complex convolutional layer to ensure the output t-f spectrum have the same shape as the input.

## C. Loss function

MSE is generally used as a loss function in the DL-based interference mitigation approaches [28], which calculates the difference between the output of the network and the related label. However, the performance of the network trained with the MSE as the loss function is limited by the size of the training dataset. With the increase of the network’s total parameters and training iterations, the overfitting problem cannot be avoided, making it challenging to extract critical features. Moreover, due to the lack of real interfered radar signals and related reference data in practice, synthetic data based on the analytical signal models are commonly generated to build the training dataset. However, the analytical model used for data synthesis is generally derived based on certain assumptions (e.g., perfect radar system and frequency-independent scattering property of targets) for simplification, which may make the synthetic dataset impractical to contain all the features of the data acquired in various realistic scenarios. Consequently, the performance of the networks trained using the MSE with only simulated radar signals would degrade when utilized to real data. To avoid the overfitting problem and improve the generalization of the trained network, explicitly incorporating the prior information could be of benefit for real data.

As shown in Section II, the interferences lead to timevarying beat frequencies after dechirping while the frequencies of targets’ beat signals are constant. The projection of the interference on the frequency axis is a line, while the projections of targets’ beat signals on the frequency axis are some points. Thus, interferences and targets’ beat signals show different sparsities along the frequency axis (i.e., different sparsities in the range profiles). To exploit this prior feature of interferences and beat signals in the $t \mathrm { - } f$ domain, we introduce the $L _ { 2 , 1 }$ norm of the recovered $t \mathrm { - } f$ domain spectrum (i.e., the output of the proposed neural network) as a regularization term for the NN training in addition to the traditional loss function MSE. The complete loss function is expressed as

$$
l ( { \bf S } , \tilde { \bf S } ) = \| { \bf S } - \tilde { \bf S } \| _ { F } ^ { 2 } + \lambda \| \tilde { \bf S } \| _ { 2 , 1 }\tag{6}
$$

$$
\| \tilde { \mathbf { S } } \| _ { 2 , 1 } = \sum _ { j = 1 } ^ { N } \sqrt { \sum _ { i = 1 } ^ { M } | \tilde { S } _ { i j } | ^ { 2 } }\tag{7}
$$

where $\| \mathbf { X } \| _ { F }$ and $\| \mathbf { X } \| _ { 2 , 1 }$ represent Frobenius norm and $L _ { 2 , 1 }$ norm of a matrix X, respectively, $\tilde { \mathbf { S } } \in \mathbb { C } ^ { M \times N }$ is the matrix of the recovered spectrum in the $t \mathrm { - } f$ domain with the row and column related to the frequency and time dimensions, respectively, and $\mathbf { S } \in \mathbb { C } ^ { M \times N }$ is the label. $\| \mathbf { S } - \tilde { \mathbf { S } } \| _ { F } ^ { 2 }$ is the MSE loss function, and $\| \tilde { \mathbf { S } } \| _ { 2 , 1 }$ is the $L _ { 2 , 1 }$ norm of $\tilde { \mathbf { S } } _ { : }$ , as shown in (7). λ is a hyper-parameter used to make a trade-off between the MSE (i.e., data consistency) and the prior feature.

Due to the introduced regularization term $\| \tilde { \mathbf { S } } \| _ { 2 , 1 }$ , the overfitting problem can be avoided as much as possible. Moreover, as the regularization term $\| \tilde { \mathbf { S } } \| _ { 2 , 1 }$ provides solid expert knowledge, it boosts the convergence rate of the network training (i.e., the network can be trained with fewer iterations) and the size of the dataset needed for training can be significantly reduced. Besides, the feature used for IM is the fusion of the prior information and the features extracted from the CNNs, which can motivate better generalization capability.

## D. Training Setup

Before being fed into the network, the complex-valued input samples are normalized. Specifically, the normalization method can be described as:

$$
\tilde { \mathbf { Y } } ( m , n ) = \frac { \mathbf { Y } ( m , n ) } { \underset { 1 \leq m \leq M } { \operatorname* { m a x } } | \mathbf { Y } ( m , n ) | _ { 2 } }\tag{8}
$$

where Y is the matrix of the STFT spectrum of beat signals contaminated by interferences, and m and n are the row and column indices of an entry of the matrix.

After being processed by the network, the matrix of the recovered spectrum is multiplied by the denominator in equation (8) for further processing.

In the network training process, the complex weight initialization strategy [22] was used to initialize the parameters of complex convolution layers. The Adam algorithm with a fixed learning rate of 0.001 and 32 input samples per batch was used for training. We end the training at epoch 100 after good convergence was observed. Moreover, all the models were trained on a single NVIDIA 2080Ti graphics processing unit (GPU). The code was implemented using Keras and Tensorflow tools.

## IV. DATASETS

In this section, the setups of numerical simulations for data synthesis and experimental measurements are introduced in detail, and then the data split algorithm for a more flexible model is described.

TABLE I  
PARAMETERS OF THE VICTIM RADAR
<table><tr><td>Parameter</td><td>Value</td><td>Parameter</td><td>Value</td></tr><tr><td>Center frequency</td><td>3GHz</td><td>Velocity</td><td>30 km/h</td></tr><tr><td>Duration of a sweep  $T _ { \mathrm { s w } }$ </td><td> $4 0 0 \mu s$ </td><td>Window type</td><td>Hamming</td></tr><tr><td>Bandwidth</td><td> $4 0 \mathrm { { M H z } }$ </td><td>Window length</td><td>256</td></tr><tr><td>Chirp rate K</td><td> $1 0 ^ { 1 1 } \mathrm { H z / s }$ </td><td>Overlap length</td><td>255</td></tr><tr><td>Sampling frequency</td><td> ${ 1 2 } \mathrm { M H z }$ </td><td>FFT points</td><td>256</td></tr><tr><td>Maximum detection distance</td><td>8 km</td><td></td><td></td></tr></table>

TABLE II  
PARAMETERS OF THE TARGETS AND INTERFERENCE
<table><tr><td>Parameter of Targets</td><td>Value</td><td>Parameter of Interferences</td><td>Value</td></tr><tr><td>Number</td><td> $\mathcal { U } \{ 0 , 2 0 \}$ </td><td>Number</td><td>U{1, 20}</td></tr><tr><td>Distance</td><td>U(8, 8000) m</td><td>Amplitude</td><td>U(0,3)</td></tr><tr><td>Amplitude</td><td>U(0,3)</td><td>Center frequency</td><td>3GHz</td></tr><tr><td>Phase</td><td>U(0,2π)</td><td>Chirp rate</td><td> $\mathcal { U } ( - 2 K , 2 K )$ </td></tr><tr><td>Velocity</td><td> $\mathcal { U } ( 0 , 8 0 ) \mathrm { k m / h }$ </td><td>Duration</td><td> $\mathcal { U } ( 0 , T _ { \mathrm { s w } } )$ </td></tr><tr><td>SNR SINR</td><td> $\mathcal { U } \{ - 2 0 , 2 0 \} \mathrm { d B }$   $\mathcal { U } [ - 4 0 , 2 0 ] \mathrm { d B }$ </td><td>Delay time</td><td> $\begin{array} { r } { \mathcal { U } \left( \frac { - T _ { \mathrm { s w } } } { 2 } , \frac { T _ { \mathrm { s w } } } { 2 } \right) } \end{array}$ </td></tr></table>

## A. Radar signals synthesis

Due to the difficulties in acquiring both interfered radar echoes and their related references in practice, especially for dynamic scenarios, in this paper we decided to use synthetic FMCW radar signals for the proposed neural network training and then employ both synthetic and measured data for test.

For data generation, a victim FMCW radar with the parameters described in Table I was considered. To emulate the scenarios with various scatterers and different interferences, each parameter of targets and interfering signals was randomly chosen from a uniform distribution $\mathcal { U } [ a , b ]$ for continuous variables in a closed interval or $\textstyle { \mathcal { U } } ( a , b )$ for continuous variables in an open interval or $\mathcal { U } \{ a , b \}$ for discrete variables, where a and b define the bounds of an interval. The detailed intervals of the values of the parameters of targets and interfering signals are shown in Table II, where K and $T _ { s w }$ refer to the chirp rate and sweep duration of the victim radar in Table I. Moreover, complex white Gaussian noise was added to synthetic signals to account for system noise and measurement errors. To characterize the interference-contaminated signals in the presence of complex white Gaussian noise, Signal to Noise Ratio (SNR) and Signal to Interference plus Noise Ratio (SINR) are used as metrics. The SNR ranges from -20 dB to 20 dB with step size of 5 dB while the SINR takes values randomly from a uniform distribution as shown in Table II.

After synthesizing the time-domain radar signals according to the setups described above, their time-frequency spectra are generated through the STFT algorithm. Specifically, the STFT was implemented by using a 256-point hamming window with a hop size of one for signal segmentation and 256-point fast Fourier transform (FFT) for spectrum calculation (see Table I). Since the beat signals of targets and interferences are synthesized according to controllable parameters, we can obtain both the interfered signals and the associated references (see the example in Fig 5).

![](images/4fa441860a4573e3c7d039ae1c9eadbd06e67ee3f56de5a05bb4e49c2fb4c9a8.jpg)  
(a) Interfered signal

![](images/5c73bedd179f408d3cd47a699f3925e0b54b9e1a87e9da70cbafb2f2d47d6acf.jpg)  
Fig. 5. t-f diagram of simulated radar signals.  
(b) Clean signal

TABLE III  
PARAMETERS OF THE PARSAX RADAR
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Center frequency</td><td>3.315 GHz</td></tr><tr><td>Duration of a sweep  $T _ { \mathrm { s w } }$ </td><td>1 ms</td></tr><tr><td>Bandwidth</td><td>30 MHz</td></tr><tr><td>Chirp rate K</td><td>30 MHz/ms</td></tr><tr><td>Sampling frequency</td><td>400 MHz</td></tr></table>

![](images/298bc0f12949cda3c3effef2f03fc1565e16a3ba7cbb6226b5a9f6f68445c563.jpg)  
(a) Camera visual image

![](images/665082476b30fe6367eb039a3c752de798b178d7da8d3ff9b3d38e3b6554f5af.jpg)  
(b) t-f diagram  
Fig. 6. Measured radar signals collected in the street scenario.

## B. Experimental Measurements

The experimental data in this paper were collected with the full-polarimetric PARSAX radar in TU Delft, which has two orthogonally polarized transmitting channels and four receiving channels for full polarimetric signal acquisition. We simultaneously use a horizontally polarized (H-pol) channel to emit a fixed FMCW signal and the vertically polarized (V-pol) channel to transmit an arbitrary FMCW-type waveform with various chirp rates, time duration, bandwidth, and time delay relative to the beginning of the signal in the H-pol channel.

The full-polarimetric signals scattered from the illuminated scene arrive at the receiving antenna at the same time. After passing through an orthomode transducer, the H-pol (i.e., HH and VH) and V-pol (i.e., HV and VV) scattered signals can be separated. However, the HH and VH (correspondingly HV and VV) signals inevitably interfere with each other at the receiving channels. As the HH (correspondingly VV) signals are generally much stronger than the VH (correspondingly HV) signals, the interference impact of HH (VV) on the VH (HV) is generally much severer. ${ \mathrm { S o } } ,$ the acquired HV signals are used to construct the experimental dataset used in this paper. The radar data were measured by illuminating three scenes: an industrical chimney, a rotating wind turbine, and a street with moving cars. In total, 500-sweep radar data were measured with various interference signals for each sweep. As the latter two scenes were dynamic, acquiring the related references with our radar system was impractical, which is generally the case in practice. As an example, Fig. 6 illustrates the street scenario at a time instant and the $t \mathrm { - } f$ spectrum of the acquired signal. As the references are unavailable, the experimental data are only used to test the trained neural networks.

## C. Data Split

In principle, the shape of the STFT spectra of radar signals is determined by the number of sampling points in a sweep and parameters of the STFT algorithm, and most CNNs can only process input samples of specific shapes. In order to process radar signals of different shapes in the $t \mathrm { - } f$ domain, the matrix of the STFT spectrum is split into a combination of smaller matrices before being fed into the network, which can be described as Algorithm 1. Each element in the matrix of the recovered spectrum is predicted according to both the past and future time-frame information, and the phase is guaranteed to be continuous. In our experiments, the $N _ { p }$ is set to 4, and the shape of the input sample (i.e., $M \times M )$ is 256×256.

## V. SIMULATION RESULTS

In this section, the prior-guided deep interference mitigation approach based on the CV-FCN proposed in Section III-B is analyzed and demonstrated using synthetic FMCW radar signals. Firstly, the performance metric used for the quantitative evaluation of interference mitigation performance in our experiments is presented. Then the optimal network architecture based on the CV-FCN is obtained by grid search using MSE as the loss function, including the size and number of filters in each convolution layer, depth of the network, and additional residual connection. Next, the CV-FCNs are compared with the real-valued counterparts over a variety of network depths to show the superiority of complex-valued representation. After that, the prior-guided loss function is used for training, and its effects on the training iterations (i.e., convergence rate) and the size of the training dataset are investigated as well. Finally, our proposed approach is compared with the state-of-the-art conventional interference mitigation algorithms.

## A. Performance Metrics

To quantitatively evaluate the performance of different interference mitigation methods, the SINR of a recovered radar signal relative to the clean reference is used as a performance metric. The SINR cannot only measure the remaining interferences and noise in the recovered signal, but also represent the signal distortion. It is defined as:

$$
\mathrm { S I N R } = 1 0 \log \left( \frac { | \mathbf { s } | _ { 2 } ^ { 2 } } { | \tilde { \mathbf { s } } - \mathbf { s } | _ { 2 } ^ { 2 } } \right)\tag{9}
$$

where ˜s is the recovered signal in the time domain, and s is the corresponding reference. Note the SINR is inversely proportional to the error vector magnitude (EVM) [9].

Algorithm 1: Data processing   
input : Interfered STFT maps Y $\overline { { ( L \times N \times M , } }$ L   
number of maps, $N$ time samples per chirp,   
$M$ number of FFT points). $N _ { p } .$ , number of   
overlap points   
output: Recovered STFT maps $\tilde { \bf S }$ $( L \times N \times M )$   
// Data split   
1 $p = N / ( M - 2 N _ { p } ) + 1 ;$   
2 $\mathbf { T } [ : L , : , : ] { = } \mathbf { Y } [ : , : M , : ] ;$   
3 for $i = 1$ to $( p - 2 )$ do   
4 $\mathbf { T } [ i \times L : ( i + 1 ) \times L , : , : ] { = } \mathbf { Y } [ : , i \times ( M - 2 N _ { p } )$   
$i \times ( M - 2 N p ) + M , : ] ;$   
5 end   
6 $\mathbf { T } [ ( p - 1 ) \times L : p \times L , 0 : N - ( p - 1 ) \times ( M - 2 N _ { p } ) , : ]$   
$\mathbf { \Gamma } = \mathbf { Y } [ : , ( p - 1 ) \times ( M - 2 N _ { p } ) : N , : ] ;$   
$/ /$ Data normalization   
7 for $i = 0$ to $( p \times L )$ do   
8 scl[i] = Max (abs $( \mathbf { T } [ i , : , : ] ) ;$   
9 $\mathbf { T } [ i , : , : ] { = } \mathbf { T } [ i , : , : ] \ / \ s c l [ i ] ) ;$   
10 end   
11 $\tilde { \mathbf { T } } = \mathop { \mathrm { M o d e 1 P r e d i c t } } \left( \mathbf { T } \right)$   
// Data denormalization   
12 for $i = 0$ to $( p \times L )$ do   
13 $| | \tilde { \bf \Delta T } [ i , : , : ] = \tilde { \bf T } [ i , : , : ] \times s c l [ i ] ) ;$   
14 end   
// Data integration   
15 $\tilde { \bf S } [ : , : M - N _ { p } , : ] = \tilde { \bf T } [ : L , : M - N _ { p } ,$ :];   
16 for $i = 1$ to $( p - 2 )$ do   
17 $\tilde { \mathbf { S } } [ : , i \times ( M - 2 N _ { p } ) + N _ { p } :$   
$i \times ( M - 2 N _ { p } ) \dot { + } M - N _ { p } , \dot { \ z } ] =$   
$\tilde { \mathbf { T } } [ i \times L : ( i + 1 ) \times L , N _ { p } : \tilde { M } - N _ { p } , : ] ;$   
18 end   
19 $\tilde { \bf S } [ : , ( p - 1 ) \times ( M - 2 N _ { p } ) + N _ { p } : N , : ] =$   
$\tilde { \bf T } [ ( p - 1 ) \times L : p \times L , N _ { p } : N - ( p - 1 ) \times ( M - 2 N _ { p } ) , : ] ;$

![](images/de3c4ac7a4456b83f635ab4956484f8cb5bc767ba3d35a6c18620f87c374dbd0.jpg)  
Fig. 7. The performance comparison of different network architectures based on the CV-FCN trained using MSE as the loss function, where 10-16-m means the network has three convolution layers, the number of filters in each layer is 16 and the kernel size is m×m.

## B. Network architecture optimization

To find an optimal network architecture based on the proposed CV-FCN for FMCW radar interference mitigation, a parameter search is performed using MSE as the loss function.

Firstly, the problem of how to design the number of filters in each convolution layer is investigated. Three different network architectures denoted as Type I, II, and III are implemented for comparison. Except for the last layer, the number of filters in each convolution layer is fixed to constant in Type I, and the number of filters is doubled or halved in each convolution layer for Type II and Type III, respectively. The performance comparison of different architectures is shown in Fig. 7, the average SINR of all evaluated architectures is given, and the xaxis indicates the number of total parameters of the network. We change the number of parameters by varying the depth of the network, the number of filters in each layer and the kernel size. We can see from the figure that the CV-FCNs where the number of filters is fixed to constant (Type I) obtain better results. In fact, the number of filters is doubled in each convolution layer for the famous CNN architectures such as VGG [29]. Due to the use of the pooling layer in VGG, the number of channels is doubled in each layer to ensure the information amount of the connected convolution layers does not differ too much. Since the pooling layer is not used in the CV-FCN to avoid signal distortion, the architecture where the number of filters is fixed to constant is more suitable.

Based on the conclusion, the CV-FCNs (Type I) with different numbers of total parameters are compared as shown in Fig. 7. The features of targets’ beat signals and interferences in the $t \mathrm { - } f$ domain are relatively simple, a larger number of filters or a deeper network is unnecessary. It follows that the maximum average SINR is obtained using a model (Model A) with ten layers and a kernel size of $3 \times 3 .$ . Except for the last layer, the number of filters in each convolution layer is fixed to 16. Moreover, we compared the CV-FCNs with kernels of $3 \times 3$ (Model A) and $5 \times 5$ (Model B). Although the number of total parameters in Model B triples, it leads to an average SINR 0.43 dB lower than that by Model A. So, the kernel size of $3 \times 3$ is used in the following experiments.

In recent years, researchers [15] have shown that introducing the residual connection can promote better backpropagation of gradient, avoiding the problems of gradient diminishing and explosion during training. To analyze the effect of residual connection for complex-valued networks, an additional residual connection is added between the input and output of the CV-FCN, resulting in a complex-valued residual network (CV-ResNet) used for comparison with CV-FCN. Except for one additional residual connection, the other layers and parameters remain unchanged. The performance comparison is shown in Fig. 8, and the result indicates that the CV-FCN has a better performance especially in low SINR scenarios. The beat frequency of the targets’ signals is constant, which results in the horizontal lines in the $t \mathrm { - } f$ spectrum. The features of the targets’ beat signals can be extracted by the convolution filters of CV-FCN, while the filters in CV-ResNet deal with the features of interferences, which show inclined lines with different slopes, intensities, and durations in the $t \mathrm { - } f$ spectrum and are relatively more complex. Different features extracted explain why the residual connection does not work well. However, the CV-ResNet may acquire better performance in other IM applications where signals are more complex than interferences.

![](images/d07dc00da881ddbae7d491fcafac424ec6584d0bd671f9a3c7edabdbbe3f5bd5.jpg)  
Fig. 8. The performance comparison of the CV-FCN with CV-ResNet, where d means the number of convolution layers in the network.

![](images/138ca8182955e7fd766e48ff71c40ac966f1118b09e72f657e5dfc34aa7e6976.jpg)  
Fig. 9. The performance comparison of the CV-FCNs with the corresponding RV-FCNs, where d means the number of convolution layers in the network.

## C. Performance comparison with real-valued networks

In order to analyze the effect of complex-valued networks in the radar signal processing chain, we compared the CV-FCNs with their real-valued counterparts over a variety of network depths.

The real-valued FCN (RV-FCN) is constructed using the real-valued convolution layer and the ReLU activation function to replace the corresponding complex modules. In the complex-valued networks, the number of complex filters in each layer is the number of complex feature maps. It is also the effective number of feature maps for each of the real and imaginary parts. To obtain the same number of feature maps for performance comparison, the number of filters in each layer in RV-FCNs is twice that in CV-FCNs, and the other parameters remain unchanged (as shown in Fig. 4).

TABLE IV  
COMPARISON OF THE CV-FCN WITH RV-FCN
<table><tr><td>Method</td><td>filter number</td><td>depth</td><td>parameter</td><td>SINR (dB) in low SINR scenarios1</td></tr><tr><td rowspan="7">CV-FCN</td><td rowspan="7">16</td><td>6</td><td>19170</td><td>3.0872</td></tr><tr><td>7</td><td>23810</td><td>4.1154</td></tr><tr><td>8</td><td>28450</td><td>2.5828</td></tr><tr><td>9</td><td>33090</td><td>3.7518</td></tr><tr><td>10</td><td>37730</td><td>4.4528(optimal)</td></tr><tr><td>11</td><td>42370</td><td>4.1615</td></tr><tr><td>12</td><td>47010</td><td>4.0407</td></tr><tr><td rowspan="6">RV-FCN</td><td></td><td>6 7</td><td>38178</td><td>2.5821</td></tr><tr><td>32</td><td></td><td>47426</td><td>3.8125</td></tr><tr><td></td><td>8</td><td>56674</td><td>1.8419</td></tr><tr><td></td><td>9</td><td>65922</td><td>0.8446</td></tr><tr><td></td><td>10</td><td>75170</td><td>2.1030</td></tr><tr><td></td><td>11</td><td>84418</td><td>4.0085(optimal)</td></tr><tr><td></td><td></td><td>12</td><td>93666</td><td>2.8022</td></tr></table>

<sup>1</sup> The SINR of interfered signals is between -40 dB and -20 dB.

The performance comparison is shown in Fig. 9, where the CV-FCNs of different depths show a better performance in low SINR scenarios compared to the real-valued counterparts. In the interference mitigation task, it is more meaningful to consider the performance in low SINR scenarios. The detailed parameters and quantitative results of the CV-FCNs and RV-FCNs are shown in Table IV. When the SINR of interfered signals is between -40 dB and -20 dB, all the CV-FCNs with different depths show better results (in bold red font), and the SINRs of the beat signals recovered by CV-FCNs are on average 1.1 dB higher than that by RV-FCNs. Moreover, due to complex multiplication and half the number of filters in each layer in the CV-FCN, its parameter amount is half of the real-valued counterparts.

Next, we compared the optimal CV-FCN, whose total parameters are 37730, with the optimal RV-FCN whose total parameters are 84418. With the number of total parameters reduced by 55.3%, the CV-FCN achieves almost the same performance as the RV-FCN. In the computer’s memory, the optimal RV-FCN requires 1.04 megabytes of memory, while the CN-FCN requires only 525 kilobytes. Additionally, the SINR of recovered signals has improved from -0.54 dB to 0.93 dB when the SINR of the interfered signals is between -40 dB and -35 dB. This suggests that the CV-FCN can be better used in practical applications due to the limitation of the hardware memory and its superior performance in suppressing strong interferences.

## D. Effects of prior-guided loss function

In Section III-C, we proposed the prior-guided loss function based on the different distributions of targets’ beat signals and interferences in the spectrogram. In this part, we use the prior-guided loss function instead of MSE to train the obtained optimal CV-FCN (Model A) in Section V-B. The hyper-parameter λ in equation (6) is used to make a trade-off between data consistency and prior knowledge. Note that the prior-guided loss function becomes the MSE when λ = 0.

1) Effect on convergence rate of training: a training dataset containing 4320 samples (t-f maps) is generated. Then, without loss of generality, λ = 0 and $\lambda = 4 0 0$ were used in the loss function (6) for comparison, and in each case the CV-FCN was trained for different epochs ranging from 20 to 100 with a step size of 20. The performance of the obtained CV-FCNs is shown in Fig. 10. One can see that the performance of the CV-FCN improves with the increase of training epochs for both cases of $\lambda = 0$ and $\lambda = 4 0 0$ . In low SINR scenarios, the CV-FCN trained for fewer epochs achieves comparable results as that trained for 100 epochs when the prior information was incorporated $( \mathrm { i . e . , } \lambda = 4 0 0 )$ .

![](images/3916c18e807a48991b59f13b0c68f1f5ac2422d340ecd8a6a31fdacac94978dd.jpg)  
Fig. 10. The performance comparison of CV-FCNs trained using all the 4320 samples.

The network has not yet learned enough features to suppress the interference components as the training epochs are less than 100. With the introduced regularization term, the features needed for interference mitigation can be extracted faster by training. On the other hand, the CV-FCN using the MSE as the loss function $( \mathrm { i . e . , } \lambda = 0 )$ converged when trained for 100 epochs according to Fig. 10. The MSE is sufficient to help the network to extract the correct features, and introducing $L _ { 2 , \cdot }$ norm does not make a difference in the performance. As a result, the CV-FCN trained using the prior-guided loss function where λ is 400 reaches almost the same results in low SINR scenarios with only 20 training epochs. By contrast, in the high SINR scenarios, the interference components are reduced, and the noise becomes the dominant disturbance to the signal. Thus the MSE becomes the key part in the prior-guided loss function. Moreover, the regularization impact of $L _ { 2 , 1 }$ norm becomes weaker for a fixed value of λ. This can explain the fact that the performance improvement in high SINR scenarios is not obvious. One possible solution is to adjust the hyperparameter λ according to the SNR to overcome this problem.

2) Effect on the size of training dataset: To evaluate the effect of prior knowledge incorporation in the loss function on the size of the dataset required for training, three datasets of different sizes, i.e., $1 / 2 , 1 / 4 .$ , and $1 / 8$ of the training dataset in section V-D1, were generated. Based on the convergence analysis in section V-D1, we set the training epochs to 100. Fig. 11 shows the performance of the CV-FCNs trained using the datasets of different sizes when λ takes various values.

According to Fig. 11(a)-(c), the SINRs of recovered signals generally degrade with the decrease of the sizes of training datasets. The smaller size of the training dataset used, the severer the SINR degradation compared to that obtained with the full dataset. However, with the increase of λ, the SINRs of recovered signals have been improved especially in low SINR scenarios, and a more noticeable improvement can be seen for a smaller training dataset.

To facilitate comparison of the regularization effect of the prior knowledge on the size of training dataset, the SINRs of recovered signals with $\lambda ~ = ~ 4 0 0$ in Fig. 11(a)-(c) are shown together in Fig. 12. It is clear that reducing the size of the training dataset results in performance degradation over a wide range of SINRs of input signals. But with the additional prior information offered by the $L _ { 2 , 1 }$ norm, the CV-FCNs trained on smaller datasets achieve comparable performance as that on the full dataset in the low SINR scenarios, even when reducing the size of the training dataset to one eighth. This is because that when the training dataset is small, the features extracted by the network using the MSE as a loss function would be insufficient for interference mitigation; thus, the network’s performance would worsen. Incorporating the prior information offered by $L _ { 2 , 1 }$ norm is helpful to guide and improve the features extracted for interference mitigation, compensating for the effect of data shortage. Therefore, the proposal interference mitigation approach is attractive for small data learning by introducing prior knowledge.

To demonstrate the performance of the CV-FCN (Model A) trained with 1/8 of the full data (i.e., 540 samples), Fig. 13 illustrates the interference mitigation results of an interfered beat signal of two point targets. Due to strong interferences between $1 0 0 \mu s$ and $2 5 0 \mu s$ in the beat signal, the weak target is almost immersed in the raised noise floor (see Fig. 13(a)-(b)). After being processed with the CV-FCN obtained with $\lambda \ = \ 0 ,$ , the interferences and noise are significantly suppressed, but some residual interference components are still observed (Fig. 13(c) and (e)). With the increase of $\lambda ,$ the residual interferences and noise are further mitigated (see Fig. 13(f)-(h)), and consequently the noise floor of the range profile decreases as well (Fig. 13(i)), which would improve the probability of target detection.

Therefore, by tunning the hyper-parameter λ, the prior information characterized by $L _ { 2 , 1 }$ norm can enforce the CV-FCN to extract meaningful features for interference mitigation faster during training, thus accelerating the convergence rate of training. Moreover, by incorporating the prior information, the proposed CV-FCNs can be trained with a smaller dataset, which is attractive for interference mitigation problems as it is generally very difficult to acquire labeled real radar data in practice, especially for dynamic scenarios.

## E. Comparative Analysis with Other Techniques

The performance of our proposed approach is compared with several state-of-the-art interference mitigation methods, including traditional signal processing approaches such as the Wavelet Denoising (WD) based method [5], Adaptive Noise Canceller (ANC) [4], CFAR-Z and CFAR-AC [30], and DLbased approaches such as CNN-based method [9] and ResNetbased method [15]. We used the simulated radar signals for test and quantitatively evaluated the performance of different methods. Fig. 14 shows the SINRs of the obtained signals after interference mitigation with different approaches. Due to the ResNet was designed to process the SAR images, in our experiments, the number of filters of the ResNet is set to half of that in [15] for FMCW radar signal processing. The CV-FCN is trained using the prior-guided loss function where λ = 400 and the CNN and ResNet are trained using the MSE loss function.

![](images/02aaafee7c8afb52daaead0968a821cb77f188069a67c1c638dd38d147c377f4.jpg)  
(a)

![](images/fbcfe1cf0442f7570a45387582d75792c2b599c1619535c21ef0ac1e30cd6adf.jpg)  
(b)

![](images/8f150c2c6f585f8b47bab01ca90c1473ad4d1bff872e272c955845e4740c249e.jpg)  
(c)  
Fig. 11. Performance comparison of CV-FCNs trained with the datasets of different sizes using the prior-guided loss function. (a) 1/2 dataset (2160 samples), (b) 1/4 dataset (1080 samples) and (c) 1/8 dataset (540 samples).

![](images/26cb97fa3be470e512066f72986400b60dc14a67e06bcae081496c91dca17a37.jpg)  
Fig. 12. The performance comparison of CV-FCNs trained using different size of the dataset.

The comparative results show that our proposed CV-FCN based prior-guided IM approach is obviously better than other methods. Specifically, the cfarZ and cfarAC use constant false alarm rate (CFAR) to detect the interference components of acquired beat signals in the time-frequency spectrum. The detection accuracy is determined by the selected parameters. Then cfarZ uses zeroing to mitigate detected interferences, which naturally removes targets’ beat signals at the same time. Different from cfarZ, cfarAC uses amplitude correction (AC) to reconstruct the beat signals removed by zeroing, which shows better performance than cfarZ. Besides, WD method can extract and remove the interferences in the wavelet domain, which shows a good performance in low SINR scenarios. In the ANC method, the negative half of the FFT spectrum is used as the input of its reference channel, and the filtering step size is manually adjusted. As described, the performance of the above traditional signal processing methods depends on a proper selection of a few manually adjustable parameters. Over a wide range of the SINR variations, their performance is not good as the selected DL-based methods<sup>1</sup>.

On the other hand, our proposed CV-FCN achieves better performance expecially in low SINR scenarios with only 12% the number of total parameters of the ResNet. The effect of residual connection has been verified and discussed in Section V-B, which is not suitable for extracting the feature of targets beat signals. The superior performance compared with other NNs shows the advantage of network architecture optimization by grid search, complex-valued representation in radar signal processing, and the prior feature offered by $L _ { 2 , 1 }$ norm.

## VI. MEASUREMNT RESULTS

In this section, the radar signals measured as described in Section IV-B are used to verify the generalization of our proposed prior-guided CV-FCN based IM approach.

We consider the scene of industrial chimneys. Due to the limitation of the experimental condition, the clean reference signal cannot be obtained. The qualitative results, including the signal waveforms in the time-domain, the $t \mathrm { - } f$ diagrams, and range profiles of beat signals, are shown in Fig. 15. As shown in Fig. 15(a), three large pulses can be observed in the received radar signal, which is caused by the strong interferences. Then the interference-contaminated beat signal leads to a range profile with significantly increased noise floor, and the two weaker targets cannot be detected (see Fig. 15(b)). The t-f spectrum of the beat signal is computed through the STFT algorithm, where the parameters setting is the same as simulated signals. One can see from Fig. 15(c) that the interferences exhibit as three inclined thick lines in the t-f spectrum.

To overcome the missed detection of targets caused by the strong interferences, the optimal RV-FCN and CV-FCN

![](images/95a1cd8dac67e7b2cd68eb5e5725281db6958f0317734a4055fbb39e53bdd418.jpg)  
(a)

![](images/2b601e629e58042fd849b8fc67787206b7c430e87596d75f751663750bac8b46.jpg)  
(b)

![](images/0d88984d9fc08011d021dc897e9d829f6b40832d02eb7665a7dbcfbf919b0a38.jpg)  
(c)

![](images/413c0f38d5a478e164b48666bc051d78abfb9b3084c91f6043b7532613c4fb1c.jpg)  
(d)

![](images/8622491980893c1b7216faae38dc2385a955523ddaf6c2e83dc4f20036eed0cd.jpg)

![](images/292ee35cf5b3091da98c9471008e309774b82527fcd756e454e6737705ed19fc.jpg)  
(e)  
(f)

![](images/1e9aa15bb835ab347e26b8e0cfbb9a12f5b358b5c0d113290c5992db1b733fd5.jpg)  
(g)

![](images/f76c960610ee2e206bfa3adb296eda7d7bc644bff6cffe082e88ac45fec50e49.jpg)  
(h)

![](images/af91987323965af2e1f0d7a85442b41855b4e8a1d3a48f7910c9b6b247edfd16.jpg)  
(i)  
Fig. 13. Interference mitigation for simulated radar signals whose SINR is -7.91 dB and SNR is 20 dB. (a) shows the acquired beat signal contaminated by mutual interferences, (b) its range profiles, and (c) its time-frequency diagram. (d) shows an interference-free reference. (e)-(h) the results of interference mitigation of optimal CV-FCN trained using one eighth of the dataset with prior-guided loss function. (i) displays the corresponding range profiles obtained after interference mitigation.

![](images/6267a527f12423ceda0c804dfe40646d4f55fd154e3b41e565081a0fde4ce910.jpg)  
Fig. 14. The performance comparison of our proposed CV-FCN based IM approach with state-of-the-art techniques

obtained in Section V-B are used to suppress the interference components in measured radar signals. The network was trained using the dataset including only simulated radar signals, and the prior-guided loss function is used for training.

The $t \mathrm { - } f$ map of the recovered signal processed by the RV-FCN is shown in Fig. 15(d), the interferences are entirely removed in the negative frequency, but there are still residual interference components mixed with the desired spectrum of targets in the positive frequency. This can be explained by the fact that the beat signals mixed with interferences and noise are relatively more difficult for the network to extract their features. In contrast, a more complete interference mitigation performance can be seen in Fig. 15(e), which shows the better generalization performance of complex-valued networks. Furthermore, with the value of λ increases, the residual interference components and noise are removed as shown in Fig. 15(e) to (h). After interference mitigation, three peaks representing the objects can be clearly seen in the range profiles as shown in Fig. 15(i), and the CV-FCN offers a lower noise floor than the RV-FCN. With the proportion of $L _ { 2 , 1 }$ norm gradually increases, the noise floor is further decreased, which would help to improve the target detection probability.

![](images/9b7fa5f9980154fa236110e771ed9fad214c3a25dea7a68c99192a54e96014f6.jpg)  
(a)

![](images/2f8f230f0b2c9e2e1a9e2b841a65091b66d432e19cf7e12d16913e7ded531bce.jpg)  
(b)

![](images/d3ae6d1c5bfb299cb46312489fcae4ef748f35ba0c51e1a973c20247de390eb2.jpg)

![](images/fb818d52643c27947a2d14ebe78b392b4cde4ecfe0ca42ce1443e1d163ddadcc.jpg)

(c)  
![](images/8f27d60258ce0722f0a1c06e2215b49f063b53f778d88dcfc42af5fb72c466cb.jpg)

![](images/efe9e256752b91e619ecf119a983cf76f7607f5339682b8c0d9d4d2deaa078bf.jpg)

(d)  
![](images/63f0c61e0b19b786562cf2530280190348ae65bcfe53f75c5c129834dac0da5e.jpg)  
(g)

(e)  
(f)  
![](images/33f3947700960fb1821b8e3e749bb335eea02f62c5508b6df081624fe8d74cfc.jpg)  
(h)

![](images/28b5b7b9dd7bfa2d066bce0c5b8b5bd9de8b0c0446512f99d367684a352b0e7a.jpg)  
(i)  
Fig. 15. Interference mitigation for measured radar signals contaminated by the interferences from chimneys. (a) shows the acquired beat signal contaminated by mutual interferences (b) its range profiles and (c) its time-frequency diagram. (d) the results of interference mitigation of optimal RV-FCN trained with MSE. (e)-(h) the results of interference mitigation of optimal CV-FCN trained using only simulated radar signals with prior-guided loss function. (i) displays the corresponding range profiles obtained after interference mitigation.

We also applied the RV-FCN and our proposed approach to the measured radar signals collected in the other two scenes for interference mitigation (a rotating wind turbine and a street with moving cars). The $t \mathrm { - } f$ maps of interference contaminated beat signals and recovered radar signals are shown in Fig. 16. Similarly, a better IM performance is obtained by the CV-FCN, but there are still interference components in the positive half of the STFT spectrum. By increasing the value of λ, this problem can be solved. The residual interference components and noise are obliterated, and the desired spectra related to targets are recovered.

The experimental results on measured radar signals collected in various real-world scenes have shown a better generalization performance of complex-valued networks. Besides, we can see the effectiveness of the prior-guided loss function in helping the neural networks to remove the residual interferences and noise in measured radar signals. Therefore, the proposed CV-FCN based prior-guided interference mitigation approach can be better applied in reality.

## VII. CONCLUSION

In this paper, a prior-guided deep learning based interference mitigation approach has been presented for FMCW radars. The STFT is used to transform received radar signals to the $t \mathrm { - } f$ domain so that the NNs can better extract the features of targets’ beat signals and interferences. Then the CV-FCN is designed to deal with the complex-valued radar signals. Meanwhile, the prior feature is introduced as a regularization term in the training stage.

An FMCW radar interference dataset with a wide and realistic range of signal parameter variations is presented. The experimental results show a better interference mitigation performance with fewer parameters in low SINR scenarios offered by complex-value networks. Additionally, the network can converge faster, and the size of the dataset needed for training can be reduced with the prior-guided loss function. Compared to the well-known traditional and DL-based interference mitigation techniques, the proposed approach achieves the state-of-the-art in SINR based performance comparison. Finally, the qualitative results on the measured radar signals show its excellent generalization. In future work, we aim to design an optimization algorithm to adjust the value of hyperparameter λ automatically in the prior-guided loss function.

![](images/d4c46640168e4ed336e7cec122e5ca5847a36d67bab8251682e3dd798826219b.jpg)

(a)  
![](images/9593352b13a2a33b902ed830da233b899d7b932b4782fc87328bbdd94b420b8f.jpg)

![](images/293ee362b1129dfba03e63c1bbf0a0b10484576efaf28e1a2ec35fa9bfa2c4ef.jpg)

(b)  
![](images/189e32013766093d8154d4186bf3fa78fd7d6725de280e57040291557f86d521.jpg)  
(d)

(c)  
![](images/76be0c592c63ab775e67571366e5e73c39be6becb29f238a2272af444ddf79a7.jpg)

![](images/d7f522e98e15083638dcb86c9f19f0c5f8b54d400f21165489bb47e91db2f9a5.jpg)  
(e)

![](images/dc1dab2c19e4fa783ed80057fc931cd60ec72df07c2ef54f04d487bfddbacf13.jpg)

![](images/92e30de2ab85446d1d3ad8857dacb9b67ad1ff052a9a05a3b3af228afdb6c57c.jpg)  
(g)

(f)  
![](images/836bba31d829b6b6113d77a4e332b708e81cbb8be00efd6c16dd610c0d67e892.jpg)

![](images/d5bee6f2c9e2f9751baa152ba92769e4fa14e5c7e5ef384ca4a4eb9746caf152.jpg)  
(j)

(h)  
![](images/a201f1b4bed325013c88e7ed228fb9c3196523aac449a2fc1bf0191ee38a3fca.jpg)  
(k)

(i)  
![](images/02a4fbc36c4ea7ed1d8048a85a2344916d78161a0cc92435c48d993c1a070a2c.jpg)  
(l)  
Fig. 16. Interference mitigation for measured radar signals in three scenarios (A13, windmill and street from left to right). (a)-(b) shows the time-frequenc diagram of acquired beat signal contaminated by mutual interferences. (g)-(h) the results of interference mitigation of optimal CV-FCN trained with prior-guided loss function where b is 0. (j)-(k) the results of interference mitigation of optimal CV-FCN trained with prior-guided loss function where b is 400.

## ACKNOWLEDGMENT

The authors would like to thank F. van der Zwan from TU Delft for his help for experimental measurements and providing the data.

## REFERENCES

[1] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors Journal, vol. 21, no. 5, pp. 6575–6586, 2021.

[2] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in 2017 European Radar Conference (EURAD), pp. 90–93, IEEE, 2017.

[3] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in 2017 18th International Radar Symposium (IRS), pp. 1–10, IEEE, 2017.

[4] F. Jin and S. Cao, “Automotive radar interference mitigation using

adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[5] S. Lee, J.-Y. Lee, and S.-C. Kim, “Mutual interference suppression using wavelet denoising in automotive fmcw radar systems,” IEEE Transactions on Intelligent Transportation Systems, 2019.

[6] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive fmcw radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS), pp. 1–4, IEEE, 2018.

[7] J. Bechter, K. Eid, F. Roos, and C. Waldschmidt, “Digital beamforming to mitigate automotive radar interference,” in 2016 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), pp. 1–4, IEEE, 2016.

[8] X. Li, Y. He, and X. Jing, “A survey of deep learning-based human activity recognition in radar,” Remote Sensing, vol. 11, no. 9, p. 1068, 2019.

[9] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in 2019 22th International Conference on Information Fusion (FUSION), pp. 1–8, IEEE, 2019.

[10] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world fmcw radar signals,” in 2020 IEEE International Radar Conference (RADAR), pp. 624–629, IEEE, 2020.

[11] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 927–940, 2021.

[12] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” arXiv preprint arXiv:2007.11102, 2020.

[13] M. L. L. de Oliveira and M. J. G. Bekooij, “Deep convolutional autoencoder applied for noise reduction in range-doppler maps of fmcw radars,” in 2020 IEEE International Radar Conference (RADAR), pp. 630–635, 2020.

[14] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR), pp. 315–320, IEEE, 2020.

[15] W. Fan, F. Zhou, M. Tao, X. Bai, P. Rong, S. Yang, and T. Tian, “Interference mitigation for synthetic aperture radar based on deep residual network,” Remote Sensing, vol. 11, no. 14, p. 1654, 2019.

[16] S. Chen, W. Shangguan, J. Taghia, U. Kuhnau, and R. Martin, “Auto-¨ motive radar interference mitigation based on a generative adversarial network,” in 2020 IEEE Asia-Pacific Microwave Conference (APMC), pp. 728–730, 2020.

[17] J. Mun, H. Kim, and J. Lee, “A deep learning approach for automotive radar interference mitigation,” in 2018 IEEE 88th Vehicular Technology Conference (VTC-Fall), pp. 1–5, IEEE, 2018.

[18] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using rnn with self attention,” in ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 3802–3806, IEEE, 2020.

[19] D. A. Brooks, O. Schwander, F. Barbaresco, J.-Y. Schneider, and M. Cord, “Complex-valued neural networks for fully-temporal microdoppler classification,” in 2019 20th International Radar Symposium (IRS), pp. 1–10, IEEE, 2019.

[20] P. Virtue, X. Y. Stella, and M. Lustig, “Better than real: Complexvalued neural nets for mri fingerprinting,” in 2017 IEEE international conference on image processing (ICIP), pp. 3953–3957, IEEE, 2017.

[21] Y. Arima and A. Hirose, “Millimeter-wave coherent imaging of moving targets by using complex-valued self-organizing map and auto-encoder,” IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, vol. 13, pp. 1784–1797, 2020.

[22] C. Trabelsi, O. Bilaniuk, Y. Zhang, D. Serdyuk, S. Subramanian, J. Santos, S. Mehri, N. Rostamzadeh, Y. Bengio, and C. Pal, “Deep complex networks. arxiv 2018,” arXiv preprint arXiv:1705.09792.

[23] A. Hirose and S. Yoshida, “Generalization characteristics of complexvalued feedforward neural networks in relation to signal coherence,” IEEE Transactions on Neural Networks and learning systems, vol. 23, no. 4, pp. 541–551, 2012.

[24] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for fmcw radar systems,” IEEE Transactions on Microwave Theory and Techniques, pp. 1–1, 2021.

[25] M. Abadi, P. Barham, J. Chen, Z. Chen, A. Davis, J. Dean, M. Devin, S. Ghemawat, G. Irving, M. Isard, et al., “Tensorflow: A system for

large-scale machine learning,” in 12th USENIX symposium on operating systems design and implementation (OSDI 16), pp. 265–283, 2016.

[26] M. Arjovsky, A. Shah, and Y. Bengio, “Unitary evolution recurrent neural networks,” in International Conference on Machine Learning, pp. 1120–1128, PMLR, 2016.

[27] N. Guberman, “On complex valued convolutional neural networks,” arXiv:1602.09046, 2016.

[28] B. G. Bodmann and P. K. Singh, “Burst erasures and the mean-square error for cyclic parseval frames,” IEEE transactions on information theory, vol. 57, no. 7, pp. 4622–4635, 2011.

[29] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” arXiv preprint arXiv:1409.1556, 2014.

[30] J. Wang, “CFAR-based interference mitigation for FMCW automotive radar systems,” 2021, arXiv:2101.01257.