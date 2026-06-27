# Reinforcement Learning for Adaptable Bandwidth Tracking Radars

ERSIN SELVI

R. MICHAEL BUEHRER

Virginia Polytechnic Institute and State University, Blacksburg, VA, USA

ANTHONY MARTONE

KELLY SHERBONDY

U.S. Army Research Laboratory, Adelphi, MD, USA

In this article,<sup>1</sup> we examine a cognitive radar that must coexist with communication systems. Specifically, we model a cognitive radar’s adaptation to the communication system as a Markov decision process (MDP) and then apply reinforcement learning to solve the resulting optimization problem. More specifically, we learn the environment model and then apply policy iteration to determine the optimal policy. The radar environment consists of a single moving target and a communication system that uses the same bands as the radar. The communication system is modeled using several different transmission behaviors: constant, intermittent, triangular frequency sweep, sawtooth frequency sweep, frequency hop, pseudorandom frequency hop, and direction-dependent interference. We demonstrate how the MDP framework and reinforcement learning can be used to help the radar determine actions (i.e., transmission strategies) to maximize its own performance.

Manuscript received May 29, 2019; revised December 11, 2019; released for publication March 12, 2020. Date of publication April 16, 2020; date of current version October 9, 2020.

DOI. No. 10.1109/TAES.2020.2987443

Refereeing of this contribution was handled by A. Charlish.

This work was supported by the Army Research Office (ARO) under Grant W911NF-17-2-0021.

Authors’ addresses: Ersin Selvi and R. Michael Buehrer are with Wireless@VT, Bradley Department of Electrical and Computer Engineering, Virginia Polytechnic Institute and State University, Blacksburg, VA 24061 USA, E-mail: (buehrer@vt.edu); Anthony Martone and Kelly Sherbondy are with the Army Combat Capabilities Development Command, U.S. Army Research Laboratory, Adelphi, MD 20783 USA, E-mail: (kelly.d.sherbondy.civ@mail.mil). (Corresponding author: R. Michael Buehrer.)

<sup>1</sup>Portions of this work were presented at the 2018 IEEE Radar Conference [1].

## I. INTRODUCTION AND MOTIVATION

The radio-frequency electromagnetic spectrum is a precious resource where an abundance of users are competing for finite and scarce bandwidth [2]. This spectrum has found uses in radar, radio and television broadcasting, navigation, and sensing applications [2]. The recent spectrum auction and reallocation [3] have further motivated the need for more effective spectrum sharing technologies [2], between systems and devices with the same application, or even different applications such as radars and communication systems. The concept of a “more intelligent” communication system was introduced by Mitola nearly 20 years ago, in which the cognitive radio was envisioned to be able to manipulate its parameters and settings to best serve the needs of its users while also coexisting with other communication systems [4].

In a similar respect, cognitive radar has emerged as a ground-breaking solution to solve the challenges facing radar today [5]. Traditional/contemporary radars are designed based on predetermined targets for signal-tointerference-plus-noise ratio (SINR) and maximum operating range, “with target and clutter models that represent averaged, anticipated responses [6].” The resulting design uses fixed parameters, and lacks flexibility in adapting to varying target and environment conditions (e.g., varying interference) [6]. When there are variations in the target or environment that depart from the assumed design conditions, the radar’s performance will be suboptimal [6]. Generally speaking, a traditional radar can only achieve optimal performance in one scenario (the scenario for which it was designed), but is unable to achieve optimal performance over all possible scenarios. Cognitive radar aims to free traditional radars from these restrictions, allowing them (ideally) to perform optimally across all scenarios.

Current research into cognitive radar is split into two main thrusts:

1) enhanced radar functionality and performance, and   
2) spectrum sharing.

Research into more enhanced functions and performance include classification of aircraft targets from inverse synthetic aperture radar (ISAR) images [7], [8], improving performance at the physical layer via transmit waveform optimization [9], [10], scheduling radar tasks through higherlevel radar resource management [11], [12], improvements to radar detection and tracking [13]–[15], and improvements to sensor management [16]–[18].

Spectrum sharing research (involving radars) includes (for example) developing policies that categorize sharing arrangements between users as either coexistence or primarysecondary [19]. Spectrum sharing between air traffic control radars and cellular system has been studied in [20] and [21], which exploit the fact that the radar is rotating. The cellular system exploits and transmits during these time slots, enabling secondary use while avoiding mutual interference. Cognitive radars can also use optimization to modify the center frequency and bandwidth to mitigate the risk of mutual interference between a radar and communication systems [22]–[25]. Additional applications include waveform notching to further enhance spectrum sharing capabilities [26], [27].

In this article, we investigate a target tracking radar that must coexist with a communication system. To perform the investigation, we use the perception-action cycle and cognitive radar framework discussed in [28]. The perceptionaction cycle is one of the components of Fuster’s paradigm of (biological) cognition [29], [30]; sensors and processors are used to develop a perception of the environment, which is then used to take an action. The action will have some measurable effect on the environment, which will again be sensed and processed to form a new perception, on which a new action will be taken [28]. This process repeats as a cycle; the “sensory or internal signals lead to actions that generate feedback that regulates further actions, and so on” [30]. The perception-action cycle works reciprocally with memory [28]; the memory stores the experiences from which the radar can learn from and make new decisions.

The model considered in our current development uses the Markov decision process (MDP) and reinforcement learning to learn actions that mitigate interference between the radar and communication systems while optimizing radar performance. MDPs model sequential decision problems in which “an agent’ s utility depends on a sequence of decisions” [31]. The goal of this application is to enable the radar to learn from offline training data instead of having to perform online optimization during each radar cycle. The motivation for using MDPs is based on the fact that most communication systems can be modeled as finite-state machines [32]. Further, the reward structure of MDPs is flexible, allowing system designers to emphasize interference avoidance behavior as desired. The perceptionaction cycle manifests as the instantaneous rewards, which evaluates actions taken by the radar and its effect on the environment. The memory manifests as the reward and transition probability functions, which contain all of the data the radar has seen during training.

More specifically, the current investigation builds on initial work presented in [1], which introduced the idea of using MDPs to model the coexistence problem. This article expands the prior contribution in [1] by providing a more comprehensive discussion and mathematical model for the MDP, investigating additional simulations for different radar and target scenarios, and providing a direct comparison of the MDP with a dynamic spectrum access technique. In more detail, we demonstrate:

1) an MDP that can be successfully used to model spectrum occupancy for both deterministic and stochastic time-frequency occupancy patterns;

2) an MDP that can be successfully used to model spectrum occupancy that is dependent on the target position;

3) the cognitive radar that uses the MDP model to successfully learn the time-frequency spectral occupancy pattern of the interference;

4) an MDP model for machine learning that can be successfully used to control the radar’s behavior (i.e., spectral occupancy) to optimize performance for various performance goals (e.g., interference avoidance, bandwidth maximization or trading the two) with both deterministic and stochastic time-frequency occupancy patterns.

In this initial exploration of using MDPs to model the perception-action cycle, we ignore estimation errors of the position and velocity information. Clearly, these variables will have an impact, but we wish to consider the usefulness of the model before bringing in these important factors. Instead, we consider a direct analysis of SINR and bandwidth for performance evaluation.

Section II introduces the proposed MDP model. Simulations are presented in Section III that examine multiple interference behaviors. The interference behavior types include the following:

1) constant interference;

2) intermittent interference;

3) triangular frequency sweep;

4) sawtooth frequency sweep;

5) pseudorandom frequency hop; and

6) direction-dependent interference.

These interference types were chosen as they represent possible scenarios that a radar could encounter. Section IV compares the proposed radar with a radar based on pure interference avoidance. Finally, Section V concludes the article.

## II. PROPOSED SYSTEM MODEL

The focus of this article is applying the MDP framework to the radar tracking problem. To prevent the state space from becoming intractably large, we make simplifying assumptions about the radar scene. The target is a simple point target and is moving generally in a cross-range direction relative to the radar, although the trajectory on each training run is random. The interferer is a communication system, which can occupy one or more bands at a time, is physically stationary and (except for the direction-dependent interferer) location independent (i.e., neither the interferer nor the target’s position with respect to the radar affects the interference sensed by the radar). Only the power level of the interference is considered in this development since it directly affects the SINR. The type of interference waveform is not considered. The environment is simple such that clutter is negligible and the radar returns are not subject to multipath or atmospheric effects (e.g., rain) other than the free-space path loss given by the radar range equation. The radar uses a linear frequency modulated (LFM) chirp waveform with the appropriate time bandwidth product. Also, the radar can perfectly determine Doppler shift and target velocity, and uses that perfect knowledge to account for the range-Doppler coupling effect as a result of using the LFM waveform.

## A. Markov Decision Processes

Since the heart of our approach is an MDP, we first briefly describe this decision process. MDPs are used to model planning for an autonomous agent in an uncertain environment [33]–[35]. MDPs are popular in two sub-fields within artificial intelligence, probabilistic planning and reinforcement learning [33]. The probabilistic planning literature focuses on developing computationally efficient approaches to solve MDPs, with the assumption that complete knowledge of the MDP is available [36]. Reinforcement learning, however, is a more difficult problem in which the agent starts with no prior knowledge of the MDP and has to learn from experience by interacting and experimenting with its environment to gain knowledge about how to optimize its behavior [33], [36]. The work in this article follows the reinforcement learning type in which our radar (the agent) learns characteristics of its environment through experience.

An MDP is specified by the tuple - , , , , γ . is the set of all possible states in the model, sometimes called the state space. A state $s \in S$ is a unique characterization of environment information [36], which in our case is a binary vector representing the presence or absence of interference in each frequency band. The action space $\mathcal { A }$ is the set of all actions that can be taken by the agent to control or change the state [36]. In our problem, the action space includes the frequency bands occupied by the radar. The transition probability function $\boldsymbol { \mathcal { T } } ( s , a , s ^ { \prime } )$ , is a description of the probability that an agent in state $s \in S$ will transition to another state $s ^ { \prime } \in \mathcal { S }$ when taking action $a \in { \mathcal { A } }$ . The Markovian attribute of an MDP means the future state as the result of an action does not depend on previous actions and states; the future state only depends on the current state and current action [36]

$$
\begin{array} { r } { \mathbb { P } \left( s _ { t + 1 } ~ \vert ~ s _ { t } , a _ { t } , s _ { t - 1 } , a _ { t - 1 } , \dots \right) = \mathbb { P } \left( s _ { t + 1 } ~ \vert ~ s _ { t } , a _ { t } \right) } \\ { = \mathcal { T } \left( s _ { t } , a , s _ { t + 1 } \right) . } \end{array}\tag{1}
$$

