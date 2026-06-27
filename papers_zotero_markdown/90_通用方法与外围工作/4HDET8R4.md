# An Uncertainty Quantification Framework for Deep Learning-Based Automatic Modulation Classification

Huian Yang and Rajeev Sahay

Abstract—Deep learning (DL) has been shown to be highly efective for automatic modulation classification (AMC), which is a pivotal technology for next-generation cognitive communications. Yet, existing DL methods for AMC often lack robust mechanisms for uncertainty quantification (UQ). This limitation restricts their ability to produce accurate and reliable predictions in real-world environments, where signals can be perturbed as a result of several factors such as interference and low signal-tonoise ratios (SNRs). To address this problem, we propose a deep ensemble approach that leverages multiple convolutional neural networks (CNNs) to generate predictive distributions, as opposed to point estimates produced by standard DL models, which produce statistical characteristics that quantify the uncertainty associated with each prediction. We validate our approach using real-world AMC data, evaluating performance through multiple UQ metrics in a variety of signal environments. Our results show that our proposed ensemble-based framework captures uncertainty to a greater degree compared with previously proposed baselines in multiple settings, including in-distribution samples, out-of-distribution (OOD) samples, and low SNR signals. These findings highlight the strong UQ capabilities of our ensemblebased AMC approach, paving the way for more robust DL-based AMC.

Index Terms—Automatic modulation classification (AMC), deep ensembles, deep learning (DL), out-of-distribution (OOD) samples, uncertainty quantification (UQ).

## I. INTRODUCTION

UTOMATIC modulation classification (AMC) is a vital component of modern wireless networks, as it enables the identification of modulation schemes without prior knowledge of the transmitted signal. This capability is crucial for ensuring reliable communication in dynamic and noisy environments, including military [1], [2] and civilian applications [3], where signals can be subject to interference and environmental distortions. As the Internet of Things (IoT) expands, next-generation communications (e.g., 6G) will heavily rely on AMC for eficient management of the increasingly congested wireless spectrum [4], [5].

Traditional AMC methods, such as maximum-likelihoodbased (MLB) approaches [6], [7], [8], [9], rely on statistical tests to estimate the probability of a particular modulation scheme. Although these methods can be efective, they require substantial prior knowledge of the received signal and its channel conditions [10]. Furthermore, MLB methods tend to be computationally expensive, incurring high latencies while requiring manual feature engineering from received in-phase and quadrature (IQ) time samples. Such limitations restrict their scalability and adaptability into the high-volume IoT spectrum in real-world scenarios.

To address these limitations, deep learning (DL) has recently emerged as a powerful alternative to MLB methods for AMC. DL models can eficiently learn distinguishing AMC characteristics from received IQ signals without requiring manual feature engineering while achieving state-of-the-art classification accuracy [3], [11], [12], [13], [14]. As a result, they provide a promising alternative to MLB approaches to meet the demands of overcrowded next-generation cellular networks. However, despite their success, DL models exhibit a critical limitation. Specifically, DL-based AMC systems are frequently overconfident [15] in their predictions, even when they are incorrect, and often lack robust mechanisms for uncertainty quantification (UQ) to characterize the confidence associated with a given prediction. This overconfidence can result in significant performance degradations during deployment, particularly on incorrect predictions, when the model encounters previously unseen signal environments. Such overconfidence is further exacerbated in mission-critical settings, where decisions must be made under uncertainty, including low signal-to-noise ratio (SNR) conditions and adversarial scenarios [16], [17].

To address these challenges, we propose a UQ framework for AMC based on an ensemble of convolutional neural networks (CNNs), which generate predictive distributions, as opposed to point estimates produced by current stateof-the-art CNNs, whose statistical characteristics quantify the uncertainty associated with each prediction. Building on ensemble learning techniques [18], [19], [20], [21], [22], our approach provides calibrated uncertainty estimates, thereby enhancing reliability and robustness of current DL-based AMC frameworks. Compared with traditional UQ methods such as Bayesian neural networks (BNNs) [23], our proposed framework ofers superior performance with lower computational overhead. Specifically, our method achieves higher classification accuracy in multiple signal environments, demonstrates better performance on multiple UQ metrics, and displays enhanced resilience on out of distribution (OOD) samples such as adversarial examples [24], [25], [26]. Moreover, our ensemble-based approach is scalable to large-parameter architectures such as ResNet [27], enabling existing DLbased AMC frameworks to improve their performance while simultaneously incorporating UQ for increased robustness.

To our knowledge, this is the first work to evaluate the eficacy of deep ensembles for AMC. While ensemble techniques have been used in DL, their application in AMC poses unique challenges due to domain-specific distortions (e.g., dynamic SNR [11] and adversarial AMC conditions [24]), and our results demonstrate that equal-weighted ensembles outperform more complex methods such as BNNs and SNR-aware weighted ensembles in both classification and uncertainty estimation.

Our specific contributions of this work can be summarized as follows.

1) Deep Ensemble Framework for AMC: We develop a robust-ensemble-based AMC framework comprising multiple CNNs. To the best of our knowledge, this is the first ensemble-based DL UQ framework for AMC.

2) UQ Characterization in AMC: For the first time, we develop UQ metrics that characterize the uncertainty associated with each received signal’s modulation prediction. In comparison to other considered baselines, under a range of UQ metrics, we show that our method demonstrates significantly higher robustness by consistently scoring higher on these metrics.

3) OOD Testing: We test our framework on OOD samples, via adversarial perturbations, and show improved resistance to these perturbations, highlighting its UQ capability on shifted signal distributions.

The remainder of this article is organized as follows. Section II reviews related work on DL-based AMC including uncertainty estimation in AMC, the robustness of ensemble learning, and recent expansions of UQ in AMC. Section III outlines our methodology, detailing the signal modeling process, ensemble modeling, estimation metrics, and the characterization of OOD samples. Section IV describes our experimental setup, presents UQ scoring and estimation results, and evaluates OOD performance. Finally, we close with concluding thoughts and future directions in Section V.

## II. RELATED WORKS

Earlier methods for AMC relied on likelihood methods [7], [9], [10], which provided theoretical guarantees and uncertainty estimation. However, such methods incur computational ineficiency in large-scale networks, making them dificult to adopt in the increasingly congested wireless spectrum. DL, as an alternative to MLB approaches, has gained significant attention for AMC due to its state-of-the-art classification performance and significantly lower inference latencies compared with MLB approaches. In this regard, various neural network architectures have been explored such as CNNs [3], [4], [28], [29], recurrent neural networks (RNNs) [30], [31], [32], and long short-term memory (LSTM) [33]. By learning hierarchical features directly from raw signals, these DL approaches, in addition to having low online latencies, often excel in AMC classification tasks with little to no need for feature engineering. However, while prior studies have demonstrated the eficiency of DL compared with MLB approaches for AMC, less attention has been given to the UQ capabilities of these methods, which is the focus of our work.

More recently, BNNs [34] have been proposed to perform DL-based AMC with UQ capabilities. Although BNNs seemingly provide the advantage of both the high classification performance of DL and UQ capabilities, their practical application is hindered by lower classification performance compared with state-of-the-art CNNs. Despite their ability to capture predictive distribution and variance, which aids in uncertainty estimation, BNNs often have significantly lower classification performance compared with CNNs for AMC. This gap in performance and adaptability motivates our development of ensemble-based UQ methods for AMC.

Ensemble learning has emerged as a compelling alternative to BNNs in multiple domains, such as image processing [19] and bioinformatics [35], where multiple models are jointly analyzed. Compared with single models, deep ensembles yield superior classification performance [36] and generate predictive distributions instead of point estimates, leading to well-calibrated UQ estimates [19], [21], [37]. In addition, deep ensembles have demonstrated higher classification accuracy in the presence of data distortions such as OOD samples, which have been shown to limit the eficacy of DL-based AMC methods [24], [25], [26].

