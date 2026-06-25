# DEEP COMPRESSION: COMPRESSING DEEP NEURAL NETWORKS WITH PRUNING, TRAINED QUANTIZATION AND HUFFMAN CODING

Song Han   
Stanford University, Stanford, CA 94305, USA   
songhan@stanford.edu

Huizi Mao Tsinghua University, Beijing, 100084, China mhz12@mails.tsinghua.edu.cn

William J. Dally   
Stanford University, Stanford, CA 94305, USA   
NVIDIA, Santa Clara, CA 95050, USA   
dally@stanford.edu

## ABSTRACT

Neural networks are both computationally intensive and memory intensive, making them difficult to deploy on embedded systems with limited hardware resources. To address this limitation, we introduce “deep compression”, a three stage pipeline: pruning, trained quantization and Huffman coding, that work together to reduce the storage requirement of neural networks by 35× to 49× without affecting their accuracy. Our method first prunes the network by learning only the important connections. Next, we quantize the weights to enforce weight sharing, finally, we apply Huffman coding. After the first two steps we retrain the network to fine tune the remaining connections and the quantized centroids. Pruning, reduces the number of connections by 9× to 13×; Quantization then reduces the number of bits that represent each connection from 32 to 5. On the ImageNet dataset, our method reduced the storage required by AlexNet by 35×, from 240MB to 6.9MB, without loss of accuracy. Our method reduced the size of VGG-16 by 49× from 552MB to 11.3MB, again with no loss of accuracy. This allows fitting the model into on-chip SRAM cache rather than off-chip DRAM memory. Our compression method also facilitates the use of complex neural networks in mobile applications where application size and download bandwidth are constrained. Benchmarked on CPU, GPU and mobile GPU, compressed network has 3× to 4× layerwise speedup and 3× to 7× better energy efficiency.

## 1 INTRODUCTION

Deep neural networks have evolved to the state-of-the-art technique for computer vision tasks (Krizhevsky et al., 2012)(Simonyan & Zisserman, 2014). Though these neural networks are very powerful, the large number of weights consumes considerable storage and memory bandwidth. For example, the AlexNet Caffemodel is over 200MB, and the VGG-16 Caffemodel is over 500MB (BVLC). This makes it difficult to deploy deep neural networks on mobile system.

First, for many mobile-first companies such as Baidu and Facebook, various apps are updated via different app stores, and they are very sensitive to the size of the binary files. For example, App Store has the restriction “apps above 100 MB will not download until you connect to Wi-Fi”. As a result, a feature that increases the binary size by 100MB will receive much more scrutiny than one that increases it by 10MB. Although having deep neural networks running on mobile has many great features such as better privacy, less network bandwidth and real time processing, the large storage overhead prevents deep neural networks from being incorporated into mobile apps.

![](images/fcdc7888682b2a1bec7854151201efa1852a5993fdb278fd103ae0240b75b5c9.jpg)  
Figure 1: The three stage compression pipeline: pruning, quantization and Huffman coding. Pruning reduces the number of weights by 10×, while quantization further improves the compression rate: between 27× and 31×. Huffman coding gives more compression: between 35× and 49×. The compression rate already included the meta-data for sparse representation. The compression scheme doesn’t incur any accuracy loss.

The second issue is energy consumption. Running large neural networks require a lot of memory bandwidth to fetch the weights and a lot of computation to do dot products— which in turn consumes considerable energy. Mobile devices are battery constrained, making power hungry applications such as deep neural networks hard to deploy.

Our goal is to reduce the storage and energy required to run inference on such large networks so they can be deployed on mobile devices. To achieve this goal, we present “deep compression”: a threestage pipeline (Figure 1) to reduce the storage required by neural network in a manner that preserves the original accuracy. First, we prune the networking by removing the redundant connections, keeping only the most informative connections. Next, the weights are quantized so that multiple connections share the same weight, thus only the codebook (effective weights) and the indices need to be stored. Finally, we apply Huffman coding to take advantage of the biased distribution of effective weights.

## 2 NETWORK PRUNING

Network pruning has been widely studied to compress CNN models. In early work, network pruning proved to be a valid way to reduce the network complexity and over-fitting (LeCun et al., 1989; Hanson & Pratt, 1989; Hassibi et al., 1993; Strom, 1997). Recently Han et al. (2015) pruned state-¨ of-the-art CNN models with no loss of accuracy. We build on top of that approach. As shown on the left side of Figure 1, we start by learning the connectivity via normal network training. Next, we prune the small-weight connections: all connections with weights below a threshold are removed from the network. Finally, we retrain the network to learn the final weights for the remaining sparse connections. Pruning reduced the number of parameters by 9× and 13× for AlexNet and VGG-16 model.

![](images/4c2b0cf65df8d361bb62d814e299cf64a237a3c1b9da0cf63f11ac99a6bcdaf6.jpg)  
Figure 2: Representing the matrix sparsity with relative index. Padding filler zero to prevent overflow.

![](images/06f3a7bf70d218d46cc53781f0c6e42fc7ce174ffbc79c2b45206bee4b210790.jpg)  
Figure 3: Weight sharing by scalar quantization (top) and centroids fine-tuning (bottom).

We store the sparse structure that results from pruning using compressed sparse row (CSR) or compressed sparse column (CSC) format, which requires 2a + n + 1 numbers, where a is the number of non-zero elements and n is the number of rows or columns.

To compress further, we store the index difference instead of the absolute position, and encode this difference in 8 bits for conv layer and 5 bits for fc layer. When we need an index difference larger than the bound, we the zero padding solution shown in Figure 2: in case when the difference exceeds 8, the largest 3-bit (as an example) unsigned number, we add a filler zero.

## 3 TRAINED QUANTIZATION AND WEIGHT SHARING

Network quantization and weight sharing further compresses the pruned network by reducing the number of bits required to represent each weight. We limit the number of effective weights we need to store by having multiple connections share the same weight, and then fine-tune those shared weights.

Weight sharing is illustrated in Figure 3. Suppose we have a layer that has 4 input neurons and 4 output neurons, the weight is a 4 × 4 matrix. On the top left is the 4 × 4 weight matrix, and on the bottom left is the 4 × 4 gradient matrix. The weights are quantized to 4 bins (denoted with 4 colors), all the weights in the same bin share the same value, thus for each weight, we then need to store only a small index into a table of shared weights. During update, all the gradients are grouped by the color and summed together, multiplied by the learning rate and subtracted from the shared centroids from last iteration. For pruned AlexNet, we are able to quantize to 8-bits (256 shared weights) for each CONV layers, and 5-bits (32 shared weights) for each FC layer without any loss of accuracy.

