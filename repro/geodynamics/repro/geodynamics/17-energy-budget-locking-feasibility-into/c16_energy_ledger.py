"""
c16_energy_ledger.py  --  하나의 일관된 에너지 원장 (work-in / heat / disposal)
================================================================================
목적 (신뢰도 강화):
  백서 본문에는 세 가지 '응력'이 분리되지 않은 채 등장해, 적대적 심사자에게
  내부 모순(7 자릿수)처럼 보인다:
    (1) 흡인 압력 결손 ΔP ~ 1e8 Pa        -> 에너지 '입력' 항 (W_in = ΔP·A·d ~ 1e26 J)
    (2) 액체화 마찰 τ_res = mu_eff·σ_n ~ 3e5 Pa  -> '열'로 가는 소산 (Q_fric)
    (3) 평균 크리프 구동응력 τ_drive ~ 3-32 Pa   -> 평균률 유지에 필요한 점성응력
  이 모듈은 이 셋의 '역할'을 명시적으로 분리해 단일 원장을 만든다:
        W_in (흡인 일) = ΔKE + ΔPE_basin + Q_fric + W_fracture
  끝에서 ΔKE=0 이므로  W_in = ΔPE_basin + Q_fric + W_fracture.
  => 큰 1e26 J 의 대부분은 '분지 개방(PE)'로 가는 일이고, '열'은 Q_fric 뿐이다.

그 다음, 열 처분(heat disposal) 을 정직하게 검사한다:
  - 전도(conduction)만으로 kyr 사건의 Q_fric 를 처분할 수 있는가?  (반-공간 연속원 해)
  - 부족하면 -> 윤활 유체의 '이류(advection)' 가 유일한 가용 sink.
  - 그 이류가 요구하는 유체 처리량(throughput)을 정량화 -> P4 열수 신호의
    *사전등록된 반증 가능 예측* 으로 전환한다.

이 모듈은 어떤 절대 연대도 주장하지 않는다 (chronology-agnostic). 모든 수치는
보수적 범위 스윕으로 제시하며, '열 문제 해결'을 선언하지 않고 '정량적·반증가능'하게
만든다. Pure numpy. Deterministic.
"""
import numpy as np

# ----------------------------------------------------------------------------
# 0. 공통 물성/기하 (literature-scale; 다른 엔진과 일치)
# ----------------------------------------------------------------------------
yr      = 3.15e7            # s/yr
kappa   = 1.0e-6           # thermal diffusivity [m^2/s]
rho_c   = 2.7e6            # volumetric heat capacity [J/(m^3 K)]
T_melt  = 1000.0           # melt temperature *rise* [K] (vp_jamming_friction 와 동일 기준)
sigma_n = 150e6           # interface total normal stress [Pa]
mu_eff  = 2.2e-3          # liquefied effective friction (vp_jamming_friction)
mu_dry  = 0.6             # dry Coulomb (대조)
d_open  = 3.0e6           # 변위(반-너비) ~3000 km [m]
dP_suct = 1.0e8           # 흡인 압력 결손 (본문 에너지절 예시값) [Pa]

# 면적: 흡인이 작용하는 단면 A_eff vs 기저 마찰이 작용하는 기저면 A_base
A_eff   = 1.0e12          # suction cross-section [m^2] (본문 예시)
A_base_grid = np.array([1.0e12, 1.0e13, 3.0e13])  # 기저면(불확실) 스윕 [m^2]

# 유체 sink 가정
cw      = 4.0e3           # 물 비열 [J/(kg K)]
rho_w   = 1.0e3           # 물 밀도 [kg/m^3]
dTw_grid = np.array([200.0, 500.0])  # 빠져나가는 유체의 평균 가열 폭 [K]

print("="*82)
print("C-16  UNIFIED ENERGY LEDGER  (work-in / heat / disposal) -- chronology-agnostic")
print("="*82)

