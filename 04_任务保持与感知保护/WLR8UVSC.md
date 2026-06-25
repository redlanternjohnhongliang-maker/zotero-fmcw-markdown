# End-to-End Training of Neural Networks for Automotive Radar Interference Mitigation

Christian Oswald

Graz University of Technology

Graz, Austria

christian.oswald@tugraz.at

Mate Toth

Graz University of Technology

Graz, Austria

mate.a.toth@tugraz.at

Paul Meissner

Infineon Technologies AG

Graz, Austria

paul.meissner@infineon.com

Franz Pernkopf Graz University of Technology Graz, Austria pernkopf@tugraz.at

Abstract—In this paper we propose a new method for training neural networks (NNs) for frequency modulated continuous wave (FMCW) radar mutual interference mitigation. Instead of training NNs to regress from interfered to clean radar signals as in previous work, we train NNs directly on object detection maps. We do so by performing a continuous relaxation of the cellaveraging constant false alarm rate (CA-CFAR) peak detector, which is a well-established algorithm for object detection using radar. With this new training objective we are able to increase object detection performance by a large margin. Furthermore, we introduce separable convolution kernels to strongly reduce the number of parameters and computational complexity of convolutional NN architectures for radar applications. We validate our contributions with experiments on real-world measurement data and compare them against signal processing interference mitigation methods.

Index Terms—Neural networks, machine learning, FMCW radar, radar interference mitigation, end-to-end training, convolutional neural networks, separable convolutions, object detection

## I. INTRODUCTION

Frequency modulated continuous wave radar is a key technology in advanced driver assistance systems such as emergency break assist or adaptive cruise control. However, FMCW radar is prone to interference due to its emited wideband signal. More concretely, data delivered by an FMCW radar might be entirely corrupted if it is interfered by another FMCW radar (mounted on e.g., another car) operating in the same frequency range; This causes mutual interference as both radars are affected. A more detailed explanation of FMCW radar mutual interference can be found in [1], [2].

## A. Motivation and Contributions

Many proposed methods for radar interference mitigation consist of NNs performing a regression from interfered to clean radar signals. However, as perfect interference mitigation is impossible in practice, residual errors remain in the neural networks’ predictions. It is not clear how these residual errors influence object detection performance, which is the main application of automotive radar. In other words, there exists a misalignment between the neural networks’ training objective and the actual desired objective, which prohibits usage of NNs in this safety critical application.

![](images/9fad7142e9e08ea9cb216e1ae0efc68f9c6537f6c1bab716b2ea212f1537a9fd.jpg)  
Fig. 1. Overview of the proposed method to train neural networks for radar interference mitigation. The network’s output as well as the groundtruth clean radar signal are passed through a CA-CFAR detector, which has been designed prior to training. The CA-CFAR detector’s threshold comparison is continuously relaxed during training, which yields continuous object detections and differentiability of the CA-CFAR detector. The predicted and ground-truth object detections are compared using the balanced crossentropy loss function, and gradients are backpropagated through the CA-CFAR detector to the parameters of the neural network.

In this paper we therefore propose to train NNs directly on object detection maps. However, we do not integrate object detection into the neural networks’ architecture, as this would increase their size while reducing their robustness and explainability. Instead, we continuously relax the well-established cell-averaging constant false alarm rate (CA-CFAR) detector [3] to enable end-to-end training of existing NN architectures. The NNs are therefore optimized for usage with a specific

CA-CFAR detector. Fig. 1 depicts the proposed training setup including interference mitigation and object detection.

Another issue preventing NNs from deployment is their computational complexity. If NNs are to be implemented on hardware for real-time processing of radar data we must reduce their size as much as possible. In this paper we therefore present a simple yet effective modification for existing convolutional architectures, which reduces compuational complexity by orders of magnitude while not sacrifycing performance. In particular, we incorporate the independence of range, velocity and angle of objects into the NN architecture.

## B. Related Work

Mutual interference mitigation in FMCW radar is a wellstudied problem. Some methods like frequency hopping [4] change transmit parameters if interference is detected in the radar’s output. Another approach, which also encompasses this paper, consists of removing interferences from an already corrupted signal. Zeroing [5] detects interfered samples in the signal and sets them to zero. Ramp filtering [6] performs nonlinear filtering over multiple FM ramps to restore the magnitude of the object signal. Iterative method with adaptive thresholding (IMAT) [7] reconstructs previously zeroed samples using the inverse FFT of the signal’s sparse spectrum.

