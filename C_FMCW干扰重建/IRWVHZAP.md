## PAPER

# A lightweight interference suppression technique for FMCW automotive radar

To cite this article: Tai-Hsing Lee and Nur Azis Salim 2026  37 066113

View the article online for updates and enhancements.

Precision or Throughput? Why Choose?

Next-generation photonic manufacturing requires nanometer precision, scalable automation, and the flexibility to adapt.

SmarAct's motion and alignment solutions combine high-dynamic positioning, automated optical alignment, and integrated metrology for demanding photonic assembly and testing applications. Flexible system architectures support scalable integration processes across a broad range of optical technologies and advanced manufacturing environments.

![](images/b31cc9d6529676009fb545b087d1377813bd738f1837c142e8fead3204c3c16c.jpg)

## You may also like

Strong interference adaptive suppressionalgorithm for respiratory and heartbea monitoring   
Jiawei Tang, Yao Zhao, Zhenmiao Deng   
et al.

An Improved Multi-Target Recognition-Method for Vehicle Linear Frequency Modulated Continuous Wave Radar Yiran Lin

A dynamic interference suppressionmethod with the optimal payoff of proximity radar based on a game model Jian Dai, Xinhong Hao, Ze Li et al.

• Nanometer Precision

• Automated Alignment

• Integrated Metrology

• Modular Architecture

• Scalable Manufacturing

Enable Scalable Optical Assembly

smaract.com

# Measurement Science and Technology

Check for updates

PAPER

RECEIVED 20 November 2025

# A lightweight interference suppression technique for FMCW automotive radar

REVISED 15 January 2026

Tai-Hsing Lee1 and Nur Azis Salim1,2,3,\* ①D

ACCEPTED FOR PUBLICATION 5 February 2026

Graduate School of Engineering Science and Technology, National Yunlin University of Science and Technology, Yunlin, Taiwan 2 Department of Electrical Engineering, Faculty of Engineering, Universitas Negeri Semarang, Semarang, Indonesia

PUBLISHED 17 February 2026

3 Current address: Department of Electrical Engineering, National Yunlin University of Science and Technology, Yunlin, Taiwan. Author to whom any correspondence should be addressed.

E-mail: d11210211@yuntech.edu.tw

Keywords: automotive radar, FMCW radar, interference mitigation, blanking and interpolation, TinyML-based classification, edge computing for automotive radar

## Abstract

Interference in frequency-modulated continuous-wave automotive radars remains a major challenge, particularly for severe, overlapping multi-chirp scenarios where real-time response is critical. Most existing methods—including moving target indication–interference mitigation (MTI-IM), iterative method with adaptive thresholding (IMAT), and wavelet denoising—either lack robust handling of multi-chirp overlap or require impractical latency for embedded, low-power systems. This work introduces a lightweight, class-adaptive signal-processing framework that performs interference suppression through TinyML-guided mitigation selection rather than a single fixed strategy. A compact classifier assigns each radar burst to one of three operational modes: clean (C0), mild single-chirp interference handled by MTI-IM (C1), or severe multi-chirp overlap suppressed via blanking, interpolation, and fixed-gain Kalman filtering (C2). This enables realtime mitigation path selection without span-dependent tuning or iterative processing. Experiments with real automotive radar data demonstrate that the proposed approach consistently restores range-Doppler contrast and target separability with sub-10 ms latency on edge hardware, achieving signal-to-noise-plus-interference ratio and visual RD-map quality competitive with slower state-of-the-art methods, while reducing compute cost by 40%–50% for spans ⩾ 3. The TinyMLguided decision framework bridges the gap between accuracy and deployability in automotive radar, enabling practical, low-power mitigation for next-generation advanced driver-assistance systems and autonomous vehicles.

## 1. Introduction

Autonomous radar systems are fundamental to modern transportation infrastructures, particularly within the domains of autonomous driving and advanced driver-assistance systems (ADAS) [1]. These sensors reliably detect objects in a variety of environmental circumstances, such as poor weather and low visibility. Among existing technologies, frequency-modulated continuous-wave (FMCW) radar has emerged as a preferred solution for short- to mid-range applications, because of its great accuracy and temporal resolution in estimating both target range and radial velocity [2]. Among existing technologies, FMCW radar has emerged as a preferred solution for short-to-mid range applications, because of its great accuracy and temporal resolution in estimating both target range and radial velocity. FMCW systems have proven practical for automotive measurement applications [3]. However, as the density of radar-equipped vehicles increases in urban and highway environments, mutual interference particularly severe overlapping multi-chirp interference poses a critical challenge that degrades range–Doppler (RD) contrast, target detectability, and system dependability in high-traffic scenarios.

The number of vehicles with radar is growing, which means that the amount of mutual interference is also growing. This interference typically occurs when overlapping chirp signals from multiple radars collide within the time-frequency space [4, 5]. Ghost targets, false alarms, signal masking, and Doppler ambiguity are some of the resulting aberrations that reduce the accuracy of object identification and system dependability, particularly in areas with high traffic density or mixed traffic [6].

To mitigate such interference, prior work spans four families. System-level coordination reduces mutual transmissions via scheduled access or cognitive resource allocation. Waveform/modulation designs improve orthogonality using phase-coded chirps or adaptive filtering. Receiver-side signal processing operates post-reception through wavelet denoising (WD), Kalman filtering (KF), tensor decompositions, fractional-Fourier filtering, or convolutional neural networks [7–11]. Hybrid and learningbased approaches combine classical filters with compact on-device inference. However, coordination presumes cooperative infrastructure, waveform redesigns may break standard compatibility, and learned models can raise latency or demand scene-specific tuning [12–14]. These considerations motivate receiver-side pipelines that preserve waveform compatibility, meet strict real-time constraints for embedded deployment, and robustly handle severe overlapping interference across variable traffic densities a gap not fully addressed by existing methods.

This work introduces a lightweight, class-adaptive signal-processing framework that performs interference suppression through TinyML-guided mitigation selection rather than a single fixed suppression strategy. Unlike prior approaches that rely on computationally expensive transforms or span-dependent tuning, the proposed pipeline uses a compact classifier to dynamically assign each radar burst to one of three operational modes: (i) pass-through processing for clean signals (C0), (ii) moving target indication interference mitigation (MTI-IM) for mild single-chirp interference (C1), and (iii) a fixed-parameter suppression path combining blanking, linear interpolation, and KF for severe multi-chirp overlap (C2). The novelty of the framework lies in the integration of class-adaptive interference assessment with lightweight TinyML-guided mitigation selection, enabling real-time span-aware processing on resourceconstrained embedded hardware. Rather than relying on a single suppression strategy or heuristic rulebased selection, the proposed system dynamically assigns each burst to the most appropriate mitigation path while preserving waveform compatibility and eliminating iterative tuning. This design choice explicitly addresses practical deployment constraints in automotive radar, where robustness, latency, and computational efficiency must be jointly satisfied for embedded operation.

The framework is evaluated using real automotive radar data collected under realistic interference scenarios, including representative multi-vehicle overlapping chirp collisions. Performance is assessed through signal-to-noise-plus-interference ratio (SNIR), RD map fidelity, target recovery quality, and perframe computational cost. Comparative analysis against four representative baseline methods from the literature demonstrates that the proposed system consistently restores target detectability and RD contrast for severe interference cases while achieving 40%–50% lower latency than methods such as WD and iterative method with adaptive thresholding (IMAT). Crucially, the framework does not require specialized hardware, waveform redesign, or inter-radar coordination, enabling deployment in diverse realworld automotive scenarios with unpredictable and time-varying interference patterns a key requirement for next-generation ADAS and autonomous driving systems operating in dense urban traffic.

## 2. State-of-the-art

Over the past decade, interference mitigation (IM) in FMCW radar systems has garnered considerable attention, particularly in the context of automotive sensing, where the dense deployment of radar units increases the likelihood of mutual interference [7, 15]. As the complexity of road environments grows, so does the need for radar systems to operate reliably despite uncoordinated transmissions from nearby vehicles [16, 17]. To address this challenge, researchers have explored various IM techniques, which can be broadly grouped into system-level coordination strategies [18, 19], waveform design approaches [4, 20], and signal processing-based solutions [21, 22]. In recent years, various hybrid and alternative paradigms have arisen [23, 24], indicating the increasing requirement for scalable and flexible mitigation solutions capable of functioning under multiple operational limitations.

System-level approaches try to cut down on interference by coordinating radar broadcasts between multiple nodes. This is usually done by allocating resources in time, frequency, or space [18]. Timedivision multiplexing, frequency hopping, and radar communication protocols are examples of this type of approach [15, 19]. These methods are particularly effective when radar units can exchange information to schedule their transmissions dynamically, either through centralized control or distributed negotiation [25, 26]. However, their effectiveness often depends on the presence of reliable inter-device communication and prior agreement on operating parameters [27], which may not always be feasible in decentralized or rapidly evolving environments [28]. Furthermore, these plans often need changes to the hardware or firmware, which can be tricky for older systems [6, 29].

Waveform-based approaches take a different route by shaping the transmitted signal to be more resilient to interference [15]. Techniques such as phase-coded FMCW, orthogonal frequency division multiplexing, and pseudo-random noise-based modulation have been proposed to improve separation in the time-frequency domain. Recent work on low-correlation FSK–PSK waveform design and tunable waveletdomain processing further advances these separation techniques [4, 30–32]. These methods offer significant potential in maintaining radar performance under overlapping transmissions [23], and some even enable joint radar and communication functionalities [33]. However, using more complex waveforms often makes receivers more complicated and requires better synchronization [34], which can lead to increased system cost and implementation overhead, particularly when targeting real-time applications in embedded platforms [35].

A third stream of research has focused on signal processing techniques that address interference at the receiver without altering the transmitted waveform. Post-processing algorithms are usually used in these methods to find and fix interference abnormalities in the baseband signal [36]. Notable examples include time-domain zeroing, WD [8], fractional-Fourier domain filtering [5], MTI-IM [37], dual recursive least squares [38], correlation based local detection for deceptive jamming [39], and iterative reconstruction frameworks such as the IMAT [40]. Some methods incorporate statistical detection mechanisms, such as constant false alarm rate, in conjunction with interpolation or thresholding to suppress interference [38, 41]. The key advantage of these approaches lies in their backward compatibility and algorithmic flexibility [9, 42], which allow them to be integrated into existing radar platforms. Nevertheless their performance may suffer in situations with a lot of overlapping interference or moving targets, and in real-time systems, their computing needs must be carefully controlled [43].

In addition to these three major types, new research has looked into other and mixed methodologies, such as compressed sensing, morphological component analysis, dual-basis pursuit, and several deep learning models including convolutional and recurrent neural networks and recent contrastive learning architectures with dilated convolution [44]. Attention-based CNN architectures have demonstrated strong denoising performance for radar signal processing applications [10, 45]. These methods frequently use sparsity, signal decomposition, or learning features to identify the difference between noise and valid echoes [46]. Even though they work well in simulations and offline environments, their use in real-time radar systems is still limited because they need a lot of computational resources [47], take a long time to train [48], and are hard to fully comprehend [49]. Hybrid architectures that combine classical filters such as Wiener or Kalman filters with adaptive learning modules provide an alternate path [9], nevertheless problems about latency and resilience under different interference situations remain [50]. In parallel, TinyML oriented perception models demonstrate that deep networks can be compressed for embedded deployment in autonomous vehicles [51], further motivating our lightweight IM design.