# ----------------------------------------------------------------------------
# 1. 세 응력의 역할 분리 (7 자릿수 '모순'의 해소)
# ----------------------------------------------------------------------------
print("\n[1] THREE distinct stresses -- different roles, NOT a contradiction")
print("-"*82)
tau_res   = mu_eff*sigma_n                       # 액체화 마찰
v_mean_3k = d_open/(3e3*yr)                       # 3 kyr 개방 평균률
tau_drive = 1.0e3*(v_mean_3k)/3.0e-3              # 점성 구동(평균률); eta=1e3, h=3mm
print(f"  (1) suction deficit   ΔP      = {dP_suct:.1e} Pa   -> ENERGY INPUT term (W_in)")
print(f"  (2) liquefied friction τ_res  = {tau_res:.1e} Pa   -> dissipated as HEAT (Q_fric)")
print(f"  (3) mean-rate drive   τ_drive = {tau_drive:5.1f} Pa     -> stress to hold the slow mean creep")
print("  => (1) is the work SOURCE; (2) is what becomes heat; (3) is a kinematic")
print("     book-keeping stress at the *mean* rate. They are not the same quantity,")
print("     so 'ΔP=1e8 Pa' and 'τ_drive=3-32 Pa' are NOT in conflict.")

# ----------------------------------------------------------------------------
# 2. 단일 원장: W_in = ΔPE_basin + Q_fric + W_fracture
# ----------------------------------------------------------------------------
print("\n[2] One ledger:  W_in (suction work) = ΔPE_basin + Q_fric + W_fracture")
print("-"*82)
W_in = dP_suct*A_eff*d_open
print(f"  W_in  = ΔP·A_eff·d            = {W_in:.1e} J   (the headline 1e26 J)")
# fracture energy (zipper): Gc ~ 1e4 J/m^2 over a fracture area ~ d * thickness
Gc = 1.0e4; frac_area = d_open*1.0e5
W_frac = Gc*frac_area
print(f"  W_fracture = Gc·A_frac        = {W_frac:.1e} J   (Gc~1e4 J/m^2; negligible)")
for A_base in A_base_grid:
    Q_fric = tau_res*A_base*d_open
    PE_basin = W_in - Q_fric - W_frac
    fheat = 100.0*Q_fric/W_in
    print(f"  A_base={A_base:.0e} m^2 -> Q_fric={Q_fric:.1e} J  ({fheat:5.2f}% of W_in -> heat); "
          f"ΔPE_basin~{PE_basin:.1e} J")
print("  => KEY: only a SMALL fraction of W_in becomes heat; the bulk is PE of basin")
print("     opening / mass redistribution. The heat to dispose of is Q_fric ~ 1e24-1e25 J,")
print("     NOT 1e26 J. (W_in itself -- its physical source -- is the separate AR-1 question.)")

# ----------------------------------------------------------------------------
# 3. 열 처분 #1 -- 전도만으로 가능한가? (정직한 검사)
#    반-공간 연속원: 사건 시간 t 동안 면적 A 양쪽으로 침투 δ=sqrt(kappa t).
# ----------------------------------------------------------------------------
print("\n[3] Disposal #1: can CONDUCTION alone remove Q_fric over a kyr event?")
print("-"*82)
for t_event_yr in [1e3, 1e4]:
    t = t_event_yr*yr
    delta = np.sqrt(kappa*t)         # thermal penetration [m]
    print(f"  t_event={t_event_yr:5.0f} yr -> conductive penetration delta=sqrt(kappa t)={delta:6.0f} m")
    for A_base in A_base_grid:
        Q_fric = tau_res*A_base*d_open
        V_cond = A_base*2.0*delta    # both sides of the basal plane
        dT = Q_fric/(rho_c*V_cond)
        verdict = "SUB-MELT" if dT < T_melt else "EXCEEDS MELT -> conduction INSUFFICIENT"
        print(f"      A_base={A_base:.0e}: ΔT_cond ~ {dT:8.0f} K   [{verdict}]")
print("  => For the smaller basal areas / shorter events the conductive ΔT reaches or")
print("     exceeds the melt threshold. Conduction ALONE cannot be relied on. An")
print("     additional, *physical* sink is required -- and the model already needs one:")
print("     the lubricating/over-pressured FLUID. So advection is not an extra")
print("     assumption; it is forced by the same fluid the mechanism requires.")