Despite these successes in various other domains, the use of ensemble learning for UQ in AMC, or for signal processing tasks in general, remains unexplored. In this work, we leverage ensemble-based methods to demonstrate their efectiveness in quantifying uncertainty in AMC. Our framework not only achieves robust performance across a range of modulation types but also is scalable to state-of-the-art DL models, highlighting its adaptability in existing DL-based AMC frameworks.

## III. METHODOLOGY

In this section, we develop our deep-ensemble-based AMC framework and describe the metrics used to quantify the uncertainty of each model. We begin by discussing our AMC signal model in Section III-A. We then present our deep ensemble approach in Section III-B and its complexity analysis in Section III-C. Subsequently, Section III-D details the estimation metrics used to evaluate the performance of diferent methods. Finally, Section III-E discusses our approach for analyzing OOD AMC signals.

## A. Signal Modeling

In our considered wireless communication environment, a transmitter transmits $\mathbf { s } = [ s [ 0 ] , \ldots , s [ \ell - 1 ] ]$ through a channel $\textbf { h } \in \mathbb { C } ^ { \ell }$ , where $\textbf { h } = \ [ h [ 0 ] , \dots , h [ \ell - \ 1 ] ] ^ { T }$ captures radio imperfections and selective fading and denotes the length of the received signal’s observation window. We model the received signal as follows:

$$
\mathbf { r } = { \sqrt { \rho } } \mathbf { H } \mathbf { s } + \mathbf { n }\tag{1}
$$

where $\mathbf { H } = \mathrm { d i a g } \{ h [ 0 ] , \ldots , h [ \ell - 1 ] \} \in { \mathbb { C } } ^ { \ell \times \ell } , { \mathbf { n } } \in { \mathbb { C } } ^ { \ell }$ represents the additive white Gaussian noise $( \mathrm { A W G N } )$ , and $\rho$ denotes <sup>ρ</sup>the SNR of the received signal. Furthermore, we map each received baseband signal to a 2-D real matrix, $\mathbf { r } \in \mathbb { C } ^ { \ell } \to \mathbf { r }$ ∈ $\mathbb { R } ^ { \ell \times 2 }$ where the first and second columns of r represent the IQ components, respectively, of r for compatibility with realvalued neural networks.

The receiver aims to perform AMC by calculating argma $\ell _ { i } P ( m _ { i } | \mathbf { r } , \theta ) .$ , where parameterizes the model used to calculate the AMC probability (further discussed in Section III-B), $m _ { i } \in { \mathcal { M } } ,$ and $\mathcal { M } = \{ m _ { 1 } , . . . , m _ { C } \}$ represents the set of considered modulation constellations. We assume that the receiver uses $\mathcal { X } _ { \mathrm { t r } } ~ = ~ \{ { \bf r } ( n ) , { \bf y } ( n ) ; n ~ = ~ 1 , \ldots , N \}$ and $\begin{array} { r l } { \mathcal { X } _ { \mathrm { t e } } } & { { } = } \end{array}$ $\{ \mathbf { r } ( t ) , \mathbf { y } ( t ) ; t \ = \ 1 , . . . , T \}$ as the training and testing datasets, respectively, where $\mathcal { X } _ { \mathrm { t r } } \cap \mathcal { X } _ { \mathrm { t e } } = \emptyset$

## B. Ensemble Modeling

Data-driven AMC models, alone, cannot efectively characterize the uncertainty associated with their predictions because they tend to produce overconfident outputs. To address this limitation, we adopt an ensemble modeling approach consisting of multiple state-of-the-art DL AMC classifiers [38]. Unlike a standalone model, ensemble predictions cannot be obtained directly because multiple models are used simultaneously. To ensure diversity in predictions, each classifier is initialized with random parameters while maintaining the same architecture, resulting in each model converging to diferent local minima thus ensuring parallelized training and diverse predictions despite training on the same dataset [18]. As a result, the ensemble exhibits variability, yielding varying levels of confidence on samples that are known to be dificult for DL classifiers to operate on such as low SNR signals. As a result, analyzing the joint output prediction from each classifier in the ensemble simultaneously improves the UQ of the model.

We denote our ensemble as $\theta = \{ \theta _ { b } \} _ { b = 1 } ^ { B }$ where B denotes the number of classifiers in the ensemble and $\theta _ { b }$ parameterizes the bth model. Each AMC classifier in the ensemble is a DL model with a softmax output. We denote each DL classifier as $f _ { \theta _ { b } } ( \mathbf { r } ) \ : \ \mathbb { R } ^ { \ell \times 2 } \ \to \ \mathbb { R } ^ { C } .$ , parameterized by $\theta _ { b } .$ . Here, the bth model aims to map the received signal $\mathbf { r } \in \mathbb { R } ^ { \ell \times 2 }$ to a modulation constellation $\mathbf { y } \in \mathbb { R } ^ { C }$ , where $C = | { \mathcal { M } } |$ represents the total number of possible modulation constellations. Due to the softmax classifier, $f _ { \theta _ { b } } ( { \bf r } )$ outputs $\hat { \mathbf { y } } ^ { ( b ) } ~ \in ~ \mathbb { R } ^ { C }$ , where $\hat { \mathbf { y } } _ { i } ^ { ( b ) } = P ( m _ { i } | \mathbf { r } , \theta ^ { ( b ) } ) \in \mathbb { R } \mathrm { ~ ( i . e . , ~ } \hat { \mathbf { y } } _ { i } ^ { ( b ) }$ is the ith element of $\hat { \mathbf { y } } ^ { ( b ) }$ and denotes the probability assigned by the bth classifier that the input r is modulated according to constellation $m _ { i } )$ . We train each AMC classifier in the ensemble by optimizing

$$
\operatorname* { m i n } _ { \boldsymbol { \theta _ { b } } } \mathcal { L } \left( \boldsymbol { \theta _ { b } } , \mathbf { r } , \mathbf { y } \right)\tag{2}
$$

where

$$
\mathcal { L } \left( \boldsymbol { \theta } _ { b } , \mathbf { r } , \mathbf { y } \right) = - \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \sum _ { j = 1 } ^ { C } { \mathbf { y } _ { i j } \log \left( \hat { \mathbf { y } } _ { i j } \right) }\tag{3}
$$

${ \bf y } _ { i j } \in \mathbb { R }$ is the jth element of $\mathbf { y } \in \mathbb { R } ^ { C }$ corresponding to the ith signal, and $\hat { \mathbf { y } } _ { i j } \in \mathbb { R }$ is the jth element of $\hat { \mathbf { y } } \in \mathbb { R } ^ { C }$ , the predicted label, corresponding to the ith signal.

During evaluation, we jointly analyze the prediction from all B classifiers in the ensemble to obtain

$$
P \left( m _ { i } | \mathbf { r } , \theta \right) = \frac { 1 } { B } \sum _ { b = 1 } ^ { B } P \left( m _ { i } \Big | \mathbf { r } , \theta ^ { ( b ) } \right)\tag{4}
$$

where argmax $. P ( m _ { i } | \mathbf { r } , \theta )$ yields the predicted modulation constellation from the ensemble. In addition to obtaining the probability with which the input belongs to a particular modulation classification, we use the distributive estimate produced by the ensemble to characterize additional UQ metrics, which are discussed in Section III-D.

## C. Complexity Analysis

