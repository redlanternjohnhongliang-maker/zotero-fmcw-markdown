# MCROOD: MULTI-CLASS RADAR OUT-OF-DISTRIBUTION DETECTION

Sabri Mustafa Kahya<sup>⋆</sup> Muhammet Sami Yavuz<sup>⋆†</sup> Eckehard Steinbach<sup>⋆</sup>

<sup>⋆</sup>Technical University of Munich, School of Computation, Information and Technology, Department of Computer Engineering, Chair of Media Technology, Munich Institute of Robotics and Machine Intelligence (MIRMI) <sup>†</sup>Infineon Technologies AG

## ABSTRACT

Out-of-distribution (OOD) detection has recently received special attention due to its critical role in safely deploying modern deep learning (DL) architectures. This work proposes a reconstruction-based multi-class OOD detector that operates on radar range doppler images (RDIs). The detector aims to classify any moving object other than a person sitting, standing, or walking as OOD. We also provide a simple yet effective pre-processing technique to detect minor human body movements like breathing. The simple idea is called respiration detector (RESPD) and eases the OOD detection, especially for human sitting and standing classes. On our dataset collected by 60GHz short-range FMCW Radar, we achieve AUROCs of 97.45%, 92.13%, and 96.58% for sitting, standing, and walking classes, respectively. We perform extensive experiments and show that our method outperforms state-of-the-art (SOTA) OOD detection methods. Also, our pipeline performs 24 times faster than the second-best method and is very suitable for real-time processing.

Index Terms— Out-of-distribution detection, 60GHz FMCW radar, deep neural networks

## 1. INTRODUCTION

Modern deep learning architectures have shown remarkable results on several problems by making closed-world assumptions. However, this assumption is unrealistic because a model may be exposed to a sample that is out of the training distribution in an open-world setting. In this case, the model assigns the sample to one of the training classes with a high prediction probability. For safety-critical applications such as medical and autonomous driving, overconfident predictions may cause catastrophic failures. Therefore, to address this issue, in recent years, many OOD detection strategies [1–7] have been revealed. Usually, the methods consider the image or video data domain. However, the same problem also exists for various kinds of sensor data domains like radar.

Radars are robust to environmental conditions like lighting, smoke, and rain and preserve privacy. Thanks to these advantages, radars have gained interest in both industry and academia. Even though many different applications, such as gesture recognition [8], people counting [9], and vital sign estimation [10], have been developed using radars, few of them emphasize the OOD detection problem. In this study, we aim to develop an OOD detector that operates on RDIs of 60GHz L-shaped FMCW Radar. It tries to classify any moving object other than a person sitting, standing, or walking as OOD.

Formally, we propose a novel DL architecture (see Figure 1) MCROOD, to perform OOD detection and a simple pre-processing technique, RESPD, to detect especially minor human body movements and to ease the OOD detection. With RESPD, instead of focusing only on a single frame’s RDI, we use the combination of multiple consecutive RDIs. Our detector relies on an autoencoder-based architecture and consists of a one-encoder multi-decoder system. Each decoder corresponds to one human activity class, such as sitting, standing, and walking. Common OOD detectors use simple thresholding for detection. Based on a scoring function, a threshold is defined and used to classify the samples as ID or OOD. We use multi-thresholding. Our key contributions are as follows:

• We propose a simple yet effective pre-processing idea (RESPD) to be applied to RDIs. Instead of framewise training and testing, we benefit from multiple consecutive frames at the same time for training and inference. Thus, we manage to detect human respiration and differentiate it from similar movements like moving curtains. The idea has a noticeable effect on classification performance for human sitting and standing classes.

• We also propose a novel reconstruction-based OOD detector (MCROOD) that operates on RDIs. It consists of a one-encoder multi-decoder system. The decoders correspond to the ID classes sitting, standing, and walking. We achieve AUROCs of 97.45%, 92.13%, and 96.58% for sitting, standing, and walking classes, respectively, on our dataset, consisting of ID and OOD samples.

• We perform extensive evaluations on our dataset and show the superiority of MCROOD over SOTA methods in terms of common OOD detection metrics. Besides, MCROOD performs 24 times faster than the secondbest method [11]. We also provide an ablation analysis to emphasize the importance of RESPD.

