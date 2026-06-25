# Fully Convolutional Neural Networks for Automotive Radar Interference Mitigation

Nicolae-Cat˘ alin Ristea ˘

University Politehnica of Bucharest

Bucharest, Romania

r.catalin196@yahoo.ro

Andrei Anghel University Politehnica of Bucharest Bucharest, Romania andrei.anghel@munde.pub.ro

Radu Tudor Ionescu   
University of Bucharest   
Bucharest, Romania   
raducu.ionescu@gmail.com

Abstract—The interest of the automotive industry has progressively focused on subjects related to driver assistance systems as well as autonomous cars. Cars combine a variety of sensors to perceive their surroundings robustly. Among them, radar sensors are indispensable because of their independence of lighting conditions and the possibility to directly measure velocity. However, radar interference is an issue that becomes prevalent with the increasing amount of radar systems in automotive scenarios. In this paper, we address this issue for frequency modulated continuous wave (FMCW) radars with fully convolutional neural networks (FCNs), a state-of-the-art deep learning technique. We propose two FCNs that take spectrograms of the beat signals as input, and provide the corresponding clean range profiles as output. We propose two architectures for interference mitigation which outperform the classical zeroing technique. Moreover, considering the lack of databases for this task, we release as open source a large scale data set that closely replicates real world automotive scenarios for single-interference cases, allowing others to objectively compare their future work in this domain. The data set is available for download at: http://github.com/ristea/arim.

Index Terms—autonomous driving, automotive radar, interference mitigation, denoising, convolutional neural networks.

## I. INTRODUCTION

Nowadays, automotive radar sensors are essential elements of driving assistance systems and autonomous driving applications. Their main goal is to estimate the distance and velocity of objects on the road. However, the technical requirements increased steadily from simple detection to braking functions and smart environment perception tasks [1] for self-driving cars. The most common radar senors used in the automotive industry are frequency modulated continuous wave (FMCW) / chirp sequence (CS) radars, which transmit sequences of linear chirp signals. Furthermore, the amount of automotive radar systems on the streets is regularly increasing [2], and the high number of automotive radar systems on roads leads to a higher probability of interference between radar sensors.

Radio frequency interference (RFI) is a relevant issue for radar sensors as it could increase the effective noise floor, reduce sensitivity or create false detections [3]. We illustrate the negative effects of RFI in Figure 1, where the noise floor has risen with approximately 15 dB and the targets become almost undetectable. Therefore, the interference mitigation task is a crucial part of current and future radar sensors used in a traffic safety context.

![](images/9826901d4fa88e4c237b65f11a01e8a0b0c5160f9f9a1b3ef7bd806d4b8129c5.jpg)  
Fig. 1: Range profile magnitude of an FMCW radar sensor. The useful profile is shown in blue, while the profile with interference is shown in red.

In this paper, we propose a novel approach for radar interference mitigation that is based on fully convolutional neural networks (FCNs) [4]. This architecture is able to learn different types of patterns with a relatively small amount of learnable parameters, a fact that recommends them for realtime applications, such as autonomous driving. Our proposed architecture is fed with spectrograms of beat signals with noise and interference. The output of our neural network is the range profile magnitude with mitigated noise and interference. Additionally, because of the lack of public databases, we propose a novel synthetic database, with signals affected by an interference source, for the community to have a common ground for the evaluation and comparison of future methods.

In summary, our contribution is twofold:

• We propose a novel approach for interference mitigation based on FCNs, transforming spectrograms into range profiles.

• We propose a radar interference data set with a wide and realistic range of signal parameter variations to be used as benchmark in future research.

## II. RELATED WORK

Classical methods. State-of-the-art interference detection (mitigation) methods are typically classified according to the domain in which the interference is mitigated [5]–[10]:

polarization, time, frequency, code and space. Polarizationbased methods assume the use of cross-polarized antennas between the two interfering radars and the mitigation margin is around 20 dB, but reflections on the ground or other surrounding targets can severely reduce this margin. Time domain methods include the following approaches: use of a low transmit duty cycle (to reduce the probability of hitting other receivers), use of a short receive window (to reduce the probability of being hit by an interferer), or employing a variable pause between chirps or a variable chirp slope (to avoid periodic interferences). Frequency domain methods imply a division of the authorized operating bandwidth into several sub-bands, such that nearby radars operate in different sub-bands. RFI mitigation in the coding domain involves the modulation of the radar waveforms with a device-specific code (to minimize cross-talk between radars, the codes of different devices should be orthogonal), whereas in the case of space domain techniques, the antenna radiation pattern is adaptively configured to avoid interfering signals.

