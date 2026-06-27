# IRNet: Interference Recognition Networks for Automotive Radars via Autocorrelation Features

Qizhe Qu , Yong-Liang Wang , Weijian Liu , Senior Member, IEEE, Shunjun Wei, Member, IEEE, and Qinglei Du

Abstract— With the rapid increase of the number of autonomous driving vehicles, more and more radars working on a similar frequency band are equipped on vehicles, which incurs risks of automotive radar interference. Therefore, a precise interference recognition method is becoming a compelling task. In this article, a novel interference recognition network, called IRNet, is proposed to recognize eight types of interference signals that include mutual interference, unintended interference, and adverse intended interference. First, autocorrelation features of interference signals are obtained via calculating their autocorrelation functions (ACFs) and converted as two-dimensional feature images. Next, these images are employed as inputs of the IRNet that owns significant representation power and adaptive feature selection ability. Finally, the prediction types of interference will be output via the IRNet directly. The robustness of autocorrelation features is verified via simulations. The simulation results show that the proposed method can achieve 90.85% overall recognition accuracy when the jamming-to-noise ratio (JNR) is 14 dB and nearly 100% when JNR > 8 dB. Compared with six state-of-the-art methods, the IRNet achieves much better recognition performance, especially under lower JNR conditions with relatively lower and acceptable computational complexity. Results on measured signals also verify the powerful generalization ability of the proposed method.

Index Terms— Automotive radar interference, convolutional neural network (CNN), interference type recognition, neural network application.

## I. INTRODUCTION

driving is winning great popularity and gaining steady improvements [1]. Autonomous driving relies greatly on multiple types of sensors to sense the real driving environment and make complex but intelligent decisions autonomously. These sensors used currently always include cameras, LiDARs, radars, and ultrasonic sensors [2]–[5]. In particular, more and more automotive radars are equipped and employed on modern vehicles due to their unique robustness under bad weather and poor light conditions [6].

At the same time, the risk of automotive ego-radar interference by other automotive radars is becoming a significant and nonnegligible issue [7] since most working frequency bands of automotive radars are highly coincident or even the same [8]. The interference to automotive radars will increase the probability of both missed detections and false alarms. Even the Tesla Model S, which is famous for its advanced autonomous driving technology, is being practically attacked by leveraging the vulnerability of its millimeter-wave radars [9]. It is also proved that the jamming attack can be employed to interfere with vehicles by decreasing or minimizing the received signalto-noise ratio (SNR) for the vehicles [9].

From the perspective of sources of interference, automotive radar interference mainly consists of mutual interference, unintended interference, and intended interference [10]. Specifically speaking, the mutual interference indicates the electronic interference between the ego vehicle and other vehicles. Nowadays, China has assigned 76–79 GHz to automotive radar devices, and with the rapid increase of the number of vehicles, mutual interference will be a great concern. Besides, many other kinds of radars also work in the mentioned frequency band, such as traffic monitors. These kinds of interference can be regarded as unintended interference. As mentioned above, almost all automotive radars can be interfered with by deliberate attacks as well. Also, the consequences of adverse or intended interference are very serious, especially for the radar sensors with higher levels of autonomy [11]. The risk of potential intended interference should not be ignored, especially for the valuable targets.

Aiming at avoiding and suppressing automotive radar interference, many interference mitigation methods are proposed reactively or proactively. In [12], an autoencoder based on the convolutional neural network (CNN) is proposed to reconstruct the ideal signals from the interfered signals by converting the interference mitigation as a denoising task. An interference mitigation technique for automotive millimeter radars is proposed based on a tunable Q-factor wavelet transform domain in [13]. In [14], a decentralized spectrum allocation using a reinforcement learning approach is proposed to deal with mutual interference. In [15], a self-motion effects cancellation method through clutter recognition is proposed. The robustness of this method is verified by both simulations and measured experiments, which also shows its suitability for radar on moving platforms.

Although these interference mitigation methods are always capable of dealing with a certain kind of interference, they may be powerless for the real complex interference driving environment. Moreover, these methods mainly focus on mutual interference but ignore other kinds of interference. As a consequence, to ensure a stable interference mitigation performance and deal with the interference more precisely, there is a need to recognize the types of occurred interference for automotive radars, and then, an appropriate mitigation or suppression approach is employed to solve the interference problems [16], that is, the recognition and classification of interference should precede the mitigation steps. Also, a precise interference recognition method is supposed to naturally lead to better mitigation and suppression techniques [11].

For the frequency-modulated continuous-wave (FMCW) automotive radar systems, five time-domain features of five kinds of interference signals are extracted and a support vector machine (SVM) is used to classify the five modulations in [16]. The five modulations are the continuous wave (CW), slow and fast chirp FMCW, pulse CW, and frequency-shift keying (FSK) The simulation results show that the recognition accuracy is over 96%. In [17], time–frequency-domain features and range–Doppler profiles of six different types of mutual interference are simulated and an SVM is also used to recognize these interference waveforms. The crossvalidation generalization accuracy in the simulation is about 90.6%. In [18], a CNN-based method is proposed to recognize five types of interference signals. The method takes the range–Doppler responses that are obtained by the 2-D Fourier transform as inputs. Through simulations, the overall recognition accuracy is about 96% and the proposed CNN is verified to outperform the SVM methods proposed in [16], while these time–frequency domain features and range–Doppler profiles require considerable computation, which may be not suitable for real-time needs in autonomous driving.

Due to the fact that few works pay attention to interference recognition in autonomous driving, many pieces of research have focused on the radar jamming recognition in electronic countermeasures (ECMs), which is also instructive for our theme in this article. In [19], features in the time domain and frequency domain of the CW, narrow, and wideband jamming signals are extracted and converted as feature images, and the VGG network is used as the classifier. In [20], a CNN-based method using power-spectrum features is designed to classify suppression and compound jamming signals. In [21], a pretrained CNN model using time–frequency images is proposed to classify jamming signals. The simulation results indicate that the recognition accuracy is about 98.66% from 0 to 8 dB.

Besides, time–frequency images are used in [22] to achieve radar jamming recognition.

On the whole, most existing works of automotive radar interference recognition only focus on mutual interference and unintended interference but ignore the risk of adverse and intended interference. In addition, the recognition method in [16] still relies on complex handcrafted features, which requires a lot of manpower. Moreover, time–frequency domain features and range–Doppler features used in [17] and [18] usually suffer from high computation complexity, which may lead to a time delay. More importantly, the received signals are interfered with not only the active jamming mentioned above but also the transmitting noise, that is, the jamming-to-noise ratio (JNR) of received signals could be very low, especially under complex driving environment [23]. Thus, the influence of JNRs should be considered as well, whereas most existing methods merely simulate the ideal interference signals. On the other hand, plain CNNs with a large number of layers may tend to induce the degradation problem [24] and conventional CNNs are prone to focus on too many local features within local receptive fields instead of global information.

To deal with these mentioned problems, a novel interference recognition network (IRNet) for automotive radars is proposed, which takes robust autocorrelation features as inputs. The IRNet is capable of recognizing eight kinds of interference signals varied with received JNRs. It is worth noting that the proposed method mainly focuses on the recognition of single occurred interference rather than compound multiple interferences. In addition, our method can recognize more types of interference signals via transfer learning. The main contributions and novelties of our works are given as follows.

1) Eight kinds of interference signals, including mutual interference, unintended interference, and adverse intended interference, are simulated and modeled. The robustness of autocorrelation features is verified via comparisons with commonly used time-domain features, time–frequency features, and power-spectrum features.

2) To address the degradation problem and boost the representation power through feature recalibration, a novel IRNet is constructed, which not only can achieve the feature adaptive selection with performance gains but also is easier to train and optimize with relatively lower computational complexity.

3) The proposed method is not only analyzed and compared on simulation datasets that are close to real electromagnetic environments but also on measured signals obtained by a radio frequency hardware platform, which is rare in the existing literature.

The rest parts of this article are organized as follows. Brief introductions and mathematical models of eight kinds of interference signals and commonly used features in interference signal recognition problems are first described in Section II. The problem formulation, structures of the proposed network, and details of the simulation dataset are given in Section III. Simulation results, measured results, and the computational complexity are analyzed and compared in Section IV. Finally, we summarize conclusions and discussions about future works in Section V.

## II. MATHEMATICAL BACKGROUND

