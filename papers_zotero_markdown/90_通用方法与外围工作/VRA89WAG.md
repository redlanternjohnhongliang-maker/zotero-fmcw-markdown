# CONDITIONAL COMPUTATION IN NEURAL NETWORKS FOR FASTER MODELS

Emmanuel Bengio, Pierre-Luc Bacon, Joelle Pineau & Doina Precup

School of Computer Science

McGill University

Montreal, Canada

{ebengi,pbacon,jpineau,dprecup}@cs.mcgill.ca

## ABSTRACT

Deep learning has become the state-of-art tool in many applications, but the evaluation and training of deep models can be time-consuming and computationally expensive. The conditional computation approach has been proposed to tackle this problem (Bengio et al., 2013; Davis & Arel, 2013). It operates by selectively activating only parts of the network at a time. In this paper, we use reinforcement learning as a tool to optimize conditional computation policies. More specifically, we cast the problem of learning activation-dependent policies for dropping out blocks of units as a reinforcement learning problem. We propose a learning scheme motivated by computation speed, capturing the idea of wanting to have parsimonious activations while maintaining prediction accuracy. We apply a policy gradient algorithm for learning policies that optimize this loss function and propose a regularization mechanism that encourages diversification of the dropout policy. We present encouraging empirical results showing that this approach improves the speed of computation without impacting the quality of the approximation.

Keywords Neural Networks, Conditional Computing, REINFORCE

## 1 INTRODUCTION

Large-scale neural networks, and in particular deep learning architectures, have seen a surge in popularity in recent years, due to their impressive empirical performance in complex supervised learning tasks, including state-of-the-art performance in image and speech recognition (He et al., 2015). Yet the task of training such networks remains a challenging optimization problem. Several related problems arise: very long training time (several weeks on modern computers, for some problems), potential for over-fitting (whereby the learned function is too specific to the training data and generalizes poorly to unseen data), and more technically, the vanishing gradient problem (Hochreiter, 1991; Bengio et al., 1994), whereby the gradient information gets increasingly diffuse as it propagates from layer to layer.

Recent approaches (Bengio et al., 2013; Davis & Arel, 2013) have proposed the use of conditional computation in order to address this problem. Conditional computation refers to activating only some of the units in a network, in an input-dependent fashion. For example, if we think we’re looking at a car, we only need to compute the activations of the vehicle detecting units, not of all features that a network could possible compute. The immediate effect of activating fewer units is that propagating information through the network will be faster, both at training as well as at test time. However, one needs to be able to decide in an intelligent fashion which units to turn on and off, depending on the input data. This is typically achieved with some form of gating structure, learned in parallel with the original network.

A secondary effect of conditional computation is that during training, information will be propagated along fewer links. Intuitively, this allows sharper gradients on the links that do get activated. Moreover, because only parts of the network are active, and fewer parameters are used in the computation, the net effect can be viewed as a form of regularization of the main network, as the approximator has to use only a small fraction of the possible parameters in order to produce an action

In this paper, we explore the formulation of conditional computation using reinforcement learning. We propose to learn input-dependent activation probabilities for every node (or blocks of nodes), while trying to jointly minimize the prediction errors at the output and the number of participating nodes at every layer, thus reducing the computational load. One can also think of our method as being related to standard dropout, which has been used as a tool to both regularize and speed up the computation. However, we emphasize that dropout is in fact a form of “unconditional” computation, in which the computation paths are data-independent. Therefore, usual dropout is less likely to lead to specialized computation paths within a network.

We present the problem formulation, and our solution to the proposed optimization problem, using policy search methods (Deisenroth et al., 2013). Preliminary results are included for standard classification benchmarks.

## 2 PROBLEM FORMULATION

Our model consists in a typical fully-connected neural network model, joined with stochastic perlayer policies that activate or deactivate nodes of the neural network in an input-dependent manner, both at train and test time. The exact algorithm is detailed in appendix A.

We cast the problem of learning the input-dependent activation probabilities at each layer in the framework of Markov Decision Processes (MDP) (Puterman, 1994). We define a discrete time, continuous state and discrete action MDP $\left. S , \mathcal { U } , P \left( \cdot \mid s , u \right) , C \right.$ . An action $\mathbf { u } \in \{ 0 , 1 \} ^ { k }$ in this model consists in the application of a mask over the units of a given layer. We define the state space of the MDP over the vector-valued activations $\mathbf { s } \in \mathbb { R } ^ { k }$ of all nodes at the previous layer. The cost C is the loss of the neural network architecture (in our case the negative log-likelihood). This MDP is single-step: an input is seen, an action is taken, a reward is observed and we are at the end state.

Similarly to the way dropout is described (Hinton et al., 2012), each node or block in a given layer has an associated Bernoulli distribution which determines its probability of being activated. We train a different policy for each layer l, and parameterize it (separately of the neural network) such that it is input-dependent. For every layer l of k units, we define a policy as a k-dimensional Bernoull distribution:

$$
\pi ^ { ( l ) } ( \mathbf { u } \mid \mathbf { s } ) = \prod _ { i = 1 } ^ { k } \sigma _ { i } ^ { u _ { i } } ( 1 - \sigma _ { i } ) ^ { ( 1 - u _ { i } ) } , \quad \qquad \sigma _ { i } = [ \mathbf { s i g m } ( \mathbf { Z } ^ { ( l ) } \mathbf { s } + \mathbf { d } ^ { ( l ) } ) ] _ { i } ,\tag{1}
$$

