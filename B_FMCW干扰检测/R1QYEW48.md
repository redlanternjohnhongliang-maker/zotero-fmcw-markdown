Received January 18, 2020, accepted February 20, 2020, date of publication February 28, 2020, date of current version March 16, 2020. Digital Object Identifier 10.1109/ACCESS.2020.2977098

# A PELT-KCN Algorithm for FMCW Radar Interference Suppression Based on Signal Reconstruction

ZHENYU LIU , WEI LU , JIAYAN WU , SIYUAN YANG , AND GUANGPING LI School of Information Engineering, Guangdong University of Technology, Guangzhou 510006, China

Corresponding author: Wei Lu (luway158@gmail.com)

This work was supported in part by the Guangzhou Science and Technology Plan Project under Grant 201907010003, and in part by the Science and Technology Program of Guangzhou, China, under Grant 201704030093.

ABSTRACT In frequency-modulated continuous-wave (FMCW) radar interference suppression based on signal reconstruction, the pruned exact linear time (PELT) algorithm is used to detect the time positions of the interference. Due to the uncertain penalty factor of the PELT algorithm, the exactness of the position detection is reduced; thus, the suppression performance is degraded. We propose a PELT algorithm with a known change number (PELT-KCN), where a known change number is used to calculate the optimal penalty factor such that the high accuracy of the algorithm can be guaranteed. After interference recognition, the beat signal is separated into two parts: the undamaged signal and the damaged signal. The former is utilized to restore the latter through an autoregressive (AR) model. In simulations and field experiments, we applied our proposed PELT-KCN algorithm to the interference suppression method and verified its performance. Our method can accurately detect the time positions of interference and effectively improve the signal-to-noise ratio (SNR) of the detected targets.

INDEX TERMS Change-point detection, frequency modulated continuous wave (FMCW) radar, mutual interference suppression, signal restoration.

## I. INTRODUCTION

Mm-wave radar sensors have become increasingly popular among automotive radar systems [1], [2]. Among the numerous types of radar sensors, FMCW radars have been the most widely used in automotive mm-wave radar systems in recent years due to their simple radio structure, low power consumption, etc. [3]. However, as the number of vehicles equipped with FMCW radar systems increases, so does the possibility of radar-to-radar interference, which may seriously affect the detection performance of these radar systems [4]. When signals transmitted by other radars are directly or indirectly received by the victim radar, the increased noise floor created by the mutual interference lowers the target detection accuracy, which may lead to traffic accidents. Therefore, the problem of mutual interference between FMCW radar systems has seen increased importance [5].

The associate editor coordinating the review of this manuscript and

The method proposed in [6] changes the slope of the chirp signal to suppress the effect of interference. This method can improve the signal-to-noise ratio (SNR) of the beat signal; however, it does not work properly when the power of the interference signal is high compared to the desired signal. In [7], the effect of mutual interference was mitigated by using morphological component analysis (MCA) to separate the interference from the received signal according to the sparse difference of the beat in the STFT domain and DFT domain. However, MCA does not work well if the period of the interference is not sufficiently long for the analysis. The authors in [8] proposed a method whereby they applied deep learning to mitigate interference. One problem of this method is that it is difficult to find numerous suitable labels for all types of scenarios before applying deep learning. In [9], mutual interference was suppressed by changing the start frequency of each FMCW radar to assure that the beat signal resulting from mixing the transmitted signals of two different sensors has a beat frequency higher than the cut-off frequency of the low-pass IF filter. The problem with the method proposed in [9] is that a coordination mechanism has not been proposed to determine how to change the start frequency of all FMCW radars on the road. In [10], the amplitude of the interference was reduced to a level similar to that of the desired signal by using the advanced weighted-envelope normalization (AWEN) method to improve the SNR of the detected targets. However, suppressed interference still exists and distorts the beat signal. If the period of interference is long, the mis-detection probability of the desired targets will be higher. To solve this problem, a method proposed in [11] uses the signal out of the period of interference to restore the signal in the period of interference by the AR model. However, the authors of [11] have not proposed a method to detect the start and end points of the interference in the time domain for distinguishing between the interfered signal and the desired signal, which was the key factor deciding the performance of signal reconstruction in [11].

Because the interference and the signal reflected from the target have different power, they show different statistical properties in the beat signal. Change-point analysis is the identification of points within a data set where the statistical properties change [12]. Therefore, the problem of detecting the start and end points of the interference in [11] can be solved by using the change-point detection method according to the difference in the statistical properties between the interference and the desired signal. Among the numerous change-point detection methods, the method based on the pruned exact linear time (PELT) search algorithm is preferred because (i) it is only controlled by one parameter, the penalty factor; (ii) it can guarantee that the global optimum will be found; and (iii) a pruned exact linear time method is used in the algorithm to increase the computational efficiency without affecting the exactness of the partitioning [13]. However, the penalty factor is a preset constant, which cannot guarantee that it is the optimal value for any data set. If the penalty factor is too small compared to the optimal value, many change-points will be detected, even those that are the result of noise. Conversely, only the most significant changes or possibly no changes will be detected with a large penalty factor. To reduce the possibility of the two situations above, it is necessary to propose a method to find the optimal penalty factor. One solution is to obtain the optimal factor according to the number of changes measured previously [14].

Therefore, we propose a PELT-KCN algorithm for mutual interference suppression in FMCW radar. First, the envelope of the beat signal is obtained by the WEN algorithm. Second, the number of change-points is determined according to the variation of the envelope. Third, more accurate positions of the interference in the time domain are obtained by the PELT-KCN algorithm based on the known number of changepoints. Finally, the degraded signals are restored by using the result of the PELT-KCN algorithm and the AR model proposed in [11].

![](images/71b501af45c1a3f2658f444e6ad3a756e6189a3cd61c6fd14b6a616353fcac7e.jpg)  
FIGURE 1. A typical FMCW radar system.

## II. SIGNAL MODEL

Fig. 1 demonstrates a simplified block diagram of the main RF components of an FMCW radar system. The chirp signal is transmitted from VCO, and the received signal reflected from the target is mixed with the output of VCO to obtain the beat signals. The time delay and Doppler shift frequency of the target can be obtained from the beat signal.

## A. SIGNAL WITHOUT INTERFERENCE

The TX signal of an FMCW radar system can be expressed by the following equation:

$$
x _ { t } ( t ) = A \cos ( 2 \pi ( ( f _ { c } - \frac { B W } { 2 } ) t + \frac { B W } { 2 t _ { m } } t ^ { 2 } ) ) ,\tag{1}
$$

where A is the amplitude of the TX signal, $f _ { c }$ is the carrier frequency, BW is the sweep bandwidth, and $t _ { m }$ is the duration of a single chirp.

