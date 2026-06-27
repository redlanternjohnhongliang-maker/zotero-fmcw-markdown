# Automotive Radar Interference Mitigation using a Convolutional Autoencoder

Jonas Fuchs, Anand Dubey, Maximilian Lubke, Robert Weigel and Fabian Lurz¨

Friedrich-Alexander University Erlangen-Nurnberg (FAU)¨

Institute for Electronics Engineering, Cauerstr. 9, 91058 Erlangen, Germany Email: {jonas.fuchs, anand.dubey, maximilian.luebke, robert.weigel, fabian.lurz}@fau.de

Abstract—Automotive radar interference imposes big challenges on signal processing algorithms as it raises the noise floor and consequently lowers the detection probability. With limited frequency bands and increasing number of sensors per car, avoidance techniques such as frequency hopping or beamforming quickly become insufficient. Detect-and-repair strategies have been studied intensively for the automotive field, to reconstruct the affected signal samples. However depending on the type of interference, reconstruction of the time domain signals is a highly non-trivial task, which can affect following signal processing modules. In this work an autoencoder based convolutional neural network is proposed to perform image based denoising. Interference mitigation is phrased as a denoising task directly on the range-Doppler spectrum. The neural networks shows significant improvement with respect to signal-to-noiseplus-interference ratio in comparison to other state-of-the-art mitigation techniques, while better preserving phase information of the spectrum compared to other techniques.

## I. INTRODUCTION

Todays vehicles are equipped with a variety of different sensors utilized for comfort functions and advanced driver assistant systems. In particular radar is a key sensing technology for estimating distance and velocity of objects especially for safety related applications. More and more vehicles are equipped with millimeter-wave radar sensors while each vehicle can already contain several radar sensors itself. Consequently the amount of automotive radar systems on the streets is steadily increasing [1]. As automotive frequency bands are limited, this leads to an increasing probability of mutual interference between different sensors [2]. Depending on the modulations of the interfered radar and the interfering radar, a limited amount of time domain samples will be corrupted. This in turn increases the effective noise floor, reduces the detection sensitivity or even creates false detections. Therefore, countermeasures for radar interference need to be addressed. Radar interference can be coped with by utilizing different kinds of techniques such as polarization or coding techniques. Those, however, have only a limited effect, as there are just very few different polarizations available and coding techniques require additional computational as well as hardware costs. By using a detect-and-repair strategy, the effects of interference can be detected and mitigated afterwards [1]. A comparison of different mitigation techniques is shown in [3]. However, some of the considered mitigation techniques need a prior interference detection step, which in turn increases processing time.

Using traditional image processing algorithms, the authors of [4] propose a combined interference detection and mitigation based on processing the 2D raw data treated as an image. In [5], the authors propose a generative adversarial network (GAN) for denoising so called micro-Doppler signatures. Their neural network architecture extends the GAN principle introduced by Goodfellow [6] with conditional GANs to help the network generalize better. It basically removes the background noise and clutter from the images to obtain a more clear micro-Doppler image. As already mentioned, radar interference raises the noise floor in the frequency domain, thus it can be also mitigated by applying denoising techniques on the range-Doppler (RD) image. A deep learning based interference mitigation approach, proposed in [7], is based on convolutional neural networks (CNN) and aims to reduce the noise floor while preserving signal components. The respective architecture can be trained using either range processed data or RD spectra as inputs. While achieving promising results, there seems to be an implicit thresholding effect applied, which raises concerns of using this approach on real world measurement data.

In this paper a new approach to radar interference mitigation is proposed, by training a CNN based autoencoder (AE) to denoise interfered RD images. A derivation of the signal model of typical chirp-sequence based radar with and without interference allows accurate manipulation of measurement data, to obtain training data based on real world scenarios. Results of the trained network are compared with reference mitigation algorithms by means of visual, as well as qualitative measures.

## II. SIGNAL MODEL

## A. Radar Basics

