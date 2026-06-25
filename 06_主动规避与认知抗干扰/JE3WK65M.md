# A Nonlinear Waveform Selection Method for Cognitive Radar Target Tracking Based on Reinforcement Learning

Peikun Zhu, Xu Si, and Jing Liang\*

School of Information and Communication Engineering

University of Electronic Science and Technology of China, Chengdu, China zhupeikun@std.uestc.edu.cn, xusi@std.uestc.edu.cn, liangjing@uestc.edu.cn

Abstract—Cognitive radar automatically adjusts its waveform via ceaseless interaction with the environment and learning from the experience. The waveform development of cognitive radar has been attracting much attention in improving tracking performance. In this paper, we propose an intelligent radar target tracking strategy based on variable nonlinear frequency modulated waveforms (NLFM). The strategy considers the combination of constant velocity (CV), constant acceleration (CA), and constant turning (CT) motion for high maneuvering targets. A library of NLFM is constructed and the entropy reward Q-Learning (ERQL) method is designed to perform joint waveform parameters selection. It merges the radar and target into a closed loop to provide the optimum target tracking performance, updating the waveform in real-time as the target state changes. Numerical results show that the tracking performance of our proposed method is much better than that of the linear frequency modulated waveform (LFM) pure parameter selection method.

Index Terms—Target tracking, Cognitive radar, Waveform selection, NLFM, ERQL

## I. INTRODUCTION

Cognitive radar adjusts its operating and processing schemes based on the changing scenarios of the environment, to achieve better detection than conventional radars. Waveform design is a key issue in cognitive radar and has become a hot research topic [1]-[3]. In general, linear frequency modulated waveform (LFM) is widely used in radar because of its easy modulation and simple signal processing. However, the NLFM can provide lower sidelobe-matched filter output and avoid the loss of signal-to-noise ratio caused by filter mismatch[4]. It has demonstrated that hyperbolic, exponential, and power-law frequency-modulated chirps [5] with parabolic instantaneous frequencies provide better tracking performance than LFM. Therefore, NLFM has attracted the attention of many scholars.

Modern targets have various shapes, maneuverability, and an increasingly complex electromagnetic environment, while conventional radar only has embedded unitary waveform, which cannot effectively cope with environmental changes. Therefore, the radar waveform type and the parameters such as phase, pulse duration, and chirp rate can be dynamically and adaptively adjusted according to the changes of the environment, to optimally improve the estimation of the target state, and the radar system can achieve better target resolution and tracking performance. Traditional approaches to achieving optimal waveform parameter selection using grid search based on criteria [6] are very costly. Reinforcement learning (RL) [7] and cognitive radar have a similar interactive learning process, which can realize self-learning during the interaction process between the target and the radar, select the optimal waveform parameters, and have perfect real-time performance. Thus, RL is an effective waveform parameter selection method.

In this paper, based on the aforementioned analyses, for cognitive radar maneuvering target tracking, we propose an NLFM selection method based on RL. The main contributions of this work are as follows: (1) A radar waveform selection framework based on the interactive multi-model (IMM) algorithm is proposed, and a predicted method for the measurement error covariance is designed, that is the filtering results are weighted and summed to obtain the predicted measurement error covariance. (2) Taking LFM, hyperbolic frequency modulated waveform (HFM), and exponential frequency modulated waveform (EFM) as examples, an NLFM library is constructed for cognitive radar adaptive waveform selection. (3) Based on RL, an entropy reward Q-learning (ERQL) waveform selection method is designed to jointly select the optimal transmit waveform type and parameters at the next moment according to the predicted measurement error covariance, to achieve the best tracking of maneuvering targets.

## II. SYSTEM MODEL

## A. Target Motion Model

This work focuses on three typical maneuvering target motion models: CV, CA, and CT motion models. The target motion is specified by the following target state model

$$
{ \pmb x } _ { k + 1 } = { \bf F } _ { k } { \pmb x } _ { k } + { \pmb w } _ { k }\tag{1}
$$

