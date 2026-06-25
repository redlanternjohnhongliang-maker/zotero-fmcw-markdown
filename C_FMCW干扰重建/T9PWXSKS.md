# A Deep Learning Approach for Automotive Radar Interference Mitigation

Jiwoo Mun, Heasung Kim, and Jungwoo Lee

Department of Electrical and Computer Engineering, Seoul National University, Seoul, Korea E-mail: {jwmun, heasung1130}@cml.snu.ac.kr, junglee@snu.ac.kr

Abstract—In automotive systems, a radar is a key component of autonomous driving. Using transmit and reflected radar signal by a target, we can capture the target range and velocity. However, when interference signals exist, noise floor increases and it severely affects the detectability of target objects. For these reasons, previous studies have been proposed to cancel interference or reconstruct original signals. However, the conventional signal processing methods for canceling the interference or reconstructing the transmit signals are difficult tasks, and also have many restrictions. In this work, we propose a novel approach to mitigate interference using deep learning. The proposed method provides high performance in various interference conditions and has low processing time. Moreover, we show that our proposed method achieves better performance compared to existing signal processing methods.

Index Terms—autonomous driving, automotive, radar, interference, mitigation, deep learning

## I. INTRODUCTION

Radars mounted on advanced vehicles, such as autonomous vehicles, require a variety of functions, including detection of multi-target and long-range sensing. These functions must be performed accurately ensure user safety and solve collision problem between vehicles. Recent popular radar technologies include Frequency Modulated Continuous Wave (FMCW) or Chirp Sequence (CS) radars [1]–[3]. However, it is difficult to perform the above functions with interference [4], [5].

Several techniques have been proposed to solve the problems related to interference [6]–[10]. [6] used the characteristics of the interference region in the time domain to remove the interference. [8] proposed a method of estimating the amplitude and frequency of the interference signal to recover the original signal as well as the interference elimination with high computational complexity. The paper [10] proposed an algorithm that requires a small computational complexity and showed that it detects targets within small distances without defining an adaptive threshold. The effect of interference still remains, however, because the target is not well detected when the interference signal source is closer to the radar than the target.

To the best of our knowledge, we are the first to use a deep learning method to mitigate interference in time domain. Recently, the development of deep learning has been remarkable, and in particular, it has made significant achievements in image and language processing. Besides, these deep learning techniques have shown outstanding results in the field of signals, and [11] and [12] showed that deep learning can be useful in signal processing. Especially we apply the Recurrent Neural Network (RNN) model with Gated Recurrent Unit (GRU) [13], which is known to be suitable for processing sequence data, to remove interference and reconstruct transmit signal simultaneously. We can reconstruct transmit signal even in the presence of various interference signals, and the reconstructed signal can be used to detect objects through Fast Fourier Transform (FFT). In particular, through the learned network, signal processing can be done only with the matrix calculation, not with any iteration structure. Also, the algorithm does not require any adaptive threshold. We show that our algorithm outperforms existing algorithms in experiments where noise and interference coexist.

![](images/673075bb5e3af10f0b3bb060bb72cda9e6c0138e6320f8eca812833d3e8b434d.jpg)  
Fig. 1: CS waveform of transmit and received signal

The rest of this paper is organized as follows. In Section II, we introduce the system model considered in the paper. In Section III, we show the deep learning model for our proposed algorithm. In Section IV, we show the simulation results for the proposed scheme. Lastly, in Section V, we conclude this paper.

## II. SYSTEM MODEL

## A. CS Radar System

One of the main radar waveforms is the CS waveform [1], [3] as shown in Fig. 1. If the transmit signal consists of k linear frequency chirps, frequency and phase of the transmit signal are as follows.

$$
\begin{array} { l } { f ( t ) = f _ { B } + \alpha ( t - k T _ { c h i r p } ) } \\ { \displaystyle { \phi ( t ) = 2 \pi \int _ { 0 } ^ { t } f ( t ) d t } } \\ { \displaystyle { \quad = 2 \pi ( f _ { B } t + \frac { 1 } { 2 } \alpha t ^ { 2 } - \alpha k T _ { c h i r p } t ) , } } \end{array}\tag{1}
$$

