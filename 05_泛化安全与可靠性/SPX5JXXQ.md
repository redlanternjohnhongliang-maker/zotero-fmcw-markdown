# HOOD: Real-Time Human Presence and Out-of-Distribution Detection Using FMCW Radar

Sabri Mustafa Kahya , Graduate Student Member, IEEE, Muhammet Sami Yavuz and Eckehard Steinbach , Fellow, IEEE

Abstract— Detecting human presence indoors with millimeterwave frequency-modulated continuous-wave (FMCW) radar faces challenges from both moving and stationary clutters. This work proposes a robust and real-time capable human presence and out-of-distribution (OOD) detection method using 60-GHz short-range FMCW radar. HOOD solves the human presence and OOD detection problems simultaneously in a single pipeline. Our solution relies on a reconstruction-based architecture and works with radar macro- and micro-range–Doppler images (RDIs). HOOD aims to accurately detect the presence of humans in the presence or absence of moving and stationary disturbers. Since HOOD is also an OOD detector, it aims to detect moving or stationary clutters as OOD in humans’ absence and predicts the current scene’s output as “no presence.” HOOD performs well in diverse scenarios, demonstrating its effectiveness across different human activities and situations. On our dataset collected with a 60-GHz short-range FMCW radar with only one transmit (Tx) and three receive antennas, we achieved an average area under the receiver operating characteristic curve (AUROC) of 94.36%. Additionally, our extensive evaluations and experiments demonstrate that HOOD outperforms state-of-the-art (SOTA) OOD detection methods in terms of common OOD detection metrics. Importantly, HOOD also perfectly fits on Raspberry Pi 3B+ with a advanced RISC machines (ARM) Cortex-A53 CPU, which showcases its versatility across different hardware environments. Videos of our human presence detection experiments are available at: https://muskahya.github.io/HOOD.

Index Terms— 60-GHz frequency-modulated continuous-wave (FMCW) radar, deep neural networks, human presence detection, out-of-distribution (OOD) detection.

## I. INTRODUCTION

N RECENT years, radars have gained huge attention among other types of sensors due to their robustness against environmental conditions such as lighting, smoke, and rain, as well as their privacy-preserving nature. Therefore, they are utilized for several applications such as reliable detection and interpretation of human gestures [1], [2], [3], [4], extracting vital signs such as heart rate and respiration rate [5], [6], [7], accurate human activity classification [8], [9], [10], and real-time people counting in various environments [11], [12], [13]. These applications cover multiple areas, particularly in human–computer interaction (HCI) and the Internet of Things (IoT). Here, they are crucial for improving smart home automation, healthcare monitoring, and other IoT solutions. Incorporating radar technology into IoT applications is key to creating smarter environments, boosting both efficiency and safety. Notably, detecting human presence is an important application in this context that takes advantage of radar’s distinctive abilities.

Real-time and robust human presence detection solutions using radars can enhance safety, energy efficiency, and personalized experiences. For instance, frequency-modulated continuous-wave (FMCW) radar-based human presence detection systems can detect threats and unauthorized access indoors, enhancing security in restricted areas. Integration in smart homes enhances personalized experiences and improves energy efficiency by automatically adjusting environmental settings such as lighting and heating based on accurate human presence detection.

In addition, human presence detection utilizing short-range radar sensors presents its own challenges. In real-world scenarios, both indoor and outdoor environments, there are many moving and stationary disturbances. With these disturbances present, extracting the signals coming from humans becomes challenging. In nonhuman environments, disturbers’ macro- or micromovements may produce human-like signals and create false detections for human presence detection applications. In [14], we addressed this issue and proposed an out-ofdistribution (OOD) detection-based solution that can identify and differentiate between a disturber and a human (sitting, standing, or walking) only when either of them is present in front of the radar sensor. However, when both disturbers and humans are in front of the sensor, the reflected signals from the disturbers may interfere with those from humans. The previous work mentioned was incapable of solving this issue and tended to classify the scenario as OOD due to the signal dominance of disturbers. This work addresses every edge case and proposes a robust presence detection solution. Similarly, this work approaches the issue as an OOD detection problem.

OOD detection has gained significant attention due to its crucial role in ensuring the secure and reliable deployment of modern deep learning (DL) architectures. Despite the impressive performance of DL models in various applications, they often make closed-world assumptions, which are unrealistic in real-world scenarios. This can result in the misclassification of OOD samples, potentially leading to severe consequences in safety-critical domains such as healthcare and autonomous driving. To address this challenge, researchers have developed various OOD detection strategies [15], [16], [17], [18], [19], which primarily focused on image or video data. In this article, we propose a reconstruction-based approach by utilizing radar macro- and micro-range–Doppler images (RDIs) for improved OOD detection in the radar domain.

OOD methods typically do not incorporate OOD samples during training. Therefore, their pipelines are never exposed to samples outside the training distribution. Moreover, these methods do not evaluate their performance using samples that simultaneously contain both in-distribution (ID) and OOD classes. In this work, in addition to samples containing only IDs, we also leverage samples that consist of both IDs and OODs (ID + OOD is also ID in our case). This approach enables us to detect IDs even in the presence of OODs, aiming to enhance the overall detection capability. This article introduces a new DL architecture designed for human and OOD detection. Additionally, we incorporate an enhanced respiration detector (E-RESPD) [14] technique as a preprocessing method to detect tiny and almost invisible human body movements in addition to respiration movement, thereby facilitating the human and OOD detection process. With the utilization of E-RESPD, the detection of humans remains possible even in cases where individuals intentionally hold their breath. HOOD relies on a reconstruction-based architecture that comprises a multiencoder multidecoder system and E-RESPD. Generally, OOD detectors employ simple thresholding for detection, where a threshold is defined based on a scoring function to classify samples as either ID or OOD. HOOD utilizes multithresholding to detect humans in the presence or absence of OODs and to detect OODs themselves. We divide the human detection process into two categories, namely, static human(s) like standing and very-static human(s) like sitting and lying. Dynamic human movement walking has a unique and dominant signature that is easily detectable in the presence or absence of disturbers using conventional signal processing or learning-based approaches. Therefore, we do not include the walking scenario in this work. For this, we refer to our previous work that shows superior performance on the walking scenario [14]. Our key contributions are as follows.

1) We propose a novel human presence detector called HOOD, which utilizes a reconstruction-based architecture and operates on radar macro- and micro-RDIs. The architecture is composed of a multiencoder multidecoder system. Each encoder–decoder pair collaboratively focuses on detecting static and very-static human(s) with the assistance of micro-RDIs. Additionally, for scenarios where humans exhibit macromovements like hand waving when they are static or very-static, HOOD employs macro-RDIs for detection. HOOD is a versatile human detector that does not rely on predefined classes and can detect humans engaged in various activities.

2) We propose HOOD as an effective OOD detector in addition to its role as a human presence detector. HOOD can identify both moving and stationary clutter in scenarios where no human presence is detected, classifying them as OOD samples.

3) We introduce E-RESPD as an improved iteration of RESPD. By integrating E-RESPD, we achieve enhanced detection of human respiration movement. It can also accurately capture minute and nearly invisible body movements, even when individuals intentionally refrain from breathing. This concept improves the overall classification performance.

In the following section, we discuss relevant previous work. Section III explains radar system design and preprocessing including E-RESPD. Section IV delves into the details of our proposed method, outlining its key components and methodologies. Section V presents the experiments conducted to validate our approach, including the experimental setup, data collection, and analysis. Finally, Section VI draws conclusions and suggests future research directions.

## II. RELATED WORK

In the literature, there are several radar-based human presence detection works [20], [21]. These works mostly utilize conventional signal processing approaches. Deiana et al. [22] described a real-time presence detection pipeline using 24-GHz FMCW radar in an office environment. The method aims to detect tiny human body movements like typing. However, it does not evaluate complete static human scenarios. Santra et al. [23] proposed an occupancy sensing application with 60-GHz FMCW radar for heating, ventilation, and air-conditioning (HVAC) systems. They created a novel pipeline to detect vital, micro-, and macro-Doppler movement from various human activities. Xiao et al. [24] proposed a transformer-based solution also for occupancy sensing. In [25], the proposed solution aims to detect the presence only by minute movements of breathing. They tested their pipeline only with sleeping babies and sitting adults. The studies mentioned earlier aim to identify the presence of people using unique methods. However, they overlook both moving and stationary clutter, which is common in indoor and outdoor environments in the real world. Chang et al. [26] described a presence detection method using a ultra-wideband (UWB) radar by considering outdoor disturbers. The algorithm uses the human body’s scattered UWB waveforms to detect the human target(s) in urban environments. However, its classical likelihood ratios-based detection pipeline requires dynamic human motion, and it is tested only with cars as outdoor disturbers. Chang et al. [27] developed an improved pipeline to simultaneously detect and track multiple human and nonhuman targets by only considering walking person activity. In their experiments, they only use an aluminum foil-covered basketball representing a small moving animal as a nonhuman object. Xia et al. [28] proposed a convolutional neural network (CNN)-based detection and displacement network for human target tracking. For detecting standing or lying individuals in the presence of clutters, Kim et al. [29] developed a two-stage detection algorithm using a UWB radar. It includes initial detection in the range domain and subsequent detection in the frequency domain. Similarly, for a human presence detection application, Nallabolu et al. [30] proposed a novel moving and stationary clutter suppression technique to identify the characteristic respiratory signal better. Luo and Li [31] utilized standard deviation weighting for human target detection with FMCW radar. Recently, Peng et al. [32] proposed a reconstruction-based framework for human detection with the same radar type. Cha et al. [33] and Dadon et al. [34] introduced classification-based solutions for human presence detection, leveraging deep CNNs and two-layer CNNs, respectively. This work is an activity-free human presence detector and detects human(s) in the presence or absence of various disturbers. Different from the literature, we approach the human presence detection task as an OOD detection problem.

