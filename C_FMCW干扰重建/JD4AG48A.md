# Deep Unfolding Using Score-based Generative Networks for Automotive Radar Interference Mitigation

Citation for published version (APA):

Wei, X., Youn, J., Overdevest, J., Li, J., Ravindran, S., & van Sloun, R. J. G. (2025). Deep Unfolding Using Score-based Generative Networks for Automotive Radar Interference Mitigation. In Article 10889785 Institute of Electrical and Electronics Engineers. https://doi.org/10.1109/ICASSP49660.2025.10889785

Document license: TAVERNE

DOI: 10.1109/ICASSP49660.2025.10889785

Document status and date: Published: 07/03/2025

Document Version: Publisher’s PDF, also known as Version of Record (includes final page, issue and volume numbers)

Please check the document version of this publication:

• A submitted manuscript is the version of the article upon submission and before peer-review. There can be important differences between the submitted version and the official published version of record. People interested in the research are advised to contact the author for the final version of the publication, or visit the DOI to the publisher's website.

• The final author version and the galley proof are versions of the publication after peer review.

• The final published version features the final layout of the paper including the volume, issue and page numbers.

Link to publication

## General rights

Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognise and abide by the legal requirements associated with these rights.

• Users may download and print one copy of any publication from the public portal for the purpose of private study or research.

• You may not further distribute the material or use it for any profit-making activity or commercial gain

• You may freely distribute the URL identifying the publication in the public portal.

If the publication is distributed under the terms of Article 25fa of the Dutch Copyright Act, indicated by the “Taverne” license above, please follow below link for the End User Agreement:

www.tue.nl/taverne

## Take down policy

If you believe that this document breaches copyright please contact us at:

openaccess@tue.nl

providing details and we will investigate your claim.

# Deep Unfolding Using Score-based Generative Networks for Automotive Radar Interference Mitigation

Xinyi Wei<sup>1</sup>, Jihwan Youn<sup>3</sup>, Jeroen Overdevest<sup>1,2</sup>, Jun Li<sup>3</sup>, Satish Ravindran<sup>3</sup>, and Ruud J.G. van Sloun

<sup>1</sup>Dept. of Electrical Engineering, Eindhoven University of Technology, The Netherlands <sup>2</sup>NXP Semiconductors, Eindhoven, The Netherlands <sup>3</sup>NXP Semiconductors, San Jose, USA

Abstract—Automotive frequency-modulated continuous wave (FMCW) radars, essential in Advanced Driver Assistance Systems, encounter mutual interference issues that degrade their detection capabilities. Modelbased algorithms, though widely used, rely heavily on predetermined assumptions about the statistical properties. General-purpose black-box deep learning approaches, while effective in their training distribution, often lack flexibility and generalizability in dynamic environments. We introduce a novel hybrid method that combines model-based techniques with deep learning, treating interference mitigation as a source separation problem. Specifically, our method employs score-based deep generative networks to accurately capture the structure of FMCW interference. Additionally, we employ deep unfolding to accelerate inference, critical for automotive radar applications. Empirical results from simulated data demonstrate that the proposed algorithm outperforms the baseline models by 3.26 dB in signal-to-interference-plus-noise ratio in the presence of aggressive interference, and also shows good generalizability with measured data.

Index Terms—score-based deep generative networks, deep unfolding, source separation, interference mitigation, automotive radar

## I. INTRODUCTION

Frequency-modulated continuous wave (FMCW) radars are widely utilized in everyday traffic as an integral component of Advanced Driver Assistance Systems. These radars assess the range, radial velocity, and direction of arrival of objects by analyzing the reflected linear frequency-modulated waves. With the growing use of automotive radars, the likelihood of mutual interference between these systems also increases. This interference can elevate the noise floor, leading to diminished detection capabilities or the creation of unwanted ghost targets [1].

