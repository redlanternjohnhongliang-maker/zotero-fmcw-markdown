# Conditional computation in neural networks: principles and research trends

SIMONE SCARDAPANE\*<sup>1</sup>, ALESSANDRO BAIOCCHI<sup>2</sup>, ALESSIO DEVOTO<sup>2</sup>, VALERIO MARSOCCI<sup>3</sup>, PASQUALE MINERVINI<sup>4</sup>, AND JARY POMPONI<sup>1</sup>

<sup>1</sup>DIET Department, Sapienza University of Rome <sup>2</sup>DIAG Department, Sapienza University of Rome <sup>3</sup>Geomatics Research Group, KU Leuven <sup>4</sup>School of Informatics, University of Edinburgh

July 9, 2024

Please cite the published version as Scardapane, S. et al., 2024. Conditional computation in neural networks: principles and research trends. Intelligenza Artificiale, in press, pp. 1-16. Feedback can be submitted to simone.scardapane@uniroma1.it.

## Abstract

This article summarizes principles and ideas from the emerging area of applying conditional computation methods to the design of neural networks. In particular, we focus on neural networks that can dynamically activate or de-activate parts of their computational graph conditionally on their input. Examples include the dynamic selection of, e.g., input tokens, layers (or sets of layers), and sub-modules inside each layer (e.g., channels in a convolutional filter). We first provide a general formalism to describe these techniques in an uniform way. Then, we introduce three notable implementations of these principles: mixture-of-experts (MoEs) networks, token selection mechanisms, and early-exit neural networks. The paper aims to provide a tutorial-like introduction to this growing field. To this end, we analyze the benefits of these modular designs in terms of efficiency, explainability, and transfer learning, with a focus on emerging applicative areas ranging from automated scientific discovery to semantic communication.

## 1 Introduction

In the last twenty years, neural networks (NNs) have undergone two opposing trends. On one hand, the number of practical applications has continued to grow, fueled by successes in, among others, language modeling <sub>[</sub>37<sub>]</sub>, drug design <sub>[</sub>94<sub>]</sub>, rendering, and language-vision reasoning <sub>[</sub>65<sub>]</sub>. On the other hand, their design has crystallized around a very small set of layers (e.g., multi-head attention) and principles (e.g., permutation equivariance), while the focus has shifted on scaling up their training, both in terms of data and parameters <sub>[</sub>37<sub>]</sub>. Apart from scale, maybe less than a dozen components and variations thereof are enough to categorize the vast majority of neural networks deployed nowadays.

Among these design principles, sequentiality has remained a key component. NNs, be they convolutional, recurrent, or transformers, are composed of a stack of differentiable operations, which are activated in sequence for each input to be processed. Stated in another way, their computational graph, i.e., the sequence of primitive operations executed on the underlying hardware, is fixed beforehand when instantiating them. Because NNs have continued to scale in depth and width, this has led to several issues in terms of computational performance and efficiency <sub>[</sub>22<sub>]</sub>. Standard techniques to make NNs more efficient only address this partially, by replacing the original network with other static models having fewer layers (distillation <sub>[</sub>96<sub>]</sub>, pruning <sub>[</sub>42<sub>]</sub>), less precision per parameter, or by approximating each weight matrix (e.g., via low-rank factorization).

By viewing neural networks as computing systems, this behavior is counter-intuitive. Hardware components are designed based on their expected peak usage, while only executing a fraction of their resources at any given time (e.g., memory). Similarly, software libraries and operating systems are composed of millions of lines of code, only a handful of which are selected and run in a given moment, thanks to the use of branches, loops, and conditional execution. Recently, a large body of literature has flourished on embedding similar sparse modularity principles in the design of neural networks <sub>[</sub>68<sub>]</sub>. Based on the original idea of conditional computation <sub>[</sub>5<sub>]</sub>, this has blossomed into a large number of practical implementations, ranging from mixture-of-experts (MoEs) <sub>[</sub>86<sub>]</sub> to dynamic mechanisms to select tokens and layers in transformers <sub>[</sub>53<sub>]</sub>. This tutorial is intended as an organized, uniform overview and entry point into this growing body of literature.

The benefits of developing networks that can dynamically adjust their computational graph go beyond memory or time efficiency. More and more, neural networks are treated in the same way as software <sub>[</sub>40<sub>]</sub>, and deploying them requires the possibility of quickly debugging their predictions <sub>[</sub>11<sub>]</sub>, continually fine-tuning them on new data, and transferring parts of their knowledge from one network to the other <sub>[</sub>3<sub>]</sub>, similarly to standalone software libraries. As we will see, dynamically-activated neural networks provide a principled way to improve both zero-shot transfer and generalization <sub>[</sub>71<sub>]</sub> (Sec. 4.2) and explainability of the models (Section 4.3). This aligns with the requirements of many novel applications of NNs, from scientific discovery <sub>[</sub>94<sub>]</sub> to AI-native telecommunications <sub>[</sub>87,100<sub>]</sub>. In particular, smart semantic communication networks <sub>[</sub>87<sub>]</sub> envisioned in the so-called beyond 6G model necessitate networks that can flexibly adapt to bandwidth and energy constraints, while ensuring transferability and communication through separate neural modules.

For the purpose of this tutorial, we consider three flavors of dynamism: (a) neural components that can restrict their computation to a smaller subset of input tokens (dynamic input sparsity); (b) layers that can selectively activate sub-components for processing a token (dynamic width sparsity); and (c) layers that can be completely skipped during their execution (dynamic depth sparsity). As we show in Section 2, a simple mathematical formalism encompasses all three cases. Section 2 also highlights how modularity can be achieved with the addition of a small set of primitives to our networks’ toolkit, namely, the possibility of sampling in a differentiable way elements from a set. We discuss in Section 2.2 the simplest technique to this end, the Gumbel-Softmax trick <sub>[</sub>35, 51<sub>]</sub>, and some common extensions.

We then proceed to discuss three notable implementations of these concepts in Section 3: early-exit (EE) models, mixture-of-expert (MoE) layers, and token selection mechanisms. While these models are generally discussed in separate fashions (e.g., see <sub>[</sub>52, 83<sub>]</sub> for EEs, and <sub>[</sub>20,106<sub>]</sub> for MoEs), viewing them as specific instances of a general framework highlights many similar trends and characteristics. In fact, we argue that designing networks with dynamically activated components is not simply a matter of enhancing performance: in all these cases, the resulting networks are more apt at adapting to variable system’s constraints (e.g., decreased energy usage), specialization, catastrophic forgetting, and multimodality. We build on these insights in Sections 4 and 5, where we list potential research directions for these models including adapting their computational cost and energy at inference and training time in an elastic way, zero-shot transfer, robustness, and explainability.

Relation to prior works: we do not claim to be the first to discuss these ideas, nor to present them in a general way. We simply hope to provide a simple, cohesive entry point into an extremely fascinating and growing research direction in the literature. Recently, modular deep learning <sub>[</sub>68<sub>]</sub> has been proposed as a general term for neural networks where computation is functionally decomposed into units that are sparsely activated. Compared to <sub>[</sub>68<sub>]</sub>, our formalism is simpler and we focus on a smaller set of ideas: for example, we do not consider input composition methods, nor soft routing strategies, and we focus on viewing modularity as discrete sampling inside neural networks. Hence, we provide an orthogonal view to <sub>[</sub>68<sub>]</sub>, to which we refer for a broader outlook on modularity and composition. We also focus on a tutorial exposition, preferring simplicity and clarity to completeness. We only describe the simplest techniques for differentiable sampling, and we refer to <sub>[</sub>60<sub>]</sub> for a larger and more in-depth introduction to this field. Additional entry points in the literature include <sub>[</sub>24<sub>]</sub> (for an overview up to 2021 of dynamism in NNs) and <sub>[</sub>22<sub>]</sub> for designing faster and more efficient transformer models.

## 2 Three types of conditional computation

## 2.1 A general formalism for sparse modularity

Neural networks can be described as the composition of several trainable, differentiable operations of the form:

$$
y = f ( x , w )\tag{1}
$$

![](images/4ad1fbd5b6108f2508ee5bd4f60cea8873c657fc0a2c686aa28d16c4b1d87996.jpg)  
Figure 1: Input sparsity: A differentiable mechanism subsamples input tokens to be processed by the later parts of the network (we show original image patches in the figure, but the tokens can be equivalently be replaced by their latent representations if we consider an intermediate layer of the architecture).

where x denotes the input, w the module’s parameters, and $f$ the specific operation. Because of functional composition, f can represent an operation at any level of complexity, e.g., a basic linear algebra operation, a layer (convolutional, recurrent, $\ldots )$ , or a composite block, such as the classical combination of token mixing, channel mixing, and layer normalization operations found in transformers.

$x _ { c } ,$ $x _ { c }$ $x$

Suppose we have available some trainable subsampling operation, defined over the conditioning input $x _ { c }$ and over some set ${ \mathcal S } ,$ such that:

$$
\Gamma ( { \mathcal { S } } , x _ { c } ) \subseteq { \mathcal { S } } .\tag{2}
$$

Practically, sets are always represented in some matrix format inside neural networks $( \mathrm { e . g . }$ by stacking all elements row-wise), in which case we assume the relevant quantities in (2) to follow the same conventions. As an example, if S is represented by a matrix S, (2) can be implemented by row-wise masking of the corresponding elements:

$$
\Gamma ( \boldsymbol { \mathsf { S } } , \boldsymbol { x } _ { c } ) = \boldsymbol { \mathsf { M } } \odot \boldsymbol { \mathsf { S } }\tag{3}
$$

where M is a binary mask of suitable shape with rows set to either 0 or 1. Different implementations can be obtained depending on whether the size of the output mask is known in

![](images/e10f57693b58d08a7fd4d25d67f9ba4848c5bf489f7ddcf6dd7055c74aa0996e.jpg)  
Figure 2: Width sparsity: Different parts of a layer (e.g., experts) can be activated based on the conditioning value.

advance (e.g., how many tokens to keep in a given layer), or must be estimated by Γ itself.   
We will see later on in Section 2.2 how such an operation can be implemented in practice.

