(d)

(c)

# Complex-valued Convolutional Neural Networks for Enhanced Radar Signal Denoising and Interference Mitigation

Alexander Fuchs<sup>1§</sup>, Johanna Rock<sup>1§</sup>, Mate Toth<sup>12</sup>, Paul Meissner<sup>2</sup>, Franz Pernkopf<sup>1</sup>

<sup>1</sup>Graz University of Technology, Austria, <sup>2</sup>Infineon Technologies Austria AG, Graz

Email: fuchs@tugraz.at, johanna.rock@tugraz.at

Abstract—Autonomous driving highly depends on capable sensors to perceive the environment and to deliver reliable information to the vehicles’ control systems. To increase its robustness, a diversified set of sensors is used, including radar sensors. Radar is a vital contribution of sensory information, providing high resolution range as well as velocity measurements. The increased use of radar sensors in road traffic introduces new challenges. As the so far unregulated frequency band becomes increasingly crowded, radar sensors suffer from mutual interference between multiple radar sensors. This interference must be mitigated in order to ensure a high and consistent detection sensitivity. In this paper, we propose the use of Complex-Valued Convolutional Neural Networks (CVCNNs) to address the issue of mutual interference between radar sensors. We extend previously developed methods to the complex domain in order to process radar data according to its physical characteristics. This not only increases data efficiency, but also improves the conservation of phase information during filtering, which is crucial for further processing, such as angle estimation. Our experiments show, that the use of CVCNNs increases data efficiency, speeds up network training and substantially improves the conservation of phase information during interference removal.

## I. INTRODUCTION

Advanced Driver Assistance Systems (ADAS) and Autonomous Vehicles (AV) rely on multi modal sensor data for the perception of the vehicles’ surroundings. Radar sensors deliver valuable information about object locations as well as object velocities. Frequency modulated continuous wave (FMCW)/chirp sequence (CS) radars are the most commonly used radar systems for automotive applications. They transmit sequences of linearly modulated chirp signals within a non-regulated spectrum.

Due to the lack of transmit regulations and the increased traffic volume of autonomous and radar-enhanced vehicles, the chance of mutual interference between multiple radar sensors increases. In most cases this interference is of non-coherent nature, where the involved radar sensors operate with different transmit parameters. Non-coherent interference leads to a decreased object detection sensitivity, caused by broadband disturbances within the radar signal.

Typically, interference mitigation of mutual interference is performed using classical signal processing algorithms. The most rudimentary method is to substitute all interference-affected samples with zero [1], followed by an optional smoothing of the boundaries. More advanced methods use non-linear filtering in slow-time [2], iterative reconstruction using Fourier transforms and thresholding [3], estimation and subtraction of the interference component [4], or beamforming [5].

Recently, the use of deep learning and neural networks has been proposed for interference mitigation. Neural networks are typically applied in a supervised manner such that the signal is filtered and the interference is damped. Recurrent Neural Networks (RNNs) [6], [7] are commonly applied to time-domain signals, while in frequency-domain preferably Convolutional Neural Network (CNN) -based models are used. The proposed CNN-architectures range from very small CNNs [8], [9] over Convolutional Autoencoders [10], U-Net inspired CNNs [11], to bigger CNNs that try to learn a signal transformation from STFT to FFT additional to denoising the signal [12].

![](images/da9981a0be836f9d1a619e4652b99af2529d9e5e274edb6ff42a1baa271949d5.jpg)  
(b)

![](images/c842c9637502b8a54dc9ff4fbf46e814c35c0413974ee8957eb89af0f3b74c7d.jpg)

![](images/264e87d6e8b0045d2bcd7956a3f0cd073bc648265afbaa609e344abb04b52804.jpg)

![](images/43d3ada6b8cdde6f95bb77e961718b9ea0d91aa93e99f4688ddf33527a9d9488.jpg)  
Fig. 1: Range-Doppler map examples; (a) clean data ; (b) with added simulated interference; (c) denoised using a complex-valued CNN; (d) denoised using a real-valued CNN.

The classical signal processing chain, as depicted in Fig. 2, processes the raw radar signal in several steps to a frequency representation that resembles the characteristics of images. This image-like representation of the signal enables the use of powerful computer-vision methods, e.g CNNs. The range-Doppler map, as presented in Fig. 1, is particularly well suited for denoising and interference mitigation. This complex-valued spectrum is represented as a 2D matrix with signal peaks corresponding to the distances and velocities of objects. The proposed CNN-based models for interference mitigation substantially improve the results of classical methods when subsequently used for object detection [8], [11], [12]. These object detection algorithms are applied to the magnitude spectrum of the interference mitigated RD-maps. However, for phase-dependent tasks none of the approaches (classical or deep learning based methods) are capable of sufficiently reconstructing the phase of the clean signal. Most of recent works provide the real- and imaginary parts of the complex spectra as inputs, in order to perform phase estimations. However, they rely purely on data to learn the relationship between real- and imaginary parts of the spectra, adding additional complexity to the learning problem.

Therefore we propose the use of complex-valued CNNs (CVCNNs) for radar signal denoising and interference mitigation. The use of complex-valued analysis introduces an inductive bias, restricting the degrees of freedom in the network. This restriction can however benefit the learning behavior substantially, since it enforces signal transformations according to the physical characteristics of the data and reduces the problem complexity.

