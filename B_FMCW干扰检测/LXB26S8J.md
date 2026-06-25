# Threshold-Free Interference Cancellation Method for Automotive FMCW Radar Systems

Matthias Wagner<sup>1</sup>, Fisnik Sulejmani<sup>1</sup>, Alexander Melzer<sup>2</sup>, Paul Meissner<sup>2</sup> and Mario Huemer<sup>1</sup> <sup>1</sup>Institute of Signal Processing, Johannes Kepler University Linz <sup>2</sup>Infineon Technologies Austria AG, Graz

Abstract—Radar systems are key components for today’s advanced driver assistance systems such as adaptive cruise control or emergency brake assistants. Along with the rising utilization of radars in modern cars, the issue of interference amongst themselves arises. It has been shown in previous work that interference between different frequency modulated continuous wave (FMCW) radar systems leads to an increased noise floor. This may severely impact the detectability of objects, especially those with a small radar cross section like pedestrians. In this work we propose a novel concept to mitigate interference in FMCW radar transceivers using digital signal processing. The actual interference cancellation is carried out in frequency domain taking into account a sequence of FMCW chirps. Therewith noise suppression is performed, the interference is cancelled, and the object information is retained in the radar image. In contrast to existing interference cancellation concepts, no threshold needs to be chosen in advance. We prove our method with simulation results, and compare it to existing work.

## I. INTRODUCTION

In recent years the utilization of radar technology in automotive applications has significantly increased. Especially for autonomous driving features it is of utmost importance to accurately detect the position and velocity of other traffic participants. Still, with more and more cars equipped with radars, the issue of interference arises [1]. Interference may significantly influence the radar measurements, specifically since it may cause severe sensitivity degradations [2].

To overcome the issue of interference, various concepts have been studied [3]. Firstly, different transmit signal schemes were investigated, including polarization and modulation schemes [4]. Secondly, changing the frequencies and bandwidths in an adaptive manner once an interferer is detected was studied. Thirdly, digital signal processing techniques were employed to suppress the interference signal in the receiver. An interesting interference cancellation technique using digital signal processing techniques is proposed in [5,6]. The authors claim to detect and cancel interference signals from patterns within the samples of the intermediate frequency (IF) signal among several frequency modulated continuous wave (FMCW) ramps. Yet, not all of the measured radar signals can be used for object detection.

Two other methods employing digital signal processing techniques for interference cancellation are time domain thresholding (TDT) and frequency domain thresholding (FDT) [7]. Both methods require a threshold to be found (adaptively) in order to distinguish between object reflections and the interfering signal. Since radar signals often exhibit a large dynamic range, finding the optimal threshold is difficult in real-world scenarios. Also, the interfered ramps are ignored completely in FDT for further processing. Differently, TDT only ignores the actually interfered signal samples.

In this paper we propose a low-complexity method for interference cancellation that works within the standard FMCW signal processing flow. In particular, a non-linear filtering operation (e.g. the minimum) of the magnitudes of the fast Fourier transform (FFT) bins among several chirps is performed. Thereby the noise is suppressed, and the interference is cancelled. Simulations prove that the proposed concept works for arbitrary and random interference patterns. We highlight that for the herein proposed algorithm no threshold is required, nor are any samples disregarded.

## II. SIGNAL MODEL

The system model used throughout this work is depicted in Fig. 1. The radar transmit signal, which is generated e.g. with a phase locked loop (PLL), is most commonly a linear FMCW signal (linear chirp), often also referred to as frequency ramp. Evaluating this transmit signal for $t \in [ 0 , T ]$ , with the chirp duration T , yields

$$
s ( t ) = A \cos \left( 2 \pi f _ { 0 } t + \pi k t ^ { 2 } + \Phi \right) ,\tag{1}
$$

where A is the output amplitude, $f _ { 0 }$ is the chirp start frequency, k is the slope of the chirp and Φ is a constant initial phase.

The received signal $r _ { T } ( t )$ from various object reflections is modelled as the sum of scaled and delayed versions of the transmit signal s(t). Specifically, we have

$$
r _ { T } ( t ) = \sum _ { i = 0 } ^ { N _ { T } - 1 } A _ { T } ^ { ( i ) } s \left( t - \tau _ { T } ^ { ( i ) } \right) ,\tag{2}
$$

where $N _ { T }$ represents the number of objects, $A _ { T } ^ { ( i ) }$ is the attenuation of the transmit signals and $\tau _ { T } ^ { ( i ) }$ models the roundtrip delay time of the i-th object reflection, respectively.

Now, assume that $r _ { T } ( t )$ is interspersed by interference, as is indicated in Fig. 1. The individual interference signals all originate from different frequency generators. Thus, the overall interference signal is written as