Note that, in this article, the transition function is assumed to be unknown in advance, and we use a frequentist approach to estimate it. The frequentist approach calculates the probability of an event ε via $\begin{array} { r } { \mathbb { P } ( \varepsilon ) = \operatorname* { l i m } n  \infty \frac { n _ { \varepsilon } } { n } . } \end{array}$ where $n _ { \varepsilon }$ is the number of times event ε occurs, n is the total number of trials, and the ratio $n _ { \varepsilon } / n$ is known as the relative frequency of event ε [37]. In our implementation, the probability is computed for each action a as such: $\mathcal { T } ( s , a , s ^ { \prime } ) = \mathbb { P } ( s ^ { \prime } \mid s ) = N _ { s ^ { \prime } } / N _ { s }$ , where $N _ { s }$ is the number of times the agent is in state s, and $N _ { s ^ { \prime } }$ is the number of times the agent transitions to state $s ^ { \prime }$ from state s.

The reward function $\textstyle { \mathcal { R } } ( s , a , s ^ { \prime } )$ is a description of the average reward accumulated by the agent when the agent was in state s, performed action $^ { a , }$ and transitioned to state $s ^ { \prime } .$ The values in the reward function could be positive (the usual connotation of reward) or negative (punishment/penalty) [36]. Like the transition function, the reward function is unknown in advance and is thus estimated in a manner similar to the transition function.

The discount factor $\gamma \in [ 0 , 1 ]$ models the preference for current rewards versus future rewards [31]. When $\gamma$ is close to 0, the agent will prefer immediate rewards and future rewards will be heavily discounted [31]. When $\gamma$ is close to 1, the agent will prefer the distant, long-term rewards. Discounting is a good model of animal and human behavior [31], and helps ensure that the utility of a state sequence is finite. The variables $\pi$ and $\pi ^ { * }$ represent the policy and optimal policy, respectively.

A value function (also known as utility)<sup>2</sup> can be used to describe “how good it is for the agent to be in a certain state,” given a particular policy π [36]

$$
V ^ { \pi } ( s ) = \mathbb { E } \bigg [ \sum _ { k = 0 } ^ { \infty } \gamma ^ { k } R _ { t + k } \bigg | \pi , s _ { t } = s \bigg ]\tag{2}
$$

where <sup>E</sup>[x] is the expectation of x and $R _ { t + k }$ is the reward obtained at time $t + k .$ . This can be written in terms of $\boldsymbol { \mathcal { T } } ( s , a , s ^ { \prime } )$ and $\textstyle { \mathcal { R } } ( s , a , s ^ { \prime } )$ [36]

$$
V ^ { \pi } ( s ) = \sum _ { s ^ { \prime } } \mathcal { T } \left( s , a , s ^ { \prime } \right) \left( \mathcal { R } \left( s , a , s ^ { \prime } \right) + \gamma V ^ { \pi } ( s ^ { \prime } ) \right) \bigg \rvert _ { a = \pi ( s ) }\tag{3}
$$

where the value function $V ^ { \pi } ( s )$ for the current state s, and given any policy π can be described in terms of the value function for the future state $s ^ { \prime } ,$ , discount factor $\gamma .$ , and the transition probabilities $\tau .$ . Equation (3) is also known as the Bellman Equation [36].

The optimal policy $\pi ^ { * }$ will be the one that results in the agent receiving the most reward, such that its value function is greater than that of any other possible realization, or in other words, $V ^ { \pi ^ { * } } ( s ) \geq V ^ { \bar { \pi } } ( s ) \forall _ { \pi , \cdot }$ <sub>s</sub> [36]. The value function for the optimal policy is defined and known as the Bellman optimality equation [36]

$$
\begin{array} { r l } & { V ^ { \pi ^ { * } } ( s ) = V ^ { * } ( s ) } \\ & { \quad \quad = \underset { a \in \mathcal { A } } { \operatorname* { m a x } } \sum _ { s ^ { \prime } \in \mathcal { S } } \mathcal { T } ( s , a , s ^ { \prime } ) \left( \mathcal { R } ( s , a , s ^ { \prime } ) + \gamma V ^ { \pi } ( s ^ { \prime } ) \right) } \end{array}\tag{4}
$$

from which, the optimal policy is derived as [36]

$$
\pi ^ { * } ( s ) = \underset { a \in \mathcal { A } } { \arg \operatorname* { m a x } } \sum _ { s ^ { \prime } \in \mathcal { S } } \mathcal { T } ( s , a , s ^ { \prime } ) \left( \mathcal { R } ( s , a , s ^ { \prime } ) + \gamma V ^ { \pi } ( s ^ { \prime } ) \right) .\tag{5}
$$

It is worth noting that in drawing connections between cognitive neuroscience and cognitive systems in [38], Haykin and Fuster link Bellman’s dynamic programming as “the mathematical basis for cognitive control.”

There are two primary methods for calculating the optimal policy, value iteration and policy iteration; the work presented in this article uses policy iteration. The solver used is from MDPToolbox, a MATLAB toolbox developed by researchers from INRA Toulouse [39]. Policy iteration begins from some initial policy $\pi _ { 0 }$ and alternates between two steps: policy evaluation and policy improvement [31].

![](images/efd5dcda3974a3b7054e96345afa3114f82f73e18502cca329feba29daacf179.jpg)  
Fig. 1. Example radar scene with cross-range trajectory.

Policy evaluation calculates the utility of all states, given a policy π [31]

$$
V ^ { \pi } ( s ) = \mathbb { E } \left[ \sum _ { k = 0 } ^ { \infty } \gamma ^ { k } R _ { t + k } \bigg | \pi , s _ { t } = s \right] .\tag{6}
$$

More specifically, policy evaluation is done using (3). Policy improvement then uses the utility function $V ^ { \pi } ( s )$ to choose the action a for the current state that maximizes the expected utility of the subsequent state s<sup></sup> [31]; thereby, creating an updated policy π<sup></sup> [36]

$$
\pi ^ { \prime } ( s ) = \underset { a \in \mathcal { A } } { \arg \operatorname* { m a x } } \sum _ { s ^ { \prime } \in \mathcal { S } } \mathcal { T } \left( s , a , s ^ { \prime } \right) \left( \mathcal { R } ( s , a , s ^ { \prime } ) + \gamma V ^ { \pi } ( s ^ { \prime } ) \right)\tag{7}
$$

Then, the new policy $\pi ^ { \prime }$ is used to compute a new value function $V ^ { \pi ^ { \prime } }$ (via policy evaluation), the result of which is used to create a newer policy (via policy improvement) [36]. This process repeats until the policy can no longer be improved, meaning the optimal policy $\pi ^ { * }$ has been obtained [36]. It should be noted that although this iteration procedure will converge in general to the optimum policy, with a fixed number of iterations and an estimated model (transition matrix), it may not always do so. However, to the best of our knowledge, convergence appears to have been achieved for all simulations examined in this research.

## B. Radar Environment

An example radar scene is shown in Fig. 1. The red circles represent position states (cells), and the blue line an example target trajectory. The radar environment is defined by a set of possible position states ${ \mathcal P } ,$ , and a set of possible velocity states

$$
\mathcal { P } = \{ \mathbf { r } _ { 1 } , ~ \mathbf { r } _ { 2 } , ~ . ~ . ~ . ~ , ~ \mathbf { r } _ { \rho } \}\tag{8}
$$

$$
\mathcal { V } = \{ \mathbf { v } _ { 1 } , \mathbf { v } _ { 2 } , \mathbf { \Omega } . ~ . ~ . ~ , \mathbf { v } _ { \nu } \}\tag{9}
$$

where $\rho$ is the number of possible positions and ν is the number of possible velocities. Each of the $\mathbf { r } _ { i }$ is a $1 \times 3$ vector, defined as

$$
\mathbf { r } _ { i } = [ r _ { x } , ~ r _ { y } , ~ r _ { z } ]\tag{10}
$$

where $r _ { x } , r _ { y } , r _ { z }$ are the position components in the crossrange, down-range, and vertical dimensions, respectively. Like the positions, each of the $\mathbf { v } _ { i }$ is a $1 \times 3$ vector defined

$$
\mathbf { v } _ { i } = [ v _ { x } , ~ v _ { y } , ~ v _ { z } ]\tag{11}
$$

where $v _ { x } , v _ { y } , v _ { z }$ are the velocity components. The radar is located at the origin, (0, 0, 0). Note the plot is a top-down view of the radar scene, and therefore the vertical dimension is not shown.

The interference states $\mathbf { \Theta } _ { \Theta }$ are defined as

$$
\boldsymbol { \Theta } = \{ \pmb { \theta } _ { 1 } , \pmb { \theta } _ { 2 } , \dots , \pmb { \theta } _ { M } \}\tag{12}
$$

where M is the number of unique interference states. Given N frequency bands, the number of unique interference states is $M = 2 ^ { N }$ . Each of the $\pmb \theta _ { i }$ is a $1 \times N$ vector defined as

$$
\pmb { \theta } _ { i } = [ \theta _ { 1 } , \theta _ { 2 } , \dots , \theta _ { N } ]\tag{13}
$$

where the $\theta _ { i } \in \{ 0 , 1 \}$ indicates if an interferer exists in the ith band. As an example, $\pmb { \theta } = [ 0 1 0 1 ]$ means there are 4 bands, of which the 2nd and 4th bands have interference present.

For our model, the set denotes all the combinations of target position states, target velocity states, and interference states. The total number of states is $N _ { S } = \rho \nu 2 ^ { N }$ . The actions are defined as

$$
\mathcal { A } = \{ \pmb { a } _ { 1 } , \pmb { a } _ { 2 } , \ldots , \pmb { a } _ { N _ { A } } \}\tag{14}
$$

where $N _ { A }$ is the number of actions. Each of the a is a $1 \times N$ vector defined as

$$
\pmb { a } _ { i } = [ \alpha _ { 1 } , \alpha _ { 2 } , \dots , \alpha _ { N } ]\tag{15}
$$

where the $\alpha _ { i } \in \{ 0 , 1 \}$ indicates whether or not the radar has selected a particular band in which to transmit its waveform. For example, $\pmb { a } = [ 1 1 1 0 ]$ means there are 4 bands, and the lowest three bands are used by the radar. Valid actions are those that use only contiguous groups of bands.<sup>3</sup> Examples of valid actions include [0 0 0 1], [0 1 1 0], [1 1 1 1], but [1 0 0 1] and [1 1 0 1] are not valid actions. It can be shown.<sup>4</sup> that the number of valid actions is $N _ { A } = [ N ( N + 1 ) ] / 2$

