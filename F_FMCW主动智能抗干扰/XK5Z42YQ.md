#

1 Key Laboratory of Trustworthy Distributed Computing and Service, Beijing University of Posts and Telecommunications, Beijing, China

2 Faculty of EEMCS, Delft University of Technology, Delft, Netherlands \*yuanhe@bupt.edu.cn

KeyWords: AUTOMOTIVE RADAR, INTERFERENCE AVOIDANCE, TIME DOMAIN STRATEGY, DEEPREINFORCEMENT LEARNING.

## Abstract

Due to the extensive usage of automotive radars on vehicles, mutual interference among radars on the road is becoming considerable. To address this , we propose a time domain strategy based on deep reinforcement learning (DRL). This approach helps avoid mutual interference for automotive radars in the time domain without extra communications. The numerical simulation results demonstrate that the proposed approach can avoid interference as effectively as frequency hopping. Moreover. the time domain strategy has more advantages than frequency hopping when encountering dynamic interference.

## 1 Introduction

Automotive radars are essential in the advanced driver assistance system. Among them, frequency modulated continuous wave (FMCW) radar has become one of the most popular choices due to its broad operational capability and low cost. However, as the number of FMCW radars equipped on vehicles increases rapidly, mutual interference among different radar devices arises inevitably in busy areas. Strong interference could mask weak targets and raise ghost targets, leading to a higher traffic accident risk. Therefore, it is crucial to mitigate interference for the safety purpose.

Various approaches have been investigated to counter mutual interference. Some studies have developed signal processing methods operated on the received signal to cancel interference [1], [2]. These methods exploit the differences between interference and target echoes in time, frequency, or time-frequency domain to suppress interference with slopes different from the victim radar, i.e., incoherent interference. However, when facing coherent interference which has an identical slope to the transmitting signal of the radar, these signal processing methods are no longer suitable. Other researchers have presented new radar systems or waveform designs [3], [4], [5], which spread interference in the frequency spectrum to avoid ghost targets. These methods are able to suppress coherent interference and improve detection performance. Nevertheless, they require new system and hardware designs as well as more complicated processing.

Over recent years, many resource allocation methods have been proposed to avoid interference. Some achieve cognitive radar approaches based on reinforcement learning (RL) [6], [7]. They exploit the information of the electromagnetic environment to implement spectrum allocation to prevent collisions in the frequency domain. However, their capabilities are limited by the spectrum resource. When facing more interference, spectrum allocation operated on finite bandwidth becomes inadequate to maintain both detection and antiinterference performance. In [8] and [9], time offset is introduced to avoid mutual interference in the time domain. They utilize radar and communication networks to realize centralized or localized resource allocation. However, these cooperative schemes heavily rely on communication.

In this paper, we propose a non-cooperative time domain method for automotive radar to avoid mutual interference. The proposed method only uses the information extracted from the received signal of the radar itself to make decisions, which does not demand any communications. The execution of the method is modelled as an MDP and implemented by deep Qlearning.

## 2. Methodology

## 2.1 Signal Model

In general, the transmitted signal of the FMCW automotive radar in one single chirp can be expressed as

$$
x ( t ) = e ^ { j 2 \pi \left[ f _ { c } t + \frac { 1 } { 2 } K \left( t - \frac { T _ { s w } } { 2 } \right) ^ { 2 } \right] } , \qquad 0 \le t \le T _ { s w }\tag{1}
$$

where $f _ { c } , K$ , and $T _ { s w }$ denote the centre frequency, sweep slope, and sweep duration of one single chirp, respectively. Once the maximum detection range $d _ { m a x }$ is determined, the maximum time delay $\tau _ { m a x }$ can be calculated as

$$
\tau _ { m a x } = \frac { 2 d _ { m a x } } { c } ,\tag{2}
$$

where c denotes the speed of light. After dechirping, the maximum beat frequency $f _ { b _ { m a x } }$ is determined as

$$
f _ { b } \sb { m a x } = K \tau _ { m a x } .\tag{3}
$$

Ideally, we assume that the cut-off frequency of low-pass filter (LPF) used after dechirping is equal to $f _ { b } { } _ { m a x }$ . For simplicity, we assume that the transmitted signal is reflected by point targets, neglecting the multipath effect and clutters. Besides the echo of targets, the received signal could also contain transmitted signals from other automotive radars which are regarded as interference.

