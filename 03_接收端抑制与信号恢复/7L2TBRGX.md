# End-to-End Trainable Deep Neural Network for Radar Interference Detection and Mitigation

Marvin Klemp<sup>∗</sup>, Shengyi Chen<sup>†</sup>, Royden Wagner<sup>∗</sup>, Martin Lauer<sup>∗</sup>

<sup>∗</sup>Institute of Measurement and Control Systems Karlsruhe Institute of Technology 76131 Karlsruhe, Germany {marvin.klemp, royden.wagner, martin.lauer}@kit.edu <sup>†</sup>Institute of Communication Acoustics Ruhr-Universitat Bochum¨ 44801 Bochum, Germany shengyi.chen@rub.de

Abstract—The automotive radar sensor is an essential sensor for intelligent transportation systems. However, the increasing number of such systems leads to mutual interference between sensors. Radar interference can be a severe disturbance, where targets within the victim radar are not perceived anymore if no countermeasures are taken. To prevent fatal injuries caused by this disturbance, several classical and deep-learning based methods to detect and mitigate radar interference have been proposed. We present an end-to-end trainable deep neural network for radar interference detection and mitigation. We evaluate different radar interference detection and mitigation methods on a large scale urban driving dataset using simulated radar interference. To our knowledge, this is the first end-to-end trainable architecture for interference detection and mitigation in the time domain. We show that our method achieves state-ofthe-art results in interference detection and mitigation. Code for our method, reference methods, simulation, and the evaluation is available at https://github.com/KIT-MRT/ridam.

Index Terms—radar interference mitigation, deep learning, radar signal processing, automotive radar

## I. INTRODUCTION

Safety, or reducing the amount of injuries is a fundamental aim of intelligent transportation systems (ITSs). To achieve this, the environment of such systems must be perceived in a robust way. Therefore, ITSs are equipped with a wide range of different sensors. Among these, the automotive radar sensors are a key technology, providing the distance, angle, and radial velocity of targets, even in adverse weather conditions.

However, due to its operating principle, such sensors are sensitive to interference. An interfering radar sends its signal directly or indirectly into a victim radar which falsely interprets this signal as a reflection of a target. The usage of the interference-contaminated signal may lead to non-existing, socalled ghost targets, or an increased noise floor, which may hide weakly reflecting targets like pedestrians or cyclists. Fig. 1 shows a range-Doppler spectrum (RDS) heavily disturbed by mutual radar interference. In the disturbed RDS targets are significantly harder to detect.

As the number of ITSs is increasing, the amount of radar sensors on the road increases accordingly, resulting in unavoidable radar interference. The MORASIM project [1] investigated the impacts of radar interference and resulted in different guidelines for radar interference mitigation.

![](images/fefd93008ccdcccf234c6435e86eb0c8938a5b0385f7997249664076e8b7a631.jpg)  
(a) Interference-free RDS

![](images/846a3c9588d7a5514afe3b20b7b96d1b6880f0aec9eb875563e481d99d5e316e.jpg)  
(b) Interference-contaminated RDS  
Fig. 1: a) An interference-free and b) a RDS disturbed by simulated radar interference.

One proposed counter-measure that is applicable in a wide range of scenarios is to detect, discard, and reconstruct the disturbed intermediate frequency (IF) signal in the time domain.

We follow this suggestion and design a multi-task deeplearning architecture implementing the detect, discard, and reconstruct paradigm in the time domain. Our main contributions are summarized as follows:

• We present a real-time capable simulation framework for non-coherent radar interference based on radar parameters of the victim and multiple interfering radars.

• We propose an end-to-end trainable multi-task deeplearning architecture for radar interference detection and mitigation.

• Based on the evaluations for interference detection, we show that deep-learning methods strongly outperform classical radar interference detection methods.

• We conclude that mitigation methods in the time-domain are heavily influenced by the quality of interference detections.

• In out interference mitigation evaluation, we show that our mitigation method achieves state-of-the-art results in multiple metrics and is safe to apply in non-interference situations.

## II. RELATED WORK

## A. Interference Detection Methods