The transition probability function is defined as follows: $\mathcal { T } ( s , a , s ^ { \prime } ) : N _ { S } \times N _ { A } \times N _ { S } \to [ 0 ,$ 1], where the first dimension represents the current state and the third dimension represents the future state, and all of its values are bounded on [0,1]. Similarly, the reward function is defined as $\mathcal { R } ( s , a , s ^ { \prime } ) : N _ { S } \times N _ { A } \times N _ { S } \to \mathbb { R }$ , where its values are real numbers. On each iteration of the simulation, after the future state $s _ { t + 1 }$ is determined, the reward for that state $R ( s _ { t + 1 } )$ based on action $a _ { t }$ is computed. The instantaneous reward is determined from the reward structure, which considers SINR and amount of bandwidth used by the radar. Note that reward is based on current conditions, whereas actions are based on the immediately preceding conditions. In other words, it is assumed that the delay between sensing and transmission is sufficient to allow for a change in conditions. The reward structure provides positive reward for higher SINR (up to some maximum value) and increased bandwidth usage, while penalizing negative SINR. Note that SINR was calculated based on an assumed transmit power, radar cross-section, target range, noise floor, and fixed interference power. The SINR varied only based on the target range.

TABLE I  
Assumed Parameters for the Radar and Communication Systems
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Coherent Processing Interval SNR at Maximum Range</td><td rowspan=1 colspan=1>3dB</td></tr><tr><td rowspan=1 colspan=1>Pulse Repetition Frequency</td><td rowspan=1 colspan=1>2000</td></tr><tr><td rowspan=1 colspan=1>Waveform</td><td rowspan=1 colspan=1>Linear Frequency Modulation</td></tr><tr><td rowspan=1 colspan=1>Pulse Width</td><td rowspan=1 colspan=1>10µs</td></tr><tr><td rowspan=1 colspan=1>Maximum Bandwidth</td><td rowspan=1 colspan=1>100MHz</td></tr><tr><td rowspan=1 colspan=1>Radar Cross Section</td><td rowspan=1 colspan=1>0.1</td></tr><tr><td rowspan=1 colspan=1>Dwell Time</td><td rowspan=1 colspan=1>20 pulses</td></tr><tr><td rowspan=1 colspan=1>Interference Bandwidth</td><td rowspan=1 colspan=1>20MHz</td></tr><tr><td rowspan=1 colspan=1>Interference-to-Noise Ratio (INR) at the radar</td><td rowspan=1 colspan=1>14dB</td></tr><tr><td rowspan=1 colspan=1>Position States, ρVelocity States, νDiscount Factor, γ</td><td rowspan=1 colspan=1>50100.9</td></tr></table>

Ideally, we wish to optimize tracking performance (position and velocity estimation), which involves an inherent tradeoff between bandwidth and SINR. To accomplish this, we use a simplified model to capture these two fundamental aspects. At the heart of this problem is the radar’s range resolution, defined as

$$
\Delta R = { \frac { c } { 2 \beta } }\tag{16}
$$

where $c$ is the speed of light and $\beta$ is the radar’s bandwidth. Range resolution dictates the accuracy of the range measurement and is inversely proportional to bandwidth. Ideally the radar would use the entire bandwidth to achieve a fine range resolution. However, the radiation from other RF users in the same frequency band generates RF interference (RFI) to the radar (while the radar generates RFI to the other RF users) causing degradation in the SINR of both systems. The radar model considered in this development must therefore balance two conflicting requirements, namely, SINR and bandwidth. The research discussed in [40] proposes a technique that requires the radar to reduce its bandwidth in order to operate in a sub-band with high SINR when no target is present. The results indicate that a target entering the scene (or range swath) is detected at an earlier time due to the increase in SINR. After detection, the radar can tradeoff SINR for more bandwidth as desired. The goal of the proposed research is to investigate this tradeoff with the MDP using reinforcement learning to enable the radar to achieve optimal performance while controlling interference. The assumed parameters of the radar and communication systems are given in Table I.

## C. Simulation Details

The simulation-based experiments involve two major steps listed as follows:

1) training; and

2) testing.

Training involves running the radar against scenarios that it may encounter. Many training runs (on the order of $1 0 ^ { 3 }$ to $1 0 ^ { 5 }$ depending on interference type) are needed. Each run is set up by selecting, at random, one position state and one velocity state. Normally distributed random “noise” is added to both the position and velocity to ensure each trajectory is unique. Further, the granularity of the simulated position/velocity is much finer than what is included in the radar states. During each training run, the current state s is determined, then a valid action a is selected at random. The amount of bandwidth is determined based on the action, and the resulting interference based on the action and interference behavior is updated. The position and range are updated, and the resulting SINR is calculated. The new/future state $s ^ { \prime }$ (based on the target velocity and interference behavior) is determined,<sup>5</sup> and the probability transition function $\boldsymbol { \mathcal { T } } ( s , a , s ^ { \prime } )$ and reward function $\textstyle { \mathcal { R } } ( s , a , s ^ { \prime } )$ are updated. When all of the training runs are complete, policy iteration uses the discount factor, the estimated probability transition function, and estimated reward function to compute the optimal policy. Then, we test the policy to see how well the radar has learned from its training. Testing starts with a user-defined trajectory, which will be different than any of the trajectories on which the radar trained. This demonstrates that the radar is able to generalize and is not overtrained on any set of trajectories. Given the user-defined trajectory, the initial state s is determined, which is used to select an action from the policy; in other words, $a = \pi ^ { * } ( s )$ . The bandwidth is computed from the action (which is given by the policy), and the interference, position, range, and SINR are updated, as well as the resulting reward. The simulation is described in algorithmic form in Appendix A. The results here are based on testing the radar on the user-defined trajectory (i.e., after training). Note that the radar is trained on random trajectories, but the majority of the results shown in this article are based on the trajectory given in Fig. 1. Note that other trajectories result in qualitatively similar behavior. Further, as discussed in the next section, we also demonstrate the performance on a more complex trajectory, which is shown to be qualitatively the same as the performance with simple trajectories, despite the fact that the radar is only trained on simple trajectories.

## III. SIMULATION RESULTS AND ANALYSIS

The following results show the performance of the radar for each interference type examined in a system with $N =$ 5 frequency bands. The bands are assumed to be 20-MHz wide and contiguous, allowing for a maximum bandwidth of 100 MHz. Sections III-A and III-B first establish baseline results using constant and intermittent interference (cases that are very simple but important), while Sections III-C through III-E investigate more challenging interference scenarios. For each figure, the upper plot shows the cumulative rewards, the amount of bandwidth used by the radar, the target’s range, and the target’s SINR over time. The rewards and bandwidth are plotted versus the left y-axis, and the range and SINR are plotted versus the right y-axis. The lower plot shows the interference and the actions taken by the radar. The numbers on the y-axis of the lower plot are the decimal conversions of $\pmb \theta _ { i }$ and ${ \pmb { a } } _ { i } ,$ where $\pmb \theta _ { i }$ and $\pmb { a } _ { i }$ can be treated as vectors of binary values. For example, if the interference’s action value is 16, then the interference occupancy vector is $\pmb { \theta } _ { i } = [ 1 0 0 0 0 ]$ , and if the radar’s action number is 31, the radar occupancy vector is $\pmb { a } _ { i } = [ 1 1 1 1 1 1 ]$

TABLE II  
Summary of Reward Structure
<table><tr><td colspan="3">Summary of Reward Structure For  $N = 5$  Bands</td></tr><tr><td>SINR (dB) Reward</td><td>Number of Bands Used</td><td>Reward</td></tr><tr><td>&lt; 0</td><td>-35</td><td>+0</td></tr><tr><td>0-2 +1</td><td>1 2</td><td>+10</td></tr><tr><td>2-5 +2</td><td>3</td><td>+20</td></tr><tr><td>5-8  $^ { + 3 }$ </td><td>4</td><td>+30</td></tr><tr><td>8-11 +4</td><td>5</td><td>+40</td></tr><tr><td>11-14 +5</td><td></td><td></td></tr><tr><td> $1 4 - 1 7$  +6</td><td></td><td></td></tr><tr><td> $1 7 - 2 0$  +8</td><td></td><td></td></tr><tr><td>&gt; 20 +10</td><td></td><td></td></tr></table>

The reward structure greatly influences the behavior of the radar. In our experiments, the reward structure is set up such that if the SINR is negative and not all bands are used by the radar, the agent will receive a large net-negative penalty. A negative penalty reflects the high probability of losing the target at negative SINR (note that the threshold of 0 dB SINR is somewhat arbitrary and could have been chosen to be any value that might result in loss of the target). When the SINR is negative, but all of the bands are used by the radar, the agent receives a small net-positive reward, where the reward for using all bands is greater than the penalty for negative SINR. This reward structure provides some incentive for the radar to take some chances and use all of the bands, even if there is risk of having negative SINR. If the reward structure is changed to make the penalty for negative SINR greater than the reward for using all bands, the radar will be more conservative in its decision making and not take the risk of having a negative SINR. This could also be used to make the radar less likely to cause interference to communication systems. Overall, the radar’s performance is dictated by SINR and bandwidth; multiplicative increases in bandwidth are more important than incremental increases in SINR. The reward for SINR also saturates at 20 dB to reflect the fact that there is no practical benefit gained from having an SINR higher than some threshold. The reward structure used in this work for all test cases is summarized in Table II. The total reward at one time instant is determined from the sum of values from both columns. For example, if $\mathrm { S I N R } = 3 ~ \mathrm { d B }$ , and the radar uses four bands, then the total reward at that time would be $2 + 3 0 = 3 2$ . It should be noted that the reward structure can be altered to change the general behavior of the radar. For example, the reward structure could be altered to penalize any action which results in a loss of SINR (i.e., complete interference avoidance). In this work, we chose a structure that trades SINR and bandwidth

![](images/cc578295b86042ca328108db60c42dcc1e13f9acc07f759d1a18bc4b3fe4bcab.jpg)  
Fig. 2. Results for constant interferer. TOP: SINR and rewards for cross-range trajectory. BOTTOM: Spectral occupancy of the radar (blue) and interference (Red). Note that the radar behavior depends on both the range and spectral occupancy of the target.