The RX signal from multiple targets can be expressed as

$$
\begin{array} { c c c } { \displaystyle { x _ { r } ( t ) = \sum _ { i = 1 } ^ { M } B _ { i } \cos ( 2 \pi ( ( f _ { c } - \frac { B W } { 2 } + f _ { d , i } ) ( t - t _ { d , i } ) } } \\ { \displaystyle { + \frac { B W } { 2 t _ { m } } ( t - t _ { d , i } ) ^ { 2 } ) ) , } } \end{array}\tag{2}
$$

where M is the number of targets, $B _ { i }$ is the attenuated amplitude of reflection from the i-th target, and $f _ { d , i }$ and $t _ { d , i }$ are the Doppler frequency shift and time delay of the reflection from the i-th target, respectively. For simplification, the noise component is not included in the above equation.

The beat signal produced by the mixer can be represented as

$$
\begin{array} { c } { \displaystyle { x _ { s } ( t ) = \sum _ { i = 1 } ^ { M } C _ { i } \cos ( 2 \pi ( \frac { B W } { t _ { m } } t _ { d , i } - f _ { d , i } ) t } } \\ { \displaystyle { + 2 \pi ( f _ { c } - \frac { B W } { 2 } + f _ { d , i } ) t _ { d , i } - \frac { \pi B W } { t _ { m } } t _ { d , i } ^ { 2 } ) ) , } } \end{array}\tag{3}
$$

where $C _ { i }$ is the amplitude of the demodulated signal from the i-th target. The beat frequency is defined by the following equation:

$$
f _ { b , i } = \frac { B W } { t _ { m } } t _ { d , i } - f _ { d , i } .\tag{4}
$$

Then the beat frequency can be converted to the distance between the radar and the i-th target by

$$
d i s t _ { i } = \frac { ( f _ { b , i } + f _ { d , i } ) \cdot c } { 2 s l o } ,\tag{5}
$$

where $\begin{array} { r } { s l o \ = \ \frac { B W } { t _ { m } } } \end{array}$ denotes the chirp slope, and c denotes the speed of light.

The fast Fourier transform (FFT) is used to transform the beat signal $x _ { s } ( t )$ from the time domain to the frequency domain, where peak detection methods, such as the constant false alarm rate (CFAR) method, can be applied to detecting the peak, whose index represents the beat frequency $f _ { b , i }$ of the i-th target. Based on equation (5), the distance spectrum can be obtained by converting the indexes of the frequency spectrum to the distances.

## B. SIGNAL WITH INTERFERENCE

When interferers are present, the sum of all interference signals from other radar systems is expressed by

$$
\begin{array} { c } { { \displaystyle x _ { r } ^ { I } ( t ) = \sum _ { i = 1 } ^ { N } B _ { i } ^ { I } \cos ( 2 \pi ( ( f _ { c , i } ^ { I } - \frac { B W _ { i } ^ { I } } { 2 } + f _ { d , i } ^ { I } ) } } \\ { { ( t - t _ { d , i } ^ { I } ) + \displaystyle \frac { B W _ { i } ^ { I } } { 2 t _ { m , i } ^ { I } } ( t - t _ { d , i } ^ { I } ) ^ { 2 } ) ) , } } \end{array}\tag{6}
$$

where N is the number of interferers. For the i-th interference signal, $B _ { i } ^ { I }$ is the amplitude, $f _ { c , i } ^ { I }$ is the carrier frequency, $B W _ { i } ^ { I }$ is the bandwidth, $t _ { m , i } ^ { I }$ is the duration of a single chirp, $f _ { d , i } ^ { I }$ is the Doppler frequency, and $t _ { d , i } ^ { I }$ is the time delay. I denotes the symbol of the interference.

In the i-th interference signal, the slope of the chirp is determined by $B W _ { i } ^ { I }$ and $t _ { m , i } ^ { I } . \mathrm { A }$ ghost target occurs when the interfering signal and our transmitted signal have the same or similar slopes [15]; moreover, $t _ { d , i } ^ { I }$ is very short, i.e., within the maximum time delay $\begin{array} { r } { t _ { d m a x } = \frac { 2 d i s t _ { m a x } } { c } } \end{array}$ (here, $d i s t _ { m a x }$ is the maximum detection range). This situation rarely occurs, with probability less than $\begin{array} { r } { 0 . 0 \bar { 0 } 0 1 6 ( = \frac { t _ { d m a x } } { 2 t _ { m } } ) [ 1 6 ] , [ 1 7 ] } \end{array}$ . Thus, it will not be discussed in this paper.

With the interference, the beat signal can be categorized into two cases according to the mixing conditions, as shown by Fig. 11.

## 1) CASE 1

Both the TX signal and the interfering signal have positive or negative chirp slopes, as shown by Fig. 2(a). The beat signal can be described as

$$
y ( t ) = x _ { s } ( t ) + x _ { I } ^ { S S } ( t ) ,\tag{7}
$$

where $x _ { I } ^ { S S } ( t )$ , the mixer output of this case, is described as

$$
\begin{array} { c } { { \displaystyle x _ { I } ^ { S S } ( t ) = \sum _ { i = 1 } ^ { N } C _ { i } ^ { I } \cos ( 2 \pi ( ( f _ { c } - f _ { c , i } ^ { I } ) \mp ( \frac { B W } { 2 } - \frac { B W _ { i } ^ { I } } { 2 } ) } } \\ { { \displaystyle \pm ( \frac { B W _ { i } ^ { I } } { t _ { m , i } ^ { I } } t _ { d , i } ^ { I } \mp f _ { d , i } ^ { I } ) ) t \pm \pi ( \frac { B W } { t _ { m } } - \frac { B W _ { i } ^ { I } } { t _ { m , i } ^ { I } } ) t ^ { 2 } } } \\ { { \displaystyle + 2 \pi ( f _ { c , i } ^ { I } \mp \frac { B W _ { i } ^ { I } } { 2 } + f _ { d , i } ^ { I } ) t _ { d , i } ^ { I } \mp \frac { \pi B W _ { i } ^ { I } } { t _ { m , i } ^ { I } } t _ { d , i } ^ { I } ) . } } \end{array}\tag{8}
$$

![](images/b7eee690d2cfcce9ec09482ac94ff5b195a0ba333970eb965157294ae2382163.jpg)

(a) Same-Sign Case.  
![](images/07a1b599e499a26adcce10413ffe5a7d535633ed8f1e5b95e955df211dc486b8.jpg)  
(b) Different-Sign Case.  
FIGURE 2. Different mixing signal cases.

## 2) CASE 2

The TX signal has a positive chirp slope, and the interference signal has a negative chirp slope or vice versa, as shown by Fig. 2(b). The beat signal can be described as