![](images/d879d7d85b9a1eefff4fea4d618471c177324fbb456bb908c3a9ee69336beb00.jpg)  
Fig. 2: Beat frequency

where $B _ { S W }$ is sweep bandwidth, $T _ { c h i r p }$ is chirp duration, $\alpha = B _ { S W } / T _ { c h i r p }$ is slope of the CS waveform, and $f _ { B }$ is carrier frequency of the transmit signal. The beat frequency is the difference between the transmit frequency and the received frequency. The beat frequency $f _ { B } ( t )$ is represented as Fig. 2. A Low Pass Filter (LPF) can remove signals with higher absolute frequency value. So the remaining beat phase through the LPF can be represented as

$$
\begin{array} { r l } & { \phi _ { B } ( t ) = \phi ( t ) - \phi ( t - \tau ) } \\ & { \qquad = 2 \pi f _ { B } \tau - \pi \alpha ( \tau ^ { 2 } - 2 \tau t ) } \\ & { \qquad \mathrm { i f ~ } \tau < t < T _ { c h i r p } . } \end{array}\tag{2}
$$

We denote target range, target velocity and speed of light as $R ,$ v, c, respectively, and the propagation delay can be represented as τ . Substituting $\begin{array} { r } { \tau \ = \ \frac { 2 ^ { \bullet } ( R + v t ) } { c } } \end{array}$ and $t ~ = ~ k T _ { c h i r p } + t _ { k }$ into equation (2) (if t is present in k-th chirp), (2) can be approximated

$$
\begin{array} { l } { \displaystyle { \phi _ { B } ( t ) = 2 \pi f _ { B } \left( \frac { 2 R } { c } + \frac { 2 v t } { c } \right) } } \\ { \displaystyle { ~ - \pi \alpha \left( \left( \frac { 2 R } { c } + \frac { 2 v t } { c } \right) ^ { 2 } - 2 \left( \frac { 2 R } { c } + \frac { 2 v t } { c } \right) t \right) } } \\ { \displaystyle { ~ \approx 2 \pi \left( \frac { 2 R } { c } f _ { B } + \frac { 2 v } { c } f _ { B } k T _ { c h i r p } \right. } } \\ { \displaystyle { ~ \left. + \left( \frac { 2 \alpha R } { c } + \frac { 2 v } { c } f _ { B } \right) t _ { k } \right) . } } \end{array}\tag{3}
$$

Applying sampling as $t ~ = ~ n T _ { s }$ , phase of the beat signal $\phi _ { B } [ n , k ]$ is written as

$$
\begin{array} { l } { \displaystyle \phi _ { B } [ n , k ] = 2 \pi \left( \frac { 2 R } { c } f _ { B } + \frac { 2 v } { c } f _ { B } k T _ { c h i r p } \right. } \\ { \displaystyle \left. + \left( \frac { 2 \alpha R } { c } + \frac { 2 v } { c } f _ { B } \right) n T _ { s } \right) . } \end{array}\tag{4}
$$

Using two dimensional Fast Fourier Transform (FFT), we can obtain following two values $f _ { R }$ and $f _ { D }$

$$
\begin{array} { l } { f _ { R } = \displaystyle \frac { 2 \alpha R } { c } } \\ { f _ { D } = \displaystyle \frac { 2 v } { c } f _ { B } T _ { c h i r p } . } \end{array}\tag{5}
$$

Range R and velocity v can be obtain by $f _ { R }$ and $f _ { D }$ .

![](images/cb493b0218e0aaa7b19de5b0d0ca74d3ff4d7af2b55e1515f90ccc27062421ee.jpg)  
Fig. 3: Interrupted transmit signal, interference occurs in a.