![](images/5af9ce53531b43295ff9b6257e099e75d18aed3e888c48e912ecd3ea33f4e674.jpg)  
Fig. 2: Block diagram of a basic FMCW/CS radar processing chain. The red dashed box indicates the location of the proposed interference mitigation step using a CNN-based approach.

CVCNNs were first proposed in the 1990s [13]. Recently, Trabelsi et al. [14] proposed a CVCNN, that incorporates complex-valued analysis using two real-valued convolution kernels. This enables model training to be performed using conventional backpropagation. CVCNNs have been applied to Synthetic Aperture Radar (SAR) data for semantic segmentation [15] and super-resolution imaging [16] with promising results, however limited in experiments and performance analysis.

In this paper we compare CVCNNs for RD-map denoising and interference mitigation with comparable real-valued networks. We consider particularly small model architectures and present insights regarding parameter efficiency, computational efficiency and data efficiency.

The main contributions of this paper are:

• Application of CVCNNs for range-Doppler map denoising and interference mitigation using real-world measurements with simulated interference.

• Complexity evaluation in terms of model parameters and operations per sample.

• Data efficiency analysis of real- and complex-valued CNNs.

• Statistical comparison of CNNs using real- or complex-valued weights with ’state-of-the-art’ interference mitigation methods.

## II. SIGNAL MODEL

The range-Doppler (RD) processing chain of a common FMCW/CS radar is depicted in Fig. 2. The radar sensor transmits a set of linearly modulated radio frequency (RF) chirps, also termed ramps. Object reflections are perceived by the receive antennas and mixed with the transmit signal resulting in the Intermediate Frequency (IF) Signal. The objects’ distances and velocities are contained in the sinusoidals’ frequencies and their linear phase change over successive ramps [17], [18], respectively. The signal is processed as an $N \times M$ data matrix $s _ { \mathrm { I F } } [ n , m ]$ , containing N fast time samples for each of M ramps. Discrete Fourier transforms (DFTs) are computed over both dimensions, yielding a two-dimensional spectrum, the RD-map $S _ { \mathrm { R D } } [ n , m ]$ . The peaks on the RD-map then correspond to objects’ distances and velocities. After peak detection, further processing can include angular estimation, tracking, and classification.

The IF signal $s _ { \mathrm { I F } } [ n , m ]$ contains object reflections, noise, and may also include interference signals. It is modeled as

$$
s _ { \mathrm { I F } } [ n , m ] = \sum _ { o = 1 } ^ { N _ { \mathrm { O } } } s _ { \mathrm { O } , o } [ n , m ] + \sum _ { i = 1 } ^ { N _ { \mathrm { I } } } s _ { \mathrm { I } , i } [ n , m ] + \upsilon [ n , m ] ,\tag{1}
$$

where $s _ { \mathrm { O } , o } [ n , m ]$ are the $N _ { \mathrm { O } }$ object reflections, $s _ { \mathrm { I } , i } [ n , m ]$ are interference signals from $N _ { I }$ interfering radars and $v [ n , m ]$ models the noise.

State-of-the-art (’classical’) interference mitigation methods are mostly signal processing algorithms that are applied either on the time-domain signal $s _ { \mathrm { I F } } [ n , m ]$ or on the frequency-domain signal $S _ { \mathrm { R } } [ n , m ]$ after the first DFT [19]. The CNN-based method used in this paper, also termed Range-Doppler Denoising (RDD), is applied on the RD-map after the second DFT (see Fig. 2).

## III. COMPLEX-VALUED CONVOLUTIONAL NEURAL NETWORKS

Complex-valued neural networks are able to solve certain tasks more efficiently than real-valued neural networks [20]. Real-Valued CNNs (RVCNNs) that are applied to complex-valued data typically use separate real-valued channels in order to represent the real- and imaginary parts. In this approach, the CNN is required to learn the relation between the real- and imaginary part of the complexvalued data based on the training samples. In contrast, the CVCNN carries out all operations using complex-valued analysis and therefore incorporates the relation between real- and imaginary parts in the model architecture rather than the learned parameters. The motivation for this approach comes from the complex-valued nature of the radar signal itself. In theory, a CVCNN should be capable of processing complex radar spectra more easily than its real-valued alternative which has no intuition about complex numbers. Like local connectivity in convolution kernels, this introduces an inductive bias to the network architecture. Therefore, tasks which rely on correct phase relations, as radar signal processing, can greatly benefit from using complex operations within the CNN. For our proposed architecture we rely on three basic operations: convolutions, batch normalization and an appropriate activation function. All three operations have to be carried out following complex analysis.

## A. Complex convolution

A convolution kernel for a two-dimensional convolution operation consists of a four dimensional tensor $W _ { i j k l }$ of size $k _ { x } \times k _ { y } \times C _ { i n } \times$ $C _ { o u t }$ . Here $k _ { x }$ and $k _ { y }$ represent the spatial size of the kernel, whereas $C _ { i n }$ indicates the number of input filter channels and $C _ { o u t }$ the number of output filter channels. Considering the number of filter channels is a multiple of two, we can always split the channels into two parts, one for the real- and one for the imaginary part. Therefore, the separate kernels have size $\begin{array} { r } { k _ { x } \times k _ { y } \times \frac { C _ { i n } } { 2 } \times \frac { C _ { o u t } } { 2 } } \end{array}$ . In complex

