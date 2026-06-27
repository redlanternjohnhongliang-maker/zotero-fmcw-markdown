# A Two-Stage DNN Model With Mask-Gated Convolution for Automotive Radar Interference Detection and Mitigation

Shengyi Chen , Jalal Taghia, Uwe Kühnau, Nils Pohl , , and Rainer Martin ,

—As the number of radar sensors on the road increases rapidly and many of these sensors share the same frequency spectrum, mutual interference cannot be avoided. This paper introduces a novel automotive radar interference mitigation approach using an autoencoder model which consists of separate neural networks for the detection and reconstruction steps. A mask-gated convolutionis proposed to help the reconstruction neural network to learn the signal pattern from interference-free samples and to interpolate accordingly

![](images/f16b433ba1b70739d81c977cb5d5f61a4fc89b3edf002967bfc839bdbcff9e5d.jpg)

the signal segments at the disturbed positions. Through perturbation analysis it is shown that the reconstruction neural network can recover the distorted samples by utilizing their surrounding relevant samples. By exploiting the nature of interference in real-world scenarios, the proposed training approach does not need hand-labeled training data. Together with the proposed composite training loss, the neural network can recover the disturbed discrete beat signal with remarkable improvements in the signal-to-interference-plus-noise ratio (SINR) and the mean absolute percentage error (MAPE). Moreover, despite the use of a purely simulated training data set, the autoencoder can deal with real-world radar measurements which are more complex than the training data set.

— Automotive radar, interference mitigation, autoencoder, mask-gated convolution, deep learning.

## I. INTRODUCTION

UTOMOTIVE radar sensors are becoming an essential ingredient to advanced driver assistance systems as they   
can scan the environment under almost all weather condi  
tions. In order to get a 360-degree view, modern vehicles   
are typically equipped with multiple radar sensors [2]. Since   
automotive radars basically use the same allocated frequency   
spectrum, mutual interference is inevitable, particularly when   
several radars transmit simultaneously on overlapping fre-

quencies in the direct line-of-sight. The functionality of radar sensors like target detection can be affected by the mutual interference to some extent, as the unexpected interference usually raises the noise level and creates ghost targets [3]–[5].

As the mutual interference between radar sensors is receiving more and more attention from both academia and industry, various methods have been proposed to address the interference problem. In addition to hardware solutions [6], [7], the classical signal recovery methods such as the zeroing method [3] and the autoregressive (AR) model-based interpolation [8] were proposed for recovering the baseband signal after the detection of disturbed samples. For example, in [9], the disturbed signal segment is recovered by linear predictive coding (LPC) after the short-time Fourier transform (STFT). These classical signal recovery methods can provide a satisfactory result if the number of disturbed samples is small. However, the performance of these methods deteriorates as the number of disturbed samples becomes larger [10]. In [11], the disturbed samples are first detected and removed. Then the discarded signal samples are recovered by modeling the beat signal as a sum of complex exponentials and using the Matrix-Pencil method to estimate their parameters.

Besides traditional signal processing methods, compressive sensing algorithms are also widely used in automotive radar interference mitigation [10], [12]–[14]. In [10], the sparse

Bayesian learning algorithm is adopted for automotive radar interference mitigation. The range-Doppler (RD) spectrum can be acquired from the mean of the maximum a posteriori (MAP) estimate under the given remaining undistorted samples in the discrete beat signal. In [12], the disturbed samples are first substituted with zeros and the iterative method with an adaptive thresholding (IMAT) algorithm is then used to interpolate these zeroed samples. In [13], it is assumed that the two components of the received signal (beat signal and interference) are sparse in different domains. Then, the morphological component analysis (MCA) approach is used to separate the interference from the beat signal and the interference mitigation problem is defined as a dual-basis pursuit problem. However, most of these compressive sensing approaches are based on an iterative reconstruction process, so the reconstruction time might vary largely from case to case. The reconstruction for severely disturbed scenarios usually requires more iterations than for weakly disturbed scenarios which makes the allocation of computational resources difficult [15].

Due to their excellent capacity for modeling highdimensional distributions, deep neural networks (e.g., convolutional neural networks (CNNs), long-short term memory (LSTM) and autoencoder networks) have been applied in a wide range of applications [16] such as natural language processing [17], image processing [18]–[20] and industrial sensor data processing [21], [22]. Recent research results have shown that deep learning approaches can be used to tackle the mutual interference problem [1], [23]–[29]. In [23], CNNs are proposed for noise suppression of both the range profile and the RD spectrum, where the range profile can be obtained after applying the first fast Fourier transform (FFT) along the fast-time samples and the RD spectrum can be obtained after applying the second FFT to the range profile. However, the target peak values may be distorted after signal recovery. An improved and resource-efficient variant of CNNs has been proposed in [24]. Solving the mutual interference issue by denoising the RD spectrum for frequency-modulated continuous wave radar has also been addressed in [25], [26], where complex-valued CNNs are employed in [25] and a convolutional autoencoder is used in [26]. Since the input of the autoencoder is the amplitude and phase components of the complex-valued RD spectra, the phase information and probably the weak target peaks cannot be fully retained in [26]. This is due to the fact that the amplitude of strong target peaks is significantly larger compared to the noise and is therefore easy for neural networks to learn, but the phase component can resemble the phase of the noise (both vary in the same range) and is therefore more difficult to acquire. In [29], a complex-valued fully convolutional network is proposed for reconstructing the disturbed complex signal in the time-frequency domain (after applying STFT to the discrete beat signal). The conditional generative adversarial network (GAN) based method was investigated in [27] for the radar interference mitigation, where the generator learns to reconstruct the disturbed RD spectra. In [28], the disturbed complex signal segments in the complex range profile are firstly detected by a classical edge detector and a GAN is proposed to recover these disturbed complex signal segments. An autoencoder for time-domain signal recovery was developed in [1], where the disturbed discrete beat signals are detected by an edge detector as in [28] and the proposed autoencoder interpolates these disturbed signals. Therefore, the performance of the interference detector may have a negative effect on the reconstruction results of the GAN and autoencoder in [28] and [1].

In this paper, we propose a two-stage autoencoder model for automotive radar interference mitigation. The proposed autoencoder model contains two separate neural networks for the detection and reconstruction. Different from [23]–[29], the detection neural network first detects the interference-contaminated samples and then the reconstruction neural network reconstructs these disturbed samples in the time domain. Most state-of-the-art deep learning approaches take the distorted RD spectrum as input and aim at the reconstruction of the RD spectrum. However, for a radar measurement in which even few samples are distorted with strong interference, after applying the two-dimensional (2D) FFT, the signal distortion is widely spread in the RD spectrum. Therefore, solving the interference problem directly in the time domain can theoretically yield a better signal reconstruction. Furthermore, in most state-of-the-art deep learning approaches, an elaborate and sophisticated labeling process of radar sensor data is required. Motivated by these challenges, we propose a novel training strategy which is only based on interference-free discrete beat signals and does not require cumbersome labeling. For the training phase a simulated data set is used. For the performance assessment, the trained autoencoder has been applied to real radar measurements. The experimental results show that the proposed autoencoder model can provide superior recovery without experiencing difficulties in reconstructing phase and target peak values as in [26] and [23], respectively.

