# SparseTVNet: Deep Learning for FMCW Radar Interference Mitigation

Shuyun Cheng<sup>1</sup>, Hao Zhang<sup>1</sup>, Yinghao Cheng<sup>1</sup>, Shunjun Wei<sup>1,2</sup>, Mou Wang<sup>1</sup>, Jun Shi<sup>1</sup>, Xiaoling Zhang<sup>1</sup>

<sup>1</sup>School of Information and Communication Engineering,

University of Electronic Science and Technology of China, Chengdu, China

<sup>2</sup>Precision Measurement Radar System Technology Key Laboratory of Sichuan Province, Chengdu, China 202352012030@std.uestc.edu.cn

Abstract—This paper proposes an interference mitigation scheme for FMCW radar by integrating deep learning with sparse optimization techniques. Specifically, the study introduces the SparseTVNet deep network, which maps the TV-ADMM algorithm into a deep learning framework, enabling automatic optimization of algorithm parameters. This approach significantly enhances the accuracy and efficiency of signal recovery, effectively addressing the sensitivity issues encountered by conventional methods in complex interference environments. Overall, it provides an efficient and reliable solution for radar interference mitigation.

Index Terms—Frequency Modulated Continuous Wave (FMCW) Radar, Interference Mitigation(IM), SparseTVNet, Deep Learning

## I. INTRODUCTION

With the development of autonomous driving and intelligent transportation systems, automotive radar has become increasingly important in environmental perception, navigation, and collision avoidance [1]. However, the growing number of radar systems leads to signal interference, significantly affecting detection, identification, and ranging accuracy, thereby threatening system performance and safety. Existing interference mitigation techniques generally suffer from issues such as insufficient accuracy, high computational complexity, and the loss of weak target signals [2], [3].

To address radar interference, this paper proposes a novel FMCW radar interference mitigation method that integrates deep learning with sparse representation techniques. Through an innovative TV-ADMM algorithm and the SparseTVNet deep network, automated parameter optimization is achieved, significantly improving interference mitigation efficiency and computational performance. The method efficiently handles complex nonlinear interference signals and improves highdimensional signal recovery accuracy through an adaptive multi-layer network structure. In summary, the proposed method combines the advantages of deep learning and sparse reconstruction, overcoming the limitations of traditional methods and demonstrating enhanced robustness and superior performance, providing solid support for practical automotive radar applications.

## II. THE PROPOSED METHOD

## A. Interference Mitigation Model

To effectively suppress interference while preserving the edges and details of the target signal, this paper introduces a sparse representation in the frequency domain and incorporates a Total Variation (TV) regularization term to enhance signal recovery. The mathematical formulation is given as follows.

Assuming the noise component is negligible, $\mathrm { i . e . , } N ( t ) \approx 0 .$ the received signal can be modeled as:

$$
Q ( t ) = S _ { b } ( t ) + I ( t )\tag{1}
$$

where $Q , I \ \in \ \mathbb { C } ^ { m \times 1 }$ denote the observed signal and the interference signal, respectively. Based on sparse modeling, the signal recovery problem can be formulated as:

$$
\operatorname* { m i n } _ { x , I } \ \| x \| _ { 1 } + \| I \| _ { 1 }\tag{2}
$$

where $\| \cdot \| _ { 1 }$ denotes the $L _ { 1 }$ norm, which promotes sparsity in the frequency domain.

To improve interference suppression and ensure stability during the time-frequency transformation, we introduce the Fourier transform matrix $\Gamma ~ \in ~ \mathbb { C } ^ { m \times m }$ . the target signal is represented as $S _ { b } = \Gamma x$ . Thus, the optimization problem is updated to:

$$
\hat { x } = \arg \operatorname* { m i n } _ { r } ~ \alpha _ { 1 } \| x \| _ { 1 } + \alpha _ { 2 } \| I \| _ { 1 } + \beta \| Q - \Gamma x - I \| _ { 2 } ^ { 2 }\tag{3}
$$

Here, $\boldsymbol { x } \in \mathbb { C } ^ { m \times 1 }$ , and $\alpha _ { 1 } , \alpha _ { 2 } , \beta$ are regularization parameters. For simplicity, we set $\alpha _ { 2 } = 1 - \alpha _ { 1 }$ . To enhance robustness against interference while preserving signal features, we incorporate a total variation (TV) regularization term:

$$
\hat { x } = \arg \operatorname* { m i n } _ { x } \alpha _ { 1 } \lVert x \rVert _ { 1 } + \alpha _ { 2 } \lVert I \rVert _ { 1 } + \beta \lVert Q - \Gamma x - I \rVert _ { 2 } ^ { 2 } + \lVert x \rVert _ { T V }\tag{4}
$$

