# FOOD: FACIAL AUTHENTICATION AND OUT-OF-DISTRIBUTION DETECTION WITH SHORT-RANGE FMCW RADAR

Sabri Mustafa Kahya<sup>⋆</sup> Boran Hamdi Sivrikaya<sup>⋆</sup> Muhammet Sami Yavuz<sup>⋆†</sup> Eckehard Steinbach<sup>⋆</sup>

<sup>⋆</sup>Technical University of Munich, School of Computation, Information and Technology, Department of Computer Engineering, Chair of Media Technology, Munich Institute of Robotics and Machine Intelligence (MIRMI) <sup>†</sup>Infineon Technologies AG

## ABSTRACT

This paper proposes a short-range FMCW radar-based facial authentication and out-of-distribution (OOD) detection framework. Our pipeline jointly estimates the correct classes for the in-distribution (ID) samples and detects the OOD samples to prevent their inaccurate prediction. Our reconstruction-based architecture consists of a main convolutional block with one encoder and multi-decoder configuration, and intermediate linear encoder-decoder parts. Together, these elements form an accurate human face classifier and a robust OOD detector. For our dataset, gathered using a 60 GHz short-range FMCW radar, our network achieves an average classification accuracy of 98.07% in identifying indistribution human faces. As an OOD detector, it achieves an average Area Under the Receiver Operating Characteristic (AUROC) curve of 98.50% and an average False Positive Rate at 95% True Positive Rate (FPR95) of 6.20%. Also, our extensive experiments show that the proposed approach outperforms previous OOD detectors in terms of common OOD detection metrics.

Index Terms— Facial authentication, out-of-distribution detection, 60 GHz FMCW radar, deep neural networks

## 1. INTRODUCTION

In recent years, short-range radars have attracted significant attention and widespread adoption across various domains due to their cost-effectiveness. Radar systems demonstrate remarkable resilience to adverse environmental conditions, including lightning, rain, and smoke. Moreover, they are not constrained by privacy issues, which provides a distinct advantage over camera-based applications. Therefore, they find extensive use in indoor applications such as human presence detection, human activity classification, people counting, gesture recognition, and even heartbeat estimation [1–5]. In this study, we propose a facial authentication system, FOOD, which also addresses the detection of out-of-distribution (OOD) samples.

OOD detection plays a critical role in ensuring the secure and reliable deployment of deep learning (DL) models in real-world scenarios by preventing overconfident decisions on samples that deviate from the training data [6–9]. FOOD provides a parallel solution for both classification and OOD detection tasks.

FOOD is a novel facial authentication system that not only classifies in-distribution (ID) human face samples but also detects OOD face samples that were not presented during training. The system utilizes a unique framework that processes raw ADC radar data to accurately classify three human faces and detect OOD samples. Our reconstruction-based framework provides convolutional and linear encoder-decoder parts (see Figure 1). We call the linear encoder-decoder parts the leaves of the network. Namely common leaf (CL) and private leaves (PLs). They are mainly designed for OOD detection purposes, but the PLs also strongly affect accurate classification together with the main convolutional part. A standard OOD detector utilizes a scoring function along with a predefined threshold. Subsequently, a test sample is categorized as ID if its score falls below the specified threshold; otherwise, it is classified as OOD. In this study, we use multi-thresholding. Here are the key contributions of this study:

• We introduce a novel reconstruction-based architecture designed to function as both a robust classifier and an OOD detector. It comprises a main convolutional one-encoder multi-decoder segment denoted as MP and intermediate linear one-encoder one-decoder components, namely CL and PLs. Within MP, the multi-decoder section is dedicated to identifying specific human face classes: Person 1 (PER<sub>1</sub>), Person 2 (PER ), and Person 3 (PER ). CL is situated at the termination of the MP’s encoder, while PLs are strategically positioned within the decoders of MP. CL and PLs are mainly designed for OOD human face sample detection, but PLs also significantly influence overall classification accuracy.

• We propose a novel loss function composed of seven distinct reconstruction losses. Among these, three originate from the MP, while one is derived from the CL. The remaining three losses are associated with the PLs. During test time, the MP and PL losses are utilized for classification purposes, while the CL and PL losses are employed for OOD detection purposes.