(MSER) Barjenbruch et al. [2] construct a logarithmically scaled image based on the radar frame. They reason that radar interference introduces a constant change to the amplitude of the analog-to-digital converter (ADC) samples of the IF signal. This leads to visually different features. To detect them, they use the maximally stable extremal regions algorithm and provide a mask of interference-contaminated samples.

(VARIATION) Radar interference adds additional frequencies to the received signal. Watanabe and Natsume [3] propose a thresholding method based on the variation of the amplitude in fast-time samples for detecting interference.

(LAPLACIAN) Chen et al. [4] extend this idea and detect interference by using a Laplacian edge detector in fast-time samples.

(AE-GATE) Chen et al. [5] propose a deep-learning based two-stage architecture for radar interference detection and mitigation. For the detection task, they use a CNN-based autoencoder. Its input is the interference-contaminated radar frame and results in a mask of disturbed ADC samples.

## B. Interference Mitigation Methods

(ZEROING) Brooker [6] proposes an interference reduction method by setting interference-contaminated samples to zero.

(AR) Rameez et al. [7] mitigate interference by replacing the disturbed ADC samples with recovered samples using autoregressive (AR) models. For the detection of interferencecontaminated samples the VARIATION method is used.

(CNN-TD) Rameez [8] evaluates the performance of different deep-learning based radar interference mitigation methods. From these, we evaluate the proposed CNN architecture that reconstructs the radar frame in the time domain. The method requires the disturbed radar frame and a mask of interference detections as input. For interference detection the VARIATION method is used.

(AE-GATE) Chen et al. [5] detect disturbed ADC samples using the CNN-based autoencoder, discard, and reconstruct them using an autoencoder architecture based on gated convolutions. As input, interference-free ADC samples and the detection mask are used. Using the detection mask, disturbed samples are set to zero. Furthermore, solely the interferencecontaminated ADC samples are recovered.

(CNN-RD) Rock et al. [9] propose a deep learning architecture primarily based on convolution, batch norm and ReLu layers. In contrast to other methods, they mitigate the radar interference in the range-Doppler domain.

## III. RADAR INTERFERENCE

## A. Radar Datasets

Obtaining a real-world radar interference dataset is difficult and time-consuming. Furthermore, radar manufacturers mitigate radar interference on-chip and often only publish already processed radar data in the form of point clusters or detected objects. Hence, only a few datasets containing radar frames are publicly available and no dataset for the sole purpose of radar interference mitigation is available to this date. In consequence, we simulate the mutual radar interference based on parameters of multiple interfering and one victim radar and add the simulated interference to the radar frame. In our experiments, we use the RaDICal dataset [10], which provides raw ADC samples recorded by a Texas Instruments IWR1443-BOOST<sup>1</sup> radar. The dataset provides different capturing configurations, we use the data captured using the 30m configuration, resulting in 192 fast-time and 64 slow-time samples in each radar frame. The exact parameters of this configuration are shown in Table I. In total, we use 75000 radar frames recorded in different urban driving situations. We split them into 60000 training frames and 15000 validation and test frames.

TABLE I: Parameters of the ego (victim) radar
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Carrier frequency</td><td>77 GHz</td></tr><tr><td>Bandwidth</td><td>1150 MHz</td></tr><tr><td>Chirp duration</td><td>23.33 µs</td></tr><tr><td>Slow-time samples</td><td>64</td></tr><tr><td>Fast-time samples</td><td>192</td></tr><tr><td>LPF cutoff frequency</td><td>15 MHz</td></tr></table>

## B. Automotive Radar Processing Pipeline

So far, automotive radars widely adopt Frequency Modulated Continuous Wave (FMCW) techniques. To simulate mutual radar interference an in-depth understanding of the FMCW radar pipeline is mandatory. This section provides a short review of the mandatory components.

