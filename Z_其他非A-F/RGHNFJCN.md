# Radar Ghost Target Detection via Multimodal Transformers

LeiChen Wang , Simon Giebenhain, Carsten Anklam, and Bastian Goldluecke

Abstract—Ghost targets caused by inter-reflections are by design unavoidable in radar measurements, and it is challenging to distinguish these artifact detections from real ones. In this letter, we propose a novel approach to detect radar ghost targets by using LiDAR data as a reference. For this, we adopt a multimodal transformer network to learn interactions between points. We employ self-attention to exchange information between radar points, and local crossmodal attention to infuse information from surrounding LiDAR points. The key idea is that a ghost target should have higher semantic affinity with the reflected real target than the other ones. Extensive experiments on nuScenes [1] show that our method outperforms the baseline method on radar ghost target detection by a large margin.

Index Terms—Ghost target, sensor fusion, multimodal transformer.

## I. INTRODUCTION

O <sup>VER</sup> <sup>the</sup> <sup>past</sup> <sup>few</sup> <sup>decades,</sup> <sup>automotive</sup> <sup>original</sup> <sup>equipment</sup>manufacturers (OEMs) have been equipping modern cars manufacturers (OEMs) have been equipping modern cars with a wide array of advanced control and sensing functions. With the help of LiDAR, radar, and cameras, automotive vehicles (AVs) can see their surroundings under a range of weather and lighting conditions. Furthermore, multi-sensor fusion contributes to the robustness of the AVs. Considering each sensor may be degraded or defective during driving, relying on only one sensor while driving is risky. Compared to LiDAR and cameras, radar enjoys several advantages, including long detection distance, all-day and all-weather operation. Moreover, due to its compact size and reasonable price, radar is the most reliable and most widely used sensor in Advanced Driver Assistance Systems (ADAS).

Automotive radar is designed to estimate objects’ positions and velocities by transmitting electromagnetic waves and receiving their reflections. Radar is designed to calculate the target objects’ positions by the time of flight (ToF) of multipath waves. On the one hand, multipath wave propagation can be used to detect occluded objects from their indirect reflections by Non-line-of-sight (NLOS) methods [16], [18]. On the other hand, multipath waves are susceptible to contamination speckle noise, reflections, and artifacts. Fig. 1 illustrates the phenomenon we refer to as the “mirror effect,” where electromagnetic waves returning from a target vehicle get reflected by a “mirror surface,” e.g. tunnels, walls, or bridges. The reflected non-existing detections are commonly referred to as ghost targets or artifact detections and are comparable to a mirage in the desert. These ghost targets are unavoidable due to the radar’s design, and it is very challenging to distinguish them from real detections. This phenomenon can significantly reduce autonomous driving’s reliability and safety due to high false-positive detection rates or unnecessary and potentially dangerous emergency brakes.

![](images/5e8f36529132767fc06e8e69bb6e3fa2b680fe13faa28d8f8b21782fb93117f9.jpg)  
Fig. 1. Mirror effect: The ego vehicle equipped with the radar sensor detects a ghost target (red radar points) on the secondary lane due to the indirect reflection of the radar wave off the real target vehicle A (green radar points). Due to the reflection relationship between real vehicle A and ghost vehicle, the ghost point has high attention to the real vehicle A, but low attention to the vehicle B.

In recent years, with artificial intelligence development, OEMs and research institutes start trying to use machine learning (or deep learning) to solve this problem [6], [7], [13]. In [7], LiDAR is directly used as ground truth to evaluate the radar’s performance. However, after detailed analysis, we found that this supervision is flawed, as LiDAR is also likely to miss some distanced or occluded targets [25]. Hence, in complicated real-world driving environments, neither LiDAR nor radar is entirely reliable. Further, those works attempt to distinguish ghost points only by hand-crafted features, such as Radar cross-section (RCS), Doppler velocity etc.However, detecting ghost targets from such hand-crafted features proved difficult, as both ghost and real points’ features have high similarity.

To address the above issues, we propose a novel approach that explicitly allows for interactions between radar points. The idea is that capturing the relationship between ghost targets and their corresponding reflected real target can yield important insights to distinguish ghost targets. For related tasks in natural language processing (NLP), transformer networks [23] have been applied with great success. Their key idea is to build semantic affinities between distant words to understand a sentence, and building relations between multiple words is crucial to comprehend the true meaning. We argue that detecting ghost targets also demands these two qualities, making self-attention a suitable framework that can efficiently be parallelized on a GPU.

![](images/4300f6a3882510e6f88b310e07f6ddbddb69a56ff56038bdd1944596d67687f6.jpg)  
Fig. 2. This paper introduces a multimodal transformer to classify raw radar points (images on top) into ghost radar points (bottom left) and actual detections The radar point in the red circle is a typical critical ghost target. Since it is only 35 meters in front of ego vehicle on the ego lane, it may cause an unexpected braking during autonomous driving. The top left image shows radar points projected onto the front camera image, while the right shows a BEV of the same scenario. Radar points are colored according to their distance to the ego vehicle. In the BEV images, the radar points’ vectors show their Doppler velocity, object annotations are shown as orange boxes, and LiDAR points are shown as reference in light gray. The bottom left image indicates the ghost point’s self-attentio map, while the middle bottom shows the cross-modal attention map of sampled LiDAR points (yellow to dark blue means increasing attention weight). Note that, for a better understanding, the LiDAR ground points are not displayed. The bottom right shows our network’s predictions of ghost targets. The critical ghost target is successfully classified. Please zoom in for details.