The field of OOD detection is relatively new. A foundational work by Hendrycks and Gimpel [35] introduces the baseline method, which relies on maximum softmax probabilities (MSPs). Their main assertion is that deep neural networks assign higher confidence values to ID samples compared to OOD samples during inference. As a result, a simple thresholding technique can be used to differentiate between ID and OOD samples. The ODIN approach, presented in [36], enhances [35] by incorporating temperature scaling and input perturbations to amplify the softmax scores of ID samples. This approach is further extended by introducing a model ensembling technique [37]. In a different study, Liu et al. [38] proposed an energy-based method for OOD detection, employing the LogSumExp function on the logit layer and noting that ID samples tend to have lower energy scores than OOD samples. The Mahalanobis distance-based detector (MAHA) [39] is designed to identify OOD samples by leveraging intermediate feature representations of deep neural networks. MAHA constructs a class conditional Gaussian distribution for each ID class and evaluates the Mahalanobis distance between a test sample and each class conditional Gaussian distribution to calculate an OOD score. Additionally, MAHA incorporates layer ensembling and input perturbation techniques.

Similarly, Sastry and Oore [40] and Ren et al. [41] employ intermediate representations for OOD detection. Hendrycks et al. [42] introduced two different methods relying on maximum logit and minimum KL divergence information. ReAct [43] addresses overconfident predictions by employing activation truncation on the penultimate layer, whereas DICE [44] uses weight sparsification for OOD detection. Huang et al. [45] introduced uniform noise and argued that OOD samples resemble noise more closely than ID samples. To estimate the OODs using the distance information, Sun et al. [46] adopt a deep-nearest-neighbor approach. Similarly, Park et al. [47] proposed a nearest neighbor guidance method for improved near OOD detection. While the aforementioned methods are compatible with any pretrained model, some require OOD samples for hyperparameter tuning. G-ODIN [48] introduced an enhanced training scheme built upon [36] to achieve improved detection capabilities. Hendrycks et al. [49] proposed the outlier exposure (OE) technique, which involves integrating a limited number of OOD samples during the fine-tuning or training process. They introduced a novel loss function that promotes the convergence of softmax probabilities for OOD samples toward a uniform distribution. OECC [50] follows a similar approach with the inclusion of a novel loss function consisting of two distinct regularization terms. In [51], a generative adversarial network (GAN) architecture is utilized, along with a specialized loss function, to generate synthetic OOD samples for OE. Moreover, other studies [52], [53] in the literature also benefit from OOD samples to provide more powerful OOD detectors. The significance of gradient information in the OOD detection task is highlighted in some studies [36], [54]. GradNorm [54] leverages the magnitudes of gradients to differentiate between ID and OOD samples. To compute the gradients, the KL divergence between the softmax output and a uniform distribution is backpropagated. According to this approach, ID samples exhibit higher gradient magnitudes compared to OOD samples. Bai et al. [55] proposed a hyperspherical learning algorithm to detect OODs in hyperspherical space. Ming et al. [56] also benefit from hyperspherical embeddings by jointly optimizing dispersion and compactness losses for OOD detection.

In a reconstruction-based method [57] that utilizes autoencoders, a combination of the reconstruction loss and Mahalanobis distance in the latent code is used as an OOD score. Other studies, such as [58] and [59], utilize variational autoencoders (VAEs) and their latent representations for OOD detection. Although most OOD detection methods rely on CNN architectures, there are also notable alternatives, such as the approaches mentioned in [60], [61], and [62], which employ pretrained transformers with attention mechanisms such as VIT [63] and BERT [64]. These transformer-based methods have achieved state-of-the-art (SOTA) results on various benchmark datasets.

In addition to the previously mentioned studies, several other approaches have been proposed within the radar domain for OOD detection. Kahya et al. [65] introduced a reconstruction-based OOD detector specifically designed for 60-GHz FMCW radar. They aim to distinguish a walking human from various moving disturbers. The proposed method utilizes two scores, incorporating patch-based reconstruction and energy scores, for OOD detection. Kahya et al. [14] proposed MCROOD as a multiclass radar OOD detector that tries to detect any clutter other than a human sitting, standing, or walking as OOD. It relies on a reconstruction-based oneencoder multidecoder architecture and a simple prepossessing idea RESPD. For OOD detection, it uses multithresholding. In [66], a hand gesture recognition system was introduced that utilizes FMCW radar technology and incorporates the capability to identify OOD input data. In [67], a comparison is made between traditional and DL techniques for near OOD detection, utilizing synthetically generated low-resolution radar micro-Doppler signatures. Additionally, Ott et al. [68] presented a meta-reinforcement learning approach that enhances radar tracking reliability and includes support for OOD detection.

## III. RADAR SYSTEM DESIGN

The research presented in this article utilizes the FMCW radar chipset provided by Infineon, known as BGT60TR13C. This radar chipset, operating at a frequency range of 57–64 GHz, offers the ability to customize the chirp duration (T<sub>c</sub>). The radar chipset has one transmit (Tx) antenna and three receiver (Rx) antennas. The Rx antennas are arranged in an L-shape configuration, and the distance between neighboring receiving antennas is half-wavelength. The gain of each receive and Tx antenna is 10 and 6 dBi, respectively.

The chipset follows the fundamental principles of FMCW radar. The reference frequency $\begin{array} { c c l } { ( f _ { \mathrm { r e f } } } & { = } & { 8 0 ~ \mathrm { M H z } ) } \end{array}$ of a voltage-controlled oscillator (VCO) is maintained by a phase-locked loop (PLL) in the transmission path. By modifying the divider value and using a tuning voltage within the range of 1–4.5 V, the chipset generates precise linear frequency chirps $( N _ { c } )$ from 57 to 64 GHz. The transmitted signal (chirp signal) in an FMCW system is given by

$$
s ( t ) = \exp \Biggl ( j 2 \pi \Biggl ( f _ { c } t + \frac { S } { 2 } t ^ { 2 } \Biggr ) \Biggr ) \quad \forall 0 < t < T _ { c }\tag{1}
$$

where $f _ { c }$ is the center frequency, and S is the chirp rate (frequency sweep rate) calculated as the ratio of the signal bandwidth B to the chirp duration $[ S = ( B / T _ { c } ) ]$ . The transmitted signal is backscattered by objects in the environment, resulting in a time delay, i.e., round trip delay due to the range of the target from the radar and its velocity. The receive antennas capture the delayed signal. A mixture of received and transmitted signals undergoes a low-pass filter to acquire the intermediate frequency (IF) signal, which is then used to apply analog-to-digital converter (ADC) with a sampling frequency of 2 MHz with 12-bit accuracy. The data are reorganized and molded into a frame referred to as $N _ { c } \times N _ { s }$ . Within this frame, each column comprises $N _ { c }$ samples denoted as slowtime samples, while each row consists of $N _ { s }$ samples known as fast-time samples. This configuration applies to a total of three receiving antennas. As a result, the digitized signal takes on the shape of $N _ { \mathrm { { R x } } } \times N _ { c } \times N _ { s }$ , making it ready for further signal processing.

The FMCW radar configuration for this study is provided in Table I. This setup achieves a range resolution of

$$
\delta r = \frac { c } { 2 B } = 1 5 \ \mathrm { c m }\tag{2}
$$

where c, the speed of light, is approximately $3 \times 1 0 ^ { 8 }$ m/s. Consequently, the maximum unambiguous range is computed as

$$
R _ { \mathrm { m a x } } = \frac { N _ { s } } { 2 } \times \delta r = 9 . 6 ~ \mathrm { m } .\tag{3}
$$

Additionally, the maximum velocity that can be measured is

$$
v _ { \mathrm { m a x } } = { \frac { c } { 2 f _ { c } T _ { \mathrm { c c } } } } \approx 6 . 3 8 ~ \mathrm { m / s }\tag{4}
$$

and the velocity resolution is

$$
\delta v = { \frac { c } { 2 f _ { c } \big ( { \frac { N _ { c } } { 2 } } \big ) T _ { \mathrm { c c } } } } \approx 0 . 2 0 \ \mathrm { m / s } .\tag{5}
$$

## A. Preprocessing

In this study, we utilize both macro- and micro-RDIs for our architecture. These RDIs are generated by applying preprocessing operations to the digitized signal $( N _ { \mathrm { { R x } } } \times N _ { c } \times N _ { s } )$

For the extraction of the macro-RDI, we initially apply the range-fast Fourier transform (FFT) on the fast time to determine the object’s range. Mean removal is also performed to obtain one channel range information out of three Rx channels. The range data are then processed using the moving target identification (MTI) function, which effectively eliminates static targets. Finally, we apply Doppler-FFT along the slow time to capture the phase across chirps, allowing us to obtain the desired macro-RDI with the dimension of $6 4 \times 6 4$

TABLE I  
FMCW RADAR CONFIGURATION PARAMETERS  
![](images/2721f23eee2122e3f32508ab97cc8a75d0758252466434333e104d0a1d5d11d5.jpg)  
Fig. 1. Preprocessing pipeline to have macro- and micro-RDIs.

To extract the micro-RDI, we begin with the range-FFT to obtain range information. To capture more detailed information, we stack eight range spectrograms. Additionally, mean removal is performed in both the fast and slow times to reduce noise. We further enhance the target signals by applying Sinc filtering. Finally, Doppler-FFT along the slow time is utilized to identify target movement in the micro-RDI (64 × 64). For a visual explanation of our preprocessing steps, please refer to Fig. 1.

## B. E-RESPD

RESPD [14] is a preprocessing technique designed for RDIs. Its objective is to capture the human respiration movement by utilizing 50 consecutive frames, equivalent to 2.5 s in the radar configuration. This is accomplished through a sliding-window approach with a window size of 50 frames. Within each window, the frames are summed, and the resulting value is written onto the first frame of the window. The window is then shifted by one frame, and the process is repeated until the end of the recording.