For further reading and guidance to the choice of the reward structure for adaptive radar, please see [41].

## A. Constant Interference

In the case of constant interference, the communication system occupies a non-zero number of bands and does not change for the duration of a training run. The motivation for this case is to test the performance of the MDP model against only the target trajectory. An example result for $\pmb { \theta } = [ 1 0 0 0 0 ]$ is shown in Fig. 2 for a target moving left to right, as shown in Fig. 1. This example demonstrates that when the target is farther away, the radar avoids the interference by selecting all the bands where the interference does not exist. As the target crosses the radar environment, its range decreases and, as a result, the SINR increases. When the SINR is sufficiently high (approximately 15 dB in this case), the radar can accept trading off SINR to use more bandwidth. At that point, the radar is able to use all of the bands, even if one is occupied by the interferer, and the SINR is still positive. This learned behavior depends to a large degree on the reward structure. After the target makes its closest approach to the radar, its range begins to increase. When the target is sufficiently far away, the radar needs the SINR to stay positive and thus trades some of the bandwidth to improve SINR, using the same bands as in the beginning of the trajectory.

In this example, since the interferer occupies only a single band on the edge, the radar learns to occupy the remaining contiguous bands when the target is farther away since using all bands would drive the SINR negative. As the target comes closer to the radar, the received signal is strong enough to provide good SINR even in the presence of interference. Thus, the radar learns to use the entire band, reaping the benefit of a larger bandwidth. Note that because the radar learns the evolution of states, it anticipates negative SINR and changes before negative SINR occurs.

The specific rewards for this example are given in Table III for two specific range values to demonstrate the optimality of the learned behavior. The rewards are computed for each possible action, when the target is farther away and when the target is closer to the radar. When the target is farther away (5.5 km), the action $\pmb { a } = [ 0 1 1 1 1 ]$ returns the highest reward (35) because it uses the highest number of bands, while also keeping the SINR positive. Since this is the highest reward the radar can $\operatorname* { g e t } , \pmb { a } = [ 0 1 1 1 1 ]$ is the optimal action under those circumstances (target is 5.5 km away). From Fig. 2, we can see that this is indeed the action learned by the radar. When the target is closer to the radar (e.g., 3.8 km), the SINR is sufficiently high to allow for using all of the bands (i.e., it learns that it can tolerate interference at this range and reap the benefits of higher bandwidth). When the radar takes the action a = [1 1 1 1 1], it maximizes its reward by using all of the bands, as seen in Table III. The additional reward due to bandwidth offsets the decrease in reward due to the lower SINR (compare action [0 1 1 1 1] to [1 1 1 1 1], where reward equals 38 and 42, respectively). Since 42 is the highest reward the radar can receive when the target is closer, a = [1 1 1 1 1] is the optimal action when the target is closer to the radar. Again, we observe this behavior in Fig. 2 (bottom).

TABLE III  
Rewards for Each Action, When the Target is Further Away and Closer to the Radar
<table><tr><td>Observed Interference</td><td>Range (km)</td><td>Action</td><td>BW (MHz)</td><td>SINR (dB)</td><td>Reward</td></tr><tr><td>[10000]</td><td>5.5</td><td>[0 0 001]</td><td>20</td><td>11.8</td><td>5</td></tr><tr><td>[10 0 0 0]</td><td>5.5</td><td>[0 0 010]</td><td>20</td><td>11.8</td><td>5</td></tr><tr><td>[10000]</td><td>5.5</td><td>[0 0100]</td><td>20</td><td>11.8</td><td>5</td></tr><tr><td>[1 0 0 0 0]</td><td>5.5</td><td>[010 0 0]</td><td>20</td><td>11.8</td><td>5</td></tr><tr><td>[10000]</td><td>5.5</td><td>[10 000]</td><td>20</td><td>-9.1</td><td>-35</td></tr><tr><td>[10 0 0 0]</td><td>5.5</td><td>[0 0011]</td><td>40</td><td>11.8</td><td>15</td></tr><tr><td>[10 0 0 0]</td><td>5.5</td><td>[0 0110]</td><td>40</td><td>11.8</td><td>15</td></tr><tr><td>[1 0 0 0 0]</td><td>5.5</td><td>[01100]</td><td>40</td><td>11.8</td><td>15</td></tr><tr><td>[10000]</td><td>5.5</td><td>[11000]</td><td>40</td><td>-6.1</td><td>-25</td></tr><tr><td>[10000]</td><td>5.5</td><td>[00111]</td><td>60</td><td>11.8</td><td>25</td></tr><tr><td>[10 0 0 0]</td><td>5.5</td><td>[01110]</td><td>60</td><td>11.8</td><td>25</td></tr><tr><td>[10 00 0]</td><td>5.5</td><td>[11100]</td><td>60 80</td><td>-4.4</td><td>-15</td></tr><tr><td>[1 0 0 0 0]</td><td>5.5 5.5</td><td>[01111] [11110]</td><td>80</td><td>11.8</td><td>35</td></tr><tr><td>[10 000] [10 0 0 0]</td><td>5.5</td><td>[11111]</td><td>100</td><td>-3.2 -2.3</td><td>-5</td></tr><tr><td>[10000]</td><td></td><td></td><td></td><td></td><td>5</td></tr><tr><td>[10000]</td><td>3.8 3.8</td><td>[0 0001] [00010]</td><td>20 20</td><td>18.2 18.2</td><td>8</td></tr><tr><td>[1 0 0 0 0]</td><td>3.8</td><td>[0 010 0]</td><td>20</td><td>18.2</td><td>8 8</td></tr><tr><td>[10000]</td><td>3.8</td><td>[01000]</td><td>20</td><td>18.2</td><td></td></tr><tr><td>[10000]</td><td>3.8</td><td>[10000]</td><td>20</td><td>-2.7</td><td>8</td></tr><tr><td>[1 0 0 0 0]</td><td>3.8</td><td>[0 0011]</td><td>40</td><td>18.2</td><td>-35</td></tr><tr><td>[1 0 0 0 0]</td><td>3.8</td><td>[00110]</td><td>40</td><td>18.2</td><td>18</td></tr><tr><td>[10000]</td><td>3.8</td><td>[01100]</td><td>40</td><td>18.2</td><td>18</td></tr><tr><td>[10 0 0 0]</td><td>3.8</td><td>[11000]</td><td>40</td><td>0.3</td><td>18</td></tr><tr><td>[10 0 0 0]</td><td>3.8</td><td>[00111]</td><td>60</td><td>18.2</td><td>-25</td></tr><tr><td>[1 0 0 0 0]</td><td>3.8</td><td>[01110]</td><td>60</td><td>18.2</td><td>28</td></tr><tr><td>[1 0 0 0 0]</td><td>3.8</td><td>[11100]</td><td>60</td><td>2.0</td><td>28</td></tr><tr><td>[10000]</td><td>3.8</td><td>[01111]</td><td>80</td><td>18.2</td><td>22 38</td></tr><tr><td>[10 0 0 0]</td><td>3.8</td><td>[11110]</td><td>80</td><td>3.2</td><td>32</td></tr><tr><td>[10000]</td><td>3.8</td><td>[11111]</td><td>100</td><td>4.2</td><td>42</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

It is natural to ask at this point whether or not more complex trajectories would confuse the radar. To test this, we presented a radar trained with various constant trajectories with a more complex trajectory for testing. An example is given in Fig. 3. The trajectory tested is given in the top sub-figure, while a plot of the SINR and rewards over time is given in the middle sub-figure. Given the fact that 1) both position and velocity of the target are included in the state variable and 2) learning with MDP models depend only on the previous state (not the entire history), one would expect that the complexity of the trajectory should not affect the performance. As the results in Fig. 3 show, that does appear to be the case. Despite the more complex trajectory, the radar behaves in a manner consistent with what is expected. More specifically, just as in the case of a simple trajectory, the radar avoids the interferer only while the target is farther away. However, as the target approaches the radar, eventually the SINR gets to a sufficiently high value, and the radar occupies the entire band, since the SINR (while low) is still above the threshold that would cause a loss in detection (chosen to be 0 dB). As the target moves away from the radar eventually the SINR drops to a level such that the radar changes its waveform in order to avoid the interference and maintain an SINR above the threshold. Note that the threshold chosen is arbitrary. If 0 dB is deemed to be too low, a higher threshold could be chosen by making the reward strongly negative (i.e., a penalty) for any SINR below that chosen threshold. Additionally, we could cause the radar to always avoid interference by appropriate choices for the reward structure.

![](images/6387dcfaa6897e819eaa1858cd742f9c8a4fd0fc29a68b1070f0e277b462989a.jpg)  
Fig. 3. Results for constant interferer with a more complex trajectory. TOP: Trajectory of the target. MIDDLE: SINR and Rewards over time. BOTTOM: Spectral Occupancy of the Radar (blue) and Interference (Red). Note that the radar behavior depends on both the range of the target and the spectral occupancy of the interference.

## B. Intermittent Interference

The intermittent interferer model is similar to the constant interferer, except the interferer is no longer always transmitting. In these experiments, the radar was tested for 10% and 90% interference transmission probability. Note that the interference uses consistent frequency bands when transmitting during each training run (but not necessarily the same band each run). The probability of interference transmission is independent from one time instant to the next. This scenario is useful for modeling the performance of communication systems that occupy a specific frequency band, but whose transmissions can vary. The 90% case is shown in Fig. 12. The radar behaves similar to the constant interference case, where it avoids the interferer until the target is close, and then the radar selects all bands. The radar learns that the interference is likely, and thus waits until the SINR is sufficiently high before maximizing its bandwidth. Results for the 10% case are shown in Fig. 13. In this case, the radar has learned that interference is unlikely, and thus selects all bands for the entire simulation length. In both cases, the radar learns that although it cannot predict when interference will occur, it can learn the probability of interference. Thus, it does not react to interference and instead learns whether the interference is common or not.

In the 10% case, the rare penalty for negative SINR due to infrequent interference is tolerated in exchange for the benefit of using more bandwidth. When the interferer transmits more frequently, the penalty is more common and thus severe, thus the radar avoids the band that contains the interferer until the SINR is guaranteed to stay positive. In the 10% case, we can make the radar more sensitive to the interference by increasing the penalty for negative SINR.

## C. Frequency Swept Interference

The triangular frequency sweep interferer occupies one band at a time and moves up and down the available bands, creating a triangular wave pattern when viewed on a waterfall plot, as shown in Fig. 4. This case (along with others to be considered) models the radar’s performance in the presence of a deterministic frequency-hopping communication system.