where the $\sigma _ { i }$ denotes the participation probability, to be computed from the activations s of the layer below and the parameters $\theta _ { l } = \{ \mathbf { Z } ^ { ( l ) } , \mathbf { d } ^ { ( l ) } \}$ . We denote the sigmoid function by sigm, the weight matrix by $\mathbf { Z } ,$ and the bias vector by d. The output of a typical hidden layer $\bar { h } ( x )$ that uses this policy is multiplied element-wise with the mask u sampled from the probabilities $\sigma _ { \mathrm { { : } } }$ , and becomes $( h ( x ) \otimes \mathbf { u } )$ . For clarity we did not superscript u, s and $\sigma _ { i }$ with $l ,$ but each layer has its own.

## 3 LEARNING SIGMOID-BERNOULLI POLICIES

We use REINFORCE (Williams, 1992) (detailed in appendix B) to learn the parameters $\Theta _ { \pi } =$ $\{ \theta _ { 1 } , . . . , \theta _ { L } \}$ of the sigmoid-Bernoulli policies. Since the nature of the observation space changes at each decision step, we learn L disjoint policies (one for each layer l of the deep network). As a consequence, the summation in the policy gradient disappears and becomes:

$$
\nabla _ { \boldsymbol { \theta } _ { l } } \mathcal { L } = \mathbb { E } \left\{ C ( \mathbf { x } ) \nabla _ { \boldsymbol { \theta } _ { l } } \log \pi ^ { ( l ) } ( \mathbf { u } ^ { ( l ) } | \mathbf { s } ^ { ( l ) } ) \right\}\tag{2}
$$

since $\theta _ { l } = \{ \mathbf { Z } ^ { ( l ) } , \mathbf { d } ^ { ( l ) } \}$ only appears in the l-th decision stage and the gradient is zero otherwise.

Estimating (2) from samples requires propagating through many instances at a time, which we achieve through mini-batches of size $m _ { b }$ . Under the mini-batch setting, $\mathbf { s } ^ { ( l ) }$ becomes a matrix and $\pi ( \cdot | \cdot )$ a vector of dimension $m _ { b }$ . Taking the gradient of the parameters with respect to the

log action probabilities can then be seen as forming a Jacobian. We can thus re-write the empirical average in matrix form:

$$
\nabla _ { \theta _ { l } } \mathcal { L } \approx \frac { 1 } { m _ { b } } \sum _ { i = 1 } ^ { m _ { b } } C ( \mathbf { x } _ { i } ) \nabla _ { \theta _ { l } } \log \pi ^ { ( l ) } ( \mathbf { u } _ { i } ^ { ( l ) } | \mathbf { s } _ { i } ^ { ( l ) } ) = \frac { 1 } { m _ { b } } \mathbf { c } ^ { \top } \nabla _ { \theta _ { l } } \log \pi ^ { ( l ) } ( \mathbf { U } ^ { ( l ) } | \mathbf { S } ^ { ( l ) } )\tag{3}
$$

where $C ( \mathbf { x } _ { i } )$ is the total cost for input $\mathbf { x } _ { i }$ and $m _ { b }$ is the number of examples in the mini-batch. The term $\mathbf { c } ^ { \top }$ denotes the row vector containing the total costs for every example in the mini-batch.

## 3.1 FAST VECTOR-JACOBIAN MULTIPLICATION

While Eqn (3) suggests that the Jacobian might have to be formed explicitly, Pearlmutter (1994) showed that computing a differential derivative suffices to compute left or right vector-Jacobian (or Hessian) multiplication. The same trick has also recently been revived with the class of socalled “Hessian-free” (Martens, 2010) methods for artificial neural networks. Using the notation of Pearlmutter (1994), we write $\mathcal { R } _ { \theta _ { l } } \left\{ \cdot \right\} = \mathbf { c } ^ { \top } \nabla _ { \theta _ { l } }$ for the differential operator.

$$
\nabla _ { \boldsymbol { \theta } _ { l } } \mathcal { L } \approx \frac { 1 } { m _ { b } } \mathcal { R } _ { \boldsymbol { \theta } _ { l } } \left\{ \log \pi ( \mathbf { U } ^ { ( l ) } \mid \mathbf { S } ^ { ( l ) } ) \right\}\tag{4}
$$

## 3.2 SPARSITY AND VARIANCE REGULARIZATIONS

$L _ { b }$ $L _ { e }$ $\tau$

$$
L _ { b } = \sum _ { j } ^ { n } \| \mathbb { E } \{ \sigma _ { j } \} - \tau \| _ { 2 } \qquad L _ { e } = \mathbb { E } \{ \| ( \frac { 1 } { n } \sum _ { j } ^ { n } \sigma _ { j } ) - \tau \| _ { 2 } \}\tag{5}
$$

Since we are in a minibatch setting, these expectations can be approximated over the minibatch:

$$
L _ { b } \approx \sum _ { j } ^ { n } \| \frac { 1 } { m _ { b } } \sum _ { i } ^ { m _ { b } } ( \sigma _ { i j } ) - \tau \| _ { 2 } \qquad L _ { e } \approx \frac { 1 } { m _ { b } } \sum _ { i } ^ { m _ { b } } \| ( \frac { 1 } { n } \sum _ { j } ^ { n } \sigma _ { i j } ) - \tau \| _ { 2 }\tag{6}
$$

We finally add a third term, ${ \cal L } _ { v } ,$ in order to favour the aforementioned configurations, where units only have a high probability of activation for certain examples, and low for the rest. We aim to maximize the variances of activations of each unit, across the data. This encourages units’ activations to be varied, and while similar in spirit to the $L _ { b }$ term, this term explicitly discourages learning a uniform distribution.

$$
L _ { v } = - \sum _ { j } ^ { n } { \mathrm { v a r } _ { i } \{ \sigma _ { i j } \} } \approx - \sum _ { j } ^ { n } { \frac { 1 } { m _ { b } } \sum _ { i } ^ { m _ { b } } \left( \sigma _ { i j } - \left( { \frac { 1 } { m _ { b } } \sum _ { i } ^ { m _ { b } } \sigma _ { i j } } \right) \right) ^ { 2 } }\tag{7}
$$