There exist various machine learning based methods for mutual interference mitigation which operate on different signal representations: [8], [9] process time-domain signals, while [10], [11], [12] perform interference mitigation on socalled range-Doppler (RD) maps, which are the time domain signal’s two-dimensional Fourier transform. More concretely, [10] operates on one antenna at a time while [11] extends this to complex-valued array processing. Other architectures processing RD-maps are based on convolutional autoencoders [13], [14]. In our previous work [15], we jointly process the entire receive array, but do so by using a fully convolutional architecture on range-Doppler-angle (RDA) maps, which is the three-dimensional Fourier transform of the receive array’s output. The architecture proposed in [16] transforms interfered signals given as spectrograms to interference mitigated rangeprofiles, which are the one-dimensional Fourier transform of the time domain signal. In [17] a fully convolutional architecture is applied to the interfered signal’s short-time Fourier transform.

Deep learning has also been utilized to perform object detection in FMCW radar data. In [18] an architecture using the single shot detector [19] is trained; It operates on sequences of RDA-maps where labels have been annotated using a LiDAR sensor. The architecture in [20] also trains on sequences of RDA-maps but is based on autoencoders. Reference [21] uses the radar calibration data to train a two-step object detector network in the style of faster-RCNN [22]. However, none of the aforementioned object detectors considers interference mitigation; Furthermore, they construct a fully trainable object detector while we do not replace the hand-designed CA-CFAR detector.

## II. END-TO-END TRAINING

Fig. 2 shows the structure of a CA-CFAR detector [3]. The key observation is that all operations inside a CA-CFAR detector except the threshold comparison are differentiable. We therefore can perform backpropagation through the CA-CFAR detector by replacing the threshold comparison with a differentiable surrogate function. The comparison operator can be continuously relaxed [23] using the logistic sigmoid

$$
\sigma \bigg ( \frac { \mathrm { S I N R } - \beta } { \tau } \bigg ) = \frac { 1 } { 1 + e ^ { \frac { \beta - \mathrm { S I N R } } { \tau } } } ,\tag{1}
$$

where $\beta$ is the threshold value and τ the temperature hyperparameter which controls the smoothness of the continuous relaxation. If we let $\tau  0$ , we recover the original discrete comparison operator, which is given as a step-function shifted by $\beta .$

In this paper we assume the CA-CFAR detector’s parameters, namely its window size, number of guard cells and threshold to be hand-designed. Furthermore, we assume the CA-CFAR detector has a three-dimensional window for cell averaging. In other words, the CA-CFAR detector’s takes RDA-maps as input and considers the vicinity of the cellunder-test w.r.t. range, velocity and angle to determine the local SINR. However, if we do not measure AoAs, we use a CA-CFAR detector operating on RD-maps with a two-dimensional window, and a four-dimensional CA-CFAR detector if we consider azimuth and elevation. Finally, we assume the CA-CFAR detector has a fixed, non-adaptive threshold. Depending on the NN architecture (cf. Section I-B) we perform multiple Fourier transforms on the NN’s output in order to feed range-Doppler-angle maps into the CA-CFAR detector, which are then included in the gradient backpropagation path.

The task at hand is a bin-wise binary classification between the two classes object and no object. However, these two classes are highly imbalanced as no object is present at the majority of bins in the RDA-map. Meanwhile, the commonly used binary cross-entropy (CE) loss function [24] assumes the data set to be balanced, i.e., both classes appear with the same frequency in the data set. If we were to train a NN using CE, it would simply predict a low magnitude at all locations, reflecting the class frequencies in the data set. One common approach to address class imbalance consists of weighting the individual terms of the CE, resulting in the balanced cross entropy loss function (BCE) [24],

$$
\mathrm { B C E } ( y , \hat { y } , \alpha ) = - \alpha y \log ( \hat { y } ) - ( 1 - \alpha ) ( 1 - y ) \log ( 1 - \hat { y } ) ,\tag{2}
$$