![](images/a8ad2fc2300e0f05a5911d0628cf51c39e17367d260af36801da6af9deb982a6.jpg)

Fig. 4. Waterfall plot of triangular frequency sweep interferer (left) and state representation (right).  
![](images/8902cebbbe8d0e1437af579dba70b052d89c4d4d994223a8f0de868c4ae64d6f.jpg)  
Fig. 5. Behavior of radar in the presence of triangle-sweep frequency interference with single memory state.

The results shown in Fig. 14 demonstrate that the SINR fluctuates greatly as the interferer moves around in frequency. When the interferer occupies any of the middle three bands, the radar is not able to predict where the interferer will go next since the radar does not know whether the frequency is increasing or decreasing based on only the current band. Only when the interferer is at the edge of the available bands does the radar know where the interferer will go next. As a result, the radar’s policy is to maximize bandwidth, even if there is a risk of collision with an interferer, because avoiding interference would mean reducing the bandwidth too much (only a single-band waveform could avoid interference entirely), thus resulting in lower rewards. This behavior depends on the following:

1) the specific range of the target (i.e., its SINR); and 2) the penalties/rewards structure for negative SINR/bandwidth, respectively.

The behavior of the radar given the observed interference is outlined in Fig. 5. When the interferer is at the band edges (θ = [00001] or [10000]), the radar knows with certainty the future interference state will be [00010] or [01000], respectively, and uses the three bands where the interferer will not go [11100] or [00111], respectively. When the interferer occupies any of the middle three bands (e.g., θ = [00100]), the radar has learned there is an equal probability (50%) of the interferer’s future state being either [01000] or [00010]. Due to the setup of the reward structure, it is advantageous for the radar to use all of bands, even if the SINR will be negative, because the reward is greater than if the radar attempted to avoid the interferer, which is only possible using a single band.

![](images/1c5d455b1283ff68fc875f996fbf67a327c21f14a9ebb7649a23fa3b3ba353f5.jpg)  
Fig. 6. Behavior of radar in the presence of triangle-sweep frequency interference with additional memory states.

We can improve the performance in this case by increasing the number of states to include two consecutive interference states. Specifically, we modify the model to include the current interference state at time t and the previous interference state at $t - 1$ . The number of states becomes $N _ { S } = \rho \nu 2 ^ { N } \cdot 2 ^ { N } = \rho \nu 2 ^ { 2 ^ { \cdot } N }$ , an increase by a factor of $2 ^ { N }$ . When memory is employed in this way (see Figs. 6 and 15), the radar is able to predict where the interferer will go, and therefore there are no drops in the SINR. The cost for using memory is training time and complexity. Specifically, training becomes somewhat longer because more training runs are needed to cover the increase in the number of states. When memory is used, the radar knows what the future interference state will be, given the current and previous states. Fig. 6 demonstrates the radar has learned the interference behavior, because each action optimizes the bandwidth it can use while also keeping the SINR positive. This coincides with the result in Fig. 15, as the SINR never drops below 0 dB.

If the frequency sweep moved in a single direction wrapping around when the band edge is reached (i.e., what is often termed a sawtooth frequency sweep interferer), additional memory states would not be needed. The results in Fig. 16 demonstrate the radar is able to predict where the interferer is going to go, thus avoiding any drops in SINR below 0 dB. Unlike the triangle frequency sweep case, the transition probability from one interference state to the next is <sup>P</sup> $( \pmb { \theta } _ { t + 1 } \mid \pmb { \theta } _ { t } ) = 1 . 0$ , thus the radar knows which bands the interferer will use and adjusts accordingly. When the target is close enough and SINR is sufficiently high, the radar then selects all bands, as the radar can accept the lower (but still positive) SINR to get more reward from the bandwidth.

## D. Frequency-Hopping Interference

One could reasonably ask if the performance in the previous section was primarily due to the fact that the interference moved in an easily predictable fashion (i.e., between adjacent bands). If the pattern of frequency occupation were pseudorandom, would the behavior be any different? To test this, we examined three pseudorandom hopping patterns: 1) a length-5 pattern, 2) a length-10 pattern, and 3) a pattern that has a very long length but still occupies each band with equal probability. In this case, the interference still occupies one band at a time, but unlike the triangle and sawtooth frequency sweep, does not always move to neighboring bands. The first hopping pattern used was {3, 1, 2, 4, 5, . . .}. When the last band in the sequence is reached, the interferer goes back to the first band and the sequence repeats. This case is useful for modeling the performance of the radar in the presence of short pseudorandom frequency-hopping communication systems. As the results in Fig. 17 show, the radar has learned the optimal behavior, as it is able to predict and avoid the interferer’s movements, and uses all of the bands only when the target is close to the radar.

![](images/d49e79c18f30b1d216710830f3dc1dec17ab13aa1009959947f557ea06613ef8.jpg)  
Fig. 7. Behavior of radar with length five frequency hopping.

Fig. 7 illustrates the action taken for each observed interference state. Since the transition probability from one state to the next is 1 (unlike triangle sweep, without memory but similar to the sawtooth pattern), the radar learns with certainty what the next interference state is going to be. As a result, the action selected for the future state, given the current state, uses as many contiguous bands as possible (three or four, in this case) while avoiding the interferer and preventing the SINR from becoming negative.

The length-10 frequency hopper is similar to the length-5 hopper, but with a longer hopping pattern: {3, 1, 2, 4, 5, 2, 3, 4, 1, 5, . . .}. Unlike the length-5 frequency hopper, the transition probability (as seen from the radar’s perspective) from one interference state to the next is going to be $\mathbb { P } ( \pmb { \theta } _ { t + 1 } \mid \pmb { \theta } _ { t } ) = 0 . 5$ . As the results in Fig. 18 demonstrate, the radar is unable to predict the future interference state, similar to the triangle frequency sweep interferer. For example, if the current interference state is $\pmb { \theta } _ { t } = [ 1 0 0 0 0 ]$ , the future interference state could be either $\pmb { \theta } _ { t + 1 } = [ 0 1 0 0 0 ]$ or $\pmb { \theta } _ { t + 1 } = [ 0 0 0 0 1 ]$ , both with equal transition probabilities of 0.5. The action selected in this instance is $\begin{array} { r } { \pmb { a } _ { t } = [ 1 1 1 1 1 0 ] , } \end{array}$ , which is optimal given the scenario because the radar attempts to maximize the reward it can get from bandwidth, despite the 50% probability of using the same bands as the interferer and having a negative SINR. The radar occasionally is able to successfully avoid the interferer, but this only occurs when the occupied bands of the future states are next to each other. For example, when $\pmb { \theta } _ { t } = [ 0 0 0 0 1 ]$ and could transition to either $\pmb { \theta } _ { t + 1 } = [ 0 1 0 0 0 ]$ or $\pmb { \theta } _ { t + 1 } = [ 0 0 1 0 0 ]$ , the radar selects $\pmb { a } _ { t } = [ 0 0 0 1 1 ]$ , because it knows either bands 2 or 3 will be occupied, and bands 4 or 5 provide an opportunity to maximize bandwidth and a guarantee of not colliding with the interferer.

TABLE IV  
Interference States and Actions for Length-10 Frequency Hopping Interferer
<table><tr><td>Observed Interference State</td><td>Next Interference State</td><td>Action (No Memory)</td><td>Action (w/Memory)</td></tr><tr><td>00100</td><td>10000</td><td>01100</td><td>01111</td></tr><tr><td>10000</td><td>01000</td><td>11110</td><td>00111</td></tr><tr><td>01000</td><td>00010</td><td>11111</td><td>11100</td></tr><tr><td>00010</td><td>00001</td><td>01110</td><td>11110</td></tr><tr><td>00001</td><td>01000</td><td>00011</td><td>00111</td></tr><tr><td>01000</td><td>00100</td><td>11111</td><td>11000</td></tr><tr><td>00100</td><td>00010</td><td>01100</td><td>11100</td></tr><tr><td>00010</td><td>10000</td><td>01110</td><td>01111</td></tr><tr><td>10000</td><td>00001</td><td>11110</td><td>11110</td></tr><tr><td>00001</td><td>00100</td><td>00011</td><td>00011</td></tr></table>

Because the radar is unable to predict a single interferer state, its performance is suboptimal and suffers drops in SINR. Like the triangle frequency sweep case, we can also utilize memory, such that each state contains information of the interference state on the current and previous time steps. When memory is employed, the transition probabilities resolve to $\mathbb { P } ( \pmb \theta _ { t + 1 } \mid \pmb \theta _ { t } , \pmb \theta _ { t - 1 } ) = 1$ , which means the radar knows with certainty which interference state is next. The results in Fig. 19 demonstrate the optimal performance of the radar when additional memory is used.

Table IV shows the actions taken by the radar given the current interference state with and without memory. Similar to the triangle frequency sweep case, each observed state has two possible future states, each with transition probabilities of 50%. Without memory, the radar does not know which of the two future states will occur. Thus, the general behavior of the radar without memory is to use as many bands as possible to maximize the reward from bandwidth, even if there is a 50% risk of negative SINR. As a result, there are times at which the SINR goes negative because the radar uses one of the bands occupied by the communication system.

Table IV also shows the actions the radar selects when memory is employed. Given the current interference state and the previous state, the radar knows with certainty what the future state will be. Therefore, each action selects as many bands as possible, while also avoiding the interferer in the future state. The actions in the table coincide with the results in Fig. 19.

If the hopping sequence is not short, but is instead a very long pseudorandom hop sequence, the transition probabilities from the current interference state to the next become equal and is the inverse of the number of bands: $\mathbb { P } ( \pmb { \theta } _ { t + 1 }$ $\pmb { \theta } _ { t } ) = 1 / N = 1 / 5$ . As the results in Fig. 20 demonstrate, the radar is unable to predict which bands the interferer will use, and therefore uses all of the bands all of the time, attempting to maximize reward from bandwidth, even if the SINR is low or negative. Like the other results, the radar does use all bands when the target is closer.

![](images/7b46158adae9f03db70298d9b191d11506a91b983fba6eb8ae84f0c350e3418c.jpg)  
Fig. 8. Trajectory of target with direction-dependent interferer.

## E. Direction-Dependent Interferer

The direction-dependent interference scenario, unlike the previous cases, removes the assumption that the interferer’s power as sensed by the radar is direction independent. As Fig. 8 illustrates, in this case, the interference is localized. The interference affects the radar only when the target is in the position cells inside the red-dashed rectangle. When the radar’s beam is tracking the target and the target is in these position states, the radar will also sense interference. When the radar is focused on the unaffected cells, it will not sense interference. We tested the radar against three cases in which the interferer is

