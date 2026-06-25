# FEW-SHOT RADAR SIGNAL RECOGNITION THROUGH SELF-SUPERVISED LEARNINGAND RADIO FREQUENCY DOMAIN ADAPTATION

Zi Huang<sup>1</sup>,<sup>2</sup>, Simon Denman<sup>1</sup>, Akila Pemasiri<sup>1</sup>, Clinton Fookes<sup>1</sup>, Terrence Martin<sup>2</sup>

<sup>1</sup>Queensland University of Technology, Brisbane, Australia <sup>2</sup>Revolution Aerospace, Brisbane, Australia

## ABSTRACT

Radar signal recognition (RSR) plays a pivotal role in electronic warfare (EW), as accurately classifying radar signals is critical for informing decision-making. Recent advances in deep learning have shown significant potential in improving RSR in domains with ample annotated data. However, these methods fall short in EW scenarios where annotated radio frequency (RF) data are scarce or impractical to obtain. To address these challenges, we introduce a self-supervised learning (SSL) method which utilises masked signal modelling and RF domain adaption to perform few-shot RSR and enhance performance in environments with limited RF samples and annotations. We propose a two-step approach, first pre-training masked autoencoders (MAE) on baseband in-phase and quadrature (I/Q) signals from diverse RF domains, and then transferring the learned representations to the radar domain, where annotated data are scarce. Empirical results show that our lightweight self-supervised ResNet1D model with domain adaptation achieves up to a 17.5% improvement in <sup>1</sup>-shot classification accuracy when pre-trained on in-domain signals (i.e., radar signals) and up to a 16.31% improvement when pre-trained on out-of-domain signals (i.e., comm signals), compared to its baseline without using SSL. We also present reference results for several MAE designs and pre-training strategies, establishing a new benchmark for few-shot radar signal classification.

<sup>Index</sup> <sup>Terms</sup>— few-shot learning, self-supervised learning, domain adaptation, radar signal recognition, masked signal modelling, masked autoencoders

## 1. INTRODUCTION

Radar signal recognition (RSR) is a crucial capability in cognitive electronic warfare (EW) [1], where accurate radar signal classification is essential for informed decision-making in the battlefield. Recent progress in deep learning has demonstrated significant potential [2] in addressing RSR sub-tasks, such as automatic modulation classification (AMC) [3] and radar activity segmentation [4], when abundant radio frequency (RF) data are available for model development. However, most existing RSR methods rely heavily on annotated

RF data, which presents a challenge in EW scenarios where mission-specific data are often scarce or difficult to acquire. Moreover, practical EW operations often demand rapid inmission re-training of models on limited data to respond to the rapidly changing threat landscape [1]. This makes few-shot learning a critical yet underexplored area in RSR.

Supervised RF signal recognition has been an active research area over the past decade [3, 5–11]. Previous methods have relied on 2D feature transformations [12–14] to enhance classification performance in supervised settings. More recently, 1D approaches [9, 10, 15] have shown improved performance by capturing fine-grained temporal relationships in I/Q signals, as demonstrated in various signal recognition tasks within the RF domain, such as modulation classification [8, 16], radar signal characterisation [10], RF fingerprinting [17], and radar activity segmentation [4]. While unsupervised methods [18, 19] have been applied to AMC, self-supervised approaches have been more extensively studied in related signal processing domains, such as visual recognition [20, 21], audio recognition [22, 23], bio-signal classification [24, 25], and natural language processing [26]. Notably, masked autoencoders (MAE) have proven to be effective self-supervised learning (SSL) architectures for time series classification [27] and representation learning in related tasks [23, 24, 28, 29]. Due to their success, MAE-based methods have been adapted in recent work [30, 31] for RF emitter identification, particularly when training samples are limited. However, selfsupervised approaches for RSR remain largely unexplored, likely due to the scarcity of publicly available radar datasets [2, 10]. Moreover, existing work in RSR has yet to explore SSL with RF domain adaptation.

In this work, we introduce a flexible two-step SSL approach that leverages masked signal modelling (MSM) and domain adaptation for few-shot RSR. Our proposed method pre-trains models on baseband I/Q signals with diverse characteristics from various RF domains. We then apply fewshot transfer learning to adapt pre-trained models to the radar domain using limited training samples. Our main contributions are as follows: (i) we propose a modular and effective SSL architecture using different MSM strategies to enhance radar signal classification performance in few-shot settings;

(ii) we introduce RF domain adaptation for self-supervised pre-training, enabling effective adaptation to the radar domain with limited data; and (iii) we release our SSL datasets<sup>1</sup> accompanied by a new benchmark for few-shot radar signal classification. To the best of our knowledge, the integration of domain adaptation of RF signals with varying sequence lengths and sampling frequencies from diverse RF domains into the radar domain has not been explored previously.