![](images/a70bef70e42943659fd3f8a77bba924baf8483cae58d354cdc12f40e7aa66720.jpg)  
Fig. 1. Time domain strategy.

## 2.2 The Time Domain Strategy for Interference Avoidance

Since several methods [1], [2], [7] have been proposed to mitigate incoherent interference, we concentrate on coherent interference here, i.e., interference shares the same sweep slope and pulse repetition interval (PRI) with the victim radar.

According to the corresponding relationship of $\tau _ { m a x }$ and $f _ { b _ { m a x } } ,$ it can be inferred that if the time delay between the transmitted signal and received signal is not within the range of $[ 0 , \tau _ { m a x } ]$ , the received signal will be removed by LPF. Inspired by this, we propose the time domain strategy for interference avoidance. As depicted in Fig. 1, the radar adjusts its transmitting time to avoid interference. Practically, the transmitted signal of the victim radar is delayed by $t _ { d } ,$ which changes the beat frequency between the transmitted signal and interference so that the interference would be filtered out by LPF after dechirping. For convenience, we set a time reference here. The transmitting time delay $t _ { d }$ of the radar and the arrival time delay $\tau _ { i n t f }$ of the interference are all defined relative to the time reference.

## 2.3 Markov Decision Process Modelling of Interference Avoiding

The execution process of the joint strategy is formulated as an MDP model which can be described by the tuple $\langle \mathcal { S } , \mathcal { A } , p , r \rangle$ . The state space $\mathcal { S } = \{ \pmb { s } _ { 1 } , \pmb { s } _ { 2 } , \dots , \pmb { s } _ { N _ { \mathcal { S } } } \}$ is the set of all possible states that the radar can reach. The state ${ \pmb s } =$ $\left[ \hat { f } _ { c } , t _ { d } , S I N R \right] \in \mathcal { S }$ consists of the radar's frequency domain state $\hat { f } _ { c } \ ( \mathrm { i . e . }$ , centre frequency), time domain state $t _ { d }$ (i.e., transmitting time delay), and the SINR of the received signal. The action space $\mathcal { A }$ can be defined as $\{ a | s \stackrel { a } { \to } s ^ { \prime } , s \in \mathcal { S } , s ^ { \prime } \in$ S}, in which the action a consists of the radar's actions in the frequency domain and time domain. Given n available frequency domain states and m available time domain states, the size of $\mathcal { A }$ is $( m n ) ^ { 2 }$ . However, the size of $\mathcal { S }$ is not countable due to the SINR with continuous values. The transition probability function $p ( \pmb { s } , \pmb { a } , \pmb { s } ^ { \prime } )$ presents the probability distribution of reaching states $\pmb { s } ^ { \prime }$ from state s by taking action a. The reward function $r ( \pmb { s } , \pmb { a } , \pmb { s } ^ { \prime } )$ presents the immediate reward obtained after transitioning to state $\pmb { s } ^ { \prime }$ from state s by taking action a.

At each time step, SINR is used to evaluate the radar's action. The metric is defined as follows:

$$
S I N R = 1 0 \log _ { 1 0 } \frac { | x _ { t } | ^ { 2 } } { | x _ { i } + n | ^ { 2 } } ,\tag{4}
$$

where $\mathbf { } x _ { t } \mid \mathbf { } x _ { i } ,$ and n are respectively the beat signal of targets, interference, and noise reserved after dechirping and low-pass filtering. The immediate reward r is calculated by the SINR:

$$
r =
$$