$$
y ( t ) = x _ { s } ( t ) + x _ { I } ^ { D S } ( t ) ,\tag{9}
$$

where $x _ { I } ^ { D S } ( t )$ , the mixer output of this case, is described as

$$
\begin{array} { r } { x _ { I } ^ { D S } ( t ) = \displaystyle \sum _ { i = 1 } ^ { N } C _ { i } ^ { I } \cos ( 2 \pi ( ( f _ { c } - f _ { c , i } ^ { I } ) \mp ( \frac { B W } { 2 } - \frac { B W _ { i } ^ { I } } { 2 } ) } \\ { \mp ( \frac { B W _ { i } ^ { I } } { t _ { m , i } ^ { I } } t _ { d , i } ^ { I } \mp f _ { d , i } ^ { I } ) ) t \pm \pi ( \frac { B W } { t _ { m } } - \frac { B W _ { i } ^ { I } } { t _ { m , i } ^ { I } } ) t ^ { 2 } } \\ { + 2 \pi ( f _ { c , i } ^ { I } \pm \frac { B W _ { i } ^ { I } } { 2 } + f _ { d , i } ^ { I } ) t _ { d , i } ^ { I } \pm \frac { \pi B W _ { i } ^ { I } } { t _ { m , i } ^ { I } } t _ { d , i } ^ { I } ) . } \end{array}\tag{10}
$$

Let the discrete sequence of $y ( t )$ be denoted by $y _ { 1 : K } =$ $( y _ { 1 } , \dots , y _ { K } )$ , where K is the length of the sequence. With interference, the beat frequency can hardly be extracted from $y _ { 1 : K }$ using only the FFT and CFAR methods due to the low SNR. The remainder of this paper will concern the processing of $y _ { 1 : K }$

## III. INTERFERENCE DETECTION AND SIGNALRECONSTRUCTION

## A. INTERFERENCE DETECTION

## 1) CHANGE-POINT DETECTION

The interference signal and RX signal have different powers; consequently, the statistical properties of the interference components in $y _ { 1 : K }$ will change. In this case, change-point detection methods can be used to measure the position of the interference. We assume that there are L segments of interference in $y _ { 1 : K } ;$ thus, there are $m ( = 2 L )$ change-points in $y _ { 1 : K }$ . Let $\tau _ { 1 : m } = ( \tau _ { 1 } , \ldots , \tau _ { m } )$ denote the sequence of changepoints. We set $\tau _ { 0 } = 0$ and $\tau _ { m + 1 } = K$ such that the changepoints split the data into m + 1 segments, with the ith segment containing the data points $y _ { ( \tau _ { i - 1 } + 1 ) : \tau _ { i } } ~ = ~ ( y _ { \tau _ { i - 1 } + 1 } , \ldots , y _ { \tau _ { i } } )$ [18], and we assume that $\tau _ { 1 : m }$ is ordered such that $\tau _ { i } ~ < ~ \tau _ { j }$ if and only if $\begin{array} { r l r } { i } & { { } < } & { j . } \end{array}$ As a result, $y _ { 1 : K }$ will be split into $m + 1$ segments by $\tau _ { 1 : m }$ . Finally, the problem of interference detection can be transformed into minimizing

$$
\sum _ { i = 1 } ^ { m + 1 } [ c ( y _ { \tau _ { i - 1 } + 1 : \tau _ { i } } ) ] + \beta p e n ( m ) .\tag{11}
$$

Here, $c ( \cdot )$ is a cost function for the segment, and $\beta p e n ( m )$ is a penalty used to guard against overfitting. $\beta$ is the penalization parameter, and pen(m) is a function of m that increases with the number of change-points m. In this paper, we choose the mean as the statistical property in change-point detection. As a result, the cost function c(·) uses

$$
c ( y _ { a : b } ) = \sum _ { t = a + 1 } ^ { b } \| y _ { t } - \bar { y } _ { a : b } \| ^ { 2 } ,\tag{12}
$$

where $\bar { y } _ { a : b }$ is the empirical mean of the sub-signal $y _ { a : b }$ [19]. According to the most popular information criteria, such as AIC and the Schwarz criteria, it is usually suggested to use $p e n ( m ) = m \left[ 1 2 \right]$

However, if we want to use the exhaustive search method to minimize equation (11) for all possible values of m and $\tau ,$ a huge solution space will be obtained. For the series $y _ { 1 : K }$ there are $2 ^ { K - 1 }$ possible solutions when m is unknown. When m is known, there are still $C _ { K - 1 } ^ { m - 1 }$ solutions (i.e., if $K = 2 0 0 0$ and $m = 4$ , there are $1 . 3 2 9 3 \times 1 0 ^ { 9 }$ solutions). Thus, it is necessary to search the solution space efficiently.

According to [19], search methods are organized into two general categories: approximate methods (such as binary segmentation, window sliding, and bottom-up segmentation) and optimal methods (such as the optimal partitioning methods OPT and PELT). The approximate methods are computationally efficient; however, the global minimum of (11) may not be found. Optimal methods yield the exact solution. Based on OPT, Killick R et al. introduced a search method denoted PELT providing exact and efficient computation achieved through a combination of optimal partitioning and pruning [12]. Therefore, PELT will be used as the search method for change-point detection in this paper.

## 2) PELT WITH KNOWN CHANGE NUMBERS

Because PELT is a search method that does not know the number of change-points, the choice of the penalization coefficient $\beta$ has a significant impact on the detection result: if $\beta$ is too small (compared to the optimal value), too many change-points are detected, even including noise. Conversely, only some of the most significant change-points or even no change-points will be detected with a too large $\beta .$ . To lower the probability of the two scenarios above, we need to find an adaptive method to obtain the optimal value of ${ \bf \nabla } \cdot { \bf \nabla } \beta .$ [14] showed that $\beta$ can be obtained when the number of change-points is known.

Equation (11) can generally be described as

$$
J _ { m } + \beta p _ { m } ,\tag{13}
$$

where $\begin{array} { r } { J _ { m } = \sum _ { i = 1 } ^ { m + 1 } [ c ( y _ { \tau _ { i - 1 } + 1 : \tau _ { i } } ) ] } \end{array}$ and $p e n ( m ) = p _ { m }$ (as mentioned above, we suggest using $p _ { m } = m )$ . Thus, the problem of minimizing (11) or (13) can be described as using the solution ${ \hat { \pmb { \tau } } } ( { \boldsymbol { \beta } } )$ to minimize the penalized contrast:

$$
\hat { \pmb { \tau } } ( \beta ) = a r g \operatorname* { m i n } _ { \pmb { \tau } } ( J _ { m } + \beta m ) = \hat { \pmb { \tau } } _ { m ( \beta ) } ,\tag{14}
$$

