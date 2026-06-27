# MODEL-BASED DIFFUSION FOR MITIGATING AUTOMOTIVE RADAR INTERFERENCE

J. Overdevest<sup>§⋆</sup>†, X. Wei<sup>§</sup>†, H. van Gorp†, R.J.G. van Sloun†

<sup>⋆</sup>Signal Processing Algorithms, NXP Semiconductors, Eindhoven, The Netherlands † Dept. of Electrical Engineering, Eindhoven University of Technology, Eindhoven, The Netherlands

## ABSTRACT

Mitigating automotive radar-to-radar interference is a challenging task, especially when the observed signal is densely corrupted with highly correlated interference signals. In this paper, we propose to remove this interference using jointconditional posterior sampling with score-based diffusion models. These models use three individual scores: a target score, an interference score, and a joint data consistency score. Leveraging the sparsity of clean target signals in the Fourier domain, we propose a model-based score estimator for the target signals, derived from the proximal step of the ℓ -norm. For the interference score, we use a neural network with denoising score-matching, given that it is difficult to obtain analytical statistical models of the interference signals. Lastly, the target and interference scores are connected by a data-consistency score. Experimental results show that our solution results in superior performance over state-of-the-art methods, in terms of normalized mean squared error (NMSE) and receiver operating characteristic (ROC) curves.

Index Terms— Automotive Radar Interference, Deep Learning, Diffusion Models

## 1. INTRODUCTION

Automotive inter-radar interference has been intensively studied due to the severe impact it can have on driving performance, especially with more radars being deployed on vehicles in the next years. Avoiding interference altogether is the first attempt to reduce its impact; either in a coordinated or uncoordinated fashion [1]. However, once the interference enters the receiver front-end, mitigation using signal processing is required. In the digital domain, many degrees of freedom can be exploited to reduce the impact, i.e. time [2], frequency [3], time-frequency [4], and/or space [5, 6]. Besides, several deep neural networks have been proposed [7, 8], of which some exploit a signal prior [9]. While Bayesian algorithms have achieved promising performance, this performance hinges on accurate signal priors. The adoption of highly expressive generative models is a promising direction to model these signal priors.

Score-based diffusion models, a subset of generative probabilistic models, have demonstrated the capability to approximate complex data distributions [10, 11]. They are state-of-the-art for image generation as well as inverse problem solving across a variety of applications [12, 13, 14]. Stevens et al. recently proposed to remove structured noise from natural images [15] and ultrasound data [16] using a joint conditional diffusion process.

In this paper, we propose a joint-conditional probabilistic diffusion model that can effectively separate radar interference signals from target signals in the time domain, specifically designed to remove highly correlated interference, as well as densely corrupted Frequency-Modulated Continuous Wave (FMCW) chirp signals. To our knowledge, we are the first to apply diffusion models to radar signals. For interference mitigation, we adopt two separate scores to incorporate two independent signal priors. Firstly, a novel model-based score is introduced within a diffusion model, called a proximal score function, that is designed for sparse target signals in the Fourier domain, offering denoising in the complex domain with reduced computational complexity. Secondly, a learned score function for interference signals exploits the signal structure in the time domain. We demonstrate that our approach outperforms other one-dimensional state-of-the-art reconstruction methods [17, 18].

## 2. SIGNAL MODEL

In automotive radar, the received signals can consist of target reflections (desired), inter-vehicle interference (undesired), and thermal noise (undesired). Given that FMCW is the most common waveform in automotive radar applications, we shall focus our signal model to FMCW radars. For a single receive antenna and a single chirp, the sampled signal $\mathbf { y } \in \mathbb { R } ^ { N }$ can be expressed as [17]:

$$
{ \bf y } = \sum _ { k } { \bf x } ^ { ( k ) } + \sum _ { l } { \bf i } ^ { ( l ) } + { \bf n } = { \bf x } + { \bf i } + { \bf n } ,\tag{1}
$$