where y is the target, yˆ the model’s prediction, and α a weighting hyperparameter between 0 and 1. If $\alpha = 0 . 5$ , both terms contributing to BCE are equally weighted, which is the desired weighting scheme for balanced datasets. If class 0 appears more frequently in the data set than class 1, one should set $\alpha > 0 . 5 \mathrm { : }$ Misclassifying a sample of class 1 then incurs a higher loss than misclassifying a sample of class 0.

A related technique to deal with non-differentiable operators in the computation graph is the so-called straight-throughestimator [23], where operations prohibiting gradient backpropagation are replaced by a continuous relaxation in the backward path of the computation graph. However, in this work we also use the continuous relaxation (1) in the forward path, i.e., we train on continuous targets $y \in [ 0 , 1 ]$ . Continuous targets ease optimization compared to discrete targets (which are used with the straight-through-estimator [23]) by providing more fine-grained feedback; Meanwhile, the discrete targets $y \in \{ 0 , 1 \}$ can be recovered by thresholding the continuous targets with 0.5. Even though the BCE is most commonly used for discrete targets it extends to continuous targets as

![](images/4185755b545ab85d52de7de2f7a18b24fe01a66db2c32fe5927e2c678bd76813.jpg)  
Fig. 2. Computations performed inside a CA-CFAR detector. When training a NN, we replace the CA-CFAR detector’s threshold comparison by the logistic sigmoid σ to allow for backpropagation of gradients. Operations are depicted in rounded and red, intermediate values in square and blue boxes.

$$
\operatorname * { a r g m i n } _ { \hat { y } } ( \mathrm { B C E } ( y , \hat { y } , \alpha ) ) = y , \forall y , \beta \in [ 0 , 1 ] .\tag{3}
$$

## III. SEPARABLE CONVOLUTIONS

Orthogonal to the training method described in Section II, we propose a method to reduce the overall complexity of convolutional NN architectures for radar interference mitigation by introducing separable convolution kernels.

A convolution kernel is called separable if it can be factored into multiple lower-dimensional kernels. For example, a twodimensional kernel W is separable if it can be written as $W \ : = \ : w _ { 1 } w _ { 2 }$ , where W is a $K \times K$ matrix, while $w _ { 1 }$ and w<sub>2</sub> have dimensions $K \times 1$ and $1 \times K$ , respectively. When designing a convolutional NN one can therefore parameterize a convolution kernel by $w _ { 1 }$ and $w _ { 2 }$ instead of $W$ . This reduces a kernel’s number of parameters, as an N-dimensional kernel now only has $K \cdot N$ instead of $K ^ { N }$ parameters. On the other hand, the model is now restricted to learning separable filters (such as Gaussian or Sobel filters), which reduces performance in the general case. In radar interference mitigation however we can use separable convolutions to encode our domain knowledge about the independence of the range, velocity and angle of objects in the RDA-map. We can assume an object’s range and angle to be independent if the distance between receivers is sufficiently small compared to the range of an object, i.e., the object is in the far-field and reflects planewaves [25]. Furthermore, an object’s measured velocity is independent from its range and angle if the object’s relative movement doppler-shifting its reflection is negligible. From an image processing viewpoint, objects typically appear as axisaligned star-shaped peaks in the RDA-map, where the length of the star’s legs is given by the corresponding aperture of the radar sensor. These star shapes can also be described in a factorized form, such that convolutional NN architectures do not lose any of their expressiveness when scanning for this shape.

Separable convolutions have lower computational complexity then generic convolutions with the same kernel size, as the input can be convolved with each of the separable kernel’s components consecutively. The number of multiplyaccumulate operations therefore reduces from $K ^ { N }$ multiplications and 1 accumulation for generic to $K \cdot N$ multiplications and N accumulations for separable kernels per convolution operation.

## IV. EXPERIMENTAL SETUP

In Section V we train our NN architecture introduced in [15] on various training objectives and compare their performance with zeroing [5], ramp-filtering [6] and iterative adaptive thresholding (IMAT) [7]. Moreover, we replace generic by separable convolutions and evaluate different kernel sizes.

## A. Angle-Equivariant Convolutional Neural Network (AENN)

In this section we briefly review our architecture introduced in [15] for FMCW radar mutual interference mitigation. We use AENN in subsequent experiments to validate our proposed end-to-end training setup as well as separable convolutions. A visualization of AENN can be found in Fig. 3.

