# Angle-Equivariant Convolutional Neural Networks for Interference Mitigation in Automotive Radar

Christian Oswald<sup>#1</sup>, Mate Toth<sup>#2</sup>, Paul Meissner<sup>\*3</sup>, Franz Pernkopf<sup>#4</sup>

<sup>#</sup>Signal Processing and Speech Communication Laboratory, Graz University of Technology, Austria <sup>\*</sup>Infineon Technologies AG, Graz, Austria

{<sup>1</sup>christian.oswald, <sup>2</sup>mate.a.toth, <sup>4</sup>pernkopf}@tugraz.at, <sup>3</sup>paul.meissner@infineon.com

Abstract — In automotive applications, frequency modulated continuous wave (FMCW) radar is an established technology to determine the distance, velocity and angle of objects in the vicinity of the vehicle. The quality of predictions might be seriously impaired if mutual interference between radar sensors occurs. Previous work processes data from the entire receiver array in parallel to increase interference mitigation quality using neural networks (NNs). However, these architectures do not generalize well across different angles of arrival (AoAs) of interferences and objects. In this paper we introduce fully convolutional neural network (CNN) with rank-three convolutions which is able to transfer learned patterns between different AoAs. Our proposed architecture outperforms previous work while having higher robustness and a lower number of trainable parameters. We evaluate our network on a diverse data set and demonstrate its angle equivariance.

Keywords — FMCW radar, convolutional neural networks, interference mitigation, angle-equivariance, deep learning, complex-valued processing

## I. INTRODUCTION

