# RIMformer: An End-to-End Transformer for FMCW Radar Interference Mitigation

Ziang Zhang, Guangzhi Chen, Member, IEEE, Youlong Weng, Shunchuan Yang, Senior Member, IEEE, Zhiyu Jia and Jingxuan Chen

Abstract—Frequency-modulated continuous-wave (FMCW) radar plays a pivotal role in the field of remote sensing. The increasing degree of FMCW radar deployment has increased the mutual interference, which weakens the detection capabilities of radars and threatens reliability and safety of systems. In this paper, a novel FMCW radar interference mitigation (RIM) method, termed as RIMformer, is proposed by using an endto-end Transformer-based structure. In the RIMformer, a dual multi-head self-attention mechanism is proposed to capture the correlations among the distinct distance elements of intermediate frequency (IF) signals. Additionally, an improved convolutional block is integrated to harness the power of convolution for extracting local features. The architecture is designed to process time-domain IF signals in an end-to-end manner, thereby avoiding the need for additional manual data processing steps. The improved decoder structure ensures the parallelization of the network to increase its computational efficiency. Simulation and measurement experiments are carried out to validate the accuracy and effectiveness of the proposed method. The results show that the proposed RIMformer can effectively mitigate interference and restore the target signals.

Index Terms—Deep learning, frequency-modulated continuous-wave (FMCW), radar detection, radar interference mitigation (RIM), Transformer.

## I. INTRODUCTION

W <sup>ITH</sup> <sup>the</sup> <sup>growth</sup> <sup>of</sup> <sup>the</sup> <sup>low</sup> <sup>altitude</sup> <sup>economy</sup> <sup>and</sup> <sup>smart</sup>city development, frequency-modulated continuous- city development, frequency-modulated continuouswave (FMCW) radars are becoming increasingly important. FMCW millimeter-wave (mmWave) radar enhances the reliability of fully autonomous systems, including both unmanned aerial vehicles (UAVs) [1] and unmanned ground vehicles (UGVs) [2]. Compared with optical sensors, mmWave radars can provide accurate distance and velocity information, even under disturbances such as fog, heavy rain, and low lighting conditions [3]. This capability is especially relevant for varieties of remote sensing applications, including height measurement [4], radar imaging [5], environment monitoring [6], [7] and target detection [8], [9]. With the growing adoption of FMCW radars in various transportation modes and ground monitoring stations, the electromagnetic interference among these systems has become a critical concern [10]. As illustrated in Fig. 1, the FMCW radar system discerns targets and obstacles by capturing reflected signals. However, the signals transmitted from other FMCW radar systems cause interference, which can surpass the power level of its own echo signal. Typically, interference in this context tends to raise the noise floor and diminish the visibility of targets. Furthermore, it obscures weak signals, consequently affecting detection capabilities and temporarily creating blind spots. Methods for effectively reducing interference have attracted considerable attention.

![](images/0c472fb9af21e14e307ab94c6f02ca5bb3e80a18ca7bf38b48409fe7c356e3c1.jpg)  
Fig. 1. Demonstration of a scenario where FMCW radar system on an UAV faces potential interference from other radars.

Various studies have been conducted on FMCW radar interference mitigation. Several methods have been proposed to either avoid or suppress interference through system designs. With a new orthogonal noise waveform design method [11], the noise waveform design of a radar system can be transformed into a phase recovery problem. In addition, strategies based on group delay filters [12] and resource allocation methods [13] based on time-frequency-division multiple access (TFDMA) can be used to mitigate vehicular radar interference. Another approach is to establish coordinated programs for different radars. RadarMAC [14] includes a system architecture and a dynamic radar parameter assignment algorithm for mitigating radar interference in self-driving cars.

Other methods for mitigating interference include signal processing methods, which use a series of algorithms to identify and remove interference from radar signals. In [15], a wavelet denoising method was proposed to suppress interference from other vehicle signals in radar systems. The interference signal was extracted from the output of a timedomain low-pass filter via the wavelet transform and thresholding. An adaptive noise canceller (ANC) was designed for radar interference suppression [16]. The interference produced by the attacking radar was cancelled from the main channel using the correlation between the positive and negative half spectra in the frequency domain. In [17], the interfered parts of the beat frequencies within a sweep were suppressed in the short-time Fourier transform (STFT) domain by beat frequency interpolation. An autoregressive (AR) model [18] was used to reconstruct a disturbed baseband signal in the time domain. In addition, empirical mode decomposition (EMD) was used to conduct interference mitigation for the interfered signal [19]. Signal separation [20] was achieved by exploiting the sparsity differences between target signals and interference signals in the tunable Q-factor wavelet transform (TQWT) domain. After converting interference suppression into an optimization problem, robust adaptive beamforming [21] and Hankel matrix decomposition [22] were used to solve the problem. In [23], the RIM was achieved by extracting the target echoes with a row-sparse constraint.

In recent years, deep learning methods have been increasingly applied to FMCW radar interference mitigation tasks and have achieved impressive results. According to the input data, these methods can be divided into time-domain methods and time-frequency-domain methods. Among the former approaches, a gated recurrent unit (GRU) with selfattention [24] was used to reconstruct time-domain signals. In some studies, time-domain signals were subjected to Fourier transforms and converted into two-dimensional data for processing with a convolutional neural network (CNN). A twostage deep neural network (DNN) model with mask-gated convolution [25] was proposed for radar interference detection and mitigation. In [26], a prior-guided method based on a complex-valued CNN was introduced to effectively eliminate interference in the time-frequency domain. In [27], dilated convolution was used to achieve improved interference mitigation performance. Quantization techniques [28] have been investigated to perform CNN-based denoising and interference mitigation on radar signals, resulting in reduced memory requirements. In [29], a feature-oriented unsupervised adaptive suppression network was proposed to adaptively suppress the mutual interference between FMCW radars.

Recently, The Transformer [30] has demonstrated impressive potential in the field of signal processing. This kind of network is particularly adept at capturing repetitive patterns with extended dependencies and is well suited for reconstructing periodic targets from disturbed signals. In this paper, a novel Transformer-based FMCW radar interference mitigation (RIM) method, named as the RIMformer, is proposed to mitigate interference and recover the target signal. The main contributions of this paper are summarized as follows.

1) A Transformer-based architecture is introduced to FMCW radar signal processing, which provides an effective RIM solution. To obviate the need for supplementary radar signal processing steps, the proposed RIMformer is designed with an end-to-end architecture to directly receive and generate