The E-RESPD, on the other hand, operates on both macroand micro-RDIs. In E-RESPD, the window size is increased from 50 to 200 frames, representing 10 s in the radar configuration, enabling the modeling of subtle and nearly imperceptible human body movements. This includes scenarios such as detecting movements when a person intentionally holds his breath. In our radar configuration, the frame-to-frame time is only 5 ms (0.005 s), making it challenging to infer the presence of especially static individuals when performing framewise evaluation. Therefore, with the help of E-RESPD, we process consecutive 200 frames (10 s of data) at once, allowing us to capture the presence of a person, even when they intentionally become more static than normal. Fig. 2 provides a detailed illustration of the overall working mechanism of E-RESPD, and Algorithm 1 demonstrates its simple pseudocode. To illustrate the application of E-RESPD with a concrete example, consider a set of micro-RDIs obtained from a recording session, with the dimensions of $2 2 0 0 \times 6 4 \times 6 4$ (2200 is the number of frames in the recording). We will focus on the micro-RDI and describe the usage of the E-RESPD process, which applies similar to macro-RDIs. Given a window size of 200 frames, we begin with the first 200 frames, summing them to create a new frame. Specifically, we compute

![](images/a460bc2db2a4038a22069932cbce7bcef262fa5527c4fef7420276a2dbac9ff8.jpg)

![](images/d2356df68f36cde48ba92dedb232d922f622e89d1b591d2a7fad7f9f8cdc8729.jpg)

Fig. 2. Overview of the HOOD architecture (top) and a detailed view of an encoder–decoder pair (bottom), illustrating the reconstruction-based processing of radar macro- and micro-RDIs for static and very-static activities. The four decoders, in top-to-bottom order, decode macro-RDIs for static activities, macro-RDIs for very-static activities, micro-RDIs for static activities, and micro-RDIs for very-static activities, also having identical structures.  
![](images/427afc10a564c01562588a7e8d1d020fe1b6d6c03b0044adec44f866320dcc93.jpg)  
Fig. 3. Illustration of the E-RESPD process for preprocessing macro- and micro-RDIs. To improve respiration detection, a sliding-window approach with a size of 200 frames is used, representing 10 s of radar data acquisition. The process begins with the summation of the first 200 frames to create a new frame, referred to as $\mathrm { F r a m e } _ { \mathrm { n e w } \_ 1 } .$ , which captures the cumulative signal across these frames, resulting in a single frame with dimensions $6 4 \times 6 4$ . The window is then shifted by one frame, and the sum of the subsequent 200 frames produces $\mathrm { F r a m e } _ { \mathrm { n e w } \_ 2 } .$ . This summation process continues until the end of the recording, producing a new set of frames.

$$
\mathrm { F r a m e } _ { \mathrm { n e w } _ { - } 1 } = \mathrm { F r a m e } _ { 1 } + \mathrm { F r a m e } _ { 2 } + \cdot \cdot \cdot + \mathrm { F r a m e } _ { 2 0 0 } .\tag{6}
$$

This operation is a standard matrix summation across frames, resulting in a new frame with dimensions of $6 4 \times 6 4 .$ . Thus, $\mathrm { F r a m e } _ { \mathrm { n e w } _ { - } 1 }$ becomes the first frame of our processed data.

Algorithm 1 Processing RDI and Micro-RDI Sequences With E-RESPD

1) Load RDI and micro RDI data from their respective files.

2) Define parameters:

a) overlap ← 199: Number of frames overlapping between consecutive sequences.

b) sequence\_length ← 200: Total number of frames in each sequence (window).

3) Create an index array to extract sequences:

a) Generate indices for sequences, ensuring that each sequence has 200 frames with a 199-frame overlap between consecutive sequences.

4) Initialize empty arrays to store results:

a) Create an array to store the summed RDI sequences, where each sequence will have a size of 64 $\times ~ 6 4 .$

b) Create an array to store the summed micro RDI sequences with the same dimensions.

5) Process each sequence:

a) For each sequence of frames:

i) For each frame in the sequence:

A) Add the corresponding RDI frame to the current sequence sum.

B) Add the corresponding micro RDI frame to the current sequence sum.

6) Save the final summed sequences to new output files.

Next, we shift the window by one frame and perform the same operation

$$
\mathrm { F r a m e } _ { \mathrm { n e w } _ { - } 2 } = \mathrm { F r a m e } _ { 2 } + \mathrm { F r a m e } _ { 3 } + \cdot \cdot \cdot + \mathrm { F r a m e } _ { 2 0 1 } .\tag{7}
$$

This process is repeated until we reach the end of the recording. Ultimately, we produce a new set of frames with dimensions 2000 × 64 × 64, consisting of

$$
\mathrm { F r a m e } _ { \mathrm { n e w } _ { - } 1 } , \mathrm { F r a m e } _ { \mathrm { n e w } _ { - } 2 } , \dots , \mathrm { F r a m e } _ { \mathrm { n e w } _ { - } 2 0 0 0 } .\tag{8}
$$

This results in a smoother representation of the underlying movements captured in both macro- and micro-RDIs, enhancing the ability to detect subtle changes and improving the effectiveness of subsequent analysis.

## IV. PROPOSED METHOD

In this section, we provide a detailed explanation of our human and OOD detector, HOOD (see Fig. 3). HOOD utilizes a reconstruction-based multiencoder multidecoder architecture, combining multiple encoders and decoders for robust presence detection. By training on scenarios, including static and very-static human activities with and without disturbers, our model learns to generalize the solution across various cases. We employ a multithresholding technique based on reconstruction errors to classify samples as human or OOD. The architecture, training process, and algorithmic implementation of HOOD are presented in detail in Sections IV-A and IV-B.

## A. Architecture and Training

HOOD relies on a reconstruction-based multiencoder (two) multidecoder (four) architecture. Each encoder shares the same architecture, while each decoder also follows an identical structure. The encoders are responsible for encoding the macro- and micro-RDIs, respectively. On the other hand, the decoders are responsible for decoding the macroand micro-RDIs of the static and very-static categories. The encoder architecture consists of three primary blocks. The initial two blocks involve the sequential application of 2-D convolution, followed by 2-D batch normalization and LeakyReLU activation. In these blocks, we, respectively, employ 16 and 64 filters with $\textbf { a } \ 3 \ \times \ 3$ kernel size for the convolutional layers. Downsampling is achieved in those blocks with a stride of $2 \times 2 .$ . The final block incorporates flattening and fully connected (dense) layers, followed by 1-D batch normalization, to generate the latent representation. On the other hand, the decoder architecture comprises four primary blocks. In the first block, the latent code undergoes through a fully connected layer with 1-D batch normalization. Subsequently, two blocks are sequentially applied for 2-D transpose convolution, followed by 2-D batch normalization and LeakyReLU activation. The fourth block includes a 2-D convolutional layer with sigmoid activation. In the middle blocks, respectively, 64 and 16 filters are utilized for the transpose convolutional layers, with a $3 \times 3$ kernel size and a stride of $2 \times 2$ for upsampling. The final convolution block employs a single filter with a $3 \times 3$ kernel size without any upsampling or downsampling.

We simultaneously train our multiencoder multidecoder architecture for each encoder and decoder, ensuring optimal performance. During training, for static and very-static activities in the presence or absence of disturbers, we only use a human and a human together with a disturber in front of the radar. However, our network generalizes its capabilities to multiple humans in the presence or absence of multiple disturbers. The upper encoder handles the encoding of macro-RDIs originating from both static and very-static humans, with and without disturber(s). Similarly, the lower encoder encodes the micro-RDIs originating from static and very-static humans, also considering the presence of disturbers. On the other hand, the decoders function as follows, progressing from top to bottom: the first decoder focuses on decoding the latent representation of macro-RDIs solely from static humans and static humans in the presence of disturbers. The second decoder decodes the latent representation of macro-RDIs exclusively from very-static humans and very-static humans in the presence of disturbers. Conversely, the third decoder is responsible for decoding the latent representation of micro-RDIs solely from static humans and static humans with disturbers. Finally, the last decoder decodes the latent representation of micro-RDIs originating from very-static humans and very-static humans accompanied by disturbers.

Encoder–decoder pairs are trained specifically for static human(s) with and without disturber(s) by simulating scenarios where a human stands in various locations, exhibiting macro- and micromovements in front of the radar. Disturbers such as fans and toy robots are introduced to create realistic interference. The objective of the pairs is to accurately detect static human(s) within the range of 1–4 m, including individuals sitting closely (1–2 m) to the radar. Similarly, additional encoder–decoder pairs are trained for very-static humans with and without disturbers by simulating scenarios where a human sits in different locations, displaying macro- and micromovements in front of the radar. These pairs are designed to detect individuals engaging in very-static activities such as sitting or lying down, both in close proximity and at distances ranging from 1 to 4 m from the radar. Interestingly, even when a person is standing far from the radar (4–5 m), these pairs can still detect their presence. Although standing activity is not categorized as very-static, it generates signals resembling those of very-static individuals due to the weak signal reflection from a standing person positioned far from the radar. The encoder–decoder pairs effectively address a wide range of scenarios, accommodating various edge cases and enabling the detection of human(s) in an activity-free manner. Notably, by focusing on two fundamental human activities—sitting and standing—and incorporating a limited set of disturbers, our solution demonstrates remarkable generalization capabilities across different types of static and very-static human activities involving both micro- and macromovements, regardless of the presence or absence of diverse disturbers. Moreover, our solution extends to scenarios involving multiple individuals simultaneously engaging in different static and very-static activities. To approach the presence detection application as an OOD detection problem, we deliberately exclude the use of disturbers in the absence of humans during training. This decision ensures that scenarios lacking human presence remain outside the scope of our training distribution, which is specifically tailored to address OOD detection.

