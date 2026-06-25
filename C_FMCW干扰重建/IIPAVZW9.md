# Resource-efficient Deep Neural Networks for Automotive Radar Interference Mitigation

Johanna Rock, Wolfgang Roth, Mate Toth, Paul Meissner, and Franz Pernkopf

![](images/7d5cc2072c7a9c0f04171a9e176292dd475931b0447992d1706e943542b841d3.jpg)  
Figure 1: Interference mitigation of radar signals using a quantized CNN to remove interference patterns, retain object signals, and provide a high detection sensitivity. To use this approach in practice, a resource-efficient model is essential.

Abstract—Radar sensors are crucial for environment perception of driver assistance systems as well as autonomous vehicles. With a rising number of radar sensors and the so far unregulated automotive radar frequency band, mutual interference is inevitable and must be dealt with. Algorithms and models operating on radar data are required to run the early processing steps on specialized radar sensor hardware. This specialized hardware typically has strict resource-constraints, i.e. a low memory capacity and low computational power. Convolutional Neural Network (CNN)-based approaches for denoising and interference mitigation yield promising results for radar processing in terms of performance. Regarding resource-constraints, however, CNNs typically exceed the hardware’s capacities by far.

In this paper we investigate quantization techniques for CNNbased denoising and interference mitigation of radar signals. We analyze the quantization of (i) weights and (ii) activations of different CNN-based model architectures. This quantization results in reduced memory requirements for model storage and during inference. We compare models with fixed and learned bit-widths and contrast two different methodologies for training quantized CNNs, i.e. the straight-through gradient estimator and training distributions over discrete weights. We illustrate the importance of structurally small real-valued base models for quantization and show that learned bit-widths yield the smallest models. We achieve a memory reduction of around 80% compared to the real-valued baseline. Due to practical reasons, however, we recommend the use of 8 bits for weights and activations, which results in models that require only 0.2 megabytes of memory.

Index Terms—Quantization aware training, resource-efficiency, binarized convolutional neural networks, straight-through estimator, discrete weight distributions, uncertainty maps, interference mitigation, automotive radar.

## I. INTRODUCTION

Mate Toth and Paul Meissner are with Infineon Technologies Austria AG, Graz, e-mail: {mate.toth, paul.meissner}@infineon.com.

DVANCED Driver Assistance Systems (ADAS) and Auheterogeneous sensors for environment perception. Among them are radar sensors that are used for object detection, classification and to directly measure relative object velocities. Advantages of radar sensors are a high range resolution and their robustness concerning difficult weather and lighting conditions.

Typically frequency modulated continuous wave (FMCW)/chirp sequence (CS) radars are used in the automotive context. They transmit sequences of linearly modulated radio frequency (RF) chirps in a shared and non-regulated band. This may lead to mutual interference of multiple radar sensors; it becomes increasingly likely with a higher number of deployed radar-enhanced vehicles and larger chirp bandwidths of individual sensors used for better range-resolution.

For a non-regulated spectrum, the most common form of mutual interference is non-coherent, where the transmitters send with non-identical parameters. This results in burstlike interferences in time domain and a decreased detection sensitivity in the range-Doppler (RD) map [1], [2]. Thus, the detection and mitigation of interference is crucial in a safety context and must be addressed.

Several conventional signal processing algorithms for interference mitigation of mutual interference have been proposed. The most simplistic method is to substitute all interferenceaffected samples with zero [3], followed by an optional smoothing of the boundaries. More advanced methods use nonlinear filtering in slow-time [4], iterative reconstruction using Fourier transforms and thresholding [5], estimation and subtraction of the interference component [6], an adaptive noise canceller [7], or beamforming [8].

Recently, the use of deep learning has emerged for radar spectra denoising and interference mitigation. For this task deep neural networks (DNNs) are applied in time domain or in frequency domain, typically in a supervised manner. For interference mitigation in time domain, recurrent neural networks (RNNs) are used in [9], [10]. For interference mitigation in frequency domain, CNN-based models [11], [12], Convolutional Autoencoders [13] and U-Net inspired CNNs [14] are used.

While the results are impressive on simulated and real-world measurement data, the problem of high memory and computational requirements of DNN models has not been addressed in sufficient detail so far. In order to use the aforementioned methods for interference mitigation in practice, they have to comply with memory, computational as well as real-time constraints of specialized hardware, i.e. the radar sensor.

![](images/10f7f1854559452ac3a378e4885ec8cd289e7501c49481db954f0d69f8881a98.jpg)  
Figure 2: Block diagram of a basic FMCW/CS radar processing chain. Dashed boxes indicate the locations of optiona interference mitigation steps, including CNN-based approaches (red) and classical methods (blue).

Typically, DNNs have thousands or even millions of parameters and require hundreds of megabytes memory to be stored and during computation. Note that memory is often the limiting factor also in terms of energy efficiency and execution time, because loading data dominates over arithmetic operations and loading from off-chip DRAM is magnitudes more costly than accessing data from on-chip SRAM [15]. Thus, memory efficiency is particularly important for specialized embedded hardware such as radar sensors.

There are several, partly orthogonal, options to reduce memory and computational requirements. The initial network architecture contributes substantially to the resource requirements, thus a small model with few parameters and a small number of activations is preferable. Neural architecture search (NAS) can be applied with resource-oriented objectives in order to find efficient models automatically [16]. Other approaches are network pruning techniques, weight sharing, knowledge distillation, special matrix structures and quantization [17]. In a quantized DNN, weights and activations are discretized and thus their bit-width is reduced. Typically, research on DNN quantization considers standard image classification data sets (e.g. MNIST, CIFAR-10 or ImageNet) rather than real-world data or regression tasks.

The aim of this paper (visually depicted in Figure 1) is to build upon the approach from [11], and find small models with decent resource requirements that retain high interference mitigation performance. We compare two quantization techniques for CNN-based models from [11] to reduce the total memory requirements on radar sensors. The first technique, known as quantization aware training, is based on the straight-through gradient estimator (STE) [18]. The second technique is based on training distributions over discrete weights [19].

In our experiments we use real-world FMCW/CS radar measurements with simulated interference. The main contributions of this paper are:

• We analyze the quantization capabilities according to different model architectures, sizes and quantization strategies, i.e. quantized weights, activations or both.

• We illustrate the importance of resource-efficient realvalued initial models w.r.t. quantization and the resulting memory requirements.

• We present results for quantizing exceptionally small models without significant performance degradation using fixed and learned bit-widths.

• We demonstrate how distributions over discrete weights can be used, in addition to denoising and interference mitigation, to obtain uncertainty estimates of the RD maps.

![](images/9c939562a7d04bd53494d39b8da13cc1120c7048a244c277cdf72951a6670689.jpg)  
Figure 3: Non-coherent mutual FMCW/CS radar interference on the time-frequency plane. The ego radar $f _ { \mathrm { E } } ( t )$ and interferer $f _ { \mathrm { I } } ( t )$ frequency courses are depicted in blue and red, respectively. When both ramps cross, a time limited interference burst appears in the IF signal (yellow).

![](images/46f19009a74db54b990a73ea8a1e54092391ae3a1d129e07de5fd1468cf2b885.jpg)  
Figure 4: Single, simulated and ideal interference burst in timedomain.

## II. SIGNAL MODEL

The RD processing chain of a common FMCW/CS radar is depicted in Figure 2. The radar sensor transmits a set of linearly modulated RF chirps, also termed ramps. Object reflections are perceived by the receive antennas and mixed with the transmit signal resulting in the Intermediate Frequency (IF) Signal. The objects’ distances and velocities are contained in the sinusoidals’ frequencies and their linear phase change over successive ramps [20], [21], respectively. The signal is processed as a $N \times M$ data matrix $s _ { \mathrm { I F } } [ n , m ]$ , containing N fast time samples for each of M ramps. Discrete Fourier transforms (DFTs) are computed over both dimensions, yielding a twodimensional spectrum, the RD map $S _ { \mathrm { R D } } [ n , m ]$ , on which peaks can be found at positions corresponding to the objects distances and velocities. After peak detection, further processing can include angular estimation, tracking, and classification.

The IF signal $s _ { \mathrm { I F } } [ n , m ]$ contains object reflections, noise, and may also include interference signals. It is modeled as

$$
s _ { \mathrm { I F } } [ n , m ] = \sum _ { o = 1 } ^ { N _ { \mathrm { O } } } s _ { \mathrm { O } , o } [ n , m ] + \sum _ { i = 1 } ^ { N _ { \mathrm { I } } } s _ { \mathrm { I } , i } [ n , m ] + v [ n , m ] ,\tag{1}
$$

where $s _ { \mathrm { O } , o } [ n , m ]$ are object reflections from $N _ { \mathrm { O } }$ objects, $s _ { \mathrm { I } , i } [ n , m ]$ are interference signals from $N _ { I }$ interfering radars and $v [ n , m ]$ models the noise.

The interference principle is illustrated in Figure 3 on the time-frequency plane for two FMCW/CS radars. Depending on the RF transmit parameters of interferer and interfered (i.e. ego) radar, as well as the relative timing of the ramp sequences $\tau _ { \mathrm { I } } ^ { \mathrm { { R F } } }$ , interference bursts appear in the IF signal where the two ramp sequences cross. The characteristic ’chirp burst’ form of the IF interference is due to the mixing and filtering process at the receiver. In discrete-time, after sampling with a frequency of $\frac { 1 } { \mathrm { T } _ { \mathrm { s } } }$ , the resulting K bursts caused by a single interferer can be parametrically modeled as