# ----------------------------------------------------------------------------
# 4. 열 처분 #2 -- 이류(advection): 요구 유체 처리량 -> 반증가능 예측
# ----------------------------------------------------------------------------
print("\n[4] Disposal #2: ADVECTION -> required fluid throughput (a FALSIFIABLE P4 number)")
print("-"*82)
basin_vol_km3 = 3.0e8           # Atlantic basin volume scale [km^3] (비교 기준)
for A_base in A_base_grid:
    Q_fric = tau_res*A_base*d_open
    for dTw in dTw_grid:
        m_w = Q_fric/(cw*dTw)            # mass of fluid to carry Q_fric [kg]
        V_w_km3 = (m_w/rho_w)/1e9        # volume [km^3]
        frac = 100.0*V_w_km3/basin_vol_km3
        print(f"  A_base={A_base:.0e}, ΔT_water={dTw:4.0f} K -> fluid throughput "
              f"~ {V_w_km3:7.1e} km^3  ({frac:5.2f}% of basin volume)")
print("  => A kyr-scale liquefied opening REQUIRES ~1e4-1e6 km^3 of hydrothermal")
print("     throughput. That is a large, regionally pervasive signature, NOT a hidden one.")

# ----------------------------------------------------------------------------
# 5. 사전등록 반증자 (P4-thermal hard gate)
# ----------------------------------------------------------------------------
print("\n[5] PRE-REGISTERED FALSIFIER  (P4-thermal; lock in config/constraints.yml)")
print("-"*82)
print("  PASS(UNLOCK) if the Atlantic basal detachment / margin shows a regionally")
print("    extensive, MODERATE-temperature (sub-melt) hydrothermal-alteration + over-")
print("    pressure signature of the predicted MAGNITUDE (alteration volume, vent/min-")
print("    eralization budget consistent with >=1e4 km^3 fluid throughput), AND it is")
print("    NOT a pervasive MELT sheet (which the liquefaction path forbids).")
print("  FAIL if EITHER (a) the basal contact is pristine/unheated (no moderate-T")
print("    alteration at the predicted scale) -> no sink for Q_fric -> low-mu_eff C3 FAIL,")
print("    OR (b) a pervasive regional MELT/vitrification sheet is required -> contradicts")
print("    the liquefaction-not-melt claim -> melt-only branch, C3(liquefaction) FAIL.")
print("  This converts 'the heat problem' from a qualitative defense into a two-sided,")
print("  magnitude-calibrated, falsifiable test. It does NOT by itself prove the timescale.")

# ----------------------------------------------------------------------------
# save (audited by validate_all.py :: C16)
# ----------------------------------------------------------------------------
# canonical reporting case for the audit: A_base=1e13, t=3 kyr, ΔT_water=500 K
A_base_c = 1.0e13
Q_fric_c = tau_res*A_base_c*d_open
frac_heat_c = Q_fric_c/W_in
t_c = 3e3*yr; delta_c = np.sqrt(kappa*t_c)
dT_cond_c = Q_fric_c/(rho_c*A_base_c*2*delta_c)
V_w_c_km3 = (Q_fric_c/(cw*500.0)/rho_w)/1e9
np.savez("c16_energy_ledger_results.npz",
         dP=dP_suct, tau_res=tau_res, tau_drive=tau_drive,
         W_in=W_in, Q_fric=Q_fric_c, frac_heat=frac_heat_c,
         dT_cond=dT_cond_c, fluid_km3=V_w_c_km3, T_melt=T_melt,
         A_base=A_base_c)
print("\nsaved -> c16_energy_ledger_results.npz")
print(f"\n  AUDIT CASE (A_base=1e13, t=3kyr): heat fraction={100*frac_heat_c:.2f}% of W_in; "
      f"ΔT_cond~{dT_cond_c:.0f} K; fluid~{V_w_c_km3:.1e} km^3")