where

$$
m ( \beta ) = a r g \operatorname* { m i n } _ { m \ge 1 } ( J _ { m } + \beta m ) .\tag{15}
$$

m(β) is the number of change-points in the segmentation that is optimal for solving the penalized optimisation problem of (15) with $\beta$ [18]. In [14], the way $m ( \beta )$ varies with the penalization parameter $\beta$ is given as follows: There exists a sequence $m _ { 1 } = 1 < m _ { 2 } < . .$ . and a sequence $\beta _ { 0 } = \infty >$ $\beta _ { 1 } > . .$ . with

$$
\beta _ { i } = \frac { J _ { m _ { i } } - J _ { m _ { i + 1 } } } { m _ { i } - m _ { i + 1 } } , \quad i \ge 1 ,\tag{16}
$$

such that $m ( \beta ) ~ = ~ m _ { i } , \forall \beta ~ \in ~ ( \beta _ { i } , \beta _ { i - 1 } )$ . In other words, to make the number of change-points equal $m _ { i }$ , we should adjust the value of $\beta$ iteratively until $\beta ~ \in ~ ( \beta _ { i } , \beta _ { i - 1 } )$ and $m ( \beta ) = m _ { i }$ . Finally, $\beta$ can be estimated and used in PELT to obtain at most m change-points.

When knowing the number of changes, the PELT-KCN can be implemented as Algorithm 1.

## 3) CHANGE NUMBER DETECTION

To obtain the number of change-points m before the algorithm above, an algorithm called weighted-envelope normalization (WEN) in [10] is used to obtain the envelope of y<sub>1</sub>:<sub>K</sub> first; then, m can be estimated according to the amplitude variance of the envelope. The specific procedure is given in Algorithm 2.

## IV. SIGNAL RECONSTRUCTION

The positions of the interfered components are determined by change-point detection. We then need to restore the signal degraded by the interference. Here, we use the AR model as the reconstruction method. As Fig. 3 shows, the signal $y _ { 1 : K }$ is divided into three portions, $y _ { F } , y _ { I }$ and ${ \bf y } _ { B }$ , denoting before, during, and after the interference, respectively. The forward restoration is the result of the AR model using time samples in $y _ { F } .$ , and the backward restoration is the result of using y<sub>B</sub>. Finally, We use the results from the two restorations to obtain the final result according to the method mentioned in [11]. As a result, the degraded signal $y _ { I }$ can be reconstructed.

Algorithm 1 PELT With Known Change Number   
(PELT-KCN)   
Input: signal $\{ y _ { t } \} _ { t = 1 } ^ { K }$   
cost function $c ( \cdot )$   
number of change-points m   
type of change to detect ’statistic’   
Output: the change-points recorded in cp   
1: $r e s m a x = c ( y _ { 1 : K } ) ,$   
2: $\begin{array} { r } { r e s m i n = \sum _ { i = 1 } ^ { K } c ( y _ { i } ) , } \end{array}$   
3: $o n e r e s i d u e = c ( y _ { 1 : \tau } ) + c ( y _ { \tau + 1 : K } ) ,$   
4: $\beta = r e s m a x - o n e r e s i d u e$   
5: $( c p , r e s i d u e ) = P E L T ( \{ y _ { t } \} _ { t = 1 } ^ { K } , \beta ,$ statistic)   
6: while length(cp) < m and residue $\geq$ resmin do   
7: $\beta _ { m a x } = \beta$   
8: resmax = residue   
9: $\beta = 0 . 5 \beta$   
10: $( c p , r e s i d u e ) = P E L T ( \{ y _ { t } \} _ { t = 1 } ^ { K } , \beta ,$ statistic)   
11: if length(cp) > m then   
12: $\beta _ { m i n } = \beta$   
13: resmin = residue   
14: end if   
15: end while   
16: while length(cp) > m and residue $\leq$ resmax do   
17: $\beta _ { m i n } = \beta$   
18: $\beta = 2 \beta$   
19: $( c p , r e s i d u e ) = P E L T ( \{ y _ { t } \} _ { t = 1 } ^ { K } , \beta ,$ statistic)   
20: if length(cp) < m then   
21: $\beta _ { m a x } = \beta$   
22: resmax = residue   
23: end if   
24: end while   
25: $\begin{array} { r } { \beta = \frac { \beta _ { m i n } + \beta _ { m a x } } { 2 } } \end{array}$   
26: while $l e n g t h ( c p ) \neq$ m and $\beta _ { m i n } < \beta < \beta _ { m a x }$ do   
27: $( c p , r e s i d u e ) = P E L T ( \{ y _ { t } \} _ { t = 1 } ^ { K } , \beta ,$ statistic)   
28: if length(cp) < m then   
29: ${ c p } _ { m a x } = { c p }$   
30: resmax = residue   
31: $\beta _ { m a x } = \beta$   
32: else   
33: $\beta _ { m i n } = \beta$   
34: end if   
35: $\begin{array} { r } { \beta = \frac { \beta _ { m i n } + \beta _ { m a x } } { 2 } } \end{array}$   
36: end while

The method of restoration consists of four steps, as outlined below.

1. Use $y _ { F }$ and $\Im B$ as references to restore $y _ { I }$ and obtain the restored signals $u ^ { F } [ q ] , ( q ~ = ~ 1 , 2 , \ldots , N _ { I } )$ and $u ^ { B } [ q ] , ( q \ = \ 1 , 2 , \ldots , N _ { I } )$ , respectively, where $N _ { I }$ is the number of samples in $y _ { I }$

2. Calculate the coefficients A, B, and C of the function F (·)

$$
F ( i ) = \frac { B } { i + A } + C ( i > 0 , B < 0 ) ,\tag{17}
$$