## 3.3 ALGORITHM

We interleave the learning of the network parameters $\Theta _ { N N }$ and the learning of the policy parameters $\Theta _ { \pi }$ . We first update the network and policy parameters to minimize the following regularized loss function via backpropagation (Rumelhart et al., 1988):

$$
\begin{array} { r } { \mathcal { L } = - \log P ( \mathbf { Y } \mid \mathbf { X } , \Theta _ { N N } ) + \lambda _ { s } ( L _ { b } + L _ { e } ) + \lambda _ { v } ( L _ { v } ) + \lambda _ { L 2 } \| \Theta _ { N N } \| ^ { 2 } + \lambda _ { L 2 } \| \Theta _ { \pi } \| ^ { 2 } } \end{array}
$$

where $\lambda _ { s }$ can be understood as a trade-off parameter between prediction accuracy and parsimony of computation (obtained through sparse node activation), and $\lambda _ { v }$ as a trade-off parameter between a stochastic policy and a more input dependent saturated policy. We then minimize the cost function C with a REINFORCE-style approach to update the policy parameters (Williams, 1992):

$$
C = - \log P ( \mathbf { Y } | \mathbf { X } , \Theta _ { N N } )
$$

As previously mentioned, we use minibatch stochastic gradient descent as well as minibatch policy gradient updates. A detailed algorithm is available in appendix A.

## 3.4 BLOCK ACTIVATION POLICY

$$
( ( H \otimes M _ { H } ) W ) \otimes M _ { O }
$$

where $M _ { H }$ and $M _ { O }$ are binary mask matrices. $M _ { O }$ is obtained for each layer from the sampling of the policy as described in eq. 1: each sampled action (0 or 1) is repeated so as to span the corresponding block. $M _ { H }$ is simply the mask of the previous layer. $M _ { H }$ and $M _ { O }$ resemble this (here there are 3 blocks of size 2):

![](images/5e27333d655b847db779ff163e1eb0c33574455f5786f3dcea484d608ef6971c.jpg)

This allows us to quickly perform matrix multiplication by only considering the non-zero output elements as well as the non-zero elements in $H \otimes M _ { H }$

## 4 EXPERIMENTS

## 4.1 MODEL IMPLEMENTATION

The proposed model was implemented within Theano (Bergstra et al., 2010), a standard library for deep learning and neural networks. In addition to using optimizations offered by Theano, we also implemented specialized matrix multiplication code for the operation exposed in section 3.4. A straightforward and fairly naive CPU implementation of this operation yielded speedups of up to 5-10x, while an equally naive GPU implementation yielded speedups of up to 2-4x, both for sparsity rates of under 20% and acceptable matrix and block sizes.

We otherwise use fairly standard methods for our neural network. The weight matrices are initialized using the heuristic of Glorot & Bengio (2010). We use a constant learning rate throughout minibatch SGD. We also use early stopping (Bishop, 2006) to avoid overfitting. We only use fully-connected layers with tanh activations (reLu activations offer similar performance).

## 4.2 MODEL EVALUATION

We first evaluate the performance of our model on the MNIST digit dataset. We use a single hidden layer of 16 blocks of 16 units (256 units total), with a target sparsity rate of $\tau = 6 . 2 5 \% = 1 / 1 6 .$ learning rates of $1 0 ^ { - 3 }$ for the neural network and $5 \times 1 0 ^ { - 5 }$ for the policy, $\lambda _ { v } = \lambda _ { s } = 2 0 0$ and $\lambda _ { L 2 } = 0 . 0 0 5$ . Under these conditions, a test error of around 2.3% was achieved. A normal neural network with the same number of hidden units achieves a test error of around 1.9%, while a normal neural network with a similar amount of computation (multiply-adds) being made (32 hidden units) achieves a test error of around 2.8%.

Looking at the activation of the policy (1c), we see that it tends towards what was hypothesized in section 3.2, i.e. where examples activate most units with low probability and some units with high probability. We can also observe that the policy is input-dependent in figures 1a and 1b, since we see different activation patterns for inputs of class ’0’ and inputs of class ’1’.

Since the computation performed in our model is sparse, one could hope that it achieves this perfor mance with less computation time, yet we consistently observe that models that deal with MNIST are too small to allow our specialized (3.4) sparse implementation to make a substantial difference. We include this result to highlight conditions under which it is less desirable to use our model.

![](images/e318bb83e419bb6c75448b0fbf4c79e820da0cc7a4803f0e9fe8979c7aecba02.jpg)  
(a)

![](images/92551f99d7d27c4f53da7d5e4f238dd88f754241e294cccb196c686e5733b38d.jpg)  
(b)

![](images/691b1e31b25eefdea04ef59030957940136bcb8841370e8a6ec9cad433a05dea.jpg)  
(c)

![](images/121312f6711943c99a1d66833031b506cbd1b97b63c52c7dfa86c756a362b8c9.jpg)  
(d)