$$
\left\{ \begin{array} { l l } { \displaystyle { \frac { 2 ( S I N R - S I N R _ { 1 } ) } { ( S I N R - S I N R _ { 1 } ) + ( S I N R _ { 2 } - S I N R _ { 1 } ) } } , ~ S I N R \geq S I N R _ { 1 } , } \\ { 0 . 1 ( S I N R - S I N R _ { 1 } ) , ~ S I N R < S I N R _ { 1 } , } \end{array} \right.\tag{5}
$$

where $S I N R _ { 1 }$ is the threshold to give positive or negative reward, which can be set based on the requirement for target detection practically. $S I N R _ { 2 }$ presents an upper bound of available SINR for reward normalization, which is usually relative to the noise level. In this paper, we assume that the SINR of the received signal can be estimated accurately, and the estimation is not going to be discussed.

A policy π is utilized to choose the action based on the current state: $\pmb { a } _ { t } = \pi ( \pmb { s } _ { t } )$ . The state-action sequence based on policy π in one episode is defined as a trajectory $\{ \boldsymbol { s } _ { 0 } , \boldsymbol { a } _ { 0 } , \boldsymbol { s } _ { 1 } , \boldsymbol { a } _ { 1 } , \ldots , \boldsymbol { s } _ { t _ { \infty } - 1 } , \boldsymbol { a } _ { t _ { \infty } - 1 } , \boldsymbol { s } _ { t _ { \infty } } \}$ $\scriptstyle { \pmb { s } } _ { 0 }$ and $\pmb { s } _ { t _ { \infty } }$ denote the initial state and the terminal state of the episode, respectively. The cumulative reward starting from time step t on this trajectory is

$$
G _ { t } ( \pi ) = \sum _ { k = t } ^ { t _ { \infty } - 1 } \gamma ^ { k - t } r _ { k + 1 } = \sum _ { k = t } ^ { t _ { \infty } - 1 } \gamma ^ { k - t } r ( s _ { k } , { \pmb a } _ { k } , { \pmb s } _ { k + 1 } ) ,\tag{6}
$$

where $\gamma \in [ 0 , 1 ]$ is the discount factor weighting the future reward. To chase a high SINR, the radar is expected to perform a trajectory getting as much cumulative reward as possible with an optimal policy which is

$$
\pi ^ { * } = \arg \operatorname* { m a x } _ { \pi } G _ { t } ( \pi ) .\tag{7}
$$

There may be more than one optimal policy, but they share the same state-action value function [10]. Here, the $\mathrm { Q }$ function $Q _ { \pi } ( \pmb { s } , \pmb { a } )$ denotes the state-action value function for a policy π which is defined as the expectation of $G _ { t }$ starting from s, taking the action ${ \pmb a } ,$ and thereafter following the policy π:

$$
\begin{array} { r l } & { \displaystyle Q _ { \pi } ( \pmb { s } , \pmb { a } ) = \mathbb { E } _ { \pi } [ G _ { t } | \pmb { s } _ { t } = \pmb { s } , \pmb { a } _ { t } = \pmb { a } ] } \\ & { \quad = \displaystyle \sum _ { s ^ { \prime } \in \mathcal { S } } p ( \pmb { s } , \pmb { a } , \pmb { s } ^ { \prime } ) \left\{ r ( \pmb { s } , \pmb { a } , \pmb { s } ^ { \prime } ) \right. } \\ & { \quad \quad \left. + \gamma \mathbb { E } _ { \pi } [ G _ { t + 1 } | \pmb { s } _ { t + 1 } = \pmb { s } ^ { \prime } ] \right\} , } \end{array}\tag{8}
$$

Then, the goal for the optimal policy $\pi ^ { * }$ is to find the optimal Q function $Q ^ { * }$ enabling the radar to choose the optimal action $\pmb { a } ^ { * }$ at each time step:

$$
\pmb { a } ^ { * } = \arg \operatorname* { m a x } _ { \pmb { a } \in \mathcal { A } } Q _ { \pi ^ { * } } ( \pmb { s } , \pmb { a } ) = \arg \operatorname* { m a x } _ { \pmb { a } \in \mathcal { A } } Q ^ { * } ( \pmb { s } , \pmb { a } ) .\tag{9}
$$

2.4 Deep Reinforcement Learning Based Implementation of the Proposed Method

We choose Q-learning to optimize the Q function for its faster convergence and sample reusability.At every time step, Q-learning updates the value function as follows:

$$
Q ( s _ { t } , \pmb { a } _ { t } ) \gets Q ( \pmb { s } _ { t } , \pmb { a } _ { t } ) + \beta \delta _ { t } ,\tag{10}
$$

where $\beta$ denotes the learning rate, and $\delta _ { t }$ is the TD error for updating:

$$
\delta _ { t } = r ( s _ { t } , \pmb { a } _ { t } , \pmb { s } _ { t + 1 } ) \qquad \\  + \gamma \operatorname* { m a x } _ { \pmb { a } _ { t + 1 } \in \mathcal { A } } Q ( \pmb { s } _ { t + 1 } , \pmb { a } _ { t + 1 } ) - Q ( \pmb { s } _ { t } , \pmb { a } _ { t } ) .\tag{11}
$$

The current state s could only present the interference situation in the current passband, but it can be inadequate for radar to make an effective decision. To provide more information about interference, we extend the state $\pmb { s } _ { t }$ to $\pmb { S } _ { t } =$ $\left[ \pmb { s } _ { t - k + 1 } , \pmb { s } _ { t - k + 2 } , \ldots , \pmb { s } _ { t } \right]$ , which contains the states of the latest k time steps within one episode. While adding more observations, the extended state $\pmb { S } _ { t }$ greatly enlarges the state space. To tackle such a complex state space, Q-network is used as the approximation of the Q function. The architecture of the network is shown in Fig. 2. At each time step, the extended state $\mathbf { } S _ { t } , \mathrm { i . e . }$ , a sequence of some recent states, is input into a gated recurrent unit (GRU) layer to extract information about interference. Then, the output of the GRU layer is input into dense layers to calculate the Q values of all actions.

![](images/6c00513f3871fb8ca3827acc0902a63f1253a0434199c4018b2f6be76a840fd3.jpg)  
Fig. 2. The architecture of Q-network

In training, several skills are employed to train the $\mathrm { Q - }$ network:

1) Double Q-networks: Two networks, evaluation network $Q _ { e v a l }$ and target network $Q _ { t a r } ,$ are used to relieve training instability. Specifically, $Q _ { e v a l }$ will be updated every time step while $Q _ { t a r }$ will be updated to $Q _ { e v a l }$ by an interval of numbers of time steps. When updating $Q _ { e v a l } ,$ $Q _ { t a r }$ is used to calculate the value of $\pmb { a } _ { t + 1 }$ chosen by $Q _ { e v a l } . \delta _ { t }$ for updating is rewritten as

