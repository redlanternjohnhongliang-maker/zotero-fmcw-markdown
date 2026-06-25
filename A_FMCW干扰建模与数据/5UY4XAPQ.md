# Performance Analysis of Uncoordinated Interference Mitigation for Automotive Radar

Yi Wang , Student Member, IEEE, Qixun Zhang , Member, IEEE, Zhiqing Wei , Member, IEEE, Liping Kui , Fan Liu , Member, IEEE, and Zhiyong Feng , Senior Member, IEEE

Abstract—As a key sensor for Advanced Driving Assistance System (ADAS), millimeter automotive radar has been a promising candidate for fulfilling tasks including adaptive cruise control and collision avoidance. However, the widely deployment of millimeter automotive radars may cause serious mutual interference among vehicles, thus degrading radar ranging performance severely. In this article, we analyze the mutual interference among multiple Frequency Modulated Continuous Wave (FMCW) radars. On one hand, we model the interference precisely by employing Matern Hard-Core Process (MHCP) model to characterize the distribution of vehicle nodes in practical bidirectional two-lane and multi-lane scenarios. Besides, the interference is analyzed in terms of the channel fading, the directional antenna pattern and the fluctuation of the target Radar Cross-Section (RCS) in two-lane and multi-lane scenarios. Besides, we analyze the reflected interference in detail. On the other hand, we evaluate the interference mitigation performance of the Random Frequency Division Multiplexing (RFDM) and Frequency Hopping (FH) approaches in terms of the probability of false detection and miss detection, effective detectable density and maximum number of interference-free radar. Finally, a novel AFH-PM mitigation approach is proposed to further improve the interference mitigation performance, which combines the adaptive FH technology with the binary phase modulation. Simulation results verify the proposed framework for interference analysis by employing Monte Carlo method, and the performance improvement of RFDM, FH and AFH-PM is 6.7 dB, 7.6 dB and 8.2 dB, respectively.

Index Terms—Automotive radars, mutual interference, FMCW, interference mitigation, frequency hopping.

## I. INTRODUCTION

M <sup>ILLIMETER</sup> <sup>Wave</sup> <sup>automotive</sup> <sup>radars</sup> <sup>have</sup> <sup>been</sup> <sup>widely</sup>deployed to support Advanced Driver Assistance System deployed to support Advanced Driver Assistance System (ADAS) (e.g., Adaptive Cruise Control (ACC), Forward Collision Warning (FCW), Blind Spot Detection (BSD), Parking Assistance (PA) and Lane Change Assistance (LCA)) owing to its excellent performance in high resolution, weak sensitivity to bad environment conditions and low cost [1], [2], [3]. However, densely deployment of automotive radars leads to serious radar mutual interference when operating in the same frequency within their respective coverage, which may cause degraded detection performance due to miss detection or false detection of the targets [4], [5]. Therefore, to promote the development of autonomous driving and guarantee the road safety, it’s essential to analyze the mutual interference and evaluate the radar ranging performance.

The interference experienced by victim radar is classified into two categories, i.e., narrow band interference and wide band interference [6], [7]. If the interfering radars employ an identical chirp slope with victim radar, narrow band interference occurs when ghost targets are created which leads to false detection of real targets [8], [9]. If the interfering radars employ different chirp slopes with victim radar, wide band interference occurs when the noise floor is increased and the probability of target detection is decreased which leads to miss detection of real targets [10], [11]. Though both types of interference are harmful to radar detection, we focus on the narrow band interference which is a challenging problem to deal with. In this article, we assume all radars have the same parameters (chirp slope, chirp duration, bandwidth, number of chirps per frame, duty cycle, etc) where ghost targets will be the dominant effect [4], [12], [13], [14], [15].

To mitigate the serious radar mutual interference, accurate interference modeling and efficient interference mitigation approaches are essential. The accurate interference analysis model is crucial to quantitatively evaluate the mutual interference performance among multiple radars. Existing research works on the modeling of radar mutual interference are summarized as follows, which can be divided into three main categories. 1) Simple two-node interference model. Brooker et al. investigated the probability of interference occurs for different types of radars under different weather conditions with frequency-related overlaps [16]. Besides, the mutual interference between automotive Chirp Sequence (CS) radars has been studied in [17]. Further, Schipper et al. provided a ray-tracing simulation predictor to obtain the qualitative and quantitative received power levels for interference signals [18]. However, the above works mainly focus on simple two-node topologies while the realistic interference problems need to be further investigated. 2) General two-lane interference model. Al-Hourani et al. adopted the stochastic geometry method to analyze the mutual interference, where a Poisson Point Process (PPP) and a regular lattice are employed to model the vehicle locations [12]. Munari et al. also derived compact closed-form expressions using stochastic geometry method for the radar detection performance to characterize the effect of mutual interference under different path-loss exponents [19]. 3) Complex multi-lane interference model. To analyze the interference accurately, Chu et al. and Wang et al. considered the interference on front- and side- mounted radars with directional antennas [13], [20]. However, they ignore the fact that the two types of radars do not share the same frequency band. Besides, Kui et al. proposed a blockage model to analyze the mutual interference in partially and completely blocking conditions [21], but the characteristic of Radar Cross-Section (RCS) of the targets is considered as a constant without modeling its fluctuation in practical scenarios. Fang et al. analyzed the mutual interference under two RCS models (i.e., Swerling I and Chi-square model) [14]. However, the conventional PPP distribution assumes the vehicle nodes are independently distributed which contradicts the fact that the two vehicle nodes are not allowed to be too close to each other. Matern Hard-Core Process (MHCP) is a suitable model to analyze the mutual interference which considers the length of vehicle [22], [23]. Additionally, most existing works still employed a PPP distribution model. Therefore, it’s essential to consider the radar mutual interference in a realistic environment.

Then it is necessary to conduct a comprehensive study of interference mitigation to avoid catastrophe in future intelligent transportation systems after given an accurate depiction of the interference model. The three years project - MOre Safety for All by Radar Interference Mitigation (MOSRIM) - is the first project to investigate the interference mechanism of automotive radars and access to some existing mitigation technologies [24]. Then a broad range of signal processing techniques in the timedomain, frequency-domain, and space-domain were proposed to mitigate the mutual interference [15], [25], [26], [27], [28], [29], [30]. Adopting such methods would require automotive radar coordination, which means that each radar sensor should share information with other radars, such as time synchronization and control messages [15], [25]. However, most existing radar systems employ uncoordinated transmissions owing to the absence of centralized control, which gives a challenge to orthogonal scheduling of different radar systems [3]. To resolve this issue, uncoordinated interference mitigation approaches may show good performance in the non-cooperative scenarios. Random frequency division multiplexing is the simplest uncoordinated approach to deal with narrow band interference, where each radar selects one of the multiple sub-bands to transmit randomly and independently [31]. Frequency hopping is a typical uncoordinated approach, which has the characteristic of distinguishing ghosts from targets [32], [33]. A random frequency hopping procedure can be implemented at the transmitter side to prevent the interference between multiple radars by altering the frequency randomly and rapidly once the interference occurs and is detected [34]. However, the performance improvement of these non-cooperative technologies is not yet known and remains to be explored.

In this article, we investigate the interference modeling and uncoordinated interference mitigation aspects of automotive Frequency Modulated Continuous Wave (FMCW) radars that mounted on intelligent vehicles for adaptive cruise control function operating at 76–77 GHz. We provide an analysis of the level of mutual interference quantitatively. Moreover, we evaluate two uncoordinated approaches to show the performance of interference mitigation based on the proposed interference model. Finally, we propose a novel AFH-PM mitigation approach based on the analyzes we conducted. The main contributions of this article are summarized as follows.

We propose an analytic framework to characterize the mutual interference experienced by FMCW radars in both two-lane and multi-lane scenarios, by considering the MHCP model, the channel fading, the directional antenna pattern and RCS fluctuation characteristic. The mutual interference are analyzed in terms of the direct incident interference and reflected interference. Besides, we evaluate the radar performance by using the successful ranging probability.

The closed-form solutions of the direct incident interference and reflected interference among radars are achieved theoretically in this paper. In addition, an in-depth analysis of the occurrence conditions of mutual interference is proposed to calculate the probability of interference.

We evaluate the performance improvement of two uncoordinated approaches (random frequency division multiplexing and frequency hopping) on interference mitigation and give closed-form expressions in terms of the probability of false detection and miss detection, effective detectable density, and maximum number of interference-free radar.

We propose a novel AFH-PM mitigation approach which combines the adaptive FH technology with the binary phase modulation to further improve the interference mitigation performance. AFH-PM can not only adjust the frequency hopping rate adaptively to reduce the probability of interference, but also spread a ghost target in Doppler by random binary phase modulation.

The rest of this article is laid out as follows. Section II presents the system model of FMCW radar network. Section III provides an analytic framework of mutual interference in both two-lane and multi-lane scenarios. Section IV illustrates a detailed analysis of the probability of interference. Section V describes the two uncoordinated mitigation approaches in detail. Networking performance of uncoordinated mitigation approaches are investigated and results are provided in Section VI. Finally, Section VII concludes this article.

## II. SYSTEM MODEL

## A. Scenario

As shown in Fig. 1, let us consider a multi-lane bi-direction road scenario in which the geometric distribution of vehicles is emulated by stochastic geometry methods. There are <sup>m</sup> and <sup>n</sup> lanes in the same and opposite directions, respectively. Assume that the victim vehicle is located at the origin of one lane while the radars mounted on the vehicles employ the FMCW modulation chirp. The target stays in the same lane as the victim vehicle and every nearby vehicle within the victim vehicle’s Field of View (FoV) can be detected accurately if it isn’t an interferer. The victim vehicle suffers from the direct incident interference when the operating time and frequency band of more than two automotive radars overlaps, which is generated among close-by radars driving in the opposite direction. Besides, the reflected interference from the one-time reflection of signals sent by potential transmitters with the same driving direction affect the radar ranging performance, too.