To calculate the compression rate, given k clusters, we only need $l o g _ { 2 } ( k )$ bits to encode the index. In general, for a network with n connections and each connection is represented with b bits, constraining the connections to have only k shared weights will result in a compression rate of:

$$
r = \frac { n b } { n l o g _ { 2 } ( k ) + k b }\tag{1}
$$

For example, Figure 3 shows the weights of a single layer neural network with four input units and four output units. There are 4 × 4 = 16 weights originally but there are only 4 shared weights: similar weights are grouped together to share the same value. Originally we need to store 16 weights each

![](images/f97eb6dff6327ee9e185bdddcb3aa5c8620622948bfbe1f564a1b8f60534c297.jpg)

![](images/82f39ef340faac3428de10c4739e46b974c8be1d944c17b4047f018489d8dedc.jpg)  
Figure 4: Left: Three different methods for centroids initialization. Right: Distribution of weight (blue) and distribution of codebook before (green cross) and after fine-tuning (red dot).

has 32 bits, now we need to store only 4 effective weights (blue, green, red and orange), each has 32 bits, together with 16 2-bit indices giving a compression rate of $\bar { 1 6 } * 3 2 / ( 4 * 3 2 + \bar { 2 } * 1 6 ) = 3 . 2$

## 3.1 WEIGHT SHARING

We use k-means clustering to identify the shared weights for each layer of a trained network, so that all the weights that fall into the same cluster will share the same weight. Weights are not shared across layers. We partition n original weights $W = \{ w _ { 1 } , w _ { 2 } , . . . , w _ { n } \}$ into k clusters $C = \{ c _ { 1 } , c _ { 2 } , . . . , c _ { k } \}$ $n \gg k ,$ , so as to minimize the within-cluster sum of squares (WCSS):

$$
\underset { C } { \operatorname { a r g m i n } } \sum _ { i = 1 } ^ { k } \sum _ { w \in c _ { i } } \left| w - c _ { i } \right| ^ { 2 }\tag{2}
$$

Different from HashNet (Chen et al., 2015) where weight sharing is determined by a hash function before the networks sees any training data, our method determines weight sharing after a network is fully trained, so that the shared weights approximate the original network.

## 3.2 INITIALIZATION OF SHARED WEIGHTS

Forgy (random) initialization randomly chooses k observations from the data set and uses these as the initial centroids. The initialized centroids are shown in yellow. Since there are two peaks in the bimodal distribution, Forgy method tend to concentrate around those two peaks.

Density-based initialization linearly spaces the CDF of the weights in the y-axis, then finds the horizontal intersection with the CDF, and finally finds the vertical intersection on the x-axis, which becomes a centroid, as shown in blue dots. This method makes the centroids denser around the two peaks, but more scatted than the Forgy method.

Linear initialization linearly spaces the centroids between the [min, max] of the original weights. This initialization method is invariant to the distribution of the weights and is the most scattered compared with the former two methods.

Larger weights play a more important role than smaller weights (Han et al., 2015), but there are fewer of these large weights. Thus for both Forgy initialization and density-based initialization, very few centroids have large absolute value which results in poor representation of these few large weights. Linear initialization does not suffer from this problem. The experiment section compares the accuracy of different initialization methods after clustering and fine-tuning, showing that linear initialization works best.

![](images/ad52e2d75738681b417189c36e69b2d45a5eebc60a193f777623a98d5a1803ac.jpg)

![](images/038988fec1fa4ef1c9a195b91c654cb8ede5662da42095aac184d353ab63d737.jpg)  
Figure 5: Distribution for weight (Left) and index (Right). The distribution is biased.

## 3.3 FEED-FORWARD AND BACK-PROPAGATION

The centroids of the one-dimensional k-means clustering are the shared weights. There is one level of indirection during feed forward phase and back-propagation phase looking up the weight table. An index into the shared weight table is stored for each connection. During back-propagation, the gradient for each shared weight is calculated and used to update the shared weight. This procedure is shown in Figure 3.

We denote the loss by ${ \mathcal { L } } ,$ the weight in the ith column and jth row by $W _ { i j }$ , the centroid index of element $W _ { i , j }$ by $I _ { i j } ,$ the kth centroid of the layer by $C _ { k }$ . By using the indicator function <sup>1</sup>(.), the gradient of the centroids is calculated as:

$$
\frac { \partial \mathcal { L } } { \partial C _ { k } } = \sum _ { i , j } \frac { \partial \mathcal { L } } { \partial W _ { i j } } \frac { \partial W _ { i j } } { \partial C _ { k } } = \sum _ { i , j } \frac { \partial \mathcal { L } } { \partial W _ { i j } } \mathbb { 1 } ( I _ { i j } = k )\tag{3}
$$

## 4 HUFFMAN CODING

A Huffman code is an optimal prefix code commonly used for lossless data compression(Van Leeuwen, 1976). It uses variable-length codewords to encode source symbols. The table is derived from the occurrence probability for each symbol. More common symbols are represented with fewer bits.

Figure 5 shows the probability distribution of quantized weights and the sparse matrix index of the last fully connected layer in AlexNet. Both distributions are biased: most of the quantized weights are distributed around the two peaks; the sparse matrix index difference are rarely above 20. Experiments show that Huffman coding these non-uniformly distributed values saves 20% − 30% of network storage.

## 5 EXPERIMENTS

## 5.1 LENET-300-100 AND LENET-5 ON MNIST

We first experimented on MNIST dataset with LeNet-300-100 and LeNet-5 network (LeCun et al., 1998). LeNet-300-100 is a fully connected network with two hidden layers, with 300 and 100 neurons each, which achieves 1.6% error rate on Mnist. LeNet-5 is a convolutional network that has two convolutional layers and two fully connected layers, which achieves 0.8% error rate on Mnist. Table 2 and table 3 show the statistics of the compression pipeline. The compression rate includes the overhead of the codebook and sparse indexes. Most of the saving comes from pruning and quantization (compressed 32×), while Huffman coding gives a marginal gain (compressed 40×)