$$
\begin{array} { c } { { \displaystyle r _ { I } ( t ) = \sum _ { i = 0 } ^ { N _ { I } - 1 } A _ { I } ^ { ( i ) } \cos \left( 2 \pi f _ { I } ^ { ( i ) } \left( t - \tau _ { I } ^ { ( i ) } \right) \right. } } \\ { { \left. + \pi k _ { I } ^ { ( i ) } \left( t - \tau _ { I } ^ { ( i ) } \right) ^ { 2 } + \Phi _ { I } ^ { ( i ) } \right) , } } \end{array}\tag{3}
$$

![](images/04a77286932cfa962cfeaa1f3391f4e268f3c89968c3f54fb4ae1689ff0d185a.jpg)  
Fig. 1. System model of the FMCW radar transceiver for multiple object reflections and interferers.

where $N _ { I }$ represents the number of interferers. Further, $A _ { I } ^ { ( i ) }$ determines the amplitudes, $f _ { I } ^ { ( i ) }$ are the chirp start frequencies, $k _ { I } ^ { ( i ) }$ are the chirp slopes, and $\Phi _ { I } ( i )$ are constant initial phase terms of the individual $N _ { I }$ interference signals. It is important to note that the own transmit signal and that of the interferers are not synchronized (this asynchronicity is regarded with the delays $\tau _ { I } ^ { \left( i \right) }$ in our signal model). Thus, we consider the parameters of the interference signals in (3) to vary randomly with respect to their influence on the wanted signal in (2).

According to Fig. 1, the received signal r(t) consists of the sum of the reflected signals from the objects and the interference signal, i.e. $r ( t ) = r _ { T } ( t ) + r _ { I } ( t )$ . Further analog signal processing of $r ( t )$ includes multiplying the transmit and received signal, and subsequently filtering the product with a lowpass filter (LPF) with impulse response $h ( t )$ to remove the image signal. The resulting IF signal is

$$
\begin{array} { r l } & { y ( t ) = \left[ s ( t ) \left( r _ { T } ( t ) + r _ { I } ( t ) \right) \right] * h ( t ) } \\ & { \qquad = \underbrace { \left[ s ( t ) r _ { T } ( t ) \right] * h ( t ) } _ { y _ { T } ( t ) } + \underbrace { \left[ s ( t ) r _ { I } ( t ) \right] * h ( t ) } _ { y _ { I } ( t ) } , } \end{array}\tag{4}
$$

where ∗ denotes the convolution operator. In $( 4 ) , y _ { T } ( t )$ and $y _ { I } ( t )$ denote the IF signal contributions of the object reflections and the interference, respectively.

Utilizing (3) it is easy to show that, by assuming the LPF to be ideal, i.e. having unit magnitude response in passband and perfect suppression of the image signal, the i-th interferer contribution $y _ { I } ^ { ( i ) } ( t )$ evaluates to

$$
\begin{array} { r } { y _ { I } ^ { ( i ) } ( t ) = \displaystyle \frac { 1 } { 2 } A A _ { I } ^ { ( i ) } \cos \left( 2 \pi \left( f _ { 0 } - f _ { I } ^ { ( i ) } \right) t + \pi \Big ( k - k _ { I } ^ { ( i ) } \Big ) t ^ { 2 } + \Phi } \\ { - \Phi _ { I } ^ { ( i ) } + 2 \pi f _ { I } ^ { ( i ) } \tau _ { I } ^ { ( i ) } + 2 \pi k _ { I } ^ { ( i ) } t \tau _ { I } ^ { ( i ) } - \pi k _ { I } ^ { ( i ) } \tau _ { I } ^ { ( i ) ^ { 2 } } \right) * h ( t ) . } \end{array}\tag{5}
$$

From (5) it follows that the impact of the interference essentially depends on the start frequencies and the slopes of the chirps of the transmitter and the individual interferers. Note also that the LPF in (5) suppresses any signal components outside the desired IF signal bandwidth. Still, if the frequencies of the chirps of the transmitter and an interferer intersect within this bandwidth, the interference becomes directly visible in the IF domain. This case is analyzed in the following section.

![](images/229ba55878c435c5398eeb4780598c85768625e289a88022ccffccaae1818f50.jpg)

(a) Frequency course of instantaneous transmit signal s(t) and one interferer, the dashed line illustrates the IF bandwidth.  
![](images/d4786a11dbb4f386da2ec09c789933a9b67ef5d2c5b74c256d807533805760dc.jpg)  
(b) Time domain IF signal, showing impairments by interference caused by the intersections in the frequency domain within the IF bandwidth.  
Fig. 2. Interference in RF frequency domain and IF time domain.