where $\scriptstyle { \mathbf { { \mathit { x } } } } _ { k }$ is given by $\mathbf { \boldsymbol { x } } _ { k } = \left[ x _ { k } , \dot { x } _ { k } , \ddot { x } _ { k } , y _ { k } , \dot { y } _ { k } , \ddot { y } _ { k } \right] ^ { \mathrm { T } }$ , among then, $[ x _ { k } , y _ { k } ] , [ \dot { x } _ { k } , \dot { y } _ { k } ] .$ , and $[ \ddot { x } _ { k } , \ddot { y } _ { k } ]$ are defined as the position, velocity, and acceleration of the target. $\mathbf { F } _ { k }$ is the target state transition matrix, ${ \pmb w } _ { k }$ is the process noise and follows the Gaussian distribution of ${ \pmb w } _ { k } \sim \mathcal { N } \left( 0 , { \bf Q } _ { k } \right)$ . The state transition matrices of CA, CA, and CT are as follows

$$
\mathbf { F } _ { k } ^ { \mathrm { c v } } = \mathbf { I } _ { 3 } \otimes { \left[ \begin{array} { l l } { 1 } & { T } \\ { 0 } & { 1 } \end{array} \right] } , \mathbf { F } _ { k } ^ { \mathrm { C A } } = \mathbf { I } _ { 2 } \otimes { \left[ \begin{array} { l l l } { 1 } & { T } & { { \frac { T ^ { 2 } } { 2 } } } \\ { 0 } & { 1 } & { T } \\ { 0 } & { 0 } & { 0 } \end{array} \right] } ,
$$

$$
\mathbf { F } _ { k } ^ { \mathrm { C T } } = \left[ \begin{array} { c c c c c c } { 1 } & { \frac { \sin \omega T } { \omega } } & { 0 } & { 0 } & { - \frac { 1 - \cos \omega T } { \omega } } & { 0 } \\ { 0 } & { \cos \omega T } & { 0 } & { 0 } & { - \sin \omega T } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { 0 } & { \frac { 1 - \cos \omega T } { \omega } } & { 0 } & { 1 } & { \frac { \sin \omega T } { \omega } } & { 0 } \\ { 0 } & { \sin \omega T } & { 0 } & { 0 } & { \cos \omega T } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \end{array} \right] ^ { - }
$$

where $T$ is the sampling period of the measured data, ω is the steering angular velocity, the operator ⊗ denotes the Kronecker operator, and ${ \mathbf I } _ { m }$ denotes an identity matrix of order $m .$ The covariance $\mathbf { Q } _ { k }$ of Gaussian state noise ${ \pmb w } _ { k }$ of CV, CA and CT are as follows

