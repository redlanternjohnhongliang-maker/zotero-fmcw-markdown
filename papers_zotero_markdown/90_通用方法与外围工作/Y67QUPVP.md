# To Trust Or Not To Trust A Classifier

Heinrich Jiang<sup>∗</sup> Google Research heinrichj@google.com

Been Kim Google Brain beenkim@google.com

Melody Y. Guan<sup>†</sup> Stanford University mguan@stanford.edu

Maya Gupta Google Research mayagupta@google.com

## Abstract

Knowing when a classifier’s prediction can be trusted is useful in many applications and critical for safely using AI. While the bulk of the effort in machine learning research has been towards improving classifier performance, understanding when a classifier’s predictions should and should not be trusted has received far less attention. The standard approach is to use the classifier’s discriminant or confidence score; however, we show there exists an alternative that is more effective in many situations. We propose a new score, called the trust score, which measures the agreement between the classifier and a modified nearest-neighbor classifier on the testing example. We show empirically that high (low) trust scores produce surprisingly high precision at identifying correctly (incorrectly) classified examples, consistently outperforming the classifier’s confidence score as well as many other baselines. Further, under some mild distributional assumptions, we show that if the trust score for an example is high (low), the classifier will likely agree (disagree) with the Bayes-optimal classifier. Our guarantees consist of non-asymptotic rates of statistical consistency under various nonparametric settings and build on recent developments in topological data analysis.

## 1 Introduction

This work focuses on one such challenge: knowing whether a classifier’s prediction for a test example can be trusted or not. Such trust scores have practical applications. They can be directly shown to users to help them gauge whether they should trust the AI system. This is crucial when a model’s prediction influences important decisions such as a medical diagnosis, but can also be helpful even in low-stakes scenarios such as movie recommendations. Trust scores can be used to override the classifier and send the decision to a human operator, or to prioritize decisions that human operators should be making. Trust scores are also useful for monitoring classifiers to detect distribution shifts that may mean the classifier is no longer as useful as it was when deployed.

A standard approach to deciding whether to trust a classifier’s decision is to use the classifiers’ own reported confidence or score, e.g. probabilities from the softmax layer of a neural network, distance to the separating hyperplane in support vector classification, mean class probabilities for the trees in a random forest. While using a model’s own implied confidences appears reasonable, it has been shown that the raw confidence values from a classifier are poorly calibrated [24, 32]. Worse yet, even if the scores are calibrated, the ranking of the scores itself may not be reliable. In other words, a higher confidence score from the model does not necessarily imply higher probability that the classifier is correct, as shown in [45, 22, 39]. A classifier may simply not be the best judge of its own trustworthiness.

In this paper, we use a set of labeled examples (e.g. training data or validation data) to help determine a classifier’s trustworthiness for a particular testing example. First, we propose a simple procedure that reduces the training data to a high density set for each class. Then we define the trust score—the ratio between the distance from the testing sample to the nearest class different from the predicted class and the distance to the predicted class—to determine whether to trust that classifier prediction.

Experimentally, we found that the trust score better identifies correctly-classified points for low and medium-dimension feature spaces than the model itself. However, high-dimensional feature spaces were more challenging, and we demonstrate that the trust score’s utility depends on the vector space used to compute the trust score differences.

## 2 Related Work

One related line of work is that of confidence calibration, which transforms classifier outputs into values that can be interpreted as probabilities, e.g. [44, 58, 40, 24]. In recent work, [32] explore the structured prediction setting, and [33] obtain confidence estimates by using ensembles of networks. These calibration techniques typically only use the the model’s reported score (and the softmax layer in the case of a neural network) for calibration, which notably preserves the rankings of the classifier scores. Similarly, [26] considered using the softmax probabilities for the related problem of identifying misclassifications and mislabeled points.

Recent work explored estimating uncertainty for Bayesian neural networks and returning a distribution over the outputs [20, 30]. The proposed trust score does not change the network structure (nor does it assume any structure) and gives a single score, rather than a distribution over outputs as the representation of uncertainty.

The problem of classification with a reject option or learning with abstention [3, 57, 9, 23, 8, 27, 10] is a highly related framework where the classifier is allowed to abstain from making a prediction at a certain cost. Typically such methods jointly learn the classifier and the rejection function. Note that the interplay between classification rate and reject rate is studied in many various forms e.g. [7, 13, 19, 48, 52, 18, 34, 14, 56, 51]. Our paper assumes an already trained and possibly black-box classifier and learns the confidence scores separately, but we do not explicitly learn the appropriate rejection thresholds.

Whether to trust a classifier also arises in the setting where one has access to a sequence of classifiers, but there is some cost to evaluating each classifier, and the goal is to decide after evaluating each classifier in the sequence if one should trust the current classifier decision enough to stop, rather than evaluating more classifiers in the sequence (e.g. [55, 43, 16]). Those confidence decisions are usually based on whether the current classifier score will match the classification of the full sequence.

Experimentally we find that the vector space used to compute the distances in the trust score matters, and that computing trust scores on more-processed layers of a deep model generally works better. This observation is similar to the work of Papernot and McDaniel [42], who use k-NN regression on the intermediate representations of the network which they showed enhances robustness to adversarial attacks and leads to better calibrated uncertainty estimations.

Our work builds on recent results in topological data analysis. Our method to filter low-density points estimates a particular density level-set given a parameter α, which aims at finding the levelset that contains 1 − α fraction of the probability mass. Level-set estimation has a long history [25, 15, 53, 50, 46, 28]. However such works assume knowledge of the density level, which is difficult to determine in practice. We provide rates for Algorithm 1 in estimating the appropriate level-set corresponding to α without knowledge of the level. The proxy α offers a more intuitive parameter compared to the density value, is used for level-set estimation. Our analysis is also done under various settings including when the data lies near a lower dimensional manifold and we provide rates that depend only on the lower dimension.

## 3 Algorithm: The Trust Score

Our approach proceeds in two steps outlined in Algorithm 1 and 2. We first pre-process the training data, as described in Algorithm 1, to find the α-high-density-set of each class, which is defined as the training samples within that class after filtering out α-fraction of the samples with lowest density (which may be outliers):

Definition 1 (α-high-density-set). Let $0 \leq \alpha < 1$ and f be a continuous density function with compact support $\check { x } \subseteq \mathbb { R } ^ { D }$ . Then define $H _ { \alpha } ( f )$ , the α-high-density-set of f , to be the $\bar { \lambda } _ { \alpha }$ -level set of f, defined as $\{ x \in \mathcal { X } : f ( x ) \geq \lambda _ { \alpha } \}$ where $\begin{array} { r } { \lambda _ { \alpha } : = \operatorname* { i n f } \left\{ \lambda \ge 0 : \int _ { \mathcal { X } } 1 \left[ f ( x ) \le \lambda \right] f ( x ) d x \ge \alpha \right\} } \end{array}$

In order to approximate the α-high-density-set, Algorithm 1 filters the α-fraction of the sample points with lowest empirical density, based on k-nearest neighbors. This data filtering step is independent of the given classifier h.

$h ,$

Our procedure can thus be viewed as a comparison to a modified nearest-neighbor classifier, where the modification lies in the initial filtering of points not in the α-high-density-set for each class.

Remark 1. The distances can be computed with respect to any representation of the data. For example, the raw inputs, an unsupervised embedding of the space, or the activations of the intermediate representations of the classifier. Moreover, the nearest-neighbor distance can be replaced by other distance measures, such as k-nearest neighbors or distance to a centroid.

```latex
Algorithm 1 Estimating α-high-density-set
Parameters: α (density threshold), k.
Inputs: Sample points $X : = \{ x _ { 1 } , . . , x _ { n } \}$ drawn from $f .$
Define k-NN radius $r _ { k } ( x ) : = \operatorname* { i n f } \{ r > 0 : | B ( x , r ) \cap { \bar { X } } | \geq k \}$ and let $\varepsilon : = \operatorname* { i n f } \{ r > 0 : | \{ x \in X$
$r _ { k } ( x ) > r \} | \leq \alpha \cdot n \}$
return ${ \widehat { H _ { \alpha } } } ( f ) : = \{ x \in X : r _ { k } ( x ) \leq \varepsilon \}$
Algorithm 2 Trust Score
Parameters: α (density threshold), k.
Input: Classifier $h : \check { \mathcal { X } }  \mathcal { Y } .$ Training data $( x _ { 1 } , y _ { 1 } ) , . . . , ( x _ { n } , y _ { n } )$ . Test example x.
For each $\ell \in \mathcal { V } .$ , let $\widehat { H _ { \alpha } } ( f _ { \ell } )$ be the output of Algorithm 1 with parameters α, k and sample points
$\{ x _ { j } : 1 \leq j \leq n , y _ { j } = \ell \}$ . Then, return the trust score, defined as:
$\xi ( h , x ) : = d \left( x , \widehat { H _ { \alpha } } ( f _ { \widetilde { h } ( x ) } ) \right) / d \left( x , \widehat { H _ { \alpha } } ( f _ { h ( x ) } ) \right)$
where $\begin{array} { r } { \widetilde { h } ( x ) = \mathrm { a r g m i n } _ { l \in \mathcal { V } , l \neq h ( x ) } d \left( x , \widehat { H _ { \alpha } } ( f _ { l } ) \right) } \end{array}$
```

The method has two hyperparameters: k (the number of neighbors, such as in k-NN) and α (fraction of data to filter) to compute the empirical densities. We show in theory that k can lie in a wide range and still give us the desired consistency guarantees. Throughout our experiments, we fix $k = 1 0$ , and use cross-validation to select α as it is data-dependent.

## 4 Theoretical Analysis

In this section, we provide theoretical guarantees for Algorithms 1 and 2. Due to space constraints, all the proofs are deferred to the Appendix. To simplify the main text, we state our results treating δ, the confidence level, as a constant. The dependence on δ in the rates is made explicit in the Appendix.

We show that Algorithm 1 is a statistically consistent estimator of the α-high-density-level set with finite-sample estimation rates. We analyze Algorithm 1 in three different settings: when the data lies on (i) a full-dimensional $\mathbb { R } ^ { D }$ ; (ii) an unknown lower dimensional submanifold embedded in $\mathbb { R } ^ { D }$ ; and (iii) an unknown lower dimensional submanifold with full-dimensional noise.

For setting (i), where the data lies in $\mathbb { R } ^ { D }$ , the estimation rate has a dependence on the dimension D, which may be unattractive in high-dimensional situations: this is known as the curse of dimensionality, suffered by density-based procedures in general. However, when the data has low intrinsic dimension in (ii), it turns out that, remarkably, without any changes to the procedure, the estimation rate depends on the lower dimension d and is independent of the ambient dimension D. However, in realistic situations, the data may not lie exactly on a lower-dimensional manifold, but near one. This reflects the setting of (iii), where the data essentially lies on a manifold but has general full-dimensional noise so the data is overall full-dimensional. Interestingly, we show that we still obtain estimation rates depending only on the manifold dimension and independent of the ambient dimension; moreover, we do not require knowledge of the manifold nor its dimension to attain these rates.

We then analyze Algorithm 2, and establish the culminating result of Theorem 4: for labeled data distributions with well-behaved class margins, when the trust score is large, the classifier likely agrees with the Bayes-optimal classifier, and when the trust score is small, the classifier likely disagrees with the Bayes-optimal classifier. If it turns out that even the Bayes-optimal classifier has high-error in a certain region, then any classifier will have difficulties in that region. Thus, Theorem 4 does not guarantee that the trust score can predict misclassification, but rather that it can predict when the classifier is making an unreasonable decision.

## 4.1 Analysis of Algorithm 1

$H _ { \alpha } ( f )$ $H _ { \alpha } ( f )$ $H _ { \alpha } ( f )$ $H _ { \alpha } ( f )$

Assumption 1 (α-high-density-set regularity). Let $\beta > 0$ . There exists $\check { C } _ { \beta } , \hat { C } _ { \beta } , \beta , r _ { c } , r _ { 0 } , \rho > 0 \mathrm { ~ } s . t .$

