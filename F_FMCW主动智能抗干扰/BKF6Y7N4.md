# FMCW Radar Network: Multiple Access and Interference Mitigation

Sian Jin and Sumit Roy , Fellow, IEEE

Abstract—With the increasing proliferation of radars on vehicles, interference among vehicular radars is becoming a serious issue. In this work, we consider a frequency modulated continuous wave (FMCW) radar network with coherent radar interference where all radars adopt the same chirp slopes. Four asynchronous non-cooperative media access control (MAC) protocols are used for mutual radar interference mitigation. We propose two cross-layer performance metrics - multiple access capacity and probability of target misdetection to quantify the network performance under each MAC protocol. Based on our analysis and extensive simulations, we find the pure random access achieves a very poor trade-off between multiple access capacity and probability of target misdetection. However, such a trade-off can be significantly improved by frequency hopping and phase coding. This shows that proper MAC protocols can achieve very good performance even without synchronization and coordination. We describe new insights behind such gains that can be valuable for FMCW radar MAC design.

Index Terms—FMCW radar, radar networks, MAC, interference detection and mitigation, interference modeling.

## I. INTRODUCTION

UTOMOTIVE radars are increasingly becoming a commodity in support of various safety-enabling driverassistive functions, based on estimating the relative range and radial velocity to targets (vehicles, pedestrians, etc.) [2]. Today, the most common automotive radar is frequency modulated continuous wave (FMCW) radar [3], [4] (shown in Fig. 2), which transmit chirps (linear frequency modulated signals) on radio frequency (RF) band, see Fig. 1. With the growing density of vehicular FMCW radars, multiple co-channel radars may cause mutual interference. In this case, the received signal at a victim radar in Fig. 2 is a superposition of the desired targets’ echoes and undesired interference from other simultaneously active cochannel radars. Such mutual radar interference can potentially degrade radar detection and estimation performance [5].<sup>1</sup>

![](images/5064171eca94bc92ccab8f73b64919f7465817d8dba9908cae478febff93fe88.jpg)

Fig. 1. Time-frequency signal representation of FMCW chirps on RF band.  
![](images/6ca724fde4e05c46feaad33955951a264350ac8172d2ef6cb2da6c2195819946.jpg)  
Fig. 2. A typical transceiver block diagram of an FMCW SISO radar [3], [14] in an interference scenario.

The interference at a victim radar receiver can be classified into incoherent and coherent interference [4], [7]–[9]. Incoherent interference is generated when the victim radar and the interfering sources have different chirp slopes, while coherent interference is generated when all radars have an identical chirp slope. At the victim radar’s intermediate frequency (IF) band, incoherent interference appears as additive noise and reduces target detection probability [4], and coherent interference creates ghosts, i.e., fictitious targets (see Fig. 2) that appear at random ranges [8], causing false alarms. While both types of interference are detrimental, coherent interference is more challenging than incoherent, since ghosts require novel signal processing to distinguish them from genuine targets [6]. As in [7]–[13], this work considers a network of mutually interfering FMCW single-input single-output (SISO) radars with identical chirp slope and analyzes coherent interference.

Media access control (MAC) techniques in the time, frequency, and coding domains are widely adopted to deal with coherent interference [4], [7], [8], [10]–[13], [15]–[18]. Radar MAC designs are based on centralized [8], [13], [18] or distributed [7], [10]–[12] protocols. The schemes in [12], [13], [18] realize MAC scheduling using GPS for time synchronization or position updates, additional communication channels and control messages. However, such standardization requirements are undesirable for existing non-cooperative radars [17]. In [8], [12], [13], time-synchronous schemes aiming at achieving orthogonal access are proposed. A challenge in time-synchronous orthogonal scheduling is that the interference propagation delay, typically in the order of chirp duration (microseconds [19]), can deteriorate orthogonality significantly. As shown in Fig. 1, even if two radar sources are synchronously and orthogonally scheduled with different transmit start instants, the receiver of the reference radar may experience interference from the other source due to the random interference propagation delay caused by relative random position. Thus, the MAC protocols in [4], [12] separate transmit start instants of different radars beyond maximum interference propagation delay to achieve guaranteed orthogonal scheduling, which can be inefficient.

In this work, we focus on distributed MAC protocols that are operated without any time synchronization and cooperation. The underlying motivation is analyzing asynchronous distributed MAC protocols for multi-radar operations with a view to characterizing the pros and cons of various designs. As noted by the recent survey [15], very few prior works have analyzed the radar performance in mutual interference. [20] studies interference between one pair of radars using a pure physical (PHY) layer analysis without considering radar network aspects. [21] adopts stochastic geometry methods for modeling aggregate radar interference, while the PHY layer signal characteristics are not captured. [7], [8] constitute early work that considered both waveform (chirp) structure and network aspects to capture the interference probability at a victim radar. While [7], [8] broadly conclude that the interference probability is low for a pure random access scheme, they do not quantify this probability in terms of target detection performance and false alarm performance under different radar densities. In this paper, we define two cross-layer metrics to quantify network performance: target misdetection probability and multiple access capacity. The multiple access capacity is defined as the average density of radars that can operate without false alarm caused by coherent interference. In contrast with the conclusions in [7], [8], our analysis shows that a pure random access scheme like un-slotted ALOHA (UA) with random frequency division multiplexing (RFDM), achieves a poor trade-off between multiple access capacity and probability of target misdetection even in a low radar density regime. To improve this trade-off, we adopt frequency hopping (FH) [10], [16] and phase coding (PC) [7], [8], [11] as potential enhancements. Our analysis shows that even without synchronization and coordination, UA along with FH and PC improve operational trade-off by significantly increasing the multiple access capacity. This can be explained by the detect-and-classify principle introduced later, which provides potential guidance for future standardization activities.

## II. OVERVIEW OF FMCW COHERENT INTERFERENCE AND PROPOSED SCHEMES

## A. FMCW PHY Layer and Coherent Interference

We now review the signal processing flow for an FMCW SISO radar complex baseband transceiver chain [7] and illustrate the impact of coherent interference. As shown in Fig. 2, FMCW radars periodically transmit a sequence of chirps [2] and receive a delayed version of the transmitted chirps. If the transmitted chirp signal is backscattered from a target at a distance of <sup>d</sup> meters, the round-trip delay for receiving the target’s echo is $\frac { 2 d } { c }$ where <sup>c</sup> is the speed of the light [14]. The received target echo is then mixed with the output of the local FMCW synthesizer (the reference signal), which is called dechirping, to generate the IF signal - a single tone whose frequency equals to the round-trip delay $\textstyle { \frac { 2 d } { c } }$ multiplied by the chirp slope <sup>h</sup> [14] (see Fig. 1). The resulting single tone signal is then passed through a low pass filter (LPF) with cutoff frequency $f _ { H }$ chosen for anti-aliasing and eliminating out-of-band interference. If the echo from the target at distance <sup>d</sup> passes the LPF, then its IF signal frequency $\frac { 2 d h } { c } \leq f _ { H }$ (see Fig. 1). Similarly, if the delayed same-slope interference chirp is de-chirped and passes through the LPF of the victim radar, the resulting single-tone IF signal looks like a de-chirped target echo and appears as a ghost (see Fig. 1 and Fig. 2). The low-pass filtered signals are sampled by an analog-to-digital converter (ADC) and processed using discrete Fourier transform (DFT) for subsequent range and velocity estimation.

![](images/5b30f6d486404ac34ae541d2c8369a432e5448d927cc3694f068935c9bcec8ec.jpg)  
Fig. 3. Signals over L chirp cycles (a CPI) on the same range bin are used for velocity DFT.

To estimate the target range <sup>d</sup>, each radar estimates IF frequency of the target $\frac { 2 \breve { d } h } { c }$ using DFT - hence called range DFT. The maximum detectable range $\begin{array} { r } { d _ { t , \operatorname* { m a x } } = \frac { f _ { H } c } { 2 h } } \end{array}$ corresponds to a radar-target pair such that the target’s IF signal just falls inside the radar’s LPF passband cutoff. The range resolution - the minimum distance that a DFT based range estimation algorithm can resolve - is $\begin{array} { r } { d _ { r e s } = \frac { c } { 2 B _ { c } } [ 1 4 ] } \end{array}$ , where $B _ { c }$ is the chirp <sup>c</sup>bandwidth. This partitions the maximum detection range into $N \triangleq { \frac { d _ { t , \operatorname* { m a x } } } { d _ { r e s } } }$ range bins (see Fig. 3), or equivalently, partitions <sup>res</sup>the IF band of bandwidth $f _ { H }$ into <sup>N</sup> frequency bins of bandwidth $\scriptstyle { \frac { f _ { H } } { N } }$ (frequency resolution). As shown in Fig. 3, the peak of each dechirped target or ghost will appear in one range bin. Note that the above range estimator is feasible when the transmit start instant of the radar’s chirp is known. Unlike measuring the range of targets, measuring ranges of interferers (or propagation delay of interference) is non-trivial because the transmit start instants of interference is unknown at the victim radar, even if ghosts were identified.

![](images/f0f42f6c9b03d7197747fddb326a84b01f2f645028bf27fb9b86d4f42e7485c9.jpg)  
Fig. 4. 2D range-velocity bins.