Automotive radar sensors transmit frequency modulated continuous wave (FMCW) signals which enable the estimation of the delay of signal reflections via the frequency difference between transmitted (TX) and received (RX) signal. A simplified version of a typical radar front-end with the most important building blocks can be seen in Fig. 1b. The chosen waveform is generated by a local oscillator (LO) and transmitted via the TX antenna. The RX antenna then captures the incoming signal reflections. After amplifying the received signal, it is mixed with the original transmitted waveform and passed through subsequent bandpass filtering (BPF). This removes any high-frequency components that could cause aliasing as well as low-frequency components from direct coupling of the local oscillator signal into the receiver [8]. After mixing and filtering the signal has been shifted to an intermediate frequency (IF) and is thus called $s _ { \mathrm { I F } } ( t )$ . The IF bandwidth $B _ { \mathrm { I F } }$ is determined by the upper cutoff frequency of the bandpass filter which is typically in the <sup>MHz</sup> range.

![](images/21d557cbee569bfbb457f4c5f50bc6dd83018a3315c6a813b5b4d9cb2689b5a8.jpg)  
Fig. 1. a) Scenario with an interferer whose transmit signal (dashed orange) superimposes a reflected signal (blue) and is received by the victim radar. b) Block diagram of the radar front-end and its receive chain including the mixer, band pass filter and analog-to-digital converter. The digitized samples s<sub>IF</sub>[k] are stored into a data matrix $s [ k , l ]$

Fig. 2a shows the concept of a FMCW modulation in detail. The LO generates a chirp signal $s _ { \mathrm { L O } } ( t )$ with starting frequency $f _ { \mathrm { 0 , L O } }$ , bandwidth $B _ { \mathrm { c } }$ , duration $T _ { \mathrm { c } }$ and resulting sweep rate $\mu _ { \mathrm { L 0 } } = \left. B _ { \mathrm { c } } \right/ T _ { \mathrm { c } }$ . Assuming unity amplitude, for a single chirp $s _ { \mathrm { L O } } ( t )$ can be formulated by

$$
s _ { \mathrm { L O } } ( t ) = \left\{ \begin{array} { l l } { \cos \left( 2 \pi f _ { \mathrm { 0 , L O } } t + \mu _ { \mathrm { L O } } \pi t ^ { 2 } + \varphi _ { \mathrm { 0 , L O } } \right) } & { 0 \leq t \leq T _ { \mathrm { c } } } \\ { 0 } & { \mathrm { e l s e } , } \end{array} \right.\tag{1}
$$

where $\varphi _ { \mathrm { 0 , L O } }$ corresponds to the initial phase of the LO. If this signal gets reflected by some object, also referred to as target, the reflection will be received at the radar with a time delay which is proportional to the targets distance. Additionally, signals of multiple reflections are superimposed to each other at the receiver. For an arbitrary number $N _ { { \mathrm { t g t } } }$ of targets, the received signal $s _ { \mathrm { R X } } ( t )$ can thus be expressed by

$$
s _ { \mathrm { R X } } ( t ) = \sum _ { i = 1 } ^ { N _ { \mathrm { t g t } } } s _ { \mathrm { L O } } ( t - \tau _ { i } ) + \mathrm { n } ,\tag{2}
$$

where $\tau _ { i }$ is the round trip delay to the -th target and <sup>n</sup> contains any noise or clutter. The noise free case is assumed for all following considerations. The received and amplified signal is mixed with the original LO signal to obtain

$$
s _ { \mathrm { m i x } } ( t ) = s _ { \mathrm { R X } } ( t ) \cdot s _ { \mathrm { L O } } ( t ) = \frac { 1 } { 2 } ( c o s ( \phi _ { \mathrm { d i f f } } ) + c o s ( \phi _ { \mathrm { s u m } } ) ) ,\tag{3}
$$

where <sub>diff</sub> contains the difference of LO and RX signal frequencies and $\phi _ { \mathrm { s u m } }$ contains the sum frequencies respectively [8]. The sum component is removed by the following bandpass filtering and the resulting intermediate frequency signal is obtained

$$
s _ { \mathrm { I F } } ( t ) = \frac { 1 } { 2 } c o s ( \phi _ { \mathrm { d i f f } } ( t ) ) .\tag{4}
$$

![](images/251983001e9ab88f076b659a8561a293cdb6ecea5dac2c556c30f69d3ea01884.jpg)  
Fig. 2. Illustration of the FMCW radar principle. In a) the transmitted frequency ramp is shown in black, whereas a delayed copy of the ramp is depicted in blue. The cyan background illustrates the intermediate frequency bandwidth of the receiver. In b) a continuous wave signal (dashed orange) interferes with the radar.