![](images/5e2e38d39c13bb4d5cc8574414d2055ca88279052b4b22eacfa42eddd63f6b3a.jpg)  
Fig. 4: Interrupted beat signal, interference occurs around the 0 to 80 samples.

## B. Interrupted Radar Signal

The equations in the previous subsection are derived in an ideal situation without interference. However, there will be a large error in distance and velocity estimation if interference occurs. In a typical driving situation, we usually encounter CS waveform signals, which have different slopes with the signal being sent, and interference situation would occur as shown in Fig. 3. Since the beat frequency passes through the low pass filter, the interference occurs in the section a only, not in the whole section. Fig. 4 shows that a large distortion occurs around 0 to 80 time samples, unlike the original beat signal. Conventionally, the interference is removed or the original beat signal is restored by using the characteristics of the timedomain beat signal. However, if noise and interference exist, the cancellation of interference and the restoration of original beat signal are difficult with a traditional method.

## III. INTERFERENCE MITIGATION USING DEEP LEARNING

In this section, we propose a deep neural network model which can be used for multi-interference mitigation without relying on adaptive threshold.

![](images/1a6fddc04b183e6ff004d917d02880b32f95218c14024e2e59933ef49c8dc13c.jpg)  
Fig. 5: Proposed deep learning model

## A. Deep Learning Model

As shown in previous studies [14], RNN is known to be suitable for sequence data processing. Since the raw data before preprocessing is consecutive time samples, we apply RNN structure for interference cancellation and restoration in our model. Following equations represents the vanilla RNN elements.

$$
\begin{array} { r c l } { } & { } & { { h _ { t } } = f _ { W } ( h _ { t - 1 } , x _ { t } ) } \\ { } & { } & { { } = t a n h ( W _ { h h } { h _ { t - 1 } } + W _ { x h } { x _ { t } } ) } \\ { } & { } & { { y _ { t } } = W _ { h y } { h _ { t } } . } \end{array}\tag{6}
$$

$x _ { t }$ is the input vector, $h _ { t }$ is the hidden state of the RNN network and $y _ { t }$ is the output vector. $W _ { h h } \mathrm { ~ \tiny ~ , ~ } W _ { x h }$ and $W _ { h y }$ are weight matrices of the hidden state to another hidden state, the input vector to the hidden state and the hidden state to the output vector, respectively. By using RNN, the network can learn the relation of consecutive samples. The input sequence may consist of hundreds of time samples. It may cause long-term dependency problem in RNN [15]. So we use a GRU cell to solve this problem in RNN. GRU has the same time series structure as RNN, but the contents of the cell are different. In the multi-layer GRU layer, each layer has a bidirectional structure, rather than one direction of the signal [16]. In addition, several GRU layers were piled up to learn various interference cases. The residual network [17] is added between layers for better propagation of gradient flow. The residual connection is written as

$$
X ^ { l + 1 } = X ^ { l } + G R U ( X ^ { l } ) , ( l = 1 , 2 , 3 , . . . , L - 1 ) ,\tag{7}
$$

where $X ^ { l }$ is l-th layer input vector of GRU cells, and $G R U ( X ^ { l } )$ is l-th layer output vector of GRU cells. When the total time step is N and the hidden state size is H, the output value of GRU network is $X ^ { L } \in \mathbb { R } ^ { H \times N }$ . If we denote $\boldsymbol { x } _ { i } ^ { L } \in \mathbb { R } ^ { H }$ as the ith column vector of $X ^ { L } , X ^ { L }$ can be represented as $[ x _ { 1 } ^ { L } , x _ { 2 } ^ { L } , . . . , x _ { N } ^ { L } ] .$ . To obtain the output dimension identical to the label dimension, we perform average pooling on $X ^ { L }$ . The average pooling output $\bar { Y } \in \mathbb { R } ^ { N }$ is written as

