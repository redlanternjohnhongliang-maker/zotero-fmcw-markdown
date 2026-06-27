# Automotive Radar Interference Avoidance Strategies for Complex Traffic Scenarios

Lizette Lorraine Tovar Torres<sup>1</sup>, Timo Grebner, Christian Waldschmidt Institute of Microwave Engineering, Ulm University, 89081 Ulm, Germany <sup>1</sup>lizette.tovar-torres@uni-ulm.de

Abstract—The issue of interference between automotive radars is an emerging topic. Although different interference suppression techniques and mitigation approaches have been previously studied, none of them have been evaluated considering complex traffic scenarios where multiple vehicles are equipped with several radar sensors. This paper presents two different interference avoidance strategies: Random Frequency Hopping with Sub-Channels and the Compass Method. The effectiveness of the strategies is evaluated by simulating two complex scenarios: A highway with 105 vehicles and an intersection of two streets with 34 vehicles, each vehicle containing five radar sensors. Subsequently, the strategies are validated by taking measurements considering the intersection of two streets.

Index Terms—Automotive radar, interference, mitigation, simulation.

## I. INTRODUCTION

Automotive radar sensors are widely used in Advanced Driver Assistance Systems due to their robustness under adverse weather and poor light conditions. To provide 360° coverage of the vehicle’s surroundings, the vehicle must be equipped with several radar sensors [1]. Nevertheless, the performance of the sensors can be seriously compromised when considering real traffic scenarios, where multiple sensors can interfere with each other.

Considering the well-known chirp-sequence modulation scheme, interference occurs when the signals transmitted by two or more radars overlap in frequency, time, and field of view. Interference affects the reliability of the victim sensor by generating ghost targets and increasing the noise floor [2], which compromises the detection of weak targets like pedestrians.

The problem of interference between automotive radars has been widely studied in the past years and different approaches based on, e.g., detection and reconstruction of the affected signal samples [3], signal separation [4], adaptive beamforming [5], and the variation of the waveform parameters [6], [7] have been proposed. However, the effectiveness of those approaches has not been verified in complex scenarios where multiple radars are present.

This paper compares the performance of two new avoidance strategies: Random Frequency Hopping with Sub-Channels and the Compass Method. The comparison is done by considering real traffic scenarios where each vehicle is equipped with five radar sensors. The simulation of a highway with six traffic lanes and 105 vehicles is carried out using an interference simulator developed in Matlab. Furthermore, the intersection

of two streets with 34 vehicles and a total of four traffic lanes is also simulated. A statistical analysis of the interference effects after applying the avoidance strategies is performed by running the scenarios several times under the very same conditions but using different sensor parameters. Furthermore, for the first time, the proposed strategies are evaluated by taking measurements of a complex traffic scenario representing the intersection of two streets.

## II. INTERFERENCE SIMULATOR

The effects of the interference can significantly vary depending on the scenario configuration and sensor waveform parameters of the radars. Previous studies consider simple scenarios where one victim radar and one interfering sensor are placed in front of each other, working at similar frequency bands and at the same time. These studies evaluate the performance of the mitigation strategy considering just one affected chirp or taking into account one frame of transmitted chirps. Still, those strategies are not evaluated using actual time-variant scenarios where not one, but multiple sensors with different waveform parameters could interfere with each other.

This work uses the fast interference simulator presented in [8]. The simulator is able to recreate complex traffic scenarios involving several vehicles with multiple potential interferer radars. A selected scenario can be run several times under the same conditions, making it possible to fairly compare the different avoidance strategies [8]. The simulator models the targets and the channel to reproduce the interfering signals and the echo signals coming from targets. Vehicles are represented using clouds of scattering centers and shadowing effects due to obstacles located in the line of sight (LoS) of the victim radar are considered. It is worth mentioning that, unlike the simulations performed in previous works, the simulator includes a predefined catalog of sensors with different waveform parameters and directional antenna radiation patterns suited for LRR, MRR, and SRR sensors (which satisfy the requirements of [9]). The simulator models the intermediate frequency (IF) time domain signals of the targets according to [10] and the IF interfering signals as stated by [8]. The generated raw data passes through the usual signal processing chain resulting in a list containing the range, velocity, and azimuth angle of the estimated targets. Furthermore, the noise floor level is calculated from the range-velocity spectrum as an evaluation criterion of interference.

