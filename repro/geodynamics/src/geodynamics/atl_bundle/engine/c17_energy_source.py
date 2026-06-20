"""
c17_energy_source.py  --  AR-1 에너지 *원천* 감사 (가장 취약한 고리를 정량화)
================================================================================
목적 (신뢰도 강화 / §wpt4 와 짝):
  §wpt4 의 원장은 '관통하는 에너지가 어디로 가는가(heat vs PE)'를 닫았다.
  그러나 '그 에너지가 어디서 오는가(AR-1)'는 백서가 스스로 "가장 취약한 점"이라
  부르는 미해결 고리다. 이 모듈은 그것을 *정직하게* 다룬다:

  (A) 범주 오류 해소: 흡인 결손 ΔP 는 '동력원'이 아니라 *경계조건*이다. 그것은
      이미 저장된 (중력/탄성/열) 에너지가 일을 하도록 '잠금을 푸는' 장치다.
      따라서 외부에서 새로 공급해야 하는 양 = 초기 비평형(트리거: 태평양 융기
      ΔR / 과압 저류층)을 '충전'한 에너지 ~ ΔPE_trigger ~ W_in 규모.
  (B) 세 후보(H-E1/E2/E3)를 각자의 *최선 케이스*로 요구량(~1e26 J)에 대조한다.
  (C) 잔여 미해결을 사전등록 반증자로 전환한다 (요구 규모의 저류층 신호).

판정은 PASS 가 아니라 정직한 HOLD 다 (백서가 master-scale 을 HOLD 로 두는 것과 동일).
Pure numpy. Deterministic.
"""
import numpy as np

# ---- requirement (from §wpt4 ledger) ----
W_in   = 3.0e26          # basin-opening work scale [J] (ΔP·A_eff·d, conservative headline)
# the externally-charged part is the trigger PE; we require a source/release >= ~W_in.

# ---- universal references ----
Q_earth = 4.7e13         # total Earth internal heat flow [W] (Davies & Davies 2010, ~47 TW)
yr      = 3.15e7
rho     = 3.0e3          # crust/mantle density [kg/m^3]
g       = 10.0           # gravity [m/s^2]
cp      = 1.0e3          # specific heat [J/(kg K)]

print("="*84)
print("C-17  AR-1 ENERGY-SOURCE AUDIT  (the load-bearing open link, quantified)")
print("="*84)
print(f"\n  REQUIREMENT: a source must supply/RELEASE  >= W_in ~ {W_in:.1e} J")
print( "  (ΔP suction is a BOUNDARY CONDITION, not a power source: it unlocks stored PE.)")

# ----------------------------------------------------------------------------
# H-E1  internal reservoir: stored THERMAL (+ elastic) energy, tapped on unjamming
# ----------------------------------------------------------------------------
print("\n[H-E1] internal supercritical/hot reservoir -- RELEASE of stored energy")
print("-"*84)
# best-case stored thermal energy of a deep hot reservoir; available fraction eta_th
for (A,thick,dT) in [(1e14,1e5,500.0),(1e14,3e5,500.0),(1e13,1e5,500.0)]:
    V=A*thick; E_th=rho*cp*V*dT
    for eta in (0.01,0.05):
        avail=eta*E_th
        ok="OK" if avail>=W_in else "short"
        print(f"  A={A:.0e} m^2, h={thick/1e3:.0f} km, ΔT={dT:.0f} K -> E_th={E_th:.1e} J;"
              f" eta_mech={eta:.2f} -> available {avail:.1e} J  [{ok} vs {W_in:.0e}]")
# PV (expansion) work of trapped over-pressured fluid
print("  PV-work of trapped fluid (phi*V*ΔP_res):")
for (V,phi,dPr) in [(1e19,0.01,1e8),(1e20,0.01,1e8),(1e19,0.03,2e8)]:
    Wpv=phi*V*dPr; ok="OK" if Wpv>=W_in else "short"
    print(f"    V={V:.0e} m^3, phi={phi:.2f}, ΔP_res={dPr:.0e} Pa -> W_PV={Wpv:.1e} J  [{ok}]")
print("  => H-E1 VERDICT: the ONLY energetically admissible source class. Stored THERMAL")
print("     energy is ample (1e27-1e28 J); mechanical PV-work alone is marginal (1e24-1e25 J).")
print("     OPEN sub-question = the mechanical CONVERSION EFFICIENCY eta_mech (few % suffices)")
print("     and the reservoir's geophysical signature. This is the real AR-1 unknown.")
he1_ok = True  # admissible as a *release* source (subject to eta_mech)