$$
Y = [ a v e r a g e ( x _ { 1 } ^ { L } ) , a v e r a g e ( x _ { 2 } ^ { L } ) , . . . , a v e r a g e ( x _ { N } ^ { L } ) ] .\tag{8}
$$

To regularize the network, we applied drop out in each GRU Cells [18]. The proposed RNN model is shown in Fig. 5.

## B. Optimizing Model

The inputs is time-sampled interference beat signal, which is represented as $X ^ { 0 } = X = [ x _ { 1 } , x _ { 2 } , . . . , x _ { N } ]$ , where $x _ { i } \in \mathbb { R }$ is amplitude of beat signal $( i = 1 , . . . , N )$ . Each input X is normalized and satisfies the following equation.

$$
\sum _ { i = 1 } ^ { N } x _ { i } ^ { 2 } = 1 .\tag{9}
$$

The output $Y$ is represented as $Y = [ y _ { 1 } , y _ { 2 } , . . . , y _ { N } ]$ , which has the same length as $X , \hat { Y } = [ \hat { y _ { 1 } } , \hat { y _ { 2 } } , . . . , \hat { y _ { N } } ]$ is a beat signal with the same target condition as X but without interference. We called $\hat { Y }$ as label. In order to minimize the difference between the two vectors $Y$ and $\hat { Y } ,$ the loss L is defined as

$$
L = \sum _ { i = 1 } ^ { N } ( \hat { y _ { i } } - y _ { i } ) ^ { 2 } .\tag{10}
$$

The loss L can be minimized by gradient descent. We use a gradient descent algorithm, Adam [19]. As the training progresses, we get output $Y$ which is similar to label $\hat { Y } .$ . We can then use this value Y to detect target range and velocity.

## IV. SIMULATION RESULTS

In this section, we introduce radar simulator parameters and deep learning model parameters. The proposed deep learning model is also compared with existing algorithms.

TABLE I: Radar simulator random parameters
<table><tr><td>Parameter</td><td>Min</td><td>Max</td></tr><tr><td>Center frequency</td><td>76GHz</td><td>78GHZ</td></tr><tr><td>Distance</td><td>1m</td><td>130m</td></tr><tr><td>Velocity</td><td>0km/h</td><td>50km/h</td></tr><tr><td>Sweep bandwidth</td><td>100MHz</td><td>200MHz</td></tr><tr><td>Chirp duration</td><td>20us</td><td>40us</td></tr><tr><td>Target number</td><td>1</td><td>2</td></tr><tr><td>Interference number</td><td>1</td><td>4</td></tr></table>

TABLE II: Deep learning hyperparameter
<table><tr><td>Hyperparameter</td><td>Value</td></tr><tr><td>Batch size</td><td>128</td></tr><tr><td>Learning rate</td><td>1e-3</td></tr><tr><td>Hidden layer size</td><td>100</td></tr><tr><td>Number of data</td><td>150000</td></tr><tr><td>Number of layer</td><td>3</td></tr><tr><td>Drop out rate</td><td>0.3</td></tr><tr><td>Optimizer</td><td>Adam</td></tr></table>

We have assumed a situation with multi-target, multiinterference, and Gaussian noise in order to reflect the practical situation. We use a randomly generated 150,000 time sampled input sequence (with no interference) and 150,000 label sequence (no interference). The range of random parameters for training is shown in Table I. The transmit signal is the CS wave mentioned in Section II and the interference waveform is the FMCW wave signal with different chirp slope (includes CS waveform, triangle sweep FMCW). The total number of chirps was 75 in both the desired and the interfering signals. The model proposed in Section III is used and the hyperparameter used in the model is shown in Table II. The deep learning model input and label are beat signals corresponding to one chirp of the transmit signal. To apply RNN, the input and label length must be constant. However, the number of samples of one chirp can vary depending on the sampling period of the signal. So we limit the maximum length of the input and label to 416 and cut the remaining part if the actual length is longer than that, and do zero-padding if it is smaller. In order to solve the exploding gradients problem in the GRU structure, the gradient clipping method is used [20].