For a target moving with relative velocity <sup>v</sup> over a chirp transmission period $T _ { g } ,$ , the relative motion $\Delta d = T _ { g } v$ is typically sufficiently small to keep the target in the same range bin. The corresponding phase difference between two consecutive range measurements is $\begin{array} { r } { \Delta \Phi = 2 \pi f _ { c } \frac { 2 \Delta d } { c } } \end{array}$ [22], where $f _ { c }$ is the chirp’s central frequency. Over <sup>L</sup> such chirp cycles, if the velocity of the target remains nearly constant, the target phase in the same range bin increases linearly with $\Delta \Phi$ per chirp cycle. Then, using the DFT on the <sup>L</sup> signals in the same range bin yields an estimate of $\Delta \Phi$ (see Fig. 3), which in turn can be used to estimate the velocity <sup>v</sup> [14] - hence such DFT is called velocity DFT. The <sup>L</sup> chirp cycle time $T _ { f } \triangleq L T _ { g }$ for a single velocity estimation is called coherent processing interval (CPI) [11]. The corresponding maximum detectable relative velocity $\begin{array} { r } { v _ { t , m a x } = \frac { c } { 4 f _ { c } T _ { g } } } \end{array}$ [16] and the velocity resolution resolvable by DFT is $\begin{array} { r } { v _ { r e s } = \frac { c } { 2 f _ { c } T _ { f } } } \end{array}$ [16]. This partitions the maximum relative velocity into $\begin{array} { r } { \frac { v _ { t , m a x } - ( - v _ { t , m a x } ) } { \circ } = L } \end{array}$ velocity <sup>res</sup>bins. Above range DFT and velocity DFT form the 2D <sup>N</sup>-by-<sup>L</sup> range-velocity bins shown in Fig. 4. The outputs on the rangevelocity bins are fed into the cell-averaging constant-false-alarm rate (CA-CFAR) detector for detecting signal peaks [2]. From Fig. 3 and Fig. 4, we can see that after range-velocity DFT, a ghost may lead to a false target and causes false alarm after CA-CFAR detection. If a target and an interference signal are well separated on different range-velocity bins, the target can be correctly detected. However, if a target and a strong interference signal fall into adjacent bins, the side-lobe of the interference may cause target misdetection.

## B. UA-RFDM

To deal with coherent interference, we first consider the simplest distributed MAC – un-slotted ALOHA with random frequency division multiplexing (UA-RFDM) shown in Fig. 5. This MAC, based on the well-known un-slotted ALOHA (UA) [23], has a key characteristic that each radar’s initial chirp transmission time is random, and after that, each radar transmits periodically with a fixed inter-chirp duration $T _ { g }$ . We combine UA with random frequency division multiplexing (RFDM), whereby each radar independently and randomly transmits on one of the multiple sub-bands over a CPI and the initial chirp phases of each radar are the same over a CPI. The resulting MAC does not require any time synchronization and control overhead. In Section IV, we show that this MAC has a very low multiple access capacity (very high false alarm probability). The fundamental reason for the poor capacity performance is that this MAC has no method to discriminate ghosts from targets and regards all ghosts as targets.

![](images/e5dd24021188cea7254d6834d3f1f893acbb2a8f44da8c57c1a216a6e586a04d.jpg)  
Fig. 5. UA-RFDM with 2 radars independently choosing sub-band 1.

![](images/842709ad66e97120029416e2a8bb8e9a71a2ea27c54d58408eb5a73a63412c51.jpg)  
Fig. 6. UA-FH on 2 sub-bands.

## C. UA-FH

To enhance the performance of UA-RFDM, we next modify the RFDM into frequency hopping (FH), an idea previously considered in [10] and [16] to suppress the interference peak power on range-velocity bins. Such a scheme is called UA-FH shown in Fig. 6. When multiple sub-bands are available, each radar randomly and independently chooses one of the sub-bands for transmission in each chirp cycle. Over a CPI, the radar targets always appear in the same range bin, while the de-chirped ghosts randomly appear in range bins due to FH. For example, in Fig. 6, radar 1 and radar 2 randomly and independently hop on 2 sub-bands in each chirp cycle, and they only choose the same sub-band in the first chirp cycle. Thus, in Fig. 7, radar 1’s ghost only appears at radar $2 \mathrm { { : } }$ receiver in the first chirp cycle. Compared to [10] and [16], the key innovation in our scheme is that we propose to use the random appearance of ghosts as a characteristic to distinguish ghosts from targets. This innovation, called detect-and-classify, avoids the identified ghosts passing for velocity DFT and reduces the probability of false alarm on range-velocity bins. It works very well when ghosts do not fall into the same range bins of targets and makes UA-FH achieving much better multiple access capacity than UA-RFDM.

![](images/e2c310066366b20b931503cc26d11fcb1a3f32111ac108b6adbbc462ea8e7299.jpg)  
Fig. 7. Detect-and-classify using frequency hopping: A ghost can be distinguished from a target as it randomly appears on a range bin over different chirp cycles.

![](images/3c4815ae5002bb5aeba00166b6f399984c9bfde30d4a23f5451b1562343969e3.jpg)  
Fig. 8. UA-RFDM-PC with 2 radars independently choosing sub-band 1.

## D. UA-RFDM-PC

Another method to enhance UA-RFDM is to combine it with phase coding (PC) proposed in [7], [8], [11]. Such scheme is called UA-RFDM-PC shown in Fig. 8. In each chirp cycle, the radar transmitter adds a random binary phase rotation 0 or <sup>π</sup> on the chirp before transmitting, where 0 and <sup>π</sup> are chosen with equal probability. At the radar receiver, the random binary phase rotation is compensated back after de-chirping the received signal. As shown in Fig. 9, after the phase compensation, the target phase increases linearly over different chirp cycles as normal. In contrast, as the code of an interfering radar does not match the code of a victim radar, the phase increment of the ghost seen at the victim radar receiver is random. Thus, after velocity DFT, ghosts are spread into pseudo-noise at the victim radar’s detector input. This scheme can achieve much better multiple access capacity than UA-RFDM, as ghosts appear as incoherent noise and infrequently cause false alarms.

## E. UA-FH-PC

In UA-FH, a persistently appearing target can make randomly appearing ghosts on the same range bin unidentified and causing false alarms. PC can spread these unidentified ghosts into pseudo-noise and further reduce false alarm probability. In UA-RFDM-PC, ghosts on any range bin are spread into pseudo-noise that has the potential to cause false alarms on any range bin. FH helps to identify ghosts and reduces the occurrence of pseudo-noise when the ghosts do not fall into the same range bin as a target. These motivate us to combine UA, FH and PC into UA-FH-PC shown in Fig. 10. In UA-FH-PC, each chirp is added with binary random phase rotation and is transmitted on a randomly picked subband. This scheme can achieve much better multiple access capacity than UA-FH and UA-RFDM-PC, as FH and PC remedy the disadvantage of each other.

![](images/04b51b808e44b6a5c50ff4461c570df8a64f795c9f73701fa9220a06e2dd520c.jpg)  
Fig. 9. Detect-and-classify using phase coding: A ghost can be distinguished from a target due to it’s random phase over different chirp cycles.

![](images/1dc09f840e546f0b44b544e82b952c32e862727eb157915de651ca196b85e313.jpg)  
Fig. 10. UA-FH-PC on 2 sub-bands.

## III. RADAR INTERFERENCE MODEL AND PERFORMANCEMETRICS

In this section, we propose a radar interference model and performance metrics for analyzing the considered MAC schemes. As shown in Fig. 11, single FMCW SISO radar-equipped vehicles distribute on an infinitely long single-lane road following 1D homogeneous Poisson point process (PPP) with density λ. We collect the first order PHY layer assumptions for our subsequent analysis as follows.

\- Assumption 1: All radars are identical with the same chirp bandwidth $\boldsymbol { B } _ { c } ,$ chirp slope <sup>h</sup>, transmit period $T _ { g } ,$ , cutoff frequency $f _ { H }$ of IF section, transmitter power $P _ { t }$ and transmit (receive) antenna gain $G _ { t } ( G _ { r } )$ . All targets have the same radar cross-section $( \operatorname { R C S } ) \sigma$ . For target at distance <sup>d</sup>, the received target power $P _ { r }$ follows the mono-static radar equation [4]

![](images/c52533c5dda127fd56a5afba2f61227bb77486d03e98a12dfbc35bebf8b488c1.jpg)  
Fig. 11. Radar interference scenario with unit-disk interference model.

$$
P _ { r } = { \frac { P _ { t } G _ { t } G _ { r } \sigma c ^ { 2 } } { ( 4 \pi ) ^ { 3 } f _ { c } ^ { 2 } d ^ { 4 } } } .\tag{1}
$$

\- Assumption 2: The total system RF band is divided into M sub-bands, each of bandwidth $B _ { c }$ that is equal to the chirp bandwidth.

\- Assumption 3: Noise power at IF band is negligible.

The same slope assumption implies that an interfering radar’s signal being de-chirped into the victim FMCW radar’s IF band appears as a ghost [7], [9], as shown in Fig. 2.<sup>2</sup> Furthermore, as range resolution $\begin{array} { r } { d _ { r e s } = \frac { c } { 2 B _ { c } } } \end{array}$ of each radar is expected to be <sup>c</sup>sufficiently small, chirp bandwidth $B _ { c }$ has a lower bound. Thus, for fixed total system bandwidth, the number of sub-bands <sup>M</sup> in Assumption 2 cannot be too large. The noise-free assumption in Assumption 3 allows us to ignore the false alarm and target misdetection caused by noise, and focus exclusively on radar mutual interference.

We only consider the line-of-sight (LOS) interference as in [4], [15], as non-LOS interference is much weaker [4]. For interference at range $d _ { i } ,$ the received interference power $P _ { i n t }$ is determined by the free-space path-loss (Friis) formula [9]

$$
P _ { i n t } \triangleq \frac { P _ { t } G _ { t } G _ { r } c ^ { 2 } } { ( 4 \pi ) ^ { 2 } f _ { c } ^ { 2 } d _ { i } ^ { 2 } } .\tag{2}
$$