Figure 1: MNIST, (a,b,c), probability distribution of the policy, each example’s probability (y axis) of activating each unit (x axis) is plotted as a transparent red dot. Redder regions represent more examples falling in the probability region. Plot (a) is for class ’0’, (b) for class ’1’, (c) for all classes. (d), weight matrix of the policy.
<table><tr><td rowspan=1 colspan=1>model</td><td rowspan=1 colspan=1>test error</td><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>#blocks</td><td rowspan=1 colspan=1>block size</td><td rowspan=1 colspan=1>test time</td><td rowspan=1 colspan=1>speedup</td></tr><tr><td rowspan=1 colspan=1>condnet</td><td rowspan=1 colspan=1>0.511</td><td rowspan=1 colspan=1>1/24</td><td rowspan=1 colspan=1>24,24</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>6.8s(26.2s)</td><td rowspan=1 colspan=1>3.8×</td></tr><tr><td rowspan=1 colspan=1>condnet</td><td rowspan=1 colspan=1>0.514</td><td rowspan=1 colspan=1>1/16</td><td rowspan=1 colspan=1>16,32</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>1.4s (8.2s)</td><td rowspan=1 colspan=1>5.7×</td></tr><tr><td rowspan=1 colspan=1>condnet</td><td rowspan=1 colspan=1>0.497</td><td rowspan=1 colspan=1>1/16</td><td rowspan=1 colspan=1>10,10</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>2.0s(10.4s)</td><td rowspan=1 colspan=1>5.3×</td></tr><tr><td rowspan=1 colspan=1>bdNN</td><td rowspan=1 colspan=1>0.629</td><td rowspan=1 colspan=1>0.17</td><td rowspan=1 colspan=1>10,10</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>1.93s(10.3s)</td><td rowspan=1 colspan=1>5.3×</td></tr><tr><td rowspan=1 colspan=1>bdNN</td><td rowspan=1 colspan=1>0.590</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>10,10</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>2.8s(10.3s)</td><td rowspan=1 colspan=1>3.5×</td></tr><tr><td rowspan=1 colspan=1>NN</td><td rowspan=1 colspan=1>0.560</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>64,64</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1.23s</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>NN</td><td rowspan=1 colspan=1>0.546</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>128,128</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2.31s</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>NN</td><td rowspan=1 colspan=1>0.497</td><td rowspan=1 colspan=1>一</td><td rowspan=1 colspan=1>480,480</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>8.34s</td><td rowspan=1 colspan=1>=</td></tr></table>

Figure 2: CIFAR-10, condnet: our approach, NN: Neural Network without the conditional activations, bdNN, block dropout Neural Network using a uniform policy. ’speedup’ is how many times faster the forward pass is when using a specialized implementation (3.4). ’test time’ is the time required to do a full pass over the test dataset using the implementation, on a CPU, running on a single core; in parenthesis is the time without the optimization.

Next, we consider the performance of our model on the CIFAR-10 (Krizhevsky & Hinton, 2009) image dataset. A brief hyperparameter search was made, and a few of the best models are shown in figure 2. These results show that it is possible to achieve similar performance with our model (denoted condnet) as with a normal neural network (denoted NN), yet using sensibly reduced computation time. A few things are worth noting; we can set τ to be lower than 1 over the number of blocks, since the model learns a policy that is actually not as sparse as τ , mostly because REINFORCE pulls the policy towards higher probabilities on average. For example our best performing model has a target of 1/16 but learns policies that average an 18% sparsity rate (we used $\lambda _ { v } = \lambda _ { s } = 2 0$ , except for the first layer $\lambda _ { v } = 4 0$ , we used $\lambda _ { L 2 } = 0 . 0 1$ , and the learning rates were 0.001 for the neural net, $1 0 ^ { - 5 }$ and $5 \times 1 0 ^ { - 4 }$ for the first and second policy layers respectively). The neural networks without conditional activations are trained with L2 regularization as well as regular unit-wise dropout.

We also train networks with the same architecture as our models, using blocks, but with a uniform policy (as in original dropout) instead of a learned conditional one. This model (denoted bdNN) does not perform as well as our model, showing that the dropout noise by itself is not sufficient, and that learning a policy is required to fully take benefit of this architecture.

![](images/6de1e4498d67c23b727b9446749e22a53aba860b7b08b42d5e1caabfdbcb4337.jpg)

Figure 3: SVHN, each point is an experiment. The x axis is the time required to do a full pass over the valid dataset (log scale, lower is better). Note that we plot the full hyperparameter exploration results, which is why condnet results are so varied.
<table><tr><td rowspan=1 colspan=1>model</td><td rowspan=1 colspan=1>test error</td><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>#blocks</td><td rowspan=1 colspan=1>block size</td><td rowspan=1 colspan=1>test time</td><td rowspan=1 colspan=1>speedup</td></tr><tr><td rowspan=1 colspan=1>condnet</td><td rowspan=1 colspan=1>0.183</td><td rowspan=1 colspan=1>1/11</td><td rowspan=1 colspan=1>13,8</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>1.5s(2.2s)</td><td rowspan=1 colspan=1>1.4×</td></tr><tr><td rowspan=1 colspan=1>condnet</td><td rowspan=1 colspan=1>0.139</td><td rowspan=1 colspan=1>1/25,1/7</td><td rowspan=1 colspan=1>27,7</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>2.8s (4.3s)</td><td rowspan=1 colspan=1>1.6×</td></tr><tr><td rowspan=1 colspan=1>condnet</td><td rowspan=1 colspan=1>0.073</td><td rowspan=1 colspan=1>1/22</td><td rowspan=1 colspan=1>25,22</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>10.2s(14.1s)</td><td rowspan=1 colspan=1>1.4×</td></tr><tr><td rowspan=1 colspan=1>NN</td><td rowspan=1 colspan=1>0.116</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>288,928</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>4.8s</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>NN</td><td rowspan=1 colspan=1>0.100</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>800,736</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>10.7s</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>NN</td><td rowspan=1 colspan=1>0.091</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1280,1056</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>16.8s</td><td rowspan=1 colspan=1>一</td></tr></table>

Figure 4: SVHN results (see fig 2)