• We conduct comprehensive experiments that yield an average human facial classification accuracy of 98.07% and an average AUROC of 98.50% in OOD detection. Additionally, we compare FOOD’s performance with state-of-the-art (SOTA) OOD detection methods, evaluating it using common OOD detection metrics and test time, and demonstrate its superior performance.

• We also perform extensive ablation studies to emphasize the effects of the novel parts of our network. We show how PLs affect the classification accuracy when they are used together with the main convolutional reconstruction part. Also, we demonstrate the results of OOD detection when we only utilize CL and CL together with PLs.

## 2. RELATED WORK

In the field of radar-based face authentication, various studies have been conducted. The work in [10] used a 61 GHz mmWave radar sensor, employing a deep neural network (DNN) to classify human faces. The authors of [10] captured signals from multiple antenna elements, with data gathered from eight individuals at varying distances and angles relative to the radar. By combining signals from each receiver, a classification accuracy of 92% was achieved. Similarly, [11] introduced a 61 GHz FMCW radar face identification system using a Convolutional Neural Networks (CNNs). Data for this system were collected from three individuals positioned 30 cm from the radar chip, both with and without cotton masks. Initially, the model was trained on subjects not wearing masks, and subsequently, data from subjects wearing cotton masks were added. The study reports findings for both scenarios. Another significant contribution is from [12], which employs a radar sensor with 32 transmit (Tx) and 32 receive (Rx) antennas. A dense auto-encoder model was utilized on a dataset comprising 200 distinct faces, training this system as a one-class classifier for a verification system tailored to each person. Following this, the authors in [13] also used the same dataset but proposed an improvement by integrating a convolutional autoencoder with a random forest classifier. [14] proposed a novel approach by introducing a one-shot learning method for a 61 GHz FMCW radar. Based on a Siamese Network architecture, this method utilized data from eight individuals positioned at distances ranging from 30 to 50 cm from the radar, achieving an accuracy of 97.6%. The most recent study, [15], proposed a face recognition system using a 77 GHz mmWave sensor. This system extracts a point cloud dataset from nine users at various distances (60 cm and 80 cm) and angles (-45°, 0°, 45°). The architecture is based on PointNet and adapted to work directly with the sparser point cloud data from mmWave radar sensors. The device used in this study is a cascade device, comprising four radar chips, each with 3 Tx and 4 Rx antennas, resulting in a total of 12 Tx and 16 Rx antennas, and achieving an accuracy of 98.69%. The studies mentioned, however, predominantly concentrate on achieving a highly accurate classifier, overlooking the performance of their pipeline when exposed to OOD samples.

OOD detection was first introduced in [16], which employed maximum softmax probabilities to differentiate OOD input from ID samples by claiming that OOD instances typically exhibit lower softmax scores than ID samples. ODIN [17] aimed to enhance ID softmax scores through input perturbation and temperature scaling of logits. A model ensembling technique was layered on ODIN’s approach in [18]. G-ODIN [19] extended ODIN’s methodology [17] with an innovative training strategy. Meanwhile, MAHA [20] introduced a Mahalanobis distance-based OOD detection using intermediate layer representations. Similarly, FSSD [21] leverages these intermediate representations for detection. The approach in [22] employs a non-parametric KNN on penultimate layer embeddings for detection. An energy-based OOD detection method was introduced by [23], utilizing the logsumexp function. ReAct [24] implements truncation on activations in the penultimate layer and it is compatible with various OOD detection methods. GradNorm [25] distinguishes between IDs and OODs using the vector norm of gradients backpropagated from the KL divergence between the softmax output and a uniform distribution. In [26], two methods were proposed: MaxLogit, which distinguishes between ID samples and OOD samples based on maximum logit scores, and KL, which utilizes minimum KL divergence information. The OE technique in [27] employs limited OOD examples during training to align their softmax scores closer to a uniform distribution. OECC [28] enhances OE with a novel loss incorporating extra regularization elements.

OOD detection has also been explored in the radar domain. [29] employs 60 GHz FMCW radar to detect commonly seen indoor objects as OOD rather than a walking person. MCROOD [30] serves as a multi-class radar OOD detector that distinguishes moving OOD objects from human activities of sitting, standing, and walking. [31] introduced a multi-encoder multi-decoder network, which handles both human presence and OOD detection concurrently. [32] also focuses on human activity classification and OOD detection.

## 3. RADAR SYSTEM DESIGN