As mentioned in Section I, time-domain features, frequency-domain features, time–frequency features, and power-spectrum features are commonly used to achieve interference recognition, while autocorrelation features are employed in our research. Eight kinds of typical interference for automotive radars are simulated and modeled in this section, including mutual interference, unintended interference, and adverse intended interference.

## A. Commonly Used Features of Interference Signals

Without loss of generality, the received interfered signal x (t) by automotive radars is modeled as

$$
x ( t ) = s ( t ) + i ( t ) + n ( t ) , 0 \leq t \leq T\tag{1}
$$

where s(t) represents the ideal interference-free received signal, i (t ) is the interference, and $n ( t )$ denotes the additive white Gaussian noise (AWGN) with mean zero and $N _ { 0 } / 2$ doublesided power spectral density. The AWGN always represents the transmitting noise to cause lower SNRs, and T denotes the pulsewidth. Time-domain features [16] are mainly based on the amplitude and the temporal information of x(t). Time–frequency features that are extracted by the short-time Fourier transform (STFT) are widely employed for nonstationary signals to demonstrate the changes in the frequency spectrum varied with time.

As for power-spectrum features [20], they indicate the power with a unit frequency band. The average power P of x (t) is calculated as

$$
P = \frac { 1 } { T } \int _ { 0 } ^ { T } x ^ { 2 } ( t ) d t .\tag{2}
$$

If the limitation of $( | F ( \omega ) | ^ { 2 } / 2 \pi T )$ exists when $T \ \to \ \infty$ where $F ( \omega )$ denotes the Fourier transform of $x ( t )$ , then $P$ can be calculated in the frequency domain

$$
P = \frac { 1 } { 2 \pi } \int _ { - \infty } ^ { \infty } \operatorname* { l i m } _ { T  \infty } \frac { | F ( \omega ) | ^ { 2 } } { T } d \omega .\tag{3}
$$

Thus, the power spectrum P(ω) of x (t) is

$$
P ( \omega ) = \operatorname* { l i m } _ { T  \infty } \frac { | F ( \omega ) | ^ { 2 } } { 2 \pi T } .\tag{4}
$$

The power-spectrum features are extracted by calculating the power-spectrum density function of x(t).

## B. Autocorrelation Features of Interference Signals

Autocorrelation features have achieved great performance in the radar signal recognition field [25], [26], and therefore, it is instructive to employ autocorrelation features in automotive radar interference recognition.

In general, the autocorrelation indicates the degree of the correlation between a signal sequence and itself at two different time points and also measures the similarity of a sequence between two observed values. The autocorrelation function (ACF) has the ability to reduce the influence of AWGN to some extent [26].

![](images/55703db11595791c9f8d321b7ae2b606e052b8f77ddd913d56847a8fb76b4ce8.jpg)  
Fig. 1. Real complex driving environments.

Mathematically, the ACF of x(t) is calculated as

$$
R _ { x } ( \tau ) = x ( \tau ) * x ^ { * } ( - \tau ) = \int _ { - \infty } ^ { \infty } x ( t + \tau ) x ^ { * } ( \tau ) d t\tag{5}
$$

where $" * >$ means the convolution operation, τ denotes the time delay, and superscript $( \cdot ) ^ { * }$ denotes the conjugate operation.

The analytical signal sequence $x ( n )$ , which is the output of $x ( t )$ in a sampler, can be defined as

$$
x ( n ) = A ( n ) \cdot \exp [ j ( 2 \pi n f ( n ) / f _ { s } + \varphi ( n ) + \varphi _ { 0 } ) ]\tag{6}
$$

where A(n), f (n), and $\varphi ( n )$ denote amplitude modulations, frequency modulations, and phase modulations, respectively, $f _ { s }$ represents the sampling frequency, and $\varphi _ { 0 }$ means an initial phase. Then, the ACF can be written as

$$
\begin{array} { c } { { A C F = x ( n ) ^ { * } x ( n + m ) } } \\ { { = A ^ { 2 } { \exp \{ j [ 2 \pi ( n + m ) f ( n + m ) / f _ { s } - 2 \pi n f ( n ) / f _ { s } ] } } }  \\ { { + \varphi ( n + m ) \varphi ( n ) \} } } \end{array}\tag{}
$$

where $m$ means the time delay. The ACF is only related to the time delay, the frequency modulations, and the phase modulations. Thus, autocorrelation features are extracted via calculating the ACF of x(t).

## C. Eight Types of Interference

In the real complex driving environment [27], shown in Fig. 1, the ego vehicle may be interfered by the mutual interference, the unintended interference, and the intended interference, which is usually ignored in existing methods. In our works, these three kinds of interference are taken into the consideration. Also, since the FMCW radar systems are most commonly used in autonomous driving vehicles [6], our works are based on FMCW automotive systems.

For the sake of simplicity, the descriptions and formulas of well-known signal types, including binary phase shift keying (BPSK), FSK, CW, and pulsed continuous wave (PCW), are ignored, while their time–frequency diagrams and ACFs are still shown in Figs. 2–5.

1) Frequency-Modulated CW: The triangular chirp FMCW is adopted to simulate the signals transmitted in on June 22,2026 at 07:35:28 UTC from IEEE Xplore. Restrictions apply.

![](images/5fee4e6dd5630f45b0b74bd9bfaedfd77a9e74c9c00cc71e48060f11614253fd.jpg)

![](images/ee150c5c95d328270f762dfe8106ad678ebb0eda562ff9bf262d613459f4c072.jpg)  
Fig. 2. Time–frequency diagram (left) and the ACF (right) of BPSK.

![](images/b6b40405c0be407dff8e1b853baa76be491ba602e543642b45c3eceda310eccd.jpg)

![](images/01db13c4ce5e347482c4c27e4aa6144a286ff9be794271a668b5651fe9204b9a.jpg)  
Fig. 3. Time–frequency diagram (left) and the ACF (right) of FSK.

![](images/eaa8c46b0b5c39d0e63fedc28f6d31dd5a4ab6d8b85a1bbdf7a8eb65d66dbf1f.jpg)

![](images/98f652179d99472235d13cddbba2277e8fac5bdcb7b2005f12742d3877c7ca99.jpg)  
Fig. 4. Time–frequency diagram (left) and the ACF (right) of CW.

![](images/49fbc47e7f5575aa7cb97329606033971af2508b346eb77b72491231d73e4a8d.jpg)

![](images/a5627f68733971eef01111e06bd91e945394e5bba75b369987731c398d8c8efd.jpg)  
Fig. 5. Time–frequency diagram (left) and the ACF (right) of PCW.

automotive radars. Also, the FMCW can be written as

$$
s ( t ) = \left\{ \begin{array} { l l } { \exp \Big ( \frac { j \pi B } { T _ { c } } t ^ { 2 } \Big ) \exp ( j 2 \pi f _ { m } t ) , } & { 0 \leq t \leq T _ { c } } \\ { \exp \Big ( - \frac { j \pi B } { T _ { c } } ( t - 2 T _ { c } ) ^ { 2 } \Big ) \exp ( j 2 \pi f _ { m } t ) , } & { T _ { c } \leq t \leq 2 T _ { c } } \end{array} \right.\tag{8}
$$

where B denotes the chirp bandwidth, $T _ { c }$ is the chirp interval, and $f _ { m }$ is carrier frequency in the mth subband. The time– frequency diagram and the ACF of FMCW are shown in Fig. 6.

2) Chirp Sequence (CS): The CS usually contains a series of sawtooth frequency waves and is also widely used in autonomous driving vehicles. Thus, CS is a major concern belonging to the mutual interference. The mathematical model

![](images/8c51f239824c07eee1a059ed538c5a24331bb4a61c21605e8d2664f6ae1182b3.jpg)

![](images/1dfd1f05e4049e0fdffc1edca5ff7c91904708faf358d1e3c343362890523ebd.jpg)  
Fig. 6. Time–frequency diagram (left) and the ACF (right) of FMCW.

![](images/b598c2afa3cd622b4114e5bf46e1cce304b1f75155236651c9cf628aa6ef9d0b.jpg)

![](images/0e6af5cc06720d1b443d81ac3c624b51b24e99fc2bbc59001e1410e6386f89f0.jpg)  
Fig. 7. Time–frequency diagram (left) and the ACF (right) of CS.

![](images/c2582f236fac881448d3f0ecdee440b60cf188dc98244153ed9fdbed06e6619e.jpg)

![](images/491a457aff43b7f8c455f10a5d1a73fafea7b29020083c7a3d3d4e23beda53b4.jpg)  
Fig. 8. Time–frequency diagram (left) and the ACF (right) of FMN.