The IF signal is then digitized by an analog-to-digital converter with sampling period $T _ { \mathrm { s } }$ at the discrete time instants $k \cdot T _ { \mathrm { s } }$ where $k \in [ 0 , . . . , N _ { \mathrm { s } } { - } 1 ]$ . Consequently the discrete time signal $s _ { \mathrm { I F } } [ k ]$ contains $N _ { \mathrm { s } }$ samples per chirp. Typically, automotive radar sensors rapidly transmit several identical chirps in a so called chirp sequence (CS) modulation. The digitized IF samples $s _ { \mathrm { I F } } [ k ]$ are then stored chirp wise in a data matrix for coherent processing, as shown in Fig. 1b. Samples are stored along the rows, called fast-time dimension, whereas consecutive chirps are stored along the columns, called slow-time dimension. By calculating the two dimensional fast Fourier transform (FFT) on this data matrix, fast-time is converted to range-frequency and slow-time to velocity-frequency. This operation yields the spectrum $S _ { \mathrm { R D } }$ from which range and velocity of all targets can be estimated [9].

## B. Interference Model

In order to analyze the influence of an interferer on the IF signal, the scenario depicted in Fig. 1a is considered. An interferer transmits an arbitrary radio frequency signal (orange), such that it overlaps with the signal reflected from the scene (blue). The interferers signal is linearly superimposed on the signal reflected by targets, thus eq. (2) can be extended to account for the interference signal components

$$
s _ { \mathrm { R X } } ^ { \prime } ( t ) = \sum _ { i = 1 } ^ { N _ { \mathrm { t g t } } } s _ { \mathrm { L O } } ( t - \tau _ { i } ) + \sum _ { j = 1 } ^ { N _ { \mathrm { i n t } } } s _ { \mathrm { i n t } , j } ( t - \tilde { \tau } _ { j } ) ,\tag{5}
$$

where $N _ { \mathrm { i n t } }$ corresponds to the total number of interferers, $s _ { \mathrm { i n t } , j } ( t )$ to the signal component transmitted by the -th interferer and $\tilde { \tau } _ { j }$ to the one way propagation delay of the $j -$ <sup>τ j</sup>th interferer. Without loss of generality the number of total interferers is limited to $N _ { \mathrm { i n t } } = 1$ for all further considerations. Using eq. (3) and eq. (5) it follows

$$
s _ { \operatorname* { m i x } } ^ { \prime } ( t ) = \underbrace { \sum _ { i = 1 } ^ { N _ { \mathrm { t g t } } } s _ { \mathrm { L O } } ( t - \tau _ { i } ) \cdot s _ { \mathrm { L O } } ( t ) } _ { s _ { \operatorname* { m i x } } ( t ) } + \underbrace { s _ { \operatorname* { m i x } , 1 } ( t - \tilde { \tau } _ { 1 } ) \cdot s _ { \mathrm { L O } } ( t ) } _ { s _ { \operatorname* { m i x } , \mathrm { i n t } } ( t ) } ,\tag{6}
$$

where the first term corresponds to the mixing signal for the case without any interference while the seconds term accounts for the interference component only. The authors of [10] give a detailed time-domain IF signal model for the interference component $s _ { \mathrm { m i x , i n t } } ( t )$ . However, the BPF is assumed to be ideal, whereas a non-ideal filter will have significant impact on the resulting IF signal, as has been shown in [8]. For differing sweep rates of victim radar and interferer $( \mu _ { \mathrm { L O } } \neq \mu _ { \mathrm { i n t } } )$ , the influence of the BPF on the final IF signal can be modeled using the filters impulse response

![](images/67eef5f7143c8f6b3d077e5748ee103edb805fc4b381e430df87d96816fc5ad9.jpg)  
Fig. 3. Diagram of a typical automotive radar signal processing chain. Samples affected by interference usually have to be detected first and are mitigated in a second step (green block). After 2D-RD processing, targets can be detected by CFAR or similar detection algorithms. The proposed approach (orange block) does not need a prior detection step and instead directly operates on the 2D-RD spectrum.