## 2. RELATED WORK

In the OOD detection field, many studies have been published using different strategies, such as post-hoc, distance-based, and outlier exposure (OE) methods.

Post-hoc methods aim to work on any pre-trained model. Seminal work [12] has been published as a baseline by Hendrycks and Gimpel and relies on maximum softmax probability (MSP) scores. They mainly claim that ID samples have higher softmax scores than OOD samples. To improve [12], a follow-up method has been revealed. ODIN [13] applies input perturbation and temperature scaling to increase the softmax scores of ID samples and to ease the detection. In energy based OOD detection study [14], the authors apply the logsumexp operator to the logit layer and get an energy value to be used for detection. ReAct [4], as one of the recent studies, utilizes activation truncation on the penultimate layer to reduce the overconfident predictions. On the other hand, DICE [15] utilizes weight sparsification for OOD detection.

Distance-based methods aim to classify samples relatively far from the center of ID classes as OOD. Mahalanobis detector [11] uses intermediate feature representations and Mahalanobis distance information for detection. In a similar study [16], the authors create uniform noise and claim that OODs are closer to noise than IDs. A recent study [7] uses a simple K-nearest-neighbor (KNN) approach to estimate the OODs. Similarly, [17–19] are examples of distance-based strategy.

OE methods expose the model to a limited number of OOD samples during training or fine-tuning. [20] uses OE with a novel loss, pushing the softmax scores of OODs to the uniform distribution. OECC [21] applies the same strategy also with a novel loss consisting of two different regularization terms. Similar studies [22, 23], exploit OE using some OOD samples and try to generalize the knowledge to all other unseen OODs.

In the literature, there are also different strategies. As a confidence enhancement method, G-ODIN [6] proposes a new training scheme on top of [13] for better detection. Grad-Norm [24] emphasizes the importance of gradient information for OOD detection. [25] belongs to reconstruction-based methods and uses Mahalanobis distance information in latent space to detect OODs.

All mentioned methods are developed and tested for the image domain. In the radar domain, there are limited DLbased methods for the OOD detection problem. In [26], the authors compare different OOD methods on synthetically generated micro RDI data. In our work, we provide a DLbased OOD detector that works on real radar data. It consists of a one-encoder multi-decoder architecture and classifies any moving target other than a sitting, standing, or walking person as OOD. We also propose a simple pre-processing idea detecting human respiration movement for better OOD detection.

## 3. RADAR CONFIGURATION & PRE-PROCESSING

We use Infineon’s BGT60TR13C chipset with a 60GHz L-Shaped FMCW radar. It consists of one transmit (Tx) and three receiver (Rx) antennas. The radar configuration is listed in Table 1. The Tx antenna transmits $N _ { c }$ chirp signals, and the Rx antennas receive the reflected signals. A mixture of transmitted and reflected signals produces an intermediate frequency (IF). Low-pass filtering and digitization of the IF signal result in the raw Analogue-to-Digital Converter (ADC) data. Each chirp has $N _ { s }$ samples, so a frame’s dimensions become $N _ { R x } \times N _ { c } \times N _ { s }$

The IF signal’s component corresponds to time within a chirp called fast time. We first apply range FFT on fast time to extract the range of the object. Then, we use the moving target identification (MTI) function on range data to remove static targets. Finally, we perform doppler FFT on slow time, which refers to phase across chirps and obtain the RDIs.

Table 1: FMCW Radar Configuration Parameters
<table><tr><td>Configuration name</td><td>Symbol</td><td>Value</td></tr><tr><td>Number of Transmit Antennas</td><td> $N _ { T x }$ </td><td>1</td></tr><tr><td>Number of Receive Antennas</td><td> $N _ { R x }$ </td><td>3</td></tr><tr><td>Number of chirps per frame</td><td> $N _ { c }$ </td><td>64</td></tr><tr><td>Number of samples per chirp</td><td> $N _ { s }$ </td><td>128</td></tr><tr><td>Frame Period</td><td> $T _ { f }$ </td><td>50 ms</td></tr><tr><td>Chirp to chirp time</td><td> $T _ { c }$ </td><td>391.55 μs</td></tr><tr><td>Bandwidth</td><td> $B$ </td><td>1 GHz</td></tr></table>