AENN consists of convolution, ReLU activation and batch normalization layers that operate on RDA-maps; All layers are complex-valued. The activations are zero-padded and the convolution stride is set to one such that AENN’s output (an interference mitigated RDA-map) has the same size as its input, which are interfered RDA-maps. The novelty of AENN is that it generalizes across different AoAs of interferences, i.e., only one AoA of interferences needs to be present in the training dataset; In other words, AENN is equivariant w.r.t. the AoA of interferences. If the ego radar measures azimuth and elevation, the three-dimensional layers can be extended by a fourth dimension to perform interference mitigation on range-Doppler-azimuth-elevation maps in an analogous manner.

The AENN we evaluate in subsequent experiments consists of three layers with 4, 2 and 1 complex-valued output channels, respectively. We use complex-valued $R e L U$ and batchnormalization with trainable scaling and bias [11] after the first and second layer.

![](images/f239f28b085645345d0f59e58c551012e663b97b9f508e0a51ec00e414f75535.jpg)  
Fig. 3. Structure of the Angle-Equivariant Neural Network (AENN) used for evaluation in Section V. The network’s input is a range-Doppler-angle map with dimensions [96, 96, 16], which is processed with complex-valued convolution kernels of size $[ K _ { A } , K _ { D } , K _ { R } ]$ . The network has 2 hidden layers which are 4 and 2 channels wide. Note that AENN can be used with range-Doppler-angle maps of variable size due to its fully convolutional architecture. For a more detailed description, please refer to [15].

## B. Data Set

Our data set consists of real-world inner-city measurements. We ran a CA-CFAR detector with a continuously relaxed threshold comparison on the measured RDA-maps to generate targets for AENN trained on BCE. For AENN trained on other objectives we directly use the measured RDA-maps as targets. We then synthesised and added artificial interferences to our measurements which are used as inputs for AENN. The interference signal model we use is the same as in [1], [2], [6], [10], amongst others. The data is finally divided into training, testing, and validation sets of sizes 2500, 250, and 250, respectively. A single sample comprises 96 range, 96 Doppler, and 16 angle bins, meaning one sample is a rankthree tensor with dimensions [96, 96, 16]. The ego radar’s parameters as well as the parameter ranges for the artificial interferers can be found in the Appendix.

## C. Metrics and Loss Functions

1) Mean Squared Error (MSE): To gauge the performance of AENN trained in the proposed end-to-end setup, we compare it against the same AENN trained to minimize the MSE between its prediction $\hat { S }$ and the clean RDA-map S, with

$$
\mathrm { M S E } ( S , \hat { S } ) = \frac { 1 } { N } \sum _ { N } ( | S - \hat { S } | ) ^ { 2 } ,\tag{4}
$$

where N is the total number of bins in a RDA-map.

2) Mean Squared Error of Magnitudes (MAGMSE): As the CA-CFAR detector only operates on the magnitude of RDAmaps, one can also train NNs to minimize the MSE of RDAmap magnitudes. By contrast, when trained on (4), NNs not only try to match the magnitude but also the phase of their prediction. We define MAGMSE as

$$
\mathbf { M A G M S E } ( S , \hat { S } ) = \frac { 1 } { N } \sum _ { N } ( | S | - | \hat { S } | ) ^ { 2 } .\tag{5}
$$

3) F1-score: We use the F1-score to evaluate object detection performance. More concretely, we perform bin-wise comparison of ground-truth and predicted object detections,

which are given as rank-three RDA binary tensors. The F1- score is defined as

$$
F _ { 1 } = 2 \cdot \frac { N _ { T P } } { N _ { T P } + \frac { 1 } { 2 } ( N _ { F P } + N _ { F N } ) } ,\tag{6}
$$

where $N _ { T P }$ is the number of true positives, false positives $N _ { F P }$ and false negatives $N _ { F N }$ . We evaluate the F1-score with a tolerance of 3 range bins, 3 Doppler bins and 1 angle bin; In other words, if a detected object has the aforementioned distance from a ground-truth object, we still count it as a true positive.

## V. EXPERIMENTS

