# Score-based Generative Modeling for Interference Mitigation in Automotive FMCW Radar

Citation for published version (APA):   
Wei, X., Overdevest, J., Li, J., Youn, J., Ravindran, S., & Van Sloun, R. J. G. (2024). Score-based Generative Modeling for Interference Mitigation in Automotive FMCW Radar. In (pp. 27-30). Article 10734954 Institute of Electrical and Electronics Engineers.   
https://doi.org/10.23919/EuRAD61604.2024.10734954

Document license: TAVERNE

DOI: 10.23919/EuRAD61604.2024.10734954

Document status and date: Published: 04/11/2024

Document Version: Publisher’s PDF, also known as Version of Record (includes final page, issue and volume numbers)

Please check the document version of this publication:

• A submitted manuscript is the version of the article upon submission and before peer-review. There can be important differences between the submitted version and the official published version of record. People interested in the research are advised to contact the author for the final version of the publication, or visit the DOI to the publisher's website.

• The final author version and the galley proof are versions of the publication after peer review.

• The final published version features the final layout of the paper including the volume, issue and page numbers.

Link to publication

## General rights

Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright owners and it is a condition of accessing publications that users recognise and abide by the legal requirements associated with these rights.

• Users may download and print one copy of any publication from the public portal for the purpose of private study or research.

• You may not further distribute the material or use it for any profit-making activity or commercial gain

• You may freely distribute the URL identifying the publication in the public portal.

If the publication is distributed under the terms of Article 25fa of the Dutch Copyright Act, indicated by the “Taverne” license above, please follow below link for the End User Agreement:

www.tue.nl/taverne

## Take down policy

If you believe that this document breaches copyright please contact us at:

openaccess@tue.nl

providing details and we will investigate your claim.

# Score-based Generative Modeling for Interference Mitigation in Automotive FMCW Radar

Xinyi Wei<sup>#</sup>, Jeroen Overdevest<sup>\$</sup>, Jun Li<sup>&</sup>, Jihwan Youn<sup>&</sup>, Satish Ravindran<sup>&</sup>, Ruud J.G. van Sloun<sup>#</sup>

<sup>#</sup>Eindhoven University of Technology, The Netherlands

<sup>\$</sup>NXP Semiconductors, The Netherlands

<sup>&</sup>NXP Semiconductors, USA

{x.wei, R.J.G.v.Sloun}@tue.nl {jeroen.overdevest, jun.li\_5, jihwan.youn, satish.ravindran}@nxp.com,

Abstract — Automotive radar interference is a growing problem as automotive radars proliferate in advanced driver assistance systems and autonomous driving. Numerous studies have been proposed to address interference mitigation based on hand-crafted priors, like sparsity-based techniques, or through purely data-driven approaches. However, their effectiveness is often compromised when these representations fail to accurately reflect the statistical characteristics of the interfering radar parameters in dynamic scenarios. In this work, we propose a new method that treats interference mitigation as a source separation problem. We leverage score-based generative networks to explicitly learn the interfering radar parameters. These learned parameters are subsequently combined with Maximum-a-posteriori estimation, allowing for an algorithm with enhanced performance. We demonstrate that our algorithm outperforms the baselines in signal-to-noise ratio.

Keywords — FMCW, maximum-a-posteriori, source separation, generative score-based networks, sparsity

## I. INTRODUCTION

In today’s world, automotive frequency-modulated continuous wave (FMCW) radars are extensively used in daily traffic as a crucial part of Advanced Driver Assistance Systems. FMCW radars determine both the distance and velocity of moving targets by analyzing the reflected linear frequency-modulated waves. However, as the popularity of automotive radar adoption grows, the probability of mutual interference among these systems also rises. Such interference can increase the noise floor, consequently resulting in reduced detection performance or even the generation of undesired ghost targets [1]. Therefore, many studies have been concentrated on exploring algorithms for mitigating interference in automotive radars.