The main contributions of this paper are summarized as follows:

• The proposed detection neural network is able to provide a more accurate interference detection than the conventional adaptive thresholding method [30].

• A reconstruction neural network with mask-gated convolution is developed for the interpolation of disturbed samples at the detected positions. The reconstruction neural network can achieve a superior reconstruction performance in comparison to the state-of-the-art algorithms.

• Based on the features of interference in real-world scenarios, we propose a novel mechanism for generating simulated interference. By applying this mechanism in the training phase, the trained neural networks are capable of handling real interference scenarios, even if the training data set is purely simulated and without extra labeling.

• We investigate the interpolation mechanism of the deep neural network by introducing a perturbation analysis. The perturbation analysis gives an intuitive explanation of the working mechanism of the deep neural network with different types of convolution networks.

The remainder of this paper is organized as follows. In Section II, the frequency-modulated continuous wave (FMCW) radar signal model is introduced. Section III describes the details of the proposed detection neural network for the detection of interference-contaminated samples and the reconstruction neural network for the reconstruction of the disturbed samples. The performance of the proposed autoencoder model is evaluated through real measurements in Section IV. Finally, conclusions are provided in Section V.

## II. AUTOMOTIVE RADAR SYSTEM

The fast chirp FMCW modulation [31] as a variant of the classical FMCW modulation is commonly used in commercial automotive radar systems. Considering a radar with fast chirp modulation that carries $Q$ successive chirps, its transmit waveform can be represented as

$$
T _ { s } ( t ) = \sum _ { q = 0 } ^ { Q - 1 } s ( t - q T ) ,\tag{1}
$$

where T denotes the pulse repetition interval and s(·) the transmit chirp signal. The individual transmit chirp signal with a normalized amplitude is given by

$$
s ( t ) = \exp { \left( j 2 \pi \left( f _ { c } t + 0 . 5 \kappa t ^ { 2 } \right) \right) } \mathrm { r e c t } \left( \frac { t } { T } \right) ,\tag{2}
$$

where $f _ { c }$ is the carrier frequency, $\kappa ~ = ~ B / T$ denotes the chirp rate of the transmit signal with B denoting the sweep bandwidth. Here we assume that the pulse repetition time is equal to the chirp duration. rect(·) denotes the unit pulse which is one in the interval [0, 1) and zero otherwise. The qth chirp of the target reflection signal is received with a delay time τ compared to the transmit signal:

$$
r _ { q } ( t ) = A _ { q } s ( t - q T - \tau ) + \mathrm { v } _ { q } ( t ) ,\tag{3}
$$

where $A _ { q }$ is the received amplitude, $\tau = 2 ( D + \upsilon t ) / c .$ , and $\mathbf { V } _ { q }$ denotes complex-valued white noise. Here, D and v denote, respectively, the distance and relative radial velocity between the radar and the target, and c represents the speed of light. The beat signal in the baseband can be obtained after stretch processing, namely mixing $r _ { q }$ conjugately with the transmitted signal: $\hat { y } _ { q } ( t ) = r _ { q } ^ { * } ( t ) s ( t - q \hat { T } )$ . After filtering with a low-pass filter (LPF) and sampling with a period of T<sub>s</sub> and collecting P samples per chirp, the discrete beat signal for one target can be approximated as [32]

$$
\begin{array} { c } { { \hat { y } _ { p , q } \approx A _ { q } \mathrm { e x p } \left( j 2 \pi \kappa \displaystyle \frac { 2 D } { c } p T _ { s } \right) \cdot \mathrm { e x p } \left( j 2 \pi f _ { c } \displaystyle \frac { 2 \upsilon } { c } q T \right) } } \\ { { \cdot \mathrm { e x p } \left( j 2 \pi f _ { c } \displaystyle \frac { 2 D } { c } \right) + { \bf v } _ { p , q } p \in \{ 0 , P - 1 \} . } } \end{array}\tag{4}
$$

With the assumption that $\grave { y } _ { p , q }$ represents the additive in-band interference, the discrete beat signal $\mathbf { y } = \{ y _ { ( q \cdot P + p ) } \}$ for $0 \leq$ $q \leq Q - 1$ can be therefore summarized as

