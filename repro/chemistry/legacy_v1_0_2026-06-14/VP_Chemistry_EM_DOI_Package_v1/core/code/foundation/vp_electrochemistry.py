# -*- coding: utf-8 -*-
"""
vp_electrochemistry.py — VP 전기화학: 전자(회전 덴트) 전달 (재현가능·인과적)
====================================================================
사용자 흐름: 양성자 전달(용액) → 전자 전달(전기화학). VP 핵심 직결:
      전자=앵커(회전 덴트), 전하=회전 방향(CW/CCW). 산화환원=회전 덴트 전달.

핵심: 산화환원 = 전자 전달. 표준환원전위 E°=전자 받으려는 경향(전기음성도·EA와 연결).
      전지전위 E°cell=E°(환원극)−E°(산화극)가 전달 추진. ΔG°=−nFE°(평형 틀 연결).
      Nernst E=E°−(RT/nF)lnQ — RT에 온도(회전에너지) 다시 등장.

인과 사슬: 전자=회전 덴트(vp 핵심). 금속 낮은 IE(쉽게 잃음)→음의 E°. 비금속 높은 EN
      (쉽게 받음)→양의 E°. E°cell→ΔG°=−nFE°→K=exp(nFE°/RT). Nernst 농도·온도 의존.

등급: [F] 전지전위(E°차)·ΔG=−nFE°·K from E°·Nernst·활동도서열 (전자전달 틀)
      [CAL] 개별 E°(원소 고유 IE·EA·용매화) · [O] 절대 E° 예측(용매화 정밀)
실행: python3 vp_electrochemistry.py   (표준 라이브러리만)
"""
import math
F = 96485.0      # 패러데이 상수 [C/mol]
R = 8.314462; T0 = 298.15

# 표준환원전위 E° [V] (수소 0 기준) — 활동도 서열
E_RED = [
 ("Li⁺/Li",-3.04,1),("K⁺/K",-2.93,1),("Ca²⁺/Ca",-2.87,2),("Na⁺/Na",-2.71,1),
 ("Mg²⁺/Mg",-2.37,2),("Al³⁺/Al",-1.66,3),("Zn²⁺/Zn",-0.76,2),("Fe²⁺/Fe",-0.44,2),
 ("Pb²⁺/Pb",-0.13,2),("H⁺/H₂",0.00,2),("Cu²⁺/Cu",0.34,2),("Ag⁺/Ag",0.80,1),
 ("Au³⁺/Au",1.50,3),("F₂/F⁻",2.87,2),
]

def cell_potential(E_cat, E_an):  return E_cat - E_an
def dG_from_E(n, E):  return -n*F*E            # J/mol
def lnK_from_E(n, E, T=T0):  return n*F*E/(R*T)
def nernst(E0, n, Q, T=T0):  return E0 - (R*T/(n*F))*math.log(Q)