We employ self-attention to exchange information between radar points and local crossmodal attention to infuse information from surrounding LiDAR points. From a theoretical perspective, this multimodal attention-based approach provides several desirable advantages. First, the global processing scheme of attention helps to capture interactions between ghost points that are far away from their corresponding real targets. Furthermore, multiple rounds of attention can capture long-range, n-ary relationships and gain a more thorough understanding of the complete scene. Second, in most cases, LiDAR captures more detailed spatial information. We thus find that crossmodal attention is a very concise and elegant strategy for LiDARradar sensor fusion, providing a more detailed context for the radar points. And finally, attention is permutation invariant by design, making it suitable for point cloud processing [5], [26].

Note that, different from LiDAR point cloud, radar points (or detections) are typically the output of digital signal processing (DSP). In detail, radar reflections are calculated by using constant false alarm rate (CFAR) thresholding and by evaluating the complex amplitudes of the peaks in the range-Doppler spectra [19]. Due to the different working principles, the extent of the decline of radar point density with further distance is much less than LiDAR [9]. However, a typical radar scan is designed to own only about one hundred points (e.g. Continental ARS40X). Compared to a 32-channels LiDAR, whose single scan has more than 30 000 points, radar points are much sparser than LiDAR points, even in the far range.

Contributions. We propose the Multimodal Transformer, which can effectively detect radar ghost targets by learning the interactions between LiDAR and radar points. Our key idea is to distinguish the ghost points from real ones by radar-radar pairwise matching as well as radar-LiDAR matching. To our understanding, a ghost target should have much higher semantic affinities with the reflected target than other ones. See Fig. 2. As end effect, radar can provide more robust and accurate data for the subsequent object detection algorithms. This will eventually enable AVs to perceive the environment more accurately through sensor fusion.

We make the following contributions:

\- To the best of our knowledge, this is the first work that leverages transformers [23] to operate directly on unordered radar data and focuses on the relationship between the ghost and reflected targets.

\- Additionally, our network effectively infuses information from spatially relevant LiDAR points using crossmodal attention, to provide richer context information.

\- We propose a new ground truth generation scheme that labels the ghost target more efficiently and accurately. It combines the advantages of both a LiDAR-based and annotation-based schemes.

Comprehensive experiments on nuScenes [1] show that our method outperforms the baseline method [11], which further improves the multimodal detection performance substantially.

## II. RELATED WORK

## A. Radar Ghost Target Detection

Radar ghost targets have long been regarded as one of the biggest challenges that affect the realization of autonomous driving [17][19]. Many works attempt to present mathematical formulations for multipath propagation models to remove the ghost targets with the help of hand-crafted features or characteristics.

By analyzing each target’s line-of-sight (LOS) distance and non-line-of-sight (NLOS) distance, [10] distinguishes ghost targets of multipath propagation. Likewise, [17] compares the object’s orientation and its motion vector to distinguish ghosts from real ones. [6] gives an overview of different types of false radar detections. Further, they present mathematical models that describe the artifacts by simulation in the radar signal processing chain. Since 2018, various machine and deep learning approaches on radar data have arisen in response to this issue. A typical machine learning approach using random forests (RF) is presented in [13] to classify radar detections into real and ghost points. In 2020, Kraus [7] designed a dataset specifically for the ghost target problem to explore the impact of the mirror-effect.

Based on this dataset, [7] presents a PointNet++[15] based approach to detect the reflected ghost targets. Their PointNet++ is trained to classify 2D radar points into the following five classes: Pedestrians, cyclists, ghost pedestrians, ghost cyclists, and background. Their experiments show that ghost targets can be detected with a precision and recall of around 53% and 56%, respectively. Similarly, [2] also uses a PointNet-like framework to classify whether points are real or ghost points.

Different from the above PointNet-based methods, in [11], a Neural Radar Filter (NRF) is proposed to voxelized radar points into a Bird’s-eye-view (BEV) grid map. The voxel-wise features are further fed to a CNN to output a result mask, which indicates the probability of each point being a ghost. However, their experiments show that the NRF has a negative impact on the subsequent object detection network.ie.mAP without NRF is 45.79%, mAP with NRF is 45.20%.

## B. Transformers on Point Clouds

As point clouds are essentially sets embedded into 3D space, designing suitable neural network architectures is challenging since they need to be permutation invariant while respecting the points’ geometric structure. Over the last few years Point-Net [14] and PointNet++ [15] proved to be the most versatile architectures and inspired most state-of-the-art models in tasks involving point clouds, e.g. PointRCNN [21], PV-RCNN [20].

However, a fundamental shortcoming of PointNet++ is that it does not explicitly model interactions between points. To overcome this issue, recent work explicitly allows for interactions by using attention mechanisms proposed in [23]. Transformers have demonstrated their representational power and flexibility over the past few years by producing state-of-the-art models in many different complex areas of machine learning, e.g. in NLP [23] and image classification [4]. As the attention mechanism is permutation invariant by design, transformers can also be directly applied to point cloud processing. For example, [5] downsamples and aggregates features in local neighborhoods before using self-attention to facilitate global information exchange. [26] establishes a new state-of-the-art for point cloud classification and segmentation by repeatedly applying local self-attention, furthest-point-sampling, and max-pooling. These results validate our choice to process radar and LiDAR points using attention mechanisms.