Here, we analyze the computational complexity of our proposed framework during inference. The computational complexity of a single layer, $l ,$ of a CNN during runtime is given by $\mathrm { ~  ~ { ~ \cal ~ O } ~ } ( \boldsymbol { C } _ { \mathrm { \scriptsize { i n } } } ^ { ( l ) } \cdot \boldsymbol { C } _ { \mathrm { \scriptsize { o u t } } } ^ { \top } \cdot \dot { \boldsymbol { K } _ { w } ^ { ( l ) } } \cdot \boldsymbol { K } _ { h } ^ { ( l ) } \cdot \boldsymbol { H } ^ { ( l ) } \cdot \boldsymbol { W } ^ { ( l ) } )$ and, thus, the complexity over an entire CNN is given by the sum of these complexities, resulting in

$$
\sum _ { l = 1 } ^ { L } \mathcal { O } \left( C _ { \mathrm { i n } } ^ { ( l ) } \cdot C _ { \mathrm { o u t } } ^ { ( l ) } \cdot K _ { w } ^ { ( l ) } \cdot K _ { h } ^ { ( l ) } \cdot H ^ { ( l ) } \cdot W ^ { ( l ) } \right)\tag{5}
$$

where $L$ is the number of layers and, in each layer $l , C _ { \mathrm { i n } } ^ { ( l ) }$ is the number of input channels, $C _ { \mathrm { o u t } } ^ { ( l ) }$ is the number of output channels, $K _ { w } ^ { ( l ) }$ and $K _ { h } ^ { ( l ) }$ are the width and height of each convolutional kernel, and $H ^ { ( l ) }$ and $W ^ { ( l ) }$ represent the output spatial size. Since each CNN in our proposed framework is independent, they can process each received signal in parallel and thus operate without incurring any additional computational overhead compared with a single CNN. Thus, the computational complexity of our proposed method is given by (5). Moreover, in terms of wall clock time, each sample requires, on average, 1 ms/sample to process. Thus, our proposed framework does not incur any additional overhead in comparison to state-of-the-art DL-based AMC approaches.

## D. Estimation Metrics

Beyond obtaining the modulation classification estimate given in (4), we also use several proper UQ scoring metrics [19] to assess model performance comprehensively. In this capacity, we consider the negative log-likelihood (NLL), the Brier score, the width of the prediction’s confidence interval (CI), the coverage of the prediction, the set of high-confidence predictions, the expected calibration error (ECE), and the Kullback–Leibler (KL) divergence.

The NLL quantifies the likelihood of the predicted probabilities aligning with the true labels and is given over the entire testing set by the following equation:

$$
- \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { j = 1 } ^ { C } \mathbf { y } _ { t j } \log \left( \hat { \mathbf { y } } _ { t j } \right)\tag{6}
$$

where lower NLL values indicate that the model assigns higher confidence to the correct classes. In AMC, low NLL is important because poor model training under low SNR conditions can lead to overconfident misclassifications. Thus,

NLL serves as an indicator of probabilistic robustness under channel impairments.

Similarly, the Brier score, which measures the mean squared diference between the predicted probabilities and the actual outcomes, is computed over all samples and classes and is given by the following equation:

$$
\frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { j = 1 } ^ { C } \left( \mathbf { y } _ { t j } - \hat { \mathbf { y } } _ { t j } \right) ^ { 2 }\tag{7}
$$

where lower Brier score values indicate that the model’s probabilistic predictions are closer to ground-truth values, minimizing deviations. Unlike accuracy, the Brier score penalizes both overconfidence in incorrect predictions and underconfidence in correct predictions. In AMC systems, where prediction certainty impacts communication reliability, the Brier score provides an interpretable measure of prediction quality.

In addition, we also analyze the CI widths, which characterize the ensemble’s uncertainty in each prediction. A higher CI width indicates higher uncertainty, as the models comprising the ensemble vary to a higher degree in their predictions, whereas lower CI widths indicate lower uncertainty as the majority of models agree about the predicted modulation class. Ideally, we aim for a wide range of CI widths rather than a concentration within a narrow range, as seen with singular DL models, which indicates overconfidence. The upper and lower bounds of the CI of the tth sample belonging to the $j \mathrm { t h }$ constellation are given by the following equation:

$$
\hat { \mathbf { y } } _ { t j } \pm z _ { \alpha } \cdot \sqrt { \frac { S ^ { 2 } } { B } }\tag{8}
$$

where $z _ { \alpha }$ is the $1 - \alpha / 2$ quantile of a zero-mean unit variance Gaussian distribution, and $S ^ { 2 }$ is the variance of the predicted probability among models, and the CI width is given by computing the diference between the upper and lower bounds of (8). In AMC applications, CI widths ofer a direct measure of the ensemble’s epistemic uncertainty, resulting in a quantified interpretable measure of the confidence associated with each signal’s modulation constellation prediction.

We next calculate the coverage proportion, which evaluates the number of samples in the testing set whose true label is within the $z _ { \alpha }$ CI. In computing the coverage of the ensemble, we consider two scenarios. First, we use a strict condition, where the CI of the true class must contain one and the CI of all other classes must contain zero. This scenario strictly requires the ensemble to be certain that the predicted sample simultaneously: 1) is modulated according to the predicted class and 2) is not modulated according to any other class. Second, we relax the second condition and only require the CI of the true class to contain one and we do not consider the CIs of the other classes. This metric, in both the scenarios, quantifies the proportion of samples for which the ensemble is confident at $\mathrm { ~ a ~ } \mathit { Z } _ { \alpha }$ level that the input belongs to the predicted class. The coverage is especially helpful for understanding the ensemble’s confidence under low SNR conditions, which often is the cause of lowered classification performance in AMC applications. It is important to note that such CIs can extend beyond the [0 1] range particularly when the mean is near zero or one, indicating that the model is generally confident in its prediction about the correct class while simultaneously being confident that the sample does not belong to another class $( \mathrm { i . e . }$ the strict condition) or merely being confident in its prediction about the correct class without considering the confidence of other incorrect classes (i.e., the relaxed condition).

To explore confidence further, we define the high-confidence set to evaluate the frequency with which the ensemble is highly confident in its predictions. A high-confidence prediction occurs when argmax $_ { i } P ( m _ { i } | \mathbf { r } , \theta ) > 0 . 8$ . A high-confidence prediction indicates overconfidence, which often occurs in singular DL models, while a low-confidence prediction reflects underconfidence. Ideally, in AMC applications, the ensemble should strike a balance, avoiding both the extremes. This metric, like others previously discussed, provides a measure for model reliability during adverse channel conditions in AMC applications.

We also compute the ECE, which measures how far the model’s predicted probabilities are from the true frequency of correct predictions. The ECE is given by the following equation:

$$
\sum _ { k = 1 } ^ { K } \frac { | \zeta _ { k } | } { T } \left| \operatorname { a c c } \left( \zeta _ { k } \right) - \operatorname { c o n f } \left( \zeta _ { k } \right) \right|\tag{9}
$$

where for each bin $\zeta _ { k }$ we take the fraction of samples in that bin, $| \zeta _ { k } | / T ,$ multiply it by the absolute diference between the bin’s actual accuracy acc( <sub>k</sub>) and its average predicted confidence $\operatorname { c o n f } ( \zeta _ { k } )$ , and then sum these values over all K bins to yield the ECE. A lower ECE indicates that the model’s prediction estimates are well-calibrated to its actual accuracy.

Finally, we measure the Kullback–Leibler (KL) divergence between the one-hot true distribution $\mathbf { y } _ { t }$ and the predictive distribution $\hat { \mathbf { y } } _ { t }$ for each sample, and the KL divergence is given by the following equation:

$$
\begin{array} { r } { D _ { \mathrm { K L } } ( \mathbf { y } _ { t } \| \hat { \mathbf { y } } _ { t } ) = \displaystyle \sum _ { j = 1 } ^ { C } y _ { t j } \log ( \frac { y _ { t j } } { \hat { y } _ { t j } } ) . } \end{array}\tag{10}
$$