Finally we tested our model on the Street View House Numbers (SVHN) (Netzer et al., 2011) dataset, which also yielded encouraging results (figure 3). As we restrain the capacity of the models (by increasing sparsity or decreasing number of units), condnets retain acceptable performance with low run times, while plain neural networks suffer highly (their performance dramatically decreases with lower run times).

The best condnet model has a test error of 7.3%, and runs a validation epoch in 10s (14s without speed optimization), while the best standard neural network model has a test error of 9.1%, and runs in 16s. Note that the variance in the SVHN results (figure 3) is due to the mostly random hyperparameter exploration, where block size, number of blocks, τ , λ , λ , as well of learning rates are randomly picked. The normal neural network results were obtained by varying the number of hidden units of a 2-hidden-layer model.

For all three datasets and all condnet models used, the required training time was higher, but still reasonable. On average experiments took 1.5 to 3 times longer (wall time).

## 4.3 EFFECTS OF REGULARIZATION

The added regularization proposed in section 3.2 seems to play an important role in our ability to train the conditional model. When using only the prediction score, we observed that the algorithm tried to compensate by recruiting more units and saturating their participation probability, or even failed by dismissing very early what were probably considered bad units.

In practice, the variance regularization term $L _ { v }$ only slightly affects the prediction accuracy and learned policies of models, but we have observed that it significantly speeds up the training process, probably by encouraging policies to become less uniform earlier in the learning process. This can be seen in figure 5b, where we train a model with different values of $\lambda _ { v }$ . When $\lambda _ { v }$ is increased, the first few epochs have a much lower error rate.

![](images/ebec3994eabb468d1cfda5137bdebf6111eef27f6d2dbe6ad382ec542aca927f.jpg)  
(a)

![](images/21c2aa668484a68b240ae8505781326667ba52ad113a67a49939edb2bdb87d05.jpg)  
(b)  
Figure 5: CIFAR-10, (a) each pair of circle and triangle is an experiment made with a given lambda (x axis), resulting in a model with a certain error and running time (y axes). As $\lambda _ { s }$ increases the running time decreases, but so does performance. (b) The same model is being trained with different values of $\lambda _ { v } .$ . Redder means lower, greener means higher.

It is possible to tune some hyperparameters to affect the point at which the trade-off between computation speed and performance lies, thus one could push the error downwards at the expense of also more computation time. This is suggested by figure 5a, which shows the effect of one such hyperparameter $( \lambda _ { s } )$ on both running times and performance for the CIFAR dataset. Here it seems that $\lambda \sim [ 3 0 0 , 4 0 0 ]$ offers the best trade-off, yet other values could be selected, depending on the specific requirements of an application.

## 5 RELATED WORK

Ba & Frey (2013) proposed a learning algorithm called standout for computing an input-dependent dropout distribution at every node. As opposed to our layer-wise method, standout computes a oneshot dropout mask over the entire network, conditioned on the input to the network. Additionally, masks are unit-wise, while our approach uses masks that span blocks of units. Bengio et al. (2013) introduced Stochastic Times Smooth neurons as gaters for conditional computation within a deep neural network. STS neurons are highly non-linear and non-differentiable functions learned using estimators of the gradient obtained through REINFORCE. They allow a sparse binary gater to be computed as a function of the input, thus reducing computations in the then sparse activation of hidden layers.

Stollenga et al. (2014) recently proposed to learn a sequential decision process over the filters of a convolutional neural network (CNN). As in our work, a direct policy search method was chosen to find the parameters of a control policy. Their problem formulation differs from ours mainly in the notion of decision “stage”. In their model, an input is first fed through a network, the activations are computed during forward propagation then they are served to the next decision stage. The goal of the policy is to select relevant filters from the previous stage so as to improve the decision accuracy on the current example. They also use a gradient-free evolutionary algorithm, in contrast to our gradient-based method.

The Deep Sequential Neural Network (DSNN) model of Denoyer & Gallinari (2014) is possibly closest to our approach. The control process is carried over the layers of the network and uses the output of the previous layer to compute actions. The REINFORCE algorithm is used to train the policy with the reward/cost function being defined as the loss at the output in the base network. DSNN considers the general problem of choosing between between different type of mappings (weights) in a composition of functions. However, they test their model on datasets in which different modes are proeminent, making it easy for a policy to distinguish between them.

Another point of comparison for our work are attention models (Mnih et al., 2014; Gregor et al., 2015; Xu et al., 2015). These models typically learn a policy, or a form of policy, that allows them to selectively attend to parts of their input sequentially, in a visual 2D environnement. Both attention and our approach aim to reduce computation times. While attention aims to perform dense computations on subsets of the inputs, our approach aims to be more general, since the policy focuses on subsets of the whole computation (it is in a sense more distributed). It should also be possible to combine these approaches, since one acts on the input space and the other acts on the representation space, altough the resulting policies would be much more complex, and not necessarily easily trainable.

## 6 CONCLUSION

This paper presents a method for tackling the problem of conditional computation in deep networks by using reinforcement learning. We propose a type of parameterized conditional computation policy that maps the activations of a layer to a Bernoulli mask. The reinforcement signal accounts for the loss function of the network in its prediction task, while the policy network itself is regularized to account for the desire to have sparse computations. The REINFORCE algorithm is used to train policies to optimize this cost. Our experiments show that it is possible to train such models at the same levels of accuracy as their standard counterparts. Additionally, it seems possible to execute these similarly accurate models faster due to their sparsity. Furthermore, the model has a few simple parameters that allow to control the trade-off between accuracy and running time.

The use of REINFORCE could be replaced by a more efficient policy search algorithm, and also, perhaps, one in which rewards (or costs) as described above are replaced by a more sequential variant. The more direct use of computation time as a cost may prove beneficial. In general, we consider conditional computation to be an area in which reinforcement learning could be very useful, and deserves further study.