The mean-squared error (MSE) function is employed as the loss function in our approach. Since our network consists of four decoders, we aim to minimize four MSEs simultaneously. During the training phase, we utilize the Adamax optimizer [69] and apply various augmentations, including random affine transformations, flips, and scaling. These augmentations not only enhance the robustness of our solution but also contribute to its generalization capabilities. In many radar-based applications, radars are typically mounted at specific heights and tilts. However, thanks to the augmentations incorporated in our approach, our application can adapt to different reasonable heights and tilts. For example, it can operate effectively at television (TV) height without tilt in TV-based applications or be mounted on the corner of a room with a slight tilt for smart home applications.

Therefore, our loss function, as shown in (9), aims to minimize the discrepancy between the original data $\mathbf { X } ^ { ( i ) }$ and its reconstructions obtained through the encoders and decoders in our architecture. The data samples are categorized into four types: macro-RDIs of static humans (M, s), micro-RDIs of static humans (m, s), macro-RDIs of very-static humans (M, vs), and micro-RDIs of very-static humans (m, vs). The encoders, $E _ { M }$ and $E _ { m }$ , are specifically designed to encode the macro-RDIs and micro-RDIs, respectively. The decoders, $D _ { M , s } , D _ { m , s } , D _ { M , \mathrm { v s } } ,$ and $D _ { m , \mathrm { v s } }$ correspondingly decode different data categories. The MSE loss measures the average squared difference between the original data and the reconstructions over the batch (size of n). Since we have four decoders in our architecture, we obtain four MSE values representing the reconstruction losses for each data category. To formulate the overall loss function, we sum the individual MSE losses as follows:

$$
\begin{array} { r l } & { \mathcal { L } = \frac { 1 } { n } \displaystyle \sum _ { j \in \{ m , M \} } \sum _ { i = 1 } ^ { n } \Bigl ( \mathbf { X } _ { j , s } ^ { ( i ) } - D _ { j , s } \Big ( E _ { j } \Big ( \mathbf { X } _ { j , s } ^ { ( i ) } \Big ) \Big ) \Big ) ^ { 2 } } \\ & { \quad \quad + \frac { 1 } { n } \displaystyle \sum _ { j \in \{ m , M \} } \sum _ { i = 1 } ^ { n } \Bigl ( \mathbf { X } _ { j , \mathrm { v s } } ^ { ( i ) } - D _ { j , \mathrm { v s } } \Big ( E _ { j } \Big ( \mathbf { X } _ { j , \mathrm { v s } } ^ { ( i ) } \Big ) \Big ) \Big ) ^ { 2 } . } \end{array}\tag{9}
$$

## B. Human and OOD Detection

In our proposed method, we detect humans and OOD samples simultaneously within a single pipeline. We approach the human detection application as an OOD detection problem. Reconstruction-based methods for OOD sample detection rely on measuring the reconstruction error between the input and the reconstructed output. A sample is classified as OOD if its reconstruction error exceeds a predefined threshold. During the training of HOOD, we exclusively use ID samples that consist of scenarios involving humans and humans with disturbers. Consequently, we expect OOD samples containing only disturbers to exhibit higher reconstruction errors. Leveraging a multidecoder system, we employ multithresholding for analysis. Our network comprises two encoders and four decoders. The encoders receive the macro- and micro-RDIs of the same input (X) through their respective input gates. The decoders decode the encoded latent codes based on their specific responsibilities. We combine the reconstruction MSEs of macro- and micro-RDIs separately for the static and very-static human categories. For this combination, we utilize a summation of reconstruction MSEs. Subsequently, we perform multithresholding on the combined reconstruction MSEs. If all combined reconstruction errors exceed their respective thresholds, the network classifies the sample as OOD (indicating the absence of humans); otherwise, it is categorized as ID (indicating the presence of humans). To ensure the effective classification of ID data, a threshold is commonly chosen to correctly classify a high percentage (e.g., 95%) of the ID samples. In the case of HOOD, we set the thresholds to ensure that 90% of the ID data for each activity (static and very-static) are correctly classified. Following this logic, we define two thresholds corresponding to static and very-static activities.

The pseudocode in Algorithm 2 explains how our human and OOD detector operates in a mathematically rigorous manner.

Fig. 4 visually depicts the macro- and micro-RDI pairs from two scenarios, encompassing both an ID case and an OOD case. The first scenario includes a sitting human alongside a rotating table fan (ID case), and the second scenario includes only the rotating table fan (OOD case). These illustrations reveal the similarities in radar signal patterns and underscore the challenges of distinguishing between human activities with disturbers and situations involving only the disturbers by visual inspection alone. As clearly seen from this example, even though the extreme similarities of the input scenarios, HOOD is capable of differentiating between ID and OOD cases.

Algorithm 2 Pseudocode of HOOD Inference   
if   
$\mathrm { M S E } ( X _ { M , s } , D _ { M , s } ( E _ { M } ( X _ { M , s } ) ) )$   
$+ \operatorname { M S E } ( X _ { m , s } , D _ { m , s } ( E _ { m } ( X _ { m , s } ) ) ) >$ threshold<sub>s</sub>   
and   
$\mathrm { M S E } ( X _ { M , v s } , D _ { M , v s } ( E _ { M } ( X _ { M , v s } ) ) )$   
$+ \mathbf { M S E } ( X _ { m , v s } , D _ { m , v s } ( E _ { m } ( X _ { m , v s } ) ) ) > \mathrm { t h r e s h o l d } _ { v s }$   
then   
X ← No Presence   
else   
X ← Presence   
end if

![](images/93aedd366791a0259b6076fa93f166fa6594823f588066ca0ae2eac89e72a41b.jpg)

![](images/df05ed024c6b5802ba879a6db51b6895f2fd338c317e092ed96ea882283effa1.jpg)

![](images/aae8394c9012f8d764fba80ff793daf14bbbafc9f5a073d9f8915ae032df77a4.jpg)  
(c)

![](images/708bd03671069cf7a57acb8b640fe44e79409274b86321f72befac82ef22bcdc.jpg)  
(d)  
Fig. 4. Visualization of RDIs. (a) Macro-RDI of a sitting human and a table fan. (b) Micro-RDI of a sitting human and a table fan. (c) Macro-RDI of a table fan. (d) Micro-RDI of a table fan. They illustrate the similarity in radar signatures between sitting human activities with the presence of an OOD object and only an OOD object. The macro-RDIs [(a) and (c)] and the micro-RDIs [(b) and (d)] of ID (sitting human together with fan) and OOD (only fan) samples appear almost the same, making it challenging to visually distinguish between them.

## V. EXPERIMENTS

In our offline experiments, we utilize a processing unit consisting of an NVIDIA GeForce RTX 3070 GPU, an Intel Core i7-11800H CPU, and a 32-GB DDR4 RAM module. We perform our real-time (online) experiments on various CPUs. Additionally, to show the compatibility and feasibility of our pipeline, we extended our tests to include the Raspberry Pi 3B+, which is equipped with a advanced RISC machines (ARM) Cortex-A53 CPU and is known for its limited resources. Despite its modest hardware, our model’s spatial complexity of 49 MB ensures smooth operation on the Raspberry Pi 3B+. Execution times varied, with the model processing one frame in just 19 ms on the Intel Core i7-11800H CPU, while taking 260 ms on the Raspberry Pi 3B+ with an ARM Cortex-A53 CPU. These findings underscore the real-time capability and adaptability of our model from high-end computing environments to resourceconstrained devices.

## A. Dataset and Evaluation Metrics

In this study, we record our own data utilizing Infineon’s BGT60TR13C 60-GHz FMCW radar sensor with four individuals in various indoor places, including 28 rooms from houses, classrooms, and offices. The radar sensor is placed at a height of around two meters and tilted 15 from the front side. We divide data from all rooms into separate sets for training and testing purposes. Specifically, 14 rooms are allocated for the training, and the remaining 14 rooms are used for the testing. The dataset consisted of two types of samples: ID and OOD. OOD samples consist of common moving household objects such as table fans, stand fans, a remote-controlled (RC) toy car, and a robot vacuum cleaner. In addition, we divide the ID samples into two categories: static and very-static. The static scenarios involve a person standing alone or standing with a disturber object present in the scene. On the other hand, the very-static scenarios consist of a person either sitting or lying alone, as well as with a disturber object present in the scene. Throughout the recordings, both the disturber objects and individuals engage in their activities at distances ranging from 1 to 4 m away from the radar. During training, we use ID samples from static and very-static categories of sitting and standing activities in the presence or absence of disturbers. The disturbers in the training set include a stand fan, a table fan, an RC toy robot, and moving lamps. For testing, we use both ID and OOD samples and expand the variety of disturber types, including an RC toy car, boiling water from a kettle, running water from a tap, a vacuum cleaner, a smart vacuum cleaner, swinging laundry, a stand fan, a table fan, and a flying paper bag. Additionally, the very-static category of ID samples is increased by including the scenario of a person lying down.

We build the training set using only ID samples, consisting of 224 063 frames from the static category and 226 484 frames from the very-static category. For the test set, we use 108 952 frames from the static category, 137 325 frames from the very-static category as ID frames, and 73 960 OOD frames. Among the entire dataset (770 784 frames), 58.45% is used for training and 41.55% for testing. In the training set, 49.73% comes from the static category and 50.27% from the verystatic category. In the test set, 34.02% is from the static category, 42.88% is from the very-static category, and 23.10% is from OOD data. To provide a clearer understanding of the data collection process and the radar’s operation, we refer to Fig. 5, which illustrates our FMCW radar workflow, and a real-world scenario.

This study utilizes several common evaluation metrics in the OOD detection field: Area under the receiver operating characteristic curve (AUROC), AUIN, AUOUT, and FPR95. AUROC is the measure of the area under the receiver operating characteristic (ROC) curve. $A U P R _ { I N }$ is the area under the precision–recall curve when considering ID samples as positives. $A U P R _ { O U T }$ is the area under the precision–recall curve when considering OOD samples as positives. FPR95 corresponds to the false positive rate (FPR) when the true positive rate (TPR) is at 95%. On the other hand, the Test Time represents the inference time in seconds required to evaluate all test samples. It also shows the minimal time complexity of our model.