## 2. PROPOSED METHOD

## 2.1. Two-Step Few-Shot Learning

Our proposed SSL approach comprises two sequential steps. First, annotation-free pre-training of a masked autoencoder is conducted on a source RF domain (i.e., radar, comm, or a mixture of both). Then, the pre-trained encoder is fine-tuned on the target radar domain using a limited amount of annotated data. We follow the modular encoder-decoder paradigm [32] to construct our autoencoder as shown in Fig. l. In the pre-training step, we utilise asymmetric masked autoencoding [21] whereby the model operates on a partially observed I/Q signal in the presence of additive white Gaussian noise (AWGN). We pre-train the model to reconstruct the original signal using a sample-wise similarity loss function [4]. This process is considered self-supervised as no annotations are required for the reconstruction task. After pre-training, we replace the decoder with a linear probing classifier consisting of a flatten operation followed by a simple fully connected layer. We fine-tune the classifier on the target domain with a small amount (i.e., a few shots) of annotated RF data before evaluating it on a large test set.

## Lightweight Autoencoders for 1/Q Signals

We implement several autoencoders to examine their effectiveness in self-supervised RSR. Specifically, we focus our experiments on lightweight models, prioritising rapid re-training and computational efficiency as they are critical considerations for adaptability in EW [ l]. We implement a ResNetlD [30], a two-stage MS-TCN [4, 33], and WaveNet [34, 35] as our autoencoders. Notably, being a well established baseline, WaveNet [35] demonstrates exceptional performance in RF signal reconstruction, surpassing more complex and recent transformer-based models [35]. In our experiments, pre-training of MS-TCN and WaveNet are conducted in an end-to-end manner as they do not have independent encoders and decoders. As such, the linear probing classifier is appended to these models during fine-tuning. For our SSL benchmark, we use the $\ell _ { 1 }$ regression loss to compute sample-wise similarity during pre-training, and the categorical cross-entropy loss for fine-tuning the classifier.

![](images/42381452f109adb229f280f520e03003641be3be98ea514f4102948c84a4ea9f.jpg)  
Fig. Proposed two-step SSL architecture. The encoder is pre-trained on various RF domains using the most optimal masking strategy, and fine-tuning is conducted on in-domain radar data using a linear probing classifier.

## 2.3. Masked Signal Modelling

Masked signal modelling (MSM) is conceptually similar to masked image modelling (MIM) [28, 36], which has gained popularity as a simple and effective SSL approach in the computer vision domain. Our approach utilises the proxy task of I/Q signal reconstruction, training a model to reconstruct intentionally corrupted signals. By applying this process across a large corpus of examples, the model learns the salient representations necessary for accurate signal reconstruction. Similar to MIM, MSM involves several key design considerations, including the masking strategy $S _ { \mathrm { { m } } } ,$ masking ratio $R _ { \mathrm { m } } .$ and model design. While the choice of model design is often influenced by external factors such as computational and memory requirements, $S _ { \mathrm { m } }$ and $R _ { \mathrm { m } }$ have a more explicit impact on the quality of pre-training [28].

We introduce several masking strategies for MSM, including random zero-masking (strat. A), random block zeromasking (strat. B), random noise-masking (strat. C), and block noise-masking (strat. D). Random masking involves modifying I/Q samples with mask values (i.e., either zero or noise), while block masking randomly obscures a continuous segment of the I/Q sequence (analogous to intentional interference in an EW setting). The extent of masking is governed by $R _ { \mathrm { m } }$ with higher values masking a larger percentage of the signal and thus making the reconstruction task more challenging. As shown by MIM [28], random masking promotes the learning of local relationships between samples, while block masking promotes the learning of broader, global patterns from the data. Our signal masking process is formalised as