![](images/4966446661ddcbed697fab6f8879a9edcba0807d7c7dd7f8a607bed33513b2e7.jpg)  
Fig. 2. Chirp signals from other FMCW radars that are contained in the same frequency band are received, which cause the pulse-like interference in the time domain.

signals in the time domain.

2) The encoding and decoding components in the RIMformer architecture are improved. Dual multi-head selfattention mechanisms using relative position coding and convolutional enhancement techniques are proposed to improve the performance of the network in terms of capturing features of beneficial components of interfered signals at different scales.

3) Both simulation and measurement experiments are carried out to validate the accuracy and effectiveness of the proposed RIMformer, which exhibits good performance in terms of its interference cancellation and target signal reconstruction capabilities.

This paper is organized as follows. In Section II, the proposed RIMformer for interference mitigation is introduced in detail. Section III contains a series of quantitative comparisons and analyses implemented through simulated experiments. Practical measurements are also carried out to validate the performance of the proposed method in Section IV. Finally, conclusions are drawn in Section V.

## II. METHODOLOGY

## A. FMCW Radar Interference

In an FMCW radar remote sensing system, the received echo signal is mixed with the transmitted signal. Subsequently, low-pass filtering (LPF) is applied to generate an intermediate frequency (IF) signal. The signal passes through an analogto-digital converter (ADC) and subsequent signal processing, which can obtain target parameters such as position, velocity and angle parameters. The transmitted signal in a chirp cycle can be expressed as

![](images/87e719b9057d84818f05cd8c0e99f418a619c542341f01ba96e964233a362165.jpg)  
Fig. 3. The RIMformer adopts a typical encoder-decoder architecture. Within the decoders, the initial signal serves as the query, while the encoding outcome functions are the key and values. The results obtained from the decoders are amalgamated to form the ultimate output, which mirrors the shape of the input time-domain signal. Both the encoders and decoders exhibit identical structures, featuring key components such as dual multi-head self-attention mechanisms, feedforward mechanisms, and convolutional blocks

$$
s _ { \mathrm { T } } \left( t \right) = A _ { \mathrm { T } } \exp { \left\{ j 2 \pi \left( f _ { 0 } t + \frac { K } { 2 } t ^ { 2 } \right) \right\} } , \ 0 < t < T\tag{1}
$$

where $f _ { 0 }$ denotes the start frequency of the transmitted signal, $K = B / T _ { c }$ denotes the frequency modulation (FM) slope of the transmitted signal, B is the effective bandwidth, $T _ { c }$ is the effective time width and $T$ is the time duration of the chirp signal. For each target, the echo signal can be expressed as:

$$
s _ { r } ( t ) = A _ { \mathrm { r } } \exp \left\{ j 2 \pi \left( f _ { 0 } ( t - \tau ) + \frac { K } { 2 } ( t - \tau ) ^ { 2 } \right) \right\}\tag{2}
$$

where τ is the echo delay of the target. Notably, the signal encompasses not only the echo derived from the target under detection but also possibly includes interference signals from radar transmitters. Typically, the chirp slopes of interference signals from other radar systems differ from that of the transmitter. After conducting mixing and LPF, the time-domain expression for the signal with interference $s _ { \mathrm { i n t } } ( t )$ can be derived as follows:

$$
\hat { s } ( t ) = \mathrm { L P F } \left\{ \left[ s _ { r } ( t ) + s _ { \mathrm { i n t } } \left( t \right) \right] \cdot s _ { T } ^ { * } ( t ) \right\}\tag{3}
$$

where the superscript \* denotes the complex conjugate. The expression for the interfered IF signal $\hat { s } _ { \mathrm { I F } } ( t )$ is obtained by summing (3) and the noise $s _ { \mathrm { n } } ( t )$ , which can be expressed as

$$
\hat { s } _ { \mathrm { I F } } ( t ) = \mathrm { L P F } \left\{ s _ { r } ( t ) \cdot s _ { T } ^ { * } ( t ) \right\} + \mathrm { L P F } \left\{ s _ { \mathrm { i n t } } ( t ) \cdot s _ { T } ^ { * } ( t ) \right\} + s _ { \mathrm { n } } \left( t \right)\tag{4}
$$

The interference formation process is illustrated in Fig. 2. After implementing mixing and LPF, the interference produces significant fluctuations in the time domain. $f _ { \mathrm { L P F } }$ is the bandwidth of the filter. $f _ { \mathrm { t a r } }$ is the differential frequency corresponding to the target. $A _ { \mathrm { t a r } }$ and $A _ { \mathrm { i n t } }$ are the amplitudes of the expected and interfered signals, respectively. The immediate consequence of interference is its broad spectrum, which extends across the entirety of the bandwidth. This spectrum broadening effect increases the level of background noise in the signal, diminishes the SINR of the target and even drowns the targets with the small radar cross section (RCS). Such interference significantly impairs the ability of the radar system to detect targets.

## B. The Proposed RIMformer

Due to the exceptional sequence modeling capabilities, Transformer-based methods have been applied across a spectrum of signal processing tasks. The Transformer processes sequences with a self-attention mechanism that allows every element to directly participate in the handling of every other element. This mechanism enables the model to effectively capture long-range dependencies. We are inspired to harness the ability of the Transformer to capture long-range characteristics within time-domain signal sequences and reconstruct the targets from an interfered signal.

We propose the RIMformer based on the encoder-decoder Transformer structure, which is designed specifically for mitigating FMCW radar interference. The overall network framework is illustrated in Fig. 3. The network inputs time-domain signals within a chirp duration with interference from an FMCW radar system and reconstructs the target waveforms. An advantageous aspect of the end-to-end design is its capacity to guide the constructed model from the initial input to the ultimate output. This ability minimizes the of the network reliance on manual preprocessing and postprocessing steps. This approach affords the model great adaptability to the given data and diminishes the challenges associated with manual data processing and parameter acquisition tasks.

![](images/0efe2d634769248b836f16aeddaa894e4d05991f5c6db5a8ffd707b54f59d0ba.jpg)  
Fig. 4. In the dual multi-head self-attention structure, the input data are split into different dimensions according to their inter-frame and intra-frame dimensions. Self-attention is then computed separately. The output is obtained by merging the two attention results and the residual.

