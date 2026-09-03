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

MZI = gf.components.mzi(
    delta_length=0.32,
    length_x=2.0,
    length_y=10
)
MZI = gf.add_padding_container(MZI, default=0, top=3, bottom=3, right=20, left=15)

sim_results = gm.get_simulation(
    component=MZI,
    resolution=20,   # 30 -> 20 (eps_averaging=False 대신 resolution으로 속도 보완)
    is_3d=False,
    extend_ports_length=0,
)
sim = sim_results['sim']
# eps_averaging은 기본값(True) 유지 - False로 하면 MMI 구조에서 flux=0 문제 발생 확인됨

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
flux_mzi_mon = sim.add_flux(
    Source_f, Source_width, nfreq,
    mp.FluxRegion(center=mp.Vector3(flux_out_x, 0, 0), size=mp.Vector3(0, 1.5, 0))
)

print('MZI 본 시뮬레이션 시작 (resolution=30, eps_averaging=False)...')
sim.run(
    until_after_sources=mp.stop_when_fields_decayed(
        dt=50,
        c=mp.Ez,
        pt=mp.Vector3(flux_out_x, 0, 0),
        decay_by=1e-4
    )
)

mzi_flux = np.array(mp.get_fluxes(flux_mzi_mon))
ref_flux = np.load("mzi_ref_flux.npy")
freqs = np.load("mzi_ref_freqs.npy")

s21 = 10 * np.log10(mzi_flux / ref_flux)
wavelengths = (1 / freqs) * 1000

if mp.am_master():
    plt.figure(figsize=(9, 5))
    plt.plot(wavelengths, s21, color='b', linewidth=1.0)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Normalized S21 (dB)")
    plt.title("Normalized MZI Spectrum (delta_L=0.32um)")
    plt.grid(True)
    plt.savefig("MZI_final_spectrum.png", dpi=150)
    plt.show()

    ratio = mzi_flux / ref_flux
    print("\nratio 범위:", ratio.min(), "~", ratio.max())
    print("dB 범위:", 10*np.log10(ratio.min()), "~", 10*np.log10(ratio.max()))

    np.save("mzi_flux.npy", mzi_flux)
    np.save("mzi_freqs.npy", freqs)
    print("MZI 데이터 저장 완료!")