All the running times reported in the Experiments section are for a CPU, running on a single core. The motivation for this is to explore deployment of large neural networks on cheap, low-power, single core CPUs such as phones, while retaining high model capacity and expressiveness. While the results presented here show that our model for conditional computation can achieve speedups in this context, it is worth also investigating adaptation of these sparse computation models in multi core/GPU architectures; this is the subject of ongoing work.

## ACKNOWLEDGEMENTS

The authors gratefully acknowledge financial support for this work by the Samsung Advanced Institute of Technology (SAIT), the Natural Sciences and Engineering Research Council of Canada (NSERC) and the Fonds de recherche du Quebec - Nature et Technologies (FQRNT).´

## REFERENCES

Ba, Jimmy and Frey, Brendan. Adaptive dropout for training deep neural networks. In Burges, C.J.C., Bottou, L., Welling, M., Ghahramani, Z., and Weinberger, K.Q. (eds.), Advances in Neural Information Processing Systems 26, pp. 3084–3092. Curran Associates, Inc., 2013. URL http://papers.nips.cc/paper/5032-adaptive-dropout-fortraining-deep-neural-networks.pdf.

Bengio, Y., Simard, P., and Frasconi, P. Learning long-term dependencies with gradient descent is difficult. IEEE Transactions on Neural Nets, pp. 157–166, 1994.

Bengio, Yoshua, Leonard, Nicholas, and Courville, Aaron. Estimating or propagating gradients´ through stochastic neurons for conditional computation. arXiv preprint arXiv:1308.3432, 2013.

Bergstra, James, Breuleux, Olivier, Bastien, Fred´ eric, Lamblin, Pascal, Pascanu, Razvan, Des-´ jardins, Guillaume, Turian, Joseph, Warde-Farley, David, and Bengio, Yoshua. Theano: a CPU

and GPU math expression compiler. In Proceedings of the Python for Scientific Computing Conference (SciPy), June 2010. Oral Presentation.

Bishop, Christopher M. Pattern Recognition and Machine Learning (Information Science and Statistics). Springer-Verlag New York, Inc., Secaucus, NJ, USA, 2006. ISBN 0387310738.

Davis, Andrew and Arel, Itamar. Low-rank approximations for conditional feedforward computation in deep neural networks. arXiv preprint arXiv:1312.4461, 2013.

Deisenroth, Marc Peter, Neumann, Gerhard, and Peters, Jan. A survey on policy search for robotics. Foundations and Trends in Robotics, 2(1-2):1–142, 2013. doi: 10.1561/2300000021. URL http://dx.doi.org/10.1561/2300000021.

Denoyer, Ludovic and Gallinari, Patrick. Deep sequential neural network. CoRR, abs/1410.0510, 2014. URL http://arxiv.org/abs/1410.0510.

Glorot, Xavier and Bengio, Yoshua. Understanding the difficulty of training deep feedforward neural networks. In Proceedings of the Thirteenth International Conference on Artificial Intelligence and Statistics, AISTATS 2010, Chia Laguna Resort, Sardinia, Italy, May 13-15, 2010, pp. 249–256, 2010. URL http://www.jmlr.org/proceedings/papers/v9/glorot10a.html.

Gregor, Karol, Danihelka, Ivo, Graves, Alex, and Wierstra, Daan. Draw: A recurrent neural network for image generation. arXiv preprint arXiv:1502.04623, 2015.

He, Kaiming, Zhang, Xiangyu, Ren, Shaoqing, and Sun, Jian. Delving deep into rectifiers: Surpassing human-level performance on imagenet classification. arXiv preprint arXiv:1502.01852, 2015.

Hinton, Geoffrey E., Srivastava, Nitish, Krizhevsky, Alex, Sutskever, Ilya, and Salakhutdinov, Ruslan. Improving neural networks by preventing co-adaptation of feature detectors. CoRR, abs/1207.0580, 2012. URL http://arxiv.org/abs/1207.0580.

Hochreiter, S. Untersuchungen zu dynamischen neuronalen Netzen. Diploma thesis, T.U. Munich,¨ 1991.

Krizhevsky, Alex and Hinton, Geoffrey. Learning multiple layers of features from tiny images, 2009.

Martens, James. Deep learning via hessian-free optimization. In Proceedings of the 27th International Conference on Machine Learning (ICML-10), June 21-24, 2010, Haifa, Israel, pp. 735– 742, 2010. URL http://www.icml2010.org/papers/458.pdf.

Mnih, Volodymyr, Heess, Nicolas, Graves, Alex, and kavukcuoglu, koray. Recurrent models of visual attention. In Ghahramani, Z., Welling, M., Cortes, C., Lawrence, N.D., and Weinberger, K.Q. (eds.), Advances in Neural Information Processing Systems 27, pp. 2204–2212. Curran Associates, Inc., 2014. URL http://papers.nips.cc/paper/5542-recurrent-modelsof-visual-attention.pdf.

Netzer, Yuval, Wang, Tao, Coates, Adam, Bissacco, Alessandro, Wu, Bo, and Ng, Andrew Y. Reading digits in natural images with unsupervised feature learning. In NIPS workshop on deep learning and unsupervised feature learning, volume 2011, pp. 5. Granada, Spain, 2011.

Pearlmutter, Barak A. Fast exact multiplication by the hessian. Neural Comput., 6(1):147– 160, January 1994. ISSN 0899-7667. doi: 10.1162/neco.1994.6.1.147. URL http: //dx.doi.org/10.1162/neco.1994.6.1.147.

Puterman, Martin L. Markov Decision Processes: Discrete Stochastic Dynamic Programming. John Wiley & Sons, Inc., New York, NY, USA, 1st edition, 1994. ISBN 0471619779.