Table 1: The compression pipeline can save 35× to 49× parameter storage with no loss of accuracy.
<table><tr><td>Network</td><td>Top-1 Error</td><td>Top-5 Error</td><td>Parameters</td><td>Compress Rate</td></tr><tr><td>LeNet-300-100 Ref LeNet-300-100 Compressed</td><td>1.64% 1.58%</td><td>一</td><td>1070 KB 27 KB</td><td>40×</td></tr><tr><td>LeNet-5 Ref LeNet-5 Compressed</td><td>0.80% 0.74%</td><td>一</td><td>1720 KB 44 KB</td><td>39×</td></tr><tr><td>AlexNet Ref AlexNet Compressed</td><td>42.78% 42.78%</td><td>19.73% 19.70%</td><td>240 MB 6.9 MB</td><td>35×</td></tr><tr><td>VGG-16 Ref VGG-16 Compressed</td><td>31.50% 31.17%</td><td>11.32% 10.91%</td><td>552 MB 11.3 MB</td><td>49×</td></tr></table>

Table 2: Compression statistics for LeNet-300-100. P: pruning, Q:quantization, H:Huffman coding.
<table><tr><td>Layer</td><td>#Weights</td><td>Weights% (P)</td><td>Weight bits (P+Q)</td><td>Weight bits (P+Q+H)</td><td>Index bits (P+Q)</td><td>Index bits</td><td>Compress rate</td><td>Compress rate</td></tr><tr><td>ip1</td><td>235K</td><td>8%</td><td>6</td><td>4.4</td><td>5</td><td>(P+Q+H) 3.7</td><td>(P+Q) 3.1%</td><td>(P+Q+H) 2.32%</td></tr><tr><td>ip2</td><td>30K</td><td>9%</td><td>6</td><td>4.4</td><td>5</td><td>4.3</td><td>3.8%</td><td>3.04%</td></tr><tr><td>ip3</td><td>1K</td><td>26%</td><td>6</td><td>4.3</td><td>5</td><td>3.2</td><td>15.7%</td><td>12.70%</td></tr><tr><td>Total</td><td>266K</td><td>8%(12×)</td><td>6</td><td>5.1</td><td>5</td><td>3.7</td><td>3.1% (32×)</td><td>2.49% (40×)</td></tr></table>

Table 3: Compression statistics for LeNet-5. P: pruning, Q:quantization, H:Huffman coding.
<table><tr><td>Layer</td><td>#Weights</td><td>Weights% (P)</td><td>Weight bits (P+Q)</td><td>Weight bits (P+Q+H)</td><td>Index bits (P+Q)</td><td>Index bits</td><td>Compress rate</td><td>Compress rate (P+Q+H)</td></tr><tr><td>conv1</td><td>0.5K</td><td>66%</td><td>8</td><td>7.2</td><td>5</td><td>(P+Q+H) 1.5</td><td>(P+Q) 78.5%</td><td>67.45%</td></tr><tr><td>conv2</td><td>25K</td><td>12%</td><td>8</td><td>7.2</td><td>5</td><td>3.9</td><td>6.0%</td><td>5.28%</td></tr><tr><td>ip1</td><td>400K</td><td>8%</td><td>5</td><td>4.5</td><td>5</td><td>4.5</td><td>2.7%</td><td>2.45%</td></tr><tr><td>ip2</td><td>5K</td><td>19%</td><td>5</td><td>5.2</td><td>5</td><td>3.7</td><td>6.9%</td><td>6.13%</td></tr><tr><td>Total</td><td>431K</td><td>8%(12×)</td><td>5.3</td><td>4.1</td><td>5</td><td>4.4</td><td>3.05% (33×)</td><td>2.55% (39×)</td></tr></table>

## 5.2 ALEXNET ON IMAGENET

We further examine the performance of Deep Compression on the ImageNet ILSVRC-2012 dataset, which has 1.2M training examples and 50k validation examples. We use the AlexNet Caffe model as the reference model, which has 61 million parameters and achieved a top-1 accuracy of 57.2% and a top-5 accuracy of 80.3%. Table 4 shows that AlexNet can be compressed to 2.88% of its original size without impacting accuracy. There are 256 shared weights in each CONV layer, which are encoded with 8 bits, and 32 shared weights in each FC layer, which are encoded with only 5 bits. The relative sparse index is encoded with 4 bits. Huffman coding compressed additional 22%, resulting in 35× compression in total.

## 5.3 VGG-16 ON IMAGENET

With promising results on AlexNet, we also looked at a larger, more recent network, VGG-16 (Simonyan & Zisserman, 2014), on the same ILSVRC-2012 dataset. VGG-16 has far more convolutional layers but still only three fully-connected layers. Following a similar methodology, we aggressively compressed both convolutional and fully-connected layers to realize a significant reduction in the number of effective weights, shown in Table5.

The VGG16 network as a whole has been compressed by 49×. Weights in the CONV layers are represented with 8 bits, and FC layers use 5 bits, which does not impact the accuracy. The two largest fully-connected layers can each be pruned to less than 1.6% of their original size. This reduction is critical for real time image processing, where there is little reuse of these layers across images (unlike batch processing). This is also critical for fast object detection algorithms where one CONV pass is used by many FC passes. The reduced layers will fit in an on-chip SRAM and have modest bandwidth requirements. Without the reduction, the bandwidth requirements are prohibitive.

