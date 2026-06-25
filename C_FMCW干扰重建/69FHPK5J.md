# Automotive Radar Interference Mitigation using a Sparse Sampling Approach

Jonathan Bechter, Fabian Roos, Mahfuzur Rahman, Christian Waldschmidt

Institute of Microwave Engineering, Ulm University, Germany

jonathan.bechter@uni-ulm.de

Abstract—The application of radar sensors for driver assistance systems and autonomous driving leads to an increasing probability of radar interferences. Those interferences degrade the detection capabilities and can cause sensor blindness. This paper uses a realistic road scenario to address the problems of a common countermeasure that simply removes interferenceaffected parts of time domain radar signals and thereby introduces a gap. The paper solves the problem with the application of a sparse sampling signal recovery algorithm that is also used for compressed sensing problems. It is shown that the signal recovery can clearly overcome the shortcomings of just removing interfered signal parts. In the end of the paper, the applicability of the used algorithm is verified with measured radar data.

## I. INTRODUCTION

For automotive safety and driver assistance systems, radar sensors become a common device. They offer certain benefits towards other sensors, like reliable functionality in the presence of fog or rain. However, the increasing usage of radar sensors leads to increasing occurrence of mutual interferences. For the very common FMCW (frequency modulated continuous wave) radars, a high chance for interference has been predicted if the sensors have different ramp slopes [1]. Although the occurrence of ghost targets is very unlikely [1], [2], interferences lead to a wide-band increase of the noise floor in the baseband signals, and therefore can severely decrease the detection capability of the sensors [3]. Even if interferences are received only through the side-lobes of a sensor, their effect is not negligible [4].

Due to theses circumstances, various methods for detection and mitigation of automotive radar interferences have been investigated. Regarding time domain radar signals, interferences typically show up as time-limited artifacts with a very high amplitude. Therefore, their occurrence can be detected with power detectors or matched filters [5], but also methods from image processing have been adapted [6]. After detection, an often recommended technique is to simply remove the interfered samples from the signal. This completely removes the interference-induced noise floor from the spectrum. However, with the newly introduced gap new artifacts arise.

The investigation in this paper starts with the incomplete radar signals. In an introductory part, the problems of simply removing the interfered signal part is discussed with a relevant road scenario. The more efficient application of a window function for blinding out interferences [6] is also taken into account. To overcome those methods’ shortcomings, an algorithm for the processing of sparse signals, which was demonstrated to be efficient in compressed sensing problems [7], is applied on the simulated data of a chirp sequence modulated FMCW radar. The signal recovery quality with a view to amplitude and phase is investigated for multiple interference durations. An adaptive selection of the algorithm’s parameters offers good performance for arbitrarily varying interference conditions. For verification, the algorithm is applied to a measured data set.

![](images/4bd93f7609ed503f21a2bbcc9d1f206e648e6ddbedca16f018163efd77d5668b.jpg)  
Fig. 1. Bicycle and truck must be detected by the car’s radar sensor. However, the radar sensor of the truck causes interferences. This leads to a challenging scenario for the signal processing.

TABLE I  
RADAR PARAMETERS OF CAR AND TRUCK
<table><tr><td></td><td> $\mathrm { C a r }$ </td><td>Truck</td></tr><tr><td>Bandwidth B</td><td>500 MHz</td><td>700 MHz</td></tr><tr><td>Ramp duration T</td><td>45 μs</td><td>45μs</td></tr><tr><td>Ramp repetition rate  $T _ { \mathrm { r 2 r } }$ </td><td>52μs</td><td>52μs</td></tr><tr><td>Center frequency  $f _ { c }$ </td><td>76.5 GHz</td><td>76.5 GHz</td></tr></table>

TABLE II  
SCENARIO SCENERY
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RCS</td><td rowspan=1 colspan=1>Range</td><td rowspan=1 colspan=1>Velocity</td></tr><tr><td rowspan=2 colspan=1>TruckBicycle</td><td rowspan=1 colspan=1>20 dBsm</td><td rowspan=1 colspan=1>19m</td><td rowspan=1 colspan=1>5m/s</td></tr><tr><td rowspan=1 colspan=1>-10 dBsm</td><td rowspan=1 colspan=1>15m</td><td rowspan=1 colspan=1>5m/s</td></tr></table>