$$
I . \ \check { C } _ { \beta } \cdot d ( x , H _ { \alpha } ( f ) ) ^ { \beta } \leq | \lambda _ { \alpha } - f ( x ) | \leq \hat { C } _ { \beta } \cdot d ( x , H _ { \alpha } ( f ) ) ^ { \beta } f o r \ a l l \ x \in \partial H _ { \alpha } ( f ) + B ( 0 , r _ { c } ) .
$$

2. For all $0 < r < r _ { 0 }$ and $x \in H _ { \alpha } ( f )$ , we have $V o l ( B ( x , r ) ) \geq \rho \cdot r ^ { D }$

where ∂A denotes the boundary of a set $\begin{array} { r } { A , d ( x , A ) : = \operatorname* { i n f } _ { x ^ { \prime } \in A } | | x - x ^ { \prime } | | , B ( x , r ) : = \{ x ^ { \prime } : | x - x ^ { \prime } | \leq \frac { 1 } { r ^ { \prime } } } \end{array}$ r} and $A + B ( 0 , r ) : = \{ x : d ( x , A ) \leq r \}$

Our statistical guarantees are under the Hausdorff metric, which ensures a uniform guarantee over our estimator: it is a stronger notion of consistency than other common metrics [46, 47].

Definition 2 (Hausdorff distance). $d _ { H } ( A , B ) : = \operatorname* { m a x } \{ \operatorname* { s u p } _ { x \in A } d ( x , B ) , \operatorname* { s u p } _ { x \in B } d ( x , A ) \}$

We now give the following result for Algorithm 1. It says that as long as our density function satisfies the regularity assumptions stated earlier, and the parameter k lies within a certain range, then we can bound the Hausdorff distance between what Algorithm 1 recovers and $H _ { \alpha } ( f )$ , the true α-high-density set, from an i.i.d. sample drawn from f of size n. Then, as n goes to $\infty ,$ , and k grows as a function of n, the quantity goes to 0.

Theorem 1 (Algorithm 1 guarantees). Let $0 < \delta < 1$ and suppose that f is continuous and has compact support $\boldsymbol { \mathcal { X } } \subseteq \mathbb { R } ^ { \mathbf { \breve { D } } }$ and satisfies Assumption 1. There exists constants $C _ { l } , C _ { u } , C ~ > ~ 0$ depending on $f$ and δ such that the following holds with probability at least $1 - \delta$ . Suppose that k satisfies $C _ { l }$ · log $n \leq k \leq C _ { u } \cdot ( \log \stackrel { \smile } { n } ) ^ { D ( 2 \beta + \stackrel { \smile } { D } ) } \cdot n ^ { 2 \beta / ( 2 \beta + D ) }$ . Then we have

$$
d _ { H } ( H _ { \alpha } ( f ) , \widehat { H _ { \alpha } } ( f ) ) \leq C \cdot \left( n ^ { - 1 / 2 D } + \log ( n ) ^ { 1 / 2 \beta } \cdot k ^ { - 1 / 2 \beta } \right) .
$$

Remark 3. The condition on k can be simplified by ignoring log factors: log $n \lesssim k \lesssim n ^ { 2 \beta / ( 2 \beta + D ) }$ which is a wide range. Setting k to its allowed upper bound, we obtain our consistency guarantee of

$$
d _ { H } \big ( H _ { \alpha } ( f ) , \widehat { H _ { \alpha } } ( f ) \big ) \lesssim \operatorname* { m a x } \{ n ^ { - 1 / 2 D } , n ^ { - 1 / ( 2 \beta + D ) } \} .
$$

The first term is due to the error from estimating the appropriate level given α (i.e. identifying the level $\lambda _ { \alpha } )$ and the second term corresponds to the error for recovering the level set given knowledge of the level. The latter term matches the lower bound for level-set estimation up to log factors [53].

## 4.2 Analysis of Algorithm 1 on Manifolds

One of the disadvantages of Theorem 1 is that the estimation errors have a dependence on D, the dimension of the data, which may be highly undesirable in high-dimensional settings. We next improve these rates when the data has a lower intrinsic dimension. Interestingly, we are able to show rates that depend only on the intrinsic dimension of the data, without explicit knowledge of that dimension nor any changes to the procedure. As common to related work in the manifold setting, we make the following regularity assumptions which are standard among works in manifold learning (e.g. [41, 21, 2]).

Assumption 2 (Manifold Regularity). M is a d-dimensional smooth compact Riemannian manifold without boundary embedded in compact subset $\boldsymbol { \mathcal { X } } \subseteq \mathbb { R } ^ { D }$ with bounded volume. M has finite condition number $1 / \tau _ { ; }$ , which controls the curvature and prevents self-intersection.

Theorem 2 (Manifold analogue of Theorem 1). Let $0 < \delta < 1$ . Suppose that density function f is continuous and supported on M and Assumptions 1 and 2 hold. Suppose also that there exists $\lambda _ { 0 } > 0$ such that $f ( x ) \geq \lambda _ { 0 }$ for all $x \in M .$ . Then, there exists constants $C _ { l } , C _ { u } , C > 0$ depending on $f$ and δ such that the following holds with probability at least $1 - \delta .$ . Suppose that k satisfies $C _ { l } \cdot \log n \le k \le C _ { u } \cdot ( \log n ) ^ { d ( 2 \beta ^ { \prime } + d ) } \cdot n ^ { 2 \beta ^ { \prime } / ( 2 \bar { \beta } ^ { \prime } + d ) }$ . where $\beta ^ { \prime } : = \operatorname* { m a x } \{ 1 , \beta \}$ . Then we have

$$
d _ { H } ( H _ { \alpha } ( f ) , \widehat { H _ { \alpha } } ( f ) ) \leq C \cdot \left( n ^ { - 1 / 2 d } + \log ( n ) ^ { 1 / 2 \beta } \cdot k ^ { - 1 / 2 \beta } \right) .
$$

Remark 4. Setting k to its allowed upper bound, we obtain (ignoring log factors),

$$
d _ { H } \big ( H _ { \alpha } ( f ) , \widehat { H _ { \alpha } } ( f ) \big ) \lesssim \operatorname* { m a x } \{ n ^ { - 1 / 2 d } , n ^ { - 1 / ( 2 \operatorname* { m a x } \{ 1 , \beta \} + d ) } \} .
$$

The first term can be compared to that of the previous result where D is replaced with d. The second term is the error for recovering the level set on manifolds, which matches recent rates [28].

## 4.3 Analysis of Algorithm 1 on Manifolds with Full Dimensional Noise

In realistic settings, the data may not lie exactly on a low-dimensional manifold, but near one. We next present a result where the data is distributed along a manifold with additional full-dimensional noise. We make mild assumptions on the noise distribution. Thus, in this situation, the data has intrinsic dimension equal to the ambient dimension. Interestingly, we are still able to show that the rates only depend on the dimension of the manifold and not the dimension of the entire data.

Theorem 3. Let $0 < \eta < \alpha < 1$ and $0 \textless \delta \textless 1$ . Suppose that distribution $\mathcal { F }$ is a weighted mixture $( 1 - \eta ) \cdot \mathcal { F } _ { M } + \eta \cdot \mathcal { F } _ { E }$ where $\mathcal { F } _ { M }$ is a distribution with continous density $f _ { M }$ supported on a d-dimensional manifold M satisfying Assumption 2 and $\mathcal { F } _ { E }$ is a (noise) distribution with continuous density $f _ { E }$ with compact support over $\mathbb { R } ^ { D }$ with $d < D$ . Suppose also that there exists $\lambda _ { 0 } > 0$ such

$f _ { M } ( x ) \geq \lambda _ { 0 }$ $x \in M$ $H _ { \widetilde \alpha } ( f _ { M } )$ $\begin{array} { r } { \widetilde \alpha : = \frac { \alpha - \eta } { 1 - \eta } ) } \end{array}$ $f _ { M }$ $\widehat { H } _ { \alpha }$ ${ \mathcal F } .$ $C _ { l } , C _ { u } , \bar { C } \bar { > }$ $f _ { M } , f _ { E } , \eta ,$ $1 - \delta .$ $C _ { l } \cdot \log n \le k \le C _ { u } \cdot ( \log n ) ^ { d ( 2 \beta ^ { \prime } + d ) } \cdot \bar { n } ^ { 2 \beta ^ { \prime } / ( 2 \beta ^ { \prime } + d ) }$ $\beta ^ { \prime } \doteq \operatorname* { m a x } \{ 1 , \beta \}$

$$
d _ { H } \big ( H _ { \widetilde { \alpha } } ( f _ { M } ) , \widehat { H _ { \alpha } } \big ) \leq C \cdot \Big ( n ^ { - 1 / 2 d } + \log ( n ) ^ { 1 / 2 \beta } \cdot k ^ { - 1 / 2 \beta } \Big ) .
$$

The above result is compelling because it shows why our methods can work, even in high-dimensions, despite the curse of dimensionality of non-parametric methods. In typical real-world data, even if the data lies in a high-dimensional space, there may be far fewer degrees of freedom. Thus, our theoretical results suggest that when this is true, then our methods will enjoy far better convergence rates – even when the data overall has full intrinsic dimension due to factors such as noise.

## 4.4 Analysis of Algorithm 2: the Trust Score

We now provide a guarantee about the trust score, making the same assumptions as in Theorem 3 for each of the label distributions. We additionally assume that the class distributions are well-behaved in the following sense: that high-density-regions for each of the classes satisfy the property that for any point $x \in \mathcal { X }$ , if the ratio of the distance to one class’s high-density-region to that of another is smaller by some margin γ, then it is more likely that $x ' s$ label corresponds to the former class.