## III. SIGNAL IMPAIRMENTS CAUSED BY INTERFERENCE

## A. Interference in IF Time Domain Signal

The actual form of impairment in the IF signal caused by interference strongly depends on the character of the intersection of the transmit signal and the interfering signals. The frequency drift of the two different chirps, having slopes k and $k _ { I } ^ { ( i ) }$ in the radio frequency (RF) domain, can be directly seen in the IF signal according to (5). It is important to note that k and $\breve { k _ { I } ^ { ( i ) } }$ are in general different in real-world applications. Thus, the interference signals $y _ { I } ^ { ( i ) } ( t )$ are in the form of chirps in the IF domain, which may cover a large portion or even the entire IF signal bandwidth.

The frequency course of an exemplary interference scenario is depicted in Fig. 2(a). Therein the own transmitter emits a chirp from 76.3 GHz to 76.5 GHz, i.e. $B = 2 0 0 \mathrm { M H z } ,$ in a duration of $T \ : = \ : 6 0 \mu \mathrm { s }$ . Meanwhile the interferer performs two down- and two up-ramps with significantly steeper chirp slopes, leading to three intersections of the frequency courses during the ramp duration T . An impairment in the IF signal occurs whenever such intersections occur within the IF bandwidth, which is indicated by the dashed lines in Fig. 2(a). The IF bandwidth is determined by the LPF cutoff frequency $f _ { c }$ (40 MHz in our example). The corresponding impaired time domain IF signal is shown in Fig. 2(b).

## B. Interference in Frequency Domain

For frequency domain analysis we extend our analysis to use $N _ { c } = 1 5 0$ total up-ramps for the transmitter, each of which is parametrized again with $f _ { 0 } = 7 6 . 3 \mathrm { G H z } , B = 2 0 0 \mathrm { M H z }$ , and $T = 6 0 \mu \mathrm { s }$ . For simplicity, the down-ramps are neglected. The interference chirps are generated randomly according to the limits given in Table I.

TABLE I  
UPPER AND LOWER LIMITS USED FOR GENERATION OF THE RANDOM INTERFERENCE SIGNALS.
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=3 colspan=1>DistanceChirp start frequencyChirp bandwidthChirp duration</td><td rowspan=2 colspan=1>mGHzGHz</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>250</td></tr><tr><td rowspan=1 colspan=1>760.1</td><td rowspan=2 colspan=1>771200</td></tr><tr><td rowspan=1 colspan=1>µs</td><td rowspan=1 colspan=1>20</td></tr></table>

![](images/afa54aa89ed2bf96148afc599693e09eefe5100adb9e9aba00db31e9ebd5cf0c.jpg)  
Fig. 3. Magnitude of the range FFTs for the $N _ { c } = 1 5 0$ chirps with three object reflections and eight random interferers (each thin line represents the range FFT of a single chirp). The bold line shows the minimum calculated along the chirps for each frequency bin. This minimum is used exemplarily for our noise suppression algorithm for interference cancellation.

In order to determine the distance of the objects, FFTs of the IF signals are computed. The magnitudes of these socalled range FFTs for our example with $N _ { c } = 1 5 0$ subsequent chirps, containing three object reflections and eight random interferers, are depicted in Fig. 3. It is observed that in case interference occurs, the noise floor significantly increases. This is due to the fact that the interference appears in the form of chirps in the IF signal according to (3). Ultimately, small or far away objects may thus no longer be detectable.

Note that a special case of interference occurs if the chirp parameters of the own transmitter and the interferer are the same and, at the same time, the time delay of the interferer is such that the mixing product is within the IF bandwidth. In this case the interferer IF signal yields a constant beat frequency such that the interferer would appear as a peak in the spectrum (like a conventional object reflection). Thus, in this particular case, the interferer creates a so-called ghost target [8]. Anyhow, the probability of an appearing ghost target in practice is very small.

## IV. CANCELLATION OF INTERFERENCE

In this section our interference cancellation concept is proposed. It operates in frequency domain by manipulating the magnitude response over $N _ { c }$ recorded chirps.

Assume that we obtain $N _ { s }$ discrete samples of the IF signal for each of the $N _ { c }$ recorded chirps. These samples are stored in a matrix $\mathbf { X } \in \mathbb { R } ^ { N _ { c } \times N _ { s } }$ . The complex data points of the discrete Fourier transform (DFT) of X over the $N _ { s }$ discrete samples are stacked in the matrix $\mathbf { Y } \in \mathbb { R } ^ { N _ { c } \times N _ { s } }$ , whose entry in the i-th row and j-th column is defined as

$$
[ \mathbf { Y } ] _ { i , j } = [ \mathbf { A } ] _ { i , j } ~ e ^ { j [ \varphi ] _ { i , j } } ,\tag{6}
$$