FMCW radar operates by continuously transmitting a frequency modulated signal, which is subsequently reflected off objects. Demodulating the received with the transmitted[ signal allows the sensor to determine the range and velocity of these objects. Furthermore, multiple receive antennas can be used to estimate the angle of objects. However, FMCW radar mutual interference may occur if an interferer radar emits a frequency that is sufficiently close to the ego radar’s frequency. In that case, interference appears as short bursts in the sensor’s output which can strongly deteriorate detection performance. A more detailed description of mutual interference in FMCW radar can be found in [1].

Some methods for interference mitigation such as frequency hopping [2] try to avoid the occurrence of interference all-together, while others aim to remove interference patterns from an already corrupted signal. Examples include setting corrupted samples to zero [3], nonlinear filtering across frequency ramps [4], and iterative adaptive thresholding (IMAT) [5]. In recent years, the problem of interference mitigation has also been tackled with machine learning. Recurrent neural network architectures such as gated recurrent units can be used on the time-domain signal [6], [7], where the latter is augmented with self-attention blocks. Reference [8] applies a CNN to denoise the range-Doppler (RD) map of a single antenna, where they use two separate input and output channels for the RD-map’s real and imaginary part. In [9] this architecture was further optimized towards resource-efficency and has subsequently been implemented on an FPGA [10]. Other possible architectures for processing in the RD-domain include convolutional autoencoders [11], [12]. The fully convolutional architecture described in [13] transforms its input given as a spectrogram into an interference mitigated range-profile. In [14] a combination of an autoencoder with a traditional interference detection filter is proposed. A complex-valued CNN, which processes the entire receiver array simultaneously to improve interference mitigation quality is introduced in [15].

![](images/f2fd4da4c837d33fd4776f3a1df2523cb80f49de128e390c45a1f331eeb61167.jpg)  
Fig. 1. Location of the proposed CCNN-3D in the digital signal processing chain. We denote the interfered multi-channel time domain signal as $s _ { I } .$ Its Fourier transform $S _ { I }$ and the NN’s prediction $\hat { S } _ { C }$ are rank-three tensors with dimensions $\left[ N _ { R } , N _ { D } , N _ { \theta } \right]$ , where $\bar { N } _ { R }$ is the number of samples per frequency modulation (FM) sweeps, $\mathrm { \bar { \it { N } } } _ { D }$ the number of FM sweeps and $\bar { N _ { \theta } }$ the number of angle-bins.

## II. ANGLE-EQUIVARIANT CNNS

We first review the two-dimensional complex-valued convolutional neural network (CCNN-2D) introduced in [15] and then use it as baseline to introduce our model. CCNN-2D consists of layers of complex-valued convolution kernels, activations and batch-normalization, and is applied to interfered multi-antenna FMCW radar data. More specifically, the inputs for the network are the two-dimensional Fourier transforms of the antennas’ signals, the so-called range-Doppler (RD) maps. Each of the $N _ { A }$ antenna’s RD-map is treated as an individual two-dimensional complex-valued input channel for the network, which means that convolutions are performed along the range and Doppler dimension of the input. The network is then trained to perform a regression from $N _ { A }$ interfered to $N _ { A }$ clean RD-maps in a supervised manner, which means that the inputs and targets are identical except for the presence of interferences.

The novel architecture presented in this paper labelled CCNN-3D is an extension of CCNN-2D and is depicted in Fig. 3. We replace the input/target tuples of multi-channel RD-maps $S _ { R D } [ r , d , a ]$ by a single-channel range-Doppler-angle (RDA) map $S [ r , d , \theta ]$ . An RDA-map is obtained by a third DFT over the antenna dimension of the multi-antenna RD-maps. An exemplary data sample used to train CCNN-3D can be seen in Fig. 2, where we have performed a non-coherent summation over all Doppler bins. The placement of CCNN-3D in the overall processing chain is visualized in Fig. 1. The main advantage of representing the radar’s signal as RDA-maps is that they capture the locality of interferences in the angle dimension. If the ego radar is interfered by another radar from an angle $\theta _ { 0 }$ , most of the interference’s energy is located around the RDA-map’s angle-bins corresponding to $\theta _ { 0 }$ and $- \theta _ { 0 }$ [16]. Furthermore, shifting an interference’s AoA results in a shifted interference pattern in the RDA-map’s angle dimension. These properties of locality and similarity can be leveraged by using convolutions in the angle dimension, resulting in rank-three convolution kernels. CCNN-3D does not use fully connected or pooling layers, i.e., shift-equivariance can be guaranteed in all three dimensions. Therefore, CCNN-3D is shift-equivariant w.r.t. the angle in addition to CCNN-2D’s shift-equivariance w.r.t. to range and Doppler. In general, the convolution operator is shift-equivariant as $W * \nu ( x ) = \nu ( W * x )$ , where x is a signal, ν is the shift operator and W is the convolution kernel. CCNN-2D can be viewed as being fully-connected w.r.t. the antenna dimension; Replacing rank-two with rank-three convolutions therefore also strongly reduces the model’s number of parameters. The convolution’s stride is always one and the input to each convolution kernel is zero-padded such that the convolution output has the same size as the input. As all activations are now rank-three, we replace rank-two complex-valued ReLU and batch-normalization by their rank-three variants. Note that the exact same architecture can be used for varying input sizes, as CCNN-3D operates independently from the input’s number of range, Doppler and angle bins. If the used radar sensor measures both azimuth and elevation, all rank-three operations can be extended to their rank-four counterparts to perform interference mitigation on range-Doppler-azimuth-elevation maps in an analogous manner.

## III. EXPERIMENTAL SETUP

In this section, we compare the proposed CCNN-3D to other interference mitigation methods, namely CCNN-2D [15], zeroing [3], ramp-filtering [4] and IMAT [5].

## A. Data Set

The targets of our data set consist of real-world inner-city measurements. We then generate and add artificial interferences to these targets, which are used as input to the CCNNs. We generate artificial interference FMCW signals by sampling uniformly from a range of radar parameters such as sweep duration (12 µs to 24 µs), sweep bandwidth (0,15 GHz to 0,25 GHz), AoA $( - 9 0 ^ { \circ } \ \mathrm { t o } \ 9 0 ^ { \circ } )$ , sweep starting frequency (78,9 GHz to 79,1 GHz), number of sweeps (100 to 156), signal-plus-noise-to-interference ratio (30 dB to 50 dB), and number of interferers (1 to 3). One sample consists of 96 range, 96 Doppler and 16 angle bins, i.e., one sample is a rank-three tensor with dimensions [96, 96, 16]. The data is subsequently split into a training, test and validation set with size 2500, 250 and 250, respectively.

![](images/1084bdc4e0ab3ccd8e03c062675e49e6e2f43f4edd86c7134fef5f52bff444cc.jpg)

![](images/100258f1d05c4546fcba0c4ca6b04013c344eabe235733960d80d45a70856d7d.jpg)

![](images/593500bf91bbc202901b5738ff3c1a9e9b4c0b63c2132a87722befa38556ea31.jpg)  
Fig. 2. Exemplary data sample used to train the proposed CCNN-3D, depicted as range-angle maps. The top map depicts a clean sample, where object locations are visible as peaks. Clean samples are used as optimization targets during training. The middle map shows the same sample corrupted by an interference impending from roughly 45 degrees, masking the objects. Interfered samples are used as input for CCNN-3D. The bottom map shows the CCNN-3D’s prediction for the middle map. We have up-sampled the plots angle resolution for better interpretability; Note that no such up-sampling is needed when feeding RDA-maps to CCNN-3D. Each map is scaled such that its maximum value is zero dB.

## B. Evaluation Metrics

As FMCW radar sensors are primarily used for object detection, we run a cell averaging-constant false alarm rate (CA-CFAR) detector [17] on the network’s output to verify that objects are no longer masked by interferences. We compute a non-coherent sum over the antenna dimension of a multi-antenna RD-map $S _ { R D } [ r , d , a ]$ or equivalently over the angle dimension of an RDA-map $S [ r , d , \theta ]$ before feeding data into the CA-CFAR detector. The CA-CFAR detector therefore returns a rank-two binary object map.

## 1) F1-score

The object map computed from the CCNN’s output can be compared to the clean sample’s object map using the F1-score, which is defined as

$$
F _ { 1 } = 2 \cdot \frac { N _ { T P } } { N _ { T P } + \frac { 1 } { 2 } ( N _ { F P } + N _ { F N } ) } ,\tag{1}
$$

![](images/647f4e58f2a421c319728b192c95616e06cad77eaf54852c9e1547c2343536c0.jpg)  
Fig. 3. Overview of the proposed structure. The network’s input, output and activations consist of $N _ { R }$ range, $N _ { D }$ doppler and $N _ { \theta }$ angle-bins, and convolution kernels have size $[ K _ { R } , \dot { K } _ { D } , \dot { K } _ { \theta } ]$

where the number of true positives $N _ { T P }$ , false positives $N _ { F P }$ and false negatives $N _ { F N }$ are obtained by element-wise comparison of the object maps. For the computation of the F1-score we only keep the peaks of detected object clusters to account for extended objects.

## 2) Error Vector Magnitude (EVM)

We use the EVM to gauge the deviation of the predicted multi-antenna RD-maps $\scriptstyle { \ddot { S } } _ { R D , C }$ from the ground-truth maps $S _ { R D , C }$ at ground-truth object peak locations. It can be computed as

$$
\mathbf { E V M } = \frac { 1 } { N _ { A } N _ { \mathcal { O } } } \sum _ { a } \sum _ { \left\{ r , d \right\} \in \mathcal { O } } \frac { | S _ { R D , C } [ r , d , a ] - \hat { S } _ { R D , C } [ r , d , a ] | } { | S _ { R D , C } [ r , d , a ] | }\tag{2}
$$

Where $N _ { A }$ is the number of antennas $a , \mathcal { O }$ is the set of ground truth object peaks, given by their location coordinates r and d and $N _ { \mathcal { O } }$ is the number of object peaks in an object map.

## 3) Peak Phase Mean Squared Error (PPMSE)

The PPMSE is a measure of difference between the predicted and the ground-truth RD-maps’ phase, evaluated at ground-truth object peak locations. It is given by

$$
\Delta [ r , d , a ] = | \angle \hat { S } _ { R D , C } [ r , d , a ] - \angle S _ { R D , C } [ r , d , a ] | ,\tag{3}
$$

$$
\mathrm { P P M S E } = \frac { 1 } { N _ { A } N _ { \mathscr { O } } } { \sum _ { a } \sum _ { \{ r , d \} \in \mathscr { O } } \operatorname* { m i n } } ( \Delta [ r , d , a ] , 2 \pi - \Delta [ r , d , a ] ) ^ { 2 } .\tag{4}
$$

Note that we need to perform an inverse DFT on CCNN-3D’s output to evaluate the EVM and the PPMSE, since CCNN-3D outputs RDA-maps.

## C. Evaluated Architectures & Training Setup

We evaluate four instantiations of CCNN-3D which differ by the number and width of layers. All variants of CCNN-3D use kernels with size [3, 3, 3]. We also train one variant of CCNN-2D with kernel size [3, 3], which has been shown to perform well in experiments conducted in [15]. The evaluated CCNNs are summarized in Table 1. We omit batch-normalization in the first layer on all CCNNs as it does not seem to improve performance.

Table 1. Evaluated architectures. The number of channels of the n-th layer is given as the n-th element in the list.
<table><tr><td rowspan=1 colspan=1>Name</td><td rowspan=1 colspan=1>Structure</td><td rowspan=1 colspan=1>#Parameters</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-1</td><td rowspan=1 colspan=1>[32, 16, 8, 4, 1]</td><td rowspan=1 colspan=1>38494</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-m</td><td rowspan=1 colspan=1>[16, 8, 4, 2, 1]</td><td rowspan=1 colspan=1>10176</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-s</td><td rowspan=1 colspan=1>[8, 4, 2, 1]</td><td rowspan=1 colspan=1>2760</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-xs</td><td rowspan=1 colspan=1>[4, 2, 1]</td><td rowspan=1 colspan=1>780</td></tr><tr><td rowspan=1 colspan=1>CCNN-2D</td><td rowspan=1 colspan=1>[32, 16, 16]</td><td rowspan=1 colspan=1>23152</td></tr></table>

We trained all CCNNs using a batch-size of 8 with a decaying learning rate for a maximum of 100 epochs. We use ADAM to minimize the mean squared error (MSE) and perform early stopping w.r.t. the validation MSE. To make results comparable, we do not perform windowing before the DFT over the antenna dimension when feeding data into CCNN-3D.

## IV. EXPERIMENTS

We evaluate our proposed CCNN-3D on the data set described in Section III-A and compare it to CCNN-2D [15] as well as classical signal processing methods. As shown in Table 2, CCNN-3D leads to a higher F1-score than other methods, which indicates that its output is the most suitable for subsequent object detection. Interestingly, this performance gap vanishes when comparing the EVM and PPMSE. We hypothesize that CCNN also suppresses noise in addition to interferences and only keeps objects in its prediction, but further research is necessary to validate this interpretation.

CCNN-3D-m and CCNN-3D-s only perform slightly worse than CCNN-3D-l while requiring a fraction of computational costs and trainable parameters. Even though CCNN-3D-xs has fewer parameters than CCNN-2D, memory requirements increase, as activations are rank-three instead of rank-two tensors. Consequently, the number of floating point operations required to process these intermediate values also grows.

Table 2. Performance after training on the data set described in Section III-A.
<table><tr><td rowspan=1 colspan=1>Mitigation Technique</td><td rowspan=1 colspan=1>F1</td><td rowspan=1 colspan=1>EVM</td><td rowspan=1 colspan=1>PPMSE</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-1 (ours)</td><td rowspan=1 colspan=1>0.9673</td><td rowspan=1 colspan=1>0.5028</td><td rowspan=1 colspan=1>0.3352</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-m (ours)</td><td rowspan=1 colspan=1>0.9595</td><td rowspan=1 colspan=1>0.6153</td><td rowspan=1 colspan=1>0.4174</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-s (ours)</td><td rowspan=1 colspan=1>0.9460</td><td rowspan=1 colspan=1>0.8232</td><td rowspan=1 colspan=1>0.5407</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-xs (ours)</td><td rowspan=1 colspan=1>0.9151</td><td rowspan=1 colspan=1>0.9686</td><td rowspan=1 colspan=1>0.6464</td></tr><tr><td rowspan=1 colspan=1>CCNN-2D [15]</td><td rowspan=1 colspan=1>0.8351</td><td rowspan=1 colspan=1>1.1766</td><td rowspan=1 colspan=1>0.7767</td></tr><tr><td rowspan=1 colspan=1>Zeroing [3]</td><td rowspan=1 colspan=1>0.7635</td><td rowspan=1 colspan=1>0.7121</td><td rowspan=1 colspan=1>0.5811</td></tr><tr><td rowspan=1 colspan=1>Ramp-Filtering [4]</td><td rowspan=1 colspan=1>0.8403</td><td rowspan=1 colspan=1>0.5368</td><td rowspan=1 colspan=1>0.3679</td></tr><tr><td rowspan=1 colspan=1>IMAT [5]</td><td rowspan=1 colspan=1>0.7880</td><td rowspan=1 colspan=1>0.7280</td><td rowspan=1 colspan=1>0.5812</td></tr><tr><td rowspan=1 colspan=1>No Mitigation</td><td rowspan=1 colspan=1>0.5446</td><td rowspan=1 colspan=1>1.6740</td><td rowspan=1 colspan=1>0.6842</td></tr></table>

Furthermore, we compare CCNN’s generalization capabilities w.r.t. the interferences’ AoA. The training and validation data set used in this experiment are identical to the data set described in Section III-A, except that now we fix the interferences’ AoA to 45°. We then report results on the same test set as above, i.e., all AoAs are allowed.

Table 3. Performance on test set with uniform AoA of interferences after training on data with a fixed AoA of 45°.
<table><tr><td rowspan=1 colspan=1>Mitigation Technique</td><td rowspan=1 colspan=1>F1</td><td rowspan=1 colspan=1>EVM</td><td rowspan=1 colspan=1>PPMSE</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-1 (ours)</td><td rowspan=1 colspan=1>0.8303</td><td rowspan=1 colspan=1>0.7922</td><td rowspan=1 colspan=1>0.4702</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-m (ours)</td><td rowspan=1 colspan=1>0.8897</td><td rowspan=1 colspan=1>0.7416</td><td rowspan=1 colspan=1>0.4808</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-s (ours)</td><td rowspan=1 colspan=1>0.9128</td><td rowspan=1 colspan=1>0.8615</td><td rowspan=1 colspan=1>0.5545</td></tr><tr><td rowspan=1 colspan=1>CCNN-3D-xs (ours)</td><td rowspan=1 colspan=1>0.8842</td><td rowspan=1 colspan=1>1.0167</td><td rowspan=1 colspan=1>0.6800</td></tr><tr><td rowspan=1 colspan=1>CCNN-2D [15]</td><td rowspan=1 colspan=1>0.5349</td><td rowspan=1 colspan=1>1.7410</td><td rowspan=1 colspan=1>0.8064</td></tr></table>

Table 3 shows the improved generalization capabilities of CCNN-3D compared to CCNN-2D. Interestingly, smaller models now outperform CCNN-3D-l w.r.t. F1 and EVM, which indicates that CCNN-3D-l is overfitting to the interferences fixed AoA in the training and validation set.

Compared to Table 2, CCNN-3D’s performance drops, as the appearance of an interference still changes when varying its AoA by a fraction of an angle-bin. For instance, when an interference’s AoA perfectly coincides with an angle-bin, it will appear as a Kronecker-delta in the RDA-map. By contrast, when an interference’s AoA is located between two neighbouring angle-bins, the corresponding interference pattern in the RDA-map will have much wider spread in the angle-dimension. We expect angle generalization to improve when using radar sensors with more receive antennas.

## V. CONCLUSION

Our proposed architecture has fewer parameters and higher robustness compared to previous work as it generalizes across all AoAs. Nevertheless, classical signal processing methods for interference mitigation are more transparent and computationally cheaper. In future work we therefore aim to reduce the model’s computational footprint by considering the independence of range, Doppler and angle of objects. Furthermore, we plan to increase CCNN-3D’s transparency by directly training it on object detections [18].

[1] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[2] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in 2016 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM). IEEE, 2016, pp. 1–4.