## III. ATTENTION MODULES

We follow the attention-based principle of Transformers [23], in order to detect ghost targets based on their relation to other points within the scene. To fully exploit the complementary information of LiDAR and radar, we introduce a multimodal Transformer network, which we describe in this and the following section. We start by reviewing the original attention module, self attention, and crossmodal attention in III-A, explain how we use self-attention among radar points III-B and describe our multimodal attention module that fuses information from radar and LiDAR points III-C. After having defined the individual modules in this section, the next section discusses our data encoding scheme and the complete network architecture.

## A. Background: Scaled dot Product Attention

The attention mechanism of transformers can be thought of as a differentiable information routing scheme, that directs information using query, key and value vectors for each element. Queries and keys are used to compute affinities between individual entities, while the values hold the actual information which is passed on. The input to the self-attention module is a feature map F of size $N \times d _ { i n }$ , where N is the number of data points and $d _ { i n }$ the input dimensionality. The attention layer outputs a feature map of size $N \times d _ { o u t }$ , where $d _ { o u t }$ is a user-defined.

We follow the scaled dot product attention scheme of the original Transformer [23], and first generate query, key and value matrices using linear transformations

$$
( Q , K , V ) = ( F W _ { Q } , F W _ { K } , F W _ { V } )\tag{1}
$$

with $Q , K \in \mathbb { R } ^ { N \times d _ { q k } } , \quad V \in \mathbb { R } ^ { N \times d _ { o u t } }$ , and the trainable weights $W _ { Q } , W _ { K } \in \mathbb { R } ^ { d _ { i n } \times d _ { q k } }$ and $W _ { V } \in \mathbb { R } ^ { d _ { i n } \times d _ { o u t } }$ , respectively. Here $d _ { q k }$ is user-defined and dictates the internal dimensionality of queries and keys.

In self-attention, the output is computed according to

$$
\mathrm { S A } ( F ) = \mathrm { s o f t m a x } \left( \frac { Q K ^ { T } } { \sqrt { d _ { q k } } } \right) V .\tag{2}
$$

This matrix notation is short for the weighted sum over the values for each row $i = 1 , \ldots , N$ of the output,

$$
\mathrm { S A } _ { i } ( F ) = \sum _ { j = 1 } ^ { N } w _ { i , j } V _ { j } ,\tag{3}
$$

where the attention weights $w _ { i , j }$ are calculated as

$$
w _ { i , j } = \frac { e x p ( Q _ { i } K _ { j } ^ { T } / \sqrt { d _ { q k } } ) } { \sum _ { l = 1 } ^ { N } e x p ( Q _ { i } K _ { l } ^ { T } / \sqrt { d _ { q k } } ) } .\tag{4}
$$

The dot product computes the similarity between queries and keys, which is scaled by $\sqrt { d _ { q k } }$ and normalized using the softmax function to produce the attention weights $w _ { i , j }$

In crossmodal attention [22], there are two input feature maps $F _ { \alpha }$ and $F _ { \beta }$ with potentially different input dimensions. Queries $Q _ { \alpha }$ are computed from the feature map $F _ { \alpha } ,$ while keys $K _ { \beta }$ and values $V _ { \beta }$ are computed from the feature map $F _ { \beta }$ , with dimensions for the trainable weights adjusted accordingly. The output is now defined as

$$
\mathrm { C M A } ( F _ { \alpha } , F _ { \beta } ) = \mathrm { s o f t m a x } \left( \frac { Q _ { \alpha } K _ { \beta } ^ { T } } { \sqrt { d _ { q k } } } \right) V _ { \beta } .\tag{5}
$$

Note that the output has the same number of rows as $F _ { \alpha }$ , but draws information from the feature space $F _ { \beta }$

## B. Self-Attention Module for Radar Points

Since ghost targets may be far way from their corresponding real targets, we use a self-attention module which facilitates information exchange between all radar points. By utilizing position embeddings, the self-attention module is also informed about the geometry of the scene. We transform raw radar input $P _ { \alpha }$ into feature space using a data encoding function specified in the next section and apply the self-attention layer (2). Generally, the quadratic time and space complexity of self-attention with respect to N is a drawback. However, since the number of radar points is relatively low (in most cases, each radar frame has about one hundred points), self-attention can be efficiently used.

## C. Multimodal Attention Module

The key idea of this module is to incorporate additional information from the LiDAR sensor and to learn important latent features of ghost targets across both modalities. To this end we build a directional pairwise crossmodal attention module, which matches radar queries with LiDAR keys to calculate similarities across both modalities. Due to LiDAR’s higher resolution, it can provide more detailed spatial information. However, in our dataset [1], the amount of LiDAR points $N _ { \beta }$ is almost one hundred times larger than radar’s $N _ { \alpha } ~ ( \sim 1 0 , 0 0 0 ~ \mathrm { v s } \sim 1 0 0 )$ rendering the computation of full radar-LiDAR cross-attention computationally infeasible.

Thus a sampling strategy is necessary. Different from farthest point sampling (FPS) in PointNet++ and its variant forms [15], we design a unique approach to sample LiDAR points. Like a “magnifying lens,” we propose to view LiDAR points around each radar point as a local description of the scene structure.

![](images/b9af38ee71d8a5bd79b80d29a82ce8b2bd809f1cf196a69e318296b97c4bc900.jpg)  
Fig. 3. Overview of our multimodal attention block, which consists of two main components: self-attention (SA) and cross modal attention (CMA).