All AENNs have been optimized using ADAM and a batchsize of 8. We perform early-stopping w.r.t. the validation F1- score. We normalize the data set such that the covariance between the RDA-maps’ real and imaginary part is the identity matrix. Through experimentation we found that we achieve best performance if we set the BCE’s weighting parameter $\alpha = 0 . 7 5$ and the continuous relaxation’s temperature $\tau = 1 0$ We hypothesize that higher values for τ lead to smoother gradients as predictions do not cap as quickly at 0 and 1. We compare various training objectives for AENN with and without separable convolution kernels. In TABLE I, Generic convolutions are indicated by $\vec { \bf \Phi } \vec { \bf g } ^ { \prime } \vec { \bf \Phi }$ and separable convolutions by $\mathbf { \vec { \Delta } } ^ { , , } \mathbf { \vec { s } } ^ { , \vec { \mathbf { \Delta } } }$ . Furthermore, we evaluate multiple signal processing methods for interference mitigation. Note that each of the complex-valued convolution kernel’s elements consists of two (real-valued) parameters. Furthermore, AENN performs complex-valued multiplications, which consist of four realvalued multiplications and two additions [11].

As can be seen in TABLE I, training AENN on BCE outperforms other training objectives by a large margin in terms of the F1-score. Training AENN on MAGMSE instead of MSE already increases object detection performance. As expected, the model trained on MAGMSE achieves the lowest MAGMSE on the test set. An example of predicted RDAmaps and their associated object detections can be seen in Fig. 4. Even though the MAGMSE of AENN trained with

TABLE I PERFORMANCE OF AENN.
<table><tr><td rowspan=1 colspan=1>trained on</td><td rowspan=1 colspan=1>size</td><td rowspan=1 colspan=1>#params</td><td rowspan=1 colspan=1>F1</td><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>MSE</td></tr><tr><td rowspan=1 colspan=1>BCE</td><td rowspan=1 colspan=1>[3,3,3] g</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>0.844</td><td rowspan=1 colspan=1>129428</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BCE</td><td rowspan=1 colspan=1>[3,3,3] s</td><td rowspan=1 colspan=1>296</td><td rowspan=1 colspan=1>0.867</td><td rowspan=1 colspan=1>154893</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BCE</td><td rowspan=1 colspan=1>[5,5,5] s</td><td rowspan=1 colspan=1>464</td><td rowspan=1 colspan=1>0.903</td><td rowspan=1 colspan=1>152258</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BCE</td><td rowspan=1 colspan=1>[7,7,7] s</td><td rowspan=1 colspan=1>632</td><td rowspan=1 colspan=1>0.921</td><td rowspan=1 colspan=1>148641</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BCE</td><td rowspan=1 colspan=1>[9,9,9] s</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>0.914</td><td rowspan=1 colspan=1>151523</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>[3,3,3] g</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>0.769</td><td rowspan=1 colspan=1>22192</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>[3,3,3] s</td><td rowspan=1 colspan=1>296</td><td rowspan=1 colspan=1>0.748</td><td rowspan=1 colspan=1>23849</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>[5,5,5] s</td><td rowspan=1 colspan=1>464</td><td rowspan=1 colspan=1>0.835</td><td rowspan=1 colspan=1>11600</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>[7,7,7] s</td><td rowspan=1 colspan=1>632</td><td rowspan=1 colspan=1>0.827</td><td rowspan=1 colspan=1>11624</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>[9,9,9] s</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>0.830</td><td rowspan=1 colspan=1>12066</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>MSE</td><td rowspan=1 colspan=1>[3,3,3] g</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>0.712</td><td rowspan=1 colspan=1>26438</td><td rowspan=1 colspan=1>34101</td></tr><tr><td rowspan=1 colspan=1>MSE</td><td rowspan=1 colspan=1>[3,3,3] s</td><td rowspan=1 colspan=1>296</td><td rowspan=1 colspan=1>0.621</td><td rowspan=1 colspan=1>53557</td><td rowspan=1 colspan=1>64813</td></tr><tr><td rowspan=1 colspan=1>MSE</td><td rowspan=1 colspan=1>[5,5,5] s</td><td rowspan=1 colspan=1>464</td><td rowspan=1 colspan=1>0.690</td><td rowspan=1 colspan=1>21311</td><td rowspan=1 colspan=1>30652</td></tr><tr><td rowspan=1 colspan=1>MSE</td><td rowspan=1 colspan=1>[7,7,7] s</td><td rowspan=1 colspan=1>632</td><td rowspan=1 colspan=1>0.628</td><td rowspan=1 colspan=1>39161</td><td rowspan=1 colspan=1>52641</td></tr><tr><td rowspan=1 colspan=1>MSE</td><td rowspan=1 colspan=1>[9,9,9] s</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>0.644</td><td rowspan=1 colspan=1>27368</td><td rowspan=1 colspan=1>38958</td></tr></table>