![](images/73f5dae1dd3c709e375427c12454b7f61f6d6cdecf891897afc989baeccb3943.jpg)  
Fig. 1. The direct incident interference and reflected interference among automotive radars.

The geometry distribution of each vehicle is modeled as a homogeneous one-dimensional Matern Hard-Core Process (1-D MHCP). We assume that the length of the vehicle is $l _ { v }$ and safety distance of two neighboring is $d _ { v }$ . Therefore, the hardcore distance is $d _ { h } = l _ { v } + d _ { v }$ . Concretely, the distance between two neighboring nodes should exceed $d _ { h }$ . We first generate a Poisson Point Process (PPP) distribution model with the same density ${ \bf \rho } _ { \rho }$ of each line. Generally, the PPP model is regarded as a parent point process to obtain an MHCP model and the density of MHCP is written as

$$
\rho _ { h } = \frac { 1 - \exp ( - 2 \rho d _ { h } ) } { 2 d _ { h } } .\tag{1}
$$

Assume that the probability of the vehicles in the opposing direction using the same frequency with the victim vehicle is $\varepsilon ,$ which makes a thinned MHCP effective interferers with density $\lambda _ { h } = \varepsilon \rho _ { h }$ on each lane. In this article, we focus on the direct incident interference caused by the overlapping field-of-view between the oncoming interfering automotive radars and the victim automotive radar.

## B. Basics of FMCW Radar

The automotive radars operating at 76–77 GHz are considered to add additional comfort functions for the driver, giving support for more stress-free driving, which requires long range ranging and high resolution capability. According to the ITU standard and application report of Texas Instruments (TI) [35], [36], the FMCW radar is an appropriate waveform, which transmits periodic chirps whose frequency increases linearly in time, as shown in Fig. 2. The transmit waveform of an FMCW radar with <sup>K</sup> consecutive linear frequency modulated chirps can be represented as [2]

![](images/75efd5c4b46df4fb632b3c6c6f2d9c1464ec51c9982a4a615ea6f522e2523656.jpg)  
Fig. 2. A spectrogram of an FMCW waveform with K consecutive linear frequency modulated chirps.

$$
s ( t ) = \sum _ { k = 0 } ^ { K - 1 } x ( t - k T ) ,\tag{2}
$$

where an individual chirp is given by

$$
x ( t ) = e ^ { j \varphi ( t ) } \mathrm { r e c t } _ { T } ( t ) , \varphi ( t ) = 2 \pi \left( f _ { c } t + 0 . 5 \alpha t ^ { 2 } \right) .\tag{3}
$$

Here, $\mathrm { r e c t } _ { T } ( t )$ denotes square pulse of duration T with an amplitude of 1, $f _ { c }$ denotes the carrier frequency, $\alpha = B _ { r } / T$ denotes the chirp slope, $B _ { r }$ denotes the chirp bandwidth and $T$ denotes the chirp duration. $T _ { R }$ and $T _ { 0 }$ denote the reset time and chirp repetition time, respectively.

Generally, the victim radar may receive two types of signals after transmitting the chirp signal. One is the radar echo signal which is reflected by the target for detection. The other is the interfering signals which come from other radars employing the same frequency with victim radar. Besides, The interfering signals are either caused by direct incident signals from vehicles driving the opposite direction with the victim vehicle, or caused by reflected signals from the same driving direction.

The power of received echo signal is denoted as

$$
P _ { e c h } = \frac { P _ { t } G _ { t } } { 4 \pi R ^ { \alpha } } \times \frac { \sigma } { 4 \pi R ^ { \alpha } } \times \frac { G _ { r } \lambda ^ { 2 } } { 4 \pi } ,\tag{4}
$$

where $P _ { t }$ denotes the transmitted power of radar, <sup>R</sup> denotes the distance between the target and victim radar, <sup>α</sup> denotes the path-loss exponent, $\sigma$ is the RCS of the target, $G _ { t } , \ G _ { r }$ are the transmitted and received antenna gain, respectively, and $\lambda = c / f _ { c }$ is the wavelength of radar. In this article, we employ the inverse square law for interference analysis, $\mathrm { i } . \mathrm { e } . , \alpha = 2$ . For clarity, we assume that $G _ { t } = G _ { r } = G _ { 0 }$ and $G _ { 0 }$ is the maximum antenna gain.

The power of direct incident interfering signals in <sup>j</sup>-th lane is denoted as

$$
I _ { i f , j } = \frac { P _ { t } G ( \beta _ { x _ { j } , y _ { j } } ) } { 4 \pi } \cdot \frac { \lambda ^ { 2 } G ( \beta _ { x _ { j } , y _ { j } } ) } { 4 \pi } h \| r _ { x _ { j } , y _ { j } } \| ^ { - 2 } ,\tag{5}
$$

where <sup>h</sup> denotes the channel fading gain, $G ( \beta _ { x _ { j } , y _ { j } } )$ denotes the directional antenna gain with incoming direction $\beta _ { x _ { j } , y _ { j } } =$ arctan $( x _ { j } / y _ { j } ) , x _ { j }$ and $y _ { j }$ denotes the vertical distance and the horizontal distance between the victim and interfering radars in the <sup>j</sup>-th lane, respectively. $r _ { x _ { j } , y _ { j } } = \sqrt { x _ { j } ^ { 2 } + y _ { j } ^ { 2 } }$ denotes the distance between the interfering and victim radar. The aggregated direct incident interference of victim radar is represented as

![](images/b8c5849d504dc2198378936a23088d7577b93a9a8db391b65564061364c110ba.jpg)  
Fig. 3. The radar transmits a chirp (blue solid line), then receives a radar echo (orange solid line) with a Doppler shift f<sub>D</sub> and an interfering chirp (red dotted line). The received chirps arrive inside the green band, which corresponds to the cutoff bandwidth. After 2D DFT, a target (orange) and a ghost (red) are presented at one of the range-velocity bins.

$$
I _ { i f } = \sum _ { j = 1 } ^ { n } I _ { i f , j } .\tag{6}
$$

The power of reflected interfering signals in <sup>i</sup>-th lane is denoted as

$$
I _ { r f , i } = \frac { P _ { t } G ( \beta _ { x _ { i } , y _ { i } } ) G ( \beta _ { x _ { i } , y _ { i } } ) \lambda ^ { 2 } \overline { { \sigma } } } { ( 4 \pi ) ^ { 3 } r _ { x _ { t } , x _ { r } } ^ { 2 } } h \Vert r _ { x _ { i } , y _ { i } } \Vert ^ { - 2 } ,\tag{7}
$$

where <sup>σ</sup> denotes the average mean value of RCS and $r _ { x _ { t } , x _ { \tau } }$ denotes the distance between the reflected vehicle and its transmitter.

After receiving the signal, a common approach for rangevelocity estimation in FMCW radar is to compute the 2D Discrete Fourier Transform (DFT) of the signal. As shown in Fig. 3, 2D <sup>N</sup>-by-<sup>L</sup> range-velocity bins are formulated to determine the target’s position and state of motion. The maximum detection range $d _ { \operatorname* { m a x } } = c B _ { \operatorname* { m a x } } / 2 \alpha$ is proportional to the cutoff frequency $B _ { \mathrm { m a x } }$ of low pass filter, where <sup>c</sup> is the speed of light and <sup>α</sup> is the slope of chirp. The chirp bandwidth $B _ { r }$ is directly linked to the range resolution $d _ { r e s } = c / 2 B _ { r } ,$ which can partition the detection range into $N = d _ { \operatorname* { m a x } } / d _ { r e s }$ range bins. The corresponding maximum detectable relative velocity is $v _ { \operatorname* { m a x } } = c / 4 f _ { c } T _ { 0 }$ , while the chirp repetition time $T _ { 0 }$ influences the velocity resolution $v _ { r e s } = c / 2 f _ { c } T _ { c }$ [28], [37]. $T _ { c } = L T _ { 0 }$ is the Coherent Processing Interval (CPI) in which the velocity of the target remains nearly constant. This partitions the relative velocity into $L = v _ { \operatorname* { m a x } } / v _ { r e s }$ velocity bins. Therefore, higher chirp bandwidth leads to better range resolution, while a longer CPI duration means improved velocity resolution.

## III. INTERFERENCE ANALYSIS

In this section, we first derive the direct incident interference in two-lane scenario to obtain how these parameters affect the performance of radar detection in terms of the channel fading, the directional antenna pattern and RCS fluctuation characteristic. Then we extend the direct incident interference analysis to the multi-lane scenario. Besides, we analyze the reflected interference from the vehicles driving in the same direction with the victim vehicle. Finally, we evaluate the radar performance by using the successful ranging probability.

## A. Direct Incident Interference

1) Two-Lane Scenario: In this part, we consider the direct incident interference from the oncoming vehicles driving in opposite direction to the victim vehicle in two-lane scenario. As described in the Campbell theorem [40], the mean value of incident interference can be written as

$$
\begin{array} { l } { { \displaystyle \overline { { I _ { i f } } } = E \left[ I _ { i f } \right] } } \\ { { \displaystyle \stackrel { \left( 1 \right) } { = } E _ { h } \left\{ \frac { \lambda _ { h } P _ { t } \lambda ^ { 2 } } { \left( 4 \pi \right) ^ { 2 } } \int _ { \frac { D } { \tan { \frac { \theta } { 2 } } } } ^ { + \infty } \left[ G \left( \arcsin \frac { D } { r _ { x , y } } \right) \right] ^ { 2 } \left\| r _ { x , y } \right\| ^ { - 2 } d r \right\} } . } \end{array}\tag{8}
$$

The step (1) follows the assumption that the distribution of propagation channel is independently identically distribution (i.i.d), which is independent of the distribution of radar location. Besides, $r _ { x , y } ^ { 2 } = x ^ { 2 } + D ^ { 2 }$ with <sup>x</sup> denotes the horizontal distance between the victim and interfering radars and <sup>D</sup> denotes the lane spacing. The lower bound $\frac { D } { \tan { \frac { \theta } { \gamma } } }$ corresponds to the minimum horizontal detection distance which is related to the antenna beamwidth <sup>θ</sup>.