$$
s _ { \mathrm { I F } } ^ { \prime } ( t ) = h _ { \mathrm { B P F } } ( t ) * s _ { \mathrm { m i x } } ^ { \prime } ( t ) .\tag{7}
$$

## III. AUTOMOTIVE RADAR SIGNAL PROCESSING

Fig. 3 shows the main steps of a typical automotive radar signal processing chain, indicated by black arrows and boxes. The sampled IF data is first processed in time domain to remove any static offsets. A subsequent interference detection step detects any corrupted samples. The mitigation algorithm performs the actual reconstruction of the affected samples. A 2D FFT in fast-time and slow-time dimension of the IF data matrix yields the complex RD spectrum. Detection of targets is usually performed by constant false alarm rate (CFAR) algorithms [9].

As interference detection and mitigation are early steps in the pipeline, all other following modules will be impacted by a possible malfunction or missed detections. Thus, a combined detection and mitigation, located after RD processing, could lead to overall increasing system performance, as it is less prone to introduce errors on subsequent processing steps. The CNN based autoencoder is depicted in orange in Fig. 3, its architecture is introduced in detail in section IV-C. To obtain a state-of-the-art reference and comparison of the proposed approach, traditional interference mitigation methods are introduced in the following.

## A. Zeroing

A simple and intuitive mitigation method is zeroing, where corrupted IF signal samples are simply set to zero. As a downside, this method needs a detection step in advance. Because of its simplicity it often serves as a baseline for comparison of different mitigation techniques as presented in [3].

TABLE I  
MODULATION PARAMETERS FOR INTERFERING RADARS IN MEASUREMENTS AS WELL AS SIMULATIONS.
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>Modulations</td></tr><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=1> $f _ { 0 }$ </td><td rowspan=1 colspan=1>76 GHz</td><td rowspan=1 colspan=1>76.75 GHz</td></tr><tr><td rowspan=1 colspan=1> $B _ { \mathrm { c } }$ </td><td rowspan=1 colspan=1>0GHz</td><td rowspan=1 colspan=1>1GHz</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c } }$ </td><td rowspan=1 colspan=1>328μs</td><td rowspan=1 colspan=1>∞(CW)</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { c c } }$ </td><td rowspan=1 colspan=1>0μs (CW)</td><td rowspan=1 colspan=1>568 μs</td></tr><tr><td rowspan=1 colspan=1> $N _ { \mathrm { c } }$ </td><td rowspan=1 colspan=1>1 (CW)</td><td rowspan=1 colspan=1>128</td></tr></table>

## B. Moving Median Filter

The median filter is a nonlinear filter that is mostly used in digital signal processing or image processing applications for signal smoothing and noise removal [11]. Basically $N _ { \mathrm { m e d } }$ signal samples are selected by a windowing operation, sorted and a median operation is performed to obtain the filtered signal value. Interfered signal samples are first detected and set to ”not a number” (NaN). For reconstruction, a moving median filter (MMF) is applied on the whole IF signal. Only missing values are replaced by the median value, while NaN values are ignored in the calculation.

## IV. METHODOLOGY

## A. Generation of Training Data

The neural network is trained for an image-to-image translation of corrupted RD images to a non-interfered version. Therefore, a considerably large amount of RD images, as well as their corrupted counterpart, is needed. During the network training, the labels are used as a baseline to compute the respective loss function and update the network parameters. As real measurement data is used for training, simulated or measured interference signals are introduced manually in a post-processing step. Using a special operation mode, similar to the one described in [8], where the transmit path of the victim radar is shut off and thus only the interference signal component is received and mixed with the LO signal to obtain $s _ { \mathrm { I F , i n t } } ^ { \prime } ( t )$ . Considering the linear superposition of interference signal and target reflections according to eq. (6), a new IF signal containing corrupted samples is artificially created by

$$
s _ { \mathrm { I F , c o r r } } ( t ) = s _ { \mathrm { I F } } ( t ) + s _ { \mathrm { I F , i n t } } ( t ) .\tag{8}
$$