def main():
    print("="*72)
    print("VP 전기화학 — 전자(회전 덴트) 전달, 전하=회전 방향")
    print("="*72)
    print("\n원리: 산화환원=전자 전달. 전자=앵커(회전 덴트). E°=전자 받으려는 경향.")

    # ── 활동도 서열 ──
    print("\n[표준환원전위 서열] E° = 전자 받으려는 경향 (IE·EN과 연결)")
    print(f"  {'반쪽반응':<12}{'E°[V]':>8}  경향")
    print("  "+"-"*34)
    for name,E,n in E_RED:
        tend = "잘 잃음(환원력↑금속)" if E<-0.5 else ("기준" if abs(E)<0.01 else "잘 받음(산화력↑)" if E>0.5 else "중간")
        print(f"  {name:<12}{E:>8.2f}  {tend}")
    print("  → 음의 E°(Li,K,Na): 낮은 IE로 전자 잘 잃음=강환원제(반응성 금속).")
    print("    양의 E°(F₂,Au,Ag): 높은 EN으로 전자 잘 받음=강산화제. IE·EN(vp_atom)과 연결. [CAL]")

    # ── 전지전위 ──
    print("\n[전지전위] E°cell = E°(환원극) − E°(산화극)")
    cells = [("다니엘 Zn|Cu",0.34,-0.76,2),("Zn|Ag",0.80,-0.76,2),
             ("Cu|Ag",0.80,0.34,2),("Mg|Cu",0.34,-2.37,2)]
    print(f"  {'전지':<14}{'E°cell[V]':>10}{'자발성':>8}")
    print("  "+"-"*34)
    for name,Ecat,Ean,n in cells:
        Ecell = cell_potential(Ecat,Ean)
        spont = "자발(>0)" if Ecell>0 else "비자발"
        print(f"  {name:<14}{Ecell:>10.2f}{spont:>8}")
    print("  → 다니엘전지 1.10V (실측 1.10 일치). E°cell>0이면 자발(전류 흐름). [F]")

    # ── ΔG°·K 연결 ──
    print("\n[자유에너지·평형상수] ΔG°=−nFE°, ln K = nFE°/RT")
    print(f"  다니엘전지(n=2, E°=1.10V):")
    dG = dG_from_E(2, 1.10); lnK = lnK_from_E(2, 1.10)
    print(f"    ΔG° = −nFE° = {dG/1000:.0f} kJ/mol (자발, 발열)")
    print(f"    ln K = nFE°/RT = {lnK:.1f} → K = {math.exp(min(lnK,700)):.1e} (완전히 정반응)")
    print("  → 전지전위가 자유에너지(vp_equilibrium 틀)·평형상수와 직결. ΔG=ΔH−TΔS와 통일. [F]")

    # ── Nernst 식 ──
    print("\n[Nernst 식] E = E° − (RT/nF)lnQ (농도·온도 의존)")
    print(f"  RT/F (298K) = {R*T0/F*1000:.1f} mV. E = E° − (0.0592/n)logQ.")
    print(f"  다니엘전지 E°=1.10V, n=2, 농도 변화:")
    print(f"  {'[Zn²⁺]/[Cu²⁺]':>14}{'Q':>8}{'E[V]':>9}")
    print("  "+"-"*32)
    for Q in [0.01, 1, 100]:
        E = nernst(1.10, 2, Q)
        print(f"  {Q:>14.2f}{Q:>8.2f}{E:>9.3f}")
    print("  → 생성물(Zn²⁺) 많을수록 E 감소(Le Chatelier). 농도가 전위 조절. [F]")

    # ── 온도 의존 (회전에너지) ──
    print("\n[온도 의존] Nernst의 RT — 온도(회전에너지)가 전위 민감도 정함")
    print(f"  Q=100일 때 전위의 온도 의존:")
    for T in [273, 298, 350]:
        E = nernst(1.10, 2, 100, T)
        print(f"    T={T}K: E={E:.4f}V (RT/nF={R*T/(2*F)*1000:.2f}mV)")
    print("  → 온도 높을수록 RT/nF 커져 농도 의존 강해짐. 회전에너지가 전기화학에도. [F]")

    # ── VP 통일 ──
    print("\n[VP 통일] 전하=회전, 전자 전달=회전 전달")
    print("  • 전자=앵커(회전 덴트), 전하=회전 방향(CW/CCW). 산화환원=회전 덴트 옮김.")
    print("  • 산화=전자 잃음(회전 내줌), 환원=전자 받음(회전 받음). E°=받으려는 경향.")
    print("  • E°cell→ΔG=−nFE°→K: 전기화학이 평형 틀(ΔG=ΔH−TΔS)과 하나.")
    print("  • Nernst RT: 온도(회전에너지)가 전위 조절. 양성자전달(pH)·전자전달(E°) 대칭.")

    print("\n" + "="*72)
    print("등급: [F] 전지전위·ΔG=−nFE°·K from E°·Nernst·활동도서열 (전자전달 틀)")
    print("      [CAL] 개별 E°(원소 고유) · [O] 절대 E° 예측(용매화 정밀)")
    print("      핵심: 산화환원=전자(회전 덴트) 전달. 전하=회전. 전위→ΔG→K 평형 통일.")
    print("="*72)


if __name__ == "__main__":
    main()
