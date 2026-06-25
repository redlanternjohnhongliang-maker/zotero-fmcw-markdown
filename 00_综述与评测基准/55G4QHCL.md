# Performance Comparison of Mutual Automotive Radar Interference Mitigation Algorithms

Mate Toth<sup>∗#</sup>, Paul Meissner<sup>∗</sup>, Alexander Melzer<sup>∗</sup> and Klaus Witrisal<sup>#</sup>

<sup>∗</sup>Infineon Technologies, Graz, Austria

<sup>#</sup>Graz University of Technology, Graz, Austria

Abstract—The number of cars equipped with radar sensors is steadily increasing. Hence, mutual sensor interference will inevitably occur frequently. Interference results in decreased sensing performance, potentially leading to dangerous traffic situations. For the chirp sequence (CS) radars prevalent in automotive applications, different processing algorithms for interference mitigation have been proposed. However, the performances of these algorithms have not typically been evaluated and compared in a systematic way. In this paper we describe a framework based on the statistical evaluation of performance measures, suitable for a general comparison of mutual radar interference mitigation algorithms. The proposed methodology is then applied to analyze selected algorithms based on radar simulations.

Index Terms—automotive components, sensor systems, millimeter wave radar, radiofrequency interference, radar signal processing.

## I. INTRODUCTION

Radar finds increased application in the automotive sector. Vehicles are equipped with several sensors, to be used in advanced driver assistance systems (ADAS). With the advent of autonomous driving, the number of such sensors on the roads is expected to strongly increase in the future [1]. As a consequence, the mutual interference of automotive radar sensors becomes an important issue. For frequency modulated continuous wave (FMCW)/chirp sequence (CS) radar, the prevalent signaling type for automotive applications, the probability and impact of mutual interference occurrences have been studied in [2]–[4].

In general, interference results in signal distortions causing decreased object detection sensitivity. It can be mitigated using signal processing techniques as e.g. described in [5]– [7]. Several further approaches have been proposed recently. However, the effectiveness of techniques is typically verified on a case-by-case basis with qualitative evaluations. No single framework for their comparative analysis has been brought forth to date, which is the aim of this paper. Metrics suitable for a general analysis of different approaches are described, enabling a meaningful and comprehensive statistical assessment of the interference mitigation performance [8]. We focus on measures that highlight the impact of interference on the application, such as signal to interference and noise ratio (SINR) as well as detection and false alarm probabilities [8].

## II. MUTUAL INTERFERENCE IN CHIRP SEQUENCE RADAR

This section summarizes the conventional signal processing for CS radar and introduces the concept of mutual interference.

![](images/a27e2c5c85b60c6764ed0b3c9b84dd708c6c61e54b5bcd549d728c7cb99ec497.jpg)  
Fig. 1. Basic CS radar signal processing chain. The dashed box indicates parts of the chain where interference mitigation processing can be implemented. In general, time domain methods may be a part of preprocessing the IF signal $\bar { s } _ { \mathrm { I F } } ^ { [ m ] } [ n ]$ , while frequency domain methods process the range spectra $S _ { \mathrm { R } } ^ { [ m ] } [ n ]$

## A. Review of Signal and Interference Model

In FMCW radar, the radio frequency (RF) transmit signal is a linearly frequency modulated carrier, also termed ramp. Transmit and received signals are mixed and filtered, yielding the so-called intermediate frequency (IF) signal. An object at a certain distance leads to a sinusoid of a corresponding frequency in the IF signal. Hence, distances can be measured by extracting the spectral peaks of the IF signal. In order to also measure velocities, a CS radar transmits a rapid sequence of ramps, and evaluates the phase differences between the respective resulting IF signals.

These processing steps can be implemented by arranging the received samples in a matrix form and computing fast Fourier transforms (FFTs) subsequently along the two dimensions (also termed fast- and slow-time, respectively). The resulting two-dimensional spectrum is the so-called range-Doppler (RD) map, which shows peaks located at certain distance and velocity indices corresponding to objects. Exact descriptions and derivations of this processing can be found in [9], [10].

