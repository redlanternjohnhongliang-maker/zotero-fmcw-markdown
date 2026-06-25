# Improving Uncertainty of Deep Learning-based Object Classification on Radar Spectra using Label Smoothing

Kanil Patel<sup>1,2</sup>, William Beluch<sup>1</sup>, Kilian Rambach<sup>1</sup>, Michael Pfeiffer<sup>1</sup>, Bin Yang<sup>2</sup>

<sup>1</sup>Bosch Center for Artificial Intelligence, Renningen, Germany

<sup>2</sup>Institute of Signal Processing and System Theory, University of Stuttgart, Stuttgart, Germany

Abstract—Object type classification for automotive radar has greatly improved with recent deep learning (DL) solutions, however these developments have mostly focused on the classification accuracy. Before employing DL solutions in safetycritical applications, such as automated driving, an indispensable prerequisite is the accurate quantification of the classifiers’ reliability. Unfortunately, DL classifiers are characterized as black-box systems which output severely over-confident predictions, leading downstream decision-making systems to false conclusions with possibly catastrophic consequences. We find that deep radar classifiers maintain high-confidences for ambiguous, difficult samples, e.g. small objects measured at large distances, under domain shift and signal corruptions, regardless of the correctness of the predictions. The focus of this article is to learn deep radar spectra classifiers which offer robust realtime uncertainty estimates using label smoothing during training. Label smoothing is a technique of refining, or softening, the hard labels typically available in classification datasets. In this article, we exploit radar-specific know-how to define soft labels which encourage the classifiers to learn to output high-quality calibrated uncertainty estimates, thereby partially resolving the problem of over-confidence. Our investigations show how simple radar knowledge can easily be combined with complex data-driven learning algorithms to yield safe automotive radar perception.

## I. INTRODUCTION

As an important component of an automated driving system, radar sensors play a crucial role in the safe and robust perception of the environment. Recently, deep learning (DL) based solutions have shown prodigious performance in accurately classifying the object type from radar spectra in the presence of labeled data [1, 2]. However, developments have mostly focused on improving the generalization accuracy instead of the robustness, reliability or uncertainty of the predictions. As a result, softmax predictions from such high capacity models tend to be highly accurate, but poor representatives of the predictive uncertainty [3, 4]. Classifiers exhibiting such characteristics, albeit most often accurate, tend to be overconfident and have limited use in practice, as decision-making systems fail to distinguish between incorrect over-confident predictions and correct high-confident predictions [4].

Among multiple reasons behind this notorious overconfidence of DL classifiers, one fundamental reason emanates from the dataset used during training, specifically the labels [5, 6]. The labels of supervised datasets are typically one-hot label vectors (i.e. a binary label for each class) with a single ground truth class label (i.e. label vectors summing to 1). These hard labels are the most accurate representation of the true classification of an object. However, given their binary nature they provide no information of the uncertainty inherent in the data and induce an unwanted over-confidence bias in the learned predictions. Alternatively, soft labels [5] are non-binary categorical distributions which better quantify the ambiguity present in the data. In this article, we identify that the over-confidence in deep radar classifiers, which emanates from using hard labels, can be fixed using soft labels [6, 7, 8, 9] and propose two novel heuristics to compute sample-specific smoothing factors to refine the hard labels.

Sources of uncertainty in radar spectra: In radar spectra classification, even in the absence of corruptions or sensor malfunctions, there exists ambiguity in the spectra that cannot be represented with hard labels. For example, measuring the same object from 2 different distances will share the same hard label even though the measurement from farther away could be harder to classifiy. According to the radar range equation, the power measured by the receiving antennas depends, among other factors, on the amount of transmitted power, the range, and reflecting characteristics of the objects. As the power transmitted to all objects in the field-of-view remains roughly uniform, the received power is some inaccessible complex function of the range and reflecting characteristics of the object. The received power, measured in the spectra, is used by deep learning classifiers to approximate this complex function by finding features which lead to the object’s accurate classification. As the received power decreases and less classspecific information is available in the spectra, the object class becomes ambiguous, ultimately making it harder to classify as the classifiers rely on much less information. This ambiguity can increase for small, low-reflective objects or objects at large distances which reflect relatively fewer or lower power peaks. Fig. 1a visualizes parts of the range-azimuth spectra for various objects, called region-of-interest (ROI) samples, measured at varying ranges which show how both these effects control the amount of received power.