In the realm of FMCW radar interference mitigation, various algorithms are applied at the receiver end for post-signal processing. Conventional methods, like model-based detection and reconstruction, concentrate on identifying samples contaminated by interference and restoring any lost segments of the desired signal [2]–[7]. However, these techniques largely depend on hand-crafted assumptions regarding the statistical characteristics of both the interference and the target signals. On the other hand, deep learning strategies are gaining traction due to their superior signal restoration capabilities. Techniques such as convolutional neural networks (CNNs) and recurrent neural networks (RNNs) are utilized to learn and predict clean signals from interference-contaminated inputs in an end-to-end supervised learning framework [8]–[11]. Despite their effectiveness, the generalizability of these deep learning methods across varying conditions remains a challenge.

In response to these limitations, following up on Wei et al. [12], we here propose to recast the interference mitigation problem as an iterative source separation problem, introducing a novel approach that combines model-based Maximum-a-posteriori (MAP) inference with deep learning techniques. We subsequently unfold these iterations as the layers of a neural network. Specifically, we employ score-

based deep generative networks [13], [14] to learn the complex statistical structure of interference characteristics. This hybrid method effectively capitalizes on the distinct statistical characteristics of both interference and the desired target signals. We then reshape the iterative MAP estimator as a deep network with deep unfolding [15]. By end-to-end training, the unfolded algorithm tailors to the specific task and data distribution, achieving comparable performance with fewer function evaluations than its iterative counterpart. Notably, using the same hardware configuration, the inference time for processing an equivalent number of samples decreased by approximately 76.6%. Moreover, empirical evidence shows that our method improves the signal-to-interference-plus-noise ratio (SINR) in simulated data and enhances detection capabilities in measured data, surpassing baseline methods.

## II. SIGNAL MODEL

The received signal after analog-to-digital conversion can be expressed as follows:

$$
\mathbf { y } = \mathbf { x } _ { \mathrm { t a r } } + \mathbf { x } _ { \mathrm { i n t } } + \mathbf { n } ,\tag{1}
$$

where $\mathbf { y } \in \mathbb { R } ^ { N _ { r } }$ represents the observed time series consisting of $N _ { r }$ fast-time samples, $\mathbf { x } _ { \mathrm { t a r } }$ is the target signal, $\mathbf { x } _ { \mathrm { i n t } }$ is the interference, and n denotes additive Gaussian noise. The challenge lies in accurately estimating $\mathbf { x } _ { \mathrm { t a r } }$ in the presence of interference $\mathbf { x } _ { \mathrm { i n t } } .$ . Without knowledge of the signal structure and statistics of $\mathbf { x } _ { \mathrm { t a r } }$ and $\mathbf { x } _ { \mathrm { i n t } } .$ , this is an illconditioned problem, which we will address via MAP estimation:

$$
\begin{array} { r l } & { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } = \underset { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } } { \arg \operatorname* { m a x } } p \left( \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } | \mathbf { y } \right) } \\ & { \qquad = \underset { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } } { \arg \operatorname* { m a x } } p \left( \mathbf { y } \vert \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } \right) \cdot p \left( \mathbf { x } _ { \mathrm { i n t } } \right) \cdot p \left( \mathbf { x } _ { \mathrm { t a r } } \right) , } \end{array}\tag{2}
$$

where $p ( \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } | \mathbf { y } )$ represents the joint posterior distribution and $p ( \mathbf { y } | \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } )$ is the measurement likelihood model. In our framework, the prior for the target signal, $p ( \mathbf { x } _ { \mathrm { t a r } } )$ , is modeled as a Laplace distribution in the range spectrum, assuming sparsity. Additionally, FMCW interference is characterized as chirp signals in the fasttime domain [9] and is better structured in the time-frequency domain [2]. Building on this, we propose modeling the interference prior in the time-frequency domain using a score-based generative network. These priors are then used in a proximal gradient-based MAP optimizer, which guides the reconstructions of the interference and target signal. We thus rewrite (2) as:

$$
\begin{array} { r } { \hat { \mathbf { x } } _ { \mathrm { t a r } } , \hat { \mathbf { x } } _ { \mathrm { i n t } } = \underset { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } } { \arg \operatorname* { m i n } } ~ \| \mathbf { y } - \mathbf { x } _ { \mathrm { t a r } } - \mathbf { x } _ { \mathrm { i n t } } \| _ { 2 } ^ { 2 } } \\ { -  \lambda _ { \mathrm { i n t } } \log p ( \mathbf { S } ( \mathbf { x } _ { \mathrm { i n t } } ) ) + \lambda _ { \mathrm { t a r } } \| \mathbf { F } \mathbf { x } _ { \mathrm { t a r } } \| _ { 1 } , } \end{array}\tag{3}
$$

where $\mathbf { F } \in \mathbb { C } ^ { N _ { r } \times N _ { r } }$ represents the Fourier transform matrix, while $\mathbf S ( \cdot ) \ : \ \mathbb R ^ { N _ { r } } \ \to \ \mathbb C ^ { F _ { s } \times \hat { T } _ { s } }$ denotes the short-time Fourier transform (STFT). Here, $F _ { s }$ specifies the number of frequency bins, and $T _ { s }$ specifies the number of time bins in the spectrograms. The terms $\lambda _ { \mathrm { i n t } }$ and $\lambda _ { \mathrm { t a r } }$ are introduced as regularization factors. Finally, we subtract the recovered interference from the observation to obtain the estimation of the target signals, ensuring the preservation of any potential weak signals.

![](images/f4c64f9a90d494929a91bbe24747d6a87ba62fb783a51dfae6c6d7b866211402.jpg)  
Fig. 1: Architecture of the proposed algorithm. At each iteration, the prior update step guides the interference estimation into a higher likelihood region within the time-frequency domain using a learned score-based network. Concurrently, target signal updates are obtained by enforcing sparsity in the range spectrum using a proximal step (soft-thresholding). Finally, a data consistency step yields refined estimations, which then feed into the next iteration.

## A. Score-based Generative Networks

We propose the use of score-based generative networks [13], [14] to model the interference prior. Unlike many other generative networks that directly model the log-probability of the data, log $p _ { \mathrm { d a t a } } ( \mathbf { x } )$ , score-based generative networks model the gradient of the log-probability distribution of the data samples. This gradient, s<sub>θ</sub> $\approx \nabla _ { \mathbf { x } } \log p _ { \mathrm { d a t a } } ( \mathbf { x } )$ , is referred to as the score function, with θ representing the learnable parameters. This provides more flexibility in the network architecture design compared to other generative networks, such as normalizing flows [16], where architectural constraints are imposed to ensure proper normalized distributions. The process of generating samples from the learned distribution involves iterative gradient-based approaches, including Langevin dynamics [13]. We will elaborate on the training of the score function in Section III-B. In the following, we assume that we have access to a trained score function $\mathbf { s } _ { \pmb { \theta } } ( \mathbf { x } ) \approx \nabla _ { \mathbf { x } } \log p _ { \mathrm { d a t a } } ( \mathbf { x } )$

## B. Iterative MAP Estimation for Source Separation

We design an iterative algorithm to solve (3). This algorithm alternates between prior updates and data consistency steps. Let $\mathbf { C } _ { \mathrm { i n t } } \in \mathbb { C } ^ { F _ { s } \times T _ { s } }$ represent the complex time-frequency representation of interference. At the $k ^ { \mathrm { { t h } } }$ iteration, the current complex timefrequency estimation of the interference, $\tilde { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } ,$ is obtained by moving the previous estimate, $\hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 }$ , towards the expected statistical features. This adjustment is guided by the learned score-based generative network, $\mathbf { s } _ { \pmb { \theta } }$ , which functions as a gradient vector field. Consequently, this process steers the estimate towards high-likelihood regions of the data distribution, yielding a plausible interference representation. The formulation of this update is as follows:

$$
\begin{array} { r } { \tilde { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } = \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 } + \lambda _ { \mathrm { i n t } } ^ { k } \mathbf { s } _ { \theta } \left( \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 } \right) , } \end{array}\tag{4}
$$

where ${ \lambda } _ { \mathrm { i n t } } ^ { k }$ specifies the step size taken in the gradient ascent process for the $k ^ { \mathrm { { t h } } }$ iteration.

Similarly, let $\mathbf { c } _ { \mathrm { t a r } } \in \mathbb { C } ^ { N _ { r } }$ represent the sparse coefficients corresponding to the target signal in the range spectrum. The estimated target signal is updated through a proximal step, employing softthresholding in the range spectrum. This update is mathematically expressed as:

$$
\tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } = \Gamma _ { \lambda _ { \mathrm { t a r } } } \left( \hat { \mathbf { c } } _ { \mathrm { t a r } } ^ { k - 1 } \right) = \mathrm { s i g n } ( \tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } ) \cdot \mathrm { m a x } \left( 0 , | \tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } | - \lambda _ { \mathrm { t a r } } \right) ,\tag{5}
$$

where $\Gamma _ { \lambda _ { \mathrm { t a r } } }$ represents the soft-thresholding operation [17]. The sign function retains the original sign of the signal, while max $\left( 0 , | \tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } | - \lambda _ { \mathrm { t a r } } \right)$ sets values below $\lambda _ { \mathrm { t a r } }$ to 0, effectively controlling the sparsity of the target signal in the range spectrum.

Subsequently, we convert the interference estimation, $\tilde { \mathbf { C } } _ { \mathrm { i n t } } ^ { k }$ , and the target signal estimation, $\tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } ,$ , back to their respective time domain presentations, which are $\tilde { \mathbf { x } } _ { \mathrm { i n t } } ^ { k }$ and $\tilde { \mathbf { x } } _ { \mathrm { t a r } } ^ { k }$ , respectively. The transformation involves applying the inverse STFT operation, denoted as $\mathbf S ^ { - 1 } ( \cdot ) : \mathbb { C } ^ { F _ { s } \times T _ { s } } \xrightarrow { \sim } \tilde { \mathbb { R } } ^ { N _ { \tau } }$ , to the interference, and the inverse Fourier transform matrix, denoted as $\mathbf { F } ^ { - 1 } \in \mathbb { C } ^ { N _ { r } \times N _ { r } }$ , to the target signal. We then perform data consistency steps in the time domain, detailed in the equations below:

$$
\hat { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } = \mathbf { S } ^ { - 1 } \left( \tilde { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } \right) - \mu _ { \mathrm { i n t } } \left( \mathbf { F } ^ { - 1 } \tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } + \mathbf { S } ^ { - 1 } \left( \tilde { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } \right) - \mathbf { y } \right) ,\tag{6}
$$

$$
\hat { \mathbf { x } } _ { \mathrm { t a r } } ^ { k } = \mathbf { F } ^ { - 1 } \tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } - \mu _ { \mathrm { t a r } } \left( \mathbf { F } ^ { - 1 } \tilde { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } + \hat { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } - \mathbf { y } \right) .\tag{7}
$$

The parameters $\mu _ { \mathrm { t a r } }$ and $\mu _ { \mathrm { i n t } }$ are used to tune the data consistency levels, determining how much the estimations should adhere to the observation. For the next iteration, we start by transforming the estimates from the time domain to their respective domains: $\hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } = \mathbf { S } \left( \hat { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } \right)$ and $\hat { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } = \mathbf { F } \hat { \mathbf { x } } _ { \mathrm { t a r } } ^ { k }$ . After the algorithm converges, we obtain the final estimated time series target signal, $\hat { \mathbf { x } } _ { \mathrm { t a r } }$ , which is obtained by subtracting the estimated time series interference $\hat { \bf x } _ { \mathrm { i n t } }$ from the observation y. An overview of the proposed algorithm is given in Fig.1.