$$
s _ { \mathrm { I } , 1 } [ n , m ] = \sum _ { k = 1 } ^ { K } h [ n ] * A _ { k } \cos { ( - 2 \pi \frac { \tau _ { k } } { 2 T _ { k } } n + \pi \frac { \mathrm { T } _ { \mathrm { s } } } { 2 T _ { k } } n ^ { 2 } + \varphi _ { k } ) } \mathbb { 1 } _ { k } [ m ] ,\tag{2}
$$

where $h [ n ]$ is the combined impulse response of the radio channel and all filters in the receiver, such as a low-pass filter for anti-aliasing. $A _ { k } , \tau _ { k } , T _ { k }$ and $\varphi _ { k }$ are the amplitude, time delay, half-duration and initial phase of the k-th chirp burst, respectively. The indicator function $\mathbb { 1 } _ { k } [ m ]$ has a value of 1 for $m = m _ { k }$ being the slow-time index of the k-th burst, and 0 else. More details on the chirp burst model can be found in [1]; equivalent models and how they are related to RF transmit parameters are discussed in [2]–[4], [6]. One such burst is illustrated in Figure 4, where an ideal $h [ n ] = \delta [ n ]$ is assumed with δ[n] being a Kronecker delta.

Classical interference mitigation methods are mostly signal processing algorithms that are applied either on the time domain signal s<sub>IF</sub>[n, m] or on the frequency domain signal $S _ { \mathrm { R } } [ n , m ]$ after the first DFT [1]. The CNN-based method used in this paper, also termed Range-Doppler Denoising (RDD), is applied on the RD map after the second DFT.

## III. CNN MODEL

The CNN model architecture is illustrated in Figure 5 [11]. The network contains L layers, each being a composite function of operations including the convolution operation (Conv), ReLU activation function [22] and Batch Normalization (BN). The last layer uses a linear activation function and two convolution channels<sup>1</sup> corresponding to the real and imaginary values of the complex-valued network output. From a signal processing perspective, the CNN model filters the RD map using learnable filter kernels.

The model is applied to radar snapshots for one antenna after the second DFT (RD maps), hence the input samples are complex valued patches of size $N \times M$ . We use two input channels in order to represent the real and imaginary parts of the complex valued input. The network inputs are RD maps with interference and their targets are the corresponding ’clean’ RD maps without interference. For the convolution, we employ square kernels and zero-padding, such that the inputs and outputs for each layer have the same spatial dimension. For training the network we use the mean squared error (MSE) loss function and the Adam algorithm [23]. In this paper, we report results for two different variants of the CNN model:

Architecture A consists of the same number of channels in every layer, except for the output layer which has a fixed number of two channels. Hence, a model denoted as $\mathrm { L } 3 \_ \mathrm { C } 3 2 \_ \mathrm { A }$ has three layers with $\mathrm { C } = [ 3 2 , 3 2 , 2 ]$ channels. See Figure 5(b).

Architecture B has a bottleneck-based structure of channels where the number of channels is halved for each layer and the last layer always consists of two channels. A model denoted as L3 C32 B has three layers with ${ \bf C } = [ 3 2 , 1 6 ,$ 2] channels. See Figure 5(c).

## IV. QUANTIZATION

The training of real-valued DNNs is typically performed using gradient-based algorithms that update the network weights according to some loss function. However, quantizers and piecewise constant activation functions are non-differentiable components, whose gradient is zero almost everywhere, such that conventional gradient-based optimization is not possible. Besides quantization of pre-trained real-valued DNNs as a post-processing step, quantization can also be incorporated in the training process by:

1) Quantization aware training using real-valued auxiliary weights and the straight-through gradient estimator (STE) during the backward pass of quantization functions [18].

2) Inspired by methods from Bayesian inference, we can train weight distributions over discrete weights. The most probable weights of the optimized weight distributions can be selected as discrete-valued, i.e. quantized, DNN [19], [24].

In this paper, we consider approaches 1) and 2) for trained quantization. We denote $\mathbb { D } ^ { D } \ = \ \{ 0 , \pm w _ { 1 } , \ldots , \pm w _ { \lfloor D / 2 \rfloor } \}$ to be a set of symmetric discrete weights with $0 ~ < ~ w _ { 1 } <$ $\dots < w _ { \lfloor D / 2 \rfloor }$ and a uniform step size $\delta _ { w } = w _ { d + 1 } - w _ { d } .$ The quantizer Q maps a real-valued number $x \in \mathbb { R }$ to one of the $D = 2 ^ { k } - 1$ quantized weights $w _ { q } \in \mathbb { D } ^ { D }$ , assuming $k \geq 2$ bits are used to encode the weights $w _ { q }$ . The quantizer Q, and thus the set of discrete weights $\mathbf { \bar { \mathbb { D } } } ^ { D }$ , are defined through three parameters: the bit-width $k \in \mathbb N$ , the step size $\delta _ { w } \in \mathbb { R }$ and the dynamic range $\alpha \in \mathbb { R }$ . These parameters depend on each other according to $\alpha = ( 2 ^ { k - 1 } - 1 ) \delta _ { w }$ . Note that this implies $\alpha = w _ { \lfloor D / 2 \rfloor }$ . For binary quantization with $k \ = \ 1$ bit, we consider $\mathbb { D } ^ { 2 } = \{ - w _ { 1 } , + w _ { 1 } \}$

## A. Straight-through gradient estimator (STE)

The gradients required for gradient-based learning are typically computed using the backpropagation algorithm in a computation graph that specifies a loss function . After evaluating the loss , backpropagation computes the gradients by repeated application of the chain rule. It is important that all components involved during backpropagation exhibit non-zero derivatives, preventing the use of many interesting components such as piecewise constant quantizers.

The STE is a simple method to approximate the zero gradient of such components by a non-zero value. More specifically, let $f ( w )$ be some function within the computation graph with $d f / d w = 0$ . The STE approximates the gradient df /dw during backpropagation by the non-zero derivative of a different function $\tilde { f } ( w )$ with similar functional shape as $f ( w )$ i.e.,

![](images/0e81b97c15e2d5055808c27e1baf26221f1288115a3fd522273f6f0f79444dd6.jpg)  
(a) CNN architecture

![](images/fa3a499a076a6cc5c7d9d69bb10881328fa0613eedaebe1fd98bda4982d60008.jpg)  
(b) Architecture A: same number of channels C in all layers

![](images/984b6f18de14bf5d777ac0e96c9d2ad63031799a904d964f7192bd62b5a8d482.jpg)  
(c) Architecture B: bottle-neck based architecture of channels, i.e. the number of channels C is halved for each layer  
Figure 5: CNN architecture for radar signal denoising and interference mitigation. It uses ReLU, Batch Normalization (BN) and the convolution operation Conv $( i , o , ( s _ { 1 } \times s _ { 2 } ) )$ , for i input channels, o output channels, and a kernel size of $s _ { 1 } \times s _ { 2 }$ . Figure (a) illustrates the general model architecture, while Figures (b) and (c) show concrete model variants with $L = 3$ layers that are used in this paper.

$$
\frac { \partial \mathcal { L } } { \partial w } = \frac { \partial \mathcal { L } } { \partial f } \frac { \partial f } { \partial w } \approx \frac { \partial \mathcal { L } } { \partial f } \frac { \partial \tilde { f } } { \partial w } .\tag{3}
$$

Note that for the commonly used identity function $\tilde { f } ( w ) = w$ the gradient is simply passed ’straight-through’ to higher components in the computation graph. Figure 6 illustrates the computation graph of the STE on a simplified convolutional layer with sign activation function. In the forward pass, the piecewise constant quantization and activation functions are applied, while their zero gradients are avoided during the backward pass. The gradient updates are then applied to the real-valued auxiliary weights.

## B. Quantization aware training using the STE

Quantization aware training [18] uses auxiliary real-valued weights and the STE to approximate the gradient of zerogradient DNN components during the backward pass. Piecewise constant quantization functions are used to discretize real-valued weights or activations. While some quantization functions (e.g. sign) map to a fixed finite set of values and therefore result in a specific bit-width of discretized values, other quantization functions (e.g. rounding) can be applied with a variable bit-width $k \geq 2$ . Let $\alpha \in \mathbb { R }$ be the dynamic range. Then we can define the following quantization schemes:

(i) Binary: sign (1 bit)

$$
Q _ { B } ( x ) = { \left\{ \begin{array} { l l } { + \alpha , } & { { \mathrm { i f ~ } } x \geq 0 } \\ { - \alpha , } & { { \mathrm { i f ~ } } x < 0 } \end{array} \right. }
$$

(ii) Integer: rounding (bit-width $k \geq 2 )$

$$
Q _ { I , k } ( x ) = \mathrm { c l i p } \left( \mathrm { r o u n d } \left( { \frac { x } { \alpha } } \right) , - 2 ^ { k - 1 } + 1 , 2 ^ { k - 1 } - 1 \right) \cdot \alpha
$$

where round $( x / \alpha )$ maps $x / \alpha$ to the closest integer value and $\mathrm { c l i p } ( x , l , u ) = \operatorname* { m a x } ( \operatorname* { m i n } ( x , u ) , l )$ , ensuring that

![](images/7aef2f1778e162cddcd8644b7779bfa893fe23fbd19d9ef151fc6cf6a1c64df2.jpg)  
Figure 6: Computation of forward (purple) and backward (green) pass through a simplified DNN building block using the STE. The building block consists of a convolution with quantized weights followed by a sign activation function. In the forward pass of layer l the convolution of the inputs $\mathbf { x } ^ { l }$ and the quantized weights $\mathbf { W } _ { q } ^ { l }$ is performed. The quantization function $Q$ is applied to the real-valued auxiliary weights $\mathbf { W } ^ { l }$ to retrieve the quantized weights ${ \mathbf { W } } _ { a } ^ { l }$ . The sign activation function is applied to the activations $\mathbf { a } ^ { l + 1 }$ resulting in the next layer’s inputs $\mathbf { x } ^ { l + 1 }$ . During backpropagation the green dashed line is followed, where the zero-gradient components (purple) are avoided and substituted by the gradients of the tanh and identity, respectively. The gradient updates are then applied to the real-valued auxiliary weights $\mathbf { W } ^ { l }$ according to the gradient based learning algorithm.

$Q _ { I , k } ( x ) \in \{ - w _ { \lfloor D / 2 \rfloor } , \cdot \cdot \cdot , + w _ { \lfloor D / 2 \rfloor } \}$ . This quantization scheme is termed integer quantization, because integer rounding is an essential component.

1) Dynamic range: The dynamic range α [25]–[27] is used to map integer weights $\mathbf { W } _ { q } \in \mathbb { D } ^ { D }$ , encoded with k bits, to real-valued numbers. The integer weights ${ \mathbf W } _ { q }$ are stored in addition to one real-valued number per layer, i.e. the dynamic range, and scaled according to that dynamic-range α. This scaling operation typically increases the model performance considerably and is thus often used in practice. Note that the memory requirements for the dynamic range can be neglected, because only one 32 bit value is stored per layer. In this paper, we consider two methods for determining the dynamic range, i.e.