Soft labels in the radar domain: Obtaining soft-labels which accurately quantify the uncertainty of a sample can often be arduous (i.e. humans are not good at accurately quantifying uncertainty), expensive (i.e. obtaining soft labels by aggregating multiple annotator hard labels for large datasets is costly) or, at times, even impossible (i.e. human annotators are not always involved in the labeling process) to obtain. For radar spectra, it is even harder as humans are not able to easily identify objects solely based on their spectra. For smaller distant objects such as the stop sign at 35m, it is clearly visible in Fig. 1a that there is only a single small peak close to the noise floor. For such samples, the radar classifiers are tasked with the challenge of providing a prediction based on this single relatively small peak. The smaller and fewer the peaks become (e.g. stop sign at even larger distances), the harder the classification tasks becomes as a similar small peak can also be received from other small objects (e.g. pedestrian) or large objects at large distances (e.g. car at 80m). The difficulty in predicting distant samples can be observed in Fig. 1b, where we evaluate the accuracy of the Baseline (i.e. trained with hard labels) and Ours (i.e. using soft labels as presented in Sec. III) on the test set at varying distances. Additionally, we evaluate the test set corrupted with speckle noise at severity 1 (i.e. the dotted curves). We observe that overall the performance degrades at larger distances as the ROI samples become increasingly ambiguous with range.

![](images/63c2f99727fd662b8d8424459724650be7a3333e0f8f3ec0e332c3d74922161c.jpg)  
(a)

![](images/b59830a0fafd90de56d9f5de31f0d290a67346c2cc7bd1f741368bf1ae7d8cf8.jpg)  
(b)

![](images/49d9faa45e75d9563bfeddb4b2ac078bbf5409291b6179d481a6136e97db520b.jpg)  
(c)  
Fig. 1: (a) Range-Azimuth spectra samples of 5 objects each measured at 3 different distances. We highlight that the number and amplitudes of the peaks reduce for each object when measured from farther away and for a given range the total received power differs across each object. As expected, objects with large metallic components (e.g. car and motorbike) are much more reflective than pedestrians and stop signs which only have few small or no metallic components. (b) Classification accuracy of the Baseline and our soft-label classifier $( \vec { \mathrm {  ~ \ o u r s ^ { \prime } ) } }$ on the test set and the corrupted test set (speckle noise at severity 1) at varying ranges. The performance significantly degrades at larger distances with better performance seen by our label smoothing method. More information can be found in Sec. VII. (c) Average received power scatter plot of all ROI spectra and the ground truth range. We again observe the received power degrades over range and that overall some objects reflect more power than others. We also plot the average power of the Noise, which are ROI spectra where no objects were present.

Exploiting radar know-how for label smoothing: Using this observation, we exploit the range and received power of the spectra to refine the hard labels to better reflect the uncertainty or difficulty in predicting the spectra. We note that there are multiple ways to approximate the uncertainty associated with a radar spectra, though we find that using these simple measures are sufficient to significantly improve the calibration performance of the classifiers. Using other measures is a part of future works. In Fig. 1c, we plot the average received power of each region-of-interest (ROI) spectra and plot it against the range for multiple object classes for the entire dataset. It is seen that the received power greatly decreases when objects are farther away, due to the loss of power with distance, and larger objects have significantly stronger reflections. We leverage this information as a proxy to the uncertainty of the spectra to smooth the hard labels.

## II. RELATED WORK

Numerous solutions have been proposed for radar classification using point-cloud and spectra representations in the context of automated driving. The class of algorithms operating on point-cloud radar reflections, first require applying a statistical detection algorithm (e.g. CFAR [10]) followed by a clustering algorithm which attempts to group reflections from the same object. Given these clusters, classification algorithms can be applied on either the extracted hand-crafted features [11, 12, 13] or learned features [14]. The clustering step is avoided in [15, 16, 17] by directly using deep learning to yield a semantic segmentation of the point cloud. The pointcloud can also be exploited to create occupancy grids which can directly be used for classification [18, 19].