## 3. FMCW radar signal and interference model

## 3.1. FMCW radar signal model

The transmitted signal of an FMCW radar can be expressed as a frequency-modulated chirp:

$$
s \left( t \right) = A \cdot \cos \left( 2 \pi \left( f _ { \mathrm { c } } t + \frac { \mu t ^ { 2 } } { 2 } \right) \right) ,\tag{1}
$$

where A is the signal amplitude, $f _ { \mathrm c }$ is the carrier frequency, and $\mu = B / T _ { \mathrm { c h i r p } }$ is the frequency slope with B being the bandwidth and $T _ { \mathrm { c h i r p } }$ the chirp duration [52, 53].

The receive signal after beating (mixing) for a single target at range R is:

$$
\begin{array} { r } { s _ { \mathrm { r x } } \left( t \right) = A _ { r } \cos \left( 2 \pi \Big ( f _ { \mathrm { c } } \left( t - \tau \right) + \frac { 1 } { 2 } \mu \left( t - \tau \right) ^ { 2 } \Big ) + \phi _ { 0 } \right) , } \end{array}\tag{2}
$$

with $\tau = 2 R / c$ as the round-trip delay. For modern automotive scenarios, typical parameters used in both simulation and commercial hardware include:

• bandwidth $B \in \left[ 1 5 0 , 2 0 0 \right] \mathrm { M H z } ,$

• chirp duration $T _ { \mathrm { c h i r p } } \in [ 2 0 , 5 0 ] \mu \mathrm { s } ,$

• carrier frequency $f _ { \mathrm { c } } = 7 7 \mathrm { G H z } .$

These settings mirror widely used radar modules such as Texas Instruments AWR1443BOOST and match key industry literature, ensuring that simulation-based studies reflect realistic automotive environments.

The received signal from the kth target is modeled as:

$$
b _ { k } \left( t \right) = A _ { k } \cdot \cos \left( 2 \pi \left( f _ { \mathrm { c } } t + f _ { \mathrm { D } , k } t + f _ { \mathrm { b } , k } t \right) \right) ,\tag{3}
$$

where $f _ { \mathrm { b } , k }$ is the beat frequency corresponding to the target range $R _ { k } ,$ and $f _ { \mathrm { D } , k }$ denotes the Doppler shift due to the target’s relative motion.

The overall received signal includes all target echoes, interference, and noise:

$$
r \left( t \right) = \sum _ { k } b _ { k } \left( t \right) + \mathrm { i } \left( t \right) + n \left( t \right) ,\tag{4}
$$

where i(t) and n(t) represent interference and additive noise, respectively.

This received signal model, inclusive of all targets, interference, and noise, forms the theoretical basis for the interference analysis and mitigation strategies presented in the following sections.

## 3.2. Interference sources in FMCW radar

In real deployments, multiple radars operating in close proximity can create unintended interference. The baseband signal for the jth interfering radar (its transmit chirp as seen at the victim) can be modeled as

$$
i _ { j } \left( t \right) = A _ { j } \cos \left( 2 \pi \left( f _ { I , j } t + \textstyle \frac { 1 } { 2 } \mu _ { j } t ^ { 2 } \right) + \phi _ { I , j } \right)\tag{5}
$$

where $A _ { j } , f _ { I , j } , \mu _ { j } ;$ , and $\phi _ { I , j }$ denote amplitude, carrier frequency, sweep slope, and initial phase for the jth interferer. In practice, interferers may have sweep slopes offset by ∼2%–10% from the victim radar and small start-time offsets; when these align, the interferer’s chirps can overlap 2–6 consecutive victim chirps, producing persistent structured interference. For example, typical values for automotive interference might be $A _ { j } = 1 \mathrm { V } , \mu _ { j } = 1 \mathrm { M H z } \mu \mathrm { s } ^ { - 1 }$ , and $f _ { I , j } \approx 7 7 \mathrm { G H z }$

When interferers remain nearly stationary relative to the victim, the baseband signal reduces to:

$$
\mathbf { i } \left( t \right) = A _ { I } \cdot \cos \left( 2 \pi \left( f _ { I } t + \phi _ { I } \right) \right) ,\tag{6}
$$

where $A _ { I } , f _ { I } ,$ and $\phi _ { I }$ are the amplitude, frequency, and phase of the interference.

The set of chirps affected by interference is defined as:

$$
\Omega = \{ c _ { 1 } , c _ { 2 } , \ldots , c _ { s } \} \subset [ 1 , 1 2 8 ] ,\tag{7}
$$

where Ω represents the span (range of chirps) corrupted by interference. Short spans (1–2 chirps) are easier to mitigate, while longer spans (5 or more chirps) pose significant challenges.

## 3.3. Overlap interference and its challenges

Overlap interference occurs when an interfering chirp i(t) temporally coincides with the target echo $b _ { k } ( t )$ within the same chirp in the fast-time domain. In this regime, the observed signal combines as:

$$
r _ { \mathrm { o v e r l a p } } \left( t \right) = \sum _ { k } b _ { k } \left( t \right) + \sum _ { j \in \Omega } i _ { j } \left( t \right) + n \left( t \right) ,\tag{8}
$$

where n(t) denotes additive noise.

Target and interference thus occupy the same time–frequency bins; simple forward/backward differencing leaves coupled residue, suppresses target beats, and blurs the RD profile, reducing SNIR. The impact scales with the span (number of consecutive chirps affected): for C1 (span = 1), most baseline methods remain effective. For C2 and larger (e.g. span = 3), discontinuities across chirps break difference-based assumptions and can remove target energy or introduce structured artifacts. Robust mitigation must (i) localize corrupted samples and (ii) reconstruct them while preserving chirp continuity and intra-chirp phase/shape.

When overlap occurs, several effects degrade the RD profile:

• Signal coupling: target and interference energy fall in the same FFT bins, so simple subtraction or masking cannot isolate one from the other.

• Target suppression: target beat components are partially masked, lowering SNIR and blurring localized RD peaks.

• Span dependence: errors compound as the span grows; discontinuities created by multiple corrupted chirps propagate to both range and Doppler.

![](images/51a12ae041f8f3e0ca865c7167cedd070a1d623b36c69c39b50247dcd59e0068.jpg)  
(a)

![](images/f9bb2f509ec7ea82c9fd2649eb47d340eb356ff8d5b3c30725f66da05fff65c5.jpg)  
(b)

![](images/516e2c135735510f1d1b15a3446812924d25b038bf6c4a9f43fda8e39432b3dc.jpg)  
(c)

![](images/9aa3b28dd58f4122c93834306138264829475a1590761c79cb9205c6801114b9.jpg)  
(d)

![](images/a8f467bae0e273b45521774cb10a5a8817d555cae1b209b345169a4bfbbcb2d6.jpg)  
(e)

![](images/ecf24479bf3410ab8ddab22ea9b4d19e6c0c6dd3a2d85183596510913d78c933.jpg)  
(f)  
Figure 1. Illustrative FMCW interference cases in time–frequency and range–Doppler domains. The top row (figure 1 (a)–(c)) shows waveform-level interactions; the bottom row (figure 1 (d)–(f)) shows the corresponding RD maps. Each column demonstrates how a specific chirp structure translates into RD artifacts: clean (a d), single-chirp C1 interference (b e), and multichirp C2 interference (c f). Panels 1(a)–(c) use ‘Victim Radar’ and ‘Interfering Radar’ to indicate dual-radar interactions in overlap scenarios, linking waveform features to downstream interference severity and motivating span-dependent mitigation strategies.

Implications for MTI-IM. Motion-cancelling subtraction between adjacent chirps MTI-IM preserves continuity and is effective for single-chirp overlap $( \mathrm { s p a n } = 1 , \mathrm { ^ { c 1 ^ { \circ } ) } }$ . For longer spans (e.g. span = 3, ‘C2’), corrupted blocks break forward/backward continuity, so subtraction removes portions of the target together with the interference and leaves residual artifacts. Figure 1 provides the illustrative traces used throughout the paper.

## 3.4. Illustrative examples and diagrams

Figure 1 Illustrates the mechanisms by which FMCW chirp interference manifests in both the time– frequency domain and corresponding RD output for three representative cases. The top row ((a)–(c)) presents waveform-level interactions between victim and interfering radars, while the bottom row ((d)– (f)) shows the corresponding RD maps after FFT processing. Each column visualizes the direct impact of time-frequency structure on RD artifacts.

• Figure 1 (a) Clean alignment. The victim’s transmit and receive chirps are perfectly matched in slope and timing. Figure 1 (d) RD map: two distinct targets with sharp, interference-free peaks (ideal baseline).

• Figure 1 (b) Single-chirp overlap (C1). An interfering radar overlaps one victim chirp with nearly identical slope, i.e. an isolated interference burst. Figure 1 (e) RD map: a narrow vertical streak at one range bin; target returns are preserved and are typically recoverable via subtraction-based methods (e.g. MTI-IM).

• Figure 1 (c) Multi-chirp overlap (C2, slope mismatch). The interfering radar overlaps three consecutive chirps with a slightly different slope, causing within-chirp frequency variation and strong coupling. Figure 1 (f) RD map: energy spreads across both range and Doppler, suppressing target energy and reducing SNIR; conventional differencing/masking struggles here.

These panels highlight a progression from benign to severe interference as span and slope mismatch increase. C1 preserves target continuity and is resilient to basic mitigation, whereas C2 produces distortions that propagate across chirps and degrade both range and Doppler estimation—motivating the advanced mitigation strategies developed in this work.

## 4. Proposed technique

## 4.1. Dataset and environment overview

The experimental evaluation was conducted using a real-world FMCW radar dataset acquired with the Texas Instruments AWR1443BOOST development platform. The radar configuration comprised four receive (Rx) channels and a single transmit (Tx) antenna, operating at a center frequency of 77 GHz. Each radar burst contained 128 chirps, and each chirp consisted of 512 fast-time samples. This yielded a data tensor of size 128 × 512 × 4 per burst, capturing both spatial and temporal signal characteristics.

In various dynamic scenarios, including both stationary and moving targets, 2493 radar bursts were recorded. The data collection spanned diverse environmental conditions and object geometries to ensure the robustness of the proposed interference detection and mitigation pipeline. The dataset provided a credible basis for generating interference patterns and assessing the effectiveness of the developed strategies.

For training and evaluate the TinyML-based interference classifier, the dataset was divided into training and testing sets using an 80:20 ratio. The training set contained a representative blend of all three interference categories (Clean, Low Interference, and Severe Overlap), with a balanced class proportions ensured using stratified sampling. Feature vectors extracted from each burst were normalized using zscore standardization prior to classification.