## C. Deep Unfolding of Iterative MAP Estimation

To minimize the number of function evaluations, we unfold the iterative algorithm into a neural network composed of a fixed number of layers [15]. Each layer i consists of independent trainable parameters, meaning that the parameters are unique to each layer and not shared with others. These include data consistency coefficients $\mu _ { \mathrm { t a t } } ^ { i }$ and $\mu _ { \mathrm { i n t } } ^ { i } ,$ as well as prior update coefficients $\lambda _ { \mathrm { t a r } } ^ { i }$ and $\lambda _ { \mathrm { i n t } } ^ { i }$ . Importantly, during the training of the unfolded algorithm, the weights of the score network are fixed to ensure consistent prior updates of interference, thereby preserving its fidelity and reflecting established prior knowledge.

![](images/51e5da1b90d0c60071084069e9d72286f19f374216daf9de127351620ccfa7d4.jpg)  
Fig. 2: Description of the experimental setup. The left figure illustrates radar sensors mounted on the front of an ego-car, facing forward. The right figure shows the measurement scene where four interference sources are present.

## III. TRAINING AND VALIDATION

## A. Simulated and Measured Dataset

The algorithm is trained and evaluated using a dynamically generated simulated dataset. Observations within this dataset feature a randomly varied number of targets, from 1 to 10, each with a signalto-noise ratio (SNR) between −15 and 15 dB. Additionally, each observation includes a single interference source with an interferenceto-noise ratio (INR) that also randomly varies between −15 and 15 dB. The interference configurations, such as chirp slope and chirp duration, are randomly configured to ensure a diverse spectrum of interference scenarios is covered.

To validate the algorithm’s effectiveness in real-world scenarios, its performance is also evaluated using data collected from a static measurement scene. Radar sensors are mounted on an ego-car facing forward, and the measurement setup includes four interference sources positioned at various distances, each with a unique chirp configuration. For an overview of the measurement setting, see Fig. 2. Detailed descriptions of the measurement scene and chirp configurations can be found in [18].

## B. Network Architecture and Training Strategy

The training involves two principal training steps. The first step aims to learn the interference score function in the STFT domain. For this, we adopt the architecture proposed by Song et al. [13], which is based on RefineNet framework [19]. Originally developed for high-resolution semantic image segmentation, RefineNet excels at integrating multi-scale contextual information. The employment of residual convolution units in RefineNet is particularly advantageous for tasks demanding accurate signal structure capture.

The training utilizes simulated fast-time data containing only a single source of interference. The data undergoes STFT to obtain its time-frequency representation. The resulting $\mathbf { C } _ { \mathrm { i n t } }$ with $F _ { s } = 6 6$ and $T _ { s } ~ = 6 6$ is obtained after zero-padding to the desired dimensions, after which we stack the real and imaginary components into two channels. The network parameters are optimized using denoising score matching [20], which can be formulated as follows:

$$
\frac { 1 } { 2 L } \sum _ { m = 1 } ^ { L } \mathbb { E } _ { p _ { \mathrm { d a t a } } ( \mathbf { C } _ { \mathrm { i n t } } ) } \mathbb { E } _ { p _ { \sigma _ { m } } \left( \mathbf { C } _ { \mathrm { i n t } } ^ { \prime } \Big \vert \mathbf { C } _ { \mathrm { i n t } } \right) } \left[ \left. \mathbf { s } _ { \theta } ( \mathbf { C } _ { \mathrm { i n t } } ^ { \prime } ) + \frac { \mathbf { C } _ { \mathrm { i n t } } ^ { \prime } - \mathbf { C } _ { \mathrm { i n t } } } { \sigma _ { m } } \right. _ { 2 } ^ { 2 } \right] ,\tag{8}
$$