One primary strategy of interference mitigation in the field of radar systems encompasses post-signal processing at the receiver end. A conventional technique, known as model-based interference detection and cancellation [2]–[5], is designed to detect and remove interference-contaminated signal samples. However, this approach risks compromising the integrity of target signals, as a potential overlap between interference and targets may unintentionally result in the loss of crucial information.

To enhance the preservation of target signals, extensive research has been directed towards source separation techniques as a means of mitigating interference. This research leverages hand-crafted statistical properties of both target and interference signals within well-defined domains as foundational priors [6]–[10]. These carefully selected priors then aid in separating target signals from interference. However, the inherent complexity of interference’s statistical nature can undermine these efforts, occasionally resulting in suboptimal performance under dynamic conditions.

Meanwhile, deep learning is increasingly explored in radar systems for mitigating interference, particularly due to its exceptional capabilities in signal restoration. This has led to the development of numerous methods [11]–[14]. These methods typically utilize an end-to-end supervised learning model, deploying networks designed to handle input-output pairs within identical or varied domains. While advancements have been made, it prompts a research question of whether the application of deep learning for modeling complicated interference parameters can be explored by shifting towards more explicit learning strategies.

In light of these considerations, we introduce a novel method that recasts interference mitigation as a source separation problem, ensuring the preservation of target signal integrity. Departing from conventional hand-crafted assumptions, our method utilizes the power of deep generative networks to learn the interference structure from training data. We specifically employ score-based generative networks [15], noted for their remarkable performance in addressing inverse problems across various fields [16], [17]. By incorporating explicitly learned knowledge as a foundational prior within our optimization algorithm, we gain the efficiency of interference mitigation. In the following sections, we will elaborate on the algorithm and demonstrate the benefits of employing such explicitly learned priors.

## II. ALGORITHM FOR INTERFERENCE MITIGATION

## A. Problem Formulation

Consider a typical FMCW automotive radar system. The received signal with interference post-ADC [5] can be modeled as:

$$
\mathbf { y } = \mathbf { x } _ { \mathrm { t a r } } + \mathbf { x } _ { \mathrm { i n t } } + \mathbf { n } ,\tag{1}
$$

where $\mathbf { y } \in \mathbb { R } ^ { l }$ represents the observed time series consisting of l signal samples, $\mathbf { x } _ { \mathrm { t a r } } \in \mathbb { R } ^ { l }$ is the target signal, $\mathbf { x } _ { \mathrm { i n t } } \in \mathbb { R } ^ { l }$ is the interference, and $\mathbf { n } \in \mathbb { R } ^ { l }$ denotes additive Gaussian noise. The challenge lies in accurately detecting $\mathbf { x } _ { \mathrm { t a r } }$ with the presence of aggressive interference $\mathbf { x } _ { \mathrm { i n t } }$ . Without knowledge of the signal structure and statistics of $\mathbf { x } _ { \mathrm { t a r } }$ and $\mathbf { x } _ { \mathrm { i n t } } ,$ this is an ill-conditioned problem, which we will address via Maximum-a-Posteriori (MAP) estimation. It can be formulated as:

$$
\begin{array} { r l } & { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } = \underset { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } } { \arg \operatorname* { m a x } } p \left( \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } | \mathbf { y } \right) } \\ & { \qquad \propto \underset { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } } { \arg \operatorname* { m a x } } p \left( \mathbf { y } \vert \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } \right) \cdot p \left( \mathbf { x } _ { \mathrm { i n t } } \right) \cdot p \left( \mathbf { x } _ { \mathrm { t a r } } \right) , } \end{array}\tag{2}
$$

where $p ( \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } | \mathbf { y } )$ represents the joint posterior distribution and $p ( \mathbf { y } | \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } )$ is the measurement likelihood model. In our framework, the prior for the target signal, $p ( \mathbf { x } _ { \mathrm { t a r } } )$ , is modeled as a Laplacian distribution in the range spectrum, assuming sparsity. On the other hand, the prior of the interference, $p ( \mathbf { x } _ { \mathrm { i n t } } )$ , is modeled in the magnitude time-frequency domain using a score-based generative network, as the interference presents more structure in this domain compared to its representation in the time domain. These priors are then used in an iterative optimization scheme, aiming to separate the two signals from the observation using their distinct statistical characteristics reflected by the priors. We thus rewrite (2) as:

$$
\hat { \mathbf { x } } _ { \mathrm { t a r } } , \hat { \mathbf { x } } _ { \mathrm { i n t } } =\tag{3}
$$

$$
\operatorname * { a r g m i n } _ { \mathbf { x } _ { \mathrm { t a r } } , \mathbf { x } _ { \mathrm { i n t } } } \ \left\| \mathbf { y } - \mathbf { x } _ { \mathrm { t a r } } - \mathbf { x } _ { \mathrm { i n t } } \right\| _ { 2 } ^ { 2 } - \lambda _ { \mathrm { i n t } } \log p \left( \left| \mathbf { A } \mathbf { x } _ { \mathrm { i n t } } \right| \right) + \lambda _ { \mathrm { t a r } } \left\| \mathbf { F } \mathbf { x } _ { \mathrm { t a r } } \right\| _ { 1 } .
$$

where F represents the Fourier transform matrix, and A denotes the matrix corresponding to the short-time Fourier transform (STFT). $\lambda _ { \mathrm { i n t } }$ and $\lambda _ { \mathrm { t a r } }$ are introduced as regularization factors. Finally, we subtract the recovered interference from the observation to obtain the estimation of the target.

## B. Score-based Generative Networks

We propose the use of score-based generative networks to model the interference prior. Unlike many other generative networks that aim to model the log-probability of the data directly, log $p _ { \mathrm { d a t a } } ( \mathbf { x } )$ , score-based generative networks model the gradient of the log-probability distribution of the data samples, $\nabla _ { \mathbf { x } } \log p _ { \mathrm { d a t a } } ( \mathbf { x } )$ , referred to as the score function. This provides more flexibility in network architecture design compared to other generative networks, such as normalizing flows [18], where architectural constraints are imposed to ensure proper normalized distributions.

Score-based generative networks are commonly trained through denoising score matching [19]. This involves perturbing the data samples with various levels of additive Gaussian noise and training the network to estimate the gradients of these perturbed samples, effectively mapping them back to the clean data manifold. The process of generating new samples from the learned distribution typically involves iterative gradient-based approaches.

## C. Iterative Optimization Algorithm for Source Separation

We address (3) by employing an iterative optimization scheme. This process involves alternating between regularization and data consistency steps. Denote $\mathbf { C } _ { \mathrm { i n t } } ,$ the complex time-frequency representation of interference, and $\mathbf { c } _ { \mathrm { t a r } }$ , the sparse coefficients corresponding to the target signal in the range spectrum. During iteration k, the current magnitude time-frequency estimation of the interference, $| \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } | .$ , is obtained by moving the estimate from the previous iteration, $| \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 } |$ , towards the expected statistical features. Leveraging the pre-trained score-based generative network, s<sub>θ</sub>, where θ represents the learnable parameters of the network, acting as a gradient vector field, this process effectively steers the estimate towards the high-likelihood region within the data distribution, thereby refining the accuracy of the interference representation. The formulation of this update is as follows:

$$
\begin{array} { r } { \vert \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } \vert = \vert \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 } \vert + \lambda _ { \mathrm { i n t } } ^ { k } \mathbf { s } _ { \theta } \left( \vert \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 } \vert \right) , } \end{array}\tag{4}
$$

where ${ \lambda _ { \mathrm { i n t } } ^ { k } }$ specifies the step size taken in the gradient ascent process for the $k ^ { \mathrm { { t h } } }$ iteration. We then transform this back to the time domain via:

$$
\tilde { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } = \mathbf { A } ^ { - 1 } \left( \vert \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } \vert \cdot e ^ { \mathrm { j } \angle \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 } } \right) ,\tag{5}
$$