The term $s _ { \mathrm { I F , i n t } } ^ { \prime }$ corresponds to the IF signal after bandpass filtering the interference term. Accordingly $s _ { \mathrm { I F } } ( t )$ corresponds <sup>s t</sup>to the IF signal of a non-interfered measurement snapshot. Instead of using real measurements of interference, simulated interference can be generated equivalently by using the signal model from eq. (7) to obtain $s _ { \mathrm { I F , i n t } } ^ { \prime } ( t )$ . Multiple configurations of an interfering radar are used to create a dataset which is as diverse as possible. Therefore, different FMCW as well as CW configurations are implemented in simulations as well as on the measurement hardware. The detailed modulation parameters are summarized in table I.

![](images/75ff42e6c8585050172d1ad6e04666863f5d742784cb5129d6f240b6d617c208.jpg)

![](images/0b12c47f8519fa5b991bff26f7966900c83e3d5b34678135aa73c8b031643b0b.jpg)

![](images/46223e86a8dd6565fe9f0b51bfa5a5bbecb6de257356ac0637f95a440927d339.jpg)  
Fig. 4. Comparison between a raw IF signal without any interference (a), measured IF signal with interference (c) and the IF signal with artificially added interference (e) on the signal from (a). The right column (b,d,f) depicts the corresponding RD images.

The difference in sweep rate between the victim radar $\left( \mu _ { \mathrm { L O } } \right)$ and the interfering radar $( \mu _ { \mathrm { i n t } } )$ , in combination with the BPF characteristics, defines the shape of the interference IF signal. Similar sweep rates produce a chirp-like signal, whereas a large difference in sweep rates produces only an impulse like IF signal [8]. In simulations the upper BPF cutoff frequency is set to $f _ { \mathrm { B P F , u p p e r } } = 4 \mathrm { M H z }$

<sup>f</sup>In a real world scenario the actual time of ramp crossing between interfering radar waveform and LO ramp is arbitrary and depends on a variety of parameters such as ramp start times $t _ { 0 , \mathrm { L O } }$ and $t _ { 0 , \mathrm { i n t } } ,$ sweep rates $\mu _ { \mathrm { L O } }$ and $\mu _ { \mathrm { i n t } }$ and start frequencies $f _ { \mathrm { 0 , L O } }$ and $f _ { 0 , \mathrm { i n t } } .$ . Thus the exact time of ramp crossing is considered as random uniformly distributed within the total chirp duration $T _ { \mathrm { c } }$ . Different time instances of crossing are simulated by adding interference onto the measurement at a random index for each chirp sequence. Standard RD processing then yields the complex valued RD spectrum. A comparison between measured and artificially corrupted RD images is depicted in Fig. 4. The first row shows a real measurement IF signal (a) and the corresponding RD image (b). In the second measurement the corruption of a CW interference can be observed at signal samples 128 - 140 (c). The resulting RD image (d) shows a significantly increased noise floor. The last row shows the results of the applied processing routine. Artificial interference samples are added onto the signal from (a) to produce the corrupted IF signal. Note the good agreement of the simulated signal (e) with the measured signal from (c) as well as their corresponding RD images.

Neural networks in generally are designed for real numbered computations, thus the complex valued RD spectrum is separated into its magnitude and phase component. All data samples are normalized in order to maintain consistent input value ranges for the network. The magnitude is normalized by the maximum value to the range <sup>[0</sup> <sup>1]</sup>, whereas the angle is <sup>,</sup>normalized to <sup>[</sup>−<sup>1</sup> <sup>1]</sup> by dividing by .

## B. Experimental Setup

Several outdoor measurements are performed in order to obtain enough real world data for training the neural network. Fig. 5a) shows the victim radar sensor as well as a camera used for recording the scenes. Several scenes containing mostly vulnerable road users such as pedestrians and cyclists are recorded. Additionally a radar sensor, acting as the interferer, is placed in a distance of approximately 4 meters from the victim radar, but outside of its field-of-view. To collect real world reference scenarios, the interference sensor was switched on for some measurements, with the modulations listed in table I.

![](images/416049de4718fb932e95c4cc998a911b0e04f03589c1de9957e99298c02dbc1f.jpg)  
Fig. 5. Experimental setup: (a) shows the victim radar and camera (left), as well as the interfering radar sensor on a tripod (right). (b) shows a typical measurement scene containing one cyclist while (c) depicts the corresponding RD image. The effect of interference is clearly visible as striped artifacts along the range dimension.