![](images/dd6930fbee2426d8a88f864b5dffa2cc7044b471c5f459bee54457dedfe657b6.jpg)  
Fig. 3: Depiction of a complex convolution on input $\mathbf { a } ^ { l } \in \mathbb { C }$ using the kernel $W \in \mathbb { C } .$ , creating the activation of the next level $\mathbf { a } ^ { l + 1 } \in \mathbb { C } .$

analysis the multiplication of two complex numbers $z _ { 1 } = ( a + i b )$ and $z _ { 2 } = ( x + i y )$ results in $z _ { 1 } \cdot z _ { 2 } = a x - b y + i ( b x + a y )$ , where $z _ { 1 } , z _ { 2 } \in \mathbb { C }$ and $a , b \in \mathbb { R }$ with i being the imaginary unit. The same works for complex tensors. Since the convolution operator (∗) is distributive we obtain,

$$
\mathbf { W } * \mathbf { h } = ( \mathbf { A } + i \mathbf { B } ) * ( \mathbf { x } + i \mathbf { y } ) = \mathbf { A } * \mathbf { x } - \mathbf { B } * \mathbf { y } + i ( \mathbf { B } * \mathbf { x } + \mathbf { A } * \mathbf { y } ) ,\tag{2}
$$

![](images/79db1235bea69657ac3c255b40243ae6847e943cf142fad3a497ea596ababa2c.jpg)  
Fig. 4: CVCNN architecture for radar signal denoising and interference mitigation. It uses <sup>C</sup>ReLU, complex BN and the complex-convolution.

convolving the complex vector $\mathbf { h } = \mathbf { x } + i \mathbf { y }$ with the complex kernel matrix $\mathbf { W } = \mathbf { A } + i \mathbf { B } \left[ 1 4 \right]$ . Therefore, the complex-valued convolution can be executed as a series of real-valued convolutions, as shown in Fig. 3.

## B. Complex Batch Normalization

Deep CNNs rely on the Batch Normalization (BN) operation to normalize activations and accelerate training [21]. Since the standard formulation of BN only applies to real-valued activations, complexvalued networks require different methods. One possibility to realize BN for complex numbers was proposed in [14], where they use a whitening procedure to standardize the complex numbers. First the inputs $\mathbf { z } \in \mathbb { C }$ are whitened and then standard BN is performed. Thus, the vector after the whitening step is scaled and shifted using γ and $\beta$ respectively.

$$
\mathrm { B N } ( \mathbf { z } ) = \gamma \odot ( \mathbf { V } ) ^ { - \frac { 1 } { 2 } } ( \mathbf { z } - \mathbb { E } [ \mathbf { z } ] ) + \beta ,\tag{3}
$$

where V is $\textsuperscript { a 2 } \times 2$ positive (semi)-definite covariance matrix. Since the proposed BN needs the square root of the inverse of V, positive definiteness of the matrix is ensured by adding I to $V ,$ , which is known as Tikhonov regularization.

## C. Complex Rectified Linear Unit (<sup>C</sup>ReLU)

The complex-valued ReLU function is defined as

$$
\mathbb { C } \mathrm { R e L U } ( z ) = \mathrm { R e L U } ( \Re ( z ) ) + i \mathrm { R e L U } ( \Im ( z ) ) .\tag{4}
$$

Although it does not fulfil the Cauchy-Riemann equations everywhere and is therefore only holomorphic on a subset of $\bar { \mathbb { C } } ,$ but it can be computed efficiently and experiments have shown superior performance compared to other proposed complex-valued activation functions [14].

## IV. CVCNN FOR RANGE-DOPPLER PROCESSING

Our CVCNN takes RD-maps with interference as inputs and predicts denoised RD-maps as outputs.

## A. Model

The proposed CVCNN architecture for interference mitigation and denoising of radar signals is shown in Fig. 4 and based on the real-valued approach described in [22]. The CNN input is a noisy range-Doppler map, which is a complex-valued two dimensional matrix. This complex-valued matrix can be represented as a three dimensional tensor of size $C \times N \times M$ with N and M being the height and width of the RD-maps and $C = 2$ the real- and imaginary parts of the complex spectra. The model architecture implements a fully convolutional NN; it consists exclusively of convolutions, BN operations and the ReLU activation function. The convolution strides are set to one and ’same’ zero padding is used such that the individual feature maps maintain a constant spatial size between layers. The CVCNN carries out all operations according to complex analysis as described in Section III. Therefore, three layers are constructed as follows:

1) The first layer performs a complex-convolution followed by a <sup>C</sup>ReLU non-linearity.

2) In the second layer the complex-convolution is followed by a complex BN and a <sup>C</sup>ReLU non-linearity.

3) The last layer consists solely of the convolution operation to create the network output.

## B. Relation of computational and parameter complexity

Since CVCNNs have a higher computational complexity perparameter, we present the number of mega (=million) floating point operations per RD-map (MFLOP/RD-map) over the number of parameters in Fig. 5. Note, that we consider the computational complexity per RD-sample for one prediction step of the network. As expected, we see that there is a linear relationship between the number of used filter channels and the computational complexity for both real-valued and complex-valued models. However, the linear relation of the complex-valued models has a larger slope than for the real-valued models. This means that a complex-valued model using the same number of parameters has a higher computational complexity than its real-valued counterpart.