![](images/68725c519c9677bcfa378dc00457b7a4b8098c305cf1a5024d6107a3ee3872c6.jpg)  
Fig. 1. Transmitted victim chirps (black) and interferer chirps (red). The interference is observed in the first victim chirp within the interval $[ t _ { I _ { i } } , t _ { I _ { f } } ] ,$ while in the second chirp no interference is present. The center frequency $\dot { \boldsymbol f } _ { c } ,$ bandwidth B, chirp duration $T _ { c }$ , and chirp repetition time $T _ { r }$ of the sensors are depicted in the figure. B<sub>RX</sub> represents the receiver bandwidth, which is determined by the IF filter. Note that the subscript $^ { \ast } V ^ { \ast }$ refers to the victim sensor parameters and $\cdot \boldsymbol { I ^ { \ast } }$ to the interferer sensor parameters.

The simulator considers time-variant scenarios by dividing the total simulation time into simulation steps. One simulation step consists of the interpretation of the selected scenario, the generation of the corresponding IF signals, as well as the application of the radar signal processing chain and the evaluation of the interference effects.

Additionally, as presented in [11], the simulator is able to choose between two propagation models. The Line-of-Sight Model is the fastest and straightforward approach to model the channel, while the Two-Path Propagation Model considers the superposition of the LoS and two-path signal components of the interfering signals by modeling a roughness factor and the Fresnel reflection coefficient of the asphalt at 77 GHz.

Given that the power of the IF signal of the interferer is directly proportional to the antenna gain of the victim $G _ { V }$ and the interferer $G _ { I }$ , and inversely proportional to the square of the path distance R [11], additional reflections caused by multi-path propagation are weaker (lower $G _ { V }$ , lower $G _ { I }$ and larger R) than the LoS signal and the ground-reflected signal components. Consequently, multi-path reflections are neglected and the computational burden of the simulation is reduced.

## III. INTERFERENCE AVOIDANCE STRATEGIES

The effects of the interference depend on the scenario configuration and the sensor parameters of the involved radars. Then, if the signals transmitted by two different radar sensors overlap in frequency, time, and field of view (FoV), there is a high probability of interference between the sensors. The interference duration is proportional to the quotient between the receiver bandwidth of the victim radar $B _ { \mathrm { R X } }$ and the difference between the slopes $\Delta \mu$ of the victim and interfering sensors (Fig.1). According to [2], ghost targets are prone to happen if the frequency ramps of the victim and the interferer are in parallel $( \Delta \mu = 0 )$ . On the other hand, if the frequency ramps cross each other $( \Delta \mu \neq 0 )$ , an increased noise floor level is expected. Considering the latest case, a larger number of affected samples is expected when the victim sensor has a large $B _ { \mathrm { R X } }$ or if $| \Delta \mu |$ is low.

![](images/747dd8810c77c162fe362bc05a912961ca868742dc62b13d43518668a1c8ab6b.jpg)  
Fig. 2. Example considering $f _ { \mathrm { d o w n } } = 7 7 \mathrm { G H z } ,$ $f _ { \mathrm { u p } } { = } 8 1 \mathrm { G H z } ,$ $N = 4 ,$ $B _ { \mathrm { c h } } = 1 \mathrm { G H z }$ and five sensors with $B \leq B _ { \mathrm { c h } } .$ . The $f _ { c }$ of each sensor is updated if the previous frame is affected by interference. In practice, a new $f _ { c } ^ { \prime }$ is set after 250 ms at the latest.

The proposed avoidance strategies explore the division of the available spectrum into sub-channels. A predefined frequency band with lower and upper frequency boundaries $f _ { \mathrm { d o w n } }$ and $f _ { \mathrm { u p } }$ is divided into N sub-channels, each one with bandwidth $\dot { B _ { \mathrm { c h } } } = ( f _ { \mathrm { u p } } - f _ { \mathrm { d o w n } } ) / N$ . Then, if the sensor detected interference in the previous frame and if the bandwidth B fulfills

$$
B \leq B _ { \mathrm { c h } } ,\tag{1}
$$

the sensor is allocated to a frequency channel and the center frequency reassignment process takes place.

The advantage of these strategies is that they highly reduce the interference from the very beginning, avoiding the computational effort of post-processing of a corrupted signal.

## A. Random Frequency Hopping with Sub-Channels (RFH)

Given a desired number of sub-channels $N .$ , this avoidance strategy defines the lower and upper frequency boundaries for each sub-channel n as