The classifier is trained for 20 epochs using a support vector machine (SVM) model with an radial basis function kernel. Dimensionality reduction via principal component analysis (PCA) was applied before training to reduce feature dimensionality and computational cost during inference. Only the leading principal components that accounted for the most substantial variance were retained. The trained model was subsequently deployed and validated in a simulated embedded environment representative of TinyML constraints, where memory usage and inference time benchmarks were recorded to evaluate deployment feasibility.

## 4.2. Interference injection for overlap simulation

To simulate realistic and challenging overlapping interference conditions, a targeted interference injection strategy was employed. The method involved extracting chirp segments from bursts that exhibited naturally occurring interference within the dataset and programmatically inserting them into clean bursts at controlled temporal positions. This process required a careful selection of interfered chirps, which were subsequently incorporated into uncorrupted time slots. The outcome was the generation of synthetic overlap conditions that effectively resembled actual radar-to-radar interference situations.

The injected chirps were positioned in non-overlapping regions with respect to the existing signal content, thereby ensuring that the resulting interference compromised chirp orthogonality, a critical assumption in FMCW radar signal separation. This intentional breach of temporal alignment mimicked situations where adjacent radar units operated out of synchronization, which resulted in significant spectral leakage and degraded target returns.

The implementation of synthetic overlap augmentation was essential for evaluating the effectiveness of IM techniques, particularly in scenarios characterized by dense, misaligned interference that poses challenges for conventional filtering methods. Moreover, it provided a controlled framework for benchmarking detection and recovery performance across a wide severity range, thereby assuring reproducibility and fairness in experimental validation.

## 4.3. Interference detection via TinyML and span logic

An interference detection pipeline is developed for deployment on TinyML-compatible embedded systems, optimized for real-time automotive radar signal processing. The architecture, as shown in figure 2, combines lightweight statistical feature extraction, machine learning classification, and rule-based logic to classify interference severity efficiently.

The detection process begins by computing a chirp-wise energy profile from each received radar burst. For each chirp n, its energy $P _ { n }$ in [54] is calculated by averaging the squared magnitude of the

![](images/4766359e22104e4a2a1a6e4d5a975bd4c130d0fecb23667007d1d651e5920525.jpg)  
Figure 2. TinyML-based interference detection workflow: feature extraction  spike-interval scoring  class mapping; PCA+SVM is trained offline and used at test time to produce the final label that drives mitigation.

complex signal samples.

$$
P _ { n } = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \lvert r ( n , k ) \rvert ^ { 2 }\tag{9}
$$

where K is the number of samples per chirp and $r ( n , k )$ denotes the signal at sample k in chirp n. This energy profile forms a temporal signature that reflects how power is distributed across time, allowing the identification of anomalies due to interference.

From this energy signature, seven statistical features are extracted: mean, standard deviation, maximum amplitude, variance, skewness, kurtosis, and the number of significant spikes. The seven statistical features were selected to capture both the global interference intensity and its temporal concentration across chirps. The mean, variance, and standard deviation of the chirp-energy profile reflect the overall power level and dispersion, which increase progressively from clean bursts (C0) to low-interference (C1) and severe overlap (C2). The maximum energy and the count of high-energy chirps emphasize localized power spikes and span length, enabling discrimination between short, isolated interference (C1) and longer multi-chirp overlap (C2). Kurtosis and skewness describe the sharpness and asymmetry of the energy distribution, separating borderline patterns near the C1/C2 boundary. Together, these features provide a compact but discriminative representation that enables reliable class assignment using a lightweight classifier. A spike is defined as any chirp whose energy exceeds a dynamic threshold T in [55].

$$
T = \mu _ { \mathrm { b a s e l i n e } } + \alpha \left( \mathrm { m a x } - \mu _ { \mathrm { b a s e l i n e } } \right)\tag{10}
$$

Here, $\mu$ represents the mean energy of the burst, max is the maximum energy observed within the same burst, and α is an empirical scaling coefficient that adjusts sensitivity to high-power events. The established threshold serves to isolate outlier chirps that are indicative of interference.

To prepare the feature set for classification, z-score normalization is applied to standardize feature scales. PCA is then performed to reduce dimensionality while preserving the most informative variance directions [1]. For each radar burst, we extract a seven-dimensional feature vector from the chirp-energy profile comprising the mean, standard deviation, maximum value, count of high-energy chirps above an adaptive threshold, variance, kurtosis, and skewness. The features are normalized using z-score statistics estimated from the training set and projected using PCA. We retain the first three principal components, which together explain 98.60% of the total variance, yielding a compact three-dimensional representation with negligible information loss. The resulting feature vector is classified using a bagged ensemble of 100 shallow decision trees trained with fitcensemble. The trained model, including PCA parameters and tree coefficients, occupies approximately 1.0 MB of memory. In our MATLAB prototype, the end-to-end inference pipeline (feature normalization, PCA projection, and ensemble prediction) requires on average ≈80 ms per burst (mean over 1000 random bursts). This value primarily reflects interpreter overhead and therefore represents a conservative upper bound on the computational cost of the decision module rather than an optimized embedded runtime. The reduced feature set is fed into a SVM classifier [2], which is trained to categorize each burst as either clean or interfered. The linear SVM model is selected for its computational efficiency and robust performance on embedded platforms.

![](images/613546f86d6a60d6823ab18260a87a323c4f4ebe79f84e42971f2244166e85b1.jpg)  
(a)

![](images/01a68d447cab89706266b66f749bd522cd8130868bf16cf99fb96fbe030d0c79.jpg)  
(b)  
Figure 3. Chirp-wise mean power for two radar bursts with the adaptive dynamic threshold from (2) overlaid (red dashed). (a) Burst 1962 shows two isolated high-energy spikes; (b) Burst 1940 shows a cluster of spikes near the end. Samples above the threshold are flagged as interference.

To complement the data-driven classifier, a span logic module analyzes the spatial distribution of detected spikes within each burst. It evaluates both the vertical (frequency) and horizontal (time) concentration of spikes and computes an interference score $f _ { \mathrm { s c o r e } }$ in (3).

$$
f _ { \mathrm { s c o r e } } = \frac { 1 } { 2 } \left( \mathrm { m e a n } \left( \nu _ { \mathrm { s c o r e s } } \right) + \mathrm { m e a n } \left( h _ { \mathrm { s c o r e s } } \right) \right)\tag{11}
$$

where $\nu _ { \mathrm { s c o r e s } }$ and $h _ { \mathrm { s c o r e s } }$ represent spike densities along the vertical and horizontal dimensions, respectively. Based on the resulting interference score, each burst is classified into one of three classes: Class 0 (Clean), Class 1 (Low Interference), or Class 2 (Severe Overlap).

Figure 3 shows two typical cases of chirp-wise mean power distributions of radar bursts of different patterns of interference. In the two panels, the red-dotted line is the adaptive threshold, as in (2), which is computed using the mean and maximum energy of the bursts. The subfigure (a) depicts a burst that has two interference spikes of varying chirp index that are typical of sporadic interference at low levels. The burst shown in subfigure (b) has a cluster of high-energy spikes near the end of the burst analogous to severe overlap and temporal correlation in the pattern of interferences. The dynamic thresholding technique works well when it comes to differentiating these high-power events through the baseline signal energy facilitating the detection of spikes at different degrees of interference levels.

A robust classifier demonstrating resilient performance across varied interference situations is achieved by integrating span logic for temporal structure assessment with TinyML-based generalization. The combined approach maintains a low computational footprint while enabling accurate realtime deployment on embedded radar systems. The objective of the decision module is not to maximize classification complexity, but to provide a minimal and deterministic TinyML mechanism that selects the appropriate mitigation path under strict latency and memory constraints. To this end, the classifier operates on only three PCA features and evaluates a set of shallow decision trees, requiring fewer than a few thousand primitive arithmetic and comparison operations per burst. This operation count is negligible compared with the FFT-based RD processing and is compatible with sub-millisecond execution in optimized C/TinyML implementations on embedded radar processors, while our MATLAB timing

provides a conservative upper bound. The framework is model-agnostic and could accommodate alternative lightweight classifiers (e.g. pruned or quantized networks) if required, but the chosen tree ensemble offers a favorable balance between accuracy, determinism, and deployability. ‘Future work may investigate alternative classifiers or quantized deployments within the same framework; however, the present design demonstrates that a minimal, deterministic TinyML decision module is sufficient to support classadaptive IM under realistic embedded-radar constraints.’ These design choices collectively satisfy the practical constraints of automotive edge radar-robustness, low latency, and compute efficiency.

## 4.4. Class-based adaptive mitigation logic

• Class 0 (clean): bursts that were identified as free from interference were passed through the standard signal processing chain without suppression. This chain included windowing and RD processing via FFT. Since no interference was present, the processing introduced minimal latency while preserving the original signal content.

• Class 1 (low interference): bursts exhibiting mild or partial interference were processed using a MTI-IM technique. This method applied selective filtering to suppress localized distortions while retaining the underlying target information. The approach offered a favorable balance between mitigation effectiveness and computational cost, thereby making it suitable for real-time implementation in lowinterference conditions.

• Class 2 (severe overlap): bursts that were severely affected by interference underwent a two-stage recovery procedure. First, a blanking operation identified and removed the heavily corrupted chirps. Subsequently, spline interpolation was employed to reconstruct the missing segments using adjacent clean chirps as references. This procedure restored signal continuity and spectral integrity, even under substantial interference.

By tailoring the processing pipeline to the predicted interference class, the system ensured that highcomplexity operations were invoked only for severely degraded bursts. Clean and mildly affected bursts were processed with minimal overhead, thereby supporting low-latency operation and scalable performance in dynamic radar environments characterized by varying levels of mutual interference.

The proposed mitigation pipeline begins by extracting relevant features and classifying each radar burst using a lightweight TinyML model to determine the level of interference (see figure 4). The resulting decision–clean (C0), low (C1), or severe (C2)–determines the subsequent mitigation path. For clean or low-interference bursts, a fast fallback branch ensures low computational overhead, utilizing standard signal processing for C0 and conventional MTI-IM subtraction for C1. For severe (span C2) overlap cases, the pipeline invokes the full suite of proposed strategies: energy-based detection, targeted blanking of corrupted chirps, in-chirp interpolation to restore signal continuity, and light Kalman smoothing to suppress reconstruction artifacts. All outputs are passed to FFT processing to yield final RD maps, and performance is quantified by SNIR improvement and qualitative target recovery across the full spectrum of test conditions. See figure 2 for expanded details of the feature extraction and classification process.

## 4.5. Blanking + interpolation with fixed KF

The proposed IM method directly addresses the overlap interference challenges outlined in section 3.3, particularly for multi-chirp scenarios (C2 and beyond) where forward–backward differencing and MTI IM methods fail due to discontinuities across multiple victim chirps. The pipeline operates in three stages: energy-based detection, hard blanking with interpolation, and optional Kalman smoothing.

## 4.5.1. Energy-based chirp detection