This small addition allows us to implement several levels of modularity inside our neural network. First, assume the input x can be decomposed into smaller components $x =$ $\{ x _ { 1 } , \ldots , x _ { n } \}$ . In many cases, this is a natural decomposition, e.g., tokens inside a transformer, time instants for a sequence, or frames for a video input. However, they can also correspond to additional register tokens <sub>[</sub>18<sub>]</sub>, to elements extracted from some external memory (e.g., AdaTape <sub>[</sub>102<sub>]</sub>), or additional views or modalities. Then, dynamic input sparsity (Fig. 1) is achieved by combining the layer with a subsampling operation on the input:

$$
{ \mathrm { I n p u t ~ s p a r s i t y : } } f ( \Gamma ( x , x _ { c } ) , w )\tag{4}
$$

This allows the layer to focus exclusively on input components that are relevant to the current operation. As an example, consider an image with a very wide, uniformly blue background: for the majority of tasks, we can imagine the layer to be able to operate even when removing the vast majority of tokens corresponding to such background <sub>[</sub>97<sub>]</sub>. This is, indeed, observed in practice, as we’ll describe in Section 3.5.

Second, assume the weights themselves can be decomposed into blocks $b = \{ w _ { 1 } , \ldots , w _ { m } \}$ 2 and the entire function decomposed as:

$$
f ( x , w ) = \oplus ( \{ f _ { 1 } ( x , w _ { 1 } ) , \ldots , f _ { m } ( x , w _ { m } ) \} ) ,\tag{5}
$$

$\oplus$ $f _ { i }$ $\mathrm { O r } , f _ { i }$