(i) Statistics approach: Maximum absolute weight value

$$
\alpha = \operatorname* { m a x } ( | \mathbf { W } | ) ) ,
$$

where W are the auxiliary weights when using quantization aware training with the STE.

(ii) Learned approach: Learns α as additional model parameter using a gradient based optimization algorithm.

2) Fixed and learned bit-width: Quantization to discrete values with multiple bits (e.g. rounding) can be performed using either a fixed or a learned bit-width. Fixed bit-width quantization typically uses one homogeneous bit-width k for all layers, which is defined prior to training.

Recent works [25] support heterogeneous bit-widths<sup>2</sup>, which can be learned alongside the model weights using the STE. This approach enables the use of different bit-widths for each layer without introducing additional hyperparameters. Note that manual hyperparameter search of layer-wise bit-widths would span over a space that is exponential in the number of layers which is generally intractable. Essentially, the bitwidth k becomes a trainable parameter and is optimized either directly, or implicitly through learning the step size $\delta _ { w }$ and the dynamic range $\alpha .$ For training these additional model parameters, they are incorporated in the computation graph and trained via backpropagation using the STE.

When the bit-widths are trainable parameters, we use an additional loss term favoring fewer bits, i.e. the average bitwidth of weights, activations, or both. By weighting this average bit-width loss by the corresponding frequencies, i.e. the number of weights or activations per layer, this average weighted bit-width loss becomes directly proportional to the resulting overall memory requirements. In order to properly scale this bit-width loss w.r.t. the performance loss (e.g. the mean squared error), an adaptive scaling factor can be used, e.g. dependent on the validation F1-Score.

## C. Training distributions over discrete weights

An alternative approach to quantization aware training is obtained by training a distribution over discrete weights [19], [24], [28]. Let $q _ { \nu } ( \mathbf { W } _ { q } )$ be a discrete distribution over the weights $\mathbf { W } _ { q }$ governed by continuous parameters ν. Moreover, assume that the individual weights $w _ { q } \in \mathbf { W } _ { q }$ are independent such that $q _ { \nu } ( \mathbf { W } _ { q } )$ factorizes into a product of factors $q _ { \nu _ { w } } ( w _ { q } )$ for the individual weights $w _ { q } .$ , each governed by its own parameters $\nu _ { w }$ . Instead of learning the discrete weights directly, the idea is to first train the distribution $q _ { \nu } ( \mathbf { W } _ { q } )$ by optimizing a loss $\mathcal { L } ( \nu )$ that is differentiable with respect to the distribution parameters ν. After training, a DNN with discrete weights $\mathbf { W } _ { q }$ is obtained by either selecting the most probable weights arg max ${ \bf W } _ { q } \ q _ { \nu } ( { \bf W } _ { q } )$ or by sampling from $q _ { \nu } ( \mathbf { W } _ { q } )$ This process is illustrated for ternary weights in Figure 7 where, intuitively, the probability bars at each connection correspond to the trainable parameters $\nu _ { w }$ . An important property of weight distributions is that they allow us to obtain prediction uncertainties by averaging the outputs of several DNNs whose weights are sampled from $q _ { \nu } ( \mathbf { W } _ { q } )$

![](images/be938b087899cc187f9a084388d21151da410ee47a4b6e5f45609840e5c9449f.jpg)  
Figure 7: Overview of training distributions over discrete weights for trained quantization. Model weights are replaced by distributions over discrete weights (left) and optimized using a gradient-based optimization algorithm. The discretevalued model is then obtained by sampling or by selecting the most probable weights (right).

For the definition of the loss $\mathcal { L } ( \nu )$ , assume that we are given a loss over the weights $\mathcal { L } ( \mathbf { W } _ { q } )$ . We can then define a loss as expectation over $\mathcal { L } ( \mathbf { W } _ { q } )$ with respect to the distribution $q _ { \nu } ( \mathbf { W } _ { q } )$ , i.e.,

$$
\begin{array} { r } { \boldsymbol { \mathcal { L } } ( \boldsymbol { \nu } ) = \mathbb { E } _ { \boldsymbol { q } ( \mathbf { W } _ { \boldsymbol { q } } \mid \boldsymbol { q } _ { \boldsymbol { \nu } } ) } [ \boldsymbol { \mathcal { L } } ( \mathbf { W } _ { \boldsymbol { q } } ) ] + \lambda \boldsymbol { r } ( \boldsymbol { \nu } ) , } \end{array}\tag{4}
$$

where $r ( \nu )$ is a regularizer for the distribution parameters ν and $\lambda \geq 0$ is a tunable hyperparameter.

However, the expectation in (4) is a sum over exponentially many terms, which is generally intractable. We use a practical approximation for the expected loss based on the central limit theorem that has been widely used in the literature [19], [24], [29]–[31]. The central limit theorem states that the average over many independent random variables tends towards a Gaussian distribution. This is particularly convenient for DNNs with weight distributions as each neuron computes a sum over many random variables. This allows us to approximate the distribution of the $i ^ { \mathrm { { t h } } }$ activation $a _ { i } ^ { l + 1 }$ in layer l + 1 by a Gaussian $\mathcal { N } ( \mu _ { a _ { i } ^ { l + 1 } } , \sigma _ { a _ { i } ^ { l + 1 } } ^ { 2 } )$ with

$$
\mu _ { a _ { i } ^ { l + 1 } } = \sum _ { j } \mathbb { E } [ w _ { i , j } ^ { l + 1 } ] x _ { j } ^ { l } \quad \mathrm { a n d } \quad \sigma _ { a _ { i } ^ { l + 1 } } ^ { 2 } = \sum _ { j } \mathbb { V } [ w _ { i , j } ^ { l + 1 } ] ( x _ { j } ^ { l } ) ^ { 2 } ,\tag{5}
$$

where $x _ { j } ^ { l }$ is the $j ^ { \mathrm { t h } }$ input from the previous layer. In the next step, the Gaussian activation distributions are converted into deterministic values by a backpropagation-compatible sampling procedure known as the local reparameterization trick [24], [31], [32].

A repeated application of these steps, i.e., Gaussian approximation followed by the local reparameterization trick, leads to a tractable approximation of $\mathcal { L } ( \nu )$ . Note that this approach can also be used for piecewise constant activation functions such as the sign function [19], [31]. In this case, the local reparameterization trick must be applied after the activation function to maintain a differentiable loss $\mathcal { L } ( \nu )$ . This introduces some subtleties in the training process; most notably, the local reparameterization trick is applied at the discrete sign activation distribution requiring methods such as the Gumbel softmax approximation [33], [34].

In practice, it is common to store the parameters ν as unnormalized log-probabilities. Shayer et al. [24] proposed to use the squared $\ell ^ { 2 }$ norm as the regularizer $r ( \nu )$ . This enforces the distribution $q _ { \nu _ { w } } ( w _ { q } )$ to become more uniform and, therefore, to exhibit increased variance and entropy. Hence, the hyperparameter λ controls the level of variability of $q _ { \nu _ { w } } ( w _ { q } )$ and, consequently, also the amount of prediction uncertainty obtained by sampling from $q _ { \nu } ( \mathbf { W } _ { q } )$

For training, the distribution parameters ν are initialized using real-valued weights W from a pre-trained DNN with the same architecture according to the method presented in [19]. In this paper, we consider training distributions over ternary weights with $\mathbb { D } ^ { 3 } = \{ - \alpha , 0 , + \alpha \}$ , requiring $k \ = \ 2$ bits per weight. In this context, the dynamic range α can be seen as a simple scaling factor for ternary integer weights $w \in \{ - 1 , 0 , + 1 \}$ . It is computed based on the real-valued weights W from a pre-trained DNN, or trained as a learnable parameter. Note that most Bayesian inspired approaches for quantization [19], [24], [28] use a dynamic range of $\alpha = 1$ hence no scaling is performed on the integer weights.

## V. EXPERIMENTAL SETUP

We use real-world FMCW/CS radar measurements combined with simulated interference to obtain input-output pairs for training CNN models in order to perform the denoising and interference mitigation tasks. The model is applied to the processed radar signal after the second DFT, i.e. the RD map. The overall goal is the correct detection of peaks in the RD map that correspond to real objects rather than clutter or noise.

## A. Data set