$$
f _ { \mathrm { c h _ { d o w n } } } = f _ { \mathrm { d o w n } } + B _ { \mathrm { c h } } ( n - 1 ) \mathrm { ~ w i t h ~ } n \in \mathbb { Z } : n \in [ 1 , N ] ,\tag{2}
$$

$$
f _ { \mathrm { c h } _ { \mathrm { u p } } } = f _ { \mathrm { c h } _ { \mathrm { d o w n } } } + B _ { \mathrm { c h } } .\tag{3}
$$

Then, if the (1) is accomplished, the channel assignment is performed according to

$$
n = \left\lfloor { \frac { f _ { c } - f _ { \mathrm { d o w n } } } { B _ { \mathrm { c h } } } } \right\rfloor + 1 .\tag{4}
$$

Once the sensor is assigned to a sub-channel, the random frequency hopping process starts by selecting a new $f _ { c } ^ { \prime }$ within the assigned channel. This selection is done by ensuring that the sensor bandwidth is still being contained in the channel

$$
f _ { \mathrm { c h } _ { \mathrm { d o w n } } } \leq f _ { c } ^ { \prime } - 0 . 5 B , \quad f _ { \mathrm { c h } _ { \mathrm { u p } } } > f _ { c } ^ { \prime } + 0 . 5 B .\tag{5}
$$

Figure 2 shows the working principle of the algorithm. Here, four sub-channels of 1 GHz bandwidth are considered. After a certain time, the center frequency of the sensors $f _ { c }$ is relocated independently within the corresponding channel. As a result, the mutual interference caused during the first frame between sensors 1-2 and 4-5 is avoided in the subsequent frames. However, it becomes likely to get interference between sensors 2 and 3, since they are assigned to the same channel.

![](images/1bbcd29a73b5788583ed3daa30cd87059fa061ae7cb668436801c067d6f13b90.jpg)  
Fig. 3. Example considering $f _ { \mathrm { d o w n } } = 7 7 \mathrm { G H z } ,$ $f _ { \mathrm { u p } } { = } 8 1 \mathrm { G H z }$ $N = 4 ,$ $B _ { \mathrm { c h } } = 1$ GHz and assuming that for all corner sensors $B \leq B _ { \mathrm { c h } }$ and $f _ { \mathrm { d o w n } } ^ { \mathrm { v n } } < f _ { c } \leq f _ { \mathrm { u p } } .$ The boresight direction of each sensor is depicted in orange and the selected channel is written in red. The frontal sensors are LRR with $7 6 \mathrm { G H z } < f _ { c } \leq 7 7 \mathrm { G H z }$ , therefore their $f _ { c }$ is not modified.

This example shows the potential of the algorithm when $N = 4$ and $B \leq B _ { \mathrm { c h } } = 1 \mathrm { G H z }$ . Nonetheless, sensors with bandwidths up to 4 GHz could be present in real traffic scenarios. Therefore, for this kind of sensors it was determined to randomly set $f _ { c } ^ { \prime }$ to 78.5 GHz or 79.5 GHz for sensors with $1 \mathrm { G H z } < B \leq 2 \mathrm { G H z } ,$ , and to set $f _ { c } ^ { \prime } { = } 7 9 \mathrm { G H z }$ for sensors with $2 \mathrm { G H z } < B \leq 4 \mathrm { G H z } .$

## B. Compass Method (CM)

This strategy performs the channel assignment by considering the sensor boresight angle α with respect to the cardinal directions. In this case, if the (1) is accomplished, the lower frequency boundary for each sub-channel is defined by

$$
f _ { \mathrm { c h } _ { \mathrm { d o w n } } } = f _ { c _ { \mathrm { B a n d } } } + \left( \left\lfloor \frac { \alpha + \pi } { 2 \pi } N \right\rfloor - \frac { N - 1 } { 2 } \right) B _ { \mathrm { c h } } - \frac { B _ { \mathrm { c h } } } { 2 } ,\tag{6}
$$

where $f _ { c _ { \mathrm { B a n d } } } = f _ { \mathrm { d o w n } } + 0 . 5 ( f _ { \mathrm { u p } } - f _ { \mathrm { d o w n } } )$ and $\alpha \in ( - \pi , \pi ]$ , while $f _ { \mathrm { c h _ { u p } } }$ is given by (3). Similar to the previous approach, a new $f _ { c } ^ { \prime }$ is randomly set within the assigned channel while ensuring that (5) is fulfilled.