The total variation norm is defined as:

$$
\| x \| _ { \mathrm { T V } } = \sum _ { i = 1 } ^ { N - 1 } \left| x _ { \mathrm { a b s } , i + 1 } - x _ { \mathrm { a b s } , i } \right| \cdot e ^ { j x _ { \mathrm { a n g } , i } }\tag{5}
$$

where $x _ { \mathrm { a b s } }$ and $x _ { \mathrm { a n g } }$ represent the amplitude and phase of the signal, respectively.

To solve the above problem efficiently, we adopt the Alternating Direction Method of Multipliers (ADMM), introduce auxiliary variables and Lagrange multipliers, and reformulate

![](images/c78b1c8ecc67294681c0a596e15ac85643e2ce6d1b22ad826b98327c72ea8ef1.jpg)  
Fig. 1. Flowchart of the SparseTVNet Network Architecture Based on the TV-ADMM Interference Suppression Method.

Algorithm TV-ADMM Interference Mitigation Method   
Require:   
Signal $Q ;$ Initialize $\mathbf { x } , \mathbf { I } , \mathbf { d } _ { 1 } , \mathbf { d } _ { 2 } , \mathbf { d } _ { 3 } , \mathbf { u } _ { 1 } , \mathbf { u } _ { 2 } , \mathbf { u } _ { 3 } .$   
Set relative error δ. Set maximum number of iterations $N .$   
Set regularization parameters $\alpha _ { 1 } , \alpha _ { 2 } , \beta , \gamma _ { 1 } , \gamma _ { 2 } ,$ γ<sub>3</sub>.   
Ensure:   
while $k \leq N$ do   
$\begin{array} { r } { { \bf { I } } ^ { k + 1 } = \frac { 1 } { \beta + \gamma _ { 3 } } \left[ \beta ( { \bf { Q } } - \Gamma { \bf { x } } ^ { k } ) + \gamma _ { 3 } ( { \bf { d } } _ { 3 } ^ { k } + { \bf { u } } _ { 3 } ^ { k } ) \right] } \end{array}$   
$\mathbf { x } ^ { k + 1 } = \frac { 1 } { \beta \mathbf { { { T } } } ^ { H } \mathbf { { { T } } } + \gamma _ { 1 } \nabla ^ { H } \nabla + \gamma _ { 2 } \mathbf { { I } } } \left[ \beta \mathbf { { { T } } } ^ { H } ( \mathbf { { Q } } - \mathbf { { { I } } } ^ { k + 1 } ) \right.$   
$+ \gamma _ { 1 } \nabla ^ { H } ( { \bf d } _ { 1 } ^ { k } + { \bf u } _ { 1 } ^ { k } ) + \gamma _ { 2 } ( { \bf d } _ { 2 } ^ { k } + { \bf u } _ { 2 } ^ { k } ) ]$   
$\begin{array} { r } { \mathbf { d } _ { 1 } ^ { k + 1 } = \operatorname { s o f t } ( \nabla \mathbf { x } ^ { k + 1 } - \mathbf { u } _ { 1 } ^ { k } , \frac { 1 } { \gamma _ { 1 } } ) } \end{array}$   
$\begin{array} { r } { \mathbf { d } _ { 2 } ^ { k + 1 } = \operatorname { s o f t } ( \mathbf { x } ^ { k + 1 } - \mathbf { u } _ { 2 } ^ { k } , \frac { \alpha _ { 1 } } { \gamma _ { 2 } } ) ^ { ' } } \end{array}$   
$\begin{array} { r } { \mathbf d _ { 3 } ^ { k + 1 } = \operatorname { s o f t } ( \mathbf I ^ { k + 1 } - \mathbf u _ { 3 } ^ { k } , \frac { \alpha _ { 2 } ^ { \prime \prime } } { \gamma _ { 3 } } ) } \end{array}$   
$\mathbf { u } _ { 1 } ^ { k + 1 } = \mathbf { u } _ { 1 } ^ { k } + \mathbf { d } _ { 1 } ^ { k + 1 } - \nabla \mathbf { x } ^ { \tilde { k } + 1 }$   
$\mathbf u _ { ? } ^ { { \dot { k } } + 1 } = \mathbf u _ { ? } ^ { \dot { k } } + \mathbf d _ { ? } ^ { { \dot { k } } + 1 } - \mathbf x ^ { k + 1 }$   
$\mathbf { u } _ { 3 } ^ { \tilde { k } + 1 } = \mathbf { u } _ { 3 } ^ { \tilde { k } } + \mathbf { d } _ { 3 } ^ { \tilde { k } + 1 } - \mathbf { I } ^ { k + 1 }$   
if $\begin{array} { r } { \frac { | | \mathbf { x } ^ { k + 1 } - \mathbf { x } ^ { k } | | _ { 2 } ^ { 2 } } { | | \mathbf { x } ^ { k } | | _ { \mathrm { \Omega } } ^ { 2 } } \leq \delta } \end{array}$ and $\frac { \| \mathbf { I } ^ { k + 1 } - \mathbf { I } ^ { k } \| _ { 2 } ^ { 2 } } { \| \mathbf { I } ^ { k } \| _ { 2 } ^ { 2 } } \leq \delta$ then   
$\mathbf { x } ^ { * } = \mathbf { x } ^ { \mathit { \Pi } ^ { \prime \prime } + 1 }$   
break   
else   
$\mathbf { x } ^ { k } = \mathbf { x } ^ { k + 1 }$   
end $\mathbf { i f }$   
end while   
return $\mathbf { x } ^ { * }$

the problem into an iterative form, as illustrated in the following algorithm.

Where, s $\mathrm { o f t } ( \mathbf { x } , \boldsymbol { \rho } ) = \mathrm { s i g n } ( \mathbf { x } ) \cdot \mathrm { m a x } ( | \mathbf { x } | - \boldsymbol { \rho } , 0 ) ; ( \cdot ) ^ { H }$ denotes Hermitian Transpose or Conjugate Transpose; $\alpha _ { 1 } = 1 - \alpha _ { 2 } .$

## B. SparseTVNet

1) network structure: The model consists of multiple BasicBlock layers, each containing a set of trainable parameters $( { \bf e . g . } , \lambda _ { 1 } , \rho , \beta ) ,$ , which are optimized during training to enhance signal recovery accuracy and maximize interference suppression. Each BasicBlock layer is similar to an iteration step in the TV-ADMM algorithm, refining the signal through nonlinear transformations and soft thresholding. Parameters like $\rho$ and λ control the update magnitude and direction, with each layer’s parameters independently adjusted to improve signal recovery flexibility. Each layer processes the signal and leverages complex-domain operations to capture phase information, enhancing recovery performance. This multilayer structure combines traditional optimization algorithms with deep learning techniques, utilizing large training datasets to optimize parameters for efficient interference suppression and accurate signal recovery, as shown in Fig. 1.

2) data preparation: In deep learning, the training dataset consists of input signals and label signals. The input signals are dimensionally reduced through a measurement matrix to simulate data loss or noise, while the label signals represent the original undisturbed signals, serving as the optimization target. The dataset is generated through random sampling to enhance generalization.Both the input and label signals are complex-valued, containing amplitude and phase information, providing rich features for signal recovery.