An FMCW radar transmits an electromagnetic sinusoidal wave modulated linearly in frequency. This signal is reflected with a time delay τ by different targets such as pedestrians, cyclists, cars or static targets. Reflections are received by one or multiple radar antennas. Afterwards, the reflection is compared with the transmitted signal through a mixer component. Resulting in the absolute difference in frequency between the transmitted and received signal. This beat frequency (IF signal) is passed through a low pass filter (LPF) to remove high-frequency components and converted into a digital representation using an ADC. A full transmission is called chirp and a radar frame consists of multiple chirps. Based on the radar frame, properties of the reflecting targets e.g. distance, radial velocity, and angle are calculated.

## C. Mutual Radar Interference

We assume both victim and interfering radars employ FMCW technology. Especially important parameters for the simulation of mutual radar interference are the carrier frequency $f _ { c } ,$ the slope k, the chirp duration $t _ { c } ,$ and the LPF cutoff frequency $f _ { c u t }$ of the victim radar.

In our simulation, we focus on the non-coherent interference. Non-coherent interference occurs, if both radars have different parameters. In this case, the received signal is only disturbed in special conditions. As the slope of both signals are different, most of the received interfering signal is outside of the LPF cutoff frequency and therefore filtered out. Hence, ADC samples from the IF signal are only disturbed if the beat frequency is smaller than the LPF cutoff frequency.

![](images/f0c2e5a391548e78ae9e913abf5d26cf3e4ff78e124ca12cd16fe29780475e6c.jpg)  
Fig. 2: Architecture of the RIDAM method. Feature concatenations from encoder to both heads are not visualized.

TABLE II: Parameters of the interfering radars used by our simulation. For each interfering radar, parameters are uniformly sampled between the minimum and maximum value.
<table><tr><td>Parameter</td><td>Min</td><td>Max</td></tr><tr><td>Carrier frequency</td><td>77GHz</td><td>78GHz</td></tr><tr><td>Bandwidth</td><td>100MHz</td><td>1000MHz</td></tr><tr><td>Number of chirps</td><td>16</td><td>512</td></tr><tr><td>Chirp duration</td><td>15μs</td><td>100µs</td></tr><tr><td>Number of interfering radars</td><td>0</td><td>4</td></tr></table>

If this is the case, additional frequencies are present in the disturbed signal. These frequencies start at the LPF cutoff frequency and decrease until they reach 0Hz. As both signals are subtracted in the mixer component this is exactly the case once the reflecting and the interfering signal have the same frequency. We call this interference bust position. Afterwards, the frequency increases until reaching the LPF cutoff frequency. Then the difference in frequency exceeds the LPF cutoff frequency and the interfering signal is filtered out by the LPF.

1) Simulation of Non-Coherent Interference: To simulate non-coherent interference, we require knowledge of the victim and the interfering radar parameters. Based on the parameters of an interfering radar, our simulation pipeline is implemented in two steps.

First, for the chirps of a given interfering radar and for all chirps of the victim radar interference burst positions are calculated. For this, we represent victim and interfering radar as sawtooth signal. Using this representation we subtract both signals and compute the roots. Each root is an interference bust position. Around these, ADC samples of the victim radar are disturbed.

Second, based on the absolute difference between the slope of the victim radar, the interfering radar, and the LPF cutoff frequency of the victim radar, the period in which ADC samples are disturbed around an interference burst position are calculated by

$$
t _ { i n t } = \frac { | k _ { v } - k _ { i } | } { f _ { c u t } } ,
$$

where $k _ { v }$ and $k _ { i }$ are the victim and interfering radar slopes. We simulate a sinusoidal signal modulated in frequency ranging from 0Hz to the LPF cutoff frequency over $t _ { i n t }$ seconds, and add this interference around the interference burst position to the interference-free ADC samples based on the sampling rate of the victim radar. Considering this procedure, the IF signal including simulated mutual radar interference can be modeled as

$$
\operatorname { R F } [ n , m ] = \sum _ { t } ^ { N _ { t } } \operatorname { R } _ { t } [ n , m ] + \sum _ { i } ^ { N _ { i } } \operatorname { I } _ { i } [ n , m ] + v [ n , m ] ,
$$