$$
\begin{array} { r } { \mathrm { W i d t h ~ s p a r s i t y : } f ( x , \Gamma ( w , x _ { c } ) ) = } \\ { \oplus ( \Gamma ( \{ f _ { 1 } ( x , w _ { 1 } ) , \dots , f _ { m } ( x , w _ { m } ) , x _ { c } \} ) } \end{array}\tag{6}
$$

![](images/b6ece4cf4d8923ce97e0bb0af7f0c68a0d05513d0e1dc8cdca0f878626fef993.jpg)  
Figure 3: Depth sparsity: A subset of the layers can be deactivated by the sampling mechanism, like in early-exit networks.

Imposing some form of structure over w is fundamental since subsampling each weight separately would result in a highly unstructured form of dynamic pruning, which is generally very difficult to optimize and control <sub>[</sub>36<sub>]</sub>. Once again, this formulation is very generic: for example, if each $f _ { i }$ corresponds to an activation function, subsampling with cardinality 1 corresponds to choosing the best activation function for each token or each input, in a form of dynamic model selection mechanism <sub>[</sub>48<sub>]</sub>. If each $f _ { i }$ is an entire model, this can be used to route information across blocks with different types or complexity (see, e.g., layer stitching <sub>[</sub>62<sub>]</sub>). We will see in Section 3.2 a common implementation of this principle in the context of MoEs, and defer more general discussions to Section 4.

Third, even if a weight decomposition is unavailable, dynamic computation can still be achieved by considering the entire layer as a single block and conditionally skipping its execution. This dynamic depth sparsity (Fig. 3) can be achieved easily by rewriting the layer with an additional, untrainable scalar weight $\sigma = 1$ , and writing:

$$
\mathrm { D e p t h ~ s p a r s i t y : } f ^ { \prime } ( x , w , \Gamma ( \{ \sigma \} , x _ { c } ) ) =\tag{7}
$$

$$
\sigma ( x _ { c } ) f ( x , w ) + ( 1 - \sigma ( x _ { c } ) ) x\tag{8}
$$

where we assume the empty set $\varnothing$ to be implemented as 0 in practice. As a variant of this idea, we can skip entire blocks of layers by exiting the network instead of adding a skip connection in (8). We will see concrete implementations of this concept in Section 3.1.

## 2.2 Discrete sampling: the Gumbel-Softmax trick

Before proceeding, we discuss briefly the implementation of the subsampling layer Γ . As a prototypical example, we restrict our analysis to subsampling a single element from the set in input. In this case, a very common implementation is the so-called Gumbel-Softmax (GS) trick <sub>[</sub>35<sub>]</sub>, also known as the concrete distribution <sub>[</sub>51<sub>]</sub>. In this section, we only provide a high-level overview, and we refer to <sub>[</sub>34<sub>]</sub> for a fuller exposition.

First of all, we process the inputs with some trainable layer $p ( \mathcal { S } , x ) \in \mathbb { R } ^ { | \mathcal { S } | }$ to provide a realvalued score for each element in ${ \mathcal S } ,$ , which is proportional to its probability of being sampled. In this section, we drop the subscript from the conditioning input $x _ { c }$ for readability. The implementation of $p$ depends on the use case. For example, suppose that the conditioning

![](images/3d16ebea8fbd612d0b6d4ac36b1b235c1da958bdc9116516999f7ef4b8afdc2b.jpg)  
Figure 4: Overview of the Gumbel-Softmax trick. We show in orange differentiable operations (the argmax’s gradient being zero almost everywhere) and with a dashed arrow the relaxed backward path.

$\boldsymbol { x } \in \mathbb { R } ^ { h \times w \times d }$ $w ,$ $h ,$ $\mathbf { c } _ { i }$

$$
\mathbf { v } = \mathrm { M L P } \left( \sum _ { i , j } x _ { i j } \right)\tag{9}
$$

$$
p ( \mathcal { S } , x ) = \left[ \mathbf { v } ^ { \top } \mathbf { c } _ { 1 } , \ldots , \mathbf { v } ^ { \top } \mathbf { c } _ { | \mathcal { S } | } \right]\tag{10}
$$

$p$ $p ,$ $g _ { i }$ $\mathcal { S } = \{ 1 , \ldots , | \mathcal { S } | \}$ $\Gamma _ { | \mathcal { S } | } ( x )$ ${ \mathcal S } ,$ $p ( s \in \mathcal { S } ) \propto \exp ( p _ { s } )$ $p _ { s }$

$$
s = \underset { i } { \mathrm { a r g m a x } } \{ p _ { i } + g _ { i } \} .\tag{11}
$$

Removing the Gumbel noise $g _ { i }$ corresponds to taking the element with the highest score $p _ { i }$ while sampling provides a degree of freedom that is helpful in exploring possible alternatives. Since the probabilities $p _ { i }$ are implicitly trained via $p ( \mathcal { S } , x )$ , the network can learn to select the element from S which is most useful for the specific input x. In the case of channel selection, for example, this can lead to specializing single channels to specific types of inputs.

The operation in (11) is not easily trainable via gradient descent (since its gradient will be zero almost everywhere), but it can be relaxed with a softmax approximation:

$$
s _ { i } = \frac { \exp ( { ( p _ { i } + g _ { i } ) / \tau } ) } { \sum _ { j } \exp ( { \left( p _ { j } + g _ { j } \right) / \tau } ) } .\tag{12}
$$

The quality of the approximation can be controlled by the user-defined parameter τ, sometimes called the temperature <sub>[</sub>34<sub>]</sub>. The values in s are not binary anymore, being generic convex combinations of the (one-hot) representations from the elements in S. However, a common relaxation is to use the binary values in (11) during the forward pass of the network, and relax the gradients to use the soft approximation in (12) during the backward pass. This is called straight-through estimation (STE). A high-level overview of the complete schema is given in Fig. 4.

The GS trick can be easily extended to sampling more than a single value by replacing the arg max with a top-k operation <sub>[</sub>43<sub>]</sub>. Suitable generalizations, such as the entmax family <sub>[</sub>16<sub>]</sub>, can also sample binary vectors with a variable number of elements. The simplicity of the GS trick makes it widespread in many applications, but several other types of sampling layers can be found in the literature, especially for more complex combinatorial spaces, for which we refer to <sub>[</sub>60<sub>]</sub>. A larger overview of possible sampling operations for MoE layers is also given in Sec. 3.3.

## 3 Concrete implementations

The previous section has introduced a generic framework for designing networks with dynamic computational graphs. In the literature, these ideas have coalesced around a few, notable set of implementations. In this section we overview three of the most popular ones: early exits (Sec. 3.1), MoE layers (Sec. 3.2), and token sampling (Sec. 3.5) as examples of networks having dynamic depth, width and input, respectively. In all cases we focus on the key strengths and drawbacks of each approach, highlighting how they connect to the framework of Sec. 2.

## 3.1 Early exits

Early exit neural networks (EENNs) were introduced based on the idea that not all the inputs to a network are required to go through all the layers of the model to be correctly classified <sub>[</sub>90<sub>]</sub>. In fact, the accuracy of a network can decrease with respect to the depth on particularly easy samples, a phenomenon known as overthinking <sub>[</sub>81<sub>]</sub>.

Consider a neural network (sometimes called the backbone network in this context), which can be either trained from scratch or pre-trained. In an early-exit framework, the backbone is augmented with auxiliary classifiers (early exits) which are connected at intermediate outputs of the backbone. These auxiliary blocks can be trained all at the same time or in a layer-wise fashion <sub>[</sub>83<sub>]</sub>, while at inference time they are used to halt the computation when the model is confident enough about the prediction. This is an example of dynamic depth sparsity (Section 2), except that an entire subset of layers is skipped at the same time.

We introduce first the most common formulation of EENNs, in which early exits are jointly trained while the early exit logic is defined manually with additional hyper-parameters. As already stated, we can see a neural network as a composition of b sequential blocks:

$$
f ( x ) = \mathbf { f } _ { b } \circ \mathbf { f } _ { b - 1 } \circ \cdots \circ \mathbf { f } _ { 1 } ( x )\tag{13}
$$

where <sup>◦</sup> denotes function composition, b is the last layer of the backbone, and we remove the dependency on the parameters for simplicity. Where to place the auxiliary classifiers is in general a hyper-parameter <sub>[</sub>83<sub>]</sub>, but here, for clarity, we add a classifier after each block, producing multiple prediction functions:

$$
y _ { i } ( x ) = \mathbf { c } _ { i } \circ ( \mathbf { f } _ { i } \circ \mathbf { f } _ { i - 1 } \circ \cdots \circ \mathbf { f } _ { 1 } ( x ) )\tag{14}
$$

where $c _ { i }$ is a small classifier (e.g., for a CNN, a typical design is to have a global average pooling operation followed by a fully-connected layer, while for a transformer we can apply a fully-connected layer on a specialized class token). This formulation leads to an EENN which is capable of classifying input samples at any stage of the computation through the sequence $y _ { 1 } ( x ) , y _ { 2 } ( x ) , \ldots , y _ { b - 1 } ( x ) , f ( x )$ . Ideally, each classifier can specialize on a subset of the training samples based on the complexity of the input. In the simplest case, given a desired output y, all early exits can be trained simultaneously by minimizing the sum of the losses for each classifier:

$$
L = \alpha \mathrm { C E } ( y , f ( x ) ) + \sum _ { i = 1 } ^ { b - 1 } \beta _ { i } \mathrm { C E } ( y , y _ { i } ( x ) ) ,\tag{15}
$$

where CE is the cross-entropy loss, and ${ \alpha , \beta _ { 1 } , . . . , \beta _ { b - 1 } }$ are hyper-parameters that balance the loss contribution from each early exit. At inference time, an exit can be chosen by comparing, e.g., the predicted class probability or the entropy of the prediction to a user-defined parameter acting as a threshold. Other strategies include combining predictions based on trainable <sub>[</sub>82<sub>]</sub> or geometric <sub>[</sub>98<sub>]</sub> ensembling.

These networks have found applications in many fields recently. Concerning NLP, many strategies with BERT have been proposed <sub>[</sub>99, 112, 115<sub>]</sub>, varying from patience-based EE <sub>[</sub>112<sub>]</sub> to extra classification layers <sub>[</sub>99<sub>]</sub>. For computer vision, EE applications vary based on the strategy, including multi-exiting <sub>[</sub>4, 8, 44, 96<sub>]</sub>, and loss-weight adjustment <sub>[</sub>95<sub>]</sub>. Also, the tasks vary, spanning semantic segmentation <sub>[</sub>44<sub>]</sub>, video recognition <sub>[</sub>23<sub>]</sub>, adversarial training <sub>[</sub>41<sub>]</sub>, and image compression <sub>[</sub>100<sub>]</sub>. Recently, EE strategies have been proposed also for vision-language models <sub>[</sub>89<sub>]</sub>.

Although this formulation of EENNs (or minor variations thereof) is very common in the literature (see e.g., <sub>[</sub>8, 52, 84, 89, 90, 112<sub>]</sub>), it only fits partially our view of dynamic sparsity, since the computational graph is unchanged during training and the dynamism is only obtained via an external heuristic. To this end, <sub>[</sub>82<sub>]</sub> proposed a mechanism to optimize the early exit selection during training, called differentiable branching. Suppose we augment each early exit with an additional output that we denote as $\gamma _ { i } ( x )$ . The key idea of differentiable branching is to define a new recursive output, which is given by a soft composition of the original outputs:

$$
\tilde { y } _ { i } ( x ) = \gamma _ { i } ( x ) y _ { i } ( x ) + ( 1 - \gamma _ { i } ( x ) ) \tilde { y } _ { i + 1 } ( x )\tag{16}
$$

where the recursion stops at $i = b _ { \colon }$ , where $\gamma _ { i } ( x ) = 1$ by definition. At inference time, this can be turned into an early exit module by viewing $\gamma _ { i } ( x )$ as a binary classifier and thresholding it at 0.5. By replacing the gates $\gamma _ { i } ( x )$ with samples from a GS distribution, we return to

the general setting described in Section 2. In fact, if the outputs of $\gamma _ { i } ( x )$ are binary we can identify:

$$
\Gamma _ { b - 1 } ( x ) = \left[ \begin{array} { c } { { \gamma _ { 1 } ( x ) } } \\ { { ( 1 - \gamma _ { 1 } ( x ) ) \gamma _ { 2 } ( x ) } } \\ { { \vdots } } \\ { { \left[ \prod _ { i = 1 } ^ { b - 2 } ( 1 - \gamma _ { i } ( x ) ) \right] \gamma _ { b - 1 } ( x ) \vphantom { \left[ \sum _ { i = 1 } ^ { b - 1 } ( 1 - \gamma _ { i } ( x ) ) \right] } } } \end{array} \right]\tag{17}
$$

with the subsampling block over the indexes of the early exits. This can also be given a Bayesian interpretation under the stick-breaking process <sub>[</sub>70<sub>]</sub>. While the sampler in (17) is conditioned on the full input, other choices are possible. For example, in multitask learning a separate task embedding can be used to select different exits for different tasks <sub>[</sub>108<sub>]</sub>, while in the case of transformers, only the class token can be used to decide an optimal exit strategy <sub>[</sub>30<sub>]</sub>. Being able to train the choice of early exit is fundamental because it allows us to regularize it further for, e.g., better inference-accuracy trade-offs: we revisit this idea in Section 4.1. See <sub>[</sub>52, 82<sub>]</sub> for in-depth reviews on EENNs and <sub>[</sub>82<sub>]</sub> for a fuller description of differentiable branching.

## 3.2 Mixture-of-experts

Mixture-of-Experts (MoEs) models were introduced more than thirty years ago as adaptive algorithms to perform dynamic ensembles of individual machine learning algorithms, denoted as experts in that context <sub>[</sub>106<sub>]</sub>. Recently, MoE layers in neural networks have gained popularity, especially for LLMs and large vision modules <sub>[</sub>79<sub>]</sub>. They allow scaling the model’s parameters while keeping the compute budget constant, and they offer the possibility of distributing the training by decomposing the computation of a layer over multiple GPUs <sub>[</sub>79<sub>]</sub>. As a side product, they offer dynamic width sparsity by selectively activating only parts of the layer for each input. At the time of writing, the largest open source language and vision models are based on a MoE formulation <sub>[</sub>17, 21, 37, 45, 79<sub>]</sub>.

$$
f ( x , w ) = \sum _ { i = 1 } ^ { n } \gamma _ { i } ( x ) f _ { i } ( x , w _ { i } )\tag{18}
$$

where $\boldsymbol { \gamma }$ is the routing function and $f _ { 1 } , f _ { 2 } \ldots f _ { n }$ are the experts. In its simplest form, this is a sparse linear combination of the outputs of the experts. This is immediately seen to be an instance of 6 with $\Gamma _ { n } ( x ) = [ \gamma _ { 1 } ( x ) , \gamma _ { 2 } ( x ) , \ldots , \gamma _ { n } ( x ) ]$ , provided that the outputs of $\gamma _ { i } ( x )$ are sparse.

The unique advantage of MoEs is that only a fraction of the network parameters, depending on the chosen value for k, are used for computation. Such fraction can be tuned by changing the value of k. Additionally, one can devise routing functions such that experts focus on different areas of the input space, leading to specialized sub-networks (see Sec. 4.2 for a discussion on specialization and Sec. 3.3 for an overview of routing algorithms for MoE layers).

Unlike early exiting, where the routing function typically works at the level of input samples (e.g., images for a CNN), an MoE layer as in (18) can work at the level of individual tokens in a transformer. More specifically, in the fully-connected layers of a transformer block, each token can be assigned to one or more experts. Transformer MoEs have been proposed for NLP <sub>[</sub>21, 73<sub>]</sub>, for vision <sub>[</sub>79<sub>]</sub> and even for multimodal training <sub>[</sub>59<sub>]</sub>. Additional variants can be applied to individual heads of an attention block <sub>[</sub>109<sub>]</sub> or adapters in a fine-tuning context <sub>[</sub>107<sub>]</sub>.

## 3.3 Routing in Mixture of Experts

Different routing strategies can be adopted to orchestrate the experts. These are defined in the gating function γ and usually leverage some differentiable sampling method similar to the Gumbel-Softmax trick (Sec. 2.2). Routing is a crucial aspect of any MoE architecture, as it must perform a matching between input data and expert network, conditioned on the input data itself. Decisions taken by the routing function govern the training. They can determine faster convergence and expert specialization or cause expert starvation, a peculiar situation where only a few experts are always activated due to their ever-increasing expertise.

The routing algorithm usually adopts a dot product for computing similarity between the embedding of each routed sample (e.g. a token in a transformer) and n trainable expert embeddings (one for each expert). Once this operation has occurred, the assignment can happen according to various methods.

In top-k token choice, each token is assigned to the k most similar experts, where k is an arbitrary value. This is the original approach from <sub>[</sub>85<sub>]</sub>, and it usually requires additional regularization to avoid expert starvation and training instability. The same approach has been adopted with minor changes (e.g. balancing loss and the k factor) in <sub>[</sub>21, 75<sub>]</sub>. Top-k expert choice, proposed in <sub>[</sub>113<sub>]</sub>, tries to solve the expert balancing problem by assigning each expert to the k most similar tokens, where k is an arbitrary value. Other works <sub>[</sub>15, 80<sub>]</sub> cast the expert assignment problem into a reinforcement learning framework and train over a routing policy to assign each token to a single expert. Finally, <sub>[</sub>116<sub>]</sub> achieves surprisingly good results by randomly assigning experts to routed samples. An empirical comparison of different routing functions can be found in <sub>[</sub>49<sub>]</sub>, while a broader overview of MoE layers is given in <sub>[</sub>20<sub>]</sub>.

## 3.4 Soft routing

We discuss here a variant of the MoE layer in (18), known as soft MoE, which has become popular recently to avoid training instabilities in the layer. The key idea is to use the gating function to combine the layer’s inputs <sub>[</sub>72<sub>]</sub> or weights <sub>[</sub>58<sub>]</sub> instead of the model’s outputs. These variants also provide a fixed compute budget which is decoupled from the total number of parameters, but they are generally easier to implement and train.

First, denote by $x _ { 1 } , \ldots , x _ { n }$ the tokens in input to the layer. The first soft MoE variant we consider can be defined as <sub>[</sub>72<sub>]</sub>:

$$
f _ { i } ( x , w _ { i } ) = f _ { i } \left( \sum _ { i = 1 } ^ { n } \gamma _ { i } ( x _ { i } ) x _ { i } , w _ { i } \right)\tag{19}
$$

i.e., each expert is activated with a soft combination of input tokens. Compared with standard top-k routing, each expert is only activated once in this formulation, irrespective of the number of tokens. The output of the layer for a single token is then given by another soft combination, this time over the experts’ outputs:

$$
f ( x _ { i } ) = \sum _ { i = 1 } ^ { n } \gamma _ { i } ( x _ { i } ) f _ { i } ( x , w _ { i } )\tag{20}
$$

By comparison, another soft MoE variant can be achieved by performing a soft combination of the experts’ weights <sub>[</sub>58<sub>]</sub>. Denote by $f ( x , w )$ the generic architecture of a single expert, we have:

$$
f ( x ) = f \left( x , \sum _ { i = 1 } ^ { n } \gamma _ { i } ( x ) w _ { i } \right)\tag{21}
$$

A thorough comparison of the relative benefits of hard vs. soft routing is still lacking in the literature, but we highlight a few benefits in Sec. 4.

## 3.5 Token dropping and token merging

We conclude with a brief analysis of token selection mechanisms. In particular, we consider two cases of token selection, which we refer to as token dropping (removal of tokens from the model) and token merging (combination of tokens). Both are conditional computation techniques that can be employed in any transformer model. The fundamental idea behind token dropping and token merging is that the input data often contains information that is nearly useless for the final task. Since transformers operate on set-based inputs with no fixed cardinality, one can dynamically reduce the number of tokens being passed to each layer depending on the relevance of said tokens for the final task.

More formally, let X be the set of n tokens inside a transformer model stacked horizontally. For the purpose of this section, the subsampling operation Γ can be implemented as a matrix multiplication of the input matrix X and a mask M:

$$
\mathbf { X } ^ { \prime } = \Gamma _ { n } ( \mathbf { X } ) = \mathbf { M } \mathbf { X }\tag{22}
$$

Depending on the properties of the matrix M, we can obtain either token dropping or token merging:

• Token dropping: M is a matrix of shape $n ^ { \prime } \times n$ that selects a subset of $n ^ { \prime }$ elements from the original tokens. This can be achieved by setting each row to a one-hot vector.

• Token merging: M is a binary matrix of shape $n ^ { \prime } \times n$ , with the requirement that each column sum to one. In this way, the output tokens are combinations of the input ones, so each input token participates in a single output token. This can be seen as a dynamic variant of the standard pooling used in CNNs.

Both methods aim to reduce the computational cost of the forward pass of a transformer by reducing the number of tokens. The mask M is usually computed depending on the input data, $\mathbf { M } = \mathbf { M L P } ( \mathbf { X } )$ , in such a way as to eliminate only redundant information, such as background patches in an image. This is usually done either by small modules that are added to the backbone model <sub>[</sub>77<sub>]</sub> or by evaluating some channels added to the tokens for this purpose <sub>[</sub>53<sub>]</sub>. For token selection, when dealing with mini-batches of inputs, the sub-sampling operation in (22) cannot be performed easily in a vectorized way. In these cases, (22) can be replaced by a masking operation as in (2), with the additional constraint that subsequent se lection modules can only select values that were not masked previously <sub>[</sub>77<sub>]</sub>. In these cases, performance gain only materialize at inference time, while at training time most operations are still executed in a masked way.

## 4 Research directions

Designing neural networks with sparse modularity principles has a number of benefits. The first and most studied is increased efficiency, both in training and in inference (Sec. 4.1). However, modular networks show emergent properties also in terms of specialization and transferability (Sec. 4.2), as long as providing a blueprint for a new type of explainability techniques (Sec. 4.3). We briefly overview these aspects in the following sections.

## 4.1 Efficiency in training and inference

Conditional computation has gained significant attention for accelerating training and inference in deep learning models <sub>[</sub>22,68<sub>]</sub>. Often, the time saving comes with a drop in accuracy, making it important to assess the accuracy<sub>/</sub>computation trade-off. An interesting example is shown in Fig. 5. The approaches can vary based on several factors. For example, some research investigated the sparsification of CNNs <sub>[</sub>92<sub>]</sub> and of transformers <sub>[</sub>12,36<sub>]</sub>, some others focused on some specific aspects of the net, such as the gradients <sub>[</sub>19<sub>]</sub>, the backpropagation, the activations <sub>[</sub>13<sub>]</sub> and the attention layers <sub>[</sub>14, 91<sub>]</sub>. For clarity, we focus here, mainly, on efficiency aspects related to the three families of models seen in Sec. 3, focusing on emerging trends and open challenges. To make the analysis more timely and precise, we have reported all the methods analyzed in Table 1.

When training from scratch an EENN, the joint training described in Sec. 3.1 cannot provide faster training since all exits must be trained simultaneously. Soft combinations of the early exits <sub>[</sub>82<sub>]</sub> combined with sampling tricks could be useful, but this aspect has been scarcely explored in the literature, possibly due to training instabilities and collapse. Still, EEs can provide indirect benefits to training by accelerating the convergence of deep neural networks <sub>[</sub>8, 90<sub>]</sub>. They can also improve the inference efficiency of large-scale pre-trained models <sub>[</sub>25, 112<sub>]</sub>, making them more discriminative <sub>[</sub>90<sub>]</sub>, act as a regularization technique <sub>[</sub>81<sub>]</sub>, and possibly reduce training problems (e.g. vanishing gradient phenomena) <sub>[</sub>64<sub>]</sub>. In addition, they can be trained in a layerwise fashion if one starts from a pre-trained network <sub>[</sub>24<sub>]</sub>. In Table 1, we can see that most of these methods require additional parameters, leading to a latency reduction.

Compared to EEs, MoEs were investigated mostly to speed up training by distributing the experts across different GPUs <sub>[</sub>20<sub>]</sub>, or to accelerate inference by activating a subset of experts for each forward pass. For the former, tiling the model across separate machines requires customized implementations <sub>[</sub>75<sub>]</sub>. In addition, to achieve an effective stable throughput, training must avoid collapses of the routing function, and care must be taken to balance the number of tokens that are sent to the different experts. This last point can be achieved with the addition of so-called balancing losses, e.g., batch prioritized routing <sub>[</sub>15, 20, 79<sub>]</sub>. Due to these problems, open-source implementations of large MoE models have generally lagged behind proprietary models, with some preliminary steps being taken in this direction <sub>[</sub>103<sub>]</sub>, as observable also in Table 1.

The benefits of applying MoEs can also vary depending on the specific component that is being replaced. In <sub>[</sub>85<sub>]</sub>, MoEs replace MLP layers to scale-up transformers. A similar methodology, for vision, was presented in <sub>[</sub>79<sub>]</sub>. Other approaches proposed to replace attention layers <sub>[</sub>109<sub>]</sub>, entire blocks <sub>[</sub>88<sub>]</sub> of the net, and adapters <sub>[</sub>107<sub>]</sub>. By comparison, soft MoEs (Sec. 3.4) can reach similar gains as standard MoE layers while being simpler to train. Finally, the majority of MoEs are trained from scratch, but recently moefication has emerged as an interesting research direction, in which a pre-trained model is converted to an MoE variant by clustering the activations <sub>[</sub>74, 110<sub>]</sub> (see Table 1 to see the approaches based on pre-training). These variants provide different accuracy-time trade-offs based on the specific routing function. Additional emerging research trends are exploring dynamic variants of routing to provide a flexible inference budget instead <sub>[</sub>69, 97<sub>]</sub>.

Finally, reducing the number of tokens with token selection techniques is a straightforward strategy to improve the inference time of the network. Most methods in this sense have focused on token dropping <sub>[</sub>9, 27, 105<sub>]</sub>: A-ViT adopts a token halting approach (shown also in Fig. 5);AdaViT <sub>[</sub>53<sub>]</sub> proposes a light-weight decision network, attached to the backbone to produce decisions on-the-fly; DynamicViT <sub>[</sub>77<sub>]</sub> proposes an attention-masking strategy to block interaction of redundant tokens; MSViT <sub>[</sub>28<sub>]</sub> proposes a conditional gating mechanism that selects the token scale for every image region; GTP-ViT <sub>[</sub>101<sub>]</sub> introduces a Graph-based Token Propagation (GTP) to propagate the information of less significant tokens. During training, token selection is generally achieved by masking the corresponding input elements (Sec. 3.5). Designing token selection mechanisms that can improve training time (for a fixed compute budget) is still an open challenge.

![](images/e31965cd0a3339539580fafc2fad7bc243fccd5304fcf270d9495fa28f4968a4.jpg)  
Figure 5: Example of accuracy-flops trade-off for inference with A-ViT <sub>[</sub>105<sub>]</sub>. Specifically, the architecture is a DeiT, trained on Imagenette.

Some works have focused more on specific tasks, such as diffusion <sub>[</sub>10<sub>]</sub>, long-input sequences <sub>[</sub>1<sub>]</sub>, segmentation <sub>[</sub>50<sub>]</sub>, or to better understand the general pattern of token dropping <sub>[</sub>27<sub>]</sub>. For token merging, PatchMerger <sub>[</sub>78<sub>]</sub> proposes a module that reduces the number of tokens by merging them between two consecutive intermediate layers <sub>[</sub>78<sub>]</sub>. Recently, a hy brid solution, Token Fusion (ToFu) <sub>[</sub>42<sub>]</sub>, proposed to put together the benefits of both token pruning and token merging. Token selection can also be combined with the other methods discussed in this paper. As an example, Adaptive Computation Module (ACM) <sub>[</sub>97<sub>]</sub> is a technique that combines token dropping with a dynamic width principle, in which each token is allocated a variable width for each layer in the network.

## 4.2 Specialization

Modularity can also lead to specialization benefits in specific tasks <sub>[</sub>55,111<sub>]</sub>, such as language modeling <sub>[</sub>47,54<sub>]</sub>, cross-lingual transfer <sub>[</sub>3,65,66,93<sub>]</sub>, speech processing <sub>[</sub>54,67<sub>]</sub>, computer vision and multi-modality <sub>[</sub>2, 59, 76<sub>]</sub>, and task generalization <sub>[</sub>57<sub>]</sub>.

Specialization can happen in two ways: implicitly if no external information is provided, or explicitly if additional information (e.g., the speaker identity) is known. The key insight is that knowledge of, e.g., the task, the domain, or the speaker provides latent information that can be used to condition the routing blocks (Γ in Sec. 2), thus specializing specific parts of the network or specific components to different scenarios. This can be achieved in different ways: manual routing in which different components are pre-selected for the different latent vectors <sub>[</sub>68<sub>]</sub>, direct conditioning of the routing functions <sub>[</sub>114<sub>]</sub>, entropy regularizers to force the distributions w.r.t. to a specific latent vector to have low entropy <sub>[</sub>59<sub>]</sub>, or weight sharing across tasks <sub>[</sub>89<sub>]</sub>. Soft merging <sub>[</sub>58<sub>]</sub> also seems to offer specialization benefits.

Table 1: Overview of methods to improve efficiency of the models, including baseline algorithms not discussed in the text (e.g., pruning). Parameters: whether the method adds additional parameters. Pre-training: whether the method requires a pre-training phase. Latency<sub>/</sub>FLOPs: whether the method optimizes one of these two metrics
<table><tr><td>Method</td><td>Approach</td><td>Parameters</td><td>Pre-training</td><td>Latency</td><td>FLOPs</td></tr><tr><td>Dynamic Convolutions [92] (2020)</td><td>Sparsity</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>Scaling Transformers [36] (2021)</td><td>Sparsity</td><td></td><td></td><td>Yes</td><td></td></tr><tr><td>SViTE [12] (2021)</td><td>Pruning</td><td></td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>Sparse Momentum [19] (2019)</td><td>Pruning</td><td></td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>SparseViT [13] (2023)</td><td>Pruning</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>Sparse Transformers [14] (2019)</td><td>Factorization</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>Differentiable branching [82] (2020)</td><td>Early Exits</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>Adaptive Early Exits [8] (2017)</td><td>Early Exits</td><td>Yes</td><td></td><td>Yes</td><td></td></tr><tr><td>L2W-DEN [25] (2022)</td><td>Early Exits</td><td>Yes</td><td></td><td>Yes</td><td></td></tr><tr><td>PABEE [112](2020)</td><td>Early Exits</td><td>Yes</td><td></td><td>Yes</td><td></td></tr><tr><td>Branchynet [90] (2016)</td><td>Early Exits</td><td>Yes</td><td></td><td>Yes</td><td></td></tr><tr><td>AEP [81] (2023)</td><td>Early Exits</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>BoF [64] (2020)</td><td>Early Exits</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>DeepSpeed-MoE [75] (2022)</td><td>MoE</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr><tr><td>Sparsely-Gated MoE [85] (2017)</td><td>MoE</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>V-MoE[79] (2021)</td><td>MoE</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>MoA [109] (2022)</td><td>MoE</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>SUT [88] (2023)</td><td>MoE</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>MoV/MoLoRA [107] (2023)</td><td>MoE</td><td>Yes</td><td>Yes</td><td></td><td>Yes</td></tr><tr><td>EMoE[74](2023)</td><td>MoE</td><td></td><td>Yes</td><td></td><td>Yes</td></tr><tr><td>GMoE [46] (2022)</td><td>MoE</td><td>Yes</td><td>Yes</td><td></td><td>Yes</td></tr><tr><td>MoEfication [110]</td><td>MoE</td><td>Yes</td><td>Yes</td><td></td><td>Yes</td></tr><tr><td>SADMoE [69] (2023)</td><td>MoE</td><td>Yes</td><td>Yes</td><td></td><td></td></tr><tr><td>A-ViT [105] (2022)</td><td>Token Sampling</td><td></td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>ToMe [9, 10] (2022)</td><td>Token Sampling</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>AdaViT [53] (2022)</td><td>Token Sampling</td><td>Yes</td><td></td><td></td><td>Yes</td></tr><tr><td>DynamicViT [77] (2021)</td><td>Token Sampling</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>MSViT [28] (2023)</td><td>Token Sampling</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>GTP-ViT [101] (2024)</td><td>Token Sampling</td><td>Yes</td><td></td><td>Yes</td><td>Yes</td></tr><tr><td>Colt5 [1] (2023)</td><td>MoE</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr><tr><td>PatchMerger [78] (2022)</td><td>Token Sampling</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr><tr><td>ToFu [42] (2024)</td><td>Token Sampling</td><td></td><td>Yes</td><td>Yes</td><td>Yes</td></tr><tr><td>ACM [97] (2023)</td><td>MoE/Token Sampling</td><td>Yes</td><td>Yes</td><td></td><td>Yes</td></tr></table>

Studies on quantifying the quality of the resulting specializations were carried out recently in the literature <sub>[</sub>103<sub>]</sub>. MoEs showed promising performance due to their nature, and, specifically, hard routing facilitates module specialization <sub>[</sub>68<sub>]</sub>. On the other hand, learned routing could lead to sub-optimal results <sub>[</sub>55, 56<sub>]</sub> w.r.t to fixed routing, except for specific cases <sub>[</sub>71<sub>]</sub>. As another example, <sub>[</sub>103<sub>]</sub> showed that many routing decisions tend to ignore context, and they can be fixed during the early stages of training. Generally speaking, understanding the interplay between routing and specialization and the extent to which this specialization correlates with human-understandable semantics and biological plausibil ity remain open challenges that will require novel benchmarks and metrics <sub>[</sub>74,111<sub>]</sub>. Recent moefications works show that some form of emergent modularity may also be found in pretrained networks with no specific modularity bias <sub>[</sub>74, 110<sub>]</sub>.

A benefit of having specialized sub-structures and components is that the networks can perform better in multi-task learning <sub>[</sub>57<sub>]</sub> and multi-domain scenarios <sub>[</sub>59<sub>]</sub>, and they can potentially enable zero-shot transfer and generalization of the resulting sub-structures. We list a few interesting examples from the recent literature. PHATGOOSE <sub>[</sub>57<sub>]</sub> is a MoE specialized in zero-shot generalization, thanks to a new post-hoc routing strategy. EMoE focuses on the implicit modular structures (Emergent Modularity) of large pre-trained transform ers <sub>[</sub>74<sub>]</sub>. DSelect-k <sub>[</sub>29<sub>]</sub> presents a continuously differentiable and sparse gate for multitask learning. Uni-Perceiver-MoE <sub>[</sub>114<sub>]</sub> is a generalist conditional MoE that shows SOTA performance when compared to specialized MoEs. LIMoE <sub>[</sub>59<sub>]</sub> is focused on language-image pre-training. DeepSeekMoE <sub>[</sub>17<sub>]</sub> manages to ensure expert specialization for language models, still reducing computational costs. Other approaches include modular submodels to scale language models <sub>[</sub>6<sub>]</sub> and a class-aware channel pruning for queriable NNs <sub>[</sub>38<sub>]</sub>.

## 4.3 Explainability

Finally, modularity and sparsity can provide significant gains in explainability, which is a sig nificant issue when deploying systems <sub>[</sub>26<sub>]</sub>. In particular, analyzing and plotting the routing decisions made by the subsampling blocks Γ almost always provide valuable insights into the predictions. These include, but are not limited to, visualizing representative tokens sent to each expert <sub>[</sub>59<sub>]</sub>, visualizing the early exits distribution for a given sequence in an autoregressive model <sub>[</sub>84<sub>]</sub>, visualizing the tokens that were never discarded in a network having token selection <sub>[</sub>53, 61, 77<sub>]</sub>, or the number of experts that were activated token-wise <sub>[</sub>97<sub>]</sub>. These techniques can provide benefit also for specific tasks, such as object detection <sub>[</sub>13<sub>]</sub>.

Also in this case, we lack principled benchmarks and frameworks to analyze the resulting plots, which is an open problem in explainability in general <sub>[</sub>26<sub>]</sub>. In addition, for networks having thousands of blocks or experts, manually analyzing each of them can be a time-consuming process. LLMs can potentially help in automating this process <sub>[</sub>7<sub>]</sub>. From

## 5 Conclusions and future trends

In this tutorial paper we have provided an introduction to the emerging field of designing neural networks which are sparsely activated in a modular fashion, via the use of conditional computation techniques. To this end, we have provided both a general mathematical formalism to categorize these approaches, and then an overview of several concrete implementations including mixture-of-expert models and early exit neural networks. Although these models have been investigated mostly for improving training and<sub>/</sub>or inference time, we have discussed a number of additional emerging benefits from this approach, including specialization, generalization, and explainability. Many of these benefits are only starting to be investigated, opening up interesting avenues of research.

Some common challenges have also emerged from our discussion: (a) being able to control and adapt the inference and<sub>/</sub>or training time is still an open challenge, with most techniques providing a fixed accuracy-time trade-off (e.g., MoEs with top-k routing); (b) sparse routing introduces balancing and collapse challenges that must be taken care of; (c) most routing decisions are taken only locally (e.g., layer-wise), while taking them globally requires sampling from a combinatorially large search space requiring new sampling techniques <sub>[</sub>60<sub>]</sub>; (d) outside of accuracy, benchmarks and metrics for evaluating specialization and generalization of these models are still being developed <sub>[</sub>55<sub>]</sub>.

There are also several research directions that we were not able to touch due to space constraints: these include scaling laws for modular models <sub>[</sub>15<sub>]</sub>, biological plausibility <sub>[</sub>83, 111<sub>]</sub>, and exploiting these models in specific applicative fields such as split computing <sub>[</sub>52<sub>]</sub> and semantic communication <sub>[</sub>108<sub>]</sub>.

## Acknowledgments

S. Scardapane is partly funded by Sapienza grants RM1221816BD028D6 (DESMOS) and RG123188B3EF6A80 (CENTS). P. Minervini is partially funded by ELIAI (The Edinburgh Laboratory for Integrated Artificial Intelligence), EPSRC (grant no. EP<sub>/</sub>W002876<sub>/</sub>1), an industry grant from Cisco, and a donation from Accenture LLP.

## References

<sub>[</sub>2<sub>]</sub> J. Andreas, M. Rohrbach, T. Darrell, and D. Klein. Neural module networks. In Proceedings of the 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 39–48, 2016.

<sub>[</sub>4<sub>]</sub> A. Bakhtiarnia, Q. Zhang, and A. Iosifidis. Improving the accuracy of early exits in multi-exit architectures via curriculum learning. In Proceedings of the 2021 International Joint Conference on Neural Networks (IJCNN), pages 1–8. IEEE, 2021.

<sub>[</sub>5<sub>]</sub> E. Bengio, P.-L. Bacon, J. Pineau, and D. Precup. Conditional computation in neural networks for faster models. arXiv preprint arXiv:1511.06297, 2015.

<sub>[</sub>6<sub>]</sub> F. Biadsy, Y. Chen, X. Zhang, O. Rybakov, A. Rosenberg, and P. Moreno. A scalable model specialization framework for training and inference using submodels and its application to speech model personalization. In Interspeech 2022. ISCA, 2022.

<sub>[</sub>7<sub>]</sub> S. Bills, N. Cammarata, D. Mossing, H. Tillman, L. Gao, G. Goh, I. Sutskever, J. Leike, J. Wu, and W. Saunders. Language models can explain neurons in language models. 2023. OpenAI Blog, 14, 2023.

<sub>[</sub>8<sub>]</sub> T. Bolukbasi, J. Wang, O. Dekel, and V. Saligrama. Adaptive neural networks for efficient inference. In Proceedings of the 34th International Conference on Machine Learning - Volume 70, ICML’17, page 527–536. JMLR.org, 2017.

<sub>[</sub>9<sub>]</sub> D. Bolya, C.-Y. Fu, X. Dai, P. Zhang, C. Feichtenhofer, and J. Hoffman. Token merging: Your ViT but faster. In Proceedings of the 2023 International Conference on Learning Representations (ICLR), 2023.

<sub>[</sub>10<sub>]</sub> D. Bolya and J. Hoffman. Token merging for fast stable diffusion. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 4598–4602, 2023.

<sub>[</sub>11<sub>]</sub> A. Bontempelli, S. Teso, K. Tentori, F. Giunchiglia, and A. Passerini. Concept-level debugging of part-prototype networks. arXiv preprint arXiv:2205.15769, 2022.

<sub>[</sub>12<sub>]</sub> T. Chen, Y. Cheng, Z. Gan, L. Yuan, L. Zhang, and Z. Wang. Chasing sparsity in vision transformers: An end-to-end exploration. In M. Ranzato, A. Beygelzimer, Y. Dauphin, P. Liang, and J. W. Vaughan, editors, Advances in Neural Information Processing Systems, volume 34, pages 19974–19988, 2021.

<sub>[</sub>13<sub>]</sub> X. Chen, Z. Liu, H. Tang, L. Yi, H. Zhao, and S. Han. Sparsevit: Revisiting activation sparsity for efficient high-resolution vision transformer. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 2061– 2070, June 2023.

<sub>[</sub>14<sub>]</sub> R. Child, S. Gray, A. Radford, and I. Sutskever. Generating long sequences with sparse transformers. arXiv preprint arXiv:1904.10509, 2019.

<sub>[</sub>15<sub>]</sub> A. Clark, D. De Las Casas, A. Guy, A. Mensch, M. Paganini, J. Hoffmann, B. Damoc, B. Hechtman, T. Cai, S. Borgeaud, G. B. Van Den Driessche, E. Rutherford, T. Hennigan, M. J. Johnson, A. Cassirer, C. Jones, E. Buchatskaya, D. Budden, L. Sifre, S. Osindero, O. Vinyals, M. Ranzato, J. Rae, E. Elsen, K. Kavukcuoglu, and K. Simonyan. Unified scaling laws for routed language models. In Proceedings of the 39th International Conference on Machine Learning, volume 162 of Proceedings of Machine Learning Research, pages 4057–4086. PMLR, 17–23 Jul 2022.

<sub>[</sub>17<sub>]</sub> D. Dai, C. Deng, C. Zhao, R. Xu, H. Gao, D. Chen, J. Li, W. Zeng, X. Yu, Y. Wu, et al. Deepseekmoe: Towards ultimate expert specialization in mixture-of-experts language models. arXiv preprint arXiv:2401.06066, 2024.

<sub>[</sub>18<sub>]</sub> T. Darcet, M. Oquab, J. Mairal, and P. Bojanowski. Vision transformers need registers. In Proceedings of the 2024 International Conference on Learning Representations (ICLR), 2024.

<sub>[</sub>19<sub>]</sub> T. Dettmers and L. Zettlemoyer. Sparse networks from scratch: Faster training without losing performance. arXiv preprint arXiv:1907.04840, 2019.

<sub>[</sub>20<sub>]</sub> W. Fedus, J. Dean, and B. Zoph. A review of sparse expert models in deep learning. arXiv preprint arXiv:2209.01667, 2022.

<sub>[</sub>21<sub>]</sub> W. Fedus, B. Zoph, and N. Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. The Journal of Machine Learning Research, 23(1):5232–5270, 2022.

<sub>[</sub>22<sub>]</sub> Q. Fournier, G. M. Caron, and D. Aloise. A practical survey on faster and lighter transformers. ACM Computing Surveys, 55(14s):1–40, 2023.

<sub>[</sub>23<sub>]</sub> A. Ghodrati, B. E. Bejnordi, and A. Habibian. Frameexit: Conditional early exiting for efficient video recognition. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 15608–15618, 2021.

<sub>[</sub>24<sub>]</sub> Y. Han, G. Huang, S. Song, L. Yang, H. Wang, and Y. Wang. Dynamic neural networks: A survey. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(11):7436– 7456, 2021.

<sub>[</sub>25<sub>]</sub> Y. Han, Y. Pu, Z. Lai, C. Wang, S. Song, J. Cao, W. Huang, C. Deng, and G. Huang. Learning to weight samples for dynamic early-exiting networks. In European Conference on Computer Vision, pages 362–378. Springer, 2022.

<sub>[</sub>26<sub>]</sub> V. Hassija, V. Chamola, A. Mahapatra, A. Singal, D. Goel, K. Huang, S. Scardapane, I. Spinelli, M. Mahmud, and A. Hussain. Interpreting black-box models: a review on explainable artificial intelligence. Cognitive Computation, 16(1):45–74, 2024.

<sub>[</sub>27<sub>]</sub> J. B. Haurum, S. Escalera, G. W. Taylor, and T. B. Moeslund. Which tokens to use? investigating token reduction in vision transformers. In Proceedings of the IEEE<sub>/</sub>CVF International Conference on Computer Vision (ICCV), pages 773–783, 2023.

<sub>[</sub>28<sub>]</sub> J. D. Havtorn, A. Royer, T. Blankevoort, and B. E. Bejnordi. Msvit: Dynamic mixedscale tokenization for vision transformers. In Proceedings of the IEEE<sub>/</sub>CVF International Conference on Computer Vision (ICCV) Workshops, pages 838–848, October 2023.

<sub>[</sub>29<sub>]</sub> H. Hazimeh, Z. Zhao, A. Chowdhery, M. Sathiamoorthy, Y. Chen, R. Mazumder, L. Hong, and E. Chi. Dselect-k: Differentiable selection in the mixture of experts with applications to multi-task learning. Advances in Neural Information Processing Systems, 34:29335–29347, 2021.

<sub>[</sub>30<sub>]</sub> X. He, I. Keivanloo, Y. Xu, X. He, B. Zeng, S. Rajagopalan, and T. Chilimbi. Magic pyramid: Accelerating inference with early exiting and token pruning. In NeurIPS 2021 Workshop on Efficient Natural Language and Speech Processing, 2021.

<sub>[</sub>31<sub>]</sub> C. Herrmann, R. S. Bowen, and R. Zabih. Channel selection using Gumbel Softmax. In European Conference on Computer Vision, pages 241–257. Springer, 2020.

<sub>[</sub>33<sub>]</sub> Y. Huang, S. Hu, X. Han, Z. Liu, and M. Sun. Unified view of grokking, double descent and emergent abilities: A perspective from circuits competition. arXiv preprint arXiv:2402.15175, 2024.

<sub>[</sub>34<sub>]</sub> I. A. Huijben, W. Kool, M. B. Paulus, and R. J. Van Sloun. A review of the Gumbel-max trick and its extensions for discrete stochasticity in machine learning. IEEE Transactions on Pattern Analysis and Machine Intelligence, 45(2):1353–1371, 2022.

<sub>[</sub>35<sub>]</sub> E. Jang, S. Gu, and B. Poole. Categorical reparameterization with Gumbel-Softmax. 2017.

<sub>[</sub>36<sub>]</sub> S. Jaszczur, A. Chowdhery, A. Mohiuddin, L. Kaiser, W. Gajewski, H. Michalewski, and J. Kanerva. Sparse is enough in scaling transformers. Advances in Neural Information Processing Systems, 34:9895–9907, 2021.

<sub>[</sub>37<sub>]</sub> A. Q. Jiang, A. Sablayrolles, A. Roux, A. Mensch, B. Savary, C. Bamford, D. S. Chaplot, D. d. l. Casas, E. B. Hanna, F. Bressand, et al. Mixtral of experts. arXiv preprint arXiv:2401.04088, 2024.

<sub>[</sub>38<sub>]</sub> Y.-H. Jin, K.-H. Lee, and D.-W. Choi. Querynet: Querying neural networks for lightweight specialized models. Information Sciences, 589:186–198, 2022.

<sub>[</sub>39<sub>]</sub> M. Jordan and R. Jacobs. Hierarchical mixtures of experts and the em algorithm. 1993.

<sub>[</sub>40<sub>]</sub> N. Kandpal, B. Lester, M. Muqeeth, A. Mascarenhas, M. Evans, V. Baskaran, T. Huang, H. Liu, and C. Raffel. Git-theta: a git extension for collaborative development of machine learning models. In Proceedings of the 40th International Conference on Machine Learning, ICML’23. JMLR.org, 2023.

<sub>[</sub>41<sub>]</sub> P. Karpikova, E. Radionova, A. Yaschenko, A. Spiridonov, L. Kostyushko, R. Fabbricatore, and A. Ivakhnenko. Fiancee: Faster inference of adversarial networks via conditional early exits. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 12032–12043, 2023.

<sub>[</sub>42<sub>]</sub> M. Kim, S. Gao, Y.-C. Hsu, Y. Shen, and H. Jin. Token fusion: Bridging the gap between token pruning and token merging. In Proceedings of the IEEE<sub>/</sub>CVF Winter Conference on Applications of Computer Vision (WACV), pages 1383–1392, January 2024.

<sub>[</sub>43<sub>]</sub> W. Kool, H. Van Hoof, and M. Welling. Ancestral gumbel-top-k sampling for sampling without replacement. The Journal of Machine Learning Research, 21(1):1726–1761, 2020.

<sub>[</sub>44<sub>]</sub> A. Kouris, S. I. Venieris, S. Laskaridis, and N. Lane. Multi-exit semantic segmentation networks. In European Conference on Computer Vision, pages 330–349. Springer, 2022.

<sub>[</sub>45<sub>]</sub> D. Lepikhin, H. Lee, Y. Xu, D. Chen, O. Firat, Y. Huang, M. Krikun, N. Shazeer, and Z. Chen. Gshard: Scaling giant models with conditional computation and automatic sharding. In Proceedings of the 2021 International Conference on Learning Representations (ICLR), 2021.

<sub>[</sub>46<sub>]</sub> B. Li, Y. Shen, J. Yang, Y. Wang, J. Ren, T. Che, J. Zhang, and Z. Liu. Sparse mixtureof-experts are domain generalizable learners. arXiv preprint arXiv:2206.04046, 2022.

<sub>[</sub>48<sub>]</sub> H. Liu, K. Simonyan, and Y. Yang. Darts: Differentiable architecture search. 2019.

<sub>[</sub>49<sub>]</sub> T. Liu, M. Blondel, C. Riquelme, and J. Puigcerver. Routers in vision mixture of experts: An empirical study. arXiv preprint arXiv:2401.15969, 2024.

<sub>[</sub>50<sub>]</sub> Y. Liu, M. Gehrig, N. Messikommer, M. Cannici, and D. Scaramuzza. Revisiting token pruning for object detection and instance segmentation. In Proceedings of the IEEE<sub>/</sub>CVF Winter Conference on Applications of Computer Vision, pages 2658–2668, 2024.

<sub>[</sub>51<sub>]</sub> C. J. Maddison, A. Mnih, and Y. W. Teh. The concrete distribution: A continuous relaxation of discrete random variables. 2017.

<sub>[</sub>52<sub>]</sub> Y. Matsubara, M. Levorato, and F. Restuccia. Split computing and early exiting for deep learning applications: Survey and research challenges. ACM Computing Surveys, 55(5):1–30, 2022.

<sub>[</sub>53<sub>]</sub> L. Meng, H. Li, B.-C. Chen, S. Lan, Z. Wu, Y.-G. Jiang, and S.-N. Lim. Adavit: Adaptive vision transformers for efficient image recognition. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 12309–12318, 2022.

<sub>[</sub>54<sub>]</sub> G. Mialon, R. Dessì, M. Lomeli, C. Nalmpantis, R. Pasunuru, R. Raileanu, B. Rozière, T. Schick, J. Dwivedi-Yu, A. Celikyilmaz, E. Grave, Y. LeCun, and T. Scialom. Augmented language models: a survey. Transactions on Machine Learning Research, 6:1–35, 2023.

<sub>[</sub>55<sub>]</sub> S. Mittal, Y. Bengio, and G. Lajoie. Is a modular architecture enough? Advances in Neural Information Processing Systems, 35:28747–28760, 2022.

<sub>[</sub>56<sub>]</sub> M. Mohammed, H. Liu, and C. Raffel. Models with conditional computation learn suboptimal solutions. In I Can’t Believe It’s Not Better Workshop: Understanding Deep Learning Through Empirical Falsification, 2022.

<sub>[</sub>57<sub>]</sub> M. Muqeeth, H. Liu, Y. Liu, and C. Raffel. Learning to route among specialized experts for zero-shot generalization. arXiv preprint arXiv:2402.05859, 2024.

<sub>[</sub>58<sub>]</sub> M. Muqeeth, H. Liu, and C. Raffel. Soft merging of experts with adaptive routing. arXiv preprint arXiv:2306.03745, 2023.

<sub>[</sub>59<sub>]</sub> B. Mustafa, C. Riquelme, J. Puigcerver, R. Jenatton, and N. Houlsby. Multimodal contrastive learning with limoe: the language-image mixture of experts. Advances in Neural Information Processing Systems, 35:9564–9576, 2022.

<sub>[</sub>60<sub>]</sub> V. Niculae, C. F. Corro, N. Nangia, T. Mihaylova, and A. F. Martins. Discrete latent structure in neural networks. arXiv preprint arXiv:2301.07473, 2023.

<sub>[</sub>61<sub>]</sub> B. Pan, R. Panda, Y. Jiang, Z. Wang, R. Feris, and A. Oliva. Ia-red<sup>2</sup>: Interpretabilityaware redundancy reduction for vision transformers. Advances in Neural Information Processing Systems, 34:24898–24911, 2021.

<sub>[</sub>62<sub>]</sub> Z. Pan, J. Cai, and B. Zhuang. Stitchable neural networks. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 16102–16112, 2023.

<sub>[</sub>63<sub>]</sub> Z. Pan, B. Zhuang, H. He, J. Liu, and J. Cai. Less is more: Pay less attention in vision transformers. Proceedings of the AAAI Conference on Artificial Intelligence, 36(2):2035– 2043, Jun. 2022.

<sub>[</sub>64<sub>]</sub> N. Passalis, J. Raitoharju, A. Tefas, and M. Gabbouj. Efficient adaptive inference for deep convolutional neural networks using hierarchical early exits. Pattern Recognition, 105:107346, 2020.

<sub>[</sub>65<sub>]</sub> J. Pfeiffer, G. Geigle, A. Kamath, J.-M. Steitz, S. Roth, I. Vuli´c, and I. Gurevych. xGQA: Cross-lingual visual question answering. In S. Muresan, P. Nakov, and A. Villavicencio, editors, Findings of the Association for Computational Linguistics: ACL 2022, pages 2497–2511. Association for Computational Linguistics, May 2022.

<sub>[</sub>68<sub>]</sub> J. Pfeiffer, S. Ruder, I. Vuli´c, and E. M. Ponti. Modular deep learning. Transactions on Machine Learning Research, 11:1–76, 2023.

<sub>[</sub>69<sub>]</sub> M. Piórczynski, F. Szatkowski, K. Bałazy, and B. Wójcik. Exploiting transformer acti-´ vation sparsity with dynamic inference. arXiv preprint arXiv:2310.04361, 2023.

<sub>[</sub>70<sub>]</sub> J. Pomponi, S. Scardapane, and A. Uncini. A probabilistic re-intepretation of confidence scores in multi-exit models. Entropy, 24:1, 2021.

<sub>[</sub>71<sub>]</sub> E. M. Ponti, A. Sordoni, Y. Bengio, and S. Reddy. Combining modular skills in multitask learning. arXiv preprint arXiv:2202.13914, 2022.

<sub>[</sub>72<sub>]</sub> J. Puigcerver, C. Riquelme, B. Mustafa, and N. Houlsby. From sparse to soft mixtures of experts. arXiv preprint arXiv:2308.00951, 2023.

<sub>[</sub>73<sub>]</sub> J. Puigcerver, C. Riquelme, B. Mustafa, C. Renggli, A. S. Pinto, S. Gelly, D. Keysers, and N. Houlsby. Scalable transfer learning with expert models. In Proceedings of the 2021 International Conference on Learning Representations (ICLR), 2021.

<sub>[</sub>74<sub>]</sub> Z. Qiu, Z. Huang, and J. Fu. Emergent mixture-of-experts: Can dense pretrained transformers benefit from emergent modular structures? arXiv preprint arXiv:2310.10908, 2023.

<sub>[</sub>75<sub>]</sub> S. Rajbhandari, C. Li, Z. Yao, M. Zhang, R. Y. Aminabadi, A. A. Awan, J. Rasley, and Y. He. DeepSpeed-MoE: Advancing mixture-of-experts inference and training to power next-generation AI scale. In Proceedings of the 39th International Conference on Machine Learning, volume 162 of Proceedings of Machine Learning Research, pages 18332– 18346. PMLR, 2022.

<sub>[</sub>76<sub>]</sub> J. Rajendran, A. Lakshminarayanan, M. M. Khapra, P. P, and B. Ravindran. Attend, adapt and transfer: Attentive deep architecture for adaptive transfer from multiple sources in the same domain. In Proceedings of the 2017 International Conference on Learning Representations (ICLR), 2017.

<sub>[</sub>77<sub>]</sub> Y. Rao, W. Zhao, B. Liu, J. Lu, J. Zhou, and C.-J. Hsieh. Dynamicvit: Efficient vision transformers with dynamic token sparsification. Advances in Neural Information Processing Systems, 34:13937–13949, 2021.

<sub>[</sub>78<sub>]</sub> C. Renggli, A. S. Pinto, N. Houlsby, B. Mustafa, J. Puigcerver, and C. Riquelme. Learning to merge tokens in vision transformers. arXiv preprint arXiv:2202.12015, 2022.

<sub>[</sub>79<sub>]</sub> C. Riquelme, J. Puigcerver, B. Mustafa, M. Neumann, R. Jenatton, A. Susano Pinto, D. Keysers, and N. Houlsby. Scaling vision with sparse mixture of experts. Advances in Neural Information Processing Systems, 34:8583–8595, 2021.

<sub>[</sub>80<sub>]</sub> C. Rosenbaum, T. Klinger, and M. Riemer. Routing networks: Adaptive selection of non-linear functions for multi-task learning. In Proceedings of the 2018 International Conference on Learning Representations (ICLR), 2018.

<sub>[</sub>81<sub>]</sub> S. Sarti, E. Lomurno, and M. Matteucci. Anticipate, ensemble and prune: Improving convolutional neural networks via aggregated early exits. Procedia Computer Science, 222:519–528, 2023.

<sub>[</sub>82<sub>]</sub> S. Scardapane, D. Comminiello, M. Scarpiniti, E. Baccarelli, and A. Uncini. Differentiable branching in deep networks for fast inference. In Proceedings of the 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pages 4167–4171. IEEE, 2020.

<sub>[</sub>83<sub>]</sub> S. Scardapane, M. Scarpiniti, E. Baccarelli, and A. Uncini. Why should we add early exits to neural networks? Cognitive Computation, 12(5):954–966, 2020.

<sub>[</sub>84<sub>]</sub> T. Schuster, A. Fisch, J. Gupta, M. Dehghani, D. Bahri, V. Tran, Y. Tay, and D. Metzler. Confident adaptive language modeling. Advances in Neural Information Processing Systems, 35:17456–17472, 2022.

<sub>[</sub>85<sub>]</sub> N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, and J. Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. In Proceedings of the 2017 International Conference on Learning Representations (ICLR), 2017.

<sub>[</sub>86<sub>]</sub> T. Shen, M. Ott, M. Auli, and M. Ranzato. Mixture models for diverse machine translation: Tricks of the trade. In International Conference on Machine Learning, pages 5719–5728. PMLR, 2019.

<sub>[</sub>87<sub>]</sub> E. C. Strinati, P. Di Lorenzo, V. Sciancalepore, A. Aijaz, M. Kountouris, D. Gündüz, P. Popovski, M. Sana, P. A. Stavrou, B. Soret, et al. Goal-oriented and semantic communication in 6g ai-native networks: The 6g-goals approach. arXiv preprint arXiv:2402.07573, 2024.

<sub>[</sub>88<sub>]</sub> S. Tan, Y. Shen, Z. Chen, A. Courville, and C. Gan. Sparse universal transformer. In H. Bouamor, J. Pino, and K. Bali, editors, Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 169–179. Association for Computational Linguistics, Dec. 2023.

<sub>[</sub>89<sub>]</sub> S. Tang, Y. Wang, Z. Kong, T. Zhang, Y. Li, C. Ding, Y. Wang, Y. Liang, and D. Xu. You need multiple exiting: Dynamic early exiting for accelerating unified vision language model. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 10781–10791, 2023.

<sub>[</sub>90<sub>]</sub> S. Teerapittayanon, B. McDanel, and H.-T. Kung. Branchynet: Fast inference via early exiting from deep neural networks. In Proceedings of the 2016 23rd International Conference on Pattern Recognition (ICPR), pages 2464–2469. IEEE, 2016.

<sub>[</sub>91<sub>]</sub> M. Treviso, A. Góis, P. Fernandes, E. Fonseca, and A. Martins. Predicting attention sparsity in transformers. In A. Vlachos, P. Agrawal, A. Martins, G. Lampouras, and C. Lyu, editors, Proceedings of the Sixth Workshop on Structured Prediction for NLP, pages 67–81. Association for Computational Linguistics, May 2022.

<sub>[</sub>92<sub>]</sub> T. Verelst and T. Tuytelaars. Dynamic convolutions: Exploiting spatial sparsity for faster inference. In Proceedings of the 2020 IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR). IEEE, 2020.