## RESPD

RESPD is a simple pre-processing step that is applied to RDIs. Healthy adults breathe 12-20 times a minute [27]. To be able to detect this rhythmic movement, an about 2.5 seconds time interval is enough that corresponds to 50 consecutive frames in our radar configuration. Therefore, we pre-process the data using a sliding-window approach with a size of 50 frames. Namely, we sum all the frames within the window and write the calculated value on the first frame in the window, then we slide the window by one frame and repeat this process until the end. RESPD has a significant effect on the classification of human sitting and standing classes.

## 4. PROBLEM STATEMENT AND MCROOD

OOD detection is a simple binary classification task. However, in an open-world setting, a detector may be exposed to infinitely many OODs, making the binary classification task harder. We test MCROOD with a diverse set of OODs and show its robustness (see Figure 2).

## 4.1. Architecture and Training

We use a reconstruction-based architecture. It consists of one encoder and multi (3) decoder parts. Each decoder represents one ID class (sitting, standing, and walking). The encoder consists of four main blocks. The first three blocks sequentially apply 2D convolution with 2D batch normalization and ReLu activation followed by 2D max pooling. In the blocks, for each convolutional layer, we use 16, 32, and 64 filters with 3x3 kernel size, respectively. The final block consists of flattening and dense layers followed by 1D batch normalization and outputs the latent representation. The three decoders have the same architecture. They consist of five main blocks. The first one takes the latent code and feeds it to a dense layer with a 1D batch normalization. The next three blocks sequentially apply 2D transpose convolution with 2D batch normalization and ReLu activation, followed by upsampling. The fifth block has a 2D transpose convolutional layer with sigmoid activation. In the blocks, for each transpose convolutional layer, we use 64, 32, 16, and 1 filters with 3x3 kernel size, respectively.

![](images/da55cf425c1bf26dc53c1cdfd376bd02cae88bcc85ca9384cf9674167bb5d945.jpg)  
Fig. 1: The overall pipeline of MCROOD.

We perform simultaneous training for each class. Our encoder takes three inputs from three classes and produces three latent codes each time. On the other hand, as input, the decoder responsible for the sitting class only takes the latent code from sitting data. Following the same logic, the other two decoders take standing and walking data’s latent codes separately. With this approach, the encoder encodes the data from three different classes while decoders only decode the class they are responsible for. As mentioned, the encoder and decoders are simultaneously trained. We use mean squared error (MSE) as our loss function. Since there are three decoders in the network, we have three MSEs. Thus our final loss function becomes the sum of each MSE loss as in Equation 1. Here n is the batch size, $\mathbf { X } _ { c } ^ { ( i ) }$ is a data instance from class $c ,$ E is the encoder, and $D _ { c }$ is the class c’s decoder.

$$
\begin{array} { l } { \displaystyle \mathcal { L } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } ( \mathbf { X } _ { s i t } ^ { ( i ) } - D _ { s i t } ( E ( \mathbf { X } _ { s i t } ^ { ( i ) } ) ) ) } \\ { \displaystyle ~ + \frac { 1 } { n } \sum _ { i = 1 } ^ { n } ( \mathbf { X } _ { s t a n d } ^ { ( i ) } - D _ { s t a n d } ( E ( \mathbf { X } _ { s t a n d } ^ { ( i ) } ) ) ) } \\ { \displaystyle ~ + \frac { 1 } { n } \sum _ { i = 1 } ^ { n } ( \mathbf { X } _ { w a l k } ^ { ( i ) } - D _ { w a l k } ( E ( \mathbf { X } _ { w a l k } ^ { ( i ) } ) ) ) } \end{array}\tag{1}
$$

## 4.2. OOD Detection

Reconstruction-based OOD detection methods detect the OODs based on the difference between the input and reconstructed output. The detector classifies the sample as OOD if the difference is more than a threshold. In MCROOD, we expect to see more reconstruction errors for OODs since we train our network using only IDs. Since we have a multidecoder system, we perform multi-thresholding. During inference, we feed the encoder with the same input (X) from its three input gates. The encoder encodes and gives the latent code to each decoder separately. After the reconstruction, we separately evaluate the errors between the input and outputs by reconstruction MSE and then perform the multithresholding. The network classifies the sample as OOD if all reconstruction errors exceed their corresponding thresholds; otherwise, ID.