of CS is defined as

$$
i ( t ) = \exp \biggl ( \frac { j \pi B } { T _ { c } } t ^ { 2 } \biggr ) \exp ( j 2 \pi f _ { m } t ) , ~ 0 \leq t \leq T _ { c }\tag{9}
$$

where B denotes the chirp bandwidth, $T _ { c }$ is the chirp interval, and $f _ { m }$ is the modulation frequency. The time–frequency diagram and the ACF of the CS are shown in Fig. 7.

3) Frequency Modulation Noise (FMN): Noise modulation jamming is the cheapest way to achieve the adverse and intended interference, which broadcasts noise into the automotive radars [11]. FMN adopts the Gaussian noise to modulate carrier frequency and the mathematic model of FMN is defined as

$$
J ( t ) = A _ { m } \cos \biggl ( f _ { c } t + 2 \pi K _ { \mathrm { F M } } \int _ { 0 } ^ { t } u \left( t ^ { \prime } \right) d t ^ { \prime } + \varphi \biggr )\tag{10}
$$

where $u ( t )$ is the band-limited Gaussian noise and $K _ { \mathrm { F M } }$ denotes the modulation slope. The time–frequency diagram and the ACF of the FMN are shown in Fig. 8.

4) Radio Frequency Noise (RFN): It is also a kind of intended interference that is usually obtained by amplifying microwave noise using an amplifier circuit directly [28]. Since the operation bandwidth of an amplifier is limited, the bandwidth of RFN is also limited and corresponds to victim radars.

![](images/d8b2f023bac88946727d9ff663484324d310c771f828adb362b83e034b84f57b.jpg)  
Fig. 9. Time–frequency diagram (left) and the ACF (right) of RFN.

The mathematic model of RFN can be written as

$$
J ( t ) = U _ { n } ( t ) \cdot \cos ( f _ { c } t + \phi ( t ) )\tag{11}
$$

where $J ( t )$ is a narrowband Gaussian process, the envelope $U _ { n } ( t )$ obeys the Rayleigh distribution, and the phase $\phi ( t )$ always obeys a uniform distribution in [0, 2π] and should be independent with $U _ { n } ( t )$ . The time–frequency diagram and the ACF of the RFN are shown in Fig. 9.

## III. METHODOLOGY

In this article, a novel interference recognition network, namely, IRNet, is constructed for the automotive radar and compared with plain CNNs. The IRNet not only owns better representational powers with recognition performance gains but also is easier for training and optimization with relatively lower computational complexity. First, the problem formulation of the interference for the automotive radar recognition issue is discussed.

## A. Problem Formulation

Equation (1) represents a sample of a complete received signal with AWGN and the interference. To measure the power of the influence of transmitting noise and existing interference, the JNR is introduced and defined, in decibel, as

$$
\mathrm { J N R } = 1 0 \log _ { 1 0 } \left( { \frac { P _ { i } } { \sigma ^ { 2 } } } \right)\tag{12}
$$

where $P _ { i }$ is the power of the existing interference and $\sigma ^ { 2 }$ denotes the power of AWGN, which is calculated as

$$
\sigma ^ { 2 } = \frac { 1 } { T } \int _ { 0 } ^ { T } n ( t ) ^ { 2 } d t .\tag{13}
$$

Then, all samples of $x ( t )$ and their corresponding labels, which indicate their real types of interference, are constituted as a sample space $( x , y )$ . Our goal in interference recognition is to find a special model to approximate the real conditional probability distribution $p _ { r } ( \pmb { y } | \pmb { x } )$ .

In general, the special model could be defined as

$$
\mathcal { F } = \left\{ f ( \boldsymbol { x } ; \boldsymbol { \theta } ) | \boldsymbol { \theta } \in \mathbb { R } ^ { D } \right\}\tag{14}
$$

where $f ( \boldsymbol { x } ; \boldsymbol { \theta } )$ is a model from a series of functions $\mathcal { F }$ and $D$ is the number of probable parameters. If adequate samples of $( x , y )$ could be obtained, the training dataset D could be constructed naturally, i.e.,

$$
D = \left\{ \left( { \pmb x } ^ { ( n ) } , { \pmb y } ^ { ( n ) } \right) \right\} _ { n = 1 } ^ { N } .\tag{15}
$$

Then, the special prediction model $f ( x ; \theta ^ { * } )$ is supposed to satisfy the following statement in theory:

$$
\left| f \left( \mathbf { x } ; \theta ^ { * } \right) - \mathbf { y } \right| < \epsilon \quad \forall ( \mathbf { x } , \mathbf { y } ) \in D\tag{16}
$$

where 	 denotes a very small positive number. Nevertheless, it is almost impossible to obtain the real conditional probability distribution $p _ { r } ( \pmb { y } | \pmb { x } )$ . Thus, for a given training dataset $D ,$ the empirical risk can be calculated to reflect the difference between the prediction model $f ( x ; \theta ^ { * } )$ and the real data distribution [29]. The empirical risk $\mathcal { R } _ { D } ^ { \mathrm { e m p } }$ is calculated as

$$
\mathcal { R } _ { D } ^ { \mathrm { e m p } } ( \theta ) = \frac { 1 } { N } \sum _ { n = 1 } ^ { N } \mathcal { L } \big ( y ^ { ( n ) } , f \big ( \pmb { x } ^ { ( n ) } ; \theta ^ { * } \big ) \big )\tag{17}
$$

where $\mathcal { L } ( \cdot )$ denotes a loss function. The cross-entropy loss function is most commonly used in multiclassification problems and it could be defined as [30]

$$
\mathcal { L } = - \sum _ { n = 1 } ^ { N } y ^ { ( n ) } \cdot \log \left( f \left( x ^ { ( n ) } ; \theta ^ { * } \right) \right)\tag{18}
$$

where real label $y ^ { ( n ) }$ and prediction label $f ( \pmb { x } ^ { ( n ) } ; \theta ^ { * } )$ are in the one-hot format.

Then, how to determine the best model $f ( x ; \theta ^ { * } )$ is actually an optimization problem. The adaptive moment estimation (Adam) [30] is selected in our works to optimize models and the Adam could be defined as