<sub>[</sub>93<sub>]</sub> T. Vu, A. Barua, B. Lester, D. Cer, M. Iyyer, and N. Constant. Overcoming catastrophic forgetting in zero-shot cross-lingual generation. In Y. Goldberg, Z. Kozareva, and Y. Zhang, editors, Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 9279–9300, Abu Dhabi, United Arab Emirates, Dec. 2022. Association for Computational Linguistics.

<sub>[</sub>94<sub>]</sub> H. Wang, T. Fu, Y. Du, W. Gao, K. Huang, Z. Liu, P. Chandak, S. Liu, P. Van Katwyk, A. Deac, et al. Scientific discovery in the age of artificial intelligence. Nature, 620(7972):47–60, 2023.

<sub>[</sub>95<sub>]</sub> M. Wang, J. Mo, J. Lin, Z. Wang, and L. Du. Dynexit: A dynamic early-exit strategy for deep residual networks. In Proceedings of the 2019 IEEE International Workshop on Signal Processing Systems (SiPS), pages 178–183. IEEE, 2019.

<sub>[</sub>96<sub>]</sub> X. Wang and Y. Li. Harmonized dense knowledge distillation training for multi-exit architectures. Proceedings of the AAAI Conference on Artificial Intelligence, 35:10218– 10226, 2021.