where $\mathbf { x } ^ { ( k ) } = \alpha _ { k } \sin ( \omega _ { k } \mathbf { v } + \phi _ { k } )$ with $\mathbf { v } = \left\lceil 0 , \dots , M - 1 \right\rceil$ denotes the k-th target reflection with $\alpha _ { k } , \ \omega _ { k }$ and $\phi _ { k }$ representing the received signal amplitude, its frequency and phase, respectively, and M is the number of fast-time samples. Moreover, $\mathbf { \dot { i } } ^ { ( l ) }$ refers to the l-th interference signal which is generally known to be time-limited after analog down-mixing and anti-aliasing filtering. Lastly, n is the thermal noise, modeled using a zero-mean Gaussian distribution.

## 2.1. Source Separation Approach

Our goal is to mitigate the interference i while preserving the targets x, which we propose to solve using a source separation approach. Given the ill-posed nature of the problem, and assuming that the target and interference signals are independent with distinct data distributions, we introduce priors and sample from the joint conditional posterior using:

$$
\mathbf { x } , \mathbf { i } \sim p ( \mathbf { x } , \mathbf { i } | \mathbf { y } ) \propto p ( \mathbf { y } | \mathbf { x } , \mathbf { i } ) \cdot p ( \mathbf { x } ) \cdot p ( \mathbf { i } ) ,\tag{2}
$$

where $p ( \mathbf { x } , \mathbf { i } | \mathbf { y } )$ is the joint conditional posterior distribution. Additionally, $p ( \mathbf { x } )$ is the prior for the targets, which are known to be sparse in the Fourier domain. Besides, $p ( \mathbf { i } )$ represents the prior for the interference, explicitly modeled in the time domain using a deep generative network. Lastly, $p ( \mathbf { y } | \mathbf { x } , \mathbf { i } )$ denotes the joint data consistency term. We now propose a three-stage approach to get samples from the joint conditional posterior. First, we define separate priors for interference and targets. Subsequently, we incorporate the priors into a diffusion process. Finally, we derive the estimated interference and subtract it from the noisy observations. This aids in preserving the weak targets buried under the noise floor, setting the stage for their recovery in subsequent signal processing steps.

## 3. METHOD

Diffusion models are generative models that evolve data in a forward diffusion process, ultimately leading to random Gaussian noise. This process can be represented by a stochastic differential equation (SDE):

$$
\begin{array} { r } { \mathrm { d } \mathbf { x } = f ( t ) \mathbf { x } + g ( t ) \mathrm { d } \mathbf { w } , } \end{array}\tag{3}
$$

where $f ( t )$ and $g ( t )$ are the drift and diffusion coefficients, respectively, at time step t. Here, we choose to utilize Variance Preserving (VP) SDE for perturbing both the targets and interference. Given a clean sample $\mathbf { x } _ { \mathrm { 0 } }$ from the target distribution, the perturbed data at time step t can be represented as: $\mathbf { x } _ { t } = \sqrt { \bar { \alpha } _ { t } } \mathbf { x } _ { 0 } + \sqrt { 1 - \bar { \alpha } _ { t } } \mathbf { z }$ with $\mathbf { z } \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } )$ and $\bar { \alpha } _ { t } = \prod _ { t } \alpha _ { t }$ with $\alpha _ { t }$ being a scalar determined from $f ( t )$ and $g ( t )$

Time-reversing the process enables us to generate novel samples from the target data distribution. The generation relies on the gradient of the log-probability density function, commonly known as the score, and can be analytically expressed through a reverse-time SDE. For joint conditional data generation, the corresponding reverse-time SDE can be formulated as follows:

$$
\mathrm { d } ( \mathbf { x } _ { t } , \mathbf { i } _ { t } ) = \bigg [ f ( t ) ( \mathbf { x } _ { t } , \mathbf { i } _ { t } ) - g ( t ) ^ { 2 } \nabla _ { \mathbf { x } _ { t } , \mathbf { i } _ { t } } \log p ( \mathbf { x } _ { t } , \mathbf { i } _ { t } | \mathbf { y } ) \bigg ] \mathrm { d } t + g ( t ) \bar { \mathbf { w } } _ { t } .\tag{4}
$$