$$
\left\{ \begin{array} { l l } { M _ { t } = \beta _ { 1 } M _ { t - 1 } + ( 1 - \beta _ { 1 } ) \pmb { g } _ { t } } \\ { G _ { t } = \beta _ { 2 } G _ { t - 1 } + ( 1 - \beta _ { 2 } ) \pmb { g } _ { t } \odot \pmb { g } _ { t } } \end{array} \right.\tag{19}
$$

where ${ \pmb g } _ { t }$ is the gradient of parameters in models, $M _ { t }$ denotes the mean value of $\mathbf { \Delta } _ { g _ { t } } , \mathbf { \Delta } G _ { t }$ means the secondary moment of ${ \pmb g } _ { t } ,$ and $\beta _ { 1 }$ and $\beta _ { 2 }$ are the decay rates of the moving average, generally $\beta _ { 1 } = 0 . 9$ and $\beta _ { 2 } = 0 . 9 9$

## B. Structure of the IRNet

Since plain CNNs with deep layers are prone to incur the degradation problem, this means that CNNs will become hard to converge and optimize. To deal with the degradation problem, a deep residual network, namely, ResNet, is proposed in [24]. Thus, a ResNet is employed as the basis of the proposed IRNet. Also, the overview and diagram of the whole method are shown in Fig. 10.

The ResNet tries to approximate mapping $F ( x ) = H ( x ) - x$ instead of the underlying mapping H (x) via stacking nonlinear layers. The ResNet demonstrates that the optimization of the residual mapping is supposed to be much easier than the original mapping. Also, the residual mapping is realized by inserting a series of short connections that skip some corresponding layers.

For the purpose of boosting the performance of the CNNs, the depth-wise overparameterized convolutional layer (DO-Conv) [32] is integrated into the proposed IRNet. The DO-Conv consists of many augmentation depth-wise convolution operations. These additional convolution kernels introduce an overparameterization that adds more learnable parameters to strengthen the nonlinear ability and improve the learning ability naturally. Thus, the DO-Conv can not only accelerate the training of the IRNet but also consistently boost the performance.

![](images/74d5f89d4f6355bf9c0947c67b356a09242d3d8366db67dfe3b09b8264fb4e1c.jpg)  
Fig. 10. Overview and diagram of the whole method.

Formally, the DO-Conv is a composition of a traditional convolution operation with a kernel $\mathbb { W } \in \mathbb { R } ^ { C _ { \mathrm { { o u t } } } \times \mathbb { D } _ { \mathrm { { m u l } } } \times \mathbb { C } _ { \mathrm { { i n } } } }$ and a depth-wise convolution operation with a kernel $\mathbb { D } \ \in \ \mathbb { R } ^ { ( M \times N ) \times D _ { \mathrm { m u l } } \times C _ { \mathrm { i n } } }$ . Here, M and N denote the spatial dimensions, $C _ { \mathrm { i n } }$ and $C _ { \mathrm { { o u t } } }$ are the number of input channels and output channels, and $D _ { \mathrm { m u l } }$ is a depth multiplier. Then, given an input $\mathbb { P } \in \mathbb { R } ^ { ( M \times N ) \times C _ { \mathrm { i n } } }$ , the output of a DO-Conv is calculated as

$$
\mathbb { O } = ( \mathbb { D } , \mathbb { W } ) \mathbb { P } = \mathbb { W } * ( \mathbb { D } \circ \mathbb { P } )\tag{20}
$$

where <sup>O</sup> is the output, denotes a DO-Conv operation, ∗ is the traditional convolution operation, and ◦ is the depth-wise convolution operation defined as

$$
\mathbb { O } _ { d _ { \mathrm { m u l } } C _ { \mathrm { i n } } } = \sum _ { i } ^ { M \times N } \mathbb { D } _ { \mathrm { i d _ { \mathrm { m u l } } C _ { \mathrm { i n } } } } \mathbb { P } _ { i C _ { \mathrm { i n } } } .\tag{21}
$$

The diagram of the DO-Conv is shown in Fig. 10. In a word, a DO-Conv gains better performance without introducing computational complexity during inference phases.

On the other hand, plain CNNs are blamed for focusing on local information too much within local receptive fields and ignoring global information. To address this issue, the squeeze and excitation block (SE-b) [33] is introduced in the proposed IRNet. The SE-b employs a channel-wise attention mechanism that performs feature recalibration to allow the IRNet to learn to adaptively emphasize significant information and suppress useless information, which can suppress the irrelevant noise in the received signals to some extent.

Formally, the SE-b consists of a squeeze operation and an excitation operation. The squeeze operation usually uses a global average pooling to embed the global information of inputs, that is, the output $O _ { \mathrm { s q } }$ of a squeeze operation can be calculated as

$$
O _ { \mathrm { s q } } = \frac { 1 } { H \times W } \sum _ { i = 1 } ^ { H } \sum _ { j = 1 } ^ { W } X ( i , j )\tag{22}
$$

where H and W are the spatial dimensions and X is the input feature of the squeeze operation.

The excitation operation is supposed to adaptively recalibrate the aggregated information by the squeeze operation and fully capture channel-wise dependencies. Also, the excitation

operation usually contains two full connection layers with nonlinear activation functions. Mathematically, the output s of the excitation operation is calculated as

$$
s = \sigma \left( W _ { 2 } \delta \bigl ( W _ { 1 } O _ { \mathrm { s q } } \bigr ) \right)\tag{23}
$$

where $W _ { 1 }$ and $W _ { 2 }$ denote the weights in the two full connection layers and σ and δ are the sigmoid activation function and ReLU activation function, respectively. Thus, the final output O of an SE-b is rescaled as

$$
O = X \cdot s .\tag{24}
$$

In addition, the parametric rectified linear unit (PReLU) is employed as an activation function instead of the ReLU since the PReLU promotes the model fitting ability and decreases the risk of overfitting with no extra computational complexity [34].

Finally, details of a module in the proposed IRNet are shown in Fig. 11. To summarize, the autocorrelation features of the received signals with interference and AWGN are obtained through calculating their ACFs in (7) and converting them as two-dimensional feature images. Then, these feature images are supposed to be employed as inputs of the proposed IRNet where these inputs will first go through the DO-Conv to extract their deep features. The significant feature information will be adaptively strengthened, while the irrelevant and useless feature information will be suppressed in the SE-b. Finally, the full connection layers will output the prediction interference types of input signals directly.

## C. Simulation Datasets

The simulation datasets are used to train and test the proposed IRNet and other comparison networks. Thus, the physical parameters of simulation datasets are chosen close to real autonomous driving environments by referring to [10], [17], and [18], which are listed in Table I.

The carrier frequency is varied from 76.8 to 77.2 GHz and the sampling frequency is 2 GHz. The sampling time is 10 ms and the chirp duration is about 50 $\mu \mathbf { S } .$ The AWGN is added into simulation signals to reflect the influence of transmitting noise. Taking the real interference environment into consideration, the JNRs are varied from −16 to 20 dB in 2-dB increment. The modulated phase sequence in BPSK is a Barker code with 13 code elements. Therefore, 12 312 samples in total are constructed for training and validation of both the proposed IRNet and comparison networks.

![](images/1b017a7c5c61120be2adf28bcef6f86d799c70c06edcd7b1b77b19d6655130d7.jpg)  
Fig. 11. Details of a module in the proposed IRNet.

## IV. EXPERIMENTS AND RESULTS

The details of simulation experiments and evaluation metrics of the recognition performance are first given in this section. Then, the simulation results of the proposed IRNet and the comparisons with six state-of-the-art networks are analyzed.

## A. Details of Experiments and Evaluation Metrics

As for the hyperparameters of training, 80% of the training dataset is used for training and the rest are employed for validation. The batch size and learning rate during the training are 32 and $1 \times \mathrm { e } ^ { - 4 }$ , respectively. Hundred epochs are run for training. Both the proposed IRNet and comparison networks are implemented in PyTorch 1.3.1, CUDA 10.1 on the PyCharm-Community 2018.1.1 platform. The hardware platform is Intel® Core i7-8700K 3.7 GHz CPU, 32 GB RAM, and NVIDIA 1080Ti with 12-GB video memory.

In order to evaluate the recognition performance of each network quantitatively, three evaluation metrics are introduced in the result part, namely, the overall accuracy (OA), the mean OA (mOA), and the kappa coefficient (Ka) [35].

Assuming that there are N samples in the test dataset, then the OA of each kind of interference signal is calculated as

$$
{ \mathrm { O A } } = { \frac { \mathrm { N u m b e r ~ o f ~ c o r r e c t ~ s a m p l e s } } { N } } \times 1 0 0 \%\tag{25}
$$

The mOA is obtained by averaging eight OAs of each network, which is calculated as

$$
{ \mathrm { m e a n ~ O A } } = { \frac { \sum _ { i } ^ { I } O A _ { i } } { i } }\tag{26}
$$

where I is the number of types of interference signals.

TABLE I  
PHYSICAL PARAMETERS OF SIMULATION DATASETS
<table><tr><td>Modulation type</td><td>Parameters</td><td>Value</td></tr><tr><td>FMCW</td><td>Center frequency JNR Bandwidth Sampling time</td><td>76.8 to 77.2 GHz -16 to 20 dB 50 to 500 MHz 10 ms</td></tr><tr><td>BPSK</td><td>Center frequency JNR Sampling time Modulation code</td><td>76.8 to 77.2 GHz -16 to 20 dB 10 ms 13 Baker code</td></tr><tr><td>CS</td><td>Center frequency JNR Bandwidth Sampling time</td><td>76.8 to 77.2 GHz -16 to 20 dB 50 to 500 MHz 10 ms</td></tr><tr><td>CW</td><td># of chirps Center frequency JNR Sampling time</td><td>20 76.8 to 77.2 GHz -16 to 20 dB 10 ms</td></tr><tr><td>FMN</td><td>Center frequency JNR Interference bandwidth Sampling time</td><td>76.8 to 77.2 GHz -16 to 20 dB 200MHz 10 ms</td></tr><tr><td>FSK</td><td>Center frequency JNR # of steps Sampling time</td><td>76.8 to 77.2 GHz -16 to 20 dB 5 10 ms</td></tr><tr><td>PCW</td><td>Center frequency JNR # of pulses Sampling time</td><td>76.8 to 77.2 GHz -16 to 20 dB 5 10 ms</td></tr><tr><td>RFN</td><td>Center frequency JNR Sampling time</td><td>76.8 to 77.2 GHz -16 to 20 dB 10 ms</td></tr></table>

Ka is always employed to measure consistency and performance in multiclassification problems [20]. Similar to OA and mOA, higher Ka values mean better recognition performance. Assume that the number of each kind of interference signal in the test dataset is $a _ { 1 } , a _ { 2 } , \ldots , a _ { 8 }$ and the number of correct samples in each type is $b _ { 1 } , b _ { 2 } , \ldots , b _ { 8 }$ . Thus, Ka is defined as

$$
{ \left\{ \begin{array} { l l } { p _ { e } = { \frac { a _ { 1 } \times b _ { 1 } + a _ { 2 } \times b _ { 2 } + \cdot \cdot \cdot + a _ { 8 } \times b _ { 8 } } { N ^ { 2 } } } } \\ { \mathrm { K a } = { \frac { \mathrm { O A } / 1 0 0 - p _ { e } } { 1 - p _ { e } } } . } \end{array} \right. }\tag{27}
$$

## B. Comparison Results of Different Features

To verify the robustness of autocorrelation features, comparisons with time-domain features, time–frequency features, and power-spectrum features are explored. First, the t-stochastic neighbor embedding (t-SNE) [36] algorithm is employed to visualize the distribution of these features and 200 samples are stochastically chosen in each kind of feature. The visualization results at 0 dB are shown in Fig. 12.

As for time-domain features, it is very hard to classify the CW, FMCW, FMN, and BPSK signals since they are mixed up greatly, which also happens for power-spectrum features. Among time–frequency features, the BPSK signals and CW signals are mixed up greatly. The RFN and FMCW are overlapped a lot. It is obvious that each type of interference signal is much more independent and separable from each other. Only a small number of RFN and CS signals are overlapped, that is, the phenotype of autocorrelation features seems more suitable for classification problems.

![](images/61cbc691249ab9818fe25b99ebd9b86bde6e730dca44714ba2456fbbabbc1245.jpg)  
(a)

![](images/36062f36adfbe294728ec0ce1697f7ad942d9bde587b2ff5afe7c86b5e6870e9.jpg)  
(b)

![](images/a93beb29476117f09da1eccbbe450a05800374be480490274456f674cd41e39e.jpg)  
(c)

![](images/887eee811bd98166700a4736cfdbe9424fb09b5600168f2ed9ccb49e79ff9e19.jpg)  
(d)  
Fig. 12. Visualization results by t-SNE at 0 dB. (a) Time-domain features. (b) Power-spectrum features. (c) Time–frequency features. (d) Autocorrelation features.

TABLE II  
mOA OF EACH KIND OF FEATURES (AVERAGE VALUE ± STANDARD DEVIATION)
<table><tr><td></td><td>Time- domain feature</td><td>Power- spectrum feature</td><td>Time- frequency feature</td><td>Autocorrelation feature</td></tr><tr><td rowspan="2">mOA</td><td>74.11%</td><td>74.94%</td><td>84.06%</td><td>97.23%</td></tr><tr><td>±0.61%</td><td>±0.22%</td><td>±0.49%</td><td>±0.27%</td></tr></table>

![](images/66c44a3c7c371cb735b05c4c4583b9deb381c98b234c02d57c3d5e7920bc0219.jpg)  
Fig. 13. OAs at different JNRs of the IRNet.

To further explore the performance of each kind of feature, the proposed IRNet has been trained and tested using these features. The mOA of each kind of feature is given in Table II. The mOA of autocorrelation features is about 97.23%, which is nearly 23.12%, 22.28%, and 13.16% higher than the mOA of time-domain features, power-spectrum features, and time–frequency features. Thus, autocorrelation features are more appropriate in interference recognition.

![](images/6cc7b2927dedd8088220c8b4b5390a8544eeaa1d9a9efa02b6c1265200c56ca7.jpg)

![](images/796089fc7e8854c777f65821824393476a3a73e8bcc4e9e6d9418be259fad41a.jpg)  
Fig. 14. Confusion matrixes at −10 dB (left) and −8 dB (right).

![](images/97a903b3bd638788fc842af60955d923b16fb266bed8d23ce8fb075e216e8932.jpg)  
(a)

![](images/8b60f06999eed7a7a20087f4636ab5a42c1f342462b7f563d66eb18060cafb85.jpg)

![](images/b688df751c486f788dc2509d78271f3552f78a7cc6920dc21a38cfe0cbf060e8.jpg)  
(c)

(b)  
![](images/1c0e04f06d083a5b7ebcfd595256105f52c12718560f6bb0e3bc821a4e649ee2.jpg)  
(d)  
Fig. 15. Autocorrelation features at −10 dB. (a) FMCW, (b) CS, (c) PCW, and (d) RFN.

## C. Performance of the Proposed IRNet

Since most existing methods ignore the JNR introduced by both interference and transmitting noise in the real driving environments, the recognition performance against JNR of the proposed IRNet is mainly focused and analyzed. The OAs at different JNRs of the IRNet are shown in Fig. 13.

At −16 dB, the OAs of CW and FMCW signals are almost 100%, which indicates that the received FMCW signals without interference can be recognized very well even at −16 dB. Also, the OAs of FSK, BPSK, FMN, and CS are about 80.5%, 77.9%, 70%, and 61.4% at −16 dB, respectively, while the OAs of the RFN and PCW are 41.2% and 12.7%, respectively, which is much worse. As the JNR improves, OAs of each type of interference increase as well. At −14 dB, the OAs of PCW, FMN, and CS are 94.8%, 92.6%, and 94.9%, respectively. OAs of BPSK and FSK are also close to 100%. Also, OAs of all types of interference except for the RFN converge to 100% at −12 dB and maintain stability against JNRs, while the OA of RFN is higher than 90% at −8 dB. Until 0 dB, the OA of RFN is close to 100% and keeps stable against JNRs.

![](images/e375a25fe06bda5f7e27c54b1b5b33696684bd61ec8ed6bf59d60f329bf83597.jpg)  
(a)

![](images/542916b5665654a138dc47830cc140f26f8376bbcbe734eff6767bada3a2b9d0.jpg)  
(b)

![](images/144f4a1ff48bc5f7cdf3ec0555ad0f38a747bac7f9b20e85f0aa291b004ddc51.jpg)  
(c)

Fig. 16. OAs at different JNRs of (a) SE, (b) VGG, and (c) SJRNet.  
![](images/da13a428a5528341235476573fdf3e2ebab20d3a3c786c3c555f16efa183308e.jpg)  
(a)

![](images/af3a26c313224635d78cd50ac5a852e16b2c713ebf8207cbb3f23e7ae1259b6b.jpg)  
(b)

![](images/1eb71219c9c06306985d18a9b7dc0e438f27b515a0463dc22eb5cf1e3cc97756.jpg)  
(c)  
Fig. 17. OAs at different JNRs of (a) PCNN, (b) RCNN, and (c) SCNN.

To further analyze the recognition ability of the IRNet, the recognition confusion matrix at −10 and −8 dB is shown in Fig. 14. At −10 dB, the major recognition error is RFN signals; 18 samples of RFN are misclassified as CS, 17 samples are misclassified as FMCW, and eight samples are misclassified as PCW. Also, merely one sample of FMCW is misclassified as FSK. The recognition performance is much better at −8 dB. All types of interference except the RFN are classified correctly, while 13 samples of RFN are still misclassified. Therefore, the autocorrelation features of the CS, FMCW, PCW, and RFN at −10 dB are shown in Fig. 15.

Obviously, due to the AWGN, the autocorrelation features are disturbed by the transmitting noise so that these features are becoming confused with each other, that is, the transmitting noise does influence and disturb received signals, which leads to the misclassification of the RFN in our works. Actually, the autocorrelation features of the FMCW, CS, and RFN are very similar even under noise-free conditions shown in Figs. 6, 7, and 9, respectively. Fortunately, the proposed IRNet gains great deep feature extraction ability and adaptive feature selection to achieve better recognition performance for these types of interference signals at higher JNRs.

## D. Comparison Results of Different Networks

To verify the efficiency of the proposed IRNet, six stateof-the-art networks, including the original SENet [33], the

VGG [19], the SJRNet [20], the PCNN [18], the RCNN [21], and the SCNN [22], are compared and analyzed on results of OA, mOA, Ka, and the computational complexity.

1) Performance Varied With JNR: Similarly, the results of OAs against JNR for each comparison network are given in Figs. 16 and 17. The original SENet achieves more than 50% average OAs at −16 dB and the OAs of most kinds of interference signals are close to 100% at −12 dB. When JNR > 0 dB, OAs of all eight types converge to 100%. As for the VGG, OAs of most types of interference are lower than 60% and the OA of CW is about 84.7% at −16 dB. Also, at −12 dB, OAs of BPSK, CS, CW, FMN, FSK, and PCW are almost 100%, while OAs of FMCW and RFN are still lower than 60%. Until 2 dB, OAs of all eight types converge to 100%. Similar to the VGG, OAs of most types for the SJRNet are worse than 60% at −16 dB, while the OA of CW is about 97.1%. At −10 dB, OAs of BPSK, CS, CW, FMN, FSK, and PCW are close to 100%. When JNR > 0 dB, OAs of all eight types converge to 100%.

The recognition performance of the PCNN is much worse. OAs of eight types are all much lower than 50% at −16 dB and all OAs are close to 100% at 6 dB. For the RCNN, OAs of CW and FMCW are about 80.8% and 65.7%, respectively, while OAs of other types are lower than 30% at −16 dB. Until 4 dB, all OAs are close to 100%. Similar to the SCNN, OAs of FMCW and CW are about 78.3% and 60.8%, respectively, while OAs of other types are lower than 20%. Also, until 6 dB, all OAs converge to 100%.

To compare the recognition performance of several methods more clearly, the mOAs against JNRs of both the proposed IRNet and six comparison networks are shown in Fig. 18.

TABLE III  
OA OF THE SIX METHODS FOR EACH KIND OF INTERFERENCE (AVERAGE VALUE ± STANDARD DEVIATION)
<table><tr><td>OA (%)</td><td>BPSK</td><td>CS</td><td>CW</td><td>FMCW</td><td>FMN</td><td>FSK</td><td>PCW</td><td>RFN</td></tr><tr><td>VGG</td><td>97.16±0.49</td><td>96.24±0.99</td><td>99.15±0.68</td><td>91.36±1.56</td><td>94.92±0.97</td><td>97.27±1.63</td><td>92.22±1.37</td><td>84.03±1.21</td></tr><tr><td>SJRNET</td><td>97.9±0.34</td><td>96.44±0.49</td><td>99.85±0.17</td><td>91.65±2.99</td><td>96.91±0.80</td><td>98.57±0.50</td><td>94.83±0.21</td><td>84.47±1.79</td></tr><tr><td>PCNN</td><td>91.94±1.23</td><td>87.52±1.22</td><td>94.6±0.05</td><td>99.23±1.0</td><td>89.6±0.47</td><td>89.79±0.21</td><td>84.52±0.22</td><td>81.47±2.72</td></tr><tr><td>RCNN</td><td>96.05±0.61</td><td>91.05±0.25</td><td>98.99±0.24</td><td>93.39±1.24</td><td>93.95±0.53</td><td>94.92±0.74</td><td>89.78±0.44</td><td>79.96±3.58</td></tr><tr><td>SCNN</td><td>95.35±0.34</td><td>90.99±0.37</td><td>97.94±0.86</td><td>75.14±3.77</td><td>94.03±0.50</td><td>94.6±0.29</td><td>89.14±0.35</td><td>72.3±1.09</td></tr><tr><td>SE</td><td>97.61±0.43</td><td>96.42±0.37</td><td>99.83±0.06</td><td>84.58±2.96</td><td>96.97±0.67</td><td>98.18±0.22</td><td>94.45±0.43</td><td>88.29±1.69</td></tr><tr><td>IRNET</td><td>98.84±0.13</td><td>97.69±0.19</td><td>99.99±0.01</td><td>99.88±0.14</td><td>98.02±0.32</td><td>98.93±0.04</td><td>95.13±0.11</td><td>89.38±1.36</td></tr></table>

![](images/731a2bce433bb5b1d49d82b24755efa22287812ccab23a82bac40c57e4290907.jpg)  
Fig. 18. mOAs against JNRs of seven methods.

At −16 dB, the mOAs of the IRNet are about 67.81%, which is nearly 17.38%, 27.96%, 17.76%, 59.96%, 41.5%, and 48.11% higher than those of the SENet, VGG, SJRNet, PCNN, RCNN, and SCNN, respectively. Also, at −14 dB, the mOAs of the IRNet are more than 90%, while the mOAs of the SENet, VGG, SJRNet, PCNN, RCNN, and SCNN are about 81.74%, 75.13%, 77.03%, 30.82%, 65.91%, and 62.83%, respectively. Until −8 dB, the mOAs of the IRNet are close to 100% and keep stable, which are about 5.44%, 7.9%, 6.04%, 8.44%, 5.27%, and 9.62% higher than those of the SENet, VGG, SJRNet, PCNN, RCNN, and SCNN, respectively. Until 2 dB, the mOAs of six comparison networks converge to 100%, that is, it takes about 8 dB for the mOAs of the IRNet to converge to 100%, while it takes about 18 dB for the mOAs of the SENet, VGG, SJRNet, PCNN, RCNN, and SCNN to converge to 100%.

On the whole, the recognition performance of the proposed IRNet is much better than these five comparison networks at low JNRs. As JNR improves, the recognition accuracy of the IRNet converges fastest than that of comparison networks. In particular, the IRNet achieves better performance than the original SENet under lower JNR conditions.

2) Performance of OA and Ka: The OA of each network for each type of interference is shown in Table III. Especially for the RFN, the OA of the IRNet is 89.38% ± 1.35%, which is about 1.09%, 5.35%, 4.92%, 7.91%, 9.42%, and 17.08% higher than that of the SENet, VGG, SJRNet, PCNN, RCNN, and SCNN, respectively. The OAs of the IRNet for the BPSK, CS, CW, FMCW, FMN, FSK, and PCW are at least 0.94%, 1.25%, 0.14%, 0.65%, 1.04%, 0.36%, and 0.3% higher than comparison networks, respectively. For the CW, OAs of the SENet and SJRNet are nearly as good as the OA of the IRNet. The OA of the PCNN for FMCW is similar to the OA of the IRNet and the OA of the SJRNet for FSK is close to the OA of the IRNet. On the whole, the IRNet owns higher OA for all eight types of interference compared with comparison methods, that is, the proposed IRNet also outperforms the original SENet from the perspective of OAs.