Table 4: Compression statistics for AlexNet. P: pruning, Q: quantization, H:Huffman coding.
<table><tr><td>Layer</td><td>#Weights</td><td>Weights% (P)</td><td>Weight bits (P+Q)</td><td>Weight bits (P+Q+H)</td><td>Index bits (P+Q)</td><td>Index bits</td><td>Compress rate</td><td>Compress rate</td></tr><tr><td>conv1</td><td>35K</td><td>84%</td><td>8</td><td>6.3</td><td>4</td><td>(P+Q+H) 1.2</td><td>(P+Q) 32.6%</td><td>(P+Q+H) 20.53%</td></tr><tr><td>conv2</td><td>307K</td><td>38%</td><td>8</td><td>5.5</td><td>4</td><td>2.3</td><td>14.5%</td><td>9.43%</td></tr><tr><td>conv3</td><td>885K</td><td>35%</td><td>8</td><td>5.1</td><td>4</td><td>2.6</td><td>13.1%</td><td>8.44%</td></tr><tr><td>conv4</td><td>663K</td><td>37%</td><td>8</td><td>5.2</td><td>4</td><td>2.5</td><td>14.1%</td><td>9.11%</td></tr><tr><td>conv5</td><td>442K</td><td>37%</td><td>8</td><td>5.6</td><td>4</td><td>2.5</td><td>14.0%</td><td>9.43%</td></tr><tr><td>fc6</td><td>38M</td><td>9%</td><td>5</td><td>3.9</td><td>4</td><td>3.2</td><td>3.0%</td><td>2.39%</td></tr><tr><td>fc7</td><td>17M</td><td>9%</td><td>5</td><td>3.6</td><td>4</td><td>3.7</td><td>3.0%</td><td>2.46%</td></tr><tr><td>fc8</td><td>4M</td><td>25%</td><td>5</td><td>4</td><td>4</td><td>3.2</td><td>7.3%</td><td>5.85%</td></tr><tr><td>Total</td><td>61M</td><td>11%(9×)</td><td>5.4</td><td>4</td><td>4</td><td>3.2</td><td>3.7% (27×)</td><td>2.88% (35×)</td></tr></table>

Table 5: Compression statistics for VGG-16. P: pruning, Q:quantization, H:Huffman coding.
<table><tr><td>Layer</td><td>#Weights</td><td>Weights% (P)</td><td>Weigh bits (P+Q)</td><td>Weight bits (P+Q+H)</td><td>Index bits (P+Q)</td><td>Index bits (P+Q+H)</td><td>Compress rate</td><td>Compress rate (P+Q+H)</td></tr><tr><td>conv1_1</td><td>2K</td><td>58%</td><td>8</td><td>6.8</td><td>5</td><td>1.7</td><td>(P+Q) 40.0%</td><td>29.97%</td></tr><tr><td>conv1_2</td><td>37K</td><td>22%</td><td>8</td><td>6.5</td><td>5</td><td>2.6</td><td>9.8%</td><td>6.99%</td></tr><tr><td>conv2_1</td><td>74K</td><td>34%</td><td>8</td><td>5.6</td><td>5</td><td>2.4</td><td>14.3%</td><td>8.91%</td></tr><tr><td>conv2_2</td><td>148K</td><td>36%</td><td>8</td><td>5.9</td><td>5</td><td>2.3</td><td>14.7%</td><td>9.31%</td></tr><tr><td>conv3_1</td><td>295K</td><td>53%</td><td>8</td><td>4.8</td><td>5</td><td>1.8</td><td>21.7%</td><td>11.15%</td></tr><tr><td>conv3_2</td><td>590K</td><td>24%</td><td>8</td><td>4.6</td><td>5</td><td>2.9</td><td>9.7%</td><td>5.67%</td></tr><tr><td>conv3_3</td><td>590K</td><td>42%</td><td>8</td><td>4.6</td><td>5</td><td>2.2</td><td>17.0%</td><td>8.96%</td></tr><tr><td>conv4_1</td><td>1M</td><td>32%</td><td>8</td><td>4.6</td><td>5</td><td>2.6</td><td>13.1%</td><td>7.29%</td></tr><tr><td>conv4_2</td><td>2M</td><td>27%</td><td>8</td><td>4.2</td><td>5</td><td>2.9</td><td>10.9%</td><td>5.93%</td></tr><tr><td>conv4_3</td><td>2M 2M</td><td>34%</td><td>8</td><td>4.4</td><td>5</td><td>2.5</td><td>14.0%</td><td>7.47%</td></tr><tr><td>conv5_1</td><td>2M</td><td>35%</td><td>8</td><td>4.7</td><td>5</td><td>2.5</td><td>14.3%</td><td>8.00%</td></tr><tr><td>conv5_2</td><td>2M</td><td>29%</td><td>8</td><td>4.6</td><td>5</td><td>2.7</td><td>11.7%</td><td>6.52%</td></tr><tr><td>conv5_3</td><td>103M</td><td>36%</td><td>8</td><td>4.6</td><td>5</td><td>2.3</td><td>14.8%</td><td>7.79%</td></tr><tr><td>fc6</td><td>17M</td><td>4% 4%</td><td>5 5</td><td>3.6 4</td><td>5 5</td><td>3.5 4.3</td><td>1.6% 1.5%</td><td>1.10%</td></tr><tr><td>fc7</td><td>4M</td><td>23%</td><td>5</td><td>4</td><td>5</td><td>3.4</td><td>7.1%</td><td>1.25%</td></tr><tr><td>fc8</td><td>138M</td><td></td><td></td><td></td><td></td><td></td><td></td><td>5.24%</td></tr><tr><td>Total</td><td></td><td>7.5%(13×)</td><td>6.4</td><td>4.1</td><td>5</td><td>3.1</td><td>3.2% (31×)</td><td>2.05% (49×)</td></tr></table>

## 6 DISCUSSIONS

## 6.1 PRUNING AND QUANTIZATION WORKING TOGETHER

Figure 6 shows the accuracy at different compression rates for pruning and quantization together or individually. When working individually, as shown in the purple and yellow lines, accuracy of pruned network begins to drop significantly when compressed below 8% of its original size; accuracy of quantized network also begins to drop significantly when compressed below 8% of its original size. But when combined, as shown in the red line, the network can be compressed to 3% of original size with no loss of accuracy. On the far right side compared the result of SVD, which is inexpensive but has a poor compression rate.

The three plots in Figure 7 show how accuracy drops with fewer bits per connection for CONV layers (left), FC layers (middle) and all layers (right). Each plot reports both top-1 and top-5 accuracy. Dashed lines only applied quantization but without pruning; solid lines did both quantization and pruning. There is very little difference between the two. This shows that pruning works well with quantization.

Quantization works well on pruned network because unpruned AlexNet has 60 million weights to quantize, while pruned AlexNet has only 6.7 million weights to quantize. Given the same amount of centroids, the latter has less error.

![](images/6ad02cb9817deaf8c3553fddd604ed4252230241011ff3f4d553eb05cf954181.jpg)  
Model Size Ratio after Compression

Figure 6: Accuracy v.s. compression rate under different compression methods. Pruning and quantization works best when combined.  
![](images/b888deb832ab624172f5d94515d06a0ecae5f6844874d2d4c6619a03f674c58e.jpg)