Fig. 1 presents a block diagram of conventional RD processing and introduces the terms and signal notation used throughout this paper. After digitization, the received IF signal consists of the signals from M ramps, containing N samples each. These will constitute the dimensions of the RD matrix, as represented by the generic sample indices m and n, regardless of domain. An optional preprocessing step follows, which might include a time domain interference mitigation technique. The two subsequent FFTs result in the RD map $S _ { \mathrm { R D } } ^ { [ m ] } [ n ]$ containing peaks at the indices corresponding to objects. These peaks are then detected by some object detector, generally implemented as a type of constant false alarm rate (CFAR) algorithm [11].

Naturally, in addition to object reflections, any signal which is inside the IF bandwidth at the ADC input during the time of measurement will be processed. Along with the inherent receiver noise, interference signals may be observed. We therefore model the basic receive IF signal as

$$
s _ { \mathrm { I F } } ^ { [ m ] } [ n ] = \sum _ { o = 1 } ^ { N _ { \mathrm { O } } } s _ { \mathrm { O } , o } ^ { [ m ] } [ n ] + \sum _ { i = 1 } ^ { N _ { \mathrm { i n t } } } s _ { \mathrm { i n t } , i } ^ { [ m ] } [ n ] + \nu ^ { [ m ] } [ n ] ,\tag{1}
$$

where $s _ { \mathrm { O } , o } ^ { [ m ] } [ n ]$ is the signal component from the o-th out of $N _ { \mathrm { O } }$ object reflections, $s _ { \mathrm { i n t } , i } ^ { [ m ] } [ n ]$ is the signal component from the i-th out of $N _ { \mathrm { i n t } }$ interferers, and $\nu ^ { [ m ] } [ n ]$ is a receiver noise term (generally AWGN).

The mutual interference of CS radars can lead to different effects [2]. So-called non-coherent interference occurs when the signaling parameters of victim and interferer are different. Their respective RF transmit ramps then “cross” in the timefrequency plane at the receiver of the victim sensor. This causes time-limited bursts in the receive IF signal, which in RD processing manifest themselves as broadband distortions of the resulting spectra. Detailed signal models can be found in [12], [13].

## B. Mitigation Methods Selected for this Analysis

The state of the art mitigation methods chosen for analysis in this work are briefly summarized below.

1) Zeroing of Interfered Samples (zero): Setting the receive IF signal samples that were affected by interference to zero is arguably the simplest, most obvious mitigation method. It has been discussed in e.g. [14], and often serves as a baseline of comparison to other algorithms [7]. An important prerequisite to this method is an initial interference detection step, which might generally be done by (adaptive) thresholding [14].

2) Ramp Filtering (RFmin): The concept of ramp filtering was introduced in [6]. The main idea is to exploit the diversity of the range spectrum $S _ { \mathrm { R } } ^ { [ m ] } [ n ]$ over the ramps m. The ramps are processed by some nonlinear operator in order to smooth the range spectrum.

The choice of nonlinear operator is of course a significant aspect influencing the characteristics and performance of the algorithm. A simple choice is the minimum operator. At range bins where no object is present, this takes the value of smallest interference/noise power. An object reflection, however, should be consistently present over all ramps. Although the behavior is not deterministic, by taking the minimum, the resulting magnitudes should be very small at every point other than the object bins. This suppresses interference and noise considerably.

3) Iterative Method with Adaptive Thresholding (IMAT): IMAT was introduced in the context of sparse sampling in [15], revealing a novel interference mitigation approach in [7]. The method is used per ramp m on the fast-time samples n of the signal $s _ { \mathrm { I F } } ^ { [ m ] } [ n ]$ . First, interfered samples are zeroed. This ensures that the spectrum of the signal is sparse, meaning that energy is concentrated around a relatively small number of components. The zeroed time-domain “gap” is then interpolated by iteratively finding said dominant spectral components and replacing the gap by their inverse Fourier transform.