where ${ { \bf A } ^ { - 1 } }$ denotes the matrix corresponding to the inverse STFT, and $\angle \hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k - 1 }$ is the phase of the estimated interference from the previous iteration. Note that we chose not to model the phase representation of interference in the time-frequency domain, given its lack of structure. Rather, we implicitly update the phase through data consistency steps. Next, the estimated target signal is updated through a proximal step (employing soft thresholding in the range spectrum), then converted back to the time domain via the inverse Fourier transform matrix, $\mathbf { F } ^ { - 1 } \cdot \mathbf { A }$ data consistency step is subsequently performed in the time domain:

$$
\hat { \mathbf { x } } _ { \mathrm { t a r } } ^ { k } = \mathbf { F } ^ { - 1 } \Gamma _ { \lambda _ { \mathrm { t a r } } } \left( \hat { \mathbf { c } } _ { \mathrm { t a r } } ^ { k - 1 } \right) - \mu _ { \mathrm { t a r } } \left( \mathbf { F } ^ { - 1 } \Gamma _ { \lambda _ { \mathrm { t a r } } } \left( \hat { \mathbf { c } } _ { \mathrm { t a r } } ^ { k - 1 } \right) + \tilde { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } - \mathbf { y } \right) ,\tag{6}
$$

where $\Gamma _ { \lambda _ { \mathrm { t a t } } }$ symbolizes a soft thresholding operation, with the sparsity level set as $\lambda _ { \mathrm { t a r } }$ . The parameter $\mu _ { \mathrm { t a r } }$ adjusts the data consistency step, determining how much the estimated target signal should adhere to the observation. Following this, we perform a data consistency step on the estimated time-series interference. The formulation is as follows:

$$
\hat { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } = \tilde { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } - \mu _ { \mathrm { i n t } } \left( \hat { \mathbf { x } } _ { \mathrm { t a r } } ^ { k } + \tilde { \mathbf { x } } _ { \mathrm { i n t } } ^ { k } - \mathbf { y } \right) ,\tag{7}
$$

where the parameter $\mu _ { \mathrm { i n t } }$ tunes the data consistency level, controlling the degree to which the estimated interference matches the observed data in the time domain. For the next iteration, we initialize by transforming the estimates from the time domain to their respective domains: $\hat { \mathbf { C } } _ { \mathrm { i n t } } ^ { k } = \mathbf { A } \hat { \mathbf { x } } _ { \mathrm { i n t } } ^ { k }$ and $\hat { \mathbf { c } } _ { \mathrm { t a r } } ^ { k } = \mathbf { F } \hat { \mathbf { x } } _ { \mathrm { t a r } } ^ { k }$ . After the algorithm converges, we obtain the estimated time series interference $\hat { \bf x } _ { \mathrm { i n t } } .$ , which is then subtracted from the observation y to derive the target signal estimation.

Table 1. This table presents mean ∆SNR in dB for all baseline methods in comparison to the proposed method across different input SNR ranges.
<table><tr><td></td><td>SNR ranges</td><td rowspan="2">[−20, −15)</td><td rowspan="2">[−15,−10)</td><td rowspan="2">[−10, −5)</td><td rowspan="2">[−5,0)</td><td rowspan="2">[0,5)</td><td rowspan="2">[5, 10)</td><td rowspan="2">[10, 15)</td><td rowspan="2">[15, 20]</td></tr><tr><td>Methods</td><td></td></tr><tr><td colspan="2">Proposed</td><td>-0.062</td><td>0.984</td><td>4.068</td><td>6.404</td><td>7.843</td><td>8.172</td><td>6.987</td><td>1.503</td></tr><tr><td colspan="2">SALSA</td><td>-13.68</td><td>-11.37</td><td>-9.427</td><td>-8.147</td><td>-7.392</td><td>-7.911</td><td>-9.082</td><td>-11.01</td></tr><tr><td colspan="2">TD-Z</td><td>-26.33</td><td>-27.47</td><td>-29.07</td><td>-30.95</td><td>-32.85</td><td>-33.75</td><td>-33.18</td><td>-32.68</td></tr><tr><td colspan="2">TFD-Z</td><td>-9.66</td><td>-8.585</td><td>-9.215</td><td>-11.24</td><td>-11.75</td><td>-13.75</td><td>-17.13</td><td>-21.18</td></tr><tr><td colspan="2">CNN</td><td>-0.723</td><td>-0.633</td><td>-0.302</td><td>-0.514</td><td>-1.106</td><td>-2.083</td><td>-3.52</td><td>-5.936</td></tr></table>