The alternative spectra representation is a result of applying a multi-dimensional FFT on the raw radar signals and produces image-like maps of the environments measuring the range, azimuth and Doppler velocity. Most learning-based tasks exploit micro-Doppler signatures of moving objects [20, 21, 22, 23], but range-azimuth maps have also been used for various tasks [24], especially for static scenes where the micro-Doppler signatures are small or non-existant [1, 2].

In deep learning, an effective technique for uncertainty estimation involves computing them from multiple forward passes via sampling or ensembles. Albeit powerful, this family of methods produce unwanted latencies which are inapt for automotive applications. Computationally efficient techniques which are better suited for real-time applications include sampling-free uncertainty estimation [25] and data augmentation [6, 9] which are employed during training. Alternatively, post-hoc calibration techniques [3, 26] improve uncertainty estimates without retraining and were applied to radar spectra in [4]. This work is orthogonal to the post-hoc calibration work presented in [4] and can be combined by applying [4] after applying the techniques presented here.

Since the pioneering work of [8] and [5], introduced to improve the generation accuracy, recently another family of methods include using soft labels during training for improving the uncertainty estimation of neural networks [6, 9, 27]. These methods involve refining the hard labels available in the supervised datasets to quantify the inherent uncertainty in the data. During the training these soft labels allow the classifier to reflect ambiguous and uncertain situations.

In this paper, we introduce two variants of a novel soft label training procedure which produces sample-specific label smoothing factors using available information such as the range of the object or the amount of received power in the spectra. We note that this is the first work applying soft labels for radar spectra classification.

## III. METHODOLOGY

We formally introduce soft labels, the concept of label smoothing [5] and the two novel techniques, called Rsmoothing and P-smoothing, presented in this work.

## A. Hard labels vs. soft labels

In a classification setting, the ground truth data distribution $P _ { * } ( x , y )$ is unknown and approximated by a finite training dataset, $D = \left\{ x _ { i } , y _ { i } \right\} _ { i = 1 } ^ { N }$ (i.e. empirical distribution $P _ { d } ( x , y ) ~ = ~ 1 / N \sum _ { ( i = 1 ) } ^ { N } \delta ( x ~ = ~ x _ { i } , y ~ = ~ y _ { i } ) )$ The empirical distribution is formed by assembling delta functions located on each example [28], with further improvements possible by replacing them with some density estimate of the vicinity [29]. Using expert domain knowledge, the vicinity around the data can be defined for further sample and label generation. Even though sample generation, known as data augmentation, is commonly performed, the labels $y$ are often left unchanged. For a C-class classification problem, these labels y are hard estimates (i.e. one-hot encodings: $y \in \{ y ^ { \prime } $ $y ^ { \prime } \in \{ 0 , 1 \} ^ { C } , 1 ^ { T } y ^ { \prime } = 1 \} )$ ) of the true conditional distribution $P _ { * } ( y | x )$ . Training with hard labels has the adverse effect of producing over-confident classifiers as they are solely trained on zero-entropy labels [6], therefore penalizing any sign of uncertainty reflected in the predictions. These predictions also tend to be highly mis-calibrated [3, 26] as the training loss tends to encourage fully confident predictions, regardless of their correctness.

An alternative, which can better reflect the true confidences for each class, is obtained by using (non-binary) soft labels (i.e. $y \in \{ y ^ { \prime } : y ^ { \prime } \in \left[ 0 , 1 \right] ^ { C } , 1 ^ { T } { y ^ { \prime } } ^ { \cdot } = 1 \} )$ . Soft labels have the capacity to discourage over-confidence by assigning lower confidences for ambiguous and uncertain samples, though at the same time maintaining the true class label information. An open problem which remains in the literature is the acquisition of these soft labels as it is often difficult to quantify uncertainty. One simple, yet effective, approach is to uniformly smooth all labels in the dataset but does not consider any class or input specific information. In this work, we aim to introduce two techniques for acquiring soft labels for radar spectra to improve the uncertainty of the trained classifiers.

## B. Label smoothing

In the pioneering work of label smoothing [5], the authors use a fixed value ǫ to smooth all hard labels, called ǫ- smoothing. ǫ-smoothing can be seen as a mixture between the hard labels y and the class prior distribution over labels υ, with weights $1 - \epsilon$ and ǫ, respectively. The resulting labels regularize the training procedure and partially address the issue of over-confidence for smoothing values even as small as $0 . 0 1 \mathrm { ~ - ~ } 0 . 1$ . However, this approach is agnostic to the ambiguity or uncertainty inherently present in each sample. More formally, the label $y$ is smoothed to