The extraction of dominant components is done by thresholding, starting with taking only the maximum spectral peak, and then lowering the threshold at every iteration by $\Delta _ { \mathrm { s t e p } } \mathrm { d B }$ This step size, together with the maximum number of iterations $\eta _ { \mathrm { m a x } }$ , are the parameters of the algorithm. In [7], a way to determine appropriate values for the parameters is given.

4) Time Domain Parametric Interpolation (IVMip): Interpolation methods have been mentioned as early as 1997 [16]. Similar to zeroing, they are based on the detection of interfered samples. However, these samples are then replaced (gaps are interpolated) with the intent of reconstructing the clean object signal. This can be done through the use of a parametric signal model estimated from the remaining non-interfered data.

A linear prediction problem can be considered,

$$
\hat { s } _ { \mathrm { I F } } ^ { [ m ] } [ n ] = \sum _ { l = 1 } ^ { \eta } a _ { l } s _ { \mathrm { I F } } ^ { ( m ) } [ n - l ] ,\tag{2}
$$

where $\eta$ is the model order and $a _ { l }$ are the prediction coefficients. The crucial point is the choice of the prediction coefficients, which could be calculated using signal modeling knowledge. One of the natural options is an autoregressive (AR) model. However, in this paper, a slightly different approach based on [17] is used.

In [17], it is shown that for a sum of sinusoidals, a unique set of coefficients exists satisfying (2) for $\eta \quad =$ 2×(Number of Sinusoidals). Afterwards, the prediction is written as a system of linear equations for $N _ { \mathrm { e s t } } >$ 2η samples. A least-squares estimate of the coefficients a<sub>l</sub> can then be computed using the instrumental variable method (IVM) [18], with the instrumental variable being simply the input matrix delayed by some value, termed D.

## III. ANALYSIS METHODOLOGY

The interference mitigation methods described in the previous section strongly differ in their approaches and properties. Hence, a simple methodology is needed that is independent of such differences and is able to evaluate mitigation performance based on general radar performance measures. The approach taken in this paper is described below.

## A. Definition of Performance Measures

Since objects in CS radar are detected as peaks in the RD map, there are two fundamental aspects relevant to the sensor’s performance for a single object:

1) Detection probability: This is dependent on the SINR, meaning the magnitude of the object peak compared to the noise floor. Note that the two dimensions of the RD matrix, corresponding to range and velocity, can exhibit different SINR values.

2) Determination of detected object properties: This includes correct magnitude and phase values of the detected peak as well as separability of different object peaks.

Essentially, the goal of interference mitigation processing is to maximize the detection probability while avoiding any distortion possibly skewing the detection results. Therefore, we define the following numerical measures:

• SINR in range dimension, computed as

$$
\mathrm { S I N R _ { r } } = \frac { \sum _ { n \in \mathcal { O } } \left| S _ { \mathrm { R D } } ^ { [ m _ { \mathrm { O } } ] } [ n ] \right| ^ { 2 } / N _ { \mathcal { O } } } { \sum _ { n \notin \mathcal { O } } \left| S _ { \mathrm { R D } } ^ { [ m _ { \mathrm { O } } ] } [ n ] \right| ^ { 2 } / ( N - N _ { \mathcal { O } } ) } .\tag{3}
$$

• SINR in velocity dimension, similarly

$$
\mathrm { S I N R _ { v } } = \frac { \sum _ { m \in \mathcal { O } } \left| S _ { \mathrm { R D } } ^ { [ m ] } [ n _ { \mathrm { O } } ] \right| ^ { 2 } / M _ { \mathcal { O } } } { \sum _ { m \notin \mathcal { O } } \left| S _ { \mathrm { R D } } ^ { [ m ] } [ n _ { \mathrm { O } } ] \right| ^ { 2 } / ( M - M _ { \mathcal { O } } ) } .\tag{4}
$$