![](images/80bf19d73a254fb3b5c57f4eb873cf199d2d2f058cb63c7faf99b0a54b766a4a.jpg)  
(a)

![](images/53245773588f4792e81537d711e9a77fa322646744f8ee2ae330a0452073973b.jpg)  
(b)

![](images/66982e24138c40ac9e44dd821c86aca2e53496a9e70298cd9a7974cbcbda3b63.jpg)  
(c)  
Fig. 2: Reconstruction MSEs at inference time (x-axis) of sitting (a), standing (b), walking (c) vs OODs. The y-axis represents the sample index. When IDs (blue points) aggregate in a specific region with low reconstruction errors, OODs (red points) spread out with higher error values.

## 5. EXPERIMENTS

We perform our experiments with a processing unit of NVIDIA GeForce RTX 3070 GPU, Intel Core i7-11800H CPU, and 32GB DDR4 module of RAM.

## 5.1. Dataset and Evaluation Metrics

Data is collected using Infineon’s BGT60TR13C 60GHz FMCW radar sensor with four individuals in 16 house, school, and office rooms (10 for training and six for inference). It consists of ID and OOD samples. IDs include human walking, sitting, and standing classes with changing ranges and distances from 1 to 5m. OOD samples include a table fan, a remote-controlled (RC) toy car, swinging plants, swinging blinds, swinging curtains, swinging laundry, a swinging paper bag, a vacuum cleaner, and a robot vacuum cleaner. We have 111416 ID frames in our training set. During inference, we used 47210 ID and 16050 OOD frames.

We chose commonly used evaluation metrics AUROC, AUPR, FPR95, and FPR80. AUROC is the area under the receiver operating characteristic (ROC) curve. AUPR is the area under the precision-recall curve. FPR95 is the false positive rate (FPR) when the true positive rate (TPR) is 95%. FPR80 is the FPR when TPR is 80%.