However, $\nabla _ { \mathbf x _ { t } , \mathbf i _ { t } }$ log $p ( \mathbf { x } _ { t } , \mathbf { i } _ { t } | \mathbf { y } )$ is not directly solvable. To address it, we resort to (2) and take the derivative with respect to $\mathbf { x } _ { t }$ or $\mathbf { i } _ { t } .$ . This results in the following equations:

$$
\begin{array} { r l } & { \nabla _ { \mathbf { x } _ { t } } \log p ( \mathbf { x } _ { t } , \mathbf { i } _ { t } | \mathbf { y } ) = \nabla _ { \mathbf { x } _ { t } } \log p ( \mathbf { x } _ { t } ) + \nabla _ { \mathbf { x } _ { t } } \log p ( \mathbf { y } | \mathbf { x } _ { t } , \mathbf { i } _ { t } ) , } \\ & { \nabla _ { \mathbf { i } _ { t } } \log p ( \mathbf { x } _ { t } , \mathbf { i } _ { t } | \mathbf { y } ) = \nabla _ { \mathbf { i } _ { t } } \log p ( \mathbf { i } _ { t } ) + \nabla _ { \mathbf { i } _ { t } } \log p ( \mathbf { y } | \mathbf { x } _ { t } , \mathbf { i } _ { t } ) . } \end{array}\tag{5}
$$

(6)

![](images/209ffab3f3b73b278b6c481737231995d17be606b0449105cee275832c36b745.jpg)  
Fig. 1: Block diagram of the proposed joint-conditional diffusion model.

Consequently, for generating interference-free signals via the joint conditional reverse-time SDE, it is essential to obtain knowledge of the scores of the targets, interference, and joint data consistency, which we address in Sections 3.1, 3.2, and 3.3. We refer to the procedure as a joint conditional diffusion process. See Fig. 1 for an overview.

## 3.1. Proximal Score Function: Targets

The clean target signal x is a sparse superposition of sinusoidal signals, as previously noted in (1). Therefore, we propose to model the prior belief of $\mathbf { X } = \mathcal { F } \mathbf { x }$ as a Laplace distribution. Using this prior knowledge, we can calculate the score function of the target signal $\nabla _ { \mathbf { x } _ { t } } \log p ( \mathbf { x } _ { t } )$ from (5) more accurately in the Fourier domain. Moreover, we can define the score using Tweedie’s approximation [19]:

$$
\nabla _ { \mathbf { X } _ { t } } \log { p ( \mathbf { X } _ { t } ) } = \frac { \sqrt { \bar { \alpha } _ { t } } \mathbf { X } _ { 0 \mid t } - \mathbf { X } _ { t } } { 1 - \bar { \alpha } _ { t } } ,\tag{7}
$$

where $\mathbf { X } _ { 0 \mid t }$ denotes the posterior mean $\mathbb { E } [ \mathbf { X } _ { 0 } | \mathbf { X } _ { t } ]$ , i.e., a denoised estimate from $\mathbf { X } _ { t }$ at time step t. Assuming independent Laplacian priors, the denoising problem is solved using the Maximum A Posterior (MAP) estimator, hence the denoised estimate $\mathbf { X } _ { 0 \mid t }$ is found from

$$
{ \bf X } _ { 0 \vert t } = \arg \operatorname* { m i n } _ { { \bf X } } \frac { 1 } { 1 - \bar { \alpha } _ { t } } \vert \vert { \bf X } _ { t } - { \bf X } \vert \vert _ { 2 } ^ { 2 } + \lambda \vert \vert { \bf X } \vert \vert _ { 1 } ,\tag{8}
$$

where $1 - \bar { \alpha } _ { t }$ refers to noise variance at time step t and λ is a scalar that balances the reconstruction error against sparsity. The solution to (8) is known to be the proximal step, defined by the soft threshold operator

$$
\mathbf { X } _ { 0 \mid t } = \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } \mathrm { p r o x } _ { \lambda \mid \mid \cdot \mid \mid } ( \mathbf { X } _ { t } ) = \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } \frac { \mathbf { X } _ { t } } { \vert \mathbf { X } _ { t } \vert } ( \vert \mathbf { X } _ { t } \vert - \lambda ) _ { + } ,\tag{9}
$$

