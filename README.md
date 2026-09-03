# **MZI 분석: 위상차 기반 간섭 스위칭 검증**

# **1.개요**
이번에는 MZI(Mach-Zehnder Interferometer)에 대해서 알아보겠습니다. MZI는 두 개의 Y-junction(MMI)을 서로 다른 길이의 두 arm으로 연결한 구조로, 두 arm을 지나온 빛의 위상차에 따라 보강 또는 상쇄간섭이 발생합니다. 본 실습에서는 이 위상차 기반 간섭을 이용한 스위칭 동작을 검증하겠습니다.
현재 MZI는 Optical Modulator, Optical Switch, Filter 등으로 널리 사용되고 있습니다. 실제 소자에서는 Heater를 이용한 열광학 효과로 위상차를 동적으로 제어하지만, 본 실습 환경에서는 전기-열-굴절률 결합을 직접 다룰 수 없기 때문에 열광학 효과로 유돟되는 위상차를 delta_length라는 변수를 도입하여 고정된 위상차를 임의로 부여하였습니다.
  
**파장(λ):** 1.55μm  
**delta_length:** 0.32μm  
**Splitter/Combiner:** MMI 1x2  
**Arm 간격(length_y):** 10μm  
**Arm 직선 결합구간(length_x):** 2.0μm  
**waveguide 물질:** Si  
**Cladding 물질:** SiO2  
  
이렇게 설계된 전체 구조의 크기는 padding 전 기준 93μm × 68μm입니다.  

![MZI_layout](./MZI_Layout.png)  
![MZI_spectrum](./MZI_spectrum.png)