Table 2: Main Results. OOD detection performance comparison with other popular methods. All values are shown in percentages. ↑ indicates that higher values are better, while ↓ indicates that lower values are better.
<table><tr><td rowspan="3">Architecture</td><td rowspan="3">Methods</td><td colspan="4">Sit</td><td colspan="4">Stand</td><td colspan="4">Walk</td></tr><tr><td>AUROC ↑</td><td>AUPR ↑</td><td>FPR95 ↓</td><td>FPR80 ↓</td><td>AUROC ↑</td><td>AUPR ↑</td><td>FPR95 ↓</td><td>FPR80 ↓</td><td>AUROC ↑</td><td>AUPR ↑</td><td>FPR95 ↓</td><td>FPR80 ↓</td></tr><tr><td rowspan="6">RESNET-34 [28]</td><td>ODIN [13]</td><td>69.51</td><td>67.62</td><td>66.64</td><td>47.43</td><td>56.11</td><td>56.50</td><td>87.19</td><td>72.08</td><td>79.11</td><td>71.99</td><td>47.27</td><td>36.82</td></tr><tr><td>MSP [12]</td><td>50.67</td><td>54.12</td><td>91.82</td><td>77.85</td><td>39.89</td><td>42.25</td><td>94.34</td><td>83.73</td><td>89.71</td><td>85.31</td><td>31.72</td><td>20.46</td></tr><tr><td>ENERGY [14]</td><td>50.89</td><td>53.52</td><td>85.20</td><td>75.06</td><td>39.73</td><td>41.59</td><td>88.93</td><td>81.85</td><td>87.78</td><td>82.64</td><td>35.42</td><td>23.45</td></tr><tr><td>MAHA [11]</td><td>96.50</td><td>96.95</td><td>10.24</td><td>5.50</td><td>86.55</td><td>81.62</td><td>46.87</td><td>20.06</td><td>66.73</td><td>53.73</td><td>73.40</td><td>58.55</td></tr><tr><td>FSSD [16]</td><td>40.33</td><td>45.67</td><td>83.67</td><td>65.82</td><td>47.65</td><td>43.10</td><td>66.20</td><td>59.07</td><td>96.67</td><td>95.09</td><td>18.46</td><td>2.82</td></tr><tr><td>OE [20]</td><td>49.73</td><td>55.40</td><td>94.89</td><td>80.30</td><td>49.72</td><td>48.97</td><td>95.30</td><td>79.45</td><td>49.99</td><td>43.55</td><td>94.97</td><td>80.04</td></tr><tr><td rowspan="7">RESNET-50 [28]</td><td>ODIN [13]</td><td>57.13</td><td>53.78</td><td>71.42</td><td>56.66</td><td>53.14</td><td>47.11</td><td>80.59</td><td>64.61</td><td>94.63</td><td>92.90</td><td>24.06</td><td>9.36</td></tr><tr><td>MSP [12]</td><td>47.31</td><td>49.25</td><td>90.02</td><td>73.54</td><td>40.67</td><td>41.10</td><td>92.88</td><td>81.58</td><td>95.42</td><td>93.08</td><td>19.95</td><td>7.96</td></tr><tr><td>ENERGY [14]</td><td>49.23</td><td>49.64</td><td>80.48</td><td>69.19</td><td>41.39</td><td>40.89</td><td>88.50</td><td>76.66</td><td>94.89</td><td>92.82</td><td>21.28</td><td>8.44</td></tr><tr><td>MAHA [11]</td><td>97.18</td><td>97.60</td><td>9.95</td><td>4.48</td><td>90.35</td><td>85.13</td><td>33.11</td><td>12.64</td><td>82.81</td><td>68.44</td><td>53.21</td><td>23.83</td></tr><tr><td>FSSD [16]</td><td>6.62</td><td>35.38</td><td>99.90</td><td>99.76</td><td>21.11</td><td>34.05</td><td>99.58</td><td>94.74</td><td>92.53</td><td>86.96</td><td>19.95</td><td>13.21</td></tr><tr><td>OE [20]</td><td>38.23</td><td>46.90</td><td>99.23</td><td>90.22</td><td>26.27</td><td>35.85</td><td>96.50</td><td>91.37</td><td>94.33</td><td>91.23</td><td>15.29</td><td>11.76</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="6">RESNET-101 [28]</td><td>ODIN [13] MSP [12]</td><td>55.00 45.31</td><td>53.84 49.07</td><td>84.36 94.69</td><td>67.01 82.84</td><td>54.66 45.27</td><td>48.54 43.40</td><td>81.61 93.58</td><td>68.98 80.32</td><td>94.14 93.44</td><td>92.05 87.43</td><td>20.29 18.83</td><td>13.83 13.41</td></tr><tr><td>ENERGY [14]</td><td>47.46</td><td>49.93</td><td>94.05</td><td>75.85</td><td>47.59</td><td>44.62</td><td>91.31</td><td>74.87</td><td>94.51</td><td>92.40</td><td></td><td>13.36</td></tr><tr><td></td><td>94.21</td><td>94.94</td><td>21.37</td><td>8.88</td><td>89.91</td><td>85.15</td><td>33.62</td><td>12.44</td><td>72.82</td><td>57.57</td><td>18.96 67.71</td><td>41.84</td></tr><tr><td>MAHA [11]</td><td>12.74</td><td>37.38</td><td>99.80</td><td>98.71</td><td>23.73</td><td>35.38</td><td>99.66</td><td>97.99</td><td>90.59</td><td></td><td></td><td></td></tr><tr><td>FSSD [16]</td><td>39.22</td><td>45.34</td><td>98.30</td><td>75.27</td><td>44.37</td><td>42.08</td><td>95.00</td><td>69.83</td><td>95.98</td><td>89.10 94.05</td><td>49.53</td><td>16.35</td></tr><tr><td>OE [20]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>14.60</td><td>8.08</td></tr><tr><td>Ours</td><td>MCROOD</td><td>97.45</td><td>98.40</td><td>12.93</td><td>0.35</td><td>92.13</td><td>93.51</td><td>50.94</td><td>9.90</td><td>96.58</td><td>94.82</td><td>13.91</td><td>5.24</td></tr></table>