Rumelhart, David E, Hinton, Geoffrey E, and Williams, Ronald J. Learning representations by back-propagating errors. Cognitive modeling, 5, 1988.

Silver, David, Lever, Guy, Heess, Nicolas, Degris, Thomas, Wierstra, Daan, and Riedmiller, Martin. Deterministic policy gradient algorithms. In Proceedings of the 31th International Conference on Machine Learning, ICML 2014, Beijing, China, 21-26 June 2014, pp. 387–395, 2014. URL http://jmlr.org/proceedings/papers/v32/silver14.html.

Stollenga, Marijn F, Masci, Jonathan, Gomez, Faustino, and Schmidhuber, Jurgen. Deep ¨ networks with internal selective attention through feedback connections. In Ghahramani, Z., Welling, M., Cortes, C., Lawrence, N.D., and Weinberger, K.Q. (eds.), Advances in Neural Information Processing Systems 27, pp. 3545–3553. Curran Associates, Inc., 2014. URL http://papers.nips.cc/paper/5276-deep-networks-withinternal-selective-attention-through-feedback-connections.pdf.

Williams, Ronald J. Simple statistical gradient-following algorithms for connectionist reinforcement learning. Machine Learning, 8(3-4):229–256, 1992. ISSN 0885-6125. doi: 10.1007/BF00992696. URL http://dx.doi.org/10.1007/BF00992696.

Xu, Kelvin, Ba, Jimmy, Kiros, Ryan, Courville, Aaron, Salakhutdinov, Ruslan, Zemel, Richard, and Bengio, Yoshua. Show, attend and tell: Neural image caption generation with visual attention. arXiv preprint arXiv:1502.03044, 2015.

## A ALGORITHM

The forward pass in our model is done as described in the algorithm below (1), both at train time and test time.

input: x   
1 $\mathbf { h } _ { 0 }  \mathbf { x }$   
2 $\mathbf { u } _ { 0 } \gets \mathbf { 1 }$ // the input mask is ones   
3 for each hidden layer $l \in { 1 , . . . , L }$ do   
4 $\mathbf { p } _ { l } \gets \mathrm { s i g m } ( \mathbf { Z } ^ { ( l ) } \mathbf { h } _ { l - 1 } + \mathbf { d } ^ { ( l ) } ) = \pi _ { l } \big ( \mathbf { u } _ { l } | \mathbf { s } _ { l } = \mathbf { h } _ { l - 1 } \big )$   
5 u<sub>l</sub> ∼ Ber(p<sub>l</sub>) ; // sample Bernoulli from probablities $p _ { l }$   
6 if blocksize > 1 then   
7 extend u<sub>l</sub> by repeating each value blocksize times   
8 end   
// this operation can be performed efficiently as described in section 3.4:   
9 $\mathbf { h } _ { l }  f ( \mathbf { W } ^ { ( l ) } ( \mathbf { h } _ { l - 1 } \otimes \mathbf { u } _ { l - 1 } ) + \mathbf { b } ^ { ( l ) } ) \otimes \mathbf { u } _ { l }$   
10 end

## Algorithm 1: Single-input forward pass

This algorithm can easily be extended to the minibatch setting by replacing vector operations by matrix operations. Note that in the case of classification, the last layer is a softmax layer and is not multiplied by a mask.

input: x   
1 yˆ = forward(x) ; // given the output of the forward pass   
2 c ← C(x) = − log P (yˆ|x)   
3 $\mathcal { L }  c + \lambda _ { s } ( L _ { b } + L _ { e } ) + \lambda _ { v } ( L _ { v } ) + \lambda _ { L 2 } \| \Theta _ { N N } \| ^ { 2 } + \lambda _ { L 2 } \| \Theta _ { \pi } \| ^ { 2 }$ ; // as in sections 3.2 and 3.3   
// update the neural network weights:   
4 $\Theta _ { N N } \gets \Theta _ { N N } - \alpha \nabla _ { \Theta _ { N N } } \mathcal { L }$   
// update the policy weights:   
5 for each hidden layer $l \bar { \in } 1 , . . . , L$ do   
$\begin{array} { r l } { \mathbf { \delta 6 } } & { | \quad \theta _ { l } \gets \theta _ { l } - \alpha _ { \pi } \underbrace { c \nabla _ { \theta _ { l } } \log \mathbf { p } _ { l } } _ { \mathrm { R E I N F O R C E } } - \alpha \nabla _ { \theta _ { l } } \mathcal { L } ; } \end{array}$ // where $\mathbf { p } _ { l }$ is computed as in algorithm 1   
7 end

## Algorithm 2: Single-input backward pass

Note that in line $^ { 4 , }$ some gradients are zeroes, for example the gradient of the L2 regularisation of $\Theta _ { \pi }$ with respect to $\Theta _ { N N }$ is zero. Similarly in line 5, the gradient of c with respect to $\Theta _ { \pi }$ is zero, which is why we have to use REINFORCE to approximate a gradient in the direction that minimizes c.

This algorithm can be extended to the minibatch setting efficiently by replacing the gradient computations in line 7 with the use of the so called R-op, as described in section 3.1, and other computations as is usually done in the minibatch setting with matrix operations.

## B REINFORCE

REINFORCE (Williams, 1992), also known as the likelihood-ratio method, is a policy search algorithm. It aims to use gradient methods to improve a given parameterized policy.

In reinforcement learning, a sequence of state-action-reward tuples is described as a trajectory $\tau$ The objective function of a parameterized policy $\pi _ { \theta }$ for the cumulative return of a trajectory τ is described as:

$$
J ( \theta ) = \mathbb { E } _ { \tau } ^ { \pi _ { \theta } } \left\{ \sum _ { t = 1 } ^ { T } r ( S _ { t } , A _ { t } | S _ { 0 } = s _ { 0 } ) \right\}
$$