![](images/841fb5a0b7ef1b0d2165afbb640fb630b659fca59a28df52aacef3f675d364c6.jpg)

(a)  
![](images/48f08c71bfd0bc3140fb1d4d719a97a09f09c647580f06d50a9af78ed7200216.jpg)  
(b)  
Fig. 19. (a) Employed millimeter-wave radar platform and (b) jammer.

Also, the mOA and Ka of each network are given in Table IV. mOA of the proposed IRNet is 97.23% ± 0.13%, which is about 2.69%, 3.37%, 2.76%, 7.82%, 4.82%, and 5.83% higher than that of the SENet, VGG, SJRNet, PCNN.

TABLE IV  
MOA AND KA OF THE SIX METHODS (AVERAGE $\mathrm { \Delta V _ { A L U E } } \pm \mathrm { \Delta S ^ { \prime } }$ TANDARD DEVIATION)
<table><tr><td></td><td>VGG</td><td>SJRNET</td><td>PCNN</td><td>RCNN</td><td>SCNN</td><td>SE</td><td>IRNET</td></tr><tr><td>MOA (%)</td><td>93.86±0.62</td><td>94.47±0.61</td><td> $8 9 . 4 1 { \pm } 1 . 2 8 $ </td><td>92.41±0.60</td><td>91.4±0.27</td><td> $9 4 . 5 4 \pm 0 . 2 8 $ </td><td>97.23±0.12</td></tr><tr><td>KA(×100)</td><td> $9 3 . 0 5 { \pm } 6 \times \mathrm { e } ^ { - 3 }$ </td><td> $9 3 . 7 3 { \pm } 5 \times \mathrm { e } ^ { - 3 }$ </td><td> $8 8 . 0 8 { \pm } 0 . 0 2 $ </td><td> $9 1 . 4 2 { \pm } 7 \times \mathrm { e } ^ { - 3 }$ </td><td> $9 0 . 2 9 { \pm } 4 \times \mathrm { e } ^ { - 3 }$ </td><td>93.81±2×  $\mathbf { e } ^ { - 3 }$ </td><td> $\mathbf { 9 6 . 8 5 { \pm } 5 \times e ^ { - 4 } }$ </td></tr></table>