<sub>[</sub>97<sub>]</sub> B. Wójcik, A. Devoto, K. Pustelnik, P. Minervini, and S. Scardapane. Adaptive computation modules: Granular conditional computation for efficient inference. arXiv preprint arXiv:2312.10193, 2023.

<sub>[</sub>98<sub>]</sub> M. Wołczyk, B. Wójcik, K. Bałazy, I. T. Podolak, J. Tabor, M. Smieja, and T. Trzcinski. <sup>´</sup> Zero time waste: Recycling predictions in early exit neural networks. Advances in Neural Information Processing Systems, 34:2516–2528, 2021.

<sub>[</sub>99<sub>]</sub> J. Xin, R. Tang, J. Lee, Y. Yu, and J. Lin. DeeBERT: Dynamic early exiting for accelerating BERT inference. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 2246–2251. Association for Computational Linguistics, July 2020.

<sub>[</sub>100<sub>]</sub> Q. Xing, M. Xu, T. Li, and Z. Guan. Early exit or not: Resource-efficient blind quality enhancement for compressed images. In European Conference on Computer Vision, pages 275–292. Springer, 2020.

<sub>[</sub>101<sub>]</sub> X. Xu, S. Wang, Y. Chen, Y. Zheng, Z. Wei, and J. Liu. Gtp-vit: Efficient vision transformers via graph-based token propagation. In Proceedings of the IEEE<sub>/</sub>CVF Winter Conference on Applications of Computer Vision (WACV), pages 86–95, January 2024.

