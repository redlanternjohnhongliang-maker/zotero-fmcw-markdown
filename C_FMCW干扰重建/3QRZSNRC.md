# Automotive Radar Interference Mitigation Based on a Generative Adversarial Network

Shengyi Chen1,2, Wangyi Shangguan1, Jalal Taghia1, Uwe Kühnau¹, and Rainer Martin2

1HELLA GmbH & Co. KGaA, Lippstadt, Germany

2Ruhr-Universität Bochum, Bochum, Germany

{shengyi.chen, wangyi.shangguan, jalal.taghia, uwe.kuehnau}@hella.com, rainer.martin@rub.de

Abstract— This paper introduces a novel automotive radar interference mitigation approach using a generative adversarial network (GAN). Instead of tackling the mutual interference in the time domain, a generative adversarial network is trained and used to recover the complex signal in the frequency domain, namely on the complex range profile obtained after the fast Fourier transform of fast-time samples (RFFT spectrum). It is shown that by employing the gated convolution and an attention mechanism, the generator network has the ability to learn the amplitude and phase information for missing data from the remaining signal. Experimental results show that the proposed method can provide a remarkable improvement in signal-to-interference-plus-noise ratio (SINR) and preserves its robustness in severely disturbed scenarios that are much more complex than the training dataset.

Keywords —automotive radar, interference mitigation, generative adversarial network.

## I. INTRODUCTION

Automotive radar sensors are becoming indispensable in modern vehicles as they can provide robust safety support under almost all weather conditions. Since the number of vehicles equipped with radar sensors is increasing rapidly, the probability of mutual interference increases. The performance of radars can be affected by the mutual interference as the interference reduces the signal-to-noise ratio [1].

Various techniques have been proposed to address the problem of mutual interference [2]. Recent research results have shown that deep learning approaches can be used to solve this problem [3], [4]. In [3], a Recurrent Neural Network (RNN) model with Gated Recurrent Units (GRUs) is trained and applied to suppress the interference-contaminated signal in the time domain. In [4], Convolutional Neural Networks (CNNs) are employed for noise suppression of range profiles after the first fast Fourier transform (RFFT) and the range-Doppler (RD) spectrum (i.e. after applying the second fast Fourier transform to the range profile). However, the performance of the CNNs used in [4] may be less robust when it comes to preserving target peak values. Solving the mutual interference issue in the frequency domain for frequency-modulated continuous wave (FMCW) radar is also considered in [5], where the signal disturbed by interference is recovered by linear predictive coding (LPC) in the short-time Fourier transform (STFT) domain. However, the interference in real-world scenarios can contain more diversity and randomness, $\mathrm { e . g . }$ , the chirp rate of different radar sensors can be similar to each other, and there can be multiple sources of interference. Hence, the samples disturbed by interference in some chirps may spread across the entire measurement. Thus, the number of available interference-free samples in these chirps is not sufficient for LPC to provide adequate recovery in the STFT domain. In order to address these interference scenarios, where a random amount of chirps are completely disturbed, a generative adversarial network (GAN) is proposed in this paper to mitigate the mutual interference in FMCW/chirp sequence (CS) radars.

The remainder of this paper is organized as follows. In Section II, the FMCW radar signal model is introduced. Section III describes the details of the proposed GAN architecture. The performance evaluation is provided in Section IV, and conclusions are drawn in Section V.

## II. AUTOMOTIVE FMCW RADAR SIGNAL MODEL

In FMCW/CS radar systems the transmit chirp signal can be represented as

$$
x ( t ) = \exp \left( j 2 \pi \left( f _ { c } t + 0 . 5 \alpha t ^ { 2 } \right) \right) \mathrm { r e c t } _ { T } ( t ) ,\tag{1}
$$

where $f _ { c }$ is the carrier frequency, $\alpha = B / T$ denotes the chirp rate of the transmit signal with B and $T$ denoting the sweep bandwidth and chirp duration, respectively, and rectT(t) is the square pulse of duration T. The transmit waveform of an FMCW radar with M consecutive chirps is thus given by

$$
S _ { t x } ( t ) = \sum _ { m = 0 } ^ { M - 1 } x \left( t - m T \right) .\tag{2}
$$

The mth chirp of the target's echo signal is delayed by $\tau$ from the transmit signal with a normalized relative Doppler shift $d \colon$

$$
r _ { m } ( t ) = A _ { m } x ( t + ( t + m T ) d - \tau ) + \mathrm { v } _ { m } ( t ) ,\tag{3}
$$