Channel Fading: In this part, we focus on the direct incident interference which come from line of sight (LOS) transmissions. For the channel fading case, we consider two typical types of fading environment, i.e., Rician fading and Nakagami fading cases [21], [41], [42], [43], [44]. A Rician fading channel is sufficient to model the LOS fading case, whose Probability Density Function (PDF) is given by

$$
p ( r ) = \frac { r } { \sigma ^ { 2 } } \exp \left( - \frac { r ^ { 2 } + A _ { 1 } ^ { 2 } } { 2 \sigma ^ { 2 } } \right) \cdot I _ { 0 } \left( \frac { r A _ { 1 } } { \sigma ^ { 2 } } \right) ,\tag{9}
$$

where $A _ { 1 }$ denotes the amplitude of the LOS transmission signal, $\sigma ^ { 2 }$ denotes the power of multi-path components and $I _ { 0 } ( x )$ denotes the zero-order modified Bessel function of the first kind.

The Nakagami model provides a generalized description of fading, whose PDF is given by

$$
p \left( r ; m , \Omega \right) = \frac { 2 } { \Gamma ( m ) } { \left( \frac { m } { \Omega } \right) } ^ { m } r ^ { 2 m - 1 } \exp \left( - \frac { m } { \Omega } r ^ { 2 } \right) ,\tag{10}
$$

where <sup>m</sup> denotes the Nakagami fading index that determines the severity of fading, Ω denotes the second moment of the distribution and $\textstyle \Gamma ( x ) = \int _ { 0 } ^ { + \infty } t ^ { x - 1 } e ^ { - t } d t$ denotes the gamma function. As a general channel fading model, Nakagami fading can also be transformed into a variety of fading models by changing the value of <sup>m</sup>.

Directional Antenna Pattern: Here, we select a widely used directional antenna model to analyze the direct incident interference which is denoted as Gaussian directional radiation pattern [45]. The reasons why selecting the Gaussian function to analyze the interference are: (1) It can derive a compact and closed-form interference expression. (2) The result of derivation is closest to actual directional antenna gain [13], [21], [45]. The directional antenna gain is represented as

$$
G ( \beta _ { x , y } ) = \{ { G } _ { 0 } \exp \{ { - 4 \ln 2 \Big ( \frac { \beta _ { x , y } } { \beta _ { 3 d B } } \Big ) ^ { 2 } } \} , \beta _ { x , y } \in [ 0 , \beta _ { m } / 2 ]\tag{11}
$$

where $\beta _ { 3 d B } , \beta _ { m }$ are the Half Power BeamWidth (HPBW) and main lobe beamwidth, respectively. $\begin{array} { r } { G _ { 0 } = 1 0 \ln { ( \frac { 1 . 6 1 6 2 } { \sin ( \beta _ { 3 d B } / 2 ) } ) ^ { 2 } } } \end{array}$ denotes the maximum antenna gain. $G _ { s }$ denotes the side lobe gain which is represented as $G _ { s } = - 0 . 4 4 1 \cdot \ln ( \beta _ { 3 d B } ) -$ 10<sup>.</sup>597. Compared with the main lobe gain, the gain of side lobe is so small that we ignore it. Therefore, we only consider the effects of main lobe on the mutual interference model in this article.

For the directional antenna model, the mean incident interference can be obtained after applying (1) and (10) to (7), i.e.,

$$
\begin{array} { l } { \displaystyle \overline { { I _ { i f } } } = E _ { h } \cdot \frac { \lambda _ { h } P _ { t } \lambda ^ { 2 } } { \left( 4 \pi \right) ^ { 2 } } \cdot \int _ { \frac { D } { \tan \frac { \theta } { 2 } } } ^ { + \infty } [ G \left( \beta _ { x , y } \right) ] ^ { 2 } \left. r _ { x , y } \right. ^ { - 2 } d r } \\ { = \lambda _ { h } E _ { h } A \int _ { 0 } ^ { \frac { \theta } { 2 } } \exp \left[ - a \beta _ { x , y } { } ^ { 2 } \right] d \beta _ { x , y } } \\ { = \lambda _ { h } E _ { h } A \frac { \sqrt { \pi } } { 2 D } \cdot \frac { 1 } { \sqrt { a } } e r f \left( \frac { \theta } { 2 } \sqrt { a } \right) . } \end{array}\tag{12}
$$

For simplicity, $\begin{array} { r } { A = \frac { P _ { t } G _ { 0 } ^ { 2 } \lambda ^ { 2 } } { \left( 4 \pi \right) ^ { 2 } } } \end{array}$ denotes the constant, $a =$ 8 ln $2 / { ( \beta _ { 3 } d B ) } ^ { 2 }$ denotes the constant factor of antenna gain. Besides, $e r f ( x )$ is the Gaussian error function with $e r f ( x ) =$ $\textstyle { \frac { 2 } { \sqrt { \pi } } } \int _ { 0 } ^ { x } e ^ { - u ^ { 2 } } d u$

2) Multi-Lane Scenario: We extend the direct incident interference analysis to multi-lane scenario where there are <sup>m</sup> and <sup>n</sup> lanes in the same and opposite directions, respectively. The geometry distribution of vehicles in different lanes follows 1-D MHCP with the same density $\rho _ { h }$

Owing to the distribution of radar is independently identical distribution in each lane, the mean mutual interference received by the victim radar can be written as

$$
\begin{array} { c } { E \left[ I _ { i f , N } \right] = E \left[ I _ { i f , 1 } + \cdot \cdot \cdot + I _ { i f , n } \right] } \\ { = E \left[ I _ { i f , 1 } \right] + \cdot \cdot \cdot + E \left[ I _ { i f , n } \right] , } \end{array}\tag{13}
$$

where

$$
E [ I _ { i f , j } ] = \frac { E _ { h } \lambda _ { h , j } P _ { t } G _ { 0 } ^ { 2 } \lambda ^ { 2 } } { \left( m - i + j \right) D \left( 4 \pi \right) ^ { 2 } } \int _ { 0 } ^ { \frac { \theta } { 2 } } \exp { \left[ - a \beta _ { x _ { j } , y _ { j } } { } ^ { 2 } \right] } d \beta _ { x _ { j } , y _ { j } } .\tag{14}
$$

$\lambda _ { h , j }$ denotes the density of MHCP nodes in the <sup>j</sup>-th lane which is assumed that each line has the same density, i.e., $\lambda _ { h , j } = \lambda _ { h }$ The vertical distance between the victim radar and the interfering radar of <sup>j</sup>-th lane is $y _ { v j } = ( m - i + j ) D$ while the minimum horizontal detection of <sup>j</sup>-th lane is $\frac { y _ { v j } } { \tan ( \frac { \theta } { \rangle } ) }$ . The aggregated direct incident interference considering all lanes is given as

$$
E \left[ I _ { i f } \right] = E [ I _ { i f , N } ] = \sum _ { j = 1 } ^ { n } { \frac { \lambda _ { h } E _ { h } A } { ( m - i + j ) D } } \cdot { \frac { \sqrt { \pi } } { 2 { \sqrt { a } } } } e r f \left( { \frac { \theta { \sqrt { a } } } { 2 } } \right) .\tag{15}
$$

## B. Reflected Interference

Typically, when two vehicles are driving in the same traffic direction, a significant part of the reflections from reflected interferer in the front will impose interference on the victim vehicle. As shown in Fig. 1, the reflected interferer can be located ahead of the victim vehicle arbitrarily. We assume that there is only one such potential transmitter existed in a certain moment on each lane. The mean value of the aggregated reflected interference is computed as

$$
\begin{array} { l } { { \displaystyle { E \left[ I _ { r f } \right] = E \left[ \sum _ { i = 1 } ^ { m - 1 } \frac { A \overline { { \sigma } } [ G \left( \beta _ { x _ { i } , y _ { i } } \right) ] ^ { 2 } } { 4 \pi r _ { x _ { t } , x _ { r } } ^ { 2 } } h \| r _ { x _ { i } , y _ { i } } \| ^ { - 2 } \right] } } } \\ { { \displaystyle { = \sum _ { i = 1 } ^ { m - 1 } E _ { h } \frac { \lambda _ { h } A \overline { { \sigma } } } { 8 \pi \left( m - i \right) D r _ { x _ { t } , x _ { r } } ^ { 2 } } \cdot \frac { \sqrt { \pi } } { \sqrt { a } } e r f \left( \frac { \theta \sqrt { a } } { 2 } \right) } } } \end{array}\tag{16}
$$

Consequently, according to the convergence of Harmonic progression and the distance limitation $\begin{array} { r } { r _ { x _ { t } , x _ { r } } \leq \frac { D } { \tan ( \frac { \theta } { 2 } ) } } \end{array}$ , the upper band of (16) is written as

$$
\begin{array} { l } { \displaystyle { E [ I _ { r f } ] \leq \sum _ { i = 1 } ^ { m - 1 } E _ { h } \frac { \lambda _ { h } A \overline { { \sigma } } \tan ^ { 2 } ( \frac { \theta } { 2 } ) } { 8 \pi ( m - i ) D ^ { 3 } } \cdot \frac { \sqrt { \pi } } { \sqrt { a } } e r f ( \frac { \theta \sqrt { a } } { 2 } ) } } \\ { \displaystyle { \qquad \leq E _ { h } \frac { \lambda _ { h } A \overline { { \sigma } } \tan ^ { 2 } ( \frac { \theta } { 2 } ) } { 8 \pi D ^ { 3 } } \cdot \frac { \sqrt { \pi } } { \sqrt { a } } e r f ( \frac { \theta \sqrt { a } } { 2 } ) [ 1 + \ln m ) ] } . } \end{array}\tag{17}
$$

## C. Radar Performance Evaluation

The radar suffers from severe mutual interference as analysed above, which may degrade the probability of successful detection causing serious traffic accidents. Then we evaluate the radar performance by using the Successful Ranging Probability (SRP) with RCS, which is defined as the probability of successful ranging once the received Signal-to-Interference-plus-Noise Ratio (SINR) exceeds the predefined threshold under different