![](images/0c6916f3c35543d41356a107df657ae73d60fbfa891f0ca5eda18930fbd6159c.jpg)

![](images/5fcf9f72a9cd1d780e4f0cf54c949344d1a20afafde22cb76b73aba134f51e9d.jpg)

Figure 7: Pruning doesn’t hurt quantization. Dashed: quantization on unpruned network. Solid: quantization on pruned network; Accuracy begins to drop at the same number of quantization bits whether or not the network has been pruned. Although pruning made the number of parameters less, quantization still works well, or even better(3 bits case on the left figure) as in the unpruned network.  
![](images/b33c330ed6c437f438bcd431cd178d4d985e6a34746fdf5fd350c50358970b92.jpg)

![](images/566dabf5dd745f9c59799c64966fb5c1e1a03652e8f7c3c3bb4fb91af90a4109.jpg)  
Figure 8: Accuracy of different initialization methods. Left: top-1 accuracy. Right: top-5 accuracy. Linear initialization gives best result.

The first two plots in Figure 7 show that CONV layers require more bits of precision than FC layers. For CONV layers, accuracy drops significantly below 4 bits, while FC layer is more robust: not until 2 bits did the accuracy drop significantly.

## 6.2 CENTROID INITIALIZATION

Figure 8 compares the accuracy of the three different initialization methods with respect to top-1 accuracy (Left) and top-5 accuracy (Right). The network is quantized to 2 ∼ 8 bits as shown on x-axis. Linear initialization outperforms the density initialization and random initialization in all cases except at 3 bits.

![](images/ddb048dadb13eac30b20de36faf57c05c20c4d29d2148f9e2caff837b9355c1f.jpg)  
Figure 9: Compared with the original network, pruned network layer achieved 3× speedup on CPU, 3.5× on GPU and 4.2× on mobile GPU on average. Batch size = 1 targeting real time processing. Performance number normalized to CPU.

![](images/fac4daf861bf8c7a56723dda0810ef61964ffe2176cc6297a9f3c4e9b7213ff8.jpg)  
Figure 10: Compared with the original network, pruned network layer takes 7× less energy on CPU, 3.3× less on GPU and 4.2× less on mobile GPU on average. Batch size = 1 targeting real time processing. Energy number normalized to CPU.

## 6.3 SPEEDUP AND ENERGY EFFICIENCY

Deep Compression is targeting extremely latency-focused applications running on mobile, which requires real-time inference, such as pedestrian detection on an embedded processor inside an autonomous vehicle. Waiting for a batch to assemble significantly adds latency. So when benchmarking the performance and energy efficiency, we consider the case when batch size = 1. The cases of batching are given in Appendix A.

Fully connected layer dominates the model size (more than 90%) and got compressed the most by Deep Compression (96% weights pruned in VGG-16). In state-of-the-art object detection algorithms such as fast R-CNN (Girshick, 2015), upto 38% computation time is consumed on FC layers on uncompressed model. So it’s interesting to benchmark on FC layers, to see the effect of Deep Compression on performance and energy. Thus we setup our benchmark on FC6, FC7, FC8 layers of AlexNet and VGG-16. In the non-batched case, the activation matrix is a vector with just one column, so the computation boils down to dense / sparse matrix-vector multiplication for original / pruned model, respectively. Since current BLAS library on CPU and GPU doesn’t support indirect look-up and relative indexing, we didn’t benchmark the quantized model.

We compare three different off-the-shelf hardware: the NVIDIA GeForce GTX Titan X and the Intel Core i7 5930K as desktop processors (same package as NVIDIA Digits Dev Box) and NVIDIA Tegra K1 as mobile processor. To run the benchmark on GPU, we used cuBLAS GEMV for the original dense layer. For the pruned sparse layer, we stored the sparse matrix in in CSR format, and used cuSPARSE CSRMV kernel, which is optimized for sparse matrix-vector multiplication on GPU. To run the benchmark on CPU, we used MKL CBLAS GEMV for the original dense model and MKL SPBLAS CSRMV for the pruned sparse model.

To compare power consumption between different systems, it is important to measure power at a consistent manner (NVIDIA, b). For our analysis, we are comparing pre-regulation power of the entire application processor (AP) / SOC and DRAM combined. On CPU, the benchmark is running on single socket with a single Haswell-E class Core i7-5930K processor. CPU socket and DRAM power are as reported by the pcm-power utility provided by Intel. For GPU, we used nvidia-smi utility to report the power of Titan X. For mobile GPU, we use a Jetson TK1 development board and measured the total power consumption with a power-meter. We assume 15% AC to DC conversion loss, 85% regulator efficiency and 15% power consumed by peripheral components (NVIDIA, a) to report the AP+DRAM power for Tegra K1.

Table 6: Accuracy of AlexNet with different aggressiveness of weight sharing and quantization. 8/5 bit quantization has no loss of accuracy; 8/4 bit quantization, which is more hardware friendly, has negligible loss of accuracy of 0.01%; To be really aggressive, 4/2 bit quantization resulted in 1.99% and 2.60% loss of accuracy.
<table><tr><td>#CONV bits / #FC bits</td><td>Top-1 Error</td><td>Top-5 Error</td><td>Top-1 Error Increase</td><td>Top-5 Error Increase</td></tr><tr><td>32bits / 32bits</td><td>42.78%</td><td>19.73%</td><td></td><td></td></tr><tr><td>8 bits / 5 bits</td><td>42.78%</td><td>19.70%</td><td>0.00%</td><td>-0.03%</td></tr><tr><td>8 bits /  4 bits</td><td>42.79%</td><td>19.73%</td><td>0.01%</td><td>0.00%</td></tr><tr><td>4 bits / 2 bits</td><td>44.77%</td><td>22.33%</td><td>1.99%</td><td>2.60%</td></tr></table>

The ratio of memory access over computation characteristic with and without batching is different. When the input activations are batched to a matrix the computation becomes matrix-matrix multiplication, where locality can be improved by blocking. Matrix could be blocked to fit in caches and reused efficiently. In this case, the amount of memory access is $O ( n ^ { 2 } )$ , and that of computation is $O ( n ^ { 3 } )$ , the ratio between memory access and computation is in the order of $1 / n$