• Error vector magnitude (EVM), as measured between the complex values of the object peak in the non-interfered $( S _ { \mathrm { R D , c l e a n } } ^ { [ m _ { \mathrm { O } } ] } [ n _ { O } ] )$ and interference mitigated $( S _ { \mathrm { R D } } ^ { [ m _ { \mathrm { O } } ] } [ n _ { O } ] )$ cases,

$$
\mathrm { E V M } = \frac { \Big | S _ { \mathrm { R D , c l e a n } } ^ { [ m _ { \mathrm { O } } ] } [ n _ { O } ] - S _ { \mathrm { R D } } ^ { [ m _ { \mathrm { O } } ] } [ n _ { O } ] \Big | } { \Big | S _ { \mathrm { R D , c l e a n } } ^ { [ m _ { \mathrm { O } } ] } [ n _ { O } ] \Big | } .\tag{5}
$$

To simplify notation, $\mathcal { O }$ was introduced as the set of object bins, pertaining to both range and velocity. The definition of this set is somewhat arbitrary. Naturally, the actual maximal peak value is $S _ { \mathrm { R D } } ^ { [ m _ { \mathrm { O } } ] } [ n _ { O } ]$ , with $n _ { O }$ and $m _ { \mathrm { O } }$ corresponding to its indices in the RD map. Then, $\mathcal { O }$ can be defined as $( n _ { \mathrm { O } } \pm$ $\Delta _ { \mathrm { r } } , m _ { \mathrm { O } } \pm \Delta _ { \mathrm { v } } )$ to account for the object peak of some width in range $\Delta _ { \mathrm { r } }$ or velocity $\Delta _ { \mathrm { v } } .$ . The total number of range and velocity bins corresponding to the object peak are then $N _ { \mathcal { O } }$ and $M _ { \mathcal { O } }$ , respectively.

General measures of radar sensor performance are the probability of detection $\mathrm { P _ { d } }$ and the probability of false alarm $\mathrm { P _ { f a } }$ These values highly depend on the object detection algorithm that is used. The determination of detection and false alarm probability metrics in this work was done using a single, essentially arbitrarily parameterized cell averaging (CA) CFAR detector [11]. Note that there are many possibilities of detector structure and parameters. An extensive discussion of detectors is out of the scope of this paper.

For the sake of simplicity, a single-object scenario is considered for the comparison carried out in Section IV. In the context of signal processing, different object signals can be generally considered independently due to the linearity of operations. However, an increase in the number of objects, as well as objects with different properties, can have an effect on the performance of some mitigation methods. An investigation of such algorithm-specific cases should always supplement the general performance comparison framework introduced in this paper.

SIMULATED VICTIM RADAR AND SIGNAL PROCESSING PARAMETERS.  
TABLE I
<table><tr><td rowspan=1 colspan=6>Parameter  Description                   Set Value</td></tr><tr><td rowspan=1 colspan=1> $\overline { { f _ { 0 , \mathrm { V } } } }$ </td><td rowspan=1 colspan=5>ramp start frequency           76GHz</td></tr><tr><td rowspan=1 colspan=1> $B _ { \mathrm { V } } ^ { \cdot }$ </td><td rowspan=1 colspan=3>ramp</td><td rowspan=1 colspan=1>np bandwi</td><td rowspan=1 colspan=1>1GHz</td></tr><tr><td rowspan=1 colspan=1> $T _ { \mathrm { V } }$ </td><td rowspan=1 colspan=1>ramp</td><td rowspan=1 colspan=3>duration</td><td rowspan=1 colspan=1>48μs</td></tr><tr><td rowspan=1 colspan=1> $B _ { \mathrm { I F } }$  $N$ </td><td rowspan=1 colspan=5>IF bandwidthnumber of fast-time samples   2048</td></tr><tr><td rowspan=1 colspan=1> $N _ { \mathrm { z p } }$ </td><td rowspan=1 colspan=5>N after zero-padding          4096</td></tr><tr><td rowspan=1 colspan=1> $M$ </td><td rowspan=1 colspan=2>nur</td><td rowspan=1 colspan=3>number of slow-time samples  128</td></tr><tr><td rowspan=1 colspan=1> $M _ { \mathrm { z p } }$ </td><td rowspan=2 colspan=5>M after zero-paddingtype used                    Hann</td></tr><tr><td rowspan=1 colspan=1>window</td></tr></table>