## II. PROBLEM DESCRIPTION

The car in Fig. 1 wants to turn left. It uses a chirp sequence modulated radar sensor to detect the bicycle and the truck that approach from the other side. The truck cannot overtake, so it drives at the same velocity as the bicycle. The radar parameters of the car’s and the truck’s sensor are given in Tab. I, while the parameters of the targets are found in Tab. II. The radar cross section (RCS) of the bicycle is chosen according to [8] for a view angle of 15◦. With this setting, it is no problem for the radar to detect the truck as well as the bicycle.

However, the truck is equipped with a radar which uses a very similar modulation as the car’s sensor. With a receiver bandwidth of $B _ { \mathrm { R x } } { = } 4 . 4 \mathrm { M H z }$ , this leads to an interference duration of [3]

$$
T _ { \mathrm { I n t } } = \frac { 2 B _ { \mathrm { R x } } } { \left| \frac { B _ { \mathrm { T r u c k } } } { T _ { \mathrm { T r u c k } } } - \frac { B _ { \mathrm { C a r } } } { T _ { \mathrm { C a r } } } \right| } = 2 \mu \mathrm { s } .\tag{1}
$$

With a sampling rate of $f _ { s } { = } 1 0 \mathrm { M H z } .$ , 20 out of 450 samples of the baseband signal are affected by interference. It is assumed here that the interference occurs in the middle of the baseband time signal. As the ramp repetition time $T _ { \mathrm { r 2 r } }$ of both sensors is identical, the interference occurs at the same time in each frequency ramp. To mitigate the interference effects discussed in the introduction, the interfered signal part can be replaced by zeros. This introduces a gap with duration $T _ { \mathrm { I n t } }$ to the signal. The effect on the baseband signal is described analytically as

$$
s ( t ) = A _ { 0 } \cos ( 2 \pi f _ { 0 } t ) \cdot \left[ \mathrm { r e c t } \left( \frac { t } { T } \right) - \mathrm { r e c t } \left( \frac { t } { T _ { \mathrm { I n t } } } \right) \right] ,\tag{2}
$$

where $f _ { 0 }$ indicates an arbitrary frequency component of the signal which has an amplitude $A _ { 0 }$

Considering the positive part of the frequency spectrum, the signal gap introduces an additional si-function:

$$
S ( f ) = \frac { A _ { 0 } } { 2 } \delta ( f - f _ { 0 } ) * \left[ T \mathrm { s i } \left( \pi T f \right) - T _ { \mathrm { I n t } } \mathrm { s i } \left( \pi T _ { \mathrm { I n t } } f \right) \right] .\tag{3}
$$

Both si-functions are convolved with each single target signal. Without taking into account a window function, the integration gain of each target is thereby reduced to

$$
G _ { \mathrm { I } } = 1 0 \log _ { 1 0 } \frac { ( T - T _ { \mathrm { I n t } } ) ^ { 2 } f _ { s } } { T } .\tag{4}
$$

For a signal that is processed with a window function w[k], this expression changes to

$$
G _ { \mathrm { I } } = 1 0 \log _ { 1 0 } \frac { \left( \sum _ { k \notin T _ { \mathrm { I n t } } } w [ k ] \right) ^ { 2 } } { T f _ { s } } .\tag{5}
$$

The sum in the numerator adds up all samples that are not affected by interference and therefore not removed from the signal. In addition to this power loss, each vacancy-induced si-function in (3) has a envelope depending on the respective target’s power $A _ { 0 }$ . The minimum distance from the envelope to the target peak power level is determined by the interference duration $T _ { \mathrm { I n t } }$ and is estimated as