where $\mathbf { C } _ { \mathrm { i n t } }$ are perturbed with additive Gaussian noise, resulting in the generation of perturbed counterparts, $\mathbf { C } _ { \mathrm { i n t } } ^ { \prime }$ . The noise level, denoted by $\sigma _ { m }$ , is uniformly selected from 232 geometrically spaced values ranging from 0.01 to 50. This training objective is to minimize the empirical average of the Euclidean distance between the score functions of the training samples and all the perturbations.

Subsequently, we integrate the learned score network into each layer of the unfolded algorithm, with its weights fixed, as described in Section II-C. The unfolded network is then trained end-to-end using mean squared error (MSE) as the loss function, which measures the discrepancy in the time domain between the ground truth target signals, $\mathbf { x } _ { \mathrm { t a r } }$ , and the estimations, $\hat { \mathbf { x } } _ { \mathrm { t a r } }$ . The MSE formulation can be expressed as follows:

$$
\mathbf { M S E } = \mathbb { E } \left[ \left( \mathbf { x } _ { \mathrm { t a r } } - \hat { \mathbf { x } } _ { \mathrm { t a r } } \right) ^ { 2 } \right] = \frac { 1 } { K } \sum _ { i = 1 } ^ { K } \left( \mathbf { x } _ { \mathrm { t a r } } - \hat { \mathbf { x } } _ { \mathrm { t a r } } \right) ^ { 2 } .\tag{9}
$$

Utilizing K training samples and the Adam optimizer [21], the learning rate is initialized at 0.01 for $\mu _ { \mathrm { t a r } } , \mu _ { \mathrm { i n t } } .$ , and $\lambda _ { \mathrm { t a r } } .$ However, for λ<sub>int</sub>, each layer’s learning rate adjusts uniquely. Specifically, the rate for the $i ^ { \mathrm { { t h } } }$ layer, which ranges from 1 to l—the total number of layers for deep unfolding, follows: $l r _ { i } = 0 . 1 \times \left( 0 . 0 0 1 / 0 . 1 \right) ^ { ( i - 1 ) / ( l - 1 ) }$ . This configuration starts at 0.1 for the first layer and decays exponentially to 0.001 for the last, allowing broader exploration within the search space for the initial layers. The training automatically terminates if the validation loss, assessed with validation samples, fails to decrease over five consecutive epochs.

## C. Baselines

We evaluate our algorithm against competitive baselines designed to mitigate interference within single chirp transmissions for low latency requirements in real-time automotive radar applications.

The first two baselines adhere to the model-based interference detection and cancellation method, which replaces removed signal samples with zeros. We selected two distinct implementations for comparison: one operating in the time domain, named Time-Z, and another in the magnitude time-frequency domain, named Spec-Z.

The third baseline, termed CNN, is trained in a fully supervised learning framework using MSE as the loss criterion. The training process involves mapping interference-contaminated complex timefrequency representations to their interference-only counterparts. Following this, the estimation of the target signal is then obtained by subtracting the interference estimation from the observation in the time domain. For the purpose of ensuring a fair comparison, it employs the same network architecture as the score-based generative network described in Section III-B.

The fourth baseline, SALSA, is described in [5]. It assumes that the target signal and interference exhibit sparsity within the range spectrum and time-frequency domain, respectively.

The final baseline addresses (3) using a conventional iterative approach [12]. The primary distinction between this algorithm and the proposed method lies in the treatment of parameters associated with prior updates and data consistency steps. In the iterative algorithm, these parameters are shared throughout all iterations and are optimized through hyperparameter tuning on a subset of validation data. Specifically, Bayesian optimization [22] is employed to minimize MSE between the estimation and ground-truth target signal in the time domain.

## IV. RESULTS AND DISCUSSIONS

## A. Evaluation on simulated data