$$
\begin{array} { r } { \tilde { y } = ( 1 - \epsilon ) y + \epsilon v , } \end{array}\tag{1}
$$

where the value of ǫ determines the amount of smoothing. Compared to assigning ǫ to a small fixed value (with best validation set performance achieved using $\epsilon = 0 . 1 \ [ 5 ] )$ , we propose to use an adaptive ǫ for each sample for further calibration performance gains.

C. Estimating soft labels for radar spectra: R-smoothing and P-smoothing

Building on the label smoothing technique, we propose Rsmoothing, which uses the range R of the object to determine the value of ǫ,

$$
\epsilon _ { R } = 1 - e ^ { - \alpha \frac { R - r _ { \mathrm { m i n } } } { r _ { \mathrm { m a x } } - r _ { \mathrm { m i n } } } } ,\tag{2}
$$

where $\alpha > 0$ controls the smoothing factor, $r _ { \mathrm { m i n } }$ and $r _ { \mathrm { m a x } }$ are the minimum and maximum range values for training samples and are used to normalize the range to [0, 1]. This smoothing technique will assign lower confidences (i.e. larger $\epsilon )$ for objects farther away, which are known to pose a greater challenge in determining its classification (see Fig. 1b) due to the reduced information present in the spectra (see Fig. 1c). However, we note that this smoothing is agnostic to the object class and smoothes each objects’ label uniformly, without leveraging any input or object specific information.

To address this, we additionally propose P-smoothing, which uses the average received power of the spectra sample $\begin{array} { r } { \pi ( x ) = \frac { 1 } { P } \sum _ { p = 1 } ^ { P } x _ { p } } \end{array}$ for the linear scale input x with P pixels to determine the smoothing factor ǫ,

$$
\epsilon _ { \pi } = 1 - e ^ { - \alpha \left( 1 - \frac { \pi ( x ) - \pi _ { \operatorname* { m i n } } } { \pi _ { \operatorname* { m a x } } - \pi _ { \operatorname* { m i n } } } \right) } ,\tag{3}
$$

where $\alpha > 0$ controls the smoothing factor, $\pi _ { \mathrm { m i n } }$ and $\pi _ { \mathrm { m a x } }$ are the minimum and maximum average power for spectra samples in the training dataset. In order to ensure that the soft labels still assign more than 50% to the ground truth class, we bound the hyper-parameter α by $0 < \alpha < - \log _ { e } 0 . 5$ . As the spectra of highly reflective objects will contain more received power and signal information, their labels will have smaller ǫ, indicating lower uncertainty. The distribution of the average power measured across range can be seen in Fig. 1c. The average power has been used in [30] as a measure to filter out noisy samples to clean the training dataset. However, instead of using this measure as a filter to remove (noisy) samples, we propose to use it to determine the degree to which the hard labels should be smoothed. This allows the classifier to still learn from these noisy samples, but is encouraged to assign them significantly lower confidences.

## IV. EXPERIMENTAL SETUP

Dataset: We use the same measurement framework and radar sensor as described in [1] to measure, pre-process, label, and extract the regions-of-interests (ROIs) from radar spectra. We also use the two static scene datasets introduced in [4] (now including objects up to 43m in range instead of the previous 30m) which consist of the following seven objects: car, construction barrier, motorbike, baby carriage, bicycle, pedestrian, and stop sign. These objects are measured by an ego-vehicle driving through the static scene in different driving patterns. Using a similar setup, we additionally create a new test set, Env3-Test, which consists of a novel scene and driving pattern. Env3-Test only consists of driving patterns which drive straight towards the objects in the scene. All datasets differ in the measured scenes, driving patterns, object instances and viewing angles. Each dataset consists of 414281, 49726 and 355544 data samples for Env1, Env2-Test and Env3- Test, respectively, where only part of Env1 is used during the training and validation phase. Env2-Test and Env3-Test are used for an unseen evaluation of the performance.

