# -*- coding: utf-8 -*-
"""
vp_equilibrium.py — VP 화학평형: 회전엔트로피가 반응방향 (재현가능·인과적)
====================================================================
사용자 흐름: 회전에너지(온도)를 잘 계산 → 통계열역학 → 화학평형. 회전·진동 분배함수의
      엔트로피가 ΔG=ΔH−TΔS를 통해 반응 방향·평형을 정한다.

핵심: 해리평형 분자⇌2원자. 결합엔탈피 ΔH(붙잡음)와 엔트로피 ΔS(흩어짐, 회전·병진)가
      ΔG=ΔH−TΔS에서 경쟁. 고온서 TΔS가 ΔH 이기면 해리. 평형상수 K=exp(−ΔG/RT).
      해리온도 T* = ΔH/ΔS (ΔG=0, K=1).

인과 사슬: 각 화학종 S°(병진 Sackur-Tetrode + 회전 분배함수 + 진동 + 전자겹침; vp_statistical).
      ΔS°=2S°(원자)−S°(분자). ΔH°=결합에너지. → K(T)·해리온도·반트호프 온도의존.

등급: [F] ΔS°(분배함수)·해리온도(ΔH/ΔS)·반트호프 · [F?] 절대 K(ΔH 입력 [CAL])
      [O] 다원자 비선형 정밀(회전 3D)·전자상관
실행: python3 vp_equilibrium.py   (표준 라이브러리만)
"""
import math
R = 8.314462; KB = 1.380649e-23; H = 6.62607015e-34; C_CM = 2.99792458e10
NA = 6.02214076e23; HC_K = H*C_CM/KB

def S_trans(mass_u, T=298.15, P=1e5):
    m = mass_u/1000/NA
    return R*(math.log((2*math.pi*m*KB*T/H**2)**1.5 * KB*T/P) + 2.5)

def S_rot_lin(B_cm, sigma, T=298.15):
    Trot = B_cm*HC_K
    return R*(math.log(T/(sigma*Trot)) + 1)

def S_vib(nu_cm, T=298.15):
    x = nu_cm*HC_K/T
    if x > 50: return 0.0
    return R*(x/(math.exp(x)-1) - math.log(1-math.exp(-x)))

def S_diatomic(B,nu,sigma,mass,g_el,T=298.15):
    return S_trans(mass,T)+S_rot_lin(B,sigma,T)+S_vib(nu,T)+R*math.log(g_el)

def S_atom(mass,g_el,T=298.15):
    return S_trans(mass,T)+R*math.log(g_el)

# 분자: (B,ν,σ,질량,g_el bond_kJ) · 원자: (질량, g_el)
DIATOM = {
 "H2": dict(B=60.85,nu=4401,sigma=2,mass=2.016, g_el=1, bond=436, atom_m=1.008, atom_g=2),
 "N2": dict(B=2.00, nu=2359,sigma=2,mass=28.01, g_el=1, bond=945, atom_m=14.01, atom_g=4),
 "O2": dict(B=1.44, nu=1580,sigma=2,mass=32.00, g_el=3, bond=498, atom_m=16.00, atom_g=9),
 "Cl2":dict(B=0.244,nu=560, sigma=2,mass=70.91, g_el=1, bond=243, atom_m=35.45, atom_g=4),
}
# 검증용 표준 엔트로피 [J/mol·K] (298K)
S_REF = {"H2":130.7,"N2":191.6,"O2":205.2,"Cl2":223.1,
         "H":114.7,"N":153.3,"O":161.1,"Cl":165.2}