An example when considering four sub-channels of 1 GHz bandwidth is depicted in Fig. 3. Here, it is assumed that the corner sensors are SRR/MRR with $B { \le } 1 \mathrm { G H z }$ and $7 7 \mathrm { G H z } < f _ { c } \leq 8 1$ GHz, while the frontal sensors are LRR/MRR whose $f _ { c }$ is not modified, since $f _ { c } \notin [ f _ { \mathrm { d o w n } } , f _ { \mathrm { u p } } ]$ This last assumption is valid considering that currently there is a large number of LRR sensors circulating on the streets and that they do not perform any interference avoidance technique. For sensors with $B { > } 1 \mathrm { G H z }$ , the same procedure as in III-A is applied.

The main advantage of the compass method is that it removes the strongest component of the interference that is caused by other radar sensors that are in the LoS of the victim.

## IV. SIMULATION RESULTS

Two scenarios are simulated for 20 s using vehicles equipped with one frontal LRR/MRR and four SRR/MRR corner sensors with bandwidths up to 4 GHz, different values of $f _ { c }$ and different chirp rates $\mu = B / T _ { c }$ . Table I presents a summary of the used sensor parameters. The first scenario considers a highway with six traffic lanes and 105 vehicles, while the second represents the intersection of two streets with 34 vehicles and a total of four traffic lanes. The selection of the scenarios is done considering the corner cases of [12]. Then, the highway is chosen as an example of a traffic situation with low sensor density and high dynamism, while the intersection represents a traffic situation with a high sensor density and low dynamism. More information of the selected scenarios is presented in [13].

TABLE I  
SENSOR PARAMETERS. IT IS ASSUMED THAT ALL THE SENSORS TRANSMIT THE SAME POWER OF 10 dBm.
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>LRR/MRR</td><td rowspan=1 colspan=1>SRR/MRR</td></tr><tr><td rowspan=1 colspan=1>Freq. Band (GHz)</td><td rowspan=1 colspan=1>76-77</td><td rowspan=1 colspan=1>77-81</td></tr><tr><td rowspan=1 colspan=1>|µ| (MHz/µs)</td><td rowspan=1 colspan=1>3-44</td><td rowspan=1 colspan=1>15-100</td></tr><tr><td rowspan=1 colspan=1>B (GHz)</td><td rowspan=1 colspan=1>0.1-1</td><td rowspan=1 colspan=1>0.2-4</td></tr><tr><td rowspan=1 colspan=1>BRx (MHz)</td><td rowspan=1 colspan=1>5-15</td><td rowspan=1 colspan=1>5-15</td></tr><tr><td rowspan=1 colspan=1>±FoV azi (°)</td><td rowspan=1 colspan=1>10- 30</td><td rowspan=1 colspan=1>30-80</td></tr><tr><td rowspan=1 colspan=1>EIRP (dBm)</td><td rowspan=1 colspan=1>30-40</td><td rowspan=1 colspan=1>20-30</td></tr></table>

Each scenario is run 420 times, each time assigning different sensor parameters to each radar. The effects of the interference and the proposed methods are evaluated taking into account one radar sensor as the victim. Every run is divided into simulation steps with the duration of one frame of the victim radar. The noise level is measured from the range-velocity spectrum of each radar frame (simulation step) of the selected victim sensor. This is done by taking the average of the rangevelocity cells, which do not contain the information of the targets.

For each run, five simulation cases are carried out in parallel using exactly the same setup (sensor parameters, vehicles positions and vehicles’ velocities). The first case considers the scenario without interference and is run to get the ground truth for the noise level of the selected victim sensor. In the second simulation case, the scenario is simulated considering that all the sensors in the scenario are active and that no countermeasure is acting, so they potentially interfere with the victim radar. The next two cases assess the scenario using the random frequency hopping approach with $N = 1$ and N = 4. Note that the simulation case of the random frequency hopping approach with N = 1 corresponds to the method of random frequency shifting after the detection of interference that is addressed in [6], but applied to a complex traffic scenario. The last simulation case evaluates the scenario when using the compass method for N = 4. In order to fairly compare the random frequency hopping approach and the compass method, both cases are simulated for $f _ { \mathrm { d o w n } } = 7 7 \mathrm { G H z }$ and $f _ { \mathrm { u p } } { = } 8 1 \mathrm { G H z } .$