<sub>[</sub>102<sub>]</sub> F. Xue, V. Likhosherstov, A. Arnab, N. Houlsby, M. Dehghani, and Y. You. Adaptive computation with elastic input sequence. In Proceedings of the 40th International Conference on Machine Learning, ICML’23. JMLR.org, 2023.

<sub>[</sub>103<sub>]</sub> F. Xue, Z. Zheng, Y. Fu, J. Ni, Z. Zheng, W. Zhou, and Y. You. Openmoe: An early effort on open mixture-of-experts language models. arXiv preprint arXiv:2402.01739, 2024.

<sub>[</sub>104<sub>]</sub> J. Yang, Q. Zhang, B. Ni, L. Li, J. Liu, M. Zhou, and Q. Tian. Modeling point clouds with self-attention and gumbel subset sampling. In 2019 IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 3318–3327, 2019.

<sub>[</sub>105<sub>]</sub> H. Yin, A. Vahdat, J. M. Alvarez, A. Mallya, J. Kautz, and P. Molchanov. A-vit: Adaptive tokens for efficient vision transformer. In Proceedings of the IEEE<sub>/</sub>CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 10809–10818, 2022.

<sub>[</sub>106<sub>]</sub> S. E. Yuksel, J. N. Wilson, and P. D. Gader. Twenty years of mixture of experts. IEEE Transactions on Neural Networks and Learning Systems, 23(8):1177–1193, 2012.