where the threshold λ is determined from the noise variance and the Laplace scale parameter $\bar { \sigma } _ { L }$ at time step t, hence $\begin{array} { r } { \lambda = \frac { \sqrt { 2 } ( 1 - \bar { \alpha } _ { t } ) } { \sqrt { \bar { \alpha } _ { t } } \bar { \sigma } _ { L } } } \end{array}$ . Unlike current real-valued diffusion models, our proximal score enables denoising complex input data, i.e. Fourier transformed data. Then, $\mathbf { X } _ { 0 \mid t }$ is used to retrieve the perturbed estimate of the previous time step $\tilde { \mathbf { x } } _ { t - 1 }$

## 3.2. Learned Score Function: Interference

Given the challenging nature of modeling the interference signal, we employ a neural network to estimate the interference’s score function $\mathbf { \boldsymbol { s } } _ { \theta } ( \mathbf { \boldsymbol { i } } _ { t } , t ) \approx \nabla _ { \mathbf { \boldsymbol { i } } _ { t } } \log { p ( \mathbf { \boldsymbol { i } } _ { t } ) }$ , which can be injected into (6). Here, we adopt a conditional U-Net architecture, following [20], while with modifications that incorporate selfattention for better temporal correlation estimation. During training, we perturb the clean interference $\mathbf { i } _ { 0 } \sim p _ { 0 } ( \mathbf { i } )$ to obtain the noisy samples $\mathbf { i } _ { t } \sim q ( \mathbf { i } _ { t } | \mathbf { i } _ { 0 } )$ , which are then fed into the network. The score function is estimated by employing denoising score matching [21], as formulated below:

$$
\pmb { \theta } ^ { * } = \arg \operatorname* { m i n } _ { \pmb { \theta } } \mathbb { E } _ { t } \left[ \mathbf { w } _ { t } \mathbb { E _ { i _ { 0 } } } \mathbb { E _ { i _ { t } | i _ { 0 } } } \Bigg | \Bigg | s _ { \pmb { \theta } } ( \mathbf { i } _ { t } , t ) - \nabla _ { \mathbf { i } _ { t } } \log q ( \mathbf { i } _ { t } | \mathbf { i } _ { 0 } ) \Bigg | \right] _ { 2 } ^ { 2 } ,\tag{10}
$$

where $\pmb \theta$ denotes the learnable parameters within the neural network, $\mathbf { w } _ { t }$ is a positive weighting function, t is uniformly sampled over $[ 1 0 ^ { - 5 } , 1 ]$ The objective of the training is to minimize the weighted squared error between the estimated score by the network and the score of the perturbed interference, sampled at various t. Guided by this objective, the network functions as a denoiser, steering towards the direction of clean samples by connecting the manifolds at different time steps. After adequately training the network, similar to $( 7 )$ , the posterior mean of the interference signal $\mathbf { i } _ { 0 \mid t }$ can be described by exploiting Tweedie’s approximation:

$$
\mathbf { i } _ { 0 \mid t } \approx \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } \Bigl ( \mathbf { i } _ { t } + \left( 1 - \bar { \alpha } _ { t } \right) \mathbf { s } _ { \theta } \left( \mathbf { i } _ { t } , t \right) \Bigr ) ,\tag{11}
$$

which implies that for a perturbed sample $\mathbf { i } _ { t } ,$ , the learned score allows to retrieve its noise-reduced version, $\mathbf { i } _ { 0 \mid t }$ . Analogous to the target signals, during inference, this can be used to obtain the perturbed estimate of the previous time step $\tilde { \mathbf { i } } _ { t - 1 }$

## 3.3. Joint Data Consistency Score

The score of the joint data consistency in (5) and (6) is typically intractable due to its dependence on the perturbed signals at time t. Instead, we employ a method known as Diffusion Posterior Sampling (DPS) as a surrogate, as described in [13]. Considering our measurement model, as described in (1), adheres to a Gaussian distribution with a zero mean and a standard deviation of $\sigma _ { n } .$ , we can establish the following approximation:

$$
p ( \mathbf { y } | \mathbf { x } _ { t } , \mathbf { i } _ { t } ) \approx p ( \mathbf { y } | \mathbf { x } _ { 0 | t } , \mathbf { i } _ { 0 | t } ) \sim \mathcal { N } ( \mathbf { x } _ { 0 | t } + \mathbf { i } _ { 0 | t } , \sigma _ { n } ^ { 2 } ) ,\tag{12}
$$

where ${ \bf x } _ { 0 \vert t } = \mathcal { F } ^ { \mathrm { H } } { \bf X } _ { 0 \vert t }$ and $\mathbf { i } _ { 0 \mid t }$ are obtained using (9) and (11), respectively. To this end, the score of the joint data consistency turns tractable and can be formulated as follows:

$$
\nabla _ { \mathbf { x } _ { t } } \log p ( \mathbf { y } | \mathbf { x } _ { t } , \mathbf { i } _ { t } ) \approx - \frac { 1 } { \sigma _ { n } ^ { 2 } } \nabla _ { \mathbf { x } _ { t } } \| \mathbf { y } - \mathbf { x } _ { 0 | t } - \mathbf { i } _ { 0 | t } \| _ { 2 } ^ { 2 }\tag{13}
$$

$$
\nabla _ { \mathbf { i } _ { t } } ~ \log p ( \mathbf { y } \vert \mathbf { x } _ { t } , \mathbf { i } _ { t } ) \approx - \frac { 1 } { \sigma _ { n } ^ { 2 } } \nabla _ { \mathbf { i } _ { t } } ~ \Vert \mathbf { y } - \mathbf { x } _ { 0 \vert t } - \mathbf { i } _ { 0 \vert t } \Vert _ { 2 } ^ { 2 }\tag{14}
$$

By integrating the score functions of the targets, interference and joint data consistency within an iterative framework, we establish a comprehensive flow for a joint conditional process. See the algorithm below for details. In this paper, the estimated target signal $\hat { \mathbf { x } } = \mathbf { y } - \mathbf { i } _ { 0 }$ is used for evaluation.

Algorithm 1 Joint Conditional Posterior Sampling   
Input: N , y, s<sub>θ</sub>, $\bar { \sigma } _ { L } , \varepsilon _ { 1 } , \varepsilon _ { 2 }$   
Initialization: ${ \bf x } _ { N } \sim \mathcal { N } ( { \bf 0 } , { \bf I } ) , { \bf i } _ { N } \sim \mathcal { N } ( { \bf 0 } , { \bf I } )$   
1: for $i = N - 1$ to 0 do   
2: $\textstyle t \gets { \frac { i + 1 } { N } }$   
3: λ← <sup>√</sup>2(1 α¯<sub>t</sub>)   
<sup>√</sup>α¯<sub>t</sub>σ¯<sub>L</sub>   
4: $\begin{array} { r l } & { c _ { 1 } \gets \frac { \check { \sqrt { \alpha _ { t } } } ( 1 - \bar { \alpha } _ { t - 1 } ) } { 1 - \bar { \alpha } _ { t } } , \ c _ { 2 } \gets \frac { \sqrt { \bar { \alpha } _ { t - 1 } } \beta _ { t } } { 1 - \bar { \alpha } _ { t } } , \ c _ { 3 } \gets \frac { 1 - \bar { \alpha } _ { t - 1 } } { 1 - \bar { \alpha } _ { t } } } \\ & { \mathbf { z } \gets \mathsf { N } / ( \mathbf { 0 } \textbf { I } ) } \end{array}$   
5: z <sub>←</sub> <sub>N</sub> (0, I)   
▷ Calculate Posterior mean   
6: $\begin{array} { r } { \mathbf { X } _ { 0 \mid t }  \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } \mathbf { p r o x } _ { \lambda \mid \mid \cdot \mid \mid } ( \mathcal { F } \mathbf { x } _ { t } ) } \end{array}$   
7: $\mathbf { x } _ { 0 \mid t }  \mathcal { F } ^ { H } \mathbf { X } _ { 0 \mid t }$   
8: i<sub>0|t</sub> $\begin{array} { r } {  \frac { 1 } { \sqrt { \bar { \alpha } _ { t } } } ( \mathbf { i } _ { t } + ( 1 - \bar { \alpha } _ { t } ) \mathbf { s } _ { \theta } ( \mathbf { i } _ { t } , t ) ) } \end{array}$   
9: x˜<sub>t 1 ←</sub> c<sub>1</sub>x<sub>t</sub> + c<sub>2</sub>x<sub>0 t</sub> + c<sub>3</sub>z   
10: $\tilde { \mathbf { i } } _ { t - 1 } \gets c _ { 1 } \mathbf { i } _ { t } + c _ { 2 } \mathbf { i } _ { 0 | t } + c _ { 3 } \mathbf { z }$   
▷ Data consistency steps   
11: $\mathbf { x } _ { t - 1 }  \tilde { \mathbf { x } } _ { t - 1 } - \varepsilon _ { 1 } \nabla _ { \mathbf { x } _ { t } } \| \mathbf { y } - \mathbf { x } _ { 0 \mid t } - \mathbf { i } _ { 0 \mid t } \| _ { 2 } ^ { 2 }$   
12: $\mathbf { i } _ { t - 1 } \longleftarrow \mathbf { \hat { i } } _ { t - 1 } - \varepsilon _ { 2 } \nabla _ { \mathbf { i } _ { t } } \| \mathbf { y } - \mathbf { x } _ { 0 \mid t } - \mathbf { i } _ { 0 \mid t } \| _ { 2 } ^ { 2 }$   
13: end for   
14: return $\hat { \mathbf { x } } = \mathbf { y } - \mathbf { i } _ { 0 }$