RANGE OF RANDOM INTERFERER AND VICTIM RECEIVER PARAMETERS.  
TABLE II
<table><tr><td>Parameter</td><td>Description</td><td>min.</td><td>max.</td></tr><tr><td> $\overline { { N _ { \mathrm { i n t } } } }$ </td><td>number of interferers</td><td>1</td><td>3</td></tr><tr><td> $f _ { 0 , { \mathrm { I } } }$ </td><td>ramp start frequency</td><td>75.8GHz</td><td>76.2GHz</td></tr><tr><td> $B _ { \mathrm { I } }$ </td><td>ramp bandwidth</td><td>0.6GHz</td><td>1.4GHz</td></tr><tr><td> $T _ { \mathrm { I } }$ </td><td>ramp duration</td><td>40μs</td><td>46μs</td></tr><tr><td> $P _ { \mathrm { I } }$ </td><td>transmit power</td><td>13dB</td><td>33dB</td></tr><tr><td> $P _ { \mathrm { N } }$ </td><td>noise power</td><td>-20dB</td><td>-5dB</td></tr></table>

## B. Simulation Aspects

The relation of simulation parameters such as listed in Tables I and II to the resulting values of the performance measures is not trivial. The connections are too complex to be analyzed individually. Therefore, in order to make general statements about algorithms, Monte Carlo simulations are carried out in this work. The goal is to obtain results over a range of the relevant parameters.

A simulation run consists of a random choice of the number of interferers and their signaling parameters. Most signal parameters of the victim radar are kept fixed for simplicity. All parameters together correspond to a certain sequence of interfered RF transmit ramps, thereby defining the interference bursts in the receive IF signal. Tables I and II list the relevant parameters of the simulated victim radar system and interferers, respectively. Table III lists the parameters of the analyzed mitigation methods.

Fig. 2 depicts the cumulative distribution function (CDF) of the resulting total IF interference power $P _ { \mathrm { i n t } }$ and receiver noise power $P _ { \nu }$ over the simulations, respectively. Note that the power of a signal is computed numerically as its average sample energy in this work. The distribution of $P _ { \nu }$ matches the uniform sampling within the range given in Table II. The values of $P _ { \mathrm { i n t } }$ depend on the number of interferers $N _ { \mathrm { i n t } }$ , their respective RF transmit powers $P _ { \mathrm { I } }$ as well as the number of IF samples affected by interference, yielding the result in the figure.

TABLE III  
CHOICE OF ALGORITHM-SPECIFIC PARAMETERS FOR THE DIFFERENT METHODS.
<table><tr><td>Method</td><td></td></tr><tr><td>RFmin IMAT IVMip</td><td>filter operation: minimum over all ramps , ηmax computed adaptively as proposed in [7]</td></tr></table>

![](images/979114aa55a65ec393eeaef28c15329cacedcdd92e63d4a07a6b51492898bd63.jpg)  
Fig. 2. CDFs of interference power and receiver noise power. The constant object signal power level is added to the plot as $P _ { \mathrm { O } } = - \mathrm { i } 0 \mathrm { d B }$ as a reference.

![](images/07c1bd2f71958240762db139f1b48221fb8dd3e527ec0d21fee0f544acd67b21.jpg)  
Fig. 3. Percentage of interfered ramps $M _ { \mathrm { i n t } }$ and samples $N _ { \mathrm { i n t } }$ resulting over the simulation runs, respectively.

In Fig. 3, it can be seen that the simulation essentially corresponds to a sweep over the cases of none to all ramps being interfered. However, we also observe that the total percentage of interfered samples varies in a relatively small range. This is inherently due to the nature of crossing ramp sequences. While ramps with similar slopes result in an interference burst of longer duration, such ramps also generally cross less often.