RCNN, and SCNN, respectively. Ka of the IRNet is 96.85 ± $5 \times 1 0 ^ { - 4 }$ , which is nearly 3.04, 3.8, 3.12, 8.77, 5.43, and 6.56 higher than that of the SENet, VGG, SJRNet, PCNN, RCNN, and SCNN, respectively. Therefore, the proposed IRNet gains more superiorities for automotive radar interference recognition compared with six state-of-the-art methods. In particular, although compared with other comparison networks, the mOAs and Ka of SENet are closer to those of the IRNet, and the proposed IRNet owns better performance on both the mOAs and Ka, which verifies the effectiveness of the proposed structure.

3) Results on Measured Signals: Indeed, it is not completely convincing to measure recognition performance only by simulation datasets due to real requirements in complex transmission environments while it is really a big challenge to obtain adequate measured interference signals, especially those intended interference signals, which leads to the fact that most existing methods fail to analyze the recognition ability of measured signals.

In our works, a millimeter-wave (mmW) radar platform, shown in Fig. 19(a), is employed as an automotive radar. The carrier frequency is 77 GHz, the frequency slope is 70.295 MHz, the sampling frequency is 5 MHz, the pulsewidth is 12.5 ms, the chirp duration is 56.87 μs, and the Azimuth FOV is 120<sup>◦</sup>. As for interference signals, especially intended interference signals, a certain military jammer is used and shown in Fig. 19(b). We have tried our best to collect more kinds of interference signals due to limited hardware systems, and finally, five types of interference signals, including CS, CW, FMCW, PCW, and FMN, are obtained and employed as the measured dataset. The employed mmW radar has one transmitting channel and four receiving channels, and measured interference signals to be recognized are randomly collected from these four receiving channels. The received SNR is about 30 dB, and these interference signals are intercepted, resampled, and normalized to ensure that they obey the same distribution as the training dataset before recognition. To obtain valid results, 200 samples of each kind of signal are collected.