![](images/15f6839174d666b014da78a4050c2cee6cfdbd6c6acbb92c6411f5d1278058e3.jpg)

![](images/3205bc54898e0c5f1713510620820bc229e3cb4e28c419436e76899d6ca22b43.jpg)

![](images/95aa4d6bd51784880ca2ad2282a5d538b463860e61baa898d55d8dff1a26b080.jpg)

![](images/4ad74c1981e7c4d73bf7bb560edd75da3b273c503447d77a268e52c4251b1c4c.jpg)  
Fig. 1. Histograms illustrate the distributions of ∆SNR in dB for input SNR ranges spanning from 15 to 20 dB.

![](images/fde3b80259c2f67e601b9a53a9050d10c4bd4df430ab01625aa4c20444ef386f.jpg)

## III. EXPERIMENTS AND RESULTS

## A. Simulated Dataset

The performance of our algorithm is trained and evaluated using a simulated dataset. This dataset is composed of fast-time ADC samples in the time domain. The dataset contains 10,000 training samples and 512 validation samples. Each data sample contains one interference with an interference-to-noise ratio (INR) of 20 dB and an arbitrary number of targets ranging from 1 to 10. These targets exhibit a wide range of signal-to-noise ratio (SNR), spanning from −20 dB to 20 dB. Additionally, our evaluation framework consists of 8 distinct test scenarios. In all these scenarios, we maintain consistent values for both the INR and the number of target signals to ensure comparability. The distinguishing factor across each scenario is the variation in target SNR, designed to assess the robustness of our approach under diverse conditions. Additionally, to enable a thorough analysis, we include a dataset of 512 test samples for each scenario.

## B. Training Strategy and Hyperparameter Tuning

We employ the score-based generative network architecture as outlined in Song et al. [15]. The initial training step involves applying STFT to the fast-time signals containing only interference. This procedure yields data samples, $| \mathbf { C } _ { \mathrm { { i n t } } } | .$ characterized by spatial dimensions of $6 6 ~ \times ~ 6 6$ pixels with a single channel. These data samples are then perturbed with additive Gaussian noise, where the noise level, $\sigma _ { m } ,$ is uniformly selected from a range of 0.01 to 50, resulting in the generation of perturbed counterparts, denoted as $| { \bf C } _ { \mathrm { i n t } } | ^ { \prime }$ Consequently, the network parameters are optimized using denoising score matching, which can be formulated as follows:

$$
\frac { 1 } { 2 L } \sum _ { m = 1 } ^ { L } \mathbb { E } _ { p _ { \mathrm { d a t } } ( | \mathbf { C } _ { \mathrm { i n t } } | ) } \mathbb { E } _ { p _ { \sigma _ { m } } \left( | \mathbf { C } _ { \mathrm { i n t } } | ^ { \prime } \Big | | \mathbf { C } _ { \mathrm { i n t } } | \right) } \left[ \left\| \mathbf { s } _ { \theta } ( | \mathbf { C } _ { \mathrm { i n t } } | ^ { \prime } ) + \frac { | \mathbf { C } _ { \mathrm { i n t } } | ^ { \prime } - | \mathbf { C } _ { \mathrm { i n t } } | } { \sigma _ { m } } \right\| _ { 2 } ^ { 2 } \right] .
$$

This loss aims to minimize the empirical average of the Euclidean distance between the score functions of the training samples and all the perturbations. Moreover, We utilize the Adam optimizer (with $\mathrm { l r } = \ 1 e ^ { - 4 } , \ \beta _ { 1 } \ = \ 0 . 9 , \ \beta _ { 2 } \ = \ 0 . 9 9 9$ $\epsilon ~ = ~ 1 e ^ { - 8 } )$ , and set the total number of training epochs to 1,000. Following this, we incorporate the learned score function into the iterative optimization process. The tuning of all the hyperparameters of the iterative optimization algorithm, including data consistency steps, regularization steps, and the total number of iterations, is conducted using validation samples. Specifically, we employ Bayesian optimization [20] to minimize the mean squared error (MSE) between the reconstructed and ground-truth interference in the time domain.