## C. Denoising Autoencoders

Autoencoders are neural networks that are trained by unsupervised learning. They inherently learn a compressed representation of their input  by first reducing  to an internal representation , also called latent variable, by applying some function $z = f ( x )$ . For CNNs, this means the dimensionality of successive layers is reduced, until the so called bottleneck, compare Fig. 6. After that, a reconstruction of the original input is performed to obtain the output $r = g ( z )$ , by increasing the dimensionality of subsequent layers. During training, the network tries to minimize the loss function

$$
L ( x , g ( f ( x ) ) ) ,\tag{9}
$$

to match the output as close as possible to the input [6]. Autoencoders can also be used for denoising tasks, by simply changing the loss function from (9) and instead minimize the function

$$
L ( x , g ( f ( x + n ) ) ) ,\tag{10}
$$

where noise  is added to the input . Therefore, the denoising autoencoder tries to learn the combination of $f ( \cdot )$ and $g ( \cdot )$ to undo the noise addition.

In the proposed architecture a CNN based autoencoder is used in combination with skip connections between encoder and decoder network. Skip connections in general can be used to pass low-level information from the input and early layers across the bottleneck and add this information to the generated image [12]. This helps to preserve important parts from the original image, i.e. signal components from target reflections, which could otherwise get lost while reducing the dimensions of the image. Fig. 6 gives an overview of all used layers of the encoder as well as the decoder part. Magnitude and phase of the RD spectrum are fed into the network as a two channel image. The input image of size <sup>256</sup>×<sup>256</sup> is fed trough two subsequent combinations of a 2D convolutional layer (Conv2D) and a max pooling layer (MaxPooling2D). Most 2D convolutional layers use a rectified linear unit (ReLU) as the activation function. Each max pooling layer halves the image size, until layers in the bottleneck with size $3 2 \times 3 2$ . After the bottleneck, a skip connection combines one layer directly from the encoder part of the network with the current convolutional layer. Convolutional transpose layers (Conv2DTranspose) are used to upsample the data to the original size. After another skip connection and a subsequent convolutional transpose layer, the original input size is obtained. The magnitude and phase output images are retrieved by two separate convolutional layers with different activation functions. To match the value range of <sup>[0 1]</sup>, a sigmoid activation is used at the magnitude output layer. Consequently a hyperbolic tangent (tanh) activation is used to generate the normalized phase in the range <sup>[</sup>−<sup>1 1]</sup> at the output. Finally a concatenation layer combines the two separate outputs into a two channel image, matching the shape of the inputs.

![](images/c1bd105dc29e0b64a7a338747056169fdee2a1145c303627ce6aa345db697494.jpg)  
Fig. 6. Diagram of the used autoencoder model, implemented as a convolutional encoder-decoder architecture with UNet inspired skip connections. Magnitude and phase of the interfered RD map are fed into the network as a two channel image. The network outputs a denoised image of the same size.

In order to train the network properly on training examples, a loss function will be evaluated after each training step. It compares the desired output, also referred to as label, with the actual output and calculates the corresponding loss. The structural similarity (SSIM) index has been shown to achieve significantly better results in qualitative visual image comparison than the mean squared error (MSE) [13]. In general SSIM assesses and compares the visual impact of three characteristics in images, namely luminance, contrast and structure. This is benefits the task of interference removal, as target peaks should be preserved in the predicted RD images. For visual comparison, only absolute values are used, thus SSIM is applied on the magnitude channel only. In addition, regular binary cross entropy (BXE) is included as pixel wise loss function on the magnitude channel. Yet, phase values of the RD image should also be retained for the prediction, hence a MSE loss is used on the phase channel. The overall loss function is a weighted combination of the aforementioned losses and can be described as

$$
\begin{array} { r l } & { L = w _ { 1 } \cdot \mathrm { M S E } ( \sphericalangle ( x ) , \odot ( r ) ) } \\ & { \phantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } } \\ & { \phantom { x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x } + w _ { 2 } \cdot \mathrm { S S I M } ( | x | , | r | ) + w _ { 3 } \cdot \mathrm { B X E } ( | x | , | r | ) , } \end{array}\tag{11}
$$

