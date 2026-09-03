import numpy as np
import sys

if not hasattr(np, "float_"):
    np.float_ = np.float64
if not hasattr(np, "int_"):
    np.int_ = np.int64
if not hasattr(np, "asfarray"):
    np.asfarray = lambda x, **kwargs: np.array(x, dtype=np.float64, **kwargs)

import meep as mp
import gdsfactory as gf
import gplugins.gmeep as gm
import matplotlib.pyplot as plt
from gdsfactory.generic_tech import get_generic_pdk

get_generic_pdk().activate()

# 1. Straight Waveguide 생성
# gdsfactory의 straight()는 기본적으로 o1 포트가 x=0에서 시작함
# MZI의 source(-18)가 이 범위 밖(왼쪽)에 있으므로, left padding을 넉넉히 줘야 함
c = gf.components.straight(length=130, width=0.5)
c = gf.add_padding_container(c, default=0, top=3, bottom=3, left=25, right=10)

sim_results = gm.get_simulation(
    component=c,
    resolution=20,   # 최종 MZI 시뮬레이션과 동일한 resolution
    is_3d=False
)
sim = sim_results['sim']
sim.eps_averaging = True

# 2. 좌표 정의 (MZI 코드와 100% 동일한 거리: 117)
src_x, flux_out_x = -18, 99
Source_f = 1 / 1.55
Source_width = 0.02

sim.sources = [
    mp.EigenModeSource(
        src=mp.GaussianSource(frequency=Source_f, fwidth=Source_width),
        center=mp.Vector3(src_x, 0, 0),
        size=mp.Vector3(0, 1.5, 0),
        direction=mp.X,
        eig_band=1
    )
]

nfreq = 500
flux_ref_mon = sim.add_flux(
    Source_f, Source_width, nfreq,
    mp.FluxRegion(center=mp.Vector3(flux_out_x, 0, 0), size=mp.Vector3(0, 1.5, 0))
)

# 3. 레이아웃 먼저 확인 (source/monitor가 PML 안에 안전하게 있는지)
sim.plot2D()
plt.savefig("MZI_Reference_Layout_check.png")

print('Reference 시뮬레이션 시작...')
sim.run(
    until_after_sources=mp.stop_when_fields_decayed(
        dt=50,
        c=mp.Ez,
        pt=mp.Vector3(flux_out_x, 0, 0),
        decay_by=1e-4
    )
)

# 4. Flux 데이터 저장 (racetrack 것과 겹치지 않게 파일명 구분!)
ref_flux = np.array(mp.get_fluxes(flux_ref_mon))
freqs = np.array(mp.get_flux_freqs(flux_ref_mon))

if mp.am_master():
    np.save("mzi_ref_flux.npy", ref_flux)
    np.save("mzi_ref_freqs.npy", freqs)
    print("MZI Reference 데이터 저장 완료! (mzi_ref_flux.npy)")