Thus, the maximum propagation range of LOS interference is $\begin{array} { r } { d _ { F r i i s } ^ { m a x } = ( \frac { P _ { t } G _ { t } G _ { r } c ^ { 2 } } { ( 4 \pi ) ^ { 2 } f _ { c } ^ { 2 } P _ { r } ^ { m i n } } ) ^ { \bar { 1 } / 2 } } \end{array}$ , where $P _ { r } ^ { m i n }$ the minimum receive power. By $[ 3 ] , P _ { t } = 1 2$ dBm, $G _ { t } = G _ { r } = 1 2$ dBi, $P _ { r } ^ { m i n } =$ −128 dBm, $f _ { c } = 7 7 \mathrm { G H z }$ , we have $d _ { F r i i s } ^ { m a x } = 4 9$ <sup>.</sup>1km. Such a large $d _ { F r i i s } ^ { m a x }$ value is an over-estimate, as interference signals cannot propagate over such ranges without blockage in most realistic scenarios. Following a large body of prior work in vehicular networking [25] (and references therein) and ignoring the effect of directional antenna beams for simplicity, we adopt a unit-disk interference model. As shown in Fig. 11, the unit-disk interference model defines the interference range $d _ { i , m a x }$ - the maximum distance that can cause interference to a victim receiver. Typically, $d _ { i , m a x } \ll d _ { F r i i s } ^ { m a x }$ and $d _ { i , m a x } \ll c T _ { g }$ For example, if $d _ { i , m a x } = 1 0 0 0$ m and $T _ { g } = 5 5$ us [19], then $\textstyle { \frac { d _ { i , m a x } } { c } } = 3 . 3 3$ us $\ll T _ { g } .$ . Any interfering radar inside the victim radar’s interference range $( d _ { i } < d _ { i , m a x } )$ contributes LOS interference following Friis formula in (2) [9]; otherwise, the interfering radar contributes no interference.

![](images/359943313965e6d651ff846c54912ed68e42e2cd8e8d79376378ca66a2da4b37.jpg)  
Fig. 12. Time condition for radar k’s interfering chirp falling into radar $\mathrm { 0 ^ { \circ } s }$ n-th range bin.

Note that an interfering radar’s presence within a victim radar’s interference range does not necessarily imply that the interfering radar leads to a ghost at the range bin of the victim radar. This is determined by two further conditions:

a) Frequency condition: At chirp cycle $y ,$ the interference causes a ghost at a range bin of the victim radar only if the two radars transmit on the same sub-band. We denote the event that radar <sup>k</sup> and radar 0 transmit on the same sub-band at chirp cycle <sup>y</sup> as $F _ { k , 0 } ^ { y }$

b) Time condition: Suppose an interfering radar <sup>k</sup> falls into a reference radar 0’s interference range. Let $t _ { 0 } \left( t _ { k } \right)$ denote the transmit start instant of radar 0 (radar <sup>k</sup>), and hence $\Delta t _ { k , 0 } =$ $t _ { 0 } - t _ { k }$ is the difference of the transmit start instants. Let $d _ { k , 0 }$ denote the distance between the two radars. As shown in Fig. 12, the interfering chirp of radar <sup>k</sup> is dechirped by reference radar 0 and falls in radar 0’s <sup>n</sup>-th range bin, only if the following time condition $G _ { k , 0 } ^ { n }$ is met:

$$
t _ { 0 } + \frac { f _ { H } } { h } \frac { n - 1 } { N } \leq t _ { k } + \frac { d _ { k , 0 } } { c } < t _ { 0 } + \frac { f _ { H } } { h } \frac { n } { N } ,\tag{3}
$$

where $\begin{array} { r } { \Delta t _ { k , 0 } \in [ - \frac { f _ { H } } { h } , T _ { g } - \frac { f _ { H } } { h } ] , } \end{array}$ , and $d _ { k , 0 } \in ( 0 , d _ { i , m a x } ]$ . It suffices to consider a single chirp repetition interval $T _ { g } ,$ since the maximum interference propagation delay $\frac { d _ { i , m a x } } { c } \ll T _ { g } .$ Fig. 12 and (3) imply two important results. First, time-domain interference avoidance by synchronous scheduling $t _ { 0 } , t _ { k }$ for two sources is challenging because $d _ { k , 0 }$ is random and unknown. Second, pure random access implies random $t _ { k }$ that in turn places ghosts randomly in victim radars’ range bins [1], [8]. In this case, false alarms can appear on any range bins. In addition, a ghost typically has larger power than a target (indicated by (1) and (2)), and its side-lobe or ghost-spread pseudo-noise can lead to target misdetection. We formally define false alarm and target misdetection as follows.

Definition 1 (False Alarm): False alarm event $E _ { f a , k , j } ^ { n , l }$ occurs if radar $j ^ { \prime } { \bf s }$ detector detects a peak at its range-velocity bin $( n , l )$ caused by the interference from radar $k ,$ given that a target does not exist in the range-velocity bin $( n , l )$ . The false alarm event caused by radar <sup>k</sup> at radar $j$ is thus $E _ { f a , k , j } \triangleq$ $\textstyle \bigcup _ { n = 1 } ^ { N } \bigcup _ { l = 1 } ^ { L } E _ { f a , k , j } ^ { n , l } .$ ♦

Definition 2 (Target Misdetection): Target misdetection event $E _ { m d , k , j } ^ { n , l }$ occurs if radar <sup>k</sup>’s ghost at range bin <sup>n</sup> renders a target at radar <sup>j</sup>’s range-velocity bin $( n , l )$ to be un-detected. The target misdetection event caused by radar <sup>k</sup> at radar $j ^ { \prime } { \bf s }$ range bin <sup>n</sup> is thus $\begin{array} { r } { E _ { m d , k , j } ^ { n } \triangleq \bigcup _ { l = 1 } ^ { L } E _ { m d , k , j } ^ { n , l } } \end{array}$ ♦

We define the target misdetection event for each range bin <sup>n</sup> because it depends on the power of the target return for that range bin. In contrast, as we’ll see in the proof of Proposition 1 (or see Proposition 1 of [1]), the ghost power under the considered MACs is independent of range bin indices, and hence it is easier to analyze the joint false alarm event $E _ { f a , k , j }$ . We denote the set of radars falling into radar $j ^ { \circ } \mathrm { s }$ interference range as $\kappa _ { j }$ . Then, radar <sup>j</sup> encounters a false alarm with probability $\begin{array} { r } { \mathbb { E } _ { \mathcal { K } _ { j } } [ \mathrm { P r } [ \bigcup _ { k \in \mathcal { K } _ { i } } E _ { f a , k , j } | \mathcal { K } _ { j } ] ] } \end{array}$ , and suffers target misdetection at <sup>j</sup>range bin <sup>n</sup> with probability $\mathbb { E } _ { \mathcal { K } _ { j } } [ \mathrm { P r } [ \bigcup _ { k \in \mathcal { K } _ { i } } E _ { m d , k , j } ^ { n } | \mathcal { K } _ { j } ] ]$

<sup>j j</sup>Definition 3 (Fair MAC and Metrics): A MAC scheme is fair if all victim radars have the same false alarm probability $\begin{array} { r } { \operatorname* { P r } [ E _ { f a } ] = \mathbb { E } _ { \mathcal { K } _ { j } } [ \operatorname* { P r } [ \bigcup _ { k \in \mathcal { K } _ { i } } E _ { f a , k , j } | \mathcal { K } _ { j } ] ] } \end{array}$ and the same target misdetection probabilities $\operatorname* { P r } [ E _ { m d } ^ { n } ] =$ $\begin{array} { r } { \mathbb { E } _ { \mathcal { K } _ { j } } [ \mathrm { P r } [ \bigcup _ { k \in \mathcal { K } _ { i } } \mathnormal { E } _ { m d , k , j } ^ { n } | \mathcal { K } _ { j } ] ] , n = 1 , 2 , \dotsc , N } \end{array}$ . The multiple <sup>j j</sup>access capacity of a fair MAC

$$
C \triangleq \lambda \left( 1 - \operatorname* { P r } \left[ E _ { f a } \right] \right)\tag{4}
$$

is average number of non-false-alarmed radars per meter. ♦

Suppose each target independently and randomly falls into one of the range-velocity bins. Also, suppose the radars in $\kappa _ { 0 }$ independently cause target misdetection and false alarm at a reference victim radar 0. Based on these assumptions, we analyze the target misdetection probabilities and multiple access capacity of four distributed fair radar MACs in the following sections.

## IV. ANALYSIS OF UA-RFDM

We now consider the simplest random access protocol: UA-RFDM, which operationally requires no changes to a typical FMCW radar in Fig. 2. To understand the conditions for false alarm $E _ { f a , k , j }$ and target misdetection $E _ { m d , k , j } ^ { n } , ~ n \in$ $\{ 1 , 2 , \ldots , N \}$ , we first run simulations for UA-RFDM under the setup in Table I.<sup>3</sup>

Our simulations show that a ghost in a range bin always leads to a false alarm (a false target and a high-power interference side-lobe) on at least one range-velocity bin (see two examples in Fig. 13 and 14). Thus, if radar <sup>k</sup> falls into the interference range of radar 0, and the time, frequency conditions in Section III are satisfied, radar <sup>k</sup> causes false alarm at radar 0. That is, $\mathrm { i f } k \in { \cal K } _ { 0 }$ then $\begin{array} { r } { E _ { f a , k , 0 } = F _ { k , 0 } ^ { 1 } \cap ( \bigcup _ { n = 1 } ^ { N } G _ { k , 0 } ^ { n } ) } \end{array}$