Training: We use the same architecture and training procedures as described in [4]. We select the classifier with the best accuracy only using a split of Env1 and evaluate the performance on the unseen test datasets: Env2-Test and Env3- Test. We train 10 independent classifiers and report their mean and standard deviations for all experiments. We used a heldout validation set to determine the hyper-parameters of each method, yielding the best accuracy performance using $\epsilon = 0 . 1$ for ǫ-smoothing and $\alpha = 0 . 5$ for R- and P-smoothing.

Uncertainty Metrics: The quality of the confidence estimates can be evaluated using the Expected Calibration Error (ECE) [3] and Mean Maximal Confidence (MMC). The ECE gives an indication of the correctness of the confidence estimates. This is calculated by grouping predicted samples into discrete bins b. More formally, ECE is computed as:

$$
\mathrm { E C E } = \sum _ { r = 1 } ^ { N _ { B } } \frac { N _ { b } } { N } | \mathrm { a c c u r a c y } ( b ) - \mathrm { c o n f i d e n c e } ( b ) | ,\tag{4}
$$

for N samples, $N _ { B }$ bins, $N _ { b }$ samples in bin $b ,$ and the calibration range b is defined by the $[ N / N _ { B } ] ^ { \mathrm { t h } }$ index of the sorted predicted confidences.

The MMC is the mean confidence across a set of samples, with the confidence being the maximum predicted class probability. We examine the MMC of correct vs. incorrect classifications, for which we wish the former set to have a high MMC, and the latter sets to have a low MMC. More details on the ECE and MMC can be found in [4].

![](images/860793dd100feb8e0e239d8fb60eaf6a70ffa8c16c40de1ebab2927061ca411f.jpg)  
(a) Env2-Test

![](images/542dfcdbf40c15cced1b615b899e9003381f22555a67ec922d763b95e6c68a44.jpg)  
(b) Env3-Test  
Fig. 2: Reliability diagrams of the Baseline and label smoothing methods for (a) Env2-Test and (b) Env3-Test. Using soft labels instead of the hard labels (i.e. Baseline) greatly improves the confidence calibration. Among these, overall Psmoothing shows the best calibration performance.

## V. UNCERTAINTY CALIBRATION

In Fig. 2, we plot the reliability diagrams of all methods evaluated on the two test sets. A classifier has perfect calibration when its predictive confidences match the accuracy (i.e. the black dashed diagonal line), and is over-confident (under-confident) when below (above) this line. The severe over-confidence of the Baseline can be seen by the skewness of the curve to the right and the largest distance to the ideal calibration curve. We observe that all label smoothing methods improve the calibration performance and that R-smoothing and P-smoothing perform best. As this is merely a qualitative evaluation to visually compare the calibration performance, in the next section we provide more quantitative evaluations.

## VI. QUANTITATIVE EVALUATIONS OF ALL METRICS

In Tab. I, we quantitatively evaluate the Accuracy, ECE and MMC on the test sets, Env2-Test and Env3-Test. We observe that all label smoothing methods improve the Baseline across all metrics, with the best performance seen with Rsmoothing and P-smoothing. Even though the soft labels used by R-/P-smoothing were designed to improve the calibration performance and address the issues of over-confidence, we also observe an accuracy improvement. In addition to significantly improving the calibration performance, the classifiers are also less over-confident on the incorrectly classified samples (i.e. lower $\mathbf { M M C } _ { \mathrm { { i n c } } } { \mathrm { v a l u e s } } )$ . This shows that the classifiers generalize better when using the modified soft labels instead of the ground truth hard labels.

## VII. STUDY OF THE PERFORMANCE OVER OBJECT RANGE

Both R- and P-smoothing were designed to improve the performance of the classifiers at larger range by lowering the confidences of the labels for these spectra. We now study if this goal has been achieved. In order to study the influence of the training methods over range, we create subsets, using 5m thresholds from 10m up to 40m, of the test sets and evaluate the ECE and $\mathbf { M M C } _ { \mathrm { i n c } }$ in Fig. 3.