where $s _ { 0 }$ is the initial state of the trajectory. Let $R ( \tau )$ denote the return for trajectory τ . The gradient of the objective with respect to the parameters of the policy is:

$$
\begin{array} { r l } & { \nabla _ { \theta } J ( \theta ) = \nabla _ { \theta } \mathbb { E } _ { \tau } ^ { \pi _ { \theta } } \{ R ( \tau ) \} } \\ & { \quad \quad \quad = \nabla _ { \theta } \int _ { \tau } \mathbb { P } \{ \tau | \theta \} R ( \tau ) d \tau } \\ & { \quad \quad \quad = \displaystyle \int _ { \tau } \nabla _ { \theta } \left[ \mathbb { P } \{ \tau | \theta \} R ( \tau ) \right] d \tau } \end{array}\tag{8}
$$

Note that the interchange in (8) is only valid under some assumptions (see Silver et al. (2014)).

$$
\begin{array} { l } { \displaystyle \nabla _ { \theta } J ( \theta ) = \int _ { \tau } \nabla _ { \theta } \left[ \mathbb { P } \{ \tau | \theta \} R ( \tau ) \right] d \tau } \\ { \displaystyle = \int _ { \tau } \left[ R ( \tau ) \nabla _ { \theta } \mathbb { P } \{ \tau | \theta \} + \nabla _ { \theta } R ( \tau ) \mathbb { P } \{ \tau | \theta \} \right] d \tau } \\ { \displaystyle = \int _ { \tau } \left[ \frac { R ( \tau ) } { \mathbb { P } \{ \tau | \theta \} } \nabla _ { \theta } \mathbb { P } \{ \tau | \theta \} + \nabla _ { \theta } R ( \tau ) \right] \mathbb { P } \{ \tau | \theta \} d \tau } \\ { \displaystyle = \mathbb { E } _ { \tau } ^ { \pi _ { \theta } } \left\{ R ( \tau ) \nabla _ { \theta } \log \mathbb { P } \{ \tau | \theta \} + \nabla _ { \theta } R ( \tau ) \right\} } \end{array}\tag{9}
$$

(10)

The product rule of derivatives is used in (9), and the derivative of a log in (10). Since $R ( \tau )$ does not depend on θ directly, the gradient $\nabla _ { \boldsymbol { \theta } } R ( \tau )$ is zero. We end up with this gradient:

$$
\nabla _ { \boldsymbol { \theta } } J ( \boldsymbol { \theta } ) = \mathbb { E } _ { \tau } ^ { \pi _ { \boldsymbol { \theta } } } \left\{ R ( \tau ) \nabla _ { \boldsymbol { \theta } } \log \mathbb { P } \{ \tau | \boldsymbol { \theta } \} \right\}\tag{11}
$$

Without knowing the transition probabilities, we cannot compute the probability of our trajectories $\mathbb { P } \{ \tau | \theta \}$ , or their gradient. Fortunately we are in a MDP setting, and we can make use of the Markov property of the trajectories to compute the gradient:

$$
\begin{array} { l } { { \nabla _ { \theta } \log \mathbb { P } \{ \tau | \theta \} = \nabla _ { \theta } \log \left[ p ( s _ { 0 } ) \displaystyle \prod _ { t = 1 } ^ { T } \mathbb { P } \{ s _ { t + 1 } | s _ { t } , a _ { t } \} \pi _ { \theta } ( a _ { t } | s _ { t } ) \right] } } \\ { { \displaystyle \qquad = \nabla _ { \theta } \log p ( s _ { 0 } ) + \displaystyle \sum _ { t = 1 } ^ { T } \nabla _ { \theta } \log \mathbb { P } \{ s _ { t + 1 } | s _ { t } , a _ { t } \} + \nabla _ { \theta } \log \pi _ { \theta } ( a _ { t } | s _ { t } ) } } \\ { { \displaystyle \qquad = \sum _ { t = 1 } ^ { T } \nabla _ { \theta } \log \pi _ { \theta } ( a _ { t } | s _ { t } ) } } \end{array}\tag{12}
$$

In (12), $p ( s _ { 0 } )$ does not depend on $\theta ,$ so the gradient is zero. Similarly, $\mathbb { P } \{ s _ { t + 1 } | s _ { t } , a _ { t } \}$ does not depend on θ (not directly at least), so the gradient is also zero. We end up with the gradient of the log policy, which is easy to compute.

In our particular case, the trajectories only have a single step and the reward of the trajectory is the neural network cost $C ( \mathbf { x } )$ , thus the summation dissapears and the gradient found in (2) is found by taking the log of the probability of our Bernoulli sample:

$$
\begin{array} { l } { { \displaystyle \nabla _ { \theta _ { l } } C ( { \bf x } ) = \mathbb { E } \left\{ C ( { \bf x } ) \nabla _ { \theta _ { l } } \log \pi _ { \theta _ { l } } ( { \bf u } | { \bf s } ) \right\} } \ ~ } \\ { { \displaystyle ~ = \mathbb { E } \left\{ C ( { \bf x } ) \nabla _ { \theta _ { l } } \log \prod _ { i = 1 } ^ { k } \sigma _ { i } ^ { u _ { i } } ( 1 - \sigma _ { i } ) ^ { ( 1 - u _ { i } ) } \right\} } \ ~ } \\ { { \displaystyle ~ = \mathbb { E } \left\{ C ( { \bf x } ) \nabla _ { \theta _ { l } } \sum _ { i = 1 } ^ { k } \log \left[ \sigma _ { i } u _ { i } + ( 1 - \sigma _ { i } ) ( 1 - u _ { i } ) \right] \right\} } } \end{array}
$$