$$
\Delta P _ { \mathrm { m i n } } = \operatorname* { m i n } _ { f > 1 / T } \left[ 1 0 \log _ { 1 0 } { \frac { T - T _ { \mathrm { I n t } } } { T \mathrm { s i } \left( \pi T f \right) - T _ { \mathrm { I n t } } \mathrm { s i } \left( \pi T _ { \mathrm { I n t } } f \right) } } \right]\tag{6}
$$

The values of $T$ and $T _ { \mathrm { I n t } }$ are known, so $\Delta P _ { \mathrm { m i n } }$ can be determined. The condition $f > 1 / T$ ensures that the envelope according to $T$ already dropped to its first zero, and therefore is not mixed up with the maximum of the vacancy-induced envelope.

In the scenario in Fig. 1, the vacancy-induced artifacts that are convolved with the truck’s signal are strong enough to cover the signal of the bicycle. The spectrum in Fig. 2 shows only the velocity 5 m/s; the bicycle cannot be detected anymore. Instead of sharp notching, a window function can be used to smoothen the junction between signal and gap [6]. Fig. 2 also shows the application of a cosine window with a length of 20 samples. It clearly reduces the side lobes of the vacancy-induced si-function, but the bicycle still cannot be detected. The sensor’s range resolution severely degrades because of the signal gap.

![](images/1a1d475a4bd4503f6b1889f04333bee23f027e3590a301c7853223be3b52bb73.jpg)  
Fig. 2. Spectrum (for 5 m/s) of the incomplete signal after interference removal (20 out of 450 samples), and the signal with the vacancy smoothed by a cosine window, in comparison to the interference-free signal without any vacancy.

![](images/c8a802389c1d3820e4dc2b0937a0067022a1ab6ef165a7690675fd96a9b743f9.jpg)  
Fig. 3. The non-existing values in the incomplete signal ( ) are estimated in each iteration n. For the current iteration the threshold thr<sub>n</sub> is depicted leading to the reconstructed signal ( ).

To overcome the problem, the lost samples are recovered with an approach called iterative method with adaptive thresholding (IMAT) [9]. The algorithm starts with considering the spectrum of the incomplete signal in Fig. 3. The value of the highest peak $\beta _ { \mathrm { d B m } }$ is used to initialize the linear threshold

$$
{ \mathrm { t h r } } _ { n } = \beta \mathrm { e } ^ { - \alpha n } .\tag{7}
$$

Every spectral point, which lies above the current threshold, is used to calculate an approximated time domain signal with an inverse Fourier Transform. In the incomplete time signal, the missing samples are replaced with the corresponding values of the approximated signal. According to (7), each iteration n lowers the threshold by a fixed value in dB scale. The parameter α determines the step size and can be chosen arbitrarily.

![](images/7fa6bd19b9eed03ac259ae90e80229a5dc8e9f9ad131b290ea347ea660df7734.jpg)  
Fig. 4. The IMAT algorithm is applied to the incomplete signal, and the blue curve is recovered. This allows the detection of the truck as well as the bicycle. The spectrum of the signal without any vacancy is shown for comparison.

While lowering the threshold, the vacancy-induced artifacts are removed step-by-step. Therefore, the artifacts must not be above $\operatorname { t h r } _ { n } ,$ or they are considered as desired signal components. This cannot happen in the first step with $n = 0 ,$ as to this time only the highest peak in the spectrum is taken into account as shown in Fig. 3. From (6) the minimum power distance of the first undesired artifacts is known. Thus $\alpha$ is chosen in a way that the algorithm will perform m iterations before the first artifacts can be reached by the threshold:

$$
m \alpha _ { \mathrm { d B } } = \Delta P _ { \mathrm { m i n } } ,\tag{8}
$$

$$
\alpha = \frac { \alpha _ { \mathrm { d B } } } { 2 0 \log \mathrm { e } } .\tag{9}
$$

The threshold must not decrease below the receiver noise floor which is given as

$$
N = k T _ { K } ( 2 B _ { \mathrm { R x } } ) F ,\tag{10}
$$

where k is the Boltzmann constant, $T _ { K }$ the temperature, and $F$ describes the receiver noise figure. The total number of iterations n is chosen in a way that the final threshold is still at least 10 dB above the noise floor:

$$
n < \frac { \beta _ { \mathrm { d B m } } - ( N + 1 0 \mathrm { d } \mathrm { B } ) } { \alpha _ { \mathrm { d B } } } .\tag{11}
$$

With the adaptive parameter selection in (7), (8), and (11), the incomplete signal is repaired. For the given scenario, this leads to $\alpha _ { \mathrm { d B } } { = } 5 . 1 4 \mathrm { d B }$ and $\beta _ { \mathrm { d B m } } { = } { \mathrm { - } } 3 6 . 3 \mathrm { d B m }$ , while $m { = } 3$ is chosen. After 9 iterations, the spectrum in Fig. 4 is achieved. It is again compared to the signal of an interference-free simulation. $\mathrm { A l - }$ though there are still minor deviations, it is clearly possible to separate the signals of bicycle and truck. Both can be detected after application of the recovery algorithm. The recovered time signal is shown in Fig. 5 for the first frequency ramp, again in comparison with the corresponding signal without gap. Only minor deviations between the signals are visible.

## III. SIMULATIVE EVALUATION

In this section, the discussed problem is investigated for multiple signal gap sizes. Different gap sizes correspond to increasing the ramp slope of the truck’s sensor, thus creating more interfered samples according to (1). The other parameters are kept as before. The value of m=3 is chosen for all simulations, as it is sufficient to achieve good results. The root mean square error (RMSE) of phase and amplitude of both target peaks in the spectrum is calculated for the incomplete signal, the incomplete signal with cosine window of length 20, and the signal recovered with IMAT. For each gap size, 25 simulations with different noise realizations are evaluated. The RMSE is calculated as

![](images/9528625f645937c9a142acdd2fd38a8333a3566247d0f4e1cc2f534ec6c2403f.jpg)  
Fig. 5. The IMAT algorithm is applied to the incomplete signal, and the blue curve is recovered. Only minor deviations remain in the time domain signal.

$$
\mathrm { R M S E } = \mathrm { E } \left( ( x _ { \mathrm { o p t } } - \hat { x } ) ^ { 2 } \right) ,\tag{12}
$$

with the expectation operator $\mathrm { E , }$ the observed variable ${ \hat { x } } ,$ and its optimum value $x _ { \mathrm { o p t } }$ . The RMSE values of phase and amplitude are called $\Delta \varphi$ and $\Delta A ,$ , respectively.

Fig. 6 shows $\Delta \varphi$ for the bicycle (peak in the distance 15 m in Fig. 2) for a receive signal with 10 %–55 % gap size. As in the above simulation, the center part of the signal is affected by the interference. The overall performance of the IMAT algorithm is very good compared to the other methods, although the phase error clearly increases at 35 % gap size.

However, the phase errors of the other two methods show a periodicity for increasing gap sizes. It is seen in Fig. 2 that the side lobes introduced by the vacancy have minima and maxima. Their positions depend on the amount of missing samples. When the number of missing samples increases, the side lobes get higher and the minima move closer to the peak at 20 m. When they fall on the signal of the bicycle, $\Delta \varphi$ decreases. When the gap size increases even more, the minima are shifted again and thus, $\Delta \varphi$ increases again. Due to this effect, $\Delta \varphi$ and $\Delta A$ are averaged over a certain gap size span. The values are given in the Tables III–VI. The IMAT algorithm performs very well up to 30 % gap size, but afterwards the estimation accuracy decreases. In case of the bicycle’s signal, the other two methods show already a high $\Delta \varphi$ for small gap sizes, see Tab. III.

## IV. MEASUREMENT VERIFICATION

For verification purpose, the IMAT algorithm is applied on a measured frequency ramp. $\mathbf { A }$ scenario with three targets is chosen, whereby one target is much smaller than the other ones. The targets are placed in close proximity.

![](images/4f75a14c388d262dc8c427f6b3dd14facbb3af673e0a34774f33fa7ff51d7351.jpg)  
Fig. 6. RMSE of the phase of the bicycle’s signal for different processing techniques.