In this research, we used Infineon’s BGT60TR13C 60 GHz FMCW radar chipset for data acquisition. The radar configuration details are provided in Table 1. This chipset has a single

Tx antenna and three Rx antennas. During the transmission, the Tx antenna emits $N _ { c }$ chirp signals. These signals, upon interaction with objects in the environment, are reflected and subsequently received by the Rx antennas with a time delay, indicative of the object’s range and velocity. The transmitted and received signals are then mixed and passed through a low-pass filter to extract the intermediate frequency (IF) signal. Subsequently, this IF signal is converted into digital form using an Analog-to-Digital Converter (ADC) that operates at a sampling frequency of 2 MHz with 12-bit accuracy. The raw ADC data is structured as $N _ { R x } \times N _ { c } \times N _ { s }$ <sub>s</sub> and used as input for our model.

Table 1: FMCW Radar Configuration Parameters
<table><tr><td>Configuration name</td><td>Symbol</td><td>Value</td></tr><tr><td>Number of transmit antennas</td><td> $N _ { \mathrm { T x } }$ </td><td>1</td></tr><tr><td>Number of receive antennas</td><td> $N _ { \mathrm { { R x } } }$ </td><td>3</td></tr><tr><td>Chirps per frame</td><td> $N _ { \mathrm { c } }$ </td><td>64</td></tr><tr><td>Samples per chirp</td><td> $N _ { \mathrm { s } }$ </td><td>128</td></tr><tr><td>Frame period</td><td> $\mathrm { T _ { f } }$ </td><td>50 ms</td></tr><tr><td>Chirp to chirp time</td><td> $T _ { \mathrm { c c } }$ </td><td>391.55 μs</td></tr><tr><td>Ramp start frequency</td><td> $f _ { \mathrm { m i n } }$ </td><td>60.1 GHz</td></tr><tr><td>Ramp stop frequency</td><td> $f _ { \mathrm { m a x } }$ </td><td>61.1 GHz</td></tr><tr><td>Bandwidth</td><td> $B$ </td><td>1GHz</td></tr></table>

## 4. PROBLEM STATEMENT AND FOOD

In this work, we address both multi-class classification and binary OOD detection tasks. FOOD provides a solution for accurately classifying ID face samples while correctly eliminating human faces (OODs) that were not present during training.

The MP consists of one encoder and three decoders. The encoder has three input gates and is responsible for encoding the three type ID samples. On the other hand, the top, middle, and bottom decoders are responsible for the reconstruction of the ID samples $\mathbf { P E R } _ { 1 } , \ \mathbf { P E R } _ { 2 }$ , and $\mathbf { P E R } _ { 3 }$ , respectively. We calculate three reconstruction losses from ${ \bf M P } _ { 1 } , { \bf M P } _ { 2 }$ and $\mathbf { M P } _ { 3 }$ , mainly used to achieve better classification performance. For example, $\mathbf { M P } _ { 2 }$ refers to the encoder (E) and decoder of PER2 $( \mathrm { D } _ { \mathrm { P E R 2 } } )$ in MP, which is also detailed in the bottom part of Figure 1. Since we use the mean-squared-error (MSE) function, the three losses from this part are shaped as in the equation below:

$$
\mathcal { L } _ { M P } = \frac { 1 } { b } \sum _ { j \in \{ p _ { 1 } , p _ { 2 } , p _ { 3 } \} } \sum _ { i = 1 } ^ { b } ( \mathbf { X } _ { j } ^ { ( i ) } - D _ { j } \big ( E ( \mathbf { X } _ { j } ^ { ( i ) } ) \big ) ) ^ { 2 } ,
$$

where $X _ { j } ^ { ( i ) }$ is raw ADC input, b is the batch size, and $j$ is an index for the ID classes $\mathbf { ( P E R _ { 1 } , P E R _ { 2 } , P E R _ { 3 } ) }$ ; E and $D _ { j }$ correspond to the encoder and decoders of MP.

The CL starts at the end of the encoder of the MP. It has a simple linear encoder-decoder architecture and is responsible

for encoding and reconstructing the intermediate features of all ID classes. The CL calculates a reconstruction MSEs to be used for better OOD detection:

$$
\mathcal { L } _ { C L } = \frac { 1 } { b } \sum _ { j \in \{ p _ { 1 } , p _ { 2 } , p _ { 3 } \} } \sum _ { i = 1 } ^ { b } ( E ( \mathbf { X } _ { j } ^ { ( i ) } ) - D _ { C L } ( E _ { C L } ( E ( \mathbf { X } _ { j } ^ { ( i ) } ) ) ) ) ^ { 2 } ,
$$

where $E _ { C L }$ and $D _ { C L }$ are the encoder and decoder of common leaf, respectively.

The PLs start just before the final reconstruction layer of each decoder. Since we have three decoders in MP, there are three PLs. Each has a simple linear encoder-decoder architecture and is responsible for encoding and reconstructing the intermediate features of their corresponding ID classes. The PLs calculate three reconstruction MSEs to be used for both more accurate classification and stronger OOD detection:

$$
\mathcal { L } _ { P L } = \frac { 1 } { b } \sum _ { k \in \{ p l _ { 1 } , p l _ { 2 } , p l _ { 3 } \} } \sum _ { i = 1 } ^ { b } ( \mathbf { I } _ { k } ^ { ( i ) } - D _ { k } ( E _ { k } ( \mathbf { I } _ { k } ^ { ( i ) } ) ) ) ^ { 2 } ,
$$

where $I _ { k } ^ { ( i ) }$ represents the intermediate input of PLs, k is an index for private leaves; $E _ { k }$ and $D _ { k }$ respectively correspond to the encoder and decoder of each PL.

The final loss function becomes $\mathcal { L } = \mathcal { L } _ { M P } + \mathcal { L } _ { C L } +$ $\mathcal { L } _ { P L }$ . We perform simultaneous training by minimizing all seven reconstruction losses at the same time. We use the MSE function to calculate the main and intermediate reconstruction losses by incorporating the Adamax optimizer [33].

## 4.1. OOD Detection

We use CL and PLs for OOD detection purposes. As a typical OOD detection task, we train our network only with IDs. Therefore, we expect less reconstruction errors coming from CL and PLs for ID samples than for OOD samples. We define three thresholds (guaranteeing 95% of ID data is correctly detected) belonging to each ID class using $\mathbf { C L } { + } \mathbf { P L } _ { 1 }$ for $\mathbf { P E R } _ { 1 }$ $\mathbf { C L } { + } \mathbf { P L } _ { 2 }$ for $\mathbf { P E R } _ { 2 }$ , and $\mathbf { C L } { + } \mathbf { P L } _ { 3 }$ for $\mathbf { P E R } _ { 3 }$ . During test time, a test sample passes through the entire network and gets three scores to be compared with the pre-defined thresholds explained above. The sample is classified as OOD if all three reconstruction scores from CL+PLs exceed their corresponding thresholds.

## 4.2. Human Face Classification

If a test sample is not classified as OOD, it is an ID. To define the correct class of the ID sample, we use PLs and MP $\begin{array} { r } { ( \mathbf { M } \mathbf { P } _ { 1 } , \mathbf { M } \mathbf { P } _ { 2 } , } \end{array}$ and $\mathrm { { { M P } _ { 3 } ) } }$ . We separately calculate three error values from $\mathbf { M P } _ { 1 } { + } \mathbf { P } \mathbf { L } _ { 1 } , \ \mathbf { M P } _ { 2 } { + } \mathbf { P } \mathbf { L } _ { 2 }$ , and $\mathbf { M } \mathbf { P } _ { 3 } \mathrm { { + } \mathbf { P } \mathbf { L } _ { 3 } }$ . We select the smallest one from these values and assign the ID sample to its corresponding class. For instance, if the total reconstruction MSE from $\mathbf { M } \mathbf { P } _ { 2 } \mathrm { + } \mathbf { P } \mathbf { L } _ { 2 }$ is less than the other two, the ID sample is classified as $\mathbf { P E R } _ { 2 }$

![](images/551c6096da418a69b0baa9eb2d7a7dedf7ce67d8b80801e324d92be481f5d9a0.jpg)  
Fig. 1: The figure presents the high-level structure of FOOD and the zoom-in version of the highlighted section. Here we have a main convolutional one-encoder multi-decoder part (MP) and intermediate linear encoder decoder parts common leaf (CL) and private leaves (PLs). The encoder of MP encodes the ID input data and from top to bottom its decoders reconstruct the ID input $\mathbf { P E R } _ { 1 } , \mathbf { P E R } _ { 2 } .$ and PER<sub>3</sub>, respectively. CL has a simple linear encoder-decoder network and is responsible for OOD detection. PLs are ID class specific and also have linear encoder-decoder network each. They have a considerable effect on both classification and OOD detection. MSE function is used for the calculation of each loss.