Here, lower KL divergence indicates that the model assigns higher probability to the true modulation class, yielding more accurate distributions. In AMC, this reflects both the confidence and correctness of probabilistic predictions under noisy channel conditions.

## E. OOD Samples

To further assess the robustness of our framework and simulate real-world environmental factors, we generate adversarial examples, denoted as $\mathbf { r } { ' } ,$ which are considered OOD samples [39]. DL AMC classifiers are highly susceptible to adversarial examples as they induce erroneous predictions, reflected in the softmax output of standalone models, particularly on high SNR signals. Although approaches to mitigate such samples have been investigated [16], [40], [41], they specifically target improving the robustness to adversarial attacks and do not consider the general UQ capabilities of the model. These samples degrade classification performance by pushing the received signal across the decision boundaries of DL models.

![](images/b3b3a09023b3a79918c3d68932cd0f7e064cdab6c24bd499cf0e735db453349a.jpg)

This phenomenon is often represented as an adversarial perturbation, $\pmb { \delta } \in \mathbb { R } ^ { \ell \times 2 }$ , which is introduced to existing samples and formulated as follows:

$$
\begin{array} { r l } & { \underset { \delta } { \operatorname* { m i n } } \ : \| \delta \| _ { \infty } } \\ & { \mathrm { s . t . } \ f _ { \theta _ { b } } \left( \mathbf { r } \right) \neq f _ { \theta _ { b } } \left( \mathbf { r } + \delta \right) } \\ & { \quad \mathbf { r } + \delta \in \mathbb { R } ^ { \ell \times 2 } } \end{array}\tag{11}
$$

where $\mathbf { r } ^ { \prime } = \mathbf { r } + { \boldsymbol { \delta } }$ represents the perturbed version of r and $\| \cdot \| _ { \infty }$ denotes the $\ell _ { \infty } .$ -norm bound of . Note that adversarial attacks using other norm bounds (e.g., the $l _ { 0 } , l _ { 1 } ,$ or $l _ { 2 }$ bound) can also be generated, but we select the $l _ { \infty }$ bound as it perturbs each sample thus helping in shift the sample away from its true distribution, which is our overall objective.

In practice, it is dificult to analytically solve (11) due to its excessive nonlinearity. Thus, solutions to (11) are approximated in practice. In this work, we use the fast gradient sign method (FGSM) [42], to approximate a solution to (11), which is given by the following equation:

$$
\mathbf { r } ^ { \prime } = \mathbf { r } + \epsilon \mathrm { s i g n } \left( \nabla _ { \mathbf { r } } \mathcal { L } \left( \theta _ { b } , \mathbf { r } , \mathbf { y } \right) \right)\tag{12}
$$

where $\epsilon = | | \delta | | _ { \propto }$ represents the $l _ { \infty }$ -bounded perturbation mag-<sup> δ</sup>nitude applied to the input samples.

We quantify the efect of the additive perturbation using the perturbation-to-noise ratio (PNR) [24]. Here, we compute the expected value of the power of the perturbation $\mathbb { E } [ \| \delta \| _ { 2 } ^ { 2 } ]$ and then obtain the expected value of the power of the received signal <sup>E</sup>[krk<sup>2</sup>]. Using these quantities, along with the SNR of the received signal, the PNR is given by the following equation:

$$
\mathrm { P N R ~ } \left[ \mathrm { d B } \right] = \frac { \mathbb { E } \left[ { \left. \delta \right. _ { 2 } ^ { 2 } } \right] } { \mathbb { E } \left[ { \left. { \bf r } \right. _ { 2 } ^ { 2 } } \right] } \left[ \mathrm { d B } \right] + \mathrm { S N R ~ } \left[ \mathrm { d B } \right]\tag{13}
$$

where a lower PNR indicates that the perturbation is less potent and has a smaller efect on the distribution shift of r, whereas a higher PNR shifts $\mathbf { r } { ' }$ further from r and is more likely to satisfy the constraints of (11).

## IV. PERFORMANCE EVALUATION

In this section, we assess the efectiveness of our proposed UQ framework for AMC. We begin by detailing our experimental setup in Section IV-A. In Section IV-B, we provide an in-depth analysis of the uncertainty estimation capabilities of our proposed framework compared with the proposed baselines. In Section IV-C, we investigate our framework’s robustness to OOD samples and adversarial perturbations, a critical consideration for deploying AMC systems in realworld, dynamic environments. Finally, in Section IV-D we provide a discussion and insights highlighting the benefits of our proposed method.

## A. Experimental Setup

We perform our empirical evaluation on two AMC datasets: RadioML2016.10a [43] and RadioML2018.01a [11]. RadioML2016.10a is a synthetic dataset generated using GNU radio while RadioML2018.01a is collected over-the-air on a wireless testbed making it a more dificult dataset but a better representation of real-world AMC data. RadioML2016.10a comprises $C \ = \ 1 1$ modulation types ranging from −10- to 20-dB SNR in increments of 2 dB. For each SNR, the dataset contains 12 000 signals, where = 128 samples in length. In comparison, RadioML2018.01a is an over-the-air dataset that contains $C = 2 4$ modulation types, ranging from −20 to 18 dB in increments of 2 dB, with each signal consisting of $\ell = 1 0 2 4$ samples and consists of 19 661 signals per SNR. Fig. 1 visualizes selected constellations used in our analysis. In each experiment, we use an 80%/20% split of the signals at each SNR to form ${ \mathcal { X } } _ { \mathrm { t r } }$ and $\mathcal { X } _ { \mathrm { t e } } . ~ \mathcal { X } _ { \mathrm { t r } }$ is used to train each classifier in the ensemble. After training, we report the UQ characteristics of the ensemble on $\mathcal { X } _ { \mathrm { t e } }$

Fig. 1. Sample modulation constellations used for AMC in our empirical evaluations including OOK (top) and 256QAM (bottom) from the RML 2018.01a dataset.  
TABLE I  
CNN ARCHITECTURE OF EACH CLASSIFIER IN OUR ENSEMBLE
<table><tr><td>Layer</td><td>Dropout Rate (%)</td><td>Activation</td><td>Shape</td></tr><tr><td>Conv 1 Conv 2 Conv 3 Conv 4 Flatten</td><td>20 20 20 20</td><td>ReLU ReLU ReLU ReLU</td><td> $3 \times 1 \times 2 5 6$   $3 \times 2 \times 1 2 8$   $3 \times 1 \times 6 4$   $3 \times 1 \times 6 4$ </td></tr></table>

Our framework uses an ensemble of B = 15 CNNs, selected for their demonstrated efectiveness in AMC tasks [29]. All the models share the same architecture, which is shown in Table I and are all independently trained on ${ \mathcal { X } } _ { \mathrm { t r } }$ by minimizing (3) using stochastic gradient descent (SGD). Each model in the ensemble is trained for 100 epochs with a batch size of 256 and a learning rate of 0.001. The hyperparameters were initially selected based on commonly used settings in the AMC literature [44], and they were further fine-tuned for our application using a grid search. Although we use the CNN architecture shown in Table I, our framework can be extended to incorporate an ensemble of classifiers with any architecture. As we will show, our ensemble of AMC classifiers consistently outperforms a standalone AMC classifier with the same architecture.

## B. Uncertainty Quantification

In this section, we examine our framework’s UQ capabilities across a range of SNRs. In addition, we compare the performance of our framework to the two most common approaches for data-driven AMC with UQ: a standalone CNN classifier [7], [9], [10] and an AMC-based BNN [34]. The CNN is a single DL classifier that provides state-ofthe-art performance but limited UQ capabilities. BNNs are another DL-based AMC framework capable of quantifying uncertainty better than standalone DL models by generating predictive distributions over point estimates, similar to our proposed ensemble, during inference. Yet, as we will show in our empirical analysis, BNNs sufer in baseline classification performance in comparison to state-of-the-art standalone DL classifiers. Furthermore, we introduce an extra baseline: an SNR-aware weighted ensemble inspired by [45], where we use an SNR-aware approach to train each model in an ensemble on a specific SNR and then calculate the weight of each model using the Shannon entropy. This approach introduces a baseline in which each model in the ensemble is trained on a unique SNR, thus distinguishing between epistemic uncertainty (model uncertainty) and aleatoric uncertainty (channel noise) in AMC tasks. Here, models with high entropy (e.g., classifiers trained on low SNR signals) are given a lower weight and models with low entropy (e.g., classifiers trained on high SNR signals) are given more weight (proportional to the Shannon entropy of each classifier). Note that although [45] does not explicitly apply a weighted ensemble to AMC, it shows the potential of a weighted ensemble to characterize aleatoric uncertainty so we adapt it for AMC as an additional baseline. Contrary to all these methods, we will see that our proposed deep ensemble framework for AMC provides both state-of-the-art classification performance and robust UQ.

Fig. 2 shows the performance of our approach in comparison to each considered baselines in terms of our considered scoring metrics. As shown in Fig. 2, our ensemble-based approach consistently outperforms a standalone CNN, the BNN, and the weighted ensemble on both the considered datasets. Notably, while the single CNN, the weighted ensemble, and our proposed ensemble exhibit relatively stable accuracy in both the datasets, the BNN’s accuracy declines sharply on the RML 2018.01a dataset—likely due to the more complex real-world signals in it compared with the GNU radio-generated data in the RML 2016.10a dataset, highlighting its limitations in AMC applications. Despite these challenges, our proposed ensemble maintains the highest overall accuracy. Similarly, Fig. 2 shows that our proposed ensemble also outperforms the standalone CNN, the BNN, and the weighted ensemble in terms of NLL, consistently achieving a lower NLL score across the entire SNR range. The BNN, in particular, consistently attains a high NLL, relative to our proposed ensemble, in both the considered datasets at each considered SNR. Finally, we see from Fig. 2 that our ensemble consistently achieves the lowest Brier scores in all considered environments, further demonstrating its robustness relative to the other considered baselines.

![](images/04ce3383f9aecaaf8d074b7a6a6ff04d486eb225c0fcf1ba6659a7e41f85ab75.jpg)

![](images/848ace657cb5109ed425fbcbb68c659715f3fcf607396d053ffa87f45cf5c7c3.jpg)

![](images/77a8ad93722e2c75c43bc53bdfb622be1549a0f6dd0b159ae84644c74b552591.jpg)

![](images/a73836a1ef202ad51aa8a6bc2b2645beffa33ee45790fbcd5de048ddba8aca10.jpg)

![](images/cc352a5e170cad03f1e880954b960646023085789812bf1700109ad8acaf57d8.jpg)

![](images/8c758dfd1210a0e56b5dfee6633da041362b1a5d508a836fd2cb2a8094dc1307.jpg)  
Fig. 2. UQ metrics on the 2016.10a (left column) and RML 2018.01a (right column) datasets. We see that our proposed ensemble model outperforms all baselines on each considered metric for both the datasets.

![](images/33036685714b9ccd20a19d728c22a7506d7f85ec7a173e4a9c1bc35d7c953409.jpg)

![](images/f2dc25966f1836c916655c2831d2f4021d5c3b0d7f666773f7d89e08c8707cee.jpg)

![](images/2bc27a0cfe01b3c97d69f56960c46c413878b676e769152d862356e58c035bfc.jpg)

![](images/15109fb89c0e741521e90a4886787cc1e221f57c2afdef3f9df907f65b0f40d3.jpg)

![](images/e1210c4d197a5185c009a70d6673aca4dae2d0f27b2e93ee28eb3a92c4e51543.jpg)

![](images/58b93dedc935c61a5779986078a6f6e7c861a1b7cb0106a449d9cacd14f70fe5.jpg)

![](images/9652d42335a8a55bb4a976dcfe6e8742155acc162f53959dbafb324556c3c66f.jpg)

![](images/c54cbaa45dea4a221d113d5fa703991746db5168538bef173faf2024a4d7d95b.jpg)

![](images/1dc5127887e2bc11a4a4f3f68be22141183fca9392236ddbb9dd79700ead79e4.jpg)  
Fig. 3. Correctly predicted CI widths of our proposed ensemble (left column), the baseline BNN approach (middle column), and the baseline weighted ensemble (right column) on RML 2018.01a. Here, we see that our ensemble has wider CI widths compared with both the baselines, demonstrating that our proposed ensemble approach can characterize uncertainty to a higher extent in comparison to the BNN and weighted ensemble.

In Fig. 3, we show the CI widths of low, medium, and high SNR values of our proposed ensemble model in comparison to BNNs and the weighted ensemble on correctly predicted signals. In this scenario, we omit results from the standalone

![](images/511626587fe71b4759c69eca75e7ed09c04c0b029c3c8aa860a516b03ea6655c.jpg)

![](images/475377355fef0a477115d1773cc6e4aabf7ab2058ee69b87b6c548ddc560c976.jpg)

![](images/a0e70bb6509070b39e6cd474fb9725e7ec984f3759125022d36f89e456929335.jpg)

![](images/b9809054775c550d8e39852aca168c7962746de8269680a58e7efd328c56329c.jpg)

![](images/9969d9f41191cf439af082d8e16de7568a0eb12ee3da6edb10f4a247b4a06fc5.jpg)

![](images/ad23e9e05a84fb5b9af9bf94201484c114556a00b5e92ffe5996107ff9e0583a.jpg)

![](images/8f4064bb59ad923440f42174b9915789bd33e8ae3adcc5eddc6e38f32ab59e16.jpg)

![](images/755aded11f5d26963e03de46400f764ca0a66e65cf34f26eb058116c2012f990.jpg)

![](images/9e9d0944b40b6a5758b2a1f8ec554e510d936ec86030578e3ca500a115beda20.jpg)  
Fig. 4. Incorrectly predicted CI widths of our proposed ensemble (left column), the baseline BNN approach (middle column), and the baseline weighted ensemble (right column) on RML 2018.01a. Similar to Fig. 3, we see here that our ensemble produces wider CI widths compared with both the baselines, demonstrating that our proposed ensemble can more efectively characterize uncertainty estimates, particularly on incorrectly predicted signals.

CNN, as they produce point predictions, resulting in CI widths of zero. From Fig. 3, we observe that at −10 dB (low SNR), the BNN exhibits a mix of narrow and moderate CI widths, suggesting some level of uncertainty in low-SNR conditions. However, as the SNR increases to 0 and 8 dB, the BNN’s CI widths shift toward smaller values, indicating greater confidence in its predictions. This behavior aligns with expectations, as higher SNR leads to cleaner input data, reducing uncertainty. The weighted ensemble, on the other hand, attains narrower widths at low SNR, where higher uncertainty expression is more crucial, and higher widths at high SNR, where higher uncertainty expression is less crucial. In contrast, our proposed ensemble model maintains a higher degree of uncertainty across all SNR levels, with wider CI widths than both the considered baselines. Moreover, as SNR increases, the ensemble also becomes more confident in its correct predictions, while still preserving some uncertainty in certain cases. Notably, our proposed ensemble achieves higher classification accuracy than the BNN and the weighted ensemble baseline (as shown in Fig. 2), despite its broader CIs. This suggests that while the ensemble model expresses more uncertainty, it does not come at the cost of accuracy. Instead, it ofers a more calibrated representation of confidence, ensuring that even in high-SNR conditions, some uncertainty is retained where appropriate.

We now turn our focus to the CI widths of low, medium, and high SNR values of our proposed ensemble model on incorrectly predicted signals. In this scenario, robust uncertainty is demonstrated with high CI widths as we would not want a model to express high confidence in a wrong AMC prediction. As shown in Fig. 4, at −10 dB, the BNN and the weighted ensemble baseline primarily produce near-zero CI widths, meaning they are overconfident even when they are incorrect. This misplaced confidence persists at higher SNRs (e.g., 0 and 8 dB), indicating that both the baselines fail to appropriately capture uncertainty in their misclassifications. In contrast, our proposed ensemble exhibits wider CI widths for incorrect predictions, suggesting that it remains more cautious, especially in low-SNR environments, where the performance of DL-based AMC classifiers is known to struggle. As the SNR increases, our proposed ensemble’s average CI width remains wide, reflecting an appropriate level of uncertainty even in moderate- to low-noise conditions. Meanwhile, the overconfidence of the other baselines remains evident across all the SNR levels, failing to distinguish between correct and incorrect predictions in terms of uncertainty representation.

![](images/1da9df2854b60d6c876c0818654ecd63116481b52b631892731b4fc481d092e3.jpg)

![](images/a59f9ee49dde664cdafc82f11c37271b0d83d4b4bc399813970e58b39ee177e5.jpg)  
Fig. 5. Coverage proportion, under strict and relaxed conditions, of our approach in comparison to each considered baseline. Here, we see that our proposed ensemble achieves a higher coverage proportion under both the strict and relaxed conditions for RML 2016.10a (left) and RML 2018.01a (right). This indicates that our proposed ensemble excels in its predictive interval, ensuring that the true class is more likely to be contained.

![](images/940b52e516754fcc4124c6111a7aefe190097dccc1418bfd8a6f089830ae2978.jpg)

![](images/e040bdaac8b8f81f6c3a06f854df2c7c4df052de17e4d2e53e13481c817aaccb.jpg)  
Fig. 6. High-confidence proportion of our proposed ensemble in comparison to each considered baseline. In both RML 2016.10a (left) and RML 2018.01a (right), our ensemble maintains a middle level between the CNN, baseline BNN, and baseline weighted ensemble indicating that our proposed ensemble is neither overconfident nor underconfident and able to strike a UQ balance compared with the other models.

Next, we assess coverage proportions in Fig. 5, which describe how well each model’s predictive intervals capture the true class. A higher coverage indicates stronger uncertainty representation. Here, we omit the coverage of the single model since it produces point estimates, which results in coverage proportions of 0. In Fig. 5, we see that the ensemble outperforms both the considered baselines, particularly surpassing the coverage proportions of BNNs. Moreover, we see this trend hold for both the strict and relaxed definitions of coverage (as defined in Section III-D), indicating that our proposed ensemble can represent, to a higher degree than each considered baseline, both its uncertainty associated with its predicted class and its uncertainty associated with its prediction that the input does not belong to any other class.

We now evaluate the high-confidence sets in Fig. 6, where we label a prediction as high-confidence if the model assigns at least an 80% probability to a particular class (as elaborated on in Section III-D). The standalone CNN leads in this category, reflecting its tendency to be overconfident. Conversely, both the BNN and the weighted ensemble baselines struggle with underconfidence, consistently producing fewer high-confidence predictions. Our proposed ensemble model strikes a balanced approach, achieving strong accuracy while also retaining suitable uncertainty, even at higher SNR levels for its high-confidence prediction, reinforcing its ability to characterize uncertainty to a higher degree in comparison to the considered baselines.

![](images/244cf7044d28f6f2c9f1411cdef3a250fbf6e10f3a584fdee0e22ff4fcd59d0b.jpg)  
Fig. 7. ECE and KL divergence of our proposed ensemble in comparison to each considered baseline on the 2016.10a (left) and 2018.01a (right) datasets. Here, we see that our proposed ensemble is able to achieve the lowest ECE and KL divergence compared with the baseline showing improved calibration.

Finally, we analyze the UQ capabilities of our framework by measuring the ECE and KL divergence. A lower ECE indicates better model calibration, and as shown in Fig. 7, our ensemble consistently achieves the smallest calibration error across all the SNR levels, whereas the BNN spikes and trails behind. Similarly, the weighted ensemble baseline exhibits a higher degree of ECE across the entire SNR range, indicating its confidence estimates are not well-calibrated to its accuracy. The same trend holds for KL divergence, where our ensemble maintains the lowest divergence from the true predictive distribution, outperforming both the standalone CNN and the BNN, and the weighted ensemble baselines showcasing more expressive and robust UQ capabilities.

In the context of AMC, it is useful to distinguish between epistemic and aleatoric uncertainty. Epistemic uncertainty arises from model limitations (e.g., insuficient training data) and can potentially be reduced by larger training sets or higher parameter models. Aleatoric uncertainty, on the other hand, stems from inherent noise in the received signals (e.g., low SNR or OOD data) and is a result of the quality of the received signals used for training. Our results shown in Figs. 2–7 demonstrate that our proposed ensemble-based framework captures both types of uncertainty: the diversity among independently trained models reflects epistemic uncertainty, while the variability in predictions across signal conditions (e.g., at low SNRs) captures aleatoric uncertainty. Compared with the BNN and weighted ensemble baselines, our method more efectively disentangles these sources, as shown by its higher CI widths on misclassified samples (epistemic) and its improved calibration under noisy conditions (aleatoric).

![](images/2b64500fcaa8ab8cbb6e5c5dc8440bcf9fd29a59a8c3e66e2493b7ac3ec7b4a2.jpg)

![](images/13319820d33da84694a76eefb6a36b6374994abc9f088008bb8f25a1aeef2d2e.jpg)

Fig. 8. Accuracy after applying a constant perturbation of 5 dB across varying SNRs on 2016.10a (left) and 2018.01a (right). The results demonstrate that under both normal and adversarial conditions, our ensemble model achieves the best performance at high and low SNR values.  
![](images/0100375d5b3c5e78091e89507cec0833f77e0d6be810ffa6f697572f371ea603.jpg)

![](images/5749ba24a4d8286062ccb68730a768406ff73a92072acbdf7c8b702d31fbfedb.jpg)  
Fig. 9. Accuracy after varying the perturbation on 10-dB SNR signals on the 2016.10a (left) and 2018.01a (right) datasets. Here, we see that our proposed ensemble is able to maintain higher performance in comparison to the considered baselines as the PNR increases and approaches the noise floor.

## C. OOD Performance

Here, we examine how our framework handles OOD scenarios by examining its efects on adversarial examples. Although they are typically below the noise floor of wireless signals, adversarial perturbations can significantly degrade the performance of neural-network-based AMC methods by inducing models to output incorrect predictions due to their underlying shifted distributions [41].

We first examine the efect of adding a constant PNR of 5 dB across the entire SNR range. Fig. 8 displays each model’s accuracy on unperturbed samples for comparison. While the ensemble and the standalone CNN show similar performance on clean signals, the ensemble significantly outperforms the CNN on OOD AMC signals. This disparity highlights the ensemble’s superior UQ capabilities in challenging signal environments. We next examine our proposed ensemble’s accuracy across increasing PNR at a constant SNR of 10 dB. As the PNR increases, the perturbed sample is shifted further from its unperturbed counterpart, thereby increasing the chance of misclassification and further shifting the distribution of the adversarial examples. Fig. 9 includes accuracies under normal (unperturbed) conditions, shown as straight lines since SNR remains constant. Here, we see that even as the PNR increases, our proposed ensemble is able to withstand the performance degradation to a greater extent than both the CNN and the BNN. Overall, these findings highlight our proposed ensemble’s ability to retain robust performance under adversarial attacks, reinforcing its ability to characterize UQ to a greater extent in comparison to the considered baselines while simultaneously striking a balance between high confidence and well-calibrated uncertainty.

## D. Discussion

Here, we examine why our proposed ensemble outperforms BNNs, which are specifically designed to deliver robust UQ. While BNNs theoretically ofer a Bayesian measure of uncertainty via their posterior distribution-based estimates, they often require unrealistic approximations that limit their ability to attain a high baseline accuracy in AMC tasks. For example, BNNs use variational inference, which by definition assumes independence between weights in the model. However, in AMC, the model operates on raw time-domain IQ samples, which are highly correlated with their nearby features. As a result, BNNs become limited from achieving state-of-the-art accuracy on AMC data as the correlation between features are highly indicative in discerning modulation type and BNNs are unable to exploit such correlations for high accuracy. In contrast, CNNs are not limited by the assumption of feature independence and, thus, ensembles of independently trained CNNs are able to exploit spatial regions of the received waveform (i.e., various portions of the time-domain signal) and are able to learn distinctive features between signals, resulting in robust uncertainty estimates through implicit posterior approximations. This makes our proposed ensemble particularly efective in comparison to BNNs, despite lacking a fully Bayesian foundation.

Furthermore, BNNs assume Gaussian priors on their weights (often with standard zero-mean, unit-variance distributions), which tends to break down for AMC as each feature in a received waveform is not necessarily Gaussian in real-world radio data, and moreover, AMC data may require more accurate assumptions on their priors to achieve high accuracy. For example, the channel distribution of received signals could difer from priors, hindering the ability of BNNs to efectively learn distinguishing features if an incorrect channel distribution assumption is made. CNNs, in contrast, require no such prior assumption on the channel distribution of received signals and are not limited to learning weights of a certain distribution, allowing more expressive power and directly allowing higher AMC performance without specific channel assumptions. Thus, ensembles of CNNs, as proposed in our framework, not only achieve higher classification performance compared with BNNs but also express uncertainty more efectively due to their stronger expressive abilities.

Finally, as shown in Figs. 2–9, our ensemble consistently outperforms the BNN baseline in both predictive accuracy and uncertainty calibration metrics (e.g., NLL and ECE). These results support the hypothesis that our proposed deepensemble-based UQ approach ofers more robust performance, even if BNNs ofer a theoretically principled approach to UQ.

## V. CONCLUSION

DL has been shown to provide cutting-edge performance in AMC. However, DL-based AMC models often exhibit overconfidence in their predictions, with no associated measure of uncertainty. This issue is especially evident in low SNR conditions and when handling OOD samples. In this work, we proposed a deep ensemble framework for AMC, which is capable of retaining the state-of-the-art performance of DL-based AMC classifiers while simultaneously providing robust UQ metrics. We demonstrated our ensemble’s ability to achieve robust performance across multiple UQ metrics such as the NLL, Brier score, prediction interval widths, prediction coverage, and high-confidence predictions. In comparison to standalone CNNs, weighted ensembles, and BNNs, we showed that our framework achieved better UQ estimates overall, particularly in low SNR and OOD environments. Moreover, our proposed framework is scalable to any DL architecture, allowing state-of-the-art performance to be extended to incorporate higher classification performance and UQ on any DL-based AMC framework. Future work will explore the resilience of our approach in more versatile environments such as the distributed AMC scenario, which requires UQ in federated learning with varying channel conditions and adversarial interference at each receiver, and in environments with insuficient channel-state information (CSI) knowledge.

## REFERENCES

[1] G. Vanhoy, N. Thurston, A. J. Burger, J. Breckenridge, and T. Bose, “Hierarchical modulation classification using deep learning,” in Proc. IEEE Mil. Commun. Conf. (MILCOM), Jun. 2018, pp. 20–25.

[2] W. H. Clark et al., “Developing RFML intuition: An automatic modulation classification architecture case study,” in Proc. IEEE Mil. Commun. Conf. (MILCOM), Nov. 2019, pp. 292–298.

[3] G. J. Mendis, J. Wei, and A. Madanayake, “Deep learning-based automated modulation classification for cognitive radio,” in Proc. IEEE Int. Conf. Commun. Syst. (ICCS), Shenzhen, China, Dec. 2016, pp. 1–6.

[4] O. Kaya, M. A. Karabulut, A. F. M. S. Shah, and H. Ilhan, “Modulation classifier based on deep learning for beyond 5G communications,” in Proc. 47th Int. Conf. Telecommun. Signal Process. (TSP), Jul. 2024, pp. 336–339.

[5] T. Huynh-The et al., “Automatic modulation classification: A deep architecture survey,” IEEE Access, vol. 9, pp. 142950–142971, 2021.

[6] J. L. Xu, W. Su, and M. Zhou, “Likelihood-ratio approaches to automatic modulation classification,” IEEE Trans. Syst., Man, Cybern., C (Appl. Rev.), vol. 41, no. 4, pp. 455–469, Jul. 2011.

[7] A. O. Abdul Salam, R. E. Sherif, S. R. Al-Araji, K. Mezher, and Q. Nasir, “A unified practical approach to modulation classification in cognitive radio using likelihood-based techniques,” in Proc. IEEE 28th Can. Conf. Electr. Comput. Eng. (CCECE), May 2015, pp. 1024–1029.

[8] M. Abu-Romoh, A. Aboutaleb, and Z. Rezki, “Automatic modulation classification using moments and likelihood maximization,” IEEE Commun. Lett., vol. 22, no. 5, pp. 938–941, May 2018.

[9] W. Wei and J. M. Mendel, “Maximum-likelihood classification for digital amplitude-phase modulations,” IEEE Trans. Commun., vol. 48, no. 2, pp. 189–193, Feb. 2000.

[10] F. Hameed, O. Dobre, and D. Popescu, “On the likelihood-based approach to modulation classification,” IEEE Trans. Wireless Commun., vol. 8, no. 12, pp. 5884–5892, Dec. 2009.

[11] T. J. O’Shea, T. Roy, and T. C. Clancy, “Over-the-air deep learning based radio signal classification,” IEEE J. Sel. Topics Signal Process., vol. 12, no. 1, pp. 168–179, Feb. 2018.

[12] T. T. An and B. M. Lee, “Robust automatic modulation classification in low signal to noise ratio,” IEEE Access, vol. 11, pp. 7860–7872, 2023.

[13] Y. Wang, J. Yang, M. Liu, and G. Gui, “LightAMC: Lightweight automatic modulation classification via deep learning and compressive sensing,” IEEE Trans. Veh. Technol., vol. 69, no. 3, pp. 3491–3495, Mar. 2020.

[14] X. Fu, G. Gui, Y. Wang, H. Gacanin, and F. Adachi, “Automatic modulation classification based on decentralized learning and ensemble learning,” IEEE Trans. Veh. Technol., vol. 71, no. 7, pp. 7942–7946, Jul. 2022.

[15] J. Moon, J. Kim, Y. Shin, and S. Hwang, “Confidence-aware learning for deep neural networks,” in Proc. Int. Conf. Mach. Learn., 2020, pp. 7034–7044.

[16] R. Sahay, D. J. Love, and C. G. Brinton, “Robust automatic modulation classification in the presence of adversarial attacks,” in Proc. 55th Annu Conf. Inf. Sci. Syst. (CISS), Mar. 2021, pp. 1–6.

[17] J. Bai et al., “A multiscale discriminative attack method for automatic modulation classification,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 294–308, 2025.

[18] R. Rahaman and A. H. Thiery, “Uncertainty quantification and deep´ ensembles,” in Proc. Adv. Neural Inf. Process. Syst., vol. 34, 2020, pp. 20063–20075.

[19] B. Lakshminarayanan, A. Pritzel, and C. Blundell, “Simple and scalable predictive uncertainty estimation using deep ensembles,” in Proc. Adv. Neural Inf. Process. Syst., 2016, pp. 6405–6416.

[20] R. Sahay, D. Ries, J. D. Zollweg, and C. G. Brinton, “Hyperspectral image target detection using deep ensembles for robust uncertainty quantification,” in Proc. 55th Asilomar Conf. Signals, Syst., Comput., Oct. 2021, pp. 1715–1719.

[21] N. Shi, F. Lai, R. Al Kontar, and M. Chowdhury, “Fed-ensemble: Ensemble models in federated learning for improved generalization and uncertainty quantification,” IEEE Trans. Autom. Sci. Eng., vol. 21, no. 3, pp. 2792–2803, Jul. 2024.

[22] G. Franchi, A. Bursuc, E. Aldea, S. Dubuisson, and I. Bloch, “One versus all for deep neural network for uncertainty (OVNNI) quantification,” IEEE Access, vol. 10, pp. 7300–7312, 2022.

[23] F. Fiedler and S. Lucia, “Improved uncertainty quantification for neural networks with Bayesian last layer,” IEEE Access, vol. 11, pp. 123149–123160, 2023.

[24] M. Sadeghi and E. G. Larsson, “Adversarial attacks on deep-learning based radio signal classification,” IEEE Wireless Commun. Lett., vol. 8, no. 1, pp. 213–216, Feb. 2019.

[25] B. Flowers, R. M. Buehrer, and W. C. Headley, “Evaluating adversarial evasion attacks in the context of wireless communications,” IEEE Trans. Inf. Forensics Security, vol. 15, pp. 1102–1113, 2020.

[26] X. Yuan, P. He, Q. Zhu, and X. Li, “Adversarial examples: Attacks and defenses for deep learning,” IEEE Trans. Neural Netw. Learn. Syst., vol. 30, no. 9, pp. 2805–2824, Sep. 2019.

[27] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2016, pp. 770–778.

[28] F. Meng, P. Chen, L. Wu, and X. Wang, “Automatic modulation classification: A deep learning enabled approach,” IEEE Trans. Veh. Technol., vol. 67, no. 11, pp. 10760–10772, Nov. 2018.

[29] A. P. Hermawan, R. R. Ginanjar, D.-S. Kim, and J.-M. Lee, “CNN-based automatic modulation classification for beyond 5G communications,” IEEE Commun. Lett., vol. 24, no. 5, pp. 1038–1041, May 2020.

[30] S. Huang et al., “Automatic modulation classification using gated recurrent residual network,” IEEE Internet Things J., vol. 7, no. 8, pp. 7795–7807, Aug. 2020.

[31] D. Hong, Z. Zhang, and X. Xu, “Automatic modulation classification using recurrent neural networks,” in Proc. 3rd IEEE Int. Conf. Comput. Commun. (ICCC), Dec. 2017, pp. 695–700.

[32] S. Hu, Y. Pei, P. P. Liang, and Y.-C. Liang, “Deep neural network for robust modulation classification under uncertain noise conditions,” IEEE Trans. Veh. Technol., vol. 69, no. 1, pp. 564–577, Jan. 2020.

[33] S. Raghunandan and S. Begaj, “Analysis of deep neural networks for automatic modulation classification,” in Proc. 40th Int. Commun. Satell. Syst. Conf. (ICSSC), vol. 2023, 2024, pp. 117–122.

[34] V.-C. Luu, J. Park, and J.-P. Hong, “Uncertainty-aware incremental automatic modulation classification with Bayesian neural network,” IEEE Internet Things J., vol. 11, no. 13, pp. 24300–24309, Jul. 2024.

[35] Y. Cao, T. A. Geddes, J. Y. H. Yang, and P. Yang, “Ensemble deep learning in bioinformatics,” Nature Mach. Intell., vol. 2, no. 9, pp. 500–508, Aug. 2020.

[36] S. Ali, S. S. Tirumala, and A. Sarrafzadeh, “Ensemble learning methods for decision making: Status and future prospects,” in Proc. Int. Conf. Mach. Learn. Cybern. (ICMLC), vol. 1, Jul. 2015, pp. 211–216.

[37] R. Sahay, J. J. Stubbs, C. G. Brinton, and G. C. Birch, “An uncertainty quantification framework for counter unmanned aircraft systems using deep ensembles,” IEEE Sensors J., vol. 22, no. 21, pp. 20896–20909, Nov. 2022.

[38] R. R. Yakkati, R. R. Yakkati, R. K. Tripathy, and L. R. Cenkeramaddi, “Radio frequency spectrum sensing by automatic modulation classification in cognitive radio system using multiscale deep CNN,” IEEE Sensors J., vol. 22, no. 1, pp. 926–938, Jan. 2022.

[39] N. Karunanayake, R. Gunawardena, S. Seneviratne, and S. Chawla, “Out-of-distribution data: An acquaintance of adversarial examples—A survey,” 2024, arXiv:2404.05219.

[40] R. Sahay, C. G. Brinton, and D. J. Love, “A deep ensemble-based wireless receiver architecture for mitigating adversarial attacks in automatic modulation classification,” IEEE Trans. Cognit. Commun. Netw., vol. 8, no. 1, pp. 71–85, Mar. 2022.

[41] P. Qi, T. Jiang, L. Wang, X. Yuan, and Z. Li, “Detection tolerant blackbox adversarial attack against automatic modulation classification with deep learning,” IEEE Trans. Rel., vol. 71, no. 2, pp. 674–686, Jun. 2022.

[42] I. J. Goodfellow, J. Shlens, and C. Szegedy, “Explaining and harnessing adversarial examples,” 2014, arXiv:1412.6572.

[43] T. O’Shea and N. West, “Radio machine learning dataset generation with gnu radio,” in Proc. GNU Radio Conf., 2016, vol. 1, no. 1, pp. 1–6.

[44] P. Ghasemzadeh, S. Banerjee, M. Hempel, and H. Sharif, “A novel deep learning and polar transformation framework for an adaptive automatic modulation classification,” IEEE Trans. Veh. Technol., vol. 69, no. 11, pp. 13243–13258, Nov. 2020.

[45] H. Wang, Y. Yu, Y. Cai, X. Chen, L. Chen, and Y. Li, “Soft-weightedaverage ensemble vehicle detection method based on single-stage and two-stage deep learning models,” IEEE Trans. Intell. Vehicles, vol. 6, no. 1, pp. 100–109, Mar. 2021.

![](images/f411e5f76c15cd9fe8974f0629c1bc13029b28195b4d9bdead4a5b92c2119e19.jpg)  
Huian Yang is currently pursuing the B.S. degree in computer engineering with the University of California, San Diego, San Diego, CA, USA.  
His research focuses on deep learning, with additional interests in embedded systems for robotics.

![](images/1435445f2bad6236ce25059afb8fa0794edca85816a3169c5a75fdbd69b4fd10.jpg)

Rajeev Sahay received the B.S. degree in electrical engineering from The University of Utah, Salt Lake City, UT, USA, in 2018, and the M.S. and Ph.D. degrees in electrical and computer engineering from Purdue University, West Lafayette, IN, USA, in 2021 and 2022, respectively.

He is a Faculty Member at the Department of Electrical and Computer Engineering, UC San Diego, San Diego, CA, USA. His research interests lie in the intersection of networking and machine learning, especially in their applications to wireless

communications and engineering education.

Dr. Sahay was a recipient of the Purdue Engineering Dean’s Teaching Fellowship and was named an Exemplary Reviewer by IEEE WIRELESS COMMUNICATIONS LETTERS.