![](images/829335d2cd47c092d124b9e117f817f046da4ef7b45ddda1d9e3636ea7c13701.jpg)  
Fig. 5: Relation of the computational complexity and the number of model parameters. The labels of the networks indicate the number of filter channels in the corresponding layers.

## V. EXPERIMENTAL SETUP

We use real-world FMCW/CS radar measurements combined with simulated interference according to (1). The signals with and without interference are used as input-output pairs for training the CNN models in order to perform denoising and interference mitigation. The model is applied to the processed radar signal after the second DFT, i.e. the RD-map. We aim to correctly detect peaks in the RD-map that correspond to real objects rather than clutter or noise.

## A. Data set

The measurements were recorded in typical inner-city scenarios, where each measurement consists of 32 consecutive radar snapshots (RD-maps) each captured with sixteen antennas. The radar signal contains reflections from static and moving objects as well as receiver noise. The simulated interference, that is added to the time-domain measurement signal, is generated by sampling uniformly from the ego radar and interferer radar transmit parameters. See [22] for a detailed description of the simulation parameters and [8], [23] for an extensive analysis of the used measurement signals.

## B. Evaluation metrics

The models are evaluated using the F1-Score, Error Vector Magnitude (EVM) and Peak Phase Mean Squared Error (PPMSE), defined as follows:

1) F1-Score: The F1-Score is a combined classification measure including the true-positive $t _ { p } ,$ false-positive $f _ { p }$ and false-negative $f _ { n }$ object detections. It is defined as

$$
F _ { 1 } = 2 \cdot \frac { t _ { p } } { t _ { p } + \frac { 1 } { 2 } ( f _ { p } + f _ { n } ) } .\tag{5}
$$

For the F1-Score calculation, we first use the Cell Averaging - Constant False Alarm Rate (CA-CFAR) peak detector on the RD-map prediction $S _ { \mathrm { R D } } [ n , m ]$ in order to create a binary object detection map. This object detection map forms, in combination with the ground truth object detection map, the basis for calculating $t _ { p } , \ f _ { p }$ and $f _ { n } .$

2) Error Vector Magnitude $( E V M ) \ :$ The EVM measures the deviation of the predicted RD-map $S _ { \mathrm { R D } } [ n , m ]$ from the clean RD-map $S _ { \mathrm { R D , c l e a n } } [ n ,$ m] at ground truth peak locations. It it given as

$$
\mathrm { E V M } = \frac { 1 } { N _ { \mathrm { O } } } \sum _ { \{ n , m \} \in \mathcal { O } } \frac { | S _ { \mathrm { R D , c l e a n } } [ n , m ] - S _ { \mathrm { R D } } [ n , m ] | } { | S _ { \mathrm { R D , c l e a n } } [ n , m ] | } ,\tag{6}
$$

where n and m are the indices of the object, within the set of cells ${ \mathcal { O } } ,$ containing object peaks, and $N _ { \mathrm { O } }$ is the number of detected peaks.

3) Peak Phase Mean Squared Error (PPMSE): The PPMSE measures the average squared difference between the angle of the clean range-Doppler signal vector $S _ { \mathrm { R D , c l e a n } } [ n , m ]$ and the predicted range-Doppler signal vector S<sub>RD</sub>[n, m] of all detected object peaks. It is defined as

$$
\begin{array} { r l } & { \Delta [ n , m ] = \left| \mathrm { a t a n 2 } \left( \frac { \displaystyle \mathfrak { I } ( S _ { \mathrm { R D } } [ n , m ] ) } { \displaystyle \mathfrak { R } ( S _ { \mathrm { R D } } [ n , m ] ) } \right) - \mathrm { a t a n 2 } \left( \frac { \displaystyle \mathfrak { I } ( S _ { \mathrm { R D } , \mathrm { c l e a n } } [ n , m ] ) } { \displaystyle \mathfrak { R } ( S _ { \mathrm { R D } , \mathrm { c l e a n } } [ n , m ] ) } \right) \right| } \\ & { \mathrm { P P M S E } [ n , m ] = \frac { 1 } { \displaystyle N _ { 0 } } \sum _ { \{ n , m \} \in \mathcal { O } } \mathrm { m i n } ( \Delta [ n , m ] , 2 \pi - \Delta [ n , m ] ) ^ { 2 } , } \end{array}\tag{7}
$$

where n and m are the indices of cells containing object peaks $\scriptscriptstyle \mathcal { O }$ and $N _ { \mathrm { O } }$ is the number of detected peaks.

## C. Training settings

The interfered RD-maps $S _ { \mathrm { R D , i n t e r f e r e d } }$ are used as inputs for the CNN, while the clean RD-maps $S _ { \mathrm { R D , c l e a n } }$ are used as the training targets. All RD-maps are cropped to $N \times M = 9 6$ range cells × 96 Doppler cells and subsequently scaled to zero-mean and unitvariance. The models were trained for 100 epochs using Adam [24] with a learning rate of $5 \cdot 1 0 ^ { - 3 }$ and a mini-batch size of $L = 8 . \ \mathrm { A s }$ our training objective, we use the mean squared error (MSE) of real and imaginary parts of the predictions $S _ { \mathrm { R D } }$ and targets S<sub>RD,clean</sub>