We find that using the smoothing methods which considers the uncertainty associated with the spectra to smoothen the hard labels, provide better calibrated outputs, especially at larger distances. Unlike the Baseline and ǫ-smoothing, which becomes significantly worse at ECE at larger distances, the calibration performance of R-/P-smoothing stay roughly constant at all ranges. As depicted in Fig. 1b, the accuracy of all classifiers become significantly worse at larger ranges, therefore it is crucial to lower the confidence of these distant samples. We observe that R-/P-smoothing significantly reduce the confidences of the incorrect predictions at larger distances. Whereas, the Baseline and ǫ-smoothing still assign more than 50% confidence on the incorrect predictions. This result shows that the design choice of smoothing the labels of farther objects and low-power spectra significantly helps maintain calibrated predictions for uncertain samples which are predominantly found at larger ranges.

TABLE I: Quantitative evaluation of the Baseline and label smoothing methods on Accuracy, ECE, and $\mathbf { M M C } _ { \mathrm { i n c } }$
<table><tr><td rowspan=1 colspan=1>Method</td><td rowspan=1 colspan=1>Acc ↑        ECE↓       $\mathbf { M M C _ { \mathrm { i n c } } } \downarrow$ </td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\mathrm { E n v { 2 - } T e s t }$ </td></tr><tr><td rowspan=2 colspan=1>Baseline€-smooth.</td><td rowspan=1 colspan=1> $5 2 . 5 0 \pm 0 . 3 2$    $0 . 2 2 7 \pm 0 . 0 3$    $0 . 6 6 6 \pm 0 . 0 3$ </td></tr><tr><td rowspan=1 colspan=1> $5 3 . 0 5 \pm 0 . 3 4$    $0 . 1 0 8 \pm 0 . 0 1$     $0 . 5 5 3 \pm 0 . 0 1$ </td></tr><tr><td rowspan=2 colspan=1>R-smooth.P-smooth.</td><td rowspan=1 colspan=1> $5 3 . 1 5 \pm 0 . 4 8$    $0 . 0 4 8 \pm 0 . 0 1$     $0 . 4 8 6 \pm 0 . 0 1$ </td></tr><tr><td rowspan=1 colspan=1> ${ \pm 3 . 5 0 \pm 0 . 6 1 }$    ${ \bf 0 . 0 3 6 } \pm 0 . 0 0$    $\mathbf { 0 . 4 5 2 \pm 0 . 0 1 }$ </td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> ${ \mathrm { E n v } } 3 { \mathrm { - } } { \mathrm { T e s t } }$ </td></tr><tr><td rowspan=1 colspan=1>Baseline</td><td rowspan=1 colspan=1> $5 7 . 0 5 \pm 0 . 2 7$    $0 . 1 9 1 \pm 0 . 0 2$    $0 . 6 7 1 \pm 0 . 0 2$ </td></tr><tr><td rowspan=1 colspan=1>€-smooth.</td><td rowspan=1 colspan=1> $5 7 . 3 5 \pm 0 . 2 1$    $0 . 1 0 2 \pm 0 . 0 1$    $0 . 5 7 9 \pm 0 . 0 1$ </td></tr><tr><td rowspan=1 colspan=1>R-smooth.</td><td rowspan=1 colspan=1> ${ \pm 7 . 7 8 \pm 0 . 3 6 }$    $\mathbf { 0 . 0 3 3 } \pm 0 . 0 0$    $0 . 4 7 8 \pm 0 . 0 1$ </td></tr><tr><td rowspan=1 colspan=1>P-smooth.</td><td rowspan=1 colspan=1> $5 7 . 4 0 \pm 0 . 4 0$    $\mathbf { 0 . 0 3 3 } \pm 0 . 0 0$    ${ \bf 0 . 4 6 7 \pm 0 . 0 1 }$ </td></tr></table>

![](images/e3d35a44a732a3cc85ef84ba1e48a6f0742ba2ec8915a299a0f02345efc9020a.jpg)

![](images/afad52ab81e46480ac82b98c0134503baba3e93fd1b3ad7138378cd7614aba8f.jpg)  
Fig. 3: Performance over range of all training methods on Env2-Test. Creating subsets by grouping objects at similar distances to the sensor, we evaluate the ECE and $\mathbf { M M C } _ { \mathrm { i n c } } .$ As expected, all methods perform worse at both metrics at larger distances with the best performance seen by R-/P-smoothing.

## VIII. SPECTRA CORRUPTIONS