## C. Baselines

In this study, we evaluate our algorithm against various baselines. The first two baselines adhere to the model-based interference detection and cancellation method, which replaces removed signal samples with zeros. We selected two distinct implementations for comparison: one operating in the time domain, named TD-Z, and another in the magnitude time-frequency domain, named TFD-Z.

The third baseline adopts a data-driven strategy within a supervised learning framework, termed CNN, and uses MSE as the loss criterion. The training process involves mapping interference-contaminated complex time-frequency representations to their interference-only counterparts. Following this, the estimation of the target signal is then obtained by subtracting the interference estimation from the observation in the time domain. For the purpose of a fair comparison, it utilizes the same network architecture as the score-based generative network previously described.

The final baseline originates from the method in [9], named SALSA, addressing interference mitigation from a source separation perspective. This method assumes that both the target signal and interference exhibit sparsity within the range spectrum and time-frequency domain, respectively.

## D. Evaluation

We evaluate our proposed algorithm against the baselines by quantifying the SNR improvements after interference mitigation in the magnitude range spectrum, denoted as ∆SNR. Table 1 demonstrates that our method’s superiority over baseline methods in the scenario involving targets with low power. In other scenarios, our proposed method improves the SNR while all baseline methods reduce it. Furthermore, Fig 1 displays the distribution of ∆SNR within a scenario characterized by input SNR values ranging from 15 to 20 dB. Our method achieves more substantial SNR improvements. In scenarios like this, thresholding-based algorithms tend to underperform due to indistinguishable power levels of interference and target signals. Compared to SALSA, our method enhances performance by explicitly modeling interference rather than relying on hand-crafted prior assumptions. Additionally, Figure 2 illustrates that while CNN shows noteworthy performance, our method achieves performance gains by transitioning from implicit to explicit learning within deep learning frameworks.

![](images/7a675039949c366f856c784820a70374d58ef0cf0b37701ee258be1f257fdf6e.jpg)

![](images/455ed57f6afa056a17c00398551cbd6e800ecd9efb42975f90320387fe08e59d.jpg)  
Fig. 2. Experimental results of the proposed algorithm compared to CNN, highlighting the two highest-performing models selected for clear visualization. Two test samples, representing the performance within the magnitude range spectrum domain, have been chosen.

## IV. CONCLUSIONS AND DISCUSSIONS

In this work, we have demonstrated the effectiveness of using deep generative networks for modeling FMCW automotive radar interference. Future work will include real-world measured data and address computational complexity to ensure applicability in real-time applications, going beyond simulations for a more comprehensive evaluation.

## ACKNOWLEDGMENT

This work was funded by the RAISE collaboration framework between Eindhoven University of Technology and NXP, including a PPS-supplement from the Dutch Ministry of Economic Affairs and Climate Policy.

## REFERENCES

[1] M. Goppelt, H.-L. Blöcher, and W. Menzel, “Analytical investigation of mutual interference between automotive FMCW radar sensors,” in 2011 German Microwave Conference, 2011, pp. 1–4.

[2] S. Neemat, O. Krasnov, and A. Yarovoy, “An interference mitigation technique for FMCW radar using beat-frequencies interpolation in the stft domain,” IEEE Transactions on Microwave Theory and Techniques, vol. 67, no. 3, pp. 1207–1220, 2019. DOI: 10 . 1109 / TMTT. 2018 . 2881154.

[3] F. Laghezza, F. Jansen, and J. Overdevest, “Enhanced interference detection method in automotive FMCW radar systems,” in 2019 20th International Radar Symposium (IRS), 2019, pp. 1–7. DOI: 10.23919/ IRS.2019.8767459.

[4] R. H. Wu, J. Li, M. Brett, and M. A. Staudenmaier, Radar communication with interference suppression, US Patent App. 17/245,613, 2022.

