# Human Tracking with mmWave Radars: a Deep Learning Approach with Uncertainty Estimation

Jacopo Pegoraro<sup>‡</sup> (Graudate Student Member, IEEE) and Michele Rossi (Senior Member, IEEE)

Abstract—mmWave radars have recently gathered significant attention as a means to track human movement within indoor environments. Widely adopted Kalman filter tracking methods experience performance degradation when the underlying movement is highly non-linear or presents long-term temporal dependencies. As a solution, in this article we design a convolutional-recurrent Neural Network (NN) that learns to accurately estimate the position and the velocity of the monitored subjects from high dimensional radar data. The NN is trained as a probabilistic model, utilizing a Gaussian negative log-likelihood loss function, obtaining explicit uncertainty estimates at its output, in the form of time-varying error covariance matrices. A thorough experimental assessment is conducted using a 77 GHz FMCW radar. The proposed architecture, besides allowing one to gauge the uncertainty in the tracking process, also leads to greatly improved performance against the best approaches from the literature, i.e., Kalman filtering, lowering the average error against the ground truth from 32.8 to 7.59 cm and from 56.8 to 14 cm/s in terms of position and velocity tracking, respectively.

Index Terms—uncertainty estimation, mmWave radar, human tracking, recurrent neural networks, indoor sensing

## I. INTRODUCTION

NDOOR human tracking with low power millimeter-wave (mmWave) radar sensors has been receiving considerable attention in the last few years, due to its wide applicability to the Internet of Things (IoT) [1]. The typical aim of these systems is to exploit the reflected signal from human subjects to infer their state in the physical space, e.g., their position and movement speed [2]–[5].

In this paper, we address the limitations of widely used Bayesian tracking techniques, such as the extended Kalman filter (EKF), which require strong assumptions about the movement process, e.g., constant velocity. Despite being widely used in the literature [3]–[5], these methods only work sufficiently well in practice because of the high frame rates of mmWave radar devices, but their capability of grasping the complexity of human movement is severely limited. In real environments, people often follow random and unpredictable trajectories, which do not match standard radar target movement models. This causes large predicted uncertainties when using model-based Bayesian filtering approaches, reflecting the intrinsic limitations of legacy models in human movement analysis. To resolve this, we advocate the use of a model-free and end-to-end deep learning approach. In addition, and to the best of our knowledge, we are the first to introduce to the radar field the concept of heteroscedastic, i.e., samplevarying, uncertainty estimation for neural network (NN) architectures. Modeling the uncertainty in the state estimates allows obtaining an error covariance matrix associated with the NN predictions: recently, this has been successfully applied to computer vision problems [6]. Note that such covariances are most valuable in indoor radar systems to increase the performance of processing blocks such as data association, in the case of (i) multiple subjects being tracked concurrently, or (ii) multiple radars with overlapping fields of view. The contributions of our work are:

1) We design a maximum-likelihood convolutional-recurrent neural network (ML-CRNN), based on gated recurrent units (GRU) [7]. This NN outputs an estimate of the current subject state (position and velocity) given an arbitrarily long sequence of past radar observations, without making any assumptions on the underlying movement process. The ML-CRNN handles both the vision part of the problem, processing the raw data, and the non-linear target tracking part.

2) The proposed ML-CRNN outputs an heteroscedastic error covariance matrix paired with each state prediction, which weighs the confidence level of the state estimates. This is achieved by making the NN output the error covariance matrix of the state estimate, and training it as a probabilistic model via a Gaussian negative log-likelihood (NLL) loss function.

3) We design ML-CRNN for end-to-end training (no preprocessing). While in the literature denoising and clustering phases are customary, [2], [3], [5], ML-CRNN sequentially processes raw range-Doppler/range-azimuth radar images.

Numerical results are obtained on our own experimental data, using a Frequency Modulated Continuous Wave (FMCW) INRAS RadarLog device working in the 77−81 GHz band. The evaluation scenario is challenging and realistic, with furniture and other humans, in addition to the tracked subject.

## II. FMCW MMWAVE RADAR SIGNAL MODEL