TABLE II

PERFORMANCE OF REFERENCE METHODS.
<table><tr><td rowspan=1 colspan=1>Method</td><td rowspan=1 colspan=1>F1</td><td rowspan=1 colspan=1>MAGMSE</td><td rowspan=1 colspan=1>MSE</td></tr><tr><td rowspan=1 colspan=1>zeroing [5]</td><td rowspan=1 colspan=1>0.655</td><td rowspan=1 colspan=1>184397</td><td rowspan=1 colspan=1>207039</td></tr><tr><td rowspan=1 colspan=1>ramp filtering [6]</td><td rowspan=1 colspan=1>0.551</td><td rowspan=1 colspan=1>1275671</td><td rowspan=1 colspan=1>1327445</td></tr><tr><td rowspan=1 colspan=1>IMAT [7]</td><td rowspan=1 colspan=1>0.513</td><td rowspan=1 colspan=1>297116</td><td rowspan=1 colspan=1>328553</td></tr><tr><td rowspan=1 colspan=1>no mitigation</td><td rowspan=1 colspan=1>0.306</td><td rowspan=1 colspan=1>12409976</td><td rowspan=1 colspan=1>12621186</td></tr></table>

BCE is multiple times higher than the MAGMSE of AENN trained with MAGMSE, the former’s prediction actually looks more similar to ground truth, which can be found in Fig. 1. This is due to the fact that AENN with MAGMSE smoothens the noise floor in addition to interference mitigation; This phenomenon has also been observed by [10].

The impact of separable convolutions on performance highly depends on the chosen training objective. While AENN with BCE greatly benefits from separable convolutions, performance of AENN with MSE actually deteriorates. This hints at the learned behaviour of AENN: When trained on BCE, AENN mainly performs template matching of the characteristic object peaks while suppressing everything else. As described in Section III, these object peaks can be represented in factorized form, which motivates the usage of separable convolutions. Meanwhile, restoring the clean complex-valued RDA-map is a more difficult task that seems to require generic convolutions. AENN trained on MAGMSE also benefits from separable convolutions, however, performance gains are not as pronounced as with BCE. Interestingly, performance of AENN trained with BCE increases when replacing generic with separable convolutions of same size even though AENN’s expressivity is reduced; We hypothesize this improvement is a consequence of the reduced optimization space.

AENN trained with BCE learns interference mitigation implicitly by uncovering masked objects. One therefore needs to ensure that a sufficient number of objects is masked by interference. The MSE for AENNs trained with BCE and MAGMSE are not reported as it becomes arbitrarily high. Interestingly, zeroing performs best amongst classical intereference mitigation methods, as summarized in TABLE II. We suspect this is caused by the high level of interferences.

For instance, ramp filtering only corrects the magnitude of an interfered signal, while corruptions proportional to the interference level remain in the signal’s phase.

## VI. CONCLUSION

In this paper we introduced end-to-end training of neural networks for FMCW radar mutual interference mitigation. Furthermore, we applied separable convolutions to reduce the overall complexity of such NN architectures. These contributions address two main issues preventing NNs from being used for interference mitigation in practice, namely computation complexity and transparency of the learned behaviour. However, more work is necessary for NNs to be usable in practice; For instance, no guarantees can be provided that NNs behave as intended under all possible circumstances, e.g. drifting sensor characteristics or changing weather conditions. In other words, the robustness of such NNs needs to be increased. Furthermore, NNs for radar interference mitigation still lack explainability necessary for this safety critical application. Therefore, we devote future work to further improve the robustness and explainability of NNs for radar interference mitigation.

## REFERENCES

[1] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[2] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical investigation of non-coherent mutual fmcw radar interference,” in 2018 15th European Radar Conference (EuRAD). IEEE, 2018, pp. 71–74.