The measurements were recorded in typical inner-city scenarios, where each measurement consists of 32 consecutive radar snapshots (RD maps). We used only the first receive antenna for constructing the data set. The radar signal contains reflections from static and moving objects as well as receiver noise. The simulated interference, that is added to the time domain measurement signal according to (1), is generated by sampling uniformly from the ego radar and interferer radar transmit parameters. See [35] for a detailed description of the simulation parameters and [11], [36] for an extensive analysis of the used measurement signals. The data set splits for training, validation and testing contain 2500, 250 and 250 RD maps, respectively. Data set splits are strictly nonoverlapping, hence, multiple RD maps belonging to snapshots within the same measurement cycle are never contained in multiple data set splits.

Validation of simulated interference: For model training and evaluation we only use simulated interference signals because of the immense effort that is required for recording large amounts of CNN input-output pairs of synchronized real-world measurements with and without interference. In the remainder of this section, we qualitatively analyze the validity of our simulated interference signals in order to show, that they indeed have the same characteristics as interference measurements and thus qualify for the proxy task. Therefore, we recorded a real sensor interference measurement for comparison. It was conducted in a static environment, such that most of the object signal can be extracted in a post-processing step and only the inference signal plus noise remain. We used the same sensor with identical configuration parameters for the interference measurement and the inner-city measurement campaign.

![](images/47bc0cf2242a552d917b1acdc7c0ea1f91a8bf53ca20a23c9348ea2f9caa9328.jpg)  
(a)

![](images/a2d29b9e1e6d199a87473a6d31137a6118e64d803cfc8cfa3ea430070c3f17c3.jpg)  
(b)

![](images/10d5be02a52077a7b217d436b7c952487433620c2b315681ceb71d2c74d93513.jpg)  
(c)

![](images/e2e3c484906ccd8b02dc215003443f50ecc09dfc89cd75c1c7344aa59f1c5be6.jpg)  
(d)

![](images/da7cba03b8ca2d326a5558c468781eb301779fb7de3f41ff9f967a690511bf7e.jpg)  
(e)

![](images/2a11baec1e031ba56e05a8c66bb2766a7205ae8e7ff750fed0e7b0ed61f9f6e2.jpg)  
(f)

![](images/c616f379b4455d8861e776e94e75ffc328350aa4f303bfa652ad884ecc3c8353.jpg)  
(g)

![](images/6c0e8c2eb97932acfd3be78b24425156e4fc812fe3c8f465a6dfef864ee46d4c.jpg)  
(h)  
Figure 8: Measured (top) and simulated (middle) IF interference signal. From left to right, the top rows show the time domain signal of a ramp with one single interference burst (a,d), the RD map with interference only (b,e), and the RD map when mixed with an object signal (c,f). The object signal without interference (g) was recorded in the traffic measurement campaign and the corresponding camera snapshot is depicted in (h); it shows a bus in around 35 m distance that is approaching the measurement vehicle with around 12 m/s relative velocity, and some parking cars. The SNR in (g) is around 22 dB; it decreases to about 10 dB in (c) and (f).

The simulated signal is generated according to (2). While the RF transmit signal parameters of ego radar and interferer are known, the relative timing as well as the effects of the filters $h [ n ]$ are unknown. For an adequate reconstruction, the unknown parameters in (2) are estimated from the measured signal.

Figure 8 illustrates a recorded interference in the top row and its simulated reconstruction in the middle row. In Figures 8(a) and 8(d), we can see the IF signal of a single interfered ramp in time domain. The interference burst is visible from roughly $5 { - } 9 \mu \mathrm { s }$ and incorporates a chirp-like form, as mentioned in Section II. The simulated signal matches the measurement relatively well in terms of its location, duration and general chirp-like form. However, differences can be found in the form of the envelope and in the signal’s symmetry properties. This is a direct consequence of missing information about the analog receive filters in the hardware sensor. In particular, a model of their phase responses would be required, as a non-constant group delay causes such distortions of the envelope. Furthermore, also multipath reflections may contribute to such effects.

Besides these analog filters, the measurement is also preprocessed digitally by zero-phase high- and low-pass filtering. These digital filters are known and simulated, which is why Figure 8(d) also differs from the ideal interference as illustrated in Figure 4.

One measurement of 128 ramps contains several such chirp bursts at different locations, this results in structured noise patterns on the RD map, as shown in Figures 8(b) and 8(e) without adding object signals and in Figures 8(c) and 8(f) when combined with the object signal from Figure 8(g). Even though simulated and measured interference are not exactly identical, they both incorporate similar characteristics and patterns, and can hardly be distinguished in RD domain. This qualitative investigation shows, that simulated interference may well approximate real-world signals.

## B. Evaluation

The F1-Score is used as evaluation metric, which is defined as the harmonic mean of precision $p$ and recall r, i.e.:

$$
\mathrm { F } _ { 1 } = 2 { \frac { p \cdot r } { p + r } } .\tag{6}
$$

The precision $p$ measures the ratio of correct object detections to the total number of object detections according to the interference mitigated RD map, thus it considers the number of false-alarms. The recall r defines the ratio of correct object detections to the total number of object detections in the ground truth data, thus it considers the number of correctly identified object peaks. The ground truth target detections were obtained by manually labeling the clean measurement RD maps without interference. A Cell Averaging Constant False Alarm Rate (CA-CFAR) target detection algorithm [37] is used to automatically extract detections, hence peak locations, from the interference mitigated model outputs. Both the ground truth target detections and the CA-CFAR generated detections from interference mitigated RD maps are the basis for the F1- Score. We calculate the mean sample-wise F1-Score per model and report the mean and the standard deviation over three individually trained models with independent initialization if not stated otherwise.

## VI. EXPERIMENTAL RESULTS

First, we analyze performance effects due to binarization of CNN-based models from [11] for interference mitigation. We consider binary weights and activations, and we illustrate the impact of the CNN architecture on the performance degradation due to quantization.

![](images/36db32f79030a35f5a0080a0e76a4cce329e4aae05e695850f54feed6b6b26c7.jpg)  
(a) Layers

![](images/251016342dc6224c43bc7712abaeabf564d56eaf6eeed048ba89e722adc6e44d.jpg)  
(b) Channels  
Figure 9: Performance comparison of binarized models using different numbers of layers and channels. The reference F1- Score of the clean measurement data (Clean) and the interfered data (Interfered) are indicated as horizontal lines. For each model configuration on the x-axis, the solid line indicates the performance of a bottleneck-based architecture of channels (Architecture B, see Section III). The dashed line uses the same number of channels $C = 1 0 2 4$ in every layer except the last one, which consists of two channels (Architecture $\mathbf { A } ,$ see Section III).<sup>3</sup>

Based on high performing, structurally small and realvalued models we present quantization results with different fixed as well as learned bit-widths, which are determined layerwise and learned in addition to the model weights. We compare a real-valued model, a quantized model and a selection of ’classical’ interference mitigation methods in terms of F1- Scores. Also, we show a qualitative example of real-sensor interference mitigation.

Next, we consider ternary weight models and compare the results obtained by quantization aware training with models that are trained using discrete weight distributions. Then, we show that the training of discrete weight distributions can be used to produce uncertainty estimates of the predicted RD maps. Finally, we visualize the CNN model’s learned filter kernels and activations.

A. Binarization effects of CNN-based models for interference mitigation

Figure 9 shows a performance comparison of different model architectures and quantization strategies. Figure 9(a) shows architectures with $C = 1 0 2 4$ maximal channels and $L \in \{ 3 , 5 , 7 \}$ layers, while Figure 9(b) shows architectures with $L = 7$ layers and $C \in \{ 3 2 , 2 5 6 , 1 0 2 4 \}$ maximal channels. Both figures contain real-valued models (Real), models with binary weights (Weights) and models with binary activations (Activations). Note that only a model surpassing the score for interfered data (Interfered) yields an improvement. All quantized models were trained using quantization aware training with the STE and binary quantization (sign).

The real-valued baseline (Real) in Figure 9(a) performs well for both model architectures (A or B, see Section III) as well as for all considered numbers of layers L and channels C. Models with binary weights (Weights) or activations (Activations) tend towards a better performance with a higher number of layers and model parameters. An exception is the model with binary activations and architecture B, where the minimal number of channels, i.e. the number of channels in the $L - 1 ^ { t h }$ layer for a model with L layers, seems to be the limiting factor. Generally, architecture B yields better results for binarized weights whereas architecture A is better suited for binarized activations.

![](images/6ab20b962a3adcd54d27e50f40ea3bace32ec8b10ed0bccf9815ab373bb01782.jpg)  
(a) Models with 8, 16, and 32 channels.

![](images/525354de3af05f35115e9127b20f052c871e7b3d8d753847a1344c2bb4048ce1.jpg)  
(b) Models with 256 and 1024 channels.  
Figure 10: Total memory requirements [MB] for real-valued models during the inference step. The total requirements consist of the memory for weights plus the memory for the two largest consecutive layers of activations.<sup>3</sup>

Figure 9(b) shows that the real-valued model (Real) is also robust with regard to different numbers of maximal channels $C ~ \in ~ \{ 3 2 , 2 5 6 , 1 0 2 4 \}$ for $L \ = \ 7$ layers. Binary weight (Weights) and binary activation (Activations) models on the other hand depend highly on the number of channels. The limiting factor is not only the minimal number of channels, but also the total number of channels. This can be observed by comparing architecture B with $C \ = \ 3 2$ and $C \ = \ 2 5 6$ maximal channels, where they both have 8 channels in layer L 1 but the model with an overall higher number of channels performs better. Models with binary activations require a very large number of channels and thus parameters in order to reach a high F1-Score.

In summary, we have shown that binary weight models can almost reach the performance of their real-valued equivalent given a high number of model parameters and especially channels. In the binary weight case, architecture B is preferable. For binary activations however, architecture A performs better. In any case, a large number of parameters is required in order to reach a high F1-Score.

