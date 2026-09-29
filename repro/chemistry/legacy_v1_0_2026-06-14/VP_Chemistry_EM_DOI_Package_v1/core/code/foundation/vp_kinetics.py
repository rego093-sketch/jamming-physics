# -*- coding: utf-8 -*-
"""
vp_kinetics.py — VP 반응속도: 회전·열에너지가 속도를 정한다 (재현가능·인과적)
====================================================================
사용자 흐름: 회전에너지(온도) → 통계열역학 → 평형(어디) → 속도(얼마나 빨리).

핵심: 반응은 분자가 전이상태(결합이 √2로 늘어 끊어지는 지점; vp_unified_rupture)에
      도달해야 일어난다. 활성화에너지 Ea = 그 문턱. 충분한 열에너지를 가진 분자비율
      = 볼츠만 꼬리 exp(−Ea/RT). 온도가 이 비율과 충돌속도를 정함.

인과 사슬: 분자 열에너지(회전·진동·병진; vp_statistical) → 문턱 넘는 비율 exp(−Ea/RT)
      → 아레니우스 k=A·exp(−Ea/RT). 충돌속도 ∝ 평균속력 √(8kT/πm). 전이상태(아이링)
      k=(kT/h)·(q‡/q_R)·exp(−E0/RT) — 분배함수(엔트로피)와 연결.

등급: [F] 볼츠만 비율·아레니우스 온도의존·10K 2배칙·kT/h 인자·평균속력
      [F?] 충돌이론 절대속도(단면적 입력) · [O] 절대 Ea(전이상태 구조), 터널링
실행: python3 vp_kinetics.py   (표준 라이브러리만)
"""
import math
R = 8.314462; KB = 1.380649e-23; H = 6.62607015e-34; NA = 6.02214076e23

def boltzmann_fraction(Ea_kJ, T):
    """문턱 Ea 넘는 분자비율 exp(−Ea/RT)."""
    return math.exp(-Ea_kJ*1000/(R*T))

def arrhenius(A, Ea_kJ, T):
    return A*boltzmann_fraction(Ea_kJ, T)

def Q10(Ea_kJ, T):
    """온도 10K 올릴 때 속도배율 k(T+10)/k(T)."""
    return boltzmann_fraction(Ea_kJ,T+10)/boltzmann_fraction(Ea_kJ,T)

def mean_speed(mass_u, T):
    """평균 분자속력 √(8kT/πm) [m/s]."""
    m = mass_u/1000/NA
    return math.sqrt(8*KB*T/(math.pi*m))

def eyring_prefactor(T):
    """아이링 보편 진동수 인자 kT/h [1/s]."""
    return KB*T/H