1) constant;

2) intermittent with high transmission probability (90%); and

3) intermittent with low transmission probability (10%).

Fig. 21 shows the results for the constant interferer. When the target is in the unaffected cells, the radar learns to use all bands. Immediately before the target enters the regime with the affected position cells, the radar switches and avoids the band where the interferer resides. As the target leaves the cells affected with interference, the radar selects to use all the bands again, because it anticipates the target leaving the affected area. Because the position cells with interference are constant on each training run, the radar learns which cells (and what bands) will have interference, and is thus able to predict which cells will have interference and avoid those bands accordingly. Note the decreasing SINR shown in the plot is only due to the target moving away from the radar and not the interferer. This behavior is optimal because the radar takes advantage of the bands being unoccupied by using all of them, and then avoiding the interferer by using one less band to maintain a positive SINR.

With an intermittent interferer with a high probability of transmission (Fig. 22), the radar performs similar to the constant case, choosing the avoid the interferer when the target is in the affected position cells and using all bands otherwise. Again, the radar avoids the band used by the interferer and avoids momentary drops in SINR.

![](images/7f594a031f9b7172bfd7d3d59f1dc8ddc3148f76b17f06207c10eb2ecda1e571.jpg)

Fig. 9. Results for comparing MDP and DSA for high intermittent case.  
![](images/b9304a3d04b7e2483c93cc6e933411ee9bf3cb54bdaf8e7354f03ec2794c9798.jpg)  
Fig. 10. Results for comparing MDP and DSA for triangle frequency sweep case.

With a low probability of transmission intermittent interferer (Fig. 23), the probability of transmission is low enough that the risk of having negative SINR is also low. It is therefore optimal for the radar to use all of the bands for the entire track, because it will receive more average reward than if it attempted to avoid the (relatively) unlikely chance the interferer may transmit and cause the SINR to drop. Note that, due to the intermittent nature of the interference, the radar cannot predict when interference will occur.

## IV. COMPARISON WITH OTHER TECHNIQUES

As a final investigation, we compare the MDP model against another technique, dynamic spectrum access (DSA). A DSA system senses the spectrum and selects the bands available at that time. While DSA is simpler, it does not have the predictive ability of a radar modeled with an MDP and trained with reinforcement learning. Fig. 9 compares the MDP and DSA models for the high intermittent (90%) case. The performance of the MDP model is indicated by the dotted lines and the DSA model is indicated by the dashed lines. The two approaches are compared by the reward accumulated at the end of the simulation. A DSA system is reactive to the interference, using bands only when they’re unoccupied, but results in drops in SINR when the interferer transmits again. And, since the DSA system is not learning from its environment, it does not learn the probability of transmission, nor does it learn to use more bandwidth when the target is closer. With the same reward structure used in all prior results, the MDP model accumulates slightly more reward than the DSA approach (6041 versus 5507). In this case, since the current and future states are identical most of the time, the advantage of the MDP approach over standard DSA is limited.

Fig. 10 shows the MDP and DSA approaches for the triangle sweep case. Comparing the accumulated reward, we see the MDP approach significantly outperforms the DSA system (5447 versus 1729). The difference in reward is due to the reinforcement learning, which enables the radar to predict which bands the interferer will use in advance and learn at which target range the radar can trade SINR for more bandwidth, thereby attaining better range resolution while maintaining positive SINR (both which maximize reward). Results for other cases (constant, low intermittent, sawtooth, etc.) also indicate the MDP model has a higher accumulated reward compared to the DSA technique, thereby demonstrating its superior performance.

![](images/5b70bd7d77462424131b5945f26308f6cfeb4090c4b5d5d05f2df68b2bed82c0.jpg)  
(a)

![](images/6c13066d7c0120cccc058a3bb0b4681e20815c95a336efd9457ccf055eb0de97.jpg)  
(b)  
Fig. 11. Rewards (a) and collisions (b) of the cognitive radar using the MDP model compared with dynamic spectrum access (DSA).

## A. Reactive Communication System

In the previous examples, the state of the interference was not dependent on the actions of the radar. Thus, the optimal action does not necessarily require long-term planning, i.e., finding the optimal policy does not necessarily require policy iteration. In this subsection, we examine a case where the state does depend on the actions of the radar. Specifically, we examine the case where the communication system reacts to the radar’s transmission. In this case, whenever the radar occupies all frequencies, not giving the communication system an opportunity to transmit, the communication responds by occupying all bands. If the radar leaves open one band, the communication system responds by either 1) occupying the one open band with probability 0.8 or 2) occupying all bands with probability 0.2. If the radar leaves open two bands, the communication system avoids the radar and occupies the remaining bands with high probability. Further, if the communication system occupies all bands, it stays in that state or transmits in the first band. Using the resulting optimal policy the reward is plotted in Fig. 11 (a), while the collisions are plotted in Fig. 11 (b). The reward and collisions when using a DSA approach is also plotted. It can be seen that the optimal policy based on an MDP model and policy iteration provides a substantial improvement over DSA. The MDP-based approach learns to avoid transmitting in all bands as that drives the communication system to also occupy all bands and stay in that state. Instead, the radar learns to force the communication system into states that are both advantageous for the radar and don’t lead it to transmit in all bands.

## V. CONCLUSION

This article has demonstrated the applicability of MDPs and reinforcement learning to the radar-coexistence problem. The results demonstrate a radar is able to learn the interference behavior of a communication system and adjust its band usage to maintain the target track with a positive SINR. Building off of prior work in online optimization to adjust center frequency and bandwidth, the approach presented here involves offline training data and then testing on an unseen target trajectory. By using reinforcement learning, the radar is no longer restricted to using a fixed band/group of bands; the cognitive radar learns the interference behavior and is able to predict its behavior in advance. Additionally, reinforcement learning allows the radar to achieve this behavior without having to be explicitly programmed to do so for each state, a feat that would have been very expensive in terms of hours spent in design and verification. The use of reinforcement learning frees traditional radars from the restrictions mentioned in Section I, allowing it to continue target tracking functions, while coexisting in the increasingly dense RF spectrum.

MDPs applied to target tracking in cognitive radars using reinforcement learning enables the radar to maintain the target track despite the presence of interference. While target tracking performance was not specifically examined, it was nonetheless studied using a simplified model. The simplified model focused on the tradeoff between SINR and bandwidth, two key aspects of target tracking performance. Specifically, MDPs were used to predict and avoid interference. The results indicate the following:

1) The radar is able to learn where the interferer will be in frequency (for the interference models examined) in the next time slot and use the contiguous bands where the interferer does not exist to maximal benefit.

2) When the target is sufficiently close to the radar, the radar can trade SINR for increased bandwidth and still maintain positive SINR, despite using the same band(s) as the interferer.

3) The radar reduces bandwidth usage to increase SINR as the target moves away.

4) The radar is able to learn how often an intermittent interferer will transmit and use the bands accordingly; the radar uses all bands for the low probability case, and for the high probability case, the radar behaves similar to the constant interference case by choosing to avoid the interferer until the target is close and its SINR is sufficiently high.

5) The radar is able to predict the band usage of a frequency-hopping communication system with short hopping patterns and adjust its own bandwidth accordingly.

6) The radar can learn where an interferer is localized and avoid the interferer’s frequency bands prior to the radar’s beam entering the area with interference.

While this article demonstrates the applicability of MDPs and reinforcement learning to solving this type of problem, there are some challenges with this approach, the first of which is state space size. If the state space is increased,<sup>6</sup> the training process will become more complex and take more time. To resolve this, techniques could be used to reduce the state space to a more manageable level. Alternatively, we have begun to explore deep reinforcement learning techniques, which allow us to handle larger state spaces with modest complexity.

A second challenge that must be addressed moving forward is the flexibility of trained radars. Specifically, if the radar is trained for a particular type of interference and it experiences a different type of interference in the field, how will it perform? Initial results show that if the interference is dramatically different, performance can be poor if online learning is not included. Alternatively, radars could be trained on a large variety of interference types, but if there are not states that allow the differentiation of these interference types, the radar will simply learn the best average actions, which can compromise performance. Thus, we are currently investigating this issue.

The other issue in this problem was modeled using fully observable Markov decision processes. Under full observability, what the radar observes/measures also matches the true values. When this ideal assumption is removed, we have a partially observable MDPs (POMDPs), in which the radar’s measurements of the environment do not necessarily coincide with the true values (which could be due to noise or inaccurate sensing) [31]. When the radar observes information about the environment, it doesn’t know with certainty which state it is in, but rather has a set of possible states it could be in, each with an associated probability. While POMDPs may provide a more realistic model, they come at a cost of computational complexity. Therefore, techniques that can facilitate the learning process on a more complex model would be very helpful. For example, POMDPs could be transformed into a set of solvable MDPs, with one MDP per belief state. Additionally, to demonstrate the applicability of reinforcement learning, the model in this work abstracted out the actual radar signal processing. When the abstractions are removed, the model then has to account for imperfections in the measurement of range and velocity (e.g., due to noise or the range-Doppler coupling effect due to using an LFM waveform).

Future work will involve revisiting the assumptions discussed in Section II and studying the effect of each. Specifically, that could entail

1) an interferer that moves with respect to the radar, and the dependence of location on the received interference;

2) a reward structure that is based more directly on tracking estimation error variance;

3) modeling an actual communication protocol, such as LTE or WiFi for the communication system;

4) real-world experiments with cognitive radar and cognitive radio testbeds;

5) explicitly modeling the radar environment, atmospheric effects, multipath, clutter, and terrain as well as the impact of position and velocity measurement errors;

6) examination of the effect of an intelligent interferer; and

7) other reinforcement learning techniques, particularly those that can reduce the state space size and training time.

Additional future work should focus on how to speed up the learning process by using the knowledge that some transitions cannot occur. Due to target motion characteristics, the target can only transition to up to eight neighboring position states, which (in this model) rules out approximately 50 remaining position states, thereby reducing the state space. Future work could also incorporate received power of interference in the model. Rather than considering interference presence as a binary value on [0, 1], the interval could be quantized into subintervals, each indicating relative power of interference. For example, with four levels of interference, the interference could take any value from 0 to 0.25, 0.25 to 0.5, 0.5 to 0.75, and 0.75 to 1. The radar could take advantage of bands that have interference, but whose interference is minimal enough to not have a severe impact on SINR. This would come at a cost of a larger state space, which would increase from $\rho \nu 2 ^ { N }$ to $\rho \nu 2 ^ { Q N }$ , where Q is the number of quantized levels.