RCS characteristics. It can be represented as

$$
P _ { s } ( \delta ) = P [ S I N R > \delta ] = P \left[ \frac { P _ { e c h } } { \overline { { I _ { i f } } } + \overline { { I _ { r f } } } + N _ { 0 } } > \delta \right] ,\tag{18}
$$

where $N _ { 0 } = k _ { B } T _ { 0 } B _ { 0 } F _ { 0 }$ denotes the the power of additive white Gaussian noise where $k _ { B }$ denotes the Boltzmann’s constant, $T _ { 0 } = 2 9 0 K$ denotes the standard temperature, $B _ { 0 } = 2 5 k H z$ denotes the equivalent noise bandwidth and $F _ { 0 } = 1 5 d B$ denotes the system loss factor [35]. <sup>δ</sup> is the threshold for target detection according to the requirements of detection.

Combining (4) and (18), the SRP can be written as

$$
P _ { s } ( \delta ) = \mathrm { P r } \left\{ \sigma \geq \frac { \delta ( 4 \pi ) ^ { 3 } R ^ { 4 } } { P _ { t } G _ { 0 } ^ { 2 } \lambda ^ { 2 } } \left( \overline { { I _ { i f } } } + \overline { { I _ { r f } } } + N _ { 0 } \right) \right\} .\tag{19}
$$

For clarity, we set $\begin{array} { r } { \widetilde A = \frac { 4 \pi R ^ { 4 } } { A } } \end{array}$ . Therefore, (19) is written as

$$
P _ { s } ( \delta ) = \mathrm { P r } \left\{ \sigma \geq \delta \widetilde { A } \left( \overline { { I _ { i f } } } + \overline { { I _ { r f } } } + N _ { 0 } \right) \right\} .\tag{20}
$$

Radar Cross Section (RCS) is the measure of a target’s ability to reflect radar signals in the direction of radar receiver, which shows the radar performance of precision. It’s not a fixed constant but fluctuates from one scan to the next, thus causing the radar echoes fluctuating independently. Swerling I and Chi-square models are two typical RCS models to characterize the fluctuation of targets, which is proved effective to capture the fluctuations through measured data with automotive FMCW radar [14], [38], [39]. In this article, we employ two statistical models, i.e., Swerling I model and Chi-square model, to evaluate the fluctuation.

1) Swerling I Model: Swerling I model is a typical slow fluctuating model where the received echoes are perfectly correlated during any one scan, but are uncorrelated between scans. The PDF of target’s RCS model is represented as

$$
p ( \sigma ) = \frac { 1 } { \overline { { \sigma } } } e ^ { - \frac { \sigma } { \overline { { \sigma } } } } , \sigma \geq 0 ,\tag{21}
$$

where $\overline { { \sigma } } = E [ \sigma ]$ denotes the mean value of target’s RCS. The Cumulative Distribution Function (CDF) of Swerling I model is $F ( s ) = 1 - e ^ { - { \frac { s } { \overline { { \sigma } } } } }$ . Applying the CDF of Swerling I model (21) into (20) and combining (15) and (17), we can obtain

$$
P _ { s } ^ { 1 } ( \delta ) = \exp \left[ - \frac { \delta \widetilde { A } } { \overline { { \sigma } } } \left( N _ { 0 } + \overline { { I _ { i f } } } + \overline { { I _ { r f } } } \right) \right] .\tag{22}
$$

2) Chi-Square Model: Chi-square model is more adaptive than Swerling I model in realistic environment. The PDF of target’s RCS model is represented as

$$
p ( \sigma ) = \frac { k ^ { k } } { \Gamma ( k ) \overline { { { \sigma } } } ^ { k } } \sigma ^ { k - 1 } \exp \left( - \frac { k } { \overline { { { \sigma } } } } \sigma \right) , \sigma \geq 0 ,\tag{23}
$$

where $\Gamma ( k )$ denotes the gamma function, <sup>k</sup> is the value of the double degrees of freedom (i.e., the higher its value, the flatter the fluctuation) and 2 <sup>k</sup> denotes the degree of freedom of Chi-square distribution. When $k = 1$ , it transmits into Swerling I model.

The CDF of Chi-square model is $\begin{array} { r } { F ( s ) = 1 - \frac { \Gamma ( k , \frac { k } { \sigma } s ) } { \Gamma ( k ) } . ~ \mathrm { A p } \mathrm { - } } \end{array}$ plying the CDF of Chi-square Model into (20) and combining (15) and (17), we can obtain

$$
P _ { s } ^ { 2 } ( \delta ) = E _ { I } \left[ \frac { \Gamma \left( k , \frac { k } { \sigma } \delta \widetilde { A } ( \overline { { I _ { i f } } } + \overline { { I _ { r f } } } + N _ { 0 } ) \right) } { \Gamma ( k ) } \right]
$$

$$
= \frac { \Gamma \left( k , \frac { k } { \sigma } \delta \widetilde { A } ( E \left[ I _ { i f } \right] + E \left[ I _ { r f } \right] + N _ { 0 } ) \right) } { \Gamma ( k ) } .\tag{24}
$$

## IV. PROBABILITY OF INTERFERENCE

After qualifying the level of mutual interference, we compute the occurrence probability of mutual interference in this section. For simplicity, we set all FMCW waveform parameters (chirp slope, chirp duration, bandwidth, number of chirps per frame, duty cycle, etc.) equivalent for all radars. We assume that the starting times of different FMCW chirps are random and uniformly distributed for all vehicles. As shown in Fig. 1, the victim vehicle transmits FMCW chirp at <sup>t</sup> and receives the echo signal at $t _ { e c } \in [ 0 , T _ { \operatorname* { m a x } } ] . T _ { \operatorname* { m a x } } = 2 d _ { \operatorname* { m a x } } / c = T B _ { \operatorname* { m a x } } / B _ { r }$ is the maximum delay of radar echo, which is proportional to the maximum detection range $d _ { \mathrm { m a x } }$ . The interfering vehicle in the opposite direction of victim vehicle transmits its signal with the same frequency resulting in mutual interference when at least one chirp of the victim radar is affected not just appear within the maximum interference range. The probability of mutual interference $P _ { i f }$ is defined as the probability that if the frequency of received echo lies in the band $f _ { c } + B _ { r } t / T +$ $[ - B _ { \mathrm { m a x } } , 0 ]$ . This is determined by two conditions:

1) Frequency condition: At chirp cycle <sup>z</sup>, an interference occurs if two radars transmit their signals with the same frequency band. $F _ { m , n } ^ { z }$ denotes the condition that radar <sup>m</sup> and radar <sup>n</sup> are using the same frequency at chirp cycle <sup>z</sup>.

2) Time condition: Assume the victim radar starts to transmit an FMCW chirp at time $t = 0$ and a facing vehicle starts at time $t = \tau$ with overlapping field-of-view. In a chirp duration, the susceptible time period $T _ { s u }$ is defined as the set of <sup>τ</sup> values, at which the interference occurs. $T _ { m , n } ^ { s }$ denotes that radar <sup>m</sup> falls into the susceptible time period of radar $n \mathrm { { : } }$ <sup>s</sup>-th range bin.

As analyzed above, the probability $P _ { i f }$ is equal to the proportion of the susceptible time period to the frame time. Then we compute the susceptible time period to quality the occurrence probability of mutual interference. Assume the transmission of interfering vehicle is received by victim vehicle at time $t _ { i f } ,$ which is the same as a chirp reception at time $t _ { i f } - \tau _ { D }$ without considering Doppler shift. $\tau _ { D }$ is the estimated Doppler time delay and is computed as follows.

$$
\begin{array} { r l } & { \tau _ { D } = T f _ { D } / B _ { r } = T v f _ { c } / \left( B _ { r } c \right) } \\ & { \qquad \subset \ \left[ - T \left| v _ { \operatorname* { m a x } } \right| f _ { c } / \left( B _ { r } c \right) , + T \left| v _ { \operatorname* { m a x } } \right| f _ { c } / \left( B _ { r } c \right) \right] } \\ & { \qquad \approx \left[ - 1 / \left( 4 B _ { r } \right) , + 1 / \left( 4 B _ { r } \right) \right] . } \end{array}\tag{25}
$$

where $f _ { D }$ is the Doppler shift.

As described in Section II, the maximum detectable velocity is $v _ { \operatorname* { m a x } } = c / 4 f _ { c } T _ { 0 }$ . The radar mutual interference occurs when $t _ { i f } - \tau _ { D } \in [ 0 , T _ { \operatorname* { m a x } } ]$ . After considering all possible interference distances, the susceptible time period is represented as

$$
T _ { s u } = \left[ - T _ { \operatorname* { m a x } } - 1 / \left( 4 B _ { r } \right) , T _ { \operatorname* { m a x } } + 1 / \left( 4 B _ { r } \right) \right] .\tag{26}
$$

In practice, the term $1 / ( 4 B _ { r } )$ can be ignored for the fact that $B _ { r } \gg 1 / T _ { \operatorname* { m a x } } .$ So the susceptible time period is roughly $T _ { s u }$ ≈ $[ - T _ { \mathrm { m a x } } , T _ { \mathrm { m a x } } ]$

![](images/3711dbba3d0962add1c617b8563264a416bc87a0d5355c7ce4bae2c1770dd0ba.jpg)  
Fig. 4. RFDM approach for radars where the transmission time of each radar are random and independent.

An FMCW signal contains <sup>K</sup> successive chirps and the mutual interference occurs if at least one of the chirps overlaps in the susceptible time period of other radar chirps. Therefore, the interference may be introduced from the $( K - 1 ) T$ prior up to the end of transmission. The susceptible time period in a whole radar frame is written as

$$
T _ { s u } ^ { f } = \bigcup _ { n = - K - 1 } ^ { K - 1 } [ n T - T _ { \operatorname* { m a x } } , n T + T _ { \operatorname* { m a x } } ] .\tag{27}
$$

