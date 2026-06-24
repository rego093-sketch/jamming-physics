"""
c2_trigger.py  --  C-2 게이트: 안티포드 트리거 ΔR 이 Ω-NoGo 안에서 분리면을 항복시키나?
================================================================================
백서: 안티포드 인장 파열 -> 초기 void/ΔR. Ω-NoGo: deltaR_stop_km=50 (ΔR>50km면 STOP).
질문: 분리면(~12-26km, sigma' ~ 200-400 MPa)을 항복/모빌라이즈할 ΔR이 50km 미만인가?

물리(구각 막응력): 반경 R 구각에 반경방향 섭동 ΔR -> 막변형 ~ ΔR/R -> 막응력 σ_m=E ΔR/R.
초기화 ΔR(threshold) = R * σ_thr / E.
(트리거의 *기원* 은 외부/미설명 = R3; 여기서는 ΔR이 *경계 내* 이고 *충분* 한지만 채점.)
Pure numpy. Deterministic.
"""
import numpy as np
R=6.371e6; E=1.0e11        # Earth radius [m]; lithosphere Young modulus [Pa]
deltaR_stop=50e3           # Omega-NoGo: ΔR stop [m]

print("="*74); print("C-2 GATE: antipodal trigger ΔR vs Ω-NoGo (deltaR_stop=50 km)"); print("="*74)
print("  membrane stress σ_m = E·ΔR/R  =>  ΔR = R·σ_thr/E\n")
rows=[("tensile rupture init", 10e6),
      ("mid-crust σ' (12 km)", 200e6),
      ("deep σ' (26 km)",      400e6),
      ("Ω-NoGo deltaP cap",    500e6)]
for lbl,s in rows:
    dR=R*s/E
    tag = "PASS (<50km)" if dR<deltaR_stop else "FAIL (>50km)"
    print(f"  reach {lbl:22s} σ={s/1e6:4.0f} MPa -> ΔR={dR/1e3:6.2f} km   [{tag}]")
dR_init=R*10e6/E; dR_mob=R*400e6/E
print(f"\n  => initiation needs ΔR~{dR_init/1e3:.1f} km; full mobilization (deep) ΔR~{dR_mob/1e3:.0f} km.")
print(f"     BOTH < Ω-NoGo 50 km. GATE C-2: PASS (a sub-50km radial perturbation suffices).")
print(f"  HONEST: this shows a trigger of this SIZE is within bounds & sufficient; it does NOT")
print(f"          explain the trigger's ORIGIN (external input, risk R3).")
np.savez("c2_results.npz", dR_init=dR_init, dR_mob=dR_mob, deltaR_stop=deltaR_stop)