The collected values of each output metric are then observed statistically as a distribution. This allows for a simple assessment of average performance and robustness, in terms of mean and spread of the distribution. Mitigation algorithm metrics are compared to each other in this way, while also including the non-mitigated case as a reference.

Important points to consider are the effect of the antialiasing filter (AAF) and the non-ideal detection of interfered samples. First, the idealized case is discussed, with the form of an interference burst as considered in [12] and perfect interference detection. The same results are presented then, when including a 9-th order Butterworth low-pass filter and a basic adaptive thresholding interference detection into the simulation framework.

## IV. SIMULATION RESULTS

Using the previously introduced mitigation methods and analysis framework, a simulation study is carried out. Key results of our comparative performance analysis are presented in the following section.

![](images/cad6ae1a95f91a0b412588e873dccf078f08b4dfb8a7ceb32bc224b02d7b8385.jpg)  
Fig. 4. CDF of $\mathrm { S I N R _ { r } }$ (range dimension) with ideal interference detection.

## A. Gain in SINR due to Mitigation Processing

Figs. 4 and 5 illustrate the noise suppression behavior of the algorithms in range and velocity domains, respectively. The main insights concerning the tested mitigation algorithms are listed below.

• Without mitigation processing (No Mit.), the SINR is simply the consequence of the input powers (see Fig. 2) with the standard RD processing gains as described in [3]. The distribution is very similar for both domains.

• Simple zeroing (zero) guarantees a complete elimination of the interference component, but also eliminates a part of the object signal.

• Parametric interpolation (IVMip) yields very similar performance to zeroing. This means that the estimation of the object frequency with the parameters used as listed in Table III is insufficiently accurate. Since the same false object signal model is used to interpolate over the interference bursts in every ramp, the performance even suffers from a degradation over zeroing in the velocity domain.

• IMAT is significantly more effective than the previously discussed techniques in this context. It is somewhat less robust in velocity than in range domain. This can be explained by the technique replacing bursts of interfered samples as a whole, possibly introducing phase uncertainty at the edges of the replaced burst. An option to alleviate said effect could be to use some method of smoothing at these edges.

• Simple ramp filtering with the minimum operator (RFmin) yields the highest SINR in range domain. It can be observed that in fact the SINR is even higher than in the case of a non-interfered clean object signal containing only receiver noise. This is possible due to the minimum operator naturally setting the noise floor magnitude to the lowest value over the range spectra. As expected, in the velocity domain a significant performance degradation is visible, since the phase remains uncorrected.

In Figs. 6 and 7, the performance degradation due to nonideal interference detection can be observed. In particular, the performance gap between zeroing and IMAT is decreased. The performance of ramp filtering is unaffected.

![](images/004179212a9388d37e1f75bb5c6633da6c46f1aefb69ea9f0a00a844832eb63f.jpg)  
Fig. 5. CDF of $\mathrm { S I N R } _ { \mathrm { v } }$ (velocity dimension) with ideal interference detection.

![](images/7a0dc5c67cf482645b9a31e38625e59239dff7d17ab03cedcbe1a5773fd281c0.jpg)  
Fig. 6. CDF of SINR<sub>r</sub> (range dimension) with non-ideal interference detection.

## B. Detection and False Alarm Probabilities

The values of $P _ { \mathrm { d } }$ and $P _ { \mathrm { f a } }$ are computed using the results from every simulation run for a respective mitigation method. Figs. 8 and 9 are a visualization of the results.

Key points from Fig. 8a include the following.

• Each method leads to a drastic improvement in detection probability. This is intuitive, considering the SINR gains of the methods as seen in the previous section.

• Zeroing, and all methods implicitly based on it, work well because (as seen in Fig. 3) the total number of interfered samples does not exceed around 20%.

A more diverse behavior can be observed from the false alarm probabilities depicted in 8b. The main observations are as follows.