The susceptible time duration is $| T _ { s u } ^ { f } | = 2 ( 2 K - 1 ) T _ { \operatorname* { m a x } }$ ≈ $4 K T _ { \mathrm { m a x } }$ since $K \gg 1$

The probability of mutual interference $P _ { i f }$ between two vehicles is represented as

$$
P _ { i f } = \frac { \left| T _ { s u } ^ { f } \right| } { T _ { f } } = \frac { 2 ( 2 K - 1 ) U B _ { \mathrm { m a x } } } { K B _ { r } } \approx \frac { 4 U B _ { \mathrm { m a x } } } { B _ { r } } ,\tag{28}
$$

where $U = K T / T _ { f } \in ( 0 , 1 ]$ denotes the duty cycle of radar.

When considering all possible interferers, the probability of mutual interference is $P _ { i f } ^ { N _ { i f } } = 1 - ( 1 - P _ { i f } ) ^ { N _ { i f } } . \mathrm { ~ } E [ N _ { i f } ] =$ $n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f }$ denotes the average number of interfering vehicles within interference range and $d _ { \operatorname* { m a x } } ^ { i f }$ denotes the maximum interference range. Owing to $N _ { i f }$ can be approximated as poisson distribution, the average probability of interference is then given by

$$
\overline { { P _ { i f } } } \approx 1 - \exp \left[ - n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f } \frac { 4 U B _ { \operatorname* { m a x } } } { B _ { r } } \right] .\tag{29}
$$

## V. PERFORMANCE EVALUATION OF UNCOORDINATED MITIGATION APPROACHES

Facing such serious mutual interference problems, one feasible solution is to employ the simplest uncoordinated mitigation approach - Random Frequency Division Multiplexing (RFDM) [31]. As shown in Fig. 4, this approach has a characteristic that the transmission time for each radar is random and independent without requiring any time synchronization and control overhead. The RFDM shows poor performance for a lack of the ability to distinguish between ghosts and targets. To further improve the performance of mitigating interference, a random Frequency Hopping (FH) procedure is implemented to suppress the peak power of mutual interference, whose carrier frequency jumps in a predetermined order over a wide band range [33], [34]. As shown in Fig. 5, even the interference occurs, the radar jumps to other working sub-bands rapidly to prevent the interference between multiple radars, which shows good anti-interference ability. Therefore, the targets are detected in the same range bin over a CPI while the ghost targets are detected in different range bins randomly when applying frequency hopping. As shown in Fig. 6, assume the radars select the same sub-band when starting transmission, then they hop on <sup>M</sup> sub-bands without coordination. The target always appears in the same distance while the ghosts appear randomly. Taking advantage of such a characteristic that the random appearance of ghosts, ghosts can be distinguished from targets easily, thus reducing the probability of false alarm. Finally, we propose a novel AFH-PM mitigation approach when considering the feature of the interference.

![](images/245a899392df8d8298beee8c0dbe6a35992145a1c5f75ebb1924ad5d2b194b59.jpg)  
Fig. 5. FH approach for radars where the carrier frequency of each radar jumps in a predetermined order over a wide band range.

![](images/d5529f298813c4d48c4087e6abe29089d27d94c5ec9bda48065d0de1dfcec31a.jpg)  
Fig. 6. Ghosts are distinguished from target due to random appearance.

## A. RDFM and FH Mitigation Approaches

In this section, we evaluate the two uncoordinated approaches in terms of the probability of false detection and miss detection, effective detectable density, and maximum number of interference-free radar according to the analytical methods employed in [34].

1) Probability of False Detection: Note that interference has a factor $d ^ { - 2 }$ while the useful echo signal has a factor $d ^ { - 4 }$ the interference may have larger power than the useful echo signal, which may cause false detection or miss detection. The false detection event $E _ { f d , m , n } ^ { i }$ occurs when the peak power of interference from radar <sup>m</sup> is detected by radar <sup>n</sup>, but the target doesn’t exist in the range bin <sup>i</sup>. The false detection event occurs when the time and frequency conditions are satisfied, which causes a ghost target and a high power interference side lobe. That is, $E _ { f d , m , n } = F _ { m , n } ^ { z } \bigcap { \bigl ( } \bigcup _ { s = 1 } ^ { N } T _ { m , n } ^ { s } { \bigr ) }$

Under RFDM, owing to the selection of sub-bands is random and dependent, the probability of frequency condition occurs is computed as $\begin{array} { r } { P [ \mathcal { F } _ { m , n } ^ { z } ] = \frac { 1 } { M } } \end{array}$ . The probability of time condition occurs is computed as $\begin{array} { r } { P [ \tilde { \bigcup } _ { s = 1 } ^ { N } T _ { m , n } ^ { s } ] = P _ { i f } = \frac { 4 U B _ { \operatorname* { m a x } } } { B _ { r } } } \end{array}$ . Thus,

$$
P \left[ E _ { f d , m , n } \right] = P \left[ F _ { m , n } ^ { z } , \bigcup _ { s = 1 } ^ { N } T _ { m , n } ^ { s } \right] = { \frac { 4 U B _ { \operatorname* { m a x } } } { M B _ { r } } } .\tag{30}
$$

Considering all possible interferers, the average number of radars within radar <sup>n</sup>’s interference range is $E [ N _ { i f } ] =$ $n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f } .$ . Thus,

$$
P \left[ E _ { f d } \right] = 1 - \left( 1 - \frac { 4 U B _ { \mathrm { { m a x } } } } { M B _ { r } } \right) ^ { N _ { i f } } .\tag{31}
$$

The average probability of false detection is then given by

$$
\overline { { P \left[ E _ { f d } \right] } } \approx 1 - \exp \left( - n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f } \frac { 4 U B _ { \operatorname* { m a x } } } { M B _ { r } } \right) .\tag{32}
$$

Under FH, a target and a ghost can be distinguished easily with the characteristic of random appearance of ghosts when they fall into different range bins. We denote $H _ { m , n } ^ { s }$ the event that at least one target falls into the same <sup>s</sup>-th range bin with a ghost caused by radar <sup>m</sup>. Thus, $\begin{array} { r } { E _ { f d , m , n } = \bigcup _ { s = 1 } ^ { N } \bar { ( T _ { m , n } ^ { s } \bigcap H _ { m , n } ^ { s } ) } } \end{array}$

With the random and independent appearance of targets, the probability of $H _ { m , n } ^ { s }$ is computed as $P [ H _ { m , n } ^ { s } ] = 1 -$ $( 1 - \frac { 1 } { N } ) ^ { N _ { t } } . \ : N _ { t }$ is defined as the number of targets. Thus,

$$
\begin{array} { l } { { \displaystyle { \cal P } \left[ E _ { f d , m , n } \right] = { \cal P } \left[ \bigcup _ { s = 1 } ^ { N } \left( T _ { m , n } ^ { s } \bigcap H _ { m , n } ^ { s } \right) \right] } } \\ { { \displaystyle ~ = \frac { 4 U B _ { \operatorname* { m a x } } } { B _ { r } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] . } } \end{array}\tag{33}
$$

Considering all possible interferers, the probability of false detection event happens is computed as

$$
P \left[ E _ { f d , n } \right] = 1 - \left( 1 - \frac { 4 U B _ { \mathrm { m a x } } } { B _ { r } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] \right) ^ { N _ { i f } } .\tag{34}
$$

The average probability of false detection is then given by

$$
\overline { { P [ E _ { f d } ] } } \approx 1 - \exp \left( - n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f } \frac { 4 U B _ { \operatorname* { m a x } } } { B _ { r } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] \right) .\tag{35}
$$

2) Probability of Miss Detection: The miss detection event $E _ { m d , m , n } ^ { s }$ occurs when the peak power of interference from radar <sup>m</sup> is large enough to make a target undetected by radar <sup>n</sup> at range bin <sup>s</sup>. We denote $D _ { m , n } ^ { s }$ the event that the distance between radar <sup>m</sup> and radar <sup>n</sup> is smaller than the threshold of a dependent range bin $d _ { s }$ . Then the miss detection event can be represented as $E _ { m d , m , n } ^ { s } = F _ { m , n } ^ { z } \bigcap T _ { m , n } ^ { s } \bigcap D _ { m , n } ^ { s } .$

Under RFDM, as radar topology is homogeneous, the probability of $D _ { m , n } ^ { s }$ is computed as $\begin{array} { r } { P [ D _ { m , n } ^ { s } ] = \frac { - d _ { s } } { d _ { \mathrm { m a x } } ^ { i f } } } \end{array}$ . Thus,

$$
P \left[ E _ { m d , m , n } ^ { s } \right] = P \left[ F _ { m , n } ^ { z } , T _ { m , n } ^ { s } , D _ { m , n } ^ { s } \right] = \frac { 4 U d _ { s } B _ { \mathrm { m a x } } } { M N B _ { r } d _ { \mathrm { m a x } } } .\tag{36}
$$

Considering all possible interferers, the probability of miss detection is computed as

$$
P \left[ E _ { m d , n } ^ { s } \right] = 1 - \left( 1 - \frac { 4 U d _ { s } B _ { \operatorname* { m a x } } } { M N B _ { r } d _ { \operatorname* { m a x } } } \right) ^ { N _ { i f } } .\tag{37}
$$

The average probability of miss detection is then given by

$$
\overline { { P \left[ E _ { m d } ^ { s } \right] } } \approx 1 - \exp \left( - \frac { 4 n U \lambda _ { h } d _ { s } B _ { \mathrm { m a x } } } { M N B _ { r } } \right) .\tag{38}
$$

Under FH, owing to the random appearance of high power ghost, the target may be miss detected with high probability. Then the miss detection event can be represented as $E _ { m d , m , n } ^ { s } =$ $T _ { m , n } ^ { z } \bigcap D _ { m , n } ^ { s } \bigcap H _ { m , n } ^ { s }$ <sup>.</sup> Thus,