$$
\delta _ { t } = r ( \pmb { s } _ { t } , \pmb { a } _ { t } , \pmb { s } _ { t + 1 } )
$$

$$
+ \gamma Q _ { t a r } \left( \arg \operatorname* { m a x } _ { { a _ { t + 1 } \in \mathcal { A } } } Q _ { e v a l } ( s _ { t + 1 } , \pmb { a } _ { t + 1 } ) \right)\tag{12}
$$

and the parameters of Qeval, w, is updated by

$$
\pmb { w }  \pmb { w } - \beta \frac { \partial \delta _ { t } ^ { 2 } } { \partial \pmb { w } } .\tag{13}
$$

2) €ε-greedy exploration: To avoid the Q-network being trapped in suboptimal actions, the radar will randomly choose actions by the exploring probability $\epsilon \in [ 0 , 1 ]$

$$
\pmb { a } _ { t } = \left\{ \begin{array} { l } { \arg \operatorname* { m a x } _ { { \pmb { a } } _ { t } \in \mathcal { A } } Q _ { e v a l } ( { \pmb { s } } _ { t } , { \pmb { a } } _ { t } ) } \\ { r a n d o m a c t i o n \mathrm { ~ w i t h ~ } } \end{array} \right.\tag{14}
$$

3) Experience replay: $\pmb { e } _ { t } = [ \pmb { S } _ { t } , \pmb { a } _ { t } , \pmb { S } _ { t } , \boldsymbol { r } _ { t + 1 } ]$ is defined as the transition of the time step t. The replay buffer stores a number of recent transitions. If the number of stored transitions reaches the upper limit, the oldest transition will be replaced by the latest one. At every time step, $Q _ { e v a l }$ is trained on a batch of transitions randomly picked from the replay buffer. Besides improving sample efficiency, experience replay can also break the correlation among consecutive samples that could harm the training.

## 3 Numerical Simulation

## 3.1 Simulation Settings

3.1.1 Radar Settings: Parameter settings of the victim radar are listed in Table 1. We assume 3 available states for radar in both frequency and time domains. One-hot vector is used to represent these parameter states. The interference shares identical sweep parameters with the victim radar, including centre frequency, sweep slope, sweep duration, bandwidth, and PRI.