## VI. EXPERIMENTS

We evaluate the denoising capabilities of CVCNNs for RD-maps with simulated interference. We compare complex-valued networks with their real-valued equivalent evaluating the computational, parameter and data efficiency. Furthermore, we analyze the performance of both CNN approaches against classical methods.

## A. Parameter efficiency

In this experiments we investigate the parameter efficiency of CVCNNs compared to their real-valued counterparts. Therefore, we train and evaluate 24 different architectures varying the number of filter channels C<sub>i</sub> per layer i. For the complex-valued network we vary the number of (complex-valued) filter kernels (= channels in the next activation map) in the first layer using $C _ { 1 } \in \{ 1 , 2 , 4 , 8 , 1 6 , 3 2 \}$ kernels and in the second layer using $C _ { 2 } \in \{ 2 , 4 , 8 , 1 6 \}$ kernels. The output layer is fixed to $C _ { 3 } = 1$ complex-valued filter kernel. The real-valued network uses $C _ { 1 } \in \{ 1 , 2 , 4 , 8 , 1 6 , 3 2 \} , C _ { 2 } \in \{ 4 , 8 , 1 6 , 3 2 \}$ and $C _ { 3 } =$ 2 real-valued filter kernels. We combine the sets of kernels per layer as a Cartesian product and thus evaluate all possible combinations, yielding 24 architectures for each approach.

![](images/1eb4eb1984f069640db7477335a1f986a73c66460f09ce1613328d2fdeb6e724.jpg)  
Fig. 6: Parameter efficiency of RVCNNs and CVCNNs. F1-Score and EVM over the number of parameters were used as performance metrics. The best real-valued and complex-valued models are annotated with their number of parameters.

The results in Fig. 6 show, that the complex-valued networks outperform the real-valued networks with respect to performance per parameter count. All metrics show substantial improvements across all architecture combinations. Complex-valued network architectures below 500 parameters can deliver comparable performance to even the largest used real-valued networks, reducing the overall memory footprint of the network.

## B. Computational efficiency

Parameter efficiency does not directly translate to computational efficiency, since complex-valued operations are slightly more computationally demanding than real-valued operations as discussed in Section IV-B. Therefore, the same architectures as above were used in order to evaluate the performance of the models w.r.t their computational efficiency in MFLOP/RD-map. Note, that we consider the computational complexity per RD-sample for one prediction step of the network. Comparing the results of the complex-valued network

![](images/2e7478dbec7ca76af290c2ab7a5ecd7a923b7620544ec133f88a82510af15763.jpg)  
Fig. 7: Computational efficiency in MFLOP/RD-map of RVCNNs and CVCNNs. F1-Score and EVM over MFLOP/RD-map were used as performance metrics. The best real-valued and complex-valued models are annotated with the used MFLOPS/RD-map.

in Fig. 7 with Fig. 6, we see that the improvement in performance compared to the real-valued networks is not as pronounced as in the last experiment. This means that while being very parameter efficient, the complex-valued models introduce a lot of computational overhead. Therefore, the performance improvement on a per FLOP level is smaller than for the case of only considering parameter count. Nevertheless, the complex-valued models are able to outperform their real-valued counterparts for most architectures.

## C. Data efficiency

In this experiments we vary the used training data with a step size of one percent. The total number of training samples (=RD-maps) is 2500, which gives a minimum number and step size of 25 training samples. We compare a three layer real-valued network containing 16- 8-2 channels (<sup>R</sup> 16-8-2) with two variants of complex-valued networks (<sup>C</sup> 8-8-1 and <sup>C</sup> 8-4-1). The two complex-valued network variants are selected, such that they have a similar number of real-valued parameters (i.e. <sup>C</sup> 8-8-1) and a similar computational complexity (i.e. <sup>C</sup> 8-4-1) when compared to the real-valued baseline. See Section IV-B and in particular Fig. 5 for details about the parameter-to-FLOP/RD map relation of real-valued and complex-valued networks. The figure indicates the closest complex-valued architectures with respect to both considered complexity measures, i.e. parameters and FLOP/RD-map.

![](images/d4eb7a57d377dbbd9efaed752891614618bd556efb5ad47c7a52ceda4fcc3852.jpg)  
Fig. 8: Data efficiency of a real-valued (<sup>R</sup> 16-8-2) and a complexvalued network (<sup>C</sup> 8-4-1) with similar computational complexity. The F1-Score and EVM have been evaluated using different percentages (1% to 100%) of the training data.

TABLE I contains the F1-Score, EVM and PPMSE results for the two chosen network architectures (<sup>C</sup> 8-4-1 and <sup>C</sup> 8-8-1 complex channels) and the real-valued baseline model (<sup>R</sup> 16-8-2) for different fractions of used training data. Both complex-valued network architectures clearly outperform the real-valued equivalent, while the bigger complex-valued model <sup>C</sup> 8-8-1 typically yields the best performance scores. Fig. 8 illustrates the data efficiency analysis of the smaller CVCNN architecture (<sup>C</sup> 8-4-1) and the real-valued baseline.