## 4. RESULTS

## 4.1. Experimental Setup

The radar data y is simulated for $K \in \{ 1 , 2 , \ldots , 3 0 \}$ targets, each target having a Signal-to-Noise Ratio (SNR) between 30 dB and 20 dB. The number of interferers is limited to one, which is configured to have an Interference-to-Noise Ratio (INR) between 0 dB and 20 dB and randomly configured interference chirp settings, i.e., chirp slope, chirp rate, RF chirp bandwidth, chirp duration, carrier frequency, etc., such that a broad range of interference samples are achieved.

First, we trained the interference score function using a training dataset composed of 7,000 clean interference samples. The INR was randomly sampled from a range of 0 dB to 20 dB. For training, the batch size was set to 100 and training was stopped after convergence, which generally required a minimum of 500 epochs. For optimization, we employ the Adam optimizer with a learning rate set at $1 0 ^ { - 4 }$ Subsequently, the score functions were integrated into an iterative framework. The hyperparameters $\lambda , \varepsilon _ { 1 }$ , and $\varepsilon _ { 2 }$ were fine-tuned based on the validation set.

## 4.2. Evaluation Metrics and Discussion

To emphasize the effectiveness of the proposed technique compared to state-of-the-art methods, we estimate the reconstruction performance in the time domain using the Normalized Mean Squared Error (NMSE) of xˆ by $1 0 \log _ { 1 0 } \left( \frac { | | \mathbf { x } - \hat { \mathbf { x } } | | _ { 2 } ^ { 2 } } { | | \mathbf { x } | | _ { 2 } ^ { 2 } } \right)$

![](images/434463571beacac795b29583c3f3593e01fa0d844d8e969777652fec740ec837.jpg)

![](images/8e770cd0bf7f32a39e87e477b777c60316b1180c6c56a53629af086916aae35b.jpg)  
Fig. 2: Reconstruction for $\mathrm { S N R } = - 2 0 \mathrm { d B }$ and $\mathbf { I N R } = 0 \mathrm { d B }$ (top) Time-domain signal y, (bottom) Distance spectrum Y.