![](images/257c03109a6a138711cd742f25d1b0b358378787e0dff008dbacb47e806ba49c.jpg)  
Fig. 4. Interference-induced noise floor (IINF) for the highway and the intersection scenarios. Each scenario is run 420 times. The interference effects are evaluated considering 14 different SRR/MRR victim sensors.

The effectiveness of the algorithms is evaluated by comparing the percentage of simulation steps with $0 , 1 , 2 , . . . , 2 0 \mathrm { d B }$ interference-induced noise floor increase (IINF) for the different simulation cases. The results are presented in Fig. 4 using histograms. The y-axis refers to the percentage of simulation steps related to the simulated time of $2 0 \mathrm { s }$ and considers that one simulation step corresponds to the victim’s frame duration. The red bars show the noise floor increase considering that all the sensors in the scenario are active without any kind of suppression technique. The blue and purple bars present the results when using the random frequency hopping approach with $N = 1$ and $N = 4 ,$ , respectively. Finally, the result of the compass method for $N = 4$ is depicted in yellow. A high value of simulation steps with 0 dB is desired since it implies that the interference is not affecting for a long time.

From the figure it can be observed that when no interference avoidance strategy is applied (red), just 48.6% of the simulation steps are not affected by interference for the highway scenario, while for the intersection this corresponds to 45.4% of the simulation steps. Furthermore, it can be seen that there is no improvement when the random frequency hopping is applied using a single channel. However, when the number of sub-channels increases to $N = 4$ , the number of steps without interference rises. This shows that the use of sub-channels is favorable. Finally, it is visible that the largest percentage of simulation steps without interference (0 dB IINF) is obtained when using the compass method (72.6% for the highway scenario and 66.3% for the intersection scenario).

For completeness, the distribution of the number of interfering sensors affecting the victim sensor is plotted for the different cases in Fig. 5. The discrete data is connected by dashed lines for illustration purposes. Similar to the previous figure, the y-axis refers to the percentage of simulation steps related to the simulated time. In principle, it is desired to have a large percentage of simulation steps with a low number of interfering sensors. For the highway scenario, it is observed that when no interference avoidance is applied ( ), the percentage of simulation steps with a low number of interfering sensors is very low. As the red curve grows, a larger percentage of simulation steps are affected by a larger amount of interfering sensors. After reaching the maximum, the percentage of simulation steps decreases while the number of interfering sensors increases. The reason why the maximum number of interfering sensors is constant for all the simulated cases, comes from the fact that the simulation considers sensors with $B > 1 \mathrm { G H z }$ and those sensors are not assigned to a single channel. As expected, when applying the avoidance techniques, the curve is shifted to the upper left side of the graph, indicating that there are more simulation steps with a lower number of interfering sensors affecting the victim sensor. A similar behavior is presented in the intersection scenario. Consequently, the compass method ( ) exhibits the best performance in both scenarios.

![](images/ab5716c61620d30766dcae1de0ff9c884b62247d23bcb0a29f60f18a7c8f19d1.jpg)  
Fig. 5. Number of interfering sensors affecting the victim sensor before (no suppression ) and after applying the interference avoidance techniques (RFH with $N = 1 \mathsfit { O }$ , RFH with ${ \bar { N } } = { \bar { 4 } } \ 0 ,$ and CM with $N = 1 \mathrm { ~ O ~ } )$

## V. MEASUREMENT RESULTS

A simplified scenario representing the intersection of two streets is chosen. For this purpose, seven MRR/SRR radar sensors are used. The measurement setup is depicted in Fig. 6. The first radar sensor (S1) is mounted as a corner sensor in a moving vehicle, while the other six sensors are static. S2, S3,

![](images/fc3c4fd6e0012a739f295305229e88d1ae69b574871d5448fa524bcc29043d4b.jpg)  
Fig. 6. Measurement setup. The vehicle containing S1 turns to the right while the other 6 sensors are static. Sensors placed in the same vehicle share the same sensor parameters and are finely synchronized to avoid mutual interference.