A multiple-input multiple-output (MIMO) FMCW radar allows the joint estimation of the distance, the angular position and the radial velocity of the target(s) with respect to the radar device. To achieve this, the radar transmits sequences of chirp signals and measures the frequency shift of the reflection at its receiving antennas. Next, we provide a brief overview of the FMCW radar signal model, detailing the parameters that are used in this work. For a more comprehensive description, the reader may refer to [8], [9].

We use an INRAS RadarLog FMCW radar with one transmitting antenna and $\Gamma = 1 6$ receiving antennas, organized as a linear array. The frequency of the transmitted chirp signal (TX) is linearly increased from a base value of $f _ { o } = 7 7$ GHz to a maximum $f _ { 1 } = 8 1$ GHz in $T _ { c } = 1 8 0 ~ \mu \mathrm { s }$ (a sweep). We define the bandwidth of the chirp as $B = f _ { 1 } - f _ { o } = 4$ GHz. The chirps are transmitted every $T _ { \mathrm { r e p } } = 2 5 0 ~ \mu \mathrm { s }$ in sequences of $P = 2 5 6$ sweeps. For each of the 16 antenna elements, a mixer combines the attenuated and delayed received signal (RX) with the transmitted one, generating the intermediate frequency (IF) signal. The IF signal is sampled along three different dimensions. First, fast time sampling returns $N = 1 0 2 4$ points from each chirp. For the slow time (or Doppler) sampling, $P$ samples, one per chirp from adjacent chirps, are taken with period $T _ { \mathrm { r e p } } .$ . Finally, the spatial sampling relates to the Γ receiving channels, spaced apart by a distance $d ,$ and enables the localization of the targets in the physical space. A discrete Fourier transform (DFT) is applied along each sampling dimension and the square of its magnitude is computed to extract the power density for each frequency component. The resulting 3-dimensional signal is referred to as range-Doppler-azimuth (RDA) map, and the position of the power peaks along each axis can be associated with the radial distance, the angular position and the radial velocity of the subjects [8]. The RDA maps are outputted by the radar at every time-step, with a rate of 15 fps, and have a dimension of 1024 × 64 × 64 points, due to the resolution used for the DFT along the fast time, angular and slow time dimensions respectively.

## III. METHOD

We define the state of a human subject at a certain time-step t as the vector $\mathbf { x } _ { t } = \left[ x _ { t } , y _ { t } , v _ { t } ^ { x } , v _ { t } ^ { y } \right] ^ { T } \in \mathbb { R } ^ { 4 }$ , containing the Cartesian coordinates of the subject in the space, $x _ { t }$ and y<sub>t</sub>, and the velocity components $\boldsymbol { v } _ { t } ^ { x }$ and $v _ { t } ^ { y } .$ Our aim is to track the subject, namely, to sequentially estimate their current state across time, using a sequence of past and present observations of the system (filtering problem). To this end, we design a recurrent NN that extracts information from a sequence of T consecutive radar RDA maps, identified by index $t = 1 , \dots , T$ , and that performs a regression task producing an estimate of the state, $\hat { \mathbf { x } } _ { t } .$ . In contrast to typical regression approaches based on NNs, we wish to estimate not only the state of the subject, but also the corresponding error covariance, $\begin{array} { r } { \Sigma _ { t } = E \left\lceil \left( \mathbf { x } _ { t } - \hat { \mathbf { x } } _ { t } \right) \left( \mathbf { x } _ { t } - \hat { \mathbf { x } } _ { t } \right) ^ { T } \right\rceil } \end{array}$

## A. Learning from raw data

Processing the raw RDA maps from the radar can be computationally very expensive given their size. To mitigate this, we first select only the range interval of interest from the fast time dimension, i.e., the first 134 points, that correspond to distances from 0 to 5 m. The resulting $1 3 4 \times 6 4 \times 6 4$ 1 RDA map is then projected onto the range-Doppler (RD) plane by integrating along the azimuth dimension and onto the range-azimuth (RA) plane by integrating along the Doppler dimension. In this way, at each time-step t we obtain a pair of $1 3 4 \times 6 4$ images, denoted by ${ \bf M } _ { t } ^ { \mathrm { R D } }$ and ${ \bf M } _ { t } ^ { \mathrm { R A } }$ , see Fig. 1. Images are normalized so that pixels intensities lie in the interval [0, 1].