3) model training: This paper uses a PyTorch-based training framework. Input signals and label signals are read in batches and fed into the model, where the model generates predicted signals through interaction with the measurement matrix and computes the error between the predicted and true signals. The error is quantified using Total Squared Error Loss (TSEL), and model parameters are updated through backpropagation to minimize the error.

The learning rate is set to $1 \times 1 0 ^ { - 4 }$ , controlling the step size of parameter updates and influencing convergence speed. The model is trained for 300 epochs, with 16 samples randomly selected per batch for computation. The Adam optimizer is used to update the parameters, combining momentum and adaptive learning rates to speed up convergence and eliminate the need for manual learning rate adjustments.

Regularization terms, including the soft-thresholding function and Total Variation (TV) norm, are introduced during training. These regularizers control parameter magnitude, suppress noise, and preserve key signal features, ensuring the model maintains good generalization ability and robustness.

![](images/fa4862fa2ebc3e64d15839d0330725de22338d341cd45c93a0dd7bde087f81a5.jpg)

![](images/b766d060bdeb6aa1ae1836d85aa8e0ae970861ed576de9759509828ad13a9e61.jpg)

![](images/5318400c80d07f94a292aa97e496e87cebcc4799df5e6ce63020e7caf459a9c6.jpg)

![](images/f56feb02c4b5952fadd3f671de1bc7854b4e208761881884903b5e93ff24a088.jpg)

![](images/24d825a3591bb13c43c04d7841ada572a36c9573ca6255ef40560407971855f1.jpg)

![](images/e657151ba3cf5df709cefcbf6f2904bc2478c99a831fad304a4b81ea0089c94b.jpg)