TABLE II  
MAIN RESULTS. HOOD PERFORMANCE COMPARISON WITH OTHER POPULAR METHODS. ALL VALUES ARE SHOWN IN PERCENTAGES EXCEPT TIME. ↑ INDICATES THAT HIGHER VALUES ARE BETTER, WHILE ↓ INDICATES THAT LOWER VALUES ARE BETTER
<table><tr><td rowspan="3">Architecture</td><td rowspan="3">Method</td><td colspan="4">Static</td><td colspan="4">Very-Static</td><td>Test Time</td></tr><tr><td>AUROC ↑</td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$  ↑</td><td> $\mathbf { A U P R } _ { \mathrm { O U T } }$  ↑</td><td>FPR95 ↓</td><td>AUROC ↑</td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$  ↑</td><td> $\mathbf { A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td><td>(seconds) ↓</td></tr><tr><td rowspan="9">RESNET-34 [70]</td><td>MSP [35]</td><td>53.82</td><td>60.27</td><td>40.72</td><td>97.51</td><td>56.75</td><td>65.71</td><td>41.54</td><td>91.31</td><td>298</td></tr><tr><td>ODIN [36]</td><td>88.67</td><td>92.81</td><td>80.77</td><td>62.08</td><td>81.44</td><td>89.25</td><td>67.20</td><td>73.81</td><td>1209</td></tr><tr><td>ENERGY [38]</td><td>47.01</td><td>57.09</td><td>38.11</td><td>95.34</td><td>54.55</td><td>65.45</td><td>45.37</td><td>83.22</td><td>288</td></tr><tr><td>MAHA [39]</td><td>37.97</td><td>49.84</td><td>50.17</td><td>73.83</td><td>54.95</td><td>67.08</td><td>52.48</td><td>73.81</td><td>3599</td></tr><tr><td>FSSD [45]</td><td>90.77</td><td>92.01</td><td>88.00</td><td>44.44</td><td>80.77</td><td>88.26</td><td>70.92</td><td>65.10</td><td>3784</td></tr><tr><td>OE [49]</td><td>64.75</td><td>66.27</td><td>63.67</td><td>72.36</td><td>77.96</td><td>84.88</td><td>69.71</td><td>68.65</td><td>289</td></tr><tr><td>GRADNORM [54]</td><td>53.38</td><td>59.02</td><td>41.56</td><td>96.66</td><td>54.01</td><td>63.68</td><td>39.72</td><td>91.79</td><td>878</td></tr><tr><td>REACT [43]</td><td>41.67</td><td>54.17</td><td>33.54</td><td>97.76</td><td>53.46</td><td>64.99</td><td>42.55</td><td>86.09</td><td>297</td></tr><tr><td>MAXLOGIT [42] KL [42]</td><td>50.17 52.95</td><td>59.64 62.89</td><td>39.34 45.40</td><td>94.98 90.61</td><td>51.59 64.65</td><td>65.84 75.76</td><td>34.35 49.86</td><td>94.85 84.83</td><td>297 287</td></tr><tr><td rowspan="9">RESNET-50 [70]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MSP [35]</td><td>19.33</td><td>43.63</td><td>25.57</td><td>100</td><td>30.43</td><td>53.32</td><td>24.25</td><td>99.50</td><td>578</td></tr><tr><td>ODIN [36]</td><td>43.21</td><td>55.57</td><td>34.56</td><td>96.97</td><td>49.64</td><td>64.99 62.02</td><td>35.46</td><td>92.75</td><td>2466</td></tr><tr><td>ENERGY [38]</td><td>50.52 82.29</td><td>57.03 87.20</td><td>41.60 78.13</td><td>93.75 60.16</td><td>48.51 81.25</td><td>89.77</td><td>33.70 70.48</td><td>94.69 66.50</td><td>600</td></tr><tr><td>MAHA [39] FSSD [45]</td><td>85.57</td><td>90.43</td><td>77.41</td><td>71.29</td><td>72.85</td><td>85.59</td><td>57.15</td><td>82.42</td><td>7249 8041</td></tr><tr><td>OE [49]</td><td>78.00</td><td>83.82</td><td>71.15</td><td>70.81</td><td>77.81</td><td>86.09</td><td>67.06</td><td>69.01</td><td>581</td></tr><tr><td>GRADNORM [54]</td><td>56.11</td><td>60.96</td><td>50.86</td><td>81.52</td><td>40.41</td><td>57.46</td><td>30.96</td><td>93.22</td><td>1850</td></tr><tr><td>REACT [43]</td><td>63.59</td><td>69.85</td><td>49.44</td><td>94.70</td><td>54.07</td><td>68.97</td><td>37.30</td><td>92.27</td><td>620</td></tr><tr><td>MAXLOGIT [42]</td><td>49.93</td><td>60.66</td><td>39.17</td><td>94.86</td><td>46.10</td><td>65.00</td><td>29.69</td><td>98.53</td><td>642</td></tr><tr><td>KL [42]</td><td>66.65</td><td>75.45</td><td>53.49</td><td>90.18</td><td>29.68</td><td>54.70</td><td>23.81</td><td></td><td>99.23</td><td>573</td></tr><tr><td rowspan="9">RESNET-101 [70]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MSP [35] ODIN [36]</td><td>62.53 76.43</td><td>68.30 78.63</td><td>57.66 74.19</td><td>80.07 60.05</td><td>54.20 65.78</td><td>67.67 74.43</td><td>41.62 54.05</td><td>87.32 81.46</td><td>959 3955</td></tr><tr><td>ENERGY [38]</td><td>71.49</td><td>80.13</td><td>58.72</td><td>85.44</td><td>53.99</td><td>72.14</td><td>35.85</td><td>94.43</td><td>938</td></tr><tr><td>MAHA [39]</td><td>70.69</td><td>75.85</td><td>69.24</td><td>64.07</td><td>83.17</td><td>90.49</td><td>73.94</td><td>61.86</td><td>10282</td></tr><tr><td>FSSD [45]]</td><td>86.07</td><td>91.09</td><td>79.21</td><td>66.48</td><td>74.28</td><td>86.62</td><td>61.25</td><td>75.15</td><td>29501</td></tr><tr><td>OE [49]</td><td>73.90</td><td>79.06</td><td>69.05</td><td>68.63</td><td>76.12</td><td>83.24</td><td>66.17</td><td>67.88</td><td>932</td></tr><tr><td>GRADNORM [54]</td><td>52.02</td><td>59.95</td><td>44.98</td><td>90.20</td><td>46.56</td><td>63.31</td><td>32.76</td><td>94.10</td><td>7472</td></tr><tr><td>REACT [43]</td><td>41.25</td><td>55.09</td><td>35.95</td><td>94.64</td><td>38.63</td><td>57.11</td><td>31.89</td><td>93.21</td><td>988</td></tr><tr><td>MAXLOGIT [42]</td><td>50.65</td><td>59.21</td><td>39.63</td><td>94.95</td><td>50.11</td><td>64.12</td><td>34.04</td><td>95.12</td><td>1049</td></tr><tr><td>KL [42]</td><td></td><td>71.41</td><td>75.62</td><td>68.17</td><td>67.35</td><td>61.82</td><td>69.25</td><td>56.94</td><td>72.71</td><td>939</td></tr><tr><td>Ours</td><td>HOOD</td><td>95.71</td><td>97.09</td><td>93.80</td><td>23.67</td><td>93.02</td><td>96.11</td><td>87.70</td><td>34.46</td><td>67</td></tr></table>

![](images/cea39177ca01bbd409ef9a59e281bb876cd192e787576d1070dfd563b1bb490d.jpg)  
Fig. 5. Illustration of our radar configuration and workflow, combined with a real-world scenario. The right diagram details the radar’s internal mechanism, including signal transmission, reflection, amplification, and ADC. The left side depicts a real-world application, showcasing how the radar detects human presence. The figure integrates the radar’s operation with the preprocessing, E-RESPD, and HOOD framework, highlighting the end-to-end classification process.

We compare the performance of HOOD with ten SOTA methods using the abovementioned common OOD detection metrics. To ensure a comprehensive comparison, we separately train ResNet34, ResNet50, and ResNet101 backbones [70] with our static and very-static ID categories in a two-class classification manner. As the nature of the OOD detection tasks, the backbones are never fed with the OOD data during training. Subsequently, we utilize the pretrained models to employ the SOTA methods and evaluate the metrics. The superiority of HOOD over the SOTA approaches is presented in Table II. For comparisons with the SOTA methods, we use the same train and test datasets employed in the HOOD framework along with identical preprocessing steps, including E-RESPD. In addition to comparisons with SOTA OOD methods, we compare the HOOD framework with existing radar-based presence detection methods. The results are listed in Table III. Similar to ours, the first two methods are reconstruction-based, the next two are machine learning-based methods, and the last two are conventional signal processingbased methods. HOOD outperforms all these methods across all metrics. For these comparisons, we use the exact same train and test data as in the HOOD framework, and except for CSPs that provide their own processing, we apply the same preprocessing steps, including E-RESPD. Furthermore, we perform an ablation study to assess the impact of incorporating E-RESPD into HOOD. Table IV shows the significant effect of E-RESPD in enhancing HOOD’s performance. In addition, in another ablation study detailed in Table V, we demonstrate the significant impact of using both RDI and micro-RDI data types together. While micro-RDIs are highly effective for detecting subtle movements, such as breathing, macro-RDIs still play an important role, particularly in easily detecting larger movements.