In general, the more training data we use, the better is the test performance for all three metrics (F1-Score, EVM and PPMSE). However, complex-valued networks require much less training samples in order to yield high performances. While a complex-valued network reaches almost top results with only 10% of the training samples, a comparable real-valued network requires at least 50% of the training samples in order to train robustly and reach high performances. The performance difference is particularly high for metrics that consider phase information (EVM and PPMSE). This emphasizes the need for an accurate treatment of complex input domains in order to correctly infer complex information.

## D. Comparison with classical signal processing methods

We compare our best CNN-based models in the real-valued setting (<sup>R</sup>-model) as well as in the complex-valued setting (<sup>C</sup>-model) with the classical and state-of-the-art interference mitigation methods zeroing [1], Iterative method with adaptive thresholding (IMAT) [25] and Ramp filtering [2]; see [26] for an overview of these methods. Zeroing and IMAT highly depend on an interference detection step, which influences their performance considerably. In our experiments we identified time-domain samples incorporating interference with approximately 90% accuracy; this interference detection rate seems feasible in practice. Note that Ramp filtering as well as the CNNbased models do not depend on such an explicit interference detection step. The average results for all methods are given in TABLE II. Fig. 9 shows the empirical cumulative density function (CDF) using the per-sample F1-Score and the EVM at peak locations. The ’clean’ measurement and interfered signals are included as reference. All classical methods, namely zeroing, IMAT and Ramp filtering, improve the F1-Score (as shown in Fig. 9(a)) when applied to the measurement signal with interference. Zeroing and IMAT yield very similar F1-Scores. Ramp filtering outperforms both other classical methods, particularly for samples with strong interference (see black magnification).

<table><tr><td rowspan=1 colspan=1>Metric</td><td rowspan=1 colspan=1>Model</td><td rowspan=1 colspan=5>Used data</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>20 %</td><td rowspan=1 colspan=1>40 %</td><td rowspan=1 colspan=1>60 %</td><td rowspan=1 colspan=1>80 %</td><td rowspan=1 colspan=1>100 %</td></tr><tr><td rowspan=3 colspan=1>F1-Score</td><td rowspan=1 colspan=1>C 8-8-1</td><td rowspan=1 colspan=1>0.895</td><td rowspan=1 colspan=1>0.898</td><td rowspan=1 colspan=1>0.896</td><td rowspan=1 colspan=1>0.898</td><td rowspan=1 colspan=1>0.897</td></tr><tr><td rowspan=1 colspan=1>C 8-4-1</td><td rowspan=1 colspan=1>0.897</td><td rowspan=1 colspan=1>0.896</td><td rowspan=1 colspan=1>0.897</td><td rowspan=1 colspan=1>0.896</td><td rowspan=1 colspan=1>0.897</td></tr><tr><td rowspan=1 colspan=1>R 16-8-2</td><td rowspan=1 colspan=1>0.872</td><td rowspan=1 colspan=1>0.881</td><td rowspan=1 colspan=1>0.887</td><td rowspan=1 colspan=1>0.891</td><td rowspan=1 colspan=1>0.885</td></tr><tr><td rowspan=3 colspan=1>EVM</td><td rowspan=1 colspan=1>C 8-8-1</td><td rowspan=1 colspan=1>0.163</td><td rowspan=1 colspan=1>0.136</td><td rowspan=1 colspan=1>0.124</td><td rowspan=1 colspan=1>0.117</td><td rowspan=1 colspan=1>0.115</td></tr><tr><td rowspan=1 colspan=1>C 8-4-1</td><td rowspan=1 colspan=1>0.163</td><td rowspan=1 colspan=1>0.143</td><td rowspan=1 colspan=1>0.133</td><td rowspan=1 colspan=1>0.127</td><td rowspan=1 colspan=1>0.122</td></tr><tr><td rowspan=1 colspan=1>R 16-8-2</td><td rowspan=1 colspan=1>0.258</td><td rowspan=1 colspan=1>0.262</td><td rowspan=1 colspan=1>0.209</td><td rowspan=1 colspan=1>0.184</td><td rowspan=1 colspan=1>0.146</td></tr><tr><td rowspan=3 colspan=1>PPMSE/ rad²</td><td rowspan=1 colspan=1>C 8-8-1</td><td rowspan=1 colspan=1>0.017</td><td rowspan=1 colspan=1>0.014</td><td rowspan=1 colspan=1>0.013</td><td rowspan=1 colspan=1>0.013</td><td rowspan=1 colspan=1>0.013</td></tr><tr><td rowspan=1 colspan=1>C 8-4-1</td><td rowspan=1 colspan=1>0.018</td><td rowspan=1 colspan=1>0.016</td><td rowspan=1 colspan=1>0.015</td><td rowspan=1 colspan=1>0.014</td><td rowspan=1 colspan=1>0.014</td></tr><tr><td rowspan=1 colspan=1>R 16-8-2</td><td rowspan=1 colspan=1>0.049</td><td rowspan=1 colspan=1>0.054</td><td rowspan=1 colspan=1>0.035</td><td rowspan=1 colspan=1>0.022</td><td rowspan=1 colspan=1>0.018</td></tr></table>