Table 1 Parameter settings of victim radar
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Centre frequency  $\hat { f } _ { c }$  [GHz] 一 Sweep slope [MHz/us]</td><td>76.5, 77.0, 77.5 10</td></tr><tr><td>Sweep duration [us]</td><td>50</td></tr><tr><td>Bandwidth [MHz]</td><td>500</td></tr><tr><td>Pulse repetition interval [us]</td><td>60</td></tr><tr><td>Chirp number per frame</td><td>128</td></tr><tr><td>Sampling frequency [MHz]</td><td></td></tr><tr><td>Maximum detection range [m]</td><td>20</td></tr><tr><td></td><td>120</td></tr><tr><td>Maximum beat frequency [MHz]</td><td>8</td></tr><tr><td>Maximum delay  $\tau _ { m a x }$  [us]</td><td>0.8</td></tr><tr><td>Time domain state  $t _ { d } \ [ \times \tau _ { m a x } ]$ </td><td>0,1,2</td></tr></table>

3.1.2 Scenario Settings: Simulation settings of training and test are shown in Table 2. Here, $\pmb { \mathcal { U } } \{ \pmb { b } _ { 1 } , \pmb { b } _ { 2 } , \dots , \pmb { b } _ { l } \}$ denotes the discrete uniform distribution on the finite set $\{ b _ { 1 } , b _ { 2 } , \ldots , b _ { l } \}$ and $\pmb { \mathcal { U } } ( \pmb { b } _ { 1 } , \pmb { b } _ { 2 } )$ denotes the continuous uniform distribution on the interval $( b _ { 1 } , b _ { 2 } )$ . Since the arrival delay of the interference signal accounts for both the distance and transmitting time of the interference source, the delay time $\pmb { \tau } _ { i n t f }$ is given directly for simplicity. Here, static scenario and dynamic scenario are defined. In the simulation, the targets and interference will be randomly initialized at the beginning of each episode. An episode has a number of time steps, and only one frame of the signal will be transmitted, received, and processed in each time step. The frame's duration is less than 10 ms, which is too short for moving targets and interference sources to significantly influence the signal in the passband. Therefore, the duration of each time step is neglected in the static scenario, which means that both targets and interference remain constant in one episode. In the dynamic scenario, the interval between time steps is enlarged so that the relative motion of targets and interference sources could have a noticeable effect. For instance, one interference can move into or out of a passband, which could influence the radar's behaviour. Specifically, the distance of the target and the delay time of interference will be updated before each time step:

$$
d ( t _ { n } ) = d ( t _ { n } ) + v _ { t a r g e t } \Delta t ,\tag{15}
$$

$$
\tau _ { i n t f } ( t _ { n } ) = \tau _ { i n t f } ( t _ { n - 1 } ) + \frac { v _ { i n t f } \Delta t } { c } ,\tag{16}
$$

where $d ( t _ { n } )$ and $\tau _ { i n t f } ( t _ { n } )$ denote the distance of the target and the delay time of interference at time step $t _ { n } . v _ { t a r g e t }$ and $v _ { i n t f }$ are the relative velocities of the target and interference source. For simplicity, the amplitudes and velocities of targets and interference would not change in one episode. If the distance of a target or $\tau _ { i n t f }$ of interference is out of the range shown in Table 2, the item will be replaced by a new one randomly initialized.

Table 2 Simulation settings
<table><tr><td colspan="2">Parameter</td><td colspan="2">Value</td></tr><tr><td rowspan="5">Point-like target</td><td>Number</td><td>Training Test U{1, 2,3}</td></tr><tr><td>Amplitude</td><td>U(0.5,1.5)</td></tr><tr><td>Distance [m]</td><td>U(0.3,120)</td></tr><tr><td>Velocity relative to</td><td></td></tr><tr><td>the victim radar [m/s] Number</td><td>U(-16,16) P(12) 6～18</td></tr><tr><td rowspan="4">Interference</td><td>Amplitude</td><td>U(1,12)</td></tr><tr><td>Velocity relative to</td><td></td></tr><tr><td>the victim radar [m/s]</td><td>U(-32,32)</td></tr><tr><td>Delay time  $[ \times \tau _ { m a x } ]$ </td><td>U(0,3)</td></tr><tr><td colspan="2">Signal-to-noise ratio [dB] Time steps per episode Time step interval [ms]</td><td>10 40 200</td></tr></table>

3.1.3 RL Settings: The settings of RL are listed in Table 3. The following radar agents are set in training and test:

1) Radar-Fixed: The agent's parameter state $\left( \hat { f } _ { c } , t _ { d } \right)$ are fixed to (77 $\mathrm { G H z } , \tau _ { m a x } )$

2) Radar-F: The agent executes frequency hopping, but its $t _ { d }$ is fixed to $\tau _ { m a x }$

3) 3) Radar-T: The agent executes the time domain strategy, but its $\hat { f } _ { c }$ is fixed to 77 GHz.

The Q-network consists of one GRU layer and two dense layers. A ReLU activation is used after the first dense layer. The input of the Q-network is the one-hot vector of the current parameter state concatenated with the SINR, and the output is the Q-values of each available parameter states. So the output shapes of Radar-F or Radar-T, i.e., the neuron numbers of the second dense layer, is 3. During training, the learning rate $\beta$ and the exploration probability ∈ are exponentially decaying to the minimum episode by episode.

Table 3 RL settings
<table><tr><td colspan="2">Item</td><td>Value</td></tr><tr><td rowspan="3">Q-network architecture</td><td>Layer</td><td>Number of neurons</td></tr><tr><td>GRU</td><td>16</td></tr><tr><td>Dense 1 Dense 2</td><td>32 3</td></tr><tr><td> $( S I N R _ { 1 } , S I N R _ { 2 } )$ </td><td>[dB]</td><td>(0,11)</td></tr><tr><td colspan="2"></td><td>0.99</td></tr><tr><td colspan="2"> $\mathbf { \Sigma } _ { \beta } ^ { \gamma }$ </td><td>0.01~0.00001</td></tr><tr><td colspan="2">€</td><td>1~ 0.05</td></tr><tr><td colspan="2">Maximum capacity of  $\pmb { S } _ { t }$  Replay buffer capacity</td><td>20 time steps</td></tr><tr><td colspan="2">Replay batch size</td><td>50000 4×32</td></tr><tr><td colspan="2"> $Q _ { t a r }$  updating interval</td><td>200 time steps</td></tr></table>

## 3.2 Simulation Results

The random initialization of interference in each episode leads to a large variance during sampling, subsequently making RL training difficult and unstable. To deal with the instability, the number of time steps per episode is reduced in training, and it takes tens of thousands of episodes for agents to reach convergence. In particular, the radar agents are first trained to converge in the static scenario and then retrained in the dynamic scenario. After training, the radar agents are tested with the interference number varying from 6 to 18. For each number of interference, the agents are tested for one thousand episodes in both dynamic and static scenarios. The test results are shown in Fig. 3, and the overall performance of interference avoidance is demonstrated in Table 4. The avoidance ratio is defined as the proportion of the time steps without interference in the passband. Besides the average SINR, the avoidance ratio presents the interference avoiding performance of the radar agent.

![](images/8433a65637f8ba503e5d44e322d02df3f5f6d2496e21479af51b1edd07216f46.jpg)  
(a)

![](images/103af78be283a8e59591b0646972b7d813bf83dcee1c0ba32871dcdd45626c05.jpg)  
(b)  
Fig. 3. The test result versus various numbers of interference. (a) Average SINR in the static scenario. (b) Average SINR in the dynamic scenario.

Table 4 The overall performance of interference avoidance
<table><tr><td rowspan="2">Radar agent</td><td colspan="2">SINR [dB]</td><td colspan="2">Avoidance ratio [%]</td></tr><tr><td>static</td><td>dynamic</td><td>static</td><td>dynamic</td></tr><tr><td>Fixed</td><td>-5.23</td><td>-5.96</td><td>18.64</td><td>16.30</td></tr><tr><td>F</td><td>0.65</td><td>-0.88</td><td>39.29</td><td>33.70</td></tr><tr><td>T</td><td>0.76</td><td>-0.51</td><td>39.86</td><td>35.22</td></tr></table>

Among the three agents, Radar-Fixed has the worst performance on interference avoidance. Compared to Radar-Fixed, Radar-F and Radar-T all perform much better. Notably, their performance is almost the same in the static scenario, which proves the ability of the proposed time domain strategy. The reason is that the numbers of available states in the time and frequency domains are the same, and the interference is distributed uniformly in both domains when initialized. In the dynamic scenario, all these agents suffer performance degradation due to the continuously changing interference. However, Radar-T slightly outperforms Radar-F. The dynamic of interference in the time domain is more regular than that in the frequency domain, so it is easier to avoid interference in the time domain, especially when facing more interference.

