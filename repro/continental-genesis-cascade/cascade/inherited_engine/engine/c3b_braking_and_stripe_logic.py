"""
c3b_braking_and_stripe_logic.py  --  C-3 재검토: 자기장은 정말 빠른 확장의 반증인가?
================================================================================
사용자 지적 2개:
  (1) 자기 줄무늬가 빠른 확장의 *진짜* 반론인지 논리적으로 추적하라.
  (2) "초기 변화가 크다" = 급한 초기확장 이후 산맥이 밀리며 브레이크(감속) 걸리는 중.

--------------------------------------------------------------------------------
PART A — 논리 추적: 줄무늬는 (속도)x(역전지속시간)의 *곱* 만 측정한다.
--------------------------------------------------------------------------------
줄무늬 폭  W_i = v_i * dt_i   (확장속도 x i번째 chron 지속시간).
줄무늬 *공간 패턴* 은 시간의 공통 rescaling 에 대해 불변:
   v -> k v  AND  reversal timescale -> k x faster  =>  같은 W_i  (구별 불가).
따라서:
  - 균일 시간압축(모든 것이 k배 빠름)은 줄무늬로 절대 반증 불가.
  - 빠름을 반증하는 *하중* 은 줄무늬 기하가 아니라, 역전 시간표의 *독립적 절대연대*
    (방사성연대 K-Ar/Ar-Ar/U-Pb + 천문연대 astrochronology) 와 해양지각 방사성연대다.
  - 표준 dt(독립연대) 를 받으면: 줄무늬 폭비 = dt비 => v_i ~ 일정(steady).
    그러면 (감속+표준시계) 도 반증됨(폭/dt 가 능선쪽으로 줄지 않으니).
  => 결론: 줄무늬는 "감속(표준시계)" 과 "균일압축" 중 *전자만* 반증.
     "급한 초기 파열(가장 오래된 지각/대륙연변) + 이후 표준확장" 과
     "균일 시간압축" 은 줄무늬만으론 반증되지 않는다. (C-3 과잉결론 교정)

--------------------------------------------------------------------------------
PART B — 감속(브레이크) 모델: 급한 초기확장 + 재잼밍/조산 브레이크
--------------------------------------------------------------------------------
잼밍 틀과 정합: 빠른 상(언잼밍-액체화) 으로 시작 -> 감속하며 *재잼밍*(State3->4) +
조산(mountain building)이 운동량을 흡수 = 브레이크. 점성 브레이크 -> v(t)=v0 e^{-t/tau}.
누적 개방 s(t)=v0 tau (1-e^{-t/tau}), 총개방 s_inf=v0 tau.
"초기 변화 큼": 첫 tau 동안 1-1/e ~ 63% 개방.  에너지: (1/2)M v0^2 -> 조산 PE + 소산.

Pure numpy. Deterministic.
"""
import numpy as np

# --- GPTS2020 young C-seq durations (Myr), as in p8_magnetic_test ---
bounds=np.array([0.000,0.773,0.990,1.070,1.775,1.934,2.116,2.140,2.581,3.032,
                 3.116,3.207,3.330,3.596,4.187,4.300,4.493,4.631,4.799,4.896,
                 4.997,5.235,6.033])
dt=np.diff(bounds)

print("="*78)
print("PART A — Do magnetic stripes REALLY refute fast expansion? (logical trace)")
print("="*78)
v_std=18.0          # standard half-rate mm/yr
# Model H0: slow-standard. positions from ridge:
pos_std=np.cumsum(dt)*v_std
# Model "uniform compression": time k x faster AND spreading k x faster
k=50.0
dt_fast=dt/k                       # reversals 50x faster
v_fast=v_std*k                     # spreading 50x faster
pos_fast=np.cumsum(dt_fast)*v_fast
print(f"  H0 (slow-standard): v={v_std} mm/yr, reversal timescale=GTS2020")
print(f"  'uniform compression': v={v_fast:.0f} mm/yr, reversals {k:.0f}x faster")
print(f"  max |position difference| between the two models = {np.max(np.abs(pos_std-pos_fast)):.3e} km")
print(f"  => IDENTICAL stripe pattern. Stripes CANNOT distinguish them.")
print(f"  => The refutation of 'fast' lives in the INDEPENDENT absolute clock")
print(f"     (radiometric + astrochronology), NOT in stripe geometry.")

# What WOULD a decelerating model (with FIXED standard reversal timescale) predict?
# v_i decreasing toward ridge -> stripe width per chron W_i/dt_i decreasing toward ridge.
# (this is the testable signature IF the clock is fixed.)
print("\n  If reversal timescale is FIXED (standard dating):")
print("    - steady spreading  => W_i/dt_i = const  (observed, per literature)")
print("    - decelerating      => W_i/dt_i DECREASES toward ridge (NOT observed under std dating)")
print("    => stripes+std clock refute 'decelerating-with-standard-clock';")
print("       they do NOT refute 'rapid INITIAL rupture (oldest crust) + later standard spreading'.")

print("\n"+"="*78)
print("PART B — Decelerating 'braking' model (rapid initial + orogeny brake)")
print("="*78)
# exponential viscous brake: v(t)=v0 exp(-t/tau); choose to open the Atlantic half-width
s_inf=3.0e6          # Atlantic half-width ~3000 km in metres
for v0_m_per_yr, label in [(1.0,"fast initial 1 m/yr (~100x present)"),
                           (0.1,"0.1 m/yr (~10x present)")]:
    tau=s_inf/v0_m_per_yr           # yr  (since s_inf=v0*tau)
    t_half=tau*np.log(2)            # time to open half of total
    frac_in_tau=1-1/np.e
    print(f"\n  {label}:")
    print(f"    deceleration timescale tau = {tau/1e6:.2f} Myr   (total opening s_inf=3000 km)")
    print(f"    opening in first tau = {frac_in_tau*100:.0f}%  (=> 'change is large initially')")
    print(f"    half of opening done by t = {t_half/1e6:.2f} Myr")
    print(f"    present-day residual rate v(tau..) decays toward ~cm/yr (matches slow modern rates)")

# energy budget: (1/2) M v0^2  vs orogenic PE (lift mountain mass) + dissipation
print("\n  Energy budget (per unit ridge length, order-of-magnitude):")
rho=2900.0; H_litho=20e3            # detachment-thick slab ~20 km (C-1 viable depth)
M=rho*H_litho                       # mass per unit area being moved [kg/m^2]
v0=1.0/3.15e7                       # 1 m/yr in m/s
KE=0.5*M*v0**2                      # J/m^2
g=9.8; H_mtn=4000.0                 # mountain height built ~4 km
PE_oro=rho*H_mtn*g*(H_mtn/2)        # crude orogenic PE per unit area [J/m^2]
print(f"    slab KE at v0=1 m/yr      ~ {KE:.2e} J/m^2   (tiny: 1 m/yr is slow in m/s)")
print(f"    orogenic PE (4 km range)  ~ {PE_oro:.2e} J/m^2")
print(f"    => KE of a 1 m/yr slab is FAR below orogenic PE: at 1 m/yr the brake is trivial.")
print(f"       The momentum/energy for orogeny must come from the DRIVING (suction/gravity),")
print(f"       not inertia. 'Brake' = re-jamming raising friction + work against orogenic load,")
print(f"       i.e. the system leaves the liquefied low-friction window (C-1) and re-jams.")

np.savez("c3b_results.npz", pos_std=pos_std, pos_fast=pos_fast, dt=dt,
         k=k, v_std=v_std, s_inf=s_inf)
print("\nsaved -> c3b_results.npz")