In real time processing when batching is not allowed, the input activation is a single vector and the computation is matrix-vector multiplication. In this case, the amount of memory access is $O ( n ^ { 2 } )$ , and the computation is $O ( n ^ { 2 } )$ , memory access and computation are of the same magnitude (as opposed to $1 / n )$ . That indicates MV is more memory-bounded than MM. So reducing the memory footprint is critical for the non-batching case.

Figure 9 illustrates the speedup of pruning on different hardware. There are 6 columns for each benchmark, showing the computation time of CPU / GPU / TK1 on dense / pruned network. Time is normalized to CPU. When batch size = 1, pruned network layer obtained $3 \times$ to 4× speedup over the dense network on average because it has smaller memory footprint and alleviates the data transferring overhead, especially for large matrices that are unable to fit into the caches. For example VGG16’s FC6 layer, the largest layer in our experiment, contains 25088 × 4096 × 4 Bytes ≈ 400MB data, which is far from the capacity of L3 cache.

In those latency-tolerating applications , batching improves memory locality, where weights could be blocked and reused in matrix-matrix multiplication. In this scenario, pruned network no longer shows its advantage. We give detailed timing results in Appendix A.

Figure 10 illustrates the energy efficiency of pruning on different hardware. We multiply power consumption with computation time to get energy consumption, then normalized to CPU to get energy efficiency. When batch size = 1, pruned network layer consumes 3× to 7× less energy over the dense network on average. Reported by nvidia-smi, GPU utilization is 99% for both dense and sparse cases.

## 6.4 RATIO OF WEIGHTS, INDEX AND CODEBOOK

Pruning makes the weight matrix sparse, so extra space is needed to store the indexes of non-zero elements. Quantization adds storage for a codebook. The experiment section has already included these two factors. Figure 11 shows the breakdown of three different components when quantizing four networks. Since on average both the weights and the sparse indexes are encoded with 5 bits, their storage is roughly half and half. The overhead of codebook is very small and often negligible.

![](images/fc4f2afdf575e1c9887d1c7db47f0a73025693ecb94227ebadd19998eb52291a.jpg)

![](images/c13e7d8c07f9d342fc5c12800d0e4198622993847ac345b51ea5d98dfb27f3ac.jpg)

![](images/8926c8afc57724d2040eae41a56acb741df2ee5867755d6033286b549c777660.jpg)

![](images/59fe6a1446a094fa673bedaf1087bcb9f46fd855d3bb3ccb356e077a26e8de98.jpg)  
Figure 11: Storage ratio of weight, index and codebook.

Table 7: Comparison with other compression methods on AlexNet. (Collins & Kohli, 2014) reduced the parameters by 4× and with inferior accuracy. Deep Fried Convnets(Yang et al., 2014) worked on fully connected layers and reduced the parameters by less than 4×. SVD save parameters but suffers from large accuracy loss as much as 2%. Network pruning (Han et al., 2015) reduced the parameters by 9×, not including index overhead. On other networks similar to AlexNet, (Denton et al., 2014) exploited linear structure of convnets and compressed the network by 2.4× to 13.4× layer wise, with 0.9% accuracy loss on compressing a single layer. (Gong et al., 2014) experimented with vector quantization and compressed the network by 16× to 24×, incurring 1% accuracy loss.
<table><tr><td>Network</td><td>Top-1 Error</td><td>Top-5 Error</td><td>Parameters</td><td>Compress Rate</td></tr><tr><td>Baseline Caffemodel (BVLC) Fastfood-32-AD (Yang et al., 2014)</td><td>42.78% 41.93%</td><td>19.73%</td><td>240MB 131MB</td><td>1× 2×</td></tr><tr><td>Fastfood-16-AD (Yang et al., 2014)</td><td>42.90%</td><td></td><td>64MB</td><td>3.7×</td></tr><tr><td>Collins &amp; Kohli (Collins &amp; Kohli, 2014)</td><td>44.40%</td><td></td><td>61MB</td><td>4×</td></tr><tr><td>SVD (Denton et al., 2014)</td><td>44.02%</td><td>20.56%</td><td>47.6MB</td><td>5×</td></tr><tr><td>Pruning (Han et al., 2015)</td><td>42.77%</td><td>19.67%</td><td>27MB</td><td>9×</td></tr><tr><td>Pruning+Quantization</td><td>42.78%</td><td>19.70%</td><td>8.9MB</td><td>27×</td></tr><tr><td>Pruning+Quantization+Huffman</td><td>42.78%</td><td>19.70%</td><td>6.9MB</td><td>35×</td></tr></table>

## 7 RELATED WORK

Neural networks are typically over-parametrized, and there is significant redundancy for deep learning models(Denil et al., 2013). This results in a waste of both computation and memory usage. There have been various proposals to remove the redundancy: Vanhoucke et al. (2011) explored a fixedpoint implementation with 8-bit integer (vs 32-bit floating point) activations. Hwang & Sung (2014) proposed an optimization method for the fixed-point network with ternary weights and 3-bit activations. Anwar et al. (2015) quantized the neural network using L2 error minimization and achieved better accuracy on MNIST and CIFAR-10 datasets.Denton et al. (2014) exploited the linear structure of the neural network by finding an appropriate low-rank approximation of the parameters and keeping the accuracy within 1% of the original model.

The empirical success in this paper is consistent with the theoretical study of random-like sparse networks with +1/0/-1 weights (Arora et al., 2014), which have been proved to enjoy nice properties (e.g. reversibility), and to allow a provably polynomial time algorithm for training.

Much work has been focused on binning the network parameters into buckets, and only the values in the buckets need to be stored. HashedNets(Chen et al., 2015) reduce model sizes by using a hash function to randomly group connection weights, so that all connections within the same hash bucket share a single parameter value. In their method, the weight binning is pre-determined by the hash function, instead of being learned through training, which doesn’t capture the nature of images. Gong et al. (2014) compressed deep convnets using vector quantization, which resulted in 1% accuracy loss. Both methods studied only the fully connected layer, ignoring the convolutional layers.

There have been other attempts to reduce the number of parameters of neural networks by replacing the fully connected layer with global average pooling. The Network in Network architecture(Lin et al., 2013) and GoogLenet(Szegedy et al., 2014) achieves state-of-the-art results on several benchmarks by adopting this idea. However, transfer learning, i.e. reusing features learned on the ImageNet dataset and applying them to new tasks by only fine-tuning the fully connected layers, is more difficult with this approach. This problem is noted by Szegedy et al. (2014) and motivates them to add a linear layer on the top of their networks to enable transfer learning.