[3] L. L. Scharf and C. Demeure, Statistical signal processing: detection, estimation, and time series analysis. Prentice Hall, 1991.

[4] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in 2016 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM). IEEE, 2016, pp. 1–4.

[5] C. Fischer, Untersuchungen zum interferenzverhalten automobiler radarsensorik. Cuvillier Verlag, 2016.

[6] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive fmcw radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS). IEEE, 2018, pp. 1–4.

[7] F. Marvasti, M. Azghani, P. Imani, P. Pakrouh, S. J. Heydari, A. Golmohammadi, A. Kazerouni, and M. Khalili, “Sparse signal processing using iterative method with adaptive thresholding (imat),” in 2012 19th International Conference on Telecommunications (ICT). IEEE, 2012, pp. 1–6.

[8] J. Mun, H. Kim, and J. Lee, “A deep learning approach for automotive radar interference mitigation,” in 2018 IEEE 88th Vehicular Technology Conference (VTC-Fall). IEEE, 2018, pp. 1–5.

[9] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using rnn with self attention,” in ICASSP 2020-2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2020, pp. 3802–3806.

[10] J. Rock, W. Roth, M. Toth, P. Meissner, and F. Pernkopf, “Resourceefficient deep neural networks for automotive radar interference mitigation,” IEEE Journal of Selected Topics in Signal Processing, vol. 15, no. 4, pp. 927–940, 2021.

[11] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Complexvalued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in 2021 IEEE Radar Conference (RadarConf21). IEEE, 2021, pp. 1–6.

[12] J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Deep interference mitigation and denoising of real-world fmcw radar signals,” in 2020 IEEE International Radar Conference (RADAR). IEEE, 2020, pp. 624– 629.

![](images/2adca38ae033b2dbe3fbcd22a1167f51120322cddff8512d6f31492b38227988.jpg)

![](images/7509319f045508381b2956ee35f66f32b524f8234ffaefa43215c074e167e418.jpg)

![](images/8106e1508818b0e74a907def6889367c265c417b25aaddfc97187ba6c264f487.jpg)

![](images/6b9c1f9867211709c4d86c99b0cc6f7e13c2f5ea3885735150b5dbd3a70decd4.jpg)  
Fig. 4. Comparison of an interference mitigated RDA-map (top) and its corresponding predicted objects (bottom) for the same AENN trained on the MSE of RDA-map magnitudes (left) and BCE of smoothened object predictions (right), visualized as range-angle maps. The objects are clearly visible in both range-angle maps; However, the AENN trained on MSE reduces its output’s SINR such that the CA-CFAR misses many objects, while most objects are correctly detected when the AENN is trained on BCE. AENN pads its activations prior to convolution, which results in deviations of magnitudes at the maps borders. The corresponding clean and interfered RDA-maps can be seen in Fig. 1. The blue boxes in the detection maps indicate the tolerance for determining true positives as described in Section IV-C3. Yellow bins are therefore true positives, while the turquoise bin is a false positive. We performed a non-coherent sum over the Doppler-dimension of the RDA-maps and a sum of the object detections to arrive at these plots. The maps in the top row have been normalized such that their maximum values are zero dB. All plots have been up-sampled for better interpretability. Best viewed in color.

[13] J. Fuchs, A. Dubey, M. Lubke, R. Weigel, and F. Lurz, “Automotive¨ radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR). IEEE, 2020, pp. 315– 320.

[14] M. L. L. de Oliveira and M. J. Bekooij, “Deep convolutional autoencoder applied for noise reduction in range-doppler maps of fmcw radars,” in 2020 IEEE International Radar Conference (RADAR). IEEE, 2020, pp. 630–635.

[15] C. Oswald, M. Toth, P. Meissner, and F. Pernkopf, “Angle-equivariant convolutional neural networks for interference mitigation in automotive radar,” in 2023 20th European Radar Conference (EuRAD). EuMA, 2023.

[16] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Fully convolutional neural networks for automotive radar interference mitigation,” in 2020 IEEE 92nd Vehicular Technology Conference (VTC2020-Fall). IEEE, 2020, pp. 1–5.

[17] J. Wang, R. Li, Y. He, and Y. Yang, “Prior-guided deep interference mitigation for fmcw radars,” IEEE Transactions on Geoscience and Remote Sensing, vol. 60, pp. 1–16, 2022.

