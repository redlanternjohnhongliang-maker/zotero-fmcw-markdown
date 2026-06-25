# Decentralized Automotive Radar Spectrum Allocation to Avoid Mutual Interference Using Reinforcement Learning

Pengfei Liu, Yimin Liu<sup>\*</sup>, Member, IEEE, Tianyao Huang, Yuxiang Lu, and Xiqin Wang

<sup>Abstract</sup>—Nowadays, mutual interference among automotive radars has become a problem of wide concern. In this paper, a decentralized spectrum allocation approach is presented to avoid mutual interference among automotive radars. Although decentralized spectrum allocation has been extensively studied in cognitive radio sensor networks, two challenges are observed for automotive sensors using radar. First, the allocation approach should be dynamic as all radars are mounted on moving vehicles. Second, each radar does not communicate with the others so it has quite limited information. A machine learning technique, reinforcement learning, is utilized because it can learn a decision making policy in an unknown dynamic environment. As a single radar observation is incomplete, a long short-term memory recurrent network is used to aggregate radar observations through time so that each radar can learn to choose a frequency subband by combining both the present and past observations. Simulation experiments are conducted to compare the proposed approach with other common spectrum allocation methods such as the random and myopic policy, indicating that our approach outperforms the others.

<sup>Index</sup> <sup>Terms</sup>—automotive radar, interference, spectrum allocation, reinforcement learning

## I. INTRODUCTION

The pursuit of safe and comfortable driving has recently given rise to the advance of self-driving technologies, such as adaptive cruise control and collision warning. Automotive radar, as one of the most important sensors on vehicles, is vastly popularized. In most countries, the frequency range of 76-77 GHz is allocated to automotive usage [1]. As the population and bandwidth demand of automotive radars are both on the rise, mutual interference becomes a problem of wide concern.

Frequency modulated continuous wave (FMCW) is widely employed in automotive radar due to its low hardware complexity [2]. The consequences of mutual interference among FMCW radars have been investigated in [1, 3–6]. The probability of ghost targets is raised if an FMCW radar is interfered by another with the same chirp rate [1, 3, 4]. To prevent ghost targets, it is proposed in [5] to use random chirp rates so that interference causes a rise in the noise level. Such interference is referred to as non-coherent interference in [6].

The MOSARIM project also concluded that the most probable consequence of real-world automotive radar interference was an increase in receiver noise which might cover targets [7].

Current solutions to mitigating automotive radar interference can be grouped into two categories, interference canceling and interference avoidance. Interference canceling techniques are usually applied in the radar receiver to suppress interference in time [8], frequency [9] and time-frequency domain [10]. For example, in [8], the interference signal is first reconstructed in time domain by parameter estimation and then subtracted from the received signal. In [9], a minimum operation is performed on a set of chirps in the frequency domain to suppress noise-like interference. In [10], an algorithm is proposed to locate and then eliminate the samples contaminated by interference in time-frequency domain. Interference avoidance is to coordinate transmission in time, frequency and space domain to prevent interference from occurring [11]. A representative interference avoidance method in the frequency domain is spectrum allocation. For example, in [12], an allocation scheme is described in which the whole band is equally divided into several non-overlapping subbands. The bandwidth of each subband is determined by the resolution requirement. Then, radars are assigned to different subbands so they do not interfere with each other. However, the interference is inevitable when radars outnumber subbands. In [13], a centralized spectrum allocation approach is proposed. Each radar sends information including its own position and velocity to a control center, which computes the allocation results and then broadcasts them to each radar. However, it increases extra communication cost. By contrast, in decentralized allocation, each radar chooses their frequency subbands in an autonomous way. A straightforward method is to choose at random [13], which is easy to implement but the mitigation of interference is limited.

In this paper, we present an interference avoidance approach for FMCW automotive radar by decentralized spectrum allocation. In our approach, like [12], we also assume that the whole band is equally divided into several non-overlapping subbands, given the resolution or bandwidth requirement. Moreover, we consider the cases where radars outnumber subbands. Based on the premise above, we propose a decentralized spectrum allocation approach in which each radar chooses a subband separately to reduce the mutual interference. Although decentralized spectrum allocation has been extensively studied in cognitive radio sensor networks, two challenges are observed for automotive sensors using radar. First, the allocation approach should be dynamic as all radars are mounted on moving vehicles. Second, each radar does not communicate with the others so it has quite limited information. In light of these challenges, a machine learning technique, reinforcement learning (RL), is employed on each radar since RL can learn a decision making policy in an unknown dynamic environment. Moreover, a long short-term memory (LSTM) recurrent network is utilized to aggregate observations through time so that radar can learn to choose a subband by combining both the present and past observations.

The proposed approach to solve automotive radar interference problem, in a broad sense, lies in the realm of spectrum sharing, which was first proposed in the field of communication to accommodate more radio frequency services and avoid mutual interference. More recently, spectrum sharing techniques have been explored extensively in radars so that they can share the scarce spectrum with both communication and other radar systems. In these techniques, two categories are reviewed in this paper. One is the co-design of the waveform for both radar and communication [14]. In [14], several metrics are considered to evaluate the shared waveform, such as spectral efficiency for communication and estimation performance for radar. The other category is the coexistence [15, 16], in which radar first uses spectrum sensing to obtain the occupancy of the whole band and then chooses proper subbands by solving an optimization problem. In [15], considering that a wide band needs to be sensed, a compressed sampling technique is proposed to reduce the sampling and processing requirements. In [16], because the optimization to improve the signal-to-interference plus noise ratio is at high computational cost, a bioinspired filtering technique is proposed to reduce the computational complexity. Although we also present an approach to achieve the coexistence of multiple automotive radars, our work differs from [15, 16] in that an extra spectrum sensing receiver is not required. Radar only needs its own receiver to estimate the interference power within the subband on which it transmits.

With the proposing of cognitive radar [17], in some researches such as [18, 19], it is indicated that cognitive approaches can be used to reduce the interference between radar and other radio frequency systems. In terms of spectrum sharing, radar cognition includes observation of the spectral environment and decision-making for the transmission [19]. In recent years, RL, which is a machine learning method for decision-making, has been adopted in radar spectrum sharing problems. For example, in [20], deep Q-learning, which is an RL approach combined with deep neural networks, is utilized so that radar learns to choose subbands to avoid the interference from a communication system. Like [15, 16], in [20], radar also needs to observe the occupancy of all subbands while deciding the transmitting subband. Whereas, in this paper, each radar only observes the subband on which it transmits by estimating the received interference power. Moreover, recurrent neural networks are adopted to aggregate radar observations through time so that radar can learn to choose a subband by combining the current and past observations. However, in [20], a fully connected network is used and radar chooses a subband based on only a single observation.

Beside the fields of spectrum sharing, RL has also been successfully applied to other cognitive radar applications, such as cognitive electronic warfare [21, 22] and waveform optimization [23]. However, only a single radar is considered in these researches. In this work, we investigate a multi-radar interference avoiding problem in which each automotive radar cognitively changes subbands according to their observations.

In communication, the multi-user interference problem has also been investigated using RL. In [24–28], a dynamic channel/subband access policy is learned so that each user can avoid colliding into the same channel/subband with others. In these researches, users are assumed to be static. Whereas, in our problem, radars are mounted on moving vehicles, so the radio environment changes with the positions of radars. To cope with such situation, we first address how radar acquires the position-related observations, which include not only the detected distance of other radars, but also the estimated interference power, which decreases with the distance. Then, we show how radar exploits these observations to choose a proper subband.

To sum up, the main contributions of this paper are listed as follows.

• A decentralized spectrum allocation approach for automotive radar is proposed using RL. Each radar learns to choose a subband to avoid interference according to its own observations, with almost no communication required.

• The LSTM network is utilized in the RL-based spectrum allocation approach so that radar can learn to choose a subband by combining its current and past observations. Moreover, an algorithm to train the LSTM network in our problem is presented.

• Simulation experiments are conducted to compare the proposed approach with other common decentralized spectrum allocation methods such as the random and myopic policy, showing that our approach outperforms the others.

The rest of the paper is organized as follows. In Section II, the scenario and signal model are constructed. In Section III, how radar measures the range, velocity and interference is explained. In Section IV, the decentralized spectrum allocation approach using RL with LSTM networks is elaborated. Simulation results and concluding remarks are presented in Section V and VI, respectively.

## II. SCENARIO AND SIGNAL MODEL

## A. Scenario Model

A simplified scenario considered in our problem is shown in Fig. 1, in which cars are traveling in two lanes with different traffic directions. Each car is equipped with one long-range radar on its front and one short range radar on its back. The long-range radar is used to provide a forward-looking view for applications such as adaptive cruise control and collision mitigation systems [29]. The short-range radar is used to detect obstacles for applications such as lane change assistance and assisted parking systems [29].

![](images/5e06da194c3c2aa45dd7f47504fd71ad9f368284885d452cc755566f8b238af3.jpg)  
Fig. 1. Problem scenario.

As is mentioned in the previous section, it is presumed that the whole band is equally divided into M non-overlapping subbands. Suppose there are N cars on a certain section of the road and they are indexed by $1 , 2 , . . . , N$ . In each period, a car chooses a working subband for both the long-range and shortrange radar. The length of a period is T . As radars outnumber subbands, i.e. $N > M$ , more than one radars will inevitably collide into the same subband causing interference. In this paper, we only focus on reducing LRR interference, as SRR interference is usually not a concern [5].