Theorem 4. Let $0 < \eta < \alpha < 1$ . Let us have labeled data $( x _ { 1 } , y _ { 1 } ) , . . . , ( x _ { n } , y _ { n } )$ drawn from distribution D, which is a joint distribution over $\mathcal { X } \times \mathcal { V }$ where $\mathcal { V }$ are the labels, $| y | < \infty ,$ , and $\boldsymbol { \mathcal { X } } \subseteq \mathbb { R } ^ { D }$ is compact. Suppose for each $\boldsymbol { \ell } \in \mathcal { V } _ { \mathrm { i } }$ , the conditional distribution for label \` satisfies the conditions of Theorem 3 for some manifold and noise level η. Let $f _ { M , \ell }$ be the density of the portion of the conditional distribution for label \` supported on M . Define $M _ { \ell } : = H _ { \widetilde { \alpha } } ( f _ { \ell } )$ , where $\begin{array} { r } { \widetilde { \alpha } : = \frac { \alpha - \eta } { 1 - \eta } } \end{array}$ and let $\epsilon _ { n }$ be the maximum Hausdorff error from estimating $M _ { \ell }$ over each $\ell \in \mathcal { V }$ in Theorem 3. Assume that min $\iota _ { \ell \in \mathcal { y } } \mathbb { P } _ { \mathcal { D } } ( y = \ell ) > 0$ to ensure we have samples from each label.

$x \in \mathcal { X } , i f d ( x , M _ { i } ) / d ( x , M _ { j } ) < 1 - \gamma$ $\mathbb { P } ( y = i | x ) > \mathbb { P } ( y = j | x )$   
$f o r \ i , j \ \in \ { \mathcal { V } }$ $M _ { j }$ $1 - \gamma ,$ $h ^ { * }$ $h ^ { \ast } ( x ) : =$   
$\operatorname { \bar { a r g m a x } } _ { \ell \in \mathcal { Y } } \mathbb { P } ( y \overset { } { = } \ell | x )$ $x \in \mathcal { X }$ ${ \bar { h } } : \mathcal { X } \to \mathcal { Y }$

$$
\xi ( h , x ) < 1 - \gamma - \frac { \epsilon _ { n } } { d ( x , M _ { h ( x ) } ) + \epsilon _ { n } } \cdot \left( \frac { d ( x , M _ { \tilde { h } ( x ) } ) } { d ( x , M _ { h ( x ) } ) } + 1 \right) \quad \Rightarrow \quad h ( x ) \neq h ^ { \ast } ( x ) ,
$$

$$
\frac { 1 } { \xi ( h , x ) } < 1 - \gamma - \frac { \epsilon _ { n } } { d ( x , M _ { \tilde { h } ( x ) } ) + \epsilon _ { n } } \cdot \left( \frac { d ( x , M _ { h ( x ) } ) } { d ( x , M _ { \tilde { h } ( x ) } ) } + 1 \right) \quad \Rightarrow \quad h ( x ) = h ^ { \ast } ( x ) .
$$

## 5 Experiments

$\mathrm { e . g . }$

![](images/74f88ffaabff0e2cfaee446d3950ba8490ee51d55332a9327fc0cf3cd56ec7fa.jpg)  
Figure 1: Two example datasets and models. For predicting correctness (top row) the vertical dotted black line indicates error level of the trained classifier. For predicting incorrectness (bottom) the vertical black dotted line is the accuracy rate of the classifier. For detecting trustworthy, for each percentile level, we take the test examples whose trust score was above that percentile level and plot the percentage of those test points that were correctly classified by the classifier, and do the same model confidence and 1-nn ratio. For detecting suspicious, we take the negative of each signal and plot the precision of identifying incorrectly classified examples. Shown are average of 20 runs with shaded standard error band. The trust score consistently attains a higher precision for each given percentile of classifier decision-rejection. Furthermore, the trust score generally shows increasing precision as the percentile level increases, but surprisingly, many of the comparison baselines do not. See the Appendix for the full results.

examples"). Here the y-axis is the misclassification rate and the x-axis corresponds to decreasing trust score or model confidence.

In both cases, the higher the precision vs percentile curve, the better the method. The vertical black dotted lines in the plots represent the omniscient ideal. For identifying trustworthy examples it is the error rate of the classifier and for identifying suspicious examples" it is the accuracy rate.

The baseline we use in Section is the model’s own confidence score, which is similar to the approach of [26]. While calibrating the classifiers’ confidence scores (i.e. transforming them into probability estimates of correctness) is an important related work [24, 44], such techniques typically do not change the rankings of the score, at least in the binary case. Since we evaluate the trust score on its precision at a given recall percentile level, we are interested in the relative ranking of the scores rather than their absolute values. Thus, we do not compare against calibration techniques. There are surprisingly few methods aimed at identifying correctly or incorrectly classified examples with precision at a recall percentile level as noted in [26].

Choosing Hyperparameters: The two hyperparameters for the trust score are α and k. Throughout the experiments, we fix k = 10 and choose α using cross-validation over (negative) powers of 2 on the training set. The metric for cross-validation was optimal performance on detecting suspicious examples at the percentile corresponding to the classifier’s accuracy. The bulk of the computational cost for the trust-score is in k-nearest neighbor computations for training and 1-nearest neighbor searches for evaluation. To speed things up for the larger datasets MNIST, SVHN, CIFAR-10 and CIFAR-100, we skipped the initial filtering step of Algorithm 1 altogether and reduced the intermediate layers down to 20 dimensions using PCA before being processed by the trust score which showed similar performance. We note that any approximation method (such as approximate instead of exact nearest neighbors) could have been used instead.

## 5.1 Performance on Benchmark UCI Datasets

In this section, we show performance on five benchmark UCI datasets [17], each for three kinds of classifiers (neural network, random forest and logistic regression). Due to space, we only show two data sets and two models in Figure 1. The rest can be found in the Appendix. For each method and dataset, we evaluated with multiple runs. For each run we took a random stratified split of the dataset into two halves. One portion was used for training the trust score and the other was used for evaluation and the standard error is shown in addition to the average precision across the runs at each percentile level. The results show that our method consistently has a higher precision vs percentile curve than the rest of the methods across the datasets and models. This suggests the trust score considerably improves upon known methods as a signal for identifying trustworthy and suspicious testing examples for low-dimensional data.

![](images/2303b2fc46cd18e4a72e10a22ca213bba506991cd48697c7e31dd46989a0ba06.jpg)  
Figure 2: We show the performance of trust score on the Digits dataset for a neural network as we increase the accuracy. As we go from left to right, we train the network with more iterations (each with batch size 50) thus increasing the accuracy indicated by the dotted vertical lines. While the trust score still performs better than model confidence, the amount of improvement diminishes.

In addition to the model’s own confidence score, we try one additional baseline, which we call the nearest neighbor ratio (1-nn ratio). It is the ratio between the 1-nearest neighbor distance to the closest and second closest class, which can be viewed as an analogue to the trust score without knowledge of the classifier’s hard prediction.

## 5.2 Performance as Model Accuracy Varies

In Figure 2, we show how the performance of trust score changes as the accuracy of the classifier changes (averaged over 20 runs for each condition). We observe that as the accuracy of the model increases, while the trust score still performs better than model confidence, the amount of improvement diminishes. This suggests that as the model improves, the information trust score can provide in addition to the model confidence decreases. However, as we show in Section 5.3, the trust score can still have added value even when the classifier is known to be of high performance on some benchmark larger-scale datasets.

## 5.3 Performance on MNIST, SVHN, CIFAR-10 and CIFAR-100 Datasets

![](images/0d7e5abcb7b493006836699730afdfaabfef7aaf9e846024c8b5e9fc74d7b56e.jpg)  
(a) MNIST

![](images/fdb3c608938ac547d06b8bd0249ed2bf709d0d6eb3a94c6413eefbbbff551d72.jpg)  
(b) SVHN

![](images/fbdad287372cad00de78ef8644305aeba3fe7a4e9f847e2b1541ce237b168bb5.jpg)  
(c) CIFAR-10

![](images/9422ea7f624aa3dc3b66e615949d91bfcc60a99ffbd93ff501e930e1d963d8ac.jpg)  
(d) MNIST

![](images/c5e231bb72a4f91e0f63bdb6310bb9f9155138cef0fef5c8090227f84871bfd7.jpg)  
(e) SVHN

![](images/62c26149e00f8cbc897abb61b594b126e81edefcecc1609bae503b735697fe43.jpg)  
(f) CIFAR-10  
Figure 3: Trust score results using convolutional neural networks on MNIST, SVHN, and CIFAR-10 datasets. Top row is detecting trustworthy; bottom row is detecting suspicious. Full chart with CIFAR-100 (which was essentially a negative result) is shown in the Appendix.

We used a pretrained VGG-16 [49] architecture with adaptation to the CIFAR datasets based on [37]. The CIFAR-10 VGG-16 network achieves a test accuracy of 93.56% while the CIFAR-100 network achieves a test accuracy of 70.48%. We used pretrained, smaller CNNs for MNIST and SVHN. The MNIST network achieves a test accuracy of 99.07% and the SVHN network achieves a test accuracy of 95.45%. All architectures were implemented in Keras [6].

The trust score results on various layers are shown in Figure 3. They suggest that for high dimensional datasets, the trust score may only provide little or no improvement over the model confidence at detecting trustworthy and suspicious examples. All plots were made using α = 0; using crossvalidation to select a different α did not improve trust score performance. We also did not see much difference from using different layers.

## Conclusion:

In this paper, we provide the trust score: a new, simple, and effective way to judge if one should trust the prediction from a classifier. The trust score provides information about the relative positions of the datapoints, which may be lost in common approaches such as the model confidence when the model is trained using SGD. We show high-probability non-asymptotic statistical guarantees that high (low) trust scores correspond to agreement (disagreement) with the Bayes-optimal classifier under various nonparametric settings, which build on recent results in topological data analysis. Our empirical results across many datasets, classifiers, and representations of the data show that our method consistently outperforms the classifier’s own reported confidence in identifying trustworthy and suspicious examples in low to mid dimensional datasets. The theoretical and empirical results suggest that this approach may have important practical implications in low to mid dimension settings.

## References

[1] Dario Amodei, Chris Olah, Jacob Steinhardt, Paul F Christiano, John Schulman, and Dan Mané. Concrete problems in AI safety. CoRR, abs/1606.06565, 2016. URL http://arxiv.org/ abs/1606.06565.

[2] Sivaraman Balakrishnan, Srivatsan Narayanan, Alessandro Rinaldo, Aarti Singh, and Larry Wasserman. Cluster trees on manifolds. In Advances in Neural Information Processing Systems, pages 2679–2687, 2013.

[3] Peter L Bartlett and Marten H Wegkamp. Classification with a reject option using a hinge loss. Journal of Machine Learning Research, 9(Aug):1823–1840, 2008.

[4] Kamalika Chaudhuri and Sanjoy Dasgupta. Rates of convergence for the cluster tree. In Advances in Neural Information Processing Systems, pages 343–351, 2010.

[5] Frédéric Chazal. An upper bound for the volume of geodesic balls in submanifolds of Euclidean spaces. https://geometrica.saclay.inria.fr/team/Fred.Chazal/BallVolumeJan2013.pdf, 2013.

[6] François Chollet et al. Keras. 2015.

[7] C Chow. On optimum recognition error and reject tradeoff. IEEE Transactions on Information Theory, 16(1):41–46, 1970.

[8] Corinna Cortes, Giulia DeSalvo, and Mehryar Mohri. Boosting with abstention. In Advances in Neural Information Processing Systems, pages 1660–1668, 2016.

[9] Corinna Cortes, Giulia DeSalvo, and Mehryar Mohri. Learning with rejection. In International Conference on Algorithmic Learning Theory, pages 67–82. Springer, 2016.

[10] Corinna Cortes, Giulia DeSalvo, Claudio Gentile, Mehryar Mohri, and Scott Yang. Online learning with abstention. arXiv preprint arXiv:1703.03478, 2017.

[11] Sanjoy Dasgupta and Samory Kpotufe. Optimal rates for k-NN density and mode estimation. In Advances in Neural Information Processing Systems, pages 2555–2563, 2014.

[12] Luc Devroye, Laszlo Gyorfi, Adam Krzyzak, and Gábor Lugosi. On the strong universal consistency of nearest neighbor regression function estimates. The Annals of Statistics, pages 1371–1385, 1994.

[13] Bernard Dubuisson and Mylene Masson. A statistical decision rule with incomplete knowledge about classes. Pattern Recognition, 26(1):155–165, 1993.

[14] Ran El-Yaniv and Yair Wiener. On the foundations of noise-free selective classification. Journal of Machine Learning Research, 11(May):1605–1641, 2010.

[15] Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu, et al. A density-based algorithm for discovering clusters in large spatial databases with noise. In Kdd, pages 226–231, 1996.

[16] Wei Fan, Fang Chu, Haixun Wang, and Philip S. Yu. Pruning and dynamic scheduling of cost-sensitive ensembles. AAAI, 2002.

[17] Jerome Friedman, Trevor Hastie, and Robert Tibshirani. The Elements of Statistical Learning. Springer, 2001.

[18] Giorgio Fumera and Fabio Roli. Support vector machines with embedded reject option. In Pattern Recognition with Support Vector Machines, pages 68–82. Springer, 2002.

[19] Giorgio Fumera, Fabio Roli, and Giorgio Giacinto. Multiple reject thresholds for improving classification reliability. In Joint IAPR International Workshops on Statistical Techniques in Pattern Recognition (SPR) and Structural and Syntactic Pattern Recognition (SSPR), pages 863–871. Springer, 2000.

[20] Yarin Gal and Zoubin Ghahramani. Dropout as a Bayesian approximation: Representing model uncertainty in deep learning. In International Conference on Machine Learning, pages 1050–1059, 2016.

[21] Christopher Genovese, Marco Perone-Pacifico, Isabella Verdinelli, and Larry Wasserman. Minimax manifold estimation. Journal of Machine Learning Research, 13(May):1263–1291, 2012.

[22] Ian J Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. arXiv preprint arXiv:1412.6572, 2014.

[23] Yves Grandvalet, Alain Rakotomamonjy, Joseph Keshet, and Stéphane Canu. Support vector machines with a reject option. In Advances in Neural Information Processing Systems, pages 537–544, 2009.

[24] Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q Weinberger. On calibration of modern neural networks. arXiv preprint arXiv:1706.04599, 2017.

[25] John A Hartigan. Clustering algorithms. 1975.

[26] Dan Hendrycks and Kevin Gimpel. A baseline for detecting misclassified and out-of-distribution examples in neural networks. arXiv preprint arXiv:1610.02136, 2016.

[27] Radu Herbei and Marten H Wegkamp. Classification with reject option. Canadian Journal of Statistics, 34(4):709–721, 2006.

[28] Heinrich Jiang. Density level set estimation on manifolds with DBSCAN. In International Conference on Machine Learning, pages 1684–1693, 2017.

[29] Heinrich Jiang. Uniform convergence rates for kernel density estimation. In International Conference on Machine Learning, pages 1694–1703, 2017.

[30] Alex Kendall and Yarin Gal. What uncertainties do we need in Bayesian deep learning for computer vision? In Advances in Neural Information Processing Systems, pages 5580–5590, 2017.

[31] Alex Krizhevsky. Learning multiple layers of features from tiny images. 2009.

[32] Volodymyr Kuleshov and Percy S Liang. Calibrated structured prediction. In Advances in Neural Information Processing Systems, pages 3474–3482, 2015.

[33] Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and scalable predictive uncertainty estimation using deep ensembles. In Advances in Neural Information Processing Systems, pages 6405–6416, 2017.

[34] Thomas CW Landgrebe, David MJ Tax, Pavel Paclík, and Robert PW Duin. The interaction between classification and reject performance for distance-based reject-option classifiers. Pattern Recognition Letters, 27(8):908–917, 2006.

[35] Yann LeCun. The MNIST database of handwritten digits. http://yann. lecun. com/exdb/mnist/, 1998.

[36] John D Lee and Katrina A See. Trust in automation: Designing for appropriate reliance. Human factors, 46(1):50–80, 2004.

[37] Shuying Liu and Weihong Deng. Very deep convolutional neural network based image classification using small training sample size. 2015 3rd IAPR Asian Conference on Pattern Recognition (ACPR), pages 730–734, 2015.

[38] Yuval Netzer, Tao Wang, Adam Coates, Alessandro Bissacco, Bo Wu, and Andrew Y Ng. Reading digits in natural images with unsupervised feature learning. 2011.

[39] Anh Nguyen, Jason Yosinski, and Jeff Clune. Deep neural networks are easily fooled: High confidence predictions for unrecognizable images. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 427–436, 2015.

[40] Alexandru Niculescu-Mizil and Rich Caruana. Predicting good probabilities with supervised learning. In Proceedings of the 22nd International Conference on Machine Learning, pages 625–632. ACM, 2005.

[41] Partha Niyogi, Stephen Smale, and Shmuel Weinberger. Finding the homology of submanifolds with high confidence from random samples. Discrete & Computational Geometry, 39(1-3): 419–441, 2008.

[42] Nicolas Papernot and Patrick McDaniel. Deep k-nearest neighbors: Towards confident, interpretable and robust deep learning. arXiv preprint arXiv:1803.04765, 2018.

[43] Nathan Parrish, Hyrum S. Anderson, Maya R. Gupta, and Dun Yu Hsaio. Classifying with confidence from incomplete information. Journal of Machine Learning Research, 14(December): 3561–3589, 2013.

[44] John Platt. Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. Advances in Large Margin Classifiers, 10(3):61–74, 1999.

[45] Foster J Provost, Tom Fawcett, and Ron Kohavi. The case against accuracy estimation for comparing induction algorithms. In ICML, volume 98, pages 445–453, 1998.

[46] Philippe Rigollet, Régis Vert, et al. Optimal rates for plug-in estimators of density level sets. Bernoulli, 15(4):1154–1178, 2009.

[47] Alessandro Rinaldo and Larry Wasserman. Generalized density clustering. The Annals of Statistics, 38(5):2678–2722, 2010.

[48] Carla M Santos-Pereira and Ana M Pires. On optimal reject rules and ROC curves. Pattern Recognition Letters, 26(7):943–952, 2005.

[49] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. arXiv preprint arXiv:1409.1556, 2014.

[50] Aarti Singh, Clayton Scott, Robert Nowak, et al. Adaptive Hausdorff estimation of density level sets. The Annals of Statistics, 37(5B):2760–2782, 2009.

[51] David MJ Tax and Robert PW Duin. Growing a multi-class classifier with a reject option. Pattern Recognition Letters, 29(10):1565–1570, 2008.

[52] Francesco Tortorella. An optimal reject rule for binary classifiers. In Joint IAPR International Workshops on Statistical Techniques in Pattern Recognition (SPR) and Structural and Syntactic Pattern Recognition (SSPR), pages 611–620. Springer, 2000.

[53] Alexandre B Tsybakov et al. On nonparametric estimation of density level sets. The Annals of Statistics, 25(3):948–969, 1997.

[54] Kush R Varshney and Homa Alemzadeh. On the safety of machine learning: Cyber-physical systems, decision sciences, and data products. Big data, 5(3):246–255, 2017.

[55] Joseph Wang, Kirill Trapeznikov, and Venkatesh Saligrama. Efficient learning by directed acyclic graph for resource constrained prediction. Advances in Neural Information Processing Systems (NIPS), 2015.

[56] Yair Wiener and Ran El-Yaniv. Agnostic selective classification. In Advances in Neural Information Processing Systems, pages 1665–1673, 2011.

[57] Ming Yuan and Marten Wegkamp. Classification methods with reject option based on convex risk minimization. Journal of Machine Learning Research, 11(Jan):111–130, 2010.

[58] Bianca Zadrozny and Charles Elkan. Transforming classifier scores into accurate multiclass probability estimates. In Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pages 694–699. ACM, 2002.

## Appendix

## A Supporting results for Theorem 1 Proof

We need the following result giving guarantees on the empirical balls.

Lemma 1 (Uniform convergence of balls [4]). Let $\mathcal { F }$ be the distribution corresponding to $f$ and $\mathcal { F } _ { n }$ be the empirical distribution corresponding to the sample X. Pick $0 < \delta < 1$ . Assume that $k \geq D$ log n. Then with probability at least $1 - \delta ,$ , for every ball $B \subset \mathbb { R } ^ { D }$ we have

$$
{ \mathcal { F } } ( B ) \geq C _ { \delta , n } { \frac { \sqrt { D \log n } } { n } } \Rightarrow { \mathcal { F } } _ { n } ( B ) > 0
$$

$$
\mathcal { F } ( B ) \geq \frac { k } { n } + C _ { \delta , n } \frac { \sqrt { k } } { n } \Rightarrow \mathcal { F } _ { n } ( B ) \geq \frac { k } { n }
$$

$$
\mathcal { F } ( B ) \leq \frac { k } { n } - C _ { \delta , n } \frac { \sqrt { k } } { n } \Rightarrow \mathcal { F } _ { n } ( B ) < \frac { k } { n } ,
$$

where $C _ { \delta , n } = 1 6 \log ( 2 / \delta ) \sqrt { D \log n }$

Remark 5. For the rest of the paper, many results are qualified to hold with probability at least $1 - \delta .$ This is precisely the event in which Lemma 1 holds.

Remark 6. $H \delta = 1 / n ,$ then $C _ { \delta , n } = O ( ( \log n ) ^ { 3 / 2 } )$

To analyze Algorithm 1, we use the $k { \mathrm { - N N } }$ density estimator[12], defined below.

Definition 3. Define the k-NN radius of $\boldsymbol { x } \in \mathbb { R } ^ { D }$ as

$$
r _ { k } ( x ) : = \operatorname* { i n f } \{ r > 0 : | X \cap B ( x , r ) | \geq k \} ,
$$

Definition 4 (k-NN Density Estimator).

$$
f _ { k } ( x ) : = \frac { k } { n \cdot v _ { D } \cdot r _ { k } ( x ) ^ { D } } ,
$$

where $v _ { D }$ is the volume of a unit ball in $\mathbb { R } ^ { D }$

We will use bounds on the k-NN density estimator from [11], which are repeated here.

Define the following one-sided modulus of continuity which characterizes how much the density increases locally:

$$
\hat { r } ( \epsilon , x ) : = \operatorname* { s u p } \left\{ r : \operatorname* { s u p } _ { x ^ { \prime } \in B ( x , r ) } f ( x ^ { \prime } ) - f ( x ) \leq \epsilon \right\} .
$$

Lemma 2 (Lemma 3 of [11]). Suppose that $k \geq 4 C _ { \delta , n } ^ { 2 }$ . Then with probability at least $1 - \delta ,$ , the following holds for all $\boldsymbol { x } \in \mathbb { R } ^ { D }$ and $\epsilon > 0$

$$
f _ { k } ( x ) < \left( 1 + 2 \frac { C _ { \delta , n } } { \sqrt { k } } \right) ( f ( x ) + \epsilon ) ,
$$

provided k satisfies $\begin{array} { r } { { v _ { D } } \cdot \hat { r } ( x , \epsilon ) ^ { D } \cdot ( f ( x ) + \epsilon ) \geq \frac { k } { n } + C _ { \delta , n } \frac { \sqrt { k } } { n } . } \end{array}$

Analogously, define the following which characterizes how much the density decreases locally:

$$
\check { r } ( \epsilon , x ) : = \operatorname* { s u p } \left\{ r : \operatorname* { s u p } _ { x ^ { \prime } \in B ( x , r ) } f ( x ) - f ( x ^ { \prime } ) \leq \epsilon \right\} .
$$

Lemma 3 (Lemma 4 of [11]). Suppose that $k \geq 4 C _ { \delta , n } ^ { 2 }$ . Then with probability at least $1 - \delta ,$ , the following holds for all $\boldsymbol { x } \in \mathbb { R } ^ { D }$ and $\epsilon > 0$

$$
f _ { k } ( x ) \geq \left( 1 - 2 \frac { C _ { \delta , n } } { \sqrt { k } } \right) ( f ( x ) - \epsilon ) ,
$$

provided k satisfies $\begin{array} { r } { v _ { D } \cdot \check { r } ( x , \epsilon ) ^ { D } \cdot ( f ( x ) - \epsilon ) \ge \frac { k } { n } - C _ { \delta , n } \frac { \sqrt { k } } { n } . } \end{array}$

## B Proof of Theorem 1

In this section, we assume the conditions of Theorem 1. We first show that $\lambda _ { \alpha }$ , that is the density level corresponding to the α-high-density-set, is smooth in α.

Lemma 4. There exists constants $C _ { 1 } , r _ { 1 } > 0$ depending on f such that the following holds for all $0 < \epsilon < r _ { 1 }$ such that

$$
0 < \lambda _ { \alpha } - \lambda _ { \alpha - \epsilon } \leq C _ { 1 } \epsilon ^ { \beta / D } a n d 0 < \lambda _ { \alpha + \epsilon } - \lambda _ { \alpha } \leq C _ { 1 } \epsilon ^ { \beta / D } .
$$

Proof. We have

$$
\epsilon = \int _ { \mathcal { X } } 1 [ \lambda _ { \alpha - \epsilon } < f ( x ) \leq \lambda _ { \alpha } ] \cdot f ( x ) d x \geq \lambda _ { \alpha - \epsilon } \int _ { \mathcal { X } } 1 [ \lambda _ { \alpha - \epsilon } < f ( x ) \leq \lambda _ { \alpha } ] d x ,
$$

where the first equality holds by definition. Choosing  sufficiently small such that Assumption 1 holds, we have

$$
\begin{array} { r l } & { \lambda _ { \alpha - \epsilon } \displaystyle \int _ { \mathcal X } 1 [ \lambda _ { \alpha - \epsilon } < f ( x ) \le \lambda _ { \alpha } ] d x } \\ & { \ge \lambda _ { \alpha - \epsilon } \cdot \operatorname { V o l } \Big ( \Big ( H _ { \alpha } ( x ) + B \left( 0 , ( ( \lambda _ { \alpha - \epsilon } - \lambda _ { \alpha } ) / \widehat C _ { \beta } ) ^ { 1 / \beta } \right) \Big ) \setminus H _ { \alpha } ( f ) \Big ) } \\ & { \ge \lambda _ { \alpha - \epsilon } \cdot C ^ { \prime } ( ( \lambda _ { \alpha - \epsilon } - \lambda _ { \alpha } ) / \widehat C _ { \beta } ) ^ { D / \beta } , } \end{array}
$$

where the last inequality holds for some constant $C ^ { \prime }$ depending on f and Vol is the volume w.r.t. to the Lebesgue measure in $\mathbb { R } ^ { D }$ . It then follows that

$$
\lambda _ { \alpha - \epsilon } - \lambda _ { \alpha } \leq \widehat { C } _ { \beta } \left( \frac { \epsilon } { \lambda _ { \alpha - \epsilon } \cdot C ^ { \prime } } \right) ^ { \beta / D } ,
$$

and the result for the first part follows by taking $C _ { 1 } \leq \widehat { C } _ { \beta } \cdot ( \lambda _ { \alpha - r _ { 1 } } \cdot C ^ { \prime } ) ^ { - \beta / D }$ and $r _ { 1 } < \alpha$ . Showing that $0 < \lambda _ { \alpha + \epsilon } - \lambda _ { \alpha } \leq C _ { 1 } \epsilon ^ { \beta / D }$ can be done analogously and is omitted here. □

The next result gets a handle on the density level corresponding to α returned by Algorithm 1.

Lemma 5. $L e t 0 < \delta < 1$ . Let $\widehat { \varepsilon }$ be the ε setting chosen by Algorithm 1. Define

$$
\widehat { \lambda _ { \alpha } } : = \frac { k } { v _ { D } \cdot n \cdot \widehat { \varepsilon } ^ { D } } .
$$

Then, with probability at least $1 - \delta ,$ we have there exist constant $C _ { 1 } > 0$ depending on $f$ such that for n sufficiently large depending on $f ,$ we have

$$
| \widehat { \lambda } _ { \alpha } - \lambda _ { \alpha } | \leq C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) .
$$

Proof. Let $\tilde { \alpha } > 0$ . Then, we have that if $x \sim f .$ , then $\mathbb { P } ( x \in H _ { \tilde { \alpha } } ( f ) ) = 1 - \tilde { \alpha }$ . Thus, the probability that a sample point falls in $H _ { \tilde { \alpha } } ( f )$ is a Bernoulli random variable with probability $1 - \tilde { \alpha }$ . Hence, by Hoeffding’s inequality, we have that there exist constant $C ^ { \prime } > 0$ such that

$$
\mathbb { P } \left( 1 - \widetilde { \alpha } - C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } } \leq \frac { | H _ { \widetilde { \alpha } } ( f ) \cap X | } { n } \leq 1 - \widetilde { \alpha } + C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) \geq 1 - \delta / 4 .
$$

Then it follows that choosing $\alpha _ { U } : = \alpha + C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } }$ we get

$$
\mathbb { P } \left( \frac { \vert H _ { \alpha _ { U } } ( f ) \cap X \vert } { n } \leq 1 - \alpha \right) \geq 1 - \delta / 4 .
$$

Similarly, choosing $\begin{array} { r } { \alpha _ { L } = \alpha - C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } } } \end{array}$ gives us

$$
\mathbb { P } \left( \frac { \vert H _ { \alpha _ { L } } ( f ) \cap X \vert } { n } \geq 1 - \alpha \right) \geq 1 - \delta / 4 .
$$

Next, define

$$
H _ { \alpha } ^ { u p p e r } ( f ) : = \{ x \in X : f _ { k } ( x ) \geq \lambda _ { \alpha } - \epsilon \} ,
$$

where $\epsilon > 0$ will be chosen later in order for ${ \widehat { H _ { \alpha } } } ( f ) \subseteq H _ { \alpha } ^ { u p p e r } ( f )$ . By Lemma 4, there exists $C _ { 2 } , r _ { 1 } > 0$ depending on $f$ such that for $\widehat { \varepsilon } < r _ { 1 }$ (which holds for n sufficiently large depending on f by Lemma 1), we have $\begin{array} { r } { \lambda _ { \alpha } - C _ { 2 } \left( \sqrt { \frac { \log \left( 1 / \delta \right) } { n } } \right) ^ { \beta / D } \le \lambda _ { \alpha _ { L } } } \end{array}$ . As such, it suffices to choose  such that for all $x \in \mathcal { X }$ such that if $f ( x ) \geq \lambda _ { \alpha } - C _ { 2 } \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D }$ then $f _ { k } ( x ) \geq \lambda _ { \alpha } - \epsilon$ . This is because $\{ x \in X : f _ { k } ( x ) \geq \lambda _ { \alpha } - \epsilon \}$ would contain $\operatorname { \dot { \cal H } } _ { \alpha _ { L } } ( f ) \cap \mathop { X }$ , which we showed earlier contains at least $1 - \alpha$ fraction of the samples. Define $\epsilon _ { \mathrm { 0 } }$ such that $\epsilon = C _ { 2 } \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \epsilon _ { 0 }$ We have by Assumption 1,

$$
\tilde { r } ( x , \epsilon _ { 0 } ) \geq \left( \frac { 1 } { \tilde { C } _ { \beta } } \left( \epsilon _ { 0 } + C _ { 2 } \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } \right) \right) ^ { 1 / \beta } - \left( \frac { 1 } { \tilde { C } _ { \beta } } \left( C _ { 2 } \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } \right) \right) ^ { 1 / \beta } .
$$

Then, there exists constant $C ^ { \prime \prime } > 0$ sufficiently large depending on f such that if

$$
\epsilon _ { 0 } \geq C ^ { \prime \prime } \left( \left( { \sqrt { \frac { \log ( 1 / \delta ) } { n } } } \right) ^ { \beta / D } + { \frac { \log ( 1 / \delta ) { \sqrt { \log n } } } { \sqrt { k } } } \right)
$$

then the conditions in Lemma 3 are satisfied for n sufficiently large. Thus, we have for all $x \in \mathcal { X }$ with $\begin{array} { r } { f ( x ) \ge \alpha - C _ { 2 } \left( \sqrt { \frac { \log \left( 1 / \delta \right) } { n } } \right) ^ { \beta / D } } \end{array}$ , then $f _ { k } ( x ) \geq \alpha - \epsilon$ . Hence, ${ \widehat { H _ { \alpha } } } ( f ) \subseteq H _ { \alpha } ^ { u p p e r } ( f )$

We now do the same in the other direction. Define

$$
H _ { \alpha } ^ { l o w e r } ( f ) : = \{ x \in X : f _ { k } ( x ) \geq \lambda _ { \alpha } + \epsilon \} ,
$$

where  will be chosen such that $H _ { \alpha } ^ { l o w e r } ( f ) \subseteq \widehat { H _ { \alpha } } ( f )$ . By Lemma 4, it suffices to show that if $f _ { k } ( x ) \geq \lambda _ { \alpha } + \epsilon$ then $\begin{array} { r } { f ( x ) \geq \lambda _ { \alpha } + C _ { 2 } \left( \sqrt { \frac { \log \left( 1 / \delta \right) } { n } } \right) ^ { \beta / L } } \end{array}$ . This direction follows a similar argument as the previous.

Thus, there exists a constant $C _ { 1 } > 0$ depending on f such that for n sufficiently large depending on f, we have:

$$
| \widehat { \lambda } _ { \alpha } - \lambda _ { \alpha } | \leq C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) ,
$$

as desired.

The next result bounds $\widehat { H _ { \alpha } } ( f )$ between two level sets of $f .$

Lemma 6. Let $0 < \delta < 1$ . There exists constant $C _ { 1 } > 0$ depending on f such that the following holds with probability at least $1 - \delta f o r$ n sufficiently large depending on f. Define

$$
H _ { \alpha } ^ { U } ( f ) : = \left\{ x \in \mathcal { X } : f ( x ) \geq \lambda _ { \alpha } - C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) \right\}
$$

$$
H _ { \alpha } ^ { L } ( f ) : = \left\{ x \in \mathcal { X } : f ( x ) \geq \lambda _ { \alpha } + C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) \right\} .
$$

Then,

$$
H _ { \alpha } ^ { L } ( f ) \cap X \subseteq \widehat { H _ { \alpha } } ( f ) \subseteq H _ { \alpha } ^ { U } ( f ) \cap X .
$$

Proof. To simplify notation, let us define the following:

$$
K ( n , k , \delta ) : = \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) .
$$

By Lemma 5, there exists $C _ { 2 } > 0$ such that defining

$$
\begin{array} { r l } & { \widehat { H _ { \alpha } ^ { U } } ( f ) : = \left\{ x \in X : f _ { k } ( x ) \geq \lambda _ { \alpha } - C _ { 2 } \cdot K ( n , k , \delta ) \right\} } \\ & { \widehat { H _ { \alpha } ^ { L } } ( f ) : = \left\{ x \in X : f _ { k } ( x ) \geq \lambda _ { \alpha } + C _ { 2 } \cdot K ( n , k , \delta ) \right\} , } \end{array}
$$

then we have

$$
\widehat { H _ { \alpha } ^ { L } } ( f ) \subseteq \widehat { H _ { \alpha } } ( f ) \subseteq \widehat { H _ { \alpha } ^ { U } } ( f ) .
$$

It suffices to show that there exists a constant $C _ { 1 } > 0$ such that

$$
H _ { \alpha } ^ { L } ( f ) \cap X \subseteq \widehat { H _ { \alpha } ^ { L } } ( f ) \mathrm { ~ a n d ~ } \widehat { H _ { \alpha } ^ { U } } ( f ) \subseteq H _ { \alpha } ^ { U } ( f ) \cap X .
$$

$H _ { \alpha } ^ { L } ( f ) \cap X \subseteq \widehat { H ^ { L } } _ { \alpha } ( f )$ $x \in \mathcal { X }$ $f ( x ) \geq \lambda _ { \alpha } + C _ { 1 } \cdot K ( n , \bar { k } , \delta ) + \epsilon$ $f _ { k } ( x ) \geq \lambda _ { \alpha } + C _ { 1 } \cdot K ( n , k , \delta )$ $\epsilon > 0$ $\epsilon \geq C ^ { \prime } \cdot K ( n , k , \delta )$ $C ^ { \prime } > 0$ $C ^ { \prime \prime } > 0$ $f _ { k } ( x ) \leq \lambda _ { \alpha } - ( C _ { 1 } + C ^ { \prime \prime } ) \cdot K ( n , k , \delta )$ $\bar { f ( x ) } \overset { \vartriangle } { \leq } \lambda _ { \alpha } - C _ { 1 } \cdot \overr { K } ( n , k , \delta )$ $C _ { 2 } = \dot { C } _ { 1 } + \operatorname* { m a x } \{ C ^ { \prime } , C ^ { \prime \prime } \}$

We are now ready to prove Theorem 5, a more general version of Theorem 1 which makes the dependence on δ explicit. Note that if $\delta = 1 / n$ , then $\log ( 1 / \delta ) = \log ( n )$

Theorem 5. [Extends Theorem 1] Let $0 < \delta < 1$ and suppose that f is continuous and has compact support $\boldsymbol { x } \subseteq \mathbb { R } ^ { D }$ and satisfies Assumption 1. There exists constants $C _ { l } , C _ { u } , C > 0$ depending on f such that the following holds with probability at least $1 - \delta .$ . Suppose that k satisfies

$$
C _ { l } \cdot \log ( 1 / \delta ) ^ { 2 } \cdot \log n \le k \le C _ { u } \cdot \log ( 1 / \delta ) ^ { 2 D / ( 2 \beta + D ) } \cdot ( \log n ) ^ { D ( 2 \beta + D ) } \cdot n ^ { 2 \beta / ( 2 \beta + D ) } ,
$$

then we have

$$
\begin{array} { r } { d _ { H } ( H _ { \alpha } ( f ) , \widehat { H _ { \alpha } } ( f ) ) \leq C \cdot \left( \log ( 1 / \delta ) ^ { 1 / 2 D } \cdot n ^ { - 1 / 2 D } + \log ( 1 / \delta ) ^ { 1 / \beta } \cdot \log ( n ) ^ { 1 / 2 \beta } \cdot k ^ { - 1 / 2 \beta } \right) . } \end{array}
$$

Proof of Theorem 5. Again, to simplify notation, let us define the following:

$$
K ( n , k , \delta ) : = \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / D } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) .
$$

There are two directions to show for the Hausdorff distance result. That (i) m $\mathrm { a x } _ { x \in \widehat { H _ { \alpha } } ( f ) } d ( x , H _ { \alpha } ( f ) )$ is bounded, that is none of the high-density points recovered by Algorithm 1 are far from the true high-density region; and (ii) that $\begin{array} { r } { \operatorname* { s u p } _ { x \in H _ { \alpha } ( f ) } d ( x , \widehat { H _ { \alpha } } ( f ) ) } \end{array}$ is bounded, that Algorithm 1 recovers a good covering of the entire high-density region.

We first show (i). By Lemma 6, we have that there exists $C _ { 1 } > 0$ such that

$$
H _ { \alpha } ^ { U } ( f ) : = \{ x \in \mathcal { X } : f ( x ) \geq \lambda _ { \alpha } - C _ { 1 } K ( n , k , \delta ) \}
$$

contains $\widehat { H _ { \alpha } } ( f )$ . Thus,

$$
\operatorname* { m a x } _ { x \in \overline { { H _ { \alpha } } } ( f ) } \ d ( x , H _ { \alpha } ( f ) ) \leq \operatorname* { s u p } _ { x \in H _ { \alpha } ^ { U } ( f ) } d ( x , H _ { \alpha } ( f ) ) \leq \bigg ( C _ { 1 } \cdot K ( n , k , \delta ) \cdot \frac { 1 } { \overline { { C } } _ { \beta } } \bigg ) ^ { 1 / \beta } ,
$$

where the second inequality holds by Assumption 1. Now for the other direction, we have by triangle inequality that

$$
\operatorname* { s u p } _ { x \in H _ { \alpha } ( f ) } d ( x , \widehat H _ { \alpha } ( f ) ) \leq \operatorname* { s u p } _ { x \in H _ { \alpha } ( f ) } d ( x , H _ { \alpha } ^ { L } ( f ) ) + \operatorname* { s u p } _ { x \in H _ { \alpha } ^ { L } ( f ) } d ( x , \widehat H _ { \alpha } ( f ) ) .
$$

The first term can be bounded by using Assumption 1:

$$
\operatorname* { s u p } _ { x \in H _ { \alpha } ( f ) } d ( x , H _ { \alpha } ^ { L } ( f ) ) \leq \left( C _ { 1 } \cdot K ( n , k , \delta ) \cdot \frac { 1 } { \check { C } _ { \beta } } \right) ^ { 1 / \beta } .
$$

Now for the second term, we see that by Lemma $6 , \widehat { H _ { \alpha } } ( f )$ contains all of the sample points of $H _ { \alpha } ^ { L } ( f )$ Thus, we have

$$
\operatorname* { s u p } _ { x \in H _ { \alpha } ^ { L } ( f ) } d ( x , \widehat H _ { \alpha } ( f ) ) \leq \operatorname* { s u p } _ { x \in H _ { \alpha } ^ { L } ( f ) } d ( x , H _ { \alpha } ^ { L } ( f ) \cap X ) .
$$

By Assumption 1, for $r \ < \ r _ { 0 }$ , and $x \in H _ { \alpha } ^ { L } ( f )$ we have $\mathcal { F } ( B ( x , r ) ) \ge \rho r ^ { D }$ , where $\mathcal { F }$ is the distribution corresponding to $f .$ Choosing $\begin{array} { r } { r \ge \left( \frac { C _ { \delta , n } } { \rho } \frac { \sqrt { D \log n } } { n } \right) ^ { 1 / D } } \end{array}$ gives us that by Lemma 1 that $\mathcal { F } _ { n } ( B ( x , r ) ) > 0$ where $\mathcal { F } _ { n }$ is the distribution of X and thus, we have

$$
\operatorname* { s u p } _ { x \in H _ { \alpha } ^ { L } ( f ) } d ( x , H _ { \alpha } ^ { L } ( f ) \cap X ) \leq \left( \frac { C _ { \delta , n } } { \rho } \frac { \sqrt { D \log n } } { n } \right) ^ { 1 / D } ,
$$

which is dominated by the error contributed by the other error and the result follows. □

## C Supporting results for Theorem 2 Proof

$\mathcal { F } _ { n }$ $1 / n$ $C _ { 0 }$ $1 - \delta .$ $x \in X \cup { \mathcal { N } } ,$

$$
\begin{array} { l l l } { \displaystyle \mathcal { F } ( B ) \geq C _ { \delta , n } \frac { \sqrt { d \log n } } { n } \Rightarrow \mathcal { F } _ { n } ( B ) > 0 } \\ { \displaystyle \mathcal { F } ( B ) \geq \frac { k } { n } + C _ { \delta , n } \frac { \sqrt { k } } { n } \Rightarrow \mathcal { F } _ { n } ( B ) \geq \frac { k } { n } } \\ { \displaystyle \mathcal { F } ( B ) \leq \frac { k } { n } - C _ { \delta , n } \frac { \sqrt { k } } { n } \Rightarrow \mathcal { F } _ { n } ( B ) < \frac { k } { n } , } \end{array}
$$

where $C _ { \delta , n } = C _ { 0 } \log ( 2 / \delta ) \sqrt { d \log n } , \mathcal { F } _ { n }$ is the empirical distribution, and $k \geq C _ { \delta , n }$

Definition 5 (k-NN Density Estimator on Manifold).

$$
f _ { k } ( x ) : = \frac { k } { n \cdot v _ { d } \cdot r _ { k } ( x ) ^ { d } } .
$$

Lemma 8 (Manifold version of $f _ { k }$ upper bound [28]). Define the following which charaterizes how much the density increases locally in M:

$$
\hat { r } ( \epsilon , x ) : = \operatorname* { s u p } \left\{ r : \operatorname* { s u p } _ { x ^ { \prime } \in B ( x , r ) \cap M } f ( x ^ { \prime } ) - f ( x ) \leq \epsilon \right\} .
$$

Fix $\lambda _ { 0 } > 0$ and $\delta > 0$ and suppose that $k \geq C _ { \delta , n } ^ { 2 }$ . Then there exists constant $C _ { 1 } \equiv C _ { 1 } ( \lambda _ { 0 } , d , \tau )$ such that if

$$
k \leq C _ { 1 } \cdot C _ { \delta , n } ^ { 2 d / ( 2 + d ) } \cdot n ^ { 2 / ( 2 + d ) } ,
$$

then the following holds with probability at least $1 - \delta$ uniformly in $\epsilon > 0$ and $x \in X$ with $f ( x ) + \epsilon \geq \lambda _ { 0 } { : }$

$$
f _ { k } ( x ) < \left( 1 + 3 \cdot \frac { C _ { \delta , n } } { \sqrt { k } } \right) \cdot ( f ( x ) + \epsilon ) ,
$$

provided k satisfies $\begin{array} { r } { v _ { d } \cdot \widehat { r } ( \epsilon , x ) ^ { d } \cdot ( f ( x ) + \epsilon ) \geq \frac { k } { n } - C _ { \delta , n } \frac { \sqrt { k } } { n } . } \end{array}$

Lemma 9 (Manifold version of $f _ { k }$ lower bound [28]). Define the following which charaterizes how much the density decreases locally in M:

$$
\check { r } ( \epsilon , x ) : = \operatorname* { s u p } \left\{ r : \operatorname* { s u p } _ { x ^ { \prime } \in B ( x , r ) \cap M } f ( x ) - f ( x ^ { \prime } ) \leq \epsilon \right\} .
$$

Fix $\lambda _ { 0 } > 0$ and $0 < \delta < 1$ and suppose $k \geq C _ { \delta , n }$ . Then there exists constant $C _ { 2 } \equiv C _ { 2 } ( \lambda _ { 0 } , d , \tau )$ such that if

$$
k \leq C _ { 2 } \cdot C _ { \delta , n } ^ { 2 d / ( 4 + d ) } \cdot n ^ { 4 / ( 4 + d ) } ,
$$

then with probability at least $1 - \delta ,$ , the following holds uniformly for all $\epsilon > 0$ and $x \in X$ with $f ( x ) - \epsilon \geq \lambda _ { 0 } { : }$

$$
f _ { k } ( x ) \geq \left( 1 - 3 \cdot \frac { C _ { \delta , n } } { \sqrt { k } } \right) \cdot ( f ( x ) - \epsilon ) ,
$$

provided k satisfies $\begin{array} { r } { v _ { d } \cdot \check { r } ( \epsilon , x ) ^ { d } \cdot ( f ( x ) - \epsilon ) \geq \frac { 4 } { 3 } \left( \frac { k } { n } + C _ { \delta , n } \frac { \sqrt { k } } { n } \right) } \end{array}$

## D Proof of Theorem 2

The proof essentially follows the same structure as the full-dimensional case, with the primary difference in the density estimation bounds.

Lemma 10 (Manifold Version of Lemma 4). There exists constants $C _ { 1 } , r _ { 1 } > 0$ depending on $f$ such that the following holds for all $0 < \epsilon < r _ { 1 }$ such that

$$
0 < \lambda _ { \alpha } - \lambda _ { \alpha - \epsilon } \leq C _ { 1 } \epsilon ^ { \beta / d } a n d 0 < \lambda _ { \alpha + \epsilon } - \lambda _ { \alpha } \leq C _ { 1 } \epsilon ^ { \beta / d } .
$$

Proof. The proof follows the same structure as the proof of Lemma $^ { 4 , }$ with the difference being the change in dimension, and is omitted here. □

Lemma 11 (Manifold Version of Lemma 5). Let $0 < \delta < 1$ . Let ε be the ε setting chosen by Algorithm 1 after the binary search procedure. Define

$$
\widehat { \lambda _ { \alpha } } : = \frac { k } { v _ { D } \cdot n \cdot \widehat { \varepsilon } ^ { d } } .
$$

Then, with probability at least $1 - \delta ,$ , we have there exist constant $C _ { 1 } > 0$ depending on $f$ and M such that for n sufficiently large depending on $f$ and M, we have

$$
| \widehat { \lambda } _ { \alpha } - \lambda _ { \alpha } | \leq C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / d } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) .
$$

$k ~ \lesssim ~ \mathsf { \bar { n } } ^ { 2 \beta / ( 2 \beta + d ) }$ $k \lesssim$ $\stackrel {  } { \{ n ^ { 2 / ( 2 + d ) } , n ^ { 2 \beta / ( 2 \beta + d ) } \} } = n ^ { 2 \operatorname* { i n } \{ 1 , \beta \} / ( 2 \beta ^ { \prime } + d ) }$

Lemma 12 (Manifold Version of Lemma $5 )$ . Let $0 < \delta < 1$ . There exists constant $C _ { 1 } > 0$ depending on $f$ and M such that the following holds with probability at least 1 − δ for n sufficiently large depending on $f$ and M. Define

$$
H _ { \alpha } ^ { U } ( f ) : = \left\{ x \in \mathcal { X } : f ( x ) \geq \lambda _ { \alpha } - C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / d } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) \right\}
$$

$$
H _ { \alpha } ^ { L } ( f ) : = \left\{ x \in \mathcal { X } : f ( x ) \geq \lambda _ { \alpha } + C _ { 1 } \left( \left( \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) ^ { \beta / d } + \frac { \log ( 1 / \delta ) \sqrt { \log n } } { \sqrt { k } } \right) \right\} .
$$

Then,

$$
H _ { \alpha } ^ { L } ( f ) \cap X \subseteq \widehat { H _ { \alpha } } ( f ) \subseteq H _ { \alpha } ^ { U } ( f ) \cap X .
$$

Proof. Same comment as the proof for Lemma 11.

Theorem 6. [Extends Theorem 2] Let $0 < \delta < 1$ . Suppose that density function $f$ is continuous and supported on M and Assumptions 1 and 2 hold. Suppose also that there exists $\lambda _ { 0 } > 0$ such that $f ( x ) \geq \lambda _ { 0 }$ for all $x \in M$ . Then, there exists constants $C _ { l } , C _ { u } , C > 0$ depending on f such that the following holds with probability at least $1 - \delta .$ . Suppose that k satisfies,

$$
C _ { l } \cdot \log ( 1 / \delta ) ^ { 2 } \cdot \log n \leq k \leq C _ { u } \cdot \log ( 1 / \delta ) ^ { 2 d / ( 2 \beta ^ { \prime } + d ) } \cdot ( \log n ) ^ { d ( 2 \beta ^ { \prime } + d ) } \cdot n ^ { 2 \beta ^ { \prime } / ( 2 \beta ^ { \prime } + d ) }
$$

where $\beta ^ { \prime } : = \operatorname* { m a x } \{ 1 , \beta \}$ . Then we have

$$
\begin{array} { r } { d _ { H } ( H _ { \alpha } ( f ) , \widehat { H _ { \alpha } } ( f ) ) \leq C \cdot \left( \log ( 1 / \delta ) ^ { 1 / 2 d } \cdot n ^ { - 1 / 2 d } + \log ( 1 / \delta ) ^ { 1 / \beta } \cdot \log ( n ) ^ { 1 / 2 \beta } \cdot k ^ { - 1 / 2 \beta } \right) . } \end{array}
$$

Proof of Theorem 6. Proof is the same as the full-dimensional case given the contributed Lemmas of this section and is omitted here. □

## E Supporting Results for Theorem 3 Proof

Next, we need the following on the volume of the intersection of the Euclidean ball and $M ;$ this is required to get a handle on the true mass of the ball under $\mathcal { F } _ { M }$ in later arguments. The upper and lower bounds follow from [5] and Lemma 5.3 of [41]. The proof can be found e.g. in [28].

Lemma 13 (Ball Volume). $I f 0 < r <$ min $\{ \tau / 4 d , 1 / \tau \}$ , and $x \in M$ then

$$
v _ { d } r ^ { d } ( 1 - \tau ^ { 2 } r ^ { 2 } ) \leq \nu o l _ { d } ( B ( x , r ) \cap M ) \leq v _ { d } r ^ { d } ( 1 + 4 d r / \tau ) ,
$$

where $v _ { d }$ is the volume of a unit ball $i n \mathbb { R } ^ { d }$ and $\nu o l _ { d }$ is the volume w.r.t. the uniform measure on $M .$

The next is a bound uniform convergence of balls:

Lemma 14 (Lemma 3 of [29]). Let B be the set of all balls in $\mathbb { R } ^ { D } , \mathcal { F }$ is some distribution and $\mathcal { F } _ { n }$ is an empirical distribution. With probability at least $1 - \delta ,$ , the following holds uniformly for every $B \in \mathcal { \dot { B } } a n d \gamma \geq 0 ;$

$$
\begin{array} { r l } & { \mathcal { F } ( B ) \geq \gamma \Rightarrow \mathcal { F } _ { n } ( B ) \geq \gamma - \beta _ { n } \sqrt { \gamma } - \beta _ { n } ^ { 2 } , } \\ & { \mathcal { F } ( B ) \leq \gamma \Rightarrow \mathcal { F } _ { n } ( B ) \leq \gamma + \beta _ { n } \sqrt { \gamma } + \beta _ { n } ^ { 2 } , } \end{array}
$$

where $\beta _ { n } = 8 d \log ( 1 / \delta ) \sqrt { \log n / n } .$

## F Proof of Theorem 3

The first result says that within the manifold, the vast majority of the probability mass is attributed to the manifold distributions.

Lemma 15. There exists $C _ { 1 } , r _ { 1 } > 0$ depending on $\mathcal { F } _ { M } , \mathcal { F } _ { E } , M$ such that the following holds uniformly over $x \in M$ and $0 < r < r _ { 1 }$

$$
\frac { \mathcal { F } _ { E } ( B ( x , r ) ) } { \mathcal { F } _ { M } ( B ( x , r ) ) } \leq C _ { 1 } \cdot r ^ { D - d } .
$$

Proof. Let $x \in M$ and $r > 0$ . We have

$$
\begin{array} { r } { \mathcal { F } _ { M } ( B ( x , r ) ) \geq \lambda _ { 0 } \cdot \mathsf { v o l } _ { d } ( B ( x , r ) \cap M ) \geq v _ { d } r ^ { d } ( 1 - \tau ^ { 2 } r ^ { 2 } ) \cdot \lambda _ { 0 } , } \end{array}
$$

where the second inequality holds by Lemma 13 for r sufficiently small. On the other hand, we have

$$
\mathcal { F } _ { E } ( B ( x , r ) ) \leq | | f _ { E } | | _ { \infty } v _ { D } r ^ { D } .
$$

Thus, we have there exists $C _ { 1 } > 0$ depending on $f _ { M } , M ,$ , and $f _ { E }$ such that

$$
\frac { \mathcal { F } _ { E } ( B ( x , r ) ) } { \mathcal { F } _ { M } ( B ( x , r ) ) } \leq C _ { 1 } \cdot r ^ { D - d } ,
$$

as desired.

We next show that points far away from $H _ { \widetilde { \alpha } } ( f _ { M } )$ do not get selected as high-density points by Algorithm 1.

Lemma 16. There exists $\omega _ { 0 } > 0$ such that for any $0 < \omega < \omega _ { 0 }$ and n sufficiently large depending on F , F , M and $\omega ,$ with probability at least $1 - \delta ,$ , Algorithm 1 will not select any points outside of $H _ { \widetilde { \alpha } - \omega } ( f _ { M } )$

Proof. By Assumption 1, we can choose ω sufficiently small so that for the density $f _ { M } , | \lambda _ { \widetilde { \alpha } - \omega } - \frac { } { }$ $\lambda _ { \widetilde { \alpha } } | \overset { \cdot } { \leq } \check { C } _ { \beta } \cdot ( r _ { c } / 3 ) ^ { \bar { \beta } }$ . Then, at the $\left( \widetilde { \alpha } - \omega \right)$ -density level, we will be within the area where the regularity <sup>e</sup>assumptions hold.

Next, by Hoeffding’s inequality, we have that there exist constant $C ^ { \prime } > 0$ such that for $\bar { \alpha } > 0 \mathrm { { : } }$

$$
\mathbb { P } \left( 1 - \bar { \alpha } - C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } } \leq \frac { | H _ { \frac { \bar { \alpha } - \eta } { 1 - \eta } } ( f _ { M } ) \cap X | } { n } \leq 1 - \bar { \alpha } + C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } } \right) \geq 1 - \delta / 3 .
$$

Choosing $\begin{array} { r } { \bar { \alpha } = \alpha - C ^ { \prime } \sqrt { \frac { \log ( 1 / \delta ) } { n } } } \end{array}$ , then it follows that with probability at least $1 - \delta / 3$

$$
H _ { 0 } : = H _ { \widetilde { \alpha } - C ^ { \prime } \sqrt { \log ( 1 / \delta ) } / ( \sqrt { n } \cdot ( 1 - \eta ) ) } ( f _ { M } )
$$

satisfies $| H _ { 0 } \cap X | > ( 1 - \alpha ) \cdot n$ . Next let

$$
H _ { \omega } : = H _ { \widetilde { \alpha } - \omega } ( f _ { M } ) .
$$

Let $r$ be the value of ε used by Algorithm 1. Now, it suffices to show that for n sufficiently large depending on $f _ { M } { : }$

$$
\operatorname* { m a x } _ { x \in X \setminus H _ { \omega } } \mathcal { F } _ { n } ( B ( x , r ) ) < \operatorname* { m i n } _ { x \in H _ { 0 } } \mathcal { F } _ { n } ( B ( x , r ) ) ,
$$

where ${ \mathcal { F } } _ { n }$ is the empirical distribution. This is because Algorithm 1 filters out sample points whose ε-ball has less than k sample points for its final ε value, which is the value which allows it to filter α-fraction of the points.

By Lemma 15, it suffices to show that

$$
\operatorname* { m a x } _ { x \in X \setminus H _ { \omega } } \mathcal { F } _ { M , n } ( B ( x , r ) ) \left( 1 + C _ { 1 } r ^ { D - d } \right) < \operatorname* { m i n } _ { x \in H _ { 0 } } \mathcal { F } _ { M , n } ( B ( x , r ) ) \left( 1 - C _ { 1 } r ^ { D - d } \right) ,
$$

where $\mathcal { F } _ { M , n } ( A )$ denote the fraction of samples drawn from $\mathcal { F } _ { M }$ which lie in A w.r.t. our entire sample X.

Then, by Lemma 14, it will be enough to show that

$$
\begin{array} { r l } {  { \operatorname* { m a x } _ { x \in X \backslash H _ { \omega } } ( \mathcal { F } _ { M } ( B ( x , r ) ) + \beta _ { n } \sqrt { \mathcal { F } _ { M } ( B ( x , r ) ) } + \beta _ { n } ^ { 2 } ) ( 1 + C _ { 1 } r ^ { D - d } ) } \quad } & { } \\ & { < \operatorname* { m i n } _ { x \in H _ { 0 } } ( \mathcal { F } _ { M } ( B ( x , r ) ) - \beta _ { n } \sqrt { \mathcal { F } _ { M } ( B ( x , r ) ) } - \beta _ { n } ^ { 2 } ) ( 1 - C _ { 1 } r ^ { D - d } ) , } \end{array}
$$

where $\beta _ { n } = 8 d \log ( 1 / \delta ) \sqrt { \log n / n } .$

To bound the LHS, we have by Lemma 13

$$
\begin{array} { r l } {  { \operatorname* { m a x } _ { x \in X \backslash H _ { \omega } } ( \mathcal { F } _ { M } ( B ( x , r ) ) + \beta _ { n } \cdot \sqrt { \mathcal { F } _ { M } ( B ( x , r ) ) } + \beta _ { n } ^ { 2 } ) ( 1 + C _ { 1 } r ^ { D - d } ) } } \\ & { \le \operatorname* { m a x } _ { x \in X \backslash H _ { \omega } } \{ ( \operatorname* { i n f } _ { x ^ { \prime } \in B ( x , r ) } f _ { M } ( x ^ { \prime } ) ) \cdot ( 1 + \beta _ { n } / \sqrt { \| f _ { M } \| _ { \infty } } + \beta _ { n } ^ { 2 } / \| f _ { M } \| _ { \infty } ) ( 1 + C _ { 1 } r ^ { D - d } ) ( 1 + 4 d r / \tau ) \} } \\ & { \le \operatorname* { m a x } _ { x \in X \backslash H _ { \omega } } \{ ( \operatorname* { i n f } _ { x ^ { \prime } \in B ( x , r ) } f _ { M } ( x ^ { \prime } ) ) ( 1 + C _ { 2 } \beta _ { n } + C _ { 3 } r ) \} } \\ & { \le ( \lambda _ { \bar { \alpha } - \omega } + \iota ( f _ { M } , r ) ) ( 1 + C _ { 2 } \beta _ { n } + C _ { 3 } r ) , } \end{array}
$$

for some $C _ { 2 } , C _ { 3 } \quad > \quad 0$ and ι is the modulus of continuity, that is $\begin{array} { r l } { \iota ( f _ { M } , r ) } & { { } : = } \end{array}$ $\begin{array} { r } { \operatorname* { s u p } _ { x , x ^ { \prime } \in M : | x - x ^ { \prime } | \leq r } | f _ { M } ( x ) - f _ { M } ( x ^ { \prime } ) | } \end{array}$ (i.e. $f _ { M }$ is uniformly continuous since it is continuous over a compact support, so $\iota ( f _ { M } , r ) \to 0 \mathrm { a s } r \to 0 )$

Similarly, for the RHS, we can show for some constants $C _ { 4 } , C _ { 5 }$ that

$$
\begin{array} { r l } & { \underset { x \in H _ { 0 } } { \operatorname* { m i n } } \big ( \mathcal { F } _ { M } ( B ( x , r ) ) - \beta _ { n } \sqrt { \mathcal { F } _ { M } ( B ( x , r ) ) } - \beta _ { n } ^ { 2 } \big ) \big ( 1 - C _ { 1 } r ^ { D - d } \big ) } \\ & { \geq \big ( \lambda _ { \widetilde { \alpha } - C ^ { \prime } } \sqrt { \log ( 1 / \delta ) } / ( \sqrt { n } ( 1 - \eta ) ) - \iota ( f _ { M } , r ) \big ) \big ( 1 - C _ { 4 } \beta _ { n } - C _ { 5 } r \big ) . } \end{array}
$$

The result follows since $r  0$ as $n \to \infty$ (since by Lemma 1, r is a k-NN radius so $r \lesssim ( k / n ) ^ { 1 / D } \to$ 0 given the conditions on k of Theorem 3) and the fact that $\lambda _ { \widetilde { \alpha } - \omega } < \lambda _ { \widetilde { \alpha } - C ^ { \prime } \sqrt { \log ( 1 / \delta ) } / \sqrt { n } }$ for n sufficiently large. As desired. □

Lemma 17 (Bounding density estimators w.r.t to entire sample vs w.r.t. samples on manifold). For $\boldsymbol { x } \in \mathbb { R } ^ { D }$ , define the following:

$$
\begin{array} { r l } & { r _ { k } ( x ) : = \operatorname* { i n f } \{ \epsilon > 0 : | B ( x , \epsilon ) \cap X | \ge k \} } \\ & { \widetilde { r _ { k } } ( x ) : = \operatorname* { i n f } \{ \epsilon > 0 : | B ( x , \epsilon ) \cap X \cap M | \ge k \} } \end{array}
$$

where the former is simply the k-NN radius we’ve been using thus far and the latter is the k-NN radius if we were to restrict the samples to only those that came from M . Then likewise, define the analogous density estimators:

$$
f _ { k } ( x ) : = \frac { k } { n \cdot v _ { d } \cdot r _ { k } ( x ) ^ { d } } a n d \widetilde f _ { k } ( x ) : = \frac { k } { n \cdot v _ { d } \cdot \widetilde { r _ { k } } ( x ) ^ { d } } ,
$$

where again, the former is the usual k-NN density estimator on manifolds. Then, there exists $C _ { 1 }$ such that the following holds with high probability.

$$
\operatorname* { s u p } _ { x \in M } | f _ { k } ( x ) - \widetilde { f } _ { k } ( x ) | \leq C _ { 1 } \cdot ( k / n ) ^ { D / d - 1 } .
$$

Proof. By Lemma 14, there exists $C _ { 2 } > 0$ depending on $\mathcal { F }$ and $\mathcal { F } _ { M }$ such that

$$
\begin{array} { r } { \mathcal { F } _ { n } ( B ( x , r _ { k } ( x ) ) = k \Rightarrow | \mathcal { F } ( B ( x , r _ { k } ( x ) ) - k | \leq C _ { 2 } \beta _ { n } , } \end{array}
$$

and

$$
\mathcal { F } _ { M , n } ( B ( x , \widetilde { r _ { k } } ( x ) ) = k \Rightarrow | \mathcal { F } _ { M } ( B ( x , \widetilde { r _ { k } } ( x ) ) - k | \leq C _ { 2 } \beta _ { n } ,
$$

where ${ \mathcal { F } } _ { M , n }$ is the empirical distribution w.r.t. $X \cap M$ . Next, by Lemma 15, we have for some constant $C _ { 3 } > 0 !$

$$
\begin{array} { r l } & { \mathcal { F } ( B ( x , \widetilde { r _ { k } } ( x ) ) \leq \mathcal { F } _ { M } ( B ( x , \widetilde { r _ { k } } ( x ) ) ( 1 + C _ { 3 } \widetilde { r _ { k } } ( x ) ^ { D - d } ) } \\ & { \qquad \leq ( k + C _ { 2 } \beta _ { n } ) ( 1 + C _ { 3 } \cdot \widetilde { r _ { k } } ( x ) ^ { D - d } ) } \\ & { \qquad \leq ( k + C _ { 2 } \beta _ { n } ) ( 1 + C _ { 4 } \cdot ( k / n ) ^ { D / d - 1 } ) } \\ & { \qquad \leq k \cdot ( 1 + C _ { 5 } ( k / n ) ^ { D / d - 1 } ) , } \end{array}
$$

where the second last inequality holds for some constant $C _ { 4 } > 0$ by Lemma 7 and $C _ { 5 } > 0$ is some constant depending on $\mathcal { F }$ and ${ \dot { \mathcal { F } } } _ { M }$ and M . Then it follows that for some constant $C _ { 6 } > 0$ , we have

$$
\frac { \mathcal { F } ( B ( x , \widetilde { r _ { k } } ( x ) ) } { \mathcal { F } ( B ( x , r _ { k } ( x ) ) } \le 1 + C _ { 6 } ( k / n ) ^ { D / d - 1 } .
$$

In the other direction, we trivially have $\widetilde { r _ { k } } ( x ) \geq r _ { k } ( x )$ , so

$$
1 \leq \frac { \mathcal { F } ( B ( x , \widetilde { r _ { k } } ( x ) ) } { \mathcal { F } ( B ( x , r _ { k } ( x ) ) } \leq 1 + C _ { 6 } ( k / n ) ^ { D / d - 1 } .
$$

The result follows.

$0 < \eta < \alpha < 1$ $0 < \delta < 1$ $( 1 - \eta ) \cdot \mathcal { F } _ { M } + \eta \cdot \mathcal { F } _ { E }$ $\mathcal { F } _ { M }$ $f _ { M }$ $\mathcal { F } _ { E }$ $f _ { E }$ $\mathbb { R } ^ { D }$ $d < D$ $\lambda _ { 0 } > 0$ $f _ { M } ( x ) \geq \lambda _ { 0 }$ $x \in M$ $H _ { \widetilde \alpha } ( f _ { M } )$ $\begin{array} { r } { \widetilde \alpha : = \frac { \dot { \alpha } - \eta } { 1 - \eta } ) } \end{array}$ $f _ { M }$ $\widehat { H } _ { \alpha }$

Then, there exists constants $C _ { l } , C _ { u } , C > 0$ depending on $f _ { M } , f _ { E } , \eta ,$ M such that the following holds with probability at least $1 - \delta$ . Suppose that k satisfies

$$
C _ { l } \cdot \log ( 1 / \delta ) ^ { 2 } \cdot \log n \leq k \leq C _ { u } \cdot \log ( 1 / \delta ) ^ { 2 d / ( 2 \beta ^ { \prime } + d ) } \cdot ( \log n ) ^ { d ( 2 \beta ^ { \prime } + d ) } \cdot n ^ { 2 \beta ^ { \prime } / ( 2 \beta ^ { \prime } + d ) }
$$

where $\beta ^ { \prime } : = \operatorname* { m a x } \{ 1 , \beta \}$ . Then we have

$$
d _ { H } ( H _ { \widetilde { \alpha } } ( f _ { M } ) , \widehat { H _ { \alpha } } ) \leq C \cdot \left( \log ( 1 / \delta ) ^ { 1 / 2 d } \cdot n ^ { - 1 / 2 d } + \log ( 1 / \delta ) ^ { 1 / \beta } \cdot \log ( n ) ^ { 1 / 2 \beta } \cdot k ^ { - 1 / 2 \beta } \right) .
$$

Proof of Theorem 7. The proof follows in a similar way as that of Theorem 6, except with the complexity of having added full-dimensional noise. We will only highlight the difference and provide a sketch of the proof here.

Lemma 16 and 17 give us a handle on the additional complexity when having separate noise distribution, compared to the earlier manifold setting of Theorem 2.

Lemma 16 guarantees that the points in $\widehat { H _ { \alpha } }$ lie in the inside of M with margin. In particular, that means the noise points are filtered out by the algorithm and thus, we are reduced to reasoning about the α-high-density-set of $f _ { M }$

Then, Lemma 17 ensures that the k-NN density estimator used for our analysis for the entire sample X is actually quite close to the k-NN density estimator with respect to $M \cap X$ within M . In other words, we can use the k-NN density estimator to estimate $f _ { M }$ without knowing which samples of X were in M. Lemma 17 shows that the additional error in density estimation we obtain is $\approx ( k / n ) ^ { D / d - 1 } \lesssim ( k / n ) ^ { 1 / d } \lesssim ( \log n ) / \sqrt { k }$ , where the first inequality holds since $D > d$ and the latter holds from the conditions on k. It turns out that this error term can be absorbed as a constant in the previous result of Theorem 6. □

## G Proof of Theorem 4

Proof of Theorem 4. For the first inequality, we have

$$
\xi ( h , x ) \ge \frac { d ( x , M _ { \tilde { h } ( x ) } ) - \epsilon _ { n } } { d ( x , M _ { h ( x ) } ) + \epsilon _ { n } } = \frac { d ( x , M _ { \tilde { h } ( x ) } ) } { d ( x , M _ { h ( x ) } ) } - \frac { \epsilon _ { n } } { d ( x , M _ { h ( x ) } ) + \epsilon _ { n } } \cdot \left( \frac { d ( x , M _ { \tilde { h } ( x ) } ) } { d ( x , M _ { h ( x ) } ) } + 1 \right) ,
$$

where the first inequality holds by Theorem 3. This, along with the condition on γ and $\varepsilon ( h , x )$ fromo the theorem statement, implies that

$$
\frac { d ( x , M _ { \widetilde { h } ( x ) } ) } { d ( x , M _ { h ( x ) } ) } < 1 - \gamma ,
$$

which implies that $h ( x ) \neq h ^ { * } ( x )$ . For the second inequality, we have

$$
\frac { 1 } { \xi ( h , x ) } \geq \frac { d ( x , M _ { h ( x ) } ) - \epsilon _ { n } } { d ( x , M _ { \tilde { h } ( x ) } ) + \epsilon _ { n } } = \frac { d ( x , M _ { h ( x ) } ) } { d ( x , M _ { \tilde { h } ( x ) } ) } - \frac { \epsilon _ { n } } { d ( x , M _ { \tilde { h } ( x ) } ) + \epsilon _ { n } } \cdot \left( \frac { d ( x , M _ { h ( x ) } ) } { d ( x , M _ { \tilde { h } ( x ) } ) } + 1 \right) ,
$$

where the first inequality holds by Theorem 3. Thus, if the condition of the theorem statement holds, then

$$
\frac { d ( x , M _ { h ( x ) } ) } { d ( x , M _ { \tilde { h } ( x ) } ) } < 1 - \gamma \Rightarrow \frac { d ( x , M _ { h ( x ) } ) } { d ( x , M _ { c } ) } < 1 - \gamma
$$

for all $c \neq h ( x )$ , which implies that $h ( x ) = h ^ { \ast } ( x )$

## H Additional UCI Experiments

## H.1 When to trust: Precision for correct predictions by percentile

![](images/65cc1c499a038aaf500f0c6ee69df83c6ec1b1962727a462cf03919edcfea15c.jpg)  
Figure 4: UCI data sets and precision on correctness

![](images/d6f259e4cccbc356a16f5a65aa4fa3a19d06a10cf815838620f3805ef3e2ec8b.jpg)  
Figure 5: UCI data sets and precision on incorrectness

## H.3 High dimensional Datasets

![](images/3c3ddc9824e198715c0633e86e73d14b4f7180c453fb5f1619bdd42fa6430146.jpg)  
(a) MNIST

![](images/02b645dd8d56b847f91e7c21fd025af9b84d0cc5f14154285d7dd9d71b931f63.jpg)  
(b) MNIST

![](images/b7f03cb2d22cd87f8e36df490b1f489702d6ebd0a86ce880c57889fe4abc6f52.jpg)  
(c) SVHN

![](images/28f00480b67aee68c904208885e04c1acb9e1a6b1c4d73f65ca25a5c945320ff.jpg)  
(d) SVHN

![](images/f0eba228bdcbcd9741ce3368a12a68e1c5e8282b08c94cecdd7d56a68c71461a.jpg)  
(e) CIFAR-10

![](images/fc98127b25f98fc6aaf53763dece23d1b936d61dfca92f4f2cd2640a7c72afd4.jpg)  
(f) CIFAR-10

![](images/0e4719d268305a193348cb86d1bfaa888b4a125b02cf58db93f66b0090da6950.jpg)  
(g) CIFAR-100

![](images/5f9f82953cf27aea90fc4095a886b69952d56061a71a8b50cba5d12afca832be.jpg)  
(h) CIFAR-100  
Figure 6: Trust score results using convolutional neural networks on MNIST, SVHN, CIFAR-10, and CIFAR-100 datasets. Left column is detecting trustworthy; right column is detecting suspicious.