with $\mathbf { A } \in \mathbb { R } ^ { N _ { c } \times N _ { s } }$ and $\boldsymbol { \varphi } \in \mathbb { R } ^ { N _ { c } \times N _ { s } }$ being the amplitudes and the phases of the data points, respectively.

In the first step the phases $\varphi$ are stored in a memory. We denote $\mathbf { a } _ { j }$ as the j-th column of A, i.e. the magnitude of the j-th range bin of each ramp, such that $\mathbf { A } = [ \mathbf { a } _ { 1 } , \dots , \mathbf { a } _ { N _ { s } } ]$ Furthermore, we define the vector

$$
\mathbf { a } _ { \mathrm { c a n c } , j } = f \left( \mathbf { a } _ { j } \right) ,\tag{7}
$$

where the function $f \left( \mathbf { a } _ { j } \right)$ operates over the $N _ { c }$ ramps of the j-th range bin. One possible choice for the function $f \left( \mathbf { a } _ { j } \right)$ is the minimum over the input vector ${ \bf a } _ { j }$ , i.e.

$$
f \left( \mathbf { a } _ { j } \right) = \operatorname* { m i n } \left( \mathbf { a } _ { j } \right) .\tag{8}
$$

When calculated for each range bin, this delivers the vector $\mathbf { a } _ { \operatorname* { m i n } } \in \mathbb { R } ^ { 1 \times N _ { s } }$ s , which is stacked up again into a matrix as

$$
{ \bf A } _ { \mathrm { c a n c } } = { \bf 1 } _ { N _ { c } } { \bf a } _ { \mathrm { m i n } } ,\tag{9}
$$

where $\mathbf { 1 } _ { N _ { c } } \in \mathbb { R } ^ { N _ { c } \times 1 }$ is a row vector with all ones. Finally, the amplitude matrix $\mathbf { A } _ { \mathrm { c a n c } }$ is merged with the previously stored phases $\varphi$ in order to obtain the modified complex data points of the DFT as

$$
[ \mathbf { Y } _ { \mathrm { c a n c } } ] _ { i , j } = [ \mathbf { A } _ { \mathrm { c a n c } } ] _ { i , j } \ e ^ { j [ \varphi ] _ { i , j } } .\tag{10}
$$

Note that the matrix $\mathbf { Y } _ { \mathrm { c a n c } }$ now contains the interference cancelled amplitudes $\mathbf { A } _ { \mathrm { { c a n c } } }$ . Thereby, only the objects, which are presumed to be present in the spectrum throughout all the chirps, remain. Still, the phases $\varphi$ are left unchanged in the cancelled signal, and thus further Doppler processing will reveal information about the speed of the detected objects.

Note further that the minimum operator in (8) is just one possible candidate to perform the noise suppression and the further interference cancellation having low computational complexity. Alternatively, the lower envelope or some sliding window statistics could be used for $f \left( \mathbf { a } _ { j } \right)$ , depending on the target application. Anyhow, in our simulations we will use the aforementioned minimum operator. This way also ghost targets are suppressed, assuming that they do not appear at the same frequency bin for all the $N _ { c }$ regarded chirps.

Since in our algorithm the phase information is unmodified, the remaining interference signal parts in $\mathbf { Y } _ { \mathrm { c a n c } }$ depend on the actual interferer power. This is shown in Fig. 4 based on a single complex discrete Fourier coefficient for low powered interference (strong object reflection, weak interferer power) and high powered interference (weak object reflection, strong interferer power). In case of low powered interference the computed phase error is negligible, whereas high powered interference may lead to a large residual error. Therefore the proposed algorithm is suited for short range radar systems, since there stronger object reflections (and thus low powered interference) appear more likely.

![](images/5e95963dd77f5a8d25bcca25787f50010d7edbbe2be29b3e6bd02556f75b675e.jpg)  
Fig . 4. Vector diagrams of low powered interference (left drawin<sub>g</sub>) and hi<sub>g</sub>h powered interference (ri<sub>g</sub>ht drawin<sub>g</sub>) of a com<sub>p</sub>lex DFT coefficient. Since onl<sub>y</sub> th<sub>e</sub> <sub>magn</sub>it<sub>u</sub>d<sub>e</sub> i<sub>s</sub> <sub>correc</sub>t<sub>e</sub>d i<sub>n</sub> <sub>our</sub> <sub>a</sub>l<sub>gor</sub>ith<sub>m</sub> th<sub>e</sub> <sub>rema</sub>i<sub>n</sub>i<sub>ng</sub> <sub>p</sub>h<sub>ase</sub> di<sub>s</sub>t<sub>or</sub>ti<sub>on</sub> hi<sub>g</sub>hl<sub>y</sub> d<sub>epen</sub>d<sub>s</sub> <sub>on</sub> th<sub>e</sub> i<sub>n</sub>t<sub>er</sub>f<sub>erer</sub> <sub>power</sub>.