According to comparison results in simulation datasets, the IRNet, SENet, VGG, and SJRNet all obtain satisfactory performance, and thus, their recognition ability of measured signals is further explored in this section. The recognition results on measured signals are shown in Fig. 20. Obviously, for simple modulation interference signals such as CW and PCW, the recognition accuracy of four methods is all close to 100%, which not only demonstrates the ability of CNNs but also verifies the robustness of autocorrelation features.

![](images/ef978e69f1a111544200f4dcb72d02b4ad011b8d1c0f3b4237e062a353de3ed9.jpg)  
Fig. 20. Comparison results on measured signals.

For FMCW signals, the recognition accuracy of IRNet is about 97%, while the accuracy of SENet is about 82%, that is, the proposed structure has more powerful generalization ability. For CS signals, only the IRNet could achieve more than 90% recognition accuracy. As for intended interference FMN signals, the accuracy of IRNet is about 96.5%, while the accuracy of SENet, VGG, and SJRNet is about 90%, 73.5%, and 81%, respectively. Thus, the proposed IRNet still outperforms these three competitive comparison methods.

4) Computational Complexity: Since the interference recognition for automotive radars requires real-time processing to some extent, the computational complexity of these methods should be considered. Both the proposed IRNet and five comparison networks are all based on CNNs. In general, the computational complexity of CNNs is always measured through floating-point operations (FLOPs) and the number of learnable parameters. The FLOPs reveal the complexity of an algorithm or a model and the number of learnable parameters indicates the time consumption and needed storage source. Also, the FLOPs of a convolutional layer FLOPs and a full connection layer FLOPs can be calculated as [20]

$$
\mathrm { F L O P } s _ { c } = \left( 2 \times C _ { i } \times K ^ { 2 } - 1 \right) \times H \times W \times C _ { o }\tag{28}
$$

$$
\mathrm { F L O P } s _ { f } = ( 2 \times I - 1 ) \times O\tag{29}
$$

where $C _ { i }$ and $C _ { o }$ are input channels and output channels, respectively, K denotes the kernel size, H and W are the sizes of output feature maps, and I and O are the numbers of input neurons and output neurons, respectively.

The FLOPs and numbers of learnable parameters of each network are given in Table V. The FLOPs of the proposed

TABLE V  
COMPUTATIONAL COMPLEXITY OF ALL METHODS
<table><tr><td>Methods</td><td>Learnable Parameters (M)</td><td>FLOPs (G)</td></tr><tr><td>VGG</td><td>138.36</td><td>15.5</td></tr><tr><td>SJRNet</td><td>27.82</td><td>4.8</td></tr><tr><td>PCNN</td><td>8.67</td><td>1.05</td></tr><tr><td>RCNN</td><td>13.12</td><td>0.48</td></tr><tr><td>SCNN</td><td>6.32</td><td>0.26</td></tr><tr><td>SE</td><td>21.7</td><td>3.68</td></tr><tr><td>IRNet</td><td>26.68</td><td>3.87</td></tr></table>

IRNet are 4.8 G and the number of learnable parameters is 26.68 M. Compared with comparison networks, the FLOPs of the IRNet are 0.93 G and 11.63 G less than that of the VGG and SJRNet but 0.21, 2.82, 3.39, and 3.61 G more than that of the SENet, PCNN, RCNN, and SCNN, respectively. The number of learnable parameters of the IRNet is 1.14 and 111.68 M less than that of the VGG and SJRNet but 4.98, 18.01, 13.56, and 20.36 M more than that of the SENet, PCNN, RCNN, and SCNN, respectively. According to the results analyzed above, the SENet and SJRNet own better recognition ability among six comparison methods, while compared with the IRNet, the IRNet outperforms SJRNet with fewer FLOPs and fewer learnable parameters. Compared with the original SENet, the increase in computational complexity of IRNet is relatively small.

To summarize, the proposed IRNet can achieve much better recognition performance of the automotive radar interference with relatively less and acceptable computational complexity.

## V. CONCLUSION

In this article, to deal with the interference recognition for automotive radars, a CNN-based recognition method was proposed to recognize eight types of interference signals, including mutual interference, unintended interference, and adverse intended interference. Besides, the transmitting noise was taken into consideration in our works. The proposed method consists of a novel IRNet that owns significant representation power and adaptive feature selection ability and autocorrelation features. The robustness of autocorrelation features is verified via simulations. The simulation results indicate that the mOAs of the IRNet can achieve 90.85% at −14 dB and nearly 100% when JNR > −8 dB. The mOAs for all eight types of interference signals are 97.23% ± 0.13% and Ka is $9 6 . 8 5 \pm 5 \times 1 0 ^ { - 4 }$ . Compared with the original SENet, VGG, SJRNet, PCNN, RCNN, and SCNN, the proposed method can achieve much better and stable recognition performance, especially at lower JNRs. Results on measured signals also verify that the IRNet achieves higher accuracy than three competitive comparison methods. About the computational complexity, the proposed method owns 3.87 G FLOPs and 26.68 M learnable parameters, which is less than the VGG and SJRNet. To summarize, the proposed outperforms these six comparison methods with relatively lower and acceptable computational complexity.

Nevertheless, the real autonomous driving environments may be much more complex than the considered scenarios. For example, the received signals are only partially distorted by interference in most real cases. In the future, more physical characteristic parameters and real cases are supposed to be considered in our works. Besides, for the sake of applications of the IRNet, we will attempt to verify the proposed method on deep-learning chips and hardware platforms.

## REFERENCES

[1] K. Ren, Q. Wang, C. Wang, Z. Qin, and X. Lin, “The security of autonomous driving: Threats, defenses, and future directions,” Proc. IEEE, vol. 108, no. 2, pp. 357–372, Feb. 2020.

[2] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[3] H. Shin et al., “Illusion and dazzle: Adversarial optical channel exploits against lidars for automotive applications,” in Proc. Int. Conf. Cryptograph. Hardw. Embedded Syst. (CHES). Cham, Switzerland: Springer, 2017, pp. 445–467.

[4] C. Bahlmann, Y. Zhu, V. Ramesh, M. Pellkofer, and T. Koehler, “A system for traffic sign detection, tracking, and recognition using color, shape, and motion information,” in Proc. IEEE Intell. Veh. Symp., Dec. 2005, pp. 255–260.

[5] Q. Du et al., “Fusing infrared and visible images of different resolutions via total variation model,” Sensors, vol. 18, no. 11, pp. 3827–3844, 2018.

[6] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[7] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[8] W. Buller et al., “Radar congestion study,” Nat. Highway Traffic Saf. Admin., Washington, DC, USA, Tech. Rep. DOT HS 812, 2018, vol. 632.