Table 1: Reconstruction Performance, measured in NMSE
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>SNR=-20 dB</td><td rowspan=1 colspan=3>SNR=0 dB</td></tr><tr><td rowspan=1 colspan=1>INRMethod</td><td rowspan=1 colspan=1>0 dB</td><td rowspan=1 colspan=1>10 dB</td><td rowspan=1 colspan=1>20 dB</td><td rowspan=1 colspan=1>0 dB</td><td rowspan=1 colspan=1>10 dB</td><td rowspan=1 colspan=1>20 dB</td></tr><tr><td rowspan=2 colspan=1>No mitigationZeroingSALSA [17]LowRaS [18]Diffuse (ours)</td><td rowspan=1 colspan=1>6.381</td><td rowspan=2 colspan=1>66.971.37520.8939.820.252</td><td rowspan=2 colspan=1>651.88.621198.4402.80.286</td><td rowspan=2 colspan=1>0.4120.3220.2470.6770.394</td><td rowspan=2 colspan=1>4.4870.4541.4252.9530.361</td><td rowspan=2 colspan=1>44.822.78913.8625.130.337</td></tr><tr><td rowspan=1 colspan=1>0.6112.1794.1430.159</td></tr></table>

and the detection performance using ROC curves, implemented with Ordered-Statistic Constant False Alarm Rate (OS-CFAR) on the distance spectrum X<sup>ˆ</sup> . Our method is compared to other source separation solutions that exploit sparsity in transformed domains (frequency, and STFT resp.) [17], or in Hankelized matrices [18].

In Fig. 2 and 3, we present two examples of real-valued time-domain signal xˆ and the positive frequency components of Fxˆ to substantiate the reconstruction performance of the proposed method in realistic interference scenarios, an uncorrelated and semi-correlated case, respectively. Despite the low SNR-valued target signal, we can accurately remove the interference and recover the distance spectrum. In Tab. 1, statistically grounded results for various SNR and INR values are provided. Hereby, we prove that our method significantly outperforms other methods for all cases, except when SNR = 0 dB and INR = 0 dB. Here, the learned interference score experiences difficulties in separating low-amplitude interference signals from target signals with similar power, which we intend to address in future work.

In Fig. 4, we show the ROC curves to compare various algorithms for a single target and single interferer by fixing SNR and INR. The detection performance of our method is close to the performance of the clean signal, but it significantly outperforms the other methods for all preset falsealarm rates $P _ { F A }$ of the detector.

![](images/0a7702f12ec71016b7dd7ddd277b0033392cfb0ad4be25a7d66715b9fbf58832.jpg)

![](images/9177d4ae3fd492f6b606ae5c522b0b3f526770a075a0776180bfdf0650d73b0c.jpg)  
Fig. 3: Reconstruction for SNR = 20 dB and INR = 20 dB (top) Time-domain signal y, (bottom) Distance spectrum Y.

![](images/ae305191431077f81fe8a4a23e6f0af20088d8d5fefdaa3d5730f1b952b00acf.jpg)

![](images/ffb15550f79e45cf3923a6ee59849e68d973f43a4281c7301074f24105f6ae3f.jpg)  
Fig. 4: ROC curves for SNR = 20 dB with 1 interferer with (top) INR = 0 dB and (bottom) INR = 20 dB.

## 5. CONCLUSIONS

We present a novel and flexible algorithm to address the interference mitigation problem as an inverse problem. Our method leverages a complex-valued proximal score function that implicitly serves as a target signal prior. In addition, we utilize a data-driven score, to accurately represent the signal structure of the interference. Moreover, leveraging the core of the diffusion process, we integrate the score functions to enable joint conditional posterior sampling. Empirically, we demonstrate that this algorithm surpasses other leading reconstruction methods utilized in FMCW automotive radar. While the paper emphasizes removing FMCW radar interference, the proposed approach is flexible and thus may be adapted to train on various interfering waveforms, i.e., Phase-Modulated Continuous Wave, Orthogonal Frequency Domain Multiplexing, and more.

## 6. REFERENCES

[1] Lizette Lorraine Tovar Torres, Timo Grebner, and Christian Waldschmidt, “Automotive radar interference avoidance strategies for complex traffic scenarios,” in 2023 IEEE Radar Conference (RadarConf23), 2023, pp. 1–6.

[2] Francesco Laghezza, Feike Jansen, and Jeroen Overdevest, “Enhanced interference detection method in automotive FMCW radar systems,” in 2019 20th International Radar Symposium (IRS), 2019, pp. 1–7.