TABLE III  
MAIN RESULTS. HOOD PERFORMANCE COMPARISON WITH RADAR-BASED HUMAN PRESENCE DETECTION METHODS. HERE, RB, ML, AND CSP REFER TO THE RECONSTRUCTION-BASED, MACHINE-LEARNING-BASED, AND CONVENTIONAL SIGNAL PROCESSING-BASED METHODS, RESPECTIVELY. ALL VALUES ARE SHOWN IN PERCENTAGES. ↑ INDICATES THAT HIGHER VALUES ARE BETTER, WHILE ↓ INDICATES THAT LOWER VALUES ARE BETTER
<table><tr><td>1</td><td colspan="4">Static</td><td colspan="4">Very-Static</td></tr><tr><td></td><td>AUROC ↑</td><td>AUPRIN ↑</td><td>AUPROUT ↑</td><td>FPR95 ↓</td><td>AUROC ↑</td><td>AUPRIN ↑</td><td>AUPROUT ↑</td><td>FPR95 ↓</td></tr><tr><td>RB1 [14]</td><td>50.23</td><td>60.84</td><td>39.51</td><td>94.86</td><td>50.34</td><td>66.20</td><td>33.84</td><td>95.03</td></tr><tr><td>RB2 [32]</td><td>85.59</td><td>91.28</td><td>79.91</td><td>62.43</td><td>82.69</td><td>91.19</td><td>72.86</td><td>64.76</td></tr><tr><td>ML1 [33]</td><td>86.93</td><td>28.34</td><td>87.45</td><td>83.51</td><td>79.51</td><td>25.85</td><td>68.93</td><td>88.43</td></tr><tr><td>ML2 [34]</td><td>86.21</td><td>41.09</td><td>91.09</td><td>100.0</td><td>83.27</td><td>37.80</td><td>82.53</td><td>100.0</td></tr><tr><td>CSP1 [30]</td><td>42.96</td><td>67.29</td><td>60.11</td><td>98.44</td><td>48.88</td><td>64.88</td><td>63.93</td><td>92.91</td></tr><tr><td>CSP2 [31]</td><td>52.00</td><td>61.48</td><td>62.33</td><td>100.0</td><td>52.61</td><td>74.62</td><td>75.83</td><td>100.0</td></tr><tr><td>HOOD</td><td>95.71</td><td>97.09</td><td>93.80</td><td>23.67</td><td>93.02</td><td>96.11</td><td>87.70</td><td>34.46</td></tr></table>

TABLE IV

ABLATION STUDY ON THE IMPACT OF E-RESPD ON THE PERFORMANCE OF HOOD. ALL VALUES ARE SHOWN IN PERCENTAGES. ↑ INDICATES THAT HIGHER VALUES ARE BETTER, WHILE ↓ INDICATES THAT LOWER VALUES ARE BETTER
<table><tr><td>一</td><td colspan="4">Static</td><td colspan="4">Very-Static</td></tr><tr><td></td><td>AUROC ↑</td><td>AUPRIN ↑</td><td>AUPROUT ↑</td><td>FPR95 ↓</td><td>AUROC ↑</td><td>AUPRIN ↑</td><td>AUPROUT ↑</td><td>FPR95 ↓</td></tr><tr><td>HOOD w/o E-RESPD</td><td>85.14</td><td>88.50</td><td>80.73</td><td>55.12</td><td>76.07</td><td>85.91</td><td>61.68</td><td>76.05</td></tr><tr><td>HOOD</td><td>95.71</td><td>97.09</td><td>93.80</td><td>23.67</td><td>93.02</td><td>96.11</td><td>87.70</td><td>34.46</td></tr></table>

TABLE V

ABLATION STUDY ON THE IMPACT OF USING BOTH RDI AND MICRO-RDI ON THE PERFORMANCE OF HOOD. ALL VALUES ARE SHOWN IN PERCENTAGES. ↑ INDICATES THAT HIGHER VALUES ARE BETTER, WHILE ↓ INDICATES THAT LOWER VALUES ARE BETTER
<table><tr><td>|</td><td colspan="4">Static</td><td colspan="4">Very-Static</td></tr><tr><td></td><td>AUROC ↑</td><td>AUPRIN ↑</td><td>AUPROUT ↑</td><td>FPR95 ↓</td><td>AUROC ↑</td><td>AUPRIN ↑</td><td>AUPROUT ↑</td><td>FPR95 ↓</td></tr><tr><td>micro-RDI</td><td>89.67</td><td>91.25</td><td>86.45</td><td>46.21</td><td>82.13</td><td>90.93</td><td>72.06</td><td>65.73</td></tr><tr><td>RDI+micro-RDI</td><td>95.71</td><td>97.09</td><td>93.80</td><td>23.67</td><td>93.02</td><td>96.11</td><td>87.70</td><td>34.46</td></tr></table>

## B. Conducted Experiments

We perform a series of additional real-time and offline experiments with different individuals to demonstrate the performance of HOOD in different scenarios. By doing so, we want to quantify its generalization performance in various cases, including challenging scenarios and for different individuals that are not observed by the model during training. For the experimental setup, we position the radar at different heights ranging from 1 to 2.5 m and adjust the tilt degree from 0<sup>◦</sup> to 30<sup>◦</sup>. The distances and angles of individuals and disturber objects with respect to the radar vary. They may be located within the same or different range and angle relative to the radar. For the following experiments, we use completely new data in addition to the one described above. Also, eight more individuals (three females and five males) join the experiments. Their data are never seen in the training and are only used for testing. The specific details of the scenarios and their results are as follows.

1) Normal-Cluttered Room With and Without Human Presence: This experiment evaluates indoor environments such as houses, offices, and classrooms, referred to as normal-cluttered rooms, where disturber objects are almost stationary and pose insignificant disruption. In the no presence scenario, there are no individuals in the room. In contrast, the presence scenario includes various human activities, such as sitting or standing, with configurations involving one or multiple individuals. These configurations encompass cases where all individuals are sitting, standing, or a mix of both, as well as situations where people have their backs facing the radar. The experiment aims to assess the HOOD system’s ability to correctly assign presence or no presence across diverse scenarios. Table VI demonstrates the average results of this scenario. Here, the IDs include scenarios of human presence within normal-cluttered rooms, while the OODs consist of normal-cluttered rooms without human presence. For this experiment, we utilize 52 992 ID frames and 31 488 OOD frames. As clearly demonstrated, HOOD performs exceptionally well in this scenario.

TABLE VI  
RESULTS OF NORMAL-CLUTTERED ROOM WITH AND WITHOUT HUMAN PRESENCE
<table><tr><td>Method</td><td>AUROC ↑</td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$  ↑</td><td> $\mathbf { A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td></tr><tr><td>HOOD</td><td>99.91</td><td>99.91</td><td>99.90</td><td>0.90</td></tr></table>

TABLE VII

RESULTS OF HEAVY-CLUTTERED ROOM WITH AND WITHOUT HUMAN PRESENCE
<table><tr><td>Method</td><td>AUROC ↑</td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$  ↑</td><td> $\mathbf { A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td></tr><tr><td>HOOD</td><td>93.60</td><td>93.86</td><td>92.24</td><td>30.83</td></tr></table>

2) Heavy-Cluttered Room With and Without Human Presence: This experiment examines indoor environments where disturber objects, such as stand fans, table fans, and RC toy cars, cause significant movement, unlike in normal-cluttered rooms. In the no presence scenario, there are no individuals in the room, and the goal is to assess the HOOD system’s ability to accurately assign no presence despite the disturbers’ movements. In the presence scenario, the experiment includes various human activities, with individuals sitting, standing, or a combination of both, in addition to the active disturbers. The objective is to evaluate HOOD’s capability to correctly assign presence in complex, multiperson scenarios with diverse postures and significant clutter-induced challenges. Table VII presents the average results of this scenario. Here, the IDs include scenarios of human presence within heavy-cluttered rooms, while the OODs consist of heavy-cluttered rooms without human presence. For this experiment, we utilize 111 616 ID frames and 45 952 OOD frames. This is one of the most challenging scenarios, and HOOD performs well.

3) Partially Visible Human in Normal- and Heavy-Cluttered Room: In this scenario, an individual is standing or sitting in a normal- or heavy-cluttered room. However, a table may partially block the human body, or the human stays at an angle at which only some body parts are in the radar’s field of view. Our system aims to accurately detect the presence of a person, even when their body is partially visible or obscured by a table or other objects in the room. If no human exists in front of the radar, HOOD assigns no presence. Table VIII shows the average results of this scenario. Here, the IDs include scenarios of partially visible human presence within normal- and heavy-cluttered rooms, while the OODs consist of normal- and heavy-cluttered rooms without human presence. For this experiment, we use 52 736 ID frames and 50 304 OOD frames.

TABLE VIII  
PARTIALLY VISIBLE HUMAN IN NORMAL- AND HEAVY-CLUTTERED ROOMS
<table><tr><td>Method</td><td>AUROC ↑</td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$  ↑</td><td> $\mathbf { A U P R } _ { \mathrm { O U T } }$  ↑</td><td>FPR95 ↓</td></tr><tr><td>HOOD</td><td>95.54</td><td>94.89</td><td>95.49</td><td>12.74</td></tr></table>

TABLE IX  
RESULTS OF EDGE CASE ANALYSIS
<table><tr><td>Method</td><td>AUROC ↑</td><td> $\mathrm { A U P R } _ { \mathrm { I N } }$  ↑</td><td> $\mathrm { \bf A U P R _ { O U T } }$  ↑</td><td>FPR95 ↓</td></tr><tr><td>HOOD</td><td>94.02</td><td>95.50</td><td>92.56</td><td>35.11</td></tr></table>