$$
\begin{array} { r l } & { { \bf Q } _ { k } ^ { \mathrm { C V } } = { \bf I } _ { 3 } \otimes [ \begin{array} { c c } { { \bf T } _ { 3 } ^ { 4 } } & { { \bf T } _ { 2 } ^ { 3 } } \\ { \frac { T } { 3 } } & { { \bf T } _ { 2 } ^ { 3 } } \\ { \frac { T ^ { 3 } } { 2 } } & { { \bf T } _ { 3 } ^ { 2 } } \end{array} ] , { \bf Q } _ { k } ^ { \mathrm { C V } } = { \bf I } _ { 2 } \otimes [ \begin{array} { c c } { \frac { T ^ { 2 } } { 2 0 } } & { \frac { T ^ { 4 } } { 8 } } & { \frac { T ^ { 3 } } { 6 } } \\ { \frac { T ^ { 4 } } { 8 } } & { \frac { T ^ { 3 } } { 6 } } & { \frac { T ^ { 2 } } { 2 } } \\ { \frac { T ^ { 3 } } { 8 } } & { \frac { T ^ { 2 } } { 2 } } & { T } \end{array} ] , } \\ & { { \bf Q } _ { k } ^ { \mathrm { C T } } = [ \begin{array} { c c } { { \bf Q } _ { \Lambda } ^ { \mathrm { C T } } } & { { \bf Q } _ { \mathrm { B } } ^ { \mathrm { C T } } } \\ { { \bf Q } _ { \mathrm { B } } ^ { \mathrm { C T } } } & { { \bf Q } _ { \mathrm { A } } ^ { \mathrm { C T } } } \end{array} ] , { \bf Q } _ { \mathrm { A } } ^ { \mathrm { C T } } = [ \begin{array} { c c } { \frac { 2 ( \omega T - \sin \omega T ) } { \frac { 1 - \omega ^ { 3 } \omega T } { \omega ^ { 2 } } } } & { \frac { 1 - \omega ^ { \omega } \omega T } { T } } & { 0 } \\ { \frac { 1 - \omega ^ { 3 } \omega T } { \omega } } & { \frac { T } { T } } & { 0 } \\ { 0 } & { 0 } & { 0 } \end{array} ] , } \\ &  { \bf Q } _ { \mathrm { B } } ^ { \mathrm { C T } } = [ \begin{array} { c c }  \frac  \end{array} \end{array}
$$

where $\mathbf { Q } _ { k }$ can be multiplied by $\overline { { \sigma } } _ { \mathrm { C V } } ^ { 2 } , \sigma _ { \mathrm { C A } } ^ { 2 }$ , and $\sigma _ { \mathrm { C T } } ^ { 2 } ,$ respectively, which are used to control the process noise of the target motion model.

For high-maneuvering targets, the single model can not effectively match the actual state of the target. Therefore, the Interactive multiple model (IMM) is adopted in this paper, and CV, CA, and CT models are taken as model sets tracking targets, and finally form the overall state estimation $\hat { \pmb x } _ { k | k }$ and the overall estimation fusion state error covariance matrix $\mathbf { P } _ { k \mid k }$ of the target. Where the measurement error covariance ${ \bf R } _ { k | k }$ in IMM is given by the measurement Cramer-Rao lower Bound´ (CRLB) $\mathbf { N } ( \pmb { \theta } _ { k } )$

## B. Measurement Model

The measurement vector of the target at time k is given by the following equation

$$
{ z } _ { k } = h _ { k } ( { \pmb x } _ { k } ) + { \pmb v } _ { k }\tag{2}
$$

where $h _ { k } ( \cdot ) = [ h _ { r } ( \cdot ) , h _ { \vec { r } } ( \cdot ) , h _ { \vartheta } ( \cdot ) ] ^ { \mathrm { T } }$ , with

$$
\left\{ \begin{array} { l l } { r = h _ { r } ( { \pmb x _ { k } } ) = \sqrt { \left( x _ { k } - x _ { o } \right) ^ { 2 } + \left( y _ { k } - y _ { o } \right) ^ { 2 } } } \\ { \dot { r } = h _ { \acute { r } } ( { \pmb x _ { k } } ) = [ x _ { k } - x _ { o } , y _ { k } - y _ { o } ] [ \dot { x } _ { k } , \dot { y } _ { k } ] ^ { \mathrm { T } } / r } \\ { \vartheta = h _ { \vartheta } ( { \pmb x _ { k } } ) = \arctan [ ( y _ { k } - y _ { o } ) / ( x _ { k } - x _ { o } ) ] } \end{array} \right.\tag{3}
$$

represent radial distance, radial velocity, and radial angle measurements, respectively. Among them, $[ x _ { o } , y _ { o } ]$ represents the position of the radar, ${ \pmb v } _ { k }$ is the measurement noise, which follows the Gaussian distribution of $\pmb { v } _ { k } \sim \mathcal { N } ( 0 , \mathbf { R } _ { k } )$

## III. WAVEFORM CHARACTERIZATION

For the following complex envelope transmission pulse

$$
\tilde { s } ( t ) = \left( 1 / ( \pi \lambda ^ { 2 } ) \right) ^ { 1 / 4 } \exp \left( - t ^ { 2 } / ( 2 \lambda ^ { 2 } ) \right) \exp ( j 2 \pi b \xi ( t ) )\tag{4}
$$

where λ represents the pulse duration, b represents the modulation slope of the frequency, and ξ(t) represents the real-valued differentiable phase function. The waveform library used in this study is composed of LFM, hyperbolic frequency modulated (HFM), and exponential frequency modulated (EFM) waveforms [5], whose phase function and waveform sweep bandwidth are shown in Table I.

TABLE I  
PHASE FUNCTION AND BANDWIDTH OF FREQUENCY MODULATION WAVEFORMS WITH GAUSSIAN ENVELOPES
<table><tr><td rowspan=1 colspan=1>Waveform</td><td rowspan=1 colspan=1>Phase function</td><td rowspan=1 colspan=1>Frequency sweep</td></tr><tr><td rowspan=1 colspan=1>LFM</td><td rowspan=1 colspan=1> $\overline { { t ^ { 2 } } }$ </td><td rowspan=1 colspan=1> $\overline { { b \lambda } }$ </td></tr><tr><td rowspan=1 colspan=1>HFM</td><td rowspan=1 colspan=1> $\overline { { \ln ( T + | t | ) , T > 0 } }$ </td><td rowspan=1 colspan=1> $\overline { { b / T } }$ </td></tr><tr><td rowspan=1 colspan=1>EFM</td><td rowspan=1 colspan=1> $\frac { \overline { { \operatorname { e x p } ( | t | ) } } } { \operatorname { e x p } ( | t | ) }$ </td><td rowspan=1 colspan=1>bexp(λ/2)</td></tr></table>

Remark 1: $1 / T$ in the table represents the reference frequency, which can be used to modulate the signal.

The narrowband signal ambiguity function of the above complex envelope transmission pulse is defined as

$$
A ( \tau , f _ { d } ) = \int _ { - \infty } ^ { \infty } \tilde { s } \left( t + \frac { \tau } { 2 } \right) \tilde { s } ^ { * } \left( t + \frac { \tau } { 2 } \right) \exp ( - j 2 \pi f _ { d } t ) d t\tag{5}
$$

Substitute (5) into (6) can obtain

$$
\begin{array} { r } { A ( \tau , f _ { d } ) = \displaystyle \int _ { - \infty } ^ { \infty } \frac { 1 } { \lambda \sqrt { \pi } } \exp \left[ - \left( \frac { 1 } { \lambda ^ { 2 } } \right) \left( t ^ { 2 } + \frac { \tau ^ { 2 } } { 4 } \right) \right] \cdot } \\ { \exp ( j 2 \pi b \beta ( \tau ) ) \exp ( - j 2 \pi f _ { d } t ) d t } \end{array}\tag{6}
$$

where

$$
\beta ( \tau ) = \xi \left( t - \frac { \tau } { 2 } \right) - \xi \left( t + \frac { \tau } { 2 } \right)\tag{7}
$$

Take the second partial derivatives of the ambiguity functions (6), and substitute $\tau = 0$ and $f _ { d } = 0$ , can obtain

$$
\left\{ \begin{array} { l l } { \left. \frac { \partial ^ { 2 } A ( \tau , f _ { d } ) } { \partial \tau ^ { 2 } } \right| _ { \tau = 0 } = - \frac { 1 } { 2 \lambda ^ { 2 } } - g ( \xi ) } \\ { \left. \frac { \partial ^ { 2 } A ( \tau , f _ { d } ) } { \partial \tau \partial f _ { d } } \right| _ { f _ { d } = 0 } = - 2 \pi \int _ { - \infty } ^ { \infty } \frac { t \xi ^ { \prime } ( t ) } { \lambda \sqrt { \pi } } \exp \left[ - \left( \frac { t ^ { 2 } } { \lambda ^ { 2 } } \right) \right] d t } \\ { \left. \frac { \partial ^ { 2 } A ( \tau , f _ { d } ) } { \partial f _ { d } ^ { 2 } } \right| _ { f _ { d } = 0 } = - ( 2 \pi ) ^ { 2 } \frac { \lambda ^ { 2 } } { 2 } } \end{array} \right.\tag{8}
$$

where

$$
\begin{array} { r l } & { g ( \xi ) = ( 2 \pi b ) ^ { 2 } \int _ { - \infty } ^ { \infty } \frac { \left( \xi ^ { \prime } ( t ) \right) ^ { 2 } } { \lambda \sqrt { \pi } } \exp \left( - \frac { t ^ { 2 } } { \lambda ^ { 2 } } \right) d t } \\ & { f ( \xi ) = 2 \pi b \int _ { - \infty } ^ { \infty } \frac { t \xi ^ { \prime } ( t ) } { \lambda \sqrt { \pi } } \exp \left( - \frac { t ^ { 2 } } { \lambda ^ { 2 } } \right) d t } \end{array}\tag{9}
$$

Since the elements of Fisher information matrix (FIM) J are the result of multiplying the negative of the above partial derivative by the signal-to-noise ratio (SNR) η

$$
{ \mathbf J } = \eta \left[ \begin{array} { c c } { \frac { 1 } { 2 \lambda ^ { 2 } } + g ( \xi ) } & { 2 \pi f ( \xi ) } \\ { 2 \pi f ( \xi ) } & { ( 2 \pi ) ^ { 2 } \frac { \lambda ^ { 2 } } { 2 } } \end{array} \right]\tag{10}
$$

Let the impulse duration λ and the frequency modulation slope b form the estimation vector $\pmb { \theta } = [ \lambda , b ] ^ { T }$ . Through the transition matrix T = diag $( c / 2 , c / 2 \omega _ { c } )$ (c is the speed of light and $\omega _ { c }$ is the carrier frequency), the CRLB of the measurement error of the modulated waveform can be obtained as [8]

$$
\mathbf { N } \left( \pmb { \theta } _ { k } \right) = \mathbf { T J } \left( \pmb { \theta } _ { k } \right) ^ { - 1 } \mathbf { T } ^ { \mathrm { T } }\tag{11}
$$

In the target tracking system, when the SNR of the received signal is large enough and the sidelobe of the ambiguity of the signal can be ignored, the target delay Doppler estimation error can reach the CRLB. That is the CRLB measurement noise covariance. This value is related to the waveform parameter, thus establishing a link between the parameter and the tracking algorithm.

## IV. WAVEFORM SELECTION METHOD

RL and cognitive radar waveform parameter selection have a similar interactive learning process. Therefore, radar waveform parameter selection based on RL is a research focus of cognitive radar. The Q learning (QL) method is a typical modelless reinforcement learning method. In QL, the Q value of the state action pair $( s , a )$ is defined as the expected cumulative discount reward, and the Q value can be obtained according to the following updated equation [9]:

$$
Q _ { k + 1 } ( s , a ) = Q _ { k } ( s , a ) + \alpha \left[ r _ { k } + \gamma \operatorname* { m a x } _ { a ^ { \prime } } Q _ { k } ( s ^ { \prime } , a ^ { \prime } ) - Q _ { k } ( s , a ) \right]\tag{12}
$$

where $s \in \mathbf { S }$ is agent state, $a \in \mathbf { A }$ is agent action, S and A represent agent state and agent action set, respectively. α is the learning rate, $\gamma \in [ 0 , 1 ]$ is the discount factor, $r _ { k }$ is the instant reward, which specific form will be given later.

After enough iterations to make the Q table converge, select the action with the largest Q value $Q ^ { * }$ as the best decision $\pi ^ { * } ( s )$

$$
\pi ^ { * } ( s ) = \arg \operatorname* { m a x } _ { a \in \mathbf { A } } Q ^ { * } ( s , a )\tag{13}
$$

In the single CV, CA, or CT scenario, the Bayesian filter at the radar receiver estimates the target state, and feedback the prediction error covariance $\mathbf { P } _ { k + 1 | k + 1 }$ to the radar transmitter, and radar selects the optimal waveform parameters based on the QL algorithm. In this paper, the IMM filtering algorithm is considered. When predicting the error covariance, the following formula should be used for weighted summation:

$$
\breve { \mathbf { P } } _ { k + 1 | k + 1 } = \sum _ { j = 1 } ^ { 3 } \bar { c } _ { k } ^ { ( j ) } \mathbf { P } _ { k + 1 | k + 1 } ^ { ( j ) }\tag{14}
$$

where $\breve { \mathbf { P } } _ { k + 1 | k + 1 }$ represents prediction error covariance, $\bar { c } _ { k } ^ { ( i ) }$ is the prediction model probability [10], $\mathbf { P } _ { k + 1 | k + 1 } ^ { ( j ) }$ represents the prediction error covariance of CA, CT, and CV, respectively.

According to the previous foundation, the ERQL method can be designed as follows:

Firstly, the tracking performance of the radar is evaluated according to the state estimation error covariance $\mathbf { P } _ { k \mid k }$ at time $k .$ The evaluation criterion is entropy state (ES), it follows that:

$$
\mathrm { E S } _ { k } = \operatorname* { d e t } ( \mathbf { P } _ { k | k } )\tag{15}
$$

where $\mathrm { E S } _ { k }$ represents the entropy at time k, and the waveform parameter $\pmb { \theta } _ { k }$ transmitted at time k is rewarded by comparing the ES at time $k - 1$ and k. The designed reward function is as follows

$$
r _ { k } = \log ( 1 + | \mathrm { E S } _ { k - 1 } - \mathrm { E S } _ { k } | ) \mathrm { s i g n } ( \mathrm { E S } _ { k - 1 } - \mathrm { E S } _ { k } )\tag{16}
$$

where sign(·) is the signum function. When the ES is less at time k than $k - 1$ , the waveform results in less estimation uncertainty and is positively rewarded. Otherwise, a negative reward is given.

Then, calculate the real-time reward $r _ { k }$ by (16) and (17), and update the Q table according to (13).

Next, predict $\breve { \mathbf { P } } _ { k + 1 | k + 1 } ( \theta _ { k + 1 } )$ in a one-step according to (15) and combine (16) and (17) to calculate the prediction reward $\hat { r } _ { k + 1 }$ , and update the Q table again according to (13). Repeat this step until the Q table converges.

Finally, use the above method to obtain the Q table of other waveforms, compare the Q table of the different waveforms, and obtain the optimal waveform strategy $\pi _ { k + 1 } ^ { * } ( s )$ at time $k + 1$

## V. SIMULATION RESULTS AND DISCUSSIONS

The simulation assumes that the radar is located at the original point of the coordinate. The initial position of the maneuvering target is (3000, 3000) m, and the initial velocity is $( 0 . 1 , \ 0 . 1 ) \ m / s ,$ and the motion trajectory is divided into three stages. The total movement time is 50 seconds, and the sampling interval is $T = 0 . 1 \ s .$ Considering the composite motion scene of the target. Within $0 \sim 2 0 ~ s ,$ , the target makes a constant acceleration with the radial acceleration of $1 0 m / s ^ { 2 }$ Within $2 1 \sim 4 0 \ s ,$ , the target makes a constant turning motion with a turning rate of $\omega = - 0 . 3 5 r a d / s$ . Within 41 ∼ 50 s, the target moves at a constant velocity. The radar carrier frequency is $f _ { c } ~ = ~ 1 0 . 4 G H z$ and the noise coefficient is $\sigma _ { \mathrm { C V } } = \sigma _ { \mathrm { C A } } = \sigma _ { \mathrm { C T } } = 0 . 0 1$

The initial target state estimation $\hat { \mathbf { \eta } } _ { \hat { \mathbf { \eta } } ( 0 | 0 }$ and its error covariance $\mathbf { P } _ { 0 | 0 }$ of CA are $\hat { \mathbf { x } } _ { 0 \mid 0 } ~ = ~ [ 3 0 \dot { 1 } 0 , 4 , 0 , 3 0 1 0 , 4 , 0 ] ^ { \mathrm { T } }$ ${ \bf P } _ { 0 | 0 } = \mathrm { d i a g } \dot { ( } 1 0 ^ { 2 } , 2 ^ { 2 } , 0 , 1 0 ^ { 2 } , 2 ^ { 2 } , 0 )$ , respectively. The measurement of radial distance r, radial velocity r˙, and radial azimuth angle ϑ can be regarded as an independent measurement process, and the azimuth angle ϑ depends only on the SNR of the receiver. The CRLB of azimuth angle ϑ estimation is $\sigma _ { \vartheta } = \vartheta _ { 3 d B } / ( \kappa \sqrt { \eta } )$ , where half power beam width $\vartheta _ { 3 d B } = 3$ and monopulse error slope $\kappa = 1$ . Therefore, the measurement noise covariance is as follows

$$
\mathbf { R } ( \pmb { \theta } _ { k } ) = \mathrm { b l k d i a g } \left[ \mathbf { N } ( \pmb { \theta } _ { k } ) , \sigma _ { \vartheta } ^ { 2 } \right]\tag{17}
$$

The waveform parameter library adopted in this paper is $P = \{ \lambda \in \left[ 1 0 ^ { - 7 } , \overset { \cdot } { 1 } 0 ^ { - 6 } \right] s , b \in \left[ { \dot { - } } \overset { \cdot } { 1 } 0 ^ { 9 } , \overset { \cdot } { 1 0 } ^ { 9 } \right] H z / s \}$ . The step sizes of waveform parameters are $\Delta \lambda = { \overset { - } { 0 } } . 5 \times 1 0 ^ { - 7 }$ s and $\Delta b = 0 . 2 \times 1 0 ^ { 9 } ~ H z / s .$ , respectively.

According to the radar equation, the SNR η of target echo with range $R = R _ { \mathrm { T x } } = R _ { \mathrm { R x } }$ is approximated as follows

$$
\eta = R _ { 0 } ^ { 4 } / ( R _ { \mathrm { T x } } ^ { 2 } R _ { \mathrm { R x } } ^ { 2 } )\tag{18}
$$

where $R _ { 0 }$ is the distance of 0dB SNR, at this time $R _ { \mathrm { T x } } = R _ { 0 }$ which is set as 7000 m in this simulation experiment.

The simulation uses the ERQL method to carry out the simulation experiments of LFM pure parameter selection and joint selection of waveform parameters. Due to the page limit, the root mean square error (RMSE) of position and velocity are shown with the X-axis as an example. Fig. 1 shows the comparison of position tracking error and velocity tracking error between the pure parameter selection method and the joint selection method of waveform parameters. It can be found that the position and velocity tracking errors of the joint waveform and parameter selection method are smaller, and compared with the pure parameter selection of the LFM method, the position and velocity tracking accuracy is increased by about 85% and 81%, respectively.

![](images/949239e6b6b670e61bd02c56f479ba5eac9ac5bcca5690ca011b47ea10000df1.jpg)  
(a)

![](images/fd2040c7936f9ec7f0943155d2e1aa00fdd2409e955fb47f51e247510eb09e18.jpg)  
(b)  
Fig. 1. The RMSE of the target position and velocity(X-axis). (a)Position, (b)Velocity.

Fig. 2 shows the comparison of the waveform parameter change curves of the two methods during the target tracking process. It can be seen that compared with the pure parameter selection method, the Joint waveform parameters selection method selects a longer pulse duration when tracking the target. And the selected chirp rate has less fluctuation.

![](images/4b6a0039a13aa6d9331021dbf13665c48e0ccfe6b71ad9d58cf8a62570ed762f.jpg)  
(a)

![](images/4f1d12dc6eab028117984c58e0b849fecf2a6ee202340977bf95260b23a0db5e.jpg)  
(b)  
Fig. 2. The pulse duration and chirp rate during target tracking. (a)Pulse duration, (b)Chirp rate.

Fig. 3 shows the selection results of the waveform type by the joint selection method of waveform parameters and each motion model selects probabilistic. It can be seen from Fig. 3(a) that in the process of target tracking, cognitive radar tends to select nonlinear waveforms HFM and EFM, which illustrates the superiority of NLFM in target tracking. Fig. 3(b) shows that the joint waveform parameter selection method has a higher selection probability for each motion stage, which is also one of the reasons for better target tracking performance.

## VI. CONCLUSION

This work proposes an NLFM selection method for cognitive radar target tracking based on RL. Through the interaction between the radar and the target, the CA, CT, and CV multimodel algorithms are combined with the ERQL waveform parameters selection method, and the optimal transmit waveform parameters are selected from the NLFM library. Numerical simulation results show that the position and velocity accuracy of the joint selection of waveform parameters is about 85% and 81% higher than the pure parameters selection of the LFM method. In addition, the cognitive radar is more inclined to select nonlinear waveforms to cope with the change of target state. In the future, the waveform selection criterion and NLFM design method can be further investigated to achieve optimal waveform illumination.

![](images/79fa00d744621d63f65f6da77b08397f20c5ee5bd9788897335f72416d932bec.jpg)  
(a)

![](images/f1194ae6b22e6a5f8b2092ebd91642b4fdbf6a7dfc396848878cd5f367aa9305.jpg)  
(b)  
Fig. 3. The joint selection results of radar transmitting waveforms and each motion model selects probabilistic. (a)1: LFM, 2: HFM, 3: EFM (The waveform type is the average of 100 Monte Carlo simulations). (b)Each motion model selects probabilistic results.

## REFERENCES

[1] A. E. Mitchell, J. L. Garry, A. J. Duly, et al, “Fully Adaptive Radar for Variable Resolution Imaging,” IEEE Transactions on Geoscience and Remote Sensing, vol. 57, no. 12, pp. 9810-9819, Dec. 2019.

[2] Z. Luo, J. Liang, Z. Xu, “Intelligent Waveform Optimization for Target Tracking in Radar Sensor Networks,” Communications, Signal Processing, and Systems (CSPS 2021), Springer-Verlag, Germany, pp. 165-172, Jul. 2021.

[3] P. Zhu, J. Liang, Z. Luo, et al. “Waveform selection method of cognitive radar target tracking based on reinforcement learning,” Journal of Radars, in press.

[4] T. Wei, W. Wang, Y. Zhang and R. Wang, ”A Novel Nonlinear Frequency Modulation Waveform With Low Sidelobes Applied to Synthetic Aperture Radar,” IEEE Geoscience and Remote Sensing Letters, vol. 19, pp. 1-5, 2022, Art no. 4515405.

[5] S. P. Sira, A. Papandreou-Suppappola, D. Morrell, “Advances in waveform-agile sensing for tracking,” Morgan & Claypool Publishers (2009).

[6] B. Le, B. Jiu, H. W. Liu, et al, “An Adaptive Waveform Selection Method for Target Tracking,” Journal of Xidian University, Xian, China, pp. 57- 63, 2014.

[7] Y. Yorozu, M. Hirano, K. Oka, and Y. Tagawa, “Electron spectroscopy studies on magneto-optical media and plastic substrate interface,” IEEE Trans. J. Magn. Japan, vol. 2, pp. 740–741, August 1987 [Digests 9th Annual Conf. Magnetics Japan, p. 301, 1982].

[8] D. J. Kershaw and R. J. Evans, “Optimal waveform selection for tracking systems, ” IEEE Transactions on Information Theory, vol. 40, no. 5, pp. 1536-1550, Sept. 1994.

[9] Q. Wang, Y. Qiao and L. Gao, “A Cognitive Radar Waveform Optimization Approach Based on Deep Reinforcement Learning,” 2019 IEEE International Conference on Signal, Information and Data Processing (ICSIDP), Chongqing, China, 2019, pp. 1-6.

[10] M. Yeddanapudi, Y. Bar-Shalom and K. Pattipati, “IMM estimation for multitarget-multisensor air traffic surveillance,” Proceedings of the IEEE, vol. 85, no. 1, pp. 80-96, Jan. 1997.