## B. Performance-memory relation of different architectures and quantization strategies

The total memory requirements during the inference step stem from storing (i) model parameters and (ii) activations of two consecutive layers that need to be stored during the computation. For the sake of run time and energy efficient computations, these parameters and variables have to be stored in fast accessible on-chip memory simultaneously.

![](images/5e3ff16be8e2eacbf61dc54701ef733817e427ea9642b777cdf400c3286624cb.jpg)  
Figure 11: Average F1-Score vs. memory requirements in megabytes [MB] during the inference step of real-valued (Real), binary weight (Weights) and binary activation (Activations) models. The circle size corresponds to the number of million operations (MOPS) required during the inference step. The Pareto optimal points are marked using black borderlines; they all belong to real-valued models. The smallest models for each category are annotated<sup>3</sup>; see TABLE I for details of annotated models.

<table><tr><td>Model</td><td>Param.</td><td>QT</td><td>Weights [MB]</td><td>Act. [MB]</td><td>Total [MB]</td><td>MOPS</td><td>F1-Score</td></tr><tr><td>L3-C8-B</td><td>504</td><td>R</td><td>0.002</td><td>0.42</td><td>0.42</td><td>5</td><td>0.888</td></tr><tr><td>L3-C8-A</td><td>864</td><td>R</td><td>0.003</td><td>0.56</td><td>0.57</td><td>8</td><td>0.895</td></tr><tr><td>L3-C16-B</td><td>1584</td><td>R</td><td>0.006</td><td>0.84</td><td>0.85</td><td>15</td><td>0.896</td></tr><tr><td>L3-C16-A</td><td>2880</td><td>R</td><td>0.011</td><td>1.12</td><td>1.14</td><td>27</td><td>0.900</td></tr><tr><td>L7-C32-A</td><td>47k</td><td>W</td><td>0.006</td><td>2.25</td><td>2.26</td><td>441</td><td>0.871</td></tr><tr><td>L7-C256-B</td><td>398k</td><td>W</td><td>0.047</td><td>13.50</td><td>13.55</td><td>3.7k</td><td>0.867</td></tr><tr><td>L7-C256-A</td><td>2958k</td><td>A</td><td>11.285</td><td>0.56</td><td>11.86</td><td>27k</td><td>0.860</td></tr></table>

TABLE I: Memory usage and performance details for models annotated<sup>3</sup> in Figure 11. The quantization type QT can be R for real-valued models, W for binary weights, or A for binary activations (sign).

Figure 10 shows the total memory requirements per model architecture. All depicted models are real-valued and reach a similar F1-Score of $F 1 \ge 0 . 8 9$ . Models with few channels (e.g. 8, 16 or 32) have much smaller memory requirements than models with many channels (e.g. 256 or 1024); note the different y-axis scales in Figures 10(a) and 10(b). Quantization reduces the memory footprint by a factor of up to 32, namely in the binary case. Since even the smallest models from Figure 10 reach a high F1-Score and bigger models could not surpass their memory efficiency even with binary quantization, only these small models can be used as base models for quantization.

Figure 11 illustrates the performance to memory relation for real-valued models, models with binary weights and models with binary activations. TABLE I lists details of the smallest models per quantization type. The results clearly show that models with binarized weights or activations reaching an acceptable F1-Score require more memory than a real-valued alternative with fewer parameters. All Pareto optimal points correspond to real-valued models. Already particularly small real-valued models reach a high F1-Score of $F 1 ~ > ~ 0 . 8 9$ such as the model denoted as $\mathbf { \vec { \tau } } _ { \mathbf { L } 3 - \mathbf { C } 1 6 - \mathbf { B } } ,$ which has $L = 3$ layers and $C _ { l } ~ = ~ [ 1 6 , 8 , 2 ]$ channels in these layers. We thus conclude, that considered binarized CNNs are not suited for radar denoising and interference mitigation. Instead, we investigate quantization with multiple bits for weights and activations which could be used to further reduce the memory requirements of small real-valued models. We choose the model with $L = 3$ layers and $C _ { l } = [ 1 6 , 8 , 2 ]$ channels as a base model for all further experiments, it yields an F1-Score of $F 1 = 0 . 8 9 6 0$

![](images/1b66fed3e20a833e4352d832d09d04447776eb9b61aac01f4d305fe9faf7703b.jpg)

![](images/5ba272a54ccc9d07c4043cf842e7c63f3220df9cc73ae492c3d01f090808a08e.jpg)

Figure 12: Average F1-Score and memory requirements [kB] for models with fixed and learned bit-widths. Fixed bitwidths (left) are used for weights as well as activations (WA). Learned bit-widths (right) are optimized for either weights (W), activations (A) or both (WA). The model has $L  = \ 3$ layers and $C \ = \ [ 1 6 , 8 , 2 ]$ channels. Details about memory requirements, performance and average bit-widths are listed in TABLE II.
<table><tr><td rowspan="2">QT</td><td colspan="2">Weights</td><td colspan="2">Activations</td><td rowspan="2">Total [kB]</td><td rowspan="2">F1-Score</td></tr><tr><td>[kB]</td><td>[Bits]</td><td>[kB]</td><td>[Bits]</td></tr><tr><td colspan="8">Fixed bit-width</td></tr><tr><td>4WA</td><td>0.77</td><td>4</td><td>108</td><td>4</td><td>109</td><td> $0 . 8 6 1 7 \pm 0 . 0 0 4$ </td></tr><tr><td>6WA</td><td>1.16</td><td>6</td><td>162</td><td>6</td><td>163</td><td> $0 . 8 8 3 6 \pm 0 . 0 0 2$ </td></tr><tr><td>8WA</td><td>1.55</td><td>8</td><td>216</td><td>8</td><td>218</td><td> $0 . 8 9 3 7 \pm 0 . 0 0 1$ </td></tr><tr><td>32WA</td><td>6.19</td><td>32</td><td>864</td><td>32</td><td>870</td><td> $0 . 8 9 6 0 \pm 0 . 0 0 2$ </td></tr><tr><td colspan="7">Learned bit-width</td></tr><tr><td>W</td><td>0.67</td><td>4.3</td><td>864</td><td>32.0</td><td>865</td><td> $0 . 9 0 0 0 \pm 0 . 0 0 1$ </td></tr><tr><td>A</td><td>6.19</td><td>32.0</td><td>171</td><td>6.5</td><td>177</td><td> $0 . 8 9 5 8 \pm 0 . 0 0 2$ </td></tr><tr><td>WA</td><td>0.83</td><td>5.0</td><td>198</td><td>7.5</td><td>198.99</td><td> $0 . 8 9 5 8 \pm 0 . 0 0 2$ </td></tr></table>

TABLE II: Memory, performance and bit-width details for results shown in Figure 12. The quantization type QT can be W for weights, A for activations, or WA for weights and activations. The number of bits for fixed bit-widths is indicated in front of the quantization type. The learned bit-width is stated in average bits per value over all layers. The memory usage is stated in kilobytes [kB] and the F1-Score is listed as ’mean standard deviation’ over three independently trained models. The model has $L = 3$ layers and $C _ { l } = [ 1 6 , 8 , 2 ]$ channels.

## C. Quantization with multiple bits using fixed and learned bitwidths

We aim to further reduce the memory size of the real-valued model with $L = 3$ layers and $C = [ 1 6 , 8 , 2 ]$ channels without substantial performance degradation. We use the Brevitas framework [38] to (i) analyze quantization performance with different fixed bit-widths $k \in \{ 1 , 2 , 4 , 6 , 8 , 3 2 \}$ for weights as well as activations and (ii) to learn the bit-width of model weights and activations per layer. In any case, we use integer quantization and determine the dynamic range as the maximum absolute value over the real-valued auxiliary weights (see Section IV-B1). Figure 12 shows the performance of these different quantization strategies, where Figure 12(a) contains models with fixed bit-widths including the real-valued base model, and Figure 12(b) contains models with learned bitwidths, using the following quantization options:

(i) Weights (W): Quantized weights with learned bit-widths and real-valued activations.

(ii) Activations (A): Real-valued weights and quantized activations with learned bit-widths.

(iii) Weights+Activations (WA): Quantized weights and ac tivations with learned bit-widths.

TABLE II lists corresponding details regarding the performance and memory requirements for weights and activations, including average bit-widths.

Models with a fixed number of $k = 1$ or $k = 2$ bits are not suited for the task and do not even reach the F1-Score of data without mitigation. With $k = 4 , k = 6$ , and $k = 8$ bits the performance increases steadily and almost reaches the real-valued score with only 8 bits. The resulting memory saving with 8-bit weights and activations is approximately 75% compared to the real-valued baseline.

For quantization strategies using learned bit-widths, we consider the smallest bit-widths reached without significant performance degradation per category (Weights, Activations, Weights+Activations). The results shown in Figure 12(b) and their corresponding details stated in TABLE II show the effectiveness of quantized activations over quantized weights for the considered task of RD interference mitigation. When optimizing only the weight bit-widths and keeping full precision activations, we reach an average learned bit-width of 4.3 bits over all layers. Nonetheless, the overall memory reduction is minimal. When quantizing only activations on the other hand, an average bit-width of 6.5 is reached which reduces the overall memory requirements during the inference step considerably. With 177.35 kB, we achieve a memory reduction of approximately 80% for the model with learned bit-width activations compared to the real-valued baseline. This behavior stems from the large number of activations in two consecutive layers compared to the total number of model weights. We have this inequality in number of values per activation layer versus model weights due to our task and the associated model.