$$
y _ { ( q \cdot P + p ) } = \left\{ { \begin{array} { l l } { { \hat { y } } _ { p , q } + { \mathbf { v } } _ { p , q } } & { q \cdot P + p \in K } \\ { { \hat { y } } _ { p , q } + { \hat { y } } _ { p , q } + { \mathbf { v } } _ { p , q } } & { q \cdot P + p \notin K , } \end{array} } \right.\tag{5}
$$

![](images/7b7bc06f7d01d8c2f90c2a9bda42780a581a2c3f1bf7f92e6130a6da54d223c5.jpg)  
(a)

![](images/d82b1d42912d20fb1f9bdff67c61a1d3ac5101f100e57579526e30c9d74844ae.jpg)  
(b)

Fig. 1. Example of a discrete beat signal without (a) and with (b) interference.  
![](images/158e931d600f967a41326592dee1df1f9cefdbeb21385f103b26cf8b31e80e50.jpg)  
(a)

![](images/42953dc44034deda3e97be974a00926b35b7b7beb9d1cc020024dd681632f9e5.jpg)  
(b)  
Fig. 2. Example of an RD spectrum without (a) and with (b) interference.

where K is the set of sample indices without interference and $q \cdot P + p \notin K$ denotes the indices of the samples containing interference. Fig. 1 shows real-world examples of interferencefree and interference-contaminated discrete beat signals.

To obtain target range and velocity, the 2D discrete Fourier transform (DFT) can be applied to the discrete beat signal matrix $\mathbf { Y } = \{ y _ { p , q } \} \in \mathbb { C } ^ { P \times Q }$

$$
\mathbf { X } = \mathbf { C } _ { P } \cdot \mathbf { Y } \cdot \mathbf { C } _ { Q } ^ { T }\tag{6}
$$

where $\mathbf { C } _ { P } \in \mathbb { C } ^ { P \times P } , \mathbf { C } _ { O } \in \mathbb { C } ^ { Q \times Q }$ are DFT matrices, and X ∈ $\mathbb { C } ^ { P \times Q }$ denotes the 2D RD spectrum. Fig. 2(a) and Fig. 2(b) show two real-world examples of the RD spectrum with and without interference, respectively.

## III. TWO-STAGE AUTOENCODER MODEL

In this section we introduce the proposed autoencoder model for automotive radar interference mitigation. As shown in Fig. 3, the proposed model contains two neural networks, namely the detection neural network and the reconstruction neural network, where $\mathbf { Y } _ { s } ~ \in ~ \mathbb { R } ^ { P \times Q \times 2 }$ denotes the tensor form of the interference-contaminated discrete beat signal, and $\tilde { \mathbf { Y } } _ { s }$ the tensor form of the autoencoder-recovered discrete beat signal. The number of kernels of each layer is specified directly above the corresponding layers. The detection neural network is trained independently and the reconstruction neural network can be trained alone or in conjunction with the trained detection neural network. By exploring the property of interference in the real-world measurements, we propose a new training strategy based on a simulated data set that contains only interference-free discrete beat signals. For training the detection neural network, the interference is then artificially superimposed according to the proposed interference generation mechanism described in Section III.A. For training the reconstruction neural network, the samples are simply set to zero instead of superimposing the interference at the corresponding positions. The efforts of the costly and challenging labeling process of the radar sensor data as in [23], [25], [26] can be therefore saved. This training strategy is proven to be effective as the trained autoencoder model can later handle the real-world interference scenarios even though the training data set is purely simulated.

![](images/5ef654b6c03782f129d1f83ad127b102a5bcdab0fb10372944c51996e987f123.jpg)  
Fig. 3. Two-stage autoencoder model for automotive radar interference mitigation.

Both the detection and the reconstruction neural network are trained using an NVIDIA RTX 3060 for 1000 epochs with a batch size of four. The stride in the encoder network is two and in the decoder network is one. The learning rate is set to 0.0001 and the ADAM optimizer [33] is used during training. The data set contains 2000 simulated interference-free complex discrete beat signals having the same size of Y. The complex discrete beat signal is converted into a tensor of the form [P, Q, 2] consisting of the real and imaginary parts as the input for the neural networks. The input data was normalized with respect to the maximum amplitude of the undisturbed discrete beat signal. The kernel size has been set to 9x3 and thus increases the receptive field to include more fasttime samples. According to our experiments, inserting more layers into the reconstruction neural network does not yield a better reconstruction accuracy. The reconstruction appears to be robust with respect to small variations of the learning rate.

## A. Detection Neural Network

The detection neural network detects the positions of interference-contaminated samples and consequently generates a binary mask. The network architecture is shown in Fig. 3, which is a simple convolutional autoencoder.

The interference in real-world scenarios can contain large diversity and randomness, e.g., due to the chirp rate of different radar sensors, the collision time between interferer and victim radar, and the number of interferers. Moreover, due to the multipath propagation and the distance between sensors, the signal strength of disturbed samples may vary largely. As shown in Fig. 1, the positions of disturbed samples do not follow a particular pattern and the interference strength varies in a wide range (from a fraction to several times of the signal amplitude). Nevertheless, a common feature of these positions of disturbed samples can be observed, namely that the interference is confined to short bursts. The bandwidth of the LPF, the differences of chirp rate, and the time instance of intersection of the spectra actually determine the interference duration on the discrete beat signal and thus the number of disturbed samples. With the assumption that the interferer has a chirp rate κ˜ different from the transmit signal described in (2), the interference duration can be described as

$$
T _ { \mathrm { i n t } } \leq | 2 \cdot B _ { l } / ( \tilde { \kappa } - \kappa ) | ,\tag{7}
$$

where $B _ { l }$ denotes the bandwidth of the LPF [34].

Based on this observation, a mask is generated at each training iteration where 0 to 3 blocks in each chirp are randomly selected and each block contains 2 to 7 continuous positions. Then, an additive interference with arbitrary signal strength (randomly sampled from a fraction to a multiple of the maximum amplitude of the undisturbed signal) is inserted at each position. The discrete beat signals are simulated in a MATLAB simulation [35] with random 1 to 15 static targets and 1 to 15 moving targets. Note that the maximum amplitude of the undisturbed discrete beat signal is about 400. Besides the interference, complex-valued additive white noise with an amplitude of one eighth of the amplitude of the interference-free signal is also added. Fig. 4 shows examples of a randomly generated mask and a simulated discrete beat signal with interference.

Since the additive interference is randomly generated in each training iteration, the neural network has therefore the opportunity to explore a wide range of interference types. Hence, this particular mechanism of interference generation guarantees the robustness of the trained neural network to various interference scenarios.

For training the detection neural network, the binary cross-entropy loss is used which is defined as

$$
l _ { b c e } = - \frac { 1 } { P \cdot Q } \sum _ { i = 1 } ^ { P \cdot Q } g _ { i } \log { ( s _ { i } ) } + ( 1 - g _ { i } ) \log { ( 1 - s _ { i } ) } ,\tag{8}
$$

![](images/77506893f7e2f732c3ca9ba954f4135c5b522ebe2e529a83b79adb677b68a1f7.jpg)

![](images/a97eb961fe601d4218c87ce89d6a3e18f74d85e69786e4b4f66f3413ae35bcde.jpg)  
Fig. 4. Example of (a) a randomly generated mask and (b) the corresponding simulated discrete beat signal with additive interference at given positions. For an intuitive visualization, only the amplitude of the complex discrete beat signal is shown in (b).

where $g _ { i }$ and $s _ { i }$ are the ground truth and the predicted probability for the i -th position.

## B. Reconstruction Neural Network

The reconstruction neural network takes the masked discrete beat signal along with the estimated binary mask as the inputs. Further, by utilizing the mask-gated convolution, the reconstruction neural network learns to extract the signal pattern from the undisturbed samples and then accordingly interpolates the signal segments at the masked positions.

Since not all signal segments of the disturbed discrete beat signal are pertinent to the reconstruction of the disturbed samples, a mechanism which forces the neural network to concentrate on the valid input samples needs to be considered. Several types of gated convolution are proposed in image processing [18], [19] and language modeling [17] to address this issue. The general concept of the gated convolution is to use the convolution in combination with a sigmoid function so that the network learns to distinguish between valid and invalid signal segments. Unlike the types of gated convolution proposed in [17]–[19], where the gating features are separated from the latent features of signal after convolution,<sup>1</sup> the proposed mask-gated convolution uses the learned mask features at each layer for the gating operation, as shown in Fig. 5. For the input layer, mask-gated convolution is formulated as

$$
\mathbf { F } = \mathbf { W } _ { f } * \bar { \mathbf { Y } } _ { s } \mathbf { G } = \mathbf { W } _ { g } * M\tag{9}
$$

$$
O = \mathbf { F } \odot \sigma \left( \mathbf { G } \right)\tag{10}
$$

where σ is the sigmoid function, ∗ represents the convolution operator and  denotes the element-wise multiplication. $\mathbf { W } _ { g }$ and $\mathbf { W } _ { f }$ are two different convolutional filters. G and F represent the features that are extracted by the convolutional filters $\mathbf { W } _ { g }$ and $\mathbf { W } _ { f } ,$ respectively. $\bar { \mathbf { Y } } _ { s }$ is the masked signal representation, M is the mask feature, and O denotes the output signal.<sup>2</sup>

![](images/1e709e797afbcdafc63735667fd635706a92f010f9872c6924466a54e0e0251c.jpg)  
Fig. 5. Illustration of mask-gated convolution.

We propose a composite loss which contains the recovery losses in the range profile and in the Doppler-FFT spectrum (obtained by applying the FFT to the discrete beat signal along the chirp direction) for the training of the reconstruction neural network. This composite loss function is defined as

$$
\begin{array} { l } { \displaystyle \mathcal { V } = \frac { \eta } { n _ { s } } \sum _ { i \in \xi _ { r } } \Big | \Phi ( \hat { \mathbf { Y } } _ { s } ) _ { i } - \Phi ( \tilde { \mathbf { Y } } _ { s } ) _ { i } \Big | + \frac { \eta } { P - n _ { s } } \sum _ { j \notin \xi _ { r } } \Big | \Phi ( \tilde { \mathbf { Y } } _ { s } ) _ { j } \Big | } \\ { \displaystyle \quad + \frac { 1 - \eta } { n _ { s } } \sum _ { \tilde { i } \in \xi _ { d } } \Big | \Psi ( \hat { \mathbf { Y } } _ { s } ) _ { \tilde { i } } - \Psi ( \tilde { \mathbf { Y } } _ { s } ) _ { \tilde { i } } \Big | + \frac { 1 - \eta } { Q - n _ { s } } \sum _ { \tilde { j } \notin \xi _ { d } } \Big | \Psi ( \tilde { \mathbf { Y } } _ { s } ) _ { \tilde { j } } \Big | , } \end{array}\tag{11}
$$

where $\hat { \textbf { Y } } _ { s } ~ \in ~ \mathbb { R } ^ { P \times Q \times 2 }$ represents the tensor form of the interference-free discrete beat signal,  the fast Fourier transform along fast-time samples, 	 the fast Fourier transform along the chirp direction, and $0 \leq \eta \leq 1$ the weighting factor. $\xi _ { r }$ and $\xi _ { d }$ represent the index sets of signal segments of the $n _ { s }$ strongest targets in the range profile and the Doppler-FFT spectrum, respectively, where $0 < n _ { s } < \operatorname * { m i n } \{ P , Q \}$ . i and <sup>˜</sup>i indicate the corresponding row and column indices of the target signal segments in the range profile and the Doppler-FFT spectrum. $j$ and $\tilde { j }$ denote the row and column indices of the signal segments without target information. During training, $n _ { s }$ can be selected by determining the frequency bins of the target peaks with a cell averaging constant false alarm rate (CA-CFAR) detector. The row and column indices of $n _ { s }$ target positions can then be used to determine the target signal segments in the corresponding spectra for the composite loss calculation, as exemplified in Fig. 6. The first and third terms in (11) help the neural network learn the signal features of the targets, while the second and fourth terms help reduce the background noise.

Alternatively, we will also consider the masked ${ } _ { - } l _ { 1 }$ loss which is defined as

$$
l _ { 1 } = \frac { 1 } { \epsilon } \sum \Big | ( \tilde { \mathbf { Y } } _ { s } - \hat { \mathbf { Y } } _ { s } ) \cdot \tilde { M } \Big | ,\tag{12}
$$

where denotes the total amount of disturbed positions and $\tilde { M }$ is the binary mask estimated by the detection neural network where the disturbed positions are encoded with the value 1 and the interference-free positions have the value 0. It should be noted that the neural network delivers a similar performance when the mean absolute error in (11) and (12) is replaced with the mean-squared error. During our experimentation phase, the reconstruction neural network was also trained based on the loss of the target peaks in the RD spectrum. It was found that the neural network trained via the proposed composite loss yields a signal-to-interference-plus-noise ratio (SINR) improvement of about 2 dB compared to the neural network trained via the loss in the RD spectrum.

![](images/fe5fe405a6308f22bcf0e66346041e145f590d14bf6e298e2764e18578cf1e7c.jpg)  
Fig. 6. Illustration of the target signal segment selection in the range profile and in the Doppler-FFT spectrum for the calculation of the composite loss function.

## IV. EVALUATION METHODS AND RESULTS

In this section, the performance of the proposed detection and reconstruction neural networks are evaluated in comparison with the state-of-the-art algorithms.

To quantitatively analyze the interference detection performance of different algorithms, the recall, precision, and F-score are introduced, which are calculated as: $\begin{array} { r } { R = \frac { \mathrm { T P } } { \mathrm { T P + F N } } . } \end{array}$ $\begin{array} { r } { P r = \frac { \mathrm { T P } } { \mathrm { T P + F P } } } \end{array}$ , and $F _ { 1 } = \frac { 2 \mathrm { T P } } { 2 \mathrm { T P } + \mathrm { F P } + \mathrm { F N } }$ where TP, FP, and FN denote the number of true-positive, false-positive, and falsenegative estimates.

The mean absolute percentage error (MAPE<sup>3</sup>) and the SINR are used as evaluation metrics for the reconstruction of the discarded samples. The SINR is defined as the ratio of the mean power of the target peaks and the mean power of the interference and noise.

$$
{ \mathrm { S I N R } } = 1 0 \log \left( { \frac { { \frac { 1 } { \# _ { \mathcal { O } } } } \sum _ { \{ n , m \} \in { \mathcal { O } } } | \mathbf { X } [ n , m ] | ^ { 2 } } { { \frac { 1 } { \# _ { \mathcal { N } } } } \sum _ { \{ n , m \} \in { \mathcal { N } } } | \mathbf { X } [ n , m ] | ^ { 2 } } } \right) ,\tag{13}
$$

where n and m are row and column indices of the RD matrix, is the set of target peaks and is the set of noise cells. # denotes the cardinality of a set. The MAPE is defined as

TABLE I  
EVALUATION OF INTERFERENCE DETECTION METHODS
<table><tr><td rowspan=1 colspan=1>Detection method</td><td rowspan=1 colspan=1>F-score</td><td rowspan=1 colspan=1>Recall</td><td rowspan=1 colspan=1>Precision</td></tr><tr><td rowspan=1 colspan=1>Proposed neural network</td><td rowspan=1 colspan=1>80.37%</td><td rowspan=1 colspan=1>86.89%</td><td rowspan=1 colspan=1>75.49%</td></tr><tr><td rowspan=1 colspan=1>Iterative adaptive thresholding</td><td rowspan=1 colspan=1>80.32%</td><td rowspan=1 colspan=1>75.62%</td><td rowspan=1 colspan=1>85.64%</td></tr></table>

the mean of the normalized absolute error between the target peaks in the interference-free RD spectrum $\mathbf { X } _ { \mathrm { c l e a n } }$ and in the reconstructed RD spectrum $\tilde { \mathbf { X } } \mathrm { : }$

$$
\mathrm { M A P E } = \frac { 1 } { \# _ { \mathcal { O } } } \sum _ { \{ n , m \} \in \mathcal { O } } \frac { \Big | \mathbf { X } _ { \mathrm { c l e a n } } [ n , m ] - \tilde { \mathbf { X } } [ n , m ] \Big | } { | \mathbf { X } _ { \mathrm { c l e a n } } [ n , m ] | } .\tag{14}
$$

Furthermore, through the ablation study and perturbation analysis, we investigate the importance of the different building blocks in the proposed reconstruction neural network as well as the interpolation mechanism of different neural networks.

## A. Performance Evaluation on the Detection Neural Network

For the evaluation of the proposed detection approach, the method in [30] will serve as a baseline reference. In [30], an interference detection method based on an iterative adaptive thresholding is proposed. The interference-contaminated samples are detected with the threshold and the detected samples are set to zero in the signal $\mathbf { y } \in \mathbb { C } ^ { L \times 1 }$ which yields a signal y¯. Then, with the number of detected samples λ, a new threshold value can be calculated as:

$$
{ \mathcal T } = \gamma \left( \sqrt { \frac { 1 } { L - \lambda } \sum _ { l = 1 } ^ { L } \bar { y } _ { l } ^ { 2 } } \right) .\tag{15}
$$

If the threshold $\tau$ changes more than a predefined value $\Delta \tau$ , the newly calculated threshold is used to detect further interference-contaminated samples. As soon as changes by less than $\Delta \tau$ between two iterations, the algorithm terminates.

For the evaluation of the interference detection performance, a data set is created containing 5000 discrete beat signals with additive interference generated according to the mechanism described in Section III.A. The number of target peaks in each synthesized discrete beat signal varies from 1 to 80 and the maximum amplitude of the additive interference also has several diversities (ranging from 300 to 1200).

The evaluation results are shown in Table I. Since the interference-contaminated samples are the minority in the discrete beat signal, the F-score is theoretically more important for evaluating the detection performance. The iterative thresholding algorithm presents a similar F-score as the proposed method. However, in radar interference mitigation, the amount of correctly detected interference positions has a greater impact on the recovery results. As shown in [1], if a small amount of interference-free samples is falsely discarded, this does not have a large impact on the recovery results. The proposed deep neural network provides therefore a better detection as it can correctly detect about 87% of the interference-contaminated samples.

![](images/796107a8af2c5c52aaf18d11a2582fc4e8f2c90b86a3685fc16bae11c248d577.jpg)  
Fig. 7. Comparison of the proposed autoencoder (model A and mode B) vs. the traditional autoencoder (model C and model D) in terms of SINR with different number of training iterations.

## B. Ablation Study and Perturbation Analysis on the Reconstruction Neural Network

In this section, we first perform an ablation study in which the proposed building blocks such as the mask-gated convolution and the composite loss are substituted by the regular convolution and the masked- ${ \bf - } l _ { 1 }$ loss, respectively, and different topologies are further investigated. Second, a perturbation analysis is performed which is inspired by the perturbation analysis in computer vision [36] and aims to interpret how the neural network reconstructs the disturbed samples.

In our ablation study, four different combinations of mask-gated convolution, regular convolution, composite loss, and masked-l loss are evaluated in terms of SINR. To ease the notation, we define model A as the model with the mask-gated convolution and the composite loss, model B as the model with the mask-gated convolution and the masked- ${ \bf - } l _ { 1 }$ loss, model C as the model with the regular convolution and the composite loss and model D as the model with the regular convolution and the masked ${ \bf - } l _ { 1 }$ loss. Note that model C and model D correspond to the traditional autoencoder.

In the test phase of our ablation study, a real-world interference-free radar measurement combined with 50 randomly generated masks are fed into different models for reconstruction. The evaluation results of SINR based on the RD spectrum of the reconstructed discrete beat signal are presented in Fig. 7. Model A and model B provide faster convergence and better SINR than model C and model D, indicating that the proposed mask-gated convolution plays an important role in the reconstruction neural network. From the comparison of model A and model B, it can be observed that the proposed composite loss can further improve the SINR of the reconstructed signal.

Since the reconstruction neural network interpolates samples at the disturbed positions in the discrete beat signal, it is of great importance to investigate the interpolation mechanism of the neural network. As shown in Fig. 8, we select and observe ten samples in the middle of a real radar measurement matrix Y<sup>ˆ</sup> . Then, an input perturbation (with an amplitude ranging from 800 to 1000) is added to one sample at a time in Y<sup>ˆ</sup> , and the values of the samples under observation are set to zero by a mask, yielding Y<sup>¯</sup> . The reconstruction neural network takes the perturbed discrete beat signal Y<sup>¯</sup> and interpolates the samples at these ten observation positions. By utilizing the original signal values at the observation positions as references, the root mean square error (RMSE) between the reconstructed values and the references can be calculated. An RMSE matrix can be created in which the RMSE is stored with respect to the perturbed sample at exactly the same position of that sample. Thus, if an input perturbation causes a larger or smaller RMSE at certain positions, it means that the samples at these positions are used for the reconstruction of the samples under observation by the neural network. An SINR matrix is created in a similar way, where the SINR value stored at each sample position is calculated based on the reconstructed RD spectrum after adding a perturbation on that exact input position of the discrete beat signal. Fig. 8(a) and Fig. 8(b) show the RMSE matrices calculated based on the values of the samples under observation which are reconstructed by the neural network using the proposed mask-gated convolution and the regular convolution, respectively. As shown in Fig. 8(a), if the input perturbation is added to the samples at the bottom left region, then the reconstructed values of the samples under observation (set to zero before the reconstruction) have the same RMSE as the recovered signal values of the input without perturbation.<sup>4</sup>

![](images/bbbcf1a038accca59a71b4e85ce7dd2cb2ed3306f6b36dae3d6df9ac627e0ea2.jpg)

![](images/4d5dd20f0e10b0440d8d19a889b117093cde9add6a017e6bf953c1b555218e44.jpg)  
Fig. 8. Perturbation analysis in terms of RMSE for the neural network with (a) the proposed mask-gated convolution and (b) the regular convolution. The RMSE stored at each sample position is calculated based on the reconstructed values of the samples under observation after adding a perturbation at that exact position in the input Y<sup>¯</sup> .

![](images/22679fc5138b8b52fca6163d5865bac85225475ce58b364240b95f35e73d150b.jpg)

![](images/f3df7e57d3c635d5141c3803d893d70600f76e40a893494e96de28ea62cec939.jpg)  
Fig. 9. Perturbation analysis in terms of SINR for the neural network with (a) the proposed mask-gated convolution and (b) the regular convolution. The SINR stored at each sample position is calculated based on the reconstructed RD spectrum after adding a perturbation at that exact position in the input Y<sup>¯</sup> .

Velocity [m/s]  
(a) Original - SINR 32.28 dB  
![](images/217d3043609dd0a49c72001275d042cc793057d347f4eccc6f0bb21ef9ac5ed6.jpg)  
Velocity [m/s]

(c) Zeroing - SINR 25.08 dB  
![](images/be4970c9e77b7d2b65fb5aa9c53da4e2457316def6bd8b034eb46eac6f4c0023.jpg)

(e) IMATCS - SINR 30.82 dB  
![](images/9b72af16fda3aca85a053398320d1fafc403bcae7358c49778cebd3dede2f4d4.jpg)  
Velocity [m/s]

(g) CNNs - SINR 27.35 dB  
![](images/9a5f0e2ff6751189625c30a443e3bfb821a03ebabaf66bd56fad1f0c1b7edd6c.jpg)  
Velocity [m/s]

(b) Distorted - SINR 12.82 dB  
![](images/3701ac380441fb6e7db18bfb6628a9ee557415ba4444c2e7e3b83ad054d79dc4.jpg)  
Velocity [m/s]

(d) AR - SINR 29.80 dB  
![](images/0be53d91753f7b1ae18efca5d03ab79c6765ef1755d8510561c7073855df2e3a.jpg)

(f) Autoencoder - SINR 31.68 dB  
![](images/c1c5814e72fd8f518add2c6c93965126cd84377a9a96cfe078d9a7eb16301608.jpg)  
Velocity [m/s]  
Fig. 10. (a) original RD spectrum, (b) distorted RD spectrum, and RD spectra recovered by (c) the zeroing method, (d) AR, (e) IMATCS, (f) autoencoder, (g) CNNs, in the case that the number of disturbed samples is about 5% of the total measurement.

Note that the reconstruction neural network interpolates only the samples under observation which were set to zero by a mask. However, if an input perturbation is added to the samples which are near the samples under observation, the RMSE of the reconstructed sample values raises. This indicates that the samples near the observation area are actually used by the neural network for reconstructing the samples in the observation area. The interpolation strategies of these two convolution layers are surprisingly different: the mask-gated convolution makes use of the direct surrounding samples for interpolation and the RMSE becomes larger when perturbations are added on the surrounding samples. Interestingly, with the regular convolution, the RMSE becomes smaller if perturbations are introduced to the surrounding samples and perturbations on the samples that are a bit apart from the nearby neighbors increase the RMSE.

Similar to the perturbation analysis on RMSE, the results on SINR in Fig. 9 show the same interpolation mechanisms of mask-gated convolution and regular convolution, namely perturbations on the direct surrounding samples deteriorate the interpolation for the mask-gated convolution and the regular convolution is more sensitive to perturbations further away.

The interpolation mechanism of the proposed mask-gated convolution is more in line with the logical consequence that an input perturbation on the relevant samples causes a higher RMSE on the reconstructed target peaks and thus a lower SINR of the reconstructed RD spectrum.

## C. Performance Assessment vs. the State-of-the-Art Methods

In this section, we evaluated the performance of the proposed two-stage autoencoder model in comparison with the zeroing method [3], the AR model [8], the IMATCS algorithm [12] and the CNNs proposed in [24]. The code implementation of $\mathrm { I M A T C S } ^ { 5 }$ is modified based on [37] and adapted to the compressive sensing framework proposed in [10] for interference mitigation. Since the interference detection is also required in those state-of-the-art methods (except for the CNNs which take the disturbed RD spectrum as input), the proposed detection neural network is therefore also applied for the detection of the positions of the disturbed samples. The validation data set used in this paper is a real-world radar measurement on the street.

First, the performance of the autoencoder is evaluated under the condition that about 5% samples of the discrete beat signal are disturbed by interference. The disturbed positions in the discrete beat signal are detected by the proposed detection neural network and further used in the reconstruction algorithms. Fig. 10 shows the recovered RD spectra in the case that 5% samples are disturbed. Both the proposed autoencoder and the AR method can produce satisfactory RD spectra in which the dominant target peaks are clearly identifiable. The CNNs has shown its strength in denoising the disturbed RD spectrum, yet due to the strong interference, some target peaks are obscured by the increased noise and disappear after reconstruction. In automotive radar target detection, the weak targets usually represent the pedestrians and bicyclists. Therefore, the absence of weak targets after the reconstruction of RD spectra could potentially cause difficulties in target detection and tracking. For this reason, the other metrics of CNNs are not further evaluated in this work, since more interference-contaminated samples are introduced for the evaluation of other metrics. Although the RD spectrum reconstructed with IMATCS contains more ghost peaks, its SINR is still better than the RD spectrum reconstructed with the AR method. This is due to the fact that IMATCS overestimates the power of the target peaks, as shown in Fig. 11, which gives the velocity cut of the recovered RD spectrum of the targets at 25 meter.

![](images/63bf6b4d9a64210753ebb974c117d649df7953fad45a80e54f3cea8b81df0e32.jpg)  
Fig. 11. Velocity cut of RD spectra at range = 25 .

As discussed in Section III.A, the amount of disturbed samples in the discrete beat signal may vary under different types of interference, the robustness of the algorithms will be further evaluated by introducing more interference-contaminated samples. By inserting further interference-contaminated samples into the real-world measured signals (about 5% of samples are disturbed at the outset), the interference scenarios with 10%, 15%, 20%, and 25% disturbed samples, can be generated. For the evaluation, 50 different interference signals are generated for each of these four interference scenarios. Fig. 12 shows how the SINR of these reconstruction algorithms changes with different percentages of disturbed samples in the discrete beat signal. As the percentage of disturbed samples increases, the SINR of the RD spectra recovered by all methods decreases accordingly. However, the autoencoder and IMATCS are more robust compared to the other methods and can provide a SINR of ca. 28 dB in the case where 25% of the samples are disturbed.

We further evaluated how the MAPE of the target peaks at 25 meter in the recovered RD spectra changes with different percentages of disturbed samples. The results are presented in Table II. In general, the proposed autoencoder yields smaller MAPE than the other algorithms, and similar to the zeroing and AR methods, its MAPE increases as more samples are disturbed. As shown in Fig. 11, IMATCS overestimates the power of the target peaks when 5% of samples are disturbed by interference. If the percentage of disturbed samples increases, the power of the reconstructed target peaks decreases accordingly, resulting in the power of the reconstructed target peaks becoming closer to the original. Hence, the MAPE of the reconstructed signal of IMATCS decreases as more samples are disturbed.

![](images/8d4edfa6aa14bdfdd9abadbbdd61a030ba862b2eda0f102d4ee3223d9db0ff34.jpg)  
Fig. 12. SINR of recovered RD spectrum. The dotted line indicates the SINR of the original RD spectrum.  
TABLE II

ANALYSIS RESULTS OF THE RECONSTRUCTION IN TERMS OF MAPEFOR DIFFERENT PERCENTAGE OF DISTURBED SAMPLES ANDMITIGATION TECHNIQUES. THE RESULTS OF THE PROPOSEDAUTOENCODER ARE HIGHLIGHTED IN BLUE
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=5>Mean absolute percentage error (MAPE)</td></tr><tr><td rowspan=1 colspan=1>Percentage</td><td rowspan=1 colspan=1>Disturbed</td><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>AR</td><td rowspan=1 colspan=1>IMATCS</td><td rowspan=1 colspan=1>Autoencoder</td></tr><tr><td rowspan=1 colspan=1>5%</td><td rowspan=1 colspan=1>0.2098</td><td rowspan=1 colspan=1>0.1160</td><td rowspan=1 colspan=1>0.0553</td><td rowspan=1 colspan=1>0.2803</td><td rowspan=1 colspan=1>0.0251</td></tr><tr><td rowspan=1 colspan=1>10%</td><td rowspan=1 colspan=1>0.2900</td><td rowspan=1 colspan=1>0.1662</td><td rowspan=1 colspan=1>0.1020</td><td rowspan=1 colspan=1>0.2291</td><td rowspan=1 colspan=1>0.0293</td></tr><tr><td rowspan=1 colspan=1>15%</td><td rowspan=1 colspan=1>0.2935</td><td rowspan=1 colspan=1>0.2044</td><td rowspan=1 colspan=1>0.1121</td><td rowspan=1 colspan=1>0.1581</td><td rowspan=1 colspan=1>0.0433</td></tr><tr><td rowspan=1 colspan=1>20%</td><td rowspan=1 colspan=1>0.3509</td><td rowspan=1 colspan=1>0.2354</td><td rowspan=1 colspan=1>0.1690</td><td rowspan=1 colspan=1>0.1599</td><td rowspan=1 colspan=1>0.0679</td></tr><tr><td rowspan=1 colspan=1>25%</td><td rowspan=1 colspan=1>0.3724</td><td rowspan=1 colspan=1>0.2546</td><td rowspan=1 colspan=1>1.1881</td><td rowspan=1 colspan=1>0.1084</td><td rowspan=1 colspan=1>0.1024</td></tr></table>

## D. Discussion

The proposed training strategy can be considered as a data augmentation technique [20] that can deal with data scarcity and insufficient data diversity. Due to the randomness of the interference generation mechanism in each training iteration, the trained model can effectively avoid overfitting.

During the training of neural networks for detection and reconstruction, about 10% samples are randomly disturbed with additive interference. However, the autoencoder is also capable of handling the scenarios that contain more interference (as presented in TABLE II). This makes its application in the real-world interference mitigation more reliable. It is worth mentioning that the proposed reconstruction neural network can deliver slightly better results in the severely disturbed scenarios if it is trained under the condition that more samples (e.g., maximum 35%) are randomly disturbed. This small improvement is observed by comparing the results (in terms of SINR and MAPE) with the reconstruction results of the neural network trained with the discrete beat signals where about 10% of the samples are randomly discarded.

The ablation study and perturbation analysis help to interpret the functionality of each component in the reconstruction neural network. The mask-gated convolution significantly improves the convergence speed of the reconstruction neural network. Interestingly, the benefits of using the composite loss can be maximized when employing the composite loss in conjunction with the mask-gated convolution.

## V. CONCLUSION

In this paper, a two-stage autoencoder model is developed for automotive radar interference mitigation. We introduce a new training strategy which eliminates the costly and challenging labeling process of the radar sensor data. The proposed interference detection network can identify the positions of disturbed samples more accurately than the conventional method regarding the F-score and the rate of true positives. Through the perturbation analysis of both the proposed autoencoder and the traditional autoencoder, the interpolation mechanism of neural networks can be better understood. The mask-gated convolution helps the neural network to exploit the relevant neighboring samples for the reconstruction of disturbed samples, thereby improving the SINR of the reconstructed RD spectra by ca. 1.5 to 2 dB compared to the traditional autoencoder. With the proposed mask-gated convolution and composite loss, the reconstruction neural network delivers superior recovery in terms of SINR and MAPE compared to the other reconstruction algorithms. Although the proposed neural networks are trained based on purely simulated discrete beat signals, they are able to properly handle the real-world scenarios that are more complex than the training data set. This demonstrates the robustness of the proposed autoencoder model. In future work, it is of interest to investigate the potential of deploying the proposed neural networks on a micro-controller, as most automotive radar sensors are constrained in terms of hardware resources.

## REFERENCES

[1] S. Chen, J. Taghia, T. Fei, U. Kühnau, N. Pohl, and R. Martin, “A DNN autoencoder for automotive radar interference mitigation,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Jun. 2021, pp. 4065–4069.

[2] J. Dickmann et al., “Automotive radar the key technology for autonomous driving: From detection and ranging to environmental understanding,” in Proc. IEEE Radar Conf. (RadarConf), May 2016, pp. 1–6.

[3] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[4] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[5] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, Sep. 2018.

[6] T.-N. Luo, C.-H. E. Wu, and Y.-J. E. Chen, “A 77-GHz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I, Reg. Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[7] S. Murali, K. Subburaj, B. Ginsburg, and K. Ramasubramanian, “Interference detection in FMCW radar using a complex baseband oversampled receiver,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 1567–1572.

[8] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[9] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207–1220, Mar. 2019.

[10] S. Chen, J. Taghia, U. Kühnau, T. Fei, F. Grünhaupt, and R. Martin, “Automotive radar interference reduction based on sparse Bayesian learning,” in Proc. IEEE Radar Conf. (RadarConf), Sep. 2020, pp. 1–6.

[11] J. Wang, M. Ding, and A. Yarovoy, “Matrix-pencil approach-based interference mitigation for FMCW radar systems,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 11, pp. 5099–5115, Nov. 2021.

[12] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. Eur. Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[13] F. Uysal and S. Sanka, “Mitigation of automotive radar interference,” in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 0405–0410.

[14] T. Fei, H. Guang, Y. Sun, C. Grimm, and E. Warsitz, “An efficient sparse sensing based interference mitigation approach for automotive radar,” in Proc. 17th Eur. Radar Conf. (EuRAD), Jan. 2021, pp. 274–277.

[15] S. Chen, P. Stockel, J. Taghia, U. Kühnau, and R. Martin, “Iterative 2D sparse signal reconstruction with masked residual updates for automotive radar interference mitigation,” EURASIP J. Adv. Signal Process., vol. 2022, no. 1, pp. 1–25, Apr. 2022.

[16] I. Goodfellow, Y. Bengio, and A. Courville, Deep Learning. Cambridge, MA, USA: MIT Press, 2016. [Online]. Available: http://www.deeplearningbook.org

[17] Y. N. Dauphin, A. Fan, M. Auli, and D. Grangier, “Language modeling with gated convolutional networks,” in Proc. 34th Int. Conf. Mach. Learn., vol. 70, 2017, pp. 933–941.

[18] J. Yu, Z. Lin, J. Yang, X. Shen, X. Lu, and T. Huang, “Free-form image inpainting with gated convolution,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2019, pp. 4470–4479.

[19] A. V. D. Oord, N. Kalchbrenner, O. Vinyals, L. Espeholt, A. Graves, and K. Kavukcuoglu, “Conditional image generation with PixelCNN decoders,” in Proc. 30th Int. Conf. Neural Inf. Process. Syst., Red Hook, NY, USA: Curran Associates, 2016, pp. 4797–4805.

[20] A. Mikolajczyk and M. Grochowski, “Data augmentation for improving deep learning in image classification problem,” in Proc. Int. Interdiscipl. PhD Workshop (IIPhDW), May 2018, pp. 117–122.

[21] X.-F. Yuan, L. Li, Y. Shardt, Y.-L. Wang, and C.-H. Yang, “Deep learning with spatiotemporal attention-based LSTM for industrial soft sensor model development,” IEEE Trans. Ind. Electron., vol. 68, no. 5, pp. 4404–4414, May 2021.

[22] X. Yuan, S. Qi, and Y. Wang, “Stacked enhanced auto-encoder for datadriven soft sensing of quality variable,” IEEE Trans. Instrum. Meas., vol. 69, no. 10, pp. 7953–7961, Oct. 2020.

[23] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in Proc. 22th Int. Conf. Inf. Fusion (FUSION), Jul. 2019, pp. 1–8.

[24] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 927–940, Jun. 2021.

[25] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Complexvalued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in Proc. IEEE Radar Conf. (Radar-Conf), May 2021, pp. 1–6.

[26] J. Fuchs, A. Dubey, M. Lübke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320.

[27] C. Jiang, T. Chen, and B. Yang, “Adversarial interference mitigation for automotive radar,” in Proc. IEEE Radar Conf. (RadarConf), May 2021, pp. 1–6.

[28] S. Chen, W. Shangguan, J. Taghia, U. Kühnau, and R. Martin, “Automotive radar interference mitigation based on a generative adversarial network,” in Proc. IEEE Asia–Pacific Microw. Conf. (APMC), Dec. 2020, pp. 728–730.

[29] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for FMCW radars,” 2021, arXiv:2108.13023.

[30] M. Umehira, T. Nozawa, Y. Makino, X. Wang, S. Takeda, and H. Kuroda, “A novel iterative inter-radar interference reduction scheme for densely deployed automotive FMCW radars,” in Proc. 19th Int. Radar Symp. (IRS), Jun. 2018, pp. 1–10.

[31] M. Kronauge and H. Rohling, “New chirp sequence radar waveform,” IEEE Trans. Aerosp. Electron. Syst., vol. 50, no. 4, pp. 2870–2877, Oct. 2014.

[32] F. Engels, P. Heidenreich, M. Wintermantel, L. Stacker, M. Al Kadi, and A. M. Zoubir, “Automotive radar signal processing: Research directions and practical challenges,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 865–878, Jun. 2021.

[33] D. P. Kingma and J. Ba, “ADAM: A method for stochastic optimization,” in Proc. 3rd Int. Conf. Learn. Represent. (ICLR), San Diego, CA, USA, May 2015, pp. 1–15.

[34] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” Int. J. Microw. Wireless Technol., vol. 6, pp. 371–378, Mar. 2014.

[35] S. Scheiblhofer, M. Treml, S. Schuster, R. Feger, and A. Stelzer, “A versatile FMCW radar system simulator for millimeter-wave applications,” in Proc. 38th Eur. Microw. Conf., Oct. 2008, pp. 1604–1607.

[36] R. C. Fong and A. Vedaldi, “Interpretable explanations of black boxes by meaningful perturbation,” in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), Oct. 2017, pp. 3449–3457.

[37] M. Azghani and F. Marvasti, “Iterative methods for random sampling and compressed sensing recovery,” in Proc. 10th Int. Conf. Sampling Theory Appl. (SAMPTA), Jul. 2013, pp. 1–4.

![](images/c2098d847a334b059908d3faceac0e59dcd54acbbf6fe91200cc53dd9e5ecac1.jpg)

Shengyi Chen received the B.Sc. degree in electrical and computer engineering from the Technical University of Kaiserslautern, Germany, and Fuzhou University, China, in 2016, and the M.Sc. degree in electrical and computer engineering from the Technical University of Munich, Germany. He is currently pursuing the Dr.-Ing. degree in electrical engineering and information technology with Ruhr-Universität Bochum, Germany, in cooperation with HELLA GmbH & Co. KGaA, Lippstadt, Germany. His research interests include automotive radar signal processing, machine learning, and compressive sensing.

![](images/e0584f795de0261c120171b282bf14d3eac8027698b0ea904ece2056e63e8aae.jpg)

Jalal Taghia received the B.Sc. and M.Sc. degrees in electrical engineering in Iran and the Dr.-Ing. degree from the Institute of Communication Acoustics (IKA), Ruhr-Universität Bochum, Bochum, Germany, in 2016.

Afterwards, he was a Research Fellow with the EU Marie Curie Initial Training Network AUDIS (“Digital Signal Processing in Audiology”) from 2009 to 2012. The title of his doctoral dissertation is “Speech Intelligibility Prediction and Single-Channel Noise Reduction Based on

Information Measures.” From 2016 to 2018, he worked as a Postdoctoral Researcher at the Institute of Communication Acoustics (IKA), Ruhr-Universität Bochum. From May 2018 to December 2021, he was a SW Developer at HELLA GmbH & Co. KGaA, Lippstadt, Germany, where he mainly contributed in the development of robust signal processing algorithms for automotive RADAR systems. Since January 2022, he has been an SW Developer for automotive RADAR solutions at Hella Aglaia Mobile Vision GmbH within Global Software House, Berlin, Germany. His main research interests include instrumental assessment of speech intelligibility, single-channel speech enhancement, and information theory for signal processing.

Uwe Kühnau received the German Diploma degree in physics and the Dr. rer. nat. degree in solid state physics from the University of Leipzig in 1993 and 1998, respectively.

He started his industrial career in pre-development for automotive sensors at Hella in 2000 and later headed the advanced engineering for radar systems. He is currently the Head of Radar Systems at Forvia.

![](images/a0930ad88a4c780c8ad68a3acbeeb75089c9b7f6a863bb865121a39c91d0645f.jpg)

Nils Pohl (Senior Member, IEEE) received the Dipl.-Ing. and Dr.Ing. degrees in electrical engineering from Ruhr University Bochum, Bochum, Germany, in 2005 and 2010, respectively.

From 2006 to 2011, he was a Research Assistant with Ruhr University Bochum, where he was involved in integrated circuits for millimeter-wave (mm-wave) radar applications. In 2011, he became an Assistant Professor with Ruhr University Bochum. In 2013, he became the Head of the Department of mm-wave Radar and

High Frequency Sensors with the Fraunhofer FHR, Wachtberg, Germany. In 2016, he became a Full Professor of Integrated Systems with Ruhr University Bochum. In parallel, he is the Head of the Research Group for Integrated Radar Sensors at Fraunhofer FHR. He has authored or coauthored more than 200 scientific papers and has issued several patents. His current research interests include ultra-wideband mm-wave radar, design, and optimization of mm-wave integrated SiGe circuits and system concepts with frequencies up to 500 GHz and above, as well as frequency synthesis and antennas.

Prof. Pohl is a member of VDE, ITG, EUMA, and URSI. He was a co-recipient of the 2009 EEEfCom Innovation Award. He was a recipient of the Karl-Arnold Award of the North Rhine-Westphalian Academy of Sciences, Humanities and the Arts in 2013 and the IEEE MTT Outstanding Young Engineer Award in 2018. Additionally, he was corecipient of the Best Paper Award at EUMIC 2012, the Best Demo Award at RWW 2015, and the Best Student Paper Awards at RadarConf 2020, RWW 2021, and EUMIC 2021.

![](images/49545c02fb5a5bec902c11f6b1b2216d61e41243844602a815e8b3f6e7fd48f5.jpg)

Rainer Martin (Fellow, IEEE) received the M.S.E.E. degree from the Georgia Institute of Technology, Atlanta, in 1989, and the Dipl.-Ing. and Dr.-Ing. degrees from RWTH Aachen University, Aachen, Germany, in 1988 and 1996, respectively.

From 1996 to 2002, he was a Senior Research Engineer with the Institute of Communication Systems and Data Processing, RWTH Aachen University. From April 1998 to March 1999, he was a Technology Consultant at the AT&T

Speech and Image Processing Services Research Lab (Shannon Labs), Florham Park, NJ, USA. From April 2002 to October 2003, he was a Professor of Digital Signal Processing at the Technische Universität Braunschweig, Braunschweig, Germany.

Since October 2003, he has been a Professor of Information Technology and Communication Acoustics at Ruhr-Universität Bochum, Bochum, Germany, and from October 2007 to September 2009, he was the Dean of the Electrical Engineering and Information Sciences Department. He is the coauthor with P. Vary of (Wiley, 2006) and the co-editor with U. Heute and C. Antweiler of (Wiley, 2008). His main research interests include signal processing, estimation and machine learning with applications in voice communication systems, hearing instruments, human–machine interfaces, and sensor networks.