![](images/5f0952294f2287127c82829b725cc4affc8d4f0decba448213728e55b9d24779.jpg)

![](images/dd941d8cbd251696ed7042c99aaa3c5371e48fdb468b3fa828d24ced4eb57015.jpg)  
(a) RD image, M<sup>RD</sup>.  
(b) RA image, $\mathbf { M } _ { t } ^ { \mathrm { R A } }$  
Fig. 1: Example RD and RA images. The target corresponds to the peak in received power around 2 m.

## B. Proposed neural network architecture

The proposed ML-CRNN combines convolutional layers operating on the single time-step with a recurrent structure based on GRU layers [7], as shown in Fig. 2. We can identify a convolutional and a recurrent block, which are connected together forming the ML-CRNN model and which are trained jointly via a common loss function (see Section III-C).

The convolutional block is a convolutional neural network (CNN) that takes as input two images per time step, namely the RD and RA projections of the RDA map, $\mathbf { M } _ { t } ^ { \mathrm { R D } } \in \left[ 0 , 1 \right] ^ { 1 3 \mathbf { \breve { 4 } } \times 6 4 }$ and $\mathbf { M } _ { t } ^ { \mathrm { R A } } \in \mathsf { \bar { [ 0 , 1 ] } } ^ { 1 3 4 \times 6 4 }$ . Given this input, the CNN learns a non-linear composite function C that maps $\mathbf { M } _ { t } ^ { \mathrm { R D } }$ and $\mathbf { M } _ { t } ^ { \mathrm { R A } }$ onto a vector ${ \bf o } _ { t } \in \mathbb { R } ^ { 1 6 }$ , called compressed observation. The function is based on two parallel network branches that extract features from each input image separately, and that are then combined into a single output. Each branch, denoted by $i \in \{ \mathrm { R D } , \mathrm { R A } \}$ , is the composition of L functions, which are the layers of the CNN, $f _ { L } ^ { i } \left( \ldots { } f _ { 1 } ^ { i } \left( \mathbf { M } _ { t } ^ { i } \right) \right)$ , with $L = 4 .$ . Each layer ℓ computes the elementwise ELU activation function [10] of the sum between the convolution of the input X with $d _ { \ell } ~ 3 \times 3$ learned kernels, $\mathbf { K } _ { \ell } ^ { i }$ , and a bias parameter $b _ { \ell } ^ { i } \colon f _ { \ell } ^ { i } \left( X \right) = \mathrm { E L U } \left( \mathbf { K } _ { \ell } ^ { i } \ast X + b _ { \ell } ^ { i } \right)$ . The term $d _ { \ell }$ represents the number of feature maps of each layer and is equal to 4, 8, 16, 4 for layer $\ell = 1 , 2 , 3 , 4$ , respectively. The kernels are applied using stride $2 \times 2$ , that means they are shifted by two positions at each step of the convolution, resulting in a dimensionality reduction of a factor 2 at each layer<sup>1</sup>. The output of each branch, is reshaped into a vector $\mathbf { y } _ { t } ^ { i } .$ , and the two outputs are concatenated into $\mathbf { y } _ { t }$ . The final layer of the convolutional block processes $\mathbf { y } _ { t }$ using a fully connected (FC) layer with dropout probability $p \ = \ 0 . 3 3 .$ Dropout refers to randomly setting to 0 the output of some NN nodes during training as a regularization method [11]. The FC layer applies the function $\mathbf { o } _ { t } = \mathrm { E L U } \left( \mathbf { W } _ { \mathrm { f c } } \mathbf { y } _ { t } + \mathbf { b } _ { \mathrm { f c } } \right)$ , with parameters $\mathbf { W } _ { \mathrm { f c } } , \mathbf { b } _ { \mathrm { f c } }$ Input radar images are processed in sequences of T frames, applying in parallel the CNN block to each pair of RD and RA <sub>1</sub>maps and obtaining a sequence of compressed observations, denoted by $\mathbf { o } _ { 1 : T }$