[5] J. Li, J. Youn, R. Wu, J. Overdevest, and S. Sun, “Performance evaluation and analysis of thresholding-based interference mitigation for automotive radar systems,” arXiv preprint arXiv:2402.14018, 2024.

[6] L. H. Nguyen and T. D. Tran, “RFI-radar signal separation via simultaneous low-rank and sparse recovery,” in 2016 IEEE Radar Conference (RadarConf), 2016, pp. 1–5. DOI: 10.1109/RADAR.2016. 7485213.

[7] J. Su, H. Tao, M. Tao, L. Wang, and J. Xie, “Narrow-band interference suppression via RPCA-based signal separation in time–frequency domain,” IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, vol. 10, no. 11, pp. 5016–5025, 2017. DOI: 10.1109/JSTARS.2017.2727520.

[8] J. Ren, T. Zhang, J. Li, L. H. Nguyen, and P. Stoica, “RFI mitigation for UWB radar via hyperparameter-free sparse spice methods,” IEEE Transactions on Geoscience and Remote Sensing, vol. 57, no. 6, pp. 3105–3118, 2019. DOI: 10.1109/TGRS.2018.2880758.

[9] F. Uysal, “Synchronous and asynchronous radar interference mitigation,” IEEE Access, vol. 7, pp. 5846–5852, 2019. DOI: 10.1109/ ACCESS.2018.2884637.

[10] J. Wang, M. Ding, and A. Yarovoy, “Interference mitigation for FMCW radar with sparse and low-rank hankel matrix decomposition,” IEEE Transactions on Signal Processing, vol. 70, pp. 822–834, 2022. DOI: 10.1109/TSP.2022.3147863.

[11] J. Mun, S. Ha, and J. Lee, “Automotive radar signal interference mitigation using RNN with Self Attention,” in ICASSP 2020 - 2020 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020, pp. 3802–3806. DOI: 10 . 1109 / ICASSP40776.2020.9053013.

[12] J. Fuchs, A. Dubey, M. Lübke, R. Weigel, and F. Lurz, “Automotive radar interference mitigation using a convolutional autoencoder,” in 2020 IEEE International Radar Conference (RADAR), 2020, pp. 315–320. DOI: 10.1109/RADAR42522.2020.9114641.

[13] N.-C. Ristea, A. Anghel, and R. T. Ionescu, “Estimating the magnitude and phase of automotive radar signals under multiple interference sources with fully convolutional networks,” IEEE Access, vol. 9, pp. 153 491–153 507, 2021. DOI: 10.1109/ACCESS.2021.3128151.

[14] A. Fuchs, J. Rock, M. Toth, P. Meissner, and F. Pernkopf, “Complex-valued convolutional neural networks for enhanced radar signal denoising and interference mitigation,” in 2021 IEEE Radar Conference (RadarConf21), IEEE, 2021, pp. 1–6.

[15] Y. Song and S. Ermon, “Improved techniques for training score-based generative models,” in Advances in Neural Information Processing Systems 33, NeurIPS 2020, 2020.

[16] H. Chung, J. Kim, M. T. Mccann, M. L. Klasky, and J. C. Ye, “Diffusion posterior sampling for general noisy inverse problems,” in The Eleventh International Conference on Learning Representations, 2023.

[17] T. S. W. Stevens, H. van Gorp, F. C. Meral, et al., “Removing structured noise with diffusion models,” arXiv:2302.05290, 2023.

[18] I. Kobyzev, S. J. Prince, and M. A. Brubaker, “Normalizing flows: An introduction and review of current methods,” IEEE transactions on pattern analysis and machine intelligence, vol. 43, no. 11, pp. 3964–3979, 2020.

[19] P. Vincent, “A connection between score matching and denoising autoencoders,” in Neural computation, vol. 23, 2011.

[20] E. Bakshy, L. Dworkin, B. Karrer, et al., “Ae: A domain-agnostic platform for adaptive experimentation,” in Conference on neural information processing systems, 2018, pp. 1–8.