$$
s _ { \mathrm { m } } = \left\{ \begin{array} { l l } { s \otimes 0 _ { \{ X < R _ { \mathrm { m } } \} } } & { \mathrm { i f ~ z e r o - m a s k i n g , } } \\ { s \oplus \hat { n } _ { \{ X < R _ { \mathrm { m } } \} } } & { \mathrm { i f ~ n o i s e - m a s k i n g , } } \\ { s } & { \mathrm { i f ~ n o ~ m a s k i n g , } } \end{array} \right.\tag{l}
$$

$$
\hat { n } \sim \mathcal { N } ( \mu _ { \mathrm { t r a i n } } , \sigma _ { \mathrm { t r a i n } } ^ { 2 } ) , \quad X \sim \mathcal { U } ( 0 , 1 ) , \quad R _ { \mathrm { m } } \in [ 0 , 1 ] ,\tag{2}
$$

where and $s _ { \mathrm { m } }$ denote the original and masked I/Q sequences respectively, ® and EB denote sample-wise multiplication and

Table Summary of RF signal classification datasets.
<table><tr><td>Dataset</td><td>Type</td><td>Frames</td><td>Size</td><td> $N _ { \mathbf { c l s } }$ </td><td> $t _ { \mathrm { r e s } }$  (µs)</td></tr><tr><td>RadioML [3] DeepRadar [9] RadarComm [8] RadChar-SSL RadChar-nShot</td><td>Comm Radar Mixed Radar Radar</td><td>255,590 782,000 125,361 500,000 205n</td><td>1024 1024 128 512 512 512</td><td>24 23 6555</td><td>1 0.01 0.1 0.3 0.3</td></tr></table>

addition respectively, and n denotes random noise sampled using statistics computed from the training data distribution ofthe source domain.

## 2.4. RF Datasets for Domain Adaption

We explore domain adaptation by applying MSM to 1/Q signals from diverse RF domains, including telecommunications and radar signals. Our approach involves pre-training, without annotations, MAEs on four diverse RF datasets: RadioML [3], DeepRadar [9], RadarComm [8], and RadChar-SSL [10]. We then perform few-shot transfer learning to fine-tune each pre-trained model on RadChar-nShot and evaluate performance on a separate test set (RadChar-Eval) derived from RadChar [ l 0]. Here, n represents the number of shots where 1-shot corresponds to precisely 205 frames (i.e., representing 1 unique training example per signal class and SNR level), while 10-shot consists of 2, 050 frames. We use only 10% of RadioML for pre-training to ensure comparable dataset sizes across all pre-training datasets. Table l provides a summary of the key characteristics of each dataset.

## 3. EXPERIMENTS

## Training Details

We perform pre-training, fine-tuning, and model evaluation on a single Nvidia Tesla A100 GPU. All models are trained with the Adam optimiser, where constant learning rates of 0.001 and 0.0001 are used for self-supervised pre-training and fine-tuning, respectively. For pre-training, we train each model for 100 epochs with early stopping based on validation loss with a 3-step patience, using a fixed 70-20-10 trainvalidation-test split for each dataset. For fine-tuning on limited frames, we train each model for the full 100 epochs with the pre-trained encoder weights frozen for the first 10 epochs. To maintain an even class distribution, no validation split is considered during fine-tuning. We establish baseline few-shot performance for each model using the same model configuration as thatused in fine-tuning, but without the pre-trained weight initialisation. A fixed batch size of 128 is used for pretraining, while a batch size of 8 is used for both fine-tuning and baseline training. To improve generalisation and training stability, we standardise input signals with the mean and variance sampled from the training set of the respective RF domain. All models are evaluated on the RadChar-Eval dataset.

![](images/f2bba3ead52e0ecac919a943ce10b9b54e0af07686267d9621befb09b6e9e120.jpg)  
(a) RadChar-SSL (Radar)

![](images/88231feeb7819a651fed20efec16c607d1c84bcc1715166e19ab8dd8990b9c13.jpg)  
(b) DeepRadar (Radar)

![](images/a04ca23aff0d51a04a129e17f7f16e68e86979999e16b212c87044c948fc4fba.jpg)  
(c) RadarComm (Mixed)

![](images/5ca97aa47372b6b35fda0119bd0e59af6d3b07634c2d80027a7b7a5afc284c95.jpg)  
(d) RadioML (Comm)  
Impact of masking strategies on the 1-shot classification performance of ResNetlD, pre-trained across different RF domains (a)–(d), and evaluated on RadChar-Eval.

## 3.2. Few-Shot Radar Signal Recognition

We establish a novel benchmark for few-shot RSR through the following experiments: (i) evaluating different MAEs; (ii) evaluating the impact ofSSL on test performance across different SNR settings; (iii) evaluating different masking strategies; and (iv) evaluating the effectiveness of self-supervised pre-training on signals from different domains for fewshot signal classification. We evaluate the test performance of each linear probing classifier using classification accuracy and the macro Fl score. The test performance of each classifier is compared to its baseline (w/o SSL), where the model is trained from scratch without self-supervised pre-training.

Table 2 presents a summary of our results. The classification performance corresponding to the optimal selection of $S _ { \mathrm { m } }$ and $R _ { \mathrm { m } }$ used during pre-training is shown for each model. Here, we observe that fine-tuned models that are pre-trained on data from the same RF domain (i.e., RadChar) yield the greatest improvement in test performance when compared to their respective baselines. This performance gain is most substantial in the 1-shot setting, which is the most challenging with the fewest labels available. The improvement diminishes as the number of annotated frames used in fine-tuning increases, as reflected by the 17.5%, 6.3%, and 4.3% increases in 1-shot, 5-shot, and 10-shot performance for ResNet1D, respectively. Separately, we observe that MS-TCN's baseline performance is relatively low in the 1-shot setting, likely due to its larger model size (33.6 million parameters). This model requires more fine-tuning samples (Table 2) to achieve a similar performance compared to ResNet1D (2.7 million parameters) and WaveNet (1 million parameters).

Table <sub>2.</sub> Comparison of optimal few-shot radar classification performance results on the RadChar-Eval dataset.
<table><tr><td rowspan="2">Model</td><td rowspan="2">Pre-Training w/SSL</td><td colspan="4">1-Shot Eval. (Best)</td><td rowspan="2"></td><td colspan="3">5-Shot Eval. (Best)</td><td rowspan="2"> $S _ { \mathbf { m } }$ </td><td colspan="3">10-Shot Eval. (Best)</td></tr><tr><td> $S _ { \mathbf { m } }$ </td><td> $R _ { \mathbf { m } }$ </td><td>Acc. (%) F1 (%)</td><td> $S _ { \mathbf { m } }$ </td><td> $R _ { \mathbf { m } }$ </td><td>Acc. (%)</td><td>F1 (%)</td><td> $R _ { \mathbf { m } }$ </td><td>Acc. (%)</td><td>F1 (%)</td></tr><tr><td rowspan="6">ResNet1D</td><td>RadChar-SSL</td><td>A</td><td>0.7</td><td>75.06</td><td>72.32</td><td>A</td><td>0.7</td><td>79.76</td><td>77.76</td><td></td><td>0.8</td><td>79.86</td><td>77.73</td></tr><tr><td>DeepRadar</td><td>AD</td><td>0.4</td><td>68.32</td><td>65.35</td><td></td><td>0.2</td><td>76.15</td><td>73.91</td><td>ABBB</td><td>0.2</td><td>76.87</td><td>74.59</td></tr><tr><td>RadarComm</td><td></td><td>0.7</td><td>70.03</td><td>66.98</td><td></td><td>0.8</td><td>77.21</td><td>75.00</td><td></td><td>0.7</td><td>78.05</td><td>75.82</td></tr><tr><td>RadioML</td><td>A</td><td>0.1</td><td>74.30</td><td>71.81</td><td>BCA</td><td>0.1</td><td>77.35</td><td>75.16</td><td></td><td>0.7</td><td>78.08</td><td>75.96</td></tr><tr><td>None</td><td></td><td></td><td>63.88</td><td>60.50</td><td>1</td><td></td><td>75.02</td><td>72.66</td><td>1</td><td></td><td>76.57</td><td>74.20</td></tr><tr><td></td><td></td><td>0.7</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0.9</td><td></td><td>79.40</td></tr><tr><td rowspan="6">MS-TCN</td><td>RadChar-SSL DeepRadar</td><td>ACAA</td><td>0.6</td><td>72.62 52.73</td><td>70.13 50.14</td><td></td><td>0.9 0.6</td><td>81.12 70.29</td><td>79.27 67.66</td><td></td><td>0.7</td><td>81.27 74.86</td><td>72.53</td></tr><tr><td>RadarComm</td><td></td><td>0.9</td><td>68.40</td><td>65.72</td><td></td><td>0.7</td><td>76.13</td><td>73.89</td><td></td><td>0.9</td><td>78.25</td><td>76.14</td></tr><tr><td>RadioML</td><td></td><td>0.8</td><td>64.76</td><td></td><td></td><td></td><td>75.36</td><td></td><td></td><td>0.8</td><td>77.89</td><td>75.75</td></tr><tr><td>None</td><td>–</td><td>-</td><td>44.00</td><td>61.95 40.81</td><td>ACＢＡ -</td><td>0.7</td><td>66.49</td><td>72.96 63.69</td><td>ACBＡ -</td><td>一</td><td>76.47</td><td>74.17</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>RadChar-SSL</td><td></td><td>0.6</td><td>73.07</td><td>70.63</td><td>A</td><td>0.8</td><td>82.00</td><td>80.26</td><td>AＡBＡ</td><td>0.8</td><td>83.37</td><td>81.64</td></tr><tr><td rowspan="5">WaveNet</td><td>DeepRadar</td><td></td><td>0.2</td><td>62.64</td><td>59.86</td><td></td><td>0.8</td><td>73.80</td><td>71.30</td><td></td><td>0.8</td><td>76.46</td><td>74.25</td></tr><tr><td>RadarComm</td><td></td><td>0.8</td><td>67.09</td><td>64.43</td><td></td><td>0.9</td><td>75.79</td><td>73.53</td><td></td><td>0.9</td><td>77.83</td><td>75.70</td></tr><tr><td>RadioML</td><td>ADDB</td><td>0.9</td><td>64.84</td><td>61.62</td><td>ABB</td><td>0.9</td><td>77.40</td><td>75.24</td><td></td><td>0.9</td><td>78.66</td><td>76.57</td></tr><tr><td>None</td><td></td><td></td><td>64.04</td><td>60.93</td><td></td><td></td><td>75.89</td><td>73.55</td><td>一</td><td></td><td>77.21</td><td>75.10</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

![](images/a47e592101c94da47ed38b79c4889bc9f597ef158dc12c018f029f78c4316ebc.jpg)  
(a) ResNet (n <sub>=</sub> 1)

![](images/5efa04f21ed3bd626275b798b3ffce472ca7e44025cec221acb7644396c0dca3.jpg)  
(b) MS-TCN (n <sub>=</sub> 1)

![](images/6bdf24c162755139443178778939eec4842e9117b918cf8e8f3de67573d46c6b.jpg)  
(c) WaveNet (n <sub>=</sub> 1)

![](images/4518b0a8d5f08f9953f326740dbd99fa68d0da92101d8c65511367da88cbc871.jpg)  
(d) WaveNet (n <sub>=</sub> 10)  
Fig. <sub>3.</sub> n-shot classification performance of different models on RadChar-Eval. The optimal masking technique $( S _ { \mathrm { m } } , R _ { \mathrm { m } } )$ for each pre-training domain is given in Table 2.

The benefit of SSL on model performance is highly dependent on SNR. Notably, models tend to benefit the most from pre-training when evaluating in moderate to high SNR levels (Fig. 3). We hypothesise that signal features (e.g., number of pulses, pulse width) become more distinguishable at higher SNRs, enabling models to learn salient information through reconstruction. In contrast, at lower SNRs, random noise dominates, making reconstruction more challenging. In the most demanding fine-tuning configuration (i.e., 1-shot), ResNetlD shows a performance boost ranging from 11.3% to 25.7% as SNR increases from -20 to 20 dB when pretrained on RadChar-SSL, whereas WaveNet's improvement is more modest (3.5% to 6.4 %) when compared to their respective baselines without SSL. WaveNet employs dilated convolutions, which provide a larger receptive field compared to ResNetlD. Consequently, WaveNet may benefit less from MSM, as the masking process may not present enough of a challenge for reconstruction. This is reflected in WaveNet's preference for higher masking ratios (Table 2). Our results (Table 2) also suggest that classification performance saturates at around 10 shots for both in-domain and out-of-domain fine-tuning. For instance, the classification accuracy of the in-domain pre-trained WaveNet improves from 73.07% (1- shot) to 82% (5-shot). However, performance improves only marginally from 82% to 83.37% between the 5-shot and 10- shot setting, respectively. These findings are consistent with a related study on SSL for RF fingerprinting of five unique emitters [30], which reported test accuracy saturation at approximately 2, 500 frames on a private RF dataset.

The optimal masking strategy for classification performance depends on the model and the pre-training domain. For ResNetlD (Fig. 2), random zero-masking (strat. A) with lower masking ratios (below 0.4) performs best when pre-training on RadioML and DeepRadar, while the same strategy with a higher masking ratio (above 0.7) is more beneficial when pre-training on RadChar-SSL. Random block noise-masking (strat. D) with a higher masking ratio (above 0.7) performs best when pre-training on the mixed RF domain RadarComm. While self-supervised pre-training on out-ofdomain RF data using the optimal masking strategy improves performance across various few-shot settings (Table 2), the effectiveness of RF domain adaptation depends on severa key factors, particularly the extent of the domain shift between datasets. We hypothesise that differences in sampling rates (i.e., temporal resolution) between datasets affect how models learn the temporal relationships in the I/Q sequence. Pre-training on signals (Table l) with higher temporal resolution $\left( t _ { \mathrm { r e s } } \right)$ may lead to the model learning features that are less relevant when fine-tuned on signals with lower sampling rates, and vice versa. While resampling the source domain to match the target domain is possible, it reduces signal information and can introduce aliasing, especially when the original signal has limited I/Q samples, such as in RadarComm (Table 1). Conversely, upsampling requires interpolation, which may not accurately capture the characteristics of the original signal, potentially leading to bias and overfitting.

Differences in domain-specific characteristics and the number of signal classes $( N _ { \mathrm { c l s } } )$ in the source and target domains (Table l) can have a significant impact on fine-tuning performance. This is highlighted by comparing in-domain results (RadChar-SSL) with out-of-domain results in Fig. 3. Performance improvements from SSL are most notable for RadChar-SSL and RadarComm, where the number of signal classes (6 and 5) and temporal resolution (0.1 and 0.3) are most similar (Table 1). In contrast, DeepRadar and RadioML contain substantially more RF classes than RadChar. Furthermore, the signal features from DeepRadar and RadioML deviate significantly from the target domain. For example, the temporally smooth telecommunications signals from RadioML and the challenging low probability of intercept (LPI) radar classes (e.g., Px codes) in DeepRadar do not appear in the target domain, which may lead to over-regularisation and the reduced efectiveness of fine-tuning.

To further evaluate the quality of SSL for RSR, we apply t-SNE to analyse how well models discriminate between radar classes during fine-tuning. For consistency, we first apply PCA to reduce the large pre-trained encoder embeddings to 50 dimensions before using t-SNE to visualise the reduced embeddings in a 2D feature space. Our results (Fig. 4) indicate that self-supervised pre-training with the optimal masking strategy enhances generalisation, allowing for effective adaptation from different RF domains. This is evident from the more compact clusters observed in Fig. 4(c)-(f) compared to Fig. 4(a) under the 1-shot configuration. In contrast, ResNetlD trained without SSL exhibits a less distinct decision boundary between Polyphase and Frank, as both classes are polyphase-coded waveforms with similar intra-pulse characteristics [10], making them difficult to distinguish. Furthermore, increasing the amount of annotated data for ResNetlD without S SL to a 1 0-shot setting, as illustrated in Fig. 4(b ), only marginally improves the quality of inter-class separation. This observation is also reflected in Table 2, where models fine-tuned using their respective domain-optimal masking strategy in a 1-shot setting achieve performance comparable to models without SSL in a 10-shot setting.

## Ablation Study

We examine the impact of various design considerations for few-shot RSR. As discussed in Section 3.2, the choice of $S _ { \mathrm { m } }$ and $R _ { \mathrm { m } }$ influences SSL performance and, in turn, fine-tuning and test performance. Although no particular masking strategy consistently outperformed others across our experiments, we found that the masking ratio played a more important role in determining test performance (Table 2). W hile a small batch size coupled with a low learning rate generally benefits fine-tuning, we observed that freezing the model weights for a few epochs provided a slight improvement (less than 5%) in test performance. This effect was consistent for models pretrained on both in-domain and out-of-domain data. We also explored $\ell _ { 2 }$ loss for pre-training, but we observed no meaningful improvements over $\ell _ { 1 }$ loss in our experiments.

![](images/a31d99c23379ce7220c5759e3d3735ad03c8e3b202a885d28a8d6e3cb5cbc8bf.jpg)  
(a) Without SSL (1-shot)

![](images/6597c903fa4c27e83cdba745f02b6739a6bab81c89ea40e10e42ab66a4344cd1.jpg)  
(b) Without SSL (10-shot)

![](images/30fee593ce2f094a0355dcc06eced54b12afd63c2c8f1bd12b4302d8ff05f196.jpg)

![](images/40aa236921ab91839cca83f90add62e7e92dd4a8c8a7cef0c0a329b042e8a9a8.jpg)

(c) RadChar-SSL (A, 0.7)  
![](images/7b8dc696d26caaca4891a36c1d1fd3de2985f8323db286b2fdbcb36481539eef.jpg)  
(e) RadarComm (D, 0.7)

(d) DeepRadar (A, 0.4)  
![](images/504b386ce5033c6e5ae124cdd49106624d6537853d6b6cd61f0c3a32eec2dede.jpg)  
(f) RadioML (A, 0.1)  
Fig. t-SNE results of 1-shot fine-tuned ResNetlD encoder embeddings using the respective domain-optimal masking strategy $( S _ { \mathrm { m } } , R _ { \mathrm { m } } )$ 10, 000 I/Q frames randomly selected from RadChar-Eval above 0 dB SNR are shown.

## 4. CONCLUSION

In this paper, we introduced MSM as an efective SSL method for few-shot RSR. We also demonstrated the viability of RF domain adaptation for enhancing signal classification performance when no target domain data was used for pre-training. Our results show that by optimally designing the masking method during pre-training, fine-tuned models can achieve significant performance improvements, particularly in moderate to high SNR settings. This is demonstrated by ResNetlD, which achieved a boost in classification accuracy of 17.5% when pre-trained on in-domain signals (RadChar-SSL), and 16.31% when pre-trained on out-of-domain data (RadioML), compared to its 1-shot baseline without SSL. In future work, additional downstream tasks may be explored to evaluate SSL and RF domain adaptation in a real-world setting.

## 5. REFERENCES

[1] Karen Haigh and Julia Andrusenko, Cognitive Electronic Warfare: An Artificial Intelligence Approach, Artech House, 2021.

[2] Zhe Geng, He Yan, Jindong Zhang, and Daiyin Zhu, “Deep Learning for Radar: A Survey,” IEEE Access, vol. 9, pp. 141800–141818, 2021.

[3] Timothy J. O’Shea, Tamoghna Roy, and T. Charles Clancy, “Over-the-Air Deep Learning Based Radio Signal Classification,” IEEE Journal of Selected Topics in Signal Processing, vol. 12, no. 1, pp. 168–179, 2018, IEEE.

[4] Zi Huang, Akila Pemasiri, Simon Denman, Clinton Fookes, and Terrence Martin, “Multi-stage Learning for Radar Pulse Activity Segmentation,” in ICASSP 2024- 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2024, pp. 7340–7344.

[5] Andres Vila, Donna Branchevsky, Kyle Logue, Sebastian Olsen, Esteban Valles, Darren Semmen, Alex Utter, and Eugene Grayver, “Deep and Ensemble Learning to Win the Army RCO AI Signal Classification Challenge,” in Proceedings of the 18th Python in Science Conference, 2019, pp. 21–26.

[6] Thien Huynh-The, Quoc-Viet Pham, Toan-Van Nguyen, Thanh Thi Nguyen, Rukhsana Ruby, Ming Zeng, and Dong-Seong Kim, “Automatic Modulation Classification: A Deep Architecture Survey,” IEEE Access, vol. 9, pp. 142950– 142971, 2021.

[7] Raied Caromi, Alex Lackpour, Kassem Kallas, Thao Nguyen, and Michael Souryal, “Deep Learning for Radar Signal Detection in the 3.5 GHz CBRS Band,” in 2021 IEEE International Symposium on Dynamic Spectrum Access Networks (DySPAN). IEEE, 2021, pp. 1–8.

[8] Anu Jagannath and Jithin Jagannath, “Multi-task Learning Approach for Automatic Modulation and Wireless Signal Classification,” in ICC 2021-IEEE Inter national Conference on Communications. 2021, pp. 1–7, IEEE

[9] Victoria Clerico, Jorge Gonzalez-L´ opez, Gady Agam, and Jes´ us Grajal, “LSTM´ Framework for Classification of Radar and Communications Signals,” in 2023 IEEE Radar Conference (RadarConf23). IEEE, 2023, pp. 1–6.

[10] Zi Huang, Akila Pemasiri, Simon Denman, Clinton Fookes, and Terrence Martin, “Multi-task Learning For Radar Signal Characterisation,” in 2023 IEEE In ternational Conference on Acoustics, Speech, and Signal Processing Workshops (ICASSPW), 2023, pp. 1–5.

[11] Akila Pemasiri, Zi Huang, Fraser Williams, Ethan Goan, Simon Denman, Terrence Martin, and Clinton Fookes, “Automatic Radar Signal Detection and FFT Estimation using Deep Learning,” in 2024 17th International Conference on Signal Processing and Communication System (ICSPCS), 2024, pp. 1–5.

[12] Tim O’Shea, Tamohgna Roy, and T Charles Clancy, “Learning Robust General Radio Signal Detection Using Computer Vision Methods,” in 2017 51st asilomar conference on signals, systems, and computers. IEEE, 2017, pp. 829–832.

[13] Thien Huynh-The, Van-Sang Doan, Cam-Hao Hua, Quoc-Viet Pham, Toan-Van Nguyen, and Dong-Seong Kim, “Accurate LPI Radar Waveform Recognition with CWD-TFA for Deep Convolutional Network,” IEEE Wireless Communications Letters, vol. 10, no. 8, pp. 1638–1642, 2021.

[14] Kyle Logue, Esteban Valles, Andres Vila, Alex Utter, Darren Semmen, Eugene Grayver, Sebastian Olsen, and Donna Branchevsky, “Expert RF Feature Extraction to Win the Army RCO AI Signal Classification Challenge,” in Proceedings of the 18th Python in Science Conference, 2019, pp. 8–14.

[15] Yu Tian, Ahmed Alhammadi, Abdullah Quran, and Abubakar Sani Ali, “A Novel Approach to WaveNet Architecture for RF Signal Separation with Learnable Dilation and Data Augmentation,” in 2024 IEEE International Conference on Acoustics, Speech, and Signal Processing Workshops (ICASSPW). IEEE, 2024, pp. 79– 80.

[16] Yi Shi, Kemal Davaslioglu, Yalin E Sagduyu, William C Headley, Michael Fowler, and Gilbert Green, “Deep Learning for RF Signal Classification in Unknown and Dynamic Spectrum Environments,” in 2019 IEEE International Symposium on Dynamic Spectrum Access Networks (DySPAN). IEEE, 2019, pp. 1–10.

[17] Weijie Zhang, Feng Shi, Qianyun Zhang, Yu Wang, Lantu Guo, Yun Lin, and Guan Gui, “Few-Shot Specific Emitter Identification Leveraging Neural Architecture Search and Advanced Deep Transfer Learning,” IEEE Internet of Things Journal, 2024.

[18] Timothy J. O’Shea, Johnathan Corgan, and T. Charles Clancy, “Unsupervised Representation Learning of Structured Radio Communication Signals,” in 2016 First International Workshop on Sensing, Processing and Learning for Intelligent Machines (SPLINE). 2016, pp. 1–5, IEEE.

[19] Afan Ali and Fan Yangyu, “Unsupervised Feature Learning and Automatic Modulation Classification Using Deep Learning Model,” Physical Communication, vol. 25, pp. 75–84, 2017.

[20] Hangbo Bao, Li Dong, Songhao Piao, and Furu Wei, “BEiT: BERT Pre-training of Image Transformers,” arXiv preprint arXiv:2106.08254, 2021.

[21] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollar, and Ross Gir-´ shick, “Masked Autoencoders Are Scalable Vision Learners,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 16000–16009.

[22] Po-Yao Huang, Hu Xu, Juncheng Li, Alexei Baevski, Michael Auli, Wojciech Galuba, Florian Metze, and Christoph Feichtenhofer, “Masked Autoencoders That Listen,” Advances in Neural Information Processing Systems, vol. 35, pp. 28708– 28720, 2022.

[23] Yuan Gong, Cheng-I Lai, Yu-An Chung, and James Glass, “SSAST: Self-Supervised Audio Spectrogram Transformer,” in Proceedings of the AAAI Conference on Artificial Intelligence, 2022, vol. 36, pp. 10699–10709.

[24] Hsiang-Yun Sherry Chien, Hanlin Goh, Christopher M Sandino, and Joseph Y Cheng, “MAEEG: Masked Auto-Encoder for EEG Representation Learning,” arXiv preprint arXiv:2211.02625, 2022.

[25] Ran Liu, Ellen L Zippi, Hadi Pouransari, Chris Sandino, Jingping Nie, Hanlin Goh, Erdrin Azemi, and Ali Moin, “Frequency-Aware Masked Autoencoders for Multimodal Pretraining on Biosignals,” arXiv preprint arXiv:2309.05927, 2023.

[26] Jacob Devlin Ming-Wei Chang Kenton and Lee Kristina Toutanova, “BERT: Pre-Training of Deep Bidirectional Transformers for Language Understanding,” in Proceedings of naacL-HLT, 2019, vol. 1, p. 2.

[27] George Zerveas, Srideepika Jayaraman, Dhaval Patel, Anuradha Bhamidipaty, and Carsten Eickhoff, “A Transformer-Based Framework for Multivariate Time Series Representation Learning,” in Proceedings of the 27th ACM SIGKDD conference on knowledge discovery & data mining, 2021, pp. 2114–2124.

[28] Zhenda Xie, Zheng Zhang, Yue Cao, Yutong Lin, Jianmin Bao, Zhuliang Yao, Qi Dai, and Han Hu, “SimMIM: A Simple Framework for Masked Image Modeling,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 9653–9663.

[29] Yutong Bai, Zeyu Wang, Junfei Xiao, Chen Wei, Huiyu Wang, Alan L Yuille, Yuyin Zhou, and Cihang Xie, “Masked Autoencoders Enable Efficient Knowledge Distillers,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2023, pp. 24256–24265.

[30] Keju Huang, Hui Liu, Pengjiang Hu, et al., “Deep Learning of Radio Frequency Fingerprints from Limited Samples by Masked Autoencoding,” IEEE Wireless Communications Letters, 2022.

[31] Zhisheng Yao, Xue Fu, Lantu Guo, Yu Wang, Yun Lin, Shengnan Shi, and Guan Gui, “Few-Shot Specific Emitter Identification Using Asymmetric Masked Auto-Encoder,” IEEE Communications Letters, 2023.

[32] Geoffrey E Hinton and Ruslan R Salakhutdinov, “Reducing the Dimensionality of Data with Neural Networks,” science, vol. 313, no. 5786, pp. 504–507, 2006.

[33] Yazan Abu Farha and Jurgen Gall, “MS-TCN: Multi-Stage Temporal Convolutional Network for Action Segmentation,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2019, pp. 3575–3584.

[34] Aaron Van Den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals, Alex Graves, Nal Kalchbrenner, Andrew Senior, Koray Kavukcuoglu, et al., “WaveNet: A Generative Model for Raw Audio,” arXiv preprint arXiv:1609.03499, vol. 12, 2016.

[35] Tejas Jayashankar, Binoy Kurien, Alejandro Lancho, Gary CF Lee, Yury Polyanskiy, Amir Weiss, and Gregory W Wornell, “The Data-Driven Radio Frequency Signal Separation Challenge,” in Proc. IEEE Int. Conf. Acoust., Speech, Signal Process.(ICASSP), 2024.

[36] Mark Chen, Alec Radford, Rewon Child, Jeffrey Wu, Heewoo Jun, David Luan, and Ilya Sutskever, “Generative Pretraining from Pixels,” in International conference on machine learning. PMLR, 2020, pp. 1691–1703.