Algorithm 2 Changes Number Detection   
Input: signal $\{ y _ { t } \} _ { t = 1 } ^ { K }$   
Output: number of change-points m   
1: $m = 0$   
2: $r = W E N ( \{ y _ { t } \} _ { t = 1 } ^ { K } )$   
//Estimate envelope $\pmb { r } = [ r _ { 1 } , \dots , r _ { K } ]$ by WEN method   
3: $T _ { c } = ( 1 + \alpha ) \operatorname* { m i n } _ { \iota _ { \cdot } } ( r _ { k } ) , 0 < \alpha < 1$   
//calculate the threshold to detect interference, where α   
is a control parameter   
4: for each $k \in [ 1 , K ]$ do   
5: if $r _ { k } \ge T _ { c }$ then   
6: $d _ { k } = 1$   
7: else   
8: $d _ { k } = 0$   
9: end if   
10: end for   
11: $\pmb { d t } = [ d _ { 2 } - d _ { 1 } , d _ { 3 } - d _ { 2 } , \dots , d _ { k } - d _ { k - 1 } ]$   
//calculates differences between adjacent elements of d   
12: for each $k \in [ 1 , K - 1 ]$ do   
13: if $d _ { k } \neq 0$ then   
14: $m = m + 1$   
15: end if   
16: end for   
where A, B, C, and D are   
$A = { \frac { D N _ { I } } { 1 - 2 D } } ,$   
$B = - A N _ { I } - A ^ { 2 } ,$   
$C = - { \frac { B } { A } } ,$   
$D = \frac { N _ { F } } { N _ { F } + N _ { B } }$ (18)   
$( N _ { F }$ and $N _ { F }$ are the numbers of samples in $y _ { F }$ and ${ \tt y } _ { B } ,$   
respectively), and the function $F ( \cdot )$ is designed to satisfy three   
conditions:   
$F ( 0 ) = 0 ,$   
$F ( N _ { I } ) = N _ { I } ,$   
$F ( \frac { N _ { F } } { N _ { F } + N _ { B } } N _ { I } ) = \frac { N _ { I } } { 2 } .$ (19)   
3. Calculate the window coefficient $\omega [ q ] ~ = ~ \nu [ F ( q ) ] .$   
where   
$\nu [ i ] = \frac { 1 } { 2 } ( 1 + \cos ( \pi ( 1 + \frac { i } { N _ { I } } ) ) ) .$ (20)   
4. Reconstruct signal $y _ { I }$ according to   
$\hat { \pmb { y } } _ { I } [ q ] = ( 1 - \omega [ q ] ) \pmb { u } ^ { F } [ q ] + \omega [ q ] \pmb { u } ^ { B } [ q ] ( q = 1 , 2 , \ldots , N _ { I } )$   
(21)

(21)

## V. SIMULATION EVALUATION

## A. MULTI-INTERFERENCE SIMULATION

Simulations were performed under the following conditions, as shown in Fig. 4. Two targets (car B and car C) are located

![](images/ca43079315a32741565e8204ec065000a66756fff56f5a2a134c7c45ed998b0b.jpg)  
FIGURE 3. Steps of signal reconstruction.

![](images/026b4199c4f8375a847d759eaf7ce8333343b2723671eb63b8be76545d1f92fd.jpg)  
FIGURE 4. Simulation scenario.

40 m and 70 m away, respectively, from the ego car (car A), and car B acts as an interferer as well. Car A is equipped with FMCW radar, of which the sweep bandwidth and sweep time are set to 150 MHz and 3.4 ms, respectively. The radar of car B is set to have a 150 MHz sweeping bandwidth and 0.21 ms sweep time. The simulation results are presented in the following pictures, in which target 1 and target 2 represent car B and car C, respectively. The two targets in the distance spectrum are detected by the cell averaging CFAR detector, in which 20 training cells and 2 guard cells in total are used, and the desired false alarm rate is 0.001. The values of the SNR for all the simulations and the experiments are reported given

$$
\begin{array} { c l l } { { S N R = 1 0 l o g _ { 1 0 } ( \displaystyle \frac { R ^ { 2 } ( d i x _ { s } ) } { \sum R ^ { 2 } ( d i x ) - \sum R ^ { 2 } ( d i x _ { s } ) } ) } } \\ { { ( d i x = 1 , \ldots , F N ; d i x _ { s } = d i x _ { 1 } , \ldots , d i x _ { S } ) , } } \end{array}\tag{22}
$$

where dix represents the index of a signal in the distance spectrum, FN is the length of the distance spectrum, $d i x _ { s }$ is the index of the signal of the target in the distance spectrum, S is the number of the targets, R(dix) denotes the peak value of the signal with index dix in the distance spectrum, $\sum R ^ { 2 } ( d i x )$ is the total power of the distance spectrum, and $\sum \overline { { R ^ { 2 } } } ( d i x _ { s } )$ is the total power of all the signals of the targets [20].

## 1) SIMULATION A: A CHIRP WITHOUT INTERFERENCE

Without interference, the beat signal and the distance spectrum of the victim radar equipped on car A are as shown

![](images/a67d0c851d3b809039e765754b5556ba5e9db00964d22f775183d369c0362e65.jpg)  
(a)

![](images/b230d69426e01b81a7fb540f04d20bdbfd814f036527e7ba89b1a928fa0136bd.jpg)  
(b)  
FIGURE 5. Results of Simulation A. (a) and (b) are the beat signal and the distance spectrum of the victim radar equipped on car A, respectively.

TABLE 1. SNR of target 1 in the simulations.
<table><tr><td colspan="2">number of interferers</td><td>0</td><td>1</td><td>2</td></tr><tr><td rowspan="3">SNR(dB)</td><td>no processing</td><td>27.573</td><td>-40.792</td><td>-36.848</td></tr><tr><td>AWEN</td><td></td><td>4.530</td><td>1.641</td></tr><tr><td>PELT-KCN</td><td>一</td><td>27.661</td><td>27.037</td></tr></table>

TABLE 2. SNR of target 2 in simulations.
<table><tr><td colspan="2">number of interferers</td><td>0</td><td>1</td><td>2</td></tr><tr><td rowspan="3">SNR(dB)</td><td>no processing</td><td>21.582</td><td>-24.549</td><td>-27.190</td></tr><tr><td>AWEN</td><td></td><td>-1.496</td><td>-3.990</td></tr><tr><td>PELT-KCN</td><td>-</td><td>21.655</td><td>20.964</td></tr></table>

in Fig. 5(a) and Fig. 5(b), respectively. The two targets are detected by the CFAR algorithm. The SNR of target 1 is 27.573 dB, and the SNR of target 2 is 21.582 dB.

## 2) SIMULATION B: A CHIRP WITH ONE INTERFERER

With one interferer, the beat signal and the distance spectrum of the victim radar equipped on car A are shown in Fig. 6(a) and Fig. 6(b), respectively. Being completely buried in the noise floor, the two targets cannot be detected by the CFAR algorithm. The SNR of target 1 is -40.792 dB, and the SNR of target 2 is -24.549 dB. After applying the AWEN algorithm, the distance spectrum is as shown in Fig. 6(c), in which the SNR of target 1 is 4.530 dB and the SNR of target 2 is -1.496 dB. After applying the proposed method, the distance spectrum is as shown in Fig. 6(d), in which the SNR of target 1 is 27.661 dB and the SNR of target 2 is 21.655 dB.

## 3) SIMULATION C: A CHIRP WITH TWO INTERFERERS