## V S IMULATION RESULTS

I<sub>n</sub> thi<sub>s</sub> <sub>sec</sub>ti<sub>on,</sub> <sub>s</sub>i<sub>mu</sub>l<sub>a</sub>ti<sub>on</sub> <sub>resu</sub>lt<sub>s</sub> <sub>are</sub> <sub>presen</sub>t<sub>e</sub>d t<sub>o</sub> <sub>prove</sub> <sub>our</sub> <sub>propose</sub>d <sub>me</sub>th<sub>o</sub>d <sub>an</sub>d t<sub>o</sub> <sub>compare</sub> it t<sub>o</sub> th<sub>e</sub> TDT <sub>an</sub>d FDT <sub>me</sub>th<sub>o</sub>d<sub>s</sub> F<sub>or</sub> thi<sub>s</sub> <sub>compar</sub>i<sub>son</sub> th<sub>e</sub> <sub>average</sub> <sub>s</sub>i<sub>gna</sub>l t<sub>o</sub> remaining interference noise ratio (SRINR) over the ran<sub>g</sub>e FFT<sub>s</sub> i<sub>s</sub> <sub>regar</sub>d<sub>e</sub>d<sub>.</sub> It i<sub>s</sub> d<sub>e</sub>t<sub>erm</sub>i<sub>ne</sub>d <sub>as</sub> th<sub>e</sub> <sub>ra</sub>ti<sub>o</sub> <sub>o</sub>f th<sub>e</sub> <sub>power</sub> <sub>o</sub>f <sub>a</sub> single obj ect reflection to the average remaining interference <sub>power</sub> <sub>a</sub>ft<sub>er</sub> <sub>cance</sub>ll<sub>a</sub>ti<sub>on.</sub> Th<sub>e</sub> <sub>resu</sub>lti<sub>ng</sub> SRINR <sub>va</sub>l<sub>ues</sub> f<sub>or</sub> 8 <sub>an</sub>d 1 6 i<sub>n</sub>t<sub>er</sub>f<sub>erers</sub> <sub>are</sub> <sub>summar</sub>i<sub>ze</sub>d i<sub>n</sub> T<sub>a</sub>bl<sub>e</sub> II<sub>.</sub> N<sub>o</sub>t<sub>e</sub> th<sub>a</sub>t th<sub>e</sub> obj ect reflections are perfectly known in simulations <sub>.</sub> Thus th<sub>e</sub> th<sub>res</sub>h<sub>o</sub>ld<sub>s</sub> f<sub>or</sub> TDT <sub>an</sub>d FDT <sub>are</sub> <sub>per</sub>f<sub>ec</sub>tl<sub>y</sub> <sub>se</sub>t<sub>.</sub> Still <sub>ou</sub>r <sub>p</sub>r<sub>opose</sub>d <sub>a</sub>l<sub>go</sub>rithm <sub>ou</sub>t<sub>pe</sub>rf<sub>o</sub>rm<sub>s</sub> TDT <sub>as</sub> <sub>we</sub>ll <sub>as</sub> FDT significantly even for the relatively large obj ect distance of 1 2 5 <sub>m</sub> i<sub>n</sub> <sub>our</sub> <sub>examp</sub>l<sub>e.</sub>