where RF is the sampled IF signal, n and m are the indexes of the fast and slow-time sample. $\mathbb { R } _ { t } [ n , m ]$ and $\mathrm { I } _ { i } [ n , m ]$ are the signal components of the t-th target reflection and i-th interfering radar, respectively. $N _ { t }$ is the number of target reflections and $N _ { i }$ is the number of interfering radars, and v[n, m] is the receiver noise.

TABLE III: Results of the interference detection evaluation. Note that radar frames are biased towards having more interferencefree samples compared to disturbed samples. Hence, even small differences in precision, recall, and F1-score may degrade mitigation methods.
<table><tr><td></td><td colspan="3">Weak</td><td colspan="3">Medium</td><td colspan="3">Strong</td></tr><tr><td></td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td></tr><tr><td colspan="10">CLASSICAL</td></tr><tr><td>MSER [2]</td><td>0.9576</td><td>0.9815</td><td>0.9694</td><td>0.9381</td><td>0.9781</td><td>0.9577</td><td>0.8267</td><td>0.979</td><td>0.8964</td></tr><tr><td>VARIATION [3]</td><td>0.9420</td><td>0.9970</td><td>0.9687</td><td>0.9092</td><td>0.9966</td><td>0.9509</td><td>0.7666</td><td>0.9919</td><td>0.8648</td></tr><tr><td>LAPLACIAN [4]</td><td>0.9528</td><td>0.9756</td><td>0.9640</td><td>0.913</td><td>0.9319</td><td>0.9224</td><td>0.7642</td><td>0.8454</td><td>0.8028</td></tr><tr><td colspan="10">DEEP-LEARNING BASED</td></tr><tr><td>AE-GATE [5]</td><td>0.9998</td><td>0.9996</td><td>0.9997</td><td>0.9997</td><td>0.9996</td><td>0.9997</td><td>0.9988</td><td>0.9984</td><td>0.9986</td></tr><tr><td>RIDAM (ours)</td><td>1.0000</td><td>1.0000</td><td>1.0000</td><td>0.9999</td><td>0.9999</td><td>0.9999</td><td>0.9993</td><td>0.9995</td><td>0.9994</td></tr></table>

## IV. METHOD

## A. Network Architecture

Recently transformer-based architectures achieve state-ofthe-art results in computer vision tasks [11]. However, as layers required for such architectures have not been widely implemented by DSP manufacturers, we build our method using a CNN-based architecture. Liu et al. [12] study why transformerbased architectures are dominant in computer vision tasks and propose a novel CNN-based architecture (convnexts), which achieve competitive results compared to transformer-based architectures.

Our method radar interference detection and mitigation (RIDAM) follows an autoencoder design, where the encoder is based on the convnext architecture. Furthermore, for interference detection and interference mitigation, two separate heads are implemented based on transposed convolution [13] and depthwise separable convolution [14]. We concatenate encoded features with the decoded feature in a given head. The full architecture is visualized in Fig. 2.

The input to our method is the interference-contaminated radar frame, which has the shape [BS, 2, F, S], where BS is the number of radar frames to mitigate, the two channels are the real and imaginary part of the complex radar frame, F is the number of fast-time samples (192), and S is the number of slow-time samples (64). Using the encoder, the input is encoded into the latent feature space, which is then further processed by the individual heads. The interference detection head computes a binary mask of the positions of interference occurrences of shape [BS, F, S], in which interferencecontaminated and interference-free samples have the value 1 and 0, respectively. The mask is computed by applying the softmax and then the argmax function to the detection head output. Similar, the interference mitigation head uses the latent feature space as input and computes an interference-free representation of the radar frame.

Depending on the situation, most of the radar frame is not disturbed by radar interference. Therefore, we only use mitigated samples if a sample was disturbed by interference and use the interference-free samples otherwise. This is achieved by computing the reconstructed radar frame as

$$
R F _ { R } = R F _ { I } * M + R F _ { I } * ( 1 - M ) ,
$$

where $R F _ { R }$ is the reconstructed radar frame, $R F _ { I }$ is the interference-contaminated input, $R F _ { M }$ is the mitigated radar frame, and M is the binary mask of interference-contaminated detections.

## B. Training