With two interferers, the beat signal and the distance spectrum of the victim radar equipped on car A are as shown in Fig. 7(a) and Fig. 7(b), respectively. Being completely buried in the noise floor, the two targets cannot be detected by the CFAR algorithm. The SNR of target 1 is -36.848 dB, and the SNR of target 2 is -27.190 dB. After applying the AWEN algorithm, the distance spectrum is as shown in Fig. 7(c), in which the SNR of target 1 is 1.641 dB and the SNR of target 2 is -3.990 dB. After applying the proposed method, the distance spectrum is as shown in Fig. 7(d), in which the SNR of target 1 is 27.037 dB. and the SNR of target 2 is 20.964 dB.

![](images/be75962aa5141f3467978761350fa2feeee7e90570e0214175ea55c8bc61095b.jpg)  
(a)

![](images/2ef117f1f396215d6f08b91fca8f35693bbc14fb7d42bee582b826403ecc6c41.jpg)  
(b)

![](images/5bedb9f30a0debf1b3b51ed5b33466800720254f5652ce3ad5a99b5c39c1e428.jpg)

![](images/adf2a58612667d75fa6c62ab7892792af9f9b3f4d685d570d308b75e092b977b.jpg)  
(c)  
(d)  
FIGURE 6. Results of Simulation B. (a) The beat signal with one interferer. (b) The distance spectrum of (a). (c) The distance spectrum after using the AWEN method. (d) The distance spectrum after using the PELT-KCN and AR models.

![](images/eea259ae725f64f97c85d961b6cf22413fe149ee9f1b732567a652e82b777367.jpg)  
(a)

![](images/f6ad5256737c6958700b352b7d545aa44c56063fcc11d492574c5ad89874bd03.jpg)  
(b)

![](images/a117bdc9df106ce5eaf989561c7a0484bd8e8d62c4de6084225e723e7ff844d5.jpg)  
(c)

![](images/507c166a2d4b47bb40f8817785707252558865206609a8e566e4c046078d8442.jpg)  
(d)  
FIGURE 7. Results of Simulation C. (a) The beat signal with two interferers. (b) The distance spectrum of (a). (c) The distance spectrum after using the AWEN method. (d) The distance spectrum after using the PELT-KCN and AR models.

## B. COMPARISON OF DETECTION PROBABILITY

In this simulation, different algorithms are used for detecting target 1 in simulation C, where the SNR of target 1 varies from -80 dB to 0 dB successively. In addition, Monte Carlo simulations are performed 100 times to obtain the detection probability $P _ { d }$ , which is used to evaluate the performance of each algorithm. Fig. 8 shows that the proposed PELT-KCN algorithm stands out, with its lower SNRs being from -80 dB to -26.67 dB, and offers a better performance than the AWEN algorithm as well as processing without the algorithm.

## VI. FIELD EXPERIMENT

The tools adopted for capturing the data of the field experiment are shown in Fig. 9, where the ADC data from Texas Instrument’s 77GHz AWR1642 EVM is captured by the

DCA1000EVM, which enables PC to stream the ADC data over Ethernet. Fig. 10 shows the field experiment scenario, in which one target is located 3.9 m away from the observer (radar 1), and the other two radars (radar 2 and radar 3) are located at approximately 40 centimeters and act as interferers. The main parameters of radar 1 are shown in Table 3. Radar 2 and radar 3 have the same parameters, as shown in Table 4. The target in the distance spectrum is detected by the cell averaging CFAR detector, in which 40 training cells and 2 guard cells in total are used, and the desired false alarm rate is 0.0015.

## A. EXPERIMENT A: A CHIRP WITHOUT INTERFERENCE

Without interference, the beat signal is as shown in Fig. 11(a), and Fig. 11(b) is the distance spectrum. The SNR of the object detected by CFAR is -11.462 dB.

![](images/dc1544e65beab7111e6e3531911bbac65c5cd415b47dc9882e260bf93d739e63.jpg)  
FIGURE 8. Comparison of $\pmb { P _ { d } }$ with various SNRs of target 1 for different algorithms.

![](images/a6f4df77018e6c8706d7d9d09b9ecea9062c2f6c475981b60227a70f317c410e.jpg)  
FIGURE 9. The AWR1642 EVM and the DCA1000EVM.

![](images/35ef2d69495c60a4c7d38f2400af4b1a158dfe2b5b98f53f50e57f5f148388af.jpg)  
FIGURE 10. The field experiment scenario.

## B. EXPERIMENT B: A CHIRP WITH

## ONE INTERFERER

With one interferer, the beat signal is as shown in Fig. 12(a) (the green lines are the output of the proposed PELT-KCN algorithm), and Fig. 12(b) is the distance spectrum. The SNR of the object is -18.604 dB. After applying the AWEN algorithm, the distance spectrum is as shown in Fig. 12(c), in which the SNR of the object is -11.400 dB. After applying the proposed method, the distance spectrum is as shown in Fig. 12(d), in which the SNR of the object is -10.449 dB.

TABLE 3. Parameters of radar 1.
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Sweep bandwidth</td><td>1.0234 GHz</td></tr><tr><td>Chirp duration</td><td>60µs</td></tr><tr><td>Chirp slope</td><td>19.9878M  $\mathbf { \widetilde { \mu } } H z / \mu s$ </td></tr><tr><td>ADC sampling rate</td><td>10 MSa/s</td></tr><tr><td>Center frequency</td><td>77 GHz</td></tr><tr><td>TX Power</td><td>12.5 dBm</td></tr></table>

TABLE 4. Parameters of radar 2 and radar 3.
<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Sweep bandwidth</td><td>4 GHz</td></tr><tr><td>Chirp duration</td><td>57.14µs</td></tr><tr><td>Chirp slope</td><td>70MHz/µs</td></tr><tr><td>ADC sampling rate</td><td>5.209 MSa/s</td></tr><tr><td>Center frequency</td><td>77 GHz</td></tr><tr><td>TX Power</td><td>12.5 dBm</td></tr></table>

![](images/60c65c481e6319ccb3950fbeb414cc83bff3343db062267e689302fb44d17a01.jpg)  
(a)

![](images/d7b11cd1598d8304ce425c77cee863e985d885dd870c51eb2acef907ae09efa0.jpg)  
(b)  
FIGURE 11. Results of Experiment A. (a) and (b) are the beat signal and the distance spectrum of the victim radar, respectively.

## C. EXPERIMENT C: A CHIRP WITH

## TWO INTERFERERS

With two interferers, the beat signal is as shown in Fig. 13(a) (the green lines are the output of the proposed PELT-KCN algorithm), and Fig. 13(b) is the distance spectrum. The SNR of the object is -23.359 dB. After applying the AWEN algorithm, the distance spectrum is as shown in Fig. 13(c), in which the SNR of the object is -13.103 dB. After applying the proposed method, the distance spectrum is as shown in Fig. 13(d), in which the SNR of the object is -11.197 dB.