TABLE III  
$\Delta \varphi$ OF THE BICYCLE IN RAD.
<table><tr><td rowspan=1 colspan=1>%-gap size</td><td rowspan=1 colspan=1>10-15</td><td rowspan=1 colspan=1>15-20</td><td rowspan=1 colspan=1>20-30</td><td rowspan=1 colspan=1>30-40</td><td rowspan=1 colspan=1>40-55</td></tr><tr><td rowspan=1 colspan=1>IMAT</td><td rowspan=1 colspan=1>0.03</td><td rowspan=1 colspan=1>0.03</td><td rowspan=1 colspan=1>0.03</td><td rowspan=2 colspan=1>0.080.7</td><td rowspan=3 colspan=1>0.180.70.8</td></tr><tr><td rowspan=1 colspan=1>Cosine win.</td><td rowspan=1 colspan=1>0.5</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>0.6</td></tr><tr><td rowspan=1 colspan=1>Incomplete</td><td rowspan=1 colspan=1>0.6</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>0.7</td><td rowspan=1 colspan=1>0.5</td></tr></table>

TABLE IV

$\Delta \varphi$ OF THE TRUCK IN RAD.
<table><tr><td rowspan=1 colspan=1>%-gap size</td><td rowspan=1 colspan=1>10-15</td><td rowspan=1 colspan=1>15-20</td><td rowspan=1 colspan=1>20-30</td><td rowspan=1 colspan=1>30-40</td><td rowspan=1 colspan=1>40-55</td></tr><tr><td rowspan=1 colspan=1>IMAT</td><td rowspan=1 colspan=1>0.002</td><td rowspan=1 colspan=1>0.002</td><td rowspan=1 colspan=1>0.003</td><td rowspan=1 colspan=1>0.005</td><td rowspan=2 colspan=1>0.0060.008</td></tr><tr><td rowspan=1 colspan=1>Cosine win.</td><td rowspan=1 colspan=1>0.002</td><td rowspan=1 colspan=1>0.003</td><td rowspan=1 colspan=1>0.003</td><td rowspan=1 colspan=1>0.005</td></tr><tr><td rowspan=1 colspan=1>Incomplete</td><td rowspan=1 colspan=1>0.002</td><td rowspan=1 colspan=1>0.003</td><td rowspan=1 colspan=1>0.002</td><td rowspan=1 colspan=1>0.004</td><td rowspan=1 colspan=1>0.005</td></tr></table>

TABLE V

ΔA OF THE BICYCLE IN DECIBEL.
<table><tr><td rowspan=1 colspan=1>%-gap size</td><td rowspan=1 colspan=1>10-15</td><td rowspan=1 colspan=1>15-20</td><td rowspan=1 colspan=1>20-30</td><td rowspan=1 colspan=1>30-40</td><td rowspan=1 colspan=1>40-55</td></tr><tr><td rowspan=1 colspan=1>IMAT</td><td rowspan=1 colspan=1>0.9</td><td rowspan=1 colspan=1>0.7</td><td rowspan=1 colspan=1>1.8</td><td rowspan=1 colspan=1>3.7</td><td rowspan=3 colspan=1>8.411.08.4</td></tr><tr><td rowspan=2 colspan=1>Cosine win.Incomplete</td><td rowspan=1 colspan=1>3.4</td><td rowspan=1 colspan=1>3.0</td><td rowspan=1 colspan=1>4.9</td><td rowspan=2 colspan=1>7.64.6</td></tr><tr><td rowspan=1 colspan=1>2.6</td><td rowspan=1 colspan=1>1.7</td><td rowspan=1 colspan=1>4.3</td></tr></table>

TABLE VI  
ΔA OF THE TRUCK IN DECIBEL.
<table><tr><td>%-gap size</td><td>10-15</td><td>15-20</td><td>20-30</td><td>30-40</td><td>40-55</td></tr><tr><td>IMAT</td><td>0.04</td><td>0.03</td><td>0.08</td><td>1.8</td><td>6.7</td></tr><tr><td>Cosine win.</td><td>4.5</td><td>4.5</td><td>6.5</td><td>9.5</td><td>14.2</td></tr><tr><td>Incomplete</td><td>3.5</td><td>3.4</td><td>5.3</td><td>8.1</td><td>12.5</td></tr></table>