<sub>[</sub>107<sub>]</sub> T. Zadouri, A. Üstün, A. Ahmadian, B. Ermi¸s, A. Locatelli, and S. Hooker. Pushing mixture of experts to the limit: Extremely parameter efficient moe for instruction tuning. arXiv preprint arXiv:2309.05444, 2023.

<sub>[</sub>108<sub>]</sub> G. Zhang, Q. Hu, Z. Qin, Y. Cai, and G. Yu. A unified multi-task semantic communication system with domain adaptation. In GLOBECOM 2022-2022 IEEE Global Communications Conference, pages 3971–3976. IEEE, 2022.

<sub>[</sub>109<sub>]</sub> X. Zhang, Y. Shen, Z. Huang, J. Zhou, W. Rong, and Z. Xiong. Mixture of attention heads: Selecting attention heads per token. In Y. Goldberg, Z. Kozareva, and Y. Zhang, editors, Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 4150–4162. Association for Computational Linguistics, Dec. 2022.

<sub>[</sub>110<sub>]</sub> Z. Zhang, Y. Lin, Z. Liu, P. Li, M. Sun, and J. Zhou. MoEfication: Transformer feedforward layers are mixtures of experts. In S. Muresan, P. Nakov, and A. Villavicencio, editors, Findings of the Association for Computational Linguistics: ACL 2022, pages 877–890, Dublin, Ireland, May 2022. Association for Computational Linguistics.