In the RIMformer, encoders are employed to perform feature extraction on the input interfered signal, while decoders utilize the encoded information for IF signal reconstruction purposes. As shown in Fig. 3, both the encoder and decoder share a common structure. In contrast to the original Transformer, the initial self-attention block in the decoder is omitted. This decision is grounded in the realization that the interference mitigation task does not necessitate the prediction of future data but focuses solely on restoring the data for the current time step based on contextual information. Consequently, both the encoder and decoder accept the raw data as inputs, thus ensuring the parallelism of the network. The results of the sequence of encoders serve as the key and query inputs in the attention computation of the decoders.

At the beginning of the processing flow of the RIMformer, the input interfered radar IF signal is decomposed into subsegments by a sliding window algorithm. These subsegments are then merged into two-dimensional data. This process is performed to facilitate dual attention calculations, which encompass attention at two different distance scales. After performing channel expansion via a one-dimensional convolution, the interrelationships within the interfered signal are captured by a series of encoders in the feature extraction stage. Upon combining the information derived from the feature map, the interference is removed, and the target is then reconstructed by multiple decoders. In the dual self-attention calculation, relative positional encoding is employed instead of absolute positional encoding. Additionally, the network incorporates supplementary convolutional block layers. This integration step capitalizes on the proficiency of Transformers in terms of capturing long-range relationships and the effectiveness of convolution at extracting localized features. Ultimately, the output of the decoders is consolidated into reconstructed onedimensional signals with the same shape as that of the input radar IF signal.

In the preprocessing stage, the time-domain interfered signal samples acquired in each sweep are partitioned into several subsegments by means of a sliding window algorithm. These subsegments are spliced in new dimensions to generate twodimensional data. The relationship between subsegment y and the input signal samples x can be represented as

$$
\begin{array} { r } { \mathrm { y } _ { k } = x [ k L : ( k + 1 ) L + M ] , k = 0 , 1 , 2 , \ldots , n } \end{array}\tag{5}
$$

where L is the distance of each slide of the window and $L + M$ is the length of a subsegment.

To enhance the ability of the network to capture information across varying distances, we propose a dual multi-head selfattention mechanism. In the context of self-attention, the allocation of weights to each input hinges upon the interactions between the inputs. An internal voting process is performed to ascertain which inputs among them merit attention. After preprocessing, the interfered IF signals of the FMCW radar are converted to a structured format (frame, size, channel). The dual attention computation occurs in two distinct phases. As shown in Fig. 4, the input signals are partitioned by their dimensions, and attention is computed within each frame as well as between frames. Subsequently, the outputs of these two attention mechanisms are amalgamated. The intra-frame attention delineates the pertinence of signals in the short term, while the inter-frame attention encapsulates long-term effects. Moreover, inspired by [31], relative position encoding is used, and the attention expression can be calculated as

$$
\mathrm { A t t e n t i o n } ( Q , K , V ) = \mathrm { s o f t m a x } \left( { \frac { Q K ^ { T } + S ^ { r e l } } { \sqrt { d _ { k } } } } \right) V\tag{6}
$$

![](images/d6743ca8c52c43cf4ecff0617db18cbf74bafce62bf161d4fd2f73acb3f0c605.jpg)  
Fig. 5. Convolutional block and details of the gated linear unit (GLU)

where $S ^ { r e l }$ is a variable representing the relative positions of elements, which can be learned during the training process. The input consists of queries (Q) and keys (K) with $d _ { k }$ dimensions and values (V ) with $d _ { v }$ dimensions. They are calculated by learnable linear transformations, which can be presented as $Q _ { i } = X W _ { i } ^ { Q } , K _ { i } = X W _ { i } ^ { K }$ , and $V _ { i } = X W _ { i } ^ { V }$ where $W ^ { * }$ denotes the parameter matrix. Multi-head attention allows the model to jointly attend to information derived from different representation subspaces at different positions.

$$
\mathrm { M u l t i H e a d } ( Q , K , V ) { = } \mathrm { C o n c a t } \left( \mathrm { h e a d } _ { 1 } , \dots , \mathrm { h e a d } _ { \mathrm { h } } \right) W ^ { O }\tag{7}
$$

where

$$
\mathbf { h e a d } _ { i } { = } \mathrm { A t t e n t i o n } _ { \mathrm { i n t e r } } \left( Q _ { i } , K _ { i } , V _ { i } \right)\tag{8}
$$

The inter-frame multi-head self-attention and intra-frame multi-head self-attention mechanisms are connected by residuals and finally combined via a summation operation.

In the RIMformer, convolution is employed to discern the interrelations among the elements situated in diverse locations within adjacent subsegments. To integrate the local feature utilization proficiency of a CNN with the ability of a Transformer to capture long-distance relationships, we incorporate a convolutional block into both the encoders and decoders. As shown in Fig. 5, inspired by [32], the convolutional block encompasses convolutional layers, linear layers, and various activation functions. Positioned between these two convolutional layers is the gated linear unit (GLU) proposed by [33], where two linear projections of x undergo pointwise multiplication, with one projection initially passing through the Sigmoid function.

$$
\operatorname { G L U } ( X ) = ( X * W + b ) \otimes \sigma ( X * V + c )\tag{9}
$$

At the end of the network, the outputs of the decoders are merged, and the resulting shape is consistent with that of the input signal. This step completes the end-to-end process of reconstructing the IF radar signal. The algorithm can be described as follows:

$$
\tilde { Y } [ k L : ( k + 1 ) L ] = \left\{ \begin{array} { l l } { \frac { 1 } { 2 } \left( y _ { k - 1 } [ L : L + M ] + y _ { k } [ 0 : M ] \right) } \\ { \oplus y _ { k } [ M : L ] , \quad k = 1 , 2 , \ldots , n } \\ { y _ { k } [ 0 : L ] , \quad k = 0 } \end{array} \right.\tag{10}
$$

TABLE I  
SIMULATION PARAMETERS
<table><tr><td>Type</td><td>Parameter</td><td>Vaule</td><td>Parameter</td><td>Value</td></tr><tr><td rowspan="3">Victim</td><td>StartFreq (GHz)</td><td>76.5</td><td>Samples</td><td>1024</td></tr><tr><td>Duration (s)</td><td>20e-6</td><td>Chirps</td><td>128</td></tr><tr><td>Slope (GHz/us)</td><td>0.03</td><td></td><td></td></tr><tr><td rowspan="2">Target</td><td>Number</td><td>(1,3)</td><td>Speed (m/s)</td><td>(3,45)</td></tr><tr><td>Range (m)</td><td>(3,45)</td><td>Amplitude*</td><td>(0.4,3)</td></tr><tr><td rowspan="2">Interference</td><td>Number</td><td>(0,5)</td><td>Slope (GHz/us)</td><td>(-0.0675, 0.0675)</td></tr><tr><td>StartFreq (GHz)</td><td>(76.2, 76.8)</td><td>Amplitude*</td><td>(6,33)</td></tr></table>

The amplitudes are relative values.

where $y _ { k }$ is the decomposed subsegment in the output of the decoder and $\tilde { Y }$ is the merged result. The symbol ⊕ represents the operation of splicing two pieces of data.

Since the commonly used mean squared error (MSE) loss function can only reflect the differences among the predicted signals in the time domain, we propose a hybrid timefrequency loss function. This loss function is formulated to include the errors of the reconstructed signal in both the temporal and frequency domains. The time-domain loss and the frequency-domain loss capture the signal differences over different domains. This allows the network to not only focus on the signal values at a specific point in time but also to optimize the frequency-domain characteristics of the signal. Compared with the MSE loss, the proposed loss function can better represent the physical meaning of the IF signal and is helpful for achieving network convergence. The hybrid timefrequency loss function can be calculated as

$$
\mathcal { L } _ { T \& F } = \frac { 1 - \lambda } { \sqrt { N } } \left\| Y - \widetilde { Y } \right\| _ { 2 } + \frac { \lambda } { \sqrt { N } } \left\| \mathcal { F } ( Y ) - \mathcal { F } ( \widetilde { Y } ) \right\| _ { 2 }\tag{11}
$$

where N is the length of the signal sequence and $\mathcal { F }$ denotes the spectrum of the signal after undergoing a Fourier transformation. λ is a hyperparameter that is used to adjust the weights of the two components and is set to 0.3 based on experience.

## III. NUMERICAL EXPERIMENTS

This section begins by describing the basic configuration of the experiments and the specific details of the training process. Then, ablation experiments are carried out to understand the role of each component in the proposed RIMformer. An exploration of the metric shifts that occur throughout the training process is undertaken to discern the optimal hyperparameters for the developed network. Finally, comparative experiments are conducted to evaluate the performance of our method and various comparative methods on a test dataset.

## A. Experimental Setup

A simulation dataset is constructed with reference to the existing FMCW mmWave radars and possible radar detection scenarios. As Table I demonstrates, multiple interference signal and target factors are considered. The simulated dataset consists of 8,000 pairs of interference and clean samples. The training set, validation set and test set are randomly divided at a ratio of 8:1:1. The number of samples per signal is 1024.

Before training the RIMformer model, data preprocessing is implemented to optimize the learning process of the network. To enhance the numerical stability of the network and expedite its convergence process during training, a normalization step is applied to the input data. The sliding window algorithm is employed to segment the sequences into overlapping windows. The algorithm generates overlapping segments with lengths of 32 through a sliding distance of 16.

In this paper, three performance metrics are employed. First, the MSE serves as an indicator of the accuracy of the network in terms of reconstructing the echo signal. A small MSE implies a heightened degree of time-domain similarity between the reconstructed and original signals. Another metric for reflecting the efficacy of radar interference mitigation is the SINR, which reflects the visibility of the target in the frequency domain. A large SINR denotes improved target recognition. Additionally, considering the real-time requirements of sensors, the processing time required for singleframe data is a pivotal reference indicator for assessing system performance. The SINR is defined as the ratio of the mean power across the target peaks and the mean power of the interference and noise.

$$
\mathrm { S I N R } = 1 0 \log 1 0 \left( \frac { \frac { 1 } { \# \tau } \sum _ { i \in \mathcal { T } } | s [ i ] | ^ { 2 } } { \frac { 1 } { \# \mathcal { N } } \sum _ { i \in \mathcal { N } } | s [ i ] | ^ { 2 } } \right)\tag{12}
$$

where i is the index of the signals $s , \ \mathcal { T }$ is the set of target peaks, N is the set of background noise and noise caused by interference, and $\#$ denotes the cardinality of a set.

The code is implemented using the Python language and the PyTorch framework. The training and inference processes are carried out on an Ubuntu server with an Nvidia RTX 3090 graphics processing unit (GPU). The parameters of the RIMformer model are initialized using the Kaiming initialization method [34]. The adaptive moment estimation (Adam) optimizer [35] is employed to update the model parameters during the training process. The initial learning rate is set to $1 \times 1 0 ^ { 4 }$ . To dynamically adjust the learning rate during the training process, cosine annealing and warm restart [36] functions from the PyTorch library are utilized.

## B. Ablation Studies

The encoder-decoder structure of the RIMformer integrates dual multi-head self-attention and convolution blocks. To better understand the role of each component, ablation experiments are performed to systematically isolate and evaluate the impact of the dual multi-head self-attention mechanism and the convolution blocks. To assess the contribution of the dual multi-head self-attention mechanism to the RIMformer model, this component is replaced with a normal self-attention mechanism. For the convolutional blocks, ablation experiments are conducted by excluding the convolution blocks from the model. To verify the effect of the joint frequency loss, the conventional MSE is used as a loss function for comparison. The model is trained with the same training parameters and evaluated based on the training loss, MSE and SINR.

The results obtained from the experiments are summarized in Table II. After 500 epochs of training, the RIMformer achieves a training loss of 0.014, an MSE of 1.879, and an average SINR of 23.878 dB. When the dual multi-head self-attention mechanism is removed, the performance metrics exhibit notable changes. When the training loss increases to 0.022, the MSE increases to 2.888, and the SINR decreases to 15.924. When the convolution blocks are omitted, the SINR decreases to 22.763 dB. After removing both the dual multihead self-attention mechanism and the convolution blocks, the combined absence of these structures results in a further performance decrease, with the SINR reaching 14.410 dB.

TABLE II  
RESULTS OF ABLATION STUDIES
<table><tr><td>Model</td><td>Epochs</td><td>Training Loss*</td><td>MSE (e-5)*</td><td>Avg SINR (dB)</td></tr><tr><td rowspan="5">RIMformer</td><td>100</td><td>0.036</td><td>4.001</td><td>5.462</td></tr><tr><td>200</td><td>0.024</td><td>2.163</td><td>21.944</td></tr><tr><td>300</td><td>0.016</td><td>2.362</td><td>22.399</td></tr><tr><td>400</td><td>0.015</td><td>2.139</td><td>23.348</td></tr><tr><td>500</td><td>0.014</td><td>1.879</td><td>23.878</td></tr><tr><td rowspan="5">RIMformer - Dual Attention</td><td>100</td><td>0.048</td><td>5.895</td><td>-2.250</td></tr><tr><td>200</td><td>0.035</td><td>3.841</td><td>6.131</td></tr><tr><td>300</td><td>0.029</td><td>3.673</td><td>6.394</td></tr><tr><td>400</td><td>0.023</td><td>3.039</td><td>14.770</td></tr><tr><td>500</td><td>0.022</td><td>2.888</td><td>15.924</td></tr><tr><td rowspan="5">RIMformer - Conv Block</td><td>100</td><td>0.037</td><td>3.984</td><td>4.427</td></tr><tr><td>200</td><td>0.023</td><td>2.154</td><td>21.529</td></tr><tr><td>300</td><td>0.021</td><td>2.098</td><td>21.613</td></tr><tr><td>400</td><td>0.017</td><td>1.882</td><td>22.698</td></tr><tr><td>500</td><td>0.015</td><td>2.014</td><td>22.763</td></tr><tr><td rowspan="5">RIMformer - Dual Attention - Conv Block</td><td>100</td><td>0.034</td><td>3.967</td><td>12.623</td></tr><tr><td>200</td><td>0.026</td><td>3.402</td><td>12.279</td></tr><tr><td>300</td><td>0.024</td><td>3.343</td><td>14.017</td></tr><tr><td>400</td><td>0.021</td><td>3.638</td><td>14.132</td></tr><tr><td>500</td><td>0.020</td><td>3.511</td><td>14.410</td></tr><tr><td rowspan="5">RIMformer - LT&amp;F</td><td>100</td><td></td><td>2.916</td><td>18.226</td></tr><tr><td>200</td><td></td><td>2.394</td><td>19.843</td></tr><tr><td>300</td><td></td><td>1.955</td><td>22.071</td></tr><tr><td>400</td><td></td><td>2.202</td><td>22.057</td></tr><tr><td>500</td><td></td><td>2.717</td><td>20.072</td></tr></table>

To avoid the effect of utilizing the magnitudes of the values, their normalized values are used for the calculations.

The dual multi-head self-attention mechanism plays a crucial role in capturing long-range dependencies and contextual information. The convolution blocks contribute to the ability of the RIMformer to extract local features. A comparative analysis of the ablation experiments confirms that the dual multi-head self-attention mechanism and convolution blocks contribute distinctively to the RIMformer model. Removing each structure causes the observed performance to degrade. When the hybrid time-frequency loss function is replaced with the MSE, the SINR reaches 22.071 dB after 300 epochs of training and then falls to 20.072 dB. These observed decreases in the performance metrics suggest that the new loss function enables the network to learn the information contained in the signal frequencies by employing.

The number N of encoders and decoders in the network is a parameter that is subject to optimization. Comparative experiments are conducted to elucidate the relationship between the interference mitigation effectiveness of the network and the number of training epochs across various layer configurations. The outcomes, including the MSE and SINR produced for the target, are depicted in Fig. 6. The network demonstrates greater training ease with fewer encoders and decoders, converging within the first 200 epochs. As N increases, the predictive accuracy of the network improves. This advancement comes at the cost of requiring more iterations for convergence, and it increases the susceptibility of the model to overfitting. Notably, at $N = 8 ,$ , the network fails to converge even after 500 training rounds, which indicates an underfitted state. This phenomenon demonstrates the tradeoff between network depth and performance. Deeper networks tend to exhibit superior performance at the expense of heightened training complexity, an increased risk of overfitting, and elevated computational demands. The N parameter of the RIMformer is set to 7 to ensure its interference mitigation performance and temporal efficiency. In addition, it can be seen from the figure that a low MSE in the time-domain signal does not necessarily imply a high SINR. therefore MSE cannot be used as the only evaluation metric for network training.

![](images/dce219810875c25f2ebe278f2c35d79df84f881b44d23d309c42727e5ef7a355.jpg)  
Fig. 6. Changes exhibited by the MSE and SINR on the test set with increasing training epochs.

## C. Performance Comparison

To assess the effectiveness of the proposed method, a range of recently proposed techniques, including wavelet denoising [15], ANC [16], an attention-based bidirectional GRU (BiGRU) [24], and a complex-valued CNN [26], are chosen for conducting a comparative analysis. The latter three methods are trained for the same number of epochs based on simulated FMCW radar signals.

To illustrate the interference suppression effects of the tested methods, the results obtained for a simulated signal sample are depicted in both the time domain and the STFT domain in Fig. 7. Within the STFT domain, the spectrum of the target signal component is represented by a horizontal line along the time axis, while a slanted thick line signifies interference. The results show that the wavelet denoising method performs unsatisfactorily in the face of multiple severe interference factors. Due to the design principle of ANC, its T-F results retain the positive frequency part. The time-domain results show that a portion of the interference signal is suppressed. Both the attention-based BiGRU and complex-valued CNN can suppress interference. However, the amplitudes of the target signals are distorted. The proposed RIMformer recovers the target signals more accurately while eliminating the interference.

![](images/0696f64400030665457934ad6427d35dad90dfb7b3f7d97c44be1144463bc14c.jpg)

![](images/23e86390bab3bd888639f6bca711a10da0f6c8181e512692cada3e38a7b88e28.jpg)

![](images/4290cfc1df6b011bdf44feeb92a6070b4d3a5f6dba4ca096a763deba2e282dc8.jpg)

![](images/35b5593e0368b651ae2477deb69608966889f2d6d7056536df3c3526b2b9c22e.jpg)  
(b)

(a)  
![](images/686805f026d8f0be9a70a1ab9471aef4bacfdb38a37a03cef9e85483012f85d9.jpg)

![](images/eec8d26fa800e39c5ccb5e325f12bd8d3d226b89fc42cb486aa85887dab79c57.jpg)

![](images/e504397110fe8928fdb874cf265dc2ad1d12d532fe428e9e33097561826212c8.jpg)  
(c)

![](images/df28d2e4410ec317c5bee1b5bfa6db84be85d5390dd362ff938c701c382739f5.jpg)

![](images/cd35ea8715415386212923a09a61e0225911b3545f0a91d0ba786a7cad4f9de6.jpg)

(d)  
![](images/55c741abe133208be544ead72532f811d77c9335b67529bc369ba473c1bb8726.jpg)

![](images/73dedb17241786b3a61315f584e234c04a7bd7860c337e349798eb8830b47681.jpg)  
(e)

![](images/1f55be55450b2ea881ecb3d25475521fd52dc59787e3e0e16f8d150d1d2ce0b4.jpg)  
(f)  
Fig. 7. Results produced by (a) received signal with interference, (b) wavelet denoising, (c) ANC, (d) attention-based BiGRU, (d) complex-valued CNN and (f) RIMformer for one of the simulated chirps, which are presented in the time and STFT domains.

The results obtained for a set of 128 chirp signals are presented as range-Doppler (RD) maps in Fig. 8. The locations of spikes in the graph correspond to the distance and speed information of the targets in the simulated scenario. The values of the spikes indicate the intensity levels of the target echo. In this scenario, the speeds of the three targets are -7.63 m/s, 0 m/s and 18.31 m/s, while their distances are 3.5 m, 30.5 m and

![](images/b251b59bb7a03bae9e3e835c711a56498ca093a9332962fba322715293b60859.jpg)  
(a)

![](images/41f5ac034ea6ab2921c805f9d5097ba6549334d555ecf83b48abc5a16bbee515.jpg)  
(b)

![](images/c449fb5c00a0866ffc3003bffa71564f4fd233dc8d3a331980e7afa2f1e837ce.jpg)  
(c)

![](images/6c37066b3b6997d5f520d79e7dc1b874769c7b4cad05778097c738cf251d46f8.jpg)  
(d)

![](images/6f6cdf7973c316ab7cfab10262bffa84f4a777178b604d4ac46f3f2f713a6371.jpg)  
(e)

![](images/f783798d611907b0add8eae7588e1938562caa149db13e022409a3a91a396aff.jpg)  
(f)  
Fig. 8. Results produced by (a) signal with interference, (b) wavelet denoising, (c) ANC, (d) attention-based BiGRU, (d) complex-valued CNN, and (f) the proposed RIMformer on a set of 128 simulated chirps, presented as RD maps.

![](images/d9db5064f48d8d59dc586080b0854ced226e0fc14aa650ff100f0f712bafaa14.jpg)  
Fig. 9. The target SINRs of different methods, including wavelet denoising, ANC, attention-based BiGRU, complex-valued CNN, the proposed RIMformer and the base signal without interference. Each point represents the target SINR of the interference mitigation result produced for one set of test data.

16.7 m. A comparative analysis with different methods shows that the complex-valued CNN and the proposed RIMformer can achieve higher peaks and lower noise floors than those of the other approaches. The RIMformer is able to restore all three targets with an average amplitude of -18.36 dB, as shown in Fig. 8 (f).

The results of the comparison conducted on the whole test set are represented as a scatter plot in Fig. 9. The horizontal and vertical coordinates represent the SINRs of the target in the input signal and the output results, respectively. Each point signifies the outcome produced for a single test sample after implementing interference mitigation, with the different methods distinguished by color. The greater proximity of a result on the plot to the clean signal indicates superior interference suppression. As illustrated in the figure, the proposed RIMformer obtains greater SINR values for the targets than do the four other methods.

TABLE III  
COMPARISON AMONG THE RESULTS PRODUCED BY DIFFERENT METHODS
<table><tr><td>Method</td><td>Avg SINR↑</td><td>Mid SINR↑</td><td>Time ↓</td></tr><tr><td>Wavelet Denoising [15]</td><td>9.13 dB</td><td>10.04 dB</td><td>1.28 ms</td></tr><tr><td>ANC [16]</td><td>10.24 dB</td><td>10.61 dB</td><td>1.14 ms</td></tr><tr><td>Attention BiGRU [24]</td><td>20.68 dB</td><td>21.32 dB</td><td>211.16 ms</td></tr><tr><td>Complex-Valued CNN [26]</td><td>21.49 dB</td><td>22.67 dB</td><td>6.83 ms</td></tr><tr><td>RIMformer (N=5)</td><td>23.12 dB</td><td>23.69 dB</td><td>14.46 ms</td></tr><tr><td>RIMformer (N=7)</td><td>24.25 dB</td><td>24.84 dB</td><td>19.37 ms</td></tr></table>

Table III presents the numerical results of various methods and their corresponding processing times. Three variations of the RIMformer, each with different numbers of encoders and decoders, are compared. In line with our previous findings, a larger N parameter leads to superior results. With $N = 7$ the RIMformer yields better results than those of the other comparison methods. In comparison with the network utilizing $N = 5 ,$ , the incorporation of two additional encoders and decoders enhances the average SINR by 1.13 dB and introduces a time overhead of 4.91 ms. Compared with those of wavelet denoising, ANC, the attention-based BiGRU, and the complex-valued CNN, the average SINR of the proposed approach is 15.12 dB, 14.01 dB, 3.57 dB and 2.76 dB greater, respectively. The numerical SINR results validate the performance of the proposed RIMformer method in terms of mitigating interference in FMCW radar systems.

![](images/9077bea6669df79cdc16bdfa4e32a9a6eb7696775bfb097b84d1df866989fd98.jpg)  
(a)

![](images/507ecef527554693311e203673f9ad0be7f9f64c649bd075b4abe481d9e8a053.jpg)  
(b)

![](images/84076e12c2735d84cafe0c133dd51c753de5b96fe53d437dfb21446308c881a7.jpg)  
(c)

![](images/3d01cef8141d267fe63db99fcbc52bfb280146808dd206d75be089d39b36b627.jpg)  
(d)

![](images/92985a19ce86e0d01de37ea23bc0b9bd594147348868abaa7226f61f7e797c41.jpg)  
(e)  
Fig. 10. CFAR detection results and spectrograms of the outputs obtained from (a) wavelet denoising, (b) ANC, (c) attention-based BiGRU, (d) complex-valued CNN, and (e) RIMformer on measured data.

![](images/a1d3eb8ed7c67fe8a272097a087bc7d7a3d9e2782ade641c0fef82349d5fa76e.jpg)  
Fig. 11. Scenario of the measured experiment. The radar marked with a yellow circle in the bottom-right corner is the victim, while those marked with red circles are the interference sources.

## IV. MEASUREMENTS

In this section, a measurement experiment is conducted to obtain data for validating the effectiveness of the proposed method in real-world scenarios. In the experiment, one FMCW mmWave radar serves as the victim, while the two other radars act as sources of interference. The experimental setup is illustrated in Fig. 11, where a nearby corner reflector and a distant car serve as the targets. The other two mmWave radars are positioned at the same locations as those of the targets, thus representing the radars equipped on the vehicle. The two targets are situated approximately 3 m and 10 m away from the receiving radar. The key parameters of both the victim and interference radars are detailed in Table IV. The start frequencies of these radars are maintained at 77 GHz, with slope variations adjusted to 24 MHz/µs, 10 MHz/µs and 25 MHz/µs. The interference radars with slopes similar to those of the victim radar generate blur with an extended time span, while the interference radar with substantial slope differences produces high-amplitude spikes.

TABLE IV  
PARAMETERS OF THE RADARS
<table><tr><td>Parameter</td><td>Victim</td><td>Interference 1</td><td>Interference 2</td></tr><tr><td>Start Frequency (GHz)</td><td>77.0</td><td>77.0</td><td>77.0</td></tr><tr><td>Frequency Slope (MHz/μs)</td><td>23.995</td><td>9.994</td><td>25.0</td></tr><tr><td>Chirps per Frame</td><td>128</td><td>128</td><td>32</td></tr><tr><td>Frame Periodicity (ms)</td><td>5.0</td><td>10.0</td><td>100.0</td></tr><tr><td>ADC Samples</td><td>1024</td><td></td><td></td></tr><tr><td>Sampling Rate (ksps)</td><td>40000</td><td></td><td></td></tr></table>

The Fourier transform results of the outputs generated by the various methods are depicted in Fig. 10. It is evident that wavelet denoising exhibits a suboptimal recovery effect for the first target. Although the ANC method successfully recovers the nearest target, it introduces an offset for the second target, and the noise level at the far end of the spectrum remains elevated. The SINRs of the first two methods are relatively small. The BiGRU with attention yields a spurious spike between the two targets and induces an error when estimating the target distance. The complex-valued CNN introduces a significant bias when reducing the magnitude of the first target. In contrast, the RIMformer demonstrates better performance than that of the other methods in terms of restoring the targets.

To further evaluate the quality of the signals restored by the five interference mitigation methods, the target detection performance of the constructed ranging profiles is tested using the same constant false-alarm rate (CFAR) detector. Empirically, the threshold factor of the detector is set to 0.82. In addition to the resulting spectra yielded by the various methods, the results of the CFAR detector are also displayed in Fig. 10. All five methods detect one or more targets after employing RIM. Wavelet denoising detects the distant vehicle. The ANC method only detects the angle reflector at a close distance due to its high noise floor. The BiGRU method produces an incorrect target judgment. In contrast, the complex-valued CNN and RIMformer are able to correctly recognize all the targets and yield higher target detection probabilities. Moreover, the spectrogram produced by the RIMformer closely approximates the clean signal and reproduces the most accurate amplitude for the target. The difference between the predicted and real peaks is 1.21 dB. The experimental results obtained on measurement data and in a comparative analysis demonstrate the effectiveness of the RIMformer in real-world FMCW radar interference scenarios. The RIMformer preserves the integrity of the target signal while minimizing the amplitude distortion effect.

## V. CONCLUSION

This paper introduces the RIMformer, a Transformer-based approach that is designed to mitigate interference from FMCW radar systems. The RIMformer seamlessly processes timedomain signals in an end-to-end manner, which eliminates the need for supplementary data processing or manual parameter tuning steps. By applying a dual multi-head selfattention mechanism, the RIMformer effectively captures the correlations among signal elements at different distances. The introduction of convolutional blocks allows the network to better extract localized features. A hybrid time-frequency loss function is proposed to learn the physical meaning of the target signal in the frequency domain. Through parameter optimization, the RIMformer strikes a balance between performance and computational efficiency. To validate the efficacy of the RIMformer, comprehensive comparisons are conducted with existing advanced methods. Both simulated and measured data are employed. The results demonstrate the superiority of the RIMformer in terms of suppressing interference and restoring the target signal.

## VI. ACKNOWLEDGMENTS

The authors would like to thank Aoyong Dong, Lixiang He and Zhanhai He from the Hefei Innovation Research Institute of Beihang University for providing suggestions and help during the experiments.

## REFERENCES

[1] L. R. Cenkeramaddi et al., ”A Novel Angle Estimation for mmWave FMCW Radars Using Machine Learning,” IEEE Sensors Journal, vol. 21, no. 8, pp. 9833-9843, 15 April15, 2021.

[2] S. Sun and Y. D. Zhang, ”4D automotive radar sensing for autonomous vehicles: A sparsity-oriented approach”, IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 879-891, Jun. 2021.

[3] G. Hakobyan and B. Yang, ”High-performance automotive radar: A review of signal processing algorithms and modulation schemes”, IEEE Signal Process. Mag., vol. 36, no. 5, pp. 32-44, Sep. 2019.

[4] Awan, M.A., Dalveren, Y., Kara, A., Derawi, M., ”Towards mmWave Altimetry for UAS: Exploring the Potential of 77 GHz Automotive Radars,” Drones. vol. 8, no. 3, pp. 94, 2024.

[5] S. Wei et al., ”Nonline-of-Sight 3-D Imaging Using Millimeter-Wave Radar,” IEEE Trans. Geosci. Remote Sens., vol. 60, pp. 1-18, 2022.

[6] S. Ayhan et al., ”Millimeter-Wave Radar Sensor for Snow Height Measurements,” IEEE Trans. Geosci. Remote Sens., vol. 55, no. 2, pp. 854- 861, Feb. 2017.

[7] G. Ludeno, I. Catapano, F. Soldovieri and G. Gennarelli, ”Retrieval of Sea Surface Currents and Directional Wave Spectra by 24 GHz FMCW MIMO Radar,” IEEE Trans. Geosci. Remote Sens., vol. 61, pp. 1-13, 2023

[8] E. Tavanti, A. Rizik, A. Fedeli, D. D. Caviglia and A. Randazzo, ”A Short-Range FMCW Radar-Based Approach for Multi-Target Human-Vehicle Detection,” IEEE Trans. Geosci. Remote Sens., vol. 60, pp. 1-16, 2022.

[9] X. Fang, J. Zhu, D. Huang, Z. Zhang and G. Xiao, ”E2DTF: An End-to-End Detection and Tracking Framework for Multiple Micro-UAVs With FMCW-MIMO Radar,” IEEE Trans. Geosci. Remote Sens., vol. 61, pp. 1-16, 2023.

[10] S. Alland, W. Stark, M. Ali and M. Hegde, ”Interference in automotive radar systems: Characteristics mitigation techniques and current and future research”, IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45-59, Sep. 2019.

[11] Z. Xu and Q. Shi, ”Interference Mitigation for Automotive Radar Using Orthogonal Noise Waveforms,” IEEE Geosci. Remote Sens. Lett., vol. 15, no. 1, pp. 137-141, Jan. 2018.

[12] F. Uysal, ”Phase-coded FMCW automotive radar: System design and interference mitigation,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 270–281, Jan. 2020.

[13] Y. Wang, Q. Zhang, Z. Wei, Y. Lin and Z. Feng, ”Performance Analysis of Coordinated Interference Mitigation Approach for Automotive Radar,” IEEE Internet Things J., vol. 10, no. 13, pp. 11683-11695, Jul. 2023.

[14] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith and T. Campbell, ”RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens. Commun. Netw., pp. 1-9, Jun. 2016.

[15] Lee S, Lee J Y, Kim S C., ”Mutual interference suppression using wavelet denoising in automotive FMCW radar systems,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 2, pp. 887-897, Feb. 2021.

[16] F. Jin and S. Cao, ”Automotive Radar Interference Mitigation Using Adaptive Noise Canceller,” IEEE Trans. Veh. Technol., vol. 68, no. 4, pp. 3747-3754, Apr. 2019.

[17] S. Neemat, O. Krasnov, and A. Yarovoy, ”An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Trans. Microw. Theory Techn., vol. 67, no. 3, pp. 1207-1220, Mar. 2018.

[18] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors J., vol. 21, no. 5, pp. 6575–6586, Mar. 2021.

[19] Z. Liu, J. Wu, S. Yang and W. Lu, ”DOA Estimation Method Based on EMD and MUSIC for Mutual Interference in FMCW Automotive Radars,” IEEE Geosci. Remote Sens. Lett., vol. 19, pp. 1-5, 2022.

[20] Z. Xu, M. Yuan, ”An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain”. IEEE Trans. Microwave Theory Tech., vol. 69, no. 12, pp. 5269- 5283, Dec. 2021.

[21] X. Zhang, W. Jiang, K. Huo, Y. Liu, and X. Li, “Robust adaptive beamforming based on linearly modified atomic-norm minimization with target contaminated data.” IEEE Trans. Signal Process. , vol. 68, 2020.

[22] J. Wang, M. Ding and A. Yarovoy, ”Interference Mitigation for FMCW Radar With Sparse and Low-Rank Hankel Matrix Decomposition,” IEEE Trans. Signal Process., vol. 70, pp. 822-834, 2022.

[23] Y. Wang, Y. Huang, C. Wen, X. Zhou, J. Liu and W. Hong, ”Mutual Interference Mitigation for Automotive FMCW Radar With Time and Frequency Domain Decomposition,” IEEE Trans. Microwave Theory Tech., vol. 71, no. 11, pp. 5028-5044, Nov. 2023.

[24] J. Mun, S. Ha and J. Lee, ”Automotive Radar Signal Interference Mitigation Using RNN with Self Attention,”. in Proc. IEEE Int. Conf. Acoust. Speech Signal Process. (ICASSP), pp. 3802-3806, 2020.

[25] S. Chen, J. Taghia, U. Kuhnau, N. Pohl and R. Martin, ”A Two-¨ Stage DNN Model With Mask-Gated Convolution for Automotive Radar

Interference Detection and Mitigation,” IEEE Sensors J., vol. 22, no. 12, pp. 12017-12027, Jun. 2022.

[26] J. Wang, R. Li, Y. He and Y. Yang, ”Prior-Guided Deep Interference Mitigation for FMCW Radars,” IEEE Trans. Geosci. Remote Sens., vol. 60, pp. 1-16, 2022.

[27] J. Wang, R. Li, X. Zhang and Y. He, ”Interference Mitigation for Automotive FMCW Radar Based on Contrastive Learning With Dilated Convolution”, IEEE Trans. Intell. Transp. Syst., vol. 25, no. 1, pp. 545- 558, Jan. 2024.

[28] J. Rock, W. Roth, M. Toth, P. Meissner and F. Pernkopf, ”Resource-Efficient Deep Neural Networks for Automotive Radar Interference Mitigation,” IEEE J. Sel. Top. Signal Process., vol. 15, no. 4, pp. 927-940, Jun. 2021.

[29] H. Zhang, S. Wei, M. Wang, Y. Hu, J. Shi and G. Cui, ”FUAS-Net: Feature-Oriented Unsupervised Network for FMCW Radar Interference Suppression”, IEEE Trans. Microw Theory Techn., vol. 72, no. 4, pp. 2602-2619, Apr. 2024.

[30] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin., ”Attention is All You Need”, in Adv. Neural Inf. Process. Syst., pp. 30-40, 2017.

[31] Shaw, Peter, Jakob Uszkoreit, and Ashish Vaswani. ”Self-Attention with Relative Position Representations.” in Proc. NAACL-HLT, pp. 464-468, 2018.

[32] A. Gulati, J. Qin, C.-C. Chiu, N. Parmar, Y. Zhang, J. Yu, W. Han, S. Wang, Z. Zhang, Y. Wu et al. ”Conformer: Convolution-augmented Transformer for Speech Recognition”, in Proc. Interspeech, pp. 5036- 5040, 2020.

[33] Dauphin, Y. N., Fan, A., Auli, M., and Grangier, D. ”Language modeling with gated convolutional networks”, in Int. Conf. Mach. Learn., pp. 933- 941, 2017.

[34] K. He, X. Zhang, S. Ren and J. Sun, ”Delving deep into rectifiers: Surpassing human-level performance on ImageNet classification”, in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), pp. 1026-1034, Dec. 2015.

[35] D. P. Kingma, J. Ba, ”Adam: A method for stochastic optimization”, in Proc. Int. Conf. Learn. Represent. (ICLR), 2015.

[36] I. Loshchilov, F. Hutter. “Sgdr: Stochastic gradient descent with warm restarts”, in Proc. Int. Conf. Learn. Represent. (ICLR), 2017.