We observe that quantizing only activations using a learned bit-width results in the highest memory reduction without substantial performance degradation. The learned activation bit-width using quantized activations is one bit lower than the learned activation bit-width when using quantized weights and activations. In the latter case, local minima in the combined loss function are reached, that hinder further optimization. The small difference in learned activation bit-widths has a stronger effect on the overall memory requirements than weight quantization.

![](images/4d9181c3431624b31ec04097249574f8236b0e5a13070768213074fb7cd66301.jpg)  
Figure 13: CDF comparison of the 0.6 0.8 <sub>sample-wise</sub> <sub>F1-Score</sub> <sub>between</sub> <sub>the</sub> <sub>real-</sub> xvalued CNN model (CNN-Real), the 8 bit quantized CNN model (CNN-8WA), and the three classical methods zeroing, IMAT and Ramp filtering.

![](images/ed666010aeeda9282102a1bc91a0d6e311c68602904ff7c2c58739285175a7c1.jpg)  
Figure 14: Performance comparison between quantization aware training with the STE and discrete weight distributions. Different factors for scaling the dynamic range are depicted on the xaxis, i.e. None, computed from statistics and learned as parameter.

![](images/ed4f61c330085eb4e7ec049349d37651d3994cb924daa6c5cc4a187f5b18aba4.jpg)  
Figure 15: F1-Score with different regularization weight λ. The discrete model weights are obtained by the most probable weights (MP), sampling once (S1) or sampling 100 times (S100).

<table><tr><td rowspan="2">Method</td><td rowspan="2">F1-Score</td><td colspan="3">Parameters</td><td rowspan="2">MOPS</td></tr><tr><td>Count</td><td>Bits</td><td>[kB]</td></tr><tr><td>CNN-Real</td><td>0.8960</td><td>1584</td><td>32</td><td>6.19</td><td>15.33</td></tr><tr><td>CNN-8WA</td><td>0.8937</td><td>1584</td><td>8</td><td>1.55</td><td>15.33</td></tr><tr><td>Zeroing</td><td>0.8515</td><td></td><td></td><td></td><td>2.83</td></tr><tr><td>RFmin</td><td>0.8754</td><td></td><td></td><td></td><td>3.13</td></tr><tr><td>IMAT</td><td>0.8604</td><td>一</td><td></td><td></td><td>3.88</td></tr></table>

TABLE III: Comparison of the average F1-Score and resource requirements between the real-valued CNN model (CNN-Real), the 8 bit quantized CNN model (CNN-8WA), and the three classical methods zeroing, IMAT and Ramp filtering.

In comparison to the fixed 8 bit model for weights and activations (8WA), we have a memory reduction for the model with learned bit-width activations (A) of around 40 kB with a slightly better F1-Score (+ 0.0021). However, this relatively small improvement might be negligible in practice, because of the implementation overhead for heterogeneous bit-widths. To fully exploit a heterogeneous bit-width, a specialized hardware with custom arithmetic units would be required. Therefore, we recommend to use 8 bits for all weights and activations, which allows the use of standard integer processing units.

## D. Performance comparison with classical interference mitigation methods

We compare our CNN-based models in the real-valued setting (Real) as well as in the 8 bit quantized setting (8WA) with the classical and state-of-the-art interference mitigation methods zeroing [3], Iterative method with adaptive thresholding (IMAT) [39] and Ramp filtering [4]; see [36], [40] for an overview of these methods. Zeroing and IMAT highly depend on an interference detection step, which influences their performance considerably. In our experiments we identified timedomain samples incorporating interference with approximately 90% accuracy; this interference detection rate seems feasible in practice. Note, that IMAT is even more susceptible to false detections than zeroing, and that Ramp filtering as well as the CNN-based models do not depend on such an explicit interference detection step at all.

Figure 13 shows the empirical cumulative density function (CDF) of their evaluated per-sample F1-Score values. The ’clean’ measurement and interfered signals are included as reference. All three classical methods, namely zeroing, IMAT and Ramp filtering, improve the F1-Score when applied to the measurement signal with interference. Zeroing and IMAT yield very similar F1-Scores. Ramp filtering outperforms both other classical methods, particularly for samples with strong interference (see black magnification). See [36] for a detailed performance analysis of classical interference mitigation methods.

The CNN-based models, both with real-valued as well as 8 bit quantized weights and activations, are competitive with the classical methods for all considered interference levels and even outperform the best classical method, namely Ramp filtering. The CDF shape indicates that the CNN-based models are robust with respect to different interference patterns and levels. This is indicated by the CDF’s narrow form and high values for the lowest F1-Scores per CNN model (see gray magnification). The lowest F1-Scores are approximately $F 1 _ { \mathrm { l o w , 8 W A } } = 0 . 5 7$ and $F 1 _ { \mathrm { l o w , R e a l } } = 0 . 6 0$ for the 8 bit quantized (CNN-8WA) and realvalued (CNN-Real) CNNs respectively. For comparison, the measurements with and without interference yield a lowest F1-Score of $F 1 _ { \mathrm { l o w , I n t e r f e r e d } } = 0$ and $F 1 _ { \mathrm { l o w , C l e a n } } = 0 . 6 3$ . The CDF of the 8 bit quantized CNN is very similar to the realvalued model’s CDF, showing that we can reduce the memory footprint by a factor of four without impairing performance.

TABLE III shows the average sample-wise F1-Score along with required parameters and million operations (MOPS) for the real-valued CNN (CNN-Real), the 8 bit quantized CNN (CNN-8WA), and the three classical methods zeroing, IMAT and Ramp filtering. The superior F1-Score of the CNN-based methods is at the expense of hardware resources. The CNN model parameters have to be stored and the models require around five times more MOPS than the classical methods. However, the quantized model improves these expenses considerably. Even though the CNN models have the same number of parameters (1584) and MOPS (15.33), only one fourth of memory is required to store the 8 bit quantized model in comparison to the real-valued CNN model. Also the energy and time consumption can be reduced in the quantized case, because pure integer arithmetic can be used for the convolution operations which might lead to a faster computation depending on the hardware.

![](images/3980466b407e2499e016e188e099011bd367e215d167f592cd8e3bcac14228e4.jpg)

![](images/d815684e884b7ac75659f5641466075f99f2ea51d2e60c251f097ce798954f05.jpg)  
(a) Object signal

![](images/5938016c6d4b1e43ce526cb548574bdfa441ddd5661a32417354771e3229baa1.jpg)  
(b) With interference  
(c) After CNN mitigation  
Figure 16: RD magnitude spectra in decibel [dB] without interference $( \mathrm { S N R } = 3 2 ~ \mathrm { d B } )$ combined with real-sensor interference $( \mathrm { S N R } = 1 9 $ dB) and after CNN interference mitigation (SNR $= 2 6 ~ \mathrm { d B } )$

## E. CNN interference mitigation on a real-sensor interference

In order to illustrate successful CNN interference mitigation performance on real-sensor interference signals, despite the lack of a large set of such measurements, we show quantitative results of an exemplary RD map in Figure 16. The interference signal is obtained using real-sensor measurements and combined with an object signal from the inner-city measurement campaign, as described in Section V-A. Several object peaks are visible in the ’clean’ measurement RD map (Figure 16(a), $\mathrm { S N R } = 3 2 \ \mathrm { d B } )$ . The interfered RD map (Figure 16(b), SNR = 19 dB) contains distinctive interference patterns and complicates the identification of object peaks. After interference mitigation using the real-valued CNN model, which was solely trained on simulated interference signals, most of these patterns are removed and the noise floor is damped, while the object peaks are retained (Figure 16(c), $\mathrm { S N R } = 2 6 ~ \mathrm { d B } )$ This example illustrates the potential of our approach, while more quantitative results and in-the-wild-interference signals are to be evaluated. The generalization from simulated to realsensor interference signals is promising, but using real-sensor interference signals during training or for transfer learning has even more potential in terms of real-world interference mitigation.

## F. Quantization aware training vs. training distributions over discrete weights

Here, we consider training discrete distributions over ternary weights as described in Section IV-C. In contrast to quantized DNN models that only produce point estimates, weight distributions additionally allow us to obtain uncertainty estimates over model predictions, i.e. RD uncertainty maps. We use the CNN model with $L \ = \ 3$ layers, $C _ { l } ~ = ~ [ 1 6 , 8 , 2 ]$ channels, real-valued ReLU activations and ternary weights $W ~ \in ~ \{ - \alpha , 0 , + \alpha \}$ requiring 2 bits $\mathrm { { e a c h . ^ { 4 } } }$ For comparison we use quantization aware training with the STE and integer quantization with a bit-width of $k \ = \ 2 ;$ this also results in ternary weights $W \in \{ - \alpha , 0 , + \alpha \}$ . Figure 14 shows the performance comparison between quantization aware training with the STE and the training of discrete weight distributions with three different methods of determining the dynamic range α. For ternary weights that are symmetric around zero, the dynamic range α is equal to the step size $\delta _ { w }$ and can be seen as a simple scaling factor that is multiplied to integer ternary weights $W \in \{ - 1 , 0 , 1 \}$ . For the calculation of the scaling factor α we consider the three methods as described in Section IV-B1:

None: no scaling factor, i.e. $\alpha = 1$

Statistics: the maximal absolute value of real-valued auxiliary weights (quantization aware training) or pre-trained weights (discrete distributions)

## Learned: scaling factor learned as a model parameter

Quantization aware training does not learn the interference mitigation task at all when no scaling factor α is used; this results from a combination of the used weight initialization (small values close to zero) and quantization type (integer rounding). Training discrete distributions over weights $W \in \{ - 1 , 0 , 1 \}$ on the other hand yields a high F1-Score of $F 1 = 0 . 8 7$ without scaling. With a scaling factor calculated from weight statistics, both quantization aware training and training with discrete distributions increase performance substantially and reach an $\mathrm { F 1 - S c o r e } \geq 0 . 8 9$ . For training discrete distributions a learned scaling factor performs similar to the one from statistics, but for quantization aware training the learned scaling factor worsens the results considerably.