## 5. EXPERIMENTS AND RESULTS

Our experiments are carried out using an NVIDIA GeForce RTX 3070 GPU, an Intel Core i7-11800H CPU, and a 32GB DDR4 RAM module.

## 5.1. Dataset and Evaluation

In this study, we constructed our own face dataset using Infineon’s BGT60TR13C 60 GHz FMCW radar sensor. The data collection process spanned a six-month period. Each recording was taken at a distance of 25 cm from the radar sensor, capturing a face for a duration of 2 minutes. Notably, none of these participants wore accessories on their faces during the recordings. The recordings took place on different days and at various times of the day, including morning, noon, and afternoon. Moreover, different room backgrounds were incorporated to introduce environmental diversity into the dataset. It consists of two types of samples: ID and OOD. ID samples are from three male participants, who are the first three authors of this study. OODs are from 13 people, including ten males and three females. In total, we acquired 190126 ID frames (balanced) and 15818 OOD frames. For the ID data, 171118 frames are allocated for training and 19008 frames for testing. The dataset will be available here<sup>1</sup>. Written consent is available from those involved in the research.

In OOD detection, we employ four standard metrics. AUROC quantifies the area under the receiver operating characteristic (ROC) curve. AUPR<sub>IN/OUT</sub> corresponds to the area under the precision-recall curve, specifically considering ID/OOD samples as positives. FPR95 denotes the false positive rate (FPR) at a true positive rate (TPR) of 95%. In the context of human face classification, accuracy serves as the evaluation metric. Additionally, we provide Test Time, signifying the inference time in seconds necessary to assess all test samples.

To compare the performance of FOOD, we train the ResNet34 [34] architecture in a multi-class classification manner. The strong ResNet34 [34] pipeline provides a slightly better human face classification of 99.10% than FOOD. However, it does not have the capability to detect the OODs. To compare the OOD detection capability of FOOD to SOTA methods, we use the same pre-trained ResNet34 [34] model above. We apply eight different and powerful OOD detectors to the model and compare their results with FOOD. As seen in Table 2, FOOD outperforms the SOTA methods in terms of widely used OOD detection metrics.

## 5.2. Ablation

We also perform ablation studies. Table 4 reflects the impact of using MP $( \mathbf { M P } _ { 1 } , \mathbf { M P } _ { 2 }$ , and $\mathrm { { { M P } _ { 3 } ) } }$ together with PLs on human face classification accuracy. Figure 2 provides a confusion matrix. Additionally, Table 3 demonstrates the effects of CL and PLs when they are used together for OOD detection. Based on the application and the level of OOD detection necessity, the CL can be used alone for immediate detection of the OODs because it also provides highly acceptable results. However, PLs are located just before the final layer of the MP’s decoders and include high-level information of their corresponding ID class. Since they are specialized only in their ID class, they greatly impact accurate classification and OOD detection.