We analyzed the interference mitigation performance of the proposed method. The results are shown in Fig. 6. We use

![](images/d167ea3b0fec87cc2631d58b4f8ab5a238f0c738c5573d7ce35b7db032dc4cc2.jpg)  
(a) Label

![](images/1b4c48925d4277a8d0f8bbbf9a8009f1a78b360b4392ea2375fbe00dad41be6d.jpg)  
(b) Input

![](images/251776d497db938c9c6311d2f2c38f76c6103b103439213c5a2feb938e24d97e.jpg)  
(c) Output

![](images/af948ed269eef488b940dec70f8542ce83483b4b4abc42c0920200040a35dc23.jpg)  
(d) FFT label

![](images/3e219c28cb97730ebd94a47c511c4c3dd0310743778001b8b821a88adc7bf0f3.jpg)  
(e) FFT input

![](images/2f7f089a796e22cfed4d2087a86653f7b27dca21f3e6d132d7cf2ccaeb9b66a1.jpg)  
(f) FFT output  
Fig. 6: Result of deep learning model. (a) to (c) is beat signal, (d) to (f) is FFT result of (a) to (c) signals respectively.

Fig. 6(a) as deep learning label (not interfered), Fig. 6(b) as deep learning input (interfered), and the deep learning output is Fig. 6(c). We can see that the proposed deep learning algorithm finds out where the interference is. Under the considered situation, the reconstruction of the original signal is not perfect. However, we can see that the result of FFT in Fig. 6(f) finds the object more clearly than the interfered input Fig. 6(e). To compare result with other methods, we use the average signal to remaining interference noise ratio (SRINR) [10]. The SRINR result is in Table III. Method I is time domain thresholding (TDT) method used in [6]. Method II did not use an adaptive threshold, which was proposed in [10]. The simulation SRINR is average of 50 random scenarios SRINR. Our proposed deep learning algorithm outperforms other methods. Especially, even in situations where the interference signal sources are close and the targets are too far away, our proposed method finds the target properly as shown in Fig. 7.

TABLE III: Simulation results
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Method I</td><td rowspan=1 colspan=1>Method II</td><td rowspan=1 colspan=1>Proposed</td></tr><tr><td rowspan=1 colspan=1>SRINR</td><td rowspan=1 colspan=1>23.369</td><td rowspan=1 colspan=1>22.665</td><td rowspan=1 colspan=1>26.091</td></tr></table>

![](images/55deaf9a0e8d638a1580a88b6f3e28c375fdacb6400a9924bd6978735495da09.jpg)  
(a) Proposed

![](images/9a71845027003ce0817b8abdc1f8b02aae303bd075c40108dfed73ff1d553c2d.jpg)  
(b) Method I

![](images/7de8dae925df7f643806204c10bc8ee4cbc96f2a16d6ecf301ea5aa2d8ffc5e3.jpg)  
(c) Method II

![](images/006337677152a4b96be5c366d00b83e11740c8d1d8678cd03ce5581d0e966b3d.jpg)  
(d) No processing  
Fig. 7: Simulated power levels with respect to range. Two targets exist in range 100m, 120m. Four interferences exist in range 40m, 50m, 60m, and 70m. Red circles are detected targets.

## V. CONCLUSION

In this paper, we proposed a novel approach to mitigate interference in CS radar system. We used a deep learning approach to mitigate interference. Our method shows better performance compared to other signal processing methods. Our method also shows good performance even when the target is far away. It is believed this method can be applied not only to CS waveforms but also to most situations where frequency changes linearly. This is because interference occurs at the point where the transmit signal crosses the interference signal. The interference patterns of linear frequency signals are similar. Experiments with other waveforms are left as future work.

## VI. ACKNOWLEDGEMENT

This work is in part supported by Basic Science Research Program (NRF-2017R1A2B2007102) through NRF funded by MSIP, Technology Innovation Program (10051928) funded by MOTIE, Bio-Mimetic Robot Research Center funded by DAPA (UD130070ID), INMAC, and BK21-plus.

