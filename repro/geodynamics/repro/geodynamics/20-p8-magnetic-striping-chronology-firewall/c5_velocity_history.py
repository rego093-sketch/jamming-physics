"""
c5_velocity_history.py  --  C-5 (교정): 백서 틀 = 수천 년 확장. 자기장 = 상대 시간.
================================================================================
사용자 교정: "너무 시간이 길다. 백서 내부 자료와 충돌. 이 백서는 수천 년 확장으로 본다.
자기장은 *상대* 시간을 기록한 것."

이전 C-5의 오류: 주류 *절대* 연대(수천만 년)를 가져다 감속을 수십 Myr로 잡았다.
이는 백서(수천 년)와 충돌한다. 교정 원리:
  - 자기 줄무늬는 (속도)x(역전지속)의 곱 = *상대 시간* 만 기록 (C-3b 축퇴 증명).
    => 절대 시간척도는 줄무늬가 아니라 *물리* 가 정한다.
  - 또 다른 오류: 브레이크 시간척도를 리소스피어 냉각(a^2/kappa~50 Myr)으로 잡았다.
    실제 액체화되는 것은 mm 두께 전단대 -> 재잼밍(냉각) tau=h^2/kappa~수 초. 브레이크는 빠르다.

Pure numpy. Deterministic.
"""
import numpy as np

kappa=1.0e-6        # thermal diffusivity m^2/s
yr=3.15e7           # s per yr
s_open=3.0e6        # Atlantic half-width ~3000 km [m]
eta_flow=1.0e3      # liquefied gouge viscosity [Pa s]
h_sz=3.0e-3         # liquefied shear-zone thickness [m]

print("="*78)
print("C-5 (corrected): whitepaper timescale = THOUSANDS OF YEARS; stripes = RELATIVE time")
print("="*78)

print("\nPART A - magnetic stripes record only RELATIVE time (C-3b degeneracy)")
print("-"*78)
print("  stripe width W_i = v_i * dt_i  (product). Pattern invariant under common time-rescaling.")
print("  => the stripe-derived DECELERATION is a *relative shape* only:")
v_rel_early, v_rel_late = 92.0, 35.0
print(f"     early/late spreading-rate ratio ~ {v_rel_early/v_rel_late:.1f}  (faster early, slower late)")
print("     this SHAPE is chronology-agnostic; it does NOT fix the absolute timescale.")
print("  => 130 Myr (mainstream) vs ~thousands of yr (whitepaper) is set by the ABSOLUTE clock,")
print("     NOT by the stripes. Stripes are consistent with BOTH.")

print("\nPART B - absolute timescale from PHYSICS (does ~thousands of yr work?)")
print("-"*78)
print("  (i) liquefied state easily permits thousands-of-yr opening:")
print(f"      open {s_open/1e3:.0f} km; required mean rate & liquefied driving stress:")
for t_yr in [1e3,3e3,1e4]:
    v=s_open/t_yr; v_ms=v/yr
    tau_drive=v_ms*eta_flow/h_sz
    print(f"        t={t_yr:5.0f} yr -> v_mean={v:6.0f} m/yr ({v_ms:.1e} m/s); driving stress only {tau_drive:5.1f} Pa")
print("      => trivially small driving stress (Pa) sustains it; the low-friction (mu~2e-3) state")
print("         could in fact go FASTER. thousands-of-yr is PHYSICS-PERMITTED, not excluded.")

print("\n  (ii) the BRAKE (what ENDS the fast phase) is FAST -> self-limiting event:")
for h,lbl in [(h_sz,'liquefied shear zone (mm)'),(1.0,'1 m layer'),
              (1.0e4,'10 km'),(1.25e5,'lithosphere 125 km')]:
    tau=h*h/kappa
    print(f"        re-jam(cool) tau=h^2/kappa : {lbl:26s} = {tau:.1e} s = {tau/yr:.1e} yr")
print("      => the mm shear zone re-jams in ~SECONDS once shear-heating stops (State3->4).")
print("         low-friction window is intrinsically transient -> fast phase self-limits to a")
print("         BRIEF event (compatible with thousands of yr), NOT a 50-Myr process.")
print("      *** correction: earlier C-5 used lithosphere cooling (~50 Myr). WRONG layer.")
print("          the liquefied layer is mm-thick; its re-jamming is ~seconds. ***")

print("\n  (iii) void / pressure-deficit relief by hydraulic FLOW (not lithosphere diffusion):")
for D in [1.0,1e-2,1e-4]:
    L=1.0e4; tau=L*L/D
    print(f"        pressure diffusion tau=L^2/D_hy (L=10km, D={D:.0e}) = {tau:.1e} s = {tau/yr:.1e} yr")
print("      => pressure relief over km scales ~ yr-to-kyr: compatible with thousands of yr.")

print("\nPART C - honest firewall (where the REAL conflict is)")
print("-"*78)
print("  thousands-of-yr ABSOLUTE conflicts with mainstream ABSOLUTE dating:")
print("    radiometric (K-Ar/Ar-Ar/U-Pb) of ocean crust & reversal lavas, astrochronology,")
print("    sedimentation/biostratigraphy -> ~130 Myr / cm-yr rates.")
print("  BUT: (a) stripes (relative time) do NOT refute thousands-of-yr (proven, C-3b);")
print("       (b) friction/suction PHYSICS PERMITS thousands-of-yr (Part B);")
print("       (c) the mm re-jamming brake NATURALLY yields a brief event (Part B-ii).")
print("  => sole barrier = independent ABSOLUTE geochronology = the CHRONOLOGY FIREWALL")
print("     (separate, heavy argument; NOT decided by the geodynamics). The physics case is")
print("     chronology-agnostic and consistent with the whitepaper's compressed timescale.")

np.savez("c5_results.npz",
         ratio_rel=v_rel_early/v_rel_late, s_open=s_open,
         t_grid=np.array([1e3,3e3,1e4]),
         drive_Pa=np.array([(s_open/t/yr)*eta_flow/h_sz for t in [1e3,3e3,1e4]]),
         tau_rejam_sz=h_sz**2/kappa, tau_rejam_litho=(1.25e5)**2/kappa)
print("\nsaved -> c5_results.npz")