## D. EXPERIMENT D: A CHIRP WITH

## THREE INTERFERERS

With three interferers, the beat signal is as shown in Fig. 14(a) (the green lines are the output of the proposed PELT-KCN algorithm), and Fig. 14(b) is the distance spectrum. The SNR of the object is -19.908 dB. After applying the AWEN algorithm, the distance spectrum is as shown in Fig. 14(c), in which the SNR of the object is -13.870 dB. After applying the proposed method, the distance spectrum is as shown in Fig. 14(d), in which the SNR of the object is -12.353 dB.

## VII. DISCUSSION

According to the simulations and field experiments, the noise floor significantly increases when interference occurs.

![](images/bebae9faef0fe707b64641b6e7274a8c2d404aa440aef110c62d9c4a7d58a250.jpg)  
(a)

![](images/d04c5b49b1e06978e03a84918b59da761cd33b62b2268bb758e989e76ffe3cae.jpg)  
(b)

![](images/b461a52bdd5f5387d1a63aa22444462e12603c082d607ffe84070cbc11956ee7.jpg)  
(c)

![](images/7147c522cc880f577c0d8d1c6fc3a1fd8acd0c3bdd6be9930be689666a3bea79.jpg)  
(d)  
FIGURE 12. Results of experiment B. (a) The beat signal with one interferer. (b) The distance spectrum of (a). (c) The distance spectrum after using the AWEN method. (d) The distance spectrum after using the PELT-KCN and AR models.

![](images/021174aed8ae7d038d62afa300f60f1096749874e8c0e90d33bbb79b533824ff.jpg)  
(a)

![](images/bf2f5a7da775d523d1f0099ff17b0f11180363d8c8c4a4fd881af1e60396deff.jpg)  
(b)

![](images/e1099d10b87dbabbe53775394519216a194384ff7048a131433fcd0589a5c1b5.jpg)

![](images/fcf80f2fb6a9c048fd3c8d4071fdbb9e51f16ec12b45b82a0e0582a453b47dfa.jpg)  
(c)  
(d)  
FIGURE 13. Results of experiment C. (a) Beat signal with two interferers. (b) The distance spectrum of (a). (c) The distance spectrum after using the AWEN method. (d) The distance spectrum after using the PELT-KCN and AR models.

TABLE 5. SNR of the target in the field experiments.
<table><tr><td colspan="2">number of interferers</td><td>0</td><td>1</td><td>2</td><td>3</td></tr><tr><td rowspan="3">SNR(dB)</td><td>no processing</td><td>-11.462</td><td>-18.604</td><td>-23.359</td><td>-19.908</td></tr><tr><td>AWEN</td><td></td><td>-11.400</td><td>-13.103</td><td>-13.870</td></tr><tr><td>PELT-KCN</td><td></td><td>-10.449</td><td>-11.197</td><td>-12.353</td></tr></table>

This is because interference appears in the form of chirps in the IF signal on the basis of (7) and (9). Thus, small or far away objects with a low power level of reflection may no longer be detectable. After using the AWEN method and the method with the PELT-KCN algorithm, the effect of interference can be mitigated. However, the method with the PELT-KCN algorithm performs better since, compared to the AWEN method, it increased the SNR of the objects by at least 23 dB in simulations and 0.95 dB in field experiments. Moreover, the simulation verifies that the PELT-KCN algorithm can maintain a high detection probability over a wide range of SNRs. In conclusion, our algorithm, combined with a signal restoration method, such as the AR model, is suitable for FMCW radar interference suppression.

![](images/1aca697d1b5162c9e1a2a496cfc3c824ee3234e82700c7e273e36f88ab7959b4.jpg)  
(a)

![](images/cae1169741c47d6ca610521b28fdbefecc04351ca32021d1191463413c881a0f.jpg)  
(b)

![](images/99781c7806892b59e2161e7a9b341d60b2e82116f94b6ff5bf297c0c66113314.jpg)  
(c)

![](images/09765ce6c5f98d1ec9ac6ab093aa38737abdb6a44da105ac5ba262c3c6488ef0.jpg)  
(d)  
FIGURE 14. Results of experiment D. (a) Beat signal with three interferers. (b) The distance spectrum of (a). (c) The distance spectrum after using the AWEN method. (d) The distance spectrum after using the PELT-KCN and AR models.

## VIII. CONCLUSION

In this paper, we have proposed a PELT-KCN algorithm for finding the optimal penalty factor of the PELT algorithm. In this PELT-KCN algorithm, first, we obtain the number of change-points by analyzing the variation of the signal envelope, which is the output of the WEN algorithm. Second, we find the optimal penalty factor based on the known number of change-points. Moreover, we have proposed a method to suppress mutual interference for FMCW radar by using the PELT-KCN algorithm. In this method, we build the signal model showing the change trend of the instantaneous frequency corresponding to the signals transmitted by the victim radar and other radars. Then, based on this signal model, interference suppression is achieved through a combination of the PELT-KCN algorithm and AR model. The results of the simulation and field experiment have verified that the proposed method can decrease the noise floor caused by mutual interference and effectively increase the SNR corresponding to the targets. The proposed algorithm is currently an offline algorithm. To realize real-time interference suppression, we will further improve the efficiency of the algorithm by choosing a more suitable cost function and methods for detecting change-point numbers. In addition, the proposed algorithm will be used for direction-of-arrival (DOA) estimation when interfering signals appear so that the performance of the algorithms for DOA estimation can be improved.

## REFERENCES

[1] A. Eltrass and M. Khalil, ‘‘Automotive radar system for multiple-vehicle detection and tracking in urban environments,’’ IET Intell. Transp. Syst., vol. 12, no. 8, pp. 783–792, Oct. 2018.

[2] S. M. Patole, M. Torlak, D. Wang, and M. Ali, ‘‘Automotive radars: A review of signal processing techniques,’’ IEEE Signal Process. Mag., vol. 34, no. 2, pp. 22–35, Mar. 2017.

[3] M. He, Y. Nian, and Y. Gong, ‘‘Novel signal processing method for vital sign monitoring using FMCW radar,’’ Biomed. Signal Process. Control, vol. 33, pp. 335–345, Mar. 2017.

[4] Y.-S. Son, H.-K. Sung, and S. Heo, ‘‘Automotive frequency modulated continuous wave radar interference reduction using per-vehicle chirp sequences,’’ Sensors, vol. 18, no. 9, p. 2831, Aug. 2018.