def main():
    print("="*72)
    print("VP 반응속도 — 회전·열에너지가 속도를 정한다 (활성화 문턱)")
    print("="*72)
    print("\n원리: 반응=전이상태(√2 결합늘림) 도달. Ea=문턱. 넘는 비율=exp(−Ea/RT). 온도가 정함.")

    # ── 볼츠만 비율 ──
    print("\n[볼츠만 비율] 문턱 Ea 넘는 분자비율 exp(−Ea/RT)")
    print(f"  {'Ea[kJ/mol]':>11}{'298K':>12}{'400K':>12}{'600K':>12}")
    print("  "+"-"*47)
    for Ea in [20, 50, 100, 150]:
        f3=boltzmann_fraction(Ea,298); f4=boltzmann_fraction(Ea,400); f6=boltzmann_fraction(Ea,600)
        print(f"  {Ea:>11}{f3:>12.2e}{f4:>12.2e}{f6:>12.2e}")
    print("  → 높은 문턱일수록 넘는 비율 급감. 온도 올리면 비율 급증(지수적). [F]")
    print("    이것이 반응이 온도에 민감한 이유 — 열에너지(회전·진동·병진)의 볼츠만 꼬리.")

    # ── 10K당 2배 법칙 ──
    print("\n[온도 민감도] 10K 올릴 때 속도배율 (경험칙: ~2배)")
    print(f"  {'Ea[kJ/mol]':>11}{'298→308K':>11}{'배율':>8}")
    print("  "+"-"*30)
    for Ea in [30, 50, 80]:
        q=Q10(Ea,298)
        print(f"  {Ea:>11}{'×':>9}{q:>8.2f}")
    print("  → Ea≈50kJ서 ×1.9≈2 (상온 10K당 2배 경험칙 재현). 큰 Ea일수록 더 민감. [F]")

    # ── 아레니우스 플롯 ──
    print("\n[아레니우스 플롯] ln k vs 1/T 직선, 기울기 = −Ea/R")
    A=1e13; Ea=75
    print(f"  A={A:.0e}/s, Ea={Ea}kJ/mol:")
    print(f"  {'T[K]':>7}{'1000/T':>9}{'k[1/s]':>12}{'ln k':>9}")
    print("  "+"-"*38)
    pts=[]
    for T in [300, 400, 500, 700]:
        k=arrhenius(A,Ea,T); pts.append((1/T, math.log(k)))
        print(f"  {T:>7}{1000/T:>9.2f}{k:>12.2e}{math.log(k):>9.2f}")
    slope=(pts[-1][1]-pts[0][1])/(pts[-1][0]-pts[0][0])
    print(f"  기울기 = {slope:.0f} K = −Ea/R → Ea = {-slope*R/1000:.0f} kJ/mol (입력 {Ea} 회수) [F]")

    # ── 평균 분자속력 (충돌이론) ──
    print("\n[충돌이론] 충돌속도 ∝ 평균속력 √(8kT/πm)")
    print(f"  {'분자':<6}{'질량u':>7}{'298K[m/s]':>11}{'600K[m/s]':>11}")
    print("  "+"-"*36)
    for name,mu in [("H2",2.016),("N2",28.01),("O2",32.00),("CO2",44.01)]:
        print(f"  {name:<6}{mu:>7.1f}{mean_speed(mu,298):>11.0f}{mean_speed(mu,600):>11.0f}")
    print("  → 가벼울수록·뜨거울수록 빠름. 속력∝√T → 충돌빈도∝√T (지수항보다 약함). [F]")
    print("    실측 N2 298K ~475 m/s 일치. 충돌=열운동(병진에너지).")

    # ── 전이상태 이론 (아이링) ──
    print("\n[전이상태 이론] 아이링 k=(kT/h)·exp(ΔS‡/R)·exp(−ΔH‡/RT)")
    print(f"  보편 진동수 인자 kT/h (298K) = {eyring_prefactor(298):.2e} /s")
    print("  • kT/h ≈ 6×10¹²/s = 전이상태가 생성물로 넘어가는 보편 시도빈도(상온).")
    print("  • exp(ΔS‡/R): 활성화 엔트로피 — 전이상태의 회전·진동 분배함수에서(vp_equilibrium).")
    print("  • exp(−ΔH‡/RT): 활성화 엔탈피 문턱 — 볼츠만 비율.")
    print("  → 속도가 전이상태의 *엔트로피*(회전·진동 자유도)와 *엔탈피*(문턱)에서. 분배함수 통일.")

    # ── 촉매 ──
    print("\n[촉매] Ea 낮추기 → 속도 급증 (평형은 불변)")
    Ea0, Ea_cat = 100, 60
    speedup = boltzmann_fraction(Ea_cat,298)/boltzmann_fraction(Ea0,298)
    print(f"  Ea {Ea0}→{Ea_cat} kJ/mol (상온): 속도 ×{speedup:.1e}")
    print("  → 촉매는 문턱만 낮춤(ΔG는 불변) → 평형 위치 같고 도달만 빨라짐.")
    print("    전이금속 촉매(가변 산화수, vp_dblock): 전자 주고받아 대체 경로 제공.")

    # ── VP 통일 ──
    print("\n[VP 통일] 회전·열에너지 → 속도")
    print("  • 활성화 문턱 = 전이상태(√2 결합늘림, vp_unified_rupture) 도달 에너지.")
    print("  • 넘는 비율 = 열에너지(회전·진동·병진)의 볼츠만 꼬리 exp(−Ea/RT).")
    print("  • 온도가 비율(지수적)과 충돌속력(√T)을 정함 → 속도. 평형(방향)+속도(빠르기).")
    print("  • 회전에너지가 *어느 반응이*(평형) 더해 *얼마나 빨리*(속도)까지 정한다.")

    print("\n" + "="*72)
    print("등급: [F] 볼츠만 비율·아레니우스·10K 2배칙·kT/h 인자·평균속력")
    print("      [F?] 충돌 절대속도(단면적) · [O] 절대 Ea(전이상태 구조), 터널링")
    print("      핵심: 회전·열에너지가 속도 결정. 문턱 넘는 비율=볼츠만 꼬리, 온도가 정함.")
    print("="*72)


if __name__ == "__main__":
    main()