We train our method over 150 epochs on four GPUs using a distributed data parallel (DDP) strategy, a total batch size of 128, the AdamW optimizer [15], and cosine annealing with warm restarts [16] using an initial learning rate of $4 * 1 0 ^ { - 3 }$ and a final learning rate of $4 * 1 0 ^ { - 4 }$ . During training, radar interference is simulated online using the parameters in Table II. For the interference detection head, we use the cross entropy loss and for the interference mitigation head we use the mean squared error loss. We sum both losses and optimize accordingly.

## V. EXPERIMENT METRICS

## A. Interference Detection

To evaluate interference detection, we use classical object detection metrics, namely precision, recall, and F1-score. In combination with an accurate mitigation method a high recall will result in a better reconstructed RDS, as less noise is in the mitigated radar frame. Meanwhile, a high precision may be required for the mitigation method, as a low precision will hide essential information to correctly recover the radar frame.

## B. Interference Mitigation

Interference mitigation is classically evaluated using the signal-to-interference-and-noise ratio (SINR), which is a comparison of the signal power between the targets and the noise floor. The SINR in RDS domain is defined as

$$
\mathit { S I N R } = 1 0 l o g \frac { \frac { 1 } { | T _ { C } | } \sum _ { ( n , m ) \in T _ { C } } | R D S [ m , n ] | ^ { 2 } } { \frac { 1 } { | N _ { C } | } \sum _ { ( n , m ) \in N _ { C } } | R D S [ m , n ] | ^ { 2 } } ,
$$

where $T _ { c }$ is the set of target cells and $N _ { c }$ is the set of noise cells based on the clean RDS.