[18] B. Major, D. Fontijne, A. Ansari, R. Teja Sukhavasi, R. Gowaikar, M. Hamilton, S. Lee, S. Grzechnik, and S. Subramanian, “Vehicle detection with automotive radar using deep learning on range-azimuth-doppler tensors,” in Proceedings of the IEEE/CVF International Conference on Computer Vision Workshops, 2019, pp. 0–0.

[19] W. Liu, D. Anguelov, D. Erhan, C. Szegedy, S. Reed, C.-Y. Fu, and A. C. Berg, “Ssd: Single shot multibox detector,” in Computer Vision– ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part I 14. Springer, 2016, pp. 21–37.

[20] X. Gao, G. Xing, S. Roy, and H. Liu, “Ramp-cnn: A novel neural network for enhanced automotive radar object recognition,” IEEE Sensors Journal, vol. 21, no. 4, pp. 5119–5132, 2020.

[21] D. Brodeski, I. Bilik, and R. Giryes, “Deep radar detector,” in 2019 IEEE Radar Conference (RadarConf). IEEE, 2019, pp. 1–6.

[22] S. Ren, K. He, R. Girshick, and J. Sun, “Faster r-cnn: Towards real-time object detection with region proposal networks,” Advances in neural information processing systems, vol. 28, 2015.

[23] Y. Bengio, N. Leonard, and A. Courville, “Estimating or propagating´ gradients through stochastic neurons for conditional computation,” arXiv preprint arXiv:1308.3432, 2013.

[24] S. Jadon, “A survey of loss functions for semantic segmentation,” in

2020 IEEE conference on computational intelligence in bioinformatics and computational biology (CIBCB). IEEE, 2020, pp. 1–7.

[25] D. H. Johnson, “Array signal processing,” concepts and techniques, 1993.

## APPENDIX

In TABLE III we list the ego radar’s parameters we used in our measurement campaign. We generate artificial interferer signals by uniformly sampling from the values given in TABLE IV. Even though the Signal & noise to interference ratio (SNIR) is positive in our data set, the local SNIR might be negative, as e.g., visible in Fig. 1.

TABLE III  
PARAMETERS OF EGO RADAR
<table><tr><td rowspan=1 colspan=2>Parameter</td></tr><tr><td rowspan=1 colspan=1>Sweep starting frequency</td><td rowspan=1 colspan=1>79 GHz</td></tr><tr><td rowspan=1 colspan=1>Sweep bandwidth</td><td rowspan=1 colspan=1>0.27 GHz</td></tr><tr><td rowspan=1 colspan=1>Sweep duration</td><td rowspan=1 colspan=1>12,8 µs</td></tr><tr><td rowspan=1 colspan=1>Number of sweeps</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>Number of receivers</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>Window type (range &amp; Doppler)</td><td rowspan=1 colspan=1>Hann</td></tr><tr><td rowspan=1 colspan=1>Window type (angle)</td><td rowspan=1 colspan=1>Taylor</td></tr></table>

TABLE IV

PARAMETER RANGES FOR INTERFERENCE SIGNALS
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>minimum</td><td rowspan=1 colspan=1>maximum</td></tr><tr><td rowspan=1 colspan=1>Number of interferers</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Sweep starting frequency</td><td rowspan=1 colspan=1>78.9 GHz</td><td rowspan=1 colspan=1>79.1 GHz</td></tr><tr><td rowspan=1 colspan=1>Sweep bandwidth</td><td rowspan=1 colspan=1>0.15 GHz</td><td rowspan=1 colspan=1>0.25 GHz</td></tr><tr><td rowspan=1 colspan=1>Sweep duration</td><td rowspan=1 colspan=1>12 µs</td><td rowspan=1 colspan=1>24 µs</td></tr><tr><td rowspan=1 colspan=1>Number of sweeps</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>156</td></tr><tr><td rowspan=1 colspan=1>Angle of arrival</td><td rowspan=1 colspan=1>-90°</td><td rowspan=1 colspan=1>90°</td></tr><tr><td rowspan=1 colspan=1>Signal &amp; noise to interference</td><td rowspan=1 colspan=1>10 dB</td><td rowspan=1 colspan=1>30 dB</td></tr></table>