![](images/96209a865439a23ad78e17796006f6d8e2f93e057a71d3c0ce649292dbeece8c.jpg)  
Fig. 2: Block diagram of the ML-CRNN architecture.

The recurrent block is a recurrent layer featuring GRU cells [7]. GRU cells maintain a hidden state across time-steps, processing it together with the current input vector to learn temporal dependencies in the input sequence (see [7] for the detailed description of a GRU cell). The recurrent block takes as input $\mathbf { o } _ { 1 : T }$ and outputs a sequence of estimates of the unobservable target states $\hat { \mathbf { x } } _ { 1 : T }$ and the corresponding error covariance matrices $\hat { \Sigma } _ { 1 : T }$ . The hidden states are denoted by $\mathbf { h } _ { 1 : T }$ and have dimension 128 each. At each time-step, they are further processed with 3 FC output layers to compute the state estimate, $\hat { \mathbf { x } } _ { t } \in \mathbb { R } ^ { 4 }$ , and two vectors $\pmb { \alpha } _ { t } \in \mathbb { R } _ { + } ^ { 4 }$ and $\beta _ { t } \in \mathbb { R } ^ { 6 }$ which are used to build the covariance matrix estimate $\hat { \mathbf { \boldsymbol { \Sigma } } } _ { t } .$ , as described in Section III-C. The expressions of the FC layers are the following

$$
\hat { \mathbf { x } } _ { t } = \mathbf { W } _ { x } \mathbf { h } _ { t } + \mathbf { b } _ { x } ,\tag{1}
$$

$$
\alpha _ { t } = \exp \left( \mathbf { W } _ { \alpha } \mathbf { h } _ { t } + \mathbf { b } _ { \alpha } \right) ,\tag{2}
$$

$$
\beta _ { t } = \operatorname { t a n h } \left( \mathbf { W } _ { \beta } \mathbf { h } _ { t } + \mathbf { b } _ { \beta } \right) ,\tag{3}
$$

where we denoted by $\mathbf { W } _ { x } , \mathbf { b } _ { x } , \mathbf { W } _ { \alpha } , \mathbf { b } _ { \alpha } , \mathbf { W } _ { \beta } , \mathbf { b } _ { \beta }$ the learned weights and biases. In the recurrent block, recurrent dropout is applied with probability $p = 0 . 3 3$ as described in [12]. The ML-CRNN contains a total of 66730 trainable parameters.

## C. Maximum likelihood state and covariance estimation

To model the uncertainty on the state estimates, we assume that the posterior distribution of the state given the observation sequence of length $T$ is Gaussian with mean $\hat { \mathbf { x } } _ { t } \mathrm { : }$ $p ( \mathbf { x } _ { t } | \mathbf { M } _ { 1 : T } ^ { \mathrm { R D } } , \mathbf { M } _ { 1 : T } ^ { \mathrm { R A } } ) \sim \mathcal { N } ( \hat { \mathbf { x } } _ { t } , \mathbf { \bar { \Delta } } _ { t } )$ . Moreover, we let $\hat { \Sigma } _ { t }$ depend on the time-step, in order to reflect the variable uncertainty that affects radar measurements due to many factors, like the range-dependent power attenuation, the clutter distribution and the variability in the movement process.

The covariance matrix Σ<sub>t</sub> must be symmetric and positive definite, and can be modeled as the sum of an aleatoric and an epistemic component [6], [13], as detailed next.

1) Aleatoric covariance, Σ<sup>a</sup>, is the uncertainty related to the intrinsic noise in the state evolution and measurement processes. It is estimated directly from the vectors $\alpha _ { t } , \beta _ { t }$ outputted by the ML-CRNN, see Eq. (2) and Eq. (3), using the Cholesky decomposition $\begin{array} { r } { \hat { \mathbf { \Sigma } } _ { t } ^ { a } = \mathbf { L } _ { t } \mathbf { L } _ { t } ^ { T } } \end{array}$ where $\mathbf { L } _ { t }$ is a lower triangular matrix [14]. To ensure that the covariance matrix is positive semi-definite it is sufficient that the diagonal elements of $\mathbf { L } _ { t }$ are all non-negative. Vector $\alpha _ { t }$ is obtained using an exponential activation function, therefore its elements are positive and can be used as the diagonal elements of $\mathbf { L } _ { t } ,$ namely $[ \mathbf { L } _ { t } ] _ { i , i } = \alpha _ { i , t }$ . The six off-diagonal elements of $\mathbf { L } _ { t }$ correspond to the elements of vector $\beta _ { t } ,$ that are placed following an arbitrary (but consistent across iterations) order.