TABLE IV: Results of the interference mitigation experiment. Methods indicated by $^ { * } , + ,$ and - use the exact, VARIATION, and RIDAM interference detection mask, respectively. If nothing is mentioned the method uses its own method or does not require interference detection. The best performing method in a given metric is marked bold. We write metrics using the exact mask in italic and don’t consider them as best performing as they are a theoretical upper bound.
<table><tr><td rowspan="2"></td><td colspan="5">Weak</td><td colspan="5">Medium</td><td colspan="5">Strong</td></tr><tr><td>SINR</td><td>EVM</td><td>P</td><td>R</td><td>F1</td><td>SINR</td><td>EVM</td><td>P</td><td>R</td><td>F1</td><td>SINR</td><td>EVM</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>Interference-free</td><td>39.62</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td><td>39.62</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td><td>39.62</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>Interference-contaminated</td><td>36.53</td><td>0.206</td><td>0.268</td><td>0.721</td><td>0.391</td><td>29.85</td><td>0.580</td><td>0.283</td><td>0.590</td><td>0.383</td><td>22.77</td><td>1.216</td><td>0.236</td><td>0.379</td><td>0.291</td></tr><tr><td colspan="10">CLASSICAL METHODS</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>ZEROING* [6]</td><td>38.29</td><td>0.430</td><td>0.540</td><td>0.913</td><td>0.679</td><td>32.88</td><td>0.535</td><td>0.465</td><td>0.722</td><td>0.566</td><td>26.77</td><td>0.986</td><td>0.344</td><td>0.496</td><td>0.407</td></tr><tr><td>ZEROING+ [6]</td><td>36.82</td><td>0.305</td><td>0.575</td><td>0.732</td><td>0.644</td><td>30.57</td><td>0.619</td><td>0.523</td><td>0.553</td><td>0.537</td><td>23.81</td><td>1.100</td><td>0.501</td><td>0.375</td><td>0.429</td></tr><tr><td>AR* [7]</td><td>39.54</td><td>0.125</td><td>0.793</td><td>0.950</td><td>0.864</td><td>37.59</td><td>0.235</td><td>0.668</td><td>0.857</td><td>0.751</td><td>33.93</td><td>0.547</td><td>0.536</td><td>0.701</td><td>0.608</td></tr><tr><td>AR [7]</td><td>37.81</td><td>0.193</td><td>0.576</td><td>0.778</td><td>0.662</td><td>31.94</td><td>0.524</td><td>0.585</td><td>0.605</td><td>0.595</td><td>24.97</td><td>1.025</td><td>0.551</td><td>0.390</td><td>0.457</td></tr><tr><td>AR- [7]</td><td>39.54</td><td>0.125</td><td>0.793</td><td>0.950</td><td>0.865</td><td>37.57</td><td>0.235</td><td>0.669</td><td>0.856</td><td>0.751</td><td>33.89</td><td>0.549</td><td>0.538</td><td>0.699</td><td>0.608</td></tr><tr><td colspan="10">DEEP-LEARNING BASED</td><td colspan="7"></td></tr><tr><td>CNN-RD [9]</td><td>16.69</td><td>0.980</td><td>0.551</td><td>0.297</td><td>0.386</td><td>15.98</td><td>0.981</td><td>0.557</td><td>0.288</td><td>0.379</td><td>14.91</td><td>0.981</td><td>0.557</td><td>0.273</td><td>0.367</td></tr><tr><td>CNN-TD* [8]</td><td>39.75</td><td>0.046</td><td>0.965</td><td>0.974</td><td>0.970</td><td>39.86</td><td>0.098</td><td>0.891</td><td>0.925</td><td>0.908</td><td>40.03</td><td>0.227</td><td>0.796</td><td>0.836</td><td>0.815</td></tr><tr><td>CNN-TD [8]</td><td>37.93</td><td>0.161</td><td>0.577</td><td>0.785</td><td>0.665</td><td>32.58</td><td>0.417</td><td>0.585</td><td>0.617</td><td>0.600</td><td>26.07</td><td>0.837</td><td>0.583</td><td>0.422</td><td>0.490</td></tr><tr><td>CNN-TD− [8]</td><td>39.75</td><td>0.046</td><td>0.965</td><td>0.974</td><td>0.969</td><td>39.85</td><td>0.099</td><td>0.892</td><td>0.924</td><td>0.907</td><td>39.99</td><td>0.228</td><td>0.801</td><td>0.831</td><td>0.816</td></tr><tr><td>AE-GATE* [5]</td><td>39.63</td><td>0.032</td><td>0.977</td><td>0.978</td><td>0.977</td><td>39.79</td><td>0.078</td><td>0.954</td><td>0.933</td><td>0.943</td><td>40.08</td><td>0.179</td><td>0.911</td><td>0.850</td><td>0.879</td></tr><tr><td>AE-GATE [5]</td><td>39.58</td><td>0.038</td><td>0.976</td><td>0.971</td><td>0.973</td><td>39.63</td><td>0.086</td><td>0.958</td><td>0.917</td><td>0.937</td><td>39.59</td><td>0.199</td><td>0.929</td><td>0.803</td><td>0.861</td></tr><tr><td>RIDAM* (ours)</td><td>39.62</td><td>0.030</td><td>0.980</td><td>0.979</td><td>0.979</td><td>39.72</td><td>0.076</td><td>0.955</td><td>0.932</td><td>0.943</td><td>39.82</td><td>0.181</td><td>0.903</td><td>0.838</td><td>0.870</td></tr><tr><td>RIDAM (ours)</td><td>39.62</td><td>0.030</td><td>0.980</td><td>0.979</td><td>0.979</td><td>39.72</td><td>0.076</td><td>0.956</td><td>0.931</td><td>0.943</td><td>39.79</td><td>0.182</td><td>0.906</td><td>0.835</td><td>0.869</td></tr></table>

Additionally, we evaluate the error vector magnitude (EVM) [9] which is defined in RDS domain as

$$
E V M = \frac { 1 } { | T _ { C } | } \sum _ { ( n , m ) \in T _ { C } } \frac { | R D S _ { C } [ n , m ] - R D S _ { M } [ n , m ] | } { | R D S _ { C } [ n , m ] | } ,
$$

where $R D S _ { C }$ and $R D S _ { M }$ are the interference-free and mitigated RDS. The EVM evaluates how similar the recovered amplitude and phase of targets in interference-free and mitigated RDS are.