[3] Jonathan Bechter, Fabian Roos, Mahfuzur Rahman, and Christian Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in 2017 European Radar Conference (EURAD), 2017, pp. 90– 93.

[4] Sharef Neemat, Oleg Krasnov, and Alexander Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the STFT domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, 2019.

[5] C. Fischer, M. Goppelt, H.-L. Blocher, and J. Dickmann,¨ “Minimizing interference in automotive radar using digital beamforming,” Advances in Radio Science, vol. 9, pp. 45–48, 2011.

[6] Sian Jin, Pu Wang, Petros Boufounos, Philip V. Orlik, Ryuhei Takahashi, and Sumit Roy, “Spatial-domain interference mitigation for slow-time MIMO-FMCW automotive radar,” in 2022 IEEE 12th Sensor Array and Multichannel Signal Processing Workshop (SAM), 2022, pp. 311–315.

[7] Shengyi Chen, Wangyi Shangguan, Jalal Taghia, Uwe Kuhnau, and Rainer Martin, “Automotive radar inter-¨ ference mitigation based on a generative adversarial network,” in 2020 IEEE Asia-Pacific Microwave Conference (APMC), 2020, pp. 728–730.

[8] Nicolae-Cat˘ alin Ristea, Andrei Anghel, and Radu Tu-˘ dor Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall), 2020, pp. 1–5.

[9] J. Overdevest, A.G.C. Koppelaar, M.J.G. Bekooij, J. Youn, and R.J.G. van Sloun, “Signal reconstruction for fmcw radar interference mitigation using deep unfolding,” in ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2023, pp. 1–5.

[10] Yang Song, Jascha Sohl-Dickstein, Diederik P. Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole, “Score-based generative modeling through stochastic differential equations,” ICLR 2021, 2021.

[11] Jonathan Ho, Ajay Jain, and Pieter Abbeel, “Denoising diffusion probabilistic models,” Advances in neural information processing systems, vol. 33, pp. 6840–6851, 2020.

[12] Yang Song, Liyue Shen, Lei Xing, and Stefano Ermon, “Solving inverse problems in medical imaging with score-based generative models,” arXiv:2111.08005, 2021.

[13] Hyungjin Chung, Jeongsol Kim, Michael Thompson Mccann, Marc Louis Klasky, and Jong Chul Ye, “Diffusion posterior sampling for general noisy inverse problems,” in The Eleventh International Conference on Learning Representations, 2023.

[14] Jiaming Song, Arash Vahdat, Morteza Mardani, and Jan Kautz, “Pseudoinverse-guided diffusion models for inverse problems,” in International Conference on Learning Representations, 2022.

[15] Tristan S. W. Stevens, Hans van Gorp, Faik C. Meral, Jun Seob Shin, Jason Yu, Jean-Luc Robert, and Ruud J. G. van Sloun, “Removing structured noise with diffusion models,” arXiv:2302.05290, 2023.

[16] Tristan S. W. Stevens, Faik C. Meral, Jason Yu, Iason Z. Apostolakis, Jean-Luc Robert, and Ruud J. G. van Sloun, “Dehazing ultrasound using diffusion models,” arXiv:2307.11204, 2023.

[17] Faruk Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846– 5852, 2019.

[18] Jianping Wang, Min Ding, and Alexander Yarovoy, “Interference mitigation for fmcw radar with sparse and low-rank hankel matrix decomposition,” IEEE Transactions on Signal Processing, vol. 70, pp. 822–834, 2022.

[19] Bradley Efron, “Tweedie’s formula and selection bias,” Journal of the American Statistical Association, vol. 106, no. 496, pp. 1602–1614, 2011.

[20] Simon Rouard and Gaetan Hadjeres, “Crash: Raw¨ audio score-based generative modeling for controllable high-resolution drum sound synthesis,” ArXiv, vol. abs/2106.07431, 2021.

[21] Pascal Vincent, “A connection between score matching and denoising autoencoders,” Neural Computation, vol. 23, no. 7, pp. 1661–1674, 2011.