Once the aleatoric covariance is obtained applying the above transformations, a maximum-likelihood (ML) approach is used to jointly optimize the state and the covariance estimates, interpreting the training phase as fitting a probabilistic model. In particular, we use the negative log-likelihood of a multivariate Gaussian as the loss function of the ML-CRNN

$$
\ell ( { \bf x } _ { t } , \hat { \bf x } _ { t } , \hat { \Sigma } _ { t } ^ { a } ) = \left( { \bf x } _ { t } - \hat { \bf x } _ { t } \right) ^ { T } ( \hat { \Sigma } _ { t } ^ { a } ) ^ { - 1 } \left( { \bf x } _ { t } - \hat { \bf x } _ { t } \right) + \ln | \hat { \Sigma } _ { t } ^ { a } | ,\tag{4}
$$

where both $\hat { \mathbf { x } } _ { t }$ and $\hat { \Sigma } _ { t } ^ { a }$ are outputted by the network at each time-step. The total loss on the sequence of T frames is computed as $\begin{array} { r } { \mathcal { L } = \sum _ { t = 1 } ^ { T } \ell ( \mathbf x _ { t } , \hat { \mathbf x } _ { t } , \hat { \mathbf { \Sigma } } _ { t } ^ { a } ) / \bar { T } } \end{array}$ . Training the network by minimizing Eq. (4) amounts to maximizing the likelihood that the predicted state and covariance actually represent the parameters of a Gaussian probabilistic model.

2) Epistemic covariance, $\Sigma _ { t } ^ { e } ,$ is due to the uncertainty in the prediction made by the deep learning model. It can be estimated using Monte-Carlo (MC) dropout [15]. This method consists in applying the dropout procedure during inference, making the NN output random even for a fixed input. MC dropout uses the last NN available at time t, and is not part of the NN parameter learning process.

Total variance. The ML-CRNN model at time t can be run M times for each input with MC dropout. In this way, M different state and covariance samples are obtained for the same input. The time index is dropped here for convenience, as we operate within a single time-step. We respectively denote by $\hat { \mathbf { x } } _ { m }$ and $\hat { \Sigma } _ { m } ^ { a } , \ m \ = \ 1 , \ldots , M$ , the state and covariance predictions outputted by the NN, while we refer to their empirical averages over the M samples as $\textstyle \bar { \mathbf { x } } = \sum _ { m } \hat { \mathbf { x } } _ { m } / M$ and $\begin{array} { r } { \bar { \Sigma } ^ { a } = \sum _ { m } \hat { \Sigma } _ { m } ^ { a } / M . } \end{array}$ . Using the sample covariance estimator for $\pmb { \Sigma } ^ { e } ,$ , and $\bar { \Sigma } ^ { a }$ as the sample mean estimate of $\pmb { \Sigma } ^ { a }$ , the total error covariance matrix can be expressed as [13]

$$
\begin{array} { r } { \hat { \bar { \mathbf { \Sigma } } } \approx \underbrace { \cfrac { 1 } { M } \displaystyle \sum _ { m = 1 } ^ { M } ( \hat { \mathbf { x } } _ { m } - \bar { \mathbf { x } } ) ( \hat { \mathbf { x } } _ { m } - \bar { \mathbf { x } } ) ^ { T } } _ { \mathrm { e p i s t e m i c } } + \underbrace { \bar { \Sigma } ^ { a } } _ { \mathrm { a l e a t o r i c } } . } \\ { = \cfrac { 1 } { M } \displaystyle \sum _ { m = 1 } ^ { M } \hat { \mathbf { x } } _ { m } \hat { \mathbf { x } } _ { m } ^ { T } - \bar { \mathbf { x } } \bar { \mathbf { x } } ^ { T } + \bar { \mathbf { \Sigma } } ^ { a } . } \end{array}\tag{5}
$$