In Fig. 4, we study the ECE and MMC of the classifiers to unseen dataset shifts. We use the same synthetic spectra corruptions introduced in [4] to corrupt the test sets. We average the metrics for all 7 corruption types across the 3 severities. The Baseline accuracies at these 3 severities are 50.1%, 33.2% and 23.8% . As the corruptions become more severe, the ECE increases with the worst performance showed by the Baseline. This is explained by the consistently high MMC of the Baseline as it fails to reduce its predicted confidences even though it becomes increasingly inaccurate with higher severities. In summary, using soft labels greatly helps remedy the over-confidence on mis-classified samples, which becomes significantly worse under dataset distribution shifts. The best performance is again observed by P-smoothing.

![](images/31151e03e7ca3801cb484b0c890aab95b5b21d851db4372db8f026accb4c77e7.jpg)  
(a)

![](images/000b003fe684d920989fa01cb4f8e67bfaaf8d778c697e73c782766a779bf1b9.jpg)  
(b)  
Fig. 4: Boxplot visualizations of (a) ECE and (b) MMC evaluated on corrupted spectra samples from Env2-Test. As expected, all ECEs become worse with higher severity and the label smoothing methods improve the calibration performance with best performance seen by P-smoothing. We also observe that the Baseline method keeps its average predicted confidences (i.e. MMC) roughly the same even though the classifiers are increasingly inaccurate and unfamiliar with the high severity corruptions. All corruptions have been averaged out per severity. Hatched boxes indicate the best performance.

## IX. CONCLUSION

In an attempt to improve the calibration performance of radar classifiers, we proposed to incorporate label smoothing during training. We developed two new techniques for producing soft labels using the range R and average received power P, which correlate with the underlying uncertainty inherent in the spectra. This was the first work aiming to improve the predictive uncertainty quality for radar classifiers during the training process. We find that the presented label smoothing methods achieve this goal and greatly improve the calibration performance of the classifiers. In addition, as a side effect of addressing the mis-calibration and over-confidence issues of deep learning classifiers, we also observe consistent generalization performance gains. As a result, R-/P-smoothing both produced more reliable and accurate classifiers, enabling better integration of such deep learning classifiers into real-world systems that rely on the predictive uncertainties to perform downstream actions. This work has shown that deep learning classifiers, which have the power of learning complex features from data, highly benefit from radar-specific knowledge and that further improvements can be made by tailoring learning algorithms to leverage this knowledge. A future research directions for improving the performance of the radar classifiers is intervening during the training epochs to improve the uncertainty and generalization performance by incorporating even more radar specific knowledge. The classifiers tend to focus on learning easy discriminative features in the data; thus, developing new ways to guide the model capacity to learn more complex and challenging features seems to be a promising direction.

[1] K. Patel, K. Rambach, T. Visentin, D. Rusev, M. Pfeiffer, and B. Yang, “Deep learning-based object classification on automotive radar spectra,” in IEEE Radar Conference, 2019.

[2] M. Sheeny, A. Wallace, and S. Wang, “Radio: Parameterized generative radar data augmentation for small datasets,” Applied Sciences, 2020.

[3] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On calibration of modern neural networks,” in International Conference on Machine Learning, 2017.

[4] K. Patel, W. Beluch, K. Rambach, A.-E. Cozma, M. Pfeiffer, and B. Yang, “Investigation of uncertainty of deep learning-based object classification on radar spectra.” in IEEE Radar Conference, 2021.

[5] C. Szegedy, V. Vanhoucke, S. Ioffe, J. Shlens, and Z. Wojna, “Rethinking the inception architecture for computer vision,” in IEEE Computer Vision and Pattern Recognition, 2016.

[6] K. Patel, W. Beluch, D. Zhang, M. Pfeiffer, and B. Yang, “On-manifold adversarial data augmentation improves uncertainty calibration,” in International Conference on Pattern Recognition, 2020.

[7] R. Mueller, S. Kornblith, and G. E. Hinton, “When does label smoothing help?” in Neural Information Processing Systems, 2019.

[8] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” in NIPS Deep Learning and Representation Learning Workshop, 2015.

[9] S. Thulasidasan, G. Chennupati, J. Bilmes, T. Bhattacharya, and S. Michalak, “On mixup training: Improved calibration and predictive uncertainty for deep neural networks,” Neural Information Processing Systems, 2019.

[10] H. Rohling, “Ordered Statistic CFAR technique - an overview,” in International Radar Symposium, Sep. 2011.