TABLE I PHY LAYER SIMULATION SETUP
<table><tr><td rowspan=1 colspan=1>Simulation platform</td><td rowspan=1 colspan=1>MATLAB</td></tr><tr><td rowspan=1 colspan=1>Transmit power</td><td rowspan=1 colspan=1> $\overline { { P _ { t } = 1 2 \mathrm { d } \mathrm { B m } \ [ 3 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>Transmit/receive antenna gain</td><td rowspan=1 colspan=1> $\overline { { G _ { t } = G _ { r } = 1 2 \mathrm { d B i } \ [ 3 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>Minimum receive power</td><td rowspan=1 colspan=1> $\overline { { P _ { r } ^ { m i n } = - 1 2 8 \mathrm { d } \mathrm { B m } \ [ 3 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>RF frequency</td><td rowspan=1 colspan=1> $f _ { c } = 7 7 \mathrm { G H z } \ [ 3 ]$ </td></tr><tr><td rowspan=1 colspan=1>Chirp bandwidth</td><td rowspan=1 colspan=1> $\overline { { B _ { c } = 5 4 0 \mathbf { M } \mathrm { H z } \ [ 2 0 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>IF cutoff frequency</td><td rowspan=1 colspan=1> $\overline { { f _ { H } = 1 0 \mathbf { M } \mathrm { H z } \left[ 2 0 \right] } }$ </td></tr><tr><td rowspan=1 colspan=1>Chirp slope</td><td rowspan=1 colspan=1> $\overline { { h = 1 2 \mathrm { M H z / u s } [ 2 0 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>Number of range bins</td><td rowspan=1 colspan=1> $\overline { { N = 4 5 0 ~ [ 2 0 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>Inter-chirp duration</td><td rowspan=1 colspan=1> $\overline { { T _ { g } = 5 5 \mathrm { u s } \ [ 2 0 ] } }$ </td></tr><tr><td rowspan=1 colspan=1>Interference range</td><td rowspan=1 colspan=1> $\overline { { d _ { i , m a x } } } = 1 0 0 0 \mathrm { m }$ </td></tr><tr><td rowspan=1 colspan=1>Number of chirps in a CPI</td><td rowspan=1 colspan=1> $\overline { { L = 2 0 0 } }$ </td></tr><tr><td rowspan=1 colspan=1>Number of sub-bands</td><td rowspan=1 colspan=1> ${ \overline { { M = 2 } } }$ </td></tr><tr><td rowspan=1 colspan=1>Target&#x27;s RCS</td><td rowspan=1 colspan=1> $\overline { { 2 0 m ^ { 2 } } }$ </td></tr><tr><td rowspan=1 colspan=1>CA-CFAR operating domain</td><td rowspan=1 colspan=1>Doppler domain</td></tr><tr><td rowspan=1 colspan=1>Number of noise window in CA-CFAR</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>Number of guard window in CA-CFAR</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>CFAR threshold</td><td rowspan=1 colspan=1>10dB</td></tr></table>

![](images/d3ab1ac772d0c435ea38c8fc00542eb5c9d32f38049d7ce35f034d5a0511c31a.jpg)  
Fig. 13. PHY layer simulation under UA-RFDM with 1 target (real range: 88.13 m, real velocity: 12.10 m/s) falls into range bin $n = 3 1 8$ (88.06 m– 88.33 m) and 1 ghost (real range: 60 m, real velocity: 16.40 m/s) falls into range bin n = 365 (101.39 m–101.67 m).

As shown in Fig. 14, when a high-power ghost and a target fall into the same range bin, the target after velocity DFT may be mis-detected due to the interference side-lobe. At radar $0 \mathrm { { ^ { \circ } s } }$ range bin $n ,$ the target misdetection caused by radar <sup>k</sup> happens if and only if the following two events occur. (a) The range $d _ { k , 0 }$ between radar <sup>k</sup> and radar 0 is smaller than a range bin dependent threshold $r _ { n } .$ , and we denote such event as $R _ { k , 0 } ^ { n } . ( \mathsf { b } )$ As shown in Fig. 14, on range bin <sup>n</sup>, a target can be misdetected only when it falls into certain velocity bins near a false target, which happens with probability $p _ { n }$ . We let $I _ { k , 0 } ^ { n }$ denote the event that at least one target falls into such velocity bins. Then, conditioned on $k \in { \mathcal { K } } _ { 0 } .$ , we model $E _ { m d , k , 0 } ^ { n } = F _ { k , 0 } ^ { 1 } \cap R _ { k , 0 } ^ { n } \cap G _ { k , 0 } ^ { n } \cap I _ { k , 0 } ^ { n } .$ Focus on analyzing the performance of a reference victim radar 0, we have the following result.

Proposition 1 (PHY and MAC Layer Properties of UA-RFDM): UA-RFDM is a fair MAC with target misdetection

(b) 2D-DFT Result on Range-velocity Bins  
![](images/cfbd4ec233765454e9536692911c5087094473797fc1bfe0db2eb5d7e4a019f3.jpg)

![](images/5b90431161ece9f3ed73f13e3f5c3c7bb0bcff14f1e0c418a7ba9380022e963f.jpg)

![](images/907b0ae3a532bdac081c5e048e9b915c472ff117fb02effebe799195095cef46.jpg)  
Fig. 14. PHY layer simulation under UA-RFDM with 1 target (real range: 101.50 m, real velocity: 12.10 m/s) and 1 ghost (real range: 60 m, real velocity: 16.40 m/s) fall into the same range bin n = 365 (101.39 m–101.67 m).

probability at range bin <sup>n</sup>

$$
\mathrm { P r } \left[ E _ { m d } ^ { n } \right] = 1 - \exp \left[ - \frac { 2 \lambda r _ { n } f _ { H } / h } { M N T _ { g } } \left( 1 - ( 1 - p _ { n } \frac { 1 } { N } ) ^ { x } \right) \right] ,\tag{5}
$$

and multiple access capacity

$$
C _ { U A - R F D M } = \lambda \exp \left[ - 2 \lambda d _ { i , m a x } \frac { f _ { H } / h } { T _ { g } M } \right] ,\tag{6}
$$

conditioned on the number of targets seen by each radar is <sup>x</sup>.

Proof: Under RFDM, we have $\begin{array} { r } { \operatorname* { P r } [ F _ { k , 0 } ^ { 1 } ] = \frac { 1 } { M } } \end{array}$ . As radar topology is homogeneous, we have $\begin{array} { r } { \operatorname* { P r } [ R _ { k , 0 } ^ { n ^ { \prime } } ] = \frac { r _ { n } } { d _ { i , m a x } } } \end{array}$ . Under UA, for a fixed $t _ { 0 }$ <sup>i,max</sup>(radar 0’s transmit start instant is known by itself), we have $\begin{array} { r } { \Delta t _ { k , 0 } = t _ { 0 } - t _ { k } \sim U [ - \frac { f _ { H } } { h } , T _ { g } - \frac { f _ { H } } { h } ] } \end{array}$ By the uniform distribution of $\Delta t _ { k , 0 }$ and (3), we have Pr $\begin{array} { r } { \cdot [ G _ { k , 0 } ^ { n } \vert k \in \mathcal { K } _ { 0 } ] = \frac { f _ { H } / h } { N T _ { q } } , \forall n \in \{ 1 , 2 , \dots , N \} } \end{array}$ . This implies <sup>g</sup>that the ghost power is the same for all range bins (more detailed proof was shown in [1]). As each target independently and randomly falls into one of range-velocity bins, $\begin{array} { r } { \mathrm { P r } [ \dot { I _ { k , 0 } ^ { n } } | F _ { k , 0 } ^ { 1 } , R _ { k , 0 } ^ { n } , \dot { G } _ { k , 0 } ^ { n } ] = 1 - ( 1 - p _ { n } \frac { 1 } { N } ) ^ { \bar { x } } } \end{array}$ Thus, $\operatorname* { P r } [ E _ { m d , k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] = \operatorname* { P r } [ F _ { k , 0 } ^ { 1 } , R _ { k , 0 } ^ { n } , G _ { k , 0 } ^ { n } , I _ { k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] =$ $\begin{array} { r } { \frac { r _ { n } f _ { H } / h } { d _ { i , m a x } M N T _ { g } } ( 1 - ( 1 - p _ { n } \frac { 1 } { N } ) ^ { x } ) } \end{array}$ and $\mathrm { P r } [ E _ { f a , k , 0 } | k \in \mathcal { K } _ { 0 } ] =$ $\begin{array} { r } { \operatorname* { P r } [ F _ { k , 0 } ^ { 1 } , \bigcup _ { n = 1 } ^ { \bar { N } } G _ { k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] = \frac { f _ { H } / h } { M T _ { a } } } \end{array}$ . By assumption, the radars in $\kappa _ { 0 }$ <sup>g</sup>independently cause target misdetection and false alarm at radar 0. Thus, $\begin{array} { r l } { \mathrm { P r } [ \bigcup _ { k \in \mathcal { K } _ { 0 } } E _ { m d , k , 0 } ^ { n } \Big | | \mathcal { K } _ { 0 } | = } & { { } } \end{array}$ $\begin{array} { r } { K _ { 0 } ] = 1 - ( 1 - \frac { r _ { n } } { d _ { i . m a x } } \frac { f _ { H } / h } { M N T _ { a } } ( 1 - ( 1 - p _ { n } \frac { 1 } { N } ) ^ { x } ) ) ^ { K _ { 0 } } } \end{array}$ and $\begin{array} { r } { \operatorname* { P r } [ \bigcup _ { k \in { \cal K } _ { 0 } } E _ { f a , k , 0 } \Big | | { \cal K } _ { 0 } | = { \cal K } _ { 0 } ] = 1 - ( 1 - \frac { f _ { H } / h } { M T _ { a } } ) ^ { K _ { 0 } } } \end{array}$ . As the <sup>g</sup>average number of radars falling into radar 0’s interference range is $\mathbb { E } [ | { \cal K } _ { 0 } | ] = 2 \lambda d _ { i , m a x } .$ , we have $| { \cal K } _ { 0 } | = { \cal K } _ { 0 } \sim \mathrm { P o i s } ( 2 \lambda d _ { i , m a x } )$ By Definition 3, we have $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ given in (5), and

$$
\mathrm { P r } \left[ E _ { f a } \right] = 1 - \exp \left[ - 2 \lambda d _ { i , m a x } \frac { f _ { H } / h } { T _ { g } M } \right] .\tag{7}
$$

![](images/e07e5f788b75729fb97fb088ccab18c3d8de1d353cd2044c7a3fb81595115bea.jpg)  
Fig. 15. FMCW radar block diagram under UA-FH.

![](images/e219b1a654ae683da1a6c5a1eaff28243c0862036523191bc671bbc4b385ee04.jpg)

![](images/cb93fee7d41c89ff7a930c34233dffa67a8e3f3751c16f8c6924a604ea590ad0.jpg)

![](images/9b6d489664adfa836791fb2f25729c5c2615b639c0e69c7ee6d37246b3faad97.jpg)  
Fig. 16. PHY layer simulation under UA-FH with the same setup as in Fig. 13.

As the above (5) and (7) are the same for all radar, UA is a fair MAC. By (4) and (7) we have (6). 

The term $\frac { f _ { H } / h } { T _ { g } }$ in (5) and (6) represents the fraction of <sup>g</sup>time that a victim radar can dechirp interference into its IF band within a chirp repetition duration $T _ { g }$ . The term <sup>M</sup> in (6) is due to RFDM, and hence is called the RFDM gain. Under the setup in Table I, we have $r _ { 2 3 0 } = 1 7 0 \mathrm { m } , r _ { 3 6 5 } = 4 3 5 \mathrm { m }$ and $p _ { 2 3 0 } = p _ { 3 6 5 } = 0 . 2 2 1$ for UA-RFDM. Under this setup, we simulate $\operatorname* { P r } [ E _ { m d } ^ { n } ] , n \in \{ 1 , 2 , . . . , N \}$ and $C _ { U A - R F D M }$ in Fig. 23, Fig. 24 and Fig. 25. From Fig. 23, we can see that $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ is very small and increases linearly with λ under the considered setup. Further, $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ increases with <sup>n</sup> as the target power decreases with $n ;  { \operatorname { P r } } [ E _ { m d } ^ { n } ]$ increases with <sup>x</sup> as the probability that targets fall into interference side-lobes increases with <sup>x</sup>. Fig. 24 and Fig. 25 show UA-RFDM achieves poor capacity when λ or $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ is moderately large. For example, when λ = 2 (2 radars/m), the capacity of UA-RFDM is close to 0. The maximum capacity of UA-RFDM $C _ { U A } ^ { * }$ −RFDM is achieved at $\begin{array} { r } { \lambda _ { U A - R F D M } ^ { * } = \frac { 1 } { 2 d _ { i , m a x } } \frac { M T _ { g } } { f _ { H } / h } = 0 . 0 6 6 } \end{array}$ radars/m, and $\begin{array} { r } { C _ { U A - R F D M } ^ { * } = \frac { \lambda _ { U A - R F D M } ^ { * } } { e } = 0 . 0 2 4 \mathrm { r a d a r s / m } . } \end{array}$

Summary of UA-RFDM: UA-RFDM achieves a poor tradeoff between multiple access capacity and probability of target misdetection (see Fig. 25), due to its low multiple access capacity. The key reason for the poor multiple access capacity of UA-RFDM is that each radar’s sub-band choice and chirp’s initial phase are unchanged over a CPI. This makes ghosts appear as targets, and hence cannot be distinguished. Thus, UA-RFDM is not a promising candidate for scaling to high-density vehicular radar scenarios. We next focus on methods that improve the multiple access capacity beyond UA-RFDM.

![](images/60ca421f37db9c1e3f1291a0c9df1d44df78b5e45786753849f4a9854a4cf5f5.jpg)

![](images/08d9274c193427dc2798d43069f6069bdfa4cc6e77b2b8b06eb64dd96bb1060f.jpg)

![](images/3d3c5ed44a73ecfe67c98ffe48d265821f77623bad0b2fde1481a11db6ccacba.jpg)  
Fig. 17. PHY layer simulation under UA-FH with the same setup as in Fig. 14.

![](images/2a83a4e3f6fad9ade3a89a73511dc75e87ee29662e8a46b6a7090aba0f9c98ea.jpg)  
Fig. 18. FMCW radar block diagram under UA-RFDM-PC.

![](images/f989295654f4967a97c55e9f9728aba90055f6036bb81ef89cbffe305d1bca80.jpg)

![](images/195c39918426e0e1f919154e7e237c9dcd76092ab9fe87416b27c8637a3568f4.jpg)

![](images/330d41b8222671098d1f560d4100787ab9aa414a4284d75fc6be40c3236c43dc.jpg)  
Fig. 19. PHY layer simulation under UA-RFDM-PC with the same setup as in Fig. 13 and Fig. 16.

![](images/324706066dd98f3d67ee5db224fb4e7dc3e0ecdb7429787a2dddf98e13524435.jpg)

![](images/583454d790573e41daf776436d291a8b7f3a5e97a38b046c5f9e251886914d3c.jpg)

![](images/ea3ebd69334d92b6643588ee82904c3b62cce9be46026442cecdaa198d60d9b2.jpg)  
Fig. 20. PHY layer simulation under UA-RFDM-PC with the same setup as in Fig. 14 and Fig. 17.

![](images/a16c5b068dcd832173011de64dfaa5de53d7a3c2514cd1adaba8c25d21606a4b.jpg)  
Fig. 21. FMCW radar block diagram under UA-FH-PC.

![](images/c02e3b975d509bf1d38197cf819ee37bf0b13468cdc098ff47d8d5fe3763d5ea.jpg)

![](images/a4897e7c542920a6c832e4483845ec7dab51c79123c69899c3a4e41761b67190.jpg)

![](images/c9d5afa1811edf70fd3e86d4a705a45017ea2dd224faefc597bdc9e33637a326.jpg)  
Fig. 22. PHY layer simulation under UA-FH-PC with the same setup as in Fig. 14, Fig. 17, and Fig. 20.

## V. ANALYSIS OF UA-FH

A potential solution to improve the multiple access capacity is to use UA-FH to distinguish ghosts from targets. The FMCW radar block diagram under UA-FH is shown in Fig. 15. The detect-and-classify block in Fig. 15 counts the appearance of a signal on each range bin over a CPI. The radar conducts velocity

![](images/3fc3ddc7be9fb3f4a8697ab3ec79f015c426dd1b208a7d8e5a338306a99c902a.jpg)  
Fig. 23. Probability of target misdetection versus λ under different range bins.

![](images/eb50ad9fde360cf9c8d16f00bfde0caeeba74aa75acc1f67276a750a06d66382.jpg)  
Fig. 24. Multiple access capacity versus λ.

DFT on a range bin only if the signal on that range bin appears in every chirp cycle (i.e., <sup>L</sup> times) over a CPI. Compared to [10] and [16] which also propose FH, the key novelty in our FH scheme is that we propose to use the random appearance of ghosts caused by FH as a characteristic to distinguish ghosts from targets. When a ghost and target do not fall into the same range bin, the ghost can be distinguished from a target and not putted into velocity DFT with probability $\begin{array} { r } { 1 - \frac { 1 } { M ^ { L } } \approx 1 } \end{array}$ , thereby mitigating false alarm, as verified in Fig. 16. However, when a ghost and a target fall into the same range bin of a victim radar, the persistently appearing target causes the detect-andclassify block to fail. In this case, under the setup in Table I, if the sub-band choice of the interfering radar and the victim radar overlap more than 6% in a CPI, which happens with probability very close to 1, the ghost from the interfering radar can cause false alarm at the victim radar (see Fig. 17). Thus, if $G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n }$ happens, where $H _ { 0 } ^ { n }$ is the event that there exists at least a target at range bin <sup>n</sup> of the victim radar 0, radar <sup>k</sup>’s ghost at range bin <sup>n</sup> causes false alarm at radar 0. Hence, conditioned on $k \in \mathcal { K } _ { 0 }$ $\begin{array} { r } { E _ { f a , k , 0 } = \bigcup _ { n = 1 } ^ { N } ( G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n } ) } \end{array}$

![](images/886967cf5baad87e4bf6fae129ad40cae0d5d7fb90bd98e49d5bd50a4bf105aa.jpg)  
Fig. 25. Multiple access capacity versus probability of target misdetection at range bin 230 (at around half of the maximum detectable range).

Our simulations find that when a high-power ghost and a target fall into the same range bin, the target may be mis-detected on range-velocity bins due to the noise floor elevation caused by the randomly appearing interference as shown in Fig. 17. This happens with a high probability when the ghost is strong enough. Then, conditioned on $k \in \mathcal { K } _ { 0 }$ , we model $E _ { m d , k , 0 } ^ { n } =$ $R _ { k , 0 } ^ { n } \cap G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n }$ , where $R _ { k , 0 } ^ { n }$ is the event that the range $d _ { k , 0 }$ between radar <sup>k</sup> and radar 0 is smaller than a threshold $r _ { n }$ . Focus on analyzing the performance of a reference victim radar 0, we have the following result.

Proposition 2 (PHY and MAC Layer Properties of UA-FH): UA-FH is a fair MAC with target misdetection probability at range bin <sup>n</sup>

$$
\mathrm { P r } \left[ E _ { m d } ^ { n } \right] = 1 - \exp \left[ - \frac { 2 \lambda r _ { n } f _ { H } / h } { N T _ { g } } \left( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } \right) \right] ,\tag{8}
$$

and multiple access capacity

$$
C _ { U A - F H } = \lambda \exp \left[ - 2 \lambda d _ { i , m a x } \frac { f _ { H } / h } { T _ { g } \left( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } \right) ^ { - 1 } } \right] ,\tag{9}
$$

conditioned on the number of targets seen by each radar is <sup>x</sup>.

Proof: As each target independently and randomly falls into radar’s range-velocity bins, $\begin{array} { r } { \operatorname* { P r } [ H _ { 0 } ^ { n } ] = 1 - ( 1 - \frac { 1 } { N } ) ^ { x } } \end{array}$ As each ghost can only fall into one range bin, we have $\begin{array} { r } { \operatorname* { P r } [ E _ { f a , k , 0 } | k \in \mathcal { K } _ { 0 } ] = \operatorname* { P r } [ \bigcup _ { n = 1 } ^ { N } ( G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n } ) | k \in \mathcal { K } _ { 0 } ] = } \end{array}$ $\begin{array} { r } { \sum _ { n = 1 } ^ { N } \operatorname* { P r } [ G _ { k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] \operatorname* { P r } [ H _ { 0 } ^ { n } ] = \frac { f _ { H } / h } { T _ { a } } ( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } ) } \end{array}$ Also, by proof of Proposition 1, $\begin{array} { r } { \operatorname* { P r } [ R _ { k , 0 } ^ { n } ] = \frac { r _ { n } } { d _ { i , m a x } } } \end{array}$ . Thus, $\begin{array} { r } { \operatorname* { P r } [ E _ { m d , k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] = \frac { r _ { 0 } } { d _ { i . m a x } } \frac { f _ { H } / h } { N T _ { o } } ( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } ) } \end{array}$ Then, <sup>i,max g</sup>using the similar steps as the proof of Proposition 1, we arrive at (8) and (9). 

The term $\begin{array} { r } { ( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } ) ^ { - 1 } } \end{array}$ in (9) can be regarded as the FH gain that must be weighed against the loss of RFDM gain <sup>M</sup>, when compared with (6) for UA-RFDM. When the number of targets $\begin{array} { r } { x < \frac { \ln ( 1 - 1 / M ) } { \ln ( 1 - 1 / N ) } } \end{array}$ , we have $( 1 - ( 1 - { \textstyle { \frac { 1 } { N } } } ) ^ { x } ) ^ { - 1 } > M ,$ and in this case, $\dot { C } _ { U A - F H } > C _ { U A - R F D M }$ . For example, under the setup in Table I, $C _ { U A - F H } > C _ { U A - R F D M } { \mathrm { ~ i f ~ } } x < 3 1 2$ As this happens in most cases, when <sup>x</sup> is small to moderate $( \mathrm { e } . \mathrm { g } . , \ x < 5 0 )$ , we have $( 1 - ( 1 - \textstyle { \frac { 1 } { N } } ) ^ { x } ) ^ { - 1 } \gg M$ , and hence $C _ { U A - F H } \gg C _ { U A }$ <sub>RFDM</sub>. However, when $\begin{array} { r } { x > \frac { \ln ( 1 - 1 / M ) } { \ln ( 1 - 1 / N ) } } \end{array}$ , we have $C _ { U A - F H } < C _ { U A - R F D M }$ . Thus, when the number of targets seen by each radar is not very large, the UA-FH capacity is larger than UA-RFDM capacity, and vice versa. Under the setup in Table I, we have $r _ { 2 3 0 } = 1 0 0$ m and $r _ { 3 6 5 } = 2 6 5$ m for UA-FH. Under this setup, we simulate $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ $n \in$ $\{ 1 , 2 , \ldots , N \}$ and $C _ { U A - F H }$ in Fig. 23, Fig. 24 and Fig. 25. From Fig. 23, we can see that $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ of UA-FH is larger than $\operatorname { P r } [ E _ { m d } ^ { n } ]$ of UA-RFDM. However, $\operatorname { P r } [ E _ { m d } ^ { n } ]$ of UA-FH is in general small, and increases linearly with λ under the considered setup. From Fig. 24 and Fig. 25, we see that $C _ { U A - F H }$ is much larger than $C _ { U A - R F D M }$ for all the considered <sup>x,</sup> λ and most region of $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ . The maximum capacity of UA-FH $C _ { U A - F H } ^ { * }$ is achieved at $\begin{array} { r } { \lambda _ { U A - F H } ^ { * } = \frac { 1 } { 2 d _ { i , m a x } } \frac { T _ { g } } { f _ { H } / h } \frac { 1 } { 1 - ( 1 - \frac { 1 } { N } ) ^ { x } } . } \end{array}$ and $\begin{array} { r } { C _ { U A - F H } ^ { * } = \frac { \lambda _ { U A - F H } ^ { * } } { e } } \end{array}$ , which is shown in Fig. 24 under different <sup>x</sup>.

Summary of UA-FH: FH helps each radar to distinguish targets and ghosts on range bins. The target misdetection and false alarm happen only when the target and ghosts fall into the same range bin. Compared with UA-RFDM, UA-FH obtains FH gain at the cost of losing RFDM gain. When the number of targets seen by each radar is not very large, the capacity of UA-FH is much larger than the capacity of UA-RFDM. The target misdetection probabilities of UA-FH are larger than those of UA-RFDM, but in most regions, UA-FH achieves better tradeoffs between multiple access capacity and target misdetection probability.

## VI. ANALYSIS OF UA-RFDM-PC

The second solution to improve UA-RFDM is to randomize the phases of the ghosts across the <sup>L</sup> chirp cycles, realized by UA-RFDM-PC. The FMCW radar block diagram under UA-RFDM-PC is shown in Fig. 18. After phase decoding, the additional phase rotations on a typical radar 0’s target signals are 0, while the additional phase rotations of radar <sup>k</sup>’s ghosts are random. After velocity DFT, the ghost is spread as pseudo-noise into radar 0’s velocity bins, due to its random phase in a CPI. This is verified in Fig. 19 and Fig. 20.

Our simulations find that the pseudo-noise on any range bin can occasionally cause false alarm; an example is shown in Fig. 19. Also, when the number of ghosts in a range bins is smaller than 4 (holds with high probability under the considered setup), the probability of false alarm caused by the ghost-spread pseudo-noise is insensitive to the ghost power and the range bin that the ghost falls into. Thus, we denote $J _ { k , 0 }$ as the event that radar $k ' \mathrm { s }$ ghost-spread pseudo-noise causes false alarm at radar 0, which happens with probability $p _ { 0 }$ . Then, conditioned on $k \in \mathcal { K } _ { 0 }$ , we model that $E _ { f a , k , 0 } = F _ { k , 0 } ^ { 1 } \cap ( \bigcup _ { n = 1 } ^ { N } G _ { k , 0 } ^ { n } ) \cap J _ { k , 0 } .$ Furthermore, when a high-power ghost and a target fall into the same range bin of the victim radar, the target can be mis-detected due to the high-power pseudo-noise, as shown in Fig. 20. This happens with high probability when the ghost is strong enough. As in Section V, for $k \in \mathcal { K } _ { 0 }$ , we model $E _ { m d , k , 0 } ^ { n } = R _ { k , 0 } ^ { n } \cap F _ { k , 0 } ^ { 1 } \cap G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n }$ , where $R _ { k , 0 } ^ { n }$ denotes the event that the range between radar <sup>k</sup> and radar 0 is smaller than a threshold $r _ { n }$ , and $H _ { 0 } ^ { n }$ denotes the event that there exists at least a target falls into the range bin <sup>n</sup> of radar 0. Then, we have the following result.

Proposition 3 (PHY and MAC Layer Properties of UA-RFDM-PC): UA-RFDM-PC is a fair MAC with target misdetection probability at range bin <sup>n</sup>

$$
\mathrm { P r } \left[ E _ { m d } ^ { n } \right] = 1 - \exp \left[ \frac { - 2 \lambda r _ { n } f _ { H } / h } { M N T _ { g } } \left( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } \right) \right] ,\tag{10}
$$

and multiple access capacity

$$
C _ { U A - R F D M - P C } = \lambda \exp \left[ - 2 \lambda d _ { i , m a x } \frac { f _ { H } / h } { T _ { g } M p _ { 0 } ^ { - 1 } } \right] ,\tag{11}
$$

conditioned on the number of targets seen by each radar is <sup>x</sup>. Proof: By proof of Propositions 1 and 2, we have $\begin{array} { r } { \operatorname* { P r } [ R _ { k , 0 } ^ { n } ] = \frac { \hat { r _ { n } } } { d _ { i , m a x } } , \operatorname* { P r } [ F _ { k , 0 } ^ { 1 } ] = \frac { 1 } { M } , \qquad \operatorname* { P r } [ G _ { k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] = } \end{array}$ $\frac { f _ { H } / h } { N T _ { g } }$ $\mathsf { \Omega } _ { \tau } ^ { h } , \quad \forall n \in \{ 1 , 2 , \ldots , N \}$ , and $\begin{array} { r } { \operatorname* { P r } [ H _ { 0 } ^ { n } ] = 1 - ( 1 - \frac { 1 } { N } ) ^ { x } } \end{array}$ <sup>g</sup>We also have $\mathrm { P r } [ J _ { k , 0 } ] = p _ { 0 }$ . Thus, $\operatorname* { P r } [ E _ { m d , k , 0 } ^ { n } | k \in K _ { 0 } ] =$ $\begin{array} { r } { \frac { r _ { 0 } } { d _ { i , m a x } } \frac { f _ { H } / h } { M N T _ { g } } ( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } ) , \mathrm { P r } [ E _ { f a , k , 0 } | k \in \mathcal { K } _ { 0 } ] = \frac { f _ { H } / h } { M T _ { g } } p _ { 0 } . } \end{array}$ <sup>i,max g g</sup>Then, using the similar steps as the proof of Proposition 1, we arrive at (10) and (11). 

The term $p _ { 0 } ^ { - 1 }$ in (11) can be regarded as the PC gain. Since UA-RFDM-PC also keeps the RFDM gain <sup>M</sup>, it follows that $C _ { U A - R F D M - P C } \gg C _ { U A - R F D M }$ . Under the setup in Table I, we have $p _ { 0 } = 0 . 0 3 3 , \ r _ { 2 3 0 } = 1 3 0$ m and $r _ { 3 6 5 } =$ 265 m for UA-RFDM-PC. Under this setup, we simulate $\operatorname* { P r } [ E _ { m d } ^ { n } ] , n \in \{ 1 , 2 , \ldots , N \}$ and $C _ { U A - R F D M - P C }$ in Fig. 23, Fig. 24 and Fig. 25. From Fig. 23, we can see that $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ of UA-RFDM-PC is smaller than that of UA-FH, but is larger than that of UA-RFDM. From Fig. 24 and Fig. 25, we see that $C _ { U A - R F D M - P C }$ is much larger than $C _ { U A }$ −RFDM for all the considered $x , \lambda$ and most region of $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ The maximum capacity of UA-RFDM-PC $C _ { U A - R F D M - P C } ^ { * }$ is achieved at $\begin{array} { r } { \lambda _ { U A - R F D M - P C } ^ { * } = \frac { 1 } { 2 d _ { i , m a x } } \frac { M T _ { g } } { f _ { H } / h } \frac { 1 } { p _ { 0 } } = 2 } \end{array}$ radars/m, and $\begin{array} { r } { C _ { U A - R F D M - P C } ^ { * } = \frac { \lambda _ { U A - R F D M - P C } ^ { * } } { e } = 0 . 7 3 6 ~ \mathrm { r a d a r s / m } } \end{array}$

Summary of UA-RFDM-PC: UA-RFDM-PC adopts PC to help each radar to distinguish targets and interference on range-velocity bins. Target misdetection happens only when the target and ghosts fall into the same range bin. False alarm occasionally happens when a ghost falls into any range bin. Compared with UA-RFDM, UA-RFDM-PC keeps RFDM gain and has an additional PC gain, which makes the capacity of UA-RFDM-PC much larger than the capacity of UA-RFDM. The target misdetection probability of UA-RFDM-PC is better than that of UA-FH under the setup in Table I.

## VII. ANALYSIS OF UA-FH-PC

The third solution to improve multiple access capacity is using UA-FH-PC; the corresponding FMCW receiver block diagram is shown in Fig. 21.

Due to FH, when a ghost and target do not fall into the same range bin, the ghost can be distinguished from a target with probability $\begin{array} { r } { 1 - \frac { 1 } { M ^ { L } } \approx 1 } \end{array}$ and not passed into velocity DFT to avoid a false alarm. But when a ghost and a target fall into the same range bin of a victim radar, the persistently appearing target causes the detect-and-classify block to fail. However, with PC, the non-classified ghost is spread into pseudo-noise (see Fig. 22) that only infrequently causes a false alarm. As in Section VII, when the number of ghosts in a range bins is smaller than 4 (holds with high probability under the considered setup), the probability of false alarm caused by the ghost-spread pseudonoise is insensitive to the ghost power and the range bin that the ghost falls into. Thus, we denote $J _ { k , 0 }$ as the event that radar <sup>k</sup>’s ghost-spread pseudo-noise causes false alarm at radar 0, which happens with probability $p _ { 0 }$ . Then, conditioned on $k \in \mathcal { K } _ { 0 }$ , we model that $\begin{array} { r } { E _ { f a , k , 0 } = \bigcup _ { n = 1 } ^ { N } ( G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n } ) \cap J _ { k , 0 } } \end{array}$ , where $G _ { k , 0 } ^ { n }$ is the time condition that radar <sup>k</sup>’s ghost falls into radar 0’s range bin $n ,$ and $H _ { 0 } ^ { n }$ denotes the event that there exists at least a target falls into the range bin <sup>n</sup> of radar 0. As in Section V and Section VII, when a strong enough ghost and a target fall into the same range bin of the victim radar, the target can be mis-detected with high probability due to the high-power pseudo-noise. Thus, for $k \in \mathcal { K } _ { 0 }$ , we model $E _ { m d , k , 0 } ^ { n } = R _ { k , 0 } ^ { n } \cap G _ { k , 0 } ^ { n } \cap H _ { 0 } ^ { n }$ , where $R _ { k , 0 } ^ { n }$ denotes the event that the range between radar <sup>k</sup> and radar 0 is smaller than a threshold $r _ { n }$ . Then, we have the following result.

Proposition 4 (PHY and MAC Layer Properties of UA-FH-PC): UA-FH-PC is a fair MAC with target misdetection probability at range bin <sup>n</sup>

$$
\mathrm { P r } \left[ E _ { m d } ^ { n } \right] = 1 - \exp \left[ \frac { - 2 \lambda r _ { n } f _ { H } / h } { N T _ { g } } \left( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } \right) \right] ,\tag{12}
$$

and multiple access capacity

$$
C _ { U A - F H - P C }
$$

$$
= \lambda \exp \left[ - 2 \lambda d _ { i , m a x } \frac { f _ { H } / h } { T _ { g } p _ { 0 } ^ { - 1 } \left( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } \right) ^ { - 1 } } \right] ,\tag{13}
$$

conditioned on the number of targets seen by each radar is <sup>x</sup>.

Proof: The proof of (12) is similar to the proof of (8) in Proposition 2. By proof of Propositions 3, we have $\begin{array} { r } { \operatorname* { P r } [ G _ { k , 0 } ^ { n } | k \in \mathcal { K } _ { 0 } ] = \frac { f _ { H } / h } { N T _ { g } } , \forall n \in \{ 1 , 2 , \ldots , N \} , \operatorname* { P r } [ J _ { k , 0 } ] = p _ { 0 } } \end{array}$ and $\begin{array} { r } { \operatorname* { P r } [ H _ { 0 } ^ { n } ] = 1 - ( 1 - \frac { 1 } { N } ) ^ { x } } \end{array}$ . Thus, $\mathrm { P r } [ E _ { f a , k , 0 } | k \in \mathcal { K } _ { 0 } ] =$ $\begin{array} { r } { \frac { f _ { H } / h } { T _ { g } } p _ { 0 } \big ( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } \big ) } \end{array}$ . Then, using the similar steps as the proof of Proposition 1, we arrive at (13). 厂

Under the setup in Table I, when <sup>x</sup> is small to moderate (e.g., $x < 5 0 )$ , the FH gain $\begin{array} { r } { ( 1 - ( 1 - \frac { 1 } { N } ) ^ { x } ) ^ { - 1 } } \end{array}$ is much larger than the RFDM gain <sup>M</sup>, and hence $C _ { U A - F H - P C } \gg C _ { U A - R F D M - P C }$ Compared to UA-FH, UA-FH-PC has an additional PC gain $p _ { 0 } ^ { - 1 }$ and hence $C _ { U A - F H - P C } \gg C _ { U A - F H }$ . For the system scenario in Table I, we further have $r _ { 2 3 0 } = 8 5$ m and $r _ { 3 6 5 } = 2 0 0$ m for UA-FH-PC, which are smaller than those of UA-RFDM-PC, as FH reduces the ghost-spread pseudo-noise power. Our PHY layer simulation finds that $p _ { 0 } = 0 . 0 3$ . Based on these, we simulated $\operatorname* { P r } [ E _ { m d } ^ { n } ] , n \in \{ 1 , 2 , \ldots , N \}$ and $C _ { U A - F H - P C }$ in Fig. 23, Fig. 24 and Fig. 25. From Fig. 23, we see that $\operatorname* { P r } [ E _ { m d } ^ { n } ]$ of UA-FH-PC is smaller than that of UA-FH, but larger than that for UA-RFDM-PC and UA-RFDM. From Fig. 24 and Fig. 25, we see that the capacity of UA-FH-PC is achieves the largest capacity for all the considered $x , \lambda$ and most region of $\operatorname { P r } [ E _ { m d } ^ { n } ]$ . The maximum capacity of $\mathrm { U A - F H - P C } \ C _ { U A - F H - P C } ^ { * }$ is achieved at $\begin{array} { r } { \lambda _ { U A - F H - P C } ^ { * } = \frac { 1 } { 2 d _ { i , m a x } } \frac { T _ { g } } { p _ { 0 } f _ { H } / h } \frac { 1 } { 1 - ( 1 - \frac { 1 } { N } ) ^ { x } } } \end{array}$ , and $\begin{array} { r } { C _ { U A - F H - P C } ^ { * } = \frac { \lambda _ { U A - F H - P C } ^ { * } } { e } } \end{array}$ , which is large. For example, when $x = 1 0$ , we have $C _ { U A - F H - P C } ^ { * } = 1 8 . 3 9 3$ radars/m achieved at density $\lambda _ { U A - F H - P C } ^ { * } = 4 9 . 9 9 7$ radars/m.

TABLE II  
SUMMARY OF 4 CONSIDERED MACS
<table><tr><td rowspan=1 colspan=1>MACs</td><td rowspan=1 colspan=1>Prob. of targetmisdetection</td><td rowspan=1 colspan=1>Capacitygain</td><td rowspan=1 colspan=1>Multiple accesscapacity</td></tr><tr><td rowspan=1 colspan=1>UA-RFDM</td><td rowspan=1 colspan=1>Very low</td><td rowspan=1 colspan=1>RFDM</td><td rowspan=1 colspan=1>Very small</td></tr><tr><td rowspan=1 colspan=1>UA-FH</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>FH</td><td rowspan=1 colspan=1>Moderate</td></tr><tr><td rowspan=1 colspan=1>UA-RFDM-PC</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>RFDM &amp; PC</td><td rowspan=1 colspan=1>Moderate</td></tr><tr><td rowspan=1 colspan=1>UA-FH-PC</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>FH &amp; PC</td><td rowspan=1 colspan=1>Large</td></tr></table>

We finally compare capacities of the considered four distributed MAC schemes with the capacity of the state-of-the-art synchronous cooperative MAC scheme - RadChat [12]. Rad-Chat uses time division multiple access (TDMA) for mitigating the radar interference. By [12], the upper bound of the maximum number of non-false-alarmed radar is $\frac { M B _ { c } } { f _ { H } + d _ { i , m a x } h / c } .$ <sup>H i,max</sup>Thus, the upper bound of the capacity of RadChat is $\frac { M B _ { c } } { 2 ( f _ { H } + d _ { i , m a x } h / c ) d _ { i , m a x } }$ . Since it’s not clear in [12] how RadChat <sup>H i,max i,max</sup>handles the case when radar density is larger than this upper bound, we assume the capacity upper bound of RadChat satu-MB   
rates at $\frac { \iota n \iota _ { C } } { 2 ( f _ { H } + d _ { i , m a x } h / c ) d _ { i , m a x } }$ after reaching this value, and do not calculate the probability of target misdetection of RadChat. Under the setup in Table I, the capacity upper bound of RadChat is 0.011 radars per meter, which is plotted in Fig. 24. The capacities of UA-FH, UA-RFDM-PC and UA-FH-PC are significantly larger than the capacity of RadChat. This indicates that 1) orthogonal TDMA scheduling may not achieve desired scaling of multiple access capacity; 2) it is possible to design radar MAC schemes with large multiple access capacity even without synchronization and coordination, by using detect-and-classify approaches such as FH and PC. These results can serve as potential guides to any future radar standardization activities.

Summary of UA-FH-PC: UA-FH-PC adopts both FH and PC to help each radar to distinguish targets and interference on range-velocity bins. The target misdetection and false alarm happen only when the target and ghosts fall into the same range bin. UA-FH-PC has FH gain and PC gain that can be multiplied together to achieve significant capacity gain. This makes the capacity of UA-FH-PC much larger than the capacities of UA-RFDM, UA-FH and UA-RFDM-PC. The target misdetection probabilities of UA-FH-PC is better than UA-FH, but worse than UA-RFDM-PC and UA-RFDM.

## VIII. CONCLUSION

In this paper, we considered four distributed radar MACs – UA-RFDM, UA-FH, UA-RFDM-PC and UA-FH-PC, which can operate without time synchronization, coordination, and control overhead. The interference mitigation principle and interference model for each MAC were provided based on extensive PHY layer simulations. We analyzed the four MACs using target misdetection probabilities and multiple access capacities proposed in this work. We summarize their respective performance in Table II. Significant new insights are revealed from our simulations and analysis. First, different from the interference probability analysis in [7], [8], our multiple access capacity analysis shows that coherent interference under UA-RFDM can lead to a very low multiple access capacity. In addition, orthogonal TDMA scheduling may also not achieve a large multiple access capacity. Finally, detect-and-classify schemes, such as FH and PC, significantly increase multiple access capacity and achieve good trade-offs between multiple access capacity and probability of target misdetection.

## REFERENCES

[1] S. Jin and S. Roy, “Cross-layer interference modeling and performance analysis in FMCW radar multiple access network,” in Proc. IEEE 92nd Veh. Technol. Conf., 2020, pp. 1–6.

[2] S. M. Patole, M. Torlak, D. Wang, and M. Ali, “Automotive radars: A review of signal processing techniques,” IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[3] K. Ramasubramanian, “mmWave radar for automotive and industrial applications,” Texas Instrument, Dallas, TX, USA, 2017.

[4] C. Aydogdu et al., “Radar interference mitigation for automated driving: Exploring proactive strategies,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 72–84, Jul. 2020.

[5] I. Bilik, O. Longman, S. Villeval, and J. Tabrikian, “The rise of radar for autonomous vehicles: Signal processing solutions and future research directions,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 20–31, Sep. 2019.

[6] S. Sun, A. P. Petropulu, and H. V. Poor, “MIMO radar for advanced driverassistance systems and autonomous driving: Advantages and challenges,” IEEE Signal Process. Mag., vol. 37, no. 4, pp. 98–117, Jul. 2020.

[7] S. Rao and A. V. Mani, “Interference characterization in FMCW radars,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[8] Z. Yang and A. Mani, “Interference mitigation for AWR/IWR devices,” Texas Instrument, Dallas, TX, USA, 2020.

[9] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[10] T. Luo, C. E. Wu, and Y. E. Chen, “A 77-ghz CMOS automotive radar transceiver with anti-interference function,” IEEE Trans. Circuits Syst. I Regular Papers, vol. 60, no. 12, pp. 3247–3255, Dec. 2013.

[11] B. Tang, W. Huang, and J. Li, “Slow-time coding for mutual interference mitigation,” in Proc. IEEE Int. Conf. Acoust., Speech Signal Process., 2018, pp. 6508–6512.

[12] C. Aydogdu, M. F. Keskin, N. Garcia, H. Wymeersch, and D. W. Bliss, “RadChat: Spectrum sharing for automotive radar interference mitigation,” IEEE Trans. Intell. Transp. Syst., vol. 22, no. 1, pp. 416–429, Jan. 2021.

[13] J. Khoury, R. Ramanathan, D. McCloskey, R. Smith, and T. Campbell, “Radarmac: Mitigating radar interference in self-driving cars,” in Proc. 13th Annu. IEEE Int. Conf. Sens., Commun. Netw., Jun. 2016, pp. 1–9.

[14] S. Rao, “Introduction to mmWave sensing: FMCW radars,” Texas Instrument, Dallas, TX, USA, 2017.

[15] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 45–59, Sep. 2019.

[16] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: Modulation schemes and interference mitigation,” IEEE Microw. Mag., vol. 20, no. 9, pp. 58–72, Sep. 2019.

[17] G. Hakobyan and B. Yang, “High-performance automotive radar: A review of signal processing algorithms and modulation schemes,” IEEE Signal Process. Mag., vol. 36, no. 5, pp. 32–44, Sep. 2019.

[18] K. U. Mazher, R. W. Heath, K. Gulati, and J. Li, “Automotive radar interference characterization and reduction by partial coordination,” in Proc. IEEE Radar Conf., 2020, pp. 1–6.

[19] V. Dham, “Programming chirp parameters in TI radar devices,” TexasInstrument, Dallas, TX, USA, 2020.

[20] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE Trans. Veh. Technol., vol. 67, no. 9, pp. 8110–8117, Sep. 2018.

[21] A. Al-Hourani, R. J. Evans, S. Kandeepan, B. Moran, and H. Eltom, “Stochastic geometry methods for modeling automotive radar interference,” IEEE Trans. Intell. Transp. Syst., vol. 19, no. 2, pp. 333–344, Feb. 2018.

[22] X. Gao, G. Xing, S. Roy, and H. Liu, “Ramp-CNN: A novel neural network for enhanced automotive radar object recognition,” IEEE Sensors J., vol. 21, no. 4, pp. 5119–5132, Feb. 2021.

[23] J. F. Kurose and K. W. Ross, Computer Networking: A Top-Down Approach, 7th ed. Pearson, Boston, MA, USA, 2016.

[24] K. Fujiwara, H. Yamaoka, T. Onzuka, S. Ozaki, Y. Akita, and Y. Fujinaka, “A simple-structure FMCW radar test system using PLL-Gunn oscillator and fundamental mixer in 79 ghz band,” in Proc. Int. Conf. Radar, 2018, pp. 1–6.

[25] N. Akhtar, S. C. Ergen, and O. Ozkasap, “Vehicle mobility and communication channel models for realistic and efficient highway VANET simulation,” IEEE Trans. Veh. Technol., vol. 64, no. 1, pp. 248–262, Jan. 2015.

[26] S. Jin, “Radar-interference-JSTSP,” GitHub, 2021. [Online]. Available: https://github.com/sianjin/Radar-Interference-JSTSP

![](images/94f19bed0c2c89e2f3f3fbf1ece16ebbfe4e9972409a3aaa09d7556321123870.jpg)  
Sian Jin received the B.E. degree in electrical engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2016. He is currently working toward the Ph.D. degree with the Department of Electrical and Computer Engineering, University of Washington, Seattle, WA, USA. His research interests include radar signal processing, WiFi PHY layer signal processing, array processing, salable network simulator design, channel modeling, and wireless systems building using MATLAB Toolboxes/ns-3.

![](images/9ec6b711a3af9ad77e81175c88ee1c28702844ee3d760b69634a769b1aec193e.jpg)

Sumit Roy (Fellow, IEEE) received the B.Tech. degree in electrical engineering from the Indian Institute of Technology Kanpur, Kanpur, India, in 1983, the M.A. degree in statistics and applied probability in 1988, and the M.S. and Ph.D. degrees in electrical engineering from the University of California Santa Barbara, Santa Barbara, CA, USA, in 1985 and 1988, respectively. He is currently a Professor of electrical and computer engineering, appointed to a term Distinguished Professorship for integrated systems. His research interests include next-gen WLANs and

cellular networks, spectrum sharing, and vehicular and sensor networking. He was an IEEE ComSoc Distinguished Lecturer and an Associate Editor for all major ComSoc journals. He is currently on the Executive Committee of National Spectrum Consortium dedicated to efficient spectrum sharing between Federal licensed and civilian sectors. He was elevated to IEEE Fellow by Communications Society in 2007 for contributions to multiuser communications theory and cross-layer design of wireless networking standards.