x¯ is typically more precise than a single sample from the MC dropout, so the final system outputs at step t are the averaged estimate $\hat { \mathbf { x } } _ { t } = \bar { \mathbf { x } } _ { t }$ and its covariance $\hat { \Sigma } _ { t }$ from Eq. (5). The complete procedure is summarized in Fig. 3

![](images/033c6a33055327b6d8d3549a1d2e43d7df97128f7b513a522ea13d7ef519c05a.jpg)  
Fig. 3: Block diagram of the ML state and covariance estimation.

<table><tr><td rowspan="2">Method</td><td colspan="2">Position</td><td>Velocity</td></tr><tr><td>RMSE [cm]</td><td>LEO(0.2) [%]</td><td>RMSE [cm/s]</td></tr><tr><td>UKF</td><td>32.8</td><td>47.1</td><td>56.8</td></tr><tr><td>MSE-CRNN</td><td>12.8</td><td>7.30</td><td>20.1</td></tr><tr><td>ML-CRNN</td><td>7.59</td><td>0.62</td><td>14.0</td></tr></table>

TABLE 1: Tracking error of UKF and the proposed CRNN network with ML (ML-CRNN) and MSE (MSE-S2S) loss criteria.

## IV. RESULTS

The proposed NN architecture is trained and tested on experimental measurements taken in a 8 m × 4 m research laboratory equipped with a motion tracking system with six infra-red cameras. A total of 10 minutes of training data and 1 minute of test data were collected for a single subject moving inside a 4 m × 2 m rectangle, i.e., the working area of the motion tracking system. The target moved following linear, circular, and zig-zag trajectories at a normal walking speed. These measurements were taken in realistic conditions, with furniture and other people inside the room, but outside the tracking area. This makes the radar images highly cluttered, with bursts of frames in which the target subject is undetectable. Ground truth data was acquired by the motion tracking system, which was time-synchronized with the radar.

We trained the ML-CRNN using the loss in Eq. (4) and the Adam optimizer [16], using a subset of the training data as the validation set. Training was stopped when the loss reached convergence on the validation set, and the epistemic covariance on the training set became negligible. The length of the temporal sequences that are fed to the NN during training is $T = 1 0$ (0.667 s). During the evaluation, instead, the predictions are obtained by inputting a new radar frame in the ML-CRNN as soon as it becomes available. The ML-CRNN then uses the hidden state, h<sub>t</sub>, and the current input to compute the prediction, similarly to how Bayesian filtering methods operate. The following metrics were used to evaluate the tracking error: (i) root mean square error (RMSE) and (ii) localization error outage, $\mathrm { L E O } ( 0 . 2 ) = \mathrm { P r o b } \left( | | \mathbf { x } - { \hat { \mathbf { x } } } | | > 2 0 \ \mathrm { c m } \right)$ ).

## A. Performance

Tracking – In Tab. 1, we show the results obtained by the proposed CRNN model with the ML loss of Eq. (4) (ML-CRNN), compared to the same model trained with standard MSE loss (MSE-CRNN), i.e., without the covariance estimation, and to an unscented Kalman filter (UKF) with a constant velocity motion model, which is a widely adopted Bayesian filtering method for estimating the posterior state distribution in non-linear radar tracking [17]. The parameters of the UKF have been optimized via grid search on the same training dataset used for the ML-CRNN. Both CRNN methods are clearly superior in tracking accuracy to the UKF, showing an RMSE reduction of about 0.25 m in the location accuracy and 0.4 m/s in the velocity estimation. Note that the UKF cannot perform tracking from high-dimensional raw data: denoising and clustering are needed to transform the RDA maps into vectors containing the range and angular position of the target. For this purpose, we implemented the clustering method used in [3]–[5], based on the DBSCAN [18] algorithm.

A further important aspect is the effect of NN training by using the ML loss: in addition to getting an estimate of the prediction uncertainty, we also observed a considerable improvement of the tracking accuracy. The ML-CRNN learning process is indeed less affected by outliers in the radar measurements due to its probabilistic nature, assigning low importance to unlikely observations.