We first evaluate the proposed algorithm by comparing it against the baselines using simulated test datasets across various scenarios. Each test scenario is characterized by a specific range of INRs and includes 512 test data. We calculate SINR within the magnitude range spectrum to assess the target’s range. Fig. 3 illustrates the performance of the proposed deep unfolded algorithm in comparison to various baselines. While it does not surpass its iterative counterpart at 140 iterations in terms of SINR, the deep unfolded algorithm exhibits substantially improved computational efficiency. It surpasses all other baselines with merely 25 layers, marking a significant reduction in the number of function evaluations required. The effectiveness of the proposed algorithm in mitigating interference highlights its principal advantage, which stems from its precise description of the statistical characteristics of interference. Furthermore, a comparison with its iterative counterpart—depicted by the dashed line—using an equivalent number of function evaluations illustrates the advantages of the deep unfolding optimization scheme.

![](images/05f405a57d27e2638066df4026c6b56be24fed449e39b74f9b3b140ab03d8f13.jpg)  
Fig. 3: SINR comparison between the proposed method and the baselines. Unfolding25 refers to the proposed unfolded algorithm with 25 layers, while Iterative25 and Iterative140 represent the iterative versions, detailing the required iterations for convergence.

![](images/8d9aac9493d30258ca2bfbbdca2c54fe2ded670b64c826612cdbe0f6186fabf1.jpg)  
Fig. 4: Detection performance comparison on the RD map of the baselines with the proposed method using measured data consisting of 256, 000 chirps.

## B. Evaluation on measured data

We compare our proposed algorithm with baselines using realworld data collected through in-house radar sensors. The test scenarios feature static scenes where each chirp may be contaminated by up to four uniquely configured interferences. We evaluate detection performance using range-Doppler (RD) maps, which allow for the assessment of both target range and radial velocity. Following the method outlined in [23], we evaluate detection performance on the RD map using estimations of the probability density functions (PDFs) for both target signals and background. These PDFs then enable the computation of probability of detection, P<sub>D</sub>, for any given probability of false alarm, P<sub>FA</sub>, which form the receiver operating characteristic curve, as shown in Fig. 4. Importantly, we finetuned the proposed algorithm and the baselines using a single paired set of interference-contaminated and interference-free data. The interference prior, learned from simulated data featuring a single source of interference, is applied directly. As shown in Fig. 4, both the proposed algorithm and its iterative counterpart exhibit good generalizability, a critical aspect often challenging for deep-learning-based algorithms. Our method significantly benefits from the learned interference prior knowledge embedded within the algorithm. Moreover, this capability underscores the practical value in scenarios where the exact configurations of interferences, such as their number, are unknown. In contrast, as can be seen in Fig. 5, while the fully supervised deep CNN performs well on simulated data, its performance degrades significantly when applied to real data.

## V. CONCLUSIONS

We have demonstrated the effectiveness of score-based generative networks combined with a MAP estimator, utilizing deep unfolding as an optimization technique in mitigating FMCW radar interference. The applicability of our method extends beyond FMCW radars and can be adapted to various source separation problems, especially where the signal exhibits structured characteristics in a specific domain.

## ACKNOWLEDGEMENT

This work was funded by the RAISE collaboration framework between Eindhoven University of Technology and NXP, including a PPS-supplement from the Dutch Ministry of Economic Affairs and Climate Policy.

![](images/8ff205cf2d6c3ad09fc05f2c0350d4fa7127e0a1486c515f9e039e6bdf4ef3f0.jpg)  
(a) RD map displays interference-contaminated scenarios.

![](images/60d3d5aeeec9509e87ee33cf72f755c7eea58ba73952887396391ad6792fc59a.jpg)  
(b) RD map post-CNN interference mitigation.

![](images/25ba8c475d84c7428b477f0677c0b0de6b3dca1e6e8491e6e3da1f11daf8806a.jpg)  
(c) RD map post-proposed algorithm interference mitigation.  
Fig. 5: Example of RD maps before and after interference mitigation using the CNN and the proposed algorithm.