Recall from (4) that the received signal r(t) contains target echoes, interference, and noise. To identify chirps corrupted by overlap interference (as visualized in figures 1 (b) and (c)), the energy of each chirp is compared against a robust statistical threshold.

The chirp energy $E _ { \mathrm { c } }$ for the cth chirp is computed as:

$$
E _ { c } = \sum _ { k = 1 } ^ { K } \left| r \left( k , c \right) \right| ^ { 2 } ,\tag{12}
$$

where K is the number of fast-time samples per chirp, and $r ( k , c )$ denotes the baseband signal at sample k in chirp c.

The set of corrupted chirps is identified as:

$$
\mathcal { T } = \left\{ c \vert E _ { c } > \mu + k \sigma \right\} ,\tag{13}
$$

![](images/d67aa25ee039b454369114419e12be5dedd733739e350561388d5db07b641fd6.jpg)  
Figure 4. Block diagram of the proposed FMCW radar interference mitigation pipeline. The pipeline includes TinyML-based classification, branch selection, and signal recovery paths for different interference levels.

where $\mu$ and $\sigma$ are the mean and standard deviation of the chirp energy profile across the observation window, respectively. In this work, k = 2.5 is fixed to ensure stable detection across varying interference levels while minimizing false positives from noise or weak targets.

This energy-based approach is motivated by the elevated power signature of overlap interference (figures 1 (e) and (f)), which consistently produces $E _ { \mathrm { c } }$ values significantly exceeding the clean baseline. The high-energy corruption clearly exceeds the global energy threshold $E _ { \mathrm { t h } }$ , motivating the binary flagging in the subsequent blanking stage.

## 4.5.2. Hard blanking and binary masking

A binary mask $M ( c )$ is generated to perform hard blanking on detected interference chirps:

$$
M ( c ) = { \left\{ \begin{array} { l l } { 0 , } & { c \in { \mathcal { Z } } , } \\ { 1 , } & { { \mathrm { o t h e r w i s e } } . } \end{array} \right. }\tag{14}
$$

The blanked signal is expressed as:

$$
r _ { \mathrm { b l a n k e d } } \left( t , c \right) = M ( c ) \cdot r \left( t , c \right) ,\tag{15}
$$

where all detected interference chirps are nullified. This operation directly removes the coupling effect described in section 3.3, preventing corrupted samples from contaminating adjacent chirps during FFT processing.

![](images/84f4fbd3ab55437f62665f202d9e090020e32f1c5fac117e9fd5f015c29d46a9.jpg)  
(a)

![](images/201dff52b56aed6bf721e7b20cc649ad9b4e599c4f24b87e968a3d08e04434f7.jpg)  
(b)

![](images/ad01ac7d89bf21e282cb2192bd0d6210c7833c9f3d1974b9c595a742e69b4d98.jpg)  
(c)

![](images/dce21025a3953b3097e258703482300b19751516ebc34494e61a3958df424652.jpg)  
(d)

![](images/444791ed9116aa63345e63138d6796d5de66886c6b388f6184c68ab1a9fcc6d8.jpg)  
(e)

![](images/944868d87efcdd00826a17ae17ac5572e4f418c3bf4ad1f8eaf8c87b93d04a20.jpg)  
(f)  
Figure 5. Visualization of the proposed mitigation pipeline on a 5-chirp window (chirps 59–63; target = c1): (a) original signal; (b) chirp-energy detection; (c) original target chirp; (d) after blanking; (e) after RMLE interpolation; (f) after fixed-gain Kalman smoothing.

## 4.5.3. Linear interpolation for missing chirps

Following blanking, the missing data is reconstructed using linear interpolation along the slow-time (chirp) dimension for each range bin independently:

$$
\hat { r } \left( t , c \right) = \mathrm { L i n e a r I n t e r p } \left( r _ { \mathrm { b l a n k e d } } \left( t , c \right) \right) ,\tag{16}
$$

where the real and imaginary components are interpolated independently using standard methods (e.g.   
interp1 in MATLAB).

Linear interpolation is chosen by default because it provides a favorable trade-off between computational cost (∼10 ms per frame) and RD-profile quality, whereas spline or Piecewise Cubic Hermite Interpolating Polynomial (PCHIP) methods introduce 25–30× higher latency. For automotive real-time constraints, this efficiency is critical. The interpolated signal $\hat { \boldsymbol r } ( t , \boldsymbol c )$ restores chirp continuity, enabling downstream FFT processing without discontinuity-induced artifacts.

## 4.5.4. Fixed-parameter kalman smoothing

Finally, a lightweight scalar Kalman filter with a fixed gain of $\alpha = 0 . 2 5$ is applied along the slow-time dimension to smooth residual distortions while preserving target fidelity. The update rule for each range bin is:

$$
\tilde { r } ( t , c ) = \tilde { r } ( t , c - 1 ) + \alpha \cdot \big ( \hat { r } ( t , c ) - \tilde { r } ( t , c - 1 ) \big ) ,\tag{17}
$$

where $\tilde { r } ( t , c )$ is the smoothed signal. The initialization is set to $\tilde { r } ( t , 0 ) = \hat { r } ( t , 0 )$ (the first interpolated chirp), and the filter is applied causally along the slow-time dimension for each range bin. The fixed gain $\alpha = 0 . 2 5$ balances noise suppression and signal responsiveness, preventing over-smoothing that would blur localized target returns. This regularization step mitigates interpolation-induced ripple while maintaining the range-profile texture necessary for downstream detection algorithms.

Figure 5 summarizes the proposed pipeline: energy detection → per-sample detection/blanking → in-chirp interpolation → light fixed-parameter KF.

• Figure 5 (a) original signal real (5-chirp window). Real parts of chirps 59–63 are overlaid; the target chirp (61) is highlighted. A high-energy corruption is visible in the target. This corruption clearly exceeds the global energy threshold $E _ { \mathrm { t h } } .$ , as quantified in the next stage.

![](images/a1af3735360479441817f1025a802b25676447dda60de9558fd269ad6ee6a040.jpg)  
Figure 6. Chirp 61 (real part) before and after the full mitigation pipeline. The pipeline consists of blanking, PCHIP interpolation, and fixed-gain Kalman filtering (KF).

• Figure $5 \ ( \mathrm { b } )$ chirp-energy detection (target = 61). The energy of each chirp is shown with a global threshold $E _ { \mathrm { t h } } .$ . Chirp 61 clearly exceeds $E _ { \mathrm { t h } }$ and is flagged.

• Figure $5 \ ( c )$ original (chirp 61) real. The fast-time waveform of the target chirp prior to processing, showing the corrupted segment.

• Figure 5 (d) after blanking (real). Samples are declared interfered using a robust median absolute deviation-based threshold (dilated by ±10 samples) and set to zero. The flat segment indicates the excised region.

• Figure 5 (e) after interpolation (PCHIP, Real). The missing fast-time samples within the target chirp are reconstructed by shape-preserving cubic interpolation (PCHIP), restoring continuity and reducing spectral leakage.

• Figure 5 (f) after KF (Real, α = 0.12). A lightweight fixed-parameter scalar Kalman smoother is applied to the interpolated region, regularizing residual ripple while preserving the surrounding rangeprofile texture.

As shown in figure 6, the before/after overlay of the target chirp confirms that the pipeline (blanking + PCHIP + fixed KF) suppresses the corruption without distorting the remainder of the chirp; together with the shared y-axis limits in figures 5 (d)–(f), this provides a fair visual comparison.

Algorithm 1 summarizes the complete runtime pipeline, integrating class-based decision logic with the proposed blanking, interpolation, and fixed-parameter Kalman smoothing stages.

## 4.6. Fixed parameter strategy

To maintain low runtime and ensure deterministic real-time execution suitable for automotive deployment, the proposed method employs fixed parameters rather than adaptive tuning. This design minimizes branching logic and computational overhead:

• Fixed threshold: the interference detection threshold is fixed at $\mu + 2 . 5 ~ \sigma$ for all bursts.

• Fixed interpolation mode: linear interpolation is always used for both real and imaginary components.

• Fixed Kalman gain: the KF gain is fixed at $\alpha = 0 . 2 5$ , avoiding span-dependent tuning.

These parameter choices were informed by the span-dependent interference characteristics described in section 3.3 and validated across the C1 and C2 scenarios illustrated in figure 1. The fixed strategy ensures consistent performance without per-frame recalibration, which is critical for real-time automotive radar systems.

To verify that the fixed parameters do not bias performance, we conducted a sensitivity study across representative interference spans. The detection threshold multiplier $( \mu + k \sigma )$ was varied in the range $k = 2 . 0 { - } 3 . 0 $ , and the resulting SNIR variation remained below 0.1 dB, confirming that the threshold is not critical once high-energy chirps are detected. Three interpolation schemes (linear, spline, and PCHIP) were evaluated; linear interpolation achieved comparable SNIR while reducing runtime by 40%– 60%, making it the most suitable choice for real-time embedded deployment. Finally, the Kalman gain α was swept in the range 0.15–0.35, and SNIR differences remained below 0.2 dB, indicating robustness to α-selection. The chosen value $\alpha = 0 . 2 5$ therefore represents a stable mid-range setting. These results justify the fixed-parameter configuration as a practical balance between accuracy, latency, and implementation simplicity on edge hardware. A sensitivity analysis validating these parameter choices is presented in table 3.

Algorithm 1. Runtime pipeline for class-driven FMCW radar interference mitigation.   
Input: radarData, burst index $^ { b , }$ clean reference $b _ { \mathrm { r e f } }$ , model M, method m   
Output: (RD,SNIR)   
1: Extract ${ \bf X } _ { b } [ r , : , : ] \gets r a d a r D a t a [ r , : , : , b ] , r = 1 . . N _ { \mathrm { R x } }$   
2: Extract $\mathbf { X } _ { \mathrm { r e f } } [ r , : , : ] \gets$ radarData $[ r , : , : , b _ { \mathrm { r e f } } ]$   
3: for $r = 1 . . N _ { \mathrm { R x } }$ do   
4: (1) Feature extraction for classification   
5: $p _ { r } [ k ] \gets \mathrm { m e a n } _ { n } ( | \mathbf { X } _ { b } [ r , n , k ] | ^ { 2 } ) , k = 1 . . N _ { c }$   
6: $\mathbf f _ { r } \gets$ ExtractFeatures $\left( \boldsymbol { p } _ { r } , \mathbf { X } _ { b } [ r , : , : ] \right)$   
7: <sup>˜</sup>f<sub>r</sub> ← Preprocess $( \mathbf { f } _ { r } , \mathcal { M } )$   
8: ˆc ← PredictClass $( \tilde { \mathbf { f } } _ { r } , \mathcal { M } )$   
9: (2) Choose mitigation branch   
10: if m ̸= FPM then   
11: $\mathbf { Z } _ { r }  \mathbf { A }$ pplyMethod $( \mathbf { X } _ { b } [ r , : , : ] , m )$   
12: else if $\hat { c } _ { r } = \mathrm { C } 0$ then $\mathbf Z _ { r } \gets \mathbf { \bar { X } } _ { b } [ r , : , : ]$   
13: else if $\hat { c } _ { r } = \mathrm { C } 1$ then $\mathbf { Z } _ { r }  \mathrm { M T I I M } ( \mathbf { X } _ { b } [ r , : , : ] )$   
14: else % $\hat { c } _ { r } = \mathrm { C } 2$   
15: $T _ { r } \gets \mu _ { \mathrm { b a s e } } + \alpha ( \rho _ { \mathrm { m a x } } - \mu _ { \mathrm { b a s e } } )$   
16: $M _ { r } [ k ]  \mathbb { I } ( p _ { r } [ k ] > T _ { r } )$   
17: $\mathbf { X } _ { r } ^ { \prime } [ : , k ] \gets 0$ for k where $M _ { r } [ k ] = 1$   
18: $\mathbf { X } _ { r } ^ { \prime \prime }$ ← InterpolateChirps $\textstyle \left( \mathbf { X } _ { r } ^ { \prime } , M _ { r } , \right)$ linear   
19: $\mathbf { Z } _ { r } \gets \mathrm { F i x e d K F } ( \mathbf { X } _ { r } ^ { \prime \prime } , \alpha _ { \mathrm { K F } } )$   
20: end if   
21: end for   
22: (3) RD and SNIR evaluation (consistent across methods)   
23: RD<sup>(r)</sup> ← RangeDopplerFFT(Z<sub>r</sub>)   
24: $\mathbf { R D }  \mathrm { C o m b i n e R x } ( \{ \mathbf { R D } ^ { ( r ) } \} _ { r = 1 } ^ { N _ { \mathrm { R x } } } )$   
25: $\mathrm { S N I R }  \mathrm { C o m p u t e S N I R } ( \mathbf { Z } , \mathbf { X } _ { \mathrm { r e f } } )$

## 4.7. Performance metrics

The performance of the proposed method is evaluated using a combination of quantitative metrics (SNIR improvement and execution time) and qualitative indicators (RD profiles).

(1) SNIR evaluation: the SNIR quantifies the interference suppression capability of the proposed method by comparing the clean reference signal to the interfered burst before and after mitigation:

$$
\mathrm { S N I R } = 1 0 \cdot \log _ { 1 0 } \left( \frac { \lVert r _ { \mathrm { c l e a n } } \rVert ^ { 2 } } { \lVert r _ { \mathrm { i n t e r f } } - r _ { \mathrm { c l e a n } } \rVert ^ { 2 } } \right) ,\tag{18}
$$

where $r _ { \mathrm { c l e a n } }$ denotes the reference clean burst (without interference), and $r _ { \mathrm { i n t e r f } }$ represents the burst corrupted by overlap interference prior to mitigation. The SNIR is computed both before (baseline) and after mitigation to quantify the improvement in dB. Higher SNIR values indicate better interference suppression and signal recovery.

(2) Time consumption: to ensure real-time feasibility, the total runtime of the algorithm (measured in milliseconds per frame) is decomposed as:

$$
T _ { \mathrm { t o t a l } } = T _ { \mathrm { b l a n k i n g } } + T _ { \mathrm { i n t e r p } } + T _ { \mathrm { K F } } + T _ { \mathrm { T i n y M L } } ,\tag{19}
$$

where each term corresponds to the processing time (in ms) of blanking, interpolation, Kalman filtering, and TinyML classification, respectively. For automotive radar applications, $T _ { \mathrm { t o t a l } } < 5 0$ ms per frame is typically required for real-time operation.

(3) RD-Profile Evaluation: RD profiles serve as a qualitative indicator of signal recovery fidelity. Visual comparison of RD maps before and after mitigation enables assessment of target clarity, peak sharpness, sidelobe suppression, and noise floor reduction. These metrics provide intuitive confirmation that the proposed method preserves target detectability and RD structure across varying interference scenarios (C1, C2), as established in section 3.3. Quantitative target detection performance (e.g. probability of detection, false alarm rate) is evaluated in the experimental section.

Algorithm 2. Evaluation protocol for multi-span, multi-burst statistical analysis.   
Input: radarData ∈ C<sup>NRx</sup>×<sup>Ns</sup>×<sup>Nc</sup>×<sup>N</sup>b;   
reference burst index b (clean);   
span groups $\{ B _ { s } \} _ { s = 1 } ^ { S } ;$   
trained TinyML model $\mathcal { M } ;$   
mitigation methods {ZEROING,MTI--IM,IMAT,WD,FPM}   
Output: Mean and standard deviation of SNIR per span and method   
1: for s = 1..Sdo % span length = s chirps   
2: for eachb ∈ B do % multiple burst realizations   
3: for eachm ∈ {ZEROING,MTI--IM,IMAT,WD,FPM}do   
4: (RD<sup>(m)</sup>, SNIR<sup>(m)</sup>) ← RunPipeline(radarData, $b , b _ { \mathrm { r e f } } , \mathcal { M } , m )$   
5: end for   
6: end for   
7: Compute $\mu _ { s } ^ { ( m ) }  \mathrm { m e a n } _ { b \in \mathcal { B } _ { s } } ( \mathrm { S N I R } _ { b } ^ { ( m ) } )$   
8: Compute $\sigma _ { s } ^ { ( m ) } \gets \mathrm { s t d } _ { b \in \mathcal { B } _ { s } } ( \mathrm { S N I R } _ { b } ^ { ( m ) } )$   
9: end for   
10: Report table: $\mu _ { s } ^ { ( m ) } \pm \sigma _ { s } ^ { ( m ) }$ for all s,m   
11: Plot SNIR vs span with error bars $\pm \sigma _ { s } ^ { ( m ) }$ (optional)

Algorithm 2 summarizes the evaluation protocol used across all interference spans and mitigation techniques.

## 4.8. Specific drawbacks of proposed method

Although the proposed approach achieves low latency and stable performance, it has several limitations:

• Lack of adaptivity: fixed parameters (threshold, interpolation mode, and Kalman gain) limit flexibility in handling diverse interference patterns.

• Linear interpolation artifacts: using linear interpolation can cause minor flattening in the RD-profile peaks compared to higher-order methods.

• Degradation for long spans: when more than 5–6 chirps are corrupted, reconstruction quality and SNIR improvement decline significantly.

• Kalman oversmoothing: a fixed gain (α = 0.25) may slightly attenuate weak moving targets.

## 5. Experimental tests and results

This section presents the experimental setup, implementation flow, and comparative evaluation of the proposed IM technique. Each step from interference injection to mitigation performance is discussed using a combination of real-world radar data, synthetic overlap scenarios, and lightweight classification logic.

## 5.1. Dataset and pre-processing

The experiments are conducted on a dataset collected using the TI AWR1443BOOST radar, consisting of 2493 bursts with 128 chirps per burst and 512 fast-time samples per chirp across 4 Rx channels. Pre-processing includes range FFT (fast-time), Doppler FFT (slow-time), and optional filtering steps. Baseline metrics such as signal power, SNIR, and RD-profile contrast are computed.

## 5.2. Overlap interference injection

To emulate realistic radar-to-radar interference, chirps from real interfered bursts are selectively injected into clean bursts. The injected chirps are overwritten on consecutive chirp indices, creating controlled interference spans of varying lengths (e.g. 1, 2, or 6 consecutive chirps). This approach reproduces practical overlap scenarios where the number of corrupted chirps directly affects both the signal recovery difficulty and the resulting RD-profile quality.

![](images/92fe71a348845c4014e1e9be34867f7b8ea0eb074776c3a618cad3bd0871add3.jpg)

![](images/9f36437e1b527d66837038117ab7e1f791902ceca38301bcbeca3a01ccb1d42c.jpg)

Burst 1955 (Interference Span 6)  
![](images/c8ac62dc60e862a4b9eef69112c591f5693294953592be042a103c79282010b4.jpg)  
Figure 7. Grouped interference energy for three sample bursts: Burst 1940 (span 1), Burst 1964 (span 2), and Burst 1955 (span 6). The interfered chirps exceed the energy threshold (red dashed line).

Figure 7 illustrates three representative interference spans:

• Span 1 (Burst 1940): a single interfered chirp is injected, resulting in minimal corruption and relatively easy recovery.

• Span 2 (Burst 1964): two consecutive interfered chirps create moderate distortion, requiring both blanking and interpolation for effective restoration.

• Span 6 (Burst 1955): six consecutive interfered chirps represent a severe overlap scenario, posing a significant challenge for interpolation-based reconstruction.

The figure plots the total chirp energy across all 128 chirps in each burst, with the interference threshold (dashed red line) clearly separating interfered chirps from the background energy level.

## 5.3. Interference classification (TinyML + Span logic)

To investigate the behavior of the proposed classifier at the burst level, representative testing outcomes were analyzed. The comparison between vertical, horizontal, and final rule-based decisions with the TinyML-based predictor provides insight into both consistent and borderline cases. As shown in table 1, the majority of clean bursts were consistently classified with confidence values equal to or very close to unity, indicating that the framework reliably preserves correct decisions under nominal conditions. For example, Bursts 1, 3, and 4 were unanimously classified as clean across all modules and the TinyML predictor, each with a confidence score of 1.00.

Borderline cases were primarily observed at the transition between low interference and severe overlap. For example, Burst 2041 was labeled severe overlap by the vertical and horizontal modules as well as by the integrated final decision, whereas the TinyML predictor assigned low interference with reduced confidence (0. 64). This constitutes a false negative with respect to the true severe overlap class, indicating that borderline interference conditions can introduce ambiguity in classification. Conversely, Bursts 2, 5, and 2493 where the final decision was low interference and the predictor agreed with confidence values of 0.97, 0.99, and 0.99, respectively illustrate that confidence tends to decrease when the interference pattern lies near the decision boundary.

While table 1 illustrates consistent and borderline cases at the burst level, it does not capture the aggregate distribution over the entire test set. For completeness, the overall performance of the TinyML predictor is summarized by the confusion matrix in figure 8, which reports the three classes of interest: clean (Class 0), low interference (Class 1), and severe overlap (Class 2).

Table 1. Representative testing outcomes of the proposed classifier.
<table><tr><td>Burst idx</td><td>Vertical</td><td>Horizontal</td><td>Final</td><td>TinyML pred</td><td>True label</td><td>acc</td><td>conf.</td></tr><tr><td>1</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>1</td><td>1.00</td></tr><tr><td>2</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Low interference</td><td>Low interference</td><td>1</td><td>0.97</td></tr><tr><td>3</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>1</td><td>1.00</td></tr><tr><td>4</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>1</td><td>1.00</td></tr><tr><td>5</td><td>Low interference</td><td>Low interference</td><td>Low interference</td><td>Low interference</td><td>Low interference</td><td>1</td><td>0.99</td></tr><tr><td>2040</td><td>Clean</td><td>Low interference</td><td>Low interference</td><td>Low interference</td><td>Low interference</td><td>1</td><td>1.00</td></tr><tr><td>2041</td><td>Severe overlap</td><td>Low interference</td><td>Severe overlap</td><td>Low interference</td><td>Severe overlap</td><td>1</td><td>0.64</td></tr><tr><td>2042</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Low interference</td><td>Clean</td><td>1</td><td>1.00</td></tr><tr><td>2043</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>Clean</td><td>1</td><td>1.00</td></tr></table>

![](images/89768ca01fe75f1aea3b3d55ff4ccfab28822ba82c01a214e6e28b9435dfe4ee.jpg)  
Figure 8. Confusion matrix of the proposed classifier. Class 0: clean, Class 1: low interference, Class 2: severe overlap.

Confusion-matrix summary (figure 8) a total of 1887 clean bursts were correctly classified, yielding no false negatives and only two false positives. For low interference, 554 bursts were correctly identified, with two misclassified as clean and one as severe overlap. For severe overlap, 48 bursts were correctly recognized, with one misclassified as low interference. Over all 2,493 bursts, the overall accuracy is 99.84%.

Class-wise metrics for clean, precision, recall, and F1 were 99.89%, 100%, and 99.94%, respectively. For low interference, the values were 99.82%, 99.46%, and 99.64%. For severe overlap, precision, recall, and F1-score each reached 97.96%. The macro-averaged F1-score is 99.18%, and the balanced accuracy is 99.14%.

Implications these results highlight two practical points: (i) the classifier provides near-perfect detection of clean bursts and robust recognition of both low interference and severe overlap, even under class imbalance; and (ii) the predicted confidence serves as a reliable proxy for decision certainty lower confidence consistently appears on borderline or misclassified cases enabling the use of adaptive confidence thresholds as a safeguard for conservative interference-mitigation triggers in automotive radar deployments.

Table 2. Mean SNIR (dB) standard deviation across bursts for different interference spans.
<table><tr><td>Span</td><td>Zeroing</td><td>MTI-IM</td><td>IMAT</td><td>WD</td><td>FPM</td></tr><tr><td>1</td><td> $3 7 . 4 1 \pm 0 . 8 4$ </td><td> $3 6 . 8 6 \pm 2 . 3 2$ </td><td> $3 7 . 7 6 \pm 0 . 8 5$ </td><td> $3 0 . 7 1 \pm 0 . 7 8$ </td><td> $3 6 . 8 4 \pm 0 . 2 4$ </td></tr><tr><td>2</td><td> $3 6 . 7 0 \pm 1 . 6 0$ </td><td> $3 6 . 0 3 \pm 2 . 7 5$ </td><td> $3 7 . 5 6 \pm 0 . 6 6$ </td><td> $3 0 . 7 4 \pm 0 . 6 4$ </td><td> $3 6 . 7 3 \pm 0 . 2 9$ </td></tr><tr><td>3</td><td> $3 6 . 5 5 \pm 1 . 8 0$ </td><td> $3 6 . 1 0 \pm 2 . 8 7$ </td><td> $3 7 . 5 7 \pm 0 . 6 8$ </td><td> $3 0 . 5 6 \pm 0 . 6 9$ </td><td> $3 6 . 6 8 \pm 0 . 3 0$ </td></tr><tr><td>4</td><td> $3 5 . 9 8 \pm 2 . 0 0$ </td><td> $3 2 . 6 9 \pm 2 . 1 8$ </td><td> $3 7 . 3 6 \pm 0 . 6 1$ </td><td> $3 0 . 7 5 \pm 0 . 6 7$ </td><td> $3 6 . 6 0 \pm 0 . 3 1$ </td></tr><tr><td>5</td><td> $3 5 . 5 2 \pm 2 . 2 9$ </td><td> $3 2 . 7 4 \pm 2 . 2 0$ </td><td> $3 7 . 4 2 \pm 0 . 5 9$ </td><td> $3 0 . 7 1 \pm 0 . 7 8$ </td><td> $3 6 . 5 7 \pm 0 . 3 1$ </td></tr><tr><td>6</td><td> $3 5 . 5 7 \pm 2 . 4 5$ </td><td> $3 2 . 8 9 \pm 1 . 9 4$ </td><td> $3 7 . 2 4 \pm 0 . 5 3$ </td><td> $3 0 . 7 3 \pm 0 . 7 5$ </td><td> $3 6 . 3 0 \pm 0 . 5 7$ </td></tr><tr><td>7</td><td> $3 4 . 6 6 \pm 3 . 1 6$ </td><td> $3 4 . 3 1 \pm 2 . 1 1$ </td><td> $3 7 . 3 3 \pm 0 . 5 8$ </td><td> $3 0 . 6 9 \pm 0 . 8 0$ </td><td> $3 6 . 2 6 \pm 0 . 5 8$ </td></tr><tr><td>8</td><td> $3 4 . 5 6 \pm 3 . 1 0$ </td><td> $3 2 . 6 3 \pm 2 . 0 2$ </td><td> $3 7 . 1 3 \pm 0 . 5 1$ </td><td> $3 0 . 7 4 \pm 0 . 7 4$ </td><td> $3 6 . 0 6 \pm 0 . 8 8$ </td></tr><tr><td>9</td><td> $3 2 . 0 8 \pm 1 . 9 9$ </td><td> $3 5 . 9 4 \pm 3 . 1 9$ </td><td> $3 7 . 3 0 \pm 0 . 5 4$ </td><td> $3 0 . 7 5 \pm 0 . 7 3$ </td><td> $3 6 . 2 2 \pm 0 . 6 0$ </td></tr><tr><td>10</td><td> $3 1 . 5 2 \pm 2 . 0 1$ </td><td> $3 4 . 8 1 \pm 2 . 0 2$ </td><td> $3 6 . 8 3 \pm 1 . 3 4$ </td><td> $3 0 . 7 3 \pm 0 . 7 3$ </td><td> $3 6 . 0 0 \pm 0 . 7 6$ </td></tr></table>

![](images/70af224dee525f5636afe9345e50c75a9e6d8f7dc857fc0bf123c9909a516fd6.jpg)  
Figure 9. Mean SNIR versus interference span with error bars indicating one standard deviation across bursts.

## 5.4. Mitigation performance per class (All Techniques)

We compare five techniques Zeroing, MTI–IM [37], IMAT [40], WD [8], and the proposed fast precision mitigation (FPM) across interference spans from 1 to 6 chirps; figures 10–13 summarize the trends.

To evaluate robustness beyond single-burst examples, we further performed a statistical analysis across multiple burst realizations for each interference span. For each span length, ten bursts with comparable interference characteristics were selected, and the mean SNIR and standard deviation were computed for all mitigation techniques. The results are summarized in table 2 and figure 9.

As shown in figure 9, classical methods such as Zeroing and MTI–IM exhibit increasing performance degradation and larger variance as the interference span increases, reflecting their sensitivity to burst-specific interference patterns and overlapping chirp corruption. IMAT achieves the highest absolute SNIR values but relies on iterative processing and incurs increased computational cost. The corresponding numerical results in table 2 confirm this trend, showing larger burst-to-burst variability for classical methods as the interference span increases.

For each interference span, ten independent burst realizations with comparable interference characteristics were evaluated. The mean SNIR and standard deviation were computed to characterize both average performance and burst-to-burst variability, providing a basic statistical description of robustness. Across spans ⩾ 2 chirps, the SNIR improvement of the proposed FPM over Zeroing and MTI– IM exceeds one standard deviation, indicating a statistically meaningful and consistent performance difference.

In contrast, the proposed FPM method maintains a relatively stable SNIR across all spans, with consistently low standard deviation (typically below 1 dB), indicating strong robustness against burst-toburst variations. Although its absolute SNIR is slightly lower than IMAT in some cases, FPM provides a favorable trade-off between performance stability and computational efficiency, which is critical for real-time automotive radar applications.

Table 3. Sensitivity analysis of fixed-parameter configuration.
<table><tr><td>Parameter study</td><td>Tested range</td><td>SNIR variation</td><td>Runtime</td><td>Conclusion</td></tr><tr><td>Threshold  $( \mu + k \sigma )$ </td><td> $k = 2 . 0 { - 3 . 0 }$ </td><td> $< 0 . 1 \mathrm { d B }$ </td><td></td><td>Not critical</td></tr><tr><td>Interpolation</td><td>Linear / Spline / PCHIP</td><td> $\pm 0 . 2 \ : \mathrm { d B }$ </td><td> $\sim 2 \times \mathrm { f a s t e r }$ </td><td>Linear chosen</td></tr><tr><td>KF gain α</td><td> $0 . 1 5 / 0 . 2 5 / 0 . 3 5$ </td><td> $< 0 . 2 \ : \mathrm { d B }$ </td><td></td><td>α = 0.25 stable</td></tr></table>

## Zeroing, Span 1

## MTI-IM, Span 1

![](images/540efda4071cd8bbb16f825422d3a8384c9b94c1c2fbed623dc788241a1ad074.jpg)  
(a)

![](images/97966baf497c14be13b1285f1a32ba5be13aadb9ece2bef6920690b04dbef0bd.jpg)  
(b)

IMAT, Span 1  
![](images/718336a8714016dd14c1bef71f211080332ab45715421fa6c209742b38c4db0a.jpg)  
(c)

WD, Span 1  
![](images/3c6789090e39aee23ca58e2032d10cbf29ac3009d6eeda83a04ee82a8e7ebebe.jpg)  
(d)

FPM, Span 1  
![](images/8141fdeb706db1aa82a3490d2d53306c621115b3b0c6cb5c9393277349c8776c.jpg)  
(e)  
Figure 10. RD profile comparison—Span 1 (all techniques). (a) Zeroing, (b) MTI-IM, (c) IMAT, (d) WD, and (e) FPM. All plots use the same color scale (power in dB).

To justify the use of fixed parameters in the proposed pipeline, we conducted a sensitivity analysis across representative interference spans. The detection threshold multiplier $( \mu + k \sigma )$ was swept over $k = 2 . 0 { - } 3 . 0 $ , three interpolation schemes (linear, spline, and PCHIP) were compared, and the Kalman gain was varied in the range $\alpha = 0 . 1 5  – 0 . 3 5$ . As summarized in table X, the resulting SNIR variation remains below 0.2 dB, demonstrating that the method is not sensitive to fine tuning of these parameters. Linear interpolation provides comparable SNIR while reducing runtime by 40%–60%, and $\alpha = 0 . 2 5$ offers a stable middle-range setting, making the chosen configuration appropriate for real-time embedded deployment.

Table 3 presents the parameter sensitivity analysis for the proposed fixed-parameter mitigation pipeline. The table reports the effect of varying the detection threshold multiplier $( \mu + k \sigma )$ , interpolation method, and Kalman gain α on SNIR and runtime. Across all tested settings, SNIR variation remains below 0.2 dB, indicating that performance is robust to parameter choice. Linear interpolation is therefore selected for deployment due to its significantly lower runtime with negligible loss in accuracy.

• Figure 10 (Span 1, all techniques): with a single interfered chirp, all methods effectively restore the RD profile. Visual differences and SNIR gaps are small; simpler methods (Zeroing, MTI–IM) are slightly faster due to lower computational cost.

Zeroing, Span 2  
![](images/c9d5851980dfef9e5dfb63c79496d7f35d7b56455e530a75bda79859530f746d.jpg)  
(a)

MTI-IM, Span 2  
![](images/afb26823be6892e5302b2149b9ac78d1116b6a67dbfd1318fc3882d229160e04.jpg)  
(b)

IMAT, Span 2  
![](images/54d058ce733cc5a1c0299b0c83c7222f1c879de1d2f555aec2d0fbbc9d1a5445.jpg)  
(c)

WD, Span 2  
![](images/19c85a24f4593da5d4a56756388ed5a60d39f569960b3b137c4a0115883609a1.jpg)  
(d)

FPM, Span 2  
![](images/4fb9c174f0fd44306dd85ea8cf8451337d5e925dd0a8dc73572cdf2f1e310f19.jpg)  
(e)  
Figure 11. RD profile comparison–Span 2 (all techniques). (a) Zeroing, (b) MTI-IM, (c) IMAT, (d) WD, and (e) FPM.

• Figure 11 (Span 2, all techniques): at two interfered chirps, performance remains close across methods. Minor deviations appear (e.g. light smoothing or residual ripple), but overall SNIR differences are limited. The proposed FPM matches the best visual quality while staying competitive in runtime.

• Figure 12 (Span 6, all techniques): under heavy interference, FPM clearly outperforms the baselines. Zeroing and MTI–IM show target suppression/smearing (hard blanking and subtraction do not scale across multiple chirps); IMAT reduces interference but introduces structured artifacts; WD smooths the map but lowers point-target contrast. FPM preserves target sharpness and background texture and maintains higher SNIR.

• Figure 13 (FPM, spans 1–6): RD quality with FPM is consistent as the span increases, with no visible distortion of static or moving targets. This indicates robustness of FPM to increasing interference span.

Table 4 summarizes the SNIR performance (in dB) of five IM techniques Zeroing, MTI-IM, IMAT, WD, and FPM across interference spans ranging from 1 to 6 chirps.

From table 4, it can be observed that MTI-IM achieves the highest SNIR for span 1 (37.13 dB), slightly outperforming FPM and IMAT. However, starting from span 2 onwards, FPM maintains stable performance around 36 dB, consistently outperforming Zeroing, MTI-IM, and WD. IMAT performs competitively and remains close to FPM across all spans, while WD exhibits the lowest SNIR values due to its strong denoising effect, which can smooth out signal peaks. This demonstrates that the proposed FPM approach provides robust performance, especially for longer interference spans (⩾ 2 chirps).

## 5.5. Computational cost comparison

To evaluate the real-time feasibility of the proposed method, the median execution times of various IM techniques were measured over multiple bursts. Table 5 summarizes the median time (in milliseconds) required by each technique.

Zeroing, Span 6  
![](images/05fe409dc686082c0998c663a0a8d6cc4ac2245e1d1275e9d234cf2f00e9f406.jpg)  
(a)

MTI-IM, Span 6  
![](images/977cf47035f92f7dbb854cf39928b2293b959a46b0d4fdc954a4981f873d3bcd.jpg)  
(b)

IMAT, Span 6  
![](images/cd065a4af5a61a2c14d3192b7037b7edb997ebef5986ad8aa08efae8d829e125.jpg)  
(c)

WD, Span 6  
![](images/366c843adda7ab262049d586197c325b308d9b52a2acb7643e06c343fe264188.jpg)  
(d)

FPM, Span 6  
![](images/50caf9065667dbf2eb7aaf287d48a41acfb75bb5ef95f536a2b303b5bf510f53.jpg)  
(e)  
Figure 12. RD profile comparison–Span 6 (all techniques). (a) Zeroing, (b) MTI-IM, (c) IMAT, (d) WD, and (e) FPM.

From table 5, it is observed that:

• Zeroing is the fastest method, with a median time of 3.6 ms, due to its simple zero-substitution approach.

• MTI-IM is slightly slower (4.5 ms) but provides better interference suppression.

• WD and MTI-IMAT are significantly slower (15.1 ms and 18.3 ms, respectively) because of their multistep and iterative computations.

• The proposed FPM method achieves 7.3 ms, which is faster than WD and MTI-IMAT while offering better RD profile quality.

In summary, the proposed method strikes a balance between computational cost and IM performance, maintaining sub-10 ms latency suitable for real-time FMCW radar processing.

## 5.6. Summary and key observations

• FPM provides the best trade-off between mitigation performance and speed, maintaining robust RD profile quality and SNIR even in heavy interference (span 3–6), while staying within real-time constraints (<10 ms).

• Conventional methods like Zeroing and MTI-IM excel in simple scenarios (span 1–2) but fail in overlapping interference where their rigid blanking/subtraction leads to target loss.

• IMAT and WD, though sophisticated, show residual artifacts and increased computation time, making them less practical for time-critical automotive radar systems.

• The proposed hybrid approach (windowed blanking + interpolation + fixed KF) effectively reconstructs suppressed chirps and minimizes distortion.

• Overall, FPM represents a robust and scalable solution for next-generation FMCW radar IM.

![](images/a5dbf1a1fb68e5caf24c4bc851675e4f71d4fbceb22d78b9b4a67531edd5cfa6.jpg)

FPM, Span 2  
![](images/cd6959b724cf0f215484aa03806c1f8a7a8cf888fa2c2516ae151af7bb54c4d4.jpg)  
(b)  
(a)

FPM, Span 3  
![](images/2fbf1c06f3bd7ecdfc00913614eb59cc031c3d67346f33953e7dde5eeb4b5a1b.jpg)  
(c)

![](images/5051a1c7804df22c4e0993201a5cbb3676465b2a01cd1ff5ccc04fa8751844bc.jpg)  
(d)

FPM, Span 5  
![](images/0e54bf666e326fce18833c3c00454cbfbeb3465287b0306ed15566dcd84ac4df.jpg)

FPM, Span 6  
![](images/b47a708a55255cb1f7cbeba1e972d6b6b0ed40820633149036d6abff15f11320.jpg)  
(e)  
Figure 13. RD profile comparison–FPM across spans. (a) Span 1, (b) Span 2, (c) Span 3, (d) Span 4, (e) Span 5, and (f) Span 6.

Table 4. SNIR (dB) of five mitigation techniques across overlap spans (chirps).
<table><tr><td>Span</td><td>Zeroing</td><td>MTI-IM</td><td>IMAT</td><td>WD</td><td>FPM</td></tr><tr><td>1</td><td>36.00</td><td>37.13</td><td>36.62</td><td>31.19</td><td>36.50</td></tr><tr><td>2</td><td>36.00</td><td>33.02</td><td>36.82</td><td>31.24</td><td>36.38</td></tr><tr><td>3</td><td>36.00</td><td>33.22</td><td>36.83</td><td>31.08</td><td>36.31</td></tr><tr><td>4</td><td>36.00</td><td>31.95</td><td>36.82</td><td>30.86</td><td>36.28</td></tr><tr><td>5</td><td>32.00</td><td>31.77</td><td>36.81</td><td>30.24</td><td>36.15</td></tr><tr><td>6</td><td>32.00</td><td>31.81</td><td>36.69</td><td>30.10</td><td>36.07</td></tr></table>

Table 5. Median execution time (ms) of different interference mitigation techniques.
<table><tr><td>Technique</td><td>Zeroing</td><td>MTI-IM</td><td>WD</td><td>MTI-IMAT</td><td>FPM</td></tr><tr><td>Median time (ms)</td><td>3.595</td><td>4.490</td><td>15.067</td><td>18.315</td><td>7.321</td></tr></table>

## 6. Conclusion

This paper presented a class-aware IM framework for FMCW radar systems in autonomous driving scenarios. The proposed technique leverages lightweight TinyML-based interference classification and span logic to determine the severity of radar-to-radar interference in real time. Based on the identified class, the system dynamically selects the appropriate mitigation strategy, including MTI-IM for moderate interference and blanking with interpolation + fixed Kalman filter for severe overlap conditions (up to interference span length 6).

Validation was conducted through experimental tests on a real-world FMCW radar dataset. Overlap interference was synthetically injected by copying real interfered chirps into clean bursts to simulate burst-level corruption scenarios. The proposed detection and mitigation pipeline was then applied to these corrupted bursts. Performance was evaluated using metrics such as SNIR improvement, RD-profile recovery, and computational cost.

When compared with conventional methods including Zeroing, MTI-IM, WD, and MTI-IMAT the proposed class-based approach consistently outperformed baseline techniques under severe interference. Notably, it successfully recovered RD profiles and improved SNIR in cases where traditional methods failed. Furthermore, it maintained execution times below 10 ms per burst, confirming its suitability for edge deployment.

Future work includes refining the interpolation scheme for longer interference spans, adaptive parameter, integrating beamforming or waveform control to proactively avoid interference, and evaluating the system under real-time deployment on embedded radar hardware. Overall, the proposed solution demonstrates significant potential for improving robustness, adaptability, and real-world feasibility of radar systems in dense automotive environments.

## Data availability statement

The data that support the findings of this study are openly available at the following URL/DOI: https:// ieee-dataport. org/documents/raw-adc-data-fmcw-radar-77-ghz-interference [56].

## Acknowledgment

The authors gratefully acknowledge Luis López-Valcárcel, Manuel García Sánchez, Francesco Fioranelli, and Oleg Krasnov for releasing the IEEE DataPort dataset ‘Raw ADC data from FMCW radar at 77 GHz with interference,’ which was used in this study and enabled the reproducible evaluation reported here [56].

## Author contributions

Tai-Hsing Lee  0009-0008-9148-0623

Conceptualization (lead), Data curation (equal), Formal analysis (equal), Funding acquisition (lead), Investigation (equal), Methodology (equal), Project administration (equal), Resources (equal), Software (equal), Supervision (equal), Validation (equal), Visualization (equal), Writing – original draft (equal), Writing – review & editing (equal)

Nur Azis Salim  0000-0002-7004-6552

Conceptualization (supporting), Data curation (equal), Formal analysis (equal), Funding acquisition (supporting), Investigation (equal), Methodology (equal), Project administration (equal), Resources (equal), Software (equal), Supervision (equal), Validation (equal), Visualization (equal), Writing – original draft (equal), Writing – review & editing (equal)

## References

[1] Kramer A J and Heckman C 2024 Radar-based localization for autonomous ground vehicles in Suburban neighborhoods IEEE Trans. Field Robot. 1 161–9

[2] Abu-Alrub N J and Rawashdeh N A 2024 Radar odometry for autonomous ground vehicles: a survey of methods and datasets IEEE Trans. Intell. Veh. 9 4275–91

[3] Yunhe S, Jing X, Qingchun H and Meili W 2021 Design and implementation of distance measurement system based on FMCW technology J. Phys.: Conf. Ser. 1820 012039

[4] Uysal F 2020 Phase-coded FMCW automotive radar: system design and interference mitigation IEEE Trans. Veh. Technol. 69 270–81

[5] Chen Q, Ren S, Sun H, Li Z, Liang W, Qiao C and Zhang R 2025 Interference mitigation for FMCW radar based on filtering in fractional Fourier domain IEEE Trans. Aerosp. Electron. Syst. 61 5799–813

[6] Singh R, Saluja D and Kumar S 2022 Spread spectrum coded radar for r2r interference mitigation in autonomous vehicles IEEE Trans. Intell. Transp. Syst. 23 10418–26

[7] Xu Z and Shi Q 2018 Interference mitigation for automotive radar using orthogonal noise waveforms IEEE Geosci. Remote Sens. Lett. 15 137–41

[8] Lee S, Lee J-Y and Kim S-C 2021 Mutual interference suppression using wavelet denoising in automotive FMCW radar systems IEEE Trans. Intell. Transp. Syst. 22 887–97

[9] Jung J, Lim S, Kim J, Kim S-C and Lee S 2020 Interference suppression and signal restoration using kalman filter in automotive radar systems Proc. IEEE Int. Radar Conf. (RADAR) (Washington, DC, USA) pp 726–31

[10] Wang Y, Huang Y, Liu J, Zhang R, Zhang H and Hong W 2024 Interference mitigation for automotive FMCW radar with tensor decomposition IEEE Trans. Intell. Transp. Syst. 25 9204–23

[11] Wang J, Ding M and Yarovoy A 2021 Matrix-pencil approach-based interference mitigation for FMCW radar systems IEEE Trans. Microw. Theory Tech. 69 5099–115

[12] Fuchs A, Rock J, Toth M, Meissner P and Pernkopf F 2025 Multiantenna radar signal interference mitigation using complex-valued convolutional neural networks IEEE Trans. Syst. Man Cybern. 55 1997–2008

[13] Weng Y, Zhang Z, Chen G, Zhang Y, Chen J and Song H 2024 Real-time interference mitigation for reliable target detection with FMCW radar in interference environments Remote Sens. 17 26

[14] Suppiah R, Noori K, Abidi K and Sharma A 2024 Real-time edge computing design for physiological signal analysis and classification Biomed. Phys. Eng. Express 10 045034

[15] Blasone G P, Colone F and Lombardo P 2022 Passive radar concept for automotive applications Proc. IEEE Radar Conf. (RadarConf22) (New York City, NY, USA) pp 1–5

[16] Mazher K U, Heath R W, Gulati K and Li J 2020 Automotive radar interference characterization and reduction by partial coordination Proc. IEEE Radar Conf. (RadarConf20) (Florence, Italy) pp 1–6

[17] Carvajal G K et al 2020 Comparison of automotive FMCW and OFDM radar under interference Proc. IEEE Radar Conf. (RadarConf20) (Florence, Italy) pp 1–6

[18] Aydogdu C, Keskin M F, Garcia N, Wymeersch H and Bliss D W 2021 Radchat: spectrum sharing for automotive radar interference mitigation IEEE Trans. Intell. Transp. Syst. 22 416–29

[19] Dapa K B S A, Point G, Bensator S and Boukour F E 2023 Vehicular communications over OFDM radar sensing in the 77 GHz mmwave band IEEE Access 11 4821–9

[20] Giroto de Oliveira L, Nuss B, Alabd M B, Diewald A, Pauli M and Zwick T 2022 Joint radar-communication systems: modulation schemes and system design IEEE Trans. Microw. Theory Tech. 70 1521–51

[21] Wang J, Ding M and Yarovoy A 2022 Interference mitigation for FMCW radar with sparse and low-rank Hankel matrix decompos ition IEEE Trans. Signal Process. 70 822–34

[22] Muja R, Anghel A, Cacoveanu R and Ciochina S 2024 Real-time interference mitigation in automotive radars using the short-time fourier transform and l-statistics IEEE Trans. Veh. Technol. 73 14617–32

[23] Hakobyan G, Armanious K and Yang B 2020 Interference-aware cognitive radar: a remedy to the automotive interference problem IEEE Trans. Aerosp. Electron. Syst. 56 2326–39

[24] Rock J, Toth M, Messner E, Meissner P and Pernkopf F 2019 Complex signal denoising and interference mitigation for automotive radar using convolutional neural networks Proc. 22nd Int. Conf. on Information Fusion (FUSION) (Ottawa, ON, Canada) pp 1–8

[25] Slavik Z and Mishra K V 2019 Cognitive interference mitigation in automotive radars Proc. IEEE Radar Conf. (RadarConf) (Boston, MA, USA) pp 1–6

[26] Lampel F et al 2020 System level synchronization of phase-coded FMCW automotive radars for RadCom Proc. 14th European Conf. on Antennas and Propagation (EuCAP) (Copenhagen, Denmark) pp 1–5

[27] Overdevest J, Laghezza F, Jansen F and Filippi A 2021 Radar waveform coexistence: interference comparison on multiple-frame basis Proc. 17th European Radar Conf. (EuRAD) (Utrecht, Netherlands) pp 168–71

[28] Ishikawa S, Kurosawa M, Umehira M, Wang X, Takeda S and Kuroda H 2019 Packet-based FMCW radar using CSMA technique to avoid narrowband interefrence Proc. Int. Radar Conf. (RADAR) (Toulon, France) pp 1–5

[29] Kitsukawa Y, Mitsumoto M, Mizutani H, Fukui N and Miyazaki C 2019 An interference suppression method by transmission chirp waveform with random repetition interval in fast-chirp FMCW radar Proc. 16th European Radar Conf. (EuRAD) (Paris, France) pp 165–8

[30] McCormick P M, Sahin C, Blunt S D and Metcalf J G 2019 Fmcw implementation of phase-attached radar-communications (PARC) Proc. IEEE Radar Conf. (RadarConf) pp 1–6

[31] Lv S, Liu S, Shi H and Zhang J 2024 Design of low-correlation sidelobe FSK-PSK waveforms with controllable frequency points J. Phys. : Conf. Ser. 2761 012019

[32] Zhihuo X and Yuan M 2021 An interference mitigation technique for automotive millimeter wave radars in the tunable q-factor wavelet transform domain IEEE Trans. Microw. Theory Tech. 69 5270–83

[33] Kim E H and Kim K H 2018 Random phase code for automotive MIMO radars using combined frequency shift keying-linear FMCW waveform IET Radar Sonar Navig. 12 1090–5

[34] Knill C, Schweizer B, Hügler P and Waldschmidt C 2018 Impact of an automotive chirp-sequence interferer on a wideband OFDM radar 2018 15th European Radar Conf. (EuRAD) (Madrid, Spain) pp 34–37

[35] Hu X, Li Y, Lu M, Wang Y and Yang X 2019 A multi-carrier-frequency random-transmission chirp sequence for TDM MIMO automotive radar IEEE Trans. Veh. Technol. 68 3672–85

[36] Wang J 2022 Cfar-based interference mitigation for FMCW automotive radar systems IEEE Trans. Intell. Transp. Syst. 23 12229–38

[37] López-Valcárcel L A, García Sánchez M, Fioranelli F and Krasnov O A 2024 An MTI-like approach for interference mitigation in FMCW radar systems IEEE Trans. Aerosp. Electron. Syst. 60 1985–2000

[38] Wang P, Yin X, Rodríguez-Piñeiro J, Chen Z, Zhu P and Li G 2023 A dual-recursive-least-squares algorithm for automotive radar interference suppression IEEE Trans. Intell. Transp. Syst. 24 10603–17

[39] Dao X, Gao M, Han Z and Cheng C 2022 Correlation-based local detection for deceptive interference mitigation in multiparameter modulated radar Signal Process. 199 108635

[40] Bechter J, Roos F, Rahman M and Waldschmidt C 2017 Automotive radar interference mitigation using a sparse sampling approach Proc. Eur. Radar Conf. pp 90–93

[41] Yang S, Shang X, Zhang D, Sun Q and Chen Y 2023 Imia: interference mitigation via iterative approaches for automotive radar IEEE Trans. Radar Syst. 1 753–66

[42] Rameez M, Pettersson M I and Dahl M 2022 Interference compression and mitigation for automotive FMCW radar systems IEEE Sens. J. 22 19739–49

[43] Rameez M, Dahl M and Pettersson M I 2021 Autoregressive model-based signal reconstruction for automotive radar interference mitigation IEEE Sens. J. 21 6575–86

[44] Wang J, Li R, Zhang X and He Y 2024 Interference mitigation for automotive FMCW radar based on contrastive learning with dilated convolution IEEE Trans. Intell. Transp. Syst. 25 545–58

[45] Shan H, Fu X, Lv Z, Xu X, Wang X and Zhang Y 2023 Synthetic aperture radar images denoising based on multi-scale attention cascade convolutional neural network Meas. Sci. Technol. 34 08540

[46] Mun J, Ha S and Lee J 2020 Automotive radar signal interference mitigation using RNN with self attention Proc. IEEE Int. Conf. on Acoustics, Speech and Signal Processing (ICASSP) (Barcelona, Spain) pp 3802–6

[47] Fuchs J, Dubey A, Lübke M, Weigel R and Lurz F 2020 Automotive radar interference mitigation using a convolutional autoencoder Proc. IEEE Int. Radar Conf. (RADAR) (Washington, DC, USA) pp 315–20

[48] Chen S, Shangguan W, Taghia J, Kühnau U and Martin R 2020 Automotive radar interference mitigation based on a generative adversarial network Proc. IEEE Asia-Pacific Microwave Conf. (APMC) (Hong Kong) pp 728–30

[49] Ristea N-C, Anghel A and Ionescu R T 2021 Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks IEEE Access 9 153491–507

[50] Correas-Serrano A and Gonzalez-Huici M A 2019 Sparse reconstruction of chirplets for automotive FMCW radar interference mitigation 2019 IEEE MTT-S Int. Conf. on Microwaves for Intelligent Mobility (ICMIM) (Detroit, MI, USA) pp 1–4

[51] Alajlan N N, Alhujaylan A I and Ibrahim D M 2025 PRDTinyML: deep learning-based TinyML-based pedestrian detection model in autonomous vehicles for smart cities Indones. J. Electr. Eng. Comput. Sci. 39 283

[52] Richards M A 2014 The stop-and-hop approximation and phase history Fundamentals of Radar Signal Processing 2 edn (McGraw-Hill) pp 152–5

[53] Richards M A 2014 Constant false alarm rate detection Fundamentals of Radar Signal Processing 2 edn (McGraw-Hill) pp 496–535

[54] Aslam S and Rabie T F 2023 Principal component analysis in image classification: a review Advances in Science and Engineering Technology Int. Conf. (ASET) (Dubai, United Arab Emirates) pp 1–7

[55] Huang J, Zhou J and Zheng L 2020 Support vector machine classification algorithm based on relief-f feature weighting Int. Conf. on Computer Engineering and Application (ICCEA) (Guangzhou, China) pp 547–53

[56] López-Valcárcel L A, García Sánchez M, Fioranelli F and Krasnov O A 2025 Raw ADC data from FMCW radar at 77 GHz with interference IEEE DataPort (available at: https://ieee-dataport. org/documents/raw-adc-data-fmcw-radar-77-ghz-interference)