[5] M. Goppelt, H.-L. Blöcher, and W. Menzel, ‘‘Automotive radar— Investigation of mutual interference mechanisms,’’ Adv. Radio Sci., vol. 8, pp. 55–60, Sep. 2010.

[6] M. A. Hossain, I. Elshafiey, and A. Al-Sanie, ‘‘Waveform diversity for mutual interference mitigation in automotive radars under realistic traffic environments,’’ Signal, Image Video Process., vol. 13, no. 1, pp. 1–8, 2019.

[7] F. Uysal and S. Sanka, ‘‘Mitigation of automotive radar interference,’’ in Proc. IEEE Radar Conf. (RadarConf), Apr. 2018, pp. 0405–0410.

[8] J. Mun, H. Kim, and J. Lee, ‘‘A deep learning approach for automotive radar interference mitigation,’’ in Proc. IEEE 88th Veh. Technol. Conf. (VTC-Fall), Aug. 2018, pp. 1–5.

[9] J.-T. González-Partida, F. León-Infante, R. Blázquez-García, and M. Burgos-García, ‘‘On the use of low-cost radar networks for collision warning systems aboard dumpers,’’ Sensors, vol. 14, no. 3, pp. 3921–3938, Feb. 2014.

[10] J.-H. Choi, H.-B. Lee, J.-W. Choi, and S.-C. Kim, ‘‘Mutual interference suppression using clipping and weighted-envelope normalization for automotive FMCW radar systems,’’ IEICE Trans. Commun., vol. E99.B, no. 1, pp. 280–287, 2016.

[11] S. Lim, S. Lee, J.-H. Choi, J. Yoon, and S.-C. Kim, ‘‘Mutual interference suppression and signal restoration in automotive FMCW radar systems,’ IEICE Trans. Commun., vol. E102.B, no. 6, pp. 1198–1208, Jun. 2019.

[12] R. Killick, P. Fearnhead, and I. A. Eckley, ‘‘Optimal detection of change points with a linear computational cost,’’ J. Amer. Stat. Assoc., vol. 107, no. 500, pp. 1590–1598, Oct. 2012.

[13] Q. Yan, Z. Sun, Q. Gan, and W.-L. Jin, ‘‘Automatic identification of near stationary traffic states based on the PELT changepoint detection,’’ Transp. Res. B, Methodol., vol. 108, pp. 39–54, Feb. 2018.

[14] M. Lavielle, ‘‘Using penalized contrasts for the change-point problem,’ Signal Process., vol. 85, no. 8, pp. 1501–1510, Aug. 2005.

[15] M. Goppelt, H.-L. Blöcher, and W. Menzel, ‘‘Analytical investigation of mutual interference between automotive fmcw radar sensors,’’ in Proc. German Microw. Conf., Mar. 2011, pp. 1–4.

[16] G. M. Brooker, ‘‘Mutual interference of millimeter-wave radar systems,’’ IEEE Trans. Electromagn. Compat., vol. 49, no. 1, pp. 170–181, Feb. 2007.

[17] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, ‘‘Threshold-free interference cancellation method for automotive FMCW radar systems,’’ in Proc. IEEE Int. Symp. Circuits Syst. (ISCAS), May 2018, pp. 1–4.

[18] K. Haynes, I. A. Eckley, and P. Fearnhead, ‘‘Computationally efficient changepoint detection for a range of penalties,’’ J. Comput. Graph. Statist., vol. 26, no. 1, pp. 134–143, Feb. 2017.

[19] C. Truong, L. Oudre, and N. Vayatis, ‘‘Selective review of offline change point detection methods,’’ 2018, arXiv:1801.00718. [Online]. Available: http://arxiv.org/abs/1801.00718

[20] S. Kim, B.-S. Kim, Y. Jin, and J. Lee, ‘‘Extrapolation-RELAX estimator based on spectrum partitioning for DOA estimation of FMCW radar,’ IEEE Access, vol. 7, pp. 98771–98780, 2019.

![](images/be58209340239cb7066a71606d5b33b5dc09d36abab9f043a35b53adb2c69812.jpg)

ZHENYU LIU received the B.S. and M.S. degrees in electronic circuits and systems from Xidian University, Xi’an, China, in 1999 and 2002, respectively, and the Ph.D. degree in signal and information processing from the South China Uni versity of Technology, Guangzhou, China, in 2008. He was an Electronic Engineer in radio communication with Guangzhou Haige Communications Group, from 2002 to 2005. He held a postdoctoral position in security of 3G/4G communication at

the South China University of Technology, from 2008 to 2011. From 2014 to 2015, he was a Visiting Scholar with the School of Electrical and Information Engineering, The University of Sydney, Sydney, NSW, Australia. He is currently an Associate Professor and the Dean of the Department of Communication Engineering, School of Information Engineering and Technology, Guangdong University of Technology, Guangzhou. His research interests include radar signal processing, wireless communication, the Internet of Things, and network security.

![](images/b9e2ef1a769503fcb708f6a4dc730f719e20460178b3ddc72ae9887294c47817.jpg)

WEI LU received the B.S. degree in measurement and control technology and instrumentation from Yangtze University, Jingzhou, China, in 2017. He is currently pursuing the M.S. degree in electronics and communication engineering with the Guangdong University of Technology, Guangzhou, China. His current research interest includes radar signal processing techniques, particularly clutter and interference suppression.

![](images/e49d57f1b3851cbae91c52283bddf99da1931c8fb518e6958d849d45ea98b90b.jpg)

JIAYAN WU is currently pursuing the M.S. degree in information and communication engineering with the Guangdong University of Technology. His main research interests include radar signal processing, particularly clutter and interference suppression, and target detection and tracking.

![](images/ebe8e11bfccac8b9a3c7ef2de362fe25059cb1d3c1746c8cb86dbaa60ee83432.jpg)

SIYUAN YANG received the B.S. degree in electronic information engineering from Guangdong Ocean University, Guangdong, China, in 2018. He is currently pursuing the master’s degree with the Guangdong University of Technology, Guangdong. His research interest includes radar signal processing techniques, particularly interference suppression and change-point detection.

![](images/9a12a4946da9112ea49fbab31ca494bd41b8227bad84c0cd34fc737473647732.jpg)

GUANGPING LI received the B.S. degree in thermal engineering and the M.S. degree in communication and information systems from Hunan University, in 2002 and 2005, respectively, and the Ph.D. degree in communication and information systems from Sun Yat-sen University, in 2009. He was a Visiting Research Student with the Department of Electrical and Computer Engineering, Queen’s University, Canada, from 2007 to 2009. Since July 2009, he has been with the Fac-

ulty of Information Engineering, Guangdong University of Technology, China, where he is currently an Associate Professor. His current research interests include massive MIMO systems, millimeter-wave radar systems, and wireless energy transfer.