Table 2: OOD Detection Results. Performance comparison with SOTA methods. All values are shown in percentages. ↑ indicates that higher values are better, while ↓ indicates that lower values are better.
<table><tr><td rowspan="3">Methods</td><td colspan="4">PER1</td><td colspan="4">PER2</td><td colspan="4"> $\mathrm { P E R _ { 3 } }$ </td><td rowspan="2">Test Time</td></tr><tr><td>AUROC</td><td> $\mathrm { A U P R } _ { \mathrm { N } }$ </td><td> $\mathbf { A U P R _ { O U T } }$ </td><td>FPR95 AUROC</td><td></td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$ </td><td> $\mathbf { A U P R _ { O U T } }$ </td><td>FPR95 AUROC</td><td></td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$ </td><td> $\mathbf { A U P R _ { O U T } }$ </td><td>FPR95 (seconds)</td></tr><tr><td>MSP [16]</td><td>↑ 53.12</td><td>↑ 30.89</td><td>↑ 76.16</td><td>↓ 84.14</td><td>↑</td><td>↑</td><td>↑</td><td>↓</td><td>↑</td><td>↑ 59.95</td><td>↑</td><td>↓</td><td>↓</td></tr><tr><td>ODIN [17]</td><td>52.56</td><td>30.29</td><td>75.96</td><td>84.26</td><td>54.98 53.76</td><td>30.65 29.90</td><td>78.80 78.40</td><td>81.55 81.65</td><td>75.64 77.53</td><td>62.92</td><td>88.17 88.98</td><td>75.49 75.02</td><td>64 255</td></tr><tr><td>ENERGY [23]</td><td>39.00</td><td>23.45</td><td>67.11</td><td>92.73</td><td>52.68</td><td>29.70</td><td>76.33</td><td>86.46</td><td>72.56</td><td>52.78</td><td>86.61</td><td>78.35</td><td>64</td></tr><tr><td>OE [27]</td><td>53.43</td><td>29.83</td><td>72.05</td><td>95.58</td><td>56.67</td><td>29.41</td><td>79.47</td><td>82.91</td><td>69.63</td><td>39.91</td><td>86.36</td><td>70.76</td><td>63</td></tr><tr><td>REACT [24]</td><td>50.55</td><td>31.00</td><td>68.02</td><td>99.15</td><td>48.76</td><td>27.02</td><td>72.97</td><td>90.73</td><td>56.81</td><td>29.75</td><td>78.69</td><td>86.44</td><td>65</td></tr><tr><td>GRADNORM [25]</td><td>77.77</td><td>61.03</td><td>88.46</td><td>70.45</td><td>90.25</td><td>76.51</td><td>95.78</td><td>34.01</td><td>100</td><td>98.95</td><td>99.60</td><td>0</td><td>191</td></tr><tr><td>MAXLOGIT [26]</td><td>48.58</td><td>28.51</td><td>70.92</td><td>92.32</td><td>51.82</td><td>28.97</td><td>74.77</td><td>91.04</td><td>60.01</td><td>33.10</td><td>81.46</td><td>82.10</td><td>64</td></tr><tr><td>KL [26]</td><td>52.75</td><td>31.67</td><td>72.10</td><td>92.57</td><td>57.28</td><td>32.49</td><td>77.90</td><td>88.20</td><td>67.99</td><td>41.06</td><td>85.25</td><td>76.37</td><td>63</td></tr><tr><td>FOOD</td><td>98.40</td><td>97.08</td><td>99.24</td><td>8.93</td><td>97.90</td><td>97.31</td><td>97.72</td><td>6.14</td><td>99.25</td><td>98.45</td><td>99.67</td><td>3.20</td><td>5</td></tr></table>