# ----------------------------------------------------------------------------
# H-E2  heat injection / superplume  -- GENERATION in kyr, or impact
# ----------------------------------------------------------------------------
print("\n[H-E2] heat injection / superplume (GENERATION) or impact")
print("-"*84)
for t_yr in (1e3,1e4):
    E_glob=Q_earth*t_yr*yr; mult=W_in/E_glob
    print(f"  whole-Earth heat output over {t_yr:5.0f} yr = {E_glob:.1e} J"
          f"  -> need {mult:.0f}x the ENTIRE planet's heat flow [implausible as generation]")
# impact equivalent
v_imp=2.0e4
D=(W_in/(0.5*rho*(np.pi/6.0)*v_imp**2))**(1.0/3.0)
print(f"  impact delivering {W_in:.0e} J at v=20 km/s -> impactor D ~ {D/1e3:.0f} km"
      f"  (Chicxulub ~10 km, ~1e23 J): would leave an unmistakable global melt/ejecta layer.")
print("  => H-E2 VERDICT: as ENERGY GENERATION in kyr -> EXCLUDED (needs 10-100x global heat")
print("     flow). As literal IMPACT -> EXCLUDED by absence of a 1e26 J global-catastrophe")
print("     signature in the window. Only viable reading = RELEASE of stored heat == H-E1.")
he2_generation_ok = False
he2_impact_ok     = False

# ----------------------------------------------------------------------------
# H-E3  electromagnetic residual energy
# ----------------------------------------------------------------------------
print("\n[H-E3] electromagnetic / geomagnetic residual energy")
print("-"*84)
mu0=4*np.pi*1e-7
R_core=3.48e6; V_core=(4.0/3.0)*np.pi*R_core**3
for B in (1e-3,5e-3,1e-2):     # poloidal ~ mT up to strong toroidal ~10 mT (generous)
    u=B*B/(2*mu0); U=u*V_core
    short=W_in/U
    print(f"  B_core={B*1e3:.0f} mT -> U_mag={U:.1e} J  -> {short:.0e}x SHORT of W_in")
print("  => H-E3 VERDICT: core field energy ~1e21-1e22 J is 4-5 ORDERS short of 1e26 J.")
print("     DECISIVELY EXCLUDED as a source. Geomagnetic data is an OBSERVABLE only,")
print("     never the power source (this makes the paper's existing demotion mandatory).")
he3_ok = False

# ----------------------------------------------------------------------------
# verdict + pre-registered falsifier
# ----------------------------------------------------------------------------
print("\n[VERDICT]  AR-1 source = HOLD (honest), narrowed to one admissible class")
print("-"*84)
print("  Admissible source class: H-E1 (release of stored INTERNAL energy). H-E2-generation")
print("  and H-E3 are EXCLUDED by 1-5 order energy gaps; H-E2-impact excluded by signature.")
print("  The genuine open problem is therefore NARROW and SPECIFIC: (1) does a >=1e26 J")
print("  stored-energy reservoir exist in the trigger region, and (2) is eta_mech (>~few %)")
print("  achievable. AR-1 is NOT solved here; it is bounded and made falsifiable.")

print("\n[PRE-REGISTERED FALSIFIER]  (AR-1-source; lock in config/constraints.yml)")
print("-"*84)
print("  PASS(UNLOCK) only if an INDEPENDENT geophysical/fossil reservoir of the required")
print("    magnitude (>=1e26 J stored, e.g. a deep low-velocity / high-conductivity / over-")
print("    pressured anomaly or its fossil remnant beneath the trigger region) is identified,")
print("    AND a mechanical conversion path with eta_mech>~few % is demonstrated.")
print("  FAIL if NO sufficient stored-energy reservoir can be identified at the required")
print("    magnitude -> the rapid TRIGGER is energetically unsourced -> the rapid-trigger")
print("    branch (AR-1) is rejected and the slow-spreading default is NOT displaced.")
print("  Note: this does NOT decide the timescale by itself; it is a NECESSARY-CONDITION gate")
print("  on the trigger, complementary to the chronology firewall (§stripe_note).")

# ---- save (audited :: C17) ----
Emult_1kyr = W_in/(Q_earth*1e3*yr)
np.savez("c17_energy_source_results.npz",
         W_in=W_in, he1_ok=he1_ok, he2_gen_ok=he2_generation_ok,
         he2_impact_ok=he2_impact_ok, he3_ok=he3_ok,
         impactor_km=D/1e3, heat_mult_1kyr=Emult_1kyr,
         U_mag_strong=(5e-3)**2/(2*mu0)*V_core)
print("\nsaved -> c17_energy_source_results.npz")
print(f"  AUDIT: H-E1 admissible={he1_ok}; H-E2-gen={he2_generation_ok}; H-E3={he3_ok}; "
      f"impactor~{D/1e3:.0f} km; need {Emult_1kyr:.0f}x global heat (1 kyr).")