A particular class of methods are the strategic RFI mitigation techniques [5], which involve additional hardware and/or software, yet rely on some of the basic techniques. The classical strategic approaches are: “communicate and avoid” (requires inter-vehicle communication to avoid simultaneous transmission), “detect and avoid” (e.g., detects the interference in a sub-band and changes the operating sub-band of the radar), “detect and repair” (after detection, the measurement with interference is reconstructed), “detect and omit” (after detection, the measurements affected by interference are removed) and “listen before talk” (the radar transmits only when no other device is detected).

Different from all these methods, which rely on algorithms handcrafted by researchers, we propose an approach based on end-to-end learning from data. In order to obtain our approach, we constructed a realistic data set to learn deep neural networks.

Deep learning methods. Deep learning techniques have been applied in a wide range of tasks with remarkable results [11], [12]. One such task is image denoising, where deep learning achieved state-of-the-art results [13], outperforming classical approaches such as median or bilateral filtering. By transforming the radio signal into a spectrogram, the task of interference mitigation becomes similar to a task of image denoising. In this context, we propose to apply fully convolutional networks, a deep learning technique, to transform a noisy spectrogram into a clean range profile of a radar sensor. To our knowledge, there are only a handful of related works [14]–[16] that employ deep learning models for radar interference mitigation, but they have different architectures that are based on input and output pairs from the same domain, e.g. both their input and output are spectrograms [14]. In [14], the authors proposed a convolutional neural network (CNN) to address RFI, aiming to reduce the noise floor while preserving the signal components of detected targets. The CNN architecture can be trained using either range processed data or range-Doppler (RD) spectra as inputs. The authors reported promising results, but they still have concerns regarding the generalization capacity on real data. Another approach that relies on CNNs is proposed in [17]. The authors employ an autoencoder based on the U-Net architecture [18], which performs interference mitigation as a denoising task directly on the range-Doppler spectrum. They surpass classical approaches, but the phase information cannot be fully preserved. Similarly, in [15], the network architecture is build upon CNNs, but residual connections, inspired from [19], were added. A different method is proposed in [16], which is based on applying a recurrent neural network model with Gated Recurrent Units [20] on the time domain signal to mitigate the interference. The authors reported better performance compared to existing signal processing methods and lower processing times.

## III. METHOD

Radar signal model. In FMCW radar solutions, the transmitted signal $s _ { T X } ( t )$ is a chirp sequence, whose frequency usually follows a sawtooth pattern. The analytical signal $s _ { T X } ( t )$ in a sweep interval is defined as follows:

$$
s _ { T X } ( t ) = \left\{ \begin{array} { l l } { e ^ { j 2 \pi ( f _ { 0 } t + \frac { \alpha t ^ { 2 } } { 2 } ) } , } & { \mathrm { i f } 0 \leq t \leq T _ { c } } \\ { 0 , } & { \mathrm { o t h e r w i s e } } \end{array} \right. ,\tag{1}
$$

where t is the time domain variable, $f _ { 0 }$ is the frequency at the initial moment $t = 0 , T _ { c }$ is the frequency variation time interval (sweep time) and α is called the chirp rate calculated as $\begin{array} { r } { \alpha = \frac { B } { T _ { c } } } \end{array}$ , where B is the bandwidth.

The receive antenna collects the reflected signal $s _ { R X } ( t )$ which, for a single target, is defined as follows:

$$
s _ { R X } ( t ) = \underline { { A } } \cdot s _ { T X } ( t - \tau ) ,\tag{2}
$$

where τ is the propagation delay and $\underline { { { A } } } \ : = \ : A \cdot e ^ { j \phi }$ is the complex amplitude of the received signal.

The reflected signal is further mixed with the transmitted signal and low-pass filtered, resulting in the beat signal $s _ { b } ( t )$ which is analytically computed as:

$$
s _ { b } ( t ) = s _ { T X } ( t ) \cdot s _ { R X } ^ { * } ( t ) ,\tag{3}
$$

where $s _ { R X } ^ { * } ( t )$ represents the complex conjugate of $s _ { R X } ( t )$ Interference signal model. In the presence of mutual interference, the radar transmits a signal which is reflected by a target and the receiving antenna collects a mix from two signals, the reflected signal and the interference signal, respectively. Consequently, the received signal is defined as follows:

$$
s _ { R X } ( t ) = \sum _ { j = 0 } ^ { N _ { t } } \underline { { { A } } } _ { j } \cdot s _ { T X } ( t - \tau _ { j } ) + \sum _ { k = 0 } ^ { N _ { i n t } } s _ { R F I , k } ( t ) ,\tag{4}
$$

where $N _ { t }$ is the number of targets, $N _ { i n t }$ is the number of interferers and $\underline { { A } } , \tau$ are the corresponding parameters from Equation (2). An uncorrelated interfering signal $s _ { R F I , k } ( t )$ (with a different modulation rate than the one of the transmitted chirp) translates, after mixing with the transmitted signal, into a chirp signal whose bandwidth is limited by the anti-aliasing filter. Therefore, an uncorrelated interference appears as a highly non-stationary component on the spectrogram, which is spread across multiple frequency bins. In the following, we limit the number of interferers to $N _ { i n t } = 1$ and we consider only uncorrelated interfering sources.

![](images/7dd948e1ea4019b7bc97e55447e4a9435a1548d5db3315e918d48cfa0dc2535f.jpg)  
Fig. 2: The general architecture of our FCN models. The input spectrogram is processed through a series of conv blocks (composed of conv and pooling layers) until the vertical dimension is reduced to 1, while preserving the horizontal dimension. The output is a range profile without the interference removed by the FCN.

Data preprocessing. Fully convolutional neural networks attain state-of-the-art results in computer vision, the convolutional operation being specifically designed for images. In order to apply FCNs to our task, we first need to transform the time domain signals into images. One of the most common approaches to obtain an image representation of a time domain signal is by computing a spectrogram using the discrete Short-Time Fourier Transform (STFT), as shown in the following equation:

$$
S T F T \{ x [ n ] \} ( m , k ) = \sum _ { n = - \infty } ^ { \infty } x [ n ] \cdot w [ n - m R ] e ^ { - j { \frac { 2 \pi } { N _ { x } } } k n } ,\tag{5}
$$

where x[n] is the discrete input signal, w[n] is a window function, $N _ { x }$ is STFT length and R is the hop/step size [21]. There are a plethora of window functions proposed in literature, such as hann, blackman and others. We chose to perform the STFT with hamming window.

Moreover, several time-frequency representations have been developed over time. Wavelet analysis, through the continuous wavelet transform with different base functions, can also be used for this purpose. Nevertheless, in this study, we restrict ourselves to the spectrogram, and leave other time-frequency representations for future investigations.

Our goal is to obtain clean range profiles from beat signal spectrograms affected by noise and uncorrelated interference. We design our FCNs to provide the clean range profiles as output (during training, the FCNs have to learn to reproduce the ground-truth clean range profiles). For this reason, we perform a Fast Fourier Transform (FFT) of our time domain labels (to obtain the ground-truth clean range profiles) and train our networks to map the STFT input to the FFT output. The FFT is computed as follows:

$$
\mathrm { F F T } \{ x [ n ] \} ( k ) = \sum _ { n = 0 } ^ { N _ { x } - 1 } x [ n ] \cdot e ^ { - j \frac { 2 \pi } { N _ { x } } k n } ,\tag{6}
$$

where $N _ { x }$ is the number of FFT points (same value as the number of STFT range bins).

Network architectures. We consider a beat signal with 1024 samples, and we design two FCN models for interference mitigation from single-channel spectrograms. The first FCN takes as input a spectrogram of 154×2048 components, while the second FCN takes as input a spectrogram of 1024 × 2048 components. The horizontal axis dimension (2048) corresponds to the number of FFT points in the range profile, while the vertical axis dimension (154 or 1024) is influenced by the computing step size of STFT. The dimensions of 154 or 1024 correspond to steps R = 6 and R = 1, respectively. We design each FCN architecture to progressively reduce the dimension on the vertical axis to one component, while preserving the horizontal axis dimension. Therefore, both FCN models produce outputs of 1 × 2048 components that are interpreted as range profiles. In order to reach the same output size from different input sizes, the two FCN models have different depths. In Figure 2, we illustrate the generic architecture of both networks, which are exclusively composed of convolutional (conv) blocks.

To reduce the spectrogram of 154 × 2048 to a range profile of 1 × 2048 components, we propose a shallower FCN of 15 layers organized into 4 conv blocks. Each of the first 3 blocks are composed of 3 conv layers followed by a maxpooling layer, while the last block has 3 conv layers (without pooling). Each conv layer in the first block is formed of 8 filters. The number of conv filters doubles in each subsequent block. Based on this rule, the first two conv layers from the fourth block are formed of 64 filters. The last conv layer needs to squeeze the number of channels to one, hence it can have only one filter.

To reduce the spectrogram of 1024×2048 to a range profile of 1×2048 components, we propose a deeper FCN of 21 layers organized into 7 conv blocks. Each of the first 6 blocks are composed of 2 conv layers followed by a max-pooling layer, while the last block has 3 conv layers (without pooling). Each conv layer in the first block is formed of 8 filters. The number of conv filters doubles in each subsequent block, except for the second and the fourth blocks, which keep the number of filters from the previous blocks. As for the shallow FCN, the last conv layer has only one filter.

For both architectures, the conv filters with 5 × 5 spatial support are applied at stride 1. Zero padding is added to preserve the horizontal dimension of the activation maps. Except for the very last conv layer, all convolutional layers are followed by ReLU activations. The pooling filters are of size 2 × 1, reducing the size of the activation maps on the vertical axis only. Zero padding for the max-pooling layers is added only when we need to make sure that the input activation maps have an even size. Both networks are trained using the Adam optimizer [22], using the mean squared error as loss function.

TABLE I: Minimum and maximum values for each parameter in our joint uniform distribution used for generating the samples in our database.
<table><tr><td>Parameter</td><td>Minimum</td><td>Maximum</td><td>Step</td></tr><tr><td>SNR [dB]</td><td>5</td><td>40</td><td>5</td></tr><tr><td>SIR [dB]</td><td>-5</td><td>40</td><td>5</td></tr><tr><td>Relative interference signal slope</td><td>0</td><td>1.5</td><td>0.1</td></tr><tr><td>Number of targets</td><td>1</td><td>4</td><td>1</td></tr><tr><td>Target amplitude</td><td>0.01</td><td>1</td><td>=</td></tr><tr><td>Target distance [m]</td><td>2</td><td>95</td><td>=</td></tr><tr><td>Target phase [rad]</td><td>-π</td><td>π</td><td>=</td></tr></table>

TABLE II: Fixed parameters for simulating a realistic radar sensor.
<table><tr><td>Parameter</td><td>Description</td><td>Value</td></tr><tr><td>B</td><td>Bandwidth</td><td>1.6 GHz</td></tr><tr><td>Tr</td><td>Time of chirp</td><td>25.6 µs</td></tr><tr><td> $f _ { s }$ </td><td>Sampling frequency</td><td>40 MHz</td></tr><tr><td> $\overline { { f _ { 0 } } }$ </td><td>Radar central frequency</td><td>78 GHz</td></tr></table>

## IV. DATA SET

It is well known that a large database is a key factor in the training process of deep neural networks with high generalization capacity. To the best of our knowledge, there are no public in-the-wild (or generated) databases for the interference mitigation task, mainly because of the difficulty imposed by the process of data acquisition and data labeling. In this context, it is hard to compare novel approaches with the previous ones in an objective manner.

In this paper, we propose a novel large scale database consisting of 48,000 samples, generated automatically while trying to replicate a realistic automotive scenario with one interference source. We generate every sample using specific randomly selected values for the set of parameters listed in Table I. While the values corresponding to some parameters are selected using a fixed step between the minimum and the maximum values specified in Table I, the values corresponding to the other parameters are randomly selected using an uniform distribution between the minimum and the maximum values. More precisely, we use linear variation with a fixed step for the signal to noise ratio (SNR), the signal to interference ratio (SIR) and the interference slope parameters. The number of targets as well as the distance, the amplitude and the phase of each target are random variables that follow an uniform distribution. The amplitude of each target is proportional with the power expected from that particular target. We added a random phase to each target to obtain more realistic radar signals.

Concerning the simulated radar sensor, we considered a fixed set of parameters such as bandwidth, sweep time, sampling frequency and central frequency. The exact values used for these parameters are listed in Table II.

Since we can control all factors during sample generation, we can produce an exact copy of each signal without interference. First of all, the clean copy can be used as ground-truth label when training a machine learning model. Second of all, it provides the means to conduct an objective assessment of the performance, by comparing the output predicted by the model with the corresponding ground-truth (expected) output. Consequently, a data sample is composed of:

• a time domain signal without interference;

• a time domain signal with interference;

• a label vector with complex amplitude values in target locations.

We randomly split our data samples into a training set of 40,000 samples and a test set of 8,000 samples. This will allow future works to directly compare novel results with previous results, without having to re-implement preceding methods in order to reproduce the corresponding results. Our data set is freely available for download at: http://github.com/ristea/arim.

## V. EXPERIMENTS

Since the database consists of different radar signals (with and without interference) referring to different range profiles, in our experiments, the interference mitigation is performed individually on each range profile.

Evaluation metrics. Usually, the goal in radar signal processing is to maximize the detection performance. Thus, a rather intuitive measure is the area under the receiver operating characteristics curve (AUC), which describes the ability to disentangle targets from noise at various thresholds. The target detection threshold grows iteratively from the lowest value to the largest value in range profile, modifying the probability of false alarms. Another performance indicator is the mean absolute error (MAE) in decibels (dB) between the range profile amplitude of targets computed from label signals and the amplitude of targets from predicted signals. In our evaluation, we employed the AUC, the MAE and the mean SNR improvement (∆SNR), which is computed for the target with the highest amplitude in a signal as the difference between SNR after and before interference mitigation.

Baseline. A very common approach to eliminate the interference is to replace amplitudes higher than a specific threshold with zero (e.g. [5], [10]). This method is denoted as zeroing. Hyperparameter tuning. We tune the hyperparameters of our FCN models on a validation set. We kept 20% of the training set (8,000 samples) for validation. We used the same hyperparameters for both architectures, in order to minimize the chance of overfitting in hyperparameter space. We trained the models for 100 epochs with a mini-batch size of 10 samples. We set the learning rate to $1 0 ^ { - 5 }$ and we used a weight decay of $1 0 ^ { - 5 }$ . These parameters are obtained using grid search. In a similar fashion, we employed grid search on the validation set to find the threshold parameter for our baseline, the zeroing method.

Results. We compared our FCN models with a zeroing benchmark and an oracle based on the ground-truth labels. We present the corresponding results in Table III. We included the oracle in order to show the achievable upper bound score for each metric, e.g. the maximum AUC score on both validation

TABLE III: Validation and test results provided by our shallow and deep FCN models versus an oracle based on true labels and a baseline based on zeroing. A higher ∆SNR value is better, a higher AUC value is better and a lower MAE value is better. The best results (excluding the oracle) are highlighted in bold.

<table><tr><td></td><td colspan="3">Validation set</td><td colspan="3">Test set</td></tr><tr><td>Method</td><td>∆SNR</td><td>AUC</td><td>MAE (dB)</td><td>∆SNR</td><td>AUC</td><td>MAE (dB)</td></tr><tr><td>Oracle (true labels)</td><td>12.92</td><td>0.978</td><td>0</td><td>13.08</td><td>0.978</td><td>0</td></tr><tr><td>Zeroing</td><td>5.27</td><td>0.951</td><td>1.26</td><td>5.44</td><td>0.951</td><td>1.27</td></tr><tr><td>Shallow FCN</td><td>10.34</td><td>0.965</td><td>2.20</td><td>10.49</td><td>0.965</td><td>2.21</td></tr><tr><td>Deep FCN</td><td>12.90</td><td>0.972</td><td>1.21</td><td>13.06</td><td>0.972</td><td>1.22</td></tr></table>

![](images/a3e02812b6aabdceb077fa120c23e99601e6f348645d9d7b6d0e2bf4a28b6f33.jpg)  
Fig. 3: Results for radar interference mitigation with our best FCN model. For comparison, we also added the groundtruth signal, the signal with interference and the signal with mitigated interference by the zeroing method.

and test is 0.978. Comparing our shallow FCN model with the zeroing baseline, we observe that our network attains better mean SNR improvement and AUC scores, but it seems to underperform according to the MAE measure. Our deep FCN provides superior results for all three metrics, surpassing both the zeroing baseline and the shallow FCN. In terms of ∆SNR and AUC, our deep FCN seems to attain performance levels quite close to the oracle, e.g. the AUC of our deep FCN is 0.006 under the AUC of the oracle on the test set.

In addition to the results on our data set, we assessed the generalization capacity of our deep FCN on real data, by testing it on samples provided by the NXP company, which were captured with the NXP TEF810X 77 GHz radar transceiver, from real-world scenarios. In Figure 3, we show an example of interference mitigation performed by our model on a real radar signal, producing an output very similar to the reference signal.

## VI. CONCLUSION

In this paper, we introduced two fully convolutional networks for automotive radar interference mitigation and a large scale database of radar signals simulated in realistic settings. We compared our FCN models with the zeroing baseline in a comprehensive experiment, showing that our deeper FCN provides superior results. We also released our novel data set to allow objective comparison in future work. To our knowledge, we are the first to establish a benchmark data set for automotive radar interference mitigation. In future work, we aim to analyze the scenario with multiple interference sources.

## REFERENCES

[1] M. Shibao and A. Kajiwara, “Road Debris Detection Using 79GHz Radar,” in Proceedings of VTC2019-Fall, pp. 1–4, 2019.

[2] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in Proceedings of EuRAD, pp. 1–5, 2012.

[3] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[4] J. Long, E. Shelhamer, and T. Darrell, “Fully convolutional networks for semantic segmentation,” in Proceedings of CVPR, pp. 3431–3440, 2015.

[5] M. Kunert, F. Bodereau, M. Goppelt, C. Fischer, A. John, T. Wixforth, A. Ossowska, T. Schipper, and R. Pietsch, “D1.5 - Study on the state-ofthe-art interference mitigation technique, MOre Safety for All by Radar Interference Mitigation (MOSARIM) project,” tech. rep., Robert Bosch GmbH, 2010.

[6] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[7] G. Kim, J. Mun, and J. Lee, “A Peer-to-Peer Interference Analysis for Automotive Chirp Sequence Radars,” IEEE Transactions on Vehicular Technology, vol. 67, pp. 8110–8117, Sep. 2018.

[8] Z. Xu and Q. Shi, “Interference Mitigation for Automotive Radar Using Orthogonal Noise Waveforms,” IEEE Geoscience and Remote Sensing Letters, vol. 15, pp. 137–141, Jan 2018.

[9] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a dbf mimo radar,” IEEE Transactions on Microwave Theory and Techniques, vol. 65, pp. 1727–1734, May 2017.

[10] F. Laghezza, F. Jansen, and J. Overdevest, “Enhanced Interference Detection Method in Automotive FMCW Radar Systems,” in Proceedings of IRS, pp. 1–7, 2019.

[11] P. Soviany and R. T. Ionescu, “Optimizing the trade-off between single-stage and two-stage deep object detectors using image difficulty prediction,” in Proceedings of SYNASC, pp. 209–214, 2018.

[12] M.-I. Georgescu, R. T. Ionescu, and N. Verga, “Convolutional Neural Networks with Intermediate Loss for 3D Super-Resolution of CT and MRI Scans,” IEEE Access, vol. 8, no. 1, pp. 49112–49124, 2020.

[13] P. A. Bricman and R. T. Ionescu, “CocoNet: A deep neural network for mapping pixel coordinates to color values,” in Proceedings of ICONIP, pp. 64–76, 2018.

[14] J. Rock, M. Toth, E. Messner, P. Meissner, and F. Pernkopf, “Complex Signal Denoising and Interference Mitigation for Automotive Radar Using Convolutional Neural Networks,” in Proceedings of FUSION, 2019.

[15] W. Fan, F. Zhou, M. Tao, X. Bai, P. Rong, S. Yang, and T. Tian, “Interference Mitigation for Synthetic Aperture Radar Based on Deep Residual Network,” Remote Sensing, vol. 11, no. 14, p. 1654, 2019.

[16] J. Mun, H. Kim, and J. Lee, “A Deep Learning Approach for Automotive Radar Interference Mitigation,” in Proceedings of VTC-Fall, pp. 1–5, 2018.

[17] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ Radar Interference Mitigation using a Convolutional Autoencoder,” in Proceedings of RADAR, 04 2020.

[18] O. Ronneberger, P. Fischer, and T. Brox, “U-Net: Convolutional Networks for Biomedical Image Segmentation,” in Proceedings of MICCAI, pp. 234–241, Springer, 2015.

[19] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of CVPR, pp. 770–778, 2016.

[20] J. Chung, C. Gulcehre, K. Cho, and Y. Bengio, “Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling,” in Proceedings of DLRL Workshop, 2014.

[21] J. B. Allen and L. R. Rabiner, “A unified approach to short-time Fourier analysis and synthesis,” Proceedings of the IEEE, vol. 65, pp. 1558– 1564, Nov 1977.

[22] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in Proceedings of ICLR, 2015.