[3] C. Fischer, Untersuchungen zum interferenzverhalten automobiler radarsensorik. Cuvillier Verlag, 2016.

[4] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive fmcw radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS). IEEE, 2018, pp. 1–4.

[5] F. Marvasti, M. Azghani, P. Imani, P. Pakrouh, S. J. Heydari, A. Golmohammadi, A. Kazerouni, and M. Khalili, “Sparse signal processing using iterative method with adaptive thresholding (imat),” in 2012 19th International Conference on Telecommunications (ICT). IEEE, 2012, pp. 1–6.

[6] J. Mun, H. Kim, and J. Lee, “A deep learning approach for automotive radar interference mitigation,” in 2018 IEEE 88th Vehicular Technology Conference (VTC-Fall). IEEE, 2018, pp. 1–5.

[7] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using rnn with self attention,” in ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2020, pp. 3802–3806.

[8] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world fmcw radar signals,” in 2020 IEEE International Radar Conference (RADAR). IEEE, 2020, pp. 624–629.

[9] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resource-efficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 927–940, 2021.

[10] M. Hirschmugl, J. Rock, P. Meissner, and F. Pernkopf, “Fast and resource-efficient cnns for radar interference mitigation on embedded hardware,” in 2022 19th European Radar Conference (EuRAD). IEEE, 2022, pp. 1–4.

[11] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive radar¨ interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR). IEEE, 2020, pp. 315–320.

[12] M. L. L. de Oliveira and M. J. Bekooij, “Deep convolutional autoencoder applied for noise reduction in range-doppler maps of fmcw radars,” in 2020 IEEE International Radar Conference (RADAR). IEEE, 2020, pp. 630–635.

[13] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall). IEEE, 2020, pp. 1–5.

[14] S. Chen, J. Taghia, T. Fei, U. Kuhnau, N. Pohl, and R. Martin, “A dnn¨ autoencoder for automotive radar interference mitigation,” in ICASSP 2021-2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2021, pp. 4065–4069.

[15] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Multi-antenna radar signal interference mitigation using complex-valued convolutional neural networks,” Graz University of Technology, Tech. Rep., 2023.

[16] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Tech., vol. 65, no. 5, pp. 1727–1734, 2017.

[17] L. L. Scharf and C. Demeure, Statistical signal processing: detection, estimation, and time series analysis. Prentice Hall, 1991.

[18] C. Oswald, M. Toth, P. Meissner, and F. Pernkopf, “End-to-end training of neural networks for automotive radar interference mitigation,” unpublished, 2023.