$$
\begin{array} { r l r } {  { P [ E _ { m d , m , n } ^ { s } ] = P [ T _ { m , n } ^ { z } \bigcap D _ { m , n } ^ { s } \bigcap H _ { m , n } ^ { s } ] } } \\ & { } & { = \frac { 4 U d _ { s } B _ { \operatorname* { m a x } } } { N B _ { r } d _ { \operatorname* { m a x } } } [ 1 - ( 1 - \frac { 1 } { N } ) ^ { N _ { t } } ] . } \end{array}\tag{39}
$$

Considering all possible interferers, the probability of miss detection event happens is computed as

$$
P \left[ E _ { m d , n } ^ { s } \right] = 1 - \left( 1 - \frac { 4 U d _ { s } B _ { \operatorname* { m a x } } } { N B _ { r } d _ { \operatorname* { m a x } } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] \right) ^ { N _ { i f } } .\tag{40}
$$

The average probability of miss detection is then given by

$$
\overline { { P \left[ E _ { m d } ^ { s } \right] } } \approx 1 - \exp \left( - \frac { 4 n U \lambda _ { h } d _ { s } B _ { \operatorname* { m a x } } } { N B _ { r } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] \right) .\tag{41}
$$

By hopping into different available sub-bands, FH approach can readily distinguish ghosts and targets than the RFDM approach. Compared with RFDM, FH reduces the probabilities of false detection event and miss detection event with a moderate number of detected targets.

3) Effective Detectable Density. Definition 1 (Effective Detectable Density): The victim radar can detect targets accurately if the false detection or miss detection event is not occurs. For simplicity, we assume all victim radars have same probability of false detection and miss detection. Thus, the effective detectable density for victim radar is defined as

$$
C = n \rho _ { h } \left( 1 - P \left[ E _ { f d } \right] - P \left[ E _ { m d } ^ { s } \right] \right) .\tag{42}
$$

Under RFDM, after combining (32), (38) and (42), the effective detectable density is computed as

$$
\begin{array} { r } { C _ { R F D M } = n \rho _ { h } \left[ \exp { \left( - n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f } \frac { 4 U B _ { \operatorname* { m a x } } } { M B _ { r } } \right) } \right. } \\ { \left. + \exp { \left( - \frac { 4 n U \lambda _ { h } d _ { s } B _ { \operatorname* { m a x } } } { M N B _ { r } } \right) } - 1 \right] . } \end{array}\tag{43}
$$

Under FH, after combining (35), (41) and (42), the effective detectable density is computed as

$$
\begin{array} { r } { C _ { F H } = n \rho _ { h } \left\{ \exp { \left( - n \lambda _ { h } d _ { \operatorname* { m a x } } ^ { i f } \frac { 4 U B _ { \operatorname* { m a x } } } { B _ { r } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] \right) } \right. } \\ { \left. + \exp { \left( - \frac { 4 n U \lambda _ { h } d _ { s } B _ { \operatorname* { m a x } } } { N B _ { r } } \left[ 1 - \left( 1 - \frac { 1 } { N } \right) ^ { N _ { t } } \right] \right) } - 1 \right\} . } \end{array}\tag{44}
$$

4) Maximum Number of Interference-Free Radar: Facing FMCW radars are able to operate in an interference-free manner if they are assigned non-overlapping susceptible time periods or non-overlapping sub-bands, which depend on the mitigation approaches. The two approaches - RFDM and FH - are uncoordinated which operate without any time synchronization and cooperation. Thus, the maximum number of radars $M _ { \mathrm { m a x } } ^ { r }$ with no interference is limited by the number of available sub-bands <sup>M</sup> , i.e.,

$$
M _ { \mathrm { m a x } } ^ { r } = M .\tag{45}
$$

## B. Proposed AFH-PM Mitigation Approach

According to the above analysis about the RFDM and FH uncoordinated mitigation approaches, though they have made great contribution on interference mitigation, we think that the performance of uncoordinated interference mitigation can be further improved when considering the feature of the interference. The Doppler shift is the apparent change in frequency due to the relative motion between the victim radar and target object, which is widely used in measuring the relative velocity of target. In fact, the LOS interference signal may have larger power than the useful echo signal while the Doppler shift may be larger as well. Besides, the interferers can be weakened after the doppler processing, whose energy are spread across doppler dimension by random binary phase modulation [46]. Thus, we propose a novel uncoordinated mitigation approach which combines the Adaptive FH technology with the binary Phase Modulation (AFH-PM).

At the receiver, the phase rotation is removed after compensating each chirp with the corresponding binary phase. By employing the binary phase modulation across transmitted chirps in a radar frame (i.e., each chirp is added by a random binary phase rotation 0 or <sup>π</sup>), the proposed AFH-PM approach not only prevents the detection of the ghost, but also reduces the noise floor after the doppler processing with the assumption that the phase modulation scheme between the victim and interferer is different. Besides, the adaptive FH technology is employed to further reduce the probability of interference, where the frequency hopping rate can be adjusted adaptively. Once the interference level increases, the frequency hopping rate can be accelerated to deal with and vice versa. The AFH-PM approach can achieve better performance than RFDM and FH for it fill in the gaps of both.

TABLE I SIMULATION PARAMETERS
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Transmit power (Pt) [35]</td><td>10 dBm</td></tr><tr><td>Carrier frequency (fc) [35]</td><td>76.5 GHz</td></tr><tr><td>Chirp bandwidth (Br) [35]</td><td>1 GHz</td></tr><tr><td>Maximum antenna gain (G0) [45]</td><td> $\left( \frac { 1 . 6 1 6 2 } { \sin \left( \beta _ { 3 d B } / 2 \right) } \right) ^ { 2 }$  10 ln</td></tr><tr><td>Radar cutoff frequency  $( B _ { \mathrm { m a x } } )$  [35]</td><td>50 MHz</td></tr><tr><td>Average radar cross-section (σ) [1]</td><td>30 dBsm</td></tr><tr><td>Spectrum collision probability (ε) [12]</td><td>0.1</td></tr><tr><td>Antenna beamwidth (θ) [35]</td><td>15°</td></tr><tr><td>Lane Spacing (D) [47]</td><td>3.6 m</td></tr><tr><td>Speed of light (c)</td><td>3 × 108 m/s</td></tr><tr><td>Chirp duration (T) [36]</td><td>20 µs</td></tr><tr><td>Duty cycle (U) [36]</td><td>0.67</td></tr><tr><td>Number of chirps in a CPI (L) [36]</td><td>200</td></tr><tr><td>Number of sub-bands (M) [33]</td><td>10</td></tr></table>

## VI. SIMULATION RESULTS

In this section, we conduct a simulation to verify the analytical results derived in this article and evaluate the performance of two uncoordinated mitigation approaches. We consider the vehicles deployed over a 1000 m long straight road with 4 lanes in each driving direction and set the maximum interference range $d _ { \operatorname* { m a x } } ^ { i f } = 1 0 0 0 \operatorname { m }$ . First, the distribution of initial vehicles position is generated by 1D-PPP model of each lane with same density $\rho .$ Then the effective interferer density is $\lambda _ { p } = \varepsilon \rho$ according to the probability of spectrum reusing. The MHCP model is generated from the parent PPP as (1) with $d _ { h } = 1 0 m$ . A total of 10,000 Monte Carlo simulations are conducted to obtain the statistic mean of interference and the successful ranging probability. Besides, we study the effect of RFDM and FH uncoordinated approaches on interference mitigation. For simplicity, a large number of uncoordinated radars are employing the same FMCW waveform parameters in the simulation. Detailed simulation parameters are shown in Table I.

The mutual interference is affected by different factors which are shown in Figs. 7–11. We verify that the Monte Carlo simulations (simu) can match our analytical results (ideal) very well. Fig. 7 shows the mean interference power under PPP and MHCP models in two-lane and multi-lane scenarios. Owing to the hardcore distance, the MHCP model has more sparse vehicle density than PPP model, resulting in less interference power, which is about 0.3 mW and 0.7 mW less than that of the PPP model in two-lane and multi-lane scenarios, respectively. As the vehicle density increases, the mean interference power grows under PPP or MHCP model. Compared with PPP model, the MHCP model is more accurate to analyze automotive radar mutual interference while both match the closed form expression.

![](images/7420e860e2d9e2f136eae201989e787c36ef0b16f28f28a32a33ff2ce3ca9001.jpg)  
Fig. 7. Mean interference power vs. initial vehicle density in PPP and MHCP model.

![](images/b42f2ac2cec0461501e7f574fb263680de5de61121b67c13ebea04088f198098.jpg)  
Fig. 8. The successful ranging probability vs. range in two-lane scenario with two fading channel models.

Fig. 8 describes the successful ranging probability with respect to range in the two-lane scenario with different channel fading cases. The Rician K-factor is defined as the ratio between the power of LOS signal and multi-path components, which is widely used to describe the characteristics of Rician channels. A Rician fading channel with $K = + \infty$ is a Gaussian channel with a strong LOS path where the target can’t be detected once the distance exceeds the maximum detection range. When $K = 0 ,$ , it represents a Rayleigh channel with no LOS path where the successful ranging probability decreased slowly. Besides, the Nakagami fading channel has a greater attenuation degree compared with the Rician channel with <sup>K</sup> = 0 case.

Fig. 9 shows the mean interference power at victim radar considering the directional antenna with Gaussian decaying gain (GauAn) and realistic Uniform Linear Array (ULA) antenna model (Real) in two-lane and multi-lane scenarios. Obviously, with the number of lanes increases, the more density of interfering radars, the more serious the mean interference will be. Besides, the mean interference with GauAn is smaller than the one with the constant antenna gain for it considers the overlapping angle of the interferer-victim beam pair, which indicates that the quantization of interference is more accurately by employing directional antenna gain than a constant one. Compared with constant gain (ConAn) model, the resulting interference power of GauAn model is about 1.1 mW and 2.4 mW less than that in two-lane and multi-lane scenarios, respectively. Fig. 9 also provides the radiation pattern for the ULA and their Gaussian approximations, which is observed that the Gaussian function is an accurate approximation to the radiation pattern of realistic ULA.