![](images/7e129e4fcfb684cd0dfc3cffbd08142acf6c88812f5336e467e43d9876c08937.jpg)

![](images/1457a933582d2dddfb2ec9b048f7e5905977e8236bb17f28a3f334f2496a9cf6.jpg)  
Fig. 2. (a) Time-frequency domain plot without interference; (b) Distance-amplitude plot without interference; (c) Time-frequency domain plot with interference; (d) Distance-amplitude plot with interference; (e) Time-frequency domain plot after interference suppression using wavelet transform; (f) Distance-amplitude plot after interference suppression using wavelet transform; (g) Time-frequency domain plot after interference suppression using the method proposed in this paper; (h) Distance-amplitude plot after interference suppression using the method proposed in this paper.

## III. SIMULATION EXPERIMENTAL COMPARISON

In this simulation experiment, we performed both qualitative and quantitative evaluations of radar image quality before and after interference reduction. In the qualitative evaluation, the radar image should be clean, without high sidelobes and false targets, and the targets should be clearly visible. Fig. 2(a) and Fig. 2(b) show the scenario without interference, while Fig. 2(c) and Fig. 2(d) show the scenario with interference. Fig. 2(e) and Fig. 2(f) display the results after applying wavelet suppression [4] for interference reduction, and Fig. 2(g) and Fig. 2(h) show the method proposed in this paper, which better preserves and restores the amplitude information of the original signal, providing more accurate signal analysis results.

In the quantitative evaluation, we use the signal correlation coefficient ρ to assess the effectiveness of signal recovery after interference suppression.As the method used in [5], by analyzing the energy matching and structural similarity between the recovered signal $x ^ { * }$ and the original clean signal x, ρ provides an intuitive evaluation. It not only assesses energy retention but also considers the consistency of waveform and spectral characteristics.The signal correlation coefficient of the method proposed in this paper is 0.8771, with a phase deviation of 0.3215, while the wavelet transform method has a correlation coefficient of 0.4467 and a phase deviation of 0.3628. Without significant loss of phase information, the method proposed in this paper significantly improves the correlation coefficient, demonstrating its advantage in signal recovery.

## IV. CONCLUSION

Based on the TV-ADMM algorithm, this paper uses the SparseTVNet deep network to automatically optimize parameters, simplifying the parameter selection process. This approach improves the accuracy of interference suppression, computational efficiency, and enhances adaptability to different interference conditions. Simulation results show that the proposed method operates stably under interference from multi-target FMCW radar and performs excellently in terms of correlation coefficient and phase deviation. Future work will involve large-scale experiments in real-world road scenarios to validate the practicality of the proposed method.

## ACKNOWLEDGMENT

This paper is supported by the National Natural Science Foundation of China (62401119, 62271108, and 62371104); and the China Postdoctoral Science Foundation(Grant 2024T170104, 2024M760354).

## REFERENCES

[1] E. Hyun, W. Oh and J. -H. Lee, ”Detection and tracking algorithm for 77GHz automotive FMCW radar,” 2011 3rd International Asia-Pacific Conference on Synthetic Aperture Radar (APSAR), Seoul, Korea (South), 2011, pp. 1-4.

[2] J. Wang, R. Li, X. Zhang and Y. He, ”Interference Mitigation for Automotive FMCW Radar Based on Contrastive Learning With Dilated Convolution,” in IEEE Transactions on Intelligent Transportation Systems, vol. 25, no. 1, pp. 545-558, Jan. 2024, doi: 10.1109/TITS.2023.3306576.

[3] J. Wang, R. Li, Y. He and Y. Yang, ”Prior-Guided Deep Interference Mitigation for FMCW Radars,” in IEEE Transactions on Geoscience and Remote Sensing, vol. 60, pp. 1-16, 2022, Art no. 5118316, doi: 10.1109/TGRS.2022.3211605.

[4] H. Zhang, S. Wei, M. Wang, Y. Hu, J. Shi and G. Cui, ”FUAS-Net: Feature-Oriented Unsupervised Network for FMCW Radar Interference Suppression,” in IEEE Transactions on Microwave Theory and Techniques, vol. 72, no. 4, pp. 2602-2619, April 2024, doi: 10.1109/TMTT.2023.3318669.

[5] S. Lee, J. -Y. Lee and S. -C. Kim, ”Mutual Interference Suppression Using Wavelet Denoising in Automotive FMCW Radar Systems,” in IEEE Transactions on Intelligent Transportation Systems, vol. 22, no. 2, pp. 887-897, Feb. 2021, doi: 10.1109/TITS.2019.2961235.