F<sub>or</sub> f<sub>ur</sub>th<sub>er</sub> <sub>ana</sub>l<sub>ys</sub>i<sub>s</sub> <sub>we</sub> <sub>eva</sub>l<sub>ua</sub>t<sub>e</sub> th<sub>e</sub> <sub>range</sub> D<sub>opp</sub>l<sub>er</sub> <sub>map</sub> <sub>o</sub>f th<sub>e</sub> <sub>resu</sub>lti<sub>ng</sub> i<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> <sub>cance</sub>ll<sub>e</sub>d <sub>s</sub>i<sub>gna</sub>l <sub>us</sub>i<sub>ng</sub> <sub>our</sub> <sub>a</sub>l<sub>gor</sub>ith<sub>m</sub> W<sub>e</sub> <sub>ex</sub>t<sub>en</sub>d <sub>our</sub> <sub>s</sub>i<sub>mu</sub>l<sub>a</sub>ti<sub>on</sub> <sub>se</sub>t<sub>up</sub> t<sub>o</sub> 50 <sub>ran</sub>d<sub>om</sub> i<sub>n</sub>t<sub>er</sub>f<sub>erers</sub> (44% interfered sam<sub>p</sub>les) and three obj ect reflections The <sub>resu</sub>lti<sub>ng</sub> <sub>range</sub> D<sub>opp</sub>l<sub>er</sub> <sub>map</sub> i<sub>s</sub> d<sub>ep</sub>i<sub>c</sub>t<sub>e</sub>d i<sub>n</sub> Fi<sub>g .</sub> 5 <sub>,</sub> <sub>s</sub>h<sub>ow</sub>i<sub>ng</sub> th<sub>a</sub>t th<sub>e</sub> <sub>a</sub>l<sub>gor</sub>ith<sub>m</sub> <sub>wor</sub>k<sub>s</sub> <sub>per</sub>f<sub>ec</sub>tl<sub>y</sub> f<sub>or</sub> <sub>s</sub>h<sub>or</sub>t di<sub>s</sub>t<sub>ances</sub> Thi<sub>s</sub> i<sub>s</sub> <sub>eas</sub>il<sub>y</sub> <sub>exp</sub>l<sub>a</sub>i<sub>ne</sub>d <sub>w</sub>ith th<sub>e</sub> <sub>ra</sub>d<sub>ar</sub> <sub>equa</sub>ti<sub>on.</sub> Th<sub>e</sub> <sub>power</sub> <sub>o</sub>f <sub>an</sub> obj ect reflection decays with $d ^ { 4 }$ <sub>w</sub>ith d b<sub>e</sub>i<sub>ng</sub> th<sub>e</sub> di<sub>s</sub>t<sub>ance.</sub> M<sub>eanw</sub>hil<sub>e,</sub> th<sub>e</sub> i<sub>n</sub>t<sub>er</sub>f<sub>erer</sub> <sub>power</sub> d<sub>ecays</sub> <sub>on</sub>l<sub>y</sub> <sub>w</sub>ith $d ^ { 2 } .$ <sub>.</sub> Th<sub>us</sub> th<sub>e</sub> i<sub>n</sub>t<sub>er</sub>f<sub>erer</sub> <sub>power</sub> i<sub>s</sub> <sub>cons</sub>id<sub>ere</sub>d t<sub>o</sub> b<sub>e</sub> <sub>compara</sub>bl<sub>y</sub> <sub>s</sub>t<sub>rong</sub> i<sub>n</sub> general <sub>.</sub> Still for close obj ects it can be as sumed that low powered interference (cf<sub>.</sub> Fi<sub>g .</sub> 4) occurs more likel<sub>y.</sub> For far away obj ects the velocity cannot be detected perfectly because of the lower power level of the obj ect reflection<sub>.</sub> In conclusion <sub>our</sub> <sub>a</sub>l<sub>gor</sub>ith<sub>m</sub> i<sub>s</sub> th<sub>us</sub> hi<sub>g</sub>hl<sub>y</sub> <sub>su</sub>it<sub>a</sub>bl<sub>e</sub> f<sub>or</sub> <sub>s</sub>h<sub>or</sub>t <sub>range</sub> <sub>ra</sub>d<sub>ar</sub> <sub>sys</sub>t<sub>ems</sub> Still it <sub>cou</sub>ld b<sub>e</sub> <sub>com</sub>bi<sub>ne</sub>d <sub>w</sub>ith f<sub>or</sub> i<sub>ns</sub>t<sub>ance</sub> TDT t<sub>o</sub> i<sub>mprove</sub> th<sub>e</sub> <sub>per</sub>f<sub>ormance.</sub>

## VI <sub>.</sub> CONCLUSION