where $\sphericalangle ( \cdot )$ extracts the phase channel and the weights $w _ { 1 }$ , <sub>2</sub> and $w _ { 3 }$ <sup>w w</sup>are determined empirically as 2, 5 and 10. All hyperparameters used to train the network, are chosen empirically from the best performing trial on validation data. The final network is trained on the full training dataset containing 6588 RD images with a batch size of 16, using an Adam optimizer with an initial learning rate of 0.001 and the prior mentioned loss function. The dataset for testing consists of 2196 images.

## V. RESULTS

The following section describes the results of the trained autoencoder network on a testing set of artificially introduced interference data as well as on real interference data.

## A. Performance measures

First several performance indicators are defined to enable a quantitative comparison of the networks prediction with the original image. Usually the goal in radar signal processing is to maximize the detection probability. Thus a rather intuitive measure is the signal-to-interference-plus-noise ratio (SINR) described in [3], [7], as it compares the average signal power of all target peaks with the average noise power. As the SSIM index is an excellent measure for visual image comparison, it is also used as a performance measure of the results to compare the interference free RD spectrum $\hat { S } _ { \mathrm { R D } }$ with the reconstructed spectrum $S _ { \mathrm { R D } , r } .$ As third measure, the so called error vector magnitude (EVM) is used. It compares the complex values of detections in the original image with the corresponding values from the prediction. The EVM is defined in [3] as

$$
\mathrm { E V M } = \frac { 1 } { N _ { 0 } } \sum _ { i , j \in \mathcal { O } } \frac { \left| \hat { S } _ { \mathrm { R D } } [ i , j ] - S _ { \mathrm { R D } , r } [ i , j ] \right| } { \left| \hat { S } _ { \mathrm { R D } } [ i , j ] \right| } ,\tag{12}
$$

where O corresponds to the set of $N _ { 0 }$ target detections, containing their corresponding indices $\{ i , j \}$ in the RD spectrum.

All performance measures which need a target detection to determine the number of targets and corresponding indices, use a standard cell averaging CFAR algorithm with arbitrary configuration.

## B. Comparison with baseline

Before evaluating quantitative measures, a visual comparison of the autoencoder denoising is performed. Fig. 7 shows original (a), interfered (b) and denoised (c) RD spectra belonging to the same measurement snapshot. It can be concluded that the network significantly reduces the noise floor of the RD image, while the prominent target peaks are retained.

![](images/a3ff0ff2d047ec66c0d0842445c3d9680e3114194224331bac99c08a4f041bd1.jpg)

![](images/ef308670df3ff3af008e39de9c6f1d72bff02a54613223108e42cb43f9430d8a.jpg)

![](images/03d11849b8f004754fe04ef0c3aaccf18aa2bec1b7d52d8b44864115908ff4e8.jpg)  
Fig. 7. Comparison of the original RD image (a), the interfered input image (b) and the denoised prediction of the autoencoder (c).

Furthermore, the aforementioned performance measures are evaluated on the whole testing set. All following numbers were obtained using a distinct test set containing corrupted images created from multiple interference modulations as described in section IV-A. Table II shows a comparison of different mentioned interference mitigation methods with respect to SINR, SSIM and EVM. Results show that SINR on average drops by about <sup>4</sup> <sup>dB</sup> for the interfered RD map. While zeroing fails to restore the original noise floor in the complex RD spectrum, the MMF algorithm increases SINR to almost the original value and the AE even increases the SINR by around <sup>5</sup> <sup>dB</sup> in comparison to the original spectrum. Regarding the EVM there is no significant difference between the interfered RD, zeroing and MMF results. The AE however, slightly decreases the average EVM by 0.1. Finally the SSIM has to be compared separately on magnitude an phase of the predictions. In general, none of the approaches achieve a high SSIM on the phase. However the AE still shows the highest similarity scores on both magnitude and phase comparison with the noninterfered RD image.

## VI. CONCLUSION