4) Edge Case Analysis: We also test various edge cases to determine the system’s performance boundaries. For example, we test a human standing and holding their breath, a human sitting and holding their breath, and a person lying down and crouching, resulting in partial obscuration of the chest area. Additionally, we place a corner reflector alongside individuals who are sitting or standing. We evaluate the system’s ability to assign presence through these tests by handling these challenging scenarios accurately. Our edge case analysis proves that regardless of the performed activity (sitting, standing, lying, crouching, etc.), if a person(s) is present in the normal- or heavy-cluttered room, HOOD robustly and correctly detects their presence. If no human exists in front of the radar, HOOD assigns no presence. Table IX demonstrates average results. IDs (51 712 frames) include human presence within edge case scenarios. OODs (50 304 frames) include normaland heavy-cluttered rooms without human presence.

Our online and offline experiments demonstrate HOOD’s robustness and high generalization capability for human presence and OOD detection tasks, considering the hardware limitations of our low-cost, short-range 60-GHz FMCW radar sensor, which consists of one Tx and three receive antennas.

Real-time tests are conducted in diverse environments incorporating multiple disturbers and individuals included and also not included in the training scenarios. Similarly, offline tests take place in completely different settings from the training ones, involving both new disturbers and participants.

During the tests, participants act freely as they would in their daily lives. Individuals and disturbances are randomly positioned, varying in proximity and range. They may be close together or far apart, within the same range bin or different ones. The system performs effectively even when many people and multiple disturbers (stationary and/or moving) are present simultaneously. These tests are crucial since reflected signals from some targets can interfere with signals from others. These varied and dynamic conditions underscore HOOD’s practical applicability in handling complex real-world scenarios and its reliability.

Since our radar sensor is primarily designed for indoor applications, we focus on indoor scenarios that are sufficient for our application use cases. For additional experimental scenarios and a comprehensive demonstration of HOOD, including detailed demo videos, please visit the project page.<sup>1</sup>

## VI. CONCLUSION

This study presents HOOD, a real-time and robust human presence and OOD detection method specifically designed for indoor environments using low-cost 60-GHz FMCW radar. By exploiting a reconstruction-based architecture and leveraging radar macro- and micro-RDIs, HOOD effectively detects the presence of humans in the presence or absence of moving and stationary disturbers. As an OOD detector, it accurately identifies and classifies disturbers as OOD when no humans are detected, providing reliable predictions for different human scenarios. The evaluations conducted on a dataset collected by the 60-GHz FMCW radar demonstrate the superior performance of HOOD, achieving high AUROC and low FPR95 values. Comparisons with SOTA OOD detection methods further confirm the effectiveness of HOOD. Moreover, the real-time capability of HOOD enhances its practical utility for various indoor applications, and its compatibility with Raspberry Pi 3B+ underscores its versatility across different hardware environments. Overall, HOOD presents a promising real-time human presence and OOD detection solution with exceptional generalization capabilities. A potential extension for the practical implementation of HOOD involves integrating it into a microcontroller, enabling autonomous operation in conjunction with the radar system. By embedding HOOD directly onto a microcontroller, it becomes possible to create a self-contained and independent solution for human presence and OOD detection.

## REFERENCES

[1] S. Hazra and A. Santra, “Robust gesture recognition using millimetricwave radar system,” IEEE Sensors Lett., vol. 2, no. 4, pp. 1–4, Dec. 2018.

[2] S. Skaria, A. Al-Hourani, M. Lech, and R. J. Evans, “Hand-gesture recognition using two-antenna Doppler radar with deep convolutional neural networks,” IEEE Sensors J., vol. 19, no. 8, pp. 3041–3048, Apr. 2019.

[3] J.-W. Choi, S.-J. Ryu, and J.-H. Kim, “Short-range radar based real-time hand gesture recognition using LSTM encoder,” IEEE Access, vol. 7, pp. 33610–33618, 2019.

[4] T. Stadelmayer, Y. Hassab, L. Servadei, A. Santra, R. Weigel, and F. Lurz, “Lightweight and person-independent radar-based hand gesture recognition for classification and regression of continuous gestures,” IEEE Internet Things J., vol. 11, no. 9, pp. 15285–15298, May 2024.

[5] M. Alizadeh, G. Shaker, J. C. M. D. Almeida, P. P. Morita, and S. Safavi-Naeini, “Remote monitoring of human vital signs using mm-wave FMCW radar,” IEEE Access, vol. 7, pp. 54958–54968, 2019.

[6] E. Turppa, J. M. Kortelainen, O. Antropov, and T. Kiuru, “Vital sign monitoring using FMCW radar in various sleeping scenarios,” Sensors, vol. 20, no. 22, p. 6505, Nov. 2020.

[7] M. Arsalan, A. Santra, and C. Will, “Improved contactless heartbeat estimation in FMCW radar via Kalman filter tracking,” IEEE Sensors Lett., vol. 4, no. 5, pp. 1–4, May 2020.

[8] P. Vaishnav and A. Santra, “Continuous human activity classification with unscented Kalman filter tracking using FMCW radar,” IEEE Sensors Lett., vol. 4, no. 5, pp. 1–4, May 2020.

[9] A. Shrestha, H. Li, J. Le Kernec, and F. Fioranelli, “Continuous human activity classification from FMCW radar with bi-LSTM networks,” IEEE Sensors J., vol. 20, no. 22, pp. 13607–13619, Nov. 2020.

[10] T. Stadelmayer, M. Stadelmayer, A. Santra, R. Weigel, and F. Lurz, “Human activity classification using mm-wave FMCW radar by improved representation learning,” in Proc. 4th ACM Workshop Millim.- Wave Netw. Sens. Syst., New York, NY, USA, Sep. 2020, pp. 1–6.

[11] C. Y. Aydogdu, S. Hazra, A. Santra, and R. Weigel, “Multimodal cross learning for improved people counting using short-range FMCW radar,” in Proc. IEEE Int. Radar Conf. (RADAR), Apr. 2020, pp. 250–255.

[12] J. Weiß, R. Pérez, and E. Biebl, “Improved people counting algorithm for indoor environments using 60 GHz FMCW radar,” in Proc. IEEE Radar Conf. (RadarConf), Sep. 2020, pp. 1–6.

[13] L. Servadei et al., “Label-aware ranked loss for robust people counting using automotive in-cabin radar,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), May 2022, pp. 3883–3887.

[14] S. M. Kahya, M. Sami Yavuz, and E. Steinbach, “Mcrood: Multi-class radar out-of-distribution detection,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Jun. 2023, pp. 1–5.

[15] H. Wang, Z. Li, L. Feng, and W. Zhang, “ViM: Out-of-distribution with virtual-logit matching,” 2022, arXiv:2203.10807.

[16] J. Yang et al., “Semantically coherent out-of-distribution detection,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2021, pp. 8281–8289.

[17] R. Huang and Y. Li, “MOS: Towards scaling out-of-distribution detection for large semantic space,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2021, pp. 8706–8715.

[18] J. Yang, K. Zhou, and Z. Liu, “Full-spectrum out-of-distribution detection,” 2022, arXiv:2204.05306.

[19] H. Wang and Y. Li, “Bridging OOD generalization and detection: A graph-theoretic view,” in Proc. Adv. Neural Inf. Process. Syst., 2024.

[20] C. Will, P. Vaishnav, A. Chakraborty, and A. Santra, “Human target detection, tracking, and classification using 24-GHz FMCW radar,” IEEE Sensors J., vol. 19, no. 17, pp. 7283–7299, Sep. 2019.

[21] M. Pavan, A. Caltabiano, and M. Roveri, “TinyML for UWB-radar based presence detection,” in Proc. Int. Joint Conf. Neural Netw. (IJCNN), 2022, pp. 1–8.

[22] D. Deiana, E. M. Suijker, R. J. Bolt, A. P. M. Maas, W. J. Vlothuizen, and A. S. Kossen, “Real time indoor presence detection with a novel radar on a chip,” in Proc. Int. Radar Conf., Oct. 2014, pp. 1–4.

[23] A. Santra, R. V. Ulaganathan, and T. Finke, “Short-range millimetricwave radar system for occupancy sensing application,” IEEE Sensors Lett., vol. 2, no. 3, pp. 1–4, Sep. 2018.

[24] Z. Xiao, K. Ye, and G. Cui, “PointNet-transformer fusion network for in-cabin occupancy monitoring with mm-wave radar,” IEEE Sensors J., vol. 24, no. 4, pp. 5370–5382, Feb. 2024.

[25] N. Regev and D. Wulich, “Radar-based, simultaneous human presence detection and breathing rate estimation,” Sensors, vol. 21, no. 10, p. 3529, 2021.

[26] S. Chang, N. Mitsumoto, and J. W. Burdick, “An algorithm for UWB radar-based human detection,” in Proc. IEEE Radar Conf., May 2009, pp. 1–6.

[27] S. H. Chang, M. Wolf, and J. W. Burdick, “Human detection and tracking via ultra-wideband (UWB) radar,” in Proc. IEEE Int. Conf. Robot. Autom., May 2010, pp. 452–457.

[28] S. Xia, Y. Xiang, K. Xiong, S. Guo, and G. Cui, “A radar target tracking algorithm based on learning displacement,” IEEE Geosci. Remote Sens. Lett., vol. 21, pp. 1–5, 2024.

[29] J.-E. Kim, J.-H. Choi, and K.-T. Kim, “Robust detection of presence of individuals in an indoor environment using iR-UWB radar,” IEEE Access, vol. 8, pp. 108133–108147, 2020.

[30] P. Nallabolu, L. Zhang, H. Hong, and C. Li, “Human presence sensing and gesture recognition for smart home applications with moving and stationary clutter suppression using a 60-GHz digital beamforming FMCW radar,” IEEE Access, vol. 9, pp. 72857–72866, 2021.

[31] Y. Luo and X. Li, “Indoor human location method for FMCW radar using standard deviation weighting,” in Proc. 2nd Int. Conf. Frontiers Electron., Inf. Comput. Technol. (ICFEICT), Aug. 2022, pp. 159–163.