## B. Transmitted Signal Model

In this work, the triangular chirp FMCW waveform [5, 13] is adopted. The transmitted waveform is

$$
s ( t ) = \left\{ \begin{array} { l r } { \exp \left( j \pi \frac { B } { T _ { c } } t ^ { 2 } \right) \exp \left( j 2 \pi f _ { m } t \right) } \\ { \qquad 0 \leq t < T _ { c } } \\ { \exp \left( - j \pi \frac { B } { T _ { c } } ( t - 2 T _ { c } ) ^ { 2 } \right) \exp \left( j 2 \pi f _ { m } t \right) } \\ { \qquad T _ { c } \leq t < 2 T _ { c } } \end{array} \right.\tag{, (1}
$$

where $T _ { c }$ is the chirp interval, B is the chirp bandwidth, and $f _ { m } = f _ { 0 } + m B$ is the carrier frequency for the mth subband. The chirp interval $T _ { c }$ determines the chirp rate $\frac { B } { 2 T _ { c } }$ , since the bandwidth B is constant. For convenience, in (1), we only express the waveform in two chirp intervals. One is the up-chirp whose instantaneous frequency increases with time. The other is the down-chirp whose instantaneous frequency decreases with time. The triangular chirp FMCW waveform used in this paper is illustrated in Fig. 2. For each transmission, radar transmits a train of triangular chirps, which is called a chirp frame. The frame duration is $T _ { f }$ . For each transmission, radar can choose a different subband. The transmission period is T .

In our problem, parameters including the bandwidth $B ,$ frame duration $T _ { f }$ and transmission period T are fixed for all radars. Moreover, radars on different cars use a different chirp interval ${ T _ { c } } ^ { 1 }$ . This practice is to avoid ghost targets, which will be elaborated in III-B. The purpose of our work is to enable each radar to learn to choose a subband for each transmission so that mutual interference can be avoided.

![](images/261483978795a1b1f354318f645f12b67e8e9c07e88b3451274ac3330cd24bff.jpg)  
Fig. 2. Illustration of the triangular chirp FMCW waveform used in this paper. In this figure, radar chooses different subbands for the two transmission periods.

## C. Received Signal Model

The received signal is composed of the target echo, interference and noise:

$$
r ( t ) = e ( t ) + h ( t ) + n ( t ) ,\tag{2}
$$

where $e ( t ) , h ( t )$ and $n ( t )$ denote the echo, interference and noise, respectively.

The echo from a single target is a delayed version of the transmitted signal:

$$
e ( t ) = \sqrt { P _ { S } } \cdot s \left( t - \tau ( t ) \right) ,\tag{3}
$$

where $P _ { S }$ is the received signal power and $\tau ( t )$ the time delay of the target reflection. For an approaching target with relative radial velocity $v ,$

$$
\tau ( t ) = \frac { 2 ( D - v t ) } { c } ,\tag{4}
$$

where $D$ is the target radial distance, v is the target relative radial velocity, and c is the light speed.

Likewise, the received interference signal from another radar with transmitted signal $s ^ { \prime } ( t )$ is

$$
h ( t ) = \sqrt { P _ { I } } \cdot s ^ { \prime } \left( t - \tau ^ { \prime } ( t ) \right) ,\tag{5}
$$

where $P _ { I }$ is the received interference power and $\tau ^ { \prime } ( t )$ the time delay:

$$
\tau ^ { \prime } ( t ) = { \frac { ( D ^ { \prime } - v ^ { \prime } t ) } { c } } ,\tag{6}
$$

where $D ^ { \prime }$ is the the radial distance and $v ^ { \prime }$ is the relative radial velocity of the interfering radar.

The received interference power $P _ { I }$ depends on the relative positions of the two radars. If they are located on different lanes (indicating the interfering radar is a long-range radar),

$$
P _ { I } = \frac { P _ { L } G A _ { e } g } { 4 \pi \left( L ^ { 2 } + d ^ { 2 } \right) } \cdot \left[ p _ { r } \left( \theta \left( d \right) \right) \right] ^ { 2 } ,\tag{7}
$$

where

$P _ { L } \colon$ transmitting power of the long-range radar;

![](images/438f2ea17b04bc32a514d3a27aef834ba761e4e527b5b63fba21ec22e63c2a5c.jpg)  
Fig. 3. Illustration of radar antenna pattern.

$G \colon$ antenna gain;

$A _ { e } \colon$ effective area;

• L: vertical distance between two lanes;

• d: horizontal distance between two radars;

• θ: radiation direction between two radars;

$p _ { r } ( \cdot ) \colon$ : normalized antenna beam pattern;

• g: propagation decaying factor.

In (7), the antenna pattern $p _ { r } ( \cdot )$ is taken into consideration, which indicates that the transmitting or receiving power also depends on the direction from one radar to another. An illustration of the antenna pattern is provided in Fig. 3. The direction can be written as a function of d:

$$
\theta ( d ) = \arctan \left( \frac { L } { d } \right) .\tag{8}
$$

If the two radars are located on the same lane (indicating the interfering radar is a short range radar),

$$
P _ { I } = { \frac { P _ { S } G A _ { e } g } { 4 \pi d ^ { 2 } } } ,\tag{9}
$$

where $P _ { S }$ is the transmitting power of the short-range radar. The antenna pattern is omitted here because the direction is approximately 0.

## III. RADAR MEASUREMENT

## A. Range and Velocity

Range and velocity estimation of FMCW signal has been studied in [5]. In this subsection, we briefly explains how the range and velocity are estimated.

In FMCW signal processing, by mixing the received signal with the transimitted signal, we obtain the intermediate frequency (IF) signal:

$$
r _ { \mathrm { I F } } ( t ) = r ( t ) \cdot \bar { s } ( t ) ,\tag{10}
$$

where $\bar { s } ( t )$ indicates the conjugate of $s ( t )$ . The instantaneous frequency of $r _ { \mathrm { I F } }$ can expressed as

$$
\frac { \partial \phi _ { r _ { \mathrm { I F } } } ( t ) } { \partial t } = \frac { \partial \phi _ { r } ( t ) } { \partial t } - \frac { \partial \phi _ { s } ( t ) } { \partial t } ,\tag{11}
$$

where $\phi _ { * } ( t )$ and $\frac { \partial \phi _ { * } ( t ) } { \partial t }$ are the phase and instantaneous frequency of the signal, respectively. As Fig. 5 shows, the instantaneous frequency difference between the transmitted signal and the target echo, which is referred to as the beat frequency [3], is approximately constant (the mathematical derivation can be found in APPENDIX A). The beat frequencies of the up-chirp and down-chirp can be expressed as [5]

$$
f _ { b } ^ { \uparrow } \approx - \frac { B } { T _ { c } } \cdot \frac { 2 D } { c } + \frac { 2 v } { c } f _ { m }\tag{12}
$$

and

$$
f _ { b } ^ { \downarrow } \approx \frac { B } { T _ { c } } \cdot \frac { 2 D } { c } + \frac { 2 v } { c } f _ { m } ,\tag{13}
$$

respectively. This implies that $r _ { I F } ( t )$ contains sinusoid components with the beat frequencies. Hence, the estimates of $f _ { b } ^ { \uparrow }$ and $f _ { b } ^ { \downarrow }$ can be obtained by analyzing the spectrum

$$
R ( f ) = \mathcal { F } \left\{ \bar { s } ( t ) r ( t ) \right\} ,\tag{14}
$$

where $\mathcal { F }$ represents the Fourier transform. As Fig. 4(a) shows, there appear peaks at the beat frequencies in the spectrum $R ( f )$ . Then, the range and velocity can be calculated according to (12)(13).

## B. Interference

If the working radar and the interfering radar use the same chirp rate, the interference signal $( 5 ) ( 6 )$ has the similar form with the target echo (3)(4) because $s ^ { \prime } ( t ) ~ = ~ s ( t )$ . Hence, the interference also generates constant beat frequencies in a similar way with the target echo:

$$
f _ { b } ^ { \prime \uparrow } \approx - \frac { B } { T _ { c } } \cdot \frac { D ^ { \prime } } { c } + \frac { v ^ { \prime } } { c } f _ { m } ,\tag{15}
$$

and

$$
f _ { b } ^ { \prime \downarrow } \approx \frac { B } { T _ { c } } \cdot \frac { D ^ { \prime } } { c } + \frac { v ^ { \prime } } { c } f _ { m } .\tag{16}
$$

Therefore, additional peaks appear at the frequencies $f _ { b } ^ { \prime \dagger }$ and $f _ { b } ^ { \prime \downarrow }$ in the spectrum $R ( f )$ , resulting in ghost targets, which is shown in Fig. 4(b). To prevent ghost target, it is proposed in [5] that different radars use different chirp rates. In this way, the frequency difference between the interference and the transmitted signal is not constant but sweeps across the subband and the spectrum $H ( f )$ is spread out within the bandwidth instead of causing additional peaks. Hence, it seems that the noise level is elevated, as shown in Fig. 4(c). The detailed mathematical derivation of the raise in the noise level can be found in APPENDIX B.

From (2)(10)(14), we have

$$
R ( f ) = E ( f ) + H ( f ) + N ( f ) ,\tag{17}
$$

where

$$
\begin{array} { r l r } { E ( f ) } & { = } & { \mathcal { F } \left\{ e ( t ) \cdot \bar { s } ( t ) \right\} , } \\ { H ( f ) } & { = } & { \mathcal { F } \left\{ h ( t ) \cdot \bar { s } ( t ) \right\} , } \\ { N ( f ) } & { = } & { \mathcal { F } \left\{ n ( t ) \cdot \bar { s } ( t ) \right\} . } \end{array}
$$

Therefore, when two radars uses different chirp rates, the interference power can be measured by the noise level, which is defined as:

$$
N _ { I } = \int | H ( f ) + N ( f ) | ^ { 2 } d f .\tag{18}
$$

![](images/48aeed7816ff9d9c607f9a942ee7a56d5e41cbf3d4d6357893c2ddf7d17d042a.jpg)  
(a) No interference

![](images/7c7039f2e1354fe3f99dfa8af76591637fd521d50d02c52f09defc3671d85f5f.jpg)  
(b) Ghost targets

![](images/c0ca5b26008001cdaf6efc515eaee0cdafc12ad7950b4e5588e4e8a0f2db2a83.jpg)  
(c) Raised noise level  
Fig. 4. Results of three simulations in which a working radar is (a) not interfered; (b) interfered by another radar with the same chirp rate; (c) interfered by another radar with a different chirp rate. In the simulations, all signals are generated according to the signal models in Subsection II-B and -C. In (a), the received signal contains only the target echo and noise. The parameters of the working radar are: $B = 2 0 0$ MHz, $f _ { m } = 7 6 ~ \mathrm { G H z }$ $T _ { c } = 5 0$ µs, $T _ { f } = 1$ ms. In (b), the received signal contains the target echo, interference and noise. The interfering radar uses the same parameters as the working radar. In (c), the settings are the same as (b) except that the chirp interval of the interfering radar is $T _ { c } ^ { \prime } = \mathrm { \bar { 2 0 } }$ µs.

![](images/360d115952077b4f61f1af9a7054cd5b8439d20ac7f5285b316c032aee4b8635.jpg)  
Fig. 5. The instantaneous frequency of the transmitted signal and the target echo.

The problem is to estimate $N _ { I }$ using the spectrum of the received signal, $R ( f )$ , which contains target echoes as well as the received interference. Some robust estimation techniques have been developed to solve similar problems. For instance, in [31], ordered statistics is used to estimate the clutter power in existence of heterogeneous samples. Likewise, we use ordered statistics to estimate the noise level.

In signal processing, the spectrum $R ( f )$ in (14) is usually obtained by the fast Fourier transform (FFT). This equals sampling $R ( f )$ with a sampling interval $\Delta f ,$ which is determined by the sampling rate and the number of FFT points. Then, we obtain a sequence $\{ R _ { m } \} ( 0 \leq m \leq M _ { f } - 1 )$ , where $M _ { f }$ is the number of FFT points and

$$
R _ { m } = R ( m \Delta f ) .\tag{19}
$$

Then, by sorting the sequence according to decreasing amplitude, we obtain a new sequence $\{ \hat { R } _ { m } \}$

$$
| \hat { R } _ { 0 } | \geq | \hat { R } _ { 1 } | \geq \ldots \geq | \hat { R } _ { M _ { f } - 1 } | ,\tag{20}
$$

where $\hat { R } _ { m }$ is the element in $\{ R _ { m } \}$ with the mth largest amplitude. As explained in Subsection III-A, the power of the target echo mainly concentrate on the peaks of the spectrum $R ( f )$ . Hence, by discarding the greatest K samples, we can obtain an estimate of the noise level:

$$
\hat { N } _ { I } = \frac { M _ { f } } { M _ { f } - K } \sum _ { m = K } ^ { M _ { f } - 1 } | \hat { R } _ { m } | ^ { 2 } \Delta f ,\tag{21}
$$

where K is the number of discarded values. The value of K can be approximately selected as

$$
K \approx n _ { \operatorname* { m a x } } \cdot \frac { B } { T _ { c } } \cdot \frac { 2 l _ { \operatorname* { m a x } } } { c } \cdot \frac { 1 } { \Delta f } ,\tag{22}
$$

where ${ l } _ { \mathrm { m a x } }$ is the maximum target size, $n _ { \mathrm { m a x } }$ is the maximum number of targets and $\frac { B } { T _ { c } } . \frac { 2 l _ { \mathrm { m a x } } } { c }$ indicates the frequency range that a target with size l<sub>max</sub> occupies. In practice, the value of K can be set larger than the equation above to ensure that all peaks corresponding to the target echo are discarded. The discarded values except for the target echo have little influence on the estimation of $N _ { I }$ because the estimation in (21) is an average of all values and moreover, $M _ { f } \gg K$

Denote the interference-free noise level as

$$
N _ { I F } = \int | N ( f ) | ^ { 2 } d f ,\tag{23}
$$

which is related to the receiver noise power and can be regarded as known. Let

$$
\eta = \frac { \hat { N } _ { I } } { N _ { I F } }\tag{24}
$$

denote the estimation of the relative noise level. In Fig. 6, we plot the relative noise level versus the interference-to-noise ratio (INR). The INR is defined as

$$
\mathrm { I N R } = \frac { P _ { I } } { \sigma ^ { 2 } } ,\tag{25}
$$

where $\sigma ^ { 2 }$ is the receiver noise power. At each value of INR, we simulate 10 cases where two radars randomly select two different chirp rates. In each simulation, the received signal power to the noise power ratio is set as 4 and the interference power varies. In the estimation of $\eta ,$ we set $K = 2 0$ . Fig. 6 conveys two messages. First, $\eta$ increases approximately linearly with INR. More specifically, we have $\eta \approx \mathrm { I N R } + 1$ because $N _ { I }$ is proportional to the interference plus the noise power and $N _ { I F }$ to the noise power. Second, η is almost irrelevant to different combinations of chirp rates. Therefore, $\eta$ is a suitable measurement for the interference power in our problem.

![](images/7410a25bd3131ef92ed9279ff8e8c5c095bfa8d9cd162f604a01278e9984f8e6.jpg)  
Fig. 6. Relative noise level versus INR. At each value of INR, we simulate 10 cases where two radars randomly select two different chirp rates. The inner subfigure is a magnified version of the plot within the box.

Now, by exploiting the spectrum of the received signal $R ( f )$ according to (19-24), we obtain an estimation of the relative noise level, $\eta ,$ as the radar measurement for the interference power. In this way, radar only monitors the subband on which it transmits.

## IV. SPECTRUM ALLOCATION USING RL

At the beginning of this section, we clarify some notations. The subscript t represents discrete time step and the superscript i represents the car index and $i \in \{ 1 , 2 , . . . , N \}$

The outline of the RL-based spectrum allocation approach for automotive radar is shown in Fig. 7. First, by processing the received signal from last time step, the receiver constructs the current observation $\mathbf { o } _ { t } ^ { i }$ . The construction of $\mathbf { o } _ { t } ^ { i }$ will be described in detail in Subsection $\mathrm { I V } { - } \mathrm { A }$ . Then, the transmitter employs a Q-network to choose a subband $u _ { t } ^ { i }$ by aggregating the historical observations $\left\{ \mathbf { o } _ { t } ^ { i } , \mathbf { o } _ { t - 1 } ^ { i } , . . . , \mathbf { o } _ { 1 } ^ { i } \right\}$ . In the meantime, the receiver also gives feedback to the transmitter in the form of a reward signal $r _ { t - 1 } ^ { i } ,$ which is evaluated based on the relative noise level $\eta _ { t - 1 } ^ { i }$ . The reward acts as a tutor guiding the Q-network to adjust parameters to generate a better subband selecting policy.

## A. Reward and Receiver Observation

The reward is defined in terms of the relative noise level $\eta _ { t } ^ { i }$ . If η<sup>i</sup> is below a predefined threshold $\eta _ { 0 } ,$ , the transmission

is regarded as successful and the corresponding reward is 1;   
otherwise, the reward is 0, i.e.

$$
r _ { t } ^ { i } = \left\{ \begin{array} { l l } { 1 } & { \eta _ { t } ^ { i } < \eta _ { 0 } } \\ { 0 } & { \eta _ { t } ^ { i } \ge \eta _ { 0 } } \end{array} \right. .\tag{26}
$$

The observation which Car i acquires at time step t is

$$
\mathbf { o } _ { t } ^ { i } = \left[ u _ { t - 1 } ^ { i } , \ r _ { t - 1 } ^ { i } , \eta _ { t - 1 } ^ { i } , \ p _ { t } ^ { i } , \ \mathbf { p } _ { t } ^ { i } \right] ,\tag{27}
$$

where

$u _ { t - 1 } ^ { i } \colon$ the last subband on which Car i transmitted;

$r _ { t - 1 } ^ { i } \colon$ the last reward which Car i received;

$\eta _ { t - 1 } ^ { i } \colon$ the relative noise level in last time step;

$p _ { t } ^ { i } \colon$ the position of Car i;

$\mathbf { p } _ { t } ^ { i } \colon$ the estimated positions of cars in front of Car i.

The car’s own position $p _ { t } ^ { i }$ can be acquired from its onboard sensors such as the global positioning system (GPS) and inertial navigation system (INS). The estimated position $\mathbf { p } _ { t } ^ { i }$ is a two dimensional vector:

$$
\mathbf { p } _ { t } ^ { i } = [ p _ { S , t } ^ { i } , p _ { D , t } ^ { i } ] ,\tag{28}
$$

where $p _ { S , t } ^ { i } , p _ { D , t } ^ { i }$ are the position of the nearest car in front of Car i in the same and different lane, respectively. The vector $\mathbf { p } _ { t } ^ { i }$ is calculated according to the radar measurement of the range and velocity, which is accompanied with estimation errors caused by noise and interference.

## B. Q-network in Transmitter

In this subsection, first, we recap the RL and Q-learning algorithm. Then, we show how the Q-network is specified for the spectrum allocation problem.

In RL, an agent learns how to choose actions by receiving rewards from an unknown environment [32]. Let $\mathbf { s } _ { t } , ~ a _ { t }$ and $r _ { t }$ denote the state of the environment, the action of the agent and the reward it receives at time step t. At each time step, action $a _ { t }$ is determined by environment state $\mathbf { s } _ { t }$ following a policy $\pi ,$ which is a mapping from the state space to the action space, by trying to maximize a discounted sum of future rewards:

$$
G _ { t } = r _ { t } + \gamma r _ { t + 1 } + \gamma ^ { 2 } r _ { t + 2 } + . . . ,\tag{29}
$$

where $\gamma \in [ 0 , 1 ]$ is the discounting factor. The factor $\gamma$ reflects how much we consider the influence of the current action on the future. An extreme example is $\gamma = 0$ , which corresponds to the case where the agent aims to maximize the immediate reward $r _ { t } .$ . The Q-function is defined as the expectation of $G _ { t }$ after taking action $a _ { t }$ under environment state $\mathbf { s } _ { t }$ following policy π:

$$
Q _ { \pi } ( \mathbf { s } _ { t } , a _ { t } ) = \mathbb { E } \left\{ G _ { t } | \mathbf { s } _ { t } , a _ { t } , \pi \right\} ,\tag{30}
$$

where the expectation is taken over the probabilistic sequence, $\mathbf { s } _ { t + 1 } , a _ { t + 1 } , r _ { t + 1 } , \mathbf { s } _ { t + 2 } , a _ { t + 2 } , r _ { t + 2 } , . . . ,$ following policy π. Learning the optimal policy equals finding the optimal Qfunction:

$$
Q ^ { * } ( \mathbf { s } _ { t } , a _ { t } ) = \operatorname* { m a x } _ { \pi } Q _ { \pi } ( \mathbf { s } _ { t } , a _ { t } ) .\tag{31}
$$

Then, the best action can be determined by the optimal Qfunction:

$$
a _ { t } ^ { * } = \arg \operatorname* { m a x } _ { a ^ { \prime } } Q ^ { * } ( \mathbf { s } _ { t } , a ^ { \prime } ) .\tag{32}
$$

![](images/21bb0eaea94d9949f2c3262027630067ed0ac29793251ca5014b56e682b9ca69.jpg)  
Fig. 7. Outline of the RL-based spectrum allocation approach for automotive radar.

The Q-learning algorithm provides an iterative way to estimate the optimal Q-function even when an explicit model of the environment is unavailable. Each iteration is based on an experience of the agent, which is represented by a quadruple, $\left( \mathbf { s } _ { t } , a _ { t } , r _ { t } , \mathbf { s } _ { t + 1 } \right)$ . The iteration is performed as [32]:

$$
\begin{array} { r c l } { Q ( \mathbf { s } _ { t } , a _ { t } ) } & { \longleftarrow } & { Q ( \mathbf { s } _ { t } , a _ { t } ) } \\ & & { \displaystyle + \alpha _ { t } \left[ r _ { t } + \gamma \operatorname* { m a x } _ { a ^ { \prime } } Q ( \mathbf { s } _ { t + 1 } , a ^ { \prime } ) - Q ( \mathbf { s } _ { t } , a _ { t } ) \right] , } \end{array}\tag{33}
$$

where $\alpha _ { t }$ is the learning step size. As the iteration in (33) is limited to cases where the state and action space are low dimensional and discrete, a neural network is usually used to approximate the Q-function [33]. The Q-function approximated by a neural network is referred to as Q-network hereafter.

In our problem, as $\mathbf { s } _ { t }$ is not fully observable, using a single observation to represent the environment state is inadequate. To construct a more complete environment state, the historical observations are aggregated:

$$
\mathbf { s } _ { t } ^ { i } = \left[ \mathbf { o } _ { 1 } ^ { i } , \mathbf { o } _ { 2 } ^ { i } , . . . , \mathbf { o } _ { t } ^ { i } \right] ,\tag{34}
$$

where $\mathbf { s } _ { t } ^ { i }$ denotes the constructed environment state by Car i. Here, we use an LSTM recurrent neural network to approximate the Q-function since the LSTM structure is capable of memorizing the past by maintaining a hidden state [34]. The Q-network for Car i is denoted as $Q ^ { i } ( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u _ { t } ^ { i } ; \mathbf { w } ^ { i } )$ , where $\mathbf { w } ^ { i }$ is the network parameter, ${ \boldsymbol u } _ { t } ^ { i }$ is the chosen subband by Car i at time step t and $\mathbf { h } _ { t - 1 } ^ { i }$ is the hidden state extracted from past observations $\mathbf { o } _ { 1 } ^ { i } , \mathbf { o } _ { 2 } ^ { i } , . . . , \mathbf { o } _ { t - 1 } ^ { i }$ . Using the LSTM network, the constructed environment state by Car i can be equally represented by:

$$
\mathbf { s } _ { t } ^ { i } = \left[ \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } \right] .\tag{35}
$$

The loss function of the i-th Q-network is defined as

$$
\begin{array} { r } { \mathcal { L } ^ { i } ( \mathbf { w } ^ { i } ) = \mathbb { E } \left\{ \left( y _ { t } ^ { i } - Q ^ { i } \left( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u _ { t } ^ { i } ; \mathbf { w } ^ { i } \right) \right) ^ { 2 } \right\} , } \end{array}\tag{36}
$$

where the expectation is taken over each experience $( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u _ { t } ^ { i } , r _ { t } ^ { i } , \mathbf { o } _ { t + 1 } ^ { i } , \mathbf { h } _ { t } ^ { i } )$ , and $y _ { t } ^ { i }$ is the target value [32]:

$$
y _ { t } ^ { i } = r _ { t } ^ { i } + \gamma \operatorname* { m a x } _ { u ^ { \prime } } Q ^ { i } \left( \mathbf { o } _ { t + 1 } ^ { i } , \mathbf { h } _ { t } ^ { i } , u ^ { \prime } ; \mathbf { w } ^ { i - } \right) ,\tag{37}
$$

where $\mathbf { w } ^ { i - }$ represents the network parameters before the update. The loss function is to minimize the error between the Q-function and target values over experiences of all radars. Then, the gradient descent step is performed to finish the update:

$$
\mathbf { w } ^ { i } = \mathbf { w } ^ { i - } - \beta \frac { \partial \mathcal { L } ^ { i } ( \mathbf { w } ) } { \partial \mathbf { w } } \bigg | _ { \mathbf { w } = \mathbf { w } ^ { i - } } ,\tag{38}
$$

where $\beta$ is the learning rate.

## C. Network Architecture

The Q-network architecture in our problem is shown in Fig. 8. A fully connected layer (FCL) transforms $\mathbf { o } _ { t } ^ { i }$ into inputs of the LSTM layers. The LSTM layers maintain a hidden state $\mathbf { h } _ { t - 1 } ^ { i }$ , which is extracted from past observations before time step t. Each element of the output represents the Q-function value of the corresponding subband. Fig. 9 shows the unfolded representation of the Q-network. At time $t ,$ subband ${ \boldsymbol u } _ { t } ^ { i }$ is chosen by combining the current observation $\mathbf { o } _ { t } ^ { i }$ and hidden state $\mathbf { h } _ { t - 1 } ^ { i }$ . Then $\mathbf { h } _ { t - 1 } ^ { i }$ evolves into $\mathbf { h } _ { t } ^ { i }$ by incorporating the new observation $\mathbf { o } _ { t } ^ { \ i }$ . In this way, the subband at each time step is determined by both the present and past observations.

## D. Network Training

In this subsection, some details of the network training are given.

In the training, a time step is equal to a transmission period T . An episode consists of a number of successive time steps randomly taken from the dynamic scenario in which cars are traveling in two lanes. In [35], several techniques are employed to train the deep Q-network with stability. In our problem, the following listed techniques are adopted to train the Qnetworks.

![](images/a588557ff0ded36af57b3b4ca5f57048e6931cf0ab1126c8a1e62739b25c0916.jpg)  
Fig. 8. The Q-network architecture. The black square stands for a time-step delay.

• Experience replay with batch learning. During the training, each experience, $e _ { t } ^ { i } = \left( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u _ { t } ^ { i } , r _ { t } ^ { i } , \mathbf { o } _ { t + 1 } ^ { i } , \mathbf { h } _ { t } ^ { i } \right)$ , is stored in memory. The memory only stores experiences of the recent 200 episodes. In each update, a batch of experiences are drawn from the memory. A batch is formed as (39) shows.

$$
\left\{ \begin{array} { c c c } { e _ { t _ { 1 } } ^ { i } } & { e _ { t _ { 1 } + 1 } ^ { i } } & { \cdot \cdot \cdot } & { e _ { t _ { 1 } + P - 1 } ^ { i } } \\ { e _ { t _ { 2 } } ^ { i } } & { e _ { t _ { 2 } + 1 } ^ { i } } & { \cdot \cdot \cdot } & { e _ { t _ { 2 } + P - 1 } ^ { i } } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { e _ { t _ { K } } ^ { i } } & { e _ { t _ { K } + 1 } ^ { i } } & { \cdot \cdot \cdot } & { e _ { t _ { K } + P - 1 } ^ { i } } \end{array} \right\}\tag{39}
$$

Each row in (39) is obtained following the two procedures: first, randomly picking an episode from the memory; then, randomly choosing a sequence of $P$ successive experiences from the whole episode. The randomization among different rows improves training stability because it breaks the correlation of experience sequences [35]. The batch is used for the gradient descent step (38) in which the gradient $\partial \mathcal { L } ( \mathbf { w } ) / \partial \mathbf { w }$ is calculated on the batch. The gradient calculation can be easily realized with the Tensorflow framework.

• ǫ-greedy policy. At each time step, each car chooses a subband corresponding to the greatest Q-function value or otherwise a random one with small exploring probability ǫ, i.e.

$$
u _ { t } ^ { i } = \left\{ \begin{array} { l l } { \arg \operatorname* { m a x } _ { u ^ { \prime } } Q ^ { i } ( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u ^ { \prime } ; \mathbf { w } ^ { i } ) } & { a \geq \epsilon } \\ { \mathrm { ~ a ~ r a n d o m ~ s u b b a n d ~ } } & { a < \epsilon } \end{array} \right. ,\tag{40}
$$

where a is one realization of a uniformly distributed random variable ranged from 0 to 1.

• Double networks. To enhance training stability, a separate network, called target network and denoted as $\hat { Q } ^ { i }$ , is introduced in the training procedures. In (37), the target value is generated by the Q-network itself, which may cause training instability. Instead, the target network is used to produce the target value in the training and (37) is replaced by

$$
y _ { t } ^ { i } = r _ { t } ^ { i } + \gamma \operatorname* { m a x } _ { u ^ { \prime } } \hat { Q } ^ { i } \left( \mathbf { o } _ { t + 1 } ^ { i } , \mathbf { h } _ { t } ^ { i } , u ^ { \prime } ; \hat { \mathbf { w } } ^ { i } \right) ,\tag{41}
$$

where $\hat { \mathbf { w } } ^ { i }$ is the network parameter of ${ \hat { Q } } ^ { i } .$ . The target network $\hat { Q } ^ { i }$ has the same structure with $Q ^ { i }$ . Unlike the Q-network which is updated every time step, the target network is updated every few time steps. In an update, the Q-network parameter $\mathbf { w } ^ { i }$ is assigned to the target network parameter $\hat { \mathbf { w } } ^ { i }$ . Between two updates, the target network parameter is held fixed. The number of steps between two updates, i.e. the training cycle of the target network, is denoted as $C .$

![](images/96ccf8754ca2e337cf4de2126ce7da9ff0b24e25c49b41e24c3422d5a5c34836.jpg)  
Fig. 9. Unfolded representation of the Q-network, showing a subband is determined by combining the present and past observations.

The Q-network training algorithm is summarized in Algorithm 1.

Algorithm 1: Q-Network Training Algorithm   
1 Set up two set of networks, $\{ Q ^ { i } \}$ and $\{ \hat { Q } ^ { i } \}$   
2 Initialize $Q ^ { i }$ and $\hat { Q } ^ { i }$ with the same random parameter   
$\mathbf { w } ^ { - }$   
3 for $e p i s o d e = 1 : N _ { e }$ do   
4 Initialize hidden state $\mathbf { h } _ { 0 } ^ { i }$ and observation ${ \mathbf o } _ { 1 } ^ { i }$   
$\forall i \in \{ 1 , 2 , . . . , N \}$   
5 for $t = 1 : T$ do   
6 for Car $i = 1 : N$ do   
7 Feed observation o<sup>i</sup> to network $\mathbf { Q } ^ { i }$ to get a   
set of action values   
$\{ Q ^ { i } ( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u ; \mathbf { w } ) \} ( u = 1 , 2 , . . . , M )$ and   
the hidden state $\mathbf { h } _ { t } ^ { i }$   
8 Choose a subband $u _ { t } ^ { i }$ as (40).   
9 Get a reward $r _ { t } ^ { i } .$   
10 Obtain new observation $\mathbf { o } _ { t + 1 } ^ { i }$   
11 Store $e _ { t } ^ { i } = \left( \mathbf { o } _ { t } ^ { i } , \mathbf { h } _ { t - 1 } ^ { i } , u _ { t } ^ { i } , r _ { t } ^ { i } , \mathbf { \mathbf { o } } _ { t + 1 } ^ { i } , \mathbf { h } _ { t } ^ { i } \right)$ into   
memory.   
12 Form a batch as (39).   
13 Calculate target values $y _ { t } ^ { i }$ using network $\hat { Q } ^ { i }$   
14 $\begin{array} { r } { \mathbf { w } ^ { i }  \mathbf { w } ^ { i } - \beta \frac { \partial \mathcal { L } ^ { i } ( \mathbf { w } ) } { \partial \mathbf { w } } , } \end{array}$   
15 Every C time steps, $\hat { Q } ^ { i } = Q ^ { i }$   
16 end   
17 end   
18 end

## V. SIMULATIONS

In this section, simulation results are presented to verify the proposed approach. First, the simulation setup is described. Then, two contrasting approaches are introduced. Last, simulation results are provided along with the corresponding discussions .

The simulations are implemented with Python. The networks used in the simulations are built and trained with the Tensorflow framework.

## A. Simulation Setup

Training Q-networks can be time-consuming. In our case, a training episode consists of around 20 to 200 time steps and it takes thousands of episodes for the Q-networks to converge. Hence, in many RL related applications, the Q-networks are first trained offline in a synthesized environment and then tested in other environments to see if the trained Q-networks are capable of generalization. This practice is also adopted in our simulations. More specifically, we first train the $\mathrm { Q - }$ networks in a simulated environment with a relatively simple scenario model. Then, we test the trained Q-networks with a more complex scenario model.

The simulated scenario for training is constructed as Fig. 1 shows. The flow of traffic is modeled by a truncated exponential distribution [36]. Under this model, the distance l between any two adjacent cars satisfies the following distribution:

$$
p ( l ) = \left\{ \begin{array} { l l } { \lambda \cdot \frac { 1 } { \rho } \exp ( - \frac { l } { \rho } ) } & { d _ { \mathrm { m i n } } \leq l \leq d _ { \mathrm { m a x } } } \\ { 0 } & { \mathrm { o t h e r w i s e } } \end{array} \right. ,\tag{42}
$$

where $\rho$ is the intensity parameter, and λ is a normalizing coefficient to assure that the integral of $p ( l )$ equals 1. Cars in each lane are assumed to travel at constant velocity, i.e., $v _ { 1 }$ and v<sub>2</sub>, respectively. The detailed scenario settings are shown in TABLE I. In the simulations, if INR ≤ 10 (10 dB), it is taken as a successful transmission. As shown in Subsection III-B, $\eta \approx \mathrm { I N R } + 1$ . Hence, we set the threshold $\eta _ { 0 }$ as 11.

In the testing scenario, the motion of each car is modeled by a probabilistic cellular automaton model [37], which is a widely used model in traffic flow simulations. Let $v _ { \operatorname* { m a x } , i } ~ ( i =$ 1, 2 indicate the two lanes, respectively) denote the maximum velocity for the two lanes. At each time interval $t _ { v } ,$ the velocity of an arbitrary car is updated by:

1) Acceleration: If the velocity v of a car is lower than $v _ { \mathrm { m a x } , i } ,$ then the car speeds up by $v = v + \Delta v ,$ where $\Delta v$ is a predefined velocity increment.

2) Slowing down: If the distance l to the next car ahead in the same lane is not larger than $d _ { \mathrm { m i n } }$ , then the car slows down by $v = v - \Delta v$

3) Randomization: With probability $p _ { \mathrm { s d } } .$ , the car slows down by $v = v - \Delta v { \mathrm { ~ i f ~ } } v \leq \Delta v$

The hyper parameters used in training the Q-networks are shown in TABLE II.

## B. Contrasting Approaches

The first contrasting approach is the random policy, which is to randomly select a subband with equal probability at each time step. The second is a commonly used method in DSA, the myopic policy [38]. The myopic policy aims to select a subband which is most likely to be unused in the next time step. However, it requires prior knowledge of the transition probability of each subband. In [38], a practical realization of the myopic policy is given without knowing the transition probability. To make it more efficient in our multiradar problem, we make some modifications. In the original myopic policy, all the subbands are kept in a predefined priority order. The user keeps using one subband if the result is a success. Otherwise, it switches to the next subband according to the priority order. In the modified myopic policy, the order is not needed. Radar switches to a random subband when failure occurs. The modified myopic policy outperforms the original version in our problem. Under the modified myopic policy, the subband chosen at time step t is

TABLE I SCENARIO SETTINGS
<table><tr><td>Notation</td><td>Description</td><td>Value</td></tr><tr><td> $T$ </td><td>Transmission period/a time step (ms)</td><td>100</td></tr><tr><td> $T _ { f }$ </td><td>Frame duration (ms)</td><td>5</td></tr><tr><td> $T _ { c }$ </td><td>Chirp interval (μs)</td><td>10～100</td></tr><tr><td> $P _ { L }$ </td><td>Transmitting power of long-range radar (dBmW)</td><td>25</td></tr><tr><td> $P _ { S }$ </td><td>Transmitting power of short-range radar (dBmW)</td><td>15</td></tr><tr><td> $A _ { e }$ </td><td>Effective area  $( \mathrm { m m ^ { 2 } } )$ </td><td>5</td></tr><tr><td> $G _ { t }$ </td><td>Antenna gain</td><td>48 dB</td></tr><tr><td> $g$ </td><td>Decaying coefficient</td><td>0.1</td></tr><tr><td> $\bar { v } _ { 1 , \operatorname* { m a x } } / v _ { 1 }$ </td><td>(Maximum) velocity of cars on Lane 1 (m/s)</td><td>30</td></tr><tr><td> $v _ { 2 , \operatorname* { m a x } } / v _ { 2 }$ </td><td>(Maximum) velocity of cars on Lane 2 (m/s)</td><td>-25</td></tr><tr><td> $\Delta v$ </td><td>Velocity increment (m/s)</td><td>5</td></tr><tr><td> $t _ { v }$ </td><td>Velocity updating interval (s)</td><td>0.5</td></tr><tr><td> $\underline { { \eta _ { 0 } } }$ </td><td>Relative noise level threshold</td><td>11</td></tr></table>

TABLE II  
PARAMETERS IN TRAINING THE Q-NETWORKS
<table><tr><td>Description</td><td colspan="2">Value</td></tr><tr><td rowspan="6">Network architecture</td><td>Layer</td><td>Number of neurons</td></tr><tr><td>Input</td><td>7</td></tr><tr><td>FCL</td><td>30</td></tr><tr><td>LSTM1</td><td>30</td></tr><tr><td>LSTM2</td><td></td></tr><tr><td>LSTM3</td><td>30 20</td></tr><tr><td rowspan="6"></td><td>LSTM4</td><td></td></tr><tr><td></td><td>10</td></tr><tr><td>Output</td><td>M</td></tr><tr><td></td><td></td></tr><tr><td></td><td>1 ms</td></tr><tr><td>40 × 20</td><td>around 20 ～ 200 time steps</td></tr></table>

$$
u _ { t } ^ { i } = \left\{ \begin{array} { l l } { u _ { t - 1 } ^ { i } } & { \eta _ { t } ^ { i } < \eta _ { 0 } } \\ { \mathrm { ~ a ~ r a n d o m ~ s u b b a n d ~ } } & { \mathrm { o t h e r w i s e } } \end{array} \right.\tag{43}
$$

## C. Performance Metric

To evaluate the proposed and contrasting approaches, we use success rate as a metric. Success rate is the percentage of the successful transmissions, expressed as

$$
\xi = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \frac { 1 } { N _ { t } } \sum _ { t = 0 } ^ { N _ { t } } \mathbb { I } _ { \eta _ { 0 } } ( \eta _ { i } ^ { t } ) ,\tag{44}
$$

where $N _ { t }$ is the total number of transmissions and $\mathbb { I } _ { \eta _ { 0 } } ( \eta _ { i } ^ { t } )$ is defined as

$$
\mathbb { I } _ { \eta _ { 0 } } ( \eta _ { i } ^ { t } ) = \left\{ \begin{array} { l l } { 1 } & { 0 \le \eta _ { i } ^ { t } \le \eta _ { 0 } } \\ { 0 } & { \mathrm { e l s e w h e r e } } \end{array} \right. .\tag{45}
$$

![](images/0ff82a822464af01a4520dd74dcd97d58a67e236461bdf6c1e95fad366f29c8c.jpg)  
(a) N <sup>=</sup> <sup>6</sup>, M <sup>=</sup> <sup>2</sup>

![](images/6407e1ae5c8d82bc9a90943fcd1c63ebbd18be05249c72956dc286396e669222.jpg)  
(b) N <sup>=</sup> <sup>8</sup>, M <sup>=</sup> <sup>3</sup>  
Fig. 10. Success rate of the three approaches versus the number of episodes in two scenarios. In the first <sup>7</sup>, <sup>000</sup> episodes, the Q-networks are trained with the uniform motion model. In the last <sup>1000</sup> episodes, the trained networks are tested with the probabilistic cellular automaton model.

## D. Results and Discussions

In Fig. 10, a comparison of the success rate achieved by the three approaches is drawn in two scenarios where $N = 6 , M = 2$ and N = 8, M = 3 (N, M are the number of cars and subbands), respectively. In the first 7, 000 episodes, the Q-networks are trained with the uniform motion model. In the last 1, 000 episodes, the trained networks are tested with the probabilistic cellular automaton model. Apparently, the myopic policy performs better than the random policy. In Fig. 10 (a), the average success rate achieved by the myopic and random policy are 58% and 47%; in Fig. 10 (b), they are 80% and 57%. As the RL-based curves show, the success rate gradually increases and then becomes stable during the training. In the beginning, the RL-based approach is close to the random policy and outperformed by the myopic policy. As the learning proceeds, the RL-based approach gradually surpasses the myopic policy. In the testing, the trained Qnetworks achieve success rate of 70% in Fig. 10 (a) and 90% in Fig. 10 (b), both realizing around 10% success rate improvement over the myopic policy in both scenarios. It should be noted that during the training each radar maintains an exploring probability $\epsilon \ = \ 0 . 0 5$ to randomly choose a subband. In the testing, each radar chooses subbands according to the learned Q-networks without exploring, i.e. ǫ = 0. This accounts for a small rise in the success rate in the last 1000 episodes.

In Fig. 11, we compare the success rate achieved by the three approaches under different testing scenarios. Each scenario has a different combination of the number of cars and the number of subbands. In each subfigure, the number of cars is fixed and success rate versus the number of subbands is plotted. Generally, success rate achieved by the three approaches all increases with the number of subbands. The

RL-based approach has the best performance in all scenarios and the random policy the worst.

In Fig. 12, we plot the success rate improvement by the RL-based approach over the random (Fig. 12 (a)) and myopic policy ( Fig. 12 (b)) versus the number of subbands. In both subfigures, the success rate improvement first increases with the number of subbands and then decreases. Compared with the myopic policy, when there is only one subband, the two approaches equal; then, the improvement reaches its peak at 2 or 3 subbands, mostly exceeding 10%; when there are 5 subbands, the improvement drops below 3%. As the myopic policy is essentially to switch to a random subband when failure occurs, if there are 2 or 3 subbands, the probability of two radars switching to the same subbands is still large (the probability is 1/M ). However, the RL-based approach can use additional position and interference information, processed by the learned Q-networks, to avoid interference. The myopic policy catches up with the RL-based approach when the number of subbands increases because the probability of two radars switching to the same subbands becomes small. By analyzing the improvement of the RL-based approach over the myopic policy, it can be concluded that the RL-based approach is more advantageous when subbands are fewer. This means that using the proposed approach, we can divide the whole band into fewer subbands so that each subband can be allocated with more bandwidth for higher resolution.

Examining the relationship between the performance of the proposed approach and the number of subbands is instructive in dividing the spectrum. As is stated previously, the number of subbands is predefined majorly according to radar resolution or bandwidth requirement. Now, the interference avoidance performance can be another factor to be considered. More subbands guarantee higher success rate but result in lower range resolution due to bandwidth reduction. The proposed approach is verified to be more advantageous over the myopic policy with fewer subbands, which means that we can achieve the same interference avoidance performance with fewer subbands so that each subband can be assigned with more bandwidth for higher resolution. In other words, our approach makes it more effective to compromise between resolution and success rate.

![](images/a8e581e384de4eac1b74e7fe564d0926d5e765d990afeef1ee6c7afc605b1136.jpg)

![](images/bba2e17e7b6e0111e76437b24ea51711eb8af0816e878cae0752f2a9e05f02cd.jpg)

![](images/5f64be0d431618525bb52dc738cbfdc3123146046e9cee5211792f8af8f4120a.jpg)

![](images/39c1e28a8a68d2732ce167ef48ac312645625018e1b85002c61d79df63bea0f6.jpg)  
Fig. 11. Success rate achieved by the three approaches versus the number of subbands when the number of cars is fixed.

![](images/1877c11d872d6d353d29e97644b4474fe657c5267b91be972be55309cdb04164.jpg)  
(a) RL-based v. random

![](images/d22a82224781f1d9c02c3e559c9f5ff882ff9641eef54865137441a51cbf38b3.jpg)  
(b) RL-based v. myopic  
Fig. 12. Success rate improvement by the RL-based approach over the random and myopic policy versus the number of subbands.

Next, we verify the robustness of the proposed approach in different road condition, such as the traffic density. In Fig. 13, we plot success rate of the three approaches versus traffic density parameter $\rho$ under 4 different scenarios. In the RLbased approach, the Q-networks are trained when $\rho = 0 . 0 2$ Then the trained Q-networks are applied to other cases with different values of $\rho$ ranged from 0.01 to 0.1. Generally, for all three approaches, success rate decreases with the traffic density parameter increasing. Compared to the myopic policy, the RLbased approach has a steady success rate improvement in the examined range of $\rho ,$ which shows that the trained network can be well generalized to other traffic density.

In the scenario model, it is assumed that the number of cars is fixed as N . As the Q-networks are trained offline, the pre-trained Q-networks for different number of cars can be stored in each car. Because the interfering power decreases with the distance in the inverse square law, we can consider a certain area within which cars interfere with each other but the interference caused by cars outside the area can be neglected. The number of cars can be acquired by each car via the popular vehicle-to-everything (V2X) communications, including vehicle-to-infrastructure communication [39]. Then, each car can select its own Q-network accordingly. The time between two adjacent communications can be much longer than T because the number of cars in the area does not change fast. After the communication, each car can independently select subbands using the Q-networks.

Furthermore, we find it interesting that the Q-networks trained for $N _ { \mathrm { 1 ^ { - } } } \mathrm { c a r }$ scenarios are also suitable for $N _ { 2 } .$ -car $( N _ { 2 } \leq N _ { 1 } )$ scenarios. In the simulation, we apply the trained Q-networks for the 10-car scenario to the 9- and 8- car scenarios, respectively. Each of the 9 or 8 cars selects its Qnetwork out of the trained 10 Q-networks, which means the remaining 1 or 2 Q-networks are not used. In Fig. 14, we plot the success rate improvement over the myopic policy for each scenario. As Fig. 14 shows, in the 9-car scenario, when the number of subbands is 2 or 3, the proposed approach can still gain around 10% success rate improvement over the myopic policy. In the 8-car scenario, the improvement is around 6%. As this simulation suggests, at the beginning, each car within an area can choose the Q-networks which are trained for a relative large number of cars. Then, new cars can just use the remaining Q-networks when they enter the area.

![](images/11a5774ed50808a6a62d72599315f4c29c57e612e829d1b9a99ff7ee8ba3f6e6.jpg)  
(a) N <sup>=</sup> <sup>10</sup>, M <sup>=</sup> <sup>3</sup>

![](images/9ab6d2ef0ba3bf50f5b36e9a4ea15b1fbad2d78edf22862d414334e4f06b64b3.jpg)  
(b) N <sup>=</sup> <sup>10</sup>, M <sup>=</sup> <sup>4</sup>

![](images/2fec1a9c331e0ecb59678e5959b265be4c9c3e8c1a91d8c93fdd12f0773a497f.jpg)  
(c) N <sup>=</sup> <sup>12</sup>, M <sup>=</sup> <sup>3</sup>

![](images/518a6e561386e50dc926d5e0488aaff240ed2aadae17c6e16c5564ad479d20be.jpg)  
(d) N <sup>=</sup> <sup>12</sup>, M <sup>=</sup> <sup>4</sup>  
Fig. 13. Success rate achieved by the three approaches versus the traffic density parameter under different scenarios. The dashed box indicates that the Q-networks are trained when the traffic density parameter is <sup>0</sup>.<sup>02</sup> and then the trained networks are applied to other cases with different traffic density parameter.

## VI. CONCLUSION

In this paper, we study the interference avoiding problem for automotive radar using an RL-based decentralized spectrum allocation approach. With RL, each radar learns to choose a frequency subband merely according to its own observations with almost no communication. Considering a single radar observation is inadequate, an LSTM neural network is incorporated in RL so that a subband is decided by combining both the present and past observations. Simulation experiments are conducted to verify the RL-based approach by comparing it with two commonly used spectrum allocation approaches, i.e., the random and myopic policy. It is shown that the RLbased approach gains a higher success rate improvement than the myopic policy with fewer subbands. Hence, the proposed approach makes it more effective to compromise between resolution and interference.

The simulation model used in this paper is simplified to demonstrate the feasibility of the proposed approach. Future work will focus on constructing a simulation model which can better represent the much more complex road environments in the real world.

![](images/c6ac2c19594b0d2debcb77899e6f375546a9d09025c878710aa833cda129ee62.jpg)  
Fig. 14. Success rate improvement over the myopic policy versus the number of subbands when applying the Q-networks trained for the 10-car scenario to the 10-, 9- and 8- car scenarios, respectively.

## APPENDIX A DERIVATION OF THE BEAT FREQUENCIES

Recall that in (3)(4), we give the target echo signal model. Let

$$
\lambda = { \frac { 2 v } { c } } .\tag{46}
$$

The phase of the transmitted signal s(t) and the target echo $e ( t )$ are

$$
\phi _ { s } ( t ) = \left\{ \begin{array} { l l } { \displaystyle \frac { B } { 2 T _ { c } } t ^ { 2 } + f _ { m } t } & { 0 \leq t < T _ { c } } \\ { \displaystyle } \\ { \displaystyle \frac { B } { 2 T _ { c } } \left( t - 2 T _ { c } \right) ^ { 2 } + f _ { m } t } & { T _ { c } \leq t < 2 T _ { c } } \end{array} \right.\tag{47}
$$

and

$$
\phi _ { e } ( t ) = \phi _ { s } \left( ( 1 + \lambda ) t - \frac { 2 D } { c } \right) ,\tag{48}
$$

respectively. Then we calculate the instantaneous frequency of $s ( t )$ and $e ( t )$ for the up-chirp:

$$
\frac { \partial \phi _ { s } ( t ) } { \partial t } = \frac { B } { T _ { c } } t + f _ { m }\tag{49}
$$

and

$$
\begin{array} { c } { \displaystyle \frac { \partial \phi _ { e } ( t ) } { \partial t } = \frac { B } { T _ { c } } \left( ( 1 + \lambda ) t - \frac { 2 D } { c } \right) ( 1 + \lambda ) + f _ { m } ( 1 + \lambda ) } \\ { = \displaystyle \frac { \partial \phi _ { s } ( t ) } { \partial t } + \frac { B } { T _ { c } } ( \lambda ^ { 2 } + 2 \lambda ) t } \\ { - \left( 1 + \lambda \right) \frac { B } { T _ { c } } \cdot \frac { 2 D } { c } + \lambda f _ { m } , } \end{array}\tag{50}
$$

respectively. As $\lambda \ll 1 , B \ll f _ { m }$ , we have

$$
\frac { B } { T _ { c } } ( \lambda ^ { 2 } + 2 \lambda ) t < B ( \lambda ^ { 2 } + 2 \lambda ) \ll \lambda f _ { m } .\tag{51}
$$

Therefore, the beat frequency of the up-chirp is

$$
f _ { b } ^ { \uparrow } = \frac { \partial \phi _ { e } ( t ) } { \partial t } - \frac { \partial \phi _ { s } ( t ) } { \partial t } \approx - \frac { B } { T _ { c } } \cdot \frac { 2 D } { c } + \frac { 2 v } { c } f _ { m } .\tag{52}
$$

![](images/c98b4ac828902cd073375497c0bc4e013bf2b3d55835e1415f103531865882ce.jpg)

![](images/1a5f56fded20b99f608bb430268c8748165760b5b0d6a3ae8577721256f5b9ae.jpg)  
Fig. 15. Illustration showing that different chirp rates cause non-constant beat frequency.

Likewise, for the down-chirp, the beat frequency is shown in (13).

## APPENDIX B

## DERIVATION OF THE RAISE IN THE NOISE LEVEL

If different radars uses different chirp rates, the frequency difference between two chirps is illustrated in Fig. 15, which shows that the intermediate frequency signal, r<sub>IF</sub>(t), consists of several pieces of linear frequency modulation signals. Therefore, $r _ { \mathrm { I F } } ( t )$ can be written as

$$
r _ { \mathrm { I F } } ( t ) = \sum _ { i = 1 } ^ { N _ { p } } r _ { p , i } ( t ) ,\tag{53}
$$

where $N _ { p }$ is the number of the pieces of linear frequency modulation signals and $r _ { p , i } ( t )$ is the ith pieces of signal. The signal $r _ { p , i } ( t )$ is expressed as (54), in which $t _ { i - 1 } , t _ { i }$ are the starting and ending time of $r _ { p , i } ( t ) , \ f _ { i - 1 } , f _ { i }$ are the starting and ending frequency, $k _ { i } = ( t _ { i } - t _ { i - 1 } ) / ( f _ { i } - f _ { i - 1 } )$ is the frequency modulation slope and $\phi _ { i }$ is the initial phase.

The Fourier transform of the ith piece of linear frequency modulation signal can be approximated by (55). Hence, we have

$$
R ( f ) = \sum _ { i = 1 } ^ { N _ { p } } R _ { p , i } ( f ) .\tag{56}
$$

As (55, 56) indicates, the spectrum $R ( f )$ can be approximately taken as the sum of several non-overlapping rectangular functions. Therefore, by using different chirp rate, ghost targets are avoided. Instead, the noise level is raised.

## REFERENCES

[1] M. Goppelt, H. L. Blcher, and W. Menzel, “Automotive radar - investigation of mutual interference mechanisms,” Advances in Radio Science, vol. 8, no. 4, pp. 55–60, 2010.

[2] G. Kim, J. Mun, and J. Lee, “A peer-to-peer interference analysis for automotive chirp sequence radars,” IEEE

$$
r _ { p , i } ( t ) = \mathrm { r e c t } \left( \frac { t - t _ { i - 1 } } { t _ { i } - t _ { i - 1 } } \right) \cdot \exp \left( j 2 \pi \left( \frac { 1 } { 2 } k _ { i } \left( t - t _ { i - 1 } \right) ^ { 2 } + f _ { i - 1 } ( t - t _ { i - 1 } ) + \phi _ { i } \right) \right)\tag{54}
$$

$$
R _ { p , i } ( f ) = { \mathcal { F } } \left. r _ { p , i } ( t ) \right. \approx { \sqrt { \frac { \pi } { 2 k _ { i } } } } \cdot \operatorname { r e c t } \left( { \frac { f - f _ { i - 1 } } { f _ { i } - f _ { i - 1 } } } \right) \cdot \exp \left( j { \frac { \pi } { 4 } } + j \phi _ { i } - j 2 \pi f t _ { i - 1 } \right)\tag{55}
$$

Transactions on Vehicular Technology, vol. 67, no. 9, pp. 8110–8117, 2018.

[3] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[4] M. Goppelt, H.-L. Bl ¨ocher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in 2011 German Microwave Conference. IEEE, 2011, pp. 1–4.

[5] T. N. Luo, C. H. E. Wu, and Y. J. E. Chen, “A 77- GHz CMOS automotive radar transceiver with antiinterference function,” IEEE Transactions on Circuits and Systems I Regular Papers, vol. 60, no. 12, pp. 3247– 3255, 2013.

[6] M. Toth, P. Meissner, A. Melzer, and K. Witrisal, “Analytical investigation of non-coherent mutual FMCW radar interference,” in 2018 15th European Radar Conference (EuRAD). IEEE, 2018, pp. 71–74.

[7] M. Kunert, “Project final report,” European Commission: MOre Safety for All by Radar Interference Mitigation (MORARIM), Luxembourg, Tech. Rep. 248231, 2010. [Online]. Available: https://cordis.europa.eu/project/rcn/94234/reporting/en

[8] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM). IEEE, 2015, pp. 1–4.

[9] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive FMCW radar systems,” in 2018 IEEE International Symposium on Circuits and Systems (ISCAS). IEEE, 2018, pp. 1–4.

[10] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in 2015 IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM). IEEE, 2015, pp. 1–4.

[11] S. Alland, W. Stark, M. Ali, and M. Hegde, “Interference in automotive radar systems: Characteristics, mitigation techniques, and current and future research,” IEEE Signal Processing Magazine, vol. 36, no. 5, pp. 45–59, 2019.

[12] M. Kunert, F. Bodereau, M. Goppelt, C. Fischer, A. John, T. Wixforth, T. Ossowska, T. Schipper, and R. Pietsch, “D1.5 - study on the state-ofthe-art interference mitigation techniques,” European Commission: MOre Safety for All by Radar Interference Mitigation (MORARIM), Luxembourg, Tech. Rep. 248231, 2010. [Online]. Available: https://cordis.europa.eu/project/rcn/94234/reporting/en

[13] J. Khoury, R. Ramanathan, M. C. Dan, R. Smith, and T. Campbell, “RadarMAC: Mitigating radar interference in self-driving cars,” in IEEE International Conference on Sensing, Communication, and Networking, 2016, pp. 1–9.

[14] D. W. Bliss, “Communications and radar spectrum sharing rf convergence,” in 2019 IEEE Radar Conference (RadarConf). IEEE, 2019, pp. 1–117.

[15] D. Cohen, K. V. Mishra, and Y. C. Eldar, “Spectrum sharing radar: Coexistence via xampling,” IEEE Transactions on Aerospace and Electronic Systems, vol. 54, no. 3, pp. 1279–1296, 2017.

[16] A. F. Martone, K. I. Ranney, K. Sherbondy, K. A. Gallagher, and S. D. Blunt, “Spectrum allocation for noncooperative radar coexistence,” IEEE Transactions on Aerospace and Electronic Systems, vol. 54, no. 1, pp. 90– 105, 2017.

[17] S. Haykin, “Cognitive radar: A way of the future,” Signal Processing Magazine IEEE, vol. 23, no. 1, pp. 30–40, 2006.

[18] H. Griffiths, L. Cohen, S. Watts, E. Mokole, C. Baker, M. Wicks, and S. Blunt, “Radar spectrum engineering and management: Technical and regulatory issues,” Proceedings of the IEEE, vol. 103, no. 1, pp. 85–102, 2014.

[19] M. S. Greco, F. Gini, P. Stinco, and K. Bell, “Cognitive radars: On the road to reality: Progress thus far and possibilities for the future,” IEEE Signal Processing Magazine, vol. 35, no. 4, pp. 112–125, 2018.

[20] M. Kozy, J. Yu, R. M. Buehrer, A. Martone, and K. Sherbondy, “Applying deep-q networks to target tracking to improve cognitive radar,” in 2019 IEEE Radar Conference (RadarConf). IEEE, 2019, pp. 1–6.

[21] L. Kang, J. Bo, L. Hongwei, and L. Siyuan, “Reinforcement learning based anti-jamming frequency hopping strategies design for cognitive radar,” in 2018 IEEE International Conference on Signal Processing, Communications and Computing (ICSPCC). IEEE, 2018, pp. 1–5.

[22] S. You, M. Diao, and L. Gao, “Deep reinforcement learning for target searching in cognitive electronic warfare,” IEEE Access, vol. 7, pp. 37 432–37 447, 2019.

[23] L. Wang, S. Fortunati, M. S. Greco, and F. Gini, “Reinforcement learning-based waveform optimization for MIMO multi-target detection,” in 2018 52nd Asilomar Conference on Signals, Systems, and Computers. IEEE, 2018, pp. 1329–1333.

[24] H. Li, “Multiagent-learning for aloha-like spectrum access in cognitive radio systems,” EURASIP Journal on Wireless Communications and Networking, vol. 2010, no. 1, p. 876216, 2010.

[25] L. R. Faganello, R. Kunst, C. B. Both, L. Z. Granville, and J. Rochol, “Improving reinforcement learning algorithms for dynamic spectrum allocation in cognitive sensor networks,” in 2013 IEEE Wireless Communications and Networking Conference (WCNC). IEEE, 2013, pp. 35–40.

[26] S. Wang, H. Liu, P. H. Gomes, and B. Krishnamachari, “Deep reinforcement learning for dynamic multichannel access in wireless networks,” IEEE Transactions on Cognitive Communications and Networking, vol. 4, no. 2, pp. 257–265, 2018.

[27] H.-H. Chang, H. Song, Y. Yi, J. Zhang, H. He, and L. Liu, “Distributive dynamic spectrum access through deep reinforcement learning: A reservoir computingbased approach,” IEEE Internet of Things Journal, vol. 6, no. 2, pp. 1938–1948, 2018.

[28] O. Naparstek and K. Cohen, “Deep multi-user reinforcement learning for distributed dynamic spectrum access,” IEEE Transactions on Wireless Communications, vol. 18, no. 1, pp. 310–323, 2018.

[29] J. Hasch, E. Topak, R. Schnabel, T. Zwick, R. Weigel, and C. Waldschmidt, “Millimeter-wave technology for automotive radar sensors in the 77 GHz frequency band,” IEEE Transactions on Microwave Theory and Techniques, vol. 60, no. 3, pp. 845–860, 2012.

[30] V. Dham, “Programming chirp parameters in TI radar devices,” Texas Instruments Incorporated, Tech. Rep., 2017. [Online]. Available: https://www.ti.com/lit/an/swra553a/swra553a.pdf

[31] H. Rohling, “Radar CFAR thresholding in clutter and multiple target situations,” IEEE transactions on aerospace and electronic systems, no. 4, pp. 608–621, 1983.

[32] R. Sutton and A. Barto, Reinforcement Learning: An Introduction. MIT Press, 1998.

[33] M. Riedmiller, “Neural fitted Q iteration first experiences with a data efficient neural reinforcement learning method,” in European Conference on Machine Learning, 2005, pp. 317–328.

[34] S. Hochreiter and J. Schmidhuber, “Long short-term memory.” Neural Computation, vol. 9, no. 8, pp. 1735– 1780, 1997.

[35] M. Volodymyr, K. Koray, S. David, A. A. Rusu, V. Joel, M. G. Bellemare, G. Alex, R. Martin, A. K. Fidjeland, and O. Georg, “Human-level control through deep reinforcement learning,” Nature, vol. 518, no. 7540, pp. 529–533, 2015.

[36] S. Liu, L. Ying, and R. Srikant, “Throughput-optimal opportunistic scheduling in the presence of flow-level dynamics,” IEEE/ACM Transactions on Networking, vol. 19, no. 4, pp. 1057–1070, 2011.

[37] M. Schreckenberg, A. Schadschneider, K. Nagel, and N. Ito, “Discrete stochastic models for traffic flow,” Physical Review E Statistical Physics Plasmas Fluids & Related Interdisciplinary Topics, vol. 51, no. 4, pp. 2939– 2949.

[38] Q. Zhao, B. Krishnamachari, and K. Liu, “On myopic sensing for multi-channel opportunistic access: Struc-

ture, optimality, and performance,” IEEE Transactions on Wireless Communications, vol. 7, no. 12, pp. 5431–5440, 2008.

[39] S. Chen, J. Hu, Y. Shi, Y. Peng, J. Fang, R. Zhao, and l. Zhao, “Vehicle-to-everything (V2X) services supported by LTE-based systems and 5G,” IEEE Communications Standards Magazine, vol. 1, no. 2, pp. 70–76, 20177.