S6 and S7 represent the corner sensors placed at the frontal part of the two static vehicles that wait in the horizontal lanes. Similarly, S4 and S5 represent the two rear corner sensors of a static vehicle in the vertical lane. It is assumed that each pair of corner sensors S2-S3, S4-S5 and S6-S7 have exactly the same parameters but do not interfere because a time delay is introduced in such a way that they do not transmit at the same time. Furthermore, it is considered that all the sensors are 3x4 MIMO radars that transmit 128 chirps, with a transmitter power $P _ { T } = 1 0 \mathrm { d B m }$ , maximum antenna gain $G = 1 2 \mathrm { d B i }$ , and receiver bandwidth $B _ { \mathrm { R X } } { = } 5 \mathrm { M H z }$ . The center frequencies and the slope of the sensors when considering B = 1 GHz are summarized in the figure.

For the first measurement, all the sensors are configured with $B { = } 1 \mathrm { G H z }$ in order to test the methods with maximum channel occupancy. Figure 7 shows the IINF for each frame at each sensor. With the purpose of getting an idea of the maximum IINF boundaries, an additional no-suppression case where all the sensors use $f _ { c } = 7 8 . 5 \mathrm { G H z }$ is included in black. Note that the case of random frequency hopping with N = 1 is omitted because of its limited performance. The influence of the moving vehicle is visible in the S1, S4 and S5 plots for the no mitigation cases between the 60th and 100th frames. During this time window, the IINF increases while the vehicle approaches the intersection and then decreases when it turns to the right. It is observed that, when using the random frequency hopping with $N = 4 ,$ , the interference in S1 is completely suppressed, while there is still interference between S2, S3, S4 and S5 since they are assigned to the same channel $( f _ { \mathrm { c h _ { d o w n } } } = 7 8 \mathrm { G H z } )$ . On the other hand, when the compass method is used, all the sensors are assigned to different channels and the interference is completely suppressed (IINF ≈ 0 dB).

A second measurement is performed and the IINF for each frame at each sensor is depicted in Fig. 8. Here, the bandwidth of S6 and S7 is increased to $B { = } 2 \mathrm { G H z }$ , while all the other sensor parameters are the same as in the first measurement. Consequently, the algorithms set $f _ { c }$ randomly to 78.5 GHz or 79.5 GHz instead of assigning a unique channel. This explains the fluctuating IINF for S6-S7 when applying the two methods. Although the interference is not completely suppressed in S2- S7, the figures show that when using the proposed methods, the average IINF for the 150 frames is lower than the average when considering the no suppression cases (Table II). This demonstrates that there is still an improvement even when the involved radars have larger bandwidths. Furthermore, it is observed that the lowest average IINF for the 150 frames is obtained when using the compass method.

![](images/0e102f32718ba09fbc6b883d66bd0b7020b0547accd4589aa51eee0eafbd3bcc.jpg)  
Fig. 7. Interference-induced noise floor (IINF) for each sensor at each frame of the first measurement. Here all the sensors use $B { = } 1 \mathrm { G H z }$

![](images/7e317866bbb9bfe0ae13c20c65f1fd327b1fdb9fd7bf762ed8fd7fc0f88f98bd.jpg)

![](images/a6e9f1544a404f210bfdb69820e0c7f1fd96d2cea52483c18c9b9c4cf52b9622.jpg)

![](images/5cee1ce3e2b78a1a337271fde44f07d2dc6c48ba51db27d27b4168e8edb92b26.jpg)

![](images/b2004dffed9e8164c5cbd6246a13a9d38863d3fe530055bf0b210d1e139e3284.jpg)

![](images/7ebd9765b809abc17c6575bfd311a31f185d76a387eed7783491b8870ae00d80.jpg)

![](images/50d8a766779e665a40b09c3f4615f08bba74d65f4ebc83772289eb4d28f934c8.jpg)

![](images/f46af92e12c0e95d6bcb3668a54cdf53d69dd60ac896fef508fd8afebf16a664.jpg)  
Fig. 8. Interference-induced noise floor (IINF) for each sensor at each frame of the second measurement. Here, sensor 6 and sensor 7 use $B { = } 2 \operatorname { G H z }$

## VI. CONCLUSION

This work presented two avoidance strategies: the Random Frequency Hopping with Sub-Channels and the Compass Method. A highway and the intersection of two streets were simulated considering vehicles equipped with five radar sensors. The evaluation was performed by running the scenarios 420 times, each time using different sensor parameters. Moreover, for the first time, measurements were taken considering a real traffic scenario representing the intersection of two streets. It was proved that the Random Frequency Hopping without sub-channels does not reduce the interference levels. However, when using four sub-channels, the number of simulation steps without interference increases. Although this strategy works, the simulations and the measurements showed that the Compass Method has the best performance with the lowest values of IINF. This method is an attractive option to mitigate the interference since it is a simple way to counteract the strongest component of the interference.