The overall purpose of interference mitigation is to detect the same targets in the mitigated as in the interference-free RDS. Therefore, we evaluate interference mitigation methods in terms of object detection. We detect ground truth targets using the CA-CFAR algorithm in interference-free RDS and compare with the detected targets in the mitigated RDS. We use precision, recall and the F1-score as metrics.

## VI. EXPERIMENTS

We simulate three different test sets based on the validation set with randomly sampled interfering radar parameters from Table II. The different test sets contain primarily weak, medium, and strong interference, where 1, 1 to 2, and 3 to 4 radars interfere with the victim radar respectively.

TABLE V: Target detection metrics after interference mitigation using RIDAM on the interference-free validation set without simulated radar interference.
<table><tr><td></td><td>SINR</td><td>EVM</td><td>P</td><td>R</td><td>F1</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>clean</td><td>39.61844</td><td>0.00000</td><td>1.00000</td><td>1.00000</td><td>1.00000</td></tr><tr><td>RIDAM</td><td>39.61846</td><td>0.00002</td><td>1.00000</td><td>0.99996</td><td>0.99998</td></tr></table>

For the evaluation, we train other deep-learning based methods according to their publications. However, our dataset is substantially larger compared to other publications. Hence, we increased the number of epochs until convergence.

## A. Interference Detection

In terms of interference detection we evaluate our method (RIDAM) with different classical MSER [2], VARIATION [3], LAPLACIAN [4], and deep-learning based AE-GATED [5] radar interference detection methods on the three different test sets. Table III shows the evaluation results.

Classical methods worsen, from weak to the strong test set. Intuitively a stronger interference should be easier to detect, as the signal power of the interference may be higher compared to the signal power of reflecting targets. However, we reason that this drop in performance is caused due to the number of interfering radars. Multiple interfering radars cause non-trivial arrangements of interference-contaminated ADC samples and therefore significantly increase the difficultly of interference detection. For classical methods, the VARIATION has a slightly higher Recall than the MSER method, while the MSER has a slightly higher Precision. Whereas both methods outperform the LAPLACIAN detection method.

In comparison, deep-learning based methods are able to correctly learn the distinction between interference-free and disturbed ADC samples. Our method has a slight improvement in metrics compared to AE-GATED. However, both methods outperform classical methods by a large margin and maintain consistent metrics over all test sets.

## B. Interference Mitigation

In the interference mitigation evaluation, we compare our method with the ZEROING [6], AR [7], CNN-RD [9], CNN-TD [8], and AE-GATE [5] interference mitigation methods on the weak, medium and strong radar interference test set. Table IV shows the results of our evaluation.

The ZEROING method weakly improves in all metrics. However, the relatively low F1-score in all test sets indicate that most of the target cells are not perceived correctly after mitigation. In comparison, the AR method reconstructs the gaps of disturbed ADC samples and performs significantly better an all test sets. Yet, the AR method also fails sufficiently mitigate interference in the strong interference test set. We reason that this is the case due to less interference-free ADC samples being available for the reconstruction of the gaps.

Deep-learning based methods perform significantly better than classical methods. Ranking purely deep-learning based methods, the CNN-TD method performs worst. However, the method still performs strongly in the weak and medium test set and outperforms classical methods when used with an accurate interference detection mask. The AE-GATE and our method perform almost on par in all metrics using the exact interference detection mask. However, our method slightly outperforms the AE-GATE method when both use their own interference detection. Unfortunately, we could not reproduce the results of the CNN-RD method. This might be caused by different parameters for detecting target cells within the RDS. In our experiments the CA-CFAR algorithm is tuned to also detect weak targets such as pedestrians and cyclists.

## C. Importance of Interference Detection for Mitigation

The exact interference detection mask specifies an upper bound for mitigation methods that recover the disturbed IF signal. Hence, we evaluate such methods using the exact and the mask proposed by a given mitigation method. Our evaluation reveals that the mask strongly impacts the result of interference mitigation. This is shown in the results of the AR and CNN-TD method, where the achieved results differ heavily from the results using the exact mask. In consequence, we evaluate both methods using the interference detection of our method and show that the mitigation methods regain almost optimal results.