def main():
    print("="*72)
    print("VP 화학평형 — 회전엔트로피가 반응방향을 정한다 (해리평형)")
    print("="*72)
    print("\n원리: 분자⇌2원자. 결합 ΔH(붙잡음) vs 엔트로피 ΔS(흩어짐, 회전·병진).")
    print("      ΔG=ΔH−TΔS. 고온서 TΔS>ΔH면 해리. 해리온도 T*=ΔH/ΔS.")

    # ── 엔트로피 검증 (분배함수) ──
    print("\n[엔트로피 검증] S°(298K) 분배함수 예측 vs 실측 [J/mol·K]")
    print(f"  {'화학종':<6}{'S예측':>8}{'S실측':>8}{'Δ':>7}")
    print("  "+"-"*30)
    for name,d in DIATOM.items():
        S = S_diatomic(d['B'],d['nu'],d['sigma'],d['mass'],d['g_el'])
        print(f"  {name:<6}{S:>8.1f}{S_REF[name]:>8.1f}  {(S-S_REF[name])/S_REF[name]*100:>+5.1f}%")
    for atom,(m,g) in [("H",(1.008,2)),("N",(14.01,4)),("O",(16.00,9)),("Cl",(35.45,4))]:
        S = S_atom(m,g)
        print(f"  {atom:<6}{S:>8.1f}{S_REF[atom]:>8.1f}  {(S-S_REF[atom])/S_REF[atom]*100:>+5.1f}%")
    print("  → 분자·원자 엔트로피가 분배함수에서. 원자는 병진+전자겹침만. [F]")

    # ── 해리평형 ──
    print("\n[해리평형] ΔS°·ΔH°·해리온도 T*=ΔH/ΔS (K=1 되는 온도)")
    print(f"  {'반응':<12}{'ΔS°[J/molK]':>12}{'ΔH°[kJ]':>9}{'해리온도T*[K]':>13}")
    print("  "+"-"*48)
    for name,d in DIATOM.items():
        S_mol = S_diatomic(d['B'],d['nu'],d['sigma'],d['mass'],d['g_el'])
        S_at = S_atom(d['atom_m'],d['atom_g'])
        dS = 2*S_at - S_mol           # J/mol·K
        dH = d['bond']*1000           # J/mol
        Tstar = dH/dS
        print(f"  {name+'→2'+name[:-1]:<12}{dS:>12.1f}{d['bond']:>9}{Tstar:>13.0f}")
    print("  → 강한결합(N2 945kJ)일수록 해리온도 높음. 엔트로피(흩어짐)가 고온서 해리 추진.")
    print("    N2 해리 ~8000K, H2 ~4400K, Cl2 ~2000K. 결합세기 순서. [F]+[CAL](ΔH)")

    # ── K(T) 온도의존 ──
    print("\n[평형상수 K(T)] H2⇌2H 의 온도의존 (반트호프)")
    d = DIATOM["H2"]; S_mol=S_diatomic(d['B'],d['nu'],d['sigma'],d['mass'],d['g_el'])
    S_at=S_atom(d['atom_m'],d['atom_g']); dS=2*S_at-S_mol; dH=d['bond']*1000
    print(f"  {'T[K]':>7}{'ΔG°[kJ]':>10}{'ln K':>9}{'해리경향':>10}")
    print("  "+"-"*38)
    for T in [298, 1000, 2000, 4000, 4417, 6000, 8000]:
        dG = dH - T*dS
        lnK = -dG/(R*T)
        tend = "분자" if lnK<-1 else ("평형" if lnK<1 else "원자(해리)")
        print(f"  {T:>7}{dG/1000:>10.0f}{lnK:>9.1f}{tend:>10}")
    print("  → 저온 분자 안정(ΔG>0, K작음), 고온 해리(ΔG<0, K큼). T*=4417K서 K=1.")
    print("    반트호프 d(lnK)/d(1/T)=−ΔH/R: 흡열해리는 고온서 진행(Le Chatelier).")

    # ── Le Chatelier (엔트로피 부호) ──
    print("\n[Le Chatelier] 온도가 평형을 미는 방향 = 엔트로피·엔탈피 경쟁")
    print("  • 해리(분자→2원자): ΔS>0(흩어짐)·ΔH>0(흡열) → 고온이 해리 추진.")
    print("  • Haber(N2+3H2→2NH3): ΔS<0(4몰→2몰)·ΔH<0(발열) → 고온이 역반응(NH3 분해).")
    print("    → 암모니아 합성은 저온 유리(평형). 단 속도 위해 타협온도+촉매(산업).")
    print("  • 회전·병진 엔트로피(분자수·질량·B)가 ΔS 부호를 정함 → 온도효과 방향.")

    # ── VP 통일 ──
    print("\n[VP 통일] 회전에너지 → 엔트로피 → 반응방향")
    print("  • 온도=회전에너지 척도(vp_statistical). 엔트로피=회전·진동·병진 분배함수.")
    print("  • ΔG=ΔH−TΔS: 결합(EM·√2)이 ΔH, 흩어짐(회전·병진)이 ΔS. 둘의 경쟁이 평형.")
    print("  • 회전에너지가 단순 열용량을 넘어 *어느 반응이 진행되는지*까지 정한다.")

    print("\n" + "="*72)
    print("등급: [F] ΔS°(분배함수)·해리온도(ΔH/ΔS)·반트호프·Le Chatelier 방향")
    print("      [F?] 절대 K(ΔH 입력 [CAL]) · [O] 다원자 비선형 정밀·전자상관")
    print("      핵심: 회전엔트로피가 반응방향 결정. 해리온도가 결합세기 순서로 [F].")
    print("="*72)


if __name__ == "__main__":
    main()