Additional work could consider the effect of more than one interferer in the environment. Instead of the interference occupancy vector looking like θ = [0 0 1 0 0], it could look like $\pmb { \theta } = [ 0 0 1 1 0 ]$ . Part of the challenge would be simulating the performance of the radar when there are different types of interferers in the environment (e.g., triangle sweep and intermittent) and designing a step-frequency radar that can utilize discontinuous bands, such as when θ = [1 1 0 1 0].

## APPENDIX A VALID ACTIONS

In this article, we assume that there is one primary frequency band made up of N sub-bands. Theoretically, there would be $2 ^ { N }$ valid actions provided that the radar could use or not use any combination of sub-bands. However, for this work, we assume that only contiguous bands can be used together. The number of valid actions when only contiguous bands can be used can be found readily, by realizing that there are N different actions which use one band, N − 1 different actions which use two bands, N − 3 different actions which use three bands, and in general, N − i + 1 different actions which use i bands. Thus, the total number of valid bands can be found as

$$
N _ { A } = \sum _ { i = 1 } ^ { N } i = { \frac { N ( N + 1 ) } { 2 } } .\tag{17}
$$

As an example, the valid actions for $N = 5$ are the following:

1) [11111];

2) [01111];

3) [11110];

4) [00111];

5) [01110];

6) [11100];

7) [00011];

8) [00110];

9) [01100];

10) [11000];

11) [00001];

12) [00010];

13) [00100];

14) [01000];

15) [10000].

## APPENDIX B

Algorithm 1: Algorithm for training radar and testing its   
performance.   
for Each training run do   
Randomly select a starting position and target   
velocity;   
Add "noise" to position and velocity;   
Calculate Initial SINR;   
for Each time index do   
Calculate initial state;   
Randomly select a valid action;   
and determine bandwidth;   
Determine bandwidth used, update interference,   
position, range, and SINR;   
Determine new state;   
Update P and R   
end   
end   
Using Policy Iteration, determine optimal policy;   
for Each testing run do   
Using a user-defined trajectory that was not   
previously trained on;   
Calculate Initial SINR;   
for Each time index do   
Calculate initial state;   
Select an action from the policy;   
Determine bandwidth used, update interference,   
position, range, and SINR;   
Determine new state;   
end   
Create plot of Rewards, Bandwidth, SINR, Range,   
Actions, and Interference States   
end

![](images/38a24de9c75aa887da6dc153787d64425e67781915626e896ca722173038fa5d.jpg)  
Fig. 12. Results for 90% intermittent interferer.

![](images/a934e936cf413a93754bda2f5008effcc2ae6815dc8bbf3bd038fdbe7265f3e5.jpg)

![](images/7ef69f802b9eb58590730cd7b87dd1b1f7d968fcfbcb9f1616d0f112aa688fa3.jpg)  
Fig. 16. Results for sawtooth frequency sweep interferer.

![](images/1d73d7aa956ed52f9c7e7420d8f91c0a38c7a57d208369304c6600fe6e58ff39.jpg)

![](images/7ef7d45a0d6bf745345b15184e5dec564a45a85d244105dc9665cf7443fc5fc1.jpg)  
Fig. 13. Results for 10% intermittent interferer.  
Fig. 14. Results for triangle sweep interferer, without memory.

![](images/7fc9a37c81c45e3f8d37f4d611bc6261f9a1370f95796933b5dd263fe5f36dbb.jpg)

![](images/f26476a0a32278b18f661d103ffbfd2217226b9ee46d91e9c926462fab7fb412.jpg)

![](images/f2da37b42d373a08b7fb0cf663f8cecbe2a4ed7955d7d3bf571344cc1f6d5bc1.jpg)

Fig. 17. Results for length-5 frequency-hopping interferer.  
![](images/3706181fa1c19a2bedc5ef311766fc215a008e065ab5d3f62a5df9c885b8a7f4.jpg)

Fig. 15. Results for triangle sweep interferer, with memory.  
![](images/1653b24955eb9f36507e02b89ab95e9b756ed1ba8284aba7904cc4d496971e83.jpg)

![](images/240046ba5ba59617ea76e0eec193350445b3a2111c06553f71f872248b693644.jpg)

Fig. 18. Results for length-10 frequency-hopper, without memory.  
![](images/7665b34148c40a7d3a120b1ec8b512cea97a608fc59216cf4e643358333c2ad5.jpg)

![](images/abe9f31edccb5c401bcf16e559dd770332073bda043d229da7e2c54005764a11.jpg)  
Fig. 19. Results for length-10 frequency-hopper, with memory.

![](images/b944a49c864ed67a9d07a7eb32d561afea1ac9563241ca8defccba0555f996bf.jpg)

![](images/0f6364f52a54e3d3a3fd7801becd6a6008591fc9e2be1c739ce425b0584ce576.jpg)

Fig. 20. Results for pseudorandom frequency-hopping interferer.  
![](images/8ab38750c1ce82d4bfc9b02a29d60ed273b825f9fb65ce03d1725e0232f0275b.jpg)

![](images/664d922df0bcf14d416cf425ad206ebd495f5a135259335a548c1cc7bbd49462.jpg)

Fig. 21. Results for direction-dependent constant interferer.  
![](images/0cc823a3f9af6b1ae2fcdfd3bb454e310400ea1f0ff2ac76119b1f5af3fcbbdb.jpg)

![](images/641de72eec447dec080fb3ed116976c8d83e861cf993ada599a23a9cfebadfcd.jpg)

Fig. 22. Results for direction-dependent intermittent interferer, with 90% transmission probability.  
![](images/86f4e11d4d4d79cee70e4ce77bdac74c95eb577dbbeeba15c41feb460e142f40.jpg)

![](images/cc705d3d4c127301b59835c6ba15e75ed6930168570657901ddc92c389e7155a.jpg)  
Fig. 23. Results for direction-dependent intermittent interferer, with 10% transmission probability.

## ACKNOWLEDGMENT

The authors wish to acknowledge the support of Dr. Joe Qui and the Army Research Lab Sensors and Electron Devices Directorate.

## REFERENCES

[1] E. Selvi, A. Martone, K. Sherbondy, and R. Buehrer On the use of Markov decision processes in cognitive radar: An application to target tracking In Proc. IEEE Radar Conf., Apr. 2018, pp. 0537–0542.

[2] H. Griffiths et al. Radar spectrum engineering and management: Technical and regulatory issues Proc. IEEE, vol. 103, no. 1, pp. 85–102, Jan. 2015.

[3] F. C. Commission et al. Auction of advanced wireless services (AWS-3) licenses closes Federal Commun. Commission, Washington DC, DA, pp. 15–131, 2015.

[4] J. Mitola and G. Q. Maguire Cognitive radio: Making software radios more personal IEEE Personal Commun., vol. 6, no. 4, pp. 13–18, Aug. 1999.

[5] A. Martone Cognitive radar demystified URSI Bull., no. 350, pp. 10–22, 2014.

[6] G. E. Smith et al. Experiments with cognitive radar IEEE Aerosp. Electron. Syst. Mag., vol. 31, no. 12, pp. 34–46, Dec. 2016.

[7] M. Martorella, E. Giusti, A. Capria, F. Berizzi, and B. Bates Automatic target recognition by means of polarimetric isar images and neural networks IEEE Trans. Geosci. Remote Sens., vol. 47, no. 11, pp. 3786–3794, Nov. 2009.

[8] F. Benedetto, F. R. Fulginei, A. Laudani, and G. Albanese Automatic aircraft target recognition by isar image processing based on neural classifier Int. J. Adv. Comput. Sci. Appl., vol. 3, no. 8, 2012.

[9] G. Rossetti, A. Deligiannis, and S. Lambotharan Waveform design and receiver filter optimization for multistatic cognitive radar In Proc. IEEE Radar Conf., 2016, pp. 1–5.

[10] P. Chen and L. Wu Waveform design for multiple extended targets in temporally correlated cognitive radar system IET Radar, Sonar Navigat., vol. 10, no. 2, pp. 398–410, 2016.

[11] E. Adler et al. Trends in radar: A US army research laboratory perspective Proc. SPIE, pp. 98290U–98290U, 2016.

[12] F. Smits, A. Huizing, W. van Rossum, and P. Hiemstra A cognitive radar network: Architecture and application to multiplatform radar management In Proc. IEEE EuRAD Eur. Radar Conf., 2008, pp. 312–315.

[13] F. Gini and M. Rangaswamy Knowledge Based Radar Detection, Tracking and Classification, vol. 52. Hoboken, NJ, USA: Wiley, 2008.

[14] J. R. Guerci Cognitive radar: A knowledge-aided fully adaptive approach In Proc. IEEE Radar Conf., 2010, pp. 1365–1370.

[15] J. Metcalf, S. D. Blunt, and B. Himed A machine learning approach to cognitive radar detection In Proc. IEEE Radar Conf., May 2015, pp. 1405–1411.

[16] C. Kreucher and K. Carter An information theoretic approach to processing management In Proc. IEEE Int. Conf. Acoust., Speech Signal Process., 2008, pp. 1869–1872.

[17] U. Gunturkun Toward the development of radar scene analyzer for cognitive radar IEEE J. Ocean. Eng., vol. 35, no. 2, pp. 303–313, Apr. 2010.

[18] M. Shaghaghi and R. S. Adve Machine learning based cognitive radar resource management In Proc. IEEE Radar Conf., Apr. 2018, pp. 1433–1438.

[19] J. M. Peha Sharing spectrum through spectrum policy reform and cogni tive radio Proc. IEEE, vol. 97, no. 4, pp. 708–719, Apr. 2009.

[20] H. Wang, J. Johnson, C. Baker, L. Ye, and C. Zhang On spectrum sharing between communications and air traffic control radar systems In Proc. IEEE Radar Conf., May 2015, pp. 1545–1550.

[21] R. Saruthirathanaworakun, J. M. Peha, and L. M. Correia Opportunistic primary-secondary spectrum sharing with a rotating radar In Proc. Int. Conf. Comput., Netw. Commun., Jan. 2012, pp. 1025–1030.

[22] A. Martone, K. Sherbondy, K. Ranney, and T. Dogaru Passive sensing for adaptable radar bandwidth In Proc. IEEE Radar Conf., May 2015, pp. 0280–0285.