We compare MCROOD with six SOTA methods in terms of common OOD metrics. For a detailed comparison, we separately train ResNet34, ResNet50, and ResNet101 backbones [28] with our three class ID data in a multi-class classification manner. During training, no OOD data are exposed to the architectures. Afterward, we use the pre-trained models to apply the SOTA methods and evaluate their performance in terms of significant metrics. Table 2 shows the superiority of MCROOD over SOTA approaches. A short demo video of our system is available at the link<sup>1</sup>.

## 5.2. Ablation

We also perform ablation experiments to show the impact of RESPD. For this experiment, we only choose the best two methods, namely MCROOD and MAHA [11], and perform a framewise evaluation on the same models without RESPD. Instead of using consecutive 50 frames, we evaluate each frame separately to perform OOD detection. Table 3 shows the effectiveness of RESPD, especially for the ID samples of sitting and standing classes. On its nature, the walking class produces macro movements, so RESPD has limited impact on it while distinguishing IDs from OODs. When all test samples are evaluated, MCROOD and MAHA [11] finish their inference in 129 and 3121 seconds, respectively.

Table 3: Ablation Study. All values are shown in percentages. ↑ indicates that higher values are better.
<table><tr><td rowspan="2">Methods</td><td colspan="3">AUROC ↑</td></tr><tr><td>Sit</td><td>Stand</td><td>Walk</td></tr><tr><td>MAHA [11]</td><td>14.93</td><td>24.68</td><td>85.85</td></tr><tr><td>MCROOD</td><td>12.69</td><td>20.73</td><td>89.43</td></tr><tr><td>MAHA+RESPD</td><td>97.18</td><td>90.35</td><td>82.81</td></tr><tr><td>MCROOD+RESPD</td><td>97.45</td><td>92.13</td><td>96.58</td></tr></table>

## 6. CONCLUSION

In this study, we developed an OOD detection pipeline to be performed on 60GHz FMCW radar data. Our detector MCROOD has a novel reconstruction-based one-encoder multi-decoder architecture; due to its modular nature, it can work with any number of in-class activities. We used our detector to classify any moving object which may appear in indoor environments other than a sitting, standing, or walking human as OOD. We also provided RESPD as a simple yet effective pre-processing idea. With RESPD, we aimed to detect minor human body movements like breathing. MCROOD with RESPD reached AUROCs of 97.45%, 92.13%, and 96.58% for sitting, standing, and walking classes, respectively. Our experiments show that MCROOD outperforms popular SOTA methods. Besides, compared with the best second method, MCROOD has a 24 times faster processing time and is very suitable for real-time evaluation.

## 7. REFERENCES

[1] Haoqi Wang, Zhizhong Li, Litong Feng, and Wayne Zhang, “Vim: Out-of-distribution with virtual-logit matching,” arXiv, 2022.

[2] Xuefeng Du, Zhaoning Wang, Mu Cai, and Yixuan Li, “Vos: Learning what you don’t know by virtual outlier synthesis,” in International Conference on Learning Representations (ICLR), 2022.

[3] Jingkang Yang, Haoqi Wang, Litong Feng, Xiaopeng Yan, Huabin Zheng, Wayne Zhang, and Ziwei Liu, “Semantically coherent out-of-distribution detection,” in IEEE International Conference on Computer Vision (ICCV), 2021.

[4] Yiyou Sun, Chuan Guo, and Yixuan Li, “React: Out-ofdistribution detection with rectified activations,” in Advances in Neural Information Processing Systems (NeurIPS), 2021.

[5] Rui Huang and Yixuan Li, “Mos: Towards scaling out-ofdistribution detection for large semantic space,” in IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021.

[6] Y. C. Hsu, Y. Shen, H. Jin, and Z. Kira, “Generalized odin: Detecting out-of-distribution image without learning from outof-distribution data,” in IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020.

[7] Yiyou Sun, Yifei Ming, Xiaojin Zhu, and Yixuan Li, “Out-ofdistribution detection with deep nearest neighbors,” in International Conference on Machine Learning (ICML), 2022.

[8] Souvik Hazra and Avik Santra, “Robust gesture recognition using millimetric-wave radar system,” IEEE Sensors Letters, vol. 2, no. 4, pp. 1–4, 2018.