• All methods except ramp filtering decrease $\mathrm { P _ { f a } }$ when compared to the non-mitigated case. The reason is that ramp filtering selects a single sample of the noise floor, and copies it to every ramp before the computation of the second FFT. This means that the noise statistics of the RD map is altered, possibly leading to minor local peaks that can then be detected by a CFAR-type detector. While a relatively strong effect unique to ramp filtering, a slight modification of the algorithm or at the detector could probably solve this issue.

![](images/941d7d2d4e2a7cff59784181baa16756502c8eefa76ae5337a6883c7a2d6fe14.jpg)  
Fig. 7. CDF of SINR<sub>v</sub> (velocity dimension) with non-ideal interference detection.

![](images/23ce473abf92719c1cd482139e69c1a1973795bb4fe4f66e329e54d22f087e74.jpg)  
(a) Detection probabilities.

![](images/fc0d0dd4f9b7f499b88e630e1c5e133ba2f78377f323ac5e88cb5f58fcdbcfe6.jpg)  
(b) False alarm probabilities.

Fig. 8. Illustration of the computed $\mathrm { P _ { d } }$ and $\mathrm { P _ { f a } }$ of the different methods.  
![](images/d039512090b74f94279cea6b9fce994e16448fe789e7d86c4b01355ec6df9f37.jpg)  
(a) Detection probabilities.

![](images/711559893114633afa0b8f82e14f725ac1dd30f55f6340c1aacd11820fc0291a.jpg)  
(b) False alarm probabilities.  
Fig. 9. Illustration of the computed $\mathrm { P _ { d } }$ and $\mathrm { P _ { f a } }$ of the different methods for the non-ideal interference detection case.

• Out of the analyzed methods, IMAT decreases $\mathrm { P _ { f a } }$ the most. This is due to its ability to increase the SINR while avoiding the introduction of artifacts on the RD map.

• Parametric interpolation, as implemented in this work, yields worse results than zeroing. This can be explained by its behavior, as already discussed in Section IV-A.

With imperfect interference detection, analyzed in Fig. 9, we observe a bigger diversity of values for $\mathrm { P _ { d } }$ . The result matches well to that of the SINR values as presented on the previous plots. IMAT leads to a modest improvement over zeroing, while parametric interpolation appears to have no effect, due to reasons discussed before. The effectiveness of ramp filtering, as mentioned, remains unchanged.

## C. Value of the Detected Object peak

The EVM is computed according to (5) at the object sample index for every simulation run. The results are depicted in Fig. 10. The main points of analysis are the following.

• Ramp filtering distorts the object value the most. Such behavior is essentially a direct consequence of the nonlinear approach of this method. Time domain methods in general seem to more easily maintain the original magni tude and initial phase value of the object signal. This is understandable, considering that said methods only alter part of the input samples prior to RD processing.

![](images/74fde01c2ce817e3ff9433231d990b636b7fec6035f496d5a2fd1435f075f9cd.jpg)  
Fig. 10. CDF of EVM with ideal interference detection.

![](images/068ab911c636dec33f2bb7fbfe3ef1279c3362e19cc7b2414bae4f376858633e.jpg)  
Fig. 11. CDF of EVM with non-ideal interference detection.

• Zeroing introduces an error, also related to a loss of resolution [14]. Parametric interpolation does not improve on the performance of zeroing, again reinforcing the result that the estimated object model is in fact not acceptably accurate.

• IMAT yields the best results, since it attempts to reconstruct the original time domain signals without introducing artifacts.

Looking at the imperfect interference detection case in Fig. 11, it can be noted that the advantage of time domain algorithms in repairing the object peak value essentially vanishes. Each method improves on the EVM metric over the non-mitigated case, but none of them seems significantly better than the others.

As mentioned previously, the actual value of the detected peak on the RD map is essential for subsequent signal processing. The magnitude might be used for clustering/classification of objects. More importantly, however, the phase value in particular is used for angle estimation when using several receive channels. For this, the phase difference of the detected peak value over the receive channels is evaluated. Interference mitigation processing would generally be applied on every channel in a multiple input multiple output (MIMO) system, possibly making EVM a crucial measure. Since in this work only single-channel simulations have been presented, such considerations are the subject of further research.