where $A _ { m }$ is the received amplitude, $\tau = 2 R / c$ and $d =$ $2 v / c .$ The variables R and v denote, respectively, the distance and relative radial velocity between the radar and target, c is the speed of light, and v denotes the complex Gaussian noise. The beat signal at the intermediate frequency can be estimated by mixing $r _ { m }$ with the complex conjugate of the transmitted signal: ${ \hat { y } } _ { m } ( t ) = r _ { m } ( t ) x ^ { * } ( t )$ . After filtering with a low-pass filter (LPF) and sampling with a period of $T _ { s }$ and N samples per chirp, the analogue-to-digital converter $( \mathrm { A D C } )$ samples of the discrete beat signal can be approximated as

$$
\begin{array} { l } { { \hat { y } _ { m , n } \approx A _ { m } \underbrace { \exp \left( j 2 \pi \left( - \alpha \tau + f _ { c } d \right) n T _ { s } \right) } _ { r a n g e } . } } \\ { { \underbrace { \mathrm {  ~ \cdot ~ } \exp \left( j 2 \pi \left( { f _ { c } } d m T \right) \right) } _ { D o p p l e r } . } } \end{array}\tag{4}
$$

After applying the first fast Fourier transform along fast-time samples in (4), we obtain the RFFT spectrum, in which the data at the same position in each chirp has a similar amplitude but a different phase. The measured phase difference between two consecutive chirps is $\triangle \phi \approx$ $2 \pi f _ { c } d ,$ which corresponds to a motion of the object of vT. The velocity of corresponding targets can be obtained after applying the second fast Fourier transform in the chirp direction. In this paper, we focus on the interference reduction in the RFFT spectrum by utilizing the property of the phase difference measured across the consecutive chirps.

