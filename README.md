# **MZI 분석: 위상차 기반 간섭 스위칭 검증**

# **1.개요**
이번에는 MZI(Mach-Zehnder Interferometer)에 대해서 알아보겠습니다. MZI는 두 개의 Y-junction(MMI)을 서로 다른 길이의 두 arm으로 연결한 구조로, 두 arm을 지나온 빛의 위상차에 따라 보강 또는 상쇄간섭이 발생합니다. 본 실습에서는 이 위상차 기반 간섭을 이용한 스위칭 동작을 검증하겠습니다.
현재 MZI는 Optical Modulator, Optical Switch, Filter 등으로 널리 사용되고 있습니다. 실제 소자에서는 Heater를 이용한 열광학 효과로 위상차를 동적으로 제어하지만, 본 실습 환경에서는 전기-열-굴절률 결합을 직접 다룰 수 없기 때문에 열광학 효과로 유도되는 위상차를 delta_length라는 변수를 도입하여 고정된 위상차를 임의로 부여하였습니다.
  
**파장(λ):** 1.55μm  
**delta_length:** 0.32μm  
**Splitter/Combiner:** MMI 1x2  
**Arm 간격(length_y):** 10μm  
**Arm 직선 결합구간(length_x):** 2.0μm  
**waveguide 물질:** Si  
**Cladding 물질:** SiO2  
  
이렇게 설계된 전체 구조의 크기는 padding 전 기준 93μm × 68μm입니다.  

# **2.수학적 모델링을 통한 이론적 예측**
MZI의 투과율은 두 arm을 지난 빛의 위상차에 의해 결정되며 이는 다음과 같은 식으로 표현이 됩니다.  
  
$$T(\lambda) = \cos^2\left(\frac{\Delta\phi}{2}\right), \quad \Delta\phi = \frac{2\pi}{\lambda} n_{eff} \Delta L$$  
  
완전한 상쇄간섭(T = 0)이 이루어질려면 Δφ = π(m = 0 기준)을 만족해야 합니다. 이를 위한 delta_length는 다음과 같이 역산됩니다.  
  
$$\Delta L = \frac{\lambda}{2 n_{eff}}$$  
  
n_eff를 약2.4 라는 근사값으로 가정을 하면 다음과 같습니다.  
  
$$\Delta L \approx \frac{1.55}{2 \times 2.4} \approx 0.323\mu m$$  
  
이를 바탕으로 delta_length = 0.32μm로 설정 하였으며, 1550nm 근처에서 상쇄간섭이 유도가 될 것으로 예측이 가능합니다.  
또한 이 구조의 파장 응답은 Ring Resonator의 FSR과 유사한 주기성을 가지며, 다음과 같이 예측할 수 있습니다.  
  
$$FSR_{MZI} \approx \frac{\lambda^2}{n_{eff} \cdot \Delta L} \approx \frac{1.55^2}{2.4 \times 0.32} \approx 3130nm$$  
해당 주기 3130nm는 관측 할려는 범위인 (1520~1580nm, 60nm)보다 훨씬 크기 때문에, 관측 구간 내에서는 하나의 dip만 관측될 것으로 예측이 됩니다.

# **3.시뮬레이션 세팅**
시뮬레이션 환경은 resolution 20~30, Gaussian Source(λ - 1.55μm, fwidth = 0.02)를 사용하였습니다.  
정규화 작업은 source-monitor의 거리를 reference(Straight_waveguide)와 동일하게 맞추어 정교화를 하였습니다.  
MZI는 splitter + com                                                                                                                                                                                          biner + 두 arm 구조로 인해 Racetrack Ring Resonator보다 도메인이 훨씬 크며(93 x 68μm) 이는 padding전 도메인의 크기 입니다. 이로인해 계산 시간이 굉장히 크게 증가하는 것을 확인하였고
![MZI_layout](./MZI_Layout.png)  
![MZI_spectrum](./MZI_spectrum.png)