TABLE I: F1-Score, EVM and PPMSE results for different fractions of used training data. The RVCNN (<sup>R</sup> 16-8-2 channels) is compared to two CVCNNs (<sup>C</sup> 8-8-1 and <sup>C</sup> 8-4-1). The F1-Score without mitigation and from the target measurements is $\mathrm { F _ { N o M i t . } = 0 . 8 3 7 }$ and $\mathrm { F _ { T a r g e t } = }$ 0.909, respectively.

The CNN-based models, both with real-valued as well as complexvalued weights and activations, are competitive with the classical methods for all considered interference levels and even outperform the best classical method, namely Ramp filtering (see black magnification). The CDF shape indicates that the CNN-based models are robust with respect to different interference patterns and levels. This is indicated by the CDF’s narrow form and high values for the lowest F1-Scores per CNN model (see gray magnification). Note, that the F1-Score, and thus the detection sensitivity, of both CNN-based models is very close to the theoretical maximum, namely the CDF of the clean data.

Fig. 9(b) shows the empirical CDF of the EVM. Generally, the better the mitigation in terms of F1-Score, the higher is the EVM and thus the distortion of the phase at object peaks. In comparison to the RVCNN, the CVCNN reduces the peak distortions although it achieves a very similar F1-Score and it even outperforms the best classical method in terms of EVM, namely IMAT. Hence, the CVCNN achieves very high F1-Scores while also retaining low EVMs. The PPMSE in Fig. 9(c) shows similar characteristics. The CVCNN outperforms all other methods incorporating less phase distortions, particularly for weak interferences.

## VII. CONCLUSION

We propose the use of complex-valued CNNs for range-Doppler denoising and interference mitigation of automotive radar signals. The proposed NN architecture follows complex-valued analysis and thus processes the complex-valued signals according to their physical characteristics. This inductive bias restricts the network structure and operations in a meaningful way and therefore reduces the complexity of the learning problem. We confirm this claim with experiments on complex-valued radar signals. We show, that complex-valued networks

![](images/4967d90a90cb09e92aab73ae6baa14736f648c50041e9d0207a6565449a639f7.jpg)  
(a) CDF of the samplewise F1-Score

![](images/708046da173294af29e28314a12ad01e06a707929265706cfceb0b5c2c250e87.jpg)  
(b) CDF of the samplewise EVM

![](images/d4dc3d3d6ef15249cd569250420d4c2fb5d753706e72a6c88e2b5fab05460862.jpg)  
(c) CDF of the samplewise PPMSE in rad<sup>2</sup>

<sup>P</sup>Fig. 9: Empirical CDF performance comparison between the real-valued model<sup>\*</sup> (<sup>R</sup>-model), the complex-valued model<sup>\*</sup> (<sup>C</sup>-model), and the P <sup>P</sup>three classical methods zeroing, IMAT and Ramp filtering. \*Model selected based on the best EVM result in the design space.
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>F1-Score</td><td rowspan=1 colspan=1>EVM</td><td rowspan=1 colspan=1>PPMSE</td><td rowspan=1 colspan=1>Params</td><td rowspan=1 colspan=1>MFLOP</td></tr><tr><td rowspan=1 colspan=1>R-16-16-2*</td><td rowspan=1 colspan=1>0.896</td><td rowspan=1 colspan=1>0.123</td><td rowspan=1 colspan=1>0.015</td><td rowspan=1 colspan=1>2946</td><td rowspan=1 colspan=1>53.24</td></tr><tr><td rowspan=1 colspan=1>C-32-16-1*</td><td rowspan=1 colspan=1>0.902</td><td rowspan=1 colspan=1>0.098</td><td rowspan=1 colspan=1>0.011</td><td rowspan=1 colspan=1>10242</td><td rowspan=1 colspan=1>374.27</td></tr><tr><td rowspan=1 colspan=1>Zeroing</td><td rowspan=1 colspan=1>0.856</td><td rowspan=1 colspan=1>0.124</td><td rowspan=1 colspan=1>0.069</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2.83</td></tr><tr><td rowspan=1 colspan=1>RFmin</td><td rowspan=1 colspan=1>0.875</td><td rowspan=1 colspan=1>0.145</td><td rowspan=1 colspan=1>0.054</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>3.13</td></tr><tr><td rowspan=1 colspan=1>IMAT</td><td rowspan=1 colspan=1>0.860</td><td rowspan=1 colspan=1>0.119</td><td rowspan=1 colspan=1>0.065</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>3.88</td></tr></table>

TABLE II: Performance comparison of real- and complex-valued models<sup>\*</sup> with the three classical methods zeroing, IMAT and Ramp filtering in terms of F1-Score, EVM and PPMSE. The F1-Score without mitigation and from the target measurements is F<sub>NoMit.</sub> = 0.837 and $\mathrm { F _ { T a r g e t } } = 0 . 9 0 9$ , respectively. \*Model selected based on the best EVM result in the design space.

with a similar (1) number of parameters and (2) computational complexity substantially improve all considered metrics (F1-Score, EVM and PPMSE) and that they are able to operate on much smaller training sets. Particularly the high performance of metrics considering the phase information (EVM and PPMSE) reveals the advantage of complex-valued NNs for applications on complex-valued signal domains. The proposed approach might thus be crucial for processing complex-valued signals, such as automotive radar signals containing valuable phase information, e.g. for angle estimation. In future research we want to focus on the transferability of models between different radar antennas, the impact of multi-antenna information during training and the direct evaluation of angle estimation capabilities.