Network pruning has been used both to reduce network complexity and to reduce over-fitting. An early approach to pruning was biased weight decay (Hanson & Pratt, 1989). Optimal Brain Damage (LeCun et al., 1989) and Optimal Brain Surgeon (Hassibi et al., 1993) prune networks to reduce the number of connections based on the Hessian of the loss function and suggest that such pruning is more accurate than magnitude-based pruning such as weight decay. A recent work (Han et al., 2015) successfully pruned several state of the art large scale networks and showed that the number of parameters could be reduce by an order of magnitude. There are also attempts to reduce the number of activations for both compression and acceleration Van Nguyen et al. (2015).

## 8 FUTURE WORK

While the pruned network has been benchmarked on various hardware, the quantized network with weight sharing has not, because off-the-shelf cuSPARSE or MKL SPBLAS library does not support indirect matrix entry lookup, nor is the relative index in CSC or CSR format supported. So the full advantage of Deep Compression that fit the model in cache is not fully unveiled. A software solution is to write customized GPU kernels that support this. A hardware solution is to build custom ASIC architecture specialized to traverse the sparse and quantized network structure, which also supports customized quantization bit width. We expect this architecture to have energy dominated by on-chip SRAM access instead of off-chip DRAM access.

## 9 CONCLUSION

We have presented “Deep Compression” that compressed neural networks without affecting accuracy. Our method operates by pruning the unimportant connections, quantizing the network using weight sharing, and then applying Huffman coding. We highlight our experiments on AlexNet which reduced the weight storage by 35× without loss of accuracy. We show similar results for VGG-16 and LeNet networks compressed by 49× and 39× without loss of accuracy. This leads to smaller storage requirement of putting convnets into mobile app. After Deep Compression the size of these networks fit into on-chip SRAM cache (5pJ/access) rather than requiring off-chip DRAM memory (640pJ/access). This potentially makes deep neural networks more energy efficient to run on mobile. Our compression method also facilitates the use of complex neural networks in mobile applications where application size and download bandwidth are constrained.

## REFERENCES

Anwar, Sajid, Hwang, Kyuyeon, and Sung, Wonyong. Fixed point optimization of deep convolutional neural networks for object recognition. In Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on, pp. 1131–1135. IEEE, 2015.

Arora, Sanjeev, Bhaskara, Aditya, Ge, Rong, and Ma, Tengyu. Provable bounds for learning some deep representations. In Proceedings of the 31th International Conference on Machine Learning, ICML 2014, pp. 584–592, 2014.

BVLC. Caffe model zoo. URL http://caffe.berkeleyvision.org/model\_zoo.

Chen, Wenlin, Wilson, James T., Tyree, Stephen, Weinberger, Kilian Q., and Chen, Yixin. Compressing neural networks with the hashing trick. arXiv preprint arXiv:1504.04788, 2015.

Collins, Maxwell D and Kohli, Pushmeet. Memory bounded deep convolutional networks. arXiv preprint arXiv:1412.1442, 2014.

Denil, Misha, Shakibi, Babak, Dinh, Laurent, de Freitas, Nando, et al. Predicting parameters in deep learning. In Advances in Neural Information Processing Systems, pp. 2148–2156, 2013.

Denton, Emily L, Zaremba, Wojciech, Bruna, Joan, LeCun, Yann, and Fergus, Rob. Exploiting linear structure within convolutional networks for efficient evaluation. In Advances in Neural Information Processing Systems, pp. 1269–1277, 2014.

Girshick, Ross. Fast r-cnn. arXiv preprint arXiv:1504.08083, 2015.

Gong, Yunchao, Liu, Liu, Yang, Ming, and Bourdev, Lubomir. Compressing deep convolutional networks using vector quantization. arXiv preprint arXiv:1412.6115, 2014.

Han, Song, Pool, Jeff, Tran, John, and Dally, William J. Learning both weights and connections for efficient neural networks. In Advances in Neural Information Processing Systems, 2015.

Han, Song, Liu, Xingyu, Mao, Huizi, Pu, Jing, Pedram, Ardavan, Horowitz, Mark A, and Dally, William J. EIE: Efficient inference engine on compressed deep neural network. arXiv preprint arXiv:1602.01528, 2016.

Hanson, Stephen Jose and Pratt, Lorien Y. Comparing biases for minimal network construction with´ back-propagation. In Advances in neural information processing systems, pp. 177–185, 1989.

Hassibi, Babak, Stork, David G, et al. Second order derivatives for network pruning: Optimal brain surgeon. Advances in neural information processing systems, pp. 164–164, 1993.

Hwang, Kyuyeon and Sung, Wonyong. Fixed-point feedforward deep neural network design using weights+ 1, 0, and- 1. In Signal Processing Systems (SiPS), 2014 IEEE Workshop on, pp. 1–6. IEEE, 2014.

Jia, Yangqing, Shelhamer, Evan, Donahue, Jeff, Karayev, Sergey, Long, Jonathan, Girshick, Ross, Guadarrama, Sergio, and Darrell, Trevor. Caffe: Convolutional architecture for fast feature embedding. arXiv preprint arXiv:1408.5093, 2014.

Krizhevsky, Alex, Sutskever, Ilya, and Hinton, Geoffrey E. Imagenet classification with deep convolutional neural networks. In NIPS, pp. 1097–1105, 2012.

LeCun, Yann, Denker, John S, Solla, Sara A, Howard, Richard E, and Jackel, Lawrence D. Optimal brain damage. In NIPs, volume 89, 1989.

LeCun, Yann, Bottou, Leon, Bengio, Yoshua, and Haffner, Patrick. Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11):2278–2324, 1998.

Lin, Min, Chen, Qiang, and Yan, Shuicheng. Network in network. arXiv:1312.4400, 2013.

NVIDIA. Technical brief: NVIDIA jetson TK1 development kit bringing GPU-accelerated computing to embedded systems, a. URL http://www.nvidia.com.

NVIDIA. Whitepaper: GPU-based deep learning inference: A performance and power analysis, b. URL http://www.nvidia.com/object/white-papers.html.