## D. Impact on Interference-free Radar Frames

Regardless of whether the IF signal is disturbed, our method is applied to each radar frame. Therefore, we evaluate our method on the validation set without any simulated interference. Table V shows the result of this evaluation. The SINR and EVM show that our method maintains target properties. Furthermore, the F1-score is close to 1.0 indicating that almost all targets are detected. Hence, we reason that our method is safe to apply on radar frames even without radar interference.

## VII. CONCLUSION

We propose RIDAM, a deep-learning based method for radar interference detection and mitigation. It is based on the idea to use an end-to-end trained deep autoencoder to represent the radar frames in a latent space which can be effectively used by separate network heads to detect and mitigate radar interference. We show that our method achieves state-ofthe-art metrics in both tasks. Furthermore, we reveal that our method can be applied to interference-free radar frames without loosing target properties or target detections. The next steps of research are to transfer our simulation results to the digital signal processor of a real radar and to evaluate its performance under normal working conditions.

## ACKNOWLEDGMENT

We thank the Karlsruhe School of Optics and Photonics (KSOP) for support.

## REFERENCES

[1] M. Kunert, “Project final report, MOSARIM: More safety for all by radar interference mitigation.” Tech. Rep. 248231, 2012. [Online]. Available: https://cordis.europa.eu/docs/projects/cnect/ 1/248231/080/deliverables/001-D611finalreportfinal.pdf

[2] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), 2015, pp. 1–4.

[3] Y. W. Natsume, “Interference determination method and FMCW radar using the same,” U.S. Patent 7 187 321, Mar. 6 2007. [Online]. Available: https://patents.google.com/patent/US7187321

[4] S. Chen, J. Taghia, T. Fei, U. Kuhnau, N. Pohl, and R. Martin, “A DNN¨ autoencoder for automotive radar interference mitigation,” in ICASSP 2021 - 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2021, pp. 4065–4069.

[5] S. Chen, J. Taghia, U. Kuhnau, N. Pohl, and R. Martin, “A two-¨ stage DNN model with mask-gated convolution for automotive radar interference detection and mitigation,” IEEE Sensors Journal, vol. 22, no. 12, pp. 12 017–12 027, 2022.

[6] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[7] M. Rameez, M. Dahl, and M. I. Pettersson, “Autoregressive model-based signal reconstruction for automotive radar interference mitigation,” IEEE Sensors Journal, vol. 21, no. 5, pp. 6575–6586, 2021.

[8] M. Rameez, “Signal processing approaches for interference mitigation in automotive radar systems,” Ph.D. dissertation, , Department of Mathematics and Natural Sciences, 2023.

[9] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks,” in 2019 22th International Conference on Information Fusion (FUSION), 2019, pp. 1–8.

[10] T.-Y. Lim, S. A. Markowitz, and M. N. Do, “Radical: A synchronized FMCW radar, depth, IMU and RGB camera data dataset with lowlevel FMCW radar signals,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 941–953, 2021.

[11] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, J. Uszkoreit, and N. Houlsby, “An image is worth 16x16 words: Transformers for image recognition at scale,” CoRR, vol. abs/2010.11929, 2020. [Online]. Available: https://arxiv.org/abs/2010.11929

[12] Z. Liu, H. Mao, C.-Y. Wu, C. Feichtenhofer, T. Darrell, and S. Xie, “A convnet for the 2020s,” in 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022, pp. 11 966–11 976.

[13] V. Dumoulin and F. Visin, “A guide to convolution arithmetic for deep learning,” 2018.

[14] L. Sifre and S. Mallat, “Rigid-motion scattering for texture classification,” CoRR, vol. abs/1403.1687, 2014. [Online]. Available: http://arxiv.org/abs/1403.1687

[15] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” in International Conference on Learning Representations, 2019. [Online]. Available: https://openreview.net/forum?id=Bkg6RiCqY7

[16] ——, “SGDR: Stochastic gradient descent with warm restarts,” in International Conference on Learning Representations, 2017. [Online]. Available: https://openreview.net/forum?id=Skq89Scxx