I<sub>n</sub> thi<sub>s</sub> <sub>wor</sub>k <sub>we</sub> <sub>propose</sub>d <sub>a</sub> <sub>nove</sub>l i<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> <sub>cance</sub>ll<sub>a</sub>ti<sub>on</sub> <sub>co</sub>n<sub>cep</sub>t f<sub>o</sub>r FMCW r<sub>a</sub>d<sub>a</sub>r <sub>sys</sub>t<sub>ems .</sub> It <sub>ma</sub>k<sub>es</sub> <sub>use</sub> <sub>o</sub>f <sub>no</sub>i<sub>se</sub> suppression to uncover true obj ect reflections <sub>.</sub> The noise sup-<sub>press</sub>i<sub>on</sub> i<sub>s</sub> <sub>per</sub>f<sub>orme</sub>d i<sub>n</sub> f<sub>requency</sub> d<sub>oma</sub>i<sub>n</sub> b<sub>y</sub> <sub>e.g .</sub> d<sub>e</sub>t<sub>erm</sub>i<sub>n</sub>i<sub>ng</sub> th<sub>e</sub> <sub>m</sub>i<sub>n</sub>i<sub>mum</sub> <sub>o</sub>f th<sub>e</sub> <sub>magn</sub>it<sub>u</sub>d<sub>e</sub> <sub>among</sub> th<sub>e</sub> <sub>recor</sub>d<sub>e</sub>d <sub>c</sub>hi<sub>rps .</sub> Si<sub>nce</sub> <sub>no</sub> <sub>con</sub>fi<sub>gura</sub>ti<sub>on</sub> i<sub>s</sub> <sub>requ</sub>i<sub>re</sub>d th<sub>e</sub> <sub>a</sub>l<sub>gor</sub>ith<sub>m</sub> i<sub>s</sub> <sub>ro</sub>b<sub>us</sub>t <sub>compare</sub>d t<sub>o</sub> <sub>ex</sub>i<sub>s</sub>ti<sub>ng</sub> th<sub>res</sub>h<sub>o</sub>ld-b<sub>ase</sub>d i<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> <sub>cance</sub>ll<sub>ers .</sub> Si<sub>mu</sub>l<sub>a</sub>ti<sub>on</sub> <sub>resu</sub>lt<sub>s</sub> <sub>s</sub>h<sub>ow</sub> th<sub>a</sub>t i<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> <sub>can</sub> b<sub>e</sub> <sub>cance</sub>ll<sub>e</sub>d <sub>a</sub>l<sub>mos</sub>t <sub>per</sub>f<sub>ec</sub>tl<sub>y</sub> <sub>par</sub>ti<sub>cu</sub>l<sub>ar</sub>l<sub>y</sub> f<sub>or</sub> <sub>sma</sub>ll di<sub>s</sub>t<sub>ances .</sub>

TABLE II  
S IGNAL TO REMAINING INTERFERENCE NOISE RATIO ( S RINR) VALUES AND THE RELATIVE INTERFERENCE TIME AVERAGED OVER 1 00 RANDOM S CENARIOS WITH $N _ { c } = 1 5 0$ TRANSMITTED CHIRPS EACH . THE OBJECT DISTANCE WAS CHOSEN TO B E 1 25 M FOR THIS ANALYSIS .
<table><tr><td>Number of interferers</td><td>Interfered samples [%]</td><td>TDT SRINR [dB]</td><td>FDT SRINR [dB]</td><td>Proposed SRINR [dB]</td></tr><tr><td>8</td><td>13.92</td><td>16.06</td><td>19.78</td><td>26.32</td></tr><tr><td>16</td><td>26.00</td><td>12.59</td><td>18.43</td><td>20.36</td></tr></table>

![](images/fb60b35d5774359c86f40707c2bf8d4a035951e54f4ced8eae41f76d089d2072.jpg)  
Fi<sub>g</sub> . 5 . I<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> <sub>cance</sub>ll<sub>e</sub>d <sub>range</sub> D<sub>opp</sub>l<sub>er</sub> <sub>map</sub> <sub>w</sub>ith 50 i<sub>n</sub>t<sub>er</sub>f<sub>erers</sub> <sub>an</sub>d th<sub>ree</sub> t<sub>arge</sub>t<sub>s</sub> Th<sub>e</sub> t<sub>arge</sub>t<sub>s</sub> <sub>can</sub> b<sub>e</sub> <sub>recogn</sub>i<sub>ze</sub>d <sub>c</sub>l<sub>ear</sub>l<sub>y</sub> <sub>par</sub>ti<sub>cu</sub>l<sub>ar</sub>l<sub>y</sub> f<sub>or</sub> <sub>sma</sub>ll di<sub>s</sub>t<sub>ances</sub>

## ACKNOWLEDGMENT

Thi<sub>s</sub> <sub>wor</sub>k h<sub>as</sub> b<sub>een</sub> f<sub>un</sub>d<sub>e</sub>d b<sub>y</sub> LCM G<sub>m</sub>bH <sub>as</sub> <sub>par</sub>t <sub>o</sub>f <sub>a</sub> K2 proj ect<sub>.</sub> K2 proj ects are financed using funding from the Austrian COMET-K2 programme<sub>.</sub> The COMET K2 projects <sub>a</sub>t LCM <sub>are</sub> <sub>suppor</sub>t<sub>e</sub>d b<sub>y</sub> th<sub>e</sub> A<sub>us</sub>t<sub>r</sub>i<sub>an</sub> f<sub>e</sub>d<sub>era</sub>l <sub>governmen</sub>t<sub>,</sub> th<sub>e</sub> f<sub>e</sub>d<sub>era</sub>l <sub>s</sub>t<sub>a</sub>t<sub>e</sub> <sub>o</sub>f U<sub>pper</sub> A<sub>us</sub>t<sub>r</sub>i<sub>a</sub> th<sub>e</sub> J<sub>o</sub>h<sub>annes</sub> K<sub>ep</sub>l<sub>er</sub> U<sub>n</sub>i<sub>vers</sub>it<sub>y</sub> <sub>an</sub>d <sub>a</sub>ll <sub>o</sub>f th<sub>e</sub> <sub>sc</sub>i<sub>en</sub>tifi<sub>c</sub> <sub>par</sub>t<sub>ners</sub> <sub>w</sub>hi<sub>c</sub>h f<sub>orm</sub> <sub>par</sub>t <sub>o</sub>f th<sub>e</sub> K2- COMET C<sub>o</sub>n<sub>so</sub>rti<sub>u</sub>m