The measured time signal in Fig. 7 is affected by interference. Removing the interfered samples leads to an incomplete signal ( ). The frequency spectrum in Fig. 8 of the interfered signal shows an increased noise floor ( ). Nulling the interfered signal part removes this noise floor ( ). However, artifacts rise around the target peaks and cover the small target with frequency 600 kHz. After the IMAT algorithm is applied ( ), the targets can be distinguished again.

## V. CONCLUSION

To mitigate the interference induced by radar sensors, which can lead to the detection failure of small close targets, the disturbed samples need to be reconstructed and not only removed. This is achieved using the sparse sampling algorithm

![](images/70fc415efe15917f7a181b9bbcbb74a680b5beba96f066eb01cb71a6ed8b6ec0.jpg)  
Fig. 7. In the interfered time domain signal ( ) the interference (black box) is removed. This results in the incomplete signal ( ).

![](images/06a36550b162d1f618f952833e220192359008af3d970d88e65dee8dd4dd320b.jpg)  
Fig. 8. The interfered spectrum has a high noise level, while the incomplete signal masks the close targets. After application of the IMAT algorithm the targets are distinguishable and at the same time the noise is at its normal level.

IMAT. It is shown that the reconstruction algorithms leads to enhanced results even in challenging scenarios. For verification the proposed procedure is applied to measurement data.

## REFERENCES

[1] D. Oprisan and H. Rohling, “Analysis of Mutual Interference between Automotive Radar Systems,” in International Radar Symposium (IRS), 2005, Berlin.

[2] M. Goppelt, H.-L. Blocher, and W. Menzel, “Analytical investigation ¨ of mutual interference between automotive FMCW radar sensors,” in German Microwave Conference (GeMIC), March 2011, pp. 1–4.

[3] T. Schipper, M. Harter, T. Mahler, O. Kern, and T. Zwick, “Discussion of the operating range of frequency modulated radars in the presence of interference,” International Journal of Microwave and Wireless Technologies, vol. 6, pp. 371–378, June 2014.

[4] G. M. Brooker, “Mutual Interference of Millimeter-Wave Radar Systems,” IEEE Transactions on Electromagnetic Compatibility, vol. 49, no. 1, pp. 170–181, Feb. 2007.

[5] C. Fischer, H.-L. Blocher, J. Dickmann, and W. Menzel, “Robust Detec-¨ tion and Mitigation of Mutual Interference in Automotive Radar,” in 16th International Radar Symposium (IRS), Jun. 2015, pp. 143–148.

[6] M. Barjenbruch, D. Kellner, K. Dietmayer, J. Klappstein, and J. Dickmann, “A Method for Interference Cancellation in Automotive Radar,” in IEEE MTT-S International Conference on Microwaves for Intelligent Mobility (ICMIM), April 2015, pp. 1–4.

[7] F. Marvasti, M. Azghani, P. Imani, P. Pakrouh, S. Heydari, A. Golmohammadi, A. Kazerouni, and M. Khalili, “Sparse Signal Processing Using iterative Method with Adaptive Thresholding (IMAT),” in 19th International Conference on Telecommunications (ICT), April 2012.

[8] D. Belgiovane and C. C. Chen, “Bicycles and Human Riders Backscattering at 77 GHz for Automotive Radar,” in 10th European Conference on Antennas and Propagation (EuCAP), April 2016, pp. 1–5.

[9] F. Marvasti, A. Amini, F. Haddadi, M. Soltanolkotabi, B. H. Khalaj, A. Aldroubi, S. Holm, S. Sanei, and J. A. Chambers, “A Unified Approach to Sparse Signal Processing,” CoRR, vol. abs/0902.1853, 2009. [Online]. Available: http://arxiv.org/abs/0902.1853