The choice of the dynamic range α has a high impact on the model performance. We propose to use the maximal absolute weight per layer. According to our results this choice of dynamic range calculation is robust, has a small computation overhead and results in a high performance, independent of the training approach. Training distributions over discrete weights yields competitive results in comparison to quantization aware training with the STE for the considered weight quantization. With regard to the scaling factor, training distributions over discrete weights even seems to be more robust.

## G. Uncertainty maps and effects of the distribution regularization term

Figure 15 shows different values for λ, i.e. the contribution of the distribution regularization term to the network loss (see Section IV-C). We use the same model as before, i.e. a CNN with $L = 3$ layers and $C _ { l } = [ 1 6 , 8 , 2 ]$ channels, and use the maximum absolute weight as scaling factor α per layer. The results illustrate the effect of λ for three different variants of retrieving the weight values:

## MP: most probable weights

S1: weights are sampled from the weight distribution

S100: weights are sampled 100 times from the weight distribution and their average is used

Each variant that involves sampling (S1 and S100) is computed and evaluated 100 times in order to capture the variance of model predictions based on these sampled weights.

Velocity [m/s]  
![](images/f0721400cff217a4850c22365fef02163fdf8b567aa8bc7c2ec0b12999cf04fe.jpg)  
(a) RD with λ = 10<sup>−10</sup>

![](images/a94bc082239d19cea894e909045eccff3e8db5c55b5138bf834e65e080c116ec.jpg)

![](images/5b352087b6a8f9a532a8966a69bb89897621d8f5a8b6aef83c758a7369208f6e.jpg)  
(b) RD with λ = 10<sup>−9</sup>

![](images/53d5d3dbafa91c953b720094c3777767bc9b546db24b436635c3207907b72833.jpg)  
(c) RD with λ = 10<sup>−8</sup>

(d) Uncertainty with λ = 10<sup>−10</sup>  
![](images/bd527f8ec443147664669740df0bed5e15f3a4440856f007a01bd2816975e931.jpg)  
(e) Uncertainty with λ = 10<sup>−9</sup>

![](images/515e87c9988f122260d319a095873dac436b1c04e279f315adf7167a8caacafb.jpg)  
(f) Uncertainty with λ = 10<sup>−8</sup>  
Figure 17: Interference mitigated RD predictions (top) and corresponding uncertainty estimates (bottom) with increasing influence (left to right) of the distribution regularization term with $\lambda = \{ 1 0 ^ { - 1 0 } , \bar { 1 0 } ^ { - 9 } , 1 0 ^ { - 8 } \}$ . Manually labeled object peaks are indicated in red.

Our results show that for large λ the performance decreases whereas there is a significant drop with $\lambda \ge 5 \cdot 1 0 ^ { - 8 }$ . The MP weights always perform best, whereas the difference to S1 and S100 increases with a higher regularization term. Both S1 and S100 tend to have a higher variance with a higher regularization term. S100 is always better than S1 but it does not outperform the most probable weights MP.

Figure 17 shows the RD predictions and their corresponding uncertainty estimates, i.e. the standard deviation of RD log magnitudes, of S100 over 100 evaluations for different $\lambda \in \{ 1 0 ^ { - 1 0 } , 1 0 ^ { - 9 } , 1 0 ^ { - 8 } \}$ . Figure 18 shows the corresponding ’clean’ measurement and the measurement with interference as reference. All RD predictions and uncertainty maps contain an overlay with the ’ground truth’ object detections, i.e. the manual labels as considered for evaluation.

As already shown in the last experiment, we achieve the highest interference mitigation performance with a low λ. Accordingly, the average RD predictions of S100 over 100 evaluations contain well-suppressed interference patterns with $\lambda = 1 0 ^ { - 1 0 }$ . For larger λ values they contain slightly more noise, interference and smoothed object peaks. Also the standard deviation over the 100 RD log magnitude predictions increases with a higher regularization term, while the object peaks have an extremely low uncertainty independent of λ. The interference patterns, as contained in the measurement with interference in Figure 18, become more apparent with higher output uncertainty as shown in Figure 17 in the right column.

## H. Visualization and interpretation of learned filter kernels

While there is no simple approach of interpreting what the CNN model has learned, we can gain more insights by inspecting visualizations of learned filter kernels and activations (i.e. feature maps) for a specific input. Figure 19 shows RD map patches of model inputs, outputs and activations after each layer for the real-valued CNN. The same RD measurement is used, where the left side input includes interference and the right side input does not. We analyzed the activations corresponding to the input with interference and the ones without interference and made the following observations:

![](images/e154f298df0b5e89be5b2092b21de53a2e25a658fbcd6bd5ed47cb2475e508eb.jpg)  
(a) Object signal

![](images/8e4d788a71d90de3d93a4b84a896e25bac1662d2e5da5e7246db05fce6dd23a7.jpg)  
(b) With interference  
Figure 18: RD magnitude spectra with and without interference. Manually labeled object peaks are indicated in red.

• Inputs with interference have similar patterns in real and imaginary parts, including positive and negative values.

• All activations after the $1 ^ { \mathrm { s t } }$ layer contain high magnitude values (positive and negative) at object positions.

• Some activations after the $1 ^ { \mathrm { s t } }$ layer contain much more interference than others (compare patches with green borders) and seem to concentrate on different aspects of interference patterns. E.g. the activations marked with an orange border contain strong diagonal patterns while the activations marked with a red border contain more unstructured noise.

• Activations after the $2 ^ { \mathrm { n d } }$ layer are either all positive or all negative for inputs without interference. However, for inputs with interference, there are activations (compare patches with blue borders) that separate a patch into objects and interference patterns by means of positive and negative values.

• The activations at the outputs resemble the inputs at object positions while possible interference and noise are removed. Note, that the output from the sample with interference contains even less noise than the output from the sample without interference which stays almost unchanged.

Figure 20 shows the learned filter kernels of the real-valued CNN model for the first and last layers. The first and last layer filter kernels can be interpreted, because we have an intuition about the input and output of the model. In contrast, an interpretation of the second layer filter kernels is difficult, since it operates on activations from hidden layers. The learned filter kernels are diverse and resemble well known spatial filter types:

Gaussian filters smooth the input. These filters have all positive or all negative values, where the intensity is higher in the middle and lower at the corners. E.g. ,

Gradient filters can detect edges along different dimensions, i.e. horizontal, vertical and diagonal. They show first order spatial derivatives of the input and they themselves have edges of positive or negative values along some dimension. E.g. , ,

Laplacian filters highlight regions of rapid intensity changes in the input. They show second order spatial derivatives of the input and have a positive or negative peak in the middle, that is surrounded by lower intensity values of the opposite sign. E.g. ,

![](images/d2aec93f6a9d1c0888f3c06db2a6d0542b0d5282f8377ca58cdc9a228a98a981.jpg)  
Figure 19: Visualization of RD map patches of inputs, outputs and activations after each layer for the real-valued CNN model. The left and right side show patches for an example with and without interference, respectively. The log magnitude spectra of inputs and outputs are shown only for illustration purpose and they are not directly used by the model. The color intensity of activations correlates with their magnitude and the color map scale is identical for corresponding activation patches on the left and right side. Red, white and blue indicate positive, zero and negative values, respectively.

![](images/fef8effc45ae09eb52e368348e292949eb1e7a7a7b0b54d1d738643d50b3c31c.jpg)  
Figure 20: Visualization of the learned filter kernels for the real-valued CNN model. Filter kernels are normalized and the color map ranges from minus to plus one, where red is positive, blue is negative and white indicates a value of zero.

The first layer contains diverse variations of Gaussian and gradient filters. They are directly applied to the input and used for low level feature detection. The third layer contains Laplacian filters, which are used to reassemble real and imaginary parts from the second layer outputs. Note, that also in classical computer vision applications Laplacian filters are often used in combination with other filters (e.g. Gaussians) that are previously applied to the inputs. This visualization gives a valuable insight into learned filter kernels and how the model detects and removes the interference. The output is then reconstructed using the objects without including that interference.

## VII. CONCLUSION

In this paper, we investigate the capability to quantize CNNbased models for denoising and interference mitigation of radar signals. Our experiments emphasize the importance of small real-valued base models in order to obtain memory efficient models after quantization. We conclude, that small architectures are not suitable for binarization in the context of the considered regression task and instead multiple bits are required to retain high performance. For the considered task and selected base model, the quantization of activations has a substantially higher impact on the overall memory than the quantization of weights. The bit-width can be learned in addition to the model weights resulting in a memory reduction of up to 80% for the selected base model. However, for simplicity and practical reasons, we advocate 8-bit quantization of all weights and activations yielding a memory footprint reduction of approximately 75% compared to the real-valued model without any noteworthy performance degradation. Furthermore, we analyze the effects of training distributions over discrete weights in contrast to quantization aware training with the STE and find that competitive results can be achieved including additional information about uncertainty estimates in interference mitigated RD maps. As future work we plan to conduct quantitative evaluations of real-world interference signals. Further interesting directions are model architectures that exploit sequential and multichannel information.

## ACKNOWLEDGMENTS

This work was supported by the Austrian Research Promotion Agency (FFG) under the project SAHaRA (17774193) and NVIDIA by providing GPUs.

[1] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical Investigation of Non-Coherent Mutual FMCW Radar Interference,” in 2018 European Radar Conference (EURAD), pp. 71–74, 2018.