## REFERENCES

[1] M. Kronauge and H. Rohling, “New chirp sequence radar waveform,” IEEE Transactions on Aerospace and Electronic Systems, vol. 50, no. 4, pp. 2870–2877, 2014.

[2] V. Winkler, “Range doppler detection for automotive fmcw radars,” in Microwave Conference, 2007. European. IEEE, 2007, pp. 1445–1448.

[3] A. G. Stove, “Linear fmcw radar techniques,” in IEE Proceedings F (Radar and Signal Processing), vol. 139, no. 5. IET, 1992, pp. 343– 350.

[4] G. M. Brooker, “Mutual interference of millimeter-wave radar systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, 2007.

[5] M. Goppelt, H.-L. Blocher, and W. Menzel, “Analytical investigation¨ of mutual interference between automotive fmcw radar sensors,” in Microwave Conference (GeMIC), 2011 German. IEEE, 2011, pp. 1–4.

[6] Y. Watanabe and K. Natsume, “Interference determination method and fmcw radar using the same,” Mar. 6 2007, uS Patent 7,187,321.

[7] M. Kunert, “The eu project mosarim: A general overview of project objectives and conducted work,” in Radar Conference (EuRAD), 2012 9th European. IEEE, 2012, pp. 1–5.

[8] J. Bechter and C. Waldschmidt, “Automotive radar interference mitigation by reconstruction and cancellation of interference component,” in Microwaves for Intelligent Mobility (ICMIM), 2015 IEEE MTT-S International Conference on. IEEE, 2015, pp. 1–4.

[9] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A method for interference cancellation in automotive radar,” in Microwaves for Intelligent Mobility (ICMIM), 2015 IEEE MTT-S International Conference on. IEEE, 2015, pp. 1–4.

[10] M. Wagner, F. Sulejmani, A. Melzer, P. Meissner, and M. Huemer, “Threshold-free interference cancellation method for automotive fmcw radar systems,” in Circuits and Systems (ISCAS), 2018 IEEE International Symposium on. IEEE, 2018, pp. 1–4.

[11] S. Yao, S. Hu, Y. Zhao, A. Zhang, and T. Abdelzaher, “Deepsense: A unified deep learning framework for time-series mobile sensing data processing,” in Proceedings of the 26th International Conference on World Wide Web. International World Wide Web Conferences Steering Committee, 2017, pp. 351–360.

[12] D. Yu and L. Deng, “Deep learning and its applications to signal and information processing [exploratory dsp],” IEEE Signal Processing Magazine, vol. 28, no. 1, pp. 145–154, 2011.

[13] J. Chung, C. Gulcehre, K. Cho, and Y. Bengio, “Empirical evaluation of gated recurrent neural networks on sequence modeling,” arXiv preprint arXiv:1412.3555, 2014.

[14] Z. C. Lipton, J. Berkowitz, and C. Elkan, “A critical review of recurrent neural networks for sequence learning,” arXiv preprint arXiv:1506.00019, 2015.

[15] Y. Bengio, P. Simard, and P. Frasconi, “Learning long-term dependencies with gradient descent is difficult,” IEEE transactions on neural networks, vol. 5, no. 2, pp. 157–166, 1994.

[16] M. Schuster and K. K. Paliwal, “Bidirectional recurrent neural networks,” IEEE Transactions on Signal Processing, vol. 45, no. 11, pp. 2673–2681, 1997.

[17] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.

[18] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, “Dropout: A simple way to prevent neural networks from overfitting,” The Journal of Machine Learning Research, vol. 15, no. 1, pp. 1929–1958, 2014.

[19] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” arXiv preprint arXiv:1412.6980, 2014.

[20] R. Pascanu, T. Mikolov, and Y. Bengio, “On the difficulty of training recurrent neural networks,” in International Conference on Machine Learning, 2013, pp. 1310–1318.