## REFERENCES

[ 1 ] S Heuel <sup>“</sup>Automotive Radar Interference Test <sup>”</sup> In Proceedin<sub>g</sub>s of the 1 8th International Radar Symposium (IRS 201 7) June 20 1 7

[2] G M Brooker <sup>“</sup>Mutual Interference of Millimeter-Wave Radar S<sub>y</sub>stems <sup>”</sup> In IEEE T<sub>ransac</sub>ti<sub>ons</sub> <sub>on</sub> El<sub>ec</sub>t<sub>romagne</sub>ti<sub>c</sub> C<sub>ompa</sub>tibilit<sub>y</sub> V<sub>o</sub>l 49 N<sub>o</sub> 1 <sub>pp</sub>. 1 70– 1 8 1 F<sub>e</sub>br<sub>ua</sub>r<sub>y</sub> 2007 .

[3 ] M. Kunert <sup>“</sup>The EU proj ect MOSARIM : A general overview of proj ect obj ectives and conducted work <sup>”</sup> In Proceedings of the 9th European Radar Conference (EuRAD 2012) pp. 1–5 October 20 1 2.

[4] A. Bourdoux K. Parashar and M. B auduin <sup>“</sup>Phenomenolo<sub>gy</sub> of Mutual Int<sub>e</sub>rf<sub>e</sub>r<sub>e</sub>n<sub>ce</sub> <sub>o</sub>f FMCW <sub>an</sub>d PMCW A<sub>u</sub>t<sub>omo</sub>ti<sub>ve</sub> R<sub>a</sub>d<sub>ars</sub> <sup>”</sup> I<sub>n</sub> P<sub>rocee</sub>di<sub>ngs</sub> of the IEEE Radar Conference pp. 1 709– 1 7 1 4 May 20 1 7 .

[5 ] M . B arj enbruch D . Kellner K. Dietma<sub>y</sub>er J. Kla<sub>pp</sub>stein and J. Dick-<sub>mann</sub> <sup>“</sup>A M<sub>e</sub>th<sub>o</sub>d f<sub>or</sub> I<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> C<sub>ance</sub>ll<sub>a</sub>ti<sub>on</sub> i<sub>n</sub> A<sub>u</sub>t<sub>omo</sub>ti<sub>ve</sub> R<sub>a</sub>d<sub>ar</sub> <sup>”</sup> I<sub>n</sub> Proceedings of the IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM 201 5) pp . 1 –4 April 20 1 5 .

[6] J. B echter K. Biswas and C . Waldschmidt <sup>“</sup>Estimation and Cancellation of Interferences in Automotive Radar Signals <sup>”</sup> In Proceedings of the 1 8th International Radar Symposium (IRS 201 7) June 20 1 7

[7] C . Fischer <sup>“</sup>Untersuchun<sub>g</sub>en zum Interferenzverhalten automobiler R<sub>a</sub>d<sub>arsensor</sub>ik <sup>”</sup> Ph D di<sub>sser</sub>t<sub>a</sub>ti<sub>on</sub> U<sub>n</sub>i<sub>vers</sub>it<sub>a</sub>t Ul<sub>m</sub> 20 1 6¨

[8] M. Go<sub>pp</sub>elt<sub>,</sub> H. L. Blocher<sub>,</sub> and W. Menzel<sub>,</sub> <sup>“</sup>Anal<sub>y</sub>tical investi<sub>g</sub>ation <sub>o</sub>f <sub>mu</sub>t<sub>ua</sub>l i<sub>n</sub>t<sub>er</sub>f<sub>erence</sub> b<sub>e</sub>t<sub>ween</sub> <sub>au</sub>t<sub>omo</sub>ti<sub>ve</sub> FMCW <sub>ra</sub>d<sub>ar</sub> <sub>sensors</sub> <sup>”</sup> I<sub>n</sub> Proceedings of the German Microwave Conference (GeMIC 201 1 ) pp . 1 –4 M<sub>arc</sub>h 20 1 1