<sub>[</sub>111<sub>]</sub> Z. Zhang, Z. Zeng, Y. Lin, C. Xiao, X. Wang, X. Han, Z. Liu, R. Xie, M. Sun, and J. Zhou. Emergent modularity in pre-trained transformers. In A. Rogers, J. Boyd-Graber, and N. Okazaki, editors, Findings of the Association for Computational Linguistics: ACL 2023, pages 4066–4083. Association for Computational Linguistics, July 2023.

<sub>[</sub>112<sub>]</sub> W. Zhou, C. Xu, T. Ge, J. McAuley, K. Xu, and F. Wei. Bert loses patience: Fast and robust inference with early exit. Advances in Neural Information Processing Systems, 33:18330–18341, 2020.

<sub>[</sub>113<sub>]</sub> Y. Zhou, T. Lei, H. Liu, N. Du, Y. Huang, V. Zhao, A. M. Dai, Q. V. Le, J. Laudon, et al. Mixture-of-experts with expert choice routing. Advances in Neural Information Processing Systems, 35:7103–7114, 2022.

<sub>[</sub>114<sub>]</sub> J. Zhu, X. Zhu, W. Wang, X. Wang, H. Li, X. Wang, and J. Dai. Uni-perceiver-moe: Learning sparse generalist models with conditional moes. Advances in Neural Information Processing Systems, 35:2664–2678, 2022.

<sub>[</sub>115<sub>]</sub> W. Zhu. LeeBERT: Learned early exit for BERT with cross-level optimization. In C. Zong, F. Xia, W. Li, and R. Navigli, editors, Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 2968–2980, Online, Aug. 2021. Association for Computational Linguistics.

<sub>[</sub>116<sub>]</sub> S. Zuo, X. Liu, J. Jiao, Y. J. Kim, H. Hassan, R. Zhang, T. Zhao, and J. Gao. Taming sparsely activated transformer with stochastic experts. In Proceedings of the 2022 International Conference on Learning Representations (ICLR), 2022.