[9] C. Yan, W. Xu, and J. Liu, “Can you trust autonomous vehicles: Contactless attacks against sensors of self-driving vehicle,” in Proc. DEFCON, vol. 24, 2016, p. 106.

[10] H. Bloecher and J. Dickmann, “Automotive radar sensor interference— Thread and probable countermeasures,” in Proc. 19th Int. Radar Symp. (IRS), Bonn, Germany, 2018, pp. 1–7.

[11] A. Stove and C. Baker, “Radio-frequency interference to automotive radar sensors,” IET Radar, Sonar Navigat., vol. 12, no. 10, pp. 1154–1164, Oct. 2018.

[12] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 315–320.

[13] Z. Xu and M. Yuan, “An interference mitigation technique for automotive millimeter wave radars in the tunable Q-factor wavelet transform domain,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 12, pp. 5270–5283, Dec. 2021.

[14] P. Liu, Y. Liu, T. Huang, Y. Lu, and X. Wang, “Decentralized automotive radar spectrum allocation to avoid mutual interference using reinforcement learning,” IEEE Trans. Aerosp. Electron. Syst., vol. 57, no. 1, pp. 190–205, Feb. 2021.

[15] E. Cardillo, C. Li, and A. Caddemi, “Vital sign detection and radar selfmotion cancellation through clutter identification,” IEEE Trans. Microw. Theory Techn., vol. 69, no. 3, pp. 1932–1942, Mar. 2021.

[16] J. Kim, S. Lee, and S. Kim, “Modulation type classification of interference signals in automotive radar systems,” IET Radar, Sonar Navigat., vol. 13, no. 6, pp. 944–952, Jun. 2019.

[17] R. Zhang and S. Cao, “Support vector machines for classification of automotive radar interference,” in Proc. IEEE Radar Conf., Apr. 2018, pp. 0366–0371.

[18] J. Kim et al., “Classification of interference signal for automotive radar systems with convolutional neural network,” IEEE Access, vol. 8, pp. 176717–176727, 2020.

[19] Y. Junfei, L. Jingwen, S. Bing, and J. Yuming, “Barrage jamming detection and classification based on convolutional neural network for synthetic aperture radar,” in Proc. IGARSS - IEEE Int. Geosci. Remote Sens. Symp., Jul. 2018, pp. 4583–4586.

[20] Q. Qu, S. Wei, S. Liu, J. Liang, and J. Shi, “JRNet: Jamming recognition networks for radar compound suppression jamming signals,” IEEE Trans. Veh. Technol., vol. 69, no. 12, pp. 15035–15045, Dec. 2020.

[21] Q. Liu and W. Zhang, “Deep learning and recognition of radar jamming based on CNN,” in Proc. 12th Int. Symp. Comput. Intell. Design (ISCID), Hangzhou, China, Dec. 2019, pp. 208–212.

[22] Y. Wang, B. Sun, and N. Wang, “Recognition of radar active-jamming through convolutional neural networks,” J. Eng., vol. 2019, no. 21, pp. 7695–7697, Nov. 2019.

[23] M. Goppelt et al., “Automotive radar-investigation of mutual interference machanisms,” Adv. Radio Sci., vol. 8, pp. 55–60, 2010.

[24] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., vol. 1, Jun. 2016, pp. 770–778.

[25] S. Wei et al., “Automatic modulation recognition for radar signals via multi-branch ACSE networks,” IEEE Access, vol. 8, pp. 94923–94935, 2020.

[26] Q. Qu, S. Wei, Y. Wu, and M. Wang, “ACSE networks and autocorrelation features for PRI modulation recognition,” IEEE Commun. Lett., vol. 24, no. 8, pp. 1729–1733, Aug. 2020.

[27] E. R. Yeh et al., “Security in automotive radar and vehicular networks,” Microw. J., vol. 60, no. 5, pp. 148–164, 2017.

[28] B. Daxiang, “A study of radar jamming type discrimination,” M.S. thesis, School Electron. Eng., Xidian Univ., Xi’an, China, 2015.

[29] Q. Xipeng, Neural Networks and Deep Learning. Beijing China: Machine Press, 2020, pp. 25–35.

[30] M. A. Nielsen, Neural Networks and Deep Learning. Determination Press, 2015.

[31] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” 2014, arXiv:1412.6980.

[32] J. Cao et al., “DO-Conv: Depthwise over-parameterized convolutional layer,” 2020, arXiv:2006.12030.

[33] J. Hu, L. Shen, and G. Sun, “Squeeze-and-excitation networks,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Dec. 2018, pp. 7132–7141.

[34] K. He, X. Zhang, S. Ren, and J. Sun, “Delving deep into rectifiers: Surpassing human-level performance on imagenet classification,” in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), Santiago, Chile, Dec. 2015, pp. 1026–1034.

[35] M. N. Sumaiya and R. S. S. Kumari, “Logarithmic mean-based thresholding for SAR image change detection,” IEEE Geosci. Remote Sens. Lett., vol. 13, no. 11, pp. 1726–1728, Nov. 2016.

[36] L. van der Maaten and G. Hinton, “Visualizing data using t-SNE,” J. Mach. Learn. Res., vol. 9, pp. 2579–2605, Dec. 2008.

![](images/9e1c183111138b54314af2204b47f73901ffeb35c4cfa07b9bdc78b0e544ac74.jpg)  
Qizhe Qu received the B.S. degree in information countermeasure technology from the North University of China, Taiyuan, China, in 2018, and the M.S. degree in electronics and communication engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2021. He is currently pursuing the Ph.D. degree with the Electronic Information School, Wuhan University, Wuhan, China.

His current research interests include electronic countermeasures and deep learning.

![](images/109b752949e36fe3138bbb699d848fb51728f699e7ed5dcc4ce20d881ae73451.jpg)

Yong-Liang Wang received the Ph.D. degree in electrical engineering from Xidian University, Xian, China, in 1994.

From June 1994 to December 1996, he was a Post-Doctoral Fellow with the Department of Electronic Engineering, Tsinghua University, Beijing, China. He has been a Full Professor since 1996, and he was the Director of the Key Research Laboratory, Wuhan Radar Academy, Wuhan, China, from 1997 to 2005. He is currently a Full Professor with the Wuhan Electronic Information Institute, Wuhan, and

also a Doctoral supervisor with the Electronic Information School, Wuhan University, Wuhan. He has authored or coauthored three books and more than 200 articles. His recent research interests include radar systems, space–time adaptive processing, and array signal processing.

Dr. Wang is a member of the Chinese Academy of Sciences and a Fellow of the Chinese Institute of Electronics. He was a recipient of the China Postdoctoral Award in 2001 and the Outstanding Young Teachers Award of the Ministry of Education, China, in 2001.

![](images/9617b9327a4d99d4c48d293359c0b43bebbd7c1f261e17ef2295f8312f973905.jpg)

Weijian Liu (Senior Member, IEEE) received the B.S. degree in information engineering and the M.S. degree in signal and information processing from the Wuhan Radar Academy, Wuhan, China, in 2006 and 2009, respectively, and the Ph.D. degree in information and communication engineering from the National University of Defense Technology, Changsha, China, in 2014, respectively.

He is currently an Associate Professor with the Wuhan Electronic Information Institute, Wuhan, China. His current research interests include mul-

tichannel signal detection, statistical, and array signal processing.

Dr. Liu is an Associate Editor of the Circuits, Systems, and Signal Processing.

![](images/7749e70e103818718c1275b84813e4834ef704ee70fabadd61c7feec28fee10a.jpg)

Shunjun Wei (Member, IEEE) received the B.S., M.S., and Ph.D. degrees in electronic engineering from the University of Electronic Science and Technology of China (UESTC), Chengdu, China, in 2006, 2009, and 2013, respectively.

He is currently an Associate Professor with UESTC. His research interests include radar signal processing, machine learning, and synthetic aperture radar systems.

![](images/3c93fbca8128f50c0779b350f7c7ab1ac9b707e59e9336a97ac348c58d10c94e.jpg)

Qinglei Du received the B.S. degree in measure and control engineering, the B.S. degree in computer science and technology, and the M.S. degree in electronics engineering from the Mechanical and Electronics School, Wuhan University of Technology, Wuhan, China, in 2005 and 2007, respectively, and the Ph.D. degree in signal and information processing from the Electronic Information School, Wuhan University, Wuhan, in 2019.

He is currently an Associate Professor with the Wuhan Electronic Information Institute, Wuhan. His

current research interests include radar target detection, recognition, and digital image processing.