![](images/a5a56fbb5b2159a8350671bece4fab16c5ea4d07fa0d8e755033e44429ddea8a.jpg)  
Fig. 9. The mean interference power with constant gain, Gaussian decaying gain and realistic ULA antenna model in two-lane and multi-lane scenarios.

![](images/4b601d151f91329ab334fe10e7c89ac4a3204e9694accef850233ed421f166b5.jpg)  
Fig. 10. The successful ranging probability vs. range, with δ = 5, 10 dB, Swerling I model.

![](images/7543ba188cb568c2bd5ada6a8dd1ce552d259252a437d86bb62379f281a699ec.jpg)  
Fig. 11. The successful ranging probability vs. range, with δ = 5, 10 dB, Chi-square model, k = 2.

Figs. 10 and 11 present the successful ranging probability with respect to range. As analyzed in [13], the target can’t be detected when the distance exceeds the specified value. In Figs. 10 and 11, the target can’t be detected when the distance exceeds 14 m. When taking the fluctuation of RCS into consideration, the successful ranging probability decreased slowly which is more suitable for practical scenarios. In this part, we also consider the effect of both the direct incident interference (IF) and the reflected interference (RF). It’s observed that the direct interference and reflected interference both have bad effect on radar ranging performance while the interference level of RF is about one tenth of that of IF. Compared with Swerling I model, the Chi-square model has a greater attenuation degree and has a more severe impact on the detection performance of victim radar. Generally, the Chi-square model represents a more general fluctuation characteristic.

Then, we evaluate the performance of two existing uncoordinated mitigation approaches (RFDM and FH) and proposed AFH-PM approach. The chirp sequence is designed to meet the maximum detectable range $d _ { \operatorname* { m a x } } = 1 5 0$ m and relative velocity $v _ { \mathrm { m a x } } = 1 2 0$ km/h while the range resolution is 15 cm and velocity resolution is smaller than 1 m/s.

First, the effect of RFDM, FH and AFH-PM on the interference mitigation is depicted in terms of the probability of false detection, miss detection, and effective detectable density. Fig. 12 shows the probability of false detection under RFDM, FH and AFH-PM approaches. It is observed that the RFDM approach has a high anti-interference performance with the 0.05 low probability of false detection in 0.01 radars/m sparse environment. However, it increases rapidly with the increased density of vehicle and achieves the 0.2 high probability of false detection in 0.1 radars/m narrow environment. The FH has the ability to distinguish ghosts from targets, resulting in 0.07 low probability of false detection even in a high density of vehicles. However, the more targets, the high probability of false detection. Besides, the AFH-PM approach has the least false detection performance for it can spread the energy of ghost across doppler dimension by random binary phase modulation.

![](images/6994df0b48ad8e05b0c3c01ab06df9488d60b33e63b7b07bc5b4c09dafc56350.jpg)  
Fig. 12. The probability of false detection versus initial vehicle density under RFDM and FH approaches.

![](images/f2055921e00f762c470b1eafb7523d4b6c03e62976c6d3eda493a3473a5fa62d.jpg)  
Fig. 13. The probability of miss detection versus initial vehicle density under RFDM and FH approaches.

Fig. 13 describes the probability of miss detection under RFDM, FH and AFH-PM approaches. Under the simulation parameter, we have $d _ { 6 7 5 } = 4 6 5$ m for RFDM while $d _ { 6 7 5 } = 2 8 0$ m for FH. The miss detection event occurs owing to the effect of large side lobe power while with $1 0 ^ { - 4 }$ order of magnitude relatively small probability compared with false detection, which indicates that reducing the probability of false detection will improve the performance of interference mitigation largely. Besides, the AFH-PM approach has the ability to reduce the noise floor, leading to the least probability of miss detection.

Besides, Fig. 14 presents the effective detectable density when employing RFDM, FH, AFH-PM and no mitigation approaches. Owing to the high probability occurrence of mutual interference, a bad effective detectable density performance is obtained when no interference mitigation approach is employed, which can achieve maximum 0.028 cars/m effective detectable density for the case 0.02 cars/m initial density. The

![](images/a0a52a68e2364bad77004d51095a3eca1d4dec714752c781c68020947d0eccfa.jpg)  
Fig. 14. The effective detectable density versus initial vehicle density under RFDM, FH and no mitigation approaches.

![](images/d16343fcedbf0a50a868af8b1a3787b651c296ba23b23c399c74c05e55b82d8f.jpg)  
Fig. 15. The probability of interference for varying frequency hopping rate.

RFDM approach improves the performance at a limited level by employing frequency division multiplexing technology, which can achieve 0.13 cars/m effective detectable density. However, limited number of sub-bands is not enough for all radars to transmit randomly and independently with increased vehicle density. The FH approach has a low probability of interference by distinguishing ghosts from targets, resulting in 0.16 cars/m high effective detectable density. The AFH-PM approach shows good performance, which can not only prevent detection of the detection of the ghost, but also reduces the noise floor. Compared with no mitigation approach, the performance improvement of RFDM, FH and AFH-PM is 6.7 dB, 7.6 dB and 8.2 dB, respectively.

Finally, the effect of the frequency hopping parameter on the interference is provided in Fig. 15. It is observed that the faster the frequency hopping rate, the better the interference mitigation performance. By hopping into available sub-bands, the interference only occurs in a short interval, thus mitigating the mutual interference to a large extent.

## VII. CONCLUSION

Based on the stochastic distribution of vehicle nodes in real environment, we have analyzed the automotive radar mutual interference in terms of channel fading, directional antenna gain and RCS characteristic in two-lane and multi-lane scenarios. Then the performance of two uncoordinated interference mitigation approaches are evaluated considering the probability of false detection and miss detection, effective detectable density and maximum number of interference-free radar. Extensive results show the effectiveness of the proposed analytic framework and reduced probability of automotive radar interference by the uncoordinated mitigation approaches even in a dense environment. Finally, a novel AFH-PM approach is proposed to prevents the detection of the ghost which combines the adaptive FH technology with the binary phase modulation. It is observed that RFDM, FH, and AFH-PM approaches can improve the performance of effective detectable density by 6.7 dB, 7.6 dB and 8.2 dB, respectively. Besides, though uncoordinated mitigation approaches have made huge effort, especially for FH, it’s still a challenge to avoid multiple radars hopping into the same available sub-band and generating co-channel interference again.

## REFERENCES

[1] J. Hatch, A. Topak, R. Schnabel, T. Zwick, R. Weigel, and C. Waldschmidt, “Millimeter-wave technology for automotive radar sensors in the 77 GHz frequency band,” IEEE Trans. Microw. Theory Techn., vol. 60, no. 3, pp. 845–860, Mar. 2012.

[2] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[3] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 32–44, Sep. 2019.

[4] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[5] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 20–31, Sep. 2019.

[6] M. Goppelt, H.-L. Blocher, and W. Menzel, “Automotive radar– investigation of mutual iinterference mechanisms,” Adv. Radio Sci.., vol. 8, no. 2010–1, pp. 55–61, 2010.

[7] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[8] M. Alhumaidi and M. Wintermantel, “Interference avoidance and mitigation in automotive radar,” in Proc. Eur. Radar Conf., 2021, pp. 172–175.

[9] D. Ammen, M. Umehira, X. Wang, S. Takeda, and H. Kuroda, “A ghost target suppression technique using interference replica for automotive FMCW radars,” in Proc. IEEE Radar Conf., 2020, pp. 1–5.

[10] S. Jin, J. H. Park, and S. Roy, “Slow-time waveform randomization performance under incoherent FMCW radar interference,” in Proc. IEEE Veh. Technol. Conf., 2021, pp. 1–7.

[11] C. Aydogdu, M. F. Keskin, and H. Wymeersch, “Automotive radar interference mitigation via multi - hop cooperative radar communications,” in Proc. Eur. Radar Conf., 2021, pp. 270–273.

[12] A. Al-Hourani, R. J. Evans, S. Kandeepan, B. Moran, and H. Eltom, “Stochastic geometry methods for modeling automotive radar interference,” IEEE Trans. Intell. Transp. Syst., vol. 19, no. 2, pp. 333–344, Feb. 2018.

[13] P. Chu, J. A. Zhang, X. Wang, Z. Fei, G. Fang, and D. Wang, “Interference characterization and power optimization for automotive radar with directional antenna,” IEEE Trans. Veh. Technol., vol. 69, no. 4, pp. 3703–3716, Apr. 2020.

[14] Z. Fang, Z. Wei, X. Chen, H. Wu, and Z. Feng, “Stochastic geometry for automotive radar interference with RCS characteristics,” IEEE Wireless Commun. Lett., vol. 9, no. 11, pp. 1817–1820, Nov. 2020.

[15] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[16] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[17] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp aequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, Sep. 2018.

[18] T. Schipper, S. Prophet, M. Harter, L. Zwirello, and T. Zwick, “Simulative prediction of the interference potential between radars in common road scenarios,” IEEE Trans. Electromagn. Compat., vol. 57, no. 3, pp. 322–328, Jun. 2015.

[19] A. Munari, L. Simic, and M. Petrova, “Stochastic geometry interference analysis of radar network performance,” IEEE Commun. Lett., vol. 22, no. 11, pp. 2362–2365, Nov. 2018.

[20] J. Huang et al., “V2X-Communication assisted interference minimization for automotive radars,” China Commun., vol. 16, no. 10, pp. 100–111, Oct. 2019.

[21] L. Kui, S. Huang, and Z. Feng, “Interference analysis for mmWave automotive radar considering blockage effect,” Sensors, vol. 21, no. 12, 2021, Art. no. 3962.

[22] M. J. Farooq, H. ElSawy, and M. -S. Alouini, “A stochastic geometry model for multi-hop highway vehicular communication,” IEEE Trans. Wireless Commun., vol. 15, no. 3, pp. 2276–2291, Mar. 2016.

[23] K. V. Mishra, B. Shankar M. R., and B. Ottersten, “Stochastic-geometry-Based interference modeling in automotive radars using matern hard-core process,” in Proc. IEEE Radar. Conf., 2020, pp. 1–5.