Uncertainty estimation – To gauge the quality of the obtained uncertainty estimates, we first compare the NLL from ML-CRNN against that of UKF during a measurement sequence, see Fig. 4a, using M = 25 MC samples in Eq. (5). Note that, in practice, the value of M can be tuned to trade off between computational complexity and quality of the resulting uncertainty estimation. We notice that ML-CRNN is slower to converge, due to its long-term dependency on past inputs, (T = 10 time-steps), but achieves much better performance (smaller NLL) after the initial transient, showing its superior capability of capturing the underlying human movement model.

In Fig. 4b, we show the relation between the predicted uncertainty and the position estimates for ML-CRNN, focusing on the y component of the velocity, $v _ { y } .$ . We see that the uncertainty (standard deviation of $v _ { y }$ , bottom) shows a positive peak when $v _ { y }$ changes rapidly (top).

A further way to investigate the quality of the covariance is to compare the empirical frequency of the squared Mahalanobis distance, $\xi _ { t } = \left( \mathbf { x } _ { t } - \hat { \mathbf { x } } _ { t } \right) ^ { T } ( \hat { \Sigma _ { t } } ) ^ { - 1 } \left( \mathbf { x } _ { t } - \hat { \mathbf { x } } _ { t } \right)$ , on the test measurements, with its theoretical probability distribution. Due to the Gaussian posterior probability assumption for the state, it can be shown that $\xi _ { t }$ should follow a $\chi ^ { 2 }$ distribution with 4 degrees of freedom (the state dimension) [19].

In Fig. 4c, we plot a comparison between the empirical frequency and the theoretical value of the probability distribution of $\xi _ { t } .$ . An ideal calibration of the uncertainty would yield a perfect match between the two, as in the black line. From our experiment, we see that a clear improvement is obtained with ML-CRNN by using both the aleatoric and the epistemic components of the covariance, over using either of them in isolation. In particular, only using the epistemic component leads to severely underestimating the uncertainty, because it neglects the intrinsic variability of the movement process of the target. On the other hand, the UKF shows inferior calibration quality, which denotes the limitations of the underlying movement model. Quantitatively, the calibration mean-squared errors between the ideal case (perfect calibration) and the predicted uncertainty are $9 \cdot 1 0 ^ { - 4 } $ and $5 \cdot 1 0 ^ { - 3 } ~ $ for the ML-

![](images/9a51ffae04f05fa3a92dae18c1cd6a59b31ae13bb3f52aa34cb7057400cd680e.jpg)  
(a)

![](images/ea77fd4985d054cca1507f784a853dcdf85428561c540aec48a557839c1bdb30.jpg)  
(b)

![](images/0569794056be0f7f5902edf87d6a0ef7a6450fa97949a6280d9cbb690c3f9353.jpg)  
(c)  
Fig. 4: (a) Negative log-likelihood (NLL) on test data for ML-CRNN and UKF. (b) Estimate of $v _ { y }$ (top) and its predicted standard deviation (bottom). (c) Comparison between the empirical distribution of the squared Mahalanobis distances and the theoretical one.

CRNN ad the UKF, respectively.

## V. CONCLUSIONS

In this paper, we proposed a convolutional recurrent neural network to track human movement in indoor spaces by means of a mmWave MIMO FMCW radar. Our model estimates position and velocity of the subjects from raw radar data with superior accuracy with respect to state-of-the-art techniques, and without requiring any assumptions on the movement evolution process. The proposed neural network is trained as a probabilistic model using a maximum-likelihood loss function, obtaining explicit uncertainty estimates at its output, in the form of a time-varying error covariance matrices. This, besides allowing one to gauge the uncertainty in the tracking process, leads to greatly improved performance against the best available approaches, i.e., the UKF, lowering the average tracking error from 32.8 to 7.59 cm and from 56.8 to 14 cm/s in terms of position and velocity, respectively.

Future research work includes the integration of deep learning models for object detection and recognition in the ML-CRNN. This would allow simultaneously detecting multiple targets, obtaining a probability distribution of their position and recognizing the target nature, e.g., person, pet, vehicle, etc.