[23] S. S. Bhat, R. M. Narayanan, and M. Rangaswamy Bandwidth sharing and scan scheduling in multimodal radar with communications and tracking IETE J. Res., vol. 59, no. 5, pp. 551–562, 2013.

[24] A. Martone, K. Ranney, K. Sherbondy, K. Gallagher, and S. Blunt Spectrum allocation for non-cooperative radar coexistence IEEE Trans. Aerosp. Electron. Syst., vol. 54, no. 1, pp. 90–105, Feb. 2018.

[25] A. Martone, K. Gallagher, K. Sherbondy, A. Hedden, and C. Dietlein Adaptable waveform design for enhanced detection of moving targets IET Radar, Sonar Navigat., vol. 11, no. 10, pp. 1567–1573, 2017.

[26] J. Jakabosky, B. Ravenscroft, S. D. Blunt, and A. Martone Gapped spectrum shaping for tandem-hopped radar/communications cognitive sensing In Proc. IEEE Radar Conf., May 2016, pp. 1–6.

[27] B. Ravenscroft, S. D. Blunt, C. Allen, A. Martone, and K. Sherbondy Analysis of spectral notching in FM noise radar using measured interference Int. Conf. Radar Syst., Belfast, 2017, pp. 1–6.

[28] K. L. Bell, C. J. Baker, G. E. Smith, J. T. Johnson, and M. Rangaswamy Cognitive radar framework for target detection and tracking IEEE J. Sel. Topics Signal Process., vol. 9, no. 8, pp. 1427–1439, Dec. 2015.

[29] S. Haykin, Y. Xue, and P. Setoodeh Cognitive radar: Step toward bridging the gap between neuroscience and engineering Proc. IEEE, vol. 100, no. 11, pp. 3102–3130, Nov. 2012.

[30] J. M. Fuster Cortex and Mind: Unifying Cognition. London, U.K.: Oxford Univ. Press, 2003.

[31] S. Russell and P. Norvig Artificial Intelligence: A Modern Approach (2nd Edition). Englewood Cliffs, NJ, USA: Prentice-Hall, 2002.

[32] M. Levorato, S. Firouzabadi, and A. Goldsmith A learning framework for cognitive interference networks with partial and noisy observations IEEE Trans. Wireless Commun., vol. 11, no. 9, pp. 3101–3111, Sep. 2012.

[33] A. Kolobov Planning with Markov decision processes: An AI perspective Synthesis Lectures Artif. Intell. Mach. Learn., vol. 6, no. 1, pp. 1–210, 2012.

[34] E. Chong, C. Kreucher, and A. Hero Monte-Carlo-based partially observable Markov decision process approximations for adaptive sensing In Proc. 9th Int. Workshop Discrete Event Syst., May 2008, pp. 173–180.

[35] A. Charlish and F. Hoffman Anticipation in cognitive radar using stochastic control In Proc. IEEE Radar Conf., May 2015, pp. 1692–1697.

[36] M. van Otterlo and M. Wiering Reinforcement Learning and Markov Decision Processes, pp. 3–42. Berlin, Germany: Springer, 2012.

[37] O. Ibe Fundamentals of Applied Probability and Random Processes. New York, NY, USA: Academic, 2014.

[38] S. Haykin and J. M. Fuster On cognitive dynamic systems: Cognitive neuroscience and engineering learning from each other Proc. IEEE, vol. 102, no. 4, pp. 608–628, Apr. 2014.

[39] I. Chadès, G. Chapron, M.-J. Cros, F. Garcia, and R. Sabbadin Markov decision processes (MDP) toolbox Jan. 2015. [Online]. Available: http://www7.inra.fr/mia/T /MDPtoolbox/MDPtoolbox.html

[40] A. F. Martone et al. Adaptable bandwidth for harmonic step-frequency radar Int. J. Antennas Propag., vol. 2015, 2015, Art. no. 808093.

[41] A. Mitchell, G. Smith, K. Bell, A. Duly, and M. Rangaswamy Cost function design for the fully adaptive radar framework IET Radar, Sonar Navigat., vol. 12, no. 12, pp. 1380–1389, 2018.

![](images/27e7582c6e8201373cf66b77946e637a32ae923985d2e275aa07c828f8e09872.jpg)

Ersin S. Selvi received the B.S. degree in electrical engineering from Pennsylvania State University, State College, PA, USA, in 2013, and the M.S. in electrical engineering from Virginia Polytechnic Institute and State University, Blacksburg, VA, USA in 2017.

His research interests include wireless communications, radar, machine learning, and control systems. From 2013 to 2015, he worked in the process automation industry as a System Engineer for Proconex, near Philadelphia, PA, USA. Since 2018, he has been with Raytheon in Arlington, VA, USA, where he is currently an Electrical Engineer.

![](images/ab0686c81ed8c17f64501b8f13b1849a2483e53d0bed4a16105d1391b902baa9.jpg)

R. Michael Buehrer received the Ph.D. degree from Virginia Tech, Virginia, USA, in 1996.

He joined Virginia Tech from Bell Labs, as an Assistant Professor, with the Bradley Department of Electrical and Computer Engineering in 2001. He is currently a Professor of electrical engineering and is the Director of Wireless @ Virginia Tech, a comprehensive research group focusing on wireless communications. In 2009, he was a Visiting Researcher with the Laboratory for Telecommunication Sciences (LTS), a federal research lab which focuses on telecommunication challenges for national defense. While at LTS, his research focus was in the area of cognitive radio with a particular emphasis on statistical learning techniques. His current research interests include cognitive radar, geolocation, machine learning applied to communication systems, position location networks, iterative receiver design, electronic warfare, dynamic spectrum sharing, cognitive radio, communication theory, multiple input multiple output (MIMO) communications, intelligent antenna techniques, ultra wideband, spread spectrum, interference avoidance/mitigation, and propagation modeling. His work has been funded by the National Science Foundation, the Defense Advanced Research Projects Agency, Office of Naval Research, and several industrial sponsors. He has authored or coauthored over 70 journal and approximately 250 conference papers and holds 12 patents in the area of wireless communications.

Dr. Buchrer was co-recipient of the Fred W. Ellersick MILCOM Award for the Best Paper in the unclassified technical program, in 2010. He is currently an Area Editor for IEEE TRANSACTIONS ON WIRELESS COMMUNICATIONS. He was formerly an Associate Editor for IEEE WIRELESS COMMUNICATIONS LETTERS, IEEE TRANSACTIONS ON VE-HICULAR TECHNOLOGIES, IEEE TRANSACTIONS ON WIRELESS COMMUNICATIONS, IEEE TRANSACTIONS ON SIGNAL PROCESSING, and IEEE TRANSACTIONS ON EDUCATION. In 2014, he received the Dean’s Award for Teaching Excellence, and in 2003, he was named Outstanding New Assistant Professor from the Virginia Tech College of Engineering.

![](images/8d5892dd26d702975a701ea7de0558578161eb66265395aa5141a816e43ca826.jpg)

Anthony F. Martone (Senior Member, IEEE) received the B.S. (summa cum laude) degree in electrical engineering from Rensselaer Polytechnic Institute, Troy, NY, USA, in 2001, and the Ph.D. degree in electrical engineering from Purdue University, West Lafayette, IN, USA, in 2007.

He joined the U.S. Army Research Laboratory in Adelphi, MD, USA, in 2007, as a Researcher in the RF Signal Processing and Modeling branch where his research interests include sensing through the wall technology, spectrum sharing, cognitive radar, and radar signal processing. He is currently the Sensors and Electron Devices Directorate Lead for cognitive radar research, where he is overseeing, directing, and collaborating with multiple universities to address spectrum sharing for radar and communication systems, softwaredefined transceiver control, and adaptive processing techniques. Since joining ARL, he has authored more than 100 journal and conference publications, two book chapters, and holds ten patents.

Dr. Martone is an Associate Editor for the IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS since 2017. He has served as a Committee Member for graduate students at The Pennsylvania State University, the Virginia Polytechnic Institute and State University, and Bowie State University. In 2011, he received the Commanders Award for Civilian Service for his research and development of sensing through the wall signal processing techniques. In 2019, he was nominated for the IEEE Aerospace and Electronic Systems Society Radar Systems Panel, where he serves on the Spectrum Innovations Committee.

![](images/24d0b9b4bfa0cc8806f7557ca244d3c587d09f584367da19bffd2eca0981aa61.jpg)

Kelly Sherbondy received the bachelor’s degree in electrical and electronics engineering from Penn State and master’s degree in electrical and electronics engineering from George Washington University.

He is the System Design and Experimentation Associate Branch Chief, RF Signal Processing & Modeling Branch, RF, Electronic Warfare, and Directed Energy (RED) Division, Sensor & Electron Devices Directorate (SEDD), Army Research Laboratory (ARL), Combat Capabilities Development Command (CCDC). His interests include basic, applied and systems research in linear and nonlinear radar detection for improvised explosive device (IED), landmine and unexploded ordnance (UXO). Also, in cognitive radar (CR) development to include dynamic spectrum sensing, waveform adaptation, radar frequency interference (RFI) prediction, software defined radars (SDRs), and transceiver hardware adaptation. He is the Counter IED (CIED) Subject Matter Expert (SME) Lead at SEDD, where he recently spent six months as the Sensors Division’s Chief, in 2019-2020. He is also a Core Member of the Office of Secretary of Defense (OSD)/Joint IED Defeat Organization (JIEDDO), CIED Science & Technology (S&T), Community of Interest (COI), and J8 CIED Executive Agent (EA) Working Group. He was an S&T Countermine Branch Chief for the Night Vision and Electronic Sensors Directorate (NVESD) within the Communications & Electronic Research Development and Engineering Center (CERDEC), where he became a Deputy Countermine Division Chief. Also, he worked four years as the RDECOM CIED Task Force Chair, and one year as the RDECOM CIED Liaison to JIEDDO. He holds three patents and has authored over 50 technical papers in CM & CIED and CR technologies.

Mr. Sherbondy has received the CERDEC Award for Employee of the Year (mid-level management) 2005, Award for Excellence (Management) 2005, Commander’s Award for Civilian Service – CERDEC 2008, Commendation of Achievement – NVESD (2009) & ARL (2012), ARL-SEDD Recognition for Excellence 2010, 2011, and 2012, ARL-SEDD Award for Engineering 2017, ARL-SEDD Award for Mentoring 2019, and ARL-SEDD Award for Entrepreneurial 2019.