[11] Z. Zhao, Y. Song, F. Cui, J. Zhu, C. Song, Z. Xu, and K. Ding, “Point cloud features-based kernel svm for human-vehicle classification in millimeter wave radar,” 2020.

[12] R. Prophet, J. Martinez, J. F. Michel, R. Ebelt, I. Weber, and M. Vossiek, “Instantaneous ghost detection identification in automotive scenarios,” in 2019 IEEE Radar Conference, 2019.

[13] R. Dube, M. Hahn, M. Schutz, J. Dickmann, and D. Gin-´ gras, “Detection of parked vehicles from a radar based occupancy grid,” in IEEE Intelligent Vehicles Symposium Proceedings, 2014.

[14] M. Ulrich, C. Glaeser, and F. Timm, “Deepreflecs: Deep learning for automotive object classification with radar reflections,” in IEEE Radar Conference, 2021.

[15] F. Kraus, N. Scheiner, W. Ritter, and K. Dietmayer, “Using machine learning to detect ghost images in automotive radar,” arXiv, 2020.

[16] Z. Feng, S. Zhang, M. Kunert, and W. Wiesbeck, “Point cloud segmentation with a high-resolution automotive

radar,” in AmE 2019-Automotive meets Electronics; 10th GMM-Symposium. VDE, 2019.

[17] O. Schumann, M. Hahn, J. Dickmann, and C. Wohler,¨ “Semantic segmentation on radar point clouds,” in International Conference on Information Fusion, 2018.

[18] J. Lombacher, M. Hahn, J. Dickmann, and C. Wohler,¨ “Object classification in radar using ensemble methods,” 2017.

[19] ——, “Potential of radar for static object classification using deep learning methods,” in International Conference on Microwaves for Intelligent Mobility, 2016.

[20] A. Palffy, J. Dong, J. F. Kooij, and D. M. Gavrila, “Cnn based road user detection using the 3D radar cube,” IEEE Robotics and Automation Letters, 2020.

[21] B. Major, D. Fontijne, A. Ansari, R. Teja Sukhavasi, R. Gowaikar, M. Hamilton, S. Lee, S. Grzechnik, and S. Subramanian, “Vehicle detection with automotive radar using deep learning on range-azimuth-doppler tensors,” in IEEE International Conference on Computer Vision Workshops, 2019.

[22] R. Perez, F. Schubert, R. Rasshofer, and E. Biebl,´ “Single-frame vulnerable road users classification with a 77 ghz fmcw radar sensor and a convolutional neural network,” in International Radar Symposium, 2018.

[23] A. Angelov, A. Robertson, R. Murray-Smith, and F. Fioranelli, “Practical classification of different moving targets using automotive radar and deep neural networks,” IET Radar, Sonar & Navigation, 2018.

[24] Y. Wang, Z. Jiang, Y. Li, J.-N. Hwang, G. Xing, and H. Liu, “Rodnet: A real-time radar object detection network cross-supervised by camera-radar fused object 3d localization,” IEEE Journal of Selected Topics in Signal Processing, 2021.

[25] J. Postels, F. Ferroni, H. Coskun, N. Navab, and F. Tombari, “Sampling-free epistemic uncertainty estimation using approximated variance propagation,” in IEEE International Conference on Computer Vision, Oct. 2019.

[26] K. Patel, W. Beluch, B. Yang, M. Pfeiffer, and D. Zhang, “Multi-class uncertainty calibration via mutual information maximization-based binning,” in International Conference on Learning Representations, 2021.

[27] M. Hein, M. Andriushchenko, and J. Bitterwolf, “Why ReLU networks yield high-confidence predictions far away from the training data and how to mitigate the problem,” in Conference on Computer Vision and Pattern Recognition, 2019.

[28] H. Zhang, M. Cisse, Y. Dauphin, and D. Lopez-Paz,´ “mixup: Beyond empirical risk minimization,” International Conference on Learning Representations, 2018.

[29] O. Chapelle, J. Weston, L. Bottou, and V. Vapnik, “Vicinal risk minimization,” Neural Information Processing Systems, 2001.

[30] T. Visentin, “Polarimetric radar for automotive applications,” Ph.D. dissertation, Karlsruher Institut fur Tech-¨ nologie, 2019.