[9] Lorenzo Servadei, Huawei Sun, Julius Ott, Michael Stephan, Souvik Hazra, Thomas Stadelmayer, Daniela Sanchez Lopera,´ Robert Wille, and Avik Santra, “Label-aware ranked loss for robust people counting using automotive in-cabin radar,” in IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2022.

[10] Muhammad Arsalan, Avik Santra, and Christoph Will, “Improved contactless heartbeat estimation in fmcw radar via kalman filter tracking,” IEEE Sensors Letters, vol. 4, no. 5, pp. 1–4, 2020.

[11] Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin, “A simple unified framework for detecting out-of-distribution samples and adversarial attacks,” in International Conference on Neural Information Processing Systems (NeurIPS), 2018.

[12] Dan Hendrycks and Kevin Gimpel, “A baseline for detecting misclassified and out-of-distribution examples in neural networks,” in International Conference on Learning Representations (ICLR), 2017.

[13] Shiyu Liang, Yixuan Li, and R. Srikant, “Enhancing the reliability of out-of-distribution image detection in neural networks,” in International Conference on Learning Representations (ICLR), 2018.

[14] Weitang Liu, Xiaoyun Wang, John Owens, and Yixuan Li, “Energy-based out-of-distribution detection,” in Advances in Neural Information Processing Systems (NeurIPS), 2020.

[15] Yiyou Sun and Yixuan Li, “Dice: Leveraging sparsification for out-of-distribution detection,” in European Conference on Computer Vision (ECCV), 2022.

[16] Haiwen Huang, Zhihan Li, Lulu Wang, Sishuo Chen, Bin Dong, and Xinyu Zhou, “Feature space singularity for outof-distribution detection,” in Proceedings of the Workshop on Artificial Intelligence Safety 2021 (SafeAI 2021), 2021.

[17] Chandramouli Shama Sastry and Sageev Oore, “Detecting outof-distribution examples with Gram matrices,” in International Conference on Machine Learning (ICML), 2020.

[18] Jie Ren, Stanislav Fort, Jeremiah Liu, Abhijit Guha Roy, Shreyas Padhy, and Balaji Lakshminarayanan, “A simple fix to mahalanobis distance for improving near-ood detection,” arXiv, 2021.

[19] Alireza Zaeemzadeh, Niccolo Bisagno, Zeno Sambugaro, Nicola Conci, Nazanin Rahnavard, and Mubarak Shah, “Outof-distribution detection using union of 1-dimensional subspaces,” in IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021.

[20] Dan Hendrycks, Mantas Mazeika, and Thomas Dietterich, “Deep anomaly detection with outlier exposure,” in International Conference on Learning Representations (ICLR), 2019.

[21] Aristotelis-Angelos Papadopoulos, Mohammad Reza Rajati, Nazim Shaikh, and Jiamian Wang, “Outlier exposure with confidence control for out-of-distribution detection,” Neurocomputing, vol. 441, pp. 138–150, 2021.

[22] Qing Yu and Kiyoharu Aizawa, “Unsupervised out-ofdistribution detection by maximum classifier discrepancy,” in IEEE/CVF International Conference on Computer Vision (ICCV), 2019.

[23] Yi Li and Nuno Vasconcelos, “Background data resampling for outlier-aware classification,” in IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020.

[24] Rui Huang, Andrew Geng, and Yixuan Li, “On the importance of gradients for detecting distributional shifts in the wild,” in Advances in Neural Information Processing Systems (NeurIPS), 2021.

[25] Taylor Denouden, Rick Salay, Krzysztof Czarnecki, Vahdat Abdelzad, Buu Phan, and Sachin Vernekar, “Improving reconstruction autoencoder out-of-distribution detection with mahalanobis distance,” arXiv, 2018.

[26] Martin Bauw, Santiago Velasco-Forero, Jesus Angulo, Claude Adnet, and Olivier Airiau, “Near out-of-distribution detection for low-resolution radar micro-doppler signatures,” arXiv, 2022.

[27] Wilburta Q Lindh, Marilyn Pooler, Carol D Tamparo, Barbara M Dahl, and Julie Morris, Delmar’s comprehensive medical assisting: administrative and clinical competencies, Cengage Learning, 2013.

[28] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun, “Deep residual learning for image recognition,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016.