Table 3: Ablation study for OOD detection. All values are shown in percentages. ↑ indicates that higher values are better, while ↓ indicates that lower values are better.
<table><tr><td rowspan="2"></td><td colspan="4">PER1</td><td colspan="4"> $\mathrm { P E R _ { 2 } }$ </td><td colspan="4">PER3</td></tr><tr><td>AUROC ↑</td><td>AUPRIN ↑</td><td> $\mathbf { A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td><td>↑</td><td>AUROC AUPRIN ↑</td><td> $\mathbf { A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td><td>AUROC AUPRIN ↑</td><td>↑</td><td> $\mathbf { A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td></tr><tr><td>CL</td><td>94.21</td><td>90.15</td><td>97.09</td><td>32.47</td><td>93.25</td><td>89.75</td><td>94.75</td><td>37.16</td><td>94.99</td><td>91.22</td><td>97.52</td><td>29.24</td></tr><tr><td> $\mathrm { C L + P L s }$ </td><td>98.40</td><td>97.08</td><td>99.24</td><td>8.93</td><td>97.90</td><td>97.31</td><td>97.72</td><td>6.14</td><td>99.25</td><td>98.45</td><td>99.67</td><td>3.20</td></tr></table>

Table 4: Ablation study for classification.
<table><tr><td rowspan="2"></td><td colspan="3">Accuracy</td><td rowspan="2">Average Accuracy</td></tr><tr><td>PER1</td><td>PER2</td><td>PER3</td></tr><tr><td>MP</td><td>59.14</td><td>44.33</td><td>99.42</td><td>67.01</td></tr><tr><td> ${ \bf M P + P L s }$ </td><td>94.82</td><td>99.70</td><td>100</td><td>98.07</td></tr></table>

## 6. CONCLUSION

This paper presents an innovative framework for short-range FMCW radar-based face authentication and OOD detection. The proposed pipeline accurately classifies ID samples and effectively prevents inaccurate predictions for OOD samples. The reconstruction-based architecture, featuring a main convolutional one-encoder multi-decoder and intermediate linear one-encoder one-decoder components, contributes to a highly accurate human face classifier and a robust OOD detector. Our network achieves 98.07% average classification accuracy for ID human faces and 98.50% average AUROC as an OOD detector, surpassing previous SOTA approaches. Despite initially using three ID classes, the flexible structure of FOOD allows easy expansion to classify as many ID human faces as needed.

![](images/13ec3c31509cefd945ca80f39724f107bfb7d2018e609e2236280ffb5635ac5d.jpg)  
Fig. 2: Confusion matrix to demonstrate the classification performance of FOOD.

## 7. REFERENCES

[1] Prateek Nallabolu, Li Zhang, Hong Hong, and Changzhi Li, “Human presence sensing and gesture recognition for smart home applications with moving and stationary clutter suppression using a 60-ghz digital beamforming fmcw radar,” IEEE Access, vol. 9, pp. 72857–72866, 2021.

[2] Thomas Stadelmayer, Markus Stadelmayer, Avik Santra, Robert Weigel, and Fabian Lurz, “Human activity classification using mmwave fmcw radar by improved representation learning,” in Proceedings of the 4th ACM Workshop on Millimeter-Wave Networks and Sensing Systems, New York, NY, USA, 2020, mmNets’20, Association for Computing Machinery.

[3] Cem Yusuf Aydogdu, Souvik Hazra, Avik Santra, and Robert Weigel, “Multi-modal cross learning for improved people counting using shortrange fmcw radar,” in 2020 IEEE International Radar Conference (RADAR), 2020, pp. 250–255.

[4] Souvik Hazra and Avik Santra, “Robust gesture recognition using millimetric-wave radar system,” IEEE Sensors Letters, vol. 2, no. 4, pp. 1–4, 2018.

[5] Muhammad Arsalan, Avik Santra, and Christoph Will, “Improved contactless heartbeat estimation in fmcw radar via kalman filter tracking,” IEEE Sensors Letters, vol. 4, no. 5, pp. 1–4, 2020.

[6] Qing Yu and Kiyoharu Aizawa, “Unsupervised out-of-distribution detection by maximum classifier discrepancy,” in IEEE/CVF International Conference on Computer Vision (ICCV), 2019.

[7] Chandramouli Shama Sastry and Sageev Oore, “Detecting out-ofdistribution examples with Gram matrices,” in International Conference on Machine Learning (ICML), 2020.

[8] Jingkang Yang, Haoqi Wang, Litong Feng, Xiaopeng Yan, Huabin Zheng, Wayne Zhang, and Ziwei Liu, “Semantically coherent out-ofdistribution detection,” in IEEE International Conference on Computer Vision (ICCV), 2021.

[9] Haoqi Wang, Zhizhong Li, Litong Feng, and Wayne Zhang, “Vim: Out-of-distribution with virtual-logit matching,” arXiv, 2022.

[10] Hae-Seung Lim, Jaehoon Jung, Jae-Eun Lee, Hyung-Min Park, and Seongwook Lee, “Dnn-based human face classification using 61 ghz fmcw radar sensor,” IEEE Sensors Journal, vol. 20, no. 20, pp. 12217– 12224, 2020.

[11] J. Kim, J.-E Lee, H.-S Lim, and S. Lee, “Face identification using millimetre-wave radar sensor data,” Electronics Letters, vol. 56, 08 2020.

[12] Eran Hof, Amichai Sanderovich, Mohammad Salama, and Evyatar Hemo, “Face verification using mmwave radar sensor,” in 2020 International Conference on Artificial Intelligence in Information and Communication (ICAIIC), 2020, pp. 320–324.

[13] Muralidhar Reddy Challa, Abhinav Kumar, and Linga Reddy Cenkeramaddi, “Face recognition using mmwave radar imaging,” in 2021 IEEE International Symposium on Smart Electronic Systems (iSES), 2021, pp. 319–322.

[14] Ha-Anh Pho, Seongwook Lee, Vo-Nguyen Tuyet-Doan, and Yong-Hwa Kim, “Radar-based face recognition: One-shot learning approach,” IEEE Sensors Journal, vol. 21, no. 5, pp. 6335–6341, 2021.

[15] Youxuan Zhong, Chun Yuan, Yi Zou, and Heng Yao, “Face recognition based on point cloud data captured by low-cost mmwave radar sensors,” in 2023 IEEE 13th Annual Computing and Communication Workshop and Conference (CCWC), 2023, pp. 0074–0083.

[16] Dan Hendrycks and Kevin Gimpel, “A baseline for detecting misclassified and out-of-distribution examples in neural networks,” in International Conference on Learning Representations (ICLR), 2017.

[17] Shiyu Liang, Yixuan Li, and R. Srikant, “Enhancing the reliability of out-of-distribution image detection in neural networks,” in International Conference on Learning Representations (ICLR), 2018.

[18] Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell, “Simple and scalable predictive uncertainty estimation using deep ensembles,” in Advances in Neural Information Processing Systems. 2017, vol. 30, Curran Associates, Inc.

[19] Y. C. Hsu, Y. Shen, H. Jin, and Z. Kira, “Generalized odin: Detecting out-of-distribution image without learning from out-of-distribution data,” in IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020.

[20] Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin, “A simple unified framework for detecting out-of-distribution samples and adversarial attacks,” in International Conference on Neural Information Processing Systems (NeurIPS), 2018.

[21] Haiwen Huang, Zhihan Li, Lulu Wang, Sishuo Chen, Bin Dong, and Xinyu Zhou, “Feature space singularity for out-of-distribution detection,” in Proceedings of the Workshop on Artificial Intelligence Safety 2021 (SafeAI 2021), 2021.

[22] Yiyou Sun, Yifei Ming, Xiaojin Zhu, and Yixuan Li, “Out-ofdistribution detection with deep nearest neighbors,” in International Conference on Machine Learning (ICML), 2022.

[23] Weitang Liu, Xiaoyun Wang, John Owens, and Yixuan Li, “Energybased out-of-distribution detection,” in Advances in Neural Information Processing Systems (NeurIPS), 2020.

[24] Yiyou Sun, Chuan Guo, and Yixuan Li, “React: Out-of-distribution detection with rectified activations,” in Advances in Neural Information Processing Systems (NeurIPS), 2021.

[25] Rui Huang, Andrew Geng, and Yixuan Li, “On the importance of gradients for detecting distributional shifts in the wild,” in Advances in Neural Information Processing Systems (NeurIPS), 2021.

[26] Dan Hendrycks, Steven Basart, Mantas Mazeika, Andy Zou, Joe Kwon, Mohammadreza Mostajabi, Jacob Steinhardt, and Dawn Song, “Scaling out-of-distribution detection for real-world settings,” International Conference on Machine Learning (ICML), 2022.

[27] Dan Hendrycks, Mantas Mazeika, and Thomas Dietterich, “Deep anomaly detection with outlier exposure,” in International Conference on Learning Representations (ICLR), 2019.

[28] Aristotelis-Angelos Papadopoulos, Mohammad Reza Rajati, Nazim Shaikh, and Jiamian Wang, “Outlier exposure with confidence control for out-of-distribution detection,” Neurocomputing, vol. 441, pp. 138–150, 2021.

[29] Sabri Mustafa Kahya, Muhammet Sami Yavuz, and Eckehard Steinbach, “Reconstruction-based out-of-distribution detection for shortrange fmcw radar,” in 2023 31st European Signal Processing Conference (EUSIPCO), 2023, pp. 1350–1354.

[30] Sabri Mustafa Kahya, Muhammet Sami Yavuz, and Eckehard Steinbach, “Mcrood: Multi-class radar out-of-distribution detection,” in ICASSP 2023 - 2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2023, pp. 1–5.

[31] Sabri Mustafa Kahya, Muhammet Sami Yavuz, and Eckehard Steinbach, “Hood: Real-time robust human presence and out-of-distribution detection with low-cost fmcw radar,” arXiv, 2023.

[32] Sabri Mustafa Kahya, Muhammet Sami Yavuz, and Eckehard Steinbach, “Harood: Human activity classification and out-of-distribution detection with short-range fmcw radar,” in ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2024, pp. 6950–6954.

[33] Diederik P. Kingma and Jimmy Ba, “Adam: A method for stochastic optimization,” arXiv preprint arXiv:1412.6980, 2014.

[34] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun, “Deep residual learning for image recognition,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016.