[1] M. Goppelt, H.-L. Blocher, and W. Menzel, “Analytical investigation of¨ mutual interference between automotive FMCW radar sensors,” in 2011 German Microwave Conference, 2011, pp. 1–4.

[2] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the stft domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, 2019.

[3] F. Laghezza, F. Jansen, and J. Overdevest, “Enhanced interference detection method in automotive FMCW radar systems,” in 2019 20th International Radar Symposium (IRS), 2019, pp. 1–7.

[4] R. H. Wu, J. Li, M. Brett, and M. A. Staudenmaier, “Radar communication with interference suppression,” Nov. 3 2022, uS Patent App. 17/245,613.

[5] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[6] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank hankel matrix decomposition,” IEEE Transactions on Signal Processing, vol. 70, pp. 822–834, 2022.

[7] J. Li, J. Youn, R. Wu, J. Overdevest, and S. Sun, “Performance evaluation and analysis of thresholding-based interference mitigation for automotive radar systems,” arXiv preprint arXiv:2402.14018, 2024.

[8] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with self attention,” in ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 3802–3806.

[9] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR), 2020, pp. 315–320.

[10] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153 491–153 507, 2021.

[11] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Complexvalued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in 2021 IEEE Radar Conference (RadarConf21). IEEE, 2021, pp. 1–6.

[12] X. Wei, J. Overdevest, J. Li, J. Youn, S. Ravindran, and R. J. Van Sloun, “Score-based generative modeling for interference mitigation in automotive fmcw radar,” in 2024 21st European Radar Conference (EuRAD). IEEE, 2024, pp. 27–30.

[13] Y. Song and S. Ermon, “Improved techniques for training score-based generative models,” in Advances in Neural Information Processing Systems 33. NeurIPS 2020, 2020.

[14] Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole, “Score-based generative modeling through stochastic differential equations.” ICLR 2021, 2021.

[15] V. Monga, Y. Li, and Y. C. Eldar, “Algorithm unrolling: Interpretable, efficient deep learning for signal and image processing,” IEEE Signal Processing Magazine, vol. 38, no. 2, pp. 18–44, 2021.

[16] I. Kobyzev, S. J. Prince, and M. A. Brubaker, “Normalizing flows: An introduction and review of current methods,” IEEE transactions on pattern analysis and machine intelligence, vol. 43, no. 11, pp. 3964– 3979, 2020.

[17] D. Donoho, “De-noising by soft-thresholding,” IEEE Transactions on Information Theory, vol. 41, no. 3, pp. 613–627, 1995.

[18] J. Overdevest, A. G. C. Koppelaar, J. Youn, X. Wei, and R. J. G. v. Sloun, “Neurally augmented deep unfolding for automotive radar interference mitigation,” IEEE Transactions on Radar Systems, vol. 2, pp. 712–724, 2024.

[19] G. Lin, A. Milan, C. Shen, and I. Reid, “Refinenet: Multi-path refinement networks for high-resolution semantic segmentation,” 2016. [Online]. Available: https://arxiv.org/abs/1611.06612

[20] P. Vincent, “A connection between score matching and denoising Autoencoders,” in Neural computation, vol. 23, 2011.

[21] D. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in International Conference on Learning Representations (ICLR), San Diega, CA, USA, 2015.

[22] E. Bakshy, L. Dworkin, B. Karrer, K. Kashin, B. Letham, A. Murthy, and S. Singh, “AE: A domain-agnostic platform for adaptive experimentation,” in Conference on neural information processing systems, 2018, pp. 1–8.

[23] J. Youn, J. Li, R. Wu, and J. Overdevest, “Interference mitigation evaluation methodology for automotive radar,” in 2024 21st European Radar Conference (EuRAD). IEEE, 2024, pp. 115–118.