An alternative approach to traditional interference mitigation, based on a convolutional autoencoder is proposed. After feeding magnitude and phase of the RD spectrum into the trained network, it predicts a denoised version of the RD spectrum. It is shown to generally perform better than reference algorithms, with respect to SINR and SSIM on real world measurement data. While the network generalizes well on different types of interference, phase information still cannot be fully preserved and thus needs to be investigated further. For future work, an extension of the autoencoder to use 3D convolutional layers, as well as the introduction of variational inference into the network could be studied. Furthermore the impact on detection performance as well as the integration into a full radar signal processing chain should be investigated in more detail.

TABLE II  
PERFORMANCE EVALUATION OF DIFFERENT INTERFERENCE MITIGATION ALGORITHMS.
<table><tr><td rowspan=1 colspan=1>Method</td><td rowspan=1 colspan=1>SINR</td><td rowspan=1 colspan=1>EVM</td><td rowspan=1 colspan=1>SSIM (abs)</td><td rowspan=1 colspan=1>SSIM (phase)</td></tr><tr><td rowspan=1 colspan=1>RD clean</td><td rowspan=1 colspan=1>22.70</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>RD interfered</td><td rowspan=1 colspan=1>18.35</td><td rowspan=1 colspan=1>0.3375</td><td rowspan=1 colspan=1>0.5969</td><td rowspan=1 colspan=1>0.0049</td></tr><tr><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>11.32</td><td rowspan=1 colspan=1>0.3612</td><td rowspan=1 colspan=1>0.012</td><td rowspan=1 colspan=1>0.0443</td></tr><tr><td rowspan=1 colspan=1>MMF</td><td rowspan=1 colspan=1>21.90</td><td rowspan=1 colspan=1>0.3348</td><td rowspan=1 colspan=1>0.0134</td><td rowspan=1 colspan=1>0.0553</td></tr><tr><td rowspan=1 colspan=1>CNN AE</td><td rowspan=1 colspan=1>27.58</td><td rowspan=1 colspan=1>0.2249</td><td rowspan=1 colspan=1>0.8677</td><td rowspan=1 colspan=1>0.2648</td></tr></table>

## ACKNOWLEDGMENT

The author wish to acknowledge all national funding authorities and the ECSEL Joint Undertaking, which funded the PRYSTINE project under the grant agreement 783190.

## REFERENCES

[1] M. Kunert, “The eu project mosarim: A general overview of project objectives and conducted work,” in 2012 9th European Radar Conference, Oct 2012, pp. 1–5.

[2] G. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, feb 2007.

[3] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Performance comparison of mutual automotive radar interference mitigation algorithms,” in 2019 IEEE Radar Conference (RadarConf), April 2019, pp. 1–6.

[4] M. Barjenbruch, D. K. J. Klappstein, K. Dietmayer, and J. Dickmann, “A method for interference cancellation in automotive radar,” in 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility. IEEE, 2015.

[5] K. Armanious, S. Abdulatif, F. Aziz, B. Kleiner, and B. Yang, “Towards adversarial denoising of radar micro-doppler signatures,” in IEEE International Radar Conference 2019, 2019.

[6] I. Goodfellow, Y. Bengio, and A. Courville, Deep Learning. MIT Press, 2016, http://www.deeplearningbook.org.

[7] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in 2019 22nd International Conference on Information Fusion (FUSION) (FUSION 2019), 2019.

[8] M. Gardill, J. Schwendner, and J. Fuchs, “In-situ time-frequency analysis of the 77 ghz bands using a commercial chirp-sequence automotive fmcw radar sensor,” in 2019 IEEE MTT-S International Microwave Symposium (IMS), June 2019, pp. 544–547.

[9] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, no. 2, pp. 22–35, mar 2017.

[10] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical investigation of non-coherent mutual fmcw radar interference,” in 2018 15th European Radar Conference (EuRAD), Sep. 2018, pp. 71–74.

[11] J. D. Broesch, Digital Signal Processing. Newnes, 2008. [Online]. Available: https://www.ebook.de/de/product/7338407/james d broesch digital signal processing instant access.htm

[12] M. Stephan and A. Santra, “Radar-based human target detection using deep residual u-net for smart home applications,” in International Conference on Machine Learning Applications (ICMLA), Dec. 2019, pp. 1–8.

[13] Zhou Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, “Image quality assessment: from error visibility to structural similarity,” IEEE Transactions on Image Processing, vol. 13, no. 4, pp. 600–612, April 2004.