Fig. 4 shows the state transitions and the performance on SINR of the three radar agents in one episode as the interference number is 12 in the dynamic scenario. The average SINR of Radar-Fixed, Radar-F, and Radar-T are -17.69 dB, 0.33 dB, and 1.33 dB, respectively. Both Radar-F and Radar-T will react immediately if a sudden drop in SINR caused by dynamic interference occurs. They almost always get a higher SINR than Radar-Fixed during the whole episode. However, Radar-T performs more stably than Radar-F. Since it is more difficult to predict the dynamic of interference, Radar-F switches its parameter state much more frequently, even if it does not suffer a low SINR.

## 4 Conclusion

In this paper, we propose a non-cooperative time domain strategy to avoid interference for FMCW automotive radar. The proposed strategy is implemented by utilizing Markov Decision Process model and deep reinforcement learning. The numerical simulation demonstrates the effectiveness of the method. The proposed time domain strategy shows a better and more stable performance than frequency hopping in the dynamic scenario.

## 5 Acknowledgements

Acknowledgements should be placed after the conclusion and before the references section. Details of grants, financial aid and other special assistance should be noted.

## 6 References

[1] Xu, Z., Xue, S., and Wang, Y.: 'Incoherent Interference Detection and Mitigation for Millimeter-Wave FMCW Radars ', Remote Sensing, vol. 14, no. 19, 2022.

[2] Wang, J., Li, R., He, Y., et al.: 'Prior-Guided Deep Interference Mitigation for FMCW Radars', IEEE Transactions on Geoscience and Remote Sensing, vol. 60, pp. 1-16, 2022.

[3] Luo, T.-N., Wu, C.-H. E., and Chen,Y.-J. E.: 'A 77-ghz cmos automotive radar transceiver with anti-interference function', IEEE Transactions on Circuits and Systems I: Regular Papers, vol. 60, no. 12, pp. 3247–3255, 2013.

[4] Kitsukawa, Y., Mitsumoto, M., Mizutani, H., et al.: 'An Interference Suppression Method by Transmission Chirp Waveform with Random Repetition Interval in Fast-Chirp FMCW Radar', 2019 16th European Radar Conference (EuRAD), Paris, France, 2019, pp. 165-168.

[5] Uysal, F.: 'Phase-Coded FMCW Automotive Radar: System Design and Interference Mitigation', IEEE Transactions on Vehicular Technology, vol. 69, no. 1, pp. 270–281, 2020.

[6] Thornton, C. E., Kozy, M. A., Buehrer, R. M., A. F. et al.: 'Deep Reinforcement Learning Control for Radar Detection and Tracking in Congested Spectral Environments', IEEE Transactions on Cognitive Communications and Networking, vol. 6, no. 4, pp. 1335– 1349, 2020.

[7] Liu, P., Liu, Y., Huang, T., et al.: 'Decentralized Automotive Radar Spectrum Allocation to Avoid Mutual Interference Using Reinforcement Learning', IEEE Transactions on Aerospace and Electronic Systems, vol. 57, no. 1, pp. 190–205, 2021.

[8] Khoury, J., Ramanathan, R., McCloskey, D., et al.: 'RadarMAC: Mitigating Radar Interference in Self-Driving Cars', 2016 13th Annual IEEE International Conference on Sensing, Communication, and Networking (SECON), London, UK, 2016, pp. 1-9.

[9] Aydogdu, C., Keskin, M. F., Garcia, N., et al.: 'RadChat: Spectrum Sharing for Automotive Radar Interference Mitigation', IEEE Transactions on Intelligent Transportation Systems, vol. 22, no. 1, pp. 416–429, 2021.

[10] Sutton, R. S., and Barto, A. G., 'Reinforcement Learning: An Introduction', MIT press, 2018.

![](images/963e8c534ec5a80c20164b3d409e40b7ca084e9193966c510624c4e26f043e82.jpg)  
Fig. 4. Test result of one episode in the dynamic scenario. Parameter state index setting is {Index : $( \widehat { f } _ { c } [ G H z ] , t _ { d } [ \times \tau _ { m a x } ] ) \ : |$ 0 : (76.25, 1), 1 : (76.75, 0), 2 : (76.75, 1), 3 : (76.75, 2), 4 : (77.25, 1)}.