With the assumption that the interfering signal has the same center frequency, the transmit waveform of an interferer radar is $\begin{array} { r } { S _ { \mathrm { { i n t } } } ( t ) ~ = ~ \sum _ { m = 0 } ^ { M - 1 } x _ { \mathrm { { i n t } } } \left( t - m { \tilde { T } } \right) \bigg ) } \end{array}$ , where $x _ { \mathrm { m } } ( t ) ~ = ~ A _ { \mathrm { m } } \mathrm { e x p } \left( j 2 \pi \left( f _ { c } l + 0 . 5 \tilde { \alpha } t ^ { 2 } \right) \right) \mathrm { r e c t } _ { \tilde { T } } ( t )$ with $\begin{array} { r l } { \tilde { c } \tilde { \alpha } } & { { } = } \end{array}$ $\boldsymbol { \tilde { B } } / \boldsymbol { \tilde { T } } , \ \boldsymbol { \tilde { B } }$ and $\tilde { T }$ denote the chirp slope, sweep bandwidth and chirp duration of the interfering radar, respectively. The interference duration can be described as $T _ { \mathrm { m t } } \overset { \cdot } { \leq } | 2 \cdot B _ { r x } | ( \hat { \alpha } -$ $\left( \mathcal { X } \right) \big |$ , where $\boldsymbol { R } _ { r x }$ denotes the bandwidth of ${ \mathrm { I . P F } } \ { \mathrm { [ } } 6 { \mathrm { ] } } .$ If α is similar to α, there are more interference-contaminated samples within the recciver bandwidth and thus the number of available interference-free samples drops significantly. This causes a broadband distortion in the RFFT spectrum. The interference-contaminated chirps in the RFFT spectrum can be detected by a classical edge detector, e.g., Laplacian filter Figure 1 shows an example of using the Laplacian filter to determine the position of the distorted chirps in a real radar measurement. In this paper, we assume that due to the different chirp duration and the limited collision time between interferer and victim radar, the chirps in the RFFT spectrum are only partially disturbed.

![](images/e9b85029c08c7bc74c1b4f20b43f01c24a982f2db648c984a02b2db5d49a4dd8.jpg)  
(a)

![](images/b9bb62a4dd33ce5f4598d2427a0632096f9fca0861d6b916cdf2e1fc62d82d52.jpg)  
Fig. 1. (a) An example RFFT spectrum with interference; (b) Position of distorted chirps detected by Laplacian filter.  
(b)  
III. GENERATIVE ADVERSARIAL NETWORK

## A. Complex Signal as Network Input Data

Recently, Iizuka et al. [7] introduced a high performance generative network model with dilated convolutions for image completion, which can reconstruct arbitrary missing regions. Yu et al. extend the generative inpainting network with contextual attention and gated convolutions [8] and thus improve inpainting results with free-form masks. Inspired by previous image inpainting works, we use here a GAN to perform complex signal "inpainting" after removing the interference-contaminated chirps in the RFFT spectrum Instead of using three-channel RGB images, the complex signal obtained after the first FFT is converted into a tensor of the form [N, M, 2] as the input for the neural network, where the chirps disturbed by interference are set to zero with a mask. Since the position of interference-contaminated chirps can be random, a set of interference-free RFFT spectra in combination with random masks is used as input during training. To ensure that the generator network is able to deal with the randomness of the interference position, masks with 10 arbitrary positions are empirically chosen, each position covering 0.02M chirps. Each training dataset contains an arbitrary number of one to three targets with additive white Gaussian noise (AWGN). Table 1 shows the details of the target parameters. In order to improve the learning ability and the robustness of the model, the input data is normalized on its maximum.

<table><tr><td>Parameter</td><td>Unit</td><td>Lower limit</td><td>Upper limit</td></tr><tr><td>Number of Targets</td><td>1</td><td>1</td><td>3</td></tr><tr><td>Distance</td><td>m</td><td>0</td><td>120</td></tr><tr><td>Velocity</td><td>m/s</td><td>-31</td><td>31</td></tr></table>

Table 1. Parameter specification of the target in training dataset.

## B. Network Architecture for Radar Interference Mitigation

An overview of the GAN architecture is shown in Figure 2 which consists of three main components, namely the coarse generator network, the fine gencrator network and the discriminator network. The number of kernels of each layer is specified directly above the corresponding layers. The generator networks learn the signal features from the residual chirps and generate the signal for the missing regions, while the discriminator evaluates the recovery generated by the generator and delivers two types of losses. One is the generator loss that can be used for gencrator network training, the other is the discriminator loss that helps discriminator training. The generator contains two stages, a coarse recovery result is created by utilizing the gated convolution [8] and this coarse recovery result is further refined by the contextual attention [8] convolutional layer which implicitly encourages the network to focus on neighboring signal segments. By combining the convolution with a sigmoid function, the gated convolution helps the generator to learn that the signals in the missing areas are invalid values and the generator can therefore concentrate on the residual signal to capture the signal pattern. The GAN can thus process the scenarios that are not contained in the training dataset, as long as the residual signal can reflect the signal pattern. The spectral-normalized Markovian discriminator [8] is used to discriminate if the input is real or reconstructed from residual samples (fake).

## C. Loss Functions

The hinge loss for the generator [9] VG $- \mathbb { E } _ { \mathrm { s } \sim P _ { \mathrm { s } } ( \mathrm { s } ) }$ {mean $\left( D ^ { s n } ( G ( \mathbf { s } ) ) \right) $ in combination with the pixel-wise $l _ { 1 }$ reconstruction loss are used as the objective function for the generator, where G is the generator network that takes the incomplete signal s, $P _ { \mathrm { { s } } } ( \mathbf { s } )$ is thc gencrator distribution and $D ^ { s n }$ represents the spectral-normalizeddiscriminator.Thediscriminator uses only the hinge loss as its objective function $\begin{array} { r l r } { \mathcal { V } _ { D ^ { s n } } } & { { } = } & { \mathbb { E } _ { { \mathbf x } \sim P _ { \mathrm { d a t a } } ( { \mathbf x } ) } \left\{ \operatorname* { m e a n } \left( \operatorname* { m a x } \left( 0 , 1 - D ^ { s n } ( { \mathbf x } ) \right) \right) \right\} ~ + } \end{array}$ ${ / } { \mathbb { E } } _ { s \sim P _ { \mathrm { s } } ( \mathrm { s } ) } \left\{ { \mathrm { m e a n } } \left( { \mathrm { m a x } } \left( 0 , 1 + D ^ { s n } ( G ( \mathrm { s } ) ) \right) \right) \right\}$ , where $\mathrm { ~ \bf ~ x ~ } \mathrm { ~ \bf ~ i s ~ }$ the interference-free data and $P _ { \mathrm { d a t a } } ( \mathbf { x } )$ denotes the data distribution. IV DED

## IV. PERFORMANCE EVALUATION

The performance of the GAN is evaluated in terms of SINR in comparison with the autoregressive (AR) model and the zeroing method. The zeroing method is a basic technique for interference rejection in which the disturbed chirps in the RFFT spectrum are simply set to zero. The validation datasets contain arbitrary five or six targets which is a challenge to the GAN because the training datasets have only one to three targets. The results are presented in Figure 3. For a small percentage of discarded chirps, the RD spectrum recovered by the GAN has similar SINR as the AR method. However, when the percentage of discarded chirps is larger than 35%, the SINR of the AR method decreases while the GAN delivers consistent results. Before applying the recovery method, the disturbed chirps are set to zero, removing also noise from this region. Thus, the SINR after recovery is slightly better than the SINR of the original signal, which is indicated by the dotted line.

![](images/e192979a82f03b78210da408a7af83c13416b45f0a8eb37984485436160280be.jpg)  
Fig. 2. Generative Adversarial Network (GAN) for RFFT spectrum interferencc mitigation.

![](images/69714072b0726e28661f4a7682a51bd20b2f1235877498968409b9972cf592eb.jpg)  
Fig. 3. SINR of recovered RD spectrum.

Figure 4 shows thc comparison of thc rccovered RFFT spectrum and RD spectrum after applying the zeroing method and GAN, where 55% chirps are discarded. It should be noted that the proposed method can deal with scenarios in which a random number of consecutive chirps is disturbed. The recovery result in this severely disturbed scenario demonstrates the robustness of GAN.

![](images/39908e73cb05d61661225b678ae172d98fbe34a71503a2e1fb85407afad6295c.jpg)  
(a)

![](images/35e446e1b4d282ba16051462314b20c5d1868db89018bd658b6fa7a1e035703f.jpg)  
Fig. 4. (a) Zeroing-method-recovered RFFT spectrum and RD spectrum; (b) GAN-recovered RFFT spectrum and RD spectrum.  
(b)

## V. CONCLUSION

To the best of our knowledge, this work is the first to use a GAN as an interference mitigation approach to the RFFT spectrum in an automotive radar system. The analysis results show that the proposed method has its advantage in recovering the RFFT spectrum compared to the AR and zeroing methods in terms of SINR. It is shown that even in severely disturbed scenarios, the proposed method can improve the SINR of the RD spectrum by ca. 8 - 15 dB in comparison with the simple zeroing method. The proposed method can preserve its robustness in RFFT spectrum recovery even with up to 55% missing chirps, which is much more complex than the training scenarios in which only 20% chirps are discarded. The proposed GAN for interference mitigation is significantly more complex than the baseline methods. Therefore, we will investigate approaches with reduced complexity in future works.

## REFERENCES

[1] G. M. Brooker, "Mutual Interferencc of Millimcter-Wavc Radar Systems," IEEE Transactions on Electromagnetic Compatibility, vol. 49, pp. 170-181, 2007.

[2] C. Aydogdu et al., "Radar Interference Mitigation for Automated Driving: Exploring Proactive Strategies," in IEEE Signal Processing Magazine, vol. 37, no. 4, pp. 72-84, July 2020

[3] J. Mun, H. Kim and J. Lee, "A Deep Learning Approach for Automotive Radar Interference Mitigation," 2018 IEEE 88th Vehicular Technology Conference (VTC-Fall), Chicago, IL, USA, pp. 1-5, 2018.

[4] J. Rock, M. Toth, E. Messner, P. Meissner and F. Pernkopf, "Complex Signal Denoising and Interference Mitigation for Automotive Radar Using Convolutional Neural Networks," 2019 22th International Conference on Information Fusion (FUSION), Ottawa, ON, Canada, pp. 1-8, 2019.

[5] S. Neemat, O. Krasnov and A. Yarovoy, "An Interference Mitigation Technique for FMCW Radar Using Beat-Frequencies Interpolation in the STFT Domain," in IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207-1220, March 2019

[6] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, "Discussion of the Operating Range of Frequency Modulated Radars in the Presence of Interference," International Journal of Microwave and Wireless Technologies, vol. 6, pp. 371–378, June 2014.

[7] S. Iizuka, E. Simo-Serra and II. Ishikawa, "Globally and Locally Consistent Image Completion," ACM Transactions on Graphics (TOG), vol. 36, no. 4, pp. 107, 2017.

[8] J. Yu et al., "Free-Form Image Inpainting with Gated Convolution," 2019 IEEE/CVF International Conference on Computer Vision (ICCV), Seoul, Korea (South), pp. 4470-4479, 2019

[9] T. Miyato et al., "Spectral Normalization for Generative Adversarial Networks," arXiv preprint arXiv:1802.05957, 2018.