## REFERENCES

[1] C. Fischer, Untersuchungen zum Interferenzverhalten automobiler Radarsensorik. PhD thesis, Ulm University, 2016.

[2] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-Free Interference Cancellation Method for Automotive FMCW Radar Systems,” in 2018 IEEE Int. Symposium on Circuits and Systems (ISCAS), 2018.

[3] F. Marvasti, M. Azghani, P. Imani, P. Pakrouh, S. Heydari, A. Golmohammadi, A. Kazerouni, and M. Khalili, “Sparse signal processing using iterative method with adaptive thresholding (IMAT),” in 2012 19th Int. Conf. on Telecommunications (ICT), 2012.

[4] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in 2017 18th Int. Radar Symposium (IRS), pp. 1–10, 2017.

[5] J. Bechter, K. Eid, F. Roos, and C. Waldschmidt, “Digital beamforming to mitigate automotive radar interference,” 2016 IEEE MTT-S Int. Conf. Microwaves Intell. Mobility, ICMIM 2016, pp. 2–5, 2016.

[6] J. Mun, H. Kim, and J. Lee, “A deep learning approach for automotive radar interference mitigation,” in 2018 IEEE 88th Vehicular Technology Conf. (VTC-Fall), pp. 1–5, 2018.

[7] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in ICASSP 2020 - 2020 IEEE Int. Conf. on Acoustics, Speech and Signal Processing (ICASSP), pp. 3802–3806, 2020.

[8] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference 0<sub>mitigation</sub> <sub>and</sub> <sub>denoising</sub> <sub>of</sub> <sub>real-world</sub> <sub>fmcw</sub> <sub>radar</sub> <sub>signals,”</sub> <sub>in</sub> <sub>2020</sub> IEEE Int. Radar Conf. (RADAR), pp. 624–629, 2020.

[9] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, 2021. Accepted for publication.

[10] M. L. L. de Oliveira and M. J. G. Bekooij, “Deep convolutional autoencoder applied for noise reduction in range-doppler maps of fmcw radars,” in 2020 IEEE Int. Radar Conf. (RADAR), pp. 630–635, 2020.

[11] J. Fuchs, A. Dubey, M. Lübke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE Int. Radar Conf. (RADAR), pp. 315–320, 2020.

[12] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully Convolutional Neural Networks for Automotive Radar Interference Mitigation,” 7 2020.

[13] G. M. Georgiou and C. Koutsougeras, “Complex domain backpropaga tion,” IEEE transactions on Circuits and systems II: analog and digital signal processing, vol. 39, no. 5, pp. 330–334, 1992.

[14] C. Trabelsi, O. Bilaniuk, D. Serdyuk, S. Subramanian, J. F. Santos, S. Mehri, N. Rostamzadeh, Y. Bengio, and C. J. Pal, “Deep complex networks,” CoRR, vol. abs/1705.09792, 2017.

[15] Z. Zhang, H. Wang, F. Xu, and Y. Jin, “Complex-valued convolutional neural network and its application in polarimetric sar image classification,” IEEE Transactions on Geoscience and Remote Sensing, vol. 55, no. 12, pp. 7177–7188, 2017.

[16] J. Gao, B. Deng, Y. Qin, H. Wang, and X. Li, “Enhanced radar imaging using a complex-valued convolutional neural network,” IEEE Geoscience and Remote Sensing Letters, vol. 16, no. 1, pp. 35–39, 2019.

[17] A. G. Stove, “Linear FMCW radar techniques,” IEE Proceedings F - Radar and Signal Processing, vol. 139, no. 5, pp. 343–350, 1992.

[18] V. Winkler, “Range Doppler detection for automotive FMCW radars,” in 2007 European Microwave Conf., pp. 1445–1448, Oct. 2007.

[19] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical Investigation of Non-Coherent Mutual FMCW Radar Interference,” in 2018 European Radar Conf. (EURAD), pp. 71–74, 2018.

[20] A. Hirose, Complex-valued neural networks, vol. 400. Springer Science & Business Media, 2012.

[21] S. Ioffe and C. Szegedy, “Batch normalization: Accelerating deep network training by reducing internal covariate shift,” CoRR, vol. abs/1502.03167, 2015.

[22] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in 2019 22nd Int. Conf. on Information Fusion (FUSION) (FUSION 2019), 2019.

[23] M. Toth, J. Rock, P. Meissner, A. Melzer, and K. Witrisal, “Analysis of automotive radar interference mitigation for real-world environments,” in European Radar Conf. (EURAD), 2020. Accepted for publication.

[24] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” CoRR, vol. abs/1412.6980, 2014.

[25] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive Radar Interference Mitigation Using a Sparse Sampling Approach,” in 2017 European Radar Conf. (EURAD), pp. 90–93, 2017.

[26] S.-W. Fu, T.-y. Hu, Y. Tsao, and X. Lu, “Complex spectrogram enhancement by convolutional neural network with multi-metrics learning,” in 2017 IEEE 27th Int. Workshop on Machine Learning for Signal Processing (MLSP), pp. 1–6, IEEE, 2017.