[32] X. Peng, M. Zhang, L. Servadei, and R. Wille, “Enhancing indoor radar detection: An FMCW radar system for distinguishing human presence and swinging blinds,” in Proc. IEEE Radar Conf. (RadarConf), May 2024, pp. 1–6.

[33] J. Cha, K. Yoo, D. Choi, and Y. Kim, “Human presence detection using ultrashort-range FMCW radar based on DCNN,” IEEE Sensors J., vol. 24, no. 16, pp. 26258–26265, Aug. 2024.

[34] Y. D. Dadon, S. Yamin, S. Feintuch, H. H. Permuter, I. Bilik, and J. Taberkian, “Moving target classification based on micro-Doppler signatures via deep learning,” in Proc. IEEE Radar Conf. (RadarConf), May 2021, pp. 1–6.

[35] D. Hendrycks and K. Gimpel, “A baseline for detecting misclassified and out-of-distribution examples in neural networks,” in Proc. Int. Conf. Learn. Represent., 2017.

[36] S. Liang, Y. Li, and R. Srikant, “Enhancing the reliability of out-ofdistribution image detection in neural networks,” in Proc. Int. Conf. Learn. Represent., Jan. 2018.

[37] B. Lakshminarayanan, A. Pritzel, and C. Blundell, “Simple and scalable predictive uncertainty estimation using deep ensembles,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30. Red Hook, NY, USA: Curran Associates, 2017, pp. 6405–6416.

[38] W. Liu, X. Wang, D. J. Owens, and Y. Li, “Energy-based out-ofdistribution detection,” in Proc. 34th Int. Conf. Neural Inf. Process. Syst., Dec. 2020, pp. 21464–21475.

[39] K. Lee et al., “A simple unified framework for detecting outof-distribution samples and adversarial attacks,” in Proc. NeurIPS, Dec. 2018, pp. 7167–7177.

[40] C. S. Sastry and S. Oore, “Detecting out-of-distribution examples with Gram matrices,” in Proc. 37th Int. Conf. Mach. Learn., Jul. 2020, pp. 8491–8501.

[41] J. Ren, S. Fort, J. Z. Liu, A. G. Roy, S. Padhy, and B. Lakshminarayanan, “A simple fix to Mahalanobis distance for improving near-OOD detection,” in Proc. ICML Workshop Uncertainty Robustness Deep Learn., Jan. 2021.

[42] D. Hendrycks et al., “Scaling out-of-distribution detection for real-world settings,” in Proc. Int. Conf. Mach. Learn. (ICML), 2022, pp. 8759–8773.

[43] Y. Sun, C. Guo, and Y. Li, “ReAct: Out-of-distribution detection with rectified activations,” in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), Jan. 2021, pp. 144–157.

[44] Y. Sun and Y. Li, “DICE: Leveraging sparsification for out-ofdistribution detection,” in Proc. Eur. Conf. Comput. Vis. (ECCV), Jan. 2022, pp. 691–708.

[45] H. Huang, Z. Li, L. Wang, S. Chen, B. Dong, and X. Zhou, “Feature space singularity for out-of-distribution detection,” in Proc. Workshop Artif. Intell. Saf. (SafeAI), 2021.

[46] Y. Sun, Y. Ming, X. Zhu, and Y. Li, “Out-of-distribution detection with deep nearest neighbors,” in Proc. Int. Conf. Mach. Learn. (ICML), 2022, pp. 20827–20840.

[47] J. Park, Y. G. Jung, and A. B. J. Teoh, “Nearest neighbor guidance for out-of-distribution detection,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2023, pp. 1686–1695.

[48] Y.-C. Hsu, Y. Shen, H. Jin, and Z. Kira, “Generalized ODIN: Detecting out-of-distribution image without learning from out-of-distribution data,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 10948–10957.

[49] D. Hendrycks, M. Mazeika, and T. Dietterich, “Deep anomaly detection with outlier exposure,” in Proc. Int. Conf. Learn. Represent. (ICLR), 2019.

[50] A.-A. Papadopoulos, M. R. Rajati, N. Shaikh, and J. Wang, “Outlier exposure with confidence control for out-of-distribution detection,” Neurocomputing, vol. 441, pp. 138–150, Jun. 2021.

[51] K. Lee, H. Lee, K. Lee, and J. Shin, “Training confidencecalibrated classifiers for detecting out-of-distribution samples,” 2017, arXiv:1711.09325.

[52] Q. Yu and K. Aizawa, “Unsupervised out-of-distribution detection by maximum classifier discrepancy,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2019, pp. 9517–9525.

[53] Y. Ming, Y. Fan, and Y. Li, “POEM: Out-of-distribution detection with posterior sampling,” in Proc. Int. Conf. Mach. Learn. (ICML), Jan. 2022, pp. 15650–15665.

[54] R. Huang, A. Geng, and Y. Li, “On the importance of gradients for detecting distributional shifts in the wild,” in Proc. Adv. Neural Inf. Process. Syst., Jan. 2021, pp. 677–689.

[55] H. Bai, Y. Ming, J. Katz-Samuels, and Y. Li, “HYPO: Hyperspherical out-of-distribution generalization,” in Proc. Int. Conf. Learn. Represent., Feb. 2024.

[56] Y. Ming, Y. Sun, O. Dia, and Y. Li, “How to exploit hyperspherical embeddings for out-of-distribution detection?” in Proc. Int. Conf. Learn. Represent., 2023.

[57] T. Denouden, R. Salay, K. Czarnecki, V. Abdelzad, B. Phan, and S. Vernekar, “Improving reconstruction autoencoder out-of-distribution detection with Mahalanobis distance,” 2018, arXiv:1812.02765.

[58] Z. Xiao, Q. Yan, and Y. Amit, “Likelihood regret: An out-of-distribution detection score for variational auto-encoder,” in Proc. Adv. Neural Inf. Process. Syst., Jan. 2020, pp. 20685–20696.

[59] A. R. Venkatakrishnan, S. Tae Kim, R. Eisawy, F. Pfister, and N. Navab, “Self-supervised out-of-distribution detection in brain CT scans,” 2020, arXiv:2011.05428.

[60] D. Hendrycks, X. Liu, E. Wallace, A. Dziedzic, R. Krishnan, and D. Song, “Pretrained transformers improve out-of-distribution robustness,” 2020, arXiv:2004.06100.

[61] S. Fort, J. Ren, and B. Lakshminarayanan, “Exploring the limits of outof-distribution detection,” 2021, arXiv:2106.03004.

[62] R. Koner, P. Sinhamahapatra, K. Roscher, S. Günnemann, and V. Tresp, “OODformer: Out-of-distribution detection transformer,” 2021, arXiv:2107.08976.

[63] A. Dosovitskiy et al., “An image is worth 16×16 words: Transformers for image recognition at scale,” 2020, arXiv:2010.11929.

[64] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of deep bidirectional transformers for language understanding,” 2018, arXiv:1810.04805.

[65] S. M. Kahya, M. S. Yavuz, and E. Steinbach, “Reconstruction-based out-of-distribution detection for short-range FMCW radar,” in Proc. 31st Eur. Signal Process. Conf. (EUSIPCO), Sep. 2023, pp. 1350–1354.

[66] J.-W. Choi, C.-W. Park, and J.-H. Kim, “FMCW radar-based realtime hand gesture recognition system capable of out-of-distribution detection,” IEEE Access, vol. 10, pp. 87425–87434, 2022.

[67] M. Bauw, S. Velasco-Forero, J. Angulo, C. Adnet, and O. Airiau, “Near out-of-distribution detection for low-resolution radar micro-Doppler signatures,” 2022, arXiv:2205.07869.

[68] J. Ott, L. Servadei, G. Mauro, T. Stadelmayer, A. Santra, and R. Wille, “Uncertainty-based meta-reinforcement learning for robust radar tracking,” in Proc. 21st IEEE Int. Conf. Mach. Learn. Appl. (ICMLA), Dec. 2022, pp. 1476–1483.

[69] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” 2014, arXiv:1412.6980.

[70] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2016, pp. 770–778.

Sabri Mustafa Kahya (Graduate Student Member, IEEE) received the B.Sc. degree in computer engineering from Istanbul Technical University, Istanbul, Türkiye, in 2017, and the M.Sc. degree in informatics from the Technical University of Munich (TUM), Munich, Germany, in 2021, where he is currently pursuing the Ph.D. degree with the Chair of Media Technology, focusing on out-of-distribution detection for frequency-modulated continuouswave (FMCW) radars.

During his M.Sc., he joined the TUM Computer Vision Group, researching 3-D reconstruction and multiview shape from shading for his thesis.

Muhammet Sami Yavuz received the B.Sc. degree in electronics engineering from Sabanci University, Istanbul, Türkiye, in 2021, with a graduation project on video anomaly detection. He is currently pursuing the M.Sc. degree in communications engineering with the Technical University of Munich, Munich, Germany.

He worked part-time with Infineon Technologies AG, Munich, from December 2021 to April 2024. His work primarily involved out-of-distribution detection and human presence sensing using frequency-modulated continuouswave (FMCW) radars.

Eckehard Steinbach (Fellow, IEEE) received the degree in electrical engineering from the University of Karlsruhe, Karlsruhe, Germany, the University of Essex, Colchester, U.K., and ESIEE, Paris, France, and the Engineering Doctorate degree from the University of Erlangen–Nuremberg, Nuremberg, Germany, in 1999.

From 1994 to 2000, he was a Member of the Research Staff with the Image Communication Group, University of Erlangen–Nuremberg. From February 2000 to December 2001, he was a Post-Doctoral Fellow with the Information Systems Laboratory, Stanford University, Stanford, CA, USA. In February 2002, he joined the Department of Electrical and Computer Engineering, Technical University of Munich, Munich, Germany, where he is currently a Full Professor of the Chair of Media Technology. His current research interests include haptic and visual communication, indoor mapping, and localization.