## REFERENCES

[1] S. A. Shah and F. Fioranelli, “RF sensing technologies for assisted daily living in healthcare: A comprehensive review,” IEEE Aerospace and Electronic Systems Magazine, vol. 34, no. 11, pp. 26–44, 2019.

[2] N. Knudde, B. Vandersmissen, K. Parashar, I. Couckuyt, A. Jalalvand, A. Bourdoux, W. De Neve, and T. Dhaene, “Indoor tracking of multiple persons with a 77 GHz MIMO FMCW radar,” in European Radar Conference (EURAD), (Nuremberg, Germany), Oct 2017.

[3] P. Zhao, C. X. Lu, J. Wang, C. Chen, W. Wang, N. Trigoni, and A. Markham, “mID: Tracking and Identifying People with Millimeter Wave Radar,” in 15th International Conference on Distributed Computing in Sensor Systems (DCOSS), (Santorini Island, Greece), May 2019.

[4] J. Pegoraro, F. Meneghello, and M. Rossi, “Multi-Person Continuous Tracking and Identification from mm-Wave micro-Doppler Signatures,” IEEE Transactions on Geoscience and Remote Sensing, vol. 59, pp. 2994 – 3009, Apr 2021.

[5] J. Pegoraro and M. Rossi, “Real-time people tracking and identification from sparse mm-wave radar point-clouds,” IEEE Access, May 2021.

[6] A. Kendall and Y. Gal, “What uncertainties do we need in Bayesian deep learning for computer vision?,” in Advances in neural information processing systems (NIPS), (Long Beach, California, USA), Dec 2017.

[7] K. Cho, B. Van Merrienboer, C. Gulcehre, D. Bahdanau, F. Bougares,¨ H. Schwenk, and Y. Bengio, “Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation,” in Conference on Empirical Methods in Natural Language Processing (EMNLP), (Doha, Qatar), Oct 2014.

[8] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Processing Magazine, vol. 34, pp. 22–35, Mar 2017.

[9] V. Winkler, “Range Doppler detection for automotive FMCW radars,” in European Radar Conference (EuRAD), (Munich, Germany), Oct 2007.

[10] D. A. Clevert, T. Unterthiner, and S. Hochreiter, “Fast and accurate deep network learning by exponential linear units (ELUs),” in International Conference on Learning Representations (ICLR), (San Juan, Puerto Rico), May 2016.

[11] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, “Dropout: a simple way to prevent neural networks from overfitting,” Journal of machine learning research, vol. 15, pp. 1929–1958, Jun 2014.

[12] Y. Gal and Z. Ghahramani, “A theoretically grounded application of dropout in recurrent neural networks,” in Advances in neural information processing systems (NIPS), (Barcelona, Spain), Dec 2016.

[13] R. L. Russell and C. Reale, “Multivariate uncertainty in deep learning,” IEEE Transactions on Neural Networks and Learning Systems, Early Access, Jun 2021.

[14] D. S. Watkins, Fundamentals of matrix computations. John Wiley & Sons, 2004.

[15] Y. Gal and Z. Ghahramani, “Dropout as a Bayesian approximation: Representing model uncertainty in deep learning,” in 33rd International Conference on Machine Learning (ICML), (New York City, New York, USA), Jun 2016.

[16] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in International Conference on Learning Representations (ICLR), (San Diego, California, USA), May 2015.

[17] S. J. Julier and J. K. Uhlmann, “New extension of the Kalman filter to nonlinear systems,” in AeroSense ’97, (Orlando, Florida, USA), International Society for Optics and Photonics, Apr 1997.

[18] M. Ester, H.-P. Kriegel, J. Sander, X. Xu, et al., “A density-based algorithm for discovering clusters in large spatial databases with noise,” in 2nd International Conference on Knowledge Discovery and Data Mining, (Portland, Oregon, USA), Aug 1996.

[19] Y. Bar-Shalom, F. Daum, and J. Huang, “The probabilistic data association filter,” IEEE Control Systems Magazine, vol. 29, pp. 82–100, Dec 2009.