## V. CONCLUSION

This paper presented a comprehensive framework for the comparative analysis of automotive radar interference mitigation algorithms. A simulation methodology was described and a number of general performance measures were defined, suitable for a statistical performance analysis. Then, an exemplary analysis was carried out using a small selection of state of the art algorithms. It could be seen that the proposed framework proves effective in yielding insights about a specific method, while also allowing for a quick comparison of different algorithms. For example, we have shown that ramp filtering performs very well in terms of interference suppression, but strongly alters the RD map and the object peak value in the process, which is not the case for time domain methods. In the future, the analysis framework is to be extended to incorporate aspects such as MIMO processing.

## REFERENCES

[1] M. Kunert, H. Meinel, C. Fischer, and M. Ahrholdt, “Report on interference density increase by market penetration forecast,” the MOSARIM Consortium, Tech. Rep. D16.1, Sep. 2010.

[2] G. M. Brooker, “Mutual Interference of Millimeter-Wave Radar Systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, Feb. 2007.

[3] M. Goppelt, H. L. Blocher, and W. Menzel, “Analytical investigation of¨ mutual interference between automotive FMCW radar sensors,” in 2011 German Microwave Conference, Mar. 2011.

[4] M. Kunert, “The EU project MOSARIM: A general overview of project objectives and conducted work,” in 2012 9th European Radar Conference, Oct. 2012.

[5] J. Bechter, K. D. Biswas, and C. Waldschmidt, “Estimation and cancellation of interferences in automotive radar signals,” in 2017 18th International Radar Symposium (IRS), Jun. 2017.

[6] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-Free Interference Cancellation Method for Automotive FMCW Radar Systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS), May 2018.

[7] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive Radar Interference Mitigation Using a Sparse Sampling Approach,” in 2017 European Radar Conference (EURAD), 2017, pp. 90–93.

[8] M. Toth, “Mutual Interference in Automotive FMCW Radar – Modeling and Mitigation Techniques,” Master’s thesis, Graz University of Technology, Austria, 2018.

[9] A. G. Stove, “Linear FMCW radar techniques,” IEE Proceedings F - Radar and Signal Processing, vol. 139, no. 5, pp. 343–350, Oct. 1992.

[10] V. Winkler, “Range Doppler detection for automotive FMCW radars,” in 2007 European Microwave Conference, Oct. 2007, pp. 1445–1448.

[11] M. Richards, Fundamentals of Radar Signal Processing, ser. Professional Engineering. McGraw-Hill Education, 2005.

[12] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical Investigation of Non-Coherent Mutual FMCW Radar Interference,” in 2018 European Radar Conference (EURAD), Sep. 2018, pp. 71–74.

[13] G. Kim, J. Mun, and J. Lee, “A Peer-to-Peer Interference Analysis for Automotive Chirp Sequence Radars,” IEEE Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8110–8117, Sept 2018.

[14] C. Fischer, “Untersuchungen zum Interferenzverhalten automobiler Radarsensorik,” Ph.D. dissertation, Universitat Ulm, 2016, in German.¨

[15] F. Marvasti, M. Azghani, P. Imani, P. Pakrouh, S. Heydari, A. Golmohammadi, A. Kazerouni, and M. Khalili, “Sparse signal processing using iterative method with adaptive thresholding (IMAT),” in 2012 19th International Conference on Telecommunications (ICT), April 2012.

[16] B. E. Tullsson, “Topics in FMCW radar disturbance suppression,” in Radar 97 (Conf. Publ. No. 449), no. 449, 1997.

[17] Y. Chan, J. Lavoie, and J. Plant, “A Parameter Estimation Approach to Estimation of Frequencies of Sinusoids,” IEEE Trans. Acoust., vol. ASSP-28, no. 2, pp. 214–219, 1981.

[18] W. Greene, Econometric Analysis. Pearson Education, 2003.