Simonyan, Karen and Zisserman, Andrew. Very deep convolutional networks for large-scale image recognition. arXiv preprint arXiv:1409.1556, 2014.

Strom, Nikko. Phoneme probability estimation with dynamic sparsely connected artificial neural¨ networks. The Free Speech Journal, 1(5):1–41, 1997.

Szegedy, Christian, Liu, Wei, Jia, Yangqing, Sermanet, Pierre, Reed, Scott, Anguelov, Dragomir, Erhan, Dumitru, Vanhoucke, Vincent, and Rabinovich, Andrew. Going deeper with convolutions. arXiv preprint arXiv:1409.4842, 2014.

Van Leeuwen, Jan. On the construction of huffman trees. In ICALP, pp. 382–410, 1976.

Van Nguyen, Hien, Zhou, Kevin, and Vemulapalli, Raviteja. Cross-domain synthesis of medical images using efficient location-sensitive deep network. In Medical Image Computing and Computer-Assisted Intervention–MICCAI 2015, pp. 677–684. Springer, 2015.

Vanhoucke, Vincent, Senior, Andrew, and Mao, Mark Z. Improving the speed of neural networks on cpus. In Proc. Deep Learning and Unsupervised Feature Learning NIPS Workshop, 2011.

Yang, Zichao, Moczulski, Marcin, Denil, Misha, de Freitas, Nando, Smola, Alex, Song, Le, and Wang, Ziyu. Deep fried convnets. arXiv preprint arXiv:1412.7149, 2014.

## A APPENDIX: DETAILED TIMING / POWER REPORTS OF DENSE & SPARSE NETWORK LAYERS

Table 8: Average time on different layers. To avoid variance, we measured the time spent on each layer for 4096 input samples, and averaged the time regarding each input sample. For GPU, the time consumed by cudaMalloc and cudaMemcpy is not counted. For batch size = 1, gemv is used; For batch size = 64, gemm is used. For sparse case, csrmv and csrmm is used, respectively.
<table><tr><td colspan="2">Time (us)</td><td>AlexNet FC6</td><td>AlexNet FC7</td><td>AlexNet FC8</td><td>VGG16 FC6</td><td>VGG16 FC7</td><td>VGG16 FC8</td></tr><tr><td>Titan X</td><td>dense (batch=1) sparse (batch=1) dense (batch=64) sparse (batch=64)</td><td>541.5 134.8 19.8 94.6</td><td>243.0 65.8 8.9 51.5</td><td>80.5 54.6 5.9 23.2</td><td>1467.8 167.0 53.6 121.5</td><td>243.0 39.8 8.9 24.4</td><td>80.5 48.0 5.9 22.0</td></tr><tr><td>Core i7-5930k</td><td>dense (batch=1) sparse (batch=1) dense (batch=64) sparse (batch=64)</td><td>7516.2 3066.5 318.4 1417.6</td><td>6187.1 1282.1 188.9 682.1</td><td>1134.9 890.5 45.8 407.7</td><td>35022.8 3774.3 1056.0 1780.3</td><td>5372.8 545.1 188.3 274.9</td><td>774.2 777.3 45.7 363.1</td></tr><tr><td>Tegra K1</td><td>dense (batch=1) sparse (batch=1) dense (batch=64) sparse (batch=64)</td><td>12437.2 2879.3 1663.6 4003.9</td><td>5765.0 1256.5 2056.8 1372.8</td><td>2252.1 837.0 298.0 576.7</td><td>35427.0 4377.2 2001.4 8024.8</td><td>5544.3 626.3 2050.7 660.2</td><td>2243.1 745.1 483.9 544.1</td></tr></table>

Table 9: Power consumption of different layers. We measured the Titan X GPU power with nvidia-smi, Core i7-5930k CPU power with pcm-power and Tegra K1 mobile GPU power with an external power meter (scaled to AP+DRAM, see paper discussion). During power measurement, we repeated each computation multiple times in order to get stable numbers. On CPU, dense matrix multiplications consume 2x energy than sparse ones because it is accelerated with multi-threading.
<table><tr><td colspan="2">Power (Watts)</td><td>AlexNet FC6</td><td>AlexNet FC7</td><td>AlexNet FC8</td><td>VGG16 FC6</td><td>VGG16 FC7</td><td>VGG16 FC8</td></tr><tr><td rowspan="4">TitanX</td><td>dense (batch=1)</td><td>157</td><td>159</td><td>159</td><td>166</td><td>163</td><td>159</td></tr><tr><td>sparse (batch=1)</td><td>181</td><td>183</td><td>162</td><td>189</td><td>166</td><td>162</td></tr><tr><td>dense (batch=64)</td><td>168</td><td>173</td><td>166</td><td>173</td><td>173</td><td>167</td></tr><tr><td>sparse (batch=64)</td><td>156</td><td>158</td><td>163</td><td>160</td><td>158</td><td>161</td></tr><tr><td rowspan="4">Core i7-5930k</td><td>dense (batch=1)</td><td>83.5</td><td>72.8</td><td>77.6</td><td>70.6</td><td>74.6</td><td>77.0</td></tr><tr><td>sparse (batch=1)</td><td>42.3</td><td>37.4</td><td>36.5</td><td>38.0</td><td>37.4</td><td>36.0</td></tr><tr><td>dense (batch=64)</td><td>85.4</td><td>84.7</td><td>101.6</td><td>83.1</td><td>97.1</td><td>87.5</td></tr><tr><td>sparse (batch=64)</td><td>37.2</td><td>37.1</td><td>38</td><td>39.5</td><td>36.6</td><td>38.2</td></tr><tr><td rowspan="4">Tegra K1</td><td>dense (batch=1)</td><td>5.1</td><td>5.1</td><td>5.4</td><td>5.3</td><td>5.3</td><td>5.4</td></tr><tr><td>sparse (batch=1)</td><td>5.9</td><td>6.1</td><td>5.8</td><td>5.6</td><td>6.3</td><td>5.8</td></tr><tr><td>dense (batch=64)</td><td>5.6</td><td>5.6</td><td>6.3</td><td>5.4</td><td>5.6</td><td>6.3</td></tr><tr><td>sparse (batch=64)</td><td>5.0</td><td>4.6</td><td>5.1</td><td>4.8</td><td>4.7</td><td>5.0</td></tr></table>