[2] G. Kim, J. Mun, and J. Lee, “A Peer-to-Peer Interference Analysis for Automotive Chirp Sequence Radars,” IEEE Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8110–8117, 2018.

[3] C. Fischer, Untersuchungen zum Interferenzverhalten automobiler Radarsensorik. PhD thesis, Ulm University, 2016.

[4] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-Free Interference Cancellation Method for Automotive FMCW Radar Systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS), 2018.

[5] F. Marvasti, M. Azghani, P. Imani, P. Pakrouh, S. Heydari, A. Golmohammadi, A. Kazerouni, and M. Khalili, “Sparse signal processing using iterative method with adaptive thresholding (IMAT),” in 2012 19th International Conference on Telecommunications (ICT), 2012.

[6] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in 2017 18th International Radar Symposium (IRS), pp. 1–10, 2017.

[7] F. Jin and S. Cao, “Automotive radar interference mitigation using adaptive noise canceller,” IEEE Transactions on Vehicular Technology, vol. 68, no. 4, pp. 3747–3754, 2019.

[8] “Digital beamforming to mitigate automotive radar interference,” 2016 IEEE MTT-S Int. Conf. Microwaves Intell. Mobility, ICMIM 2016, pp. 2– 5, 2016.

[9] J. Mun, H. Kim, and J. Lee, “A deep learning approach for automotive radar interference mitigation,” in 2018 IEEE 88th Vehicular Technology Conference (VTC-Fall), pp. 1–5, 2018.

[10] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using rnn with self attention,” in ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 3802–3806, 2020.

[11] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world fmcw radar signals,” in 2020 IEEE International Radar Conference (RADAR), pp. 624–629, 2020.

[12] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully Convolutional Neural Networks for Automotive Radar Interference Mitigation,” 7 2020.

[13] M. L. L. de Oliveira and M. J. G. Bekooij, “Deep convolutional autoencoder applied for noise reduction in range-doppler maps of fmcw radars,” in 2020 IEEE International Radar Conference (RADAR), pp. 630–635, 2020.

[14] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR), pp. 315–320, 2020.

[15] S. Han, J. Pool, J. Tran, and W. J. Dally, “Learning both weights and connections for efficient neural networks,” 2015.

[16] H. Cai, L. Zhu, and S. Han, “ProxylessNAS: Direct neural architecture search on target task and hardware,” in International Conference on Learning Representations, 2019.

[17] W. Roth, G. Schindler, M. Zohrer, L. Pfeifenberger, R. Peharz, S. Tschi-¨ atschek, H. Froning, F. Pernkopf, and Z. Ghahramani, “Resource-¨ efficient neural networks for embedded systems,” 2020.

[18] I. Hubara, M. Courbariaux, D. Soudry, R. El-Yaniv, and Y. Bengio, “Binarized neural networks,” in Advances in Neural Information Processing Systems 29, pp. 4107–4115, 2016.

[19] W. Roth, G. Schindler, H. Froning, and F. Pernkopf, “Training discrete-¨ valued neural networks with sign activations using weight distributions,” in Machine Learning and Knowledge Discovery in Databases, pp. 382– 398, 2020.

[20] A. G. Stove, “Linear FMCW radar techniques,” IEE Proceedings F - Radar and Signal Processing, vol. 139, no. 5, pp. 343–350, 1992.

[21] V. Winkler, “Range Doppler detection for automotive FMCW radars,” in 2007 European Microwave Conference, pp. 1445–1448, Oct. 2007.

[22] X. Glorot, A. Bordes, and Y. Bengio, “Deep sparse rectifier neural networks.,” in AISTATS, vol. 15 of JMLR Proceedings, pp. 315–323, JMLR.org, 2011.

[23] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” CoRR, vol. abs/1412.6980, 2014.

[24] O. Shayer, D. Levi, and E. Fetaya, “Learning discrete weights using the local reparameterization trick,” in International Conference on Learning Representations, 2018.

[25] S. Uhlich, L. Mauch, K. Yoshiyama, F. Cardinaux, J. A. Garcia, S. Tiedemann, T. Kemp, and A. Nakamura, “Differentiable quantization of deep neural networks,” arXiv preprint arXiv:1905.11452, vol. 2, no. 8, 2019.

[26] S. R. Jain, A. Gural, M. Wu, and C. H. Dick, “Trained quantization thresholds for accurate and efficient fixed-point inference of deep neural networks,” 2019.

[27] S. K. Esser, J. L. McKinstry, D. Bablani, R. Appuswamy, and D. S. Modha, “Learned step size quantization,” 2019.

[28] D. P. Kingma, T. Salimans, and M. Welling, “Variational dropout and the local reparameterization trick,” in Advances in Neural Information Processing Systems 28, pp. 2575–2583, Curran Associates, Inc., 2015.

[29] D. Soudry, I. Hubara, and R. Meir, “Expectation backpropagation: Parameter-free training of multilayer neural networks with continuous or discrete weights,” in Advances in Neural Information Processing Systems 27, pp. 963–971, Curran Associates, Inc., 2014.

[30] J. M. Hernandez-Lobato and R. Adams, “Probabilistic backpropagation for scalable learning of bayesian neural networks,” vol. 37 of Proceedings of Machine Learning Research, (Lille, France), pp. 1861–1869, PMLR, 07–09 Jul 2015.

[31] J. W. T. Peters and M. Welling, “Probabilistic binary neural networks,” 2018.

[32] D. P. Kingma, T. Salimans, and M. Welling, “Variational dropout and the local reparameterization trick,” in Advances in Neural Information Processing Systems 28, pp. 2575–2583, Curran Associates, Inc., 2015.

[33] E. Jang, S. Gu, and B. Poole, “Categorical reparameterization with gumbel-softmax,” arXiv preprint arXiv:1611.01144, 2016.

[34] C. J. Maddison, A. Mnih, and Y. W. Teh, “The concrete distribution: A continuous relaxation of discrete random variables,” arXiv preprint arXiv:1611.00712, 2016.

[35] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in 2019 22nd International Conference on Information Fusion (FUSION) (FUSION 2019), 2019.

[36] M. Toth, J. Rock, P. Meissner, A. Melzer, and K. Witrisal, “Analysis of automotive radar interference mitigation for real-world environments,” in European Radar Conference (EURAD), 2020.

[37] L. Scharf and C. Demeure, Statistical Signal Processing: Detection, Estimation, and Time Series Analysis. Addison-Wesley series in electrical and computer engineering, Addison-Wesley Publishing Company, 1991.

[38] A. Pappalardo @ Xilinx Research Labs, “Brevitas - a library for quantization-aware training,” 2020.

[39] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive Radar Interference Mitigation Using a Sparse Sampling Approach,” in 2017 European Radar Conference (EURAD), pp. 90–93, 2017.

[40] S.-W. Fu, T.-y. Hu, Y. Tsao, and X. Lu, “Complex spectrogram enhancement by convolutional neural network with multi-metrics learning,” in 2017 IEEE 27th International Workshop on Machine Learning for Signal Processing (MLSP), pp. 1–6, IEEE, 2017.

![](images/ce67082ec990401458b4a94a581e1ef12b03f9304988d43017df70ce37c0f348.jpg)  
Johanna Rock received her MSc degree in computer science from Graz University of Technology, Austria, in 2018. Currently she is pursuing towards her PhD as a research associate at the Signal Processing and Speech Communication Laboratory at Graz University of Technology. Her main research interests are in the area of machine learning and pattern recognition with a focus on real-world signals, automotive-radar, interference mitigation, target detection, resource-efficient deep learning and uncertainty for robust neural networks.

![](images/d0c9f33cebb0eebcabd533e84f4a24d381d661a50e4621249c08d2ec3504d3d5.jpg)

Wolfgang Roth received his Msc degree in computer science from Graz University of Technology, Austria, in 2015. He is currently a PhD student at the Signal Processing and Speech Communication Laboratory at Graz University of Technology. His research interests include Bayesian inference, deep learning, and resource-efficient models.

![](images/25b9f6ef80c11879b14870440f05a468b1ce5dba51da71f201609366d4b5f1a9.jpg)

Mate Toth received his MSc degree in electrical engineering from Graz University of Technology, Austria, in 2018. He is currently pursuing a PhD at Infineon Technologies Austria in cooperation with Graz University of Technology. His research interests include robust and efficient signal processing for sensors and communication, with a current focus on signal denoising and parameter estimation in automotive radar.

![](images/22221277dc123ef8aea97ce19ae9a22c252578a9ea9ccc35d1b435d78244e375.jpg)

Paul Meissner received his MSc degree in information and communications engineering in 2009 and the PhD degree in electrical engineering in 2014 from Graz University of Technology, respectively. He is currently a concept engineer for automotive radar at Infineon Technologies Austria, focusing on receiver architectures for radar MMICs. His research interests are statistical signal processing, system modeling for complex sensor systems, and data processing algorithms for radar sensors.

![](images/ae3b77e0a5287ff8d8555be626b5cf78ba677764042bd45b013dbac176b644ed.jpg)

Franz Pernkopf received his PhD degree from the University of Leoben in 2002. He was awarded the Erwin Schrodinger Fellowship and was a research¨ associate at the Department of Electrical Engineering at the University of Washington, Seattle, from 2004 to 2006. Since 2010 (Associate) and 2019 (Full) he is a Professor for Intelligent Systems at the Signal Processing and Speech Communication Laboratory at Graz University of Technology, Austria. His research is focused on machine learning and data analysis with a wide range of applications including

signal and speech processing. He is particularly interested in probabilistic graphical models for reasoning under uncertainty, discriminative and hybrid learning paradigms, deep neural networks and sequence modeling.