[24] I. M. Kunert, “Project final report, MOSARIM: MOre safety for all by radar interference mitigation,” 2012. [Online]. Available: http: //cordis.europa.eu/docs/projects/cnect/1/248231/080/deliverables/001- D611finalreportfinal.pdf

[25] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun. Netw., 2016, pp. 1–9.

[26] S. Rao and A. V. Mani, “Interference characterization in FMCW radars,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[27] K. U. Mazher, R. W. Heath, K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[28] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: Modulation schemes and interference mitigation,” IEEE Microw. Mag., vol. 20, no. 9, pp. 58–72, Sep. 2019.

[29] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Tech., vol. 65, no. 5, pp. 1727–1734, May 2017.

[30] J. Bechter, K. Eid, F. Roos, and C. Waldschmidt, “Digital beamforming to mitigate automotive radar interference,” in Proc. IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2016, pp. 1–4.

[31] J. F. Kurose and K. W. Ross, Computer Networking: A. Top-Down Approach, 7th ed. Boston, MA, USA: Pearson, 2016.

[32] J. Bechter, C. Sippel, and C. Waldschmidt, “BATS-Inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. 2016 IEEE MTT-S Int. Conf. Microw. Intell. Mobility, 2016, pp. 1–4.

[33] M. Zhang, S. He, C. Yang, J. Chen, and J. Zhang, “VANET-Assisted interference mitigation for millimeter-wave automotive radar sensors,” IEEE Netw., vol. 34, no. 2, pp. 238–245, Mar. 2020.

[34] S. Jin and S. Roy, “FMCW radar network: Multiple access and interference mitigation,” IEEE J. Sel. Topics Signal Process., vol. 15, no. 4, pp. 968–979, Jun. 2021.

[35] Systems Characteristics of Automotive Radars Operating in the Frequency Band 76-81 GHz for Intelligent Transport Systems Applications, Rec. ITU-R M. 2057-1, 2018.

[36] V. Dham, “Programming chirp parameters in TI radar devices,” Texas Instruments, Appl. Rep. SWRA553, May 2017.

[37] F. Roos et al., “Enhancement of Doppler resolution for chirp-sequence modulated radars,” in Proc. Eur. Radar Conf., 2016, pp. 237–240.

[38] D. Lewinski, “Nonstationary pprobabilistic target and clutter scattering models,” IEEE Trans. Antennas. Propag., vol. 31, no. 3, pp. 490–498, May 1983.

[39] Y. Lee et al., “RCS based target recognition with real FMCW radar implementation,” Microw. Opt. Technol. Lett., vol. 58, no. 7, pp. 1745–1750, Jul. 2016.

[40] M. Haenggi, Stochastic Geometry for Wireless Networks. Cambridge, U.K.: Cambridge Univ. Press, 2012.

[41] K. M. Noga and B. Palczynska, “Overview of fading channel modeling,” Int. J. Electron. Telecommun., vol. 56, no. 4, pp. 339–344, Nov. 2010.

[42] J. D. Vega Sanchez, L. Urquiza-Aguiar, and M. C. Paredes, “Fading channel models for mm-Wave communications,” Electronics, vol. 10, no. 7, 2021, Art. no. 798.

[43] R. He, A. F. Molisch, F. Tufvesson, Z. Zhong, B. Ai, and T. Zhang, “Vehicle-to-vehicle propagation models with large vehicle obstructions,” IEEE Trans. Intell. Transp. Syst., vol. 15, no. 5, pp. 2237–2248, Oct. 2014.

[44] 3GPP, “Study on channel model for frequency spectrum above 6 GHz,” Tech. Rep. TR 38.900 (V15.0.0), 2018.

[45] I. Toyoda, T. Seki, and K. Iiguse, “Reference antenna model with side lobe for TG3c evaluation,” IEEE 802.15-06-0474-00-003c, Dallas, USA, Nov. 2006. [Online]. Avialable: https://mentor.ieee.org/802.15/file/06/15- 06-0474-00-003c-reference-antenna-model-with-side-lobe-tg3cevaluation.pdf

[46] Z. Yang and A. Mani, “Interference mitigation for AWR/IWR devices,” Texas Instruments, Appl. Rep. SWRA662, Jan. 2017.

[47] Design Specification for Highway Alignment, JTG D20-2017, CCCC First Highway Consultants Co., Ltd., China Communications Press, Beijing, China, Dec. 2017.

![](images/7899549a3f885f61fb3b09328222d49b46fc354a64a053d29602eb7047fa8bc4.jpg)  
Yi Wang (Student Member, IEEE) received the B.Eng. degree from Beijing Jiaotong University, Beijing, China, in 2018. He is currently working toward the Ph.D. degree with the Beijing University of Posts and Telecommunications, Beijing, China. His research interest includes interference management, joint communication and sensing network, and resource allocation.

![](images/710807d7f620df021eb4dc9d65cddf1593e50b80c22aea7e7926577c5f81ad51.jpg)

Qixun Zhang (Member, IEEE) received the B.Eng. degree in communication engineering and the Ph.D. degree in circuit and system from the Beijing University of Posts and Telecommunications (BUPT), Beijing, China, in 2006 and 2011, respectively. From March to June 2006, he was a Visiting Scholar with the University of Maryland, College Park, MD, USA. From November 2018 to November 2019, he was a Visiting Scholar with the Department of Electrical and Computer Engineering, University of Houston, Houston, TX, USA. He is currently a Professor with

the Key Laboratory of Universal Wireless Communications, Ministry of Education, and the School of Information and Communication Engineering, BUPT. He is also an active in ITU-R WP5A/5C/5D Standards. His research interests include B5G/6G mobile communication system, joint communication and sensing system for autonomous driving vehicle, mmWave communication systems, cognitive radio and heterogeneous networks, game theory, and unmanned aerial vehicles (UAVs) communication.

![](images/297719c0d6275bab9d53fa3fef67c19829d227cc1547f0020aeb902b9078d65a.jpg)

Zhiqing Wei (Member, IEEE) received the B.Eng. and Ph.D. degrees from the Beijing University of Posts and Telecommunications (BUPT), Beijing, China, in 2010 and 2015, respectively. He is currently an Associate Professor with BUPT. He has authored one book, three book chapters, and more than 50 papers. His research interest include the performance analysis and optimization of intelligent machine networks. He was the recipient of Exemplary Reviewer of IEEE WIRELESS COMMUNICATIONS LETTERS in 2017, Best Paper Award of WCSP 2018. He was

the Registration Co-Chair of IEEE/CIC ICCC 2018, Publication Co-Chair of IEEE/CIC ICCC 2019 and IEEE/CIC ICCC 2020.

![](images/98448027eecdc432c463972cccdc0fdce978cc3899e86b17ba45f57a07f93fde.jpg)

Liping Kui received the B.S. and M.S. degrees from Yunnan University, Kunming, China, in 2009 and 2012. She is currently working toward the Ph.D. degree with the Beijing University of Posts and Telecommunications, Beijing, China. Her research interests include millimeter wave communication, interference analysis of automotive radar, and joint sensing and communication network.

![](images/7bd9e5640b4d4181e21e02354e7cc32ad039dccdce8a21cd64b0739d69233017.jpg)

Zhiyong Feng (Senior Member, IEEE) received the B.S., M.S., and Ph.D. degrees from the Beijing University of Posts and Telecommunications (BUPT), Beijing, China. She is currently a Professor with the School of Information and Communication Engineering, BUPT, and the Director of the Key Laboratory of Universal Wireless Communications, Ministry of Education, China. Her research interests include wireless network architecture design and radio resource management in 5th generation mobile networks (5G), spectrum sensing and dynamic spectrum

management in cognitive wireless networks, universal signal detection and identification, and network information theory. She is also an active in standards development, such as ITU-R WP5A/5C/5D, IEEE 1900, ETSI, and CCSA.

![](images/9d00da9fdc7042676c3747dfae1367aa2577a45ea430aa840d2d537878e5ef50.jpg)

Fan Liu (Member, IEEE) received the B.Eng. and Ph.D. degrees from the Beijing Institute of Technology, Beijing, China, in 2013 and 2018, respectively. He is currently an Assistant Professor with the Department of Electronic and Electrical Engineering, Southern University of Science and Technology, Shenzhen, China. From 2016 to 2018, he has previously held Academic Positions with the University College London, London, UK, as a Visiting Researcher, and as a Marie Curie Research Fellow from 2018 to 2020.

His research interests include the general area of signal processing and wireless communications, and in particular in the area of Integrated Sensing and Communications (ISAC). He has ten publications selected as IEEE ComSoc Besting Readings in ISAC. He is the Founding Academic Chair of the IEEE ComSoc ISAC Emerging Technology Initiative (ISAC-ETI), Associate Editor for the IEEE COMMUNICATIONS LETTERS and the IEEE OPEN JOURNAL OF SIG-NAL PROCESSING, and Guest Editor of the IEEE JOURNAL ON SELECTED AREAS IN COMMUNICATIONS, IEEE WIRELESS COMMUNICATIONS, and China Communications. He was also an organizer and Co-Chair for numerous workshops, special sessions and tutorials in flagship IEEE/ACM conferences, including ICC, GLOBECOM, ICASSP, and MobiCom. He is the TPC Co-Chair of the 2nd and 3rd IEEE Joint Communication and Sensing Symposium (JC&S), and will be a Track Co-Chair for the IEEE WCNC 2024. He is a Member of the IMT-2030 (6G) ISAC Task Group. He was the recipient of the IEEE Signal Processing Society Young Author Best Paper Award of 2021, Best Ph.D. Thesis Award of Chinese Institute of Electronics of 2019, EU Marie Curie Individual Fellowship in 2018, and has been named as an Exemplary Reviewer for IEEE TWC/TCOM/COMML for five times. Dr. Fan Liu was listed in the World’s Top 2% Scientists by Stanford University for citation impact in 2021 and 2022.