Incorporating this local information helps to process radar points according to their environmental contexts. For this, we first use KNN to search a fixed amount $N _ { K }$ of LiDAR points around each of the $N _ { \alpha }$ radar points. Since $N _ { K } \cdot N _ { \alpha } < N _ { \beta }$ in our setting and we delete possible duplicate points, we further randomly sample from the remaining points to insert into the accumulated point set until it has $N _ { \beta }$ points.

From the resulting point sets, we assemble the feature maps $( F _ { \alpha } , F _ { \beta } )$ for radar and LiDAR points, respectively, and compute a new feature map $\mathrm { C M A } ( F _ { \alpha } , F _ { \beta } )$ with crossmodal attention (5), taking into account the similarity between each radar-LiDAR pair.

To fuse radar and LiDAR information, we concatenate selfattention and crossmodal attention to generate the final multimodal attention features,

$$
\mathrm { M M A } ( F _ { \alpha } , F _ { \beta } ) = \mathrm { c o n c a t } \big ( ( \mathrm { S A } ( F _ { \alpha } ) , \mathrm { C M A } ( F _ { \alpha } , F _ { \beta } ) \big ) .\tag{6}
$$

This way the final features for each point contain information from all radar and sampled LiDAR points that are relevant for the point. The self-attention module focuses on the relationship within radar points, while crossmodal attention blocks tend to search LiDAR data around each radar point to absorb local features. See Fig. 3 for an illustration of the architecture of a multimodal attention module.

## IV. MULTIMODAL TRANSFORMER NETWORK

We will now explain how the data from the two different modalities are encoded and construct our network architecture from the different building blocks.

## A. Data Encoding

Since both radar and LiDAR points consist of two parts, namely the point coordinates $P _ { C }$ and the corresponding point features $\mathit { P } _ { F } , e . g .$ intensity, velocity, RCS, we divide this part into positional and feature encoding.

In the original Transformer [23], positional embeddings are introduced to represent the discrete positions of words. In our application both radar and LiDAR points have positional information. Radar points have 2D coordinate information $( X , Y$ no vertical data) in three-dimensional Euclidean space, while a LiDAR points have 3D coordinates $( X , Y , Z )$ . To further unify and optimize their position information, 2D radar point coordinates $P _ { C \alpha }$ and 3D LiDAR point coordinates $P _ { C \beta }$ are encoded into a common feature space with dimension $d _ { C } ,$

![](images/afd3ccf85bb65077711a80b2ef112824ae4d58da393ae240d74ab46d68dd0106.jpg)  
Fig. 4. Our two backbone variants. Top: Variant V 1 consists of one MMA and two SA blocks. Bottom: Variant V 2 is made up of three MMA blocks.

$$
\begin{array} { r l } & { F _ { C \alpha } = \theta _ { \alpha } ( P _ { C \alpha } ) , F _ { C \alpha } \in \mathbb { R } ^ { N _ { \alpha } \times d _ { C } } , } \\ & { F _ { C \beta } = \theta _ { \beta } ( P _ { C \beta } ) , F _ { C \beta } \in \mathbb { R } ^ { N _ { \beta } \times d _ { C } } . } \end{array}\tag{7}
$$

In contrast to their coordinate values, both sensors’ feature values are entirely different. For example, radar points contain corresponding velocity information while LiDAR has intensity as the laser beam’s return strength. So we encode the point features into two different representation subspaces $F _ { F \alpha }$ and $F _ { F \beta }$ with respective dimensions,

$$
\begin{array} { r l } & { F _ { F \alpha } = \lambda _ { \alpha } ( P _ { F \alpha } ) , \ F _ { F \alpha } \in \mathbb { R } ^ { N _ { \alpha } \times d _ { F \alpha } } , } \\ & { F _ { F \beta } = \lambda _ { \beta } ( P _ { F \beta } ) , \ F _ { F \beta } \in \mathbb { R } ^ { N _ { \beta } \times d _ { F \beta } } . } \end{array}\tag{8}
$$

Finally, both features are concatenated,

$$
\begin{array} { r l } & { F _ { \alpha } = \mathrm { c o n c a t } ( F _ { C \alpha } , F _ { F \alpha } ) , \ F _ { \alpha } \in \mathbb { R } ^ { N _ { \alpha } \times ( d _ { C } + d _ { F \alpha } ) } , } \\ & { F _ { \beta } = \mathrm { c o n c a t } ( F _ { C \beta } , F _ { F \beta } ) , \ F _ { \beta } \in \mathbb { R } ^ { N _ { \beta } \times ( d _ { C } + d _ { F \beta } ) } . } \end{array}\tag{9}
$$

The encoding functions θ and λ consist of three layers with ReLU activations and batch normalization, and are trained end-to-end. We give exact details about our hyperparameter configuration in Section V.

## B. Network Architecture

Backbone structure. After encoding all entities from each modality in the feature space as described in the previous section, we utilize three stages of attention blocks. Note that the number of stages can be varied depending on the application and data size. In particular, we design two backbone variants to evaluate the influence of different modules on the final result. Fig. 4 provides an overview of both variants.

In the first backbone variant V1, a multimodal attention block (6) is followed by two self-attention blocks (2). The output features of each attention block are

$$
\begin{array} { r l } & { F _ { 1 } = \mathrm { M M A } ^ { 1 } ( F _ { \alpha } , F _ { \beta } ) , } \\ & { F _ { i } = \mathrm { S A } ^ { i - 1 } ( F _ { i - 1 } ) , \mathrm { f o r } i \in \{ 2 , 3 \} , } \end{array}\tag{10}
$$

where $F _ { i }$ means the output feature of the i-th block. To obtain the final feature vector, which is fed into the output head, we concatenate the features from all three layers.

In the second backbone variant V2, we replace two selfattention blocks with multimodal attention blocks, which attempt to repeatedly reinforce low-level information from the LiDAR points. By doing so, the second and third block can build more complex relations between the fused high-level and low-level LiDAR features. The output features of each attention block are

$$
\begin{array} { r l } & { F _ { 1 } = \mathrm { M M A } ^ { 1 } ( F _ { \alpha } , F _ { \beta } ) , } \\ & { F _ { i } = \mathrm { M M A } ^ { i } ( F _ { i - 1 } , F _ { \beta } ) \mathrm { f o r } i \in \{ 2 , 3 \} . } \end{array}\tag{11}
$$

Output head. As our task is essentially a two-class semantic segmentation problem, we leverage the segmentation output head from PointNet++[15] and PCT [5]. The final features are passed through two shared fully connected (FC), batch normalization, and ReLU layers, which are applied to produce each point’s feature vector. The last score prediction layer only consists of a linear mapping to a single scalar without a batch normalization or ReLU layer. For details see Section V-C.

Evaluation Metric and Loss Function. To evaluate this binary classification problem, we follow the evaluation metric of the baseline work [7] and use the area under the receiver operating characteristic curve (AUC-ROC) [3]. The ROC curve is plotted with the True Positive Rate (TPR) on the y-axis against the False Positive Rate (FPR) on the x-axis at different classification thresholds. The AUC-ROC measures the entire 2D area underneath the ROC curve from (0,0) to (1,1). It provides an aggregate measure of performance across all possible classification thresholds. During training, we minimize the binary cross-entropy loss.

## V. EXPERIMENTAL SETUP

## A. Dataset

We validate the proposed method on the nuScenes dataset [1]. nuScenes is one of the first datasets collected from an AV approved for testing on public roads containing multimodal sensors, LiDAR, camera, and radar. The test AV is equipped with six cameras (12 Hz), five automotive long-range-radars Continental ARS40X (13 Hz), and one Velodyne 32-channel-LiDAR (20 Hz). The keyframes are sampled at 2 Hz to be annotated on the object-level (bounding boxes parametrized with $x , y , z ,$ width, length, height, yaw angle etc.). The dataset consists of recordings for more than 1000 scenes of 20 s duration each. We follow the official training/validation split with 700/150 logs each.

Each 2D radar point consists of its coordinates X, Y , and corresponding measurement $V _ { x } , \ V _ { y } ,$ RCS, pdh0, dynP rop, ambig state and invalid state. Due to limited space, we refer to see [24] and [1] for details about parameters and annotations.

## B. Ground Truth Generation

Labeling ghost targets has long been considered a very challenging task. Since manually labeling ghost targets is very expensive and time-consuming, generating “approximate ground truth” is an emerging solution to such cases. For ground truth generation, the radar points must be divided into positive radar points $P ^ { + }$ (containing only radar points belonging to real objects) and negative points $P ^ { - }$ (noise and ghost points). In prior works, there are two typical schemes to achieve this. In NRF [11], real (or positive) radar points $P ^ { + }$ are defined as all radar points in 3D annotations boxes; the remaining points $P ^ { - }$ belong to ghost or irrelevant objects. Another method [2] projects radar data into a 2D depth image, which is generated by LiDAR points based on Ku et al. [8]. The radar points are regarded as real $P ^ { + }$ when their depth values are within a certain threshold of the corresponding LiDAR point’s depth. The remaining points $P ^ { - }$ are considered to be ghost targets.

![](images/5d95f6452e111f3509cc63cca48ed473f8af089f2ec8facf8b95276aacbf9413.jpg)  
Fig. 5. Schematic diagram for ground truth generation. All radar points are colored in red. $L e f t { : }$ raw input data. Center: the radar points filtered by LiDAR depth map. Right: after further filtering using annotation boxes.

However, we believe that neither method is perfect. The first method may falsely label radar points as ghost targets that are located in some unannotated object, $e . g .$ buildings, and roads. The second LiDAR-based scheme may work effectively in the close range but deteriorate in the far range due to the significantly reduced LiDAR density at increased distance. For more details about LiDAR’s performance in the far range, we refer to [9].

We combine the advantages of both schemes by filtering ghost targets using both LiDAR references and annotation boxes. Fig. 5 shows that only the points which neither lie in annotation boxes nor close to LiDAR points are considered as ghost points $P ^ { - } ,$ . According to the nuScenes team [1], the annotation position mainly depends on LiDAR data. Considering LiDAR and radar’s asynchrony, the radar points belonging to a real object may also be outside the annotated bounding box. Therefore we also follow the tolerance setting as described in [11].

For a fair comparison, we additionally provide the evaluation results using the ground truth estimation from [11] in the next section.

## C. Implementation Details

Since radar points are very sparse and unordered, each single radar sweep only consists of about a hundred points. To obtain denser data, we first merge the data from the five radar sensors, and then merge temporally over several consecutive sweeps. Since annotations are only available for keyframes, we only merge data from a 0.25-second interval to make sure ground truth estimation remains accurate. These are five sweeps of LiDAR (one annotated keyframe plus four preceding non-annotated frames) and three sweeps of merged radar (one annotated keyframe plus two preceding non-annotated frames). Since the radar has no vertical information, the evaluation range is limited to [−100100]m for the X axis, [−100100]m for the Y axis and [−3.5, 3]m for the Z axis. We ignore radar points whose false alarm probability exceeds 75% $( p d h 0 > 3 )$ , or which are labeled as invalid due to certain reasons (invalid state ∈ $\{ 0 x 0 1 , 0 x 0 2 , 0 x 0 3 , 0 x 0 5 , 0 x 0 6 , 0 x 0 7 , 0 x 0 d , 0 x 0 e \} )$

We set the target input number for radar points as $N _ { \alpha } = 1 0 0 0 $ If there are fewer, we will randomly generate duplicates to reach the number. The $N _ { K } = 1 5$ nearest LiDAR points around each radar point are sampled and accumulated; from the remaining LiDAR points, we randomly select 1000 to reach the fixed input number of $N _ { \beta } = 1 6 0 0 0$ . For the original input radar $P _ { \alpha } ,$ the eight parameters, X, $Y , V _ { x } , V _ { y } , R C S , p d h 0 , d y n P r o p ,$ invalid state, and temporal information $\Delta T$ are then fed into the data encoding subnetwork; the input features of LiDAR $P _ { \beta }$ are X, $Y , Z \Delta T$ and intensity I.

![](images/dbd7b2cfb2b97d6a8a47f1a382a9acba76eb5c948a4e11addf707e7fd0129d50.jpg)  
Fig. 6. We evaluate our network’s impact on object detection. Left: the baseline methods, SPN is fed with raw LiDAR, radar, and camera data. Right: radar data is first filtered by our multimodal transformer, then passed to the following SPN.

In the data encoding step, we set $d _ { C } = 6 4 , d _ { F \alpha } = 1 2 8 , d _ { F \beta } =$ 64. Thus, the input feature map $F _ { \alpha }$ has dimension $1 0 0 0 \times 1 9 2$ the feature map $F _ { \beta }$ has dimension 16000 × 128.

The hyperparameters for the architecture of the backbone networks in Fig. 4 is given as follows:

<table><tr><td>Backbone 1 (V1)</td><td>Backbone 2 (V2)</td></tr><tr><td>MMA(256) SA(256)</td><td>MMA(256) MMA(512)</td></tr><tr><td>SA(256) FC(256,0.5)</td><td>MMA(1024) FC(512,0.5)</td></tr><tr><td>FC(128,0.5)</td><td>FC(128, 0.5)</td></tr><tr><td>FC(2)</td><td>FC(2)</td></tr></table>

Here, MMA $, ( d _ { o u t } )$ and $\mathrm { S A } ( d _ { o u t } )$ denote a MMA and SA block with $d _ { o u t }$ as output dimension. The internal dimensions are set to $d _ { q k } = 1 2 8$ for all attention layers. FC(l, dp) represents a fully connected layer with width l and dropout ratio $d p .$ . Features of all attention layers are concatenated before the first fully connected layer.

Our implementation is based on the officially released code of OpenPCDet.<sup>1</sup> For data augmentation, random translation in [−0.5, 0.5], random rotation in $[ - 7 ^ { \circ } , 7 ^ { \circ } ]$ , and random anisotropic scaling in [0.93, 1.07] are applied for robustness. We use the Adam optimizer with a learning rate 0.001 and batch size 16 for 60 epochs of training. All experiments are trained on the train split and evaluated on the val/test split. The model is implemented in PyTorch [12]. All experiments are trained using two NVIDIA P40 graphic cards.

## D. Impact on Object Detection

Next to our main experiment of detecting radar ghost detections, we evaluate the impact of using our filtered radar data on object detection. Since almost all research is focused on object detection based on LiDAR data only, we use Sparse PointNet (SPN) [9], the only recent method that jointly uses radar and LiDAR. Fig. 6 indicates the flow diagram of the comparison experiments. In comparison with the baseline, we just feed filtered radar points to SPN without retraining. We use the metrics of nuScenes object detection benchmark, which evaluates the performance by mAP (mean Average Precision) on different object classes.

![](images/9d05e6b1248f74c1d9cc30c33f31a55a20b79959cd880ee8de1e42048d8c77fb.jpg)  
Fig. 7. Several test examples on nuScenes dataset[1]. In each example, the top image shows the radar points projected onto the front camera image, the bottom left is input raw radar data on a BEV image, the bottom right shows the ghost points detected by our method. Radar points are colored according to their distance to the ego vehicle. In each BEV image, the radar points’ vectors show their Doppler velocity, object annotations are shown as orange boxes, and LiDAR points are shown as a reference in light gray. We manually highlight the critical ghost targets (either too close to the ego vehicle or regarded as moving targets) by red circles. Please zoom in for details.

## VI. RESULTS

## A. Baselines

We compare our results to the most related prior work: NRF [11]. For fair comparisons across different methods, we report results for both ground truth (GT) generation schemes. As shown in Table I, on our GT scheme, our best AUC-ROC is 77.34%, 5.44% higher than NRF. On GT scheme of [11], our best AUC-ROC is 3.71% higher than 82.89%, which is reported as the best optimized result in the baseline’s work.

## B. Ablation Studies

To further understand our network’s behavior during ghost target detection, we investigate three components of both variants. Table I presents the details of the comparative analysis. First, we evaluate version V0 of our model, which only uses self-attention on radar points. Version V0 does not use LiDAR points and already outperforms NRF by a decent margin, indicating that our self-attention based architecture is more suitable than the NRF architecture. When comparing V0 to most other models, one can observe that our model benefits from incorporating LiDAR data as a reference using our MMA module. Second, we compare our data encoding method with the “naïve” encoding approach, which does not use separate encoding spaces for features and coordinates. The results indicate that the detection performance benefits much from transforming the original data into separate feature spaces. Finally, we show that our novel LiDAR sampling methods make the system achieve a better quality than FPS sampling. In general, the V2 framework proves to be better in terms of detection performance.

TABLE I  
QUANTITATIVE COMPARISON BETWEEN OUR APPROACH AND THE BASELINE METHOD [11]. ALL EXPERIMENT ARE EVALUATED ON THE NUSCENES VAL SET
<table><tr><td rowspan="2">Results on Our GT Scheme</td><td colspan="2">Data Encoding</td><td colspan="2">Sampling Method</td><td rowspan="2">AUC-ROC</td></tr><tr><td>Naïve</td><td>Ours</td><td>FPS</td><td>Ours</td></tr><tr><td>NRF(baseline)</td><td>-</td><td>–</td><td>-</td><td>-</td><td>71.90%</td></tr><tr><td>Our V0 (only radar) Our V1</td><td>× √</td><td>√ ×</td><td>– √</td><td>– ×</td><td>73.64% 73.53%</td></tr><tr><td>Our V1</td><td>×</td><td>V</td><td>√</td><td>×</td><td>75.40%</td></tr><tr><td>Our V1</td><td>×</td><td></td><td>×</td><td></td><td></td></tr><tr><td>Our V2</td><td></td><td>√</td><td></td><td>√</td><td>77.02%</td></tr><tr><td></td><td>√</td><td>×</td><td>√</td><td>×</td><td>72.90%</td></tr><tr><td>Our V2 Our V2</td><td>×</td><td>√</td><td>√</td><td>X</td><td>75.01%</td></tr><tr><td></td><td>×</td><td>√</td><td>×</td><td>√</td><td>77.34%</td></tr><tr><td>Results on the GT Scheme of [11]</td><td>Data Encoding</td><td></td><td>Sampling Method</td><td></td><td>AUC-ROC</td></tr><tr><td></td><td>Naïve</td><td>Ours</td><td>FPS</td><td>Ours</td><td></td></tr><tr><td>NRF(baseline)</td><td>–</td><td>–</td><td>–</td><td>–</td><td>82.89%</td></tr><tr><td>Our V1</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Our V2</td><td>× ×</td><td>√ √</td><td>× ×</td><td>√ √</td><td>86.24% 86.60%</td></tr></table>

TABLE II  
WE EVALUATE THE DETECTION PERFORMANCE ON NUSCENES VAL SET. THE METRIC IS MAP AT DIFFERENT DISTANCES FOR CAR, 0 ∼ 10 MEANS IN THE RANGE OF 0 TO 10 METERS, ∼ 20 MEANS IN THE RANGE OF 10 TO 20 METERS, ETC
<table><tr><td>mAP at range(m)</td><td>0~10</td><td>~20</td><td>~30</td><td>~40</td><td>~50</td></tr><tr><td>SPN[9]</td><td>76</td><td>73</td><td>70</td><td>64</td><td>62</td></tr><tr><td>SPN+Ours V1</td><td>76</td><td>71</td><td>70</td><td>63</td><td>62</td></tr><tr><td>SPN+Ours V2</td><td>75</td><td>73</td><td>70</td><td>65</td><td>64</td></tr><tr><td>mAP at range(m)</td><td>50~60</td><td>~70</td><td>~80</td><td>~90</td><td>~100</td></tr><tr><td>SPN[9]</td><td>58</td><td>54</td><td>46</td><td>33</td><td>21</td></tr><tr><td>SPN+Ours V1</td><td>59</td><td>56</td><td>46</td><td>35</td><td>24</td></tr><tr><td>SPN+Ours V2</td><td>61</td><td>57</td><td>47</td><td>33</td><td>24</td></tr></table>

## C. Qualitative Analysis

As a qualitative analysis, Fig. 7 shows several representative results. In most cases, the critical ghost targets, close to the ego vehicle and measured as moving objects, can be effectively and correctly classified. Furthermore, the bottom row of Fig. 3 indicates that our model learns a sensible distribution over attention weights, demonstrating that information is drawn from a broad sample of points.

## D. Analysis of Impact on Object Detection

As the baseline work [11] reported, that filtering radar with NRF will decrease the final object detection performance, we are concerned with our network’s impact on this task. Table II shows that our filter only positively influences the test results beyond the detection range of 40 meters. We assumed that SPN tends to ignore the inaccurate radar data in the close range because the accurate LiDAR points are considerably denser within 40 meters. Nevertheless, in the far range, when LiDAR points are much sparser, radar points play an important role in object localization, and thus the filtering of ghost detections becomes more relevant.

## VII. CONCLUSION

We propose a Multimodal Transformer for radar ghost target detection, and show how to employ self-attention to exchange information in between radar points, and crossmodal attention to infuse information from locally sampled LiDAR points. On nuScenes [1], our method outperforms the baseline [11] by a large margin. Although the results are satisfactory, there is a gap to fully autonomous driving that requires further investigation. Future research intends to apply our multimodal transformer directly to object detection, which might further improve our framework’s detection performance and run-time.

## REFERENCES

[1] H. Caesar et al., “nuScenes: A multimodal dataset for autonomous driving,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2020, pp. 11621–11631.

[2] M. Chamseddine, J. Rambach, D. Stricker, and O. Wasenmüller, “Ghost target detection in 3D radar data using point cloud based deep neural network,” in Proc. Int. Conf. Pattern Recognit. Int. Conf. Pattern Recognit., 2020, pp. 10398–10403.

[3] J. Davis and M. Goadrich, “The relationship between precision-recall and roc curves,” in Proc. Int. Conf. Mach. Learn., 2006, pp. 233–240.

[4] A. Dosovitskiy et al., “An image is worth 16x16 words: Transformers for image recognition at scale,” in Proc. Int. Conf. Learn. Representations, 2021.

[5] M.-H. Guo, J.-X. Cai, Z.-N. Liu, T.-J. Mu, R. R. Martin, and S.-M. Hu, “Pct: Point cloud transformer,” 2020, arXiv:2012.09688.

[6] M. F. Holder, C. Linnhoff, P. Rosenberger, C. Popp, and H. Winner, “Modeling and simulation of radar sensor artifacts for virtual testing of autonomous driving,” in 9, Tagung Automatisiertes Fahren, 2019.

[7] F. Kraus, N. Scheiner, W. Ritter, and K. Dietmayer, “Using machine learning to detect ghost images in automotive radar,” in Proc. IEEE Int. Conf. Intell. Transp. Syst., 2020, pp. 1–7.

[8] J. Ku, A. Harakeh, and S. L. Waslander, “ In defense of classical image processing: Fast depth completion on the CPU,” in Proc. Conf. Comput Robot Vis., 2018, pp. 16–22.

[9] L. Wang and B. Goldluecke, “Sparse-Pointnet : See further in autonomous vehicles,” preprint on ResearchGate, 2021.

[10] C. Liu, S. Liu, C. Zhang, Y. Huang, and H. Wang, “ Multipath propagation analysis and ghost target removal for FMCW automotive radars,” in Proc. IEEE Radar Conf., 2020, pp. 330–334.

[11] F. Nobis, “Autonomous driving: Radar sensor noise filtering and multimodal sensor fusion for object detection with artificial neural net-works” preprint on ResearchGate, 2019.

[12] A. Paszke et al., “Automatic differentiation in PyTorch,” Proc. Conf. Neural Inf. Process. Syst. Workshop, 2017.

[13] R. Prophet, J. Martinez, J.-C. F. Michel, R. Ebelt, I. Weber, and M. Vossiek, “ Instantaneous ghost detection identification in automotive scenarios,” in Proc. IEEE Radar Conf., 2019, pp. 1–6.

[14] C. R. Qi, H. Su, K. Mo, and L. J. Guibas, “ Pointnet: Deep learning on point sets for 3 d classification and segmentation,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2017, pp. 652–660.

[15] C. R. Qi, L. Yi, H. Su, and L. J. Guibas, “ PointNet : Deep hierarchical feature learning on point sets in a metric space,” in Proc. Conf. Neural Inf. Process. Syst., 2017.

[16] O. Rabaste et al., “Around-the-corner radar: Detection and localization of a target in non-line of sight,” in Proc. IEEE Radar Conf., 2017, pp. 842– 0847.

[17] F. Roos, M. Sadeghi, J. Bechter, N. Appenrodt, J. Dickmann, and C. Waldschmidt, “ Ghost target identification by analysis of the doppler distribution in automotive scenarios,” in Proc. Int. Radar Symp., 2017, pp. 1–9.

[18] N. Scheiner et al., “Seeing around street corners: Non-line-of-sight detection and tracking in-the-wild using doppler radar,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2020, pp. 2068–2077.

[19] M. Schneider, “ Automotive radar-status and trends,” in Proc. German Microw. Conf., 2005, pp. 144–147.

[20] S. Shi et al., “PV-RCNN: Point-voxel feature set abstraction for 3D object detection,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2020, pp. 10529–10538.

[21] S. Shi, X. Wang, and H. Li, “ PointRCNN: 3D object proposal generation and detection from point cloud,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit., 2019, pp. 770–779.

[22] Y.-H. H. Tsai, S. Bai, P. P. Liang, J. Z. Kolter, L.-P. Morency, and R. Salakhutdinov, “Multimodal transformer for unaligned multimodal language sequences,” in Meeting Assoc. Comput. Linguistics. NIH Public Access, 2019, vol. 2019, pp. 6558.

[23] A. Vaswani et al., “Attention is all you need,” in Proc. Conf. Neural Inf. Process. Syst., 2017, pp. 5998–6008.

[24] L. Wang, T. Chen, C. Anklam, and B. Goldluecke, “ High dimensional frustum PointNet for 3D object detection from camera, LiDAR, and radar,” in Proc. IEEE Intell. Veh. Symp., 2020, pp. 1621–1628.

[25] B. Yang, R. Guo, M. Liang, S. Casas, and R. Urtasun, “ Radarnet: Exploiting radar for robust perception of dynamic objects,” in Proc. Eur. Conf. Comput. Vis.. Springer, 2020, pp. 496–512.

[26] H. Zhao, L. Jiang, J. Jia, P. Torr, and V. Koltun. Point transformer. 2020, arXiv:2012.09164.