TABLE II  
AVERAGE IINF FOR SECOND MEASUREMENT.
<table><tr><td rowspan=1 colspan=1>Case</td><td rowspan=1 colspan=1>S6</td><td rowspan=1 colspan=1>S7</td></tr><tr><td rowspan=1 colspan=1>No suppression, same $f _ { c }$ </td><td rowspan=1 colspan=1>15 dB</td><td rowspan=1 colspan=1>13 dB</td></tr><tr><td rowspan=1 colspan=1>No suppression</td><td rowspan=1 colspan=1>13 dB</td><td rowspan=1 colspan=1>10 dB</td></tr><tr><td rowspan=1 colspan=1>RFH $\overline { { N = 4 } }$ </td><td rowspan=1 colspan=1>11 dB</td><td rowspan=1 colspan=1>9dB</td></tr><tr><td rowspan=1 colspan=1>CM  $N = 4$ </td><td rowspan=1 colspan=1>6 dB</td><td rowspan=1 colspan=1> $0 . 3 \mathrm { d B }$ </td></tr></table>

## ACKNOWLEDGMENT

The authors sincerely thank the German Federal Ministry of Education and Research for funding this research in the project IMIKO-Radar (German: Interferenzminimierung durch Kooperation bei Radarsensoren, grant: 16EMO0345).

## REFERENCES

[1] F. Roos, J. Bechter, C. Knill, B. Schweizer, and C. Waldschmidt, “Radar sensors for autonomous driving: Modulation schemes and interference mitigation,” IEEE Microwave Mag., vol. 20, no. 9, pp. 58–72, Sep. 2019.

[2] D. Oprisan and H. Rohling, “Analysis of mutual interference between automotive radar systems,” in Proc. Int. Radar Symp. (IRS), 2005, pp. 83–90.

[3] J. Bechter, F. Roos, M. Rahman, and C. Waldschmidt, “Automotive radar interference mitigation using a sparse sampling approach,” in Proc. European Radar Conf. (EURAD), Oct. 2017, pp. 90–93.

[4] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019.

[5] J. Bechter, M. Rameez, and C. Waldschmidt, “Analytical and experimental investigations on mitigation of interference in a DBF MIMO radar,” IEEE Trans. Microw. Theory Techn., vol. 65, no. 5, pp. 1727–1734, May 2017.

[6] J. Bechter, C. Sippel, and C. Waldschmidt, “Bats-inspired frequency hopping for mitigation of interference between automotive radars,” in Proc. IEEE MTT-S International Conf. on Microwaves for Intelligent Mobility (ICMIM), May 2016, pp. 1–4.

[7] F. Norouzian, A. Pirkani, E. Hoare, M. Cherniakov, and M. Gashinova, “Automotive radar waveform parameters randomisation for interference level reduction,” in Proc. IEEE Radar Conf. (RadarConf20), Sep. 2020, pp. 1–5.

[8] L. Tovar Torres, F. Roos, and C. Waldschmidt, “Simulator design for interference analysis in complex automotive multi-user traffic scenarios,” in Proc. IEEE Radar Conf. (RadarConf20), Sep. 2020, pp. 1–6.

[9] J. Hasch, E. Topak, R. Schnabel, T. Zwick, R. Weigel, and C. Waldschmidt, “Millimeter-wave technology for automotive radar sensors in the 77 GHz frequency band,” IEEE Trans. Microw. Theory Techn., vol. 60, no. 3, pp. 845–860, March 2012.

[10] V. Winkler, “Range doppler detection for automotive FMCW radars,” in Proc. European Radar Conf. (EuRAD), Oct. 2007, pp. 166–169.

[11] L. Tovar Torres, M. Steiner, and C. Waldschmidt, “Channel influence for the analysis of interferences between automotive radars,” in Proc European Radar Conf. (EuRAD), Jan 2021, pp. 266–269.

[12] W. Sorgel, T. Poguntke, and T. Binzer, “IMIKO-Radar: Towards cooperative radar-interference mitigation,” Automotive Forum, 16th European Microwave Week, Oct 2019.

[13] L. Tovar Torres and C. Waldschmidt, “Analysis of automotive radar interference in complex traffic scenarios using graph theory,” in Proc. Int. Radar Symp. (IRS), Sep. 2022, pp. 269–274.